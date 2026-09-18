"""Evidence consistency and preservation checks; no launch and no acceptance authority."""
import json
from pathlib import Path

from intake import (ROOT, WORKSPACE, PACKAGE, QA, MANIFEST, FIXTURE, INDEX_SHA,
                    binding, candidate_check, check_binding, sha256, utc_now, write)


def read(path):
    return json.loads(Path(path).read_bytes())


def main():
    assert sha256(QA / "artifact-index.json") == INDEX_SHA
    index = read(QA / "artifact-index.json")
    qa_checks = [check_binding(row) for row in index["artifacts"].values()]
    inputs = [check_binding(row) for row in read(QA / "input-bindings.json")]
    old_native = [check_binding(row) for row in read(ROOT / "prior-native-bindings.json")]
    before = read(ROOT / "intake-readback.json")
    snapshots = [check_binding(row) for row in before["snapshot_checks"]]
    candidate = candidate_check()
    assert candidate == before["candidate_files"]
    selected = []
    for version in ("inputs-001", "inputs-002-prelaunch"):
        bound = read(ROOT / version / "input-bindings.json")
        for key in ("fixture", "request", "review", "source_inventory", "policy", "worker", "binary"):
            selected.append({"version": version, "role": key, **check_binding(bound[key])})
        review = read(bound["review"]["path"])
        assert len(review["findings"]) == 4 and all(v is False for v in review["findings"].values())
    assert all(row["matches"] for row in qa_checks + inputs + old_native + snapshots + selected)
    first = read(ROOT / "sources-001/stdout.bin")
    launch = read(ROOT / "sources-002-prelaunch/stdout.bin")
    after = read(ROOT / "sources-003-after/stdout.bin")
    first_entries = {row["path"]: row for row in first["entries"]}
    launch_entries = {row["path"]: row for row in launch["entries"]}
    changed = [{"path": path, "before": first_entries.get(path), "prelaunch": launch_entries.get(path)}
        for path in sorted(set(first_entries) | set(launch_entries))
        if first_entries.get(path) != launch_entries.get(path)]
    assert launch == after
    assert (ROOT / "sources-002-prelaunch/stdout.bin").read_bytes() == (ROOT / "sources-003-after/stdout.bin").read_bytes()
    fixture = binding(FIXTURE / "task.json")
    assert fixture == read(ROOT / "native-001/receipt.json")["fixture"]
    assert sorted(p.name for p in FIXTURE.iterdir()) == ["task.json"]
    run = FIXTURE.parent / "run"
    journal_bytes = (run / "journal.jsonl").read_bytes()
    assert journal_bytes == (ROOT / "native-001/stdout.bin").read_bytes()
    events = [json.loads(line) for line in journal_bytes.splitlines()]
    assert [e["seq"] for e in events] == list(range(1, len(events) + 1))
    inspect = read(ROOT / "inspect-001/stdout.bin")
    assert inspect["events"] == events and inspect["truncated_tail"] == 0
    assert read(ROOT / "inspect-001/receipt.json")["native_exit_code"] == 0
    forbidden_kinds = {"profile_checked", "thread_bound", "turn_intent", "turn_bound"}
    assert not any(e["kind"] in forbidden_kinds for e in events)
    assert sum(e["kind"] == "server_started" for e in events) == 1
    diagnostics = [e["data"]["diagnostic"] for e in events if "diagnostic" in e["data"]]
    assert diagnostics == [
        {"schema_version": 1, "stage": "process_accounting", "rpc": "initialize",
         "checkpoint": "before_send", "predicate": "unexpected_process_count",
         "total_processes": 1, "active_processes": 0},
        {"schema_version": 1, "stage": "rpc", "rpc": "initialize", "predicate": "process_guard_rejected"},
    ]
    terminal = events[-1]["data"]
    assert events[-1]["kind"] == "terminal" and terminal["reason"] == "profile_unqualified"
    assert terminal["thread_id"] is None and terminal["turn_id"] is None
    assert terminal["tree_stopped"] is True and terminal["fixture_unchanged"] is True
    assert terminal["oracle"] == "not_evaluated"
    receipt = read(ROOT / "native-001/receipt.json")
    assert receipt["native_exit_code"] == 3 and not receipt["timed_out"]
    assert receipt["harness_stopped"] and receipt["parent_environment_unchanged"]
    assert receipt["stdout"] == binding(ROOT / "native-001/stdout.bin")
    assert receipt["stderr"] == binding(ROOT / "native-001/stderr.bin")
    assert receipt["recorder"] == binding(ROOT / "diagnostic.py")
    normalized = read(run / "request.json")
    original = read(ROOT / "inputs-002-prelaunch/request.json")
    for key in ("checkout_root", "run_dir", "worker_executable"):
        assert normalized[key].removeprefix("\\\\?\\").lower() == original[key].lower()
        normalized[key] = original[key]
    assert normalized == original
    assert (run / "profile-review.json").read_bytes() == (ROOT / "inputs-002-prelaunch/review.unqualified.json").read_bytes()
    assert (run / "task.json").read_bytes() == (FIXTURE / "task.json").read_bytes()
    runtime_inputs = read(run / "inputs.json")
    assert runtime_inputs["request_sha256"] == sha256(run / "request.json")
    assert runtime_inputs["profile_sha256"] == sha256(run / "profile-review.json")
    owned_pid = next(e["data"]["pid_observation"] for e in events if e["kind"] == "server_started")
    host_before = read(ROOT / "host-processes-before.json")
    host_after = read(ROOT / "host-processes-after.json")
    after_pids = {p["Id"] for p in host_after["processes"]}
    assert owned_pid not in after_pids and receipt["owned_pid"] not in after_pids
    retained_processes = {p["Id"] for p in host_before["processes"]}.issubset(after_pids)
    write(ROOT / "preservation-readback.json", {
        "utc": utc_now(), "qa_artifact_checks": qa_checks, "input_checks": inputs,
        "prior_native_checks": old_native, "snapshot_checks": snapshots,
        "candidate_files": candidate, "selected_input_checks": selected,
        "all_checks_match": True, "qa_index": binding(QA / "artifact-index.json"),
        "framework_acceptance": "NOT_EVALUATED",
    })
    write(ROOT / "source-refresh-readback.json", {
        "initial": binding(ROOT / "sources-001/stdout.bin"),
        "prelaunch": binding(ROOT / "sources-002-prelaunch/stdout.bin"),
        "after": binding(ROOT / "sources-003-after/stdout.bin"),
        "changed_entries_before_launch": changed, "prelaunch_after_bytes_equal": True,
        "entry_count": len(launch["entries"]),
        "scope": "Inventoried control inputs only; credential contents and unrelated runtime bookkeeping not inspected",
    })
    summary = {
        "utc": utc_now(), "native_attempts": 1, "native_retries": 0,
        "preflight_result": "BLOCKED", "native_exit_code": 3,
        "duration_seconds": receipt["duration_monotonic_ns"] / 1e9,
        "diagnostics": diagnostics, "required_process_counts": {"total": 1, "active": 1},
        "terminal": terminal, "journal_records": len(events),
        "initialize_sent": False, "config_read_sent": False, "thread_turn_dispatches": 0,
        "dispatch_basis": "Journal plus frozen protocol.rs guard-before-send ordering",
        "worker_pid_observation": owned_pid, "worker_exit_observation": terminal["worker_exit_code"],
        "source_review": "Reached initialize guard after mandatory post-spawn source review",
        "compiled_inspection_exit": 0, "compiled_inspection_state": inspect["state"],
        "held_handle_cleanup": terminal["tree_stopped"], "outer_containment_used": receipt["containment"] is not None,
        "fixture_unchanged": True, "source_inventory_unchanged_after_launch": True,
        "preexisting_observed_processes_still_present": retained_processes,
        "qa_artifacts_preserved": len(qa_checks), "inputs_preserved": len(inputs),
        "candidate_files_preserved": len(candidate), "snapshot_files_preserved": len(snapshots),
        "prior_native_files_preserved": len(old_native),
        "classification": "Native startup/liveness prerequisite BLOCKED; underlying cause UNRESOLVED",
        "classification_limits": "No demonstrated product defect or effective-profile predicate failure; current evidence does not distinguish host/profile startup prerequisite, launch/runtime compatibility, or an unobserved harness interaction",
        "next_unresolved_question": "Why did the pinned fixed-policy app-server become inactive before initialize?",
        "model_trials": "NOT_RUN", "WN_01_WN_02_credit": 0, "framework_acceptance": "NOT_EVALUATED",
    }
    write(ROOT / "observed-result.json", summary)
    print(json.dumps({"native_result": summary["preflight_result"], "predicate": diagnostics[0],
        "preserved": {"qa_artifacts": len(qa_checks), "inputs": len(inputs),
        "candidate": len(candidate), "snapshot": len(snapshots), "prior_native": len(old_native)},
        "changed_entries_before_launch": changed,
        "prelaunch_after_bytes_equal": True, "compiled_inspection_exit": 0}))


if __name__ == "__main__":
    main()
