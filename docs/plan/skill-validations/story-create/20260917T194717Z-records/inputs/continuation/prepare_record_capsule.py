"""Reuse byte-verified prior observations while keeping new execution evidence separate."""
import hashlib
import json
from pathlib import Path
import sys
from prepare_continuation import RUN,PRIOR,PROJECT,put,copy_file

ROOT=RUN.with_name(RUN.name+'-records')
OLD=PRIOR.with_name(PRIOR.name+'-records')
sys.path.insert(0,str(PROJECT/'.agents/skills/skill-validator/scripts'))
import observe

def relative_ref(path):return {'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    assert json.loads((RUN/'source-manifest.json').read_bytes())['files']==json.loads((ROOT/'source-manifest.json').read_bytes())['files']
    for folder in ['inputs','evaluator','guidance']:
        files,excluded=observe.inventory(OLD/folder)
        assert not excluded,excluded
        for relative,path,info in files:copy_file(path,ROOT/folder/relative)
    for file in ['rule-set.json','semantic-review.md']:
        copy_file(OLD/file,ROOT/file)
    for file in ['sources.json','workflow-map.json']:
        value=json.loads((OLD/file).read_bytes());value['run_id']=RUN.name
        put(ROOT/file,value)
    origin=json.loads((OLD/'origin-record.json').read_bytes())
    origin['run_id']=RUN.name
    origin['manifest']=relative_ref(ROOT/'source-manifest.json')
    origin['source_readback_state']='NOT_RUN'
    origin['uncertainties']=['Authored custody remains distinct from tested quality history.','Continuation reuses earlier completed observations only for exact unchanged source/specification/operational identities; previous failed and incomplete attempts remain unchanged.']
    put(ROOT/'origin-record.json',origin)
    copied=[p for p in (ROOT/'inputs').rglob('*') if p.is_file()]
    put(RUN/'record-capsule-preparation.json',{'root':str(ROOT),'reused_prior_input_files':len(copied),'prior_assessment':{'path':str(OLD/'assessment.json'),'sha256':hashlib.sha256((OLD/'assessment.json').read_bytes()).hexdigest()},'rule_set_unchanged':(ROOT/'rule-set.json').read_bytes()==(RUN/'rule-set.json').read_bytes(),'scope':'Static/source/helper/routing results will be carried forward with original timestamps and exact evidence. New native/artifact/semantic observations will be retained under inputs/continuation.'})
    print(json.dumps({'root':str(ROOT),'retained_prior_inputs':len(copied)}))

if __name__=='__main__':main()
