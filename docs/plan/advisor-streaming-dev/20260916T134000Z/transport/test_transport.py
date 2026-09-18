"""Requirement tests for the advisor streaming transport (AP-02/03/04/07)."""

import io
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / "docs/plan/skill-authorings/advisor/20260916T134000Z-streaming/candidate/scripts"
sys.path.insert(0, str(SCRIPTS))

import advisor_stream  # noqa: E402


def json_line(value):
    return json.dumps(value, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


class ParseStreamTests(unittest.TestCase):
    def test_returns_the_single_last_result_envelope(self):
        result = {"type": "result", "subtype": "success", "is_error": False, "result": "answer"}
        raw = json_line({"type": "system", "subtype": "init"}) + json_line(result)
        self.assertEqual(result, advisor_stream.parse_stream(raw))

    def test_accepts_utf8_bom_only_at_stream_start(self):
        result = {"type": "result", "subtype": "failed", "is_error": True}
        self.assertEqual(result, advisor_stream.parse_stream(b"\xef\xbb\xbf" + json_line(result)))

    def test_rejects_invalid_stream_framing(self):
        cases = {
            "malformed": b'{"type":"system"}\n{broken\n',
            "non_object": b'[]\n',
            "blank_type": b'{"type":""}\n',
            "missing_result": b'{"type":"system"}\n',
            "duplicate_result": b'{"type":"result"}\n{"type":"result"}\n',
            "event_after_result": b'{"type":"result"}\n{"type":"system"}\n',
            "duplicate_key": b'{"type":"result","type":"result"}\n',
            "nonfinite": b'{"type":"result","total_cost_usd":NaN}\n',
            "overflow_nonfinite": b'{"type":"result","nested":{"value":1e999}}\n',
            "bom_after_start": b'{"type":"system"}\n\xef\xbb\xbf{"type":"result"}\n',
        }
        for label, raw in cases.items():
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    advisor_stream.parse_stream(raw)


class ExecuteStreamTests(unittest.TestCase):
    def run_child(self, source, timeout=3, progress=None):
        return advisor_stream.execute_stream(
            [sys.executable, "-B", "-X", "utf8", "-c", source],
            str(ROOT), timeout, env=None, progress=progress,
        )

    def test_concurrently_drains_and_retains_exact_raw_bytes(self):
        stdout = json_line({"type": "system", "payload": "x" * 131072}) + json_line({"type": "result"})
        stderr = b"e" * 131072
        source = (
            "import json,sys;"
            "j=lambda v:(json.dumps(v,separators=(',',':'))+'\\n').encode();"
            "sys.stdout.buffer.write(j({'type':'system','payload':'x'*131072})+j({'type':'result'}));"
            "sys.stdout.buffer.flush();sys.stderr.buffer.write(b'e'*131072);sys.stderr.buffer.flush()"
        )
        observed = self.run_child(source, progress=io.StringIO())
        self.assertEqual(0, observed["exit_code"])
        self.assertEqual(stdout, observed["stdout"])
        self.assertEqual(stderr, observed["stderr"])
        self.assertFalse(observed["timed_out"])
        self.assertFalse(observed["interrupted"])
        self.assertIsNone(observed["spawn_error"])
        self.assertIsNone(observed["transport_error"])
        self.assertEqual({"child_exited": True, "pipes_closed": True}, observed["cleanup"])

    def test_progress_discloses_only_allowlisted_metadata(self):
        session = "a6642f50-4f69-4efd-8bdb-8811861debb7"
        events = (
            json_line({"type": "system", "subtype": "init", "session_id": session,
                       "secret": "DO-NOT-PRINT"})
            + json_line({"type": "assistant", "message": {"content": [
                {"type": "text", "text": "MODEL SECRET\\x1b[31m"},
                {"type": "tool_use", "name": "Read", "input": {"file_path": "C:/secret.txt"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "credential"}},
                {"type": "tool_use", "name": ["Read"], "input": {"file_path": "C:/also-secret.txt"}},
            ]}})
            + json_line({"type": "result", "subtype": "success", "result": "PRIVATE RESULT"})
        )
        progress = io.StringIO()
        observed = self.run_child(
            "import sys;sys.stdout.buffer.write(" + repr(events) + ");sys.stdout.buffer.flush()",
            progress=progress,
        )
        display = progress.getvalue()
        self.assertEqual(events, observed["stdout"])
        self.assertIn(session, display)
        self.assertIn("Read", display)
        self.assertIn("assistant activity", display)
        self.assertIn("final result received", display)
        for forbidden in ("DO-NOT-PRINT", "MODEL SECRET", "secret.txt", "also-secret", "Bash", "credential", "PRIVATE RESULT", "\x1b"):
            self.assertNotIn(forbidden, display)
        self.assertNotIn("success", display.lower())

    def test_timeout_covers_process_exit_and_bounded_cleanup(self):
        started = time.monotonic()
        observed = self.run_child("import time;time.sleep(30)", timeout=0.15, progress=io.StringIO())
        elapsed = time.monotonic() - started
        self.assertTrue(observed["timed_out"])
        self.assertIsNone(observed["exit_code"] if not observed["cleanup"]["child_exited"] else None)
        self.assertLess(elapsed, 5.75)
        self.assertEqual(observed["cleanup"]["child_exited"], observed["exit_code"] is not None)
        self.assertTrue(observed["cleanup"]["pipes_closed"])

    def test_nonzero_child_is_transport_complete_but_not_process_success(self):
        result = json_line({"type": "result", "subtype": "error", "is_error": True})
        observed = self.run_child(
            "import sys;sys.stdout.buffer.write(" + repr(result) + ");sys.stdout.buffer.flush();raise SystemExit(7)",
            progress=io.StringIO(),
        )
        self.assertEqual(7, observed["exit_code"])
        self.assertEqual(result, observed["stdout"])
        self.assertIsNone(observed["transport_error"])
        self.assertEqual({"child_exited": True, "pipes_closed": True}, observed["cleanup"])

    def test_keyboard_interrupt_from_progress_triggers_cleanup(self):
        class InterruptingProgress:
            def write(self, _value):
                raise KeyboardInterrupt

            def flush(self):
                pass

        event = json_line({"type": "assistant", "message": {"content": []}})
        source = (
            "import sys,time;sys.stdout.buffer.write(" + repr(event) + ");"
            "sys.stdout.buffer.flush();time.sleep(30)"
        )
        started = time.monotonic()
        observed = self.run_child(source, timeout=5, progress=InterruptingProgress())
        self.assertTrue(observed["interrupted"])
        self.assertFalse(observed["timed_out"])
        self.assertTrue(observed["cleanup"]["child_exited"])
        self.assertTrue(observed["cleanup"]["pipes_closed"])
        self.assertLess(time.monotonic() - started, 5.75)


class TransportFaultTests(unittest.TestCase):
    def test_pipe_read_error_is_reported_before_eof(self):
        class BrokenPipe:
            def read1(self, _size):
                raise OSError("synthetic read failure")

        events = advisor_stream.queue.Queue()
        advisor_stream._read_pipe("stdout", BrokenPipe(), events)
        self.assertEqual(("stdout", "error", "synthetic read failure"), events.get_nowait())
        self.assertEqual(("stdout", "eof", None), events.get_nowait())

    def test_wait_error_is_retained_and_bounded(self):
        class BrokenWaitProcess:
            def poll(self):
                return None

            def wait(self, timeout):
                raise OSError("synthetic wait failure")

        errors = []
        started = time.monotonic()
        interrupted = advisor_stream._wait_for_exit(BrokenWaitProcess(), started + 1, errors)
        self.assertFalse(interrupted)
        self.assertEqual(["direct child wait failed: synthetic wait failure"], errors)
        self.assertLess(time.monotonic() - started, 0.25)

    def test_continuously_filled_queue_does_not_extend_cleanup_ceiling(self):
        class ExitedProcess:
            def poll(self):
                return 0

        class LiveThread:
            def is_alive(self):
                return True

        class EndlessEvents:
            def get(self, timeout=None):
                time.sleep(0.001)
                return ("stderr", "data", b"x")

            def get_nowait(self):
                time.sleep(0.001)
                return ("stderr", "data", b"x")

            def empty(self):
                return False

        errors = []
        started = time.monotonic()
        with mock.patch.object(advisor_stream, "CLEANUP_SECONDS", 0.05):
            cleanup, interrupted = advisor_stream._cleanup(
                ExitedProcess(), [LiveThread()], EndlessEvents(), [], [], set(), errors,
                advisor_stream._ProgressView(io.StringIO(), started),
            )
        self.assertFalse(interrupted)
        self.assertEqual({"child_exited": True, "pipes_closed": False}, cleanup)
        self.assertLess(time.monotonic() - started, 0.25)
        self.assertTrue(any("pipe readers" in item for item in errors))
        self.assertTrue(any("not fully drained" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
