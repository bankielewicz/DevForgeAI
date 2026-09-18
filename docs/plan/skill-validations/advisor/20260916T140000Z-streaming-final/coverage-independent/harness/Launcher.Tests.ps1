Describe 'advisor launcher native behavior' {
    BeforeEach {
        $global:LASTEXITCODE = $null
        $env:ADVISOR_ARGS_PATH = Join-Path -Path $env:ADVISOR_CASE_ROOT -ChildPath (([Guid]::NewGuid().ToString('N')) + '.txt')
    }

    It 'forwards progress and propagates native success' {
        $env:ADVISOR_FAKE_PYTHON_EXIT = '0'
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason retry -Python $env:ADVISOR_FAKE_PYTHON -ShowProgress
        $observedExit = $LASTEXITCODE
        $observedArguments = Get-Content -LiteralPath $env:ADVISOR_ARGS_PATH -Raw
        if ($observedExit -ne 0) { throw "expected exit 0, observed $observedExit" }
        if ($observedArguments -notmatch '(?m)(?:^|\s)--show-progress(?:\s|$)') { throw 'expected --show-progress' }
        if ($observedArguments -notmatch '(?m)(?:^|\s)--reason\s+retry(?:\s|$)') { throw 'expected retry reason' }
    }

    It 'omits progress and propagates native failure' {
        $env:ADVISOR_FAKE_PYTHON_EXIT = '7'
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_FAKE_PYTHON
        $observedExit = $LASTEXITCODE
        $observedArguments = Get-Content -LiteralPath $env:ADVISOR_ARGS_PATH -Raw
        if ($observedExit -ne 7) { throw "expected exit 7, observed $observedExit" }
        if ($observedArguments -match '(?m)(?:^|\s)--show-progress(?:\s|$)') { throw 'unexpected --show-progress' }
        if ($observedArguments -notmatch '(?m)(?:^|\s)--reason\s+initial(?:\s|$)') { throw 'expected initial reason' }
    }

    It 'rejects a non-native Python command with no process status' {
        $global:LASTEXITCODE = $null
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_FAKE_SCRIPT
        $observedExit = $LASTEXITCODE
        if ($observedExit -ne 2) { throw "expected exit 2, observed $observedExit" }
    }

    It 'reports invocation failure as exit 2' {
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_MISSING_PYTHON -ShowProgress
        $observedExit = $LASTEXITCODE
        if ($observedExit -ne 2) { throw "expected exit 2, observed $observedExit" }
    }
}
