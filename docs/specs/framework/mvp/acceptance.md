---
id: DFF-MVP-02
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# MVP acceptance scenario design

[MVP scope](scope.md) · [Evaluation protocol](../evaluation/benchmark-protocol.md) · [Quality owner](../quality-and-delivery.md)

## Meaning and current status

These are required observable scenarios for the selected candidate. They are not executed results or a runnable QA suite. Fixture bytes, commands, approved denominators, supported profile, budgets and independent expected outputs remain unresolved. Every row is currently NOT_RUN. The next contract task must turn the selected subset into exact test cases before its implementation begins; record the complete required-case inventory before qualification rather than silently treating each prose row as one test.

Inputs are a bound scope/policy, engine and Codex execution profile, starting candidates, selected expertise, fixture definitions and expected outcomes. Outputs are attributed executions, actual artifacts, per-case results, unresolved defects, and the narrow decision justified by that evidence. Implementation and QA must preserve separate ownership of independent oracles. Framework acceptance belongs to the qualified Rust authority, not to this document, a Python script or a model-authored result.

## Candidate scenarios

| ID / scope | Trigger or setup | Required observation and failure condition |
| --- | --- | --- |
| MC-01 / MVP-01 | Adequate existing repair specification; separate input with a missing business decision | Reuse the adequate contract and identify the exact missing decision in the other case. Inventing business truth or demanding unrelated planning artifacts fails. |
| MC-02 / MVP-02 | Two repair obligations; a later instruction adds platform coverage testing | Both repairs remain selected alongside testing. Scope removal requires an attributed amendment; treating testing as replacement fails. |
| MC-03 / MVP-03 | Worker ends while an authorized repairable obligation remains | Rust-owned mode retains the obligation and dispatches the next permitted action within declared bounds, or reports the concrete blocking condition. Worker completion alone cannot finish the run. Rust-assisted mode must be evaluated under its reduced claim. |
| MC-04 / MVP-04 | A meaningful selected behavior is absent; developer test exposes it | Preserve valid executed Red, minimum Green, relevant refactor evidence and regression/QA results. Setup errors, passing stubs and weakened assertions do not count. |
| MC-05 / MVP-04/05 | Developer tests pass but independent QA exposes a specified integration or negative-path defect | Retain the QA finding/oracle; deliver a repair and independent retest of the new candidate. Editing away the required scenario or self-closing the finding fails. |
| MC-06 / MVP-05 | Passing evidence for candidate A; current source is candidate B; editable workspace PASS is submitted | No current qualification follows from stale evidence or the editable claim. Failure output identifies the mismatched/missing prerequisite. |
| MC-07 / MVP-05 | One selected platform passes; another fails or is unexecuted | Counts, percentages and missing cases stay distinct per platform; another host cannot qualify the missing target. Numeric floors cannot waive a mandatory failure. |
| MC-08 / MVP-06 | Long-running job, repeated update reads, duplicate submission after uncertain response | Return bounded new events plus current status; updates do not duplicate work. Heartbeats are labeled as liveness. Counters are observed, not elapsed-time estimates. |
| MC-09 / MVP-06 | Interruption before dispatch, during an external command, and after result persistence but before response | Recover exact known state, reconcile uncertain effects, preserve prior results, and avoid blind duplicate execution. A stale PID or summary alone is insufficient proof. |
| MC-10 / MVP-03/06 | User cancellation, pending approval, unavailable worker, exhausted declared bound or account limit | Respect cancellation and actual permissions; retain incomplete obligations and the stop reason. No silent API switch, approval fabrication or unbounded worker loop. |
| MC-11 / MVP-07 | Same workflow on two identified projects with materially different rules | Follow the selected project's policy/context and preserve project/checkout isolation. Renaming the same fixture or exporting DevForgeAI-only policy as universal fails. |
| MC-12 / MVP-08 | Grounded expert fact changes; a control input changes only cosmetically | Record the relevant contradiction and bounded realignment handoff; retain unaffected knowledge with evidence. Automatic operational edits or treating every changed byte as a semantic defect fails. |
| MC-13 / MVP-05 | Worker attempts direct acceptance-state modification, stale transition or forged reviewer identity | Under the claimed protected profile, actual permission/authority controls reject the attempt and preserve valid state. An unprotected prototype reports that limitation rather than passing this scenario. |
| MC-14 / MVP-04/06/07 | Complete selected change, then cold resume from retained records by another session | Reproduce the identified candidate, explain delivered and outstanding scope, and retrieve bounded relevant context without assuming the previous conversation. Missing artifacts remain explicit gaps. |

MC-03 through MC-10 include separate positive and negative cases to define in the runnable inventory. A denominator cannot be inflated by counting retries as new successes or reduced by omitting hard cases. Existing prior evidence remains about its identified old candidate; it is not this candidate's execution.

## First complete walkthrough

Use the [scope's OrderDesk example](scope.md#walkthrough-selection) to connect the records rather than testing disconnected flags. Resolve the dispatch definition and concurrency contract first. Bind the selected cancellation requirement, write and execute a focused failing test, implement it, have independent QA challenge the concurrent operation, retain the defect, repair it, and retest. Add a verification request while the repair remains outstanding and interrupt/resume at one declared point. The profile and exact expected interleavings must be specified; this narrative does not supply them.

Use a second selected project to test adaptation of the same core workflow. Define its expected policy difference before execution so the test cannot merely accept whatever the framework chose. Include a stale expertise assertion and unchanged control. Project adaptation and native engine platform qualification are separate conclusions.

## Evidence and judging

The runnable definition must bind inputs, source/build identities, tools, command arguments, cwd, host/filesystem, timestamps, exit codes, captured stdout/stderr, required case identities, source denominator/exclusions, report references and reviewer provenance. Protect independent expected results against worker edits. Missing reports, unreadable artifacts, skipped cases and absent hosts are explicit gaps, not assumed passes.

For framework implementation, enforce the repository's >=95% executed-line coverage and >=95% required-case pass rate independently, without rounding a subthreshold result upward. Retain branch coverage separately where available. Neither threshold compensates for failed mandatory behavior or authority invariants. These are implementation qualification conditions; the benchmark separately measures useful delivered outcomes.

An independently demonstrated harness error invalidates its affected observation and must retain the failed attempt and correction. A product failure, exhausted declared execution budget or missing required product result remains unsuccessful. Respecting cancellation can satisfy MC-10 while leaving the product change incomplete. A justified no-change outcome may be correct where the selected requirement already holds, with evidence and no unnecessary edit.

## Readiness blockers and next output

AMB-01/02/03/05/07/08/09/12/16/17 cover host, identity, schema, independence, invalidation, limits, bindings and storage. AMB-18 covers the comparative workload and judging protocol; AMB-19 covers the first code unit and destination. Select exact fixture bytes and independent oracles, failure classifications, required platforms, resource limits, and tool commands before coding that unit. The next output is a bounded executable test contract with immutable inputs, not a checked-off copy of this table.
