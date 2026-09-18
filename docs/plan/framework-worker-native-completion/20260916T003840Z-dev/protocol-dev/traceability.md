# Protocol edge requirement traceability

| Source-qualified ID | Statement locator and requirement | Dependencies/shared-contract owner | Implementation paths | Verification and evidence | State |
| --- | --- | --- | --- | --- | --- |
| FEAS-5-REQUEST / PE-01 | DFF-WORKER-FEAS-01 section 5: command/file approval requests receive `decision:cancel` and stop without a grant | `Session::receive`; root owns production | `tests/protocol_edges.rs`, `tests/support/protocol_edges_peer.rs` | `08-focused-integrity-green`, exact outbound response and no-work trace | VERIFIED |
| FEAS-5-REQUEST / PE-02 | DFF-WORKER-FEAS-01 section 5: unknown request receives method-not-supported `-32601` and stops | same | same | `08-focused-integrity-green`, exact response and sanitized evidence | VERIFIED |
| FEAS-5-CORRELATION / PE-03 | DFF-WORKER-FEAS-01 section 5: invalid server-request ID is a protocol error | same | same | `08-focused-integrity-green`, malformed object ID, no response/grant | VERIFIED |
| FEAS-4-STREAM / PE-04 | DFF-WORKER-FEAS-01 sections 4 and 7: bounded stderr is drained and retained only as omitted content with size/digest | process reader and journal remain production-owned | same | `08-focused-integrity-green`, exact total bytes across any chunk count; private sentinel absent from product evidence | VERIFIED |
| PREFLIGHT-3 / PE-05 | DFF-WORKER-PREFLIGHT-01 item 3: maximum 100 entries per feature page | `Session::profile_pages`; root owns production | same | `08-focused-integrity-green`, 101-entry page -> `protocol_error` | VERIFIED |
| PREFLIGHT-3 / PE-06 | DFF-WORKER-PREFLIGHT-01 item 3: repeated cursor rejects | same | same | `08-focused-integrity-green`, repeated cursor -> `profile_unqualified` | VERIFIED |
| FEAS-5-RATE / PE-07 | DFF-WORKER-FEAS-01 section 5 and PREFLIGHT item 8: unavailable rate limit is explicit and no number is invented | `Session::check_account`; root owns production | same | `08-focused-integrity-green`, RPC error -> one `not_measured`, message absent | VERIFIED |
| FEAS-5-RATE / PE-08 | Same requirement: invalid negative percentage is not treated as available quota | same | same | `08-focused-integrity-green`, negative value -> one `not_measured` | VERIFIED |
| PREFLIGHT-3 / PE-09 | DFF-WORKER-PREFLIGHT-01 item 3: maximum ten pages; incomplete pagination rejects | `Session::profile_pages`; root owns production | same | `08-focused-integrity-green`, ten nonfinal pages -> `profile_unqualified` | VERIFIED |
| OUTPUT-PROTOCOL-DEV | Root assignment: evidence under exact `...\20260916T003840Z-dev\protocol-dev` | root selected destination; this slice owns records | this directory | `readback.md` | VERIFIED |

Selected behavioral count: 9; verified 9; pending 0; blocked 0. The output-location obligation is tracked separately and does not inflate the behavioral denominator.

Selected exclusions/deferred capabilities: full-candidate regression/coverage/freeze and independent QA are root/QA responsibilities; native WN-01/WN-02 and protected framework acceptance are outside this slice. The synthetic peer does not qualify native behavior.

