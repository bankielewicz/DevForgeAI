"""Write-once evidence index; no framework acceptance authority."""
import json
import os
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
WORK = record.WORKSPACE
ADVISOR = WORK/'docs/plan/advisor-runs/20260916T034812Z-8d3c2a'
INTAKE = WORK/'docs/plan/advisor-runs/20260916T034812Z-8d3c2a-intake'
assert not (ADVISOR/'.lock').exists()
assert not (ROOT/'artifact-manifest.json').exists(), 'Evidence seal is write-once'
readback = json.loads((ROOT/'final-readback.json').read_text())
assert record.package_manifest() == json.loads((ROOT/'candidate-final.json').read_text())
checkpoint = {'created_utc':record.utc_now(),'execution_status':'COMPLETED_WITH_NATIVE_BLOCKER',
              'source_identity_amendment':'COMPLETE','independent_offline_qa':'PASS',
              'native_qualification':'INCOMPLETE','native_trials':'0/2 BLOCKED/NOT_RUN',
              'native_trial_attempts':0,'preflight_attempts':2,'codex_process_starts':1,
              'framework_acceptance':'NOT_EVALUATED','owned_processes':[],
              'candidate_manifest_sha256':readback['candidate_manifest_sha256'],
              'next_action':'Separately select the sanitized diagnostic development/QA handoff; no further launch or policy relaxation in this continuation',
              'handoff':str(ROOT/'native-diagnostic-handoff.md')}
with (ROOT/'checkpoint.json').open('x',encoding='utf-8') as out:
    json.dump(checkpoint,out,indent=2); out.write('\n')
bases = [ROOT,ADVISOR,INTAKE]
for row in readback['fixtures']:
    fixture = Path(row['fixture'])
    assert fixture.name == 'fixture' and fixture.parent.parent == WORK/'docs/plan/framework-worker-trials'
    bases.append(fixture.parent)
rows = []
for base in bases:
    assert base.is_relative_to(WORK)
    for directory, dirs, names in os.walk(base,followlinks=False):
        for name in list(dirs):
            path = Path(directory)/name
            assert not path.lstat().st_file_attributes & 0x400, str(path)
        for name in names:
            path = Path(directory)/name
            stat = path.lstat()
            assert not stat.st_file_attributes & 0x400, str(path)
            rows.append({'path':str(path),'bytes':stat.st_size,'sha256':record.sha256(path)})
rows.sort(key=lambda row:row['path'].casefold())
value = {'created_utc':record.utc_now(),'scope':'Continuation evidence, two owned trial roots, advisor intake/run; excludes already sealed developer and independent QA roots',
         'entry_count':len(rows),'entries':rows}
with (ROOT/'artifact-manifest.json').open('x',encoding='utf-8') as out:
    json.dump(value,out,indent=2); out.write('\n')
errors = [row['path'] for row in rows if Path(row['path']).stat().st_size != row['bytes'] or record.sha256(Path(row['path'])) != row['sha256']]
assert not errors,errors
print(json.dumps({'artifact_count':len(rows),'artifact_manifest_sha256':record.sha256(ROOT/'artifact-manifest.json'),
                  'readback_errors':errors,'report_sha256':record.sha256(ROOT/'continuation-report.md'),
                  'handoff_sha256':record.sha256(ROOT/'native-diagnostic-handoff.md')}))
