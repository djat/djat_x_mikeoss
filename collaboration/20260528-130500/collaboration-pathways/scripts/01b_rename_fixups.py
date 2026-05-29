#!/usr/bin/env python3
"""01b_rename_fixups.py - post-rename consistency fixups (Phase 1).

Two issues from the ordered catch-all:
  1. The journey action "OpenInvitationTransmission" became "OpenInvitationCollaboration"
     (redundant). Normalize to "OpenInvitation" and rename its file to match.
  2. One all-caps "TRANSMISSION" survived in a manifest comment -> "COLLABORATION".
Recorded as a Collaboration.Refactor.RenameTerm@v1 run.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
EXCLUDE = {"pathway-runs", "attestations", "scripts", ".git", ".obsidian"}
PRESERVE = {"Collaboration.Refactor.RenameTerm.v1.yaml",
            "Collaboration.Attestation.RecordPathwayRun.v1.yaml"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html"}
REPL = [
    ("OpenInvitationCollaboration", "OpenInvitation"),
    ("OpenInvitationTransmission", "OpenInvitation"),
    ("MIKEOSS TRANSMISSION", "MIKEOSS COLLABORATION"),
    ("TRANSMISSION", "COLLABORATION"),
]
RENAMES = [
    (f"{SNAP}/collaboration-pathways/pathways/Experience.Collaboration.OpenInvitationTransmission.v1.yaml",
     f"{SNAP}/collaboration-pathways/pathways/Experience.Collaboration.OpenInvitation.v1.yaml"),
]


def excluded(p: Path) -> bool:
    return p.name in PRESERVE or any(x in EXCLUDE for x in p.parts)


def main() -> int:
    changed, renamed = [], []
    for p in SNAP.rglob("*"):
        if not p.is_file() or excluded(p) or p.suffix not in TEXT_EXT:
            continue
        orig = p.read_text(encoding="utf-8")
        new = orig
        for a, b in REPL:
            new = new.replace(a, b)
        if new != orig:
            p.write_text(new, encoding="utf-8")
            changed.append(str(p))
    for old, new in RENAMES:
        if Path(old).exists():
            os.rename(old, new)
            renamed.append(new)
    print(f"fixups: {len(changed)} files, {len(renamed)} renamed")
    produced = renamed + [f"{SNAP}/collaboration-pathways/scripts/01b_rename_fixups.py"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
