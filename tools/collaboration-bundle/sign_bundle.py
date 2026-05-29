#!/usr/bin/env python3
"""Hash-bind and Ed25519-sign a Pathways collaboration convergence repository."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED_PREFIXES = (".git", ".obsidian", ".DS_Store")
EXCLUDED_ATTESTATION_FILES = {
    "CONTENT_MANIFEST.yaml",
    "BUNDLE_SIGNATURE.yaml",
    "BUNDLE_SIGNATURE.json",
}


def is_excluded(bundle_root: Path, path: Path) -> bool:
    rel = path.relative_to(bundle_root)
    parts = rel.parts
    if not parts:
        return True
    if parts[0] in EXCLUDED_PREFIXES:
        return True
    if parts[0] == "attestations":
        if len(parts) == 1:
            return True
        if parts[1] == "files":
            return True
        if parts[1] in EXCLUDED_ATTESTATION_FILES:
            return True
    return False


def list_bundle_files(bundle_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(bundle_root.rglob("*")):
        if not path.is_file():
            continue
        if is_excluded(bundle_root, path):
            continue
        files.append(path)
    return files


def sha256_file(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    return digest, len(data)


def bundle_root_hash(entries: list[dict]) -> str:
    lines = [f"{e['rel_path']}\t{e['content_sha256']}" for e in entries]
    lines.sort()
    payload = "\n".join(lines) + ("\n" if lines else "")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ensure_key(key_path: Path) -> None:
    key_path.parent.mkdir(parents=True, exist_ok=True)
    if key_path.exists():
        return
    subprocess.run(
        ["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(key_path)],
        check=True,
    )


def export_public_key(key_path: Path, public_path: Path) -> None:
    subprocess.run(
        ["openssl", "pkey", "-in", str(key_path), "-pubout", "-out", str(public_path)],
        check=True,
    )


def sign_hash(key_path: Path, digest_hex: str) -> str:
    proc = subprocess.run(
        [
            "openssl",
            "pkeyutl",
            "-sign",
            "-inkey",
            str(key_path),
            "-rawin",
            "-in",
            "/dev/stdin",
        ],
        input=digest_hex.encode("utf-8"),
        check=True,
        capture_output=True,
    )
    return base64.b64encode(proc.stdout).decode("ascii")


def write_manifest(
    manifest_path: Path,
    *,
    bundle_id: str,
    issued_at: str,
    issuer_label: str,
    root_hash: str,
    entries: list[dict],
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Collaboration bundle content manifest — SHA-256 bound",
        'manifest_version: "1.0"',
        "manifest_kind: content_manifest",
        f"bundle_id: {bundle_id}",
        f"issued_at: {issued_at}",
        f'issuer_label: "{issuer_label}"',
        "",
        "state:",
        "  hash_status: real",
        "  signature_status: pending",
        "",
        "bundle_root_hash:",
        "  algorithm: sha256",
        '  method: "sha256(sort-join(rel_path \\t content_sha256 \\n))"',
        f"  hash: {root_hash}",
        "",
        f"file_count: {len(entries)}",
        "",
        "files:",
    ]
    for entry in entries:
        lines.extend(
            [
                f"  - rel_path: {entry['rel_path']}",
                f"    content_sha256: {entry['content_sha256']}",
                f"    file_size: {entry['file_size']}",
            ]
        )
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_signature(
    signature_path: Path,
    *,
    bundle_id: str,
    issued_at: str,
    issuer_label: str,
    root_hash: str,
    signature_b64: str,
    public_key_path: Path,
    verify_target: str,
) -> None:
    public_pem = public_key_path.read_text(encoding="utf-8")
    payload = {
        "manifest_version": "1.0",
        "manifest_kind": "bundle_signature",
        "bundle_id": bundle_id,
        "issued_at": issued_at,
        "issuer_label": issuer_label,
        "signing_method": "Ed25519 OpenSSL rawin over bundle_root_hash hex",
        "bundle_root_hash": root_hash,
        "signature_base64": signature_b64,
        "public_key_pem": public_pem,
        "verify_command": (
            f"python3 tools/collaboration-bundle/sign_bundle.py verify {verify_target}"
        ),
    }
    signature_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def cmd_sign(args: argparse.Namespace) -> int:
    bundle_root = Path(args.bundle_dir).resolve()
    repo_root = Path(args.repo_root).resolve()
    key_path = repo_root / "keys" / "bundle-signing.key"
    public_path = repo_root / "keys" / "bundle-signing.public.pem"

    ensure_key(key_path)
    export_public_key(key_path, public_path)

    entries: list[dict] = []
    for full in list_bundle_files(bundle_root):
        rel = full.relative_to(bundle_root).as_posix()
        digest, size = sha256_file(full)
        entries.append(
            {"rel_path": rel, "content_sha256": digest, "file_size": size}
        )

    root_hash = bundle_root_hash(entries)
    issued_at = args.issued_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest_path = bundle_root / "attestations" / "CONTENT_MANIFEST.yaml"
    write_manifest(
        manifest_path,
        bundle_id=args.bundle_id,
        issued_at=issued_at,
        issuer_label=args.issuer,
        root_hash=root_hash,
        entries=entries,
    )

    signature_b64 = sign_hash(key_path, root_hash)
    signature_path = bundle_root / "attestations" / "BUNDLE_SIGNATURE.json"
    try:
        verify_target = bundle_root.relative_to(repo_root).as_posix()
    except ValueError:
        verify_target = bundle_root.name
    write_signature(
        signature_path,
        bundle_id=args.bundle_id,
        issued_at=issued_at,
        issuer_label=args.issuer,
        root_hash=root_hash,
        signature_b64=signature_b64,
        public_key_path=public_path,
        verify_target=verify_target,
    )

    manifest_text = manifest_path.read_text(encoding="utf-8").replace(
        "signature_status: pending", "signature_status: signed"
    )
    manifest_path.write_text(manifest_text, encoding="utf-8")

    print(f"Signed bundle: {bundle_root}")
    print(f"  files: {len(entries)}")
    print(f"  bundle_root_hash: {root_hash}")
    print(f"  manifest: {manifest_path.relative_to(repo_root)}")
    print(f"  signature: {signature_path.relative_to(repo_root)}")
    print(f"  public key: {public_path.relative_to(repo_root)}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    bundle_root = Path(args.bundle_dir).resolve()
    manifest_path = bundle_root / "attestations" / "CONTENT_MANIFEST.yaml"
    signature_path = bundle_root / "attestations" / "BUNDLE_SIGNATURE.json"

    if not manifest_path.exists() or not signature_path.exists():
        print("verify: FAIL — missing manifest or signature", file=sys.stderr)
        return 1

    sig = json.loads(signature_path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for full in list_bundle_files(bundle_root):
        rel = full.relative_to(bundle_root).as_posix()
        digest, size = sha256_file(full)
        entries.append(
            {"rel_path": rel, "content_sha256": digest, "file_size": size}
        )

    recomputed = bundle_root_hash(entries)
    if recomputed != sig["bundle_root_hash"]:
        print("verify: FAIL — bundle_root_hash mismatch", file=sys.stderr)
        print(f"  expected: {sig['bundle_root_hash']}", file=sys.stderr)
        print(f"  got:      {recomputed}", file=sys.stderr)
        return 1

    public_pem = sig["public_key_pem"].encode("utf-8")
    signature = base64.b64decode(sig["signature_base64"])

    import tempfile

    with tempfile.NamedTemporaryFile("wb", delete=False) as pub:
        pub.write(public_pem)
        pub_path = pub.name
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as inf:
        inf.write(recomputed)
        in_path = inf.name
    with tempfile.NamedTemporaryFile("wb", delete=False) as sigf:
        sigf.write(signature)
        sig_path = sigf.name

    verify = subprocess.run(
        [
            "openssl",
            "pkeyutl",
            "-verify",
            "-pubin",
            "-inkey",
            pub_path,
            "-rawin",
            "-in",
            in_path,
            "-sigfile",
            sig_path,
        ],
        capture_output=True,
        text=True,
    )
    Path(in_path).unlink(missing_ok=True)
    Path(pub_path).unlink(missing_ok=True)
    Path(sig_path).unlink(missing_ok=True)

    if verify.returncode != 0:
        print("verify: FAIL — Ed25519 signature invalid", file=sys.stderr)
        return 1

    print("verify: OK")
    print(f"  bundle_root_hash: {recomputed}")
    print(f"  file_count: {len(entries)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sign or verify collaboration bundles")
    sub = parser.add_subparsers(dest="command", required=True)

    sign = sub.add_parser("sign", help="Hash-bind and sign a convergence repo")
    sign.add_argument("bundle_dir", help="Path to collaboration/YYYYMMDD-HHMMSS")
    sign.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing keys/",
    )
    sign.add_argument(
        "--bundle-id",
        default="djat-mikeoss-20260528",
    )
    sign.add_argument("--issuer", default="Originator (Pathways framework author)")
    sign.add_argument("--issued-at", default=None)
    sign.set_defaults(func=cmd_sign)

    verify = sub.add_parser("verify", help="Verify manifest and signature")
    verify.add_argument("bundle_dir")
    verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
