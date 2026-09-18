param($Module, $Target, $Test, $Output)
$ErrorActionPreference = 'Stop'
Remove-Module Pester -Force -ErrorAction SilentlyContinue
Import-Module -Name $Module -Force
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
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($Target, [ref]$tokens, [ref]$errors)
$statements = @($ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.StatementAst] }, $true))
$record = [ordered]@{
    pester_version = (Get-Module Pester).Version.ToString()
    passed = $passed
    failed = $failed
    commands = @($rows | ForEach-Object {
        $line = [int]$_.Line
        $parent = @($statements | Where-Object {
            $_.Extent.StartLineNumber -le $line -and $_.Extent.EndLineNumber -ge $line
        } | Sort-Object { $_.Extent.EndLineNumber - $_.Extent.StartLineNumber } | Select-Object -First 1)
        [ordered]@{
            line = $line
            command = [string]$_.Command
            parent_start_line = $(if ($parent) { [int]$parent[0].Extent.StartLineNumber } else { $line })
        }
    })
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Output -Encoding UTF8
