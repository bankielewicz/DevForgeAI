"""Prepare QA-owned execution helpers and case bindings; no product invocation."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / '20260917T023835Z-qa'
DEV = ROOT.parent / '20260917T102726Z-dev-qa-fixes'
SOURCE = 'C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe-logging'
TARGET = SOURCE + '-qa-fixes'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value)


def save(name, value):
    write(name, json.dumps(value, indent=2) + '\n')


for name in ['candidate-manifest.json','input-manifest.json','preserved-manifest.json']:
    for item in read(ROOT / name):
        assert sha(Path(item['path'])) == item['sha256'], item['path']

(ROOT / 'qa-harness').mkdir()
transforms = []
for source in sorted((OLD / 'qa-harness').iterdir()):
    if not source.is_file():
        continue
    data = source.read_bytes()
    if source.name in ['Cargo.toml','independent.rs']:
        data = data.replace(SOURCE.encode(), TARGET.encode())
    target = ROOT / 'qa-harness' / source.name
    target.write_bytes(data)
    transforms.append({'original': str(source), 'original_sha256': sha(source), 'path': str(target), 'sha256': sha(target), 'bytes': target.stat().st_size, 'change': 'selected candidate path only' if data != source.read_bytes() else 'byte-identical'})
write('run_command.py', (OLD / 'run_command.py').read_text().replace(SOURCE, TARGET).replace('20260917T014842Z-dev/qa-harness/Cargo.toml','20260917T102726Z-dev-qa-fixes/supplemental-harness/Cargo.toml').replace('[-5000:]','[-1200:]').replace('[-2000:]','[-1000:]'))
write('measure.py', (OLD / 'measure.py').read_text().replace('152-case','162-case').replace('cases[:152]','cases[:162]'))
old_cases = read(OLD / 'required-cases.json')
declared = read(DEV / 'declared-cases.json')['package_cases']
names = [item['name'] for item in old_cases if item['id'].startswith('PKG-')]
added = sorted(set(declared) - set(names))
assert len(declared) == len(set(declared)) == 162
assert set(names) <= set(declared) and len(added) == 10
cases = [dict(item) for item in old_cases[:152]]
for number,name in enumerate(added,153):
    cases.append({'id':f'PKG-{number:03d}', 'name':name, 'category':'integration', 'provenance':'developer-authored repair regression, independently executed by QA', 'platform':'Windows x64','readiness':'READY','status':'NOT_RUN'})
cases.append({'id':'SUP-01','name':'real_windows_invalid_utf8_and_unterminated_line_preserve_exact_bytes','category':'integration','provenance':'developer-authored supplemental, independently executed by QA','platform':'Windows x64','readiness':'READY','status':'NOT_RUN'})
independent = re.findall(r'^fn (qa_\d\d_\w+)\(', (ROOT / 'qa-harness/independent.rs').read_text(),re.MULTILINE)
assert len(independent) == 13
for number,name in enumerate(independent,1):
    cases.append({'id':f'QA-{number:02d}','name':name,'category':'acceptance','provenance':'original independently authored QA oracle, fresh execution against corrected source','platform':'Windows x64','readiness':'READY','status':'NOT_RUN'})
for ident,name in [('RT-01','success_capture_and_exit_cli_matrix'),('RT-02','failure_history_and_cursor_cli_matrix')]:
    cases.append({'id':ident,'name':name,'category':'acceptance','provenance':'new independent CLI matrix','platform':'Windows x64','readiness':'READY','status':'NOT_RUN'})
assert len(cases) == 178 and sum(item['category']=='unit' for item in cases)==49
save('required-cases.json',cases)
save('helper-provenance.json',transforms)
save('plan-binding.json',{'plan_path':str(ROOT/'plan.md'),'sha256':sha(ROOT/'plan.md'),'candidate_manifest_sha256':sha(ROOT/'candidate-manifest.json'),'input_manifest_sha256':sha(ROOT/'input-manifest.json'),'required_cases_sha256':sha(ROOT/'required-cases.json')})
save('checkpoint.json',{'intent':'retest','plan_readiness':'READY','execution_status':'NOT_STARTED','verdict':None,'candidate_manifest':'candidate-manifest.json','input_manifest':'input-manifest.json','plan_binding':'plan-binding.json','owned_processes':[],'remaining_cases':'required-cases.json','stop_trigger':None,'next_safe_action':'Read back helpers, record integrity, build and inventory then full metric campaign.'})
print(json.dumps({'required_cases':len(cases),'units':49,'new_regressions':added,'plan_sha256':sha(ROOT/'plan.md'),'candidate_manifest_sha256':sha(ROOT/'candidate-manifest.json')},indent=2))
