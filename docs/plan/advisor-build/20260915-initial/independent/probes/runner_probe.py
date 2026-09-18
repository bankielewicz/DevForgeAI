import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[4]
SCRIPT = WORKSPACE / "src" / "agents" / "skills" / "advisor" / "scripts" / "advisor_run.py"
SPEC = importlib.util.spec_from_file_location("advisor_run", SCRIPT)
advisor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(advisor)

SYNTHETIC = ROOT / "synthetic-repo"
REQUEST = json.loads((ROOT / "intake" / "request.json").read_text(encoding="utf-8"))
BRIEFING = ROOT / "intake" / "briefing.md"
RUN_DIR = ROOT / "simulated-run"
CALLS = []


RESPONSE = """VERDICT: STOP_REDIRECT

ASK RESTATED:
Determine whether src/limit_cli.py satisfies docs/limit-cli-spec.md.

DO THIS:
1. Reject the completion claim because the candidate accepts noncanonical values and sends invalid-input errors to stdout.
2. Report LIM-01 and LIM-03 as failed while leaving the candidate unchanged.

DO NOT:
- Treat the single happy-path test as specification conformance.

CLAIM AUDIT:
- The candidate must reject surrounding whitespace -> CONTRADICTED (src/limit_cli.py:6) - actually: strip removes surrounding whitespace before parsing.
- Invalid input must write only to stderr -> CONTRADICTED (src/limit_cli.py:10) - actually: print without file=sys.stderr writes to stdout.
- The existing test covers only valid input -> CONFIRMED (tests/test_limit_cli.py:11).

RISKS:
1. A completion claim would ship invalid-input behavior - triggered by: whitespace, leading zero, malformed, or out-of-range input - detect early by: exact stdout/stderr and exit-code probes.

COULD NOT VERIFY:
- Runtime behavior beyond the retained happy-path test - would need: executed negative-path probes.

FLIP CONDITIONS:
- A different candidate revision that rejects noncanonical input and writes every invalid-input error only to stderr.
"""


def fake_execute(argv, cwd, timeout):
    CALLS.append({"argv": list(map(str, argv)), "cwd": str(cwd), "timeout": timeout})
    if "--version" in argv:
        stdout = b"2.1.273 (Claude Code)\n"
    elif "--help" in argv:
        stdout = (" ".join(advisor.REQUIRED_FLAGS) + " --append-system-prompt[-file]\n").encode("utf-8")
    else:
        stdout = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "result": RESPONSE,
                "total_cost_usd": 0.0,
            }
        ).encode("utf-8")
    return {
        "exit_code": 0,
        "stdout": stdout,
        "stderr": b"",
        "timed_out": False,
        "spawn_error": None,
    }


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    receipt = advisor.run_review(REQUEST, RUN_DIR, BRIEFING, execute=fake_execute)
    require(receipt["execution_status"] == "SUCCEEDED", "simulated process did not succeed")
    require(receipt["response_status"] == "VALID", "valid structured response was rejected")
    require(receipt["verdict"] == "STOP_REDIRECT", "verdict was not retained")
    require(receipt["all_unverified"] is False, "confirmed/contradicted claims were lost")

    review_calls = [call for call in CALLS if "--print" in call["argv"]]
    require(len(review_calls) == 1, "runner did not issue exactly one reviewer process call")
    command = review_calls[0]["argv"]
    require(review_calls[0]["cwd"] == str(SYNTHETIC), "review cwd changed")
    require(command[command.index("--max-budget-usd") + 1] == "1.00", "attempt cap is not half the total")
    require(command[command.index("--tools") + 1] == "Read,Grep,Glob", "tool allowlist changed")
    require(command[command.index("--permission-mode") + 1] == "dontAsk", "permission mode changed")
    require("--restricted" in command and "--safe-mode" in command, "read-only confinement flags are absent")
    require("--dangerously-skip-permissions" not in command, "unsafe permission bypass was added")

    attempt = RUN_DIR / "attempt-001"
    required = {
        "briefing.md",
        "started.json",
        "preflight.json",
        "stdout.txt",
        "stderr.txt",
        "execution.json",
        "response.md",
    }
    require(required <= {path.name for path in attempt.iterdir()}, "retained artifact set is incomplete")
    require((attempt / "briefing.md").read_bytes() == BRIEFING.read_bytes(), "briefing bytes changed")
    require((attempt / "response.md").read_text(encoding="utf-8") == RESPONSE, "response extraction changed")
    require(receipt["briefing_sha256"] == hashlib.sha256(BRIEFING.read_bytes()).hexdigest(), "briefing digest mismatch")

    all_unverified = advisor.parse_response(RESPONSE.replace(
        "-> CONTRADICTED (src/limit_cli.py:6) - actually:",
        "-> UNVERIFIED (review tool unavailable) - actually:",
    ).replace(
        "-> CONTRADICTED (src/limit_cli.py:10) - actually:",
        "-> UNVERIFIED (review tool unavailable) - actually:",
    ).replace(
        "-> CONFIRMED (tests/test_limit_cli.py:11).",
        "-> UNVERIFIED (review tool unavailable).",
    ))
    require(all_unverified["all_unverified"] is True, "all-unverified advice was not flagged")

    print(json.dumps({
        "status": "PASS",
        "qualification": "SIMULATED_PROCESS_ONLY",
        "review_calls": len(review_calls),
        "verdict": receipt["verdict"],
        "all_unverified": receipt["all_unverified"],
        "attempt_files": sorted(path.name for path in attempt.iterdir()),
        "command": command,
    }, indent=2))


if __name__ == "__main__":
    main()
