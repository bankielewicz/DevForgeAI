"""Behavioral custody and handoff regressions; no wording-matching assertions."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[5] / 'src/agents/skills/skill-validator'
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

    def test_linux_literal_path_spellings_round_trip_to_intake(self):
        for spelling in ('native', 'forward'):
            with self.subTest(spelling=spelling):
                self.target = self.project / ('literal Ω [path] $ ' + spelling) / 'brief-note'
                c = self.contract()
                if spelling == 'forward':
                    c['project_root'] = self.project.as_posix()
                    c['target_root'] = self.target.as_posix()
                elif spelling == 'mixed':
                    c['target_root'] = str(self.target.parent) + '/brief-note'
                run = self.begin(c)
                (run / 'candidate/SKILL.md').write_text('Literal path fixture')
                self.assertEqual('AUTHORED', a.publish(run)['state'])
                packet = run / 'validation-request.json'
                self.assertEqual('BOUND', intake.intake(packet, a.digest(packet.read_bytes()))['status'])
                self.assertTrue((self.target / 'SKILL.md').is_file())

    def test_effective_contract_preserves_original_selection(self):
        c = self.contract()
        c['target_root'] = self.target.as_posix()
        c['project_root'] = self.project.as_posix()
        run = self.begin(c)
        supplied = self.project / ('contract-' + c['run_id'] + '.json')
        self.assertEqual(supplied.read_bytes(), (run / 'supplied-contract.json').read_bytes())
        effective = json.loads((run / 'contract.json').read_bytes())
        self.assertEqual(str(self.target), effective['target_root'])
        self.assertEqual(str(self.project), effective['project_root'])
        resolution = json.loads((run / 'contract-paths.json').read_bytes())
        self.assertEqual(c['target_root'], resolution['target_root']['supplied'])
        self.assertEqual(str(self.target), resolution['target_root']['resolved'])

    def test_contract_source_drift_blocks_before_target_creation(self):
        c = self.contract()
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_text('Candidate')
        supplied = self.project / ('contract-' + c['run_id'] + '.json')
        supplied.write_bytes(supplied.read_bytes() + b' ')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse(self.target.exists())

    def test_effective_contract_tamper_blocks_before_target_creation(self):
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('Candidate')
        p = run / 'contract.json'
        p.write_bytes(p.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'captured contract changed'):
            a.publish(run)
        self.assertFalse(self.target.exists())

    def test_original_contract_snapshot_tamper_blocks_publication(self):
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('Candidate')
        p = run / 'supplied-contract.json'
        p.write_bytes(p.read_bytes() + b' ')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse(self.target.exists())

    def test_path_resolution_tamper_blocks_publication(self):
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('Candidate')
        p = run / 'contract-paths.json'
        p.write_bytes(p.read_bytes() + b' ')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse(self.target.exists())

    def test_linux_changed_stage_requires_fresh_run(self):
        c = self.contract()
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_text('Candidate')
        c['target_root'] = self.target.as_posix()
        raw = json.dumps(c).encode()
        (run / 'contract.json').write_bytes(raw)
        origin = json.loads((run / 'origin.json').read_bytes())
        origin['contract_sha256'] = a.digest(raw)
        for key in ('supplied_contract_sha256', 'path_resolution_sha256'):
            origin.pop(key, None)
        (run / 'origin.json').write_text(json.dumps(origin))
        result = a.publish(run)
        self.assertEqual('BLOCKED', result['state'])
        self.assertIn('fresh', json.dumps(result))
        self.assertFalse(self.target.exists())
        self.assertEqual(raw, (run / 'contract.json').read_bytes())

    def test_forward_slash_edit_preserves_authored_history(self):
        previous = self.create()
        c = self.contract('edit', prior=previous / 'authoring-baseline.json')
        c['target_root'] = self.target.as_posix()
        c['project_root'] = self.project.as_posix()
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_text('Revised fixture')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        p = run / 'validation-request.json'
        self.assertEqual('BOUND', intake.intake(p, a.digest(p.read_bytes()))['status'])
        self.assertEqual('authored', json.loads((run / 'origin.json').read_bytes())['prior_origin']['kind'])

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

    def test_incomplete_legacy_claim_not_a_baseline(self):
        previous = self.project / 'old'
        previous.mkdir()
        (previous / 'baseline').mkdir()
        (previous / 'baseline/SKILL.md').write_bytes(b'old generated')
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'old generated')
        p = previous / 'provenance.json'
        a.save(p, {'schema_version':'1','result':'COMPLETE','target_name':'brief-note','outputs':[{'path':'SKILL.md','ownership':'generated','baseline_path':'baseline/SKILL.md','baseline_sha256':a.digest(b'old generated')}]})
        with self.assertRaises(ValueError):
            self.begin(self.contract('edit', prior=p))

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

    def test_verified_schema1_legacy_origin(self):
        from fixture_data import build_candidate
        import shutil
        root = self.project / 'legacy'
        build_candidate(root, '0' * 64)
        self.target = self.target.parent / 'synthetic-total'
        shutil.copytree(root / 'trace/destination', self.target)
        c = self.contract('edit', prior=root / 'trace/evidence/build-provenance.json')
        c['target_name'] = 'synthetic-total'
        c['legacy_root'] = str(root)
        # Historical unrelated excluded test directories are not provenance inputs.
        (root / 'backup-test-artifacts').mkdir()
        (root / 'backup-test-artifacts/unrelated').write_bytes(b'do not traverse')
        run = self.begin(c)
        original = (run / 'candidate/SKILL.md').read_bytes()
        (run / 'candidate/SKILL.md').write_bytes(original + b'\nA narrow addition.\n')
        self.assertEqual('AUTHORED', a.publish(run)['state'])

    def test_verified_legacy_adoption_origin(self):
        from adoption_fixture import build_adoption
        import shutil
        root = self.project / 'legacy'
        record = build_adoption(root)
        self.target = Path(record['target_root'])
        shutil.copytree(root / 'adoption/destination', self.target)
        c = self.contract('edit', prior=root / 'adoption/evidence/pointer.json')
        c['target_name'] = 'synthetic-total'
        c['legacy_root'] = str(root)
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_bytes(b'Now authored from observed adopted base.')
        self.assertEqual('AUTHORED', a.publish(run)['state'])

    def test_metadata_explicit_policy_change(self):
        import yaml
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('---\nname: brief-note\ndescription: Brief supplied notes\n---\n')
        result = subprocess.run([sys.executable, '-B', str(BUILDER / 'scripts/generate_openai_yaml.py'), str(self.target), '--allow-implicit-invocation', 'false', '--interface', 'default_prompt=Use $brief-note to summarize my notes.'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        value = yaml.safe_load((self.target / 'agents/openai.yaml').read_text())
        self.assertFalse(value['policy']['allow_implicit_invocation'])
        self.assertEqual('Use $brief-note to summarize my notes.', value['interface']['default_prompt'])

    def test_original_input_drift_blocks_publication(self):
        p = self.project / 'request.txt'
        p.write_text('Summarize supplied notes.')
        c = self.contract()
        c['inputs'] = [a.reference(p)]
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_text('Candidate')
        p.write_text('Changed input')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertFalse(self.target.exists())

    def test_failed_publication_cannot_be_reused(self):
        from unittest.mock import patch
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('Candidate')
        original = a.save
        def fail(path, value):
            if path.name == 'publication-readback.json':
                raise OSError('publication interrupted')
            return original(path, value)
        with patch.object(a, 'save', fail):
            result = a.publish(run)
        self.assertEqual('PARTIAL', result['state'])
        self.assertTrue((run / 'publication-failure.json').exists())
        with self.assertRaisesRegex(ValueError, 'failed baseline publication'):
            self.begin(self.contract('edit', prior=run / 'authoring-baseline.json'))

    def test_protected_path_and_traversal_rejected(self):
        c = self.contract()
        c['target_root'] = str(self.project / '.agents/skills/brief-note')
        with self.assertRaises(ValueError):
            self.begin(c)
        c = self.contract(paths=['../outside'])
        with self.assertRaises(ValueError):
            self.begin(c)

    def test_new_record_schemas_match_actual_outputs(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest('optional installed jsonschema unavailable; no installation')
        run = self.create()
        for filename, schema_name in [('contract.json','authoring-contract'),('authoring-record.json','authoring-record'),('authoring-baseline.json','authoring-baseline'),('validation-request.json','validation-request')]:
            value = json.loads((run / filename).read_text())
            schema = json.loads((PACKAGE / 'schemas' / (schema_name + '.schema.json')).read_text())
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.validate(value,schema)
            value['schema_version'] = 'not-the-same-family'
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(value,schema)

    def test_existing_64_character_identity_is_preserved(self):
        name = 'n' * 64
        self.target = self.target.parent / name
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('Existing valid identity')
        c = self.contract('edit')
        c['target_name'] = name
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_text('Requested edit')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        self.assertEqual(name, a.read_record(run / 'authoring-record.json')['target_name'])

    def test_malformed_contract_rejected_before_writes(self):
        for key in ('known_issues','inputs','change_paths','requirements','capabilities','expected_outputs','side_effects'):
            with self.subTest(key=key):
                c = self.contract()
                c[key] = None
                with self.assertRaisesRegex(ValueError, r'\$\.' + key + ': wrong type'):
                    self.begin(c)
                self.assertFalse(self.target.exists())
                self.assertFalse((self.project / 'docs/plan' / c['run_id']).exists())

    def test_record_write_failure_retains_partial_delta(self):
        from unittest.mock import patch
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_text('Candidate')
        original = a.save
        def fail(path, value):
            if path.name == 'authoring-record.json':
                raise OSError('record publication failed')
            return original(path, value)
        with patch.object(a, 'save', fail):
            result = a.publish(run)
        self.assertEqual('PARTIAL', result['state'])
        self.assertEqual(['SKILL.md'], result['applied_paths'])
        self.assertTrue((run / 'publication-failure.json').exists())
        self.assertFalse((run / 'authoring-baseline.json').exists())

if __name__ == '__main__':
    unittest.main()
