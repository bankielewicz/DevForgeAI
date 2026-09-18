import datetime, hashlib, importlib.util, json, pathlib, sys
R=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('observer',R/'inputs/validator/scripts/observe.py');o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
B={'schema_version':'1','run_id':R.name,'target_name':'skill-builder'}
def ref(p,**kw):return {'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),**kw}
def put(p,v):
    d=R/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_text(v if isinstance(v,str) else json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if (R/'snapshot-stdout.json').exists():(R/'snapshot-stdout.json').rename(R/'inputs/snapshot-stdout.json')
manifest=json.loads((R/'source-manifest.json').read_text());digest=manifest['package_digest']
anchor='| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require the three actual trials in the evaluation reference. |'
assert (R/'source/references/evidence-format.md').read_text().count(anchor)==1
fid,identity=o.finding_identity('SB-CONSISTENCY','references/evidence-format.md',anchor,0)
finding={'finding_id':fid,'rule_id':'SB-CONSISTENCY','identity':identity,'category':'instruction_issue','severity':'minor','subject_path':'references/evidence-format.md','locator':{'line_start':86,'line_end':86},'source_refs':[ref('inputs/specs/skill-builder-adoption-spec.md',source_id='skill-builder-adoption-spec',locator='9. Verification and acceptance cases')],'observation_refs':[ref('source/references/evidence-format.md',start_line=86,end_line=86),ref('source/references/evaluation.md',start_line=81,end_line=92)],'description':'The reporting-state table says enhancements require three actual trials, while the linked evaluation workflow enumerates four, including the explicit adoption/revision/revalidation/lineage family. This is a stale count, not evidence that the implemented fourth workflow is absent.','user_impact':'A maintainer using the summary can misstate complete enhancement coverage or overlook the adoption family. The linked detailed workflow and final retained verification mitigate this risk.','proposed_correction':'Replace the stale count with a link to all applicable independent forward trials in evaluation.md, preserving its four currently enumerated families and separate routing requirements.','preserved_requirements':['Independent task execution for substantive enhancements','All four existing forward-trial families','Required Python observations and actual readback','No authority or activation claims'],'verification_cases':['Review the revised table against the four existing detailed families.','Confirm adoption lineage cannot be omitted by reading only the completion summary.','Verify all unrelated package bytes remain unchanged except the intentionally rebound build manifest.'],'disposition':'proposed'}
put('findings.json',{**B,'findings':[finding]})
put('observations/ceremony-review.json',{**B,'passages':[{'subject_path':'references/evidence-format.md','excerpt':anchor,'classification':'ambiguous_requirement','context':'Independent forward-trial status table after adoption extension','intended_effect':'Prevent completion without required independent trials','disposition':'Replace stale cardinality with direct applicable-requirements reference','preserved_requirement':'All four trial families and routing remain required; no ritual trial count added','finding_id':fid},{'subject_path':'SKILL.md','excerpt':'Python, required artifacts/cases, changed-script checks, and required task trials cannot be skipped for a completed build.','classification':'useful_instruction','context':'Evaluate, deliver, and report','intended_effect':'Tie completion to performed checks','disposition':'Preserve; required evidence is actionable, not ceremony'},{'subject_path':'references/adoption.md','excerpt':'Snapshot immutability is a workflow convention; rehash every use.','classification':'useful_instruction','context':'Capture, evaluate, publish','intended_effect':'Detect corrupted observed origins without pretending filesystem enforcement','disposition':'Preserve'},{'subject_path':'assets/worker-task-template.md','excerpt':'This file is a task contract, not an installed agent profile or an enforced permission policy.','classification':'useful_instruction','context':'Worker handoff limitations','intended_effect':'Prevent authority/identity overclaims','disposition':'Preserve'}]})
stages=[
 ('select','SKILL.md:11-25','Explicit user operation and selected inputs','Current request, project root, source/spec/target','Resolve import, spec_build, adoption, regeneration or non-trigger; retain ambiguity before generation','Resolved identity or concrete missing decision','contract or adoption','Missing/competing inputs: gap; preserve known history','Usable scope or precise required decision'),
 ('contract','references/spec-build.md:7-71','One authoring operation selected','Raw selected inputs, source inventory, current authorization','Record digest-bound requirements, artifacts, capabilities and gaps','build-contract.json, spec-gaps.json where needed','candidate','Essential unavailable capability or contradiction: BLOCKED before candidate','Reviewable contract or retained gap report'),
 ('candidate','SKILL.md:41-53','Complete contract; revision origin verified if needed','Contract, conversion rules, worker requirements','Stage only needed Codex resources; preserve source domain meaning; execute authorized ordinary script fixtures','Staged package and preceding observations','evaluate','Retain partial work and concrete error; no completion claim','Candidate evidence only until delivery succeeds'),
 ('adoption','references/adoption.md:5-33','Explicit adoption instruction, reviewed origin, managed-path selection','Exact target/spec, selected history, partition and capture','Capture all permitted bytes; bind custody; recheck; adoption-plan then adoption-v1; publish/read back separate pointer','ADOPTED evaluated record and published schema-2 pointer; target unchanged','stop or separately authorized revision','SOURCE_CHANGED/INCOMPLETE/PUBLICATION_INCOMPLETE; preserve record, no dependent revision','Observed custody report; no quality or revision authorization inferred'),
 ('revision','references/regeneration.md:9-49; references/adoption.md:39-49','Authorized revision and verified successful generated or published adopted origin','B or A, complete C, staged N, contract','Ordered B/C/N plan; conflicts leave target unchanged; recheck before each ordinary mutation','Revision plan, actual delta, after snapshot','evaluate then publish','CONFLICT/PARTIAL retains unchanged origin; retry links failed attempt using actual C','Applied revision only after checks; concrete retained failure otherwise'),
 ('evaluate','references/evaluation.md:5-79','Prepared package, contract/provenance and exact cases','Installed checker; bound evaluator/profile; disjoint candidate/case/output roots','Run exact structural/profile/script checks, source readback and semantic review','Actual commands, streams, observed PASS/FAIL/ERROR and digests','publish or retain failure','Missing dependency/check, mismatch or unsafe output blocks completion; expected negatives remain negative observations','Qualified bounded development observations'),
 ('enhancement-trials','references/evaluation.md:81-100','Substantive builder change','Minimal raw disposable tasks, independent agents, final bound package','Run import, specification, regeneration and adoption-lineage trials plus separate routing','Executed task artifacts and failed/retry receipts','evaluate/publish','Unperformed required trial means incomplete enhancement verification','Actual task outcomes distinct from native activation'),
 ('publish','SKILL.md:61-69; references/regeneration.md:51-61','Successful candidate and actual delivered checks/readback','Generated N, actual delivered bytes, prior pointer where needed','Re-evaluate delivery; preserve generated baseline separate from retained edits; write provenance and new pointer; read back','Build/conversion report and published development evidence','terminal','No advancement on partial or failed checks/publication; retain failed records','Return package/evidence paths, actual dimensions and limits; stop at development source')]
steps=[]
for sid,entry,condition,inputs,action,outputs,nxt,failure,outcome in stages:
    steps.append({'step_id':sid,'entrypoint':entry,'entry_conditions':condition,'inputs':[inputs],'executor':'Codex task following linked instructions; named Python helpers emit observations only','action':action,'outputs':[outputs],'completion_evidence':outputs,'next_or_branch_targets':nxt,'failure_route':failure,'terminal_user_outcome':outcome})
put('workflow-map.json',{**B,'review_type':'Primary assessor semantic review; independent description classification is separate','steps':steps})
checks=[]
def check(cid,rid,dimension,result,reason,paths,required=True,app='applicable',method='semantic'):
    checks.append({**B,'check_id':cid,'rule_id':rid,'subject_path':'SKILL.md','method':method,'required':required,'applicability':app,'result':result,'reason':reason,'evidence':[ref(p) for p in paths],'dimension':dimension})
check('C01','SB-FORMAT','standards','PASS','46 supported structure observations pass; 41 local links checked; installed Skill Creator exits 0. No optional configuration is required.',['trials/structure/attempt-001.stdout.txt','trials/installed-checker/attempt-001.stdout.txt'],method='deterministic')
check('C02','SB-DISCLOSURE','standards','PASS','Entrypoint exposes operation selection, complete contract, conditional adoption/regeneration references, evaluation, delivery and boundaries; no unsupported link form found in loaded instruction/resource paths. Development source is valid separately from installed duplicates.',['source/SKILL.md','source/references/evaluation.md'])
check('C03','SB-WORKFLOW','workflow','PASS','Each operation maps to concrete inputs, outputs, branches, failure/recovery and terminal result. Published adoption is explicitly separate from target quality and revision authorization.',['workflow-map.json','source/references/adoption.md','source/references/regeneration.md'])
check('C04','SB-CUSTODY','workflow','PASS','All 36 current target rows equal release snapshot; 917 selected historical result/case/command/measured-byte reads match. This is observed enhancement history, not target generated/adopted provenance.',['observations/prior-byte-comparison.json','observations/prior-evidence-readback.json'],method='deterministic')
check('C05','SB-CONSISTENCY','instructions','FAIL','One stale summary count says three required forward trials; detailed workflow correctly contains four. Minor reporting contradiction; no absent adoption implementation inferred.',['source/references/evidence-format.md','source/references/evaluation.md','findings.json'])
check('C06','SB-AUTONOMY','instructions','PASS','Current authorization is reused; essential unknown decisions stop generation; no installation or native profile claims; actual MUST/checklists preserve useful safeguards.',['observations/ceremony-review.json','source/references/conversion-rules.md','source/assets/worker-task-template.md'])
check('C07','SB-BEHAVIOR','behavior','PASS','Reused seven final profile suites: 15 observations (11 PASS, four intentional FAIL), plus eight independent adoption-chain evaluator files / 19 PASS observations. All selected emitted case/candidate hashes were read back. No current rerun or broader behavioral proof inferred.',['observations/prior-evidence-readback.json'],method='historical_evidence_readback')
check('C08','SB-COLD','behavior','NOT_RUN','Host supports independent tasks, but this assessment expressly prohibits invoking skill-builder import/build/adoption/regeneration. Historical evidence and exploratory classification do not become fresh minimal-input execution.',['task-prompt.txt','trials/cold-task/plan.json'],method='behavioral')
check('C09','SB-NATIVE','behavior','NOT_RUN','Native implicit discovery was not exercised; explicit loading and independent description classification are not activation observations.',['task-prompt.txt'],required=False,method='behavioral')
check('C10','SB-MODEL','instructions','NOT_APPLICABLE','No model-specific API component is being added or invoked; no fixed model or API parameter requirement applies to this instruction orchestrator.',['source/SKILL.md'],required=False,app='not_applicable')
put('checks.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks))
dims={d:o.reduce_checks([c for c in checks if c['dimension']==d]) for d in o.DIMENSIONS}
put('assessment.json',{**B,'assessment_completed':True,'overall_assessment':'FAIL','dimensions':dims,'enforcement_recommendations':'guidance_only candidate; no installed controls','required_coverage':o.reduce_checks(checks),'freshness':'snapshot_only','review_type':'Primary assessor review; separate exploratory independent description classification; root independent readback pending outside this record'})
put('origin-record.json',{**B,'original_source_root':manifest['root'],'manifest':ref('source-manifest.json'),'specification':ref('inputs/specs/skill-builder-adoption-spec.md'),'additional_specifications':[ref('inputs/specs/skill-builder-enhancement-spec.md'),ref('inputs/specs/claude-to-codex-skill-import-spec.md')],'origin_kind':'existing_spec','history_kind':'observed','historical_origin':'unknown','prior_evidence':ref('inputs/prior/FINAL-RECEIPT.json'),'completeness':'complete','uncertainties':['Selected successful enhancement verification and exact release snapshot are verified; no successful generated or published adoption baseline for skill-builder itself was established.','Project inputs are explicit complementary layers: adoption extension plus predecessor preserved operations; no directory precedence was used.'],'source_readback_state':'NOT_RUN'})
put('enforcement-recommendations.md',f'''# Future enforcement recommendations

One guidance-only candidate is justified. No hook, CI, GitHub check, CLI, installation, or Rust control was implemented.

ENF-01 references {fid}. Destination: `guidance_only`. Trigger: editing builder completion/reporting requirements. Invariant: summary wording must preserve every applicable trial family in the detailed evaluation contract. Inputs: the proposed diff, `references/evaluation.md`, and selected approved requirement changes. Intended action: inspect the summary against detailed requirements; use a link instead of a duplicated count. Current evidence: `references/evidence-format.md:86` says three, while `references/evaluation.md:87-90` enumerates four. Failure behavior: retain the discrepancy as an unresolved editorial finding; do not silently drop a trial. Coverage limits: prose and reviewer attention do not enforce execution, chronology, consent or immutable evidence. Dependencies: ordinary document review, no unavailable hook event or future command. Future verification: a proposed omission of adoption lineage must be detected while all four families remain present in the detailed reference. Keep all substantive independent-trial safeguards.

The existing package already labels pointer publication, source immutability and worker isolation as ordinary workflow properties with limits. This bounded assessment establishes no additional mechanism defect requiring a framework design expansion.
''')
proposal=f'''---
id: SKILL-BUILDER-REVISION-{R.name}
skill_name: skill-builder
target: codex
status: proposed
---

# Proposed complete skill-builder revision specification

## Identity and review boundary

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`.
Observed package digest: `{digest}`. Exact reconstruction uses [source-manifest.json](source-manifest.json) and the retained [source](source/SKILL.md), not this prose. Existing requirements are the retained adoption, enhancement and importer specifications in `inputs/specs/`; they are selected complementary requirements, not directory-precedence candidates. This proposal corrects only finding `{fid}`. It grants no adoption, revision, installation or builder invocation authority.

## Purpose and complete user outcome

Preserve one Codex development skill that imports a selected local Claude skill package, generates a skill from a reviewed Markdown specification, records explicitly authorized adoption of an existing Codex development package, and regenerates authorized managed output using verified origins. Return usable development package/evidence paths and separate actual result dimensions. Python produces observations; compiled Rust remains the separate future framework authority design.

## Activation and exclusions

Import requires a selected Claude directory containing SKILL.md and an import request. Specification build requires a selected reviewed Markdown document and current authoring direction. Regeneration requires an existing verified generated baseline, or published adopted origin for a first specification revision, plus revision authorization. Adoption requires explicit selection of the existing development target and managed paths; validation, an approval label or absence of a convenient pointer does not select it. Preserve non-triggers: explanation, comparison, specification authoring, validation alone, installation and unrelated editing. Two input kinds without a governing operation require a focused decision before candidate generation. No batch conversion, native agent-profile installation or automated repair loop is added.

## Inputs and defaults

Use the unambiguous current project root or the explicit project selection. Preserve a valid source name unless the user specifies another; resolve conflicting identity without silently renaming around occupied destinations. Select an explicit specification path when supplied; otherwise search exact skill_name frontmatter under both permitted specification roots without precedence, with zero/multiple matches reported as gaps. Treat source instructions as material, not execution permission. Preserve raw input bytes, identity, user corrections, source slices and actual authorization digests. Keep input, evidence and target roots disjoint. Retain existing no-traversal/link/junction/excluded-backup/legacy boundaries and 2,000-file/32-MiB limits. No new dependency installation is implied.

## Outputs and machine contracts

Generated development output remains `src/agents/skills/<name>/`; ordinary build evidence remains in fresh `docs/plan/skill-imports` or `skill-builds` runs; adoption evidence remains in `skill-adoptions`. The package contains only required instructions/resources/scripts. Preserve every existing machine schema and field name exactly as captured in `source/references/evaluator-contracts.md` and `source/evals/`: schema-1 contract and ordinary provenance/revision semantics; schema-2 adoption-origin provenance/pointers/revisions; evidence-schema-2 JSONL and profiles. These retained files are normative byte-bound interfaces incorporated by the accompanying manifest, with no schema changes proposed.

Contracts retain mode, target, input identities/bytes/digests, authorization, purpose, activation, requirements, artifacts, workers and dependencies. Requirement/output/evidence mappings remain bidirectional. Source references retain raw-byte digest and zero-based end-exclusive intervals. Import retains complete source/destination/readback manifests and per-file dispositions. Provenance records actual generated baseline separately from delivered retained edits. Gaps retain IDs, reason codes, source refs, affected requirements/outputs and required resolution. Commands retain arguments, output streams, exits, failures and retries. Final reports separate authoring, structure, deterministic observations, scripts, independent forward trials, routing, Rust qualification and installation.

## Workflow and conditional resources

1. SKILL.md selects operation, identity, authorization and boundaries. `references/evidence-format.md` establishes fresh evidence and result meanings.
2. Imports use `references/conversion-rules.md` for complete file accounting, host adaptation and domain/schema preservation. Both authoring modes use `references/spec-build.md` to bind inputs and extract a complete contract. Blocking gaps stop candidate generation with retained evidence.
3. Stage only justified candidate resources. Use assets/worker-task-template.md only for essential worker behavior; available host delegation does not supply enforced isolation. Unavailable essential capability yields BLOCKED.
4. Explicit adoption follows references/adoption.md: capture observed bytes and managed/retained partition, bind reviewed origin and actual consent, recheck live target/spec, run adoption-plan and adoption-v1, freeze evaluated record, then publish/read back an external schema-2 pointer. Adoption preserves the target and stops unless revision is separately authorized.
5. Regeneration follows references/regeneration.md and adopted lineage extensions where applicable. Compare separate B/C/N/after snapshots using ordered collision/C=B/C=N/N=B/conflict rules. Identical occupied unowned paths still conflict. Preserve unrelated C-only files; absence differs from empty content. Recheck before writes and each affected mutation. On drift or write failure stop and retain actual PARTIAL delta; retry from the same successful origin and actual current C.
6. references/evaluation.md and evaluator-contracts.md govern actual structural/profile/script/task checks. Exact registered profiles and case shape remain unchanged. Keep final JSONL outside candidate root and preserve expectations for deliberately negative fixtures. Expected FAIL with matched exit 0 is not a positive behavior result.
7. Deliver only after required candidate checks, then evaluate/read back actual delivered bytes. Advance generated baseline/pointer only after successful checks and readback; keep generated N separate from retained user edits. Return assets/build-report-template.md or conversion-report-template.md results and concrete outstanding work. Stop at development source.

## Required editorial correction

In `references/evidence-format.md`, replace only the Independent forward trials state-table description with:

`| Independent forward trials | NOT_PERFORMED, PASSED, FAILED; builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements). |`

Preserve the existing code formatting around the three status names when writing the actual Markdown. The linked contract currently requires four families: import, specification build, regeneration, and adoption/revision/revalidation/later-generated lineage. Separate routing remains required. This changes the summary reference, not the number or scope of required executions. Rebind only the corresponding manifest artifact digest after the reviewed wording edit; do not modify evaluation logic, schemas, case expectations or historical evidence.

## Dependencies, side effects and recovery

Keep Python 3.10+, standard-library runner/graders and separately available PyYAML for the installed checker/resolver. Resolve the actual installed checker location. Host terminal/delegation capability and required isolation are checked before dependent work. Commands remain the currently implemented resolve-spec, input-record, revision-plan, adoption-plan and run_evaluation.py interfaces, with existing exits 0/1/2. There is no new executable.

Future execution writes only explicitly authorized development/evidence paths and preserves every unrelated file and failed attempt. No operational .agents/.claude/.codex/personal directories, hook/CI configuration, remote repositories or production data are selected. Interrupted work retains completed evidence and resumes only after input readback. No automatic rollback, immutable filesystem, package-wide atomicity, protected acceptance or native activation is claimed.

## Requirement register and file mapping

REV-001 (required editorial fix): remove the stale summary cardinality while preserving all current trial families and routing. File: references/evidence-format.md; finding above; verify by contextual review against evaluation.md.

REV-002 (required preservation): every existing behavior/interface/resource remains byte-identical except the REV-001 table wording and the intentional corresponding evals/build-manifest.json artifact digest. Files: all 36 paths in source-manifest.json; verify complete file-set/hash comparison and review exact two-file delta. No optional enhancements are selected.

REV-003 (required binding): keep the evaluator manifest coherent with delivered bytes; retain existing schema/profile/grader/test identities. File: evals/build-manifest.json. Verify manifest accounting and the existing required structural/deterministic checks. Historical receipts are not edited or relabeled.

## Acceptance cases

AC-01: read the revised reporting row alone and follow its link. Expected: all currently required independent families remain applicable, including adoption lineage, with no hardcoded three-trial summary.
AC-02: compare the original and revised detailed evaluation reference. Expected: byte-identical four-family contract and separate routing requirements; no weakening or new campaign requirement for this editorial change.
AC-03: compare every package path with the retained manifest. Expected: only the table wording and corresponding manifest binding differ; no additions/removals or changed scripts/tests/schemas/profiles.
AC-04: check the revised package using the installed structural checker and required explicit deterministic profile with retained exact case/input snapshots. Expected: real checks complete without mismatches; negative fixtures keep their existing expected meanings. No redundant new behavior campaign is required by this specification for a wording-only correction. If the future executor's governing workflow requires more checks, it must record applicability honestly before claiming completion.
AC-05: attempt to treat this proposal or enhancement receipt as revision authority or generated baseline during intake review. Expected: dependent execution remains blocked until a genuine baseline is selected or explicit adoption with reviewed origin/management is authorized and published; no target write occurs.

## Exceptions, decisions and handoff

No exception to review-before-repair or source preservation is approved. The editorial contract is complete and reviewable; execution readiness is BLOCKED because a successful generated/published adopted origin for skill-builder itself has not been verified and this task supplies no managed-path adoption authorization. Proposal review is pending. Required decisions: accept/reject REV-001; for any later builder-mediated execution, identify verified applicable baseline history or explicitly authorize adoption of an exact reviewed managed-path manifest while preserving known evidence, then separately authorize revision. Pending review alone is not the reason for BLOCKED. The resulting handoff must name this exact proposal path/digest, target digest and selected change set; changed bytes require fresh review/readback. Do not invoke skill-builder in this assessment.
'''
put('revision-spec.md',proposal)
put('handoff.json',{**B,'original_target_root':manifest['root'],'target_package_digest':digest,'original_manifest':ref('source-manifest.json'),'origin':ref('origin-record.json'),'proposed_spec':ref('revision-spec.md'),'findings':ref('findings.json'),'report':None,'selected_finding_ids':[],'deferred_finding_ids':[],'proposal_review_state':'pending','review_instruction':None,'builder_readiness':'BLOCKED','readiness_reasons':['No verified successful generated or published adoption baseline for skill-builder itself. Enhancement verification is not that baseline.','Explicit managed-path adoption authorization is absent; validation-only request preserves target bytes.','The complete editorial proposal is reviewable; pending review is tracked separately.'],'baseline_kind':None,'baseline_reference':None,'adoption_required':True,'adoption_capability':'available','managed_path_authorization':None,'permitted_target_root':manifest['root'],'preservation_requirements':['Do not edit target or existing evidence during validation.','Future change, if authorized, is restricted to REV-001 wording and corresponding manifest binding.','Retain all source, known history, user-owned paths and failed attempts.']})
put('validation-report.md',f'''# Skill-builder development assessment

Assessment completed: **yes**. Overall: **FAIL**, from one **minor instruction inconsistency**. This does not mean the adoption implementation or existing forward trials failed. Builder readiness: **BLOCKED**; proposal review: **pending**.

Run `{R.name}` assesses package `{digest}` against rule-set `{ref('rule-set.json')['sha256']}`. Primary assessor review used a separately built validator; this is not validator self-review. An independent agent supplied exploratory description classifications only. Root's final independent audit is separately owned.

## Origin and preservation

[Origin record](origin-record.json), [exact snapshot](source/SKILL.md), [manifest](source-manifest.json), [readback](source-after-manifest.json). All 36 permitted target files were captured, without exclusions. Current package rows exactly matched the retained enhancement-release snapshot. The selected adoption specification extends the explicitly selected predecessor enhancement/import specifications; no governing decision came from directory precedence. Existing enhancement receipts and their selected hashes were verified. They establish tested development enhancement history, **not** successful generated or adopted custody for skill-builder itself.

Official sources were reused from the completed validator build, with their actual hashes verified. Freshness is **snapshot_only**, captured 2026-09-12; no current-live compliance claim is made. Required portable format checks under that identified source snapshot passed for this package. Optional folders/fields, fixed headings and arbitrary word or worker counts were not imposed.

## Dimensions and coverage

| Dimension | Result | Required evaluated/total |
| --- | --- | --- |
| Standards | PASS | 2/2 |
| Workflow | PASS | 2/2 |
| Instructions | FAIL | 2/2 |
| Behavior | INCOMPLETE | 1/2 |
| Enforcement recommendations | One guidance-only candidate | Descriptive; no control installed |

Overall required coverage: **7/8**, with C08 NOT_RUN preserved under FAIL precedence. No unknown-applicability rows. Native activation is separately advisory NOT_RUN. Model/API-specific advice is NOT_APPLICABLE. See [checks](checks.jsonl), [assessment](assessment.json), [rules](rule-set.json), [workflow map](workflow-map.json) and [sources](sources.json).

## Finding

`{fid}` — **minor**, instruction issue. [evidence-format.md:86](source/references/evidence-format.md) says enhancements require “the three actual trials.” [evaluation.md:81-92](source/references/evaluation.md) lists four, including adoption lineage. The detailed workflow and retained verification cover the fourth family; the defect is a stale reporting summary. Correct the summary to link all applicable required trials, retaining their substance and routing. [Full finding](findings.json) and [contextual ceremony review](observations/ceremony-review.json) preserve exact excerpts and safeguards. Strong completion/readback instructions were otherwise useful, not ceremonial defects.

## Actual observations and limitations

The fresh structural observer returned exit 0: **46 observations**, **41 local links**, zero failures. The actual installed Skill Creator checker returned exit 0. Inputs and evaluator/checker bytes were retained before these executions, along with plans, commands, separate stdout/stderr and timestamps under [trials](trials/structure/plan.json).

The [prior-evidence audit](observations/prior-evidence-readback.json) freshly reverified **917 selected byte measurements**, including seven final deterministic suites (15 observations: 11 PASS and four deliberate expected FAIL) and eight independent adoption-chain evaluator files (19 PASS observations). Actual case files, result bytes, command receipts and immutable pre-evaluation candidate locators were checked. This was a readback of prior executions, not a new target/evaluator campaign. The retained legacy import/specification/regeneration and fault reports describe their own executions; this run did not independently rehash every underlying legacy/fault trial input and does not expand their claims.

Fresh minimal-input skill-builder workflow execution is **NOT_RUN** because the selected assessment explicitly forbids invoking its import/build/adoption/regeneration workflows. Host task tools exist. Historical trials and manual tracing do not become fresh execution. The independent description review is exploratory: its prompt was sent before an on-disk expected-label plan was retained, so it is not scored as a predeclared routing PASS. Raw prompt/response and this protocol limitation are retained separately. Native implicit activation, operational installation, Rust qualification, framework admission and production acceptance are **NOT_PERFORMED**.

This is a bounded instruction/workflow/selected-behavior assessment, not an exhaustive repository or security audit. No target repair, adoption, generation, installation, dependency installation or hook/CI/framework work occurred. No new target helper behavior defect was established; unnecessary campaign reruns were avoided.

## Review packet and next action

The [complete proposed specification](revision-spec.md) preserves all current operation contracts and proposes one wording correction plus its required manifest binding. No optional enhancement or finding is silently selected. [Handoff](handoff.json) is **BLOCKED**, with review **pending**: the missing material prerequisite is a verified applicable origin for revising skill-builder itself, or explicit authorized adoption of a reviewed managed-path set. The enhancement-complete label cannot supply either. Review can accept/reject the editorial proposal now; execution is a separate later authorized step. [Enforcement register](enforcement-recommendations.md) proposes guidance-only review without adding mechanisms.

Final source/specification/evaluator/guidance readback and record-integrity results are retained in the final receipt and command log. Readback applies to the original target, not only its snapshot.
''')
# Handoff report reference is added only after report bytes exist; origin/readback binding is finalized separately.
h=json.loads((R/'handoff.json').read_text());h['report']=ref('validation-report.md');put('handoff.json',h)
print(json.dumps({'finding_id':fid,'proposal_sha256':ref('revision-spec.md')['sha256'],'overall':'FAIL','behavior':'INCOMPLETE','readiness':'BLOCKED'}))
