# WSL Restore Script
# Run from PowerShell after fresh WSL install

param(
    [string]$BackupDir = ""
)

Write-Host "=== WSL Restore Script ===" -ForegroundColor Cyan

# Find backup directory if not specified
if (-not $BackupDir) {
    $backups = Get-ChildItem "$env:USERPROFILE\wsl-backup-*" -Directory | Sort-Object LastWriteTime -Descending
    if ($backups.Count -eq 0) {
        Write-Host "No backup directories found in $env:USERPROFILE" -ForegroundColor Red
        Write-Host "Usage: .\restore-wsl.ps1 -BackupDir 'C:\path\to\backup'" -ForegroundColor Yellow
        exit 1
    }
    $BackupDir = $backups[0].FullName
    Write-Host "Using most recent backup: $BackupDir" -ForegroundColor Yellow
}

if (-not (Test-Path $BackupDir)) {
    Write-Host "Backup directory not found: $BackupDir" -ForegroundColor Red
    exit 1
}

# Get WSL username
$wslUser = wsl whoami 2>$null
if (-not $wslUser) {
    Write-Host "WSL not running. Start WSL first and complete initial setup." -ForegroundColor Red
    exit 1
}
$wslUser = $wslUser.Trim()
$wslHome = "\\wsl$\Ubuntu\home\$wslUser"

Write-Host "Restoring to user: $wslUser" -ForegroundColor Yellow
Write-Host "WSL home: $wslHome" -ForegroundColor Yellow

# Items to restore
$itemsToRestore = @(
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
    ".local",
    ".config"
)

$restored = @()
$skipped = @()

foreach ($item in $itemsToRestore) {
    $sourcePath = Join-Path $BackupDir $item

    if (Test-Path $sourcePath) {
        try {
            $destPath = Join-Path $wslHome $item
            $parentDir = Split-Path $destPath -Parent

            if (-not (Test-Path $parentDir)) {
                New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
            }

            # Remove existing if present
            if (Test-Path $destPath) {
                Remove-Item -Path $destPath -Recurse -Force
            }

            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            $restored += $item
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

# Fix SSH permissions (WSL requires strict permissions)
Write-Host "`nFixing SSH permissions..." -ForegroundColor Yellow
wsl chmod 700 ~/.ssh 2>$null
wsl chmod 600 ~/.ssh/* 2>$null
wsl chmod 644 ~/.ssh/*.pub 2>$null
Write-Host "  [OK] SSH permissions fixed" -ForegroundColor Green

# Show package restore instructions
$packageFile = Join-Path $BackupDir "installed-packages.txt"
if (Test-Path $packageFile) {
    Write-Host "`n=== Package Restore ===" -ForegroundColor Cyan
    Write-Host "To restore packages, run in WSL:" -ForegroundColor Yellow
    Write-Host "  sudo dpkg --set-selections < /mnt/c/Users/$env:USERNAME/$(Split-Path $BackupDir -Leaf)/installed-packages.txt" -ForegroundColor White
    Write-Host "  sudo apt-get dselect-upgrade" -ForegroundColor White
}

# Summary
Write-Host "`n=== Restore Summary ===" -ForegroundColor Cyan
Write-Host "Restored: $($restored.Count) items" -ForegroundColor Green
Write-Host "Skipped (not in backup): $($skipped.Count) items" -ForegroundColor Gray

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Restart WSL: wsl --shutdown && wsl" -ForegroundColor White
Write-Host "2. Verify configs: ls -la ~/" -ForegroundColor White
Write-Host "3. Test git: git config --list" -ForegroundColor White
Write-Host "4. Resume work: cd /mnt/c/Projects/DevForgeAI2" -ForegroundColor White
