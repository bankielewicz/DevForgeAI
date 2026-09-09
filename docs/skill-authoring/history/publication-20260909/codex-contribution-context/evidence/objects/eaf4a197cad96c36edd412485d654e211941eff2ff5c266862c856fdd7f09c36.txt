---
schema_version: "devforge.artifact/v1"
artifact_id: "XSPEC-{{number}}"
artifact_type: "expert-spec"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Project expert specification

## Concrete capability

- Capability ID and task/goal: {{CAP-ID and requirement/story reference}}
- Why current skills/context are insufficient: {{observed gap}}
- Reuse versus new skill decision: {{rationale}}
- Intended native skill name: {{project-capability name}}
- Supported target terminal(s): {{Codex / Claude, to be evaluated separately}}

## Scope and activation

| Case | Representative request | Should activate? | Required behavior |
| --- | --- | --- | --- |
| Direct | {{request}} | yes | {{observable outcome}} |
| Indirect | {{request}} | yes | {{observable outcome}} |
| Similar but unrelated | {{request}} | no | {{appropriate routing}} |
| Missing input | {{request}} | {{conditional}} | {{question or bounded stop}} |

## Governing knowledge

| Knowledge ID | Approved rule or project fact | Exact upstream reference | Version-specific source | Verification date / limit |
| --- | --- | --- | --- | --- |
| KNOW-001 | {{fact}} | {{ARCH/PROD/STORY reference}} | {{source}} | {{date/limit}} |

## Capability behavior and deliverables

{{Decision guidance that changes work, required inputs, native outputs, uncertainty handling, and verification. Avoid generic expert-persona claims.}}

## Candidate-independent acceptance expectations

| Case ID | Task / condition | Expected observable behavior | Governing source | Failure that matters |
| --- | --- | --- | --- | --- |
| XCASE-001 | {{realistic task}} | {{expectation}} | {{rule/requirement}} | {{violation}} |

## Permissions and refresh

- Required runtime tools and permitted paths: {{scope}}
- External controls the skill cannot change: {{policy/runner/evaluation authority}}
- Refresh triggers: {{relevant versions, rules, source layout, observed failures}}
- Prior expert/evaluation references: {{references or none}}
- Acceptance expectation identity before candidate authoring: {{reference}}
