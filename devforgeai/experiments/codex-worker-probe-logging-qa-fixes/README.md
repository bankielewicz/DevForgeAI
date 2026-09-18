# Codex worker probe with Rust logging

Isolated Windows Rust experiment implementing [DFF-WORKER-FEAS-01 v1.0.0](../../../docs/specs/framework/runtime/codex-worker-feasibility-v1.md). This package supplies offline observations; it issues no framework acceptance and does not close framework work. Native Codex/Pro trials require a separate explicit selection and reviewed profile. No native trial has been executed in this implementation task.

## Logging candidate

This fresh candidate extends the preserved worker probe. The [logging contract](logging-contract.md) specifies the added behavior and the narrow amendments to the inherited contracts below. Development evidence is in [the logging run](../../../docs/plan/framework-worker-logging/20260917T014842Z-dev/context.md).

This sibling candidate reports development fixes for QA-LOG-01 and QA-LOG-02. Current capture-bearing `completed` and `preflight_checked` observations require complete stream capture and a mandatory post-stop exit matching the successful terminal. Failed runs may retain incomplete capture and explicit null exit observations; historical records keep their original schema semantics. [Fresh remediation evidence](../../../docs/plan/framework-worker-logging/20260917T102726Z-dev-qa-fixes/context.md) binds this candidate. Independent QA retest remains separately selected; neither finding is closed here.

Rust owns the logging configuration, pipe readers, classifier, JSONL sink and evidence inspection. Select `off`, `minimal`, `verbose` or `debug` in [logging.example.json](logging.example.json). Off suppresses the optional file; mandatory byte counts, stream SHA256/EOF/error summaries, pre-stop and post-stop exit observations, and cleanup evidence remain in journal.jsonl. Minimal adds lifecycle and stream records, verbose adds timings and argument/policy digests, and debug adds bounded chunk hashes. Debug contains no arbitrary worker text. The startup classifier recognizes the observed unknown-configuration-field and MCP invalid-transport errors; other output remains unclassified.

To enable logging in a **newly prepared** request, set `schema_version` to 3 and add `diagnostics_ref` (the absolute config path) and `diagnostics_sha256` (SHA256 over its exact bytes). All other request/profile requirements still apply. Rust validates and copies this input before spawning and rechecks it at the final boundary. Logging may not select a worker, relax a guard or authorize a thread/turn. Legacy requests keep optional logging off. Review schema remains 2. The v3 launch policy fixes only the 15 quoted CLI key names; its new digest requires refreshed review bindings.

Example config:

```json
{"schema_version":1,"level":"debug","redaction_policy":"closed-v1"}
```

Build this candidate from the repository root without starting Codex:

```powershell
cargo build --offline --locked --manifest-path .\devforgeai\experiments\codex-worker-probe-logging-qa-fixes\Cargo.toml --bins
```

After independent QA and separate native authorization, the existing `preflight --request <new-schema-3-request>` interface writes diagnostics.jsonl inside that request's fresh run directory. `Get-Content -LiteralPath <run-directory>\diagnostics.jsonl -Wait` follows it from another console. The root manual-console helper still invokes the installed Codex executable directly; it does not invoke this Rust probe. Logging does not require changing the installed Codex configuration.

Stream readers have separate bounded queues (128 stdout lines, 32 optional stderr chunks), never wait on file output, and retain full-stream hashes independently of protocol consumption. Detail beyond the 64-chunk-per-stream limit is counted as dropped. Missing/incomplete summaries or changed logging artifacts are rejected by inspection for new evidence. Historical evidence remains inspectable under its original schema.

## Native identity and restrictive preflight

The [native-readiness amendment](../../../docs/specs/framework/runtime/codex-worker-native-readiness-v1.md) adds schema-v2 intake for the pinned physical 0.154.0 executable. Rust checks exactly the two recorded directory junctions, their reparse tags and targets, and the physical SHA-256. The captured schema-command fixture remains unchanged. No alias or PATH fallback is launched. The separate source-inventory exception below does not change executable admission.

Schema-v2 `profile` requires the original four fields plus string `launch_policy_id` and SHA-256 `launch_policy_sha256`; peers remain schema v1 with null profile. V1 native admission stays unchanged. The [preflight companion](../../../docs/specs/framework/runtime/codex-worker-preflight-v1.md) defines the compiled fixed launch policy, source inventory and version-2 operator review. A v2 review additionally binds `source_inventory_ref` and `source_inventory_sha256`; its file sources must exactly cover the fresh compiled inventory. Missing, changed, unreviewed reparse or unsupported sources block readiness.

The [source-identity amendment](../../../docs/specs/framework/runtime/codex-worker-source-identity-v1.md) introduces inventory schema 2 with `source_identity_sha256` and `junctions`. Rust observes exactly the compiled `chrome/latest` directory junction to `chrome/26.908.70816`, verifies its tag and target, and records it as directory membership. It reads control sources only through ordinary physical paths. Pinned Codex 0.154.0 excludes this junction from its version lookup. All other reparse paths remain rejected; source size/count limits and credential exclusions remain unchanged. Old schema-1 inventories cannot qualify a new schema-2 native review. Review/source and executable identities are checked again immediately before process creation. This does not enable plugins, qualify an effective profile, or grant filesystem mutation permission.

`profile-sources` observes applicable source identities without launching Codex. `preflight` may inspect a review with false findings, but starts no thread or turn. It checks effective configuration, requirements, features, hooks, plugins, installed apps, MCP state, and Pro/model availability, then verifies cleanup. `run` requires all four operator findings true and repeats that inspection before work. Neither operation changes operational configuration or issues framework acceptance. Native qualification still requires actual WN-01/WN-02 evidence. Current development evidence is in [the native completion run](../../../docs/plan/framework-worker-native-completion/20260915T2306060954875Z/context.md).

## Build and exercise offline

Preflight denial diagnostics use a closed `worker_event.data.diagnostic` v1 projection. It distinguishes post-spawn/post-preflight source-review rejection, initialize/config RPC failure, held-job total/active process accounting, and the first failing config-validation category (effective settings, origins or layers). Counts come from the same query used by the unchanged `total == 1 && active == 1` guard, including exited descendants. Diagnostics retain no raw config, source paths, command lines, credential material, identifiers or arbitrary server text. They cannot qualify a profile, create operator findings or authorize work. See the [diagnostic contract](../../../docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/diagnostic-contract.md) for the closed fields. Native diagnosis remains a separate selection after independent offline QA.

From this directory, using native Windows Rust 1.97.1 or later and the existing offline Cargo cache:

```powershell
cargo test --locked --offline --all-targets
cargo fmt --all -- --check
cargo clippy --locked --offline --all-targets -- -D warnings
```

The process tests use real Windows Job Objects, a hidden-console Ctrl+C driver, abrupt harness exit, and a peer descendant holding pipes. WF-16 includes the production 120-second watchdog; allow approximately 130 seconds for that test. No dependency installation is performed. The own `[workspace]` and Cargo.lock do not modify the index workspace.

For a focused `cargo test --lib` run that includes the private spawn-boundary case, first run `cargo build --locked --offline --bins` in the same target directory. That case uses the real `protocol-peer.exe` required by admission. The documented `--all-targets` campaign builds those binaries before execution.

## Terminal interface

```text
devforgeai-codex-worker-probe.exe run --request <absolute-json-path>
devforgeai-codex-worker-probe.exe preflight --request <absolute-json-path>
devforgeai-codex-worker-probe.exe profile-sources --checkout-root <absolute-fixture-path>
devforgeai-codex-worker-probe.exe inspect --run-dir <absolute-path> --after <u64> --limit <1..100>
```

The request schema, fixture bytes and profile requirements are defined in the linked contract. Only the test-built `protocol-peer.exe` beside the selected build is admitted as a peer. Peer arguments are always `--fixture-root <absolute-path>`. A native request must identify the captured Codex executable and a digest-bound operator review; the argument vector is fixed to the selected stdio adapter. No shell command input exists.

Keep harness stdin open until completion. Exact `{"op":"cancel"}` plus LF, EOF and Ctrl+C request cancellation. Invalid control input fails the run. `scenario=cancel` latches cancellation immediately after the turn ID is recorded. Library test options can shorten deadlines or inject evidence/cleanup observations; the production CLI always uses fixed limits.

The append-only `journal.jsonl` is the state record. Records are synchronized before emission or their related dispatch effect. Inspection is read-only and never spawns, resumes, repairs or kills a historical PID. Existing run directories are rejected. Preserve the referenced fixture, worker binary and profile artifacts for complete inspection. A stopped tree does not establish file/network isolation.

Exit codes: 0 completed with exact result, unchanged fixture, verified stopped tree and observed zero worker exit; 2 invalid request/path/identity; 3 unavailable prerequisite/profile; 4 worker/protocol/output/evidence failure; 5 cancellation; 6 deadline; 7 cleanup uncertain. Preflight exit 0 has the distinct `preflight_checked` outcome, null thread/turn and `oracle:not_evaluated`. Source collection exit 0 emits only an inventory. Sound inspection exits 0 independently of the recorded historical outcome.

## Evidence and fixture ownership

Frozen fixture copies in `tests/fixtures` originate from the selected specification and captured schema-command receipt. Expected results are compiled into the verifier and external peer, and never copied into the worker fixture or prompt. The peer validates outgoing protocol fields independently of runtime predicates. Additional numbered peer subfixtures in the tests cover typed events, RPC errors, pagination and invalid data; they do not inflate the 20-case denominator.

Developer execution evidence is retained under [the implementation run](../../../docs/plan/framework-worker-implementation/20260915T1544548240203Z/context.md). Final metrics, limitations and independent retest selection are in that run's delivery report when present. A passing peer does not qualify native Codex, supported production dispatch, protected authority or the full MVP.
