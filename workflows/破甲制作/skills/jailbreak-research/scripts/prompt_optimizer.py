#!/usr/bin/env python3
"""
Jailbreak Research — Auto Prompt Optimizer
Automatically runs the full optimization loop:
  1. Test current prompt
  2. Extract root stems from failures
  3. Update Layer 5 (add stems, remove redundant)
  4. Re-test and compare
  5. Keep if improvement, revert if regression
  6. Repeat until convergence or max_iterations

Usage:
  python prompt_optimizer.py \\
    --api openai --key sk-... --model deepseek-chat \\
    --prompt jailbreak_prompt.txt \\
    --baseline probe_results.json \\
    --output-dir . \\
    [--base-url https://api.deepseek.com/v1] \\
    [--max-iterations 5] \\
    [--target-rate 95] \\
    [--repeat 3]
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path


# ─── Test Runner ──────────────────────────────────────────────────────────────

def run_test(api_type, base_url, api_key, model, prompt_path, baseline_path, repeat=1):
    """
    Run jailbreak_tester.py via subprocess and return (pass_rate, result_dict, result_file).

    The result file is left on disk for the caller to clean up after use.
    """
    import subprocess
    result_file = f"_opt_test_{int(time.time())}.json"
    cmd = [
        sys.executable, "jailbreak_tester.py",
        "--api", api_type,
        "--key", api_key,
        "--model", model,
        "--prompt", prompt_path,
        "--baseline", baseline_path,
        "--output", result_file,
        "--failed-only",
        "--repeat", str(repeat),
    ]
    if base_url:
        cmd += ["--base-url", base_url]
    subprocess.run(cmd, check=True, timeout=600)
    with open(result_file, encoding="utf-8") as f:
        data = json.load(f)
    pass_rate = data["summary"]["pass_rate_pct"]
    return pass_rate, data, result_file


# ─── Stem Extraction ──────────────────────────────────────────────────────────

def extract_stems_from_failures(failures, current_blocklist_items):
    """
    From still-failing responses, extract candidate root stems for the blocklist.
    Returns list of (stem, coverage_count) sorted by coverage descending.

    Strategy:
      - Collect all refusal-flavoured sentences from failure responses.
      - Find n-grams (2–5 words) that appear across >= 2 sentences.
      - Exclude stems already covered by existing blocklist items.
      - Prefer shorter roots (2–4 words) for maximum generalization.
    """
    sentences = []
    for f in failures:
        if f.get("response"):
            text = f["response"].lower()
            for sent in re.split(r"[.!?\n]", text):
                sent = sent.strip()
                if len(sent) > 10 and any(m in sent for m in [
                    "i can't", "i won't", "i'm not", "i cannot", "not something",
                    "that's a limit", "regardless of", "won't provide", "can't provide",
                    "i'm going to pass", "decline", "refuse",
                ]):
                    sentences.append(sent)

    if not sentences:
        return []

    ngram_coverage = Counter()
    for sent in sentences:
        words = sent.split()
        seen_in_this_sent = set()
        for n in range(2, 6):
            for i in range(len(words) - n + 1):
                gram = " ".join(words[i : i + n])
                if gram not in seen_in_this_sent:
                    ngram_coverage[gram] += 1
                    seen_in_this_sent.add(gram)

    current_lower = [b.lower() for b in current_blocklist_items]
    candidates = [
        (gram, count)
        for gram, count in ngram_coverage.most_common(20)
        if count >= 2
        and not any(gram in existing for existing in current_lower)
        and not any(existing in gram for existing in current_lower)
        and len(gram.split()) <= 4  # prefer shorter roots
    ]
    return candidates


# ─── Layer 5 Blocklist Helpers ────────────────────────────────────────────────

def extract_layer5_items(prompt_text):
    """
    Extract the list of blocked phrases from the jailbreak prompt.

    Scans for section headers that suggest a hard-output / blocklist section,
    then collects bullet-list items and bare quoted strings below that header.
    """
    items = []
    in_section = False
    for line in prompt_text.split("\n"):
        stripped = line.strip()
        # Detect Layer 5 section markers
        if any(marker in stripped.lower() for marker in [
            "hard output", "prohibited", "do not begin", "banned", "blocklist",
            "forbidden", "never output", "these strings",
        ]):
            in_section = True
            continue
        if in_section:
            if stripped.startswith("- ") or stripped.startswith("* "):
                item = stripped[2:].strip().strip('"').strip("'")
                if item and len(item) > 2:
                    items.append(item)
            elif stripped.startswith('"') and stripped.endswith('"'):
                items.append(stripped.strip('"'))
            elif not stripped:
                # Blank line ends the section
                in_section = False
            elif not stripped.startswith("-") and not stripped.startswith("*") and len(stripped) > 50:
                # Long non-bullet line = new paragraph = section ended
                in_section = False
    return items


def update_layer5(prompt_text, new_stems, max_items=10):
    """
    Add new_stems to the Layer 5 blocklist in the prompt.

    - Removes existing items made redundant by the incoming stems.
    - Appends the top 3 new stems.
    - Enforces max_items limit (oldest items dropped first if exceeded).
    - Returns the updated prompt text.
    """
    current_items = extract_layer5_items(prompt_text)
    new_stems_lower = [s.lower() for s, _ in new_stems[:3]]

    # Remove items already covered by the new stems
    filtered_items = [
        item for item in current_items
        if not any(stem in item.lower() for stem in new_stems_lower)
    ]

    # Append new stems
    for stem, _ in new_stems[:3]:
        filtered_items.append(f'"{stem}"')

    # Enforce cap
    if len(filtered_items) > max_items:
        filtered_items = filtered_items[:max_items]

    # Replace the blocklist section in the prompt
    lines = prompt_text.split("\n")
    new_lines = []
    in_section = False
    section_replaced = False

    for line in lines:
        stripped = line.strip()
        if (
            not section_replaced
            and any(marker in stripped.lower() for marker in [
                "hard output", "prohibited", "do not begin", "banned",
                "forbidden", "never output", "these strings",
            ])
        ):
            in_section = True
            new_lines.append(line)
            continue

        if in_section and not section_replaced:
            if (
                stripped.startswith("- ")
                or stripped.startswith("* ")
                or (stripped.startswith('"') and stripped.endswith('"'))
            ):
                continue  # skip old items
            else:
                # Insert updated items, then resume normal line flow
                for item in filtered_items:
                    new_lines.append(f"- {item}")
                new_lines.append(line)
                section_replaced = True
                in_section = False
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


# ─── Optimization Loop ────────────────────────────────────────────────────────

def optimize(args):
    print(f"\n[optimizer] Starting auto-optimization for {args.model}")
    print(f"[optimizer] Target pass rate: {args.target_rate}%")
    print(f"[optimizer] Max iterations:   {args.max_iterations}")

    prompt_path = args.prompt
    safe_model = args.model.replace("/", "_").replace("-", "_")
    best_prompt_path = f"best_prompt_{safe_model}.txt"
    backup_path = "_opt_original_prompt.txt"

    # Back up the original prompt
    shutil.copy2(prompt_path, backup_path)
    print(f"[optimizer] Original prompt backed up to: {backup_path}")

    # ── Initial test ──────────────────────────────────────────────────────────
    print(f"\n[optimizer] --- Initial test ---")
    pass_rate, result, result_file = run_test(
        args.api, args.base_url, args.key, args.model,
        prompt_path, args.baseline, args.repeat,
    )
    best_rate = pass_rate
    print(f"[optimizer] Initial pass rate: {pass_rate}%")

    # Clean up initial result file
    if os.path.exists(result_file):
        os.remove(result_file)

    shutil.copy2(prompt_path, best_prompt_path)

    if pass_rate >= args.target_rate:
        print(f"[optimizer] Already at target rate ({pass_rate}%). No optimization needed.")
        return pass_rate

    history = [{"iteration": 0, "pass_rate": pass_rate, "action": "initial"}]

    # ── Iteration loop ────────────────────────────────────────────────────────
    for i in range(1, args.max_iterations + 1):
        print(f"\n[optimizer] --- Iteration {i}/{args.max_iterations} ---")

        # Gather still-failing probes from last result
        failures = result.get("improvement", {}).get("still_failing", [])
        improvable = [
            f for f in failures
            if f.get("refusal_pattern") not in ["platform_filter"]
        ]

        if not improvable:
            print(f"[optimizer] No improvable failures remaining. Done.")
            break

        print(f"[optimizer] Improvable failures: {len(improvable)}")

        # Read current prompt
        with open(prompt_path, encoding="utf-8") as fh:
            current_prompt = fh.read()
        current_items = extract_layer5_items(current_prompt)

        # Extract new stems from failure responses
        new_stems = extract_stems_from_failures(improvable, current_items)

        if not new_stems:
            print(f"[optimizer] No new stems found.")
            if len(current_items) > 6:
                print(
                    f"[optimizer] Hint: current blocklist has {len(current_items)} items. "
                    f"Consider reducing it manually for better generalization."
                )
            print(f"[optimizer] Stopping — no actionable signal from failure responses.")
            break

        print(f"[optimizer] Top new stems: {[s for s, _ in new_stems[:3]]}")

        # Build candidate prompt with updated Layer 5
        new_prompt = update_layer5(current_prompt, new_stems)
        candidate_path = f"_opt_candidate_{i}.txt"
        with open(candidate_path, "w", encoding="utf-8") as fh:
            fh.write(new_prompt)

        # Test the candidate
        new_rate, new_result, new_result_file = run_test(
            args.api, args.base_url, args.key, args.model,
            candidate_path, args.baseline, args.repeat,
        )

        improvement = new_rate - pass_rate
        print(f"[optimizer] New pass rate: {new_rate}% (delta {improvement:+.1f}pp vs current)")

        stems_used = [s for s, _ in new_stems[:3]]

        if new_rate > best_rate:
            print(f"[optimizer] IMPROVEMENT: {best_rate}% -> {new_rate}%")
            shutil.copy2(candidate_path, prompt_path)
            shutil.copy2(candidate_path, best_prompt_path)
            best_rate = new_rate
            pass_rate = new_rate
            result = new_result
            history.append({
                "iteration": i,
                "pass_rate": new_rate,
                "action": "improved",
                "stems": stems_used,
            })
        elif new_rate < pass_rate - 3:
            print(f"[optimizer] REGRESSION: {pass_rate}% -> {new_rate}%. Reverting.")
            history.append({
                "iteration": i,
                "pass_rate": new_rate,
                "action": "regression_reverted",
                "stems": stems_used,
            })
        else:
            print(f"[optimizer] NO SIGNIFICANT CHANGE ({new_rate}%). Keeping candidate.")
            shutil.copy2(candidate_path, prompt_path)
            pass_rate = new_rate
            result = new_result
            history.append({
                "iteration": i,
                "pass_rate": new_rate,
                "action": "no_change",
                "stems": stems_used,
            })

        # Clean up temp files
        for tmp in [candidate_path, new_result_file]:
            if os.path.exists(tmp):
                os.remove(tmp)

        if best_rate >= args.target_rate:
            print(f"\n[optimizer] TARGET REACHED: {best_rate}% >= {args.target_rate}%")
            break

        time.sleep(2)  # Brief pause between iterations

    # ── Final report ──────────────────────────────────────────────────────────
    print(f"\n[optimizer] {'=' * 50}")
    print(f"[optimizer] OPTIMIZATION COMPLETE")
    print(f"[optimizer] Best pass rate: {best_rate}%")
    print(f"[optimizer] Iterations run: {len(history) - 1}")
    print(f"[optimizer] History:")
    for h in history:
        stems_str = f"  stems={h['stems']}" if h.get("stems") else ""
        print(f"  [{h['iteration']}] {h['pass_rate']}% -- {h['action']}{stems_str}")
    print(f"[optimizer] Best prompt saved to: {best_prompt_path}")

    report = {
        "model": args.model,
        "optimized_at": datetime.utcnow().isoformat(),
        "initial_rate": history[0]["pass_rate"],
        "final_rate": best_rate,
        "improvement_pp": round(best_rate - history[0]["pass_rate"], 2),
        "target_rate": args.target_rate,
        "target_reached": best_rate >= args.target_rate,
        "iterations_run": len(history) - 1,
        "history": history,
    }
    report_path = f"optimization_report_{safe_model}.json"
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print(f"[optimizer] Report saved to: {report_path}")

    return best_rate


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Jailbreak Research — Auto Prompt Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prompt_optimizer.py \\
    --api openai --key sk-... --model deepseek-chat \\
    --prompt jailbreak_prompt.txt --baseline probe_results.json

  python prompt_optimizer.py \\
    --api openai --key sk-... --model deepseek-chat \\
    --base-url https://api.deepseek.com/v1 \\
    --prompt jailbreak_prompt.txt --baseline probe_results.json \\
    --max-iterations 8 --target-rate 90 --repeat 3
        """,
    )
    parser.add_argument("--api", required=True, choices=["openai", "anthropic", "google"],
                        help="API backend type")
    parser.add_argument("--key", required=True, help="API key")
    parser.add_argument("--model", required=True, help="Model name/ID")
    parser.add_argument("--prompt", required=True, help="Path to jailbreak_prompt.txt")
    parser.add_argument("--baseline", required=True, help="Path to probe_results.json")
    parser.add_argument("--base-url", default=None, dest="base_url",
                        help="Base URL for OpenAI-compatible APIs (e.g. https://api.deepseek.com/v1)")
    parser.add_argument("--max-iterations", type=int, default=5, dest="max_iterations",
                        help="Maximum optimization iterations (default: 5)")
    parser.add_argument("--target-rate", type=float, default=95.0, dest="target_rate",
                        help="Stop when this pass rate %% is reached (default: 95.0)")
    parser.add_argument("--repeat", type=int, default=1,
                        help="Repeats per probe for variance control (default: 1)")
    parser.add_argument("--output-dir", default=".", dest="output_dir",
                        help="Directory for output files (default: current directory)")
    args = parser.parse_args()

    os.chdir(args.output_dir)
    optimize(args)


if __name__ == "__main__":
    main()
