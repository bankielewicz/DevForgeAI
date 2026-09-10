---
schema_version: "devforge.artifact/v1"
artifact_id: "EVPLAN-{{number}}"
artifact_type: "expert-evaluation-plan"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Expert evaluation plan

## Candidate and task identity

- Expert specification: {{XSPEC-ID@revision}}
- Exact candidate package: {{XPKG-ID@revision and digest}}
- Relevant project facts: {{same raw inputs supplied to candidate and baseline}}
- Target terminal/version/model configuration: {{observed or planned}}
- Evaluation session/worktree references: {{separate assignments}}
- Required independence and how it is established: {{actual process, not merely a role name}}

## Runtime and discovery checks

{{How to observe installed skill discovery, explicit activation, indirect activation, supporting-resource resolution, and installed revision identity. A --version result is not a discovery test.}}

## Evaluation cases

| Case ID | Request / input fixture | Expected behavior | Source expectation | Negative condition | Outcome criterion |
| --- | --- | --- | --- | --- | --- |
| ECASE-001 | {{realistic task}} | {{observable result}} | {{XCASE/rule reference}} | {{violation}} | {{pass/fail condition}} |

## Comparison and grading

- Baseline: {{no skill for a new capability / prior revision for an improvement}}
- Equal underlying context and tool access: {{how ensured}}
- Output locations: {{separate candidate and baseline paths}}
- Grading method: {{behavioral artifacts and executable checks where applicable}}
- Held-out or repeated cases: {{proportionate choice and rationale}}
- Decision threshold defined before execution: {{threshold}}
- Resource/time bound: {{bound}}
- Limitations: {{sampling, independence, runtime, or tool limits}}

## Common A/B/C evidence

- Tier A: {{native explicit invocation, direct/indirect consultation, and negative outcomes separately}}
- Tier B: {{candidate versus old_skill/without_skill outputs and requirement-based grades}}
- Tier C: {{installed resource resolution, source visibility, and consuming-project output paths}}
- Run manifests: {{devforge.skill-run/v1 records and exact identities}}
- Authored cases/fixtures and fixed trigger split: {{paths and hashes}}
- Sibling availability and actual invocations: {{separate observations}}
- Client/harness version and subscription execution method: {{verified method}}
- Human feedback and metrics: {{observed or unavailable}}

## Promoted Codex content mapping

Reference the exact detailed source and its stable sections; do not duplicate an independently maintained design/report. XSPEC maps to skill-design-spec.md; XPKG maps to the candidate file/provenance manifest; EVPLAN maps to validation-plan.json; EVREPORT maps to verification-results.md, validation-results.json and decision.json. Preserve original artifact IDs and exact input revisions/hashes. Include actual Routine/Full selection, requested claim, current/qualified lineage, unresolved evidence and next user-mediated handoff where applicable. A prepared handoff is not receiving execution.
