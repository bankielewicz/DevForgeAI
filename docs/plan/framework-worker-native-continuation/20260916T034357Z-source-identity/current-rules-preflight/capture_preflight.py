"""Bounded evidence supervisor; Rust retains every admission/policy decision."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import time
import record

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--environment', choices=['inherited', 'omit-anthropic-key'], required=True)
args = parser.parse_args()
bindings = json.loads((ROOT/'bindings.json').read_text())
inputs = json.loads((ROOT/'preflight-input-bindings.json').read_text())
binary = Path(bindings['binary'])
request_path = ROOT/'preflight-request.json'
assert record.sha256(binary) == bindings['binary_sha256']
assert record.sha256(request_path) == inputs['request_sha256']
assert record.sha256(ROOT/'preflight-review.unqualified.json') == inputs['review_sha256']
assert record.sha256(ROOT/'source-observation-001/stdout.bin') == inputs['source_inventory_sha256']
assert record.sha256(Path(bindings['candidate_manifest'])) == bindings['candidate_manifest_sha256']
assert record.package_manifest() == json.loads(Path(bindings['candidate_manifest']).read_text())
request = json.loads(request_path.read_text())
assert not Path(request['run_dir']).exists(), 'Never replay or overwrite a retained run'
attempt = ROOT/'preflight-001'
attempt.mkdir(exist_ok=False)
environment = os.environ.copy()
parent_names = sorted(k for k in environment if 'API_KEY' in k.upper() or 'ACCESS_TOKEN' in k.upper() or k.upper() == 'OPENAI_BASE_URL')
removed_names = []
if args.environment == 'omit-anthropic-key':
    for key in list(environment):
        if key.upper() == 'ANTHROPIC_API_KEY':
            removed_names.append(key)
            del environment[key]
child_names = sorted(k for k in environment if 'API_KEY' in k.upper() or 'ACCESS_TOKEN' in k.upper() or k.upper() == 'OPENAI_BASE_URL')
argv = [str(binary), 'preflight', '--request', str(request_path)]
receipt = {'argv': argv, 'cwd': str(record.WORKSPACE), 'executable_sha256': record.sha256(binary),
           'recorder_sha256': record.sha256(Path(__file__).resolve()),
           'request_sha256': record.sha256(request_path), 'start_utc': record.utc_now(),
           'stdin': 'PIPE held open without input until process exits',
           'outer_timeout_seconds': 145, 'environment_mode': args.environment,
           'parent_guard_matched_names': parent_names, 'removed_child_only_names': removed_names,
           'child_guard_matched_names': child_names,
           'credential_values_logged': False, 'saved_credentials_modified': False,
           'native_model_trial_attempts': 0, 'framework_acceptance': 'NOT_EVALUATED'}
with (attempt/'started.json').open('x',encoding='utf-8') as stream:
    json.dump(receipt,stream,indent=2); stream.write('\n')
record.atomic_json(attempt/'candidate-before.json',record.package_manifest())
started = time.monotonic_ns()
code = None
child = None
timed_out = False
spawn_error = None
cleanup = None
with (attempt/'stdout.bin').open('xb') as stdout, (attempt/'stderr.bin').open('xb') as stderr:
    try:
        child = subprocess.Popen(argv,cwd=record.WORKSPACE,env=environment,
                                 stdin=subprocess.PIPE,stdout=stdout,stderr=stderr,shell=False)
        receipt['owned_pid'] = child.pid
        try:
            code = child.wait(timeout=145)
        except subprocess.TimeoutExpired:
            timed_out = True
            command = [r'C:\Windows\System32\taskkill.exe','/PID',str(child.pid),'/T','/F']
            try:
                result = subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,shell=False,timeout=10,check=False)
                (attempt/'containment.stdout.bin').write_bytes(result.stdout)
                (attempt/'containment.stderr.bin').write_bytes(result.stderr)
                cleanup = {'argv':command,'exit_code':result.returncode}
            except subprocess.TimeoutExpired:
                cleanup = {'argv':command,'timed_out':True}
            try:
                code = child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                code = None
    except OSError as error:
        spawn_error = {'type':type(error).__name__,'winerror':getattr(error,'winerror',None),'errno':error.errno}
    finally:
        if child is not None and child.stdin is not None:
            child.stdin.close()
record.atomic_json(attempt/'candidate-after.json',record.package_manifest())
receipt.update({'end_utc':record.utc_now(),'duration_monotonic_ns':time.monotonic_ns()-started,
                'native_exit_code':code,'timed_out':timed_out,'spawn_error':spawn_error,'containment':cleanup,
                'harness_stopped':child is None or child.poll() is not None,
                'parent_names_unchanged':parent_names == sorted(k for k in os.environ if 'API_KEY' in k.upper() or 'ACCESS_TOKEN' in k.upper() or k.upper() == 'OPENAI_BASE_URL'),
                'candidate_unchanged':(attempt/'candidate-before.json').read_bytes() == (attempt/'candidate-after.json').read_bytes()})
for stream_name in ['stdout','stderr']:
    path = attempt/(stream_name+'.bin')
    receipt[stream_name+'_bytes'] = path.stat().st_size
    receipt[stream_name+'_sha256'] = record.sha256(path)
record.atomic_json(attempt/'receipt.json',receipt)
print(json.dumps(receipt))
raise SystemExit(124 if timed_out else 125 if code is None else code)
