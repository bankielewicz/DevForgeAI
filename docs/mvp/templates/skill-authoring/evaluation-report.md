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

For an externally selected VPR-2 validator assignment, populate the following from the frozen v2 plan and actual evidence. Other-provider and legacy reports retain their original governing policy and native obligations. The artifact envelope remains devforge.artifact/v1; it is not a protected admission or acceptance receipt.

- Policy/mode and owner acceptance pin: {{VPR-2; Routine or Full; exact source/acceptance hashes, or legacy policy}}
- Actual requested claim: {{exact wording and whether its release/support contract requires Full}}
- Owner-accepted baseline/scope and destination: {{exact identities and authority, or missing}}
- Immediate and cumulative impact: {{both diff pins, fixed anchor, affected requirement/dependency union, CI-01–CI-09 union}}
- Compatibility: {{CP-01–CP-04 dispositions and used-capability evidence; unresolved changed components remain explicit}}
- Independent T04 review: {{actual selected producer, frozen plan/review pins, selection judgment and separate R01–R10 outcomes}}
- Current routinely accepted candidate/environment: {{actual owner record identity, or none}}
- Last fully qualified candidate/environment: {{exact anchor and Full evidence, ABSENT or UNKNOWN; Routine does not move it}}
- Accepted unqualified anchor/acceptance chain: {{actual source when no qualified anchor exists; never silently reset}}

| Tier | Cases/assertions | Selection and obligation disposition | Observations and evidence | Outcome | Limits |
| --- | --- | --- | --- | --- | --- |
| A discovery/activation | {{cases}} | {{REQUIRED / reviewed NOT_SELECTED / genuine NOT_APPLICABLE; task disposition}} | {{consultation traces; explicit/implicit distinction}} | NOT_RUN | {{limits}} |
| B output quality | {{cases}} | {{same; never relabel selected failure as unselected}} | {{separate candidate and baseline outputs/grades}} | NOT_RUN | {{limits}} |
| C installed resources | {{cases}} | {{same; selected failure blocks dependents}} | {{loaded paths, script execution, project outputs}} | NOT_RUN | {{limits}} |

- Enforced task accounting: {{all T01–T12, with separate selection/disposition and observation outcome; every P1–P6 remains Enforced}}
- Assertion coverage: {{complete original catalog/variant/arm mapping, D/S/N evidence kinds, gaps and genuine scope exclusions}}
- Shared observations/batched grades: {{conditions, exact raw-output pins, separate arm/assertion judgments and correlation/sample limits}}
- Target receiving transfer before T09: {{eligible actual target output, receiver load and required action/negative disposition, or missing/unselected}}

- Run manifests/transcripts/grades: {{paths and hashes}}
- Human feedback: {{actual feedback or not obtained}}
- Resource measurements: {{observed values or unavailable}}
- Proposed disposition: {{revise / suitable for stated scope / insufficient evidence}}
- Report completion: {{COMPLETE / PARTIAL / BLOCKED; completeness is not validation PASS}}
- Validation disposition: {{ROUTINE_PASS / FULL_PASS / FAIL / INSUFFICIENT_EVIDENCE under v2, or actual legacy outcome}}
- Routine adoption eligibility: {{true/false with exact authority, byte, scope and required post-install check basis; not human approval}}
- Qualification claim and limits: {{exact current Full evidence scope or no current qualification for these bytes}}
- Behavioral status: NOT_EVALUATED
- Unavailable or excluded observations: {{cause and effect on scope}}
- Required refresh and next owner: {{bounded task}}
- Adoption reference: null
- Prepared evaluator handoff: {{path/hash and next owner; no recursive qualification or receiving invocation implied}}
