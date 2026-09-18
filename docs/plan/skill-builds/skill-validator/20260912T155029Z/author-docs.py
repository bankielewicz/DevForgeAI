import hashlib, json, re
from pathlib import Path
from bootstrap import ROOT, PROJECT, write, digest

SPEC=(ROOT/'inputs/skill-validator-spec.md').read_text(encoding='utf-8')
C=ROOT/'candidate'
def put(path, text):
    p=C/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text.strip()+'\n',encoding='utf-8')
def section(a,b): return SPEC.split('## '+a+'. ',1)[1].split('## '+b+'. ',1)[0].split('\n',1)[1].strip()
front=re.search(r'Required generated frontmatter:\n\n```yaml\n(.*?)\n```',SPEC,re.S)[1]
put('SKILL.md','---\n'+front+'\n---\n\n'+'''# Skill Validator

Assess one explicitly selected Codex development skill. Preserve its bytes and exact origin, inspect its workflow, execute authorized disposable trials, and return findings plus a proposed full revision specification for review. This is a development assessment: Python observations and model conclusions are not DevForgeAI admission, enforcement or mutation authority. Compiled Rust remains the separate future enforcement design.

## Intake and boundaries

Use the explicit target and unambiguous project root. A name must resolve uniquely within user-selected discovery locations; relevant duplicates are an input decision, not permission to audit the repository. Resolve bundled resources relative to this loaded package, and work products relative to the project. Do not install, repair, adopt, configure hooks/CI, invoke skill-builder, or operate on production data during validation.

Create a fresh UTC run directory at `docs/plan/skill-validations/<target-name>/<run-id>/`, disjoint from target, source specifications and this package. Establish boundaries before writes. Enumerate directories before recursion; omit backup directories and `devforgeai_cli` before reading/hashing. Do not follow links/junctions; reject escaping roots, traversal and special files. The default capture ceiling is 2,000 files and 32 MiB. An omission is disclosed; material omissions prevent complete restoration or assessment. Never silently truncate or raise a ceiling.

Record OS, shell, Python/PyYAML availability, installed checker identity, host task capability, user requirements and authorized effects. Python 3.10+ and PyYAML are the helper defaults; check without installation. If unavailable, continue manual independent checks and mark affected observations NOT_RUN. No future CLI is required.

## Establish the origin before assessment

Read [origin.md](references/origin.md). An explicit specification path governs; missing explicit input or ambiguous provenance/lookup remains unresolved while independent package checks continue. Otherwise verify matching provenance, then perform bounded exact `skill_name` lookup in `docs/plan` and `docs/design/specs` without precedence. Only actual absence permits reconstructing [origin-spec-template.md](assets/origin-spec-template.md). Capture existing specification bytes under `inputs/`.

Inspect [observe.py](scripts/observe.py) before executing its documented interface. `snapshot --source <target> --output <new-dir>` creates `<new-dir>/source/` and `<new-dir>/source-manifest.json`; choose the fresh run directory itself as the new-dir, with its parent existing, or capture to a disjoint fresh staging directory and transfer the exact files with verified readback. Do not precreate the snapshot output. Snapshot is the only helper command that writes. Retain partial output after errors and never treat it as complete.

Record origin kind, honest history, original absolute target, source manifest, specification reference, exclusions and uncertainties in `origin-record.json`. An observed origin is not an adopted/generated baseline; prose is not an exact backup.

## Select rules and inspect

Read [rules.md](references/rules.md); use [rules-snapshot.json](assets/rules-snapshot.json) as the dated fallback. Refresh official guidance through available read-only tools when possible, retain the retrieved content and source identity, and pin `sources.json` plus `rule-set.json` before results. Distinguish mandatory format requirements, official recommendations and project policies. Model/API advice is conditional. Unsupported assertions remain unresolved; a checker restriction is not automatically a universal format rule.

Plan applicability and required/advisory classification before checks. Run `structure --source <run>/source` and the actual installed Skill Creator checker when available, recording their limited coverage separately. Inspect unsupported links/anchors manually. Trace each real workflow step from its cited entrypoint, inputs and executor to outputs, next branches, completion evidence, failure/recovery route and terminal user result in `workflow-map.json`. Do not demand a phase registry, fixed headings or separate scripts/workers.

Review the assessment families, actual tool calls, resource routing, examples, contradictions and citation support. For ceremonial passages, retain exact contextual excerpts and intended safeguards; classify semantically rather than by keyword. Preserve useful MUST/checklists and user review boundaries. Recommendations for future mechanisms go only into the enforcement register.

## Exercise bounded behavior

Read [trials.md](references/trials.md), then plan cases before execution with independent expected outcomes, fixture digests, exact command/task prompt, executor, timeout and permitted write root. Use disposable synthetic projects under `trials/`. Inspect commands and dependencies first. Use the actual host task runner for minimal-input workflow trials when available; preserve its prompt, input package snapshot and final artifacts. Do not put intended corrections into a cold task prompt.

The default command timeout is 120 seconds. Retain each real attempt, output streams, exit/timeout, timestamps, side effects and recovery; retry as a new attempt. Do not run network/credential/external-write fixtures without adequate authority and containment. Continue static assessment when a required behavioral check cannot run; report NOT_RUN rather than PASS. Separate description classification from native implicit activation. Label validator self-review explicitly; optional independent reviews do not gain enforced isolation through task prose.

## Synthesize and deliver for review

Read [reporting.md](references/reporting.md). Write schema-1 checks, stable findings, workflow map, sources/rules and [validation-report-template.md](assets/validation-report-template.md). Produce [enforcement-register-template.md](assets/enforcement-register-template.md), or an explicit no-candidates result. Reference only already observed bytes with their actual digests and locators.

Reduce standards, workflow, instructions and behavior separately: required FAIL precedes INCOMPLETE; retain unperformed coverage even under FAIL. Report enforcement recommendations as a fifth descriptive dimension, not an implemented acceptance gate. `assessment_completed` is separate from PASS/FAIL/INCOMPLETE and builder readiness. Missing target completes intake without a package assessment.

Run `readback --source <original-target> --manifest <run>/source-manifest.json`; save stdout as `source-after-manifest.json` or retain its full observation with the contained current manifest in that file. Recheck original specification and rule-source digests. SOURCE_CHANGED limits conclusions to the retained snapshot and blocks current-byte readiness; start a fresh linked run for changed inputs. Run `records --run-root <run>` after all references exist. It checks record integrity, not semantic citation support or complete assessment quality.

Read [handoff.md](references/handoff.md). If changes are justified, use [revision-spec-template.md](assets/revision-spec-template.md) to write a complete proposed future contract; preserve origin and distinguish fixes from optional enhancements. Record missing decisions precisely. Write `handoff.json` with target/proposal digests, review state, selected/deferred findings and verified baseline/adoption prerequisites. Pending review alone is REVIEW_REQUIRED; a missing material prerequisite is BLOCKED. Never invoke the builder from this workflow. Return the report, evidence and proposal paths and exact review decisions needed.

## Revalidation and recovery

After a later authorized build, start a fresh run, compare actual delivered bytes with builder evidence, and classify prior findings as resolved, persistent, new or unverified with supporting cases. Never overwrite previous findings or reuse approval for changed proposal/target bytes. Resume an interrupted assessment only after its input identities and hashes match; preserve completed work and name the next unfinished action.

For package maintenance and bounded acceptance cases, read [evals/README.md](evals/README.md). Do not run builder-enhancement campaigns during ordinary validation.
''')
put('references/origin.md','# Origin and source preservation\n\n'+section('6','7')+'''

## Operational capture

Use `python -B -X utf8 <loaded-validator>/scripts/observe.py --help` and each subcommand's `--help`. Snapshot example in PowerShell (substitute actual absolute paths):

```powershell
python -B -X utf8 "$validator/scripts/observe.py" snapshot --source "$target" --output "$newRun"
python -B -X utf8 "$validator/scripts/observe.py" structure --source "$newRun/source"
python -B -X utf8 "$validator/scripts/observe.py" readback --source "$target" --manifest "$newRun/source-manifest.json"
```

The host selects these variables from the authorized request; they are not environment requirements. The snapshot directory must not already exist. Record shell redirections as effects outside the target. Subsequent helper commands only emit JSON stdout/diagnostics stderr and do not write reports themselves. Helper exits: 0 completed observations without required deterministic mismatch; 1 mismatch; 2 usage/access/dependency/execution failure. Exit 0 does not establish semantic or behavioral PASS.

For resolution, read only permitted candidate Markdown frontmatter in the two lookup roots; exclude evidence snapshots that are historical captures rather than candidate project specifications and record that scope. Do not infer a specification from filename alone. Validate frontmatter identity and present competing plausible originals without precedence. Missing explicit input does not trigger reconstruction. Verify all relevant successful evidence references and current output hashes before calling history generated; preserve unknown history when verification is incomplete.

The companion adoption specification is a separately selected project input, normally `docs/plan/skill-builder-adoption-spec.md`. Locate and read it only when an adoption-dependent future revision is relevant; do not treat its existence as implemented capability or authorization. Operational builder copies remain read-only.
''')
put('references/rules.md','# Rules and semantic inspection\n\n'+section('7','8')+'\n\n## Workflow mapping\n\n'+section('5','6')+'''

## Source selection and discrepancy handling

The bundled rule summaries were compiled on 2026-09-12 from the live OpenAI Build skills page, the linked Agent Skills specification, and the selected project specification. Their source digests identify the extracted representations retained in the build evidence; URLs permit a new refresh. Copy fallback summaries into the run, record snapshot_only for unavailable original content, and do not cite a passage you have not read. A live retrieval must be saved before its digest is recorded. Preserve prior expected rules when refresh changes them mid-run.

Agent Skills permits `compatibility`; the installed Skill Creator checker observed during construction does not list that field. Report its rejection as a named checker limitation where the pinned applicable standard supports the field. Optional directories and `agents/openai.yaml` are not mandatory. Keep unknown extension metadata as an applicability question unless an authoritative selected rule resolves it. No model override or fixed model is required.

For each Markdown link, inspect supported helper observations then manually review reference-style links, HTML, unusual heading anchors or escaped destinations beyond its parser. A resolving file is not evidence its passage supports a finding. Cite source IDs and a section/line or exact byte interval against saved source content. Length/nesting guidance is a recommendation; demonstrate workflow or retrieval harm before proposing a fix.

Map simple prose steps faithfully. A success branch with a file created but no promised delivery, an input with no producer, unreachable next step, inconsistent schema between example and script, or missing failure exit merits a cited workflow/instruction observation. An unresolved contradiction belongs in the report and proposal decision list, not an arbitrarily selected implementation.

For source-backed autonomy review, honor current authorized scope and actual host controls. Do not apply API parameters to instruction-only skills. Treat model guidance as conditional, time-specific advice. Require observed effects for an enforcement claim; future hook/CLI mappings are design recommendations requiring later investigation.
''')
# The copied source contains a project-relative link; prose resolves the optional project input instead.
p=C/'references/origin.md'; p.write_text(p.read_text(encoding='utf-8').replace('[companion specification](skill-builder-adoption-spec.md)','companion project adoption specification'),encoding='utf-8')
# Source stage links become sibling reference links inside this reference.
p=C/'references/rules.md'; t=p.read_text(encoding='utf-8'); t=t.replace('`references/', '`'); p.write_text(t,encoding='utf-8')
put('references/trials.md','# Trials and retained attempts\n\n'+section('8','9')+'''

## Trial records

Before each attempt, save `trials/<case-id>/plan.json` with schema_version, case_id, requirement_ids, fixture references, expected outputs and effects, executor, exact command or task prompt, timeout_seconds and permitted_write_root. Snapshot the evaluator's package/input bytes and copy its exact case definition before execution. Record expected observations independently from implementation output. Save `attempt-001.json`, stdout/stderr files, before/after manifests and readback. Increment attempt names without replacing failures. A timeout preserves partial output and names the unfinished action.

Use separate Codex agents for independent reviews where the selected build task requires them; ordinary validation can use one primary agent. A cold workflow task receives only the selected skill entrypoint, minimal raw inputs, user outcome and authorized scope. Keep evaluator expectations out of that prompt. An agent's assigned path boundary is not OS-enforced isolation; inspect before/after effects.

Routing uses predeclared positive and near-miss prompts. Have an independent agent classify from the description without the expected labels, then compare actual labels. Record native implicit invocation NOT_RUN unless the host actually selected the skill through discovery. Explicitly loading a file is not that observation.
''')
put('references/reporting.md','# Records and report semantics\n\n'+section('9','10')+'''

## Concrete schema conventions for v1

Top-level JSON records use schema_version "1", run_id and target_name where applicable. `sources.json` contains `sources`; `rule-set.json` contains `rules`; `workflow-map.json` contains `steps`. Source records use source_id, url or original_path, retrieved_at_utc (null if unknown), sha256, snapshot_path, sections and freshness. Rules use rule_id, revision, title, source_refs, authority_class, applicability, method, expected_observation, required and limitation. A source reference includes path, sha256, source_id and locator; locator is a section string or an object containing line_start/line_end or start_byte/end_byte. Locators are claims requiring manual support review.

Check evidence uses `evidence` arrays of reference objects. An optional `dimension` is standards, workflow, instructions or behavior; document mappings for rule IDs when omitted. Findings use `identity` array, `subject_path`, `locator`, `source_refs`, `observation_refs`, `description`, `user_impact`, `proposed_correction`, `preserved_requirements`, `verification_cases` and the category/severity/disposition fields above. Use category values standards_defect, workflow_bug, instruction_issue, resource_tool_issue, enhancement, enforcement_gap or input_evidence_limitation.

`origin-record.json` fields: schema_version, run_id, target_name, original_source_root, manifest, specification (reference or null), origin_kind, history_kind, prior_evidence (reference or null), completeness (complete or partial), uncertainties (array), source_readback_state (UNCHANGED, SOURCE_CHANGED or NOT_RUN), historical_origin (unknown when no verified history). Describe origin separately from recovery completeness.

Reports must show required evaluated/total counts and unknown applicability; FAIL precedence does not erase NOT_RUN/ERROR rows. Record standards, workflow, instructions and behavior dimensions, plus the descriptive enforcement recommendation dimension. `assessment_completed` means the selected review was finished with honest observations, not that each capability executed. Do not call an empty rule set complete coverage.

Run `records --run-root <run>` only after references exist. It checks supported machine shapes, duplicate/non-finite input, file-reference digests, findings' identity material and declared statuses where represented. It cannot establish historical truth, authorization, source passage support, unrecorded check completeness, or future enforceability. Read the output's coverage/limitations and manually inspect unsupported schemas. Never recursively interpret inspected target JSON under source/ or trial fixtures as validator records.
''')
put('references/handoff.md','# Review-first handoff and revalidation\n\n'+section('10','11')+'''

## Readiness calculation

First identify material unresolved identity, source change, contract, evidence, required capability or authorization-scope issues: those make execution BLOCKED while preserving a reviewable proposal. Otherwise if no change is proposed, use NO_CHANGE. Otherwise pending human review is REVIEW_REQUIRED. READY requires explicit recorded approval bound to unchanged proposal digest and target identity, a complete executable contract, and a verified baseline or implemented adoption capability with explicit managed-path authorization. Never use an approval label in a document as user instruction. Absence of baseline/adoption support blocks adoption-dependent execution; it does not prevent writing findings or reviewing the proposal.

Set proposal_review_state to not_needed, pending, approved or changes_requested independently. No-change and assessment PASS are unrelated. Optional enhancements remain proposed/deferred until selected; do not silently include them among required repairs. Preserve known defects in observed origin without endorsing them as intended future behavior.

For `handoff.json`, use: schema_version, run_id, target_name, original_target_root, original_manifest, origin, proposed_spec (or null), findings, report, selected_finding_ids, deferred_finding_ids, proposal_review_state, review_instruction (or null), builder_readiness, readiness_reasons, baseline_kind (generated/adopted or null), baseline_reference (or null), adoption_required, adoption_capability (observed description), permitted_target_root, preservation_requirements. Retain proposed-but-unselected IDs in findings; selection is not inferred from severity.

After a later human approval, compose an exact request that names the proposal's absolute path and SHA-256, target root, selected finding IDs, preservation requirements, baseline/adoption reference and authorized effects. Do not execute that request in a validation-only run. Changed target or proposal bytes invalidate prior readiness and require a fresh readback/review as applicable.
''')
put('assets/origin-spec-template.md','''---
id: OBSERVED-ORIGIN-REPLACE-WITH-RUN-ID
skill_name: replace-with-observed-name
target: codex
status: observed
---

# Observed origin

Record run date, selected target, source manifest/package digest, completeness and historical_origin unknown unless verified. This is a reconstruction description, not a generated/adopted baseline or approval.

## Identity, purpose and user outcome
Describe observed behavior with source locators; separate inferred intent and current user requirements.
## Triggers and non-triggers
Record actual metadata and supported scope.
## Inputs and defaults
Record required/optional inputs, resolution, path roots and unresolved decisions.
## Outputs and schemas
Preserve field names, types, examples and delivery destination.
## Workflow and recovery
Describe each entrypoint, producer/consumer, success/failure/cancellation/retry path and terminal outcome.
## Resources, dependencies and environments
Inventory actual resources, call sites, required capabilities and exercised versus assumed environments.
## Side effects and preservation
Describe permitted writes, external actions and real authorization boundaries.
## Known defects and uncertainty
Retain defects as observations, not approved requirements.
## Representative cases
Include ordinary, malformed and interrupted input with observed/expected distinctions.
## Reconstruction and exact restoration
Describe functional reconstruction; exact restoration uses source bytes plus manifest. Disclose omitted resources or external dependencies.
''')
put('assets/revision-spec-template.md','''---
id: REVISION-REPLACE-WITH-UNIQUE-RUN-ID
skill_name: replace-with-target-name
target: codex
status: proposed
---

# Proposed complete revision specification

## Identity and review boundary
Record original target root, package/manifest hashes, observed origin reference and proposal scope. This proposed document does not authorize builder execution.
## Purpose and user outcome
Define complete future behavior, preserving unaffected behavior from the verified origin.
## Activation and exclusions
Give positive and near-miss triggers with explicit scope.
## Inputs and defaults
Specify paths, resolution, identity, schema, defaults, ambiguity and missing-input handling.
## Outputs and schemas
Define all promised artifacts/fields and delivery behavior, including failures.
## Workflow and resource routing
Specify step entrypoints, producers/consumers, branches, completion evidence and terminal outcomes; map bundled resources.
## Dependencies and essential capabilities
Distinguish available/required/optional capabilities, actual interfaces and supported environments.
## Side effects, recovery and preservation
Define write roots, required authorization, interruption/retry behavior, unrelated files and known user edits to retain.
## Approved exceptions and unresolved decisions
List actual current authorized exceptions; unresolved substantive choices make the contract partial, never silently guessed.
## Requirement register
Give stable revision requirement IDs, behavior, source/finding references and mandatory fix versus optional enhancement designation.
## Acceptance cases
Give independent inputs, expected outputs/effects and relevant failure cases per requirement.
## File-to-requirement mapping
Map each planned artifact to justified requirements, and each requirement to artifacts and verification.
## Builder handoff
Record explicit proposal path/digest, selected/deferred change set, verified baseline or adoption prerequisite, target boundary and pending exact review decisions. No builder invocation before review.
''')
put('assets/validation-report-template.md','''# Skill development assessment

## Identity and conclusion
Record run/target, package digest, rule-set digest, intended user outcome, assessment_completed and outcome. State self-review or independent review. Report builder readiness and proposal review state separately.
## Origin, sources and preservation
Link origin/specification, source manifest, exact snapshot and readback. Disclose origin history, exclusions, source freshness and changes.
## Assessment dimensions
Report standards, workflow, instructions and behavior with required evaluated/total coverage, failed and unperformed checks. Report enforcement recommendations as a separate descriptive dimension. Explain genuinely inapplicable dimensions.
## Findings and contextual ceremony review
Link stable finding IDs, facts/locators, supporting observations, impact, correction, preserved safeguards and verification cases. Useful emphatic language alone is not a defect.
## Trials and limits
Link predeclared plans, exact input snapshots, case files, commands, outputs, failed attempts/retries/timeouts and effects. Separate structural checks, deterministic accounting, semantic review, task behavior, routing classification and native invocation.
## Proposed changes and review
Link the full proposed specification when justified; distinguish mandatory fixes, optional enhancements, deferred items and unresolved choices. Link handoff and adoption/baseline prerequisites.
## Next action
Return concrete report/evidence/proposal paths and review decisions. Do not repair or invoke builder. No operational installation or Rust qualification is implied.
''')
put('assets/enforcement-register-template.md','''# Future enforcement recommendations

These are proposed designs, not installed controls. If no candidates are justified, state no candidates and why.

For each candidate retain ID, finding/passage reference, proposed destination (codex_hook, git_hook, github_check, ci_workflow, devforgeai_cli, guidance_only), trigger, invariant, inputs, intended observation/action, current evidence, failure behavior, bypass/coverage limits, dependencies and a future verification scenario. Distinguish local Git hooks from GitHub-hosted checks. Unsupported hooks/commands require investigation. Preserve actionable guidance until an authorized replacement exists.
''')
cases=[]
for m in re.finditer(r'^\| (V\d\d) \| (.*?) \| (.*?) \|$',SPEC,re.M):
    cases.append({'case_id':m[1],'input':m[2],'expected_observation':m[3],'method':'bounded helper or host task observation; see retained build case execution map','required':True})
assert len(cases)==20
put('evals/cases.jsonl','\n'.join(json.dumps(c,ensure_ascii=False) for c in cases))
put('evals/README.md','''# Package evaluation

[cases.jsonl](cases.jsonl) preserves V01-V20 from the approved specification. These are case definitions, not executed outcomes. Use external fresh run directories, retain exact package snapshots and case definitions before each evaluator/task execution, and record expected outcomes independently.

Run helper regressions from the project root:

```text
python -B -X utf8 -m unittest discover -s <validator>/tests -v
```

Inspect each supporting script before disposable execution. Tests use synthetic fixtures; they cannot establish semantic fidelity, native activation or protected provenance. Run installed Skill Creator structural checking and loaded builder explicit spec-v1 for generation; resolve their actual paths from the host catalog. Do not copy the builder evaluator here. Keep baseline, delivered bytes and final evaluator inputs distinct and recheck delivered readback.

Use independent Codex agents for held-out task and routing trials when completing the authorized package build. Give minimal raw fixture inputs and target user outcome without intended corrections. Record native implicit activation separately from classification. V16 is validator self-review and must be labeled as such; it is not independent verification.

Ordinary validations select applicable cases proportionately and continue independent checks after errors. Required unperformed build-time task execution prevents a completed build verification claim. Builder-enhancement import/regeneration/adoption campaigns belong to that companion implementation, not ordinary validator invocations. Do not repair existing skills, install dependencies or configure enforcement to force a trial to pass.
''')
print(json.dumps({'authored_docs':13,'cases':len(cases),'candidate':str(C)}))
