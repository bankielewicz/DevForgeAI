# Linux and WSL coverage extension

**FAIL for both measured line-coverage floors and Unix Clippy.** All collected Linux unit/integration tests pass, including the repaired tray formatter assertions. The Windows-to-WSL bridge pause/identity test remains incomplete due to a fixture error. This is developer testing, not independent QA closure.

The user extended the active task with “test wsl & linux coverage” and supplied `me@192.168.245.128`. The corrected candidate is unchanged: parent [source-manifest.json](../source-manifest.json), SHA256 `cf3ee99015db0dcc1eb544fdac1bfdb0fcd2f10bfc8b749857d52740d8258094`. Selected spec SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`. No product edits or remote checkout synchronization occurred during this test extension.

| Check | SSH Ubuntu 26.04.1 | WSL2 Ubuntu 24.04.5 |
| --- | --- | --- |
| Native source identity | 61 files match corrected candidate | 61 files match corrected candidate |
| Executed-line coverage | **2410/2830 = 85.15901060070671%, FAIL** | **2418/2830 = 85.4416961130742%, FAIL** |
| Cargo product cases | 75/75 PASS | 75/75 PASS |
| Original declared units (subset) | 18/18 PASS | 18/18 PASS |
| Setup cases, no product credit | 2/2 PASS | 2/2 PASS |
| Formatting | PASS, exit 0 | PASS, exit 0 |
| Clippy all targets, -D warnings | FAIL, exit 101 | FAIL, exit 101 |
| Release binaries and WSL example | PASS, exit 0 | PASS, exit 0 |
| Branch coverage | NOT_RUN | NOT_RUN |

All 77 collected cases ran on each Linux host; no ignored/failed Cargo cases. Native Windows-only test modules are not applicable inside Linux and are not claimed as Linux passes. Windows-to-WSL tests run separately on Windows. Counts are per unique case per host, not accumulated attempts. Full acceptance and integrity inventories remain incomplete.

Evidence: [Linux metrics](linux/metrics.json), [Linux raw coverage](linux/coverage.json), [Linux test output](linux/attempts/coverage/stdout.txt), [Linux completion/builds](linux/completion.json); [WSL metrics](wsl/metrics.json), [WSL raw coverage](wsl/coverage.json), [WSL test output](wsl/attempts/coverage/stdout.txt), [WSL completion/builds](wsl/completion.json). Each host has exact argv/cwd/environment/source-bound receipts under `attempts/`, native tool versions in `tools.json`, a unique test inventory, profile-manifest.json and retained raw/merged profiles. Source/build paths remain native Linux paths, not `/mnt/c` build trees.

## Observed gaps

QA-D02 still fails on Linux and WSL. The largest gaps are CLI (229 uncovered Linux, 227 WSL), tray shared support (48 each), platform support (42 Linux, 37 WSL), service (35 Linux, 34 WSL), and client (23 each). Coverage counts all 13 compiled first-party files including binaries. Original exclusions remain tests/examples/fixtures, dependencies and generated code; no first-party behavior is removed or suppressed. A successful test process does not waive the 95% floor.

Additional portability regression observed in developer tests: `tests/coverage_edges.rs:3` imports `platform` outside its Windows-only uses; WSL Clippy also reports `tests/platform.rs:48` importing `Path` outside its Windows-only block. These are strict unused-import failures, not Rust build or runtime failures. Both native Clippy receipts and stderr are retained. They require a focused developer correction and subsequent source-matched checks; no warning suppression or source mutation was used to make this testing result pass.

## Native Windows-to-WSL bridge

[bridge/receipt.json](bridge/receipt.json) records `cargo test --locked --offline --test wsl_bridge -- --ignored --test-threads=1`, Windows cwd and explicit `DEVFORGEAI_WSL_FIXTURE`, against the same candidate. Exit 101: `stopped_distribution_is_never_invoked_by_a_status_poll` PASS; `native_wsl_bridge_preserves_pause_and_environment_identity` FAIL before obtaining its initial handshake envelope (`WslCliMissing`, child exit 1). The passing probe uses a deliberately absent distribution, so it does not qualify the installed-but-stopped distribution lifecycle matrix.

The native fixture binaries were copied with matching SHA256 to a short isolated `/tmp` path before the test, to respect Unix socket path limits. [Post-run diagnostic readback](wsl-final-readback.json) found that directory and executable absent; the persistent build binaries and candidate still match. This supports an unresolved fixture/setup ERROR, not a confirmed product bridge defect. The cause and exact removal time were not established. No automatic retry occurred and no successful pause/identity claim is made. A later selected continuation should use a persistent short fixture location, verify it immediately before invocation, retain this attempt and run a new attempt.

## Identities and preservation

SSH isolated project: `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai`. Existing `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai` was read, not modified; its 48 original entries had no drift and the complete before/after snapshot matches. Remote AGENTS.md was read; Git metadata absent and Git executable unavailable. Native Rust 1.93.1, cargo-llvm-cov 0.9.1, LLVM 21.1.8.

WSL isolated project: `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai`. The unrelated `/home/bryan/Projects/DevForgeAI` checkout was not selected or changed. Native Rust 1.98.1, cargo-llvm-cov 0.9.0 and its bundled LLVM. The installed Ubuntu distribution was started for user-requested tests; docker-desktop was not selected or changed.

[Transfer manifest](transfer-manifest.json) binds candidate archive SHA256 `30b2cd9d0ace40fef3109af5c7194408629f0c1f6f7ed76ea3f521d0b8088dbd`, checked before extraction on both hosts. Fetched evidence archive hashes were checked before safe local extraction: Linux `4ce12761fe4f1c5a52ae576825d133c8c171d7291586eb60671f832d91665744`; WSL `72a8832a7d1626af1c6c98218c188ec630a5b53aa0591d29b5a32dee116b486a`. These preserve native paths and raw receipts; local relocation does not imply execution on Windows.

| Host | Built artifact retained at native path | SHA256 |
| --- | --- | --- |
| linux | `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai/target/release/devforgeai` | `1ec5df2442e956be9fccb88ad64c322ccc388dbf17517835e5522b0cda95bf70` |
| linux | `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai/target/release/devforgeai-indexd` | `c6b3360a50863d70b728550b55a622474bffb1992b0b68edbf3b7f87b9489f3c` |
| linux | `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai/target/release/devforgeai-tray` | `2b9f750406f7da92e240240124e3e669f4c272245e8aed8616c3ac9091e4d838` |
| linux | `/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/dev-remediation/20260914T1950304158791Z/devforgeai/target/release/examples/wsl_fixture` | `115e923432da6db8c024437355a818c176d399385bdc4e2f11ab5d0f88debb38` |
| wsl | `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai/target/release/devforgeai` | `51a6013f96a41f5f7ccbac285596ac7594270b448bb859345d2064b6da4e1f40` |
| wsl | `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai/target/release/devforgeai-indexd` | `37c4b274e7e4ad78ad1170ee3bc58e4d8513f1b559152e3506a6041dda87d01a` |
| wsl | `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai/target/release/devforgeai-tray` | `8be167d388be740b6c54ab263a94893da6e7c8cddb1ee1b5c4b07a1be5fae98b` |
| wsl | `/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z/devforgeai/target/release/examples/wsl_fixture` | `eb1c31135dde39c54921a97565ca682b07b4f1946a651601962475180d6c0c74` |

The user-supplied credential was used only for SSH authentication and is absent from evidence files. No installation, deployment, dependency upgrade, startup/systemd changes, operational skill edits, or original checkout overwrite occurred. Remote completion and final WSL readback show no owned product process remaining. The SSH session was closed. Initial sandbox WSL enumeration AccessDenied was separately followed by approved native discovery; no setup error was counted as a behavioral pass.

Evidence root is exactly `C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z\platform-extension-001`, as bound in [context.md](context.md) before native writes. [extension-manifest.json](extension-manifest.json) and parent verification.json provide path/hash readback. The earlier parent Windows-only draft report is historical scope; this report supersedes its Linux/WSL NOT_RUN statements with current measured failures.

Next owner: dev for Linux/WSL coverage gaps and Unix test-import correction, followed by independent QA retest of the corrected candidate. Bridge fixture continuation remains separate from product defect confirmation. QA-D01/D02 stay OPEN until independent QA; full qualification INCOMPLETE; framework acceptance NOT_EVALUATED.
