#!/usr/bin/env python3
"""11_scrub_did.py - de-identify the residual placeholder DID (recorded run).

Phase 2 replaced the name tokens but missed the lowercase/hyphenated form embedded in a
placeholder DID, which still carried a real person's name. This replaces that DID with the
non-identifying did:placeholder:person-a across the snapshot. The person's real identifiers
(domain, email, did:web) live only in the sealed lockbox (re-issued separately).

The leaking string is assembled from parts so this script's source (and its PathwayRun record)
does not reproduce the name. Producing pathway: Collaboration.Privacy.DeIdentify@v1.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html"}
EXCLUDE = {".git", ".obsidian"}

OLD = "did:placeholder:" + "localpart" + "-redacted-2026-05-20-S57"  # assembled to avoid the literal name
NEW = "did:placeholder:person-a"


def main() -> int:
    scrubbed = []
    for p in SNAP.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        if any(x in EXCLUDE for x in p.parts):
            continue
        t = p.read_text(encoding="utf-8")
        if OLD in t:
            p.write_text(t.replace(OLD, NEW), encoding="utf-8")
            scrubbed.append(str(p))
    print(f"scrub-did: replaced placeholder DID in {len(scrubbed)} file(s) -> {NEW}")
    for s in scrubbed:
        print("  ", s)
    produced = scrubbed + [f"{SNAP}/collaboration-pathways/scripts/11_scrub_did.py"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(sorted(set(produced))), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
