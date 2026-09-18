"""Aggregate existing QA evidence; never build, launch a worker, or change candidate files."""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
PROJECT = Path("C:/Projects/DevForgeAI")


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True)
        stream.write("\n")


manifest_names = [
    "candidate-manifest.json", "input-manifest.json", "preserved-manifest.json",
    "qa-helper-manifest-v2.json", "binary-manifest.json",
]
checks = []
for name in manifest_names:
    entries = read(name)
    assert isinstance(entries, list), name
    for item in entries:
        path = Path(item["path"])
        actual = digest(path)
        assert actual == item["sha256"].lower(), str(path)
        assert path.stat().st_size == item["bytes"], str(path)
    checks.append({"manifest": name, "sha256": digest(ROOT / name), "verified_entries": len(entries), "mismatches": []})
binary = read("independent-binary-v2.json")
assert digest(Path(binary["Path"])) == binary["Hash"].lower()
checks.append({"manifest": "independent-binary-v2.json", "verified_entries": 1, "mismatches": []})

required = read("required-cases.json")
package = read("package-results.json")
assert len(required) == 166 and len(package) == 152
assert all(item["status"] == "PASS" for item in package)
cases = [dict(item) for item in package]
attempts = []
for receipt_path in sorted((ROOT / "attempts").glob("*/receipt.json")):
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    if "action" not in receipt:
        assert receipt_path.parent.name == "24-cli-confirm"
        assert all(result["exit_code"] == 0 and result["state"] == "completed" and result["unchanged"] for result in receipt["results"])
        attempts.append({"attempt": receipt_path.parent.name, "action": "read-only compiled inspector confirmation", "exit_codes": [r["exit_code"] for r in receipt["results"]], "status": "CONFIRMED_PRODUCT_FAILURES", "receipt": str(receipt_path)})
        continue
    assert not receipt["timed_out"] and receipt.get("ended_utc"), str(receipt_path)
    for output in receipt["outputs"]:
        assert digest(Path(output["path"])) == output["sha256"], output["path"]
    expected_exit = 101 if receipt["attempt"] in ["06-qa01", "16-qa09"] else 0
    assert receipt["exit_code"] == expected_exit, str(receipt_path)
    attempts.append({key: receipt.get(key) for key in ["attempt", "action", "case", "exit_code", "elapsed_seconds", "started_utc", "ended_utc", "timed_out"]} | {"receipt": str(receipt_path)})

for item in required[152:]:
    item = dict(item)
    if item["id"] == "SUP-01":
        attempt = "21-supplement"
    else:
        number = int(item["id"].split("-")[1])
        attempt = f"{7 + number:02d}-qa{number:02d}"
    stdout = (ROOT / "attempts" / attempt / "stdout.txt").read_text(encoding="utf-8-sig")
    matches = re.findall(r"^test ([^\r\n]+) \.\.\. (ok|FAILED)\s*$", stdout, re.MULTILINE)
    assert len(matches) == 1, (attempt, matches)
    item.update({"status": "PASS" if matches[0][1] == "ok" else "FAIL", "attempt": attempt, "executed_name": matches[0][0]})
    if item["id"] == "QA-01":
        item["retained_prior_attempt"] = {"attempt": "06-qa01", "status": "ERROR", "cause": "QA-H01 junction setup", "superseded_only_for_complete_case_count": True}
    if item["id"] == "QA-09":
        item["findings"] = ["QA-LOG-01", "QA-LOG-02"]
    cases.append(item)
assert [item["id"] for item in cases] == [item["id"] for item in required]
counts = Counter(item["status"] for item in cases)
assert counts == {"PASS": 165, "FAIL": 1}, counts
coverage = read("coverage-analysis.json")
assert coverage["line_floor_pass"] and coverage["unit_floor_pass"]
assert digest(ROOT / "coverage.json") == coverage["coverage_sha256"]

documents = [
    PROJECT / "devforgeai/experiments/codex-worker-probe-logging/README.md",
    PROJECT / "devforgeai/experiments/codex-worker-probe-logging/logging-contract.md",
]
for item in read("input-manifest.json"):
    path = Path(item["path"])
    if path.suffix == ".md" and (
        "docs/specs/framework/runtime" in path.as_posix()
        or path.name in ["logging-design.md", "investigation-report.md", "diagnostic-contract.md", "delivery.md", "qa-handoff.md"]
    ):
        documents.append(path)
links = []
for path in sorted(set(documents)):
    contents = path.read_text(encoding="utf-8-sig")
    without_fences = re.sub(r"```.*?```", "", contents, flags=re.DOTALL)
    for destination in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", without_fences):
        destination = destination.strip().strip("<>")
        parts = urlsplit(destination)
        if parts.scheme or not parts.path:
            continue
        resolved = (path.parent / unquote(parts.path)).resolve()
        links.append({"source": str(path), "destination": destination, "resolved": str(resolved), "exists": resolved.exists()})
write("documentation-review.json", {
    "reviewed_documents": [str(p) for p in sorted(set(documents))],
    "local_links": links,
    "broken_links": [item for item in links if not item["exists"]],
    "method": "Manual requirement and factual review plus local inline Markdown destination existence check; code fences and remote/fragment-only links excluded. No claim of native execution or protected acceptance inferred from documentation.",
    "factual_findings": ["LG-06 mandatory completed-evidence validity is violated by QA-LOG-01 and QA-LOG-02; implementation claims are reduced to FAIL in the QA report.", "README's historical 20-case wording describes inherited WF groups, not this run's declared166-case denominator."]
})
write("case-results.json", cases)
write("attempt-index.json", attempts)
write("final-identity-check.json", {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "checks": checks, "problems": [], "candidate_files": 67, "preserved_files": 116, "input_files": 37})
write("metrics.json", {
    "platform": "Windows x64", "overall_platforms": ["Windows x64"],
    "line_coverage": {"passing": 3858, "required": 4041, "percent": coverage["line_percent"], "floor": 95, "status": "PASS", "scope": "complete152-case package campaign; no supplemental or independent cases contribute"},
    "unit_test_rate": {"passing": 49, "required": 49, "percent": "100", "floor": 95, "status": "PASS"},
    "project_suite_rate": {"passing": 165, "required": 166, "percent": str(Decimal(165) * 100 / Decimal(166)), "floor": 95, "status": "PASS"},
    "package_integration": {"passing": 103, "required": 103},
    "supplemental_integration": {"passing": 1, "required": 1},
    "independent_acceptance": {"passing": 12, "required": 13, "percent": str(Decimal(12) * 100 / Decimal(13)), "separate_numeric_floor": None, "conformance_status": "FAIL"},
    "unique_case_status_counts": dict(counts), "retained_prior_harness_errors": ["06-qa01"],
    "skipped_or_unexecuted_required_cases": [], "metric_stop_trigger": None,
    "verdict": "FAIL", "basis": ["QA-LOG-01", "QA-LOG-02"],
    "native_codex": "NOT_RUN", "branch_coverage": "NOT_RUN", "framework_acceptance": "NOT_EVALUATED"
})
print(json.dumps({"cases": dict(counts), "identity_checks": checks, "documentation_count": len(set(documents)), "links": len(links), "broken_links": [item for item in links if not item["exists"]]}, indent=2))
