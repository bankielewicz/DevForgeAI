"""One bounded offline command per invocation; preserves streams and exact identities."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from intake import RUN, PKG, MANIFEST, binding


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    attempt, scope, *args = sys.argv[1:]
    if not attempt.replace("-", "").isalnum() or scope not in {"original", "harness", "coverage", "tool"}:
        raise ValueError("invalid recorder selection")
    if (RUN / "STOP.json").exists():
        raise RuntimeError("Whole-run stop recorded; no more commands")
    manifest = json.loads(MANIFEST.read_text())
    for row in manifest:
        actual = binding(PKG / row["path"])
        if any(actual[k] != row[k] for k in ("bytes", "sha256")):
            raise RuntimeError("candidate drift: " + row["path"])
    dest = RUN / "attempts" / attempt
    dest.mkdir(parents=True, exist_ok=False)
    cwd = RUN / "harness" if scope == "harness" else PKG
    cargo = Path(r"C:\Users\bryan\.cargo\bin\cargo.exe")
    argv = [str(cargo), *args]
    env = os.environ.copy()
    overrides = {
        "CARGO_TARGET_DIR": str(RUN / ("harness-target" if scope == "harness" else "target")),
        "CARGO_LLVM_COV_TARGET_DIR": str(RUN / "coverage-target"),
        "WF_TEST_EVIDENCE": str(RUN / "fixtures" / attempt),
        "CARGO_NET_OFFLINE": "true", "CARGO_TERM_COLOR": "never",
    }
    env.update(overrides)
    started = {"attempt": attempt, "argv": argv, "cwd": str(cwd), "scope": scope,
               "env_overrides": overrides, "executable": binding(cargo),
               "candidate_manifest": binding(MANIFEST), "plan": binding(RUN / "test-plan.md"),
               "start_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "outer_timeout_seconds": 600, "native_codex_authorized": False}
    if scope == "harness":
        started["harness"] = [binding(p) for p in sorted(cwd.rglob("*")) if p.is_file()]
    write(dest / "started.json", started)
    before = time.monotonic()
    with (dest / "stdout.bin").open("xb") as out, (dest / "stderr.bin").open("xb") as err:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdout=out, stderr=err)
        write(dest / "owned-process.json", {"pid": process.pid, "argv": argv})
        try:
            code = process.wait(timeout=600)
            timeout = False
        except subprocess.TimeoutExpired:
            # Never silently restart a possibly running operation. Contain only
            # the known recorder child; owned Job Objects govern test workers.
            process.terminate()
            code = process.wait(timeout=15)
            timeout = True
    receipt = {**started, "end_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "elapsed_seconds": time.monotonic() - before, "exit_code": code, "timeout": timeout,
               "stdout": binding(dest / "stdout.bin"), "stderr": binding(dest / "stderr.bin")}
    write(dest / "receipt.json", receipt)
    print(json.dumps({"attempt": attempt, "exit_code": code, "elapsed_seconds": receipt["elapsed_seconds"],
                      "timeout": timeout, "receipt": str(dest / "receipt.json")}))
    for name in ("stdout.bin", "stderr.bin"):
        content = (dest / name).read_text(encoding="utf-8", errors="replace")
        print(name + ":\n" + content[-16000:])
    raise SystemExit(code if not timeout else 124)


if __name__ == "__main__":
    main()
