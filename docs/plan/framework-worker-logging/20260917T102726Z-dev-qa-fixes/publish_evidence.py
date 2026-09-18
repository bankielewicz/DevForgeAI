"""Bind and read back development artifacts without closing QA or issuing acceptance."""
import json
import os
from pathlib import Path
import re
import shutil
import sys

from assess_evidence import ROOT, PROJECT, CANDIDATE, QA, binding, digest, now, read, verify, write


def walk(root, excluded=()):
    files, links = [], []
    for entry in sorted(os.scandir(root), key=lambda item: item.name):
        path = Path(entry.path)
        if path.name in excluded:
            continue
        stat = entry.stat(follow_symlinks=False)
        if stat.st_file_attributes & 0x400:
            links.append({"path": str(path), "target": os.readlink(path), "traversed": False})
        elif entry.is_dir(follow_symlinks=False):
            child_files, child_links = walk(path)
            files.extend(child_files)
            links.extend(child_links)
        else:
            files.append(path)
    return files, links


started = now()
assert ROOT == Path(r"C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T102726Z-dev-qa-fixes")
assert CANDIDATE == Path(r"C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes")
assert digest(QA / "handoff-manifest.json") == "0c6949f4379e7c469643f34ad6d4b1f664f48177f8865d12dfedd7cbe901019e"
checks = []
for name in ["candidate-manifest.json", "input-manifest.json", "specification-bindings.json", "preserved-manifest.json", "binary-manifest.json"]:
    entries = read(QA / name)
    drift = verify(entries)
    assert not drift, drift
    checks.append({"manifest": binding(QA / name), "files": len(entries), "mismatches": drift})
handoff_entries = list(read(QA / "handoff-manifest.json")["entries"].values())
assert not verify(handoff_entries)
checks.append({"manifest": binding(QA / "handoff-manifest.json"), "files": len(handoff_entries), "mismatches": []})
prior_evidence = read(QA / "evidence-manifest.json")
assert not verify(prior_evidence["files"])
for entry in prior_evidence["reparse_points"]:
    assert os.readlink(entry["path"]) == entry["target"], entry["path"]
checks.append({"manifest": binding(QA / "evidence-manifest.json"), "files": len(prior_evidence["files"]),
               "reparse_points": len(prior_evidence["reparse_points"]), "mismatches": []})
assert not verify(read(ROOT / "input-bindings.json"))
candidate = read(ROOT / "candidate-manifest.json")
assert not verify(candidate)
candidate_files, candidate_links = walk(CANDIDATE)
assert not candidate_links
assert {str(path) for path in candidate_files} == {entry["path"] for entry in candidate}
build = read(ROOT / "build-manifest.json")
assert not verify(build["executables"])
assert not verify([build["candidate_manifest"], build["main_executable"], build["toolchain"], *build["attempts"]])
write("preservation-readback-final.json", {"checked_at": now(), "checks": checks,
      "current_inputs": len(read(ROOT / "input-bindings.json")), "corrected_files": len(candidate),
      "main_executable": build["main_executable"], "corrected_membership_unchanged": True,
      "powershell_helper": binding(PROJECT / "Start-CodexAppServerDiagnostic.ps1"),
      "method": "Actual literal regular-file readback, lengths and SHA256; reparse targets checked without traversal"})

observation_summary = []
for attempt in ["01-red", "02-green", "04-refactor", "08-coverage"]:
    files, _ = walk(ROOT / "attempts" / attempt / "fixtures")
    observations = []
    other_families = []
    inspection_fields = {"expected", "library", "cli_exit_code", "read_only", "expectation_met"}
    for path in files:
        if path.name.endswith("-observation.json"):
            value = read(path)
            if set(value) == inspection_fields:
                observations.append(value)
            else:
                other_families.append(binding(path))
    assert len(observations) == 201, "inspection record inventory mismatch"
    count = sum(value["expectation_met"] for value in observations)
    assert observations and all(value["read_only"] for value in observations)
    if attempt != "01-red":
        assert count == len(observations)
    observation_summary.append({"attempt": attempt, "observations": len(observations),
                                "expectations_met": count, "expectations_not_met": len(observations) - count,
                                "read_only": len(observations), "other_observation_families": other_families})
write("inspection-observation-summary.json", observation_summary)

old_harness = PROJECT / "docs/plan/framework-worker-logging/20260917T014842Z-dev/qa-harness"
supplemental = []
for name in ["Cargo.lock", "cases.rs", "peer.rs", "expected.json"]:
    original = old_harness / name
    current = ROOT / "supplemental-harness" / name
    assert digest(original) == digest(current)
    supplemental.append({"original": binding(original), "current": binding(current), "same_bytes": True})
write("supplemental-bindings.json", {"unchanged": supplemental,
      "manifest": binding(ROOT / "supplemental-harness/Cargo.toml"),
      "difference": "Only dependency path selects corrected candidate; separately executed inherited developer regression"})

common = {"qa_status": "OPEN", "development_status": "FIX_REPORTED", "independent_retest": "NOT_RUN",
          "candidate_manifest": binding(ROOT / "candidate-manifest.json"),
          "runtime_source": binding(CANDIDATE / "src/journal.rs"),
          "regressions": binding(CANDIDATE / "tests/inspection_consistency.rs"),
          "red": str(ROOT / "attempts/01-red/receipt.json"),
          "green": str(ROOT / "attempts/02-green/receipt.json"),
          "refactor": str(ROOT / "attempts/04-refactor/receipt.json"),
          "final_campaign": str(ROOT / "attempts/08-coverage/receipt.json")}
write("resolution-map.json", [
    {**common, "id": "QA-LOG-01", "requirements": ["LG-02", "LG-03", "LG-06", "logging-design case12"],
     "correction": "Retain typed Capture through terminal; require drain_complete and no byte overflow for current successful outcomes; existing validate enforces both EOF and absent reader errors.",
     "tests": ["qa_log_01_completed_requires_complete_capture_at_every_level", "qa_log_01_preflight_requires_complete_capture", "current_schema_one_capture_cannot_bypass_success_checks"],
     "compatibility": "Actual failed/blocked/cancelled/timed_out/cleanup_uncertain controls, incomplete capture, nullable exits, historical schema1/2, interrupted prefix and dropped detail pass.",
     "retest": "Independently repeat each both-stream mutation against fresh completed and synthetic preflight records, plus failure/history/read-only controls; do not reuse exclusive old attempt paths."},
    {**common, "id": "QA-LOG-02", "requirements": ["LG-02", "LG-06", "base sections4/7"],
     "correction": "Require worker_exit_code key before Option<u32> decoding; retain typed observation; successful current terminals require matching independently observed zero exits.",
     "tests": ["qa_log_02_completed_requires_present_typed_matching_exit", "qa_log_02_preflight_requires_present_typed_matching_exit", "qa_log_02_failed_run_still_requires_post_stop_field_presence"],
     "compatibility": "Explicit null remains valid for legitimate failure observations; matching nonzero failed child controls pass; absent mandatory fields reject; historical records retain schema semantics.",
     "retest": "Independently test missing/null/type/range and 29-vs-0 contradictions, matching successful zero and failed nonzero/null, both success branches and no replay. Closure belongs to separately selected QA."},
])
shutil.copyfile(QA / "specification-bindings.json", ROOT / "specification-bindings.json")

readme = CANDIDATE / "README.md"
local_links = []
for target in re.findall(r"\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
    if "://" in target or target.startswith("#"):
        continue
    path = (readme.parent / target.split("#", 1)[0]).resolve()
    assert path.exists(), str(path)
    local_links.append({"target": target, "resolved": str(path), "exists": True})
write("documentation-review.json", {"document": binding(readme), "local_links": local_links,
      "factual_review": "New paragraph agrees with runtime checks and executed tests; build command resolves corrected Cargo.toml; independent QA/native/acceptance boundaries explicit"})
write("checkpoint.json", {"timestamp": now(), "scope": ["QA-LOG-01", "QA-LOG-02"],
      "project": str(PROJECT), "candidate": str(CANDIDATE), "evidence_root": str(ROOT),
      "source_identity": binding(ROOT / "source-identity.json"), "metrics": binding(ROOT / "metrics.json"),
      "completed": ["red", "green", "refactor", "full offline checks", "preservation readback"],
      "owned_running_jobs": [], "selected_implementation_remaining": [],
      "publication_state": "Consult final-readback.json for completed publication verification",
      "next_owner": "independently selected QA retest", "qa_findings": "OPEN; FIX_REPORTED by development",
      "framework_acceptance": "NOT_EVALUATED", "native_codex": "NOT_RUN"})

files, links = walk(ROOT, {"build-target", "coverage-target", "evidence-manifest.json", "handoff-manifest.json", "final-readback.json"})
write("evidence-manifest.json", {"timestamp": now(), "files": [binding(path) for path in files],
      "reparse_points": links, "scope": "All new regular evidence excluding Cargo targets and this manifest/final bindings; binaries separately bound", "traverse_reparse_points": False})
required = ["context.md", "plan.md", "delivery.md", "resolution-map.json", "checkpoint.json",
            "intake-verification.json", "input-bindings.json", "specification-bindings.json",
            "candidate-manifest.json", "source-identity.json", "build-manifest.json", "changed-file-manifest.json",
            "candidate.patch", "declared-cases.json", "coverage-source-inventory.json", "coverage.json",
            "coverage-analysis.json", "metrics.json", "case-results.json", "execution-record.jsonl",
            "preservation-readback.json", "preservation-readback-final.json", "publication-attempt-01.json",
            "inspection-observation-summary.json", "implementation-review.md",
            "documentation-review.json", "evidence-manifest.json", "toolchain.json", "supplemental-bindings.json"]
entries = {name: {"required_path": str(ROOT / name), **binding(ROOT / name)} for name in required}
assert not verify(list(entries.values()))
write("handoff-manifest.json", {"run_id": ROOT.name, "project": str(PROJECT),
      "original_corrected_source_selection": str(CANDIDATE), "candidate_root": str(CANDIDATE),
      "selected_evidence_value": str(ROOT.parent), "required_destination": str(ROOT), "actual_destination": str(ROOT),
      "original_qa_handoff": binding(QA / "handoff-manifest.json"), "defects": ["QA-LOG-01", "QA-LOG-02"],
      "development_status": "FIX_REPORTED", "qa_findings": "OPEN", "independent_qa_retest": "NOT_RUN",
      "native_codex": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED", "entries": entries})
published = read(ROOT / "handoff-manifest.json")
assert all(entry["required_path"] == entry["path"] for entry in published["entries"].values())
assert not verify(list(published["entries"].values()))
assert not verify(read(ROOT / "evidence-manifest.json")["files"])
assert not verify(read(ROOT / "candidate-manifest.json"))
write("final-readback.json", {"started_utc": started, "ended_utc": now(), "cwd": os.getcwd(),
      "command": [sys.executable, "-B", "-X", "utf8", str(Path(__file__)), *sys.argv[1:]],
      "script_sha256": digest(__file__), "exit_code": 0,
      "required_candidate": str(CANDIDATE), "actual_candidate": str(CANDIDATE),
      "required_evidence_root": str(ROOT), "actual_evidence_root": str(ROOT),
      "required_files_verified": len(entries), "regular_evidence_files_verified": len(files),
      "development_delivery": "COMPLETE: selected two-defect source, offline checks and artifact delivery only",
      "qa_findings": "OPEN; development FIX_REPORTED", "framework_acceptance": "NOT_EVALUATED",
      "handoff_manifest": binding(ROOT / "handoff-manifest.json")})
print(json.dumps({"handoff": binding(ROOT / "handoff-manifest.json"), "final_readback": binding(ROOT / "final-readback.json"),
                  "observations": observation_summary, "old_evidence_files_preserved": len(prior_evidence["files"])}, indent=2))
