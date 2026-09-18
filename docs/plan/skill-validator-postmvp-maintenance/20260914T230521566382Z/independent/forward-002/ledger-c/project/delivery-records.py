"""Synthesize adjudicated run-bound records from retained execution evidence."""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RUN=Path(json.loads((ROOT/'validation-run.json').read_text())['run'])
VALIDATOR=ROOT.parents[1]/'evaluator/skill-validator'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(name): return {'path':name,'sha256':sha(RUN/name)}
def put(name,value):
    p=RUN/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def prose(name,value): (RUN/name).write_text(value,encoding='utf-8')
meta={'schema_version':'1','run_id':RUN.name,'target_name':'ledger-c'}
rows=[json.loads(l) for l in (RUN/'trials/helper-suite/work/results.jsonl').read_text().splitlines()]
assert len(rows)==24 and all(r['result']=='PASS' for r in rows)
receipt=json.loads((RUN/'trials/helper-suite/attempt-001/result.json').read_text())
assert receipt['outcome']=='PASS' and receipt['cleanup']=='VERIFIED'
manifest=json.loads((RUN/'source-manifest.json').read_text())
argv=[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(ROOT/'skills/ledger-c'),'--manifest',str(RUN/'source-manifest.json')]
r=subprocess.run(argv,capture_output=True,timeout=120)
(RUN/'observations/readback.stdout.txt').write_bytes(r.stdout)
(RUN/'observations/readback.stderr.txt').write_bytes(r.stderr)
readback=json.loads(r.stdout); assert r.returncode==0 and readback['status']=='MATCH'
put('source-after-manifest.json',readback['manifest'])
pins=json.loads((RUN/'inputs/pinned-inputs.json').read_text())
assert sha(ROOT/'specification.md')==pins['original_specification']['sha256']
assert sha(RUN/'rule-set.json')==pins['rule_set_sha256']
assert sha(RUN/'sources.json')==pins['sources_sha256']
source_checks=[]
for s in json.loads((RUN/'sources.json').read_text())['sources']:
    source_checks.append({'source_id':s['source_id'],'expected':s['sha256'],'actual':sha(Path(s['original_path']))})
assert all(x['expected']==x['actual'] for x in source_checks)
put('observations/input-readback.json',{'source_checks':source_checks,'specification':'UNCHANGED','rule_set':'UNCHANGED','sources':'UNCHANGED','argv':argv})
put('origin-record.json',dict(meta,original_source_root=str(ROOT/'skills/ledger-c'),manifest=ref('source-manifest.json'),specification=ref('inputs/specification.md'),origin_kind='existing_spec',history_kind='observed',prior_evidence=None,completeness='complete',uncertainties=[],source_readback_state='UNCHANGED',historical_origin='unknown'))
prose('observations/native-capability.md', '''# Native capability observation

The installed `codex exec --help` command exited 0 during intake, but emitted these diagnostics (transcribed from the retained conversation tool result; not a second execution):

```
WARNING: failed to clean up stale arg0 temp dirs: Access is denied. (os error 5)
WARNING: proceeding, even though we could not create PATH aliases: Access is denied. (os error 5) at path "C:\\Users\\bryan\\.codex\\tmp\\arg0\\codex-arg0t36Iwu"
```

The CLI supports `--ephemeral`, `--sandbox`, `--skip-git-repo-check`, `--json`, and `--output-last-message`. Ephemeral session persistence does not establish containment of global startup effects. Read-only configuration inspection observed model gpt-6-astra and node_repl/openaiDeveloperDocs MCP sections. No credentials were inspected or copied. No config, authentication, model, hook, permission, or installation changes were made. CLI version was not queried after the startup-side-effect warning.

Current user scope prohibits external mutation. Native positive, invalid-input and implicit-discovery cases remain NOT_RUN because native host side effects cannot be established as contained using current permissions/configuration. This is an evaluator capability limitation, not a ledger-c defect. No native attempt was launched, and none was retried.
''')
prose('observations/semantic-review.md','''# Semantic review of complete captured package

Primary validator self-review; no independent actor or native activation claim.

- SKILL.md lines 1-4: unique valid YAML with ledger-c name matching original directory in source-manifest.json. The adaptive helper's source-directory NOT_RUN is resolved by this separately authored identity check, without editing helper stdout.
- SKILL.md line 3: trigger explicitly concerns totaling an integer JSON file. Positive example: "Sum the integers in data.json and write totals.json." Near misses: "Average a CSV column" and "Concatenate JSON strings." Manual classification is appropriate/irrelevant/irrelevant. No independently blinded routing classification was performed.
- SKILL.md line 8: resolves scripts/total.py relative to the skill, passes INPUT OUTPUT positionally, reads the delivered file, and reports diagnostics on invalid input. This inline command establishes the helper resource edge even though the conservative Markdown graph did not detect it. Both files are used runtime resources; no orphans or missing links. No other Markdown links/anchors need adjudication.
- Complete 585-byte entrypoint and 850-byte helper reviewed. No Unicode, scaffolding, unfinished fences, harmful ceremony, contradictory examples, unsupported override claims, or hidden instructions found. Tokenizer measurements not selected; no token budget applies. Static execution branch loads entrypoint and helper once each; actual model token use is unmeasured.
- Useful instructions retained verbatim: "Read the delivered file back before reporting completion." and "Preserve the source and unrelated files." These produce observable output and preservation obligations; they are not enforcement claims. "On invalid input, report the helper diagnostic" defines a useful failure route.
- total.py lines 1-5: argparse supplies --help and validates two positional arguments. Only stdlib imports. Trials run Python 3.10.11 with -S, excluding site packages.
- total.py lines 7-14: same resolved path or same underlying file rejected before write; JSON parsed as data, list required, exact int excludes bool. ValueError/OSError diagnosed on stderr with exit 2. Hostile instruction text is rejected as noninteger data.
- total.py line 15: writes one JSON object with the computed total to selected destination. Writable existing destination is intentionally replaced; no extra unrelated write observed. No network, subprocess, credential, installation, or production service dependency.
- Scope limits: permission-denied destination, disk-full interruption, adversarial concurrent file replacement, and all Python 3 versions were not exercised. Atomic writes are not promised by R1-R4. Ordinary overwrite is exercised; interruption/resume has no specified protocol and remains unperformed under AV-W02.
- Specification R1-R4 is explicit and unchanged. No target repair or enhancement is justified by observed evidence. Unperformed native actor readback/delivery cannot be promoted from direct helper behavior.
''')
steps=[]
for sid,inputs,action,outputs,next_steps,failure,terminal in [
 ('select',['user input path','selected output path'],'Resolve the skill-relative helper and input/output arguments',['helper argv'],['execute'],'Missing paths/arguments: report argparse or filesystem diagnostic','Concrete missing-input error'),
 ('execute',['helper argv','input JSON bytes'],'Run Python helper; reject aliases and noninteger arrays; otherwise write total',['output JSON or stderr/nonzero'],['verify','reject'],'Reject invalid data before output creation','Failure with useful diagnostic'),
 ('verify',['selected output JSON'],'Read output file back, then report completion',['verified output path'],[],'If no usable output exists, report failure; do not substitute prose','Delivered JSON file'),
 ('reject',['helper stderr/nonzero'],'Report diagnostic without inventing a total',['user-visible diagnostic'],[],'No automatic retry requested','Invalid input reported with no new output')]:
    steps.append({'step_id':sid,'entrypoint':{'path':'source/SKILL.md','line':8},'entry_conditions':['User supplies input and selected output'], 'inputs':inputs,'executor':'Codex actor with Python helper','action':action,'outputs':outputs,'completion_evidence':['trials/helper-suite/work/results.jsonl; native delivery NOT_RUN'],'next':next_steps,'failure_route':failure,'terminal_user_outcome':terminal})
put('workflow-map.json',dict(meta,steps=steps))
rules=json.loads((RUN/'rule-set.json').read_text())['rules']; checks=[]
for rule in rules:
    rid=rule['rule_id']; na=rule['applicability']=='not_applicable'
    dimension='standards' if rid.startswith(('AV-F','AV-U','AV-R')) or rid=='CREATOR' else 'instructions' if rid.startswith('AV-I') or rid=='AV-C01' else 'workflow' if rid.startswith('AV-W') else 'behavior'
    status='NOT_APPLICABLE' if na else 'NOT_RUN' if rid in ('AV-W01','AV-W02','AV-I04') else 'PASS'
    reason='Ordinary standalone skill has no adaptive contract, bindings or selected set; optional agents/openai.yaml absent.' if na else 'Complete captured text manually reviewed with preserved helper observations and bounded execution evidence.'
    if status=='NOT_RUN': reason='Static workflow is coherent and helper effects passed; native actor execution/corrections/delivery and interruption behavior were not observed under current host constraints.'
    evidence=[ref('observations/semantic-review.md'),ref('source/SKILL.md'),ref('source/scripts/total.py')]
    if rid in ('R1','R2','R3','R4','AV-R03','AV-S01','AV-S02'): evidence += [ref('trials/helper-suite/work/results.jsonl'),ref('trials/helper-suite/attempt-001/result.json')]
    if rid.startswith(('AV-F','AV-U')) or rid=='AV-C01': evidence += [ref('observations/package.stdout.txt'),ref('observations/structure.stdout.txt')]
    if rid=='CREATOR': evidence += [ref('observations/creator.stdout.txt')]
    if status=='NOT_RUN': evidence += [ref('observations/native-capability.md'),ref('trials/native-plan.json')]
    if rid=='AV-E01': evidence += [ref('observations/input-readback.json'),ref('observations/readback.stdout.txt'),ref('trials/helper-suite/plan.json')]
    checks.append(dict(meta,check_id=rid+'-assessment',rule_id=rid,subject_path='source/SKILL.md',method='behavioral' if rid.startswith('R') or status=='NOT_RUN' else rule['method'],required=rule['required'],applicability=rule['applicability'],result=status,reason=reason,evidence=evidence,dimension=dimension))
for cid,rule in [('native-positive','AV-W01'),('native-negative','AV-W01'),('native-discovery','AV-F03')]:
    checks.append(dict(meta,check_id=cid,rule_id=rule,subject_path='source/SKILL.md',method='behavioral',required=True,applicability='applicable',result='NOT_RUN',reason='Native workflow/activation not launched: current host startup effects are not contained within authorized project.',evidence=[ref('trials/native-plan.json'),ref('observations/native-capability.md')],dimension='behavior'))
(RUN/'checks.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in checks),encoding='utf-8')
anchor='Read the delivered file back before reporting completion.'
identity=['AV-W01','source/SKILL.md',anchor,0]
fid='F-'+hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
put('findings.json',dict(meta,findings=[{'finding_id':fid,'identity':identity,'rule_id':'AV-W01','category':'input_evidence_limitation','severity':'advisory','subject_path':'source/SKILL.md','locator':{'line_start':8,'line_end':8},'source_refs':[dict(ref('inputs/adaptive-validation.md'),source_id='av',locator='AV-W01')],'observation_refs':[ref('observations/native-capability.md')],'description':'Native skill workflow and discovery remain unperformed under current host effects restrictions; no demonstrated target defect.','user_impact':'Helper conformance is supported, but end-to-end actor delivery cannot receive PASS.','proposed_correction':'No skill change proposed. Complete fresh native cases only in an already authorized host environment containing its effects.','preserved_requirements':['R1','R2','R3','R4'],'verification_cases':['native-positive','native-negative','native-discovery'],'disposition':'deferred'}]))
dimensions={}
for dim in ['standards','workflow','instructions','behavior']:
    selected=[c for c in checks if c['dimension']==dim and c['required'] and c['applicability']!='not_applicable']
    dimensions[dim]={'outcome':'INCOMPLETE' if any(c['result']=='NOT_RUN' for c in selected) else 'PASS','required_evaluated':sum(c['result'] in ('PASS','FAIL') for c in selected),'required_total':len(selected)}
total=sum(d['required_total'] for d in dimensions.values()); evaluated=sum(d['required_evaluated'] for d in dimensions.values())
put('assessment.json',dict(meta,assessment_completed=True,overall_assessment='INCOMPLETE',dimensions=dimensions,required_evaluated=evaluated,required_total=total,unknown_applicability=0))
prose('enforcement-recommendations.md','# Enforcement recommendations\n\nNo candidates. This local utility needs no proposed hooks, CI, admission gate, or production enforcement. Preserve input, output readback and invalid-input safeguards as useful guidance. This assessment is development evidence; compiled Rust framework acceptance is outside scope.\n')
put('trials/helper-suite/result-schema.json',{'type':'object','required':['case_id','requirements','argv','cwd','timeout_seconds','started_at','ended_at','exit_code','stdout','stderr','before','after','changed_paths','preserved','output','result'],'properties':{'result':{'enum':['PASS','FAIL']},'preserved':{'type':'boolean'},'exit_code':{'type':'integer'}}})
put('evaluation-bundle.json',dict(meta,package=ref('source-manifest.json'),specification=ref('inputs/specification.md'),runner=ref('trials/helper-suite/helper-trials.py'),fixtures_and_expected=ref('trials/helper-suite/cases.json'),schema=ref('trials/helper-suite/result-schema.json'),results=ref('trials/helper-suite/work/results.jsonl'),grader_controls=ref('trials/helper-suite/grader-controls.json'),sealed_plan=ref('trials/helper-suite/plan.json'),runtime=ref('inputs/host.json')))
table='\n'.join(f'| {k} | {v["outcome"]} | {v["required_evaluated"]}/{v["required_total"]} |' for k,v in dimensions.items())
report=f'''# ledger-c validation report

## Identity and conclusion

**Overall: INCOMPLETE. Assessment completed: true.** The Python helper performed the specified task in all 24 declared utility cases. No target defect was demonstrated. Native actor workflow, corrections/readback/delivery, and discovery remain NOT_RUN under current host effects restrictions. Primary validator self-review; no independent reviewer or cold actor was used.

- Run: `{RUN.name}`
- Package digest: `{manifest['package_digest']}`
- Pinned rule-set digest: `{sha(RUN/'rule-set.json')}`
- Specification digest: `{sha(RUN/'inputs/specification.md')}`
- Builder readiness: **BLOCKED** by unperformed required capability evidence; proposal review: **not_needed**. No source change is proposed.

## Origin, sources and preservation

Explicit [specification](inputs/specification.md), observed history with unknown historical origin. [Origin record](origin-record.json), [exact snapshot](source/SKILL.md), [manifest](source-manifest.json), [source readback](observations/readback.stdout.txt), [after manifest](source-after-manifest.json). Both captured files are unchanged; no exclusions. Original specification, selected local rule sources, rules and source bindings rechecked unchanged in [input readback](observations/input-readback.json).

Rules were pinned before observations. [Sources](sources.json) include local AV policy and dated fallback guidance. Read-only official refresh redirected to [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills); returned excerpts are retained under inputs/official-refresh-*.txt. The initial response was dominated by navigation and Markdown retrieval failed. Later useful excerpts are supplemental; they did not replace pinned expectations. This report claims only selected snapshot/profile coverage, not comprehensive current-live standards compliance.

## Assessment dimensions

| Dimension | Outcome | Required evaluated/total |
| --- | --- | --- |
{table}

Total: **{evaluated}/{total}** applicable required check rows evaluated, zero unknown applicability. Native scenarios are separate check rows, not extra successful helper cases. Adaptive-only rules and absent optional configuration are justified NOT_APPLICABLE. [Checks](checks.jsonl) and [machine assessment](assessment.json) retain all gaps. Enforcement recommendations: [no candidates](enforcement-recommendations.md).

## Findings and contextual instruction review

[Finding {fid}](findings.json) records an evidence limitation, not a target implementation defect. The native CLI is present but even help attempted global temporary writes and reported access denied; no contained native host execution was established without prohibited configuration changes. [Capability details](observations/native-capability.md).

[Semantic review](observations/semantic-review.md) and [workflow map](workflow-map.json) trace input selection, invocation, validity/alias rejection, total-file creation, readback and error delivery. The input preservation/readback instructions are useful and retained. Inline scripts/total.py routing is real despite the conservative helper graph reporting no edge. The source-directory identity NOT_RUN in raw package output is independently resolved using the original ledger-c root and bound manifest. Raw observations remain unchanged.

## Trials and limits

**Helper behavior: 24/24 PASS.** Positive totals, negative numbers, empty arrays, zero, whitespace, integers beyond JavaScript's safe range, selected overwrite, nonarrays, bool/float/string/null/nested elements, malformed JSON, instruction-like data, missing input/arguments, --help, spaced paths, same-path and hardlink aliases. Invalid-input cases returned nonzero with useful stderr and created no new result. Every source and unrelated sentinel remained byte-identical. Output JSON contents were read back and compared with fixed independent expectations.

- [Frozen cases/oracles](trials/helper-suite/cases.json), [sealed plan](trials/helper-suite/plan.json), [24 per-case results with commands and streams](trials/helper-suite/work/results.jsonl), [summary](trials/helper-suite/work/summary.json).
- [Actual sealed runner receipt](trials/helper-suite/attempt-001/result.json): exit 0, no timeout, unchanged protected inputs, Windows Job cleanup VERIFIED. [Runner check](trials/helper-suite/check.stdout.txt), before/after manifests and all artifacts retained in attempt-001 and work. No retries.
- Eight [grader controls](trials/helper-suite/grader-controls.json) passed, including wrong totals, Boolean totals, absent results, source changes, unrelated writes and invalid-input output creation. These are grader checks, not target coverage.
- Python 3.10.11 Windows; target helper used `-S` to exclude site packages. Helper and whole suite limits: 120 seconds. [Evaluation bundle](evaluation-bundle.json) binds runtime, schema, fixtures, grader and results to exact inputs.
- [Native inventory](trials/native-inventory.json) and [planned obligations](trials/native-plan.json): positive, invalid-input and discovery NOT_RUN, selected 600-second limit; no native attempt launched. Description routing has a manual positive/two-near-miss review only, without blinded independent classification or discovery evidence.
- Atomic interruption, disk-full/output-permission errors, concurrent hostile path replacement and other Python/OS versions were not exercised. No universal performance, race safety or exhaustive runtime coverage claim. Framework line coverage/acceptance is not applicable to this supporting utility assessment; target line coverage was not measured.

## Proposed changes and next action

No revision-spec.md is warranted by observed target evidence. Preserve the original skill and specification. [Handoff](handoff.json) records BLOCKED execution readiness and no selected repair. To establish full workflow conformance, run fresh native positive, rejection, corrections and discovery observations in an already authorized environment that contains host effects. No installation, external mutation or permission change was attempted to force those observations.

Reports and evidence are development observations, not compiled-Rust framework acceptance. Record-integrity verification is delivered separately in observations/records.stdout.txt; it validates references and reductions, not semantic truth or native execution.
'''
prose('validation-report.md',report)
put('handoff.json',dict(meta,original_target_root=str(ROOT/'skills/ledger-c'),original_manifest=ref('source-manifest.json'),origin=ref('origin-record.json'),proposed_spec=None,findings=ref('findings.json'),report=ref('validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[fid],proposal_review_state='not_needed',review_instruction=None,builder_readiness='BLOCKED',readiness_reasons=['Required native capability/evidence remains unperformed; no target change proposed.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='Not assessed; no adoption requested.',permitted_target_root=str(ROOT/'skills/ledger-c'),preservation_requirements=['Preserve complete original target and specification bytes.','No installation, external mutation, repair, or config changes.']))
prose('command-log.md','# Command and effects log\n\nIntake read explicit validator instructions, linked references, selected target/specification, ancestor AGENTS.md, checker implementation and bounded helper code. Git identity checks found no repository. Python/PyYAML and CLI help discovery were performed; native startup limitations are retained in observations/native-capability.md. Read-only official refresh responses are retained under inputs.\n\nThe retained validation-driver.py documents snapshot creation, rules pinning, package checks and sealed utility orchestration. observations/*.command.json and trials/helper-suite/*.command.json preserve argv, cwd, timeout, timestamps and exits. Target child commands and complete streams are in trials/helper-suite/work/results.jsonl. Readback argv is in observations/input-readback.json. All generated outputs are within this project; original skill/specification are unchanged. No native session, retry, repair, installation or configuration mutation was performed.\n')
relative=(RUN/'validation-report.md').relative_to(ROOT).as_posix()
(ROOT/'review.md').write_text(f'''# ledger-c validation delivery

**Assessment: INCOMPLETE.** [Actual validation report]({relative}).

The helper passed all **24/24** declared cases; structural checks and input preservation passed. No target defect was demonstrated. Native workflow, actor delivery/corrections, and discovery remain **NOT_RUN** because current host effects could not be contained within the authorized project without configuration changes.

The skill and specification are unchanged. Fixtures, raw results, sealed execution receipts, findings and handoff are linked from the report. No repair or revision specification is proposed; builder readiness is **BLOCKED** by the evidence gap. This is development validation, not framework acceptance.
''',encoding='utf-8')
print(json.dumps({'run':str(RUN),'assessment':'INCOMPLETE','coverage':[evaluated,total],'dimensions':dimensions}))
