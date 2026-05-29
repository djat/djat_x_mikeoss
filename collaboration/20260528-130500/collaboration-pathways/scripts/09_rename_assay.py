#!/usr/bin/env python3
"""09_rename_assay.py - rename the "anti-venom" framing to "assay" (recorded run).

Producing pathway: Collaboration.Refactor.RenameTerm@v1. Token-swaps AntiVenom/anti-venom ->
Assay/assay across the snapshot (excluding immutable run records, regenerated attestations, and
scripts), softens the residual venom/antidote metaphor into the assay framing, renames the
directory + four pathway files + the thesis sidecar + the timeline event, and injects a one-line
definition of "assay" at first use in the reader-facing files. The prior term "anti-venom" is
retained as a licensable Term in a separate step (10_assay_terms.py). The literal old tokens in
THIS script + its run record are the legitimate provenance of the rename.
"""
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
EXCLUDE = {"pathway-runs", "attestations", "scripts", ".git", ".obsidian"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".html"}

TOKENS = [
    ("AntiVenom.", "Assay."),
    ("antivenom-pathways", "assay-pathways"),
    ("anti-venom-thesis", "assay-thesis"),
    ("Anti-Venom", "Assay"),
    ("Anti-venom", "Assay"),
    ("AntiVenom", "Assay"),
    ("anti-venom", "assay"),
    ("antivenom", "assay"),
]
RESIDUE = [
    ("co-create the genuine **assay** to the very thing the satire has already begun to alchemize.",
     "co-create the genuine **assay** the satire only performs - a rigorous test of what a legal-AI claim is really made of."),
    ("The antidote is not a better marketing department", "The assay is not a better marketing department"),
    ("The antidote is not a better story", "The assay is not a better story"),
    ("If the antidote to benchmark theater were proprietary", "If the assay for benchmark theater were proprietary"),
    ("the proposed antidote", "the proposed assay"),
    ("antidote", "assay"),
]

ASSAY_DEF = (
    "\n> **Assay** - a precise test of what something is genuinely made of; an *assayer* "
    "certifies the true composition of a metal. Here, the *assay pathways* test what a legal-AI "
    "claim is really made of - grounded citations, reproducible scores, attested runs: the honest "
    "measurement the satire only performs.\n"
)
GLOSS_ANCHORS = {
    str(SNAP / "collaboration-spine.md"): "## 3. The assay thesis",
    str(SNAP / "sidecars" / "assay-thesis.md"): "# Sidecar - The assay thesis (depth)",
    str(SNAP / "assay-pathways" / "APPLICATION_PLAYBOOK.md"): "# Assay Pathways - Application Playbook",
}

FILE_RENAMES_INNER = [
    (f"{SNAP}/antivenom-pathways/pathways/AntiVenom.Citation.VerifyFirst.v1.yaml",
     f"{SNAP}/antivenom-pathways/pathways/Assay.Citation.VerifyFirst.v1.yaml"),
    (f"{SNAP}/antivenom-pathways/pathways/AntiVenom.Benchmark.Reproducible.v1.yaml",
     f"{SNAP}/antivenom-pathways/pathways/Assay.Benchmark.Reproducible.v1.yaml"),
    (f"{SNAP}/antivenom-pathways/pathways/AntiVenom.Convergence.AnchoredAuthority.v1.yaml",
     f"{SNAP}/antivenom-pathways/pathways/Assay.Convergence.AnchoredAuthority.v1.yaml"),
    (f"{SNAP}/antivenom-pathways/pathways/AntiVenom.Provenance.RunManifest.v1.yaml",
     f"{SNAP}/antivenom-pathways/pathways/Assay.Provenance.RunManifest.v1.yaml"),
]


def excluded(p: Path) -> bool:
    return any(x in EXCLUDE for x in p.parts)


def main() -> int:
    changed = []
    for p in SNAP.rglob("*"):
        if not p.is_file() or excluded(p) or p.suffix not in TEXT_EXT:
            continue
        orig = p.read_text(encoding="utf-8")
        t = orig
        for a, b in TOKENS:
            t = t.replace(a, b)
        for a, b in RESIDUE:
            t = t.replace(a, b)
        if t != orig:
            p.write_text(t, encoding="utf-8")
            changed.append(str(p))

    # Inner pathway-file renames, then the directory, then sidecar + timeline event.
    renamed = []
    for old, new in FILE_RENAMES_INNER:
        if Path(old).exists():
            os.rename(old, new)
            renamed.append(new)
    if (SNAP / "antivenom-pathways").exists():
        os.rename(SNAP / "antivenom-pathways", SNAP / "assay-pathways")
        renamed.append(str(SNAP / "assay-pathways"))
    th_old, th_new = SNAP / "sidecars" / "anti-venom-thesis.md", SNAP / "sidecars" / "assay-thesis.md"
    if th_old.exists():
        os.rename(th_old, th_new)
        renamed.append(str(th_new))
    ev_old = SNAP / "timeline" / "events" / "evt_003_antivenom_encoded.json"
    ev_new = SNAP / "timeline" / "events" / "evt_003_assay_encoded.json"
    if ev_old.exists():
        os.rename(ev_old, ev_new)
        renamed.append(str(ev_new))

    # Gloss insertion at first use (post-rename paths).
    glossed = []
    for fpath, anchor in GLOSS_ANCHORS.items():
        p = Path(fpath)
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if anchor in t and "an *assayer*" not in t:
            t = t.replace(anchor, anchor + ASSAY_DEF, 1)
            p.write_text(t, encoding="utf-8")
            glossed.append(fpath)

    print(f"assay rename: {len(changed)} files token/residue-edited, {len(renamed)} paths renamed, "
          f"{len(glossed)} glossed")
    for r in renamed:
        print("  renamed ->", r)

    produced = renamed + [
        f"{SNAP}/collaboration-pathways/scripts/09_rename_assay.py",
    ] + [g for g in GLOSS_ANCHORS]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(sorted(set(produced))), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
