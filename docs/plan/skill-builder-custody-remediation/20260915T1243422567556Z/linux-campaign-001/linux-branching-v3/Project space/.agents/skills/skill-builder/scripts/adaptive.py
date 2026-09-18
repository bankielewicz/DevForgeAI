"""Read-only adaptive record custody and selected-set planning. No quality execution.

inspect --record FILE; plan-set --selection FILE. Python 3.10+ standard library;
The generic runtime interprets the supported frontmatter name scalar.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('adaptive_binding_runtime', PACKAGE / 'assets/adaptive-runtime/check_project_binding.py')
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)
import authoring
import record_schema

VERSIONS = {'project-evidence-v1', 'adaptation-proposal-v1', 'adaptation-selection-v1',
            'set-authoring-v1', 'set-validation-request-v1', 'adaptive-skill-v1',
            'project-binding-v1', 'adaptive-observation-v1', 'binding-observation-v1'}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate_shape(value, schema, document, location='$'):
    """Evaluate only the Draft 2020-12 vocabulary used by shipped closed schemas.

    This is not an arbitrary external JSON Schema engine; remote refs never load.
    """
    def resolve(reference):
        need(reference.startswith('adaptive-common.schema.json#/$defs/'), 'unsupported schema reference')
        common = runtime.strict_json((PACKAGE / 'schemas/adaptive-common.schema.json').read_bytes())
        return common, reference[len('adaptive-common.schema.json'):]
    record_schema.validate(value, schema, document, location, resolve)


def shape(value, version=None):
    need(isinstance(value, dict), 'record must be an object')
    version = version or value.get('schema_version')
    need(version in VERSIONS, 'unknown adaptive schema version')
    schema = runtime.strict_json((PACKAGE / 'schemas' / (version + '.schema.json')).read_bytes())
    validate_shape(value, schema, schema)
    return value


def indexed(rows, key='id'):
    result = {row[key]: row for row in rows}
    need(len(result) == len(rows), 'duplicate ' + key)
    return result


def topology(members):
    pending = {key: set(row['depends_on']) for key, row in members.items()}
    need(all(deps <= set(members) for deps in pending.values()), 'missing dependency/selection closure')
    result = []
    while pending:
        ready = sorted(key for key, deps in pending.items() if not deps)
        need(bool(ready), 'dependency cycle')
        key = ready[0]
        result.append(key)
        pending.pop(key)
        for deps in pending.values():
            deps.discard(key)
    return result


def aggregate(members):
    statuses = [row['status'] for row in members]
    if statuses and all(s == 'RETAINED' for s in statuses):
        return 'NO_CHANGE'
    if 'AUTHORED' in statuses and all(s in ('AUTHORED', 'RETAINED') for s in statuses):
        return 'AUTHORED'
    return 'PARTIAL' if any(row['applied_paths'] or row['status'] == 'AUTHORED' for row in members) else 'BLOCKED'


class Reader:
    def __init__(self):
        self.capture = runtime.Capture()
        self.active = set()
        self.records = {}
        self.references = {}
        self.packages = {}

    def absolute(self, value, write=False):
        need(isinstance(value, str) and Path(value).is_absolute(), 'resolved absolute path required')
        path = runtime.safe_path(value)
        need(str(path) == value, 'noncanonical absolute path')
        if write:
            authoring.safe(path, write=True)
        return path

    def ref(self, value):
        need(isinstance(value, dict) and set(value) == {'path', 'sha256'}, 'invalid Ref')
        runtime.string(value['sha256'], runtime.DIGEST)
        path = self.absolute(value['path'])
        need(not runtime.excluded(path) and not str(path).replace('\\', '/').endswith('/.agents/devforgeai/project-binding.json'), 'excluded reference; binding contents must remain operational')
        data = self.capture.read(path)
        need(runtime.digest(data) == value['sha256'], 'STALE_REFERENCE: ' + str(path))
        self.references[str(path)] = value['sha256']
        return data

    def locators(self, rows):
        for row in rows:
            text = self.ref(row['ref']).decode('utf-8')
            lines = text.splitlines()
            need(1 <= row['start_line'] <= row['end_line'] <= len(lines), 'locator outside retained text')
            need(any(x.strip() for x in lines[row['start_line'] - 1:row['end_line']]), 'empty supporting passage')

    def references_in(self, value):
        if isinstance(value, dict):
            if set(value) == {'path', 'sha256'}:
                self.ref(value)
            elif set(value) == {'ref', 'start_line', 'end_line'}:
                self.locators([value])
            else:
                for child in value.values():
                    self.references_in(child)
        elif isinstance(value, list):
            for child in value:
                self.references_in(child)

    def package(self, value):
        root = self.absolute(value['root'])
        need(root.name == value['name'], 'package directory/name mismatch')
        raw_manifest = runtime.strict_json(self.ref(value['manifest']))
        # New PackageRef manifests are arrays. Existing authoring manifests are
        # deliberately wrapped outside legacy records, never reinterpreted here.
        need(isinstance(raw_manifest, list), 'new package manifest must be row array')
        paths = []
        for row in raw_manifest:
            need(isinstance(row, dict) and set(row) == {'path', 'bytes', 'sha256'}, 'manifest row fields')
            runtime.relpath(row['path'])
            need(type(row['bytes']) is int and row['bytes'] >= 0, 'manifest bytes')
            runtime.string(row['sha256'], runtime.DIGEST)
            paths.append(row['path'])
        need(paths == sorted(set(paths)), 'manifest paths must be unique/sorted')
        rows = self.capture.inventory(root)
        need(raw_manifest == rows and runtime.digest(runtime.compact(rows)) == value['package_digest'], 'STALE_PACKAGE: incomplete or changed package')
        self.packages[str(root)] = rows
        return root

    def requirement_index(self, root):
        """Read an explicit parent index, not guessed IDs from arbitrary prose.

        Accept a fenced devforgeai-requirements JSON array or an explicit
        requirement table anywhere in the captured parent's Markdown. An absent
        or ambiguous index is a concrete gap, never reconstructed history.
        """
        # An older selected core need not have adaptive metadata or a convenient
        # contract filename. Inspect explicit inventories in its captured text.
        paths = [r['path'] for r in self.capture.inventory(root) if r['path'].lower().endswith('.md')]
        text = '\n'.join(self.capture.read(runtime.under(root, p)).decode('utf-8').replace('\r\n', '\n') for p in paths)
        blocks = re.findall(r'^```devforgeai-requirements[ \t]*\r?\n(.*?)^```[ \t]*\r?$', text, re.M | re.S)
        need(len(blocks) <= 1, 'ambiguous parent requirement indexes')
        rows = runtime.strict_json(blocks[0]) if blocks else []
        if not blocks:
            table = False
            for line in text.splitlines():
                cells = [x.strip().strip('`') for x in line.strip().strip('|').split('|')]
                if len(cells) >= 2 and cells[0].lower() in ('id', 'requirement id', 'requirement') and cells[1].lower() in ('requirement', 'statement', 'required behavior', 'behavior'):
                    table = True
                    continue
                if table and not line.strip().startswith('|'):
                    table = False
                if table and len(cells) >= 2 and re.fullmatch(runtime.IDENT, cells[0]):
                    rows.append({'id': cells[0], 'statement': cells[1]})
        need(isinstance(rows, list) and len(rows) > 0, 'empty parent requirements')
        for row in rows:
            need(isinstance(row, dict) and set(row) == {'id', 'statement'}, 'requirement index fields')
            runtime.string(row['id'], runtime.IDENT)
            runtime.string(row['statement'])
        return indexed(rows)

    def record_ref(self, ref, version):
        value = runtime.strict_json(self.ref(ref))
        need(value.get('schema_version') == version, 'referenced record family mismatch')
        return self.record(value, ref['path'])

    def record(self, value, path=None):
        shape(value)
        key = runtime.digest(runtime.compact(value))
        need(key not in self.active, 'record reference cycle')
        if key in self.records:
            return value
        need(len(self.active) < 64, 'record depth exceeds bounded reader')
        self.active.add(key)
        try:
            version = value['schema_version']
            if version != 'project-binding-v1':
                self.references_in(value)
            if version == 'project-evidence-v1':
                self.evidence(value)
            elif version == 'adaptation-proposal-v1':
                self.proposal(value)
            elif version == 'adaptation-selection-v1':
                self.selection(value)
            elif version == 'set-authoring-v1':
                self.set_authoring(value)
            elif version == 'set-validation-request-v1':
                self.set_request(value)
            elif version == 'adaptive-skill-v1':
                runtime.descriptor(value)
                if path:
                    descriptor_path = self.absolute(path)
                    need(descriptor_path.name == 'devforgeai-skill.json' and descriptor_path.parent.name == 'assets', 'descriptor package locator required')
                    root = descriptor_path.parent.parent
                    runtime.descriptor(value, root, self.capture)
                    if value['parent_core']:
                        text = self.capture.read(runtime.under(root, value['contract_path'])).decode('utf-8')
                        for ident in value['parent_core']['requirement_ids']:
                            need(re.search(r'(?<![A-Za-z0-9._-])' + re.escape(ident) + r'(?![A-Za-z0-9._-])', text), 'missing parent disposition locator')
            elif version == 'project-binding-v1':
                runtime.binding(value)
            self.records[key] = value
            return value
        finally:
            self.active.remove(key)

    def evidence(self, value):
        self.absolute(value['project_root'])
        for root in value['scope_roots']:
            self.absolute(root)
        facts = indexed(value['facts'])
        indexed(value['capabilities'])
        input_paths = {x['path'] for x in value['inputs']}
        for fact in facts.values():
            need((fact['basis'] == 'unknown') == (not fact['sources']), 'observed/user facts need evidence; unknown facts assert no evidence')
            need(all(x['ref']['path'] in input_paths for x in fact['sources']), 'fact source outside retained inputs')
        need(not value['complete'] or not any(x['material'] for x in value['exclusions']), 'material omission cannot be complete')

    def proposal(self, value):
        evidence = self.record_ref(value['project_evidence'], 'project-evidence-v1')
        if value['prior_proposal']:
            self.record_ref(value['prior_proposal'], 'adaptation-proposal-v1')
        facts = indexed(evidence['facts'])
        reqs, members = indexed(value['requirements']), indexed(value['members'])
        if value['mode'] == 'review_updates':
            need(all(m['role'] == 'project_variant' and m['existing_package'] is not None for m in members.values()), 'update review requires selected existing variants')
        need(len({m['name'] for m in members.values()}) == len(members), 'duplicate member name')
        for req in reqs.values():
            need(bool(req['rationale']) if req['origin'] == 'derived' else bool(req['source_refs']), 'requirement needs source or derived rationale')
        for member in members.values():
            need(set(member['requirement_ids']) <= set(reqs) and set(member['fact_ids']) <= set(facts), 'unresolved requirement/fact ID')
            indexed(member['capabilities'])
            if member['target_root']:
                target = self.absolute(member['target_root'], write=True)
                need(target.name == member['name'], 'member destination/name mismatch')
            if member['action'] == 'create':
                need(member['existing_package'] is None, 'create cannot claim existing package')
            else:
                need(member['existing_package'] is not None, 'retain/revise requires existing package')
                self.package(member['existing_package'])
                need(member['existing_package']['name'] == member['name'], 'existing member identity mismatch')
                if member['action'] == 'retain':
                    need(member['target_root'] is not None, 'retained destination missing')
            if member['role'] == 'project_variant':
                need(member['parent_core'] is not None and member['name'] != member['parent_core']['name'], 'distinct variant/parent required')
                parent = self.package(member['parent_core'])
                parent_requirements = self.requirement_index(parent)
                delta = indexed(member['lineage_delta'], 'requirement_id')
                need(set(delta) == set(parent_requirements), 'incomplete parent requirement dispositions')
                for ident, row in delta.items():
                    replacements = row['replacement_requirement_ids']
                    need(set(replacements) <= set(member['requirement_ids']), 'unresolved lineage replacement')
                    if row['disposition'] == 'modified':
                        need(bool(replacements), 'modified requirement needs replacement')
                    if row['disposition'] == 'retained':
                        choices = replacements or [ident]
                        need(all(x in member['requirement_ids'] for x in choices), 'retained requirement missing child')
                        need(any(reqs[x]['statement'] == parent_requirements[ident]['statement'] for x in choices), 'retained statement differs; use modified disposition')
                    if row['disposition'] == 'removed':
                        need(not replacements, 'removed requirement has replacements')
                        # A cited user requirement must record the selected
                        # removal. A reader checks linkage, never grants consent.
                        need(any(reqs[x]['origin'] == 'user' and ident in reqs[x]['statement'] and reqs[x]['source_refs'] for x in member['requirement_ids']), 'removed parent lacks current user requirement linkage')
                need(not member['target_root'] or self.absolute(member['target_root']) != parent, 'core destination cannot be variant')
            else:
                need(member['parent_core'] is None and not member['lineage_delta'], 'nonvariant lineage not permitted')
            if member['role'] == 'expertise':
                need(any(facts[x]['category'] in ('domain', 'architecture') and facts[x]['basis'] != 'unknown' for x in member['fact_ids']) or any(reqs[x]['origin'] == 'user' and reqs[x]['source_refs'] for x in member['requirement_ids']), 'expertise requires domain evidence or explicit user domain requirement')
        topology(members)
        handoffs = indexed(value['handoffs'])
        edges = {key: {'depends_on': []} for key in members}
        for row in handoffs.values():
            need(row['producer'] in members and row['consumer'] in members, 'unknown handoff endpoint')
            need(row['schema_ref'] is not None if row['format'] == 'json' else True, 'JSON handoff needs schema')
            if row['schema_ref']:
                schema = runtime.strict_json(self.ref(row['schema_ref']))
                need(isinstance(schema, (dict, bool)), 'handoff schema must be JSON Schema')
            need(row['failure_behavior'] == ('block_consumer' if row['required'] else 'report_optional_absence'), 'handoff failure branch mismatch')
            if row['required']:
                need(row['producer'] in members[row['consumer']]['depends_on'], 'required producer missing dependency')
            edges[row['consumer']]['depends_on'].append(row['producer'])
        topology(edges)
        for gap in value['gaps']:
            need(gap['member_id'] is None or gap['member_id'] in members, 'gap has unknown member')
            need(set(gap['requirement_ids']) <= set(reqs), 'gap has unknown requirement')
        unchanged = all(m['action'] == 'retain' for m in members.values())
        if value['mode'] == 'review_updates' and unchanged:
            # More specific update-review rule: equal semantics cannot hide a
            # changed input digest. No historical input means no no-change claim.
            unchanged = False
            if value['prior_proposal']:
                prior = self.record_ref(value['prior_proposal'], 'adaptation-proposal-v1')
                old_evidence = self.record_ref(prior['project_evidence'], 'project-evidence-v1')
                old_members = indexed(prior['members'])
                unchanged = ({x['sha256'] for x in evidence['inputs']} == {x['sha256'] for x in old_evidence['inputs']}
                             and value['requirements'] == prior['requirements']
                             and all(k in old_members and m['parent_core'] == old_members[k]['parent_core'] for k, m in members.items()))
        expected = 'BLOCKED' if value['gaps'] or not evidence['complete'] or evidence['gaps'] else ('NO_CHANGE' if unchanged else 'PROPOSED')
        need(value['state'] == expected, 'proposal state disagrees with gaps/actions')

    def selection(self, value, preflight=False):
        proposal = self.record_ref(value['proposal'], 'adaptation-proposal-v1')
        members = indexed(proposal['members'])
        need(set(value['member_ids']) <= set(members), 'unselected/unknown member')
        selected = {key: members[key] for key in value['member_ids']}
        order = topology(selected)
        destinations = indexed(value['destinations'], 'member_id')
        need(set(destinations) == set(selected), 'exact destination membership required')
        paths = []
        authorization = self.ref(value['authorization']).decode('utf-8')
        for key in order:
            member = selected[key]
            dest = self.absolute(destinations[key]['target_root'], write=True)
            need(dest.name == member['name'], 'destination identity mismatch')
            need(not any(dest == old or dest.is_relative_to(old) or old.is_relative_to(dest) for old in paths), 'colliding destination roots')
            paths.append(dest)
            if member['target_root'] != str(dest):
                need(str(dest) in authorization, 'changed destination needs captured explicit selection')
            if member['parent_core']:
                parent = self.absolute(member['parent_core']['root'])
                need(dest != parent and not dest.is_relative_to(parent) and not parent.is_relative_to(dest), 'parent core overlap')
            if preflight:
                need(not any(g['member_id'] in (None, key) for g in proposal['gaps']), 'selected member has unresolved gap')
                need(all(not c['required'] or c['observed'] == 'available' for c in member['capabilities']), 'essential member capability unavailable')
                if member['action'] == 'create':
                    need(not os.path.lexists(dest), 'occupied destination')
                else:
                    live = self.capture.inventory(dest)
                    need(runtime.digest(runtime.compact(live)) == member['existing_package']['package_digest'], 'existing destination drift')
        if preflight:
            evidence = self.record_ref(proposal['project_evidence'], 'project-evidence-v1')
            need(evidence['complete'], 'DISCOVERY_LIMIT or incomplete selected evidence')
            need(not any(g['member_id'] is None or g['member_id'] in selected for g in evidence['gaps']), 'selected project evidence has unresolved gap')
            need(all(not c['required'] or c['observed'] == 'available' for c in evidence['capabilities']), 'essential custody capability unavailable')
        return proposal, selected, order

    def legacy_ref(self, ref, version):
        value = runtime.strict_json(self.ref(ref))
        filename = {'authoring-v1': 'authoring-record', 'validation-request-v1': 'validation-request', 'authoring-contract-v1': 'authoring-contract'}[version]
        schema = runtime.strict_json((PACKAGE / 'schemas' / (filename + '.schema.json')).read_bytes())
        validate_shape(value, schema, schema)
        self.references_in(value)
        return value

    def legacy_manifest(self, ref, package):
        value = runtime.strict_json(self.ref(ref))
        runtime.fields(value, 'schema_version files package_digest')
        need(value['schema_version'] == '1' and isinstance(value['files'], list), 'legacy manifest shape')
        rows = []
        for row in value['files']:
            runtime.fields(row, 'path bytes sha256')
            runtime.relpath(row['path'])
            need(type(row['bytes']) is int and row['bytes'] >= 0, 'legacy manifest bytes')
            runtime.string(row['sha256'], runtime.DIGEST)
            rows.append({key: row[key] for key in ('path', 'bytes', 'sha256')})
        need(rows == self.packages[package['root']], 'legacy manifest differs from delivered rows')
        need(runtime.digest(runtime.compact(rows)) == value['package_digest'] == package['package_digest'], 'legacy manifest digest mismatch')

    def set_authoring(self, value):
        selection = self.record_ref(value['selection'], 'adaptation-selection-v1')
        proposal, selected, order = self.selection(selection)
        results = indexed(value['members'], 'member_id')
        need(value['ordered_member_ids'] == order and set(results) == set(selected), 'set membership/order mismatch')
        for key in order:
            row, member = results[key], selected[key]
            record = None
            failed_deps = [x for x in member['depends_on'] if results[x]['status'] not in ('AUTHORED', 'RETAINED')]
            need((row['status'] == 'DEPENDENCY_BLOCKED') == bool(failed_deps), 'transitive dependency failure mislabeled')
            if row['status'] in ('AUTHORED', 'RETAINED'):
                need(row['package'] is not None, 'eligible result needs complete package')
            if row['package']:
                package_root = self.package(row['package'])
                dest = next(d['target_root'] for d in selection['destinations'] if d['member_id'] == key)
                need(row['package']['root'] == dest and row['package']['name'] == member['name'], 'result package differs from selected identity')
                desc_path = runtime.under(package_root, 'assets/devforgeai-skill.json')
                if row['status'] == 'AUTHORED' or desc_path.exists():
                    need(desc_path.is_file(), 'delivered adaptive descriptor missing')
                    desc = runtime.strict_json(self.capture.read(desc_path))
                    self.record(desc, str(desc_path))
                    need(desc['role'] == member['role'], 'delivered role differs from selection')
                    if member['role'] == 'project_variant':
                        parent = member['parent_core']
                        need(desc['parent_core']['name'] == parent['name'] and desc['parent_core']['package_digest'] == parent['package_digest']
                             and set(desc['parent_core']['requirement_ids']) == {r['requirement_id'] for r in member['lineage_delta']}, 'delivered parent lineage differs from selection')
            if row['status'] == 'RETAINED':
                need(member['action'] == 'retain' and row['package']['package_digest'] == member['existing_package']['package_digest'] and not row['applied_paths'], 'retention cannot invent authoring')
            if row['status'] == 'DEPENDENCY_BLOCKED':
                need(not row['applied_paths'] and row['authoring_record'] is None and row['validation_request'] is None, 'blocked dependency performed authoring')
            if row['status'] == 'BLOCKED':
                need(not row['applied_paths'], 'applied bytes require PARTIAL')
            if row['status'] == 'AUTHORED':
                need(member['action'] != 'retain' and row['authoring_record'] is not None and row['validation_request'] is not None, 'authored result requires per-member records')
            if row['authoring_record']:
                record = self.legacy_ref(row['authoring_record'], 'authoring-v1')
                contract = self.legacy_ref(record['contract'], 'authoring-contract-v1')
                need(all(record[k] == contract[k] for k in ('run_id', 'project_root', 'target_root', 'target_name', 'operation', 'authorization')), 'per-member contract identity mismatch')
                need(record['authoring_state'] == row['status'] and record['applied_paths'] == row['applied_paths'], 'member state/applied paths disagree with custody')
                need(record['target_name'] == member['name'], 'per-member authoring identity mismatch')
                if row['package']:
                    need(record['target_root'] == row['package']['root'], 'per-member delivered target mismatch')
                    self.legacy_manifest(record['delivered_manifest'], row['package'])
                if row['status'] == 'AUTHORED':
                    run = self.absolute(row['authoring_record']['path']).parent
                    need(not (run / 'publication-failure.json').exists(), 'member publication failed')
                    receipt = runtime.strict_json(self.capture.read(run / 'publication-readback.json'))
                    need(receipt.get('state') == 'PUBLISHED' and receipt.get('authoring_record') == row['authoring_record'] and receipt.get('request') == row['validation_request'], 'member publication readback missing/mismatch')
            if row['validation_request']:
                request = self.legacy_ref(row['validation_request'], 'validation-request-v1')
                need(record is not None and row['package'] is not None and request['package_digest'] == row['package']['package_digest'] and request['authoring_record'] == row['authoring_record'], 'per-member validation request mismatch')
                need(request['authoring_run_id'] == record['run_id'] and all(request[k] == record[k] for k in ('project_root', 'target_root', 'target_name')), 'per-member request identity mismatch')
                need(request['changed_paths'] == record['applied_paths'], 'per-member request changed paths mismatch')
                self.legacy_manifest(request['target_manifest'], row['package'])
        need(value['state'] == aggregate(value['members']), 'aggregate state mismatch')
        return selected, results

    def set_request(self, value):
        selection = self.record_ref(value['selection'], 'adaptation-selection-v1')
        result = self.record_ref(value['set_authoring'], 'set-authoring-v1')
        need(result['selection'] == value['selection'], 'set selection reference mismatch')
        proposal, selected, order = self.selection(selection)
        results = indexed(result['members'], 'member_id')
        requested = indexed(value['members'], 'member_id')
        omitted = set(value['omitted_member_ids'])
        need(not set(requested) & omitted and set(requested) | omitted == set(selected), 'request and omissions must partition selection')
        need((value['scope'] == 'full_set') == (not omitted), 'full_set/subset scope mismatch')
        for key, row in requested.items():
            source = results[key]
            need(source['status'] in ('AUTHORED', 'RETAINED') and row['package'] == source['package'], 'ineligible package in request')
            need(set(selected[key]['depends_on']) <= set(requested), 'subset is not dependency closed')
            need(row['request'] == source['validation_request'], 'request member handoff mismatch')
            root = self.package(row['package'])
            descriptor = runtime.under(root, 'assets/devforgeai-skill.json')
            if source['status'] == 'AUTHORED' or descriptor.exists():
                need(row['adaptive_descriptor'] is not None and row['adaptive_descriptor']['path'] == str(descriptor), 'adaptive descriptor required')
                self.record_ref(row['adaptive_descriptor'], 'adaptive-skill-v1')
        handoffs = [h for h in proposal['handoffs'] if h['producer'] in selected and h['consumer'] in selected]
        expected = [h for h in handoffs if h['producer'] in requested and h['consumer'] in requested]
        need(indexed(value['handoffs']) == indexed(expected), 'requested handoffs differ from proposal')
        need(set(value['omitted_handoff_ids']) == {h['id'] for h in handoffs if h not in expected}, 'handoff omissions incomplete')

    def readback(self):
        for path, expected in list(self.references.items()):
            need(runtime.digest(self.capture.read(path)) == expected, 'STALE_REFERENCE at readback')
        for root, expected in self.packages.items():
            need(self.capture.inventory(root) == expected, 'STALE_PACKAGE at readback')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('inspect').add_argument('--record', required=True)
    commands.add_parser('plan-set').add_argument('--selection', required=True)
    args = parser.parse_args()
    output = {'schema_version': 'adaptive-observation-v1', 'status': 'VALID', 'errors': [], 'ordered_member_ids': []}
    code = 0
    try:
        reader = Reader()
        path = runtime.safe_path(args.record if args.command == 'inspect' else args.selection)
        raw = reader.capture.read(path)
        value = runtime.strict_json(raw)
        reader.record(value, str(path))
        if args.command == 'plan-set':
            need(value['schema_version'] == 'adaptation-selection-v1', 'plan-set requires selection')
            output['ordered_member_ids'] = reader.selection(value, preflight=True)[2]
        reader.readback()
        need(reader.capture.read(path) == raw, 'STALE_REFERENCE: selected record changed')
    except runtime.BindingError as exc:
        code = 2 if exc.code in ('CAPTURE_LIMIT', 'IO_ERROR') else 1
        output['errors'] = [exc.code]
    except OSError:
        code, output['errors'] = 2, ['IO_ERROR: selected local input unavailable']
    except (ValueError, KeyError, TypeError, UnicodeError, RecursionError) as exc:
        code, output['errors'] = 1, [str(exc)]
    if code:
        output.update(status='UNAVAILABLE' if code == 2 else 'INVALID', ordered_member_ids=[])
    print(json.dumps(output, ensure_ascii=False, allow_nan=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
