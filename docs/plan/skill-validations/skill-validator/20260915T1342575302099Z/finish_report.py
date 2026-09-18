import datetime,hashlib,json,os,pathlib,re,shutil,sys
from run_checks import command
R=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('C:/Projects/DevForgeAI')
OPS=ROOT/'.agents/skills/skill-validator/scripts'
def save(p,v):
    p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')
def text(p,v):
    with (R/p).open('x',encoding='utf-8',newline='\n') as f:f.write(v)
def ref(p):
    p=R/p;return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def external_ref(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
M=json.loads((R/'source-manifest.json').read_text())
# Exact raw-byte specification captures complement the earlier decoded text representations.
raws=[]
for source in [ROOT/'AGENTS.md',ROOT/'docs/plan/skill-validator-spec.md',ROOT/'docs/plan/skill-validator-adaptive-enhancement-spec.md']:
    dest=R/'inputs/raw'/source.name;dest.parent.mkdir(exist_ok=True)
    shutil.copyfile(source,dest);raws.append({'original_path':str(source),'captured':ref(dest.relative_to(R))})
save('inputs/raw-bindings.json',raws)
shutil.move(str(R/'snapshot-observation.json'),str(R/'inputs/snapshot-observation.json'))
# Bounded original-document lookup, excluding historical assessment and implementation evidence trees.
lookup=[]
for root in [ROOT/'docs/plan',ROOT/'docs/design/specs']:
    if root.exists():
        for p in sorted(root.iterdir()):
            if p.is_file() and p.suffix.lower()=='.md' and not p.is_symlink():
                raw=p.read_text(encoding='utf-8-sig')
                match=re.match(r'---\s*\n(.*?)\n---',raw,re.S)
                if match and re.search(r'^skill_name:\s*skill-validator\s*$',match[1],re.M):
                    lookup.append({'original_path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
save('inputs/origin-lookup.json',{'scope':'Top-level original Markdown specifications in both documented roots; nested historical run/capture/implementation evidence excluded. No directory precedence.','matches':lookup})
command('source-readback',[sys.executable,'-B','-X','utf8',str(OPS/'observe.py'),'readback','--source',str(ROOT/'src/agents/skills/skill-validator'),'--manifest',str(R/'source-manifest.json')])
readback=json.loads((R/'commands/source-readback/stdout.txt').read_text())
save('source-after-manifest.json',readback['manifest'])
save('origin-record.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-validator','original_source_root':str(ROOT/'src/agents/skills/skill-validator'),'source_manifest':ref('source-manifest.json'),'specification':ref('inputs/raw/skill-validator-spec.md'),'origin_kind':'existing_spec' if len(lookup)==1 else 'unresolved','history_kind':'observed','prior_evidence':None,'complete':M['complete'],'uncertainties':['Historical generated/adopted lineage not verified. Supplemental enhancement requirements and observed current resources inform this assessment; no new origin reconstructed.'],'source_readback_state':readback['status']})
command('dependency-readback',[sys.executable,'-B','-X','utf8',str(OPS/'observe.py'),'readback','--source',str(ROOT/'src/agents/skills/skill-builder'),'--manifest',str(R/'inputs/builder-dependency/source-manifest.json')])
save('inputs/rule-spec-readback.json',{'original_files':[{'path':v['original_path'],'unchanged':hashlib.sha256(pathlib.Path(v['original_path']).read_bytes()).hexdigest()==v['captured']['sha256']} for v in raws],'pinned_sources':[{'source_id':v['source_id'],'unchanged':hashlib.sha256((R/v['snapshot_path']).read_bytes()).hexdigest()==v['sha256']} for v in json.loads((R/'sources.json').read_text())['sources']]})
text('trials/routing-observation.md','Cold description-only subagent /root/description_routing, no parent history: MATCH, MATCH, MATCH, NO_MATCH, NO_MATCH, NO_MATCH. Reasons: selected skill audit; specification testing; revalidation; product repair excluded; installation excluded; creation outside validation. All six match the predeclared labels. This is not native discovery.\n')
cold=R/'trials/cold/project/docs/plan/skill-validations/invoice-total/20260915T134720167905Z'
cold_plan=json.loads((R/'trials/cold/plan.json').read_text())
cold_unchanged=all(hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256'] for v in cold_plan['inputs'])
save('trials/cold/assessment.json',{'executor':'collaboration /root/cold_validator; fork_turns=none; inherited host; task-scoped write boundary only','completed_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':600,'result':'PARTIAL','preserved_inputs':cold_unchanged,'report':ref((cold/'validation-report.md').relative_to(R)),'proposal':ref((cold/'revision-spec.md').relative_to(R)),'finding':ref((cold/'findings.json').relative_to(R)),'observations':['PASS: delivered report, defect detection, proposal, no repair and no framework acceptance. Independently executed mixed, negative-only, positive, zero, empty and large-number cases.','NOT_RUN: predeclared sample-specific 1300-versus-800 observation. Actor used equivalent independent cases (120 versus 100 and 0 versus -20); do not retroactively claim exact sample execution.','NOT_RUN: native CLI discovery; separate cold subagent execution is not implicit activation.'],'limits':['Full actor tool transcript is not exported; actor-retained commands, plans and artifacts plus parent task/result identify this trial.','This is validator self-review with a held-out task context, not enforced independent qualification.']})
text('semantic-review.md',"""# Semantic and test-integrity review

This is validator self-review. A cold subagent received only the skill, synthetic task, specification and permitted effects; no expected answer or historical finding was supplied.

## Structure, text and resources

The selected entrypoint is 12,181 bytes, 12,181 Unicode characters and 75 physical lines. The manifest binds its original directory name skill-validator; the temporary name source is not an identity defect. The 61 parsed Markdown resource edges resolve. The only Unicode candidate is fullwidth p in tests/test_adaptive.py:102, an intentional confusable-command fixture whose assertions check detection and redaction. Placeholder candidates in references/set-trials.md:81 and references/text-resource-checks.md:18 describe positive/negative fixtures, not unfinished instructions. No optional agents/openai.yaml is present or required. No token budget was selected; no tokenizer was run.

Referenced instructions supply actual input, output, continuation and failure branches. scripts modules are consumed by entrypoint commands or local imports; schemas/assets and evals have reference/runner consumers; tests are intentionally reachable through unittest discovery documented by evals/README.md. Package graph reachability alone does not establish executable imports; cited source inspection and executed regression evidence supply that context. Remote guidance and renderer-specific behavior are not comprehensively crawled.

## Contextual wording

SKILL.md requires fresh capture and readback: useful actionable instructions preserving evidence, not ceremonial scoring. Its statement that Python observations are not framework acceptance accurately limits authority. references/reliable-evaluation.md separates timeouts from product defects and bounds retries; this provides concrete recovery behavior. These safeguards remain in the proposal. Long paragraphs and cross-references can cost context, but no universal length failure or destructive rewrite is justified by these measurements. Native user-correction and adversarial prompt handling were not exercised.

## Test integrity and confirmed integration mismatch

331 standalone/regression cases pass. Two modules initially failed to import without their documented AUTHORING_BUILDER_ROOT dependency. Their 71 real cases were then executed once with captured current development builder bytes; 68 pass, two fail, one errors. The initial loader errors remain in the first log; they are not counted as extra test cases. Total: 399/402, no skipped methods.

Three test assumptions are incompatible with that captured dependency:

- tests/test_authoring.py:139 requires result['issues']. Current builder recheck_stage failure returns a nonempty error, BLOCKED and zero applied paths before entering its legacy issues-return branch. The test errors before its preservation assertions.
- tests/test_authoring_safeguards.py:200 writes into a target that the create fixture has not created. The current before_write callback occurs before target.mkdir, so the callback cannot install a competing file. BLOCKED does not prove a preservation defect; the intended competing-write scenario was not reached.
- tests/test_authoring_safeguards.py:264-273 makes files(target) fail after interruption but does not create the target. Recovery tests target.exists() before calling files, so the planned read failure is not exercised.

This establishes broken integration test expectations/fixtures against the selected dependency, not a product mutation defect or permission to repair builder. No failing test was weakened or rerun. Mock usage reviewed includes bounded limit overrides, simulated links and targeted filesystem fault injection; those do not prove actual OS races or Windows symlink capability. The test suite contains substantive negative assertions, not only metadata checks.

## Coverage and evaluator limitations

Measured line coverage is 3424/3802 (90.05786428195686%); branch coverage is 1593/1908 (83.49056603773585%). No first-party lines were excluded. The denominator includes all 14 captured scripts, including migrated custody/build fixture-support modules. The measurement configuration instruments the captured source path. Tests that copy the evaluator to disposable locations can execute identical code outside that configured source path; those copied-path executions are not credited here. Consequently this measurement does not establish a precise package-wide deficit, but it does not prove the required 95% floor. Correct byte-bound copied-path instrumentation before deciding what extra tests are needed; never discard source from the denominator.

The first coverage aggregation with a changed data basename found no data. Its logs are preserved. Corrected aggregation of the existing chunks succeeded; no tests were repeated for that correction.

Independent CLI probes: seven of eight match the frozen expected exit code. The quoted-inline-link probe incorrectly expected exit 2 although its clean metadata, exact directory identity and absence of Unicode justify exit 0. Its useful no-false-missing-link predicate holds, but the frozen case remains an evaluator ERROR, not a retroactive PASS or target defect. Its plan/results are unchanged.

Description-only routing passed 6/6. The cold workflow detected the seeded credit defect and delivered useful artifacts; its exact sample-specific obligation was not exercised. Native CLI activation, adversarial host input, user correction and other platforms remain NOT_RUN. No comparison, installation or compiled-Rust acceptance was performed.
""")
# One stable source finding; coverage and harness limitations are separately described rather than attributed as production defects.
anchor="self.assertTrue(any('fresh run' in issue for issue in result['issues']))"
identity=['AV-R03','tests/test_authoring.py',anchor,0]
fid='F-'+hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
finding={'finding_id':fid,'identity':identity,'rule_id':'AV-R03','category':'resource_tool_issue','severity':'major','subject_path':'tests/test_authoring.py','source_refs':[ref('source/tests/test_authoring.py'),ref('source/tests/test_authoring_safeguards.py'),ref('source/references/evaluation.md')],'observation_refs':[ref('commands/integration-missing/stderr.txt'),ref('inputs/builder-dependency/source/scripts/authoring.py'),ref('semantic-review.md')],'description':'Three validator-owned integration tests do not reach or correctly assess their intended safeguards against the captured current builder dependency. One assumes a missing issues key; two require a target directory before their callback has created it.','user_impact':'The documented regression suite cannot pass against this dependency, and these failure-path safety scenarios are not qualified.','proposed_correction':'Make failure-record assertions explicit for the selected authoring contract and construct an existing target for competing-write/read-failure scenarios. Preserve mutation, no-baseline, evidence-retention and error-reason assertions. Pin the dependency identity.','preserved_requirements':['No target or dependency repair during validation','No source mutation on blocked publication','Retain competing writer bytes','Expose unavailable readback','Do not weaken failure-path assertions'],'verification_cases':['test_old_noncanonical_stage_requires_fresh_run','test_per_path_concurrent_write_is_preserved','test_unreadable_after_interruption_reports_gap'],'disposition':'proposed'}
save('findings.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-validator','findings':[finding]})
steps=[]
for sid,entry,inputs,action,outputs,branch,failure in [
('intake','SKILL.md / Intake and boundaries',['explicit target','project root'],'Bound snapshot and select origin',['source','manifest','origin-record'],'rules','Retain exclusions or unresolved origin and continue independent checks'),
('rules','references/rules.md',['captured package','official or dated sources'],'Pin authority, applicability and expectations',['sources','rule-set','trial plans'],'inspect','Use disclosed dated fallback; unknown assertions stay unresolved'),
('inspect','references/text-resource-checks.md',['source','rules'],'Run structure/creator/package and adjudicate contextual candidates',['checks','workflow-map','semantic review'],'trials','Retain raw errors and continue independent checks'),
('trials','references/trials.md',['fixtures','frozen oracles','actual host capability'],'Execute bounded disposable tests and retain all attempts',['commands','results','side-effect readback'],'synthesize','Timeout or missing dependency leaves affected checks unperformed'),
('synthesize','references/reporting.md',['checks','findings','readback'],'Reduce each dimension with failure before incomplete',['report','proposal','enforcement register'],'handoff','Unknown or missing obligations remain explicit'),
('handoff','references/handoff.md',['report','target/proposal hashes'],'Deliver reviewable future contract without invoking builder',['handoff','user result paths'],'terminal','Missing baseline or review limits execution readiness'),
('revalidate','SKILL.md / Revalidation and recovery',['later authorized changed package'],'Start fresh linked assessment and compare findings',['new report','resolution evidence'],'terminal','Changed bytes invalidate old approval; retain old evidence')]:
    steps.append({'step_id':sid,'entrypoint':entry,'entry_conditions':'Inputs selected and readable; conditional revalidation only after later delivery','inputs':inputs,'executor':'host agent using documented terminal helpers','action':action,'outputs':outputs,'completion_evidence':'Observed artifacts and checks; no protected phase transition','next_branches':[branch],'failure_route':failure,'terminal_user_outcome':'Evidence-backed report, limitations and review proposal'})
save('workflow-map.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-validator','steps':steps})
rules=json.loads((R/'rule-set.json').read_text())['rules']
checks=[]
for rule in rules:
    rid=rule['rule_id'];result='PASS';reason='Reviewed in semantic-review.md with retained source and command evidence.'
    if rid.startswith('AV-A'):result='NOT_APPLICABLE';reason='Selected target is an ordinary validator skill, with no adaptive descriptor or selected set execution. Adaptive input readers are separately covered in its regression suite.'
    if rid=='AV-F04':result='NOT_APPLICABLE';reason='No optional agents/openai.yaml is present.'
    if rid=='AV-R03':result='FAIL';reason='Three documented integration tests fail against the captured dependency; see stable finding.'
    if rid in ('AV-I04','AV-S01'):result='NOT_RUN';reason='Static boundary review completed; native user-correction/adversarial host behavior was not exercised.'
    if rid=='AV-E01':result='FAIL';reason='Measured line coverage 3424/3802 is below required 95%; copied-path executions are not credited. One independent probe has a retained evaluator-oracle error.'
    if rid=='AV-W01':result='NOT_RUN';reason='Cold actor delivered the report, seeded-defect finding and proposal, but the frozen sample-specific observation was not executed; implicit native CLI discovery is unperformed.'
    dimension='standards' if rid.startswith(('AV-F','AV-U','AV-R','AV-C','AV-E')) else 'instructions' if rid.startswith(('AV-I','AV-S')) else 'workflow'
    if rid in ('AV-W02','AV-R03'):dimension='behavior'
    checks.append({'schema_version':'1','run_id':R.name,'check_id':'check-'+rid,'rule_id':rid,'subject_path':'SKILL.md','dimension':dimension,'method':'semantic' if rid not in ('AV-C01','AV-F01') else 'deterministic','required':True,'applicability':'not_applicable' if result=='NOT_APPLICABLE' else 'applicable','result':result,'reason':reason,'evidence':[ref('semantic-review.md'),ref('commands/structure/stdout.txt'),ref('commands/package/stdout.txt'),ref('coverage-merged/coverage.json'),ref('trials/cold/assessment.json')]})
text('checks.jsonl',''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in checks))
text('enforcement-recommendations.md','# Enforcement recommendations\n\nNo new enforcement candidates selected. Existing boundaries correctly reserve framework acceptance and mutation authority for a separately implemented and qualified compiled Rust service. The observed issues concern test fixtures and measurement; they do not justify new hooks, CI policy, or an invented gate.\n')
text('revision-spec.md',f"""---
id: SKILL-VALIDATOR-REVISION-{R.name}
skill_name: skill-validator
target: codex
status: proposed
---
# Proposed validator test and measurement repair contract

## Identity, purpose and scope

Target: {ROOT/'src/agents/skills/skill-validator'}. Package digest: {M['package_digest']}. Origin is inputs/raw/skill-validator-spec.md; current complete implementation is the 89-file source snapshot. Finding {fid} motivates this proposal. This is a future scoped repair contract; no changes are authorized by this document.

Retain the current skill's purpose: assess explicitly selected Codex skill packages, preserve source and origin, use grounded rules, inspect instructions/resources/workflow, execute bounded disposable tests, deliver findings and a revision proposal, then stop at review. Existing adaptive-set, authoring-intake and legacy assessment interfaces remain unchanged. The snapshot plus preserved origin and linked current references define all unchanged behavior.

## Triggers and inputs

Keep the current description and invocation policy. Validation/revalidation requests activate the skill; creation, repair, installation, product-code audits and framework implementation remain separate. Inputs remain explicit package/project, optional selected specification/prior evidence, current user requirements and available tools. No new metadata or mandatory dependency for ordinary validation is introduced.

The maintenance test task additionally selects a byte-bound development builder dependency and existing Python/PyYAML/coverage tools. AUTHORING_BUILDER_ROOT continues to select that dependency for integration tests only. Do not silently bind an arbitrary installed copy or copy credentials.

## Outputs and operational workflow

Preserve existing schema-1 records, supplemental adaptive records, Python JSONL runner/cases/graders/schemas/manifests and their meanings. Ordinary assessment continues through snapshot, origin, rule pinning, static/semantic review, bounded behavior, readback, report, findings, optional full revision specification and handoff. Missing dependencies produce explicit unperformed checks while independent work proceeds. Reports distinguish observations from compiled-Rust authority.

Maintenance should declare all unique required cases before execution, run them against captured packages with temporary files under the evidence root, and retain every attempt. Load errors must identify missing dependency setup without counting synthetic loader placeholders as additional test cases. Never erase failed attempts or count successful retries twice.

## Mandatory repair requirements

VR-01: Update the noncanonical-stage test to handle the actual selected authoring failure-record contract. Verify BLOCKED, zero applied paths, a concrete recovery reason in the contract-defined error representation, absent successful baseline and unchanged source/contract bytes. Do not reduce this to accepting any exception or nonzero exit.

VR-02: Construct a valid competing-writer fixture at the actual callback boundary. Ensure the synthetic target directory exists when the independent writer writes. Prove the competing write occurred, preserved bytes equal that writer's content, validator/builder applied no replacement, and publication did not create successful custody evidence. Do not merely change PARTIAL to BLOCKED to make the old test pass.

VR-03: Make the interrupted readback fixture reach files(target). Establish the target's existence before injecting read failure. Prove the attempted read and real exception, explicit readback gap, no accepted baseline and retained failed-attempt evidence. Do not assert an error phrase for a branch never exercised.

VR-04: Retain validator-only coverage denominator: every executable line in its 14 captured scripts, with no first-party exclusion. Instrument subprocess/copy execution using verified source identity; only merge a copied file's executed lines when its bytes match the bound source. Report unmapped or changed copies separately. Preserve initial limited measurements. Once measurement is correct, add meaningful negative/integration cases only for genuinely uncovered behavior. Require >=95% line coverage and >=95% unique-case pass rate independently; failed mandatory cases still prevent qualification.

VR-05: Update maintenance invocation guidance if needed to show explicit dependency selection and coverage setup. Ordinary skill execution must remain builder-independent. Retain exact runtime versions, source/dependency manifests, cases, stdout/stderr, duration, source readback and all errors.

## Files and preservation

Primary allowed future test edits: tests/test_authoring.py and tests/test_authoring_safeguards.py (VR-01 through VR-03). Maintenance guidance/evaluation support may implement VR-04/VR-05 after selecting the coverage approach. Preserve SKILL.md, runtime scripts, schemas and legacy record meanings unless an additional demonstrated requirement justifies an explicitly selected change. No edits to src/agents/skills/skill-builder, .agents, prior evidence, source specifications, hooks or startup configuration.

## Dependencies, failure paths and recovery

Use existing Python 3.10+ and PyYAML. Coverage is an evaluation dependency, not a framework authority. Windows fault-injection tests remain Windows-qualified; other platforms need separately reported runs. Preserve setup errors, test failures, timeouts and incomplete source mapping. Re-execution uses fresh attempt directories and unchanged or freshly captured inputs.

## Acceptance and handoff

A1: Execute the three focused original failure scenarios before repair and retain real failures; then verify VR-01/02/03 with independent assertions of reached effects and preservation.
A2: Execute all 402 currently declared unique regression cases (plus justified new cases), with no skipped required cases promoted to pass.
A3: Verify correct byte-bound subprocess/copy coverage and report line/branch numerators and denominators; meet VR-04 without narrowing source.
A4: Repeat relevant cold assessment only if instructions/workflow changed; preserve target/source and distinguish implicit discovery.
A5: Run creator/structure/record checks and target/dependency readback, then deliver evidence for independent validation. These are development checks, not framework acceptance.

The observed source snapshot can support a later authorized scoped edit; no generated/adopted history was verified here. Proposal review is pending. Exact builder failure-contract version and the byte-bound copied-path coverage mechanism need selection before calling this implementation-ready. No repair or installation occurs in this assessment.
""")
text('validation-report.md',f"""# Skill Validator assessment: FAIL

Assessment completed: true. This is validator self-review, using the installed operational validator and Skill Creator guidance, with a separate cold task context.

Target: {ROOT/'src/agents/skills/skill-validator'}  
Package digest: {M['package_digest']}  
Rule-set digest: {ref('rule-set.json')['sha256']}

## Results

| Check | Result |
|---|---|
| Installed Skill Creator checker | PASS |
| Structural scan | PASS |
| Captured package | 89 files; no exclusions; unchanged on readback |
| Regression cases | 399/402 pass (99.25373134328358%); 2 fail, 1 error, 0 skipped |
| Executed-line coverage | 3424/3802 (90.05786428195686%); below 95% |
| Branch coverage | 1593/1908 (83.49056603773585%) |
| Independent helper probes | 7/8 pass; 1 evaluator-oracle ERROR |
| Description routing | 6/6 match |
| Cold task | Detected seeded defect, preserved inputs, delivered report and proposal; exact predeclared sample observation NOT_RUN |
| Native CLI implicit activation | NOT_RUN |
| Compiled-Rust/framework acceptance | NOT_RUN |

The pass-rate floor is met, but mandatory integration failures and unproven coverage floor prevent a passing assessment. Coverage is a measured lower bound for the configured captured paths: copied evaluator executions outside those paths were not credited. No coverage was estimated or rounded up. Every first-party script stays in the denominator.

## Dimensions

Standards/evidence: FAIL due to measurement floor and evaluator error; basic format checks pass. Workflow: INCOMPLETE due to unperformed exact cold sample/native discovery obligations. Instructions: INCOMPLETE for native correction/adversarial-host behavior; static review found no confirmed instruction defect. Behavior: FAIL because three integration cases fail. Enforcement recommendations: no new candidates.

See checks.jsonl for all 29 considered AV rules, including 10 adaptive-only rules and optional configuration marked inapplicable with reasons. Required FAIL takes precedence over unperformed checks.

## Confirmed finding

{fid}: three validator-owned authoring integration tests have stale failure-record/fixture assumptions against the captured current builder dependency. One accesses a missing issues key; two do not create the target needed to reach their fault-injection scenario. See findings.json, semantic-review.md and commands/integration-missing/stderr.txt. These failures do not establish a builder mutation defect. Neither package was repaired.

## Evidence and limits

The first discovery run passed 331 cases and had two module-loading errors because its snapshot lacked the documented sibling dependency. The remaining 71 methods were executed once with AUTHORING_BUILDER_ROOT pointing at inputs/builder-dependency/source. Initial failures remain; loader placeholders are not extra cases. No successful test case was rerun.

All command plans/streams/results are in commands/. Coverage configuration and raw chunks are retained. The failed aggregation attempt and corrected aggregation are separate. Probe plans/results retain the wrong quoted-link exit expectation as evaluator error, with no retroactive PASS.

The cold invoice assessment contains six actual script cases and a supported negative-credit finding. It delivered a full proposed contract. The actor chose other equivalent examples rather than the parent's exact sample; that specific observation remains unperformed. Its FAIL describes the intentionally defective invoice fixture, not failure to identify it. Full parent/child OS isolation and independent model qualification are not claimed.

Environment: Windows 10.0.26200, PowerShell 7.6.6, C:/Program Files/Python310/python.exe 3.10.11, PyYAML 6.0.2, coverage 7.9.0, native C: filesystem; cwd C:/Projects/DevForgeAI. Codex CLI 0.154.0 was discovered but no standalone CLI workflow trial was run. CLI discovery emitted access warnings for its temporary PATH-alias directory; no installation or permission change was attempted.

## Origin and guidance

Existing exact-name base specification is retained byte-for-byte under inputs/raw/. Historical generated/adopted lineage was not inferred. Supplemental enhancement content is preserved as context. OpenAI Build skills was fetched live and retained; broader project AV rules and bundled standard summaries remain pinned dated guidance. No current-live claim beyond retrieved material. [Official skill guidance](https://learn.chatgpt.com/docs/build-skills) supports the format, progressive disclosure and trigger distinctions used here.

Source, rule/specification and builder-dependency readbacks are retained. Source was unchanged. No operational skills, specifications or historical evidence were edited.

## Proposed repair and next action

[Revision proposal](revision-spec.md) addresses the three tests and correct coverage measurement before adding missing tests. [Findings](findings.json), [semantic review](semantic-review.md), [workflow map](workflow-map.json), [checks](checks.jsonl), and [handoff](handoff.json) retain supporting detail.

Proposal review: pending. Builder execution: BLOCKED pending selection of the precise integration failure contract and coverage mapping, plus future scoped-edit authorization/intake. No repair is requested or executed by this report. The next authorized work is the proposed test/measurement repair, followed by fresh validation.
""")
save('handoff.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-validator','original_target_root':str(ROOT/'src/agents/skills/skill-validator'),'original_manifest':ref('source-manifest.json'),'origin':ref('origin-record.json'),'proposed_spec':ref('revision-spec.md'),'findings':ref('findings.json'),'report':ref('validation-report.md'),'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'pending','review_instruction':None,'builder_readiness':'BLOCKED','readiness_reasons':['Select exact dependency failure contract and byte-bound copied-path coverage mechanism; future repair/intake has not been authorized.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':False,'adoption_capability':'Not inspected; current observed scoped-edit compatibility is described by the package. No generated/adopted baseline asserted.','permitted_target_root':str(ROOT/'src/agents/skills/skill-validator'),'preservation_requirements':['No repair during validation','Preserve operational and companion packages','Preserve all prior evidence'],'target_package_digest':M['package_digest']})
logs=['# Commands and outcomes\n','Read-only PowerShell discovery inspected package, applicable skills, runtime and referenced contracts before executions. Initial registry memory lookup informed separation of deterministic/native results; historical counts were not used as current results.\n']
for d in sorted((R/'commands').iterdir()):
    if (d/'result.json').exists():
        p=json.loads((d/'plan.json').read_text());v=json.loads((d/'result.json').read_text())
        logs.append('## '+d.name+'\n\n'+json.dumps(p['argv'])+'\n\n'+json.dumps(v)+'\n')
text('command-log.md','\n'.join(logs))
print('Report written',fid)

