"""Executed parser and input-record regression cases from independent review."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location("review_" + name, PACKAGE / "scripts" / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class ReviewInputTests(unittest.TestCase):
    def test_all_parsers_reject_nested_positive_and_negative_overflow(self):
        for name in ("run_evaluation", "graders", "build_evidence"):
            loaded = module(name)
            parser = getattr(loaded, "strict_json", getattr(loaded, "json_value", None))
            for number in ("1e400", "-1e400"):
                with self.subTest(parser=name, number=number):
                    with self.assertRaisesRegex(ValueError, "non-finite"):
                        parser('{"observation":{"values":[' + number + ']}}')

    def test_all_parsers_preserve_finite_exponent_values(self):
        for name in ("run_evaluation", "graders", "build_evidence"):
            loaded = module(name)
            parser = getattr(loaded, "strict_json", getattr(loaded, "json_value", None))
            with self.subTest(parser=name):
                self.assertEqual(parser('{"values":[1e100,-1e100]}'), {"values": [1e100, -1e100]})

    def input_record(self, data, extra=()):
        temporary = tempfile.TemporaryDirectory(prefix="builder-input-review-")
        self.addCleanup(temporary.cleanup)
        source = Path(temporary.name) / "source.txt"
        source.write_bytes(data)
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(PACKAGE / "scripts/build_evidence.py"),
             "input-record", "--file", str(source), "--id", "source", "--snapshot-path", "inputs/source.txt", *extra],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        self.assertEqual(source.read_bytes(), data)
        self.assertEqual(list(source.parent.iterdir()), [source])
        return result

    def test_empty_file_without_range_emits_input_only(self):
        result = self.input_record(b"")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(set(value), {"input"})
        self.assertEqual(value["input"]["bytes"], 0)
        self.assertEqual(value["input"]["sha256"], hashlib.sha256(b"").hexdigest())

    def test_nonempty_file_without_range_does_not_invent_excerpt(self):
        result = self.input_record(b"One source.\r\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"input"})

    def test_empty_file_with_explicit_empty_range_is_error(self):
        result = self.input_record(b"", ("--start-byte", "0", "--end-byte", "0"))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("source byte range", result.stderr)

    def test_explicit_end_range_preserves_raw_bytes(self):
        result = self.input_record(b"One\r\nTwo\r\n", ("--end-byte", "5"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["source_ref"], {
            "input_id": "source", "start_byte": 0, "end_byte": 5,
            "sha256": hashlib.sha256(b"One\r\n").hexdigest(),
        })


if __name__ == "__main__":
    unittest.main()
