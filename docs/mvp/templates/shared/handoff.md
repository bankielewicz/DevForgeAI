---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "{{producing-skill}}"
  skill_revision: "{{exact-producer-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill handoff

## You are here

- Skill and use case: {{name and goal}}
- Current phase: {{phase}}
- Task state: {{complete / partial / blocked; distinguish from document status}}
- Session/worktree assignment: {{external SESSION reference}}
- Exact candidate or artifact scope: {{identity}}
- Existing authorization carried forward: {{reference}}

For a VPR-2 skill-validation handoff, retain the following from the frozen plan/results; for other workflows, retain their governing contract and mark this policy block outside scope. This optional reporting block does not change the devforge.artifact/v1 envelope or issue execution authority.

- Policy and actual requested claim: {{version/source/acceptance pins, Routine or Full, exact claim and any Full-required contract}}
- Accepted baseline/scope and impact: {{owner decision, immediate/cumulative diff pins, fixed anchor and affected dependency union}}
- Current routinely accepted identity: {{actual candidate/environment and acceptance-chain pin, or none}}
- Last fully qualified identity: {{candidate/environment and exact Full evidence, ABSENT or UNKNOWN; unchanged by Routine}}
- Validation/report dispositions: {{separate ROUTINE_PASS/FULL_PASS/FAIL/INSUFFICIENT_EVIDENCE and COMPLETE/PARTIAL/BLOCKED}}
- Conditional native coverage: {{reviewed selections and independent T04 pin; unselected observations remain NOT_RUN}}
- Owner acceptance/install authority: {{actual carried decision and conditions, or not granted}}
- Deferred qualification observations: {{required actual native/compatibility/control/receiving evidence and next owner}}

## Inputs consumed and outputs produced

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{state}} |
| output | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{state}} |

## What changed and what remains open

{{Concrete outcome, new proposals versus adopted decisions, unresolved questions, and work not completed.}}

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| {{check}} | NOT_RUN | {{reference}} | {{cause/limit}} |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{one immediate next task}} | {{user / skill / external operator}} | {{required inputs or decisions}} | {{artifact/receipt}} |
| {{later optional order}} | {{follow-on work if useful}} | {{owner}} | {{dependency}} | {{evidence}} |

## Copyable next-session prompt

Goal: {{one concrete result}}
Context: {{exact artifact references and the relevant sections}}
Output: {{named template/deliverable and permitted destination}}
Boundaries: {{assigned worktree/fence, existing decisions, and consequential limits}}
Verify: {{observable completion checks}}

Use an actual installed skill name or known command. If the capability is not implemented, make the next task authoring/evaluation of that capability; do not present a fictional command as runnable.

## Resume and custody

- Authoritative saved output and readback: {{path and digest, or not yet persisted}}
- Worktree ownership disposition: {{retained / handed off / released with operator reference}}
- External gate state: {{actual receipt reference, not an inferred phase}}
- Conditions invalidating this handoff: {{source, candidate, runtime, or assignment changes}}
- Target receiving evidence: {{when qualification requires it, actual eligible target-produced output and receiver action observed before T09; not this prepared evaluator handoff}}
- Handoff execution state: {{prepared / actual receiving invocation observed with evidence; a prepared T12 handoff enqueues no recursive evaluator qualification}}
