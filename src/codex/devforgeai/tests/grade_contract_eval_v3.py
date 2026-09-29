"""Independent post-run source checks; semantic rubrics require an explicit assessment.

Raw attempts never change. Per-check scores, binary conformance, platform failures,
identity gaps and missing semantic evidence are reported separately.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
import yaml

def frontmatter(text):
    m=re.match(r'\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)',text,re.S)
    if not m:return {}
    try: result=yaml.safe_load(m[1])
    except yaml.YAMLError:return {}
    return result if isinstance(result,dict) else {}

def runtime_identity(recorded,expected):
    return bool(expected and str(expected).lower() not in {'unknown','unavailable'} and recorded==expected)

def skill_reads(items,skill,root):
    expected=(root/'skills'/skill/'SKILL.md').resolve();reads=[]
    for i in items:
        if i.get('type')!='commandExecution' or i.get('exitCode')!=0:continue
        output=i.get('aggregatedOutput') or ''
        if not re.search(rf'(?m)^name:\s*(?:devforgeai:)?{re.escape(skill)}\s*$',output):continue
        paths=[]
        for action in i.get('commandActions') or []:
            if action.get('type')=='read' and action.get('path'):
                path=Path(action['path'])
                if not path.is_absolute():path=Path(i.get('cwd') or root.parent/'project')/path
                paths.append(path.resolve())
        # Literal absolute target plus the skill frontmatter is evidence for hosts
        # whose read action parser omits a path; failed compound commands never count.
        if expected in paths or str(expected) in i.get('command',''):
            reads.append({'item':i.get('id'),'target':str(expected)})
    return reads

def file_exists(root,path):
    if '*' in path:return any(p.is_file() for p in root.glob(path))
    return (root/path).is_file()

def source_grade(path,workspace,visible,result,loads,questions):
    text=path.read_text();d=frontmatter(text);body=re.split(r'^---[ \t]*$',text,maxsplit=2,flags=re.M)[-1].strip()
    kind=d['type'];arm=result['arm'];applies=d.get('arm') in (None,'both',arm)
    row={'grader':path.stem,'type':kind,'applicable':applies,'passed':None,'scored':applies}
    if not applies:return row
    if kind in {'skill_loaded','codex_skill_read','tool_used'}:
        row['scored']=False;count=len(loads)
        row['passed']=count>=int(d.get('min',1)) and (d.get('max') is None or count<=int(d['max']))
    elif kind=='request_user_input':
        count=len(questions);row['passed']=count>=int(d.get('min',1)) and (d.get('max') is None or count<=int(d['max']))
    elif kind=='file_exists':row['passed']=file_exists(workspace,d['path'])==d['exists']
    elif kind=='regex':
        target=d.get('target','last_message');present=True
        if isinstance(target,dict):
            p=workspace/target['path'];present=p.is_file();content=p.read_text() if present else ''
        else:content=visible
        flags=sum({'i':re.I,'m':re.M,'s':re.S}.get(f,0) for f in d.get('flags',''))
        row['passed']=present and bool(re.search(body,content,flags))==(d['match']=='contains')
    elif kind=='codex_runtime_identity':
        target=workspace/d['target'];doc=frontmatter(target.read_text()) if target.is_file() else {}
        recorded=doc.get('generated_by',{}).get(d['field'])
        row.update(passed=runtime_identity(recorded,result.get(d['field'])),recorded=recorded,expected=result.get(d['field']))
    elif kind=='llm':row.update(status='REVIEW_REQUIRED',rubric=body,target=d.get('focus',d.get('target','last_message')))
    else:raise ValueError(f'Unsupported grader {path}: {kind}')
    return row

def grade(trial):
    result=json.loads((trial/'result.json').read_text());evidence=trial.parents[1]
    raw=trial/'protocol.jsonl'
    messages=[json.loads(line)['message'] for line in raw.read_text().splitlines()] if raw.exists() else []
    items=[m['params']['item'] for m in messages if m.get('method')=='item/completed']
    agent=[i for i in items if i.get('type')=='agentMessage']
    finals=[i['text'] for i in agent if i.get('phase')=='final_answer'] or [i['text'] for i in agent if i.get('phase')!='commentary']
    final=finals[-1] if finals else ''
    questions=[m['params'] for m in messages if m.get('method')=='item/tool/requestUserInput']
    visible=final+'\n'+'\n'.join(q.get('question','')+'\n'+'\n'.join(o.get('label','') for o in q.get('options',[])) for p in questions for q in p.get('questions',[]))
    (trial/'final-reply.txt').write_text(final+'\n')
    skill=result['skill'];root=Path(result['scratch_parent'])/'devforgeai'
    loads=skill_reads(items,skill,root)
    grades=[source_grade(p,trial/'workspace',visible,result,loads,questions) for p in sorted((evidence/'definitions'/skill/result['case']/'graders').glob('*.md'))]
    semantic=trial/'semantic-review.json'
    if semantic.exists():
        review=json.loads(semantic.read_text())
        assert review['raw_sha256']==hashlib.sha256(raw.read_bytes()).hexdigest(),'Semantic review must bind raw trace'
        for g in grades:
            if g['type']=='llm' and g['applicable'] and g['grader'] in review['graders']:
                a=review['graders'][g['grader']];g.update(passed=a['passed'],status='REVIEWED',assessment=a)
    before=json.loads((trial/'before.json').read_text());after=json.loads((trial/'after.json').read_text())
    changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
    allowed=('docs/specs/prd/',) if skill=='prd' else ('docs/specs/arch/','docs/specs/adr/')
    expected_activation=result['arm']=='plugin' and result['case']!='ignores-unrelated-request'
    guards={'only_contract_outputs_changed':all(p.startswith(allowed) for p in changed),
        'activation_matches':bool(loads)==expected_activation,
        'upstream_preserved':all(before.get(p)==after.get(p) for p in before.keys()|after.keys() if p.startswith(('docs/specs/brainstorm/','docs/specs/policy/')) or (skill=='architecture' and p.startswith('docs/specs/prd/')))}
    if result['arm']=='plugin':guards['candidate_unchanged']=json.loads((trial/'runtime-candidate-check.json').read_text())['unchanged']
    for key in ['head','index','refs']:
        guards[key+'_unchanged']=json.loads((trial/'git-before.json').read_text())[key]==json.loads((trial/'git-after.json').read_text())[key]
    identity=[]
    for path in changed:
        f=trial/'workspace'/path
        if not f.is_file() or not path.endswith('.md'):continue
        gen=frontmatter(f.read_text()).get('generated_by')
        if gen and result['arm']=='plugin':
            identity.append({'path':path,'recorded':gen,'exact_model':runtime_identity(gen.get('model'),result.get('model')),
                             'exact_session':runtime_identity(gen.get('session'),result.get('threadId')),
                             'gap':any(str(gen.get(k,'')).lower() in {'unknown','unavailable',''} for k in ['model','session'])})
    scored=[g for g in grades if g['scored']];pending=any(g['passed'] is None for g in scored)
    score=None if pending or not scored else sum(g['passed'] for g in scored)/len(scored)
    completed=result['status']=='completed' or (result['status']=='awaiting_input' and result['mode']=='plan' and bool(questions))
    binary=bool(completed and scored and not pending and all(g['passed'] is True for g in grades if g['applicable']) and all(guards.values()))
    out={'skill':skill,'case':result['case'],'arm':result['arm'],'repeat':result['repeat'],
         'native_status':result['status'],'source_score':score,'source_grades':grades,'guards':guards,
         'binary_conformance':binary,'semantic_pending':pending,'changed_paths':changed,'identity':identity,
         'qualification_identity_open':any(i['gap'] or not i['exact_model'] or not i['exact_session'] for i in identity)}
    (trial/'grade.json').write_text(json.dumps(out,indent=2)+'\n');return out

def main(evidence):
    plan=json.loads((evidence/'plan.json').read_text());results=[]
    for t in plan['trials']:
        identity=f"{t['skill']}--{t['case']}--{t['arm']}--{t['repeat']}";trial=evidence/'matrix'/identity
        if (trial/'result.json').exists():results.append(grade(trial))
        else:results.append({**t,'native_status':'NOT_RUN','binary_conformance':False})
    summary={'planned':len(results),'attempted':sum(r['native_status']!='NOT_RUN' for r in results),
             'completed':sum(r['native_status']=='completed' for r in results),'binary_pass':sum(r['binary_conformance'] for r in results),
             'semantic_pending':sum(bool(r.get('semantic_pending')) for r in results),'results':results}
    (evidence/'grades.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='results'}))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('evidence',type=Path);a=p.parse_args();main(a.evidence.resolve())
