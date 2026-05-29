# Privacy refactor - provenanced event

This collaboration bundle was refactored as a single provenanced event, every step recorded
as a PathwayRun (see pathway-runs/) and indexed in pathway-runs/ASSET_PROVENANCE.yaml:

1. Phase 0 - provenance harness installed + bootstrap rename (Collaboration.Attestation.RecordPathwayRun@v1)
2. Phase 1 - full rename "transmission bundle" -> "collaboration bundle" (Collaboration.Refactor.RenameTerm@v1)
   + name-as-artifact: Term.CollaborationBundle@v1 supersedes Term.TransmissionBundle@v1
   (prior term retained + freely licensable) (Collaboration.Naming.RegisterTerm@v1)
3. Phase 2 - de-identification of external persons/entities to placeholders
   (Collaboration.Privacy.DeIdentify@v1); real names sealed, never in the snapshot
4. Phase 3 - self-asserted Personhood/Entity credentials + 1-of-2 lockboxes
   (Collaboration.Identity.IssuePersonhoodCredential/SealNameLockbox/AssertRelationship@v1)
5. Phase 4 - privacy-proxy reveal viewer (Collaboration.UX.RenderRevealViewer@v1 +
   Collaboration.Identity.RevealLockbox@v1)
6. Phase 5 - completeness gate + reseal

Attribution preserved as fact; identifiable names live only behind the 1-of-2 lockboxes, which
the Originator can open and which upgrade to genuine subject-key 1-of-2 when each subject
registers a DID key. ZK progressive reveal + FHE are the roadmap.
