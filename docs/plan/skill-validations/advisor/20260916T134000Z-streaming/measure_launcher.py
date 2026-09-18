"""Measure executable launcher lines under one native PowerShell runtime.

Pester supplies the executable-command line denominator. Native traced child
sessions execute all launcher branches because advisor.ps1 terminates its own
PowerShell process to propagate the Python status, which prevents in-process
Pester coverage collection from completing.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def run(command, env=None, timeout=30):
    process = subprocess.run(
        command,
        cwd=Path.cwd(),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        shell=False,
    )
    return {
        "command": [str(item) for item in command],
        "exit_code": process.returncode,
        "stdout": process.stdout.decode("utf-8", errors="replace"),
        "stderr": process.stderr.decode("utf-8", errors="replace"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell", required=True, type=Path)
    parser.add_argument("--pester", required=True, type=Path)
    parser.add_argument("--launcher", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    shell = args.shell.resolve(strict=True)
    pester = args.pester.resolve(strict=True)
    launcher = args.launcher.resolve(strict=True)
    work = args.work.resolve()
    if work.exists():
        raise SystemExit("work directory must be fresh")
    work.mkdir(parents=True)

    noop = work / "Noop.Tests.ps1"
    write(noop, "Describe 'inventory' { It 'passes' { if (-not $true) { throw 'no' } } }\n")
    inventory_runner = work / "inventory.ps1"
    write(inventory_runner, r'''param($Module, $Target, $Test, $Output)
$ErrorActionPreference = 'Stop'
Remove-Module Pester -Force -ErrorAction SilentlyContinue
Import-Module -Name $Module -Force
$major = (Get-Module Pester).Version.Major
if ($major -ge 5) {
    $configuration = New-PesterConfiguration
    $configuration.Run.Path = @($Test)
    $configuration.Run.PassThru = $true
    $configuration.Output.Verbosity = 'None'
    $configuration.CodeCoverage.Enabled = $true
    $configuration.CodeCoverage.Path = @($Target)
    $configuration.TestRegistry.Enabled = $false
    $result = Invoke-Pester -Configuration $configuration
    $rows = $result.CodeCoverage.CommandsMissed
    $passed = $result.PassedCount
    $failed = $result.FailedCount
}
else {
    $result = Invoke-Pester -Script $Test -CodeCoverage $Target -PassThru -Quiet
    $rows = $result.CodeCoverage.MissedCommands
    $passed = $result.PassedCount
    $failed = $result.FailedCount
}
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($Target, [ref]$tokens, [ref]$errors)
$statements = @($ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.StatementAst] }, $true))
$record = [ordered]@{
    pester_version = (Get-Module Pester).Version.ToString()
    passed = $passed
    failed = $failed
    commands = @($rows | ForEach-Object {
        $line = [int]$_.Line
        $parent = @($statements | Where-Object {
            $_.Extent.StartLineNumber -le $line -and $_.Extent.EndLineNumber -ge $line
        } | Sort-Object { $_.Extent.EndLineNumber - $_.Extent.StartLineNumber } -Descending | Select-Object -First 1)
        [ordered]@{
            line = $line
            command = [string]$_.Command
            parent_start_line = $(if ($parent) { [int]$parent[0].Extent.StartLineNumber } else { $line })
        }
    })
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Output -Encoding UTF8
''')
    inventory_path = work / "pester-inventory.json"
    inventory_process = run([
        str(shell), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(inventory_runner),
        "-Module", str(pester), "-Target", str(launcher), "-Test", str(noop), "-Output", str(inventory_path),
    ])
    if inventory_process["exit_code"] != 0 or not inventory_path.is_file():
        raise SystemExit("Pester inventory failed: " + inventory_process["stderr"])
    inventory = json.loads(inventory_path.read_text(encoding="utf-8-sig"))
    denominator_lines = sorted({int(row["line"]) for row in inventory["commands"]})

    fake_python = work / "fake-python.cmd"
    fake_python.write_text("@echo off\r\nexit /b %ADVISOR_FAKE_PYTHON_EXIT%\r\n", encoding="ascii", newline="")
    fake_script = work / "fake-python.ps1"
    write(fake_script, "# Deliberately produces no native LASTEXITCODE.\n")
    trace_runner = work / "trace.ps1"
    write(trace_runner, r'''param($Launcher, $Python, [switch]$Progress)
Set-PSDebug -Trace 1
if ($Progress) {
    & $Launcher -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason retry -Python $Python -ShowProgress
}
else {
    & $Launcher -Request 'C:\synthetic request.json' -Briefing 'C:\synthetic briefing.md' -RunDir 'C:\synthetic run' -Reason initial -Python $Python
}
''')

    traces = []
    for name, code, progress, python_path in (
        ("success-progress", "0", True, fake_python),
        ("failure-quiet", "7", False, fake_python),
        ("no-native-status", "0", False, fake_script),
        ("invocation-error", "0", True, work / "missing-python.exe"),
    ):
        env = dict(os.environ)
        env["ADVISOR_FAKE_PYTHON_EXIT"] = code
        command = [
            str(shell), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(trace_runner),
            "-Launcher", str(launcher), "-Python", str(python_path),
        ]
        if progress:
            command.append("-Progress")
        observed = run(command, env=env)
        observed["name"] = name
        write(work / (name + ".stdout.txt"), observed["stdout"])
        write(work / (name + ".stderr.txt"), observed["stderr"])
        traces.append(observed)

    executed = set()
    pattern = re.compile(r"DEBUG:\s+(\d+)\+")
    launcher_path = str(launcher).replace("'", "''")
    for trace in traces:
        for line_text in (trace["stdout"] + "\n" + trace["stderr"]).splitlines():
            # Trace has no file marker for nested scripts. Keep only lines after
            # the invocation of the selected launcher until exit terminates it.
            if launcher_path in line_text:
                continue
            match = pattern.search(line_text)
            if match and int(match.group(1)) in denominator_lines:
                executed.add(int(match.group(1)))
    direct_or_parent = {
        int(row["line"]): int(row.get("parent_start_line", row["line"]))
        for row in inventory["commands"]
    }
    executed |= {line for line, parent in direct_or_parent.items() if parent in executed}
    missed = sorted(set(denominator_lines) - executed)
    # PowerShell's exit inside the nested script may not set the outer script's
    # process exit code; the real end-to-end cases test propagation separately.
    behavior_ok = (inventory["passed"] == 1 and inventory["failed"] == 0
                   and all("DEBUG:" in trace["stdout"] for trace in traces))
    report = {
        "schema_version": "advisor-launcher-line-coverage-v1",
        "shell": str(shell),
        "pester": str(pester),
        "pester_version": inventory["pester_version"],
        "launcher": str(launcher),
        "denominator_lines": denominator_lines,
        "executed_lines": sorted(executed),
        "missed_lines": missed,
        "executed_line_numerator": len(executed),
        "executed_line_denominator": len(denominator_lines),
        "executed_line_percent": (100.0 * len(executed) / len(denominator_lines)) if denominator_lines else 0.0,
        "pester_inventory_passed": inventory["passed"],
        "pester_inventory_failed": inventory["failed"],
        "behavior_exit_codes": {trace["name"]: trace["exit_code"] for trace in traces},
        "behavior_exit_codes_matched": behavior_ok,
        "method": "Pester command inventory supplies unique executable source lines; native Set-PSDebug traces from isolated child shells supply executed lines. Trace-launcher padding prevents its own line numbers from overlapping the target.",
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=True))
    return 0 if behavior_ok and not missed else 1


if __name__ == "__main__":
    raise SystemExit(main())
