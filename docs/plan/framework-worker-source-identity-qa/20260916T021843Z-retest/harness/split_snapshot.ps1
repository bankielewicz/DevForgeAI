$ErrorActionPreference = 'Stop'

$candidate = (Resolve-Path -LiteralPath 'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe').Path
$frozen = (Resolve-Path -LiteralPath 'C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\harness\packages\frozen-package').Path
$matrix = 'C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\harness\packages\qa-negative-matrix'
$allowedRoot = (Resolve-Path -LiteralPath 'C:\Projects\DevForgeAI\docs\plan\framework-worker-source-identity-qa\20260916T021843Z-retest\harness\packages').Path

if (-not $frozen.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'frozen snapshot is outside the QA package root'
}
if (-not $matrix.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'matrix destination is outside the QA package root'
}
if (Test-Path -LiteralPath $matrix) {
    throw 'matrix destination already exists'
}

Move-Item -LiteralPath $frozen -Destination $matrix
Copy-Item -LiteralPath $candidate -Destination $frozen -Recurse

[pscustomobject]@{
    Candidate = $candidate
    Frozen = $frozen
    Matrix = $matrix
    AllowedRoot = $allowedRoot
} | ConvertTo-Json -Compress
