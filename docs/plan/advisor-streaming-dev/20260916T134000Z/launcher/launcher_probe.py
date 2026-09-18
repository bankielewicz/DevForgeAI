#!/usr/bin/env python3
"""Independent native probe for the thin advisor PowerShell launcher."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def powershells() -> list[Path]:
    candidates = [
        Path(os.environ.get("SystemRoot", r"C:\Windows"))
        / "System32"
        / "WindowsPowerShell"
        / "v1.0"
        / "powershell.exe",
        Path(r"C:\Program Files\PowerShell\7\pwsh.exe"),
    ]
    missing = [str(path) for path in candidates if not path.is_file()]
    if missing:
        raise AssertionError(f"required PowerShell executable missing: {missing}")
    return candidates


def run_process(argv: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
        shell=False,
        env=env,
        timeout=30,
        check=False,
    )


def invoke(
    powershell: Path,
    launcher: Path,
    request: Path,
    briefing: Path,
    run_dir: Path,
    *,
    reason: str | None,
    show_progress: bool,
    python: str,
    exit_code: int,
) -> subprocess.CompletedProcess[str]:
    argv = [
        str(powershell),
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(launcher),
        "-Request",
        str(request),
        "-Briefing",
        str(briefing),
        "-RunDir",
        str(run_dir),
        "-Python",
        python,
    ]
    if reason is not None:
        argv.extend(["-Reason", reason])
    if show_progress:
        argv.append("-ShowProgress")
    env = os.environ.copy()
    env["ADVISOR_WRAPPER_PROBE_EXIT"] = str(exit_code)
    return run_process(argv, env)


def parse_stdout(process: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = process.stdout.splitlines()
    if len(lines) != 1:
        raise AssertionError(f"expected one stdout line, got {lines!r}")
    value = json.loads(lines[0])
    if not isinstance(value, dict):
        raise AssertionError("stdout probe value is not an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--launcher", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started_at = dt.datetime.now(dt.timezone.utc)
    started = time.monotonic()
    result: dict[str, object] = {
        "schema": "advisor-launcher-probe-v1",
        "started_at": started_at.isoformat().replace("+00:00", "Z"),
        "launcher": str(args.launcher.resolve()),
        "command": [sys.executable, *sys.argv],
        "status": "FAIL",
        "checks": [],
    }
    checks: list[dict[str, object]] = result["checks"]  # type: ignore[assignment]

    try:
        if not args.launcher.is_file():
            raise AssertionError("required scripts/advisor.ps1 launcher is missing")

        source = args.launcher.read_text(encoding="utf-8-sig")
        forbidden = [token for token in ("ProcessStartInfo", "ANTHROPIC_API_KEY", "claude.exe") if token in source]
        if forbidden:
            raise AssertionError(f"thin launcher contains forbidden policy/process tokens: {forbidden}")

        with tempfile.TemporaryDirectory(prefix="advisor launcher Ω & 'quote' ") as temp_name:
            probe_root = Path(temp_name)
            launcher_copy = probe_root / "advisor.ps1"
            shutil.copyfile(args.launcher, launcher_copy)
            stub = probe_root / "advisor_run.py"
            stub.write_text(
                "import json, os, sys\n"
                "print(json.dumps({'probe': 'stdout', 'argv': sys.argv[1:]}, ensure_ascii=False))\n"
                "print('probe-stderr', file=sys.stderr)\n"
                "raise SystemExit(int(os.environ.get('ADVISOR_WRAPPER_PROBE_EXIT', '0')))\n",
                encoding="utf-8",
            )
            request = probe_root / "request Ω & 'quoted name'.json"
            briefing = probe_root / "briefing Ω & 'quoted name'.md"
            run_dir = probe_root / "run Ω & 'quoted name'"

            for powershell in powershells():
                version_process = run_process(
                    [
                        str(powershell),
                        "-NoLogo",
                        "-NoProfile",
                        "-NonInteractive",
                        "-Command",
                        "$PSVersionTable.PSVersion.ToString()",
                    ]
                )
                if version_process.returncode != 0:
                    raise AssertionError(f"could not query {powershell}: {version_process.stderr}")

                explicit = invoke(
                    powershell,
                    launcher_copy,
                    request,
                    briefing,
                    run_dir,
                    reason="reconcile",
                    show_progress=True,
                    python=sys.executable,
                    exit_code=7,
                )
                explicit_value = parse_stdout(explicit)
                expected = [
                    "run",
                    "--request",
                    str(request),
                    "--briefing",
                    str(briefing),
                    "--run-dir",
                    str(run_dir),
                    "--reason",
                    "reconcile",
                    "--show-progress",
                ]
                if explicit.returncode != 7:
                    raise AssertionError(f"{powershell} did not propagate exit 7: {explicit.returncode}")
                if explicit_value.get("argv") != expected:
                    raise AssertionError(f"{powershell} argv mismatch: {explicit_value.get('argv')!r}")
                if explicit.stderr.strip() != "probe-stderr":
                    raise AssertionError(f"{powershell} stderr was not preserved: {explicit.stderr!r}")

                default = invoke(
                    powershell,
                    launcher_copy,
                    request,
                    briefing,
                    run_dir,
                    reason=None,
                    show_progress=False,
                    python=sys.executable,
                    exit_code=0,
                )
                default_value = parse_stdout(default)
                expected_default = expected[:-3] + ["--reason", "initial"]
                if default.returncode != 0 or default_value.get("argv") != expected_default:
                    raise AssertionError(
                        f"{powershell} default invocation mismatch: exit={default.returncode}, "
                        f"argv={default_value.get('argv')!r}"
                    )

                missing = invoke(
                    powershell,
                    launcher_copy,
                    request,
                    briefing,
                    run_dir,
                    reason=None,
                    show_progress=False,
                    python=str(probe_root / "missing-python.exe"),
                    exit_code=0,
                )
                if missing.returncode != 2:
                    raise AssertionError(f"{powershell} invocation failure exit was {missing.returncode}, expected 2")
                if missing.stdout:
                    raise AssertionError(f"{powershell} invocation failure wrote stdout: {missing.stdout!r}")

                checks.append(
                    {
                        "powershell": str(powershell),
                        "version": version_process.stdout.strip(),
                        "explicit_argument_forwarding": "PASS",
                        "default_reason": "PASS",
                        "stdout_stderr_preservation": "PASS",
                        "exit_status_propagation": "PASS",
                        "invocation_failure_exit_2": "PASS",
                    }
                )

        result["status"] = "PASS"
    except Exception as error:  # evidence must retain the focused Red as data
        result["error"] = f"{type(error).__name__}: {error}"

    result["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    result["duration_seconds"] = round(time.monotonic() - started, 6)
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
