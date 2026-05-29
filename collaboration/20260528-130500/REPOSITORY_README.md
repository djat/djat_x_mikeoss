# the open Pathways project × MikeOSS — Open Collaboration Bundle

**Prepared by:** the open Pathways project (Originator)
**Prepared for:** the open MikeOSS project and team
**Channel:** `djat-mikeoss-20260528`
**Date:** 2026-05-28
**Purpose:** An open invitation to co-create the assay to legal-AI benchmark theater, and the first canonical Pathways encoding of the collaboration-bundle technique.

This file is a copy of the repository README oriented for readers who land inside the convergence folder. **Authoritative repo-level docs:** [`../../README.md`](../../README.md).

---

## Start here

- **Agent:** run [`../../START_COLLABORATION_HANDOFF.prompt.md`](../../START_COLLABORATION_HANDOFF.prompt.md) from repository root.
- **Human:** start at [`companion-bundle-index.md`](companion-bundle-index.md) in this directory.

---

## Repository layout

| Path | Role | Authoritative? |
|---|---|---|
| **This directory** (`collaboration/20260528-130500/`) | Signed convergence snapshot | **Yes** |
| `tools/`, `keys/` at repo root | Verify/sign harness | Required for integrity check |

Set `BUNDLE_ROOT` to this directory. All links in companion docs resolve here.

---

## Handoff

**Status:** SIGNED — ready for open collaboration to the MikeOSS project and team.

### Verify (from repository root)

```bash
python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
```

Expected: `verify: OK`. Authoritative `bundle_root_hash`: [`attestations/CONTENT_MANIFEST.yaml`](attestations/CONTENT_MANIFEST.yaml).

### Signed artifacts

| Artifact | Role |
|---|---|
| `attestations/CONTENT_MANIFEST.yaml` | SHA-256 hash manifest |
| `attestations/BUNDLE_SIGNATURE.json` | Ed25519 signature over `bundle_root_hash` |
| `../../keys/bundle-signing.public.pem` | Public verification key |

---

## Read order (paths relative to this directory)

1. [`companion-bundle-index.md`](companion-bundle-index.md) — start here
2. [`collaboration-spine.md`](collaboration-spine.md) — invitation, exercise, asks
3. [`collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md`](collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md) — the technique, encoded
4. [`assay-pathways/APPLICATION_PLAYBOOK.md`](assay-pathways/APPLICATION_PLAYBOOK.md) — the legal assay pathways
5. [`collaboration-pathways/test/HYPOTHESES.md`](collaboration-pathways/test/HYPOTHESES.md) — the asks, pre-registered

---

## Lineage

| Stage | Artifact | Role |
|---|---|---|
| 1st | collaboration-bundle | Inbound premise pattern (person-a → Originator) |
| 2nd | collaboration-bundle-reciprocal | Reciprocal handoff |
| 3rd | prior-instance-3 | Attestation validation instance |
| 4th | prior-instance-4 | Deal Flow application seeding |
| **5th** | **djat_x_mikeoss (this bundle)** | **Open invitation + first canonical technique encoding** |

Collaboration-bundle technique co-originators: **person-a + Originator (DJ Thomson)**.
