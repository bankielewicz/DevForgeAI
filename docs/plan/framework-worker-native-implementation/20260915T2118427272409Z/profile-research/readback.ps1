$ErrorActionPreference = 'Stop'

$paths = @(
    'C:\Users\bryan\.codex\config.toml',
    'C:\Users\bryan\.codex\hooks.json',
    'C:\ProgramData\OpenAI\Codex\config.toml',
    'C:\ProgramData\OpenAI\Codex\requirements.toml',
    'C:\ProgramData\OpenAI\Codex\hooks.json',
    'C:\Projects\DevForgeAI\.codex\config.toml',
    'C:\Projects\DevForgeAI\.codex\hooks.json'
)

$observations = foreach ($path in $paths) {
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        $item = Get-Item -LiteralPath $path
        [ordered]@{
            path = $path
            exists = $true
            bytes = $item.Length
            last_write_utc = $item.LastWriteTimeUtc.ToString('o')
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
        }
    }
    else {
        [ordered]@{
            path = $path
            exists = $false
        }
    }
}

[ordered]@{
    observed_utc = [DateTime]::UtcNow.ToString('o')
    cwd = (Get-Location).Path
    files = $observations
} | ConvertTo-Json -Depth 4
