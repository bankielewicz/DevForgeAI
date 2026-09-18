"""Behavioral custody and handoff regressions; no wording-matching assertions."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
BUILDER = Path(os.environ.get('AUTHORING_BUILDER_ROOT', PACKAGE.parent / 'skill-builder'))
sys.path.insert(0, str(BUILDER / 'scripts'))
sys.path.insert(0, str(PACKAGE / 'scripts'))
import authoring as a
import authoring_intake as intake

class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='authoring-')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.target = self.project / 'Custom skills with spaces/brief-note'
        self.counter = 0

    def contract(self, operation='create', paths=None, prior=None):
        self.counter += 1
        request = {'schema_version': 'authoring-contract-v1', 'run_id': str(self.counter), 'project_root': str(self.project), 'target_root': str(self.target), 'target_name': 'brief-note', 'operation': operation, 'authorization': 'Create or edit the selected synthetic briefing skill in the selected development destination.', 'history_review': 'no_known_history' if prior is None else 'selected verified prior', 'change_paths': paths or ['SKILL.md'], 'requirements': [{'origin':'user','outcome':'Summarize supplied notes in three bullets.'}], 'capabilities': [], 'expected_outputs': ['briefing text'], 'side_effects': [], 'inputs': [], 'known_issues': []}
        if prior:
            request['prior'] = a.reference(prior)
        return request

    def begin(self, c):
        p = self.project / ('contract-' + c['run_id'] + '.json')
        a.save(p, c)
        run = self.project / 'docs/plan' / c['run_id']
        a.begin(p, run)
        return run

    def create(self):
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('---\nname: brief-note\ndescription: Summarize supplied notes\n---\nReturn three bullets.\n')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        return run

    def test_conversation_create_portable_handoff(self):
        run = self.create()
        packet = run / 'validation-request.json'
        result = intake.intake(packet, a.digest(packet.read_bytes()))
        self.assertEqual('BOUND', result['status'])
        record = a.read_record(run / 'authoring-record.json')
        self.assertEqual('NOT_PERFORMED', record['testing_status'])
        self.assertEqual('observed', record['prior_origin']['kind'])
        self.assertEqual(str(self.target), json.loads(packet.read_text())['target_root'])

    def test_untested_revision(self):
        previous = self.create()
        run = self.begin(self.contract('edit', prior=previous / 'authoring-baseline.json'))
        (run / 'candidate/SKILL.md').write_text('New requested concise output.\n')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        record = a.read_record(run / 'authoring-record.json')
        self.assertEqual('authored', record['prior_origin']['kind'])
        self.assertEqual('NOT_PERFORMED', record['validation_status'])

    def test_observed_edit_preserves_unrelated(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'original')
        (self.target / 'domain.bin').write_bytes(b'\x00\xffUNCHANGED')
        run = self.begin(self.contract('edit'))
        (run / 'candidate/SKILL.md').write_bytes(b'edited')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        record = a.read_record(run / 'authoring-record.json')
        self.assertEqual(['SKILL.md'], record['managed_paths'])
        self.assertEqual(['domain.bin'], record['retained_user_paths'])
        self.assertEqual(b'\x00\xffUNCHANGED', (self.target / 'domain.bin').read_bytes())

    def test_unowned_collision(self):
        previous = self.create()
        (self.target / 'user.txt').write_bytes(b'user')
        run = self.begin(self.contract('edit', ['user.txt'], previous / 'authoring-baseline.json'))
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse((run / 'authoring-baseline.json').exists())

    def test_divergent_managed_conflict(self):
        previous = self.create()
        (self.target / 'SKILL.md').write_bytes(b'user changed')
        run = self.begin(self.contract('edit', prior=previous / 'authoring-baseline.json'))
        (run / 'candidate/SKILL.md').write_bytes(b'generated changed')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertEqual(b'user changed', (self.target / 'SKILL.md').read_bytes())

    def test_source_drift(self):
        run = self.create()
        later = self.begin(self.contract('edit', prior=run / 'authoring-baseline.json'))
        (self.target / 'SKILL.md').write_bytes(b'drift')
        self.assertIn(a.publish(later)['state'], ('PARTIAL', 'BLOCKED'))
        self.assertFalse((later / 'authoring-baseline.json').exists())

    def test_interrupted_write_retains_delta(self):
        c = self.contract(paths=['SKILL.md', 'z.txt'])
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_bytes(b'first')
        (run / 'candidate/z.txt').write_bytes(b'second')
        def fail(path):
            if path == 'z.txt':
                raise OSError('injected interruption')
        result = a.publish(run, before_write=fail)
        self.assertEqual('PARTIAL', result['state'])
        self.assertEqual(['SKILL.md'], result['applied_paths'])
        self.assertFalse((run / 'authoring-baseline.json').exists())

    def test_stale_request_rejected(self):
        run = self.create()
        p = run / 'validation-request.json'
        (self.target / 'SKILL.md').write_bytes(b'later bytes')
        with self.assertRaisesRegex(ValueError, 'STALE_REQUEST'):
            intake.intake(p, a.digest(p.read_bytes()))

    def test_tampered_authoring_record_rejected(self):
        run = self.create()
        p = run / 'validation-request.json'
        (run / 'authoring-record.json').write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError, 'STALE_REQUEST'):
            intake.intake(p, a.digest(p.read_bytes()))

    def test_known_failed_history_not_observed(self):
        c = self.contract()
        c['history_review'] = 'known missing origin'
        with self.assertRaisesRegex(ValueError, 'known history'):
            self.begin(c)

    def test_reject_occupied_initializer(self):
        self.target.mkdir(parents=True)
        (self.target / 'keep').write_bytes(b'existing')
        p = subprocess.run([sys.executable, '-B', str(BUILDER / 'scripts/init_skill.py'), 'brief-note', '--path', str(self.target.parent)], capture_output=True, text=True)
        self.assertNotEqual(0, p.returncode)
        self.assertEqual({'keep': b'existing'}, a.files(self.target))

    def test_new_initializer_and_metadata_preservation(self):
        import yaml
        p = subprocess.run([sys.executable, '-B', str(BUILDER / 'scripts/init_skill.py'), 'brief-note', '--path', str(self.target.parent)], capture_output=True, text=True)
        self.assertEqual(0, p.returncode, p.stderr)
        ui = self.target / 'agents/openai.yaml'
        ui.write_text('interface:\n  display_name: Old\n  short_description: A sufficiently long existing description\n  brand_color: "#123456"\npolicy:\n  allow_implicit_invocation: false\ndependencies:\n  tools: []\n')
        p = subprocess.run([sys.executable, '-B', str(BUILDER / 'scripts/generate_openai_yaml.py'), str(self.target), '--interface', 'display_name=Updated'], capture_output=True, text=True)
        self.assertEqual(0, p.returncode, p.stderr)
        value = yaml.safe_load(ui.read_text())
        self.assertEqual('Updated', value['interface']['display_name'])
        self.assertFalse(value['policy']['allow_implicit_invocation'])
        self.assertEqual('#123456', value['interface']['brand_color'])
        self.assertEqual({'tools': []}, value['dependencies'])

    def test_wrong_scope_rejected(self):
        run = self.begin(self.contract())
        (run / 'candidate/unapproved').write_bytes(b'no')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse(self.target.exists())

    def test_prior_baseline_bytes_tamper(self):
        run = self.create()
        (run / 'baseline/SKILL.md').write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'baseline snapshot changed'):
            self.begin(self.contract('edit', prior=run / 'authoring-baseline.json'))

    def test_unknown_version_and_duplicate_keys(self):
        p = self.project / 'bad.json'
        p.write_text('{"schema_version":"authoring-v2"}')
        with self.assertRaises(ValueError):
            a.read_record(p)
        with self.assertRaises(ValueError):
            a.parse('{"x":1,"x":2}')

    def test_legacy_meaning_preserved(self):
        for version in ('1', '2'):
            p = self.project / (version + '.json')
            a.save(p, {'schema_version': version, 'result': 'COMPLETE'})
            self.assertEqual('COMPLETE', a.read_record(p)['result'])

    def test_legacy_generated_baseline(self):
        previous = self.project / 'old'
        previous.mkdir()
        (previous / 'baseline').mkdir()
        (previous / 'baseline/SKILL.md').write_bytes(b'old generated')
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'old generated')
        p = previous / 'provenance.json'
        a.save(p, {'schema_version':'1','result':'COMPLETE','target_name':'brief-note','outputs':[{'path':'SKILL.md','ownership':'generated','baseline_path':'baseline/SKILL.md','baseline_sha256':a.digest(b'old generated')}]})
        run = self.begin(self.contract('edit', prior=p))
        (run / 'candidate/SKILL.md').write_bytes(b'new authored')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        self.assertEqual('legacy_generated', a.read_record(run / 'authoring-record.json')['prior_origin']['kind'])

    def test_explicit_adoption_is_distinct(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'existing')
        run = self.begin(self.contract('adopt'))
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        record = a.read_record(run / 'authoring-record.json')
        self.assertEqual('adopt', record['operation'])
        self.assertEqual([], record['applied_paths'])
        c = self.contract('edit', prior=run / 'authoring-baseline.json')
        later = self.begin(c)
        self.assertEqual('adopted', json.loads((later / 'origin.json').read_text())['prior_origin']['kind'])

if __name__ == '__main__':
    unittest.main()
