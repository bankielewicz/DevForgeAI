# Protocol edge coverage remediation delivery

Status: **COMPLETE for this bounded development slice**. This is test implementation evidence for QA-F-COV-01, not full-candidate qualification and not independent QA closure.

## Delivered behavior checks

Added `tests/protocol_edges.rs` (SHA-256 `b5b0eb58b2d04b0c553d4b200fcf2353213bb8c6cd44fb01024b44778323bce0`) and the distinct compiled child `tests/support/protocol_edges_peer.rs` (SHA-256 `2cdd924668cd7d841942ccd76a694c5fc85afa4f7b9b194b6adc1ff0252506fd`). Root registered that child as `protocol-edges-peer` in the shared `Cargo.toml`; root owns the shared manifest and integrated candidate.

The tests exercise the real `Session::preflight`, Windows owned process, stdin/stdout/stderr pipes and durable journal. Expected results come from DFF-WORKER-FEAS-01 section 5 and DFF-WORKER-PREFLIGHT-01 Required pre-thread protocol:

- PE-01 command/file approval request: exact cancel response, `approval_required`, no work.
- PE-02 unsupported server request: exact `-32601` response, `unsupported_request`, no work.
- PE-03 malformed server-request ID: `protocol_error`, no response/grant, no work.
- PE-04 stderr: exact diagnostic byte total observed in one or more omitted-content chunks, hashes retained, private bytes absent from product evidence.
- PE-05 101 feature entries: `protocol_error`.
- PE-06 repeated feature cursor: `profile_unqualified`.
- PE-07 rate-limit RPC error: successful preflight with exactly one typed `rate_limits:not_measured`, private error text absent.
- PE-08 negative reported percentage: successful preflight with exactly one typed `rate_limits:not_measured`.
- PE-09 ten nonfinal feature pages: `profile_unqualified`.

Every case verifies that no `thread/start` or `turn/start` was sent. Required traces and journals use failing reads rather than defaults, the first trace message must be `initialize`, the fixture task/selector are read back unchanged, and all nine final fixtures retain input, trace, journal and task files.

No functional product defect was reproduced. `src/protocol.rs` stayed byte-identical at SHA-256 `51a75924b10ae57ec208161d5fcb68732a9e371b8bbbfcdd49eacf187594889d`; no production logic, original test, requirement or threshold was changed.

## Results

Focused required cases: **9/9 passed (100%)**, represented by four nonduplicative Rust test functions. Final receipt: `08-focused-integrity-green/receipt.json` SHA-256 `1909ab78c9e5b030a5167464386a086d53f74bdb365016d21bba3c2efd763e04`; raw stdout reports 4 passed, 0 failed, 0 ignored.

Focused Clippy: **PASS**, exact command `cargo clippy --locked --offline --test protocol_edges --bin protocol-edges-peer -- -D warnings`. Final receipt: `09-focused-clippy-final/receipt.json` SHA-256 `10ec45bb4c4ab872e0a96955f81b8400b4cc4d3f16969a30bae4f2a0b9737687`.

Owned-file rustfmt check: **PASS** for the two new Rust files. Final receipt: `10-owned-format-final/receipt.json` SHA-256 `cdb93c6274e32a79d6696960dc80426e1e93bf1c1aed4b0d887d22b17b32a345`.

The retained initial `cargo fmt --all -- --check` attempt (`02-format-check`) exited 1 before formatting: it reported the two new owned files plus a concurrently owned `tests/runtime_edges.rs`. This slice formatted only its owned files and did not rewrite the other actor's file. Root still owns the coherent full-package formatting check.

## Boundaries and handoff

This slice deliberately did not collect coverage, run the full suite, freeze the candidate, run Codex/native trials, or issue QA/framework acceptance. Root must integrate all disjoint test slices, run one complete locked/offline regression, all-target formatting/Clippy and full first-party line coverage, then freeze the returned candidate. Fresh independent QA alone may mark QA-F-COV-01 `VERIFIED_FIXED`.

Native WN-01/WN-02 remain outside this slice and consume zero attempts. Framework acceptance is **NOT_EVALUATED**.

