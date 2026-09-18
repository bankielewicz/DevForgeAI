# Independent QA preparation context

- Invocation intent: `run`, preparation phase while development is still changing the candidate.
- Plan readiness: `READY` for frozen-candidate integrity inspection and offline execution. Live preflight and NI-T11/NI-T12 remain dependency-blocked until their preceding checks pass.
- Execution status: `IN_PROGRESS`.
- Selected component: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Required host: native Windows x64 in `C:\Projects\DevForgeAI`; WSL/Linux is outside the selected platform.
- Evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z`.
- Selection source: parent QA assignment in the current Codex session.
- Candidate status: frozen by development under `docs/plan/framework-worker-native-completion/20260915T2306060954875Z`. Candidate manifest SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`, 48 entries; input manifest SHA-256 `3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288`. A same-size candidate snapshot is present and will be independently read back.
- Authority boundary: this QA run cannot issue protected framework acceptance. Framework acceptance remains `NOT_EVALUATED`.

## Selected specifications

| Path | SHA-256 observed during preparation |
| --- | --- |
| `docs/specs/framework/runtime/codex-worker-feasibility-v1.md` | `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23` |
| `docs/specs/framework/runtime/codex-worker-native-readiness-v1.md` | `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d` |
| `docs/specs/framework/runtime/codex-worker-preflight-v1.md` | `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1` |
| `AGENTS.md` | `d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7` |

These identities are the selected frozen inputs and will be rechecked before and after each execution attempt. Any drift stops affected work.

## Environment observed during preparation

- OS API description: `Microsoft Windows 10.0.26200`; architecture `X64`; 64-bit process.
- Shell: PowerShell `7.6.6`.
- Working directory: `C:\Projects\DevForgeAI`.
- Cargo `1.97.1`; rustc `1.97.1` (`x86_64-pc-windows-msvc`, LLVM `22.1.6`).
- rustfmt `1.9.0-stable`; Clippy `0.1.97`; cargo-llvm-cov `0.8.4`; Python `3.10.11`.
- Git metadata: absent according to the repository instructions; the frozen candidate must therefore use a complete scoped SHA-256 manifest.
- Filesystem query through `Get-Volume` was denied during preparation. The final environment receipt will use a non-privileged drive API and will not infer a filesystem result from this error.

## Effects and ownership

QA may create only fresh evidence, isolated fixtures, build outputs, and QA helpers under this evidence root. Product source, developer tests, selected specifications, operational configuration, Codex configuration, credential stores, startup settings, and historical evidence remain preserved. The two native trials have zero automatic retries. No actual Codex process may start until the frozen offline QA campaign and live preflight prerequisites pass.
