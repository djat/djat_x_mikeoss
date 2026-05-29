#!/usr/bin/env python3
"""06_finalize.py - completeness gate + refactor lineage note (Phase 5, pre-seal).

Completeness gate: every asset generated during this refactor (scripts, new pathway
templates, terms, identities, viewer, de-id map) MUST appear in ASSET_PROVENANCE.yaml with a
producing pathway + run. Reports coverage to pathway-runs/COMPLETENESS.md and exits nonzero if
any expected asset is unaccounted for (so the seal is gated on completeness). Also writes a
refactor lineage sidecar. Producing pathway: Collaboration.Refactor.Finalize@v1.
"""
import json
import os
import re
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
AP = SNAP / "pathway-runs" / "ASSET_PROVENANCE.yaml"
RUN_ID = os.environ.get("PATHWAY_RUN_ID", "")

NEW_TEMPLATES = {
    "Collaboration.Attestation.RecordPathwayRun.v1.yaml",
    "Collaboration.Refactor.RenameTerm.v1.yaml",
    "Collaboration.Naming.RegisterTerm.v1.yaml",
    "Collaboration.Privacy.DeIdentify.v1.yaml",
    "Collaboration.Identity.IssuePersonhoodCredential.v1.yaml",
    "Collaboration.Identity.SealNameLockbox.v1.yaml",
    "Collaboration.Identity.AssertRelationship.v1.yaml",
    "Collaboration.UX.RenderRevealViewer.v1.yaml",
    "Collaboration.Identity.RevealLockbox.v1.yaml",
    "Collaboration.Canon.UpdateSpec.v1.yaml",
    "Collaboration.Refactor.HardenGateProfile.v1.yaml",
    "Collaboration.Identity.SovereignAttributionProxy.v1.yaml",
}


def indexed_assets() -> set[str]:
    s = set()
    for line in AP.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*- asset:\s*(.+)$", line)
        if m:
            s.add(m.group(1).strip())
    return s


def expected_assets() -> list[Path]:
    e = []
    e += sorted((SNAP / "collaboration-pathways" / "scripts").glob("*.py"))
    e += sorted((SNAP / "collaboration-pathways" / "terms").glob("*.yaml"))
    e += [p for p in (SNAP / "identities").rglob("*") if p.is_file()]
    e += [SNAP / "collaboration-pathways" / "patterns" / "Pattern.Naming.ProvenancedTermBinding.yaml"]
    e += [SNAP / "canon" / "PATHWAYS_REFERENCE_v1.1.0.md",
          SNAP / "canon" / "PATHWAYS_ARCHITECTURE_v1.1.0.md"]
    for name in NEW_TEMPLATES:
        e.append(SNAP / "collaboration-pathways" / "pathways" / name)
    return [p for p in e if p.exists()]


def main() -> int:
    idx = indexed_assets()
    # This run's OWN assets are indexed only after the run completes; exclude from the gate.
    self_assets = {
        str(SNAP / "collaboration-pathways" / "scripts" / "06_finalize.py"),
        str(SNAP / "collaboration-pathways" / "pathways" / "Collaboration.Refactor.Finalize.v1.yaml"),
        str(SNAP / "pathway-runs" / "COMPLETENESS.md"),
        str(SNAP / "collaboration-pathways" / "sidecars" / "privacy-refactor-lineage.md"),
    }
    expected = [p for p in expected_assets() if str(p) not in self_assets]
    missing = [str(p) for p in expected if str(p) not in idx]
    covered = [str(p) for p in expected if str(p) in idx]

    report = ["# Completeness gate - refactor asset provenance", "",
              f"Run: {RUN_ID}", f"Indexed assets in ASSET_PROVENANCE.yaml: {len(idx)}",
              f"Expected refactor assets present: {len(expected)}",
              f"Covered: {len(covered)}", f"Missing: {len(missing)}", ""]
    if missing:
        report.append("## MISSING (no producing pathway + run):")
        report += [f"- {m}" for m in missing]
    else:
        report.append("All refactor assets have a producing Pathway + PathwayRun. Seal may proceed.")
    (SNAP / "pathway-runs" / "COMPLETENESS.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    lineage = """# Privacy refactor - provenanced event

This collaboration bundle was refactored as a single provenanced event, every step recorded
as a PathwayRun (see pathway-runs/) and indexed in pathway-runs/ASSET_PROVENANCE.yaml:

1. Phase 0 - provenance harness installed + bootstrap rename (Collaboration.Attestation.RecordPathwayRun@v1)
2. Phase 1 - full rename "transmission bundle" -> "collaboration bundle" (Collaboration.Refactor.RenameTerm@v1)
   + name-as-artifact: Term.CollaborationBundle@v1 supersedes Term.TransmissionBundle@v1
   (prior term retained + freely licensable) (Collaboration.Naming.RegisterTerm@v1)
3. Phase 2 - de-identification of external persons/entities to placeholders
   (Collaboration.Privacy.DeIdentify@v1); real names sealed, never in the snapshot
4. Phase 3 - self-asserted Personhood/Entity credentials + 1-of-2 lockboxes
   (Collaboration.Identity.IssuePersonhoodCredential/SealNameLockbox/AssertRelationship@v1)
5. Phase 4 - privacy-proxy reveal viewer (Collaboration.UX.RenderRevealViewer@v1 +
   Collaboration.Identity.RevealLockbox@v1)
6. Phase 5 - completeness gate + reseal

Attribution preserved as fact; identifiable names live only behind the 1-of-2 lockboxes, which
the Originator can open and which upgrade to genuine subject-key 1-of-2 when each subject
registers a DID key. ZK progressive reveal + FHE are the roadmap.
"""
    note = SNAP / "collaboration-pathways" / "sidecars" / "privacy-refactor-lineage.md"
    note.write_text(lineage, encoding="utf-8")

    produced = [str(SNAP / "pathway-runs" / "COMPLETENESS.md"), str(note),
                str(SNAP / "collaboration-pathways" / "scripts" / "06_finalize.py"),
                str(SNAP / "collaboration-pathways" / "pathways" / "Collaboration.Refactor.Finalize.v1.yaml")]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")

    print(f"completeness: {len(covered)}/{len(expected)} covered, {len(missing)} missing")
    if missing:
        for m in missing[:20]:
            print("  MISSING:", m)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
