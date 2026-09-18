"""Independent malformed-input and resource oracles for SVE-02/03/07.

Synthetic bytes exercise public observation interfaces. No target code executes.
"""
import argparse
import contextlib
import copy
import io
import json
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import observe
import skill_format
import standards_observe
import text_resources


class ResourceQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='resource-quality-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'example'
        self.skill.mkdir()
        self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n---\n# Overview\n')

    def write(self, path, content):
        target = self.skill / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content if isinstance(content, bytes) else content.encode('utf-8'))
        return target

    def structure(self):
        return observe.structure(argparse.Namespace(source=self.skill))

    def test_yaml_parser_rejects_nonmapping_syntax_and_nested_duplicate_keys(self):
        for value in ('[a, b]', 'name: [', 'name: example\nmetadata:\n  a: b\n  a: c',
                      'true: value', '? [a, b]\n: value', 'null'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                skill_format.yaml_mapping(value)

    def test_required_metadata_types_empty_values_and_optional_types(self):
        base = {'name': 'example', 'description': 'Task'}
        for updates in ({'name': ''}, {'name': 23}, {'description': ' '}, {'description': []},
                        {'license': []}, {'compatibility': 1}, {'compatibility': 'x' * 501},
                        {'metadata': []}, {'metadata': {1: 'a'}}, {'metadata': {'a': False}},
                        {'allowed-tools': ['Read', 3]}, {'allowed-tools': []},
                        {'effort': 'ultra'}, {'shell': 'fish'}, {'context': 'spawn'},
                        {'disable-model-invocation': 'maybe'}, {'hooks': []},
                        {'agent': 'Explore', 'context': 'fork-later'}):
            with self.subTest(updates=updates):
                checks = skill_format.metadata_checks(dict(base, **updates))
                self.assertTrue(any(not passed for _, passed, _ in checks))

    def test_frontmatter_missing_delimiters_and_bom_are_diagnostics(self):
        for value in ('name: example', '\ufeff---\nname: example\ndescription: x\n---\n',
                      '---\nname: example\ndescription: x\n'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                skill_format.frontmatter(value)

    def test_structure_keeps_unknown_metadata_unresolved(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\nfuture-host: value\n---\n')
        result, code = self.structure()
        self.assertEqual(code, 0)
        extension = next(v for v in result['checks'] if v['check_id'] == 'additional_metadata')
        self.assertEqual(extension['result'], 'NOT_RUN')
        self.assertFalse(extension['required'])

    def test_structure_optional_invocation_policy_valid_and_invalid_shapes(self):
        # Claude Code carries invocation policy in the frontmatter, not a separate
        # configuration document, and its booleans accept more than true/false.
        for field, expected in [('disable-model-invocation: false', 0),
                                ('disable-model-invocation: "off"', 0),
                                ('user-invocable: 0', 0),
                                ('allowed-tools: [Read]', 0),
                                ('allowed-tools: Read Grep', 0),
                                ('disable-model-invocation: maybe', 1),
                                ('allowed-tools: []', 1),
                                ('effort: ultra', 1)]:
            with self.subTest(field=field):
                self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n'
                           + field + '\n---\n# Overview\n')
                self.assertEqual(self.structure()[1], expected)

    def test_structure_reports_foreign_host_configuration_as_unread(self):
        self.write('agents/openai.yaml', 'policy: {allow_implicit_invocation: false}\n')
        result, code = self.structure()
        self.assertEqual(code, 0, 'another host\'s configuration file is not a Claude Code defect')
        foreign = next(v for v in result['checks'] if v['check_id'] == 'foreign_host_configuration')
        self.assertEqual(foreign['result'], 'NOT_RUN')
        self.assertFalse(foreign['required'])

    def test_structure_directory_identity_uses_bound_snapshot(self):
        output = self.root / 'capture'
        _, code = observe.snapshot(argparse.Namespace(source=self.skill, output=output))
        self.assertEqual(code, 0)
        result, code = observe.structure(argparse.Namespace(source=output / 'source'))
        self.assertEqual(code, 0)
        self.assertEqual(next(v for v in result['checks'] if v['check_id'] == 'directory_identity')['result'], 'PASS')
        (output / 'source' / 'SKILL.md').write_text('---\nname: example\ndescription: Altered\n---\n')
        result, code = observe.structure(argparse.Namespace(source=output / 'source'))
        self.assertEqual(code, 1)
        self.assertEqual(next(v for v in result['checks'] if v['check_id'] == 'snapshot_identity')['result'], 'FAIL')

    def test_structure_distinguishes_local_remote_outside_and_binary_anchor(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n'
                   '[Local](references/a.md#same-1)\n[Remote](https://example.org/a)\n'
                   '[Outside](../other.md)\n[Binary](assets/a.bin#rendered)\n')
        self.write('references/a.md', '# Same\n# Same\n')
        self.write('assets/a.bin', b'\x00')
        result, code = self.structure()
        self.assertEqual(code, 0)
        self.assertEqual(result['links_checked'], 3)
        self.assertTrue(any(v['check_id'] == 'external_resource_scope' and v['result'] == 'NOT_RUN' for v in result['checks']))
        self.assertTrue(any(v['check_id'] == 'resource_anchor' and v['result'] == 'NOT_RUN' for v in result['checks']))

    def test_structure_does_not_fail_quoted_inline_link_example(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n'
                   'Describe the Markdown syntax `[label](not-an-actual-resource.md)` to the user.\n')
        result, code = self.structure()
        self.assertEqual(code, 0, 'An inline code example is not a live resource link: ' + json.dumps(result))
        self.assertEqual(result['links_checked'], 0)

    def test_package_optional_frontmatter_fields_and_extensions(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n'
                   'allowed-tools: Read Grep\ndisable-model-invocation: true\n'
                   'effort: high\n---\n# Overview\n')
        checks, _, _ = text_resources.package(self.skill)
        self.assertEqual(next(v for v in checks if v['rule_id'] == 'AV-F04')['result'], 'PASS')
        self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n'
                   'future-host-field: value\n---\n# Overview\n')
        checks, _, _ = text_resources.package(self.skill)
        self.assertEqual(next(v for v in checks if v['rule_id'] == 'AV-F04')['result'], 'NOT_RUN')

    def test_package_records_tool_list_portability_divergence_without_failing(self):
        # Every Claude Code skill in this repository declares allowed-tools as a YAML
        # list. If the divergence entered the required reduction they would all reduce
        # to INCOMPLETE, which is the same defect as failing them outright.
        self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n'
                   'allowed-tools:\n  - Read\n---\n# Overview\n')
        checks, _, _ = text_resources.package(self.skill)
        rows = [v for v in checks if v['rule_id'] == 'AV-F04']
        required = [v for v in rows if v['required']]
        self.assertEqual(1, len(required))
        self.assertEqual('PASS', required[0]['result'])
        divergence = [v for v in rows if not v['required']]
        self.assertEqual(1, len(divergence))
        self.assertIn('Agent Skills specification', divergence[0]['reason'])
        self.assertEqual('PASS', observe.reduce_checks(rows)['outcome'])

    def test_package_divergence_rows_do_not_collide_on_check_identity(self):
        self.write('SKILL.md', '---\nname: claude-example\ndescription: Useful task\n'
                   'allowed-tools:\n  - Read\n---\n# Overview\n')
        checks, _, _ = text_resources.package(self.skill)
        rows = [v for v in checks if v['rule_id'] == 'AV-F04' and not v['required']]
        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(len(rows), len({v['check_id'] for v in rows}))
        self.assertEqual('PASS', observe.reduce_checks(
            [v for v in checks if v['rule_id'] == 'AV-F04'])['outcome'])

    def test_package_reports_foreign_host_configuration_as_unread(self):
        self.write('agents/openai.yaml', 'interface: {display_name: Example}\n')
        checks, _, _ = text_resources.package(self.skill)
        foreign = next(v for v in checks
                       if v['rule_id'] == 'AV-F04' and v['subject_path'] == 'agents/openai.yaml')
        self.assertEqual(foreign['result'], 'NOT_RUN')

    def test_package_bad_frontmatter_shapes_fail_once_not_twice(self):
        # The entrypoint is parsed once. AV-F01 carries the failure; AV-F04 must not
        # re-raise the same exception and bill it a second time.
        for value in ('allowed-tools: 3', 'allowed-tools: []', 'metadata: []',
                      'metadata: {a: false}', 'effort: ultra', 'shell: fish',
                      'context: spawn', 'disable-model-invocation: maybe',
                      'compatibility: 1', 'hooks: []', 'model: [inherit]'):
            with self.subTest(value=value):
                self.write('SKILL.md', '---\nname: example\ndescription: Useful task\n'
                           + value + '\n---\n# Overview\n')
                checks, _, _ = text_resources.package(self.skill)
                entry = [v for v in checks if v['subject_path'] == 'SKILL.md' and v['required']]
                failed = [v for v in entry if v['result'] == 'FAIL']
                self.assertEqual(1, len(failed), 'exactly one required FAIL per entrypoint')
                self.assertEqual('AV-F01', failed[0]['rule_id'])
                skipped = next(v for v in entry if v['rule_id'] == 'AV-F04')
                self.assertEqual('NOT_APPLICABLE', skipped['result'])
                self.assertEqual('not_applicable', skipped['applicability'])
                self.assertTrue(skipped['reason'])

    def test_package_bad_text_missing_entrypoint_and_unknown_extensions(self):
        self.write('references/bad.md', b'\xff')
        checks, _, _ = text_resources.package(self.skill)
        self.assertTrue(any(v['subject_path'] == 'references/bad.md' and v['result'] == 'FAIL' for v in checks))
        (self.skill / 'SKILL.md').unlink()
        checks, _, _ = text_resources.package(self.skill)
        self.assertTrue(any(v['subject_path'] == 'SKILL.md' and v['result'] == 'FAIL' for v in checks))
        self.write('SKILL.md', '---\nname: example\ndescription: Task\nfuture: abc\n---')
        checks, _, _ = text_resources.package(self.skill)
        self.assertTrue(any(v['subject_path'] == 'metadata-extensions' and v['result'] == 'NOT_RUN' for v in checks))

    def test_package_quoted_placeholders_unicode_and_orphan_assets_not_defects(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n'
                   'Résumé Ω 中文\n```md\nTODO [not real](absent.md)\n```\n')
        self.write('assets/unlinked.png', b'\x00\xff')
        checks, details, _ = text_resources.package(self.skill)
        self.assertFalse(any(v['result'] == 'FAIL' for v in checks))
        self.assertEqual(details['unicode_candidates'], [])
        self.assertFalse(next(v for v in details['resources'] if v['path'] == 'assets/unlinked.png')['reachable'])
        self.assertIsNone(details['context']['tokenizer'])
        self.assertTrue(all(v['tokens'] is None for v in details['context']['files']))

    def test_resource_references_and_escaped_parentheses(self):
        rows, unmatched = text_resources.links('[Image][pic]\n![pic][]\n[pic]: assets/a.png\n'
                                              '[Missing][unknown]\n[A](references/a\\(b\\).md)\n[Incomplete](unclosed\n')
        self.assertFalse(unmatched)
        self.assertEqual(sum(target == 'assets/a.png' for _, target, _ in rows), 2)
        self.assertIn('references/a(b).md', [v[1] for v in rows])
        self.assertTrue(any(v[1].startswith('unresolved-reference:') for v in rows))

    def test_resource_resolutions_distinguish_manual_adjudication(self):
        texts = {'SKILL.md': '# Overview\n', 'references/a.md': 'Title\n=====\n<div id="custom"></div>\n'}
        paths = set(texts) | {'assets/a.png'}
        for source, target, expected in [('SKILL.md', '#overview', 'resolved'),
            ('SKILL.md', 'references/a.md#title', 'resolved'), ('SKILL.md', 'references/a.md#custom', 'resolved'),
            ('SKILL.md', 'references/a.md#unsupported', 'unsupported_anchor'),
            ('SKILL.md', 'assets/a.png#x', 'unsupported_anchor'), ('SKILL.md', '../escape', 'outside_scope'),
            ('SKILL.md', '${dynamic}/a', 'dynamic'), ('SKILL.md', 'unresolved-reference:a', 'dynamic'),
            ('SKILL.md', 'absent.md', 'missing'), ('references/a.md', '../SKILL.md', 'resolved')]:
            with self.subTest(target=target):
                self.assertEqual(text_resources.resolve(source, target, texts, paths)[0], expected)

    def test_unicode_protocol_candidate_redacts_surrounding_secret(self):
        text = '{"schema_version":"１","secret":"keep-me-private"}\n'
        rows = text_resources.candidates('record.json', text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['context'], 'unknown')
        self.assertEqual(text.encode('utf-8')[rows[0]['start_byte']:rows[0]['end_byte']].decode('utf-8'), '１')
        self.assertNotIn('keep-me-private', json.dumps(rows))
        self.assertEqual(text_resources.protocol_value_spans('prose.md', text), [])

    def test_organization_cli_reports_advice_and_decode_error(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = standards_observe.main(['--source', str(self.skill)])
        value = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(value['authority'], 'NONE')
        self.assertNotIn('verdict', value)
        self.write('references/bad.md', b'\xff')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = standards_observe.main(['--source', str(self.skill)])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())['outcome'], 'ERROR')

    def test_inventory_limits_and_unstable_read_fail_without_partial_success(self):
        with self.assertRaises(observe.ObservationError):
            observe.inventory(self.skill, max_files=0)
        with self.assertRaises(observe.ObservationError):
            observe.inventory(self.skill, max_bytes=1)
        with self.assertRaises(observe.ObservationError):
            observe.inventory(self.skill / 'SKILL.md')
        with self.assertRaises(observe.ObservationError):
            observe.read_stable(self.skill)
        original = (self.skill / 'SKILL.md').stat()
        self.write('SKILL.md', 'changed')
        with self.assertRaises(observe.ObservationError):
            observe.read_stable(self.skill / 'SKILL.md', original)
        with self.assertRaises(observe.ObservationError):
            observe.safe_path(self.skill / '..' / 'escape')

    def test_excluded_boundaries_prevent_complete_capture(self):
        self.write('backup/secret.txt', 'excluded')
        manifest = observe.make_manifest(self.skill)
        self.assertFalse(manifest['complete'])
        self.assertEqual([v['path'] for v in manifest['files']], ['SKILL.md'])
        result, code = observe.snapshot(argparse.Namespace(source=self.skill, output=self.root / 'capture'))
        self.assertEqual(code, 1)
        self.assertEqual(result['status'], 'INCOMPLETE')
        checks, _, limits = text_resources.package(self.skill)
        self.assertTrue(any(v['rule_id'] == 'AV-E01' and v['result'] == 'NOT_RUN' for v in checks))
        self.assertTrue(any('backup' in value for value in limits))

    def test_manifest_invalid_shapes_and_complete_claims_are_rejected(self):
        original = observe.make_manifest(self.skill)
        invalids = [[], {'schema_version': '1', 'files': {}}, dict(original, files=[1]),
                    dict(original, files=original['files'] * 2), dict(original, package_digest='0' * 64),
                    dict(original, excluded_boundaries={}), dict(original, complete=1),
                    dict(original, excluded_boundaries=[{'path': 'backup'}], complete=True)]
        for value in invalids:
            with self.subTest(value=value):
                self.assertTrue(observe.validate_manifest(value))

    def test_readback_rejects_malformed_manifest_and_tracks_removed_added_changed(self):
        manifest = observe.make_manifest(self.skill)
        path = self.root / 'manifest.json'
        path.write_text(json.dumps(dict(manifest, package_digest='0' * 64)))
        result, code = observe.readback(argparse.Namespace(source=self.skill, manifest=path))
        self.assertEqual((result['status'], code), ('MISMATCH', 1))
        path.write_text(json.dumps(manifest))
        self.write('SKILL.md', 'changed')
        self.write('new.txt', 'new')
        result, code = observe.readback(argparse.Namespace(source=self.skill, manifest=path))
        self.assertEqual((result['status'], code), ('SOURCE_CHANGED', 1))
        self.assertEqual(result['changed'], ['SKILL.md'])
        self.assertEqual(result['added'], ['new.txt'])

    def test_records_invalid_sources_shapes_and_reference_locators(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'evidence.txt').write_text('one\ntwo\n')
        digest = observe.sha256((run / 'evidence.txt').read_bytes())
        refs = [dict(path='evidence.txt', sha256=digest, source_id='missing', start_byte=-1, end_byte=50,
                     start_line=0, end_line=3, locator={'line_start': 0, 'line_end': 9, 'start_byte': 8, 'end_byte': 7}),
                dict(path='missing.txt', sha256=digest), dict(path='../escape', sha256=digest),
                dict(path='evidence.txt', sha256='0' * 64), dict(path='sources.json', sha256=digest)]
        (run / 'sources.json').write_text(json.dumps({'sources': [{'source_id': 'a'}, {'source_id': 'a'}, 3], 'refs': refs}))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        for expected in ('source IDs', 'source record must be an object', 'invalid byte locator', 'invalid line locator',
                         'invalid nested line locator', 'invalid nested byte locator', 'unknown source_id',
                         'invalid path/digest', 'reference digest mismatch', 'self-referential digest'):
            self.assertIn(expected, errors)

    def test_records_parse_errors_and_wrong_collection_shapes(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'bad.json').write_text('{"duplicate":1,"duplicate":2}')
        (run / 'sources.json').write_text('{"sources":{}}')
        (run / 'rule-set.json').write_text('{"rules":{}}')
        (run / 'findings.json').write_text('{"findings":{}}')
        (run / 'origin-record.json').write_text('[]')
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        for expected in ('duplicate JSON key', 'sources must be an array', 'rules must be an array',
                         'findings must be an array', 'origin-record.json must be an object'):
            self.assertIn(expected, errors)

    def test_records_malformed_checks_do_not_gain_acceptance(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'rule-set.json').write_text('{"rules":[{"rule_id":"known"},{"rule_id":"known"}]}')
        invalid = {'schema_version': 'wrong', 'run_id': '', 'check_id': 'duplicate', 'rule_id': 'unknown',
                   'subject_path': '../escape', 'method': '', 'required': 'true', 'applicability': 'unknown',
                   'result': 'PASS', 'reason': '', 'evidence': [{}], 'dimension': 'invented'}
        (run / 'checks.jsonl').write_text('\n'.join(json.dumps(v) for v in [[], {}, invalid, invalid]))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        self.assertNotEqual(result['overall_assessment'], 'PASS')
        errors = '\n'.join(result['errors'])
        for expected in ('duplicate rule_id', 'check row must be an object', 'check missing fields',
                         'schema_version/required invalid', 'missing/duplicate check_id',
                         'inconsistent check applicability/result', 'unknown rule_id',
                         'invalid check subject_path', 'evidence entries require', 'unsupported check dimension'):
            self.assertIn(expected, errors)

    def test_records_ready_handoff_requires_bound_review_and_matching_source(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'origin-record.json').write_text('{"history_kind":"generated","source_readback_state":"SOURCE_CHANGED"}')
        (run / 'handoff.json').write_text(json.dumps({'builder_readiness': 'READY', 'review_state': 'pending',
            'proposal_review_state': 'approved', 'selected_finding_ids': ['unknown'], 'deferred_finding_ids': [],
            'proposed_spec': {'future': 'unbound'}}))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        for expected in ('prior_evidence', 'unknown finding ID', 'conflicting review-state aliases',
                         'recorded approved review instruction', 'READY requires baseline',
                         'review authorization must bind', 'matching source readback', 'changed source requires BLOCKED'):
            self.assertIn(expected, errors)

    def test_record_cli_malformed_input_emits_json_without_traceback(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'source-manifest.json').write_text('{"schema_version":"1","files":[]}')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = observe.main(['records', '--run-root', str(run)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out.getvalue())['status'], 'MISMATCH')
        self.assertNotIn('Traceback', err.getvalue())

    def test_findings_validate_identity_aliases_and_duplicate_observations(self):
        run = self.root / 'run'; run.mkdir()
        identity_id, identity = observe.finding_identity('unknown', 'SKILL.md', 'MISSING_FILE', 1)
        finding = dict(finding_id=identity_id, rule_id='unknown', category='workflow', severity='invalid',
                       subject_path='SKILL.md', identity=identity, source_refs=[], source_references=[{}],
                       observation_references=[], description='Observed failure', user_impact='Cannot complete',
                       proposed_correction='Repair', preserved_requirements=[], verification_cases=['case'],
                       disposition='invalid')
        (run / 'rule-set.json').write_text('{"rules":[{"rule_id":"known"}]}')
        (run / 'findings.json').write_text(json.dumps({'findings': [3, {}, finding, finding]}))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        for expected in ('finding must be an object', 'finding missing fields', 'conflicting finding reference aliases',
                         'finding identity must be', 'MISSING_FILE finding occurrence', 'duplicate finding identity',
                         'invalid finding severity/disposition', 'finding references unknown rule_id'):
            self.assertIn(expected, errors)

    def test_four_dimensions_support_aliases_and_reject_wrong_assessment(self):
        run = self.root / 'run'; run.mkdir()
        rows = []
        aliases = ['standards_compliance', 'workflow_correctness', 'instruction_quality', 'behavioral_evaluation']
        for dimension in aliases:
            rows.append(dict(schema_version='1', run_id='a', check_id=dimension, rule_id='R', subject_path='SKILL.md',
                             method='independent', required=True, applicability='applicable', result='PASS',
                             reason='Observed output', evidence=[], dimension=dimension))
        (run / 'checks.jsonl').write_text('\n'.join(json.dumps(v) for v in rows))
        (run / 'assessment.json').write_text(json.dumps({'overall_assessment': 'PASS',
                                                       'dimensions': {key: {'outcome': 'PASS'} for key in aliases}}))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 0, result['errors'])
        self.assertEqual(result['overall_assessment'], 'PASS')
        (run / 'assessment.json').write_text('{"overall_assessment":"FAIL","dimensions":[]}')
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        self.assertIn('declared overall assessment contradicts', errors)
        self.assertIn('assessment dimensions must be an object', errors)
        self.assertIn('declared dimension contradicts', errors)

    def test_manifest_invalid_size_digest_and_false_original_identity(self):
        original = observe.make_manifest(self.skill)
        for replacement in ({'path': '../escape', 'bytes': 0, 'sha256': '0' * 64},
                            {'path': 'SKILL.md', 'bytes': True, 'sha256': '0' * 64},
                            {'path': 'SKILL.md', 'bytes': -1, 'sha256': '0' * 64},
                            {'path': 'SKILL.md', 'bytes': 0, 'sha256': 'wrong'}):
            with self.subTest(replacement=replacement):
                manifest = dict(original, files=[replacement])
                self.assertIn('invalid manifest file row', observe.validate_manifest(manifest))

    def test_package_missing_resource_vs_dynamic_anchor_and_secret_redaction(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n'
                   '[Missing](absent.md)\n[Dynamic](${version}/README.md)\n'
                   '[Unsupported](SKILL.md#renderer-specific)\n[Remote](https://host/?token=private-value)\n')
        checks, details, _ = text_resources.package(self.skill)
        resource_checks = [v for v in checks if v['rule_id'] == 'AV-R01']
        self.assertEqual(sum(v['result'] == 'FAIL' for v in resource_checks), 1)
        self.assertEqual(sum(v['result'] == 'NOT_RUN' for v in resource_checks), 2)
        self.assertNotIn('private-value', json.dumps(details['edges']))

    def test_local_tokenizer_invalid_selection_does_not_download(self):
        for name, encoding in [('other', 'x'), ('tiktoken', None)]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                text_resources.local_tokenizer(name, encoding)

    def test_empty_and_malformed_record_sets_are_unperformed(self):
        run = self.root / 'run'; run.mkdir()
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        self.assertIn('no parseable machine records found', result['errors'])
        (run / 'bad.json').write_bytes(b'\xff')
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        self.assertNotEqual(result['overall_assessment'], 'PASS')

    def test_record_handoff_invalid_states_and_unreviewed_change(self):
        run = self.root / 'run'; run.mkdir()
        for handoff, expected in [
            ({'builder_readiness': 'unknown', 'review_state': 'unknown', 'selected_finding_ids': 1}, 'invalid builder_readiness'),
            ({'builder_readiness': 'NO_CHANGE', 'review_state': 'not_needed', 'proposed_spec': {'proposal': 'x'}}, 'NO_CHANGE contradicts'),
            ({'builder_readiness': 'REVIEW_REQUIRED', 'review_state': 'approved'}, 'REVIEW_REQUIRED must retain'),
            ({'builder_readiness': 'REVIEW_REQUIRED', 'review_state': 'pending', 'proposed_spec': {'proposal': 'x'}}, 'adoption-dependent execution')]:
            with self.subTest(handoff=handoff):
                (run / 'handoff.json').write_text(json.dumps(handoff))
                result, code = observe.records(argparse.Namespace(run_root=run))
                self.assertEqual(code, 1)
                self.assertIn(expected, '\n'.join(result['errors']))

    def test_installed_tokenizer_disabled_missing_and_corrupt_local_cache(self):
        # Exercise the installed tokenizer's real cache loading, without network.
        # None of these scenarios constructs an Encoding, so no global encoding
        # cache is populated or cleared.
        original = os.environ.get('TIKTOKEN_CACHE_DIR')
        try:
            os.environ['TIKTOKEN_CACHE_DIR'] = ''
            encoder, identity, reason = text_resources.local_tokenizer('tiktoken', 'r50k_base')
            self.assertIsNone(encoder)
            self.assertIsNone(identity)
            self.assertIn('NOT_RUN', reason)
            cache = self.root / 'token-cache'; cache.mkdir()
            os.environ['TIKTOKEN_CACHE_DIR'] = str(cache)
            encoder, identity, reason = text_resources.local_tokenizer('tiktoken', 'r50k_base')
            self.assertIsNone(encoder)
            self.assertIn('No download', reason)
            self.assertEqual(list(cache.iterdir()), [])
            locator = 'https://openaipublic.blob.core.windows.net/encodings/r50k_base.tiktoken'
            cached_file = cache / hashlib.sha1(locator.encode()).hexdigest()
            cached_file.write_bytes(b'invalid cached token ranks')
            encoder, identity, reason = text_resources.local_tokenizer('tiktoken', 'r50k_base')
            self.assertIsNone(encoder)
            self.assertIn('NOT_RUN', reason)
            self.assertEqual(cached_file.read_bytes(), b'invalid cached token ranks')
        finally:
            if original is None:
                os.environ.pop('TIKTOKEN_CACHE_DIR', None)
            else:
                os.environ['TIKTOKEN_CACHE_DIR'] = original

    def test_adaptive_resource_roles_are_observed_without_claiming_usage(self):
        descriptor = dict(schema_version='adaptive-skill-v1', name='example', role='core', binding_required=True,
                          parent_core=None, contract_path='references/adaptive-contract.md',
                          required_capabilities=['Python 3.10+'],
                          resource_roles=[dict(path='references/adaptive-contract.md', role='reference', reason='Required contract')])
        self.write('references/adaptive-contract.md', 'Contract')
        self.write('assets/devforgeai-skill.json', json.dumps(descriptor))
        checks, detail, _ = text_resources.package(self.skill)
        self.assertEqual(next(v for v in checks if v['rule_id'] == 'AV-A04')['result'], 'PASS')
        resource = next(v for v in detail['resources'] if v['path'] == 'references/adaptive-contract.md')
        self.assertEqual(resource['role'], 'reference')
        self.assertEqual(resource['usage'], 'unresolved_usage')
        self.assertFalse(resource['reachable'])
        self.write('assets/devforgeai-skill.json', '{}')
        checks, _, _ = text_resources.package(self.skill)
        self.assertEqual(next(v for v in checks if v['rule_id'] == 'AV-A04')['result'], 'FAIL')

    def test_structure_fenced_examples_and_same_file_anchor(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n# Overview\n'
                   '[Here](#overview)\n```md\n[Example](absent.md)\n```\n'
                   '~~~md\n# False heading\n[Example](absent.md)\n~~~\n')
        result, code = self.structure()
        self.assertEqual(code, 0)
        self.assertEqual(result['links_checked'], 1)
        anchors = observe.anchors((self.skill / 'SKILL.md').read_text())
        self.assertIn('overview', anchors)
        self.assertNotIn('false-heading', anchors)

    def test_records_cycle_duplicate_dependencies_and_source_snapshot_paths(self):
        run = self.root / 'run'; run.mkdir()
        (run / 'directory').mkdir()
        # Digests intentionally mismatch as no cyclic fixed-point hashes are
        # constructible. The cycle must still be diagnosed rather than recursed.
        (run / 'a.json').write_text(json.dumps({'path': 'b.json', 'sha256': '0' * 64}))
        (run / 'b.json').write_text(json.dumps({'path': 'a.json', 'sha256': '0' * 64}))
        (run / 'c.json').write_text(json.dumps({'path': 'b.json', 'sha256': '0' * 64}))
        (run / 'sources.json').write_text(json.dumps({'sources': [dict(source_id='s', snapshot_path='directory', sha256='0' * 64)]}))
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        errors = '\n'.join(result['errors'])
        self.assertIn('cyclic digest references', errors)
        self.assertIn('reference is not a regular file', errors)

    def test_records_retained_snapshot_drift_and_malformed_fixture_json(self):
        run = self.root / 'run'
        observe.snapshot(argparse.Namespace(source=self.skill, output=run))
        (run / 'inputs').mkdir()
        (run / 'inputs' / 'broken.json').write_text('not JSON fixture')
        (run / 'trials').mkdir()
        (run / 'trials' / 'broken.json').write_text('not JSON fixture')
        (run / 'source' / 'SKILL.md').write_text('changed candidate')
        result, code = observe.records(argparse.Namespace(run_root=run))
        self.assertEqual(code, 1)
        self.assertIn('source-manifest.json does not match retained source bytes/file set', result['errors'])
        self.assertFalse(any('broken.json' in item for item in result['errors']))

    def test_advisory_only_reduction_does_not_create_required_cases(self):
        result = observe.reduce_checks([dict(check_id='advice', applicability='applicable', required=False,
                                            result='FAIL', reason='Size recommendation')])
        self.assertEqual(result['required_total'], 0)
        self.assertEqual(result['outcome'], 'PASS')

    def test_unmatched_fence_is_unresolved_not_required_defect(self):
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n```text\nopen fence')
        checks, _, _ = text_resources.package(self.skill)
        self.assertTrue(any(v['rule_id'] == 'AV-F05' and v['result'] == 'NOT_RUN' for v in checks))
        self.assertFalse(any(v['result'] == 'FAIL' for v in checks))

    def test_structure_no_metadata_and_package_source_named_snapshot(self):
        self.write('SKILL.md', 'no metadata')
        checks, _, _ = text_resources.package(self.skill)
        self.assertTrue(any(v['rule_id'] == 'AV-F01' and v['result'] == 'FAIL' for v in checks))
        self.write('SKILL.md', '---\nname: example\ndescription: Task\n---\n')
        snapshot = self.root / 'captured'
        observe.snapshot(argparse.Namespace(source=self.skill, output=snapshot))
        checks, _, _ = text_resources.package(snapshot / 'source')
        self.assertEqual(next(v for v in checks if v['rule_id'] == 'AV-F02')['result'], 'NOT_RUN')


if __name__ == '__main__':
    unittest.main()
