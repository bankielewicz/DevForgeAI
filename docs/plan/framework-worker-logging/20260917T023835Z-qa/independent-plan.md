# Independent-case execution supplement

This fills the known preparation in plan.md without changing its166-case inventory or collection metrics. All QA-01..13 are READY. The unchanged candidate remains the path dependency. Supplemental developer test SUP-01 uses its original manifest and a new target; no results are reused.

Absolute harness: C:/Projects/DevForgeAI/docs/plan/framework-worker-logging/20260917T023835Z-qa/qa-harness/Cargo.toml.
Cargo command prefix for each case: C:/Users/bryan/.cargo/bin/cargo.exe test --offline --locked --manifest-path C:/Projects/DevForgeAI/docs/plan/framework-worker-logging/20260917T023835Z-qa/qa-harness/Cargo.toml --test independent -- NAME --exact --test-threads=1.
Replace NAME only with the exact mapped name below. run_command.py supplies the resolved vector, 180-second outer bound and distinct fixtures; child waits are <=4 seconds plus2-second teardown. Runs are sequential with result classification before the next case.

| ID | Exact name | Conjunctive expected behavior |
| --- | --- | --- |
| QA-01 | qa_01_config_denials_and_exact_boundary | Eight malformed/schema/oversize configurations plus digest, traversal and real Windows junction reject before spawn; exact4096 bytes accepted and copied unchanged. |
| QA-02 | qa_02_drift_and_legacy_composition | Change config after spawn_intent; no server_started, original copy preserved; legacy succeeds/off; unsupported version composition rejects. |
| QA-03 | qa_03_early_exit_classification | Four real early child exit29 cases (silent/known config/known transport/negative lookalike); exact hashes, both readers joined, pre/post29, correct closed category. |
| QA-04 | qa_04_raw_utf8_final_line_and_argv | Real byte-at-a-time invalid UTF8/final partial line; hashes/counts; Windows spaces/quote/trailing slash/Unicode argv round trip. |
| QA-05 | qa_05_delayed_consumer_and_budgets | 700001-byte stderr before receive, then exact/over1MiB stdout line,128-line queue and8MiB byte budget; exact independently expected stream bytes/hash and overflow/drain status. |
| QA-06 | qa_06_levels_and_capture_privacy | Each level preserves full mandatory capture and ordered exit; expected lifecycle/detail fields, fixed file behavior and absence of child/config-path canaries. |
| QA-07 | qa_07_sink_faults_caps_and_required_write_failure | Actual optional file-open denial, exact512/513 event cap status, mandatory journal failure remains code4 and stopped tree. Full byte-cap/read-only-write fault also remains required in package tests. |
| QA-08 | qa_08_untrusted_server_request_privacy | Independently authored server request contains unique method/id/path/token/prompt/account canaries; all levels deny with -32601, no arbitrary canary persisted/emitted, stopped held job. |
| QA-09 | qa_09_inspector_rejects_inconsistent_capture | Nine fresh successful runs plus accepted controls; missing capture/status/bad log and incomplete/contradictory capture or exit code must not remain completed. Retain all mutation results and fail once if any were accepted. Each isolated mutation is planned evidence, not a retry of an earlier outcome. |
| QA-10 | qa_10_legacy_and_interrupted_prefix | Explicit legacy input remains inspectable; current partial journal stays interrupted_unknown and unmodified. |
| QA-11 | qa_11_policy_and_native_schema | Exactly15 key quote corrections across116 positions; value bytes unchanged; schema3 inherits v2/native review denial without launch. |
| QA-12 | qa_12_independent_trace_and_oracle | Four real peer scenarios: success, unqualified policy, extra output key, nonzero worker exit; exact codes/reasons, single initialize/turn bound, fixed independent specification result. |
| QA-13 | qa_13_preservation_and_documentation | Recompute all candidate/original/snapshot/input hashes, schema-selection and native-boundary docs present. Full documentation/link review is manual and separately recorded. |

The unmodified candidate test peer source is also compiled as a qa-harness bin named protocol-peer. This satisfies the public admission rule requiring the test-built peer next to the running test executable; it does not alter candidate source or native admission. CARGO_MANIFEST_DIR in the path dependency remains the original selected candidate, so its workspace/source containment is not relocated. Custom qa-byte-peer runs only through public OwnedProcess/Session APIs. It cannot be admitted by a production peer request and supplies no native-qualification credit.

The Python expected-byte generator consumes literal fixture definitions, never product output; it freezes14 stream-oracle pairs. The Rust harness compares capture results to those fixed values. Input-binding hashes are computed separately using standard SHA256 for request admissibility, not as output expectations.

Pre-execution helper review: byte_peer.rs, independent.rs, generate_expected.py, Cargo.toml/lock and recorder changes read back. Attributes are only Rust #[test]; no macro decorators, hidden tests, swallowed assertions or fabricated process results. The held-job process API stops actual owned children before capture-result assertions. A custom peer is required to read/deny the exact unexpected server request. QA-09 accumulates all predeclared ordinary evidence-consistency mutations and asserts no accepted result at the end; this preserves all negative observations without waiving failure. Other issues are classified before further cases.

Helper inputs and built binaries are bound in qa-helper-manifest.json and independent-binary-manifest.json. No native Codex invocation, installation, production repair or operational changes are authorized or performed.

