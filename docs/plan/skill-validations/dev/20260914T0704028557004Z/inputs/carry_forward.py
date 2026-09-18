"""Read-only requalification of historical PASS evidence for unchanged candidate."""
import continue_evaluation as c
import sys
import importlib.util
from pathlib import Path
sys.path.insert(0,str(c.PRIOR/'bundle'))
import graders
spec=importlib.util.spec_from_file_location('prior_audit',c.PRIOR/'audit_native.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
rows=c.load(c.PRIOR/'case-observations-final.json')['cases']
package=c.load(c.RUN/'source-manifest.json')
oldhost=c.load(c.PRIOR/'commands/host-probe/stdout.txt')
host=c.load(c.RUN/'commands/host-probe/stdout.txt')
host_fields=['platform','python','python_executable','codex_executable','config_fields','PyYAML']
host_matches={key:oldhost[key]==host[key] for key in host_fields}
host_matches['codex_version']=oldhost['--version']['stdout']==host['--version']['stdout']
carried=[]
def retain(src):
    rel=src.relative_to(c.PRIOR)
    dst=c.RUN/'inputs/carried'/rel
    if dst.exists(): assert dst.read_bytes()==src.read_bytes()
    else: c.copy_file(src,dst)
    return {'path':dst.relative_to(c.RUN).as_posix(),'sha256':c.h.sha(dst.read_bytes())}
for case in rows:
    if case['result']!='PASS': continue
    problems=[]; refs=[]; trials=[]
    try:
        graders.verify_refs(c.PRIOR,case['evidence'])
        for ref in case['evidence']: refs.append(retain(c.PRIOR/ref['path']))
        for name in case.get('native_trials',[]):
            a=case.get('native_attempts',{}).get(name,'001')
            base=c.PRIOR/'trials'/name
            plan=c.load(base/'plan.json')
            project=Path(plan['permitted_write_root'])
            before=c.load(base/('attempt-'+a)/'before.json')
            after=c.load(base/('attempt-'+a)/'after.json')
            actual=c.h.inventory(project)
            if actual['files']!=after['files']: problems.append(name+': retained project file set/hash changed')
            if plan['package_digest']!=package['package_digest']: problems.append(name+': stale package')
            actual_skill=c.h.inventory(project/'trial-skill/dev')
            if actual_skill['files']!=package['files']: problems.append(name+': captured skill changed')
            fixture=c.h.inventory(Path(plan['fixture_origin']))
            if fixture['files']!=plan['fixture_manifest']['files']: problems.append(name+': fixture changed')
            checked=audit.audit(name)
            if checked['problems'] or checked['immutable_changes']: problems.append(name+': receipt/protected-byte mismatch')
            trials.append({'trial_id':name,'attempt':a,'project_matches_retained_after':actual['files']==after['files'],
                           'fixture_matches':fixture['files']==plan['fixture_manifest']['files'],'audit':checked})
    except (ValueError,OSError,KeyError) as error:
        problems.append(str(error))
    if not all(host_matches.values()): problems.append('host prerequisite identity changed')
    carried.append({'case_id':case['case_id'],'eligible':not problems,'problems':problems,
        'prior_result':case['result'],'prior_reason':case['reason'],'evidence':refs,'trials':trials,
        'basis':'Historical execution retained, not re-executed. Same skill package and bound original inputs/fixtures; original product outputs, candidate and receipt references independently read back.',
        'prior_case':case})
c.save(c.RUN/'inputs/carry-forward.json',{'package_digest':package['package_digest'],'host_matches':host_matches,
 'prior_run':str(c.PRIOR),'cases':carried,'limit':'Native explicit-path evidence only. No implicit activation, namespaced invocation, installation or framework acceptance inferred.'})
print({x['case_id']: {'eligible':x['eligible'],'problems':x['problems']} for x in carried})

