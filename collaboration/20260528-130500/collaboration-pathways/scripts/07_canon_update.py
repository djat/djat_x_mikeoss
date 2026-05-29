#!/usr/bin/env python3
"""07_canon_update.py - bring authoritative Pathways spec + architecture v1.1.0 into canon (Phase 6).

Producing pathway: Collaboration.Canon.UpdateSpec@v1. Copies the full v1.1.0 specification and
architecture verbatim, computes their sha256 signatures, removes the v1.0.0 excerpt, and updates
artifacts to reference v1.1.0 + the exact signatures. The verbatim specs may reference the
upstream ecosystem (allowed); the bundle's own de-identified prose is unaffected (the specs
contain none of the de-identified subject names).
"""
import hashlib
import json
import os
import shutil
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
SRC = Path("/Users/djathomson/Projects/your-org/legal-services-crew")
CANON = SNAP / "canon"
RUN_ID = os.environ.get("PATHWAY_RUN_ID", "")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    CANON.mkdir(parents=True, exist_ok=True)
    arch_dst = CANON / "PATHWAYS_ARCHITECTURE_v1.1.0.md"
    spec_dst = CANON / "PATHWAYS_REFERENCE_v1.1.0.md"
    shutil.copyfile(SRC / "PATHWAYS_ARCHITECTURE.md", arch_dst)
    shutil.copyfile(SRC / "PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md", spec_dst)
    arch_sha, spec_sha = sha256(arch_dst), sha256(spec_dst)

    old = CANON / "PATHWAYS_REFERENCE_v1.0.0.md"
    if old.exists():
        old.unlink()

    (CANON / "CANON_MANIFEST.yaml").write_text(f"""# Canon Manifest - frozen normative spec + architecture (v1.1.0)
manifest_version: "1.1"
channel: djat-mikeoss-20260528

specification:
  reference_implementation_spec:
    file: PATHWAYS_REFERENCE_v1.1.0.md
    version: 1.1.0
    title: "Pathways Reference Implementation Specification - Authority Boundaries"
    signature: {{ alg: sha256, value: {spec_sha} }}
  architecture:
    file: PATHWAYS_ARCHITECTURE_v1.1.0.md
    version: 1.1.0
    title: "Pathways Architecture - Spec alignment (coherent with RIS 1.1.0)"
    signature: {{ alg: sha256, value: {arch_sha} }}

note: |
  Full authoritative v1.1.0 specification and architecture, included verbatim and frozen for
  this bundle. These are the normative source of truth; every artifact that cites the spec
  references version 1.1.0 and the sha256 signatures above. The verbatim docs may reference
  the upstream Pathways ecosystem; the bundle's own authored prose is separately de-identified.
""", encoding="utf-8")

    # pathways_canon architecture excerpt -> pointer to the full canonical doc
    (SNAP / "pathways_canon" / "PATHWAYS_ARCHITECTURE.md").write_text(
        f"""# Pathways Architecture - pointer

The authoritative architecture document (v1.1.0) is carried in full at
[`../canon/PATHWAYS_ARCHITECTURE_v1.1.0.md`](../canon/PATHWAYS_ARCHITECTURE_v1.1.0.md).

- version: 1.1.0 (Spec alignment; coherent with RIS 1.1.0 Authority Boundaries)
- sha256: {arch_sha}

This stub exists only so older read-order links resolve; read the full canon doc.
""", encoding="utf-8")

    # token-patch references v1.0.0 -> v1.1.0 across snapshot text artifacts
    patch_targets = [
        SNAP / "companion-bundle-index.md",
        SNAP / "collaboration-spine.md",
        SNAP / "collaboration-pathways" / "PACKAGE.yaml",
        SNAP / "collaboration-pathways" / "APPLICATION_PLAYBOOK.md",
        SNAP / "collaboration-manifest.yaml",
    ]
    patched = []
    for p in patch_targets:
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        nt = t.replace("PATHWAYS_REFERENCE_v1.0.0", "PATHWAYS_REFERENCE_v1.1.0")
        if nt != t:
            p.write_text(nt, encoding="utf-8")
            patched.append(str(p))

    # PACKAGE.yaml: add conforms_to_spec + point normative docs at v1.1.0
    pkg = SNAP / "collaboration-pathways" / "PACKAGE.yaml"
    if pkg.exists():
        with pkg.open("a", encoding="utf-8") as f:
            f.write(f"""
conforms_to_spec:
  version: 1.1.0
  reference_spec: canon/PATHWAYS_REFERENCE_v1.1.0.md
  reference_spec_sha256: {spec_sha}
  architecture: canon/PATHWAYS_ARCHITECTURE_v1.1.0.md
  architecture_sha256: {arch_sha}
""")

    # collaboration-manifest.yaml: append specification_provenance
    man = SNAP / "collaboration-manifest.yaml"
    with man.open("a", encoding="utf-8") as f:
        f.write(f"""
# ---------------------------------------------------------------------------
# SPECIFICATION PROVENANCE - artifacts reference these exact spec signatures
# ---------------------------------------------------------------------------
specification_provenance:
  spec:
    file: canon/PATHWAYS_REFERENCE_v1.1.0.md
    version: 1.1.0
    sha256: {spec_sha}
  architecture:
    file: canon/PATHWAYS_ARCHITECTURE_v1.1.0.md
    version: 1.1.0
    sha256: {arch_sha}
""")

    produced = [str(arch_dst), str(spec_dst), str(CANON / "CANON_MANIFEST.yaml"),
                str(SNAP / "pathways_canon" / "PATHWAYS_ARCHITECTURE.md"),
                str(pkg), str(man),
                f"{SNAP}/collaboration-pathways/scripts/07_canon_update.py",
                f"{SNAP}/collaboration-pathways/pathways/Collaboration.Canon.UpdateSpec.v1.yaml"]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")

    print(f"canon: imported v1.1.0 spec + architecture verbatim")
    print(f"  PATHWAYS_REFERENCE_v1.1.0.md     sha256 {spec_sha}")
    print(f"  PATHWAYS_ARCHITECTURE_v1.1.0.md  sha256 {arch_sha}")
    print(f"  removed v1.0.0 excerpt; patched {len(patched)} reference(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
