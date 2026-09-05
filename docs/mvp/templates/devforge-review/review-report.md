---
schema_version: "devforge.artifact/v1"
artifact_id: "QA-{{number}}"
artifact_type: "review-report"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-review"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Candidate review and QA

## Scope and immutable inputs

- Candidate manifest / commit: {{exact identity}}
- Development/gate evidence: {{DEV and external receipt refs}}
- Story/architecture/design references: {{exact applicable revisions}}
- Required expert/evaluation references: {{identities}}
- Reviewer session/worktree assignment: {{SESSION reference}}
- Independence requirement and actual process: {{observed process}}

## Acceptance coverage

| Story AC / rule reference | Candidate evidence | Test or inspection | Outcome | Gap |
| --- | --- | --- | --- | --- |
| {{reference}} | {{path/behavior}} | {{check}} | NOT_RUN | {{gap}} |

## Quality checks selected by requirements

| Concern | Applicable requirement/risk | Check performed | Outcome | Raw evidence / not-applicable rationale |
| --- | --- | --- | --- | --- |
| {{security/performance/accessibility/operations/etc.}} | {{source}} | {{actual check}} | NOT_RUN | {{reference}} |

## Findings and ownership

| Finding ID | Severity / impact | Evidence | Governing reference | Owner workflow | Recheck condition |
| --- | --- | --- | --- | --- | --- |
| FIND-001 | {{impact}} | {{path/output}} | {{requirement/rule}} | {{develop/plan/change}} | {{observable resolution}} |

## Readiness recommendation

- Recommendation: {{ready for stated next step / changes required / insufficient evidence}}
- Blocking findings: {{IDs or none}}
- Unavailable checks: {{checks and causes}}
- Exact candidate covered: {{identity}}
- Decision authority / adoption reference: null
- Handoff reference: {{HANDOFF-ID@revision}}

A passing suite is evidence for its tested behavior; it is not proof of all requirement semantics.
