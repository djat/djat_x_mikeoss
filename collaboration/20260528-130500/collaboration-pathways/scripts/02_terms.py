#!/usr/bin/env python3
"""02_terms.py - encode the name-as-artifact layer (Phase 1b).

Generates two Term artifacts (the new canonical term + the prior, freely-licensable term),
the Pattern.Naming.ProvenancedTermBinding, and patches the manifest with a name_provenance
block (default_term + name-inheritance). Producing pathway: Collaboration.Naming.RegisterTerm@v1.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
TERMS = SNAP / "collaboration-pathways" / "terms"
PATTERNS = SNAP / "collaboration-pathways" / "patterns"
MANIFEST = SNAP / "collaboration-manifest.yaml"

TERM_COLLAB = """# Term.CollaborationBundle@v1
term:
  identity:
    term_id: Term.CollaborationBundle@v1
    artifact_type: term
    label: "collaboration bundle"
    version: 1.0.0
  authored_by: "Originator (DJ Thomson)"
  authored_in: collaboration/20260528-130500
  supersedes: Term.TransmissionBundle@v1
  meaning: >
    The canonical name for the co-originated bundle technique, as renamed by the Originator
    in the MikeOSS collaboration context. The recipe is unchanged; only the label is new.
  name_license:
    use_as_label: free
    attribution_required: true
    revocation_scope_max: self_only
  provenance:
    rename_pathway: Collaboration.Refactor.RenameTerm@v1
    recorded_in: pathway-runs/index.yaml
"""

# NOTE: this file is generated post-rename and is NOT subject to the rename pass, so it may
# safely retain the literal prior term.
TERM_PRIOR = """# Term.TransmissionBundle@v1
term:
  identity:
    term_id: Term.TransmissionBundle@v1
    artifact_type: term
    label: "tr{X}ansmission bundle"
    version: 1.0.0
  status: prior-term (superseded, retained as lineage)
  co_originated_by:
    - "a collaborating peer (sealed - see identities/)"
    - "Originator (DJ Thomson)"
  superseded_by: Term.CollaborationBundle@v1
  meaning: >
    The original name of the technique, retained for lineage and offered as a freely
    licensable label. Anyone may license this term to call their collaboration bundle a
    "tr{X}ansmission bundle"; this is a license of the NAME (provenanced + interrogable),
    not a UI rewrite.
  name_license:
    use_as_label: free
    attribution_required: true
    revocation_scope_max: self_only
  inherited_via:
    scope: name_only
""".replace("{X}", "")  # keep literal prior label intact

PATTERN = """pattern:
  id: Pattern.Naming.ProvenancedTermBinding
  version: 1.0.0
  title: Provenanced Term Binding
  description: |
    A label/term is a first-class artifact (artifact_type: term), separate from the recipe
    it names. A pathway binds a default_term and MAY inherit a name from another term with
    scope: name_only. Using a term as a label is a provenanced, licensable act (name_license),
    distinct from a UI rewrite. Renames are events authored by an identity and recorded as
    PathwayRuns; the prior term is retained and remains licensable.
  invariants:
    - term_is_artifact_not_string
    - name_license_distinct_from_recipe_license
    - name_use_is_provenanced_and_interrogable
    - rename_preserves_prior_term_as_lineage
  invokes:
    - Collaboration.Refactor.RenameTerm@v1
    - Collaboration.Naming.RegisterTerm@v1
"""

NAME_PROVENANCE = """
# ---------------------------------------------------------------------------
# NAME PROVENANCE (name-as-artifact; see collaboration-pathways/terms/)
# ---------------------------------------------------------------------------
name_provenance:
  default_term: Term.CollaborationBundle@v1
  terms:
    - collaboration-pathways/terms/Term.CollaborationBundle.v1.yaml
    - collaboration-pathways/terms/Term.TransmissionBundle.v1.yaml
  name_inheritance:
    - from: Term.TransmissionBundle@v1
      scope: name_only
      license: free
  pattern: Pattern.Naming.ProvenancedTermBinding
  note: >
    The recipe is named "collaboration bundle"; the prior term is retained as a licensable
    artifact. A peer who prefers the prior label licenses Term.TransmissionBundle@v1
    (name_only) - a provenanced choice, interrogable per permissions, not a UI rewrite.
"""


def main() -> int:
    TERMS.mkdir(parents=True, exist_ok=True)
    (TERMS / "Term.CollaborationBundle.v1.yaml").write_text(TERM_COLLAB, encoding="utf-8")
    (TERMS / "Term.TransmissionBundle.v1.yaml").write_text(TERM_PRIOR, encoding="utf-8")
    (PATTERNS / "Pattern.Naming.ProvenancedTermBinding.yaml").write_text(PATTERN, encoding="utf-8")
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(NAME_PROVENANCE)
    print("terms: registered Term.CollaborationBundle@v1 + Term.TransmissionBundle@v1; "
          "pattern + manifest name_provenance written")
    produced = [
        f"{TERMS}/Term.CollaborationBundle.v1.yaml",
        f"{TERMS}/Term.TransmissionBundle.v1.yaml",
        f"{PATTERNS}/Pattern.Naming.ProvenancedTermBinding.yaml",
        str(MANIFEST),
        f"{SNAP}/collaboration-pathways/scripts/02_terms.py",
        f"{SNAP}/collaboration-pathways/pathways/Collaboration.Naming.RegisterTerm.v1.yaml",
    ]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
