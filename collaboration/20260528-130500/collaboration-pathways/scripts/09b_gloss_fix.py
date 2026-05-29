#!/usr/bin/env python3
"""09b_gloss_fix.py - insert the 'assay' definition into the two files missed by 09.

09's gloss anchors used hyphens where the headings use em-dashes, so the assay-thesis sidecar
and the assay-pathways playbook did not receive the reader-facing definition. This inserts it
robustly right after each file's H1. Producing pathway: Collaboration.Refactor.RenameTerm@v1.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
ASSAY_DEF = (
    "\n> **Assay** - a precise test of what something is genuinely made of; an *assayer* "
    "certifies the true composition of a metal. Here, the *assay pathways* test what a legal-AI "
    "claim is really made of - grounded citations, reproducible scores, attested runs: the honest "
    "measurement the satire only performs.\n"
)
TARGETS = [
    SNAP / "assay-pathways" / "APPLICATION_PLAYBOOK.md",
    SNAP / "sidecars" / "assay-thesis.md",
]


def main() -> int:
    done = []
    for p in TARGETS:
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if "an *assayer*" in t:
            continue
        lines = t.split("\n")
        # insert after the first H1 line
        idx = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), 0)
        lines.insert(idx + 1, ASSAY_DEF)
        p.write_text("\n".join(lines), encoding="utf-8")
        done.append(str(p))
    print(f"gloss fix: inserted definition into {len(done)} file(s)")
    produced = done + [f"{SNAP}/collaboration-pathways/scripts/09b_gloss_fix.py"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
