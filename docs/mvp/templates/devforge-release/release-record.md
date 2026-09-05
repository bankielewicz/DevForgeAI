---
schema_version: "devforge.artifact/v1"
artifact_id: "REL-{{number}}"
artifact_type: "release-record"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-release"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# PR and release preparation record

## Reviewed candidate and target

- QA report: {{QA-ID@revision}}
- Candidate snapshot and mapped Git commit/tree: {{exact identities; explain the mapping}}
- Story/epic references: {{scope}}
- Target repository/branch/environment: {{observed targets}}
- Integration worktree/session assignment: {{SESSION reference}}
- Final external verification: {{receipt or NOT_RUN}}

## Reviewable PR draft

- Title: {{concrete problem and resulting behavior}}
- Body: {{scope, why, verification, and material limitations}}
- Release notes: {{user-visible changes}}
- Applicable migration and recovery steps: {{steps or explicit not-applicable rationale}}

## Planned actions and authority

| Action | Concrete target | Existing authorization reference | Prerequisites | Planned verification |
| --- | --- | --- | --- | --- |
| {{create PR / merge / deploy / verify}} | {{target}} | {{reference or missing}} | {{conditions}} | {{readback/check}} |

## Actual delivery observations

| Event | Outcome | Commit/PR/release/environment reference | Evidence and timestamp | Remaining action |
| --- | --- | --- | --- | --- |
| Local candidate verification | NOT_RUN | {{identity}} | {{receipt}} | {{next}} |
| PR creation | NOT_RUN | {{actual URL if created}} | {{readback}} | {{next}} |
| Merge | NOT_RUN | {{actual commit if merged}} | {{readback}} | {{next}} |
| Deployment | NOT_RUN | {{actual deployment if performed}} | {{readback}} | {{next}} |
| Post-release verification | NOT_RUN | {{target}} | {{observation}} | {{next}} |

## CI and feedback

- Deterministic CI result and exact revision: {{observed result or unavailable}}
- Model-driven Codex GitHub Action: deferred for the subscription-only MVP; its documented setup requires an API key.
- Operational feedback / unresolved risk: {{items}}
- Change-request references: {{CHG IDs when applicable}}
- Handoff reference: {{HANDOFF-ID@revision}}
