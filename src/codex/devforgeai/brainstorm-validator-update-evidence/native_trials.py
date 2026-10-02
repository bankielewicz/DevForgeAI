"""Two bounded native trials using the historical Brainstorm app-server controller.

Candidate and definitions are frozen before any launch. Each trial has a unique parent
containing only its own project and runtime copy. No installation or saved config writes.
"""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

E = Path(__file__).resolve().parent
PACKAGE = E.parent
ROOT = PACKAGE.parents[2]
HISTORICAL = PACKAGE / "import-evidence/native-evaluation-20260928"
CASES = ("writes-valid-brn", "records-provenance")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as handle:
        handle.write(json.dumps(value, indent=2) + "\n")


def inventory(root):
    return {p.relative_to(root).as_posix(): digest(p)
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def freeze():
    native = E / "native"
    native.mkdir(exist_ok=False)
    runtime_files = [PACKAGE / ".codex-plugin/plugin.json"]
    runtime_files.extend(p for p in sorted((PACKAGE / "skills").rglob("*")) if p.is_file())
    files = {p.relative_to(PACKAGE).as_posix(): digest(p) for p in runtime_files}
    definitions = {}
    for case in CASES:
        source = PACKAGE / "evals/brainstorm" / case
        shutil.copytree(source, native / "definitions" / case)
        for p in source.rglob("*"):
            if p.is_file():
                definitions[p.relative_to(PACKAGE).as_posix()] = digest(p)
    executable = Path(shutil.which("codex")).resolve(strict=True)
    version = subprocess.run([str(executable), "--version"], text=True, capture_output=True)
    version.check_returncode()
    config = Path("/home/bryan/.codex/config.toml")
    binding = {
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "files": files,
        "candidate_sha256": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
        "case_definitions": definitions,
        "case_definitions_sha256": hashlib.sha256(json.dumps(definitions, sort_keys=True).encode()).hexdigest(),
        "runtime": str(executable),
        "runtime_sha256": digest(executable),
        "runtime_version": version.stdout.strip(),
        "runtime_version_stderr": version.stderr,
        "config_sha256": digest(config),
        "controller": str(HISTORICAL / "native_eval.py"),
        "controller_sha256": digest(HISTORICAL / "native_eval.py"),
        "grader_sha256": digest(HISTORICAL / "grade_eval.py"),
        "wrapper_sha256": digest(Path(__file__)),
        "cases": [{"case": c, "arm": "plugin", "repeat": 1, "status": "NOT_RUN"} for c in CASES],
        "limits": {"max_attempts_per_case": 1, "timeout_seconds_per_case": 900},
        "scoring": "Historical all-applicable-graders binary trial score; 0.8 inherited threshold. One repetition is scoped smoke evidence, not three-run qualification.",
        "source_model": "Host configured default, recorded from each thread/start result",
        "integration_reference": "https://learn.chatgpt.com/docs/app-server#skills",
        "scope": "Process-scoped native skills roots, full package runtime copy; plugin manifest checked separately. No saved config changes or installation.",
    }
    save(native / "binding.json", binding)
    print(json.dumps({k: binding[k] for k in ("candidate_sha256", "runtime", "runtime_version", "runtime_sha256")}), flush=True)


def load_historical():
    spec = importlib.util.spec_from_file_location("brainstorm_native_historical", HISTORICAL / "native_eval.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(case):
    assert case in CASES
    binding = json.loads((E / "native/binding.json").read_text())
    for relative, expected in {**binding["files"], **binding["case_definitions"]}.items():
        assert digest(PACKAGE / relative) == expected, relative
    assert digest(Path(binding["runtime"])) == binding["runtime_sha256"], "runtime drift"
    assert digest(HISTORICAL / "native_eval.py") == binding["controller_sha256"]
    assert digest(Path(__file__)) == binding["wrapper_sha256"]
    evidence = E / "native" / (case + "--plugin--1")
    evidence.mkdir(exist_ok=False)
    parent = Path(tempfile.mkdtemp(prefix="devforgeai-brn-trial-"))
    cwd = parent / "project"
    cwd.mkdir()
    candidate = parent / "candidate"
    for relative in binding["files"]:
        target = candidate / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE / relative, target)
    assert inventory(candidate) == binding["files"]
    prompt = (E / "native/definitions" / case / "prompt.md").read_text().split("---", 2)[2].strip()
    (evidence / "prompt.md").write_text(prompt + "\n")
    save(evidence / "before.json", inventory(cwd))
    save(evidence / "candidate-before.json", inventory(candidate))
    save(evidence / "attempt.json", {"case": case, "arm": "plugin", "repeat": 1,
                                    "workspace": str(cwd), "candidate": str(candidate),
                                    "runtime_sha256": digest(Path(binding["runtime"])),
                                    "started": datetime.datetime.now(datetime.timezone.utc).isoformat()})
    historical = load_historical()
    historical.EXE = binding["runtime"]
    server = None
    started = time.monotonic()
    try:
        server = historical.Server(evidence, cwd)
        server.setup(cwd, "plugin", candidate)
        result = server.turn(prompt, 900)
        result.update(threadId=server.thread, model=server.model)
    except Exception as exc:
        result = {"status": "harness_error", "error": repr(exc)}
    finally:
        if server is not None:
            server.close()
    result.update(case=case, arm="plugin", repeat=1, elapsed_seconds=round(time.monotonic()-started, 3),
                  workspace=str(cwd), candidate=str(candidate))
    save(evidence / "result.json", result)
    save(evidence / "after.json", inventory(cwd))
    save(evidence / "candidate-after.json", inventory(candidate))
    shutil.copytree(cwd, evidence / "workspace")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "freeze":
        freeze()
    else:
        run(sys.argv[1])
