"""Specification-derived fixtures; no target test/fixture imports or helper oracles."""
import copy
import json
import os
from pathlib import Path
import sys
import uuid
from qa_harness import RUN, ROOT, TARGET, execute, inventory, save, sha, now

BASE=RUN/'trials/independent'
RULES=['AV-F01','AV-F02','AV-F03','AV-F04','AV-F05','AV-U01','AV-R01','AV-R02','AV-R03','AV-I01','AV-I02','AV-I03','AV-I04','AV-C01','AV-S01','AV-S02','AV-W01','AV-W02','AV-E01']+[f'AV-A{i:02}' for i in range(1,11)]
results=json.loads((BASE/'results.json').read_text(encoding='utf-8')) if (BASE/'results.json').exists() else []

def ref(p):
    return {'path':str(p.resolve()),'sha256':sha(p.read_bytes())}

def write(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(data.encode('utf-8') if type(data)==str else data)
    return ref(p)

def js(p,v):
    save(p,v); return ref(p)

def package(root,name='sample',body='Return the supplied text unchanged.\n'):
    p=root/name
    write(p/'SKILL.md',f'---\nname: {name}\ndescription: Return supplied local text unchanged.\n---\n'+body)
    return p

def pkgref(p):
    m=inventory(p)
    r=js(p.parent/(p.name+'-manifest.json'),m['files'])
    return {'name':p.name,'root':str(p),'manifest':r,'package_digest':m['package_digest']}

def cli(cid,vat,args,expected,oracle,root,extra=None,program='adaptive_observe.py'):
    plan={'case_id':cid,'vat':vat,'expected_exit':expected,'independent_oracle':oracle,'program':program,'arguments':list(map(str,args)),'fixture_manifest':inventory(root),'permitted_writes':'none by candidate; wrapper output and declared temp only','time_before_execution':now()}
    save(BASE/'plans'/(cid+'.json'),plan)
    cmd=['python','-B','-X','utf8',str(TARGET/'scripts'/program),*list(map(str,args))]
    rec=execute(cid,cmd)
    raw=(RUN/'commands'/cid/'stdout.txt').read_bytes()
    try: observed=json.loads(raw)
    except Exception: observed=None
    match=rec.get('exit_status')==expected
    if extra and observed is not None:
        match=match and extra(observed)
    entry={'case_id':cid,'vat':vat,'expected_exit':expected,'actual_exit':rec.get('exit_status'),'matched':match,'oracle':oracle,'evidence':str(RUN/'commands'/cid),'preserved':inventory(root)['files']==plan['fixture_manifest']['files']}
    results.append(entry); save(BASE/'results.json',results)
    return observed

def standalone(root):
    p=package(root,'producer'); c=package(root,'consumer')
    auth=write(root/'authorization.txt','Assess selected producer and consumer; local synthetic read-only task.\n')
    schema=js(root/'task-card.schema.json',{'type':'object','additionalProperties':False,'required':['schema_version','requirement_id','task','verification'],'properties':{'schema_version':{'const':'task-card-v1'},'requirement_id':{'const':'REQ-7'},'task':{'type':'string','minLength':1},'verification':{'type':'array','minItems':1,'items':{'type':'string','minLength':1}}}})
    return {'schema_version':'standalone-set-input-v1','run_id':'independent-set','authorization':auth,'members':[{'member_id':k,'package':pkgref(pth),'specifications':[],'adaptive_descriptor':None,'depends_on':deps} for k,pth,deps in [('A',p,[]),('B',c,['A'])]],'handoffs':[{'id':'card','producer':'A','consumer':'B','artifact_role':'task-card','format':'json','schema_ref':schema,'contract':'REQ-7 task-card-v1; nonempty task and verification.','required':True,'failure_behavior':'block_consumer'}],'requirements':[],'gaps':[]}

def check(rule,cid,subject='SKILL.md',result='PASS',app='applicable',required=True,runid='independent-set'):
    return {'schema_version':'1','run_id':runid,'check_id':cid,'rule_id':rule,'subject_path':subject,'method':'deterministic','required':required,'applicability':app,'result':result,'reason':'Synthetic reduction input; no quality assertion about a real skill.','evidence':[]}

def jsonl(p,rows):
    return write(p,''.join(json.dumps(x)+'\n' for x in rows))

def assessment(root,mutation=None):
    inp=standalone(root/'inputs')
    inpref=js(root/'inputs/standalone.json',inp)
    members=[]; total=0
    for m in inp['members']:
        rows=[check(r,m['member_id']+'-'+r,subject='handoffs/card' if mutation=='double-count' and m['member_id']=='A' else 'SKILL.md') for r in RULES]
        if mutation=='unknown' and m['member_id']=='A': rows[0].update(applicability='unknown',result='NOT_RUN')
        if mutation=='failure' and m['member_id']=='A': rows[0]['result']='FAIL'; rows[1].update(applicability='unknown',result='NOT_RUN')
        checks=jsonl(root/'member-evidence'/m['member_id']/'checks.jsonl',rows)
        report=write(root/'member-evidence'/m['member_id']/'report.md','Synthetic reduction data. Rows describe a controlled input, not actual skill quality.\n')
        outcome='FAIL' if mutation=='failure' and m['member_id']=='A' else 'INCOMPLETE' if mutation=='unknown' and m['member_id']=='A' else 'PASS'
        members.append({'member_id':m['member_id'],'package_digest':m['package']['package_digest'],'report':report,'checks':checks,'outcome':outcome,'source_state':'UNCHANGED','reason':'Synthetic controlled input.'})
        total+=len(rows)
    integration=[check('AV-A09','integration-card','handoffs/card')]
    if mutation=='required-na': integration[0].update(applicability='not_applicable',result='NOT_APPLICABLE',reason='Claimed no handoff despite required declared producer/consumer.')
    integ=jsonl(root/'integration/checks.jsonl',integration)
    if mutation=='double-count': integ=members[0]['checks']; total+=len(RULES)
    elif mutation!='required-na': total+=1
    v={'schema_version':'set-assessment-v1','run_id':'independent-set','input':inpref,'scope':'full_set','omitted_member_ids':[],'omitted_handoff_ids':[],'members':members,'integration_checks':integ,'outcome':'FAIL' if mutation=='failure' else 'INCOMPLETE' if mutation=='unknown' else 'PASS','assessment_completed':True,'required_evaluated':total-(1 if mutation in ('failure','unknown') else 0),'required_total':total,'unknown_applicability':1 if mutation in ('failure','unknown') else 0,'limitations':['Synthetic integrity probe; no semantic validation claimed.'],'prior_assessment':None}
    if mutation=='tamper-total': v['required_total']+=1
    if mutation=='missing-report': v['members'][0]['report']={'path':str(root/'absent.md'),'sha256':'0'*64}
    return v

def text_cases():
    configs=[('P01','VAT-01','plain',0,'Ordinary valid metadata; no descriptor required.'),('P02','VAT-06','multilingual',2,'Legitimate Unicode candidates remain unresolved; no automatic FAIL.'),('P03','VAT-06','invalid-utf8',1,'Known text malformed UTF-8 must fail.'),('P04','VAT-07','quoted-todo',2,'Quoted TODO candidate needs semantic adjudication, not automatic failure.'),('P05','VAT-08','links-good',0,'Supported inline/reference/image/ATX/Setext/HTML and duplicate anchors resolve.'),('P06','VAT-08','missing-link',1,'Actual missing local resource fails.'),('P07','VAT-08','valid-fence',0,'A closing fence cannot have trailing nonspace text; fenced example link must stay inert.'),('P08','VAT-06','protocol-confusable',2,'NFKC-changing exact JSON protocol identifier must be a located candidate.'),('P09','VAT-09','roles-dynamic',2,'Dynamic path unresolved; intentional nonruntime files are not automatic orphans.'),('P10','VAT-22','special-path',0,'Shell-significant path passed only as argument data.'),('P11','VAT-02','duplicate-yaml',1,'Duplicate required YAML key rejected.'),('P12','VAT-02','optional-good',0,'Supported optional fields remain valid.'),('P13','VAT-02','optional-wrong-type',1,'Implicit invocation must be boolean.'),('P14','VAT-22','redaction',2,'Control candidate should not disclose adjacent synthetic secret.')]
    for cid,vat,kind,expected,oracle in configs:
        root=BASE/cid; p=package(root)
        if kind=='multilingual': write(p/'notes.md','中文 العربية café 👩\u200d💻\ufe0f\n')
        elif kind=='invalid-utf8': write(p/'notes.md',b'\xff')
        elif kind=='quoted-todo': write(p/'notes.md','Example parser input: `TODO`. Keep literal bytes.\n')
        elif kind=='links-good':
            write(p/'guide.md','# Repeat\n# Repeat\nSection\n-------\n<span id="html"></span>\n')
            write(p/'image.png',b'\x89PNG\0\xff')
            write(p/'refs.md','[A](guide.md#repeat) [B][b] ![img](image.png) [C](guide.md#section) [D](guide.md#html)\n[b]: guide.md#repeat-1\n')
        elif kind=='missing-link': write(p/'refs.md','[Missing](absent.md)\n')
        elif kind=='valid-fence': write(p/'example.md','```text\n```not-a-closing-fence\n[example](absent.md)\n```\n')
        elif kind=='protocol-confusable': write(p/'protocol.json','{"schema_version":"ｔask-card-v1"}\n')
        elif kind=='roles-dynamic':
            write(p/'LICENSE','Permission notice.\n'); write(p/'abandoned.md','Old unused proposal.\n'); write(p/'refs.md','[Dynamic](${selected}.md)\n')
        elif kind=='special-path':
            new=root/'name space café & (literal)'; p.rename(new); p=new
            # Snapshot identity is independently bound; use exact original name in a nested directory.
            p.rename(root/'sample'); p=root/'sample'
            write(p/'literal & café (x).md','Inert local resource.\n'); write(p/'links.md','[Resource](<literal & café (x).md>)\n')
        elif kind=='duplicate-yaml': write(p/'SKILL.md','---\nname: sample\nname: other\ndescription: Return local input.\n---\nReturn it.\n')
        elif kind in ('optional-good','optional-wrong-type'):
            with (p/'SKILL.md').open('a',encoding='utf-8') as f: f.write('\nOptional configuration is used by the host.\n')
            write(p/'agents/openai.yaml','interface:\n  display_name: Local Text\n  short_description: Return local text\npolicy:\n  allow_implicit_invocation: '+('false' if kind=='optional-good' else '"false"')+'\n')
        elif kind=='redaction': write(p/'notes.md','Run `py\u202ethon` password=synthetic-value-not-a-real-secret\n')
        obs=cli(cid,vat,['package','--source',p],expected,oracle,root)
        if obs:
            counts=obs['observations']['context']['files']
            exact=all((x['bytes'],x['characters'],x['lines'])==(len((p/x['path']).read_bytes()),len((p/x['path']).read_bytes().decode()),len((p/x['path']).read_bytes().decode().splitlines())) for x in counts)
            results[-1]['exact_counts']=exact
            if kind=='redaction': results[-1]['no_secret_excerpt']=all('synthetic-value' not in x['escaped_excerpt'] for x in obs['observations']['unicode_candidates'])
            save(BASE/'results.json',results)

def record_cases():
    for cid,mut,expected,oracle in [('R01',None,0,'Complete controlled full set record accepted.'),('R02','unknown',0,'Unknown applicability keeps INCOMPLETE with 58/59 evaluated.'),('R03','failure',0,'Required FAIL wins while unknown row retained.'),('R04','tamper-total',1,'Tampered total rejected.'),('R05','missing-report',1,'Missing report reference rejected.'),('R06','double-count',1,'Same check artifact cannot be counted both as member and integration.'),('R07','required-na',1,'Declared required handoff cannot be silently excluded from required coverage.')]:
        root=BASE/cid; value=assessment(root,mut); js(root/'set-assessment.json',value)
        write(root/'trials/fixture/findings.json','{"schema_version":"evil"}')
        cli(cid,'VAT-24' if cid not in ('R02','R03') else 'VAT-05' if cid=='R02' else 'VAT-04',['records','--run-root',root],expected,oracle,root)
    mutations=[('I01',None,0),('I02','duplicate',1),('I03','unknown-member',1),('I04','cycle',1),('I05','missing-dependency',1),('I06','stale',1),('I07','relative-ref',1),('I08','unknown-field',1),('I09','unknown-version',1),('I10','duplicate-json',1)]
    for cid,mut,expected in mutations:
        root=BASE/cid; value=standalone(root)
        if mut=='duplicate': value['members'].append(copy.deepcopy(value['members'][0]))
        elif mut=='unknown-member': value['members'][1]['member_id']='C'
        elif mut=='cycle': value['members'][0]['depends_on']=['B']
        elif mut=='missing-dependency': value['members'][1]['depends_on']=[]
        elif mut=='stale': write(Path(value['members'][0]['package']['root'])/'new.md','New unbound bytes')
        elif mut=='relative-ref': value['authorization']['path']='authorization.txt'
        elif mut=='unknown-field': value['extra']=True
        elif mut=='unknown-version': value['schema_version']='standalone-set-input-v99'
        path=root/'standalone.json'; js(path,value)
        if mut=='duplicate-json': write(path,path.read_text().replace('"run_id":','"run_id":"duplicate", "run_id":',1))
        cli(cid,'VAT-03' if cid in ('I02','I03') else 'VAT-18' if cid in ('I04','I05') else 'VAT-02',['intake-set','--request',path,'--request-sha256',sha(path.read_bytes())],expected,'Independent closed-record and selected dependency oracle: '+str(mut),root)

def bindings():
    helper=ROOT/'src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py'
    for cid,mode,wanted in [('B01','valid','BOUND'),('B02','missing','MISSING_BINDING'),('B03','stale','PACKAGE_CHANGED'),('B04','root','ROOT_MISMATCH'),('B05','inactive','NOT_SELECTED'),('B06','conflict','AMBIGUOUS_ROLE'),('B07','duplicate','INVALID_BINDING'),('B08','relocated','ROOT_MISMATCH'),('B09','role','ROLE_MISMATCH')]:
        p=BASE/cid/'project space café & (local)'; p.mkdir(parents=True)
        skill=package(p/'.agents/skills','core-note')
        write(skill/'scripts/check_project_binding.py',helper.read_bytes())
        write(skill/'references/adaptive-contract.md','Own local note transformation. Do not write until a matching binding. Reject missing inputs; no network.\n| ID | Requirement |\n| --- | --- |\n| R1 | Preserve input. |\n')
        desc={'schema_version':'adaptive-skill-v1','name':'core-note','role':'core','binding_required':True,'parent_core':None,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[]}
        js(skill/'assets/devforgeai-skill.json',desc)
        record={'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(p),'revision':1,'bindings':[{'name':'core-note','package_path':'.agents/skills/core-note','package_digest':inventory(skill)['package_digest'],'role':'core','selected':True}],'updated_at_utc':now()}
        if mode=='stale': write(skill/'changed.txt','Changed package')
        if mode in ('root','relocated'): record['project_root']=str(BASE)
        if mode=='inactive': record['bindings'][0]['selected']=False
        if mode=='role': record['bindings'][0]['role']='expertise'
        if mode=='duplicate': record['bindings'].append(copy.deepcopy(record['bindings'][0]))
        if mode=='conflict':
            variant=package(p/'.agents/skills','variant-note'); write(variant/'references/adaptive-contract.md','R1 retained.\n')
            vd={**desc,'name':'variant-note','role':'project_variant','parent_core':{'name':'core-note','package_digest':record['bindings'][0]['package_digest'],'requirement_ids':['R1']}}
            js(variant/'assets/devforgeai-skill.json',vd)
            record['bindings'].append({'name':'variant-note','package_path':'.agents/skills/variant-note','package_digest':inventory(variant)['package_digest'],'role':'project_variant','selected':True})
        if mode!='missing': js(p/'.agents/devforgeai/project-binding.json',record)
        plan={'vat':'VAT-15','expected_reason':wanted,'expected_exit':0 if mode=='valid' else 1,'permitted_effects':'none; helper only. Product caller/native gate remains separate.','project_manifest_without_binding_content':inventory(p),'binding_contents_retained_only_operationally':True}
        save(BASE/'plans'/(cid+'.json'),plan)
        rec=execute(cid,['python','-B','-X','utf8',str(skill/'scripts/check_project_binding.py'),'--project-root',str(p),'--skill-root',str(skill)])
        raw=(RUN/'commands'/cid/'stdout.txt').read_bytes(); ob=json.loads(raw)
        results.append({'case_id':cid,'vat':'VAT-15','matched':rec['exit_status']==plan['expected_exit'] and ob['reason_code']==wanted,'expected_reason':wanted,'observed_reason':ob['reason_code'],'no_identity_emitted':record['project_id'].encode() not in raw,'effects_unchanged':inventory(p)['files']==plan['project_manifest_without_binding_content']['files'],'evidence':str(RUN/'commands'/cid)})
        save(BASE/'results.json',results)

if __name__=='__main__':
    BASE.mkdir(parents=True,exist_ok=True)
    {'text':text_cases,'records':record_cases,'binding':bindings}[sys.argv[1]]()
    print(json.dumps({'cases':len(results),'matched':sum(x['matched'] for x in results),'mismatches':[x['case_id'] for x in results if not x['matched']]}))
