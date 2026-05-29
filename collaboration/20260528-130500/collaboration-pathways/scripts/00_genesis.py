#!/usr/bin/env python3
"""00_genesis.py - genesis run of the provenance harness.

Records the Phase 0 bootstrap: the snapshot directory rename (transmission/ ->
collaboration/) and the installation of the provenance harness itself. This is the first
PathwayRun; it self-attests the harness (the recorder records itself) and declares the
Phase 0 assets so they enter ASSET_PROVENANCE.yaml.
"""
import json
import os
from pathlib import Path

SNAP = "collaboration/20260528-130500"

BOOTSTRAP = {
    "event": "phase0_bootstrap",
    "directory_rename": {"from": "transmission/20260528-130500", "to": f"{SNAP}"},
    "harness_installed": f"{SNAP}/collaboration-pathways/scripts/run_with_provenance.py",
    "note": (
        "The top-level snapshot directory was renamed transmission/ -> collaboration/ as "
        "the bootstrap move; this genesis PathwayRun attests it. All subsequent scripts run "
        "through the harness under the stable collaboration/ path."
    ),
}

# Phase 0 assets produced/installed during bootstrap
ASSETS = [
    f"{SNAP}/collaboration-pathways/scripts/run_with_provenance.py",
    f"{SNAP}/collaboration-pathways/scripts/00_genesis.py",
    f"{SNAP}/collaboration-pathways/pathways/Collaboration.Attestation.RecordPathwayRun.v1.yaml",
]

def main() -> int:
    Path(f"{SNAP}/pathway-runs/genesis-bootstrap.json").write_text(
        json.dumps(BOOTSTRAP, indent=2) + "\n", encoding="utf-8"
    )
    ASSETS.append(f"{SNAP}/pathway-runs/genesis-bootstrap.json")
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(ASSETS), encoding="utf-8")
    print("genesis: bootstrap recorded; harness self-attested; phase-0 assets declared")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
