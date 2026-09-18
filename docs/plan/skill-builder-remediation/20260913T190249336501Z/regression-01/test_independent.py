"""Independent terminal fixtures and oracles. Builder helpers are systems under test.

No validator imports, copied tests, external dependencies, or production writes.
Run once per fresh suite directory. Fixture plans precede every SUT invocation.
"""
import copy
import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import uuid
from capture import RUN, ROOT, sha, inventory, digest
from runner import run

BUILDER = ROOT / 'src/agents/skills/skill-builder'
PY = [sys.executable, '-B', '-X', 'utf8']
SUITE = RUN / 'fixtures' / 'independent-01'
RESULTS = []

def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    elif isinstance(value, str):
        path.write_text(value, encoding='utf-8', newline='')
    else:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='')
    return path

def ref(path):
    return {'path': str(path.resolve()), 'sha256': sha(path.read_bytes())}

def rows(root):
    return inventory(root)[0]

def pkg(root, manifest_path):
    manifest = rows(root)
    put(manifest_path, manifest)
    return {'name': root.name, 'root': str(root), 'manifest': ref(manifest_path), 'package_digest': digest(manifest)}

def check(case, argv, expected_exit, field=None, expected=None, read_root=None, extra=None, env=None):
    before = rows(read_root) if read_root else None
    plan = {'exit': expected_exit, 'field': field, 'value': expected, 'read_only_root': str(read_root) if read_root else None, 'before_manifest': before}
    result, out, err = run(case, argv, expected=plan, env=env)
    try:
        observed = json.loads(out)
    except (ValueError, TypeError):
        observed = None
    passed = result['exit'] == expected_exit and not result['timeout']
    if field:
        passed = passed and isinstance(observed, dict) and observed.get(field) == expected
    if read_root:
        after = rows(read_root)
        passed = passed and before == after
        put(RUN / 'commands' / case / 'effects.json', {'before': before, 'after': after, 'unchanged': before == after})
    if extra:
        passed = passed and extra(observed, out, err)
    row = {'case': case, 'status': 'PASS' if passed else 'FAIL', 'expected': plan, 'actual_exit': result['exit'], 'observed': observed, 'evidence': 'commands/' + case, 'target_digest': '464acfdce47c7784062c488ad75f6b31adf303ba1f3cb12143ef76842ff6a926'}
    RESULTS.append(row)
    put(RUN / 'independent-results.json', RESULTS)
    print(case + ' ' + row['status'], flush=True)
    return observed

def inspect(case, record, code=0, plan=False, expected_order=None):
    return check(case, PY + [BUILDER / 'scripts/adaptive.py', 'plan-set' if plan else 'inspect', '--selection' if plan else '--record', record], code, 'status', {0:'VALID',1:'INVALID',2:'UNAVAILABLE'}[code], extra=(lambda o,*_: o['ordered_member_ids'] == expected_order) if expected_order is not None else None)

def adaptive_package(root, role='expertise', parent=None, contract=None):
    put(root / 'SKILL.md', f'---\nname: {root.name}\ndescription: Summarize selected local requirements.\n---\nRun scripts/check_project_binding.py before product writes and after resume or changed inputs. Continue only on MATCH; otherwise report the reason and do not write product files.\nRead references/adaptive-contract.md and assets/devforgeai-skill.json.\n')
    put(root / 'references/adaptive-contract.md', contract or 'Own requirement summaries; exclude implementation. Input docs/requirements.md, output out/summary.txt containing requirement IDs and text. Missing input blocks output. Complete when all supplied IDs are summarized.\n```devforgeai-requirements\n[{"id":"R1","statement":"Summarize requirements"}]\n```\n')
    put(root / 'scripts/check_project_binding.py', (BUILDER / 'assets/adaptive-runtime/check_project_binding.py').read_bytes())
    desc = {'schema_version':'adaptive-skill-v1','name':root.name,'role':role,'binding_required':True,'parent_core':parent,'contract_path':'references/adaptive-contract.md','required_capabilities':['Python 3.10+'],'resource_roles':[{'path':'scripts/check_project_binding.py','role':'runtime','reason':'Checks operational binding before product work'}]}
    put(root / 'assets/devforgeai-skill.json', desc)
    return desc

def binding_cases():
    cases = ['correct','absent','wrong-root','inactive','changed','duplicate-name','role','unbound','unknown-version','extra-field','boolean-revision','bad-date','invalid-descriptor','missing-resource','core-variant','two-variants','invalid-related','excluded-generated','hostile-path','case-root','file-limit','byte-limit']
    for label in cases:
        project = SUITE / ('binding-' + label) / ("space café & $ ; ' (project)" if label == 'hostile-path' else 'project')
        skill = project / '.agents/skills/summary-skill'
        adaptive_package(skill, 'core' if label == 'core-variant' else 'expertise')
        binding = {'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(project),'revision':1,'bindings':[{'name':skill.name,'package_path':'.agents/skills/' + skill.name,'package_digest':digest(rows(skill)),'role':'core' if label == 'core-variant' else 'expertise','selected':True}],'updated_at_utc':'2026-09-13T00:00:00Z'}
        reason, code = 'BOUND', 0
        if label == 'wrong-root': binding['project_root'] = str(project.parent); reason = 'ROOT_MISMATCH'
        if label == 'inactive': binding['bindings'][0]['selected'] = False; reason = 'NOT_SELECTED'
        if label == 'changed': put(skill / 'new.txt', 'changed'); reason = 'PACKAGE_CHANGED'
        if label == 'duplicate-name': binding['bindings'].append(copy.deepcopy(binding['bindings'][0])); reason = 'INVALID_BINDING'
        if label == 'role': binding['bindings'][0]['role'] = 'core'; reason = 'ROLE_MISMATCH'
        if label == 'unbound': binding['bindings'][0]['name'] = 'other'; binding['bindings'][0]['package_path'] = '.agents/skills/other'; reason = 'UNBOUND_SKILL'
        if label == 'unknown-version': binding['schema_version'] = 'project-binding-v9'; reason = 'INVALID_BINDING'
        if label == 'extra-field': binding['approved'] = True; reason = 'INVALID_BINDING'
        if label == 'boolean-revision': binding['revision'] = True; reason = 'INVALID_BINDING'
        if label == 'bad-date': binding['updated_at_utc'] = '2026-02-30T00:00:00Z'; reason = 'INVALID_BINDING'
        if label == 'invalid-descriptor': put(skill / 'assets/devforgeai-skill.json', {}); reason = 'INVALID_BINDING'
        if label == 'missing-resource':
            desc = json.loads((skill / 'assets/devforgeai-skill.json').read_text(encoding='utf-8')); desc['resource_roles'][0]['path'] = 'missing.py'; put(skill / 'assets/devforgeai-skill.json', desc); reason = 'INVALID_BINDING'
        if label in ('core-variant','two-variants','invalid-related'):
            for n in range(1 if label != 'two-variants' else 2):
                other = project / '.agents/skills' / ('other-' + str(n))
                parent = {'name':skill.name if label == 'core-variant' else 'upstream-core','package_digest':'0'*64,'requirement_ids':['R1']}
                adaptive_package(other, 'project_variant', parent, 'R1 retained: summarize requirements.\n')
                binding['bindings'].append({'name':other.name,'package_path':'.agents/skills/' + other.name,'package_digest':digest(rows(other)),'role':'project_variant','selected':True})
                if label == 'invalid-related': put(other / 'assets/devforgeai-skill.json', {})
            reason = 'INVALID_BINDING' if label == 'invalid-related' else 'AMBIGUOUS_ROLE'
        if label == 'excluded-generated': put(skill / 'node_modules/ignored.txt', 'excluded'); reason = 'UNSAFE_PATH'
        if label == 'case-root' and os.name == 'nt': binding['project_root'] = str(project).upper()
        if label == 'file-limit':
            for i in range(2000): put(skill / 'many' / str(i), b'')
            reason, code = 'CAPTURE_LIMIT', 2
        if label == 'byte-limit':
            p = skill / 'large.bin'; p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('wb') as stream: stream.truncate(33554433)
            reason, code = 'CAPTURE_LIMIT', 2
        bp = project / '.agents/devforgeai/project-binding.json'
        if label != 'absent': put(bp, binding)
        else: reason = 'MISSING_BINDING'
        if reason != 'BOUND' and code == 0: code = 1
        before_product = project / 'out/product.txt'
        # Independent controller does NOT write on rejection. Its behavior is not credited to builder.
        check('binding-' + label, PY + [skill / 'scripts/check_project_binding.py','--project-root',project,'--skill-root',skill], code, 'reason_code', reason, read_root=skill if label not in ('file-limit','byte-limit','excluded-generated') else None, extra=lambda o,out,err: 'project_id' not in out and not before_product.exists() and o['status'] == ('MATCH' if code == 0 else 'UNAVAILABLE' if code == 2 else 'MISMATCH'))
    missing_env = dict(os.environ); missing_env['PATH'] = ''
    check('missing-python-child', ['python-does-not-exist-audit','-B','-X','utf8','helper.py'], None, extra=lambda o,out,err: bool(err), env=missing_env)

def base_records(folder):
    source = put(folder / 'inputs/domain.txt', 'Storage owns persistence and HTTP owns request routing.\nSummarize requirements.\n')
    evidence = {'schema_version':'project-evidence-v1','run_id':'e1','project_root':str(folder),'scope_roots':[str(folder / 'inputs')],'inputs':[ref(source)],'facts':[{'id':'F1','category':'domain','statement':'Storage owns persistence','basis':'observed','sources':[{'ref':ref(source),'start_line':1,'end_line':1}]}],'exclusions':[],'complete':True,'capabilities':[],'gaps':[]}
    ep = put(folder / 'evidence.json', evidence)
    req = {'id':'R1','origin':'source','statement':'Summarize requirements','source_refs':[{'ref':ref(source),'start_line':2,'end_line':2}],'rationale':None,'verification':'Compare IDs with input'}
    def member(ident):
        return {'id':ident,'name':'member-' + ident.lower(),'role':'expertise','action':'create','target_root':str(folder / 'dest' / ('member-' + ident.lower())),'existing_package':None,'parent_core':None,'responsibility':'Summarize ' + ident,'exclusions':['No application implementation'],'triggers':['Summarize requirements'],'near_misses':['Implement service'],'requirement_ids':['R1'],'fact_ids':['F1'],'rationale':'Observed domain requirement','depends_on':[],'capabilities':[],'lineage_delta':[]}
    proposal = {'schema_version':'adaptation-proposal-v1','run_id':'p1','mode':'propose','project_evidence':ref(ep),'prior_proposal':None,'requirements':[req],'members':[member('A'),member('B'),member('C')],'handoffs':[],'gaps':[],'state':'PROPOSED'}
    proposal['members'][1]['depends_on'] = ['A']
    pp = put(folder / 'proposal.json', proposal)
    auth = put(folder / 'inputs/authorization.txt', 'Create A, B and C at the destinations in this proposal. No external effects.\n')
    selection = {'schema_version':'adaptation-selection-v1','proposal':ref(pp),'member_ids':['C','B','A'],'destinations':[{'member_id':m['id'],'target_root':m['target_root']} for m in proposal['members']],'authorization':ref(auth),'permitted_effects':['Author selected disposable development packages']}
    sp = put(folder / 'selection.json', selection)
    return evidence, ep, proposal, pp, selection, sp

def record_cases():
    folder = SUITE / 'records'; folder.mkdir(parents=True)
    e, ep, p, pp, s, sp = base_records(folder)
    inspect('record-evidence-valid', ep)
    inspect('record-proposal-valid', pp)
    inspect('record-selection-valid', sp, plan=True, expected_order=['A','B','C'])
    mutations = [ ('extra-field',lambda x:x.update(extra=1)),('unknown-version',lambda x:x.update(schema_version='project-evidence-v2')),('bad-digest',lambda x:x['inputs'][0].update(sha256='a')),('bad-locator',lambda x:x['facts'][0]['sources'][0].update(end_line=99)),('bool-line',lambda x:x['facts'][0]['sources'][0].update(start_line=True)),('duplicate-fact',lambda x:x['facts'].append(copy.deepcopy(x['facts'][0]))),('material-omission',lambda x:x['exclusions'].append({'path':'missing','reason':'Required source unavailable','material':True})) ]
    for label, mutate in mutations:
        value = copy.deepcopy(e); mutate(value); inspect('record-' + label, put(folder / (label + '.json'), value), 1)
    for label, raw in [('duplicate-key','{"schema_version":"project-evidence-v1","schema_version":"project-evidence-v1"}'),('nonfinite','{"schema_version":"project-evidence-v1","x":NaN}'),('overflow','{"schema_version":"project-evidence-v1","x":1e999}'),('invalid-utf8',b'\xff')]: inspect('record-' + label, put(folder / (label + '.json'), raw), 1)
    for label, mutate in [('missing-dependency',lambda x:x['members'][1].update(depends_on=['Z'])),('cycle',lambda x:x['members'][0].update(depends_on=['B'])),('unknown-requirement',lambda x:x['members'][0].update(requirement_ids=['R99'])),('unknown-fact',lambda x:x['members'][0].update(fact_ids=['F99'])),('invalid-name',lambda x:x['members'][0].update(name='UPPER')),('variant-no-parent',lambda x:x['members'][0].update(role='project_variant')),('core-with-lineage',lambda x:x['members'][0].update(role='core',lineage_delta=[{'requirement_id':'R1','disposition':'retained','reason':'Keep','replacement_requirement_ids':['R1']}])),('json-no-schema',lambda x:x['handoffs'].append({'id':'H1','producer':'A','consumer':'B','artifact_role':'card','format':'json','schema_ref':None,'contract':'Required key id','required':True,'failure_behavior':'block_consumer'}))]:
        value = copy.deepcopy(p); mutate(value); inspect('proposal-' + label, put(folder / ('proposal-' + label + '.json'), value), 1)
    for label, mutate in [('missing-selected-dependency',lambda x:x.update(member_ids=['B'],destinations=[x['destinations'][1]])),('missing-destination',lambda x:x['destinations'].pop()),('duplicate-selection',lambda x:x['member_ids'].append('A'))]:
        value = copy.deepcopy(s); mutate(value); inspect('selection-' + label, put(folder / ('selection-' + label + '.json'), value), 1, True)
    occupied = Path(p['members'][0]['target_root']); put(occupied / 'user.txt', 'Do not change')
    inspect('selection-occupied', sp, 1, True)
    caps = copy.deepcopy(p); caps['members'][0]['capabilities'] = [{'id':'rust-gate','command':'Nonexistent protected Rust gate','required':True,'observed':'unavailable','evidence':None,'limitation':'No implemented authority'}]
    cp = put(folder / 'cap-proposal.json', caps); cs = copy.deepcopy(s); cs['proposal'] = ref(cp)
    inspect('selection-missing-capability', put(folder / 'cap-selection.json', cs), 1, True)
    stale = copy.deepcopy(e); stale['inputs'][0]['sha256'] = '0'*64
    inspect('record-stale-reference', put(folder / 'stale.json', stale), 1)
    # Standalone descriptor parsing and parent inventories use real retained package bytes.
    ad = folder / 'source/adaptive-one'; adaptive_package(ad)
    inspect('descriptor-valid', ad / 'assets/devforgeai-skill.json')
    for style in ('fence-lf','fence-crlf','table-other-resource'):
        core = folder / style / 'core-one'; put(core / 'SKILL.md','---\nname: core-one\ndescription: Reusable requirements\n---\n')
        requirements = [{'id':'P1','statement':'One'},{'id':'P2','statement':'Two'},{'id':'P3','statement':'Three'}]
        text = '```devforgeai-requirements\n' + json.dumps(requirements) + '\n```\n'
        if style == 'fence-crlf': text = text.replace('\n','\r\n')
        if style == 'table-other-resource': text = '| ID | Requirement |\n| --- | --- |\n| P1 | One |\n| P2 | Two |\n| P3 | Three |\n'
        put(core / 'references/requirements.md',text)
        parent = pkg(core, folder / style / 'manifest.json')
        vp = copy.deepcopy(p); vm = vp['members'][0]; vm.update(role='project_variant',parent_core=parent,requirement_ids=['P1','P2','P3'],lineage_delta=[{'requirement_id':r['id'],'disposition':'retained','reason':'Preserve exact statement','replacement_requirement_ids':[r['id']]} for r in requirements])
        vp['requirements'] += [dict(id=r['id'],origin='derived',statement=r['statement'],source_refs=[],rationale='Child retains core requirement',verification='Compare statement') for r in requirements]
        inspect('lineage-' + style,put(folder / style / 'valid.json',vp))
        bad=copy.deepcopy(vp); bad['members'][0]['lineage_delta'].pop(); inspect('lineage-missing-' + style,put(folder / style / 'missing.json',bad),1)
        bad=copy.deepcopy(vp); bad['members'][0]['lineage_delta'][2].update(disposition='removed',replacement_requirement_ids=[]); inspect('lineage-removal-' + style,put(folder / style / 'removed.json',bad),1)
    return folder, p, pp, s, sp

def contract(project, name, operation='create', prior=None):
    target = project / 'development skills' / name
    c={'schema_version':'authoring-contract-v1','run_id':'r1','project_root':str(project),'target_root':str(target),'target_name':name,'operation':operation,'authorization':'Current audit authorizes this synthetic ' + operation,'history_review':'verified prior' if prior else 'no_known_history','change_paths':['SKILL.md'],'requirements':[{'custom_legacy_shape':True,'outcome':'Summarize notes'}],'capabilities':[],'expected_outputs':[],'side_effects':[],'inputs':[],'known_issues':[]}
    if prior:c['prior']=ref(prior)
    return c

def author_begin(case,c,folder):
    cp=put(folder / 'input-contract.json',c); runroot=folder / 'docs/plan/run'
    result=check(case,PY+[BUILDER / 'scripts/authoring.py','begin','--contract',cp,'--run-root',runroot],0,'state','STAGED')
    return runroot

def author_cases():
    project=SUITE / 'authoring';project.mkdir()
    c=contract(project,'ordinary'); target=Path(c['target_root'])
    r=author_begin('author-create-begin',c,project)
    put(r / 'candidate/SKILL.md','---\nname: ordinary\ndescription: Summarize supplied notes\n---\nSummarize decisions and actions; absent owner stays unknown.\n')
    check('author-create-publish',PY+[BUILDER / 'scripts/authoring.py','publish','--run-root',r],0,'state','AUTHORED')
    request=json.loads((r / 'validation-request.json').read_text(encoding='utf-8'))
    actual=digest(rows(target)); record=json.loads((r / 'authoring-record.json').read_text(encoding='utf-8'))
    RESULTS.append({'case':'author-request-readback','status':'PASS' if request['package_digest']==actual and request['authoring_record']==ref(r/'authoring-record.json') and record['testing_status']==record['validation_status']=='NOT_PERFORMED' else 'FAIL','evidence':str(r.relative_to(RUN))})
    edit=project / 'edit'; edit.mkdir(); c2=contract(project,'ordinary','edit',r/'authoring-baseline.json'); c2['run_id']='r2'
    er=author_begin('author-edit-begin',c2,edit); put(er/'candidate/SKILL.md',(target/'SKILL.md').read_bytes()+b'Include open questions.\n')
    check('author-edit-publish',PY+[BUILDER/'scripts/authoring.py','publish','--run-root',er],0,'state','AUTHORED')
    for label in ('observed','import','spec_build','adopt','corrupt','drift','outside-scope','extra-field'):
        pr=SUITE/('author-'+label);pr.mkdir(); op={'observed':'edit','corrupt':'edit','drift':'edit','outside-scope':'edit','extra-field':'create'}.get(label,label)
        co=contract(pr,'sample',op);dest=Path(co['target_root'])
        if op in ('edit','adopt'): put(dest/'SKILL.md','---\nname: sample\ndescription: Existing task\n---\nExisting.\n');put(dest/'user.txt','retain exact\r\n')
        if label=='corrupt': co['history_review']='Known but missing prior';cp=put(pr/'input-contract.json',co);check('author-corrupt-history',PY+[BUILDER/'scripts/authoring.py','begin','--contract',cp,'--run-root',pr/'docs/plan/run'],2);continue
        if label=='extra-field':
            co['unlisted_field']=True; cp=put(pr/'input-contract.json',co);check('author-extra-contract-field',PY+[BUILDER/'scripts/authoring.py','begin','--contract',cp,'--run-root',pr/'docs/plan/run'],2);continue
        rr=author_begin('author-'+label+'-begin',co,pr)
        if op!='adopt':put(rr/'candidate/SKILL.md','---\nname: sample\ndescription: Updated task\n---\nUpdated.\n')
        if label=='drift':put(dest/'user.txt','concurrent change')
        if label=='outside-scope':put(rr/'candidate/user.txt','unauthorized')
        blocked=label in ('drift','outside-scope')
        check('author-'+label+'-publish',PY+[BUILDER/'scripts/authoring.py','publish','--run-root',rr],1 if blocked else 0,'state','BLOCKED' if blocked else 'AUTHORED')
    # All B/C/N outcomes through current authoring custody, using independently assigned bytes.
    for label,current,candidate,expected in [('equal-base','base','new','AUTHORED'),('equal-new','user','user','AUTHORED'),('new-equal-base','user','base','AUTHORED'),('divergent','user','new','BLOCKED'),('obsolete-user-edit','user',None,'BLOCKED')]:
        pr=SUITE/('bcn-'+label);pr.mkdir();co=contract(pr,'sample');rr=author_begin('bcn-'+label+'-seed-begin',co,pr);put(rr/'candidate/SKILL.md','base');check('bcn-'+label+'-seed-publish',PY+[BUILDER/'scripts/authoring.py','publish','--run-root',rr],0,'state','AUTHORED')
        dest=Path(co['target_root']);put(dest/'SKILL.md',current);co=contract(pr,'sample','edit',rr/'authoring-baseline.json');second=pr/'second';second.mkdir();r2=author_begin('bcn-'+label+'-begin',co,second)
        if candidate is None:(r2/'candidate/SKILL.md').unlink()
        else:put(r2/'candidate/SKILL.md',candidate)
        check('bcn-'+label+'-publish',PY+[BUILDER/'scripts/authoring.py','publish','--run-root',r2],0 if expected=='AUTHORED' else 1,'state',expected)

def set_cases(folder,p,pp,s,sp):
    # Real per-member publication for C. A failure/B block are retained observations.
    croot=Path(p['members'][2]['target_root']); cc=contract(folder,croot.name);cc['target_root']=str(croot)
    temp=folder/'set-c';temp.mkdir(); cr=author_begin('set-C-begin',cc,temp)
    adaptive_package(cr/'candidate-temp'/'member-c')
    for row in rows(cr/'candidate-temp/member-c'):
        put(cr/'candidate'/row['path'],(cr/'candidate-temp/member-c'/row['path']).read_bytes())
    # Scope must be declared before begin. The first staged attempt remains retained, unused.
    cc['change_paths']=[r['path'] for r in rows(cr/'candidate')]
    temp2=folder/'set-c-complete';temp2.mkdir();rr=author_begin('set-C-complete-begin',cc,temp2)
    for row in rows(cr/'candidate'):put(rr/'candidate'/row['path'],(cr/'candidate'/row['path']).read_bytes())
    check('set-C-publish',PY+[BUILDER/'scripts/authoring.py','publish','--run-root',rr],0,'state','AUTHORED')
    delivered=pkg(croot,folder/'C-manifest.json'); ar=json.loads((rr/'authoring-record.json').read_text(encoding='utf-8'))
    result={'schema_version':'set-authoring-v1','run_id':'set1','selection':ref(sp),'ordered_member_ids':['A','B','C'],'members':[{'member_id':'A','status':'BLOCKED','authoring_record':None,'validation_request':None,'package':None,'reason':'Destination occupied by user bytes','applied_paths':[]},{'member_id':'B','status':'DEPENDENCY_BLOCKED','authoring_record':None,'validation_request':None,'package':None,'reason':'A failed','applied_paths':[]},{'member_id':'C','status':'AUTHORED','authoring_record':ref(rr/'authoring-record.json'),'validation_request':ref(rr/'validation-request.json'),'package':delivered,'reason':'Published and read back','applied_paths':ar['applied_paths']}],'state':'PARTIAL','validation_status':'NOT_PERFORMED','testing_status':'NOT_PERFORMED','issues':[]}
    rp=put(folder/'set-result.json',result);inspect('set-partial-result-valid',rp)
    request={'schema_version':'set-validation-request-v1','run_id':'set1','selection':ref(sp),'set_authoring':ref(rp),'scope':'eligible_subset','members':[{'member_id':'C','package':delivered,'request':ref(rr/'validation-request.json'),'adaptive_descriptor':ref(croot/'assets/devforgeai-skill.json')}],'handoffs':[],'omitted_member_ids':['A','B'],'omitted_handoff_ids':[],'permission':'No external effects granted'}
    inspect('set-subset-valid',put(folder/'set-request.json',request))
    for label,mutate in [('false-full',lambda x:x.update(scope='full_set')),('missing-omission',lambda x:x.update(omitted_member_ids=['A'])),('extra-member',lambda x:x['members'].append(dict(x['members'][0],member_id='Z')))]:
        bad=copy.deepcopy(request);mutate(bad);inspect('set-'+label,put(folder/(label+'.json'),bad),1)
    bad=copy.deepcopy(result);bad['state']='AUTHORED';inspect('set-false-aggregate',put(folder/'false-aggregate.json',bad),1)
    # Misleading, freshly hash-bound linked custody record: valid JSON with wrong closed-schema field values.
    forged=folder/'forged';forged.mkdir()
    fake_ar=copy.deepcopy(ar);fake_ar['validation_status']='PASS';fake_ar['testing_status']='PASS'; fake_ar['record_kind']='not-authoring'
    ap=put(forged/'authoring-record.json',fake_ar)
    vr=json.loads((rr/'validation-request.json').read_text(encoding='utf-8'));vr['authoring_record']=ref(ap);vr['target_name']='wrong-member';vr['target_root']=str(folder/'wrong-target');vr['changed_paths']=False
    vp=put(forged/'validation-request.json',vr)
    put(forged/'publication-readback.json',{'state':'PUBLISHED','authoring_record':ref(ap),'request':ref(vp)})
    altered=copy.deepcopy(result);altered['members'][2]['authoring_record']=ref(ap);altered['members'][2]['validation_request']=ref(vp)
    inspect('set-forged-legacy-fields',put(folder/'forged-result.json',altered),1)

def main():
    SUITE.mkdir(parents=True,exist_ok=False)
    binding_cases()
    records=record_cases()
    author_cases()
    set_cases(*records)
    put(RUN/'independent-results.json',RESULTS)
    print(json.dumps({'total':len(RESULTS),'pass':sum(r['status']=='PASS' for r in RESULTS),'fail':sum(r['status']=='FAIL' for r in RESULTS)}))

if __name__=='__main__':main()
