#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate DSH workflow-lite (0.11.0) workflows, sync manifests, and pack .wflite.zip.

Usage:
    python scripts/pack_workflows.py          # Validate, update manifest.json, repack .wflite.zip
    python scripts/pack_workflows.py --check  # Read-only validation (exit non-zero on mismatch)
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS_DIR = os.path.join(REPO_ROOT, "workflows")

DSH_PLUGIN_VERSION = "0.11.0"
VALID_COLORS = {"blue", "green", "amber", "coral", "teal", "pink", "olive", "violet", "slate"}
VALID_ICONS = {"idea", "target", "terminal", "bug", "test", "database", "chart", "globe", "chat", "mail", "report"}
IGNORE_DIRS = {"__pycache__", ".git", ".work"}
IGNORE_EXTS = {".pyc", ".pyo"}


def discover_workflows():
    names = []
    for entry in sorted(os.listdir(WORKFLOWS_DIR)):
        full = os.path.join(WORKFLOWS_DIR, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "manifest.json")):
            names.append(entry)
    return names


def validate_version_doc(wf, vnum, vdata):
    errors = []
    if vdata.get("format") != 1:
        errors.append(f"{wf}/versions/{vnum}.json: format must be 1")
    if vdata.get("n") != vnum:
        errors.append(f"{wf}/versions/{vnum}.json: n={vdata.get('n')} != {vnum}")

    doc = vdata.get("document", {})
    nodes = doc.get("nodes", [])
    edges = doc.get("edges", [])
    node_ids = set()

    for node in nodes:
        nid = node.get("id")
        if not nid or nid in node_ids:
            errors.append(f"{wf}/versions/{vnum}.json: missing or duplicate node id {nid!r}")
        node_ids.add(nid)
        data = node.get("data", {})
        if node.get("type") == "wfNode":
            color = data.get("color")
            icon = data.get("icon")
            if color not in VALID_COLORS:
                errors.append(f"{wf}/versions/{vnum}.json: node {nid} invalid color {color!r}")
            if icon not in VALID_ICONS:
                errors.append(f"{wf}/versions/{vnum}.json: node {nid} invalid icon {icon!r}")
            prompt = data.get("prompt", "")
            if "\\n" in prompt:
                errors.append(f"{wf}/versions/{vnum}.json: node {nid} contains literal \\\\n in prompt")
            if re.search(r"[A-Za-z]:/(?:Users|WorkSpace|devtools|Documents|Desktop)", prompt):
                errors.append(f"{wf}/versions/{vnum}.json: node {nid} contains hardcoded local path")

    edge_ids = set()
    for edge in edges:
        eid = edge.get("id")
        if not eid or eid in edge_ids:
            errors.append(f"{wf}/versions/{vnum}.json: missing or duplicate edge id {eid!r}")
        edge_ids.add(eid)
        if edge.get("source") not in node_ids:
            errors.append(f"{wf}/versions/{vnum}.json: edge {eid} dangling source {edge.get('source')!r}")
        if edge.get("target") not in node_ids:
            errors.append(f"{wf}/versions/{vnum}.json: edge {eid} dangling target {edge.get('target')!r}")
        if "sourceHandle" not in edge or "targetHandle" not in edge:
            errors.append(f"{wf}/versions/{vnum}.json: edge {eid} missing sourceHandle/targetHandle")

    return errors, len(nodes), len(edges)


def iter_workflow_files(wdir):
    for dirpath, dirnames, filenames in os.walk(wdir):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS)
        for fn in sorted(filenames):
            if os.path.splitext(fn)[1] in IGNORE_EXTS:
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, wdir).replace(os.sep, "/")
            yield fp, rel


def process_workflow(wf, check_only=False):
    wdir = os.path.join(WORKFLOWS_DIR, wf)
    mpath = os.path.join(wdir, "manifest.json")
    zpath = os.path.join(WORKFLOWS_DIR, f"{wf}.wflite.zip")
    manifest = json.load(open(mpath, encoding="utf-8"))
    errors = []

    vfiles = sorted(
        glob.glob(os.path.join(wdir, "versions", "*.json")),
        key=lambda p: int(os.path.splitext(os.path.basename(p))[0]),
    )
    if not vfiles:
        return [f"{wf}: no versions/*.json found"], ""

    versions_meta = []
    latest_nodes, latest_edges = 0, 0
    for vf in vfiles:
        vnum = int(os.path.splitext(os.path.basename(vf))[0])
        vdata = json.load(open(vf, encoding="utf-8"))
        verrs, ncnt, ecnt = validate_version_doc(wf, vnum, vdata)
        errors.extend(verrs)
        latest_nodes, latest_edges = ncnt, ecnt
        versions_meta.append({
            "n": vnum,
            "createdAt": vdata.get("createdAt", 0),
            "note": vdata.get("note", ""),
            "nodeCount": ncnt,
        })

    # Collect skills metadata
    skills_dir = os.path.join(wdir, "skills")
    new_skills = []
    if os.path.isdir(skills_dir):
        existing_sources = {s["name"]: s.get("source", "user-agents") for s in manifest.get("skills", [])}
        for sname in sorted(os.listdir(skills_dir)):
            spath = os.path.join(skills_dir, sname)
            if not os.path.isdir(spath) or sname in IGNORE_DIRS:
                continue
            files_meta = []
            for fp, rel in iter_workflow_files(spath):
                raw = open(fp, "rb").read()
                files_meta.append({
                    "path": rel,
                    "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                })
            files_meta.sort(key=lambda x: x["path"])
            new_skills.append({
                "name": sname,
                "source": existing_sources.get(sname, "user-agents"),
                "files": files_meta,
            })

    if check_only:
        if manifest.get("plugin") != DSH_PLUGIN_VERSION:
            errors.append(f"{wf}/manifest.json: plugin={manifest.get('plugin')} != {DSH_PLUGIN_VERSION}")
        if manifest.get("current") != versions_meta[-1]["n"]:
            errors.append(f"{wf}/manifest.json: current={manifest.get('current')} != {versions_meta[-1]['n']}")
        if manifest.get("versions") != versions_meta:
            errors.append(f"{wf}/manifest.json: versions metadata out of sync with versions/*.json")
        if manifest.get("skills", []) != new_skills:
            errors.append(f"{wf}/manifest.json: skills hashes/files out of sync with skills/")
        if not os.path.isfile(zpath):
            errors.append(f"{wf}: missing {os.path.basename(zpath)}")
        else:
            with zipfile.ZipFile(zpath, "r") as zf:
                expected = {f"{wf}/{rel}": open(fp, "rb").read() for fp, rel in iter_workflow_files(wdir)}
                actual = {n: zf.read(n) for n in zf.namelist() if not n.endswith("/")}
                if set(expected.keys()) != set(actual.keys()):
                    errors.append(f"{wf}.wflite.zip: file list differs from directory")
                else:
                    for k, v in expected.items():
                        if actual[k] != v:
                            errors.append(f"{wf}.wflite.zip: content differs for {k}")
        summary = f"[CHECK] {wf}: v{versions_meta[-1]['n']} ({latest_nodes} nodes / {latest_edges} edges)"
        return errors, summary

    # Sync manifest.json
    manifest["format"] = 1
    manifest["kind"] = "dsh-workflow-lite.workflow"
    manifest["plugin"] = DSH_PLUGIN_VERSION
    manifest["exportedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    manifest["current"] = versions_meta[-1]["n"]
    manifest["versions"] = versions_meta
    manifest["skills"] = new_skills

    with open(mpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Pack .wflite.zip
    file_count = 0
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for fp, rel in iter_workflow_files(wdir):
            zf.write(fp, f"{wf}/{rel}")
            file_count += 1

    summary = (
        f"[PACKED] {wf}: plugin={DSH_PLUGIN_VERSION}, current=v{manifest['current']}, "
        f"nodes={latest_nodes}, edges={latest_edges}, zip_files={file_count}"
    )
    return errors, summary


def main():
    parser = argparse.ArgumentParser(description="Validate and pack DSH .wflite.zip workflows")
    parser.add_argument("--check", action="store_true", help="Read-only check mode (do not modify files)")
    args = parser.parse_args()

    all_errors = []
    for wf in discover_workflows():
        errs, summary = process_workflow(wf, check_only=args.check)
        print(summary)
        for e in errs:
            print(f"  ERROR: {e}")
        all_errors.extend(errs)

    if all_errors:
        print(f"\nFailed with {len(all_errors)} error(s).")
        sys.exit(1)
    print("\nAll workflows passed validation.")


if __name__ == "__main__":
    main()
