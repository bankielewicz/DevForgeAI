BeforeAll {
    $script:entry = 'C:\Projects\DevForgeAI\Invoke-CodexWorkerDiagnostic.ps1'
    $script:text = Get-Content -LiteralPath $script:entry -Raw
    $global:DiagnosticTestSeal = [regex]::Match($script:text, "manifestSha256 = '([a-f0-9]{64})'").Groups[1].Value
    $script:fakePath = 'C:\fixture space & literal\module.py'
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
        Mock 'C:\Program Files\Python310\python.exe' {
            $global:DiagnosticTestArgs = @($args)
            if ($global:DiagnosticTestMode -eq 'invoke-error') { throw 'Synthetic process dispatch error' }
            $global:LASTEXITCODE = $global:DiagnosticTestChildExit
        }
    }

    It 'prepares by default with literal module arguments and no native run flag' {
        & $script:entry
        $LASTEXITCODE | Should -Be 0
        $global:DiagnosticTestArgs.Count | Should -Be 5
        $global:DiagnosticTestArgs[0..2] -join ',' | Should -Be '-B,-X,utf8'
        $global:DiagnosticTestArgs[3] | Should -Be 'C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic\operator-harness-001\diagnostic.py'
        $global:DiagnosticTestArgs[4] | Should -Be '--prepare'
        Should -Invoke 'python.exe' -Times 1 -Exactly
    }

    It 'dispatches once only with the explicit switch and preserves nonzero child exit' {
        $global:DiagnosticTestChildExit = 7
        & $script:entry -RunOnce
        $LASTEXITCODE | Should -Be 7
        $global:DiagnosticTestArgs[4] | Should -Be '--run-once'
        Should -Invoke 'python.exe' -Times 1 -Exactly
    }

    It 'stops if the sealed runtime manifest changed' {
        $global:DiagnosticTestMode = 'manifest-drift'
        & $script:entry
        $LASTEXITCODE | Should -Be 3
        Should -Invoke 'python.exe' -Times 0 -Exactly
    }

    It 'stops on a runtime source hash mismatch' {
        $global:DiagnosticTestMode = 'source-drift'
        & $script:entry -RunOnce
        $LASTEXITCODE | Should -Be 3
        Should -Invoke 'python.exe' -Times 0 -Exactly
    }

    It 'stops on a runtime source size mismatch' {
        $global:DiagnosticTestMode = 'size-drift'
        & $script:entry
        $LASTEXITCODE | Should -Be 3
        Should -Invoke 'python.exe' -Times 0 -Exactly
    }

    It 'reports missing runtime inputs without invoking Python' {
        $global:DiagnosticTestMode = 'missing'
        & $script:entry
        $LASTEXITCODE | Should -Be 3
        Should -Invoke 'python.exe' -Times 0 -Exactly
    }

    It 'reports an invocation error and never retries' {
        $global:DiagnosticTestMode = 'invoke-error'
        & $script:entry
        $LASTEXITCODE | Should -Be 3
        Should -Invoke 'python.exe' -Times 1 -Exactly
    }

    AfterEach {
        Remove-Variable DiagnosticTestArgs,DiagnosticTestMode,DiagnosticTestChildExit -Scope Global
    }
}
