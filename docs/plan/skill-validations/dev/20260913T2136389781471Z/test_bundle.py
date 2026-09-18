"""Validator build-contract tests, not dev behavioral trials."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent
BUNDLE=ROOT/'bundle'
REQUIRED=('runner.py','graders.py','scenarios.jsonl','expected-results.json','evidence.schema.json','runtime.json','artifact-manifest.json')

class BundleContract(unittest.TestCase):
    def test_mandatory_artifacts_and_bindings(self):
        self.assertEqual([], [name for name in REQUIRED if not (BUNDLE/name).is_file()], 'DEV-026 requires an external executable bundle')
        manifest=json.loads((BUNDLE/'artifact-manifest.json').read_bytes())
        self.assertEqual('7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae',manifest['package_digest'])
        for row in manifest['artifacts']:
            self.assertEqual(row['sha256'],hashlib.sha256((BUNDLE/row['path']).read_bytes()).hexdigest())

    def test_required_cases_exact_once_and_predeclared(self):
        self.assertTrue((BUNDLE/'scenarios.jsonl').is_file(),'Required DV scenarios are missing')
        cases=[json.loads(line) for line in (BUNDLE/'scenarios.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual([f'DV-{i:02d}' for i in range(1,19)],[c['case_id'] for c in cases])
        self.assertTrue(all(c['expected'] and c['requirement_ids'] and c['fixture_refs'] and c['timeout_seconds']==120 for c in cases))

if __name__=='__main__':
    unittest.main()
