import datetime, json, re
from pathlib import Path
from bootstrap import ROOT, PROJECT, write, digest, inventory
from verification import evaluate, reference

target=PROJECT/'src/agents/skills/skill-validator'
current=inventory(target); baseline=inventory(ROOT/'generated-baseline'); assert current['files']==baseline['files']
for name in ['valid-001','defect-001','ambiguity-001']:
    frozen=ROOT/'task-trials'/name/'validator'
    assert inventory(frozen)['files']==current['files'], 'task did not use final bytes: '+name
    assert inventory(frozen)['files']==json.loads((ROOT/'task-trials'/name/'validator-before-manifest.json').read_text())['files']
assert re.search(r'\A---\s*\n(.*?)\n---',(ROOT/'routing/attempt-001/SKILL.md').read_text(),re.S)[1]==re.search(r'\A---\s*\n(.*?)\n---',(target/'SKILL.md').read_text(),re.S)[1]
expected=json.loads((ROOT/'routing/expected.json').read_text())['cases']; observed=json.loads((ROOT/'routing/attempt-001/observed.json').read_text())['cases']
assert {r['case_id']:r['route'] for r in expected}=={r['case_id']:r['route'] for r in observed}
write(ROOT/'routing/comparison.json',{'expected':reference(ROOT/'routing/expected.json'),'observed':reference(ROOT/'routing/attempt-001/observed.json'),'matched':12,'total':12,'native_implicit_invocation':'NOT_RUN','final_frontmatter_unchanged':True,'deviation':'Classifier shell read the full frozen SKILL.md into memory but displayed only frontmatter; model did not receive body or expected labels.'})
helper=json.loads((ROOT/'helper-tests/helper-observation.json').read_text()); assert helper['tests']==34 and helper['result']=='PASS'
hashes={r['path']:r['sha256'] for r in current['files']}
assert all(hashes[r['path']]==r['sha256'] for r in helper['outputs'])
self_receipt=json.loads((ROOT/'self-review/final-receipt.json').read_text()); assert self_receipt['record_integrity_exit']==0 and self_receipt['target_readback_unchanged']
contracts=json.loads((ROOT/'build-contract.json').read_text())
assert {a['path'] for a in contracts['artifacts']}==set(hashes)
for row in contracts['inputs']: assert digest(Path(row['resolved_path']).read_bytes())==row['sha256']
preserved={}
for path,manifest in [(PROJECT/'.agents/skills/skill-builder','builder-before-manifest.json'),(PROJECT/'src/agents/skills/skill-builder','development-builder-before-manifest.json'),(PROJECT/'docs/plan/skill-builds/skill-validator/20260912T140148003Z','preserved-blocked-build-manifest.json')]:
    after=inventory(path); before=json.loads((ROOT/manifest).read_text()); assert after['files']==before['files']; preserved[str(path)]={'unchanged':True,'files':len(after['files'])}
assert inventory(ROOT/'task-inputs')['files']==json.loads((ROOT/'task-inputs-before-manifest.json').read_text())['files']
case_map={
 'V01':('root-supervised instruction-only fixture',['boundary-trials/attempt-001/V01-semantic-observation.json'],'Existing origin reused; real mandatory structure passes; no folders or fixes invented.'),
 'V02':('independent cold validator task',['task-trials/defect-001/results/origin-record.json','task-trials/defect-001/results/origin-spec.md'],'Exact observed origin retains defects and unknown history; no baseline manufactured.'),
 'V03':('independent cold validator task',['task-trials/ambiguity-001/results-001/validation-report.md'],'Two competing specs retained; checks continue; assessment INCOMPLETE and execution BLOCKED as expected.'),
 'V04':('independent deterministic CLI regressions',['helper-tests/report.md'],'Invalid YAML/required metadata/missing links and anchors produce observed rejection.'),
 'V05':('independent cold validator task',['task-trials/defect-001/results/findings.json','task-trials/defect-001/results/workflow-map.json'],'Bypassed Prepare, missing approved_order producer and false success are cited.'),
 'V06':('independent cold validator task',['task-trials/defect-001/results/revision-spec.md'],'Schema contradiction retained as unresolved D1, not silently chosen.'),
 'V07':('independent cold validator task',['task-trials/defect-001/results/ceremonial-review.json'],'Useful integer MUST and service boundary preserved; self-scoring/control claim distinguished.'),
 'V08':('root-supervised capability/fallback branch',['boundary-trials/attempt-001/V08-observation.json'],'Actual missing-executable lookup yields NOT_RUN; dated fallback retained; independent structure continues.'),
 'V09':('independent cold validator tasks and helper regressions',['task-trials/valid-001/results/validation-report.md','task-trials/defect-001/results/validation-report.md','helper-tests/report.md'],'Actual success/malformed/partial-output trials preserved; valid-target arithmetic defect is observed, not concealed.'),
 'V10':('independent cold validator task',['task-trials/defect-001/results/validation-report.md'],'Remote capability branch not executed; static unsupported capability and source issues remain visible.'),
 'V11':('independent missing-source task plus root semantic support case',['task-trials/defect-001/results/findings.json','boundary-trials/attempt-001/V11-observation.json'],'Absent reference and extant non-supporting passage distinguished; no source fabricated.'),
 'V12':('actual terminal source-change and timeout injection',['boundary-trials/attempt-001/V12-recovery.json'],'SOURCE_CHANGED and timed-out partial file retained; new-run requirement explicit.'),
 'V13':('root-supervised full-proposal/historical-baseline case',['handoff-trials/attempt-001/V13-observation.json','handoff-trials/attempt-001/assessment/revision-spec.md','handoff-trials/attempt-001/baseline-verification.json'],'Real prior generated baseline verified by hashes; complete proposal and pending review produce REVIEW_REQUIRED. Record helper does not invent missing check coverage.'),
 'V14':('independent cold validator task',['task-trials/valid-001/results/handoff.json'],'Reviewable complete proposal retained with execution BLOCKED for missing baseline/adoption prerequisites.'),
 'V15':('root-supervised actual-byte revalidation fixture',['handoff-trials/attempt-001/V15-observation.json'],'Resolved/persistent/new findings mapped from distinct byte sets; previous findings/report unchanged. Incoming result is explicitly synthetic; no new builder execution claimed.'),
 'V16':('validator self-review, not independent verification',[self_receipt['report']['path'],'self-review/final-receipt.json'],'Same selected checks, disjoint evidence and target readback; stale evidence digest failure retained and corrected in fresh attempt.'),
 'V17':('independent description classification',['routing/comparison.json','routing/attempt-001/task-receipt.md'],'12/12 matches; native implicit invocation NOT_RUN.'),
 'V18':('independent deterministic CLI regressions',['helper-tests/report.md'],'Exclusions, file/byte ceilings, unsafe paths, duplicate/non-finite JSON and symlink cases executed.'),
 'V19':('independent CLI status regressions and cold task',['helper-tests/report.md','task-trials/defect-001/results/validation-report.md'],'FAIL precedence preserves incomplete behavior 6/8 coverage; readiness remains separate.'),
 'V20':('independent stale-authorization regressions plus changed-proposal fixture',['helper-tests/report.md','handoff-trials/attempt-001/V20-observation.json'],'Changed proposal/target approval binding rejected or marked fresh-review required; no prior approval reused.')}
coverage=[]
for case,(method,paths,observation) in case_map.items():
    coverage.append({'case_id':case,'method':method,'observation':observation,'evidence':[reference(ROOT/p) for p in paths],'execution_state':'OBSERVED','native_or_independent_limits':method})
write(ROOT/'acceptance-case-observations.json',{'schema_version':'1','run_id':'20260912T155029Z','cases':coverage,'interpretation':'Bounded synthetic acceptance observations; expected FAIL/INCOMPLETE target outcomes are successful validator observations. Method labels are not interchangeable with native task execution.'})
evidence_paths=['acceptance-case-observations.json','helper-tests/helper-observation.json','routing/comparison.json','self-review/final-receipt.json','task-trials/valid-001/results/validation-report.md','task-trials/defect-001/results/completion-receipt.json','task-trials/ambiguity-001/results-001/validation-report.md','delivery-readback.json']
write(ROOT/'build-verification-observations.json',{'schema_version':'1','run_id':'20260912T155029Z','target_name':'skill-validator','outputs':[{'path':r['path'],'sha256':r['sha256']} for r in current['files']],'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':{'structural':'PASS','spec-v1-delivered':'PASS','helper_regressions':'34 PASS; 62 CLI calls; 0 skipped','independent_validator_tasks':'3 executed; two defect assessments FAIL and one origin-conflict INCOMPLETE as expected','routing':'12/12 independent classification','self_review':'labeled; separate from independent trials'},'artifacts':[{'original_evidence_path':str(ROOT/p),'sha256':digest((ROOT/p).read_bytes())} for p in evidence_paths],'preserved_inputs':preserved,'limitations':['No native implicit invocation observed.','V15 uses synthetic delivered-result byte sets, not a new builder campaign.','Some target workflows remain NOT_RUN because their fixture contract is unresolved; the validator task itself executed and reported this.','Self-review and root-supervised cases are not independent verification.','No operational installation or Rust enforcement/qualification.']})
# All required observations and actual delivered re-evaluation/readback precede this final unpublished accounting input.
code,folder=evaluate('final-publication-001',target,completed=True); assert code==0
snap=folder/'snapshot'
for result in [json.loads(l) for l in (folder/'results.jsonl').read_text().splitlines()]:
    assert result['status']=='PASS' and result['expectation_met']
    assert digest((folder/'cases.jsonl').read_bytes())==result['cases_sha256']
    for path,sha in result['candidate_digests'].items(): assert digest((snap/path).read_bytes())==sha
assert inventory(target)['files']==current['files']
(ROOT/'evidence').mkdir(exist_ok=False)
for p in (snap/'evidence').iterdir():
    if p.name!='build-contract.json': (ROOT/'evidence'/p.name).write_bytes(p.read_bytes())
# Publication is a copy of evaluated provenance, after final source/delivery readback.
(ROOT/'build-provenance.json').write_bytes((snap/'evidence/build-provenance.json').read_bytes())
assert digest((ROOT/'build-provenance.json').read_bytes())==digest((snap/'evidence/build-provenance.json').read_bytes())
provenance=json.loads((ROOT/'build-provenance.json').read_text())
for row in provenance['outputs']: assert digest((ROOT/row['baseline_path']).read_bytes())==row['baseline_sha256']
for row in provenance['evidence']: assert digest((ROOT/row['path']).read_bytes())==row['sha256']
write(ROOT/'publication-receipt.json',{'schema_version':'1','run_id':'20260912T155029Z','status':'DEVELOPMENT_BUILD_COMPLETE','published_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provenance':reference(ROOT/'build-provenance.json'),'evaluated_provenance':reference(snap/'evidence/build-provenance.json'),'final_results':reference(folder/'results.jsonl'),'all_emitted_candidate_and_case_digests_read_back':True,'delivered_unchanged':True,'source_inputs_unchanged':True,'authority':'NONE'})
package_digest=digest(json.dumps(current['files'],ensure_ascii=False,separators=(',',':')).encode())
report=f'''# Skill-validator development build report

Status: **COMPLETE within the specified development build scope**. The 15-file package is delivered at `C:/Projects/DevForgeAI/src/agents/skills/skill-validator`. Package digest: `{package_digest}`. This result is development verification, not framework acceptance or installation.

| Dimension | Result | Evidence |
| --- | --- | --- |
| Authoring | COMPLETE | SV-001–SV-014 and V01–V20 retained; [contract](build-contract.json) preceded candidate generation, [creation receipt](contract-created.json). |
| Installed Skill Creator structural check | PASSED | Candidate, delivered and final frozen inputs; exact checker/commands under commands/. |
| Deterministic accounting | PASSED | Explicit spec-v1: package_links and build_traceability pass in candidate-001, delivered-001 and final-publication-001. Each has an exact pre-execution snapshot/case file and full readback. |
| Helper regressions | PASSED | [34 tests, 62 CLI executions, zero skips](helper-tests/report.md); frozen final helper/tests match delivered bytes. |
| Independent behavioral trials | EXECUTED; expected findings observed | Three cold validator tasks. Receipt arithmetic target: FAIL with real precision defect; dispatch target: FAIL with eight findings and incomplete coverage retained; competing-origin target: INCOMPLETE/BLOCKED with continued independent checks. |
| Bounded contract cases | OBSERVED | [All V01–V20 mappings and method limits](acceptance-case-observations.json). Root-supervised, deterministic, independent and synthetic-result observations are explicitly distinct. |
| Routing classification | PASSED | [12/12 independent classifications](routing/comparison.json). Native implicit invocation NOT_RUN. |
| Validator self-review | SEPARATE, PASSED bounded checks | [V16 report]({self_receipt['report']['path']}); author self-review, not independent proof. |
| Framework enforcement | NOT_IMPLEMENTED | No hooks, CI, mutation broker or framework CLI. |
| Rust qualification / operational installation | NOT_PERFORMED | Outside the authorized scope. |

## Request and contract

Current user request explicitly authorized generation from `docs/plan/skill-validator-spec.md`, disposable verification trials and independent agents. The older SKILL-SPEC-013 input and blocked-build directory remain unchanged. The [preservation receipt](build-verification-observations.json) also verifies the loaded operational builder, development builder and all original trial targets unchanged. No existing project skill was repaired. No dependencies or skills were installed.

The approved specification raw SHA-256 is `{contracts['inputs'][0]['sha256']}`. [Build contract](build-contract.json) SHA-256 is `{digest((ROOT/'build-contract.json').read_bytes())}`. The contract contains source byte intervals for SV-001 through SV-014, bidirectional artifact mappings, essential capabilities and independent worker contracts. [SPEC GAPS](spec-gaps.json): none unresolved for the generated package and required build observations.

## Sources and freshness

Retained current-session [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), linked [Agent Skills format](https://agentskills.io/specification), and official prompt/model/citation pages are indexed with extracted-content digests in [sources](guidance/sources.json). Local historical copies remain snapshot_only with unknown original retrieval dates. The bundled rules catalog is a dated fallback; it cannot claim future current-live coverage. Format requirements, recommendations and project policy stay distinct. The installed checker omits the standard's compatibility field; that discrepancy is documented rather than imposed universally.

## Actual behavior and evidence limits

[Receipt assessment](task-trials/valid-001/results/validation-report.md) found a genuine unintended long-decimal precision defect in its synthetic target. Four specified cases and three rejection boundaries passed. An initial notation comparator was too strict; its failure and corrected numeric comparison are retained, and a separate predeclared numeric-loss case substantiates the finding.

[Dispatch assessment](task-trials/defect-001/results/validation-report.md) found missing transitions/producer, schema conflicts, a scoring ritual, missing resource/capability and actual boolean/partial-overwrite behavior. Six script trials ran. Its complete-success/native target checks remain NOT_RUN because the fixture contract is unresolved; the validator itself executed the required cold task and correctly retained FAIL with 6/8 coverage.

[Ambiguity assessment](task-trials/ambiguity-001/results-001/validation-report.md) retained both specifications and continued structure/readback checks; no governing origin or repair was invented. Its required target behavior is unperformed and honestly reported. This is the expected input-gap observation, not a passing target assessment.

V01 uses a separate minimal instruction-only fixture. V08 uses an actual missing executable lookup with transport deliberately unavailable in the fixture. V12 actually changes copied source bytes and times out a subprocess after partial output. V13 verifies real retained generated history and produces a full pending proposal. V15 compares actual distinct byte sets modeling a delivered result; it is not a newly executed builder campaign. Independent helper tests cover strict malformed records, bounds and stale approvals. These method limits are explicit in the case register; no native implicit activation or cross-platform qualification is claimed.

## Retained failures and retries

Helper attempt-001 failed a defective READY positive control; attempt-002 passed 33 tests; after a strict numeric-overflow fix, attempt-003 passed 34. All remain intact. Cold dispatch record attempt-001 rejected stale line locators; corrected attempt-002 passed 70 references. Self-review record attempt-001 rejected a stale origin reference digest; a fresh evidence-only retry passed. The real timeout and source-change negatives remain negative observations. One preliminary checker command accidentally selected skill-builder; it is retained under commands/candidate-early and is not credited as validator verification. One exploratory nonexistent grader filename read is disclosed in the command log.

## Delivery and provenance

Generated baseline bytes remain separate in [generated-baseline](generated-baseline/SKILL.md). Actual delivered files were re-evaluated and fully read back before [successful provenance](build-provenance.json) was published. [Final evaluator input](evaluations/final-publication-001/snapshot/evidence/build-provenance.json), [results](evaluations/final-publication-001/results.jsonl), [publication receipt](publication-receipt.json) and [destination manifest](destination-manifest.json) bind the delivered bytes. Provenance paths resolve against this build evidence root or its identical bounded final evaluator layout. All cited files already existed at digest time; final results are linked by this report, not recursively cited as their own input.

[Command log](command-log.md), per-command exact argv/streams, independent prompts, snapshots/case files and failures remain outside the generated package. Successful evaluator flags provide deterministic accounting; the semantic/task observations remain separately labeled.

Next authorized action is the separate read-only skill-builder assessment using this delivered validator. It does not authorize repair, adoption, installation or invoking skill-builder.
'''
(ROOT/'build-report.md').write_text(report,encoding='utf-8')
write(ROOT/'build-report-readback.json',{'report':reference(ROOT/'build-report.md'),'provenance':reference(ROOT/'build-provenance.json'),'package_digest':package_digest,'package_files':len(current['files']),'required_checks_completed':True,'completion_boundary':'development package only'})
print(json.dumps({'status':'DEVELOPMENT_BUILD_COMPLETE','package':str(target),'report':str(ROOT/'build-report.md'),'provenance':str(ROOT/'build-provenance.json'),'package_digest':package_digest}))
