#!/usr/bin/env python3
"""12_redact_name_fragments.py - redact residual name fragments from de-id provenance (recorded run).

The DID scrub (11) assembled its search string from parts, leaving readable name fragments in its
own source and run record. This loads those fragments from keys/.scrub_token.json (gitignored,
never sealed) and replaces them across the snapshot, so a grep of the sealed bundle returns no
readable name fragment. This script's own source contains no name (the fragments live only in the
gitignored key file). Producing pathway: Collaboration.Privacy.DeIdentify@v1.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html", ".py"}
EXCLUDE = {".git", ".obsidian"}

atoms = json.loads(Path("keys/.scrub_token.json").read_text(encoding="utf-8"))["atoms"]


def main() -> int:
    edited = []
    for p in SNAP.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        if any(x in EXCLUDE for x in p.parts):
            continue
        t = p.read_text(encoding="utf-8")
        nt = t
        for old, new in atoms:
            nt = nt.replace(old, new)
        if nt != t:
            p.write_text(nt, encoding="utf-8")
            edited.append(str(p))
    print(f"redact: removed residual fragments from {len(edited)} file(s)")
    for e in edited:
        print("  ", e)
    produced = edited + [f"{SNAP}/collaboration-pathways/scripts/12_redact_name_fragments.py"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(sorted(set(produced))), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
