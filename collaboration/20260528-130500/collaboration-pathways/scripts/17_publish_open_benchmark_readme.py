#!/usr/bin/env python3
"""17_publish_open_benchmark_readme.py - record + gate the repo-root open-benchmark README.

Publishes the Pathways -> MikeOSS collaboration offering README at repository root:
an open benchmarking tool riff on the Elite MegaLaw Benchmark satire, with direct
links to the Pathways v1.1.0 spec and all four assay pathways.

Producing pathway: Experience.Collaboration.OpenInvitation@v1
Stdlib only. No network.

Usage:
  17_publish_open_benchmark_readme.py              # validate README markers
  17_publish_open_benchmark_readme.py --sync-integrity  # post-seal: sync hash + file_count
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

REPO = Path(".")
SNAP = Path("collaboration/20260528-130500")
README = REPO / "README.md"
MANIFEST = SNAP / "attestations" / "CONTENT_MANIFEST.yaml"
SCRIPT = SNAP / "collaboration-pathways" / "scripts" / "17_publish_open_benchmark_readme.py"

MARKERS = [
    "An Open Benchmarking Tool for MikeOSS",
    "elite-megalaw-benchmark",
    "PATHWAYS_REFERENCE_v1.1.0.md",
    "Assay.Citation.VerifyFirst.v1.yaml",
    "Assay.Benchmark.Reproducible.v1.yaml",
    "Assay.Convergence.AnchoredAuthority.v1.yaml",
    "Assay.Provenance.RunManifest.v1.yaml",
    "authority-boundaries-for-ai",
    "SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md",
]


def validate_readme(text: str) -> list[str]:
    missing = [m for m in MARKERS if m not in text]
    return missing


def sync_integrity(text: str) -> tuple[str, str, str]:
    if not MANIFEST.is_file():
        raise SystemExit(f"missing manifest: {MANIFEST}")
    manifest = MANIFEST.read_text(encoding="utf-8")
    hm = re.search(r"^\s*hash:\s*([0-9a-f]{64})\s*$", manifest, re.M)
    fc = re.search(r"^file_count:\s*(\d+)\s*$", manifest, re.M)
    if not hm or not fc:
        raise SystemExit("could not parse bundle_root_hash or file_count from manifest")
    root_hash, file_count = hm.group(1), fc.group(1)
    text = re.sub(
        r"\*\*bundle_root_hash:\*\*\s*`[0-9a-f]{64}`",
        f"**bundle_root_hash:** `{root_hash}`",
        text,
    )
    text = re.sub(
        r"\*\*file_count:\*\*\s*\d+",
        f"**file_count:** {file_count}",
        text,
    )
    return text, root_hash, file_count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync-integrity", action="store_true")
    args = ap.parse_args()

    if not README.is_file():
        print(f"error: missing {README}", flush=True)
        return 1

    text = README.read_text(encoding="utf-8")
    missing = validate_readme(text)
    if missing:
        print("README validation failed; missing markers:", flush=True)
        for m in missing:
            print(f"  - {m}", flush=True)
        return 1

    if args.sync_integrity:
        text, root_hash, file_count = sync_integrity(text)
        README.write_text(text, encoding="utf-8")
        print(f"synced integrity: bundle_root_hash={root_hash} file_count={file_count}", flush=True)

    produced = [str(README), str(SCRIPT)]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")

    print("open-benchmark README: validated OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
