---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-004"
artifact_type: "architecture-contract"
project_id: "shiftwell"
revision: 1
status: draft
created_at_utc: "2026-08-21T10:30:00Z"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: null
upstream:
  - artifact_id: "PB-003"
    revision: 1
    store: "project"
    path: "preserved/PB-003.r1.md"
    sha256: "b6097c371bc88e64c41a77ee772d138e8173900614574649798f53f051ddc3b2"
    sections:
      - REQ-020
      - REQ-021
      - NFR-020
evidence: []
supersedes: null
decision_ref: "user adoption recorded 2026-08-21 for ADR-010 only"
missing_inputs: []
---

# Architecture and project contract: Shiftwell notifications

Synthetic fixture. The upstream digest above is the real SHA-256 of
`preserved/PB-003.r1.md` in this fixture directory, so the reference resolves.
The brief's live path now holds revision 2, whose NFR-020 says something different.

## Architecture decisions

| ADR ID | Requirement references | Decision | Alternatives / rationale | Decision state | Adoption reference |
| --- | --- | --- | --- | --- | --- |
| ADR-010 | REQ-020, REQ-021, NFR-020 | Send notifications from a background queue with no delivery guarantee; drop after three failures | A synchronous send was rejected because a slow provider would block publishing | accepted | user adoption 2026-08-21 |

## Approved stack and version-specific knowledge

| Rule ID | Capability | Package/provider | Exact version or accepted range | Real manifest/lockfile | Verified API reference | Decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-010 | outbound email | MailKit | 4.7.1 | Directory.Packages.props | not verified; recorded as an open item | ADR-010 |

## Verification and operations

- External enforcement coverage: none implemented. RULE-010 is recorded for the external policy owner and no adapter checks it.
