# Operator console: PowerShell compatibility and menu layout

Selected scope: Bryan requested native Windows PowerShell 5.1 and PowerShell 7
support, plus a readable, professionally spaced menu. Existing Git safety and
build behavior remain the regression contract. This is an operator convenience,
not a protected framework authority implementation.

Candidate worktree: `C:\Projects\DevForgeAI\worktrees\git\operator-console-compatibility`.
Branch: `fix/operator-console-compatibility`.
Base: `317b193eacdb9cb9602a726bbfa74f2854516f1c` (`origin/main` at preflight).
The [manifest](manifest.json) binds changed source/tests, this report and local
execution evidence. Prior verification records remain unchanged.

## Changes

- The entry requires PowerShell 5.1 and runs in the invoking host without relaunch
  or installation. Removed reliance on `ProcessStartInfo.ArgumentList`; the shared
  Windows native argument encoder preserves empty arguments, spaces, quotes,
  backslashes, Unicode and shell metacharacters without invoking a shell.
- Select the first executable on PATH rather than concatenating multiple matches.
  Use the process environment API shared by both runtimes.
- Select the explicit `String.Split(char[], options)` overload: on .NET Framework,
  the earlier scalar-char call admitted an empty Git path into checkpoint capture.
- Preserve streamed compiler diagnostics and actual exit-code handling on 5.1,
  where redirected native stderr becomes PowerShell ErrorRecords. Restore the
  caller's error preference after the build.
- Render one aligned option per line, with blank lines and named groups. Root,
  branch and HEAD occupy separate lines. Existing option numbers and confirmation
  behavior remain unchanged; color is supplementary to readable plain text.
- Make the existing tests run in both hosts: explicit native-stderr handling,
  current-host child invocation, portable binary comparison, and UTF-8 BOM for the
  test file containing literal Japanese filenames. Assertions were not weakened.

## Final results

| Host | Required cases | Executed lines | Commands | Exit |
| --- | ---: | ---: | ---: | ---: |
| Windows PowerShell 5.1.26100.9444 | 32/32 (100%) | 276/278 (99.280575%) | 502/515 (97.475728%) | 0 |
| PowerShell 7.6.6 | 32/32 (100%) | 276/278 (99.280575%) | 502/515 (97.475728%) | 0 |
| Host-case total | 64/64 (100%) | 552/556 host-lines (99.280575%) | 1004/1030 host-commands (97.475728%) | 0 |

No required case was failed, skipped, blocked or unexecuted in the final campaigns.
The denominator is both complete production files: `DevForgeAI-Console.ps1` and
`scripts/operator-console/OperatorConsole.psm1`. No first-party executable behavior
is excluded. Tests/fixtures and third-party tooling are outside the denominator.
The two uncovered entry lines are error reporting/exit paths exercised in child
processes but not counted by in-process coverage. Branch coverage is NOT_MEASURED;
one covered line does not prove every conditional on it executed. The aggregate
does not replace either host's independent result.

Tests use real disposable Git repositories, local bare remotes and worktrees.
They cover dirty-state and unsafe-operation refusals, recovery content, ignored
collisions, branch availability, native argument round-trips, command failure,
and real Rust debug/release fixture compilation including a compiler failure with
a stale executable. GitHub and menu prompts remain bounded test doubles; tests
do not publish PRs. Public startup/status and unapproved-mutation exit behavior
execute through the actual selected host. Additional menu-and-exit smoke runs
against the primary checkout returned 0 on both hosts; plain-text captures were
reviewed. Native GUI rendering was not assessed.

PSScriptAnalyzer 1.25.0: **0 errors, 40 warnings, 17 informational findings**.
Warnings are 37 intentional `Write-Host` menu/output uses and three existing
ShouldProcess recommendations; the entry's explicit approval contract owns
confirmation. Findings remain recorded without suppression. The entry was analyzed
in PowerShell 7 and the module in 5.1 after the 7-host analyzer raised an internal
null-reference error and hung. This is a completed alternate-host static scan,
not a successful PowerShell 7 module scan.

## Retained red and intermediate runs

Raw records are under `tmp/console-compatibility-001/` in this worktree:

1. `red-ps7`: 1/3 focused cases passed; reproduced cramped menu and multiple-PATH
   executable selection failure. `red-ps51` also actually ran in 7.6.6 because the
   tool shell setting resolved there; its saved host identity is authoritative.
2. `red-native51`: explicitly invoked `powershell.exe`; 0/3 focused cases passed,
   reproducing the entry version refusal and missing ArgumentList API.
3. `green-native7`: 32/32 passed on the initial repaired source. `green-native51`
   exposed test harness stderr/JSON compatibility failures; it is not counted as
   successful product qualification.
4. `regression-native51-002`: after harness repair, reproduced the .NET Framework
   empty-path checkpoint defect. Fixed the overload, retaining all failed reports.
5. `final-native51` and `final-native7`: complete final campaigns above, after
   extracting the shared argument encoder and resolving the compatibility defects.
6. First redirected menu smoke expected a captured `Read-Host` prompt; 5.1 omits
   that prompt when input is redirected. Its transcript is retained. Revised
   observation checked successful exit and actual rendered menu content; both
   `menu-*-002.txt` transcripts passed. No mutation was attempted by these smokes.

Earlier attempts do not inflate the final denominator or disappear from evidence.
Two PowerShell 7 static-analysis attempts failed internally and were stopped;
the successful module findings are `static-module-native51.json`, entry findings
are `static-entry.json`.

## Reproduction and handoff

Native host tools: Git 2.53.0.windows.3, Cargo 1.97.1, Python 3.10.11,
Pester 5.7.1, PSScriptAnalyzer 1.25.0. Python is used only by the native-argument
test fixture; it is not needed to run the console. No tools were installed.
The runner imports the existing Pester 5 manifest by absolute path, uses both
test files, and records JaCoCo coverage for both production files.

Final commands from the candidate root (each exit 0):

```powershell
& 'C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe' -NoProfile -File .\tmp\run-console-checks.ps1 -RunName final-native51
& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoProfile -File .\tmp\run-console-checks.ps1 -RunName final-native7
```

Use a new run name for any retest; the runner refuses an existing directory.
The [operator guide](../../../workflows/operator-console.md) includes the portable
Pester configuration so another checkout can run the suite without this local
runner. Required test/coverage outputs, runner bytes and menu transcripts are
hash-bound by the manifest and remain local-only; Bryan can arrange reviewer
access. Preserve this worktree while that evidence remains needed. No raw evidence
bundle or executable is uploaded in the PR.

The primary checkout remained clean at the base commit. Source changes are confined
to this task worktree; unrelated worktrees, operational copies and prior evidence
were preserved. No real repository mutation was performed through the revised menu.
Real Git mutations and compilations ran only on disposable fixtures. The framework
application itself was not rebuilt or launched for this compatibility change.

Developer verification is complete for the selected hosts. Independent QA is
NOT_RUN; framework acceptance is NOT_EVALUATED. The draft PR is for Bryan's review;
no automatic merge or installation is included. After merge and fast-forwarding
the primary checkout, run `.\DevForgeAI-Console.ps1` directly in either host.
