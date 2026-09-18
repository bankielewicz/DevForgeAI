import hashlib
import json

import runner_probe as initial


def main():
    first_execution = initial.RUN_DIR / "attempt-001" / "execution.json"
    first_digest = hashlib.sha256(first_execution.read_bytes()).hexdigest()
    receipt = initial.advisor.run_review(
        initial.REQUEST,
        initial.RUN_DIR,
        initial.BRIEFING,
        reason="citation",
        execute=initial.fake_execute,
    )
    if hashlib.sha256(first_execution.read_bytes()).hexdigest() != first_digest:
        raise AssertionError("attempt-001 was modified")
    if receipt["attempt"] != 2 or receipt["reason"] != "citation":
        raise AssertionError("citation follow-up was not retained as attempt-002")
    if receipt["response_status"] != "VALID" or receipt["verdict"] != "STOP_REDIRECT":
        raise AssertionError("follow-up response was not retained")
    third_blocked = False
    try:
        initial.advisor.run_review(
            initial.REQUEST,
            initial.RUN_DIR,
            initial.BRIEFING,
            reason="context",
            execute=initial.fake_execute,
        )
    except ValueError as error:
        third_blocked = "Two-attempt limit exhausted" in str(error)
    if not third_blocked:
        raise AssertionError("third process attempt was not blocked")
    print(json.dumps({
        "status": "PASS",
        "qualification": "SIMULATED_PROCESS_ONLY",
        "attempt": receipt["attempt"],
        "reason": receipt["reason"],
        "prior_attempt_unchanged": True,
        "third_attempt_blocked": True,
    }, indent=2))


if __name__ == "__main__":
    main()
