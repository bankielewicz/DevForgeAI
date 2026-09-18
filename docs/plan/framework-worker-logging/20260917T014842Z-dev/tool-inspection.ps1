$ErrorActionPreference='Stop'
Get-Location
[System.Environment]::OSVersion.VersionString
$PSVersionTable.PSVersion.ToString()
Get-Command cargo,rustc,rustfmt,python,pwsh | Select-Object Name,Source
cargo --version
rustc --version --verbose
cargo llvm-cov --version
rustup toolchain list
cargo llvm-cov --help | Select-String -Pattern '\-\-branch','unstable' -Context 0,2
