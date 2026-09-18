# F-01/F-02 remediation delivered for independent retest

**Development status: PARTIAL.** Both repairs are implemented and focused/full developer regressions pass. The unchanged copied QA helper retains one failed deadline assertion: expected exit 4, actual exit 6 (`timed_out/deadline`). Independent QA must assess that expectation and both findings. No finding is self-closed and no all-checks QA PASS is issued.

## Corrected candidate

- Project: C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe, native Windows build 26200 x64, C: NTFS, PowerShell 7.6.6, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4 / LLVM 22.1.6. No Git metadata. Exact host and tool observations are in host.json and the version receipt directories.
- [Candidate manifest](candidate-manifest.json): 32 files, SHA-256 `3f65ade36cf8186fe711da73f1a2794a17d7fb51e02bf66261e9bba0ce158e39`. Exact current bytes retained in candidate-snapshot/.
- [Changed files](changed-files.json): src/process_windows.rs, src/protocol.rs, tests/support/peer.rs; new tests/remediation.rs. Cargo manifest/lockfile, original test files and frozen fixtures/oracle remain unchanged.
- [Build identities](build-identities.json): normal main executable SHA-256 `48eb7f41d05e6e810d47f7c369c88a47038aa993cfc59a2aca730228a898995a`; instrumented main `9f3acc6da8fcc678cdf867e50d0bdf2f741866797084c9385fdbffa10f18048d`; copied-fixture driver `9352d84ec1df4b627ea48753d7e753dbc80446c12b64b4c953e43d0de5eff56f`. Full paths and all 54 executable identities are in that manifest.

## Per-defect results

### F-01: writes no longer block deadline/control handling

The process writer owns stdin on a separate thread with one outstanding message. The control thread polls completion, cancellation and the current deadline. An interrupted write stays marked as uncertain; another message is not queued behind it. RPC timing starts before its send, and interrupt send/wait use one shared grace budget. Job teardown unblocks the pipe, and stopped verification includes writer completion.

Unchanged Red fixtures hung for three seconds in both variants and required supervisor containment. Green on the original fixture: deadline returns exit 6 in 0.797 seconds; cancellation returns exit 5 in 0.531 seconds. Both have stopped held peer handles and unchanged fixtures without external termination. New tests additionally verify descendant handles, invalid control while writing, ordinary RPC-shaped full-pipe writes, pending-write interruption and an interrupt that itself blocks on a full pipe. See [traceability](traceability.md), [review](ownership-review.md), and both roots' independent-attempts/IQ-02-*.

**Preserved mismatch:** the copied helper's deadline expected_exit is 4. Its raw pass=false remains untouched. Spec §4 defines exit 6 for a reached deadline; the report/fix packet permits a bounded timeout. The new behavioral regression explicitly requires exit 6/deadline and stopped processes. This is submitted for independent review, not used to overwrite the old oracle or close F-01.

### F-02: retain only approved typed error fields

CodexErrorInfo now validates the captured category variants and reconstructs their approved fields before append/emit. Unknown outer categories and malformed values fail with protocol_error; nested extension data is omitted. Legitimate categories and numeric/null/absent HTTP details are retained. Related RPC error_code retention now requires an integer and never copies an arbitrary JSON payload. Free-form message/details are omitted.

Unchanged Red fixture copied its synthetic marker to stdout and journal. Green original IQ-05 exits 4/protocol_error with no marker in stdout/stderr/journal and a stopped peer. Nineteen additional CLI subfixtures check unknown/nested fields, malformed category/code types, range errors, valid numeric category details, and approved category retention. No real credentials or live profile were accessed.

## Verification

`G` below is ../20260915T1834258428322Z-green. Exact argv/cwd/tool hashes/times/exits and streams are retained in each receipt directory and execution-records.jsonl.

| Check | Result | Evidence |
| --- | --- | --- |
| Focused remediation | 4/4 PASS | G/04-focused; earlier 3-test Green in G/02-focused |
| Normal all-target suite | 20/20 mandatory + 26/26 original supplemental + 4/4 remediation PASS; 141.922 seconds | G/01-tests |
| Instrumented all-target suite | Same 50/50 PASS; 147.969 seconds | G/04-coverage |
| Declared original unit cases | 6/6 PASS in each full run | test-inventory.json, metrics.json |
| Original 26-group scope, unchanged copied IQ assertions | 25/26 = 96.15384615384616%; one FAIL retained | metrics.json, copied-iq-results.json |
| Executed-line coverage | 1420/1487 = 95.49428379287156%, PASS | G/coverage.json; 147 raw/merged profile identities retained |
| Formatting | PASS | G/02-format |
| Clippy all-targets, -D warnings | PASS | G/03-clippy |
| Branch coverage | NOT_RUN; installed stable help labels collection unstable | Original environment coverage-help receipt |
| Native Codex WN-01/WN-02 | NOT_RUN; 0/2 demonstrated native passes | Unselected and prohibited in this task |
| Framework acceptance | NOT_EVALUATED | No protected authority decision |

Coverage denominator includes every executable src line: journal 216/220, main 80/86, oracle 7/7, process_windows 287/300, protocol 467/485, request 250/263, runner 113/126. lib.rs contains declarations only. Tests/support/fixtures and third-party/generated dependencies are excluded; no runtime exclusions. The two numeric floors pass independently, but a failed required assertion is not waived by those floors. Added tests do not inflate the historical 26-group denominator. Test runs on separate revisions are not combined as extra cases.

## Evidence custody, limits and delivery

Original handoff hash matched the supplied value; all original 31 candidate files matched before edits. Final readback verifies original bound evidence, all 335 contract/schema entries, index manifest/lock and selected operational boundaries. No old source was restored or old evidence overwritten. Green fixture helpers retain the original bytes. The copied driver was built before the final test-only addition; its production source/prerequisite hashes match the final candidate, and its build receipt retains that earlier full manifest.

One early focused build failed on a test closure lifetime and is retained as ERROR. An explicit closure argument type fixed it. This was not counted as behavioral Red. The first formatting receipt retains its pre-format manifest digest, but that intermediate draft manifest file was overwritten before archive preservation was added; original Red/input evidence and final candidate identity are intact. Subsequent intermediate manifests are archived. No unresolved timing flakiness was observed in the executed cases.

Original selected evidence destination and sibling Green mapping are in context.md, derived from the fix packet's fresh-sibling requirement. Required final outputs are candidate-manifest.json, candidate-snapshot/, changed-files.json, build-identities.json, raw-profile-identities.json, metrics.json, traceability.md, execution-records.jsonl, this report and handoff.md under the exact -dev root; raw Green receipts/profiles are under the exact -green sibling. delivery-manifest.json binds expected/actual paths and bytes; output-readback.json records literal-path verification. No active owned test job remains; held process handles signalled in lifecycle checks. Evidence and fixtures remain retained.

Next action: separately select [independent retest](handoff.md). F-01/F-02 remain OPEN. No native trial, launcher/profile amendment, installation, deployment, index repair or operational-skill update occurred.
