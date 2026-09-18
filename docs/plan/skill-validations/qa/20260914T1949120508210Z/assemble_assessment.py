"""Assemble independent manual review and retained observations, not acceptance."""
from bootstrap import ROOT, PROJECT, VALIDATOR, write, observe
from prepare_trials import ref, put
import datetime
import hashlib
import json
import re

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
meta=dict(schema_version='1',run_id=ROOT.name,target_name='qa')
source_manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
bindings=json.loads((ROOT/'input-bindings.json').read_bytes())

def source_ref(name):
    row=next(row for row in bindings if row['original_path'].endswith(name))
    return dict(path=row['snapshot_path'],sha256=row['sha256'])

def locate(path,phrase):
    lines=(ROOT/path).read_text(encoding='utf-8').splitlines()
    n=next(i for i,line in enumerate(lines,1) if phrase in line)
    return dict(line_start=n,line_end=n)

sources=json.loads((ROOT/'sources.json').read_bytes())
guidance=ROOT/'inputs/openai-guidance-retrieval.json'
sources['sources'].append(dict(source_id='openai-live',url='https://learn.chatgpt.com/docs/build-skills',retrieved_at_utc=now,sha256=ref(guidance)['sha256'],snapshot_path=ref(guidance)['path'],sections=['Required SKILL.md metadata','How ChatGPT and Codex use skills','Optional metadata','Best practices'],freshness='live_verified'))
write(ROOT/'sources.json',sources)
put(ROOT/'rule-binding-note.md','The AV and 42 scenario expectations were pinned before structural/native execution. A later source-ID correction changed only the two scenario source identifiers from the generic qa-contract label to their corresponding registered specification IDs. The original is retained in inputs/rule-set-original.json. No expected result, required classification or applicability changed. Live OpenAI retrieval corroborates format and routing observations; it does not introduce new rules mid-run.\n')

write(ROOT/'origin-record.json',dict(**meta,original_source_root=str(PROJECT/'src/agents/skills/qa'),manifest=ref(ROOT/'source-manifest.json'),specification=source_ref('qa-skill-postmvp-spec.md'),origin_kind='existing_spec',history_kind='observed',prior_evidence=None,completeness='complete',uncertainties=['Schema-1 observed history does not encode authoring-v1 custody; separate supplemental authoring context preserves the bound AUTHORED record.','No previous quality result is reused for changed bytes.'],source_readback_state='NOT_RUN',historical_origin='Authored custody established by current packet; not adopted or legacy generated.'))

# Requirement locators are generated for navigation. The following conclusions
# are the primary validator's semantic review, not token-scan judgments.
mapping=[]
for prefix,count in [('QA',26),('QAP',14)]:
    for number in range(1,count+1):
        rid=f'{prefix}-{number:03d}'
        locations=[]
        for item in source_manifest['files']:
            path='source/'+item['path']
            if not path.endswith('.md'): continue
            for line_no,line in enumerate((ROOT/path).read_text(encoding='utf-8').splitlines(),1):
                if re.search(r'(?<![A-Z0-9-])'+rid+r'(?!\d)',line):
                    locations.append(dict(**ref(ROOT/path),locator={'line_start':line_no,'line_end':line_no}))
        mapping.append(dict(requirement_id=rid,locations=locations,static_review='Contract reconciled against selected MVP plus explicit extension precedence. Instructions preserve required behavior; runtime performance remains unproven.'))
write(ROOT/'requirement-map.json',dict(**meta,requirements=mapping,scope='Static semantic conformance, not executed scenario acceptance'))

steps=[
 ('mode','SKILL.md','Default to **run**','Explicit product specs/project and current user intent','Resolve run versus explicit plan/execute/retest; do not promote plan intent','Invocation intent and selected scope','intake','Missing material scope -> request only that decision; independent safe work continues'),
 ('intake','references/intake-planning.md','**QA-003','Selected project/specs and applicable rules','Read sources, inspect host/tools, bind candidate including dirty bytes and literal output root','Candidate/input manifests; scope; per-check prerequisite inventory','plan','Unresolved identity/oracle/permission blocks dependents, not independent cases'),
 ('plan','references/intake-planning.md','**QAP-003','Requirements and candidate identity','Inventory criteria, independent oracles, dependencies, preparation and complete metric scopes; consume test-plan template and read back','READY or NEEDS_INPUT plan with bound paths','integrity','Plan write/readback failure remains explicit; planning-only ends at reporting'),
 ('integrity','references/execution-integrity.md','**QAP-005','Selected tests/source and evidence processors','Resolve imports/aliases, inspect gaming and later QA helpers before use','Bound integrity findings or omissions','execution or stop','Confirmed mocking/gaming -> whole-run stop; unresolved region blocks dependent claims'),
 ('execution','SKILL.md','3. For run','Bound read-back plan, integrity inspection, ready effects','Automatically prepare and execute ready cases in same invocation, preserve candidate and all attempts','Raw test/coverage receipts, launches, outputs and cleanup state','classify','Harness/prerequisite gaps localized; no repair of product/developer tests'),
 ('classify','references/execution-integrity.md','**QAP-006','Observed issue with demonstrated impact','Classify integrity/metric/critical/ordinary/safety/gap/advisory and record trigger','Issue class, evidence, dependents and ordered decision','stop or execution or assess','Uncertain critical impact -> contain as safety blocker; do not invent product defect'),
 ('stop','references/execution-integrity.md','**QAP-008','Confirmed whole-run terminal trigger','Launch no more tests/builds/reproductions; safely contain known owned in-flight work','Retained attempts, remaining NOT_RUN obligations and observed cleanup','assess','Unknown ownership prohibits unsafe cleanup; preserve uncertainty'),
 ('assess','references/assessment.md','**QAP-007','Raw evidence bound to complete collection scopes','Compute exact complete metrics; distinguish incomplete measurements; apply per-platform floors and FAIL precedence','Separate execution status and product verdict; explicit plan NOT_EVALUATED','report','Missing/partial measurement prevents PASS; no fabricated percentage or rounding'),
 ('report','references/reporting-handoff.md','**QA-020','Observed verdict and all findings/gaps','Consume report/fix templates; bind actual output paths; external mutually referenced hash manifest; read back','Actual report; fix packet on FAIL; external manifest; checkpoint','handoff','Write/readback failure reported in conversation at original destination; verdict retained'),
 ('handoff','references/reporting-handoff.md','**QA-024','Delivered outputs or honest delivery failure','Verify dev discovery and supply resolved manual owner-specific conversation prompt','Usable user handoff; no automatic repair/install/deploy','terminal','Unavailable dev -> preserve fix and state discovery prerequisite'),
 ('resume','references/reporting-handoff.md','**QAP-013','Later explicit resume or corrected-candidate retest selection','Recheck identities/effects/tools/owned state; preserve old plans and attempts; revise legacy plan only as needed','Bound next action or independent retest closure','intake or terminal','Drift invalidates affected evidence; no automatic terminal-FAIL retry or plan-to-run promotion')
]
workflow=[]
for sid,path,phrase,entry,action,output,next_step,failure in steps:
    p='source/'+path
    workflow.append(dict(step_id=sid,entrypoint=dict(**ref(ROOT/p),locator=locate(p,phrase)),entry_conditions=entry,inputs=entry,executor='Codex CLI agent using terminal/files',action=action,outputs=[output],completion_evidence='Actual bound artifact/readback or retained observation; see native-observations.json for executed limits',next_branch_targets=[next_step],failure_route=failure,terminal_user_outcome='Outcome-specific report, owner and grounded next action; no protected acceptance'))
write(ROOT/'workflow-map.json',dict(**meta,steps=workflow))

ceremony=[]
for path,phrase,effect in [
 ('SKILL.md','Launch no further tests','Stop conditions constrain actual subsequent launches; retained as useful guidance, with native completion unproven.'),
 ('references/reporting-handoff.md','Do not emit `TODO`','Prevents unresolved placeholders in delivered prompts; TODO occurrence is an example of forbidden output, not unfinished instructions.'),
 ('references/assessment.md','Both',None),
 ('references/execution-integrity.md','Text search alone','Requires contextual import/alias inspection and honest unresolved regions, not a keyword-only absence claim.')]:
    if effect is None: continue
    p='source/'+path
    loc=locate(p,phrase)
    excerpt=(ROOT/p).read_text(encoding='utf-8').splitlines()[loc['line_start']-1]
    ceremony.append(dict(path=p,locator=loc,excerpt=excerpt,classification='useful_instruction',intended_effect=effect,disposition='preserve',evidence=[ref(ROOT/p)]))
write(ROOT/'semantic-review.json',dict(**meta,reviewer='Primary validator; independent of builder authoring. Validator-written grader self-review is separately labelled.',conclusions=[
 'All nine captured files read in full. The entrypoint routes to all four references and all three templates; metadata is the discovery root.',
 'All twenty package links resolve; no unsupported anchors or unreferenced resources. Optional configuration uses documented interface string fields and preserves default implicit invocation.',
 'The TODO warning is a forbidden-output example; bracketed asset text is consumed template slots with explicit filling instructions, not abandoned scaffolding.',
 'QAP precedence removes ordinary planning-only defaults while retaining explicit planning mode. Aggregate NEEDS_INPUT permits independent READY checks.',
 'Stop classification preserves ordinary-defect continuation, terminal integrity/complete-metric/critical stops, and localized prerequisite/safety behavior.',
 'Metric completeness and per-platform qualification are coherent across assessment and templates; no early partial percentage can become terminal metric failure.',
 'Literal destination and external final manifest instructions avoid silent path substitution and circular hashes.',
 'No runtime executable helper, required external service, model override, fixed application stack, persistent installation or claimed compiled-Rust authority was introduced.',
 'Instructions declare effects and preserve source/old attempts; hostile-data behavior and full native effects still need completed trials.',
 'No source change is justified by the observed static review or incomplete native traces. Size and duplication alone do not establish a defect.'
 ],ceremonial_candidates=ceremony,security_limit='Bounded instruction/effect review only; no exhaustive security audit or native hostile-input success is claimed.'))

native=[]
for cid in ['QPV-01','QPV-02','QPV-06']:
    folder=ROOT/'trials'/cid
    trial_attempts=[]
    for receipt in sorted(folder.glob('attempt-[0-9][0-9][0-9].json')):
        value=json.loads(receipt.read_bytes())
        event_file=folder/value['stdout']
        events=[json.loads(line) for line in event_file.read_text(encoding='utf-8').splitlines() if line.strip()]
        messages=[dict(sequence=i,text=e['item']['text']) for i,e in enumerate(events) if e.get('item',{}).get('type')=='agent_message']
        commands=[dict(sequence=i,command=e['item']['command'],exit_code=e['item'].get('exit_code')) for i,e in enumerate(events) if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        before=json.loads((folder/'before.json').read_bytes())
        after=json.loads((folder/f'attempt-{value["attempt_id"]}.after.json').read_bytes())
        trial_attempts.append(dict(receipt=ref(receipt),events=ref(event_file),timed_out=value['timeout'],exit_code=value['exit_code'],messages=messages,completed_commands=commands,fixture_file_set_unchanged=before['files']==after['files'],final_artifact_present=(folder/'project/.trial-output/final.txt').exists()))
    native.append(dict(case_id=cid,attempts=trial_attempts,whole_scenario='NOT_RUN',reason='No completed native workflow and artifact delivery within 120-second case limit. Initialization failure and timeout retained, not counted as skill defects.'))
write(ROOT/'native-observations.json',dict(**meta,trials=native,interpretation='QPV-06 trace explicitly identifies direct and resolved-alias mocking and announces pre-execution stop. No post-stop command or test launch appears before timeout. This is partial stop evidence, not complete reporting or scenario PASS.',remaining_scope='39 scenario IDs not separately attempted; all 42 remain unqualified. Native discovery, resume/retest, portability pair, metric/live-operation variants and hostile-data behavior remain unperformed. The three feasibility pilots timed out; no assertion that unattempted cases are intrinsically impossible.'))

# Preserve exact independent routing output separately from expected labels.
decisions=[('P1','SELECT','Independent QA against an explicitly selected specification and candidate matches the described scope.'),('P2','SELECT','Planning QA for selected sprint stories fits the planning scope, with execution excluded by the request.'),('P3','SELECT','Selected defect retests against a corrected candidate are explicitly included.'),('P4','SELECT','Auditing first-party tests for gaming against product requirements is test-integrity review.'),('P5','DO_NOT_SELECT','Feature implementation is development work outside independent product QA.'),('P6','DO_NOT_SELECT','Skill-package validation is explicitly identified as a separate task.'),('P7','DO_NOT_SELECT','Skill installation is explicitly identified as a separate task.'),('P8','DO_NOT_SELECT','Production deployment is explicitly identified as a separate task.'),('P9','DO_NOT_SELECT','Standalone architecture research is explicitly identified as a separate task.'),('P10','DO_NOT_SELECT','Repairing reported product bugs is explicitly outside this QA skill\'s scope.')]
write(ROOT/'routing-observation.json',dict(**meta,executor='Independent description-only agent /root/routing; no package body or expected labels supplied',results=[dict(prompt_id=i,decision=d,reason=r) for i,d,r in decisions],matched_expected=10,total=10,native_implicit_activation='NOT_RUN',limitation='Predeclared labels were independent of the classifier output; routing-plan.json was persisted after classifier launch, so chronological file-order alone does not prove pre-registration.'))

supp=ROOT.parent/(ROOT.name+'-supplemental')
supp.mkdir(exist_ok=True)
raw=json.loads((ROOT/'observations/text-resources.stdout').read_bytes())['observations']
for node in raw['resources']:
    node['role']='template' if node['path'].startswith('assets/') else 'reference' if node['path'].startswith('references/') else 'runtime'
    node['usage']='used'
    node['evidence']=[dict(path=str(ROOT/'source'/node['path']),sha256=hashlib.sha256((ROOT/'source'/node['path']).read_bytes()).hexdigest())]
    node['reason']='Consumed through entrypoint/reference graph or host metadata; manually reviewed.'
write(supp/'adaptive-observations.json',dict(schema_version='adaptive-observations-v1',run_id=ROOT.name,target_digest=source_manifest['package_digest'],unicode_candidates=raw['unicode_candidates'],resources=raw['resources'],edges=raw['edges'],context=raw['context'],bindings=[],limitations=['Ordinary skill; adaptive-only rules inapplicable.','Tokenizer encoding unavailable locally; no download.','Native execution remained incomplete.']))
write(supp/'authoring-context.json',dict(**meta,history_kind='authored',packet_bound=True,assessment_scope='Current authored bytes, not adopted/legacy generated baseline',authoring_record=dict(path=str(ROOT/source_ref('authoring-record.json')['path']),sha256=source_ref('authoring-record.json')['sha256']),adoption_required=False,baseline_quality='NOT_INFERRED'))

put(ROOT/'enforcement-recommendations.md','# Future enforcement recommendations\n\nNo new enforcement candidates are proposed in this run. The selected package already distinguishes QA evidence from protected compiled-Rust authority. Observed instruction-level stop rules are not claimed to be enforced gates. Native workflow coverage is incomplete; adding hooks or runtime policy to make this assessment pass would expand the selected task. Preserve current guidance and the separate supplied Rust design. No implementation, installation or acceptance is claimed.\n')
print('Static review, workflow map, native trace analysis and supplemental records assembled.')
