"""Independent QA evidence capture only; never framework authority."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(r"C:\Projects\DevForgeAI")
PACKAGE = WORKSPACE / "devforgeai" / "experiments" / "codex-worker-probe"
REPARSE_ATTRIBUTE = 0x400


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def package_manifest() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []

    def visit(directory: Path) -> None:
        with os.scandir(directory) as scan:
            children = sorted(scan, key=lambda item: item.name.casefold())
        for child in children:
            path = Path(child.path)
            relative = path.relative_to(PACKAGE).as_posix()
            stat = child.stat(follow_symlinks=False)
            attributes = int(getattr(stat, "st_file_attributes", 0))
            if attributes & REPARSE_ATTRIBUTE:
                entries.append(
                    {
                        "path": relative,
                        "kind": "reparse",
                        "file_attributes": attributes,
                    }
                )
                continue
            if child.is_dir(follow_symlinks=False):
                if relative == "target" or relative.startswith("target/"):
                    continue
                visit(path)
            elif child.is_file(follow_symlinks=False):
                entries.append(
                    {
                        "path": relative,
                        "kind": "file",
                        "bytes": stat.st_size,
                        "sha256": sha256(path),
                    }
                )

    visit(PACKAGE)
    return entries


def parse_override(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("environment override must be NAME=VALUE")
    name, setting = value.split("=", 1)
    if not name or "=" in name or "\x00" in name or "\x00" in setting:
        raise argparse.ArgumentTypeError("invalid environment override")
    return name, setting


def capture(
    label: str,
    argv: list[str],
    cwd: Path,
    timeout_seconds: int,
    overrides: list[tuple[str, str]],
) -> int:
    if not label or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in label):
        raise SystemExit("label must contain only ASCII letters, digits, hyphen or underscore")
    if not argv:
        raise SystemExit("missing command after --")
    attempt = ROOT / label
    attempt.mkdir(parents=False, exist_ok=False)

    before_path = attempt / "candidate-before.json"
    atomic_json(before_path, package_manifest())

    executable = Path(argv[0]).resolve(strict=True)
    environment = os.environ.copy()
    recorded_overrides: dict[str, str] = {}
    for name, value in overrides:
        environment[name] = value
        recorded_overrides[name] = value

    stdout_path = attempt / "stdout.bin"
    stderr_path = attempt / "stderr.bin"
    receipt: dict[str, object] = {
        "schema_version": 1,
        "label": label,
        "argv": argv,
        "cwd": str(cwd.resolve(strict=True)),
        "environment_overrides": recorded_overrides,
        "stdin": "DEVNULL",
        "executable": str(executable),
        "executable_sha256": sha256(executable),
        "recorder_sha256": sha256(Path(__file__).resolve()),
        "candidate_before_sha256": sha256(before_path),
        "start_utc": utc_now(),
        "timeout_seconds": timeout_seconds,
    }

    started = time.monotonic_ns()
    timed_out = False
    containment: dict[str, object] | None = None
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        child = subprocess.Popen(
            argv,
            cwd=cwd,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            shell=False,
        )
        receipt["owned_pid"] = child.pid
        try:
            native_exit = child.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            taskkill_argv = [
                r"C:\Windows\System32\taskkill.exe",
                "/PID",
                str(child.pid),
                "/T",
                "/F",
            ]
            cleanup = subprocess.run(
                taskkill_argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,
                shell=False,
                check=False,
            )
            (attempt / "containment.stdout.bin").write_bytes(cleanup.stdout)
            (attempt / "containment.stderr.bin").write_bytes(cleanup.stderr)
            containment = {
                "argv": taskkill_argv,
                "exit_code": cleanup.returncode,
                "stdout_sha256": sha256(attempt / "containment.stdout.bin"),
                "stderr_sha256": sha256(attempt / "containment.stderr.bin"),
            }
            try:
                native_exit = child.wait(timeout=20)
            except subprocess.TimeoutExpired:
                native_exit = None

    ended = time.monotonic_ns()
    after_path = attempt / "candidate-after.json"
    atomic_json(after_path, package_manifest())
    receipt.update(
        {
            "end_utc": utc_now(),
            "duration_monotonic_ns": ended - started,
            "native_exit_code": native_exit,
            "timed_out": timed_out,
            "containment": containment,
            "stdout_bytes": stdout_path.stat().st_size,
            "stdout_sha256": sha256(stdout_path),
            "stderr_bytes": stderr_path.stat().st_size,
            "stderr_sha256": sha256(stderr_path),
            "candidate_after_sha256": sha256(after_path),
            "candidate_unchanged": before_path.read_bytes() == after_path.read_bytes(),
        }
    )
    atomic_json(attempt / "receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True), flush=True)
    if timed_out:
        return 124
    if native_exit is None:
        return 125
    return int(native_exit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--cwd", type=Path, default=PACKAGE)
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--env", action="append", type=parse_override, default=[])
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    if not 1 <= args.timeout <= 900:
        raise SystemExit("timeout must be in 1..900 seconds")
    return capture(args.label, command, args.cwd, args.timeout, args.env)


if __name__ == "__main__":
    raise SystemExit(main())
