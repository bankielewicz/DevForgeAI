"""Retain supported adaptive observations separately from legacy record parsing."""
import copy
import hashlib
import json
from pathlib import Path

RAW=Path(__file__).resolve().parent
ROOT=RAW.with_name(RAW.name+'-supplemental')
CAPSULE=RAW.with_name(RAW.name+'-records')

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write('\n')

def ref(path):
    return {'path':str(path.resolve()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    observed=json.loads((RAW/'package.stdout.txt').read_bytes())['observations']
    resources=copy.deepcopy(observed['resources'])
    for row in resources:
        row.update(reachable=True,usage='used',evidence=[ref(RAW/'semantic-review.md')],reason='Reviewed entry routing or downstream consumer instruction; static usage does not claim every branch executed.')
        if row['path']=='scripts/check_project_binding.py':
            row['reason']='Explicit command at SKILL.md line 17; runtime helper checked on Windows and Linux.'
            row['evidence']+=[ref(RAW/'evaluation/attempt-001/results.jsonl')]
    edges=copy.deepcopy(observed['edges'])
    edges.append(dict(source='SKILL.md',line=17,target='scripts/check_project_binding.py',kind='script_call',resolution='resolved'))
    bindings=[]
    for line in (RAW/'evaluation/attempt-001/results.jsonl').read_text(encoding='utf-8').splitlines():
        result=json.loads(line)
        path=RAW/'evaluation/attempt-001'/result['case_id']/'stdout.txt'
        observation=json.loads(path.read_bytes())
        assert observation==result['observation'] and result['result']=='PASS'
        expected=next(json.loads(item)['expected'] for item in (RAW/'evaluation/cases.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(item)['case_id']==result['case_id'])
        bindings.append(dict(case_id=result['case_id'],binding_sha256=observation['binding_sha256'],observation=ref(path),expected=expected['status'],observed=observation['status'],effects_match=result['before']==result['after']))
    digest=json.loads((RAW/'source-manifest.json').read_bytes())['package_digest']
    write(ROOT/'adaptive-observations.json',dict(schema_version='adaptive-observations-v1',run_id=RAW.name,target_digest=digest,unicode_candidates=observed['unicode_candidates'],resources=resources,edges=edges,context=observed['context'],bindings=bindings,limitations=['Resource usage is a semantic review of captured instructions, not all native branch coverage.','No selected context budget; token counting and model-load accounting NOT_RUN.','Binding records observe fixtures only and convey no protected authorization.','Raw package observations remain unchanged; snapshot-name and quoted-placeholder items were manually adjudicated.']))
    packet=RAW/'inputs/repository/docs/plan/skill-authorings/story-create/20260917T182711Z-02/validation-request.json'
    base=packet.parent
    write(ROOT/'authoring-family-assessment.json',dict(schema_version='story-create-authoring-assessment-v1',run_id=RAW.name,target_digest=digest,request=ref(packet),baseline=ref(base/'authoring-baseline.json'),authoring_record=ref(base/'authoring-record.json'),intake=ref(RAW/'intake.stdout.json'),assessment=ref(CAPSULE/'assessment.json'),history='Verified authoring-v1 custody; not a previous tested build or legacy generated/adopted quality history.',assessment_completed=True,outcome='INCOMPLETE',target_mutations=False,framework_acceptance='NOT_EVALUATED',limitations=['The custom authoring-family supplement has manual field/reference review, not a claim of schema-1 helper coverage.']))
    print(json.dumps({'root':str(ROOT),'resources':len(resources),'bindings':len(bindings)}))

if __name__=='__main__':main()
