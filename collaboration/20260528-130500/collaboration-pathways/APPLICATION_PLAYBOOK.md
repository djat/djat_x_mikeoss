# Project Collaboration Pathways - Application Playbook

**A self-contained narrative recipe for encoding peer technical collaboration as Pathways - and, in this bundle, for the first canonical encoding of the collaboration-bundle technique itself.**

**Document type:** Application playbook (Collaboration domain)
**Conformance target:** Level S (collaboration bundle + content-hash binding + Ed25519 seal)
**Reference instance:** the open Pathways project × the open MikeOSS project and team - open invitation
**Technique co-originators:** person-a + Originator (DJ Thomson)

---

## About this playbook

This playbook describes how to **encode a collaboration** - not just its outputs - as a Pathways sub-bundle, and how this bundle carries the **technique's own canon** so it is self-describing:

1. **Convergence** - copy artifacts, rewrite links, assemble dated collaboration folder
2. **Content binding** - SHA-256 hash manifest for integrity verification
3. **Sealing** - Ed25519 signature over the bundle_root_hash
4. **Self-description** - embed the technique canon + provenance (the new enhancement)
5. **Meta** - record prompt ledger + collaboration instance YAML
6. **Investigation** - declare what remains open
7. **Proof** - run falsifiable, mostly-unilateral experiments before claiming anything

Read [`../pathways_canon/PATHWAYS_PROJECT_COLLABORATION_REPORT.md`](../pathways_canon/PATHWAYS_PROJECT_COLLABORATION_REPORT.md) for the domain theory and [`canon/COLLABORATION_BUNDLE_TECHNIQUE.md`](canon/COLLABORATION_BUNDLE_TECHNIQUE.md) for the technique itself.

---

## Part I - The collaboration surface

### Chapter 1 - Counterparties and channel

```yaml
prepared_by: "the open Pathways project (Originator)"
prepared_for: "the open MikeOSS project and team"
channel: "djat-mikeoss-20260528"
governance_descriptor: shared-spec-sovereign-implementations
```

This instance: an **open invitation** (not a build handoff); focus = co-creating the assay to legal-AI benchmark theater.

### Chapter 2 - Convergence repository

Lives at `collaboration/20260528-130500/`. The **initial shared ground** - both parties verify the same `bundle_root_hash`.

Steps: [pathway:Collaboration.Convergence.AssembleBundle@v1]

### Chapter 3 - Content binding and sealing

All bytes are hash-bound via `attestations/CONTENT_MANIFEST.yaml`; the root hash is Ed25519-signed into `attestations/BUNDLE_SIGNATURE.json`.

Steps: [pathway:Collaboration.Attestation.BindContentHashes@v1] then [pathway:Collaboration.Bundle.SealBundle@v1]. Verify with [pathway:Collaboration.Bundle.VerifyBundle@v1].

---

## Part II - Self-description (the new enhancement)

### Chapter 4 - Embed technique provenance

This bundle carries the technique's own canon and provenance so any peer can interrogate the formalization, not just the format.

Steps: [pathway:Collaboration.Meta.EmbedTechniqueProvenance@v1]
Invariant: [pattern:Pattern.CollaborationBundle.SelfDescribing]

### Chapter 5 - Prompt ledger and process snapshot

Every material author prompt is appended to `prompt-ledger.yaml`. `meta/collaboration-instance.yaml` binds hashes, investigation id, and collaboration status.

Steps: [pathway:Collaboration.Meta.EncodePromptLedger@v1]

---

## Part III - Investigation and proof

### Chapter 6 - Pending investigation

A collaboration **MUST NOT** close without either completing or explicitly abandoning its investigation declaration.

| Field | Value |
|---|---|
| `investigation_id` | `open-assay-co-creation-mikeoss` |
| `hypothesis` | Two open projects can co-create a transparent, attested assay to legal-AI benchmark theater; and most of the value can be produced unilaterally |
| `blocking_on` | Nothing required from MikeOSS; reciprocation welcome, not required |
| `success_criteria` | Unilateral experiments confirmed and published openly; door left open |

Steps: [pathway:Collaboration.Investigation.DeclarePending@v1]

### Chapter 7 - Proof experiments (mostly unilateral)

The asks are pre-registered as H-MO1..H-MO10 in [`test/HYPOTHESES.md`](test/HYPOTHESES.md). Most can be confirmed without any reply.

Steps: [pathway:Collaboration.Proof.RunUnilateralExperiment@v1]; optional reciprocal proof via [pathway:Collaboration.Proof.AwaitCounterpartyBuild@v1].

### Chapter 8 - Hypotheses, seal, and fate

Pre-register via [pathway:Collaboration.Investigation.PreRegisterHypotheses@v1]; evaluate via [pathway:Collaboration.Investigation.SealOrInvalidateBundle@v1]:

| Status | Meaning |
|---|---|
| `ASSEMBLED` | Convergence repo complete; experiments pending |
| `SEALED` | Unilateral hypotheses confirmed; investigation resolved |
| `INVALIDATED` | A structural falsifier fired |
| `INCONCLUSIVE` | Structural pass but reciprocal-only hypotheses unanswered |

**This instance:** `ASSEMBLED` at issue; SEALED is reachable on the unilateral experiments alone.

**Co-origin attribution:** collaboration-bundle technique co-originators person-a + Originator (DJ Thomson) - see [`sidecars/collaboration-pattern-lineage-and-attribution.md`](sidecars/collaboration-pattern-lineage-and-attribution.md).

---

## Part IV - Journey composition

End-to-end: [pathway:Experience.Collaboration.OpenInvitation@v1] invokes all Part I–III pathways in order.

---

## Part V - Reciprocation (optional)

If MikeOSS chooses to reply, the reciprocal collaboration is itself a self-describing bundle in this same lineage.

Steps: [pathway:Collaboration.Reciprocation.AssembleReturnBundle@v1]

---

## Appendix A - Pointer legend

- `[pathway:Collaboration.*]` - collaboration domain template
- `[pathway:Experience.Collaboration.*]` - journey wrapper
- `[pathway:Assay.*]` - the legal assay domain pathways in this bundle
- `[pattern:...]` - invariant pattern
- `[artifact:collaboration/...]` - convergence repo path
