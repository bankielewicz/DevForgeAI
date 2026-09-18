"""Seal, execute and read back disposable trial evidence; no framework authority.

Only Windows execution is qualified. Existing host permissions remain in force.
Exit: 0 observed PASS/sealed, 1 completed mismatch, 2 invalid/unperformed evidence.
"""
import argparse
import base64
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import observe


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(observe.safe_path(path).read_bytes()).hexdigest()


def read(path):
    return observe.strict_json(observe.safe_path(path).read_bytes())


def write(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)


def reference(value):
    require(type(value) is dict and set(value) == {'path', 'sha256'}, 'expected path/sha256 reference')
    require(type(value['path']) is str and Path(value['path']).is_absolute(), 'reference path must be absolute')
    require(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']), 'invalid digest')
    require(digest(value['path']) == value['sha256'], 'input identity changed: ' + value['path'])


def validate(plan):
    required = {'schema_version', 'case_id', 'kind', 'argv', 'cwd', 'permitted_write_root',
                'inputs', 'prompt', 'requirement_ids', 'dependencies', 'expected_outputs'}
    require(type(plan) is dict and required <= plan.keys() and not set(plan) - required - {'timeout_seconds', 'dependency_attempts'}, 'trial plan fields')
    require(plan['schema_version'] == 'trial-plan-v1', 'trial plan version')
    require(type(plan['case_id']) is str and re.fullmatch('[A-Za-z0-9_-]+', plan['case_id']), 'case identity')
    require(plan['kind'] in ('native', 'utility'), 'trial kind')
    require(type(plan['argv']) is list and plan['argv'] and all(type(v) is str and v and '\0' not in v for v in plan['argv']), 'argv must be an argument array')
    timeout = plan.get('timeout_seconds', 600 if plan['kind'] == 'native' else 120)
    require(type(timeout) in (int, float) and math.isfinite(timeout) and timeout > 0, 'positive finite timeout required')
    for key in ('requirement_ids', 'dependencies'):
        values = plan[key]
        require(type(values) is list and all(type(v) is str and v for v in values) and len(values) == len(set(values)), key + ' must contain unique strings')
    require(plan['requirement_ids'] and plan['case_id'] not in plan['dependencies'], 'requirements required; self dependency forbidden')
    for key in ('cwd', 'permitted_write_root'):
        require(type(plan[key]) is str and Path(plan[key]).is_absolute(), key + ' must be absolute')
    root = observe.safe_path(plan['permitted_write_root']); cwd = observe.safe_path(plan['cwd'])
    require(root.is_dir() and cwd.is_dir() and observe.within(cwd, root), 'cwd must be in disposable write root')
    require(type(plan['inputs']) is list and plan['inputs'], 'input identities required')
    for item in plan['inputs']:
        reference(item)
    require(len({v['path'] for v in plan['inputs']}) == len(plan['inputs']), 'duplicate input reference')
    if plan['prompt'] is not None:
        reference(plan['prompt'])
    require(type(plan['expected_outputs']) is list, 'expected outputs must be array')
    require(plan['kind'] != 'native' or plan['expected_outputs'], 'native scenario requires output/semantic obligations')
    seen = set()
    for output in plan['expected_outputs']:
        require(type(output) is dict and {'path', 'kind', 'requirement_id'} <= output.keys() and not set(output) - {'path', 'kind', 'value', 'requirement_id'}, 'output assertion fields')
        require(observe.normalized_relative(output['path']), 'output must be relative without traversal')
        require(output['kind'] in ('exists', 'text', 'json', 'manual'), 'output assertion kind')
        require(output['requirement_id'] in plan['requirement_ids'], 'unselected output requirement')
        require(output['kind'] not in ('text', 'json') or 'value' in output, 'output expectation missing')
        require(output['kind'] != 'text' or type(output['value']) is str, 'text expectation must be string')
        key = (output['path'], output['kind'], output['requirement_id'])
        require(key not in seen, 'duplicate assertion'); seen.add(key)
        target = observe.safe_path(root / output['path'], must_exist=False)
        require(str(target) not in {item['path'] for item in plan['inputs']}, 'output overlaps protected input')
    dependencies = plan.get('dependency_attempts', {})
    require(type(dependencies) is dict and set(dependencies) == set(plan['dependencies']), 'dependency receipts required')
    for case, attempt in dependencies.items():
        checked = check_attempt(attempt)
        require(checked.get('case_id') == case and checked['outcome'] == 'PASS', 'dependency not qualified: ' + case)
    return timeout


def seal(plan_path, attempt):
    plan_path = observe.safe_path(plan_path); attempt = observe.safe_path(attempt, must_exist=False)
    plan = read(plan_path); timeout = validate(plan)
    root = observe.safe_path(plan['permitted_write_root'])
    require(not observe.within(attempt, root) and not observe.within(root, attempt) and not observe.within(plan_path, root), 'plan, evidence and write roots must be disjoint')
    require(all(not (root / item['path']).exists() for item in plan['expected_outputs']), 'expected outputs must be fresh, not preexisting artifacts')
    attempt.mkdir(parents=True, exist_ok=False)
    (attempt / 'plan.json').write_bytes(plan_path.read_bytes())
    record = dict(schema_version='trial-seal-v1', original_plan={'path': str(plan_path), 'sha256': digest(plan_path)},
                  plan_sha256=digest(attempt / 'plan.json'), timeout_seconds=timeout, sealed_at=now())
    write(attempt / 'seal.json', record)
    return record


def bound(attempt):
    attempt = observe.safe_path(attempt)
    record = read(attempt / 'seal.json'); reference(record['original_plan'])
    require(digest(attempt / 'plan.json') == record['plan_sha256'], 'sealed plan changed')
    plan = read(attempt / 'plan.json'); timeout = validate(plan)
    require(timeout == record['timeout_seconds'], 'sealed timeout changed')
    return plan, record


def outputs(plan):
    checks, artifacts = [], []
    for item in plan['expected_outputs']:
        target = observe.safe_path(Path(plan['permitted_write_root']) / item['path'], must_exist=False)
        status = 'FAIL'; reason = 'Required output absent'
        if target.is_file():
            artifacts.append(dict(path=str(target), sha256=digest(target)))
            status, reason = 'PASS', 'Declared output observed'
            try:
                if item['kind'] == 'text':
                    require(target.read_bytes().decode('utf-8') == item['value'], 'text mismatch')
                elif item['kind'] == 'json':
                    require(json.dumps(read(target), sort_keys=True, ensure_ascii=False) == json.dumps(item['value'], sort_keys=True, ensure_ascii=False), 'JSON mismatch')
                elif item['kind'] == 'manual':
                    status, reason = 'NOT_RUN', 'Independent semantic adjudication required'
            except (ValueError, UnicodeError) as error:
                status, reason = 'FAIL', str(error)
        checks.append(dict(item, result=status, reason=reason))
    return checks, artifacts


def changed(before, after):
    a = {row['path']: row['sha256'] for row in before['files']}
    b = {row['path']: row['sha256'] for row in after['files']}
    return sorted(key for key in a.keys() | b.keys() if a.get(key) != b.get(key))


def run(attempt):
    attempt = observe.safe_path(attempt); plan, sealed = bound(attempt)
    require(not (attempt / 'started.json').exists() and not (attempt / 'result.json').exists(), 'attempt already started; retain it and select a new attempt')
    require(os.name == 'nt', 'Windows adapter only; other platforms NOT_RUN')
    from windows_trial import Job
    started = now(); tick = time.monotonic()
    write(attempt / 'started.json', dict(started_at=started, plan_sha256=sealed['plan_sha256'], seal_sha256=digest(attempt / 'seal.json')))
    before = observe.make_manifest(Path(plan['permitted_write_root']))
    write(attempt / 'before.json', before)
    timeout = False; cleanup = 'NOT_STARTED'; error = None; process = None; job = None
    try:
        job = Job()
        with (attempt / 'stdout.txt').open('xb') as stdout, (attempt / 'stderr.txt').open('xb') as stderr:
            process = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', str(Path(__file__).with_name('trial_worker.py'))],
                                       cwd=plan['cwd'], stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            job.assign(process)
            write(attempt / 'process.json', dict(pid=process.pid, ownership='Windows Job Object; target gated on stdin'))
            prompt = Path(plan['prompt']['path']).read_bytes() if plan['prompt'] else b''
            payload = json.dumps(dict(argv=plan['argv'], cwd=plan['cwd'], stdin=base64.b64encode(prompt).decode())).encode()
            process.communicate(payload, timeout=sealed['timeout_seconds'])
    except subprocess.TimeoutExpired:
        timeout = True
    except (OSError, ValueError, KeyboardInterrupt) as caught:
        error = type(caught).__name__ + ': ' + str(caught)
    finally:
        if job is not None:
            try:
                cleanup = job.cleanup()
            except OSError as caught:
                cleanup = 'UNVERIFIED'; error = str(caught)
            finally:
                job.close()
        if process is not None:
            if process.poll() is None:
                process.kill()  # worker has no target before successful assignment/gate
            process.wait(timeout=10)
            if process.stdin:
                process.stdin.close()
    try:
        bound(attempt)
        unchanged = True
    except (ValueError, OSError) as caught:
        unchanged = False; error = str(caught)
    checks, artifacts = [], []
    try:
        checks, artifacts = outputs(plan)
    except (ValueError, OSError) as caught:
        error = str(caught)
    code = process.returncode if process else None
    after = observe.make_manifest(Path(plan['permitted_write_root']))
    write(attempt / 'after.json', after)
    outcome = 'NOT_RUN'
    if not timeout and not error and cleanup == 'VERIFIED' and unchanged and code == 0:
        outcome = 'FAIL' if any(v['result'] == 'FAIL' for v in checks) else 'NOT_RUN' if any(v['result'] == 'NOT_RUN' for v in checks) else 'PASS'
    result = dict(schema_version='trial-result-v1', case_id=plan['case_id'], kind=plan['kind'], started_at=started,
                  ended_at=now(), elapsed_seconds=time.monotonic()-tick, timeout_seconds=sealed['timeout_seconds'],
                  timeout=timeout, exit_code=code, cleanup=cleanup, input_unchanged=unchanged, outcome=outcome,
                  error=error, plan_sha256=sealed['plan_sha256'], started_sha256=digest(attempt / 'started.json'),
                  manifests=[dict(path=str(attempt / name), sha256=digest(attempt / name)) for name in ('before.json', 'after.json')],
                  changed_paths=changed(before, after),
                  output_checks=checks, artifacts=artifacts, streams=[dict(path=str(attempt / name), sha256=digest(attempt / name)) for name in ('stdout.txt', 'stderr.txt') if (attempt / name).exists()],
                  limitations=['Editable evaluation evidence; not framework acceptance or proof of OS-wide filesystem isolation.', 'Nonzero exit/timeout alone is not a confirmed source defect.'])
    write(attempt / 'result.json', result)
    return result


def check_attempt(attempt):
    attempt = observe.safe_path(attempt); plan, sealed = bound(attempt)
    if not (attempt / 'result.json').exists():
        return dict(case_id=plan['case_id'], outcome='NOT_RUN', reason='No final receipt; do not replay uncertain effects')
    result = read(attempt / 'result.json'); started = read(attempt / 'started.json')
    fields = {'schema_version','case_id','kind','started_at','ended_at','elapsed_seconds','timeout_seconds',
              'timeout','exit_code','cleanup','input_unchanged','outcome','error','plan_sha256',
              'started_sha256','manifests','changed_paths','output_checks','artifacts','streams','limitations'}
    require(type(result) is dict and set(result) == fields and result['schema_version'] == 'trial-result-v1', 'result schema/fields')
    require(result['kind'] == plan['kind'] and type(result['timeout_seconds']) in (int,float) and result['timeout_seconds'] == sealed['timeout_seconds'], 'result timeout/kind differs from plan')
    require(type(result['elapsed_seconds']) in (int,float) and math.isfinite(result['elapsed_seconds']) and result['elapsed_seconds'] >= 0, 'invalid elapsed time')
    require(all(type(result[k]) is bool for k in ('timeout','input_unchanged')), 'receipt booleans required')
    require(result['exit_code'] is None or type(result['exit_code']) is int, 'exit code must be integer or null')
    require(result['cleanup'] in ('VERIFIED','UNVERIFIED','NOT_STARTED') and result['outcome'] in ('PASS','FAIL','NOT_RUN'), 'receipt disposition')
    require(result['error'] is None or type(result['error']) is str, 'receipt error type')
    require(result['case_id'] == plan['case_id'] and result['plan_sha256'] == sealed['plan_sha256'] == started['plan_sha256'], 'result identity mismatch')
    require(result['started_sha256'] == digest(attempt / 'started.json') and started['seal_sha256'] == digest(attempt / 'seal.json'), 'start/seal changed')
    require(sealed['sealed_at'] <= started['started_at'] == result['started_at'] <= result['ended_at'], 'plan/start/result chronology')
    require(type(result['streams']) is list and [v['path'] for v in result['streams']] == [str(attempt / name) for name in ('stdout.txt','stderr.txt')], 'complete original stream references required')
    require(type(result['manifests']) is list and [v['path'] for v in result['manifests']] == [str(attempt / name) for name in ('before.json','after.json')], 'before/after manifests required')
    for item in result['artifacts'] + result['streams'] + result['manifests']:
        reference(item)
    before, after = read(attempt / 'before.json'), read(attempt / 'after.json')
    require(not observe.validate_manifest(before) and not observe.validate_manifest(after), 'invalid side-effect manifest')
    require(after['files'] == observe.make_manifest(Path(plan['permitted_write_root']))['files'], 'write-root state changed after trial')
    require(result['changed_paths'] == changed(before, after), 'side-effect accounting mismatch')
    checked, artifacts = outputs(plan)
    require(checked == result['output_checks'] and artifacts == result['artifacts'], 'output observations changed')
    expected = 'NOT_RUN'
    if not result['timeout'] and not result['error'] and result['cleanup'] == 'VERIFIED' and result['input_unchanged'] and result['exit_code'] == 0:
        expected = 'FAIL' if any(v['result'] == 'FAIL' for v in checked) else 'NOT_RUN' if any(v['result'] == 'NOT_RUN' for v in checked) else 'PASS'
    require(result['outcome'] == expected, 'unsupported trial outcome')
    return result


def summarize(cases):
    require(type(cases) is list and cases, 'complete nonempty selected case inventory required')
    ids, attempts, rows = set(), set(), []
    for case in cases:
        require(type(case) is dict and set(case) == {'case_id', 'attempt', 'dependencies'}, 'case inventory fields')
        require(type(case['case_id']) is str and case['case_id'] not in ids, 'duplicate case identity')
        ids.add(case['case_id'])
        attempt = case['attempt']
        if attempt is not None:
            normalized = str(observe.safe_path(attempt))
            require(normalized not in attempts, 'execution reused across cases'); attempts.add(normalized)
            receipt = check_attempt(attempt)
            sealed_plan = read(Path(attempt) / 'plan.json')
            require(case['dependencies'] == sealed_plan['dependencies'], 'inventory differs from sealed dependencies')
            require(receipt['case_id'] == case['case_id'], 'case/attempt identity mismatch')
            status = receipt['outcome']
        else:
            status = 'NOT_RUN'
        rows.append(dict(case_id=case['case_id'], result=status))
    by_id = {v['case_id']: v['result'] for v in rows}
    for case in cases:
        require(type(case['dependencies']) is list and all(dep in ids and dep != case['case_id'] for dep in case['dependencies']), 'unknown/self dependency')
        require(by_id[case['case_id']] != 'PASS' or all(by_id[dep] == 'PASS' for dep in case['dependencies']), 'passing case has unqualified dependency')
    passed = sum(v['result'] == 'PASS' for v in rows)
    return dict(schema_version='trial-summary-v1', required_total=len(rows), passed=passed, cases=rows,
                outcome='FAIL' if any(v['result'] == 'FAIL' for v in rows) else 'INCOMPLETE' if passed != len(rows) else 'PASS')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    child = commands.add_parser('seal', help='capture a plan before any execution')
    child.add_argument('--plan', required=True); child.add_argument('--attempt', required=True)
    for name in ('run', 'check'):
        child = commands.add_parser(name); child.add_argument('--attempt', required=True)
    child = commands.add_parser('summary'); child.add_argument('--cases', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'seal': result = seal(args.plan, args.attempt)
        elif args.command == 'run': result = run(args.attempt)
        elif args.command == 'check': result = check_attempt(args.attempt)
        else: result = summarize(read(args.cases))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('outcome', 'PASS') == 'PASS' else 1 if result['outcome'] == 'FAIL' else 2
    except (ValueError, OSError, KeyError, TypeError, RecursionError, observe.ObservationError) as error:
        print(json.dumps(dict(outcome='ERROR', error=str(error))))
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
