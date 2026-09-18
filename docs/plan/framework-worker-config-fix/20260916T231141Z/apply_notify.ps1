#requires -Version 7
# Apply only the reviewed deletion, retaining the original file's ACL and a backup.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$configPath = 'C:\Users\bryan\.codex\config.toml'
$backupPath = 'C:\Users\bryan\.codex\config.toml.before-history-notify-fix-20260916T231141Z.bak'
$plan = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'prepared-change.json') -Raw | ConvertFrom-Json
if ($plan.config -cne $configPath -or $plan.backup -cne $backupPath) {
    throw 'Unexpected repair paths.'
}

function Get-BytesHash([byte[]] $Bytes) {
    return [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}

# Refuse concurrent access while checking, backing up, and writing the file.
$stream = [System.IO.File]::Open($configPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
try {
    $original = [byte[]]::new([int] $stream.Length)
    $stream.ReadExactly($original, 0, $original.Length)
    if ((Get-BytesHash $original) -cne $plan.before_sha256) {
        throw 'Config changed since preparation; nothing was changed.'
    }
    $offset = [int] $plan.remove_byte_offset
    $removed = [int] $plan.remove_byte_length
    $corrected = [byte[]]::new($original.Length - $removed)
    [Buffer]::BlockCopy($original, 0, $corrected, 0, $offset)
    [Buffer]::BlockCopy($original, $offset + $removed, $corrected, $offset, $original.Length - $offset - $removed)
    if ((Get-BytesHash $corrected) -cne $plan.after_sha256) {
        throw 'Prepared output digest mismatch; nothing was changed.'
    }
    $backup = [System.IO.File]::Open($backupPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    try {
        $backup.Write($original, 0, $original.Length)
        $backup.Flush($true)
    }
    finally {
        $backup.Dispose()
    }
    if ((Get-FileHash -LiteralPath $backupPath -Algorithm SHA256).Hash -ine $plan.before_sha256) {
        throw 'Backup verification failed; config was not changed.'
    }
    try {
        $stream.Position = 0
        $stream.Write($corrected, 0, $corrected.Length)
        $stream.SetLength($corrected.Length)
        $stream.Flush($true)
        $stream.Position = 0
        $readback = [byte[]]::new($corrected.Length)
        $stream.ReadExactly($readback, 0, $readback.Length)
        if ((Get-BytesHash $readback) -cne $plan.after_sha256) {
            throw 'Config readback mismatch.'
        }
    }
    catch {
        $stream.Position = 0
        $stream.Write($original, 0, $original.Length)
        $stream.SetLength($original.Length)
        $stream.Flush($true)
        throw
    }
}
finally {
    $stream.Dispose()
}
[pscustomobject]@{
    config = $configPath
    backup = $backupPath
    removed_original_line = 90
    top_level_notify_unchanged = $true
    after_sha256 = $plan.after_sha256
} | ConvertTo-Json
