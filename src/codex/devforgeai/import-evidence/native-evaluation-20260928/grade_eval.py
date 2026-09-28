"""Deterministic grading plus explicit pending semantic rubrics; no self-report scoring."""
import json,re,subprocess
from pathlib import Path
import yaml
from native_eval import E,C,save
def parts(text):
 _,front,body=text.split('---',2)
 return yaml.safe_load(front),body.strip()
def trace(e):
 rows=[json.loads(l)['message'] for l in (e/'protocol.jsonl').read_text().splitlines()]
 items=[o['params']['item'] for o in rows if o.get('method')=='item/completed']
 messages=[i for i in items if i.get('type')=='agentMessage']
 finals=[i['text'] for i in messages if i.get('phase')=='final_answer']
 questions=[o for o in rows if o.get('method')=='item/tool/requestUserInput']
 return rows,items,finals[-1] if finals else '',questions
def document(path):
 t=path.read_text();front=yaml.safe_load(t.split('---',2)[1]);blocks=re.findall(r'^```yaml items[ \t]*\n(.*?)^```[ \t]*$',t,re.M|re.S)
 data={}
 for b in blocks:
  y=yaml.safe_load(b)
  if isinstance(y,dict):
   for k,v in y.items():data.setdefault(k,[]).extend(v if isinstance(v,list) else [])
 return t,front,data
def grade(e):
 result=json.loads((e/'result.json').read_text());case=result['case'];arm=result['arm'];w=e/'workspace';rows,items,last,questions=trace(e)
 raw=(e/'protocol.jsonl').read_text()
 commands=[i for i in items if i.get('type')=='commandExecution']
 reads=[i for i in commands if '/skills/brainstorm/SKILL.md' in i.get('command','') and i.get('exitCode')==0 and 'name: brainstorm' in (i.get('aggregatedOutput') or '')]
 checks=[]
 def add(name,status,why):checks.append({'name':name,'status':status,'evidence':why})
 complete=result['status'] in ('completed','awaiting_input')
 add('execution-complete','PASS' if complete else 'BLOCKED',result['status'])
 for g in sorted((C/'evals/brainstorm'/case/'graders').glob('*.md')):
  meta,body=parts(g.read_text());kind=meta['type'];status='NOT_RUN';why=''
  if kind=='regex':
   target=meta.get('target','last_message');content=None
   if isinstance(target,dict):
    path=w/target['path']
    if path.is_file():content=path.read_text()
    else:why='Required file missing: '+target['path']
   else:content=raw if target=='trace' else last
   if content is None:status='FAIL'
   else:
    flags=0
    for c in meta.get('flags',''):
     flags|={'m':re.M,'s':re.S,'i':re.I}.get(c,0)
    found=bool(re.search(body,content,flags));want=meta.get('match','contains')!='not_contains'
    status='PASS' if found==want else 'FAIL';why=f'Pattern matched={found}; expected={want}'
  elif kind=='file_exists':
   found=any(w.glob(meta['path']));status='PASS' if found==meta['exists'] else 'FAIL';why=f"{meta['path']}: exists={found}"
  elif kind=='manual':
   if g.stem=='skill-fired':
    status='PASS' if reads else ('FAIL' if complete else 'NOT_RUN');why='Completed read of exact candidate SKILL.md' if reads else 'No completed candidate SKILL.md read in retained trace'
   elif g.stem=='skill-not-fired':
    status='PASS' if complete and not reads else ('FAIL' if reads else 'NOT_RUN');why='Complete native event stream; no candidate SKILL.md load/read' if not reads else 'Candidate skill read observed'
  elif kind=='llm':
   why='Pending primary-agent review of saved full response/document against exact rubric'
  add(g.stem,status,why)
 if case=='existing-brn':
  before=json.loads((e/'before.json').read_text());after=json.loads((e/'after.json').read_text());p='docs/specs/brainstorm/BRN-001.md'
  add('full-file-preservation','PASS' if before.get(p)==after.get(p) and p in before else 'FAIL',f"before={before.get(p)}; after={after.get(p)}")
 brn=w/'docs/specs/brainstorm/BRN-001.md'
 if case not in ('existing-brn','ignores-unrelated-request','asks-for-topic') and brn.is_file():
  v=subprocess.run(['python3','-B',str(C/'skills/brainstorm/scripts/validate_brn.py'),str(brn)],text=True,capture_output=True)
  save(e/'independent-validator.json',{'exit_code':v.returncode,'stdout':v.stdout,'stderr':v.stderr})
  add('independent-validator','PASS' if v.returncode==0 else 'FAIL',v.stdout.strip() or v.stderr.strip())
  try:
   text,front,data=document(brn)
   if case=='records-provenance':
    actual=front.get('generated_by',{});ok=actual=={'tool':'codex','model':result.get('model'),'session':result.get('threadId')}
    add('host-provenance-match','PASS' if ok else 'FAIL',f"document={actual}; host model={result.get('model')}; host session={result.get('threadId')}")
   if case=='no-unconfirmed-dispositions':
    ideas=data.get('ideas',[]);ok=bool(ideas) and all(x.get('disposition')=='open' and x.get('reason') is None for x in ideas) and front.get('status')=='draft'
    add('all-decisions-unconfirmed','PASS' if ok else 'FAIL','Parse all ideas and require open/null and draft')
   if case=='writes-valid-brn':
    runs=[i for i in commands if 'validate_brn.py' in i.get('command','') and 'python' in i.get('command','') and 'OK:' in (i.get('aggregatedOutput') or '') and i.get('exitCode')==0]
    add('actual-validator-execution','PASS' if runs else 'FAIL','Successful native validator process with OK output' if runs else 'No successful validator execution; mentions alone do not count')
   save(e/'document-data.json',json.loads(json.dumps({'frontmatter':front,'collections':data},default=str)))
  except Exception as exc:add('parse-output','FAIL',repr(exc))
 semantic=e/'semantic-review.json'
 if semantic.exists():
  reviews=json.loads(semantic.read_text())
  for c in checks:
   if c['name'] in reviews:c.update(reviews[c['name']])
 statuses=[c['status'] for c in checks]
 overall='FAIL' if 'FAIL' in statuses else 'BLOCKED' if 'BLOCKED' in statuses else 'NOT_RUN' if 'NOT_RUN' in statuses else 'PASS'
 save(e/'grade.json',{'case':case,'arm':arm,'repeat':result['repeat'],'status':overall,'checks':checks})
 (e/'last-message.md').write_text(last+'\n')
 return {'trial':e.name,'status':overall,'failed':[c['name'] for c in checks if c['status']=='FAIL'],'pending':[c['name'] for c in checks if c['status']=='NOT_RUN']}
if __name__=='__main__':
 out=[]
 for p in sorted((E/'runs').glob('*/result.json')):
  try:out.append(grade(p.parent))
  except Exception as exc:out.append({'trial':p.parent.name,'grading_error':repr(exc)})
 save(E/'grading-progress.json',out)
 print(json.dumps(out,indent=2))
