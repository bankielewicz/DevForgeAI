import hashlib,json,pathlib,sys
from run_checks import command
R=pathlib.Path(__file__).resolve().parent
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
base='---\nname: example\ndescription: Compute a local result.\n---\n'
cases=[
('valid','structure',base+'# Task\nReturn the requested local result.\n',0),
('missing_description','structure','---\nname: example\n---\nDo task.',1),
('duplicate_yaml','structure','---\nname: example\nname: other\ndescription: Task\n---\nDo task.',1),
('broken_resource','structure',base+'[Instructions](missing.md)\n',1),
('quoted_link','package',base+'The literal syntax is `[label](absent.md)`.\n',2),
('compatibility','structure',base.replace('description:', 'compatibility: Python 3.10+\ndescription:')+'Return output.',0),
('useful_must','structure',base+'MUST preserve source bytes; compare a retained manifest before delivery.\n',0),
('duplicate_json','records','{"schema_version":"1","schema_version":"2"}',1)]
rows=[]
for ident,mode,content,expected in cases:
    folder=R/'trials/probes'/ident/'example';folder.mkdir(parents=True)
    path=folder/('record.json' if mode=='records' else 'SKILL.md')
    path.write_text(content,encoding='utf-8')
    rows.append({'case_id':ident,'mode':mode,'fixture':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'expected_exit':expected,'expected_no_required_failure':ident=='quoted_link'})
(R/'trials/probes/cases.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
save(R/'trials/probes/schema.json',{'type':'object','required':['case_id','mode','fixture','sha256','expected_exit']})
out=[]
for row in rows:
    script='adaptive_observe.py' if row['mode']=='package' else 'observe.py'
    args=[sys.executable,'-B','-X','utf8',str(R/'source/scripts'/script),row['mode'],'--run-root' if row['mode']=='records' else '--source',str(pathlib.Path(row['fixture']).parent)]
    state=command('probe-'+row['case_id'],args)
    raw=json.loads((R/'commands'/('probe-'+row['case_id'])/'stdout.txt').read_text(encoding='utf-8'))
    passed=state['exit_code']==row['expected_exit']
    if row['expected_no_required_failure']:passed=passed and not any(c['result']=='FAIL' for c in raw['checks'])
    out.append({'case_id':row['case_id'],'passed':passed,'actual_exit':state['exit_code'],'expected_exit':row['expected_exit']})
save(R/'trials/probes/results.json',out)
print(json.dumps(out,indent=2))

