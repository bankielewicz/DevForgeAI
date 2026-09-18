"""Portable authoring custody. No quality checks, test execution or validator calls.

begin --contract FILE --run-root NEW_DIR [--design FILE]
publish --run-root DIR
read --record FILE
Records are ordinary development evidence, not enforcement or an atomic broker.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import record_schema

sys.dont_write_bytecode = True
MAX_FILES = 2000
MAX_BYTES = 32 * 1024 * 1024
EXCLUDED = {'.git', '__pycache__', 'backup', 'backups', 'devforgeai_cli'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')

def parse(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON number: ' + value)
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)
    # Reject overflow-to-infinity numbers as well as named nonfinite constants.
    compact(value)
    return value

def safe(value, write=False):
    # write marks caller intent only. Destination policy is the selected contract's
    # target_root, not a fixed directory-name denylist: a deployed skill authors into
    # whatever skills directory the host project uses, including .claude/skills.
    path = Path(value).expanduser()
    if '..' in path.parts:
        raise ValueError('traversal rejected')
    path = Path(os.path.abspath(path))
    for part in [path, *path.parents]:
        if part.name.lower() in EXCLUDED or 'backup' in part.name.lower():
            raise ValueError('excluded boundary: ' + str(part))
        if os.path.lexists(part):
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('link/junction rejected: ' + str(part))
    return path

def relative(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value or value.startswith('/') or any(p in ('', '.', '..') for p in value.split('/')):
        raise ValueError('invalid relative path')
    return value

def child(root, value):
    path = safe(root / relative(value), write=True)
    if not path.is_relative_to(root):
        raise ValueError('escaping path')
    return path

def read_bytes(path):
    path = safe(path)
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_BYTES:
        raise ValueError('not a bounded regular file')
    with path.open('rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    after = path.stat()
    if len(data) > MAX_BYTES or (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError('SOURCE_CHANGED while reading')
    return data

def files(root):
    root = safe(root)
    if not root.is_dir():
        raise ValueError('package directory missing')
    result, total, pending = {}, 0, [root]
    while pending:
        for path in sorted(pending.pop().iterdir()):
            safe(path)
            if path.is_dir():
                pending.append(path)
            else:
                data = read_bytes(path)
                total += len(data)
                if len(result) >= MAX_FILES or total > MAX_BYTES:
                    raise ValueError('capture ceiling exceeded: 2000 files / 32 MiB')
                result[path.relative_to(root).as_posix()] = data
    return dict(sorted(result.items()))

def manifest(data):
    rows = [{'path': p, 'bytes': len(b), 'sha256': digest(b)} for p,b in sorted(data.items())]
    return {'schema_version': '1', 'files': rows, 'package_digest': digest(compact(rows))}

def save(path, value):
    path = safe(path, write=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8') + b'\n')

def copy_files(data, root):
    root.mkdir(parents=True, exist_ok=False)
    for name, content in data.items():
        path = child(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(content)
    if files(root) != data:
        raise ValueError('snapshot readback failed')

def reference(path):
    path = safe(path)
    return {'path': str(path), 'sha256': digest(read_bytes(path))}

def referenced(ref):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}:
        raise ValueError('reference requires path and sha256')
    data = read_bytes(safe(ref['path']))
    if digest(data) != ref['sha256']:
        raise ValueError('SOURCE_CHANGED reference: ' + ref['path'])
    return data

def read_record(path):
    """Read new authoring and legacy records without reinterpreting COMPLETE."""
    value = parse(read_bytes(path))
    kind = value.get('record_kind')
    if kind == 'authoring':
        if value.get('schema_version') != 'authoring-v1' or value.get('authoring_state') not in ('AUTHORED', 'PARTIAL', 'BLOCKED'):
            raise ValueError('invalid authoring record')
    elif kind == 'authoring_baseline':
        if value.get('schema_version') != 'authoring-baseline-v1':
            raise ValueError('invalid authoring baseline')
    elif value.get('schema_version') not in ('1', '2'):
        raise ValueError('unknown record family/version')
    return value

def origin(contract):
    """Resolve a selected, digest-bound baseline. Never infer absent history."""
    prior = contract.get('prior')
    if prior is None:
        if contract.get('history_review') != 'no_known_history':
            raise ValueError('known history must be resolved before observed editing')
        return {'kind': 'observed', 'historical_origin': 'unknown'}, {}
    value = parse(referenced(prior))
    target = str(safe(contract['target_root']))
    if value.get('schema_version') == 'authoring-baseline-v1':
        if value.get('record_kind') != 'authoring_baseline' or value.get('target_root') != target or value.get('target_name') != contract['target_name']:
            raise ValueError('authoring baseline identity mismatch')
        record = parse(referenced(value['authoring_record']))
        prior_run = safe(prior['path']).parent
        if (prior_run / 'publication-failure.json').exists():
            raise ValueError('failed baseline publication')
        publication = parse(read_bytes(prior_run / 'publication-readback.json'))
        if publication.get('state') != 'PUBLISHED' or publication.get('baseline') != prior:
            raise ValueError('baseline publication/readback mismatch')
        if record.get('schema_version') != 'authoring-v1' or record.get('authoring_state') != 'AUTHORED' or record.get('run_id') != value['run_id'] or record.get('target_root') != target:
            raise ValueError('baseline requires matching authored readback record')
        generated = parse(referenced(value['baseline_manifest']))
        if generated != parse(referenced(record['baseline_manifest'])):
            raise ValueError('baseline differs from published authoring record')
        expected = {r['path']: r['sha256'] for r in generated['files']}
        if len(expected) != len(generated['files']) or sorted(expected) != record['managed_paths']:
            raise ValueError('baseline ownership mismatch')
        if manifest(files(safe(value['baseline_root']))) != generated:
            raise ValueError('baseline snapshot changed')
        return {'kind': 'adopted' if record['operation'] == 'adopt' else 'authored', 'reference': prior}, expected
    # Historical provenance is read exactly as written. Its prior success stays
    # historical; this operation publishes only authoring-v1 records.
    if value.get('schema_version') in ('1', '2') and value.get('result') == 'COMPLETE':
        import custody
        if value.get('target_name') != contract['target_name']:
            raise ValueError('legacy target mismatch')
        base = safe(contract.get('legacy_root', safe(prior['path']).parent))
        custody.prior_provenance_record(value, value['schema_version'])
        prior_path = safe(prior['path']).relative_to(base).as_posix()
        problems = []
        if value['schema_version'] == '2':
            captured_files = files(base)
            adopted = custody.reference_json(base, captured_files, value['adoption_origin'], problems)
            custody.adoption_record(base, captured_files, adopted, problems)
            custody.generated_origin_record(base, captured_files, value, value['adoption_origin'], problems, prior_path)
        else:
            cp = (Path(prior_path).parent / 'build-contract.json').as_posix()
            contract_bytes = read_bytes(child(base, cp))
            historical_contract = parse(contract_bytes)
            if digest(contract_bytes) != value['contract_sha256'] or historical_contract.get('target_name') != value['target_name']:
                problems.append('legacy contract identity/digest mismatch')
            inputs = {r['id']: r['sha256'] for r in historical_contract['inputs']}
            if inputs != {r['id']: r['sha256'] for r in value['inputs']} or inputs != {r['id']: r['sha256'] for r in historical_contract['authorization']['inputs']}:
                problems.append('legacy authorized inputs mismatch')
            for row in historical_contract['inputs']:
                data = read_bytes(child(base, row['path']))
                if (len(data), digest(data)) != (row['bytes'], row['sha256']):
                    problems.append('legacy source input changed')
            for row in value['evidence']:
                if digest(read_bytes(child(base, row['path']))) != row['sha256']:
                    problems.append('legacy evidence digest mismatch')
        if problems:
            raise ValueError('; '.join(problems))
        outputs = value['outputs']
        expected = {}
        for row in outputs:
            if row['ownership'] in ('generated', 'adopted'):
                p = child(base, row['baseline_path'])
                if digest(read_bytes(p)) != row['baseline_sha256']:
                    raise ValueError('invalid legacy baseline bytes')
                expected[relative(row['path'])] = row['baseline_sha256']
        if not expected:
            raise ValueError('empty legacy generated baseline')
        return {'kind': 'legacy_generated', 'reference': prior}, expected
    if value.get('schema_version') == '2' and value.get('origin', {}).get('kind') == 'adopted':
        import custody
        base = safe(contract.get('legacy_root', safe(prior['path']).parent))
        problems = []
        captured_files = files(base)
        record, expected = custody.pointer_record(base, captured_files, value, problems)
        custody.adoption_record(base, captured_files, record, problems)
        if problems:
            raise ValueError('; '.join(problems))
        if record.get('recording_state') != 'ADOPTED' or record.get('target_root') != target or record.get('target_name') != contract['target_name']:
            raise ValueError('invalid adoption origin')
        if sorted(expected) != record['managed_paths']:
            raise ValueError('adoption ownership mismatch')
        for p, h in expected.items():
            if digest(read_bytes(child(base, record['snapshot_root'] + '/' + relative(p)))) != h:
                raise ValueError('adoption snapshot mismatch')
        return {'kind': 'adopted', 'reference': prior}, expected
    raise ValueError('unresolved or unsuccessful known history; cannot silently adopt')

def design_input(contract, design_path):
    """Check authoring input shape/bindings, never candidate quality."""
    path = safe(design_path)
    matches = [(i, ref) for i, ref in enumerate(contract['inputs']) if safe(ref['path']) == path]
    if len(matches) != 1:
        raise ValueError('design must bind exactly one contract input')
    index, ref = matches[0]
    value = parse(referenced(ref))
    schema = parse(read_bytes(Path(__file__).resolve().parents[1] / 'schemas/authoring-design.schema.json'))
    record_schema.validate(value, schema)
    if value['target_name'] != contract['target_name']:
        raise ValueError('design target identity mismatch')
    for source in value['source_refs']:
        if safe(source['path']) == path or source not in contract['inputs']:
            raise ValueError('design source must bind another selected contract input')
        referenced(source)
    for rows, key in ((value['behaviors'], 'id'), (value['resources'], 'path'),
                      (value['adverse_conditions'], 'id'), (value['open_questions'], 'id')):
        if len({row[key] for row in rows}) != len(rows):
            raise ValueError('duplicate design ' + key)
    resources = {relative(row['path']) for row in value['resources']}
    for row in value['resources']:
        child(safe(contract['target_root'], write=True), row['path'])
        if (row['kind'] == 'helper') != (row['helper_contract'] is not None):
            raise ValueError('helper contract required only for helpers')
    behaviors = {row['id'] for row in value['behaviors']}
    for row in value['behaviors']:
        if not set(row['resource_paths']) <= resources:
            raise ValueError('undeclared design resource')
    for row in value['adverse_conditions'] + value['execution_limits']:
        if row['behavior_id'] not in behaviors:
            raise ValueError('unknown design behavior')
    for row in value['open_questions']:
        if not set(row['affected_behavior_ids']) <= behaviors:
            raise ValueError('unknown question behavior')
    return index, ref, value


def recheck_stage(run, contract, captured=None):
    """Bind publication to the staged mode/origin; editable evidence, not authority."""
    origin_path = run / 'origin.json'
    current = parse(read_bytes(origin_path))
    if not isinstance(current, dict):
        raise ValueError('invalid stage origin')
    receipt_path = run / 'stage-integrity.json'
    if receipt_path.exists():
        receipt = parse(read_bytes(receipt_path))
        fields = {'schema_version', 'run_id', 'target_name', 'origin_ref',
                  'design_capture_requested'}
        if not isinstance(receipt, dict) or set(receipt) != fields or receipt['schema_version'] != 'authoring-stage-integrity-v1':
            raise ValueError('invalid stage integrity receipt')
        if receipt['run_id'] != contract['run_id'] or receipt['target_name'] != contract['target_name']:
            raise ValueError('stage integrity identity mismatch')
        mode = receipt['design_capture_requested']
        if type(mode) is not bool or current.get('design_capture_requested') is not mode:
            raise ValueError('stage integrity design mode mismatch')
        if receipt['origin_ref'] != reference(origin_path):
            raise ValueError('SOURCE_CHANGED stage origin binding')
    elif ('design_capture_requested' in current or 'design_capture_ref' in current
          or (run / 'design-capture.json').exists()):
        raise ValueError('missing stage integrity receipt; retain stage and start a fresh linked run')
    if captured is not None and current != captured:
        raise ValueError('SOURCE_CHANGED stage origin during publication')
    return current


def recheck_design(run, contract, captured):
    """Reject missing/changed custody and loss of a design-enabled binding."""
    recheck_stage(run, contract, captured)
    capture_path = run / 'design-capture.json'
    requested = captured.get('design_capture_requested')
    if requested is not None and type(requested) is not bool:
        raise ValueError('invalid design capture mode')
    if requested is False:
        if 'design_capture_ref' in captured or capture_path.exists():
            raise ValueError('conflicting legacy/design capture mode')
        return None
    candidates = []
    for ref in contract['inputs']:
        raw = referenced(ref)
        try:
            value = parse(raw)
        except (ValueError, UnicodeError):
            continue
        if isinstance(value, dict) and value.get('schema_version') == 'authoring-design-v1':
            candidates.append(ref)
    if requested is not True and not candidates and 'design_capture_ref' not in captured and not capture_path.exists():
        return None
    if parse(read_bytes(run / 'origin.json')) != captured:
        raise ValueError('design origin changed during publication')
    binding = captured.get('design_capture_ref')
    if not binding or safe(binding['path']) != capture_path:
        raise ValueError('missing or misplaced design capture binding')
    capture = parse(referenced(binding))
    if set(capture) != {'schema_version', 'run_id', 'target_name', 'source_ref', 'snapshot_ref'} or capture['schema_version'] != 'authoring-design-capture-v1':
        raise ValueError('invalid design capture record')
    if capture['run_id'] != contract['run_id'] or capture['target_name'] != contract['target_name']:
        raise ValueError('design capture identity mismatch')
    index, source, value = design_input(contract, capture['source_ref']['path'])
    if capture['source_ref'] != source or capture['snapshot_ref'] != {'path': str(run / 'inputs' / str(index)), 'sha256': source['sha256']}:
        raise ValueError('design capture source/snapshot binding mismatch')
    if referenced(capture['snapshot_ref']) != referenced(source):
        raise ValueError('design snapshot readback mismatch')
    return value


def design_handoff(run, contract, captured, source_action):
    value = recheck_design(run, contract, captured)
    if value is None:
        return ''
    capture = parse(referenced(captured['design_capture_ref']))
    lines = ['Authored design (not observed behavior): ' + json.dumps(capture['source_ref'], ensure_ascii=False),
             'Design capture: ' + json.dumps(captured['design_capture_ref'], ensure_ascii=False),
             'Original selected requirement sources: ' + json.dumps(value['source_refs'], ensure_ascii=False),
             'Open questions: ' + json.dumps(value['open_questions'], ensure_ascii=False),
             'Independently derive fixtures and oracles from original requirements; design challenges are untested design information.',
             'Unperformed obligations: independently exercise all selected native behaviors, outputs, failures and recovery.']
    for row in value['resources']:
        if row['kind'] == 'helper':
            lines.append('Unperformed helper testing: ' + row['path'] + ' ' + json.dumps(row['helper_contract'], ensure_ascii=False))
    lines.append('Source action: ' + source_action + '. AUTHORED and handoff delivery do not establish evaluated-build completion.')
    return '\n'.join(lines) + '\n'


def begin(contract_path, run_root, design=None):
    contract_path, run = safe(contract_path), safe(run_root, write=True)
    raw = read_bytes(contract_path)
    c = parse(raw)
    schema = parse(read_bytes(Path(__file__).resolve().parents[1] / 'schemas/authoring-contract.schema.json'))
    record_schema.validate(c, schema)
    required = {'schema_version', 'run_id', 'project_root', 'target_root', 'target_name', 'operation', 'authorization', 'history_review', 'change_paths', 'requirements', 'capabilities', 'expected_outputs', 'side_effects', 'inputs', 'known_issues'}
    if not isinstance(c, dict) or not required <= set(c) or c['schema_version'] != 'authoring-contract-v1':
        raise ValueError('authoring contract fields missing or wrong version')
    for key in ('run_id', 'project_root', 'target_root', 'target_name', 'operation', 'authorization', 'history_review'):
        if not isinstance(c[key], str) or not c[key].strip():
            raise ValueError('contract ' + key + ' must be a nonempty string')
    for key in ('change_paths', 'requirements', 'capabilities', 'expected_outputs', 'side_effects', 'inputs', 'known_issues'):
        if not isinstance(c[key], list):
            raise ValueError('contract ' + key + ' must be an array')
    if any(not isinstance(x, str) for x in c['known_issues'] + c['change_paths']):
        raise ValueError('known_issues and change_paths must contain strings')
    target, project = safe(c['target_root'], write=True), safe(c['project_root'])
    if not project.is_dir() or not run.is_relative_to(project / 'docs/plan'):
        raise ValueError('run must be under selected project docs/plan')
    if target == project or project.is_relative_to(target) or target.is_relative_to(run) or run.is_relative_to(target):
        raise ValueError('overlapping project/target/evidence roots')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['target_name']) or len(c['target_name']) > 64 or target.name != c['target_name']:
        raise ValueError('resolve valid skill identity and final destination')
    if not c['authorization'] or not c['requirements'] or c['operation'] not in ('create', 'edit', 'import', 'spec_build', 'adopt'):
        raise ValueError('missing authorization/requirements or unsupported operation')
    paths = c['change_paths']
    if not isinstance(paths, list) or len(paths) != len(set(paths)):
        raise ValueError('change_paths must be unique')
    for p in paths:
        child(target, p)
    if c['operation'] in ('create', 'import', 'spec_build') and os.path.lexists(target):
        raise ValueError('occupied destination: use authorized edit')
    if c['operation'] in ('edit', 'adopt') and not target.is_dir():
        raise ValueError('existing package missing')
    if c['operation'] == 'adopt' and c.get('prior'):
        raise ValueError('existing baseline selects edit, not re-adoption')
    for ref in c['inputs']:
        p = safe(ref['path'])
        if p.is_relative_to(target) or p.is_relative_to(run):
            raise ValueError('input overlaps target/evidence')
        referenced(ref)
    selected_design = design_input(c, design) if design is not None else None
    if selected_design is not None:
        if len(c['inputs']) + 1 > MAX_FILES or len(raw) + sum(len(referenced(ref)) for ref in c['inputs']) > MAX_BYTES:
            raise ValueError('input capture ceiling exceeded: 2000 files / 32 MiB')
    # Retain supplied bytes while using one host-resolved identity everywhere.
    resolution = {key: {'supplied': c[key], 'resolved': str(path)}
                  for key, path in (('project_root', project), ('target_root', target))}
    c = dict(c, project_root=str(project), target_root=str(target))
    effective_raw = (raw if parse(raw) == c else
                     json.dumps(c, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8') + b'\n')
    source_ref = {'path': str(contract_path), 'sha256': digest(raw)}
    referenced(source_ref)
    prior, baseline = origin(c)
    before = files(target) if target.exists() else {}
    if not baseline:
        baseline = {p: digest(before[p]) for p in paths if p in before}
    run.mkdir(parents=True, exist_ok=False)
    try:
        (run / 'supplied-contract.json').write_bytes(raw)
        (run / 'contract.json').write_bytes(effective_raw)
        save(run / 'contract-paths.json', resolution)
        save(run / 'contract-source.json', source_ref)
        if read_bytes(run / 'supplied-contract.json') != raw or read_bytes(run / 'contract.json') != effective_raw:
            raise ValueError('contract capture readback mismatch')
        for index, ref in enumerate(c['inputs']):
            p = run / 'inputs' / str(index)
            p.parent.mkdir(exist_ok=True)
            p.write_bytes(referenced(ref))
            if read_bytes(p) != referenced(ref):
                raise ValueError('input snapshot readback mismatch')
        copy_files(before, run / 'before')
        copy_files(before, run / 'candidate')
        save(run / 'before-manifest.json', manifest(before))
        captured = {'prior_origin': prior, 'baseline': baseline,
                                  'design_capture_requested': selected_design is not None,
                                  'contract_sha256': digest(effective_raw),
                                  'supplied_contract_sha256': digest(raw),
                                  'path_resolution_sha256': digest(read_bytes(run / 'contract-paths.json'))}
        if selected_design is not None:
            index, ref, _ = selected_design
            capture = {'schema_version': 'authoring-design-capture-v1', 'run_id': c['run_id'],
                       'target_name': c['target_name'], 'source_ref': ref,
                       'snapshot_ref': reference(run / 'inputs' / str(index))}
            save(run / 'design-capture.json', capture)
            captured['design_capture_ref'] = reference(run / 'design-capture.json')
        save(run / 'origin.json', captured)
        if parse(read_bytes(run / 'origin.json')) != captured:
            raise ValueError('origin capture readback mismatch')
        save(run / 'stage-integrity.json', {
            'schema_version': 'authoring-stage-integrity-v1',
            'run_id': c['run_id'], 'target_name': c['target_name'],
            'origin_ref': reference(run / 'origin.json'),
            'design_capture_requested': selected_design is not None})
        recheck_stage(run, c, captured)
        if selected_design is not None:
            recheck_design(run, c, captured)
        if target.exists() and files(target) != before:
            raise ValueError('SOURCE_CHANGED during capture')
        return {'state': 'STAGED', 'run_root': str(run), 'candidate': str(run / 'candidate')}
    except Exception as exc:
        save(run / 'capture-failure.json', {'state': 'PARTIAL', 'error': str(exc)})
        raise

def publish(run_root, before_write=None):
    """Publish once. before_write is a fault-injection seam for validator trials."""
    run = safe(run_root, write=True)
    if (run / 'capture-failure.json').exists():
        raise ValueError('failed capture; retain it and start a fresh linked run')
    if (run / 'authoring-record.json').exists() or (run / 'publication-failure.json').exists():
        raise ValueError('run already attempted; retain it and start a fresh linked run')
    c = parse(read_bytes(run / 'contract.json'))
    try:
        captured = recheck_stage(run, c)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        failure = {'state': 'BLOCKED', 'run_root': str(run),
                   'applied_paths': [],
                   'error': str(exc) + '; retain this attempt and start a fresh linked run'}
        try:
            save(run / 'publication-failure.json', failure)
        except (OSError, ValueError):
            failure['evidence_write_failed'] = True
        return failure
    target = safe(c['target_root'], write=True)
    applied, problems, rows = [], [], []
    state, delivered, baseline = 'BLOCKED', {}, captured['baseline']
    before, candidate = files(run / 'before'), files(run / 'candidate')
    if manifest(before) != parse(read_bytes(run / 'before-manifest.json')):
        raise ValueError('captured edit base changed')
    if digest(read_bytes(run / 'contract.json')) != captured['contract_sha256']:
        raise ValueError('captured contract changed')
    scope = set(c['change_paths'])
    try:
        project = safe(c['project_root'])
        if c['project_root'] != str(project) or c['target_root'] != str(target):
            raise ValueError('noncanonical staged identity; preserve this attempt and start a fresh run')
        supplied = referenced(parse(read_bytes(run / 'contract-source.json')))
        if 'supplied_contract_sha256' in captured or 'path_resolution_sha256' in captured:
            if digest(read_bytes(run / 'supplied-contract.json')) != captured['supplied_contract_sha256'] or digest(supplied) != captured['supplied_contract_sha256']:
                raise ValueError('SOURCE_CHANGED supplied contract snapshot')
            path_bytes = read_bytes(run / 'contract-paths.json')
            if digest(path_bytes) != captured['path_resolution_sha256']:
                raise ValueError('SOURCE_CHANGED contract path resolution')
            original = parse(supplied)
            expected_paths = {key: {'supplied': original[key], 'resolved': c[key]}
                              for key in ('project_root', 'target_root')}
            if parse(path_bytes) != expected_paths or dict(original, project_root=c['project_root'], target_root=c['target_root']) != c:
                raise ValueError('supplied/effective contract mismatch')
        for ref in c['inputs']:
            referenced(ref)
        recheck_design(run, c, captured)
        origin(c)
        current = files(target) if target.exists() else {}
        if current != before or (not before and c['operation'] in ('create', 'import', 'spec_build') and target.exists()):
            raise ValueError('SOURCE_CHANGED live target differs from captured current')
        outside = [p for p in set(before) | set(candidate) if p not in scope and before.get(p) != candidate.get(p)]
        if outside:
            raise ValueError('candidate changes outside authorized paths: ' + ', '.join(sorted(outside)))
        owned = set(baseline)
        planned = dict(before)
        next_baseline = dict(baseline)
        for p in sorted(scope):
            b = baseline.get(p)
            current_hash = digest(before[p]) if p in before else None
            new_hash = digest(candidate[p]) if p in candidate else None
            if p not in owned and p in before and captured['prior_origin']['kind'] != 'observed':
                action = 'CONFLICT'
            elif current_hash == b:
                action = 'USE_NEW'
            elif current_hash == new_hash or new_hash == b:
                action = 'KEEP_CURRENT'
            else:
                action = 'CONFLICT'
            rows.append({'path': p, 'b_sha256': b, 'c_sha256': current_hash, 'n_sha256': new_hash, 'action': action})
            if action == 'CONFLICT':
                problems.append('REVISION_CONFLICT: ' + p)
            elif action == 'USE_NEW':
                if p in candidate:
                    planned[p] = candidate[p]
                else:
                    planned.pop(p, None)
            if new_hash is None:
                next_baseline.pop(p, None)
            else:
                next_baseline[p] = new_hash
        if problems:
            raise ValueError('; '.join(problems))
        if c['operation'] == 'adopt' and planned != before:
            raise ValueError('adoption cannot change package bytes')
        save(run / 'candidate-manifest.json', manifest(candidate))
        save(run / 'write-plan.json', {'rows': rows, 'planned_manifest': manifest(planned)})
        if files(run / 'candidate') != candidate or files(run / 'before') != before:
            raise ValueError('SOURCE_CHANGED staging input')
        for ref in c['inputs']:
            referenced(ref)
        recheck_design(run, c, captured)
        if (files(target) if target.exists() else {}) != before:
            raise ValueError('SOURCE_CHANGED before first write')
        for p in sorted(set(before) | set(planned)):
            if before.get(p) == planned.get(p):
                continue
            if before_write:
                before_write(p)
            recheck_design(run, c, captured)
            if not target.exists():
                target.mkdir(parents=True, exist_ok=False)
            path = child(target, p)
            actual = read_bytes(path) if path.exists() else None
            if actual != before.get(p):
                raise ValueError('SOURCE_CHANGED before path write: ' + p)
            if p in planned:
                path.parent.mkdir(parents=True, exist_ok=True)
                # Per-path exclusive create or guarded overwrite; no atomicity claim.
                with path.open('wb' if path.exists() else 'xb') as stream:
                    stream.write(planned[p])
            else:
                path.unlink()
            applied.append(p)
        if not target.exists():
            recheck_design(run, c, captured)
            target.mkdir(parents=True, exist_ok=False)
        delivered = files(target)
        if delivered != planned:
            raise ValueError('delivered readback mismatch')
        recheck_design(run, c, captured)
        # Store baseline bytes separately from delivered retained user edits.
        base_bytes = {}
        for p, h in next_baseline.items():
            choices = [candidate.get(p), before.get(p)]
            if c.get('prior') and h not in [digest(x) for x in choices if x is not None]:
                prior = parse(referenced(c['prior']))
                if prior.get('schema_version') == 'authoring-baseline-v1':
                    choices.append(read_bytes(child(safe(prior['baseline_root']), p)))
                else:
                    for row in prior.get('outputs', []):
                        if row['path'] == p:
                            choices.append(read_bytes(child(safe(c.get('legacy_root', safe(c['prior']['path']).parent)), row['baseline_path'])))
            matches = [x for x in choices if x is not None and digest(x) == h]
            if not matches:
                raise ValueError('baseline bytes unavailable: ' + p)
            base_bytes[p] = matches[0]
        copy_files(base_bytes, run / 'baseline')
        save(run / 'baseline-manifest.json', manifest(base_bytes))
        state = 'AUTHORED'
    except (OSError, ValueError, KeyError, TypeError) as exc:
        problems.append(str(exc))
        try:
            delivered = files(target) if target.exists() else {}
        except (OSError, ValueError) as read_error:
            problems.append('after capture unavailable: ' + str(read_error))
        state = 'PARTIAL' if applied or delivered != before else 'BLOCKED'
    try:
        save(run / 'delivered-manifest.json', manifest(delivered))
        record = {'schema_version': 'authoring-v1', 'record_kind': 'authoring', 'run_id': c['run_id'], 'project_root': c['project_root'], 'target_root': str(target), 'target_name': c['target_name'], 'operation': c['operation'], 'authorization': c['authorization'], 'contract': reference(run / 'contract.json'), 'inputs': c['inputs'], 'prior_origin': captured['prior_origin'], 'managed_paths': sorted(next_baseline) if state == 'AUTHORED' else sorted(baseline), 'retained_user_paths': sorted(set(delivered) - (set(next_baseline) if state == 'AUTHORED' else set(baseline))), 'before_manifest': reference(run / 'before-manifest.json'), 'candidate_manifest': reference(run / 'candidate-manifest.json') if (run / 'candidate-manifest.json').exists() else None, 'delivered_manifest': reference(run / 'delivered-manifest.json'), 'applied_paths': applied, 'authoring_state': state, 'validation_status': 'NOT_PERFORMED', 'testing_status': 'NOT_PERFORMED', 'unresolved_issues': c['known_issues'] + problems, 'rows': rows}
        if state == 'AUTHORED':
            record['baseline_manifest'] = reference(run / 'baseline-manifest.json')
        save(run / 'authoring-record.json', record)
        if state == 'AUTHORED':
            try:
                recheck_design(run, c, captured)
                if files(target) != delivered:
                    raise ValueError('SOURCE_CHANGED before baseline publication')
                pointer = {'schema_version': 'authoring-baseline-v1', 'record_kind': 'authoring_baseline', 'run_id': c['run_id'], 'target_root': str(target), 'target_name': c['target_name'], 'authoring_record': reference(run / 'authoring-record.json'), 'baseline_manifest': reference(run / 'baseline-manifest.json'), 'baseline_root': str(run / 'baseline')}
                save(run / 'authoring-baseline.json', pointer)
                if parse(read_bytes(run / 'authoring-baseline.json')) != pointer:
                    raise ValueError('pointer readback mismatch')
                request = {'schema_version': 'validation-request-v1', 'record_kind': 'validation_request', 'authoring_run_id': c['run_id'], 'project_root': c['project_root'], 'target_root': str(target), 'target_name': c['target_name'], 'target_manifest': reference(run / 'delivered-manifest.json'), 'package_digest': manifest(delivered)['package_digest'], 'authoring_record': reference(run / 'authoring-record.json'), 'specification_refs': c['inputs'], 'changed_paths': applied, 'known_issues': record['unresolved_issues'], 'capabilities': c['capabilities'], 'expected_outputs': c['expected_outputs'], 'side_effects': c['side_effects'], 'permission': 'Assessment proposal only; current user invocation determines permitted effects.'}
                save(run / 'validation-request.json', request)
                message = 'Use /skill-validator to validate and test ' + str(target) + ' in project ' + c['project_root'] + '. Read validation request ' + str(run / 'validation-request.json') + ' (SHA-256 ' + digest(read_bytes(run / 'validation-request.json')) + '). Re-read the package and reject stale bindings. Select disposable tests under current authorization.\n\nValidation status: NOT_PERFORMED. Testing status: NOT_PERFORMED.\n'
                source_action = ('created' if c['operation'] in ('create', 'import', 'spec_build') else 'edited') if applied else 'unchanged'
                message += design_handoff(run, c, captured, source_action)
                (run / 'validator-request.md').write_text(message, encoding='utf-8')
                if read_bytes(run / 'validator-request.md').decode('utf-8') != message.replace('\n', os.linesep):
                    raise ValueError('manual handoff readback mismatch')
                recheck_design(run, c, captured)
                if files(target) != delivered:
                    raise ValueError('SOURCE_CHANGED at publication readback')
                save(run / 'publication-readback.json', {'state': 'PUBLISHED', 'authoring_record': reference(run / 'authoring-record.json'), 'baseline': reference(run / 'authoring-baseline.json'), 'request': reference(run / 'validation-request.json'), 'package_digest': manifest(delivered)['package_digest']})
            except (ValueError, OSError, KeyError, TypeError) as exc:
                save(run / 'publication-failure.json', {'state': 'PARTIAL', 'error': str(exc)})
                return {'state': 'PARTIAL', 'run_root': str(run), 'error': str(exc)}
        return {'state': state, 'run_root': str(run), 'applied_paths': applied, 'issues': problems}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # A failed record write after destination effects must not escape as a
        # misleading no-write BLOCKED response. Preserve the observed delta in
        # a separate attempt file when possible, and always return it on stdout.
        failure = {'state': 'PARTIAL' if applied or delivered != before else 'BLOCKED',
                   'run_root': str(run), 'applied_paths': applied,
                   'delivered_manifest': manifest(delivered), 'error': str(exc)}
        try:
            save(run / 'publication-failure.json', failure)
        except (OSError, ValueError):
            failure['evidence_write_failed'] = True
        return failure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('begin'); p.add_argument('--contract', required=True); p.add_argument('--run-root', required=True)
    p.add_argument('--design')
    p = sub.add_parser('publish'); p.add_argument('--run-root', required=True)
    p = sub.add_parser('read'); p.add_argument('--record', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'begin':
            value = begin(args.contract, args.run_root, design=args.design)
        elif args.command == 'publish':
            value = publish(args.run_root)
        else:
            value = read_record(args.record)
        print(json.dumps(value, ensure_ascii=False, allow_nan=False))
        return 1 if value.get('state') in ('BLOCKED', 'PARTIAL') else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'state': 'BLOCKED', 'error': str(exc)}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
