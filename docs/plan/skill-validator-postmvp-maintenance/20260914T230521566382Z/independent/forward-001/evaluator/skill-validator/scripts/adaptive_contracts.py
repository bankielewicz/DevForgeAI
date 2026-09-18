"""Independent read-only readers for frozen adaptive v1 contracts.

Only validator-local modules are used. Schema documents are shared data, never
builder executable logic. Semantic support and authorization remain review work.
"""
import datetime
import json
import os
from pathlib import Path
import re
import stat
import uuid

import observe
import authoring_intake

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'
SHARED = {'project-evidence-v1', 'adaptation-proposal-v1', 'adaptation-selection-v1',
          'adaptive-skill-v1', 'set-authoring-v1', 'set-validation-request-v1',
          'project-binding-v1', 'binding-observation-v1', 'adaptive-observation-v1'}
VERSIONS = SHARED | {'standalone-set-input-v1', 'set-assessment-v1',
                     'adaptive-observations-v1', 'adaptive-check-observation-v1'}
EXCLUDED = {'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '.agents', '.claude', '.codex'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(value, schema, document=None):
    """The closed local Draft 2020-12 vocabulary; no remote schema loading."""
    document = document or schema
    if '$ref' in schema:
        name, _, fragment = schema['$ref'].partition('#')
        if name:
            require(name == 'adaptive-common.schema.json', 'unsupported schema resource')
            document = observe.strict_json((SCHEMAS / name).read_bytes())
        require(fragment.startswith('/$defs/'), 'unsupported schema fragment')
        return validate(value, document['$defs'][fragment[7:]], document)
    if 'anyOf' in schema:
        for alternative in schema['anyOf']:
            try:
                validate(value, alternative, document)
                return
            except ValueError:
                continue
        raise ValueError('no allowed schema alternative')
    if 'const' in schema:
        require(type(value) is type(schema['const']) and value == schema['const'], 'wrong constant/version')
    if 'enum' in schema:
        require(any(type(value) is type(item) and value == item for item in schema['enum']), 'unknown enum')
    kind = schema.get('type')
    expected = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool, 'null': type(None)}
    if kind:
        require(type(value) is expected[kind], 'wrong schema type: ' + kind)
    if kind == 'object':
        require(set(schema.get('required', [])) <= value.keys(), 'missing required fields')
        if schema.get('additionalProperties') is False:
            require(value.keys() <= schema.get('properties', {}).keys(), 'extra fields')
        for key in value.keys() & schema.get('properties', {}).keys():
            validate(value[key], schema['properties'][key], document)
    elif kind == 'array':
        require(len(value) >= schema.get('minItems', 0), 'too few array items')
        if schema.get('uniqueItems'):
            require(len({observe.compact(item) for item in value}) == len(value), 'duplicate array items')
        for item in value:
            if 'items' in schema:
                validate(item, schema['items'], document)
    elif kind == 'string':
        require(schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value)), 'string length')
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None and not value.endswith('\n'), 'invalid string pattern')
    elif kind == 'integer':
        require(value >= schema.get('minimum', value), 'integer minimum')


def shape(value):
    require(type(value) is dict and value.get('schema_version') in VERSIONS, 'unknown adaptive schema version')
    schema = observe.strict_json((SCHEMAS / (value['schema_version'] + '.schema.json')).read_bytes())
    validate(value, schema)
    return value


def index(rows, key='id'):
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows), 'duplicate ' + key)
    return result


def order(members):
    edges = {key: set(row['depends_on']) for key, row in members.items()}
    require(all(deps <= edges.keys() for deps in edges.values()), 'unknown dependency / incomplete selection')
    answer = []
    while edges:
        ready = sorted(key for key in edges if not edges[key])
        require(bool(ready), 'dependency or handoff cycle')
        key = ready[0]
        answer.append(key)
        del edges[key]
        for deps in edges.values():
            deps.discard(key)
    return answer


def excluded(path):
    return any(part in EXCLUDED or observe.exclusion(part) or part.startswith('.env') or part.lower().endswith(('.pem', '.key')) for part in path.parts)


def inventory(root, allow_exclusions=False):
    """Enumerate before descent; excluded trees are never traversed."""
    require(root.is_dir(), 'package root must be directory')
    files, omissions, pending, total = [], [], [root], 0
    while pending:
        for path in sorted(pending.pop().iterdir()):
            relative = path.relative_to(root)
            if excluded(relative):
                require(allow_exclusions, 'unexpected excluded/generated package entry')
                omissions.append({'path':relative.as_posix(),'reason':'excluded before recursion'})
                continue
            info = path.lstat()
            if observe.is_link(path):
                require(allow_exclusions, 'link/junction package entry')
                omissions.append({'path':relative.as_posix(),'reason':'link/junction not followed'})
            elif stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                require(observe.normalized_relative(relative.as_posix()) and '\0' not in relative.as_posix(), 'unsafe relative path')
                total += info.st_size
                if len(files) >= 2000 or total > 32 * 1024 * 1024:
                    raise observe.ObservationError('capture ceiling exceeded')
                files.append((relative.as_posix(),path,info))
            else:
                raise ValueError('special file rejected')
    return sorted(files), omissions


class Reader:
    def __init__(self):
        self.seen = {}
        self.packages = {}
        self.active = set()
        self.done = set()
        self.total = 0

    def absolute(self, name, exists=True):
        require(type(name) is str and Path(name).is_absolute(), 'absolute external reference required')
        path = observe.safe_path(name, must_exist=exists)
        require(str(path) == name, 'canonical resolved absolute path required')
        return path

    def read(self, path):
        path = observe.safe_path(path)
        data = observe.read_stable(path)
        if str(path) not in self.seen:
            self.total += len(data)
            if len(self.seen) >= 2000 or self.total > 32 * 1024 * 1024:
                raise observe.ObservationError('aggregate capture ceiling exceeded')
        current = observe.sha256(data)
        require(str(path) not in self.seen or self.seen[str(path)] == current, 'SOURCE_CHANGED during read')
        self.seen[str(path)] = current
        return data

    def ref(self, reference):
        validate(reference, {'$ref':'adaptive-common.schema.json#/$defs/Ref'})
        path = self.absolute(reference['path'])
        # Operational identities are never accepted as general external inputs.
        require(not any(part in ('node_modules','.venv','venv','target','dist','build') or observe.exclusion(part) or part.startswith('.env') for part in path.parts) and not path.suffix.lower() in ('.pem','.key') and '/.agents/devforgeai/' not in path.as_posix(), 'excluded external reference')
        data = self.read(path)
        require(observe.sha256(data) == reference['sha256'], 'STALE_REFERENCE')
        return data

    def refs(self, value):
        if type(value) is dict:
            if set(value) == {'path', 'sha256'}:
                self.ref(value)
            elif set(value) == {'ref', 'start_line', 'end_line'}:
                lines = self.ref(value['ref']).decode('utf-8').splitlines()
                require(1 <= value['start_line'] <= value['end_line'] <= len(lines), 'locator outside retained text')
                require(any(line.strip() for line in lines[value['start_line']-1:value['end_line']]), 'empty supporting passage')
            else:
                for item in value.values():
                    self.refs(item)
        elif type(value) is list:
            for item in value:
                self.refs(item)

    def manifest(self, root):
        files, omissions = inventory(root)
        require(not omissions, 'incomplete package inventory')
        rows = []
        for relative, path, info in files:
            require(not excluded(Path(relative)), 'unexpected excluded/generated package file')
            data = self.read(path)
            rows.append({'path':relative, 'bytes':len(data), 'sha256':observe.sha256(data)})
        return rows

    def package(self, package):
        validate(package, {'$ref':'adaptive-common.schema.json#/$defs/PackageRef'})
        root = self.absolute(package['root'])
        require(root.name == package['name'], 'package directory identity mismatch')
        expected = observe.strict_json(self.ref(package['manifest']))
        actual = self.manifest(root)
        require(expected == actual and observe.sha256(observe.compact(actual)) == package['package_digest'], 'STALE_PACKAGE / incomplete manifest')
        self.packages[str(root)] = actual
        return root

    def record_ref(self, reference, version):
        value = observe.strict_json(self.ref(reference))
        require(type(value) is dict and value.get('schema_version') == version, 'referenced record version mismatch')
        return self.record(value, reference['path'])

    def requirements(self, rows):
        result = index(rows)
        for row in rows:
            require(bool(row['rationale']) if row['origin'] == 'derived' else bool(row['source_refs']), 'requirement lacks supporting origin')
        return result

    def handoffs(self, rows, members):
        index(rows)
        graph = {key: {'depends_on': []} for key in members}
        for row in rows:
            require(row['producer'] in members and row['consumer'] in members, 'unknown handoff endpoint')
            require(row['failure_behavior'] == ('block_consumer' if row['required'] else 'report_optional_absence'), 'handoff failure contract')
            require(row['format'] != 'json' or row['schema_ref'] is not None, 'JSON handoff lacks schema')
            if row['schema_ref']:
                require(type(observe.strict_json(self.ref(row['schema_ref']))) in (dict, bool), 'invalid handoff schema')
            if row['required']:
                require(row['producer'] in members[row['consumer']]['depends_on'], 'required producer missing dependency')
            graph[row['consumer']]['depends_on'].append(row['producer'])
        order(graph)

    def descriptor(self, value, path=None):
        variant = value['role'] == 'project_variant'
        require(variant == (value['parent_core'] is not None), 'descriptor lineage role mismatch')
        require(value['contract_path'] == 'references/adaptive-contract.md', 'descriptor contract path')
        require(any(re.search(r'Python\s*3\.10\+', item, re.I) for item in value['required_capabilities']), 'descriptor requires Python 3.10+ capability')
        if value['parent_core']:
            require(value['parent_core']['name'] != value['name'], 'variant must differ from parent')
            require(len(set(value['parent_core']['requirement_ids'])) == len(value['parent_core']['requirement_ids']), 'duplicate parent requirements')
        index(value['resource_roles'], 'path')
        if path:
            file = self.absolute(path)
            require(file.name == 'devforgeai-skill.json' and file.parent.name == 'assets', 'descriptor locator')
            root = file.parent.parent
            require(root.name == value['name'], 'descriptor package identity')
            import text_resources
            metadata = text_resources.frontmatter(self.read(root / 'SKILL.md').decode('utf-8'))
            require(metadata['name'] == value['name'], 'descriptor frontmatter identity')
            self.read(observe.safe_path(root / value['contract_path']))
            for row in value['resource_roles']:
                require(observe.normalized_relative(row['path']), 'invalid resource role path')
                self.read(observe.safe_path(root / row['path']))

    def binding(self, value):
        require(str(uuid.UUID(value['project_id'])) == value['project_id'], 'invalid canonical project identity')
        self.absolute(value['project_root'])
        require(value['updated_at_utc'].endswith('Z'), 'binding requires UTC timestamp')
        datetime.datetime.fromisoformat(value['updated_at_utc'][:-1] + '+00:00')
        index(value['bindings'], 'name')
        index(value['bindings'], 'package_path')
        for row in value['bindings']:
            require(row['package_path'] == '.agents/skills/' + row['name'], 'invalid installed path')

    def proposal(self, value):
        evidence = self.record_ref(value['project_evidence'], 'project-evidence-v1')
        if value['prior_proposal']:
            self.record_ref(value['prior_proposal'], 'adaptation-proposal-v1')
        facts, requirements, members = index(evidence['facts']), self.requirements(value['requirements']), index(value['members'])
        index(value['members'], 'name')
        for member in members.values():
            require(set(member['requirement_ids']) <= requirements.keys() and set(member['fact_ids']) <= facts.keys(), 'unknown fact or requirement')
            index(member['capabilities'])
            if member['target_root']:
                require(self.absolute(member['target_root'], False).name == member['name'], 'destination/name mismatch')
            require((member['action'] == 'create') == (member['existing_package'] is None), 'action/existing package mismatch')
            if member['existing_package']:
                self.package(member['existing_package'])
                require(member['existing_package']['name'] == member['name'], 'existing identity mismatch')
            require(member['action'] != 'retain' or member['target_root'] is not None, 'retained destination missing')
            if member['role'] == 'project_variant':
                require(member['parent_core'] is not None and member['parent_core']['name'] != member['name'], 'distinct parent required')
                root = self.package(member['parent_core'])
                text = self.read(root / 'references/adaptive-contract.md').decode('utf-8')
                parent = parent_requirements(text)
                delta = index(member['lineage_delta'], 'requirement_id')
                require(delta.keys() == parent.keys(), 'incomplete parent requirement dispositions')
                for ident, row in delta.items():
                    replacements = row['replacement_requirement_ids']
                    require(set(replacements) <= set(member['requirement_ids']), 'unresolved lineage replacement')
                    if row['disposition'] == 'modified':
                        require(bool(replacements), 'modified requirement needs replacement')
                    elif row['disposition'] == 'retained':
                        choices = replacements or [ident]
                        require(set(choices) <= set(member['requirement_ids']), 'retained child missing')
                        require(any(requirements[x]['statement'] == parent[ident]['statement'] for x in choices), 'retained statement changed')
                    else:
                        require(not replacements and any(requirements[x]['origin'] == 'user' and ident in requirements[x]['statement'] and requirements[x]['source_refs'] for x in member['requirement_ids']), 'removal lacks current user linkage; semantic authorization review required')
            else:
                require(member['parent_core'] is None and not member['lineage_delta'], 'nonvariant has lineage')
            if member['role'] == 'expertise':
                require(any(facts[x]['category'] in ('domain','architecture') and facts[x]['basis'] != 'unknown' for x in member['fact_ids']) or any(requirements[x]['origin'] == 'user' for x in member['requirement_ids']), 'expertise lacks domain evidence')
        order(members)
        self.handoffs(value['handoffs'], members)
        for gap in value['gaps']:
            require(gap['member_id'] is None or gap['member_id'] in members, 'unknown gap member')
            require(set(gap['requirement_ids']) <= requirements.keys(), 'unknown gap requirement')
        state = 'BLOCKED' if value['gaps'] or not evidence['complete'] or evidence['gaps'] else ('NO_CHANGE' if all(m['action'] == 'retain' for m in members.values()) else 'PROPOSED')
        require(value['state'] == state, 'proposal state mismatch')

    def selection(self, value):
        proposal = self.record_ref(value['proposal'], 'adaptation-proposal-v1')
        all_members = index(proposal['members'])
        require(set(value['member_ids']) <= all_members.keys(), 'unknown selected member')
        members = {key: all_members[key] for key in value['member_ids']}
        sequence = order(members)
        destinations = index(value['destinations'], 'member_id')
        require(destinations.keys() == members.keys(), 'destination membership mismatch')
        paths = []
        authorization = self.ref(value['authorization']).decode('utf-8')
        for key, member in members.items():
            path = self.absolute(destinations[key]['target_root'], False)
            require(path.name == member['name'], 'destination name mismatch')
            require(not any(path == prior or observe.within(path, prior) or observe.within(prior, path) for prior in paths), 'overlapping destinations')
            paths.append(path)
            if member['parent_core']:
                parent = self.absolute(member['parent_core']['root'])
                require(not observe.within(path, parent) and not observe.within(parent, path), 'parent destination overlap')
            if str(path) != member['target_root']:
                require(str(path) in authorization, 'changed destination lacks selected input')
        return proposal, members, sequence

    def set_authoring(self, value):
        selection = self.record_ref(value['selection'], 'adaptation-selection-v1')
        proposal, members, sequence = self.selection(selection)
        results = index(value['members'], 'member_id')
        require(results.keys() == members.keys() and value['ordered_member_ids'] == sequence, 'set result membership/order')
        for key in sequence:
            row, member = results[key], members[key]
            failed = any(results[dep]['status'] not in ('AUTHORED','RETAINED') for dep in member['depends_on'])
            require((row['status'] == 'DEPENDENCY_BLOCKED') == failed, 'dependency result mismatch')
            if row['status'] in ('AUTHORED','RETAINED'):
                require(row['package'] is not None, 'eligible member missing package')
            if row['package']:
                self.package(row['package'])
                destination = next(x['target_root'] for x in selection['destinations'] if x['member_id'] == key)
                require(row['package']['root'] == destination and row['package']['name'] == member['name'], 'delivered identity mismatch')
            if row['status'] == 'RETAINED':
                require(member['action'] == 'retain' and row['package']['package_digest'] == member['existing_package']['package_digest'] and not row['applied_paths'], 'invalid retained result')
            if row['status'] in ('BLOCKED','DEPENDENCY_BLOCKED'):
                require(not row['applied_paths'], 'partial writes must be retained as PARTIAL')
            if row['status'] == 'DEPENDENCY_BLOCKED':
                require(row['authoring_record'] is None and row['validation_request'] is None, 'blocked dependency authored')
            if row['status'] == 'AUTHORED':
                require(member['action'] != 'retain' and row['authoring_record'] and row['validation_request'], 'authored member missing custody')
            if row['authoring_record']:
                authored = observe.strict_json(self.ref(row['authoring_record']))
                validate(authored, observe.strict_json((SCHEMAS / 'authoring-record.schema.json').read_bytes()))
                self.refs(authored)
                require(authored['authoring_state'] == row['status'] and authored['applied_paths'] == row['applied_paths'] and authored['target_name'] == member['name'], 'authoring member mismatch')
                if row['package']:
                    delivered = observe.strict_json(self.ref(authored['delivered_manifest']))
                    require(authored['target_root'] == row['package']['root'] and delivered['package_digest'] == row['package']['package_digest'], 'authoring delivered mismatch')
            if row['validation_request']:
                request = observe.strict_json(self.ref(row['validation_request']))
                validate(request, observe.strict_json((SCHEMAS / 'validation-request.schema.json').read_bytes()))
                require(row['package'] is not None and request['package_digest'] == row['package']['package_digest'] and request['authoring_record'] == row['authoring_record'], 'authoring request mismatch')
                authoring_intake.intake(row['validation_request']['path'], row['validation_request']['sha256'])
        statuses = [x['status'] for x in results.values()]
        state = ('NO_CHANGE' if statuses and all(x == 'RETAINED' for x in statuses) else
                 'AUTHORED' if 'AUTHORED' in statuses and all(x in ('AUTHORED','RETAINED') for x in statuses) else
                 'PARTIAL' if any(x['applied_paths'] or x['status'] == 'AUTHORED' for x in results.values()) else 'BLOCKED')
        require(value['state'] == state, 'set authoring reduction mismatch')

    def intake(self, value):
        if value['schema_version'] == 'standalone-set-input-v1':
            members = index(value['members'], 'member_id')
            self.requirements(value['requirements'])
            sequence = order(members)
            self.handoffs(value['handoffs'], members)
            for row in members.values():
                root = self.package(row['package'])
                self.member_descriptor(row, root)
            for gap in value['gaps']:
                require(gap['member_id'] is None or gap['member_id'] in members, 'unknown gap member')
                require(set(gap['requirement_ids']) <= {r['id'] for r in value['requirements']}, 'unknown gap requirement')
            return sequence
        require(value['schema_version'] == 'set-validation-request-v1', 'set input required')
        selection = self.record_ref(value['selection'], 'adaptation-selection-v1')
        authored = self.record_ref(value['set_authoring'], 'set-authoring-v1')
        require(authored['selection'] == value['selection'], 'selection reference mismatch')
        proposal, selected, _ = self.selection(selection)
        results, requested = index(authored['members'],'member_id'), index(value['members'],'member_id')
        omitted = set(value['omitted_member_ids'])
        require(not requested.keys() & omitted and requested.keys() | omitted == selected.keys(), 'selected membership/omission mismatch')
        require((value['scope'] == 'full_set') == (not omitted), 'scope/omission mismatch')
        subset = {key: selected[key] for key in requested}
        sequence = order(subset)
        for key, row in requested.items():
            result = results[key]
            require(result['status'] in ('AUTHORED','RETAINED') and row['package'] == result['package'] and row['request'] == result['validation_request'], 'ineligible or rebound member')
            root = self.package(row['package'])
            self.member_descriptor(row, root, result['status'] == 'AUTHORED')
        handoffs = [x for x in proposal['handoffs'] if x['producer'] in selected and x['consumer'] in selected]
        expected = [x for x in handoffs if x['producer'] in requested and x['consumer'] in requested]
        require(index(value['handoffs']) == index(expected), 'handoff membership/content mismatch')
        require(set(value['omitted_handoff_ids']) == {x['id'] for x in handoffs if x not in expected}, 'handoff omissions mismatch')
        self.handoffs(value['handoffs'], subset)
        return sequence

    def member_descriptor(self, row, root, adaptive=False):
        path = root / 'assets/devforgeai-skill.json'
        if path.exists() or adaptive:
            require(row['adaptive_descriptor'] is not None, 'missing adaptive descriptor')
        if row['adaptive_descriptor']:
            require(row['adaptive_descriptor']['path'] == str(path), 'descriptor outside selected package')
            self.record_ref(row['adaptive_descriptor'], 'adaptive-skill-v1')

    def record(self, value, path=None):
        shape(value)
        key = observe.sha256(observe.compact(value))
        require(key not in self.active and len(self.active) < 64, 'record reference cycle/depth')
        if key in self.done:
            return value
        self.active.add(key)
        try:
            version = value['schema_version']
            if version != 'project-binding-v1':
                self.refs(value)
            if version == 'project-evidence-v1':
                self.absolute(value['project_root'])
                for root in value['scope_roots']:
                    self.absolute(root)
                index(value['facts'])
                index(value['capabilities'])
                for fact in value['facts']:
                    require((fact['basis'] == 'unknown') == (not fact['sources']), 'fact basis/source mismatch')
                    require(all(x['ref'] in value['inputs'] for x in fact['sources']), 'fact outside inputs')
                require(not value['complete'] or not any(x['material'] for x in value['exclusions']), 'material exclusion cannot be complete')
            elif version == 'adaptation-proposal-v1':
                self.proposal(value)
            elif version == 'adaptation-selection-v1':
                self.selection(value)
            elif version == 'set-authoring-v1':
                self.set_authoring(value)
            elif version in ('set-validation-request-v1','standalone-set-input-v1'):
                self.intake(value)
            elif version == 'adaptive-skill-v1':
                self.descriptor(value, path)
            elif version == 'project-binding-v1':
                self.binding(value)
            self.done.add(key)
        finally:
            self.active.remove(key)
        return value

    def readback(self):
        for path, expected in list(self.seen.items()):
            require(observe.sha256(observe.read_stable(observe.safe_path(path))) == expected, 'SOURCE_CHANGED reference readback')
        for root, expected in list(self.packages.items()):
            require(self.manifest(Path(root)) == expected, 'SOURCE_CHANGED package membership')


def parent_requirements(text):
    blocks = re.findall(r'^```devforgeai-requirements[^\S\r\n]*\r?\n(.*?)^```[^\S\r\n]*$', text, re.M | re.S)
    require(len(blocks) <= 1, 'ambiguous parent index')
    rows = observe.strict_json(blocks[0]) if blocks else []
    if not blocks:
        in_table = False
        for line in text.splitlines():
            cells = [x.strip().strip('`') for x in line.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[0].lower() in ('id','requirement id') and cells[1].lower() in ('requirement','statement'):
                in_table = True
                continue
            if in_table and not line.strip().startswith('|'):
                in_table = False
            if in_table and len(cells) >= 2 and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', cells[0]):
                rows.append({'id':cells[0],'statement':cells[1]})
    require(type(rows) is list and bool(rows), 'unresolved parent requirement inventory; manual mapping required')
    for row in rows:
        require(type(row) is dict and set(row) == {'id','statement'} and type(row['statement']) is str and bool(row['statement']), 'invalid parent requirement row')
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', row['id']) is not None, 'invalid parent requirement ID')
    return index(rows)
