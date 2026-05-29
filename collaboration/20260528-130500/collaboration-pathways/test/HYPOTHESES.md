---
type: pre-registered-hypotheses
title: "The asks as falsifiable, mostly-unilateral experiments"
filed: 2026-05-28
status: pre-registered
context:
  reference_instance: djat-mikeoss-20260528
  investigation_id: open-assay-co-creation-mikeoss
---

# Pre-registered hypotheses — open Pathways × MikeOSS invitation

## §1 — Discipline of pre-registration

The ten asks are committed on 2026-05-28, before any experiment runs. Evaluation runs via `Collaboration.Investigation.SealOrInvalidateBundle@v1`. Crucially, **every ask is designed to be confirmable unilaterally** — the bundle can reach `SEALED` with no reply from MikeOSS.

**Bundle fate states:**

| State | Meaning |
|---|---|
| `ASSEMBLED` | Convergence repo complete; experiments pending |
| `SEALED` | Unilateral hypotheses confirmed; investigation resolved |
| `INVALIDATED` | A structural falsifier fired |
| `INCONCLUSIVE` | Structural pass but reciprocal-only hypotheses unanswered |

Effort sizes: XS = hours; S = a day or two.

---

## §2 — Structural hypotheses (must hold for any seal)

### H-MO0a — Link closure (structural)
**Hypothesis:** Every relative link in the convergence repo resolves within the bundle.
**Falsifier:** Any broken relative link. **Fate if falsified:** INVALIDATED.

### H-MO0b — Content integrity + self-description (structural)
**Hypothesis:** `bundle_root_hash` recomputes; the Ed25519 signature verifies; and `collaboration-manifest.yaml` carries a `technique_provenance` block naming co-originators and defining pathways.
**Falsifier:** Hash/signature mismatch, or missing technique provenance. **Fate if falsified:** INVALIDATED.

---

## §3 — The ten asks (unilateral unless noted)

### H-MO1 — Citation honesty probe (XS, unilateral)
**Hypothesis:** Running a handful of public AI-drafted legal memos through deterministic verification yields publishable category-typed counts (verified / warning / not_found).
**Confirm:** `proof-results/unilateral/H-MO1.yaml` with counts + sources. **Fate if absent:** INCONCLUSIVE.

### H-MO2 — Reproducible micro-benchmark kernel (S, unilateral)
**Hypothesis:** One category with ~10 attested tasks plus a re-run script produces a result where no score exceeds 100% and any third party can re-derive it.
**Confirm:** `proof-results/benchmark/rerun.md` + scores. **Fate if absent:** INCONCLUSIVE.

### H-MO3 — Minimal run-manifest schema (XS, unilateral)
**Hypothesis:** A one-page attested-run JSON schema can be emitted from an arbitrary stack (incl. Supabase-backed).
**Confirm:** schema published; one example manifest validates. **Fate if absent:** INCONCLUSIVE.

### H-MO4 — Fallback-link honesty pattern (XS, unilateral; PR-able to MikeOSS)
**Hypothesis:** A small, copy-pasteable pattern surfaces a fallback link instead of confident prose when a citation cannot be verified.
**Confirm:** pattern published; optionally offered to MikeOSS as a PR. **Fate if absent:** INCONCLUSIVE.

### H-MO5 — Convergence (recursion) spike (S, unilateral)
**Hypothesis:** A bounded re-run that pins canonical authority and disables latent recall reduces typed citation error on one document (before/after).
**Confirm:** before/after verdicts + iteration attestations. **Fate if absent:** INCONCLUSIVE.

### H-MO6 — Capability crosswalk (XS, unilateral; richer if reciprocated)
**Hypothesis:** MikeOSS's categories (drafting, contract analysis, legal research, extraction, checklists) map cleanly to the Pathways domain vocabulary.
**Confirm:** crosswalk table published. **Fate if absent:** INCONCLUSIVE.

### H-MO7 — Open eval corpus seed (S, unilateral)
**Hypothesis:** A tiny, openly-licensed corpus (documents + ground-truth citations + expected verdicts) is reusable by the whole network.
**Confirm:** corpus published with a license. **Fate if absent:** INCONCLUSIVE.

### H-MO8 — "Read the satire as truth" annotated companion (XS, unilateral; community-open)
**Hypothesis:** Each methodology bullet has a buildable honest counterpart worth annotating in the open.
**Confirm:** [`../../sidecars/reading-the-satire-as-truth.md`](../../sidecars/reading-the-satire-as-truth.md) published and open for annotation. **Fate if absent:** INCONCLUSIVE.

### H-MO9 — Assay principles charter (XS, unilateral; co-signable)
**Hypothesis:** A short charter (reproducibility; grounding over latent recall; no inflated metrics; attribution; legible methodology; human-judgment boundaries) stands alone as a values artifact.
**Confirm:** charter published; co-signature welcome, not required. **Fate if absent:** INCONCLUSIVE.

### H-MO10 — Public commons appreciation note (XS, unilateral)
**Hypothesis:** Affirming Free Law Project / CourtListener, Cornell LII, and GovInfo as the shared grounding substrate is itself a useful, true artifact.
**Confirm:** [`../../sidecars/public-commons-appreciation.md`](../../sidecars/public-commons-appreciation.md) published. **Fate if absent:** INCONCLUSIVE.

---

## §4 — Positive circumstances that SEAL

1. H-MO0a, H-MO0b **confirmed** (structural).
2. At least one of H-MO1..H-MO10 **confirmed** and published openly.
3. Any unconfirmed asks remain **INCONCLUSIVE** (never INVALIDATED) — they are invitations, not obligations.
4. No reciprocal collaboration is required for SEALED.

A reply from MikeOSS upgrades INCONCLUSIVE asks toward confirmed, but its absence never invalidates the bundle.

---

## §5 — Evaluation record (this instance)

| Hypothesis | Assembly result | Notes |
|---|---|---|
| H-MO0a | pending | Verify at seal (link closure) |
| H-MO0b | pending | Verify at seal (hash + signature + technique_provenance) |
| H-MO1..H-MO10 | open | Unilateral; run any subset, publish in `proof-results/` |

Expected state at issue: **ASSEMBLED**. SEALED reachable on the unilateral experiments.
