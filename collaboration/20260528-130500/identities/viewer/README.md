# Reveal viewer (privacy proxy)

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
