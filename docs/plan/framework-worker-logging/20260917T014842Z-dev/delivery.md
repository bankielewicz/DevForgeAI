# Rust logging development delivery

Development status: COMPLETE for the selected fresh Rust probe logging candidate and Windows offline verification. The candidate is at C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging. It adds configuration-controlled off/minimal/verbose/debug logging, mandatory startup stream/exit evidence, bounded independent readers, closed classification, and inspection of logging artifacts. Source changes are reviewable in [candidate.patch](candidate.patch); every candidate file is bound in [candidate-manifest.json](candidate-manifest.json).

This modifies the DevForgeAI Rust worker probe. The root manual-console script continues to invoke the installed Codex executable directly. No installed Codex rebuild, operational configuration update, skill installation or native Codex launch occurred. The [candidate README](../../../../devforgeai/experiments/codex-worker-probe-logging/README.md) explains the schema-3 request/config selection and build command. Review schema remains 2; the new launch policy has SHA256 `c8ef7b6184e20fd55833c9b8f7cd17b6dc1f0af494ca367c857953680dab1b49`, so future native requests require refreshed bindings.

## Implemented behavior

The Rust logger writes diagnostics.jsonl with increasing detail by level. Off suppresses that file while mandatory journal evidence still records full read-byte SHA256/counts, EOF and overflow/read errors, pre-stop exit observation and post-stop code, dropped detail, and verified cleanup. Log content is typed: ordinary debug never stores arbitrary child text, config/environment values or protocol payloads. Unknown server method names now use closed journal labels.

Both reader handles are owned and joined. Separate bounded queues and independent aggregate accounting prevent an unread stderr queue or slow log write from blocking the pipe pumps. Byte/line limits remain enforced. A race found during regression testing—stderr overflow being reported as worker_exited when stdout closed—was repaired with a post-wait stream-error check. The observed config-field and MCP-transport startup errors have narrow closed classifier categories; unknown output remains unclassified. An exit observed before cleanup is not proof that the worker exited on its own or that Rust crashed.

## Executed verification

Windows x64, C:\Projects\DevForgeAI on the native Windows filesystem; PowerShell 7.6.6, Rust/Cargo 1.97.1, cargo-llvm-cov 0.8.4. Exact executables, command vectors, working directories, exit codes and raw streams are in tool-inspection.txt and attempts/*/receipt.json. All code commands ran against the actual Cargo manifest and lockfile using the offline cache.

| Check | Result | Evidence |
| --- | --- | --- |
| Required candidate cases | 152/152, 100%; 49 units + 103 integration/regression cases | full unfiltered --all-targets coverage campaign, attempt 23; test-analysis.json |
| Additional real Windows malformed UTF8 / final unterminated line | 1/1; exact hashes, both EOF, joined readers, exit 23 before/after cleanup, stopped tree | attempt 24; qa-harness literal-byte oracle |
| Overall selected required cases | 153/153, 100%; no unresolved failed, skipped, blocked or unexecuted required behavioral case | suite-summary.json |
| Executed first-party lines | 3858/4041 = 95.47141796585004%; PASS against the independent 95% floor | coverage.json and coverage-analysis.json |
| Formatting | PASS | attempt 25 |
| Clippy, all targets, warnings denied | PASS | attempt 22 |
| Final compiled binaries | PASS | attempt 26; binary-manifest.json |
| Preservation and required output paths | PASS: 58 original + 58 snapshot files and all selected inputs unchanged | preservation-readback.json |
| Branch coverage | NOT_RUN | Only stable toolchains installed; collector branch mode is unstable; tool-inspection.txt |
| Native Codex / independent product QA | NOT_RUN | Not included in this development verification |
| Framework acceptance | NOT_EVALUATED | No qualified Rust acceptance authority response was obtained |

The source denominator includes all 14 executable src files; lib.rs contains only module declarations and has zero executable lines. Test/fixture sources and dependencies are excluded, with no first-party executable exclusion. The additional external harness does not contribute to the coverage percentage. Each required case counts once; repetitions add no credit. The 120-second watchdog was executed, not skipped. The former query_failed gap now has runtime evidence from real QueryInformationJobObject access denial on a restricted duplicate of the same Job Object, plus null-count projection and mandatory evidence-write-failure precedence checks. It is not a serialization-only test or mocked API result.

All nine selected obligations in [traceability.md](traceability.md), including the output destination, have current supporting evidence. Early failing attempts are retained and explained there. Attempt 03 selected zero cases and earns no pass credit. Attempt 11 exposed an old fixture that needed the current mandatory summary/status; its original inspection assertions remain. Attempt 17 exposed the stream-error race; attempt 21 verified the repair including the full watchdog, followed by the complete final attempt 23. The old coverage target was retained; final coverage used its own disjoint target directory. No failed attempt was overwritten or promoted to a pass.

## Delivery boundaries and next step

Fresh candidate and evidence paths match the selected locations recorded before copying. The root console helper's SHA256 remains `f69da72fb44737127dcfde3607fb0e027e4afeb2463a78ac8f844bc3abfc58a0`; the frozen candidate and prior evidence remain in place. [Preservation readback](preservation-readback.json) and [input bindings](input-bindings.json) bind this observation.

Next: independent QA against this candidate manifest and [qa-handoff.md](qa-handoff.md), using a fresh QA-owned evidence directory. Only after independent QA passes is a separately authorized native diagnostic appropriate. These offline results do not establish the cause of a future startup failure or framework acceptance.
