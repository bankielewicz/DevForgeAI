"""Independent public CLI checks for the fixed source-identity policy.

This harness never starts Codex. It runs only the QA-built frozen candidate's
`profile-sources` command against QA-owned alternate USERPROFILE and ProgramData
roots. The positive case has no applicable junction. The negative case creates
the same relative `chrome/latest` junction under the alternate root and proves
that the compiled absolute exception does not relocate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


REPARSE_ATTRIBUTE = 0x400


def normalized_windows_path(value: str | Path) -> str:
    text = str(value)
    if text.startswith("\\\\?\\UNC\\"):
        text = "\\\\" + text[8:]
    elif text.startswith("\\\\?\\"):
        text = text[4:]
    return str(Path(text).absolute()).casefold()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def run_profile(binary: Path, fixture: Path, user: Path, program_data: Path) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["USERPROFILE"] = str(user)
    environment["ProgramData"] = str(program_data)
    return subprocess.run(
        [str(binary), "profile-sources", "--checkout-root", str(fixture)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        timeout=60,
        shell=False,
        check=False,
    )


def fixture(trials: Path, run_id: str, task: bytes) -> Path:
    root = trials / run_id / "fixture"
    root.mkdir(parents=True, exist_ok=False)
    write_bytes(root / "task.json", task)
    return root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()

    binary = args.binary.resolve(strict=True)
    package = args.package.resolve(strict=True)
    workspace = args.workspace.resolve(strict=True)
    evidence = args.evidence.resolve(strict=False)
    evidence.mkdir(parents=True, exist_ok=False)
    try:
        package.relative_to(workspace)
    except ValueError as error:
        raise SystemExit("package is outside selected workspace") from error
    if not args.run_prefix or any(
        char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        for char in args.run_prefix
    ):
        raise SystemExit("run prefix must contain only ASCII letters, digits, hyphen or underscore")

    trials = workspace / "docs" / "plan" / "framework-worker-trials"
    trials.mkdir(parents=True, exist_ok=True)
    task = (package / "tests" / "fixtures" / "task.json").read_bytes()
    record = package / "src" / "plugin-source-identity.json"
    record_sha256 = digest(record)

    positive_fixture = fixture(trials, f"{args.run_prefix}-empty", task)
    positive_user = evidence / "positive-user"
    positive_program_data = evidence / "positive-program-data"
    positive_user.mkdir()
    positive_program_data.mkdir()
    positive = run_profile(binary, positive_fixture, positive_user, positive_program_data)
    write_bytes(evidence / "positive.stdout.bin", positive.stdout)
    write_bytes(evidence / "positive.stderr.bin", positive.stderr)
    if positive.returncode != 0 or positive.stderr:
        raise AssertionError(
            f"positive public collection failed: exit={positive.returncode} stderr={positive.stderr!r}"
        )
    inventory = json.loads(positive.stdout)
    if inventory.get("schema_version") != 2:
        raise AssertionError("positive inventory is not schema 2")
    if inventory.get("source_identity_sha256") != record_sha256:
        raise AssertionError("positive inventory does not bind exact compiled record bytes")
    if inventory.get("junctions") != []:
        raise AssertionError("disjoint derived root must have an empty applicable mapping set")

    negative_fixture = fixture(trials, f"{args.run_prefix}-relocated-alias", task)
    negative_user = evidence / "negative-user"
    negative_program_data = evidence / "negative-program-data"
    target = (
        negative_user
        / ".codex"
        / "plugins"
        / "cache"
        / "openai-bundled"
        / "chrome"
        / "26.908.70816"
    )
    (target / ".codex-plugin").mkdir(parents=True)
    write_bytes(target / ".codex-plugin" / "plugin.json", b"{}\n")
    write_bytes(target / ".mcp.json", b"{}\n")
    negative_program_data.mkdir()
    alias = target.with_name("latest")
    mklink = subprocess.run(
        [r"C:\Windows\System32\cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(target)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
        shell=False,
        check=False,
    )
    write_bytes(evidence / "mklink.stdout.bin", mklink.stdout)
    write_bytes(evidence / "mklink.stderr.bin", mklink.stderr)
    if mklink.returncode != 0:
        raise AssertionError(f"junction setup failed: {mklink.stderr!r}")
    stat = alias.lstat()
    if int(getattr(stat, "st_file_attributes", 0)) & REPARSE_ATTRIBUTE == 0:
        raise AssertionError("created alias is not a Windows reparse point")
    observed_target = os.readlink(alias)
    if normalized_windows_path(observed_target) != normalized_windows_path(target):
        raise AssertionError("created junction target differs from requested target")
    fsutil = subprocess.run(
        [r"C:\Windows\System32\fsutil.exe", "reparsepoint", "query", str(alias)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
        shell=False,
        check=False,
    )
    write_bytes(evidence / "fsutil.stdout.bin", fsutil.stdout)
    write_bytes(evidence / "fsutil.stderr.bin", fsutil.stderr)
    if fsutil.returncode != 0 or b"0xa0000003" not in fsutil.stdout.lower():
        raise AssertionError("fixture is not proven to be a directory junction")

    negative = run_profile(binary, negative_fixture, negative_user, negative_program_data)
    write_bytes(evidence / "negative.stdout.bin", negative.stdout)
    write_bytes(evidence / "negative.stderr.bin", negative.stderr)
    if negative.returncode != 3 or negative.stdout:
        raise AssertionError(
            f"relocated exception was not rejected: exit={negative.returncode} stdout={negative.stdout!r}"
        )
    diagnostic = json.loads(negative.stderr)
    error = diagnostic.get("error", "")
    if not error.startswith("profile_source_reparse:") or not error.lower().endswith("chrome\\latest"):
        raise AssertionError(f"unexpected negative diagnostic: {diagnostic!r}")

    result = {
        "schema_version": 1,
        "binary": str(binary),
        "binary_sha256": digest(binary),
        "package": str(package),
        "plugin_source_identity_sha256": record_sha256,
        "positive": {
            "exit_code": positive.returncode,
            "schema_version": inventory["schema_version"],
            "junctions": inventory["junctions"],
            "stdout_sha256": hashlib.sha256(positive.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(positive.stderr).hexdigest(),
        },
        "relocated_alias": {
            "exit_code": negative.returncode,
            "diagnostic": diagnostic,
            "junction_path": str(alias),
            "junction_target": str(target),
            "junction_target_observed": observed_target,
            "junction_reparse_attribute": int(getattr(stat, "st_file_attributes", 0)),
            "fsutil_stdout_sha256": hashlib.sha256(fsutil.stdout).hexdigest(),
        },
        "codex_started": False,
        "installed_profile_collected": False,
    }
    output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    (evidence / "result.json").write_text(output, encoding="utf-8")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
