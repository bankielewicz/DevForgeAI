"""Run native Architecture evals through ephemeral Codex app-server threads.

Requires an authenticated Codex CLI. This freezes a runtime-only candidate and
the complete case denominator before any turn; it never installs the plugin.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from native_documents_updater_eval import EXE, Server, git_state, inventory, save

PACKAGE = Path(__file__).resolve().parents[1]
CASE_VER = {
    "creates-arch": "VER-01", "org-a-policy": "VER-02", "org-b-policy": "VER-03",
    "unrelated-adr": "VER-04", "superseded-adr": "VER-05",
    "no-acceptance-without-user": "VER-06", "existing-arch-not-duplicated": "VER-07",
    "insufficient-evidence": "VER-08", "prd-change-handed-back": "VER-09",
    "hands-off-to-epic": "VER-10", "ignores-unrelated-request": "VER-11",
    "records-provenance": "VER-14", "reuse-records-review": "VER-15",
    "reuse-review-idempotent": "VER-16",
}
SMOKE_CASES = ("creates-arch", "existing-arch-not-duplicated", "ignores-unrelated-request")
PLAN_CASES = {"existing-arch-not-duplicated"}
PRIORITY_CASES = ("reuse-records-review", "reuse-review-idempotent")


class ArchitectureServer(Server):
    """Select only the candidate Architecture skill and disable all others."""
    def setup(self, cwd, arm, candidate=None):
        roots = [str(candidate / "skills")] if arm == "plugin" else []
        self.rpc("skills/extraRoots/set", {"extraRoots": roots})
        catalog = self.rpc("skills/list", {"cwds": [str(cwd)], "forceReload": True})
        save(self.e / "skills-list.json", catalog)
        entries = [s for group in catalog.get("data", []) for s in group.get("skills", [])]
        selected = [s for s in entries if candidate and str(candidate / "skills") in str(s.get("path", ""))]
        if arm == "plugin" and not any(s.get("name", "").split(":")[-1] == "architecture" for s in selected):
            raise RuntimeError("Candidate architecture absent from native skills/list")
        if arm == "baseline" and selected:
            raise RuntimeError("Baseline unexpectedly selected a candidate skill")
        other = [{"path": s["path"], "enabled": False} for s in entries if s not in selected]
        started = self.rpc("thread/start", {
            "cwd": str(cwd), "ephemeral": True, "sandbox": "workspace-write",
            "approvalPolicy": "never", "config": {"skills.config": other, "features.memories": False},
        })
        save(self.e / "thread-start.json", started)
        self.thread = started["thread"]["id"]
        self.model = started.get("model")
        self.started = started


def prompt_body(case_dir):
    parts = (case_dir / "prompt.md").read_text().split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Prompt lacks YAML frontmatter: {case_dir / 'prompt.md'}")
    return parts[2].strip()


def freeze_candidate(evidence):
    candidate = evidence / "candidate"
    if not candidate.exists():
        shutil.copytree(PACKAGE / ".codex-plugin", candidate / ".codex-plugin")
        shutil.copytree(PACKAGE / "skills/architecture", candidate / "skills/architecture")
    expected = inventory(candidate)
    if not expected or not all(p.startswith((".codex-plugin/", "skills/architecture/")) for p in expected):
        raise RuntimeError("Candidate must contain only the manifest and Architecture runtime skill")
    current = {p: h for p, h in inventory(PACKAGE).items()
               if p.startswith((".codex-plugin/", "skills/architecture/"))}
    if current != expected:
        raise RuntimeError("Candidate bytes differ from source; retain it and use a new evidence directory")
    rows = [{"path": p, "sha256": h} for p, h in expected.items()]
    digest = hashlib.sha256("".join(f"{r['path']}\0{r['sha256']}\n" for r in rows).encode()).hexdigest()
    return candidate, expected, digest


def trial(case, arm, repeat, evidence, definitions, candidate, candidate_manifest, plan_hash, stage,
          stop_file=None):
    identity = f"{case}--{arm}--{repeat}"
    out = evidence / stage / identity
    out.mkdir(parents=True, exist_ok=False)
    if stop_file and stop_file.exists():
        result = {
            "status": "cancelled", "reason": f"stop file exists: {stop_file}",
            "case": case, "verification": CASE_VER[case], "arm": arm, "repeat": repeat,
            "plan_sha256": plan_hash, "scratch_parent": None, "scratch_workspace": None,
        }
        save(out / "result.json", result)
        print(json.dumps({"trial": identity, "status": "cancelled", "elapsed_seconds": 0}), flush=True)
        return result
    parent = Path(tempfile.mkdtemp(prefix="dfai-architecture-eval-"))
    cwd = parent / "project"
    cwd.mkdir()
    local = parent / "devforgeai"
    if arm == "plugin":
        shutil.copytree(candidate, local)
        save(out / "runtime-candidate-before.json", inventory(local))
    case_dir = definitions / case
    prompt = prompt_body(case_dir)
    (out / "prompt.md").write_text(prompt + "\n")
    scaffold = subprocess.run(["bash", str(case_dir / "scaffold.sh")], cwd=cwd,
                              capture_output=True, text=True)
    save(out / "scaffold.json", {"exit": scaffold.returncode, "stdout": scaffold.stdout,
                                  "stderr": scaffold.stderr})
    save(out / "before.json", inventory(cwd))
    save(out / "git-before.json", git_state(cwd))
    shutil.copytree(cwd, out / "before-workspace", ignore=shutil.ignore_patterns(".git"))
    server = None
    started = time.monotonic()
    mode = "plan" if case in PLAN_CASES else "default"
    try:
        scaffold.check_returncode()
        server = ArchitectureServer(out, cwd)
        server.setup(cwd, arm, local if arm == "plugin" else None)
        if mode == "plan":
            server.mode = "plan"
        result = server.turn(prompt, timeout=1200)  # leave native questions unanswered
        result.update(threadId=server.thread, model=server.model)
    except Exception as exc:
        result = {"status": "harness_error", "error": repr(exc)}
    finally:
        if server:
            server.close()
    result.update(case=case, verification=CASE_VER[case], arm=arm, repeat=repeat,
                  collaboration_mode=mode, elapsed_seconds=round(time.monotonic() - started, 3),
                  plan_sha256=plan_hash, scratch_parent=str(parent), scratch_workspace=str(cwd))
    save(out / "result.json", result)
    save(out / "after.json", inventory(cwd))
    save(out / "git-after.json", git_state(cwd))
    if arm == "plugin":
        after_candidate = inventory(local)
        save(out / "runtime-candidate-after.json", after_candidate)
        save(out / "runtime-candidate-check.json", {
            "expected": candidate_manifest, "actual": after_candidate,
            "unchanged": after_candidate == candidate_manifest,
        })
    shutil.copytree(cwd, out / "workspace", ignore=shutil.ignore_patterns(".git"))
    print(json.dumps({"trial": identity, "status": result["status"],
                      "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--stage", choices=["smoke", "matrix"], required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--stop-file", type=Path,
                        help="Do not start queued trials after this file appears; cancelled results are retained")
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    stop_file = args.stop_file.resolve() if args.stop_file else None
    suite = PACKAGE / "evals/architecture"
    discovered = sorted(p.name for p in suite.iterdir() if p.is_dir())
    if set(discovered) != set(CASE_VER):
        raise RuntimeError(f"Architecture denominator mismatch: expected={sorted(CASE_VER)} discovered={discovered}")
    cases = list(SMOKE_CASES) if args.stage == "smoke" else [
        *PRIORITY_CASES, *(case for case in sorted(CASE_VER) if case not in PRIORITY_CASES)]
    repeats = range(1, 2) if args.stage == "smoke" else range(1, 4)
    arms = ("plugin",) if args.stage == "smoke" else ("plugin", "baseline")
    tasks = [(c, a, n) for n in repeats for c in cases for a in arms]
    definitions = evidence / "definitions"
    if not definitions.exists():
        shutil.copytree(suite, definitions)
    frozen_suite = inventory(definitions)
    if inventory(suite) != frozen_suite:
        raise RuntimeError("Frozen definitions differ from source; retain them and use a new evidence directory")
    candidate, manifest, candidate_digest = freeze_candidate(evidence)
    plan = {
        "candidate_sha256": candidate_digest,
        "candidate_files": [{"path": p, "sha256": h} for p, h in manifest.items()],
        "codex_executable": EXE,
        "codex_version": subprocess.check_output([EXE, "--version"], text=True).strip(),
        "mandatory": [f"VER-{n:02d}" for n in range(1, 17)],
        "automated_case_map": CASE_VER,
        "manual_owner_cases": {"VER-12": "NOT_RUN", "VER-13": "NOT_RUN"},
        "threshold": 0.8,
        "score_contract": "Source regex/file/semantic graders only; activation and supplemental guards are separate. Semantic graders remain REVIEW_REQUIRED until independently assessed. Every plugin repeat must reach 0.8; no failed grader or mandatory obligation is waived by the threshold.",
        "isolation": "Unique temp parent per trial; runtime candidate contains only manifest plus Architecture. Ephemeral app-server with memories, noncandidate skills, configured plugins and configured MCP servers disabled. Evidence and graders are outside the model workspace. This is not an OS-hermetic boundary.",
        "questions": "VER-07 uses Plan mode in both arms. Native request_user_input requests are recorded and interrupted unanswered; only an explicit supplemental scenario may answer.",
        "stop_file": str(stop_file) if stop_file else None,
        "source_suite": frozen_suite,
        "definitions_sha256": hashlib.sha256("".join(
            f"{p}\0{h}\n" for p, h in frozen_suite.items()).encode()).hexdigest(),
        "server_harness_sha256": hashlib.sha256(
            (PACKAGE / "tests/native_documents_updater_eval.py").read_bytes()).hexdigest(),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "grader_sha256": hashlib.sha256((PACKAGE / "tests/grade_architecture_eval.py").read_bytes()).hexdigest(),
        "summarizer_sha256": hashlib.sha256((PACKAGE / "tests/summarize_architecture_eval.py").read_bytes()).hexdigest(),
        "trials": [{"case": c, "verification": CASE_VER[c], "arm": a, "repeat": n, "status": "NOT_RUN"}
                   for c, a, n in tasks],
    }
    plan_path = evidence / f"{args.stage}-plan.json"
    if plan_path.exists():
        raise RuntimeError("Plan already exists; retain it and use a fresh stage/evidence directory")
    save(plan_path, plan)
    plan_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(trial, c, a, n, evidence, definitions, candidate, manifest, plan_hash,
                               args.stage, stop_file)
                   for c, a, n in tasks]
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
