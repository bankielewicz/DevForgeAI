param($Module, $Target, $Test, $Output)
$ErrorActionPreference = 'Stop'
Remove-Module Pester -Force -ErrorAction SilentlyContinue
Import-Module -LiteralPath $Module -Force
$major = (Get-Module Pester).Version.Major
if ($major -ge 5) {
    $result = Invoke-Pester -Path $Test -CodeCoverage $Target -PassThru -Show None
    $rows = $result.CodeCoverage.CommandsMissed
    $passed = $result.PassedCount
    $failed = $result.FailedCount
}
else {
    $result = Invoke-Pester -Script $Test -CodeCoverage $Target -PassThru -Quiet
    $rows = $result.CodeCoverage.MissedCommands
    $passed = $result.PassedCount
    $failed = $result.FailedCount
}
$record = [ordered]@{
    pester_version = (Get-Module Pester).Version.ToString()
    passed = $passed
    failed = $failed
    commands = @($rows | ForEach-Object {
        [ordered]@{ line = [int]$_.Line; command = [string]$_.Command }
    })
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Output -Encoding UTF8
