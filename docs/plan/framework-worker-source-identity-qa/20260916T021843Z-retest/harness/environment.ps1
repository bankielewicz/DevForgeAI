$ErrorActionPreference = 'Stop'

[pscustomobject]@{
    Platform = [Environment]::OSVersion.Platform.ToString()
    Version = [Environment]::OSVersion.Version.ToString()
    Is64BitOperatingSystem = [Environment]::Is64BitOperatingSystem
    Architecture = [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
} | ConvertTo-Json -Compress

[pscustomobject]@{
    PowerShell = $PSVersionTable.PSVersion.ToString()
    Python = (python --version 2>&1)
    Rustc = (rustc --version)
    Cargo = (cargo --version)
    LlvmCov = (cargo llvm-cov --version)
    CargoPath = (Get-Command cargo).Source
    RustcPath = (Get-Command rustc).Source
    PythonPath = (Get-Command python).Source
} | ConvertTo-Json -Compress
