# NI-T07 fixed launch-policy development context

- Selected evidence value: `docs/plan/framework-worker-native-completion/20260915T2306060954875Z`
- Selection source: parent development assignment for the remaining native-readiness criteria.
- Resolved child evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\policy-dev`
- Candidate package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`
- Owned source scope: `src/launch_policy.rs`, `src/restrictive-launch-policy.json`, `tests/launch_policy.rs`, and the `pub mod launch_policy;` export in `src/lib.rs` requested during implementation.
- Requirement: compile a closed schema-version-1 native launch policy for adapter `codex-0.154.0-stdio`, bind callers to its final ID and SHA-256, return only the fixed argument vector, and expose every selected required-disabled feature name.
- Final policy ID: `codex-0.154.0-readonly-no-external-tools-v2`.
- Source argv: retained proposed policy at `docs/plan/framework-worker-native-implementation/20260915T2118427272409Z/restrictive-launch-policy.next-proposed.json`; proposal-only metadata is excluded from the compiled record. The selected companion amendment appends fixed `sandbox_mode=\"read-only\"` and `approval_policy=\"never\"` values supported by the pinned ConfigRead schema.
- Feature extension source: pinned baseline feature output `docs/plan/framework-worker-native-implementation/20260915T2118427272409Z/profile-research/14-features-baseline/stdout.txt`, SHA-256 `10e096f2fdf3dd3546065097bb3eadccb1336d91160586fb4a5b0a6eeb577ec9`. The final vector preserves the original fourteen names, then appends twenty-one selected enabled effect-capable names in lexical order before the two bootstrap settings.
- TDD boundary: execute an integration test first, where the intentionally missing public module is the expected contract failure; then implement only the selected module and compiled record. The parent owns `src/lib.rs` export/integration.
- Exclusions: no app-server/Codex launch, profile/review changes, configuration writes, native trials, full-suite qualification, coverage, or protected acceptance.
- Evidence capture: each attempt retains exact argv/cwd, start/end/duration, native exit code, raw stdout/stderr, executable digest, and package manifest at attempt start.
