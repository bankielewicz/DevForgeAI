# Declared protocol edge cases

Declared before test execution. These cases exercise compiled `Session::preflight` against a distinct compiled Rust child over owned JSONL pipes. The peer validates outbound parameters independently and no case sends `thread/start` or `turn/start`.

| ID | Requirement and independent expected result |
| --- | --- |
| PE-01 | DFF-WORKER-FEAS-01 section 5 and preflight section Required pre-thread protocol: a command/file approval server request receives `decision:cancel`, records only bounded typed metadata, and stops with `approval_required`. |
| PE-02 | DFF-WORKER-FEAS-01 section 5: an unsupported server request receives JSON-RPC error `-32601` and stops with `unsupported_request`. |
| PE-03 | DFF-WORKER-FEAS-01 section 5: a server request whose ID is neither string nor unsigned integer stops with `protocol_error` and receives no grant. |
| PE-04 | DFF-WORKER-FEAS-01 section 4: stderr drains concurrently into a content-omitted size/digest observation while an otherwise valid preflight succeeds; secret bytes do not enter retained evidence. |
| PE-05 | DFF-WORKER-PREFLIGHT-01 item 3: a feature page with 101 entries exceeds the page limit and stops with `protocol_error`. |
| PE-06 | DFF-WORKER-PREFLIGHT-01 item 3: a repeated nonempty feature cursor stops with `profile_unqualified` and pagination does not advance to work. |
| PE-07 | DFF-WORKER-FEAS-01 section 5 and preflight section item 8: a JSON-RPC error from rate-limit observation does not invent a numeric limit; preflight succeeds with exactly one `rate_limits:not_measured` observation. |
| PE-08 | DFF-WORKER-FEAS-01 section 5 and preflight item 8: a negative reported rate-limit percentage is invalid measurement, not available credit; preflight succeeds with exactly one `rate_limits:not_measured` observation. |
| PE-09 | DFF-WORKER-PREFLIGHT-01 item 3: ten nonfinal feature pages exhaust the selected bound and stop with `profile_unqualified`. |

Denominator for this focused slice: nine required cases, grouped into four Rust test functions to keep shared setup explicit without inflating pass rate. Each case counts once from its labeled scenario assertion. Full package required-case and executed-line denominators are owned by root development and fresh independent QA; this slice does not collect or claim coverage.
