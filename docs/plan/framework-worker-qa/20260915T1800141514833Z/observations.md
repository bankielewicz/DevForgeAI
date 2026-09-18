# Independent observations before final sanitization probe

## F-01 — Worker stdin backpressure stalls deadline and cancellation

Classification: MANDATORY_PRODUCT_DEFECT, high severity, independently reproduced by IQ-02-deadline and IQ-02-cancel on unchanged candidate. Continue safe independent checks; no critical data loss, unauthorized external effects or escaped process tree demonstrated by these probes.

Contract sections 4–6 require bounded dispatch, RPC, cancellation and teardown. The library permits shorter test deadlines. Driver sets total=750 ms, RPC=500 ms, grace=200 ms, teardown=500 ms; cancellation subfixture sets the flag after 300 ms. A 262,144-character string request ID fits the captured RequestId type (ServerRequest.json:1708) and incoming line/output budgets. Unsupported requests must receive a bounded rejection, never indefinitely stall ownership.

The independently written peer receives initialize, sends its request completely, records large-request-sent, and makes no further stdin reads. Both driver executions remain alive at the external 3-second deadline, as does the independently held peer handle. Journals contain admitted/spawn_intent/server_started only, without stop_requested/process_exit/terminal. The QA supervisor kills the live owned driver; the peer handle then signals. Fixture bytes remain unchanged.

Source: src/process_windows.rs:283–291 synchronous File::write_all/flush. src/protocol.rs:98 replies from receive on the same thread that checks cancellation/deadlines; rpc and interrupt also use this send. No independent deadline thread can terminate the job while that writer owns execution. Root-cause evidence combines this call path with the stalled peer stimulus and retained observations; no native Codex trial or production-duration stalled-write run is claimed.

Raw results: independent-attempts/IQ-02-deadline/result.json and independent-attempts/IQ-02-cancel/result.json. These are distinct declared stimuli, not retries. Binary hashes, exact args and fixture identities are in each result/request.

## IQ-06 — Bounded process ownership review

PASS within selected inspection/lifecycle scope: reviewed all of process_windows.rs and console/crash support. CreateJobObjectW uses null security attributes, job handle is not in inherited handle list; kill-on-last-handle-close enabled; PROC_THREAD_ATTRIBUTE_JOB_LIST and the three-pipe HANDLE_LIST installed before CreateProcessW; no breakaway flags; CREATE_NO_WINDOW. RAII drop and stop target the owned Job Object, not recovered PIDs. Inherited child pipe handles are dropped in the parent after creation. Independent held-handle stdin, Ctrl+C and killed-harness checks in IQ-03 passed; initially both handles were WAIT_TIMEOUT (258), finally both WAIT_OBJECT_0 (0).

This does not establish file/network isolation, native Codex sandbox compatibility, or arbitrary malicious-child escape resistance. Those claims were not tested. No additional test process is required for this static-plus-lifecycle case.

## Current execution accounting

01-tests and 04-coverage each executed all 46 functions: 20 mandatory, 26 supplemental, no ignored/failed/filtered required tests. Coverage 1311/1374=95.41484716157206%, all seven executable runtime files; lib.rs declares modules only. Six declared unit-level cases passed. Formatting and Clippy exited 0. IQ-01 six independent protocol/result subfixtures passed. IQ-03 three independent lifecycle subfixtures passed. IQ-04 compiled read-only repeat/pagination passed (11 events exactly once, no bytes changed, one turn total). IQ-05 sanitization remains pending.

No mock decorators or result-gaming confirmed. Fault-injection seams and the external deterministic peer are allowed by this contract and do not count as native Codex evidence. Existing tests do not cover the blocking-write input now used by IQ-02.
