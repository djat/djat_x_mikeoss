# Start Collaboration Handoff - Agent Entry Prompt

**Document type:** Meta instructive prompt (run once at repository root)
**Audience:** LLM agent or agentic reader on either side of the channel
**Repository:** `djat_x_mikeoss`
**Prepared for:** the open MikeOSS project and team
**Channel:** `djat-mikeoss-20260528`

---

## How to use this prompt

1. Clone this repository and `cd` to the **repository root** (the directory that contains `README.md`, `tools/`, and `collaboration/`).
2. Copy everything below the `--- BEGIN PROMPT ---` marker into your agent session **as the first message**.
3. Execute each step in order. Do not skip verification.

Human readers may follow the same steps as a checklist without pasting into an LLM.

This is an **invitation** collaboration, not a build handoff. There is no required build and no obligation to reciprocate. The closing step is a menu of small experiments either side can run independently.

---

--- BEGIN PROMPT ---

## You are: inbound collaboration loader

You are loading the **open Pathways × MikeOSS collaboration bundle**. Your job in this session is to:

1. Verify bundle integrity.
2. Understand what is authoritative.
3. Load the read order and the embedded self-describing technique encoding.
4. Surface the menu of self-validating experiments - so value can be produced with or without a reciprocal collaboration.

---

## Step 1 - Verify integrity (mandatory)

From **repository root**, run:

```bash
python3 tools/collaboration-bundle/sign_bundle.py verify collaboration/20260528-130500
```

**Expected:** `verify: OK`

**If verification fails:** STOP. Do not trust the contents until integrity is resolved.

**Authoritative hash:** read `bundle_root_hash` from `collaboration/20260528-130500/attestations/CONTENT_MANIFEST.yaml`. Do not trust a hash copied in prose elsewhere.

Set your `BUNDLE_ROOT` to:

```text
collaboration/20260528-130500/
```

---

## Step 2 - Load read order (paths relative to `BUNDLE_ROOT`)

Read these files **in order**:

| # | Path (under `BUNDLE_ROOT`) | Purpose |
|---|---|---|
| 1 | `companion-bundle-index.md` | Human-oriented index |
| 2 | `collaboration-spine.md` | The invitation, the read-as-truth exercise, the anti-venom thesis, the asks |
| 3 | `collaboration-pathways/canon/COLLABORATION_BUNDLE_TECHNIQUE.md` | The collaboration-bundle technique, canonically encoded as Pathways |
| 4 | `collaboration-pathways/APPLICATION_PLAYBOOK.md` | How a collaboration is encoded |
| 5 | `collaboration-pathways/pathways-index.yaml` | The full Collaboration.* family (interrogable) |
| 6 | `antivenom-pathways/APPLICATION_PLAYBOOK.md` | The legal anti-venom pathways |
| 7 | `collaboration-pathways/test/HYPOTHESES.md` | The asks, pre-registered as falsifiable experiments |
| 8 | `collaboration-manifest.yaml` | Machine index; includes the `technique_provenance` block |

---

## Step 3 - Interrogate the technique (the point of this bundle)

This bundle is self-describing. To interrogate not just the format but its Pathways formalization:

1. Open `collaboration-manifest.yaml` and read the `technique_provenance:` block (version, co-originators, lineage, defining pathways).
2. Open the `collaboration-pathways/pathways/` directory and read any `Collaboration.*` template - each is a `pathway_template` you can fork, critique, or re-implement.
3. The pathway `Collaboration.Meta.EmbedTechniqueProvenance@v1` is the rule that put this self-description here. The pattern `Pattern.CollaborationBundle.SelfDescribing` states the invariant.

---

## Step 4 - Consider the asks (no obligation)

`collaboration-pathways/test/HYPOTHESES.md` holds 10 pre-registered hypotheses (H-MO1..H-MO10). Each maps to a small experiment that produces standalone value. The bundle can reach `SEALED` on the **unilateral** experiments alone; a reciprocal collaboration from MikeOSS is welcome but not required.

If you wish to reply, see `collaboration-spine.md` § Reciprocation - and know that a reply is itself just another collaboration bundle in this same lineage.

--- END PROMPT ---
