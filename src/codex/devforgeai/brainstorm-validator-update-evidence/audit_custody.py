"""Read-only comparison of the final files against the captured intake inventories."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

E = Path(__file__).resolve().parent
ROOT = E.parents[3]
PACKAGE = E.parent
MUTABLE = {
    "src/codex/devforgeai/skills/brainstorm/scripts/validate_brn.py",
    "src/codex/devforgeai/IMPORT-REPORT.md",
}
NEW_TEST = "src/codex/devforgeai/tests/test_validate_brn_regressions.py"
EVIDENCE_PREFIX = "src/codex/devforgeai/brainstorm-validator-update-evidence/"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True,
                                   env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))


def main():
    target = E / sys.argv[1]
    if target.exists():
        raise SystemExit("Audit already exists: " + str(target))
    initial = json.loads((E / "worktree-before.json").read_text())
    primary = json.loads((E / "primary-before.json").read_text())
    primary_root = Path(primary["root"])
    protected = {p: h for p, h in initial["files"].items() if p not in MUTABLE}
    protected_after = {p: digest(ROOT / p) for p in protected}
    primary_after = {p: digest(primary_root / p) for p in primary["files"]}
    external = json.loads((E / "external-inputs-before.json").read_text())
    external_after = {p: digest(Path(p)) for p in external}
    current_primary_paths = set(git(primary_root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")) - {""}
    additions = sorted(current_primary_paths - set(primary["files"]))
    changed = set(git(ROOT, "diff", "--name-only", initial["commit"]).splitlines())
    changed.update(git(ROOT, "ls-files", "--others", "--exclude-standard").splitlines())
    outside = sorted(p for p in changed if p not in MUTABLE | {NEW_TEST} and not p.startswith(EVIDENCE_PREFIX))
    before_report = git(ROOT, "show", initial["commit"] + ":src/codex/devforgeai/IMPORT-REPORT.md")
    after_report = (PACKAGE / "IMPORT-REPORT.md").read_text()
    report_deletions = [line for line in difflib.ndiff(before_report.splitlines(keepends=True), after_report.splitlines(keepends=True)) if line.startswith("- ")]
    binding = json.loads((E / "native/binding.json").read_text())
    candidate_after = {p: digest(PACKAGE / p) for p in binding["files"]}
    definitions_after = {p: digest(PACKAGE / p) for p in binding["case_definitions"]}
    native = {}
    for case in ("writes-valid-brn", "records-provenance"):
        trial = E / "native" / (case + "--plugin--1")
        if (trial / "candidate-after.json").is_file():
            before = json.loads((trial / "candidate-before.json").read_text())
            after = json.loads((trial / "candidate-after.json").read_text())
            native[case] = before == after == binding["files"]
        else:
            native[case] = None
    checks = {
        "worktree_read_only_files_unchanged": protected == protected_after,
        "primary_file_bytes_unchanged": primary["files"] == primary_after,
        "primary_head_unchanged": git(primary_root, "rev-parse", "HEAD").strip() == primary["head"],
        "primary_origin_main_unchanged": git(primary_root, "rev-parse", "origin/main").strip() == primary["origin_main"],
        "primary_status_unchanged": git(primary_root, "status", "--porcelain=v1", "--untracked-files=all") == primary["status"],
        "no_added_primary_paths": not additions,
        "external_inputs_unchanged": external == external_after,
        "write_fence": not outside,
        "import_report_additions_only": not report_deletions,
        "frozen_runtime_source_unchanged": candidate_after == binding["files"],
        "frozen_definitions_unchanged": definitions_after == binding["case_definitions"],
        "frozen_executable_unchanged": digest(Path(binding["runtime"])) == binding["runtime_sha256"],
        "user_config_unchanged": digest(Path("/home/bryan/.codex/config.toml")) == binding["config_sha256"],
        "trial_candidate_copies_unchanged": all(value is True for value in native.values()),
    }
    result = {
        "commit": git(ROOT, "rev-parse", "HEAD").strip(),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "worktree_read_only_before": protected,
        "worktree_read_only_after": protected_after,
        "primary_before": primary["files"],
        "primary_after": primary_after,
        "external_before": external,
        "external_after": external_after,
        "added_primary_paths": additions,
        "outside_scope_paths": outside,
        "report_deletions": report_deletions,
        "native_candidate_copies": native,
        "changed_paths": sorted(changed),
    }
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": checks,
                      "readonly_count": len(protected), "primary_count": len(primary_after),
                      "external_count": len(external), "outside_scope_paths": outside}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
