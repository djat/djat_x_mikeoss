#!/usr/bin/env python3
"""10_assay_terms.py - register the domain rename as Term artifacts (recorded run).

Producing pathway: Collaboration.Naming.RegisterTerm@v1. Records that "assay" supersedes the
prior "anti-venom" framing, keeping the prior term as a freely licensable artifact (name-as-
artifact discipline). Written after the rename, so Term.AntiVenom retains the literal prior label.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
TERMS = SNAP / "collaboration-pathways" / "terms"
MANIFEST = SNAP / "collaboration-manifest.yaml"

TERM_ASSAY = """# Term.Assay@v1
term:
  identity:
    term_id: Term.Assay@v1
    artifact_type: term
    label: "assay (pathways)"
    version: 1.0.0
  authored_by: "Originator (DJ Thomson)"
  authored_in: collaboration/20260528-130500
  supersedes: Term.AntiVenom@v1
  meaning: >
    The domain name for the legal-AI trustworthiness pathways. An assay is a precise test of what
    something is genuinely made of - an assayer certifies the true composition of a metal. Chosen
    to replace the prior oppositional/medical framing with a positive, constructive one.
  name_license:
    use_as_label: free
    attribution_required: true
    revocation_scope_max: self_only
"""

# Written post-rename and not subject to the rename pass, so it retains the literal prior label.
TERM_PRIOR = """# Term.AntiVenom@v1
term:
  identity:
    term_id: Term.AntiVenom@v1
    artifact_type: term
    label: "anti-venom"
    version: 1.0.0
  status: prior-term (superseded, retained as lineage)
  superseded_by: Term.Assay@v1
  meaning: >
    The original framing for the trustworthiness pathways - the "antidote" to benchmark-theater
    "venom". Oppositional/medical; replaced by "assay". Retained for lineage and offered as a
    freely licensable label for anyone who prefers it.
  name_license:
    use_as_label: free
    attribution_required: true
    revocation_scope_max: self_only
"""

MANIFEST_BLOCK = """
# ---------------------------------------------------------------------------
# DOMAIN NAME PROVENANCE (the assay pathways; renamed from "anti-venom")
# ---------------------------------------------------------------------------
domain_name_provenance:
  default_term: Term.Assay@v1
  terms:
    - collaboration-pathways/terms/Term.Assay.v1.yaml
    - collaboration-pathways/terms/Term.AntiVenom.v1.yaml
  supersession:
    new: Term.Assay@v1
    prior: Term.AntiVenom@v1
    scope: name_only
    license: free
  pattern: Pattern.Naming.ProvenancedTermBinding
  note: >
    The pathway recipes (verify-first grounding, reproducible benchmark, anchored-authority
    convergence, run-manifest) are unchanged; only the domain label changed. The prior term is
    retained and freely licensable.
"""


def main() -> int:
    TERMS.mkdir(parents=True, exist_ok=True)
    (TERMS / "Term.Assay.v1.yaml").write_text(TERM_ASSAY, encoding="utf-8")
    (TERMS / "Term.AntiVenom.v1.yaml").write_text(TERM_PRIOR, encoding="utf-8")
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(MANIFEST_BLOCK)
    print("assay terms: Term.Assay@v1 supersedes Term.AntiVenom@v1; manifest domain_name_provenance written")
    produced = [
        str(TERMS / "Term.Assay.v1.yaml"),
        str(TERMS / "Term.AntiVenom.v1.yaml"),
        str(MANIFEST),
        f"{SNAP}/collaboration-pathways/scripts/10_assay_terms.py",
    ]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
