import json

import runner_probe as base


NAN_RUN = base.ROOT / "nan-cost-retest"
CORRUPT_RUN = base.ROOT / "corrupt-history-retest"


def nan_cost_execute(argv, cwd, timeout):
    if "--version" in argv:
        stdout = b"2.1.273 (Claude Code)\n"
    elif "--help" in argv:
        stdout = (" ".join(base.advisor.REQUIRED_FLAGS) + " --append-system-prompt[-file]\n").encode("utf-8")
    else:
        stdout = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "result": base.RESPONSE,
                "total_cost_usd": float("nan"),
            }
        ).encode("utf-8")
    return {
        "exit_code": 0,
        "stdout": stdout,
        "stderr": b"",
        "timed_out": False,
        "spawn_error": None,
    }


def main():
    nan_receipt = base.advisor.run_review(
        base.REQUEST,
        NAN_RUN,
        base.BRIEFING,
        execute=nan_cost_execute,
    )
    retained_nan = base.advisor.read_json(NAN_RUN / "attempt-001" / "execution.json")
    if nan_receipt["response_status"] != "INVALID":
        raise AssertionError("nonfinite reported cost was not classified INVALID")
    if retained_nan != nan_receipt:
        raise AssertionError("retained nonfinite-cost receipt is incomplete or changed")

    base.advisor.run_review(
        base.REQUEST,
        CORRUPT_RUN,
        base.BRIEFING,
        execute=base.fake_execute,
    )
    corrupt_receipt = CORRUPT_RUN / "attempt-001" / "execution.json"
    corrupt_receipt.write_bytes(b'{"partial":')
    before = len(base.CALLS)
    blocked = None
    try:
        base.advisor.run_review(
            base.REQUEST,
            CORRUPT_RUN,
            base.BRIEFING,
            reason="retry",
            execute=base.fake_execute,
        )
    except ValueError as error:
        blocked = str(error)
    if not blocked or len(base.CALLS) != before:
        raise AssertionError("corrupt prior receipt did not block before preflight/invocation")

    print(json.dumps({
        "status": "PASS",
        "qualification": "SIMULATED_PROCESS_ONLY",
        "nonfinite_cost": {
            "response_status": nan_receipt["response_status"],
            "error": nan_receipt["error"],
            "receipt_json_valid": True,
        },
        "corrupt_history": {
            "blocked": True,
            "error": blocked,
            "additional_execute_calls": len(base.CALLS) - before,
        },
    }, indent=2))


if __name__ == "__main__":
    main()
