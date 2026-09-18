#Requires -Version 7.2
<#
.SYNOPSIS
Human-operated Git safety menu and Rust CLI build helper. Run with pwsh.exe.
.EXAMPLE
pwsh -File .\DevForgeAI-Console.ps1 -RepositoryPath C:\Projects\DevForgeAI
.EXAMPLE
pwsh -File .\DevForgeAI-Console.ps1 -Action SyncMain -Approve
#>
[CmdletBinding()]
param(
    [string]$RepositoryPath = $PSScriptRoot,
    [ValidateSet('Menu', 'Status', 'Fetch', 'Checkpoint', 'SyncMain', 'SwitchBranch', 'Worktree', 'Commit', 'Push', 'PullRequests', 'DraftPr', 'Recovery', 'BuildDebug', 'BuildRelease')]
    [string]$Action = 'Menu',
    [string]$Branch,
    [string]$Message,
    [switch]$Approve,
    [switch]$AllowNetwork
)

$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $PSScriptRoot 'scripts/operator-console/OperatorConsole.psm1') -Force
try {
    if ($Action -eq 'Menu') { Start-OperatorMenu -RepositoryPath $RepositoryPath }
    else { Invoke-OperatorAction -RepositoryPath $RepositoryPath -Action $Action -Branch $Branch -Message $Message -Approve:$Approve -AllowNetwork:$AllowNetwork }
}
catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
