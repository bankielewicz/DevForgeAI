"""A no-plugin baseline must not be required to load the missing plugin."""
from pathlib import Path
import json
import tempfile
import unittest
import grade_contract_eval_v4 as previous
import grade_contract_eval_v5 as current


class BaselineActivationTests(unittest.TestCase):
    def source(self, metadata, arm, loads=()):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            grader = root/'activation.md'
            grader.write_text('---\ntype: codex_skill_read\nskill: prd\n' + metadata + '---\n')
            return current.source_grade(grader, root, '', {'arm': arm}, list(loads), [])

    def test_positive_unscoped_is_plugin_only(self):
        self.assertFalse(self.source('', 'baseline')['applicable'])
        self.assertFalse(self.source('', 'plugin')['passed'])
        self.assertTrue(self.source('', 'plugin', ['observed read'])['passed'])

    def test_negative_activation_remains_both_arms(self):
        for arm in ['baseline', 'plugin']:
            with self.subTest(arm=arm):
                self.assertTrue(self.source('min: 0\nmax: 0\n', arm)['passed'])
                self.assertFalse(self.source('min: 0\nmax: 0\n', arm, ['unexpected read'])['passed'])

    def test_explicit_arm_metadata_is_not_relaxed(self):
        self.assertTrue(self.source('arm: both\n', 'baseline')['applicable'])
        self.assertFalse(self.source('arm: both\n', 'baseline')['passed'])
        self.assertTrue(self.source('arm: baseline\n', 'baseline')['applicable'])
        self.assertFalse(self.source('arm: plugin\n', 'baseline')['applicable'])

    def test_current_source_scope_is_exactly_two_grader_files(self):
        suite = Path(__file__).resolve().parents[1]/'evals'
        affected = []
        for path in suite.glob('*/*/graders/*.md'):
            d = current.frontmatter(path.read_text())
            if d.get('type') in {'skill_loaded', 'tool_used', 'codex_skill_read'} and d.get('arm') is None and int(d.get('min', 1)) > 0:
                affected.append(path.relative_to(suite).as_posix())
        # Restrict this campaign's comparison to its two suites.
        affected = [p for p in affected if p.startswith(('prd/', 'architecture/'))]
        self.assertEqual(sorted(affected), ['prd/selects-unprocessed-brn/graders/skill-fired.md', 'prd/writes-prd-from-brn/graders/skill-fired.md'])

    def test_content_pass_does_not_require_baseline_activation_but_leak_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trial = root/'matrix/control'
            trial.mkdir(parents=True)
            definitions = root/'definitions/prd/control/graders'
            definitions.mkdir(parents=True)
            (definitions/'skill-fired.md').write_text('---\ntype: codex_skill_read\nskill: prd\n---\n')
            (definitions/'document.md').write_text('---\ntype: file_exists\npath: docs/specs/prd/PRD-001.md\nexists: true\n---\n')
            document = trial/'workspace/docs/specs/prd/PRD-001.md'
            document.parent.mkdir(parents=True)
            document.write_text('Control fixture, not native evidence.\n')
            def save(name, data):
                (trial/name).write_text(json.dumps(data))
            result = {'skill': 'prd', 'case': 'control', 'arm': 'baseline', 'repeat': 1,
                      'status': 'completed', 'mode': 'default', 'scratch_parent': str(root/'scratch'),
                      'model': 'control-model', 'threadId': 'control-session'}
            save('result.json', result)
            save('before.json', {})
            save('after.json', {'docs/specs/prd/PRD-001.md': 'control-hash'})
            for name in ['git-before.json', 'git-after.json']:
                save(name, dict(head={}, index={}, refs={}))
            (trial/'protocol.jsonl').write_text('')
            self.assertFalse(previous.grade(trial)['binary_conformance'])
            fixed = current.grade(trial)
            self.assertTrue(fixed['binary_conformance'])
            self.assertEqual(fixed['source_score'], 1)
            skill = root/'scratch/devforgeai/skills/prd/SKILL.md'
            leaked = {'message': {'method': 'item/completed', 'params': {'item': {
                'type': 'commandExecution', 'id': 'leak-control', 'exitCode': 0,
                'aggregatedOutput': 'name: devforgeai:prd\n', 'command': 'cat ' + str(skill),
                'commandActions': [{'type': 'read', 'path': str(skill)}]}}}}
            (trial/'protocol.jsonl').write_text(json.dumps(leaked) + '\n')
            leaked_grade = current.grade(trial)
            self.assertFalse(leaked_grade['guards']['activation_matches'])
            self.assertFalse(leaked_grade['binary_conformance'])


if __name__ == '__main__':
    unittest.main()
