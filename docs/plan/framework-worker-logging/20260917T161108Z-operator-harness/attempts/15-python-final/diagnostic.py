"""Operator diagnostic support; Rust retains admission and inspection authority."""
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import threading
import time
import uuid

HERE = Path(__file__).resolve().parent
TRIAL = HERE.parent
sys.path.insert(0, str(TRIAL))
sys.path.insert(0, str(HERE))
from recorder import binding, capture, write_new

SOURCE_BUDGET = dict(cancel_after=25, grace=2, reap=1, finalize=2, hold_stdin=False)
NATIVE_BUDGET = dict(cancel_after=135, grace=5, reap=2, finalize=3, hold_stdin=True)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def selected_config():
    return read_json(HERE / "configuration.json")


def verify_preservation(config=None):
    """Check preserved evidence and the selected live inventory independently."""
    config = selected_config() if config is None else config
    checked = {}

    def check(expected):
        path = str(expected["path"])
        if path not in checked:
            checked[path] = binding(path)
        actual = checked[path]
        require(actual["sha256"] == expected["sha256"], "binding_drift: " + path)
        require("bytes" not in expected or actual["bytes"] == expected["bytes"], "size_drift: " + path)

    for group in config["preserved_manifests"]:
        check(group["binding"])
        document = read_json(group["binding"]["path"])
        for selector in group["selectors"]:
            rows = document
            for key in selector:
                rows = rows[key]
            if isinstance(rows, dict):
                rows = rows.values()
            for expected in rows:
                check(expected)
        if isinstance(document, dict):
            for link in document.get("reparse_points", []):
                require(os.readlink(link["path"]).removeprefix("\\\\?\\") == link["target"].removeprefix("\\\\?\\"), "retained_reparse_drift")
    for expected in config["extra_bindings"]:
        check(expected)
    for link in config["junctions"]:
        require(os.lstat(link["path"]).st_reparse_tag == 0xA0000003, "junction_tag_drift")
        require(os.readlink(link["path"]).removeprefix("\\\\?\\") == link["target"].removeprefix("\\\\?\\"), "junction_target_drift")
    for name in ("probe", "worker", "review_template", "diagnostics", "selection", "approved_inventory"):
        check(config[name])
    inventory = read_json(config["approved_inventory"]["path"])
    current = [row for row in inventory["entries"] if row["state"] == "file"]
    for expected in current:
        check(expected)
    fixture = Path(config["request"]["checkout_root"])
    require(sorted(path.name for path in fixture.iterdir()) == ["task.json"], "fixture_membership_changed")
    check(config["fixture"])
    return {"unique_files_hashed": len(checked), "current_reviewed_files_hashed": len(current),
            "approved_inventory": config["approved_inventory"], "framework_acceptance": "NOT_EVALUATED"}


def emit(record):
    # Escape control characters for display; raw recorder files remain exact.
    print(json.dumps(record, ensure_ascii=True), flush=True)


def guarded_names(environment):
    return sorted(name for name in environment if "API_KEY" in name.upper()
                  or "ACCESS_TOKEN" in name.upper() or name.upper() in ("OPENAI_BASE_URL", "CODEX_HOME"))


def child_environment(parent):
    names = guarded_names(parent)
    require(all(name.upper() == "ANTHROPIC_API_KEY" for name in names),
            "unapproved_guarded_environment_name: " + ", ".join(names))
    child = {key: value for key, value in parent.items() if key.upper() != "ANTHROPIC_API_KEY"}
    return child, {"parent_guarded_names": names, "child_omitted_names": names,
                   "child_guarded_names": guarded_names(child), "values_recorded": False,
                   "parent_modified": False, "configuration_modified": False}


def monitor(attempt, stop, stage):
    """Best-effort bounded console copy, independent of capture and cleanup."""
    started = time.monotonic()
    positions = dict(stdout=0, stderr=0)
    next_progress = 0.0
    try:
        while True:
            for stream in positions:
                path = attempt / (stream + ".bin")
                if path.is_file() and positions[stream] < 65536:
                    with path.open("rb") as source:
                        source.seek(positions[stream])
                        data = source.read(min(4096, 65536 - positions[stream]))
                    positions[stream] += len(data)
                    if data:
                        emit({"stage": stage, "stream": stream, "display": data.decode("utf-8", errors="replace"),
                              "display_limit_bytes_per_stream": 65536})
            elapsed = time.monotonic() - started
            if elapsed >= next_progress:
                emit({"stage": stage, "elapsed_seconds": round(elapsed, 1),
                      "raw_evidence": str(attempt)})
                next_progress = elapsed + 5
            if stop.wait(0.1):
                return
    except (OSError, UnicodeError):
        # A broken console cannot prevent cancellation or exact file capture.
        return


def capture_visible(argv, config, attempt, environment, stage, budgets):
    emit({"stage": stage, "argv": argv, "cwd": config["workspace"], "shell": False,
          "stdin_held_open": budgets["hold_stdin"]})
    stop = threading.Event()
    display = threading.Thread(target=monitor, args=(attempt, stop, stage), daemon=True)
    started = time.monotonic()
    display.start()
    try:
        receipt = capture(argv, config["workspace"], attempt, environment=environment, **budgets)
    finally:
        stop.set()
        display.join(timeout=0.05)  # Never wait indefinitely on a blocked console.
    elapsed = time.monotonic() - started
    return receipt, elapsed


def reservation_path(config):
    if config.get("prior_preparation_stop"):
        return Path(config["package_root"]) / "launch-invocation-after-preparation-stop.json"
    return Path(config["trial_root"]) / "launch-invocation.json"


def ensure_unoccupied(config):
    root = Path(config["trial_root"])
    for name in ("run", "native-001", "sources-002-prelaunch", "inputs-003-native"):
        require(not os.path.lexists(root / name), "existing_attempt_or_input: " + name)
    previous = config.get("prior_preparation_stop")
    if previous:
        require(Path(previous["reservation"]["path"]) == root / "launch-invocation.json", "prior_reservation_path_mismatch")
        for expected in previous.values():
            require(binding(expected["path"]) == expected, "prior_preparation_record_drift")
        stop = read_json(previous["stop"]["path"])
        reservation = read_json(previous["reservation"]["path"])
        require(stop["stage"] == "PREPARATION_FAILED" and type(stop["native_preflight_invocations"]) is int
                and stop["native_preflight_invocations"] == 0, "previous_dispatch_not_reusable")
        require(Path(reservation["invocation"]) == Path(previous["stop"]["path"]).parent, "prior_stop_not_bound_to_reservation")
    require(not os.path.lexists(reservation_path(config)), "existing_attempt_or_input: launch-invocation.json")


def prepare(config, invocation, environment):
    emit({"stage": "VERIFYING_PRESERVATION", "probe": config["probe"], "worker": config["worker"]})
    write_new(invocation / "preservation.json", verify_preservation(config))
    attempt = invocation / "sources"
    argv = [config["probe"]["path"], "profile-sources", "--checkout-root", config["request"]["checkout_root"]]
    receipt, elapsed = capture_visible(argv, config, attempt, environment, "COLLECTING_SOURCES", SOURCE_BUDGET)
    require(receipt["process_exit_code"] == 0 and not receipt["timed_out"]
            and not receipt["interrupted"] and receipt["owned_probe_stopped"]
            and receipt["stderr"]["bytes"] == 0 and elapsed <= 30, "source_collection_failed")
    observed = read_json(attempt / "stdout.bin")
    matches = observed == read_json(config["approved_inventory"]["path"])
    write_new(invocation / "source-comparison.json", {
        "observed": binding(attempt / "stdout.bin"), "approved": config["approved_inventory"],
        "exact_inventory_match": matches, "elapsed_including_receipt_seconds": elapsed,
        "same_process_token_and_child_environment_as_dispatch": True})
    require(matches, "source_inventory_drift_requires_review")
    packet = invocation / "inputs"
    packet.mkdir(exist_ok=False)
    review = read_json(config["review_template"]["path"])
    require(len(review["findings"]) == 4 and all(value is False for value in review["findings"].values()),
            "unexpected_operator_findings")
    review.update(reviewer=config["reviewer"], trial_selection_ref=config["selection"]["path"],
                  source_inventory_ref=str(attempt / "stdout.bin"),
                  source_inventory_sha256=receipt["stdout"]["sha256"],
                  profile_sources=[{"path": row["path"], "sha256": row["sha256"]}
                                   for row in observed["entries"] if row["state"] == "file"])
    write_new(packet / "review.json", review)
    with (packet / "diagnostics.json").open("xb") as output:
        output.write(Path(config["diagnostics"]["path"]).read_bytes())
    request = copy.deepcopy(config["request"])
    request["profile"]["review_ref"] = str(packet / "review.json")
    request["profile"]["review_sha256"] = binding(packet / "review.json")["sha256"]
    request["diagnostics_ref"] = str(packet / "diagnostics.json")
    request["diagnostics_sha256"] = binding(packet / "diagnostics.json")["sha256"]
    write_new(packet / "request.json", request)
    paths = [packet / name for name in ("request.json", "review.json", "diagnostics.json")]
    paths += [attempt / "stdout.bin", invocation / "configuration.json", Path(__file__), HERE / "recorder.py", TRIAL / "supervisor.py"]
    paths += [Path(config[name]["path"]) for name in ("selection", "fixture", "probe", "worker")]
    write_new(packet / "input-manifest.json", [binding(path) for path in paths])
    return packet


def worker_observation(config):
    """Display an observation only; OW-04 still requires the Rust inspector."""
    path = Path(config["request"]["run_dir"]) / "journal.jsonl"
    try:
        with path.open("rb") as stream:
            data = stream.read(32 * 1024 * 1024 + 1)
        require(len(data) <= 32 * 1024 * 1024, "journal_display_limit")
        events = [json.loads(line) for line in data.splitlines()]
        exits = [row["data"].get("worker_exit_code") for row in events if row["kind"] == "process_exit"]
        code = exits[-1] if exits else None
        return {"observed_worker_exit_code": code if type(code) is int else None,
                "worker_outcome": "FAILURE_OBSERVED" if type(code) is int and code != 0 else "REQUIRES_RUST_INSPECTION",
                "inspection": "NOT_RUN", "observation_is_not_validation": True}
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        return {"worker_outcome": "UNKNOWN_MISSING_OR_UNREADABLE_JOURNAL", "inspection": "NOT_RUN"}


def operate(mode, config=None, parent_environment=None):
    require(mode in ("--prepare", "--run-once"), "explicit_prepare_or_run_once_required")
    config = selected_config() if config is None else config
    parent = os.environ if parent_environment is None else parent_environment
    invocations = Path(config["package_root"]) / "invocations"
    invocations.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:8]
    invocation = invocations / stamp
    invocation.mkdir(exist_ok=False)
    dispatches = 0
    stage = "PREPARATION_FAILED"
    try:
        write_new(invocation / "configuration.json", config)
        ensure_unoccupied(config)
        environment, environment_receipt = child_environment(parent)
        write_new(invocation / "environment.json", environment_receipt)
        if mode == "--run-once":
            write_new(reservation_path(config), {
                "status": "ONE_INVOCATION_RESERVED", "invocation": str(invocation),
                "selection": config["selection"], "executor": binding(Path(__file__)),
                "maximum_native_invocations": 1, "automatic_retries": 0})
        packet = prepare(config, invocation, environment)
        argv = [config["probe"]["path"], "preflight", "--request", str(packet / "request.json")]
        result = {"stage": "PREPARED", "packet": str(packet), "argv": argv,
                  "request": binding(packet / "request.json"), "native_preflight_invocations": 0,
                  "framework_acceptance": "NOT_EVALUATED"}
        code = 0
        if mode == "--run-once":
            stage = "DISPATCH_OR_RECORDING_FAILED"
            # Recheck selected bytes after preparation, immediately before dispatch.
            write_new(invocation / "pre-dispatch-preservation.json", verify_preservation(config))
            write_new(invocation / "dispatch.json", {"argv": argv, "cwd": config["workspace"],
                "input_manifest": binding(packet / "input-manifest.json"), "shell": False,
                "rust_total_seconds": 120, "recorder_total_seconds": 145, "automatic_retries": 0})
            dispatches = 1
            attempt = Path(config["trial_root"]) / "native-001"
            receipt, elapsed = capture_visible(argv, config, attempt, environment, "NATIVE_PREFLIGHT", NATIVE_BUDGET)
            result.update(stage="DIAGNOSTIC_RECORDED", native_preflight_invocations=1,
                          probe_exit_code=receipt["process_exit_code"], timed_out=receipt["timed_out"],
                          interrupted=receipt["interrupted"], owned_probe_stopped=receipt["owned_probe_stopped"],
                          spawn_error=receipt["spawn_error"], worker_tree_status=receipt["worker_tree_status"],
                          elapsed_including_receipt_seconds=elapsed, within_145_seconds=elapsed <= 145,
                          receipt=binding(attempt / "receipt.json"), **worker_observation(config))
            code = receipt["process_exit_code"] if receipt["process_exit_code"] is not None else 125
            if receipt["timed_out"] or receipt["interrupted"] or not receipt["owned_probe_stopped"] or elapsed > 145:
                code = 124
            result["operator_exit_code"] = code
        write_new(invocation / "result.json", result)
        emit(dict(result, invocation=str(invocation)))
        return code
    except (Exception, KeyboardInterrupt) as error:
        stopped = {"stage": stage, "error_type": type(error).__name__, "reason": str(error),
                   "native_preflight_invocations": dispatches, "automatic_retry": False,
                   "invocation": str(invocation), "framework_acceptance": "NOT_EVALUATED"}
        write_new(invocation / "stop.json", stopped)
        emit(stopped)
        return 3


def main(arguments):
    if arguments not in (["--prepare"], ["--run-once"]):
        emit({"stage": "USAGE", "usage": "diagnostic.py --prepare | --run-once"})
        return 2
    return operate(arguments[0])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
