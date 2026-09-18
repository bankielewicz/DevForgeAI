$ErrorActionPreference = 'Stop'
$specPath = 'C:\Projects\DevForgeAI\docs\specs\skill-builder-postmvp-spec.md'
$specBytes = [System.IO.File]::ReadAllBytes($specPath)
$specText = [System.Text.UTF8Encoding]::new($false, $true).GetString($specBytes)
$specHash = (Get-FileHash -LiteralPath $specPath -Algorithm SHA256).Hash.ToLowerInvariant()
$requirementIds = @([regex]::Matches($specText, '(?m)^\*\*(SBP-\d{3})\s') | ForEach-Object { $_.Groups[1].Value })
$scenarioIds = @([regex]::Matches($specText, '(?m)^\| (SBPV-\d{2}) ') | ForEach-Object { $_.Groups[1].Value })
$expectedRequirements = @(1..16 | ForEach-Object { 'SBP-{0:000}' -f $_ })
$expectedScenarios = @(1..18 | ForEach-Object { 'SBPV-{0:00}' -f $_ })
if (($requirementIds -join ',') -cne ($expectedRequirements -join ',')) { throw 'Requirement inventory mismatch' }
if (($scenarioIds -join ',') -cne ($expectedScenarios -join ',')) { throw 'Scenario inventory mismatch' }
$unknownReferences = @([regex]::Matches($specText, '\bSBP-\d{3}\b') | ForEach-Object { $_.Value } | Where-Object { $_ -notin $expectedRequirements })
if ($unknownReferences.Count -gt 0) { throw 'Undefined requirement references' }
$links = @()
foreach ($match in [regex]::Matches($specText, '\[[^\]]+\]\(([^)]+)\)')) {
    $relativeLink = $match.Groups[1].Value
    if ($relativeLink -match '^https?:') { throw 'Unexpected external link requires separate review' }
    $target = [System.IO.Path]::GetFullPath((Join-Path (Split-Path -Parent $specPath) $relativeLink))
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw "Missing linked file: $target" }
    $links += [ordered]@{ reference = $relativeLink; resolved_path = $target; exists = $true }
}
if ($specText -notmatch '(?m)^implementation_status: not_implemented_by_this_document$') { throw 'Missing implementation-status boundary' }
if ($specText -match '(?m)^skill_name:') { throw 'Enhancement document must not enter ordinary skill-name lookup' }
if ([Convert]::ToBase64String([System.IO.File]::ReadAllBytes($specPath)) -cne [Convert]::ToBase64String($specBytes)) { throw 'Specification changed during readback' }
$receipt = [ordered]@{
    record_kind = 'specification_document_review'
    recorded_utc = (Get-Date -AsUTC).ToString('o')
    command = '& .\docs\plan\specification-reviews\skill-builder-postmvp\20260914T2052234323802Z\review.ps1'
    cwd = (Get-Location).Path
    shell_version = $PSVersionTable.PSVersion.ToString()
    scope = 'Documentation-only save and review; no skill implementation or validation'
    specification = [ordered]@{ path = $specPath; bytes = $specBytes.Length; sha256 = $specHash }
    requirement_ids = $requirementIds
    scenario_ids = $scenarioIds
    local_links = $links
    readback = 'IDENTICAL'
    document_checks = 'Completed: UTF-8 decoding, exact requirement/scenario inventories, defined requirement references, local link existence, implementation-status boundary, no skill-name lookup collision, byte readback'
    manual_consistency_review = 'Reviewed design field types, authoring-only versus input-custody checks, legacy and validator packet compatibility, terminal argument semantics, failure/readback handling, requirement-to-scenario mapping, proposed versus implemented claims'
    limitations = 'Link existence and document review do not establish runtime conformance or validation success'
    builder_implementation = 'NOT_PERFORMED'
    runtime_testing = 'NOT_PERFORMED'
    skill_validation = 'NOT_PERFORMED'
    framework_acceptance = 'NOT_EVALUATED'
}
$receiptPath = Join-Path $PSScriptRoot 'review.json'
if (Test-Path -LiteralPath $receiptPath) { throw 'Retain earlier receipt; use a new review attempt' }
$receiptBytes = [System.Text.UTF8Encoding]::new($false).GetBytes(($receipt | ConvertTo-Json -Depth 7))
[System.IO.File]::WriteAllBytes($receiptPath, $receiptBytes)
if ([Convert]::ToBase64String([System.IO.File]::ReadAllBytes($receiptPath)) -cne [Convert]::ToBase64String($receiptBytes)) { throw 'Receipt readback mismatch' }
[ordered]@{ specification = $receipt.specification; requirements = $requirementIds.Count; scenarios = $scenarioIds.Count; local_links = $links.Count; receipt = $receiptPath; readback = 'IDENTICAL' } | ConvertTo-Json -Depth 4
