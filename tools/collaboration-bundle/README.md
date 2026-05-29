# Collaboration bundle signing

Generic, self-contained Ed25519 + SHA-256 binding for Pathways collaboration bundles. No external attestation SDK and no network. Timestamping is the internal `issued_at` only (no qTSA).

Note: a richer entity-2 attestation (per-file aqua trees + signed compositional anchor) and a qualified timestamp (qTSA) are deliberately not wired here — entity-2 3.2 does not provide qTSA, and this bundle takes no dependency on the 4.0 SDK. Internal `issued_at` timestamping is used for now.

## Sign

```bash
python3 tools/collaboration-bundle/sign_bundle.py sign collaboration/20260528-130500 --repo-root .
```

Produces:

- `collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml`
- `collaboration/20260528-130500/attestations/BUNDLE_SIGNATURE.json`
- `keys/bundle-signing.key` (gitignored)
- `keys/bundle-signing.public.pem` (committed)

After signing, do **not** embed `bundle_root_hash` in any file inside the convergence repo (e.g. `REPOSITORY_README.md`) — that creates hash drift. Record the hash only in repo-root `README.md` (outside the signed bundle).

## Verify

```bash
python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
```
