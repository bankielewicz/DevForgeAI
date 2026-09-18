param([Parameter(Mandatory=$true)][string]$Path)
$ErrorActionPreference = 'Stop'
Import-Module PSScriptAnalyzer -RequiredVersion 1.25.0
$issues = @(Invoke-ScriptAnalyzer -Path $Path -Severity Error,Warning)
$issues | Select-Object RuleName,Severity,Line,Message | ConvertTo-Json -Depth 5
if ($issues.Count -gt 0) { exit 1 }
Write-Output '{"status":"PASS","errors":0,"warnings":0}'
exit 0
