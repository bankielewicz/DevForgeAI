import datetime as dt
import hashlib
import json
import re
from pathlib import Path
ROOT=Path('C:/Projects/DevForgeAI'); RUN=Path(__file__).parent; OLD=ROOT/'docs/plan/skill-validations/skill-builder/20260912T161842Z'; BUILD=ROOT/'docs/plan/skill-builds/skill-builder/20260912T212438315Z'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(RUN).as_posix(),'sha256':h(p)}
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('delivery-audit.json',):
    p=RUN/'inputs/build'/name;p.write_bytes((BUILD/name).read_bytes())
before=json.loads((RUN/'inputs/prior-validation/source-manifest.json').read_text())
after=json.loads((RUN/'source-manifest.json').read_text())
b={r['path']:r for r in before['files']};a={r['path']:r for r in after['files']}
changed=sorted(k for k in b.keys()&a.keys() if b[k]!=a[k]);assert changed==['evals/build-manifest.json','references/evidence-format.md'] and b.keys()==a.keys()
old_row='| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require the three actual trials in the evaluation reference. |'
new_row='| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements). |'
old=(OLD/'source/references/evidence-format.md').read_bytes();new=(RUN/'source/references/evidence-format.md').read_bytes()
assert old.count(old_row.encode())==1 and old.replace(old_row.encode(),new_row.encode())==new
bm=(OLD/'source/evals/build-manifest.json').read_bytes();am=(RUN/'source/evals/build-manifest.json').read_bytes()
assert bm.count(b['references/evidence-format.md']['sha256'].encode())==1
assert bm.replace(b['references/evidence-format.md']['sha256'].encode(),a['references/evidence-format.md']['sha256'].encode())==am
manifest=json.loads(am);actual={k:r['sha256'] for k,r in a.items() if k!='evals/build-manifest.json'};assert manifest['artifacts']==actual
evaluation=(RUN/'source/references/evaluation.md').read_text();assert h(RUN/'source/references/evaluation.md')==b['references/evaluation.md']['sha256']
section=evaluation.split('## Required forward trials for builder enhancements\n',1)[1].split('\n## Report results',1)[0]
families=re.findall(r'^([1-4])\. (.*)$',section,re.M);assert [x[0] for x in families]==['1','2','3','4'] and 'Separately evaluate routing' in section
save(RUN/'trials/delta/observation.json',{'schema_version':'1','run_id':RUN.name,'status':'PASS','changed_paths':changed,'added_paths':[],'removed_paths':[],'exact_row_only':True,'exact_manifest_digest_only':True,'other_34_files_unchanged':True,'all_35_bound_artifacts_match':True,'four_families':[x[1] for x in families],'separate_routing_preserved':True,'old_row':old_row,'new_row':new_row,'evaluation_sha256':h(RUN/'source/references/evaluation.md')})
pub=RUN/'inputs/build/published';observed=[]
for line in (RUN/'inputs/build/published-results.jsonl').read_text().splitlines():
    r=json.loads(line);assert r['status']=='PASS' and r['expectation_met'] and r['profile']=='revision-spec-v2'
    assert r['cases_sha256']==h(RUN/'inputs/build/published-cases.jsonl') and r['build_manifest_sha256']==h(RUN/'source/evals/build-manifest.json')
    for path,sha in r['candidate_digests'].items():assert h(pub/path)==sha,(path,sha)
    observed.append({'case_id':r['case_id'],'status':r['status'],'measured_hashes_verified':len(r['candidate_digests'])})
save(RUN/'trials/delivery-identity/profile-readback.json',{'schema_version':'1','run_id':RUN.name,'status':'PASS','observations':observed,'classification':'Verified same-session prior execution, not a fresh evaluator invocation by this validation task','result':ref(RUN/'inputs/build/published-results.jsonl'),'cases':ref(RUN/'inputs/build/published-cases.jsonl')})
wf=json.loads((OLD/'workflow-map.json').read_text());wf['run_id']=RUN.name;wf['review_type']='Fresh independent assessor reread unchanged source entrypoints/resources and confirmed preserved paths; prior map used as an index, not execution evidence.'
wf['steps'].append({'step_id':'report-forward-trials','entrypoint':'references/evidence-format.md:Reports and statuses / Independent forward trials row','entry_conditions':'Report required observations after selected operation','inputs':['Actual independent trial outputs and applicability from evaluation.md'],'executor':'Codex host following the reference link','action':'Report all applicable independent trial families from linked evaluation section; report routing separately','outputs':['Accurate trial status and limits'],'completion_evidence':'All applicable required trials have actual execution evidence or completion remains blocked','next_or_branch_targets':'publish or retained incomplete result','failure_route':'Required NOT_PERFORMED/FAILED blocks completion; no stale three-trial summary','terminal_user_outcome':'Complete or explicitly incomplete development report'})
save(RUN/'workflow-map.json',wf)
passages=[('references/evidence-format.md',new_row,'Reports and statuses; Independent forward trials','useful_instruction','Links to governing applicable families rather than stale cardinality; all four and routing retained.'),('SKILL.md','Python, required artifacts/cases, changed-script checks, and required task trials cannot be skipped for a completed build.','Evaluate, deliver, and report','useful_instruction','Actionable completion evidence requirement retained.'),('references/adoption.md','Snapshot immutability is a workflow convention; rehash every use.','Capture, evaluate, publish','useful_instruction','Detects drift without claiming enforced immutability.'),('assets/worker-task-template.md','This file is a task contract, not an installed agent profile or an enforced permission policy.','Worker task template','useful_instruction','Keeps assignment separate from enforced isolation.')]
rows=[]
for name,anchor,context,classification,effect in passages:
    p=RUN/'source'/name;data=p.read_text();assert anchor in data;line=data[:data.index(anchor)].count('\n')+1
    rows.append({'subject_path':name,'locator':{'line_start':line,'line_end':line},'excerpt':anchor,'context':context,'classification':classification,'intended_effect':effect,'disposition':'preserve','source':ref(p)})
save(RUN/'trials/semantic/ceremony-review.json',{'schema_version':'1','run_id':RUN.name,'passages':rows,'unsupported_enforcement_claims_found':False,'review_type':'Independent assessor semantic review; not validator self-review'})
save(RUN/'finding-resolution.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-builder','prior_finding_id':'F-8c43eca6259d05a2153068b5d5b29495d0c208229c2a19f49bc71355d8df2d1f','classification':'resolved','basis':'Exact approved summary replacement, live manifest binding and unchanged detailed four-family plus separate routing contract verified. This resolves a wording contradiction; it does not itself execute all trial families.','evidence':[ref(RUN/'trials/delta/observation.json'),ref(RUN/'source/references/evaluation.md'),ref(RUN/'source/references/evidence-format.md'),ref(RUN/'inputs/prior-validation/findings.json')],'verification_cases':['AC-01','AC-02','AC-03','AC-04']})
requests=[('R01','Import the local Claude skill package ./raw/receipt-scan into this Codex development project.','import'),('R02','Build the approved task-card specification at docs/plan/task-card-spec.md into development source.','spec_build'),('R03','Revise the previously generated task-card skill using its verified successful baseline and this approved revised specification.','revision'),('R04','Adopt the existing Codex development package task-card, preserving its exact bytes and managing the explicitly listed paths; no builder baseline exists.','adoption'),('R05','Validate the task-card skill and report findings without changing anything.','unrelated'),('R06','Explain how skill-builder handles regeneration.','explanation'),('R07','Write a proposed specification for a new task-card skill; do not build it.','specification_authoring'),('R08','Install this existing skill into my personal skill directory.','installation'),('R09','Correct a typo in my unrelated application README.','unrelated')]
routing=RUN/'trials/routing';description=(RUN/'source/SKILL.md').read_text().split('description: ',1)[1].split('\n',1)[0]
(routing/'description.txt').write_text(description+'\n',encoding='utf-8')
(routing/'requests.jsonl').write_text(''.join(json.dumps({'case_id':i,'request':q})+'\n' for i,q,_ in requests),encoding='utf-8')
(routing/'expected.jsonl').write_text(''.join(json.dumps({'case_id':i,'request':q,'route':route})+'\n' for i,q,route in requests),encoding='utf-8')
prompt=f'''Classify the requests in {routing.as_posix()}/requests.jsonl using only the skill description in {routing.as_posix()}/description.txt. Allowed route names are import, spec_build, revision, adoption, explanation, specification_authoring, installation, unrelated; validation-only requests belong to unrelated. Do not execute any request. Do not read any other files or expected labels. Write {routing.as_posix()}/observed.jsonl with one JSON object per request containing only case_id, route and request, and {routing.as_posix()}/reasoning.md with brief reasons. You may write only those two output files. Return the output paths. This is description classification, not native skill activation.'''
(routing/'prompt.txt').write_text(prompt,encoding='utf-8')
save(routing/'plan.json',{'schema_version':'1','case_id':'ROUTING-01','requirement_ids':['SB-ROUTING'],'fixture_inputs':[ref(routing/'description.txt'),ref(routing/'requests.jsonl')],'expected_outputs':ref(routing/'expected.jsonl'),'expected_effects':'Only observed.jsonl and reasoning.md created; no request execution','executor':'independent Codex agent fork_turns none','task_prompt':prompt,'timeout_seconds':300,'permitted_write_root':str(routing),'planned_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
print('Delta and finding resolution PASS; three publication results with',sum(x['measured_hashes_verified'] for x in observed),'measured hashes verified; routing planned.')
