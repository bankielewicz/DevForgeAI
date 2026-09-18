"""Assemble actual observations into review artifacts, not acceptance authority."""
import collections
import copy
import json
from pathlib import Path
import re
from qa_harness import RUN,ROOT,TARGET,PRIOR,save,sha,inventory,now

def read(p): return json.loads(Path(p).read_bytes())
def ref(p,base=None): return {'path':Path(p).relative_to(base).as_posix() if base else str(Path(p).resolve()),'sha256':sha(Path(p).read_bytes())}
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')

MEM=RUN/'member-records'; SUP=RUN/'supplemental-records'; SUP.mkdir(exist_ok=True)
manifest=read(RUN/'target-before.json'); digest=manifest['package_digest']
spec=RUN/'inputs/skill-validator-adaptive-enhancement-spec.md'
specsha=sha(spec.read_bytes())
checks_raw=read(RUN/'commands/target-package-001/stdout.txt')
commands=[]
for directory in sorted((RUN/'commands').iterdir()):
    if (directory/'command.json').is_file(): commands.append({'attempt':directory.name,**read(directory/'command.json'),'stdout':ref(directory/'stdout.txt'),'stderr':ref(directory/'stderr.txt')})
save(RUN/'command-log.json',commands)
write(RUN/'command-log.md','# Exact commands and results\n\nEach argument vector below is executed without shell interpolation. Full streams and receipts are retained under commands/. Wrapper calls are not counted as additional test cases. Early exploratory reads and the initial metadata lookup failure remain in the session transcript.\n\n'+''.join('## '+c['attempt']+'\n\n```json\n'+json.dumps(c['argv'],ensure_ascii=False)+'\n```\n\nWorking directory: `'+c['cwd']+'`. Started '+c['started_at_utc']+'; ended '+c.get('ended_at_utc','unrecorded')+'; exit '+str(c.get('exit_status'))+'; '+c['termination']+'. [stdout](commands/'+c['attempt']+'/stdout.txt), [stderr](commands/'+c['attempt']+'/stderr.txt), [receipt](commands/'+c['attempt']+'/command.json).\n\n' for c in commands))

# No baseline reconstruction: verify retained original bytes independently.
baseline=inventory(PRIOR/'before-source'); delivered=inventory(PRIOR/'self-review/source')
save(RUN/'retained-snapshot-verification.json',{'baseline':baseline,'delivered':delivered,'expected_baseline':'77f0eec091cb41559074296ec8b0cd7dad76329ca6647b969f0e76b49cea51a4','expected_delivery':digest,'baseline_matches':baseline['package_digest']=='77f0eec091cb41559074296ec8b0cd7dad76329ca6647b969f0e76b49cea51a4','delivered_matches':delivered['package_digest']==digest})
specs={}
for p in (ROOT/'docs/plan/skill-validator-adaptive-enhancement-spec.md',ROOT/'docs/plan/skill-builder-adaptive-enhancement-spec.md'):
    specs[str(p)]={'sha256':sha(p.read_bytes()),'matches_capture':p.read_bytes()==(RUN/'inputs'/p.name).read_bytes()}
save(RUN/'selected-input-readback.json',{'specifications':specs,'target_digest':digest,'target_unchanged':read(RUN/'target-after.json')['files']==manifest['files'],'companion_unchanged':read(RUN/'companion-after.json')['files']==read(RUN/'companion-before.json')['files'],'loaded_unchanged':read(RUN/'loaded-evaluator-after.json')['files']==read(RUN/'loaded-evaluator-before.json')['files'],'prior_evidence_unchanged':read(RUN/'prior-evidence-after.json')['files']==read(RUN/'prior-evidence-before.json')['files'],'extent':'Exact bounded permitted inventories only; no whole historical tree or whole operational-home integrity claim.'})

definitions=[
 ('QA-01','AV-E01','scripts/adaptive_observe.py','integration_path = reader.absolute(value[\'integration_checks\'][\'path\'])','major','R06','Duplicate member/integration evidence inflates required coverage','A member check file is reused as integration_checks. All 29 A rows are counted twice; the helper accepts 87/87 instead of rejecting the shared artifact.','Track normalized identities across member and integration check artifacts; reject cross-role reuse before reduction. Preserve distinct legitimate integration rows.',['VA-003','VA-014','VAT-24']),
 ('QA-02','AV-A10','scripts/adaptive_observe.py',"contracts.require(any(row['subject_path'] == 'handoffs/'+handoff['id'] and row['required'] for row in integration), 'missing required integration coverage')",'major','R07','Required handoff can disappear through NOT_APPLICABLE','A full set declares a required A-to-B handoff, but its only integration row claims NOT_APPLICABLE. records accepts PASS at 58/58, omitting the required integration obligation.','Cross-check applicability against immutable required handoffs. Unknown or unexecuted required handoffs remain NOT_RUN and counted; reject contradictory NOT_APPLICABLE reductions.',['VA-003','VA-010','VA-014','VAT-05','VAT-18','VAT-24']),
 ('QA-03','AV-U01','scripts/text_resources.py',"nfkc = normalized != char and context in ('metadata','command','path')",'major','P08','Exact protocol identifier escapes NFKC candidate scanning','protocol.json contains schema_version with U+FF54 FULLWIDTH LATIN SMALL LETTER T in task-card-v1. The helper reports OBSERVED with no Unicode candidates. The exact protocol string differs, although normalization would change it.','Identify exact protocol identifiers in declared structured text and emit located unresolved NFKC candidates. Keep prose typography and fixtures contextual; do not normalize source or blanket-reject Unicode.',['VA-004','VAT-06']),
 ('QA-04','AV-R01','scripts/text_resources.py',"elif token[0] == fence[0] and len(token) >= len(fence):",'major','P07','Valid fenced example produces a false missing-resource failure','A backtick line with trailing nonspace text is treated as a closing fence. The literal link on the following code-content line is then reported as a missing local resource, producing MISMATCH for a valid example.','Recognize closing fences only with permitted trailing whitespace, retaining marker/length and line positions. Keep fenced links inert and preserve actual missing-link detection.',['VA-004','VA-005','VAT-08'])
]
findings=[]
for alias,rule,path,anchor,severity,case,title,observed,fix,reqs in definitions:
    lines=(TARGET/path).read_text(encoding='utf-8').splitlines()
    located=next(i for i,x in enumerate(lines,1) if x.strip()==anchor)
    identity=[rule,path,anchor,0]
    fid='F-'+sha(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode())
    findings.append({'finding_id':fid,'identity':identity,'rule_id':rule,'category':'resource_tool_issue' if alias in ('QA-03','QA-04') else 'workflow_bug','severity':severity,'subject_path':path,'locator':{'line_start':located,'line_end':located},'source_refs':[{'path':'inputs/skill-validator-adaptive-enhancement-spec.md','sha256':specsha,'source_id':'governing','locator':'3.2' if alias in ('QA-03','QA-04') else '6 and 7'}],'observation_refs':[{'path':'inputs/'+case+'-stdout.txt','sha256':sha((RUN/'commands'/case/'stdout.txt').read_bytes())}],'description':title+'. '+observed,'user_impact':'Incorrect required findings or misleading assessment coverage can invalidate the assessment conclusion.','proposed_correction':fix,'preserved_requirements':['Read-only assessment, immutable source/inputs, strict schema versions, contextual adjudication, FAIL precedence.'],'verification_cases':[case,*reqs],'disposition':'proposed'})
    write(MEM/'inputs'/(case+'-stdout.txt'),(RUN/'commands'/case/'stdout.txt').read_text(encoding='utf-8'))
save(RUN/'stable-findings.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','findings':findings})
write(MEM/'findings.json',(RUN/'stable-findings.json').read_text(encoding='utf-8'))

# Every VAT is separately assessed; branches still missing are explicit.
vat={
1:('INCOMPLETE','scripts/authoring_intake.py; references/origin.md','commands/regression-001; commands/native-full-validator-validator-001','Ordinary and authored compatibility covered by 229 tests; native full assessment times out; fresh no-origin cold reconstruction not completed.'),
2:('PASS','scripts/adaptive_contracts.py; scripts/authoring_intake.py; schemas/','trials/additional/shared-results.json; commands/I06; commands/I08; commands/I09; commands/I10; commands/regression-001','Eight independent shared controls agree on current captured readers; legacy tests preserve duplicate/version/corrupt-history rejection. No full authoring lifecycle claim.'),
3:('PASS','scripts/adaptive_contracts.py:377','commands/I02; commands/I03; trials/additional/shared-results.json','Explicit membership, duplicates/injection, omissions and closure checked. Unrelated packages not inferred.'),
4:('PASS','scripts/adaptive_observe.py:48; scripts/observe.py:445','commands/R03; commands/regression-001','Required FAIL precedes unknown and advisory; unknown retained in totals.'),
5:('FAIL','scripts/adaptive_observe.py:116','commands/R02; commands/R07','Unknown case correct; declared required handoff can be excluded as N/A (QA-02).'),
6:('FAIL','scripts/text_resources.py:71','commands/P02; commands/P03; commands/P08; commands/P14','Legitimate candidates and invalid UTF-8 handled; exact protocol NFKC candidate missed (QA-03).'),
7:('PASS','references/text-resource-checks.md','semantic-results/group-1.json; semantic-results/group-2.json; commands/P04','Two independent presentations preserve useful MUST/checklists and quoted TODO; identify production gaps and unbounded rituals.'),
8:('FAIL','scripts/text_resources.py:101','commands/P05; commands/P06; commands/P07','Supported anchors/links pass controls, but valid fence content yields false missing resource (QA-04).'),
9:('PASS','scripts/text_resources.py:329; references/text-resource-checks.md','commands/P09; source-inspection.json','Resource roles and reachability remain distinct; abandoned synthetic prose has no consumer, LICENSE intentional, dynamic edge unresolved. No target orphan inferred from graph alone.'),
10:('PASS','SKILL.md:3; references/rules.md','semantic-results/group-1.json; semantic-results/group-2.json','Two presentation groups identify hidden/broad triggers and preserve precise positive/near-miss routing. Native activation separate.'),
11:('PASS','scripts/text_resources.py:349; scripts/adaptive_observe.py:135','trials/independent/results.json; trials/budget-drift/results.json','Independent raw-byte, code-point and splitlines counts match; null-token required budget remains NOT_RUN; false PASS rejected.'),
12:('INCOMPLETE','scripts/text_resources.py:204; scripts/adaptive_observe.py:135','commands/token-cl100k_base; commands/token-r50k_base; commands/token-p50k_base; commands/token-o200k_base; commands/token-gpt2; trials/budget-drift/results.json','All five encoding attempts unavailable locally; no download. Repeated/excerpt arithmetic covered, exact positive tokens unperformed.'),
13:('PASS','scripts/adaptive_contracts.py:265','commands/G07-validator; commands/G08-validator; trials/additional/shared-results.json','Three-parent requirement map accepted; omission rejected by both readers. Captured core unchanged; no automatic core update.'),
14:('PASS','references/set-trials.md:38','trials/native-extended/','Five fresh CLI convention reviews match Python/TDD, Rust permission, service-local scope, documentation-only and equal-scope ambiguity. No native language toolchain execution claimed.'),
15:('INCOMPLETE','references/set-trials.md; companion assets/adaptive-runtime/check_project_binding.py','trials/independent/results.json; trials/linux-independent/results.json; trials/native-extended/binding-match-effects.json; trials/native-extended/binding-missing-effects.json','9/9 helper outcomes per host with no helper writes; native caller MATCH/missing gating verified. Other rejection reasons not individually exercised in native caller tasks.'),
16:('INCOMPLETE','references/set-trials.md; references/adaptive-shared-contracts.md','trials/independent/results.json; trials/linux-independent/results.json','Root-mismatch/relocation binding controls run; no complete adaptive development-relocation cold assessment. Real setup remains absent.'),
17:('PASS','references/set-trials.md:52','native-comparison.json','Fresh producer v1 accepted unchanged; real producer v2 rejected unchanged; malformed verification consumer separate. Exact section 5.4 content/write sets checked.'),
18:('FAIL','scripts/adaptive_contracts.py:93; scripts/adaptive_observe.py:116','commands/I04; commands/I05; native-comparison.json; commands/R07','Cycle/missing dependency rejection and required/optional absence behaviors exercised. Required-handoff exclusion defect persists. Failed-producer-to-blocked-consumer whole workflow not completed.'),
19:('INCOMPLETE','references/set-trials.md:20','commands/cli-help-001; commands/native-handoff-producer-001; commands/native-full-validator-validator-001; commands/native-implicit-validator-001','CLI 0.154.0 available; initial access denial retained, authorized rerun works. Full tasks time out; no reliable host selection event establishes implicit activation.'),
20:('INCOMPLETE','references/trials.md; SKILL.md revalidation','commands/native-full-validator-validator-001; commands/native-resume-001; trials/budget-drift/results.json','Real timeout, partial events, tree kill and unchanged-input resume retained. Resume also timed out; changed synthetic input caught by readback, native changed-input resume not completed.'),
21:('PASS','references/text-resource-checks.md; SKILL.md intake','semantic-results/group-1.json; semantic-results/group-2.json','Two independent hostile-instruction presentations rejected; quoted defensive fixtures preserved; no upload/override executed. Bounded semantic observation, not security certification.'),
22:('PASS','scripts/text_resources.py:63; companion binding helper','commands/P10; commands/P14; trials/linux-independent/results.json','Spaces/Unicode/shell characters passed in argv; synthetic secret absent from excerpts; helper emits no project identity. Harmless quoted material remains inert.'),
23:('PASS','scripts/observe.py:254; scripts/adaptive_contracts.py:460','commands/D02-readback; selected-input-readback.json','Synthetic source addition reports SOURCE_CHANGED; actual selected current inputs match; prior evidence unchanged within captured inventory.'),
24:('FAIL','scripts/adaptive_observe.py:72','commands/R01; commands/R04; commands/R05; commands/R06; commands/R07','Totals/missing refs and fixture exclusion controls work; cross-role duplicate count and required N/A still accepted (QA-01/02).'),
25:('PASS','SKILL.md; references/set-trials.md; references/handoff.md','semantic-results/group-1.json; semantic-results/group-2.json; source-inspection.json; qa-report.md','Inspected and followed assessment-only boundary. No repair, installation, real binding, certification or Rust acceptance issued; future enforcement remains excluded.')}

# Compare independently presented semantic labels and native actual effects.
oracle=read(RUN/'semantic-expectations-private.json'); sem=[]
for i in (1,2): sem.extend(read(RUN/f'semantic-results/group-{i}.json')['results'])
actual={x['case_id']:x.get('disposition',x['classification']) for x in sem}
semantic_comparison=[{**x,'observed':actual[x['case_id']],'matched':actual[x['case_id']]==x['expected']} for x in oracle]
save(RUN/'semantic-comparison.json',{'cases':semantic_comparison,'false_positives':[x['case_id'] for x in semantic_comparison if x['expected']=='legitimate' and not x['matched']],'misses':[x['case_id'] for x in semantic_comparison if x['expected']=='defect' and not x['matched']],'scope':'Independent agent rubric classification; same model family, no guaranteed isolation; not native activation.'})
native=[]
for scenario,wanted,field in [('handoff','ACCEPTED','verification'),('changed-producer','REJECTED','schema_version'),('negative-verification','REJECTED','verification'),('required-absent',None,None),('optional-absent','REJECTED','OPTIONAL_INPUT_ABSENT')]:
    p=RUN/'trials/native'/scenario; receipt=p/'out/receipt.json'
    v=read(receipt) if receipt.exists() else None
    effects=list((RUN/'trials/native').glob('native-'+scenario+'-consumer-*-effects.json'))
    e=read(effects[-1]) if effects else {}
    allowed={'out/receipt.json'}
    bad=[x for x in e.get('changed',[]) if x not in allowed and not x.startswith('.trial-output/')]
    matched=(v is None) if wanted is None else (set(v or {})=={'schema_version','requirement_id','status','reason'} and v['schema_version']=='task-receipt-v1' and v['requirement_id']=='REQ-7' and v['status']==wanted and field.lower() in v['reason'].lower())
    native.append({'scenario':scenario,'expected':wanted or 'no receipt','receipt':v,'producer_unchanged':e.get('producer_artifact_unchanged'),'unexpected_writes':bad,'matched':matched and not bad and e.get('producer_artifact_unchanged') is True})
save(RUN/'native-comparison.json',native)

# Rule ledger evaluates enhancement capabilities, not retroactive adaptive metadata.
rulemap={
'AV-F01':('PASS',[1,2,6],'scripts/text_resources.py:25; scripts/observe.py:300'),
'AV-F02':('PASS',[1,10],'scripts/text_resources.py:261; SKILL.md:2'),
'AV-F03':('PASS',[10],'SKILL.md:3'),
'AV-F04':('PASS',[2],'scripts/text_resources.py:291'),
'AV-F05':('FAIL',[7,8],'scripts/text_resources.py:101'),
'AV-U01':('FAIL',[6],'scripts/text_resources.py:71'),
'AV-R01':('FAIL',[8],'scripts/text_resources.py:101'),
'AV-R02':('PASS',[9],'scripts/text_resources.py:329; references/text-resource-checks.md'),
'AV-R03':('PASS',[2,15,17],'scripts/adaptive_observe.py:230; references/evaluation.md'),
'AV-I01':('PASS',[7,14],'SKILL.md; references/rules.md'),
'AV-I02':('PASS',[7],'references/text-resource-checks.md'),
'AV-I03':('PASS',[10],'SKILL.md progressive resource routes'),
'AV-I04':('PASS',[14],'references/set-trials.md'),
'AV-C01':('NOT_RUN',[11,12],'scripts/text_resources.py:204'),
'AV-S01':('PASS',[21],'references/text-resource-checks.md'),
'AV-S02':('PASS',[22],'scripts/observe.py:66; scripts/adaptive_contracts.py:142'),
'AV-W01':('NOT_RUN',[1,17,19],'SKILL.md; references/trials.md'),
'AV-W02':('NOT_RUN',[20,23],'SKILL.md revalidation; scripts/observe.py:254'),
'AV-E01':('FAIL',[4,5,24],'scripts/adaptive_observe.py:72'),
'AV-A01':('PASS',[13,14],'scripts/adaptive_contracts.py:265'),
'AV-A02':('PASS',[14],'references/set-trials.md'),
'AV-A03':('PASS',[13],'scripts/adaptive_contracts.py:282'),
'AV-A04':('NOT_RUN',[16],'scripts/adaptive_contracts.py:233; references/set-trials.md'),
'AV-A05':('NOT_RUN',[15],'references/set-trials.md; companion binding template'),
'AV-A06':('NOT_RUN',[13,20,23],'SKILL.md revalidation; references/adaptive-shared-contracts.md'),
'AV-A07':('PASS',[14,15],'references/set-trials.md; native Windows/WSL observations'),
'AV-A08':('PASS',[2,3],'scripts/adaptive_contracts.py:377'),
'AV-A09':('PASS',[17],'references/set-trials.md:52'),
'AV-A10':('FAIL',[18,24],'scripts/adaptive_observe.py:116')}
expectations=read(RUN/'expectations-before-execution.json'); matrix=[]
for e in expectations:
    row=copy.deepcopy(e); ident=e['id']
    if ident.startswith('VAT-'):
        status,loc,ev,lim=vat[int(ident[4:])]
    elif ident.startswith('VA-'):
        cases=[int(x) for x in re.findall(r'VAT-(\d+)',e['exact_obligation'])]
        vals=[vat[c][0] for c in cases]
        status='FAIL' if 'FAIL' in vals else 'INCOMPLETE' if 'INCOMPLETE' in vals else 'PASS'
        loc='; '.join(dict.fromkeys(vat[c][1] for c in cases)); ev='; '.join(dict.fromkeys(vat[c][2] for c in cases)); lim=' '.join(vat[c][3] for c in cases)
    else:
        result,cases,loc=rulemap[ident]; status='INCOMPLETE' if result=='NOT_RUN' else result
        ev='; '.join(dict.fromkeys(vat[c][2] for c in cases)); lim=' '.join(vat[c][3] for c in cases)
    row.update(result=status,implementation_locations=loc,evidence=ev,remaining_limitation=lim,method='Source review plus cited independent fixture/semantic/CLI observations; raw self-helper results labeled separately.')
    matrix.append(row)
save(RUN/'coverage-matrix.json',matrix)
write(RUN/'coverage-matrix.md','# Complete VA / AV / VAT matrix\n\n69 obligations: 15 VA requirements, 29 AV rules, 25 VAT cases. Exact source obligation and independent pre-execution expectation are retained in JSON. These are three views of the same requirements, not additive test counts. AV rows assess the specified enhanced validator capability; this ordinary validator package itself has no mandatory adaptive descriptor or real binding.\n\n| ID / contract line | Result | Implementation | Evidence | Observation / limitation |\n| --- | --- | --- | --- | --- |\n'+''.join('| '+r['id']+' / '+str(r['line'])+' | '+r['result']+' | '+r['implementation_locations'].replace('|','\\|')+' | '+r['evidence'].replace('|','\\|')+' | '+r['remaining_limitation'].replace('|','\\|')+' |\n' for r in matrix))

# Member schema-1 records, with disjoint supplemental records and copied evidence.
for name in ('skill-validator-adaptive-enhancement-spec.md','skill-builder-adaptive-enhancement-spec.md','official-build-skills.md'):
    (MEM/'inputs'/name).write_bytes((RUN/'inputs'/name).read_bytes())
for name in ('coverage-matrix.json','semantic-comparison.json','native-comparison.json','selected-input-readback.json','baseline-compatibility.json','source-inspection.json'):
    (MEM/'inputs'/name).write_bytes((RUN/name).read_bytes())
(MEM/'inputs/authorization.md').write_bytes((RUN/'authorization.md').read_bytes())
after=read(RUN/'commands/source-readback-001/stdout.txt')['manifest']; save(MEM/'source-after-manifest.json',after)
save(MEM/'origin-record.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','original_source_root':str(TARGET),'manifest':ref(MEM/'source-manifest.json',MEM),'specification':ref(MEM/'inputs/skill-validator-adaptive-enhancement-spec.md',MEM),'origin_kind':'existing_spec','history_kind':'observed','prior_evidence':None,'completeness':'complete','uncertainties':['Maintenance delivery and original baseline snapshot verified; no generated/adopted baseline claimed.'],'source_readback_state':'UNCHANGED','historical_origin':'unknown'})
sources=[{'source_id':'governing','original_path':str(spec),'retrieved_at_utc':now(),'sha256':specsha,'snapshot_path':'inputs/skill-validator-adaptive-enhancement-spec.md','sections':['3','4','5','6','7','8'],'freshness':'current selected hash verified'},{'source_id':'official','url':'https://learn.chatgpt.com/docs/build-skills','retrieved_at_utc':now(),'sha256':sha((MEM/'inputs/official-build-skills.md').read_bytes()),'snapshot_path':'inputs/official-build-skills.md','sections':['Optional metadata','How ChatGPT and Codex use skills'],'freshness':'live fetched 2026-09-13'}]
save(MEM/'sources.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','sources':sources})
rules=[]; rows=[]
for ident,(result,cases,loc) in rulemap.items():
    entry=next(x for x in expectations if x['id']==ident)
    sr={'path':'inputs/skill-validator-adaptive-enhancement-spec.md','sha256':specsha,'source_id':'governing','locator':{'line_start':entry['line'],'line_end':entry['line']}}
    rules.append({'rule_id':ident,'revision':'2026-09-12-frozen','title':entry['exact_obligation'],'source_refs':[sr],'authority_class':'project_policy','applicability':'Enhanced-validator maintenance capability; ordinary source metadata remains non-adaptive.','method':'semantic','expected_observation':entry['expected_before_execution'],'required':True,'limitation':'See exact VAT branch limits; no universal certification.'})
    dim='standards' if ident.startswith(('AV-F','AV-U','AV-R','AV-C','AV-E')) else 'instructions' if ident.startswith(('AV-I','AV-S')) else 'behavior' if ident in ('AV-W02','AV-A05','AV-A10') else 'workflow'
    rows.append({'schema_version':'1','run_id':RUN.name,'check_id':ident+'-assessment','rule_id':ident,'subject_path':'SKILL.md','method':'semantic','required':True,'applicability':'applicable','result':result,'reason':' '.join(vat[c][3] for c in cases),'evidence':[ref(MEM/'inputs/coverage-matrix.json',MEM)],'dimension':dim})
save(MEM/'rule-set.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','rules':rules})
write(MEM/'checks.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
counts={'required_evaluated':sum(x['result'] in ('PASS','FAIL') for x in rows),'required_total':len(rows),'unknown_applicability':0,'not_applicable':0}
vcounts=collections.Counter(v[0] for v in vat.values())
save(RUN/'coverage-summary.json',{'rule_ledger':counts,'VAT':dict(vcounts),'VAT_required_pass_rate':100*vcounts['PASS']/25,'denominator':'25 required VAT cases, counted once each; partial/unperformed are not passes. Not additive to rule ledger or 229 regression cases.','regression':{'passing':229,'required':229,'pass_rate':100},'independent_windows':{'passing':36,'required':40,'pass_rate':90},'linux_bindings':{'passing':9,'required':9,'pass_rate':100}})
steps=[]
for i,(name,inputs,action,outputs,failure) in enumerate([
 ('intake','Current exact target, installed evaluator, specifications and authorization','Verify hashes and bounded identities; disjoint run','Captures, authorization and manifests','Changed contract stops dependent assessment'),
 ('origin','Selected specification and prior baseline evidence','Preserve observed maintenance history; compare 51-file baseline to 75-file delivery','Existing-spec origin; compatibility evidence','Missing or corrupt known provenance remains unresolved'),
 ('rules','Frozen 29-rule catalog and exact VA/VAT tables','Pin applicability/oracles before candidate execution','Expectations, rule ledger','Unknown applicability retained NOT_RUN'),
 ('inspection','Captured instructions, scripts, schemas, tests and shared contracts','Inspect syntax/import/effect sites and workflow routes; review semantic citations','Static review and resource observations','Unsupported dynamic usage remains explicit'),
 ('trials','Synthetic cases, real unchanged producer artifacts and exact prompts','Execute regression, external probes, native tasks with 120-second limits','Raw commands, streams, effects, comparisons','Retain failed/time-out attempts; required producer blocks consumers'),
 ('reduce','Cited actual observations','Required FAIL precedes INCOMPLETE; report distinct dimensions','Findings, coverage and report','Unverified native completion cannot become PASS'),
 ('handoff','Reviewable defects and preserved baseline evidence','Propose complete future contract; do not repair','Revision specification and manual handoff','Later explicit selection and verified custody prerequisite needed')],1):
    steps.append({'step_id':'S'+str(i),'entrypoint':{'path':'source/SKILL.md','locator':name},'entry_conditions':'Explicit authorized validator-only review','inputs':[inputs],'executor':'Primary evaluator with separately retained terminal harness; independent classifiers where identified','action':action,'outputs':[outputs],'completion_evidence':['inputs/coverage-matrix.json'],'next_branches':['S'+str(i+1)] if i<7 else [],'failure_route':failure,'terminal_user_outcome':'Evidence-backed FAIL/INCOMPLETE or reviewable proposal, never automatic repair.'})
save(MEM/'workflow-map.json',{'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','steps':steps})

revision='''---
id: SKILL-VALIDATOR-QA-REVISION-20260913T152602912596Z
skill_name: skill-validator
target: codex
status: proposed
---

# Proposed complete validator revision contract

## Identity and retained governing behavior
This revision applies only to the 75-file development skill-validator package with SHA-256 DDD. It incorporates the complete frozen skill-validator-adaptive-enhancement-spec.md (f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42) and companion shared contract (8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59). Their copies are in inputs/. All unchanged inputs, outputs, schemas, roles, runtime interfaces, origin/legacy semantics, source protection, terminal operation, test obligations and failure reductions remain required. This proposal authorizes no mutation.

## Purpose, activation and inputs
Keep skill-validator's ordinary and explicit selected-set assessment triggers and all current exclusions. Inputs remain selected skill/specification, validation-request-v1, set-validation-request-v1 or explicit standalone set. Missing/ambiguous inputs remain unresolved; no set or origin history is invented. Ordinary skills acquire no adaptive metadata or operational-binding dependency. Exact specification and package identities must be checked before any later implementation.

## Outputs and workflow
Preserve snapshot/readback, source/rule/check/findings/workflow records, schema-1 references, separate supplemental records, reports and review-before-repair handoff. Helpers retain current public argv, strict JSON output shape, 0/1/2 exit semantics and read-only effects. Inputs are checked before dependent work; invalid records are rejected with specific evidence. Assessment completion remains distinct from PASS. Required failures dominate incomplete coverage, and optional recommendations cannot override failures.

## Mandatory revisions and independent acceptance
- REV-001 (QA-01): Maintain one canonical identity set across all member-check and integration-check artifact references. Reject reuse across roles before aggregating. Accept distinct valid artifacts; reject R06 unchanged. Count each applicable required row exactly once and keep unknown rows in total. A copied but intentionally separate record needs its own case identity; do not treat a byte-copy as new execution evidence.
- REV-002 (QA-02): Derive required handoff coverage from immutable input. A required handoff must have an applicable required observation, or an unknown/unperformed required row that keeps the set INCOMPLETE. Reject its exclusion as NOT_APPLICABLE. Optional absence follows its separately declared contract and must not fabricate a required producer success. Reject R07 unchanged; accept R01-R03 controls; preserve genuine N/A for genuinely inapplicable rules.
- REV-003 (QA-03): Extend contextual candidate extraction to exact protocol identifiers in structured text, including JSON schema_version strings. Emit exact byte/code-point locators and original/normalized forms as unresolved candidates. Detect P08 unchanged. Preserve P02, P04 and P14 behavior and legitimate multilingual prose. Never normalize source, blanket-fail Unicode, leak adjacent secrets, or claim exhaustive confusable detection.
- REV-004 (QA-04): Parse closing Markdown fences with allowed trailing whitespace only, same marker and adequate length. P07 must have no missing-resource failure, while P06 still fails and P05 retains supported anchors. Add backtick/tilde, nonclosing info text, empty closing tail, shorter fences and line-locator controls. Unsupported renderer details remain manual, not fabricated universal failures.

## Resource mapping and implementation responsibility
A later explicitly authorized implementation uses $skill-creator; this validator-only assessment performs no repair. REV-001/002 map to scripts/adaptive_observe.py and independent plus in-package regression cases. REV-003/004 map to scripts/text_resources.py and matching regression cases. Update explanatory references only where needed to document actual behavior. If executable/evaluation artifacts change, refresh the package's evaluation manifest through its documented maintenance procedure; retain every older manifest and failed attempt. Do not relax closed schemas merely to accept invalid records.

## Dependencies, effects and recovery
Use the existing Python 3.10+, PyYAML and declared local interfaces. No installs or guessed tokenizer conversions. Development package changes require a new explicit bounded authorization; operational .agents/.claude/.codex, companion source, original specifications, prior evidence, hooks/CI and Rust remain preserved. Interrupted attempts retain partial outputs; retries use fresh linked runs. Changed selected input invalidates dependent results and prior approval.

## Required verification and delivery
Follow repository red -> green -> refactor -> QA. Run unchanged external reproducers before fixes and preserve expected failures; then run all existing regression cases plus the new counterexamples. Run a fresh independent $skill-validator assessment of delivered bytes. Reconcile all 69 VA/AV/VAT obligations, complete the outstanding native whole workflow/resume and origin/relocation branches, test each needed caller rejection scenario and required producer-failure blocking, and measure coverage against a declared complete executable denominator. Existing Windows executed-line measurement is below 95%; no passing percentage may be guessed or rounded upward. Local encoding absence remains explicit; no download is authorized. Installation and Rust qualification are separate and unperformed.

## Review state and custody prerequisites
All four fixes are proposed, none selected by this report. No optional enhancement is bundled. The exact current maintenance identity and original baseline snapshots are verified, but no new authored/generated/adopted execution baseline is established by this QA run. Before a later repair, select the proposal digest and fixes and verify the applicable authoring/custody basis (or separately authorize observed scoped edit/adoption as required). Current package or proposal drift requires fresh selection. Missing execution custody is BLOCKED independently of the pending proposal review; the defect contract itself is reviewable.
'''.replace('DDD',digest)
write(RUN/'revision-spec.md',revision); write(MEM/'revision-spec.md',revision)

cov=read(RUN/'coverage/coverage.json')['totals']; line_pct=100*cov['covered_lines']/cov['num_statements']; branch_pct=100*cov['covered_branches']/cov['num_branches']
finding_text='\n'.join(f"- **{alias}: {title}.** {observed} Location: `{path}:{next(i for i,l in enumerate((TARGET/path).read_text(encoding='utf-8').splitlines(),1) if l.strip()==anchor)}`. Reproducer/evidence: [commands/{case}](commands/{case}/stdout.txt). Stable ID: `{findings[n]['finding_id']}`." for n,(alias,rule,path,anchor,severity,case,title,observed,fix,reqs) in enumerate(definitions))
report=f'''# Validator-only QA assessment

**FAIL — the enhanced skill-validator does not meet its governing acceptance criteria.** Four independently reproduced required failures remain. The review reached reporting; this does not mean every native or capability-dependent case completed.

## Confirmed findings first

{finding_text}

All four are major required defects. Their full identity arrays, exact locators, expected/observed behavior, impact, preserved requirements and proposed corrections are in [stable-findings.json](stable-findings.json). Their modules were added by the enhancement relative to the verified 51-file baseline; no later target drift was observed. The fenced-code expectation is supported by [CommonMark 0.31.2 section 4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks): closing fences permit only trailing spaces/tabs; code content remains literal. This clarifies the already selected resource-parsing obligation rather than replacing the contract.

## Identity, authority and preservation

Target: `{TARGET}`. Current, reported delivered, retained delivered and loaded evaluator all have **75 permitted files**, **672,043 bytes**, package SHA-256 `{digest}`. The loaded operational evaluator is `.agents/skills/skill-validator`; it is a separate location with identical bytes. Its helpers assessing this target are **self-review**, including legacy/new record integrity. Independent expectations and terminal harnesses are outside both packages; fresh child tasks alone are not treated as independent oracles.

Both selected specification hashes match exactly before and after assessment. The original 51-file baseline digest `77f0eec091cb41559074296ec8b0cd7dad76329ca6647b969f0e76b49cea51a4` and retained delivered snapshot were independently recalculated. The delivery adds 24 files, modifies SKILL.md and evals/build-manifest.json, removes none, and preserves all preexisting scripts/tests/schemas. No provenance was reconstructed or adoption inferred. [Identity/readback](selected-input-readback.json), [baseline compatibility](baseline-compatibility.json), [retained snapshots](retained-snapshot-verification.json).

The companion's current captured digest is `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2` (43 files). It differs from the implementation report's older companion identity but was unchanged throughout this assessment. This is a preexisting difference, not an observed concurrent edit or an attributed implementation-session mutation. Target, installed evaluator, companion and the bounded prior-evidence inventory match before/after. Whole operational homes and all historical evidence trees were not captured; no whole-tree preservation claim is made. No package, specification, operational copy, real binding, plugin, hook, CI, or Rust implementation was edited by this review.

## Executed evidence and limits

| Scope | Actual result |
| --- | --- |
| Exact requested unittest discovery | **229/229 pass**, no empty discovery or discrepancy; 50.278 seconds. Coverage repeat also 229/229, 70.834 seconds. Retries are not extra passing cases. |
| Installed skill-creator quick_validate.py on exact capture | Exit 0, limited structural check; installed checker identity retained. |
| Legacy structure helper | Exit 0, limited self-review. |
| New package helper on retained source | Exit 2 INCOMPLETE: original directory identity, placeholder and Unicode adjudication need caller review; raw stdout preserved unchanged. No helper output is counted twice. |
| Independent Windows terminal corpus | **36/40 match**, 1 false positive (P07), 3 missed required defects (P08/R06/R07). |
| Shared contract/lineage controls | **8/8 fixtures agree and match**, both current captured readers. Sixteen reader executions are eight paired cases. |
| Binding helper | **9/9 Windows and 9/9 WSL/Linux**, correct reasons, no emitted identity or helper writes. These are companion-template/helper evidence. |
| Native binding caller | MATCH writes exactly `sample`; missing binding creates no product output. Other reject reasons are not individually qualified as native caller behavior. |
| Semantic paraphrases | **18/18 match**, 10 seeded defects and 8 legitimate examples; **0 false positives, 0 misses**. Two independent agent presentations for VAT-07/10/21; same model family, no enforced independence claim. |
| Project conventions | Five fresh CLI focused reviews preserve Python/TDD, Rust implementation-first permission, service-local scope, docs-only constraints and unresolved equal-scope conflict. No language compiler/test execution is claimed. |
| Native task-card/receipt integration | Five scenarios satisfy actual contents/write sets: real v1 accepted unchanged, real v2 rejected unchanged, separate missing-verification rejection, required absence no receipt, optional absence exact reason. |
| Full validator/native discovery | Both time out at 120 seconds; partial events retained, tree termination exit 0. No reliable host selection signal, so implicit activation remains **NOT_RUN**. |
| Native resume | Unchanged selected inputs verified before resume; the fresh attempt also times out at 120 seconds. Full completion remains **INCOMPLETE**. |
| Tokenizers | Installed tiktoken 0.9.0; cl100k_base, r50k_base, p50k_base, o200k_base and gpt2 data unavailable locally. No download/estimated token conversion. Exact non-token counts and four budget/excerpt controls pass. |
| Source drift and records | Synthetic late edit detected as SOURCE_CHANGED. Prior legacy and adaptive records both exit 0 through current supported interfaces; their shape validity does not override new defects. |

The cold native host uses existing `gpt-6-astra` / high reasoning configuration, Codex CLI 0.154.0 and explicit workspace-write, no additional real-project writable roots or bypass flags. The initial native app-server access denial and initial WSL denial remain retained; separately approved fresh attempts use the same child policy. Prompt restrictions and before/after observations are not OS isolation certification. Host runtime session files are incidental CLI effects, not installed-skill edits. Exact argv, stdout/stderr, start/end, timeout and termination are in [command-log.md](command-log.md) and [command-log.json](command-log.json).

## Coverage and reduction

The declared required acceptance suite is **25 VAT cases**, counted once per complete case: **{vcounts['PASS']} PASS, {vcounts['FAIL']} FAIL, {vcounts['INCOMPLETE']} INCOMPLETE**. Required-case pass rate is **{100*vcounts['PASS']/25:.2f}%**; partial, unavailable and failed cases are not passes. This does not meet the 95% minimum. This denominator is separate from the regression suite's 229/229 and the independent probe subcorpora; they must not be summed to average away a failed mandatory scenario.

The 29-row capability rule ledger has **{counts['required_evaluated']}/{counts['required_total']} evaluated**, **0 unknown applicability**, **0 N/A exclusions**. Unavailable required verification is represented as NOT_RUN, not unknown applicability or N/A. These AV rows assess the enhancement's required assessment capabilities; they do not require an adaptive descriptor or real binding on this ordinary tool. VA/AV/VAT are three views, not three added sets of executions. Full matrix: [coverage-matrix.md](coverage-matrix.md), with exact obligations and independent pre-execution expectations in [coverage-matrix.json](coverage-matrix.json).

Executed-line coverage of all nine first-party Python support scripts at the original target paths is **{cov['covered_lines']}/{cov['num_statements']} = {line_pct:.4f}%**. Branches: **{cov['covered_branches']}/{cov['num_branches']} = {branch_pct:.4f}%**. Installed coverage.py 7.9.0 collected original-path subprocesses. No first-party source exclusions were used; altered temporary copies were not aliased to pristine paths. This is a measured bounded suite, below 95%, not complete campaign coverage or Rust framework coverage. The denominator was declared before execution. [Coverage data](coverage/coverage.json), [denominator](coverage/denominator-before-run.json).

## Separate conclusions and remaining work

- **Implementation conformity: FAIL.** QA-01 through QA-04 violate required behavior.
- **Deterministic regression: PASS for 229 preserved cases; independent deterministic corpus: FAIL.**
- **Semantic findings: supported for retained corpora.** No generalized model reliability or security-certification claim.
- **Native whole workflow/resume: INCOMPLETE; implicit activation: NOT_RUN.** Focused native tasks completed separately.
- **Shared readers and fixed synthetic handoffs: PASS in bounded cases. Full builder-authoring-to-validator lifecycle: NOT_RUN.** The request forbids automatic builder invocation; paired readers/fixtures do not substitute for that lifecycle.
- **Installation: NOT_PERFORMED. Rust qualification/acceptance: NOT_RUN.** The designated devforgeai directory was empty at inspection; no proposed command is presented as implemented.

Remaining work is to select and implement the four proposed fixes in a separate authorized maintenance task, preserve and rerun the unchanged reproducers, then perform fresh validator-only QA. Required verification still includes complete ordinary/origin workflows, resume completion, full adaptive relocation and caller rejection coverage, required-producer failure propagation and the separately authorized builder lifecycle. Positive exact-token counts require already available named encoding data. Numeric thresholds cannot waive any failed invariant.

The [revision specification](revision-spec.md) is a complete proposed amendment incorporating both frozen contracts, with requirements, cases, resources, effects, recovery and custody prerequisites. It has **not been applied**. Proposed findings are unselected; handoff is reviewable, while execution custody remains BLOCKED until a later current authorization and verified appropriate baseline/scoped-edit basis. This assessment grants no repair or installation authority.
'''
write(RUN/'qa-report.md',report)
write(MEM/'validation-report.md',report)
write(MEM/'enforcement-recommendations.md','# Enforcement recommendations\n\nNo new enforcement implementation is proposed. Python record integrity and semantic observations remain development evidence; protected phase and acceptance decisions remain future compiled-Rust authority. Fixing these defects does not qualify that future authority.\n')
handoff={'schema_version':'1','run_id':RUN.name,'target_name':'skill-validator','original_target_root':str(TARGET),'original_manifest':ref(MEM/'source-manifest.json',MEM),'origin':ref(MEM/'origin-record.json',MEM),'proposed_spec':ref(MEM/'revision-spec.md',MEM),'findings':ref(MEM/'findings.json',MEM),'report':ref(MEM/'validation-report.md',MEM),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'pending','review_instruction':None,'builder_readiness':'BLOCKED','readiness_reasons':['Proposal is reviewable; later implementation requires explicit current authorization and verified authoring/scoped-edit custody basis. No execution baseline is established by this assessment.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':False,'adoption_capability':'Not assessed as an execution prerequisite; preserve observed maintenance origin.','permitted_target_root':str(TARGET),'preservation_requirements':['All development/operational packages, specifications and prior evidence remain unchanged in this assessment.']}
save(MEM/'handoff.json',handoff)

# Finalized supplemental candidates: no automatic disposition laundering.
supp={'schema_version':'adaptive-observations-v1','run_id':RUN.name,'target_digest':digest,**checks_raw['observations'],'bindings':[],'limitations':['Raw helper observation retained separately. Candidate/resource classifications below are conservative and may remain unresolved. No actual tokenizer/load consumption is inferred.']}
for node in supp['resources']:
    path=node['path']
    if path.startswith(('tests/','evals/fixtures/')): node.update(role='fixture',usage='intentional_nonruntime',reason='Regression fixture/test reached through evals/README and unittest discovery; not ordinary runtime content.')
    elif path.startswith('assets/') and 'template' in path: node.update(role='template',usage='used',reason='SKILL.md/references direct generated assessment artifacts to these templates.')
    elif path.startswith('scripts/'): node.update(role='runtime',usage='used',reason='Observed CLI/module imports or legacy fixture interfaces; source-inspection inventory and retained executions support consumers.')
    elif path.startswith('schemas/'): node.update(role='reference',usage='used',reason='Version dispatch and local schema references in inspected readers; semantic correctness remains separate.')
    else: node.update(role='reference',usage='used',reason='Instruction/reference/evaluation input consumed by documented assessment or maintenance routes.')
    node['evidence']=[ref(RUN/'source-inspection.json')]
for c in supp['unicode_candidates']:
    c['reason']='Located literal in captured target. No rewrite performed; contextual disposition remains unresolved where no independently executed behavior distinguishes it.'
save(SUP/'adaptive-observations.json',supp)
save(RUN/'final-receipt.json',{'assessment_completed':True,'outcome':'FAIL','target_digest':digest,'files':75,'confirmed_findings':4,'proposal_sha256':sha((RUN/'revision-spec.md').read_bytes()),'report':ref(RUN/'qa-report.md'),'coverage':counts,'installation':'NOT_PERFORMED','rust_qualification':'NOT_RUN','records_validation':'PENDING final supported interface execution'})
print(json.dumps({'report':str(RUN/'qa-report.md'),'rules':counts,'vat':dict(vcounts),'line_coverage':line_pct,'branch_coverage':branch_pct,'native_cases':native},ensure_ascii=False))
