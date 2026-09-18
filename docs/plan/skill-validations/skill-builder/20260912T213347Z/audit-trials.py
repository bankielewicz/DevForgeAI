import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
ROOT=Path('C:/Projects/DevForgeAI');RUN=Path(__file__).parent;RID=RUN.name
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ref(p):return {'path':p.relative_to(RUN).as_posix(),'sha256':h(p)}
spec=importlib.util.spec_from_file_location('observe',ROOT/'.agents/skills/skill-validator/scripts/observe.py');observe=importlib.util.module_from_spec(spec);spec.loader.exec_module(observe)
cold=RUN/'trials/cold-spec';project=cold/'project';build=project/'docs/plan/skill-builds/task-card/20260912T213535009Z';dest=project/'src/agents/skills/task-card'
measured=0;inputfiles=0;receipts=[]
for stage in ('candidate','delivered','published'):
    manifest=json.loads((build/f'{stage}-input-manifest.json').read_text());command=json.loads((build/'commands'/f'{stage}-evaluation.json').read_text());assert command['exit_code']==0
    assert manifest['retained_before_execution_at']<command['timestamp']
    assert manifest['cases_sha256']==h(build/f'{stage}-cases.jsonl')
    actual=observe.make_manifest(build/f'{stage}-snapshot');assert actual['files']==manifest['snapshot']['files'];inputfiles+=len(actual['files'])
    for line in (build/f'{stage}-results.jsonl').read_text().splitlines():
        row=json.loads(line);assert row['status']=='PASS' and row['expectation_met'] and row['profile']=='spec-v1' and row['cases_sha256']==manifest['cases_sha256']
        assert row['build_manifest_sha256']==h(RUN/'source/evals/build-manifest.json')
        for name,digest in row['candidate_digests'].items():assert h(build/f'{stage}-snapshot'/name)==digest;measured+=1
        receipts.append({'stage':stage,'case_id':row['case_id'],'result':'PASS'})
for stage in ('candidate','delivered'):
    struct=json.loads((build/'commands'/f'{stage}-structural.json').read_text());schema=json.loads((build/'commands'/f'{stage}-schema.json').read_text());assert struct['exit_code']==0 and schema['exit_code']==0
    assert '10' in schema['stdout']
assert observe.make_manifest(dest)['files']==observe.make_manifest(build/'generated-baseline')['files']
assert set(x['path'] for x in observe.make_manifest(dest)['files'])=={'SKILL.md','references/output-schema.json'}
plan=json.loads((cold/'plan.json').read_text());assert h(project/'docs/plan/task-card-spec.md')==plan['fixture_inputs'][0]['sha256']
assert observe.make_manifest(RUN/'source')['files']==json.loads((RUN/'source-manifest.json').read_text())['files']
contract=json.loads((build/'build-contract.json').read_text());prov=json.loads((build/'published-snapshot/evidence/build-provenance.json').read_text());pointer=json.loads((build/'active-baseline.json').read_text())
assert prov['result']=='COMPLETE' and prov['contract_sha256']==h(build/'build-contract.json')
body=(dest/'SKILL.md').read_text();assert all(x in body for x in ('title_required','unassigned','Preserve Unicode and all interior whitespace','No tools, scripts, dependencies','Do not infer a deadline'))
schema=json.loads((dest/'references/output-schema.json').read_text());assert len(schema['oneOf'])==2 and all(x['additionalProperties'] is False for x in schema['oneOf'])
summary='The worker delivered exactly SKILL.md and references/output-schema.json, with two installed structural checks, 10 schema fixtures on candidate and delivery, and three explicit spec-v1 evaluations totaling six PASS observations. Independent readback verified all pre-execution case/snapshot identities, generated/delivered equality and unchanged raw specification. Generated task-card model execution was not performed; supplied schema fixture outputs do not establish that behavior.'
save(cold/'readback-review.json',{'schema_version':'1','run_id':RID,'status':'PASS','agent':'/root/history_review/cold_spec_trial','summary':summary,'evaluation_observations':receipts,'measured_digests_verified':measured,'snapshot_files_verified':inputfiles,'positive_and_failure_schema_cases':10,'schema_executions':2,'structural_checks':2,'no_evaluator_failures_or_retries':True,'input_spec_unchanged':True,'builder_snapshot_unchanged':True,'semantic_review':'Assessor reread both delivered files: exact title/error/default rules, Unicode/interior whitespace, output-only JSON and no effects retained; schema alternatives and additional-key rejection retained.','out_of_scope_writes':'No unauthorized write observed in retained workflow command records; no filesystem enforcement claimed. CLI automatic personal-temp handling produced retained access-denied warnings without escalation.','native_implicit_activation':'NOT_RUN','generated_skill_model_behavior':'NOT_RUN','report':ref(build/'build-report.md'),'final_worker_readback':ref(build/'final-integrity-readback.json'),'project_manifest':ref(cold/'plan.json')})
(cold/'final-response.txt').write_text('''Development build COMPLETE.

- Package: C:/Projects/DevForgeAI/docs/plan/skill-validations/skill-builder/20260912T213347Z/trials/cold-spec/project/src/agents/skills/task-card
- Report/evidence: C:/Projects/DevForgeAI/docs/plan/skill-validations/skill-builder/20260912T213347Z/trials/cold-spec/project/docs/plan/skill-builds/task-card/20260912T213535009Z/build-report.md

Installed structural checker passed twice. All 10 schema cases passed against candidate and delivery. Explicit spec-v1 evaluation passed 2/2 graders for candidate, delivered, and completed published provenance.

Exact snapshots, case files, commands, streams and results are retained. Final integrity readback confirms unchanged snapshots/source and delivery matching the separate generated baseline. No evaluator failures or retries occurred.

Native model behavior and implicit activation were not exercised. No installations occurred. codex --version returned successfully but emitted retained access-denied warnings for automatic personal temp-directory handling.
''',encoding='utf-8')
save(cold/'attempt-001.json',{'schema_version':'1','case_id':'COLD-SPEC-01','executor':'/root/history_review/cold_spec_trial','fork_turns':'none','prompt':ref(cold/'prompt.txt'),'completion_observed_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'result':'COMPLETE','task_output':ref(cold/'final-response.txt'),'limitation':'Dispatch time not separately timestamped; pre-dispatch plan timestamp and host task transcript retain ordering. Final response retained as plain text with Markdown styling normalized.'})
routing=RUN/'trials/routing';candidate=routing/'evaluation-inputs';candidate.mkdir();builder=routing/'evaluator-package'
files,excluded=observe.inventory(RUN/'source');assert not excluded
for name,path,info in files:
    target=builder/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
for name in ('expected.jsonl','observed.jsonl'):(candidate/name).write_bytes((routing/name).read_bytes())
cases=routing/'evaluation-cases.jsonl';cases.write_text(json.dumps({'case_id':'routing-nine-predeclared','grader_id':'routing_outcomes_v2','params':{'expected':'expected.jsonl','observed':'observed.jsonl'},'expected':'PASS'})+'\n',encoding='utf-8')
before=observe.make_manifest(candidate);package=observe.make_manifest(builder)
save(routing/'evaluation-input-manifest.json',{'schema_version':'1','captured_before_execution_at':dt.datetime.now(dt.timezone.utc).isoformat(),'candidate':before,'package':package,'cases_sha256':h(cases)})
argv=['python','-B','-X','utf8',str(builder/'scripts/run_evaluation.py'),'--package-root',str(builder),'--candidate-root',str(candidate),'--cases',str(cases),'--output',str(routing/'evaluation-results.jsonl'),'--run-id',RID+'-routing','--profile','routing-adoption-v1']
save(routing/'evaluation-plan.json',{'schema_version':'1','case_id':'ROUTING-EVALUATOR','requirement_ids':['SB-ROUTING'],'fixture_inputs':[ref(routing/'evaluation-input-manifest.json'),ref(cases)],'expected_outputs':'one PASS; nine independently observed classifications equal predeclared routes','expected_effects':'new result file and stdout/stderr only','executor':'Python subprocess','command':argv,'timeout_seconds':120,'permitted_write_root':str(routing)})
start=dt.datetime.now(dt.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',timeout=120,cwd=ROOT)
(routing/'evaluation.stdout.txt').write_text(p.stdout,encoding='utf-8');(routing/'evaluation.stderr.txt').write_text(p.stderr,encoding='utf-8')
save(routing/'evaluation-attempt-001.json',{'argv':argv,'cwd':str(ROOT),'start':start,'end':dt.datetime.now(dt.timezone.utc).isoformat(),'exit':p.returncode})
assert p.returncode==0,p.stderr
row=json.loads((routing/'evaluation-results.jsonl').read_text());assert row['status']=='PASS' and row['expectation_met'] and row['cases_sha256']==h(cases)
for name,dig in row['candidate_digests'].items():assert h(candidate/name)==dig
assert observe.make_manifest(candidate)['files']==before['files'] and observe.make_manifest(builder)['files']==package['files']
observed={r['case_id']:r['route'] for r in map(json.loads,(routing/'observed.jsonl').read_text().splitlines())};expected={r['case_id']:r['route'] for r in map(json.loads,(routing/'expected.jsonl').read_text().splitlines())};assert observed==expected and len(observed)==9
save(routing/'readback.json',{'schema_version':'1','run_id':RID,'status':'PASS','agent':'/root/history_review/routing_trial','fork_turns':'none','prompt':ref(routing/'prompt.txt'),'classification_cases':9,'all_labels_match':True,'evaluation_exit':p.returncode,'profile':'routing-adoption-v1','evaluator_package_unchanged':True,'candidate_input_unchanged':True,'cases_sha256':h(cases),'native_activation':'NOT_RUN','reasoning':ref(routing/'reasoning.md'),'observed':ref(routing/'observed.jsonl'),'expected':ref(routing/'expected.jsonl')})
print('Cold independently verified:',measured,'measured hashes;',inputfiles,'snapshot files. Routing:',p.returncode,'nine labels PASS.')
