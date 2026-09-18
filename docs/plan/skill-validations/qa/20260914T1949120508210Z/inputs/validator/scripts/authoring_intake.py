"""Read-only, independent byte-binding intake for manual authoring requests."""
import argparse
import json
from pathlib import Path
import sys
import observe

sys.dont_write_bytecode = True

def reference(ref):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not observe.DIGEST.fullmatch(ref['sha256']):
        raise ValueError('invalid file reference')
    data = observe.read_stable(observe.safe_path(ref['path']))
    if observe.sha256(data) != ref['sha256']:
        raise ValueError('STALE_REQUEST: reference changed: ' + ref['path'])
    return data

def intake(path, expected_digest):
    raw = observe.read_stable(observe.safe_path(path))
    if observe.sha256(raw) != expected_digest:
        raise ValueError('STALE_REQUEST: selected request digest mismatch')
    request = observe.strict_json(raw)
    required = {'schema_version', 'record_kind', 'authoring_run_id', 'project_root', 'target_root', 'target_name', 'target_manifest', 'package_digest', 'authoring_record', 'specification_refs', 'changed_paths', 'known_issues', 'capabilities', 'expected_outputs', 'side_effects', 'permission'}
    if set(request) != required or request['schema_version'] != 'validation-request-v1' or request['record_kind'] != 'validation_request':
        raise ValueError('unsupported authoring request shape/version')
    target = observe.safe_path(request['target_root'])
    project = observe.safe_path(request['project_root'])
    if not project.is_dir() or target.name != request['target_name']:
        raise ValueError('request project/target identity mismatch')
    expected = observe.strict_json(reference(request['target_manifest']))
    actual = observe.make_manifest(target)
    if not actual['complete'] or actual['files'] != expected['files'] or actual['package_digest'] != expected['package_digest'] or actual['package_digest'] != request['package_digest']:
        raise ValueError('STALE_REQUEST: target bytes or package digest mismatch')
    record = observe.strict_json(reference(request['authoring_record']))
    if record.get('schema_version') != 'authoring-v1' or record.get('record_kind') != 'authoring' or record.get('authoring_state') != 'AUTHORED':
        raise ValueError('request requires completed authoring record')
    if any(record.get(key) != request[key] for key in ('project_root', 'target_root', 'target_name')) or record['run_id'] != request['authoring_run_id']:
        raise ValueError('authoring identity mismatch')
    if record['delivered_manifest'] != request['target_manifest'] or record['applied_paths'] != request['changed_paths'] or record['unresolved_issues'] != request['known_issues']:
        raise ValueError('authoring delivery/request mismatch')
    contract = observe.strict_json(reference(record['contract']))
    if contract.get('schema_version') != 'authoring-contract-v1' or any(contract.get(key) != request[key] for key in ('project_root', 'target_root', 'target_name', 'capabilities', 'expected_outputs', 'side_effects')) or contract['inputs'] != request['specification_refs'] or record['inputs'] != request['specification_refs']:
        raise ValueError('authoring contract/request mismatch')
    for ref in request['specification_refs']:
        reference(ref)
    # Inspection of authoring record is custody evidence, not a quality verdict.
    after = observe.make_manifest(target)
    if after['files'] != actual['files'] or not after['complete']:
        raise ValueError('SOURCE_CHANGED during intake')
    return {'schema_version': '1', 'status': 'BOUND', 'target_root': str(target), 'target_name': request['target_name'], 'package_digest': actual['package_digest'], 'authoring_run_id': request['authoring_run_id'], 'history': record['prior_origin'], 'coverage': ['manual request byte bindings', 'independent complete target readback'], 'quality_status': 'NOT_PERFORMED', 'testing_status': 'NOT_PERFORMED', 'limitations': ['No semantic assessment, native activation, or external-effect authorization.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    parser.add_argument('--request-sha256', required=True)
    args = parser.parse_args()
    try:
        result = intake(args.request, args.request_sha256)
        code = 0
    except (ValueError, OSError, KeyError, TypeError, observe.ObservationError) as exc:
        result = {'schema_version': '1', 'status': 'REJECTED', 'error': str(exc)}
        code = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code

if __name__ == '__main__':
    sys.exit(main())
