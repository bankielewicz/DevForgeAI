"""Behavioral regressions for confirmed QA-01 through QA-04 (frozen v1)."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import adaptive_observe as adaptive
import adaptive_fixtures as fixture
import text_resources as text


class ConfirmedFindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='validator-confirmed-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def checks(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
        return fixture.reference(path)

    def assessment(self, same_run=False):
        selected = fixture.standalone(self.root / 'inputs')
        members = []
        for member in selected['members']:
            ident = member['member_id']
            rows = [dict(text.check(rule, 'handoffs/card', 'PASS', 'Synthetic record control.'),
                         run_id='set' if same_run else ident, check_id=rule)
                    for rule in adaptive.ALL_RULES]
            folder = self.root / 'members' / ident
            checks = self.checks(folder / 'checks.jsonl', rows)
            report = folder / 'report.md'
            report.write_text('Synthetic record fixture, not actual skill quality.', encoding='utf-8')
            members.append(dict(member_id=ident, package_digest=member['package']['package_digest'],
                                report=fixture.reference(report), checks=checks, outcome='PASS',
                                source_state='UNCHANGED', reason='Controlled fixture.'))
        integration = [dict(text.check('AV-A09', 'handoffs/card', 'PASS', 'Controlled handoff.'),
                            run_id='set', check_id='integration')]
        value = dict(schema_version='set-assessment-v1', run_id='set',
                     input=fixture.write(self.root / 'inputs/input.json', selected), scope='full_set',
                     omitted_member_ids=[], omitted_handoff_ids=[], members=members,
                     integration_checks=self.checks(self.root / 'integration/checks.jsonl', integration),
                     outcome='PASS', assessment_completed=True, required_evaluated=59,
                     required_total=59, unknown_applicability=0, limitations=['Synthetic records.'],
                     prior_assessment=None)
        return value

    def errors(self, value):
        records = self.root / 'records'
        fixture.write(records / 'assessment.json', value)
        return adaptive.records(records)[1]

    def test_member_integration_artifact_reuse_rejected(self):
        value = self.assessment()
        path = Path(value['members'][0]['checks']['path'])
        rows = [dict(json.loads(line), run_id='set') for line in path.read_text().splitlines()]
        value['members'][0]['checks'] = self.checks(path, rows)
        value['integration_checks'] = value['members'][0]['checks']
        value.update(required_evaluated=87, required_total=87)
        self.assertTrue(self.errors(value))

    def test_copied_check_execution_rejected(self):
        value = self.assessment()
        original = Path(value['members'][0]['checks']['path'])
        rows = [dict(json.loads(line), run_id='set') for line in original.read_text().splitlines()]
        value['members'][0]['checks'] = self.checks(original, rows)
        value['integration_checks'] = self.checks(self.root / 'copied/checks.jsonl', rows)
        value.update(required_evaluated=87, required_total=87)
        self.assertTrue(self.errors(value))

    def test_same_execution_in_two_members_rejected(self):
        self.assertTrue(self.errors(self.assessment(same_run=True)))

    def test_same_check_id_in_distinct_runs_accepted(self):
        self.assertEqual(self.errors(self.assessment()), [])

    def test_same_member_artifact_reused_by_other_member_rejected(self):
        value = self.assessment()
        value['members'][1]['checks'] = value['members'][0]['checks']
        self.assertTrue(self.errors(value))

    def test_missing_report_does_not_hide_reused_checks(self):
        value = self.assessment()
        value['members'][0].update(report=None, outcome='INCOMPLETE')
        value['members'][1]['checks'] = value['members'][0]['checks']
        value['outcome'] = 'INCOMPLETE'
        self.assertTrue(self.errors(value))

    @unittest.skipUnless(os.name == 'nt', 'Windows path identity scenario')
    def test_windows_case_alias_is_same_artifact(self):
        value = self.assessment()
        value['members'][1]['checks'] = dict(value['members'][0]['checks'])
        value['members'][1]['checks']['path'] = value['members'][1]['checks']['path'].replace('members', 'MEMBERS')
        self.assertTrue(self.errors(value))

    def test_shared_evidence_is_not_duplicate_execution(self):
        value = self.assessment()
        for member in value['members']:
            path = Path(member['checks']['path'])
            evidence = path.parent / 'evidence.txt'
            evidence.write_text('A shared observation supports distinct rules.')
            reference = fixture.reference(evidence)
            reference['path'] = evidence.name
            rows = [dict(json.loads(line), evidence=[reference]) for line in path.read_text().splitlines()]
            member['checks'] = self.checks(path, rows)
        self.assertEqual(self.errors(value), [])

    def test_required_handoff_not_applicable_rejected(self):
        value = self.assessment()
        path = Path(value['integration_checks']['path'])
        row = json.loads(path.read_text())
        row.update(result='NOT_APPLICABLE', applicability='not_applicable')
        value['integration_checks'] = self.checks(path, [row])
        value.update(required_total=58, required_evaluated=58)
        self.assertTrue(self.errors(value))

    def test_passing_row_does_not_hide_contradictory_required_na(self):
        value = self.assessment()
        path = Path(value['integration_checks']['path'])
        row = json.loads(path.read_text())
        bad = dict(row, check_id='contradiction', result='NOT_APPLICABLE', applicability='not_applicable')
        value['integration_checks'] = self.checks(path, [row, bad])
        self.assertTrue(self.errors(value))

    def test_unperformed_handoff_keeps_incomplete(self):
        value = self.assessment()
        path = Path(value['integration_checks']['path'])
        row = dict(json.loads(path.read_text()), result='NOT_RUN', applicability='unknown')
        value['integration_checks'] = self.checks(path, [row])
        value.update(outcome='INCOMPLETE', required_evaluated=58, unknown_applicability=1)
        self.assertEqual(self.errors(value), [])

    def test_protocol_candidate_multiline_offsets_and_redaction(self):
        raw = '{\r\n "note":"中文 café", "password":"SYNTHETIC_SECRET",\r\n "schema_version":\r\n "ｔask-card-v1"\r\n}\r\n'
        before = raw.encode()
        observed = text.candidates('protocol.json', raw)
        found = [r for r in observed if r['codepoint'] == 'U+FF54']
        self.assertEqual(len(found), 1)
        item = found[0]
        prefix = raw[:raw.index('ｔ')]
        self.assertEqual((item['start_byte'], item['end_byte'], item['line'], item['column']),
                         (len(prefix.encode()), len(prefix.encode()) + 3, 4, 3))
        self.assertEqual(item['disposition'], 'unresolved')
        self.assertIn('\\uff54 -> t', item['reason'])
        self.assertNotIn('SYNTHETIC_SECRET', json.dumps(observed))
        self.assertEqual(raw.encode(), before)

    def test_jsonl_protocol_values_are_located(self):
        raw = '{"schema_version":"task-card-v1"}\n{"schema_version":"ｔask-card-v1"}\n'
        found = text.candidates('protocol.jsonl', raw)
        self.assertEqual(len(found), 1)
        self.assertEqual((found[0]['line'], found[0]['column']), (2, 20))

    def test_json_string_containing_key_example_is_not_protocol(self):
        raw = json.dumps({'note': 'Example "schema_version":"ｔask-card-v1"'}, ensure_ascii=False)
        self.assertEqual(text.candidates('notes.json', raw), [])

    def test_plain_prose_and_ascii_protocol_preserved(self):
        self.assertEqual(text.candidates('notes.md', '中文 العربية café Ａ typography.'), [])
        self.assertEqual(text.candidates('protocol.json', '{"schema_version":"task-card-v1"}'), [])

    def test_nonclosing_fence_tail_keeps_example_literal(self):
        for marker in ('```', '~~~'):
            with self.subTest(marker=marker):
                links, unmatched = text.links(marker + 'text\n' + marker + 'not-close\n[example](absent.md)\n' + marker + '\n')
                self.assertEqual(links, [])
                self.assertFalse(unmatched)

    def test_real_link_after_fence_has_original_line(self):
        links, unmatched = text.links('```text\n```not-close\n[example](absent.md)\n```\n[real](missing.md)\n')
        self.assertEqual(links, [(5, 'missing.md', 'link')])
        self.assertFalse(unmatched)

    def test_tilde_whitespace_closer_and_shorter_marker(self):
        links, unmatched = text.links('~~~~text\n~~~\n[example](absent.md)\n~~~~ \t\n[real](missing.md)\n')
        self.assertEqual(links, [(5, 'missing.md', 'link')])
        self.assertFalse(unmatched)

    def test_backtick_in_info_string_does_not_open_block(self):
        links, unmatched = text.links('```bad`info\n[real](missing.md)\n')
        self.assertEqual(links, [(2, 'missing.md', 'link')])
        self.assertFalse(unmatched)

    def test_headings_inside_false_closer_stay_literal(self):
        self.assertEqual(text.anchors('```text\n```not-close\n# Example\n```\n# Actual\n'), {'actual'})
