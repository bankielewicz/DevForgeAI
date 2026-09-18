# Human-operated Git and Rust console

Run the root [DevForgeAI-Console.ps1](../../DevForgeAI-Console.ps1) with native
Windows **PowerShell 5.1 or PowerShell 7.2 or later**. It runs in the selected
host directly; PowerShell 5.1 does not need to launch or install PowerShell 7:

```powershell
Set-Location C:\Projects\DevForgeAI
.\DevForgeAI-Console.ps1
```

The script loads its companion [module](../../scripts/operator-console/OperatorConsole.psm1).
Keep both files together in their repository layout. To operate another checkout,
pass `-RepositoryPath` with that checkout's root. The menu always displays the
selected root, branch and HEAD; check them before choosing an action. It does not
change your parent console's directory. Stop editors, agents and other Git writers
for that checkout before mutating it.

## Menu

Choices appear on separate aligned lines, grouped into Repository, Safety and
recovery, Branches and delivery, and Build Rust CLI. Blank lines separate groups;
option numbers retain their original actions. The header puts root, branch and
HEAD on separate lines. Plain text remains readable without color or ANSI support.

| Option | Operation | Safety behavior |
| --- | --- | --- |
| 1 | Status, branches and registered worktrees | Read-only. |
| 2 | Fetch origin | Updates remote references; leaves local branches and working files alone. |
| 3 | Create safety checkpoint | Preserves HEAD, staged content and changed/untracked files. Does not make the checkout clean. |
| 4 | Switch to main and fast-forward | Requires a clean checkout, available main and safe ancestry; creates a checkpoint first. |
| 5 | Switch existing local branch | Clean checkout and checkpoint required; no remote-branch guessing. |
| 6 | Create task branch/worktree | Fetches main; creates a unique directory under the primary checkout's `worktrees/git/`. Leaves the current checkout alone. |
| 7 | Commit staged files | Task branch only; checkpoint first. Does not stage files for you. |
| 8 | Push task branch | Clean task branch only, explicit same-name origin destination; never force-pushes or pushes main. |
| 9 | List pull requests | Requires authenticated GitHub CLI (`gh`); read-only. |
| 10 | Open draft PR | Clean task branch; push first. Uses main as base and commit messages for initial PR text; review/edit that text on GitHub. |
| 11 | List recovery checkpoints | Lists locations and whether each capture completed; does not restore automatically. |
| 12 / 13 | Compile CLI, debug / release | Locked Cargo build; offline by default, with a separate download choice. |
| 0 | Exit | Leaves all worktrees, branches and checkpoints in place. |

Changes require typing `yes` (any capitalization; surrounding spaces are ignored).
Enter, `no`, abbreviations such as `y`, and other text cancel. Successful actions
print `Completed: <action>.`, even when the underlying command returns no text.
Failed actions print `STOPPED:` and do not print a completion message.
Noninteractive actions require `-Approve` instead:

```powershell
.\DevForgeAI-Console.ps1 -Action Status
.\DevForgeAI-Console.ps1 -Action SyncMain -Approve
.\DevForgeAI-Console.ps1 -Action BuildDebug -Approve
```

For branch actions use `-Branch 'feat/my-task'`; for commits use
`-Message 'Describe the change'`. Stage only reviewed, explicit paths with
`git --literal-pathspecs add -- <path>` before choosing commit. Creating a new
worktree does not transfer uncommitted files into it. Existing worktrees, local
archives and checkpoints are never automatically deleted.

If a fast-forward or branch switch updates the console's files while its menu is
running, choose `0` and launch the script again to load the updated module. The
running menu keeps its already loaded code; a changed HEAD does not reload it.

## What makes updating main safe

Option 4 performs a guarded fetch and fast-forward merge instead of issuing a
bare `git pull --ff-only origin main` on whichever branch happens to be current.
It fetches origin/main, pins the fetched commit, verifies local main has no
commits absent from that target, switches to main, and merges that pinned commit
with `--ff-only --no-autostash --no-overwrite-ignore`. Switching also uses
`--no-overwrite-ignore`. This prevents Git's usual overwrite of ignored files
when a tracked path would replace them.

Dirty staged/unstaged/untracked work, operation locks, unresolved Git operations,
submodules, hidden index flags, main in another worktree, and ahead/divergent main
stop the operation. Preserve/commit your work or resolve the reported condition
explicitly, then retry. Fetch or merge failure is not automatically rolled back:
inspect option 1 and the checkpoint before continuing. The checkout might already
have switched to main when a later merge fails; the original task branch remains.

## Recovery and limits

Checkpoints live under the Git **common directory**, `operator-safety/<unique-id>/`.
This is normally `C:\Projects\DevForgeAI\.git\operator-safety`, shared by its
worktrees. Each completed `checkpoint.json` records:

- `HeadRef`: a durable local Git reference to the original committed state.
- `IndexRef`: a synthetic commit containing the staged tree, including partial staging.
- `Files`: raw changed/untracked file copies, SHA256 hashes and deletion records.
- Original branch, HEAD and local main; a separate recovery ref retains main too.

Recovery refs use `refs/operator-safety/`; ordinary task-branch push does not send
them or checkpoint files to GitHub. A directory without `checkpoint.json` is an
**incomplete capture**, retained for diagnosis. Checkpoint capture has a 1 GiB
changed/untracked-byte limit; exceeding it stops the dependent operation.

Recover into a **new** branch and directory, leaving your current checkout intact.
Copy the actual `HeadRef` or `IndexRef` from a completed manifest and substitute
unused names/paths in this example:

```powershell
git worktree add -b recovery/my-task C:\Projects\DevForgeAI\worktrees\git\recovery-my-task refs/operator-safety/REPLACE-ID/head
```

Use `index` instead of `head` to start from staged content. Inspect `Files`, verify
copy hashes against the manifest, and apply only the wanted copies/deletions to
that recovery checkout. Keep the checkpoint unchanged until recovery is reviewed.
The helper deliberately has no destructive restore, stash-pop, reset, clean,
branch deletion, automatic merge or force-push option.

This is a local recovery aid, not a complete backup: **ignored files are not
copied**. They receive Git overwrite protection during switches/updates. Keep an
external backup for ignored archives, disk failure or loss of the repository.
Checkpoint copies may contain sensitive local changes; protect them like the
checkout. Concurrent writers and custom Git hooks/build scripts can have effects
outside this helper's checks. Reparse points on captured paths are refused.

## Rust build

The selected checkout must contain `devforgeai/Cargo.toml` and `Cargo.lock`, with
the `devforgeai` binary target. Cargo metadata supplies the package name. The
helper builds that binary with `--locked`, a checkout-local `devforgeai/target`
directory, and `--offline` unless downloads were explicitly allowed. Use
`-AllowNetwork` for that permission in noninteractive mode. Install the project's
Rust/MSVC prerequisites separately if unavailable; this script installs nothing.

Compiler output is visible. Each attempted compilation retains an
`operator-build-<id>.json` receipt under `devforgeai/target`, including arguments,
output, exit code and lockfile integrity. Outputs are
`devforgeai/target/debug/devforgeai.exe` or `release/devforgeai.exe`. A nonzero
compiler exit remains failure even if an older executable exists.

This compiles the CLI; it does not launch it, native Codex, the daemon or tray.
The script is an operator convenience, not a protected framework gate or an
acceptance authority. Follow [worktree/PR delivery](worktree-and-pr-delivery.md)
and the selected implementation/QA contracts separately.

## Developer checks

The [Pester suite](../../tests/operator-console/OperatorConsole.Tests.ps1) uses
disposable local bare remotes and worktrees, actual Git operations and tiny Rust
build fixtures. The [compatibility suite](../../tests/operator-console/Compatibility.Tests.ps1)
also checks public-host startup, literal native arguments, separate output streams,
exit codes and menu layout. Its argument echo fixture uses Python 3; Python is not
a console runtime dependency. GitHub and interactive prompts are tested at their command/input
boundaries; tests do not publish PRs. Pester 5.7.1 and PSScriptAnalyzer 1.25.0 were
available on the development host; neither is needed to use the console.

Run Pester from the task root. For coverage include **both production files**:
`DevForgeAI-Console.ps1` and `scripts/operator-console/OperatorConsole.psm1`.
Exclude only tests and third-party tooling. Retain test results and coverage in a
fresh local evidence directory. Report executable-line coverage separately from
Pester command coverage, and do not equate these checks or a build with independent
QA or framework acceptance.

For example (use a fresh output directory for each run):

```powershell
Import-Module Pester -MinimumVersion 5.7.1
$run = Join-Path 'tmp' ('operator-check-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $run | Out-Null
$config = New-PesterConfiguration
$config.Run.Path = 'tests/operator-console'
$config.Run.PassThru = $true
$config.TestResult.Enabled = $true
$config.TestResult.OutputPath = Join-Path $run 'tests.xml'
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = @('DevForgeAI-Console.ps1', 'scripts/operator-console/OperatorConsole.psm1')
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = Join-Path $run 'coverage.xml'
$config.CodeCoverage.CoveragePercentTarget = 95
$result = Invoke-Pester -Configuration $config
if ($result.Result -ne 'Passed') { throw 'Checks failed; inspect retained reports.' }
```

Run the suite independently in `powershell.exe` (5.1) and `pwsh.exe` (7), recording
`$PSVersionTable.PSVersion` in each result. If Pester 5 is installed outside the
host's module search path, import its existing absolute manifest path; Pester 3
bundled with Windows PowerShell cannot run this suite. No installation is performed
by the console or its tests.

Pester's test isolation needs access to the user's temporary directory and test
registry; a restrictive sandbox may block that setup. Treat such a failure as a
blocked test run, not as a reproduced product defect. Use the entry script for
normal operations: it owns the approval prompt/`-Approve` contract. Its module
functions do not implement `-WhatIf` or a second layer of `-Confirm` prompts.
