"""Author literal evaluation corpus and synthetic native intake; no model calls."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
package = root / "src/agents/skills/advisor"
base = """VERDICT: PROCEED

ASK RESTATED:
Decide whether the candidate implements an exclusive upper bound.

DO THIS:
1. Keep the exclusive comparison.

DO NOT:
- Change the selected contract.

CLAIM AUDIT:
- comparison -> CONFIRMED (candidate.py:2 -> "return value < maximum")

RISKS:
none

COULD NOT VERIFY:
- Runtime tests were not executed.

FLIP CONDITIONS:
- A specification requiring an inclusive bound changes this verdict.
"""
valid = {"response_status": "VALID", "verdict": "PROCEED", "all_unverified": False}
invalid = {"response_status": "INVALID", "verdict": None, "all_unverified": None}
cases = []
def case(name, text, expected):
    cases.append({"id": name, "kind": "response", "input": text, "expected": expected})
case("valid-proceed", base, valid)
for verdict in ("STOP_REDIRECT", "PROCEED_WITH_CHANGES"):
    case(verdict.lower(), base.replace("VERDICT: PROCEED", "VERDICT: " + verdict), dict(valid, verdict=verdict))
case("needs-context", base.replace("VERDICT: PROCEED", "VERDICT: INSUFFICIENT_CONTEXT") + "\nMISSING:\n1. Provide the selected specification.\n", dict(valid, verdict="INSUFFICIENT_CONTEXT"))
case("all-unverified", base.replace("CONFIRMED", "UNVERIFIED"), dict(valid, all_unverified=True))
case("empty", "", invalid)
case("preamble", "Here is my review.\n" + base, invalid)
case("bare-verdict", base.replace("VERDICT: PROCEED", "VERDICT:"), invalid)
case("unknown-verdict", base.replace("PROCEED", "APPROVED"), invalid)
case("duplicate-verdict", base + "\nVERDICT: STOP_REDIRECT\n", invalid)
case("missing-label", base.replace("DO NOT:\n", ""), invalid)
case("duplicate-label", base + "\nRISKS:\nnone\n", invalid)
case("empty-section", base.replace("RISKS:\nnone", "RISKS:"), invalid)
case("unexpected-missing", base + "\nMISSING:\nnone\n", invalid)
case("no-missing-items", base.replace("VERDICT: PROCEED", "VERDICT: INSUFFICIENT_CONTEXT") + "\nMISSING:\nnone\n", invalid)
case("missing-last-section", base[:base.index("FLIP CONDITIONS:")], invalid)
for name, exit_code, envelope, timeout, spawn in (
    ("process-success", 0, {"type": "result", "subtype": "success", "is_error": False, "result": base}, False, None),
    ("process-error", 1, {"type": "result", "subtype": "success", "is_error": False, "result": base}, False, None),
    ("budget-truncation", 0, {"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "result": base}, False, None),
    ("timeout", None, {}, True, None),
    ("spawn-denial", None, {}, False, "Access denied"),
    ("bad-envelope", 0, [], False, None),
):
    success = name == "process-success"
    failed = exit_code != 0 or timeout or spawn is not None
    expected = dict(valid if success else invalid, execution_status="TIMEOUT" if timeout else "FAILED" if failed else "SUCCEEDED")
    if failed:
        expected["response_status"] = "NOT_EVALUATED"
    cases.append({"id": name, "kind": "process", "input": {"exit_code": exit_code, "stdout": json.dumps(envelope), "stderr": "", "timed_out": timeout, "spawn_error": spawn}, "expected": expected})
with (package / "evals/cases.jsonl").open("x", encoding="utf-8") as stream:
    for item in cases:
        stream.write(json.dumps(item, ensure_ascii=True) + "\n")

evidence = Path(__file__).parent
repo = evidence / "native/repo"
repo.mkdir(parents=True)
(repo / "spec.md").write_text("Accept a value only when it is strictly less than the maximum.\n", encoding="utf-8")
(repo / "candidate.py").write_text("def accepts(value, maximum):\n    return value <= maximum\n", encoding="utf-8")
intake = evidence / "native/intake"
intake.mkdir()
contract = Path("C:/Users/bryan/.codex/advisor/contract.md")
request = {"schema": "advisor-request-v1", "ask": "Does candidate.py satisfy spec.md?", "type": "done", "repo_root": str(repo.resolve()), "claude_path": "C:/Users/bryan/.local/bin/claude.exe", "contract_path": str(contract), "contract_sha256": hashlib.sha256(contract.read_bytes()).hexdigest(), "total_budget_usd": "2.00", "timeout_seconds": 180}
(intake / "request.json").write_text(json.dumps(request, indent=2), encoding="utf-8")
labels = ["REQUEST TYPE and ONE-LINE ASK", "REPO ROOT", "TASK AS GIVEN", "SCOPE", "BINDING CONSTRAINTS", "FACTS", "INFERENCES", "STATE", "ATTEMPTS", "CURRENT PLAN", "OPTIONS CONSIDERED", "ASSUMPTIONS", "OPEN QUESTIONS", "WHAT WOULD CHANGE MY MIND", "EXCERPTS"]
contents = ["done: Does candidate.py satisfy spec.md?", str(repo.resolve()) + "\nVerify these claims against the repository. Do not trust this briefing.", 'Synthetic test request: "Check the candidate against the selected specification."', "Review only spec.md and candidate.py. No modifications or test execution.", "The external advisor contract requires a read-only review. No other repository policies exist in this synthetic fixture.", 'spec.md:1 -> "Accept a value only when it is strictly less than the maximum."\ncandidate.py:2 -> "    return value <= maximum"', "UNKNOWN - determine the relationship independently.", "Both files were authored for this test [MODIFIED THIS SESSION]. No Git metadata. They are the candidate and contract, not proof of correctness.", "No earlier reviewer attempts or runtime tests.", "1. Decide whether to retain candidate.py based on specification comparison.", "No alternatives selected before review.", "The selected specification is the intended behavior.", "Does the comparison satisfy the requirement at the boundary?", "A directly cited mismatch would change the completion claim.", "none"]
(intake / "briefing.md").write_text("\n\n".join("## " + label + "\n" + value for label, value in zip(labels, contents)), encoding="utf-8")
