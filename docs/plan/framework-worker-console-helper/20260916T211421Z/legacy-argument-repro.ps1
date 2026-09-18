# Reproduce the prior argument-builder failure without starting any worker.
$ErrorActionPreference = 'Continue'
$policyPath = 'C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-snapshot\src\restrictive-launch-policy.json'
$policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
$launch = [System.Diagnostics.ProcessStartInfo]::new()
foreach ($argument in $policy.argv) {
    $launch.ArgumentList.Add([string]$argument)
}
$actualCount = 0
if ($null -ne $launch.ArgumentList) {
    $actualCount = $launch.ArgumentList.Count
}
[pscustomobject]@{
    shell = $PSVersionTable.PSVersion.ToString()
    expected_arguments = 116
    actual_arguments = $actualCount
    worker_started = $false
} | ConvertTo-Json
if ($actualCount -ne 116) {
    throw 'Expected 116 arguments before allowing a worker launch; observed zero.'
}
