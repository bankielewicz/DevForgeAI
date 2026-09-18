"""New independent linked-record, legacy, metadata and update-review cases."""
import copy
import json
from pathlib import Path
import sys
import test_independent as t

OUT=t.RUN/'fixtures/extended-03'
original=t.check
t.RESULTS=[]

def check(case,argv,*args,**kwargs):
    if len(argv)>4 and Path(str(argv[4])).is_relative_to(t.BUILDER):
        argv=argv[:4]+['-m','coverage','run','--append','--branch','--data-file='+str(t.RUN/'coverage-data'),'--source='+str(t.BUILDER)]+argv[4:]
    return original('ext-'+case,argv,*args,**kwargs)
t.check=check

def inspect(case,path,code=0):return t.inspect(case,path,code)

def linked():
    src=t.RUN/'fixtures/followup-02/records'; result=json.loads((src/'set-result.json').read_text(encoding='utf-8'))
    rr=src/'docs/plan/set-c-complete-run'; ar=json.loads((rr/'authoring-record.json').read_text(encoding='utf-8'));vr=json.loads((rr/'validation-request.json').read_text(encoding='utf-8'))
    for label in ('valid','quality','kind','request-identity','request-type','request-manifest'):
        folder=OUT/label;folder.mkdir(parents=True);a=copy.deepcopy(ar);v=copy.deepcopy(vr)
        if label=='quality':a.update(validation_status='PASS',testing_status='PASS')
        if label=='kind':a['record_kind']='unrelated-record'
        ap=t.put(folder/'authoring-record.json',a);v['authoring_record']=t.ref(ap)
        if label=='request-identity':v.update(target_name='unrelated',target_root=str(OUT/'unrelated'))
        if label=='request-type':v['changed_paths']=False
        if label=='request-manifest':v['target_manifest']=t.ref(t.put(folder/'wrong-manifest.json',{'schema_version':'1','files':[],'package_digest':t.digest([])}))
        vp=t.put(folder/'validation-request.json',v)
        t.put(folder/'publication-readback.json',{'state':'PUBLISHED','authoring_record':t.ref(ap),'request':t.ref(vp)})
        r=copy.deepcopy(result);r['members'][2].update(authoring_record=t.ref(ap),validation_request=t.ref(vp))
        inspect('linked-'+label,t.put(folder/'set.json',r),0 if label=='valid' else 1)

def legacy():
    for kind in ('generated','adopted','wrong-pointer','corrupt-generated'):
        project=OUT/('legacy-'+kind);project.mkdir();target=project/'src/agents/skills/sample';t.put(target/'SKILL.md','baseline\n');hist=project/'history';hist.mkdir();t.put(hist/'snapshot/SKILL.md','baseline\n');spec=t.put(hist/'spec.md','Explicit historical requirement R1.\n')
        manifest=t.rows(hist/'snapshot');mh=t.put(hist/'snapshot-manifest.json',{'schema_version':'1','files':manifest});managed=t.put(hist/'managed-manifest.json',{'schema_version':'1','files':manifest})
        rel=lambda p:{'path':p.relative_to(hist).as_posix(),'sha256':t.sha(p.read_bytes())}
        if kind in ('adopted','wrong-pointer'):
            rb=t.put(hist/'readback.json',{'schema_version':'1','run_id':'old1','target_root':str(target),'before':manifest,'after':manifest,'spec_before_sha256':t.sha(spec.read_bytes()),'spec_after_sha256':t.sha(spec.read_bytes()),'outcome':'UNCHANGED'})
            adoption={'schema_version':'1','record_kind':'adoption','run_id':'old1','target_name':'sample','target_root':str(target),'project_root':str(project),'captured_at_utc':'2026-09-12T00:00:00Z','historical_origin':'unknown','snapshot_root':'snapshot','snapshot_manifest':rel(mh),'managed_paths':['SKILL.md'],'retained_user_paths':[],'origin_spec':rel(spec),'authorization':{'instruction':'Explicitly adopt sample SKILL.md only','target_root':str(target),'managed_manifest_sha256':t.sha(managed.read_bytes()),'origin_spec_sha256':t.sha(spec.read_bytes())},'prior_evidence':[],'quality_evidence':[],'source_readback':rel(rb),'recording_state':'ADOPTED','managed_manifest':rel(managed),'origin_spec_input':{'resolved_path':str(spec),'bytes':spec.stat().st_size,'sha256':t.sha(spec.read_bytes())}}
            ap=t.put(hist/'adoption.json',adoption);pointer={'schema_version':'2','run_id':'wrong-run' if kind=='wrong-pointer' else 'old1','target_name':'wrong-skill' if kind=='wrong-pointer' else 'sample','origin':dict(kind='adopted',**rel(ap)),'baseline':[{'path':'SKILL.md','sha256':t.sha(b'baseline\n')}]};prior=t.put(hist/'pointer.json',pointer)
        else:
            old_contract={'schema_version':'1','mode':'spec_build','target_name':'sample','inputs':[{'id':'S1','path':'spec.md','resolved_path':str(spec),'role':'spec','bytes':spec.stat().st_size,'sha256':t.sha(spec.read_bytes())}],'authorization':{'instruction':'Historical build sample','inputs':[{'id':'S1','sha256':t.sha(spec.read_bytes())}]},'artifacts':[{'path':'SKILL.md'}]}
            cp=t.put(hist/'build-contract.json',old_contract);ev=t.put(hist/'evidence.json',{'schema_version':'1','run_id':'old1','target_name':'sample','outputs':[{'path':'SKILL.md','sha256':t.sha(b'baseline\n')}]})
            provenance={'schema_version':'1','run_id':'old1','mode':'spec_build','target_name':'sample','builder_manifest_sha256':'0'*64,'contract_sha256':t.sha(cp.read_bytes()),'inputs':[{'id':'S1','sha256':t.sha(spec.read_bytes())}],'dependencies':[],'outputs':[{'path':'SKILL.md','sha256':t.sha(b'baseline\n'),'ownership':'generated','baseline_path':'snapshot/SKILL.md','baseline_sha256':t.sha(b'baseline\n')}],'mappings':[{'requirement_id':'R1','artifact_paths':['SKILL.md'],'evidence_ids':['E1']}],'evidence':[dict(id='E1',**rel(ev))],'result':'COMPLETE','prior_build':None}
            prior=t.put(hist/'provenance.json',provenance)
            if kind=='corrupt-generated':t.put(hist/'snapshot/SKILL.md','corrupt')
        c=t.contract(project,'sample','edit',prior);c.update(target_root=str(target),legacy_root=str(hist));cp=t.put(project/'contract.json',c)
        before=t.rows(hist)
        check('legacy-'+kind,t.PY+[t.BUILDER/'scripts/authoring.py','begin','--contract',cp,'--run-root',project/'docs/plan/edit'],2 if kind in ('wrong-pointer','corrupt-generated') else 0)
        t.put(project/'history-preservation.json',{'before':before,'after':t.rows(hist),'unchanged':before==t.rows(hist)})

def updates():
    folder=OUT/'updates';folder.mkdir();e,ep,p,pp,s,sp=t.base_records(folder)
    core=folder/'parents/core-one';t.put(core/'SKILL.md','---\nname: core-one\ndescription: Reusable workflow\n---\n| ID | Requirement |\n| --- | --- |\n| R1 | Summarize requirements |\n')
    parent=t.pkg(core,folder/'core-manifest.json');variant=folder/'dest/variant-one';t.adaptive_package(variant,'project_variant',{'name':'core-one','package_digest':parent['package_digest'],'requirement_ids':['R1']},'R1 retained: Summarize requirements.\n')
    existing=t.pkg(variant,folder/'variant-manifest.json');m=p['members'][0];m.update(name='variant-one',role='project_variant',action='retain',target_root=str(variant),existing_package=existing,parent_core=parent,lineage_delta=[{'requirement_id':'R1','disposition':'retained','reason':'Equivalent child','replacement_requirement_ids':['R1']}]);p.update(members=[m],state='NO_CHANGE');prior=t.put(folder/'prior.json',p)
    current=copy.deepcopy(p);current.update(mode='review_updates',prior_proposal=t.ref(prior));inspect('update-unchanged',t.put(folder/'unchanged.json',current))
    newer=folder/'new-parent/core-one';t.put(newer/'SKILL.md',(core/'SKILL.md').read_bytes()+b'\nAdditional whitespace.\n');newref=t.pkg(newer,folder/'new-core-manifest.json');current['members'][0]['parent_core']=newref;current['state']='PROPOSED';inspect('update-equivalent-bytes',t.put(folder/'equivalent.json',current))
    bad=copy.deepcopy(current);bad['state']='NO_CHANGE';inspect('update-false-no-change',t.put(folder/'false-unchanged.json',bad),1)
    missing=copy.deepcopy(current);missing['members'][0]['parent_core']['manifest']['sha256']='0'*64;inspect('update-missing-history',t.put(folder/'missing.json',missing),1)

def metadata():
    root=OUT/'metadata/sample';t.put(root/'SKILL.md','---\nname: sample\ndescription: Example\n---\n');t.put(root/'agents/openai.yaml','interface:\n  display_name: Original\n  short_description: Useful original description here\n  brand_color: "#123456"\npolicy:\n  allow_implicit_invocation: false\ndependencies:\n  tools: []\n')
    check('metadata-preserve',t.PY+[t.BUILDER/'scripts/generate_openai_yaml.py',root,'--interface','display_name=Changed'],0)
    import yaml
    value=yaml.safe_load((root/'agents/openai.yaml').read_text(encoding='utf-8'));t.RESULTS.append({'case':'metadata-unrelated-fields','status':'PASS' if value['interface']['brand_color']=='#123456' and value['policy']['allow_implicit_invocation'] is False and value['dependencies']=={'tools':[]} else 'FAIL'})
    check('initializer-occupied',t.PY+[t.BUILDER/'scripts/init_skill.py','sample','--path',root.parent],1)
    check('initializer-new',t.PY+[t.BUILDER/'scripts/init_skill.py','new-sample','--path',root.parent],0)
    for n in ('one','two'):t.put(OUT/'resolver/docs/plan'/f'{n}.md','---\nskill_name: requested\n---\nTask\n')
    check('spec-ambiguous',t.PY+[t.BUILDER/'scripts/build_evidence.py','resolve-spec','--project-root',OUT/'resolver','--name','requested'],1,'reason_code','AMBIGUOUS_INPUT')
    check('spec-explicit',t.PY+[t.BUILDER/'scripts/build_evidence.py','resolve-spec','--project-root',OUT/'resolver','--spec','docs/plan/one.md'],0,'status','RESOLVED')

def main():
    OUT.mkdir(parents=True,exist_ok=False)
    t.put(t.RUN/'coverage-scope.json',{'denominator':'All executable lines in seven selected builder Python files, including copied-runtime template and adapted initializer/metadata code. No first-party exclusions.','measurement':'Supplemental Windows test_extended.py commands only; earlier uninstrumented runs cannot contribute. Branch coverage separate.','tool':'coverage.py 7.9.0','floor':95,'interpretation':'Audit observation, not compiled Rust framework qualification'})
    linked();legacy();updates();metadata();t.put(t.RUN/'extended-results.json',t.RESULTS)
    print(json.dumps({'count':len(t.RESULTS),'failures':[r['case'] for r in t.RESULTS if r['status']=='FAIL']}))

if __name__=='__main__':main()
