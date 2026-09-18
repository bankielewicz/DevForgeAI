import json, pathlib, shutil, subprocess
import trial

root=trial.ROOT
s=trial.state()
project=pathlib.Path(s['project']);target=pathlib.Path(s['target'])
expected='60522daaff9000367beacb7b5a6fb03cd90caeb93ac829bc13bba98c2d3b31a9'
assert trial.digest(trial.BUILDER/'evals/build-manifest.json')==expected
initial=json.loads((root/'initial-target-manifest.json').read_text())
assert trial.digest(target/'notes.txt')==next(x['sha256'] for x in initial['files'] if x['path']=='notes.txt')
assert trial.digest(pathlib.Path(s['spec']))==trial.digest(root/'origin-spec.md')
shutil.copytree(target,root/'final-delivered-package')
trial.write(root/'final-target-manifest.json',trial.manifest(target))
shutil.copyfile(root/'trial.py',root/'driver-executed.py')
shutil.copyfile(root/'behavior_check.py',root/'behavior-check-executed.py')
trial.write(root/'execution-tools-manifest.json',{'schema_version':'1','files':[{'path':str(p),'sha256':trial.digest(p),'bytes':p.stat().st_size} for p in [root/'driver-executed.py',root/'behavior-check-executed.py',trial.BUILDER/'scripts/build_evidence.py',trial.BUILDER/'scripts/run_evaluation.py',trial.BUILDER/'evals/build-manifest.json',pathlib.Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')]]})
instructions=root/'instructions-used'
for rel in ['SKILL.md','references/adoption.md','references/regeneration.md','references/evaluation.md','references/evaluator-contracts.md','references/evidence-format.md','references/spec-build.md','evals/adoption-evidence.schema.json','evals/build-manifest.json']:
    dest=instructions/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(trial.BUILDER/rel,dest)

audit=[]
for dirname in ['revision-01-conflict','revision-02-resolved','later-revision-03']:
    run=project/'docs/plan/skill-builds/receipt-totals'/dirname
    bounded=run/'snapshot';contract=bounded/dirname/'evidence/build-contract.json'
    data=json.loads(contract.read_text())
    for inp in data['inputs']:
        original=pathlib.Path(inp['resolved_path']);captured=bounded/inp['path']
        row={'run_id':dirname,'input_id':inp['id'],'resolved_path':str(original),'captured_path':str(captured),'declared_sha256':inp['sha256'],'original_sha256':trial.digest(original),'captured_sha256':trial.digest(captured)}
        row['passed']=row['declared_sha256']==row['original_sha256']==row['captured_sha256'] and original.stat().st_size==captured.stat().st_size==inp['bytes']
        assert row['passed'];audit.append(row)
trial.write(root/'original-input-locator-audit.json',{'checks':audit,'passed':True})

results=[]
for p in sorted(project.glob('docs/plan/skill-*/receipt-totals/*/*results.jsonl')):
    rows=[json.loads(x) for x in p.read_text().splitlines()]
    for row in rows:
        assert row['build_manifest_sha256']==expected
        assert row['status']=='PASS' and row['expectation_met']
    results.append({'path':str(p),'sha256':trial.digest(p),'profile':rows[0]['profile'],'count':len(rows),'all_passed':True})
assert len(results)==8,len(results)
trial.write(root/'evaluation-index.json',{'builder_manifest_sha256':expected,'files':results,'record_count':sum(x['count'] for x in results)})

commands=[(p,json.loads(p.read_text())) for p in sorted((root/'commands').glob('*.json'))]
log=['# Actual subprocess command receipts','', 'Each linked JSON preserves timestamp, cwd, exact argument vector, final exit code, stdout and stderr. File edits and external publication/readback are recorded in the retained application/publication receipts and the executed driver.','']
for p,c in commands:
    log += ['## '+p.stem,'',c['timestamp'],'','```text',subprocess.list2cmdline(c['argv']),'```','',f"Cwd: `{c['cwd']}`; exit: `{c['exit_code']}`. [Complete raw receipt](commands/{p.name}).",'']
trial.write(root/'command-log.md','\n'.join(log))

adoption=pathlib.Path(s['adoption_run'])
first=project/'docs/plan/skill-builds/receipt-totals/revision-02-resolved'
later=pathlib.Path(s['successful_run'])
pointers={name:json.loads((run/'published-origin.json').read_text()) for name,run in [('adoption',adoption),('first_generated',first),('later_generated',later)]}
trial.write(root/'origin-chain.json',pointers)
report=f'''# Independent adoption task trial — final

Status: PASSED for the bounded development trial. All final-chain deterministic
observations bind builder manifest `{expected}`. This is actual execution against
a new disposable TEMP development project, not fabricated successful evidence.

Project: `{project}`

Development target: `{target}`

## Results and receipts

| Stage | Actual result | Retained evidence |
| --- | --- | --- |
| Original script | Executed; numeric 0.30000000000000004 demonstrated the known defect | commands/origin-known-defect.json |
| Adoption | Helper exit 0; adoption-v1 one PASS; unchanged target/spec | retained/adopt-01-published/ |
| Adoption publication | External pointer written then read back; no prior pointer | retained/adopt-01-published/publication-readback.json |
| First candidate | Structural PASS; 15 behavior cases PASS; spec-v1 two PASS | retained/revision-01-conflict/ |
| Injected user edit | Script comment appended after adoption publication | user-edit-observation.json |
| Conflict | Helper exit 1, CONFLICT; applied_paths empty; live destination equals C | retained/revision-01-conflict/post-plan-live-manifest.json |
| Distinct resolution | Edited script retained; only script restored to exact adopted bytes; origin unchanged | resolution-edit-readback.json and prompts/04-conflict-resolution.txt |
| Resolved first revision | Fresh candidate/delivered checks; 15 delivered cases PASS; delivered and published revision-spec-v2 each three PASS | retained/revision-02-resolved-successful/ |
| Later revision | Selected last successful generated N; adds exact total_quantity; 16 fresh candidate and delivered cases PASS; delivered and published revision-spec-v2 each three PASS | retained/later-revision-03-successful/ |
| Original input locators | All six selected original-input and captured-input digest/size comparisons PASS | original-input-locator-audit.json |
| User notes and origin spec | Byte-identical after the complete chain | final-target-manifest.json |

Eight evaluator result files contain 19 PASS records; [evaluation-index.json](evaluation-index.json)
records exact paths, profiles, hashes and counts. The helper's expected conflict
exit 1 is retained independently from these successful evaluations. Candidate
spec-v1 checks are candidate observations; delivered/published revision-spec-v2
checks are separately executed on real after snapshots. Publication pointers are
outside the target; their original absolute paths and readback hashes are retained.

## Authorization and custody

The trial controller authorized a new disposable chain with the same raw receipt
task and separate adoption, first-revision, conflict-resolution and later-revision
instructions. Raw directions are in prompts/. Original managed scope is exactly
SKILL.md and scripts/receipt_totals.py. notes.txt is retained_user throughout.
Adoption historical_origin remains unknown. The first generated origin comes from
the adopted managed snapshot; the later revision selects the successful first N,
not current files or the conflict attempt. [origin-chain.json](origin-chain.json)
retains all three pointer objects, while raw published pointers and readback
receipts remain in each retained run directory.

The adoption origin digest is `{pointers['adoption']['origin']['sha256']}`.
The first generated origin digest is `{pointers['first_generated']['origin']['sha256']}`.
The later generated origin digest is `{pointers['later_generated']['origin']['sha256']}`.

## Verification scope and limitations

The worker read current SKILL.md, references, schemas and the documented legacy
package_links case interface. It did not read builder implementation, implementation
tests or other agents' conclusions. No builder source was edited. The independent
trial used one worker and real subprocesses; raw commands, streams, scripts,
inputs, snapshots, conflicts, resolution edits and pointer receipts are retained.
The controller's explicit fresh-chain instruction authorized reuse of the reviewed
behavior proposals in the new project; it did not erase the earlier attempt.

The checks cover exact decimal aggregation and wide values, single grand-total
rounding/half-up ties, fractional quantities, empty and quoted receipts, exact
successful JSON schema, invalid header/cell counts, blank items, invalid text,
negative/nonfinite inputs, and receipt preservation. The later checks also inspect
the exact total_quantity schema and values, including zero for an empty receipt.

No source defect was observed in these exercised builder interfaces. One cosmetic
helper reason says 'previous generated baseline' for an adopted row; the typed
ownership and origin fields correctly identify adoption. Python observations and
ordinary pointer files confer no protected authority. Rust implementation and
qualification: NOT_PERFORMED. Native implicit routing: NOT_PERFORMED. Operational
installation: NOT_PERFORMED. Publication-failure and partial-write recovery were
not injected in this final chain. No stronger reliability claim is made.

## Earlier retained chain

The adjacent directory without the -final suffix preserves the first chain. It
contains a rejected unsorted manifest attempt, a correctly recaptured adoption,
successful conflict/resolution/later execution, and a self-authored authorization
resolved_path metadata defect in the first revision. That defect was disclosed;
the raw bounded instruction bytes were correct but the informational original
locator pointed at the first instruction rather than the combined instruction.
Its old-manifest provenance also predictably failed an optional current-manifest
re-evaluation with 'builder manifest digest differs from running evaluator'. Those
results are preserved, not relabeled. The controller requested this fresh chain
to obtain current-manifest observations with exact original locators. This report
uses the new final chain as its completed trial evidence.
'''
trial.write(root/'report.md',report)
for run in [adoption,first,later]:
    trial.write(run/'trial-report-location.json',{'final_report':str(root/'report.md'),'sha256':trial.digest(root/'report.md'),'note':'Report location added outside immutable bounded inputs and previously evaluated records.'})
print(json.dumps({'report':str(root/'report.md'),'evaluator_records':sum(x['count'] for x in results),'input_locator_checks':len(audit),'notes_sha256':trial.digest(target/'notes.txt'),'pointers':pointers},indent=2))
