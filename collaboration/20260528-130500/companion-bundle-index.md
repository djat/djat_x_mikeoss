---
type: bundle-manifest
title: "The open Pathways × MikeOSS Collaboration - Companion Bundle Index"
purpose: Read-me-first for the open MikeOSS project and team
created: 2026-05-28
status: ASSEMBLED
addressed_to: the open MikeOSS project and team
---

# The open Pathways × MikeOSS Collaboration - Companion Bundle Index

MikeOSS team - start here. This bundle is an **open invitation**, not a build handoff and not a pitch. It does three things: recognizes your work and our shared values; runs an exercise reading the *Elite MegaLaw Benchmark* satire as truth to find the buildable delta; and offers a short menu of small experiments worth doing whether or not you ever reply.

It is also the first bundle to carry the **canonical Pathways encoding of the collaboration-bundle technique itself** - co-originated by **person-a + Originator (DJ Thomson)** - so you can interrogate not just the bundle's format but its formalization.

This index is, deliberately, an instance of the idea it carries: an addressable artifact manifest, every file named and role-typed, content-hash bound and Ed25519-sealed.

---

## Agent entry (LLM / agentic reader)

Start at **repository root** (not inside this folder):

1. Open [`../../START_COLLABORATION_HANDOFF.prompt.md`](../../START_COLLABORATION_HANDOFF.prompt.md)
2. Copy everything below `--- BEGIN PROMPT ---` into your session as the **first message**
3. It verifies integrity, sets `BUNDLE_ROOT` to this directory, and orients you to the invitation + the self-validating experiments

All paths below are relative to **this directory** (`collaboration/20260528-130500/`).

---

## Read order

1. [`collaboration-spine.md`](collaboration-spine.md) - the invitation, the read-as-truth exercise, the assay thesis, the asks
2. [`collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md`](collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md) - the collaboration-bundle technique, canonically encoded
3. [`collaboration-pathways/APPLICATION_PLAYBOOK.md`](collaboration-pathways/APPLICATION_PLAYBOOK.md) - how a collaboration is encoded as Pathways
4. [`collaboration-pathways/pathways-index.yaml`](collaboration-pathways/pathways-index.yaml) - the full Collaboration.* family (interrogable)
5. [`assay-pathways/APPLICATION_PLAYBOOK.md`](assay-pathways/APPLICATION_PLAYBOOK.md) - the legal assay pathways
6. [`collaboration-pathways/test/HYPOTHESES.md`](collaboration-pathways/test/HYPOTHESES.md) - the asks, pre-registered as self-validating experiments
7. [`canon/PATHWAYS_REFERENCE_v1.1.0.md`](canon/PATHWAYS_REFERENCE_v1.1.0.md) - normative Pathways substrate excerpt
8. [`collaboration-manifest.yaml`](collaboration-manifest.yaml) - machine index + `technique_provenance` block
9. [`attestations/CONTENT_MANIFEST.yaml`](attestations/CONTENT_MANIFEST.yaml) - SHA-256 content binding
10. [`attestations/BUNDLE_SIGNATURE.json`](attestations/BUNDLE_SIGNATURE.json) - Ed25519 signature

---

## What this bundle is (and is not)

- **Is:** an open invitation, an exercise, a vocabulary (four `assay-pathways/` stubs), and a self-describing technique canon.
- **Is not:** a product pitch, a benchmark of its own, a licensing proposal, or a demand. No executable application code is bundled.

---

## What you might do (no obligation)

Run any subset of the ten asks in [`collaboration-pathways/test/HYPOTHESES.md`](collaboration-pathways/test/HYPOTHESES.md). Each produces standalone value. The bundle can reach `SEALED` on the unilateral experiments alone; a reciprocal collaboration from MikeOSS is welcome but not required.

---

## Integrity verification

From **repository root**:

```bash
python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
```

Expected: `verify: OK` - compare `bundle_root_hash` to [`attestations/CONTENT_MANIFEST.yaml`](attestations/CONTENT_MANIFEST.yaml). Nothing but `python3` and `openssl` required; no account, no network.

---

*Collaboration-bundle technique co-originators: person-a + Originator (DJ Thomson). This instance: an open invitation to the MikeOSS project and team, and the first canonical encoding of the technique.*
