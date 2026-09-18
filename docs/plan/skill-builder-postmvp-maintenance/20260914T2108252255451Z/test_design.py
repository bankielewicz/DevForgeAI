"""Requirement-derived custody fixtures; no generated skill is executed."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
BUILDER = ROOT / 'src/agents/skills/skill-builder'
sys.path.insert(0, str(BUILDER / 'scripts'))
import authoring as a


class DesignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='design space Ω ')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.target = self.project / 'custom skills/brief-note'
        self.run = self.project / 'docs/plan/one'
        self.source = self.project / 'request Ω.txt'
        self.source.write_bytes(b'R1: Return the supplied note without changing its facts.')
        self.design_path = self.project / 'design Ω.json'
        self.contract_path = self.project / 'contract.json'
        self.design = {
            'schema_version': 'authoring-design-v1', 'target_name': 'brief-note',
            'source_refs': [a.reference(self.source)],
            'behaviors': [{'id': 'B1', 'requirement_ids': ['request:R1'],
                'trigger': 'User supplies a note', 'inputs': ['Supplied text'],
                'completion': 'User receives text preserving the supplied facts',
                'outputs': ['Text in the response; no file destination'],
                'resource_paths': ['SKILL.md'], 'prerequisites': [], 'effects': [],
                'failure': 'Ask for absent note', 'recovery': 'Resume after user supplies note'}],
            'resources': [{'path': 'SKILL.md', 'kind': 'instruction',
                'purpose': 'Return the note', 'load_when': 'On invocation', 'helper_contract': None}],
            'adverse_conditions': [], 'execution_limits': [], 'open_questions': []}
        self.contract = {'schema_version': 'authoring-contract-v1', 'run_id': 'one',
            'project_root': str(self.project), 'target_root': str(self.target),
            'target_name': 'brief-note', 'operation': 'create',
            'authorization': 'Create the selected local fixture.',
            'history_review': 'no_known_history', 'change_paths': ['SKILL.md'],
            'requirements': [{'origin': 'user', 'outcome': 'Preserve note facts'}],
            'capabilities': [], 'expected_outputs': ['Response text'],
            'side_effects': [], 'inputs': [], 'known_issues': []}

    def write_inputs(self):
        self.design_path.write_text(json.dumps(self.design, ensure_ascii=False), encoding='utf-8')
        self.contract['inputs'] = [a.reference(self.source), a.reference(self.design_path)]
        self.contract_path.write_text(json.dumps(self.contract, ensure_ascii=False), encoding='utf-8')

    def stage(self):
        self.write_inputs()
        result = a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertEqual('STAGED', result['state'])
        (self.run / 'candidate/SKILL.md').write_bytes(b'---\nname: brief-note\ndescription: Return notes\n---\nPreserve supplied facts.\n')

    def test_cli_captures_selected_design(self):
        self.write_inputs()
        command = [sys.executable, '-B', '-X', 'utf8', str(BUILDER / 'scripts/authoring.py'), 'begin',
                   '--contract', str(self.contract_path), '--run-root', str(self.run),
                   '--design', str(self.design_path)]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=120)
        self.assertEqual(0, result.returncode, result.stderr)
        capture = a.parse((self.run / 'design-capture.json').read_bytes())
        self.assertEqual(a.reference(self.design_path), capture['source_ref'])
        self.assertEqual(self.design_path.read_bytes(), a.referenced(capture['snapshot_ref']))

    def test_capture_and_unchanged_validator_packet(self):
        self.stage()
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])
        capture = a.parse((self.run / 'design-capture.json').read_bytes())
        self.assertEqual(str(self.run / 'inputs/1'), capture['snapshot_ref']['path'])
        self.assertEqual(a.reference(self.run / 'design-capture.json'),
                         a.parse((self.run / 'origin.json').read_bytes())['design_capture_ref'])
        packet = a.parse((self.run / 'validation-request.json').read_bytes())
        schema = a.parse((BUILDER / 'schemas/validation-request.schema.json').read_bytes())
        a.record_schema.validate(packet, schema)
        self.assertEqual(self.contract['inputs'], packet['specification_refs'])
        self.assertEqual(self.contract_path.read_bytes(), (self.run / 'supplied-contract.json').read_bytes())
        sys.path.insert(0, str(ROOT / 'src/agents/skills/skill-validator/scripts'))
        import authoring_intake
        request = self.run / 'validation-request.json'
        self.assertEqual('BOUND', authoring_intake.intake(request, a.digest(request.read_bytes()))['status'])
        self.design_path.write_bytes(self.design_path.read_bytes() + b' ')
        with self.assertRaises(ValueError):
            authoring_intake.intake(request, a.digest(request.read_bytes()))

    def test_original_design_change_blocks(self):
        self.stage()
        self.design_path.write_bytes(self.design_path.read_bytes() + b' ')
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])
        self.assertFalse(self.target.exists())

    def test_snapshot_change_blocks(self):
        self.stage()
        (self.run / 'inputs/1').write_bytes(b'changed')
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])
        self.assertFalse((self.run / 'authoring-baseline.json').exists())

    def test_capture_change_blocks(self):
        self.stage()
        (self.run / 'design-capture.json').write_bytes(b'{}')
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])

    def test_removed_capture_and_origin_binding_cannot_downgrade(self):
        self.stage()
        (self.run / 'design-capture.json').unlink()
        origin = a.parse((self.run / 'origin.json').read_bytes())
        origin.pop('design_capture_ref')
        (self.run / 'origin.json').write_text(json.dumps(origin))
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])

    def test_invalid_internal_capture_mode_blocks(self):
        self.stage()
        path = self.run / 'origin.json'
        origin = a.parse(path.read_bytes())
        origin['design_capture_requested'] = 'yes'
        path.write_text(json.dumps(origin))
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])

    def test_false_mode_with_capture_blocks(self):
        self.stage()
        path = self.run / 'origin.json'
        origin = a.parse(path.read_bytes())
        origin['design_capture_requested'] = False
        path.write_text(json.dumps(origin))
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])

    def test_old_stage_without_mode_remains_publishable(self):
        self.contract_path.write_text(json.dumps(self.contract))
        a.begin(self.contract_path, self.run)
        path = self.run / 'origin.json'
        origin = a.parse(path.read_bytes())
        origin.pop('design_capture_requested')
        path.write_text(json.dumps(origin))
        (self.run / 'candidate/SKILL.md').write_bytes(b'legacy')
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])

    def test_capture_failure_cannot_publish(self):
        self.write_inputs()
        original = a.save
        def saving(path, value):
            if path.name == 'design-capture.json':
                raise OSError('injected capture write failure')
            return original(path, value)
        with patch.object(a, 'save', saving), self.assertRaises(OSError):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertTrue((self.run / 'capture-failure.json').exists())
        with self.assertRaises(ValueError):
            a.publish(self.run)
        self.assertFalse(self.target.exists())

    def test_design_drift_after_write_retains_partial(self):
        self.stage()
        def interrupt(path):
            (self.run / 'inputs/1').write_bytes(b'changed')
        result = a.publish(self.run, before_write=interrupt)
        self.assertEqual('PARTIAL', result['state'])
        self.assertEqual(['SKILL.md'], result['applied_paths'])
        self.assertTrue((self.target / 'SKILL.md').exists())
        self.assertFalse((self.run / 'authoring-baseline.json').exists())

    def test_invalid_target_rejected_before_capture(self):
        self.design['target_name'] = 'wrong'
        self.write_inputs()
        with self.assertRaises(ValueError):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())

    def test_legacy_begin_publish_unchanged(self):
        self.contract_path.write_text(json.dumps(self.contract))
        a.begin(self.contract_path, self.run)
        (self.run / 'candidate/SKILL.md').write_bytes(b'legacy')
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])
        self.assertFalse((self.run / 'design-capture.json').exists())

    def test_legacy_call_can_carry_design_as_ordinary_input(self):
        self.write_inputs()
        a.begin(self.contract_path, self.run)
        (self.run / 'candidate/SKILL.md').write_bytes(b'legacy input selection')
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])
        self.assertFalse((self.run / 'design-capture.json').exists())

    def test_relative_cli_arguments(self):
        self.write_inputs()
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8',
            str(BUILDER / 'scripts/authoring.py'), 'begin', '--contract', 'contract.json',
            '--run-root', 'docs/plan/one', '--design', self.design_path.name],
            cwd=self.project, capture_output=True, text=True, encoding='utf-8', timeout=120)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(a.reference(self.design_path),
            a.parse((self.run / 'design-capture.json').read_bytes())['source_ref'])

    def test_helper_contract_and_questions_in_handoff(self):
        self.design['resources'].append({'path': 'scripts/repeat.py', 'kind': 'helper',
            'purpose': 'Repeated deterministic note transformation', 'load_when': 'When transforming batches',
            'helper_contract': {'inputs': 'UTF-8 text', 'outputs': 'Response text', 'runtime': 'Python 3.10+',
                'effects': 'Read only', 'errors': 'Exit 2 for malformed input', 'reuse_reason': 'Batch transformation'}})
        self.design['open_questions'] = [{'id': 'Q1', 'question': 'Which optional batch output order?',
            'owner': 'User', 'affected_behavior_ids': ['B1']}]
        self.design['adverse_conditions'] = [{'id': 'A1', 'behavior_id': 'B1', 'condition': 'Absent note',
            'expected_observation': 'Request note', 'requirement_basis': 'request:R1'}]
        self.design['execution_limits'] = [{'behavior_id': 'B1', 'seconds': 30,
            'kind': 'execution_ceiling', 'source_basis': 'Selected disposable trial budget'}]
        self.stage()
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])
        prompt = (self.run / 'validator-request.md').read_text(encoding='utf-8')
        for fact in (str(self.design_path), a.reference(self.design_path)['sha256'], str(self.source),
                     'scripts/repeat.py', 'Which optional batch output order?'):
            self.assertIn(fact if fact not in (str(self.design_path), str(self.source)) else
                          json.dumps(fact, ensure_ascii=False)[1:-1], prompt)

    def test_origin_drift_during_publication(self):
        self.stage()
        def drift(path):
            origin = a.parse((self.run / 'origin.json').read_bytes())
            origin['extra'] = True
            (self.run / 'origin.json').write_text(json.dumps(origin))
        result = a.publish(self.run, before_write=drift)
        self.assertEqual('PARTIAL', result['state'])
        self.assertFalse((self.run / 'authoring-baseline.json').exists())

    def test_input_count_ceiling_rejected_before_capture(self):
        self.write_inputs()
        self.contract['inputs'].extend([a.reference(self.source)] * 1999)
        self.contract_path.write_text(json.dumps(self.contract))
        with self.assertRaisesRegex(ValueError, 'capture ceiling'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())

    def test_input_bytes_ceiling_rejected_before_capture(self):
        self.source.write_bytes(b'x' * (17 * 1024 * 1024))
        self.design['source_refs'] = [a.reference(self.source)]
        self.write_inputs()
        self.contract['inputs'].append(a.reference(self.source))
        self.contract_path.write_text(json.dumps(self.contract))
        with self.assertRaisesRegex(ValueError, 'capture ceiling'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())

    def test_unbound_design_rejected(self):
        self.write_inputs()
        self.contract['inputs'].pop()
        self.contract_path.write_text(json.dumps(self.contract))
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())

    def test_duplicate_design_binding_rejected(self):
        self.write_inputs()
        self.contract['inputs'].append(a.reference(self.design_path))
        self.contract_path.write_text(json.dumps(self.contract))
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            a.begin(self.contract_path, self.run, design=self.design_path)

    def test_source_design_inside_target_rejected(self):
        self.target.mkdir(parents=True)
        self.contract['operation'] = 'edit'
        self.design_path = self.target / 'design.json'
        self.write_inputs()
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            a.begin(self.contract_path, self.run, design=self.design_path)

    def test_design_inside_run_rejected(self):
        self.run.mkdir(parents=True)
        self.design_path = self.run / 'design.json'
        self.write_inputs()
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse((self.run / 'contract.json').exists())

    def test_design_link_rejected(self):
        self.write_inputs()
        alias = self.project / 'linked'
        # Windows directory junctions do not require symbolic-link privileges.
        if os.name == 'nt':
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            command = 'New-Item -ItemType Junction -Path ' + quote(alias) + ' -Target ' + quote(self.project)
            result = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command',
                command],
                capture_output=True, text=True, timeout=120)
            # Avoid a loop for fixture cleanup: remove the junction itself only.
            if result.returncode != 0:
                self.fail('Junction fixture setup failed: ' + result.stderr)
        else:
            alias.symlink_to(self.project, target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError, 'link/junction'):
                a.begin(self.contract_path, self.run, design=alias / self.design_path.name)
        finally:
            if os.name == 'nt':
                os.rmdir(alias)
            else:
                alias.unlink()

    def test_duplicate_json_keys_rejected(self):
        self.write_inputs()
        raw = self.design_path.read_text(encoding='utf-8')
        self.design_path.write_text(raw.replace('"target_name":', '"target_name": "brief-note", "target_name":'), encoding='utf-8')
        self.contract['inputs'][1] = a.reference(self.design_path)
        self.contract_path.write_text(json.dumps(self.contract))
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())

    def test_nonfinite_json_rejected(self):
        for token in ('NaN', 'Infinity', '-Infinity', '1e999'):
            with self.subTest(token=token):
                self.write_inputs()
                raw = self.design_path.read_text(encoding='utf-8')
                self.design_path.write_text(raw.replace('"open_questions": []', '"open_questions": ' + token), encoding='utf-8')
                self.contract['inputs'][1] = a.reference(self.design_path)
                self.contract_path.write_text(json.dumps(self.contract))
                with self.assertRaises(ValueError):
                    a.begin(self.contract_path, self.run, design=self.design_path)
                self.assertFalse(self.run.exists())

    def test_capture_readback_corruption_retained(self):
        self.write_inputs()
        original = a.read_bytes
        def reading(path):
            value = original(path)
            return value + b' ' if path == self.run / 'inputs/1' else value
        with patch.object(a, 'read_bytes', reading), self.assertRaisesRegex(ValueError, 'input snapshot readback'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertTrue((self.run / 'capture-failure.json').exists())

    def test_origin_readback_corruption_retained(self):
        self.write_inputs()
        original = a.save
        def saving(path, value):
            original(path, value)
            if path.name == 'origin.json':
                path.write_bytes(b'{}')
        with patch.object(a, 'save', saving), self.assertRaisesRegex(ValueError, 'origin capture readback'):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertTrue((self.run / 'capture-failure.json').exists())

    def test_handoff_write_corruption_prevents_baseline_reuse(self):
        self.stage()
        original = Path.write_text
        def writing(path, text, *args, **kwargs):
            return original(path, text + 'corrupted' if path.name == 'validator-request.md' else text, *args, **kwargs)
        with patch.object(Path, 'write_text', writing):
            self.assertEqual('PARTIAL', a.publish(self.run)['state'])
        self.assertTrue((self.run / 'publication-failure.json').exists())
        self.assertFalse((self.run / 'publication-readback.json').exists())
        next_contract = dict(self.contract, prior=a.reference(self.run / 'authoring-baseline.json'))
        with self.assertRaisesRegex(ValueError, 'failed baseline publication'):
            a.origin(next_contract)

    def test_unchanged_source_report_is_explicit(self):
        self.stage()
        self.assertEqual('AUTHORED', a.publish(self.run)['state'])
        self.contract.update(operation='edit', run_id='two',
            prior=a.reference(self.run / 'authoring-baseline.json'), history_review='selected authored prior')
        # Preserve the previous input contract as part of its completed custody.
        self.contract_path = self.project / 'contract-two.json'
        self.run = self.project / 'docs/plan/two'
        self.stage()
        result = a.publish(self.run)
        self.assertEqual('AUTHORED', result['state'])
        self.assertEqual([], result['applied_paths'])
        prompt = (self.run / 'validator-request.md').read_text(encoding='utf-8')
        self.assertIn('Source action: unchanged.', prompt)


def corrupt_capture_test(change):
    def test(self):
        self.stage()
        capture_path = self.run / 'design-capture.json'
        value = a.parse(capture_path.read_bytes())
        change(value)
        capture_path.write_text(json.dumps(value))
        origin_path = self.run / 'origin.json'
        origin = a.parse(origin_path.read_bytes())
        origin['design_capture_ref'] = a.reference(capture_path)
        origin_path.write_text(json.dumps(origin))
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])
        self.assertFalse(self.target.exists())
    return test

for name, change in {
    'unknown_field': lambda c: c.update(extra=True),
    'wrong_run': lambda c: c.update(run_id='two'),
    'wrong_target': lambda c: c.update(target_name='other'),
    'wrong_snapshot': lambda c: c['snapshot_ref'].update(sha256='0' * 64),
    'wrong_original': lambda c: c['source_ref'].update(sha256='0' * 64),
}.items():
    setattr(DesignTests, 'test_rebound_capture_' + name, corrupt_capture_test(change))


def invalid_design_test(mutate):
    def test(self):
        mutate(self.design)
        self.write_inputs()
        with self.assertRaises(ValueError):
            a.begin(self.contract_path, self.run, design=self.design_path)
        self.assertFalse(self.run.exists())
        self.assertFalse(self.target.exists())
    return test


INVALID = {
    'unknown_top_field': lambda d: d.update(extra=True),
    'unknown_behavior_field': lambda d: d['behaviors'][0].update(extra=True),
    'empty_behaviors': lambda d: d.update(behaviors=[]),
    'duplicate_behavior_id': lambda d: d['behaviors'].append(copy.deepcopy(d['behaviors'][0])),
    'duplicate_resource': lambda d: d['resources'].append(copy.deepcopy(d['resources'][0])),
    'blank_completion': lambda d: d['behaviors'][0].update(completion='  '),
    'blank_requirement_id': lambda d: d['behaviors'][0].update(requirement_ids=['']),
    'empty_requirement_ids': lambda d: d['behaviors'][0].update(requirement_ids=[]),
    'unresolved_resource': lambda d: d['behaviors'][0].update(resource_paths=['missing.md']),
    'traversal_resource': lambda d: d['resources'][0].update(path='../outside'),
    'absolute_resource': lambda d: d['resources'][0].update(path='/outside'),
    'backslash_resource': lambda d: d['resources'][0].update(path='references\\x.md'),
    'drive_resource': lambda d: d['resources'][0].update(path='C:/outside'),
    'excluded_resource': lambda d: d['resources'][0].update(path='backups/secret'),
    'missing_helper_contract': lambda d: d['resources'][0].update(kind='helper'),
    'nonhelper_with_contract': lambda d: d['resources'][0].update(helper_contract={k: 'x' for k in ('inputs', 'outputs', 'runtime', 'effects', 'errors', 'reuse_reason')}),
    'unbound_source': lambda d: d['source_refs'][0].update(sha256='0' * 64),
    'unknown_adverse_behavior': lambda d: d.update(adverse_conditions=[{'id': 'A1', 'behavior_id': 'B2', 'condition': 'Missing', 'expected_observation': 'Ask', 'requirement_basis': 'R1'}]),
    'unknown_question_behavior': lambda d: d.update(open_questions=[{'id': 'Q1', 'question': 'Why?', 'owner': 'User', 'affected_behavior_ids': ['B2']}]),
    'invalid_limit_kind': lambda d: d.update(execution_limits=[{'behavior_id': 'B1', 'seconds': 1, 'kind': 'universal', 'source_basis': 'R1'}]),
    'zero_seconds': lambda d: d.update(execution_limits=[{'behavior_id': 'B1', 'seconds': 0, 'kind': 'execution_ceiling', 'source_basis': 'R1'}]),
    'boolean_seconds': lambda d: d.update(execution_limits=[{'behavior_id': 'B1', 'seconds': True, 'kind': 'execution_ceiling', 'source_basis': 'R1'}]),
    'duplicate_question_id': lambda d: d.update(open_questions=[{'id': 'Q1', 'question': 'Why?', 'owner': 'User', 'affected_behavior_ids': ['B1']}] * 2),
    'duplicate_adverse_id': lambda d: d.update(adverse_conditions=[{'id': 'A1', 'behavior_id': 'B1', 'condition': 'Missing', 'expected_observation': 'Ask', 'requirement_basis': 'R1'}] * 2),
}
for name, mutation in INVALID.items():
    setattr(DesignTests, 'test_invalid_' + name, invalid_design_test(mutation))


def missing_evidence_test(relative_path):
    def test(self):
        self.stage()
        path = self.design_path if relative_path == 'original' else self.run / relative_path
        path.unlink()
        self.assertEqual('BLOCKED', a.publish(self.run)['state'])
        self.assertFalse(self.target.exists())
        self.assertFalse((self.run / 'authoring-baseline.json').exists())
    return test

for name, path in [('original', 'original'), ('snapshot', 'inputs/1'), ('capture', 'design-capture.json')]:
    setattr(DesignTests, 'test_missing_' + name, missing_evidence_test(path))


if __name__ == '__main__':
    unittest.main()
