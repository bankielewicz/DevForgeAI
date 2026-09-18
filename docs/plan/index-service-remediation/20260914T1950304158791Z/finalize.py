"""Retain and summarize observed remediation artifacts. Not an acceptance authority."""
import datetime
import difflib
import json
import platform
import re
import shutil
import subprocess
from pathlib import Path
from record import ROOT, PROJECT, QA, digest, manifest, write

initial = json.loads((ROOT / "initial-source-manifest.json").read_text(encoding="utf-8"))
current = manifest()
for attempt in ["coverage-final-002", "release-build", "fmt-final", "clippy-final"]:
    evidence = ROOT / "attempts" / attempt
    assert json.loads((evidence / "source-manifest.json").read_text(encoding="utf-8")) == current, attempt
    receipt = json.loads((evidence / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["exit_code"] == 0, attempt
    assert digest(evidence / "source-manifest.json") == receipt["source_manifest_sha256"], attempt
    for name in ["stdout.txt", "stderr.txt"]:
        assert digest(evidence / name) == receipt[name + "_sha256"], (attempt, name)
by_path = {row["path"]: row for row in current["files"]}
before = {row["path"]: row for row in initial["files"]}
original_copy = PROJECT.parent / "tmp" / "qa-20260914T191133863776Z" / "candidate"
changed = []
diffs = []
for path in sorted(set(before) | set(by_path)):
    old, new = before.get(path), by_path.get(path)
    if old and new and old["sha256"] == new["sha256"]:
        continue
    relative = Path(path).relative_to(PROJECT)
    changed.append({"path": path, "status": "added" if old is None else "modified" if new else "removed", "before": old, "after": new})
    old_bytes = b""
    if old:
        original = original_copy / relative
        assert digest(original) == old["sha256"], str(original)
        old_bytes = original.read_bytes()
    new_bytes = Path(path).read_bytes() if new else b""
    diffs.extend(difflib.unified_diff(old_bytes.decode("utf-8").splitlines(True), new_bytes.decode("utf-8").splitlines(True), fromfile="before/" + relative.as_posix(), tofile="after/" + relative.as_posix()))
write(ROOT / "source-manifest.json", current)
write(ROOT / "changed-files.json", changed)
(ROOT / "candidate.diff").write_text("".join(diffs), encoding="utf-8")
candidate = ROOT / "candidate"
candidate.mkdir(exist_ok=False)
for row in current["files"]:
    source = Path(row["path"])
    target = candidate / source.relative_to(PROJECT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert digest(target) == row["sha256"]

runtime = ROOT / "runtime"
runtime.mkdir(exist_ok=False)
builds = []
for name in ["devforgeai.exe", "devforgeai-indexd.exe", "devforgeai-tray.exe"]:
    source = PROJECT / "target" / "release" / name
    target = runtime / name
    shutil.copyfile(source, target)
    builds.append({"source": str(source), "retained": str(target), "bytes": target.stat().st_size, "sha256": digest(target)})
write(ROOT / "runtime-artifacts.json", {"candidate_manifest_sha256": digest(ROOT / "source-manifest.json"), "build_receipt": str(ROOT / "attempts" / "release-build" / "receipt.json"), "binaries": builds})

coverage = json.loads((ROOT / "coverage-final-002.json").read_text(encoding="utf-8"))["data"][0]
qa_inventory = json.loads((QA / "executed-test-inventory.json").read_text(encoding="utf-8"))
prior = {item["id"]: item for item in qa_inventory if item["platform"] == "windows"}
inventory = []
stdout = (ROOT / "attempts" / "coverage-final-002" / "stdout.txt").read_text(encoding="utf-8")
for name, result, reason in re.findall(r"^test (\S+) \.\.\. (ok|FAILED|ignored)(?:, ([^\n]*))?$", stdout, re.M):
    inventory.append({"id": name, "status": {"ok":"PASS", "FAILED":"FAIL", "ignored":"NOT_RUN"}[result], "reason": reason, "category": prior.get(name, {}).get("category", "new regression"), "original_QA_case": name in prior})
assert len({item["id"] for item in inventory}) == len(inventory)
original_units = [item for item in inventory if item["original_QA_case"] and item["category"] == "unit"]
assert len(original_units) == 18
product = [item for item in inventory if item["category"] != "setup"]
windows = [item for item in product if item["status"] != "NOT_RUN"]
def count(items):
    passing = sum(item["status"] == "PASS" for item in items)
    return {"passed": passing, "required": len(items), "percent": passing * 100 / len(items), "failed": sum(item["status"] == "FAIL" for item in items), "not_run": sum(item["status"] == "NOT_RUN" for item in items)}
metrics = {"platform":"Windows native", "source_manifest_sha256":digest(ROOT / "source-manifest.json"), "coverage":coverage["totals"]["lines"], "coverage_threshold":95, "coverage_result":"PASS" if coverage["totals"]["lines"]["covered"] * 100 >= coverage["totals"]["lines"]["count"] * 95 else "FAIL", "branch_coverage":"NOT_RUN", "original_declared_units":count(original_units), "native_windows_product_cases":count(windows), "all_declared_product_cargo_cases_including_WSL_not_run":count(product), "setup_tests":count([item for item in inventory if item["category"] == "setup"]), "per_file":[{"path":f["filename"], **f["summary"]["lines"]} for f in coverage["files"]], "Ubuntu":"NOT_RUN on corrected candidate; remote synchronization outside scope", "WSL":"NOT_RUN; two original ignored cases retained", "full_qualification":"INCOMPLETE", "framework_acceptance":"NOT_EVALUATED"}
write(ROOT / "metrics.json", metrics)
write(ROOT / "test-inventory.json", inventory)

preservation = []
for row in json.loads((ROOT / "inputs.json").read_text(encoding="utf-8-sig")):
    path = Path(row["path"])
    observed = digest(path)
    preservation.append({"path":str(path), "expected":row["sha256"], "observed":observed, "matches":observed == row["sha256"]})
handoff = json.loads((QA / "handoff-manifest.json").read_text(encoding="utf-8"))
for row in handoff["artifacts"]:
    path = Path(row["actual_path"])
    observed = digest(path)
    preservation.append({"path":str(path), "expected":row["sha256"], "observed":observed, "matches":observed == row["sha256"] and path.stat().st_size == row["bytes"]})
assert all(row["matches"] for row in preservation)
assert digest(PROJECT / "tests" / "qa_independent.rs") == digest(QA / "qa_independent.rs")
write(ROOT / "preservation.json", {"verified_inputs_and_original_QA_artifacts":preservation, "original_QA_oracle_copy_unchanged":True, "unrelated_original_candidate_files_unchanged":len(initial["files"]) - sum(row["status"] == "modified" for row in changed)})

tools = {"platform":platform.platform(), "python":platform.python_version(), "recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(), "commands":[]}
for argv in [["rustc", "-vV"], ["cargo", "-vV"], ["cargo", "llvm-cov", "--version"], ["rustup", "show", "active-toolchain"]]:
    result = subprocess.run(argv, cwd=PROJECT, capture_output=True, text=True, timeout=30)
    tools["commands"].append({"argv":argv, "cwd":str(PROJECT), "exit_code":result.returncode, "stdout":result.stdout, "stderr":result.stderr, "executable":shutil.which(argv[0])})
write(ROOT / "tools.json", tools)
print(json.dumps({"metrics":metrics, "changed_count":len(changed), "source_manifest_sha256":digest(ROOT / "source-manifest.json"), "builds":builds, "preservation_count":len(preservation)}, indent=2))
