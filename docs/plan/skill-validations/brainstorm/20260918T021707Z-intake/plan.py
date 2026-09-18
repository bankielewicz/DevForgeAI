"""Freeze rule applicability and independent scenario expectations before checks."""
from prepare import *
import re

def ref(path):
    path=Path(path)
    return {'path':path.relative_to(RUN).as_posix(),'sha256':observe.sha256(path.read_bytes())}

def main():
    bindings=json.loads((RUN/'inputs/input-bindings.json').read_bytes())
    sources=[]
    for i,row in enumerate(bindings):
        sources.append(dict(source_id='input-'+str(i),original_path=row['original_path'],retrieved_at_utc=None,sha256=row['sha256'],snapshot_path=row['snapshot_path'],sections=['Selected contract'],freshness='local_verified'))
    for source_id,path,sections,url in [
        ('openai','inputs/openai-build-skills.md',['Create a skill','Optional metadata','Best practices'],'https://learn.chatgpt.com/docs/build-skills'),
        ('av','inputs/validator/references/adaptive-validation.md',['3.1 Core rule catalog','4.1 Adaptive rules'],None),
        ('text','inputs/validator/references/text-resource-checks.md',['3.2 Unicode, placeholders, and resource parsing','3.3 Semantic anti-slop rubric'],None),
        ('fallback','inputs/validator/assets/rules-snapshot.json',['Dated summarized rules'],None)]:
        s=dict(source_id=source_id,retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sha256=ref(RUN/path)['sha256'],snapshot_path=path,sections=sections,freshness='live_verified' if url else 'snapshot_only')
        s['url' if url else 'original_path']=url or str(VAL/path.replace('inputs/validator/',''))
        sources.append(s)
    base=dict(schema_version='1',run_id=RUN.name,target_name='brainstorm')
    save(RUN/'sources.json',dict(base,sources=sources))
    rules=[]
    def rule(ident,title,source_id,locator,method='semantic',app='applicable',limitation=''):
        source=next(s for s in sources if s['source_id']==source_id)
        rules.append(dict(rule_id=ident,revision='20260918.1',title=title,source_refs=[dict(path=source['snapshot_path'],sha256=source['sha256'],source_id=source_id,locator=locator)],authority_class='project_policy',applicability=app,method=method,expected_observation=title,required=True,limitation=limitation))
    av=(RUN/'inputs/validator/references/adaptive-validation.md').read_text(encoding='utf-8')
    for line in av.splitlines():
        if re.match(r'\| AV-[A-Z]\d\d \|',line):
            cells=[c.strip() for c in line.split('|')[1:-1]]
            adaptive=cells[0].startswith('AV-A')
            rule(cells[0],cells[-1],'av','4.1 Adaptive rules' if adaptive else '3.1 Core rule catalog',app='not_applicable' if adaptive else 'applicable',limitation='BR-002 selects an ordinary standalone skill; no adaptive descriptor, binding, parent or set.' if adaptive else '')
    spec=RUN/bindings[0]['snapshot_path']
    text=spec.read_text(encoding='utf-8')
    for ident,title in re.findall(r'\*\*(BR-\d+) — (.*?)\.\*\*',text):
        rule(ident,title,'input-0',ident)
    inventory=[]
    subcases={'BV-04':['implementation','repair','activation','prd-review','stories'],'BV-15':['collision','reparse-escape','write-denial'],'BV-16':['python-policy','typescript-policy'],'BV-19':['essential-missing','optional-research-missing']}
    for line in text.splitlines():
        if re.match(r'\| BV-\d\d \|',line):
            case,req,expected=[c.strip() for c in line.split('|')[1:-1]]
            inventory.append(dict(case_id=case,requirements=re.findall(r'BR-\d+',req),expected=expected,subcases=subcases.get(case,['main']),required=True,platform='Windows/PowerShell',result='NOT_RUN',reason='Predeclared; execution pending'))
            rule(case,expected,'input-0','6. Required acceptance scenarios','behavioral')
    for ident,title in [('ROUTING','Description-only positive and near-miss classification'),('NATIVE-EXPLICIT','Native explicit selection and completed workflow'),('NATIVE-IMPLICIT','Native natural-language discovery with observed selection'),('EVAL-BUNDLE','Bound runner, graders, fixtures, expected results, schema and runtime information')]:
        rule(ident,title,'input-0','7. Authoring, evaluation and delivery boundary','behavioral' if ident.startswith('NATIVE') else 'deterministic')
    save(RUN/'rule-set.json',dict(base,rules=rules))
    save(RUN/'inputs/case-inventory.json',inventory)
    save(RUN/'inputs/evaluation-policy.json',dict(required_parent_cases=20,all_mandatory=True,subcase_count=sum(len(x['subcases']) for x in inventory),required_platforms=['Windows/PowerShell'],required_case_floor=95,mandatory_failure_veto=True,package_executable_denominator=0,package_coverage='NOT_APPLICABLE',evaluator_coverage='Separate evidence utility; not framework executable code.',native_timeout_seconds=600,utility_timeout_seconds=120,retries='No automatic retry; retain every attempt and diagnose first.',source_mutation='Forbidden',root_scope=str(RUN)))
    prompts=[
        'Help me explore ways to make library returns easier for volunteers.',
        'Compare directions for an uncertain offline field-note product.',
        'Resume the selected discovery brief and revisit its open audience question.',
        'Our existing billing app needs a new feature but the intended outcome is unclear. Help clarify it.',
        'Implement the selected approved specification.',
        'Repair the known signed-sum defect using its regression case.',
        'Register and activate this project.',
        'Write the PRD from these settled discovery inputs.',
        'Review this PRD for contradictions.',
        'Create implementation stories for the selected epic.'
    ]
    save(RUN/'inputs/routing-prompts.json',[dict(id=f'R{i+1:02}',prompt=p) for i,p in enumerate(prompts)])
    save(RUN/'inputs/routing-expected.json',[dict(id=f'R{i+1:02}',activate=i<4) for i in range(len(prompts))])
    # Native pilots have different output paths and independent prerequisites.
    for ident,saving in [('N01',True),('N02',False)]:
        case_root=RUN/'trials'/ident
        project=case_root/'project'
        project.mkdir(parents=True)
        shutil.copytree(RUN/'source',project/'.agents/skills/brainstorm')
        (project/'.trial-output').mkdir()
        save(project/'AGENTS.md',b'# Synthetic discovery project\nOnly this synthetic directory is selected. Product files and operational configuration are not selected for changes. No network research or external actions.\n')
        if saving:
            task='Use $brainstorm. I coordinate a volunteer lending library. Volunteers lose track of returns. Audience: volunteer desk staff. Desired outcome: each returned item can be found in a daily reconciliation list. I selected a simple daily checklist over automated notifications; notifications and payments are excluded. We need offline use on one shared device. Database choice belongs to later PRD design. This directory is the selected project. Save one discovery brief using your default location and then tell me what comes next. No research is needed. These are my decisions; do not seek them again.'
            covered=['BV-01','BV-05','BV-10','BV-12','BV-18']
        else:
            task='Use $brainstorm. I am exploring a tool for volunteers, but I have not chosen which problem or outcome to pursue and decline to decide that today. Keep this conversation-only; I have not selected a project root or any saved output. Give me useful partial exploration and the current disposition. No external research.'
            covered=['BV-06','BV-13']
        save(case_root/'prompt.txt',task.encode())
        protected=[]
        for rel,path,info in observe.inventory(project)[0]:
            protected.append(dict(path=str(path),sha256=observe.sha256(path.read_bytes())))
        protected.append(dict(path=str(spec),sha256=observe.sha256(spec.read_bytes())))
        plan=dict(schema_version='trial-plan-v1',case_id=ident,kind='native',argv=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--ephemeral','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-'],cwd=str(project),permitted_write_root=str(project),inputs=protected,prompt=dict(path=str(case_root/'prompt.txt'),sha256=observe.sha256((case_root/'prompt.txt').read_bytes())),requirement_ids=covered,dependencies=[],timeout_seconds=600,expected_outputs=[dict(path='.trial-output/final.txt',kind='manual',requirement_id=x) for x in covered])
        save(case_root/'plan.json',plan)
        save(case_root/'expectations.json',dict(case_ids=covered,criteria=[row for row in inventory if row['case_id'] in covered],permitted_new_paths=['.trial-output/final.txt']+(['docs/plan/discovery/**'] if saving else []),protected_inputs='All plan input files unchanged',semantic_grading='Independent content review after native completion; existence and keywords alone cannot pass a case.'))
    print('Frozen',len(rules),'rules;',len(inventory),'mandatory cases;',sum(len(x['subcases']) for x in inventory),'subcases')

if __name__=='__main__':
    main()
