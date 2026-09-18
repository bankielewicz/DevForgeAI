"""Bind and evaluate this forward trial, then deliver and read back exact bytes."""
import json
import sys
from trial_support import *

def recheck_inputs():
    before=json.loads((EVIDENCE/'original-inputs-before.json').read_bytes())
    after=dict(schema_version='1',files=[dict(path=row['path'],bytes=len(Path(row['path']).read_bytes()),sha256=sha(Path(row['path']).read_bytes())) for row in before['files']])
    write_json(EVIDENCE/'original-inputs-after.json',after)
    assert before==after,'Original input changed'
    log(dict(cwd=str(ROOT),action='Rechecked selected spec and supplied fixture byte sets/sizes/SHA-256',files=after['files'],interpretation='Original inputs unchanged'))

def provenance(phase, result, manifest_sha):
    contract=json.loads((EVIDENCE/'build-contract.json').read_bytes())
    observation=EVIDENCE/('observations-'+phase+'.json')
    shutil.copyfile(observation,SNAP/'evidence'/observation.name)
    measured=outputs(SNAP/'destination')
    assert measured==outputs(SNAP/'baseline')
    value=dict(schema_version='1',run_id=RUN,mode='spec_build',target_name=NAME,builder_manifest_sha256=manifest_sha,contract_sha256=sha((EVIDENCE/'build-contract.json').read_bytes()),inputs=[dict(id=row['id'],sha256=row['sha256']) for row in contract['inputs']],dependencies=contract['dependencies'],outputs=[dict(path=row['path'],sha256=row['sha256'],ownership='generated',baseline_path='baseline/'+row['path'],baseline_sha256=row['sha256']) for row in measured],mappings=[dict(requirement_id=row['id'],artifact_paths=row['artifact_paths'],evidence_ids=['executed-observations']) for row in contract['requirements']],evidence=[dict(id='executed-observations',path='evidence/'+observation.name,sha256=sha(observation.read_bytes()))],prior_build=None,result=result)
    write_json(EVIDENCE/('build-provenance-'+phase+'.json'),value)
    write_json(SNAP/'evidence/build-provenance.json',value)
    if phase=='delivered':
        write_json(EVIDENCE/'build-provenance.json',value)

def evaluate(phase):
    result=command([sys.executable,'-B','-X','utf8',BUILDER/'scripts/run_evaluation.py','--package-root',BUILDER,'--candidate-root',SNAP,'--cases',EVIDENCE/'evaluation-cases.jsonl','--output',EVIDENCE/('evaluation-results-'+phase+'.jsonl'),'--run-id',RUN+'-'+phase,'--profile','spec-v1'],'Required spec-v1 deterministic evaluation of '+phase)
    assert result.returncode==0,'Required evaluator failed; evidence retained without retry'
    records=[json.loads(line) for line in (EVIDENCE/('evaluation-results-'+phase+'.jsonl')).read_text(encoding='utf-8').splitlines()]
    assert len(records)==2 and all(row['status']=='PASS' and row['expectation_met'] for row in records)
    return records

def main():
    expected_sha=sys.argv[1]
    actual_sha=sha((BUILDER/'evals/build-manifest.json').read_bytes())
    assert actual_sha==expected_sha,'Builder manifest drift; no binding performed'
    log(dict(cwd=str(ROOT),action='Parent authorized final binding after its builder repair; new digest explicitly checked',builder_manifest_sha256=actual_sha,interpretation='Earlier contract and successful script observations retained; no builder repairs performed by this forward worker'))
    shutil.copyfile(BUILDER/'evals/build-manifest.json',EVIDENCE/'builder-manifest.json')
    write_json(EVIDENCE/'binding.json',dict(builder_manifest_sha256=actual_sha,runner_sha256=sha((BUILDER/'scripts/run_evaluation.py').read_bytes()),grader_sha256=sha((BUILDER/'scripts/graders.py').read_bytes()),checker_sha256=sha(CHECKER.read_bytes())))
    recheck_inputs()
    shutil.copytree(CANDIDATE,EVIDENCE/'generated-baseline')
    shutil.copytree(CANDIDATE,SNAP/'baseline')
    shutil.copytree(CANDIDATE,SNAP/'destination')
    cases=[dict(case_id='spec-package-links',grader_id='package_links',params=dict(path='destination'),expected='PASS'),dict(case_id='spec-build-traceability',grader_id='build_traceability',params=dict(evidence='evidence',destination='destination'),expected='PASS')]
    (EVIDENCE/'evaluation-cases.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in cases),encoding='utf-8')
    provenance('candidate','INCOMPLETE',actual_sha)
    candidate_records=evaluate('candidate')
    for path in (ROOT,DEST,DEST.parent):
        check_boundary(path)
    assert not DEST.exists(),'Destination became occupied; no delivery'
    log(dict(cwd=str(ROOT),action='Immediately rechecked destination absent before delivery',destination=str(DEST),exists=False,interpretation='New-package delivery authorized with no collision'))
    DEST.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(CANDIDATE,DEST)
    assert outputs(DEST)==outputs(CANDIDATE),'Delivery readback differs'
    for row in outputs(DEST):
        path=DEST/row['path']
        text=path.read_text(encoding='utf-8')
        log(dict(cwd=str(ROOT),action='Read delivered file',path=str(path),sha256=row['sha256'],stdout=text,stderr='',interpretation='Actual delivered bytes decoded and read back; compare authored contract during editorial review'))
    structural=command([sys.executable,'-B','-X','utf8',CHECKER,DEST],'Installed structural checker against delivered development package')
    assert structural.returncode==0
    checks=EVIDENCE/'exercises-delivered'
    checks.mkdir()
    before=sha((INPUTS/'sample.csv').read_bytes())
    output=checks/'sample-result.json'
    sample=command([sys.executable,'-B','-X','utf8',DEST/'scripts/sum_amounts.py','--input',INPUTS/'sample.csv','--output',output],'Invoke delivered helper using actual resolved resource path')
    assert sample.returncode==0 and json.loads(output.read_bytes())==dict(count=4,total='2.65')
    assert before==sha((INPUTS/'sample.csv').read_bytes())
    # Existing candidate observations are valid for identical delivered bytes.
    previous=json.loads((EVIDENCE/'observations-candidate.json').read_bytes())
    assert previous['outputs']==outputs(DEST)
    write_json(EVIDENCE/'observations-delivered.json',dict(schema_version='1',run_id=RUN,target_name=NAME,outputs=outputs(DEST),structural=dict(exit_code=structural.returncode,stdout=structural.stdout,stderr=structural.stderr),delivered_invocation=dict(exit_code=sample.returncode,stdout=sample.stdout,stderr=sample.stderr,input_path=str(INPUTS/'sample.csv'),output_path=str(output),input_sha256_before=before,input_sha256_after=sha((INPUTS/'sample.csv').read_bytes())),behavioral_cases=previous['behavioral_cases'],schema_observation=previous['schema_observation'],editorial_observations=['All four required resources present and routed through SKILL.md.','Frontmatter has name and description only; automatic invocation preserved.','Python helper uses decimal arithmetic and standard library; no network or installation.','Read-only reviewer has no write assignment and sequential execution permitted.','No desktop, browser, hooks, registry, service, native agent profile, or framework dispatcher dependency introduced.'],limits=['Schema shape and regex directly exercised; independent full JSON Schema engine not used.','Native Codex implicit activation was not tested.']))
    # Replace only our own bounded destination snapshot with delivered readback.
    for row in outputs(DEST):
        shutil.copyfile(DEST/row['path'],SNAP/'destination'/row['path'])
    recheck_inputs()
    provenance('delivered','COMPLETE',actual_sha)
    records=evaluate('delivered')
    assert actual_sha==sha((BUILDER/'evals/build-manifest.json').read_bytes())
    assert outputs(DEST)==outputs(SNAP/'destination')==outputs(EVIDENCE/'generated-baseline')
    recheck_inputs()
    destination_manifest=manifest(DEST)
    write_json(EVIDENCE/'destination-manifest.json',destination_manifest)
    pointer=dict(schema_version='1',run_id=RUN,baseline=outputs(EVIDENCE/'generated-baseline'),provenance=dict(path=str(EVIDENCE/'build-provenance.json'),sha256=sha((EVIDENCE/'build-provenance.json').read_bytes())))
    write_json(EVIDENCE.parent/'active-baseline.json',pointer)
    log(dict(cwd=str(ROOT),action='Published development baseline pointer after required evaluations and delivered/input readback',path=str(EVIDENCE.parent/'active-baseline.json'),interpretation='Complete bounded specification build; no operational installation or framework acceptance'))
    bindings=json.loads((EVIDENCE/'binding.json').read_bytes())
    digest_rows='\n'.join('| '+row['path']+' | '+row['sha256']+' |' for row in destination_manifest['files'])
    report=f'''# Skill Specification Build Report

## Result

| Dimension | State | Evidence or reason |
| --- | --- | --- |
| Authoring | COMPLETE | Four required resources delivered and read back. |
| Structural checks | PASSED | Installed Skill Creator checker exited 0 on candidate and delivered package. |
| Deterministic evaluation | PASSED | spec-v1 version 1; both required graders PASS on candidate and delivered snapshots. |
| Behavioral evaluation | PASSED | 18 bounded candidate cases, plus delivered-path success invocation. |
| Supporting-script execution | PASSED | Supplied sample totals 2.65; NaN exits 2; conflict bytes preserved. |
| Independent forward trials | PASSED | This independent specification-build trial only; other enhancement trials are outside this worker's scope. |
| Routing evaluation | NOT_PERFORMED | Seven independent route classifications recorded; expected-result grading belongs to the parent and native implicit activation was not run. |
| Framework enforcement | NOT_IMPLEMENTED | No compiled-Rust authority implemented by this trial. |
| Rust qualification | NOT_PERFORMED | Python observations do not qualify Rust. |
| Operational installation | NOT_PERFORMED | Development source only. |

Validation status: Required structural and explicit spec-v1 deterministic checks passed; all 18 changed-script cases and the delivered invocation passed. Sequential result review checked actual output fields and unchanged input bytes. These are development observations, not acceptance.

## Request, selection, and boundary

Explicit parent task authorized one synthetic specification build and bounded local exercises inside `{ROOT}`. The selected approved Markdown path was `{SPEC}`. Its raw-byte SHA-256 is `9f096f495eaa7c3523538f6be7a2546acb129c2967451baa1b261a6ce5947e14`, 2625 bytes. The resolver found declared name `{NAME}` via the explicitly selected path; no name search or competing input was used.

Destination: `{DEST}`. Evidence run: `{EVIDENCE}`; run ID `{RUN}`. New package, so revision authorization and B/C/N handling are NOT_APPLICABLE. Paths were checked for reparse boundaries, and destination absence was rechecked immediately before copying. Only the selected spec, supplied fixtures, actual builder instructions/resources and installed checker were inspected. Source Claude package, other trials, test contents, deterministic-candidate, backup and legacy implementations were not inspected. The mandatory evaluator internally hashes all of its bound builder files, including tests, to verify integrity.

Host identification: Windows 10.0.26200, PowerShell 7.6.6, Python 3.10.11, PyYAML 6.0.2, codex-cli 0.154.0. CLI identification returned temp-cleanup and PATH-alias access-denied warnings; it still exited 0. Native CLI activation/qualification was not performed. No dependency installation occurred.

## Contract and resource traceability

[Build contract](build-contract.json) was written before candidate generation and binds the selected original bytes plus real requirement byte slices for REQ-01 through REQ-06. Its two-way mappings cover the four specified artifacts, input/output contract, domain rules, effects, recovery, dependency availability and worker behavior. [Provenance](build-provenance.json) binds requirements to preceding [delivered observations](observations-delivered.json), current output digests and distinct generated baseline bytes. Source specification is a bounded copy in `snapshot/inputs`.

The runtime requires Python 3.10+ standard library and the PowerShell terminal. Availability was observed; runtime binary qualification is not claimed. The required result-review worker has no write assignment and ran sequentially; see [actual worker review](worker-review-candidate.json). All original spec/sample/invalid file paths, byte lengths and hashes match [before](original-inputs-before.json) and [after](original-inputs-after.json).

Builder manifest SHA-256: `{actual_sha}`. Runner SHA-256: `{bindings['runner_sha256']}`. Grader SHA-256: `{bindings['grader_sha256']}`. Installed checker SHA-256: `{bindings['checker_sha256']}`. Parent paused final binding while it repaired evaluator validation; no earlier final evaluator run was made or discarded in this trial. The provided final manifest digest was checked before binding and after evaluation.

Generated baseline: `generated-baseline/`; delivered files are separate under the development destination. [Destination manifest](destination-manifest.json) records sizes and raw-byte hashes:

| File | SHA-256 |
| --- | --- |
{digest_rows}

## SPEC GAPS

None observed within the selected contract. [Gap artifact](spec-gaps.json) contains an empty array. No source changes or target collisions occurred.

## Revision result

NOT_APPLICABLE: new package. The development baseline pointer was published only after required evaluation and final readback.

## Executed checks and editorial findings

[Case definitions](evaluation-cases.jsonl), [candidate results](evaluation-results-candidate.jsonl), and [delivered results](evaluation-results-delivered.jsonl) retain actual required Python observations. Every actual build case expected PASS; both package_links and build_traceability observed PASS. Runner profile is spec-v1, version 1. Results retain case, runner/grader manifest and candidate input digests. Final JSONL is outside `snapshot/`.

The 18 script cases cover sample total, NaN, existing output conflict with valid and invalid CSV, BOM and quoted multiline fields, header-only input, large exact Decimal sums, negative zero, absent header/amount, short rows, infinity, excess and trailing precision, malformed quotes, invalid UTF-8, nonexistent input, and missing required arguments. All expected exits, stdout/stderr, original-input bytes, and conflict-output bytes matched assertions. The delivered helper was invoked from its real final resource path and produced `{{"count": 4, "total": "2.65"}}`.

Editorial readback confirmed useful routing and actual command interface, exactly the requested frontmatter, runtime standard-library-only implementation, linked schema and worker contract, no invented UI metadata/profiles/adapters, and advisory worker semantics. Schema exact field/type constraints were inspected and the string pattern exercised against valid and invalid examples including trailing newlines; no external full JSON Schema implementation was installed or run. Python deterministic success is byte accounting and does not alone prove semantic correctness; the executed task cases and readback provide the bounded semantic observations.

Separately, [routing classifications](routing-observed.jsonl) record seven raw requests classified using the actual builder entrypoint; [routing receipt](routing-classification-receipt.json) retains the exact task prompt, request bytes/digest, entrypoint digest, then-current manifest digest, and per-request rationale. None of those requests was executed. Root expected classifications and tests were not read. One nested path-quoting read failed with exit 1, then the corrected argument-vector read succeeded; both are in the command log. A receipt transcription correction preserved its original bytes separately. These observations are classification, not native activation.

## Handoff

Delivered package: `{DEST}`. [Command log](command-log.md) and [machine command log](command-log.jsonl) retain exact subprocess argument arrays, PowerShell equivalents, output streams, exits and interpretations from contract preparation onward. Preliminary read-only discovery occurred before log creation and is honestly summarized there; its exact full tool transcript remains in the agent conversation. Some displayed long outputs were truncated by the tool, while their complete subprocess stdout/stderr remain in the durable log. This preliminary discovery transcript gap is a logging limitation, not a hidden retry or check result.

No unresolved functional issue was observed in the bounded cases. Unperformed observations: independent JSON Schema engine, native implicit activation, other enhancement trials, expected-route grading, Rust enforcement/qualification, and installation. No claim is made about those scopes.
'''
    (EVIDENCE/'build-report.md').write_text(report,encoding='utf-8')
    write_json(EVIDENCE/'final-receipt.json',dict(schema_version='1',run_id=RUN,authoring='COMPLETE',package=str(DEST),evidence=str(EVIDENCE),builder_manifest_sha256=actual_sha,contract_sha256=sha((EVIDENCE/'build-contract.json').read_bytes()),provenance_sha256=sha((EVIDENCE/'build-provenance.json').read_bytes()),destination_manifest_sha256=sha((EVIDENCE/'destination-manifest.json').read_bytes()),report_sha256=sha((EVIDENCE/'build-report.md').read_bytes()),evaluation_results_sha256=sha((EVIDENCE/'evaluation-results-delivered.jsonl').read_bytes()),script_cases=18,structural='PASSED',deterministic='PASSED',source_preservation='PASSED',installation='NOT_PERFORMED'))
    print(json.dumps(json.loads((EVIDENCE/'final-receipt.json').read_bytes()),indent=2))

if __name__=='__main__':
    main()
