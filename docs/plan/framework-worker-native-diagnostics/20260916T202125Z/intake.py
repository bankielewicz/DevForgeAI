"""Literal-path evidence readback only. No native launch or authority decision."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(r"C:\Projects\DevForgeAI")
PACKAGE = WORKSPACE / "devforgeai/experiments/codex-worker-probe"
QA = WORKSPACE / "docs/plan/framework-worker-diagnostics-qa/20260916T191731Z"
DEV = WORKSPACE / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev"
MANIFEST = DEV / "candidate-v2-manifest.json"
BINARY = QA / "target/debug/devforgeai-codex-worker-probe.exe"
FIXTURE = WORKSPACE / "docs/plan/framework-worker-trials/20260916T202125Z-diagnostic/fixture"
INDEX_SHA = "552912696c5260091a8cb2305b13d1f1987e53630b610dd66afec55f84d132d9"
MANIFEST_SHA = "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540"
BINARY_SHA = "0ab81c4c0e6c1a23227cc5c6343c810ae62e37d92dd356b39d8101a34c4d9623"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path):
    path = Path(path)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}


def write(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True)
        stream.write("\n")


def collect_files(base):
    rows = []
    for directory, dirs, files in os.walk(base, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in {"target", "__pycache__"})
        for name in dirs + sorted(files):
            path = Path(directory) / name
            if path.lstat().st_file_attributes & 0x400:
                raise RuntimeError("Unexpected reparse in retained evidence or package")
        rows.extend(binding(Path(directory) / name) for name in sorted(files))
    return rows


def check_binding(expected):
    try:
        current = binding(expected["path"])
        return {**current, "matches": all(current[k] == expected[k] for k in ("bytes", "sha256"))}
    except OSError as error:
        return {"path": expected["path"], "matches": False,
                "error": type(error).__name__, "winerror": getattr(error, "winerror", None)}


def candidate_check():
    assert sha256(MANIFEST) == MANIFEST_SHA
    assert sha256(BINARY) == BINARY_SHA and BINARY.stat().st_size == 2307584
    expected = json.loads(MANIFEST.read_bytes())
    actual = collect_files(PACKAGE)
    keyed = {Path(row["path"]).relative_to(PACKAGE).as_posix(): row for row in actual}
    assert set(keyed) == {row["path"] for row in expected}, "Candidate membership drift"
    assert all(all(keyed[row["path"]][k] == row[k] for k in ("bytes", "sha256")) for row in expected), "Candidate byte drift"
    return actual


def main():
    before = ROOT / "intake-readback.json"
    assert not before.exists()
    assert sha256(QA / "artifact-index.json") == INDEX_SHA
    index = json.loads((QA / "artifact-index.json").read_bytes())
    checks = [check_binding(row) for row in index["artifacts"].values()]
    input_checks = [check_binding(row) for row in json.loads((QA / "input-bindings.json").read_bytes())]
    candidate = candidate_check()
    snapshot_checks = [check_binding({**row, "path": str(DEV / "candidate-v2-snapshot" / row["path"])})
                       for row in json.loads(MANIFEST.read_bytes())]
    identity = json.loads((PACKAGE / "src/native-executable-identity.json").read_bytes())
    worker = binding(identity["physical_executable"])
    assert worker["sha256"] == identity["executable_sha256"]
    old_native = WORKSPACE / "docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity"
    prior_native = collect_files(old_native)
    write(ROOT / "prior-native-bindings.json", prior_native)
    result = {
        "utc": utc_now(), "qa_index": binding(QA / "artifact-index.json"),
        "qa_artifact_checks": checks, "input_checks": input_checks,
        "candidate_manifest": binding(MANIFEST), "candidate_files": candidate,
        "snapshot_checks": snapshot_checks, "binary": binding(BINARY), "worker": worker,
        "prior_native_files": len(prior_native),
        "all_checks_match": all(row["matches"] for row in checks + input_checks + snapshot_checks),
        "native_attempts": 0, "framework_acceptance": "NOT_EVALUATED",
    }
    write(before, result)
    assert result["all_checks_match"], "Bound evidence/input drift; stop before fixture/launch"
    FIXTURE.mkdir(parents=True, exist_ok=False)
    with (FIXTURE / "task.json").open("xb") as stream:
        stream.write((PACKAGE / "tests/fixtures/task.json").read_bytes())
    write(ROOT / "bindings.json", {
        "binary": str(BINARY), "binary_sha256": BINARY_SHA,
        "candidate_manifest": str(MANIFEST), "candidate_manifest_sha256": MANIFEST_SHA,
        "fixture": str(FIXTURE), "task_sha256": sha256(FIXTURE / "task.json"),
        "worker": worker, "launch_policy": binding(PACKAGE / "src/restrictive-launch-policy.json"),
        "source_identity": binding(PACKAGE / "src/plugin-source-identity.json"),
    })
    write(ROOT / "environment.json", {
        "utc": utc_now(), "platform": platform.platform(), "machine": platform.machine(),
        "python": sys.version, "python_executable": sys.executable,
        "cwd": str(Path.cwd()), "workspace": str(WORKSPACE),
        "git_present": (WORKSPACE / ".git").exists(),
        "parent_guard_matched_names": sorted(k for k in os.environ if "API_KEY" in k.upper()
            or "ACCESS_TOKEN" in k.upper() or k.upper() == "OPENAI_BASE_URL"),
        "alternate_codex_home_selected": False, "credential_values_logged": False,
    })
    print(json.dumps({"qa_artifacts": len(checks), "inputs": len(input_checks),
        "candidate_files": len(candidate), "snapshot_files": len(snapshot_checks),
        "prior_native_files": len(prior_native), "all_checks_match": result["all_checks_match"],
        "fixture": binding(FIXTURE / "task.json")}))


if __name__ == "__main__":
    main()
