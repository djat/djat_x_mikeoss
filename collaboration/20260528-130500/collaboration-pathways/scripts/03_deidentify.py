#!/usr/bin/env python3
"""03_deidentify.py - replace identifiable external entities with stable placeholders (Phase 2).

Producing pathway: Collaboration.Privacy.DeIdentify@v1.

The real names are NOT in this script - they are loaded from keys/subjects.private.json
(unsealed, gitignored), so this script's source (captured in the PathwayRun record) contains
no identifiable names and the sealed bundle never leaks them. Emits
identities/deidentification-map.json (placeholder -> {file, count}). MikeOSS (the addressee),
the Originator (the vouching issuer), and the public legal commons are NOT de-identified.
"""
import json
import os
import re
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
PRIVATE = Path("keys/subjects.private.json")
RUN_ID = os.environ.get("PATHWAY_RUN_ID", "")
EXCLUDE = {"pathway-runs", "scripts", "attestations", ".git", ".obsidian"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html"}

cfg = json.loads(PRIVATE.read_text(encoding="utf-8"))
LITERAL = cfg["replacements"]["literal"]
BOUNDARY = cfg["replacements"]["boundary"]
KIND = cfg["kinds"]

placeholder_sites: dict[str, dict[str, int]] = {}


def record(ph: str, fname: str, n: int) -> None:
    if n > 0:
        placeholder_sites.setdefault(ph, {})
        placeholder_sites[ph][fname] = placeholder_sites[ph].get(fname, 0) + n


def deidentify(text: str, fname: str) -> str:
    for old, ph in LITERAL:
        c = text.count(old)
        if c:
            text = text.replace(old, ph)
            record(ph, fname, c)
    for pat, ph in BOUNDARY:
        new, c = re.subn(pat, ph, text)
        if c:
            text = new
            record(ph, fname, c)
    return text


def excluded(p: Path) -> bool:
    return any(x in EXCLUDE for x in p.parts)


def main() -> int:
    files = [p for p in SNAP.rglob("*") if p.is_file()]
    files += [p for p in Path("tools").rglob("*") if p.is_file()]
    files += [Path("README.md"), Path("START_COLLABORATION_HANDOFF.prompt.md")]
    edited = []
    for p in files:
        if not p.exists() or excluded(p) or p.suffix not in TEXT_EXT:
            continue
        try:
            orig = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = deidentify(orig, str(p))
        if new != orig:
            p.write_text(new, encoding="utf-8")
            edited.append(str(p))

    out = SNAP / "identities" / "deidentification-map.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "produced_by_pathway": "Collaboration.Privacy.DeIdentify@v1",
        "pathway_run_id": RUN_ID,
        "note": "Placeholders key into the sealed lockboxes (identities/). MikeOSS, the Originator, and the public legal commons are not de-identified.",
        "placeholders": {
            ph: {
                "kind": KIND.get(ph, "unknown"),
                "total": sum(sites.values()),
                "sites": [{"file": f, "count": c} for f, c in sorted(sites.items())],
            }
            for ph, sites in sorted(placeholder_sites.items())
        },
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"de-identify: {len(edited)} files edited; placeholders: {sorted(placeholder_sites)}")
    produced = [str(out), f"{SNAP}/collaboration-pathways/scripts/03_deidentify.py",
                f"{SNAP}/collaboration-pathways/pathways/Collaboration.Privacy.DeIdentify.v1.yaml"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
