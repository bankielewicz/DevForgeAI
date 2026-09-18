# Effective-profile coverage remediation context

Selected evidence value: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev\effective-dev`.

Selection source: the root QA-F-COV-01 development context assigned this disjoint `effective-dev` evidence subdirectory and ownership of only `devforgeai/experiments/codex-worker-probe/tests/effective_profile_edges.rs`. The resolved path is identical to the selected value. The package is `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe` on native Windows x64. Git metadata is absent.

This bounded slice adds meaningful contract-derived integration tests for existing effective-profile validation. It does not alter production source, existing tests, specifications, operational copies, coverage exclusions, thresholds, launch policy, native configuration, or native trial state. A characterization test may pass on its first execution because QA-F-COV-01 is a metric failure rather than an established functional defect. Any observed functional defect must remain a valid Red and be reported to the root owner before production repair.

## Bound inputs

- `AGENTS.md`: SHA-256 `d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7` (bound by the failed QA report and reread for this slice).
- DFF-WORKER-FEAS-01: SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`.
- DFF-WORKER-NATIVE-01: SHA-256 `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`.
- DFF-WORKER-PREFLIGHT-01: SHA-256 `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`.
- Failed candidate manifest: 48 files, manifest SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`.
- Historical raw coverage: `08a-coverage/coverage.json`, SHA-256 `271212ab24ab2939f4a595103c9978c2d451dc826fecfe341da06d5d4c3dc3b8`; it reported `src/effective_profile.rs` at 485/573 executed lines. It guides risk selection only and cannot qualify the changed candidate.
- `src/effective_profile.rs`: SHA-256 `33edc40ceb050be3ce0195de0c5ca7176475b2b0d14d8b730fe0ebe41872302c` before this slice.
- Existing `tests/effective_profile.rs`: SHA-256 `90676312ab3b73af79760bedd5337b05af72f85a231dc8bc306c20d4f9119d52` before this slice.
- `Cargo.toml`: SHA-256 `8f4dae9ae80b5189b26f4973cf5a008004bca7b7473336bbe97ad93814f20a50`.
- `Cargo.lock`: SHA-256 `b8932b591aa403a916c78d324964e52e2849444ebb4826c87653f40558f15b84`.
- `tests/effective_profile_edges.rs` was absent before this slice.

## Tools and commands

Observed tools: Cargo 1.97.1, rustc 1.97.1 (`x86_64-pc-windows-msvc`, LLVM 22.1.6), rustfmt 1.9.0-stable and Clippy 0.1.97. Commands use exact `C:\Users\bryan\.cargo\bin\cargo.exe`, `--locked --offline`, a slice-owned `CARGO_TARGET_DIR`, and the package cwd. The copied root recorder retains exact argv, cwd, environment overrides, executable hash, raw stdout/stderr, exit, timing and before/after package manifests. Full regression and coverage remain root-owned.

One setup attempt used unsupported `New-Item -LiteralPath` and created nothing. The subsequent literal constant `New-Item -Path` created only this evidence directory. No Cargo or product process ran in either setup attempt.

## Output mapping

- Context and declared cases: `context.md`, `case-map.md`.
- Recorder copy: `record.py`.
- Focused execution attempts: one fresh child directory per label with raw streams and receipts.
- Slice delivery/readback: `delivery.md`, `changed-files.json`.

Framework acceptance remains `NOT_EVALUATED`. Native Codex execution and coverage collection are outside this slice.
