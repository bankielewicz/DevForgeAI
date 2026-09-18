"""Fresh companion readback and supplemental arithmetic oracles."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from capture import ROOT, RUN, scan
from terminal_harness import command, save

def companion():
    root = RUN/'companion-final'
    root.mkdir()
    source = ROOT/'src/agents/skills/skill-builder'
    snapshot = root/'skill-builder'
    snapshot.mkdir()
    manifest = scan(source,copy=snapshot)
    save(root/'manifest.json',manifest)
    if scan(source)['files'] != manifest['files'] or scan(snapshot)['files'] != manifest['files']:
        raise ValueError('companion changed during capture')
    save(root/'expectations.json',{'golden':'same fixed input bytes and expectations as golden-contracts/expectations.json','lineage':'same fixed inputs as lineage-fixtures/expectations.json','source_unchanged':True})
    results = []
    for plan in json.loads((RUN/'golden-contracts/expectations.json').read_bytes()):
        name = plan['case_id']
        path = RUN/'golden-contracts'/(name+'.json')
        builder = command(root/'results'/name/'builder',[sys.executable,'-B','-X','utf8',str(snapshot/'scripts/adaptive.py'),'inspect','--record',str(path)])
        validator = command(root/'results'/name/'validator',[sys.executable,'-B','-X','utf8',str(RUN/'self-review/source/scripts/adaptive_observe.py'),'intake-set','--request',str(path),'--request-sha256',hashlib.sha256(path.read_bytes()).hexdigest()])
        results.append({'case_id':name,'builder_exit':builder.returncode,'validator_exit':validator.returncode,'expected_exit':plan['expected_exit'],'agreement':builder.returncode==validator.returncode==plan['expected_exit']})
    save(root/'results.json',results)
    save(root/'readback.json',{'snapshot_unchanged':scan(snapshot)['files']==manifest['files'],'live_unchanged_since_capture':scan(source)['files']==manifest['files']})
    print(json.dumps(results))

def budgets():
    root = RUN/'budget-fixtures'
    root.mkdir()
    (root/'budget.txt').write_text('Required budget: entrypoint at most 10 tokens.\n',encoding='utf-8')
    source_ref = {'path':str(root/'budget.txt'),'sha256':hashlib.sha256((root/'budget.txt').read_bytes()).hexdigest()}
    value = {'schema_version':'adaptive-observations-v1','run_id':'budget-test','target_digest':'a'*64,'unicode_candidates':[],'resources':[{'path':'SKILL.md','role':'runtime','reachable':True,'usage':'unresolved_usage','evidence':[],'reason':'Synthetic count input.'}],'edges':[],'context':{'tokenizer':None,'files':[{'path':'SKILL.md','bytes':5,'characters':5,'lines':1,'tokens':None}],'loads':[],'budget':{'unit':'tokens','scope':'entrypoint','maximum':10,'case_id':None,'source':source_ref},'budget_result':'NOT_RUN','reason':'Tokenizer unavailable; required budget cannot be measured.'},'bindings':[],'limitations':['Synthetic integrity fixture; no actual consumption claim.']}
    save(root/'expectations.json',{'required-token-budget':0,'false-token-pass':1,'repeated-loads':0,'false-unique-total':1,'excerpt-not-full-file':0})
    cases = [('required-token-budget',value,0)]
    wrong = copy.deepcopy(value)
    wrong['context']['budget_result']='PASS'
    cases.append(('false-token-pass',wrong,1))
    repeated = copy.deepcopy(value)
    repeated['context']['budget']={'unit':'bytes','scope':'observed_total_loads','maximum':9,'case_id':'loads','source':source_ref}
    repeated['context']['loads']=[{'case_id':'loads','path':'SKILL.md','occurrences':2,'basis':'observed_full_file','tokens':None,'evidence':[source_ref]}]
    repeated['context']['budget_result']='FAIL'
    cases.append(('repeated-loads',repeated,0))
    wrong = copy.deepcopy(repeated)
    wrong['context']['budget_result']='PASS'
    cases.append(('false-unique-total',wrong,1))
    excerpt=copy.deepcopy(repeated)
    excerpt['context']['loads'][0]['basis']='observed_excerpt'
    excerpt['context']['budget_result']='NOT_RUN'
    cases.append(('excerpt-not-full-file',excerpt,0))
    results=[]
    for name,record,expected in cases:
        directory=root/name
        save(directory/'adaptive-observations.json',record)
        result=command(root/'results'/name,[sys.executable,'-B','-X','utf8',str(RUN/'self-review/source/scripts/adaptive_observe.py'),'records','--run-root',str(directory)])
        results.append({'case_id':name,'exit_code':result.returncode,'expected_exit':expected,'expectation_met':result.returncode==expected})
    save(root/'results.json',results)
    print(json.dumps(results))

if __name__=='__main__':
    {'companion':companion,'budgets':budgets}[sys.argv[1]]()
