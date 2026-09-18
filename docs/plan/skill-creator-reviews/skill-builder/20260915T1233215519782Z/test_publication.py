"""Independent observable publication checks; fixtures and failed attempts retained."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(r'C:\Projects\DevForgeAI')
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src/agents/skills/skill-builder/scripts'))
import authoring


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def ref(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.project = Path(tempfile.mkdtemp(prefix='builder-review-'))
        with (RUN / 'fixture-paths.jsonl').open('a', encoding='utf-8') as out:
            out.write(json.dumps({'test': self.id(), 'project': str(self.project)}) + '\n')
        self.target = self.project / 'skills/brief-note'
        self.run = self.project / 'docs/plan/one'
        self.source = self.project / 'request.txt'
        self.source.write_text('Return supplied notes without inventing facts.', encoding='utf-8')
        self.design_path = self.project / 'design.json'
        design = {
            'schema_version': 'authoring-design-v1', 'target_name': 'brief-note',
            'source_refs': [ref(self.source)],
            'behaviors': [{'id': 'B1', 'requirement_ids': ['request.txt'],
                'trigger': 'Supplied note', 'inputs': ['Note text'],
                'completion': 'Return the supplied facts', 'outputs': ['Chat response'],
                'resource_paths': ['SKILL.md'], 'prerequisites': [], 'effects': [],
                'failure': 'Request missing note', 'recovery': 'Resume on receipt'}],
            'resources': [{'path': 'SKILL.md', 'kind': 'instruction', 'purpose': 'Preserve facts',
                'load_when': 'Invocation', 'helper_contract': None}],
            'adverse_conditions': [], 'execution_limits': [], 'open_questions': []}
        write_json(self.design_path, design)
        self.contract_path = self.project / 'contract.json'
        self.contract = {
            'schema_version': 'authoring-contract-v1', 'run_id': 'one',
            'project_root': str(self.project), 'target_root': str(self.target),
            'target_name': 'brief-note', 'operation': 'create',
            'authorization': 'Create this isolated review fixture.',
            'history_review': 'no_known_history', 'change_paths': ['SKILL.md'],
            'requirements': [{'origin': 'user', 'outcome': 'Preserve supplied note facts',
                              'artifacts': ['SKILL.md']}],
            'capabilities': [], 'expected_outputs': ['Chat response'], 'side_effects': [],
            'inputs': [ref(self.source), ref(self.design_path)], 'known_issues': []}
        self.content = b'---\nname: brief-note\ndescription: Restate supplied notes.\n---\nPreserve the supplied facts.\n'

    def stage(self, design=True):
        write_json(self.contract_path, self.contract)
        result = authoring.begin(self.contract_path, self.run,
                                 design=self.design_path if design else None)
        self.assertEqual('STAGED', result['state'])
        (self.run / 'candidate/SKILL.md').write_bytes(self.content)

    def blocked(self):
        result = authoring.publish(self.run)
        self.assertEqual('BLOCKED', result['state'], result)
        self.assertFalse(self.target.exists())
        self.assertFalse((self.run / 'authoring-baseline.json').exists())

    def test_design_publication_delivers_exact_bytes_and_unperformed_quality(self):
        self.stage()
        self.assertEqual('AUTHORED', authoring.publish(self.run)['state'])
        self.assertEqual(self.content, (self.target / 'SKILL.md').read_bytes())
        record = json.loads((self.run / 'authoring-record.json').read_bytes())
        self.assertEqual('NOT_PERFORMED', record['validation_status'])
        self.assertEqual('NOT_PERFORMED', record['testing_status'])
        self.assertTrue((self.run / 'publication-readback.json').is_file())
        self.assertTrue((self.run / 'validation-request.json').is_file())

    def test_legacy_no_design_remains_supported(self):
        self.stage(design=False)
        self.assertEqual('AUTHORED', authoring.publish(self.run)['state'])
        self.assertEqual(self.content, (self.target / 'SKILL.md').read_bytes())

    def test_changed_original_design_blocks_before_delivery(self):
        self.stage()
        self.design_path.write_bytes(self.design_path.read_bytes() + b' ')
        self.blocked()

    def test_changed_design_snapshot_blocks_before_delivery(self):
        self.stage()
        (self.run / 'inputs/1').write_bytes(b'changed snapshot')
        self.blocked()

    def test_missing_design_capture_blocks_before_delivery(self):
        self.stage()
        (self.run / 'design-capture.json').rename(self.run / 'removed-design-capture.json')
        self.blocked()

    def test_legacy_mode_downgrade_cannot_hide_changed_design_snapshot(self):
        self.stage()
        path = self.run / 'origin.json'
        origin = json.loads(path.read_bytes())
        origin['design_capture_requested'] = False
        origin.pop('design_capture_ref')
        write_json(path, origin)
        (self.run / 'design-capture.json').rename(self.run / 'removed-design-capture.json')
        (self.run / 'inputs/1').write_bytes(b'changed snapshot')
        self.blocked()

    def test_input_source_drift_blocks_before_delivery(self):
        self.stage()
        self.source.write_bytes(b'Changed requirement')
        self.blocked()

    def test_focused_edit_preserves_unmanaged_bytes(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'old skill')
        (self.target / 'user.txt').write_bytes(b'User bytes\x00\r\n')
        self.contract['operation'] = 'edit'
        self.stage()
        self.assertEqual('AUTHORED', authoring.publish(self.run)['state'])
        self.assertEqual(b'User bytes\x00\r\n', (self.target / 'user.txt').read_bytes())
        self.assertEqual(self.content, (self.target / 'SKILL.md').read_bytes())


if __name__ == '__main__':
    unittest.main(verbosity=2)
