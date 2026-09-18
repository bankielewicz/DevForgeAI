# Developer review of corrected process and error boundaries

Review scope: all of changed process_windows.rs and protocol.rs, their callers in runner.rs, all added remediation tests and peer branches, unchanged existing process/negative-path tests. This is developer review, not independent finding closure.

## Process ownership / IQ-06

Atomic PROC_THREAD_ATTRIBUTE_JOB_LIST attachment, noninheritable Job Object, kill-on-last-handle-close, inherited three-pipe handle list, CREATE_NO_WINDOW and no-breakaway flags remain unchanged. Child endpoints are dropped in the parent after spawn. The new writer owns only the parent stdin handle, never the job handle. It accepts one outstanding write; completed sends preserve order and exact JSONL bytes. A cancelled/timed-out send leaves uncertain delivery marked pending, and subsequent sends fail rather than queueing a retry. Session RPC deadline starts before send, server reply writes use the receive deadline/control state, initialized uses the capped RPC deadline, and interrupt send/wait consume one shared grace interval. The existing owned-job teardown unblocks a stalled writer by killing all pipe readers. Stopped verification now also observes writer-thread completion. Stop and Drop target held Job Object handles, not recovered PIDs. No stdout/stderr reader behavior or authority boundary was changed.

Four new real-process integration groups passed: full server reply with peer/descendant held handles for deadline/cancel; ordinary large RPC-shaped writes with deadline/cancel/invalid-control and subsequent interrupt; a full 4096-byte pipe with no pending send followed by a blocked interrupt under a single grace budget; malformed errors through the actual CLI. The 4096-byte fill assumption is an observed Windows fixture property: the fill completes and the subsequent interrupt consumes its deadline. It is not a portable pipe-size claim.

Fresh copied IQ-03 stdin/Ctrl+C/forced-owner-death probes observed peer and descendant handles initially unsignalled and finally signalled. IQ-01 outbound trace and strict result-negative controls and IQ-04 read-only/pagination probes passed. These support IQ-06 within the original bounded process-review scope. No arbitrary file/network isolation or native Codex behavior is established.

## Sanitization / F-02

Captured v2/TurnCompletedNotification.json defines 13 string categories, four HTTP variants with nullable/optional uint16 status and activeTurnNotSteerable with review/compact. Runtime error_category reconstructs only these fields. Outer unknown/multiple categories and invalid required values return protocol_error before journal append/emit. Nested extension fields are omitted; supported categories and approved numeric/null/absent details survive. Free-form error message/details are omitted. RPC error_code is extracted as signed integer before append/emit; malformed objects, strings and fractional codes are rejected. Negative fixtures are synthetic only.

Regression tests check actual CLI stdout/stderr plus persisted journal for marker absence and assert exact retained approved fields and terminal reasons. Existing usageLimitExceeded and token-counter regressions remain unchanged. The original IQ-05 fixture now yields protocol_error without private marker retention.

## Integrity and limits

No changed thresholds, dropped original tests, skips, mock-generated behavior or coverage exclusions. The peer remains an explicit external deterministic dependency. Existing fixture/oracle bytes are unchanged. Refactor consists of central bounded writer operation and field projection; further restructuring would add unrelated churn. Full regression reruns those paths on the same runtime bytes.

The copied IQ-02 helper still marks its deadline subfixture FAIL because it expects exit 4. Raw result is preserved: actual exit 6, timed_out/deadline, 0.797 seconds, stopped peer, unchanged fixture, no external termination. Section 4 specifies exit 6 for deadlines and the fix packet permits bounded timeout. Independent QA must assess this expectation mismatch; this review neither changes that helper nor grants QA closure. Native WN-01/WN-02 and production-duration *blocked-write* trials are NOT_RUN; unchanged WF-16 still checks the production receive watchdog. External framework acceptance NOT_EVALUATED.
