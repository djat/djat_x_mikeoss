# How the Collaboration Bundle Uses Pathways v1.1.0 — and Why It Tests the Greenwood "Authority Boundaries" Thesis

*A companion report (outside the sealed snapshot). It is honest about what the bundle genuinely **uses**, what it only **designs toward**, and what it deliberately **leaves to a MikeOSS adoption** — because that last gap is precisely where the significant test lives.*

---

## 0. What is actually "new" in 1.1.0

Per the spec's own change header (`canon/PATHWAYS_REFERENCE_v1.1.0.md`, line 8), the **only** features introduced in the 1.1.0 *Authority Boundaries* revision are:

1. **§4.8 Autonomy Bands and Gate Profiles** — autonomy bands `A0`–`A3`; the **six registers of restraint** `R1`–`R6`; per-band minimum-register requirements; three enforcement choke points (launch / pre-step / seam).
2. **The `ToolGateway`** (R2 capability + R4 economic + R5 temporal + R6 phase) and **`HandoffBus`** (R3 code-at-seams) runtime contracts.
3. **Practice profile (R1 cold-start)** — a DID-signed, Aqua-attested tenant config that the engine refuses to run without (`BLOCKED_CONFIGURATION`).
4. **`non_delegable_acts`** registry (Level R).
5. **§13.7 gate-profile conformance tests** and new normative fields (`autonomy` on `PathwayRun`, `gate_profile` manifest on templates).
6. **Appendix C — Spec Self-Provenance and Meta-Pathways** — the spec encodes *its own* origin and revision provenance as Pathways and PathwayRuns.

Everything else the bundle leans on (conformance levels M/S/F/R, trusted peering, the four author rights, license precision, the six discovery dimensions, genesis attestation) is **1.0.0** and is **not** counted as "new" here. This report is strict about that distinction because the question was specifically about *new* 1.1 features.

The spec is explicit (line 292) that §4.8 "was introduced in spec version 1.1.0 **in response to** *Authority Boundaries for AI* (Greenwood, 2026-05-20)." So the new 1.1 surface **is** the Greenwood thesis, rendered normative. That is why "which 1.1 features does the bundle use" and "how does the bundle test Greenwood" are the same question viewed from two ends.

---

## 1. Verdict at a glance

| 1.1 feature (new) | Bundle status | Where / how |
|---|---|---|
| **Appendix C — spec self-provenance / meta-pathways** | **Genuinely embodied** | The whole bundle is a working instance: `Pattern.CollaborationBundle.SelfDescribing`, `Collaboration.Meta.EmbedTechniqueProvenance@v1`, `pathway-runs/` + `ASSET_PROVENANCE.yaml` |
| **Conformance binding to ≥1.1.0** (new normative requirement) | **Genuinely used** | `collaboration-pathways/PACKAGE.yaml` → `conforms_to_spec: 1.1.0` + `reference_spec_sha256` + `architecture_sha256` |
| **Autonomy bands (A0–A3)** | **Declared** *(hardened 2026-05-29)* | `Assay.Citation.VerifyFirst` → `default_autonomy: A0`; `Assay.Convergence.AnchoredAuthority` → `default_autonomy: A1, max_autonomy: A2` |
| **Registers R1 / R4 / R5 / R6** | **Declared as a `gate_profile`** | `VerifyFirst`: R1. `AnchoredAuthority`: R1 + R4 (`max_usd`/`max_tokens`) + R5 (`halt_channel`/`idle_ttl`) + R6 (phase profile with `human_gate: required` on the converge step) |
| **`gate_profile` manifest (§4.8.4)** | **Present** | Full §4.8.4 manifests (autonomy, registers, `escalation_rule: strict`, attestation) on both citation pathways |
| **Practice profile cold-start (§4.8.5 / R1)** | **Present (stub)** | `assay-pathways/practice-profiles/legal-research-grounding.v1.yaml` — kind `practice_profile`, DID-signed, anti-pattern annotations; the R1 refs resolve so the cold-start gate passes |
| **`non_delegable_acts`** | **Declared** | `[sign, file, send_external, certify]` on both citation gate profiles |
| **Attested-run record (§4.8.6)** | **Present** | `Assay.Provenance.RunManifest` now persists `autonomy` + `effective_gate_profile` (+ practice-profile revision hash) |
| **`HandoffBus` envelope (§4.8.7 / R3)** | **Schema present, not runtime-enforced** | `RunManifest` carries a typed `handoff_envelope_schema` (closed intent enum + JSONSchema params + target allowlist) a HandoffBus would validate |
| **`ToolGateway` (R2/R4/R5/R6 runtime)** | **Not exercised** | No runtime engine ships in the bundle — the gate profiles declare the intent for a Level-F runtime to enforce |
| **§13.7 gate-profile conformance tests** | **Not run** | Requires an executable Level-F/R engine |

The honest summary: as of the 2026-05-29 hardening run (`Collaboration.Refactor.HardenGateProfile@v1`), the bundle now **carries** the full §4.8 authority-boundary manifest surface — autonomy bands, register-typed gate profiles, a cold-start practice profile, an attested-run record, and a typed handoff envelope — in addition to **using** Appendix C self-provenance and **binding itself to 1.1.0 by signature**. What remains unbuilt is only the **runtime that enforces** those manifests (ToolGateway/HandoffBus/launch-gate execution), because the bundle ships no engine. The package therefore declares its **authoring level honestly as M** (code-free) while marking the templates **Level-F-enforceable** (`gate_profile_target_level: F` in `assay-pathways/PACKAGE.yaml`). That enforcement gap is the proposed experiment, not an omission.

---

## 2. The new feature the bundle genuinely uses: Appendix C (self-provenance / meta-pathways)

This is the strongest and most literal alignment. Appendix C's premise is that a spec should encode *its own* origin as Pathways + PathwayRuns, so the artifact can explain how it was made. The bundle applies that exact discipline **one level down**, to itself:

- **Every script that built the bundle was run through a provenance harness** (`Collaboration.Attestation.RecordPathwayRun@v1` / `run_with_provenance.py`), producing the `pathway-runs/` ledger — source + hash, argv, stdout/stderr, exit code, and pre/post hashes of every changed file.
- **`pathway-runs/ASSET_PROVENANCE.yaml`** maps *every generated asset → producing Pathway → run → hash*, and a completeness gate (`Collaboration.Refactor.Finalize@v1`) refuses to seal unless every artifact is accounted for.
- **The technique itself is a first-class artifact**: `Pattern.CollaborationBundle.SelfDescribing`, `Collaboration.Meta.EmbedTechniqueProvenance@v1`, and `Term.*` nodes make even the *names* ("collaboration bundle," "assay") versioned, superseding, licensable artifacts with lineage.

In other words, the bundle is a **recursive proof of Appendix C**: where the spec says "a spec can carry its own provenance as Pathways," the bundle demonstrates "so can a *deliverable built under that spec*." That is the cleanest possible use of a 1.1-only feature, and it is fully verifiable offline.

---

## 3. How the bundle now declares the register surface (hardened 2026-05-29)

`Assay.Convergence.AnchoredAuthority@v1` is the bundle's reading of the satire's "recursive agentic orchestration," and it was — almost line for line — a Greenwood register profile written as a workflow. The 2026-05-29 hardening run promoted that prose into a formal `gate_profile`, so it is now engine-enforceable rather than merely descriptive:

```
never use latent/parametric recall for case references —
answer only from the anchored authority; if a reference
is not in the anchor, return not_found + a fallback link.
Each iteration is attested; grounding is monotonic;
depth and budget are bounded.
```

Mapped to the now-declared registers (`gate_profile`, `default_autonomy: A1`, `escalation_rule: strict`):

- **R1 (prompt-and-workflow restraint):** `enabled: true` with `output_contract_profile: assay.converged_verification.v1`, `recoverable_error_bias: true`, and a `practice_profile_ref` — "answer only from the anchored authority… else `not_found` + fallback link" is exactly Greenwood's *capability-gap honesty* and *recoverable-error bias*.
- **R4 (economic):** `enabled: true` with `max_usd: 5.00` / `max_tokens: 200000` — halt before overspend, now a typed field a runner can enforce.
- **R5 (temporal):** `enabled: true` with `halt_channel` + `idle_ttl_seconds`, backing the existing bounded `max_depth` / `threshold` stop condition with an external halt switch.
- **R6 (contextual/phase):** `enabled: true` with a phase list and `human_gate: required` on the `converge_or_halt` step — the A1 commit gate (a human approves the converged verdict before it leaves the loop).
- **A0:** `Assay.Citation.VerifyFirst` now declares `default_autonomy: A0` with R1 only — a licensed human reads verified/warning/not-found output before any external effect.

The **formal wrapper is now present**: both citation pathways carry a §4.8.4 `gate_profile` (with `non_delegable_acts: [sign, file, send_external, certify]` and an attestation block), a §4.8.5 `practice_profile` ships so the R1 cold-start gate resolves, and `Assay.Provenance.RunManifest` persists the effective gate profile + autonomy band (§4.8.6) and a typed handoff envelope (§4.8.7 R3). A conformant Level-F engine could now *launch-gate* these verbatim. What the bundle still does not include is that **engine** — which is exactly the joint experiment §5 proposes.

---

## 4. Why the bundle is a significant *test* of the Greenwood article

Greenwood's central claim is that professional AI must **encode and verify the boundary between machine work and human judgment** — not sloganize "human in the loop." The 1.1 spec turns that claim into normative machinery. The bundle, dropped into a real second project (MikeOSS: a self-hostable, BYO-key, Supabase/Express legal assistant), is a rare chance to run that claim as an **end-to-end field experiment** instead of a reference architecture. Each Greenwood idea maps to a concrete, measurable test the bundle sets up:

| Greenwood idea | The test the bundle enables |
|---|---|
| **Encode the boundary; match gate strength to autonomy** | Implement `AnchoredAuthority` in MikeOSS with a declared `autonomy` band + R1/R4/R5 `gate_profile`, then measure whether anchored, budget-/depth-bounded loops actually suppress the failure the satire mocks (confident, ungrounded citation). This is the first time the escalation rule would be tested on real legal-research traffic, not in a spec. |
| **Structured deliverables; capability-gap honesty; decision trees** | `Assay.Citation.VerifyFirst`'s `verified / warning / not_found + fallback` is a direct instance of "cannot issue GREEN." The reproducible benchmark (`Assay.Benchmark.Reproducible`, "no score can exceed reality") tests at scale whether severity-flagged, honest output reduces harm vs. fluent prose — the *Mata v. Avianca* failure mode, measured. |
| **Attestation and audit; evidentiary handoff logs** | The bundle's `pathway-runs/` + `ASSET_PROVENANCE.yaml` + Ed25519 seal is a working test of "can a third party (opposing counsel, a judge, a regulator) **replay and verify** exactly how an answer was produced?" `Assay.Provenance.RunManifest` proposes the one-page schema any tool — including a Supabase-backed one — could emit to make that true. |
| **Living playbooks; cold-start refusal** | The bundle ships an Application Playbook but *not* a signed `practice_profile`. A MikeOSS adoption that adds one would test the spec's `BLOCKED_CONFIGURATION` cold-start gate: does refusing to run high-autonomy work until counsel has signed institutional rules actually prevent cold-start misuse? |
| **Privilege and destination (label ≠ control)** | The `identities/` 1-of-2 lockboxes test a privacy-preserving analog: participation is vouched-for and revealed by **key/destination control**, not by a cleartext label — exactly Greenwood's "privileged header is a label; destination is the control." |
| **Agent lane vs. lawyer lane; non-delegable acts** | Verify-first + "answer only from the anchor, else `not_found`" keeps the model in the *retrieval/comparison* lane and the *determination* in the human lane — a testable instance of the lane separation the spec formalizes as `non_delegable_acts`. |
| **Fork-and-disable; supply-chain visibility; signed scope-of-authority** | The bundle's de-identification + `Term` supersession (`anti-venom → assay`, `transmission → collaboration`) + `license_terms` (revocation `self_only`, attribution required) is a live instance of lineage-with-attribution. Two MikeOSS nodes forking the assay pathways — one stripping a gate — would test the spec's `register_removed` revision + "gates removed" visibility badge in the wild. |
| **Reflexive attestation (the meta-test)** | Greenwood asks for attestation and audit of professional AI work. The bundle applies it to *its own construction* (§2 above). If the self-provenance discipline holds for a deliverable this complex, it is strong evidence the same discipline can hold for a legal work product. |

The crucial framing: the bundle now demonstrates the **document-satisfiable half** of Greenwood's thesis (honest deliverable contracts, attestation, self-provenance, conformance binding) **and fully specifies** the runtime-enforced half (autonomy-banded `gate_profile`s, a cold-start practice profile, an attested-run record, a typed handoff envelope) — but deliberately does not build the **engine** that enforces them (ToolGateway, HandoffBus, launch-gate execution). A MikeOSS implementation is therefore not a nice-to-have; it is the **only way to actually test** whether Greenwood's harder registers (R2/R3/R5/R6) survive contact with a real product and real legal tasks. The bundle's value is that it makes that test cheap to start: the substrates, the conformance target (1.1.0, by signature), the honest deliverable contracts, the **enforceable gate profiles**, and the audit ledger are already supplied.

---

## 5. Hardening applied (2026-05-29) — what was done, what remains

The three edits below were applied as a single provenanced step — pathway `Collaboration.Refactor.HardenGateProfile@v1`, recorded in `pathway-runs/` and re-sealed (`verify: OK`) — moving the package from "designs toward" to **carrying** the §4.8 surface:

1. **Bands + profiles declared.** `Assay.Citation.VerifyFirst` → `A0` (R1); `Assay.Convergence.AnchoredAuthority` → `A1` with R1 + R4 + R5 + R6 and `escalation_rule: strict`. Both are now launch-gateable by any Level-F engine.
2. **Practice profile added** (`assay-pathways/practice-profiles/legal-research-grounding.v1.yaml`, R1 cold-start) — DID-signed stub with escalation thresholds and forkable anti-pattern annotations, so the cold-start gate resolves rather than `BLOCKED_CONFIGURATION`.
3. **`RunManifest` promoted** to the §4.8.6 attested-run record (persists `autonomy` + `effective_gate_profile` + practice-profile revision hash) and given a §4.8.7 R3 `handoff_envelope_schema` a `HandoffBus` could validate.

None of these added an engine; they make the bundle a *complete 1.1 specification of intent* that any Level-F runtime (a future MikeOSS node included) can enforce verbatim. **What remains** — and is the actual experiment — is standing up that runtime: a ToolGateway/HandoffBus that reads these manifests and refuses launches that under-gate.

---

*Bottom line: the bundle uses Appendix C self-provenance, binds itself to 1.1.0 by signature, and — as of the 2026-05-29 hardening — now **carries** Greenwood's authority-boundary **policy** as enforceable §4.8 gate profiles, a cold-start practice profile, and an attested-run record, while leaving the runtime **enforcement** as the proposed joint experiment. That gap is the point: it is exactly the part of Greenwood's thesis that has never been tested end-to-end in a shipping legal-AI product, and the bundle is engineered to make MikeOSS the place it finally is.*
