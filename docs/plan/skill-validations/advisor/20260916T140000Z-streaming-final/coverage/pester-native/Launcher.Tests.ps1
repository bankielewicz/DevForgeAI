Describe 'advisor launcher native behavior' {
    It 'forwards progress and returns native success' {
        $env:ADVISOR_FAKE_PYTHON_EXIT = '0'
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason retry -Python $env:ADVISOR_FAKE_PYTHON -ShowProgress
        if ($LASTEXITCODE -ne 0) { throw "expected 0, observed $LASTEXITCODE" }
    }

    It 'forwards quiet mode and returns native failure' {
        $env:ADVISOR_FAKE_PYTHON_EXIT = '7'
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_FAKE_PYTHON
        if ($LASTEXITCODE -ne 7) { throw "expected 7, observed $LASTEXITCODE" }
    }

    It 'rejects a nonnative Python command with no process status' {
        $global:LASTEXITCODE = $null
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_FAKE_SCRIPT
        if ($LASTEXITCODE -ne 2) { throw "expected 2, observed $LASTEXITCODE" }
    }

    It 'reports invocation failure as exit 2' {
        & $env:ADVISOR_LAUNCHER -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $env:ADVISOR_MISSING_PYTHON -ShowProgress
        if ($LASTEXITCODE -ne 2) { throw "expected 2, observed $LASTEXITCODE" }
    }
}
