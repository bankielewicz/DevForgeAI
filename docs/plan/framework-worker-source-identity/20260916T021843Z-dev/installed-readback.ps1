$ErrorActionPreference = 'Stop'
$cache = 'C:\Users\bryan\.codex\plugins\cache'
$rows = [System.Collections.Generic.List[object]]::new()
foreach ($provider in Get-ChildItem -LiteralPath $cache -Force) {
    if (-not $provider.PSIsContainer -or ($provider.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'unexpected provider type' }
    foreach ($plugin in Get-ChildItem -LiteralPath $provider.FullName -Force) {
        if (-not $plugin.PSIsContainer -or ($plugin.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'unexpected plugin type' }
        foreach ($member in Get-ChildItem -LiteralPath $plugin.FullName -Force) {
            $rows.Add([pscustomobject]@{ path=$member.FullName; attributes=[int]$member.Attributes; link_type=$member.LinkType; target=$member.Target })
        }
    }
}
$rows | ConvertTo-Json -Depth 4
& 'C:\Windows\System32\fsutil.exe' reparsepoint query 'C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest'
if ($LASTEXITCODE) { exit $LASTEXITCODE }
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816\.codex-plugin\plugin.json' | ConvertTo-Json
