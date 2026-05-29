/**
 * make_aqua_trees.js - sign every Pathways artifact with a real AquaTree (Aqua Protocol v3.2).
 *
 * For each pathway template, pattern, and term in the bundle, this creates an Aqua genesis
 * (file) revision plus a "did" signature revision: an Ed25519 JWS signed by a did:key
 * (offline, no witness, no network). Writes "<artifact>.aqua.json" alongside each artifact,
 * and aqua-trees-index.yaml summarizing each tree, its revision hashes, and the signer DID.
 *
 * Overwrites existing trees (re-sign). The Ed25519 private key is generated once and kept in
 * keys/aqua-signing.did.json (gitignored, never sealed); only the public did:key is recorded.
 *
 * Run THROUGH the provenance harness so it is captured as a PathwayRun.
 * Uses aqua-js-sdk@3.2 CJS build (the ESM build has a broken dynamic require of crypto).
 */
const aqua = require("aqua-js-sdk");
const { Mnemonic } = require("ethers");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const Aquafier = aqua.default || aqua.Aquafier;
const isErr = aqua.isErr;

const REPO = process.cwd();
const SNAP = "collaboration/20260528-130500";
const KEYS = path.join(REPO, "keys", "aqua-signing.did.json");
const DIRS = [
  `${SNAP}/assay-pathways/pathways`,
  `${SNAP}/collaboration-pathways/pathways`,
  `${SNAP}/collaboration-pathways/patterns`,
  `${SNAP}/collaboration-pathways/terms`,
];

function loadCredentials() {
  if (fs.existsSync(KEYS)) return JSON.parse(fs.readFileSync(KEYS, "utf-8"));
  const did_key = crypto.randomBytes(32).toString("hex"); // Ed25519 private key, hex
  const creds = {
    mnemonic: "", nostr_sk: "", did_key, alchemy_key: "",
    witness_eth_network: "", witness_method: "did",
  };
  fs.mkdirSync(path.dirname(KEYS), { recursive: true });
  fs.writeFileSync(KEYS, JSON.stringify(creds, null, 2) + "\n");
  return creds;
}

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
  const creds = loadCredentials();
  const produced = [];
  const indexRows = [];
  let signer = null;

  for (const rel of targets()) {
    const abs = path.join(REPO, rel);
    const treePath = abs + ".aqua.json";
    const treeRel = rel + ".aqua.json";

    const fileName = path.basename(rel);
    const fileObject = { fileName, fileContent: fs.readFileSync(abs, "utf-8"), path: fileName };

    const gen = await aquafier.createGenesisRevision(fileObject);
    if (isErr(gen)) { console.error("genesis failed:", rel); (gen.data || []).forEach(e => console.error(e)); process.exit(1); }

    const wrapper = { aquaTree: gen.data.aquaTree, fileObject, revision: "" };
    const signed = await aquafier.signAquaTree(wrapper, "did", creds, false);
    if (isErr(signed)) { console.error("sign failed:", rel); (signed.data || []).forEach(e => console.error(JSON.stringify(e))); process.exit(1); }

    const tree = signed.data.aquaTree;
    fs.writeFileSync(treePath, JSON.stringify(tree, null, 2) + "\n");
    produced.push(treeRel);

    const hashes = Object.keys(tree.revisions);
    const sigRev = Object.values(tree.revisions).find(r => r.revision_type === "signature");
    const signerDid = sigRev && (sigRev.signature_public_key || sigRev.signature_wallet_address);
    if (signerDid) signer = signerDid;
    indexRows.push({ artifact: rel, tree: treeRel, revisions: hashes.length, genesis: hashes[0], signer_did: signerDid });
    console.log("aqua:", treeRel, `(${hashes.length} revisions)`);
  }

  // index
  const lines = [
    "# AquaTree attestation index - Aqua Protocol v3.2 (aqua-js-sdk)",
    "# Each Pathways artifact carries a sidecar <artifact>.aqua.json: genesis (file) + did:key signature revision.",
    "# Signing is offline (Ed25519 JWS via did:key, no witness). Verify with aqua-js-sdk verifyAquaTree.",
    `aqua_protocol_version: "3.2"`,
    `sdk: "aqua-js-sdk@3.2.1-45"`,
    `sign_type: did_key`,
    `signer_did: "${signer || ""}"`,
    `count: ${indexRows.length}`,
    "trees:",
  ];
  for (const r of indexRows) {
    lines.push(`  - artifact: ${r.artifact}`);
    lines.push(`    tree: ${r.tree}`);
    lines.push(`    revisions: ${r.revisions}`);
    lines.push(`    genesis_hash: ${r.genesis}`);
    lines.push(`    signer_did: "${r.signer_did || ""}"`);
  }
  const indexRel = `${SNAP}/aqua-trees-index.yaml`;
  if (produced.length > 0) {
    fs.writeFileSync(path.join(REPO, indexRel), lines.join("\n") + "\n");
    produced.push(indexRel);
  }

  produced.push("tools/aqua/make_aqua_trees.js");
  const am = process.env.ASSET_MANIFEST;
  if (am) fs.writeFileSync(am, JSON.stringify(produced));
  console.log(`aqua trees: ${indexRows.length} artifact(s) signed; signer ${signer}`);
})();
