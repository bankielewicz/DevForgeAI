Set-StrictMode -Version Latest

function Invoke-OperatorTool {
    param([string]$Directory, [string]$Program, [string[]]$Arguments, [switch]$AllowFailure)
    $executable = (Get-Command $Program -CommandType Application -ErrorAction Stop).Source
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $executable
    $start.WorkingDirectory = $Directory
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.StandardOutputEncoding = [Text.UTF8Encoding]::new($false)
    $start.StandardErrorEncoding = [Text.UTF8Encoding]::new($false)
    $start.Environment['GIT_TERMINAL_PROMPT'] = '0'
    foreach ($argument in $Arguments) { $start.ArgumentList.Add($argument) }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        $null = $process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        $result = [pscustomobject]@{ ExitCode = $process.ExitCode; Output = $stdout.GetAwaiter().GetResult(); Error = $stderr.GetAwaiter().GetResult() }
        if ($result.ExitCode -ne 0 -and -not $AllowFailure) {
            throw "$Program failed (exit $($result.ExitCode)): $($result.Error)$($result.Output)"
        }
        return $result
    }
    finally { $process.Dispose() }
}

function Get-OperatorGit {
    param([string]$Root, [string[]]$Arguments)
    (Invoke-OperatorTool $Root git $Arguments).Output.TrimEnd([char[]]"`r`n")
}

function Confirm-PlainPath {
    param([string]$Path)
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse points are not supported here: $current" }
        }
        $current = [IO.Path]::GetDirectoryName($current)
    }
}

function Get-OperatorRepository {
    param([string]$RepositoryPath)
    $selected = (Resolve-Path -LiteralPath $RepositoryPath -ErrorAction Stop).Path
    Confirm-PlainPath $selected
    $root = Get-OperatorGit $selected @('rev-parse', '--show-toplevel')
    if ([IO.Path]::GetFullPath($root) -ne [IO.Path]::GetFullPath($selected)) { throw 'Select the repository/worktree root, not a subdirectory.' }
    $common = Get-OperatorGit $root @('rev-parse', '--path-format=absolute', '--git-common-dir')
    Confirm-PlainPath $common
    [pscustomobject]@{
        Root = [IO.Path]::GetFullPath($root)
        GitDirectory = Get-OperatorGit $root @('rev-parse', '--absolute-git-dir')
        CommonDirectory = $common
        Head = Get-OperatorGit $root @('rev-parse', '--verify', 'HEAD')
        Branch = Get-OperatorGit $root @('branch', '--show-current')
    }
}

function Confirm-OperatorReady {
    param($Repository, [switch]$Clean)
    foreach ($marker in @('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'BISECT_LOG', 'index.lock')) {
        if (Test-Path -LiteralPath (Join-Path $Repository.GitDirectory $marker)) { throw "Git operation/lock in progress: $marker. Resolve it manually first." }
    }
    if ((Get-OperatorGit $Repository.Root @('ls-files', '--stage')) -match '(?m)^160000 ') { throw 'Submodule checkouts are not supported for mutations by this helper.' }
    if ((Get-OperatorGit $Repository.Root @('ls-files', '-v')) -cmatch '(?m)^[a-zS] ') { throw 'Hidden index flags (assume-unchanged or skip-worktree) are unsupported. Review them manually first.' }
    if ($Clean -and (Get-OperatorGit $Repository.Root @('status', '--porcelain=v1', '--untracked-files=all', '--ignore-submodules=none'))) {
        throw 'Working tree/index is not clean. Preserve and commit your changes first. No automatic stash, reset or clean is performed.'
    }
}

function Confirm-BranchName {
    param([string]$Root, [string]$Branch)
    if (-not $Branch -or $Branch.StartsWith('-') -or $Branch -eq 'HEAD') { throw 'Supply a literal local branch name.' }
    $null = Get-OperatorGit $Root @('check-ref-format', '--branch', $Branch)
}

function Get-OperatorRef {
    param([string]$Root, [string]$Reference)
    $result = Invoke-OperatorTool $Root git @('rev-parse', '--verify', '--quiet', "$Reference^{commit}") -AllowFailure
    if ($result.ExitCode -eq 0) { return $result.Output.Trim() }
    if ($result.ExitCode -ne 1) { throw "Cannot inspect Git reference: $($result.Error)" }
    return $null
}

function Confirm-BranchAvailable {
    param($Repository, [string]$Branch)
    $listing = Get-OperatorGit $Repository.Root @('worktree', 'list', '--porcelain', '-z')
    foreach ($block in ($listing -split "`0`0")) {
        $fields = $block -split "`0"
        if ($fields -contains "branch refs/heads/$Branch") {
            $path = ($fields | Where-Object { $_.StartsWith('worktree ') } | Select-Object -First 1).Substring(9)
            if ([IO.Path]::GetFullPath($path) -ne $Repository.Root) { throw "Branch '$Branch' is in another worktree: $path. Run the helper there; it will not force-switch it." }
        }
    }
}

function New-OperatorCheckpoint {
    param([string]$RepositoryPath, [long]$MaxBytes = 1073741824)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-OperatorReady $repo
    $id = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [guid]::NewGuid().ToString('N')
    $folder = Join-Path $repo.CommonDirectory "operator-safety/$id"
    Confirm-PlainPath $folder
    $null = New-Item -ItemType Directory -Path $folder -ErrorAction Stop
    try {
        $status = Get-OperatorGit $repo.Root @('status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=none')
        $indexTree = Get-OperatorGit $repo.Root @('write-tree')
        $paths = @(
            (Get-OperatorGit $repo.Root @('diff', '--name-only', '--no-renames', '-z')).Split([char]0, [StringSplitOptions]::RemoveEmptyEntries)
            (Get-OperatorGit $repo.Root @('diff', '--cached', '--name-only', '--no-renames', '-z')).Split([char]0, [StringSplitOptions]::RemoveEmptyEntries)
            (Get-OperatorGit $repo.Root @('ls-files', '--others', '--exclude-standard', '-z')).Split([char]0, [StringSplitOptions]::RemoveEmptyEntries)
        ) | Sort-Object -Unique
        $records = @()
        [long]$total = 0
        foreach ($relative in $paths) {
            $source = [IO.Path]::GetFullPath((Join-Path $repo.Root $relative))
            if (-not $source.StartsWith($repo.Root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Backup path escaped the repository.' }
            Confirm-PlainPath $source
            if (-not (Test-Path -LiteralPath $source)) { $records += @{ Path = $relative; Missing = $true }; continue }
            $item = Get-Item -LiteralPath $source -Force
            if ($item.PSIsContainer) { throw "Nested/untracked repository or directory cannot be captured as a file: $relative" }
            $total += $item.Length
            if ($total -gt $MaxBytes) { throw "Checkpoint exceeds the $MaxBytes byte limit. No working files were changed." }
            $destination = Join-Path $folder "files/$relative"
            $null = New-Item -ItemType Directory -Path (Split-Path $destination) -Force
            [IO.File]::Copy($source, $destination, $false)
            $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
            if ($hash -ne (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash) { throw "Concurrent file change: $relative" }
            $records += @{ Path = $relative; Missing = $false; Sha256 = $hash }
        }
        $indexCommit = Get-OperatorGit $repo.Root @('-c', 'user.name=Local operator safety', '-c', 'user.email=operator-safety@localhost', 'commit-tree', $indexTree, '-p', $repo.Head, '-m', "Local index checkpoint $id")
        $headRef = "refs/operator-safety/$id/head"
        $indexRef = "refs/operator-safety/$id/index"
        $null = Get-OperatorGit $repo.Root @('update-ref', $headRef, $repo.Head, ('0' * $repo.Head.Length))
        $null = Get-OperatorGit $repo.Root @('update-ref', $indexRef, $indexCommit, ('0' * $indexCommit.Length))
        $main = Get-OperatorRef $repo.Root 'refs/heads/main'
        if ($main) { $null = Get-OperatorGit $repo.Root @('update-ref', "refs/operator-safety/$id/main", $main, ('0' * $main.Length)) }
        if ($repo.Head -ne (Get-OperatorGit $repo.Root @('rev-parse', 'HEAD')) -or $indexTree -ne (Get-OperatorGit $repo.Root @('write-tree')) -or $status -ne (Get-OperatorGit $repo.Root @('status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=none'))) { throw 'Repository changed during checkpoint creation.' }
        foreach ($record in $records) {
            $source = Join-Path $repo.Root $record.Path
            if ($record.Missing) { if (Test-Path -LiteralPath $source) { throw 'A deleted path reappeared during checkpoint.' } }
            elseif ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $record.Sha256) { throw 'Working bytes changed during checkpoint.' }
        }
        $manifest = [ordered]@{ Version = 1; Repository = $repo.Root; Head = $repo.Head; Branch = $repo.Branch; HeadRef = $headRef; IndexRef = $indexRef; Main = $main; Files = @($records); IgnoredFiles = 'NOT_COPIED; Git overwrite protection is required'; Status = $status }
        [IO.File]::WriteAllText((Join-Path $folder 'checkpoint.json'), ($manifest | ConvertTo-Json -Depth 6))
        return $folder
    }
    catch { throw "Checkpoint incomplete; retained at $folder. $($_.Exception.Message)" }
}

function Sync-OperatorMain {
    param([string]$RepositoryPath)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-OperatorReady $repo -Clean
    Confirm-BranchAvailable $repo main
    $checkpoint = New-OperatorCheckpoint $repo.Root
    $null = Get-OperatorGit $repo.Root @('fetch', '--no-tags', '--no-recurse-submodules', 'origin', 'main')
    $target = Get-OperatorGit $repo.Root @('rev-parse', '--verify', 'FETCH_HEAD^{commit}')
    $main = Get-OperatorRef $repo.Root 'refs/heads/main'
    if ($main) {
        $ancestor = Invoke-OperatorTool $repo.Root git @('merge-base', '--is-ancestor', $main, $target) -AllowFailure
        if ($ancestor.ExitCode -ne 0) { throw "Local main has commits absent from fetched main, or ancestry could not be verified. Nothing switched. Checkpoint: $checkpoint" }
    }
    Confirm-OperatorReady $repo -Clean
    if ((Get-OperatorGit $repo.Root @('rev-parse', 'HEAD')) -ne $repo.Head -or (Get-OperatorGit $repo.Root @('branch', '--show-current')) -ne $repo.Branch -or (Get-OperatorRef $repo.Root 'refs/heads/main') -ne $main) { throw 'A local ref changed during fetch. Retry after inspecting the repository.' }
    if ($repo.Branch -ne 'main') {
        $arguments = @('switch', '--no-overwrite-ignore', '--no-recurse-submodules')
        if ($main) { $arguments += @('main') } else { $arguments += @('--no-track', '-c', 'main', $target) }
        $null = Get-OperatorGit $repo.Root $arguments
    }
    $null = Get-OperatorGit $repo.Root @('-c', 'merge.autoStash=false', 'merge', '--ff-only', '--no-autostash', '--no-overwrite-ignore', $target)
    if ((Get-OperatorGit $repo.Root @('rev-parse', 'HEAD')) -ne $target) { throw "Main did not reach the fetched commit. Inspect state; checkpoint: $checkpoint" }
    [pscustomobject]@{ Branch = 'main'; Head = $target; Checkpoint = $checkpoint }
}

function Switch-OperatorBranch {
    param([string]$RepositoryPath, [string]$Branch)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-BranchName $repo.Root $Branch
    Confirm-OperatorReady $repo -Clean
    Confirm-BranchAvailable $repo $Branch
    if (-not (Get-OperatorRef $repo.Root "refs/heads/$Branch")) { throw 'Branch does not exist locally. This action does not guess a remote branch.' }
    $checkpoint = New-OperatorCheckpoint $repo.Root
    Confirm-OperatorReady $repo -Clean
    $null = Get-OperatorGit $repo.Root @('switch', '--no-overwrite-ignore', '--no-recurse-submodules', '--no-guess', $Branch)
    [pscustomobject]@{ Branch = $Branch; Checkpoint = $checkpoint }
}

function Get-OperatorRecovery {
    param([string]$RepositoryPath)
    $repo = Get-OperatorRepository $RepositoryPath
    $folder = Join-Path $repo.CommonDirectory 'operator-safety'
    if (-not (Test-Path -LiteralPath $folder)) { return 'No operator checkpoints yet.' }
    Confirm-PlainPath $folder
    Get-ChildItem -LiteralPath $folder -Directory | ForEach-Object {
        Confirm-PlainPath $_.FullName
        $file = Join-Path $_.FullName 'checkpoint.json'
        [pscustomobject]@{ Directory = $_.FullName; Complete = Test-Path -LiteralPath $file }
    }
}

function New-OperatorWorktree {
    param([string]$RepositoryPath, [string]$Branch)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-OperatorReady $repo
    Confirm-BranchName $repo.Root $Branch
    if ($Branch -eq 'main' -or (Get-OperatorRef $repo.Root "refs/heads/$Branch")) { throw 'Choose a new task branch; existing branches and main are not created again.' }
    $primary = ((Get-OperatorGit $repo.Root @('worktree', 'list', '--porcelain', '-z')) -split "`0")[0].Substring(9)
    $path = Join-Path $primary ('worktrees/git/task-' + [guid]::NewGuid().ToString('N'))
    Confirm-PlainPath $path
    if (Test-Path -LiteralPath $path) { throw 'The new worktree destination already exists.' }
    $null = Get-OperatorGit $repo.Root @('fetch', '--no-tags', '--no-recurse-submodules', 'origin', 'main')
    $target = Get-OperatorGit $repo.Root @('rev-parse', 'FETCH_HEAD^{commit}')
    $null = Get-OperatorGit $repo.Root @('worktree', 'add', '--no-track', '-b', $Branch, $path, $target)
    [pscustomobject]@{ Branch = $Branch; Worktree = $path; Base = $target }
}

function Save-OperatorCommit {
    param([string]$RepositoryPath, [string]$Message)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-OperatorReady $repo
    if (-not $repo.Branch -or $repo.Branch -eq 'main') { throw 'Commit on an attached task branch, not main or detached HEAD.' }
    if ([string]::IsNullOrWhiteSpace($Message)) { throw 'A commit message is required.' }
    if (-not (Get-OperatorGit $repo.Root @('diff', '--cached', '--name-only'))) { throw 'Nothing staged. Stage explicit paths yourself after reviewing their contents.' }
    $null = Get-OperatorGit $repo.Root @('diff', '--cached', '--check')
    $checkpoint = New-OperatorCheckpoint $repo.Root
    $null = Get-OperatorGit $repo.Root @('commit', '-m', $Message)
    [pscustomobject]@{ Head = Get-OperatorGit $repo.Root @('rev-parse', 'HEAD'); Checkpoint = $checkpoint }
}

function Push-OperatorBranch {
    param([string]$RepositoryPath)
    $repo = Get-OperatorRepository $RepositoryPath
    Confirm-OperatorReady $repo -Clean
    if (-not $repo.Branch -or $repo.Branch -eq 'main') { throw 'Push is limited to an attached task branch, never main.' }
    Get-OperatorGit $repo.Root @('push', '--no-follow-tags', '-u', 'origin', "refs/heads/$($repo.Branch):refs/heads/$($repo.Branch)")
}

function Invoke-OperatorBuild {
    param([string]$RepositoryPath, [switch]$Release, [switch]$AllowNetwork)
    $repo = Get-OperatorRepository $RepositoryPath
    $manifest = Join-Path $repo.Root 'devforgeai/Cargo.toml'
    $lock = Join-Path $repo.Root 'devforgeai/Cargo.lock'
    Confirm-PlainPath $manifest
    if (-not (Test-Path -LiteralPath $manifest) -or -not (Test-Path -LiteralPath $lock)) { throw 'The selected checkout needs devforgeai/Cargo.toml and Cargo.lock.' }
    $metadata = (Invoke-OperatorTool $repo.Root cargo @('metadata', '--manifest-path', $manifest, '--no-deps', '--format-version=1', '--offline', '--locked')).Output | ConvertFrom-Json
    $package = @($metadata.packages | Where-Object { [IO.Path]::GetFullPath($_.manifest_path) -eq $manifest })
    if ($package.Count -ne 1 -or -not @($package[0].targets | Where-Object { $_.name -eq 'devforgeai' -and $_.kind -contains 'bin' }).Count) { throw 'This manifest does not declare the expected devforgeai CLI binary.' }
    $target = Join-Path $repo.Root 'devforgeai/target'
    Confirm-PlainPath $target
    $arguments = @('build', '--manifest-path', $manifest, '--package', $package[0].name, '--bin', 'devforgeai', '--locked', '--target-dir', $target)
    if (-not $AllowNetwork) { $arguments += '--offline' }
    if ($Release) { $arguments += '--release' }
    $buildProfile = if ($Release) { 'release' } else { 'debug' }
    $before = (Get-FileHash -LiteralPath $lock -Algorithm SHA256).Hash
    $cargo = (Get-Command cargo -CommandType Application -ErrorAction Stop).Source
    $PSNativeCommandUseErrorActionPreference = $false
    Push-Location $repo.Root
    try {
        $output = @(& $cargo @arguments 2>&1 | ForEach-Object { Write-Host $_; $_.ToString() })
        $code = $LASTEXITCODE
    }
    finally { Pop-Location }
    $null = New-Item -ItemType Directory -Path $target -Force
    $receipt = Join-Path $target ('operator-build-' + [guid]::NewGuid().ToString('N') + '.json')
    $binary = Join-Path $target "$buildProfile/devforgeai.exe"
    $result = [ordered]@{ ExitCode = $code; Repository = $repo.Root; Head = $repo.Head; Arguments = $arguments; Output = $output; Binary = $binary; LockUnchanged = $before -eq (Get-FileHash -LiteralPath $lock -Algorithm SHA256).Hash; Receipt = $receipt }
    [IO.File]::WriteAllText($receipt, ($result | ConvertTo-Json -Depth 4))
    if ($code -ne 0 -or -not $result.LockUnchanged -or -not (Test-Path -LiteralPath $binary)) { throw "Build failed or expected output/lock integrity missing. Receipt: $receipt. No install or CLI execution performed." }
    [pscustomobject]$result
}

function Invoke-OperatorAction {
    param([string]$RepositoryPath, [string]$Action, [string]$Branch, [string]$Message, [switch]$Approve, [switch]$AllowNetwork)
    $repo = Get-OperatorRepository $RepositoryPath
    if ($Action -notin @('Status', 'Recovery', 'PullRequests') -and -not $Approve) { throw 'This action needs explicit approval. Use the menu or pass -Approve after inspecting the repository.' }
    switch ($Action) {
        Status {
            Get-OperatorGit $repo.Root @('status', '--short', '--branch')
            Get-OperatorGit $repo.Root @('branch', '-vv')
            Get-OperatorGit $repo.Root @('worktree', 'list')
        }
        Fetch { Get-OperatorGit $repo.Root @('fetch', '--no-tags', '--no-recurse-submodules', 'origin') }
        Checkpoint { New-OperatorCheckpoint $repo.Root }
        SyncMain { Sync-OperatorMain $repo.Root }
        SwitchBranch { Switch-OperatorBranch $repo.Root $Branch }
        Worktree { New-OperatorWorktree $repo.Root $Branch }
        Commit { Save-OperatorCommit $repo.Root $Message }
        Push { Push-OperatorBranch $repo.Root }
        Recovery { Get-OperatorRecovery $repo.Root }
        BuildDebug { Invoke-OperatorBuild $repo.Root -AllowNetwork:$AllowNetwork }
        BuildRelease { Invoke-OperatorBuild $repo.Root -Release -AllowNetwork:$AllowNetwork }
        PullRequests { (Invoke-OperatorTool $repo.Root gh @('pr', 'list', '--limit', '20')).Output }
        DraftPr {
            Confirm-OperatorReady $repo -Clean
            if (-not $repo.Branch -or $repo.Branch -eq 'main') { throw 'Open a draft PR from an attached task branch.' }
            (Invoke-OperatorTool $repo.Root gh @('pr', 'create', '--draft', '--base', 'main', '--head', $repo.Branch, '--fill')).Output
        }
        default { throw "Unknown action: $Action" }
    }
}

function Start-OperatorMenu {
    param([string]$RepositoryPath)
    $actions = @('Status', 'Fetch', 'Checkpoint', 'SyncMain', 'SwitchBranch', 'Worktree', 'Commit', 'Push', 'PullRequests', 'DraftPr', 'Recovery', 'BuildDebug', 'BuildRelease')
    while ($true) {
        $repo = Get-OperatorRepository $RepositoryPath
        Write-Host "`nDevForgeAI operator console`nRoot: $($repo.Root)`nBranch: $($repo.Branch)  HEAD: $($repo.Head)"
        Write-Host '1 Status/branches/worktrees  2 Fetch  3 Safety checkpoint  4 Switch to main + fast-forward'
        Write-Host '5 Switch local branch  6 New task worktree  7 Commit staged files  8 Push task branch'
        Write-Host '9 List PRs  10 Open draft PR  11 List recovery checkpoints  12 Build CLI debug  13 Build CLI release  0 Exit'
        Write-Host 'No automatic stash, reset, clean, force-push, PR merge, install, or worktree deletion.'
        $choice = Read-Host 'Option'
        if ($choice -eq '0') { return }
        [int]$number = 0
        if (-not [int]::TryParse($choice, [ref]$number) -or $number -lt 1 -or $number -gt $actions.Count) { Write-Host 'Choose a displayed number.'; continue }
        $action = $actions[$number - 1]
        $parameters = @{ RepositoryPath = $repo.Root; Action = $action }
        if ($action -in @('SwitchBranch', 'Worktree')) { $parameters.Branch = Read-Host 'Literal branch name' }
        if ($action -eq 'Commit') { $parameters.Message = Read-Host 'Commit message (only already staged files will be committed)' }
        if ($action -in @('BuildDebug', 'BuildRelease')) { $parameters.AllowNetwork = (Read-Host 'Allow Cargo dependency downloads? [y/N]') -eq 'y' }
        if ($action -notin @('Status', 'Recovery', 'PullRequests')) {
            Write-Host "Selected action: $action in $($repo.Root). Stop other writers before continuing."
            if ((Read-Host 'Type YES to proceed') -cne 'YES') { Write-Host 'Cancelled.'; continue }
            $parameters.Approve = $true
        }
        try { Invoke-OperatorAction @parameters | Format-List | Out-Host }
        catch { Write-Host "STOPPED: $($_.Exception.Message)" -ForegroundColor Yellow }
    }
}

Export-ModuleMember -Function Get-OperatorRepository, New-OperatorCheckpoint, Sync-OperatorMain, Switch-OperatorBranch, Get-OperatorRecovery, New-OperatorWorktree, Save-OperatorCommit, Push-OperatorBranch, Invoke-OperatorBuild, Invoke-OperatorAction, Start-OperatorMenu
