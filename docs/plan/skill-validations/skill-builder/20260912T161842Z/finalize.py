import datetime, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('obs',R/'inputs/validator/scripts/observe.py');o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
def write(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def ref(p):return {'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()}
def run(label,args):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();x=subprocess.run(args,cwd=R,capture_output=True,timeout=120)
    (R/('observations/'+label+'.stdout.txt')).write_bytes(x.stdout);(R/('observations/'+label+'.stderr.txt')).write_bytes(x.stderr)
    write('observations/'+label+'.attempt.json',{'command':args,'cwd':str(R),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout':False,'exit_code':x.returncode})
    return x,json.loads(x.stdout)
cmd=['python','-B','-X','utf8',str(R/'inputs/validator/scripts/observe.py')]
x,out=run('final-source-readback-001',cmd+['readback','--source','C:/Projects/DevForgeAI/src/agents/skills/skill-builder','--manifest',str(R/'source-manifest.json')]);assert x.returncode==0 and out['status']=='MATCH'
write('source-after-manifest.json',out['manifest'])
inputs=json.loads((R/'input-capture-manifest.json').read_text())['files'];readbacks=[]
for row in inputs:
    original=o.read_stable(o.safe_path(row['original_path'])); retained=(R/row['retained_path']).read_bytes()
    assert hashlib.sha256(original).hexdigest()==row['sha256'] and original==retained,row['original_path']
    readbacks.append({'original_path':row['original_path'],'retained_path':row['retained_path'],'sha256':row['sha256'],'state':'MATCH'})
validator=o.make_manifest(o.safe_path('C:/Projects/DevForgeAI/src/agents/skills/skill-validator'));before=json.loads((R/'inputs/validator-manifest.json').read_text());assert validator['files']==before['files']
write('observations/final-input-readback.json',{'state':'MATCH','count':len(readbacks),'validator_package_digest':validator['package_digest'],'validator_file_set_match':True,'rows':readbacks})
origin=json.loads((R/'origin-record.json').read_text());origin['source_readback_state']='UNCHANGED';write('origin-record.json',origin)
handoff=json.loads((R/'handoff.json').read_text());handoff['origin']=ref('origin-record.json');write('handoff.json',handoff)
x,records=run('records-001',cmd+['records','--run-root',str(R)])
print(json.dumps({'records_exit':x.returncode,'status':records['status'],'errors':records.get('errors'),'references_checked':records.get('references_checked'),'overall':records.get('overall_assessment')}))
if x.returncode:sys.exit(x.returncode)
files,excluded=o.inventory(R);assert not excluded
rows=[{'path':rel,'bytes':len(o.read_stable(p)),'sha256':hashlib.sha256(o.read_stable(p)).hexdigest()} for rel,p,info in files]
write('final-readback-receipt.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-builder','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assessment_completed':True,'overall_assessment':'FAIL','required_coverage':'7/8','behavior':'INCOMPLETE','builder_readiness':'BLOCKED','proposal_review_state':'pending','target_package_digest':out['manifest']['package_digest'],'target_readback':'MATCH','input_readback':'MATCH','validator_package_digest':validator['package_digest'],'records_status':records['status'],'records_exit_code':x.returncode,'references_checked':records['references_checked'],'report':ref('validation-report.md'),'proposal':ref('revision-spec.md'),'handoff':ref('handoff.json'),'source_readback':ref('observations/final-source-readback-001.stdout.txt'),'input_readback_receipt':ref('observations/final-input-readback.json'),'record_integrity':ref('observations/records-001.stdout.txt'),'retained_files_excluding_this_receipt':rows,'authority':'NONE','target_mutation':'NOT_PERFORMED','retention_limitation':'Initial read-only inspection console streams are in host transcript rather than separate complete stdout/stderr artifacts; exact required source bytes retained. Exploratory routing lacked a disk-pinned expected-label plan and is unscored.'})
print('Final receipt written; no target mutation.')
