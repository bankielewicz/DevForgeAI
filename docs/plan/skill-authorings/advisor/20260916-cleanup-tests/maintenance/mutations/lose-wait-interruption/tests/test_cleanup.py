"""Cleanup fault tests use real children/pipes and faults at OS boundaries only."""

import io
import queue
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from test_streaming import advisor, jsonl, result_event, streaming


NATIVE_POPEN = subprocess.Popen


class ProcessProxy:
    """Delegate to an actual child; individual tests override one boundary."""

    def __init__(self, child):
        self.child = child
        self.stdout = child.stdout
        self.stderr = child.stderr

    def __getattr__(self, name):
        return getattr(self.child, name)


class PipeProxy:
    def __init__(self, pipe):
        self.pipe = pipe

    def __getattr__(self, name):
        return getattr(self.pipe, name)


class CleanupFailureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def own(self, child):
        def release():
            if child.poll() is None:
                child.kill()
            child.wait(timeout=5)
            for pipe in (child.stdout, child.stderr):
                if pipe is not None:
                    pipe.close()

        self.addCleanup(release)
        return child

    def child(self, code="pass"):
        return self.own(NATIVE_POPEN(
            [sys.executable, "-B", "-c", code], cwd=self.root,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE))

    def assert_no_advice(self, value):
        outcome, text, _ = advisor.interpret_stream(value, cap="1.00")
        self.assertEqual(outcome["execution_status"], "FAILED")
        self.assertEqual(outcome["response_status"], "NOT_EVALUATED")
        self.assertIsNone(outcome["verdict"])
        self.assertIsNone(text)

    def test_closed_real_pipe_reports_read_error_and_eof_without_hanging(self):
        children = []

        def factory(*args, **kwargs):
            child = self.own(NATIVE_POPEN(*args, **kwargs))
            children.append(child)
            child.stdout.close()
            return child

        with patch.object(streaming.subprocess, "Popen", factory):
            value = streaming.execute_stream(
                [sys.executable, "-B", "-c", "pass"], self.root, 5,
                progress=io.StringIO())
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["stdout"], b"")
        self.assertFalse(value["timed_out"])
        self.assertIn("stdout read failed:", value["transport_error"])
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        self.assertIsNotNone(children[0].poll())
        self.assertTrue(children[0].stderr.closed)
        self.assert_no_advice(value)

    def test_read_oserror_after_real_bytes_retains_bytes_and_denies_advice(self):
        raw = jsonl(result_event())

        class ReadFault(PipeProxy):
            first = True

            def read1(self, size):
                if self.first:
                    self.first = False
                    return self.pipe.read(len(raw))
                raise OSError("injected pipe read failure")

        def factory(*args, **kwargs):
            proxy = ProcessProxy(self.own(NATIVE_POPEN(*args, **kwargs)))
            proxy.stdout = ReadFault(proxy.stdout)
            return proxy

        code = f"import sys; sys.stdout.buffer.write({raw!r}); sys.stdout.buffer.flush()"
        with patch.object(streaming.subprocess, "Popen", factory):
            value = streaming.execute_stream(
                [sys.executable, "-B", "-c", code], self.root, 5,
                progress=io.StringIO())
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["stdout"], raw)
        self.assertEqual(value["stderr"], b"")
        self.assertEqual(value["transport_error"], "stdout read failed: injected pipe read failure")
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        self.assert_no_advice(value)

    def close_fault(self, error):
        raw = jsonl(result_event())
        children = []

        class CloseFault(PipeProxy):
            def close(self):
                self.pipe.close()
                raise error

        def factory(*args, **kwargs):
            child = self.own(NATIVE_POPEN(*args, **kwargs))
            children.append(child)
            proxy = ProcessProxy(child)
            proxy.stdout = CloseFault(child.stdout)
            return proxy

        code = (f"import sys; sys.stdout.buffer.write({raw!r}); "
                "sys.stdout.buffer.flush(); sys.stderr.buffer.write(b'diagnostic')")
        with patch.object(streaming.subprocess, "Popen", factory):
            value = streaming.execute_stream(
                [sys.executable, "-B", "-c", code], self.root, 5,
                progress=io.StringIO())
        self.assertEqual(value["stdout"], raw)
        self.assertEqual(value["stderr"], b"diagnostic")
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["cleanup"], {"child_exited": True, "pipes_closed": True})
        self.assertTrue(children[0].stdout.closed)
        self.assertTrue(children[0].stderr.closed)
        self.assertIsNotNone(children[0].poll())
        self.assert_no_advice(value)
        return value

    def test_pipe_close_oserror_preserves_evidence_and_closes_other_pipe(self):
        value = self.close_fault(OSError("injected close failure"))
        self.assertEqual(value["transport_error"], "pipe close failed: injected close failure")
        self.assertFalse(value["interrupted"])

    def test_pipe_close_interrupt_preserves_evidence_and_closes_other_pipe(self):
        value = self.close_fault(KeyboardInterrupt())
        self.assertEqual(value["transport_error"], "pipe close interrupted")
        self.assertTrue(value["interrupted"])

    def test_spawn_with_missing_working_directory_reports_failure_without_advice(self):
        value = streaming.execute_stream(
            [sys.executable, "-B", "-c", "pass"], self.root / "absent", 5,
            progress=io.StringIO())
        self.assertIsNone(value["exit_code"])
        self.assertIsInstance(value["spawn_error"], str)
        self.assertTrue(value["spawn_error"])
        self.assertFalse(value["timed_out"])
        self.assertEqual(value["stdout"], b"")
        self.assertEqual(value["stderr"], b"")
        self.assertEqual(value["cleanup"], {"child_exited": False, "pipes_closed": True})
        self.assert_no_advice(value)

    def test_interrupted_wait_retries_and_reaps_real_child(self):
        child = self.child("import time; time.sleep(30)")

        class WaitInterrupt(ProcessProxy):
            calls = 0

            def wait(self, timeout=None):
                self.calls += 1
                if self.calls == 1:
                    raise KeyboardInterrupt()
                self.child.kill()
                return self.child.wait(timeout=timeout)

        proxy = WaitInterrupt(child)
        errors = []
        interrupted = streaming._wait_for_exit(proxy, time.monotonic() + 5, errors)
        self.assertTrue(interrupted)
        self.assertGreaterEqual(proxy.calls, 2)
        self.assertEqual(errors, ["cleanup wait interrupted"])
        self.assertIsNotNone(child.poll())

    def test_exit_during_kill_error_is_not_reported_as_live_child_failure(self):
        child = self.child("import time; time.sleep(30)")

        class ExitRace(ProcessProxy):
            def kill(self):
                self.child.kill()
                self.child.wait(timeout=5)
                raise ProcessLookupError("process exited during termination")

        errors = []
        interrupted = streaming._kill_child(ExitRace(child), time.monotonic() + 5, errors)
        self.assertFalse(interrupted)
        self.assertEqual(errors, [])
        self.assertIsNotNone(child.poll())

    def test_already_exited_child_is_not_killed_again(self):
        child = self.child()
        child.wait(timeout=5)

        class NoKill(ProcessProxy):
            def kill(self):
                self.fail_if_called = True
                raise AssertionError("An exited child must not be killed")

        errors = []
        self.assertFalse(streaming._kill_child(NoKill(child), time.monotonic() + 5, errors))
        self.assertEqual(errors, [])
        self.assertEqual(child.returncode, 0)

    def cleanup(self, events, threads=()):
        child = self.child()
        child.wait(timeout=5)
        stdout, stderr, eof, errors = [], [], set(), []
        status, interrupted = streaming._cleanup(
            child, threads, events, stdout, stderr, eof, errors,
            streaming._ProgressView(io.StringIO(), time.monotonic()))
        self.assertEqual(child.poll(), 0)
        return status, interrupted, b"".join(stdout), b"".join(stderr), eof, errors

    def test_interrupt_while_reader_is_alive_still_drains_real_thread_events(self):
        release = threading.Event()
        raw = jsonl(result_event())

        class InterruptQueue(queue.Queue):
            pending = True

            def get(self, *args, **kwargs):
                if self.pending:
                    self.pending = False
                    release.set()
                    raise KeyboardInterrupt()
                return super().get(*args, **kwargs)

        events = InterruptQueue()

        def producer():
            if release.wait(5):
                events.put(("stdout", "data", raw))
                events.put(("stdout", "eof", None))

        thread = threading.Thread(target=producer)
        thread.start()
        try:
            status, interrupted, stdout, stderr, eof, errors = self.cleanup(events, [thread])
        finally:
            release.set()
            thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(status, {"child_exited": True, "pipes_closed": True})
        self.assertTrue(interrupted)
        self.assertEqual(stdout, raw)
        self.assertEqual(stderr, b"")
        self.assertEqual(eof, {"stdout"})
        self.assertEqual(errors, ["cleanup pipe drain interrupted"])
        self.assertTrue(events.empty())

    def test_interrupt_during_final_queue_drain_retains_every_event(self):
        class InterruptQueue(queue.Queue):
            pending = True

            def get_nowait(self):
                if self.pending:
                    self.pending = False
                    raise KeyboardInterrupt()
                return super().get_nowait()

        events = InterruptQueue()
        raw = jsonl(result_event())
        events.put(("stdout", "data", raw))
        events.put(("stdout", "eof", None))
        events.put(("stderr", "data", b"diagnostic"))
        status, interrupted, stdout, stderr, eof, errors = self.cleanup(events)
        self.assertEqual(status, {"child_exited": True, "pipes_closed": True})
        self.assertTrue(interrupted)
        self.assertEqual(stdout, raw)
        self.assertEqual(stderr, b"diagnostic")
        self.assertEqual(eof, {"stdout"})
        self.assertEqual(errors, ["cleanup queue drain interrupted"])
        self.assertTrue(events.empty())

    def test_cleanup_deadline_reports_undrained_queue_instead_of_losing_evidence_silently(self):
        class SlowQueue(queue.Queue):
            def get_nowait(self):
                time.sleep(0.06)
                return super().get_nowait()

        events = SlowQueue()
        events.put(("stdout", "data", b"first"))
        events.put(("stdout", "data", b"remaining"))
        started = time.monotonic()
        with patch.object(streaming, "CLEANUP_SECONDS", 0.03):
            status, interrupted, stdout, stderr, eof, errors = self.cleanup(events)
        self.assertLess(time.monotonic() - started, 2)
        self.assertEqual(status, {"child_exited": True, "pipes_closed": True})
        self.assertFalse(interrupted)
        self.assertEqual(stdout, b"first")
        self.assertEqual(stderr, b"")
        self.assertEqual(eof, set())
        self.assertEqual(errors, ["captured stream queue was not fully drained within cleanup ceiling"])
        self.assertEqual(events.qsize(), 1)
        self.assertEqual(events.get_nowait(), ("stdout", "data", b"remaining"))


if __name__ == "__main__":
    unittest.main()
