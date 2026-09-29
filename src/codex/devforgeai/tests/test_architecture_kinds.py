"""Component-kinds schema compatibility and the native Python-regex grading contract."""
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

TESTS = Path(__file__).resolve().parent
PACKAGE = TESTS.parent
REPO = TESTS.parents[3]
sys.path.insert(0, str(TESTS))
import grade_architecture_eval as grader


class ArchitectureKindsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        previous = Path.cwd()
        try:
            os.chdir(REPO)
            spec = importlib.util.spec_from_file_location('kinds_fixtures', TESTS/'make_architecture_evals.py')
            cls.fixtures = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.fixtures)
        finally:
            os.chdir(previous)
        cls.fixtures.SCHEMAS = REPO/'src/schemas'
        cls.template = (PACKAGE/'skills/architecture/assets/arch.md').read_text().replace('YYYY-MM-DD', '2026-09-29')

    def kinds_fixture(self, field):
        # Replace only the template component's kinds field; retain the complete document.
        return self.template.replace(
            '    kinds:                 # one or more: user-interface | service | platform | api | relational-store | data-store | external\n      - "service"\n', field)

    def test_template_mode_schema(self):
        self.fixtures.validate('dated template', self.template, 'arch.schema.json')

    def test_schema_accepts_all_kinds_multiple_and_legacy_absence(self):
        kinds = ['user-interface', 'service', 'platform', 'api', 'relational-store', 'data-store', 'external']
        fields = [''] + ['    kinds:\n      - "'+kind+'"\n' for kind in kinds]
        fields += ['    kinds:\n      - "service"\n      - "api"\n']
        for field in fields:
            with self.subTest(field=field):
                self.fixtures.validate('valid kinds', self.kinds_fixture(field), 'arch.schema.json')

    def test_schema_rejects_unknown_duplicate_empty_and_scalar(self):
        fields = ['    kinds:\n      - "unknown-kind"\n',
                  '    kinds:\n      - "service"\n      - "service"\n',
                  '    kinds: []\n', '    kinds: "service"\n']
        for field in fields:
            with self.subTest(field=field), self.assertRaises(AssertionError):
                self.fixtures.validate('invalid kinds', self.kinds_fixture(field), 'arch.schema.json')

    def grade_kinds(self, content):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            trial = root/'matrix/kinds--plugin--1'
            artifact = trial/'workspace/docs/specs/arch/ARCH-001.md'
            artifact.parent.mkdir(parents=True)
            artifact.write_text(content)
            definitions = root/'definitions/creates-arch/graders'
            definitions.mkdir(parents=True)
            shutil.copy2(PACKAGE/'evals/architecture/creates-arch/graders/cmp-kinds.md', definitions)
            rows = grader.grade_source('creates-arch', trial, '', [], [], 'plugin')
            self.assertEqual(len(rows), 1)
            return rows[0]['passed']

    def test_native_grader_accepts_kinds_block_and_uncertainty_marker(self):
        for field in ['    kinds:\n      - "service"\n',
                      '    kinds:\n      - "service"\n      - "api"\n']:
            with self.subTest(field=field):
                self.assertTrue(self.grade_kinds(self.kinds_fixture(field)))
        uncertain = self.kinds_fixture('').replace('[NEEDS CLARIFICATION: <question>]', '[NEEDS CLARIFICATION: kinds of CMP-01]')
        self.assertTrue(self.grade_kinds(uncertain))

    def test_native_grader_rejects_unknown_flow_empty_and_mixed_fields(self):
        fields = ['    kinds:\n      - "unknown-kind"\n',
                  '    kinds: ["service"]\n', '    kinds: []\n', '    kinds:\n',
                  '    kinds:\n      - "service"\n      - "unknown-kind"\n']
        for field in fields:
            with self.subTest(field=field):
                document = self.kinds_fixture(field)
                self.assertFalse(self.grade_kinds(document))
                self.assertFalse(self.grade_kinds(document.replace('[NEEDS CLARIFICATION: <question>]', '[NEEDS CLARIFICATION: kinds of CMP-02]')))
        self.assertFalse(self.grade_kinds(self.kinds_fixture('')))

    def test_legacy_fixture_components_remain_schema_valid_without_kinds(self):
        for label in ('ARCH_EXISTING', 'ARCH_SUPERSEDED', 'ARCH_TO_REVIEW', 'ARCH_REVIEWED'):
            with self.subTest(label=label):
                content = getattr(self.fixtures, label)
                self.assertNotIn('    kinds:', content)
                self.fixtures.validate(label, content, 'arch.schema.json')


if __name__ == '__main__':
    unittest.main()
