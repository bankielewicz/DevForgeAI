"""Bounded Windows development evidence recorder; no acceptance authority."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parent
PROJECT = Path(r"C:\Projects\DevForgeAI\devforgeai")
QA = Path(r"C:\Projects\DevForgeAI\docs\plan\index-service-qa\20260914T184442947070Z\executions\20260914T191133863776Z")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest():
    return {"root": str(PROJECT), "scope": "all application files excluding target build outputs", "files": [
        {"path": str(p), "bytes": p.stat().st_size, "sha256": digest(p)}
        for p in sorted(PROJECT.rglob("*"))
        if p.is_file() and "target" not in p.relative_to(PROJECT).parts
    ]}


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run(attempt, stage, argv):
    out = ROOT / "attempts" / attempt
    out.mkdir(parents=True, exist_ok=False)
    write(out / "source-manifest.json", manifest())
    env = os.environ.copy()
    overrides = {
        "DEVFORGEAI_INDEX_DATA": str(ROOT / "scratch" / "default-data"),
        "DEVFORGEAI_GUI_EVIDENCE": str(out / "gui"),
    }
    env.update(overrides)
    receipt = {"attempt_id": attempt, "stage": stage, "argv": argv, "cwd": str(PROJECT),
               "platform": sys.platform, "environment_overrides": overrides,
               "source_manifest_sha256": digest(out / "source-manifest.json"),
               "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "timeout_seconds": 1800}
    start = time.monotonic()
    with (out / "stdout.txt").open("wb") as stdout, (out / "stderr.txt").open("wb") as stderr:
        try:
            result = subprocess.run(argv, cwd=PROJECT, env=env, stdout=stdout, stderr=stderr, timeout=1800)
            receipt["exit_code"] = result.returncode
            receipt["outcome"] = "observed_exit"
        except subprocess.TimeoutExpired:
            receipt.update(exit_code=None, outcome="timeout")
    receipt.update(ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   elapsed_seconds=time.monotonic() - start)
    if "llvm-cov" in argv and "report" not in argv:
        profiles = out / "profiles"
        profiles.mkdir()
        collected = []
        target = PROJECT / "target" / "llvm-cov-target"
        for path in sorted(target.rglob("*")):
            if path.is_file() and path.suffix in (".profraw", ".profdata"):
                destination = profiles / path.relative_to(target)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
                collected.append({"source": str(path), "retained": str(destination), "bytes": destination.stat().st_size, "sha256": digest(destination)})
        write(out / "profile-manifest.json", collected)
        write(out / "instrumented-binaries.json", [
            {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}
            for path in sorted(target.rglob("*.exe"))
        ])
    for name in ["stdout.txt", "stderr.txt"]:
        receipt[name + "_sha256"] = digest(out / name)
    write(out / "receipt.json", receipt)
    with (ROOT / "executions.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt) + "\n")
    print(json.dumps(receipt, indent=2))
    print((out / "stdout.txt").read_text(encoding="utf-8", errors="replace")[-12000:])
    print((out / "stderr.txt").read_text(encoding="utf-8", errors="replace")[-8000:])
    return receipt["exit_code"] if receipt["exit_code"] is not None else 124


if __name__ == "__main__":
    sys.exit(run(sys.argv[1], sys.argv[2], sys.argv[3:]))
