"""Evidence-backed QA synthesis and final source protection readback."""
import json
from pathlib import Path
import re
import sys
from harness import RUN, ROOT, TARGET, LOADED, CHECKER, SPECS, read, write, save, ref, sha, compact, inventory, execute, now

BUILD=ROOT/'docs/plan/skill-adaptive-implementations/skill-validator/20260913T211315150947Z'
PRIOR=ROOT/'docs/plan/skill-validations/skill-validator/20260913T201813155594Z'
candidate=json.loads(read(BUILD/'candidate-manifest.json'))
current=inventory(TARGET)
assert current['files']==candidate['files']
results=json.loads(read(RUN/'probe-results.json'))+[json.loads(read(RUN/'results/H11.json'))]
assert len(results)==37 and all(r['matched'] for r in results)
full=read(RUN/'commands/FULL-REGRESSION/stderr.txt').decode()
baseline=read(RUN/'commands/PRE-REPAIR-FAILURE-CONTROL/stderr.txt').decode()
assert 'Ran 249 tests' in full and 'FAILED (failures=7)' in full
fail_names=re.findall(r'^FAIL: ([^\n]+)',full,re.M)
baseline_names=re.findall(r'^FAIL: ([^\n]+)',baseline,re.M)
assert fail_names==baseline_names and len(fail_names)==7
assert len({name.split(' (')[0] for name in fail_names})==1
coverage=json.loads(read(RUN/'coverage/coverage.json'))['totals']
line=100*coverage['covered_lines']/coverage['num_statements']
branch=100*coverage['covered_branches']/coverage['num_branches']
readbacks={}
for name,path,beforepath in [('target',TARGET,BUILD/'candidate-manifest.json'),('loaded-evaluator',LOADED,BUILD/'inputs/loaded-evaluator-before.json'),('companion',ROOT/'src/agents/skills/skill-builder',BUILD/'inputs/companion-before.json')]:
    before=json.loads(read(beforepath)); after=inventory(path)
    assert before['files']==after['files']
    save(RUN/'readback'/f'{name}-after.json',after)
    readbacks[name]={'unchanged':True,'package_digest':after['package_digest'],'files':len(after['files'])}
for name,digest in SPECS.items():
    assert sha(read(ROOT/'docs/plan'/name))==digest
    readbacks[name]={'unchanged':True,'sha256':digest}
for name in ('finding-validation-report.md','revision-spec.md','final-receipt.json','expectations-before-execution.json'):
    # Selected originals are bound now and compared with earlier pinned copies
    # where available; no unsupported whole-tree preservation claim.
    if name=='revision-spec.md': assert sha(read(PRIOR/name))==sha(read(BUILD/'inputs/revision-spec.md'))
    readbacks['prior/'+name]=ref(PRIOR/name)
save(RUN/'final-input-readback.json',{'time':now(),'inputs':readbacks,'extent':'Target candidate, complete loaded and companion packages, governing specs. Prior fixture preservation is in each replay receipt; no whole historical tree claim.'})
prior_findings=json.loads(read(PRIOR/'finding-matrix.json'))['findings']
resolution=[]
for f in prior_findings:
    cases=[r for r in results if r['finding']==f['qa_id']]
    resolution.append({'qa_id':f['qa_id'],'finding_id':f['stable_id'],'status':'RESOLVED','before_digest':'d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1','after_digest':current['package_digest'],'cases':[r['case_id'] for r in cases],'all_match':all(r['matched'] for r in cases),'evidence':[r['evidence'] for r in cases]})
save(RUN/'resolution-map.json',{'target_digest':current['package_digest'],'findings':resolution,'scope':'Four selected defects only; full acceptance separately FAIL.'})
save(RUN/'coverage-summary.json',{'line':{'covered':coverage['covered_lines'],'total':coverage['num_statements'],'percent':line,'threshold':95,'result':'FAIL'},'branch':{'covered':coverage['covered_branches'],'total':coverage['num_branches'],'percent':branch},'regression_methods':{'pass':248,'total':249,'percent':100*248/249,'failed_methods':1,'failed_subtests':7,'result':'FAIL despite numeric floor met'},'probe_cases':{'pass':37,'total':37},'no_combined_percentage':'Independent probe, regression method and review-corpus denominators remain separate.'})

report=f'''# Fresh repair QA

**QA-01 through QA-04 are RESOLVED on the delivered candidate. Full package acceptance remains FAIL.**

## Remaining findings first

1. **Existing regression assertion mismatch:** one unchanged authoring test method fails in seven subtests. It expects `must be an array`; the current companion reader emits `$.<field>: wrong type`. The exact same seven failures reproduce on the untouched pre-repair 75-file validator snapshot with the same companion. This is not introduced by the selected repairs. No assertion was weakened and no companion file was changed. [Current run](commands/FULL-REGRESSION/stderr.txt), [pre-repair control](commands/PRE-REPAIR-FAILURE-CONTROL/stderr.txt), [controlled input identity](baseline-failure-plan.json).
2. **Coverage requirement unmet:** executed-line coverage is {coverage['covered_lines']}/{coverage['num_statements']} = **{line:.4f}%**, below 95%. Branch coverage is {coverage['covered_branches']}/{coverage['num_branches']} = {branch:.4f}%. All nine first-party executable support scripts were declared before collection; no first-party exclusions or aliasing of temporary code copies to pristine paths. This is Windows Python coverage, not Rust coverage. [Measurement](coverage-summary.json), [denominator](coverage/denominator-before-run.json).

## Selected repairs

| Finding | Result | Evidence |
| --- | --- | --- |
| QA-01 duplicate execution/artifact counts | RESOLVED | D01-D05, REPLAY-R06; new duplicate/different-run/shared-citation regressions |
| QA-02 required handoff excluded as N/A | RESOLVED | H01-H11, REPLAY-R07; contradictory-N/A and unknown regressions |
| QA-03 missing protocol Unicode candidate | RESOLVED | U01-U07, REPLAY-P08; JSONL, multiline locations and redaction regressions |
| QA-04 premature fence closure | RESOLVED | F01-F10, REPLAY-P07; true line-5 edge, literal line-3 example and anchor regressions |

All **37 retained cases pass**, with zero observed false positives or missed expected detections in that selected corpus. Expected outcomes were retained before execution; originals were replayed read-only and independent fixtures were reconstructed in this fresh run. The complete suite discovered **249 test methods**, versus the previous 229: the increase is exactly 20 new focused methods. **248/249 methods pass**; one method has seven failing subtests, all reproduced before the repair. Counting 249 minus seven would incorrectly mix method and subtest denominators. All 20 added methods pass; their initial run retained 13 requirement failures and no setup errors.

The independent reviewer used a separate agent context, verified candidate identity, reviewed record-integrity changes, and executed 16 additional JSON/fence/anchor probes: all matched. Its accounting/handoff review is static; root's retained public-interface probes supply executed coverage. Same-model review is not enforced isolation or protected acceptance. [Independent report](independent-review/independent-review.md).

Installed quick_validate.py passes on the captured candidate. The bound evaluator ran the actual legacy-import-v1 profile and emitted two matching JSONL observations after validating artifact binding. Full regression tests also exercised the existing compatibility profiles. A valid structural/profile result does not override the failed regression or coverage requirement.

## Identity, scope and effects

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-validator`; **76 files**, package digest `{current['package_digest']}`. Changes are exactly two production scripts, one added test file, and the evaluation manifest. Existing tests and schemas were preserved. Both frozen specification hashes match. The operational evaluator remains the original 75-file package; it was loaded as instructions but was not installed or updated. Target helpers assessing target behavior are self-review, supplemented by independent expectations and the separate reviewer.

Executed with native Windows Python on the C: checkout, with installed coverage.py and PyYAML. Temporary roots and coverage startup helper are confined to this QA run; no installed sitecustomize or environment configuration was changed. No WSL checkout switch, dependency installation, real binding, operational-copy edit, remote publication, or Rust change occurred. Target candidate, companion and operational evaluator match final readback; replay receipts verify fixture preservation. Whole operational homes/historical trees were not captured.

## Closure

Selected defect remediation: **PASS**. Full regression: **FAIL (existing mismatch)**. Line-coverage floor: **FAIL**. Full package acceptance: **FAIL**. Native whole workflow/resume, activation, lifecycle integration, tokenizer qualification, installation and Rust qualification remain NOT_RUN or NOT_PERFORMED in this scoped maintenance.

Next work is a separately scoped reconciliation of the authoring test's expected error contract, additional meaningful coverage for uncovered first-party behavior, and the previously unperformed acceptance scenarios. The four repaired defects do not need reopening on the evidence available. [Resolution map](resolution-map.json), [commands](command-log.md), [final readback](final-input-readback.json).
'''
write(RUN/'qa-report.md',report)

# Keep schema-1 evidence isolated from supplemental raw adaptive observations.
records=RUN/'member-records'
save(records/'source-manifest.json',current)
save(records/'source-after-manifest.json',current)
for r in current['files']: write(records/'source'/r['path'],read(RUN/'source'/r['path']))
write(records/'inputs/spec.md',read(RUN/'inputs/skill-validator-adaptive-enhancement-spec.md'))
write(records/'inputs/qa-report.md',read(RUN/'qa-report.md'))
write(records/'inputs/coverage.json',read(RUN/'coverage-summary.json'))
write(records/'inputs/regression.txt',read(RUN/'commands/FULL-REGRESSION/stderr.txt'))
checks=[]
for result in results:
    cid=result['case_id']; q=int(result['finding'][-1])-1
    write(records/'inputs'/f'{cid}.json',read(RUN/'commands'/cid/'stdout.txt'))
    checks.append(dict(schema_version='1',run_id=RUN.name,check_id=cid,rule_id=['AV-E01','AV-A10','AV-U01','AV-R01'][q],subject_path='scripts/adaptive_observe.py' if q<2 else 'scripts/text_resources.py',method='deterministic',required=True,applicability='applicable',result='PASS',reason='Matched pinned independent expected output and preservation.',evidence=[ref(records/'inputs'/f'{cid}.json',records)],dimension='workflow' if q<2 else 'standards'))
    write(RUN/'supplemental-records'/f'{cid}.json',read(RUN/'commands'/cid/'stdout.txt'))
for cid,evidence,reason in [('REGRESSION','regression.txt','One required existing test method fails in seven subtests, also before repair.'),('COVERAGE','coverage.json','Measured full first-party support-script line coverage is below 95%.')]:
    checks.append(dict(schema_version='1',run_id=RUN.name,check_id=cid,rule_id='AV-E01',subject_path='SKILL.md',method='deterministic',required=True,applicability='applicable',result='FAIL',reason=reason,evidence=[ref(records/'inputs'/evidence,records)],dimension='behavior'))
write(records/'checks.jsonl',b'\n'.join(compact(c) for c in checks)+b'\n')
save(records/'findings.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',findings=[]))
save(records/'origin-record.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',original_source_root=str(TARGET),manifest=ref(records/'source-manifest.json',records),specification=ref(records/'inputs/spec.md',records),origin_kind='existing_spec',history_kind='observed',prior_evidence=None,completeness='complete',uncertainties=['Existing generated/adopted history is not reclassified by this scoped edit.'],source_readback_state='UNCHANGED',historical_origin='unknown'))
for cid,program,root in [('LEGACY-RECORDS','observe.py',records),('ADAPTIVE-RECORDS','adaptive_observe.py',RUN/'supplemental-records')]:
    observation=execute(cid,[sys.executable,'-B','-X','utf8',str(TARGET/'scripts'/program),'records','--run-root',str(root)])
    print(cid,observation['exit'])
print('Line',line,'Branch',branch,'Full regression 248/249 methods; seven subtest failures in one existing method.')
