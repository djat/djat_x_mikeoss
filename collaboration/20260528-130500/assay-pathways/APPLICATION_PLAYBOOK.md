# Assay Pathways — Application Playbook

> **Assay** - a precise test of what something is genuinely made of; an *assayer* certifies the true composition of a metal. Here, the *assay pathways* test what a legal-AI claim is really made of - grounded citations, reproducible scores, attested runs: the honest measurement the satire only performs.


**A starting vocabulary for trustworthy legal AI. Owned by neither project; built on the public legal-data commons.**

**Document type:** Application playbook (Assay domain)
**Conformance target:** Level M (stubs; no executable code)
**Read with:** [`../collaboration-spine.md`](../collaboration-spine.md) §2–§3 (the read-as-truth exercise and the assay thesis)

---

## Why these four

The *Elite MegaLaw Benchmark* satire works because everyone recognizes the failure mode: a vendor's self-administered panel reporting impossible numbers in an unreadable methodology. The assay is not a better story; it is whether a claim can be **checked**. These four pathways are the smallest honest vocabulary for that.

| Pathway | Answers the satire | The honest counterpart |
|---|---|---|
| [`Assay.Citation.VerifyFirst@v1`](pathways/Assay.Citation.VerifyFirst.v1.yaml) | "Legal Research 271.5%" | Deterministic grounding against the public commons before any model speaks |
| [`Assay.Benchmark.Reproducible@v1`](pathways/Assay.Benchmark.Reproducible.v1.yaml) | "chart smoothing", scores above 100% | Attested, re-runnable scoring bounded by ground truth |
| [`Assay.Convergence.AnchoredAuthority@v1`](pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) | "recursive agentic orchestration" | A bounded loop that pins canonical authority and forbids latent recall |
| [`Assay.Provenance.RunManifest@v1`](pathways/Assay.Provenance.RunManifest.v1.yaml) | "a panel consisting entirely of MikeOSS" | Separation of who-ran / who-attested / who-authored |

---

## How they compose

`Assay.Convergence.AnchoredAuthority` is the meta-technique: it invokes `VerifyFirst` for the first pass, then re-enters with the canonical-consensus oracle pinned as authority, attesting each iteration via `RunManifest`, until typed citation error falls below a threshold. `Benchmark.Reproducible` wraps any of them in an attested, re-runnable harness so a number can be re-derived by anyone — never inflated.

---

## What these are not

- Not a product, not a benchmark of their own, not a claim that the Pathways project has fully shipped them. Several are early-stage. They are **probes and a shared vocabulary**, offered in the open.
- Not owned by either project. The public legal-data commons (Free Law Project / CourtListener, Cornell LII, GovInfo) is the shared ground; credit it loudly.

---

## Human-judgment boundary

None of these pathways issue legal conclusions. They surface verdicts, confidence, and explicit "insufficient authority" states, and they leave the determination to a licensed human. That boundary is itself a principle in the assay charter (ask H-MO9).
