# Operator console developer verification

Candidate: `feat/operator-console`, rooted at
`C:\Projects\DevForgeAI\worktrees\git\operator-console`.
Base: `164b652572cbb349e2c44eb3270f4d653bac05e5` (also origin/main at delivery preflight).
The [manifest](manifest.json) binds candidate files, retained reports and the built
binary. These are developer checks; independent QA is NOT_RUN and framework
acceptance is NOT_EVALUATED. No installation or native Codex launch was performed.

## Outcome

- Required cases: **29/29 passed (100%)**, no skipped, blocked or unexecuted cases
  in the final Windows campaign. [Raw results](tests.xml).
- Executed-line coverage: **245/247 (99.190283%)** across both production files,
  as reported by Pester's JaCoCo line counters. [Raw coverage](coverage.xml).
- Command coverage: **462/475 (97.263157%)**. Line coverage counts a line as
  covered when an instrumented command on it executes; it is not proof every
  condition/throw on that line ran. Branch coverage is NOT_MEASURED by this collector.
- Root entry: 4/6 executable lines; module: 241/241. No first-party executable
  source excluded. Tests, build fixtures and third-party tooling are outside this
  denominator. Child-process entry failure is tested but outside in-process coverage.
- Actual framework CLI debug build: exit **0**, offline and locked, with unchanged
  Cargo.lock. [Build receipt](rust-build.json). Release mode was exercised on a
  real tiny Rust fixture; a framework release build was NOT_RUN.
- Static analysis: **0 errors, 13 reviewed warnings, 17 informational findings**.
  [Findings](static-analysis.json). Ten warnings concern intentional `Write-Host`
  console output; three concern absence of `ShouldProcess`. The entry script's
  explicit menu/`-Approve` contract owns confirmation. Informational findings
  concern internal module help and positional internal calls. These are retained,
  not silently suppressed or reported as a zero-warning scan.

Coverage qualifies this PowerShell change only. It does not qualify the unchanged
Rust application's tests, coverage or runtime behavior.

## Red, green and regression history

1. Initial Pester isolation was blocked by sandbox registry/CIM permissions.
   Retained locally as `tmp/operator-console-evidence/red.xml`; not product red.
2. The focused [red test](red.xml) reproduced the absent main synchronization
   behavior (1 failed case). Implemented checkpoint + guarded switch/fast-forward;
   focused green passed 1/1 (`green-focused.xml` in the local evidence directory).
3. Expanded suite discovery initially exposed an extra test-file brace; next run
   exposed a test mock scope error. Both were fixed; original attempts remain local
   (`integration-001.xml`, `integration-002.xml`). No passing result is inferred
   from the earlier discovery failure's shell exit code.
4. [Safety regression red](safety-regression-red.xml): 26 passed, 3 failed. Hidden
   index flags and a same-commit concurrent branch switch were wrongly admitted.
   Added flag rejection and branch-identity verification; renamed the build profile
   variable to avoid shadowing PowerShell's automatic `$PROFILE` variable.
5. Final full regression/coverage campaign: 29/29, results above. Earlier attempts
   are not added to the final denominator or erased. No mandatory failure remains.

The suite exercises actual local Git remotes/worktrees, staged-versus-working
bytes, binary/Unicode files, deletions, dirty-state refusal, branch availability,
divergence, ignored-file collision, detached recovery, failed fetch, hidden flags,
concurrent mutation, submodules, operation markers, junction refusal, checkpoint
size failure, commit/push boundaries and real successful/failed Rust builds.
Mocks are limited to deterministic concurrency injection, menu input/action
routing and the GitHub CLI boundary; no GitHub PR is created by tests.

## Commands and environment

Native Windows, PowerShell 7.6.6, Git 2.53.0.windows.3,
Cargo 1.97.1 (`c980f4866`, 2026-06-30), rustc 1.97.1
(`8bab26f4f`, 2026-07-14), Pester 5.7.1, PSScriptAnalyzer 1.25.0.
All commands ran at the candidate root above. Pester needed normal host access
to its disposable test registry/temp directory. No tool installation was performed.

Final Pester command (exit 0):

```powershell
Import-Module Pester -MinimumVersion 5.7.1
$config = New-PesterConfiguration
$config.Run.Path = 'tests/operator-console/OperatorConsole.Tests.ps1'
$config.Run.PassThru = $true
$config.Output.Verbosity = 'Normal'
$config.TestResult.Enabled = $true
$config.TestResult.OutputPath = 'tmp/operator-console-evidence/integration-004.xml'
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = @('DevForgeAI-Console.ps1','scripts/operator-console/OperatorConsole.psm1')
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = 'tmp/operator-console-evidence/coverage-001.xml'
$config.CodeCoverage.CoveragePercentTarget = 95
$result = Invoke-Pester -Configuration $config
$result.CodeCoverage | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath tmp/operator-console-evidence/coverage-001-detail.json
if ($result.Result -ne 'Passed') { exit 1 }
```

Static analysis was rerun in separate invocations for each production path after
an earlier batched invocation encountered a dynamic-assembly tool error. Final
invocations used `Invoke-ScriptAnalyzer -Path <production-path>` with all default
rules, exit 0. The complete returned findings are summarized without exclusions
in `static-analysis.json`; original objects remain under local evidence.

Build invocation (exit 0):

```powershell
& .\DevForgeAI-Console.ps1 -Action BuildDebug -Approve
```

Cargo compiled package `devforgeai-index` / bin `devforgeai` in 14.88 seconds
(Cargo-reported). The receipt contains the exact build arguments and output.
Rust source tree identity: `1705f2a5c414e1b75972c2f10f09ed928be7fe0f`.
`git diff --exit-code -- devforgeai` passed; no Rust source/lockfile edit was made.

Binary: `devforgeai/target/debug/devforgeai.exe`.
SHA256: `1c3d8e299512d1e4844179100c956313c1f57603696d95a44d45d1a939424987`.
Cargo.lock SHA256: `f8557a6d5fa164f171177f217ddf527d49de01791829f58b2effafe5eebe206e`.
The binary stays local, is not installed, and was not executed.

## Handoff

Use the [operator guide](../../../workflows/operator-console.md) for invocation,
menu choices, recovery and limits. Existing primary checkout and unrelated
worktrees remain in place. Checkpoints are local recovery aids, not backups of
ignored archives or protection against concurrent external writers/disk failure.
The PR is a draft for review; merging is a separate operator decision.
