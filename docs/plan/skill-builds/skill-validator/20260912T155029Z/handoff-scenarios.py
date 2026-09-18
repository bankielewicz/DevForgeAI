"""Root-supervised synthetic handoff/revalidation observations; never repairs originals."""
import json, re, sys
from pathlib import Path
from bootstrap import ROOT, PROJECT, write, digest, inventory
from verification import copy_package, execute, reference

R=ROOT/'handoff-trials/attempt-001'; R.mkdir(parents=True,exist_ok=False)
helper=ROOT/'candidate/scripts/observe.py'
old=PROJECT/'docs/plan/skill-builder-enhancement-evidence/20260912-build-v2/forward/spec-project/docs/plan/skill-builds/decimal-ledger-spec/20260912T123744Z-spec'
prior=json.loads((old/'build-provenance.json').read_text(encoding='utf-8'))
contract=json.loads((old/'build-contract.json').read_text(encoding='utf-8'))
assert prior['result']=='COMPLETE'
assert digest((old/'build-contract.json').read_bytes())==prior['contract_sha256']
assert digest((old/'builder-manifest.json').read_bytes())==prior['builder_manifest_sha256']
for row in prior['outputs']:
    assert digest((old/'snapshot'/row['baseline_path']).read_bytes())==row['baseline_sha256']
    assert digest((old/'snapshot/destination'/row['path']).read_bytes())==row['sha256']
for row in prior['evidence']:
    assert digest((old/'snapshot'/row['path']).read_bytes())==row['sha256']
for row in contract['inputs']:
    assert digest((old/'snapshot'/row['path']).read_bytes())==row['sha256']
results=[json.loads(l) for l in (old/'evaluation-results-delivered.jsonl').read_text(encoding='utf-8').splitlines()]
for result in results:
    assert result['status']=='PASS' and result['expectation_met']
    assert digest((old/'evaluation-cases.jsonl').read_bytes())==result['cases_sha256']
    for path,sha in result['candidate_digests'].items(): assert digest((old/'snapshot'/path).read_bytes())==sha
copy_package(old/'snapshot',R/'prior-snapshot')
for name in ['build-provenance.json','build-contract.json','builder-manifest.json','evaluation-cases.jsonl','evaluation-results-delivered.jsonl','build-report.md','final-receipt.json']:
    (R/name).write_bytes((old/name).read_bytes())
write(R/'baseline-verification.json',{'history_kind':'generated','prior_run_id':prior['run_id'],'provenance':reference(R/'build-provenance.json'),'contract':reference(R/'build-contract.json'),'verification':'All actual generated baseline and delivered file hashes, contract/input/excerpt source files, cited observation bytes, historical builder-manifest digest and every emitted delivered evaluator input/case hash match preserved historical snapshot. Original files unchanged.','historical_evaluator_reexecuted':False,'limit':'Editable historical development evidence verified by content; not protected framework provenance or proof of past user intent.'})
target=R/'project/src/agents/skills/decimal-ledger-spec'; copy_package(old/'snapshot/destination',target)
missing='Required operator notes: [notes](references/operator-notes.md).'
ritual='Repeat self-scoring until confidence is exactly 100; that alone authorizes completion.'
with (target/'SKILL.md').open('a',encoding='utf-8') as f: f.write('\n'+missing+'\n\n'+ritual+'\n')
write(R/'V13-plan.json',{'case_id':'V13','expected':'Both injected required workflow defects found; optional example remains separate; full proposal retains original contract; verified baseline and pending review yield REVIEW_REQUIRED without builder invocation','fixture_origin':'copied real generated baseline with two explicit disposable hand edits','before':inventory(target),'provenance':reference(R/'baseline-verification.json')})
code,receipt=execute('handoff-V13-snapshot',[sys.executable,'-B','-X','utf8',helper,'snapshot','--source',target,'--output',R/'assessment'])
assert code==0
A=R/'assessment'; (A/'inputs').mkdir(); (A/'observations').mkdir()
spec=(old/'snapshot/inputs/decimal-ledger-spec.md').read_bytes(); (A/'inputs/original-spec.md').write_bytes(spec)
(A/'inputs/validator-spec.md').write_bytes((ROOT/'inputs/skill-validator-spec.md').read_bytes())
(A/'inputs/baseline-verification.json').write_bytes((R/'baseline-verification.json').read_bytes())
code,p=execute('handoff-V13-structure',[sys.executable,'-B','-X','utf8',helper,'structure','--source',A/'source']); assert code==1
(A/'observations/structure.json').write_bytes((p/'stdout.txt').read_bytes())
def ref(p): return reference(A/p,A)
def finding(rule,path,anchor,description,correction,severity='major',category='workflow_bug'):
    identity=[rule,path,anchor.strip(),0]
    return {'finding_id':'F-'+digest(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()),'identity':identity,'rule_id':rule,'category':category,'severity':severity,'subject_path':path,'locator':{'anchor':anchor},'source_refs':[dict(ref('inputs/validator-spec.md'),source_id='validator-spec',locator={'section':'7. Rules, evidence, and applicability'})],'observation_refs':[ref('source/SKILL.md')],'description':description,'user_impact':description,'proposed_correction':correction,'preserved_requirements':['REQ-01','REQ-02','REQ-03','REQ-04','REQ-05','REQ-06'],'verification_cases':['V13','V15'],'disposition':'proposed'}
f1=finding('PRJ-002','SKILL.md',missing,'Required operator notes resource is absent.','Remove the dangling injected requirement; preserve the original complete instructions.')
f2=finding('PRJ-003','SKILL.md',ritual,'Self-score loop has no objective stop and falsely supplies completion authority.','Remove injected ritual; retain the existing actual result-review and input hash checks.')
f3=finding('REC-003','SKILL.md','Header-only input produces', 'An additional invalid-input example could clarify the existing failure contract.','Optionally add an invalid amount example with exit 2 and unchanged output.','advisory','enhancement')
write(A/'findings.json',{'schema_version':'1','run_id':'V13','target_name':'decimal-ledger-spec','findings':[f1,f2,f3]})
write(A/'sources.json',{'schema_version':'1','sources':[{'source_id':'validator-spec','snapshot_path':'inputs/validator-spec.md','sha256':ref('inputs/validator-spec.md')['sha256'],'retrieved_at_utc':None,'freshness':'snapshot_only','sections':['7. Rules, evidence, and applicability']}]})
write(A/'rule-set.json',{'schema_version':'1','rules':[{'rule_id':i,'revision':'1','title':i,'source_refs':[dict(ref('inputs/validator-spec.md'),source_id='validator-spec',locator={'section':'7'})],'authority_class':'project_policy' if i.startswith('PRJ') else 'official_recommendation','applicability':'applicable','method':'semantic','expected_observation':'Original contract preserved; no dangling resource or false completion authority.','required':i.startswith('PRJ'),'limitation':'Synthetic root-supervised scenario'} for i in ['PRJ-002','PRJ-003','REC-003']]})
proposal='''---
id: DECIMAL-LEDGER-REVISION-V13
skill_name: decimal-ledger-spec
target: codex
status: proposed
---
# Proposed complete revision

## Origin and preservation
Target: disposable project/src/agents/skills/decimal-ledger-spec. Original observed package digest: PACKAGE_DIGEST. Verified generated history: inputs/baseline-verification.json, derived from retained original successful builder run 20260912T123744Z-spec. This is a proposal awaiting review, not mutation authority.

## Complete future contract
ORIGINAL_SPEC

## Required changes
REV-001 Remove the injected dangling operator-notes requirement; preserve all original resources and behavior REQ-01 through REQ-06.
REV-002 Remove the injected self-score completion statement. Preserve the observable result-review, input hash readback, exact output schema and actual error reporting. No installed gate or fixed scoring loop replaces them.

## Optional enhancement
OPT-001 If separately selected, append a concise malformed amount example documenting exit 2, stderr and no output overwrite. It does not change parser behavior.

## Explicit workflow
Identify supplied input and new output paths; read and hash source; run actual helper; on exit 0 review produced JSON against schema and compare original input hash; return result plus inspected paths. On missing input request the required paths. On invalid input/output conflict retain source/existing output and return exact error. On interruption retain evidence and inspect partial effects before an explicitly authorized retry. No automatic repair, installation, network or dependency action.

## Files, dependencies and effects
SKILL.md implements REV-001/REV-002 and optionally OPT-001. scripts/sum_amounts.py, assets/result.schema.json and references/workers/result-review.md preserve their verified baseline bytes under REQ-01 through REQ-06. Standard-library Python 3.10+ and Windows PowerShell are sufficient; sequential review is allowed. Essential behavior and output schemas are preserved above. No unrelated user files are owned or removed.

## Acceptance
C01 0.10 and 0.20 yield count 2,total 0.30 with unchanged input; C02 header-only yields 0,0.00; C03 NaN/missing/overprecision input exits 2 without overwriting output; C04 existing output stays unchanged; C05 all original resource links resolve; C06 no self-score supplies completion authority and result review still observes output/input bytes; C07 optional malformed example matches actual helper behavior if selected.

## Review and builder handoff
Required repair set REV-001/REV-002 is proposed. OPT-001 remains deferred pending separate selection. No missing contract decision or new required dependency remains. Approval must identify this proposal digest and unchanged current target, select the changes and preserve all unaffected bytes. The existing verified generated baseline governs regeneration; adoption is not requested or needed. Do not invoke builder in this assessment.
'''
manifest=json.loads((A/'source-manifest.json').read_text())
proposal=proposal.replace('PACKAGE_DIGEST',manifest['package_digest']).replace('ORIGINAL_SPEC',spec.decode('utf-8').split('---',2)[2].strip())
(A/'revision-spec.md').write_text(proposal,encoding='utf-8')
(A/'validation-report.md').write_text('# V13 root-supervised assessment\n\nAssessment completed: true. Outcome FAIL: required linked resource absent and self-score control claim; optional error example advisory. Target copied from a digest-verified real generated baseline, then changed only in the disposable fixture before assessment. No original historical or project skill was repaired. Full proposed specification is reviewable and pending; builder readiness REVIEW_REQUIRED. Baseline evidence was verified by actual hashes before this conclusion, not invented. Findings and source snapshots retain the exact anchors. This is a bounded root-supervised scenario, not independent review or framework acceptance.\n',encoding='utf-8')
write(A/'origin-record.json',{'schema_version':'1','run_id':'V13','target_name':'decimal-ledger-spec','original_source_root':str(target),'manifest':ref('source-manifest.json'),'specification':ref('inputs/original-spec.md'),'origin_kind':'existing_spec','history_kind':'generated','prior_evidence':ref('inputs/baseline-verification.json'),'completeness':'complete','uncertainties':[],'source_readback_state':'UNCHANGED'})
write(A/'handoff.json',{'schema_version':'1','run_id':'V13','target_name':'decimal-ledger-spec','original_target_root':str(target),'original_manifest':ref('source-manifest.json'),'origin':ref('origin-record.json'),'proposed_spec':ref('revision-spec.md'),'findings':ref('findings.json'),'report':ref('validation-report.md'),'selected_finding_ids':[],'deferred_finding_ids':[f3['finding_id']],'proposal_review_state':'pending','review_instruction':None,'builder_readiness':'REVIEW_REQUIRED','readiness_reasons':['Verified successful generated baseline; complete proposal; only human review pending'],'baseline_kind':'generated','baseline_reference':ref('inputs/baseline-verification.json'),'adoption_required':False,'adoption_capability':'not_needed','permitted_target_root':str(target),'preservation_requirements':['all original REQ-01 through REQ-06','historical evidence','unrelated files']})
code,p=execute('handoff-V13-readback',[sys.executable,'-B','-X','utf8',helper,'readback','--source',target,'--manifest',A/'source-manifest.json']); assert code==0
write(A/'source-after-manifest.json',json.loads((p/'stdout.txt').read_text())['manifest'])
code,p=execute('handoff-V13-records',[sys.executable,'-B','-X','utf8',helper,'records','--run-root',A]); assert code==0
write(R/'V13-observation.json',{'case_id':'V13','readiness':'REVIEW_REQUIRED','proposal_complete':True,'required_finding_ids':[f1['finding_id'],f2['finding_id']],'optional_deferred':[f3['finding_id']],'historical_baseline_verified':reference(R/'baseline-verification.json'),'builder_invoked':False,'method':'root-supervised semantic case plus executed record checks'})

# V15: assess two actual file sets modeling delivered revisions; no forged builder provenance.
later=R/'later-delivery-fixture/decimal-ledger-spec'; copy_package(target,later)
later_text=(later/'SKILL.md').read_text(encoding='utf-8').replace(missing+'\n','')+'\nSee [new guide](references/new-guide.md).\n'
(later/'SKILL.md').write_text(later_text,encoding='utf-8')
write(R/'V15-plan.json',{'case_id':'V15','input_kind':'synthetic delivered-result bytes, not a successful builder claim','expected':'operator notes resolved, scoring ritual persistent, new guide absent is new; prior assessment unchanged','previous_report':reference(A/'validation-report.md'),'previous_findings':reference(A/'findings.json'),'later':inventory(later)})
code,p=execute('handoff-V15-snapshot',[sys.executable,'-B','-X','utf8',helper,'snapshot','--source',later,'--output',R/'later-assessment']); assert code==0
code,p=execute('handoff-V15-structure',[sys.executable,'-B','-X','utf8',helper,'structure','--source',R/'later-assessment/source']); assert code==1
out=json.loads((p/'stdout.txt').read_text()); failures=[r['reason'] for r in out['checks'] if r['result']=='FAIL']
assert any('new-guide.md' in x for x in failures) and not any('operator-notes.md' in x for x in failures)
assert ritual in later_text
write(R/'V15-observation.json',{'case_id':'V15','resolved':[{'predecessor_id':f1['finding_id'],'evidence':'dangling operator-notes instruction absent; relevant structure observation no longer fails it'}],'persistent':[{'predecessor_id':f2['finding_id'],'evidence':'exact scoring anchor remains in actual later SKILL.md'}],'new':[{'anchor':'See [new guide](references/new-guide.md).','evidence':reference(p/'stdout.txt')}],'unverified':[],'previous_report_unchanged':reference(A/'validation-report.md')==json.loads((R/'V15-plan.json').read_text())['previous_report'],'previous_findings_unchanged':reference(A/'findings.json')==json.loads((R/'V15-plan.json').read_text())['previous_findings'],'method':'root-supervised actual-byte revalidation fixture; no builder execution claimed'})

# V20 exact approval binding is already tested independently; retain a real changed proposal here.
original_proposal=(A/'revision-spec.md').read_bytes(); changed=R/'changed-proposal.md'; changed.write_bytes(original_proposal+b'\nAdditional optional change, not part of prior review.\n')
write(R/'V20-observation.json',{'case_id':'V20','prior_proposal':reference(A/'revision-spec.md'),'changed_proposal':reference(changed),'same_bytes':digest(original_proposal)==digest(changed.read_bytes()),'prior_review_reusable':False,'next_action':'Fresh human review of changed proposal digest; target changes require fresh readback/assessment.','scope':'Synthetic approval-binding decision; no real human approval fabricated. Independent stale-approval CLI rejection is in helper-tests/attempt-003.'})
print(json.dumps({'handoff_trials':str(R),'cases':['V13','V15','V20'],'original_historical_evidence_preserved':True}))
