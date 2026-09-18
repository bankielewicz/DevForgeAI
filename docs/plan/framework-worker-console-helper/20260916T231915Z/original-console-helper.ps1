#requires -Version 5.1
<#
.SYNOPSIS
Runs the pinned Codex app-server in this console and displays its startup errors.
.DESCRIPTION
Uses the frozen diagnostic launch arguments and a fresh copy of the fixture.
Windows PowerShell 5.1 automatically delegates to the installed PowerShell 7.
Output stays attached to the console; no protocol input, thread, turn, or retry
is sent. Press Ctrl+C to stop a server that remains running.

This manual diagnostic does not run the Rust probe's Job Object/preflight checks
and cannot establish framework acceptance. It does not change installed config.
.PARAMETER CheckOnly
Checks the shell, saved inputs, executable hash, and argument construction without
starting Codex or creating a runtime directory.
.EXAMPLE
.\Start-CodexAppServerDiagnostic.ps1
.EXAMPLE
.\Start-CodexAppServerDiagnostic.ps1 -CheckOnly
#>
[CmdletBinding()]
param(
    [switch] $CheckOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ArgumentList is unavailable in Windows PowerShell 5.1. Never fall through to
# a launch with an empty argument list, which would open interactive Codex.
if ($PSVersionTable.PSVersion.Major -lt 7) {
    $powerShell7 = 'C:\Program Files\PowerShell\7\pwsh.exe'
    if (-not (Test-Path -LiteralPath $powerShell7 -PathType Leaf)) {
        throw "PowerShell 7 was not found at $powerShell7. Nothing was launched."
    }
    $forwardedArguments = @('-NoLogo', '-NoProfile', '-File', $PSCommandPath)
    if ($CheckOnly) {
        $forwardedArguments += '-CheckOnly'
    }
    & $powerShell7 @forwardedArguments
    exit $LASTEXITCODE
}

if (-not $IsWindows) {
    throw 'This diagnostic requires native Windows. Nothing was launched.'
}

function Assert-FileDigest {
    param(
        [string] $LiteralPath,
        [string] $ExpectedSha256,
        [string] $Label
    )
    $actual = (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash
    if ($actual -ine $ExpectedSha256) {
        throw "$Label SHA256 mismatch. Nothing was launched."
    }
}

$snapshot = Join-Path $PSScriptRoot 'docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-snapshot\src'
$identityPath = Join-Path $snapshot 'native-executable-identity.json'
$policyPath = Join-Path $snapshot 'restrictive-launch-policy.json'
$fixturePath = Join-Path $PSScriptRoot 'docs\plan\framework-worker-trials\20260916T202125Z-diagnostic\fixture\task.json'

Assert-FileDigest $policyPath '1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5' 'Saved launch policy'
Assert-FileDigest $identityPath '0ddc66d726e8d862366a135170fdc82206858d48f1b343b898e671de352ae45d' 'Saved executable identity'
Assert-FileDigest $fixturePath 'b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a' 'Saved fixture'

$identity = Get-Content -LiteralPath $identityPath -Raw | ConvertFrom-Json
$policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
Assert-FileDigest $identity.physical_executable $identity.executable_sha256 'Pinned Codex executable'

if ($policy.argv.Count -ne 116 -or $policy.argv[0] -cne 'app-server') {
    throw 'Expected the 116 saved app-server arguments. Nothing was launched.'
}

$launch = [System.Diagnostics.ProcessStartInfo]::new()
$launch.FileName = $identity.physical_executable
$launch.UseShellExecute = $false
foreach ($argument in $policy.argv) {
    $launch.ArgumentList.Add([string] $argument)
}
if ($launch.ArgumentList.Count -ne 116 -or $launch.ArgumentList[0] -cne 'app-server') {
    throw 'Argument construction failed. Nothing was launched.'
}
for ($argumentIndex = 0; $argumentIndex -lt $policy.argv.Count; $argumentIndex++) {
    if ($launch.ArgumentList[$argumentIndex] -cne $policy.argv[$argumentIndex]) {
        throw 'An argument changed during construction. Nothing was launched.'
    }
}

# Modify only this child's environment, matching the retained manual command.
[void] $launch.Environment.Remove('ANTHROPIC_API_KEY')

if ($CheckOnly) {
    [pscustomobject]@{
        powershell_version = $PSVersionTable.PSVersion.ToString()
        executable = $launch.FileName
        executable_sha256 = $identity.executable_sha256
        argument_count = $launch.ArgumentList.Count
        argv = @($launch.ArgumentList)
        child_only_removed_environment_names = @('ANTHROPIC_API_KEY')
        worker_started = $false
    } | ConvertTo-Json -Depth 4
    exit 0
}

$runName = 'manual-console-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [guid]::NewGuid().ToString('N')
$runPath = Join-Path $PSScriptRoot ('docs\plan\framework-worker-trials\' + $runName)
$work = New-Item -ItemType Directory -Path $runPath
Copy-Item -LiteralPath $fixturePath -Destination (Join-Path $work.FullName 'task.json')
$launch.WorkingDirectory = $work.FullName

Write-Host "PowerShell $($PSVersionTable.PSVersion); 116 saved app-server arguments verified."
Write-Host "Working directory: $($work.FullName)"
Write-Host 'Startup output follows. If the server stays running silently, press Ctrl+C to stop it.'

$worker = $null
$workerExitCode = 1
try {
    # Inherit console stdin/stdout/stderr. Do not redirect or send protocol input.
    $worker = [System.Diagnostics.Process]::Start($launch)
    if ($null -eq $worker) {
        throw 'Windows did not return a worker process handle.'
    }
    # Short waits let PowerShell process Ctrl+C and enter the cleanup block.
    while (-not $worker.WaitForExit(200)) {
        # No retries, input, or protocol activity.
    }
    $workerExitCode = $worker.ExitCode
    Write-Host "Codex app-server exit code: $workerExitCode"
}
finally {
    if ($null -ne $worker) {
        try {
            if (-not $worker.HasExited) {
                # Stop only the process tree owned by this invocation.
                $worker.Kill($true)
                if (-not $worker.WaitForExit(5000)) {
                    Write-Warning "Worker PID $($worker.Id) has not confirmed exit after cleanup."
                }
            }
        }
        finally {
            $worker.Dispose()
        }
    }
}

exit $workerExitCode
