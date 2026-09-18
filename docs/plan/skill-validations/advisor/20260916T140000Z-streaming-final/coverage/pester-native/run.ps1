param(
    [Parameter(Mandatory = $true)][string] $Module,
    [Parameter(Mandatory = $true)][string] $Target,
    [Parameter(Mandatory = $true)][string] $Tests,
    [Parameter(Mandatory = $true)][string] $Output
)

$ErrorActionPreference = 'Stop'
Remove-Module Pester -Force -ErrorAction SilentlyContinue
Import-Module -Name $Module -Force
$major = (Get-Module Pester).Version.Major

if ($major -ge 5) {
    $configuration = New-PesterConfiguration
    $configuration.Run.Path = @($Tests)
    $configuration.Run.PassThru = $true
    $configuration.Output.Verbosity = 'None'
    $configuration.CodeCoverage.Enabled = $true
    $configuration.CodeCoverage.Path = @($Target)
    $configuration.TestRegistry.Enabled = $false
    $result = Invoke-Pester -Configuration $configuration
    $hit = @($result.CodeCoverage.CommandsExecuted)
    $missed = @($result.CodeCoverage.CommandsMissed)
}
else {
    $result = Invoke-Pester -Script $Tests -CodeCoverage $Target -PassThru -Quiet
    $hit = @($result.CodeCoverage.HitCommands)
    $missed = @($result.CodeCoverage.MissedCommands)
}

$all = @($hit) + @($missed)
$allLines = @($all | ForEach-Object { [int]$_.Line } | Sort-Object -Unique)
$missedLines = @($missed | ForEach-Object { [int]$_.Line } | Sort-Object -Unique)
$hitLines = @($allLines | Where-Object { $_ -notin $missedLines })
$record = [ordered]@{
    schema_version = 'advisor-launcher-pester-coverage-v1'
    shell_version = $PSVersionTable.PSVersion.ToString()
    pester_version = (Get-Module Pester).Version.ToString()
    target = (Resolve-Path -LiteralPath $Target).Path
    tests_passed = [int]$result.PassedCount
    tests_failed = [int]$result.FailedCount
    commands_executed = [int]$hit.Count
    commands_missed = [int]$missed.Count
    executable_lines = $allLines
    executed_lines = $hitLines
    missed_lines = $missedLines
    executed_line_numerator = [int]$hitLines.Count
    executed_line_denominator = [int]$allLines.Count
    executed_line_percent = if ($allLines.Count) { 100.0 * $hitLines.Count / $allLines.Count } else { 0.0 }
    test_registry_enabled = if ($major -ge 5) { $false } else { $null }
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Output -Encoding UTF8
$record | ConvertTo-Json -Depth 5
if ($result.FailedCount -or $missed.Count) { exit 1 }
exit 0
