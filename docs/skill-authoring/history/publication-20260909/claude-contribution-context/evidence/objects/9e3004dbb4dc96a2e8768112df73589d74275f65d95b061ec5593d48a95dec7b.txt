---
schema_version: "devforge.artifact/v1"
artifact_id: "DEV-{{number}}"
artifact_type: "development-record"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-develop"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Development and gate evidence

## Governing identities and assignment

- Story reference: {{STORY-ID@revision}}
- Architecture reference: {{ARCH-ID@revision}}
- Required expert/evaluation references: {{XPKG/EVREPORT identities}}
- Authority-selected session/worktree record: {{SESSION reference}}
- Base commit and baseline manifest: {{identities}}
- External policy, CLI/runner, and run-state references: {{exact paths and digests}}
- Candidate write fence: {{paths}}

## Acceptance-to-test mapping

| Story AC reference | Test identifier/path | Behavior discriminated | Negative case | Evidence |
| --- | --- | --- | --- | --- |
| {{STORY-ID:AC-ID}} | {{test}} | {{behavior}} | {{case}} | {{receipt}} |

## Observed phase evidence

| Phase | Candidate/test identity | Runner/command reference | Outcome | External receipt | Cause if unavailable |
| --- | --- | --- | --- | --- | --- |
| Baseline initialization | {{identity}} | {{runner}} | NOT_RUN | {{reference}} | {{cause}} |
| RED | {{test digest}} | {{runner}} | NOT_RUN | {{reference}} | {{cause}} |
| GREEN | {{candidate + same test digest}} | {{runner}} | NOT_RUN | {{reference}} | {{cause}} |

## Candidate and changes

- Candidate manifest / patch reference: {{immutable reference}}
- Source and test changes: {{summary with paths}}
- Rule compliance observations: {{checks and evidence}}
- Test changes or baseline/context changes requiring a new run: {{items or none}}
- Untested conditions and remaining risks: {{items}}
- Intended reviewer task: {{request}}
- Handoff reference: {{HANDOFF-ID@revision}}

This record summarizes external evidence; editing it cannot create a RED/GREEN receipt or authorize acceptance.
