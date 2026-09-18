# Template: QA test plan

**Producer:** current `qa` modes `plan` / `run` / `execute` / `retest`  
**Consumers:** same `qa` invocation (run/execute/retest); human for explicit planning-only  
**Operational template:** `src/agents/skills/qa/assets/test-plan-template.md`  
**Does not:** execute product tests in explicit plan mode; repair product source; claim PASS.

## Envelope

| Field | Value |
| --- | --- |
| Plan / run identity | |
| Intent | run / plan / execute / retest |
| Planning status | READY / NEEDS_INPUT |
| Execution status | NOT_STARTED / IN_PROGRESS / COMPLETED / STOPPED |
| Producer | qa |
| Downstream consumer | qa execution, or human if planning-only |
| Failure behavior | NEEDS_INPUT blocks only dependent cases |
| Non-claims | A saved plan is not a QA verdict |

## Upstream inputs

| Role | Locator | SHA-256 |
| --- | --- | --- |
| Specs / stories | | |
| Candidate source / build | | |
| Project policy | | |
| Development delivery | | optional |
| Prior plan (execute/retest) | | if any |

## Evidence destination

- Literal selected evidence value:
- Resolved run directory:
- Role-to-path map: plan, manifests, receipts, report, qa-fix, checkpoint

## Criterion and case inventory

| Criterion | Required behavior | Mandatory? | Cases | Independent oracle | Readiness |
| --- | --- | --- | --- | --- | --- |
| | | | | derived from spec, not from dev report | READY / BLOCKED |

Every selected clause is inventoried, including errors, recovery, concurrency, platforms, and documentation obligations.

## Environment matrix

| Platform | Tools / versions | Native/visual needed | Readiness / missing prerequisite |
| --- | --- | --- | --- |
| | | | |

## Metrics declared before execution

- Executed-line denominator and exclusions:
- Required unit-case denominator (include skipped/blocked/unexecuted):
- Floors: coverage and unit pass rate each >= 95% or stricter project policy
- Other suite thresholds kept separate
- Partial collection: no final percentage

## Integrity inspection plan

- First-party mock-decorator / gaming checks:
- Candidate preservation method:
- Stop classes: INTEGRITY_FAILURE, METRIC_FAILURE, CRITICAL_PRODUCT_DEFECT stop the whole run

## Downstream handoff

**Full run:** after readback and integrity inspection, continue into ready execution in the same invocation. Do not ask the user to re-select this plan.

**Planning-only:** verdict marker `NOT_EVALUATED`. Provide a copyable execute prompt only when planning was explicit.

**Return path:** identity drift invalidates affected evidence; do not replay uncertain effects.
