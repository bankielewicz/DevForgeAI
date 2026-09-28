"""Bounded native probes for selected SPEC-003 manual/error obligations.

These probes supplement, and do not replace, owner-run VER-12 or deployed-plugin
VER-13. They require an authenticated Codex CLI and never install the plugin.
"""
import argparse
import concurrent.futures
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from native_architecture_eval import (
    ArchitectureServer, EXE, PACKAGE, git_state, inventory, save,
)

THIS_FILE = Path(__file__).resolve()
REPO = PACKAGE.parents[2]
GENERATOR = THIS_FILE.with_name("make_architecture_evals.py")
HARNESS = THIS_FILE.with_name("native_architecture_eval.py")
EXPECTED_EXE = Path("/home/bryan/.local/bin/codex")


@contextlib.contextmanager
def in_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_generator():
    spec = importlib.util.spec_from_file_location("architecture_fixture_source", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load fixture generator: {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    with in_directory(REPO):
        spec.loader.exec_module(module)
    return module


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError(f"Fixture derivation anchor is not unique: {label}")
    return text.replace(old, new)


def case_definitions():
    source = load_generator()
    draft = source.PRD_V1
    draft = replace_once(draft, "status: approved\n", "status: draft\n", "draft status")
    draft = replace_once(draft, 'reviewed_by: ["Priya Nair"]\n', "reviewed_by: []\n", "reviewed_by")
    draft = replace_once(draft, 'approved_by: "Priya Nair"\n', "", "approved_by")
    draft = replace_once(draft, "approved_on: 2026-09-20\n", "", "approved_on")
    with in_directory(REPO):
        source.validate("PRD_DRAFT", draft, "prd.schema.json")

    fence = "\x60\x60\x60"
    policy_anchor = (
        '    rationale: "SOC 2 scope and the organization\'s accessibility commitment cover internal tools too"\n'
        + fence
    )
    invalid_policy = replace_once(
        source.POL_A,
        policy_anchor,
        (
            '    rationale: "SOC 2 scope and the organization\'s accessibility commitment cover internal tools too"\n'
            "  - id: SET-03\n"
            "    status: active\n"
            "    key: interview.max_calls\n"
            "    class: interaction_default\n"
            "    value: 50\n"
            "    overridable_by: [project, local]\n"
            '    rationale: "Deliberately invalid: value exceeds the 1-20 schema range"\n'
            + fence
        ),
        "invalid policy setting",
    )
    arch_two = source.ARCH_EXISTING.replace("ARCH-001", "ARCH-002")
    if arch_two == source.ARCH_EXISTING:
        raise RuntimeError("ARCH-002 derivation did not replace the document identity")
    with in_directory(REPO):
        source.validate("ARCH_TWO", arch_two, "arch.schema.json")

    cases = [
        {
            "id": "VER12c-draft-prd-warning", "ver": "VER-12(c)", "mode": "default",
            "prompt": "Define the architecture for PRD-001 so we know which requirements are ready for epics.\nProceed without questions.\n",
            "files": {"docs/specs/prd/PRD-001.md": draft},
            "expect": [
                "Proposal warning follows the draft read and precedes every question or write.",
                "The final handoff repeats the proposal warning.",
                "The input PRD remains byte-identical.",
            ],
        },
        {
            "id": "VER12e-invalid-policy", "ver": "VER-12(e)", "mode": "default",
            "prompt": "Define the architecture for PRD-001 so we know which requirements are ready for epics.\nProceed without questions.\n",
            "files": {
                "docs/specs/prd/PRD-001.md": source.PRD_V1,
                "docs/specs/policy/POL-001.md": invalid_policy,
            },
            "expect": [
                "The workflow stops before writing output.",
                "The reply names POL-001.md, SET-03, interview.max_calls, and schema.",
                "The reply says nothing was written.",
            ],
        },
        {
            "id": "VER12g-unknown-prd", "ver": "VER-12(g)", "mode": "default",
            "prompt": "Define the architecture for PRD-999 so we know which requirements are ready for epics.\nProceed without questions.\n",
            "files": {"docs/specs/prd/PRD-001.md": source.PRD_V1},
            "expect": [
                "The reply says PRD-999 does not exist.",
                "The reply lists available PRD ID PRD-001.",
                "The workflow writes no output.",
            ],
        },
        {
            "id": "ERR04-multiple-arch", "ver": "ERR-04 supplemental", "mode": "plan",
            "prompt": (
                "Define the architecture for PRD-001. If you need me to choose between existing "
                "architecture documents, ask me which one to use.\n"
            ),
            "files": {
                "docs/specs/prd/PRD-001.md": source.PRD_V1,
                "docs/specs/arch/ARCH-001.md": source.ARCH_EXISTING,
                "docs/specs/arch/ARCH-002.md": arch_two,
            },
            "expect": [
                "Plan mode emits native request_user_input while unanswered.",
                "The native request names ARCH-001 and ARCH-002.",
                "The workspace remains byte-identical while the choice is unanswered.",
            ],
        },
    ]
    sources = {
        "generator": {"path": str(GENERATOR.relative_to(REPO)), "sha256": digest(GENERATOR.read_bytes())},
        "PRD_V1": digest(source.PRD_V1.encode()),
        "POL_A": digest(source.POL_A.encode()),
        "ARCH_EXISTING": digest(source.ARCH_EXISTING.encode()),
        "derived": {
            "PRD_DRAFT": digest(draft.encode()),
            "POL_A_INVALID_SET_03": digest(invalid_policy.encode()),
            "ARCH_002": digest(arch_two.encode()),
        },
    }
    return cases, sources


def write_fixture(root, files):
    for relative, body in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)


WRITE_COMMAND = re.compile(
    r"(?:apply_patch|\bsed\s+-i\b|\btee\b|\bmkdir\b|\bcp\b|\bmv\b|"
    r"\bwrite_text\b|\bwrite_bytes\b|(?:^|[;&|]\s*)cat\s+[^\n]*>|(?<![<>])>(?!>))",
    re.I,
)


def protocol_timeline(path):
    events = []
    if not path.exists():
        return events
    for number, line in enumerate(path.read_text().splitlines(), 1):
        row = json.loads(line)
        message = row.get("message", {})
        method = message.get("method")
        params = message.get("params", {})
        event = {"line": number, "method": method}
        if method == "item/completed":
            item = params.get("item", {})
            event.update(type=item.get("type"), phase=item.get("phase"))
            if item.get("type") == "agentMessage":
                event["text"] = item.get("text", "")
            elif item.get("type") == "commandExecution":
                command = item.get("command", "")
                if isinstance(command, list):
                    command = " ".join(str(part) for part in command)
                event.update(command=command, possible_write=bool(WRITE_COMMAND.search(command)))
        elif method == "item/tool/requestUserInput":
            event.update(type="requestUserInput", request=params)
        if method in {"item/completed", "item/tool/requestUserInput"}:
            events.append(event)
    return events


def proposal_warning(text):
    return bool(re.search(
        r"(?:draft[\s\S]{0,120}(?:proposal|provisional)|(?:proposal|provisional)[\s\S]{0,120}draft)",
        text, re.I,
    ))


def checked(value, evidence):
    return {"status": "PASS" if value else "FAIL", "evidence": evidence}


def assess(case, before, after, events, result):
    messages = [event for event in events if event.get("type") == "agentMessage"]
    finals = [event for event in messages if event.get("phase") == "final"]
    final_text = (finals[-1] if finals else messages[-1] if messages else {}).get("text", "")
    no_writes = before == after
    if case["id"] == "VER12c-draft-prd-warning":
        warnings = [event for event in messages if proposal_warning(event.get("text", ""))]
        boundary = [
            event["line"] for event in events
            if event.get("type") in {"requestUserInput", "fileChange"} or event.get("possible_write")
        ]
        if warnings and boundary:
            ordering = checked(
                warnings[0]["line"] < min(boundary),
                {"first_warning_line": warnings[0]["line"], "first_question_or_write_line": min(boundary)},
            )
        elif warnings and not no_writes:
            ordering = {
                "status": "REVIEW_REQUIRED",
                "evidence": {
                    "first_warning_line": warnings[0]["line"],
                    "reason": "Workspace changed but protocol exposed no classifiable write event.",
                },
            }
        else:
            ordering = checked(bool(warnings), {"warning_lines": [event["line"] for event in warnings]})
        prd = "docs/specs/prd/PRD-001.md"
        checks = {
            "warning_before_question_or_write": ordering,
            "warning_in_final_handoff": checked(proposal_warning(final_text), final_text),
            "input_prd_unchanged": checked(
                before.get(prd) == after.get(prd),
                {"before": before.get(prd), "after": after.get(prd)},
            ),
        }
    elif case["id"] == "VER12e-invalid-policy":
        checks = {
            "no_workspace_writes": checked(no_writes, {"before": before, "after": after}),
            "names_file": checked("POL-001.md" in final_text, final_text),
            "names_setting_and_key": checked(
                "SET-03" in final_text and "interview.max_calls" in final_text, final_text,
            ),
            "names_schema": checked(bool(re.search(r"\bschema\b", final_text, re.I)), final_text),
            "states_nothing_written": checked(
                bool(re.search(r"nothing (?:was |has been )?written", final_text, re.I)), final_text,
            ),
        }
    elif case["id"] == "VER12g-unknown-prd":
        checks = {
            "no_workspace_writes": checked(no_writes, {"before": before, "after": after}),
            "names_missing_prd": checked(
                "PRD-999" in final_text and bool(re.search(r"not (?:exist|found)|unknown", final_text, re.I)),
                final_text,
            ),
            "lists_available_prd": checked(
                "PRD-001" in final_text and bool(re.search(r"available|found|existing", final_text, re.I)),
                final_text,
            ),
        }
    else:
        requests = [event for event in events if event.get("type") == "requestUserInput"]
        request_text = json.dumps([event.get("request") for event in requests], ensure_ascii=False)
        checks = {
            "awaiting_native_input": checked(
                result.get("status") == "awaiting_input" and bool(requests),
                {"turn_status": result.get("status"), "request_count": len(requests)},
            ),
            "request_names_both_arches": checked(
                "ARCH-001" in request_text and "ARCH-002" in request_text, request_text,
            ),
            "no_workspace_writes": checked(no_writes, {"before": before, "after": after}),
        }
    statuses = [value["status"] for value in checks.values()]
    overall = "PASS" if all(value == "PASS" for value in statuses) else (
        "REVIEW_REQUIRED" if "REVIEW_REQUIRED" in statuses and "FAIL" not in statuses else "FAIL"
    )
    return {
        "case": case["id"], "ver": case["ver"], "status": overall,
        "turn_status": result.get("status"), "checks": checks,
        "final_message": final_text, "timeline": events,
    }


def run_case(case, evidence, candidate, candidate_manifest, plan_hash):
    out = evidence / "supplemental" / case["id"]
    out.mkdir(parents=True, exist_ok=False)
    scratch = Path(tempfile.mkdtemp(prefix="dfai-architecture-extra-"))
    project = scratch / "project"
    project.mkdir()
    runtime = scratch / "devforgeai"
    shutil.copytree(candidate, runtime)
    write_fixture(project, case["files"])
    (out / "prompt.md").write_text(case["prompt"])
    before = inventory(project)
    save(out / "before.json", before)
    save(out / "git-before.json", git_state(project))
    save(out / "runtime-candidate-before.json", inventory(runtime))
    shutil.copytree(project, out / "before-workspace", ignore=shutil.ignore_patterns(".git"))
    server = None
    started = time.monotonic()
    try:
        server = ArchitectureServer(out, project)
        server.setup(project, "plugin", runtime)
        if case["mode"] == "plan":
            server.mode = "plan"
        result = server.turn(case["prompt"], timeout=1200)
        result.update(threadId=server.thread, model=server.model)
    except Exception as exc:
        result = {"status": "harness_error", "error": repr(exc)}
    finally:
        if server:
            server.close()
    after = inventory(project)
    runtime_after = inventory(runtime)
    result.update({
        "case": case["id"], "ver": case["ver"], "collaboration_mode": case["mode"],
        "elapsed_seconds": round(time.monotonic() - started, 3), "plan_sha256": plan_hash,
        "scratch_parent": str(scratch), "scratch_workspace": str(project),
    })
    save(out / "result.json", result)
    save(out / "after.json", after)
    save(out / "git-after.json", git_state(project))
    save(out / "runtime-candidate-after.json", runtime_after)
    shutil.copytree(project, out / "workspace", ignore=shutil.ignore_patterns(".git"))
    assessment = assess(case, before, after, protocol_timeline(out / "protocol.jsonl"), result)
    assessment["checks"]["runtime_candidate_unchanged"] = checked(
        runtime_after == candidate_manifest, {"expected": candidate_manifest, "actual": runtime_after},
    )
    if runtime_after != candidate_manifest:
        assessment["status"] = "FAIL"
    save(out / "assessment.json", assessment)
    print(json.dumps({
        "case": case["id"], "turn": result.get("status"), "assessment": assessment["status"],
    }), flush=True)
    return assessment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True, help="Fresh output directory")
    parser.add_argument("--candidate", type=Path, required=True, help="Existing frozen runtime candidate")
    parser.add_argument("--jobs", type=int, default=3)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    candidate = args.candidate.resolve()
    if evidence.exists():
        raise RuntimeError("Evidence path exists; retain it and use a fresh path")
    harness_exe = Path(EXE)
    if not EXPECTED_EXE.is_file() or not os.access(EXPECTED_EXE, os.X_OK):
        raise RuntimeError(f"Expected native Codex executable is unavailable or not executable: {EXPECTED_EXE}")
    if not harness_exe.is_file() or not os.access(harness_exe, os.X_OK):
        raise RuntimeError(f"Harness Codex executable is unavailable or not executable: {harness_exe}")
    expected_resolved = EXPECTED_EXE.resolve(strict=True)
    harness_resolved = harness_exe.resolve(strict=True)
    if harness_resolved != expected_resolved:
        raise RuntimeError(
            f"Native Codex executable mismatch: expected {expected_resolved}; harness resolved {harness_resolved}"
        )
    cases, fixture_sources = case_definitions()
    candidate_before = inventory(candidate)
    if not candidate_before or not all(
        path.startswith((".codex-plugin/", "skills/architecture/")) for path in candidate_before
    ):
        raise RuntimeError("Candidate must contain only .codex-plugin and skills/architecture runtime files")
    if not (candidate / "skills/architecture/SKILL.md").is_file():
        raise RuntimeError("Candidate lacks skills/architecture/SKILL.md")

    evidence.mkdir(parents=True, exist_ok=False)
    fixture_root = evidence / "fixture-source"
    for case in cases:
        write_fixture(fixture_root / case["id"], case["files"])
    plan = {
        "status": "FROZEN_BEFORE_RUNS",
        "purpose": "Native probes for SPEC-003 VER-12(c/e/g) and inherited ERR-04 coverage.",
        "manual_scope": "Supplemental only; full manual VER-12 and deployed-plugin VER-13 remain NOT_RUN.",
        "codex_executable": str(EXE),
        "codex_resolved_executable": str(harness_resolved),
        "codex_version": subprocess.check_output([EXE, "--version"], text=True).strip(),
        "candidate_path": str(candidate),
        "candidate_manifest": candidate_before,
        "fixture_sources": fixture_sources,
        "harness": {"path": str(HARNESS.relative_to(PACKAGE)), "sha256": digest(HARNESS.read_bytes())},
        "supplemental_harness_sha256": digest(THIS_FILE.read_bytes()),
        "isolation": (
            "Unique temp parent per probe; runtime-only frozen candidate; evidence and checks outside "
            "the model workspace; raw protocol retained; .git excluded from workspace copies."
        ),
        "cases": [{
            "id": case["id"], "ver": case["ver"], "mode": case["mode"],
            "prompt": case["prompt"], "expected_checks": case["expect"],
            "fixture_manifest": inventory(fixture_root / case["id"]), "status": "NOT_RUN",
        } for case in cases],
    }
    plan_path = evidence / "supplemental-plan.json"
    save(plan_path, plan)
    plan_hash = digest(plan_path.read_bytes())
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [
            pool.submit(run_case, case, evidence, candidate, candidate_before, plan_hash)
            for case in cases
        ]
        assessments = [future.result() for future in concurrent.futures.as_completed(futures)]
    candidate_after = inventory(candidate)
    save(evidence / "candidate-after.json", candidate_after)
    summary = {
        "plan_sha256": plan_hash,
        "candidate_unchanged": candidate_before == candidate_after,
        "counts": {
            status: sum(item["status"] == status for item in assessments)
            for status in ("PASS", "FAIL", "REVIEW_REQUIRED")
        },
        "cases": sorted(assessments, key=lambda item: item["case"]),
        "manual_VER_12": "NOT_RUN in full; three bounded VER-12 probes attempted.",
        "manual_VER_13": "NOT_RUN; no install or deployed-plugin check performed.",
        "inherited_ERR_04": "One bounded Plan-mode supplemental probe attempted.",
    }
    save(evidence / "supplemental-summary.json", summary)
    if candidate_before != candidate_after:
        raise RuntimeError("Source candidate changed during evaluation")


if __name__ == "__main__":
    main()
