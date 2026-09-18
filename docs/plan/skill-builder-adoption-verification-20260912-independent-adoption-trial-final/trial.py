"""Independent disposable task execution; only documented builder interfaces used."""
import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent
BUILDER = pathlib.Path('C:/Projects/DevForgeAI/src/agents/skills/skill-builder')
STATE = ROOT / 'trial-state.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, indent=2) + '\n'
    path.write_text(value, encoding='utf-8', newline='\n')

def manifest(path):
    return {'schema_version':'1','files':[{'path':p.relative_to(path).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(path.rglob('*'),key=lambda p:p.relative_to(path).as_posix()) if p.is_file()]}

def command(name, args, cwd=None):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, encoding='utf-8')
    write(ROOT / 'commands' / (name+'.json'), {'timestamp':started,'cwd':str(cwd or ROOT),'argv':list(map(str,args)),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    print(name, 'exit', result.returncode)
    print(result.stdout)
    print(result.stderr)
    return result

def state():
    return json.loads(STATE.read_text())

def ref(root, path):
    return {'path':path.relative_to(root).as_posix(),'sha256':digest(path)}

def adoption_prepare():
    s = state()
    project, target, spec = map(pathlib.Path, (s['project'],s['target'],s['spec']))
    run_id = 'adopt-02' if 'adoption_run' in s else 'adopt-01'
    if 'adoption_run' in s:
        shutil.copytree(pathlib.Path(s['adoption_run']),ROOT/'retained/adopt-01-helper-error')
    run = project/'docs/plan/skill-adoptions/receipt-totals'/run_id
    bounded = run/'snapshot'
    ev = bounded/'adoption/evidence'
    ev.mkdir(parents=True)
    before = manifest(target)
    # Target created in this disposable task; check links/limits before copy.
    entries = list(target.rglob('*'))
    assert not any(p.is_symlink() or (p.lstat().st_file_attributes & 1024) for p in entries)
    assert len(before['files']) <= 2000 and sum(x['bytes'] for x in before['files']) <= 32*1024*1024
    shutil.copytree(target, ev/'captured')
    shutil.copytree(target, bounded/'adoption/destination')
    shutil.copyfile(spec, ev/'origin-spec.md')
    shutil.copyfile(ROOT/'commands/origin-known-defect.json', ev/'quality-observation.json')
    write(ev/'complete-manifest.json', before)
    managed = {'schema_version':'1','files':[row for row in before['files'] if row['path'] in s['managed']]}
    write(ev/'managed-manifest.json',managed)
    after = manifest(target)
    write(ev/'source-readback.json', {'schema_version':'1','run_id':run_id,'target_root':str(target),'before':before['files'],'after':after['files'],'spec_before_sha256':digest(ev/'origin-spec.md'),'spec_after_sha256':digest(spec),'outcome':'UNCHANGED' if before==after and digest(spec)==digest(ev/'origin-spec.md') else 'SOURCE_CHANGED'})
    record = {'schema_version':'1','record_kind':'adoption','run_id':'adopt-01','target_name':'receipt-totals','target_root':str(target),'project_root':str(project),'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_origin':'unknown','snapshot_root':'adoption/evidence/captured','snapshot_manifest':ref(bounded,ev/'complete-manifest.json'),'managed_manifest':ref(bounded,ev/'managed-manifest.json'),'managed_paths':s['managed'],'origin_spec':ref(bounded,ev/'origin-spec.md'),'origin_spec_input':{'resolved_path':str(spec),'bytes':spec.stat().st_size,'sha256':digest(spec)},'authorization':{'instruction':s['adoption_instruction'],'target_root':str(target),'managed_manifest_sha256':digest(ev/'managed-manifest.json'),'origin_spec_sha256':digest(spec)},'prior_evidence':[],'quality_evidence':[ref(bounded,ev/'quality-observation.json')],'source_readback':ref(bounded,ev/'source-readback.json'),'known_defects':['Observed floating point numeric output 0.30000000000000004 for the 0.1 plus 0.2 receipt, contrary to reviewed string output contract.']}
    record['run_id']=run_id
    write(ev/'adoption-request.json', {'operation':'adopt','record':record})
    write(run/'cases.jsonl',json.dumps({'case_id':'adopt-real-receipts','grader_id':'adoption_consistency','params':{'evidence':'adoption/evidence','destination':'adoption/destination'},'expected':'PASS'})+'\n')
    s.update(adoption_run=str(run),adoption_root=str(bounded))
    write(STATE,s)
    shutil.copytree(run,ROOT/'retained'/(run_id+'-prepared'))
    print(run)

def adoption_execute():
    s=state(); run=pathlib.Path(s['adoption_run']); bounded=pathlib.Path(s['adoption_root']); ev=bounded/'adoption/evidence'
    result=command(run.name+'-plan',[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/build_evidence.py'),'adoption-plan','--snapshot-root',str(bounded),'--request','adoption/evidence/adoption-request.json'])
    if result.returncode: raise SystemExit(result.returncode)
    write(ev/'adoption-record.json',result.stdout)
    result=command(run.name+'-evaluation',[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/run_evaluation.py'),'--package-root',str(BUILDER),'--candidate-root',str(bounded),'--cases',str(run/'cases.jsonl'),'--output',str(run/'evaluation-results.jsonl'),'--run-id',run.name,'--profile','adoption-v1'])
    if result.returncode:
        shutil.copytree(run,ROOT/'retained/adopt-01-failed')
        raise SystemExit(result.returncode)
    target=pathlib.Path(s['target']); spec=pathlib.Path(s['spec'])
    assert manifest(target)==json.loads((ev/'complete-manifest.json').read_text())
    assert digest(spec)==digest(ev/'origin-spec.md')
    # Rehash every evaluated captured input before publishing.
    assert manifest(ev/'captured')==manifest(target)
    record=json.loads((ev/'adoption-record.json').read_text())
    for key in ['snapshot_manifest','managed_manifest','origin_spec','source_readback']:
        assert digest(bounded/record[key]['path'])==record[key]['sha256']
    pointer={'schema_version':'2','run_id':run.name,'target_name':'receipt-totals','origin':{'kind':'adopted',**ref(bounded,ev/'adoption-record.json')},'baseline':[{'path':row['path'],'sha256':row['sha256']} for row in json.loads((ev/'managed-manifest.json').read_text())['files']]}
    external=run/'published-origin.json'
    assert not external.exists()
    write(external,pointer)
    assert json.loads(external.read_text())==pointer
    shutil.copyfile(external,ev/'published-origin.json')
    write(run/'publication-readback.json',{'published_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'external_path':str(external),'sha256':digest(external),'readback_sha256':digest(ev/'published-origin.json'),'previous_pointer':None,'live_target_manifest':manifest(target),'outcome':'PUBLISHED_READBACK_MATCH'})
    shutil.copytree(run,ROOT/'retained'/(run.name+'-published'))
    print('Adoption publication read back:',external)

def receipt_source(later=False):
    code = '''import csv
import json
import re
import sys
from decimal import Decimal, DecimalException, ROUND_HALF_UP, localcontext

NUMBER = re.compile(r"[+]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\Z")

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("usage: receipt_totals.py RECEIPT.csv")
        values = []
        with open(sys.argv[1], newline='', encoding='utf-8') as handle:
            reader = csv.reader(handle, strict=True)
            if next(reader, None) != ['item', 'quantity', 'unit_price']:
                raise ValueError('expected header item,quantity,unit_price')
            for line, row in enumerate(reader, 2):
                if len(row) != 3 or not row[0].strip():
                    raise ValueError(f'row {line}: expected nonempty item and exactly three cells')
                numbers = []
                for value in row[1:]:
                    value = value.strip()
                    if not NUMBER.fullmatch(value):
                        raise ValueError(f'row {line}: expected finite nonnegative decimal')
                    number = Decimal(value)
                    if not number.is_finite() or number < 0:
                        raise ValueError(f'row {line}: expected finite nonnegative decimal')
                    numbers.append(number)
                values.append(numbers)
        with localcontext() as context:
            context.prec = max(50, sum(len(n.as_tuple().digits) + abs(n.as_tuple().exponent) for pair in values for n in pair) + 10)
            total = sum((quantity * price for quantity, price in values), Decimal(0))
            result = {'total': format(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), '.2f'), 'line_count': len(values)}
            # LATER_OUTPUT
        print(json.dumps(result))
        return 0
    except (OSError, UnicodeError, csv.Error, ValueError, DecimalException) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
'''
    return code.replace('            # LATER_OUTPUT', "            quantity = sum((pair[0] for pair in values), Decimal(0))\n            result['total_quantity'] = format(quantity, 'f')" if later else '')

def contract(root, ev, spec, authorization, run_id):
    inputs=root/ev.parent.name/'inputs'
    inputs.mkdir(parents=True)
    shutil.copyfile(spec,inputs/'spec.md')
    write(inputs/'authorization.txt',authorization)
    rows=[]
    for ident,file,role in [('spec',inputs/'spec.md','spec'),('authorization',inputs/'authorization.txt','clarification')]:
        rows.append({'id':ident,'path':file.relative_to(root).as_posix(),'resolved_path':str(spec if ident=='spec' else file),'role':role,'bytes':file.stat().st_size,'sha256':digest(file)})
    content=spec.read_bytes()
    req={'id':'receipt-contract','origin':'source','text':'Preserve the complete reviewed receipt CLI, decimal arithmetic, JSON, validation, activation, side-effect, and management contract.','source_refs':[{'input_id':'spec','start_byte':0,'end_byte':len(content),'sha256':digest(spec)}],'artifact_paths':['SKILL.md','scripts/receipt_totals.py'],'verification':[{'method':'structural check plus fresh executed receipt cases','expected':'valid skill, decimal JSON values and deterministic errors; no receipt or note mutation'}]}
    data={'schema_version':'1','mode':'spec_build','target_name':'receipt-totals','inputs':rows,'authorization':{'instruction':authorization,'inputs':[{'id':x['id'],'sha256':x['sha256']} for x in rows]},'purpose':'Aggregate receipt CSV into exact decimal JSON totals.','activation':{'positive':['Summarize receipt CSV totals'],'excluded':['Install this skill','Edit my accounting notes']},'requirements':[req],'artifacts':[{'path':p,'role':'entrypoint' if p=='SKILL.md' else 'script','requirement_ids':['receipt-contract'],'purpose':'Receipt contract implementation and usage'} for p in req['artifact_paths']],'workers':[],'dependencies':[]}
    write(ev/'build-contract.json',data)
    return data

def check_candidate(run_id, bounded, ev, candidate, spec, authorization):
    structural=command(run_id+'-candidate-structural',[sys.executable,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(candidate)])
    behavioral=command(run_id+'-candidate-behavior',[sys.executable,'-B','-X','utf8',str(ROOT/'behavior_check.py'),str(candidate/'scripts/receipt_totals.py'),str(ROOT/'behavior-inputs'/run_id),str(ROOT/'behavior-results'/(run_id+'-candidate.json')),run_id])
    if structural.returncode or behavioral.returncode: raise SystemExit('Required candidate check failed')
    check=pathlib.Path(bounded).parent/'candidate-check'
    shutil.copytree(candidate,check/'destination')
    shutil.copytree(candidate,check/'baseline')
    ce=check/'evidence';ce.mkdir()
    # Keep contract's original relative input paths unchanged.
    bc=json.loads((ev/'build-contract.json').read_text())
    for row in bc['inputs']:
        dest=check/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(bounded/row['path'],dest)
    write(ce/'build-contract.json',bc)
    obs={'schema_version':'1','run_id':run_id+'-candidate','target_name':'receipt-totals','outputs':[{'path':x['path'],'sha256':x['sha256']} for x in manifest(candidate)['files']],'structural':json.loads((ROOT/'commands'/(run_id+'-candidate-structural.json')).read_text()),'behavior':json.loads((ROOT/'behavior-results'/(run_id+'-candidate.json')).read_text())}
    write(ce/'checks.json',obs)
    provenance={'schema_version':'1','run_id':run_id+'-candidate','mode':'spec_build','target_name':'receipt-totals','builder_manifest_sha256':digest(BUILDER/'evals/build-manifest.json'),'contract_sha256':digest(ce/'build-contract.json'),'inputs':bc['authorization']['inputs'],'dependencies':[],'outputs':[{'path':x['path'],'sha256':x['sha256'],'ownership':'generated','baseline_path':'baseline/'+x['path'],'baseline_sha256':x['sha256']} for x in manifest(candidate)['files']],'mappings':[{'requirement_id':'receipt-contract','artifact_paths':['SKILL.md','scripts/receipt_totals.py'],'evidence_ids':['checks']}],'evidence':[{'id':'checks',**ref(check,ce/'checks.json')}],'prior_build':None,'result':'COMPLETE'}
    write(ce/'build-provenance.json',provenance)
    cases=check.parent/'candidate-cases.jsonl'
    write(cases,'\n'.join(json.dumps({'case_id':run_id+'-'+g,'grader_id':g,'params':{'path':'destination'} if g=='package_links' else {'evidence':'evidence','destination':'destination'},'expected':'PASS'}) for g in ['package_links','build_traceability'])+'\n')
    result=command(run_id+'-candidate-evaluation',[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/run_evaluation.py'),'--package-root',str(BUILDER),'--candidate-root',str(check),'--cases',str(cases),'--output',str(check.parent/'candidate-results.jsonl'),'--run-id',run_id+'-candidate','--profile','spec-v1'])
    if result.returncode: raise SystemExit(result.returncode)

def revision_prepare():
    s=state();project=pathlib.Path(s['project']);target=pathlib.Path(s['target']);spec=pathlib.Path(s['spec'])
    adoption=pathlib.Path(s['adoption_root'])
    assert (adoption/'adoption/evidence/published-origin.json').exists()
    run_id='revision-01-conflict';run=project/'docs/plan/skill-builds/receipt-totals'/run_id;bounded=run/'snapshot'
    shutil.copytree(adoption/'adoption',bounded/'adoption')
    ev=bounded/run_id/'evidence';ev.mkdir(parents=True)
    authorization=(ROOT/'prompts/02-first-revision-authorization.txt').read_text()
    write(ev/'review-authorization.json',{'instruction':authorization,'spec_sha256':digest(spec),'managed_manifest_sha256':digest(adoption/'adoption/evidence/managed-manifest.json'),'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    bc=contract(bounded,ev,spec,authorization,run_id)
    b=bounded/run_id/'baseline';b.mkdir()
    for name in s['managed']:
        dest=b/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(adoption/'adoption/evidence/captured'/name,dest)
    n=bounded/run_id/'candidate'
    write(n/'SKILL.md','''---
name: receipt-totals
description: Aggregate item, quantity, and unit_price receipt CSV files into decimal JSON totals.
---

# Receipt Totals

Run `python -B -X utf8 <skill-directory>/scripts/receipt_totals.py RECEIPT.csv`
using the bundled [receipt script](scripts/receipt_totals.py).
The CSV header is exactly item,quantity,unit_price. Quantities and prices must
be finite nonnegative decimals; items must be nonempty. Output is a JSON object
with a two-place string total, rounded half-up once, and integer line_count.
An empty receipt returns total 0.00 and zero lines. Invalid input exits 2,
writes a readable stderr error, and emits no JSON. Inputs remain unchanged.
Requires Python 3.10+ standard library. Resolve the script relative to this skill
and receipt paths relative to the caller's working directory. Notes are user-owned.
''')
    write(n/'scripts/receipt_totals.py',receipt_source())
    check_candidate(run_id,bounded,ev,n,spec,authorization)
    write(ROOT/'prompts/03-deliberate-user-edit.txt','Trial user edit: append the comment "User note: preserve receipt troubleshooting context." to the existing scripts/receipt_totals.py after adoption capture and before revision planning. This deliberate development edit is not authorization to override a resulting conflict.\n')
    before=manifest(target)
    current_script=target/'scripts/receipt_totals.py'
    write(current_script,current_script.read_text()+'\n# User note: preserve receipt troubleshooting context.\n')
    write(ROOT/'user-edit-observation.json',{'before':before,'after':manifest(target),'instruction_path':'prompts/03-deliberate-user-edit.txt'})
    shutil.copytree(target,bounded/run_id/'current');shutil.copytree(target,bounded/run_id/'after')
    pointer=ref(bounded,bounded/'adoption/evidence/published-origin.json')
    origin={'kind':'adopted',**ref(bounded,bounded/'adoption/evidence/adoption-record.json')}
    request={'schema_version':'2','run_id':run_id,'status':'PLANNED','baseline':run_id+'/baseline','current':run_id+'/current','candidate':run_id+'/candidate','after':run_id+'/after','required_paths':s['managed'],'owned_paths':s['managed'],'applied_paths':[],'baseline_advanced':False,'readback_passed':False,'evaluation_passed':False,'prior_origin':origin,'adoption_origin':ref(bounded,bounded/'adoption/evidence/adoption-record.json'),'baseline_before':pointer,'baseline_after':pointer}
    write(ev/'revision-request.json',request)
    s.update(revision_run=str(run),revision_root=str(bounded));write(STATE,s)
    result=command(run_id+'-plan',[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/build_evidence.py'),'revision-plan','--snapshot-root',str(bounded),'--request',run_id+'/evidence/revision-request.json'])
    write(ev/'revision-plan.json',result.stdout)
    write(run/'post-plan-live-manifest.json',manifest(target))
    assert manifest(target)==manifest(bounded/run_id/'current')
    shutil.copytree(run,ROOT/'retained'/run_id)
    print('Expected conflict observation; actual exit:',result.returncode)

def apply_and_publish(s, run, bounded, ev, request, later=False):
    run_id=run.name;target=pathlib.Path(s['target']);n=bounded/request['candidate'];c=bounded/request['current'];after=bounded/request['after']
    result=command(run_id+'-plan',[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/build_evidence.py'),'revision-plan','--snapshot-root',str(bounded),'--request',str((ev/'revision-request.json').relative_to(bounded).as_posix())])
    write(ev/'revision-plan-preview.json',result.stdout)
    if result.returncode:
        shutil.copytree(run,ROOT/'retained'/(run_id+'-plan-failed'))
        raise SystemExit(result.returncode)
    plan=json.loads(result.stdout)
    assert manifest(target)==manifest(c)
    writes=[]
    for row in plan['rows']:
        if row['action']!='USE_NEW': continue
        path=target/row['path'];source=n/row['path']
        assert path.resolve().is_relative_to(target.resolve())
        assert (digest(path) if path.exists() else None)==row['c_sha256']
        assert source.exists(), 'This bounded task does not propose deletions'
        path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,path)
        writes.append({'path':row['path'],'before_sha256':row['c_sha256'],'after_sha256':digest(path),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()})
        assert digest(path)==row['n_sha256']
    # The fresh after snapshot replaces only this run's pre-write preview snapshot.
    for item in manifest(target)['files']:
        dest=after/item['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target/item['path'],dest)
    assert manifest(after)==manifest(target)
    write(run/'application-readback.json',{'writes':writes,'before':manifest(c),'after':manifest(after),'live':manifest(target),'outcome':'READBACK_MATCH'})
    structural=command(run_id+'-delivered-structural',[sys.executable,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(target)])
    behavior=command(run_id+'-delivered-behavior',[sys.executable,'-B','-X','utf8',str(ROOT/'behavior_check.py'),str(target/'scripts/receipt_totals.py'),str(ROOT/'behavior-inputs'/(run_id+'-delivered')),str(ROOT/'behavior-results'/(run_id+'-delivered.json')),'later-delivered' if later else run_id+'-delivered'])
    if structural.returncode or behavior.returncode: raise SystemExit('Delivered verification failed; no publication')
    plan.update(status='APPLIED',applied_paths=sorted(x['path'] for x in writes),readback_passed=True,evaluation_passed=True)
    write(ev/'revision-plan.json',plan)
    bc=json.loads((ev/'build-contract.json').read_text())
    obs={'schema_version':'1','run_id':run_id,'target_name':'receipt-totals','outputs':[{'path':x['path'],'sha256':x['sha256']} for x in manifest(target)['files']],'structural':json.loads((ROOT/'commands'/(run_id+'-delivered-structural.json')).read_text()),'behavior':json.loads((ROOT/'behavior-results'/(run_id+'-delivered.json')).read_text()),'readback':json.loads((run/'application-readback.json').read_text())}
    write(ev/'checks.json',obs)
    provenance={'schema_version':'2','run_id':run_id,'mode':'spec_build','target_name':'receipt-totals','builder_manifest_sha256':digest(BUILDER/'evals/build-manifest.json'),'contract_sha256':digest(ev/'build-contract.json'),'inputs':bc['authorization']['inputs'],'dependencies':[],'outputs':[{'path':x['path'],'sha256':x['sha256'],'ownership':'generated' if x['path'] in s['managed'] else 'retained_user','baseline_path':request['candidate']+'/'+x['path'] if x['path'] in s['managed'] else None,'baseline_sha256':digest(n/x['path']) if x['path'] in s['managed'] else None} for x in manifest(target)['files']],'mappings':[{'requirement_id':'receipt-contract','artifact_paths':s['managed'],'evidence_ids':['checks']}],'evidence':[{'id':'checks',**ref(bounded,ev/'checks.json')}],'prior_origin':request['prior_origin'],'adoption_origin':request['adoption_origin'],'result':'COMPLETE'}
    write(ev/'build-provenance.json',provenance)
    cases=run/'revision-cases.jsonl'
    graders=['package_links','build_traceability_v2','revision_consistency_v2']
    write(cases,'\n'.join(json.dumps({'case_id':run_id+'-'+g,'grader_id':g,'params':{'path':request['after']} if g=='package_links' else {'evidence':ev.relative_to(bounded).as_posix(),'destination':request['after']} if g=='build_traceability_v2' else {'path':(ev/'revision-plan.json').relative_to(bounded).as_posix()},'expected':'PASS'}) for g in graders)+'\n')
    def evaluate(label):
        result=command(run_id+'-'+label,[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/run_evaluation.py'),'--package-root',str(BUILDER),'--candidate-root',str(bounded),'--cases',str(cases),'--output',str(run/(label+'-results.jsonl')),'--run-id',run_id+'-'+label,'--profile','revision-spec-v2'])
        if result.returncode:
            shutil.copytree(run,ROOT/'retained'/(run_id+'-'+label+'-failed'))
            raise SystemExit(result.returncode)
    evaluate('delivered')
    assert manifest(target)==manifest(after)
    for row in bc['inputs']:
        assert digest(bounded/row['path'])==row['sha256']
    pointer={'schema_version':'2','run_id':run_id,'target_name':'receipt-totals','origin':{'kind':'generated',**ref(bounded,ev/'build-provenance.json')},'baseline':[{'path':row['path'],'sha256':row['sha256']} for row in manifest(n)['files']]}
    external=run/'published-origin.json';assert not external.exists()
    write(external,pointer)
    assert json.loads(external.read_text())==pointer
    shutil.copyfile(external,ev/'published-origin.json')
    write(run/'publication-readback.json',{'published_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'external_path':str(external),'sha256':digest(external),'readback_sha256':digest(ev/'published-origin.json'),'previous_pointer':request['baseline_before'],'outcome':'PUBLISHED_READBACK_MATCH'})
    shutil.copyfile(ev/'revision-plan.json',ev/'revision-plan-before-publication.json')
    plan.update(baseline_advanced=True,baseline_after=ref(bounded,ev/'published-origin.json'))
    write(ev/'revision-plan.json',plan)
    evaluate('published')
    s.update(successful_run=str(run),successful_root=str(bounded),successful_run_id=run_id)
    write(STATE,s)
    shutil.copytree(run,ROOT/'retained'/(run_id+'-successful'))
    print('Successful generated origin published and re-evaluated:',external)

def resolution_execute():
    s=state();old=pathlib.Path(s['revision_root']);target=pathlib.Path(s['target']);project=pathlib.Path(s['project']);spec=pathlib.Path(s['spec'])
    resolution=(ROOT/'prompts/04-conflict-resolution.txt').read_text()
    assert resolution.strip()
    # Distinct user-directed restoration, recorded independently of builder application.
    before=manifest(target)
    assert before==manifest(old/'revision-01-conflict/current')
    edited=target/'scripts/receipt_totals.py'
    shutil.copyfile(edited,ROOT/'retained/user-edited-script-before-resolution.py')
    shutil.copyfile(old/'revision-01-conflict/baseline/scripts/receipt_totals.py',edited)
    write(ROOT/'resolution-edit-readback.json',{'instruction':resolution,'before':before,'after':manifest(target),'restored_path':'scripts/receipt_totals.py','restored_sha256':digest(edited),'adoption_origin':ref(old,old/'adoption/evidence/adoption-record.json'),'conflict_plan':ref(old,old/'revision-01-conflict/evidence/revision-plan.json'),'candidate_spec_sha256':digest(spec),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    run_id='revision-02-resolved';run=project/'docs/plan/skill-builds/receipt-totals'/run_id;bounded=run/'snapshot'
    shutil.copytree(old,bounded)
    ev=bounded/run_id/'evidence';ev.mkdir(parents=True)
    authorization=(ROOT/'prompts/02-first-revision-authorization.txt').read_text()+'\nSeparate resolution direction:\n'+resolution
    contract(bounded,ev,spec,authorization,run_id)
    for leaf in ['baseline','candidate']:
        shutil.copytree(old/'revision-01-conflict'/leaf,bounded/run_id/leaf)
    check_candidate(run_id,bounded,ev,bounded/run_id/'candidate',spec,authorization)
    shutil.copytree(target,bounded/run_id/'current');shutil.copytree(target,bounded/run_id/'after')
    request=json.loads((old/'revision-01-conflict/evidence/revision-request.json').read_text())
    request.update(run_id=run_id,baseline=run_id+'/baseline',current=run_id+'/current',candidate=run_id+'/candidate',after=run_id+'/after',retry_of=ref(bounded,bounded/'revision-01-conflict/evidence/revision-plan.json'))
    write(ev/'revision-request.json',request)
    apply_and_publish(s,run,bounded,ev,request)

def revalidate_latest():
    s=state()
    for key,profile,casefile in [('adoption_run','adoption-v1','cases.jsonl'),('successful_run','revision-spec-v2','revision-cases.jsonl')]:
        run=pathlib.Path(s[key]);label=run.name+'-latest-60522daa'
        result=command(label,[sys.executable,'-B','-X','utf8',str(BUILDER/'scripts/run_evaluation.py'),'--package-root',str(BUILDER),'--candidate-root',str(run/'snapshot'),'--cases',str(run/casefile),'--output',str(run/'latest-60522daa-results.jsonl'),'--run-id',label,'--profile',profile])
        shutil.copyfile(run/'latest-60522daa-results.jsonl',ROOT/(label+'-results.jsonl'))
        if result.returncode: raise SystemExit(result.returncode)

def later_execute():
    s=state();old=pathlib.Path(s['successful_root']);previous=s['successful_run_id'];target=pathlib.Path(s['target']);project=pathlib.Path(s['project'])
    assert previous=='revision-02-resolved'
    run_id='later-revision-03';run=project/'docs/plan/skill-builds/receipt-totals'/run_id;bounded=run/'snapshot'
    shutil.copytree(old,bounded)
    ev=bounded/run_id/'evidence';ev.mkdir(parents=True)
    authorization=(ROOT/'prompts/05-later-revision-authorization.txt').read_text()
    spec=project/'docs/design/specs/receipt-totals-v2.md'
    original=pathlib.Path(s['spec']).read_text()
    revised=original.replace('decimal string and line_count as an integer.', 'decimal string, line_count as an integer, and total_quantity as the exact fixed-point decimal string sum of quantity without rounding.').replace('{"total":"0.00","line_count":0}', '{"total":"0.00","line_count":0,"total_quantity":"0"}')
    write(spec,revised)
    write(ROOT/'later-spec.md',revised)
    contract(bounded,ev,spec,authorization,run_id)
    prior_pointer=json.loads((old/previous/'evidence/published-origin.json').read_text())
    assert digest(old/prior_pointer['origin']['path'])==prior_pointer['origin']['sha256']
    prior_provenance=json.loads((old/prior_pointer['origin']['path']).read_text())
    for entry in prior_provenance['outputs']:
        if entry['ownership']=='generated': assert digest(old/entry['baseline_path'])==entry['baseline_sha256']
    shutil.copytree(old/previous/'candidate',bounded/run_id/'baseline')
    n=bounded/run_id/'candidate'
    write(n/'SKILL.md',(old/previous/'candidate/SKILL.md').read_text()+'\nSuccessful JSON also includes total_quantity: the exact fixed-point decimal\nstring sum of quantities without rounding; empty receipts use "0".\n')
    write(n/'scripts/receipt_totals.py',receipt_source(later=True))
    check_candidate(run_id,bounded,ev,n,spec,authorization)
    shutil.copytree(target,bounded/run_id/'current');shutil.copytree(target,bounded/run_id/'after')
    pointer=ref(bounded,bounded/previous/'evidence/published-origin.json')
    request={'schema_version':'2','run_id':run_id,'status':'PLANNED','baseline':run_id+'/baseline','current':run_id+'/current','candidate':run_id+'/candidate','after':run_id+'/after','required_paths':s['managed'],'owned_paths':s['managed'],'applied_paths':[],'baseline_advanced':False,'readback_passed':False,'evaluation_passed':False,'prior_origin':prior_pointer['origin'],'adoption_origin':ref(bounded,bounded/'adoption/evidence/adoption-record.json'),'baseline_before':pointer,'baseline_after':pointer}
    write(ev/'revision-request.json',request)
    apply_and_publish(s,run,bounded,ev,request,later=True)

def prepare():
    if STATE.exists():
        raise SystemExit('State already exists; preserve it.')
    project = pathlib.Path(tempfile.mkdtemp(prefix='skill-builder-adoption-trial-'))
    target = project / 'src/agents/skills/receipt-totals'
    target.mkdir(parents=True)
    write(target/'SKILL.md', '''---
name: receipt-totals
description: Summarize item, quantity, and unit_price receipt CSV files as JSON totals.
---

# Receipt Totals

Run the bundled [receipt script](scripts/receipt_totals.py) with a CSV path.
Return its JSON result to the user. Keep receipt input files unchanged.
''')
    write(target/'scripts/receipt_totals.py', '''import csv
import json
import sys

with open(sys.argv[1], newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
total = sum(float(row['quantity']) * float(row['unit_price']) for row in rows)
print(json.dumps({'total': total, 'line_count': len(rows)}))
''')
    write(target/'notes.txt', 'User-maintained: compare September receipts with the paper ledger.\nDo not rewrite this note during skill maintenance.\n')
    spec = project/'docs/design/specs/receipt-totals.md'
    write(spec, '''---
skill_name: receipt-totals
status: reviewed
---

# Receipt totals behavior

Read one UTF-8 CSV path from the command line. The header must be exactly
item,quantity,unit_price in that order. Each item is nonempty after trimming.
Quantity and unit_price are finite nonnegative decimal numbers; fractional
quantities are allowed. Calculate with decimal arithmetic from the input strings.
Do not round individual line products. Round the grand total once to two decimal
places using round-half-up. Write exactly one JSON object with total as a two-place
decimal string and line_count as an integer. An empty data section returns
{"total":"0.00","line_count":0}. Reject missing/extra cells, malformed headers,
negative or nonfinite numbers, and invalid decimal text with exit 2, a readable
stderr error, and no stdout JSON. Successful execution exits 0. Do not modify the
input CSV, contact services, install dependencies, or create receipt output files.
Use Python 3.10+ standard library only. The skill activates for receipt aggregation
requests and routes the user to its bundled executable script. Manage SKILL.md and
scripts/receipt_totals.py only; notes.txt remains user owned.
''')
    instruction = 'Adopt the existing development package at '+str(target)+'. Preserve every existing byte and unknown history. The complete approved managed list is SKILL.md and scripts/receipt_totals.py. Keep notes.txt user-owned. Use the reviewed origin specification at '+str(spec)+'. This instruction authorizes custody recording and external pointer publication/readback only; it does not authorize repair or installation.'
    write(ROOT/'prompts/01-adoption-user-direction.txt', instruction+'\n')
    write(ROOT/'prompts/00-independent-task.txt', 'Use the selected skill-builder on the supplied existing receipt-totals development package. Adopt the package under the separately supplied direction. After adoption, present the concrete specification revision proposal for separate review. Record conflicts, obtain distinct resolution direction, and retain all attempts. Do not edit builder source or install skills.\n')
    shutil.copytree(target, ROOT/'initial-package')
    shutil.copyfile(spec, ROOT/'origin-spec.md')
    write(ROOT/'initial-target-manifest.json', manifest(target))
    write(ROOT/'history-inspection.json', {'selected_project':str(project),'selected_prior_evidence':[],'observation':'New disposable project created by this task. No known successful generated baseline supplied. Existing skill package has unknown historical origin; no history inferred from absent pointer alone.'})
    write(STATE, {'project':str(project),'target':str(target),'spec':str(spec),'managed':['SKILL.md','scripts/receipt_totals.py'],'adoption_instruction':instruction})
    command('python-version', [sys.executable,'--version'])
    command('codex-version', ['C:/Users/bryan/AppData/Local/Programs/OpenAI/Codex/bin/codex.exe','--version'])
    command('pyyaml-capability', [sys.executable,'-B','-c','import yaml; print(yaml.__version__)'])
    sample = ROOT/'behavior-inputs/origin-decimal.csv'
    write(sample, 'item,quantity,unit_price\nCoffee,1,0.1\nTea,1,0.2\n')
    command('origin-known-defect', [sys.executable,'-B','-X','utf8',str(target/'scripts/receipt_totals.py'),str(sample)])
    print(json.dumps(json.loads(STATE.read_text()), indent=2))

if __name__ == '__main__':
    globals()[sys.argv[1]]()
