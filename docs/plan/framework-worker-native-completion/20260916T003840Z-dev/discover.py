"""Capture installed tool versions without building product code."""
from pathlib import Path
import record

commands = [
    ('env-rustc', [r'C:\Users\bryan\.cargo\bin\rustc.exe', '--version', '--verbose']),
    ('env-cargo', [r'C:\Users\bryan\.cargo\bin\cargo.exe', '--version']),
    ('env-fmt', [r'C:\Users\bryan\.cargo\bin\rustfmt.exe', '--version']),
    ('env-clippy', [r'C:\Users\bryan\.cargo\bin\cargo.exe', 'clippy', '--version']),
    ('env-coverage', [r'C:\Users\bryan\.cargo\bin\cargo.exe', 'llvm-cov', '--version']),
    ('env-shell', [r'C:\Program Files\PowerShell\7\pwsh.exe', '-NoProfile', '-NonInteractive', '-Command', '$PSVersionTable.PSVersion.ToString(); [System.Environment]::OSVersion.VersionString; [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()']),
]
for label, command in commands:
    status = record.capture(label, command, record.PACKAGE, 30, [])
    if status:
        raise SystemExit(status)
