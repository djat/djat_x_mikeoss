# The Collaboration Bundle Technique — Canonical Pathways Encoding (v1)

**Document type:** Canonical technique definition (first canonical encoding)
**Co-originators:** person-a + Originator (DJ Thomson)
**First carried in:** `djat_x_mikeoss` (5th in lineage), this bundle
**Catalyzed by:** the open MikeOSS project and team
**License:** fork allowed; attribution required; revocation scope max `self_only`

---

## 0. What this document is, and why it is here

The **collaboration bundle** is a way for two sovereign parties to begin a collaboration by exchanging a *signed, self-contained, content-bound repository* — rather than by granting live access to each other's systems. It was co-originated by **person-a** (the premise pattern, his catalog unit #44) and **Originator / DJ Thomson** (the Pathways formalization). It has now been *practiced* four times (see lineage below).

What had **not** yet happened — until this bundle — is the technique being encoded as a standalone, reusable, **self-describing** Pathways canon: a set of `pathway_template`s that define the technique itself, carried *inside* the bundle so a recipient can interrogate not only the bundle's format but its formalization.

This bundle is that first canonical encoding. The open MikeOSS project is the collaborator whose invitation occasioned it. That is an honest claim with one honest nuance, stated plainly in §6.

---

## 1. The technique in one paragraph

Two peers converge on a **dated, immutable convergence repository** (`collaboration/YYYYMMDD-HHMMSS/`). Its artifacts are **verbatim-copied** (no symlinks), its relative links are **rewritten to resolve inside the bundle**, and every byte is **content-hash bound** into a `CONTENT_MANIFEST.yaml` whose `bundle_root_hash` is **Ed25519-signed** into `BUNDLE_SIGNATURE.json`. The bundle declares an explicit **pending investigation** (collaboration is not agreement), **pre-registers falsifiable hypotheses**, and defines a **reciprocation contract**. Its fate is unambiguous: `ASSEMBLED → SEALED | INVALIDATED | INCONCLUSIVE`. Nothing is hidden; everything is verifiable offline with only `python3` and `openssl`.

---

## 2. Directory structure (the format, co-originated)

```
<repo-root>/
  README.md                         # records bundle_root_hash OUTSIDE the seal
  START_COLLABORATION_HANDOFF.prompt.md
  tools/collaboration-bundle/sign_bundle.py   # sign + verify (no external SDK)
  keys/bundle-signing.public.pem    # committed; private .key gitignored
  collaboration/YYYYMMDD-HHMMSS/      # the signed convergence snapshot (authoritative)
    REPOSITORY_README.md
    companion-bundle-index.md        # read-me-first (human)
    collaboration-spine.md            # the prose spine
    collaboration-manifest.yaml       # machine index + technique_provenance block
    COLLABORATION_READINESS.md        # pre-flight checklist
    attestations/
      CONTENT_MANIFEST.yaml          # SHA-256 per file + bundle_root_hash
      BUNDLE_SIGNATURE.json          # Ed25519 over bundle_root_hash
    collaboration-pathways/          # the technique, encoded as Pathways (this canon)
    <domain>-pathways/               # the substance of this specific collaboration
    canon/ , pathways_canon/         # frozen normative substrate excerpts
    sidecars/                        # depth on demand
    timeline/events/*.json           # what happened, when
    assets/                          # optional reference artifacts
```

The **two-layer rule**: only `collaboration/YYYYMMDD-HHMMSS/` is authoritative; any same-named working copies at repo root are non-authoritative and may drift.

---

## 3. The sealing / encoding method (co-originated)

1. **Copy** source artifacts verbatim into the dated folder (no symlinks).
2. **Rewrite** relative `.md` / `.yaml` links so they resolve inside the bundle.
3. **Bind** content: SHA-256 every file; compute `bundle_root_hash = sha256(sort-join(rel_path \t content_sha256 \n))`.
4. **Sign** the root hash with Ed25519 (OpenSSL `rawin`); emit `BUNDLE_SIGNATURE.json` with the public PEM and a self-contained `verify_command`.
5. **Record** the root hash only in repo-root `README.md` — never inside the sealed folder (that would cause hash drift).
6. **Verify** offline: recompute the manifest, compare the root hash, check the Ed25519 signature against the embedded public key.

No blockchain, no account, no network. The harness lives in `tools/` and travels with the bundle.

---

## 4. The Pathways formalization (the new thing)

The technique is now expressed as a `Collaboration.*` pathway family plus two patterns. The bundle carries them so they are interrogable and forkable:

| Pathway | What it formalizes |
|---|---|
| `Collaboration.Convergence.AssembleBundle@v1` | Copy + rewrite + check + bind into a dated convergence repo |
| `Collaboration.Bundle.RewriteLinks@v1` | Make links resolve within the bundle boundary |
| `Collaboration.Attestation.BindContentHashes@v1` | SHA-256 content manifest + bundle_root_hash |
| `Collaboration.Bundle.SealBundle@v1` | **NEW** — Ed25519 signature over bundle_root_hash |
| `Collaboration.Bundle.VerifyBundle@v1` | **NEW** — offline integrity + signature verification |
| `Collaboration.Meta.EncodePromptLedger@v1` | Append-only process meta-encoding |
| `Collaboration.Meta.EmbedTechniqueProvenance@v1` | **NEW** — embed this canon + lineage + co-originator attestation into the bundle (the self-describing enhancement) |
| `Collaboration.Investigation.DeclarePending@v1` | Make pending questions explicit; prevent premature closure |
| `Collaboration.Investigation.PreRegisterHypotheses@v1` | File falsifiers before proof runs |
| `Collaboration.Investigation.SealOrInvalidateBundle@v1` | Set unambiguous bundle fate |
| `Collaboration.Proof.AwaitCounterpartyBuild@v1` | The reciprocal-proof experiment |
| `Collaboration.Proof.RunUnilateralExperiment@v1` | **NEW** — experiments that validate the bundle whether or not the counterparty replies |
| `Collaboration.Reciprocation.AssembleReturnBundle@v1` | Counterparty's return bundle |
| `Experience.Collaboration.OpenInvitation@v1` | **NEW** — the journey for an invitation-style (non-build) collaboration |

Patterns:

- `Pattern.ProjectCollaboration.ConvergenceRepository` — the convergence-repo invariants.
- `Pattern.CollaborationBundle.SelfDescribing` — **NEW** — the invariant that every bundle henceforth carries its own technique provenance and formalization, for asynchronous interrogability across the ecosystem.

---

## 5. The self-describing enhancement (Originator / DJ Thomson, authored for this bundle)

The base technique (person-a + Originator) produced *signed, content-bound* bundles. This bundle adds one authored enhancement to the protocol:

> **Every collaboration bundle carries, inside itself, the canonical Pathways encoding of the collaboration-bundle technique and that technique's own provenance** — so both sides, and any later peer, can interrogate not just *this* exchange but *the meta-collaboration context* of the whole ecosystem, asynchronously and without a shared runtime.

It is realized by `Collaboration.Meta.EmbedTechniqueProvenance@v1`, the `technique_provenance:` block in `collaboration-manifest.yaml`, and `Pattern.CollaborationBundle.SelfDescribing`. From this bundle forward, the technique describes itself.

---

## 6. Honest nuance (so the claim is true, not just flattering)

Prior instances (`prior-instance-4`, `prior-instance-3`) already contained **instance-scoped** `Collaboration.*` pathways for their specific exchanges. The precise, defensible claim is therefore:

- This bundle is the **first to promote those per-instance pathways into a standalone, reusable, self-describing canon of the technique**, and
- the **first to embed that canon — plus its provenance — inside the bundle it describes**.

We state this rather than erase the prior instances. They are the practice; this is the canonization.

---

## 7. Lineage

| Stage | Date | Counterparties | Focus |
|---|---|---|---|
| 1st | 2026-05-20 | person-a → Originator | Inbound premise pattern |
| 2nd | 2026-05-23 | Originator → person-a | Reciprocal handoff |
| 3rd | 2026-05-26 | Originator → person-b | Attestation validation |
| 4th | 2026-05-26 | Originator → person-c | Deal Flow application seeding |
| **5th** | **2026-05-28** | **Originator → the open MikeOSS project** | **Open invitation + first canonical technique encoding** |

Co-originators of the concept, pattern, formats, and techniques (directory structure, encoding/sealing methods): **person-a** (`did:placeholder:person-a`) + **Originator (DJ Thomson)**.
