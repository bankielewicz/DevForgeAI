param([Parameter(Mandatory)][string]$EvidencePath)
$ErrorActionPreference = 'Stop'
Import-Module 'C:\Users\bryan\OneDrive\Documents\PowerShell\Modules\Pester\5.7.1\Pester.psd1'
$config = New-PesterConfiguration
$config.Run.Path = Join-Path $PSScriptRoot 'tests\OperatorHarness.Tests.ps1'
$config.Run.PassThru = $true
$config.Output.Verbosity = 'Detailed'
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = 'C:\Projects\DevForgeAI\Invoke-CodexWorkerDiagnostic.ps1'
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = Join-Path $EvidencePath 'coverage.xml'
$config.TestResult.Enabled = $true
$config.TestResult.OutputPath = Join-Path $EvidencePath 'tests.xml'
$result = Invoke-Pester -Configuration $config
$result | Export-Clixml -LiteralPath (Join-Path $EvidencePath 'pester-result.clixml') -Depth 8
[pscustomobject]@{
    Total = $result.TotalCount
    Passed = $result.PassedCount
    Failed = $result.FailedCount
    Skipped = $result.SkippedCount
    NotRun = $result.NotRunCount
    PesterVersion = '5.7.1'
    PowerShell = $PSVersionTable.PSVersion.ToString()
    Platform = [Environment]::OSVersion.ToString()
    NativeCodex = 'NOT_RUN'
    FrameworkAcceptance = 'NOT_EVALUATED'
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $EvidencePath 'test-results.json')
if ($null -eq $result -or $result.Result -ne 'Passed' -or $result.TotalCount -ne 9 -or $result.PassedCount -ne 9) { exit 1 }
exit 0
