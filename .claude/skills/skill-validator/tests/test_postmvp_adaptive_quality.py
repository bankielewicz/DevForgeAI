"""Independent content-level contract checks using real disposable files."""
import contextlib
import copy
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import adaptive_contracts as contracts
import adaptive_observe as adaptive
import authoring_intake
import adaptive_fixtures as fixtures
import observe
import text_resources


class AdaptiveQualityTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='independent-adaptive-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()

    def call(self, module, args):
        previous = sys.argv
        output = io.StringIO()
        try:
            sys.argv = [str(SCRIPTS / module)] + args
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as stopped:
                runpy.run_path(str(SCRIPTS / module), run_name='__main__')
            return stopped.exception.code, json.loads(output.getvalue())
        finally:
            sys.argv = previous

    def test_intake_entrypoint_preserves_membership_and_rejects_digest(self):
        value = fixtures.standalone(self.root / 'inputs')
        reference = fixtures.write(self.root / 'request.json', value)
        args = ['intake-set', '--request', reference['path'], '--request-sha256', reference['sha256']]
        code, result = self.call('adaptive_observe.py', args)
        self.assertEqual(code, 0)
        self.assertEqual(result['observations']['ordered_member_ids'], ['A', 'B'])
        self.assertEqual([row['member_id'] for row in result['observations']['member_bindings']], ['A', 'B'])
        code, result = self.call('adaptive_observe.py', args[:-1] + ['0' * 64])
        self.assertEqual((code, result['status']), (1, 'MISMATCH'))

    def test_package_entrypoint_and_records_round_trip(self):
        package = fixtures.package(self.root / 'inputs', 'sample')
        code, result = self.call('adaptive_observe.py', ['package', '--source', package['root']])
        self.assertEqual(code, 0)
        fixtures.write(self.root / 'observation.json', result)
        code, checked = self.call('adaptive_observe.py', ['records', '--run-root', str(self.root)])
        self.assertEqual(code, 0)
        self.assertEqual(checked['observations']['checked_records'], ['observation.json'])
        result['observations']['resources'][0]['usage'] = 'used'
        fixtures.write(self.root / 'observation.json', result)
        code, checked = self.call('adaptive_observe.py', ['records', '--run-root', str(self.root)])
        self.assertEqual((code, checked['status']), (1, 'MISMATCH'))
        self.assertTrue(any('adjudicate resource' in item for item in checked['observations']['errors']))

    def test_missing_input_is_unavailable_not_success(self):
        code, result = self.call('adaptive_observe.py', ['package', '--source', str(self.root / 'missing')])
        self.assertEqual((code, result['status']), (2, 'INCOMPLETE'))
        code, result = self.call('adaptive_observe.py', ['records', '--run-root', str(self.root)])
        self.assertEqual((code, result['status']), (1, 'MISMATCH'))

    def observation(self):
        source = fixtures.package(self.root, 'sample')
        root = Path(source['root'])
        (root / 'guide.md').write_text('Retain raw bytes.\n', encoding='utf-8')
        with (root / 'SKILL.md').open('a', encoding='utf-8') as stream:
            stream.write('\n[guide](guide.md)\nLiteral directional mark: \u202e\n')
        _, data, _ = text_resources.package(root)
        return dict(schema_version='adaptive-observations-v1', run_id='quality', target_digest=source['package_digest'], bindings=[], limitations=[], **data)

    def test_supplemental_locations_and_no_guessed_tokens(self):
        value = self.observation()
        adaptive.supplemental(value, contracts.Reader())
        for mutate, message in [
            (lambda x: x['unicode_candidates'][0].update(end_byte=999999), 'interval'),
            (lambda x: x['unicode_candidates'][0].update(codepoint='202E'), 'codepoint'),
            (lambda x: x['edges'][0].update(source='absent.md'), 'edge source'),
            (lambda x: x['context']['files'][0].update(tokens=1), 'tokens without'),
            (lambda x: x['context'].update(budget_result='PASS'), 'without selected budget'),
        ]:
            bad = copy.deepcopy(value)
            mutate(bad)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                adaptive.supplemental(bad, contracts.Reader())

    def test_context_budget_uses_complete_measurement_and_occurrences(self):
        value = self.observation()
        source = fixtures.write(self.root / 'budget.json', {'maximum': 1})
        context = value['context']
        context['budget'] = dict(unit='bytes', scope='entrypoint', maximum=1, case_id=None, source=source)
        context['budget_result'] = 'FAIL'
        adaptive.supplemental(value, contracts.Reader())
        context['budget']['unit'] = 'tokens'
        context['budget_result'] = 'NOT_RUN'
        adaptive.supplemental(value, contracts.Reader())
        context['budget'].update(unit='bytes', scope='unique_branch_content', maximum=100000, case_id='one')
        context['loads'] = [dict(case_id='one', path='guide.md', occurrences=3, basis='static_estimate', tokens=None, evidence=[])]
        context['budget_result'] = 'PASS'
        adaptive.supplemental(value, contracts.Reader())
        context['budget']['scope'] = 'observed_total_loads'
        context['budget_result'] = 'NOT_RUN'
        adaptive.supplemental(value, contracts.Reader())
        context['loads'][0].update(basis='observed_full_file', evidence=[source])
        byte_count = len((self.root / 'sample/guide.md').read_bytes())
        context['budget']['maximum'] = byte_count * 3 - 1
        context['budget_result'] = 'FAIL'
        adaptive.supplemental(value, contracts.Reader())
        context['budget']['maximum'] += 1
        context['budget_result'] = 'PASS'
        adaptive.supplemental(value, contracts.Reader())
        context['tokenizer'] = dict(name='tiktoken', version='fixture', encoding='fixture')
        context['loads'][0]['tokens'] = 4
        context['budget'].update(unit='tokens', maximum=11)
        context['budget_result'] = 'FAIL'
        adaptive.supplemental(value, contracts.Reader())
        context['budget_result'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'measurement/result'):
            adaptive.supplemental(value, contracts.Reader())

    def test_descriptor_requires_actual_contract_resources(self):
        package = fixtures.package(self.root, 'sample')
        root = Path(package['root'])
        (root / 'references').mkdir()
        (root / 'references/adaptive-contract.md').write_text('Preserve source.', encoding='utf-8')
        value = dict(schema_version='adaptive-skill-v1', name='sample', role='core', binding_required=True, parent_core=None, contract_path='references/adaptive-contract.md', required_capabilities=['Python 3.10+'], resource_roles=[dict(path='references/adaptive-contract.md', role='reference', reason='Required contract')])
        reference = fixtures.write(root / 'assets/devforgeai-skill.json', value)
        reader = contracts.Reader()
        reader.record(value, reference['path'])
        reader.member_descriptor({'adaptive_descriptor': reference}, root)
        reader.readback()
        with self.assertRaisesRegex(ValueError, 'missing adaptive descriptor'):
            contracts.Reader().member_descriptor({'adaptive_descriptor': None}, root)
        value['resource_roles'][0]['path'] = 'references/missing.md'
        with self.assertRaises((OSError, observe.ObservationError)):
            contracts.Reader().record(value, reference['path'])

    def test_binding_identity_and_timestamp(self):
        value = dict(schema_version='project-binding-v1', project_id='12345678-1234-1234-1234-123456789abc', project_root=str(self.root), revision=1, updated_at_utc='2026-09-14T23:00:00Z', bindings=[dict(name='sample', package_path='.agents/skills/sample', package_digest='a' * 64, role='core', selected=True)])
        contracts.Reader().record(value)
        for field, new in [('updated_at_utc', '2026-19-14T23:00:00Z'), ('project_id', 'invalid')]:
            bad = dict(value, **{field: new})
            with self.subTest(field=field), self.assertRaises(ValueError):
                contracts.Reader().record(bad)
        value['bindings'][0]['package_path'] = '.agents/skills/other'
        with self.assertRaisesRegex(ValueError, 'installed path'):
            contracts.Reader().record(value)

    def test_inventory_exclusion_and_capture_ceiling(self):
        (self.root / 'nested').mkdir()
        (self.root / 'nested/a.md').write_text('retained', encoding='utf-8')
        (self.root / '.env').write_text('fixture only', encoding='utf-8')
        rows, omissions = contracts.inventory(self.root, allow_exclusions=True)
        self.assertEqual([row[0] for row in rows], ['nested/a.md'])
        self.assertEqual([row['path'] for row in omissions], ['.env'])
        with self.assertRaisesRegex(ValueError, 'excluded/generated'):
            contracts.inventory(self.root)
        with (self.root / 'nested/large.bin').open('wb') as stream:
            stream.truncate(32 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(observe.ObservationError, 'ceiling'):
            contracts.inventory(self.root / 'nested')
        with self.assertRaisesRegex(observe.ObservationError, 'ceiling'):
            contracts.Reader().read(self.root / 'nested/large.bin')

    def test_parent_inventory_and_schema_alternatives(self):
        content = '```devforgeai-requirements\n[{"id":"R1","statement":"Preserve bytes."}]\n```\n'
        self.assertEqual(contracts.parent_requirements(content)['R1']['statement'], 'Preserve bytes.')
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            contracts.parent_requirements(content + content)
        with self.assertRaisesRegex(ValueError, 'no allowed'):
            contracts.validate([], {'anyOf': [{'type': 'null'}, {'type': 'integer'}]})

    def proposal(self):
        fixtures.shared(self.root)
        return json.loads((self.root / 'adaptation-proposal.json').read_text(encoding='utf-8'))

    def test_variant_lineage_requires_complete_faithful_dispositions(self):
        proposal = self.proposal()
        parent = fixtures.package(self.root, 'parent')
        root = Path(parent['root'])
        (root / 'references').mkdir()
        statement = proposal['requirements'][0]['statement']
        (root / 'references/adaptive-contract.md').write_text('| ID | Requirement |\n| --- | --- |\n| P1 | ' + statement + ' |\n', encoding='utf-8')
        rows = []
        for path in sorted(root.rglob('*')):
            if path.is_file():
                data = path.read_bytes()
                rows.append(dict(path=path.relative_to(root).as_posix(), bytes=len(data), sha256=observe.sha256(data)))
        rows.sort(key=lambda row: row['path'])
        parent.update(manifest=fixtures.write(self.root / 'parent-manifest.json', rows), package_digest=observe.sha256(observe.compact(rows)))
        member = proposal['members'][0]
        member.update(role='project_variant', parent_core=parent, lineage_delta=[dict(requirement_id='P1', disposition='retained', reason='Same obligation', replacement_requirement_ids=['REQ-7'])])
        contracts.Reader().record(proposal)
        for disposition, replacements, statement_value, valid in [
            ('retained', ['REQ-7'], 'Changed statement.', False),
            ('modified', ['REQ-7'], 'Changed statement.', True),
            ('modified', [], 'Changed statement.', False),
            ('removed', [], 'Remove P1 for this selected variant.', True),
            ('removed', [], 'Unrelated request.', False),
        ]:
            bad = copy.deepcopy(proposal)
            bad['members'][0]['lineage_delta'][0].update(disposition=disposition, replacement_requirement_ids=replacements)
            bad['requirements'][0]['statement'] = statement_value
            with self.subTest(disposition=disposition, valid=valid):
                if valid:
                    contracts.Reader().record(bad)
                else:
                    with self.assertRaises(ValueError):
                        contracts.Reader().record(bad)
        proposal['members'][0]['lineage_delta'] = []
        with self.assertRaisesRegex(ValueError, 'incomplete parent'):
            contracts.Reader().record(proposal)

    def test_expertise_and_proposal_gaps_preserve_blocked_status(self):
        proposal = self.proposal()
        proposal['members'][0]['role'] = 'expertise'
        contracts.Reader().record(proposal)
        proposal['gaps'] = [dict(code='G1', member_id='A', requirement_ids=['REQ-7'], description='Capability not available.', resolution='Supply capability.', evidence=[])]
        with self.assertRaisesRegex(ValueError, 'state mismatch'):
            contracts.Reader().record(proposal)
        proposal['state'] = 'BLOCKED'
        contracts.Reader().record(proposal)
        proposal['gaps'][0]['member_id'] = 'absent'
        with self.assertRaisesRegex(ValueError, 'unknown gap member'):
            contracts.Reader().record(proposal)

    def test_selection_changed_destination_requires_literal_authorization(self):
        self.proposal()
        selection = json.loads((self.root / 'adaptation-selection.json').read_text(encoding='utf-8'))
        destination = str(self.root / 'new/producer')
        selection['destinations'][0]['target_root'] = destination
        with self.assertRaisesRegex(ValueError, 'changed destination'):
            contracts.Reader().record(selection)
        authorization = self.root / 'selection-authorization.txt'
        authorization.write_text('Select destination ' + destination, encoding='utf-8')
        selection['authorization'] = fixtures.reference(authorization)
        contracts.Reader().record(selection)

    def test_blocked_producer_cannot_leave_dependent_retained(self):
        self.proposal()
        authored = json.loads((self.root / 'set-authoring.json').read_text(encoding='utf-8'))
        authored['members'][0].update(status='BLOCKED', package=None)
        authored['state'] = 'BLOCKED'
        with self.assertRaisesRegex(ValueError, 'dependency result'):
            contracts.Reader().record(authored)
        authored['members'][1].update(status='DEPENDENCY_BLOCKED', package=None)
        contracts.Reader().record(authored)
        authored['members'][0]['applied_paths'] = ['SKILL.md']
        with self.assertRaisesRegex(ValueError, 'partial writes'):
            contracts.Reader().record(authored)

    def test_reference_readback_detects_drift_and_invalid_locators(self):
        path = self.root / 'evidence.txt'
        path.write_text('Evidence\n\n', encoding='utf-8')
        reference = fixtures.reference(path)
        reader = contracts.Reader()
        reader.ref(reference)
        for start, end, message in [(3, 3, 'outside retained'), (2, 2, 'empty supporting')]:
            with self.assertRaisesRegex(ValueError, message):
                contracts.Reader().refs(dict(ref=reference, start_line=start, end_line=end))
        path.write_text('Changed evidence', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED'):
            reader.readback()
        with self.assertRaisesRegex(ValueError, 'STALE_REQUEST'):
            authoring_intake.reference(reference)

    def test_supplemental_binding_must_match_observed_status_and_digest(self):
        value = self.observation()
        binding = dict(schema_version='binding-observation-v1', status='UNAVAILABLE', reason_code='ABSENT', binding_sha256=None, package_digest=None, details=['No binding fixture selected.'])
        reference = fixtures.write(self.root / 'binding-observation.json', binding)
        value['bindings'] = [dict(case_id='binding-case', binding_sha256=None, observation=reference, expected='UNAVAILABLE', observed='UNAVAILABLE', effects_match=True)]
        adaptive.supplemental(value, contracts.Reader())
        value['bindings'][0]['observed'] = 'MATCH'
        with self.assertRaisesRegex(ValueError, 'binding observation mismatch'):
            adaptive.supplemental(value, contracts.Reader())

    def test_raw_package_cannot_adjudicate_unicode(self):
        value = self.observation()
        code, raw = self.call('adaptive_observe.py', ['package', '--source', str(self.root / 'sample')])
        self.assertEqual((code, raw['status']), (2, 'INCOMPLETE'))
        raw['observations']['unicode_candidates'][0]['disposition'] = 'legitimate'
        fixtures.write(self.root / 'raw.json', raw)
        checked, errors = adaptive.records(self.root)
        self.assertTrue(any('raw helper cannot adjudicate Unicode' in error for error in errors))
        self.assertNotIn('raw.json', checked)

    def test_variant_descriptor_requires_distinct_parent_identity(self):
        value = dict(schema_version='adaptive-skill-v1', name='child', role='project_variant', binding_required=True, parent_core=dict(name='parent', package_digest='a' * 64, requirement_ids=['REQ-1']), contract_path='references/adaptive-contract.md', required_capabilities=['Python 3.10+'], resource_roles=[])
        contracts.Reader().record(value)
        value['parent_core']['name'] = 'child'
        with self.assertRaisesRegex(ValueError, 'differ from parent'):
            contracts.Reader().record(value)

    def test_standalone_gaps_and_dimensions_are_validated(self):
        value = fixtures.standalone(self.root)
        value['gaps'] = [dict(code='G1', member_id='B', requirement_ids=[], description='Missing fixture.', resolution='Supply fixture.', evidence=[])]
        contracts.Reader().record(value)
        value['gaps'][0]['requirement_ids'] = ['UNKNOWN']
        with self.assertRaisesRegex(ValueError, 'unknown gap requirement'):
            contracts.Reader().record(value)
        row = text_resources.check('AV-I01', 'SKILL.md', 'PASS', 'Observed.')
        row['dimension'] = 'instructions'
        adaptive.check_rows(json.dumps(row).encode(), self.root)
        row['dimension'] = 'decorative'
        with self.assertRaisesRegex(ValueError, 'unknown dimension'):
            adaptive.check_rows(json.dumps(row).encode(), self.root)

    def authored_set(self):
        fixtures.shared(self.root)
        proposal_path = self.root / 'adaptation-proposal.json'
        proposal = json.loads(proposal_path.read_text(encoding='utf-8'))
        proposal['members'][0]['action'] = 'revise'
        proposal['state'] = 'PROPOSED'
        proposal_ref = fixtures.write(proposal_path, proposal)
        selection_path = self.root / 'adaptation-selection.json'
        selection = json.loads(selection_path.read_text(encoding='utf-8'))
        selection['proposal'] = proposal_ref
        selection_ref = fixtures.write(selection_path, selection)
        authored = json.loads((self.root / 'set-authoring.json').read_text(encoding='utf-8'))
        authored.update(selection=selection_ref, state='AUTHORED')
        row = authored['members'][0]
        target = Path(row['package']['root'])
        manifest = fixtures.write(self.root / 'delivered-manifest.json', observe.make_manifest(target))
        spec = fixtures.write(self.root / 'requirements.json', {'requirement': 'Produce task card.'})
        shared = dict(project_root=str(self.root), target_root=str(target), target_name='producer')
        contract = dict(schema_version='authoring-contract-v1', inputs=[spec], capabilities=[], expected_outputs=[], side_effects=[], **shared)
        record = dict(schema_version='authoring-v1', record_kind='authoring', authoring_state='AUTHORED', run_id='case-authored', operation='edit', authorization='Revise selected source.', inputs=[spec], contract=fixtures.write(self.root / 'contract.json', contract), prior_origin={'kind': 'observed'}, managed_paths=['SKILL.md'], retained_user_paths=[], before_manifest=manifest, candidate_manifest=manifest, delivered_manifest=manifest, applied_paths=['SKILL.md'], validation_status='NOT_PERFORMED', testing_status='NOT_PERFORMED', unresolved_issues=[], rows=[], **shared)
        record_ref = fixtures.write(self.root / 'authoring-record.json', record)
        request = dict(schema_version='validation-request-v1', record_kind='validation_request', authoring_run_id='case-authored', target_manifest=manifest, package_digest=row['package']['package_digest'], authoring_record=record_ref, specification_refs=[spec], changed_paths=['SKILL.md'], known_issues=[], capabilities=[], expected_outputs=[], side_effects=[], permission='No external effects.', **shared)
        row.update(status='AUTHORED', authoring_record=record_ref, validation_request=fixtures.write(self.root / 'validation-request.json', request), applied_paths=['SKILL.md'])
        return authored, record, request

    def test_authored_set_custody_is_bound_through_request(self):
        authored, record, request = self.authored_set()
        reader = contracts.Reader()
        reader.record(authored)
        reader.readback()
        for field, value, message in [('target_name', 'other', 'authoring member mismatch'), ('applied_paths', [], 'authoring member mismatch')]:
            bad = copy.deepcopy(authored)
            changed = dict(record, **{field: value})
            bad['members'][0]['authoring_record'] = fixtures.write(self.root / 'altered-authoring.json', changed)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message):
                contracts.Reader().record(bad)
        changed = dict(request, package_digest='0' * 64)
        authored['members'][0]['validation_request'] = fixtures.write(self.root / 'altered-request.json', changed)
        with self.assertRaisesRegex(ValueError, 'authoring request mismatch'):
            contracts.Reader().record(authored)

    def assessment(self):
        selected = fixtures.standalone(self.root / 'inputs')
        input_ref = fixtures.write(self.root / 'selected.json', selected)
        members = []
        for member in selected['members']:
            name = member['member_id']
            rows = [dict(text_resources.check(rule, 'SKILL.md', 'PASS', 'Independent fixture passed.'), run_id=name, check_id=name + '-' + rule) for rule in adaptive.ALL_RULES]
            path = self.root / (name + '.jsonl')
            path.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
            report = self.root / (name + '.md')
            report.write_text('All fixture checks completed.', encoding='utf-8')
            members.append(dict(member_id=name, package_digest=member['package']['package_digest'], report=fixtures.reference(report), checks=fixtures.reference(path), outcome='PASS', source_state='UNCHANGED', reason='All fixture checks complete.'))
        integration = dict(text_resources.check('AV-A10', 'handoffs/card', 'PASS', 'Exact task card schema preserved.'), run_id='assessment')
        path = self.root / 'integration.jsonl'
        path.write_text(json.dumps(integration), encoding='utf-8')
        count = 2 * len(adaptive.ALL_RULES) + 1
        return dict(schema_version='set-assessment-v1', run_id='assessment', input=input_ref, scope='full_set', omitted_member_ids=[], omitted_handoff_ids=[], members=members, integration_checks=fixtures.reference(path), outcome='PASS', assessment_completed=True, required_evaluated=count, required_total=count, unknown_applicability=0, limitations=[], prior_assessment=None)

    def test_missing_report_preserves_failed_checks_in_aggregate(self):
        value = self.assessment()
        adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')
        value['members'][0].update(report=None, outcome='INCOMPLETE')
        checks_path = Path(value['members'][0]['checks']['path'])
        rows = [json.loads(line) for line in checks_path.read_text(encoding='utf-8').splitlines()]
        rows[0].update(result='FAIL', reason='Malformed metadata observed.')
        checks_path.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
        value['members'][0]['checks'] = fixtures.reference(checks_path)
        value['outcome'] = 'FAIL'
        adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')
        value['outcome'] = 'INCOMPLETE'
        with self.assertRaisesRegex(ValueError, 'set outcome'):
            adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')

    def test_set_gaps_and_prior_linkage_cannot_be_hidden(self):
        value = self.assessment()
        previous = dict(value, run_id='prior')
        value['prior_assessment'] = fixtures.write(self.root / 'prior.json', previous)
        adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')
        previous['run_id'] = value['run_id']
        value['prior_assessment'] = fixtures.write(self.root / 'prior.json', previous)
        with self.assertRaisesRegex(ValueError, 'prior assessment linkage'):
            adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')
        value['prior_assessment'] = None
        selected_path = Path(value['input']['path'])
        selected = json.loads(selected_path.read_text(encoding='utf-8'))
        selected['gaps'] = [dict(code='MISSING', member_id='A', requirement_ids=[], description='Missing native activation.', resolution='Observe native activation.', evidence=[])]
        value['input'] = fixtures.write(selected_path, selected)
        value['outcome'] = 'INCOMPLETE'
        adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')
        value['outcome'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'set outcome'):
            adaptive.assess_record(value, contracts.Reader(), self.root / 'assessment.json')

    def test_aggregate_reader_limit_counts_distinct_references(self):
        paths = [self.root / name for name in ('first.bin', 'second.bin')]
        for path in paths:
            with path.open('wb') as stream:
                stream.truncate(17 * 1024 * 1024)
        reader = contracts.Reader()
        self.assertEqual(len(reader.read(paths[0])), 17 * 1024 * 1024)
        self.assertEqual(len(reader.read(paths[0])), 17 * 1024 * 1024)
        with self.assertRaisesRegex(observe.ObservationError, 'aggregate capture ceiling'):
            reader.read(paths[1])

    def test_raw_pending_observation_cannot_claim_complete_status(self):
        self.observation()
        _, raw = self.call('adaptive_observe.py', ['package', '--source', str(self.root / 'sample')])
        raw_path = self.root / 'raw.json'
        raw['observations']['unicode_candidates'][0]['end_byte'] = 999999
        fixtures.write(raw_path, raw)
        self.assertTrue(any('raw Unicode interval' in item for item in adaptive.records(self.root)[1]))
        raw['observations']['unicode_candidates'][0]['end_byte'] = raw['observations']['unicode_candidates'][0]['start_byte'] + 3
        raw['status'] = 'OBSERVED'
        fixtures.write(raw_path, raw)
        self.assertTrue(any('hides pending observations' in item for item in adaptive.records(self.root)[1]))

    def test_wrong_input_family_is_cli_mismatch(self):
        reference = fixtures.write(self.root / 'not-a-set.json', {'schema_version': 'binding-observation-v1'})
        code, result = self.call('adaptive_observe.py', ['intake-set', '--request', reference['path'], '--request-sha256', reference['sha256']])
        self.assertEqual((code, result['status']), (1, 'MISMATCH'))
        self.assertTrue(any('unsupported set input' in item for item in result['limitations']))

    def test_schema1_records_stay_with_original_record_checker(self):
        fixtures.write(self.root / 'legacy.json', {'schema_version': '1'})
        checked, errors = adaptive.records(self.root)
        self.assertEqual(checked, [])
        self.assertTrue(any('use observe.py' in item for item in errors))

    def test_parent_table_ends_before_unrelated_content(self):
        content = '| ID | Requirement |\n| --- | --- |\n| R1 | Preserve input. |\n\nUnrelated prose\n| X | Unrelated table |\n'
        self.assertEqual(set(contracts.parent_requirements(content)), {'R1'})

    def test_prior_proposal_chain_is_byte_bound(self):
        proposal = self.proposal()
        prior = fixtures.write(self.root / 'prior-proposal.json', proposal)
        proposal = dict(proposal, run_id='next-proposal', prior_proposal=prior)
        contracts.Reader().record(proposal)
        Path(prior['path']).write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'STALE_REFERENCE'):
            contracts.Reader().record(proposal)

    def request(self):
        target = Path(fixtures.package(self.root, 'sample')['root'])
        manifest = fixtures.write(self.root / 'manifest.json', observe.make_manifest(target))
        spec = fixtures.write(self.root / 'spec.json', {'requirement': 'Preserve source.'})
        shared = dict(project_root=str(self.root), target_root=str(target), target_name='sample', capabilities=[], expected_outputs=[], side_effects=[])
        contract = dict(schema_version='authoring-contract-v1', inputs=[spec], **shared)
        record = dict(schema_version='authoring-v1', record_kind='authoring', authoring_state='AUTHORED', run_id='authoring-case', delivered_manifest=manifest, applied_paths=['SKILL.md'], unresolved_issues=[], inputs=[spec], contract=fixtures.write(self.root / 'contract.json', contract), prior_origin='observed', **shared)
        record_ref = fixtures.write(self.root / 'authoring.json', record)
        request = dict(schema_version='validation-request-v1', record_kind='validation_request', authoring_run_id='authoring-case', target_manifest=manifest, package_digest=observe.make_manifest(target)['package_digest'], authoring_record=record_ref, specification_refs=[spec], changed_paths=['SKILL.md'], known_issues=[], permission='No external effects.', **shared)
        return request, record, contract

    def test_authoring_intake_entrypoint_and_corruption(self):
        request, record, contract = self.request()
        reference = fixtures.write(self.root / 'request.json', request)
        code, result = self.call('authoring_intake.py', ['--request', reference['path'], '--request-sha256', reference['sha256']])
        self.assertEqual((code, result['status']), (0, 'BOUND'))
        self.assertEqual(result['quality_status'], 'NOT_PERFORMED')
        code, result = self.call('authoring_intake.py', ['--request', reference['path'], '--request-sha256', '0' * 64])
        self.assertEqual((code, result['status']), (1, 'REJECTED'))
        for field, new, message in [('schema_version', 'other', 'shape/version'), ('target_name', 'other', 'identity'), ('package_digest', '0' * 64, 'target bytes'), ('authoring_run_id', 'other', 'identity'), ('changed_paths', [], 'delivery/request'), ('capabilities', ['new'], 'contract/request')]:
            bad = dict(request, **{field: new})
            reference = fixtures.write(self.root / 'request.json', bad)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message):
                authoring_intake.intake(reference['path'], reference['sha256'])
        record['authoring_state'] = 'PARTIAL'
        request['authoring_record'] = fixtures.write(self.root / 'authoring.json', record)
        reference = fixtures.write(self.root / 'request.json', request)
        with self.assertRaisesRegex(ValueError, 'completed authoring'):
            authoring_intake.intake(reference['path'], reference['sha256'])
        with self.assertRaisesRegex(ValueError, 'invalid file reference'):
            authoring_intake.reference({})


if __name__ == '__main__':
    unittest.main()
