$ErrorActionPreference = 'Stop'
$rcaRoot = $PSScriptRoot
$sourceManifestPath = Join-Path $rcaRoot 'source-manifest.json'
$sourceManifest = Get-Content -LiteralPath $sourceManifestPath -Raw | ConvertFrom-Json
$inputResults = @()
foreach ($entry in $sourceManifest.files) {
    $snapshot = Join-Path $rcaRoot $entry.snapshot
    $snapshotHash = (Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash.ToLowerInvariant()
    $currentHash = (Get-FileHash -LiteralPath $entry.source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($snapshotHash -ne $entry.sha256 -or $currentHash -ne $entry.sha256) {
        throw "Source or snapshot changed: $($entry.source)"
    }
    $inputResults += [ordered]@{ source = $entry.source; sha256 = $currentHash; snapshot_matches = $true; source_matches = $true }
}
$reportPath = Join-Path $rcaRoot 'analysis.md'
$reportBytes = [System.IO.File]::ReadAllBytes($reportPath)
$report = [System.Text.Encoding]::UTF8.GetString($reportBytes)
$linkResults = @()
foreach ($match in [regex]::Matches($report, '\[[^\]]+\]\(([^)]+)\)')) {
    $link = $match.Groups[1].Value
    if ([System.IO.Path]::IsPathRooted($link) -or $link -match '^https?:') {
        throw "Unexpected nonlocal report link: $link"
    }
    $target = Join-Path $rcaRoot $link
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw "Missing report link: $link" }
    $linkResults += $link
}
$resultRows = Get-Content -LiteralPath (Join-Path $rcaRoot 'inputs\18-results-001.jsonl') | ForEach-Object { $_ | ConvertFrom-Json }
$counts = @($resultRows | Group-Object kind,result | ForEach-Object { [ordered]@{ kind_and_result = $_.Name; count = $_.Count } })
$record = [ordered]@{
    record_kind = 'rca_document_review'
    recorded_utc = (Get-Date -AsUTC).ToString('o')
    cwd = (Get-Location).Path
    shell_version = $PSVersionTable.PSVersion.ToString()
    command = '& .\docs\plan\root-cause-analyses\qa-completion\20260914T2024442802835Z\review.ps1'
    source_readback = $inputResults
    resolved_report_links = @($linkResults | Sort-Object -Unique)
    retained_result_counts = $counts
    review_scope = 'Source/snapshot hashes, document link existence, retained result inventory counts. Requirement/causal review performed in the RCA prose; no skill or product campaign executed.'
    manual_review = 'Checked chronology versus source timestamps, authored-versus-evaluated distinction, uncertainty of timeout cause, existing dev safeguards, terminal-only proposal boundaries, ownership and nonexecuted acceptance cases.'
    runtime_testing = 'NOT_PERFORMED'
    skill_validation = 'NOT_PERFORMED'
    prevention_implementation = 'NOT_PERFORMED'
}
$reviewPath = Join-Path $rcaRoot 'review.json'
if (Test-Path -LiteralPath $reviewPath) { throw 'Retain previous receipt; select a fresh review attempt.' }
$reviewBytes = [System.Text.Encoding]::UTF8.GetBytes(($record | ConvertTo-Json -Depth 8))
[System.IO.File]::WriteAllBytes($reviewPath, $reviewBytes)
$reread = [System.IO.File]::ReadAllBytes($reviewPath)
if ([Convert]::ToBase64String($reread) -ne [Convert]::ToBase64String($reviewBytes)) { throw 'Review readback mismatch' }
$artifacts = @('analysis.md','capture.py','review.ps1','source-manifest.json','review.json') | ForEach-Object {
    $filePath = Join-Path $rcaRoot $_
    [ordered]@{ path = $_; bytes = (Get-Item -LiteralPath $filePath).Length; sha256 = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant() }
}
$artifactPath = Join-Path $rcaRoot 'artifact-manifest.json'
if (Test-Path -LiteralPath $artifactPath) { throw 'Artifact manifest already exists' }
$artifactBytes = [System.Text.Encoding]::UTF8.GetBytes(($artifacts | ConvertTo-Json -Depth 4))
[System.IO.File]::WriteAllBytes($artifactPath, $artifactBytes)
if ([Convert]::ToBase64String([System.IO.File]::ReadAllBytes($artifactPath)) -ne [Convert]::ToBase64String($artifactBytes)) { throw 'Artifact manifest readback mismatch' }
[ordered]@{ selected_inputs_unchanged = $inputResults.Count; unique_links_resolved = @($linkResults | Sort-Object -Unique).Count; result_counts = $counts; artifact_manifest = $artifactPath; artifact_manifest_sha256 = (Get-FileHash -LiteralPath $artifactPath -Algorithm SHA256).Hash.ToLowerInvariant() } | ConvertTo-Json -Depth 5
