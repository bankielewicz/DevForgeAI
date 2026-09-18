import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SESSION = ROOT.parent
WORKSPACE = Path(r"C:\Projects\DevForgeAI")
CANDIDATE = WORKSPACE / "devforgeai/experiments/codex-worker-probe"
MANIFEST = WORKSPACE / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-manifest.json"
EXPECTED_MANIFEST = "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


assert bind(MANIFEST)["sha256"] == EXPECTED_MANIFEST
manifest = load(MANIFEST)
for entry in manifest:
    observed = bind(CANDIDATE / entry["path"])
    assert observed["bytes"] == entry["bytes"]
    assert observed["sha256"] == entry["sha256"]

summary_path = ROOT / "runtime/04-run/summary.json"
summary = load(summary_path)
early = summary["early_exit"]
control = summary["receive_control"]
digest = "d3cf90ebd82863af99e57c32156dd7b3a6645c3877eccde5e26aa19e12f01fca"
assert summary["outcome"] == "observed" and summary["native_codex_launched"] is False
assert early["child_exit_code"] == 23 and early["counts_before"] == {"total": 1, "active": 0}
assert early["journal_stderr_events"] == []
assert early["queued_receiver_stderr"] == [{"bytes": 38, "sha256": digest}]
assert early["tree_stopped"] is True and early["active_after"] == 0
assert control["counts_before"] == {"total": 1, "active": 1}
assert control["result"] == {"Ok": {"synthetic": "initialize-ok"}}
assert control["journal_stderr_events"][0]["data"] == {
    "stream": "stderr", "bytes": 38, "sha256": digest, "content": "omitted"
}
assert control["tree_stopped"] is True and control["active_after"] == 0
assert early["thread_id"] is None and early["turn_id"] is None
assert control["thread_id"] is None and control["turn_id"] is None

receipts = {name: load(ROOT / f"attempts/{name}/receipt.json") for name in ["01-build", "02-run", "03-run", "04-run"]}
assert receipts["01-build"]["exit_code"] == 0
assert receipts["02-run"]["exit_code"] == 101
assert receipts["03-run"]["exit_code"] == 101
assert receipts["04-run"]["exit_code"] == 0
for receipt in receipts.values():
    assert receipt["candidate_files_checked"] == 58
    assert receipt["candidate_matches_manifest_before"] is True
    assert receipt["candidate_matches_manifest_after"] is True

dependency = (ROOT / "target/debug/startup-repro.d").read_text(encoding="utf-8")
for source in [
    "diagnostic.rs", "effective_profile.rs", "journal.rs", "launch_policy.rs",
    "native_identity.rs", "oracle.rs", "process_windows.rs", "profile_sources.rs",
    "protocol.rs", "request.rs", "runner.rs",
]:
    assert source in dependency

verification = {
    "schema_version": 1,
    "candidate_manifest_sha256": EXPECTED_MANIFEST,
    "candidate_files_verified_current": len(manifest),
    "retained_attempt_exit_codes": {name: receipt["exit_code"] for name, receipt in receipts.items()},
    "declared_cases_observed": ["SR-01", "SR-02"],
    "source_modules_compiler_mapped": 11,
    "process_cleanup": {"SR-01": {"tree_stopped": True, "active": 0}, "SR-02": {"tree_stopped": True, "active": 0}},
    "native_codex_launched": False,
}
(ROOT / "verification.json").write_text(json.dumps(verification, indent=2), encoding="utf-8")

selected = [
    SESSION / "offline-reproduction.md",
    ROOT / "test-plan.md",
    ROOT / "integrity-review.md",
    ROOT / "record.py",
    ROOT / "seal.py",
    ROOT / "verification.json",
    ROOT / "target/debug/startup-repro.d",
    ROOT / "target/debug/startup-repro.exe",
    ROOT / "target/debug/synthetic-peer.exe",
]
for folder in [ROOT / "harness", ROOT / "attempts", ROOT / "runtime"]:
    selected.extend(path for path in folder.rglob("*") if path.is_file())
selected = sorted(set(selected), key=lambda path: str(path).lower())
index = {
    "schema_version": 1,
    "root": str(SESSION),
    "artifacts": {
        str(path.relative_to(SESSION)).replace("\\", "/"): bind(path)
        for path in selected
    },
}
(ROOT / "artifact-index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
print(json.dumps({"verified": True, "artifacts": len(selected)}))
