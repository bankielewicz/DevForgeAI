"""Reduce independent evidence without converting gaps into passes."""
from pathlib import Path
import ast
import collections
import datetime
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture import manifest, SOURCE, RUN

DIGEST='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
def load(path): return json.loads((RUN/path).read_text(encoding='utf-8'))
def save(path,data): (RUN/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Each mapping concerns only the named subcase; the full compound BAT remains
# incomplete when any required native or deterministic branch lacks evidence.
MAPPING={
'BAT-01-manual-handoff-byte-binding':'test_ordinary_create_manual_request',
'BAT-05-missing-disposition':'test_extra_lineage_missing_row',
'BAT-05-unauthorized-removal':'test_extra_lineage_unauthorized_removed',
'BAT-05-complete-three-row-lineage':'test_extra_lineage_complete',
'BAT-05-core-preserved':'test_extra_lineage_modified',
'BAT-07-bound':'test_binding_bound',
'BAT-07-missing':'test_binding_missing',
'BAT-07-invalid':'test_binding_bad_descriptor',
'BAT-07-root-mismatch':'test_binding_wrong_root',
'BAT-07-unbound':'test_binding_unbound',
'BAT-07-package-changed':'test_binding_changed',
'BAT-07-role-mismatch':'test_binding_role_mismatch',
'BAT-07-not-selected':'test_binding_inactive',
'BAT-07-ambiguous-role':'test_binding_ambiguous',
'BAT-07-unsafe-path':'test_binding_unsafe_argument',
'BAT-07-capture-limit':'test_binding_2001_limit',
'BAT-07-duplicate-name':'test_binding_duplicate',
'BAT-08-duplicate-key':'test_records_duplicate_and_nonfinite',
'BAT-08-extra-field':'test_records_extra_field',
'BAT-08-unknown-version':'test_records_unknown_version',
'BAT-08-malformed-reference':'test_records_wrong_locator',
'BAT-08-unresolved-id':'test_records_unresolved_requirement',
'BAT-08-boolean-integer':'test_records_boolean_integer',
'BAT-08-nonfinite-number':'test_records_duplicate_and_nonfinite',
'BAT-09-legacy-authoring-contract':'test_legacy_arbitrary_requirements',
'BAT-09-legacy-validation-request':'test_ordinary_create_manual_request',
'BAT-09-closed-top-level':'test_legacy_closed_contract',
'BAT-10-aggregate-partial':'test_records_partial_reduction',
'BAT-10-subset-dependency-closure':'test_extra_subset_dependency_rejected',
'BAT-11-cycle':'test_records_cycle',
'BAT-11-missing-dependency':'test_records_missing_dependency',
'BAT-11-occupied-target':'test_records_occupied_target',
'BAT-11-concurrent-drift':'test_extra_concurrent_drift_preserved',
'BAT-16-evidence-drift':'test_records_stale_reference',
'BAT-17-observed-first-edit':'test_observed_edit_preserves_unrelated',
'BAT-17-authored-baseline':'test_extra_authored_baseline_edit',
'BAT-17-corrupt-history':'test_known_corrupt_history_blocks',
}
LOCATIONS={
'BA-001':['SKILL.md:9','references/authoring.md:7','references/validation-handoff.md:3','scripts/authoring.py:419'],
'BA-002':['references/adaptation.md:7','references/adaptation.md:9','references/adaptation.md:11','scripts/adaptive.py:225'],
'BA-003':['references/adaptation.md:15','references/adaptive-contracts.md:23','scripts/adaptive.py:237'],
'BA-004':['SKILL.md:25','references/project-binding.md:3','assets/adaptive-runtime/check_project_binding.py:246'],
'BA-005':['references/adaptive-contracts.md:17','scripts/record_schema.py:15','scripts/adaptive.py:44','scripts/adaptive.py:97','scripts/adaptive.py:129'],
'BA-006':['references/adaptation.md:23','scripts/adaptive.py:321','scripts/adaptive.py:381','scripts/adaptive.py:444'],
'BA-007':['references/adaptive-contracts.md:25','scripts/adaptive.py:152','scripts/adaptive.py:264'],
'BA-008':['references/adaptation.md:15','scripts/adaptive.py:291'],
'BA-009':['references/adaptive-contracts.md:31','references/project-binding.md:5','assets/adaptive-runtime/check_project_binding.py:158'],
'BA-010':['references/adaptation.md:45','scripts/adaptive.py:307'],
'BA-011':['references/regeneration.md:3','scripts/authoring.py:148','scripts/custody.py:159','scripts/build_evidence.py:204'],
'BA-012':['references/adaptation.md:7','references/project-binding.md:13','scripts/authoring.py:459','assets/adaptive-runtime/check_project_binding.py:309'],
'BA-013':['SKILL.md:3','SKILL.md:17','references/adaptation.md:3'],
'BA-014':['SKILL.md:43','references/evidence-format.md:32','scripts/authoring.py:406','scripts/adaptive.py:69'],
}

def main():
    receipt=manifest(SOURCE)
    source_unchanged=receipt['package_digest']==DIGEST
    results={}; platform_counts={}
    for platform in ('windows','linux'):
        records=[]
        path=RUN/'reports'/f'{platform}-final04-results.json'
        if path.exists():
            value=json.loads(path.read_bytes())
            assert value['target_digest']==DIGEST
            records.extend(value['results'])
        results[platform]={row['id'].split('.')[-1]:row for row in records}
        platform_counts[platform]=dict(collections.Counter(row['status'] for row in records))
    cases=load('cases.json')
    for case in cases:
        case['target_digest']=DIGEST
        case['platform_results']={}
        test=MAPPING.get(case['id'])
        case['independent_test']=test
        for platform in ('windows','linux'):
            actual=results[platform].get(test)
            case['platform_results'][platform]={'status':actual['status'] if actual else 'NOT_RUN','method':'deterministic helper' if actual else 'required behavior not independently executed','evidence': ['reports/'+platform+'-final04-results.json'] if actual else []}
        if case['id']=='BAT-07-io-error' and (RUN/'reports/io-error-result.json').exists():
            case['platform_results']['windows']={'status':'PASS','method':'deterministic I/O failure injection; no native OS permission-isolation claim','evidence':['reports/io-error-plan.json','reports/io-error-result.json']}
        if case['id'] in ('BAT-15-spaces','BAT-15-non-ascii','BAT-15-shell-significant'):
            case['platform_results']['windows']={'status':'PASS','method':'Actual CLI argv with hostile synthetic path; original runtime template','evidence':['reports/hostile-cli-plan.json','reports/hostile-cli-result.json']}
        if case['id'] in ('BAT-12-positive-propose','BAT-12-positive-author-set','BAT-12-positive-review-updates','BAT-12-negative-install','BAT-12-negative-test-only'):
            case['platform_results']['windows']={'status':'PASS','method':'Native description-only classification; no host discovery or workflow-completion claim','evidence':['reports/native-final04-assessment.json','native/routing-description-04/output/final.txt','native/routing-description-04/result.json']}
        if case['id'] in ('BAT-13-equal-semantics-changed-bytes','BAT-13-removed-required-contract','BAT-13-no-auto-rebase','BAT-17-claude-import'):
            case['platform_results']['windows']={'status':'NOT_RUN','method':'120-second native attempt timed out; partial readback retained','evidence':['reports/native-final04-assessment.json']}
        case['status']='FAIL' if any(x['status'] in ('FAIL','ERROR') for x in case['platform_results'].values()) else ('PASS' if all(x['status']=='PASS' for x in case['platform_results'].values()) else 'NOT_RUN')
        case['limitation']='Helper observations establish only the named subcase. Cold autonomous behavior, generated-package effects and other compound obligations remain separately unperformed.'
    save('case-results.json',cases)
    bats=[]
    for number in range(1,18):
        name=f'BAT-{number:02d}'
        members=[c for c in cases if c['id'].startswith(name+'-')]
        per_platform={}
        for platform in ('windows','linux'):
            statuses=[c['platform_results'][platform]['status'] for c in members]
            per_platform[platform]={'status':'FAIL' if any(x in ('FAIL','ERROR') for x in statuses) else ('PASS' if all(x=='PASS' for x in statuses) else 'NOT_RUN'),'passing':statuses.count('PASS'),'required':len(statuses)}
        bats.append({'id':name,'target_digest':DIGEST,'platform_results':per_platform,'subcases':[c['id'] for c in members],'status':'FAIL' if any(p['status']=='FAIL' for p in per_platform.values()) else ('PASS' if all(p['status']=='PASS' for p in per_platform.values()) else 'NOT_RUN'),'reason':'Compound acceptance requires every applicable subcase; partial helper or timed-out native evidence does not qualify it.'})
    save('bat-results.json',bats)
    requirements=load('requirements.json')
    for req in requirements:
        requirement_bats=req['cases'].split(', ')
        relevant=[c for c in cases if c['id'][:6] in requirement_bats]
        req.update(source_locations=LOCATIONS[req['requirement']],target_digest=DIGEST,evidence=['reports/static-observations-final04.json','case-results.json'],method='Source semantic review plus independently mapped helper evidence',status='FAIL' if any(c['status']=='FAIL' for c in relevant) else ('PASS' if relevant and all(c['status']=='PASS' for c in relevant) else 'NOT_RUN'),limitation='Complete requirement not demonstrated while required BAT subcases are unperformed.')
    save('requirement-results.json',requirements)
    clauses=load('complete-clause-inventory.json')
    for clause in clauses:
        section=clause['section']
        if section.startswith('## 6') or section.startswith('### 6'): sources=LOCATIONS['BA-009']
        elif section.startswith('## 7'): sources=LOCATIONS['BA-010']
        elif section.startswith('### 5.3'): sources=LOCATIONS['BA-006']
        elif section.startswith('### 5.4'): sources=LOCATIONS['BA-009']
        elif section.startswith('## 5') or section.startswith('### 5'): sources=LOCATIONS['BA-005']
        elif section.startswith('## 4') or section.startswith('### 4'): sources=LOCATIONS['BA-002']
        elif section.startswith('## 3'): sources=LOCATIONS['BA-012']
        else: sources=LOCATIONS['BA-001']
        nonnormative=clause['text'].startswith(('---','id:','target:','status:','specification_version:','recorded:','```','| ---'))
        clause.update(source_locations=sources,target_digest=DIGEST,method='Semantic source review; indexed source pointers are supporting context, not proof of all effects',status='NOT_APPLICABLE' if nonnormative else 'NOT_RUN',reason='Specification metadata/table/code delimiter, not an independent behavior.' if nonnormative else 'Reviewed against listed source routes; full clause verification depends on unperformed native or uncovered semantic/legacy branches.',evidence=['reports/static-observations-final04.json','requirement-results.json','case-results.json'])
    save('complete-clause-results.json',clauses)
    lines=['# Requirement and BAT traceability','',f'Target: `{DIGEST}`. PASS applies only to a named executed subcase. NOT_RUN includes reviewed requirements with incomplete behavioral evidence.','', '| Requirement | Status | Source locators | Required BATs |','| --- | --- | --- | --- |']
    for req in requirements: lines.append('| '+req['requirement']+' | '+req['status']+' | '+', '.join(req['source_locations'])+' | '+req['cases']+' |')
    lines+=['','| Parent BAT | Windows (passes/required) | Linux (passes/required) | Overall |','| --- | --- | --- | --- |']
    for bat in bats:
        cells=[bat['id']]
        for platform in ('windows','linux'):
            p=bat['platform_results'][platform]
            cells.append(f"{p['status']} ({p['passing']}/{p['required']})")
        lines.append('| '+' | '.join(cells+[bat['status']])+' |')
    lines+=['','| Subcase | Windows | Linux | Independent test |','| --- | --- | --- | --- |']
    for case in cases: lines.append('| '+case['id']+' | '+case['platform_results']['windows']['status']+' | '+case['platform_results']['linux']['status']+' | '+(case['independent_test'] or 'Native/semantic campaign incomplete')+' |')
    (RUN/'traceability.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    coverage=load('reports/windows-final04-coverage.json')['totals']
    executed=coverage['covered_lines']; total=coverage['num_statements']; percent=100*executed/total
    native=[]
    for attempt in sorted((RUN/'native').iterdir()):
        path=attempt/'result.json'
        if path.exists():
            value=json.loads(path.read_bytes()); native.append({'attempt':attempt.name,'exit_code':value['exit_code'],'timed_out':value['timed_out'],'before_files':len(value['before']),'after_files':len(value['after'])})
    counts={p:collections.Counter(c['platform_results'][p]['status'] for c in cases) for p in ('windows','linux')}
    save('coverage-summary.json',{'subcases_per_platform':len(cases),'mapped_case_counts':counts,'required_subcase_pass_rates':{p:100*counts[p]['PASS']/len(cases) for p in counts},'executed_helper_cases':platform_counts,'windows_lines':{'executed':executed,'total':total,'percent':percent},'linux_lines':{'status':'NOT_RUN','reason':'Helper execution recorded; no Linux executed-line collector run.'},'branch_coverage':{'covered':coverage['covered_branches'],'total':coverage['num_branches']},'native_attempts':native})
    findings=[{'id':'QA-GAP-01','classification':'unperformed coverage / failed measurement floor','severity':'high','requirement':'AGENTS.md mandatory quality thresholds; BA-011; BAT-17','source_locations':['scripts/build_evidence.py:1','scripts/custody.py:1','scripts/init_skill.py:1','scripts/generate_openai_yaml.py:1'],'expected':'At least 95% executed-line coverage across declared first-party Python denominator; complete legacy behavior evidence.','actual':f'{executed}/{total} lines ({percent:.8f}%) independently measured. Legacy generated/adopted history and scaffolding are not independently replayed.','reproduction':'Run the retained coverage commands in command-log.md; inspect reports/windows-coverage-extended.json.','evidence':['reports/windows-coverage-extended.json'],'impact':'This independent campaign cannot qualify the whole executable package.','confidence':'confirmed evidence gap; not proof of an implementation defect','proposed_correction':'Execute independently specified legacy/scaffolding/error/recovery branches, preserving the denominator and all failed attempts.'},
    {'id':'QA-GAP-02','classification':'unperformed native coverage','severity':'high','requirement':'BAT-01 through BAT-17 applicable cold workflows','source_locations':['SKILL.md:9','references/adaptation.md:23','references/project-binding.md:5'],'expected':'Applicable cold tasks complete within bounded attempts with authored artifacts and independent readback.','actual':'Initial seven attempts exited before model work because the in-process app-server could not initialize (access denied). Escalation was interrupted without a launch receipt; root-owned fresh retry outcomes are listed separately.','reproduction':'See native/*-01/prompt.txt, plan.json, result.json and output/stderr.txt.','evidence':['native/ordinary-create-01/output/stderr.txt','coverage-summary.json'],'impact':'No complete native set orchestration, discovery/convention, update review/resume, or generated no-product-write assurance follows from helper tests.','confidence':'confirmed execution/coverage gap; no implementation defect inferred','proposed_correction':'Use normal host-approved bounded fresh attempts for remaining raw-input cases; grade actual artifacts and tool traces independently.'},
    {'id':'QA-NOTE-03','classification':'audit harness correction','severity':'low','requirement':'QA prompt independent fixture and exact evidence quality','source_locations':['test_independent.py:209','native_campaign.py:32'],'expected':'Fixtures honor custody run layout and native capture bounds before tests.','actual':'First Windows suite used the wrong run layout in four cases; 38 passed and four setup/oracle errors were retained. Fresh corrected Windows attempt passed 42/42. Native initial inventory lacked no-follow bounds; fixed before root create03, preserving script. Extension initially failed import before cases; fixed before 14 cases passed.','reproduction':'Compare inputs/test_independent-attempt01.py and reports/windows-independent-results-attempt01.json with current test_independent.py.','evidence':['inputs/test_independent-attempt01.py','reports/windows-independent-results-attempt01.json','inputs/native_campaign-before-inventory-fix.py'],'impact':'Initial setup failures do not count as product failures or valid TDD red results.','confidence':'confirmed audit limitation','proposed_correction':'Retain both attempts and use corrected fixtures; do not inflate the required-case denominator using retries.'}]
    findings[0]['evidence']=['reports/windows-final04-coverage.json']
    findings[0]['reproduction']='Run retest_final.py under the retained final04 coverage command; inspect reports/windows-final04-coverage.json.'
    findings[1]['actual']='Seven initial access-denied attempts; predecessor approved create/edit passed while seven other tasks timed out; final routing classifications passed while two reviews and import timed out. Import published partially verified artifacts before its limit.'
    findings[1]['evidence']+=['reports/native-predecessor-assessment.md','reports/native-final04-assessment.json']
    findings[1]['proposed_correction']='Diagnose bounded host/task completion cost before any separately authorized fresh campaign. Preserve timeout evidence and complete unperformed BAT subcases; do not claim an implementation defect from timing alone.'
    findings.append({'id':'QA-DEFECT-04','classification':'implementation defect, remediated by maintainer','severity':'medium','requirement':'BA-002/BA-009; sections 4.2/6.2; BAT-07 unsafe/excluded paths','source_locations':['assets/adaptive-runtime/check_project_binding.py:112'],'expected':'Environment file prefixes are excluded before content capture; Windows .ENV resolves through .env and must be rejected.','actual_predecessor':'On ecb5f805, synthetic .ENV had a true lowercase .env alias yet returned exit0/MATCH/BOUND.','reproduction':'probe_env_case.py; preserved reports/env-case-plan.json and env-case-result.json.','evidence':['reports/env-case-result.json','reports/windows-final04-results.json'],'impact':'Excluded environment files could be included in exact package capture instead of failing closed. No real secrets were used or emitted in this trial.','confidence':'confirmed native Windows reproduction; correction independently verified','proposed_correction':'Maintainer changed p.startswith to p.casefold().startswith, updated documentation/manifest. Auditor applied no source fix.','remediation_digest':DIGEST,'retest':'Final04 .ENV, .Env and .ENV.local regressions all reject with UNSAFE_PATH; complete independent suite replayed.'})
    save('findings.json',findings)
    source_before=load('source-final04-receipt.json')
    specs=[]
    for name in ('skill-builder-adaptive-enhancement-spec.md','skill-validator-adaptive-enhancement-spec.md','skill-builder-independent-qa-prompt.md'):
        data=(RUN.parents[4]/'docs/plan'/name).read_bytes(); retained=(RUN/'inputs'/name).read_bytes(); specs.append({'name':name,'sha256':hashlib.sha256(data).hexdigest(),'unchanged':data==retained})
    save('final-readback-receipt.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_digest':receipt['package_digest'],'source_unchanged':source_unchanged and receipt['manifest']==source_before['manifest'],'specifications':specs,'source_files':receipt['files'],'source_bytes':receipt['bytes'],'source_manifest':receipt['manifest'],'audit_write_scope':[str(RUN),'/tmp/devforgeai-skill-builder-20260913T190357053555Z-* (user-authorized native Linux synthetic fixtures)'],'old_evidence_writes':'none performed outside this fresh audit','operational_writes':'synthetic fixture bindings only; no real operational writes','limitations':['No before/after whole-workspace manifest; write preservation based on bounded tool actions, final source/spec readback and scoped scripts.','Initial command stdout/stderr is retained in session tool receipts and structured per-case results; not every terminal discovery call has an independent raw-file log.']})
    report=f'''# Independent QA report

This exact development-source skill-builder is **not established as meeting the complete acceptance contract**. Overall independent audit outcome: **FAIL for the independent declared coverage and required-case floors, with substantial INCOMPLETE behavioral coverage**. This is a failed QA qualification, not an assertion of an unresolved implementation defect. One independent Windows environment-file exclusion defect was confirmed on predecessor bytes and repaired by the maintainer; the corrected package passes the independent final helper replay. This is development QA evidence, not installation, enhanced-validator integration or Rust acceptance.

Target: `{DIGEST}`; 44 files, {receipt['bytes']} bytes. Final source/specification readback unchanged: {source_unchanged and all(s['unchanged'] for s in specs)}. Earlier `464acfdc...` and `ecb5f805...` snapshots and their native attempts remain separate. Final04 helper results bind the corrected package; predecessor native passes are not relabeled as final-byte acceptance.

## Executed evidence

- Windows independent helper cases: {platform_counts['windows']}. Initial incorrect-layout fixture results remain in `reports/windows-independent-results-attempt01.json`; retries count once for the required-case denominator.
- Linux independent helper cases: {platform_counts['linux'] or 'NOT_RUN; no result artifact received at report generation'}.
- Linux executed-line and branch coverage: **NOT_RUN**. Fixture execution used native `/tmp/devforgeai-skill-builder-20260913T190357053555Z-linux04`; reports remained here. The earlier mounted-filesystem attempt is incomplete and preserved.
- Static review: all 44 files inventoried; all 8 Python files parsed; all 17 shipped JSON schemas pass Draft 2020-12 meta-schema checking; all 33 local Markdown links resolve. The routed Markdown and Python call sites were read. These observations do not prove behavioral acceptance or external host metadata compatibility.
- Independent Windows executed-line coverage: **{executed}/{total} = {percent:.8f}%**, below 95%. Branch coverage: {coverage['covered_branches']}/{coverage['num_branches']}; tool combined percentages are not substituted for line coverage. Denominator includes all seven scripts and the original runtime template, including record_schema.py. No first-party files were excluded. Parent maintenance coverage is separate and is not copied into this independent result.
- Predeclared BAT subcases: {len(cases)} per platform. Windows mapped counts: {dict(counts['windows'])}; Linux: {dict(counts['linux'])}. Unexecuted required cases are not passes. Every BA requirement remains incomplete while its applicable compound subcases lack evidence.

The maintainer separately reports final Windows 2028/2133 lines (95.0773558368495%) and 825/944 branches with zero exclusions, and 258/259 required maintenance cases (99.6138996%) with the historical D-01 status-oracle disagreement retained as raw FAIL. Those are maintainer evidence, not independent oracles or a replacement for this campaign's missing BAT evidence. Independent required-subcase rates are Windows {100*counts['windows']['PASS']/len(cases):.2f}% and Linux {100*counts['linux']['PASS']/len(cases):.2f}%; across both declared platforms {100*sum(counts[p]['PASS'] for p in counts)/(2*len(cases)):.2f}%. Retries are not additional passing required cases.

The helper campaign directly exercises matching/missing/invalid/stale/inactive/ambiguous/unsafe bindings, output status/reason/exit shape, exact 2,000-file and 32-MiB boundaries and each limit excess, hostile project names, strict JSON/type/reference handling, selected topology, capability/collision rejection, complete/modified/missing/unauthorized lineage, legacy flexible authoring requirements, actual authoring/readback/manual handoff, observed edit preservation, authored revisions, explicit adoption followed by edit, user conflict and drift, and retained full-set/subset envelopes. Runtime observations left synthetic fixture files unchanged. Helper-only checks do not prove autonomous orchestration or a generated agent's refusal to write after non-MATCH.

## Native evidence and remaining work

`coverage-summary.json` lists every completed native receipt. Seven initial attempts exited before work with an app-server access denial. A normal escalation request was interrupted after a prolonged tool wait, with no retry directory/receipt. Root-owned approved predecessor create03 and edit03 passed independent artifact/trace review. Seven other predecessor native tasks reached their 120-second limits with no new project artifacts. The partial-set trace stated the correct intended dependency outcome but did not publish it. The implicit task selected and read the disposable builder, but did not finish a proposal. See `reports/native-predecessor-assessment.md`. Exit 0 or model intention alone does not qualify a workflow.

On the corrected final digest, description-only routing classified all five positive/negative requests correctly with no tool commands or writes. Equivalent-parent and removed-contract review tasks each timed out after reading the selected builder and raw inputs; neither changed an input or published a review. Import published a semantically preserved skill, captured baseline, AUTHORED import record and byte-bound manual request with testing/validation NOT_PERFORMED, but timed out before a final handoff. That partial positive artifact evidence does not convert the bounded import task into PASS. `reports/native-final04-assessment.json` retains independent checks, command traces and limits. Native host configuration and memory were inherited, so these are cold conversation trials, not hermetic absence of all validator context. Ten total approved workflow timeouts are coverage limits; further timeout diagnosis is follow-up work, not a proven product defect.

Still required: final-byte full cold create/edit; bounded monorepo discovery including junction and unknown manifest; unavailable-capability proposals; HTTP retention/storage expertise; generated adaptive relocation and runtime no-product-write behavior; autonomous failed-A/dependent-B/successful-C set authoring; all record-family mutation combinations; occupied/user-edited-obsolete/partial-write recovery; native host explicit versus implicit activation; unchanged/equivalent/material/missing update outputs; all four project conventions; resume after evidence drift; complete import and legacy schema-1/schema-2 generated/adopted history replay. Description classification is the one completed final native routing observation. Follow the 100 predeclared subcase rows; do not reduce these gaps to a passing helper count.

## Findings and interpretation

`findings.json` records unmet independent coverage, unavailable/incomplete native coverage, corrected audit-fixture defects, and the remediated implementation defect. The independent `.ENV` reproduction returned MATCH despite a lowercase `.env` filesystem alias. The maintainer corrected case folding; all three case-variant regressions and the 56 prior independent cases pass on final Windows bytes. Source readback and these checks supply counterevidence against a broad broken-package claim. The historical ordinary native receipt is an older exit-0 attempt and cannot qualify this final digest. A historical validator-based readback command was not rerun or used as an oracle. Actual enhanced-validator consumption is excluded by the audit request.

The full source, request, pinned specifications, oracles, exact fixtures, test sources, raw native streams and per-case results are retained here. `traceability.md`, `requirement-results.json`, `case-results.json`, and `complete-clause-results.json` preserve all BA/BAT and remaining specification clauses with actual evidence or explicit gaps. Source locations are supporting implementation routes; no keyword, schema validity, agreement between helpers or model status is treated as semantic proof.

## Evidence integrity

Audit writes were scoped to this fresh directory plus user-authorized native Linux `/tmp/devforgeai-skill-builder-20260913T190357053555Z-*` fixtures. Binding UUIDs remain only in their synthetic operational records. Mounted-filesystem Linux attempts remain separate; Windows is the primary host. Initial and final package captures remain disjoint. No skill source, validator package, real operational/personal copy, specification, configuration or preexisting evidence was modified by this auditor. Final hashes are in `final-readback-receipt.json`. Some initial discovery/tool stdout is available only in session receipts and structured outputs; missing raw capture is not reconstructed as original evidence. Parent maintenance results and independent audit results remain distinct.
'''
    (RUN/'qa-report.md').write_text(report,encoding='utf-8')
    print(json.dumps({'outcome':'FAIL/INCOMPLETE','source_unchanged':source_unchanged,'helper_counts':platform_counts,'lines':[executed,total],'native_receipts':len(native),'subcase_counts':counts}))

if __name__=='__main__': main()
