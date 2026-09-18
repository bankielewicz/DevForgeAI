"""Synthesize retained results; no target imports or mutations."""
import copy
import json
from pathlib import Path
from harness import RUN, ROOT, TARGET, LOADED, PRIOR, SPECS, EXPECTED, CHECKER, read, write, save, ref, sha, compact, inventory, now

results=json.loads(read(RUN/'probe-results.json'))+[json.loads(read(RUN/'results/H11.json'))]
fresh=[r for r in results if not r['case_id'].startswith('REPLAY')]
replay=[r for r in results if r['case_id'].startswith('REPLAY')]
assert len(fresh)==33 and sum(r['matched'] for r in fresh)==22
assert len(replay)==4 and not any(r['matched'] for r in replay)

before_names={'target':TARGET,'loaded-evaluator':LOADED,'companion':ROOT/'src/agents/skills/skill-builder'}
readbacks={}
for name,path in before_names.items():
    before=json.loads(read(RUN/'inputs'/f'{name}-before.json'))
    after=inventory(path)
    save(RUN/'readback'/f'{name}-after.json',after)
    readbacks[name]={'unchanged':before['files']==after['files'] and before['excluded_boundaries']==after['excluded_boundaries'],'package_digest':after['package_digest'],'files':len(after['files'])}
for name,digest in SPECS.items():
    readbacks[name]={'unchanged':sha(read(ROOT/'docs/plan'/name))==digest,'sha256':sha(read(ROOT/'docs/plan'/name))}
selected=json.loads(read(RUN/'inputs/prior-selected-before.json'))
readbacks['prior-selected']={'unchanged':all(sha(read(Path(r['path'])))==r['sha256'] for r in selected),'file_references':len(selected),'extent':'Selected prior documents, receipts, outputs and four fixture inventories only; no whole historical tree claim.'}
readbacks['AGENTS.md']={'unchanged':sha(read(ROOT/'AGENTS.md'))==sha(read(RUN/'inputs/AGENTS.md'))}
readbacks['checker']={'unchanged':sha(read(CHECKER))==json.loads(read(RUN/'inputs/checker-identity.json'))['sha256']}
assert all(r['unchanged'] for r in readbacks.values())
save(RUN/'final-input-readback.json',{'time':now(),'inputs':readbacks})

prior=json.loads(read(RUN/'inputs/prior/stable-findings.json'))['findings']
details=[
 ('QA-01','major','Duplicate check executions inflate totals','D01,D02,D03','D04,D05','VA-003, VA-014; AV-E01; VAT-24',
  'The helper accepts the same artifact across member/integration roles (including a Windows case alias) and accepts copied rows preserving the same run/check identity. D01/D02/D03 declare 87 required/evaluated rows although only 58 distinct check identities exist.',
  'Misleading coverage and accepted invalid records. This does not prove a false native task success. Shared citations and distinct checks are valid controls, not defects.'),
 ('QA-02','major','Required handoff obligation disappears as N/A','H01','H02,H03,H04,H05,H06,H07,H08,H09,H10,H11','VA-003, VA-014; AV-A10, AV-E01; VAT-04, VAT-05, VAT-24',
  'A required selected transfer is represented only by required NOT_APPLICABLE. The helper accepts PASS and 58/58, removing the required integration obligation. A valid required observation would produce 59 total; unavailable execution must remain NOT_RUN/INCOMPLETE.',
  'Invalid full-set success can be accepted despite missing required integration assessment. This is record coverage validation, not an executed producer/consumer failure.'),
 ('QA-03','minor','Exact protocol value has no Unicode candidate','U01,U02,U03','U04,U05,U06,U07','VA-004; AV-U01; VAT-06',
  'Literal U+FF54 in JSON schema_version is unreported. All three fresh layouts and the original P08 return OBSERVED/exit 0 with no candidate; the required result is a located unresolved candidate and INCOMPLETE/exit 2, absent other failures.',
  'A specific required scanner signal is missing. Severity is narrowed from prior major to minor: no runtime acceptance of the malformed protocol was demonstrated, and manual review or an exact downstream schema check can still reject it. It remains a required defect worth fixing.'),
 ('QA-04','major','Premature fence closure corrupts resource edges','F01,F02,F08,F09','F03,F04,F05,F06,F07,F10','VA-005; AV-F05, AV-R01; VAT-08',
  'A fence-like code line with trailing nonspace content toggles the fence off. Literal example links become false missing-resource failures. F08 additionally reports line 3 inside code while omitting the genuine missing link on line 5 after the valid closer.',
  'Both unsupported resource failures and missed real resource edges are reproduced. F08 exits 1 as expected but fails the content/line oracle, demonstrating why exit-only comparison is inadequate.')]
matrix=[]
for i,(qid,severity,title,bad,controls,req,description,impact) in enumerate(details):
    old=prior[i]
    identity=old['identity']
    assert 'F-'+sha(compact(identity))==old['finding_id']
    text=read(RUN/'source'/old['subject_path']).decode('utf-8')
    anchor=identity[2]
    assert anchor in text
    lineno=text[:text.index(anchor)].count('\n')+1
    matching=[r for r in results if r['finding']==qid]
    matrix.append(dict(qa_id=qid,stable_id=old['finding_id'],status='CONFIRMED',severity=severity,prior_severity=old['severity'],title=title,
                       subject_path=old['subject_path'],line=lineno,requirements=req,description=description,impact=impact,
                       reproductions=bad.split(','),controls=controls.split(','),results=matching,
                       remediation=f'FV-00{i+1}',repair_status='NOT_PERFORMED',scope='Read-only Windows helper assessment; no native activation or complete acceptance claim.'))
save(RUN/'finding-matrix.json',{'target_digest':EXPECTED,'findings':matrix,'fresh_cases':33,'fresh_matches':22,'fresh_mismatches':11,'original_replays':4,'original_reproduced':4})

lines=['# Focused finding validation — FAIL for assessed behavior','',
       '**All four QA findings are genuine and merit correction.** Each original reproducer failed again against unchanged delivered bytes, and an independently constructed fixture reproduced each mechanism. No repairs were made.','',
       '| Finding | Verdict | Severity | Repair priority |', '| --- | --- | --- | --- |']
for i,m in enumerate(matrix): lines.append(f"| {m['qa_id']}: {m['title']} | CONFIRMED | {m['severity']} | {'First: record integrity' if i<2 else 'Then: focused text scanner correction'} |")
lines+=['','## Findings and merit','']
for m in matrix:
    lines += [f"### {m['qa_id']} — {m['title']}",'',m['description'],'',m['impact'],'',
              f"Location: [captured source]({('source/'+m['subject_path'])}) line {m['line']}. Stable ID: `{m['stable_id']}`. Contract: {m['requirements']}.",
              f"Fresh reproductions: {', '.join(m['reproductions'])}. Controls: {', '.join(m['controls'])}. Exact expectations precede execution in [case plans](expectations-before-execution.json); H11 has [its separate plan](expectations-H11-before-execution.json).",'']
lines += ['## Evidence and scope','',
          '- 33 fresh cases: **22 matched, 11 mismatched** the specification-derived expectations. The 11 mismatches are repeated manifestations of four findings, not eleven new findings.',
          '- Four original replays: all four reproduce their previously reported failures. They are reported separately from fresh case counts.',
          '- Fresh false-positive cases: F01, F02, F08, F09 (4). Missed required rejections/candidates/edges: D01, D02, D03, H01, U01, U02, U03, F08 (8). F08 belongs to both groups; these counts must not be added as distinct cases.',
          '- Original replays: P07 false positive; R06/R07 missed rejections; P08 missed candidate. No native-model reliability rate is inferred.',
          '- Independent installed jsonschema 4.24.0 audit: **42 record shapes and 180 reference occurrences verified**, including original R06/R07. Source package manifests and required dependency references were independently reconciled. Shared schemas are input data; semantic expectations derive separately from frozen specifications.',
          '- **27/27 affected regression tests passed** (`test_adaptive.py`); installed quick_validate.py passed on exact captured bytes. Both are limited observations. The full historical 229-case suite was not repeated in this focused assessment; its prior result remains a prior claim, with no new repairs to qualify.',
          '- Fresh Python line/branch coverage: **NOT_RUN**. The previous 67.7758% line measurement is not refreshed or relabeled as current coverage. Coverage improvement and full regression/acceptance are requirements of the later maintenance QA, not evidence of whether these four defects exist.',
          '- Fresh-case conformance is 22/33 = 66.6667%, below 95%; each reproduced mandatory failure independently prevents a scoped PASS. Original replays and self-tests are not pooled to improve this percentage.',
          '- Both specification hashes match. Target and loaded evaluator each remain 75 files with package digest `'+EXPECTED+'`; their helpers therefore remain self-review. Independent harnesses import no target test/helper functions as oracles.',
          '- Native Windows Python 3.10, PyYAML 6.0.2. No WSL execution or checkout relocation; the added AGENTS.md performance guidance was read and followed.',
          '- No candidate fixture writes were observed. The target, loaded evaluator, companion package, checker, AGENTS.md, specifications and selected prior-evidence files match final readback. Whole operational homes and historical trees were not captured.',
          '- The CommonMark fence interpretation was checked against [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks); a bounded paraphrase and retrieval identity are [retained](inputs/commonmark-notes.md). No full Markdown renderer certification is claimed.',
          '', '## Remediation decision','',
          'Recommend the four focused fixes in [revision-spec.md](revision-spec.md). QA-01 and QA-02 are first priority because invalid coverage records can be accepted. QA-04 also deserves correction because the parser both invents and misses edges. QA-03 merits a localized scanner fix, with severity narrowed to minor; missing a candidate is not proof of runtime acceptance of an invalid protocol.',
          '', 'The proposal preserves public interfaces and closed schemas. It explicitly avoids banning shared citations, treating all Unicode as defects, rejecting valid FAIL/INCOMPLETE records, or suppressing real links to avoid false positives. No optional enhancement or broad coverage campaign is bundled.',
          '', 'A later authorized $skill-creator maintenance task must retain red tests, implement the selected corrections, and hand delivered bytes to fresh $skill-validator QA. Known provenance must be checked before changes; this assessment establishes an exact observed source capture, not generated/adopted custody. Proposal review and execution custody are separately represented in the handoff.',
          '', '## Separate conclusions and remaining work','',
          '**Focused implementation conformity: FAIL. Finding-verification work: completed. Repairs: NOT_PERFORMED.** The four findings remain persistent on current bytes.',
          '', 'Native whole-workflow/resume, implicit activation, complete lifecycle integration, tokenizer availability, Linux behavior, installation and Rust qualification were not exercised. Their previous gaps remain open. Closing these four issues would not establish full package acceptance.',
          '', 'Review the proposed corrections; then authorize only the selected repair scope against its exact digest. Fresh QA must check unchanged reproducers, new controls, the full regression suite and required coverage measurements. See [command log](command-log.md), [finding matrix](finding-matrix.json), and [final input readback](final-input-readback.json).','']
write(RUN/'finding-validation-report.md','\n'.join(lines))

# Legacy schema-1 output lives in an isolated root; do not recursively reinterpret
# arbitrary fixture/input records or operation receipts as evaluator authority.
recroot=RUN/'member-records'
manifest=json.loads(read(RUN/'source-manifest.json'))
save(recroot/'source-manifest.json',manifest)
save(recroot/'source-after-manifest.json',json.loads(read(RUN/'readback/target-after.json')))
for r in manifest['files']: write(recroot/'source'/r['path'],read(RUN/'source'/r['path']))
for name in ('skill-validator-adaptive-enhancement-spec.md','skill-builder-adaptive-enhancement-spec.md','commonmark-notes.md'):
    write(recroot/'inputs'/name,read(RUN/'inputs'/name))
for name in ('finding-validation-report.md','revision-spec.md','expectations-before-execution.json','expectations-H11-before-execution.json','finding-matrix.json','final-input-readback.json'):
    write(recroot/'inputs'/name,read(RUN/name))
sources=[]
for sid,name in [('governing','skill-validator-adaptive-enhancement-spec.md'),('companion','skill-builder-adaptive-enhancement-spec.md'),('commonmark','commonmark-notes.md')]:
    sources.append(dict(source_id=sid,original_path=str(RUN/'inputs'/name),retrieved_at_utc=None,sha256=sha(read(recroot/'inputs'/name)),snapshot_path='inputs/'+name,sections=['Pinned focused obligations'],freshness='snapshot_only'))
save(recroot/'sources.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',sources=sources))
rule_ids=[]
for line in read(RUN/'inputs/skill-validator-adaptive-enhancement-spec.md').decode().splitlines():
    if line.startswith('| AV-'): rule_ids.append(line.split('|')[1].strip())
selected_rules={'AV-E01','AV-A10','AV-U01','AV-R01'}
rules=[]
for rid in rule_ids:
    rules.append(dict(rule_id=rid,revision='frozen-1.0',title=rid,source_refs=[dict(**ref(recroot/'inputs/skill-validator-adaptive-enhancement-spec.md',recroot),source_id='governing',locator='3, 4, 6 and 7')],authority_class='project_policy',applicability='applicable' if rid in selected_rules else 'unknown',method='deterministic' if rid in selected_rules else 'semantic',expected_observation='Selected finding cases in pinned pre-execution plans.' if rid in selected_rules else 'Catalog considered; not selected for this focused review.',required=rid in selected_rules,limitation='Focused finding assessment, not complete enhancement validation.'))
save(recroot/'rule-set.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',rules=rules))
checks=[]
for r in results:
    cid=r['case_id']; q=int(r['finding'][-1])-1
    out=write(recroot/'inputs'/f'{cid}-stdout.txt',read(RUN/'commands'/cid/'stdout.txt'))
    receipt=write(recroot/'inputs'/f'{cid}-receipt.json',read(RUN/'commands'/cid/'receipt.json'))
    checks.append(dict(schema_version='1',run_id=RUN.name,check_id=cid,rule_id=['AV-E01','AV-A10','AV-U01','AV-R01'][q],subject_path=matrix[q]['subject_path'],method='deterministic',required=True,applicability='applicable',result='PASS' if r['matched'] else 'FAIL',reason='Matched independent expected output and effects.' if r['matched'] else 'Contract expectation mismatch; see retained raw output and finding matrix.',evidence=[ref(out,recroot)],dimension='workflow' if q<2 else 'standards'))
write(recroot/'checks.jsonl',b'\n'.join(compact(r) for r in checks)+b'\n')
findings=[]
for i,m in enumerate(matrix):
    f=copy.deepcopy(prior[i]); f.update(severity=m['severity'],description=m['description'],user_impact=m['impact'],verification_cases=m['reproductions']+m['controls'],disposition='proposed')
    f['source_refs']=[dict(**ref(recroot/'inputs/skill-validator-adaptive-enhancement-spec.md',recroot),source_id='governing',locator={'line_start':252,'line_end':252} if i<2 else {'line_start':96 if i==2 else 102,'line_end':98 if i==2 else 102})]
    f['observation_refs']=[ref(recroot/'inputs'/f'{cid}-stdout.txt',recroot) for cid in m['reproductions']]
    f['proposed_correction']='Apply only '+m['remediation']+' from the proposed focused revision, after separate authorization.'
    findings.append(f)
save(recroot/'findings.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',findings=findings))
save(recroot/'origin-record.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',original_source_root=str(TARGET),manifest=ref(recroot/'source-manifest.json',recroot),specification=ref(recroot/'inputs/skill-validator-adaptive-enhancement-spec.md',recroot),origin_kind='existing_spec',history_kind='observed',prior_evidence=None,completeness='complete',uncertainties=['Historical generated/adopted custody is not requalified in this focused finding review.'],source_readback_state='UNCHANGED',historical_origin='unknown'))
save(recroot/'workflow-map.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',steps=[dict(step_id='record-reduction',entrypoint='scripts/adaptive_observe.py records',inputs=['immutable selection','member checks','integration checks'],executor='Windows Python',outputs=['integrity observation'],next_steps=['caller reporting'],failure_recovery='Report mismatch; preserve raw input; no correction during validation.',evidence=[ref(recroot/'inputs/D01-stdout.txt',recroot)]),dict(step_id='text-scan',entrypoint='scripts/adaptive_observe.py package',inputs=['captured UTF-8 text'],executor='Windows Python',outputs=['Unicode candidates','resource edges'],next_steps=['manual semantic adjudication'],failure_recovery='Unperformed/candidate remains explicit; preserve original bytes.',evidence=[ref(recroot/'inputs/U01-stdout.txt',recroot),ref(recroot/'inputs/F08-stdout.txt',recroot)])]))
write(recroot/'enforcement-recommendations.md','# Enforcement register\n\nNo new enforcement mechanism proposed. These are local Python observation defects. Rust qualification and privileged acceptance remain outside this assessment.\n')
save(recroot/'handoff.json',dict(schema_version='1',run_id=RUN.name,target_name='skill-validator',original_target_root=str(TARGET),original_manifest=ref(recroot/'source-manifest.json',recroot),origin=ref(recroot/'origin-record.json',recroot),proposed_spec=ref(recroot/'inputs/revision-spec.md',recroot),findings=ref(recroot/'findings.json',recroot),report=ref(recroot/'inputs/finding-validation-report.md',recroot),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='pending',review_instruction=None,builder_readiness='BLOCKED',readiness_reasons=['Proposal is reviewable; later scoped maintenance authorization is separate.','Legacy generated/adopted execution custody was not established in this focused run; do not infer adoption. See authoring supplement for the observed scoped-edit basis.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='not_assessed',permitted_target_root=str(TARGET),preservation_requirements=['Companion and operational copies read-only','Frozen contracts and prior evidence unchanged']))
save(RUN/'authoring-handoff-supplement.json',{'record_kind':'focused-observed-edit-handoff','target_digest':EXPECTED,'target_manifest':ref(RUN/'source-manifest.json'),'proposal':ref(RUN/'revision-spec.md'),'proposal_review_state':'pending','reviewed_findings':[m['stable_id'] for m in matrix],'authorized_for_repair':False,'observed_scoped_edit_basis':ref(RUN/'source-manifest.json'),'basis_limit':'Exact current-byte capture; not a generated/adopted baseline and not proof that known historical custody is valid. The later maintainer must inspect applicable provenance and explicitly select the supported edit basis.','adoption_is_not_automatically_required':True,'legacy_handoff':ref(recroot/'handoff.json')})

commands=[]
for dest in sorted((RUN/'commands').iterdir()):
    if (dest/'receipt.json').exists(): commands.append(json.loads(read(dest/'receipt.json')))
save(RUN/'command-log.json',commands)
log=['# Candidate execution log','', 'All retained command receipts include argv, working directory, stdout/stderr hashes, timing, timeout, effects and termination. Candidate mismatch exit codes are expected evidence, not setup failures. No attempt was retried or overwritten.','']
for c in commands:
    cid=c['case_id']; log += [f'## {cid}','', '```json',json.dumps(c['argv'],ensure_ascii=False),'```','',f"Cwd: `{c['cwd']}`. Start: {c['start']}; end: {c['end']}; elapsed: {c['elapsed_seconds']:.3f}s; exit: {c['exit']}; timeout: {c['timed_out']}.",f'[stdout](commands/{cid}/stdout.txt) · [stderr](commands/{cid}/stderr.txt) · [receipt](commands/{cid}/receipt.json)','']
write(RUN/'command-log.md','\n'.join(log))
print('Reports and isolated legacy records written. Fresh: 22/33. Four findings confirmed. Readbacks unchanged.')
