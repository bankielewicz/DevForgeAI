"""The document-fixture validator must enforce calendar dates through JSON Schema."""
import importlib.util
import os
from pathlib import Path
import unittest

from grade_contract_eval_v5 import source_grade


class DocumentDateFormats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tests = Path(__file__).resolve().parent
        repo = tests.parents[3]
        previous = Path.cwd()
        try:
            os.chdir(repo)
            spec = importlib.util.spec_from_file_location("date_fixtures", tests / "make_architecture_evals.py")
            cls.fixtures = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.fixtures)
        finally:
            os.chdir(previous)
        cls.fixtures.SCHEMAS = repo / "src/schemas"

    def test_impossible_dates_rejected_by_fixture_validator(self):
        for date in ("2026-13-45", "2026-02-30", "2025-02-29"):
            with self.subTest(date=date):
                document = self.fixtures.PRD_V1.replace("created: 2026-09-14", f"created: {date}")
                with self.assertRaisesRegex(AssertionError, "is not a 'date'"):
                    self.fixtures.validate("impossible date", document, "prd.schema.json")

    def test_leap_day_accepted_by_fixture_validator(self):
        document = self.fixtures.PRD_V1.replace("created: 2026-09-14", "created: 2024-02-29")
        self.fixtures.validate("leap day", document, "prd.schema.json")

    def test_bad_date_response_must_name_schema_rule(self):
        package = Path(__file__).resolve().parents[1]
        for skill in ("prd", "architecture"):
            grader = package / "evals" / skill / "policy-bad-date/graders/names-field.md"
            for response, expected in (
                ("POL-001.md updated: '2026-13-45' is not a 'date' (schema). Nothing was written.", True),
                ("POL-001.md updated: date is invalid. Nothing was written.", False),
                ("POL-001.md: schema error. Nothing was written.", False),
            ):
                with self.subTest(skill=skill, response=response):
                    result = source_grade(grader, package, response, {"arm": "plugin"}, [], [])
                    self.assertEqual(result["passed"], expected)


if __name__ == "__main__":
    unittest.main()
