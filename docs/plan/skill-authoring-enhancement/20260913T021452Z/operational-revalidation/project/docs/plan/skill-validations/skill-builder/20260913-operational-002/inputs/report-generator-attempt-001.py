import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path

R=Path(__file__).parent.resolve()
TASK=R.parents[5]
ROOT=TASK.parent
PRIOR=ROOT/'operational-assessment/project/docs/plan/skill-validations/skill-builder/20260913-operational-001'
VALIDATOR=ROOT/'inputs/operational-validator'
SPEC=ROOT/'inputs/skill-builder-authoring-enhancement-spec.md'
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p,**kw): return dict(path=p.relative_to(R).as_posix(),sha256=h(p),**kw)
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text(p,v): p.write_text(v,encoding='utf-8')
def source(path,line): return ref(R/'source'/path,locator={'line_start':line,'line_end':line})
now=dt.datetime.now(dt.timezone.utc).isoformat()
old=json.loads((PRIOR/'source-manifest.json').read_text()); current=json.loads((R/'source-manifest.json').read_text()); rb=json.loads((R/'inputs/readback-stdout.json').read_text())
assert current['files']==rb['manifest']['files'] and rb['status']=='MATCH'
assert h(SPEC)==h(R/'inputs/enhancement-spec.md')=='43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14'
save(R/'source-after-manifest.json',rb['manifest'])
for rel in ['findings.json','assessment.json','source-manifest.json','validation-report.md','workflow-map.json','sources.json','revision-spec.md','inputs/records-attempt-001.json']:
    dest=R/'inputs/prior'/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes((PRIOR/rel).read_bytes())
validator_checks=[]
for rel in ['SKILL.md','scripts/observe.py','references/origin.md','references/rules.md','references/trials.md','references/reporting.md','references/handoff.md','assets/rules-snapshot.json']:
    p=VALIDATOR/rel; dest=R/'inputs/validator'/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.read_bytes())
    oldp=PRIOR/'inputs/validator'/rel
    if rel=='assets/rules-snapshot.json': oldp=PRIOR/'inputs/rules-fallback.json'
    validator_checks.append(dict(original_path=str(p),retained=ref(dest),same_as_previously_loaded=oldp.exists() and h(p)==h(oldp)))
assert all(x['same_as_previously_loaded'] for x in validator_checks)
save(R/'input-readback.json',dict(schema_version='1',checked_at_utc=now,specification_original_path=str(SPEC),specification=ref(R/'inputs/enhancement-spec.md'),specification_unchanged=True,validator_inputs=validator_checks))
sources=json.loads((R/'sources.json').read_text())
old_sources=json.loads((PRIOR/'sources.json').read_text())['sources']
for row in sources['sources']:
    if row['source_id']=='standard':
        row['retrieved_at_utc']=next(x['retrieved_at_utc'] for x in old_sources if x['source_id']=='standard')
        row['freshness']='snapshot_only'; row['reuse_note']='Exact retained live retrieval from the linked prior assessment, no fresh network retrieval.'
save(R/'sources.json',sources)

oldrows={x['path']:x for x in old['files']}; newrows={x['path']:x for x in current['files']}
changed=[p for p in sorted(set(oldrows)|set(newrows)) if oldrows.get(p)!=newrows.get(p)]
diff=''
for p in changed:
    left=(PRIOR/'source'/p).read_text(encoding='utf-8').splitlines(True) if p in oldrows else []
    right=(R/'source'/p).read_text(encoding='utf-8').splitlines(True) if p in newrows else []
    diff+=''.join(difflib.unified_diff(left,right,fromfile='prior/'+p,tofile='current/'+p))+'\n'
text(R/'inputs/package-diff.txt',diff)
save(R/'package-comparison.json',dict(schema_version='1',prior_run=str(PRIOR),prior_manifest=ref(R/'inputs/prior/source-manifest.json'),current_manifest=ref(R/'source-manifest.json'),prior_digest=old['package_digest'],current_digest=current['package_digest'],changed_paths=changed,added_paths=sorted(set(newrows)-set(oldrows)),removed_paths=sorted(set(oldrows)-set(newrows)),diff=ref(R/'inputs/package-diff.txt'),limitations=['Compared actual selected snapshots. Builder delivery evidence was not selected; do not claim an independently verified build/delivery manifest chain.']))
assert set(changed)=={'scripts/authoring.py','scripts/custody.py','references/conversion-rules.md','package-manifest.json'}
origin=dict(schema_version='1',run_id=R.name,target_name='skill-builder',original_source_root=str(TASK/'skill-builder'),manifest=ref(R/'source-manifest.json'),specification=ref(R/'inputs/enhancement-spec.md'),origin_kind='existing_spec',history_kind='observed',historical_origin='unknown',prior_evidence=ref(R/'inputs/prior/assessment.json'),completeness='complete',uncertainties=['Prior assessment evidence is linked, not a builder custody baseline.','No actual builder delivery records were selected; comparison binds the two observed snapshots only.'],source_readback_state='UNCHANGED')
save(R/'origin-record.json',origin)

findings=json.loads((PRIOR/'findings.json').read_text())['findings']
resolutions=[]
for oldf,cases,src,explanation in [
 (findings[0],['malformed-contract','record-write-failure'],'scripts/authoring.py','Malformed known_issues:null now rejects at begin before target creation. A separate real-write record-save fault returns and retains PARTIAL, applied SKILL.md and matching delivered manifest; no publication readback appears.'),
 (findings[1],['name-64'],'scripts/authoring.py','A valid existing 64-character identity now begins and publishes AUTHORED without renaming; unrelated bytes remain preserved. The comparison changed >=64 to >64.'),
 (findings[2],['synthetic-import'],'references/conversion-rules.md','Active import guidance now explicitly preserves supported compatibility metadata and assigns checker disagreements to later validator assessment. The synthetic CSV import preserved name, description, compatibility, license, metadata, resource bytes and output contract; removed only Claude model and adapted Read wording.')]:
    case_refs=[]
    for cid in cases:
        p=R/'trials'/cid/'result.json'; result=json.loads(p.read_text()); assert result['result']=='PASS'; case_refs.append(ref(p))
    resolutions.append(dict(prior_finding_id=oldf['finding_id'],status='resolved',scope='Exact prior defect and bounded cases',prior_finding_source=ref(R/'inputs/prior/findings.json'),current_source=ref(R/'source'/src),observations=case_refs,description=explanation,limitations='Helper/manual-host observations do not establish independent cold workflow behavior or native activation.'))
save(R/'revalidation.json',dict(schema_version='1',run_id=R.name,target_name='skill-builder',prior_assessment=ref(R/'inputs/prior/assessment.json'),comparison=ref(R/'package-comparison.json'),resolutions=resolutions,new_findings=[],persistent_findings=[],unverified_prior_findings=[]))
save(R/'findings.json',dict(schema_version='1',run_id=R.name,target_name='skill-builder',findings=[],note='All prior findings resolved at their tested scope; linkage is in revalidation.json. Prior finding bytes remain in inputs/prior/findings.json.'))

steps=[]
for sid,entry,action,outs,next_,failure in [
 ('resolve','SKILL.md:11-24','Resolve authorized operation, identity, inputs and destination; route conversation/spec/import/edit/adopt.',['selected scope and destination'],'capture','Material ambiguity or known-history conflict remains concrete input issue.'),
 ('capture','references/authoring.md; scripts/authoring.py:241-302','Validate contract field kinds, references and custody; capture before/candidate and known or observed origin.',['contract.json','origin.json','before-manifest.json','before/','candidate/'],'author','Malformed contract rejects before target mutation; capture failures retain partial evidence.'),
 ('author','SKILL.md:26-32; references/conversion-rules.md:17-18','Apply authorized candidate edits, preserve supported metadata/resources/contracts, adapt source host mechanisms.',['candidate files','import dispositions where applicable'],'publish','Missing essential capability blocks dependent work; do not run authored skill or quality checker.'),
 ('publish','scripts/authoring.py:304-454','Compare B/C/N, reject drift/conflicts, write per-path and read back, retain authoring record or partial failure.',['delivered manifest','authoring record or publication-failure with actual applied delta'],'handoff','Ordinary and record-save failures return retained PARTIAL/BLOCKED as appropriate; no successful baseline from failure.'),
 ('handoff','references/validation-handoff.md; scripts/authoring.py:424-442','Publish exact authoring baseline and manual validator request, confirm publication readback.',['authoring-baseline.json','validation-request.json','validator-request.md','publication-readback.json'],'stop','Publication error retains failed attempt; no automatic validator or retry.'),
 ('revise','references/regeneration.md; references/adoption.md','Use verified current authored/adopted/legacy baseline for later authorized edit without requiring quality completion.',['fresh linked authoring run'],'capture','Do not bypass conflicting/missing known history or silently adopt.')]:
    steps.append(dict(step_id=sid,entrypoint=entry,entry_conditions='Current authorized scope and producer artifacts exist',inputs=['current task and selected specification','selected package/prior custody as applicable'],executor='Host agent and bundled Python custody helpers',action=action,outputs=outs,completion_evidence=outs,next_targets=[next_],branch_targets=[],failure_route=failure,terminal_user_outcome='Authored package/manual request, explicit unresolved decision, or retained incomplete effect report'))
save(R/'workflow-map.json',dict(schema_version='1',run_id=R.name,target_name='skill-builder',steps=steps,note='Unchanged routed behavior was rechecked by exact source comparison; edited custody/import paths were inspected and exercised.'))
save(R/'ceremonial-review.json',dict(schema_version='1',passages=[dict(subject_path='source/references/conversion-rules.md',locator={'line_start':18,'line_end':18},exact_excerpt=(R/'source/references/conversion-rules.md').read_text().splitlines()[17],classification='useful_instruction',intended_effect='Preserve supported metadata; defer checker disagreement',disposition='Preserve',evidence=source('references/conversion-rules.md',18)),dict(subject_path='source/SKILL.md',locator={'line_start':8,'line_end':8},exact_excerpt=(R/'source/SKILL.md').read_text().splitlines()[7],classification='useful_instruction',intended_effect='Keep authoring and quality execution ownership distinct',disposition='Preserve',evidence=source('SKILL.md',8))]))

checks=[]
def check(cid,rule,dim,result,reason,evidence,required=True,subject='source/SKILL.md'):
    checks.append(dict(schema_version='1',run_id=R.name,check_id=cid,rule_id=rule,subject_path=subject,method='behavioral' if dim=='behavior' else 'deterministic' if dim=='standards' else 'semantic',required=required,applicability='applicable',result=result,reason=reason,evidence=evidence,dimension=dim))
structure=json.loads((R/'inputs/structure-stdout.json').read_text()); assert structure['status']=='OBSERVED'
check('format-links','FMT','standards','PASS','Limited operational structure observation has no required mismatch.',[ref(R/'inputs/structure-stdout.json')])
check('installed-checker','FMT','standards','NOT_RUN','Actual personal Skill Creator checker remains outside selected local-input boundaries; this is a named unavailable observation, not a target format defect.',[ref(R/'environment.json')],False)
check('routed-workflow','WORKFLOW','workflow','PASS','Routed steps and terminal outcomes remain concrete; recovery fix now exercised.',[ref(R/'workflow-map.json'),ref(R/'trials/record-write-failure/result.json')])
check('authoring-instructions','INSTRUCTIONS','instructions','PASS','Previous metadata/checker contradiction removed; supported target fields preserved in the current guidance. Other essential routing/contracts unchanged.',[source('references/conversion-rules.md',18),ref(R/'ceremonial-review.json'),ref(R/'package-comparison.json')])
results=json.loads((R/'trials/results.json').read_text())['results']
for row in results:
    assert row['result']=='PASS'
    check('trial-'+row['case_id'],row['rule_id'],'behavior',row['result'],row['expected'],[ref(R/'trials'/row['case_id']/'result.json')])
check('trial-synthetic-import','INSTRUCTIONS','behavior','PASS','Realistic synthetic host import preserves supported metadata/resources and produces target-bound manual request; no imported script or validator execution.',[ref(R/'trials/synthetic-import/result.json')])
check('trial-record-write-failure','CUSTODY','behavior','PASS','Scoped post-write record save error retains PARTIAL with actual applied path and delivered digest, with no usable new baseline.',[ref(R/'trials/record-write-failure/result.json')])
for cid,why in [('cold-workflow','No independent/blind builder model workflow or routing classifier ran; delegation is prohibited. The synthetic import is a same-agent transparent walkthrough.'),('native-activation','Explicitly loading selected skill instructions does not exercise native implicit discovery/activation.'),('legacy-regression','Complete legacy schema-1/schema-2 positive/corrupt lineage campaign and companion validator relocation/consumption were not selected or executed.'),('platform-and-race','Alternate OS, absent dependencies, links/junctions, concurrent per-path races and all publication failure modes remain unperformed. The narrow record-save fault is separately exercised.')]:
    check(cid,'NATIVE','behavior','NOT_RUN',why,[ref(R/'environment.json')])
text(R/'checks.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in checks))
dims={}
for dim in ['standards','workflow','instructions','behavior']:
    group=[c for c in checks if c['dimension']==dim and c['required']]
    dims[dim]=dict(outcome='FAIL' if any(c['result']=='FAIL' for c in group) else 'INCOMPLETE' if any(c['result'] in ('NOT_RUN','ERROR') for c in group) else 'PASS',evaluated=sum(c['result'] in ('PASS','FAIL') for c in group),required=len(group),not_run=sum(c['result']=='NOT_RUN' for c in group))
save(R/'assessment.json',dict(schema_version='1',run_id=R.name,target_name='skill-builder',assessment_completed=True,overall_assessment='INCOMPLETE',dimensions=dims,package_digest=current['package_digest'],rule_set_digest=h(R/'rule-set.json'),enforcement='No new enforcement mechanisms proposed.'))
text(R/'enforcement-recommendations.md','# Enforcement recommendations\n\nNo new hooks, GitHub checks, CI workflows or DevForgeAI CLI controls are proposed. The revised input parsing and record-failure behavior are ordinary development custody safeguards; the observed executions do not confer protected authority. Preserve authoring scope, partial evidence, source drift checks and manual validator handoff.\n')

log='''# Exact command and effect evidence

The selected task prompt was read first. Reads were limited to the selected current builder, selected operational validator/specification and the explicitly linked prior assessment. No unrelated sibling outcomes, baseline evidence or memory were read. No target edits, installation, external writes or delegation occurred.

The newly selected operational validator SKILL.md was read. observe.py and reporting hashes were compared to the exact previously read snapshot; subsequent input-readback.json compares all relevant loaded references and confirms byte equality. The enhancement specification digest matches the prior selected specification. Directory enumeration preceded snapshot recursion.

Snapshot: python -B -X utf8 <selected-validator>/scripts/observe.py snapshot --source <operational-revalidation>/skill-builder --output <new-run>. It returned COMPLETE, no exclusions and 28 files. The complete snapshot output appeared in the terminal receipt; source-manifest.json preserves its full source manifest. No fabricated replay of this attempt was made.

The ten-case prior harness was copied into this fresh run, with only selected specification path and inherited documentation freshness description adapted before execution. It creates new cases and plans, pins source/rule records before results and does not read prior expected outcomes from sibling tasks. Command: python -B -X utf8 <run>/assessment_trials.py > <run>/inputs/trial-suite-stdout.txt. Outer shell yielded a session, then completed exit 0. Exact expanded helper commands, timestamps, stdout/stderr, exit/timeout and before/after manifests are in trials/<case>/attempt-*.json. All helper subprocesses have 120-second timeouts. All ten cases passed.

Additional command: python -B -X utf8 -c wrapper calling subprocess.run([sys.executable,'-B','-X','utf8',<run>/additional_trials.py], capture_output=True, timeout=120), preserving stdout/stderr in inputs/additional-stdout.txt and inputs/additional-stderr.txt. Wrapper exited 0. Additional case plans and fixtures existed before each first helper action. Synthetic import performs two real CLI actions with transparent host staging between them. The fault case uses begin CLI then direct publish API under unittest.mock.patch.object(authoring,'save') raising OSError only for authoring-record.json. Its API receipt records return data instead of inventing a shell exit code. The outer subprocess applies the 120-second ceiling to this API case.

Structure: python -B -X utf8 <selected-validator>/scripts/observe.py structure --source <run>/source > <run>/inputs/structure-stdout.json. Status OBSERVED, no required mismatches. Readback: python -B -X utf8 <selected-validator>/scripts/observe.py readback --source <operational-revalidation>/skill-builder --manifest <run>/source-manifest.json > <run>/inputs/readback-stdout.json. Status MATCH; final compound shell exited 0. These two individual exit codes were not separately persisted; their complete JSON observations are retained.

The current package was compared with the selected prior snapshot by exact manifest row changes and unified textual differences. Only authoring.py, custody.py, conversion-rules.md and package-manifest.json changed. custody.py removed an unused generic result formatter; source search/diff shows no remaining call sites. Builder delivery evidence was not selected and was not inferred from the observed package.

write_revalidation.py writes only this evidence run and expressly requested response.md, copies exact selected inputs, computes actual digests and reports prior findings. It rechecks original target, specification and operational validator inputs. The retained official documentation is the prior live retrieval, reused as snapshot_only; no new network access occurred in revalidation. Record-integrity checking runs only after all report references exist and is retained as a separate observation.
'''
text(R/'command-log.md',log)

table='\n'.join('| '+k+' | '+v['outcome']+' | '+str(v['evaluated'])+'/'+str(v['required'])+' | '+str(v['not_run'])+' |' for k,v in dims.items())
report=f'''# Linked skill-builder revalidation

Assessment completed: **true**. Overall assessment: **INCOMPLETE**. All three prior findings: **resolved within tested scope**. New findings: **none observed**. Proposed changes: **none**; builder readiness **NO_CHANGE**, review **not_needed**. NO_CHANGE does not mean acceptance or a complete PASS.

Target: `{TASK/'skill-builder'}`. Exact package digest: `{current['package_digest']}`. Prior package digest: `{old['package_digest']}`. Pinned rule-set digest: `{h(R/'rule-set.json')}`.

## Source preservation and comparison

The exact approved enhancement specification remains SHA-256 `43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14`. The current snapshot contains 28 files without exclusions; final source readback is **MATCH**. Target bytes were not changed. The current operational validator and its relevant references match the previously inspected operational bytes. See [origin](origin-record.json), [manifest](source-manifest.json), [source readback](inputs/readback-stdout.json) and [input identities](input-readback.json).

Exactly four package files differ from the prior snapshot: scripts/authoring.py, references/conversion-rules.md, scripts/custody.py and package-manifest.json. The custody change removes an unused generic result formatter; no changed caller depends on it. See [comparison](package-comparison.json) and [exact diff](inputs/package-diff.txt). No builder delivery records were selected, so this establishes observed snapshot identity rather than a separately verified generated/adopted delivery chain. History stays observed/unknown.

## Prior findings

| Prior issue | Status | Fresh observation |
|---|---|---|
| Malformed contract writes then loses authoring record | Resolved | known_issues:null rejects during begin, exit 2, before creating target. Separate injected post-write record failure retains PARTIAL, applied SKILL.md and exact delivered manifest; no usable publication. |
| Valid 64-character identity rejected | Resolved | Same boundary case now begins/publishes AUTHORED and preserves identity plus unrelated bytes. |
| Checker-gated supported metadata preservation | Resolved | Revised import guidance preserves supported compatibility and defers checker disagreements. Synthetic CSV-skill import preserved supported metadata, resource bytes and output contract, adapted only Claude-specific instructions/override, then published a target-bound manual request. |

[revalidation.json](revalidation.json) retains exact predecessor finding IDs and digest-bound evidence. Prior finding bytes remain unchanged under inputs/prior. [findings.json](findings.json) contains no new findings; no prior finding was rewritten as if it had never occurred.

## Fresh executed evidence

**12 bounded cases passed; 0 failed.** Ten original helper cases were rerun against the current snapshot. They cover portable creation/repeat edit; observed edit/conflict; outside-scope candidate rejection; source drift; 64-character identity; malformed-contract rejection; metadata/policy preservation; occupied initialization; adoption/next-edit origin; referenced-input drift. Two added cases exercised synthetic import and record-save failure after a real target write. No retries or timeouts occurred.

The import used a synthetic Claude CSV summarizer with compatibility, license, metadata, a provider model override, a Python helper and an explicit JSON output contract. The assessment agent followed the current import route, removed the provider override, translated Read wording, and preserved the supported fields and resources. No imported script, quality checker, test campaign or validator ran during that authoring segment. Afterwards the assessment harness inspected actual bytes and handoff bindings. This is a transparent same-agent host walkthrough, **not independent or blind model execution**.

The record-failure case scoped its injected OSError to authoring-record.json only. Target SKILL.md had already been written; the actual return and retained publication-failure record both show PARTIAL, applied_paths=[SKILL.md], and the correct delivered manifest. This verifies the specific added recovery path, not every possible filesystem failure.

See [original cases](trials/results.json), [synthetic import](trials/synthetic-import/result.json), [record-save failure](trials/record-write-failure/result.json), predeclared `trials/*/plan.json`, [original-case harness](assessment_trials.py), [additional harness](additional_trials.py) and [command log](command-log.md). All trial effects are in disposable project docs/plan descendants. Source and prior assessment bytes were not edited.

## Dimensions and retained limitations

| Dimension | Outcome | Evaluated/required | NOT_RUN |
|---|---|---|---|
{table}

The fifth descriptive dimension contains [no new enforcement mechanism proposals](enforcement-recommendations.md). [Checks](checks.jsonl) and [workflow map](workflow-map.json) preserve applicability and actual producer/consumer paths. The loaded structural observer passed its limited metadata/link checks; personal installed Skill Creator checking remains outside selected local-input scope. Its absence is not a package defect.

Native implicit activation and independent cold builder/routing behavior remain NOT_RUN. Complete legacy schema-1/schema-2 lineage regressions, companion validator relocation/packet consumption, alternate OS, unavailable dependency behavior, links/junctions and full concurrency/publication-fault coverage remain unperformed or outside this selected builder scope. The retained format source is the prior assessment's live retrieval, reused as snapshot_only; no fresh broad current-OpenAI compliance claim is made. Required unperformed coverage makes the overall result INCOMPLETE despite the resolved findings and all executed cases passing.

## Outcome

No additional builder revision is proposed from this bounded revalidation; therefore no new revision-spec.md is emitted. [handoff.json](handoff.json) records NO_CHANGE separately from assessment completeness. Further acceptance requires the applicable unperformed workflow/legacy/environment coverage under separate authority. This assessment does not establish native activation, installation, Rust qualification or framework acceptance.
'''
text(R/'validation-report.md',report)
save(R/'handoff.json',dict(schema_version='1',run_id=R.name,target_name='skill-builder',original_target_root=str(TASK/'skill-builder'),original_manifest=ref(R/'source-manifest.json'),origin=ref(R/'origin-record.json'),proposed_spec=None,findings=ref(R/'findings.json'),report=ref(R/'validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='not_needed',review_instruction=None,builder_readiness='NO_CHANGE',readiness_reasons=['All prior findings resolved at tested scope; no further change proposed.','NO_CHANGE is not overall assessment PASS; required coverage remains unperformed.'],baseline_kind=None,baseline_reference=None,adoption_required=False,adoption_capability='Not needed for no-change handoff; no custody claim established.',permitted_target_root=str(TASK/'skill-builder'),preservation_requirements=['Read-only assessment: all target and historical bytes preserved.'],target_package_digest=current['package_digest']))
response=f'''Fresh linked revalidation completed: **INCOMPLETE**, with **all three prior findings resolved** and **no new findings observed**.

- Original ten cases: **10 PASS**.
- Synthetic import and post-write record-failure cases: **2 PASS**.
- Target readback: **MATCH**; no target edits.
- Native activation, independent cold workflow execution and full legacy/environment coverage remain **NOT_RUN**.

Report: [validation-report.md]({(R/'validation-report.md').as_posix()})

Prior finding dispositions: [revalidation.json]({(R/'revalidation.json').as_posix()})

Evidence directory: [{R.name}]({R.as_posix()})

No additional revision proposed; handoff is **NO_CHANGE**, which does not imply acceptance. Package digest: `{current['package_digest']}`.
'''
text(TASK/'response.md',response)
print(json.dumps(dict(overall='INCOMPLETE',resolutions=[x['status'] for x in resolutions],cases_passed=12,package_digest=current['package_digest'],dimensions=dims,report=str(R/'validation-report.md')),indent=2))
