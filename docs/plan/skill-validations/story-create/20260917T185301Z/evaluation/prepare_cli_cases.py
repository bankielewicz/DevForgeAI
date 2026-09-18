"""Freeze positive/adverse helper CLI inputs independently from target output."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prepare_trials import binding,put,ref,RUN

def main():
    cases=[]
    definitions=[('H01','valid',0,'BOUND','MATCH'),('H02','missing',1,'MISSING_BINDING','MISMATCH'),('H03','malformed',1,'INVALID_BINDING','MISMATCH'),('H04','duplicate',1,'INVALID_BINDING','MISMATCH'),('H05','stale',1,'PACKAGE_CHANGED','MISMATCH'),('H06','unselected',1,'NOT_SELECTED','MISMATCH'),('H07','wrong_root',1,'ROOT_MISMATCH','MISMATCH'),('H08','wrong_role',1,'ROLE_MISMATCH','MISMATCH'),('H09','relocated',1,'UNBOUND_SKILL','MISMATCH'),('H10','unicode_spaces',0,'BOUND','MATCH'),('H11','extra',1,'INVALID_BINDING','MISMATCH'),('H12','nonfinite',1,'INVALID_BINDING','MISMATCH'),('H13','missing_argument',2,None,None),('H14','help',0,None,None)]
    for ident,kind,exit_code,reason,status in definitions:
        root=RUN/'evaluation/fixtures'/ident/('project space Ω [literal]' if kind=='unicode_spaces' else 'project')
        skill=root/'.agents/skills/story-create';shutil.copytree(RUN/'source',skill)
        value=binding(root)
        if kind=='stale':value['bindings'][0]['package_digest']='0'*64
        if kind=='unselected':value['bindings'][0]['selected']=False
        if kind=='wrong_root':value['project_root']=str(root.parent)
        if kind=='wrong_role':value['bindings'][0]['role']='expertise'
        if kind=='extra':value['unexpected']=True
        path=root/'.agents/devforgeai/project-binding.json'
        if kind!='missing':
            raw='{' if kind=='malformed' else '{"x":1,"x":2}' if kind=='duplicate' else '{"x":NaN}' if kind=='nonfinite' else json.dumps(value)
            put(path,raw)
        if kind=='relocated':
            other=root/'relocated/story-create';shutil.copytree(skill,other);skill=other
        argv=[sys.executable,'-B','-X','utf8',str(skill/'scripts/check_project_binding.py')]
        if kind=='help':argv+=['--help']
        elif kind!='missing_argument':argv+=['--project-root',str(root),'--skill-root',str(skill)]
        expected={'exit_code':exit_code}
        if reason:expected.update(reason_code=reason,status=status)
        cases.append({'case_id':ident,'argv':argv,'cwd':str(root),'project_root':str(root),'expected':expected,'inputs':[ref(p) for p in root.rglob('*') if p.is_file()],'timeout_seconds':120})
    put(RUN/'evaluation/cases.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in cases))
    put(RUN/'evaluation/runtime.json',{'python':'3.10+','observed_python':sys.version,'dependencies':{'helper':'Python standard library','graders':'PyYAML 6.0.2','coverage':'coverage 7.9.0'},'network':False,'source_manifest':ref(RUN/'source-manifest.json'),'requirements':ref(RUN/'inputs/repository/docs/plan/skill-authorings/story-create/20260917T182711Z-intake/requirements.json'),'authority':'Evidence only; no mutations authorized or framework acceptance.'})
    put(RUN/'evaluation/cases.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['case_id','argv','cwd','project_root','expected','inputs','timeout_seconds'],'properties':{'case_id':{'type':'string'},'argv':{'type':'array','items':{'type':'string'}},'cwd':{'type':'string'},'project_root':{'type':'string'},'expected':{'type':'object','required':['exit_code'],'properties':{'exit_code':{'type':'integer'},'reason_code':{'type':'string'},'status':{'type':'string'}}},'inputs':{'type':'array','items':{'type':'object','required':['path','sha256']}},'timeout_seconds':{'type':'number','minimum':1}}})
    print('Frozen',len(cases),'CLI cases')

if __name__=='__main__':main()
