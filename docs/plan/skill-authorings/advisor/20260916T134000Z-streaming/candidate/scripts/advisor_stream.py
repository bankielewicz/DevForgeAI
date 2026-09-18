"""Bounded streaming subprocess transport for the advisor helper.

This module captures exact stdout and stderr bytes while showing only a small,
allowlisted progress view.  It observes and cleans up the direct child process;
it does not claim process-tree or detached-descendant cleanup.
"""

import json
import math
import queue
import re
import subprocess
import sys
import threading
import time


CLEANUP_SECONDS = 5.0
HEARTBEAT_SECONDS = 5.0
READ_SIZE = 64 * 1024
ALLOWED_TOOLS = frozenset(("Read", "Grep", "Glob"))
SESSION_ID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.IGNORECASE,
)


def _reject_constant(value):
    raise ValueError("Nonfinite JSON value: " + value)


def _finite_float(value):
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("Nonfinite JSON number: " + value)
    return parsed


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def _load_event(line):
    try:
        value = json.loads(
            line,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError("Malformed JSONL event: " + str(error)) from error
    if not isinstance(value, dict):
        raise ValueError("JSONL events must be objects")
    event_type = value.get("type")
    if not isinstance(event_type, str) or not event_type.strip():
        raise ValueError("JSONL event requires a nonempty type")
    return value


def parse_stream(raw):
    """Return the one final result object from a strictly framed JSONL stream."""
    if not isinstance(raw, (bytes, bytearray)):
        raise ValueError("Stream must be bytes")
    try:
        text = bytes(raw).decode("utf-8-sig")
    except UnicodeError as error:
        raise ValueError("Stream is not valid UTF-8: " + str(error)) from error

    result = None
    for line in text.splitlines():
        if not line.strip():
            continue
        event = _load_event(line)
        if result is not None:
            if event["type"] == "result":
                raise ValueError("Stream contains multiple result events")
            raise ValueError("Stream contains an event after the result")
        if event["type"] == "result":
            result = event
    if result is None:
        raise ValueError("Stream is missing a result event")
    return result


def _emit(progress, started, message):
    try:
        progress.write(f"{time.monotonic() - started:6.1f}s  {message}\n")
        progress.flush()
    except (AttributeError, OSError, ValueError):
        # Progress is informational. Raw evidence collection remains authoritative.
        pass


class _ProgressView:
    def __init__(self, stream, started):
        self.stream = stream
        self.started = started
        self.buffer = bytearray()

    def feed(self, chunk, final=False):
        self.buffer.extend(chunk)
        while True:
            position = self.buffer.find(b"\n")
            if position < 0:
                break
            line = bytes(self.buffer[:position]).rstrip(b"\r")
            del self.buffer[:position + 1]
            self._line(line)
        if final and self.buffer:
            line = bytes(self.buffer).rstrip(b"\r")
            self.buffer.clear()
            self._line(line)

    def _line(self, raw):
        if not raw.strip():
            return
        try:
            event = _load_event(raw.decode("utf-8"))
        except (ValueError, UnicodeError):
            return
        event_type = event["type"]
        if event_type == "system" and event.get("subtype") == "init":
            session_id = event.get("session_id")
            if isinstance(session_id, str) and SESSION_ID.fullmatch(session_id):
                _emit(self.stream, self.started, "session " + session_id)
        elif event_type == "assistant":
            _emit(self.stream, self.started, "assistant activity")
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if isinstance(content, list):
                for item in content:
                    if not isinstance(item, dict) or item.get("type") != "tool_use":
                        continue
                    name = item.get("name")
                    if isinstance(name, str) and name in ALLOWED_TOOLS:
                        _emit(self.stream, self.started, "tool " + name)
        elif event_type == "result":
            _emit(self.stream, self.started, "final result received")


def _read_pipe(name, pipe, events):
    try:
        reader = getattr(pipe, "read1", None) or pipe.read
        while True:
            chunk = reader(READ_SIZE)
            if not chunk:
                break
            events.put((name, "data", chunk))
    except (OSError, ValueError) as error:
        events.put((name, "error", str(error)))
    finally:
        events.put((name, "eof", None))


def _consume(event, stdout, stderr, eof, errors, view):
    name, kind, value = event
    if kind == "data":
        (stdout if name == "stdout" else stderr).append(value)
        if name == "stdout":
            view.feed(value)
    elif kind == "error":
        errors.append(name + " read failed: " + value)
    else:
        eof.add(name)
        if name == "stdout":
            view.feed(b"", final=True)


def _wait_for_exit(process, deadline, errors):
    interrupted = False
    while process.poll() is None and time.monotonic() < deadline:
        try:
            process.wait(timeout=min(0.05, max(0.0, deadline - time.monotonic())))
        except subprocess.TimeoutExpired:
            continue
        except KeyboardInterrupt:
            interrupted = True
            errors.append("cleanup wait interrupted")
        except OSError as error:
            errors.append("direct child wait failed: " + str(error))
            break
    return interrupted


def _kill_child(process, deadline, errors):
    interrupted = False
    while process.poll() is None and time.monotonic() < deadline:
        try:
            process.kill()
            break
        except KeyboardInterrupt:
            interrupted = True
            errors.append("cleanup kill interrupted")
        except OSError as error:
            if process.poll() is None:
                errors.append("direct child kill failed: " + str(error))
            break
    return interrupted


def _cleanup(process, threads, events, stdout, stderr, eof, errors, view):
    """Stop and reap the direct child, then bound pipe-reader shutdown."""
    deadline = time.monotonic() + CLEANUP_SECONDS
    interrupted = False
    if process.poll() is None:
        interrupted |= _kill_child(process, deadline, errors)
        interrupted |= _wait_for_exit(process, deadline, errors)
        if process.poll() is None:
            errors.append("direct child did not exit within cleanup ceiling")

    while any(thread.is_alive() for thread in threads) and time.monotonic() < deadline:
        try:
            event = events.get(timeout=min(0.05, max(0.0, deadline - time.monotonic())))
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            interrupted = True
            errors.append("cleanup pipe drain interrupted")
            continue
        _consume(event, stdout, stderr, eof, errors, view)
    while time.monotonic() < deadline:
        try:
            _consume(events.get_nowait(), stdout, stderr, eof, errors, view)
        except queue.Empty:
            break
        except KeyboardInterrupt:
            interrupted = True
            errors.append("cleanup queue drain interrupted")

    child_exited = process.poll() is not None
    pipes_closed = not any(thread.is_alive() for thread in threads)
    if not pipes_closed:
        errors.append("pipe readers did not close within cleanup ceiling")
    if not events.empty():
        errors.append("captured stream queue was not fully drained within cleanup ceiling")
    return {"child_exited": child_exited, "pipes_closed": pipes_closed}, interrupted


def execute_stream(argv, cwd, timeout, env=None, progress=None):
    """Run one direct child with exact byte capture and bounded cleanup.

    The caller validates the returned JSONL separately with :func:`parse_stream`.
    Progress is written to ``progress`` (stderr by default) and never contains
    model text, tool arguments, paths, or terminal data from untrusted events.
    """
    progress = sys.stderr if progress is None else progress
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            env=env,
        )
    except OSError as error:
        return {
            "exit_code": None,
            "stdout": b"",
            "stderr": b"",
            "timed_out": False,
            "spawn_error": str(error),
            "cleanup": {"child_exited": False, "pipes_closed": True},
            "interrupted": False,
            "transport_error": None,
        }

    events = queue.Queue()
    stdout = []
    stderr = []
    eof = set()
    errors = []
    view = _ProgressView(progress, started)
    threads = [
        threading.Thread(target=_read_pipe, args=("stdout", process.stdout, events), daemon=True),
        threading.Thread(target=_read_pipe, args=("stderr", process.stderr, events), daemon=True),
    ]
    for thread in threads:
        thread.start()

    deadline = started + timeout
    heartbeat = started + HEARTBEAT_SECONDS
    timed_out = False
    interrupted = False
    try:
        while process.poll() is None or len(eof) < 2:
            current = time.monotonic()
            if current >= deadline:
                timed_out = True
                break
            wait_until = min(deadline, heartbeat, current + 0.05)
            try:
                event = events.get(timeout=max(0.0, wait_until - current))
            except queue.Empty:
                if time.monotonic() >= heartbeat:
                    _emit(progress, started, "waiting")
                    heartbeat += HEARTBEAT_SECONDS
                continue
            _consume(event, stdout, stderr, eof, errors, view)
    except KeyboardInterrupt:
        interrupted = True

    cleanup, cleanup_interrupted = _cleanup(process, threads, events, stdout, stderr, eof, errors, view)
    interrupted |= cleanup_interrupted
    for pipe in (process.stdout, process.stderr):
        if pipe is not None and cleanup["pipes_closed"]:
            try:
                pipe.close()
            except KeyboardInterrupt:
                interrupted = True
                errors.append("pipe close interrupted")
            except OSError as error:
                errors.append("pipe close failed: " + str(error))
    if not cleanup["child_exited"] or not cleanup["pipes_closed"]:
        errors.append("cleanup observations are incomplete")
    return {
        "exit_code": process.poll(),
        "stdout": b"".join(stdout),
        "stderr": b"".join(stderr),
        "timed_out": timed_out,
        "spawn_error": None,
        "cleanup": cleanup,
        "interrupted": interrupted,
        "transport_error": "; ".join(dict.fromkeys(errors)) or None,
    }


__all__ = ["execute_stream", "parse_stream"]
