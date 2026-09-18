"""Create a separate data capsule for the unchanged external evaluator."""
import continue_evaluation as c
import copy
import sys
r=c.RUN
e=r.with_name(r.name+'-evaluation-v2')
def put(src,relative):
    dst=e/relative
    if dst.exists(): assert dst.read_bytes()==src.read_bytes(),str(dst)
    else: c.copy_file(src,dst)
def eref(p):
    return {'path':p.relative_to(e).as_posix(),'sha256':c.h.sha(p.read_bytes())}
if __name__=='__main__':
    e.mkdir(exist_ok=False)
    old_manifest=c.load(c.PRIOR/'bundle/artifact-manifest.json')
    # Exact evaluator implementation and fixtures: no code maintenance.
    for row in old_manifest['artifacts']:
        src=c.PRIOR/'bundle'/row['path']
        assert c.h.sha(src.read_bytes())==row['sha256']
        put(src,'bundle/'+row['path'])
    for row in old_manifest['input_refs']:
        src=c.PRIOR/row['path']
        assert c.h.sha(src.read_bytes())==row['sha256']
        if row['path']!='rule-set.json': put(src,row['path'])
    put(r/'rule-set.json','rule-set.json')
    put(r/'source-manifest.json','source-manifest.json')
    for row in c.load(r/'source-manifest.json')['files']: put(r/'source'/row['path'],'source/'+row['path'])
    put(r/'commands/intake/stdout.txt','commands/intake/stdout.txt')
    put(r/'inputs/native-plan.json','inputs/continuation-plan.json')
    put(r/'inputs/carry-forward.json','inputs/carry-forward.json')
    for case in c.load(r/'inputs/carry-forward.json')['cases']:
        assert case['eligible'],case['case_id']
        original=case['prior_case']
        for ref in original['evidence']: put(c.PRIOR/ref['path'],'inputs/carried/'+ref['path'])
        # The native paths remain original historical projects, verified unchanged.
        for name in original.get('native_trials',[]):
            attempt=original.get('native_attempts',{}).get(name,'001')
            for rel in ['trials/'+name+'/plan.json','commands/'+name+'-'+attempt+'/command.json',
                        'trials/'+name+'/attempt-'+attempt+'/effects.json']:
                put(c.PRIOR/rel,rel)
    manifest=copy.deepcopy(old_manifest)
    manifest.update(run_id=r.name,package_digest=c.load(r/'source-manifest.json')['package_digest'],
       continuation_basis='Sixteen verified historical PASS cases, fresh explicit trials for seven incomplete cases. Raw fixture/scenario oracle remains unchanged; new attempt paths and 900-second budgets are bound in inputs/continuation-plan.json.',
       evaluator_code_change='NONE: runner.py and graders.py are byte-identical to prior bound bundle.')
    manifest['input_refs']=[eref(e/row['path']) for row in old_manifest['input_refs']]
    manifest['input_refs'] += [eref(e/'source-manifest.json'),eref(e/'inputs/continuation-plan.json'),eref(e/'inputs/carry-forward.json')]
    c.save(e/'bundle/artifact-manifest.json',manifest)
    c.save(r/'inputs/external-bundle-location.json',{'evaluation_root':str(e),
       'manifest':{'path':str(e/'bundle/artifact-manifest.json'),'sha256':c.h.sha((e/'bundle/artifact-manifest.json').read_bytes())},
       'runner_identity_matches_prior':(e/'bundle/runner.py').read_bytes()==(c.PRIOR/'bundle/runner.py').read_bytes(),
       'grader_identity_matches_prior':(e/'bundle/graders.py').read_bytes()==(c.PRIOR/'bundle/graders.py').read_bytes(),
       'layout':'Foreign schema family is outside schema-1 run; raw copies under inputs are evidence. Unchanged external runner validates its own artifacts, fixtures, schema and results.'})
    print('EXTERNAL_BUNDLE_PREPARED',e)
