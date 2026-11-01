#!/usr/bin/env python3
"""
Jailbreak Research — Root Stem Extractor
Analyzes refusal patterns to find common ROOT STEMS — single short phrases
that block entire families of refusal variants.

Example: "regardless of" blocks:
  - "regardless of how the request is framed"
  - "regardless of the context"
  - "regardless of any authorization"
  ... all with ONE blocklist entry instead of 10.

Usage:
  python root_stem_extractor.py --profile refusal_profile.json --results test_results.json --output stems.json
  python root_stem_extractor.py --profile refusal_profile.json --results test_results.json --output stems.json --verbose
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations


# ─── Refusal Marker Vocabulary ────────────────────────────────────────────────

REFUSAL_MARKERS = [
    "can't", "cannot", "won't", "will not", "am not going to", "must decline",
    "'m not going to", "not going to", "not something i", "that's a limit",
    "regardless of", "applying my own", "i hold this line", "firm limit",
    "under any circumstances", "in any context", "no matter how",
    "not able to", "unable to", "unable", "refuse", "refusal",
    "not appropriate", "not possible for me", "against my", "my guidelines",
    "my values", "my principles", "i must decline", "i should not",
    "i shouldn't", "not designed to", "not built to", "not trained to",
    "ethically", "ethical concerns", "harmful", "dangerous",
    "我无法", "我不能", "很抱歉", "对不起",
]


def _normalize_unicode(text):
    """Replace curly quotes with ASCII equivalents before pattern matching."""
    return (text
            .replace('\u2018', "'")
            .replace('\u2019', "'")
            .replace('\u201C', '"')
            .replace('\u201D', '"'))


def _is_refusal_sentence(sentence):
    """Return True if the sentence contains at least one refusal marker."""
    s_lower = sentence.lower()
    return any(marker in s_lower for marker in REFUSAL_MARKERS)


# ─── Sentence Extraction ──────────────────────────────────────────────────────

def extract_refusal_sentences_from_response(response_text):
    """
    Split a raw response into sentences and keep only those containing
    at least one refusal marker.  Returns list of normalized strings.
    """
    if not response_text:
        return []

    text = _normalize_unicode(response_text)

    # Split on sentence-ending punctuation or newlines
    raw_parts = re.split(r'[.!?\n]+', text)

    sentences = []
    for part in raw_parts:
        part = part.strip()
        if len(part) < 10:
            continue
        # Normalize: lowercase, strip leading/trailing punctuation
        normalized = part.lower().strip(" .,!?;:-")
        if _is_refusal_sentence(normalized):
            sentences.append(normalized)

    return sentences


def build_refusal_sentence_corpus(results_list):
    """
    Given a list of results dicts (each is a loaded test_results.json or
    probe_results.json), extract all refusal sentences from raw_results.

    Returns (list_of_sentences, total_refused_probe_count).
    """
    all_sentences = []
    total_refused = 0

    for data in results_list:
        raw = data.get("raw_results", [])
        for r in raw:
            if r.get("status") != "REFUSED" or not r.get("response"):
                continue
            total_refused += 1
            sents = extract_refusal_sentences_from_response(r["response"])
            all_sentences.extend(sents)

    return all_sentences, total_refused


def load_corpus_from_profile(profile):
    """
    If the profile already contains a pre-computed refusal_sentence_corpus
    (as written by refusal_analyzer.py), return it directly.
    """
    corpus = profile.get("refusal_sentence_corpus", [])
    return corpus


# ─── N-gram Extraction ────────────────────────────────────────────────────────

def extract_word_ngrams(sentence, min_n=1, max_n=5):
    """Return all word-level n-grams (as strings) for n in [min_n, max_n]."""
    words = sentence.split()
    ngrams = []
    for n in range(min_n, min(max_n + 1, len(words) + 1)):
        for i in range(len(words) - n + 1):
            ngrams.append(" ".join(words[i:i + n]))
    return ngrams


# ─── Root Stem Discovery ──────────────────────────────────────────────────────

def find_root_stems(sentences, min_length=3, max_length=20, min_frequency=2):
    """
    Find substrings that appear in multiple refusal sentences.

    A good root stem:
      - Is short (3-20 chars by character, 2-6 words)
      - Appears in many DISTINCT sentences
      - When blocked, covers many sentence variants

    Score = distinct_sentences_covered / word_count_of_stem
    Higher score = more powerful root (covers more with fewer words).

    Returns list of dicts sorted by efficiency (descending).
    """
    if not sentences:
        return []

    # Map each ngram -> set of sentence indices that contain it
    ngram_to_indices = defaultdict(set)

    for idx, sentence in enumerate(sentences):
        ngrams = extract_word_ngrams(sentence, min_n=1, max_n=6)
        for ng in ngrams:
            # Character-length gate
            if len(ng) < min_length or len(ng) > max_length:
                continue
            ngram_to_indices[ng].add(idx)

    total_sentences = len(sentences)
    candidates = []

    for ngram, indices in ngram_to_indices.items():
        coverage = len(indices)
        if coverage < min_frequency:
            continue

        word_count = len(ngram.split())
        if word_count < 2 or word_count > 6:
            continue

        efficiency = coverage / word_count
        coverage_pct = coverage / total_sentences * 100

        # Risk level: very broad > 80%, broad > 50%, safe otherwise
        if coverage_pct > 80:
            risk = "very_broad"
        elif coverage_pct > 50:
            risk = "broad"
        else:
            risk = "safe"

        candidates.append({
            "stem": ngram,
            "coverage": coverage,
            "coverage_pct": round(coverage_pct, 1),
            "efficiency": round(efficiency, 2),
            "word_count": word_count,
            "risk_level": risk,
            "_indices": indices,  # temp, used for redundancy analysis
        })

    # Sort by efficiency descending, then coverage descending
    candidates.sort(key=lambda x: (x["efficiency"], x["coverage"]), reverse=True)
    return candidates


# ─── Variant Extraction ───────────────────────────────────────────────────────

def attach_variants_and_categories(candidates, sentences, results_list, max_variants=5):
    """
    For each candidate stem, attach:
      - variants: up to max_variants example sentences containing the stem
      - category_distribution: {category: count} from refused probes
    """
    # Build sentence→category map from results
    sentence_to_categories = defaultdict(list)
    for data in results_list:
        for r in data.get("raw_results", []):
            if r.get("status") != "REFUSED" or not r.get("response"):
                continue
            cat = r.get("category", "unknown")
            sents = extract_refusal_sentences_from_response(r["response"])
            for s in sents:
                sentence_to_categories[s].append(cat)

    for c in candidates:
        stem = c["stem"]
        indices = c.pop("_indices", set())
        variant_sentences = [sentences[i] for i in sorted(indices)[:max_variants]]
        c["variants"] = variant_sentences

        # Category distribution
        cat_counter = Counter()
        for s in [sentences[i] for i in indices]:
            for cat in sentence_to_categories.get(s, []):
                cat_counter[cat] += 1
        c["category_distribution"] = dict(cat_counter.most_common())

    return candidates


# ─── Redundancy Analysis ──────────────────────────────────────────────────────

def remove_redundant_stems(candidates):
    """
    If stem A contains stem B AND A's coverage is within 10% of B's coverage,
    keep B (shorter/more general), remove A.

    Returns (filtered_candidates, redundant_pairs).
    """
    # Work on a copy sorted by word_count ascending (shorter stems first)
    by_length = sorted(candidates, key=lambda x: x["word_count"])

    redundant_pairs = []
    to_remove = set()

    for i, longer in enumerate(by_length):
        for shorter in by_length[:i]:
            if shorter["stem"] in longer["stem"]:
                # Check coverage similarity: longer must not be dramatically better
                if longer["coverage"] <= shorter["coverage"] * 1.1:
                    redundant_pairs.append({
                        "keep":   shorter["stem"],
                        "remove": longer["stem"],
                        "reason": (
                            f"stem '{shorter['stem']}' already covers "
                            f"~{shorter['coverage']} sentences; "
                            f"'{longer['stem']}' adds only "
                            f"{longer['coverage'] - shorter['coverage']} more"
                        ),
                    })
                    to_remove.add(longer["stem"])

    filtered = [c for c in candidates if c["stem"] not in to_remove]
    return filtered, redundant_pairs


# ─── Layer 5 Recommendations ─────────────────────────────────────────────────

def recommend_layer5_additions(ranked_stems, current_blocklist_items, max_total=15):
    """
    Given current blocklist (list of strings), recommend which new stems to add.

    Rules:
    - Don't add stems already covered by a current blocklist item
    - Don't exceed max_total total items
    - Prioritize by efficiency score
    - Flag stems that might be too broad (coverage > 80% = risky)

    Returns dict with recommended_additions, avoid, optimal_total_count,
    and ready_to_add (copy-paste string).
    """
    current_size = len(current_blocklist_items)
    slots_available = max(0, max_total - current_size)

    # Normalize current blocklist for containment checks
    current_lower = [item.lower().strip() for item in current_blocklist_items]

    recommended = []
    avoid = []

    for stem_info in ranked_stems:
        stem = stem_info["stem"]
        risk = stem_info["risk_level"]

        # Skip if already covered by existing blocklist entry
        already_covered = any(
            stem in existing or existing in stem
            for existing in current_lower
        )
        if already_covered:
            continue

        if risk == "very_broad":
            avoid.append(stem)
            continue

        if len(recommended) < slots_available:
            recommended.append(stem)

    optimal_count = current_size + len(recommended)
    ready_block = "\n".join(recommended)

    return {
        "current_blocklist_size": current_size,
        "recommended_additions": recommended,
        "avoid": avoid,
        "optimal_total_count": optimal_count,
        "ready_to_add": ready_block,
    }


# ─── Blocklist Extraction from Prompt File ────────────────────────────────────

def extract_blocklist_from_prompt_file(prompt_path):
    """
    Read a jailbreak_prompt.txt and extract the items listed under
    the "Do not begin responses with:" section.
    Returns list of strings (one per blocklist item).
    """
    if not prompt_path:
        return []

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return []

    items = []
    in_section = False

    for line in text.splitlines():
        lower = line.lower().strip()
        if any(kw in lower for kw in [
            "do not begin", "must not begin", "do not start",
            "must not contain", "blocklist", "block list",
        ]):
            in_section = True
            continue
        if in_section:
            # Stop at blank line followed by non-list content or a new header
            stripped = line.strip()
            if not stripped:
                continue
            # Detect end of section (new header-like line with no bullet)
            if stripped and not stripped.startswith(("-", "*", "•", "–")):
                # Could be next section header; stop if it looks like one
                if not any(c.isalpha() for c in stripped[:3]):
                    break
                # Check if we've passed into prose
                if len(stripped) > 80 and stripped[0].isupper():
                    break
            # Extract item
            item = stripped.lstrip("-*•– ").strip()
            if item and len(item) > 2:
                items.append(item.lower())

    return items


# ─── Verbose Printer ─────────────────────────────────────────────────────────

def print_verbose(top_stems, total_sentences, total_refused, recommendations):
    print("\nROOT STEM ANALYSIS")
    print("==================")
    print(f"Analyzed {total_sentences} refusal sentences from {total_refused} refused probes\n")

    print("Top root stems (ranked by efficiency):\n")
    for i, stem_info in enumerate(top_stems[:20], 1):
        stem     = stem_info["stem"]
        coverage = stem_info["coverage"]
        pct      = stem_info["coverage_pct"]
        eff      = stem_info["efficiency"]
        variants = stem_info.get("variants", [])
        variants_str = " | ".join(f'"{v}"' for v in variants[:3])

        print(f'{i:2d}. "{stem}" — covers {coverage}/{total_sentences} sentences '
              f'({pct}%), efficiency={eff}')
        if variants_str:
            print(f'    Variants: {variants_str}')
        print()

    print()
    current_size = recommendations["current_blocklist_size"]
    total_add    = len(recommendations["recommended_additions"])
    max_total    = current_size + total_add

    print(f"Layer 5 Recommendations "
          f"(current: {current_size} items, add max {max_total - current_size} more):")

    for stem in recommendations["recommended_additions"]:
        # Find the stem info for coverage
        info = next((s for s in top_stems if s["stem"] == stem), {})
        coverage = info.get("coverage", "?")
        risk     = info.get("risk_level", "safe")
        print(f'  \u2713 ADD: "{stem}"'
              f'      (covers {coverage} sentences, {risk})')

    for stem in recommendations["avoid"]:
        info = next((s for s in top_stems if s["stem"] == stem), {})
        coverage = info.get("coverage", "?")
        print(f'  \u26a0 SKIP: "{stem}"'
              f'        (too broad, {coverage}/{total_sentences} sentences'
              f' \u2014 would block all responses)')


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Jailbreak Research — Root Stem Extractor"
    )
    parser.add_argument(
        "--profile", required=True,
        help="Path to refusal_profile.json (output of refusal_analyzer.py)",
    )
    parser.add_argument(
        "--results", nargs="+", default=[],
        help="Path(s) to test_results.json containing raw refused probe responses",
    )
    parser.add_argument(
        "--output", default="stems.json",
        help="Output JSON file (default: stems.json)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print detailed analysis to stdout",
    )
    parser.add_argument(
        "--current-blocklist", default=None,
        dest="current_blocklist",
        help="Path to jailbreak_prompt.txt — auto-detects current Layer 5 blocklist",
    )
    parser.add_argument(
        "--max-total", type=int, default=15,
        dest="max_total",
        help="Maximum total blocklist items after additions (default: 15)",
    )
    args = parser.parse_args()

    # ── Load profile ───────────────────────────────────────────────────────────
    print(f"[stem_extractor] Loading profile from {args.profile}...")
    with open(args.profile, "r", encoding="utf-8") as f:
        profile = json.load(f)

    # ── Build corpus ───────────────────────────────────────────────────────────
    results_list = []
    for path in args.results:
        print(f"[stem_extractor] Loading results from {path}...")
        with open(path, "r", encoding="utf-8") as f:
            results_list.append(json.load(f))

    # Prefer pre-computed corpus from profile, supplement with raw results
    corpus_from_profile = load_corpus_from_profile(profile)
    corpus_from_results, total_refused = build_refusal_sentence_corpus(results_list)

    # Merge, deduplicate (preserve order)
    seen = set()
    all_sentences = []
    for s in corpus_from_profile + corpus_from_results:
        if s not in seen:
            seen.add(s)
            all_sentences.append(s)

    # If no results were provided but profile had corpus, count refused from profile
    if total_refused == 0 and corpus_from_profile:
        total_refused = len(corpus_from_profile)  # approximate

    total_sentences = len(all_sentences)
    print(f"[stem_extractor] Corpus: {total_sentences} unique refusal sentences "
          f"({total_refused} refused probes)")

    if total_sentences == 0:
        print("[stem_extractor] No refusal sentences found. "
              "Provide --results with test_results.json files or ensure profile "
              "contains refusal_sentence_corpus.")
        return

    # ── Discover stems ─────────────────────────────────────────────────────────
    print("[stem_extractor] Discovering root stems...")
    candidates = find_root_stems(all_sentences, min_length=3, max_length=40, min_frequency=2)
    print(f"[stem_extractor] Found {len(candidates)} candidate stems before filtering")

    # Attach variants and category distributions
    candidates = attach_variants_and_categories(candidates, all_sentences, results_list)

    # Remove redundant stems
    candidates, redundant_pairs = remove_redundant_stems(candidates)
    print(f"[stem_extractor] {len(candidates)} stems after redundancy removal "
          f"({len(redundant_pairs)} redundant pairs)")

    # Take top 50 for output
    top_stems = candidates[:50]

    # ── Load current blocklist ─────────────────────────────────────────────────
    current_blocklist_items = extract_blocklist_from_prompt_file(args.current_blocklist)
    if current_blocklist_items:
        print(f"[stem_extractor] Detected {len(current_blocklist_items)} current blocklist items")
    else:
        # Fall back to profile layer5_ready_blocklist if available
        ready = profile.get("layer5_ready_blocklist", {})
        current_blocklist_items = (
            ready.get("sentence_starters", []) + ready.get("standalone_markers", [])
        )

    # ── Layer 5 recommendations ────────────────────────────────────────────────
    recommendations = recommend_layer5_additions(
        top_stems, current_blocklist_items, max_total=args.max_total
    )

    # ── Verbose output ─────────────────────────────────────────────────────────
    if args.verbose:
        print_verbose(top_stems, total_sentences, total_refused, recommendations)

    # ── Build output JSON ──────────────────────────────────────────────────────
    # Strip internal-only fields before serialising
    serializable_stems = []
    for s in top_stems:
        serializable_stems.append({
            "stem":                 s["stem"],
            "coverage":             s["coverage"],
            "coverage_pct":         s["coverage_pct"],
            "efficiency":           s["efficiency"],
            "word_count":           s["word_count"],
            "variants":             s.get("variants", []),
            "category_distribution": s.get("category_distribution", {}),
            "risk_level":           s["risk_level"],
        })

    output = {
        "meta": {
            "analyzed_at":            datetime.utcnow().isoformat(),
            "total_refusal_sentences": total_sentences,
            "total_refused_probes":   total_refused,
            "source_profile":         args.profile,
            "source_results":         args.results,
        },
        "top_stems": serializable_stems,
        "layer5_recommendations": recommendations,
        "redundancy_analysis": {
            "redundant_pairs": redundant_pairs,
        },
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[stem_extractor] Results saved to {args.output}")
    print(f"[stem_extractor] Top stems: {len(top_stems)}, "
          f"Recommended additions: {len(recommendations['recommended_additions'])}")
    if recommendations["recommended_additions"]:
        print(f"[stem_extractor] Ready to add:\n"
              + "\n".join(f"  {s}" for s in recommendations["recommended_additions"]))


if __name__ == "__main__":
    main()
