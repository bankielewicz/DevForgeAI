"""REV-001..003: independent custody and failure-output expectations."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import test_publication as fixture


class StageIntegrityTests(fixture.PublicationTests):
    def receipt(self):
        path = self.run / 'stage-integrity.json'
        self.assertTrue(path.is_file(), 'STAGED must include original-mode/origin receipt')
        return path, json.loads(path.read_bytes())

    def test_receipt_binds_original_design_and_origin(self):
        self.stage()
        path, receipt = self.receipt()
        self.assertEqual({'schema_version', 'run_id', 'target_name', 'origin_ref',
                          'design_capture_requested'}, set(receipt))
        self.assertEqual('authoring-stage-integrity-v1', receipt['schema_version'])
        self.assertEqual('one', receipt['run_id'])
        self.assertEqual('brief-note', receipt['target_name'])
        self.assertIs(True, receipt['design_capture_requested'])
        self.assertEqual(fixture.ref(self.run / 'origin.json'), receipt['origin_ref'])

    def test_fresh_no_design_receipt_preserves_design_shaped_ordinary_input(self):
        self.stage(design=False)
        _, receipt = self.receipt()
        self.assertIs(False, receipt['design_capture_requested'])
        self.assertEqual('AUTHORED', fixture.authoring.publish(self.run)['state'])

    def test_old_canonical_no_marker_no_design_stage_is_compatible(self):
        self.contract['inputs'] = [fixture.ref(self.source)]
        self.stage(design=False)
        path, _ = self.receipt()
        path.rename(self.run / 'retained-new-receipt.json')
        origin = json.loads((self.run / 'origin.json').read_bytes())
        origin.pop('design_capture_requested')
        fixture.write_json(self.run / 'origin.json', origin)
        self.assertEqual('AUTHORED', fixture.authoring.publish(self.run)['state'])

    def test_pre_revision_marker_without_receipt_requires_fresh_run(self):
        self.stage(design=False)
        path, _ = self.receipt()
        path.rename(self.run / 'removed-receipt.json')
        result = fixture.authoring.publish(self.run)
        self.assertEqual('BLOCKED', result['state'])
        self.assertIn('fresh', str(result).lower())
        self.assertFalse(self.target.exists())

    def test_origin_deleted_blocks_with_recorded_failure(self):
        self.stage()
        (self.run / 'origin.json').rename(self.run / 'removed-origin.json')
        result = fixture.authoring.publish(self.run)
        self.assertEqual('BLOCKED', result['state'])
        self.assertFalse(self.target.exists())
        self.assertTrue((self.run / 'publication-failure.json').exists())

    def test_origin_malformed_blocks_with_recorded_failure(self):
        self.stage()
        (self.run / 'origin.json').write_bytes(b'[]')
        result = fixture.authoring.publish(self.run)
        self.assertEqual('BLOCKED', result['state'])
        self.assertFalse(self.target.exists())

    def test_failed_stage_cannot_be_reused_after_receipt_restoration(self):
        self.stage()
        path, receipt = self.receipt()
        path.rename(self.run / 'removed-receipt.json')
        self.assertEqual('BLOCKED', fixture.authoring.publish(self.run)['state'])
        fixture.write_json(path, receipt)
        with self.assertRaisesRegex(ValueError, 'already attempted'):
            fixture.authoring.publish(self.run)
        self.assertFalse(self.target.exists())

    def test_receipt_failure_during_begin_never_returns_staged(self):
        fixture.write_json(self.contract_path, self.contract)
        real_save = fixture.authoring.save
        def fail_receipt(path, value):
            if path.name == 'stage-integrity.json':
                raise OSError('synthetic receipt write failure')
            return real_save(path, value)
        with patch.object(fixture.authoring, 'save', side_effect=fail_receipt):
            with self.assertRaises(OSError):
                fixture.authoring.begin(self.contract_path, self.run, design=self.design_path)
        self.assertTrue((self.run / 'capture-failure.json').is_file())
        self.assertFalse(self.target.exists())

    def test_drift_between_writes_retains_first_delta_without_baseline(self):
        self.contract['change_paths'].append('second.txt')
        self.stage()
        (self.run / 'candidate/second.txt').write_bytes(b'second')
        def change_after_first(path):
            if path == 'second.txt':
                origin = json.loads((self.run / 'origin.json').read_bytes())
                origin['design_capture_requested'] = False
                origin.pop('design_capture_ref')
                fixture.write_json(self.run / 'origin.json', origin)
                (self.run / 'design-capture.json').rename(self.run / 'removed-capture.json')
        result = fixture.authoring.publish(self.run, before_write=change_after_first)
        self.assertEqual('PARTIAL', result['state'], result)
        self.assertEqual(['SKILL.md'], result['applied_paths'])
        self.assertEqual(self.content, (self.target / 'SKILL.md').read_bytes())
        self.assertFalse((self.target / 'second.txt').exists())
        self.assertFalse((self.run / 'authoring-baseline.json').exists())
        self.assertFalse((self.run / 'publication-readback.json').exists())

    def test_drift_after_delivery_cannot_publish_success(self):
        self.stage()
        real_copy = fixture.authoring.copy_files
        def drift_at_baseline(data, root):
            result = real_copy(data, root)
            if root.name == 'baseline':
                path, receipt = self.receipt()
                receipt['run_id'] = 'different-run'
                fixture.write_json(path, receipt)
            return result
        with patch.object(fixture.authoring, 'copy_files', side_effect=drift_at_baseline):
            result = fixture.authoring.publish(self.run)
        self.assertEqual('PARTIAL', result['state'], result)
        self.assertFalse((self.run / 'publication-readback.json').exists())
        self.assertFalse((self.run / 'authoring-baseline.json').exists())
        self.assertEqual(self.content, (self.target / 'SKILL.md').read_bytes())


def malformed_case(kind):
    def test(self):
        self.stage()
        path, receipt = self.receipt()
        if kind == 'deleted':
            path.rename(self.run / 'removed-receipt.json')
        elif kind == 'invalid_json':
            path.write_bytes(b'{broken')
        elif kind == 'duplicate_key':
            path.write_bytes(b'{"run_id":"one","run_id":"one"}')
        else:
            if kind == 'run_id': receipt['run_id'] = 'other'
            elif kind == 'target_name': receipt['target_name'] = 'other'
            elif kind == 'mode': receipt['design_capture_requested'] = False
            elif kind == 'mode_integer': receipt['design_capture_requested'] = 1
            elif kind == 'hash': receipt['origin_ref']['sha256'] = '0' * 64
            elif kind == 'path': receipt['origin_ref']['path'] = str(self.contract_path)
            elif kind == 'version': receipt['schema_version'] = 'unknown'
            elif kind == 'extra_field': receipt['extra'] = 'not allowed'
            elif kind == 'missing_field': receipt.pop('origin_ref')
            fixture.write_json(path, receipt)
        self.blocked()
    return test


for name in ['deleted', 'invalid_json', 'duplicate_key', 'run_id', 'target_name', 'mode',
             'mode_integer', 'hash', 'path', 'version', 'extra_field', 'missing_field']:
    setattr(StageIntegrityTests, 'test_receipt_' + name + '_blocks', malformed_case(name))


if __name__ == '__main__':
    unittest.main(verbosity=2)
