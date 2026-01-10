# WSL Backup Script
# Run from PowerShell (not as admin required)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = "$env:USERPROFILE\wsl-backup-$timestamp"
$wslHome = "\\wsl$\Ubuntu\home"

# Get WSL username
$wslUser = wsl whoami 2>$null
if (-not $wslUser) {
    Write-Host "WSL not running or no distro installed" -ForegroundColor Red
    exit 1
}
$wslUser = $wslUser.Trim()

Write-Host "=== WSL Backup Script ===" -ForegroundColor Cyan
Write-Host "Backing up user: $wslUser" -ForegroundColor Yellow
Write-Host "Backup location: $backupDir" -ForegroundColor Yellow

# Create backup directory
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Files/folders to backup
$itemsToBackup = @(
    ".bashrc",
    ".bash_profile",
    ".profile",
    ".zshrc",
    ".gitconfig",
    ".ssh",
    ".gnupg",
    ".npmrc",
    ".pypirc",
    ".netrc",
    ".aws",
    ".azure",
    ".kube",
    ".docker",
    ".local/bin",
    ".config"
)

$backedUp = @()
$skipped = @()

foreach ($item in $itemsToBackup) {
    $sourcePath = "$wslHome\$wslUser\$item"

    if (Test-Path $sourcePath) {
        try {
            $destPath = Join-Path $backupDir $item
            $parentDir = Split-Path $destPath -Parent

            if (-not (Test-Path $parentDir)) {
                New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
            }

            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            $backedUp += $item
            Write-Host "  [OK] $item" -ForegroundColor Green
        }
        catch {
            Write-Host "  [FAIL] $item - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        $skipped += $item
    }
}

# Also backup list of installed apt packages
Write-Host "`nBacking up package list..." -ForegroundColor Yellow
$packageList = wsl dpkg --get-selections 2>$null
if ($packageList) {
    $packageList | Out-File -FilePath "$backupDir\installed-packages.txt" -Encoding UTF8
    Write-Host "  [OK] installed-packages.txt" -ForegroundColor Green
}

# Summary
Write-Host "`n=== Backup Summary ===" -ForegroundColor Cyan
Write-Host "Backed up: $($backedUp.Count) items" -ForegroundColor Green
Write-Host "Skipped (not found): $($skipped.Count) items" -ForegroundColor Gray
Write-Host "`nBackup saved to: $backupDir" -ForegroundColor Yellow

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Verify backup: dir '$backupDir'" -ForegroundColor White
Write-Host "2. Unregister WSL: wsl --unregister Ubuntu" -ForegroundColor White
Write-Host "3. Reinstall: wsl --install -d Ubuntu" -ForegroundColor White
Write-Host "4. Restore configs from: $backupDir" -ForegroundColor White
