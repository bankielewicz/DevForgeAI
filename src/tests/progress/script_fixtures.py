"""Fixtures shared by the tests of chain_state.py and history.py (SPEC-012 version 17, VER-50 to VER-54).

Everything is built in a temporary folder the test owns. Run states come from the evaluator itself, on logs the case
generator builds, so history.py reads what a run really writes. Every spawn uses -B, so no __pycache__ lands in the
plugin folder, which deploys.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_cases as mc  # noqa: E402

ROOT = mc.ROOT
PROGRESS = ROOT / "src/claude/DevForgeAI/progress"
# CHAIN_STATE_UNDER_TEST and HISTORY_UNDER_TEST point the tests at a modified copy, to check that they can fail (as
# test_prune.py's PRUNE_UNDER_TEST does).
CHAIN_STATE = Path(os.environ.get("CHAIN_STATE_UNDER_TEST") or PROGRESS / "chain_state.py")
HISTORY = Path(os.environ.get("HISTORY_UNDER_TEST") or PROGRESS / "history.py")
SCHEMAS = PROGRESS / "schemas"


def run_script(script, args, interpreter=(sys.executable, "-B"), cwd=None, env=None):
    """Run a script as its own process; the contract is exit codes, stdout and stderr."""
    return subprocess.run(list(interpreter) + [str(script)] + [str(a) for a in args], cwd=cwd or ROOT,
                          capture_output=True, text=True, env=env)


def run_script_bytes(script, args, interpreter=(sys.executable, "-B"), cwd=None, env=None):
    return subprocess.run(list(interpreter) + [str(script)] + [str(a) for a in args], cwd=cwd or ROOT,
                          capture_output=True, env=env)


def write(root, rel, content, mode="w"):
    """Write a file under root, creating its folders; content is text, or bytes with mode 'wb'."""
    path = Path(root) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "wb":
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


# ---- run states made by the evaluator ----------------------------------------------------------------------

def evaluate_log(log, interpreter=(sys.executable, "-B")):
    """The state.json text the evaluator writes for a log built in memory (a make_cases.Log or a list of lines)."""
    lines = log if isinstance(log, list) else log.lines()
    with tempfile.TemporaryDirectory() as tmp:
        events, out = Path(tmp) / "events.jsonl", Path(tmp) / "state.json"
        events.write_text("\n".join(lines) + "\n", encoding="utf-8")
        proc = subprocess.run(list(interpreter) + [mc.EVALUATE, "evaluate", "--manifests", mc.PLUGIN_MANIFESTS,
                                                   "--events", str(events), "--out", str(out)],
                              cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError(proc.stderr)
        return out.read_text(encoding="utf-8")


def spread(events, total):
    """Times for a log of `events` events that make its active time exactly `total` seconds (gaps under 30 minutes)."""
    gaps = events - 1
    base = total // gaps
    steps = [base] * (gaps - 1) + [total - base * (gaps - 1)]
    times, at = [0], 0
    for step in steps:
        at += step
        times.append(at)
    return times


def brainstorm_run(active, end="session-end"):
    """A brainstorm run that reaches every step and (with `end`) ends, its active time `active` seconds: step 5 was left
    open (not applicable), the rest done."""
    log = mc.Log("brainstorm", times=spread(8, active))
    mc.brn_start(log).write(mc.BRN_PATH, mc.brn(["open"] * 15)).bash(mc.VALIDATE).tick(6, 7).tick(8)
    if end:
        log.end(end)
    return log


def architecture_run_ending_idle():
    """An architecture run through the task list that passes over the conditional steps 5 and 7 and reaches the rest,
    then ends 'idle': every step is done or not applicable."""
    log = mc.arch_steps_to_six(mc.following("architecture"))
    log.worked(7).started(8).answer(step=8).done(8).started(9).write(mc.ARCH_PATH, mc.arch("create")).done(9)
    log.started(10).read(mc.ARCH_PATH).done(10).worked(11)
    return log.end("idle")


STATE_FILE = "state.json"


def put_run(root, name, text):
    """A run folder with a state.json under devforgeai/progress/runs/."""
    return write(root, "devforgeai/progress/runs/%s/%s" % (name, STATE_FILE), text)


def run_name(skill, n):
    return "20261002T1200%02dZ-%s-%08x" % (n % 60, skill, n)


# ---- the odometer ledger ---------------------------------------------------------------------------------

LEDGER = "devforgeai/progress/odometer"


def line(session, turn, source, input=1, output=1, cache_read=1, cache_write=1, time="2026-10-06T12:00:00Z"):
    """One ledger line (DM-04), as a dict."""
    return {"session": session, "turn": turn, "source": source, "input": input, "output": output,
            "cacheRead": cache_read, "cacheWrite": cache_write, "time": time}


def ledger(root, name, lines, trailing_newline=True):
    """A ledger file; lines are dicts (written as JSON) or text (written as given)."""
    text = "\n".join(l if isinstance(l, str) else json.dumps(l, sort_keys=True) for l in lines)
    return write(root, "%s/%s" % (LEDGER, name), text + ("\n" if trailing_newline and lines else ""))


# ---- snapshots (VER-53) ----------------------------------------------------------------------------------------

def snapshot(base):
    """{relative path: file content or the folder's listing} of everything under base, links as their targets' names."""
    base = Path(base)
    seen = {}
    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        here = Path(dirpath)
        seen[str(here.relative_to(base)) + "/"] = sorted(dirnames + filenames)
        for name in filenames:
            path = here / name
            rel = str(path.relative_to(base))
            seen[rel] = os.readlink(path) if path.is_symlink() else path.read_bytes() if os.access(path, os.R_OK) else None
    return seen
