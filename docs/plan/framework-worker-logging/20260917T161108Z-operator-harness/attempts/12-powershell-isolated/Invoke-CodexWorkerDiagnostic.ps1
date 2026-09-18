<#
.SYNOPSIS
Prepare the selected diagnostic, or explicitly dispatch its single native preflight.
.DESCRIPTION
Default mode collects read-only Rust preparation evidence. -RunOnce consumes the
one selected attempt. It never retries. Rust owns worker admission and containment.
#>
[CmdletBinding()]
param([switch]$RunOnce)

function Invoke-DiagnosticPython {
    param([string]$Python, [string]$Entry, [string]$Mode)
    $PSNativeCommandUseErrorActionPreference = $false
    & $Python -B -X utf8 $Entry $Mode | Out-Host
    return $LASTEXITCODE
}

function Invoke-DiagnosticEntry {
    param([switch]$RunOnce)
    Set-StrictMode -Version Latest
    $ErrorActionPreference = 'Stop'
    $package = Join-Path $PSScriptRoot 'docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic\operator-harness-001'
    $manifest = Join-Path $package 'runtime-manifest.json'
    $manifestSha256 = 'd127e55a2f2f24f8a3460e486b18c529145813d753559755627810472651d869'
    $python = 'C:\Program Files\Python310\python.exe'
    $entry = Join-Path $package 'diagnostic.py'

    try {
        if ((Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() -cne $manifestSha256) {
            throw 'Runtime manifest changed; retain the files and report the drift.'
        }
        $bindings = Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
        foreach ($binding in $bindings) {
            $actual = Get-FileHash -LiteralPath $binding.path -Algorithm SHA256
            if ($actual.Hash.ToLowerInvariant() -cne $binding.sha256 -or (Get-Item -LiteralPath $binding.path).Length -ne $binding.bytes) {
                throw "Runtime binding changed: $($binding.path)"
            }
        }
        $mode = '--prepare'
        if ($RunOnce) {
            $mode = '--run-once'
        }
        Write-Host "Diagnostic mode: $mode"
        Write-Host "Support module: $entry"
        Write-Host 'Rust total: 120 seconds. Recorder: 145 seconds. Automatic retries: 0.'
        $result = Invoke-DiagnosticPython -Python $python -Entry $entry -Mode $mode
        Write-Host "Diagnostic harness exit code: $result"
        return $result
    }
    catch {
        Write-Error -Message "Preparation stopped: $($_.Exception.Message)" -ErrorAction Continue
        return 3
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    exit (Invoke-DiagnosticEntry -RunOnce:$RunOnce)
}
