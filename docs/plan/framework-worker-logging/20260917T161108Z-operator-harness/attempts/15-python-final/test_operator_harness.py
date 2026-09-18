"""Offline operator composition using synthetic files and processes only."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

TRIAL = Path(r"C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic")
SOURCE = TRIAL / "operator-harness-001/diagnostic.py"
spec = importlib.util.spec_from_file_location("operator_under_test", SOURCE)
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class OperatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="operator & space-", dir=Path(__file__).parent.parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "package"
        self.package.mkdir()
        fixture = self.root / "fixture"
        fixture.mkdir()
        self.file(fixture / "task.json", {"fixture": True})
        live = self.file(self.root / "current.txt", {"synthetic": True})
        self.inventory = {"schema_version": 2, "entries": [dict(d.binding(live), state="file"),
                          {"path": str(self.root / "removed"), "state": "absent"},
                          {"path": str(fixture), "state": "directory", "members": ["task.json"]}]}
        approved = self.file(self.root / "approved.json", self.inventory)
        review = self.file(self.root / "review.json", {"findings": dict(a=False, b=False, c=False, e=False)})
        diagnostics = self.file(self.root / "diagnostics.json", {"level": "debug", "redaction": "closed-v1"})
        selection = self.file(self.root / "selection.md", {"reviewer": "Bryan"})
        worker = self.file(self.root / "worker.txt", {"never_executed": True})
        self.peer = self.root / "synthetic peer & literal.py"
        self.peer.write_text(
            "import json,sys,pathlib,threading,time,os\n"
            "root=pathlib.Path(__file__).parent\n"
            "if sys.argv[1]=='profile-sources':\n"
            " sys.stdout.buffer.write((root/'observed.json').read_bytes())\n"
            "else:\n"
            " request=json.loads(pathlib.Path(sys.argv[3]).read_text())\n"
            " seen=[]\n"
            " threading.Thread(target=lambda:seen.append(os.read(0,1)),daemon=True).start()\n"
            " time.sleep(.12)\n"
            " print('STDIN_OPEN' if not seen else 'STDIN_CLOSED',flush=True)\n"
            " sys.stderr.buffer.write(b'probe synthetic diagnostic\\x00\\xff')\n"
            " run=pathlib.Path(request['run_dir']); run.mkdir()\n"
            " (run/'journal.jsonl').write_text(json.dumps({'kind':'process_exit','data':{'worker_exit_code':1}})+'\\n')\n"
            " sys.exit(3)\n", encoding="utf-8")
        self.file(self.root / "observed.json", self.inventory)
        manifest = self.file(self.root / "manifest.json", {"entries": {"fixture": d.binding(fixture / "task.json")},
                                                          "reparse_points": []})
        self.config = dict(workspace=str(self.root), trial_root=str(self.root), package_root=str(self.package),
            probe=d.binding(self.peer), worker=d.binding(worker),
            preserved_manifests=[dict(binding=d.binding(manifest), selectors=[["entries"]])],
            extra_bindings=[d.binding(live)], junctions=[], approved_inventory=d.binding(approved),
            selection=d.binding(selection), fixture=d.binding(fixture / "task.json"),
            review_template=d.binding(review), diagnostics=d.binding(diagnostics), reviewer="Bryan",
            request=dict(schema_version=3, checkout_root=str(fixture), run_dir=str(self.root / "run"),
                         profile=dict(model="gpt-6-astra", effort="high"), worker_executable=str(worker)))
        self.emitted = []
        self.addCleanup(patch.stopall)
        patch.object(d, "emit", side_effect=self.emitted.append).start()
        self.real_capture = d.capture
        self.commands = []
        self.environment = {key: value for key, value in os.environ.items() if key not in d.guarded_names(os.environ)}

    def file(self, path, document):
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def synthetic_capture(self, argv, cwd, attempt, **kwargs):
        self.commands.append(list(argv))
        # Replace only the external executable at the process boundary. All
        # recording, argv transfer, stdin, files and timeouts are real Windows I/O.
        return self.real_capture([sys.executable, "-B", "-X", "utf8", *argv], cwd, attempt, **kwargs)

    def invoke(self, mode="--prepare"):
        with patch.object(d, "capture", side_effect=self.synthetic_capture):
            return d.operate(mode, self.config, self.environment)

    def last_invocation(self):
        return sorted((self.package / "invocations").iterdir())[-1]

    def test_preservation_checks_root_arrays_and_nested_dicts(self):
        array = self.file(self.root / "array.json", [self.config["fixture"]])
        self.config["preserved_manifests"].append(dict(binding=d.binding(array), selectors=[[]]))
        result = d.verify_preservation(self.config)
        self.assertEqual(1, result["current_reviewed_files_hashed"])
        self.assertEqual("NOT_EVALUATED", result["framework_acceptance"])

    def test_changed_and_missing_preserved_files_stop(self):
        live = Path(self.config["extra_bindings"][0]["path"])
        live.write_bytes(b"changed")
        with self.assertRaisesRegex(RuntimeError, "binding_drift"):
            d.verify_preservation(self.config)
        live.unlink()
        with self.assertRaises(FileNotFoundError):
            d.verify_preservation(self.config)

    def test_size_binding_drift_stops(self):
        self.config["fixture"]["bytes"] += 1
        with self.assertRaisesRegex(RuntimeError, "size_drift"):
            d.verify_preservation(self.config)

    def test_fixture_membership_drift_stops(self):
        self.file(Path(self.config["request"]["checkout_root"]) / "extra", {})
        with self.assertRaisesRegex(RuntimeError, "fixture_membership"):
            d.verify_preservation(self.config)

    def test_junction_metadata_is_checked_without_traversal(self):
        self.config["junctions"] = [dict(path="synthetic junction", target="target")]
        with patch.object(d.os, "lstat") as info, patch.object(d.os, "readlink", return_value="\\\\?\\target"):
            info.return_value.st_reparse_tag = 0xA0000003
            d.verify_preservation(self.config)
            info.return_value.st_reparse_tag = 123
            with self.assertRaisesRegex(RuntimeError, "junction_tag_drift"):
                d.verify_preservation(self.config)
            info.return_value.st_reparse_tag = 0xA0000003
            with patch.object(d.os, "readlink", return_value="other"):
                with self.assertRaisesRegex(RuntimeError, "junction_target_drift"):
                    d.verify_preservation(self.config)

    def test_retained_reparse_target_drift_stops(self):
        group = self.config["preserved_manifests"][0]
        path = Path(group["binding"]["path"])
        self.file(path, dict(entries={}, reparse_points=[dict(path="link", target="target")]))
        group["binding"] = d.binding(path)
        with patch.object(d.os, "readlink", return_value="target"):
            d.verify_preservation(self.config)
        with patch.object(d.os, "readlink", return_value="different"):
            with self.assertRaisesRegex(RuntimeError, "retained_reparse_drift"):
                d.verify_preservation(self.config)

    def test_child_environment_omits_only_approved_name_without_values(self):
        parent = dict(Path="unchanged", anthropic_API_KEY="fixture-secret")
        before = parent.copy()
        child, receipt = d.child_environment(parent)
        self.assertEqual(dict(Path="unchanged"), child)
        self.assertEqual(before, parent)
        self.assertNotIn("fixture-secret", json.dumps(receipt))
        for name in ("OPENAI_API_KEY", "service_ACCESS_TOKEN", "OPENAI_BASE_URL", "CODEX_HOME"):
            with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, "unapproved_guarded"):
                d.child_environment({name: "never_print_this"})

    def test_prepare_binds_exact_bytes_and_launches_only_collector(self):
        self.assertEqual(0, self.invoke())
        result = d.read_json(self.last_invocation() / "result.json")
        self.assertEqual("PREPARED", result["stage"])
        packet = Path(result["packet"])
        request = d.read_json(packet / "request.json")
        review = d.read_json(packet / "review.json")
        self.assertEqual("Bryan", review["reviewer"])
        self.assertEqual(self.config["selection"]["path"], review["trial_selection_ref"])
        self.assertEqual(d.binding(packet / "review.json")["sha256"], request["profile"]["review_sha256"])
        self.assertEqual(Path(self.config["diagnostics"]["path"]).read_bytes(), (packet / "diagnostics.json").read_bytes())
        for expected in d.read_json(packet / "input-manifest.json"):
            self.assertEqual(expected, d.binding(expected["path"]))
        self.assertEqual(["profile-sources"], [argv[1] for argv in self.commands])
        self.assertFalse((self.root / "launch-invocation.json").exists())
        self.assertFalse((self.root / "native-001").exists())

    def test_absence_or_membership_drift_stops_before_dispatch(self):
        observed = copy.deepcopy(self.inventory)
        observed["entries"][2]["members"].append("new-file")
        self.file(self.root / "observed.json", observed)
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertTrue((self.root / "launch-invocation.json").is_file())
        self.assertEqual(["profile-sources"], [argv[1] for argv in self.commands])
        stop = d.read_json(self.last_invocation() / "stop.json")
        self.assertEqual(0, stop["native_preflight_invocations"])
        self.assertIn("source_inventory_drift", stop["reason"])
        comparison = d.read_json(self.last_invocation() / "source-comparison.json")
        self.assertFalse(comparison["exact_inventory_match"])

    def test_source_collection_failures_are_not_ready(self):
        for field, value in (("process_exit_code", 1), ("timed_out", True),
                             ("interrupted", True), ("owned_probe_stopped", False), ("stderr", {"bytes": 1})):
            with self.subTest(field=field):
                receipt = dict(process_exit_code=0, timed_out=False, interrupted=False,
                               owned_probe_stopped=True, stderr=dict(bytes=0))
                receipt[field] = value
                invocation = self.root / field
                invocation.mkdir()
                with patch.object(d, "capture_visible", return_value=(receipt, 0.1)):
                    with self.assertRaisesRegex(RuntimeError, "source_collection_failed"):
                        d.prepare(self.config, invocation, {})

    def test_source_outer_budget_includes_receipt_write(self):
        receipt = dict(process_exit_code=0, timed_out=False, interrupted=False,
                       owned_probe_stopped=True, stderr=dict(bytes=0))
        with patch.object(d, "capture_visible", return_value=(receipt, 30.01)):
            invocation = self.root / "late"
            invocation.mkdir()
            with self.assertRaisesRegex(RuntimeError, "source_collection_failed"):
                d.prepare(self.config, invocation, {})

    def test_positive_findings_cannot_be_silently_introduced(self):
        path = Path(self.config["review_template"]["path"])
        self.file(path, {"findings": dict(a=True, b=False, c=False, e=False)})
        self.config["review_template"] = d.binding(path)
        self.assertEqual(3, self.invoke())
        self.assertIn("unexpected_operator_findings", d.read_json(self.last_invocation() / "stop.json")["reason"])

    def test_each_occupied_path_prevents_dispatch(self):
        for name in ("run", "native-001", "sources-002-prelaunch", "inputs-003-native", "launch-invocation.json"):
            path = self.root / name
            path.write_bytes(b"preserve")
            with self.subTest(name=name):
                self.assertEqual(3, self.invoke("--run-once"))
                self.assertEqual(b"preserve", path.read_bytes())
                self.assertEqual([], self.commands)
            path.unlink()

    def preserved_stop(self, invocations=0):
        previous = self.root / "previous"
        previous.mkdir()
        stop = self.file(previous / "stop.json", dict(stage="PREPARATION_FAILED", native_preflight_invocations=invocations))
        reservation = self.file(self.root / "launch-invocation.json", dict(invocation=str(previous)))
        self.config["prior_preparation_stop"] = dict(reservation=d.binding(reservation), stop=d.binding(stop))
        return reservation.read_bytes(), stop.read_bytes()

    def test_selected_preparation_stop_is_preserved_without_spending_native_budget(self):
        before = self.preserved_stop()
        self.assertEqual(0, self.invoke())
        self.assertEqual(before[0], (self.root / "launch-invocation.json").read_bytes())
        self.assertEqual(before[1], (self.root / "previous/stop.json").read_bytes())
        self.assertFalse((self.package / "launch-invocation-after-preparation-stop.json").exists())

    def test_a_consumed_or_modified_prior_stop_cannot_be_reopened(self):
        self.preserved_stop(invocations=1)
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertFalse((self.root / "native-001").exists())
        (self.root / "previous/stop.json").write_bytes(b"changed")
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertEqual([], self.commands)

    def test_resumed_selection_still_allows_at_most_one_dispatch(self):
        before = self.preserved_stop()
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertEqual(1, sum(argv[1] == "preflight" for argv in self.commands))
        self.assertTrue((self.package / "launch-invocation-after-preparation-stop.json").exists())
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertEqual(1, sum(argv[1] == "preflight" for argv in self.commands))
        self.assertEqual(before[0], (self.root / "launch-invocation.json").read_bytes())

    def test_native_synthetic_failure_retains_streams_exit_and_open_stdin(self):
        self.assertEqual(3, self.invoke("--run-once"))
        attempt = self.root / "native-001"
        self.assertEqual(b"STDIN_OPEN\r\n", (attempt / "stdout.bin").read_bytes())
        self.assertEqual(b"probe synthetic diagnostic\x00\xff", (attempt / "stderr.bin").read_bytes())
        result = d.read_json(self.last_invocation() / "result.json")
        self.assertEqual(3, result["probe_exit_code"])
        self.assertEqual(1, result["observed_worker_exit_code"])
        self.assertEqual("FAILURE_OBSERVED", result["worker_outcome"])
        self.assertEqual("REQUIRES_RUST_EVIDENCE", result["worker_tree_status"])
        self.assertEqual(1, result["native_preflight_invocations"])
        self.assertEqual(["profile-sources", "preflight"], [argv[1] for argv in self.commands])
        before = (attempt / "receipt.json").read_bytes()
        self.assertEqual(3, self.invoke("--run-once"))
        self.assertEqual(before, (attempt / "receipt.json").read_bytes())
        self.assertEqual(2, len(self.commands))

    def test_native_timeout_is_distinct_and_never_retried(self):
        self.peer.write_text("import sys,pathlib,time\nroot=pathlib.Path(__file__).parent\n"
            "if sys.argv[1]=='profile-sources': sys.stdout.buffer.write((root/'observed.json').read_bytes())\n"
            "else: print('waiting',flush=True); time.sleep(10)\n", encoding="utf-8")
        self.config["probe"] = d.binding(self.peer)
        with patch.object(d, "NATIVE_BUDGET", dict(cancel_after=.2, grace=.1, reap=.3, finalize=.5, hold_stdin=True)):
            self.assertEqual(124, self.invoke("--run-once"))
        result = d.read_json(self.last_invocation() / "result.json")
        self.assertTrue(result["timed_out"])
        self.assertTrue(result["owned_probe_stopped"])
        self.assertEqual(1, result["native_preflight_invocations"])

    def test_cleanup_unknown_or_interrupt_never_reports_success(self):
        actual = d.capture_visible
        for field, value in (("owned_probe_stopped", False), ("interrupted", True), ("process_exit_code", None)):
            with self.subTest(field=field):
                def changed(argv, config, attempt, environment, stage, budgets):
                    receipt, elapsed = actual(argv, config, attempt, environment, stage, budgets)
                    if stage == "NATIVE_PREFLIGHT":
                        receipt[field] = value
                    return receipt, elapsed
                with patch.object(d, "capture_visible", side_effect=changed):
                    self.assertEqual(125 if field == "process_exit_code" else 124, self.invoke("--run-once"))
                # Each subcase is a separate disposable trial, never a replay of
                # retained production or native evidence.
                self.config["trial_root"] = str(self.root / field)
                Path(self.config["trial_root"]).mkdir()
                self.config["request"]["run_dir"] = str(Path(self.config["trial_root"]) / "run")

    def test_recording_exception_leaves_consumed_latch_and_stop(self):
        actual = d.capture_visible
        def fail(argv, config, attempt, environment, stage, budgets):
            if stage == "NATIVE_PREFLIGHT":
                raise OSError("synthetic recorder failure")
            return actual(argv, config, attempt, environment, stage, budgets)
        with patch.object(d, "capture_visible", side_effect=fail):
            self.assertEqual(3, self.invoke("--run-once"))
        self.assertTrue((self.root / "launch-invocation.json").exists())
        stop = d.read_json(self.last_invocation() / "stop.json")
        self.assertEqual("DISPATCH_OR_RECORDING_FAILED", stop["stage"])
        self.assertEqual(1, stop["native_preflight_invocations"])

    def test_failure_receipts_are_unique_and_keep_secret_values_out(self):
        parent = {"OPENAI_API_KEY": "SYNTHETIC_NEVER_LOG"}
        for _ in range(2):
            self.assertEqual(3, d.operate("--prepare", self.config, parent))
        files = list((self.package / "invocations").glob("*/stop.json"))
        self.assertEqual(2, len(files))
        for path in files:
            self.assertNotIn("SYNTHETIC_NEVER_LOG", path.read_text())

    def test_monitor_escapes_through_emit_and_does_not_change_files(self):
        attempt = self.root / "display"
        attempt.mkdir()
        data = bytes(range(256)) * 300
        (attempt / "stdout.bin").write_bytes(data)
        (attempt / "stderr.bin").write_bytes(b"problem")
        event = threading.Event()
        event.set()
        d.monitor(attempt, event, "SYNTHETIC")
        self.assertEqual(data, (attempt / "stdout.bin").read_bytes())
        self.assertTrue(any(record.get("stream") == "stderr" for record in self.emitted))
        self.assertTrue(any("elapsed_seconds" in record for record in self.emitted))
        with patch.object(d, "emit", side_effect=BrokenPipeError):
            d.monitor(attempt, event, "SYNTHETIC")

    def test_console_backpressure_does_not_delay_process_cleanup(self):
        release = threading.Event()
        entered = threading.Event()
        main_thread = threading.current_thread()
        def slow(record):
            if threading.current_thread() is not main_thread:
                entered.set()
                release.wait(5)
        started = time.monotonic()
        try:
            with patch.object(d, "emit", side_effect=slow):
                receipt, _ = d.capture_visible([sys.executable, "-B", "-c", "print('done')"],
                    self.config, self.root / "backpressure", self.environment, "SYNTHETIC",
                    dict(cancel_after=1, grace=.1, reap=.1, finalize=.1, hold_stdin=True))
            self.assertTrue(entered.is_set())
            self.assertEqual(0, receipt["process_exit_code"])
            self.assertLess(time.monotonic() - started, 1.3)
        finally:
            release.set()

    def test_worker_observation_is_explicitly_not_inspection(self):
        self.assertIn("UNKNOWN", d.worker_observation(self.config)["worker_outcome"])
        run = Path(self.config["request"]["run_dir"])
        run.mkdir()
        path = run / "journal.jsonl"
        for content in (b"invalid", b"{}", b"null", b"x" * (32 * 1024 * 1024 + 1)):
            path.write_bytes(content)
            self.assertIn("UNKNOWN", d.worker_observation(self.config)["worker_outcome"])
        path.write_bytes(b'{"kind":"admitted","data":{}}\n')
        self.assertIsNone(d.worker_observation(self.config)["observed_worker_exit_code"])
        path.write_bytes(b'{"kind":"process_exit","data":{"worker_exit_code":0}}\n')
        self.assertEqual("REQUIRES_RUST_INSPECTION", d.worker_observation(self.config)["worker_outcome"])

    def test_main_requires_exact_mode_and_has_no_implicit_launch(self):
        self.assertEqual(2, d.main([]))
        self.assertEqual(2, d.main(["--run-once", "--run-once"]))
        with self.assertRaisesRegex(RuntimeError, "explicit_prepare"):
            d.operate("unknown", self.config, {})
        with patch.object(d, "selected_config", return_value=self.config), patch.object(d, "capture", side_effect=self.synthetic_capture):
            with patch.dict(os.environ, self.environment, clear=True):
                self.assertEqual(0, d.main(["--prepare"]))
        with patch.object(sys, "argv", [str(SOURCE)]), patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as result:
                runpy.run_path(str(SOURCE), run_name="__main__")
            self.assertEqual(2, result.exception.code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
