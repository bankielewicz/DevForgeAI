---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-{{number}}"
artifact_type: "expert-evaluation-report"
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

# Expert evaluation results

## Bound identities

- Evaluation plan: {{EVPLAN-ID@revision}}
- Candidate source and installed digests: {{exact identities}}
- Baseline identity: {{no skill or prior package digest}}
- Terminal/version/model configuration: {{observed values}}
- Actual execution assignments: {{session/worktree references}}
- Independence conditions met: {{yes/no and evidence}}

## Discovery and activation

| Check | Actual observation | Outcome | Evidence |
| --- | --- | --- | --- |
| Native installed-skill discovery | {{observation}} | NOT_RUN | {{reference}} |
| Explicit activation | {{observation}} | NOT_RUN | {{reference}} |
| Indirect activation | {{observation}} | NOT_RUN | {{reference}} |
| Similar request does not activate | {{observation}} | NOT_RUN | {{reference}} |

## Behavioral comparison

| Case ID | Candidate output/evidence | Candidate outcome | Baseline output/evidence | Baseline outcome | Constraint violations |
| --- | --- | --- | --- | --- | --- |
| ECASE-001 | {{artifact reference}} | NOT_RUN | {{artifact reference}} | NOT_RUN | {{findings}} |

## Interpretation and limits

- Recommendation: {{suitable for stated scope / revise / insufficient evidence}}
- Behavior status: NOT_EVALUATED
- Covered task and runtime scope: {{observed coverage}}
- Observed time/token metrics, if available: {{measurements or unavailable}}
- Unavailable checks and causes: {{items}}
- Findings routed to creator: {{case IDs and evidence}}
- Candidate adoption reference: null
- Handoff reference: {{HANDOFF-ID@revision}}

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
