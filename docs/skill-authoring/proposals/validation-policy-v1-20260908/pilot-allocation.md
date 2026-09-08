# Proposed cost measurement pilot CMP-1

Status: **UNFUNDED DRAFT — NOT ADMITTED — NOT RUN.** Review this allocation before any preparation that launches evaluation clients, authentication, model/reviewer call, target helper or native execution. It is an allocation demand, not a grant of ten additional calls.

## Purpose and limits of the sample

Measure the costs of a focused independent review, native interactive authoring in candidate/baseline arms, independent paired grading, a native validator's nested independent review, and result return/report grading. These exercise distinct cost sources found in the preserved complete campaign without attempting its full case inventory.

Use one specimen per listed condition, one repetition and zero retries. This can produce initial observed unit costs and identify dominant overhead. It cannot estimate failure probability, stable percentiles, causal improvement, broad activation accuracy or Full qualification. Grades test whether the intended workload was actually observed; they do not qualify either utility or accept the proposed policy. Do not credit this pilot against mandatory cases or relabel it Routine PASS.

## Frozen source selections and inert packets

Candidate builder and validator: DevForgeAI `9970e92db7d824dea0c49e1a61a122480f2aa8b5`. Builder baseline: `a78b9bff83c090153952b31b84b0584ef1650f02`, labeled `old_skill`. This baseline already includes workspace allocation work; the pilot does not claim to measure improvement caused by that earlier work. Runtime reference: DevForge `c7b2a62696c7f3764fdea3313182b9e896339a2a`. These selections do not establish readiness or current runtime support for the whole pilot.

The [allocation JSON](pilot-allocation.json) freezes node IDs, profile IDs, role inputs, dependency conditions, generation limits, time accounting and measurement fields. [Pilot packets](pilot-packets.json) contain proposed raw fixture bytes and literal prompts/answer policy as data. They are not installed skills, execution directories or a controller input. Grader criteria and operator answer policy are separate entries and must not be visible to measured workers. This authoring session did not materialize native workspaces or authenticate profiles.

The builder pair receives identical ordinary facts and a request to author a small local scope-note skill. One necessary included-work input is deliberately withheld, with an explicit request to ask for it. This controlled clarification measures one operator answer and continuation; it is not a test of spontaneous question selection. The validator receives the raw request from preserved SV-010 and its raw fixture/specification, without the source case ID, diagnostic title, expected result or author conclusion. This samples a semantic static-review workload; it does not execute the complete SV-010 evaluation or replace its original results.

## Maximum model allocation

Every row permits one externally dispatched model generation at most. Seven initial generations have separate fresh profiles; three conditional rows resume only their own paused parent. No grader has a recursive grader. Model context expansion that requires another externally dispatched generation is not free.

| Node | Role and workload | Profile / parent | Maximum generation wall seconds | Admission / conditional behavior |
| --- | --- | --- | ---: | --- |
| M01 | Focused independent static review of the actual validator change from the preserved baseline, with all R01–R10 records and complete relevant context. | F01 fresh | 600 | Raw candidate/base/spec/rubric and change paths; no author diagnosis or prior grade. |
| M02 | Candidate builder authors the small fixture skill; initial turn asks the one withheld input. | F02 fresh | 240 | Exact candidate package and builder raw packet. |
| M03 | Deliver the literal answer and continue candidate builder. | F02 / M02 | 180 | Only if an actual eligible question was captured and interpreted within the frozen answer policy. No synthetic question or forced extra turn. |
| M04 | Baseline builder, same task/facts and initial conditions. | F03 fresh | 240 | Exact old-skill package; same fixture bytes and effective tools. |
| M05 | Deliver the same literal answer and continue baseline builder. | F03 / M04 | 180 | Same question-matching and deadline rule as M03. |
| M06 | One fresh independent grader assesses both builder outputs against frozen criteria, separately then paired. | F04 fresh | 600 | Neutral labels; exact outputs/transcripts or authentic failure records; no previous verdicts. |
| M07 | Native validator handles the small raw static+AI request: intake, deterministic inspection and preparation of the independent review request. | F05 fresh | 150 | Exact validator package and read-only fixture. No unallocated child/native campaign. |
| M08 | Actual fresh independent AI review requested by M07. | F06 fresh | 150 | Only after authentic request exists; raw target/spec/rubric only, without validator's diagnosis or expected result. |
| M09 | Return the authentic M08 result to the same validator parent for adjudication and reporting. | F05 / M07 | 150 | Valid matching result or authenticated failure/unavailability record; parent must remain safe, intact and within its original deadline. |
| M10 | Fresh independent grader assesses validator deliverables, evidence separation and whether the intended nested workload occurred. | F07 fresh | 600 | Exact parent/child evidence or authentic unavailable records; no worker self-grade. |

Maximum demand: **10 generations = 7 fresh profiles + 3 same-parent continuations**. M03/M05 are unused if the parent completed without the eligible question or could not ask it. A second question receives no automatic answer or extra slot. M08/M09 depend on actual protected events, not a planner-authored success flag. If a parent cannot request or receive review safely, preserve the failure and skip dependent continuation; M10 can still measure the grading/reporting cost of that authentic unavailable workload. No unlaunched row is charged as executed or reported as successful.

All generations are serialized. Candidate then baseline is one fixed order; M06 sees neutral output labels in the opposite display order. Record any arm leakage and order effects. With one pair, no counterbalanced statistical claim is possible. Shared nominal tools are not proof of equal effective assistance; record actual assistance, denied calls and model configuration unknowns.

The independent grader demand is two generations (M06/M10). Static independent review demand is two (M01/M08). M08 is also a nested review; count it once with both descriptive tags. Worker demand is six including the three reserved continuations. Internal provider requests, tool round trips, compaction and automatic retries are measured separately when observable; they do not disappear into a misleading ten-request cost claim.

## Unchanged authority and bounded time

The existing ledger remains **24 charged / 24 approved / 0 remaining**. No new cap, refund, reclaimed past slot, reset campaign or additional tranche is proposed. There is presently no authorized way to admit even the first row. Accepting this pilot's design does not change that fact. Execution needs an explicit owner decision identifying lawful funding within the user's unchanged budget constraint; if none exists, the pilot stays unexecuted. All later implementation/review demand must also fit actual authority, not be hidden outside these ten rows.

The existing 600-second **whole-attempt** and 14,400-second campaign limits remain. A parent deadline includes operator waiting, children, transport, continuation and teardown; it does not restart at a resumed turn. Proposed builder parent bound: 240 initial + 120 total operator/wait/transport overhead + 180 continuation + 60 settlement = 600 seconds. Proposed validator parent bound: 150 initial + 150 child + 150 return + 150 total transport/settlement = 600 seconds. A child inherits the minimum of its own sub-bound and the unchanged parent/campaign deadline. A return is denied when insufficient parent time remains, even if a row is unused.

All seven profiles require their actual isolated state/configuration and authorized direct subscription sign-in. Parent/child authentication occurs before admitting a parent; no credential copying, ordinary global state cleanup or reused writable histories. Recheck required freshness before launch. Authentication is not yet authorized and has not occurred.

| Reserved component | Conservative maximum seconds | Accounting |
| --- | ---: | --- |
| Ten model generation windows | 3,090 | Sum of row bounds; includes the two independent graders and two static reviews. |
| Seven fresh direct sign-ins | 4,200 | 600 each; fail/stop if unavailable, no unallocated retry. |
| Builder parent operator/wait/transport overhead | 240 | 120 per parent; actual active human time is measured separately. |
| Builder parent settlement | 120 | 60 per parent. |
| Validator nested transport/settlement | 150 | Within the unchanged 600-second parent bound. |
| Ten staging/identity/readiness windows | 600 | 60 per row, before admission when possible; no implied successful preflight. |
| Final custody, operator review and closeout | 1,800 | Reporting included, even on partial execution. |
| Non-model contingency reserve | 600 | Cannot become an extra model call or extend any individual/parent cutoff. |
| **Pilot elapsed ceiling** | **10,800 (3 hours)** | Within the unchanged 14,400-second ceiling; includes all listed execution preparation and closeout. |

The component maxima sum to 10,800 seconds. These are allocation bounds, not measured estimates. Continuation staging that happens while a parent is open must also fit that parent's existing overhead sub-bound; the global staging reserve cannot extend a parent deadline. Any overlap is accounted once in actual elapsed measurements. This is a proposed smaller window, not a newly bound clock. Pre-execution engineering that does not yet exist is an explicit blocking prerequisite; it is not asserted to fit a sixty-second staging slot or authorized as hidden pilot work. A future execution allocation must account for any such work before admission without silently extending the user's limits.

## Measurement contract

Record raw events with UTC timestamps and monotonic elapsed offsets, exact run/node/profile/parent identities, event source and final byte locators. Retain the original records; derived tables link their input hashes. Never collect credentials, access tokens or hidden model reasoning.

For each node collect: externally dispatched generations; actual model identity/configuration when observable; input, cached-input, output and other reported token categories with provider definitions; observable internal model request/retry/compaction counts; tool-call counts; packet bytes; launch, generation, first-output, end and settlement times; outcome and stop reason. Missing counters are `NOT_OBSERVABLE` with a cause, never zero. Distinguish unavailable fields from actual observed zeros. Record token totals once at their native scope; do not add a cumulative session total to its turn deltas. A subscription generation count is not a monetary API charge.

For grading report M06/M10 separately: grading generations/tokens, packet preparation time, grader elapsed time, operator adjudication time, and disagreements/unavailability. Report M01/M08 review overhead separately; keep M08's nested role without double counting its cost.

The operator records active intervals for preparation, boundary checks, each sign-in, interpreting the actual question, sending the permitted answer, nested review transport, monitoring/intervention, grade review and final custody. Record waiting/idle intervals separately. A measured answer turnaround is not all active human work. If multiple people participate, sum person-seconds by person without overlapping intervals for the same person.

Total elapsed cost is the union of actual intervals from preparation through closeout. Parent spans overlap their child spans; do not add both to total wall time. Report parent elapsed and component times as different views. Do not subtract operator waiting from enforcement deadlines. “Model service time” is reported only if directly observed; otherwise use generation wall time and separately visible tool/wait intervals, without inferring server compute.

Deliver `cost-events.jsonl`, `cost-observations.json`, per-node raw usage evidence, operator interval log, independent review/grade records, and a `measurement-report.md` with sample counts, completion/censoring, strata, token/time/operator totals and unknowns. These are future output names; no empty file here is a measured result.

## How to use the results

For each workload stratum report the observed count, individual values, median only when meaningful, range, and whether a timeout censored the observation. With one specimen, report that value as one observation rather than a distribution or confidence interval. Include failed/blocked/timeout costs in incurred totals and mark intended workload components not observed.

Estimate a future **explicitly selected** Routine allocation by multiplying each stratum's observed unit cost by its required count, adding fixed setup, sign-in and closeout work once, and showing sensitivity to unobserved/variable components. Keep input/output token categories separate. Do not multiply a tiny fixture's cost across all 1,099 full-campaign units without a justified workload map; complex control, activation, receiver and long-context strata are unsampled here. List these gaps and use bounds or unknowns, not invented measurements.

The pilot report can conclude “measurement complete for these observed components” or “partial measurement.” It cannot conclude skill qualified, routine validation passed, native campaign accepted or budget automatically revised. Further sampling would need a separately reviewed allocation and real remaining authority; this pilot includes none.

## Admission blockers and review boundary

Before any execution, the owner must accept the pilot design, retain the original budget ledger, establish actual available funding, freeze fresh collision-safe workspace/output/client-state paths and exact installed manifests, and select a demonstrated native method with real filesystem/process boundaries. Nested fresh review plus counted same-parent return must be supported by that method and independently checked. A documented command or synthetic boundary record is insufficient. No unsupported broker or unconfined fallback is assumed.

The chosen method must support this cost-measurement scope without a fabricated qualification gate. If it requires an additional model-driven bootstrap, resource probe, controller decision or review, that is unallocated here: stop and revise the pilot demand for review within the unchanged limits. Do not hide such a call in non-model staging, treat it as free, or bypass a currently enforced C/B/A prerequisite by renaming a qualification run. Deterministic preflight is also bounded and must produce actual evidence.

Policy specification acceptance does not prove these conditions. If its new Routine semantics are to be exercised, their implementation and independent verification are additional prerequisites; this pilot's existing static-only validator request does not pretend the proposed policy is already installed. Prepared packets and this document remain inert until those conditions and explicit execution authority exist.
