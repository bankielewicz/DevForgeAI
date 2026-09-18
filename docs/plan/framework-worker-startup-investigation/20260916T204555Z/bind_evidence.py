"""Read back frozen inputs and seal investigation artifacts; no runtime authority."""
import hashlib
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\DevForgeAI")
RUN = Path(__file__).resolve().parent
DEV = ROOT / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev"
PKG = ROOT / "devforgeai/experiments/codex-worker-probe"
NATIVE = ROOT / "docs/plan/framework-worker-native-diagnostics/20260916T202125Z"
QA = ROOT / "docs/plan/framework-worker-diagnostics-qa/20260916T191731Z"


def binding(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def check(row):
    actual = binding(Path(row["path"]))
    return {**actual, "matches": all(actual[k] == row[k] for k in ("bytes", "sha256"))}


def preserve():
    native_index = binding(NATIVE / "artifact-index.json")
    assert native_index["sha256"] == "1a22ca36d2fe92f86b7ebded1c6345db0d969ee39e600d5d79502fed1d708750"
    qa_index = binding(QA / "artifact-index.json")
    assert qa_index["sha256"] == "552912696c5260091a8cb2305b13d1f1987e53630b610dd66afec55f84d132d9"
    candidate_manifest = binding(DEV / "candidate-v2-manifest.json")
    assert candidate_manifest["sha256"] == "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540"
    rows = []
    for item in read(DEV / "candidate-v2-manifest.json"):
        for base in (PKG, DEV / "candidate-v2-snapshot"):
            rows.append(check({**item, "path": str(base / item["path"])}))
    for manifest in (NATIVE / "artifact-index.json", QA / "artifact-index.json"):
        rows.extend(check(row) for row in read(manifest)["artifacts"].values())
    assert len(rows) == 6004 and all(r["matches"] for r in rows)
    result = {"observed_utc": datetime.now(timezone.utc).isoformat(), "candidate_manifest": candidate_manifest,
              "native_index":native_index,"qa_index":qa_index,"checks":rows,"matching":len(rows),
              "native_launches_this_investigation":0,"framework_acceptance":"NOT_EVALUATED"}
    write(RUN / "preservation-readback.json", result)
    print(json.dumps({"matching_input_files":len(rows),"preservation_record":binding(RUN/"preservation-readback.json")},indent=2))


def seal():
    required = ["investigation-report.md", "startup-lifecycle.md", "native-evidence.md", "launch-compatibility.md",
                "logging-design.md", "offline-reproduction.md", "preservation-readback.json",
                "windows-event-observation.json", "log-directory-metadata.json", "source-review-notes.md"]
    assert all((RUN / name).is_file() for name in required)
    offline_index = RUN / "offline-repro/artifact-index.json"
    assert binding(offline_index)["sha256"] == "4bcf861a64bd44ef51981b568f637509e31434355dd8ac9d5e70b3ed2b6eb53a"
    offline_checks = [check(row) for row in read(offline_index)["artifacts"].values()]
    assert len(offline_checks) == 60 and all(row["matches"] for row in offline_checks)
    artifacts, reparses = {}, []
    def walk(path, prefix=""):
        with os.scandir(path) as stream:
            entries = sorted(stream,key=lambda e:e.name)
        for entry in entries:
            key = prefix+entry.name
            info = entry.stat(follow_symlinks=False)
            if getattr(info,"st_file_attributes",0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparses.append({"path":entry.path,"followed":False})
            elif stat.S_ISDIR(info.st_mode):
                if entry.name in {"target", "__pycache__"}:
                    continue
                walk(entry.path,key+"/")
            elif stat.S_ISREG(info.st_mode) and key not in {"artifact-index.json","final-readback.json"}:
                artifacts[key] = binding(Path(entry.path))
    walk(str(RUN))
    index = {"schema":"worker-startup-investigation-index-v1","created_utc":datetime.now(timezone.utc).isoformat(),
             "run":str(RUN),"required_artifacts":required,"artifacts":artifacts,"reparse_entries":reparses,
             "excluded_generated_trees":["target","__pycache__"],"self_hash":"Bound by final-readback.json and final conversation",
             "scope":"Investigation and synthetic reproduction, not repair or full QA", "native_launches":0,
             "framework_acceptance":"NOT_EVALUATED"}
    write(RUN/"artifact-index.json", index)
    assert read(RUN/"artifact-index.json") == index
    checks=[check(row) for row in read(RUN/"artifact-index.json")["artifacts"].values()]
    assert all(row["matches"] for row in checks)
    for row in read(RUN/"preservation-readback.json")["checks"]:
        assert check(row)["matches"]
    receipt={"index":binding(RUN/"artifact-index.json"),"indexed_files_checked":len(checks),"matching":len(checks),
             "required_outputs":{name:binding(RUN/name) for name in required},"retained_inputs_rechecked":6004,
             "offline_index":binding(offline_index),"offline_files_rechecked":len(offline_checks),
             "native_launches":0,"framework_acceptance":"NOT_EVALUATED"}
    write(RUN/"final-readback.json",receipt)
    assert read(RUN/"final-readback.json")==receipt
    print(json.dumps({"index":receipt["index"],"indexed_files_checked":len(checks),"readback":binding(RUN/"final-readback.json")},indent=2))


if __name__ == "__main__":
    {"preserve":preserve,"seal":seal}[sys.argv[1]]()
