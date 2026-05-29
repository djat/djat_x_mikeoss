#!/usr/bin/env python3
"""13_harden_v11.py - move the assay package from "designs toward" to CARRYING the
spec-1.1.0 Authority-Boundaries surface (§4.8). Authoring-level hardening only; adds no
executable engine. Three edits, all idempotent (full rewrites):

  1. Attach §4.8.4 gate_profile manifests:
       - Assay.Citation.VerifyFirst       -> A0, register R1
       - Assay.Convergence.AnchoredAuthority -> A1, registers R1 + R4 + R5 + R6
  2. Add a §4.8.5 practice profile so the R1 cold-start gate resolves out of the box.
  3. Promote Assay.Provenance.RunManifest to the §4.8.6 attested-run record
     (effective gate_profile + autonomy band) and add the §4.8.7 R3 handoff envelope.

Plus PACKAGE/index metadata declaring exactly which spec features are now used, and a
new technique template Collaboration.Refactor.HardenGateProfile@v1.

Producing pathway: Collaboration.Refactor.HardenGateProfile@v1
Stdlib only. No network. No names. DIDs are generic placeholders (did:web:pathways.example).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
ASSAY = SNAP / "assay-pathways"
SPEC_SHA = "1588cda3f28fc8c22007ab05cad4231b1212444f2d0c2a1b404e9603ac6c75cc"
PP_REF = "did:web:pathways.example/playbook/legal-research-grounding@v1"
PP_DID = "did:web:pathways.example"

VERIFY_FIRST = """# Assay.Citation.VerifyFirst@v1

pathway_template:
  identity:
    template_id: Assay.Citation.VerifyFirst@v1
    artifact_type: pathway-template
    triple: { domain: Assay, subdomain: Citation, action: VerifyFirst }
    version: 1.1.0

  description: |
    The honest counterpart to "Legal Research 271.5%". A deterministic grounding gate
    runs BEFORE any model speaks: every citation is checked against the public
    legal-data commons (Free Law Project / CourtListener, Cornell LII, GovInfo).
    Hallucinated citations are caught by math, not vibes. The model is reserved for a
    bounded support check on already-verified authorities. STUB - no executable code.

  inputs:
    - name: document
      type: path
    - name: authorities
      type: list
      description: Citations extracted from the document (typed)

  steps:
    - id: extract_authorities
      agent_id: extraction
      skill: legal_references
      config:
        typed: true

    - id: deterministic_verify
      agent_id: verification
      skill: database_verification
      config:
        provider_order: [courtlistener, cornell_lii, govinfo]
        model_provider: deterministic
        emit: { statuses: [verified, warning, not_found], field_level_diagnostics: true }

    - id: bounded_support_check
      agent_id: analysis
      skill: support_check
      config:
        only_on: verified
        constraint: "Use only the retrieved verbatim opinion text. Never invent quotations."

    - id: fallback_links
      agent_id: composer
      skill: emit_fallback_links
      config:
        when: [warning, not_found]
        targets: [scholar, lii, courtlistener]

  output:
    artifact: verification_report
    includes: [verdicts, citations, fallback_links]

  ethos:
    principle: deterministic-grounding-over-latent-recall
    commons: [free_law_project, cornell_lii, govinfo]

  # Spec 1.1.0 §4.8 - authority-boundary manifest. A0 (Assisted): a licensed human reads
  # every verification report before any external effect; the only required register is R1.
  gate_profile:
    spec_version: "1.1.0"
    default_autonomy: A0
    max_autonomy: A1
    escalation_rule: strict
    registers:
      R1:
        enabled: true
        practice_profile_ref: "%PP_REF%"
        output_contract_profile: "assay.verification.v1"
        recoverable_error_bias: true   # warning/not_found surface fallback links; never fabricate
    non_delegable_acts: [sign, file, send_external, certify]
    attestation:
      signed_by: "%PP_DID%"
      note: "Self-asserted placeholder for the donation. Re-sign under tenant counsel DID on adoption."
""".replace("%PP_REF%", PP_REF).replace("%PP_DID%", PP_DID)

ANCHORED = """# Assay.Convergence.AnchoredAuthority@v1

pathway_template:
  identity:
    template_id: Assay.Convergence.AnchoredAuthority@v1
    artifact_type: pathway-template
    triple: { domain: Assay, subdomain: Convergence, action: AnchoredAuthority }
    version: 1.1.0

  description: |
    "Recursive agentic orchestration" read as truth: a BOUNDED convergence loop. Run a
    first-pass multi-model analysis; compare its citations to a concentrated public
    canonical-consensus oracle (CourtListener clusters / opinion text, Cornell LII,
    GovInfo). If typed category error exceeds a threshold, re-enter with the oracle
    PRE-INJECTED as pinned authority and a hard instruction: never use latent/parametric
    recall for case references - answer only from the anchored authority; if a reference
    is not in the anchor, return not_found + a fallback link. Each iteration is attested;
    grounding is monotonic; depth and budget are bounded. STUB - no executable code.

  inputs:
    - name: document
      type: path
    - name: threshold
      type: dict
      default: { not_found_max: 0, warning_max: 1 }
    - name: max_depth
      type: int
      default: 3
    - name: budget
      type: dict
      description: economic + temporal bounds per loop

  steps:
    - id: first_pass
      agent_id: pathway
      invokes:
        - Assay.Citation.VerifyFirst

    - id: evaluate_typed_error
      agent_id: verification
      skill: typed_error_predicate
      config:
        over: verdicts
        statuses: [verified, warning, not_found]

    - id: anchored_reentry
      agent_id: pathway
      skill: reenter_with_anchored_authority
      config:
        when: "typed_error > threshold and depth < max_depth"
        inject: concentrated_public_consensus_context
        hard_constraint: "Answer ONLY from anchored authority; never from latent space."
        monotonic_grounding: true

    - id: converge_or_halt
      agent_id: verification
      skill: convergence_predicate
      config:
        stop_when: "typed_error <= threshold OR depth == max_depth OR budget exhausted"

    - id: attest_each_iteration
      agent_id: persist
      skill: attest_iteration
      config:
        one_record_per_loop: true

  output:
    artifact: converged_verification
    includes: [final_verdicts, iteration_attestations, convergence_trace]

  notes:
    meta_technique: true
    composes_with: [Assay.Citation.VerifyFirst, Assay.Provenance.RunManifest]
    invariant: "Each iteration may only narrow toward the anchor; latent recall is never re-opened."

  # Spec 1.1.0 §4.8 - A1 (Supervised async): a human approves the converged verdict before
  # it leaves the loop. Minimum registers for A1 are R1 + R6; this profile ALSO enables
  # R4 + R5 because the loop already encodes economic + temporal bounds (budget, max_depth,
  # halt). Declaring them makes those bounds engine-enforceable, not just prose.
  gate_profile:
    spec_version: "1.1.0"
    default_autonomy: A1
    max_autonomy: A2
    escalation_rule: strict
    registers:
      R1:
        enabled: true
        practice_profile_ref: "%PP_REF%"
        output_contract_profile: "assay.converged_verification.v1"
        recoverable_error_bias: true
      R4:
        enabled: true
        max_usd: 5.00
        max_tokens: 200000
      R5:
        enabled: true
        halt_channel: "run/{run_id}/halt"
        idle_ttl_seconds: 300
      R6:
        enabled: true
        phases: [first_pass, evaluate_typed_error, anchored_reentry, converge_or_halt, attest_each_iteration]
        phase_defaults:
          anchored_reentry:
            human_gate: not_required    # bounded + monotonic; latent recall forbidden
          converge_or_halt:
            human_gate: required        # human approves converged verdict (A1 commit gate)
    non_delegable_acts: [sign, file, send_external, certify]
    attestation:
      signed_by: "%PP_DID%"
      note: "Self-asserted placeholder for the donation. Re-sign under tenant counsel DID on adoption."
""".replace("%PP_REF%", PP_REF).replace("%PP_DID%", PP_DID)

RUN_MANIFEST = """# Assay.Provenance.RunManifest@v1

pathway_template:
  identity:
    template_id: Assay.Provenance.RunManifest@v1
    artifact_type: pathway-template
    triple: { domain: Assay, subdomain: Provenance, action: RunManifest }
    version: 1.1.0

  description: |
    The minimal attested-run schema any tool - including a Supabase-backed one like
    MikeOSS - could emit. It makes the difference between "who ran / who attested /
    who authored" visible, which is the structural assay to a panel "consisting
    entirely of MikeOSS". v1.1.0 promotes the schema to the attested-run record the
    spec's choke-point audit (§4.8.6) expects: it persists the run's effective autonomy
    band + gate_profile, and carries a typed handoff envelope (§4.8.7 R3) that a
    HandoffBus can validate at the seam. STUB - no executable code; the schemas are the
    artifact.

  inputs:
    - name: run
      type: dict

  # §4.8.1: every PathwayRun MUST carry an autonomy band. §4.8.6: runs MUST persist the
  # effective gate_profile and the practice-profile revision that shaped the work.
  run_manifest_schema:
    run_id: string
    timestamp: iso8601
    autonomy: "A0|A1|A2|A3"            # NEW (spec 1.1.0 §4.8.1) - rejected if absent/unknown
    actor:
      ran_by: string            # human / org
      model: { provider: string, name: string, version: string }
      attested_by: string       # may differ from ran_by
      authored_by: string       # may differ from both
    effective_gate_profile:     # NEW (spec 1.1.0 §4.8.6) - what the run was launched with
      gate_profile_sha256: hex
      autonomy: "A0|A1|A2|A3"
      registers_enabled: ["R1"]
      practice_profile_ref: "did:web|did:key ... @version"
      practice_profile_revision_sha256: hex
    inputs:
      prompt_sha256: hex
      document_sha256: hex
    outputs:
      output_sha256: hex
    grounding:
      sources: [courtlistener, cornell_lii, govinfo]
      verdicts: [{ citation: string, status: "verified|warning|not_found", source_url: string }]
    handoff_audit:              # NEW (spec 1.1.0 §4.8.7 R3) - append-only seam log
      - { seam: string, intent: string, target: string, decision: "accepted|rejected|neutralized", at: iso8601 }
    signature:
      method: "ed25519 (optional)"
      public_key_pem: string
      signature_base64: string

  # §4.8.7 R3 - the typed envelope a HandoffBus validates at every seam: closed intent
  # enum + JSONSchema params + target allowlist. Downstream NEVER sees upstream free text
  # as steering; steering is template-rendered; the audit is append-only.
  handoff_envelope_schema:
    intent: { enum: [verify_citation, support_check, emit_fallback, attest_iteration] }
    params: { json_schema_ref: "assay.handoff.params.v1" }
    target: { allowlist: ["subrun:Assay.*", "store:proof-results/*"] }
    steering_source: template-rendered
    audit: append-only

  steps:
    - id: assemble_manifest
      agent_id: persist
      skill: write_run_manifest
      config:
        target: proof-results/run-manifests/<run_id>.json
        persist_effective_gate_profile: true   # §4.8.6 enforcement-record requirement

  output:
    artifact: run_manifest
    interop_note: "One page; emit from any stack. Validates interoperability even if unanswered."
    choke_point_note: "Carries the fields the launch/seam choke points (§4.8.6) record, so a Level-F runtime can audit this run without bespoke glue."
"""

PRACTICE_PROFILE = """# Practice profile (registry node) - spec 1.1.0 §4.8.5 (R1 cold-start)
#
# A practice profile is the Pathways analog of the article's CLAUDE.md practice file:
# tenant-scoped institutional rules the engine MUST resolve before launching any template
# whose gate_profile.R1.enabled = true. If it does not resolve, the run is
# BLOCKED_CONFIGURATION (it never starts). This stub ships so the assay templates' R1 refs
# resolve out of the box; on adoption, replace it with a counsel-signed profile.

practice_profile:
  kind: practice_profile          # registry node kind (Level-F+)
  slug: legal-research-grounding
  version: "1.0.0"
  ref: "%PP_REF%"
  signed_by: "%PP_DID%"           # placeholder; re-sign under supervising-counsel DID
  self_asserted: true
  spec: { reference: "canon/PATHWAYS_REFERENCE_v1.1.0.md", section: "4.8.5", version: "1.1.0", reference_sha256: "%SPEC_SHA%" }

  jurisdictional_posture:
    default: "US federal + state; cite only retrievable authority"
    unknown_jurisdiction: escalate

  escalation_thresholds:
    not_found_citations: { max: 0, on_exceed: block_delivery }
    warning_citations:   { max: 1, on_exceed: human_review }

  institutional_rules:
    - "Never present a case citation that was not retrieved from the public legal-data commons."
    - "On any unverifiable authority, emit a fallback link; never paraphrase a holding from latent recall."
    - "A verification report is agent-lane work; the legal determination remains lawyer-lane."

  anti_patterns:                  # forkable annotations (§4.8.5); referenced via narrative pointers
    - id: latent-citation
      note: "Citing from parametric memory instead of retrieved authority. The primary failure the Elite MegaLaw satire mocks."
    - id: confident-not-found
      note: "Returning fluent prose where a citation could not be verified, instead of a fallback link."

  revision_history:               # Aqua-attested in a Level-F deployment; stub here
    - { version: "1.0.0", at: "2026-05-28", note: "Initial donation stub.", revision_sha256: "<computed-on-adoption>" }
""".replace("%PP_REF%", PP_REF).replace("%PP_DID%", PP_DID).replace("%SPEC_SHA%", SPEC_SHA)

PACKAGE = """# Assay Pathways - packaging manifest

bundle_id: assay-pathways
version: "1.1.0"
title: "Assay Pathways (legal AI trustworthiness)"
description: >
  A starting vocabulary - not a product - for the assay to legal-AI benchmark
  theater: verify-first deterministic grounding, reproducible attested benchmarking,
  bounded anchored-authority convergence (recursion read as truth), and a minimal
  attested run-manifest schema. Stubs only; no executable code. Owned by neither
  project; built on the public legal-data commons.

# What THIS code-free package ships is Level M. But its templates now carry full §4.8.4
# gate_profile manifests + an §4.8.5 practice profile + an §4.8.6 attested-run schema, so
# any Level-F runtime (a future MikeOSS node included) can ENFORCE them verbatim at
# autonomy >= A1. We declare the AUTHORING level, not a runtime conformance claim.
conformance_target_default: M
contains_code: false
gate_profile_manifests: present
gate_profile_target_level: F
spec_features_used:
  - feature: "§4.8 autonomy bands + gate_profile manifests"
    where: ["pathways/Assay.Citation.VerifyFirst.v1.yaml (A0/R1)", "pathways/Assay.Convergence.AnchoredAuthority.v1.yaml (A1/R1+R4+R5+R6)"]
  - feature: "§4.8.5 practice profile (R1 cold-start)"
    where: ["practice-profiles/legal-research-grounding.v1.yaml"]
  - feature: "§4.8.6 effective gate_profile + §4.8.7 R3 handoff envelope"
    where: ["pathways/Assay.Provenance.RunManifest.v1.yaml"]
reference_spec: ../canon/PATHWAYS_REFERENCE_v1.1.0.md
reference_spec_sha256: %SPEC_SHA%

primary_artifact: APPLICATION_PLAYBOOK.md
pathways_index: pathways-index.yaml

commons:
  - free_law_project_courtlistener
  - cornell_lii
  - govinfo

ethos_principles:
  - reproducibility
  - deterministic_grounding_over_latent_recall
  - no_inflated_metrics
  - attribution
  - legible_methodology
  - explicit_human_judgment_boundaries

files:
  - APPLICATION_PLAYBOOK.md
  - PACKAGE.yaml
  - pathways-index.yaml
  - pathways/Assay.Citation.VerifyFirst.v1.yaml
  - pathways/Assay.Benchmark.Reproducible.v1.yaml
  - pathways/Assay.Convergence.AnchoredAuthority.v1.yaml
  - pathways/Assay.Provenance.RunManifest.v1.yaml
  - practice-profiles/legal-research-grounding.v1.yaml

license_terms:
  fork: true
  attribution_required: true
  revocation_scope_max: self_only
""".replace("%SPEC_SHA%", SPEC_SHA)

INDEX = """bundle_id: assay-pathways
version: "1.1.0"
filesystem_root: assay-pathways/

pathways:
  - id: Assay.Citation.VerifyFirst
    file: pathways/Assay.Citation.VerifyFirst.v1.yaml
    answers_satire: "Legal Research / Citation pass rates"
    autonomy: A0
    gate_profile_registers: [R1]
    invokes: []

  - id: Assay.Benchmark.Reproducible
    file: pathways/Assay.Benchmark.Reproducible.v1.yaml
    answers_satire: "chart smoothing / decimal optimisation / scores above 100%"
    invokes: []

  - id: Assay.Convergence.AnchoredAuthority
    file: pathways/Assay.Convergence.AnchoredAuthority.v1.yaml
    answers_satire: "recursive agentic orchestration"
    autonomy: A1
    gate_profile_registers: [R1, R4, R5, R6]
    invokes:
      - Assay.Citation.VerifyFirst
      - Assay.Provenance.RunManifest

  - id: Assay.Provenance.RunManifest
    file: pathways/Assay.Provenance.RunManifest.v1.yaml
    answers_satire: "a panel consisting entirely of MikeOSS"
    emits: [autonomy, effective_gate_profile, handoff_envelope]
    invokes: []

practice_profiles:
  - kind: practice_profile
    slug: legal-research-grounding
    version: "1.0.0"
    ref: "%PP_REF%"
    file: practice-profiles/legal-research-grounding.v1.yaml
    satisfies: "§4.8.5 R1 cold-start for VerifyFirst + AnchoredAuthority"
""".replace("%PP_REF%", PP_REF)

HARDEN_TEMPLATE = """# Collaboration.Refactor.HardenGateProfile@v1

pathway_template:
  identity:
    template_id: Collaboration.Refactor.HardenGateProfile@v1
    artifact_type: pathway-template
    triple: { domain: Collaboration, subdomain: Refactor, action: HardenGateProfile }
    version: 1.0.0

  description: |
    Provenanced technique for moving a code-free Pathways package from "designs toward"
    the spec-1.1.0 Authority-Boundaries surface to formally CARRYING it: attach §4.8.4
    gate_profile manifests (autonomy band + registers) to templates, add a §4.8.5
    practice profile so the R1 cold-start gate resolves, and promote the run-manifest to
    the §4.8.6 attested-run record (+ §4.8.7 R3 handoff envelope). Authoring-level
    hardening only - adds no executable engine; a Level-F runtime can then enforce the
    declared profiles verbatim.

  inputs:
    - name: target_package
      type: path
    - name: practice_profile_ref
      type: string

  steps:
    - id: declare_gate_profiles
      agent_id: pathway
      skill: attach_gate_profile_manifest
      config:
        per_template_autonomy: true
        escalation_rule: strict
    - id: add_practice_profile
      agent_id: persist
      skill: write_practice_profile
      config:
        kind: practice_profile
        cold_start_gate: true
    - id: promote_run_manifest
      agent_id: pathway
      skill: promote_attested_run_schema
      config:
        persist_effective_gate_profile: true
        add_handoff_envelope: true
    - id: record_provenance
      agent_id: persist
      invokes: [Collaboration.Attestation.RecordPathwayRun]

  output:
    artifact: hardened_package
    includes: [gate_profiles, practice_profile, attested_run_schema]

  notes:
    spec_alignment: "Greenwood Authority Boundaries -> spec 1.1.0 §4.8; this template makes a package carry, not merely gesture at, the registers."
    contains_code: false
"""


def write(rel: str, text: str) -> str:
    p = Path(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"wrote {rel}")
    return rel


def main() -> int:
    produced = [
        write(str(ASSAY / "pathways" / "Assay.Citation.VerifyFirst.v1.yaml"), VERIFY_FIRST),
        write(str(ASSAY / "pathways" / "Assay.Convergence.AnchoredAuthority.v1.yaml"), ANCHORED),
        write(str(ASSAY / "pathways" / "Assay.Provenance.RunManifest.v1.yaml"), RUN_MANIFEST),
        write(str(ASSAY / "practice-profiles" / "legal-research-grounding.v1.yaml"), PRACTICE_PROFILE),
        write(str(ASSAY / "PACKAGE.yaml"), PACKAGE),
        write(str(ASSAY / "pathways-index.yaml"), INDEX),
        write(str(SNAP / "collaboration-pathways" / "pathways" / "Collaboration.Refactor.HardenGateProfile.v1.yaml"), HARDEN_TEMPLATE),
        str(SNAP / "collaboration-pathways" / "scripts" / "13_harden_v11.py"),
    ]

    manifest = os.environ.get("ASSET_MANIFEST")
    if manifest:
        Path(manifest).write_text(json.dumps(produced), encoding="utf-8")
    print(f"hardening complete: {len(produced)} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
