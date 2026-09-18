# Closed review-v2 development context

- Selected evidence value: `docs/plan/framework-worker-native-completion/20260915T2306060954875Z`.
- Resolved child evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\review-dev`.
- Selected contract: `docs/specs/framework/runtime/codex-worker-preflight-v1.md`, DFF-WORKER-PREFLIGHT-01 v0.1.0.
- Candidate package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Owned production scope: the review parsing and verification portion of `src/request.rs`; owned test scope: `tests/support/review_v2_cases.rs` and its cfg(test) module link.
- Required behavior: preserve review v1; add a closed v2 record with exact request/compiled-policy/model/effort/source-inventory bindings; allow false findings only for preflight; require all findings for run; verify inventory freshness from fixed production roots; require exact profile-source coverage; return the covered file paths.
- Production source inventory API: `profile_sources::Inventory::{verify,fixture_cwd,file_bindings,file_paths}`. Any collector override is private and cfg(test)-only; production always invokes fixed-root verification.
- Exclusions: no request schema/layout changes, runner/main/protocol edits, Codex launch, configuration changes, trial execution, or protected acceptance.
- Evidence capture: every attempt records exact argv/cwd, UTC times/duration, native exit, raw stdout/stderr, executable digest, and package manifest.

