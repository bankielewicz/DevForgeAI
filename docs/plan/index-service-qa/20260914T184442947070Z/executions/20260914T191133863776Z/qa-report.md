# Independent product QA report

## Verdict and scope

**FAIL.** Two independent Windows status-rendering tests fail against mandatory DS-025, and measured Windows/standalone Ubuntu executed-line coverage is below95%. Failure takes precedence over the remaining incomplete checks.

Run 20260914T191133863776Z, mode execute. User explicitly selected the saved plan and current candidate, authorized isolated builds/tests/coverage/native Windows UI and SSH Ubuntu, and left unavailable WSL and startup/systemd changes as gaps. The campaign completed the executed checks below; it did not complete every acceptance subcase.

Project: C:\Projects\DevForgeAI, native Windows11 x64. Supplied SSH host: me@192.168.245.128, Ubuntu26.04.1 LTS x64, original checkout /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai. Source-equivalent isolated copies were used for builds and12 independent Rust tests; no product source or developer-test repair occurred.

- Selected plan: C:\Projects\DevForgeAI\docs\plan\index-service-qa\20260914T184442947070Z\test-plan.md; SHA256432649b12605ee0cfb043870854b0ad29e21970f9f5c1daebaa0fd4e2bd1d378.
- Selected specification: C:\Projects\DevForgeAI\docs\plan\devforgeai-index-service-mvp-spec.md; SHA25652d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4.
- Candidate: [source-manifest.json](source-manifest.json), SHA25643b63b5a9496b9d5374996d274cf5b852e2301ba23a87490717c786f71790343;48 original application files. [Runtime artifacts](runtime-artifacts.json) and Ubuntu completion bind fresh native binaries; current original source and both test copies match the original48 files.
- Exact execution/output binding: [binding.json](binding.json). Current evidence root: C:/Projects/DevForgeAI/docs/plan/index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z. Report/fix byte bindings live in final [handoff-manifest.json](handoff-manifest.json), entries qa-report.md and qa-fix.md.
- Inputs/rules: [inputs.json](inputs.json), current AGENTS.md and QA skill. The differing remote spec was not substituted; selected local spec bytes were supplied as remote QA context. Query extension, authority-service implementation and installation remain unselected.
- Prior developer reports were context only. No prior product result was reused.

## Confirmed findings

| ID | Requirement | Evidence and impact | Owner/state |
| --- | --- | --- | --- |
| QA-D01 | DS-025: management window includes current generation and last reconciliation | qa_u06_tray_displays_current_generation and qa_u07_tray_displays_last_reconciliation fail on both compiled hosts. Windows native screenshot confirms fields absent. Users cannot see the required indexed-generation/reconciliation provenance. | dev / OPEN |
| QA-D02 | Section1.4/AGENTS.md: first-party executed-line coverage >=95% per platform | Windows2626/3442 (76.29285299244624%); Ubuntu2075/2786 (74.47954055994256%). Missing executed lines816 and711 respectively; source denominator retained. | dev / OPEN |

QA-D01 is a Windows product UI defect; Linux execution of its shared formatter independently reproduces the same library behavior and does not imply a Linux tray requirement. The declared18 unit cases include these shared formatter tests. Their16/18 pass result is also below95%, traced to QA-D01 rather than counted as an unrelated repair defect.

## Executed checks and metrics

| Platform | Check | Result | Evidence |
| --- | --- | --- | --- |
| Windows11 x64 | Locked offline release build | PASS | attempts/build/receipt.json |
| Ubuntu26.04.1 x64 | Locked offline release build | PASS | ubuntu/attempts/build/receipt.json |
| Windows | Formatting; Clippy all targets with -D warnings | PASS | attempts/fmt; attempts/clippy-002 |
| Ubuntu | Formatting; Clippy all targets with -D warnings | PASS | ubuntu/attempts/fmt; ubuntu/attempts/clippy |
| Windows | Fresh Cargo test executions, including native tray |46 passed,2 failed,2 ignored | attempts/coverage-002/stdout.txt |
| Ubuntu | Fresh Cargo test executions |46 passed,2 failed | ubuntu/attempts/coverage-002/stdout.txt |
| Both tested platforms, separately | Independent native CLI cases N01..N09 |9/9 PASS each | native-acceptance/results.json and ubuntu/native-acceptance/results.json |
| Windows | Executed-line coverage |2626/3442 =76.29285299244624%, FAIL | coverage.json |
| Ubuntu | Executed-line coverage |2075/2786 =74.47954055994256%, FAIL | ubuntu/coverage.json |
| Each tested platform | Declared component-unit cases |16/18 =88.88888888888889%, FAIL for declared suite | executed-test-inventory.json; metrics.json |
| WSL2 Ubuntu24.04 | Tests/coverage |NOT_RUN, no ratio | QA-G01 |
| Full three-platform scope | Overall required coverage/unit/suite rate |INCOMPLETE; no valid full-scope ratio | WSL and inventory/subcase gaps |
| Both tested platforms | Branch coverage |NOT_RUN | no supported branch collector selected |

[Metrics](metrics.json) contain integer counts and per-file line reports; [test inventory](executed-test-inventory.json) separates provenance/category/platform. Product line denominator is all compiled first-party Rust src lines including binaries/native adapters; Windows tray_windows.rs is included on Windows. Tests/examples/fixtures and third-party/generated dependencies are excluded from product line coverage, not from integrity review. Windows14 executable files and Linux13 appear in raw coverage; src/lib.rs has no executable lines. No first-party behavior is excluded to improve coverage.

Raw totals include two setup tests per platform (Rust type-size smoke and benchmark-fixture generator); neither receives product-unit or acceptance credit. Excluding setup, known Cargo product-case counts are44/48 Windows (2 failures,2 WSL ignored) and44/46 Ubuntu (2 failures). Nine independent native cases per tested platform are separate acceptance counts; benchmarks, setup and GUI are not mixed into unit rates. The complete requirement-derived unit inventory remains unproven;18 is the declared executed suite, not proof no units are missing. Retried harness setup/static analysis attempts do not inflate test cases or erase failures.

Compatible observed two-host line subtotal is4701/6228 (about75.48%), not a full required-platform overall metric. No platform's result qualifies WSL. Neither numeric floors nor this subtotal can waive QA-D01.

Tooling: Windows cargo/rustc1.97.1, cargo-llvm-cov0.8.4, PowerShell7.6.6; Ubuntu cargo/rustc1.93.1, cargo-llvm-cov0.9.1, LLVM21.1.8 binaries. Python3.10 Windows orchestration and Ubuntu Python produce evidence only; no runtime Python dependency added to the Rust application.

Collector continuity used --ignore-run-fail so raw reports survive the two test failures. This option cannot grant a pass: Windows underlying cargo test exited101, collector exited1; Ubuntu collector exited101 with raw coverage produced. Receipts retain these statuses even where the evidence recorder itself exited0.54 Windows and53 Linux profraw artifacts were observed, including process/native-code execution; raw output and native module coverage are retained.

## Native and independent observations

Windows [native tray capture](attempts/coverage-002/gui/tray-paused.bmp) was visually inspected. The window shows environment/project, paused state, coverage/freshness and counters; it does not show required generation or reconciliation time. Native GUI test actions successfully started the owned daemon, registered a synthetic project, paused it, hid/reopened/exited the window and confirmed the daemon remained running. Its cleanup then stopped the daemon. This smoke test does not qualify every menu/dialog/control state or mixed-environment UI.

N01..N09 independently exercised stopped/idempotent starts; paused registration and queued scan; exact five-file exclusion/UTF16/binary counters; captured source/hash and absence of excluded secret bytes; same-mtime edits reconciled; a real read transaction held its generation over two daemon reindexes; rename/delete convergence; --yes enforcement/cache-only removal with unchanged source manifest; protocol version rejection; and final idempotent shutdown. Commands, input payloads, timestamps, exit codes/stdout/stderr and results are retained beneath both native-acceptance directories.

Independent Rust tests cover all11 structural extension aliases, exact BOM coordinates and Python method/docstring ranges, full1MiB/8MiB frame boundaries, request budget edges, mandatory exclusions despite configurable default overrides, Git/nested negation, exact size/hash answer, invalid snapshot rejection, replay expiry/conflict and the two failed UI assertions. Fixtures and expected results come from the contract/literal golden bytes, not copied from product output. The invalid snapshot is a negative control; known SHA256 abc and altered bytes distinguish a valid from an invalid snapshot.

## Benchmark observations

Three release repetitions per tested platform used seed20260913,10,000 UTF8 files totaling104857600 bytes, balanced across Rust/Python/JavaScript/TypeScript/text, with a100-file edit batch. Both fixture manifests bind the workload. Each repetition reported10,000 text/8,000 structural files and complete fixture indexing.

| Host | Repetition | Cold ms | Warm ms |100-file edit ms |
| --- | --- | --- | --- | --- |
| Windows |1|46226|30064|29870|
| Windows |2|42879|27860|27724|
| Windows |3|44351|28464|28939|
| Ubuntu VM |1|12146|2810|3880|
| Ubuntu VM |2|12118|2794|3274|
| Ubuntu VM |3|11852|2813|3158|

These are baseline observations, not a speed comparison or production SLO. Raw JSONL is in each attempts/benchmark/stdout.txt and exact command/elapsed/exit in receipts. CPU/RAM and sustained idle activity were not collected; concurrent benchmark readers call daemon.status, not indexed content queries. N05 separately proves real content-reader transaction isolation. DS-A18 full qualification remains incomplete; no benchmark PASS is inferred from partial performance evidence.

## Acceptance traceability

Full selected passages and scenario definitions remain in the saved plan's criteria.json. Every selected requirement is accounted for below; “remaining” is unperformed work, not an implied pass.

| Criterion | Actual evidence | Cases | Remaining qualification |
| --- | --- | --- | --- |
| DS-001 | Builds and packaged Rust/query/license/lock checks passed | Q-01,Q-DEL | Full packaged runtime audit not complete |
| DS-002 | N03 snapshot bytes and hashes; N05 generation reader passed | Q-02,N03,N05 | Capture/publication interruption boundaries not exhaustively scheduled |
| DS-003 | Windows11 and standalone Ubuntu26.04.1 native build/tests executed | Q-03 | Ubuntu24.04 WSL2 NOT_RUN |
| DS-004 | Native same-user IPC and simultaneous-start/lock regressions passed | Q-04 | Alternate-principal/remote pipe denial not exercised |
| DS-005 | WSL test functions left ignored by selected execution scope | Q-05 | WSL bridge native target unavailable for this run |
| DS-006 | No WSL executable launched | Q-06 | Installed-stopped polling/lifetime scenario NOT_RUN |
| DS-007 | Root/overlap and Unix links tested by existing suite | Q-07 | Windows junction replacement and full native case matrix incomplete |
| DS-008 | N02 distinguishes paused/queued/partial counts; status regressions passed | Q-08,N02 | All state/race combinations not covered |
| DS-009 | Existing simultaneous starts and N01 idempotent start passed | Q-09,N01 | Foreground signals/default deadline boundary incomplete |
| DS-010 | Pause persistence/resume and same-mtime edit reconciliation passed | Q-10,N02,N04 | During-file quiescence/race and overflow stress remain |
| DS-011 | N09 stop/idempotence and native tray exit preservation passed | Q-11,N09 | Deliberate stop-timeout and crash-boundary recovery unperformed |
| DS-012 | Job conflict/cancel/retry/retention subset and reindex readers passed | Q-12,N05 | Seven-day job expiry and deterministic cancellation at commit incomplete |
| DS-013 | N02 add, N07 noninteractive confirmation and source-preserving removal passed | Q-13,N02,N07 | Native removal dialog and environment alias scenario incomplete |
| DS-014 | Independent mandatory exclusion override, Git rules, size/hash and exact five-file ledger passed | Q-14,qa_i01,qa_i02,qa_i03,N02 | Full extension/encoding/configuration Cartesian matrix incomplete |
| DS-015 | All11 structural extension fixtures, exact BOM/function/docstring ranges and existing parser cases passed | Q-15,qa_u01,qa_u02,qa_u03 | All named kinds/import/comment associations and ERROR/MISSING shapes incomplete |
| DS-016 | Same-mtime changed bytes plus rename/delete convergence passed | Q-16,N04,N06 | Overflow/failure injection, unstable capture schedule and full5-minute timer incomplete |
| DS-017 | Parser-pool/cancellation regressions and fixed benchmark completed | Q-17,Q-BEN | Queue byte instrumentation, per-file timeout and CPU/RAM measurements incomplete |
| DS-018 | SQLite storage/corruption/schema-refusal regressions passed | Q-18 | Migration matrix and default directory/permission targets incomplete |
| DS-019 | Real active read transaction across two daemon publications; invalid snapshot rejection passed | Q-19,N05,qa_i04 | Crash exactly at commit and all version-retention cases incomplete |
| DS-020 | N02 exact counters, timestamp, generation, partial coverage observed | Q-20,N02 | All watcher/storage/parser error classifications incomplete |
| DS-021 | Corrupt-cache rebuild exact confirmation regression passed | Q-21 | 10MiB rotation/retention stress and full diagnostics/no-content cases incomplete |
| DS-022 | Full-size frame boundaries, budget bounds, validation/replay tests passed | Q-22,qa_u04,qa_u05,qa_i05 | Timed-out live mutations/full protocol matrix incomplete |
| DS-023 | Management CLI native lifecycle/index/job/removal/rebuild subsets passed | Q-23,N01..N09 | Full command/flag cross-platform matrix incomplete |
| DS-024 | Existing exit/envelope cases plus N08 version negotiation passed | Q-24,N08 | All emitted error families and shell boundary permutations incomplete |
| DS-025 | FAIL: generation and last reconciliation absent from rendered status; native screenshot confirms | Q-25,qa_u06,qa_u07 | QA-D01; full UI/menu/disabled-control/mixed-environment qualification incomplete |
| DS-026 | Startup defaults/read-only code and native exit preservation inspected/tested | Q-26 | Startup changes and systemd explicitly unperformed |

[acceptance-results.json](acceptance-results.json) separately lists all19 scenarios and per-platform limits. DS-A19 FAIL on both measured platforms because the quality floor fails; all WSL requirements remain NOT_RUN. No unexecuted scenario is promoted to PASS by a passing unit test or successful build.

## Integrity, incomplete work and retained attempts

[syntax-inventory.json](syntax-inventory.json) records31 first-party Rust files and192 attribute locators. Inspected attributes/imports use ordinary Rust cfg/test/path, serde derives/fields, clap commands and tokio runtime/tests. No first-party mock decorator/analogous mocking attribute was confirmed. Text inventory alone does not establish absence; complete macro/re-export and dependency-expansion investigation is INCOMPLETE. Relevant assertions/helpers were reviewed, with setup-only smoke tests excluded from product credit. No result-gaming finding confirmed; full integrity audit remains incomplete. QA helper sources are included in review scope.

Historical developer red/green/refactor chronology was not independently rebound/replayed. Existing traceability was inspected as claimed prior evidence, not acceptance. No product implementation or repair happened here, so no fabricated red/green repair result is reported.

[finding records](findings.json) contain QA-D01/D02 and QA-G01..05:
- QA-G01, platform owner/QA: WSL2 target left NOT_RUN by selected scope; two Windows WSL test functions ignored, not credited as passes.
- QA-G02, user/platform owner: Startup/systemd changes explicitly excluded; no settings/Run key/unit installation or WSL startup changes.
- QA-G03, QA/platform owner: Remaining native/negative/race acceptance subcases listed per criterion in report; no cross-account fixture, no deterministic crash-at-commit/overflow/unstable-capture campaign or complete UI matrix.
- QA-G04, QA: Three fixed-seed indexing benchmark repetitions completed per tested host, but CPU/RAM and sustained idle collection not instrumented; concurrent benchmark uses daemon.status, not content queries. Real read-transaction concurrency separately tested in N05.
- QA-G05, QA: 31 first-party Rust files/192 attribute locators inventoried; relevant syntax/imports and assertions inspected. No mocking/gaming confirmed. Complete macro/re-export/dependency and helper audit and historical TDD chronology not established. Full requirement-derived unit inventory remains incomplete; report18 declared units as bounded metrics, never complete inventory.

Preserved non-product/harness attempts: incompatible Windows collector option pair before tests; Ubuntu default LLVM-tool discovery failure before tests; Windows Clippy flagged a needless clone in the newly authored QA helper. The helper correction uses std::slice::from_ref, leaves assertions unchanged, and original coverage-tested helper bytes are preserved as qa_independent-coverage-v1.rs.txt (SHA25645e078b8aaba9d37e1a49d3163a238232e9cdf20260d7a9b0c39fecaeb4c9ce1). Final Clippy used corrected helper; runtime evidence remains bound to the original test helper. Initial metadata tooling lacked tomllib and an overescaped regex initially found zero test records; these were evidence-processing errors corrected before assessment, with metrics-parser-attempt001.json retained. No zero denominator was credited as100%.

## Disposition and handoff

QA verdict **FAIL**; QA-D01 and QA-D02 OPEN, remediation owner **dev**. [qa-fix.md](qa-fix.md) is the repair packet; final manifest supplies its SHA256. Original source and copied first-party source stayed byte-identical. Windows/Ubuntu owned product process inventories were empty at completion; both native acceptance runs confirmed shutdown. Scratch/build/evidence trees are retained. No old evidence deleted, no operational skill/source/startup/systemd changes, no WSL wake or installation. SSH sessions ended after transfer; archive hash verified before extraction.

External protected framework acceptance **NOT_EVALUATED**. No deployment or release permission. In this host's available-skill catalog, dev is present; no automatic dev invocation or agent handoff was performed.

Open C:\Projects\DevForgeAI in native Windows Codex and use the complete prompt in [dev-handoff.md](dev-handoff.md). The next owner repairs confirmed defects and returns a corrected candidate and evidence for independently selected QA retest. QA-G gaps remain separate qualification obligations.

