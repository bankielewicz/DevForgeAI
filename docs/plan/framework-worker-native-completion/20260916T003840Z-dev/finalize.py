"""Bind developer results and unchanged candidate; evidence, never acceptance authority."""
import json
import re
from pathlib import Path
import record

root = Path(__file__).resolve().parent
declared = json.loads((root/'required-cases.json').read_text())
current = record.package_manifest()
frozen = json.loads((root/'candidate-package.json').read_text())
if current != frozen:
    raise SystemExit('Candidate drift after freeze')
inputs = json.loads((root/'inputs-manifest.json').read_text())
for entry in inputs:
    if record.sha256(Path(entry['path'])) != entry['sha256']:
        raise SystemExit('Input drift:'+entry['path'])
attempts = {}
for label in ['full-tests','final-fmt','final-clippy','doc-tests','full-coverage']:
    receipt = json.loads((root/label/'receipt.json').read_text())
    for stream in ['stdout','stderr']:
        if record.sha256(root/label/(stream+'.bin')) != receipt[stream+'_sha256']:
            raise SystemExit('Raw output mismatch:'+label)
    attempts[label] = receipt
functions = re.findall(r'^test (\S+) \.\.\. (ok|FAILED|ignored)$', (root/'full-tests/stdout.bin').read_text(), re.M)
names = [name for name,status in functions]
if set(names) != set(declared['required_functions']) or len(names) != len(set(names)):
    raise SystemExit('Executed functions differ from declaration')
passed = sum(status=='ok' for name,status in functions)
coverage = json.loads((root/'coverage-analysis.json').read_text())
checks = all(item['native_exit_code']==0 and not item['timed_out'] and item['candidate_unchanged'] for item in attempts.values())
result = {
    'finding':'QA-F-COV-01','developer_status':'FIX_REPORTED' if checks and passed==len(names) and coverage['meets_threshold'] else 'NOT_FIXED',
    'candidate_manifest_sha256':record.sha256(root/'candidate-manifest.json'),
    'platform':'Windows x64','passed_required_functions':passed,'required_functions':len(names),
    'pass_rate_percent':100*passed/len(names),'mandatory_wf_passed':sum(status=='ok' and name.startswith('wf_') for name,status in functions),
    'unit_passed':28 if all(status=='ok' for name,status in functions[:28]) else None,
    'covered_lines':coverage['covered_lines'],'executable_lines':coverage['executable_lines'],'coverage_percent':coverage['percent'],
    'native_trials_attempted':0,'framework_acceptance':'NOT_EVALUATED',
    'commands':[{k:v for k,v in item.items() if k in ['label','argv','cwd','duration_monotonic_ns','native_exit_code','timed_out','candidate_unchanged']} for item in attempts.values()],
}
record.atomic_json(root/'developer-result.json',result)
record.atomic_json(root/'final-source-readback.json',{'candidate_file_count':len(current),'matches_frozen':True,'input_file_count':len(inputs),'inputs_unchanged':True,'candidate_manifest_sha256':result['candidate_manifest_sha256']})
print(json.dumps(result))
