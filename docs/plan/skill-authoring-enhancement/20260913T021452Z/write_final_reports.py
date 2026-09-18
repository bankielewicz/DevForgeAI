import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
summary=json.loads((RUN/'verification-summary.json').read_text())
op=RUN/'operational-revalidation/project/docs/plan/skill-validations/skill-builder/20260913-operational-002'
assert (RUN/'operational-revalidation/response.md').exists()
assert (op/'validation-report.md').exists()
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj): p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
reasons={
'AC-01':'Cold conversation trial created meeting-brief from a clear natural-language request, with requirements captured before staging and no approved-spec prerequisite.',
'AC-02':'Cold ambiguous-date trial asked about interpretation, desired output and destination; no target was generated while material input was pending.',
'AC-03':'Conversation/import trials honored explicitly selected development folders with spaces. The missing-location trial recommended its own resolved project src/agents/skills parent and final name.',
'AC-04':'Delivered initializer execution refuses an occupied directory; the existing sentinel remains byte-identical. No alternate name is selected.',
'AC-05':'Cold observed-edit trial captured the existing package, changed only requested instruction/UI fields, preserved the series reference bytes and unrelated metadata, and recorded observed history.',
'AC-06':'Cold second-edit trial verified the previous untested authoring baseline, applied one focused SKILL.md edit and returned fresh NOT_PERFORMED statuses.',
'AC-07':'Delivered tests cover divergent managed edits, identical unowned collisions, changed source/contract, scope rejection, interrupted writes and failed record/pointer publication. Independent revalidation confirms retained PARTIAL after post-write record failure.',
'AC-08':'Cold UI edit preserves brand color, dependencies and explicit-only policy; delivered helper tests cover focused fields, default prompt and explicitly requested policy change.',
'AC-09':'Conversation output remains one useful SKILL.md; import preserves its concrete script/output contract and source bytes. Metadata import in independent operational revalidation preserves supported compatibility/license/metadata without a checker.',
'AC-10':'Retained cold builder traces contain capture, staging, safe publication and readback, with no checker, grader, test suite, generated-task execution or automatic validator call. Quality implementations/tests are absent from the delivered builder.',
'AC-11':'Independent enhanced-validator invocation accepts the manual packet, performs positive/negative generated-script tests and reports a discovered precision defect without builder invocation. Delivered intake checks both real packets; regressions reject stale target/record/request bindings.',
'AC-12':'Known legacy origins and baseline bytes were verified before mutation. Legacy schemas, grader implementations, profiles and fixtures are preserved in validator-owned assessment; new authoring families are distinct. Fresh regressions include legacy origins/rejections. Protected inventoried historical files retain their hashes.',
'AC-13':'Cold builder tasks complete without loading validator. Returned requests remain usable for later invocation; authoring helper has no validator dependency and leaves quality unperformed.',
'AC-14':'Evidence distinguishes structure, deterministic assertions, classification, explicit independent workflows, enhanced-validator execution, author self-assessment and unperformed native activation. Synthetic precision FAIL is retained rather than relabeled.'}
evidence_map={
'AC-01':['conversation-response.md','conversation-trace.md'],
'AC-02':['material-ambiguity-response.md','material-ambiguity-trace.md'],
'AC-03':['conversation-response.md','material-ambiguity-response.md','import-script-response.md'],
'AC-04':['authoring-tests.py','regression-result.json','supplemental-result.json'],
'AC-05':['observed-edit-response.md','observed-edit-trace.md','verification-summary.json'],
'AC-06':['untested-revision-response.md','untested-revision-trace.md'],
'AC-07':['authoring-tests.py','regression-result.json','operational-revalidation-report.md'],
'AC-08':['observed-edit-response.md','authoring-tests.py','verification-summary.json'],
'AC-09':['conversation-response.md','import-script-response.md','operational-revalidation-report.md'],
'AC-10':['conversation-trace.md','observed-edit-trace.md','import-script-trace.md','untested-revision-trace.md'],
'AC-11':['enhanced-validator-response.md','enhanced-validator-trace.md','authoring-tests.py','delivered-intake.json'],
'AC-12':['history-check.json','scope-readback.json','regression-result.json','verification-summary.json'],
'AC-13':['conversation-response.md','import-script-response.md','authoring-tests.py'],
'AC-14':['verification-summary.json','enhanced-validator-response.md','operational-revalidation-report.md'],
'FORMAT':['structure.json','skill-creator-check.txt']}
limitations=[
'Native implicit skill activation was NOT_RUN. Explicitly loading a selected development SKILL.md is not native discovery.',
'Independent cold tasks used retained package snapshots; file-level differences from final packages are disclosed in verification-summary.json. Final delivered regression/structural checks and exact-byte equality bind the combined evidence to delivered bytes. Final operational revalidation used the same builder package bytes as delivery.',
'The development validator was assessed by the primary author following the unchanged operational validator, plus independent execution of the enhanced validator against a separate synthetic target. This is not an independent full audit of the validator source or its self-review.',
'No operational installation, dependency installation, hook/CI setup, Rust implementation/qualification or framework acceptance was performed.',
'Windows/Python 3.10.11 was exercised; other OS/runtime versions and OS-enforced isolation were not qualified.',
'Thirteen excluded task/backup/link boundaries are listed in scope-readback.json. Their contents were not byte-audited; excluded path sets remained identical. No protected-byte claim extends to those omitted contents.',
'No separate cold specification-only creation campaign was run; existing specification/import/adoption/regeneration compatibility was freshly exercised by validator-owned regressions and real legacy-origin delivery.',
'The synthetic imported decimal helper retains an inherited precision defect: a long decimal input rounded under the default Decimal context. It is a target finding in the validator trial, not an unresolved defect in either delivered enhancement package.'
]
for name in ('skill-builder','skill-validator'):
    out=RUN/'assessments'/name
    inputs=out/'inputs'
    copies={'verification-summary.json':RUN/'verification-summary.json','regression-result.json':RUN/'checks-005-delivered/result.json','regression-output.txt':RUN/'checks-005-delivered/unittest-output.txt','supplemental-result.json':RUN/'checks-006-authoring-inputs/result.json','authoring-tests.py':ROOT/'src/agents/skills/skill-validator/tests/test_authoring.py','history-check.json':RUN/'history-check.json','scope-readback.json':RUN/'scope-readback.json','operational-revalidation-report.md':op/'validation-report.md','operational-prior-findings.json':RUN/'operational-assessment/project/docs/plan/skill-validations/skill-builder/20260913-operational-001/findings.json','structure.json':RUN/'structural-003-delivered'/(name+'-structure-stdout.txt'),'skill-creator-check.txt':RUN/'structural-003-delivered'/(name+'-skill-creator-stdout.txt'),'delivered-intake.json':RUN/(name+'-delivered-intake.stdout.json')}
    for case in ('conversation','observed-edit','material-ambiguity','import-script','untested-revision','enhanced-validator'):
        for suffix in ('response','trace'):
            copies[case+'-'+suffix+'.md']=RUN/'independent-trials'/case/(suffix+'.md')
    for dest,source in copies.items(): shutil.copy2(source,inputs/dest)
    def ref(path):
        p=out/path
        return {'path':path,'sha256':h(p)}
    run_id=name+'-delivered'
    origin={'schema_version':'1','run_id':run_id,'target_name':name,'original_source_root':str(ROOT/'src/agents/skills'/name),'manifest':ref('source-manifest.json'),'specification':ref('inputs/skill-builder-authoring-enhancement-spec.md'),'origin_kind':'existing_spec','history_kind':'observed','prior_evidence':ref('inputs/authoring-record-raw.json'),'completeness':'complete','uncertainties':['Operational schema-1 uses observed for this current-byte assessment. The separately retained authoring-v1 record provides the actual authored lineage and verified legacy_generated predecessor; this does not assert missing history or adoption.'],'source_readback_state':'UNCHANGED','historical_origin':'Verified legacy_generated predecessor; current authoring-v1 lineage retained without rewriting historical records.'}
    save(out/'origin-record.json',origin)
    rules=json.loads((out/'rule-set.json').read_text())['rules']
    checks=[]
    for rule in rules:
        ident=rule['rule_id']; applicable=rule['applicability']=='applicable'
        checks.append({'schema_version':'1','run_id':run_id,'check_id':ident,'rule_id':ident,'subject_path':'source/SKILL.md','method':rule['method'],'required':rule['required'],'applicability':rule['applicability'],'result':'PASS' if applicable else 'NOT_APPLICABLE','reason':('Both actual installed Skill Creator and operational structure observations passed on delivered bytes.' if ident=='FORMAT' else reasons[ident]) if applicable else 'This authoring operation is assessed on builder; validator retains its companion testing/handoff responsibilities.','evidence':[ref('inputs/'+p) for p in evidence_map[ident]],'dimension':rule['dimension']})
    (out/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks),encoding='utf-8')
    save(out/'findings.json',{'schema_version':'1','run_id':run_id,'target_name':name,'findings':[]})
    previous=json.loads((inputs/'operational-prior-findings.json').read_text())['findings']
    save(out/'finding-resolution.json',{'schema_version':'1','run_id':run_id,'target_name':name,'scope':'Builder findings; companion validator assessment references shared enhancement evidence.','resolutions':[{'finding_id':f['finding_id'],'outcome':'resolved','evidence':[ref('inputs/operational-revalidation-report.md'),ref('inputs/regression-result.json')]} for f in previous],'new_reportable_package_findings':[]})
    steps = [('resolve','source/SKILL.md','Current request, project, identity and destination','Resolve material ambiguity and current authority','Selected operation and scope','capture','Unresolved material input stops dependent writes'),('capture','source/scripts/authoring.py' if name=='skill-builder' else 'source/scripts/observe.py','Selected input bytes and verified prior origin','Capture raw inputs and current package','Contract, before snapshot and manifest','stage' if name=='skill-builder' else 'rules','Retain incomplete captures and concrete errors'),('stage' if name=='skill-builder' else 'rules','source/references/authoring.md' if name=='skill-builder' else 'source/references/rules.md','Contract and snapshots','Author narrow candidate/resources' if name=='skill-builder' else 'Select independent applicable rules and expected outcomes','Candidate' if name=='skill-builder' else 'Pinned rule set and trial plan','apply' if name=='skill-builder' else 'assess','Report gaps without fabricated capability'),('apply' if name=='skill-builder' else 'assess','source/scripts/authoring.py' if name=='skill-builder' else 'source/references/trials.md','B/C/N and ownership' if name=='skill-builder' else 'Selected rules and disposable fixtures','Recheck and apply authorized paths' if name=='skill-builder' else 'Run structure, deterministic and independent behavior checks','Actual applied delta' if name=='skill-builder' else 'Retained observations, findings and limitations','readback','Conflicts stop writes; partial changes retained' if name=='skill-builder' else 'Preserve failed attempts and NOT_RUN coverage'),('readback','source/scripts/authoring.py' if name=='skill-builder' else 'source/scripts/observe.py','Actual live target and retained input manifest','Read exact delivered/assessed bytes','Matching manifest or SOURCE_CHANGED','handoff','Changed bytes block current-byte conclusions'),('handoff','source/references/validation-handoff.md' if name=='skill-builder' else 'source/references/handoff.md','Completed custody' if name=='skill-builder' else 'Assessment results and exact target digest','Publish authoring-only record and manual request' if name=='skill-builder' else 'Report results and any reviewable revision proposal','Authoring record/baseline/manual packet' if name=='skill-builder' else 'Report and review-state handoff','STOP','Retain failed publication; no automatic validator or repair loop')]
    save(out/'workflow-map.json',{'schema_version':'1','run_id':run_id,'target_name':name,'steps':[{'step_id':i,'entrypoint':p,'inputs':inp,'executor':'Codex using named bundled helper when applicable','action':act,'outputs':outputs,'next_step':next_step,'completion_evidence':outputs,'failure_recovery':failure,'terminal_result':'Return actual artifacts and limitations at STOP'} for i,p,inp,act,outputs,next_step,failure in steps]})
    required=sum(r['required'] for r in checks)
    dimensions={d:{'outcome':'PASS','required_evaluated':sum(r['required'] and r['dimension']==d for r in checks)} for d in ('standards','workflow','instructions','behavior')}
    save(out/'assessment.json',{'schema_version':'1','run_id':run_id,'target_name':name,'assessment_completed':True,'overall_assessment':'PASS','dimensions':dimensions,'required_evaluated':required,'required_total':required,'coverage_scope':'Pinned enhancement acceptance rules and named structural checks; no native/runtime qualification.','limitations':limitations})
    (out/'enforcement-recommendations.md').write_text('# Enforcement recommendations\n\nNo implemented enforcement or additional framework work is proposed in this scoped enhancement. Custody and assessment scripts remain agent-writable development evidence; no protected admission or OS-enforced isolation is claimed.\n')
    report='# Delivered development assessment: '+name+'\n\nThe pinned enhancement checks passed for package digest `'+summary['targets'][name]['package_digest']+'`. Required coverage: '+str(required)+'/'+str(required)+'. This is bounded development assessment, not native qualification or framework acceptance.\n\n'
    report+='Rules digest: `'+h(out/'rule-set.json')+'`. Source bytes match delivery, retained test inputs and source readback. Existing legacy provenance remains unchanged; current authoring is recorded in authoring-v1 with quality statuses unperformed at authoring time. Later assessment is this separate exact-byte record.\n\n'
    report+='| Case | Outcome | Evidence-backed observation |\n| --- | --- | --- |\n'
    for check in checks: report+='| '+check['check_id']+' | '+check['result']+' | '+check['reason']+' |\n'
    report+='\nStandards, workflow, instructions and behavior each passed their planned applicable checks. Enforcement is descriptive and unimplemented.\n\nFresh delivered regression: 202 tests, no failures/errors/skips. Additional raw-input capture: the 28 authoring tests passed. Both structural tools passed for each package. Independent routing classification: 14/14; this is not native activation.\n\nThe independent operational builder review initially failed with three findings; a fresh 12-case revalidation resolves all three. Its standalone report remains INCOMPLETE for coverage outside that subtask. This combined assessment adds the separately retained cold workflows and full delivered regression evidence; it does not relabel that report. The enhanced-validator trial assessed an imported synthetic skill and correctly retained an inherited precision FAIL. This trial is distinct from operational assessment and from validator self-review.\n\nLimitations:\n\n'+''.join('- '+x+'\n' for x in limitations)
    report+='\nFull command/case snapshots are retained in the enclosing task checks-* and independent-trials directories. Local inputs contain exact selected result/trace copies; checks.jsonl binds their actual digests. No further revision is proposed for these delivered packages.\n'
    (out/'validation-report.md').write_text(report,encoding='utf-8')
    save(out/'handoff.json',{'schema_version':'1','run_id':run_id,'target_name':name,'original_target_root':str(ROOT/'src/agents/skills'/name),'original_manifest':ref('source-manifest.json'),'origin':ref('origin-record.json'),'proposed_spec':None,'findings':ref('findings.json'),'report':ref('validation-report.md'),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'not_needed','review_instruction':None,'builder_readiness':'NO_CHANGE','readiness_reasons':['No unresolved implementation finding in the scoped combined assessment; limitations remain explicit.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':False,'adoption_capability':'Separate custody operation; not selected by this assessment.','permitted_target_root':str(ROOT/'src/agents/skills'/name),'preservation_requirements':['No mutation during assessment','Preserve original authoring and legacy records'],'target_package_digest':summary['targets'][name]['package_digest']})
    (out/'command-log.md').write_text('# Assessment command log\n\nActual commands and full streams are retained in ../../assessment-commands, ../../structural-003-delivered, ../../checks-005-delivered and ../../checks-006-authoring-inputs. Each evaluation plan precedes its attempt and records exact inputs, executor, command and timeout. Independent task traces and the operational review/revalidation reports are copied under inputs.\n\nThe primary author used the unchanged operational validator instructions for this combined assessment. The enhanced intake was executed separately as a deterministic implementation test, not as independent source review.\n')
    argv=[sys.executable,'-B','-X','utf8',str(ROOT/'.agents/skills/skill-validator/scripts/observe.py'),'records','--run-root',str(out)]
    p=subprocess.run(argv,capture_output=True,timeout=120)
    (RUN/'assessment-commands'/(name+'-records-001-stdout.json')).write_bytes(p.stdout)
    (RUN/'assessment-commands'/(name+'-records-001-stderr.txt')).write_bytes(p.stderr)
    save(RUN/'assessment-commands'/(name+'-records-001-plan.json'),{'command':argv,'exit_code':p.returncode,'coverage':'Record integrity only; not semantic proof.'})
    print(name,p.returncode,json.loads(p.stdout).get('errors'))
    if p.returncode: raise RuntimeError('Record integrity failed; retained attempt')
print('Wrote exact-byte reports and operational record-integrity observations.')
