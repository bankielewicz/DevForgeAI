# QA Report

## Identity and scope
- QA run and mode: [identity; run/plan/execute/retest]
- Plan readiness: [READY/NEEDS_INPUT; basis and blocked IDs]
- Execution status: [NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED; COMPLETED is not PASS]
- Plan path and SHA-256: [actual reference]
- Project and execution environment: [resolved identity]
- Candidate source/build identity: [manifest/hash and artifact references]
- Specification/story inputs: [paths, revisions, hashes]
- Requested scope and exclusions: [explicit selection and reasons]
- Development handoff: [reference or not supplied]
- QA verdict: [PASS/FAIL/INCOMPLETE; explicit planning-only uses NOT_EVALUATED as a non-verdict marker; static full-run FAIL may have execution NOT_STARTED]
- Decision basis: [confirmed facts; no unsupported acceptance claim]

## Acceptance traceability
| Criterion and source | Required behavior | Case IDs | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [criterion] | [behavior] | [cases] | [observable oracle] | [observation] | [status] | [bound references] |

## Test integrity
- Inspected first-party scope and omissions: [inventory/reference]
- Mock-decorator result: [findings or bounded clean evidence or incomplete]
- Result-gaming assessment: [findings, source/assertion review, negative controls]
- Aliases/dynamic behavior and remaining uncertainty: [details]
- Supplied versus independently executed evidence: [classification]

## Metrics and environments
| Platform | Metric | Numerator | Denominator | Exact percentage | Required floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [platform] | [line coverage/unit pass rate] | [count] | [count] | [value or unavailable] | [effective floor] | [status] | [reference] |
- Source/test inventory, exclusions, and tool versions: [references]
- Separate acceptance/integration/regression results: [counts and references]
- Unavailable platforms or measurements: [cases and reasons]
- Collection scope and completion evidence per metric/platform: [contributing cases, terminal outcomes, collector usability and bound denominator]
- Complete versus partial/unavailable metrics: [valid final counts/ratio or retained partial counts with no final percentage/threshold decision]
- Applicable project-wide suite threshold results: [separate inventory, counts, floor and evidence]
- Metric-trigger decision: [valid completed measurement, exact floor comparison, issue ID or none; no second collection after terminal stop]

## Defects and unresolved work
| Defect/gap ID | Criterion/policy | Issue class and demonstrated impact | Confirmed failure or missing evidence | Exact artifact and owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| [ID] | [reference] | [QAP-006 class and observed impact] | [confirmed finding or exact gap] | [verified artifact path and dev/prerequisite owner] | [reference] |
- Advisory items outside mandatory scope: [explicitly separate list or none]
- Remaining test/qualification obligations: [case IDs and prerequisites]

## Continuation, stopping and remaining obligations
- Observation/decision order: [stable issue/case/attempt IDs, timestamps or sequence and actual test-launch records]
- Continuation/stop decision: [terminal/nonterminal, classification, trigger ID/evidence, governing requirement and demonstrated impact]
- Reclassifications: [original observation, revised class and evidence-backed reason or none]
- Affected/blocked dependents and reasons: [case IDs and prerequisite/trigger references]
- Independent checks continued: [IDs and identity/safety/readiness/oracle basis or none]
- In-flight work at stop: [owned operation identities, safe cancellation or bounded shutdown/drain and observed disposition]
- Tests stopped and still required: [case IDs; NOT_RUN with trigger ID; preserve observed FAIL/ERROR]
- Partial metrics, remaining fixtures and uncertainty: [actual observations; stopped run never claims complete testing]
- Cleanup: [QA-owned state, necessary actions, results/errors and unresolved state; no claimed unobserved cleanup]

## Disposition
- Product QA outcome: [verdict and basis]
- Remediation owner on FAIL: dev
- Fix packet path and SHA-256: [reference or not applicable]
- Source/candidate drift check and cleanup: [actual results]
- External framework acceptance: [actual authority reference or NOT_EVALUATED]
- Release/deployment authorization: [separate supplied decision or not granted]

## Artifact delivery
- Original evidence selection and bound artifact paths: [literal destinations and role map]
- Required versus actual delivery/readback: [plan/report/fix/checkpoint/external manifest, hashes or exact failure/undelivered status]
- Final external manifest: [path and exact entry names for mutually referencing file hashes; no circular self-hash]
- Recovery action for failed writes/readback: [exact artifacts, original destination and owner/action; no silent substitution; confirmed FAIL retained]

## End-user handoff
- Open this project/environment in Claude Code: [actual resolved location/host]
- Next owner: [dev, prerequisite owner, QA resume, or project-defined downstream reviewer]
- Next action: [dev remediation, QA execution/retest, prerequisite resolution, or downstream review]
- Skill availability observation: [skills actually listed in the session, or missing prerequisite]
- Paste into the Claude Code session input: [complete resolved prompt in a fenced text block]
