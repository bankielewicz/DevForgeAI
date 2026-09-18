#requires -Version 5.1

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $Request,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $Briefing,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string] $RunDir,

    [ValidateSet('initial', 'context', 'citation', 'reconcile', 'retry')]
    [string] $Reason = 'initial',

    [ValidateNotNullOrEmpty()]
    [string] $Python = 'python',

    [switch] $ShowProgress
)

$runner = Join-Path -Path $PSScriptRoot -ChildPath 'advisor_run.py'
$runnerArguments = @(
    '-B',
    '-X',
    'utf8',
    $runner,
    'run',
    '--request',
    $Request,
    '--briefing',
    $Briefing,
    '--run-dir',
    $RunDir,
    '--reason',
    $Reason
)
if ($ShowProgress) {
    $runnerArguments += '--show-progress'
}

$ErrorActionPreference = 'Stop'
try {
    & $Python @runnerArguments
    $childExitCode = $LASTEXITCODE
    if ($null -eq $childExitCode) {
        throw 'Python invocation returned no native process exit status.'
    }
    exit ([int] $childExitCode)
}
catch {
    [Console]::Error.WriteLine('advisor launcher failed: {0}', $_.Exception.Message)
    exit 2
}
