"""Independent custody safeguards: real fixtures and injected I/O interruptions.

Fault injection models a competing writer or unavailable filesystem; it never
bypasses schema validation or supplies a synthetic passing custody decision.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import sys
import unittest
from unittest.mock import patch

import test_authoring as fixtures

a = fixtures.a


class AuthoringSafeguards(unittest.TestCase):
    setUp = fixtures.AuthoringTests.setUp
    contract = fixtures.AuthoringTests.contract
    begin = fixtures.AuthoringTests.begin
    create = fixtures.AuthoringTests.create

    def stage(self):
        run = self.begin(self.contract())
        (run / 'candidate/SKILL.md').write_bytes(b'candidate')
        return run

    def test_json_nonfinite_rejected(self):
        for text in ('NaN', 'Infinity', '1e999'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                a.parse(text)

    def test_path_and_reference_boundaries(self):
        for value in ('../escape', 'backup-archive/file', 'devforgeai_cli/file'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                a.safe(self.project / value)
        with self.assertRaises(ValueError):
            a.referenced({'path': 'incomplete'})
        with self.assertRaisesRegex(ValueError, 'package directory missing'):
            a.files(self.project / 'absent')
        with self.assertRaisesRegex(ValueError, 'bounded regular file'):
            a.read_bytes(self.project)

    def test_capture_actual_file_count_limit(self):
        root = self.project / 'bounded'
        root.mkdir()
        for i in range(2001):
            (root / str(i)).touch()
        with self.assertRaisesRegex(ValueError, 'capture ceiling'):
            a.files(root)

    def test_capture_actual_byte_limit(self):
        path = self.project / 'oversized'
        with path.open('wb') as stream:
            stream.truncate(32 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(ValueError, 'bounded regular file'):
            a.read_bytes(path)

    def test_read_detects_concurrent_size_change(self):
        path = self.project / 'source'
        path.write_bytes(b'old')
        original = Path.open
        def opening(p, *args, **kwargs):
            if p == path and args == ('rb',):
                with original(p, 'ab') as writer:
                    writer.write(b'new')
            return original(p, *args, **kwargs)
        with patch.object(Path, 'open', opening), self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED'):
            a.read_bytes(path)

    def test_snapshot_write_corruption_is_detected(self):
        original = a.files
        root = self.project / 'snapshot'
        def observed(p):
            if p == root:
                (p / 'SKILL.md').write_bytes(b'corrupted')
            return original(p)
        with patch.object(a, 'files', observed), self.assertRaisesRegex(ValueError, 'snapshot readback failed'):
            a.copy_files({'SKILL.md': b'expected'}, root)

    def test_record_families_reject_invalid_states(self):
        for i, value in enumerate((
                {'record_kind': 'authoring', 'schema_version': 'authoring-v1', 'authoring_state': 'COMPLETE'},
                {'record_kind': 'authoring_baseline', 'schema_version': '2'})):
            path = self.project / ('record' + str(i))
            a.save(path, value)
            with self.assertRaises(ValueError):
                a.read_record(path)
        run = self.create()
        self.assertEqual('authoring-baseline-v1', a.read_record(run / 'authoring-baseline.json')['schema_version'])

    def test_intake_location_and_identity_constraints(self):
        for change in ({'project_root': str(self.project / 'missing')},
                       {'target_root': str(self.project)},
                       {'target_name': 'incorrect'},
                       {'authorization': '   '},
                       {'operation': 'edit'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.begin(dict(self.contract(), **change))
        self.target.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'occupied destination'):
            self.begin(self.contract())

    def test_re_adoption_with_prior_rejected(self):
        prior = self.create()
        with self.assertRaisesRegex(ValueError, 'not re-adoption'):
            self.begin(self.contract('adopt', prior=prior / 'authoring-baseline.json'))

    def test_input_in_target_rejected(self):
        self.target.mkdir(parents=True)
        p = self.target / 'SKILL.md'
        p.write_bytes(b'original')
        c = self.contract('edit')
        c['inputs'] = [a.reference(p)]
        with self.assertRaisesRegex(ValueError, 'input overlaps'):
            self.begin(c)

    def test_capture_drift_preserves_failed_attempt(self):
        self.target.mkdir(parents=True)
        p = self.target / 'SKILL.md'
        p.write_bytes(b'original')
        original = a.copy_files
        def copying(data, root):
            original(data, root)
            if root.name == 'candidate':
                p.write_bytes(b'concurrent edit')
        c = self.contract('edit')
        with patch.object(a, 'copy_files', copying), self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED'):
            self.begin(c)
        run = self.project / 'docs/plan' / c['run_id']
        self.assertTrue((run / 'capture-failure.json').exists())
        self.assertEqual(b'original', (run / 'before/SKILL.md').read_bytes())

    def test_supplied_capture_corruption_retains_failure(self):
        original = Path.write_bytes
        def writing(p, data):
            return original(p, data + b' ' if p.name == 'supplied-contract.json' else data)
        c = self.contract()
        with patch.object(Path, 'write_bytes', writing), self.assertRaisesRegex(ValueError, 'capture readback'):
            self.begin(c)
        self.assertTrue((self.project / 'docs/plan' / c['run_id'] / 'capture-failure.json').exists())

    def test_attempt_cannot_publish_twice(self):
        run = self.create()
        with self.assertRaisesRegex(ValueError, 'already attempted'):
            a.publish(run)

    def test_captured_base_tampering_rejected(self):
        run = self.stage()
        (run / 'before/extra').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'captured edit base changed'):
            a.publish(run)
        self.assertFalse(self.target.exists())

    def test_authorized_deletion_records_delta(self):
        previous = self.create()
        run = self.begin(self.contract('edit', prior=previous / 'authoring-baseline.json'))
        (run / 'candidate/SKILL.md').unlink()
        result = a.publish(run)
        self.assertEqual('AUTHORED', result['state'])
        self.assertEqual(['SKILL.md'], result['applied_paths'])
        self.assertEqual({}, a.files(self.target))

    def test_keep_current_retains_user_change_and_generated_baseline(self):
        prior = self.create()
        old = (self.target / 'SKILL.md').read_bytes()
        (self.target / 'SKILL.md').write_bytes(b'user edit')
        run = self.begin(self.contract('edit', prior=prior / 'authoring-baseline.json'))
        (run / 'candidate/SKILL.md').write_bytes(old)
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        self.assertEqual(b'user edit', (self.target / 'SKILL.md').read_bytes())
        self.assertEqual(old, (run / 'baseline/SKILL.md').read_bytes())

    def test_out_of_scope_baseline_recovered_from_prior(self):
        prior = self.create()
        old = (self.target / 'SKILL.md').read_bytes()
        (self.target / 'SKILL.md').write_bytes(b'user change')
        run = self.begin(self.contract('edit', ['new.txt'], prior / 'authoring-baseline.json'))
        (run / 'candidate/new.txt').write_bytes(b'new')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        self.assertEqual(old, (run / 'baseline/SKILL.md').read_bytes())
        self.assertEqual(b'user change', (self.target / 'SKILL.md').read_bytes())

    def test_adoption_cannot_change_bytes(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'existing')
        run = self.begin(self.contract('adopt'))
        (run / 'candidate/SKILL.md').write_bytes(b'edited')
        self.assertEqual('BLOCKED', a.publish(run)['state'])
        self.assertEqual(b'existing', (self.target / 'SKILL.md').read_bytes())

    def test_per_path_concurrent_write_is_preserved(self):
        run = self.stage()
        def competing_writer(path):
            (self.target / path).write_bytes(b'other writer')
        result = a.publish(run, before_write=competing_writer)
        self.assertEqual('PARTIAL', result['state'])
        self.assertEqual([], result['applied_paths'])
        self.assertEqual(b'other writer', (self.target / 'SKILL.md').read_bytes())

    def publication_fault(self, trigger, mutate):
        run = self.stage()
        original = a.save
        def saving(path, value):
            original(path, value)
            if path.name == trigger:
                mutate(run)
        with patch.object(a, 'save', saving):
            result = a.publish(run)
        self.assertNotEqual('AUTHORED', result['state'])
        self.assertFalse((run / 'publication-readback.json').exists())
        return run, result

    def test_staging_changes_during_preflight_block_write(self):
        run, result = self.publication_fault('write-plan.json', lambda r: (r / 'candidate/SKILL.md').write_bytes(b'changed'))
        self.assertEqual('BLOCKED', result['state'])
        self.assertFalse(self.target.exists())

    def test_target_changes_at_first_write_check_block_write(self):
        def mutate(run):
            self.target.mkdir(parents=True)
            (self.target / 'SKILL.md').write_bytes(b'competing')
        _, result = self.publication_fault('write-plan.json', mutate)
        self.assertEqual('PARTIAL', result['state'])
        self.assertEqual([], result['applied_paths'])

    def test_target_changes_before_baseline_block_publication(self):
        run, result = self.publication_fault('authoring-record.json', lambda r: (self.target / 'SKILL.md').write_bytes(b'changed'))
        self.assertEqual('PARTIAL', result['state'])
        self.assertFalse((run / 'authoring-baseline.json').exists())

    def test_pointer_write_corruption_blocks_publication(self):
        _, result = self.publication_fault('authoring-baseline.json', lambda r: (r / 'authoring-baseline.json').write_text('{}'))
        self.assertEqual('PARTIAL', result['state'])

    def test_final_target_drift_blocks_publication(self):
        _, result = self.publication_fault('validation-request.json', lambda r: (self.target / 'SKILL.md').write_bytes(b'changed'))
        self.assertEqual('PARTIAL', result['state'])

    def test_double_evidence_write_failure_returns_actual_delta(self):
        run = self.stage()
        original = a.save
        def saving(path, value):
            if path.name in ('authoring-record.json', 'publication-failure.json'):
                raise OSError('disk unavailable')
            return original(path, value)
        with patch.object(a, 'save', saving):
            result = a.publish(run)
        self.assertEqual('PARTIAL', result['state'])
        self.assertTrue(result['evidence_write_failed'])
        self.assertEqual(['SKILL.md'], result['applied_paths'])

    def test_unreadable_after_interruption_reports_gap(self):
        run = self.stage()
        original = a.files
        unavailable = False
        def failing(p):
            if unavailable and p == self.target:
                raise OSError('destination unavailable')
            return original(p)
        def interrupt(path):
            nonlocal unavailable
            unavailable = True
            raise OSError('write interrupted')
        with patch.object(a, 'files', failing):
            result = a.publish(run, before_write=interrupt)
        self.assertEqual('BLOCKED', result['state'])
        self.assertTrue(any('after capture unavailable' in p for p in result['issues']))

    def test_delivered_corruption_never_creates_baseline(self):
        run = self.stage()
        original = a.files
        def observed(p):
            if p == self.target and (p / 'SKILL.md').exists():
                (p / 'SKILL.md').write_bytes(b'corrupted')
            return original(p)
        with patch.object(a, 'files', observed):
            result = a.publish(run)
        self.assertEqual('PARTIAL', result['state'])
        self.assertFalse((run / 'authoring-baseline.json').exists())

    def test_cli_begin_publish_read_and_invalid_input(self):
        c = self.contract()
        path = self.project / 'cli-contract.json'
        a.save(path, c)
        run = self.project / 'docs/plan/cli'
        def cli(args, expected):
            out, err = io.StringIO(), io.StringIO()
            with patch.object(sys, 'argv', ['authoring.py', *args]), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as status:
                    runpy.run_path(str(fixtures.BUILDER / 'scripts/authoring.py'), run_name='__main__')
            self.assertEqual(expected, status.exception.code, err.getvalue())
            return json.loads(out.getvalue() or err.getvalue())
        self.assertEqual('STAGED', cli(['begin', '--contract', str(path), '--run-root', str(run)], 0)['state'])
        (run / 'candidate/SKILL.md').write_bytes(b'CLI')
        self.assertEqual('AUTHORED', cli(['publish', '--run-root', str(run)], 0)['state'])
        self.assertEqual('AUTHORED', cli(['read', '--record', str(run / 'authoring-record.json')], 0)['authoring_state'])
        self.assertEqual('BLOCKED', cli(['read', '--record', str(self.project / 'missing')], 2)['state'])

    def legacy(self, version=1):
        from fixture_data import build_candidate
        from adoption_fixture import build_v2
        root = self.project / ('legacy' + str(version))
        (build_candidate if version == 1 else build_v2)(root, '0' * 64)
        self.target = self.target.parent / 'synthetic-total'
        shutil.copytree(root / 'trace/destination', self.target)
        p = root / 'trace/evidence/build-provenance.json'
        c = self.contract('edit', prior=p)
        c.update(target_name='synthetic-total', legacy_root=str(root))
        return root, p, c

    def test_verified_schema2_generated_legacy_origin(self):
        root, p, c = self.legacy(2)
        run = self.begin(c)
        (run / 'candidate/SKILL.md').write_bytes(b'new authored text')
        self.assertEqual('AUTHORED', a.publish(run)['state'])

    def test_legacy_out_of_scope_baseline_recovery(self):
        root, p, c = self.legacy()
        old = (self.target / 'SKILL.md').read_bytes()
        (self.target / 'SKILL.md').write_bytes(b'user modified')
        c['change_paths'] = ['extra.txt']
        run = self.begin(c)
        (run / 'candidate/extra.txt').write_bytes(b'extra')
        self.assertEqual('AUTHORED', a.publish(run)['state'])
        self.assertEqual(old, (run / 'baseline/SKILL.md').read_bytes())

    def test_legacy_wrong_identity_and_failed_history_rejected(self):
        root, p, c = self.legacy()
        bad = dict(c, target_name='brief-note', target_root=str(self.target.parent / 'brief-note'))
        with self.assertRaisesRegex(ValueError, 'legacy target mismatch'):
            a.origin(bad)
        value = json.loads(p.read_bytes())
        value['result'] = 'INCOMPLETE'
        p.write_text(json.dumps(value))
        c['prior'] = a.reference(p)
        with self.assertRaisesRegex(ValueError, 'unresolved or unsuccessful'):
            a.origin(c)


if __name__ == '__main__':
    unittest.main()
