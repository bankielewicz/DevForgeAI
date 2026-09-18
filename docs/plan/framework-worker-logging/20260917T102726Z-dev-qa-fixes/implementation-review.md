# Scoped implementation and integrity review

QA findings remain OPEN; this development run can report fixes, not close them. The production delta is confined to journal.rs. It changes the prior boolean exit marker to an Option containing typed Capture and nullable u32 post-stop exit. Deserialization uses get/ok_or so missing is distinct from explicit null. Capture::validate still validates each current summary. A shared check for completed/preflight_checked requires a retained exit summary, drain_complete, no stdout/stderr byte overflow, and matching successful zero codes. Existing EOF/reader-error checks are enforced by validate when drain_complete is true. Existing historical success conditions and diagnostic status/file verification remain in place.

No functional refactor beyond the shared success check was needed: both success outcomes use one guard and historical schema selection already has one owner. Attempt03 applied rustfmt; attempt04 reran identical focused assertions on formatted bytes. The additional README paragraph identifies the corrected sibling and separate independent retest, and its build command points at that sibling.

## Executed TDD observations

- 01-red: production files matched the failed candidate. All ten new tests compiled and executed. Six failed on actual accepted invalid evidence; four compatibility tests passed. Cargo exit101 was behavioral red, not a setup failure. Every mutation/control observation and CLI stream is retained beneath the attempt fixtures.
- 02-green: the same ten tests and assertions passed after the bounded journal repair, exit0.
- 04-refactor: ten tests passed after rustfmt and documentation update, exit0. No weakened assertion, reduced variant set, ignore marker or fabricated result was introduced.

## Oracle and boundary review

The new completed-run tests start the actual deterministic Rust peer through the unchanged runner, verify the successful control, change one planned evidence condition, then require the library and compiled public CLI to report evidence_corrupt/exit4. Expected error/state values are literal contract outcomes, not computed with production validation. Bad type/range and terminal nonzero variants are negative controls already rejected before this repair. Both streams and every logging level are covered.

Preflight fixtures are explicitly synthetic historical journal records, written with the existing Journal API. They exercise both schema2 and schema3 preflight_checked inspection branches, not native admission or native startup. They never launch Codex. Their original controls require inspect success before mutations.

Failure compatibility starts real peers for blocked, failed, cancelled, timed_out and cleanup_uncertain outcomes, verifies original inspection, then supplies truthful incomplete-capture/explicit-null observation shapes. The failed early-exit control checks actual child exit1. Historical schema1/2 fixtures remove only newer capture/status data; current schema1/2 records still require capture checks. Interrupted prefixes stay interrupted_unknown. Dropped detail and pre-stop null are not misclassified as failed capture.

Every inspection snapshots the complete fresh test root's file membership and raw bytes before and after both library/CLI reads. This includes journal, bound inputs, task fixture and peer trace; unchanged trace and unchanged bytes provide no-replay evidence. CLI outputs and observed expectation results are written by the test only after the readback comparison. Test fixtures and all test-created expected/actual evidence are retained via WF_TEST_EVIDENCE. The 10 top-level tests are conjunctive and count once each.

Marker search across all candidate src/tests found no mock, ignored test or coverage exclusion markers (integrity-search.json). Manual review concentrated on the changed source, all new assertions/helpers, existing Capture::validate, process capture/runner terminal production, inherited recovery/logging tests and the supplemental Windows byte oracle. This is a scoped test-integrity review, not an exhaustive repository security review. Existing external peer dependencies and private fault seams remain unchanged. No first-party executable source is excluded from line measurement.

The inherited supplemental harness is copied to supplemental-harness with cases.rs, peer.rs, expected.json and Cargo.lock byte-identical; only its Cargo.toml dependency path points to the corrected sibling. Its exact literal malformed-byte SHA256 oracle is retained. No independent QA skill or QA campaign is invoked by reusing this developer regression.
