"""Independent maintenance fixtures/oracles; no campaign shipped in builder.

Expected results are asserted from the frozen BAT contract before execution.
Each run receives a fresh ADAPTIVE_TEST_ROOT; trial files remain for review.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
import uuid

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[3]
BUILDER = PROJECT / 'src/agents/skills/skill-builder'
sys.path.insert(0, str(BUILDER / 'scripts'))
import adaptive as a
import authoring as old

TRIALS = Path(os.environ['ADAPTIVE_TEST_ROOT'])
RUNTIME = BUILDER / 'assets/adaptive-runtime/check_project_binding.py'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    return reference(path)


def reference(path):
    return {'path': str(path.resolve()), 'sha256': sha(path.read_bytes())}


def manifest(root):
    # Independent fixture oracle over our own known regular-file trees.
    rows = [{'path': p.relative_to(root).as_posix(), 'bytes': len(p.read_bytes()), 'sha256': sha(p.read_bytes())}
            for p in sorted(root.rglob('*')) if p.is_file()]
    rows.sort(key=lambda r: r['path'])
    return rows, sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode())


def package(root, role='core', parent=None):
    root.mkdir(parents=True, exist_ok=False)
    (root / 'SKILL.md').write_text('---\nname: ' + root.name + '\ndescription: Summarize supplied synthetic notes.\n---\nRead [contract](references/adaptive-contract.md) and [descriptor](assets/devforgeai-skill.json).\nRun scripts/check_project_binding.py before product writes; on non-MATCH stop.\n', encoding='utf-8')
    contract = '# Synthetic contract\nOwn notes; no network or unrelated writes. Input notes.txt, output out/summary.txt.\nCompletion: summary contains supplied note facts.\n```devforgeai-requirements\n' + json.dumps([{'id': 'R1', 'statement': 'Keep supplied facts.'}, {'id': 'R2', 'statement': 'Use local files.'}, {'id': 'R3', 'statement': 'Preserve inputs.'}]) + '\n```\n'
    (root / 'references').mkdir()
    (root / 'references/adaptive-contract.md').write_text(contract, encoding='utf-8')
    (root / 'scripts').mkdir()
    shutil.copyfile(RUNTIME, root / 'scripts/check_project_binding.py')
    descriptor = {'schema_version': 'adaptive-skill-v1', 'name': root.name, 'role': role, 'binding_required': True, 'parent_core': parent, 'contract_path': 'references/adaptive-contract.md', 'required_capabilities': ['Python 3.10+'], 'resource_roles': [{'path': 'scripts/check_project_binding.py', 'role': 'runtime', 'reason': 'Checks binding before product actions.'}]}
    write(root / 'assets/devforgeai-skill.json', descriptor)
    return descriptor


class AdaptiveTests(unittest.TestCase):
    def setUp(self):
        self.root = TRIALS / self._testMethodName
        self.root.mkdir(parents=True, exist_ok=False)
        self.sequence = 0

    def run_cli(self, script, arguments):
        self.sequence += 1
        command = [sys.executable, '-B', '-X', 'utf8', str(script), *map(str, arguments)]
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True, encoding='utf-8', timeout=120)
        prefix = self.root / ('command-' + str(self.sequence))
        write(prefix.with_suffix('.json'), {'command': command, 'exit_code': result.returncode, 'timeout_seconds': 120})
        prefix.with_suffix('.stdout').write_text(result.stdout, encoding='utf-8')
        prefix.with_suffix('.stderr').write_text(result.stderr, encoding='utf-8')
        return result

    def inspect(self, value, expected=0):
        path = self.root / ('record-' + str(self.sequence) + '.json')
        write(path, value)
        result = self.run_cli(BUILDER / 'scripts/adaptive.py', ['inspect', '--record', path])
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual([], output['ordered_member_ids'])
        return output

    def proposal(self):
        raw = self.root / 'inputs/requirements.md'
        raw.parent.mkdir()
        raw.write_text('Storage owns note persistence. Existing HTTP skill owns HTTP.\nKeep supplied facts.\n', encoding='utf-8')
        loc = {'ref': reference(raw), 'start_line': 1, 'end_line': 2}
        evidence = {'schema_version': 'project-evidence-v1', 'run_id': 'fixture', 'project_root': str(self.root), 'scope_roots': [str(raw.parent)], 'inputs': [reference(raw)], 'facts': [{'id': 'domain', 'category': 'domain', 'statement': 'Storage persists notes.', 'basis': 'observed', 'sources': [loc]}], 'exclusions': [], 'complete': True, 'capabilities': [], 'gaps': []}
        reqs = [{'id': 'R1', 'origin': 'source', 'statement': 'Keep supplied facts.', 'source_refs': [loc], 'rationale': None, 'verification': 'Output retains supplied facts.'}]
        member = {'id': 'A', 'name': 'notes-a', 'role': 'expertise', 'action': 'create', 'target_root': str(self.root / 'skills/notes-a'), 'existing_package': None, 'parent_core': None, 'responsibility': 'Persist supplied notes.', 'exclusions': ['HTTP'], 'triggers': ['Persist notes'], 'near_misses': ['Serve HTTP'], 'requirement_ids': ['R1'], 'fact_ids': ['domain'], 'rationale': 'Unmet note persistence responsibility.', 'depends_on': [], 'capabilities': [], 'lineage_delta': []}
        proposal = {'schema_version': 'adaptation-proposal-v1', 'run_id': 'fixture', 'mode': 'propose', 'project_evidence': write(self.root / 'evidence.json', evidence), 'prior_proposal': None, 'requirements': reqs, 'members': [member], 'handoffs': [], 'gaps': [], 'state': 'PROPOSED'}
        return proposal

    def selection(self, proposal):
        auth = self.root / 'authorization.txt'
        auth.write_text('Create the selected members at the supplied destinations.\n', encoding='utf-8')
        return {'schema_version': 'adaptation-selection-v1', 'proposal': write(self.root / 'proposal.json', proposal), 'member_ids': [m['id'] for m in proposal['members']], 'destinations': [{'member_id': m['id'], 'target_root': m['target_root']} for m in proposal['members']], 'authorization': reference(auth), 'permitted_effects': ['Author selected synthetic development packages.']}

    def package_ref(self, root):
        rows, digest = manifest(root)
        return {'name': root.name, 'root': str(root), 'manifest': write(self.root / (root.name + '-manifest.json'), rows), 'package_digest': digest}

    def operational(self, role='core'):
        project = self.root / "project café & $x; (safe) '"
        skill = project / '.agents/skills/notes-a'
        package(skill, role)
        binding = {'schema_version': 'project-binding-v1', 'project_id': str(uuid.uuid4()), 'project_root': str(project), 'revision': 1, 'bindings': [{'name': skill.name, 'package_path': '.agents/skills/' + skill.name, 'package_digest': manifest(skill)[1], 'role': role, 'selected': True}], 'updated_at_utc': '2026-09-13T00:00:00Z'}
        return project, skill, binding

    def check_binding(self, project, skill, value, expected, code):
        binding_path = project / '.agents/devforgeai/project-binding.json'
        if value is not None:
            write(binding_path, value)
        before = manifest(skill)
        result = self.run_cli(skill / 'scripts/check_project_binding.py', ['--project-root', project, '--skill-root', skill])
        output = json.loads(result.stdout)
        self.assertEqual(code, result.returncode, result.stdout)
        self.assertEqual(expected, output['reason_code'])
        self.assertNotRegex(result.stdout + result.stderr, r'[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}')
        self.assertEqual(before, manifest(skill))
        self.assertFalse((project / 'out').exists())

    def test_BAT08_valid_and_closed_records(self):
        p = self.proposal()
        self.inspect(p)
        for label, mutate in [('extra', lambda x: x.update(extra=True)), ('version', lambda x: x.update(schema_version='adaptation-proposal-v2')), ('id', lambda x: x['members'][0].update(id='bad id')), ('unresolved', lambda x: x['members'][0].update(requirement_ids=['missing'])), ('digest', lambda x: x['project_evidence'].update(sha256='A' * 64))]:
            with self.subTest(label=label):
                bad = copy.deepcopy(p)
                mutate(bad)
                self.inspect(bad, 1)

    def test_BAT08_strict_json(self):
        for index, raw in enumerate(['{"schema_version":"x","schema_version":"x"}', '{"x":NaN}', '{"x":1e999}', '[true]']):
            path = self.root / (str(index) + '.json')
            path.write_text(raw)
            result = self.run_cli(BUILDER / 'scripts/adaptive.py', ['inspect', '--record', path])
            self.assertEqual(1, result.returncode)

    def test_BAT08_schema_paths_dates(self):
        doc = json.loads((BUILDER / 'schemas/adaptive-common.schema.json').read_text())
        schema = doc['$defs']['RelPath']
        for good in ['scripts/check_project_binding.py', 'assets/a0.json', 'café & a.txt']:
            a.validate_shape(good, schema, doc)
        for bad in ['../x', 'x/../y', 'x//y', '/x', 'C:/x', 'x\\y', 'x\0y']:
            with self.assertRaises(ValueError, msg=repr(bad)):
                a.validate_shape(bad, schema, doc)
        project, skill, binding = self.operational()
        a.shape(binding)
        with self.assertRaises(ValueError):
            a.shape({**binding, 'revision': True})

    def test_BAT07_runtime_binding_matrix(self):
        project, skill, binding = self.operational()
        self.check_binding(project, skill, None, 'MISSING_BINDING', 1)
        self.check_binding(project, skill, binding, 'BOUND', 0)
        wrong = copy.deepcopy(binding)
        wrong['project_root'] = str(self.root)
        self.check_binding(project, skill, wrong, 'ROOT_MISMATCH', 1)
        inactive = copy.deepcopy(binding)
        inactive['bindings'][0]['selected'] = False
        self.check_binding(project, skill, inactive, 'NOT_SELECTED', 1)
        duplicate = copy.deepcopy(binding)
        duplicate['bindings'].append(duplicate['bindings'][0])
        self.check_binding(project, skill, duplicate, 'INVALID_BINDING', 1)
        changed = copy.deepcopy(binding)
        changed['bindings'][0]['package_digest'] = '0' * 64
        self.check_binding(project, skill, changed, 'PACKAGE_CHANGED', 1)
        wrong_role = copy.deepcopy(binding)
        wrong_role['bindings'][0]['role'] = 'expertise'
        self.check_binding(project, skill, wrong_role, 'ROLE_MISMATCH', 1)
        future = copy.deepcopy(binding)
        future['schema_version'] = 'project-binding-v2'
        self.check_binding(project, skill, future, 'INVALID_BINDING', 1)

    def test_BAT07_ambiguous_core_variants(self):
        project, skill, binding = self.operational()
        variant = project / '.agents/skills/notes-variant'
        package(variant, 'project_variant', {'name': skill.name, 'package_digest': manifest(skill)[1], 'requirement_ids': ['R1', 'R2', 'R3']})
        binding['bindings'].append({'name': variant.name, 'package_path': '.agents/skills/' + variant.name, 'package_digest': manifest(variant)[1], 'role': 'project_variant', 'selected': True})
        self.check_binding(project, skill, binding, 'AMBIGUOUS_ROLE', 1)
        binding['bindings'][0]['selected'] = False
        self.check_binding(project, variant, binding, 'BOUND', 0)

    def test_BAT06_portability_identity_and_unbound(self):
        project, skill, binding = self.operational()
        moved = self.root / 'relocated/notes-a'
        shutil.copytree(skill, moved)
        self.assertEqual(manifest(skill), manifest(moved))
        for path in moved.rglob('*'):
            if path.is_file():
                data = path.read_bytes()
                self.assertNotIn(str(project).encode(), data)
                self.assertNotIn(binding['project_id'].encode(), data)
        self.check_binding(project, moved, binding, 'UNBOUND_SKILL', 1)

    def test_BAT03_capture_ceilings(self):
        many = self.root / 'many'
        many.mkdir()
        for n in range(2001):
            (many / str(n)).write_bytes(b'')
        with self.assertRaisesRegex(a.runtime.BindingError, 'CAPTURE_LIMIT'):
            a.runtime.Capture().inventory(many)
        large = self.root / 'large'
        large.mkdir()
        with (large / 'oversized').open('wb') as stream:
            stream.truncate(32 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(a.runtime.BindingError, 'CAPTURE_LIMIT'):
            a.runtime.Capture().inventory(large)

    def test_BAT11_cycle_missing_and_occupied(self):
        p = self.proposal()
        p['members'][0]['depends_on'] = ['missing']
        self.inspect(p, 1)
        p['members'][0]['depends_on'] = ['A']
        self.inspect(p, 1)
        p['members'][0]['depends_on'] = []
        selection = self.selection(p)
        selected_path = self.root / 'selection.json'
        write(selected_path, selection)
        good = self.run_cli(BUILDER / 'scripts/adaptive.py', ['plan-set', '--selection', selected_path])
        self.assertEqual(0, good.returncode, good.stdout)
        Path(p['members'][0]['target_root']).mkdir(parents=True)
        bad = self.run_cli(BUILDER / 'scripts/adaptive.py', ['plan-set', '--selection', selected_path])
        self.assertEqual(1, bad.returncode)
        self.assertIn('occupied', bad.stdout)

    def test_BAT16_stale_locator_and_evidence(self):
        p = self.proposal()
        selection = self.selection(p)
        self.inspect(selection)
        (self.root / 'inputs/requirements.md').write_text('Changed user input')
        self.inspect(selection, 1)

    def test_BAT05_parent_full_dispositions_and_preservation(self):
        p = self.proposal()
        core = self.root / 'captured/notes-core'
        package(core)
        before = manifest(core)
        p['members'][0].update(role='project_variant', parent_core=self.package_ref(core), lineage_delta=[])
        self.inspect(p, 1)
        for ident, statement in [('R2', 'Use local files.'), ('R3', 'Preserve inputs.')]:
            p['requirements'].append({**copy.deepcopy(p['requirements'][0]), 'id': ident, 'statement': statement})
        p['members'][0]['requirement_ids'] = ['R1', 'R2', 'R3']
        p['members'][0]['lineage_delta'] = [{'requirement_id': ident, 'disposition': 'retained', 'reason': 'Unchanged required behavior.', 'replacement_requirement_ids': [ident]} for ident in ['R1', 'R2', 'R3']]
        self.inspect(p)
        p['members'][0]['lineage_delta'][-1].update(disposition='removed', replacement_requirement_ids=[])
        self.inspect(p, 1)
        self.assertEqual(before, manifest(core))

    def test_BAT10_independent_continuation_and_subset(self):
        p = self.proposal()
        for ident in ['B', 'C']:
            member = copy.deepcopy(p['members'][0])
            member.update(id=ident, name='notes-' + ident.lower(), target_root=str(self.root / ('skills/notes-' + ident.lower())), depends_on=['A'] if ident == 'B' else [])
            p['members'].append(member)
        selection = self.selection(p)
        selection_ref = write(self.root / 'selection.json', selection)
        statuses = []
        for ident in ['A', 'B', 'C']:
            member = next(m for m in p['members'] if m['id'] == ident)
            if ident == 'B':
                statuses.append({'member_id': ident, 'status': 'DEPENDENCY_BLOCKED', 'authoring_record': None, 'validation_request': None, 'package': None, 'reason': 'Required A failed.', 'applied_paths': []})
                continue
            target = Path(member['target_root'])
            contract = {'schema_version': 'authoring-contract-v1', 'run_id': ident, 'project_root': str(self.root), 'target_root': str(target), 'target_name': target.name, 'operation': 'create', 'authorization': 'Create selected synthetic member.', 'history_review': 'no_known_history', 'change_paths': ['SKILL.md', 'references/adaptive-contract.md', 'assets/devforgeai-skill.json', 'scripts/check_project_binding.py'], 'requirements': p['requirements'], 'capabilities': [], 'expected_outputs': [], 'side_effects': [], 'inputs': [], 'known_issues': []}
            contract_path = self.root / (ident + '-contract.json')
            write(contract_path, contract)
            run = self.root / 'docs/plan/skill-authorings' / target.name / ident
            old.begin(contract_path, run)
            if ident == 'A':
                (run / 'candidate/outside-scope').write_text('Injected unauthorized candidate output')
            else:
                staging = self.root / 'staging' / target.name
                package(staging, 'expertise')
                shutil.copytree(staging, run / 'candidate', dirs_exist_ok=True)
            outcome = old.publish(run)
            self.assertEqual('BLOCKED' if ident == 'A' else 'AUTHORED', outcome['state'])
            statuses.append({'member_id': ident, 'status': outcome['state'], 'authoring_record': reference(run / 'authoring-record.json'), 'validation_request': reference(run / 'validation-request.json') if ident == 'C' else None, 'package': self.package_ref(target) if ident == 'C' else None, 'reason': 'Actual custody publication outcome.', 'applied_paths': outcome['applied_paths']})
        result = {'schema_version': 'set-authoring-v1', 'run_id': 'set', 'selection': selection_ref, 'ordered_member_ids': ['A', 'B', 'C'], 'members': statuses, 'state': 'PARTIAL', 'validation_status': 'NOT_PERFORMED', 'testing_status': 'NOT_PERFORMED', 'issues': []}
        self.inspect(result)
        request = {'schema_version': 'set-validation-request-v1', 'run_id': 'set', 'selection': selection_ref, 'set_authoring': write(self.root / 'set-authoring.json', result), 'scope': 'eligible_subset', 'members': [{'member_id': 'C', 'package': statuses[2]['package'], 'request': statuses[2]['validation_request'], 'adaptive_descriptor': reference(Path(statuses[2]['package']['root']) / 'assets/devforgeai-skill.json')}], 'handoffs': [], 'omitted_member_ids': ['A', 'B'], 'omitted_handoff_ids': [], 'permission': 'No external effects are granted.'}
        self.inspect(request)
        self.inspect({**request, 'scope': 'full_set'}, 1)
        self.inspect({**request, 'omitted_member_ids': ['A']}, 1)
        self.assertFalse(Path(p['members'][0]['target_root']).exists())
        self.assertFalse(Path(p['members'][1]['target_root']).exists())

    def test_BAT15_excluded_file_and_usage(self):
        project, skill, binding = self.operational()
        (skill / '__pycache__').mkdir()
        (skill / '__pycache__/unexpected.pyc').write_bytes(b'generated')
        self.check_binding(project, skill, binding, 'UNSAFE_PATH', 1)
        result = self.run_cli(RUNTIME, [])
        self.assertEqual(2, result.returncode)
        self.assertEqual('', result.stdout)

    def test_BAT03_required_capability(self):
        p = self.proposal()
        p['members'][0]['capabilities'] = [{'id': 'rust-enforcement', 'command': 'Required actual Rust phase enforcement', 'required': True, 'observed': 'unavailable', 'evidence': None, 'limitation': 'No implemented selected runtime.'}]
        selection = self.selection(p)
        path = self.root / 'selection.json'
        write(path, selection)
        result = self.run_cli(BUILDER / 'scripts/adaptive.py', ['plan-set', '--selection', path])
        self.assertEqual(1, result.returncode)
        self.assertIn('capability', result.stdout)

    def test_BAT03_evidence_gap_blocks_selection(self):
        p = self.proposal()
        evidence_path = self.root / 'evidence.json'
        evidence = json.loads(evidence_path.read_text())
        evidence['gaps'] = [{'code': 'CONFLICTING_CONVENTION', 'member_id': None, 'requirement_ids': [], 'description': 'Same-scope conventions conflict.', 'resolution': 'Current user selects the intended convention.', 'evidence': []}]
        p['project_evidence'] = write(evidence_path, evidence)
        p['state'] = 'BLOCKED'
        selection = self.selection(p)
        path = self.root / 'selection.json'
        write(path, selection)
        result = self.run_cli(BUILDER / 'scripts/adaptive.py', ['plan-set', '--selection', path])
        self.assertEqual(1, result.returncode)
        self.assertIn('project evidence has unresolved gap', result.stdout)

    def test_BAT09_legacy_schema_bytes_preserved(self):
        before = json.loads((RUN / 'builder-before.json').read_text())
        for row in before['files']:
            if (row['path'].startswith('schemas/') or row['path'].startswith('scripts/')) and row['path'] != 'scripts/authoring.py':
                self.assertEqual(row['sha256'], sha((BUILDER / row['path']).read_bytes()), row['path'])

    def test_BAT11_deterministic_order_and_aggregate(self):
        members = {'C': {'depends_on': []}, 'B': {'depends_on': ['A']}, 'A': {'depends_on': []}}
        self.assertEqual(['A', 'B', 'C'], a.topology(members))
        for states, expected in [(['RETAINED'], 'NO_CHANGE'), (['RETAINED', 'BLOCKED'], 'BLOCKED'), (['AUTHORED', 'RETAINED'], 'AUTHORED'), (['AUTHORED', 'DEPENDENCY_BLOCKED'], 'PARTIAL')]:
            self.assertEqual(expected, a.aggregate([{'status': x, 'applied_paths': []} for x in states]))

    def test_BAT08_full_set_and_handoff_omissions(self):
        p = self.proposal()
        for ident in ['B', 'C']:
            member = copy.deepcopy(p['members'][0])
            member.update(id=ident, name='notes-' + ident.lower(), target_root=str(self.root / ('skills/notes-' + ident.lower())), depends_on=['A'] if ident == 'B' else [])
            p['members'].append(member)
        p['state'] = 'NO_CHANGE'
        for member in p['members']:
            root = Path(member['target_root'])
            package(root, 'expertise')
            member.update(action='retain', existing_package=self.package_ref(root))
        schema_ref = write(self.root / 'card.schema.json', {'type': 'object', 'required': ['summary'], 'properties': {'summary': {'type': 'string'}}, 'additionalProperties': False})
        p['handoffs'] = [{'id': 'H1', 'producer': 'A', 'consumer': 'B', 'artifact_role': 'summary', 'format': 'json', 'schema_ref': schema_ref, 'contract': 'summary string contains source facts.', 'required': True, 'failure_behavior': 'block_consumer'}]
        selection = self.selection(p)
        selection_ref = write(self.root / 'selection.json', selection)
        rows = [{'member_id': m['id'], 'status': 'RETAINED', 'authoring_record': None, 'validation_request': None, 'package': m['existing_package'], 'reason': 'Already covers selected responsibility.', 'applied_paths': []} for m in p['members']]
        result = {'schema_version': 'set-authoring-v1', 'run_id': 'retained', 'selection': selection_ref, 'ordered_member_ids': ['A', 'B', 'C'], 'members': rows, 'state': 'NO_CHANGE', 'validation_status': 'NOT_PERFORMED', 'testing_status': 'NOT_PERFORMED', 'issues': []}
        request = {'schema_version': 'set-validation-request-v1', 'run_id': 'retained', 'selection': selection_ref, 'set_authoring': write(self.root / 'set.json', result), 'scope': 'full_set', 'members': [{'member_id': m['id'], 'package': m['existing_package'], 'request': None, 'adaptive_descriptor': reference(Path(m['target_root']) / 'assets/devforgeai-skill.json')} for m in p['members']], 'handoffs': p['handoffs'], 'omitted_member_ids': [], 'omitted_handoff_ids': [], 'permission': 'No external effects are granted.'}
        self.inspect(request)
        subset = copy.deepcopy(request)
        subset.update(scope='eligible_subset', members=[request['members'][2]], handoffs=[], omitted_member_ids=['A', 'B'], omitted_handoff_ids=['H1'])
        self.inspect(subset)
        self.inspect({**subset, 'omitted_handoff_ids': []}, 1)
        self.inspect({**subset, 'members': [request['members'][1]], 'omitted_member_ids': ['A', 'C']}, 1)
        # Internally bound retained package must still implement selected role.
        p['members'][0]['role'] = 'core'
        selection['proposal'] = write(self.root / 'proposal-role-change.json', p)
        selection_ref = write(self.root / 'selection-role-change.json', selection)
        result['selection'] = selection_ref
        wrong_role = {**request, 'selection': selection_ref, 'set_authoring': write(self.root / 'set-role-change.json', result)}
        observation = self.inspect(wrong_role, 1)
        self.assertIn('delivered role differs', observation['errors'][0])

    def test_BAT13_equivalent_parent_change_then_missing_requirement(self):
        p = self.proposal()
        core = self.root / 'parent-before/notes-core'
        package(core)
        parent_ref = self.package_ref(core)
        variant = Path(p['members'][0]['target_root'])
        package(variant, 'project_variant', {'name': core.name, 'package_digest': parent_ref['package_digest'], 'requirement_ids': ['R1', 'R2', 'R3']})
        for ident, statement in [('R2', 'Use local files.'), ('R3', 'Preserve inputs.')]:
            p['requirements'].append({**copy.deepcopy(p['requirements'][0]), 'id': ident, 'statement': statement})
        member = p['members'][0]
        member.update(role='project_variant', action='retain', existing_package=self.package_ref(variant), parent_core=parent_ref, requirement_ids=['R1', 'R2', 'R3'], lineage_delta=[{'requirement_id': x, 'disposition': 'retained', 'reason': 'Equivalent required behavior.', 'replacement_requirement_ids': [x]} for x in ['R1', 'R2', 'R3']])
        p['state'] = 'NO_CHANGE'
        self.inspect(p)
        prior = write(self.root / 'prior-proposal.json', p)
        current = self.root / 'parent-after/notes-core'
        shutil.copytree(core, current)
        (current / 'comment.txt').write_text('A documentation-only byte change.')
        rows, digest = manifest(current)
        changed_ref = {'name': current.name, 'root': str(current), 'manifest': write(self.root / 'current-parent-manifest.json', rows), 'package_digest': digest}
        review = copy.deepcopy(p)
        review.update(mode='review_updates', prior_proposal=prior, state='PROPOSED')
        review['members'][0]['parent_core'] = changed_ref
        self.inspect(review)
        self.inspect({**review, 'state': 'NO_CHANGE'}, 1)
        before = manifest(core)
        contract = current / 'references/adaptive-contract.md'
        contract.write_text('```devforgeai-requirements\n[{"id":"R1","statement":"Keep supplied facts."}]\n```\n')
        rows, digest = manifest(current)
        review['members'][0]['parent_core'] = {**changed_ref, 'manifest': write(self.root / 'removed-parent-manifest.json', rows), 'package_digest': digest}
        self.inspect(review, 1)
        self.assertEqual(before, manifest(core))

    def test_BAT07_malformed_descriptor_and_extra_package_files(self):
        project, skill, binding = self.operational()
        desc_path = skill / 'assets/devforgeai-skill.json'
        desc = json.loads(desc_path.read_text())
        write(desc_path, {**desc, 'unexpected': True})
        self.check_binding(project, skill, binding, 'INVALID_BINDING', 1)
        write(desc_path, desc)
        (skill / 'unexpected.txt').write_text('Unbound additional bytes.')
        self.check_binding(project, skill, binding, 'PACKAGE_CHANGED', 1)

    def test_BAT05_ordinary_parent_index_and_BAT16_readback(self):
        core = self.root / 'ordinary-core'
        core.mkdir()
        (core / 'SKILL.md').write_text('---\nname: ordinary-core\ndescription: Use for local notes.\n---\n| ID | Requirement |\n| --- | --- |\n| R1 | Preserve facts. |\n')
        reader = a.Reader()
        self.assertEqual({'R1': {'id': 'R1', 'statement': 'Preserve facts.'}}, reader.requirement_index(core))
        reader.package(self.package_ref(core))
        reader.readback()
        (core / 'extra.md').write_text('Changed after input inspection.')
        with self.assertRaisesRegex(ValueError, 'STALE_PACKAGE'):
            reader.readback()
        proposal = self.proposal()
        proposal['run_id'] = 'invalid\n'
        with self.assertRaises(ValueError):
            a.shape(proposal)

    def test_BAT02_link_rejection(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'marker').write_text('Excluded content.')
        package_root = self.root / 'package'
        package_root.mkdir()
        link = package_root / 'escape'
        if os.name == 'nt':
            result = subprocess.run(['powershell', '-NoProfile', '-Command', 'New-Item', '-ItemType', 'Junction', '-Path', str(link), '-Target', str(outside)], capture_output=True, timeout=15)
            if result.returncode:
                self.skipTest('Windows junction creation unavailable; no bypass.')
        else:
            link.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(a.runtime.BindingError, 'UNSAFE_PATH'):
            a.runtime.Capture().inventory(package_root)


if __name__ == '__main__':
    unittest.main(verbosity=2)
