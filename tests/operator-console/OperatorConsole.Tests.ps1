BeforeAll {
    $script:projectRoot = Split-Path (Split-Path $PSScriptRoot)
    Import-Module (Join-Path $script:projectRoot 'scripts/operator-console/OperatorConsole.psm1') -Force
    function Invoke-TestGit {
        param([string]$At, [string[]]$Arguments)
        # Windows PowerShell wraps native stderr as ErrorRecords, even on success.
        $ErrorActionPreference = 'Continue'
        $text = & git -C $At @Arguments 2>&1
        if ($LASTEXITCODE -ne 0) { throw "Fixture Git failure: $Arguments`n$text" }
        ($text -join "`n")
    }
    function New-TestRepository {
        $base = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $base | Out-Null
        Invoke-TestGit $base @('init', '--bare', '--initial-branch=main', 'origin.git') | Out-Null
        Invoke-TestGit $base @('init', '--initial-branch=main', 'seed') | Out-Null
        $seed = Join-Path $base 'seed'
        Invoke-TestGit $seed @('config', 'user.name', 'Fixture') | Out-Null
        Invoke-TestGit $seed @('config', 'user.email', 'fixture@example.invalid') | Out-Null
        [IO.File]::WriteAllText((Join-Path $seed 'tracked.txt'), 'original')
        [IO.File]::WriteAllText((Join-Path $seed '.gitignore'), "ignored/`nworktrees/`n")
        Invoke-TestGit $seed @('add', '--', 'tracked.txt', '.gitignore') | Out-Null
        Invoke-TestGit $seed @('commit', '-m', 'initial') | Out-Null
        Invoke-TestGit $seed @('remote', 'add', 'origin', (Join-Path $base 'origin.git')) | Out-Null
        Invoke-TestGit $seed @('push', '-u', 'origin', 'main') | Out-Null
        Invoke-TestGit $base @('clone', (Join-Path $base 'origin.git'), 'operator') | Out-Null
        $repo = Join-Path $base 'operator'
        Invoke-TestGit $repo @('config', 'user.name', 'Fixture') | Out-Null
        Invoke-TestGit $repo @('config', 'user.email', 'fixture@example.invalid') | Out-Null
        @{ Base = $base; Seed = $seed; Repo = $repo }
    }
    function Add-UpstreamCommit {
        param($Fixture)
        [IO.File]::WriteAllText((Join-Path $Fixture.Seed 'tracked.txt'), 'upstream')
        Invoke-TestGit $Fixture.Seed @('commit', '-am', 'upstream change') | Out-Null
        Invoke-TestGit $Fixture.Seed @('push', 'origin', 'main') | Out-Null
    }
}

Describe 'Safe main synchronization' {
    It 'switches a clean task branch and fast-forwards main while retaining a recovery point' -Tag Red {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/example') | Out-Null
        $oldHead = Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD')
        Add-UpstreamCommit $fixture
        $result = Sync-OperatorMain -RepositoryPath $fixture.Repo
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'main'
        [IO.File]::ReadAllText((Join-Path $fixture.Repo 'tracked.txt')) | Should -Be 'upstream'
        Invoke-TestGit $fixture.Repo @('rev-parse', 'task/example') | Should -Be $oldHead
        Test-Path -LiteralPath (Join-Path $result.Checkpoint 'checkpoint.json') | Should -BeTrue
    }

    It 'refuses <Kind> changes without touching local bytes' -ForEach @(@{ Kind = 'unstaged' }, @{ Kind = 'staged' }, @{ Kind = 'untracked' }) {
        $fixture = New-TestRepository
        $file = if ($Kind -eq 'untracked') { 'new file.txt' } else { 'tracked.txt' }
        [IO.File]::WriteAllText((Join-Path $fixture.Repo $file), 'precious local data')
        if ($Kind -eq 'staged') { Invoke-TestGit $fixture.Repo @('add', '--', $file) | Out-Null }
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*not clean*'
        [IO.File]::ReadAllText((Join-Path $fixture.Repo $file)) | Should -Be 'precious local data'
    }

    It 'refuses divergent or ahead main and preserves both local branches' {
        $fixture = New-TestRepository
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'local.txt'), 'local commit')
        Invoke-TestGit $fixture.Repo @('add', '--', 'local.txt') | Out-Null
        Invoke-TestGit $fixture.Repo @('commit', '-m', 'local change') | Out-Null
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/local') | Out-Null
        $head = Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD')
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*absent from fetched main*'
        Add-UpstreamCommit $fixture
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*absent from fetched main*'
        Invoke-TestGit $fixture.Repo @('rev-parse', 'main') | Should -Be $head
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'task/local'
    }

    It 'refuses main occupied by another worktree without moving its checkout' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/other') | Out-Null
        $other = Join-Path $fixture.Base 'main checkout'
        Invoke-TestGit $fixture.Repo @('worktree', 'add', $other, 'main') | Out-Null
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*another worktree*'
        [IO.File]::ReadAllText((Join-Path $other 'tracked.txt')) | Should -Be 'original'
    }

    It 'protects ignored file collisions during a fast-forward' {
        $fixture = New-TestRepository
        foreach ($root in @($fixture.Seed, $fixture.Repo)) { New-Item -ItemType Directory -Path (Join-Path $root 'ignored') | Out-Null }
        $local = Join-Path $fixture.Repo 'ignored/private.txt'
        [IO.File]::WriteAllText($local, 'private local data')
        [IO.File]::WriteAllText((Join-Path $fixture.Seed 'ignored/private.txt'), 'remote tracked content')
        Invoke-TestGit $fixture.Seed @('add', '-f', '--', 'ignored/private.txt') | Out-Null
        Invoke-TestGit $fixture.Seed @('commit', '-m', 'track previously ignored path') | Out-Null
        Invoke-TestGit $fixture.Seed @('push', 'origin', 'main') | Out-Null
        $head = Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD')
        { Sync-OperatorMain $fixture.Repo } | Should -Throw
        [IO.File]::ReadAllText($local) | Should -Be 'private local data'
        Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD') | Should -Be $head
    }

    It 'creates missing main while preserving detached commits through a recovery ref' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('branch', '-m', 'task/renamed') | Out-Null
        Invoke-TestGit $fixture.Repo @('switch', '--detach') | Out-Null
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'detached work')
        Invoke-TestGit $fixture.Repo @('commit', '-am', 'detached change') | Out-Null
        $detached = Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD')
        $result = Sync-OperatorMain $fixture.Repo
        $manifest = Get-Content -Raw -LiteralPath (Join-Path $result.Checkpoint 'checkpoint.json') | ConvertFrom-Json
        Invoke-TestGit $fixture.Repo @('rev-parse', $manifest.HeadRef) | Should -Be $detached
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'main'
    }

    It 'keeps the original branch and checkpoint on a fetch failure' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/offline') | Out-Null
        Invoke-TestGit $fixture.Repo @('remote', 'set-url', 'origin', (Join-Path $fixture.Base 'missing.git')) | Out-Null
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*git failed*'
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'task/offline'
        @(Get-OperatorRecovery $fixture.Repo).Count | Should -Be 1
    }

    It 'refuses untracked data introduced during fetch' {
        $fixture = New-TestRepository
        Mock Get-OperatorGit -ModuleName OperatorConsole -ParameterFilter { $Arguments[0] -eq 'fetch' } -MockWith {
            param($Root, $Arguments)
            $ErrorActionPreference = 'Continue'
            $result = & git -C $Root @Arguments 2>&1
            if ($LASTEXITCODE -ne 0) { throw 'Fixture fetch failed.' }
            [IO.File]::WriteAllText((Join-Path $Root 'concurrent.txt'), 'concurrent writer')
            $result -join "`n"
        }
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*not clean*'
        [IO.File]::ReadAllText((Join-Path $fixture.Repo 'concurrent.txt')) | Should -Be 'concurrent writer'
    }
}

Describe 'Checkpoints and mutation admission' {
    It 'preserves staged, unstaged, deleted and Unicode binary untracked content independently' {
        $fixture = New-TestRepository
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'staged')
        Invoke-TestGit $fixture.Repo @('add', '--', 'tracked.txt') | Out-Null
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'working')
        [IO.File]::WriteAllBytes((Join-Path $fixture.Repo '日本語 file.bin'), [byte[]](0, 255, 128, 10, 13))
        Remove-Item -LiteralPath (Join-Path $fixture.Repo '.gitignore')
        $before = Invoke-TestGit $fixture.Repo @('status', '--porcelain=v1')
        $directory = New-OperatorCheckpoint $fixture.Repo
        $manifest = Get-Content -Raw -LiteralPath (Join-Path $directory 'checkpoint.json') | ConvertFrom-Json
        Invoke-TestGit $fixture.Repo @('show', ($manifest.IndexRef + ':tracked.txt')) | Should -Be 'staged'
        Invoke-TestGit $fixture.Repo @('show', ($manifest.HeadRef + ':tracked.txt')) | Should -Be 'original'
        [IO.File]::ReadAllText((Join-Path $directory 'files/tracked.txt')) | Should -Be 'working'
        [BitConverter]::ToString([IO.File]::ReadAllBytes((Join-Path $directory 'files/日本語 file.bin'))).Replace('-', '') | Should -Be '00FF800A0D'
        ($manifest.Files | Where-Object Path -EQ '.gitignore').Missing | Should -BeTrue
        Invoke-TestGit $fixture.Repo @('status', '--porcelain=v1') | Should -Be $before
    }

    It 'retains a clearly incomplete checkpoint when the byte limit prevents capture' {
        $fixture = New-TestRepository
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'too large for selected limit')
        { New-OperatorCheckpoint $fixture.Repo -MaxBytes 1 } | Should -Throw '*Checkpoint incomplete*byte limit*'
        @(Get-OperatorRecovery $fixture.Repo)[0].Complete | Should -BeFalse
        [IO.File]::ReadAllText((Join-Path $fixture.Repo 'tracked.txt')) | Should -Be 'too large for selected limit'
    }

    It 'rejects operation markers and submodules without altering the index' {
        $fixture = New-TestRepository
        foreach ($marker in @('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'BISECT_LOG', 'index.lock')) {
            $path = Join-Path $fixture.Repo ".git/$marker"
            [IO.File]::WriteAllText($path, 'busy')
            { Sync-OperatorMain $fixture.Repo } | Should -Throw '*in progress*'
            Remove-Item -LiteralPath $path
        }
        $head = Invoke-TestGit $fixture.Repo @('rev-parse', 'HEAD')
        Invoke-TestGit $fixture.Repo @('update-index', '--add', '--cacheinfo', "160000,$head,submodule") | Out-Null
        { New-OperatorCheckpoint $fixture.Repo } | Should -Throw '*Submodule*'
    }

    It 'rejects junction capture instead of following an untracked directory' {
        $fixture = New-TestRepository
        $outside = Join-Path $fixture.Base 'outside'
        New-Item -ItemType Directory -Path $outside | Out-Null
        [IO.File]::WriteAllText((Join-Path $outside 'secret.txt'), 'outside sentinel')
        $junction = Join-Path $fixture.Repo 'junction'
        New-Item -ItemType Junction -Path $junction -Target $outside | Out-Null
        { New-OperatorCheckpoint $fixture.Repo } | Should -Throw '*Reparse*'
        [IO.File]::ReadAllText((Join-Path $outside 'secret.txt')) | Should -Be 'outside sentinel'
        [IO.Directory]::Delete($junction)
    }

    It 'reports no checkpoints and rejects subdirectory or nonrepository roots' {
        $fixture = New-TestRepository
        Get-OperatorRecovery $fixture.Repo | Should -Be 'No operator checkpoints yet.'
        New-Item -ItemType Directory -Path (Join-Path $fixture.Repo 'nested') | Out-Null
        { Get-OperatorRepository (Join-Path $fixture.Repo 'nested') } | Should -Throw '*root, not a subdirectory*'
        { Get-OperatorRepository $fixture.Base } | Should -Throw '*git failed*'
    }
}

Describe 'Common operator actions' {
    It 'switches an existing clean branch and refuses missing or option-shaped names' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('branch', 'task/next') | Out-Null
        (Switch-OperatorBranch $fixture.Repo 'task/next').Branch | Should -Be 'task/next'
        foreach ($name in @('', '-f', 'HEAD', 'bad..name', 'task/missing')) { { Switch-OperatorBranch $fixture.Repo $name } | Should -Throw }
    }

    It 'creates a real task worktree without switching the primary checkout' {
        $fixture = New-TestRepository
        $created = New-OperatorWorktree $fixture.Repo 'task/new'
        Invoke-TestGit $created.Worktree @('branch', '--show-current') | Should -Be 'task/new'
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'main'
        { New-OperatorWorktree $fixture.Repo 'task/new' } | Should -Throw '*new task branch*'
    }

    It 'commits only staged files on task branches with a prior checkpoint' {
        $fixture = New-TestRepository
        { Save-OperatorCommit $fixture.Repo 'unsafe' } | Should -Throw '*not main*'
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/commit') | Out-Null
        { Save-OperatorCommit $fixture.Repo '' } | Should -Throw '*message*'
        { Save-OperatorCommit $fixture.Repo 'empty' } | Should -Throw '*Nothing staged*'
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'commit this')
        Invoke-TestGit $fixture.Repo @('add', '--', 'tracked.txt') | Out-Null
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'untracked.txt'), 'leave this')
        $result = Save-OperatorCommit $fixture.Repo 'selected staged change'
        Invoke-TestGit $fixture.Repo @('show', 'HEAD:tracked.txt') | Should -Be 'commit this'
        Invoke-TestGit $fixture.Repo @('ls-files', '--', 'untracked.txt') | Should -Be ''
        Test-Path -LiteralPath (Join-Path $result.Checkpoint 'files/untracked.txt') | Should -BeTrue
    }

    It 'pushes an explicit task branch and refuses main' {
        $fixture = New-TestRepository
        { Push-OperatorBranch $fixture.Repo } | Should -Throw '*never main*'
        Invoke-TestGit $fixture.Repo @('switch', '-c', 'task/push') | Out-Null
        Push-OperatorBranch $fixture.Repo | Out-Null
        Invoke-TestGit $fixture.Repo @('rev-parse', '--abbrev-ref', '@{upstream}') | Should -Be 'origin/task/push'
    }

    It 'requires explicit approval for mutating noninteractive actions' {
        $fixture = New-TestRepository
        { Invoke-OperatorAction $fixture.Repo SyncMain } | Should -Throw '*explicit approval*'
        { Invoke-OperatorAction $fixture.Repo Unknown -Approve } | Should -Throw '*Unknown action*'
        (Invoke-OperatorAction $fixture.Repo Status) -join "`n" | Should -Match 'main'
        Invoke-OperatorAction $fixture.Repo Recovery | Should -Be 'No operator checkpoints yet.'
        Invoke-OperatorAction $fixture.Repo Fetch -Approve | Out-Null
        Invoke-OperatorAction $fixture.Repo Checkpoint -Approve | Should -Not -BeNullOrEmpty
        Invoke-OperatorAction $fixture.Repo SyncMain -Approve | Should -Not -BeNullOrEmpty
        { Invoke-OperatorAction $fixture.Repo DraftPr -Approve } | Should -Throw '*attached task branch*'
    }
}

Describe 'Rust build and console entry' {
    BeforeAll {
        function Add-RustFixture {
            param($Fixture, [string]$Code = 'fn main() { println!("fixture"); }')
            $ErrorActionPreference = 'Continue'
            $source = Join-Path $Fixture.Repo 'devforgeai/src'
            New-Item -ItemType Directory -Path $source -Force | Out-Null
            [IO.File]::WriteAllText((Join-Path $Fixture.Repo 'devforgeai/Cargo.toml'), "[package]`nname = `"operator-build-fixture`"`nversion = `"0.1.0`"`nedition = `"2021`"`n[[bin]]`nname = `"devforgeai`"`npath = `"src/main.rs`"`n")
            [IO.File]::WriteAllText((Join-Path $source 'main.rs'), $Code)
            & cargo generate-lockfile --manifest-path (Join-Path $Fixture.Repo 'devforgeai/Cargo.toml') --offline 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { throw 'Fixture lockfile generation failed.' }
        }
    }
    It 'builds an actual Rust executable in both profiles and preserves the lockfile' {
        $fixture = New-TestRepository
        Add-RustFixture $fixture
        $debug = Invoke-OperatorAction $fixture.Repo BuildDebug -Approve
        $debug.ExitCode | Should -Be 0
        $debug.Arguments | Should -Contain '--offline'
        $debug.LockUnchanged | Should -BeTrue
        Test-Path -LiteralPath $debug.Binary | Should -BeTrue
        $release = Invoke-OperatorAction $fixture.Repo BuildRelease -Approve -AllowNetwork
        $release.Arguments | Should -Not -Contain '--offline'
        $release.Arguments | Should -Contain '--release'
        Test-Path -LiteralPath $release.Binary | Should -BeTrue
        $debug.Receipt | Should -Not -Be $release.Receipt
    }
    It 'retains compiler errors without reporting a stale executable as success' {
        $fixture = New-TestRepository
        Add-RustFixture $fixture 'this is not Rust'
        $target = Join-Path $fixture.Repo 'devforgeai/target/debug'
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        [IO.File]::WriteAllText((Join-Path $target 'devforgeai.exe'), 'stale sentinel')
        { Invoke-OperatorBuild $fixture.Repo } | Should -Throw '*Build failed*Receipt*'
        $receipt = Get-ChildItem -LiteralPath (Split-Path $target) -Filter 'operator-build-*.json' | Get-Content -Raw | ConvertFrom-Json
        $receipt.ExitCode | Should -Not -Be 0
        ($receipt.Output -join "`n") | Should -Match 'error'
        [IO.File]::ReadAllText((Join-Path $target 'devforgeai.exe')) | Should -Be 'stale sentinel'
    }
    It 'rejects absent manifests and a manifest with the wrong binary target' {
        $fixture = New-TestRepository
        { Invoke-OperatorBuild $fixture.Repo } | Should -Throw '*Cargo.toml and Cargo.lock*'
        Add-RustFixture $fixture
        $manifest = Join-Path $fixture.Repo 'devforgeai/Cargo.toml'
        [IO.File]::WriteAllText($manifest, ([IO.File]::ReadAllText($manifest).Replace('name = "devforgeai"', 'name = "wrong-cli"')))
        { Invoke-OperatorBuild $fixture.Repo } | Should -Throw '*expected devforgeai CLI*'
    }
    It 'runs the public script for status and returns a failing exit code for an unapproved mutation' {
        $fixture = New-TestRepository
        $entry = Join-Path $script:projectRoot 'DevForgeAI-Console.ps1'
        & $entry -RepositoryPath $fixture.Repo -Action Status | Out-String | Should -Match 'main'
        $hostPath = (Get-Process -Id $PID).Path
        $ErrorActionPreference = 'Continue'
        $output = & $hostPath -NoProfile -File $entry -RepositoryPath $fixture.Repo -Action SyncMain 2>&1
        $LASTEXITCODE | Should -Be 1
        ($output -join "`n") | Should -Match 'explicit approval'
    }
}

Describe 'Interactive menu and command routing' {
    It 'handles invalid choices, cancellation, prompts and errors while returning to the menu' {
        $fixture = New-TestRepository
        $answers = [Collections.Generic.Queue[string]]::new()
        foreach ($answer in @('bogus', '99', '4', 'no', '5', 'task/example', 'YES', '7', 'message', 'YES', '12', 'n', 'YES', '9', '0')) { $answers.Enqueue($answer) }
        Mock Read-Host -ModuleName OperatorConsole { $answers.Dequeue() }
        Mock Invoke-OperatorAction -ModuleName OperatorConsole {
            param($Action)
            if ($Action -eq 'SwitchBranch') { throw 'Fixture action failure' }
            'fixture action output'
        }
        Start-OperatorMenu $fixture.Repo
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 4 -Exactly
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 0 -ParameterFilter { $Action -eq 'SyncMain' }
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 1 -ParameterFilter { $Action -eq 'Commit' -and $Message -eq 'message' -and $Approve }
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 1 -ParameterFilter { $Action -eq 'BuildDebug' -and -not $AllowNetwork }
        $answers.Count | Should -Be 0
    }
    It 'routes task actions and only requests draft PR creation' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('branch', 'task/actions') | Out-Null
        Invoke-OperatorAction $fixture.Repo SwitchBranch -Branch 'task/actions' -Approve | Out-Null
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'dispatch commit')
        Invoke-TestGit $fixture.Repo @('add', '--', 'tracked.txt') | Out-Null
        Invoke-OperatorAction $fixture.Repo Commit -Message 'dispatch commit' -Approve | Out-Null
        Invoke-OperatorAction $fixture.Repo Push -Approve | Out-Null
        Invoke-OperatorAction $fixture.Repo Worktree -Branch 'task/new-dispatch' -Approve | Out-Null
        Mock Invoke-OperatorTool -ModuleName OperatorConsole -ParameterFilter { $Program -eq 'gh' } { [pscustomobject]@{ Output = 'fixture PR response' } }
        Invoke-OperatorAction $fixture.Repo PullRequests | Should -Be 'fixture PR response'
        Invoke-OperatorAction $fixture.Repo DraftPr -Approve | Should -Be 'fixture PR response'
        Should -Invoke Invoke-OperatorTool -ModuleName OperatorConsole -Times 1 -ParameterFilter { $Program -eq 'gh' -and $Arguments[1] -eq 'create' -and $Arguments -contains '--draft' -and $Arguments -contains 'task/actions' }
    }
}

Describe 'Hidden changes and concurrent branch movement' {
    It 'refuses <Flag> index flags instead of treating hidden edits as clean' -ForEach @(@{ Flag = '--assume-unchanged' }, @{ Flag = '--skip-worktree' }) {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('update-index', $Flag, '--', 'tracked.txt') | Out-Null
        [IO.File]::WriteAllText((Join-Path $fixture.Repo 'tracked.txt'), 'hidden local bytes')
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*index flags*'
        [IO.File]::ReadAllText((Join-Path $fixture.Repo 'tracked.txt')) | Should -Be 'hidden local bytes'
    }
    It 'refuses a same-commit branch switch by another writer during fetch' {
        $fixture = New-TestRepository
        Invoke-TestGit $fixture.Repo @('branch', 'task/concurrent') | Out-Null
        Mock Get-OperatorGit -ModuleName OperatorConsole -ParameterFilter { $Arguments[0] -eq 'fetch' } {
            param($Root, $Arguments)
            $ErrorActionPreference = 'Continue'
            & git -C $Root @Arguments 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { throw 'Fixture fetch failed.' }
            & git -C $Root switch task/concurrent 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { throw 'Fixture switch failed.' }
            ''
        }
        { Sync-OperatorMain $fixture.Repo } | Should -Throw '*local ref changed*'
        Invoke-TestGit $fixture.Repo @('branch', '--show-current') | Should -Be 'task/concurrent'
    }
}
