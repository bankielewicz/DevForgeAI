BeforeAll {
    $script:projectRoot = Split-Path (Split-Path $PSScriptRoot)
    Import-Module (Join-Path $script:projectRoot 'scripts/operator-console/OperatorConsole.psm1') -Force
}

Describe 'Menu confirmation and completion feedback' -Tag Confirmation {
    It 'accepts <Reply> for <Action> and reports a silent success' -ForEach @(
        @{ Reply = 'yes'; Choice = '2'; Action = 'Fetch' }
        @{ Reply = 'YES'; Choice = '3'; Action = 'Checkpoint' }
        @{ Reply = 'Yes'; Choice = '4'; Action = 'SyncMain' }
        @{ Reply = '  yes  '; Choice = '2'; Action = 'Fetch' }
    ) {
        $expectedAction = $Action
        $answers = [Collections.Generic.Queue[string]]::new()
        foreach ($answer in @($Choice, $Reply, '0')) { $answers.Enqueue($answer) }
        Mock Read-Host -ModuleName OperatorConsole { $answers.Dequeue() }
        Mock Invoke-OperatorAction -ModuleName OperatorConsole { }
        $output = @(Start-OperatorMenu $script:projectRoot 6>&1 | ForEach-Object { $_.ToString() }) -join "`n"
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 1 -Exactly -ParameterFilter { $Action -eq $expectedAction -and $Approve }
        $output | Should -Match ([regex]::Escape("Completed: $Action."))
        $output | Should -Not -Match 'Cancelled\.'
        $answers.Count | Should -Be 0
    }

    It 'cancels <Label> without invoking an action or reporting completion' -ForEach @(
        @{ Reply = ''; Label = 'empty input' }
        @{ Reply = '   '; Label = 'whitespace' }
        @{ Reply = 'no'; Label = 'no' }
        @{ Reply = 'y'; Label = 'abbreviation' }
        @{ Reply = 'yesterday'; Label = 'other text' }
    ) {
        $answers = [Collections.Generic.Queue[string]]::new()
        foreach ($answer in @('2', $Reply, '0')) { $answers.Enqueue($answer) }
        Mock Read-Host -ModuleName OperatorConsole { $answers.Dequeue() }
        Mock Invoke-OperatorAction -ModuleName OperatorConsole { }
        $output = @(Start-OperatorMenu $script:projectRoot 6>&1 | ForEach-Object { $_.ToString() }) -join "`n"
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 0 -Exactly
        $output | Should -Match 'Cancelled\.'
        $output | Should -Not -Match 'Completed:'
        $answers.Count | Should -Be 0
    }

    It 'reports a failed action without printing a success message' {
        $answers = [Collections.Generic.Queue[string]]::new()
        foreach ($answer in @('2', 'YES', '0')) { $answers.Enqueue($answer) }
        Mock Read-Host -ModuleName OperatorConsole { $answers.Dequeue() }
        Mock Invoke-OperatorAction -ModuleName OperatorConsole { throw 'fixture failure' }
        $output = @(Start-OperatorMenu $script:projectRoot 6>&1 | ForEach-Object { $_.ToString() }) -join "`n"
        Should -Invoke Invoke-OperatorAction -ModuleName OperatorConsole -Times 1 -Exactly
        $output | Should -Match 'STOPPED: fixture failure'
        $output | Should -Not -Match 'Completed:'
    }
}

Describe 'Windows PowerShell compatibility and menu layout' -Tag Compatibility {
    It 'starts the public entry in the current host without changing Git state' {
        $entry = Join-Path $script:projectRoot 'DevForgeAI-Console.ps1'
        $hostPath = (Get-Process -Id $PID).Path
        $before = & git -C $script:projectRoot status --porcelain=v1
        $ErrorActionPreference = 'Continue'
        $output = & $hostPath -NoProfile -NonInteractive -File $entry -RepositoryPath $script:projectRoot -Action Status 2>&1
        $code = $LASTEXITCODE
        $code | Should -Be 0
        ($output -join "`n") | Should -Match '## '
        (& git -C $script:projectRoot status --porcelain=v1) -join "`n" | Should -Be ($before -join "`n")
    }

    It 'passes literal arguments and captures separate streams and the actual exit code' {
        $echo = Join-Path $TestDrive 'echo arguments.py'
        [IO.File]::WriteAllText($echo, "import json, os, sys`nprint(json.dumps(sys.argv[1:]))`nprint(os.environ['GIT_TERMINAL_PROMPT'], file=sys.stderr)`nsys.exit(7)`n")
        $expected = @('', 'two words', 'embedded"quote', 'slash\"quote', 'C:\path with space\', 'plain', '$(never); & | < >', ([string][char]0x65e5 + [char]0x672c))
        $module = Get-Module OperatorConsole
        $result = & $module {
            param($Directory, $Arguments)
            Invoke-OperatorTool $Directory python $Arguments -AllowFailure
        } $TestDrive (@('-B', '-X', 'utf8', $echo) + $expected)
        $result.ExitCode | Should -Be 7
        $result.Error.Trim() | Should -Be '0'
        $actual = ConvertFrom-Json -InputObject $result.Output
        $actual.Count | Should -Be $expected.Count
        for ($i = 0; $i -lt $expected.Count; $i++) { $actual[$i] | Should -BeExactly $expected[$i] }
    }

    It 'renders every choice on its own aligned line with separated groups' {
        Mock Read-Host -ModuleName OperatorConsole { '0' }
        $lines = @(Start-OperatorMenu $script:projectRoot 6>&1 | ForEach-Object { $_.ToString() })
        $menu = $lines -join "`n"
        foreach ($number in 0..13) {
            @($lines | Where-Object { $_ -match ('^\s*' + $number + '\s{2,}\S') }).Count | Should -Be 1
        }
        foreach ($heading in @('Repository', 'Safety and recovery', 'Branches and delivery', 'Build Rust CLI')) {
            $menu | Should -Match ([regex]::Escape($heading))
        }
        @($lines | Where-Object { $_ -eq '' }).Count | Should -BeGreaterThan 3
        $menu | Should -Match 'Root:'
        $menu | Should -Match 'Branch:'
        $menu | Should -Match 'HEAD:'
    }
}
