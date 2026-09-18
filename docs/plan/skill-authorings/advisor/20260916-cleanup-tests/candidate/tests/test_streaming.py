"""Streaming transport and evidence tests use only synthetic local processes."""

import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1]
RUNNER_PATH = PACKAGE / "scripts" / "advisor_run.py"
STREAM_PATH = PACKAGE / "scripts" / "advisor_stream.py"

RUNNER_SPEC = importlib.util.spec_from_file_location("advisor_streaming_runner", RUNNER_PATH)
advisor = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(advisor)
STREAM_SPEC = importlib.util.spec_from_file_location("advisor_stream", STREAM_PATH)
streaming = importlib.util.module_from_spec(STREAM_SPEC)
STREAM_SPEC.loader.exec_module(streaming)


def response():
    return (
        "VERDICT: PROCEED\n\n"
        "ASK RESTATED:\nCheck the selected implementation.\n\n"
        "DO THIS:\n1. Continue the selected task.\n\n"
        "DO NOT:\n- Expand scope.\n\n"
        "CLAIM AUDIT:\n- selected behavior -> CONFIRMED (sample.txt:1)\n\n"
        "RISKS:\nnone\n\n"
        "COULD NOT VERIFY:\nnone\n\n"
        "FLIP CONDITIONS:\n- Changed evidence.\n"
    )


def result_event(**changes):
    event = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "result": response(),
        "total_cost_usd": 0.25,
    }
    event.update(changes)
    return event


def jsonl(*events):
    return b"".join(
        json.dumps(event, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("utf-8") + b"\n"
        for event in events
    )


def process(stdout, **changes):
    value = {
        "exit_code": 0,
        "stdout": stdout,
        "stderr": b"",
        "timed_out": False,
        "spawn_error": None,
        "interrupted": False,
        "transport_error": None,
        "cleanup": {"child_exited": True, "pipes_closed": True},
    }
    value.update(changes)
    return value


class StreamParserTests(unittest.TestCase):
    def test_unknown_nonfinal_events_are_allowed_and_final_result_is_returned(self):
        final = result_event(session_id="synthetic-session")
        raw = jsonl({"type": "system", "subtype": "init", "session_id": "synthetic-session"},
                    {"type": "future_event", "untrusted": {"text": "ignored"}}, final)
        self.assertEqual(streaming.parse_stream(raw), final)

    def test_malformed_missing_duplicate_and_nonterminal_result_are_rejected(self):
        bad_streams = {
            "empty": b"",
            "invalid-utf8": b"\xff\n",
            "malformed-json": b'{"type":"system"\n',
            "non-object": b"[]\n",
            "missing-result": jsonl({"type": "system"}),
            "duplicate-result": jsonl(result_event(), result_event()),
            "result-not-last": jsonl(result_event(), {"type": "system"}),
            "duplicate-key": b'{"type":"result","type":"result","subtype":"success","is_error":false,"result":"x"}\n',
            "nonfinite": b'{"type":"result","subtype":"success","is_error":false,"result":"x","total_cost_usd":NaN}\n',
            "overflow-nonfinite": b'{"type":"result","nested":{"value":1e999}}\n',
        }
        for name, raw in bad_streams.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                streaming.parse_stream(raw)


class StreamInterpretationTests(unittest.TestCase):
    def test_success_requires_valid_terminal_advice(self):
        final = result_event()
        outcome, text, envelope = advisor.interpret_stream(process(jsonl({"type": "system"}, final)), cap="1.00")
        self.assertEqual(outcome["execution_status"], "SUCCEEDED")
        self.assertEqual(outcome["response_status"], "VALID")
        self.assertEqual(outcome["verdict"], "PROCEED")
        self.assertEqual(outcome["reported_cost_usd"], 0.25)
        self.assertFalse(outcome["budget_cap_exceeded"])
        self.assertEqual(text, response())
        self.assertEqual(envelope, final)

    def test_failed_process_retains_finite_cost_and_never_exposes_advice(self):
        final = result_event(subtype="error_max_budget_usd", is_error=True,
                             result="partial untrusted text", total_cost_usd=1.015353)
        outcome, text, envelope = advisor.interpret_stream(
            process(jsonl(final), exit_code=1), cap="1.00")
        self.assertEqual(outcome["execution_status"], "FAILED")
        self.assertEqual(outcome["response_status"], "NOT_EVALUATED")
        self.assertIsNone(outcome["verdict"])
        self.assertEqual(outcome["reported_cost_usd"], 1.015353)
        self.assertTrue(outcome["budget_cap_exceeded"])
        self.assertIsNone(text)
        self.assertEqual(envelope, final)

    def test_timeout_interruption_transport_and_cleanup_failure_never_yield_advice(self):
        cases = (
            process(jsonl(result_event()), exit_code=None, timed_out=True),
            process(jsonl(result_event()), exit_code=None, interrupted=True),
            process(jsonl(result_event()), exit_code=None, transport_error="reader failed"),
            process(jsonl(result_event()), cleanup={"child_exited": False, "pipes_closed": True}),
            process(jsonl(result_event()), cleanup={"child_exited": True, "pipes_closed": False}),
        )
        for value in cases:
            with self.subTest(value=value):
                outcome, text, _ = advisor.interpret_stream(value, cap="1.00")
                self.assertNotEqual(outcome["response_status"], "VALID")
                self.assertIsNone(outcome["verdict"])
                self.assertIsNone(text)

    def test_malformed_stream_is_invalid_even_when_process_exit_is_zero(self):
        outcome, text, envelope = advisor.interpret_stream(process(b'{"type":"result"\n'), cap="1.00")
        self.assertEqual(outcome["execution_status"], "SUCCEEDED")
        self.assertEqual(outcome["response_status"], "INVALID")
        self.assertIsNone(outcome["verdict"])
        self.assertIsNone(text)
        self.assertIsNone(envelope)

    def test_invalid_cost_types_and_values_are_rejected(self):
        for cost in (True, -0.01, "0.25"):
            with self.subTest(cost=cost):
                outcome, text, envelope = advisor.interpret_stream(
                    process(jsonl(result_event(total_cost_usd=cost))), cap="1.00")
                self.assertEqual(outcome["response_status"], "INVALID")
                self.assertIsNone(outcome["reported_cost_usd"])
                self.assertIsNone(text)
                self.assertEqual(envelope["total_cost_usd"], cost)

    def test_noncompleted_terminal_reason_is_invalid(self):
        outcome, text, envelope = advisor.interpret_stream(
            process(jsonl(result_event(terminal_reason="budget_exhausted"))), cap="1.00")
        self.assertEqual(outcome["execution_status"], "SUCCEEDED")
        self.assertEqual(outcome["response_status"], "INVALID")
        self.assertIsNone(outcome["verdict"])
        self.assertIsNone(text)
        self.assertEqual(envelope["terminal_reason"], "budget_exhausted")


class RetryProgressTests(unittest.TestCase):
    def display(self, event):
        progress = io.StringIO()
        streaming._ProgressView(progress, time.monotonic()).feed(jsonl(event))
        return progress.getvalue()

    def test_retry_counts_and_numeric_status_are_visible(self):
        display = self.display({"type": "system", "subtype": "api_retry",
                                "attempt": 1, "max_retries": 10, "error_status": 401})
        self.assertRegex(display, r"^\s*\d+\.\ds  retry 1/10 status 401\n$")

    def test_missing_or_noninteger_status_keeps_counts_without_untrusted_text(self):
        event = {"type": "system", "subtype": "api_retry", "attempt": 2, "max_retries": 10,
                 "error": "PRIVATE ERROR\u001b[31m", "path": "C:/private.txt"}
        self.assertRegex(self.display(event), r"retry 2/10\n$")
        for status in (None, True, False, "401\u001b[31m", 401.0, [401], {"secret": "value"}):
            with self.subTest(status=status):
                display = self.display(dict(event, error_status=status))
                self.assertRegex(display, r"^\s*\d+\.\ds  retry 2/10\n$")

    def test_noninteger_or_missing_counts_produce_no_progress(self):
        event = {"type": "system", "subtype": "api_retry", "attempt": 1,
                 "max_retries": 10, "error_status": 503}
        for field in ("attempt", "max_retries"):
            missing = dict(event)
            del missing[field]
            with self.subTest(field=field, missing=True):
                self.assertEqual(self.display(missing), "")
            for value in (None, True, False, "1\u001b[31m", 1.0, [1], {"value": 1}):
                with self.subTest(field=field, value=value):
                    self.assertEqual(self.display(dict(event, **{field: value})), "")

    def test_only_system_api_retry_events_emit_retry_progress(self):
        for event_type, subtype in (("system", "other"), ("api_retry", "api_retry"),
                                    ("user", "api_retry")):
            with self.subTest(event_type=event_type, subtype=subtype):
                self.assertEqual(self.display({"type": event_type, "subtype": subtype,
                                               "attempt": 1, "max_retries": 10}), "")

    def test_chunked_retry_event_is_emitted_once_when_complete(self):
        progress = io.StringIO()
        view = streaming._ProgressView(progress, time.monotonic())
        raw = jsonl({"type": "system", "subtype": "api_retry", "attempt": 3,
                     "max_retries": 10, "error_status": None})
        for byte in raw[:-1]:
            view.feed(bytes([byte]))
        self.assertEqual(progress.getvalue(), "")
        view.feed(raw[-1:])
        view.feed(b"", final=True)
        self.assertRegex(progress.getvalue(), r"^\s*\d+\.\ds  retry 3/10\n$")

    def test_retry_without_final_newline_is_emitted_once_at_eof(self):
        progress = io.StringIO()
        view = streaming._ProgressView(progress, time.monotonic())
        raw = jsonl({"type": "system", "subtype": "api_retry", "attempt": 4,
                     "max_retries": 10, "error_status": 429}).rstrip(b"\n")
        view.feed(raw)
        self.assertEqual(progress.getvalue(), "")
        view.feed(b"", final=True)
        view.feed(b"", final=True)
        self.assertRegex(progress.getvalue(), r"^\s*\d+\.\ds  retry 4/10 status 429\n$")

    def test_blank_and_malformed_events_do_not_hide_next_retry_or_leak_text(self):
        progress = io.StringIO()
        view = streaming._ProgressView(progress, time.monotonic())
        view.feed(b'\n  \r\n{"type":"system","subtype":"api_retry","error":"PRIVATE"\n\xff\n')
        self.assertEqual(progress.getvalue(), "")
        view.feed(jsonl({"type": "system", "subtype": "api_retry", "attempt": 5,
                         "max_retries": 10, "error_status": None}))
        self.assertRegex(progress.getvalue(), r"^\s*\d+\.\ds  retry 5/10\n$")


class StreamProcessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_real_subprocess_preserves_raw_streams_and_cleanup_observations(self):
        stdout = jsonl({"type": "system", "session_id": "synthetic", "payload": "x" * 131072}, result_event())
        stderr = b"e" * 131072
        final = result_event()
        code = (
            "import json,sys; "
            "j=lambda v:(json.dumps(v,separators=(',',':'))+'\\n').encode(); "
            f"sys.stdout.buffer.write(j({{'type':'system','session_id':'synthetic','payload':'x'*131072}})+j({final!r})); "
            "sys.stdout.buffer.flush(); sys.stderr.buffer.write(b'e'*131072); sys.stderr.buffer.flush()"
        )
        observed = io.StringIO()
        value = streaming.execute_stream(
            [sys.executable, "-c", code], self.root, 10, progress=observed)
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["stdout"], stdout)
        self.assertEqual(value["stderr"], stderr)
        self.assertFalse(value["timed_out"])
        self.assertFalse(value["interrupted"])
        self.assertIsNone(value["transport_error"])
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        progress = observed.getvalue()
        self.assertIn("final result received", progress)
        self.assertNotIn(response(), progress)
        self.assertNotIn("payload", progress)

    def test_real_retry_stream_preserves_evidence_and_failed_result(self):
        final = result_event(is_error=True, result="PRIVATE FAILURE")
        raw = jsonl(
            {"type": "system", "subtype": "api_retry", "attempt": 1,
             "max_retries": 10, "error_status": None, "error": "PRIVATE ERROR\u001b[31m"},
            {"type": "system", "subtype": "api_retry", "attempt": 2,
             "max_retries": 10, "error_status": 503}, final)
        code = (f"import sys; sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush(); "
                "sys.stderr.buffer.write(b'PRIVATE STDERR'); raise SystemExit(1)")
        progress = io.StringIO()
        value = streaming.execute_stream([sys.executable, "-c", code], self.root, 5,
                                         progress=progress)
        self.assertEqual(value["stdout"], raw)
        self.assertEqual(value["stderr"], b"PRIVATE STDERR")
        self.assertEqual(value["exit_code"], 1)
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        self.assertIsNone(value["transport_error"])
        self.assertEqual(streaming.parse_stream(value["stdout"]), final)
        display = progress.getvalue()
        self.assertRegex(display, r"retry 1/10\n")
        self.assertRegex(display, r"retry 2/10 status 503\n")
        self.assertIn("final result received", display)
        for forbidden in ("PRIVATE", "\x1b", "status None"):
            self.assertNotIn(forbidden, display)
        outcome, advice, _ = advisor.interpret_stream(value, cap="1.00")
        self.assertEqual(outcome["execution_status"], "FAILED")
        self.assertEqual(outcome["response_status"], "NOT_EVALUATED")
        self.assertIsNone(advice)

    def test_real_timeout_is_bounded_and_records_cleanup(self):
        started = time.monotonic()
        value = streaming.execute_stream(
            [sys.executable, "-c", "import time; time.sleep(30)"], self.root, 0.05)
        self.assertTrue(value["timed_out"])
        self.assertTrue(value["cleanup"]["child_exited"])
        self.assertTrue(value["cleanup"]["pipes_closed"])
        self.assertLess(time.monotonic() - started, 6.0)

    def test_progress_allowlist_handles_untrusted_shapes_without_disclosure(self):
        session = "a6642f50-4f69-4efd-8bdb-8811861debb7"
        raw = jsonl(
            {"type": "system", "subtype": "init", "session_id": session, "secret": "DO-NOT-PRINT"},
            {"type": "assistant", "message": {"content": [
                {"type": "text", "text": "MODEL SECRET\u001b[31m"},
                {"type": "tool_use", "name": "Read", "input": {"file_path": "C:/secret.txt"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "credential"}},
                {"type": "tool_use", "name": ["Read"], "input": {"file_path": "C:/also-secret.txt"}},
            ]}},
            {"type": "result", "subtype": "success", "result": "PRIVATE RESULT"},
        )
        progress = io.StringIO()
        code = f"import sys; sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush()"
        value = streaming.execute_stream([sys.executable, "-c", code], self.root, 10, progress=progress)
        self.assertEqual(value["stdout"], raw)
        display = progress.getvalue()
        self.assertIn(session, display)
        self.assertIn("tool Read", display)
        self.assertIn("final result received", display)
        for forbidden in ("DO-NOT-PRINT", "MODEL SECRET", "secret.txt", "also-secret", "Bash",
                          "credential", "PRIVATE RESULT", "\x1b"):
            self.assertNotIn(forbidden, display)

    def test_spawn_failure_is_explicit_and_has_no_raw_output(self):
        missing = self.root / "missing-executable.exe"
        value = streaming.execute_stream([str(missing)], self.root, 1, progress=io.StringIO())
        self.assertIsNone(value["exit_code"])
        self.assertEqual(value["stdout"], b"")
        self.assertEqual(value["stderr"], b"")
        self.assertIsInstance(value["spawn_error"], str)
        self.assertFalse(value["timed_out"])
        self.assertEqual(value["cleanup"], {"child_exited": False, "pipes_closed": True})

    def test_heartbeat_reports_waiting_without_child_content(self):
        raw = jsonl(result_event())
        code = f"import sys,time; time.sleep(0.08); sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush()"
        progress = io.StringIO()
        with patch.object(streaming, "HEARTBEAT_SECONDS", 0.02):
            value = streaming.execute_stream([sys.executable, "-c", code], self.root, 5, progress=progress)
        self.assertEqual(value["exit_code"], 0)
        self.assertIn("waiting", progress.getvalue())
        self.assertNotIn(response(), progress.getvalue())

    def test_nonzero_child_retains_stream_and_complete_cleanup(self):
        raw = jsonl(result_event(subtype="error", is_error=True, result="partial"))
        code = f"import sys; sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush(); raise SystemExit(7)"
        value = streaming.execute_stream([sys.executable, "-c", code], self.root, 5, progress=io.StringIO())
        self.assertEqual(value["exit_code"], 7)
        self.assertEqual(value["stdout"], raw)
        self.assertIsNone(value["transport_error"])
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})

    def test_keyboard_interrupt_stops_and_reaps_actual_child(self):
        real_queue = streaming.queue.Queue

        class InterruptOnceQueue:
            def __init__(self):
                self.inner = real_queue()
                self.pending_interrupt = True

            def put(self, value):
                return self.inner.put(value)

            def get(self, *args, **kwargs):
                if self.pending_interrupt:
                    self.pending_interrupt = False
                    raise KeyboardInterrupt()
                return self.inner.get(*args, **kwargs)

            def get_nowait(self):
                return self.inner.get_nowait()

            def empty(self):
                return self.inner.empty()

        started = time.monotonic()
        with patch.object(streaming.queue, "Queue", InterruptOnceQueue):
            value = streaming.execute_stream(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                self.root, 10, progress=io.StringIO())
        self.assertTrue(value["interrupted"])
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        self.assertLess(time.monotonic() - started, 6.0)

    def test_repeated_interrupt_during_kill_remains_bounded(self):
        real_queue = streaming.queue.Queue
        real_popen = streaming.subprocess.Popen
        holder = {}

        class InterruptOnceQueue:
            def __init__(self):
                self.inner = real_queue()
                self.pending_interrupt = True

            def put(self, value):
                return self.inner.put(value)

            def get(self, *args, **kwargs):
                if self.pending_interrupt:
                    self.pending_interrupt = False
                    raise KeyboardInterrupt()
                return self.inner.get(*args, **kwargs)

            def get_nowait(self):
                return self.inner.get_nowait()

            def empty(self):
                return self.inner.empty()

        class KillInterruptProxy:
            def __init__(self, inner):
                self.inner = inner
                self.stdout = inner.stdout
                self.stderr = inner.stderr
                self.kill_calls = 0

            def poll(self):
                return self.inner.poll()

            def kill(self):
                self.kill_calls += 1
                if self.kill_calls == 1:
                    raise KeyboardInterrupt()
                return self.inner.kill()

            def wait(self, timeout=None):
                return self.inner.wait(timeout=timeout)

        def factory(*args, **kwargs):
            holder["proxy"] = KillInterruptProxy(real_popen(*args, **kwargs))
            return holder["proxy"]

        started = time.monotonic()
        with patch.object(streaming.queue, "Queue", InterruptOnceQueue), \
                patch.object(streaming.subprocess, "Popen", factory):
            value = streaming.execute_stream(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                self.root, 10, progress=io.StringIO())
        self.assertTrue(value["interrupted"])
        self.assertGreaterEqual(holder["proxy"].kill_calls, 2)
        self.assertTrue(value["cleanup"]["child_exited"])
        self.assertIn("cleanup kill interrupted", value["transport_error"])
        self.assertLess(time.monotonic() - started, 6.0)

    def test_pipe_read_failure_is_retained_as_transport_error(self):
        original = streaming._read_pipe

        def faulty_reader(name, pipe, events):
            if name == "stdout":
                events.put((name, "error", "synthetic read fault"))
                events.put((name, "eof", None))
            else:
                original(name, pipe, events)

        with patch.object(streaming, "_read_pipe", faulty_reader):
            value = streaming.execute_stream(
                [sys.executable, "-c", "pass"], self.root, 5, progress=io.StringIO())
        self.assertEqual(value["exit_code"], 0)
        self.assertIn("stdout read failed: synthetic read fault", value["transport_error"])
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})

    def test_wait_failure_is_retained_after_actual_child_stop(self):
        real_popen = streaming.subprocess.Popen
        holder = {}

        class WaitFaultProxy:
            def __init__(self, inner):
                self.inner = inner
                self.stdout = inner.stdout
                self.stderr = inner.stderr
                self.force_pending = True

            def poll(self):
                return None if self.force_pending else self.inner.poll()

            def kill(self):
                return self.inner.kill()

            def wait(self, timeout=None):
                self.force_pending = False
                raise OSError("synthetic wait fault")

        def factory(*args, **kwargs):
            holder["proxy"] = WaitFaultProxy(real_popen(*args, **kwargs))
            return holder["proxy"]

        try:
            with patch.object(streaming.subprocess, "Popen", factory):
                value = streaming.execute_stream(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    self.root, 0.02, progress=io.StringIO())
        finally:
            inner = holder.get("proxy").inner if holder.get("proxy") else None
            if inner is not None and inner.poll() is None:
                inner.kill()
                inner.wait()
            if inner is not None:
                inner.stdout.close()
                inner.stderr.close()
        self.assertIn("direct child wait failed: synthetic wait fault", value["transport_error"])
        self.assertFalse(value["cleanup"]["child_exited"])
        self.assertIn("direct child did not exit", value["transport_error"])

    def test_kill_failure_is_bounded_and_reports_incomplete_cleanup(self):
        real_popen = streaming.subprocess.Popen
        holder = {}

        class KillFaultProxy:
            def __init__(self, inner):
                self.inner = inner
                self.stdout = inner.stdout
                self.stderr = inner.stderr
                self.faulting = True

            def poll(self):
                return None if self.faulting else self.inner.poll()

            def kill(self):
                raise OSError("synthetic kill fault")

            def wait(self, timeout=None):
                return self.inner.wait(timeout=timeout)

        def factory(*args, **kwargs):
            holder["proxy"] = KillFaultProxy(real_popen(*args, **kwargs))
            return holder["proxy"]

        started = time.monotonic()
        try:
            with patch.object(streaming.subprocess, "Popen", factory):
                value = streaming.execute_stream(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    self.root, 0.02, progress=io.StringIO())
        finally:
            proxy = holder.get("proxy")
            if proxy is not None:
                proxy.faulting = False
                if proxy.inner.poll() is None:
                    proxy.inner.kill()
                    proxy.inner.wait()
                proxy.inner.stdout.close()
                proxy.inner.stderr.close()
        self.assertFalse(value["cleanup"]["child_exited"])
        self.assertIn("direct child kill failed: synthetic kill fault", value["transport_error"])
        self.assertIn("cleanup observations are incomplete", value["transport_error"])
        self.assertLess(time.monotonic() - started, 6.0)

    def test_continuously_filled_queue_still_obeys_cleanup_ceiling(self):
        original = streaming._read_pipe

        def flooding_reader(name, pipe, events):
            if name != "stdout":
                return original(name, pipe, events)
            deadline = time.monotonic() + streaming.CLEANUP_SECONDS + 0.2
            while time.monotonic() < deadline:
                events.put((name, "data", b"{}\n"))
                time.sleep(0.001)
            events.put((name, "eof", None))
            pipe.close()

        started = time.monotonic()
        with patch.object(streaming, "_read_pipe", flooding_reader):
            value = streaming.execute_stream(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                self.root, 0.02, progress=io.StringIO())
        elapsed = time.monotonic() - started
        self.assertFalse(value["cleanup"]["pipes_closed"])
        self.assertIn("pipe readers did not close", value["transport_error"])
        self.assertLess(elapsed, streaming.CLEANUP_SECONDS + 0.75)
        time.sleep(0.25)

    def test_progress_sink_write_failure_does_not_change_raw_evidence(self):
        class BrokenProgress:
            def write(self, value):
                raise OSError("synthetic progress sink fault")

            def flush(self):
                raise OSError("synthetic progress sink fault")

        raw = jsonl(result_event())
        code = f"import sys; sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush()"
        value = streaming.execute_stream(
            [sys.executable, "-c", code], self.root, 5, progress=BrokenProgress())
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["stdout"], raw)
        self.assertIsNone(value["transport_error"])


class CommandAndPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.request = {
            "claude_path": str(self.root / "claude.exe"),
            "model": "opus",
            "effort": "high",
            "contract_path": str(self.root / "contract.md"),
        }

    def test_stream_command_changes_only_transport_flags(self):
        attempt = self.root / "attempt-001"
        quiet = advisor.build_command(self.request, attempt, "1.00")
        streamed = advisor.build_command(self.request, attempt, "1.00", stream=True)
        self.assertEqual(quiet[quiet.index("--output-format") + 1], "json")
        self.assertNotIn("--verbose", quiet)
        self.assertEqual(streamed[streamed.index("--output-format") + 1], "stream-json")
        self.assertIn("--verbose", streamed)
        self.assertEqual(streamed.count("--output-format"), 1)
        self.assertEqual([x for x in quiet if x not in ("json",)],
                         [x for x in streamed if x not in ("stream-json", "--verbose")])

    def test_preflight_retains_help_for_streaming_capability_decision(self):
        def execute(argv, cwd, timeout, env=None):
            text = "2.1.273" if "--version" in argv else " ".join(
                flag for flag in advisor.REQUIRED_FLAGS if flag != "--verbose") + " --append-system-prompt-file"
            return {"exit_code": 0, "stdout": text.encode(), "stderr": b"",
                    "timed_out": False, "spawn_error": None}

        profile = advisor.preflight(sys.executable, self.root, execute=execute)
        self.assertNotIn("--verbose", profile["help"])


class StreamingEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.contract = self.root / "contract.md"
        self.contract.write_text("Review independently.", encoding="utf-8")
        self.briefing = self.root / "briefing.md"
        self.briefing.write_text("\n\n".join(
            f"## {label}\nSynthetic evidence."
            for label in advisor.BRIEFING_SECTIONS), encoding="utf-8")
        self.request = {
            "schema": "advisor-request-v1",
            "ask": "Check scope",
            "repo_root": str(self.root),
            "contract_path": str(self.contract),
            "claude_path": sys.executable,
            "contract_sha256": hashlib.sha256(self.contract.read_bytes()).hexdigest(),
        }
        self.run_dir = self.root / "run"
        self.quiet_calls = []
        self.stream_calls = []

    def quiet(self, argv, cwd, timeout, env=None):
        self.quiet_calls.append(argv)
        if "--help" in argv:
            text = " ".join(advisor.REQUIRED_FLAGS) + " --append-system-prompt-file --verbose stream-json"
        elif "--version" in argv:
            text = "2.1.273"
        else:
            text = json.dumps(result_event())
        return {"exit_code": 0, "stdout": text.encode(), "stderr": b"",
                "timed_out": False, "spawn_error": None}

    def streamed(self, argv, cwd, timeout, env=None, progress=None):
        self.stream_calls.append(argv)
        return process(jsonl({"type": "system", "session_id": "synthetic"}, result_event()))

    def review(self, show_progress, reason="initial"):
        return advisor.run_review(
            self.request, self.run_dir, self.briefing, reason=reason,
            execute=self.quiet, show_progress=show_progress, stream_execute=self.streamed)

    def test_v1_history_allows_v2_followup_and_preserves_old_bytes(self):
        first = self.review(False)
        self.assertEqual(first["schema"], "advisor-execution-v1")
        old = {path: path.read_bytes() for path in (self.run_dir / "attempt-001").rglob("*") if path.is_file()}
        second = self.review(True, reason="reconcile")
        self.assertEqual(second["schema"], "advisor-execution-v2")
        self.assertEqual(len(self.stream_calls), 1)
        for path, content in old.items():
            self.assertEqual(path.read_bytes(), content)
        attempt = self.run_dir / "attempt-002"
        self.assertEqual(json.loads((attempt / "result.json").read_text(encoding="utf-8"))["type"], "result")
        self.assertEqual((attempt / "response.md").read_text(encoding="utf-8"), response())

    def test_v2_history_allows_quiet_v1_followup(self):
        first = self.review(True)
        self.assertEqual(first["schema"], "advisor-execution-v2")
        second = self.review(False, reason="citation")
        self.assertEqual(second["schema"], "advisor-execution-v1")
        self.assertEqual(len(self.stream_calls), 1)
        self.assertEqual(sum("--print" in call for call in self.quiet_calls), 1)

    def test_streaming_preflight_rejects_missing_stream_capabilities_before_attempt(self):
        def incomplete(argv, cwd, timeout, env=None):
            if "--help" in argv:
                text = " ".join(advisor.REQUIRED_FLAGS) + " --append-system-prompt-file"
            else:
                text = "2.1.273"
            return {"exit_code": 0, "stdout": text.encode(), "stderr": b"",
                    "timed_out": False, "spawn_error": None}

        with self.assertRaisesRegex(ValueError, "streaming profile"):
            advisor.run_review(
                self.request, self.run_dir, self.briefing, execute=incomplete,
                show_progress=True, stream_execute=self.streamed)
        self.assertEqual(self.stream_calls, [])
        self.assertFalse((self.run_dir / "attempt-001").exists())

    def test_stream_evidence_forgery_blocks_followup_without_review_invocation(self):
        variants = ("stdout.txt", "result.json", "result-missing", "started.json", "preflight.json",
                    "execution.json", "transport-extra")
        for index, name in enumerate(variants):
            with self.subTest(name=name):
                run_dir = self.root / f"run-{index}"
                self.run_dir = run_dir
                self.review(True)
                path = run_dir / "attempt-001" / ("execution.json" if name in ("execution.json", "transport-extra") else name)
                if name == "execution.json":
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["transport"]["cleanup"] = {"child_exited": False, "pipes_closed": True}
                    path.write_text(json.dumps(value), encoding="utf-8")
                elif name == "transport-extra":
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["transport"]["unexpected"] = True
                    path.write_text(json.dumps(value), encoding="utf-8")
                elif name == "result-missing":
                    (run_dir / "attempt-001" / "result.json").unlink()
                else:
                    path.write_bytes(path.read_bytes() + b"forged")
                before = len(self.stream_calls) + sum("--print" in call for call in self.quiet_calls)
                with self.assertRaisesRegex(ValueError, "prior"):
                    self.review(False, reason="retry")
                after = len(self.stream_calls) + sum("--print" in call for call in self.quiet_calls)
                self.assertEqual(after, before)

    def test_uncertain_cleanup_history_blocks_another_attempt(self):
        def uncertain(argv, cwd, timeout, env=None, progress=None):
            self.stream_calls.append(argv)
            return process(
                jsonl({"type": "system"}, result_event()),
                cleanup={"child_exited": False, "pipes_closed": True},
                transport_error="cleanup observations are incomplete",
            )

        first = advisor.run_review(
            self.request, self.run_dir, self.briefing, execute=self.quiet,
            show_progress=True, stream_execute=uncertain)
        self.assertEqual(first["execution_status"], "FAILED")
        before = len(self.stream_calls) + sum("--print" in call for call in self.quiet_calls)
        with self.assertRaisesRegex(ValueError, "Incomplete|uncertain|cleanup"):
            self.review(False, reason="retry")
        after = len(self.stream_calls) + sum("--print" in call for call in self.quiet_calls)
        self.assertEqual(after, before)


class CommandLinePresentationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.request = self.root / "request.json"
        self.request.write_text("{}", encoding="utf-8")
        self.briefing = self.root / "briefing.md"
        self.briefing.write_text("synthetic", encoding="utf-8")

    def invoke(self, receipt):
        stdout, stderr = io.StringIO(), io.StringIO()
        argv = ["run", "--request", str(self.request), "--run-dir", str(self.root / "run"),
                "--briefing", str(self.briefing), "--show-progress"]
        with patch.object(advisor, "run_review", return_value=receipt), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = advisor.main(argv)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_show_progress_keeps_final_json_on_stdout_and_summary_on_stderr(self):
        receipt = {"execution_status": "SUCCEEDED", "response_status": "VALID", "verdict": "PROCEED",
                   "budget_cap_exceeded": False}
        exit_code, stdout, stderr = self.invoke(receipt)
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout), receipt)
        self.assertNotIn("Advisor:", stdout)
        self.assertIn("execution=SUCCEEDED response=VALID verdict=PROCEED", stderr)

    def test_show_progress_warns_when_failed_envelope_exceeds_cli_cap(self):
        receipt = {"execution_status": "FAILED", "response_status": "NOT_EVALUATED", "verdict": None,
                   "budget_cap_exceeded": True, "reported_cost_usd": 1.015353}
        exit_code, stdout, stderr = self.invoke(receipt)
        self.assertEqual(exit_code, 1)
        self.assertEqual(json.loads(stdout), receipt)
        self.assertIn("verdict=none", stderr)
        self.assertIn("reported cost exceeded", stderr)


if __name__ == "__main__":
    unittest.main()
