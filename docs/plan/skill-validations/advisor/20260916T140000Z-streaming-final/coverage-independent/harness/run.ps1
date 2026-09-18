param(
    [Parameter(Mandatory = $true)][string] $Module,
    [Parameter(Mandatory = $true)][string] $Target,
    [Parameter(Mandatory = $true)][string] $Tests,
    [Parameter(Mandatory = $true)][string] $CaseRoot,
    [Parameter(Mandatory = $true)][string] $FakePython,
    [Parameter(Mandatory = $true)][string] $FakeScript,
    [Parameter(Mandatory = $true)][string] $MissingPython,
    [Parameter(Mandatory = $true)][string] $Output
)

$ErrorActionPreference = 'Stop'
$startedUtc = [DateTime]::UtcNow.ToString('o')
$sourceHashBefore = (Get-FileHash -Algorithm SHA256 -LiteralPath $Target).Hash.ToLowerInvariant()
$env:ADVISOR_LAUNCHER = (Resolve-Path -LiteralPath $Target).Path
$env:ADVISOR_CASE_ROOT = (Resolve-Path -LiteralPath $CaseRoot).Path
$env:ADVISOR_FAKE_PYTHON = (Resolve-Path -LiteralPath $FakePython).Path
$env:ADVISOR_FAKE_SCRIPT = (Resolve-Path -LiteralPath $FakeScript).Path
$env:ADVISOR_MISSING_PYTHON = $MissingPython

Remove-Module Pester -Force -ErrorAction SilentlyContinue
Import-Module -Name $Module -Force
$major = (Get-Module Pester).Version.Major

if ($major -ge 5) {
    $configuration = New-PesterConfiguration
    $configuration.Run.Path = @($Tests)
    $configuration.Run.PassThru = $true
    $configuration.Output.Verbosity = 'Detailed'
    $configuration.CodeCoverage.Enabled = $true
    $configuration.CodeCoverage.Path = @($Target)
    # These tests have no registry behavior. Disable Pester's registry test drive
    # because this managed host does not grant the required registry write.
    $configuration.TestRegistry.Enabled = $false
    $result = Invoke-Pester -Configuration $configuration
    $hit = @($result.CodeCoverage.CommandsExecuted)
    $missed = @($result.CodeCoverage.CommandsMissed)
}
else {
    $result = Invoke-Pester -Script $Tests -CodeCoverage $Target -PassThru
    $hit = @($result.CodeCoverage.HitCommands)
    $missed = @($result.CodeCoverage.MissedCommands)
}

$all = @($hit) + @($missed)
$allLines = @($all | ForEach-Object { [int]$_.Line } | Sort-Object -Unique)
$missedLines = @($missed | ForEach-Object { [int]$_.Line } | Sort-Object -Unique)
$hitLines = @($allLines | Where-Object { $_ -notin $missedLines })
$sourceHashAfter = (Get-FileHash -Algorithm SHA256 -LiteralPath $Target).Hash.ToLowerInvariant()
$record = [ordered]@{
    schema_version = 'advisor-launcher-pester-coverage-v1'
    started_utc = $startedUtc
    finished_utc = [DateTime]::UtcNow.ToString('o')
    shell_path = (Get-Process -Id $PID).Path
    shell_version = $PSVersionTable.PSVersion.ToString()
    pester_module = (Resolve-Path -LiteralPath $Module).Path
    pester_version = (Get-Module Pester).Version.ToString()
    execution_policy = [ordered]@{
        process = (Get-ExecutionPolicy -Scope Process)
        current_user = (Get-ExecutionPolicy -Scope CurrentUser)
        local_machine = (Get-ExecutionPolicy -Scope LocalMachine)
    }
    target = (Resolve-Path -LiteralPath $Target).Path
    target_sha256_before = $sourceHashBefore
    target_sha256_after = $sourceHashAfter
    target_unchanged = ($sourceHashBefore -eq $sourceHashAfter)
    tests_passed = [int]$result.PassedCount
    tests_failed = [int]$result.FailedCount
    tests_skipped = [int]$result.SkippedCount
    commands_executed = [int]$hit.Count
    commands_missed = [int]$missed.Count
    executable_lines = $allLines
    executed_lines = $hitLines
    missed_lines = $missedLines
    executed_line_numerator = [int]$hitLines.Count
    executed_line_denominator = [int]$allLines.Count
    executed_line_percent = if ($allLines.Count) { 100.0 * $hitLines.Count / $allLines.Count } else { 0.0 }
    test_registry_enabled = if ($major -ge 5) { $false } else { $null }
    execution_policy_bypass_used = $false
}
$record | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Output -Encoding UTF8
$record | ConvertTo-Json -Depth 6
if ($result.FailedCount -or $result.SkippedCount -or $missed.Count -or -not $record.target_unchanged) { exit 1 }
exit 0
