# Index service platform status

Updated 2026-09-14. **WSL has been tested. Standalone Linux has not been tested.** WSL results must not be presented as standalone Linux qualification.

| Target | Actual evidence | Qualification |
| --- | --- | --- |
| Windows 11 x64 | Attempt 085: 38/38 automated cases passed, including native IPC/process tests, native tray smoke, and the prepared WSL bridge fixture. Rust 1.97.1. | PARTIAL; line coverage 2744/3442 = 79.72109238814643%, below mandatory 95%. |
| Ubuntu 24.04.5 x64 under WSL2 | Attempt 086: 36/36 automated cases passed, including Unix sockets, process lifecycle, source-link exclusion and storage readers. Rust 1.98.1. | PARTIAL; line coverage 2071/2786 = 74.33596554199569%, below mandatory 95%. |
| Standalone Ubuntu 24.04 x64 | NOT_RUN; no standalone host was used. | NOT_RUN. Explicitly required by the current specification. |
| Standalone Ubuntu 26.04.1 LTS x64 | Proposed by the user for the manual campaign; no results received yet. | NOT_RUN. Results will be labeled as 26.04.1 compatibility evidence; they do not prove the specified 24.04 target. |

Raw reports: [Windows](windows-coverage-004.json), [WSL](wsl-coverage-002.json), [execution receipts](executions.jsonl). Both coverage commands returned exit 1 because coverage was below 95%; the contained tests passed. Branch instrumentation was not enabled: branch coverage is NOT_RUN, not 0% measured coverage. The declared denominator is all first-party executable files under `devforgeai/src` compiled for that platform; tests, examples, fixtures and third-party/generated code are excluded. Windows GUI source is included on Windows.

The automated counts cover the implemented test suite (including one setup smoke test). They are not the denominator for all specified acceptance scenarios. Unperformed crash-boundary, cross-account, watcher-overflow, mixed-environment visual, installed-stopped WSL, startup/systemd and other checks remain unperformed; a suite pass cannot waive them. No full development completion or protected framework acceptance is claimed.

The [offline HTML playbook](../../index-service-validation-playbook.html) records all 19 scenarios, exact OS release, commands/actions, expected and observed results, exits, artifact references, failed attempts and coverage counts. The user requested this manual handoff. Send its exported JSON and the referenced raw evidence for independent evaluation. Export alone does not include the referenced files.

## Retained Windows benchmark

Attempt 069 completed three release repetitions with seed 20260913, 10,000 files / 104,857,600 bytes, balanced Rust/Python/JS/TS/text and a 100-file edit batch. All repetitions reported 10,000 text and 8,000 structural files, complete fixture coverage, and unchanged generations during the one-second idle observations.

| Repetition | Cold ms | Warm ms | 100-file edit ms | Concurrent status p95 microseconds |
| --- | ---: | ---: | ---: | ---: |
| 1 | 40189 | 28361 | 28909 | 7542 |
| 2 | 46287 | 29290 | 30286 | 8004 |
| 3 | 46171 | 28353 | 31058 | 8532 |

Hardware: AMD Ryzen 9 9900X, 12 cores / 24 logical processors, 100298813440 bytes RAM. Whole benchmark process: 318164 ms wall time, 196687.5 ms CPU time, 27148288 bytes peak working set. CPU/RAM samples are external native observations in [benchmark-resources-003.json](benchmark-resources-003.json); the Rust example's `NOT_MEASURED` field refers to its own lack of resource collection. Phase results are in [benchmark-003.stdout.jsonl](benchmark-003.stdout.jsonl), progress in [benchmark-003.stderr.txt](benchmark-003.stderr.txt), and fixture hashes in [benchmark-fixture-manifest-003.json](benchmark-fixture-manifest-003.json).

Limitations: four concurrent management-status readers, not the unselected companion code-query workload; short idle generation observations do not measure sustained idle CPU. Linux/WSL benchmark runs are NOT_RUN. The executable was built in attempt 067; the later root-recovery fix was not part of this benchmark. Attempt 049 timed out; attempt 057 completed but failed to retain phase stdout; both are preserved. These are baseline measurements, not a production performance promise or complete DS-A18 qualification.

## HTML verification

Attempt 076 verifies JavaScript syntax, 19 unique scenarios, exact release capture, empty coverage handling, subthreshold arithmetic, retained attempts, platform separation, command newlines and evidence-only export through a Node unit harness. A missing coverage value initially became numeric zero; attempt 075 retained that failure and 076 verifies the correction.

Browser security policy blocked opening the local HTML URL. No browser workaround was attempted. Rendered visual and live browser import/download checks are NOT_RUN. Terminal/static artifact checks remain separate from native browser verification.

## Formal QA handoff and test integrity

Formal QA is PENDING. QA must independently verify specification conformance, executed-line coverage >=95%, and the required unit-test pass rate >=95% per platform. Any mock decorator or test that games results is a QA failure. Reject vacuous assertions, fabricated outputs, weakened expectations, skipped required cases counted as passes, unjustified coverage exclusions and duplicate retry counts. Failed QA returns this candidate for remediation; the current coverage already fails both measured platforms.

The focused test-integrity review found a setup-only assertion in devforgeai/tests/harness.rs (size_of::<u32>() == 4). It supplies no product evidence and receives no required-case credit. Raw runner totals of 38 Windows / 36 WSL include it; removing that setup count leaves 37 / 35 executed non-setup cases, not a complete required-case denominator. The absent-distribution WSL probe does not establish installed-stopped behavior. No mock decorator was found in the scoped Rust source/tests/examples scan. This scan is not a completed anti-gaming audit. The HTML Node checker uses minimal DOM/storage substitutes and supplies only helper logic evidence, never native browser or product qualification.
