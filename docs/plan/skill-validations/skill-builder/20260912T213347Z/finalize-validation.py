import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
ROOT=Path('C:/Projects/DevForgeAI'); RUN=Path(__file__).parent; RID=RUN.name
VALIDATOR=ROOT/'.agents/skills/skill-validator'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(RUN).as_posix(),'sha256':h(p)}
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def command(folder,argv):
    folder.mkdir(parents=True,exist_ok=True)
    start=dt.datetime.now(dt.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',cwd=ROOT,timeout=120)
    (folder/'attempt-001.stdout.txt').write_text(p.stdout,encoding='utf-8');(folder/'attempt-001.stderr.txt').write_text(p.stderr,encoding='utf-8')
    save(folder/'attempt-001.json',{'argv':argv,'cwd':str(ROOT),'start':start,'end':dt.datetime.now(dt.timezone.utc).isoformat(),'exit':p.returncode})
    return p

def finish():
    cold=json.loads((RUN/'trials/cold-spec/readback-review.json').read_text());routing=json.loads((RUN/'trials/routing/readback.json').read_text())
    assert cold['status']=='PASS' and routing['status']=='PASS'
    readback=command(RUN/'trials/final-source-readback',['python','-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(ROOT/'src/agents/skills/skill-builder'),'--manifest',str(RUN/'source-manifest.json')])
    assert readback.returncode==0
    observed=json.loads(readback.stdout);assert observed['status']=='MATCH'
    save(RUN/'source-after-manifest.json',observed['manifest'])
    original_spec=ROOT/'docs/plan/skill-validations/skill-builder/20260912T161842Z/revision-spec.md'
    assert h(original_spec)==h(RUN/'inputs/prior-validation/revision-spec.md')=='9b8570392db9ed2128a71d820ba3710f58a000749db3f0ca0b780e33da28248c'
    sources=json.loads((RUN/'sources.json').read_text())
    for source in sources['sources']:assert h(RUN/source['snapshot_path'])==source['sha256']
    save(RUN/'trials/final-source-readback/input-readback.json',{'schema_version':'1','status':'UNCHANGED','original_spec_sha256':h(original_spec),'rule_set_sha256':h(RUN/'rule-set.json'),'source_count':len(sources['sources']),'guidance_local_captures_unchanged':True,'remote_pages_retrieved_again':False})
    origin=json.loads((RUN/'origin-record.json').read_text());origin['source_readback_state']='UNCHANGED';save(RUN/'origin-record.json',origin)
    findings={'schema_version':'1','run_id':RID,'target_name':'skill-builder','findings':[],'prior_finding_resolution':ref(RUN/'finding-resolution.json')};save(RUN/'findings.json',findings)
    (RUN/'enforcement-recommendations.md').write_text('# Enforcement recommendations\n\nNo new enforcement candidate is proposed for this wording-only correction. Existing instructions accurately separate ordinary editable evidence, host task assignments and Python observations from future compiled-Rust authority. Independent trials demonstrate bounded workflow behavior, not protected mutation, enforced isolation, installation or qualification. Existing future design remains outside this assessment.\n',encoding='utf-8')
    specs=[
    ('C01','SB-FORMAT','standards','deterministic',True,'applicable','PASS','Fresh structure helper and installed Skill Creator checker both exit 0; 42 local links including the corrected section anchor resolve. Metadata and original target name agree.',['trials/structure/attempt-001.stdout.txt','trials/installed-checker/attempt-001.stdout.txt']),
    ('C02','SB-DISCLOSURE','standards','semantic',True,'applicable','PASS','Entrypoint exposes operation, contract, candidate, evaluation and delivery decisions; relevant conditional details have explicit links. Optional host metadata is not required.',['source/SKILL.md','source/references/spec-build.md','workflow-map.json']),
    ('C03','SB-WORKFLOW','workflow','semantic',True,'applicable','PASS','Freshly traced operation paths have concrete inputs, outputs, branch/failure routes and terminal user outcomes; adopted custody remains distinct from quality and revision permission.',['workflow-map.json','source/references/adoption.md','source/references/regeneration.md']),
    ('C04','SB-CUSTODY','workflow','deterministic',True,'applicable','PASS','All 36 delivered rows match the published generated origin; contract and pointer hashes match. Three same-session published revision results rehashed against 616 measured input entries.',['trials/delivery-identity/observation.json','trials/delivery-identity/profile-readback.json','inputs/build/delivery-audit.json']),
    ('C05','SB-CONSISTENCY','instructions','semantic',True,'applicable','PASS','Prior finding is resolved by the exact approved summary reference; all four detailed trial families and separate routing remain byte-identical and required when applicable.',['finding-resolution.json','trials/delta/observation.json','source/references/evaluation.md']),
    ('C06','SB-AUTONOMY','instructions','semantic',True,'applicable','PASS','Existing authorization is reused; essential missing decisions stop dependent work; explicit evidence requirements and review boundaries remain useful instructions without fictitious enforcement.',['trials/semantic/ceremony-review.json','source/references/conversion-rules.md','source/assets/worker-task-template.md']),
    ('C07','SB-BEHAVIOR','behavior','historical_evidence_readback',True,'applicable','PASS','Same-session revision delivery evaluation supports exact delivered bytes; fresh cold build and routing are recorded separately. Older broad enhancement campaigns are not relabeled as current execution.',['trials/delivery-identity/profile-readback.json','inputs/build/published-results.jsonl']),
    ('C08','SB-COLD','behavior','behavioral',True,'applicable','PASS','Independent cold minimal-input builder task completed a disposable specification build with actual required checks and delivered readback; prompt excluded corrections and expectations.',['trials/cold-spec/plan.json','trials/cold-spec/readback-review.json','trials/cold-spec/final-response.txt']),
    ('C09','SB-NATIVE','behavior','behavioral',False,'applicable','NOT_RUN','Native implicit discovery/activation was not exercised. Explicit file loading and independent classification do not establish native selection.',['trials/routing/plan.json']),
    ('C10','SB-MODEL','instructions','semantic',False,'not_applicable','NOT_APPLICABLE','No API-backed or model-specific component was added; no fixed model/API parameter requirement applies.',['source/SKILL.md']),
    ('C11','SB-DELTA','instructions','deterministic',True,'applicable','PASS','Only exact reporting row and its corresponding manifest digest differ; all other 34 files, profile/schema/grader/script/test bytes and detailed workflow remain unchanged.',['trials/delta/observation.json','inputs/prior-validation/revision-spec.md']),
    ('C12','SB-ROUTING','behavior','behavioral',True,'applicable','PASS','Independent classifier matched nine predeclared positive and near-miss routes; explicit routing-adoption-v1 evaluator passed with exact frozen inputs/cases.',['trials/routing/plan.json','trials/routing/readback.json','trials/routing/evaluation-results.jsonl']),
    ('C13','SB-RECORDS','workflow','deterministic',True,'applicable','NOT_RUN','Final source/specification/rule capture readback matches; records integrity helper remains to execute.',['trials/final-source-readback/attempt-001.stdout.txt','trials/final-source-readback/input-readback.json'])]
    checks=[]
    for cid,rule,dimension,method,required,app,result,reason,paths in specs:
        checks.append({'schema_version':'1','run_id':RID,'check_id':cid,'rule_id':rule,'subject_path':'SKILL.md','method':method,'required':required,'applicability':app,'result':result,'reason':reason,'evidence':[ref(RUN/p) for p in paths],'dimension':dimension})
    def save_checks():(RUN/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks),encoding='utf-8')
    save_checks()
    draft=command(RUN/'trials/records-initial',['python','-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(RUN)])
    if draft.returncode:print(draft.stdout);raise RuntimeError('Initial records error retained')
    checks[-1]['result']='PASS';checks[-1]['reason']='Actual source/spec/rule capture readbacks match; initial records helper returned no integrity errors. Final records run will verify completed report/handoff references.';checks[-1]['evidence'].append(ref(RUN/'trials/records-initial/attempt-001.stdout.txt'));save_checks()
    required=[x for x in checks if x['required'] and x['applicability']=='applicable']
    dims={d:'PASS' for d in ('standards','workflow','instructions','behavior')}
    save(RUN/'assessment.json',{'schema_version':'1','run_id':RID,'target_name':'skill-builder','assessment_completed':True,'overall_assessment':'PASS','dimensions':dims,'required_evaluated':len(required),'required_total':len(required),'unknown_applicability':0,'native_implicit_activation':'NOT_RUN','builder_readiness':'NO_CHANGE','rule_set_sha256':h(RUN/'rule-set.json'),'package_digest':observed['manifest']['package_digest'],'review_type':'Independent assessor; cold builder and routing workers independent of assessor. This is not validator self-review.'})
    coldsummary=cold['summary']
    report=f'''# Fresh skill-builder revalidation

**PASS for the selected bounded assessment; assessment_completed: true.** All {len(required)}/{len(required)} applicable required checks in rule set `{h(RUN/'rule-set.json')}` passed for package `{observed['manifest']['package_digest']}`. Builder readiness is **NO_CHANGE**; no further revision proposal or approval is required. These results are development observations, not framework acceptance.

The prior finding `F-8c43eca6259d05a2153068b5d5b29495d0c208229c2a19f49bc71355d8df2d1f` is **resolved**. The reporting row now links to all applicable independent forward trials. Exact byte comparison verifies that the detailed four-family contract and separate routing remain unchanged. [Finding resolution](finding-resolution.json), [exact delta](trials/delta/observation.json).

## Origin and preservation

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`. Run: `{RID}`. All 36 permitted files are retained without exclusions in [source/](source/SKILL.md) and [source manifest](source-manifest.json). The final [readback](trials/final-source-readback/attempt-001.stdout.txt) matches actual delivered bytes; original approved specification and saved rule-source hashes remain unchanged.

History is now verified **generated**, following the explicit adopted unknown-history origin. The [origin record](origin-record.json) binds the [approved revision specification](inputs/prior-validation/revision-spec.md) and exact [generated provenance](inputs/build/published/revision/evidence/build-provenance.json). Its contract, pointer and delivered rows agree. Three published revision-spec-v2 records were rehashed against 616 measured input entries in [profile readback](trials/delivery-identity/profile-readback.json). These are verified same-session delivery checks, not new evaluator invocations by this validation task. Historical enhancement receipts were not promoted to provenance.

## Assessment dimensions

| Dimension | Result | Required coverage |
| --- | --- | --- |
| Standards | PASS | 2/2 |
| Workflow | PASS | 3/3 |
| Instructions | PASS | 3/3 |
| Behavior | PASS | 3/3 |
| Enforcement recommendations | No new candidate | Descriptive only |

The fresh installed Skill Creator checker exited 0. The separate validator structure helper exited 0 and checked 42 links, including the new section link. Semantic review traced all operation and recovery paths, resource routing, examples and permission/evidence boundaries. [Checks](checks.jsonl), [workflow map](workflow-map.json), [contextual instruction review](trials/semantic/ceremony-review.json), [findings](findings.json).

Live official [OpenAI Build Skills](https://learn.chatgpt.com/docs/build-skills) and [Agent Skills specification](https://agentskills.io/specification) guidance was fetched and retained before checks. Required metadata and format constraints are distinguished from recommendations and project policy; optional folders, host metadata and fixed model/API settings were not invented as requirements. See [sources](sources.json) and [pinned rules](rule-set.json). Existing project specifications are exact retained inputs; live coverage is limited to the two retrieved sources.

## Fresh trials and limits

The independent cold worker received only the selected builder snapshot, a small approved task-card specification, outcome and disposable write scope; expected outcomes and the correction were withheld. {coldsummary} [Plan and exact prompt](trials/cold-spec/plan.json), [worker result](trials/cold-spec/final-response.txt), [independent artifact readback](trials/cold-spec/readback-review.json). This demonstrates actual builder workflow execution; it is not native implicit activation or an exhaustive guarantee about generated-skill behavior.

A separate independent classifier matched all nine predeclared import, specification-build, regeneration, adoption, validation-only, explanation, specification-authoring, installation and unrelated-edit cases. The actual `routing-adoption-v1` evaluator passed with retained package/input/case snapshots. [Routing plan](trials/routing/plan.json), [observations](trials/routing/observed.jsonl), [evaluation](trials/routing/evaluation-results.jsonl), [readback](trials/routing/readback.json).

The four-family substantive-enhancement campaign remains required when applicable, but was not repeated for this wording-only change. Fresh execution here covers a minimal specification build and routing; current parent delivery covers adoption and first adopted-origin revision. Synthetic decimal import, conflict/resolution, later-generated revision and publication fault campaigns were not freshly rerun. Earlier retained enhancement evidence remains historical and is not claimed as current execution. Scripts, tests, profiles, schemas and grader versions are byte-identical, so no new regression campaign was required for this correction.

One assessor-only readback attempt failed because its parser expected a numeric schema summary, while the actual worker stdout contained ten individual JSONL observations. The failed script/streams remain under `trials/assessor-audit/` and `audit-trials.py`; distinct `audit-trials-attempt002.py` decoded all ten expected/observed pairs and passed. No target, cold-workflow evaluator or routing-evaluator failure was concealed or retried. The cold worker's `codex --version` returned 0 with retained access-denied warnings from automatic personal-temp cleanup/PATH-alias handling; no escalation or installation followed.

Native implicit activation, operational installation, Rust implementation/qualification and production acceptance remain **NOT_RUN/NOT_PERFORMED**. No target or operational copies were changed during validation; task write boundaries are ordinary instructions, not OS-enforced isolation. This assessment used an independent assessor and cold/routing workers; it is not validator self-review. No new enforcement mechanism is proposed. [Enforcement register](enforcement-recommendations.md).

## Delivery and next action

No open finding or further package change is proposed. [Handoff](handoff.json) records NO_CHANGE and the verified generated baseline. The final records-integrity output is retained at `trials/records-final/attempt-001.stdout.txt`; that helper checks bytes and record shapes, not semantic truth or future enforceability. [Command log](command-log.md).
'''
    (RUN/'validation-report.md').write_text(report,encoding='utf-8')
    save(RUN/'handoff.json',{'schema_version':'1','run_id':RID,'target_name':'skill-builder','original_target_root':str(ROOT/'src/agents/skills/skill-builder'),'target_package_digest':observed['manifest']['package_digest'],'original_manifest':ref(RUN/'source-manifest.json'),'origin':ref(RUN/'origin-record.json'),'proposed_spec':None,'findings':ref(RUN/'findings.json'),'report':ref(RUN/'validation-report.md'),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'not_needed','review_instruction':None,'builder_readiness':'NO_CHANGE','readiness_reasons':['Approved correction is delivered and prior finding resolved; no further change proposed.'],'baseline_kind':'generated','baseline_reference':ref(RUN/'inputs/build/published/revision/evidence/build-provenance.json'),'adoption_required':False,'adoption_capability':'available and prior explicit origin verified; no new adoption requested','permitted_target_root':str(ROOT/'src/agents/skills/skill-builder'),'preservation_requirements':['Preserve delivered source and historical evidence; no further package or operational mutations authorized by this handoff.']})
    final=command(RUN/'trials/records-final',['python','-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(RUN)])
    print(final.stdout)
    if final.returncode:raise RuntimeError('Final records error retained')
    save(RUN/'final-receipt.json',{'schema_version':'1','run_id':RID,'target_name':'skill-builder','assessment_completed':True,'overall_assessment':'PASS','builder_readiness':'NO_CHANGE','package_digest':observed['manifest']['package_digest'],'rule_set_sha256':h(RUN/'rule-set.json'),'report':ref(RUN/'validation-report.md'),'handoff':ref(RUN/'handoff.json'),'records_integrity':ref(RUN/'trials/records-final/attempt-001.stdout.txt'),'remaining_gaps':['Native implicit activation not run','Broad unchanged enhancement campaigns not freshly rerun; no new script/schema/profile behavior introduced','Rust qualification and operational installation not performed']})
if __name__=='__main__':finish()
