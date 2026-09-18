"""Read executed development evidence; no framework policy or acceptance authority."""
from __future__ import annotations

import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).parent
PROJECT = Path(r"C:\Projects\DevForgeAI")
CANDIDATE = PROJECT / "devforgeai/experiments/codex-worker-probe-logging-qa-fixes"
FAILED = PROJECT / "devforgeai/experiments/codex-worker-probe-logging"
QA = PROJECT / "docs/plan/framework-worker-logging/20260917T023835Z-qa"


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def binding(path):
    path = Path(path)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(name, value):
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=True)
        handle.write("\n")


def verify(entries):
    mismatches = []
    for entry in entries:
        path = Path(entry["path"])
        if not path.is_file() or path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
            mismatches.append(str(path))
    return mismatches


def tests(attempt):
    directory = ROOT / "attempts" / attempt
    output = (directory / "stdout.txt").read_text(encoding="utf-8-sig")
    pairs = re.findall(r"^test (.+?) \.\.\. (ok|FAILED|ignored)\s*$", output, re.M)
    assert len({name for name, _ in pairs}) == len(pairs), "duplicate case identity"
    summaries = re.findall(r"test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored; (\d+) measured; (\d+) filtered out", output)
    assert summaries, "missing terminal test summaries"
    counts = [sum(int(row[i]) for row in summaries) for i in range(5)]
    assert counts[:3] == [sum(state == key for _, state in pairs) for key in ["ok", "FAILED", "ignored"]]
    assert counts[3:] == [0, 0], "unexpected measured/filtered cases"
    return {name: state for name, state in pairs}


def fraction(passed, total):
    return {"passing": passed, "required": total, "exact_percent": f"100*{passed}/{total}",
            "percent": 100 * passed / total, "meets_95_percent": passed * 100 >= total * 95}


def assess():
    started = now()
    declared = read(ROOT / "declared-cases.json")
    package = tests("08-coverage")
    supplemental = tests("09-supplemental")
    assert set(package) == set(declared["package_cases"])
    assert set(supplemental) == set(declared["supplemental"])
    cases = [{"name": name, "status": "PASS" if status == "ok" else status,
              "category": "unit" if "::" in name else "integration", "attempt": "08-coverage"}
             for name, status in package.items()]
    cases.extend({"name": name, "status": "PASS" if status == "ok" else status,
                  "category": "supplemental", "attempt": "09-supplemental"}
                 for name, status in supplemental.items())
    units = [case for case in cases if case["category"] == "unit"]
    assert len(units) == declared["unit_count"] == 49
    assert len(cases) == declared["required_project_count"] == 163
    source_files = read(ROOT / "coverage-source-inventory.json")
    assert not verify(source_files), "coverage source drift"
    source_paths = {os.path.normcase(entry["path"]): entry for entry in source_files}
    coverage = read(ROOT / "coverage.json")
    files = []
    for data in coverage["data"]:
        for entry in data["files"]:
            path = os.path.normcase(entry["filename"])
            assert path in source_paths, f"unexpected coverage file: {path}"
            lines = entry["summary"]["lines"]
            files.append({**source_paths[path], "lines": lines["count"], "covered": lines["covered"],
                          "reported_percent": lines["percent"]})
    assert len({file["path"] for file in files}) == len(files)
    omitted = set(source_paths) - {os.path.normcase(file["path"]) for file in files}
    assert omitted <= {os.path.normcase(str(CANDIDATE / "src/lib.rs"))}, f"missing runtime files: {omitted}"
    line_total = sum(file["lines"] for file in files)
    line_covered = sum(file["covered"] for file in files)
    assert sum(data["totals"]["lines"]["count"] for data in coverage["data"]) == line_total
    assert sum(data["totals"]["lines"]["covered"] for data in coverage["data"]) == line_covered
    attempts = [read(path) for path in sorted((ROOT / "attempts").glob("*/receipt.json"))]
    assert {r["attempt_id"] for r in attempts} == {row["attempt_id"] for row in
        (json.loads(line) for line in (ROOT / "execution-record.jsonl").read_text(encoding="utf-8-sig").splitlines())}
    assert all(not receipt["timed_out"] for receipt in attempts)
    assert all(receipt["exit_code"] == (101 if receipt["attempt_id"] == "01-red" else 0) for receipt in attempts)
    candidate = [{**binding(path), "relative_path": path.relative_to(CANDIDATE).as_posix()}
                 for path in sorted(CANDIDATE.rglob("*")) if path.is_file()]
    for attempt in ["04-refactor", "05-list", "06-fmt-check", "07-clippy", "08-coverage", "09-supplemental", "10-build"]:
        assert not verify(read(ROOT / "attempts" / attempt / "source-manifest.json")), f"candidate drift since {attempt}"
    original = read(QA / "candidate-manifest.json")
    assert not verify(original)
    old = {Path(entry["path"]).relative_to(FAILED).as_posix(): entry for entry in original}
    changed = []
    patch = []
    for entry in candidate:
        rel = entry["relative_path"]
        before = old.pop(rel, None)
        if before and before["sha256"] == entry["sha256"]:
            continue
        changed.append({"relative_path": rel, "change": "modified" if before else "added", "before": before, "after": entry})
        old_text = Path(before["path"]).read_text(encoding="utf-8").splitlines(keepends=True) if before else []
        new_text = Path(entry["path"]).read_text(encoding="utf-8").splitlines(keepends=True)
        patch.extend(difflib.unified_diff(old_text, new_text, fromfile="a/" + rel, tofile="b/" + rel))
    assert not old, "unexpected deletion"
    assert {entry["relative_path"] for entry in changed} == {"src/journal.rs", "tests/inspection_consistency.rs", "README.md"}
    metrics = {"scope": "Development offline checks only; independent QA findings remain OPEN",
               "platform": "Windows x64, native C:", "line_coverage": fraction(line_covered, line_total),
               "required_units": fraction(sum(case["status"] == "PASS" for case in units), len(units)),
               "required_project_suite": fraction(sum(case["status"] == "PASS" for case in cases), len(cases)),
               "failed": sum(case["status"] == "FAILED" for case in cases),
               "ignored": sum(case["status"] == "ignored" for case in cases),
               "errored": 0, "blocked": 0, "unexecuted": 0,
               "branch_coverage": "NOT_RUN: unstable collector feature and no installed nightly",
               "native_codex": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED"}
    write("candidate-manifest.json", candidate)
    write("changed-file-manifest.json", changed)
    with (ROOT / "candidate.patch").open("x", encoding="utf-8", newline="\n") as handle:
        handle.writelines(patch)
    write("case-results.json", cases)
    write("metrics.json", metrics)
    write("coverage-analysis.json", {"raw": binding(ROOT / "coverage.json"), "files": files,
          "declaration_only_files_without_executable_lines": sorted(omitted),
          "exclusions": "tests/support and dependencies only; no executable first-party exclusions",
          "totals": metrics["line_coverage"]})
    identity_bytes = json.dumps([{key: entry[key] for key in ["relative_path", "bytes", "sha256"]}
                                for entry in candidate], sort_keys=True, separators=(",", ":")).encode("utf-8")
    write("source-identity.json", {"root": str(CANDIDATE), "files": len(candidate),
          "manifest": binding(ROOT / "candidate-manifest.json"),
          "content_sha256": hashlib.sha256(identity_bytes).hexdigest(),
          "scheme": "SHA256 UTF8 compact sorted-key JSON of sorted relative_path/bytes/sha256 records"})
    write("build-manifest.json", {"candidate_manifest": binding(ROOT / "candidate-manifest.json"),
          "main_executable": binding(ROOT / "build-target/debug/devforgeai-codex-worker-probe.exe"),
          "executables": [binding(path) for target in ["build-target", "coverage-target"]
                          for path in sorted((ROOT / target).rglob("*.exe"))],
          "toolchain": binding(ROOT / "toolchain.json"), "attempts": [binding(ROOT / "attempts" / r["attempt_id"] / "receipt.json") for r in attempts]})
    write("assessment-receipt.json", {"started_utc": started, "ended_utc": now(), "executable": sys.executable,
          "argv": sys.argv, "cwd": os.getcwd(), "script": binding(__file__), "exit_code": 0})
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    assert sys.argv[1:] == ["assess"]
    assess()
