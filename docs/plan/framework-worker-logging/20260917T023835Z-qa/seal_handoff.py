"""Bind final retained QA artifacts; read-only outside this evidence root."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def binding(path):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def write(name, value):
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True)
        stream.write("\n")


def verify(items):
    for item in items:
        assert binding(Path(item["path"])) == item, item["path"]


for name in ["candidate-manifest.json", "preserved-manifest.json", "input-manifest.json", "specification-bindings.json", "qa-helper-manifest-v2.json", "binary-manifest.json"]:
    verify(read(name))
for name in ["qa-report.md", "qa-fix.md", "checkpoint.json", "plan.md", "dev-prompt.txt"]:
    contents = (ROOT / name).read_text(encoding="utf-8-sig")
    assert contents and "<project>" not in contents and "TODO" not in contents, name
assert read("checkpoint.json")["execution_status"] == "COMPLETED"
assert read("checkpoint.json")["verdict"] == "FAIL"
assert len(read("attempt-index.json")) == 24
assert not (ROOT / "STOP.json").exists()

# Do not walk target intermediates or any Windows reparse point, including owned junctions.
excluded = {"evidence-manifest.json", "handoff-manifest.json", "final-readback.json"}
files, reparses = [], []
for current, directories, names in os.walk(ROOT, followlinks=False):
    base = Path(current)
    safe = []
    for name in sorted(directories):
        path = base / name
        if base == ROOT and name.endswith("-target"):
            continue
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        if attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            reparses.append({"path": str(path), "target": os.readlink(path), "traversed": False})
        else:
            safe.append(name)
    directories[:] = safe
    for name in sorted(names):
        path = base / name
        if base == ROOT and name in excluded:
            continue
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        if attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            reparses.append({"path": str(path), "target": os.readlink(path), "traversed": False})
            continue
        files.append(binding(path))

# Retain executable identities without binding disposable Cargo intermediates.
binaries = []
for target_name in ["build-target", "coverage-target", "independent-target", "supplemental-target"]:
    target = ROOT / target_name
    for path in sorted(target.rglob("*.exe")):
        if "build" in path.relative_to(target).parts:
            continue  # third-party build-script executables are not product/test identities
        binaries.append(binding(path))
write("evidence-manifest.json", {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "All regular retained evidence outside Cargo target directories; first-party test/product executable identities bound separately. Reparse points recorded, never traversed.",
    "files": files, "binaries": binaries, "reparse_points": reparses,
    "excluded_self_and_final_bindings": sorted(excluded),
})
entry_names = [
    "qa-report.md", "qa-fix.md", "dev-prompt.txt", "checkpoint.json",
    "plan.md", "plan-binding.json", "independent-plan.md", "candidate-manifest.json",
    "input-manifest.json", "preserved-manifest.json", "specification-bindings.json",
    "case-results.json", "criterion-results.json", "metrics.json", "coverage-analysis.json",
    "findings.json", "integrity.md", "documentation-review.json", "attempt-index.json",
    "final-identity-check.json", "binary-manifest.json", "qa-helper-manifest-v2.json",
    "independent-binary-v2.json", "evidence-manifest.json",
]
manifest = {
    "qa_run": "20260917T023835Z-qa", "project": "C:\\Projects\\DevForgeAI",
    "original_evidence_selection": "C:\\Projects\\DevForgeAI\\docs\\plan\\framework-worker-logging",
    "required_destination": str(ROOT), "actual_destination": str(ROOT),
    "execution_status": "COMPLETED", "verdict": "FAIL", "open_findings": ["QA-LOG-01", "QA-LOG-02"],
    "candidate_root": "C:\\Projects\\DevForgeAI\\devforgeai\\experiments\\codex-worker-probe-logging",
    "framework_acceptance": "NOT_EVALUATED", "native_codex": "NOT_RUN",
    "entries": {name: {"required_path": str(ROOT / name), **binding(ROOT / name)} for name in entry_names},
}
write("handoff-manifest.json", manifest)
actual_manifest = read("handoff-manifest.json")
assert actual_manifest == manifest
for name, item in actual_manifest["entries"].items():
    assert item["required_path"] == item["path"] == str(ROOT / name)
    verify([{key: item[key] for key in ["path", "bytes", "sha256"]}])
evidence = read("evidence-manifest.json")
verify(evidence["files"])
verify(evidence["binaries"])
for name in ["candidate-manifest.json", "preserved-manifest.json", "input-manifest.json"]:
    verify(read(name))
result = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "READBACK_VERIFIED",
    "handoff_manifest": binding(ROOT / "handoff-manifest.json"),
    "verified_handoff_entries": len(entry_names), "verified_evidence_files": len(files),
    "verified_executables": len(binaries), "untraversed_reparse_points": len(reparses),
    "candidate_files_unchanged": 67, "preserved_files_unchanged": 116, "input_files_unchanged": 37,
    "report_sha256": sha(ROOT / "qa-report.md"), "fix_sha256": sha(ROOT / "qa-fix.md"),
    "errors": [], "verdict": "FAIL", "framework_acceptance": "NOT_EVALUATED",
}
write("final-readback.json", result)
assert read("final-readback.json") == result
print(json.dumps(result, indent=2))
