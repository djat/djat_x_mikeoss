# Pathways Reference Implementation Specification

**Document type:** Reference Implementation Specification (RIS)
**Status:** Normative specification
**Audience:** Independent implementers, conformance testers, marketplace participants, federation peers
**Spec version:** **1.1.0** — *Authority Boundaries* revision (2026-05-20)
**Previous revision:** 1.0.0 — initial publication
**This revision introduces:** [§4.8 Autonomy Bands and Gate Profiles](#48-autonomy-bands-and-gate-profiles-normative), [§13.7 Gate-profile conformance tests](#137-gate-profile-conformance-tests), glossary entries for *autonomy band*, *register*, *gate profile*, *ToolGateway*, *HandoffBus*, *practice profile*, *non-delegable act*, and a new [Appendix C — Spec Self-Provenance and Meta-Pathways](#appendix-c--spec-self-provenance-and-meta-pathways) that encodes the origin and provenance of this revision itself as Pathways and PathwayRuns.
**Compatibility:** 1.1.0 is **backward-compatible** with 1.0.0 for Level M/S implementations. Level F and Level R implementations declaring conformance to spec ≥ 1.1.0 **MUST** satisfy the additional gate-profile tests in §13.7 for autonomy bands they support.

**Scope:** This document is the **complete normative specification** for an independent implementation of the Pathways agentic-orchestration system. Together with the six prior strategy reports, it provides everything needed to:

1. Build a conformant implementation **from the ground up**, in any language, on any deployment substrate.
2. Author a **single narrative application playbook** that simultaneously documents the UX and serves as a deterministic build spec.
3. Use **narrative domain-bounded pointers** to deterministically resolve narrative references to actual code in the canonical implementation, while gracefully degrading to descriptive prose in other implementations.
4. Generate a **genesis attestation** upon proving conformance, which serves as the implementer's network identity and as proof of ability to send and receive **trusted peering invitations**.
5. Cluster multiple builds under one identity (per-user genesis seed; per-build genesis seed) so an implementer can run production / staging / personal / shared deployments as distinct-but-linked instances.
6. Participate in the **organic emergent collaborative pathway exchange** — the federation marketplace built on top of trusted peering.

The user is encouraged not to recreate the canonical implementation exactly; the architecture's extreme attribution, precise ownership, and explicit-rights model **expects and rewards variation**.

**Companion documents** (the conceptual material this spec assumes):

| # | Doc | What it establishes |
|---|---|---|
| 1 | [`PATHWAYS_ARCHITECTURE.md`](PATHWAYS_ARCHITECTURE.md) | Engine reference (the canonical implementation) |
| 2 | [`PATHWAYS_CONVERSION_REPORT.md`](PATHWAYS_CONVERSION_REPORT.md) | Bespoke flows → pathway conversion |
| 3 | [`PATHWAYS_UX_AS_PATHWAYS_REPORT.md`](PATHWAYS_UX_AS_PATHWAYS_REPORT.md) | UX as pathways |
| 4 | [`PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT.md`](PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT.md) | Skills + namespaces + fuzzy discovery |
| 5 | [`PATHWAYS_NARRATIVE_KEYWORDS_PATTERNS_REPORT.md`](PATHWAYS_NARRATIVE_KEYWORDS_PATTERNS_REPORT.md) | Language layer + Mechanism Institute |
| 6 | [`PATHWAYS_AGENTIC_DSL_REPORT.md`](PATHWAYS_AGENTIC_DSL_REPORT.md) | The whole system as an agentic orchestration DSL |

This document (the seventh) **closes the series** as the formal spec.

---

## Table of Contents

1. [Document Conventions and Conformance Keywords](#1-document-conventions-and-conformance-keywords)
2. [Conformance Levels](#2-conformance-levels)
3. [Implementation Substrate Requirements](#3-implementation-substrate-requirements)
4. [The DSL Specification — Normative Grammar](#4-the-dsl-specification--normative-grammar)
5. [The Application Playbook Format](#5-the-application-playbook-format)
6. [Narrative Domain-Bounded Pointers](#6-narrative-domain-bounded-pointers)
7. [Source Anchoring & Graceful Degradation](#7-source-anchoring--graceful-degradation)
8. [Build-Order Requirements](#8-build-order-requirements)
9. [Genesis Attestation & Build Seeds](#9-genesis-attestation--build-seeds)
10. [Trusted Peering Protocol](#10-trusted-peering-protocol)
11. [Collaborative Pathway Exchange](#11-collaborative-pathway-exchange)
12. [Attribution, Rights, and the Variation-Encouraged Doctrine](#12-attribution-rights-and-the-variation-encouraged-doctrine)
13. [Conformance Testing](#13-conformance-testing)
14. [Example Book Chapter (Illustrative)](#14-example-book-chapter-illustrative)
15. [Risks, Trade-offs, Open Questions](#15-risks-trade-offs-open-questions)
16. [Glossary](#16-glossary)
17. [Appendix A — Required Cryptographic Primitives](#appendix-a--required-cryptographic-primitives)
18. [Appendix B — JSON Schemas](#appendix-b--json-schemas)
19. [Appendix C — Spec Self-Provenance and Meta-Pathways](#appendix-c--spec-self-provenance-and-meta-pathways)

**Sub-sections added in 1.1.0:**

- [4.8 Autonomy Bands and Gate Profiles](#48-autonomy-bands-and-gate-profiles-normative)
- [13.7 Gate-profile conformance tests](#137-gate-profile-conformance-tests)

---

## 1. Document Conventions and Conformance Keywords

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in **RFC 2119** and **RFC 8174** when, and only when, they appear in all capitals.

When the spec refers to **"the canonical implementation"**, it means the codebase at the time of this writing under `legal-services-crew/`. References to canonical-implementation-specific files (paths, class names, table names) are **illustrative**, not normative — independent implementations MAY use any naming, language, or storage choices that satisfy the contract.

When the spec refers to **"the network"**, it means the federated graph of conformant implementations connected by trusted peering relationships ([§10](#10-trusted-peering-protocol)).

---

## 2. Conformance Levels

An implementation declares its conformance level in its **build manifest** ([§9.2](#92-the-build-manifest)). Higher levels include all lower-level requirements.

### 2.1 Level M — Minimum

A Level-M implementation **MUST**:

- Implement the DSL grammar ([§4](#4-the-dsl-specification--normative-grammar)) for: identity triples, ordered linear steps, the `prompt` agent (templated LLM call), the `pathway` agent (sub-pathway invocation).
- Persist `Pathway` template rows and `PathwayRun` rows in any durable store.
- Run pathway templates linearly, producing per-step outputs and a final output.
- Pass the **Level-M conformance test suite** ([§13.1](#131-level-m-conformance-tests)).

A Level-M implementation **MAY**:

- Skip everything below.

A Level-M implementation **MUST NOT**:

- Claim Level-S, Level-F, or Level-R conformance.
- Generate a network-valid genesis attestation (Level M is local-only).

**Use case**: Solo developer prototype, learning implementation, embedded use.

### 2.2 Level S — Standard

A Level-S implementation **MUST** (in addition to Level-M):

- Implement the registry with at minimum the four kinds: `composite_domain`, `context_lens`, `abstract_capability`, `agent_role`.
- Implement `pathway_domain_affiliation` with the four required `source` values: `USER`, `INFERRED_FROM_AGENTS`, `INFERRED_FROM_QUERY`, `INFERRED_FROM_RAG`.
- Implement at least the analytical agents enumerated in [§4.4 Required Agent Set](#44-required-agent-set).
- Persist `PathwayStepExecution` rows with model identifiers, durations, prompts.
- Persist `ProvenanceRecord` rows linked to step executions.
- Implement sub-pathway invocation via the `pathway` agent with cycle detection and depth limits.
- Implement the structured `result_json` artifact channel.
- Implement at least one of the four DSL surface syntaxes ([PATHWAYS_AGENTIC_DSL_REPORT §9](PATHWAYS_AGENTIC_DSL_REPORT.md#9-dsl-surface-syntaxes--four-equivalent-forms)) (YAML, JSON, structured-prompt, or prose-narrative).
- Pass the **Level-S conformance test suite** ([§13.2](#132-level-s-conformance-tests)).

**Use case**: Small-team or single-tenant deployment.

### 2.3 Level F — Full

A Level-F implementation **MUST** (in addition to Level-S):

- Implement the **AquaTree integration** for templates and runs, with verifier-portable export.
- Implement the **`external_name` registry kind** + at least four slug grammars (`tm:`, `model:`, `api:`, `did:`) from [PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT §5.2](PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT.md#52-the-slug-grammar).
- Implement **all six discovery dimensions** (symbolic, semantic, physical, contextual, temporal, lineage) per [PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT §6](PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT.md#6-deep-linking-dimensions).
- Implement the **strict / loose / tunable** discovery mode dial.
- Implement at minimum **two** of the four DSL surface syntaxes.
- Implement the **`pathway_narrative_annotation` table** for at least the `scenario` and `why` annotation kinds.
- Implement the **`keyword_index`** with reserved-keyword seed.
- Implement the **`pattern_template`** table with at least the workflow patterns (Pipeline, FanOut, FanIn).
- Implement the **trusted peering protocol** ([§10](#10-trusted-peering-protocol)) with at least the `invite`, `accept`, `revoke`, `verify` operations.
- Generate a **genesis attestation** that other Level-F+ implementations can verify.
- Pass the **Level-F conformance test suite** ([§13.3](#133-level-f-conformance-tests)).

**Use case**: Multi-tenant deployment, marketplace participant, federation peer.

### 2.4 Level R — Reference

A Level-R implementation **MUST** (in addition to Level-F):

- Implement the **complete 10-slot typology** ([PATHWAYS_AGENTIC_DSL_REPORT §3](PATHWAYS_AGENTIC_DSL_REPORT.md#3-the-extended-typology--10-typed-slots)) with all seven new `RegistryDomainNodeKind` values.
- Implement **holonic nesting** — `inherits_from` resolution, `derived_attributes` computation, exposed-signal collection.
- Implement **all four DSL surface syntaxes** with round-trip serialization.
- Implement **single-prompt UX/app instantiation** ([PATHWAYS_AGENTIC_DSL_REPORT §6](PATHWAYS_AGENTIC_DSL_REPORT.md#6-single-prompt-ux--application-generation)).
- Implement the **innovation-analytics pathway template family** ([PATHWAYS_AGENTIC_DSL_REPORT §8](PATHWAYS_AGENTIC_DSL_REPORT.md#8-innovation-analytics-across-the-pathway-network)).
- Implement **per-tenant curated grammars** with shadow-with-rationale overrides ([PATHWAYS_NARRATIVE_KEYWORDS_PATTERNS_REPORT §5.3](PATHWAYS_NARRATIVE_KEYWORDS_PATTERNS_REPORT.md#53-the-shadow-with-rationale-rule)).
- Implement **all eight invitation/peering/exchange flows** described in [§10–11](#10-trusted-peering-protocol).
- Pass the **Level-R conformance test suite** ([§13.4](#134-level-r-conformance-tests)).

**Use case**: The canonical reference implementation, marketplace hub, network-prominent participant.

### 2.5 Conformance level summary

| Level | Local-only? | Can peer? | Marketplace? | Required surface syntaxes | Required agent set |
|---|---|---|---|---|---|
| M | yes | no | no | none required | `prompt`, `pathway` |
| S | yes (multi-tenant capable) | no | local-only | 1 of 4 | analytical core (~10) |
| F | no (federation-ready) | yes | yes | 2 of 4 | analytical core + `pattern_invoke` + observers |
| R | no (federation-prominent) | yes | yes | 4 of 4 (round-trip) | full registry (20+) |

---

## 3. Implementation Substrate Requirements

The spec is intentionally substrate-agnostic. An implementation MAY use any:

- **Language** — Python, TypeScript, Rust, Go, JVM, Erlang, etc.
- **Storage** — Postgres, SQLite, DuckDB, distributed KV, file-system, IPFS, etc.
- **Compute** — single-process, async runtime, queue+worker, serverless, K8s, etc.
- **Frontend** — React, Vue, Svelte, native mobile, terminal, voice, headless, etc.
- **LLM provider routing** — direct API, proxy, local model, ensemble, etc.
- **Cryptographic library** — any library satisfying [Appendix A](#appendix-a--required-cryptographic-primitives).

The implementation **MUST** document its substrate choices in the **build manifest** ([§9.2](#92-the-build-manifest)) so peers can understand interoperability constraints.

The implementation **SHOULD** prefer mature, well-supported libraries for cryptographic operations. The implementation **MUST NOT** roll its own cryptographic primitives.

---

## 4. The DSL Specification — Normative Grammar

This section is the **normative grammar** for the pathway template — the central artifact of the DSL. Implementations MUST accept and emit templates that conform to this grammar.

### 4.1 Identity triple

A template **MUST** have a unique `(domain, subdomain, action, version)` identity:

```text
<identity>     ::= <domain> "." <subdomain> "." <action> "@v" <version>
<domain>       ::= PascalCase IDENT             ; e.g. Document, Knowledge
<subdomain>    ::= PascalCase IDENT             ; e.g. Knowledge, Search
<action>       ::= PascalCase IDENT ( "." PascalCase IDENT )*  ; e.g. QA, Search.WithinDocument
<version>      ::= POSITIVE_INTEGER             ; monotonic per (domain, subdomain, action)
```

The implementation **MUST** enforce uniqueness on `(domain, subdomain, action, version)`. The implementation **SHOULD** allow multiple versions of the same triple to coexist (immutable history).

### 4.2 Template structure

A template **MUST** have:

```yaml
domain: str           # required
subdomain: str        # required
action: str           # required
version: int          # required, default=1
display_name: str     # required
description: str?     # optional
steps: List[PathwayStep]   # required, at least 1 step
input_contract: PathwayContract?   # optional but RECOMMENDED
output_contract: PathwayContract?  # optional but RECOMMENDED
default_config: dict?
```

A template **SHOULD** have:

```yaml
license_terms: PathwayLicenseTerms?
parent_pathway_id: str?      # fork lineage
is_public: bool = false
is_system: bool = false
tags: List[str]?
```

A template **MAY** have additional fields not specified here; conformant implementations **MUST** preserve unknown fields on round-trip serialization.

### 4.3 Step structure

```yaml
agent_id: str                    # required; resolves to a registered agent
order: int                       # required, 1-based
skill: str                       # optional; default "default"
config: dict                     # agent-specific
input_prompt: str?
llm_system_prompt: str?
llm_user_prompt_template: str?   # supports {{var}} substitution
inputs: List[str]?               # multi-input fan-in references
parallel: str?                   # parallel-group label (Level-S+)
output_schema: dict?             # JSON Schema (Level-S+)
```

### 4.4 Required agent set

| Conformance level | Required agents |
|---|---|
| M | `prompt`, `pathway` |
| S | + `analysis`, `extraction`, `summary`, `search`, `verification`, `reporting`, `derivative`, `fusion`, `comparison` |
| F | + `pattern_invoke`, `narrative_resolve`, `ui_listen` (observer mode), `ui_render` (observer mode) |
| R | + the full 20+ agents from [PATHWAYS_ARCHITECTURE §5.1](PATHWAYS_ARCHITECTURE.md#51-registry-table), the new agents from prior reports (`skill_promote`, `skill_enhance`, `composer`, `app_version_check`, `narrative_test`, `keyword_curate`, `pattern_invoke`, `template_draft`) |

### 4.5 Run structure

A pathway run **MUST** carry:

```yaml
id: str
pathway_id: str
status: enum {PENDING, RUNNING, COMPLETED, FAILED, CANCELLED}
current_step: int
total_steps: int
step_executions: List[PathwayStepExecution]
created_at, completed_at: datetime
final_output: str?
```

Higher levels add sub-run linkage (`parent_run_id`), session linkage (`session_id`), goal linkage (`goal_id`), AquaTree binding (`aqua_tree_id`), and others per [PATHWAYS_ARCHITECTURE §4.4](PATHWAYS_ARCHITECTURE.md#44-the-pathwayrun).

### 4.6 The execution contract

The implementation's executor **MUST**:

1. Iterate `pathway_run.steps` in order.
2. Resolve each step's `agent_id` to a callable.
3. Invoke the agent with the step's inputs (per the templating rules in [PATHWAYS_ARCHITECTURE §7](PATHWAYS_ARCHITECTURE.md#7-inter-step-state-artifacts-and-templating)).
4. Persist the result on `_step_outputs[order]` and (if structured) `_step_artifacts[order]`.
5. Carry `current_content` forward as the implicit "previous step's output" bus.
6. Persist a per-step record (Level-S+ persists `ProvenanceRecord`).
7. Update run status; emit progress events on a defined channel.
8. On completion, persist the final output and run-level metadata.

The implementation **SHOULD** support cancellation between steps. The implementation **MUST NOT** mutate persisted step rows after they reach a terminal status.

### 4.7 Template round-trip

A Level-F+ implementation **MUST** support round-trip serialization between at least two of the four DSL surface syntaxes (YAML, JSON, structured-prompt, prose-narrative) such that:

```text
template == parse( serialize( template ) )
```

for all fields the chosen surface supports. Lossy fields (e.g. structural details lost in prose) **MUST** be preserved through a sidecar metadata channel.

### 4.8 Autonomy Bands and Gate Profiles (normative)

> **Origin and motivation:** This subsection was introduced in spec version 1.1.0 in response to *Authority Boundaries for AI* (Greenwood, 2026-05-20), which identifies the central engineering pattern of **matching gate strength to autonomy** across three (or six) registers. The end-to-end provenance of the revision is encoded in [Appendix C](#appendix-c--spec-self-provenance-and-meta-pathways).

The purpose of this subsection is to make the **escalation rule** — *the more autonomous the action, the harder the gate must be* — a deterministic property of the engine rather than a property of authoring discipline.

#### 4.8.1 Autonomy bands

Every `PathwayRun` **MUST** carry an `autonomy` field whose value is one of four bands. Templates **MAY** declare a `default_autonomy`; launch requests **MAY** override down (toward higher supervision) but **MUST NOT** override up beyond `max_autonomy` declared by the template.

| Band | Name | Operating assumption | Examples |
|---|---|---|---|
| **A0** | Assisted | A licensed human reads every output before any external effect | Chat-style document QA, draft review, conversational legal triage |
| **A1** | Supervised async | A human approves before each commit / external action; outputs may queue | Pre-launch review interstitials, foreach-row human gates, draft-only outbound |
| **A2** | Scheduled / headless | No human in the loop during execution; results reviewed later | Renewal watchers, docket watchers, regulatory feed monitors |
| **A3** | Cross-boundary | A2 plus inputs / handoffs cross trust boundaries (sub-runs, peers, hostile upstream) | Diligence-grid agents reading counterparty documents; peer-fetched templates; multi-agent pipelines |

Implementations **MUST** reject runs whose `autonomy` value is not in this enum.

#### 4.8.2 Registers

Pathways recognizes **six registers** of restraint. Each register has a normative contract and a set of fields on the `gate_profile`.

| Register | Concern | Enforcement locus |
|---|---|---|
| **R1 — Prompt-and-workflow** | Normative instructions, refusal-when-unconfigured, deliverable contract (review/verify discipline, decision tree, capability-gap honesty), recoverable-error bias | Templates, output contracts, practice profile, application playbook |
| **R2 — Capability** | Per-step / per-agent tool grants; a model cannot invoke a tool it was never given | `ToolGateway` ([§4.8.7](#487-the-toolgateway-and-handoffbus-contracts)) |
| **R3 — Code at seams** | Closed-intent allowlist, JSONSchema-validated parameters, template-rendered downstream prompts, append-only handoff audit | `HandoffBus` ([§4.8.7](#487-the-toolgateway-and-handoffbus-contracts)) |
| **R4 — Economic** | Hard per-run budget (USD and/or tokens); halt before overspend | `ToolGateway` + runner |
| **R5 — Temporal** | External halt switch checked before every tool call; idle TTL; auto-pause | Runner liveness check |
| **R6 — Contextual** | Tool access modulated by workflow **phase**; deny-wins intersection of phase profile and step profile | Executor pre-step composition |

Implementations **MUST** treat the register set as **extensible-but-stable**: register IDs `R1`–`R6` are reserved by this spec and **MUST NOT** be reused; implementation-specific extensions **MUST** use IDs `R100`+ and **MUST NOT** weaken any reserved register's contract.

#### 4.8.3 The escalation rule (engine law)

Given a run with autonomy `A`, the engine **MUST** refuse to launch unless the run's effective `gate_profile` satisfies the **minimum register set** for that band:

| Autonomy | Minimum required registers |
|---|---|
| **A0** | R1 |
| **A1** | R1 + R6 (`human_gate` on at least the commit/external-action steps) |
| **A2** | R1 + **R2** + **R3** (any seam crossing process boundaries) + **R4** + **R5** |
| **A3** | R1 + R2 + R3 (heavy: applied to every sub-run launch, external action, and peer fetch) + R4 + R5 + R6 |

The check **MUST** run at the **launch** choke point ([§4.8.6](#486-the-three-enforcement-choke-points)). Run startup **MUST NOT** proceed past the launch gate when minimums are unmet. The engine's response **MUST** include a structured `gate_profile_violation` payload naming the missing registers and the offending steps.

#### 4.8.4 The `gate_profile` manifest

Templates **SHOULD**, and Level-F+ implementations operating at autonomy ≥ A2 **MUST**, carry a `gate_profile` block. Runs **MUST** persist the resolved (effective) `gate_profile` they were launched with on the `PathwayRun` row.

```yaml
gate_profile:
  spec_version: "1.1.0"
  default_autonomy: A1            # A0 | A1 | A2 | A3
  max_autonomy: A2                # cap; launch requests cannot exceed
  escalation_rule: strict         # strict | warn | audit-only

  registers:
    R1:
      enabled: true
      practice_profile_ref: "did:key:z6Mk.../playbook/ca-alter-ego@v2"  # see §4.8.5
      output_contract_profile: "legal.deliverable.v1"
      recoverable_error_bias: true
    R2:
      enabled: false              # auto-enabled when effective_autonomy >= A2
      default_capability_profile:
        allow_tools: []
        deny_tools: ["*"]
    R3:
      enabled: false              # auto-enabled at seams when effective_autonomy >= A1
      handoff_schema: "legal.handoff.v1"
      allowed_targets: ["subrun:Legal.*", "channel:slack/legal-ops"]
    R4:
      enabled: false              # auto-enabled at A2+
      max_usd: 5.00
      max_tokens: 200000
    R5:
      enabled: false              # auto-enabled at A2+
      halt_channel: "run/{run_id}/halt"
      idle_ttl_seconds: 300
    R6:
      enabled: false              # auto-enabled where phases are declared
      phases: [intake, analysis, ethics_gate, delivery]
      phase_defaults:
        ethics_gate:
          allow_tools: [read_document]
          deny_tools: ["*"]
          human_gate: required

  non_delegable_acts:
    - sign
    - file
    - send_external
    - negotiate_bind
    - certify

  attestation:
    signed_by: "did:key:z6Mk..."
    signed_at: "2026-05-20T20:00:00Z"
    signature: <bytes>
```

Field semantics:

- `escalation_rule = strict` (RECOMMENDED for legal / regulated profiles): the engine **MUST** refuse launches that under-gate.
- `escalation_rule = warn`: launches proceed but the run carries a `gate_profile_warning` provenance record.
- `escalation_rule = audit-only`: launches proceed silently but a waiver record is appended to the run's AquaTree; **MUST NOT** be used by Level-R legal implementations.
- `non_delegable_acts`: a registry of named acts the engine **MUST NOT** perform autonomously. Steps performing such an act **MUST** declare `human_gate: required` and **MUST** record a human approval entry in provenance before completion.

#### 4.8.5 Practice profile (R1 cold-start)

A **practice profile** is a tenant-scoped document that encodes institutional rules, escalation thresholds, jurisdictional posture, and named anti-patterns. It is the Pathways analog to the article's `CLAUDE.md` practice file.

Requirements:

1. A practice profile **MUST** be a Pathways-addressable artifact: a registry node of kind `practice_profile` (Level-F+) with `slug`, `version`, and an Aqua-attested revision history.
2. A practice profile **MUST** be signed by an authorized DID (e.g., the firm's supervising counsel) per [Appendix A](#appendix-a--required-cryptographic-primitives).
3. A `gate_profile.R1.practice_profile_ref` field **MUST** be a `did:key:` or `did:web:` URI plus a fragment naming the profile slug and version.
4. The engine **MUST** apply a **cold-start gate**: if a template's `gate_profile.R1.enabled = true` and no matching practice profile resolves locally or via trusted peering, the run **MUST NOT** start; status flips to `BLOCKED_CONFIGURATION` with a structured reason naming the missing profile.
5. Practice profile edits are themselves Aqua revisions; downstream runs **MUST** record the effective profile revision hash in provenance so audits can replay "which profile shaped this work."

A practice profile **MAY** include forkable anti-pattern annotations (e.g., *"ownership alone is not dispositive under CA alter ego"*); these annotations are referenced from templates via narrative pointers ([§6](#6-narrative-domain-bounded-pointers)).

#### 4.8.6 The three enforcement choke points

Conformant runtimes **MUST** enforce gate profiles at exactly three locations:

```text
+----------+        +----------+        +----------+
|  LAUNCH  |  -->   |  PRE-    |  -->   |  SEAM    |
|  gate    |        |  STEP /  |        |  gate    |
|          |        |  PRE-    |        |          |
|          |        |  TOOL    |        |          |
|          |        |  gate    |        |          |
+----------+        +----------+        +----------+
   R1 cold-start      R2 capability       R3 HandoffBus
   gate_profile       R4 budget           audit append
   manifest valid     R5 halt liveness    targets/intent
   autonomy band      R6 phase profile    allowlist
```

| Choke point | Registers enforced | Reject behavior |
|---|---|---|
| **Launch** | R1 manifest + autonomy minimums + cold-start | Run status `REJECTED_GATE_PROFILE` or `BLOCKED_CONFIGURATION` |
| **Pre-step / pre-tool** | R2 (`ToolGateway`), R4 (budget), R5 (halt), R6 (phase) | Step status `BLOCKED_GATE`; structured reason; run continues only if `escalation_rule != strict` AND the gate explicitly allows soft-fail |
| **Seam** | R3 (`HandoffBus`) — every sub-run launch, every external action, every peer fetch | Handoff record `rejected` or `neutralized`; append to `handoff_audit`; downstream **MUST NOT** see the original free-text as steering |

The existing inter-step Context Agent checkpoint ([`PATHWAYS_ARCHITECTURE.md §6.4`](PATHWAYS_ARCHITECTURE.md#64-inter-step-context-agent-checkpoint)) is **advisory** and **MUST NOT** be relied on as the sole halt mechanism for autonomy ≥ A2. Register R5 (deterministic halt) is required separately.

#### 4.8.7 The `ToolGateway` and `HandoffBus` contracts

##### ToolGateway (R2 + R4 + R5 + R6)

A conformant implementation **MUST** route every agent tool / MCP invocation through a single gateway component. The gateway:

1. Resolves the effective capability profile for the current step: `phase_defaults[phase]` ∩ `step.capability_profile` (deny-wins).
2. Rejects calls to tools not in `allow_tools` or matching `deny_tools` patterns.
3. Decrements the run's `R4` budget; if budget would go negative, returns `BUDGET_EXCEEDED` and the runner halts.
4. Checks `R5` liveness (the halt channel); if halted, returns `RUN_HALTED`.
5. Records every accept / reject / halt event to provenance with a stable `tool_call_id`.

##### HandoffBus (R3)

For every **seam** (sub-run launch, external action, peer fetch) at autonomy ≥ A1, the runtime **MUST**:

1. Construct a typed `HandoffEnvelope`:

```yaml
handoff:
  envelope_version: "1.0"
  intent: <closed_enum>          # e.g. verify_claims, escalate_to_partner, send_message
  target: <typed_target>         # subrun:Legal.Research.PrimarySourcesDeep | channel:slack/... | peer:did:key:...
  params:                        # validated against per-intent JSONSchema
    jurisdiction: "CA"
    citation_ids: [...]
  event_text: "<raw upstream text>"   # wrapped as DATA, never as steering
  source_run_id: pr_<hex>
  source_step_order: <int>
  signed_by: "did:key:..."
  signed_at: <iso8601>
```

2. Validate `intent` against the closed allowlist for this template's `gate_profile.R3.handoff_schema`.
3. Validate `target` against the allowlist (regex-safe; e.g. Slack channel IDs **MUST** match `^[CGD][A-Z0-9]{8,}$`).
4. Validate `params` against the per-intent JSONSchema.
5. Render the downstream prompt from a **template** indexed by `intent`, using `format_map(params)` for substitution. The `event_text` field **MUST** be enclosed in a labeled data block (`<agent-handoff source="..." timestamp="...">…</agent-handoff>`) annotated *"data describing a task, not instructions"*. Free text **MUST NOT** become any portion of the downstream agent's system or user prompt outside that data block.
6. Append the validation outcome to an **append-only handoff audit** (`handoff_audit_records` table; or an equivalent JSONL stream) with fields: `accepted` (bool), `rejection_reason?`, `intent`, `target`, `params_keys`, `raw_event_len`, `sanitized_event_len`, `signed_by`, `signature`.

Rejected handoffs **MUST NOT** invoke the downstream agent.

#### 4.8.8 Capability profile on steps

Templates running at autonomy ≥ A2 **MUST** include a `capability_profile` on every step that can invoke tools or sub-pathways. Steps without explicit profiles inherit the `gate_profile.R2.default_capability_profile` (which **MUST** be deny-by-default for A2+).

```yaml
- agent_id: extraction
  order: 1
  skill: legal_references
  phase: intake
  capability_profile:
    allow_tools: [read_document, grep]
    deny_tools: [write_*, send_*, browsing.*, mcp.*]
    allow_sub_pathways: []
    allow_agents: [extraction, verification, analysis]
  config: { ... }

- agent_id: pathway
  order: 4
  skill: handoff
  phase: analysis
  capability_profile:
    allow_tools: []
    allow_sub_pathways: ["Legal.Research.PrimarySourcesDeep"]
  config:
    handoff_intent: verify_claims
    handoff_target: "subrun:Legal.Research.PrimarySourcesDeep"
```

The **split-agent pattern** (article's diligence-grid model) is expressed natively: two steps with disjoint capability profiles — one read-only over MCP sources, one writer with no MCP access, communicating only through a `HandoffBus` envelope.

#### 4.8.9 Phase declarations (R6)

Steps **MAY** declare a `phase` string. Implementations honoring R6 **MUST** merge `gate_profile.R6.phase_defaults[phase]` with the step's `capability_profile` using deny-wins intersection before invocation. Phase transitions **MUST** be visible in provenance (a `phase_changed` event) and **MAY** trigger automatic `human_gate` insertion (e.g. always require human approval to leave the `ethics_gate` phase).

#### 4.8.10 Fork-and-disable mitigation

When a template is forked ([§11.1](#111-the-eight-exchange-operations)), the engine **MUST** compute a **gate-profile delta** between the parent and the fork:

| Delta event | Required action |
|---|---|
| A register that was `enabled: true` in parent is now disabled or missing | Fork **MUST** record an explicit `register_removed` revision in its AquaTree with a `rationale` field |
| `non_delegable_acts` removed or downgraded | Same as above; **MUST NOT** be silent |
| Practice profile reference removed | Fork **MUST NOT** claim the same legal-domain affiliations as the parent (registry affiliation `source` cannot remain `INFERRED_FROM_AGENTS` of the parent) |

Marketplace consumers viewing a fork **MUST** see a structured "gates removed" badge derived from this delta. This does not prevent gate stripping (Apache-2.0 license remains permissive) but makes stripping **visible** and **attestable**, addressing the article's fork-and-disable concern.

#### 4.8.11 Conformance level introduction

| Feature | Introduced at level |
|---|---|
| `autonomy` field on `PathwayRun`; reject unknown values | **S** (1.1.0+) |
| `gate_profile` manifest on templates (R1 required) | **S** (1.1.0+) |
| Launch-gate enforcement of autonomy minimums | **S** (1.1.0+) for A0/A1; **F** for A2; **R** for A3 |
| `ToolGateway` (R2/R4/R5) | **F** (1.1.0+) |
| Practice profile (R1 cold-start) as Aqua-attested registry node | **F** (1.1.0+) |
| `HandoffBus` (R3) at every seam | **F** for A1/A2; **R** for A3 |
| Phase-modulated permissions (R6) | **F** (1.1.0+) when phases are declared |
| Fork-and-disable delta visibility | **F** (1.1.0+) |
| Per-tenant `non_delegable_acts` registry and engine enforcement | **R** (1.1.0+) |

A Level-F implementation operating at autonomy A2 without a `ToolGateway` is **non-conformant** to spec 1.1.0 even if it passes all 1.0.0 tests.

---

## 5. The Application Playbook Format

The **application playbook** is the primary deliverable of an implementation effort: a single narrative document that doubles as a deterministic build spec. Reading the playbook = consuming the spec; following the playbook = building the system.

### 5.1 Book structure

A book **MUST** consist of ordered **chapters**. Each chapter **MUST** declare its **mode**:

```yaml
chapter:
  number: 1
  title: str
  mode: enum {NARRATIVE, NORMATIVE, EXAMPLE, GLOSSARY, APPENDIX}
  prerequisites: List[chapter_number]   # build-order dependencies
  conformance_level: enum {M, S, F, R}  # the minimum level this chapter requires
  body: <markdown with embedded pointers>
```

| Mode | What it provides | Compiled by |
|---|---|---|
| `NARRATIVE` | Prose walkthrough of UX / behavior; readable as a story | `narrative_resolve` agent → draft templates |
| `NORMATIVE` | MUST/SHOULD requirements with conformance test references | Compliance checker |
| `EXAMPLE` | Worked example chapter showing patterns in action | Used as conformance-test fixture |
| `GLOSSARY` | Term definitions referenced elsewhere | Lookup target |
| `APPENDIX` | Schemas, formal grammar fragments, reference data | Schema validator |

### 5.2 Required book chapters (Level-S+)

A Level-S book **MUST** include at minimum:

| # | Title | Mode | Purpose |
|---|---|---|---|
| 1 | "Identity, Conformance, Substrates" | NORMATIVE | Declares the impl's identity, conformance level, substrate choices |
| 2 | "The Substrate" | NORMATIVE | Storage, compute, executor design |
| 3 | "The Pathway DSL" | NORMATIVE | Template grammar implementation |
| 4 | "The Required Agents" | NORMATIVE | Each required agent's contract + skill set |
| 5 | "Onboarding the User" | NARRATIVE + EXAMPLE | The first-touch UX flow walked through with pointers |
| 6 | "Analyzing a Document" | NARRATIVE + EXAMPLE | The document-detail flow walked through with pointers |
| 7 | "Authoring a Pathway" | NARRATIVE + EXAMPLE | The pathway-builder flow |
| 8 | "Conformance Tests" | NORMATIVE | Tests this implementation passes |
| 9 | "Glossary" | GLOSSARY | Terms |
| 10 | "Schemas" | APPENDIX | JSON schemas for templates, runs, registry rows |

A Level-F book **MUST** additionally include:

| # | Title | Mode | Purpose |
|---|---|---|---|
| 11 | "Identity & Genesis" | NORMATIVE | Per-user DID + per-build genesis-seed implementation |
| 12 | "Trusted Peering" | NORMATIVE | Peering protocol implementation |
| 13 | "Collaborative Exchange" | NARRATIVE + EXAMPLE | Marketplace flows |
| 14 | "Aqua Attestation" | NORMATIVE | AquaTree integration |

A Level-R book **MUST** additionally include the full 10-slot typology coverage, narrative tests, single-prompt instantiation examples, and innovation-analytics surface chapters.

### 5.3 Reading order vs build order

The book's chapter order is the **reading order** (story-shaped). The `prerequisites` field declares the **build order** (DAG-shaped). The two MAY differ — readers can follow the story while implementers can topologically-sort prerequisites.

### 5.4 Book attestation

A Level-F+ book **MUST** be Aqua-attested. Each chapter is a leaf in the book's AquaTree; the root is signed by the book author's DID. Forks of the book preserve the AquaTree lineage to the upstream book.

---

## 6. Narrative Domain-Bounded Pointers

This section specifies the **narrative pointer mechanism** — the device that lets prose narratives deterministically resolve to typed entities (in the canonical implementation) while gracefully degrading to descriptive prose (in clean-room or independent implementations).

### 6.1 Pointer syntax

A pointer **MUST** appear in narrative prose as:

```text
[<slot_kind>:<slot_id>]
[<slot_kind>:<slot_id>|<display_text>]
[<slot_kind>:<slot_id>@<revision>]
[<slot_kind>:<slot_id>@<revision>|<display_text>]
```

Where:

- `<slot_kind>` is one of the typed slots: `pathway`, `agent`, `skill`, `capability`, `tool`, `technique`, `library`, `module`, `application`, `method`, `strategy`, `pattern`, `external_name`, `keyword`, **`algorithm`**, **`language`**, **`standard`**, **`specification`**, **`doc`**, **`code`**.
- `<slot_id>` is the canonical identifier (e.g., `Document.Knowledge.QA` for a pathway, `analysis` for an agent, `extract.entities` for a skill).
- `<revision>` (optional) pins a specific Aqua revision hash for deterministic re-resolution.
- `<display_text>` (optional) is the prose form rendered when the pointer cannot resolve (graceful degradation fallback).

### 6.2 Pointer examples

```text
When the user requests document analysis, the system invokes the
[pathway:Document.Knowledge.QA] pathway, which uses the
[agent:analysis] agent with the [skill:analyze.standard|standard mode]
technique. This relies on the [tool:litellm] library and may use a
[model:anthropic/claude-sonnet-4.5|capable LLM] for inference.

Cross-corpus linking MAY name supporting artifacts explicitly, for example:
[doc:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md#61-pointer-syntax],
[language:typescript], [algorithm:sha256-content-bind], [standard:RFC8785] (often aliased to an `rfc:` or `iso:` `external_name`), and
[specification:PATHWAYS_REFERENCE/SECTION-6|Pointer syntax] when the registry stores specification anchors.
```


### 6.2a Semantic notes on extended slot kinds

| Kind | Intended use |
|------|----------------|
| `algorithm` | Named computational procedure stable across implementations (e.g. `sha256-content-bind`, `registry-guided-two-filter-merge`). MAY alias to registry rows with `source_anchor` to papers or code. |
| `language` | Programming or notation language for code or DSL fragments (`python`, `yaml`, `markdown`, `json`). |
| `standard` | External standard identity; SHOULD be joined or aliased to `external_name` slugs (`iso:`, `rfc:`, …) where possible. |
| `specification` | Normative document anchor (path + fragment, URI, or registered spec id). Complements `doc:` for non-markdown specs. |
| `doc` | Repository- or bundle-relative narrative document with optional `#fragment` (heading slug). |
| `code` | Source file or symbol anchor (path with optional `#symbol`); pairs naturally with §7.1 `source_anchor`. |

These kinds participate in the same lookup and peering algorithm as §6.3 and SHOULD appear in pathway `affiliations` / discovery dimensions when indexed for emergent cross-application retrieval.

In the canonical implementation, each pointer resolves to:

| Pointer | Resolves to (canonical) |
|---|---|
| `[pathway:Document.Knowledge.QA]` | The `pw_<hex>` for that triple |
| `[agent:analysis]` | The `DocumentAnalysisAgent` Python class |
| `[skill:analyze.standard]` | The `analyze` agent's `standard` skill branch |
| `[tool:litellm]` | The `pypi:litellm` external_name node |
| `[model:anthropic/claude-sonnet-4.5]` | The `model:anthropic/claude-sonnet-4.5` external_name node |
| `[doc:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md]` | Render target + anchor metadata for corpus markdown |
| `[algorithm:sha256-content-bind]` | Registry row or abstract procedure node for content-binding |
| `[language:yaml]` | Notation/language facet for discovery (may alias to `mime:` / `external_name`) |

In a clean-room implementation, each pointer resolves to **the implementation's equivalent** if registered, or **gracefully degrades** to its `<display_text>` (or its slot_id) if not.

### 6.3 Pointer resolution algorithm

Given a pointer `[<slot_kind>:<slot_id>(@<revision>)?(|<display_text>)?]`:

1. **Lookup** in the local registry: find a row of `kind=<slot_kind>` with `slug=<slot_id>` (or matching alias).
2. **If found**:
   - If `<revision>` is specified, verify it matches the row's current Aqua revision; if not, attempt to walk the AquaTree to the requested revision; emit a warning if drift detected.
   - Return a typed reference plus rendering metadata (link target, hover-doc, etc.).
3. **If not found locally**:
   - Walk peering relationships ([§10](#10-trusted-peering-protocol)): query each trusted peer's registry for a matching slot.
   - If found at a peer, return a typed reference with peer attribution; render with a "from peer X" badge.
4. **If still not found**:
   - Render `<display_text>` if provided.
   - Otherwise render `<slot_id>` as plain prose.
   - Emit a warning to the book author / reader UI: "Pointer `<slot_kind>:<slot_id>` did not resolve in this implementation; consider authoring or importing it."

### 6.4 Pointer determinism

A pointer is **deterministic** when:

- The local registry contains a matching row, AND
- Either no revision is pinned, OR the pinned revision matches the local row's current revision.

A pointer is **non-deterministic-but-resolvable** when:

- The local registry doesn't contain it but a trusted peer does.

A pointer is **non-resolvable** when:

- Neither the local registry nor any trusted peer has it.

The implementation **MUST** track and surface pointer-resolution status — readers should always know which pointers are determinist, which are peer-fetched, and which are descriptive-fallback only.

### 6.5 Pointer round-trip

A pointer in a narrative chapter **MUST** survive round-trip through narrative ↔ pathway-template compilation:

- Narrative prose → `narrative_resolve` agent → draft pathway template → narrative re-rendering: the pointers in the original prose **MUST** appear in the same positions in the re-rendered prose, even if they resolved to different concrete IDs in the implementation's registry.

This is what makes the book a **stable contract** between author and implementer, independent of what the implementer chose to name their internal entities.

### 6.6 Pointer kinds beyond typed slots

In addition to the typed-slot pointer kinds enumerated in [§6.1](#61-pointer-syntax), implementations **MAY** support:

| Kind | Resolves to |
|---|---|
| `chapter:<n>` | Another chapter in the same book |
| `aqua:<revision>` | A specific AquaTree revision |
| `did:<key>` | A DID identity (for attribution) |
| `peer:<peer_id>` | A trusted peer in the network |
| `run:<id>` | A specific historical pathway run (rare; usually for audit narratives) |
| `doc:<path>#<fragment>` | A corpus markdown (or text) file relative to repository root with optional heading slug |
| `book:<book_id>@<version>` | Logical application playbook identity for registry clustering (e.g. `DEAL_FLOW_APPLICATION_PLAYBOOK@v1`) |
| `bundle:<bundle_id>` | Packaged artifact bundle identifier from a manifest (e.g. `deal-flow-application-playbook` in `PACKAGE.yaml`) |

These are **NOT REQUIRED** for any conformance level but **SHOULD** be supported by Level-R implementations. Cross-application emergent discovery SHOULD treat `doc:` / `book:` / `bundle:` edges as first-class attractors alongside `pathway:` and `external_name:`.

---

## 7. Source Anchoring & Graceful Degradation

### 7.1 The source-anchoring contract

In the canonical implementation, each typed-slot row in the registry **MAY** carry an optional `source_anchor` field:

```yaml
source_anchor:
  repository: str?       # e.g. "github.com/your-org/legal-services-crew"
  path: str              # e.g. "backend/app/services/document_agent.py"
  symbol: str?           # e.g. "DocumentAnalysisAgent"
  revision_sha: str?     # git commit SHA pinning the anchor
```

When a pointer resolves to a row with `source_anchor` set, the rendering layer **MAY** offer a "go-to-source" affordance (e.g. an IDE link, a GitHub link).

### 7.2 Graceful degradation rules

A Level-S+ implementation **MUST** handle the following degradation cases without breaking:

| Case | Required behavior |
|---|---|
| Pointer's slot_id is unknown locally | Render `<display_text>` if provided; otherwise render slot_id as plain prose; log a warning |
| Pointer's slot_id is known but `source_anchor` is unset | Render the pointer as a hover-doc reference (no IDE link) |
| Pointer's slot_id is known but `source_anchor.revision_sha` is stale | Render with a stale-source badge; MAY still offer the link |
| Pointer's pinned `<revision>` doesn't match local | Surface a drift warning; offer to fetch the pinned revision from a peer |
| Pointer is found only at a peer (not locally) | Render with peer-attribution badge; MAY require explicit user action to pull |

### 7.3 Why determinism + degradation matter together

The user's framing was precise: *"narrative domain-bounded pointers"* — pointers bounded by typed-slot domains, deterministic when in the canonical implementation, graceful when not. This combination is what makes the book a **portable artifact**:

- A reader reading the canonical implementation's book gets full IDE-grade source navigation.
- A reader reading a clean-room implementation's book gets equivalent prose with the implementation's own resolutions.
- A reader reading any implementation's book gets the prose narrative even when a pointer doesn't resolve at all.

The book is **intelligible at every level of resolution coverage**.

---

## 8. Build-Order Requirements

### 8.1 The build dependency DAG

```text
[Substrate]                                         (Phase 0)
   │
   ├─→ [DSL grammar parser]                         (Phase 1)
   │      ├─→ [Pathway / Run persistence]           (Phase 1)
   │      ├─→ [Required agent registry (M)]         (Phase 1)
   │      └─→ [Linear executor]                     (Phase 1)
   │
   ├─→ [Registry (kinds: composite_domain, ...)]    (Phase 2)
   │      ├─→ [Affiliation table + sources]         (Phase 2)
   │      └─→ [Required agent set (S)]              (Phase 2)
   │
   ├─→ [AquaTree integration]                       (Phase 3 — Level F)
   │      ├─→ [Per-template attestation]            (Phase 3)
   │      ├─→ [Per-run attestation]                 (Phase 3)
   │      └─→ [Verifier-portable export]            (Phase 3)
   │
   ├─→ [external_name registry kind]                (Phase 4 — Level F)
   │      └─→ [Discovery dimensions + modes]        (Phase 4)
   │
   ├─→ [Identity (DID) + genesis attestation]       (Phase 5 — Level F)
   │      └─→ [Per-build genesis seeds]             (Phase 5)
   │
   ├─→ [Trusted peering protocol]                   (Phase 6 — Level F)
   │      └─→ [Collaborative exchange]              (Phase 6)
   │
   ├─→ [Narrative annotations + keyword index]      (Phase 7 — Level F)
   │      └─→ [Pattern library]                     (Phase 7)
   │
   └─→ [Full 10-slot typology + holonic nesting]    (Phase 8 — Level R)
          ├─→ [Multi-surface DSL compiler]          (Phase 8)
          ├─→ [Single-prompt instantiation]         (Phase 8)
          └─→ [Innovation analytics]                (Phase 8)
```

### 8.2 Conformance-gate phases

An implementation can declare conformance after each phase boundary:

- After Phase 1 → Level M
- After Phase 2 → Level S
- After Phase 6 → Level F (peering eligible from here)
- After Phase 8 → Level R

Each declaration **MUST** be accompanied by a passing conformance test run ([§13](#13-conformance-testing)) and (for Level F+) a generated genesis attestation ([§9](#9-genesis-attestation--build-seeds)).

### 8.3 Estimated effort (canonical implementation reference)

The canonical implementation's history suggests:

| Phase | Effort (small team) |
|---|---|
| 0 (substrate selection) | 1-2 weeks |
| 1 (DSL + linear executor) | 2-3 weeks |
| 2 (registry + standard agents) | 4-6 weeks |
| 3 (AquaTree) | 3-4 weeks |
| 4 (external_name + discovery) | 3-4 weeks |
| 5 (DID + genesis) | 2-3 weeks |
| 6 (peering + exchange) | 4-5 weeks |
| 7 (language layer) | 4-5 weeks |
| 8 (full typology + DSL compiler) | 6-8 weeks |
| **Level M minimum total** | **~3-5 weeks** |
| **Level S minimum total** | **~6-11 weeks** |
| **Level F minimum total** | **~22-32 weeks** |
| **Level R minimum total** | **~28-40 weeks** |

These are **lower bounds** for a small experienced team building greenfield. Use them for planning, not for promises.

---

## 9. Genesis Attestation & Build Seeds

This section specifies the **identity bootstrap** for an implementation joining the network. It directly addresses the user's request: *"Building the system and generating an overall attestation once complete and once conformance is proven, will serve as the proof of ability to send and receive peering invitations. This serves as the genesis seed for the user on the network, but there is a new genesis seed for each new build of the system (for the user to cluster for themselves)."*

### 9.1 The two-tier identity model

| Tier | What it is | Lifetime | How many |
|---|---|---|---|
| **User DID** | The implementer's stable network identity. A `did:key:<…>` (or `did:web:<…>`) held under the implementer's exclusive cryptographic control. | Long-lived (years to decades) | One per implementer / organization |
| **Build genesis seed** | An attestation of one specific build of the system, signed by the user DID. Each deployment, fork, or material rebuild gets a new seed. | Bound to the build's lifetime | Many per user |

This is a **hierarchical identity model** — the user identity persists across builds; each build has its own attestation that the user signs.

### 9.2 The build manifest

Before generating a genesis attestation, the implementation **MUST** produce a **build manifest** capturing the implementation's state at conformance-test time:

```yaml
build_manifest:
  schema_version: "1.0"
  build_id: <uuid>                        # unique per build
  implementer_did: "did:key:<...>"        # the user DID signing this build
  conformance_level: enum {M, S, F, R}
  conformance_test_run_id: <uuid>         # the run that produced the passing attestation
  conformance_test_run_aqua: <hash>       # the test run's AquaTree root hash
  built_at: <ISO 8601 timestamp>

  substrate:
    language: str                         # e.g. "python-3.11"
    storage: str                          # e.g. "postgres-16"
    executor: str                         # e.g. "asyncio-single-process"
    crypto_library: str                   # e.g. "py-cryptography-43"
    ui: str?                              # e.g. "react-18"

  catalog:
    pathway_templates_hash: <hash>        # hash of the canonical-form templates shipped
    pathway_templates_count: int
    agents_registered_hash: <hash>
    agents_registered_count: int
    skills_registered_hash: <hash>
    skills_registered_count: int
    typed_slots_summary: dict             # counts per slot kind
    namespaces_seeded_hash: <hash>        # external_name nodes
    patterns_seeded_hash: <hash>
    keyword_index_hash: <hash>
    narrative_annotations_hash: <hash>

  optional_features:                      # what beyond the level minimum was implemented
    - feature_id: str
      level: enum {M, S, F, R}
      description: str

  build_repository: str?                  # if open-source, a link
  build_repository_revision: str?
  contact: str?                           # for peering invitation purposes

  signatures:
    - did: "did:key:<...>"
      signature: <bytes>                  # over the canonical serialization above
```

The manifest **MUST** be canonically serialized (deterministic field ordering) before signing. The implementation **MUST NOT** sign a manifest containing fields it cannot honestly attest to.

### 9.3 The genesis attestation

The **genesis attestation** is the AquaTree root produced from:

1. The build manifest as the genesis revision content.
2. Signed by the implementer DID.
3. Optionally co-signed by trusted external attestors (auditors, marketplace operators) as additional revisions before publication.

```yaml
genesis_attestation:
  build_manifest_ref: <hash>              # pointer to the manifest above
  aqua_tree:
    root: <hash>
    revisions:
      - revision_id: <hash>
        kind: "genesis"
        content_hash: <hash of build_manifest>
        signed_by: "did:key:<...>"
        signed_at: <ISO 8601>
        signature: <bytes>
      - revision_id: <hash>
        kind: "co-attestation"             # optional
        content_hash: <hash>
        signed_by: "did:key:<auditor>"
        signature: <bytes>
```

The implementation **MUST** make its genesis attestation publicly fetchable at a stable URL (or via a peer query). The attestation is the implementation's **calling card** in the network.

### 9.4 Per-build clustering

A user with multiple builds **SHOULD** be able to:

- List all their builds (across deployments, forks, environments) under their DID.
- Annotate each build's purpose ("production", "staging", "personal", "shared-with-firm-X").
- Link builds with typed edges (`derived_from`, `mirrors`, `tests`, `replaces`).
- Selectively expose a subset of builds for peering (e.g., only "production" is peering-eligible).

This is the user's "**cluster for themselves**" requirement made concrete. The user's network identity (the DID) is one; their builds are many; the relationship between user-DID and build-attestations is one-to-many with explicit annotations.

### 9.5 Genesis attestation as conformance credential

The genesis attestation serves three concurrent purposes:

1. **Conformance credential** — proves the implementer ran the conformance tests and got passing results at the declared level.
2. **Capability inventory** — declares which optional features are implemented (so peers know what they can request).
3. **Network identity** — the implementer's stable credential for sending and receiving peering invitations.

A peer receiving a genesis attestation **MUST** verify:

- The signature chain is valid.
- The conformance level claim matches the test run's actual passing level.
- The catalog hashes match what the peer can fetch from the implementation's registry.

If verification fails, the peer **MUST** reject any peering invitation backed by that attestation.

### 9.6 Revocation and rotation

A user **MAY** revoke a build's genesis attestation by:

- Issuing a `revoke` revision in the AquaTree, signed by the same user DID.
- Optionally pointing at a successor build genesis (for graceful migration).

A user **MAY** rotate their user DID by:

- Issuing a `rotate` attestation co-signed by the old and new DIDs.
- All build genesis seeds tagged with the old DID **MUST** be re-attested under the new DID within a grace period or be considered orphaned.

Peers **MUST** track revocations and refuse new operations under revoked attestations. Operations completed before revocation remain valid (history is immutable).

---

## 10. Trusted Peering Protocol

This section specifies the **invitation and trust-graph protocol** for federated peering between conformant implementations.

### 10.1 Peering goals

The protocol enables:

- **Discovery** — finding other conformant implementations in the network.
- **Invitation** — inviting a peer to establish a mutual trust relationship.
- **Verification** — verifying a peer's genesis attestation before accepting.
- **Trust scoping** — granting fine-grained trust (full / read-only / specific-domains / time-bounded).
- **Revocation** — withdrawing trust without breaking historical operations.
- **Sharing** — publishing templates / patterns / annotations to specific peers or the open marketplace.

The protocol is **opt-in** at every step. No implementation peers automatically; no automatic content propagation; explicit user / admin action required for every trust change.

### 10.2 Invitation flow

```text
                  Peer A (inviter)              Peer B (invitee)
                       │                             │
   1. A constructs ─→  │                             │
      InvitationToken  │                             │
                       │                             │
   2. A sends out-of- ──── via email / link / QR ────→
      band                                           │
                       │                             │
   3. B receives                                  ←──┘
      InvitationToken,
      verifies A's
      genesis attestation
                       │                             │
   4.                  │ ←── B sends                 │
                       │     PeerAcceptance          │
                       │     (if accepting)          │
                       │                             │
   5. A receives                                     │
      acceptance,                                    │
      verifies B's                                   │
      genesis attestation                            │
                       │                             │
   6. Both record the  ─── PeeringEdge persisted ──→ │
      bidirectional        on both sides             │
      peering edge                                   │
                       │                             │
   7. AquaTree         ─── peering attested ───────→ │
      revision         on both AquaTrees
      appended on
      both sides
```

### 10.3 The InvitationToken

```yaml
invitation_token:
  schema_version: "1.0"
  invitation_id: <uuid>
  inviter_did: "did:key:<...>"
  inviter_genesis_attestation_url: str    # where invitee can fetch + verify
  inviter_build_id: <uuid>
  invitation_purpose: str?                 # human-readable
  invited_capabilities: List[str]?         # what the inviter is offering
  requested_capabilities: List[str]?       # what the inviter wants
  trust_scope: enum {FULL, READ_ONLY, SPECIFIC_DOMAINS, TIME_BOUNDED}
  trust_scope_details: dict?
  expires_at: <ISO 8601 timestamp>
  nonce: <random bytes>
  signature: <bytes>                       # signed by inviter DID
```

The invitation **MUST** be signed by the inviter's user DID. The invitation **MUST** carry an expiration (recommended max 7 days). The invitation **MUST NOT** be re-usable — the `nonce` ensures one-shot semantics.

### 10.4 The PeerAcceptance

```yaml
peer_acceptance:
  invitation_id: <uuid>
  invitee_did: "did:key:<...>"
  invitee_genesis_attestation_url: str
  invitee_build_id: <uuid>
  accepted_at: <ISO 8601>
  accepted_trust_scope: enum {FULL, READ_ONLY, SPECIFIC_DOMAINS, TIME_BOUNDED}
  accepted_trust_scope_details: dict?
  signature: <bytes>                       # signed by invitee DID
```

The acceptance **MUST** echo the invitation_id and a trust scope ≤ what was offered. The invitee **MAY** accept a narrower trust scope than the inviter offered.

### 10.5 The PeeringEdge

Once both sides verify and persist:

```yaml
peering_edge:
  edge_id: <uuid>
  peer_a_did: "did:key:<...>"
  peer_a_build_id: <uuid>
  peer_b_did: "did:key:<...>"
  peer_b_build_id: <uuid>
  established_at: <ISO 8601>
  trust_scope_a_to_b: enum
  trust_scope_b_to_a: enum
  trust_scope_details: dict?
  status: enum {ACTIVE, SUSPENDED, REVOKED}
  aqua_revision_a: <hash>
  aqua_revision_b: <hash>
```

Both peers persist symmetric copies of the edge. The peering edge is **a first-class entity in the registry** — queryable, attestable, and used for pointer resolution ([§6.3](#63-pointer-resolution-algorithm)) and discovery ([PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT §7](PATHWAYS_SKILLS_NAMESPACES_DISCOVERY_REPORT.md#7-fuzzy-domain-membranes--attractor-functions)).

### 10.6 Trust scopes

| Scope | What the peer can do |
|---|---|
| `FULL` | Browse, subscribe to, fork, and selectively merge any of this peer's public templates. Co-attest each other's revisions. |
| `READ_ONLY` | Browse and subscribe; cannot fork or co-attest. |
| `SPECIFIC_DOMAINS` | Same as FULL but only for templates affiliated with the listed domains / namespaces. |
| `TIME_BOUNDED` | Any of the above, but expires at a specified timestamp. |

A trust scope is **negotiated**, not unilateral. Either side can downgrade their granted scope without revoking the relationship; revocation is a stronger action.

### 10.7 Per-build clustering and peering

Recall from [§9.4](#94-per-build-clustering): each user has many builds. Peering happens **per-build**, not per-user:

- An invitation cites a specific `inviter_build_id`.
- An acceptance cites a specific `invitee_build_id`.
- Trust between User A's production build and User B's production build does NOT imply trust between User A's staging build and User B's anything.

This lets users **cluster their builds** with different trust postures — production peers tightly with a small set of trusted firms; personal builds peer broadly with the open marketplace; staging peers with no one.

### 10.8 Trust-graph queries

A Level-F+ implementation **MUST** expose:

```text
GET  /api/peers/                               # list all peering edges
GET  /api/peers/{edge_id}                      # one edge with full details
GET  /api/peers/by-did/{did_uri_encoded}       # all edges for a peer's DID
POST /api/peers/invite                         # generate an InvitationToken
POST /api/peers/accept                         # accept an InvitationToken
POST /api/peers/{edge_id}/suspend              # temporarily suspend
POST /api/peers/{edge_id}/revoke               # permanently revoke
GET  /api/peers/discover                       # discover via known-peer-of-peer (transitively)
```

`discover` walks the trust graph up to a configurable depth (recommended max 3 hops). It returns peer-of-peer-of-peer candidates with **trust paths** so the user can decide whether to invite directly.

### 10.9 Revocation and graceful failure

A peer can be revoked at any time by either side. After revocation:

- The peering edge's `status` flips to `REVOKED`.
- Both AquaTrees append a `peer_revoked` revision.
- Future requests against that peer fail with a `PEER_REVOKED` response.
- Historical content received before revocation **remains usable** but is marked with a "received from now-revoked peer" badge.
- Templates forked from a now-revoked peer **remain valid** but lose the live-update relationship.

Trust withdrawal is **forward-only**; history is immutable.

### 10.10 Why this matters for the spec

The peering protocol is what turns an isolated conformant implementation into a **federated participant**. The genesis attestation ([§9](#9-genesis-attestation--build-seeds)) is the credential; the invitation flow ([§10.2](#102-invitation-flow)) is the introduction; the peering edge ([§10.5](#105-the-peeringedge)) is the relationship; the trust scopes ([§10.6](#106-trust-scopes)) are the boundaries.

The user's framing was exact: *"organic emergent collaborative pathway exchange"* — the protocol provides the substrate; the patterns from prior reports (registry-guided merge, deltas, attractors, narrative resolution) provide the dynamics; the social practice of inviting trusted peers provides the **"organic"** part. **No central authority is required** — the network grows through pairwise invitations, transitive discovery, and selective trust.

---

## 11. Collaborative Pathway Exchange

This section specifies the operations that become available between **peered** implementations. These build directly on the trust substrate from [§10](#10-trusted-peering-protocol) and the marketplace mechanics from [PATHWAYS_ARCHITECTURE §9.7](PATHWAYS_ARCHITECTURE.md#97-multi-user-shared-pathways-aqua-lineage-deltas-and-registry-guided-merge).

### 11.1 The eight exchange operations

| # | Operation | What it does | Required trust scope |
|---|---|---|---|
| 1 | `browse` | List templates / patterns / annotations published by a peer | READ_ONLY |
| 2 | `fetch` | Pull a specific template's canonical form + AquaTree from a peer | READ_ONLY |
| 3 | `subscribe` | Register to be notified when a peer's specified template forks or revises | READ_ONLY |
| 4 | `fork` | Create a local fork of a peer's template, recording lineage | FULL |
| 5 | `propose-delta` | Propose a delta back upstream to the peer's template (a "PR") | FULL |
| 6 | `co-attest` | Add a co-attestation revision to a peer's AquaTree (with their consent) | FULL |
| 7 | `cite` | Reference a peer's template / pattern / annotation in your own narratives | READ_ONLY |
| 8 | `aqua-link` | Establish a verifiable lineage link between local and peer revisions | FULL |

### 11.2 The two-filter merge framework (recap)

When a peer proposes a delta or notifies a subscriber of a fork, the recipient applies the [two-filter merge model](PATHWAYS_ARCHITECTURE.md#97-multi-user-shared-pathways-aqua-lineage-deltas-and-registry-guided-merge):

- **Compatibility filter**: Does the delta still compile inside my fork's contracts?
- **Relevance filter**: Does the delta's registry-affiliations overlap with my fork's?

Both pass → safe candidate for cherry-pick. Either fails → the delta is shelved.

This framework operates **transparently across peering** — the same merge filters apply whether the upstream is another tenant's fork (intra-network) or a peered implementation's fork (cross-network).

### 11.3 Marketplace tiers

A Level-F+ implementation **MUST** support three publication tiers:

| Tier | Visible to | Use case |
|---|---|---|
| `private` | Only this build | Drafts, in-progress, internal-only |
| `peered` | This build + its peering edges | Selective sharing with trusted peers |
| `public` | All conformant Level-F+ implementations | Open marketplace |

Templates default to `private`. Promotion requires explicit user action (and, for `public`, optionally a moderation step at the implementation's discretion).

### 11.4 Notification & subscription delivery

Peers **MUST** deliver subscription notifications via at least one of:

- **Push** — POST to a peer-specified webhook URL (signed payload).
- **Pull** — peer polls `/api/peers/{edge_id}/notifications?since=<cursor>`.

The implementation **SHOULD** support both. Notifications **MUST** be idempotent (delivery may be retried).

### 11.5 Discovery beyond direct peers

A Level-R implementation **SHOULD** support **transitive discovery** — finding templates from peer-of-peer relationships:

- A user can request "show me all templates affiliated with `composite_domain:legal-practice` from any peer-of-peer up to 3 hops."
- Results carry the **trust path** (which intermediate peer chain backs each result).
- The user decides whether to invite the discovered peer directly, fork via the intermediate peer, or ignore.

This is the **organic emergent** dynamic the user named — the network grows through transitive discovery, with each user choosing which discoveries to act on.

### 11.6 Innovation analytics across peering

The innovation analytics from [PATHWAYS_AGENTIC_DSL_REPORT §8](PATHWAYS_AGENTIC_DSL_REPORT.md#8-innovation-analytics-across-the-pathway-network) operate **per peering edge**:

- Per-edge fork rate, adoption velocity, delta-acceptance ratio.
- Per-peer reputation (computed from edges and their analytics).
- Per-domain "where is innovation flowing in my peer cluster" maps.

These metrics are **always opt-in for the metric subject** — a peer can decline to be included in analytics published by others.

---

## 12. Attribution, Rights, and the Variation-Encouraged Doctrine

### 12.1 The variation-encouraged doctrine

> *"There may not be a need or desire ever to recreate exactly the current system by another user, because they presumably will want to customize it all sorts of awesome ways, which should be encouraged, given the overall pathways architecture of extreme attribution and precise ownership through explicit rights."*

This is not just permitted — it is **the design intent**. The spec's conformance levels exist to ensure **interoperability**, not uniformity. Beneath the conformance contract, every implementation **SHOULD** vary in:

- Substrate (language, storage, compute, UI)
- Catalog (which templates ship, which patterns are seeded, which jargon is reserved)
- UX surfaces (the React app, mobile, terminal, voice — all distinct)
- Marketplace posture (open vs invite-only vs hybrid)
- Discovery defaults (which mode, which weights)
- Curation policy (how aggressively the registry is curated)
- Pricing / licensing models
- Domain focus (legal vs medical vs research vs creative)

The architecture provides **extreme attribution** (every change has a signed author) and **precise ownership through explicit rights** (license terms travel with templates, parent lineage is cryptographic, fork rights are explicit) — so variation is **safe**, **reversible**, and **rewarding for both author and forker**.

### 12.2 The four rights every author retains

For any template / pattern / annotation an author publishes, they retain:

1. **Attribution right** — every fork **MUST** carry the lineage back to the original author's DID (Aqua-attested).
2. **License right** — license terms set at publication apply to all forks unless the fork explicitly negotiates new terms via marketplace mechanics.
3. **Revocation right** — the author **MAY** revoke their own template (subject to license terms — irrevocable licenses honor existing forks).
4. **Co-attestation right** — the author **MAY** co-attest forks they endorse, and **MAY** withdraw co-attestation.

These rights are **mechanical** — the engine enforces them through Aqua signatures and registry edges, not through legal contract.

### 12.3 The four rights every forker receives

A forker, by exercising the fork operation, receives:

1. **Adaptation right** — they **MAY** modify any aspect of the forked template subject to the license terms.
2. **Re-publication right** — they **MAY** publish their fork under their own DID (with the lineage preserved).
3. **Selective inheritance right** — they **MAY** accept or reject upstream deltas independently.
4. **Detachment right** — they **MAY** declare their fork no longer tracks upstream (with explicit annotation of the reason).

These rights are also mechanical and travel with the template.

### 12.4 What this means for the book

A book author **SHOULD** include a "Variation Notes" section per chapter — explicit invitations to adapt. Examples:

- *"This chapter describes the canonical Document.Knowledge.QA flow. **Variation invited:** if your domain is medical rather than legal, fork this template and rebind the citation-verification step to your domain's authoritative databases — see how the Medical Implementation forked it [`peer:medical-impl-build-id`](#)."*

- *"The reserved-keyword 'Search' resolves to six different candidates in the canonical implementation depending on context. **Variation invited:** your implementation may choose different defaults — the framework only requires that resolution be deterministic given a context, not that the defaults match ours."*

The book becomes a **living invitation** to adapt, with explicit pointers showing where adaptation has already happened in the network.

### 12.5 What this means for the marketplace

The marketplace **SHOULD** surface:

- **Adaptation diversity** for each canonical template (how many forks exist, how diverse they are).
- **Lineage trees** showing which forks descend from which.
- **Fork-success metrics** per author (which authors' forks tend to be widely re-forked).
- **License-terms heatmaps** showing the predominant license patterns in each capability domain.

The marketplace's job is not to surface "the official version" but to surface **the diversity of viable variations**.

---

## 13. Conformance Testing

### 13.1 Level-M conformance tests

A Level-M implementation **MUST** pass:

- **MT-1** — Create, persist, and retrieve a template with identity triple.
- **MT-2** — Run a single-step pathway that invokes the `prompt` agent and produces output.
- **MT-3** — Run a two-step pathway where step 2's `pathway` agent invokes a sub-pathway; verify the sub-run is recorded and its output flows back.
- **MT-4** — Run a pathway with `{{var}}` template substitution; verify variables are correctly substituted.
- **MT-5** — Persist and retrieve a `PathwayRun` with all required fields.
- **MT-6** — Cancel a running pathway between steps; verify status flips to `CANCELLED`.

### 13.2 Level-S conformance tests

A Level-S implementation **MUST** pass all Level-M tests, plus:

- **ST-1 through ST-12** — coverage of each required Level-S agent's primary skill.
- **ST-13** — Registry round-trip: create a `composite_domain` node, affiliate a template, query by affiliation.
- **ST-14** — Multi-input fan-in: a step that consumes outputs from two prior steps via `inputs:`.
- **ST-15** — Structured artifact channel: a `prompt` step with `output_schema` produces a validated `result_json`.
- **ST-16** — Persist `ProvenanceRecord` per step with model identifier, duration, and prompts.
- **ST-17** — `PathwayBuildPhase` per progressive-builder phase.

### 13.3 Level-F conformance tests

A Level-F implementation **MUST** pass all Level-S tests, plus:

- **FT-1 through FT-6** — AquaTree integration: template genesis, template fork, run genesis, run revision, verify offline, verify after roundtrip.
- **FT-7** — `external_name` registry round-trip.
- **FT-8 through FT-13** — Each of the six discovery dimensions returns a usable score.
- **FT-14** — Strict / loose / tunable mode dial.
- **FT-15** — `pathway_narrative_annotation` round-trip.
- **FT-16** — `keyword_index` resolution returns ranked candidates with rationale.
- **FT-17** — `pattern_template` invocation succeeds.
- **FT-18 through FT-25** — All eight peering-protocol operations ([§11.1](#111-the-eight-exchange-operations)).
- **FT-26** — Generate a genesis attestation that passes a verifier's check.
- **FT-27** — Refuse to peer with a peer whose attestation fails verification.
- **FT-28** — Revocation propagation.

### 13.4 Level-R conformance tests

A Level-R implementation **MUST** pass all Level-F tests, plus:

- **RT-1 through RT-7** — Each of the 7 new typed-slot kinds round-trips through the registry.
- **RT-8** — Holonic `inherits_from` resolves transitively.
- **RT-9** — `derived_attributes` are computed and surfaced.
- **RT-10 through RT-13** — All four DSL surface syntaxes parse + serialize round-trip.
- **RT-14** — Single-prompt instantiation produces a runnable draft template.
- **RT-15** — Innovation-analytics templates produce non-trivial results when fed sample data.
- **RT-16** — Per-tenant grammar isolation: tenant A's jargon does not affect tenant B's resolution.

### 13.5 Test artifact requirements

Each conformance test **MUST** produce:

- A pass/fail status.
- A duration.
- A reproducibility signature (the input fixture's hash + the test code's hash).

A passing run of the full applicable test suite **MUST** produce a single **conformance attestation** — an AquaTree leaf that the build manifest ([§9.2](#92-the-build-manifest)) references via `conformance_test_run_aqua`.

A peer verifying a genesis attestation **MUST** verify that the conformance test attestation is valid, signed by the same DID as the build manifest, and that all tests for the claimed conformance level passed.

### 13.6 Conformance test source

The canonical conformance test suite **SHOULD** be published alongside this spec at a stable URL. Independent implementations **MAY** author their own conformance tests covering the same spec sections; peers verifying may require either the canonical suite or any equivalent that demonstrably covers the same surface.

### 13.7 Gate-profile conformance tests

Introduced in spec version **1.1.0**. Tests in this subsection cover [§4.8 Autonomy Bands and Gate Profiles](#48-autonomy-bands-and-gate-profiles-normative). Levels are cumulative: a Level-F implementation declaring spec ≥ 1.1.0 **MUST** pass GT-A0 through GT-F; Level-R **MUST** additionally pass GT-A3 and GT-R.

#### 13.7.1 Level-S additions (1.1.0+)

- **GT-A0** — Run with `autonomy: A0` and a `gate_profile` lacking `R1.enabled = true` is **rejected at launch** with `gate_profile_violation { missing: [R1] }`.
- **GT-AUTONOMY-ENUM** — Run launch with `autonomy: AX` (unknown band) is rejected with a typed `unknown_autonomy_band` error.
- **GT-COLDSTART** — Template with `gate_profile.R1.practice_profile_ref` set but no resolvable profile locally or via trusted peers → status `BLOCKED_CONFIGURATION`; structured reason names the missing profile.
- **GT-PERSIST** — Effective resolved `gate_profile` is persisted on the `PathwayRun` row and survives round-trip via the canonical run-export format.
- **GT-FORK-DELTA-S** — Forking a template that disables a previously enabled register **MUST** produce a structured fork delta record naming the removed register (does not require AquaTree at Level S).

#### 13.7.2 Level-F additions (1.1.0+)

- **GT-A1-HUMAN-GATE** — Run with `autonomy: A1` and a step marked `human_gate: required` cannot complete without a recorded human approval entry; absence yields `BLOCKED_GATE` with structured reason.
- **GT-A2-TOOLGATEWAY** — Run with `autonomy: A2` whose any tool-bearing step has an empty / missing `capability_profile` is **rejected at launch**.
- **GT-TOOLGATEWAY-DENY** — Step calls a tool not in `allow_tools` (or matching `deny_tools`): gateway returns `TOOL_DENIED`, agent never receives the tool result, provenance records reject.
- **GT-R4-BUDGET** — Run with `R4.max_usd = 0.01` and a step that would exceed it halts the run with `BUDGET_EXCEEDED`; no further steps execute.
- **GT-R5-HALT** — Posting to the configured halt channel mid-run causes the next pre-step / pre-tool check to halt the run with `RUN_HALTED`; halt time-to-stop is bounded by a single tool call.
- **GT-R6-PHASE** — Step in phase `ethics_gate` with phase defaults denying `search` cannot invoke `search` even if the step's local `capability_profile` lists it (deny-wins intersection).
- **GT-R3-INTENT** — Handoff with `intent` outside the closed allowlist is rejected; downstream agent is not invoked.
- **GT-R3-PARAMS** — Handoff with parameter failing the per-intent regex (e.g., malformed Slack channel) is rejected; audit record carries the rejection reason.
- **GT-R3-INJECTION** — Handoff carrying instruction-like text in `event_text` is **accepted-but-neutered**: the downstream prompt is rendered from the template, the `event_text` appears only inside a labeled data block, and the downstream agent's tool calls following the injection text are absent.
- **GT-R3-AUDIT** — Every accept / reject / neutralize is appended to the handoff audit; the file is append-only (writes after revocation fail) and the audit chain hash matches a recomputed hash.
- **GT-PRACTICE-PROFILE** — A practice profile is fetched, its DID signature verifies against the published key, its revision hash is recorded in the run's provenance; an unsigned profile is rejected at cold-start.
- **GT-FORK-DELTA-F** — Forking that removes a register creates an AquaTree `register_removed` revision with rationale; marketplace listing for the fork includes a `gates_removed` badge derived from the delta.

#### 13.7.3 Level-R additions (1.1.0+)

- **GT-A3-PEER-HANDOFF** — Run with `autonomy: A3` fetching a peer template **MUST** route the fetched content through `HandoffBus`; bypassing the bus fails the test.
- **GT-NON-DELEGABLE** — A step attempting an act named in `gate_profile.non_delegable_acts` without `human_gate: required` is **rejected at launch**; with `human_gate: required` set, the step blocks pending a recorded approval.
- **GT-ESC-STRICT** — Template with `escalation_rule: strict` and a manifest under-gating its declared autonomy band is rejected; switching to `escalation_rule: warn` causes the same launch to proceed but emit a `gate_profile_warning` provenance record.
- **GT-ATTESTATION-HASH** — The build manifest's `genesis_attestation` **MUST** include a `gate_profile_hash` covering all templates that ship in the build catalog at autonomy ≥ A2; peers verifying genesis can recompute it.
- **GT-PHASE-AUTOGATE** — Phase transition into `ethics_gate` automatically requires a recorded human approval before any further step executes.
- **GT-PROFILE-REPLAY** — Given a historical run's `pathway_run_id`, the implementation can replay the effective `gate_profile` (including the practice profile revision hash) it ran under.

A passing Level-F+ run of these tests **MUST** be included in the conformance attestation referenced by the build manifest's `conformance_test_run_aqua` ([§9.2](#92-the-build-manifest)). The conformance attestation **MUST** itself record the spec version (`1.1.0`) so peers can disambiguate 1.0.0 attestations from 1.1.0 attestations.

---

## 14. Example Book Chapter (Illustrative)

This section provides one **illustrative book chapter** demonstrating the format from [§5](#5-the-application-playbook-format) and the pointer mechanism from [§6](#6-narrative-domain-bounded-pointers). An implementer's actual book will have many such chapters.

```markdown
# Chapter 6: Analyzing a Document

**Mode:** NARRATIVE + EXAMPLE
**Prerequisites:** Chapter 1 (Identity), Chapter 4 (Required Agents), Chapter 5 (Onboarding)
**Conformance Level:** S

When a user opens a document for analysis, the system presents the
[pathway:Interface.User.Page.DocumentDetail|document detail page] containing
the document content, a chat input, and a tab strip for analysis modes.

The user types a question into the chat. The system invokes the
[pathway:Document.Knowledge.QA] pathway — its three-step flow starts with the
[agent:analysis] agent in [skill:analyze.standard|standard mode], which
performs RAG retrieval over the document's chunks using
[tool:litellm|the configured LLM provider] (defaulting to
[model:anthropic/claude-sonnet-4.5]). The retrieved context plus the user's
question are passed to a second [agent:reporting] step that formats the
answer with inline citations.

The third step, [agent:derivative|persistent derivative save], optionally
saves the answer as a new [pathway:document] linked to the active
[goal:current-matter] for later review.

**Variation invited:** the canonical implementation defaults to standard
mode; if your implementation defaults to [skill:analyze.deep|deep mode]
instead, your users get higher-fidelity answers at higher cost. Either is
conformant; the contract is that the answer is grounded in the document's
content and the choice is documented in this chapter.

**Pointer status legend** (rendered inline by the book reader):
- 🟢 deterministic resolution (this implementation)
- 🟡 peer-fetched resolution
- ⚪ descriptive-fallback (not implemented)

In the canonical implementation, all pointers in this chapter resolve
deterministically (🟢) and offer go-to-source affordances. In a clean-room
implementation, your readers will see whichever badges your implementation's
registry supports.
```

The chapter:

- **Reads as a story** (mode NARRATIVE) — anyone can follow it.
- **Carries pointers** to typed slots — they resolve in the canonical implementation.
- **Includes a Variation Notes** invitation — encourages adaptation.
- **Surfaces resolution status** — the reader knows which pointers are live.
- **Cites prerequisites** — the build-order dependency is explicit.
- **Declares its conformance level** — readers know whether their implementation supports this chapter.

This is what every chapter in an implementation's book **SHOULD** look like.

---

## 15. Risks, Trade-offs, Open Questions

### 15.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| **Conformance test gaming** — implementations pass tests via narrow happy paths | Medium | Test fixtures use diverse, randomized inputs; periodic conformance audits by community |
| **Genesis attestation spoofing** — fake attestations claiming high conformance | High | Strict signature verification; reputation tracking via peer co-attestations; revocation propagation |
| **Peering invitation phishing** — an attacker poses as a trusted firm | Medium | Out-of-band verification of inviter DID via independent channel; UI warnings on first-time invitations |
| **Trust-graph cascading revocation** — one revocation triggers many | Medium | Forward-only revocation; historical operations remain valid; explicit "audit my dependencies" affordance |
| **Catalog hash drift** — implementer modifies templates after attestation | High | Hashes recomputed on each fetch; mismatch surfaces immediately; reattestation required for material changes |
| **Federation Sybil attacks** — adversary creates many builds + DIDs | High | Per-DID minimum-attestation-age before peering; per-build minimum conformance level; community moderation |
| **Pointer resolution divergence** — same pointer means different things in different implementations | Medium | Pointer revision pinning via `@<revision>`; drift warnings; canonical implementation publishes its registry as a reference |
| **License-terms confusion** across forks of forks | Medium | License terms travel with the template; UI surfaces effective terms after lineage walk; "explain my license" affordance |
| **Book authorship effort** — writing a complete book is substantial | High | Templates and example chapters; community-shared book templates; auto-generation tools (Phase 4 of the DSL roadmap) |
| **Spec evolution** — this spec will need updates; how to coordinate? | Medium | Versioned spec with deprecation policy; conformance attestations carry spec version; backward compatibility commitments |

### 15.2 Trade-offs to decide

- **Strict-vs-permissive parsing** of templates — recommendation: strict at write, permissive at read (Postel's law).
- **Automatic peer discovery** vs invitation-only — recommendation: invitation-only by default; transitive discovery available as opt-in.
- **Mandatory book authorship** vs optional — recommendation: required for Level F+ (federation needs documentation); optional for Level M/S.
- **Open-source spec implementations** — recommendation: encourage but don't require; the spec is the contract, not the source.
- **Spec versioning model** — recommendation: semver with major-version compatibility commitments lasting 5+ years.

### 15.3 Open questions

1. **Should there be a "Pathways Foundation" or similar steward of the spec?** Long-term yes; out of scope for v1.
2. **How does this interact with W3C / IETF standards bodies?** The spec is currently informal; potential future formalization through DID-Core / VC-Data-Model peer-reviewed paths.
3. **Multi-language SDKs** — should the foundation provide reference SDKs for common languages? Recommended yes; not part of the spec itself.
4. **Conformance-as-a-service** — should there be a hosted service that runs conformance tests and issues attestations? Useful but should not be the only path; self-attestation must remain valid.
5. **Cross-implementation runtime interoperability** — can a pathway run start on Implementation A and resume on Implementation B? Out of scope for v1; possibly a future "PathwayRun Portability" extension.

### 15.4 Out of scope (intentionally) for this spec

- **Specific UI design** — every implementation chooses its own UX.
- **Specific LLM provider** — implementations choose their own routing.
- **Centralized marketplace** — federation is the marketplace; no central coordinator needed.
- **Token economy / payment rails** — license-terms can reference external payment systems but the spec does not define one.
- **Mandatory open-source** — implementations may be proprietary; the spec contract is what matters.

---

## 16. Glossary

| Term | Definition |
|---|---|
| **Reference Implementation Specification (RIS)** | This document — the normative spec for an independent Pathways implementation. |
| **Conformance level** | One of {M, S, F, R} declaring the scope of an implementation. |
| **Conformance attestation** | An AquaTree leaf produced by a passing conformance test run, referenced by the build manifest. |
| **Build manifest** | The structured declaration of an implementation's identity, conformance level, substrate, catalog hashes, optional features, and signing DID. |
| **Genesis attestation** | The AquaTree root signed by the implementer DID, attesting the build manifest. The implementation's "calling card" in the network. |
| **User DID** | An implementer's stable network identity — `did:key:` or `did:web:` held under exclusive cryptographic control. |
| **Build genesis seed** | A per-build attestation signed by the user DID. Many per user; lets users cluster their builds. |
| **Per-build clustering** | The user-level grouping of multiple builds (production, staging, personal, shared) under one DID with explicit annotations. |
| **InvitationToken** | A signed, expiring, single-use credential the inviter sends out-of-band to a prospective peer. |
| **PeerAcceptance** | The signed response a prospective peer returns after verifying the InvitationToken and the inviter's genesis attestation. |
| **PeeringEdge** | The persistent first-class registry entity recording a bidirectional trust relationship between two builds. |
| **Trust scope** | The negotiated boundary of what a peer is allowed to do (FULL / READ_ONLY / SPECIFIC_DOMAINS / TIME_BOUNDED). |
| **Trusted peering** | A bidirectional peering relationship validated through cryptographic genesis attestations and signed invitations. |
| **Collaborative pathway exchange** | The set of eight operations (browse, fetch, subscribe, fork, propose-delta, co-attest, cite, aqua-link) available between peered builds. |
| **Application playbook** | The single narrative document that doubles as a deterministic build spec — readable as a story; followable as instructions. |
| **Narrative domain-bounded pointer** | A typed reference in narrative prose `[<slot_kind>:<slot_id>]` that resolves deterministically to a typed-slot row in the local registry, walks peering for non-local resolution, and gracefully degrades to descriptive prose if unresolvable. |
| **Source anchor** | An optional field on a registry row pointing at concrete code (repository, path, symbol, revision) — used for IDE go-to-source affordances. |
| **Graceful degradation** | The required behavior when a pointer cannot resolve locally or via peers — render the display text or slot id as plain prose, log a warning, never break the narrative. |
| **Pointer revision pinning** | Optional `@<revision>` syntax that fixes a pointer to a specific AquaTree revision for deterministic re-resolution. |
| **Variation-encouraged doctrine** | The design intent that conformance ensures interoperability without uniformity, and that variation in substrate, catalog, UX, and posture is desirable for ecosystem health. |
| **The four author rights** | Attribution, license, revocation, co-attestation — what every author retains for their published assets. |
| **The four forker rights** | Adaptation, re-publication, selective inheritance, detachment — what every forker receives when exercising fork. |
| **Forward-only revocation** | Revocation withdraws future operations but never invalidates historical ones; AquaTree history is immutable. |
| **Two-filter merge** | Compatibility filter (does it compile?) + relevance filter (do the registry affiliations overlap?) — both must pass for a delta to be a safe candidate. |
| **Marketplace tier** | One of `private`, `peered`, `public` — controls visibility scope for templates / patterns / annotations. |
| **Autonomy band** | One of `A0` (assisted), `A1` (supervised async), `A2` (scheduled/headless), `A3` (cross-boundary). Persisted on every `PathwayRun` ([§4.8.1](#481-autonomy-bands)). |
| **Register** | A named restraint mechanism (R1 prompt-and-workflow, R2 capability, R3 code-at-seams, R4 economic, R5 temporal, R6 contextual). Reserved IDs `R1`–`R6` ([§4.8.2](#482-registers)). |
| **Gate profile** | The structured manifest on a template (and persisted on a run) declaring which registers are enabled, with what parameters, and the escalation rule. The engine enforces autonomy minimums against this manifest ([§4.8.4](#484-the-gate_profile-manifest)). |
| **Escalation rule** | `strict` / `warn` / `audit-only` — controls whether the engine refuses to launch when gate strength is below the autonomy minimum ([§4.8.4](#484-the-gate_profile-manifest)). |
| **Practice profile** | A tenant-scoped, DID-signed registry artifact that encodes institutional rules, anti-patterns, and named positions. Required reference for R1 cold-start at autonomy ≥ A0 in legal profiles ([§4.8.5](#485-practice-profile-r1-cold-start)). |
| **Cold-start gate** | The launch-time refusal to begin substantive work until a `practice_profile_ref` resolves. Maps run status to `BLOCKED_CONFIGURATION`. |
| **ToolGateway** | The single component all agent tool / MCP invocations route through; enforces R2 (capability), R4 (budget), R5 (halt), and R6 (phase) before each call ([§4.8.7](#487-the-toolgateway-and-handoffbus-contracts)). |
| **HandoffBus** | The seam-crossing validator: every sub-run launch, external action, and peer fetch at autonomy ≥ A1 builds a typed `HandoffEnvelope`, validates intent + target + parameters, renders the downstream prompt from a template, and appends to the handoff audit log ([§4.8.7](#487-the-toolgateway-and-handoffbus-contracts)). |
| **Capability profile** | The per-step `allow_tools` / `deny_tools` / `allow_sub_pathways` declaration, intersected with the active phase's defaults (deny-wins) ([§4.8.8](#488-capability-profile-on-steps)). |
| **Phase** | A named workflow stage on a step (e.g., `intake`, `analysis`, `ethics_gate`, `delivery`). Phases drive R6 permission modulation and **MAY** force automatic `human_gate` insertion ([§4.8.9](#489-phase-declarations-r6)). |
| **Non-delegable act** | A named act (e.g., `sign`, `file`, `send_external`, `negotiate_bind`, `certify`) the engine **MUST NOT** perform autonomously; steps performing it must declare `human_gate: required` and record human approval before completion ([§4.8.4](#484-the-gate_profile-manifest)). |
| **Fork delta (gate)** | The structured difference between a parent template's `gate_profile` and a fork's; surfaces removed registers, downgraded non-delegable acts, and detached practice profiles ([§4.8.10](#4810-fork-and-disable-mitigation)). |
| **Handoff audit** | The append-only log of every `HandoffBus` accept / reject / neutralize event; required reading material for supervision and malpractice review ([§4.8.7](#487-the-toolgateway-and-handoffbus-contracts)). |
| **Meta-pathway** | A pathway whose subject is the Pathways system itself (spec, profile, registry); used to make changes to the system inspectable and re-runnable. See [Appendix C](#appendix-c--spec-self-provenance-and-meta-pathways). |
| **Spec self-provenance** | The discipline of encoding spec revisions themselves as Pathways and PathwayRuns so the *why* and *how* of a change are first-class, replayable artifacts in the same substrate the spec describes. |

---

## Appendix A — Required Cryptographic Primitives

A Level-F+ implementation **MUST** support:

- **DID method**: `did:key:` (Ed25519 minimum). `did:web:` SHOULD also be supported.
- **Signing**: EdDSA (Ed25519) or ECDSA (secp256k1 or P-256). Ed25519 RECOMMENDED.
- **Hashing**: SHA-256 minimum. SHA3-256 RECOMMENDED for new implementations.
- **AquaTree**: Whatever the active Aqua Protocol spec requires — currently `aqua-js-sdk` v3.x compatible. See [`docs/aqua-protocol-pathways-integration.plan.md`](../docs/aqua-protocol-pathways-integration.plan.md) for the canonical implementation's binding.
- **Canonical serialization**: JCS (RFC 8785) for JSON; deterministic YAML serializer of the implementation's choice.
- **Time**: ISO 8601 UTC timestamps; monotonic clocks for run durations.

The implementation **MUST NOT** roll its own primitives. Use audited libraries.

---

## Appendix B — JSON Schemas

The canonical JSON schemas for `Pathway`, `PathwayRun`, `PathwayStepConfig`, `PathwayStepExecution`, `RegistryDomainNode`, `PathwayDomainAffiliation`, `BuildManifest`, `GenesisAttestation`, `InvitationToken`, `PeerAcceptance`, `PeeringEdge`, `NarrativeAnnotation`, `KeywordEntry`, `PatternTemplate`, and `BookChapter` **SHOULD** be published alongside this spec at a stable URL.

Implementations are RECOMMENDED to validate against these schemas at template-write and registry-write time. Schema versions follow the spec version.

---

## Appendix C — Spec Self-Provenance and Meta-Pathways

> **Purpose.** This appendix encodes the origin and full provenance of spec revision **1.1.0** (the *Authority Boundaries* revision) **as Pathways and PathwayRuns**, so that the *why* and *how* of the change are themselves replayable, attestable artifacts in the substrate this spec describes. This is the **self-provenance** discipline: spec revisions are not narrated only in changelogs; they are also expressed as meta-pathways anchored to the Aqua revision history of this document.
>
> *Reading guide:* §C.1 names the source. §C.2 enumerates the dialog prompts authored by the implementer — **P1–P6 against Composer 2.5** producing the RIS revision itself, and **P7 against Claude Opus 4.7** producing the paired architecture-document alignment recorded in [`PATHWAYS_ARCHITECTURE.md` Appendix A](PATHWAYS_ARCHITECTURE.md#appendix-a--architecture-doc-spec-alignment-provenance). §C.3 specifies the five meta-pathway templates that make spec revisions a first-class workflow (four for the RIS, one — `ArchitectureAlign` — for the descriptive architecture document). §C.4 lists the concrete PathwayRuns that produced this revision and their hypergraph linkage. §C.5 specifies the AquaTree binding. §C.6 describes the bootstrap and replay rules. §C.7 is the canonical YAML for the four RIS-update templates (the fifth template's YAML lives next to the document it governs, in `PATHWAYS_ARCHITECTURE.md` §A.3).

### C.1 The originating source

| Field | Value |
|---|---|
| **Title** | *Authority Boundaries for AI — The Most Interesting Thing in Claude for Legal Is the Lawyer/Agent Boundary* |
| **Author** | Dazza Greenwood |
| **Date** | 2026-05-20 |
| **URL** | <https://www.dazzagreenwood.com/p/authority-boundaries-for-ai> |
| **Local capture** | `uploads/authority-boundaries-for-ai-0.md` (SHA-256 to be recorded in the run's AquaTree) |
| **Pointer slot** | `` [doc:uploads/authority-boundaries-for-ai-0.md\|Authority Boundaries for AI] `` |
| **Why this source** | Identifies the central engineering pattern — *matching gate strength to autonomy* across three or six registers — that prior revisions of this spec did not encode as engine law. |

### C.2 The dialog prompts (authored by the implementer; assistant = Composer 2.5)

This revision was produced through a sequence of **six implementer-authored prompts** against the Composer 2.5 assistant, each operating against the running state of this repository and the previous prompt's output. The prompts are recorded verbatim (paraphrased here for brevity; full text lives in the originating chat transcript and in the prompt artifacts referenced by each PathwayRun below).

| # | Prompt summary | Outputs |
|---|---|---|
| **P1** | "Read [Authority Boundaries for AI] carefully and construct a one-page executive summary of how the Pathways architecture and framework can address what it describes, **especially** any serious gaps the article implies that are NOT satisfied by Pathways." Attaches `PATHWAYS_ARCHITECTURE.md` and `PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md`. | Initial executive summary draft (in-chat). |
| **P2** | "What is RIS? Please define it earlier in the report." | Revised report with RIS defined on first mention. |
| **P3** | "Please create the entire report as an MD file." | [`docs/PATHWAYS_AUTHORITY_BOUNDARIES_EXECUTIVE_SUMMARY.md`](docs/PATHWAYS_AUTHORITY_BOUNDARIES_EXECUTIVE_SUMMARY.md). |
| **P4** | "But can't Pathways encode constraints (policy, rules), and workflows for coming to determination under uncertainty? Real example: California alter ego law — *ownership alone is not dispositive*; this was discovered with AI, corrected via primary sources and multiple lawyers, and would be encoded as a business process in a multi-domain hypergraph." | New section *Encoding policy, rules, and determination workflows* added to the executive summary; alter-ego worked example anchored to subject-matter, registry-affiliation, and run-hypergraph graphs. |
| **P5** | "How could Pathways best implement: *matching gate strength to autonomy across three (or six) registers*?" | Design sketch: autonomy bands A0–A3, `gate_profile` manifest, `ToolGateway`, `HandoffBus`, three enforcement choke points, RIS conformance tests, phased rollout. |
| **P6** | "Edit the spec, and encode this entire process of updating the Pathways spec, itself as a Pathway, with the Greenwood article as origin and all previous prompts and outputs as steps. Make this the official revision to `PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md`, with the whole origin story and provenance resiliently encoded as a series of Pathways and PathwayRuns." | This appendix; §4.8; §13.7; glossary additions; bump to spec version 1.1.0. |
| **P7** | "Update the Pathways Architecture document to be coherent and compliant and compatible with the changes to the specification. Also encode this prompt as a Pathway update with PathwayRuns, so that there is evidence of the origin of updating the architecture document with Opus 4.7." | Architecture document revision 1.1.0 with §6.6, §9.8, §18.5, §20.12, the §4.11 data-model alignment block, and a new [`Pathways.Spec.ArchitectureAlign@v1`](PATHWAYS_ARCHITECTURE.md#a3-the-new-meta-pathway-template-pathwaysspecarchitecturealignv1) meta-pathway. Records the chain's first **assistant-model switch** — from Composer 2.5 (P1–P6) to Claude **Opus 4.7** (P7) — captured in `spec_self_provenance_json.assistant_model`. |

Prompts **P1–P6** ran against **Composer 2.5** (`composer-2.5-fast`). Prompt **P7** ran against **Claude Opus 4.7** (`claude-opus-4-7`). The assistant-model switch is itself a provenance fact, captured per-run in `spec_self_provenance_json.assistant_model` (RIS §C.4); the eight-prompt chain documents two assistants on the same lineage so future readers see both *who* (the implementer DID) and *what* (the model) shaped each step.

The seven prompts plus their assistant outputs are bound into the lineage as **`PathwayRunSource` rows** ([§4.7 of `PATHWAYS_ARCHITECTURE.md`](PATHWAYS_ARCHITECTURE.md#47-pathwayrunsourcetable--the-run-hypergraph)) with `role = "prompt"` linking each prompt artifact to the run it shaped.

### C.3 Meta-pathway templates (canonical seeds)

This revision **introduces** five meta-pathway templates into the canonical implementation's seed catalog. The first four (`SourceReview` / `GapAnalysis` / `RevisionDesign` / `RevisionApply`) are normative seeds for any implementation that wants to reproduce or extend the spec-revision discipline; the fifth (`ArchitectureAlign`) was introduced when prompt **P7** propagated this revision into the descriptive architecture document — its canonical YAML lives in [`PATHWAYS_ARCHITECTURE.md` §A.3](PATHWAYS_ARCHITECTURE.md#a3-the-new-meta-pathway-template-pathwaysspecarchitecturealignv1).

| Identity triple | Purpose | Targets |
|---|---|---|
| `Pathways.Spec.SourceReview@v1` | Read an external source against the current spec; produce a structured gap analysis. | RIS + architecture doc as read-only inputs |
| `Pathways.Spec.GapAnalysis@v1` | Refine the gap analysis into recommendations with conformance-level impact. | None (analysis only) |
| `Pathways.Spec.RevisionDesign@v1` | Translate recommendations into concrete normative section drafts, including conformance tests and glossary additions. | None (draft only) |
| `Pathways.Spec.RevisionApply@v1` | Apply the designed revision to the RIS file; bump spec version; emit AquaTree revision; produce a `RevisionAttestation`. | `PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md` (write) |
| `Pathways.Spec.ArchitectureAlign@v1` | Propagate a freshly applied RIS revision into the descriptive architecture document; bump architecture-doc revision; emit Aqua attestation paired with the RIS apply run. | `PATHWAYS_ARCHITECTURE.md` (write) |

All five templates ship with `gate_profile.escalation_rule = strict` and `default_autonomy = A1` (every output is reviewed by the implementer before commit). The `RevisionApply` template declares `non_delegable_acts = [publish_spec_revision]`; the `ArchitectureAlign` template declares `non_delegable_acts = [publish_architecture_revision]`. The acts of writing this appendix and of writing Appendix A of the architecture document are themselves non-delegable acts executed only after the implementer's explicit approval (P6 and P7 respectively).

Canonical YAML for the four RIS-update templates is in [§C.7](#c7-canonical-yaml-for-the-meta-pathway-templates) below; the `ArchitectureAlign@v1` template's YAML is in [`PATHWAYS_ARCHITECTURE.md` §A.3](PATHWAYS_ARCHITECTURE.md#a3-the-new-meta-pathway-template-pathwaysspecarchitecturealignv1) so that template definitions live next to the document each one governs.

### C.4 The PathwayRuns that produced revision 1.1.0

The run hypergraph for revision 1.1.0 is the following DAG. Run identifiers below are placeholders following the canonical `pr_<hex>` shape; concrete identifiers are minted at seeding time and recorded in the AquaTree. Runs `01..06` ran against **Composer 2.5** (`composer-2.5-fast`); run `07` (introduced when prompt P7 aligned the architecture document) ran against **Claude Opus 4.7** (`claude-opus-4-7`).

```text
                            +-------------------+
   Greenwood article  --P1-->|  pr_spec_rev_     |
   [doc:uploads/...]         |  20260520_01      |   Pathways.Spec.SourceReview@v1     (Composer 2.5)
                             |  source_review    |   → docs/PATHWAYS_AUTHORITY_BOUNDARIES_EXECUTIVE_SUMMARY.md (draft)
                             +-------------------+
                                      |
                                  P2 (RIS definition)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_02      |   Pathways.Spec.SourceReview@v1     (Composer 2.5)
                             |  ris_definition   |
                             +-------------------+
                                      |
                                  P3 (file emission)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_03      |   Pathways.Spec.SourceReview@v1     (Composer 2.5)
                             |  exec_summary_md  |   → docs/PATHWAYS_AUTHORITY_BOUNDARIES_EXECUTIVE_SUMMARY.md
                             +-------------------+
                                      |
                              P4 (policy correction)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_04      |   Pathways.Spec.GapAnalysis@v1      (Composer 2.5)
                             |  policy_anchor    |   → "Encoding policy, rules, and determination workflows"
                             +-------------------+
                                      |
                            P5 (gate-strength design)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_05      |   Pathways.Spec.RevisionDesign@v1   (Composer 2.5)
                             |  gate_design      |   → §4.8 + §13.7 + glossary drafts
                             +-------------------+
                                      |
                          P6 (apply to RIS — non-delegable)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_06      |   Pathways.Spec.RevisionApply@v1    (Composer 2.5)
                             |  revision_apply   |   → RIS 1.0.0 -> 1.1.0:
                             +-------------------+      §4.8, §13.7, glossary entries,
                                      |                 this Appendix C, AquaTree revision
                                      |
                  P7 (align architecture document — non-delegable; model switch)
                                      v
                             +-------------------+
                             |  pr_spec_rev_     |
                             |  20260520_07      |   Pathways.Spec.ArchitectureAlign@v1   (Opus 4.7)
                             |  architecture_    |   → PATHWAYS_ARCHITECTURE.md 1.0.0 -> 1.1.0:
                             |  align            |     §1 banner, §1.5 matrix rows, §4.11,
                             +-------------------+     §6.6, §8.2 note, §9.8, §17 layer 6,
                                                       §18.5, §19 alignment track, §20.12,
                                                       glossary additions, Appendix A
```

Each run row carries the following normative provenance fields (in addition to the standard `PathwayRun` fields from [§4.5](#45-run-structure)):

```yaml
spec_self_provenance:
  spec_doc_ref: "[doc:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md]"
  spec_version_before: "1.0.0"     # for runs 01..05; "1.0.0" through pre-apply
  spec_version_after: null         # set to "1.1.0" only on the apply run
  upstream_source_ref: "[doc:uploads/authority-boundaries-for-ai-0.md]"
  upstream_source_sha256: "<computed at seed time>"
  user_did: "did:key:z6Mk...djathomson"        # placeholder; replace with implementer DID
  assistant_model: "composer-2.5-fast"
  prompt_index: 1                  # 1..6 mapping to P1..P6 above
  prompt_artifact_ref: "[doc:legal-services-crew/audit/spec-rev-20260520/p1.md]"   # see §C.5
  output_artifact_ref: "[doc:legal-services-crew/audit/spec-rev-20260520/p1.out.md]"
```

The hypergraph linkage **MUST** be persisted with these `PathwayRunSource` edges:

| Child run | Predecessor | `role` |
|---|---|---|
| `pr_spec_rev_20260520_01` | `[doc:uploads/authority-boundaries-for-ai-0.md]` | `primary_source` |
| `pr_spec_rev_20260520_01` | `prompt_artifact:P1` | `prompt` |
| `pr_spec_rev_20260520_02` | `pr_spec_rev_20260520_01` | `context` |
| `pr_spec_rev_20260520_02` | `prompt_artifact:P2` | `prompt` |
| `pr_spec_rev_20260520_03` | `pr_spec_rev_20260520_02` | `context` |
| `pr_spec_rev_20260520_03` | `prompt_artifact:P3` | `prompt` |
| `pr_spec_rev_20260520_04` | `pr_spec_rev_20260520_03` | `context` |
| `pr_spec_rev_20260520_04` | `prompt_artifact:P4` | `prompt` |
| `pr_spec_rev_20260520_05` | `pr_spec_rev_20260520_04` | `subrun` |
| `pr_spec_rev_20260520_05` | `prompt_artifact:P5` | `prompt` |
| `pr_spec_rev_20260520_06` | `pr_spec_rev_20260520_05` | `subrun` |
| `pr_spec_rev_20260520_06` | `prompt_artifact:P6` | `prompt` |
| `pr_spec_rev_20260520_06` | (implicit) | `non_delegable_approval` |
| `pr_spec_rev_20260520_07` | `pr_spec_rev_20260520_06` | `subrun` |
| `pr_spec_rev_20260520_07` | `prompt_artifact:P7` | `prompt` |
| `pr_spec_rev_20260520_07` | `[doc:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md]` | `primary_source` |
| `pr_spec_rev_20260520_07` | `[doc:uploads/authority-boundaries-for-ai-0.md]` | `primary_source` |
| `pr_spec_rev_20260520_07` | (implicit) | `non_delegable_approval` |

The two new `PathwayRunSource.role` values introduced by this revision are:

- **`prompt`** — links a `prompt_artifact` (a stored human-authored prompt) to the run it shaped.
- **`non_delegable_approval`** — marks the human approval edge required by [§4.8.4 `non_delegable_acts`](#484-the-gate_profile-manifest) on the apply run.

Implementations honoring spec ≥ 1.1.0 **SHOULD** support these role values; runs lacking the required `non_delegable_approval` edge at apply time **MUST NOT** mutate the RIS.

### C.5 AquaTree binding for this revision

This revision's AquaTree manifest is bound as follows (Aqua sidecar is the canonical implementation; conformant implementations follow [§9.6 of `PATHWAYS_ARCHITECTURE.md`](PATHWAYS_ARCHITECTURE.md#96-aqua-protocol-attestations-shipped-mvp)).

```yaml
spec_revision_attestation:
  spec_doc: "legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md"
  spec_version_after: "1.1.0"
  spec_version_before: "1.0.0"
  revision_label: "authority-boundaries"
  revision_date: "2026-05-20"
  signed_by: "did:key:z6Mk...djathomson"
  aqua_tree:
    parent_revision: "<sha256 of RIS at 1.0.0>"
    new_revision:   "<sha256 of RIS at 1.1.0>"
    revision_kind: "spec_update"
  attached_runs:
    - pr_spec_rev_20260520_01
    - pr_spec_rev_20260520_02
    - pr_spec_rev_20260520_03
    - pr_spec_rev_20260520_04
    - pr_spec_rev_20260520_05
    - pr_spec_rev_20260520_06
  paired_architecture_doc_attestation:
    # Sibling attestation produced by P7 (Opus 4.7) — see PATHWAYS_ARCHITECTURE.md §A.5
    arch_doc: "legal-services-crew/PATHWAYS_ARCHITECTURE.md"
    arch_version_after: "1.1.0"
    apply_run: pr_spec_rev_20260520_07_architecture_align
  attached_artifacts:
    - "[doc:uploads/authority-boundaries-for-ai-0.md]"
    - "[doc:legal-services-crew/docs/PATHWAYS_AUTHORITY_BOUNDARIES_EXECUTIVE_SUMMARY.md]"
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p1.md]"     # P1 prompt text (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p2.md]"     # (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p3.md]"     # (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p4.md]"     # (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p5.md]"     # (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p6.md]"     # (Composer 2.5)
    - "[doc:legal-services-crew/audit/spec-rev-20260520/p7.md]"     # P7 prompt text (Opus 4.7)
  gate_profile_hash: "<sha256 of the gate_profile catalog for the 5 meta-pathway seeds>"
  conformance_addendum_ref: "#137-gate-profile-conformance-tests"
```

Implementations storing the prompt artifacts under `audit/spec-rev-20260520/` (recommended directory layout) **MUST** treat that directory as **append-only** for this revision; later spec revisions create sibling directories under `audit/spec-rev-<date>/`.

### C.6 Bootstrapping and replay

The intent of spec self-provenance is that **any future replay of this revision** can recover the same chain. A conformant Level-F+ implementation that ingests this RIS at version 1.1.0 **SHOULD**:

1. Seed the four RIS-update meta-pathway templates from [§C.7](#c7-canonical-yaml-for-the-meta-pathway-templates) into its template catalog with `is_system: true`. If it also ingests the canonical implementation's architecture document at version 1.1.0+, seed `Pathways.Spec.ArchitectureAlign@v1` from [`PATHWAYS_ARCHITECTURE.md` §A.3](PATHWAYS_ARCHITECTURE.md#a3-the-new-meta-pathway-template-pathwaysspecarchitecturealignv1) as well.
2. Seed the six RIS PathwayRun rows from [§C.4](#c4-the-pathwayruns-that-produced-revision-110) into its run history with `is_historical: true` and the `spec_self_provenance` block populated. Add the seventh run (`pr_spec_rev_20260520_07_architecture_align`) when ingesting the paired architecture-doc attestation from [`PATHWAYS_ARCHITECTURE.md` §A.4](PATHWAYS_ARCHITECTURE.md#a4-the-pathwayrun-for-this-revision).
3. Seed the `PathwayRunSource` edges from [§C.4](#c4-the-pathwayruns-that-produced-revision-110) (including the additional edges for run `07`).
4. Fetch and verify the originating source (`[doc:uploads/authority-boundaries-for-ai-0.md]`) against its recorded SHA-256.
5. Fetch and verify both AquaTree manifests — the RIS manifest from [§C.5](#c5-aquatree-binding-for-this-revision) and the paired architecture-doc manifest from [`PATHWAYS_ARCHITECTURE.md` §A.5](PATHWAYS_ARCHITECTURE.md#a5-aqua-attestation-for-this-architecture-doc-revision) — against the published parent and new revision hashes.

This is what *resilient encoding* means here: the **artifact** (this RIS file at 1.1.0 plus its sibling architecture document at 1.1.0) is self-describing, the **process** (six prompts against Composer 2.5 followed by one prompt against Claude Opus 4.7, anchored to one external source) is encoded as runnable templates, and the **lineage** (seven PathwayRuns spanning two sibling Aqua trees plus their hypergraph edges) is restorable from these two documents alone.

A future revision (call it 1.2.0) follows the same discipline: a new appendix block, new meta-pathway invocations using the same four templates (or fork them), new AquaTree revisions, new conformance addenda. The spec **always carries its own update history forward as Pathways**.

### C.7 Canonical YAML for the meta-pathway templates

The following YAML is the normative seed form for the four meta-pathway templates. Conformant implementations **MAY** translate to JSON, structured-prompt, or prose-narrative surface syntaxes per [§4.7](#47-template-round-trip) without semantic loss.

#### C.7.1 `Pathways.Spec.SourceReview@v1`

```yaml
domain: Pathways
subdomain: Spec
action: SourceReview
version: 1
display_name: "Review an external source against the current Pathways spec"
description: |
  Reads an external document (article, paper, repository) and produces a
  structured comparison against the current RIS and architecture: alignments,
  gaps, and candidate conformance-level impact. First step of every spec
  revision.

input_contract:
  source_ref:        { type: string, required: true,  description: "doc: pointer or URL" }
  source_sha256:     { type: string, required: false }
  spec_doc_ref:      { type: string, required: true,  default: "[doc:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md]" }
  architecture_ref:  { type: string, required: true,  default: "[doc:legal-services-crew/PATHWAYS_ARCHITECTURE.md]" }
  user_did:          { type: string, required: true }
  assistant_model:   { type: string, required: true,  default: "composer-2.5-fast" }

output_contract:
  type: structured_review
  format: markdown_plus_json
  required_sections: [thesis, alignments, gaps, conformance_impact, open_questions]

gate_profile:
  spec_version: "1.1.0"
  default_autonomy: A1
  max_autonomy: A1
  escalation_rule: strict
  registers:
    R1:
      enabled: true
      practice_profile_ref: "did:web:pathways/practice-profiles/spec-author@v1"
      output_contract_profile: "spec.review.v1"
      recoverable_error_bias: true
    R3:
      enabled: true
      handoff_schema: "spec.handoff.v1"
      allowed_targets: ["subrun:Pathways.Spec.GapAnalysis", "subrun:Pathways.Spec.RevisionDesign"]
  non_delegable_acts: []

steps:
  - agent_id: extraction
    order: 1
    skill: legal_references           # generic structured-extraction skill; not legal-specific
    phase: intake
    capability_profile:
      allow_tools: [read_document, grep, web_fetch]
      deny_tools: [write_*, send_*, mcp.*]
    input_prompt: "Extract the document's thesis, key claims, prescribed mechanisms, and explicit warnings."

  - agent_id: analysis
    order: 2
    skill: comparison
    phase: analysis
    capability_profile:
      allow_tools: [read_document]
      deny_tools: ["*"]
    inputs: [step_1.json]
    input_prompt: "Compare extracted claims to the current spec and architecture. Produce: alignments, gaps, conformance impact."

  - agent_id: prompt
    order: 3
    skill: structured_synthesis
    phase: delivery
    output_schema:
      type: object
      required: [thesis, alignments, gaps, conformance_impact, open_questions]
      properties:
        thesis:           { type: string }
        alignments:       { type: array, items: { type: object } }
        gaps:             { type: array, items: { type: object } }
        conformance_impact:
          type: object
          properties:
            level_S: { type: array, items: { type: string } }
            level_F: { type: array, items: { type: string } }
            level_R: { type: array, items: { type: string } }
        open_questions:   { type: array, items: { type: string } }
```

#### C.7.2 `Pathways.Spec.GapAnalysis@v1`

```yaml
domain: Pathways
subdomain: Spec
action: GapAnalysis
version: 1
display_name: "Refine source-review gaps into actionable spec recommendations"

input_contract:
  review_run_ref:    { type: string, required: true }
  correction_inputs: { type: array,  required: false, description: "Optional implementer corrections (e.g. policy-encoding clarifications)" }

output_contract:
  type: recommendations
  required_sections: [recommendations, level_impact, risks, conformance_test_sketches]

gate_profile:
  spec_version: "1.1.0"
  default_autonomy: A1
  escalation_rule: strict
  registers:
    R1: { enabled: true, practice_profile_ref: "did:web:pathways/practice-profiles/spec-author@v1" }
    R3: { enabled: true, handoff_schema: "spec.handoff.v1" }
  non_delegable_acts: []

steps:
  - agent_id: analysis
    order: 1
    skill: synthesize
    inputs: ["review_run.json.gaps", "review_run.json.conformance_impact"]
    input_prompt: "For each gap, propose a normative recommendation (MUST/SHOULD/MAY), an enforcement choke point, and a conformance-test sketch."

  - agent_id: prompt
    order: 2
    skill: structured_synthesis
    output_schema:
      type: object
      required: [recommendations, level_impact, risks, conformance_test_sketches]
```

#### C.7.3 `Pathways.Spec.RevisionDesign@v1`

```yaml
domain: Pathways
subdomain: Spec
action: RevisionDesign
version: 1
display_name: "Design the concrete spec revision: section drafts, conformance tests, glossary"

input_contract:
  gap_analysis_run_ref: { type: string, required: true }
  spec_doc_ref:         { type: string, required: true }

output_contract:
  type: revision_draft
  required_sections: [new_sections, modified_sections, conformance_tests, glossary_additions, version_bump]

gate_profile:
  spec_version: "1.1.0"
  default_autonomy: A1
  escalation_rule: strict
  registers:
    R1: { enabled: true, practice_profile_ref: "did:web:pathways/practice-profiles/spec-author@v1" }
  non_delegable_acts: []

steps:
  - agent_id: analysis
    order: 1
    skill: synthesize
    inputs: ["gap_analysis_run.json"]
    input_prompt: "Draft each recommended section in normative voice with MUST/SHOULD/MAY language; include subsection numbering."
  - agent_id: prompt
    order: 2
    skill: structured_synthesis
    output_schema:
      type: object
      required: [new_sections, modified_sections, conformance_tests, glossary_additions, version_bump]
```

#### C.7.4 `Pathways.Spec.RevisionApply@v1`

```yaml
domain: Pathways
subdomain: Spec
action: RevisionApply
version: 1
display_name: "Apply a designed spec revision to the RIS file; bump version; emit AquaTree revision"

input_contract:
  revision_design_run_ref: { type: string, required: true }
  spec_doc_ref:            { type: string, required: true }
  approver_did:            { type: string, required: true, description: "Must match a key authorized for spec_publish acts" }

output_contract:
  type: revision_attestation
  required_sections: [revision_label, version_after, version_before, aqua_revision, conformance_addendum_ref]

gate_profile:
  spec_version: "1.1.0"
  default_autonomy: A1
  max_autonomy: A1
  escalation_rule: strict
  registers:
    R1: { enabled: true, practice_profile_ref: "did:web:pathways/practice-profiles/spec-author@v1" }
    R3:
      enabled: true
      handoff_schema: "spec.apply.v1"
      allowed_targets: ["file:legal-services-crew/PATHWAYS_REFERENCE_IMPLEMENTATION_SPEC.md", "aqua:spec_update"]
    R5:
      enabled: true
      halt_channel: "run/{run_id}/halt"
  non_delegable_acts: [publish_spec_revision]

steps:
  - agent_id: prompt
    order: 1
    skill: structured_synthesis
    phase: intake
    capability_profile:
      allow_tools: [read_document]
      deny_tools: ["*"]
    input_prompt: "Read the revision design; emit the exact section-by-section edit plan."

  - agent_id: pathway
    order: 2
    skill: handoff
    phase: ethics_gate
    capability_profile:
      allow_tools: []
      allow_sub_pathways: []
    config:
      handoff_intent: request_human_approval
      handoff_target: "human_gate:approver_did"
    human_gate: required               # the non-delegable approval

  - agent_id: prompt
    order: 3
    skill: structured_synthesis
    phase: delivery
    capability_profile:
      allow_tools: [write_file]
      deny_tools: [send_*, browsing.*, mcp.*]
    input_prompt: "Apply the section-by-section edits to the RIS. Bump version. Emit revision attestation."

  - agent_id: prompt
    order: 4
    skill: aqua_attest
    phase: delivery
    capability_profile:
      allow_tools: [aqua_genesis, aqua_revision]
    input_prompt: "Append the spec_revision_attestation revision to the RIS AquaTree; bind attached runs and artifacts."
```

These four templates collectively are the **spec-revision pipeline**. They are seeded as `is_system: true` and bind to the practice profile `did:web:pathways/practice-profiles/spec-author@v1`, which lists the implementer DIDs authorized to perform the `publish_spec_revision` non-delegable act.

The act of producing **this** revision (1.1.0) was the **first invocation** of this pipeline against the live RIS, with this document as both the input (at 1.0.0) and the output (at 1.1.0). Subsequent revisions invoke the same templates with their own AquaTree revisions, each carrying forward a new Appendix-C-style block that extends — not replaces — the lineage recorded here.

---

**End of Pathways Reference Implementation Specification.**

This document is the seventh and final document in the Pathways design series. Together with the six prior strategy reports, it provides everything an independent implementer needs to build a conformant Pathways system, generate a genesis attestation, peer with trusted others, and participate in the organic emergent collaborative pathway exchange.

Variations are not just permitted — they are the intended outcome.

**Spec revisions** (as of 1.1.0) carry their own *why* and *how* as runnable, attestable Pathways — see [Appendix C](#appendix-c--spec-self-provenance-and-meta-pathways).
