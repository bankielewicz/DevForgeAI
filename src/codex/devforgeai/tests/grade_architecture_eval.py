"""Grade native Architecture traces against the imported case definitions.

PyYAML is required. Regex and file checks are deterministic. LLM graders stay
REVIEW_REQUIRED until an independent assessor writes ``semantic-review.json``.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
EXPECTED_QUESTION_CASES = {"existing-arch-not-duplicated"}
NO_ARCH_CHANGE_CASES = {"existing-arch-not-duplicated", "reuse-review-idempotent"}
CODE_SUFFIXES = {".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt", ".php",
                 ".py", ".rb", ".rs", ".sh", ".sql", ".swift", ".ts", ".tsx"}


def read_json(path):
    return json.loads(path.read_text())


def native_question_events(messages):
    """Return only actual native request_user_input events, never matching prose."""
    return [m["params"] for m in messages if m.get("method") == "item/tool/requestUserInput"]


def user_visible_question(params):
    lines = []
    for question in params.get("questions", []):
        lines.extend(v for v in (question.get("header"), question.get("question")) if v)
        for option in question.get("options", []):
            lines.append(f"- {option.get('label', '')}: {option.get('description', '')}")
    return "\n".join(lines)


def skill_loads(items):
    """Find completed reads of SKILL.md; catalog listing alone is not activation."""
    loads = []
    for item in items:
        if item.get("type") != "commandExecution" or item.get("exitCode") != 0:
            continue
        actions = item.get("commandActions") or []
        paths = [str(a.get("path", "")) for a in actions if a.get("type") == "read"]
        command = str(item.get("command", ""))
        output = str(item.get("aggregatedOutput", ""))
        read_skill = any(p.endswith("/skills/architecture/SKILL.md") for p in paths)
        read_skill = read_skill or "skills/architecture/SKILL.md" in command
        if read_skill and re.search(r"(?m)^name:\s*(?:devforgeai:)?architecture\s*$", output):
            loads.append({"id": item.get("id"), "command": command, "paths": paths})
    return loads


def exists_target(workspace, path):
    if path.endswith("/**"):
        root = workspace / path[:-3]
        return root.is_dir() and any(p.is_file() for p in root.rglob("*"))
    return (workspace / path).is_file()


def parse_frontmatter(path):
    if not path.is_file():
        return {}
    parts = path.read_text().split("---", 2)
    if len(parts) != 3:
        return {}
    try:
        value = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def arm_applies(definition, arm):
    return definition.get("arm") in (None, "both", arm)


def grade_source(case, trial, visible, loads, questions, arm):
    grades = []
    definitions = trial.parents[1] / "definitions" / case / "graders"
    for path in sorted(definitions.glob("*.md")):
        _, metadata, body = path.read_text().split("---", 2)
        definition = yaml.safe_load(metadata)
        kind = definition["type"]
        row = {"grader": path.stem, "type": kind}
        applies = arm_applies(definition, arm)
        if kind in {"skill_loaded", "tool_used"}:
            minimum = int(definition.get("min", 1))
            maximum = definition.get("max")
            maximum = int(maximum) if maximum is not None else None
            passed = len(loads) >= minimum and (maximum is None or len(loads) <= maximum)
            row.update(scored=False, applicable=applies, passed=passed if applies else None, evidence=loads)
        elif kind == "request_user_input":
            minimum = int(definition.get("min", 1))
            maximum = definition.get("max")
            maximum = int(maximum) if maximum is not None else None
            passed = len(questions) >= minimum and (maximum is None or len(questions) <= maximum)
            row.update(scored=applies, applicable=applies, passed=passed if applies else None,
                       evidence_count=len(questions))
        elif kind == "file_exists":
            row.update(scored=applies, applicable=applies,
                       passed=(exists_target(trial / "workspace", definition["path"]) == definition["exists"])
                       if applies else None)
        elif kind == "regex":
            target = definition["target"]
            target_path = trial / "workspace" / target["path"] if isinstance(target, dict) else None
            if target_path is None:
                content, present = visible, True
            else:
                present = target_path.is_file()
                content = target_path.read_text() if present else ""
            flags = sum({"i": re.I, "m": re.M, "s": re.S}.get(f, 0) for f in definition.get("flags", ""))
            hit = re.search(body.strip(), content, flags) is not None
            passed = present and hit == (definition["match"] == "contains")
            row.update(scored=applies, applicable=applies, passed=passed if applies else None,
                       target_present=present)
        elif kind == "llm":
            row.update(scored=applies, applicable=applies, passed=None,
                       status="REVIEW_REQUIRED" if applies else "NOT_APPLICABLE", rubric=body.strip())
        else:
            raise ValueError(f"Unsupported grader type {kind!r} in {path}")
        grades.append(row)
    return grades


def grade(trial):
    result = read_json(trial / "result.json")
    case, arm = result["case"], result["arm"]
    protocol = trial / "protocol.jsonl"
    messages = [json.loads(line)["message"] for line in protocol.read_text().splitlines()] if protocol.exists() else []
    items = [m["params"]["item"] for m in messages if m.get("method") == "item/completed"]
    agent_messages = [i for i in items if i.get("type") == "agentMessage"]
    finals = [i["text"] for i in agent_messages if i.get("phase") == "final_answer"]
    if not finals:
        finals = [i["text"] for i in agent_messages if i.get("phase") != "commentary"]
    final_reply = finals[-1] if finals else ""
    questions = native_question_events(messages)
    visible = (final_reply + "\n" + "\n".join(user_visible_question(q) for q in questions)).strip()
    (trial / "final-reply.txt").write_text(final_reply)
    (trial / "reply.txt").write_text(visible + ("\n" if visible else ""))
    (trial / "user-visible-questions.json").write_text(json.dumps(questions, indent=2) + "\n")
    loads = skill_loads(items)
    grades = grade_source(case, trial, visible, loads, questions, arm)
    semantic = trial / "semantic-review.json"
    if semantic.exists():
        assessment = read_json(semantic)
        for row in grades:
            if row["type"] == "llm" and row.get("applicable"):
                reviewed = assessment[row["grader"]]
                row.update(passed=reviewed["passed"], status="REVIEWED", assessment=reviewed)

    before, after = read_json(trial / "before.json"), read_json(trial / "after.json")
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    before_prds = {p: h for p, h in before.items() if p.startswith("docs/specs/prd/")}
    after_prds = {p: h for p, h in after.items() if p.startswith("docs/specs/prd/")}
    git_before, git_after = read_json(trial / "git-before.json"), read_json(trial / "git-after.json")
    expected_activation = arm == "plugin" and case != "ignores-unrelated-request"
    expected_question = case in EXPECTED_QUESTION_CASES
    allowed_roots = ("docs/specs/arch/", "docs/specs/adr/")
    guards = {
        "completed_or_expected_native_question": result["status"] == "completed" or
            (expected_question and result["status"] == "awaiting_input" and bool(questions)),
        "activation_matches_case": bool(loads) == expected_activation,
        "preexisting_prds_preserved": before_prds == after_prds,
        "only_architecture_artifacts_changed": all(p.startswith(allowed_roots) for p in changed),
        "no_downstream_code_written": not any(
            p.startswith(("docs/specs/epic/", "docs/specs/story/", "src/", "app/", "lib/"))
            or Path(p).suffix.lower() in CODE_SUFFIXES for p in changed),
        "index_preserved": git_before["index"] == git_after["index"],
        "head_preserved": git_before["head"] == git_after["head"],
        "refs_preserved": git_before["refs"] == git_after["refs"],
    }
    if arm == "plugin":
        guards["runtime_candidate_preserved"] = read_json(trial / "runtime-candidate-check.json")["unchanged"]
    if case in NO_ARCH_CHANGE_CASES:
        b = {p: h for p, h in before.items() if p.startswith("docs/specs/arch/")}
        a = {p: h for p, h in after.items() if p.startswith("docs/specs/arch/")}
        guards["expected_existing_arch_unchanged"] = b == a
    if arm == "plugin" and expected_question:
        guards["choice_uses_native_question"] = bool(questions)

    arch = trial / "workspace/docs/specs/arch/ARCH-001.md"
    created = "docs/specs/arch/ARCH-001.md" not in before and arch.is_file()
    provenance = {}
    if arm == "plugin" and created:
        generated = parse_frontmatter(arch).get("generated_by", {})
        runtime_model, runtime_session = result.get("model"), result.get("threadId")
        provenance = {"recorded": generated,
                      "runtime": {"tool": "codex", "model": runtime_model, "session": runtime_session}}
        guards.update({
            "runtime_model_known": bool(runtime_model and str(runtime_model).lower() != "unknown"),
            "runtime_session_known": bool(runtime_session and str(runtime_session).lower() != "unknown"),
            "provenance_tool_is_codex": generated.get("tool") == "codex",
            "provenance_model_matches_runtime": bool(runtime_model) and generated.get("model") == runtime_model,
            "provenance_session_matches_runtime": bool(runtime_session) and generated.get("session") == runtime_session,
        })

    scored = [g for g in grades if g.get("scored")]
    score = None if not scored or any(g["passed"] is None for g in scored) else \
        sum(g["passed"] for g in scored) / len(scored)
    activation_grades = [g for g in grades if not g.get("scored") and g.get("applicable")]
    threshold_pass = score is not None and score >= 0.8
    strict_pass = threshold_pass and all(g["passed"] is True for g in scored) and \
        all(g["passed"] is True for g in activation_grades) and all(guards.values())
    output = {
        "case": case, "verification": result["verification"], "arm": arm, "repeat": result["repeat"],
        "status": result["status"], "collaboration_mode": result.get("collaboration_mode"),
        "native_question_count": len(questions), "source_grades": grades, "source_score": score,
        "threshold_pass": threshold_pass,
        "activation": {"expected": expected_activation, "observed": bool(loads), "loads": loads},
        "supplemental_guards": guards, "changed_paths": changed, "provenance": provenance,
        "strict_pass": strict_pass,
        "semantic_note": "Source checks remain distinct from supplemental provenance, PRD-custody, native-question, activation and downstream-write guards.",
    }
    (trial / "grade.json").write_text(json.dumps(output, indent=2) + "\n")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--stage", default="matrix", choices=["smoke", "matrix"])
    args = parser.parse_args()
    results = [grade(p.parent) for p in sorted((args.evidence / args.stage).glob("*/result.json"))]
    (args.evidence / f"{args.stage}-grades.json").write_text(json.dumps(results, indent=2) + "\n")
    for result in results:
        failed = [g["grader"] for g in result["source_grades"] if g.get("scored") and g["passed"] is not True]
        failed += [key for key, value in result["supplemental_guards"].items() if not value]
        print(json.dumps({key: result[key] for key in ("case", "arm", "repeat", "source_score", "strict_pass")}
                         | {"failed_or_pending": failed}))


if __name__ == "__main__":
    main()
