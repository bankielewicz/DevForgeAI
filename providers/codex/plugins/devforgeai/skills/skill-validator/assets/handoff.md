---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project-id}}"
revision: 1
status: draft
created_at_utc: "{{actual-UTC-time}}"
producer:
  skill: "skill-validator"
  skill_revision: "{{exact-loaded-validator-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prepared skill validation handoff

Populate at completion, transfer or recovery using only observations already available when this document is authored. A prepared handoff is substantive continuation, not a runtime receipt or receiving invocation. Never amend it to claim a later check, publication or delivery event.

## You are here

- Skill/use case: skill-validator evaluating {{exact target and goal}}.
- Current phase / task state: {{P1-P6; complete reporting / partial / blocked}}.
- Candidate passing state: {{separate from reporting completion}}.
- Assignment / write fence: {{actual authority reference and permitted paths}}.
- Authorization carried forward: {{existing user scope; no inferred additional permission}}.

## Inputs and completed outputs

Reference saved complete files; never include this handoff's own digest or create circular receipt references. Runtime owns managed final identities and authoritative custody. If those identities have not yet been supplied, retain the exact path with null and a cause. Unmanaged ordinary source/write identities may be labelled as author observations.

| Direction | Artifact / revision | Path | SHA-256 | Relevant IDs | Freshness / decision state |
| --- | --- | --- | --- | --- | --- |
| input | {{candidate manifest/spec/plan}} | {{path}} | {{digest or unavailable cause}} | {{requirements}} | {{state}} |
| output | {{verification report}} | {{path}} | {{digest}} | {{F IDs}} | {{state}} |
| output | {{decision receipt or explicit unavailable}} | {{path or none}} | {{digest or none}} | {{checks}} | {{state}} |
| output | {{enhancement specification}} | {{path}} | {{digest}} | {{CHG IDs}} | {{state}} |

## Observed verification and remaining work

| Group / task | Outcome | Exact raw evidence / receipt | Cause or limit |
| --- | --- | --- | --- |
| {{intake/structure/AI/C/B/A}} | {{outcome}} | {{path and digest}} | {{limit}} |

Observed discoveries, supported defects, and new proposals: {{separate each}}.
Unavailable observations: {{causes, scope effects, owners}}.
Target edited by validator: No.
External acceptance / adoption: {{actual reference or not granted / null}}.

## Continuation

| Order | Task | Owner | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{apply justified changes, or resolve missing evaluation prerequisites}} | {{skill-builder or operator}} | {{CHG IDs and authority, or runtime facts}} | {{authored revision/change record or boundary receipt}} |
| 2 | Reevaluate affected findings and regressions | skill-validator | {{new candidate identity and fresh frozen plan}} | {{new evidence and closure records}} |
| 3 | Consider adoption for the observed scope | {{external acceptance owner}} | {{required evidence}} | {{actual decision reference}} |

## Next-session prompt

Use skill-builder to implement the authorized CHG items in {{enhancement specification path and digest}} against {{candidate manifest path and digest}}. Preserve {{requirement IDs}} and the existing enforcement choices. Write only within {{canonical scope}}. If identities differ, reconcile the change against the retained candidate before applying it. Return the new source manifest, change record and updated specification. Do not execute validation or activate hooks. Return the result to skill-validator for the listed reruns.

When no target changes are justified, replace that prompt with the concrete operator/evaluation prerequisite task. Use an actual available skill name; do not invent a command or imply another skill has already run.

## Custody and invalidation

- Saved output paths and readback: {{completed outputs only}}.
- This handoff location: {{actual saved path; no self-digest}}.
- External handoff receipt: {{actual preexisting reference or null; later publication/readback NOT_RUN at creation}}. Protected runtime owns managed final-byte checks, snapshot, receipt publication/readback and transport. Do not call a receipt helper or controller as a fallback; never write a later digest back into this document.
- Owned processes and assignment disposition: {{actual identities; retained/handed off/released with owner record}}.
- Invalidating changes: {{candidate, installed copy, cases, rubric, contracts, baseline, runtime, assignment}}.
- Resume point: {{last completed phase and exact pending task}}.

## Workspace preparation and native continuation

- Selected environment and carried authorization: {{actual choice and source}}.
- Frozen workspace allocation references/count/paths: {{saved path and SHA-256, or non-Git reason}}.
- Preparation observations: {{saved setup references; actual retained paths and statuses}}.
- Remaining native inputs/readiness: {{model/auth/budgets/observations/boundaries still missing; no inference from creation}}.
- Complete experiment plan and attempt/workspace/client-state bindings: {{saved refs, or explicit pending cause}}.
- Additional workspaces: {{new bounded allocation or none; no silent independent-attempt reuse}}.
- Protected runtime admission/integration status: {{actual evidence or unavailable; no active-enforcement claim from templates}}.

Prepared workspaces can be delivered with native execution NOT_RUN and dependent observations COULD_NOT_RUN. Preserve all old allocations, setup records, plans and attempts. No cleanup, acceptance or release follows from preparation.

## Creation-time runtime observations

| Observation | Outcome at creation | Exact evidence or missing cause |
| --- | --- | --- |
| Handoff preparation | {{prepared / partial}} | {{saved substantive outputs}} |
| Protected final-byte checks | {{observed / NOT_RUN}} | {{actual evidence or null with cause}} |
| Runtime receipt publication/readback | {{separate actual observations / NOT_RUN}} | {{actual evidence or null with cause}} |
| Runtime transition admission | {{observed / NOT_OBSERVED}} | {{actual evidence or null with cause}} |
| Receiving skill invocation | {{observed / NOT_RUN}} | {{allocated execution evidence or null with cause}} |
| Rendered human delivery | {{observed / NOT_OBSERVED}} | {{actual observation or null with cause}} |

These fields do not authorize new execution, expand the budget or transfer a protected lease. Changed source, installation, runtime, assignment or accepted inputs requires affected reconciliation and new evidence.

## VPR-2 claim and lineage

For a VPR-2 skill-validation handoff, retain the following from the frozen plan/results; for other workflows, retain their governing contract and mark this policy block outside scope. This optional reporting block does not change the devforge.artifact/v1 envelope or issue execution authority.

- Policy and actual requested claim: {{version/source/acceptance pins, Routine or Full, exact claim and any Full-required contract}}
- Accepted baseline/scope and impact: {{owner decision, immediate/cumulative diff pins, fixed anchor and affected dependency union}}
- Current routinely accepted identity: {{actual candidate/environment and acceptance-chain pin, or none}}
- Last fully qualified identity: {{candidate/environment and exact Full evidence, ABSENT or UNKNOWN; unchanged by Routine}}
- Validation/report dispositions: {{separate ROUTINE_PASS/FULL_PASS/FAIL/INSUFFICIENT_EVIDENCE and COMPLETE/PARTIAL/BLOCKED}}
- Conditional native coverage: {{reviewed selections and independent T04 pin; unselected observations remain NOT_RUN}}
- Owner acceptance/install authority: {{actual carried decision and conditions, or not granted}}
- Deferred qualification observations: {{required actual native/compatibility/control/receiving evidence and next owner}}


Target receiving evidence: {{actual eligible target output, receiver load and completed action before Full T09, or missing}}. This evaluator T12 handoff enqueues zero recursive qualification calls.
