param(
    [Parameter(Mandatory)][ValidateSet('Deny','Restore')][string]$Action,
    [Parameter(Mandatory)][string]$Target,
    [Parameter(Mandatory)][string]$StatePath
)
$ErrorActionPreference = 'Stop'
$TaskRunRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
$TaskTargetPath = [System.IO.Path]::GetFullPath($Target)
$TaskStatePath = [System.IO.Path]::GetFullPath($StatePath)
$TaskControlRoot = Join-Path $TaskRunRoot 'harness-controls'
$TaskDenialTarget = Join-Path $TaskRunRoot 'trials\G02\project\backlog'
if (-not ($TaskTargetPath -eq $TaskDenialTarget -or $TaskTargetPath.StartsWith($TaskControlRoot + '\', [System.StringComparison]::OrdinalIgnoreCase))) { throw 'Target is outside declared synthetic fault roots.' }
if (-not $TaskStatePath.StartsWith($TaskRunRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'ACL state must stay in the validation run.' }
$TaskItem = Get-Item -LiteralPath $TaskTargetPath -Force
if (-not $TaskItem.PSIsContainer -or ($TaskItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) { throw 'Target must be a plain synthetic directory.' }
# Initial control implementation; the executed red test must establish missing denial.
@{ action = $Action; result = 'NO_EFFECT_CONTROL' } | ConvertTo-Json -Compress
