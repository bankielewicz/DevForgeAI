"""Publish and verify QA evidence bindings; no product mutation or acceptance authority."""
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
plan = root.parent.parent


def read(name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    path = root / name
    if path.exists():
        raise RuntimeError("Refusing to replace final artifact: " + str(path))
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


checks = []
for name in ("source-manifest.json", "inputs.json"):
    rows = read(name)["files"]
    for row in rows:
        path = Path(row["path"])
        assert digest(path) == row["sha256"], str(path)
        assert path.stat().st_size == row["bytes"], str(path)
    checks.append({"check": name + " current byte identity", "files": len(rows), "result": "PASS"})

prior = json.loads((plan / "handoff-manifest.json").read_text(encoding="utf-8-sig"))
for row in prior["artifacts"]:
    assert digest(Path(row["actual_path"])) == row["sha256"], row["actual_path"]
checks.append({"check": "prior plan artifacts preserved", "files": len(prior["artifacts"]), "result": "PASS"})

binding = read("binding.json")
assert digest(Path(binding["selected_plan"])) == binding["plan_sha256"]
for row in read("source-manifest.json")["files"]:
    relative = Path(row["path"]).relative_to(Path(binding["candidate_original"]))
    assert digest(Path(binding["candidate_copy"]) / relative) == row["sha256"]
checks.append({"check": "Windows QA copy original source identity", "files": 48, "result": "PASS"})

metrics = read("metrics.json")
inventory = read("executed-test-inventory.json")
for platform, expected in (("windows", (46, 2, 2, 2626, 3442)), ("ubuntu", (46, 2, 0, 2075, 2786))):
    rows = [r for r in inventory if r["platform"] == platform]
    counts = Counter(r["status"] for r in rows)
    assert counts["PASS"] == expected[0] and counts["FAIL"] == expected[1]
    assert len(rows) == sum(expected[:3])
    units = [r for r in rows if r["category"] == "unit"]
    assert len(units) == 18 and sum(r["status"] == "PASS" for r in units) == 16
    coverage = metrics[platform]["line_coverage"]
    assert (coverage["covered"], coverage["count"]) == expected[3:]
    assert abs(coverage["percent"] - 100 * coverage["covered"] / coverage["count"]) < 1e-9
    raw_path = "coverage.json" if platform == "windows" else "ubuntu/coverage.json"
    raw = read(raw_path)["data"][0]["totals"]["lines"]
    assert raw["covered"] == coverage["covered"] and raw["count"] == coverage["count"]
    assert len(metrics[platform]["native_independent"]) == 9
    assert all(r["status"] == "PASS" for r in metrics[platform]["native_independent"])
checks.append({"check": "metrics match inventory and raw LLVM line totals", "result": "PASS"})

scenarios = read("acceptance-results.json")
assert {r["scenario"] for r in scenarios} == {"DS-A%02d" % i for i in range(1, 20)}
report = (root / "qa-report.md").read_text(encoding="utf-8-sig")
assert set(re.findall(r"\| (DS-\d{3}) \|", report)) == {"DS-%03d" % i for i in range(1, 27)}
links = []
for name in ("qa-report.md", "qa-fix.md", "dev-handoff.md"):
    content = (root / name).read_text(encoding="utf-8-sig")
    assert not re.search(r"\bTODO\b|<project>|<specification>", content)
    for target in re.findall(r"\]\(([^)]+)\)", content):
        if target == "handoff-manifest.json":
            continue
        assert (root / target).is_file(), (name, target)
        links.append({"from": name, "target": target})
checks.append({"check": "26 requirements, 19 scenarios, local artifact links and resolved handoff", "result": "PASS", "links": links})

for name in ("windows-completion.json", "ubuntu/completion.json"):
    completion = read(name)
    assert completion["source_drift"] == []
    assert completion["owned_product_processes"] == []
checks.append({"check": "native completion records source and owned processes", "result": "PASS"})
assert digest(root / "ubuntu-evidence.tar.gz") == "294371e6c8111cdb5f266bed000cb021eb8b7eb9f4fc1878c89e10119b7c4e24"

write("checkpoint.json", {
    "mode": "execute", "assessment": "FAIL", "full_qualification": "INCOMPLETE",
    "evidence_root": str(root), "plan": binding["selected_plan"],
    "candidate_manifest": str(root / "source-manifest.json"),
    "report": str(root / "qa-report.md"), "fix_packet": str(root / "qa-fix.md"),
    "confirmed_open_defects": ["QA-D01", "QA-D02"],
    "gaps": ["QA-G01", "QA-G02", "QA-G03", "QA-G04", "QA-G05"],
    "owned_product_processes_at_native_completion": [],
    "retained_windows_scratch": binding["scratch"],
    "retained_ubuntu_scratch": binding["remote_scratch"],
    "remote_sessions": "ended after evidence transfer",
    "next_owner": "dev", "next_safe_action": "User selects dev remediation of QA-D01 and QA-D02 using byte-bound handoff. No automatic repair or retest.",
    "framework_acceptance": "NOT_EVALUATED"
})
write("publication-check.json", {
    "time_utc": datetime.now(timezone.utc).isoformat(),
    "purpose": "Evidence publication consistency only; not product acceptance",
    "checks": checks,
    "result": "PASS"
})
artifacts = []
for path in sorted(root.rglob("*")):
    if path.is_file() and path.name != "handoff-manifest.json":
        artifacts.append({"role": path.relative_to(root).as_posix(), "required_path": str(path),
                          "actual_path": str(path), "bytes": path.stat().st_size,
                          "sha256": digest(path), "readback": True})
write("handoff-manifest.json", {
    "resolved_evidence_root": str(root), "assessment": "FAIL",
    "selected_plan_manifest": str(plan / "handoff-manifest.json"),
    "selected_plan_manifest_sha256": digest(plan / "handoff-manifest.json"),
    "artifacts": artifacts
})
manifest = read("handoff-manifest.json")
for row in manifest["artifacts"]:
    path = Path(row["actual_path"])
    assert digest(path) == row["sha256"] and path.stat().st_size == row["bytes"]
print(json.dumps({"artifact_count": len(artifacts), "all_manifest_entries_verified": True,
                  "manifest_sha256": digest(root / "handoff-manifest.json"),
                  "report_sha256": digest(root / "qa-report.md"),
                  "fix_sha256": digest(root / "qa-fix.md")}, indent=2))
