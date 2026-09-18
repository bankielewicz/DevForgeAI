"""Assemble retained compatibility observations into schema-1 member reports."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
STAMP=RUN.name
V=ROOT/'.agents/skills/skill-validator'
sys.path.insert(0,str(V/'scripts'))
import observe
import adaptive_observe as ao
from run_checks import execute
PY=[sys.executable,'-B','-X','utf8']
def sha(data): return hashlib.sha256(data).hexdigest()
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream: json.dump(value,stream,indent=2,ensure_ascii=False)
def text(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream: stream.write(value)
def ref(path,root=None): return {'path':path.relative_to(root).as_posix() if root else str(path),'sha256':sha(path.read_bytes())}
def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as stream: stream.write(source.read_bytes())

cases=json.loads((RUN/'compatibility-results-round2.json').read_text())['cases']+json.loads((RUN/'additional-results.json').read_text())['cases']
case_map={r['case']:r for r in cases}
attempts=sorted((RUN/'attempts').glob('*/receipt.json'))
def latest(suffix): return [p.parent for p in attempts if p.parent.name.endswith('-'+suffix)][-1]
schema_rows=json.loads((RUN/'schema-comparison-round2.json').read_text())['schemas']
assert all(r['json_equal'] for r in schema_rows)
findings_spec=[
('VC-001','AV-A06',308,'Update review state and member rules drift',['changed-equivalent-proposed','changed-false-no-change','review-nonvariant'],'Changed-equivalent PROPOSED is rejected while false NO_CHANGE and a nonvariant review are accepted.','Apply mode-specific prior/current input comparison and require existing variants.'),
('VC-002','AV-A03',284,'Ordinary core inventory requires a new fixed resource',['ordinary-parent'],'The reader rejects an ordinary core whose full explicit requirement table is in SKILL.md because references/adaptive-contract.md is absent.','Resolve explicit inventories from bounded captured parent Markdown; retain ambiguity as a specific gap.'),
('VC-003','AV-A03',465,'CRLF parent inventory is rejected',['crlf-parent'],'The same valid fenced parent inventory is accepted with LF and rejected with CRLF. Raw decode preserves CRLF and the closing-fence expression excludes CR.','Parse LF/CRLF equivalently while preserving original bytes and strict index content checks.'),
('VC-004','AV-A08',345,'Delivered role and parent are not bound to selection',['wrong-delivered-role','wrong-parent'],'Intake accepts self-consistent delivered descriptors with the wrong selected role or parent digest; builder rejects both.','Bind descriptor role, parent name/digest and complete requirement-ID set to the selected proposal.'),
('VC-005','AV-A04',250,'Missing parent disposition locator is accepted',['missing-parent-disposition'],'Descriptor lists R3 but its contract has no R3 disposition; validator records accepts it and builder rejects it.','Require all parent requirement IDs in the linked disposition map, followed by semantic disposition/authorization review.')]

native=sorted((RUN/'native').glob('*/receipt.json'))[-1]
native_observation='Timed out at 120 seconds. Partial agent message independently identified expertise versus project_variant mismatch; no completed final report.'
text(RUN/'native-observation.md','# Cold validator observation\n\n'+native_observation+'\n\nThe first attempt could not initialize app-server under the parent sandbox. The approved outer launcher preserved normal child workspace-write and existing model/auth. No configuration or trust bypass was used. Raw traces, prompts, commands, fixture snapshots and termination evidence remain under native/.\n')

catalog=(RUN/'inputs/adaptive-validation.md').read_text()
titles={}
for line in catalog.splitlines():
    m=re.match(r'\| (AV-[A-Z][0-9]{2}) \| (.*?) \| (.*?) \|',line)
    if m: titles[m[1]]=m[3]
assert set(ao.ALL_RULES)<=titles.keys()
member_records={}
for name,original in [('skill-validator',V),('skill-builder',ROOT/'src/agents/skills/skill-builder')]:
    out=ROOT/'docs/plan/skill-validations'/name/STAMP
    label='validator' if name=='skill-validator' else 'builder'
    metadata={'schema_version':'1','run_id':STAMP,'target_name':name}
    manifest=json.loads((out/'source-manifest.json').read_text())
    digest=manifest['package_digest']
    for source,filename in [(RUN/'inputs'/('skill-validator-adaptive-enhancement-spec.md' if label=='validator' else 'skill-builder-adaptive-enhancement-spec.md'),'governing-spec.md'),(RUN/'inputs/adaptive-validation.md','av-catalog.md'),(RUN/'plan.json','pre-execution-plan.json'),(RUN/'compatibility-results-round2.json','differential-results.json'),(RUN/'additional-results.json','additional-results.json'),(RUN/'independent-review.md','independent-review.md'),(RUN/'native-observation.md','native-observation.md'),(RUN/'schema-comparison-round2.json','schema-comparison.json'),(RUN/'revision-spec.md','proposed-revision.md')]:
        copy(source,out/'inputs'/filename)
    for suffix in ['unit','structure-'+label,'package-'+label,'quick-'+label]:
        for filename in ['receipt.json','stdout.txt','stderr.txt']:
            copy(latest(suffix)/filename,out/'inputs'/suffix/filename)
    for case in cases:
        for side in ['validator','builder']:
            if side+'_evidence' in case:
                for filename in ['receipt.json','stdout.txt','stderr.txt']:
                    copy(Path(case[side+'_evidence'])/filename,out/'inputs/differential'/case['case']/side/filename)
    a,receipt=execute('readback-'+label,PY+[str(V/'scripts/observe.py'),'readback','--source',str(original),'--manifest',str(out/'source-manifest.json')],'Exact original source matches captured manifest.')
    readback=json.loads((a/'stdout.txt').read_text())
    assert receipt['exit_code']==0 and readback['status']=='MATCH'
    copy(a/'stdout.txt',out/'inputs/readback-stdout.json')
    write(out/'source-after-manifest.json',readback['manifest'])
    source_rows=[]
    for ident,path in [('governing','inputs/governing-spec.md'),('catalog','inputs/av-catalog.md')]:
        source_rows.append({'source_id':ident,'original_path':str(RUN/'inputs'/('adaptive-validation.md' if ident=='catalog' else name+'-adaptive-enhancement-spec.md')),'retrieved_at_utc':None,'sha256':sha((out/path).read_bytes()),'snapshot_path':path,'sections':['Complete selected local document'],'freshness':'snapshot_only'})
    write(out/'sources.json',{**metadata,'sources':source_rows})
    rules=[]
    for rule in ao.ALL_RULES:
        source=ref(out/'inputs/av-catalog.md',out)
        source.update(source_id='catalog',locator=rule+' catalog row')
        rules.append({'rule_id':rule,'revision':'2026-09-12','title':titles[rule],'source_refs':[source],'authority_class':'project_policy','applicability':'applicable per check; ordinary adaptive exclusions explicit','method':'semantic','expected_observation':titles[rule],'required':True,'limitation':'Catalog and C01-C08 oracle plan retained before observations; this serialization records the same selected rules, not a new live standard.'})
    write(out/'rule-set.json',{**metadata,'rules':rules})
    checks=[]
    for rule in ao.ALL_RULES:
        result,method,reason='PASS','semantic','Scoped instruction/source review supports this obligation; helper/native limits remain separate.'
        evidence=['inputs/independent-review.md']
        if rule in ('AV-F01','AV-F02','AV-R01'):
            method='deterministic';reason='Existing structure and exact source identity observations passed.';evidence=['inputs/structure-'+label+'/stdout.txt']
        elif rule=='AV-F04':
            result='NOT_APPLICABLE';reason='No optional agents/openai.yaml in this selected package.'
        elif rule in ('AV-F05','AV-U01'):
            reason='Placeholder mentions document test criteria; U+FF50 in validator tests/test_adaptive.py:102 is an intentional fullwidth Python-token negative fixture. No production defect inferred.' if label=='validator' else 'Whole-text helper found no candidates requiring a defect finding.'
            evidence=['inputs/package-'+label+'/stdout.txt']
        elif rule=='AV-C01':
            method='deterministic';reason='Exact bytes/characters/lines measured; no tokenizer or budget selected, no invented token counts.';evidence=['inputs/package-'+label+'/stdout.txt']
        elif rule in ('AV-R02','AV-I04','AV-S01','AV-A05','AV-A09','AV-A10'):
            result='NOT_RUN';reason='Full dynamic consumer/native product behavior or adversarial coverage is beyond the completed compatibility observations.';evidence=['inputs/native-observation.md']
        elif rule in ('AV-A01','AV-A02'):
            result='NOT_APPLICABLE';reason='This selected authoring/assessment tool is not an adaptive domain expertise/core package.'
        elif rule in ('AV-S02','AV-W02'):
            method='deterministic';reason='229 current regressions and independent stale/membership/path observations exercise applicable reader/custody boundaries.';evidence=['inputs/unit/stderr.txt']
        elif rule=='AV-E01':
            method='deterministic';reason='Exact input hashes, immutable attempts, sorted manifests and truthful divergent outcomes retained.';evidence=['inputs/differential-results.json','inputs/readback-stdout.json']
        elif rule in ('AV-R03','AV-I01','AV-W01','AV-A03','AV-A04','AV-A06','AV-A08'):
            result='FAIL' if label=='validator' else 'PASS';method='deterministic';reason='Public reader responses contradict the selected shared contract in retained differential fixtures.' if label=='validator' else 'Builder responses agree with independent expected acceptance/rejection for these scoped fixtures; full builder behavior is not requalified.';evidence=['inputs/differential-results.json','inputs/additional-results.json']
        if rule=='AV-W01' and label=='builder':
            result='NOT_RUN';method='behavioral';reason='No new cold builder authoring campaign was run; earlier timeouts remain unclosed.'
        checks.append({'schema_version':'1','run_id':STAMP,'check_id':label+'-'+rule,'rule_id':rule,'subject_path':'SKILL.md','dimension':ao.dimension(rule),'method':method,'required':True,'applicability':'not_applicable' if result=='NOT_APPLICABLE' else 'applicable','result':result,'reason':reason,'evidence':[ref(out/p,out) for p in evidence]})
    text(out/'checks.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks))
    findings=[]
    if label=='validator':
        for ident,rule,line,title,case_ids,description,correction in findings_spec:
            anchor=(out/'source/scripts/adaptive_contracts.py').read_text().splitlines()[line-1].strip()
            identity=[rule,'scripts/adaptive_contracts.py',anchor,0]
            fid='F-'+sha(json.dumps(identity,separators=(',',':'),ensure_ascii=False).encode())
            findings.append({'finding_id':fid,'identity':identity,'rule_id':rule,'category':'workflow_bug','severity':'major','subject_path':identity[1],'locator':{'line_start':line,'line_end':line},'source_refs':[ref(out/'inputs/governing-spec.md',out)],'observation_refs':[ref(out/'inputs/differential'/case/'validator/stdout.txt',out) for case in case_ids],'description':description,'user_impact':'Valid builder output may be rejected or a changed/incorrect adaptive contract may be admitted for assessment. Manual review does not correct the deterministic custody interface.','proposed_correction':correction,'preserved_requirements':['Independent local readers','Exact shared schemas','No repair or operational effects during validation'],'verification_cases':case_ids,'disposition':'proposed'})
    write(out/'findings.json',{**metadata,'findings':findings})
    outcome,dimensions=ao.member_outcome(checks,'UNCHANGED')
    write(out/'assessment.json',{**metadata,'assessment_completed':True,'overall_assessment':outcome,'dimensions':dimensions})
    write(out/'origin-record.json',{**metadata,'original_source_root':str(original),'manifest':ref(out/'source-manifest.json',out),'specification':ref(out/'inputs/governing-spec.md',out),'origin_kind':'existing_spec','history_kind':'observed','historical_origin':'unknown','prior_evidence':None,'completeness':'complete','uncertainties':['Scope is compatibility; snapshot does not invent generated/adopted origin.'],'source_readback_state':'UNCHANGED'})
    write(out/'workflow-map.json',{**metadata,'steps':[{'step_id':step,'entrypoint':'SKILL.md','entry_conditions':'Selected package or explicit manual/set request.','inputs':['Current request','Exact source and specification'],'executor':'Codex and inspected local helper','action':action,'outputs':[output],'completion_evidence':'Retained exact bytes and raw observations','next':'Next scoped assessment step or terminal delivery','failure_route':'Preserve specific mismatch; no dependent trusted handoff or repair.','terminal_user_outcome':'Evidence-backed assessment and proposed change only.'} for step,action,output in [('intake','Resolve explicit target and binding.','Selected membership and origin'),('inspect','Pin rules, inspect text and call sites.','Located observations'),('test','Exercise read-only synthetic public interfaces.','Attempts and independent comparisons'),('report','Reduce required checks; preserve missing coverage.','Findings/report/manual proposal')]]})
    text(out/'enforcement-recommendations.md','# Enforcement boundary\n\nThese five reader corrections are ordinary deterministic input checks. No hook, CI or Rust enforcement change is proposed. Python results and editable binding records are not protected authorization; manual review and native coverage remain distinct.\n')
    report='# '+name+' compatibility assessment\n\nOutcome: **'+outcome+'**. Exact package digest: `'+digest+'`. This is '+('validator self-assessment with independent differential CLI fixtures and a bounded independent static review' if label=='validator' else 'a scoped builder compatibility assessment, not a new authoring campaign')+'.\n\n229 updated-validator regression tests pass. Fourteen shared schemas match. All 13 public-interface differential cases are retained in inputs; the builder agrees with its independently defined expected outcomes. The validator disagrees in eight cases, grouped into five findings. Valid full-set and actual prior partial-set/single-skill handoffs are accepted.\n\n'
    if findings:
        report+='| Finding | Evidence-backed gap |\n| --- | --- |\n'+'\n'.join('| '+f['finding_id'][:14]+' | '+f['description']+' |' for f in findings)+'\n\n'
    report+='Cold validator trial: '+native_observation+' Native implicit discovery remains NOT_RUN. Product producer-to-consumer execution and prior builder convention/author_set/update cold timeouts remain distinct; successful intake does not close them.\n\nThe validator package text observer emitted INCOMPLETE because it leaves fixture/placeholder candidate adjudication to the assessor. Manual review treats its one fullwidth-p character in a negative parser fixture as legitimate. Resource dynamic-use coverage remains NOT_RUN. Exact counts are retained; tokens were not guessed.\n\nThe initial differential fixture round had a harness manifest-sort error (Windows path ordering instead of ASCII row paths). It is preserved; round2 uses new fixture roots and correct sorted manifests. No package fix or test result replacement occurred.\n\nReadback: UNCHANGED. Both specifications remain at selected hashes. Live OpenAI standards were not refreshed; this compatibility conclusion uses the pinned local project contracts. No installation, adoption, repair, operational binding change or Rust qualification.\n\nSee the coordinator compatibility-report.md, revision-spec.md, exact command-log.md and checks.jsonl for evidence and proposed next work.\n'
    text(out/'validation-report.md',report)
    handoff={**metadata,'original_target_root':str(original),'original_manifest':ref(out/'source-manifest.json',out),'origin':ref(out/'origin-record.json',out),'proposed_spec':ref(out/'inputs/proposed-revision.md',out) if findings else None,'findings':ref(out/'findings.json',out),'report':ref(out/'validation-report.md',out),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'pending' if findings else 'not_needed','review_instruction':None,'builder_readiness':'REVIEW_REQUIRED' if findings else 'NO_CHANGE','readiness_reasons':['Proposed validator maintenance; no repair selected. Observed scoped edit is supported; known custody must be rechecked before any future edit.'] if findings else ['No builder change proposed from this scoped comparison.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':False,'adoption_capability':'Existing observed scoped edit is supported; no adoption occurred.','permitted_target_root':str(ROOT/'src/agents/skills'/name),'preservation_requirements':['Operational packages','Specifications','Prior evidence','Unrelated bytes'],'target_package_digest':digest}
    # Schema-1 readiness checker demands baseline/adoption for reviewable proposals;
    # retain BLOCKED execution rather than inventing a prior origin.
    if findings:
        handoff['builder_readiness']='BLOCKED'
        handoff['readiness_reasons'].append('No baseline/adoption reference selected for schema-1 execution handoff. Proposal review remains pending; no repair authorization.')
    write(out/'handoff.json',handoff)
    member_records[label]={'member_id':label,'package_digest':digest,'report':ref(out/'validation-report.md'),'checks':ref(out/'checks.jsonl'),'outcome':outcome,'source_state':'UNCHANGED','reason':'Scoped compatibility observations; full native assurance incomplete.'}
write(RUN/'member-records.json',{'schema_version':'1','members':member_records})
print({key:row['outcome'] for key,row in member_records.items()})
