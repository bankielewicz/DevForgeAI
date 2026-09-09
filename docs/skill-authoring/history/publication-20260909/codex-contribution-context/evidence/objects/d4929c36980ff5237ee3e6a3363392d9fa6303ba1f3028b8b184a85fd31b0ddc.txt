---
schema_version: "devforge.artifact/v1"
artifact_id: "SEVAL-{{number}}"
artifact_type: "skill-evaluation-report"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "{{actual-native-creator-or-operator}}"
  skill_revision: "{{actual-revision-or-digest}}"
execution_ref: "{{actual-session-reference}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill authoring evaluation

- Skill/provider: {{identity}}
- Source and installed package: {{separate file manifests and digests}}
- Selected specification and cases: {{exact revisions/digests}}
- Baseline: {{old_skill or without_skill; exact identity and isolation}}
- Runtime and installation mode: {{actual client/version/model and discovery location}}
- Context/assignment: {{observed isolation and operator assignment}}
- Prior evaluation: {{preserved reference or none}}

| Tier | Cases | Observations and evidence | Outcome | Limits |
| --- | --- | --- | --- | --- |
| A discovery/activation | {{cases}} | {{consultation traces; explicit/implicit distinction}} | NOT_RUN | {{limits}} |
| B output quality | {{cases}} | {{candidate and baseline outputs/grades}} | NOT_RUN | {{limits}} |
| C installed resources | {{cases}} | {{loaded paths, script execution, project outputs}} | NOT_RUN | {{limits}} |

- Run manifests/transcripts/grades: {{paths and hashes}}
- Human feedback: {{actual feedback or not obtained}}
- Resource measurements: {{observed values or unavailable}}
- Proposed disposition: {{revise / suitable for stated scope / insufficient evidence}}
- Behavioral status: NOT_EVALUATED
- Unavailable or excluded observations: {{cause and effect on scope}}
- Required refresh and next owner: {{bounded task}}
- Adoption reference: null
