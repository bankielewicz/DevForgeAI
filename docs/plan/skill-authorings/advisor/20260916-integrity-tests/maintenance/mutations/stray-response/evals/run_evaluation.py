"""Evaluate JSONL fixtures with deterministic graders; evidence only."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import advisor_run as advisor


def observe(case):
    if case["kind"] == "environment":
        return {"environment": advisor.build_environment(case["input"]["auth_mode"], case["input"]["environment"])}
    if case["kind"] == "response":
        try:
            parsed = advisor.parse_response(case["input"])
            return {"response_status": "VALID", "verdict": parsed["verdict"], "all_unverified": parsed["all_unverified"]}
        except ValueError:
            return {"response_status": "INVALID", "verdict": None, "all_unverified": None}
    if case["kind"] == "process":
        payload = dict(case["input"])
        payload["stdout"] = payload["stdout"].encode("utf-8")
        payload["stderr"] = payload["stderr"].encode("utf-8")
        result, _ = advisor.interpret(payload)
        return {key: result[key] for key in ("execution_status", "response_status", "verdict", "all_unverified")}
    if case["kind"] == "stream":
        source = case["input"]
        if not isinstance(source, dict) or set(source) - {"process", "cap"} or "process" not in source:
            raise ValueError("Stream fixture requires process and optional cap")
        payload = dict(source["process"])
        payload["stdout"] = payload["stdout"].encode("utf-8")
        payload["stderr"] = payload["stderr"].encode("utf-8")
        result, _, _ = advisor.interpret_stream(payload, source.get("cap"))
        return {key: result[key] for key in (
            "execution_status", "response_status", "verdict", "all_unverified",
            "reported_cost_usd", "budget_cap_exceeded")}
    raise ValueError("Unknown fixture kind")


def grade(actual, expected):
    return json.dumps(actual, sort_keys=True, allow_nan=False) == json.dumps(expected, sort_keys=True, allow_nan=False)


def evaluate(cases_path, output):
    cases_path, output = Path(cases_path), Path(output)
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for case in cases:
        if (not isinstance(case, dict) or set(case) != {"id", "kind", "input", "expected"}
                or not isinstance(case["id"], str) or not case["id"].strip()
                or not isinstance(case["expected"], dict)):
            raise ValueError("Invalid evaluation case shape")
    ids = [case["id"] for case in cases]
    if not cases or len(ids) != len(set(ids)):
        raise ValueError("Fixtures must have nonempty unique IDs")
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for case in cases:
        try:
            actual = observe(case)
            result = {"id": case["id"], "status": "PASS" if grade(actual, case["expected"]) else "FAIL", "actual": actual, "expected": case["expected"]}
        except (ValueError, KeyError, TypeError) as error:
            result = {"id": case["id"], "status": "ERROR", "error": str(error)}
        results.append(result)
    with (output / "results.jsonl").open("x", encoding="utf-8") as stream:
        for result in results:
            stream.write(json.dumps(result, ensure_ascii=True) + "\n")
    passed = sum(result["status"] == "PASS" for result in results)
    summary = {"schema": "advisor-evaluation-v1", "required": len(cases), "passed": passed,
               "pass_rate": 100 * passed / len(cases), "cases_sha256": advisor.digest(cases_path.read_bytes()),
               "framework_acceptance": "NOT_EVALUATED", "native_qualification": "NOT_RUN"}
    advisor.write_json(output / "summary.json", summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path(__file__).parent / "cases.jsonl")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate(args.cases, args.output)
        print(json.dumps(result))
        return 0 if result["passed"] == result["required"] else 1
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
