import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(r"C:\Projects\DevForgeAI")
CANDIDATE = WORKSPACE / "devforgeai/experiments/codex-worker-probe"
MANIFEST = WORKSPACE / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-manifest.json"
HARNESS = ROOT / "harness"


def binding(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def candidate_readback() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    observed = []
    for expected in manifest:
        path = CANDIDATE / expected["path"]
        actual = binding(path)
        actual["relative_path"] = expected["path"]
        actual["matches_manifest"] = (
            actual["bytes"] == expected["bytes"] and actual["sha256"] == expected["sha256"]
        )
        if not actual["matches_manifest"]:
            raise RuntimeError(f"candidate drift: {expected['path']}")
        observed.append(actual)
    return observed


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: record.py LABEL COMMAND [ARG ...]")
    label = sys.argv[1]
    argv = sys.argv[2:]
    attempt = ROOT / "attempts" / label
    attempt.mkdir(parents=True, exist_ok=False)
    manifest_binding = binding(MANIFEST)
    if manifest_binding["sha256"] != "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540":
        raise RuntimeError("selected manifest drift")
    before = candidate_readback()
    (attempt / "candidate-before.json").write_text(json.dumps(before, indent=2), encoding="utf-8")
    request = {
        "argv": argv,
        "cwd": str(HARNESS),
        "candidate_manifest": manifest_binding,
        "shell": False,
        "network_mode": "cargo_offline",
    }
    (attempt / "request.json").write_text(json.dumps(request, indent=2), encoding="utf-8")
    environment = os.environ.copy()
    environment["CARGO_TARGET_DIR"] = str(ROOT / "target")
    environment["CARGO_NET_OFFLINE"] = "true"
    environment["CARGO_TERM_COLOR"] = "never"
    environment["STARTUP_REPRO_EVIDENCE"] = str(ROOT / "runtime" / label)
    started = time.time()
    with (attempt / "stdout.bin").open("xb") as stdout, (attempt / "stderr.bin").open("xb") as stderr:
        completed = subprocess.run(
            argv,
            cwd=HARNESS,
            env=environment,
            shell=False,
            stdout=stdout,
            stderr=stderr,
            timeout=120,
            check=False,
        )
    after = candidate_readback()
    (attempt / "candidate-after.json").write_text(json.dumps(after, indent=2), encoding="utf-8")
    receipt = {
        "argv": argv,
        "cwd": str(HARNESS),
        "exit_code": completed.returncode,
        "elapsed_seconds": time.time() - started,
        "stdout": binding(attempt / "stdout.bin"),
        "stderr": binding(attempt / "stderr.bin"),
        "candidate_files_checked": len(after),
        "candidate_matches_manifest_before": all(item["matches_manifest"] for item in before),
        "candidate_matches_manifest_after": all(item["matches_manifest"] for item in after),
    }
    (attempt / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
