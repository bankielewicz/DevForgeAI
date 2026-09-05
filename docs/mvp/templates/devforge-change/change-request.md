---
schema_version: "devforge.artifact/v1"
artifact_id: "CHG-{{number}}"
artifact_type: "change-request"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-change"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Change proposal and impact assessment

## Trigger and requested outcome

- Trigger type: {{user feedback / defect / dependency update / changed assumption}}
- Evidence and origin: {{source reference}}
- Current accepted behavior or decision: {{exact artifact/section/revision}}
- Requested change: {{before/after}}
- Decision state: proposed
- Adoption or rejection reference: null

## Direct and transitive impact

| Affected artifact / installed package / run | Current identity | Dependency path from changed source | Expected impact | Required owner action | Confidence / missing edge |
| --- | --- | --- | --- | --- | --- |
| {{identity}} | {{revision/digest}} | {{upstream chain}} | {{semantic or structural impact}} | {{revise/refresh/retest/review}} | {{coverage limit}} |

## Routing decision

- In-scope implementation repair or governing amendment: {{classification and reason}}
- Owning skill for the first revision: {{skill}}
- Unaffected work that can continue: {{scope}}
- Work that must remain stale or blocked: {{scope and reason}}
- Active sessions/worktrees affected: {{external assignment references}}
- Integration/rebase implications: {{new baseline or combined-candidate checks}}

## Refresh and verification plan

| Required revision or check | Inputs to pin | Expected evidence | Owner | State |
| --- | --- | --- | --- | --- |
| {{task}} | {{identities}} | {{artifact/receipt}} | {{owner}} | proposed |

Include generated expert source, installed copies, evaluations, and downstream candidates where affected. A refresh is not complete when only the source SKILL.md changed.

## Completion and preservation

- Superseded artifacts retained at: {{immutable references}}
- New accepted artifacts and evidence: {{references or none}}
- Declined/deferred work and rationale: {{items}}
- Handoff reference: {{HANDOFF-ID@revision}}
