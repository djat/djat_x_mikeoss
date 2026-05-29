#!/usr/bin/env python3
"""08_strip_token.py - scrub a local-org token from the bundle (Phase 6 cleanup).

Removes one originator-local organization token (a local filesystem/repo name that appeared
in the verbatim spec's example URL, in the canon-import script's source path, and in that
script's run record) and replaces it with the neutral placeholder "your-org". Then recomputes
the spec/architecture sha256 signatures and updates every artifact that references them.

The token is assembled from parts so this script's own source (captured in its PathwayRun)
does not contain the literal - otherwise scrubbing would re-introduce it via provenance.
Producing pathway: Collaboration.Canon.UpdateSpec@v1.
"""
import hashlib
import json
import os
import re
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
TOKEN = "david" + "Xverses"   # avoid the literal in this source
REPL = "your-org"
RUN_ID = os.environ.get("PATHWAY_RUN_ID", "")
HEX64 = re.compile(r"[0-9a-f]{64}")
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html", ".py"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    spec = SNAP / "canon" / "PATHWAYS_REFERENCE_v1.1.0.md"
    arch = SNAP / "canon" / "PATHWAYS_ARCHITECTURE_v1.1.0.md"
    old_spec, old_arch = sha256(spec), sha256(arch)

    # 1) scrub the token everywhere in the snapshot (text files)
    scrubbed = []
    for p in SNAP.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        if TOKEN in t:
            p.write_text(t.replace(TOKEN, REPL), encoding="utf-8")
            scrubbed.append(str(p))

    # 2) recompute signatures (spec changed if token was in it)
    new_spec, new_arch = sha256(spec), sha256(arch)

    # 3) update every reference to the old signatures -> new (CANON_MANIFEST, manifest, PACKAGE)
    ref_files = [SNAP / "canon" / "CANON_MANIFEST.yaml",
                 SNAP / "collaboration-manifest.yaml",
                 SNAP / "collaboration-pathways" / "PACKAGE.yaml"]
    for rf in ref_files:
        if not rf.exists():
            continue
        t = rf.read_text(encoding="utf-8")
        t = t.replace(old_spec, new_spec).replace(old_arch, new_arch)
        rf.write_text(t, encoding="utf-8")

    produced = [str(spec), str(arch)] + [str(x) for x in ref_files if x.exists()] + scrubbed
    produced.append(f"{SNAP}/collaboration-pathways/scripts/08_strip_token.py")
    produced = sorted(set(produced))
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")

    print(f"strip: scrubbed token in {len(scrubbed)} file(s)")
    print(f"  spec sha256 {old_spec[:12]}... -> {new_spec}")
    print(f"  arch sha256 {old_arch[:12]}... -> {new_arch} (unchanged if equal)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
