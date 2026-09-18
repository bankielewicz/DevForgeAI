"""Evidence supervisor for the one selected attempt; Rust owns policy and execution."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from intake import (ROOT, WORKSPACE, PACKAGE, QA, BINARY, FIXTURE, INDEX_SHA,
                    binding, candidate_check, check_binding, sha256, utc_now, write)


def child_environment():
    parent = os.environ.copy()
    child = parent.copy()
    removed = [key for key in child if key.upper() == "ANTHROPIC_API_KEY"]
    for key in removed:
        del child[key]
    guard = sorted(key for key in child if "API_KEY" in key.upper()
                   or "ACCESS_TOKEN" in key.upper() or key.upper() == "OPENAI_BASE_URL")
    assert not guard, "Other credential/provider environment prerequisite is unresolved"
    return parent, child, removed


def capture(label, arguments, timeout, native=False):
    candidate = candidate_check()
    assert sha256(QA / "artifact-index.json") == INDEX_SHA
    bindings = json.loads((ROOT / "bindings.json").read_bytes())
    assert sha256(FIXTURE / "task.json") == bindings["task_sha256"]
    assert [p.name for p in FIXTURE.iterdir()] == ["task.json"]
    if native:
        assert label == "native-001" and arguments[0] == "preflight"
        assert not (FIXTURE.parent / "run").exists()
    else:
        assert arguments[0] in {"profile-sources", "inspect"}
    attempt = ROOT / label
    attempt.mkdir(exist_ok=False)
    parent, environment, removed = child_environment()
    argv = [str(BINARY), *arguments]
    receipt = {
        "argv": argv, "cwd": str(WORKSPACE), "binary": binding(BINARY),
        "recorder": binding(Path(__file__)), "start_utc": utc_now(),
        "stdin": "PIPE held open with no input" if native else "DEVNULL",
        "outer_timeout_seconds": timeout, "native_attempt": native,
        "child_only_removed_names": removed, "parent_environment_mutated": False,
        "credential_values_logged": False, "framework_acceptance": "NOT_EVALUATED",
    }
    write(attempt / "started.json", receipt)
    write(attempt / "candidate-before.json", candidate)
    started = time.monotonic_ns()
    child = None
    code = None
    timed_out = False
    spawn_error = None
    containment = None
    with (attempt / "stdout.bin").open("xb") as stdout, (attempt / "stderr.bin").open("xb") as stderr:
        try:
            child = subprocess.Popen(argv, cwd=WORKSPACE, env=environment, shell=False,
                stdin=subprocess.PIPE if native else subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
            receipt["owned_pid"] = child.pid
            write(attempt / "owned-process.json", {"pid": child.pid, "start_utc": utc_now(),
                  "argv": argv, "ownership": "live subprocess handle", "hidden": True})
            try:
                code = child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                # The retained live Popen handle establishes ownership; no historical PID lookup.
                if child.poll() is None:
                    command = [r"C:\Windows\System32\taskkill.exe", "/PID", str(child.pid), "/T", "/F"]
                    try:
                        stopped = subprocess.run(command, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
                            timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
                        (attempt / "containment.stdout.bin").write_bytes(stopped.stdout)
                        (attempt / "containment.stderr.bin").write_bytes(stopped.stderr)
                        containment = {"argv": command, "exit_code": stopped.returncode}
                    except subprocess.TimeoutExpired:
                        containment = {"argv": command, "timed_out": True}
                try:
                    code = child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    code = None
        except OSError as error:
            spawn_error = {"type": type(error).__name__, "errno": error.errno,
                           "winerror": getattr(error, "winerror", None)}
        finally:
            if child is not None and child.stdin is not None:
                child.stdin.close()
    elapsed = time.monotonic_ns() - started
    after = candidate_check()
    write(attempt / "candidate-after.json", after)
    receipt.update({"end_utc": utc_now(), "duration_monotonic_ns": elapsed,
        "native_exit_code": code, "timed_out": timed_out, "spawn_error": spawn_error,
        "containment": containment, "harness_stopped": child is None or child.poll() is not None,
        "candidate_unchanged": candidate == after, "parent_environment_unchanged": parent == dict(os.environ),
        "fixture": binding(FIXTURE / "task.json"), "fixture_members": sorted(p.name for p in FIXTURE.iterdir()),
        "stdout": binding(attempt / "stdout.bin"), "stderr": binding(attempt / "stderr.bin")})
    write(attempt / "receipt.json", receipt)
    print(json.dumps({"label": label, "native_exit_code": code, "timed_out": timed_out,
        "duration_seconds": elapsed / 1e9, "candidate_unchanged": candidate == after,
        "stdout_bytes": receipt["stdout"]["bytes"], "stderr_bytes": receipt["stderr"]["bytes"]}), flush=True)
    return receipt


def prepare(version, inventory_path):
    inventory_path = Path(inventory_path)
    receipt = json.loads((inventory_path.parent / "receipt.json").read_bytes())
    assert receipt["native_exit_code"] == 0 and not receipt["timed_out"]
    assert receipt["stdout"] == binding(inventory_path)
    inventory = json.loads(inventory_path.read_bytes())
    assert inventory["schema_version"] == 2
    assert inventory["fixture_cwd"].lower() == str(FIXTURE).lower()
    candidate_check()
    policy_path = PACKAGE / "src/restrictive-launch-policy.json"
    policy = json.loads(policy_path.read_bytes())
    identity = json.loads((PACKAGE / "src/native-executable-identity.json").read_bytes())
    assert sha256(identity["physical_executable"]) == identity["executable_sha256"]
    assert not (FIXTURE.parent / "run").exists()
    folder = ROOT / version
    folder.mkdir(exist_ok=False)
    review_path = folder / "review.unqualified.json"
    request_path = folder / "request.json"
    review = {
        "schema_version": 2,
        "reviewer": "Codex evidence preparation only; all findings false; no human operator attestation",
        "trial_selection_ref": str(ROOT / "selection.md"),
        "codex_sha256": identity["executable_sha256"], "checkout_root": str(FIXTURE),
        "model": "gpt-6-astra", "effort": "high",
        "profile_sources": [{"path": e["path"], "sha256": e["sha256"]}
                            for e in inventory["entries"] if e["state"] == "file"],
        "findings": {"native_read_only_available": False, "no_external_tool_or_hook_effects": False,
                     "codex_managed_chatgpt": False, "no_custom_provider": False},
        "launch_policy_id": policy["policy_id"], "launch_policy_sha256": sha256(policy_path),
        "source_inventory_ref": str(inventory_path), "source_inventory_sha256": sha256(inventory_path),
    }
    write(review_path, review)
    request = {
        "schema_version": 2, "project_id": "DevForgeAI", "checkout_id": "native-diagnostic",
        "work_id": "no-work-profile-diagnostic", "run_id": FIXTURE.parent.name,
        "candidate_sha256": sha256(FIXTURE / "task.json"), "checkout_root": str(FIXTURE),
        "run_dir": str(FIXTURE.parent / "run"), "worker_executable": identity["physical_executable"],
        "worker_sha256": identity["executable_sha256"], "adapter": identity["adapter"],
        "scenario": "complete", "profile": {
            "model": "gpt-6-astra", "effort": "high", "review_ref": str(review_path),
            "review_sha256": sha256(review_path), "launch_policy_id": policy["policy_id"],
            "launch_policy_sha256": sha256(policy_path)},
    }
    write(request_path, request)
    write(folder / "input-bindings.json", {
        "prepared_utc": utc_now(), "fixture": binding(FIXTURE / "task.json"),
        "request": binding(request_path), "review": binding(review_path),
        "source_inventory": binding(inventory_path), "policy": binding(policy_path),
        "worker": binding(identity["physical_executable"]), "binary": binding(BINARY),
        "all_findings_false": all(value is False for value in review["findings"].values()),
        "source_entries": len(inventory["entries"]), "physical_source_files": len(review["profile_sources"]),
        "native_attempts": 0, "framework_acceptance": "NOT_EVALUATED",
    })
    print(json.dumps({"version": version, "request": binding(request_path),
                      "source_entries": len(inventory["entries"]), "all_findings_false": True}), flush=True)
    return request_path


def main():
    assert len(sys.argv) == 2
    mode = sys.argv[1]
    if mode == "prepare":
        observed = capture("sources-001", ["profile-sources", "--checkout-root", str(FIXTURE)], 30)
        if observed["native_exit_code"] != 0:
            raise SystemExit(3)
        prepare("inputs-001", ROOT / "sources-001/stdout.bin")
    elif mode == "launch":
        # This immutable latch is made before source refresh, not only before native spawn.
        write(ROOT / "launch-invocation.json", {"utc": utc_now(), "maximum_native_attempts": 1,
              "retry_permitted": False, "recorder": binding(Path(__file__))})
        candidate_check()
        initial = json.loads((ROOT / "inputs-001/input-bindings.json").read_bytes())
        for key in ("fixture", "request", "review", "source_inventory", "policy", "worker", "binary"):
            assert check_binding(initial[key])["matches"], "Prepared input changed"
        # Recollect and rebind under the exact permission context used for launch.
        observed = capture("sources-002-prelaunch", ["profile-sources", "--checkout-root", str(FIXTURE)], 30)
        if observed["native_exit_code"] != 0:
            raise SystemExit(3)
        request = prepare("inputs-002-prelaunch", ROOT / "sources-002-prelaunch/stdout.bin")
        first = json.loads((ROOT / "sources-001/stdout.bin").read_bytes())
        refreshed = json.loads((ROOT / "sources-002-prelaunch/stdout.bin").read_bytes())
        write(ROOT / "permission-refresh.json", {"utc": utc_now(),
            "initial_inventory": binding(ROOT / "sources-001/stdout.bin"),
            "prelaunch_inventory": binding(ROOT / "sources-002-prelaunch/stdout.bin"),
            "typed_inventory_equal": first == refreshed,
            "request_rebound": binding(request), "prior_inputs_preserved": True})
        result = capture("native-001", ["preflight", "--request", str(request)], 145, native=True)
        raise SystemExit(124 if result["timed_out"] else 125 if result["native_exit_code"] is None else result["native_exit_code"])
    elif mode == "readback":
        observed = capture("sources-003-after", ["profile-sources", "--checkout-root", str(FIXTURE)], 30)
        run_dir = FIXTURE.parent / "run"
        if run_dir.exists():
            capture("inspect-001", ["inspect", "--run-dir", str(run_dir), "--after", "0", "--limit", "100"], 30)
        raise SystemExit(0 if observed["native_exit_code"] == 0 else 3)
    else:
        raise SystemExit("Unknown mode")


if __name__ == "__main__":
    main()
