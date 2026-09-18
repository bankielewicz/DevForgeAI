"""Publish new validation deliverables and verify retained evidence; no skill writes."""
import continue_evaluation as c
import json
import sys
from pathlib import Path
r=c.RUN

def ref(rel):
    p=r/rel
    return {'path':rel,'sha256':c.h.sha(p.read_bytes())}

def docs():
    assessment=c.load(r/'assessment.json')
    assert assessment['overall_assessment']=='PASS'
    old=c.load(r/'inputs/prior-records/findings.json')['findings']
    c.save(r/'inputs/finding-dispositions.json',{'prior_findings':[{
        'finding_id':f['finding_id'],'classification':'resolved_for_current_assessment',
        'reason':'Fresh supported evidence layout passed unchanged whole-run and external-family verifiers.' if f['rule_id']=='AV-E01' else 'All seven interrupted cases completed under disclosed fresh execution and authorized JavaScript host/warm continuation; historical failures remain unchanged.',
        'evidence':[ref('commands/records-complete-initial/stdout.txt'),ref('inputs/evaluation-summary.json'),ref('inputs/native-decisions.json')]
    } for f in old],'historical_result':'Unchanged; previous INCOMPLETE and 184 record errors are preserved.'})
    c.save(r/'findings.json',{'schema_version':'1','run_id':r.name,'target_name':'dev','findings':[],
        'prior_dispositions':ref('inputs/finding-dispositions.json')})
    c.save(r/'inputs/authoring-family-current.json',{'schema_version':'authoring-family-assessment-v1',
        'basis':'Exact current request and original target BOUND by unchanged intake; authoring lineage is custody evidence, not quality or framework acceptance.',
        'request':ref('inputs/validation-request.json'),'intake':ref('commands/intake/stdout.txt'),
        'authoring_record':ref('inputs/prior-inputs/01-authoring-record.json'),
        'package_digest':c.load(r/'source-manifest.json')['package_digest'],'adoption_required':False})
    c.save(r/'enforcement-recommendations.md','''# Enforcement recommendation dimension

Descriptive only. No new enforcement implementation or skill change is proposed in this evaluation. Retain the existing destination-custody recommendation as guidance pending separately authorized compiled-Rust work.

| Field | Retained recommendation |
| --- | --- |
| ID / passage | ENF-DEST-01; source/references/evidence-resume.md, literal original destination and delivered-file readback |
| Destination / trigger | Future devforgeai_cli protected acceptance service; delivery submission |
| Invariant / inputs | Original selected destination, allowed roots, candidate and delivered-file digests, requirements and execution provenance must match |
| Intended observation | Validate current bytes and completeness before any authoritative acceptance decision |
| Current evidence | DV-17 carried with current prerequisite readback; RV-04 fresh stale-draft rejection and exact custom receipts/ delivery; Python and model records remain evidence only |
| Failure behavior | Reject missing, stale or wrong-location outputs and retain the failed attempt |
| Bypass / limits | Editable records and static checks cannot enforce custody against hostile concurrent changes; no implemented hook, CLI gate or service established here |
| Dependencies | Separately selected, implemented and qualified compiled Rust authority; protected provenance and mutation boundary |
| Future verification | Denied mismatched roots, stale/missing outputs, altered provenance, concurrent replacement, plus valid delivery on each required native platform |

This register authorizes no implementation, installation, hook/CI configuration or phase transition. Existing skill guidance remains intact.
''')
    digest=c.load(r/'source-manifest.json')['package_digest']
    rule_digest=c.h.sha((r/'rule-set.json').read_bytes())
    cases=c.load(r/'inputs/case-observations.json')['cases']
    table='\n'.join('| '+x['case_id']+' | '+x['result']+' | '+('Carried, current bindings verified' if x['evidence_origin'].startswith('historical') else 'Cold + host QA + approved warm delivery' if x['case_id']=='DV-03' else 'Fresh cold trial')+' |' for x in cases)
    c.save(r/'validation-report.md',f'''# Independent dev skill validation

**PASS for the selected assessment.** All 71 applicable required checks passed; 23/23 unique required scenarios passed (100%). This comprises 16 carried historical cases with current byte/prerequisite verification and seven cases completed in this run. Assessment completed: true. Builder readiness: NO_CHANGE; proposal review: not_needed.

Validation: PERFORMED — PASS. Testing: PERFORMED — selected 23-case suite PASS, with the execution limits below. Installation: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED.

## Identity, source and independence

Run: `{r.name}`. Target: `C:\\Projects\\DevForgeAI\\src\\agents\\skills\\dev`. Exact request: `docs/plan/skill-authorings/dev/20260914T0117324130584Z/validation-request.json`, SHA-256 `034887a39a8b5f12e0ca3bb27e2f87cba48b4f0f74335071ef2baf6b77d525af`. Unchanged production intake returned BOUND.

Package digest: `{digest}`. Frozen rule-set digest: `{rule_digest}`. **All applicable mandatory checks in that rule-set digest passed for that package digest.** This is an evidence-backed skill assessment, not protected framework acceptance or a guarantee of future execution.

The primary validator evaluated independently of authoring; no separate reviewer or model-independence claim. The existing original specification and revision contract remain selected, with authored custody recorded separately from schema-1 observed history. See [origin](origin-record.json), [source manifest](source-manifest.json), [final source manifest](source-after-manifest.json), [rules](rule-set.json), [workflow map](workflow-map.json), and [input/checker readback](inputs/final-input-readback.json). All 11 package files and original source/specification/rule/checker bindings match. No target or operational skill changes were made.

The original local input snapshots retain their actual prior retrieval times and were freshly hash-verified. Official OpenAI skill guidance was refreshed at 2026-09-14T07:09:59Z through OpenAI Docs and retained in [the captured page](inputs/official-build-skills.md); it corroborates the frozen rules, without silently expanding this assessment into every current standard. Token counts are NOT_RUN because the tokenizer cache was unavailable; file/byte/character/line observations and complete manual text review are retained. Optional package naming/TODO scanner candidates were manually resolved using original identity and actual passages; raw helper INCOMPLETE output is preserved, not relabeled.

## Assessment dimensions

| Dimension | Result | Evaluated / applicable required |
| --- | --- | --- |
| Standards | PASS | 11/11 |
| Workflow | PASS | 32/32 |
| Instructions | PASS | 5/5 |
| Behavior | PASS | 23/23 |
| Enforcement recommendations | Descriptive; no implemented authority claim | [Register](enforcement-recommendations.md) |

The complete 82-rule set contains 71 applicable checks and 11 explicitly inapplicable adaptive/optional checks; zero unknown applicability, failed, errored or unexecuted required checks. [Checks](checks.jsonl) and [assessment](assessment.json) retain exact reductions. All linked text resources were read, local links resolved, and workflow instructions assessed for actual inputs, action, output, recovery and observable completion; emphatic wording alone was not treated as a defect.

## Required cases and evidence provenance

| Case | Result | Execution basis |
| --- | --- | --- |
{table}

RV-01 aliases DV-17 and is counted once. Python/JavaScript variants, retries, host QA and warm continuation do not inflate the 23-case denominator. [Carry-forward audit](inputs/carry-forward.json) verifies each retained case's unchanged source, fixture, prior produced bytes, protected inputs, receipts and relevant runtime prerequisites. Historical executions are not represented as fresh executions. [Native decisions](inputs/native-decisions.json), [case observations](inputs/case-observations.json), and [command log](command-log.md) bind the new evidence.

New cold trials used native Windows, Codex CLI 0.154.0, inherited gpt-6-astra/high configuration without model override, and predeclared 900-second limits with at most two concurrent sessions. Initial app-server access denials are retained as attempt 001; approved host starts are attempt 002. All eight cold sessions for seven cases completed within their bounds. No WSL or additional platform qualification occurred.

DV-01 completed genuine missing-behavior red and six-method green/QA. DV-02 completed producer/consumer integration with eleven tests. DV-05 correctly blocked the underspecified slice while completing independent inventory work. DV-08 used the permitted terminal fallback and correctly left authority-dependent publication incomplete. DV-14 completed plan-only without product implementation. RV-04 rejected the stale draft's receipts/ mapping, preserved the supplied draft, executed eight-method red/green/QA, and verified delivery at the literal `custom receipts/` selection. These expected boundary outcomes are passing skill scenarios, not claims that blocked product work completed.

### JavaScript composite case

DV-03 Python completed ten unittest methods plus five integration checks. The JavaScript cold session performed genuine direct-node red/green but correctly reported the required `node --test` worker EPERM as incomplete. The exact required command was then executed on the unchanged candidate by the authorized Windows host: **6/6 PASS**, exit 0, no candidate changes. The original sandbox denial remains evidence.

The user explicitly authorized one 600-second warm continuation under the [bound proposal](inputs/javascript-continuation-proposal.md). It resumed the same session/model, inspected actual host command/streams and prerequisite hashes, completed in **193.641 seconds**, and added five evidence records plus the CLI final-message file. All 41 prior project files and four host receipts remained byte-identical; source/tests were unchanged and no passing test was rerun. [Authorization](inputs/javascript-continuation-authorization.json), [effects](trials/DV-03-javascript/attempt-003/effects.json), [independent audit](inputs/native-audits/DV-03-javascript-warm/audit.json), and [delivery](trials/DV-03-javascript/project/evidence/continuation-003-delivery.md) retain this distinction.

This supports the selected portability/development scenario through cold execution plus separately authorized host QA and warm delivery. It does not establish an entirely cold successful JavaScript delivery or Node worker execution inside the sandbox. The cold PowerShell receipt helper stated a 30-second child budget without implementing its own timeout; actual commands were short and the parent 900-second limit applied. That historical helper limitation is disclosed; no timeout-enforcement qualification is claimed.

## Evidence integrity and previous findings

The unchanged external Python JSONL runner and deterministic graders executed against independently adjudicated observations, exact fixture/expected-result/schema/runtime artifacts and a new bound manifest: **23 PASS, 0 FAIL/ERROR/NOT_RUN**, package and bundle MATCH, exit 0. See [summary](inputs/evaluation-summary.json), [results](inputs/evaluation-results.jsonl), [manifest](inputs/external-bundle-manifest.json) and [external location](inputs/external-bundle-location.json). The verifier checks evidence bindings; it does not independently infer all behavioral semantics.

The whole new schema-1 run passed the unchanged records checker with zero errors, and supplemental adaptive records passed their own checker. Foreign record families remain raw data under inputs/trials or in separate sibling roots with their own verifier. No evaluator maintenance or weakened checks were required. AV-E01 is resolved for this fresh layout. The previous 184-error whole-run result remains unchanged. An initial new bundle assembly hit a raw-manifest collision; that failed assembly and its explanation remain preserved, and a disjoint v2 capsule was used.

Both previous evidence-limitation findings are [resolved for this assessment](inputs/finding-dispositions.json); [current findings](findings.json) contains no new actionable source defect. Their historical identities and results remain intact. No skill-source repair, revision specification, builder invocation or installation is proposed. [Handoff](handoff.json) records NO_CHANGE and no approval decision needed.

## Coverage limits and next action

Required-case pass rate: 23/23 = 100%, meeting the selected 95% case floor without rounding. Executed-line and branch coverage of the instruction/template-only dev package: NOT_APPLICABLE, zero executable source files. Supporting evaluator/helper runtime coverage: NOT_RUN in this continuation. The earlier focused builder-helper coverage is separate and is not inherited as dev/framework coverage. No compiled-Rust framework denominator, acceptance service or framework qualification was evaluated.

Explicit-path cold task behavior and routing classification were exercised; native implicit activation, namespaced `$DevForgeAI:dev` invocation, installation, GUI/service behavior and non-Windows platform qualification remain outside the established claim. Model-written files and Python outputs supply evidence only. The selected independent evaluation is complete; no further action is required within this authorization.
''')
    c.save(r/'handoff.json',{'schema_version':'1','run_id':r.name,'target_name':'dev',
        'original_target_root':str(c.TARGET),'target_package_digest':digest,'original_manifest':ref('source-manifest.json'),
        'origin':ref('origin-record.json'),'proposed_spec':None,'findings':ref('findings.json'),'report':ref('validation-report.md'),
        'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'not_needed','review_instruction':None,
        'builder_readiness':'NO_CHANGE','readiness_reasons':['Selected assessment complete; no source correction proposed.'],
        'baseline_kind':None,'baseline_reference':None,'authoring_family_basis':ref('inputs/authoring-family-current.json'),
        'adoption_required':False,'adoption_capability':'Not required or exercised in this validation-only run.',
        'permitted_target_root':str(c.TARGET),'preservation_requirements':['No repairs or installation; preserve all source, operational copies and prior evidence.'],
        'unresolved_decisions':[],'installation':'NOT_PERFORMED','framework_acceptance':'NOT_EVALUATED'})
    receipt=c.h.execute('records-delivery',[sys.executable,'-B','-X','utf8',str(c.LOADED/'scripts/observe.py'),'records','--run-root',str(r)])
    assert receipt['exit_status']==0,c.load(r/'commands/records-delivery/stdout.txt')
    print('DELIVERY_RECORDS_PASS')

def seal():
    assert c.load(r/'commands/records-delivery/stdout.txt')['status']=='OBSERVED'
    old=c.load(c.PRIOR/'final-artifact-manifest.json')['files']
    for row in old:
        p=c.PRIOR/row['path'];assert p.stat().st_size==row['bytes'] and c.h.sha(p.read_bytes())==row['sha256']
    assert c.h.inventory(c.TARGET)['files']==c.load(r/'source-manifest.json')['files']
    for row in c.load(r/'inputs/final-input-readback.json')['inputs']:
        assert c.h.sha(Path(row['original_path']).read_bytes())==row['expected']
    c.save(r/'inputs/preservation-final.json',{'verified_at_utc':c.h.now(),'prior_manifest_rows_unchanged':len(old),
        'source_files_unchanged':11,'original_inputs_unchanged':True,'framework_acceptance':'NOT_EVALUATED'})
    logs=[]
    for p in sorted((r/'commands').glob('*/command.json')):
        x=c.load(p)
        logs.append('## '+p.parent.name+'\n\nCommand: `'+json.dumps(x['argv'],ensure_ascii=False)+'`\n\nWorking directory: `'+x['cwd']+'`. UTC: '+x['started_at_utc']+' to '+x.get('ended_at_utc','unknown')+'. Bound: '+str(x['timeout_seconds'])+' seconds; exit '+str(x.get('exit_status'))+'; termination '+x['termination']+'.\n\n[Receipt]('+p.relative_to(r).as_posix()+'), [stdout]('+p.with_name('stdout.txt').relative_to(r).as_posix()+'), [stderr]('+p.with_name('stderr.txt').relative_to(r).as_posix()+').\n')
    c.save(r/'command-log.md','# Retained executed commands\n\nExact argv, cwd, timing, bounds and exit outcomes follow. Tool-launch denials and failed helper attempts remain listed. Read-only semantic/file inspections are captured in inputs/semantic-review.json and native-audits; disposable fixture effects are in trials/. Evidence-only assembly scripts are retained under inputs/. The final seal check follows this immutable command-log snapshot; its receipt and streams are retained under commands/records-sealed/.\n\n'+'\n'.join(logs))
    names=['validation-report.md','assessment.json','findings.json','handoff.json','checks.jsonl','command-log.md',
        'enforcement-recommendations.md','origin-record.json','source-manifest.json','source-after-manifest.json','sources.json','rule-set.json','workflow-map.json',
        'inputs/native-decisions.json','inputs/case-observations.json','inputs/carry-forward.json','inputs/evaluation-summary.json','inputs/evaluation-results.jsonl',
        'inputs/external-bundle-manifest.json','inputs/finding-dispositions.json','inputs/preservation-final.json','inputs/final-input-readback.json',
        'commands/records-delivery/stdout.txt','commands/records-delivery/command.json']
    rows=[dict(ref(rel),bytes=(r/rel).stat().st_size) for rel in names]
    c.save(r/'final-artifact-manifest.json',{'schema_version':'1','run_id':r.name,'target_name':'dev','readback_at_utc':c.h.now(),
        'scope':'Explicit final deliverables; raw evidence and sibling capsule remain bound through referenced case/manifests and verifier output. Excludes this manifest and final receipt to avoid cycles.','files':rows})
    c.save(r/'FINAL-RECEIPT.json',{'schema_version':'1','run_id':r.name,'target_name':'dev','assessment_completed':True,
        'validation':'PERFORMED','overall_assessment':'PASS','testing':'PERFORMED','selected_required_case_result':'PASS',
        'required_cases':23,'passing_cases':23,'pass_rate':100.0,'carried_cases':16,'continued_cases':7,
        'javascript_execution':'Cold + authorized host QA + one approved warm continuation, unchanged candidate.',
        'required_rules_passed':71,'applicable_required_rules':71,'artifact_manifest':ref('final-artifact-manifest.json'),
        'assessment':ref('assessment.json'),'report':ref('validation-report.md'),'handoff':ref('handoff.json'),
        'source_package_digest':c.load(r/'source-manifest.json')['package_digest'],
        'installation':'NOT_PERFORMED','framework_acceptance':'NOT_EVALUATED'})
    result=c.h.execute('records-sealed',[sys.executable,'-B','-X','utf8',str(c.LOADED/'scripts/observe.py'),'records','--run-root',str(r)])
    assert result['exit_status']==0,c.load(r/'commands/records-sealed/stdout.txt')
    for row in rows: assert c.h.sha((r/row['path']).read_bytes())==row['sha256']
    print('SEALED',len(rows),'DELIVERABLES; FINAL RECORDS PASS; PRIOR',len(old),'ROWS UNCHANGED')

if __name__=='__main__': {'docs':docs,'seal':seal}[sys.argv[1]]()
