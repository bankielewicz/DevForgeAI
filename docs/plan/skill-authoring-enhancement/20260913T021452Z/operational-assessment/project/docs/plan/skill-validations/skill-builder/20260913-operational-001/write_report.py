import datetime as dt
import hashlib
import json
from pathlib import Path

R=Path(__file__).parent.resolve()
B=R.parents[5]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p,**more): return dict(path=p.relative_to(R).as_posix(),sha256=sha(p),**more)
def save(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s): p.write_text(s,encoding='utf-8')
def source(path,line1,line2=None):
    return ref(R/path,locator={'line_start':line1,'line_end':line2 or line1})

manifest=json.loads((R/'source-manifest.json').read_text())
readback=json.loads((R/'inputs/readback-stdout.json').read_text())
save(R/'source-after-manifest.json',readback['manifest'])
assert manifest['package_digest']==readback['manifest']['package_digest']
assert sha(B/'enhancement-spec.md')=='43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14'
assert sha(B/'operational-validator/assets/rules-snapshot.json')==sha(R/'inputs/rules-fallback.json')
inputs=[]
for rel in ['SKILL.md','scripts/observe.py','references/origin.md','references/rules.md','references/trials.md','references/reporting.md','references/handoff.md','assets/revision-spec-template.md','assets/validation-report-template.md','assets/enforcement-register-template.md']:
    p=B/'operational-validator'/rel; d=R/'inputs/validator'/rel
    d.parent.mkdir(parents=True,exist_ok=True); d.write_bytes(p.read_bytes())
    inputs.append({'original_path':str(p),'retained':ref(d)})
save(R/'input-readback.json',{'schema_version':'1','specification_sha256':sha(B/'enhancement-spec.md'),'specification_match':True,'fallback_sha256':sha(R/'inputs/rules-fallback.json'),'fallback_match':True,'validator_inputs':inputs,'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
origin=dict(schema_version='1',run_id=R.name,target_name='skill-builder',original_source_root=str(B/'skill-builder'),manifest=ref(R/'source-manifest.json'),specification=ref(R/'inputs/enhancement-spec.md'),origin_kind='existing_spec',history_kind='observed',historical_origin='unknown',prior_evidence=None,completeness='complete',uncertainties=['No builder baseline or historical evidence was selected; do not infer authored/adopted custody for this assessment target.','Specification frontmatter says proposed; current assessment request explicitly treats it as approved applicable enhancement.'],source_readback_state='UNCHANGED')
save(R/'origin-record.json',origin)

spec=ref(R/'inputs/enhancement-spec.md',source_id='spec',locator='Sections 2-4')
findings=[]
def finding(rule,path,line,severity,category,description,impact,correction,cases):
    p=R/'source'/path; anchor=p.read_text(encoding='utf-8').splitlines()[line-1].strip()
    identity=[rule,'source/'+path,anchor,0]
    fid='F-'+hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    obs=[source('source/'+path,line)]
    for case in cases:
        obs.append(ref(R/'trials'/case/'result.json'))
    row=dict(finding_id=fid,rule_id=rule,category=category,severity=severity,subject_path='source/'+path,locator={'line_start':line,'line_end':line},identity=identity,source_refs=[spec],observation_refs=obs,description=description,user_impact=impact,proposed_correction=correction,preserved_requirements=['Authoring-only workflow','Explicit scope and ownership','Exact historical evidence','Validation/testing remain separate'],verification_cases=cases or ['Import a package with supported compatibility metadata; preserve it without running a checker.'],disposition='proposed')
    findings.append(row); return fid

f1=finding('CUSTODY','scripts/authoring.py',410,'major','workflow_bug','begin accepts known_issues:null although the bundled contract schema requires an array. publish writes SKILL.md, a baseline snapshot and delivered-manifest, then c[known_issues] + problems raises TypeError outside its retained-failure block. CLI returns state BLOCKED and exit 2 without authoring-record.json or publication-failure.json.','A malformed authoring input can leave applied package changes without the promised actual applied-path record and with an inaccurate BLOCKED terminal status. Retained before/candidate/baseline manifests exist; the failure is not total evidence loss.','Validate all contract field types before any target mutation; cover record construction/publication in retained failure handling. If a failure follows writes, preserve PARTIAL with actual applied paths and readback. Do not execute authored-skill quality tests in builder.',['malformed-contract'])
f2=finding('AB-009','scripts/authoring.py',252,'minor','resource_tool_issue','The authoring begin identity check rejects length >=64. The valid existing 64-character synthetic identity is rejected with exit 2. The initializer and current Agent Skills format permit 64.','Focused editing cannot preserve a valid boundary-length existing identity through the documented helper route.','Accept lengths 1 through 64 inclusively and align authoring, initializer, import guidance and resolver boundaries without silently renaming existing skills.',['name-64'])
findings[-1]['source_refs'].append(ref(R/'inputs/official-refresh.json',source_id='standard',locator='Agent Skills name field, retrieved source lines 83-91'))
f3=finding('INSTRUCTIONS','references/conversion-rules.md',18,'minor','instruction_issue','The active Other metadata conversion row conditions preservation on a required structural checker and directs compatibility requirements into instructions when that checker rejects compatibility. This conflicts with the authoring-only boundary and preservation of supported metadata. The selected current format explicitly supports compatibility. No actual import model trial was run; this is an instruction contradiction.','A builder following this import branch may discard supported machine-readable metadata because of a checker-specific restriction or seek a checker during authoring.','Preserve fields supported by the selected target specification, including compatibility. Treat checker disagreements as a later validator observation; remove the required-checker preservation condition while retaining actual compatibility constraints. ',[])
findings[-1]['source_refs'].append(ref(R/'inputs/official-refresh.json',source_id='standard',locator='Agent Skills frontmatter and compatibility fields'))
save(R/'findings.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-builder','findings':findings})

steps=[]
for ident,entry,conditions,action,outputs,next_,failure,terminal in [
 ('resolve','SKILL.md:11-24','Selected project, request and identity','Resolve destination; ask only material missing decisions; choose conversational/spec/import/edit/adopt route',['selected identity and scope'],'capture','Retain material ambiguity; do not assume conflicting history absent','Focused clarification or authoring route'),
 ('capture','references/authoring.md:3-13; scripts/authoring.py:240','Explicit target, raw inputs, contract and prior history if known','begin validates basic custody inputs, resolves origin, captures before and candidate',['contract.json','before/','candidate/','origin.json'],'stage','Capture-failure.json inside created run; errors before run require caller to retain stderr','Staged candidate or concrete intake failure'),
 ('stage','SKILL.md:26-32; references/scaffolding.md','Captured contract and candidate','Author focused changes; optionally initialize separate scaffold or update metadata',['candidate files'],'publish','Preserve unrelated bytes; material missing capability blocks','Concrete authored candidate'),
 ('publish','scripts/authoring.py:299-411; references/regeneration.md','Captured contract, B/C/N and permitted paths','Recheck inputs/current, plan conflicts, apply per-path writes and read back',['candidate/write-plan/delivered manifests','applied_paths','authoring-record.json'],'handoff','Normally PARTIAL/BLOCKED with retained record; malformed-contract case bypasses this promised exit','AUTHORED or retained partial/conflict'),
 ('handoff','scripts/authoring.py:413-435; references/validation-handoff.md','AUTHORED delivered bytes and record','Publish separate baseline and manual assessment request with exact digest',['authoring-baseline.json','validation-request.json','validator-request.md','publication-readback.json'],'stop','Retain publication-failure.json; do not reuse failed baseline','Package, changed paths, history, gaps and manual request; no validation invocation'),
 ('revise','references/regeneration.md; references/adoption.md','Later authorized edit and verified current history','Reuse untested authored baseline or verified legacy origin; preserve custody distinction',['fresh authoring run'],'capture','Conflicting/missing known history blocks; no automatic readoption','Fresh authorized edit or unresolved evidence')]:
    steps.append(dict(step_id=ident,entrypoint=entry,entry_conditions=conditions,inputs=['current request','selected package/specification','prior custody where applicable'],executor='Codex host plus named bundled Python helper',action=action,outputs=outputs,completion_evidence=outputs,next_targets=[next_],branch_targets=['spec_build','import','observed edit','authored edit','explicit adoption'] if ident=='resolve' else [],failure_route=failure,terminal_user_outcome=terminal))
save(R/'workflow-map.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-builder','steps':steps,'assessment_kind':'single assessment agent, not a cold builder workflow run'})

ceremony=[]
for path,line,intended in [('SKILL.md',8,'Keep quality work assigned to validator'),('SKILL.md',24,'Bound captures and reject unsafe boundaries'),('references/regeneration.md',9,'Preserve conflict and source-drift safeguards'),('references/conversion-rules.md',18,'Preserve target-compatible metadata')]:
    text=(R/'source'/path).read_text().splitlines()[line-1]
    ceremony.append(dict(subject_path='source/'+path,line=line,exact_excerpt=text,context='Routed authoring guidance',intended_effect=intended,classification='ambiguous_requirement' if line==18 else 'useful_instruction',disposition='Revise as finding '+f3 if line==18 else 'Preserve',observation=source('source/'+path,line)))
save(R/'ceremonial-review.json',{'schema_version':'1','passages':ceremony,'limitations':'Emphasis, MUST wording and checklists alone were not treated as defects.'})

checks=[]
def check(cid,rule,dim,result,reason,evidence,required=True,subject='source/SKILL.md'):
    checks.append(dict(schema_version='1',run_id=R.name,check_id=cid,rule_id=rule,subject_path=subject,method='behavioral' if dim=='behavior' else 'semantic' if dim in ('instructions','workflow') else 'deterministic',required=required,applicability='applicable',result=result,reason=reason,evidence=evidence,dimension=dim))
structure=json.loads((R/'inputs/structure-stdout.json').read_text())
check('format-and-links','FMT','standards','PASS','Operational observe structure completed with no required mismatches; actual package name agrees with original directory.',[ref(R/'inputs/structure-stdout.json')])
check('installed-checker','FMT','standards','NOT_RUN','Personal installed checker is outside selected local input boundaries; not a target defect and not promoted to mandatory format authority.',[ref(R/'environment.json')],False)
check('routed-workflow','WORKFLOW','workflow','PASS','Entry routing covers conversation, selected specification, imports, observed/known-history editing, adoption and manual handoff; input/output map retained.',[ref(R/'workflow-map.json')])
check('failure-record-workflow','CUSTODY','workflow','FAIL','Malformed contract can mutate target before terminal BLOCKED without authoring record.',[ref(R/'trials/malformed-contract/result.json'),source('source/scripts/authoring.py',410)])
check('instruction-preservation','INSTRUCTIONS','instructions','FAIL','Active import guidance conditions supported-metadata preservation on a structural checker contrary to authoring-only and supported-field preservation.',[source('source/references/conversion-rules.md',18),source('source/SKILL.md',8),ref(R/'inputs/official-refresh.json')])
check('instruction-design','INSTRUCTIONS','instructions','PASS','Purpose, routing, proportional clarification, resources, declared effects, current authority and manual stopping result are concrete; no fixed phase count or automatic delegation required.',[ref(R/'source/SKILL.md'),ref(R/'ceremonial-review.json')])
results=json.loads((R/'trials/results.json').read_text())['results']
for row in results:
    cid=row['case_id']; check('trial-'+cid,row['rule_id'],'behavior',row['result'],row['expected']+' See actual observations.',[ref(R/'trials'/cid/'result.json')],subject='source/scripts/authoring.py' if cid not in ('metadata','initialize') else 'source/scripts/'+('generate_openai_yaml.py' if cid=='metadata' else 'init_skill.py'))
for cid,reason in [('cold-workflow','Independent builder model execution for conversational clarification, destination asking, import and handoff was not run: this task expressly prohibits subagents; helper fixtures are separate observations.'),('native-activation','Native implicit skill discovery/activation was not exercised; explicit loading is not activation evidence.'),('legacy-complete-regressions','Legacy schema-1/schema-2 custody readers were inspected; full positive/corrupt lineage regression campaign was not executed. Companion validator relocation and consumption were outside this selected-builder assessment.'),('interruption-and-platform','Concurrent per-path fault injection, post-write publication errors, link/junction trials, alternate OS, and absent-PyYAML execution were not exercised.')]:
    check(cid,'NATIVE','behavior','NOT_RUN',reason,[ref(R/'environment.json')])
write(R/'checks.jsonl',''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in checks))
dimensions={}
for dim in ['standards','workflow','instructions','behavior']:
    rows=[c for c in checks if c['dimension']==dim and c['required']]
    outcome='FAIL' if any(x['result']=='FAIL' for x in rows) else 'INCOMPLETE' if any(x['result'] in ('NOT_RUN','ERROR') for x in rows) else 'PASS'
    dimensions[dim]={'outcome':outcome,'evaluated':sum(x['result'] in ('PASS','FAIL') for x in rows),'required':len(rows),'not_run':sum(x['result']=='NOT_RUN' for x in rows)}
save(R/'assessment.json',{'schema_version':'1','run_id':R.name,'target_name':'skill-builder','assessment_completed':True,'overall_assessment':'FAIL','dimensions':dimensions,'enforcement':'No new framework enforcement candidates; proposed ordinary helper/input corrections only.','package_digest':manifest['package_digest'],'rule_set_digest':sha(R/'rule-set.json')})

rows=[]
for ident in range(1,15):
    rid=f'AB-{ident:03d}'
    state='Static support; native execution unperformed'
    evidence='source/SKILL.md and routed references'
    if ident==6: state='Initializer/occupied helper case PASS; generated workflow unperformed'; evidence='trials/initialize/'
    if ident==8: state='Metadata helper case PASS; import guidance contradiction remains'; evidence='trials/metadata/; finding '+f3
    if ident==9: state='FAIL: existing 64-character identity'; evidence='trials/name-64/'
    if ident in (4,5,13): state='Observed edit, retention and divergent conflict helper cases PASS'; evidence='trials/observed-conflict/'
    if ident==14: state='Normal handoff PASS; malformed failure recording FAIL'; evidence='trials/create-repeat/; trials/malformed-contract/'
    rows.append(f'| {rid} | {state} | {evidence} |')
write(R/'applicability.md','# Applicable builder requirements\n\nCompanion validator implementation, relocation acceptance and stale-packet consumption are outside this selected builder. Applicable builder duties in specification sections 3-4 remain assessed. Raw conversational model behavior and native activation are unperformed even where static guidance and helpers support a requirement.\n\n| Requirement | Observation | Evidence |\n|---|---|---|\n'+'\n'.join(rows)+'\n\nSection 3 records and manual handoff: directly exercised in normal runs; malformed contract failure remains. Section 4: no grader/evaluator imports or calls found in active authoring helpers; legacy readers retain COMPLETE predicates. Full historical rejection regression campaign and relocated validator implementation are unperformed/outside scope.\n')

write(R/'enforcement-recommendations.md','# Enforcement recommendations\n\nNo new hook, CI, GitHub check or devforgeai_cli candidate is justified by this bounded assessment. The confirmed custody failure calls for ordinary pre-write contract parsing and durable partial-operation records in the existing helper. These editable Python checks establish development observations, not protected framework authority. Preserve current scope, readback, conflict and explicit review guidance. Native isolation and Rust qualification remain unassessed.\n')

proposal='''---
id: OPERATIONAL-BUILDER-REVISION-20260913-001
skill_name: skill-builder
target: codex
status: proposed
---

# Complete proposed builder contract

This proposal applies only to the observed builder development package selected by this assessment. It is reviewable remediation, not permission to write or install. The supplied enhancement specification remains the complete approved two-package design; this contract restates the selected builder responsibilities and proposes three fixes without enlarging its scope.

## Purpose, activation and exclusions

Author one Codex development skill from conversational requirements, a selected Markdown specification, a Claude source package or a requested edit. Support explicit custody adoption separately. A clear current request authorizes proportionate creation/editing; preserve user-selected review boundaries. Do not trigger for standalone testing, validation, installation or standalone specification writing. Never invoke validator automatically or repair its findings without a later request.

## Inputs and defaults

Resolve the selected project, exact identity, operation and destination. Ask once for missing destination and show the resolved project/src/agents/skills parent recommendation and final skill directory; an already supplied location answers that question. Accept another development directory including paths with spaces. Discover routine facts and ask only consequential missing decisions. Existing valid identities are preserved, including names of exactly 64 characters. New identities use 1-64 lowercase letters/digits with single separating hyphens; resolve collisions explicitly.

Capture raw requirements, references and actual authorization before staging. Use authoring-contract-v1 with project_root, target_root, target_name, operation, run_id, authorization, history_review, change_paths, requirements, capabilities, expected_outputs, side_effects, inputs and known_issues; retain prior/legacy_root/retry_of where applicable. Require field types and reference shapes from the bundled contract schema before mutation, including known_issues as an array of strings. JSON rejects duplicate keys and nonfinite values. These checks interpret write-custody data, not authored-skill quality. Known contradictory or missing history is unresolved, not absence.

## Outputs and schemas

Produce contract and input captures, before/candidate/delivered manifests, B/C/N write plan, actual applied paths, managed and retained ownership, and an authoring-v1 record. Successful authoring uses AUTHORED; incomplete operations use PARTIAL or BLOCKED according to actual applied effects. Keep validation/testing NOT_PERFORMED unless an explicit separate result binds the exact delivered bytes. Publish authoring-baseline-v1 only after successful delivery and publication readback. Old schema-1/schema-2 COMPLETE records keep historical meanings and original bytes.

Return validation-request-v1 containing schema/record kind, originating run, project and actual target/name, target manifest/package digest, authoring record/specification references, changed paths, known issues, capabilities, outputs and side effects. Also return a human-readable validator invocation with exact request path/digest. This proposes assessment and grants no credentials, network, installation or external-write authority. Return destination, changes, history, unresolved issues and handoff to the user.

## Workflow and routing

1. Resolve operation, scope and development destination through SKILL.md and references/authoring.md. Selected specifications additionally use spec-build.md; Claude imports use conversion-rules.md; existing packages use regeneration.md; explicit adoption uses adoption.md.
2. Record the contract and verify all input shapes, safe roots and selected history before target writes. Begin a fresh run under the selected project docs/plan, disjoint from target and input roots. Capture exact bytes and observed history when no known baseline exists. Observation does not adopt or manage unrelated paths.
3. Stage changes in candidate. Use bundled initializer only for a fresh staging destination and refuse occupied locations. Use bundled UI helper or focused edits, preserving unrelated interface/policy/dependency fields. Resource directories, examples, scripts, references and assets serve concrete requirements; remove unused scaffold placeholders. Do not create automatic README/changelog/install/test trees.
4. Write clear purpose, activation, inputs/outputs, dependencies, effects, recovery and constraints. Keep essential routing in SKILL.md; put substantial conditional detail in references. Preserve useful existing structure, identities, supported metadata and output/domain contracts. Import decisions depend on supported target format, never on a checker restriction. Preserve supported compatibility metadata. Do not execute a checker, grader, generated helper, sample task, campaign or validator during authoring.
5. Resolve B/C/N for selected managed paths. Reject unowned collisions and divergent managed changes. Preserve unrelated current bytes. Recheck source inputs and captured target before first write and each changed path before mutation. Read back actual delivery and retain real applied deltas.
6. Retain all interrupted attempts and record-construction/publication failures. A malformed pre-write input blocks without target mutation. Any failure after applied writes produces durable PARTIAL evidence with actual paths and after observation; never label a changed target merely BLOCKED or claim rollback. Do not advance a failed baseline. Recovery requires a fresh linked run and the last verified successful baseline.
7. Publish successful authoring record, baseline, manual request and publication readback; return them and stop. Further authorized editing may use the untested authoring baseline. Explicit adoption remains custody-only and records adopted origin for later edits. Validator absence does not stop otherwise complete authoring.

## Dependencies and side effects

Use Python 3.10+ for bundled custody/scaffolding; PyYAML is needed by specification lookup and metadata parsing. No personal skill-creator path dependency or dependency installation is introduced. Missing helper dependencies permit ordinary authoring tools where custody can still be honored; otherwise retain a concrete blocker. Operational .agents/.claude/.codex, installed/personal skills, hooks, CI, external systems and Rust implementation are excluded. Reject traversal, links/junctions and special files; apply the existing bounded 2000-file/32-MiB capture ceiling with disclosed exclusions. These are ordinary safeguards, not OS-enforced isolation or framework authority.

## Required fixes and acceptance

R-01 (mandatory): validate the contract before mutation and retain honest post-write failure evidence. A fixture with known_issues:null must be rejected before creating/changing target bytes; wrong types in other used fields must also fail safely. Inject a record/publication failure after a real applied path: preserve PARTIAL, exact applied paths/readback, and no usable new baseline. Retest ordinary creation, observed editing, conflict/drift and adoption.

R-02 (mandatory): preserve valid 64-character identity through begin/publish and align routed naming guidance. Editing a 64-character existing identity succeeds without rename; 63 and 64 are permitted, 65 remains rejected. Initializer and authoring must agree.

R-03 (mandatory): remove checker-gated metadata preservation from import instructions. An import with supported compatibility metadata preserves that field and its meaning without invoking a structural checker. Unsupported actual host fields require an explicit compatibility decision, not fabricated universal rules.

Retain all original AB-001 through AB-014 and applicable section 3-4 responsibilities. Validator owns execution of these quality and behavioral acceptance cases. Native activation, cold independent workflow execution, structural checks and helper cases are reported separately. The companion validator implementation is not part of this proposed builder patch.

## File mapping, preservation and decisions

scripts/authoring.py and schemas/authoring-contract.schema.json implement R-01/R-02 custody interpretation; preserve existing record versions. references/conversion-rules.md implements R-02/R-03 naming/metadata guidance. Update any directly inconsistent authoring/evidence/scaffolding references and package identity manifest only as required by these fixes. Preserve unrelated package files, licenses, metadata/domain contracts and every historical evidence byte. Test ownership remains with validator. No optional enhancements are selected.

Review must select these finding corrections and authorize the exact development target and managed paths. No verified target authoring/generated/adopted baseline was supplied to this isolated assessment. The loaded operational validator's handoff requires a verified baseline or explicitly authorized supported adoption before builder-ready execution; therefore readiness is BLOCKED while the proposal remains pending review. Do not silently invent history. A later explicit observed-edit request under an enhanced builder is a separate authorization/workflow decision.
'''
proposal += '\nObserved package digest: `'+manifest['package_digest']+'`. Origin/specification: `inputs/enhancement-spec.md`, SHA-256 `'+sha(R/'inputs/enhancement-spec.md')+'`.\n\nFinding bindings: '+', '.join('`'+f+'`' for f in [f1,f2,f3])+'.\n'
write(R/'revision-spec.md',proposal)

coverage='\n'.join('| '+d+' | '+x['outcome']+' | '+str(x['evaluated'])+'/'+str(x['required'])+' | '+str(x['not_run'])+' |' for d,x in dimensions.items())
report=f'''# Skill builder operational assessment

Assessment completed: **true**. Overall: **FAIL**. Readiness: **BLOCKED**; proposal review: **pending**. This is one assessment agent using the selected operational validator snapshot. It is not a native builder activation or an independently executed builder model workflow, and the validator is not assessing itself.

Target: `{B/'skill-builder'}`. Package digest: `{manifest['package_digest']}`. Rule-set digest: `{sha(R/'rule-set.json')}`.

## Preserved origin and evidence

The selected enhancement specification matched SHA-256 `43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14`. Current request treats it as approved despite its retained proposed frontmatter. The snapshot captured {len(manifest['files'])} files with no exclusions. Final source readback is **MATCH**; original target bytes were not edited. History is observed/unknown because no baseline evidence was selected. Source and rule inputs were rehashed.

See [origin](origin-record.json), [source manifest](source-manifest.json), [exact source](source/), [readback](inputs/readback-stdout.json), [sources](sources.json), [pinned rules](rule-set.json) and [input readback](input-readback.json). A live read-only Agent Skills format refresh is retained. OpenAI Build skills retrieval was reachable, but its Markdown transport failed; no current broad OpenAI compliance claim is made. The operational fallback was preserved separately; its historic source locators were not treated as freshly read sources.

## Dimensions and required coverage

| Dimension | Outcome | Evaluated/required | NOT_RUN |
|---|---|---|---|
{coverage}

Enforcement is a fifth descriptive dimension: no new hook/CLI/CI mechanism is proposed. Existing guidance and ordinary input parsing/readback safeguards remain appropriate. See [enforcement recommendations](enforcement-recommendations.md).

## Findings

1. **Major — malformed input leaves writes without authoring record.** `scripts/authoring.py:244-245` checks field presence but not all types. With `known_issues:null`, begin exits 0; publish writes the synthetic target SKILL.md and baseline, then line 410 raises TypeError. It exits 2 with BLOCKED, no authoring-record.json and no publication-failure.json. Before/candidate/baseline/delivered evidence still exists. Fix pre-write parsing and retained post-write failure reporting. Finding `{f1}`; [case](trials/malformed-contract/result.json), [stderr](trials/malformed-contract/attempt-002.stderr.txt), [after effect manifest](trials/malformed-contract/attempt-002.after.json).

2. **Minor — valid 64-character identity rejected.** `scripts/authoring.py:252` uses `>= 64`; begin exits 2 on a valid existing identity. The initializer permits 64 and the current [Agent Skills name contract](https://agentskills.io/specification#name-field) permits 1–64 characters. Fix the inclusive boundary without renaming existing skills. Finding `{f2}`; [case](trials/name-64/result.json), [stderr](trials/name-64/attempt-001.stderr.txt).

3. **Minor — import preservation still depends on a structural checker.** `references/conversion-rules.md:18` tells the host to condition preservation on a required checker and move compatibility into prose if rejected. This conflicts with the package's authoring-only entrypoint and preservation requirement; the [format supports compatibility](https://agentskills.io/specification#compatibility-field). This is an instruction finding, not an observed model deleting metadata. Finding `{f3}`; [exact source](source/references/conversion-rules.md), [contextual review](ceremonial-review.json).

Stable machine findings and digest-bound locators are in [findings.json](findings.json). All three remain proposed, not approved or executed changes.

## Trials, positive evidence and limitations

Ten disposable cases ran: **8 PASS, 2 FAIL**, with command-level stdout/stderr, exit codes, timestamps and before/after manifests retained. No timeouts or retries occurred. Passing cases cover creation in a path with spaces and a second untested edit; observed first edit and divergent conflict; rejection of outside-scope candidate changes; source drift; metadata/policy/dependency preservation; occupied initializer destination; explicit adoption followed by adopted-origin editing; referenced-input drift. Normal successful runs retain NOT_PERFORMED validation/testing and publish exact request references. A source-drift case returned PARTIAL with no applied paths because the external fixture changed; the captured effects make the distinction visible.

See [trial results](trials/results.json), individual pre-execution `trials/*/plan.json`, [harness](assessment_trials.py), [command log](command-log.md), [workflow map](workflow-map.json), [applicability](applicability.md) and [checks](checks.jsonl). Fixtures are synthetic; package and operational validator remained read-only. Test-created instruction files are not examples authored by the builder model.

Structural observation passed its limited metadata/link checks. The personal installed checker was outside the selected local-input scope and was not run. Manual inspection found routed resources and concrete terminal outcomes except the cited failure. No grader import, quality-test subprocess or automatic validator invocation was found in the active authoring path. This static observation is not a full runtime trace for all future model choices.

Native implicit activation, independent cold workflow execution, full legacy schema-1/schema-2 lineage rejection regressions, interleaved per-path failures, publication fault injection, link/junction fixtures, alternate OS and missing-dependency runs were **NOT_RUN**. No subagents were authorized, so description-based independent classification was not substituted. Companion validator changes, its stale-packet detection and test relocation are outside the selected-builder assessment. Neither helper success nor report integrity establishes framework acceptance, native execution, Rust qualification or installation.

The harness records fixture identities and predeclared expectations before the first behavioral command. Some branch-specific fixture details are generated by the retained case code and appear in command-before manifests. All shell commands use 120-second subprocess timeouts. The wrapper command initially yielded a live session and completed normally. Early read commands are recorded in the log with their coverage; terminal transcript remains their exact raw output source.

## Proposed next action

[revision-spec.md](revision-spec.md) is the full proposed builder contract and mandatory correction scope. [handoff.json](handoff.json) binds it to the observed target. Review the three proposed findings and select the exact authorized development paths plus a valid baseline/custody prerequisite. The operational validator requires this prerequisite for an executable repair handoff; no verified baseline was supplied. Pending review and that missing execution prerequisite remain separate. No repair, builder invocation or installation was performed.
'''
write(R/'validation-report.md',report)

log='''# Command and operation log

All local commands ran in PowerShell from C:/Projects/DevForgeAI. Inspection stayed within the selected assessment prompt, builder package, operational validator snapshot and enhancement specification. No sibling results/plans or memory files were read. No target/package mutation, dependency installation, delegation, native activation or external write occurred.

Initial read sequence: Get-Content prompt.txt; operational-validator/SKILL.md; enhancement-spec.md; operational-validator references origin/rules/trials/reporting/handoff; observe.py; rules-snapshot.json. Directory inventory used Get-ChildItem at the builder root followed by rg --files over that selected package. Subsequent scoped reads covered builder SKILL.md, all routed references, assets, authoring.py, initializer/metadata scripts, build_evidence.py, custody.py and contract schema. Large combined initial outputs were truncated by the display; focused subsequent reads covered the relevant workflow, helper and evidence interfaces. These commands emitted terminal output and did not modify source files.

Snapshot command: python -B -X utf8 <operational-validator>/scripts/observe.py snapshot --source <assessment>/skill-builder --output <run>. Exit was observed through resulting COMPLETE JSON and complete manifest; the original compound shell command did not separately persist each subcommand exit. stdout was first redirected to project/snapshot-stdout.json, then moved into this run; no synthetic test target was outside docs/plan. It is retained at inputs/snapshot-stdout.json. Python availability probe printed 3.10.11, PyYAML 6.0.2 and Windows 10.0.26200.

Structure command: python -B -X utf8 <operational-validator>/scripts/observe.py structure --source <run>/source. stdout is inputs/structure-stdout.json, status OBSERVED; initial compound shell command did not persist an isolated exit code. This raw observation preceded rule-set pinning; the package result and all behavioral results were reduced under the subsequently recorded pinned rules.

Read-only web operations: open https://developers.openai.com/codex/skills/ redirected to https://learn.chatgpt.com/docs/build-skills; open https://learn.chatgpt.com/docs/build-skills.md failed with unsupported content-type; open https://agentskills.io/specification succeeded. Retrieved representation and transport error are retained in inputs/official-refresh.json. No installation or external write followed.

Behavioral command: python -B -X utf8 <run>/assessment_trials.py. It first saved environment, source/rule records and predeclared case plans, then invoked bounded subprocess helpers. The outer session exited 0 after emitting all results; this reflects harness completion, not all cases passing. Exact expanded commands, cwd, UTC start/end, stdout/stderr, timeout/exit and before/after file manifests are in trials/<case>/attempt-*.json. Case commands are independent attempts/steps, not silent retries. Plans and captured harness define direct synthetic staging edits between helper invocations.

Readback command: python -B -X utf8 <operational-validator>/scripts/observe.py readback --source <assessment>/skill-builder --manifest <run>/source-manifest.json. Shell exited 0 and complete stdout is inputs/readback-stdout.json. Extracted manifest is source-after-manifest.json. Specification and fallback hashes were rechecked using actual original bytes in write_report.py. That reporting script only writes this evidence run and the expressly requested response.md.

Report artifacts were generated by write_report.py from actual captured files. Machine record validation is performed after all references exist; each attempt is retained separately. Its integrity output does not assess semantic correctness, historical truth or complete quality coverage.
'''
write(R/'command-log.md',log)

handoff=dict(schema_version='1',run_id=R.name,target_name='skill-builder',original_target_root=str(B/'skill-builder'),original_manifest=ref(R/'source-manifest.json'),origin=ref(R/'origin-record.json'),proposed_spec=ref(R/'revision-spec.md'),findings=ref(R/'findings.json'),report=ref(R/'validation-report.md'),selected_finding_ids=[],deferred_finding_ids=[],proposal_review_state='pending',review_instruction=None,builder_readiness='BLOCKED',readiness_reasons=['No verified target baseline or explicitly authorized adoption/management scope was supplied for repair under this operational validator contract.','Assessment only; findings are proposed and target remained unchanged.'],baseline_kind=None,baseline_reference=None,adoption_required=True,adoption_capability='Selected development builder contains new explicit authoring adoption; legacy/operational repair prerequisite not independently established.',permitted_target_root=str(B/'skill-builder'),preservation_requirements=['All target bytes remain read-only until a separate exact authorization.','Preserve historical records, failed attempts, valid identities, unrelated files and supported metadata.','No operational installation or automatic validator/builder invocation.'],target_package_digest=manifest['package_digest'])
save(R/'handoff.json',handoff)

response=f'''Assessment completed: **FAIL**. Target readback: **MATCH**; no target changes.

- **Major:** `authoring.py` accepts `known_issues:null`, writes target bytes, then returns BLOCKED without an authoring record. Reproduced in a disposable fixture.
- **Minor:** existing valid 64-character skill identities are rejected (`>= 64`).
- **Minor:** import guidance still conditions supported metadata preservation on a structural checker.

Bounded helper trials: **8 passed, 2 failed**. Native activation, independent model execution and full historical regressions remain **NOT_RUN**. Structural observation passed its limited checks.

Report: [{R/'validation-report.md'}]({(R/'validation-report.md').as_posix()})

Evidence: [{R}]({R.as_posix()})

Proposed revision: [{R/'revision-spec.md'}]({(R/'revision-spec.md').as_posix()})

Handoff: [{R/'handoff.json'}]({(R/'handoff.json').as_posix()}) — proposal pending review; executable repair readiness BLOCKED because this isolated input selection supplied no verified target baseline or authorized custody prerequisite.
'''
write(B/'response.md',response)
print(json.dumps({'package_digest':manifest['package_digest'],'dimensions':dimensions,'findings':[f['finding_id'] for f in findings],'report':str(R/'validation-report.md')},indent=2))
