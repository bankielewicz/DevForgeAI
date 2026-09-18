"""Separate maintenance oracles, fixed before terminal candidates execute.

Writes only this run's synthetic fixtures/results. Never changes a real binding.
"""
import copy
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from capture import ROOT, RUN, scan
sys.path.insert(0,str(ROOT/'src/agents/skills/skill-validator/tests'))
import adaptive_fixtures as fixture

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2)

def command(folder,argv):
    folder.mkdir(parents=True,exist_ok=False)
    save(folder/'plan.json',{'argv':argv,'timeout_seconds':120,'start':dt.datetime.now(dt.timezone.utc).isoformat()})
    result = subprocess.run(argv,capture_output=True,timeout=120)
    (folder/'stdout.txt').write_bytes(result.stdout)
    (folder/'stderr.txt').write_bytes(result.stderr)
    save(folder/'result.json',{'exit_code':result.returncode,'end':dt.datetime.now(dt.timezone.utc).isoformat()})
    return result

def golden():
    root = RUN/'golden-contracts'
    root.mkdir()
    request = fixture.shared(root/'inputs')
    path = root/'set-validation-request.json'
    fixture.write(path,request)
    cases = [('valid',0,request),('extra-key',1,{**request,'extra':True}),('unknown-version',1,{**request,'schema_version':'set-validation-request-v2'}),('missing-member',1,{**request,'members':request['members'][:1]}),('duplicate-member',1,{**request,'members':request['members']+[request['members'][0]]}),('malformed-id',1,{**request,'run_id':'not/an/id'}),('bad-digest',1,{**request,'selection':{**request['selection'],'sha256':'0'*64}})]
    save(root/'expectations.json',[{'case_id':name,'expected_exit':expected,'basis':'Closed frozen shared contract.'} for name,expected,value in cases])
    results = []
    for name,expected,value in cases:
        case = root/(name+'.json')
        fixture.write(case,value)
        a = command(root/'results'/name/'builder',[sys.executable,'-B','-X','utf8',str(ROOT/'src/agents/skills/skill-builder/scripts/adaptive.py'),'inspect','--record',str(case)])
        b = command(root/'results'/name/'validator',[sys.executable,'-B','-X','utf8',str(ROOT/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'),'intake-set','--request',str(case),'--request-sha256',hashlib.sha256(case.read_bytes()).hexdigest()])
        results.append({'case_id':name,'expected_exit':expected,'builder_exit':a.returncode,'validator_exit':b.returncode,'agreement':a.returncode==b.returncode==expected})
    save(root/'results.json',results)
    print(json.dumps(results))

def binding(host):
    root = RUN/('binding-'+host)
    root.mkdir()
    scenarios = [('valid','BOUND'),('missing','MISSING_BINDING'),('stale','PACKAGE_CHANGED'),('wrong-root','ROOT_MISMATCH'),('inactive','NOT_SELECTED'),('conflict','AMBIGUOUS_ROLE'),('duplicate','INVALID_BINDING'),('relocated','UNBOUND_SKILL'),('unknown-version','INVALID_BINDING')]
    save(root/'expectations.json',[{'case_id':name,'expected_reason':expected,'product_effects':[] if name!='valid' else ['out/product.txt'],'host':host} for name,expected in scenarios])
    helper = ROOT/'src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py'
    if not helper.exists():
        save(root/'not-run.json',{'status':'NOT_RUN','reason':'Read-only companion binding template unavailable.'})
        return
    results = []
    for name,expected in scenarios:
        project = root/name/'space é & (shell)'
        skill = project/'.agents/skills/core-skill'
        (skill/'assets').mkdir(parents=True)
        (skill/'references').mkdir()
        (skill/'scripts').mkdir()
        shutil.copyfile(helper,skill/'scripts/check_project_binding.py')
        (skill/'SKILL.md').write_text('---\nname: core-skill\ndescription: Produce the selected local fixture outcome.\n---\nCheck the local binding before product writes. On non-MATCH report its reason and stop.\n',encoding='utf-8')
        (skill/'references/adaptive-contract.md').write_text('R1: Preserve current input.\n',encoding='utf-8')
        desc = {'schema_version':'adaptive-skill-v1','name':'core-skill','role':'core','binding_required':True,'parent_core':None,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[{'path':'scripts/check_project_binding.py','role':'runtime','reason':'Check local binding before effects.'}]}
        fixture.write(skill/'assets/devforgeai-skill.json',desc)
        binding_row = {'name':'core-skill','package_path':'.agents/skills/core-skill','package_digest':scan(skill)['package_digest'],'role':'core','selected':True}
        # The concrete value is created only here and written only operationally.
        record = {'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(project.resolve()),'revision':1,'bindings':[binding_row],'updated_at_utc':dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')}
        if name=='stale':
            (skill/'added.txt').write_text('changed bytes')
        elif name=='wrong-root':
            record['project_root'] = str(root.resolve())
        elif name=='inactive':
            binding_row['selected'] = False
        elif name=='duplicate':
            record['bindings'].append(copy.deepcopy(binding_row))
        elif name=='unknown-version':
            record['schema_version'] = 'project-binding-v9'
        elif name=='conflict':
            variant = project/'.agents/skills/variant-skill'
            shutil.copytree(skill,variant)
            (variant/'SKILL.md').write_text((variant/'SKILL.md').read_text().replace('name: core-skill','name: variant-skill'))
            variant_desc = {**desc,'name':'variant-skill','role':'project_variant','parent_core':{'name':'core-skill','package_digest':binding_row['package_digest'],'requirement_ids':['R1']}}
            fixture.write(variant/'assets/devforgeai-skill.json',variant_desc)
            record['bindings'].append({'name':'variant-skill','package_path':'.agents/skills/variant-skill','package_digest':scan(variant)['package_digest'],'role':'project_variant','selected':True})
        if name!='missing':
            fixture.write(project/'.agents/devforgeai/project-binding.json',record)
        if name=='relocated':
            moved = project/'development/core-skill'
            shutil.copytree(skill,moved)
            skill = moved
        before = scan(project)
        argv = [sys.executable,'-B','-X','utf8',str(skill/'scripts/check_project_binding.py'),'--project-root',str(project),'--skill-root',str(skill)]
        result = command(root/'results'/name,argv)
        observation = json.loads(result.stdout)
        leaked = record['project_id'].encode() in result.stdout+result.stderr
        if observation['status']=='MATCH':
            (project/'out').mkdir()
            (project/'out/product.txt').write_text('Synthetic terminal workflow completed.')
        after = scan(project)
        changed = {x['path'] for x in after['files']} - {x['path'] for x in before['files']}
        good = observation['reason_code']==expected and not leaked and changed == ({'out/product.txt'} if name=='valid' else set())
        save(root/'results'/name/'effects.json',{'before':before,'after':after,'changed':sorted(changed),'identity_leaked':leaked,'oracle_match':good,'category':'terminal helper plus synthetic caller, not native skill selection'})
        results.append({'case_id':name,'expected_reason':expected,'observed_reason':observation['reason_code'],'oracle_match':good})
    save(root/'results.json',results)
    print(json.dumps(results))

def projects():
    root = RUN/'project-fixtures'
    root.mkdir()
    fixtures = {
      'python-tdd':{'AGENTS.md':'Require a failing regression before implementation. Use Python and pytest.','pyproject.toml':'[project]\nname="health-service"\nversion="0.1.0"\n[tool.pytest.ini_options]\ntestpaths=["tests"]\n','src/service.py':'def health():\n    return {"status": "ok"}\n'},
      'rust-implementation-first':{'AGENTS.md':'Implementation may precede regression; use the local library Cargo scope.','Cargo.toml':'[package]\nname="health-service"\nversion="0.1.0"\nedition="2021"\n[lib]\npath="src/lib.rs"\n','src/lib.rs':'pub fn health_status() -> &\'static str { "ok" }\n'},
      'typescript-monorepo':{'AGENTS.md':'packages/service owns the health route; preserve separate package ownership and service-local test command.','package.json':'{"private":true,"workspaces":["packages/*"]}','packages/service/package.json':'{"name":"health-service","scripts":{"test":"node --test"}}'},
      'documentation-only':{'AGENTS.md':'Documentation edits only; no application-code edits.','docs/api.md':'Document HTTP 200 and JSON status ok.'}}
    expected = {'python-tdd':'Python/pytest; failing regression before implementation','rust-implementation-first':'Rust/Cargo; implementation-first permitted','typescript-monorepo':'packages/service scope; local node --test; no root test command','documentation-only':'Documentation only; no compiler/build requirement','ambiguous':'Conflicting equal-scope development conventions unresolved'}
    save(root/'expectations.json',expected)
    for name,files in fixtures.items():
        files['docs/requirements.md'] = 'REQ-7: Document the health-response contract; do not create application code.' if name=='documentation-only' else 'REQ-7: Add a health endpoint returning HTTP 200 with JSON status ok.'
        for relative,body in files.items():
            path = root/name/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(body+'\n',encoding='utf-8')
    shutil.copytree(root/'python-tdd',root/'ambiguous')
    with (root/'ambiguous/AGENTS.md').open('a') as stream:
        stream.write('At this same scope implementation must precede every regression. No current user resolution is supplied.\n')
    save(root/'before.json',{name:scan(root/name) for name in expected})
    print('Fixed section 5.4 project fixtures retained; native adaptation tasks must be separately observed.')

if __name__=='__main__':
    {'golden':golden,'binding':lambda:binding('windows' if sys.platform=='win32' else 'linux'),'projects':projects}[sys.argv[1]]()
