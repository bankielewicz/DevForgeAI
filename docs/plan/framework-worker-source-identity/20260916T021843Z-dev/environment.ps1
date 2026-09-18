$ErrorActionPreference = 'Stop'
[pscustomobject]@{ cwd=(Get-Location).Path; shell=$PSVersionTable.PSVersion.ToString(); os=[Environment]::OSVersion.VersionString; architecture=[System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString(); filesystem='Windows native C: workspace'; git=(Test-Path -LiteralPath 'C:\Projects\DevForgeAI\.git') } | ConvertTo-Json
Get-Command cargo,rustc,rustfmt,clippy-driver,python,pwsh | Select-Object Name,Source | ConvertTo-Json
& 'C:\Users\bryan\.cargo\bin\rustc.exe' -Vv
if ($LASTEXITCODE) { exit $LASTEXITCODE }
& 'C:\Users\bryan\.cargo\bin\cargo.exe' -V
& 'C:\Users\bryan\.cargo\bin\cargo.exe' fmt --version
& 'C:\Users\bryan\.cargo\bin\cargo.exe' clippy --version
& 'C:\Users\bryan\.cargo\bin\cargo.exe' llvm-cov --version
& 'C:\Program Files\Python310\python.exe' --version
& 'C:\Users\bryan\.cargo\bin\rustup.exe' component list --installed
exit $LASTEXITCODE
