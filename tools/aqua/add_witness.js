/**
 * add_witness.js - append a TSA timestamp witness revision to each Pathways AquaTree.
 *
 * Loads each existing "<artifact>.aqua.json" (genesis + did:key signature), appends an
 * Aqua "tsa" witness revision (RFC 3161 timestamp via DigiCert's public TSA, no wallet,
 * no chain), and writes the tree back (now genesis + signature + witness). Existing
 * signatures are preserved; this ADDS the timestamp only. Rebuilds aqua-trees-index.yaml
 * with witness metadata.
 *
 * Idempotent: a tree that already has a witness revision is left unchanged.
 * Requires network (timestamp.digicert.com). Uses aqua-js-sdk@3.2 CJS build.
 */
const aqua = require("aqua-js-sdk");
const fs = require("node:fs");
const path = require("node:path");

const Aquafier = aqua.default || aqua.Aquafier;
const isErr = aqua.isErr;

const REPO = process.cwd();
const SNAP = "collaboration/20260528-130500";
const DIRS = [
  `${SNAP}/assay-pathways/pathways`,
  `${SNAP}/collaboration-pathways/pathways`,
  `${SNAP}/collaboration-pathways/patterns`,
  `${SNAP}/collaboration-pathways/terms`,
];

function targets() {
  const out = [];
  for (const d of DIRS) {
    const abs = path.join(REPO, d);
    if (!fs.existsSync(abs)) continue;
    for (const f of fs.readdirSync(abs).sort()) {
      if (f.endsWith(".yaml") && !f.endsWith(".aqua.json")) out.push(path.join(d, f));
    }
  }
  return out;
}

(async () => {
  const aquafier = new Aquafier();
  const produced = [];
  const rows = [];
  let signer = null;

  for (const rel of targets()) {
    const abs = path.join(REPO, rel);
    const treePath = abs + ".aqua.json";
    const treeRel = rel + ".aqua.json";
    if (!fs.existsSync(treePath)) { console.error("missing tree (sign first):", treeRel); process.exit(1); }

    let tree = JSON.parse(fs.readFileSync(treePath, "utf-8"));
    const fileObject = { fileName: path.basename(rel), fileContent: fs.readFileSync(abs, "utf-8"), path: path.basename(rel) };

    const alreadyWitnessed = Object.values(tree.revisions).some(r => r.revision_type === "witness");
    if (!alreadyWitnessed) {
      const w = await aquafier.witnessAquaTree({ aquaTree: tree, fileObject, revision: "" }, "tsa", "sepolia", "cli", {}, false);
      if (isErr(w)) { console.error("witness failed:", rel); (w.data || []).forEach(e => console.error(JSON.stringify(e))); process.exit(1); }
      tree = w.data.aquaTree;
      fs.writeFileSync(treePath, JSON.stringify(tree, null, 2) + "\n");
    }
    produced.push(treeRel);

    const revs = Object.values(tree.revisions);
    const sig = revs.find(r => r.revision_type === "signature");
    const wit = revs.find(r => r.revision_type === "witness");
    if (sig && sig.signature_public_key) signer = sig.signature_public_key;
    rows.push({
      artifact: rel, tree: treeRel, revisions: revs.length,
      genesis: Object.keys(tree.revisions)[0],
      signer: sig && sig.signature_public_key,
      witness_ts: wit && wit.witness_timestamp,
    });
    console.log("witnessed:", treeRel, `(${revs.length} revisions, ts ${wit && wit.witness_timestamp})`);
  }

  const lines = [
    "# AquaTree attestation index - Aqua Protocol v3.2 (aqua-js-sdk)",
    "# Each Pathways artifact carries a sidecar <artifact>.aqua.json:",
    "#   genesis (file) + did:key signature + tsa witness (RFC 3161 timestamp).",
    "# Verify with aqua-js-sdk verifyAquaTree. Signing offline; witness via public TSA.",
    `aqua_protocol_version: "3.2"`,
    `sdk: "aqua-js-sdk@3.2.1-45"`,
    `sign_type: did_key`,
    `signer_did: "${signer || ""}"`,
    `witness_type: tsa`,
    `witness_protocol: TSA_RFC3161`,
    `witness_tsa_url: "http://timestamp.digicert.com"`,
    `count: ${rows.length}`,
    "trees:",
  ];
  for (const r of rows) {
    lines.push(`  - artifact: ${r.artifact}`);
    lines.push(`    tree: ${r.tree}`);
    lines.push(`    revisions: ${r.revisions}`);
    lines.push(`    genesis_hash: ${r.genesis}`);
    lines.push(`    signer_did: "${r.signer || ""}"`);
    lines.push(`    witness_timestamp: ${r.witness_ts || ""}`);
  }
  const indexRel = `${SNAP}/aqua-trees-index.yaml`;
  fs.writeFileSync(path.join(REPO, indexRel), lines.join("\n") + "\n");
  produced.push(indexRel);
  produced.push("tools/aqua/add_witness.js");

  const am = process.env.ASSET_MANIFEST;
  if (am) fs.writeFileSync(am, JSON.stringify(produced));
  console.log(`witness: ${rows.length} tree(s) timestamped; signer ${signer}`);
})();
