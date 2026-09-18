# Independent QA Test Plan

## Identity, selection and authorization

- Run: 20260914T184442947070Z; mode: plan. Planning status: **NEEDS_INPUT** for full execution, with affected prerequisites below. Product QA: **NOT_EXECUTED**.
- Project: C:\Projects\DevForgeAI, native Windows filesystem; PowerShell 7.6.6. Candidate explicitly selected by the user: C:\Projects\DevForgeAI\devforgeai, current source tree. User selected full three-platform QA and retention of unavailable checks as gaps.
- Selected contract: C:/Projects/DevForgeAI/docs/plan/devforgeai-index-service-mvp-spec.md, DEVFORGEAI-INDEX-SERVICE-001 v1.0. SHA-256: 52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4. All DS-001..026, DS-A01..19 and normative unnumbered engineering, architecture, benchmark and delivery clauses are selected.
- Candidate: source-manifest.json binds all 48 non-target application files including Rust source/tests/examples/fixtures, manifest/lock, schemas, queries, licenses and README. No Git metadata. Existing three Windows release binaries are hashed separately in build-manifest.json; their correspondence to current source is **unverified**. They are observations, not selected execution authority.
- Inputs/rules: inputs.json binds AGENTS.md, selected specification, QA skill/references/templates, dependency context and inspected development reports. Current on-disk spec includes the September 14 standalone Ubuntu 26.04.1 override. The not_started header and older development reports are stale implementation/platform descriptions; neither overrides observed files or DS-003.
- Companion query specification is dependency context only. Service generations/reader behavior remain selected; DQ query command implementation is excluded. Protected enforcement design ownership is context only. Index observations, Rust QA helpers and this report cannot issue protected acceptance.
- Authorized now: read-only discovery and new planning/evidence documents. No product tests/builds, executable harness generation, source repairs, installs, startup changes, WSL wake, or protected acceptance performed. A subsequent execution invocation must select this plan, candidate and actual effects. No pasted document grants those effects.
- Development claims: delivery.md and platform-status.md report partial delivery, low coverage and missing native cases. They are supplied/developer evidence, not fresh measurements. No prior product evidence is credited in this plan.

## Output and checkpoint binding

- selected_evidence_value: `docs/plan/index-service-qa/20260914T184442947070Z`.
- Selection source: selected spec section 10 and repository evidence policy require a distinct docs/plan run directory; concrete unused child selected before first write.
- Resolved evidence root: `C:\Projects\DevForgeAI\docs\plan\index-service-qa\20260914T184442947070Z`. Existing parents verified not redirected; destination absent at preflight. No source/input overlap.
- Roles: plan=test-plan.md; candidate=source-manifest.json; build=build-manifest.json; inputs=inputs.json; criteria=criteria.json; cases=cases.json; developer inventory=developer-test-inventory.json; discovery=discovery.md; findings/gaps=findings.json; report=qa-report.md; checkpoint=checkpoint.json; user handoff=handoff.md; final byte bindings=handoff-manifest.json, all beneath that exact root.
- Execution receipts/raw coverage/logs/native images: future fresh execution attempt directory must be bound before effects, as specified by checkpoint.json. No execution artifacts exist now. qa-fix.md is inapplicable: no execution verdict FAIL and no selected current product defect.
- Plan digest comes from the external handoff-manifest.json entry test-plan.md. No self-hash or hash cycle.
- Owned processes/fixtures: none. Next safe action: resolve host/effect/fixture prerequisites, then select a later execution plan revision with exact native paths and source/build identities. Do not blindly execute commands in this planning document.

## Acceptance inventory and risks

criteria.json preserves the complete exact DS requirement passages with source-line locators plus all 19 acceptance rows. The following mapped procedures supplement those complete obligations; oracle summaries do not narrow the source passages.

| Criterion | Case | Priority | Mandatory behavior/oracle |
| --- | --- | --- | --- |
| DS-001 | Q-01 | P1 | Three binaries on Windows, CLI/daemon on Linux, shared Rust client/protocol/index/platform ownership; daemon sole writer and CLI/tray never directly open SQLite. No Python, browser runtime, network listener/upload, operational skill or source mutation; bundled/pinned grammars and query versions. |
| DS-002 | Q-02 | P0 | Hash, length, parse ranges and text derive from the same captured bytes; only daemon writes application database; readers observe published state or typed management jobs. |
| DS-003 | Q-03 | P1 | Separate native builds and results; no WSL substitution for standalone Linux, no Windows build for Linux qualification; unsupported targets remain deferred. |
| DS-004 | Q-04 | P0 | Exactly one daemon owner per user/environment; unauthorized peers denied before effects. Stale PID never sufficient to kill a process; no TCP listener or cross-environment DB. |
| DS-005 | Q-05 | P0 | One unframed bounded JSON request/response, no banner/prompts or arbitrary shell/source writes; owning Linux user and DB only; bridge validates same protocol. Missing CLI has typed error. |
| DS-006 | Q-06 | P0 | No intentional wake by polling; second inventory check precedes invocation; race acknowledged. Explicit Start may wake, Stop never shuts down WSL. One poll per environment; visible 5s, hidden/backoff 30s. |
| DS-007 | Q-07 | P0 | Duplicate/overlap/escape and unsupported roots rejected; no directory-link traversal; outside regular links excluded; non-UTF8 paths skipped with reason. No silent environment translation. |
| DS-008 | Q-08 | P0 | Daemon/indexing/activity/coverage distinct; idle never implies complete/current. Complete only after successful reconciliation of eligible files; structural/text/excluded/skipped/error counts remain separate. |
| DS-009 | Q-09 | P0 | One owner; 10s default handshake deadline; already_running accurate; paused persisted; new environment active; Windows detached child has no visible console or held CLI pipe. |
| DS-010 | Q-10 | P0 | New scheduling stops immediately; paused only after writer quiescence; bounded dirty markers, IPC readable; full eligible-file reconciliation before caught-up; no duplicate work for already-active Resume. |
| DS-011 | Q-11 | P0 | Pending work cancelled; unpublished transaction rolled back; published data preserved; clean cancellations distinct from interrupted jobs; stopped target succeeds already_stopped. Timeout means uncertain continued stop. |
| DS-012 | Q-12 | P0 | Immediate opaque job IDs; one indexing job per project; JOB_CONFLICT existing ID; background coalescing, idempotent cancel, success unchanged, terminal records expire after 7 days. Rescan hash reuse; reindex parses all atomically; file gaps partial, job storage/scan failure no publish. |
| DS-013 | Q-13 | P0 | Canonical roots and independent IDs; no indexed-root config writes; removal cancels jobs and deletes only cache/registration; UI names target and effect; CLI requires --yes; alias removal does not stop/delete projects. |
| DS-014 | Q-14 | P0 | Exact inclusion/reason/counters from DS-014 clauses; global Git ignore not used; immutable BOM byte coordinates, no transcoding; mandatory exclusions not overrideable; oversized skipped. |
| DS-015 | Q-15 | P0 | Exact captures/ranges/parent and association kinds, no header misattachment or invented summaries; anonymous outline without named identity; partial parse status, syntactic-only resolution. Compare to manually specified ranges, never parser output reused as expectation. |
| DS-016 | Q-16 | P0 | Hash-driven convergence, no deleted-symbol orphans, newer dirty marker retained; bounded event memory; captured bytes and hash consistent; unstable source leaves dirty with reason; changing filesystem not claimed atomic. |
| DS-017 | Q-17 | P0 | Default two parse workers and one coordinator; cooperative 2s parse budget, timed-out file partial and work continues; queued captured bytes <=64MiB excluding stated allocations; cancellation checked at files/parser callbacks. |
| DS-018 | Q-18 | P0 | Private native local storage, no cross-env DB; metadata backup before migration; unsupported newer schema refused without destructive downgrade; FTS5 available. |
| DS-019 | Q-19 | P0 | Atomic pointer, no mixed generation IDs; current/previous retained with snapshots; active reader survives GC; old version provenance retained; failed/cancelled publication preserves prior pointer and bytes. |
| DS-020 | Q-20 | P0 | All DS-020 counts, jobs, generation and reconciliation time present; current/dirty/unknown with observation timestamp and coverage; gaps never complete. |
| DS-021 | Q-21 | P0 | Operation IDs/durations/counts/codes, no default source/query contents; bounded diagnostics, degraded status available, quarantine preserved and exact affected projects confirmed, no arbitrary deletion path. |
| DS-022 | Q-22 | P0 | 4-byte big-endian, request <=1MiB/response <=8MiB, one message pair; typed validation, version rejection before effect, all response fields/null rules; 100..120000ms/default10000 both service and end-to-end enforced; durable idempotent replay/conflict and unknown outcome retained. |
| DS-023 | Q-23 | P0 | Shared registry including handshake/reconcile/rebuild; explicit project IDs; one schema/examples set; immediate job ID versus --wait; wait timeout never cancels; no hidden Resume. Lifecycle controls independent of companion query implementation. |
| DS-024 | Q-24 | P0 | Exact exits 0,2..11; error data null and success error null; diagnostics stderr; job status failed outcome exit0 versus waited failure exit11; stopped daemon status exit0 vs unavailable operation exit3. |
| DS-025 | Q-25 | P1 | One tray/session, text distinguishes state, required status fields/coverage/jobs/errors; shared async client and responsive UI; explanatory disabled controls, no premature success/duplicate jobs, correct native folder versus WSL entry. |
| DS-026 | Q-26 | P0 | Both settings default off; only per-user tray entry, no elevation/WSL wake; separate daemon-start setting; exit keeps all daemons, stop-and-exit only selected target after confirmation/choice. Unit foreground Restart=on-failure, clean Stop not restarted; no linger/WSL config changes. |

Unnumbered obligations: section 1/1.1 authority/network/host/source custody and section 2 flow are covered by Q-01/Q-02/Q-04/Q-07; section 1.4 TDD/quality/terminal operation by Q-POL/Q-MET/Q-23/Q-26; section 9 reproducible benchmark by Q-BEN; section 10 delivery/deferred scope by Q-DEL. Recommendations require a documented deviation rather than silent omission. No advisory feature additions selected.

| Selected acceptance scenario | Cases with separate assertions required |
| --- | --- |
| DS-A01: two simultaneous Starts | Q-04, Q-09 |
| DS-A02: pause during scanning, edit files, resume | Q-08, Q-10, Q-16 |
| DS-A03: Stop and tray exit | Q-11, Q-26 |
| DS-A04: crash during publication/reindex | Q-12, Q-18, Q-19 |
| DS-A05: multi-environment Windows tray | Q-03, Q-05, Q-25 |
| DS-A06: stopped WSL and explicit start/stop | Q-05, Q-06 |
| DS-A07: unauthorized peer and invalid protocol | Q-04, Q-22 |
| DS-A08: root boundaries and removal | Q-07, Q-13, Q-14 |
| DS-A09: exclusions and encodings | Q-14, Q-20 |
| DS-A10: language adapter fixtures | Q-15 |
| DS-A11: edits, renames, deletes, overflow | Q-16 |
| DS-A12: atomic reindex with active readers | Q-12, Q-19 |
| DS-A13: resource cancellation and UI response | Q-17, Q-25 |
| DS-A14: schema/corruption recovery | Q-18, Q-21, Q-23 |
| DS-A15: protocol, output, and retry | Q-22, Q-24 |
| DS-A16: startup and systemd hosts | Q-03, Q-09, Q-26 |
| DS-A17: source immutability | Q-01, Q-13, Q-23 |
| DS-A18: benchmark | Q-17, Q-20, Q-BEN |
| DS-A19: engineering policy | Q-26, Q-POL, Q-MET |

Every acceptance result is NOT_RUN. A case family passes only if each applicable clause/subcase has evidence. Expand independent subcases into stable IDs Q-nn.01 etc before execution; missing subcase enumeration blocks completeness, never shrinks the denominator.

## Environment and capability matrix

| Required target | Current discovery | Capabilities and limits |
| --- | --- | --- |
| Windows 11 x64 | Microsoft Windows 11 Pro 10.0.26200, 64-bit; PowerShell 7.6.6; cargo/rustc 1.97.1; cargo-llvm-cov 0.8.4 | MSVC target installed, actual source and existing release binaries present; fresh native build/linker, dependency cache, LLVM collection, GUI and cross-account permissions not exercised. |
| Standalone Ubuntu 26.04.1 LTS x64 | SSH verified Ubuntu26.04.1 x64 at me@192.168.245.128, /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai; Rust/Cargo1.93.1 and cargo-llvm-cov0.9.1. All48 application source files and AGENTS.md match; remote specification hash differs. See ssh-discovery.json. Remote build correspondence and collector isolation remain pending. | Existing ubuntu-results directory observed, not independently evaluated or credited. Remote native source/OS/tools are verified; use the selected Windows specification, not the differing remote copy. Native binaries/output/collector bindings still pending. |
| Ubuntu 24.04 WSL2 | Inventory shows Ubuntu stopped, version 2; docker-desktop also stopped | Release/user/CLI/path/current source identity not verified. No Linux process launched. User must select isolated native fixture location and explicit Start effects; verify release and pwd/executable resolution before work. |
| Installed targets | i686-unknown-linux-musl, x86_64-pc-windows-msvc, x86_64-unknown-linux-gnu | An installed target is not a native test host. No target substitutes for another required platform. |

Initial CIM/WSL inventory was denied in sandbox; explicitly escalated read-only retry succeeded. No runtime test credit. Dependency graph is locked in Cargo.lock; minimum Rust 1.93/edition2024; native C compiler required per README. Network/dependency installation not selected. Native visual evidence requires real screenshots and observed actions, independently reviewed.

## Execution procedures and command provenance

README inspected from the bound candidate documents the build/test/fmt/clippy commands. Cargo llvm-cov version/help was read without running coverage. These are **conditional procedures, not executed commands**:

- Working directory for native Windows build procedures: C:\Projects\DevForgeAI\devforgeai. Set CARGO_TARGET_DIR to the separately bound fresh execution output directory before any Cargo build/test; set TMP/TEMP and DEVFORGEAI_INDEX_DATA to distinct owned fixture/data roots and DEVFORGEAI_GUI_EVIDENCE to the owned image destination. Confirm child inheritance and source/data separation. Restore previous environment values on exit.
- Release build: `cargo build --locked --offline --release`. Unit/integration/native regression inventory: `cargo test --locked --offline --all-targets -- --list`; this compiles and therefore is deferred to execution. After fixture/effect admission, `cargo test --locked --offline --all-targets`. Its GUI test spawns a visible tray; this aggregate must not run without native GUI effects selected.
- Formatting: `cargo fmt --all -- --check`. Static analysis: `cargo clippy --locked --offline --all-targets -- -D warnings`. Commands come from README; offline is the bounded adaptation to avoid unselected dependency downloads. Missing caches are a prerequisite failure; no auto-install or locked dependency update.
- Coverage options verified in installed help: `cargo llvm-cov --locked --offline --all-targets --json --output-path` plus the bound absolute report path, `--fail-under-lines 95 --ignore-filename-regex '[/\\](tests|examples|fixtures)[/\\]'`. This excludes only declared non-product paths; retain every first-party src module including Windows UI. The exact isolated coverage target/profraw environment must be verified with installed collector help before the command is admitted; do not let cleaning overwrite existing target/evidence. Child daemon/tray coverage requires inherited instrumented environment, normal owned shutdown and profile merge verification. Test process exit alone does not prove child coverage.
- Ignored WSL test commands after real fixture binding: `cargo test --locked --offline --test wsl_bridge native_wsl_bridge_preserves_pause_and_environment_identity -- --ignored --exact`; its source hardcodes Ubuntu/bryan and uses DEVFORGEAI_WSL_FIXTURE. This is not ready until that identity/path is explicitly verified. The absent-distribution test may supply a narrow negative regression, not DS-A06 installed-stopped credit. Both ignored cases remain visible and required native cases cannot be counted as passes merely by omitting them.
- Linux commands derive from the same manifest/README but require an explicitly selected Linux-native source/output path, OS/tool discovery and byte-equivalent candidate. No /mnt/c sustained build or automatic checkout copy/sync is authorized. Exact Linux invocation cannot be finalized before that selection.
- Native operation grammar is inspected in README/cli.rs: daemon start/run/status/pause/resume/stop/diagnostics, project add/list/update/remove, index status/rescan/reindex/rebuild, job status/cancel, environment add-wsl/list/remove, tray/settings show/set. Pass returned project/job IDs from receipts as data; do not invent IDs. Use process argument arrays, no shell interpolation. Each Q case binds exact command/action vectors at fixture admission.
- Timing budgets for execution harness planning: build/test/coverage 30 minutes per invocation; individual non-benchmark QA case 15 minutes; benchmark 30 minutes; protocol timeouts retain their specified 100ms..120s bounds and default10s. Harness budgets are observation cutoffs, not new product SLOs. Stream status at least every 60s. On timeout record ERROR/NOT_RUN as appropriate and observe owned process state before cleanup or retry.
- Retry budget: one deliberate attempt per case per candidate, except the three benchmark repetitions and retries explicitly required to test idempotency. Product capture's two allowed retries are behavior under test, not permission to erase QA failures. New attempts require a recorded reason/current authorization; preserve every raw attempt.

## Required case inventory and reusable case fields

cases.json binds stable case IDs, criterion mapping, category, platform, procedure, oracle, prerequisite and NOT_RUN status. All Q cases are independent QA design; existing developer tests are separately recorded, never substituted for whole case-family conformance. Platforms `all` mean Windows 11 x64; standalone Ubuntu 26.04.1 LTS x64; Ubuntu 24.04 WSL2; `windows+wsl` means Windows controller plus selected Ubuntu24.04 WSL2 target; `windows` means native Windows only.

For every Q case:
- Entry: selected candidate/plan unchanged, actual native host/path/build/tool/dependency binding, complete subcase inventory and specific test effects authorized.
- Fixture identity: synthetic, independently authored bytes plus expected-results manifest under the fresh execution fixture root; digest before first action. Golden expected bytes/coordinates must precede product observations. Existing developer fixtures are baseline regression inputs only.
- Isolation: owned data outside all indexed roots; QA fixture source distinct from application source; no current user daemon/state. Builds in owned output or explicitly authorized disposable source copy, verified before/after. Do not edit product/developer tests.
- Evidence: execution receipts.jsonl entries include case/platform/attempt, exact command or native action, working directory, start/end, tool/build/candidate/input hashes, exit/timeout, stdout/stderr, golden/actual assertions, cleanup, screenshot/raw-metric paths and digests.
- Actual observation: NOT_RUN; empty actual results are not success. Case-specific procedures below retain all source-clause expected outcomes in criteria.json.
- Cleanup: inventory only owned processes by PID plus executable/start-time/handshake identity; stop the owned daemon through its API, observe endpoint/process termination, then release owned fixtures. Preserve state/evidence on uncertain timeout. No recursive deletion of unverified paths, no kill based on stale PID, no distribution shutdown. Destructive crash fixtures require separate explicit permission.
- Sensitivity: for critical oracles, corrupt a returned snapshot digest, mark dirty/partial as complete, or change an expected range by one byte in a disposable **QA observation copy**; verify the oracle rejects it. This tests oracle sensitivity, not a product mutation or acceptance. Any candidate mutation study would need separate explicit disposable-copy scope.
- Category result and source-criterion result are separate; setup utilities never receive product acceptance credit.

### Q-01: Architecture and deliverables

- Criterion: DS-001; category: review; platform: all; priority: P1.
- Procedure: Review Cargo manifest, bins, imports and runtime dependency resolution; inspect CLI/tray call paths and database opens. Compare grammar-manifest entries, shipped query bytes and licenses to Cargo.lock. Inspect packaged release directory on each native host.
- Expected independent observation: Three binaries on Windows, CLI/daemon on Linux, shared Rust client/protocol/index/platform ownership; daemon sole writer and CLI/tray never directly open SQLite. No Python, browser runtime, network listener/upload, operational skill or source mutation; bundled/pinned grammars and query versions.
- Prerequisite/assertion limitation: Package dependency and binary correspondence audit remains pending.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-02: Capture-to-publication ownership

- Criterion: DS-002; category: integration; platform: all; priority: P0.
- Procedure: Create an independently specified multibyte fixture, capture then change the live file before extraction; inspect published record and snapshot through a Rust QA reader. Run concurrent publication/readers in disposable state.
- Expected independent observation: Hash, length, parse ranges and text derive from the same captured bytes; only daemon writes application database; readers observe published state or typed management jobs.
- Prerequisite/assertion limitation: Requires independent QA orchestration and verified source-to-build mapping.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-03: Native platform qualification

- Criterion: DS-003; category: native; platform: all; priority: P1.
- Procedure: Record native OS/release/architecture, binary hashes and source manifest on Windows 11, standalone Ubuntu 26.04.1, and Ubuntu 24.04 WSL2. Run applicable full suites separately. Inspect artifacts without installing.
- Expected independent observation: Separate native builds and results; no WSL substitution for standalone Linux, no Windows build for Linux qualification; unsupported targets remain deferred.
- Prerequisite/assertion limitation: Standalone host/evidence selection and WSL native path/user/release verification needed.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-04: Peer isolation and instance locking

- Criterion: DS-004; category: native; platform: all; priority: P0.
- Procedure: Start two owned clients concurrently; attempt local handshake as authorized alternate OS principal and malformed/remote peer. Inspect Windows DACL, remote-pipe rejection, Linux 0700 runtime/0600 socket and peer UID. Exercise XDG fallback, stale PID and conflicting authenticated instance.
- Expected independent observation: Exactly one daemon owner per user/environment; unauthorized peers denied before effects. Stale PID never sufficient to kill a process; no TCP listener or cross-environment DB.
- Prerequisite/assertion limitation: Alternate-principal fixture and permissions not supplied; no user-account creation authorized.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-05: WSL argument-vector bridge

- Criterion: DS-005; category: native; platform: windows+wsl; priority: P0.
- Procedure: Bind real installed WSL distribution, user, absolute CLI and source/build hashes. Register synthetic alias; send valid and invalid known operations and quote/metacharacter-bearing arguments via bridge stdin. Capture stdout/stderr, child argument vectors and Linux state.
- Expected independent observation: One unframed bounded JSON request/response, no banner/prompts or arbitrary shell/source writes; owning Linux user and DB only; bridge validates same protocol. Missing CLI has typed error.
- Prerequisite/assertion limitation: Distribution Ubuntu exists but is stopped; user, fixture path and Ubuntu release not currently verified.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-06: WSL polling and lifetime

- Criterion: DS-006; category: native; platform: windows+wsl; priority: P0.
- Procedure: On an explicitly selected installed-stopped test distribution, observe inventory before and after >30 seconds of hidden-window polling and >5 seconds visible polling; verify no Linux invocation. Explicitly Start, Stop only owned daemon, and observe unrelated process survival. Exercise failed probes/backoff and simultaneous polls.
- Expected independent observation: No intentional wake by polling; second inventory check precedes invocation; race acknowledged. Explicit Start may wake, Stop never shuts down WSL. One poll per environment; visible 5s, hidden/backoff 30s.
- Prerequisite/assertion limitation: Requires explicit lifecycle test effects and prepared stopped distribution; absent-distribution developer test is not this oracle.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-07: Native roots and traversal

- Criterion: DS-007; category: integration; platform: all; priority: P0.
- Procedure: Create sibling/overlapping roots, case variants under actual filesystem semantics, directory symlinks/junctions, inside/outside regular links, escape paths, UNC and WSL /mnt/drive roots. Try registration and capture including root without Git; include non-UTF8 Linux name.
- Expected independent observation: Duplicate/overlap/escape and unsupported roots rejected; no directory-link traversal; outside regular links excluded; non-UTF8 paths skipped with reason. No silent environment translation.
- Prerequisite/assertion limitation: Native links/permissions and WSL root fixtures require scoped effects; existing Unix link test does not prove Windows reparse behavior.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-08: State and accounting

- Criterion: DS-008; category: acceptance; platform: all; priority: P0.
- Procedure: Observe all lifecycle/index/job dimensions before first scan, midscan, paused, idle with dirty source, partial extraction and missing root. Compare counters to independent fixture ledger.
- Expected independent observation: Daemon/indexing/activity/coverage distinct; idle never implies complete/current. Complete only after successful reconciliation of eligible files; structural/text/excluded/skipped/error counts remain separate.
- Prerequisite/assertion limitation: Construct complete state/counter fixtures; existing single-file status assertions cover only subsets.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-09: Start/run semantics

- Criterion: DS-009; category: native; platform: all; priority: P0.
- Procedure: Run foreground host then ordinary termination; separately launch detached Start twice concurrently, Start while paused, restart paused state and Start already running. Collect PID/lock/handshake timelines and Windows console behavior.
- Expected independent observation: One owner; 10s default handshake deadline; already_running accurate; paused persisted; new environment active; Windows detached child has no visible console or held CLI pipe.
- Prerequisite/assertion limitation: Native terminal session and owned process capture needed; default startup settings untouched.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-10: Pause/resume boundary

- Criterion: DS-010; category: integration; platform: all; priority: P0.
- Procedure: Pause during actual multi-file scan while querying existing generation; wait for paused then verify writer inactivity. Make many fixture edits while paused, repeat Pause/Resume, and inspect resume reconciliation and dirty sequence.
- Expected independent observation: New scheduling stops immediately; paused only after writer quiescence; bounded dirty markers, IPC readable; full eligible-file reconciliation before caught-up; no duplicate work for already-active Resume.
- Prerequisite/assertion limitation: Independent file-boundary/writer observation required; developer sleep-based tests do not prove all races.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-11: Stop, crash and uncertainty

- Criterion: DS-011; category: native; platform: all; priority: P0.
- Procedure: Stop during queued/running work; observe commits, endpoint and PID for 10s. Create controlled delayed stop to observe TIMEOUT without auto-kill; inspect state before next action. Restart after graceful stop and separately authorized process interruption.
- Expected independent observation: Pending work cancelled; unpublished transaction rolled back; published data preserved; clean cancellations distinct from interrupted jobs; stopped target succeeds already_stopped. Timeout means uncertain continued stop.
- Prerequisite/assertion limitation: Delayed-stop/crash fixture and explicit owned-process interruption effects must be bound; no automatic retry.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-12: Job semantics and retention

- Criterion: DS-012; category: integration; platform: all; priority: P0.
- Procedure: Submit rescan/reindex concurrently, cancel queued/running/succeeded/cancelled jobs, scan same-content changed-mtime files then changed-content same-mtime files. Force extraction versus storage/scan failure; inspect 7-day expiry with controlled QA time/state fixture.
- Expected independent observation: Immediate opaque job IDs; one indexing job per project; JOB_CONFLICT existing ID; background coalescing, idempotent cancel, success unchanged, terminal records expire after 7 days. Rescan hash reuse; reindex parses all atomically; file gaps partial, job storage/scan failure no publish.
- Prerequisite/assertion limitation: Clock/expiry injection mechanism must be reviewed in disposable test code; no system clock changes.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-13: Project registration/update/removal

- Criterion: DS-013; category: acceptance; platform: all; priority: P0.
- Procedure: Add synthetic roots, update each typed setting, attempt unknown config, inspect opaque IDs/timestamps. Remove with/without --yes and via named UI cache-confirmation; hash source before/after. Unregister a WSL alias with daemon running.
- Expected independent observation: Canonical roots and independent IDs; no indexed-root config writes; removal cancels jobs and deletes only cache/registration; UI names target and effect; CLI requires --yes; alias removal does not stop/delete projects.
- Prerequisite/assertion limitation: Native dialog and mixed-environment fixture still needed; source manifest is independent oracle.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-14: Eligibility and byte encoding

- Criterion: DS-014; category: integration; platform: all; priority: P0.
- Procedure: Build ledger for .gitignore and .git/info/exclude, synthetic global-ignore rule, all mandatory exclusions, every configurable build default, sensitive patterns, hidden files, all listed extensions/names, untracked files. Test 1KiB/5MiB/50MiB boundaries, UTF8/BOM, binary/UTF16 and invalid bytes.
- Expected independent observation: Exact inclusion/reason/counters from DS-014 clauses; global Git ignore not used; immutable BOM byte coordinates, no transcoding; mandatory exclusions not overrideable; oversized skipped.
- Prerequisite/assertion limitation: Do not change real global Git config; use a disposable user/config environment after verifying isolation.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-15: Language extraction and documentation

- Criterion: DS-015; category: unit+integration; platform: all; priority: P0.
- Procedure: Independently author byte-exact golden fixtures for every structural extension, named kinds, imports/calls, nested/anonymous declarations and signatures. Include multibyte/BOM offsets, headers/adjacent/internal comments, Python docstrings, ERROR/MISSING with unaffected captures.
- Expected independent observation: Exact captures/ranges/parent and association kinds, no header misattachment or invented summaries; anonymous outline without named identity; partial parse status, syntactic-only resolution. Compare to manually specified ranges, never parser output reused as expectation.
- Prerequisite/assertion limitation: Current assertions often test substring containment; missing extension/kind/range cases need independent fixtures and capability review.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-16: Watcher/reconciliation races

- Criterion: DS-016; category: integration; platform: all; priority: P0.
- Procedure: Record 500ms debounce with monotonic clock; exercise full 5-minute reconciliation, restart/resume/config triggers, overflow/failure, atomic save, delete/rename, permission loss and unavailable root. Inject edit during reconciliation and unstable capture across initial attempt plus at most two retries.
- Expected independent observation: Hash-driven convergence, no deleted-symbol orphans, newer dirty marker retained; bounded event memory; captured bytes and hash consistent; unstable source leaves dirty with reason; changing filesystem not claimed atomic.
- Prerequisite/assertion limitation: Deterministic event/capture scheduling fixture and native watcher overflow procedure unresolved; no guessed timing acceptance margin.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-17: Resource bounds

- Criterion: DS-017; category: integration; platform: all; priority: P0.
- Procedure: Record worker/coordinator concurrency and admitted source queue bytes under large/slow files; cancel during parser work. Separate queue accounting from current file/parser allocation, record per-file duration and progress. Run benchmark case Q-BEN separately.
- Expected independent observation: Default two parse workers and one coordinator; cooperative 2s parse budget, timed-out file partial and work continues; queued captured bytes <=64MiB excluding stated allocations; cancellation checked at files/parser callbacks.
- Prerequisite/assertion limitation: Need observable queue/parser instrumentation in independent disposable fixture; cannot infer allocation bound from process RSS alone.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-18: Storage and schema recovery

- Criterion: DS-018; category: integration; platform: all; priority: P0.
- Procedure: Inspect default/override data paths and ownership, FTS5 and single-writer behavior; reject indexed-root/shared-mount storage. Create disposable older/current/newer schema and corrupt DB; compare bytes/metadata backups before/after open and migration.
- Expected independent observation: Private native local storage, no cross-env DB; metadata backup before migration; unsupported newer schema refused without destructive downgrade; FTS5 available.
- Prerequisite/assertion limitation: Migration fixture/schema support must be derived from inspected current storage code, not invented versions.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-19: Generation consistency and GC

- Criterion: DS-019; category: integration; platform: all; priority: P0.
- Procedure: Publish three generations with distinct hand-authored snapshots; hold a real read transaction across publication/GC; read current and preceding generations plus old record versions. Cancel/fail staged reindex and interrupt during publication at controlled points.
- Expected independent observation: Atomic pointer, no mixed generation IDs; current/previous retained with snapshots; active reader survives GC; old version provenance retained; failed/cancelled publication preserves prior pointer and bytes.
- Prerequisite/assertion limitation: Direct read-only Rust QA Store/SQLite inspection permitted as oracle, never a new product CLI DB path; crash-boundary trigger still needed.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-20: Coverage/freshness diagnostics

- Criterion: DS-020; category: acceptance; platform: all; priority: P0.
- Procedure: Reconcile a known eligibility ledger including parse timeout, unavailable root, unsupported extension and watcher/storage failures. Observe before/after edits, partial success and recovery; compare fields and timestamps.
- Expected independent observation: All DS-020 counts, jobs, generation and reconciliation time present; current/dirty/unknown with observation timestamp and coverage; gaps never complete.
- Prerequisite/assertion limitation: Fixture ledger and exact counter convention must be compared to all DS-014 rules; not inferred from status output itself.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-21: Logs and corrupt rebuild

- Criterion: DS-021; category: integration; platform: all; priority: P0.
- Procedure: Use synthetic source/query markers, inspect default logs and >10MiB rotation boundary with five-file retention. Corrupt only owned DB; call status/diagnostics, preview rebuild across two projects, reject mismatched confirmation then explicitly rebuild. Compare corrupt bytes in quarantine and recover registrations.
- Expected independent observation: Operation IDs/durations/counts/codes, no default source/query contents; bounded diagnostics, degraded status available, quarantine preserved and exact affected projects confirmed, no arbitrary deletion path.
- Prerequisite/assertion limitation: Log generation fixture and rebuild effects pending; no modification of current user state or preexisting evidence.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-22: Protocol and retry boundaries

- Criterion: DS-022; category: unit+integration; platform: all; priority: P0.
- Procedure: Exercise raw framed transport and bridge with 0/limit/limit+1/truncated payloads, invalid UTF8/JSON, UUID/version/operation/params/budget boundaries. Reuse request ID identical then changed payload before/after restart and at 24h expiry; timeout after accepted mutation then observe without replay.
- Expected independent observation: 4-byte big-endian, request <=1MiB/response <=8MiB, one message pair; typed validation, version rejection before effect, all response fields/null rules; 100..120000ms/default10000 both service and end-to-end enforced; durable idempotent replay/conflict and unknown outcome retained.
- Prerequisite/assertion limitation: Raw transport/clock fixtures to author; existing framing test uses size 3/4 not full-size allocation boundary.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-23: Management CLI completeness

- Criterion: DS-023; category: acceptance; platform: all; priority: P0.
- Procedure: Enumerate every DS-023 command, global flag, config schema and internal operation; inspect parser plus native outputs. Run add/list/update/remove, rescan/reindex --wait and paused queue, job status/cancel, rebuild preview and exact list. Use literal spaces/Unicode/metacharacters in native shell arguments.
- Expected independent observation: Shared registry including handshake/reconcile/rebuild; explicit project IDs; one schema/examples set; immediate job ID versus --wait; wait timeout never cancels; no hidden Resume. Lifecycle controls independent of companion query implementation.
- Prerequisite/assertion limitation: Independent command matrix to bind at execute; IDs are values obtained from receipts, not fixed source constants.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-24: JSON, errors and exit codes

- Criterion: DS-024; category: unit+native; platform: all; priority: P0.
- Procedure: Capture stdout/stderr and OS exit for every DS-024 category and successful no-op, malformed CLI, stopped status and stopped request. Validate JSON strictly as exactly one complete envelope, no prompts, and run both PowerShell/POSIX argument cases.
- Expected independent observation: Exact exits 0,2..11; error data null and success error null; diagnostics stderr; job status failed outcome exit0 versus waited failure exit11; stopped daemon status exit0 vs unavailable operation exit3.
- Prerequisite/assertion limitation: Full emitted error matrix and deadline fixtures still required; schema serialization tests alone insufficient.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-25: Native tray interactions

- Criterion: DS-025; category: native+visual; platform: windows; priority: P1.
- Procedure: Capture screenshots/actions for tray/tooltips and compact window in disconnected/active/paused/error states; attempt second instance; exercise environment/project selection and all controls, root picker/WSL text, repeated clicks, slow IPC and inapplicable actions.
- Expected independent observation: One tray/session, text distinguishes state, required status fields/coverage/jobs/errors; shared async client and responsive UI; explanatory disabled controls, no premature success/duplicate jobs, correct native folder versus WSL entry.
- Prerequisite/assertion limitation: Visible Windows session and explicit GUI test effects needed; existing native smoke does not establish full visual/menu/multi-env behavior.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.

### Q-26: Startup, settings and exit

- Criterion: DS-026; category: native; platform: all; priority: P0.
- Procedure: In an explicitly authorized disposable account/VM snapshot original startup state; inspect both defaults, run tray settings show/set while daemon unavailable, toggle opt-ins and read back registry/settings. Verify exit alone and selected stop-and-exit including timeout choice. On Linux inspect/run optional user unit under one supervisor and explicitly Stop.
- Expected independent observation: Both settings default off; only per-user tray entry, no elevation/WSL wake; separate daemon-start setting; exit keeps all daemons, stop-and-exit only selected target after confirmation/choice. Unit foreground Restart=on-failure, clean Stop not restarted; no linger/WSL config changes.
- Prerequisite/assertion limitation: Startup mutation/systemd installation are separate explicit authorizations, not included in generic test permission; qualified disposable host/user and restoration observation required.
- Common fixture/effects/evidence/cleanup/attempt rules above apply; current actual/status: NOT_RUN.


### Q-BEN: reproducible native benchmark

DS-A18, DS-017, DS-020 and section9. All three targets independently. Bind seed20260913, 10,000 files, exactly104857600 UTF8 bytes, five balanced Rust/Python/JS/TS/text groups, documented100-file edit batch and fixture manifest. The inspected examples/benchmark.rs creates this workload and three repetitions, accepts optional first argument for manifest destination, and performs concurrent daemon.status reads. That measures management responsiveness, not indexed-content query concurrency.

Use the inspected example as a baseline only after execution selection: `cargo run --locked --offline --release --example benchmark --` followed by bound fixture-manifest path. Capture all three raw repetitions, cold/warm/edit elapsed times and configuration. Independently add concurrent real read transactions against published source/generation records for service-level query behavior (Q-19); do not require the unselected DQ command extension. Record hardware/build/grammar versions, CPU and memory for all owned processes and idle activity over a declared observation window (60s default observation window, not an SLO). Host-specific resource collector and Linux paths remain prerequisites. No fabricated CPU/RAM from example output; no comparison threshold beyond specified correctness/resource bounds. Each repetition gets its own attempt suffix, one required benchmark family per platform.

### Q-POL: development engineering evidence

Section1.4, DS-A19. Read the original developer red/green/refactor/regression evidence with source/version/time bindings. Verify a real requirement failure preceded the matching repair, not a setup error or rewritten test expectation. Never manufacture historical red evidence. Missing chronology is an evidence gap. Check terminal equivalents of all selected management/startup operations, Rust-only application implementation, native UI distinction, no operational skill writes or protected acceptance claim. No product tests executed now.

### Q-DEL: delivery and documentation

Section10, DS-001, DS-003, DS-023, DS-026. Review source, locks, bundled grammar/query manifests/licenses, protocol schemas/examples against actual registry, synthetic fixtures, native binaries/build receipts and source correspondence, optional unit/startup examples and user documentation. Resolve stale not_started/platform claims at assessment without editing them in QA. Check local links exist and command help agrees when execute is authorized. Query extension, SCM hosting, remote/MCP/embeddings/compiler semantics/skills/hooks/framework enforcement and all listed deferred features remain excluded.

### Q-MET: complete metrics and integrity accounting

Apply the declared metrics below independently on every platform and overall; reconcile raw results to unique case IDs. This is an evidence calculation, not protected authority. Missing denominator, profile or required case is a gap. Do not reuse old summaries as counts.

## Test-integrity inspection

- Bound scope: all source-manifest.json first-party Rust implementation, tests, examples and fixture generator plus any future QA helpers. Generated dependency code/licenses are not first-party mock uses; first-party attributes invoking dependencies are in scope.
- Planning inspection: read test assertions in protocol, capture, storage, service, platform, CLI, IPC, process, tray, GUI, WSL bridge and harness sources to varying depth; fixture/benchmark source only partially inspected. Inventory textual test/attribute locators in developer-test-inventory.json. This is **partial inspection**, not an absence claim for mocking/gaming.
- Syntax/alias procedure for execute admission: enumerate every attribute/import/macro invocation in all first-party files, resolve proc-macro paths, reexports, wrappers and factories using Cargo.lock and actual source. Inspect each test body and helper. Any unresolved dynamic/macro expansion is an inspection gap. Text search alone cannot establish absence.
- Confirmed planning observations: harness.rs asserts size_of::<u32>() ==4 and provides no product behavior evidence; categorize setup and preserve it. benchmark_fixture.rs validates fixture generation and is also setup, separate from product unit metrics. WSL stopped_distribution_is_never_invoked_by_a_status_poll uses a deliberately absent distribution, so it cannot establish installed-stopped DS-A06.
- Existing protocol tests exercise important decode/frame/exit rules but omit some production-size/in-flight cases; capture tests often use containment instead of exact complete golden captures. Add independent unit/acceptance cases rather than repair these tests.
- Gaming assessment remains INCOMPLETE. The setup test alone does not prove deceptive reporting, and the developer report explicitly denies product credit. Confirm FAIL only with source/claimed behavior evidence: vacuous success credited as conformance, swallowed errors, fabricated output, fake integration, skipped/retried counts manipulated, coverage suppressions or expected results derived from the same defective logic.
- Any confirmed first-party mocking decorator/analogous attribute, even unused/resolved alias, is prohibited under selected QA policy. No clean finding or product FAIL is asserted from this partial planning review.
- Negative controls use disposable QA observation copies only; do not alter original candidate or old evidence.

## Metrics and accounting declared before execution

- Product executed-line scope: every first-party executable Rust line in devforgeai/src compiled for each required platform, all three bins and native adapters where applicable. No source-file exclusions to improve percentages. Exclude tests, example/fixture utilities, vendored grammars and external/generated dependency code from **product** denominator; inspect utilities for integrity separately.
- Source manifest enumerates eligible files; exact executable-line count is collector-derived and unavailable before execution. Record platform cfg exclusions explicitly, e.g. Windows adapter not compiled on Linux; retain it on Windows.
- Required unit inventory: developer-test-inventory.json locates39 test functions across source;11 pure component-behavior tests provisionally categorized unit, remaining tests integration/native/setup. Rust integration-test target placement alone does not decide behavioral category. Missing independent protocol boundary, exact adapter fixture, scheduling/retention and CLI mapping units are explicit gaps; final required unit denominator **unresolved** until case expansion/native enumeration is complete. Do not present11 as the complete denominator.
- Each required case/platform pair counted once; failed, errored, ignored/skipped, blocked and unexecuted required cases nonpassing. Both ignored Windows WSL cases remain tracked in native inventory; no silent omission.
- Independently require line coverage >=95% and required unit-test pass rate >=95% under QA skill. Additionally repository/spec require >=95% over the entire declared required QA suite; report that separate metric too, with category counts. Do not mix acceptance/native/setup counts into unit rate; setup receives no product-case credit.
- Coverage =100*executed eligible lines/all eligible executable lines. Unit rate =100*passing required unit cases/all required unit cases. Overall compatible counts sum numerator/denominator across native platform pairs, never union Windows/Linux hits or average rounded percentages. Record integer counts/exact fractions and compare without rounding.
- Missing/zero/unresolved denominator means NOT_RUN/INCOMPLETE, never100%. Branch coverage separately: installed collector labels --branch unstable; compatibility not established, therefore NOT_RUN unless a supported native collection is explicitly selected. This does not replace executed-line measurement.
- Raw outputs/collector settings and identities retained in fresh execution scope; missing child profiles, tool gaps or candidate drift invalidate affected measurements. Current values: all NOT_RUN; historical development percentages not reassessed.
- No thresholds waive a mandatory failure, integrity violation or regression.

## Existing evidence proposed for reuse

No product test/coverage result is admitted for reuse now. Bound developer context/delivery/platform reports are inspection inputs only. Their Windows2744/3442 and WSL2071/2786 coverage figures are reported historical claims, not current QA measurements; they remain visible as risk. The older standalone24.04 language is superseded by current DS-003. Discovered ubuntu-results directories and existing binaries require source/spec/raw-receipt/host identity validation before any later reuse.

## Entry, exit and final user handoff

Execution entry gaps:
1. E-01 (user/QA): select this concrete plan for execute and authorize exact effects. Current invocation only plans.
2. E-02 (platform owner): verify the supplied SSH Ubuntu host at me@192.168.245.128, /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai (OS and byte equivalence still pending), and select Ubuntu24.04 WSL2 user/CLI/native fixture path; bind equivalent candidate bytes without unselected copying/installation or waking WSL.
3. E-03 (user/platform owner): native GUI access, isolated alternate-principal fixtures, explicit owned-process crash tests, and separate startup/systemd opt-in test authority with restoration procedure.
4. E-04 (QA): author independent fixtures/subcase map in authorized future QA location; resolve boundary/expiry/overflow/capture timing instrumentation, exact host commands, executable/source correspondence, collector target/profile isolation and complete required unit denominator.
5. E-05 (QA): complete syntax/alias/test-integrity inspection, golden-oracle sensitivity, historical TDD evidence review and any prior evidence revalidation.

NEEDS_INPUT means the full plan is not executable yet; missing hosts/effects may remain NOT_RUN during a later explicitly scoped execution, but never qualify full PASS. Preparation does not require altering application code or operational copies.

Exit rules: planning READY or NEEDS_INPUT only. During execute FAIL takes precedence for confirmed mandatory conformance/integrity/regression failure or measured subthreshold metric. Otherwise required missing evidence yields INCOMPLETE. PASS requires every selected mandatory obligation and both QA floors plus repository required-suite floor per target and overall. QA recommendations never grant protected framework acceptance or release/install permission.

Publication: read back all actual files at this literal destination and bind final SHA256 values in handoff-manifest.json; verify current source/input digests have not drifted. On resume reread input/candidate/plan/tool/effect identities, stop affected checks on drift, retain old attempts and observe any owned processes before uncertain effects.

Open C:\Projects\DevForgeAI in native Windows Codex. Host catalog exposes qa and dev, but no follow-on skill/session is invoked. Next owner: user/platform owner for E-01..03; QA for E-04..05. A READY execute prompt is intentionally absent while those prerequisites remain unresolved. See handoff.md for exact next inputs. Product QA NOT_EXECUTED; framework acceptance NOT_EVALUATED; release authorization not granted.

## Final planning updates

SSH verified Ubuntu26.04.1 x64 at me@192.168.245.128, /home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai; Rust/Cargo1.93.1 and cargo-llvm-cov0.9.1. All48 application source files and AGENTS.md match; remote specification hash differs. See ssh-discovery.json. Remote build correspondence and collector isolation remain pending.

E-02 standalone host/source selection is resolved; remaining E-02 work is remote build/selected-spec access and WSL identity/fixture binding. No checkout copy, remote specification repair or installation was performed. All SSH connections ended. Scenario case mapping was checked against source rows and corrected during document readback before final publication. See publication-check.json for final factual/link/identity/coverage-of-plan checks (documentation checks only).

