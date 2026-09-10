---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-007"
artifact_type: "expert-evaluation-report"
project_id: "tidepool"
revision: 1
status: accepted
created_at_utc: "2026-08-11T13:55:00Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: "SESSION-053@1"
upstream:
  - artifact_id: "XPKG-004"
    revision: 2
    store: "project"
    path: "docs/devforge/experts/XPKG-tide-sync.md"
    sha256: "recompute from fixtures/shared/XPKG-tide-sync.md"
    sections: ["File manifest"]
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Evaluation report: tide-sync

Synthetic fixture.

## Bound candidate

The exact bytes examined were the XPKG-004 revision-2 manifest above, specifically
`SKILL.md` at `a1b2c3d4…8f90`. This report is evidence about those bytes and no others.

## Observations

- Tier C: installed resources resolved.
- Tier B: five of six cases matched the expected behaviour; the reconciliation-refusal case
  matched.
- Tier A: NOT_RUN.

Any change to the candidate bytes ends this report's applicability to the changed package.
