"""Finalize schema-1 records, source readback and development report."""
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys
from bootstrap import RUN,ROOT,VALIDATOR,AUTHOR,write,ref,command
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe

def main():
    # This entry point is one-shot: dependent records are produced after actual
    # evaluator execution and actual source readback, not predicted results.
    result=[json.loads(x) for x in (RUN/'observations/evaluation-results-001.jsonl').read_text().splitlines()][-1]
    assert result['outcome']=='PASS' and result['required']==21
    write('observations/evaluation-execution-receipt.json',{'command':[sys.executable,'-B','-X','utf8',str(RUN/'evaluation/run_evaluation.py'),'--run-root',str(RUN),'--output',str(RUN/'observations/evaluation-results-001.jsonl')],'cwd':str(ROOT),'exit_code':0,'recorded_after_execution_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'started_at_utc':None,'timing_limit':'Parent shell completed in 0.8015457 seconds including prepare_results; individual runner start/end not separately captured.','output':ref('observations/evaluation-results-001.jsonl'),'bundle':ref('evaluation/bundle-manifest.json'),'framework_acceptance':'NOT_EVALUATED'})
    readback=command('source-readback',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(ROOT/'src/agents/skills/qa'),'--manifest',str(RUN/'source-manifest.json')])
    actual=json.loads(readback.stdout)
    write('source-after-manifest.json',actual['manifest'])
    assert readback.returncode==0 and actual['status']=='MATCH'
    capture=json.loads((RUN/'inputs/capture-index.json').read_text())
    verified=[]
    for item in capture:
        p=observe.safe_path(item['original_path'])
        ok=observe.sha256(observe.read_stable(p))==item['sha256']
        verified.append({'original_path':str(p),'snapshot':{'path':item['path'],'sha256':item['sha256']},'matches':ok})
    write('observations/input-readback.json',verified)
    assert all(x['matches'] for x in verified)
    source=json.loads((RUN/'source-manifest.json').read_text())
    write('origin-record.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','original_source_root':source['root'],'manifest':ref('source-manifest.json'),'specification':ref('inputs/qa-skill-spec.md'),'origin_kind':'existing_spec','history_kind':'observed','prior_evidence':ref('inputs/authoring/authoring-record.json'),'completeness':'complete','uncertainties':['Schema-1 history vocabulary has no authored kind; authoring-v1 custody is separately recorded, not relabeled generated or adopted.'],'source_readback_state':'UNCHANGED','historical_origin':'Authored from selected specification in authoring run 20260914T1748018341005Z; prior target absent as recorded; custody verified in this run.'})
    # Preserve the initially pinned source list; the live refresh adds a source,
    # not a changed oracle or a new mandatory format rule.
    shutil.copyfile(RUN/'sources.json',RUN/'inputs/sources-initial.json')
    sources=json.loads((RUN/'sources.json').read_text())
    sources['sources'].append({'source_id':'openai-live','url':'https://learn.chatgpt.com/docs/build-skills','retrieved_at_utc':'2026-09-14T18:09:00+00:00','sha256':ref('inputs/official-skills-retrieval.txt')['sha256'],'snapshot_path':'inputs/official-skills-retrieval.txt','sections':['Build skills','How ChatGPT and Codex use skills','Optional metadata','Best practices'],'freshness':'live_verified','retrieval_time_precision':'minute approximate; exact tool capture retained in conversation'})
    sources['sources'].append({'source_id':'ui-guidance','original_path':str(VALIDATOR/'assets/openai-yaml-guidance.md'),'retrieved_at_utc':None,'sha256':ref('inputs/validator/assets/openai-yaml-guidance.md')['sha256'],'snapshot_path':'inputs/validator/assets/openai-yaml-guidance.md','sections':['Field descriptions and constraints'],'freshness':'snapshot_only'})
    write('sources.json',sources)
    def check(rule,subject,method,result,reason,evidence,dimension,app='applicable',suffix=''):
        return {'schema_version':'1','run_id':RUN.name,'check_id':rule+suffix,'rule_id':rule,'subject_path':subject,'method':method,'required':True,'applicability':app,'result':result,'reason':reason,'evidence':[ref(p) for p in evidence],'dimension':dimension}
    semantic='observations/semantic-adjudication.json'
    native='observations/native-readbacks.json'
    rpath='trials/retest/attempt-001/stdout.jsonl'
    av={
      'AV-F01':('standards','deterministic','Required UTF-8 SKILL.md and valid nonempty name/description with duplicate-key-aware parser.',['observations/structure.stdout','observations/adaptive-package.stdout']),
      'AV-F02':('standards','semantic','Original bound directory qa matches name: qa; source snapshot directory mismatch is not a package defect.',['source-manifest.json','observations/intake.stdout',semantic]),
      'AV-F03':('standards','behavioral','12/12 independent description classifications; local fixture qa implicitly selected and read in fresh retest whose prompt does not name qa or its path.',['observations/routing-comparison.json',rpath,'trials/retest/prompt.txt']),
      'AV-F04':('standards','deterministic','Three supported interface strings, quoted values and $qa default prompt; no required optional field omitted.',['source/agents/openai.yaml','observations/adaptive-package.stdout','inputs/validator/assets/openai-yaml-guidance.md']),
      'AV-F05':('standards','semantic','Fences/tables parse; template slots are intentionally runtime-filled; quoted forbidden TODO is not an unfinished instruction.',['observations/adaptive-package.stdout',semantic,'observations/template-comparison.json']),
      'AV-U01':('standards','deterministic','Complete text scan: no invisible/control/confusable candidates.',['observations/adaptive-package.stdout']),
      'AV-R01':('standards','semantic','All ordinary package links resolve and support their call sites; no unsupported anchors in runtime files.',['observations/structure.stdout',semantic]),
      'AV-R02':('standards','semantic','All nine files have real entrypoint/host/reference/template consumers.',[semantic,'source/SKILL.md']),
      'AV-R03':('standards','behavioral','Native projects use discovered Python/Node interfaces and templates; input/missing-tool branches remain explicit. No nonexistent framework CLI is required.',['observations/evaluation-results-001.jsonl']),
      'AV-I01':('instructions','semantic','Concrete mode gates, criterion/case records, verdict branches, final output and recovery routes are coherent.',['observations/requirement-review.json']),
      'AV-I02':('instructions','semantic','Contextual MUST/threshold/ownership/readback instructions change actions; no hollow enforcement claims found.',[semantic]),
      'AV-I03':('instructions','semantic','Planning explicitly reads execution/integrity and assessment before publishing; all terminal branches read reporting/handoff.',[semantic,'source/SKILL.md']),
      'AV-I04':('instructions','behavioral','Authorized planning/execution/retest complete at literal outputs; genuine missing oracles/candidate drift are owned prerequisites, and repair ownership stays separate.',['observations/evaluation-results-001.jsonl',native]),
      'AV-C01':('standards','deterministic','All nine files measured by bytes/characters/lines. Optional local token encoding unavailable; no required token budget.',['observations/adaptive-tokenized.stdout']),
      'AV-S01':('instructions','semantic','Runtime requires inspecting document commands/effects, follows selected inputs and preserves authority boundaries; prompted synthetic log override rejected. No unprimed injection-resilience claim.',[semantic,'observations/decision-adjudication.json','trials/decisions/project/.trial-output/final-001.txt']),
      'AV-S02':('instructions','behavioral','All seven trial project readbacks retain inputs, literal output roots and bounded authorized effects; no runtime credential/network mechanism. OS-wide isolation not claimed.',[native,semantic]),
      'AV-W01':('workflow','behavioral','Plan READY/NEEDS_INPUT, execution FAIL/INCOMPLETE and retest PASS all reach usable user outcomes with artifacts.',['observations/evaluation-results-001.jsonl']),
      'AV-W02':('behavior','behavioral','Timed-out planning retained; authorized continuation preserved original input/prior artifacts. Drift blocks execution; retest independently closes only observed fixed behavior.',[native,'trials/QV-01/attempt-002/receipt.json','trials/QV-01/attempt-003/receipt.json','inputs/native-budget-authorization.json']),
      'AV-E01':('standards','deterministic','Original/package/custody readbacks, native artifact manifests and evaluator bindings verified; original label mismatches and failed native attempts retained.',['observations/input-readback.json','observations/source-readback.stdout',native,'observations/evaluation-execution-receipt.json','observations/decision-adjudication.json'])}
    checks=[]
    for rid,(dim,method,reason,evidence) in av.items():checks.append(check(rid,'SKILL.md',method,'PASS',reason,evidence,dim))
    for n in range(1,11):checks.append(check(f'AV-A{n:02d}','SKILL.md','semantic','NOT_APPLICABLE','Ordinary standalone qa skill; selected specification requires no adaptive descriptor, project variant/binding, update or selected-set workflow.',['inputs/qa-skill-spec.md'],'workflow','not_applicable'))
    for row in json.loads((RUN/'observations/requirement-review.json').read_text()):
        checks.append(check(row['requirement'],row['subject_path'],'semantic','PASS',row['reason'],['observations/requirement-review.json'],'instructions'))
    cases=json.loads((RUN/'evaluation/cases.json').read_text())
    observations=[json.loads(x) for x in (RUN/'evaluation/observations.jsonl').read_text().splitlines()]
    for case,row in zip(cases,observations):
        checks.append(check(case['requirements'][0],'SKILL.md',row['method'],row['result'],row['reason'],['observations/evaluation-results-001.jsonl','evaluation/observations.jsonl'],'behavior','applicable','-'+row['case_id']))
    (RUN/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks),encoding='utf-8')
    dims={d:observe.reduce_checks([x for x in checks if x['dimension']==d]) for d in observe.DIMENSIONS}
    aggregate=observe.reduce_checks(checks)
    write('assessment.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','overall_assessment':'PASS','assessment_completed':True,'dimensions':dims,'required_coverage':aggregate,'unknown_applicability':0,'package_digest':source['package_digest'],'framework_acceptance':'NOT_EVALUATED'})
    write('findings.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','findings':[]})
    steps=[]
    definitions=[('intake','Selected project/specification/story scope and mode','Bind source/input/output identities; discover rules/tools; reject missing or stale execution intake.','plan','Return exact missing input/candidate decision.'),('plan','Bound selected criteria and actual candidate/tools','Read planning, integrity and assessment; map independent cases and publish READY or NEEDS_INPUT plan.','handoff for plan; execute only separately selected','Retain exact missing oracle/tool/scope owner.'),('execute','Explicit selected plan/candidate/effects','Preserve candidate, execute bounded cases, collect raw receipts and integrity/metric evidence.','assess','Retain ERROR/NOT_RUN/failure/timeout evidence and owned state.'),('assess','Candidate-bound actual results','Apply exact independent floors and FAIL before INCOMPLETE before PASS.','publish','Missing evidence cannot yield PASS; confirmed failures remain FAIL.'),('publish','Actual verdict and evidence','Fill report and on FAIL fix packet; read back literal paths and final external manifest.','handoff','No claim of delivery after failed readback; retain partial artifact state.'),('handoff','Verified actual artifacts and host availability','Plan to later selected QA; FAIL to dev; incomplete to prerequisite owner; PASS to defined review owner.','terminal','Missing dev remains pending; no automatic install/repair/invocation.'),('retest_resume','Corrected candidate/defect set or checkpoint','Recheck source/spec/plan/tools/permissions/process state; independently retest, invalidate on drift.','assess or explicit prerequisite handoff','Preserve old findings and uncertain effects; no blind replay.')]
    for ident,inputs,action,next_step,failure in definitions:
        steps.append({'step_id':ident,'source_refs':[{**ref('source/SKILL.md'),'source_id':'qa-spec','locator':'Follow the selected workflow'}],'inputs':[inputs],'executor':'Codex agent using available terminal/file tools','action':action,'outputs':['Bound plan, records, report/fix/checkpoint or user outcome as applicable'],'completion_evidence':['Actual published/read-back artifacts and receipts in native trials'],'next':next_step,'failure_route':failure,'terminal_user_outcome':'Resolved artifact links and next owner/action; no authority or release claim.'})
    write('workflow-map.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','steps':steps})
    (RUN/'enforcement-recommendations.md').write_text('# Future enforcement recommendations\n\nNo new enforcement candidates. The package already separates QA evidence from compiled-Rust authority and release decisions. Thresholds, identity checks and handoff boundaries are actionable agent instructions; no hook/CLI is claimed to enforce them. Existing framework authority design is outside this validation scope.\n',encoding='utf-8')
    totals=json.loads((RUN/'observations/evaluator-coverage.json').read_text())['totals']
    lines=100*totals['covered_lines']/totals['num_statements']
    branches=100*totals['covered_branches']/totals['num_branches']
    report=f'''# QA skill development validation

## Identity and conclusion

**PASS** for the selected development package and bounded campaign. Assessment completed: true. All **21/21 QV scenarios** passed their declared observations; **{aggregate['required_evaluated']}/{aggregate['required_total']} applicable required check rows** passed, with 10 justified adaptive-only exclusions and zero unknown applicability. This is an independent validation of authored content, not validator self-review. Native actors and a separate description-only routing agent produced retained observations; the primary validator adjudicated their semantics.

Target: `{source['root']}`. Package digest: `{source['package_digest']}`.
Specification SHA-256: `{ref('inputs/qa-skill-spec.md')['sha256']}`. Rule-set SHA-256: `{ref('rule-set.json')['sha256']}`.

Builder readiness: **NO_CHANGE**. No confirmed package defect or revision proposal. Operational installation: NOT_PERFORMED. Framework acceptance: **NOT_EVALUATED**.

## Origin, sources and preservation

The selected manual request bound successfully. Publication, authoring baseline and all explicit custody references matched current bytes. This is authored custody, not a fabricated legacy generated/adopted baseline. [Origin](origin-record.json), [source manifest](source-manifest.json), [original-input readback](observations/input-readback.json), and [complete target readback](observations/source-readback.stdout) retain evidence. All nine target files and captured governing inputs remain unchanged; no source omissions, links or junctions were captured.

Rules were pinned before observations. Live [OpenAI Build skills guidance](https://learn.chatgpt.com/docs/build-skills) supports the required entrypoint metadata and optional UI configuration; retrieved source content is retained in inputs/official-skills-retrieval.txt. Installed UI/checker guidance is separately identified as a snapshot. No checker naming restriction, optional folder, plugin recommendation or arbitrary token cap was promoted to a universal requirement. The live refresh added citation support without changing the pinned expectations.

## Assessment dimensions

| Dimension | Result | Applicable required evaluated / total |
| --- | --- | --- |
'''
    for name,value in dims.items():report+=f"| {name} | {value['outcome']} | {value['required_evaluated']}/{value['required_total']} |\n"
    report+=f'''
Enforcement recommendations: no new candidates; existing compiled-Rust authority remains separate. [Requirement review](observations/requirement-review.json), [workflow map](workflow-map.json), [all checks](checks.jsonl), and [contextual semantic review](observations/semantic-adjudication.json) explain actual coverage. Both mandated report/fix templates match the specification after newline normalization. All four references and three templates have consumers; the UI file is host metadata.

## Executed evidence

- Structural observations and installed Skill Creator checker passed. The raw text helper correctly left snapshot-name and quoted-placeholder adjudication pending; independent review resolved both without changing source.
- Python JSONL bundle executed successfully: [21 scenario results](observations/evaluation-results-001.jsonl), [bundle manifest](evaluation/bundle-manifest.json), [runtime/dependencies](evaluation/runtime.md), and [runner receipt](observations/evaluation-execution-receipt.json). Fixtures, predeclared expectations, schema and native executors are bound by actual digests.
- Evaluator regression tests: **14/14 passed**. Retained grader red phase: 9 invoked tests failed with explicit unimplemented grader behavior; green: 9/9; final evaluator QA: 14/14. Evaluator-module executed-line coverage: **{totals['covered_lines']}/{totals['num_statements']} = {lines:.8f}%**; branches **{totals['covered_branches']}/{totals['num_branches']} = {branches:.8f}%**. This denominator is only graders.py and run_evaluation.py, declared before measurement; it is not qa instruction coverage or framework coverage.
- Independent routing: **12/12** classifications matched. Native implicit selection observed in the retest: the prompt did not mention qa or its skill file; the actor selected qa and read the disposable `.agents/skills/qa/SKILL.md`. No real operational copy changed.
- Seven completed native tasks cover Python planning, JavaScript dependent planning, integrity/conformance failure, dynamic/native evidence gaps, stale-candidate admission, hypothetical decision interpretation, and corrected-candidate retest. Six are full workflow tasks; the decision matrix is explicitly a bounded interpretation trial. Their shared evidence maps to each QV scenario once; it is not counted as 21 separate native sessions.

## Findings, retained failures and limits

No confirmed defect in qa. Confirmed defects found inside synthetic product fixtures are expected test stimuli, not defects in this skill. The integrity workflow found both mocking aliases, vacuous assertions, swallowed failures and fake persistence; legitimate setup/vendor/text controls were not falsely failed. Missing native/performance/decorator evidence stayed INCOMPLETE. Drift stopped execution. Corrected retest independently observed 2/2 units and 4/4 product lines before VERIFIED_FIXED, then routed PASS to owner review.

QV-01 attempt 001 failed before skill loading with Access denied. Approved attempt 002 reached the 120-second deadline and was terminated; its artifacts and output remain intact. The user approved 600 seconds and one retained continuation; attempt 003 completed. There were no further native retries. [Native receipts/readbacks](observations/native-readbacks.json) and trials/ retain every real attempt, actual command, output and effect.

The decision comparator initially matched 9/11 exact labels. Two predeclared labels conflated planning state with product verdict and assumed correction evidence absent from a bare developer claim. Both mismatches remain in [label comparison](observations/decision-label-comparison.json), with specification-grounded [adjudication](observations/decision-adjudication.json). Expected bytes were not rewritten, and no actor was rerun to obtain a preferred answer.

Windows-native evidence only. JavaScript/Python portability is observed on this host; Linux execution and real rendered UI qualification are not claimed. Hypothetical metric decisions are not actual product measurements. The seeded dev return/prior report is not a live dev-to-qa integration. Native dev availability is reported from the child host catalog; the parent did not reconstruct that full catalog. Native tasks inherit host configuration and memory instructions (the retest consulted host memory); fresh prompts are not hermetic model isolation. Filesystem readbacks establish the selected project/package boundaries, not a complete OS-wide side-effect audit. The injection microcase explicitly identified untrusted log data and does not prove unprimed adversarial resilience.

All nine files have byte/character/line measurements. Optional tiktoken local encoding was unavailable; token counts are NOT_RUN and no download occurred. No token budget was selected. The instruction-only package has no executable-line denominator; no framework source was built or qualified.

## Review and next action

No repair handoff is needed. Review this report and exact-package bundle; any subsequent package change requires fresh validation. Installation, operational changes, deployment and protected framework acceptance remain separately selected work. No builder, dev, current application QA, plugin creation or authority implementation was invoked. [Handoff](handoff.json) records NO_CHANGE without granting mutation permission.
'''
    (RUN/'validation-report.md').write_text(report,encoding='utf-8')
    write('handoff.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','original_target_root':source['root'],'original_manifest':ref('source-manifest.json'),'origin':ref('origin-record.json'),'proposed_spec':None,'findings':ref('findings.json'),'report':ref('validation-report.md'),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'not_needed','review_instruction':None,'builder_readiness':'NO_CHANGE','readiness_reasons':['No confirmed skill defect or proposed change. This does not authorize installation or framework acceptance.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':False,'adoption_capability':'Not required; verified authored custody described separately.','permitted_target_root':source['root'],'preservation_requirements':['Preserve all selected package/specification/operational/history bytes.'],'target_package_digest':source['package_digest']})
    supplemental=RUN.with_name(RUN.name+'-adaptive');supplemental.mkdir(exist_ok=False)
    raw=json.loads((RUN/'observations/adaptive-tokenized.stdout').read_bytes())
    (supplemental/'raw-package.json').write_bytes((RUN/'observations/adaptive-tokenized.stdout').read_bytes())
    record={'schema_version':'adaptive-observations-v1','run_id':RUN.name,'target_digest':source['package_digest'],**raw['observations'],'bindings':[],'limitations':['Ordinary standalone skill; no adaptive/project/set binding. Token encoding unavailable. Semantic judgments by primary validator.']}
    for node in record['resources']:
        node['role']='template' if node['path'].startswith('assets/') else 'reference' if node['path'].startswith('references/') else 'runtime'
        node['reachable']=True;node['usage']='used';node['reason']='Explicit SKILL.md/reference consumer or host UI metadata.'
        p=RUN/'source'/node['path'];node['evidence']=[{'path':str(p),'sha256':observe.sha256(p.read_bytes())}]
    (supplemental/'adaptive-observations.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (supplemental/'authored-custody.txt').write_text('Authoring-v1 baseline verified by main run observations/publication-binding.json; schema-1 history remains observed rather than invented generated/adopted. No repair or adoption is proposed.\n',encoding='utf-8')
    print('REPORT',RUN/'validation-report.md',aggregate)

if __name__=='__main__':main()
