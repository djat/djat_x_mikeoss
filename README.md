# A Donation + Open Collaboration Invitation — to the MikeOSS project & team

*From one open project to another. This bundle **donates** the core trust substrates that turn the Elite MegaLaw Benchmark from satire into something you could actually stand behind — grounded, reproducible, attested. **No strings.** No account, no install, no obligation, no license fee. You can read it in a browser, verify it offline, drop the pieces straight into MikeOSS, fork it, or ignore it. This page assumes zero prior context.*

---

## TL;DR (60 seconds)

- Your *Elite MegaLaw Benchmark* post is excellent satire about legal-AI benchmark theater (>100% scores, a panel "consisting entirely of MikeOSS"). We took it seriously and asked: *what would the honest version actually require?*
- The honest version needs four things a document-chat product structurally lacks: **verify-first grounding**, **multi-model reconciliation**, **provenance/attestation**, and **honest convergence**. We're **donating** all four as ready-to-implement **Pathways** specifications.
- They arrive as an **Application Playbook** — a narrative + machine-readable recipe set that drops directly into the MikeOSS stack (Supabase/Next/Express), no rewrite required.
- The same substrate lets any two Pathways-compliant apps — including **two local MikeOSS nodes** — **peer** and cross-reference each other's work across multiple dimensions, privately, and **infer better practices from each other** without sharing raw data.
- It's a **commons**: owned by neither project. The Pathways spec supports a full spectrum of licensing — from fully free (what this donation uses) to cryptographically gated paid exchange — but **requires none of it**.

---

## 1. What this is — a donation, with no strings

This is not a sales pitch, not a contract, and not a request for your data, code, or money. It is a **gift of mechanisms**: the small set of trust primitives that make legal-AI claims *checkable* rather than merely *asserted*.

The satire lands because everyone in legal AI recognizes the failure mode — a vendor grading its own homework with unverifiable numbers. The cure isn't a better marketing department; it's **infrastructure that makes lying impossible to do quietly**. We built that infrastructure as an open standard called **Pathways**, and this bundle hands you the relevant parts, free, under a fork-allowed / attribution-only posture.

Everything here is **specifications, recipes, prose, and cryptographic attestation** — no executable application code to adopt or trust blindly. You implement it in your own stack, on your own terms, or not at all.

---

## 2. For the lawyer reading this — the plain-language version

A few terms, defined once:

- **Pathways** — an open standard for writing a *workflow* down as a **versioned, signed, forkable recipe** (a small file with a stable name like `Assay.Citation.VerifyFirst@v1`). Once a process is a signed artifact, anyone can **run it, verify exactly what happened, attribute it, fork it, and recombine it.** Think of it as *source control + notarization for procedures*, not just code. Project home: **[tesseractstakes.com/pathways](https://tesseractstakes.com/pathways)**.
- **Assay** — a precise test of what something is genuinely made of; an *assayer* certifies the true composition of a metal. The **assay pathways** test what a legal-AI claim is really made of — grounded citations, reproducible scores, attested runs — the honest measurement the satire only performs.
- **Collaboration bundle** — this signed, self-contained folder: the unit two parties exchange to start working together without granting each other live access to private systems. You can confirm it is intact and untampered with one command (see §9).

The full **Pathways v1.1.0 specification + architecture** are included verbatim in [`collaboration/20260528-130500/canon/`](collaboration/20260528-130500/canon/) (with sha256 signatures), so "this is a real standard" is something you can check, not take on faith.

---

## 3. What's donated — the core substrates, as an Application Playbook

These ship as Pathway **specifications** (no bundled code), structured so an agentic SDLC — or your team — can implement them directly inside MikeOSS (Supabase tables for runs/attestations; an Express route per pathway; the existing model providers as the LLM step). The four substrates that turn the satirized categories into honest capabilities:

- **`Assay.Citation.VerifyFirst@v1`** — *deterministic grounding before the model speaks.* Every citation is checked against the public legal-data commons (Free Law Project / CourtListener, Cornell LII, GovInfo) **first**; the model is reserved for a bounded text-comparison on already-verified authorities. This is the single biggest fix for "Legal Research 271.5%" — a model's recall of case law is the #1 source of hallucinated citations, and the cure is to not ask it to recall.
- **`Assay.Benchmark.Reproducible@v1`** — *attested, re-runnable scoring where no score can exceed reality.* Each task is a recorded run with hashed prompt + output and deterministic grounding. You literally cannot publish 502.8% — the citations resolve against canonical sources or they don't. This is the honest inverse of the satirized benchmark, co-ownable by both projects.
- **`Assay.Convergence.AnchoredAuthority@v1`** — *the honest reading of "recursive agentic orchestration."* A bounded loop that re-pins canonical authority and **forbids latent recall** until typed citation error falls below threshold — with each iteration attested.
- **`Assay.Provenance.RunManifest@v1`** — *who-ran / who-attested / who-authored, kept separate.* A minimal attested-run schema any tool (including a Supabase-backed one) can emit. This is the structural answer to "a panel consisting entirely of MikeOSS."

Plus the **collaboration-pathways** (how a signed bundle is assembled, sealed, and verified) and the **provenance harness** (every step recorded as a run). See the playbooks: [`assay-pathways/APPLICATION_PLAYBOOK.md`](collaboration/20260528-130500/assay-pathways/APPLICATION_PLAYBOOK.md) and [`collaboration-pathways/APPLICATION_PLAYBOOK.md`](collaboration/20260528-130500/collaboration-pathways/APPLICATION_PLAYBOOK.md).

The recipes are unchanged building blocks; **you keep your product, your UX, and your edge.** Adopting the trust layer doesn't make MikeOSS less yours — it makes its claims defensible.

---

## 4. Decentralized hyper-collaboration across private context

Here's the part that goes beyond one integration. Because every pathway, run, and identity is a signed, addressable artifact, Pathways enables **privacy-preserving, agent-mediated collaboration** across organizations that never expose their raw data to each other:

- **Selective-disclosure identities.** This bundle already ships identity credentials with **commitment hashes** and **1-of-2 reveal lockboxes** (see [`identities/`](collaboration/20260528-130500/identities/)): you can prove "a real, vetted party stands behind this work" and reveal *only* what you choose, to *whom* you choose. **Zero-knowledge progressive reveal and homomorphic matching are the explicit roadmap** — the commitment design is the first step.
- **Agent-mediated matching, discovery, and recommendation.** An agent acting for MikeOSS can ask the network "who has a higher-fidelity citation-grounding pathway for the Ninth Circuit?" and be **matched, by inference, against attested capabilities** — without either side disclosing private corpora, clients, or methods. Discovery runs over signed *capability descriptions*, not over your data.

The result is hyper-collaboration where **what is shared is the attested shape of a capability**, not the confidential substance behind it.

---

## 5. Proof of personhood — this bundle as a *trust proxy* for its authors

This bundle carries the de-identified lineage of several real collaborators (`person-a`, `entity-1`, …). Their names are masked — but their **participation is not erased, it is attested.** The bundle itself acts as a **trust proxy**: it lets a cold reader trust, *by inference*, that real, unique people and entities stand behind every embedded pathway — **without exposing a single name**, and without asking you to take that on faith.

Each masked author keeps four things at once:

- **Sovereign proof of participation.** Every placeholder has a public, self-asserted **Personhood Credential** (for a person) or **Entity Credential** (for an org) carrying a salted commitment `sha256(real_name‖salt)`. The name never appears, but a later reveal can be *checked against* the commitment — so the proof is real, not a promise.
- **Full attribution of the underlying lineage.** On reveal, the placeholder resolves to a DID **and to every Pathways-encoded provenance record it underpins** — the run ledger, fork lineage, and `Term` edges in [`pathway-runs/`](collaboration/20260528-130500/pathway-runs/). The credit for the substrate beneath the referenced pathways is theirs, and it is structural.
- **Forward rights — sovereign control of what comes next.** The reveal is a **1-of-2 lockbox**: the Originator can open it now as an interim convenience, but **each author's own key is the upgrade path**, so reveal — *and any future action taken under that identity* — remains theirs to authorize. Future actions may be bounded by **inherited constraints** that travel as explicit, signed terms with a clear cryptographic lineage back to this attestation (they bind forks, never the person's autonomy outside this context).
- **Privacy.** Nothing reveals without a holder of the reveal key. You can open the **client-side reveal viewer** at [`identities/viewer/index.html`](collaboration/20260528-130500/identities/viewer/index.html) in any browser; it shows *where* attribution has been sealed and reveals nothing without the key.

**The technique itself is now encoded as a Pathway** — `Collaboration.Identity.SovereignAttributionProxy@v1` ([file](collaboration/20260528-130500/collaboration-pathways/pathways/Collaboration.Identity.SovereignAttributionProxy.v1.yaml)), **authored by the Originator (DJ Thomson)**. It is identity *masking as attestation*: de-identify → bind the placeholder to a real DID / public identity anchor via a Personhood/Entity Credential → seal a 1-of-2 reveal lockbox → assert person↔entity relationships → grant forward rights with cryptographic lineage. So the method that protects these collaborators is itself an inspectable, forkable, attributed recipe — not a one-off. MikeOSS is, implicitly, the first collaborator whose invitation occasioned that encoding.

**Scaffolding & roadmap.** The credential shapes and lockboxes in [`identities/`](collaboration/20260528-130500/identities/) are prototyped to be **OpenVTC-compatible** — [github.com/OpenVTC/openvtc](https://github.com/OpenVTC/openvtc), an open Rust toolkit for DIDs, Verifiable Credentials, **Personhood Credentials (PHCs)** and **Verifiable Relationship Credentials (VRCs)** over `did:webvh`. A production deployment would issue real `did:webvh` Persona DIDs and exchange VRCs over DIDComm, and we see strong **future integration potential with the First Person Project & network** ([firstperson.network](https://firstperson.network)), whose first-person trust model these credentials are designed to interoperate with. Zero-knowledge progressive reveal and homomorphic matching remain the explicit next steps; the salted-commitment design is the first.

---

## 6. Peering — two Pathways apps (including two MikeOSS nodes) cross-referencing across dimensions

Any two **Pathways-compliant** applications — two firms, two products, or **two local MikeOSS nodes that adopt these assets** — can establish a **trusted peering relationship** (the spec's §10 invite / accept / verify / revoke protocol; conformance Level **F** = "federation-ready, can peer"). Peering needs **no central broker** and **no shared runtime** — just mutual genesis attestations.

Once peered, they cross-reference each other's pathways across the spec's **six discovery dimensions** simultaneously:

- **symbolic** (exact names, slugs, identifiers),
- **semantic** (meaning / embedding similarity),
- **physical / spatial** (jurisdiction, locality),
- **contextual** (the lens or domain a pathway operates in),
- **temporal** (when, recency, version history),
- **lineage** (fork ancestry and attribution).

Cross-referencing across these `composite_domain` / `context_lens` / `abstract_capability` registry substrates lets two peers **infer best practices and concrete improvements from each other** — e.g. "your judge-research pathway and mine converge except your authority-synthesis step has a lower not-found rate; here's the delta." Variation is **safe, reversible, and rewarding** because every change carries a signed author and explicit rights (§7). Two MikeOSS nodes starting from these same assets can therefore *co-evolve* — each improving the shared substrate, with credit and provenance intact.

---

## 7. License precision — from free to cryptographically gated, with no requirement

The Pathways spec gives authors **precise, graduated control** over how their pathways travel — a wide spectrum, none of it mandatory. Every published template carries **four author rights** that travel with it cryptographically (license terms are part of the signed artifact and follow it across forks):

- **Attribution** — every change has a signed author; credit is structural, not optional.
- **License** — `license_terms` set at publication apply to all forks unless a fork explicitly renegotiates via marketplace mechanics. Terms range from *fully open* (fork freely) to *terms-bound*, and **may reference external payment systems** so a pathway's use can be **cryptographically and contractually gated** (pay-per-run, revenue share, seat licensing) — though the spec defines **no** payment rail and **requires none**.
- **Revocation** — forward-only: an author may withdraw future use without ever invalidating historical, already-attested operations (irrevocable licenses honor existing forks).
- **Co-attestation** — peers can vouch for each other's templates, building reputation without a central authority.

So the same standard supports a tiny solo author giving everything away, *and* a firm that wants metered, contract-gated access to a proprietary method — by changing only the `license_terms`, not the mechanism. Forks even surface a **"gates removed" badge** so any stripping of safeguards is visible and attestable.

**This donation sits at the fully-open end:** fork allowed, attribution required, revocation scope `self_only`, **no fee, no gate.** The precision exists so that *if* value ever flows between the projects, it can — transparently, contractually, on terms you set — but nothing here asks it to.

---

## 8. What's inside (artifact inventory)

All under `collaboration/20260528-130500/`:

- [`collaboration-spine.md`](collaboration/20260528-130500/collaboration-spine.md) — the invitation, the read-the-satire-as-truth exercise, the assay thesis, the asks. *Start here if you read one thing.*
- [`assay-pathways/`](collaboration/20260528-130500/assay-pathways/) — the four donated trust substrates (§3).
- [`collaboration-pathways/`](collaboration/20260528-130500/collaboration-pathways/) — the collaboration-bundle technique encoded as Pathways, plus `Term` artifacts that make even the *names* versioned and licensable.
- [`canon/`](collaboration/20260528-130500/canon/) — the **Pathways v1.1.0 specification + architecture** (verbatim, with sha256 signatures).
- [`identities/`](collaboration/20260528-130500/identities/) — selective-disclosure credentials + 1-of-2 lockboxes + a browser viewer; the **trust-proxy / proof-of-personhood** layer (§5).
- [`pathway-runs/`](collaboration/20260528-130500/pathway-runs/) — the provenance ledger: every script that built this bundle, recorded as a run, mapped in `ASSET_PROVENANCE.yaml`.
- `attestations/` — the SHA-256 manifest + Ed25519 signature sealing the whole folder.

The 9-10 small, **self-validating experiments** ("the asks") are in [`collaboration-pathways/test/HYPOTHESES.md`](collaboration/20260528-130500/collaboration-pathways/test/HYPOTHESES.md) — each produces value whether or not you ever reply.

---

## 9. How to engage (any of these, or none)

1. **Verify it's intact** (from the repo root):
   ```bash
   python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
   ```
   Expected: `verify: OK`.
2. **Read** [`collaboration/20260528-130500/companion-bundle-index.md`](collaboration/20260528-130500/companion-bundle-index.md), then the spine.
3. **Implement** one substrate (start with `Assay.Citation.VerifyFirst`) inside MikeOSS, or **run one experiment** and publish the result.
4. **Write back** — a reply is just another collaboration bundle in the same lineage. Entirely optional.

### For an LLM / agentic reader
Run [`START_COLLABORATION_HANDOFF.prompt.md`](START_COLLABORATION_HANDOFF.prompt.md) from the repo root; paste everything below `--- BEGIN PROMPT ---` as your first message.

---

## Repository layout

| Path | Role | Authoritative? |
|---|---|---|
| **`collaboration/20260528-130500/`** | Signed convergence snapshot (SHA-256 manifest + Ed25519 signature) | **Yes** |
| `tools/`, `keys/` at repo root | Verify/sign harness; private keys (gitignored, never sealed) | Required for integrity check |

## Lineage

| Stage | Role |
|---|---|
| 1st–2nd | Inbound premise + reciprocal handoff (a collaborating peer ↔ Originator) |
| 3rd | `prior-instance-3` — attestation validation instance |
| 4th | `prior-instance-4` — deal-flow application seeding |
| **5th** | **this bundle** — donation + open invitation; first canonical Pathways encoding of the collaboration-bundle technique |

(`person-a`, `prior-instance-N`, etc. are de-identified placeholders; identifiable parties are sealed in `identities/` and revealable only under their own control. Co-originators of the technique: **a collaborating peer + the Originator, DJ Thomson**.)

## Integrity

**bundle_root_hash (recorded outside the seal):** `8cb466fc2fb9d3e16e1869d40ec3d2ac044d7d0501257ef26620a2ea23605ff3`
**file_count:** 153 · **signing:** Ed25519 over bundle_root_hash · **spec:** Pathways v1.1.0 · **verify:** `verify: OK`
Authoritative hash lives in [`collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml`](collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml).

## License

This donation: **fork allowed; attribution required; revocation scope max `self_only`; no fee, no gate.** (The Pathways spec supports the full licensing spectrum of §7; this bundle chooses the most open end.)
