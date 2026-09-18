# Offline worker harness delivery

**Overall development status: COMPLETE for the selected offline harness and developer QA.** Independent QA and native qualification are separate, unperformed selections. Framework acceptance is NOT_EVALUATED.

## Candidate and outputs

- Selected contract: DFF-WORKER-FEAS-01 v1.0.0, `docs/specs/framework/runtime/codex-worker-feasibility-v1.md`, SHA256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`.
- Package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, with its own Cargo workspace and lockfile. Implemented strict request/profile admission, atomic Windows process ownership, bounded stdio protocol, durable journal, read-only inspection, cancellation, usage observations and independent exact-result comparison. External peer, hidden-console driver and abrupt-exit driver exercise actual process boundaries.
- [Frozen source/test manifest](final-source-test-manifest.json): SHA256 `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604`; identical to [the checked candidate](063-clippy/candidate.json). All 31 package files read back unchanged in [candidate-readback.json](candidate-readback.json). The earlier source-test-manifest.json is an intermediate failed-compilation candidate, not this delivery.
- [Binary identities and retained copies](binary-manifest.json), [tool versions/executable hashes](tool-identities.json), [exact fixture provenance](fixture-provenance.json), [requirement/subfixture mapping](traceability.md), [execution lineage](executions.jsonl), and [independent QA handoff](independent-qa-handoff.md).
- All 335 manifest-selected inputs and both index Cargo files matched their initial identities: [input-final-checks.json](input-final-checks.json). No index source, operational skills, startup configuration or dependencies were installed or changed by this work.

## Executed Windows checks

Native Windows 11 Pro / kernel 10.0.26200, PowerShell 7.6.6, C: filesystem. All Cargo commands ran from the package path above. Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4; exact resolved launchers and toolchain executables are in tool-identities.json. Offline dependency resolution used existing cache.

| Attempt | Exact Cargo argv | Exit/result |
| --- | --- | --- |
| `063-clippy` | `cargo clippy --locked --offline --all-targets -- -D warnings` | 0 / PASS |
| `064-format-check` | `cargo fmt --all -- --check` | 0 / PASS |
| `065-coverage` | `cargo llvm-cov --locked --offline --all-targets --json --output-path C:/Projects/DevForgeAI/docs/plan/framework-worker-implementation/20260915T1544548240203Z/coverage-05.json` | 0 / PASS |
| `066-tests` | `cargo test --locked --offline --all-targets` | 0 / PASS |

Each attempt directory retains cwd, executable hash, start/end, source/test manifest and stdout/stderr hashes in receipt.json. The evidence recorder command prefix is `python -B -X utf8 docs/plan/framework-worker-implementation/20260915T1544548240203Z/record.py <attempt> qa`; executions.jsonl retains actual invocations. Normal and instrumented suites used separate build outputs and disjoint fixtures while overlapping in wall time.

- Mandatory offline cases: **20/20 = 100%**, with all required subfixtures. Final failed/errored/skipped/blocked/unexecuted mandatory counts: **0/0/0/0/0**. Every case counts once per candidate; retries do not inflate 20.
- Supplemental cases: **26/26** passed in each final suite. See [actual test names and retained fixture roots](final-test-inventory.json). The production 120-second watchdog and real Ctrl+C/descendant/crash checks executed.
- Executed-line coverage: **1310/1374 = 95.34206695778748%**, meeting >=95% without rounding. [Full JSON](coverage-05.json) and [raw summary](coverage-05.summary.json).
- Denominator: every first-party executable line under src, including CLI, native adapter, Windows and error paths. No runtime exclusions; tests/support/fixtures and generated/vendor dependencies excluded. lib.rs contains declarations with no executable lines. Per-file values below expose remaining uncovered code; the selected threshold applies to the full package denominator.
- Branch coverage: **NOT_RUN**; stable collector used, no unstable compiler/collector installed.

| Runtime file | Covered/executable lines | Raw percentage |
| --- | --- | --- |
| journal.rs | 216/220 | 98.18181818181819% |
| main.rs | 80/86 | 93.02325581395348% |
| oracle.rs | 7/7 | 100.0% |
| process_windows.rs | 241/254 | 94.88188976377953% |
| protocol.rs | 403/418 | 96.41148325358851% |
| request.rs | 250/263 | 95.05703422053232% |
| runner.rs | 113/126 | 89.68253968253968% |

## Earlier attempts and limitations

TDD and repair attempts are retained with interpretation in [development-notes.md](development-notes.md). Setup/compiler errors are distinguished from behavioral Red. Earlier full coverage results 81.6782%, 94.4529%, and 94.9782% remain failures on their respective candidates. A 95.0073% earlier candidate was superseded by the grace repair. No earlier evidence was erased or used to qualify changed bytes. Final checks have no unresolved observed test failure; independent review may find gaps beyond these developer cases.

Native WN-01/WN-02: **NOT_RUN, 0/2 demonstrated passes**, no native qualification. No Codex launch, authentication, live account/configuration review or model trial occurred. Metadata-only admission found a reparse component in the captured launcher path; resolving that identity/path dependency and selecting a reviewed Pro model/effort profile are prerequisites for a separately authorized native trial. The adapter's native runtime paths are not demonstrated by peer success. AMB-01/02/16 and production dispatch remain unresolved. No protected authority response was requested or produced.

Windows is the only selected offline host. Linux/WSL and visual application QA are NOT_APPLICABLE to this bounded terminal experiment; they are not qualified by these results. The process tests prove the tested owned process-tree behavior, not file/network isolation or production support. Request snapshots are normalized JSON; original caller formatting is not preserved as request.json. Original test inputs remain in retained fixture roots.

## Destination readback and continuation

Original handoff selected a fresh absolute child of docs/plan/framework-worker-implementation/. Before writes, [context.md](context.md) bound the complete destination to `C:\Projects\DevForgeAI\docs\plan\framework-worker-implementation\20260915T1544548240203Z`. The original handoff was reread; all promised source outputs remain under the isolated package and reports under that exact root. [output-readback.json](output-readback.json) enumerates required absolute paths, actual readback paths, byte lengths and SHA256. No path substitution or location correction is pending. R01..R18 have implementation/check accounting in traceability.md; native and protected dependencies are expressly separate.

Next step: separately select [independent QA](independent-qa-handoff.md) against the frozen candidate and contract. The developer has not closed independent findings. Native trials require their own selection and reviewed profile. [Checkpoint](checkpoint.md) records this boundary. Development completion grants no framework acceptance.
