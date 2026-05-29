#!/usr/bin/env python3
"""05_build_viewer.py - generate the self-contained privacy-proxy reveal UX (Phase 4).

The viewer's HTML/JS is a generated asset, encoded as Collaboration.UX.RenderRevealViewer@v1;
the in-browser decryption technique is Collaboration.Identity.RevealLockbox@v1 (Web Crypto
PBKDF2 -> AES-CBC, reproducing the openssl seal). Data (de-identification map + public claims +
ciphertexts) is inlined so the viewer works from file:// with no server/fetch. The real names
are NEVER inlined - only ciphertext - so the viewer itself leaks nothing without the reveal key.
"""
import hashlib
import json
import os
from pathlib import Path

SNAP = Path("collaboration/20260528-130500")
IDENT = SNAP / "identities"
VIEWER = IDENT / "viewer"
RUN_ID = os.environ.get("PATHWAY_RUN_ID", "")


def load_subject(kind_dir: str, ph: str) -> dict:
    cred = json.loads((IDENT / kind_dir / f"{ph}.credential.json").read_text())
    lb = json.loads((IDENT / kind_dir / f"{ph}.lockbox.json").read_text())
    return {
        "ph": ph,
        "kind": cred["subject_kind"],
        "claim": cred["claim"],
        "commitment": cred["commitment"]["value"],
        "recipients": lb["recipients"],
        "ciphertext_b64": lb["reveal"]["ciphertext_b64"],
        "iter": lb["reveal"]["iter"],
    }


def main() -> int:
    VIEWER.mkdir(parents=True, exist_ok=True)
    dmap = json.loads((IDENT / "deidentification-map.json").read_text())
    subjects = []
    for d, phs in (("persons", ["person-a", "person-b", "person-c"]),
                   ("entities", ["entity-1", "entity-2", "entity-3"])):
        for ph in phs:
            if (IDENT / d / f"{ph}.lockbox.json").exists():
                subjects.append(load_subject(d, ph))
    rels = []
    rd = IDENT / "relationships"
    if rd.exists():
        for f in sorted(rd.glob("*.json")):
            rels.append(json.loads(f.read_text()))

    data = {"placeholders": dmap.get("placeholders", {}), "subjects": subjects,
            "relationships": rels, "generated_run": RUN_ID}
    data_js = json.dumps(data, indent=2)

    html = HTML_TEMPLATE.replace("/*__DATA__*/", data_js)
    (VIEWER / "index.html").write_text(html, encoding="utf-8")
    sha = hashlib.sha256(html.encode("utf-8")).hexdigest()

    (VIEWER / "PROVENANCE.json").write_text(json.dumps({
        "asset": "identities/viewer/index.html",
        "produced_by_pathway": "Collaboration.UX.RenderRevealViewer@v1",
        "decrypt_technique_pathway": "Collaboration.Identity.RevealLockbox@v1",
        "pathway_run_id": RUN_ID,
        "sha256": sha,
        "note": "Generated HTML/JS is a Pathway-produced asset; HTML cannot hold metadata inline so it is recorded here and in ASSET_PROVENANCE.yaml.",
    }, indent=2) + "\n", encoding="utf-8")

    (VIEWER / "README.md").write_text(VIEWER_README, encoding="utf-8")

    for name, body in TEMPLATES.items():
        (SNAP / "collaboration-pathways" / "pathways" / name).write_text(body, encoding="utf-8")

    produced = [
        "identities/viewer/index.html", "identities/viewer/PROVENANCE.json",
        "identities/viewer/README.md",
        "collaboration-pathways/pathways/Collaboration.UX.RenderRevealViewer.v1.yaml",
        "collaboration-pathways/pathways/Collaboration.Identity.RevealLockbox.v1.yaml",
        "collaboration-pathways/scripts/05_build_viewer.py",
    ]
    produced = [str(SNAP / p) for p in produced]
    am = os.environ.get("ASSET_MANIFEST")
    if am:
        Path(am).write_text(json.dumps(produced), encoding="utf-8")
    print(f"viewer: built index.html (sha256 {sha[:16]}...), {len(subjects)} subjects, {len(rels)} relationships")
    return 0


TEMPLATES = {
    "Collaboration.UX.RenderRevealViewer.v1.yaml": """# Collaboration.UX.RenderRevealViewer@v1
pathway_template:
  identity:
    template_id: Collaboration.UX.RenderRevealViewer@v1
    artifact_type: pathway-template
    triple: { domain: Collaboration, subdomain: UX, action: RenderRevealViewer }
    version: 1.0.0
  description: |
    Generates the self-contained privacy-proxy reveal UX (identities/viewer/index.html). The
    generated HTML/JS is itself a Pathway-produced asset (recorded in viewer/PROVENANCE.json +
    ASSET_PROVENANCE.yaml), NOT a hand-waved artifact. It lists every de-identified site, shows
    the public personhood/entity claims + relationships, and reveals real names + digital
    identities client-side via Collaboration.Identity.RevealLockbox@v1. Inlines only ciphertext.
  implementation: collaboration-pathways/scripts/05_build_viewer.py
  output: { artifact: reveal_viewer }
""",
    "Collaboration.Identity.RevealLockbox.v1.yaml": """# Collaboration.Identity.RevealLockbox@v1
pathway_template:
  identity:
    template_id: Collaboration.Identity.RevealLockbox@v1
    artifact_type: pathway-template
    triple: { domain: Collaboration, subdomain: Identity, action: RevealLockbox }
    version: 1.0.0
  description: |
    The reveal technique: reproduce the openssl AES-256-CBC / PBKDF2-HMAC-SHA256 seal in the
    browser via Web Crypto (PBKDF2 deriveBits -> AES-CBC decrypt -> PKCS7), then verify the
    salted commitment sha256(real_name||salt) against the public credential. The Originator's
    reveal key (1-of-2: originator side) opens the box; the subject's DID key is the upgrade path.
  implementation: identities/viewer/index.html (inline Web Crypto)
  output: { artifact: revealed_identity }
""",
}

VIEWER_README = """# Reveal viewer (privacy proxy)

Open `index.html` in any modern browser (works from file://). It shows:
- every de-identified placeholder and every file/site where it appears;
- the public, self-asserted personhood/entity claims, commitments, and 1-of-2 recipient status;
- a reveal panel.

To reveal: paste the contents of `keys/originator-reveal.key` (the Originator's reveal key,
gitignored, never sealed) into the key field and click Reveal on any subject. The browser
reproduces the openssl decryption (PBKDF2 -> AES-CBC) and verifies the salted commitment.

Nothing real is embedded in this page - only ciphertext. Without the reveal key it discloses
no names. This is the privacy proxy: least-privilege, selective conversion of placeholders back
to identities, fully under the Originator's (or, on the roadmap, the subject's) control.
"""

HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Collaboration Bundle - Privacy Proxy Reveal Viewer</title>
<style>
  :root{color-scheme:dark light}
  body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#0f1115;color:#e6e6e6}
  header{padding:20px 24px;border-bottom:1px solid #2a2f3a;background:#141821}
  h1{font-size:18px;margin:0 0 4px} .sub{color:#9aa4b2;font-size:13px}
  main{max-width:980px;margin:0 auto;padding:20px 24px}
  .keybar{display:flex;gap:10px;align-items:center;background:#141821;border:1px solid #2a2f3a;border-radius:10px;padding:12px 14px;margin-bottom:20px;flex-wrap:wrap}
  .keybar input{flex:1;min-width:240px;background:#0b0e13;border:1px solid #2a2f3a;color:#e6e6e6;border-radius:8px;padding:8px 10px;font-family:ui-monospace,monospace}
  button{background:#2d6cdf;color:#fff;border:0;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:13px}
  button.ghost{background:#222936}
  .card{background:#141821;border:1px solid #2a2f3a;border-radius:10px;padding:14px 16px;margin-bottom:12px}
  .row{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}
  .ph{font-family:ui-monospace,monospace;font-weight:600}
  .tag{font-size:11px;padding:2px 8px;border-radius:999px;background:#222936;color:#9aa4b2;margin-left:6px}
  .claim{color:#c9d2de;font-size:13px;margin:6px 0}
  .reveal{margin-top:10px;padding:10px;border-radius:8px;background:#0b1a12;border:1px solid #1f6f43;display:none}
  .reveal.err{background:#1a0e0e;border-color:#6f2020}
  .mono{font-family:ui-monospace,monospace;font-size:12px;word-break:break-all}
  a{color:#6ea8fe} h2{font-size:15px;margin:26px 0 10px;color:#c9d2de}
  .sites{font-size:12px;color:#9aa4b2} .sites li{margin:2px 0}
  .recip{font-size:12px;color:#9aa4b2;margin-top:4px}
  details summary{cursor:pointer;color:#9aa4b2;font-size:12px}
  .ok{color:#5fd08a} .bad{color:#f08a8a}
</style></head>
<body>
<header>
  <h1>Collaboration Bundle - Privacy Proxy Reveal Viewer</h1>
  <div class="sub">Self-asserted personhood/entity claims with 1-of-2 lockboxes. Paste the Originator reveal key to selectively reveal real names + digital identities. Nothing real is stored on this page - only ciphertext.</div>
</header>
<main>
  <div class="keybar">
    <input id="revealKey" type="password" placeholder="paste contents of keys/originator-reveal.key" autocomplete="off"/>
    <button onclick="revealAll()">Reveal all</button>
    <button class="ghost" onclick="toggleKey()">show/hide</button>
  </div>
  <div id="subjects"></div>
  <h2>Relationships (representative-of)</h2>
  <div id="rels"></div>
  <h2>De-identification map - every placeholder, every site</h2>
  <div id="map"></div>
</main>
<script>
const DATA = /*__DATA__*/;

function toggleKey(){const k=document.getElementById('revealKey');k.type=k.type==='password'?'text':'password';}

async function sha256hex(s){
  const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
}

async function revealLockbox(sub, keyText){
  const raw=Uint8Array.from(atob(sub.ciphertext_b64),c=>c.charCodeAt(0));
  const magic=String.fromCharCode.apply(null,raw.slice(0,8));
  if(magic!=='Salted__') throw new Error('unexpected ciphertext format');
  const salt=raw.slice(8,16), ct=raw.slice(16);
  const pw=new TextEncoder().encode(keyText);
  const base=await crypto.subtle.importKey('raw',pw,{name:'PBKDF2'},false,['deriveBits']);
  const bits=new Uint8Array(await crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:salt,iterations:sub.iter},base,48*8));
  const aesKey=await crypto.subtle.importKey('raw',bits.slice(0,32),{name:'AES-CBC'},false,['decrypt']);
  const ptBuf=await crypto.subtle.decrypt({name:'AES-CBC',iv:bits.slice(32,48)},aesKey,ct);
  const obj=JSON.parse(new TextDecoder().decode(ptBuf));
  const commit=await sha256hex(obj.real_name+obj.salt);
  obj.__commitment_ok = (commit===sub.commitment);
  return obj;
}

async function doReveal(ph){
  const key=document.getElementById('revealKey').value.trim();
  const el=document.getElementById('rv-'+ph);
  const sub=DATA.subjects.find(s=>s.ph===ph);
  if(!key){el.className='reveal err';el.style.display='block';el.textContent='Paste the reveal key first.';return;}
  try{
    const o=await revealLockbox(sub,key);
    const ids=(o.identities||[]).map(u=>u.startsWith('http')?`<a href="${u}" target="_blank" rel="noopener">${u}</a>`:`<span class="mono">${u}</span>`).join('<br>');
    el.className='reveal';el.style.display='block';
    el.innerHTML=`<div><b>Real name:</b> ${o.real_name}</div>`+
      (o.did?`<div><b>DID:</b> <span class="mono">${o.did}</span></div>`:'')+
      (ids?`<div style="margin-top:4px"><b>Digital identities:</b><br>${ids}</div>`:'')+
      (o.associated_entity?`<div style="margin-top:4px"><b>Associated entity:</b> ${o.associated_entity}</div>`:'')+
      (o.representative?`<div style="margin-top:4px"><b>Representative:</b> ${o.representative}</div>`:'')+
      `<div style="margin-top:6px" class="${o.__commitment_ok?'ok':'bad'}">commitment ${o.__commitment_ok?'verified ✓ (matches public claim)':'MISMATCH ✗'}</div>`;
  }catch(e){el.className='reveal err';el.style.display='block';el.textContent='Reveal failed (wrong key or unsupported browser): '+e.message;}
}
async function revealAll(){for(const s of DATA.subjects){await doReveal(s.ph);}}

function recipLine(r){
  return r.map(x=>`${x.role}: ${x.can_open?'<span class="ok">can open</span>':'<span class="bad">pending subject key</span>'}`).join(' &nbsp;|&nbsp; ');
}

function render(){
  document.getElementById('subjects').innerHTML=DATA.subjects.map(s=>`
    <div class="card">
      <div class="row"><div><span class="ph">${s.ph}</span><span class="tag">${s.kind}</span></div>
        <button onclick="doReveal('${s.ph}')">Reveal</button></div>
      <div class="claim">${s.claim}</div>
      <div class="recip">1-of-2: ${recipLine(s.recipients)}</div>
      <details><summary>commitment</summary><div class="mono">${s.commitment}</div></details>
      <div class="reveal" id="rv-${s.ph}"></div>
    </div>`).join('');
  document.getElementById('rels').innerHTML=(DATA.relationships||[]).map(r=>`
    <div class="card"><div class="claim"><span class="ph">${r.person}</span> represents <span class="ph">${r.entity}</span></div>
    <div class="sites">${r.claim}</div></div>`).join('') || '<div class="sites">none</div>';
  const ph=DATA.placeholders||{};
  document.getElementById('map').innerHTML=Object.keys(ph).sort().map(k=>`
    <div class="card"><div class="row"><div><span class="ph">${k}</span><span class="tag">${ph[k].kind}</span></div>
      <div class="sites">${ph[k].total} occurrences</div></div>
      <ul class="sites">${(ph[k].sites||[]).map(s=>`<li>${s.file} (${s.count})</li>`).join('')}</ul></div>`).join('');
}
render();
</script>
</body></html>
"""

if __name__ == "__main__":
    raise SystemExit(main())
