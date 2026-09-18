"""Append deterministic streaming cases to the staged advisor JSONL fixtures."""

import json
from pathlib import Path


CASES = Path(__file__).resolve().parents[3] / "skill-authorings/advisor/20260916T134000Z-streaming/candidate/evals/cases.jsonl"
RESPONSE = (
    "VERDICT: PROCEED\n\n"
    "ASK RESTATED:\nCheck the selected implementation.\n\n"
    "DO THIS:\n1. Continue the selected task.\n\n"
    "DO NOT:\n- Expand scope.\n\n"
    "CLAIM AUDIT:\n- selected behavior -> CONFIRMED (sample.txt:1)\n\n"
    "RISKS:\nnone\n\n"
    "COULD NOT VERIFY:\nnone\n\n"
    "FLIP CONDITIONS:\n- Changed evidence.\n"
)


def event(**changes):
    value = {"type": "result", "subtype": "success", "is_error": False,
             "result": RESPONSE, "total_cost_usd": 0.25}
    value.update(changes)
    return value


def line(*events):
    return "".join(json.dumps(value, separators=(",", ":")) + "\n" for value in events)


def process(stdout, **changes):
    value = {"exit_code": 0, "stdout": stdout, "stderr": "", "timed_out": False,
             "spawn_error": None, "interrupted": False, "transport_error": None,
             "cleanup": {"child_exited": True, "pipes_closed": True}}
    value.update(changes)
    return value


CORE_SUCCESS = {"execution_status": "SUCCEEDED", "response_status": "VALID", "verdict": "PROCEED",
                "all_unverified": False, "reported_cost_usd": 0.25, "budget_cap_exceeded": False}
CORE_INVALID = {"execution_status": "SUCCEEDED", "response_status": "INVALID", "verdict": None,
                "all_unverified": None, "reported_cost_usd": None, "budget_cap_exceeded": False}
CORE_FAILED = {"execution_status": "FAILED", "response_status": "NOT_EVALUATED", "verdict": None,
               "all_unverified": None, "reported_cost_usd": None, "budget_cap_exceeded": False}

cases = [
    {"id": "stream-success", "kind": "stream",
     "input": {"process": process(line({"type": "system", "subtype": "init"}, event())), "cap": "1.00"},
     "expected": CORE_SUCCESS},
    {"id": "stream-budget-failed-cost", "kind": "stream",
     "input": {"process": process(line(event(subtype="error_max_budget_usd", is_error=True,
                                                result="partial", total_cost_usd=1.015353)), exit_code=1), "cap": "1.00"},
     "expected": {**CORE_FAILED, "reported_cost_usd": 1.015353, "budget_cap_exceeded": True}},
    {"id": "stream-malformed", "kind": "stream",
     "input": {"process": process('{"type":"result"\n'), "cap": "1.00"}, "expected": CORE_INVALID},
    {"id": "stream-missing-result", "kind": "stream",
     "input": {"process": process(line({"type": "system"})), "cap": "1.00"}, "expected": CORE_INVALID},
    {"id": "stream-duplicate-result", "kind": "stream",
     "input": {"process": process(line(event(), event())), "cap": "1.00"}, "expected": CORE_INVALID},
    {"id": "stream-result-not-terminal", "kind": "stream",
     "input": {"process": process(line(event(), {"type": "system"})), "cap": "1.00"}, "expected": CORE_INVALID},
    {"id": "stream-timeout", "kind": "stream",
     "input": {"process": process("", exit_code=None, timed_out=True), "cap": "1.00"},
     "expected": {**CORE_FAILED, "execution_status": "TIMEOUT"}},
    {"id": "stream-interrupted", "kind": "stream",
     "input": {"process": process(line(event()), exit_code=None, interrupted=True), "cap": "1.00"},
     "expected": {**CORE_FAILED, "reported_cost_usd": 0.25}},
    {"id": "stream-cleanup-child-active", "kind": "stream",
     "input": {"process": process(line(event()), cleanup={"child_exited": False, "pipes_closed": True}), "cap": "1.00"},
     "expected": {**CORE_FAILED, "reported_cost_usd": 0.25}},
    {"id": "stream-cleanup-pipe-open", "kind": "stream",
     "input": {"process": process(line(event()), cleanup={"child_exited": True, "pipes_closed": False}), "cap": "1.00"},
     "expected": {**CORE_FAILED, "reported_cost_usd": 0.25}},
    {"id": "stream-transport-error", "kind": "stream",
     "input": {"process": process(line(event()), transport_error="reader failed"), "cap": "1.00"},
     "expected": {**CORE_FAILED, "reported_cost_usd": 0.25}},
]

existing = [json.loads(item) for item in CASES.read_text(encoding="utf-8").splitlines() if item.strip()]
existing_ids = {item["id"] for item in existing}
new_ids = {item["id"] for item in cases}
if existing_ids & new_ids:
    raise SystemExit("streaming fixture IDs already exist")
with CASES.open("a", encoding="utf-8", newline="\n") as output:
    for case in cases:
        output.write(json.dumps(case, ensure_ascii=True, allow_nan=False, separators=(",", ":")) + "\n")
print(json.dumps({"appended": len(cases), "total": len(existing) + len(cases)}))
