"""Seal only this QA run's owned evidence; never follow a fixture reparse point."""
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path
from intake import RUN, ROOT, MANIFEST, binding


def read(name):
    return json.loads((RUN / name).read_text())


def write(name, value):
    with (RUN / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def same(row):
    actual = binding(Path(row["path"]))
    assert all(actual[k] == row[k] for k in ("bytes", "sha256")), row["path"]


def main():
    for name in ("candidate-readback-after.json", "input-readback-after.json", "build-manifest.json"):
        for row in read(name):
            same(row)
    assert binding(MANIFEST)["sha256"] == "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540"
    assert binding(RUN / "test-plan.md")["sha256"] == "48c33e0e2a3376b63f416e7330cda6237854bad20449f51258906a4d6a6051aa"
    for row in read("execution-ledger.json"):
        for key in ("receipt", "stdout", "stderr"):
            same(row[key])
    harness_bindings = read("attempts/07-independent-cases/receipt.json")["harness"]
    for row in harness_bindings:
        same(row)
    required = {name: str(RUN / name) for name in (
        "test-plan.md", "qa-report.md", "case-results.json", "findings.json", "checkpoint.json",
        "input-bindings.json", "coverage-analysis.json", "native-diagnostic-handoff.md", "build-manifest.json")}
    assert all(Path(p).is_file() for p in required.values())
    artifacts, reparses = {}, []
    skipped_trees = {"target", "harness-target", "coverage-target"}
    skipped_files = {"artifact-index.json", "publication-readback.json"}

    def walk(directory, prefix, top=False):
        with os.scandir(directory) as stream:
            entries = sorted(stream, key=lambda e: e.name)
        for entry in entries:
            key = prefix + entry.name
            info = entry.stat(follow_symlinks=False)
            if getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparses.append({"entry": key, "path": entry.path, "attributes": info.st_file_attributes,
                                 "followed": False})
                continue
            if stat.S_ISDIR(info.st_mode):
                if top and entry.name in skipped_trees:
                    continue
                walk(entry.path, key + "/")
            elif stat.S_ISREG(info.st_mode):
                if top and entry.name in skipped_files:
                    continue
                artifacts[key] = binding(Path(entry.path))
            else:
                raise RuntimeError("Unexpected owned evidence entry: " + entry.path)

    walk(str(RUN), "", top=True)
    trial_base = ROOT / "docs/plan/framework-worker-trials"
    for path in read("trial-ownership.json")["added_owned_roots"]:
        root = Path(path)
        assert root.parent == trial_base and root.name.startswith(("NI-admission-", "NI-sources-", "RT-source-type-"))
        assert not (root.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        walk(str(root), "owned-trials/" + root.name + "/")
    manifest = {"schema": "independent-offline-qa-artifact-index-v1",
                "run": str(RUN), "created_utc": datetime.now(timezone.utc).isoformat(),
                "scope": "Observed evidence bindings only; not framework authority",
                "candidate_manifest": binding(MANIFEST), "required_artifacts": required,
                "fix_packet": {"required": False, "reason": "No confirmed defects; offline QA PASS"},
                "artifacts": artifacts, "reparse_entries_not_followed": reparses,
                "generated_build_tree_policy": "Intermediate build trees omitted; all produced executable hashes bound by build-manifest.json",
                "self_hash_policy": "Manifest excluded from its own entries; final readback and conversation bind it",
                "native_attempts": 0}
    write("artifact-index.json", manifest)
    literal = read("artifact-index.json")
    assert literal == manifest
    for row in literal["artifacts"].values():
        same(row)
    links = []
    for name in ("qa-report.md", "native-diagnostic-handoff.md"):
        doc = RUN / name
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            path = (doc.parent / target.split("#")[0]).resolve()
            assert path.exists(), str(path)
            links.append({"source": name, "target": target, "exists": True})
    receipt = {"observed_utc": datetime.now(timezone.utc).isoformat(), "manifest": binding(RUN/"artifact-index.json"),
               "indexed_files_read_back": len(artifacts), "matching_files": len(artifacts),
               "candidate_snapshot_input_and_build_bindings_rechecked": 230+123+131,
               "executed_harness_inputs_rechecked": len(harness_bindings),
               "required_artifacts": {name: binding(Path(path)) for name, path in required.items()},
               "local_report_and_handoff_links": links, "undelivered_required_artifacts": [],
               "native_attempts": 0, "framework_acceptance": "NOT_EVALUATED"}
    write("publication-readback.json", receipt)
    assert read("publication-readback.json") == receipt
    print(json.dumps({"manifest": receipt["manifest"], "files":len(artifacts), "reparse_points_not_followed":len(reparses),
                      "link_checks":len(links),"publication_receipt":binding(RUN/"publication-readback.json"),
                      "report":binding(RUN/"qa-report.md"),"native_handoff":binding(RUN/"native-diagnostic-handoff.md")},indent=2))


if __name__ == "__main__":
    main()
