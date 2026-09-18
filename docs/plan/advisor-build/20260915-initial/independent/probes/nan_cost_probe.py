import json

import runner_probe as base


RUN_DIR = base.ROOT / "nan-cost-run"


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
    first_error = None
    try:
        base.advisor.run_review(
            base.REQUEST,
            RUN_DIR,
            base.BRIEFING,
            execute=nan_cost_execute,
        )
    except Exception as error:
        first_error = {"type": type(error).__name__, "message": str(error)}

    attempt = RUN_DIR / "attempt-001"
    second_error = None
    try:
        base.advisor.run_review(
            base.REQUEST,
            RUN_DIR,
            base.BRIEFING,
            reason="retry",
            execute=base.fake_execute,
        )
    except Exception as error:
        second_error = {"type": type(error).__name__, "message": str(error)}

    print(json.dumps({
        "first_error": first_error,
        "attempt_files_after_failure": sorted(path.name for path in attempt.iterdir()),
        "execution_receipt_exists": (attempt / "execution.json").exists(),
        "response_exists": (attempt / "response.md").exists(),
        "second_error": second_error,
    }, indent=2))


if __name__ == "__main__":
    main()
