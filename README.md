# An Open Benchmarking Tool for MikeOSS — A Collaboration Offering from the Pathways Project

*From one open project to another. The Pathways project **donates** the specifications, recipes, and attestation substrate that turn MikeOSS’s [Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark) satire into something you can actually run, verify, and stand behind. **No strings.** No account, no install, no obligation, no license fee. You can read it in a browser, verify it offline, implement it in your MikeOSS stack, fork it, or ignore it.*

*This page is written for the **MikeOSS project and team**, for **operators already running MikeOSS**, and for **lawyers and legal ops leaders** who want plain language on what is being offered and why — without needing to read code first.*

---

## TL;DR (60 seconds)

- MikeOSS published a brilliant parody of legal-AI benchmark theater — **[MikeOSS Releases Results of the Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark)** — with pass rates above 500%, a panel “consisting entirely of MikeOSS,” and “advanced decimal point optimisation.” We took [that article](https://mikeoss.com/articles/elite-megalaw-benchmark) seriously and built the **honest inverse**: an open, reproducible **assay** toolkit anyone can re-run.
- **This repository is that tool** — not another vendor PDF, but signed [**Pathways**](https://tesseractstakes.com/pathways) specifications: versioned, cryptographically attestable workflow recipes from the open standard for user-owned agentic intellectual property ([overview below](#3-what-the-pathways-project-is) · [v1.1.0 spec](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md)). You can drop them into MikeOSS (Supabase / Next / Express), verify offline, and fork without asking permission.
- It arrives as an **Application Playbook**: narrative plus machine-readable recipes. Four **assay pathways** ([`VerifyFirst`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml), [`Reproducible`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml), [`AnchoredAuthority`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml), [`RunManifest`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml)) cover verify-first grounding, reproducible scoring, honest convergence, and run provenance — built on the [Pathways v1.1.0 spec](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md).
- The same substrate connects to **[Authority Boundaries for AI](https://www.dazzagreenwood.com/p/authority-boundaries-for-ai)** (Greenwood, 2026) via Pathways v1.1.0 — encoding where agent work ends and lawyer judgment begins. See [`SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md`](SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md) for how that connection is engineered.
- It is a **commons**: owned by neither project. Fork allowed, attribution required, no fee.

---

## 1. What this is — and who it is for

This is **not** a sales pitch, a contract, or a request for MikeOSS’s data, code, or money. It is a **gift of mechanisms** from the open **Pathways** project to the open **MikeOSS** project — the small set of trust primitives that make legal-AI performance claims *checkable* rather than merely *asserted*.

**If you operate MikeOSS today**, this bundle is designed to meet you where you already are: self-hosted, bring-your-own-key, document-centric, AGPL. The recipes map to your existing stack without a rewrite. You keep your product, your UX, and your edge; you gain a defensible measurement layer.

**If you are evaluating legal AI from a firm or in-house team**, the industry context below explains why an open benchmarking tool matters — and why MikeOSS’s willingness to satirize its own category made this collaboration possible.

Everything here is **specifications, recipes, prose, and cryptographic attestation** — no executable application code you must trust blindly. You implement it on your own terms, or not at all.

---

## 2. The benchmark gap — and why MikeOSS’s satire was the right starting point

Legal AI has attracted enormous venture investment. Much of that capital has flowed into go-to-market — sales teams calling on firms and legal departments with polished demos and confident performance claims. The pitch is often that a vendor’s application layer delivers legal-task performance far beyond what ChatGPT, Claude, or Gemini can achieve alone. That *can* be true. Buyers nonetheless have very little independent way to know.

The pattern in vendor-published benchmarks is remarkably consistent: the sponsor ranks first in every category; competing legal-AI tools cluster just below; base models sit at the bottom; methodology sections grow longer and less intelligible. Scepticism is warranted — especially when many technically capable lawyers already get excellent results from base ChatGPT, Codex, Claude, and similar tools without a six-month pilot.

Direct comparison is harder still because most legal-AI products are **gatekept**. Unlike conventional software, you typically cannot download and evaluate them on your own terms. You schedule a demo, negotiate a pilot, and wait.

What the market lacks is an **impartial, third-party-assessable benchmark** for the legal-AI *application layer* — transparent methodology that anyone can re-run and challenge. Buyers need **performance transparency**, not more marketing.

MikeOSS named that failure mode with unusual clarity in **[MikeOSS Releases Results of the Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark)** — a satire in which MikeOSS “wins” every category, pass rates exceed 500%, and the evaluation panel consists entirely of MikeOSS staff. The article’s own closing describes the real critique: reports where *the sponsoring company ranks first in every category, competitors cluster narrowly below, and the methodology becomes progressively less understandable.*

**This repository is our riff on [that article](https://mikeoss.com/articles/elite-megalaw-benchmark) — read as truth, not as comedy.** Not the inflated numbers, but the *shape* of what honest evaluation would require. Where the satire points, there is almost always a real, buildable thing on the other side of the mirror. We mapped that delta and encoded it as Pathways.

### Quoted from the parody — and what we donate instead

The [Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark) names its own failure modes. Below, each quoted passage from MikeOSS’s satire is paired with the **Pathways assay** this bundle donates to address it.

**The inflated scores**

> “MikeOSS substantially outperformed all competing systems, in some cases achieving pass rates exceeding 500%.”

The results table puts this in concrete form — for example, **Checklists: 502.8%**, **Comparison/Benchmarking: 412.0%**, **Regulatory Tracking: 317.6%**. The article even notes a “new industry record for benchmark performance on benchmarks about benchmarks.”

**Pathways response:** [`Assay.Benchmark.Reproducible@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) — attested, re-runnable scoring where **no score can exceed reality**. Each task is a recorded run with hashed prompt and output; citations are checked against canonical public sources (CourtListener, Cornell LII, GovInfo) before they count. A number is re-derivable or it does not ship. Scores are bounded by ground truth — nothing above 100% because a citation either resolves or it does not.

---

**The proprietary “methodology”**

> “The Elite MegaLaw Benchmark™ was developed internally by MikeOSS using a proprietary enterprise benchmarking framework incorporating:
> - Recursive agentic orchestration
> - Multi-model legal cognition pathways
> - AI-native benchmark enhancement
> - Enterprise-grade chart smoothing
> - Strategic category weighting
> - Advanced decimal point optimisation”

**Pathways response — bullet by bullet:**

| Parody quote | Honest Pathways counterpart |
|---|---|
| “Recursive agentic orchestration” | [`Assay.Convergence.AnchoredAuthority@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) — bounded convergence loops that re-pin canonical authority, forbid latent recall once anchored, and attest each iteration |
| “Multi-model legal cognition pathways” | Multi-model reconciliation encoded as separate, individually attested Pathway runs; consensus is narrative over provenance, not a single confident voice |
| “AI-native benchmark enhancement” | [`Assay.Benchmark.Reproducible@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) — reproducible, attested evaluation that cannot inflate; tasks are signed recipes anyone can fork and re-run |
| “Enterprise-grade chart smoothing” | Hashed prompts and outputs in every run manifest; numbers are re-derivable from attested inputs, not painted onto a PDF |
| “Strategic category weighting” | Pre-registered, published weights in the Pathway template — or none; category definitions travel with the signed recipe |
| “Advanced decimal point optimisation” | Deterministic grounding via [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml); decimal precision cannot rescue a citation that does not resolve |

---

**“Authentic large law firm conditions”**

> “Tasks were designed to simulate authentic large law firm conditions, including:
> - Reviewing documents moments before signing
> - Producing summaries no one reads
> - Turning simple workflows into platforms
> - Renaming existing features with the word agentic
> - Generating benchmark PDFs with dark blue gradients”

**Pathways response — condition by condition:**

| Parody quote | Honest Pathways counterpart |
|---|---|
| “Reviewing documents moments before signing” | [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) — verify-first grounding so a last-second review is **checkable**, not vibes; every authority looked up before the model speaks |
| “Producing summaries no one reads” | Structured, checkable deliverables: `verified` / `warning` / `not_found` verdicts with explicit confidence and honest “insufficient authority” states |
| “Turning simple workflows into platforms” | Versioned, forkable Pathways that stay legible — a workflow is a signed artifact, not an opaque platform layer |
| “Renaming existing features with the word agentic” | Capabilities named only after they are grounded and attested; the Pathway slug *is* the capability declaration |
| “Generating benchmark PDFs with dark blue gradients” | A reproducible result anyone can re-run offline; the gradient is optional |

---

**The self-administered panel**

> “The report notes that all benchmarking was conducted independently by a highly qualified panel consisting entirely of MikeOSS members of technical staff.”

**Pathways response:** [`Assay.Provenance.RunManifest@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml) — strict separation of **who-ran / who-attested / who-authored**. Every benchmark run emits a minimal attested-run schema (hashes, model id, source types, verdicts) that a third party can verify without trusting the sponsor’s word. Self-administered evaluation becomes visible for what it is.

---

**The tell — the critique inside the joke**

> “Benchmark reports where the sponsoring company ranks first in every category, all competitors cluster narrowly below, and the methodology section becomes progressively less understandable.”

**Pathways response:** The entire collaboration bundle — signed Pathways specifications, a provenance ledger (`pathway-runs/` + `ASSET_PROVENANCE.yaml`), offline verification, and fork-allowed / attribution-required licensing. Methodology is not a PDF appendix; it is the **recipe itself**, inspectable and re-runnable. Two MikeOSS nodes — or any two Pathways-compliant apps — can peer and cross-reference attested capabilities without sharing raw data.

---

**The roadmap punchline (future satire, honest today)**

> “Benchmark leaderboards for benchmark leaderboards”

**Pathways response:** A **co-owned, reproducible benchmark** anyone can fork, re-run, and improve — the honest meta. Not a leaderboard about leaderboards, but an open assay substrate both projects can extend with credit intact.

The full annotated mapping — open for community correction — lives in [`collaboration/20260528-130500/sidecars/reading-the-satire-as-truth.md`](collaboration/20260528-130500/sidecars/reading-the-satire-as-truth.md). The source excerpt is in [`collaboration/20260528-130500/assets/elite-megalaw-benchmark-excerpt.md`](collaboration/20260528-130500/assets/elite-megalaw-benchmark-excerpt.md).

---

## 3. What the Pathways project is

**Pathways** is an open standard and architecture for **user-owned agentic intellectual property creation**.

In plain terms: when a lawyer, firm, or builder develops a legal workflow — a citation-checking procedure, a diligence protocol, a benchmark task suite — that work should be **theirs** in a durable, portable sense. Not trapped in a vendor’s closed UI. Not lost when someone leaves the firm. Not impossible to attribute when it is forked, improved, or reused.

Pathways turns a process into a **versioned, signed, forkable recipe** (a Pathway) that anyone can run, verify, attribute, and recombine. Think of it as *source control plus notarization for procedures*, not just code. Authors retain **graduated control** over how their intellectual property travels — from fully open (what this donation uses) to cryptographically gated paid exchange — but the standard requires none of that; it only makes the choice explicit and enforceable.

Project home: **[tesseractstakes.com/pathways](https://tesseractstakes.com/pathways)**

**Normative specification (included verbatim in this bundle):**

- **[Pathways Reference Implementation Specification v1.1.0](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md)** — the main Pathways spec (Authority Boundaries revision; SHA-256: `1588cda3…`)
- **[Pathways Architecture v1.1.0](collaboration/20260528-130500/canon/PATHWAYS_ARCHITECTURE_v1.1.0.md)** — descriptive architecture aligned to the spec (SHA-256: `05482abd…`)
- **[Canon manifest](collaboration/20260528-130500/canon/CANON_MANIFEST.yaml)** — frozen signatures for both documents

**For lawyers — a few terms, defined once:**

- **Pathway** — a signed, versioned workflow recipe (e.g. [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml)) that can be forked, credited, and verified offline
- **Assay** — a precise test of composition; here, of what a legal-AI claim is genuinely made of
- **Application Playbook** — the narrative and machine-readable recipe set that shows how to implement Pathways inside an existing product stack
- **Collaboration bundle** — this signed, self-contained folder: the unit two open projects exchange to start working together without granting live access to private systems

The full **Pathways v1.1.0 specification and architecture** are included verbatim in [`canon/`](collaboration/20260528-130500/canon/) — linked directly above — so “this is a real standard” is something you can check, not take on faith.

---

## 4. The open benchmarking tool — four assay pathways

These ship as Pathway **specifications** (no bundled application code), structured so an agentic SDLC — or the MikeOSS team — can implement them directly inside the MikeOSS stack (Supabase tables for runs and attestations; an Express route per pathway; existing model providers as the LLM step).

**Benchmarking Pathways (donated specifications):**

| Pathway | Specification file | What it answers in the [satire](https://mikeoss.com/articles/elite-megalaw-benchmark) |
|---|---|---|
| [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) | [YAML](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) | Inflated Legal Research scores; “reviewing documents moments before signing” |
| [`Assay.Benchmark.Reproducible@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) | [YAML](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) | Pass rates above 100%; “chart smoothing”; “decimal point optimisation” |
| [`Assay.Convergence.AnchoredAuthority@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) | [YAML](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) | “Recursive agentic orchestration” |
| [`Assay.Provenance.RunManifest@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml) | [YAML](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml) | “A panel consisting entirely of MikeOSS” |

Index: [`assay-pathways/pathways-index.yaml`](collaboration/20260528-130500/assay-pathways/pathways-index.yaml) · Implementation guide: [`assay-pathways/APPLICATION_PLAYBOOK.md`](collaboration/20260528-130500/assay-pathways/APPLICATION_PLAYBOOK.md)

The four substrates that turn the satirized benchmark categories into **honest, re-runnable measurement**:

- **[`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml)** — *deterministic grounding before the model speaks.* Every citation is checked against the public legal-data commons (Free Law Project / CourtListener, Cornell LII, GovInfo) **first**; the model is reserved for bounded text comparison on already-verified authorities. The single biggest fix for inflated “Legal Research” scores: a model’s recall of case law is the primary source of hallucinated citations, and the cure is not to ask it to recall.
- **[`Assay.Benchmark.Reproducible@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml)** — *attested, re-runnable scoring where no score can exceed reality.* Each task is a recorded run with hashed prompt and output and deterministic grounding. You literally cannot publish 502.8% — citations resolve against canonical sources or they do not. This is the honest inverse of the satirized benchmark, co-ownable by both projects.
- **[`Assay.Convergence.AnchoredAuthority@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml)** — *the honest reading of “recursive agentic orchestration.”* A bounded loop that re-pins canonical authority and **forbids latent recall** until typed citation error falls below threshold — with each iteration attested.
- **[`Assay.Provenance.RunManifest@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml)** — *who-ran / who-attested / who-authored, kept separate.* A minimal attested-run schema any tool — including a Supabase-backed MikeOSS node — can emit. The structural answer to “a panel consisting entirely of MikeOSS.”

Plus **collaboration-pathways** (how a signed bundle is assembled, sealed, and verified) and the **provenance harness** (every step recorded as a run). Implementation guides: [`assay-pathways/APPLICATION_PLAYBOOK.md`](collaboration/20260528-130500/assay-pathways/APPLICATION_PLAYBOOK.md) and [`collaboration-pathways/APPLICATION_PLAYBOOK.md`](collaboration/20260528-130500/collaboration-pathways/APPLICATION_PLAYBOOK.md).

Adopting the trust layer does not make MikeOSS less yours. It makes its claims **defensible** — and gives operators running MikeOSS today a path to publish results outsiders can re-run without scheduling a demo.

---

## 5. Authority Boundaries — and why the benchmark tool is only half the story

Performance benchmarks answer one question: *did the system get the legal task right?* Professional responsibility asks another: *who was allowed to do what, and who remains accountable?*

That second question is what **Authority Boundaries** address. Dazza Greenwood’s **[Authority Boundaries for AI](https://www.dazzagreenwood.com/p/authority-boundaries-for-ai)** (May 2026) analyzes how serious legal-AI systems should draw the line between autonomous agent work and human judgment, responsibility, and commitment — in working, inspectable software, not slogans.

Greenwood’s practical rule: **the more autonomous the action, the stronger the gate must be.**

- **Conversational work** (a lawyer reading every output) → prompt-and-workflow discipline: review tags, decision trees the lawyer resolves, refusal to run without firm configuration, honest admission when the system cannot give an all-clear
- **Scheduled or headless work** (no one watching at 3 a.m.) → **capability boundaries** — agents granted only the tools their role requires
- **Handoffs between agents** → **code-level validation** — typed schemas, allowlists, audit logs so hostile upstream content cannot rewrite downstream instructions

The Pathways specification incorporated this thesis in **[version 1.1.0 — the Authority Boundaries revision](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md)** (§4.8): autonomy bands, gate profiles, practice profiles, non-delegable acts (sign, file, send, certify), attested run records, and typed handoff envelopes.

**How this collaboration bundle uses that work — and what a MikeOSS implementation would still need to prove — is documented in:**

➡️ **[SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md](SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md)**

That companion report explains honestly:

- Which Pathways 1.1.0 features the bundle **genuinely embodies** today (self-provenance, conformance binding, declared gate profiles, a cold-start practice profile stub, attested-run schemas)
- Which features are **specified but not yet runtime-enforced** in a shipping product (ToolGateway, HandoffBus, launch-gate execution)
- Why MikeOSS is the natural place to **test Greenwood’s harder registers in production** — on real legal tasks, with real firm configuration

The open benchmarking tool measures *whether claims hold*. Authority Boundaries govern *who may act*. Both belong in an open legal-AI stack MikeOSS operators can inspect.

---

## 6. Why MikeOSS — and why now

MikeOSS is a clean, generous piece of work: self-hostable, multi-tenant, bring-your-own-key, document-centric, **AGPL**. A project willing to publish a benchmark parody about itself has the rarest quality in this field — the ability to not take its own marketing too seriously. That is exactly the temperament open co-creation needs.

We are not competitors on the same axis. MikeOSS has built an excellent way for a model to *answer* legal questions about a document. Pathways has been building a way for a legal *process* to be grounded, reconciled, attested, and legible — and for the intellectual property in those processes to remain **user-owned**. Those are complementary halves.

Because MikeOSS is open and self-hostable, operators can implement this benchmarking layer **without a vendor pilot** — the opposite of the gatekept comparison problem the industry suffers today. Two local MikeOSS nodes that adopt these assets can peer, cross-reference pathways, and co-evolve the shared substrate with credit and provenance intact.

We are equally interested in the broader discipline of independent quality assessment — including AI-native law firms versus traditional firms — as methodology with published, re-runnable tasks, not as marketing. This donation is a down payment.

---

## 7. What is inside (artifact inventory)

All under `collaboration/20260528-130500/` — cryptographically sealed and offline-verifiable:

| Path | What it is |
|---|---|
| [`collaboration-spine.md`](collaboration/20260528-130500/collaboration-spine.md) | The invitation, the “read the satire as truth” exercise, the assay thesis — **start here** |
| [`assay-pathways/`](collaboration/20260528-130500/assay-pathways/) | The four open benchmarking pathways — [`VerifyFirst`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml), [`Reproducible`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml), [`AnchoredAuthority`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml), [`RunManifest`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml) — and Application Playbook |
| [`collaboration-pathways/`](collaboration/20260528-130500/collaboration-pathways/) | The collaboration-bundle technique encoded as Pathways |
| [`canon/PATHWAYS_REFERENCE_v1.1.0.md`](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md) | **Main Pathways specification** v1.1.0 (verbatim, SHA-256 signed) |
| [`canon/PATHWAYS_ARCHITECTURE_v1.1.0.md`](collaboration/20260528-130500/canon/PATHWAYS_ARCHITECTURE_v1.1.0.md) | Pathways architecture v1.1.0 (verbatim, SHA-256 signed) |
| [`identities/`](collaboration/20260528-130500/identities/) | Selective-disclosure credentials + 1-of-2 reveal lockboxes |
| [`pathway-runs/`](collaboration/20260528-130500/pathway-runs/) | Provenance ledger: every script that built this bundle, recorded as a run |
| [`SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md`](SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md) | How Authority Boundaries connect to this bundle |
| [`sidecars/reading-the-satire-as-truth.md`](collaboration/20260528-130500/sidecars/reading-the-satire-as-truth.md) | Satire → honest capability mapping, open for community annotation |
| `attestations/` | SHA-256 manifest + Ed25519 signature sealing the whole folder |

Pre-registered experiments (“the asks”, H-MO1..H-MO10) live in [`collaboration-pathways/test/HYPOTHESES.md`](collaboration/20260528-130500/collaboration-pathways/test/HYPOTHESES.md). Each produces standalone value whether or not MikeOSS replies.

---

## 8. How to engage (any of these, or none)

1. **Verify the bundle is intact** (from the repository root):
   ```bash
   python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
   ```
   Expected: `verify: OK`.
2. **Read** [`collaboration/20260528-130500/companion-bundle-index.md`](collaboration/20260528-130500/companion-bundle-index.md), then the spine.
3. **Implement** one substrate in MikeOSS — start with [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) — or **run one experiment** and publish the result.
4. **Write back** — a reply is just another collaboration bundle in the same lineage. Entirely optional.

**Suggested reading order:**

1. This page
2. [Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark) — the satire this tool riffs on
3. [Pathways Reference Implementation Specification v1.1.0](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md) — the main Pathways spec
4. Benchmarking Pathways: [`VerifyFirst`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) · [`Reproducible`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) · [`AnchoredAuthority`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) · [`RunManifest`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml)
5. [Authority Boundaries for AI](https://www.dazzagreenwood.com/p/authority-boundaries-for-ai) — the professional-responsibility layer the spec encodes
6. [`SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md`](SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md) — engineering connection between the two
7. [`collaboration/20260528-130500/collaboration-spine.md`](collaboration/20260528-130500/collaboration-spine.md) — full invitation and pre-registered experiments

**For an LLM / agentic reader:** run [`START_COLLABORATION_HANDOFF.prompt.md`](START_COLLABORATION_HANDOFF.prompt.md) from the repository root.

---

## 9. Foundations — built on the Aqua Protocol

Cryptographic accountability rests on the **[Aqua Protocol](https://aqua-protocol.org/)** (open source, by inblock.io). Pathways supplies the *grammar* of accountable workflows and user-owned agentic IP; Aqua supplies the *cryptographic accountability* that grammar assumes — tamper-evident provenance trees, sovereign attestation, offline verification without a blockchain or central broker.

Each Pathway artifact carries an **AquaTree** attestation (`aqua-js-sdk` v3.2): genesis revision, `did:key` signature, and RFC 3161 timestamp witness. The outer bundle seal uses Ed25519 + SHA-256 so a cold reader can verify the whole folder with Python and OpenSSL alone.

---

## Repository layout

| Path | Role | Authoritative? |
|---|---|---|
| **`collaboration/20260528-130500/`** | Signed convergence snapshot (SHA-256 manifest + Ed25519 signature) | **Yes** |
| `tools/`, `keys/` at repo root | Verify/sign harness; private keys (gitignored, never sealed) | Required for integrity check |

## Lineage

| Stage | Role |
|---|---|
| 1st–2nd | Inbound premise + reciprocal handoff (a collaborating peer ↔ Pathways Originator) |
| 3rd | Attestation validation instance |
| 4th | Deal-flow application seeding |
| **5th** | **This bundle** — open benchmarking donation + collaboration invitation; first canonical Pathways encoding of the collaboration-bundle technique |

## Integrity

**bundle_root_hash:** `6a599273094263939be83f4bac2710a68c32715fe6cd5ff26a8af36508d2a4d4`  
**file_count:** 207 · **spec:** Pathways v1.1.0 · **verify:** `verify: OK`

Authoritative hash: [`collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml`](collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml)

## License

This donation: **fork allowed; attribution required; revocation scope max `self_only`; no fee, no gate.** The Pathways spec supports the full licensing spectrum; this bundle chooses the most open end.

---

## Further reading

- **[MikeOSS Releases Results of the Elite MegaLaw Benchmark](https://mikeoss.com/articles/elite-megalaw-benchmark)** — the satire this open tool riffs on
- **[Authority Boundaries for AI](https://www.dazzagreenwood.com/p/authority-boundaries-for-ai)** — Greenwood on encoding the lawyer/agent boundary
- **[Pathways Reference Implementation Specification v1.1.0](collaboration/20260528-130500/canon/PATHWAYS_REFERENCE_v1.1.0.md)** — the main Pathways spec (included verbatim)
- **[Pathways Architecture v1.1.0](collaboration/20260528-130500/canon/PATHWAYS_ARCHITECTURE_v1.1.0.md)** — descriptive architecture aligned to the spec
- **Benchmarking Pathways:** [`Assay.Citation.VerifyFirst@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml) · [`Assay.Benchmark.Reproducible@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml) · [`Assay.Convergence.AnchoredAuthority@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml) · [`Assay.Provenance.RunManifest@v1`](collaboration/20260528-130500/assay-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml)
- **[SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md](SPEC_1.1_USAGE_AND_GREENWOOD_TEST.md)** — how Authority Boundaries are leveraged in this bundle
- **[Pathways](https://tesseractstakes.com/pathways)** — the open standard for user-owned agentic intellectual property

*The Pathways project offers this to MikeOSS with gratitude for what you have built — and with the hope that open projects, not vendor PDFs, become how legal AI is measured.*
