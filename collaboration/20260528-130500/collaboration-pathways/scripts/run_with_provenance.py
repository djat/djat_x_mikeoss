#!/usr/bin/env python3
"""run_with_provenance.py - the provenance harness for the Collaboration Bundle refactor.

Every script written and run during this refactor is executed THROUGH this wrapper so
that the technique (the script source), its execution (argv, stdout/stderr, exit), and
its outputs (produced assets) are all recorded as a PathwayRun and indexed in
ASSET_PROVENANCE.yaml. This realizes the universal mandate: every asset, technique, and
piece of code is encoded AS a Pathway and recorded AS a PathwayRun.

Canonical pathway: Collaboration.Attestation.RecordPathwayRun@v1
Stdlib only. No network.

Usage:
  run_with_provenance.py --snapshot <dir> --pathway <id> [--label <txt>]
                         [--produces <relpath> ...] -- <command...>

A wrapped script MAY also declare produced assets by writing a JSON list of repo-relative
paths to the file named in env var ASSET_MANIFEST (set by this harness); the harness folds
those into ASSET_PROVENANCE.yaml.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def primary_script(cmd: list[str]) -> str | None:
    for tok in cmd:
        if tok.endswith((".py", ".sh", ".mjs", ".js")):
            return tok
    return None


def append_index(run_store: Path, entry: dict) -> None:
    idx = run_store / "index.yaml"
    line = (
        f"  - run_id: {entry['run_id']}\n"
        f"    pathway: {entry['pathway']}\n"
        f"    label: \"{entry['label']}\"\n"
        f"    started: {entry['started']}\n"
        f"    ended: {entry['ended']}\n"
        f"    exit_code: {entry['exit_code']}\n"
        f"    script: {entry['script_path']}\n"
        f"    script_sha256: {entry['script_sha256']}\n"
        f"    record: pathway-runs/{entry['run_id']}.json\n"
        f"    produced: {json.dumps(entry['produced'])}\n"
    )
    if not idx.exists():
        idx.write_text("# PathwayRun index - append-only\nruns:\n", encoding="utf-8")
    with idx.open("a", encoding="utf-8") as f:
        f.write(line)


def update_asset_provenance(run_store: Path, snapshot: Path, repo_root: Path,
                            pathway: str, run_id: str, produced: list[str]) -> list[dict]:
    ap = run_store / "ASSET_PROVENANCE.yaml"
    if not ap.exists():
        ap.write_text(
            "# ASSET_PROVENANCE - asset -> producing pathway -> run -> sha256\n"
            "# Universal mandate: every generated asset/technique/code is recorded here.\n"
            "assets:\n",
            encoding="utf-8",
        )
    rows = []
    with ap.open("a", encoding="utf-8") as f:
        for rel in produced:
            ap_path = (repo_root / rel)
            digest = sha256_file(ap_path)
            f.write(
                f"  - asset: {rel}\n"
                f"    produced_by_pathway: {pathway}\n"
                f"    pathway_run_id: {run_id}\n"
                f"    sha256: {digest}\n"
            )
            rows.append({"asset": rel, "sha256": digest})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--pathway", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--produces", nargs="*", default=[])
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    cmd = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("error: no command after --", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root).resolve()
    snapshot = Path(args.snapshot).resolve()
    run_store = snapshot / "pathway-runs"
    run_store.mkdir(parents=True, exist_ok=True)

    run_id = "pr_" + uuid.uuid4().hex[:12]
    script_path = primary_script(cmd)
    script_src = ""
    script_sha = ""
    if script_path and Path(script_path).is_file():
        script_src = Path(script_path).read_text(encoding="utf-8", errors="replace")
        script_sha = hashlib.sha256(script_src.encode("utf-8")).hexdigest()

    # let the wrapped script declare extra produced assets
    asset_manifest = run_store / f".assets_{run_id}.json"
    env = dict(os.environ)
    env["ASSET_MANIFEST"] = str(asset_manifest)
    env["PATHWAY_RUN_ID"] = run_id
    env["PRODUCED_BY_PATHWAY"] = args.pathway

    started = now_iso()
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=repo_root, env=env, capture_output=True, text=True)
    elapsed_ms = int((time.time() - t0) * 1000)
    ended = now_iso()

    produced = list(args.produces)
    if asset_manifest.exists():
        try:
            produced += [p for p in json.loads(asset_manifest.read_text()) if p not in produced]
        finally:
            asset_manifest.unlink(missing_ok=True)

    asset_rows = update_asset_provenance(run_store, snapshot, repo_root,
                                         args.pathway, run_id, produced)

    record = {
        "schema": "pathway-run/1.0",
        "run_id": run_id,
        "pathway": args.pathway,
        "label": args.label,
        "status": "COMPLETED" if proc.returncode == 0 else "FAILED",
        "started": started,
        "ended": ended,
        "elapsed_ms": elapsed_ms,
        "command": cmd,
        "exit_code": proc.returncode,
        "script_path": script_path,
        "script_sha256": script_sha,
        "script_source": script_src,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "produced_assets": asset_rows,
        # domain access -> pre-registered identity hook (filled by scripts that touch domains)
        "accessed_domains": [],
        "authenticated_by_identity": None,
        "harness": "collaboration-pathways/scripts/run_with_provenance.py",
        "recorded_at": now_iso(),
    }
    (run_store / f"{run_id}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    append_index(run_store, {
        "run_id": run_id, "pathway": args.pathway, "label": args.label,
        "started": started, "ended": ended, "exit_code": proc.returncode,
        "script_path": script_path or "", "script_sha256": script_sha,
        "produced": produced,
    })

    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    print(f"[provenance] {run_id} pathway={args.pathway} exit={proc.returncode} "
          f"produced={len(produced)} -> pathway-runs/{run_id}.json", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
