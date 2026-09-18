$ErrorActionPreference = 'Stop'
$evidenceRoot = $PSScriptRoot
$workspaceRoot = 'C:\Projects\DevForgeAI'
$sourceRoot = Join-Path $workspaceRoot 'src\agents\skills\advisor'
$installedRoot = Join-Path $workspaceRoot '.agents\skills\advisor'
$backupRoot = Join-Path $evidenceRoot 'installed-before'
$checks = Get-Content -Raw -LiteralPath (Join-Path $evidenceRoot 'source-checks.json') | ConvertFrom-Json
$sourceManifestPath = Join-Path $sourceRoot 'artifact-manifest.json'
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $sourceManifestPath).Hash.ToLowerInvariant() -ne $checks.source_manifest_sha256) { throw 'Validated manifest drifted' }
$manifest = Get-Content -Raw -LiteralPath $sourceManifestPath | ConvertFrom-Json
foreach ($entry in $manifest.files.PSObject.Properties) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $sourceRoot $entry.Name)).Hash.ToLowerInvariant() -ne $entry.Value) { throw "Source drift: $($entry.Name)" }
}
$appliedPaths = [System.Collections.Generic.List[string]]::new()
$installStatus = 'INCOMPLETE'
try {
    $paths = @($checks.changed_files | Where-Object { $_ -ne 'artifact-manifest.json' }) + @('artifact-manifest.json')
    foreach ($relativePath in $paths) {
        $destinationPath = [IO.Path]::GetFullPath((Join-Path $installedRoot $relativePath))
        if (-not $destinationPath.StartsWith($installedRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Destination outside installed advisor' }
        $backupPath = Join-Path $backupRoot $relativePath
        if (Test-Path -LiteralPath $backupPath) {
            if (-not (Test-Path -LiteralPath $destinationPath)) { throw "Installed file disappeared: $relativePath" }
            if ((Get-FileHash -Algorithm SHA256 -LiteralPath $destinationPath).Hash -ne (Get-FileHash -Algorithm SHA256 -LiteralPath $backupPath).Hash) { throw "Installed drift: $relativePath" }
        } elseif (Test-Path -LiteralPath $destinationPath) { throw "New destination already exists: $relativePath" }
        $sourcePath = Join-Path $sourceRoot $relativePath
        Copy-Item -LiteralPath $sourcePath -Destination $destinationPath
        $appliedPaths.Add($relativePath)
        if ((Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash -ne (Get-FileHash -Algorithm SHA256 -LiteralPath $destinationPath).Hash) { throw "Readback mismatch: $relativePath" }
    }
    foreach ($entry in $manifest.files.PSObject.Properties) {
        if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $installedRoot $entry.Name)).Hash.ToLowerInvariant() -ne $entry.Value) { throw "Installed manifest mismatch: $($entry.Name)" }
    }
    $installStatus = 'COPIED_AND_HASH_VERIFIED'
} finally {
    $receipt = [ordered]@{status=$installStatus; source=$sourceRoot; destination=$installedRoot; backup=$backupRoot; applied_paths=@($appliedPaths.ToArray()); source_manifest_sha256=$checks.source_manifest_sha256; framework_acceptance='NOT_EVALUATED'}
    $receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $evidenceRoot 'installation.json') -Encoding utf8
    $receipt | ConvertTo-Json -Depth 5
}
