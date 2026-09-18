"""Independent synthetic acceptance cases for the advisor streaming delivery.

This runner never invokes Claude. It treats the candidate as a black-box CLI for
workflow cases and uses the public streaming module only for real local process
deadline cases that cannot be expressed through the fixed Claude command line.
"""

import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


SESSION_ID = "12345678-1234-1234-1234-123456789abc"
SECRET_TEXT = "SECRET_MODEL_TEXT_7812"
SECRET_PATH = "C:/secret/tool/payload.txt"
RAW_STDERR = "RAW_STDERR_MARKER_9921\n"
RESPONSE = """VERDICT: PROCEED

ASK RESTATED:
Check the synthetic candidate.

DO THIS:
1. Keep the tested behavior.

DO NOT:
- Expand the test scope.

CLAIM AUDIT:
- synthetic claim -> CONFIRMED (fixture.txt:1 -> \"ok\")

RISKS:
- none

COULD NOT VERIFY:
- live provider behavior

FLIP CONDITIONS:
- a changed contract
"""
BRIEFING_LABELS = (
    "REQUEST TYPE and ONE-LINE ASK", "REPO ROOT", "TASK AS GIVEN", "SCOPE",
    "BINDING CONSTRAINTS", "FACTS", "INFERENCES", "STATE", "ATTEMPTS",
    "CURRENT PLAN", "OPTIONS CONSIDERED", "ASSUMPTIONS", "OPEN QUESTIONS",
    "WHAT WOULD CHANGE MY MIND", "EXCERPTS",
)
RESTRICTED_FLAGS = (
    "--restricted", "--safe-mode", "--strict-mcp-config", "--tools",
    "--allowedTools", "--permission-mode", "--permission-prompts",
    "--no-session-persistence", "--max-budget-usd",
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def result_event(subtype="success", is_error=False, result=RESPONSE, cost=0.25):
    return {
        "type": "result",
        "subtype": subtype,
        "is_error": is_error,
        "result": result,
        "total_cost_usd": cost,
    }


def encoded_line(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("utf-8") + b"\n"


def expected_success_stream():
    events = [
        {"type": "system", "subtype": "init", "session_id": SESSION_ID},
        {"type": "assistant", "message": {"content": [
            {"type": "text", "text": SECRET_TEXT},
            {"type": "tool_use", "name": "Read", "input": {"file_path": SECRET_PATH}},
            {"type": "tool_use", "name": "Bad\u001b[31m", "input": {"value": SECRET_TEXT}},
        ]}},
        result_event(),
    ]
    # The fixture uses Python's text stdout on native Windows, which expands
    # each LF record terminator to CRLF before the candidate captures bytes.
    return b"".join(encoded_line(item).replace(b"\n", b"\r\n") for item in events)


FAKE_SOURCE = r'''import json, os, sys

SESSION_ID = "12345678-1234-1234-1234-123456789abc"
SECRET_TEXT = "SECRET_MODEL_TEXT_7812"
SECRET_PATH = "C:/secret/tool/payload.txt"
RAW_STDERR = "RAW_STDERR_MARKER_9921\n"
RESPONSE = """VERDICT: PROCEED

ASK RESTATED:
Check the synthetic candidate.

DO THIS:
1. Keep the tested behavior.

DO NOT:
- Expand the test scope.

CLAIM AUDIT:
- synthetic claim -> CONFIRMED (fixture.txt:1 -> \"ok\")

RISKS:
- none

COULD NOT VERIFY:
- live provider behavior

FLIP CONDITIONS:
- a changed contract
"""

def emit(value):
    sys.stdout.write(json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()

def result(subtype="success", is_error=False, text=RESPONSE, cost=0.25):
    return {"type":"result","subtype":subtype,"is_error":is_error,
            "result":text,"total_cost_usd":cost}

if "--version" in sys.argv:
    print("synthetic-claude 1.0")
    raise SystemExit(0)
if "--help" in sys.argv:
    print(" ".join([
        "--print","--model","--effort","--restricted","--safe-mode",
        "--strict-mcp-config","--tools","--allowedTools","--permission-mode",
        "--permission-prompts","--add-dir","--append-system-prompt-file",
        "--no-session-persistence","--max-budget-usd","--output-format",
        "--verbose","stream-json"
    ]))
    raise SystemExit(0)

argv_path = os.environ.get("ADVISOR_ARGV_PATH")
if argv_path:
    with open(argv_path, "w", encoding="utf-8", newline="\n") as stream:
        json.dump(sys.argv[1:], stream, ensure_ascii=True)
        stream.write("\n")
counter_path = os.environ.get("ADVISOR_COUNTER_PATH")
if counter_path:
    with open(counter_path, "a", encoding="ascii", newline="\n") as stream:
        stream.write("review\n")
env_path = os.environ.get("ADVISOR_ENV_PATH")
if env_path:
    keys = [key.upper() for key in os.environ]
    with open(env_path, "w", encoding="utf-8", newline="\n") as stream:
        json.dump({"anthropic_present":"ANTHROPIC_API_KEY" in keys,
                   "other_present":"ADVISOR_OTHER_MARKER" in keys}, stream)
        stream.write("\n")

scenario = os.environ.get("ADVISOR_SCENARIO", "success")
format_name = None
if "--output-format" in sys.argv:
    format_name = sys.argv[sys.argv.index("--output-format") + 1]

if format_name == "json":
    print(json.dumps(result(), ensure_ascii=True, allow_nan=False))
    raise SystemExit(0)

sys.stderr.write(RAW_STDERR)
sys.stderr.flush()
if scenario == "success":
    emit({"type":"system","subtype":"init","session_id":SESSION_ID})
    emit({"type":"assistant","message":{"content":[
        {"type":"text","text":SECRET_TEXT},
        {"type":"tool_use","name":"Read","input":{"file_path":SECRET_PATH}},
        {"type":"tool_use","name":"Bad\u001b[31m","input":{"value":SECRET_TEXT}}
    ]}})
    emit(result())
elif scenario == "malformed":
    sys.stdout.write('{"type":"system"\n')
    emit(result())
elif scenario == "missing":
    emit({"type":"system","subtype":"init","session_id":SESSION_ID})
elif scenario == "duplicate":
    emit(result())
    emit(result())
elif scenario == "after":
    emit(result())
    emit({"type":"system","subtype":"late"})
elif scenario == "budget":
    emit(result("error_max_budget_usd", True, "partial untrusted text", 1.015353))
    raise SystemExit(1)
else:
    raise SystemExit(9)
'''


class Recorder:
    def __init__(self):
        self.cases = []

    def add(self, case_id, passed, reason, evidence=None, actual=None):
        self.cases.append({
            "id": case_id,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
            "evidence": evidence or [],
            "actual": actual,
        })

    def error(self, case_id, error):
        self.cases.append({
            "id": case_id,
            "status": "ERROR",
            "reason": type(error).__name__ + ": " + str(error),
            "evidence": [],
            "actual": None,
        })


def make_fixture(root, auth_mode="subscription"):
    root.mkdir(parents=True)
    repo = root / "repo"
    repo.mkdir()
    (repo / "fixture.txt").write_text("ok\n", encoding="utf-8", newline="\n")
    contract = root / "contract.md"
    contract.write_text("Synthetic response contract.\n", encoding="utf-8", newline="\n")
    briefing = root / "briefing.md"
    briefing.write_text(
        "\n\n".join("## " + label + "\nSynthetic fixture value." for label in BRIEFING_LABELS) + "\n",
        encoding="utf-8", newline="\n",
    )
    fake_py = root / "fake_claude.py"
    fake_py.write_text(FAKE_SOURCE, encoding="utf-8", newline="\n")
    fake_cmd = root / "claude.cmd"
    fake_cmd.write_text(
        '@echo off\r\n"' + str(Path(sys.executable).resolve()) + '" -B -X utf8 "%~dp0fake_claude.py" %*\r\n',
        encoding="ascii", newline="",
    )
    request = {
        "schema": "advisor-request-v1",
        "ask": "Check a synthetic candidate.",
        "type": "approach",
        "model": "opus",
        "effort": "high",
        "auth_mode": auth_mode,
        "repo_root": str(repo.resolve()),
        "claude_path": str(fake_cmd.resolve()),
        "contract_path": str(contract.resolve()),
        "contract_sha256": sha256(contract.read_bytes()),
        "total_budget_usd": "2.00",
        "timeout_seconds": 10,
    }
    request_path = root / "request.json"
    write_json(request_path, request)
    return {
        "root": root,
        "repo": repo,
        "contract": contract,
        "briefing": briefing,
        "request": request_path,
        "fake": fake_cmd,
        "argv": root / "observed-argv.json",
        "counter": root / "review-counter.txt",
        "env": root / "observed-env.json",
    }


def run_cli(candidate, fixture, run_dir, scenario="success", show_progress=False,
            reason="initial", request=None, runner=None, extra_env=None, timeout=30):
    runner = Path(runner or (candidate / "scripts" / "advisor_run.py")).resolve()
    command = [
        sys.executable, "-B", "-X", "utf8", str(runner), "run",
        "--request", str(Path(request or fixture["request"]).resolve()),
        "--run-dir", str(Path(run_dir).resolve()),
        "--briefing", str(fixture["briefing"].resolve()),
        "--reason", reason,
    ]
    if show_progress:
        command.append("--show-progress")
    environment = dict(os.environ)
    environment.update({
        "ADVISOR_SCENARIO": scenario,
        "ADVISOR_ARGV_PATH": str(fixture["argv"].resolve()),
        "ADVISOR_COUNTER_PATH": str(fixture["counter"].resolve()),
        "ADVISOR_ENV_PATH": str(fixture["env"].resolve()),
    })
    if extra_env:
        environment.update(extra_env)
    started = time.monotonic()
    process = subprocess.run(
        command, cwd=Path.cwd(), env=environment, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, shell=False,
    )
    return {
        "command": command,
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "duration_seconds": time.monotonic() - started,
    }


def parsed_stdout(run):
    return json.loads(run["stdout"].decode("utf-8-sig"))


def invocation_count(fixture):
    return len(fixture["counter"].read_text(encoding="ascii").splitlines()) if fixture["counter"].exists() else 0


def process_running(pid):
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return False
    try:
        code = ctypes.c_ulong()
        if not ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
            return False
        return code.value == STILL_ACTIVE
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


def stop_owned_process(pid):
    if not process_running(pid):
        return
    handle = ctypes.windll.kernel32.OpenProcess(0x0001 | 0x00100000, False, pid)
    if not handle:
        return
    try:
        ctypes.windll.kernel32.TerminateProcess(handle, 1)
        ctypes.windll.kernel32.WaitForSingleObject(handle, 1000)
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


def import_stream(candidate):
    path = candidate / "scripts" / "advisor_stream.py"
    spec = importlib.util.spec_from_file_location("independent_candidate_advisor_stream", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_wrapper(shell, candidate, root):
    fixture = make_fixture(root / "fixture")
    run_dir = root / "run with spaces"
    wrapper = candidate / "scripts" / "advisor.ps1"
    base = [
        str(shell), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper),
        "-Request", str(fixture["request"]), "-Briefing", str(fixture["briefing"]),
        "-RunDir", str(run_dir), "-Python", sys.executable, "-ShowProgress",
    ]
    env = dict(os.environ)
    env.update({
        "ADVISOR_SCENARIO": "success", "ADVISOR_ARGV_PATH": str(fixture["argv"]),
        "ADVISOR_COUNTER_PATH": str(fixture["counter"]), "ADVISOR_ENV_PATH": str(fixture["env"]),
    })
    first = subprocess.run(
        base + ["-Reason", "initial"], cwd=Path.cwd(), env=env,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30, shell=False,
    )
    env["ADVISOR_SCENARIO"] = "budget"
    second = subprocess.run(
        base + ["-Reason", "retry"], cwd=Path.cwd(), env=env,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30, shell=False,
    )
    return fixture, run_dir, first, second


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--legacy-candidate", required=True, type=Path)
    parser.add_argument("--trial-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--powershell5", required=True, type=Path)
    parser.add_argument("--powershell7", required=True, type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve(strict=True)
    legacy = args.legacy_candidate.resolve(strict=True)
    trial_root = args.trial_root.resolve()
    if trial_root.exists():
        raise SystemExit("trial root must be fresh")
    trial_root.mkdir(parents=True)
    recorder = Recorder()

    # Shared successful quiet and streaming observations.
    try:
        quiet_fixture = make_fixture(trial_root / "shared-quiet")
        quiet_run_dir = quiet_fixture["root"] / "run"
        quiet = run_cli(candidate, quiet_fixture, quiet_run_dir)
        write_json(quiet_fixture["root"] / "process.json", {
            "command": quiet["command"], "exit_code": quiet["exit_code"],
            "duration_seconds": quiet["duration_seconds"],
            "stdout_sha256": sha256(quiet["stdout"]), "stderr_sha256": sha256(quiet["stderr"]),
        })
        quiet_receipt = parsed_stdout(quiet)
        recorder.add("SV-SP-001", quiet["exit_code"] == 0 and quiet_receipt.get("schema") == "advisor-execution-v1"
                     and quiet_receipt.get("response_status") == "VALID",
                     "Quiet mode retained the v1 JSON workflow.", ["shared-quiet/process.json", "shared-quiet/run/attempt-001/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-001", error)

    try:
        stream_fixture = make_fixture(trial_root / "shared-stream")
        stream_run_dir = stream_fixture["root"] / "run"
        stream = run_cli(candidate, stream_fixture, stream_run_dir, show_progress=True)
        (stream_fixture["root"] / "cli.stdout").write_bytes(stream["stdout"])
        (stream_fixture["root"] / "cli.stderr").write_bytes(stream["stderr"])
        write_json(stream_fixture["root"] / "process.json", {
            "command": stream["command"], "exit_code": stream["exit_code"],
            "duration_seconds": stream["duration_seconds"],
            "stdout_sha256": sha256(stream["stdout"]), "stderr_sha256": sha256(stream["stderr"]),
        })
        receipt_path = stream_run_dir / "attempt-001" / "execution.json"
        receipt = read_json(receipt_path)
        command = receipt["command"]
        progress = stream["stderr"].decode("utf-8", errors="replace")
        recorder.add("SV-SP-002", stream["exit_code"] == 0 and receipt.get("schema") == "advisor-execution-v2"
                     and receipt.get("response_status") == "VALID",
                     "Progress mode completed with a valid v2 receipt.", ["shared-stream/process.json", "shared-stream/run/attempt-001/execution.json"])
        recorder.add("SV-SP-003", command[command.index("--output-format") + 1] == "stream-json"
                     and command.count("--verbose") == 1,
                     "The retained native command selected stream-json and verbose exactly once.", ["shared-stream/run/attempt-001/execution.json"])
        recorder.add("SV-SP-004", all(flag in command for flag in RESTRICTED_FLAGS)
                     and command[command.index("--tools") + 1] == "Read,Grep,Glob"
                     and command[command.index("--allowedTools") + 1] == "Read,Grep,Glob",
                     "All legacy restricted read-only flags remained in the streaming command.", ["shared-stream/run/attempt-001/execution.json"])
        recorder.add("SV-SP-005", len(stream["stdout"].splitlines()) == 1 and b"session " not in stream["stdout"]
                     and "session " + SESSION_ID in progress and "assistant activity" in progress,
                     "Progress appeared on stderr while stdout contained one receipt line.", ["shared-stream/cli.stdout", "shared-stream/cli.stderr"])
        recorder.add("SV-SP-006", SECRET_TEXT not in progress and SECRET_PATH not in progress and RAW_STDERR.strip() not in progress,
                     "Model text, tool input and raw child stderr were absent from progress.", ["shared-stream/cli.stderr"])
        recorder.add("SV-SP-007", "tool Read" in progress and "Bad" not in progress and "\x1b" not in progress,
                     "Only allowlisted tool metadata was shown and no terminal escape reached progress.", ["shared-stream/cli.stderr"])
        whole = json.loads(stream["stdout"].decode("utf-8-sig"))
        recorder.add("SV-SP-008", isinstance(whole, dict) and whole.get("schema") == "advisor-execution-v2",
                     "The complete stdout decoded as one machine-readable JSON value.", ["shared-stream/cli.stdout"])
        raw_stdout = (stream_run_dir / "attempt-001" / "stdout.txt").read_bytes()
        raw_stderr = (stream_run_dir / "attempt-001" / "stderr.txt").read_bytes()
        recorder.add("SV-SP-009", raw_stdout == expected_success_stream() and raw_stderr == RAW_STDERR.replace("\n", "\r\n").encode("utf-8")
                     and receipt["stdout_sha256"] == sha256(raw_stdout) and receipt["stderr_sha256"] == sha256(raw_stderr),
                     "Raw child streams matched the independent fixture bytes and receipt digests.", ["shared-stream/run/attempt-001/stdout.txt", "shared-stream/run/attempt-001/stderr.txt", "shared-stream/run/attempt-001/execution.json"])
        final = read_json(stream_run_dir / "attempt-001" / "result.json")
        response = (stream_run_dir / "attempt-001" / "response.md").read_text(encoding="utf-8")
        recorder.add("SV-SP-010", final == result_event() and response == RESPONSE
                     and receipt.get("result_sha256") == sha256((stream_run_dir / "attempt-001" / "result.json").read_bytes()),
                     "The exact terminal envelope and validated response were retained and bound.", ["shared-stream/run/attempt-001/result.json", "shared-stream/run/attempt-001/response.md", "shared-stream/run/attempt-001/execution.json"])
        required_v2 = {"schema", "command", "output_format", "transport", "stdout_sha256", "stderr_sha256",
                       "result_sha256", "started_sha256", "preflight_sha256", "execution_status", "response_status"}
        started_ok = receipt.get("started_sha256") == sha256((stream_run_dir / "attempt-001" / "started.json").read_bytes())
        preflight_ok = receipt.get("preflight_sha256") == sha256((stream_run_dir / "attempt-001" / "preflight.json").read_bytes())
        recorder.add("SV-SP-019", required_v2 <= set(receipt) and started_ok and preflight_ok
                     and set(receipt["transport"]) == {"timed_out", "spawn_error", "interrupted", "transport_error", "cleanup"},
                     "The v2 receipt bound command, transport, raw streams, terminal envelope and pre-execution records.", ["shared-stream/run/attempt-001/execution.json", "shared-stream/run/attempt-001/started.json", "shared-stream/run/attempt-001/preflight.json"])
    except Exception as error:
        for case_id in ("SV-SP-002", "SV-SP-003", "SV-SP-004", "SV-SP-005", "SV-SP-006", "SV-SP-007",
                        "SV-SP-008", "SV-SP-009", "SV-SP-010", "SV-SP-019"):
            if not any(item["id"] == case_id for item in recorder.cases):
                recorder.error(case_id, error)

    # Strict framing negative paths.
    for case_id, scenario in (("SV-SP-011", "malformed"), ("SV-SP-012", "missing"),
                              ("SV-SP-013", "duplicate"), ("SV-SP-014", "after")):
        try:
            fixture = make_fixture(trial_root / case_id.lower())
            run_dir = fixture["root"] / "run"
            observed = run_cli(candidate, fixture, run_dir, scenario=scenario, show_progress=True)
            receipt = read_json(run_dir / "attempt-001" / "execution.json")
            passed = observed["exit_code"] == 1 and receipt["response_status"] == "INVALID"
            passed = passed and not (run_dir / "attempt-001" / "response.md").exists()
            recorder.add(case_id, passed, "The invalid stream was retained and rejected without advice.",
                         [f"{case_id.lower()}/run/attempt-001/execution.json", f"{case_id.lower()}/run/attempt-001/stdout.txt"])
        except Exception as error:
            recorder.error(case_id, error)

    # Real subprocess deadline, concurrent drain and cleanup observations.
    try:
        streaming = import_stream(candidate)
        deadline_root = trial_root / "deadline"
        deadline_root.mkdir()
        pid_path = deadline_root / "pid.txt"
        code = ("import os,time; "
                f"open({str(pid_path)!r},'w').write(str(os.getpid())); "
                "os.close(1); os.close(2); time.sleep(30)")
        started = time.monotonic()
        deadline = streaming.execute_stream([sys.executable, "-c", code], deadline_root, 0.2)
        duration = time.monotonic() - started
        pid = int(pid_path.read_text(encoding="ascii"))
        write_json(deadline_root / "result.json", dict(deadline, stdout=deadline["stdout"].decode("latin1"), stderr=deadline["stderr"].decode("latin1"), duration_seconds=duration, pid=pid))
        recorder.add("SV-SP-015", deadline["timed_out"] is True and duration < 5.75,
                     "EOF before child exit remained governed by the reviewer deadline plus bounded cleanup ceiling.", ["deadline/result.json"], {"duration_seconds": duration})

        flood_root = trial_root / "flood"
        flood_root.mkdir()
        size = 2 * 1024 * 1024
        flood_code = ("import sys; "
                      f"sys.stdout.buffer.write(b'x'*{size});sys.stdout.buffer.flush();"
                      f"sys.stderr.buffer.write(b'y'*{size});sys.stderr.buffer.flush()")
        flood = streaming.execute_stream([sys.executable, "-c", flood_code], flood_root, 10)
        write_json(flood_root / "result.json", {"exit_code": flood["exit_code"], "timed_out": flood["timed_out"],
                                                  "stdout_bytes": len(flood["stdout"]), "stderr_bytes": len(flood["stderr"]),
                                                  "cleanup": flood["cleanup"], "transport_error": flood["transport_error"]})
        recorder.add("SV-SP-016", flood["exit_code"] == 0 and not flood["timed_out"]
                     and len(flood["stdout"]) == size and len(flood["stderr"]) == size,
                     "Concurrent readers drained two full pipes without deadlock or truncation.", ["flood/result.json"])
        stopped = not process_running(pid)
        if not stopped:
            stop_owned_process(pid)
        recorder.add("SV-SP-017", deadline["cleanup"]["child_exited"] is True and stopped,
                     "The timed-out direct child was independently observed stopped.", ["deadline/result.json"])
        recorder.add("SV-SP-018", deadline["cleanup"]["pipes_closed"] is True and deadline["transport_error"] is None,
                     "Pipe readers closed within the cleanup ceiling and no cleanup uncertainty remained.", ["deadline/result.json"])
    except Exception as error:
        for case_id in ("SV-SP-015", "SV-SP-016", "SV-SP-017", "SV-SP-018"):
            if not any(item["id"] == case_id for item in recorder.cases):
                recorder.error(case_id, error)

    # v2 evidence tamper must block before another review invocation.
    try:
        fixture = make_fixture(trial_root / "v2-tamper")
        run_dir = fixture["root"] / "run"
        first = run_cli(candidate, fixture, run_dir, show_progress=True)
        before = invocation_count(fixture)
        preflight_path = run_dir / "attempt-001" / "preflight.json"
        preflight_path.write_bytes(preflight_path.read_bytes() + b" ")
        second = run_cli(candidate, fixture, run_dir, show_progress=True, reason="retry")
        recorder.add("SV-SP-020", first["exit_code"] == 0 and second["exit_code"] == 2
                     and invocation_count(fixture) == before and not (run_dir / "attempt-002").exists(),
                     "Tampered derived v2 evidence blocked the follow-up before reviewer invocation.", ["v2-tamper/run/attempt-001/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-020", error)

    # Exact legacy v1 compatibility and integrity.
    try:
        fixture = make_fixture(trial_root / "legacy-followup")
        run_dir = fixture["root"] / "run"
        first = run_cli(legacy, fixture, run_dir, runner=legacy / "scripts" / "advisor_run.py")
        old_files = {str(path.relative_to(run_dir)): sha256(path.read_bytes()) for path in run_dir.rglob("*") if path.is_file()}
        second = run_cli(candidate, fixture, run_dir, show_progress=True, reason="retry")
        unchanged = all(sha256((run_dir / name).read_bytes()) == digest for name, digest in old_files.items())
        recorder.add("SV-SP-021", first["exit_code"] == 0 and second["exit_code"] == 0 and unchanged
                     and read_json(run_dir / "attempt-002" / "execution.json")["schema"] == "advisor-execution-v2",
                     "An exact pre-change v1 attempt was accepted unchanged for one v2 follow-up.", ["legacy-followup/run/attempt-001/execution.json", "legacy-followup/run/attempt-002/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-021", error)

    try:
        fixture = make_fixture(trial_root / "legacy-tamper")
        run_dir = fixture["root"] / "run"
        first = run_cli(legacy, fixture, run_dir, runner=legacy / "scripts" / "advisor_run.py")
        (run_dir / "attempt-001" / "stdout.txt").write_bytes((run_dir / "attempt-001" / "stdout.txt").read_bytes() + b"x")
        before = invocation_count(fixture)
        second = run_cli(candidate, fixture, run_dir, show_progress=True, reason="retry")
        recorder.add("SV-SP-022", first["exit_code"] == 0 and second["exit_code"] == 2
                     and invocation_count(fixture) == before and not (run_dir / "attempt-002").exists(),
                     "Tampered legacy raw output blocked follow-up before reviewer invocation.", ["legacy-tamper/run/attempt-001/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-022", error)

    # Attempts, immutable request, and child-only auth.
    try:
        fixture = make_fixture(trial_root / "two-attempts")
        run_dir = fixture["root"] / "run"
        first = run_cli(candidate, fixture, run_dir, show_progress=True)
        second = run_cli(candidate, fixture, run_dir, reason="retry")
        before = invocation_count(fixture)
        third = run_cli(candidate, fixture, run_dir, show_progress=True, reason="retry")
        recorder.add("SV-SP-023", first["exit_code"] == 0 and second["exit_code"] == 0
                     and third["exit_code"] == 2 and invocation_count(fixture) == before
                     and not (run_dir / "attempt-003").exists(),
                     "A third attempt was blocked without reviewer invocation.", ["two-attempts/run/attempt-001/execution.json", "two-attempts/run/attempt-002/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-023", error)

    try:
        fixture = make_fixture(trial_root / "immutable-request")
        run_dir = fixture["root"] / "run"
        first = run_cli(candidate, fixture, run_dir, show_progress=True)
        changed = read_json(fixture["request"])
        changed["ask"] = "Changed ask must not reset the review."
        changed_path = fixture["root"] / "changed-request.json"
        write_json(changed_path, changed)
        before = invocation_count(fixture)
        second = run_cli(candidate, fixture, run_dir, show_progress=True, reason="retry", request=changed_path)
        recorder.add("SV-SP-024", first["exit_code"] == 0 and second["exit_code"] == 2
                     and invocation_count(fixture) == before and not (run_dir / "attempt-002").exists(),
                     "A changed request could not reset the same run or trigger another reviewer call.", ["immutable-request/run/request.json"])
    except Exception as error:
        recorder.error("SV-SP-024", error)

    try:
        fixture = make_fixture(trial_root / "auth")
        run_dir = fixture["root"] / "run"
        observed = run_cli(candidate, fixture, run_dir, show_progress=True,
                           extra_env={"AnThRoPiC_ApI_KeY": "synthetic-secret", "ADVISOR_OTHER_MARKER": "retained"})
        env_observed = read_json(fixture["env"])
        receipt = read_json(run_dir / "attempt-001" / "execution.json")
        recorder.add("SV-SP-025", observed["exit_code"] == 0 and env_observed == {"anthropic_present": False, "other_present": True}
                     and receipt["auth_mode"] == "subscription" and receipt["reserved_budget_usd"] == "1.00",
                     "Subscription mode removed only the case-insensitive Anthropic key while preserving policy and budget fields.", ["auth/observed-env.json", "auth/run/attempt-001/execution.json"])
    except Exception as error:
        recorder.error("SV-SP-025", error)

    try:
        fixture = make_fixture(trial_root / "budget")
        run_dir = fixture["root"] / "run"
        observed = run_cli(candidate, fixture, run_dir, scenario="budget", show_progress=True)
        receipt = read_json(run_dir / "attempt-001" / "execution.json")
        recorder.add("SV-SP-026", observed["exit_code"] == 1 and receipt["execution_status"] == "FAILED"
                     and receipt["response_status"] == "NOT_EVALUATED" and receipt["reported_cost_usd"] == 1.015353
                     and receipt["budget_cap_exceeded"] is True and (run_dir / "attempt-001" / "result.json").is_file()
                     and not (run_dir / "attempt-001" / "response.md").exists(),
                     "The failed terminal envelope retained reported cost and cap discrepancy without exposing advice.", ["budget/run/attempt-001/execution.json", "budget/run/attempt-001/result.json"])
    except Exception as error:
        recorder.error("SV-SP-026", error)

    # Native wrapper behavior in both required shells.
    for case_id, shell in (("SV-SP-027", args.powershell5.resolve(strict=True)),
                           ("SV-SP-028", args.powershell7.resolve(strict=True))):
        try:
            fixture, run_dir, first, second = run_wrapper(shell, candidate, trial_root / case_id.lower())
            (fixture["root"].parent / "first.stdout").write_bytes(first.stdout)
            (fixture["root"].parent / "first.stderr").write_bytes(first.stderr)
            (fixture["root"].parent / "second.stdout").write_bytes(second.stdout)
            (fixture["root"].parent / "second.stderr").write_bytes(second.stderr)
            first_receipt = json.loads(first.stdout.decode("utf-8-sig"))
            second_receipt = json.loads(second.stdout.decode("utf-8-sig"))
            passed = first.returncode == 0 and second.returncode == 1
            passed = passed and first_receipt["schema"] == "advisor-execution-v2" and second_receipt["reason"] == "retry"
            passed = passed and second_receipt["response_status"] == "NOT_EVALUATED"
            recorder.add(case_id, passed, "The native launcher forwarded all selected inputs and propagated success and failure exit codes.",
                         [f"{case_id.lower()}/first.stdout", f"{case_id.lower()}/second.stdout", f"{case_id.lower()}/run with spaces/attempt-002/execution.json"])
        except Exception as error:
            recorder.error(case_id, error)

    try:
        wrapper_text = (candidate / "scripts" / "advisor.ps1").read_text(encoding="utf-8-sig")
        forbidden = ("ANTHROPIC_API_KEY", "max-budget-usd", "contract_sha256", "reserved_budget_usd", "attempt-001")
        recorder.add("SV-SP-029", all(item not in wrapper_text for item in forbidden)
                     and "advisor_run.py" in wrapper_text and "--show-progress" in wrapper_text
                     and "& $Python @runnerArguments" in wrapper_text,
                     "The launcher delegates to Python and contains no duplicated auth, budget, evidence or retry policy.", [str((candidate / "scripts" / "advisor.ps1").relative_to(candidate))])
    except Exception as error:
        recorder.error("SV-SP-029", error)

    try:
        manifest = read_json(candidate / "artifact-manifest.json")
        files = manifest.get("files", {})
        actual_paths = sorted(str(path.relative_to(candidate)).replace("\\", "/") for path in candidate.rglob("*")
                              if path.is_file() and path.name != "artifact-manifest.json" and "__pycache__" not in path.parts)
        manifest_ok = sorted(files) == actual_paths and all(
            files[name] == sha256((candidate / name).read_bytes()) for name in actual_paths)
        docs = "\n".join((candidate / name).read_text(encoding="utf-8-sig") for name in
                         ("SKILL.md", "references/execution.md", "references/evaluation.md"))
        cases_text = (candidate / "evals" / "cases.jsonl").read_text(encoding="utf-8-sig")
        required_docs = ("--show-progress", "advisor.ps1", "advisor-execution-v2", "stream-json",
                         "PowerShell 5.1", "framework acceptance")
        recorder.add("SV-SP-030", manifest_ok and all(term in docs for term in required_docs)
                     and "stream" in cases_text.lower(),
                     "The manifest bound every package file and instructions/evaluation artifacts documented the delivered behavior and authority boundary.", ["artifact-manifest.json", "SKILL.md", "references/execution.md", "references/evaluation.md", "evals/cases.jsonl"])
    except Exception as error:
        recorder.error("SV-SP-030", error)

    expected_ids = [f"SV-SP-{number:03}" for number in range(1, 31)]
    observed_ids = [item["id"] for item in recorder.cases]
    missing = [case_id for case_id in expected_ids if case_id not in observed_ids]
    duplicates = sorted({case_id for case_id in observed_ids if observed_ids.count(case_id) > 1})
    passed = sum(item["status"] == "PASS" for item in recorder.cases)
    report = {
        "schema_version": "advisor-streaming-independent-cases-v1",
        "candidate": str(candidate),
        "legacy_candidate": str(legacy),
        "required_case_ids": expected_ids,
        "cases": sorted(recorder.cases, key=lambda item: item["id"]),
        "missing_case_ids": missing,
        "duplicate_case_ids": duplicates,
        "passing": passed,
        "total": 30,
        "pass_rate_percent": passed * 100.0 / 30,
    }
    write_json(args.output, report)
    print(json.dumps(report, ensure_ascii=True, allow_nan=False))
    return 0 if passed == 30 and not missing and not duplicates else 1


if __name__ == "__main__":
    raise SystemExit(main())
