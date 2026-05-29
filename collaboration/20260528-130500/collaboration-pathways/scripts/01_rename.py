#!/usr/bin/env python3
"""01_rename.py - full rename "transmission" -> "collaboration" (Phase 1).

Technique (encoded as Collaboration.Refactor.RenameTerm@v1): ordered token replacements
(specific before catch-all) across all text files, then file/dir renames. The OLD term is
deliberately re-introduced as a licensable Term artifact + lineage in the terms step, so
this is a name change WITH provenance, not erasure.

Excludes pathway-runs/ (immutable history), attestations/ (regenerated at reseal), and
scripts/ (their sha256 are already recorded in ASSET_PROVENANCE).
"""
import json
import os
from pathlib import Path

REPO = Path(".").resolve()
SNAP = Path("collaboration/20260528-130500")

# Ordered: specific identifier forms first, catch-all last.
REPLACEMENTS = [
    ("Transmission Bundle", "Collaboration Bundle"),
    ("transmission bundle", "collaboration bundle"),
    ("transmission-bundle", "collaboration-bundle"),
    ("TransmissionBundle", "CollaborationBundle"),
    ("TRANSMISSION_BUNDLE", "COLLABORATION_BUNDLE"),
    ("Collaboration.Transmission.", "Collaboration.Bundle."),
    ("subdomain: Transmission", "subdomain: Bundle"),
    ("transmission-spine", "collaboration-spine"),
    ("transmission-manifest", "collaboration-manifest"),
    ("transmission-pattern-lineage", "collaboration-pattern-lineage"),
    ("TRANSMISSION_READINESS", "COLLABORATION_READINESS"),
    ("START_TRANSMISSION_HANDOFF", "START_COLLABORATION_HANDOFF"),
    ("transmission/20260528-130500", "collaboration/20260528-130500"),
    ("transmission_kind", "collaboration_kind"),
    ("transmission_status", "collaboration_status"),
    # catch-all (act-of-transmitting noun) last
    ("Transmission", "Collaboration"),
    ("transmission", "collaboration"),
]

# (old_path, new_path) relative to repo root
FILE_RENAMES = [
    (f"{SNAP}/transmission-spine.md", f"{SNAP}/collaboration-spine.md"),
    (f"{SNAP}/transmission-manifest.yaml", f"{SNAP}/collaboration-manifest.yaml"),
    (f"{SNAP}/TRANSMISSION_READINESS.md", f"{SNAP}/COLLABORATION_READINESS.md"),
    (f"{SNAP}/collaboration-pathways/canon/TRANSMISSION_BUNDLE_TECHNIQUE.md",
     f"{SNAP}/collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md"),
    (f"{SNAP}/collaboration-pathways/sidecars/transmission-pattern-lineage-and-attribution.md",
     f"{SNAP}/collaboration-pathways/sidecars/collaboration-pattern-lineage-and-attribution.md"),
    (f"{SNAP}/collaboration-pathways/patterns/Pattern.TransmissionBundle.SelfDescribing.yaml",
     f"{SNAP}/collaboration-pathways/patterns/Pattern.CollaborationBundle.SelfDescribing.yaml"),
    (f"{SNAP}/collaboration-pathways/pathways/Collaboration.Transmission.RewriteLinks.v1.yaml",
     f"{SNAP}/collaboration-pathways/pathways/Collaboration.Bundle.RewriteLinks.v1.yaml"),
    (f"{SNAP}/collaboration-pathways/pathways/Collaboration.Transmission.SealBundle.v1.yaml",
     f"{SNAP}/collaboration-pathways/pathways/Collaboration.Bundle.SealBundle.v1.yaml"),
    (f"{SNAP}/collaboration-pathways/pathways/Collaboration.Transmission.VerifyBundle.v1.yaml",
     f"{SNAP}/collaboration-pathways/pathways/Collaboration.Bundle.VerifyBundle.v1.yaml"),
    ("START_TRANSMISSION_HANDOFF.prompt.md", "START_COLLABORATION_HANDOFF.prompt.md"),
    ("tools/transmission-bundle", "tools/collaboration-bundle"),
]

EXCLUDE_DIR_PARTS = {"pathway-runs", "attestations", "scripts", ".git", ".obsidian"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".sh", ".html", ".prompt"}
# Files that intentionally document BOTH the old and new term must not be token-replaced.
PRESERVE_NAMES = {
    "Collaboration.Refactor.RenameTerm.v1.yaml",
    "Collaboration.Attestation.RecordPathwayRun.v1.yaml",
}


def is_excluded(p: Path) -> bool:
    if p.name in PRESERVE_NAMES:
        return True
    return any(part in EXCLUDE_DIR_PARTS for part in p.parts)


def apply_replacements(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def main() -> int:
    changed, renamed = [], []
    # 1) token replacements across text files in snapshot + repo-root handoff prompt + tools
    roots = [SNAP, Path("tools")]
    files = []
    for r in roots:
        if r.exists():
            files += [p for p in r.rglob("*") if p.is_file()]
    files += [Path("README.md"), Path("START_TRANSMISSION_HANDOFF.prompt.md")]
    for p in files:
        if not p.exists() or is_excluded(p):
            continue
        if p.suffix not in TEXT_EXT and not p.name.endswith(".prompt.md"):
            continue
        try:
            orig = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = apply_replacements(orig)
        if new != orig:
            p.write_text(new, encoding="utf-8")
            changed.append(str(p))
    # 2) file/dir renames
    for old, new in FILE_RENAMES:
        op, np = Path(old), Path(new)
        if op.exists():
            np.parent.mkdir(parents=True, exist_ok=True)
            os.rename(op, np)
            renamed.append({"from": old, "to": new})

    print(f"rename: {len(changed)} files token-replaced, {len(renamed)} paths renamed")
    for r in renamed:
        print(f"  {r['from']} -> {r['to']}")

    # declare assets: renamed targets + this script + its template
    produced = [r["to"] for r in renamed]
    produced += [
        f"{SNAP}/collaboration-pathways/scripts/01_rename.py",
        f"{SNAP}/collaboration-pathways/pathways/Collaboration.Refactor.RenameTerm.v1.yaml",
    ]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
