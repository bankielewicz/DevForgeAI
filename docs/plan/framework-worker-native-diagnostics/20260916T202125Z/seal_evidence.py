"""Create and read back an evidence index. Not an acceptance authority."""
import json
import re
from pathlib import Path

from intake import ROOT, FIXTURE, binding, check_binding, collect_files, sha256, utc_now, write


def main():
    index_path = ROOT / "artifact-index.json"
    final_path = ROOT / "final-readback.json"
    assert not index_path.exists() and not final_path.exists()
    archived = ROOT / "diagnostic-preparation-001.py"
    initial_receipt = json.loads((ROOT / "sources-001/started.json").read_bytes())
    assert sha256(archived) == initial_receipt["recorder"]["sha256"]
    actual_receipt = json.loads((ROOT / "native-001/receipt.json").read_bytes())
    assert actual_receipt["recorder"] == binding(ROOT / "diagnostic.py")
    artifact_rows = collect_files(ROOT)
    trial_rows = collect_files(FIXTURE.parent)
    artifacts = {Path(row["path"]).relative_to(ROOT).as_posix(): row for row in artifact_rows}
    artifacts.update({"trial/" + Path(row["path"]).relative_to(FIXTURE.parent).as_posix(): row for row in trial_rows})
    write(index_path, {
        "schema": "native-diagnostic-artifact-index-v1", "created_utc": utc_now(), "run": str(ROOT),
        "scope": "Evidence bindings only; no framework authority",
        "artifacts": artifacts, "native_attempts": 1, "native_retries": 0,
        "model_trials": 0, "framework_acceptance": "NOT_EVALUATED",
        "self_hash_policy": "Index excluded from itself; final-readback.json and final conversation bind its SHA256",
        "post_index_artifacts": [str(final_path)],
    })
    checks = [check_binding(row) for row in artifacts.values()]
    assert all(row["matches"] for row in checks)
    links = []
    for doc in ROOT.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            local = (doc.parent / target.split("#", 1)[0]).resolve()
            links.append({"source": str(doc), "target": target, "resolved": str(local), "exists": local.exists()})
    assert all(row["exists"] for row in links)
    write(final_path, {"utc": utc_now(), "index": binding(index_path), "artifacts_checked": len(checks),
        "all_indexed_hashes_match": True, "documentation_links": links,
        "initial_helper_archive_matches_executed_digest": True,
        "native_helper_matches_executed_digest": True,
        "no_launch_performed_by_this_check": True, "framework_acceptance": "NOT_EVALUATED"})
    print(json.dumps({"index": binding(index_path), "indexed_artifacts": len(checks),
        "valid_local_links": len(links), "all_indexed_hashes_match": True,
        "final_readback": binding(final_path)}))


if __name__ == "__main__":
    main()
