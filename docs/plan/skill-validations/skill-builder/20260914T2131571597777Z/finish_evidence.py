"""Final evidence reductions and bounded direct-reference integrity review."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import sys
from prepare_validation import ROOT,PROJECT,VALIDATOR,put,ref,sha,command
import coverage
out=ROOT/'observations/combined-coverage'
out.mkdir(parents=True,exist_ok=False)
c=coverage.Coverage(data_file=str(out/'.coverage'),source=[str(ROOT/'source/scripts'),str(ROOT/'source/assets/adaptive-runtime')],branch=True)
c.combine(data_paths=[str(ROOT/'observations/independent-tests/.coverage'),str(ROOT/'observations/regressions/.coverage')],keep=True)
c.save();c.json_report(outfile=str(out/'coverage.json'))
raw=json.loads((out/'coverage.json').read_bytes());t=raw['totals']
totals={'covered_lines':t['covered_lines'],'executable_lines':t['num_statements'],'covered_branches':t['covered_branches'],'branches':t['num_branches'],'line_percent':100*t['covered_lines']/t['num_statements'],'branch_percent':100*t['covered_branches']/t['num_branches']}
old=json.loads((ROOT/'observations/coverage-summary.json').read_bytes())
put('inputs/initial-coverage-reduction.json',old)
put('observations/coverage-summary.json',{'platform':'Windows','totals':totals,'result':'FAIL','denominator':'All eight first-party executable Python files, no first-party exclusions','tool':'coverage.py native combine/report; statement denominator excludes nonstatement line events','limitations':'Uninstrumented execution receives no credit; Linux coverage NOT_RUN','original_reduction_correction':'Initial manual set union included two nonstatement line events; original reduction retained under inputs.'})
report=(ROOT/'validation-report.md').read_text(encoding='utf-8')
ot=old['totals']
report=report.replace(f"{ot['covered_lines']}/{ot['executable_lines']} = {ot['line_percent']:.6f}%",f"{totals['covered_lines']}/{totals['executable_lines']} = {totals['line_percent']:.6f}%")
report=report.replace(f"{ot['covered_branches']}/{ot['branches']} = {ot['branch_percent']:.6f}%",f"{totals['covered_branches']}/{totals['branches']} = {totals['branch_percent']:.6f}%")
# Keep initially selected rule bytes; add explicit scenario identities from the already-pinned campaign plan.
shutil.copyfile(ROOT/'rule-set.json',ROOT/'inputs/rule-set-initial.json')
rules=json.loads((ROOT/'rule-set.json').read_bytes())
spec=(ROOT/'inputs/skill-builder-postmvp-spec.md').read_text(encoding='utf-8')
for n in range(1,19):
    ident=f'SBPV-{n:02d}'
    row=next(l for l in spec.splitlines() if l.startswith('| '+ident+' '))
    rules['rules'].append({'rule_id':ident,'revision':'1.0','title':row.split('|')[1].strip(),'source_refs':[dict(**ref('inputs/skill-builder-postmvp-spec.md'),source_id='postmvp',locator='5. Independent verification and acceptance; '+ident)],'authority_class':'project_policy','applicability':'applicable','method':'behavioral','expected_observation':row.split('|')[3].strip(),'required':True,'limitation':'Scenario identities predeclared in campaign-plan.json; added here for final schema-1 reference enumeration, not newly invented requirements.'})
old_rule_sha=sha(ROOT/'rule-set.json');put('rule-set.json',rules);report=report.replace(old_rule_sha,sha(ROOT/'rule-set.json'))
(ROOT/'validation-report.md').write_text(report,encoding='utf-8')
findings=json.loads((ROOT/'findings.json').read_bytes());findings['findings'][0]['locator']={'line_start':285,'line_end':288};put('findings.json',findings)
checks=[json.loads(l) for l in (ROOT/'checks.jsonl').read_text(encoding='utf-8').splitlines()]
for row in checks:
    if row['check_id']=='QUALITY-WINDOWS-LINE':
        row['reason']=f"Measured {totals['covered_lines']}/{totals['executable_lines']} first-party statements ({totals['line_percent']:.6f}%), below 95%."
    for r in row['evidence']:r['sha256']=sha(ROOT/r['path'])
(ROOT/'checks.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in checks),encoding='utf-8')
# Evaluation bundle defines actual result records and grades each planned case once.
put('evaluation-result.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['case_id','result','detail'],'properties':{'case_id':{'type':'string'},'result':{'enum':['PASS','FAIL','ERROR','NOT_RUN']},'detail':{'type':'string'},'elapsed_seconds':{'type':'number','minimum':0}},'additionalProperties':False})
put('runtime-dependencies.json',{'windows_python':'3.10.11','linux_python':'3.12.3','libraries':['PyYAML 6.0.2 (existing metadata helpers)','coverage.py 7.9.0 (Windows measurement)','jsonschema (existing regression schema validation)'],'installations':[],'native_cli':'codex-cli 0.154.0','default_execution_ceiling_seconds':120,'authority':'Evidence only; no Rust acceptance'})
bundle_names=['test_independent_design.py','run_tests.py','run_regressions.py','run_adaptive_regressions.py','linux_checks.py','native_trial.py','check_handoff_readback.py','focused_regression.py','evaluation-result.schema.json','runtime-dependencies.json','campaign-plan.json','inputs/skill-builder-postmvp-spec.md','observations/independent-tests/expected.json','observations/regressions/expected.json','observations/adaptive-regressions/plan.json','observations/linux-checks/plan.json']
put('evaluation-bundle-manifest.json',{'schema_version':'validation-evaluation-bundle-v1','purpose':'External Python runners, deterministic reductions, independent assertions/fixture builders, expected case inventories, schema and runtime. Builder-generated runtime candidates did not complete.','artifacts':[ref(p) for p in bundle_names],'fixture_binding':'Each retained case uses run-local requirements/design/contracts with raw-byte refs. Source manifest independently binds product snapshot.','graded_observations':[ref('observations/'+p+'/results.jsonl') for p in ['independent-tests','regressions','adaptive-regressions','linux-checks']]})
(ROOT/'command-log.md').write_text('''# Executed command record

All work used C:/Projects/DevForgeAI unless a retained native/POSIX receipt names the disposable case directory. Python commands used -B -X utf8. Tool transcript retains preliminary discovery and source reads.

| Command/script | Actual outcome |
| --- | --- |
| observe.py snapshot --source src/agents/skills/skill-builder --output this new run | COMPLETE; 47 files, no exclusions |
| prepare_validation.py | Exit 0; structure 0, installed checker 0, text-resources 2 solely snapshot directory identity pending manual adjudication, codex help/version 0 |
| run_tests.py | Exit 1; 33/35 initially; one product failure and one escaped-path harness assertion |
| check_handoff_readback.py | Exit 0; exact parsed path/hash checks pass against retained positive artifact |
| run_regressions.py | Exit 1; 70/71 initially; one copied test resource-root error |
| focused_regression.py | Exit 0; unchanged schema assertions pass using actual validator resource root |
| run_adaptive_regressions.py | Exit 0; 21/21 |
| native_trial.py native-simple / native-branching | Each launcher returns 0 after recording child initialization failure (child exit 1); no model execution |
| native_trial.py native-simple 002 / native-branching 002 | Approved host execution, child workspace-write; each child times out at 120 seconds, taskkill /T /F returns 0; launcher 0 does not mean scenario success |
| wsl --list --verbose | First sandbox access denied; escalated read-only discovery succeeds; Ubuntu available |
| wsl --distribution Ubuntu --cd /mnt/c/Projects/DevForgeAI --exec bash -lc discovery | Exit 0; exact cwd and native python3/timeout verified |
| wsl --distribution Ubuntu --cd /mnt/c/Projects/DevForgeAI --exec timeout 120 python3 -B -X utf8 .../linux_checks.py | Exit 1; 34/35, same product failure |
| assemble_report.py | Exit 0; final observe readback 0, original source/specs unchanged |
| finish_evidence.py | Final combined-coverage and direct-reference audit; see its retained artifacts and tool receipt |

Source helper execution and fixtures are observations, not builder-authorized quality decisions. Retained scripts specify permitted roots and expected effects. No native timeout was increased. No whole test suite was repeated solely to replace a failure. Original harness mistakes and raw output rows remain available.
''',encoding='utf-8')
# Run the actual shipped helper without changing its configured ceiling.
response=command('records',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(ROOT)])
records_text=response.stdout.decode('utf-8',errors='replace')
(ROOT/'record-integrity.md').write_text('''# Record integrity

The shipped observe.py records command was executed against the real run without raising its ceiling. It returned exit '''+str(response.returncode)+'''. The retained regression fixtures include an actual 2,001-file limit case and an oversized-file case; the complete retained run exceeds the helper's global inventory ceiling. Raw stdout/stderr and receipt are in observations/records. This is an evaluator/tooling limitation, not another builder finding.

A separate direct-reference audit checks only the explicitly named final schema-1 documents, all check evidence references, source snapshots and finding identities without recursively capturing trial trees. It does not replace the unavailable whole-run records inventory, inspect every arbitrary fixture JSON as authority, or claim semantic acceptance. Its result is observations/direct-reference-audit.json. Original attempts and limit fixtures remain in place.
''',encoding='utf-8')
handoff=json.loads((ROOT/'handoff.json').read_bytes());handoff.update(report=ref('validation-report.md'),findings=ref('findings.json'));put('handoff.json',handoff)
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe,adaptive_observe
errors=[];verified=[]
names=['sources.json','rule-set.json','origin-record.json','workflow-map.json','checks.jsonl','findings.json','handoff.json','assessment.json']
def walk(v,owner):
    if isinstance(v,dict):
        if 'path' in v and 'sha256' in v:
            p=v['path']
            if not observe.normalized_relative(p):errors.append(owner+': invalid relative ref '+p)
            else:
                try:
                    if sha(ROOT/p)!=v['sha256']:errors.append(owner+': stale ref '+p)
                    verified.append({'owner':owner,'target':p})
                except OSError as e:errors.append(str(e))
        for x in v.values():walk(x,owner)
    elif isinstance(v,list):
        for x in v:walk(x,owner)
for name in names:
    raw=(ROOT/name).read_bytes()
    v=[observe.strict_json(l) for l in raw.decode().splitlines()] if name.endswith('.jsonl') else observe.strict_json(raw)
    walk(v,name)
for s in json.loads((ROOT/'sources.json').read_bytes())['sources']:
    if sha(ROOT/s['snapshot_path'])!=s['sha256']:errors.append('source mismatch '+s['source_id'])
try:adaptive_observe.check_rows((ROOT/'checks.jsonl').read_bytes(),ROOT,ROOT.name,True)
except Exception as e:errors.append('check rows: '+str(e))
for f in findings['findings']:
    if observe.finding_identity(*f['identity'])[0]!=f['finding_id']:errors.append('finding identity')
    if f['identity'][2] not in (ROOT/'source'/f['subject_path']).read_text(encoding='utf-8'):errors.append('finding anchor absent')
if observe.make_manifest(ROOT/'source')['files']!=json.loads((ROOT/'source-manifest.json').read_bytes())['files']:errors.append('source snapshot changed')
rule_ids={r['rule_id'] for r in rules['rules']}
if {r['rule_id'] for r in checks}-rule_ids:errors.append('unknown check rule')
put('observations/direct-reference-audit.json',{'result':'PASS' if not errors else 'FAIL','named_documents':names,'references_verified':len(verified),'errors':errors,'coverage':'Named record refs, AV check schema/coverage, source snapshots and source-source hashes, stable finding anchor/identity. Not full-run record enumeration or framework acceptance.'})
print(json.dumps({'coverage':totals,'records_helper_exit':response.returncode,'direct_reference_errors':errors,'references_verified':len(verified)}))
