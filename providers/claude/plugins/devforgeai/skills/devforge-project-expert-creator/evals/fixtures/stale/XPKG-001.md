---
schema_version: "devforge.artifact/v1"
artifact_id: "XPKG-001"
artifact_type: "expert-package"
project_id: "synthetic-notes"
revision: 1
status: accepted
created_at_utc: "2026-08-15T11:05:00Z"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "unknown; synthetic fixture"
execution_ref: null
upstream:
  - artifact_id: "ARCH-001"
    revision: 1
    store: project
    path: "docs/devforge/architecture/ARCH-001.md"
    sha256: "65d99ab516b5fb2bca9e0d45dc5587c27d692fc426957329173a6d357ad70314"
    sections:
      - RULE-001
      - RULE-002
      - RULE-003
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Expert package record: notes-storage

Synthetic fixture. Illustrative values for an evaluation case.

## Candidate identity

- Expert specification: XSPEC-001@1
- Native skill name: notes-storage
- Source skill directory: project/experts/notes-storage
- Structural binding reference: NOT_RUN
- Behavioural status: NOT_EVALUATED

## Candidate limits

The recorded knowledge rests on ARCH-001 at revision 1, in which RULE-003 was
not addressed. Guidance about unrecognised stored fields is therefore absent from
this package by design, not by omission.
