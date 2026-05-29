# Collaboration Spine - An Open Invitation to MikeOSS

**Bundle:** the open Pathways project × the open MikeOSS project and team
**Channel:** `djat-mikeoss-20260528`
**Status:** ASSEMBLED - open invitation; no reply required
**Co-originated collaboration technique:** person-a + Originator (DJ Thomson)

---

## 0. The framing

I read the *Elite MegaLaw Benchmark* as beautiful satire - a near-perfect parody of legal-AI benchmark theater: a panel "consisting entirely of MikeOSS," pass rates above 500%, "advanced decimal point optimisation," "enterprise-grade chart smoothing." It made me laugh, and then it made me think.

So I ran an exercise: **read it as if it were true.** Not the numbers - those are the joke - but the *shape* of what it describes. Where the satire points, there is almost always a real, buildable thing on the other side of the mirror. This collaboration is the map of that delta, and an invitation: that two open projects - yours and the Pathways project - co-create the genuine **assay** the satire only performs - a rigorous test of what a legal-AI claim is really made of.

This is, first, recognition. Second, an exercise. Third, a short menu of small experiments that are worth doing whether or not you ever reply.

---

## 1. Recognition

MikeOSS is a clean, generous piece of work: a self-hostable, multi-tenant legal document assistant; bring-your-own-key across multiple model providers; a document-centric UX; an AGPL posture that says, plainly, *this should be open*. And a project willing to publish a benchmark parody about itself is a project with the rarest quality in this field - the ability to not take its own marketing too seriously. That is exactly the temperament co-creation needs.

We are not competitors on the same axis. You have built an excellent way for a model to *answer* legal questions about a document. The Pathways project has been building a way for a legal *process* to be grounded, reconciled, attested, and legible. Those are complementary halves. That is why this is an invitation and not a pitch.

---

## 2. Reading the satire as truth - the delta

For each satirical bullet, the honest, buildable counterpart it points at:

| The satire says | Read as truth, it points at |
|---|---|
| "Recursive agentic orchestration" | **Bounded convergence loops** - re-run a verification until typed error falls below a threshold, anchored to canonical authority, with each iteration attested. |
| "Multi-model legal cognition pathways" | **Multi-model reconciliation** - run the same question across models as separate, individually-attested runs, then reconcile honestly. |
| "Enterprise-grade chart smoothing" / "advanced decimal point optimisation" / "strategic category weighting" | **Reproducible, attested scoring that cannot exceed reality** - hashed prompts/outputs and deterministic grounding mean a number can be re-derived, never inflated. |
| Pass rates above 100% (e.g. 502.8%) | **Scores bounded by ground truth** - a citation either resolves against a canonical public source or it does not. |
| A panel "consisting entirely of MikeOSS" | **Separation of who-ran / who-attested / who-authored** - provenance and signed identity make self-administered evaluation visible for what it is. |
| "Producing summaries no one reads" | **Structured, checkable deliverables** - verdicts with confidence bands and explicit "insufficient authority" states. |
| "Benchmark leaderboards for benchmark leaderboards" | **A co-owned, reproducible benchmark** anyone can fork and re-run - the honest meta. |

The satire is funny precisely because everyone in legal AI recognizes the failure mode. The assay is not a better marketing department; it is **grounding + reconciliation + provenance + honest convergence**.

---

## 3. The assay thesis
> **Assay** - a precise test of what something is genuinely made of; an *assayer* certifies the true composition of a metal. Here, the *assay pathways* test what a legal-AI claim is really made of - grounded citations, reproducible scores, attested runs: the honest measurement the satire only performs.


The gap between *marketing* legal AI and *trustworthy* legal AI is not model quality. It is whether a claim can be **checked**:

1. **Verify-first grounding** - deterministic lookups against the public legal-data commons (Free Law Project / CourtListener, Cornell LII, GovInfo) *before* any model speaks, so hallucinated citations are caught by math, not vibes.
2. **Multi-model reconciliation** - each model run individually attested; consensus is narrative reconciliation over provenance, not a single confident voice.
3. **Provenance / attestation** - hashed prompts and outputs, signed identity, offline-verifiable. The structural opposite of the self-administered panel.
4. **Honest convergence (the recursion read as truth)** - re-run bounded against anchored authority until typed error is low; never re-open latent recall once anchored.

This thesis is owned by **neither project**. It is a commons. The four `assay-pathways/` templates in this bundle are a starting vocabulary for it, not a product.

---

## 4. Co-creation, stated as values (not contracts)

No licensing terms live in this bundle. The proposal is only this: each project keeps its own edges and ethos, and collaboration grows a **transparent, attributed, shared surface** - pathways that can be forked, credited, recombined, and re-run by anyone. The public legal-data commons (Free Law Project, Cornell LII, GovInfo) is the shared ground we both already stand on; let us build on it together and credit it loudly.

---

## 5. The asks (small, modest, self-validating)

Pre-registered as **H-MO1..H-MO10** in [`collaboration-pathways/test/HYPOTHESES.md`](collaboration-pathways/test/HYPOTHESES.md). Each is designed to produce standalone value **whether or not you send a reciprocal collaboration**. Effort: XS = hours, S = a day or two.

1. **Citation honesty probe** (XS) - run a handful of public AI-drafted legal memos through deterministic verification; publish category-typed verified / warning / not_found counts.
2. **Reproducible micro-benchmark kernel** (S) - one category, ~10 attested tasks, a re-run script, and no score that can exceed 100%.
3. **Minimal run-manifest schema** (XS) - a one-page JSON schema for an attested run (hashes, model id, source types, verdicts) any tool - including a Supabase-backed one - could emit.
4. **Fallback-link honesty pattern** (XS) - when a citation cannot be verified, surface a fallback link instead of confident prose; PR-ready for MikeOSS, useful to anyone.
5. **Convergence (recursion) spike** (S) - a bounded re-run that pins canonical authority and disables latent recall until typed citation error falls below threshold; before/after on one document.
6. **Capability crosswalk** (XS) - map MikeOSS's categories (drafting, contract analysis, legal research, extraction, checklists) to the Pathways domain vocabulary.
7. **Open eval corpus seed** (S) - a tiny, openly-licensed corpus: documents + ground-truth citations + expected verdicts, reusable by the whole network.
8. **"Read the satire as truth" annotated companion** (XS) - for each methodology bullet, the buildable honest counterpart, opened for community annotation (seed in [`sidecars/`](sidecars/)).
9. **Assay principles charter** (XS) - a short, co-signable set of principles: reproducibility; deterministic grounding over latent recall; no inflated metrics; attribution; legible methodology; explicit human-judgment boundaries.
10. **Public commons appreciation note** (XS) - affirm Free Law Project / CourtListener, Cornell LII, and GovInfo as the shared grounding substrate, and propose both projects build on it.

These are probes, not promises. Several Pathways capabilities are themselves early-stage; the asks are honest experiments, run in the open.

---

## 6. Reciprocation (optional)

There is **no obligation** to reply. The bundle reaches a valid, `SEALED` fate on the unilateral experiments alone. If you *do* wish to reply, the reciprocal collaboration is simply another bundle in this same lineage - same structure, same offline-verifiable seal, same self-describing technique provenance. See [`collaboration-pathways/pathways/Collaboration.Reciprocation.AssembleReturnBundle.v1.yaml`](collaboration-pathways/pathways/Collaboration.Reciprocation.AssembleReturnBundle.v1.yaml).

---

## 7. A note on this bundle's own form

This is also the first collaboration in which the **collaboration-bundle technique itself** - co-originated by **person-a + Originator (DJ Thomson)** - is canonically encoded as Pathways and carried *inside* the bundle, so you can interrogate not just its format but its formalization. Start at [`collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md`](collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md). That you occasioned this is, to us, a small and genuine gift. Thank you.

---

*Prepared 2026-05-28 by the open Pathways project. Collaboration-bundle technique co-originators: person-a + Originator (DJ Thomson). Fork allowed; attribution required.*
