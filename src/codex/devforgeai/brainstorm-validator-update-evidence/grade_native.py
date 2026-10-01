"""Apply the frozen historical graders once and retain every individual result."""
import hashlib
import importlib
import json
from pathlib import Path
import sys

E = Path(__file__).resolve().parent
PACKAGE = E.parent
HISTORICAL = PACKAGE / "import-evidence/native-evaluation-20260928"
sys.path.insert(0, str(HISTORICAL))
grader = importlib.import_module("grade_eval")
grader.C = PACKAGE
grader.E = E / "native"


def main():
    summary = []
    binding = json.loads((E / "native/binding.json").read_text())
    assert hashlib.sha256((HISTORICAL / "grade_eval.py").read_bytes()).hexdigest() == binding["grader_sha256"]
    for case in ("writes-valid-brn", "records-provenance"):
        trial = E / "native" / (case + "--plugin--1")
        if (trial / "grade.json").exists():
            raise SystemExit("Already graded: " + case)
        result = json.loads((trial / "result.json").read_text())
        grade = grader.grade(trial)
        raw, items, final, questions = grader.trace(trial)
        commands = [i for i in items if i.get("type") == "commandExecution"]
        runs = [i for i in commands if "validate_brn.py" in i.get("command", "")
                and "python" in i.get("command", "")]
        executions = [{k: i.get(k) for k in ("id", "command", "cwd", "exitCode", "aggregatedOutput")}
                      for i in runs]
        retries = sum(i.get("exitCode") != 0 for i in runs)
        # These completed traces each contain exactly one invocation, so zero retries
        # is directly observable without inferring whether a later validation is a repair.
        record = {
            "case": case, "arm": "plugin", "repeat": 1,
            "native_status": result["status"], "assessment": grade,
            "score": 1.0 if grade["status"] == "PASS" else 0.0 if grade["status"] == "FAIL" else None,
            "scoring": "Frozen historical binary all-applicable-checks rule",
            "validator_invocations": len(runs), "failed_validator_invocations": retries,
            "observed_repair_retries": 0 if len(runs) == 1 and retries == 0 else None,
            "validator_executions": executions,
            "model": result.get("model"), "threadId": result.get("threadId"),
            "harness_failure": result["status"] == "harness_error",
            "platform_limit": "Model identifier not exposed to the actor in its checked context/environment; emitted unknown, reproducing existing D-04.",
            "grader_defect": None,
            "missing_evidence": grade.get("pending", []),
            "completion_or_validation_failure": result["status"] != "completed" or any(i.get("exitCode") != 0 for i in runs),
        }
        (trial / "trial-assessment.json").write_text(json.dumps(record, indent=2) + "\n")
        summary.append(record)
    (E / "native/summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps([{k: r[k] for k in ("case", "native_status", "assessment", "score",
                                        "validator_invocations", "observed_repair_retries")} for r in summary], indent=2))


if __name__ == "__main__":
    main()
