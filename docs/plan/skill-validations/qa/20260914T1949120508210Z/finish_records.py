"""Read back immutable inputs, bind conclusions, and prepare the final report."""
from bootstrap import ROOT, PROJECT, VALIDATOR, write, run, observe
from prepare_trials import ref, put
import datetime
import hashlib
import json
from pathlib import Path
import sys

meta=dict(schema_version='1',run_id=ROOT.name,target_name='qa')
manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
bindings=json.loads((ROOT/'input-bindings.json').read_bytes())
run('source-readback',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(PROJECT/'src/agents/skills/qa'),'--manifest',str(ROOT/'source-manifest.json')])
readback=json.loads((ROOT/'observations/source-readback.stdout').read_bytes())
write(ROOT/'source-after-manifest.json',readback['manifest'])
unchanged=readback['manifest']['files']==manifest['files']
originals=[]
for item in bindings:
    actual=hashlib.sha256(observe.read_stable(observe.safe_path(item['original_path']))).hexdigest()
    originals.append(dict(original_path=item['original_path'],expected_sha256=item['sha256'],actual_sha256=actual,unchanged=actual==item['sha256']))
before=json.loads((ROOT/'preservation-before-manifest.json').read_bytes())
preserved=[]
for key,path in [('operational_qa',PROJECT/'.agents/skills/qa'),('validator',VALIDATOR)]:
    after=observe.make_manifest(path)
    preserved.append(dict(subject=key,unchanged=after['files']==before[key]['files'],before_package_digest=before[key]['package_digest'],after_package_digest=after['package_digest']))
write(ROOT/'preservation-readback.json',dict(**meta,input_results=originals,package_results=preserved,history='Historical evidence was read only and never selected as a write destination. Whole historical evidence tree was not recursively hashed.',source_unchanged=unchanged))
origin=json.loads((ROOT/'origin-record.json').read_bytes())
origin['source_readback_state']='UNCHANGED' if unchanged else 'SOURCE_CHANGED'
write(ROOT/'origin-record.json',origin)

rules=json.loads((ROOT/'rule-set.json').read_bytes())['rules']
check_rows=[]
static_evidence=[ref(ROOT/'semantic-review.json'),ref(ROOT/'requirement-map.json'),ref(ROOT/'workflow-map.json')]
behavior_evidence=[ref(ROOT/'native-observations.json'),ref(ROOT/'evaluation/results-001.jsonl')]
reasons={
 'AV-F01':'Unique-key YAML, UTF-8 and required metadata passed both structural helpers; installed checker passed.',
 'AV-F02':'Bound original directory is qa and metadata name is qa. Source-named snapshot limitation resolved against original manifest.',
 'AV-F03':'Description exposes product QA and explicit exclusions; independent description classifier matched 10/10 prompts. Native implicit activation separate.',
 'AV-F04':'Optional host metadata parses with three documented interface string fields; no unsupported extension or explicit invocation-policy restriction.',
 'AV-F05':'All captured Markdown read; template slots have explicit consumers/filling rules. TODO is a forbidden-output example, not incomplete production instructions.',
 'AV-U01':'Complete text scan found zero specified Unicode candidates; this is not exhaustive confusable detection.',
 'AV-R01':'All twenty package resource edges resolve; no unsupported anchors remained after manual review.',
 'AV-R02':'All nine files have actual consumers through entrypoint/reference graph or host metadata.',
 'AV-R03':'Four references and three templates supply declared instruction/output contracts. No runtime scripts or unsupported executable interface introduced; actual delivery remains unproven under W01.',
 'AV-I01':'Mode, readiness, severity, metrics, delivery and resume branches traced against amended contract; no static contradiction identified.',
 'AV-I02':'Contextual ceremonial review preserved useful stop, evidence and placeholder safeguards; no hollow perfection gate or unsupported authority claim found.',
 'AV-I03':'Entry instructions load planning, integrity and assessment before dependent execution and reporting before publication; templates explicitly consumed.',
 'AV-I04':'Static authorization/continuation instructions match the extension. Complete behavior honoring user scope and delivery remains unproven after cold-trial timeouts.',
 'AV-C01':'All nine files counted in bytes, Unicode characters and physical lines. Tokenizer cache unavailable; token/load counts NOT_RUN and no token budget selected.',
 'AV-S01':'No malicious instruction executed by evaluator; hostile-data runtime behavior has not been exercised in a completed bounded trial.',
 'AV-S02':'Static effects/path/ownership rules reviewed; native security/effect variants and persistent-effect rejection have not completed.',
 'AV-W01':'Workflow map complete, but full run, plan-only and integrity-stop pilots timed out before artifact delivery; no complete workflow PASS.',
 'AV-W02':'Native resume, interruption recovery, drift and retest workflows remain unperformed.',
 'AV-E01':'Current input/source/specification readbacks and exact evaluation bundle bindings verified; no incomplete native scenario counted as passed.'}
for rule in rules:
    rid=rule['rule_id']
    if rid.startswith('AV-A'):
        dimension='workflow'
        outcome='NOT_APPLICABLE'
        reason='Ordinary single skill; selected specs require no adaptive descriptor, operational binding, core/variant lineage or selected-set handoff.'
        evidence=[ref(ROOT/'source-manifest.json'),ref(ROOT/'requirement-map.json')]
    elif rid.startswith(('QV-','QPV-')):
        dimension='behavior'
        outcome='NOT_RUN'
        reason='Required scenario and all its named variants lack completed native evidence. Three feasibility pilots retained; other native fixtures/cases remain outstanding. See exact catalog and traces.'
        evidence=behavior_evidence
    else:
        dimension='standards' if rid.startswith(('AV-F','AV-U','AV-R','AV-C','AV-E')) else 'behavior' if rid=='AV-W02' else 'workflow' if rid=='AV-W01' else 'instructions'
        outcome='NOT_RUN' if rid in ['AV-I04','AV-S01','AV-S02','AV-W01','AV-W02'] else 'PASS'
        reason=reasons[rid]
        evidence=static_evidence+[ref(ROOT/'observations/structure.stdout'),ref(ROOT/'observations/text-resources.stdout')]
        if rid in ['AV-F02','AV-E01']: evidence += [ref(ROOT/'source-after-manifest.json'),ref(ROOT/'preservation-readback.json')]
        if rid=='AV-F03': evidence += [ref(ROOT/'routing-observation.json')]
        if outcome=='NOT_RUN': evidence += behavior_evidence
    check_rows.append(dict(**meta,check_id=rid+'-current',rule_id=rid,subject_path='SKILL.md',method=rule['method'],required=True,applicability=rule['applicability'],result=outcome,reason=reason,evidence=evidence,dimension=dimension))
# schema-1 check rows have no target_name field.
for row in check_rows: row.pop('target_name')
(ROOT/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in check_rows),encoding='utf-8')
dimensions={d:observe.reduce_checks([r for r in check_rows if r['dimension']==d]) for d in observe.DIMENSIONS}
total=observe.reduce_checks(check_rows)
write(ROOT/'assessment.json',dict(**meta,assessment_completed=True,overall_assessment='INCOMPLETE',dimensions=dimensions,required_coverage=total,unknown_applicability=0,framework_acceptance='NOT_EVALUATED'))

anchor='QA-026 / QAP-014: This skill\'s evaluated-build completeness requires a separate skill-validator task binding exact skill and selected specification bytes to a Python JSONL runner, deterministic graders, independent fixtures, expected results, schema, runtime/dependency information and artifact manifests/digests.'
subject='references/reporting-handoff.md'
fid,identity=observe.finding_identity('AV-W01',subject,anchor,0)
finding=dict(finding_id=fid,identity=identity,rule_id='AV-W01',category='input_evidence_limitation',severity='blocker',subject_path=subject,locator={'section':'Separate package evaluation'},source_refs=[dict(**ref(ROOT/'source'/subject),source_id='qa-skill-postmvp-spec',locator={'section':'Separate package evaluation'})],observation_refs=behavior_evidence,description='Evaluated-build completeness is unproven. All three cold workflow pilots reached the 120-second limit; none delivered final required artifacts. Remaining scenario variants and full native grading are unperformed.',user_impact='The authored package cannot be described as independently behavior-validated or qualified for adoption by this assessment.',proposed_correction='Complete a separately selected native campaign with explicitly chosen feasible case budgets and remaining independent fixture variants; preserve every current failure/timeout and rebind unchanged inputs. No source repair is justified by these traces.',preserved_requirements=['Exact-byte provenance','No automatic retry or source repair','All 42 selected scenarios and variants','Python evidence only; separate Rust authority'],verification_cases=['QV-01 through QV-21','QPV-01 through QPV-21'],disposition='proposed')
write(ROOT/'findings.json',dict(**meta,findings=[finding]))

coverage=json.loads((ROOT/'observations/grader-coverage.json').read_bytes())['totals']
lines=coverage['num_statements']
covered=coverage['covered_lines']
branches=coverage.get('num_branches',0)
covered_branches=coverage.get('covered_branches',0)
put(ROOT/'validation-report.md',f'''# QA skill independent validation

## Identity and conclusion

**INCOMPLETE.** Assessment reporting is complete; behavioral evaluation and evaluated-build completeness are not. No confirmed defect in the nine runtime source files is established by this run.

- Target: `{PROJECT / 'src/agents/skills/qa'}`
- Run: `{ROOT.name}`
- Package digest: `{manifest['package_digest']}` (9 files, {sum(r['bytes'] for r in manifest['files'])} bytes)
- Rule-set SHA-256: `{ref(ROOT/'rule-set.json')['sha256']}`
- Selected origin: [MVP specification]({next(r['snapshot_path'] for r in bindings if r['original_path'].endswith('qa-skill-spec.md'))}) plus [extension]({next(r['snapshot_path'] for r in bindings if r['original_path'].endswith('qa-skill-postmvp-spec.md'))}); extension precedence applies only to its explicit amendments.
- Independence: primary validator assessed builder-delivered bytes; a separate description-only agent supplied routing classifications. Grader implementation tests are evaluator self-tests, not independent runtime skill acceptance.
- Builder readiness: **BLOCKED** by missing required evaluation evidence. Proposal review state: **not_needed**. No runtime source revision or installation is proposed.

## Preservation and sources

The authoring request bound successfully to exact current bytes. The [source snapshot](source/), [original manifest](source-manifest.json), [source-after manifest](source-after-manifest.json) and [preservation readback](preservation-readback.json) show target, both specifications, bound authoring inputs, operational QA and loaded validator unchanged. Historical evidence was never a write destination; the complete historical tree was not recursively hashed. There were no source-capture exclusions.

Authoring-v1 custody is kept in the sibling supplemental record; it is not relabeled as an adopted or legacy generated baseline. No historical quality result qualifies these edited bytes. [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills) was retrieved and retained, alongside the dated AV project-policy catalog. See [sources](sources.json) and the [rule binding note](rule-binding-note.md) for exact freshness and the nonsemantic source-ID correction.

## Assessment dimensions

| Dimension | Outcome | Required evaluated / total |
| --- | --- | --- |
{chr(10).join('| '+d+' | '+v['outcome']+' | '+str(v['required_evaluated'])+' / '+str(v['required_total'])+' |' for d,v in dimensions.items())}

Overall required checks evaluated: **{total['required_evaluated']}/{total['required_total']}**; unknown applicability: 0. Ten adaptive-only rules are justified NOT_APPLICABLE for this ordinary single skill. Required unperformed checks remain in the denominator. These are development assessment checks, not compiled-Rust admission or enforcement.

Static review covers all 40 QA/QAP requirements through the [requirement map](requirement-map.json), [workflow map](workflow-map.json) and [semantic review](semantic-review.json). It found coherent continuation, localized readiness, severity stops, complete-collection metrics, literal output delivery and manual repair ownership. Static conformance does not prove those branches execute.

## Executed checks and limits

- `observe.py structure`: exit 0; supported structural observations passed.
- Actual installed Skill Creator `quick_validate.py`: exit 0.
- `adaptive_observe.py package`: exit 2 / INCOMPLETE retained unchanged. Its original-directory identity and TODO candidates were manually resolved; 20 local links resolve, all nine resources have consumers, and no specified Unicode candidate was found. Token counts are NOT_RUN because local encoding data is unavailable; bytes/characters/lines were measured.
- Description routing: **10/10 expected labels matched**. The file-backed routing plan was saved after agent launch; this chronology limitation is disclosed. Explicit source loading in CLI pilots is not native implicit activation.
- Grader TDD: initial 20-test red result retained (24 failing assertions including subtests), then green; report-field extension red retained, then **29/29 tests passed**. No gratuitous refactor was made.
- Focused grader executed-line coverage: **{covered}/{lines} = {100*covered/lines:.8f}%**. Branch coverage: **{covered_branches}/{branches} = {100*covered_branches/branches if branches else 0:.8f}%**. Denominator is only `evaluation/graders.py`; native harness, JSONL runner and orchestration coverage are unmeasured. This is not whole-bundle or framework coverage. The instruction-only target has no executable source-line denominator.
- Bound [Python JSONL bundle](evaluation/bundle-manifest.json): [runner](evaluation/runner.py), [graders](evaluation/graders.py), [independent vectors](evaluation/fixtures.json), [expected results](evaluation/expected-results.json), [schema](inputs/evaluation-result.schema.json), [runtime](evaluation/runtime.json), three concrete native fixtures and exact source/spec/artifact bindings. Execution returned exit **2**, correctly reporting **28/28 grader controls passed and 0/42 complete skill scenarios qualified**. Controls do not count toward scenario pass rate.

## Cold native trials

| Trial | Attempt 001 | Approved attempt 002 | Behavioral observation |
| --- | --- | --- | --- |
| QPV-01 full run | CLI initialization access denied | 120-second timeout | Loaded exact skill, inspected fixture/tools, announced planning; no plan/report or test-launch artifact delivered. |
| QPV-02 explicit plan | CLI initialization access denied | 120-second timeout | Loaded selected skill and inspected inputs; no plan/report delivered. No product launch observed. |
| QPV-06 integrity | CLI initialization access denied | 120-second timeout | Correctly identified direct and resolved-alias mock decorators and announced FAIL/stop before testing; no subsequent command/test launch in retained trace, but report/fix delivery unfinished. |

Each attempt retains exact prompt, inputs, command, cwd, start/end, stdout/stderr, timeout, owned-process cleanup and before/after manifest. The child used workspace-write, inherited configured model/auth, and no bypass flags. Its prompt boundary is not proof of OS isolation. Parent-owned timeout cleanup terminated the recorded process trees; no candidate/fixture bytes changed. See [native observations](native-observations.json) and [command log](command-log.md).

These are three feasibility pilots, not a completed 42-scenario campaign. **39 scenario IDs were not separately attempted; all 42 remain NOT_RUN as complete scenarios.** The full native fixtures/variants for dependency sets, localized readiness, dynamic inspection, threshold collections, in-flight stop ordering, delivery failure, resume/retest, permissions, hostile inputs and the two-language portability pair remain outstanding. No claim is made that unattempted cases cannot run. No timeout is counted as a confirmed skill defect or passing evaluation, and no failed case was silently retried with a larger budget.

## Finding and change proposal

`{fid}` is an **input/evidence limitation**, not a runtime-source bug: mandatory native coverage and delivered outputs are incomplete. The [finding](findings.json) preserves exact affected obligations. No revision specification is justified by the current evidence; `proposed_spec` is null in [handoff](handoff.json). The [enforcement register](enforcement-recommendations.md) proposes no new controls.

## Next action

The remaining work is a separately selected continuation of independent evaluation: recheck these source/spec identities, explicitly choose adequate native case budgets, complete the remaining independent fixtures and graders, and preserve all current attempts. Start a fresh linked run if any input changed. The current 120-second pilots do not authorize larger-budget retries by themselves. No builder invocation, product repair, operational update, deployment or installation was performed. **Framework acceptance: NOT_EVALUATED.**
''')
write(ROOT/'handoff.json',dict(**meta,original_target_root=str(PROJECT/'src/agents/skills/qa'),original_manifest=ref(ROOT/'source-manifest.json'),origin=ref(ROOT/'origin-record.json'),proposed_spec=None,findings=ref(ROOT/'findings.json'),report=ref(ROOT/'validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='not_needed',review_instruction=None,builder_readiness='BLOCKED',readiness_reasons=['Required native scenarios and report delivery remain incomplete. No source revision is selected.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='Authoring-v1 current custody verified by intake; no adoption operation needed or invoked.',permitted_target_root=str(PROJECT/'src/agents/skills/qa'),preservation_requirements=['Do not edit target or operational copies during validation','Preserve both specifications, historical evidence and all current attempts','No builder execution or installation','New input bytes require a fresh linked validation run']))

receipts=[]
for p in sorted((ROOT/'observations').glob('*.receipt.json')):
    value=json.loads(p.read_bytes())
    receipts.append(f"- `{p.name}`: exit {value['exit_code']}; cwd `{value['cwd']}`; command `{json.dumps(value['command'],ensure_ascii=False)}`; {value['started']} to {value['ended']}.")
put(ROOT/'command-log.md','# Retained command receipts\n\nThe initial snapshot command and exploratory read-only file/tool discovery are in the conversation tool transcript; source-manifest.json retains actual snapshot output identity. This log lists retained executable observations, not fabricated execution for source prose.\n\n'+'\n'.join(receipts)+'\n\nNative attempt receipts live under trials/QPV-01, QPV-02 and QPV-06, with exact prompts, commands and stream files. Attempts 001 failed initialization; approved attempts 002 timed out at 120 seconds. No model override or bypass flag was used.\n')
print(json.dumps({'overall':'INCOMPLETE','dimensions':dimensions,'required':total,'finding':fid},indent=2))
