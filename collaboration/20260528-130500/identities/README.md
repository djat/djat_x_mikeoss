# identities/ - de-identification lockboxes (privacy proxy)

Every de-identified placeholder (person-a/b/c, entity-1/2/3) has:
- a public, self-asserted credential (`*.credential.json`) - OpenVTC-compatible PHC (person)
  or Entity Credential, claiming "a real, unique person/entity participated", carrying a
  salted commitment but NO real name; and
- a lockbox (`*.lockbox.json`) - the real name + digital identities (DIDs/URLs), encrypted
  AES-256-CBC / PBKDF2-HMAC-SHA256 (600k iters).

Relationships (`relationships/*.json`) assert person<->entity (representative-of) so a peer
can be vouched for "by inference" (at least one real representative exists) without revealing
who - selective, least-privilege disclosure.

## Reveal (v1)
The Originator holds `keys/originator-reveal.key` (gitignored, never sealed) and can open any
lockbox. The viewer (`viewer/index.html`) reproduces the openssl decryption in-browser via
Web Crypto (PBKDF2 -> AES-CBC). The intended **1-of-2** with each subject's DID key is recorded
in each lockbox `recipients[]` as the upgrade path: once a subject registers/converts a key,
their slot is wrapped so EITHER party can open it.

## Roadmap (designed-for, not in v1)
- Per-recipient DID key-wrapping (genuine 1-of-2 with subject keys; X25519 from did:key).
- Zero-knowledge progressive reveal (prove "a real person exists" / "represents entity-2"
  without revealing the name); the salted commitment is the first step.
- Fully homomorphic encryption over sealed identity attributes.
