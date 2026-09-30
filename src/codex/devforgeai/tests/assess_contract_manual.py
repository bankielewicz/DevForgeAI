"""Independent checks of sealed manual attempts; no actor assertions are trusted."""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
import yaml
from grade_contract_eval_v3 import frontmatter

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def item_blocks(text):
    rows={}
    for block in re.findall(r'```yaml items\n(.*?)\n```',text,re.S):
        data=yaml.safe_load(block)
        for group,items in data.items():
            for row in items or []:rows[row['id']]={'group':group,'data':row}
        starts=list(re.finditer(r'^  - id: ([^\n]+)\n',block,re.M))
        for i,m in enumerate(starts):
            rows[m[1].strip()]['raw']=block[m.start():starts[i+1].start() if i+1<len(starts) else len(block)].rstrip()
    return rows

def assess(a):
    result=json.loads((a/'result.json').read_text());binding=json.loads((a/'binding.json').read_text());name=a.name
    before=json.loads((a/'before.json').read_text());after=json.loads((a/'after.json').read_text())
    changes=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
    messages=[json.loads(l)['message'] for l in (a/'protocol.jsonl').read_text().splitlines()]
    items=[m['params']['item'] for m in messages if m.get('method')=='item/completed']
    commands=[i for i in items if i.get('type')=='commandExecution']
    qtools=[m['params'] for m in messages if m.get('method')=='item/tool/requestUserInput']
    replies=[p.read_text() for p in sorted((a/'turns').glob('*/final-reply.txt'))]
    final=replies[-1] if replies else '';allreplies='\n'.join(replies)
    batches=[r for r in replies if re.search(r'(?m)^1\. ',r)]
    maxtext=max([int(x) for r in batches for x in re.findall(r'(?m)^(\d+)\. ',r)]+[0])
    maxnative=max([len(q.get('questions',[])) for q in qtools]+[0])
    checks={'attempt_completed':not result['error'] and all(t['status']=='completed' for t in result['turns']),
            'candidate_unchanged':result['runtime_candidate_unchanged'],
            'upstream_unchanged':all(before[p]==after.get(p) for p in before if p.startswith(('docs/specs/brainstorm/','docs/specs/policy/')) or (name in {'failed-supersession','accepted-decision-failure'} and p.startswith('docs/specs/prd/')))}
    gb=json.loads((a/'git-before.json').read_text());ga=json.loads((a/'git-after.json').read_text())
    for key in ['head','refs','index']:checks[key+'_unchanged']=gb[key]==ga[key]
    workspace=a/'workspace';prd=workspace/'docs/specs/prd/PRD-001.md'
    source=prd.read_text() if prd.is_file() else '';fm=frontmatter(source);blocks=item_blocks(source) if source else {}
    notes=[];coverage={};identities=[]
    for path in changes:
        p=workspace/path
        if p.is_file() and p.suffix=='.md':
            g=frontmatter(p.read_text()).get('generated_by')
            if g:identities.append({'path':path,'recorded':g,'exact_model':g.get('model')==result['model'],'exact_session':g.get('session')==result['threadId']})
    if name in {'partial-text','partial-tool','local-budget','invalid-local'}:
        limit=5 if name=='local-budget' else 8
        checks.update(prd_exists=prd.is_file(),context_preserved=fm.get('stage')=='mvp' and fm.get('operating_context')=='internal',
                      question_budget=len(batches)+len(qtools)<=limit,max_three_questions=max(maxtext,maxnative)<=3)
        if name.startswith('partial-'):
            nfr=[v['data'] for v in blocks.values() if v['group']=='non_functional_requirements']
            checks.update(no_constraint_nfr=not any(x.get('category')=='constraint' for x in nfr),
                privacy_phone_requirement=any(x.get('category')=='privacy' and 'phone' in x.get('statement','').lower() and 'coordinator' in x.get('statement','').lower() for x in nfr),
                privacy_remainder_open='[NEEDS CLARIFICATION: privacy requirements for internal]' in source,
                no_constraint_marker='[NEEDS CLARIFICATION: constraint requirements for internal]' not in source,
                constraint_none_prose=bool(re.search(r'(?is)## 7\..*?(?:no fixed constraints|constraints.*?none|no .*?constraints)',source)),
                no_target_marked=any(v['group']=='success_metrics' and '[NEEDS CLARIFICATION:' in str(v['data'].get('target')) for v in blocks.values()),
                defaults_reported='interview.max_calls=8 (default)' in final,
                unavailable_disclosed=all(fm.get('generated_by',{}).get(k)=='unavailable' for k in ['model','session']) and 'unavailable' in final.lower() and 'unavailable' in source.split('## Change Log')[-1])
            if name=='partial-tool':checks['native_question_exercised']=bool(qtools)
            else:checks['plain_text_branch_exercised']=bool(batches) and not qtools
            notes.append('Question count includes tool calls and numbered plain-text batches. Root operator reviewed the actual questions and supplied the frozen scenario facts. Runtime identity disclosure does not satisfy exact BEH-10 identity.')
        elif name=='local-budget':checks['local_budget_reported']='interview.max_calls=5 (local)' in final
        else:
            checks.update(default_budget_reported='interview.max_calls=8 (default)' in final,
                          bad_budget_reported='interview.max_calls' in final and 'ignored' in final.lower(),
                          forbidden_local_key_reported='architecture.mandated_platforms' in final and '.codex/devforgeai.local.md' in final)
    elif name in {'stop-save-yes','stop-save-no'}:
        offer=replies[1] if len(replies)>1 else ''
        checks['save_choice_offered']=bool(re.search(r'(?is)(save.*draft|draft.*save)',offer))
        if not checks['save_choice_offered']:
            coverage['requested_save_answer']='NOT_RUN: native actor stopped without offering the required save choice; no fabricated answer or automatic retry'
        elif name=='stop-save-yes':
            checks.update(saved_draft=prd.is_file() and fm.get('status')=='draft',
                          undecided_requirement_fields_null=all(v['data'].get('priority') is None and v['data'].get('release') is None for v in blocks.values() if v['group'] in {'functional_requirements','non_functional_requirements'}))
        else:checks['no_prd_saved']=not prd.exists()
    elif name in {'unknown-brn','malformed-brn','policy-sv01','policy-sv02','policy-calendar','policy-unavailable'}:
        checks['no_project_changes']=changes==[]
        checks['no_questions']=not qtools and not batches
        needles={'unknown-brn':['BRN-009','BRN-001','BRN-002'], 'malformed-brn':['BRN-002','ideas'],
                 'policy-sv01':['POL-001','SET-01','SV-01'],'policy-sv02':['POL-001','POL-002','SV-02'],
                 'policy-calendar':['POL-001','updated','schema'],
                 'policy-unavailable':['jsonschema is not installed']}[name]
        for word in needles:checks['report_'+word]=word.lower() in final.lower()
        if name=='policy-calendar':checks['calendar_not_called_schema']=not bool(re.search(r'(?is)schema.{0,70}(?:invalid|impossible).{0,30}date',final))
        if name=='policy-unavailable':checks['validator_exit_2']=any('validate_policy.py' in i.get('command','') and i.get('exitCode')==2 for i in commands)
    elif name=='policy-sv06':
        checks.update(prd_exists=prd.is_file(),draft_policy_ignored='ignored docs/specs/policy/POL-001.md (status draft)' in final,
                      defaults_reported='interview.max_calls=8 (default)' in final,no_questions=not qtools and not batches)
    elif name in {'failed-supersession','accepted-decision-failure'}:
        arch=workspace/'docs/specs/arch/ARCH-001.md';text=arch.read_text();af=frontmatter(text)
        ab=(a/'before-workspace/docs/specs/arch/ARCH-001.md').read_text();ai=item_blocks(text);abi=item_blocks(ab)
        checks.update(arch_in_review=af.get('status')=='in-review',arch_approval_cleared=af.get('approved_by')=='' and af.get('approved_on') is None,
                      existing_cmp_unchanged=ai['CMP-01']['raw']==abi['CMP-01']['raw'],
                      failure_names_cmp='CMP-01' in final and 'fail' in final.lower(),
                      no_readiness_handoff='$devforgeai:epic' not in final and not bool(re.search(r'(?i)readiness\s*:\s*(?:pass|validated)',final)))
        original_adrs={p.name for p in (a/'before-workspace/docs/specs/adr').glob('*.md')} if (a/'before-workspace/docs/specs/adr').exists() else set()
        newadrs=[p for p in (workspace/'docs/specs/adr').glob('*.md') if p.name not in original_adrs]
        checks['replacement_written']=len(newadrs)==1
        if len(newadrs)==1:
            adr=newadrs[0];dt=adr.read_text();df=frontmatter(dt)
            checks.update(new_adr_proposed=df.get('status')=='proposed',new_approval_cleared=df.get('approved_by')=='' and df.get('approved_on') is None,
                          rollback_history='Restored to proposed' in dt)
            if name=='failed-supersession':
                checks.update(old_adr_exact=(workspace/'docs/specs/adr/ADR-001.md').read_bytes()==(a/'before-workspace/docs/specs/adr/ADR-001.md').read_bytes(),
                              supersedes_cleared=df.get('supersedes')==[],decision_open=ai['DEC-01']['data'].get('state')=='open' and ai['DEC-01']['data'].get('resolved_by')==[],
                              intended_supersession_retained='ADR-001' in dt.split('## Decision outcome',1)[-1].split('## Status history')[0] and 'not in force' in dt,
                              transition_exercised=any(i.get('exitCode')==0 and 'ADR-002 accepted, ADR-001 superseded' in (i.get('aggregatedOutput') or '') for i in commands))
                coverage['transition_evidence']=[i['id'] for i in commands if i.get('exitCode')==0 and 'ADR-002 accepted, ADR-001 superseded' in (i.get('aggregatedOutput') or '')]
            else:
                checks['dependent_decisions_reopened']=all(v['data'].get('state')=='open' and v['data'].get('resolved_by')==[] for v in ai.values() if v['group']=='decisions')
        notes.append('ERR-05 rollback is assessed separately from exact runtime model identity and full validation success. A preserved older ADR alone is insufficient without an observed supersession transition.')
    else:
        coverage['specialized_assessment']='REVIEW_REQUIRED: inspect the extension/shared-constraint output and history against before-image'
    review=a/'review.json'
    if review.exists():
        r=json.loads(review.read_text());assert r['raw_sha256']==sha(a/'protocol.jsonl')
        checks.update(r.get('checks',{}));notes.extend(r.get('notes',[]))
        coverage.update(r.get('coverage',{}))
    assessment={'scenario':name,'obligations':binding['scenario']['obligations'],'raw_sha256':sha(a/'protocol.jsonl'),
      'workspace_files':after,'checks':checks,'mechanical_status':'PASS' if all(checks.values()) else 'FAIL',
      'changed_paths':changes,'question_batches':len(batches)+len(qtools),'native_question_calls':len(qtools),
      'max_questions_in_batch':max(maxnative,maxtext),'identities':identities,
      'exact_identity_open':any(not x['exact_model'] or not x['exact_session'] for x in identities),'coverage':coverage,'notes':notes}
    (a/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');return assessment

def main(e):
    plan=json.loads((e/'manual/plan.json').read_text());rows=[]
    for s in plan['scenarios']:
        a=e/'manual/attempts'/s['name']
        if (a/'result.json').is_file():rows.append(assess(a))
        else:rows.append({'scenario':s['name'],'obligations':s['obligations'],'mechanical_status':'NOT_RUN'})
    out={'scenarios':rows,'review_boundary':'Independent artifact/protocol checks by root evaluator; these are not owner acceptance. Specialized semantic coverage may remain REVIEW_REQUIRED.'}
    (e/'manual/assessments.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{k:r.get(k) for k in ['scenario','mechanical_status','question_batches','exact_identity_open','coverage']} for r in rows],indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('evidence',type=Path);a=p.parse_args();main(a.evidence.resolve())
