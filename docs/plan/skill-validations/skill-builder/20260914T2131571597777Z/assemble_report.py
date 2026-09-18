"""Assemble actual observations, explicit gaps and review-only findings."""
import ast
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from prepare_validation import ROOT,PROJECT,VALIDATOR,put,ref,sha,command

def read(path):return json.loads((ROOT/path).read_bytes())
def source_ref(path,source_id,locator):return dict(**ref(path),source_id=source_id,locator=locator)
manifest=read('source-manifest.json')
# Required final readback on original bytes; stdout is retained complete.
response=command('source-readback',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(PROJECT/'src/agents/skills/skill-builder'),'--manifest',str(ROOT/'source-manifest.json')])
value=json.loads(response.stdout)
put('source-after-manifest.json',value['manifest'])
origin=read('origin-record.json');origin['source_readback_state']='UNCHANGED' if response.returncode==0 else 'SOURCE_CHANGED';put('origin-record.json',origin)
readbacks=[]
for s in read('sources.json')['sources']:
    if 'original_path' in s:
        readbacks.append({'source_id':s['source_id'],'expected_sha256':s['sha256'],'actual_sha256':sha(s['original_path']),'unchanged':sha(s['original_path'])==s['sha256']})
put('observations/input-readback.json',{'sources':readbacks,'official_saved_content_unchanged':sha(ROOT/'guidance/openai-build-skills.md')==next(s['sha256'] for s in read('sources.json')['sources'] if s['source_id']=='openai-skills')})

package=ROOT/'source'
artifacts=read('source/package-manifest.json')['artifacts']
static={'manifest_mismatches':[p for p,h in artifacts.items() if sha(package/p)!=h], 'unlisted_files':sorted({r['path'] for r in manifest['files']}-set(artifacts)-{'package-manifest.json'}),'python_files':[],'json_files':[],'utf8_files':len(manifest['files'])}
for row in manifest['files']:
    p=package/row['path']
    if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'));static['python_files'].append(row['path'])
    if p.suffix=='.json':json.loads(p.read_bytes());static['json_files'].append(row['path'])
put('observations/static.json',static)

coverage_files=[read('observations/independent-tests/coverage.json'),read('observations/regressions/coverage.json')]
coverage_rows=[]
for name, item in coverage_files[0]['files'].items():
    same=[c['files'][name] for c in coverage_files]
    executable=set(item['executed_lines'])|set(item['missing_lines'])
    covered=set().union(*(set(v['executed_lines']) for v in same))
    branches=set(map(tuple,item['executed_branches']+item['missing_branches']))
    seen=set().union(*(set(map(tuple,v['executed_branches'])) for v in same))
    coverage_rows.append({'path':name,'covered_lines':len(covered),'executable_lines':len(executable),'covered_branches':len(seen),'branches':len(branches)})
totals={k:sum(v[k] for v in coverage_rows) for k in ['covered_lines','executable_lines','covered_branches','branches']}
totals['line_percent']=100*totals['covered_lines']/totals['executable_lines']
totals['branch_percent']=100*totals['covered_branches']/totals['branches']
put('observations/coverage-summary.json',dict(platform='Windows',files=coverage_rows,totals=totals,exclusions='Zero first-party lines excluded; tests/evaluator are outside source denominator.',limits='Union of instrumented independent and custody regression execution. Uninstrumented subprocess/adaptive/native execution receives no credit. Linux coverage NOT_RUN.',result='PASS' if totals['line_percent']>=95 else 'FAIL'))

put('observations/routing.json',{'reviewer':'Independent /root/routing agent; description only; no files or tools','classifications':{f'R{i}':('DO_NOT_ACTIVATE' if i in [3,4,6,9] else 'ACTIVATE') for i in range(1,13)},'observed_match':'12/12 intended classifications','limitation':'No native implicit activation observation. Expected labels were selected by primary before request but not separately persisted before the reviewer returned; advisory routing evidence only.'})
textobs=read('observations/text-resources/stdout.txt')['observations']
put('observations/context-summary.json',{'files':len(textobs['context']['files']),'bytes':sum(x['bytes'] for x in textobs['context']['files']),'characters':sum(x['characters'] for x in textobs['context']['files']),'lines':sum(x['lines'] for x in textobs['context']['files']),'tokenizer':None,'tokens':None,'unicode_candidates':textobs['unicode_candidates'],'assessment':'No universal context cap. Shared constraints reside in SKILL.md; substantial import/adaptive/schema detail is conditional. Native prompts read branch references; no completed total-load budget claimed.'})
resource_rows=[]
for r in manifest['files']:
    path=r['path']
    if path=='SKILL.md':consumer='Codex selected skill entrypoint'
    elif path.startswith('schemas/'):consumer='Custody script schema readers; schema-to-schema references; authoring/evidence contract documentation'
    elif path.startswith('scripts/'):consumer={'authoring.py':'authoring.md/evidence-format.md; begin/publish/read','adaptive.py':'adaptation.md; inspect/plan-set','build_evidence.py':'spec-build.md; selected source/provenance readers','custody.py':'authoring.py legacy history resolution','record_schema.py':'authoring.py and adaptive.py schema integrity','init_skill.py':'scaffolding.md new-package-only initialization','generate_openai_yaml.py':'scaffolding.md and init_skill.py metadata authoring'}[Path(path).name]
    elif path.startswith('references/'):consumer='SKILL.md branch routing and linked references; see raw graph edges'
    elif path=='package-manifest.json':consumer='External artifact identity/readback; intentionally not loaded for every authoring task'
    else:consumer={'authoring-design-template.json':'workflow-design.md before selected authoring','build-report-template.md':'authoring terminal report contract','conversion-report-template.md':'conversion-rules.md import accounting','worker-task-template.md':'spec-build.md only for required workers','skill-creator-license.txt':'scaffolding notice licensing','skill-creator-notice.md':'scaffolding.md source attribution','check_project_binding.py':'project-binding.md copied generic runtime for selected adaptive members'}[Path(path).name]
    resource_rows.append({'path':path,'consumer':consumer,'orphan_finding':False})
put('observations/resource-adjudication.json',{'resources':resource_rows,'unsupported_edges':'Raw deterministic graph retained; dynamic Python schema/import edges adjudicated by actual consumer references, not file counts.','placeholder_review':'Empty strings in the design template and bracketed worker/conversion templates are authoring slots explicitly requiring completion; quoted TODO/ceremony examples are not unfinished runtime behavior.'})
put('observations/ceremony-review.json',{'passages':[{'path':'source/SKILL.md','anchor':'Do not generate executable test campaigns during authoring.','classification':'useful_instruction','effect':'Preserve validator-owned evaluation.','disposition':'retain'},{'path':'source/references/workflow-design.md','anchor':'An open question preserves a gap, not permission to invent a product fact or present the dependent design as complete.','classification':'useful_instruction','effect':'Blocks dependent authoring on missing behavior decisions.','disposition':'retain'},{'path':'source/references/evidence-format.md','anchor':'All such records are editable custody evidence, not protected authority.','classification':'useful_instruction','effect':'Limits claimed trust. Does not waive SBP-011 local consistency checks.','disposition':'retain'}],'conclusion':'No defect based solely on MUST, repetition, headings, templates or future review boundaries.'})

steps=[
 ('intake','SKILL.md / Resolve the task','Current invocation','Select project, identity, destination and applicable branch','Bound inputs or precise missing decision','design; history; adoption; adaptive','Ask only for material missing information; independent scope may proceed'),
 ('history','references/regeneration.md','Existing selected package','Read known baseline and current; otherwise authorized observed change paths','Bound B/C/N inputs','design','Conflicting known history blocks affected edit'),
 ('design','references/workflow-design.md','Selected create/edit/import/specification behavior','Record observable outcomes, consumers, effects and independent challenge descriptions','External authoring-design-v1 and exact input refs','stage','Unresolved behavior decision blocks dependent authoring'),
 ('stage','references/authoring.md; scripts/authoring.py begin','Bound contract and optional selected design','Validate custody inputs; capture supplied/effective contract, before/candidate, origin and design evidence','STAGED with readback','candidate','Input rejection code 2; capture failure retained'),
 ('candidate','SKILL.md / Author the package','Successful staging and selected requirements','Write only authorized candidate paths; optional scaffolding and conditional resources','Candidate bytes','publish','Retain partial authoring; no generated execution'),
 ('publish','scripts/authoring.py publish','Candidate, original inputs and captured origin','Compare B/C/N, recheck sources/paths/design and write/read back target','Authoring record; baseline only after success','handoff','BLOCKED/PARTIAL with actual deltas; confirmed design-mode bypass finding'),
 ('handoff','references/validation-handoff.md','Successful delivered readback','Return literal target, source action, state, design references and packet/prompt','Manual validator request and unperformed obligations','terminal','Publication failure remains partial; absent validator does not block authoring'),
 ('adoption','references/adoption.md','Explicit custody-only request','Capture selected existing bytes and management scope without changing candidate','Distinct adopted-operation authoring evidence','handoff','Reject changed candidate or unresolved prior history'),
 ('adaptive','references/adaptation.md','Explicit propose/author_set/review_updates selection','Capture project facts; preserve exact membership/dependencies; per-member authoring; update proposals','Proposal or exact full_set/eligible_subset records','design; stage; handoff; terminal','Block required dependents, continue independent selected members; no inferred membership'),
 ('import','references/conversion-rules.md','Selected Claude input','Capture input bytes and dispositions; map only supported host semantics','Portable candidate plus import accounting','design; stage','Unsupported essential mapping remains a precise gap, no imported command execution')]
put('workflow-map.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',steps=[dict(step_id=i,entrypoint=entry,entry_conditions=cond,inputs=[cond],executor='Codex host following selected builder; Python custody where named',action=action,outputs=[output],completion_evidence=output,next_branches=nexts,failure_route=failure,terminal_user_outcome='Delivered source/manual handoff or explicit retained blocked/partial outcome') for i,entry,cond,action,output,nexts,failure in steps]))

anchor="if requested is False:\n        if 'design_capture_ref' in captured or capture_path.exists():\n            raise ValueError('conflicting legacy/design capture mode')\n        return None"
identity=['SBP-011','scripts/authoring.py',anchor,0]
fid='F-'+hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
finding=dict(finding_id=fid,identity=identity,rule_id='SBP-011',category='workflow_bug',severity='major',subject_path='scripts/authoring.py',locator={'line_start':287,'line_end':296},source_refs=[source_ref('inputs/skill-builder-postmvp-spec.md','postmvp','SBP-011; SBPV-11')],observation_refs=[ref('observations/independent-tests/results.jsonl'),ref('observations/linux-checks/results.jsonl'),ref('trials/independent/test_silent_legacy_downgrade/docs/plan/authoring/run1/publication-readback.json'),ref('source/scripts/authoring.py')],description='A design-enabled stage can publish as legacy after origin.design_capture_requested is changed to false, design_capture_ref and design-capture.json are removed, and the captured design is modified. recheck_design returns before binding/snapshot checks; Windows and Linux both returned AUTHORED and wrote successful publication-readback.',user_impact='Required design custody can be lost while a successful next baseline and handoff are published. This is a reproducible local consistency failure; editable evidence is not a protected security boundary.',proposed_correction='Bind exact origin/mode to an independent begin-time stage-integrity receipt and check it before any legacy/design dispatch; explicitly handle existing stages and retain no-design ordinary-input compatibility.',preserved_requirements=['Authoring-only boundary','Legacy no-design calls','Closed contract/request schemas','Raw-byte preservation','No protected authority claim'],verification_cases=['test_silent_legacy_downgrade on Windows and Linux','SBPV-11','REV-001 through REV-003'],disposition='proposed')
put('findings.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',findings=[finding]))

checks=[]
def check(ident,rule,result,reason,dimension='behavior',ev=(),app='applicable',required=True):
    checks.append(dict(schema_version='1',run_id=ROOT.name,check_id=ident,rule_id=rule,subject_path='SKILL.md' if not rule.startswith('SBPV') else 'scenarios/'+rule,method='deterministic' if dimension=='standards' else 'behavioral' if dimension=='behavior' else 'semantic',required=required,applicability=app,result=result,reason=reason,evidence=[ref(p) for p in ev],dimension=dimension))
for rule in read('rule-set.json')['rules']:
    ident=rule['rule_id']
    if ident.startswith('SBP-'):continue
    if rule['applicability']=='not_applicable':check(ident,ident,'NOT_APPLICABLE',rule['limitation'],'standards' if ident=='AV-F04' else 'workflow',app='not_applicable');continue
    dim='standards' if ident.startswith(('AV-F','AV-R','AV-U','AV-C','AV-E')) else 'instructions' if ident.startswith(('AV-I','AV-S')) else 'workflow'
    result='PASS';reason='Captured format, resource, contextual instruction or bounded custody observations support this rule within the retained scope.'
    ev=['observations/static.json','observations/resource-adjudication.json','observations/ceremony-review.json']
    if ident=='AV-F02':reason='Original source root ends in skill-builder and captured frontmatter name matches; source-named snapshot helper limitation manually resolved.'
    if ident=='AV-F03':ev=['observations/routing.json'];reason='Description matches authoring scope; advisory independent routing 12/12. Implicit native discovery unverified.'
    if ident=='AV-U01':ev=['observations/context-summary.json'];reason='Complete captured text scan reported zero Unicode candidates.'
    if ident=='AV-C01':ev=['observations/context-summary.json'];reason='Complete bytes/code-points/lines measured; no token budget or tokenizer selected.'
    if ident in ['AV-R03','AV-I04','AV-S01']:
        result='NOT_RUN';reason='Static/helper portions inspected; complete host workflow, correction/authorization or hostile-input behavior not qualified by timed-out cold producers.';ev=['trials/native-simple-002/attempt-001.json','trials/native-branching-002/attempt-001.json']
    if ident in ['AV-W01','AV-W02','AV-S02']:
        result='FAIL';reason='Design-enabled stage can silently downgrade and publish despite changed captured design; other native branches remain unperformed.';ev=['observations/independent-tests/results.jsonl','observations/linux-checks/results.jsonl'];dim='behavior' if ident=='AV-W02' else dim
    if ident in ['AV-A06','AV-A07','AV-A08']:ev=['observations/adaptive-regressions/results.jsonl'];reason='Retained adaptive helper scenarios pass; no claim of completed native set generation.'
    if ident=='AV-E01':ev=['observations/input-readback.json','source-after-manifest.json'];reason='Direct source/spec identities and actual findings bound; full records helper and independent integrity audit reported separately.'
    check(ident,ident,result,reason,dim,ev)
for n in range(1,17):
    ident=f'SBP-{n:03d}'
    result='FAIL' if n==11 else 'NOT_RUN' if n in [15,16] else 'PASS'
    reason='Source instructions and relevant custody interfaces implement the selected contract; this static mapping does not substitute for the SBPV behavior ledger.'
    if n==11:reason='Required design evidence loss was not rejected after the origin mode downgrade; publication succeeded on both platforms.'
    if n in [15,16]:reason='Independent evaluation reached reporting, but full native generated-skill obligations and numeric qualification are incomplete; authoring maintenance evidence is separate.'
    check(ident,ident,result,reason,'workflow' if n in [10,11,12,14,16] else 'instructions',['source/SKILL.md','source/references/workflow-design.md','source/scripts/authoring.py'])
scenario={11:('FAIL','Design-mode downgrade reproduced on Windows and Linux.'),13:('PASS','Independent publication interruption retained actual first-file delta and no successful baseline.'),14:('PASS','71 retained custody regressions supported after one harness-path correction; 21 adaptive regressions passed; legacy no-design design-shaped input passed.'),15:('PASS','Unchanged loaded validator intake accepted the valid generated helper packet and rejected stale design source.'),16:('PASS','Real unchanged edit returned AUTHORED with no applied paths and explicit unchanged/unperformed reporting.'),17:('PASS','Independent fixtures/oracles authored from the selected specification; builder challenge data never scored as observed execution.')}
for n in range(1,19):
    result,reason=scenario.get(n,('NOT_RUN','Cold representative authoring did not deliver a package within its execution ceiling; complete selected observation remains unperformed. Static or helper portions do not qualify this scenario.'))
    if n==12:reason='Malformed shape/key/ID/path cases passed; exhaustive selected link/overlap and no-write coverage for the enhanced CLI is not complete.'
    check(f'SBPV-{n:02d}',f'SBPV-{n:02d}',result,reason,'behavior',['observations/independent-tests/results.jsonl','observations/regressions/results.jsonl','observations/adaptive-regressions/results.jsonl','observations/handoff-readback/result.json','observations/regression-schema-correction/result.json','trials/native-simple-002/attempt-001.json','trials/native-branching-002/attempt-001.json'])
check('QUALITY-WINDOWS-LINE','SBP-015','FAIL',f"Measured {totals['covered_lines']}/{totals['executable_lines']} first-party lines ({totals['line_percent']:.6f}%), below 95%.",'behavior',['observations/coverage-summary.json'])
check('QUALITY-LINUX-LINE','SBP-015','NOT_RUN','Linux first-party line coverage was not instrumented; targeted native custody execution does not supply coverage.','behavior',['observations/linux-checks/grade.json'])
check('NATIVE-IMPLICIT','AV-F03','NOT_RUN','Explicit cold source load is not native implicit activation.','behavior',required=False)
(ROOT/'checks.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in checks),encoding='utf-8')
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe
dimensions={d:observe.reduce_checks([c for c in checks if c['dimension']==d]) for d in observe.DIMENSIONS}
reduction=observe.reduce_checks(checks)
put('assessment.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',overall_assessment='FAIL',assessment_completed=True,dimensions=dimensions,required_coverage=reduction,unknown_applicability=0))
put('observations/quality-inventories.json',{'windows_helper_cases':{'required':127,'passing_after_documented_harness_corrections':126,'confirmed_product_failures':1,'raw_first_attempts':'Independent 33/35 plus regression 70/71 plus adaptive 21/21; two harness-only nonpasses retained, not product fixes.'},'windows_sbpv_scenarios':{'required':18,'passing':5,'failed':1,'not_run':12},'linux_custody_cases':{'required':35,'passing':34,'failed':1},'overall_declared_case_inventory':{'required':180,'passing':165,'pass_percentage':100*165/180,'note':'Each named case once; helper and complete scenario inventories separately identified. No retry count inflation. Linux full workflow/coverage unperformed.'}})
report=f'''# Skill-builder post-MVP validation

**FAIL** for package `{manifest['package_digest']}` against the selected [post-MVP specification](inputs/skill-builder-postmvp-spec.md). Assessment completed: true. Source readback: **{origin['source_readback_state']}**; all {len(manifest['files'])} files captured, no exclusions. No source repair or operational installation occurred.

## Confirmed finding

**Major: design-enabled publication can silently downgrade to legacy mode.** Changing `origin.json`'s mode to false, removing its capture binding/file, and altering the captured design still produced AUTHORED, a new baseline and successful publication readback. Reproduced with independent fixtures on Windows and Linux. This violates SBP-011/SBPV-11. The failure concerns local custody consistency; it is not a claim of protected security authority.

Stable finding: `{fid}`. See [full finding](findings.json), [Windows observations](observations/independent-tests/results.jsonl), [Linux observations](observations/linux-checks/results.jsonl), and the [actual successful publication after corruption](trials/independent/test_silent_legacy_downgrade/docs/plan/authoring/run1/publication-readback.json).

## Qualification and gaps

| Inventory | Outcome |
| --- | --- |
| Installed Skill Creator structural checker | Exit 0 |
| Validator structure observation | Exit 0 |
| Complete text/resource scan | No Unicode candidates; helper's source-directory naming uncertainty resolved against original bound path |
| Independent design custody, Windows | 34/35 supported after correcting one JSON-escaping assertion; 1 product failure |
| Retained custody regressions | 71/71 supported after correcting one copied-fixture schema path |
| Retained adaptive regressions | 21/21 passed |
| Independent design custody, Linux | 34/35 passed; same product failure |
| Required SBPV-01–18 | 5 PASS, 1 FAIL, 12 NOT_RUN/incomplete |
| Native implicit activation | NOT_RUN; explicit loading is different |
| Generated-skill execution | NOT_RUN: neither cold producer delivered a published package |

The original Windows attempts remain 33/35 and 70/71; [handoff assertion correction](observations/handoff-readback/result.json) and [schema-path correction](observations/regression-schema-correction/result.json) are separately retained. No product assertion was weakened, no failed product case was retried into a passing count, and no source was changed. The independent routing reviewer classified 12/12 intended prompts; expected labels were not separately persisted before the response, so this is advisory evidence only.

The full declared Windows first-party denominator is 2,264 executable lines across captured scripts and the generic runtime template, with zero first-party exclusions. Instrumented execution covered **{totals['covered_lines']}/{totals['executable_lines']} = {totals['line_percent']:.6f}%**. Branches: **{totals['covered_branches']}/{totals['branches']} = {totals['branch_percent']:.6f}%**. Uninstrumented execution receives no invented credit. This fails the 95% executed-line requirement. Linux line/branch coverage is NOT_RUN. See [coverage](observations/coverage-summary.json).

Windows helper cases are 126/127 (99.212598%) after separately documented harness corrections; complete SBPV scenarios are 5/18 (27.777778%). Linux targeted custody is 34/35 (97.142857%). The declared combined case inventory is 165/180 (91.666667%); [inventory definitions](observations/quality-inventories.json) keep the layers and prior attempts visible. Numeric floors do not waive the failed mandatory custody case or missing complete workflows.

## Cold trials and recovery

Each representative first attempt failed to initialize the local Codex client with Access denied, before model execution. Approved second attempts ran the installed Codex CLI with workspace-write, inherited configuration and a 120-second ceiling. [Simple](trials/native-simple-002/attempt-001.json) and [branching](trials/native-branching-002/attempt-001.json) trials both timed out; parent-owned taskkill returned 0 for each process tree. No timeout was increased and no timeout retry was performed. Exact prompts, events, stderr and before/after manifests are retained under trials.

Simple authoring retained the task capture, contract and design, but no staged/delivered package. Branching authoring retained native event observations but no authored output files. Partial discussions/designs are not completed SBPV scenarios. These ceilings are evaluation limits, not product performance requirements or proof that source caused the timeout. The next dependent action is fresh authorized cold producer execution followed by independent execution of its unmodified delivered skill. Do not fabricate consumer input from an evaluator-written package.

Linux checks ran with native Python 3.12.3 under Ubuntu at the verified `/mnt/c/Projects/DevForgeAI`, accessing the same selected Windows checkout. This bounded compatibility run did not switch to or qualify another checkout. Windows used Python 3.10.11. No tool/dependency installation occurred.

## Assessment dimensions and evidence

''' + '\n'.join(f"- {d}: **{v['outcome']}**, {v['required_evaluated']}/{v['required_total']} required checks evaluated." for d,v in dimensions.items()) + f'''

Required coverage: {reduction['required_evaluated']}/{reduction['required_total']}; unknown applicability: 0. [Checks](checks.jsonl) retain unperformed obligations under FAIL. Semantic assessment is by the primary validator, separate from builder maintenance; description routing used an independent agent. [Workflow map](workflow-map.json), [resource consumers](observations/resource-adjudication.json), [context counts](observations/context-summary.json), and [ceremony review](observations/ceremony-review.json) retain their limits. Templates and useful MUST/review instructions were not treated as defects merely for their wording.

Rules: `{sha(ROOT/'rule-set.json')}`. Official guidance was refreshed from [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) and retained in guidance; repository and SBP requirements remain distinct project policies. No API/model parameter requirements were imposed on this instruction-based skill. [Sources](sources.json), [origin](origin-record.json), [input readback](observations/input-readback.json) and [source after manifest](source-after-manifest.json) bind the observed bytes. Maintenance claims were inspected as history, not reused as fresh passes or a generated baseline.

## Proposed revision and next action

The [complete proposed revision](revision-spec.md) addresses the single custody finding with an independently bound internal stage-integrity receipt checked before branch selection. It preserves authoring-only scope and closed packet schemas, and explicitly proposes fresh linked runs for pre-revision staged records that cannot establish the new property. That compatibility choice requires review. No timeout-driven product redesign is proposed.

[Handoff](handoff.json) preserves pending proposal review and separate execution readiness. No legacy generated/adopted baseline is asserted; the supported observed-edit/skill-creator maintenance route is documented separately and does not require invented adoption. A repair must be a newly selected, narrowly scoped task followed by a fresh validation run. [Enforcement register](enforcement-recommendations.md) keeps protected authority in future compiled Rust.

Record-check outcomes and reference-audit limitations are in [record-integrity](record-integrity.md). These are evidence integrity observations, not semantic acceptance. Framework acceptance and installation: NOT_RUN.
'''
(ROOT/'validation-report.md').write_text(report,encoding='utf-8')
(ROOT/'enforcement-recommendations.md').write_text('''# Future enforcement recommendations

E-01 — proposed destination: devforgeai_cli (future compiled Rust only).

Trigger: a future protected authoring/publication request. Invariant: selected mode, source inputs and original stage identity cannot be replaced by editable status files. Inputs: independently authenticated selected contract/mode plus exact input and stage digests. Intended action: independently verify provenance, required evidence and permitted effects before authorizing mutation; reject missing/conflicting evidence and retain actual partial effects. Current evidence: the confirmed SBP-011 downgrade finding and editable-record limitations. No authority service/command is implemented or qualified by this validation.

Bypass limits: a new Python receipt provides local consistency only; a writer able to coherently replace all records remains outside that guarantee. Dependencies: separately implemented and qualified Rust authority, protected provenance and mutation boundary. Future verification: corrupt local mode/origin/capture records, including coherent rewrites, and prove the trusted selected contract prevents protected publication. Do not replace present custody safeguards before an authorized alternative exists. No hook/CI installation is proposed in this run.
''',encoding='utf-8')
put('handoff.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',original_target_root=str(PROJECT/'src/agents/skills/skill-builder'),original_manifest=ref('source-manifest.json'),origin=ref('origin-record.json'),proposed_spec=ref('revision-spec.md'),findings=ref('findings.json'),report=ref('validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='pending',review_instruction=None,builder_readiness='BLOCKED',readiness_reasons=['No selected verified legacy generated/adopted baseline for a schema-1 builder execution handoff. This does not prevent review or independently authorized skill-creator/observed-edit maintenance.','Review must explicitly select the proposed staged-run compatibility migration. No adoption is inferred.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='Authoring observed first edit and explicit adoption implementation inspected; no adoption requested or performed.',permitted_target_root=str(PROJECT/'src/agents/skills/skill-builder'),preservation_requirements=['Operational copies unchanged','Validator implementation unchanged','Source specs and historical evidence unchanged','Only a new selected repair may change development source']))
put('inputs/authoring-readiness-supplement.json',{'schema_version':'authoring-family-assessment-note','basis':'Observed scoped edit supported by current authoring/regeneration instructions; current manifest is an observation, not a fabricated generated baseline.','proposal_review_state':'pending','modern_maintenance_next_action':'Select exact proposed changes and compatibility migration; bind fresh observed target bytes for narrowly scoped skill-creator maintenance.','adoption_required':False,'quality':'FAIL; do not carry current results to changed bytes.'})
print(json.dumps({'finding_id':fid,'coverage':totals,'dimensions':dimensions,'required':reduction}))
