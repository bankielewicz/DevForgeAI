BeforeAll {
    $script:entry = 'C:\Projects\DevForgeAI\Invoke-CodexWorkerDiagnostic.ps1'
    $script:text = Get-Content -LiteralPath $script:entry -Raw
    $global:DiagnosticTestSeal = [regex]::Match($script:text, "manifestSha256 = '([a-f0-9]{64})'").Groups[1].Value
    . $script:entry
}

Describe 'Operator PowerShell entrypoint' {
    BeforeEach {
        $global:DiagnosticTestArgs = @()
        $global:DiagnosticTestMode = 'normal'
        $global:DiagnosticTestChildExit = 0
        Mock Write-Host {}
        Mock Write-Error { param($Message) $global:DiagnosticTestError = $Message }
        Mock Get-Content { '[{"path":"C:\\fixture space & literal\\module.py","sha256":"abc","bytes":12}]' }
        Mock Get-FileHash {
            param($LiteralPath)
            if ($global:DiagnosticTestMode -eq 'missing') { throw 'Missing synthetic runtime file' }
            if ($LiteralPath.EndsWith('runtime-manifest.json')) {
                return [pscustomobject]@{ Hash = $(if ($global:DiagnosticTestMode -eq 'manifest-drift') { 'bad' } else { $global:DiagnosticTestSeal }) }
            }
            return [pscustomobject]@{ Hash = $(if ($global:DiagnosticTestMode -eq 'source-drift') { 'bad' } else { 'abc' }) }
        }
        Mock Get-Item {
            return [pscustomobject]@{ Length = $(if ($global:DiagnosticTestMode -eq 'size-drift') { 13 } else { 12 }) }
        }
        Mock Invoke-DiagnosticPython {
            param($Python, $Entry, $Mode)
            $global:DiagnosticTestArgs = @($Python, $Entry, $Mode)
            if ($global:DiagnosticTestMode -eq 'invoke-error') { throw 'Synthetic process dispatch error' }
            return $global:DiagnosticTestChildExit
        }
    }

    It 'prepares by default with literal module arguments and no native run flag' {
        $actualExit = Invoke-DiagnosticEntry
        $actualExit | Should -Be 0
        $global:DiagnosticTestArgs.Count | Should -Be 3
        $global:DiagnosticTestArgs[0] | Should -Be 'C:\Program Files\Python310\python.exe'
        $global:DiagnosticTestArgs[1] | Should -Be 'C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic\operator-harness-001\diagnostic.py'
        $global:DiagnosticTestArgs[2] | Should -Be '--prepare'
        Should -Invoke Invoke-DiagnosticPython -Times 1 -Exactly
    }

    It 'dispatches once only with the explicit switch and preserves nonzero child exit' {
        $global:DiagnosticTestChildExit = 7
        $actualExit = Invoke-DiagnosticEntry -RunOnce
        $actualExit | Should -Be 7
        $global:DiagnosticTestArgs[2] | Should -Be '--run-once'
        Should -Invoke Invoke-DiagnosticPython -Times 1 -Exactly
    }

    It 'stops if the sealed runtime manifest changed' {
        $global:DiagnosticTestMode = 'manifest-drift'
        $actualExit = Invoke-DiagnosticEntry
        $actualExit | Should -Be 3
        Should -Invoke Invoke-DiagnosticPython -Times 0 -Exactly
    }

    It 'stops on a runtime source hash mismatch' {
        $global:DiagnosticTestMode = 'source-drift'
        $actualExit = Invoke-DiagnosticEntry -RunOnce
        $actualExit | Should -Be 3
        Should -Invoke Invoke-DiagnosticPython -Times 0 -Exactly
    }

    It 'stops on a runtime source size mismatch' {
        $global:DiagnosticTestMode = 'size-drift'
        $actualExit = Invoke-DiagnosticEntry
        $actualExit | Should -Be 3
        Should -Invoke Invoke-DiagnosticPython -Times 0 -Exactly
    }

    It 'reports missing runtime inputs without invoking Python' {
        $global:DiagnosticTestMode = 'missing'
        $actualExit = Invoke-DiagnosticEntry
        $actualExit | Should -Be 3
        Should -Invoke Invoke-DiagnosticPython -Times 0 -Exactly
    }

    It 'reports an invocation error and never retries' {
        $global:DiagnosticTestMode = 'invoke-error'
        $actualExit = Invoke-DiagnosticEntry
        $actualExit | Should -Be 3
        Should -Invoke Invoke-DiagnosticPython -Times 1 -Exactly
    }

    AfterEach {
        Remove-Variable DiagnosticTestArgs,DiagnosticTestMode,DiagnosticTestChildExit -Scope Global
    }
}

Describe 'Literal synthetic Python boundary' {
    It 'transfers a path and argument with shell characters without changing exit status' {
        $peer = Join-Path $TestDrive 'synthetic peer & literal.py'
        'import json,sys; from pathlib import Path; Path(__file__).with_suffix(".json").write_text(json.dumps(sys.argv[1:])); print("synthetic output"); sys.exit(7)' | Set-Content -LiteralPath $peer
        $literal = 'a & echo NOT_EXECUTED $([literal])'
        $code = Invoke-DiagnosticPython -Python 'C:\Program Files\Python310\python.exe' -Entry $peer -Mode $literal
        $code | Should -Be 7
        $arguments = @(Get-Content -LiteralPath ([IO.Path]::ChangeExtension($peer, '.json')) -Raw | ConvertFrom-Json)
        @($arguments).Count | Should -Be 1
        $arguments[0] | Should -Be $literal
    }
}

Describe 'Real entrypoint preparation stop' {
    It 'returns the preparation exit and preserves the occupied reservation without dispatch' {
        $trial = 'C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic'
        $latch = Join-Path $trial 'launch-invocation.json'
        $before = (Get-FileHash -LiteralPath $latch).Hash
        & $script:entry
        $LASTEXITCODE | Should -Be 3
        (Get-FileHash -LiteralPath $latch).Hash | Should -Be $before
        Test-Path -LiteralPath (Join-Path $trial 'native-001') | Should -BeFalse
        Test-Path -LiteralPath (Join-Path $trial 'run') | Should -BeFalse
    }
}
