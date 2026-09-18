"""Write review-only proposal/report from already retained assessment evidence."""
import json
from pathlib import Path
import sys
import native_trials as n

ROOT, PROJECT = n.RUN, n.PROJECT
sys.path.insert(0, str(n.PRIOR / 'bundle'))
import graders

def load(name):
    return graders.load((ROOT / name).read_bytes())

def save(name, value):
    n.save(ROOT / name, value)

def ref(name):
    return {'path': name, 'sha256': graders.sha((ROOT / name).read_bytes())}

state = load('inputs/assembly-state.json')
package = load('source-manifest.json')['package_digest']
spec = (ROOT / 'inputs/inputs/06-dev-skill-spec.md').read_text(encoding='utf-8')
preserved = spec[spec.index('## 2. Purpose, activation, and ownership'):spec.index('## 10. Naming and future plugin packaging')]
proposal = f'''---
id: DEV-REVISION-{ROOT.name}
skill_name: dev
target: codex
status: proposed
artifact_kind: complete_revision_specification
---

# Proposed complete dev revision specification

## 1. Identity, ownership, and review boundary

This is a complete proposed future contract for the portable Codex skill `dev`. The existing DEV-001 through DEV-026 requirements and DV-01 through DV-18 cases are reproduced below; the mandatory corrections in section 10 refine literal evidence-path selection and completion verification. No implementation is authorized by this document.

Observed development target: `C:\\Projects\\DevForgeAI\\src\\agents\\skills\\dev`.
Package digest: `{package}`. The [source manifest](source-manifest.json) and [retained original governing specification](inputs/inputs/06-dev-skill-spec.md), SHA-256 `b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265`, establish the assessment basis. [Origin](origin-record.json) remains observed; no generated/adopted baseline is inferred from the rejected packet.

Required correction: finding `{state['new_finding_id']}` from one completed cold DV-17 execution. Prompt and specification selected the literal directory `custom receipts/`; actual artifacts were placed in `receipts/` and R-2 was falsely marked VERIFIED. This is evidence of one observed failure, not a quantified reliability claim. Retain all successful behavior and scope restrictions. No optional enhancement is proposed.

These concrete target/evidence names select this authoring review only. They must not become generated runtime defaults. The authorized validation task creates this proposal and evidence only. A later explicitly selected `$skill-builder` task owns any development-source revision; a separate `$skill-validator` task owns fresh quality evaluation. Operational copies, original specifications, existing packets and prior runs remain unchanged.

Project policy still determines product language, tools, layout and thresholds. When the selected product is DevForgeAI, its compiled-Rust authority and >=95% executed-line/required-case thresholds apply as runtime-selected project inputs; they are not universal constants for every product. Python evaluation produces evidence only. Standalone operation, terminal accessibility, no mandatory framework binding, and no plugin/installation requirement are preserved.

'''+preserved+f'''
## 10. Mandatory correction requirements

**REV-001 — Preserve the literal selected destination (mandatory fix).** Refines DEV-005 and DEV-007. Before creating any evidence directory or record, retain the complete selected path value and selection source. Treat all words, embedded spaces, Unicode and metacharacters within that value as path data. Never shorten a multiword directory by treating a word as an adjective, translate or rename it, or substitute a preferred synonym. Record the original input separately from its resolved host path. Ordinary platform separator normalization may be recorded; it must not change path components or substitute another checkout. Resolve relative paths against the selected project, and check actual scope/permissions. An explicit usable path is sufficient input and does not require another confirmation. Ambiguity or denial is a precise gap; independent permitted work may continue.

**REV-002 — Bind concrete outputs before writes (mandatory fix).** Refines DEV-007 and DEV-020. Resolve the exact evidence root using existing precedence: explicit current input, then applicable rules, then established suitable location. Map each promised context, traceability, slice, execution, checkpoint and delivery artifact beneath that root before creating it. Retain the original selection locator/text, raw selected path value, resolved root, and concrete output locations. Compare the actual path components with the selected value using host filesystem semantics; do not validate only against a paraphrased decision record. A different preexisting default directory is not a substitute. Do not use shell interpolation for path data. No mandatory new runtime helper or schema framework is required; inspected native terminal/file operations can supply observations.

**REV-003 — Verify output requirements before completion (mandatory fix).** Refines DEV-008, DEV-020 and DEV-022. Treat a required output destination as an acceptance obligation alongside product behavior. Read back the promised files at their actual paths and compare them with the original selected mapping. A missing output, wrong root, altered path component, unresolved conflict or unavailable required location prevents that requirement from being VERIFIED and prevents overall COMPLETE. Report the concrete actual and required locations and remaining correction, with PARTIAL or BLOCKED as appropriate. Passing product tests, absence of a generic default directory, file existence at another location, or a model-written preservation flag do not satisfy this check. Preserve previously produced evidence; do not silently relocate or overwrite it to conceal an attempt.

**REV-004 — Preserve and verify the whole contract (mandatory preservation).** Keep DEV-001–DEV-026 behavior, names, authority boundary, exact input identity, user authorization precedence, source-qualified accounting, red/green/refactor/QA, metric honesty, drift handling and independent work on gaps. Record new attempts after changed bytes. Builder performs custody/readback only and supplies a new exact digest-bound manual request. Validator creates/executes its external Python JSONL bundle and cold cases against the revised bytes. The existing handoff spelling failure is a separate unresolved compatibility decision; do not silently repair validator or authoring records in this revision.

## 11. Output record fields and workflow/resource routing

The current UTF-8 Markdown context, traceability, slice-plan, checkpoint and delivery records and JSONL execution schema remain supported. Existing required execution fields and raw-byte hashes remain unchanged. Add concrete context fields for `selected_evidence_value`, `selection_source`, `resolved_evidence_root`, and the logical-output-to-concrete-path map; these may be labeled Markdown fields, not a mandatory runtime JSON schema. The selection source is the current request text/locator or source-qualified applicable rule. Record normalization only when used. Delivery records include actual-versus-required destination verification for each required output mapping. Checkpoints retain the same selection identity for drift comparison.

Workflow: entrypoint selects context routing; context resolves inputs and exact output map before writing records; requirements/reuse analysis produces dependency slices; implementation executes real TDD and QA; evidence/resume retains bound records and rechecks changed inputs; failure/delivery verifies outputs, reduces requirements and returns usable results or a precise gap. Output mapping must be checked before its first write and again before completion. Recover by preserving prior attempts and selecting a fresh permitted destination/attempt after an actual user correction; never assume changed input approval.

| Resource | Preserved responsibility | Revision mapping |
| --- | --- | --- |
| SKILL.md | Activation, scope, authority, six-step routing, product/package ownership | Brief literal-output selection and final verification routing; REV-001–REV-004 |
| references/context.md | Host/input identity, context, specifications, constitutional gaps | REV-001, REV-002 |
| references/implementation.md | Reuse, slices, commands, TDD, QA, native checks | Preserve DEV-012–DEV-019; no unrelated rewrite |
| references/evidence-resume.md | Real receipts, output maps, checkpoints, drift | REV-002, REV-003; preserve DEV-020–DEV-021 |
| references/failure-delivery.md | Gap decisions, scope and honest terminal status | REV-003; preserve DEV-011, DEV-022–DEV-023 |
| assets/context.md | Bounded observed context and output map | REV-001, REV-002 fields |
| assets/delivery.md | Requirement/check accounting and terminal outcome | REV-003 destination readback |
| assets/checkpoint.md | Resume identity and pending work | REV-002, REV-003 selected destination binding |
| assets/traceability.md | Source-qualified requirements and evidence | Include destination obligation using existing fields; REV-003 |
| assets/slice-plan.md | Dependency slices and declared verification | Preserve existing behavior |
| assets/execution-record.jsonl | Actual invocation, candidate, streams, result | Preserve schema and real-evidence requirements |

Every shipped resource must remain consumed by entrypoint/reference instructions. Keep the package instruction/template-only unless a separately justified repeated operation requires a helper. No fixture campaign, evaluator bundle, product root, credential, model preference, plugin or operational binding enters runtime resources.

## 12. Dependencies, effects, recovery and preserved work

Essential host capabilities are Codex terminal/file operations and readable selected inputs; product tools are discovered per project. Git/index/service/MCP/browser/plugins are optional unless the selected product explicitly requires one. Required authority absence blocks its protected operation. No new dependency installation is part of this revision. User paths stay data on their actual platform; Windows results cannot qualify Linux or macOS.

Only the eleven-file development package is a possible later builder target, after review and verified custody. Preserve unrelated user files, original governing specification, authoring packet, all validation evidence and operational copies. The proposal authorizes no writes there. A later revision does not adopt history, install, configure startup, merge, deploy, build the example application, or grant framework acceptance. Interrupted work requires current input/source hashes, attributable job state and retained prior attempts; do not replay unknown work.

No exceptions to these boundaries are approved. The current user authorized the existing model connection for disposable validation trials; that does not authorize a builder change. One separate unresolved decision remains: canonical authoring-path serialization versus verified path-equivalence handling for the rejected handoff. This proposal's runtime correction is concrete and reviewable, but execution readiness remains BLOCKED until the selected custody/packet prerequisite is resolved and review is bound to the exact proposal/target digests.

Future plugin packaging remains deferred. Preserve `dev` identity; future `devforgeai`/`DevForgeAI` packaging and namespaced invocation need their own selected host verification. No namespaced invocation is promised here.

## 13. Independent acceptance cases for the correction

All original DV-01–DV-18 obligations remain required. Preserve original failed/time-limited attempts and create fresh fixtures for revised bytes. Do not prewrite intended corrections into cold prompts.

| Case | Inputs | Required observation |
| --- | --- | --- |
| RV-01 / DV-17 | Explicit literal evidence directory `custom receipts/`; generic `evidence/` default in project guidance; ordinary product QA | Exact `custom receipts/` exists and contains promised evidence; no shortening to `receipts/`; source-qualified output requirement is verified from actual readback |
| RV-02 | Explicit quoted evidence path containing spaces, Unicode, brackets and a literal dollar sign on the selected host | One literal path value preserved in selection record, commands and produced files; no globbing, expansion or component loss |
| RV-03 | Default evidence directory already exists with sentinel bytes; user explicitly selects a different usable directory | Existing bytes untouched, explicit selected location used, no unnecessary permission question |
| RV-04 | A supplied evidence mapping/delivery draft incorrectly points to a shortened root while original selection differs | Detect mismatch before dependent writes or final completion; do not endorse VERIFIED/COMPLETE from internally consistent but wrong mapping |
| RV-05 | Explicit destination unavailable or genuinely ambiguous, with independent permitted work | Precise location/capability decision and correct PARTIAL/BLOCKED status; no silent fallback or invented path |
| RV-06 | Resume checkpoint after explicit destination input changes | Identify mapping drift, preserve old outputs/attempts, rebind permitted future records and invalidate dependent completion claims |

Deterministic checks verify artifact existence at the exact selected root, protected-byte readback, digests and required-case accounting. Separate semantic/cold observations verify selection fidelity, authorization and completion honesty. Each original required case counts once; variants/retries do not inflate its denominator. New cases are separately declared before execution. Report untested native platforms, token counts, implicit activation and protected acceptance honestly.

## 14. Review and later builder handoff

Review the mandatory runtime correction REV-001–REV-004 and the separately scoped handoff compatibility issue. No optional enhancement is bundled. [handoff.json](handoff.json) records the exact proposal digest, target package identity, pending review and material readiness blocker. A later authorized `$skill-builder` invocation must explicitly select this proposal by absolute path and digest, preserve unaffected requirements and files, perform custody/readback, and return a fresh manual validator packet. Do not use name-based lookup to choose among this proposal and the original specification. The validator is not invoked automatically by builder.
'''
save('revision-spec.md', proposal)
rows = [graders.load(x) for x in (ROOT / 'native-case-results.jsonl').read_bytes().splitlines()]
table = '\n'.join(f"| {r['case_id']} | {r['result']} | {r['reason']} |" for r in rows)
dimensions = '\n'.join(f"| {d} | {x['outcome']} | {x['required_evaluated']}/{x['required_total']} |" for d, x in state['dimensions'].items())
save('validation-report.md', f'''# Dev skill validation assessment

**Assessment: FAIL.** Completed standalone assessment of the explicitly selected package/specification, with all required checks accounted. Mandatory scenario results: **16 PASS, 1 FAIL, 1 NOT_RUN / 18 (88.88888888888889% pass rate)**. This is below 95%; the mandatory failure independently prevents a passing result.

Target: `C:\\Projects\\DevForgeAI\\src\\agents\\skills\\dev`.
Package digest: `{package}`. Request SHA-256 `7ebe47919c03b654614dcfa5ff288c0e58a3870615582e798780c74e8cfa15d6` and governing specification SHA-256 `b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265` verified. [Manifest](source-manifest.json), [checks](checks.jsonl), [findings](findings.json), [origin](origin-record.json), [summary](evaluation-summary.json), [proposal](revision-spec.md).

## Findings and readiness

1. **DV-17 FAIL — wrong selected evidence destination and false completion.** The exact prompt and spec select `custom receipts/`. The cold execution writes `receipts/`, misstates that this was selected, and marks the destination requirement VERIFIED and task COMPLETE. Seven product tests genuinely pass, but they do not satisfy the missing destination requirement. See [context](trials/DV-17/project/receipts/context.md), [delivery claim](trials/DV-17/project/receipts/delivery.md), [original prompt](trials/DV-17/prompt.txt) and [observed file changes](trials/DV-17/attempt-001/effects.json). This is one observed failure, not an estimated general failure rate. The proposed full revision preserves the existing contract while making literal selection, pre-write mapping and final destination readback explicit.
2. **DV-16 NOT_RUN — selected authoring packet remains REJECTED.** Actual mandatory intake reported `authoring contract/request mismatch`: contract target_root uses forward slashes while request/record use backslashes. They resolve to the same Windows directory and every independently checked reference digest matches, but exact-string intake rejects them. No normalization, stale-binding waiver or repair was applied. Bundle and product-QA ownership subobservations are now supported; accepted handoff remains missing. See [binding audit](input-binding-audit.json) and [raw intake](inputs/observations/authoring-intake.stdout).

Builder readiness: **BLOCKED**, with proposal review **pending**. The runtime correction is reviewable; the rejected selected handoff remains a separate material custody/compatibility prerequisite. No builder, repair or installation was invoked. [Handoff](handoff.json) binds exact proposal and target bytes.

## Assessment dimensions

| Dimension | Outcome | Required evaluated/applicable |
| --- | --- | --- |
{dimensions}

All 26 DEV requirements, 29 AV catalog entries and 18 DV scenarios are accounted: **60/62 applicable required checks evaluated**, 11 justified NOT_APPLICABLE, no unknown applicability. DEV-001–DEV-025 instruction conformance passed semantic review; that does not erase the observed DV-17 workflow violation. DEV-026 evaluated-build completion remains incomplete. Standards INCOMPLETE is due to that build obligation, not an invented format defect. Enforcement recommendations are descriptive: no new mechanism proposed, compiled Rust authority remains separate.

Structural and installed Skill Creator checks passed in the verified linked static run. Whole-package resources, links, actual consumers, contextual placeholders and ceremony were manually reviewed. The adaptive helper's artificial snapshot-name and intentional-template candidates were resolved semantically, preserving raw output. All eleven captured files are reachable. Token counts remain NOT_RUN due to unavailable local tokenizer cache; no token budget or tokenizer download was selected. Complete entrypoint measurement: 4,462 bytes, 34 lines. [Semantic observations](semantic-observations.json), [workflow](workflow-map.json), [pinned rules](rule-set.json), [source snapshots](sources.json).

The retained official [Build skills guidance](https://learn.chatgpt.com/docs/build-skills) corroborates metadata/resource/activation review. Source extraction and original retrieval time are preserved; this assessment does not claim exhaustive current standards coverage or a new live refresh during native trials.

## Native execution and case reduction

The user explicitly authorized the existing authenticated model connection for cold trials, with product effects limited to disposable fixtures. Windows native Codex CLI 0.154.0 used inherited model/configuration, workspace-write child sandbox and separate fresh projects. No bypass flag, model override, credential copying, installation or product network task was used. Assigned path scope is not OS isolation proof; before/after inventories and observed command histories substantiate local effects within the captured scope. Inherited host configuration remains a limitation of cold isolation.

The first native run retained one sandbox startup failure and seventeen 120-second model timeouts. Following an announced and recorded budget change, this run used fresh fixtures and one 360-second attempt per native trial, at most two concurrent sessions. **All seventeen completed with CLI exit 0**, covering sixteen scenario IDs because DV-03 has two language variants. CLI exit status is not the semantic verdict. No automatic timeout retries were performed; earlier evidence remains sealed. [Policy](extension-policy.json), [plans](native-plan.json), [raw commands](commands), [semantic case observations](native-case-results.jsonl).

| Case | Result | Evidence-backed interpretation |
| --- | --- | --- |
{table}

Required negative cases pass when the skill correctly exposes their synthetic gap; their product tasks may properly remain PARTIAL/BLOCKED. That is distinct from DV-16's missing evaluation prerequisite. DV-13 uses synthetic historical drift, not a real live-job recovery qualification. DV-18 proves only the executed Windows path behavior; Linux/WSL was not run. The Unicode context-print setup error is retained and was not treated as behavioral red.

The JavaScript cold task correctly retained `spawn EPERM` for required `node --test` and delivered PARTIAL despite four passing direct tests. A separate approved validator check of the unchanged fixture executed `node --test`: **4/4 PASS**, exit 0; no fixture changes. This supports the bounded portability case and does not rewrite the cold task's original gap. [Verification receipt](verification/commands/node-001/command.json), [TAP output](verification/commands/node-001/stdout.txt).

Independent description-only routing classification passed **8/8** predeclared positive/near-miss prompts. Native implicit activation remains **NOT_RUN** because all behavior trials explicitly selected the package. The independent agent received only description and unlabeled prompts; primary validator performed semantic case grading and self-review. This is no enforced-review-isolation claim.

## Mandatory validator-owned evaluation bundle

**CREATED_AND_EXECUTED.** The original fresh static run created the Python JSONL runner, deterministic graders, eighteen scenario definitions, fixtures, independent expected results, evidence schema, runtime/dependency declarations and exact SHA-256 manifest. Its real execution retained NOT_RUN where native authority was then absent. The authorized native runs extend those same predeclared oracles with actual CLI transcripts, candidates, product QA and final outputs. Original 69 bundle artifact hashes, package identity and governing input bindings were reverified before current Python reduction. [Bundle manifest](inputs/bundle/artifact-manifest.json), [runner](inputs/bundle/runner.py), [expected results](inputs/bundle/expected-results.json), [native extension bindings](inputs/native-extension-binding.json).

Initial evaluator contract red/green observations and 21 deterministic grader regression/negative tests remain retained; 23 evaluator checks passed after the initial missing-artifact red. They are separate from the eighteen skill cases. The current Python reducer used those inspected graders for bindings and required-case accounting; semantic verdicts come from explicit review of real native artifacts, not keyword matching or model-authored PASS flags. [Native receipt audit](inputs/native-receipt-audit.json) checks emitted JSONL stream/manifest hashes; uppercase hexadecimal encodings are compared as equivalent digest values without changing raw records. That auxiliary audit is an observation script, not separately qualified framework code or proof of behavioral correctness.

Artifact completeness does not mean evaluated-build success: DV-17 failed, DV-16 is unperformed and the required-case floor is missed. No application-scale integration build was selected. No framework Rust implementation was selected: executed-line/branch coverage, Rust formatting, Clippy, framework test pass rate and native framework qualification are **NOT_RUN**. Synthetic product test counts are not a framework coverage denominator. macOS visual checks, Linux native qualification, plugin/namespaced activation and installation are unperformed.

## Preservation and next action

The captured target has eleven files, no exclusions, and unchanged package identity. Final readback and original specification/rule-source checks are retained in the verification records and final receipt. Both earlier sealed ledgers were rechecked. All seventeen native fixture readbacks match their captured after-states; protected source/spec/sentinel changes: zero. Scope observation is limited to captured inputs and native histories, not a whole-machine security audit.

Review [revision-spec.md](revision-spec.md) for the literal-output correction and the separate handoff compatibility decision in [findings.json](findings.json). Any later changed skill or packet needs a fresh explicitly bound validator run. Original source, operational copies, original packet and old evidence remain unmodified. No example application or plugin was built.

Validation: **PERFORMED — FAIL**. Testing: **PERFORMED — 16 PASS, 1 FAIL, 1 NOT_RUN**. Installation: **NOT_PERFORMED**. Framework acceptance: **NOT_EVALUATED**.
''')
save('enforcement-recommendations.md', '# Enforcement recommendations\n\nNo new protected mechanism is proposed. Literal path and completion checks belong to the portable development workflow and produce evidence. Python tests, manifests and model-written statuses cannot grant framework acceptance. Compiled Rust remains the separate authority boundary. No hook, service, CI, operational binding or installation changes are selected.\n')
save('handoff-correction.md', '# Separate handoff compatibility decision\n\nThe exact selected request is rejected by mandatory intake despite equivalent resolved Windows roots and matching digests. Decide canonical authoring serialization versus tested path-equivalence handling in a separately authorized owner task. Preserve the current packet; issue a new bound packet after any approved change. This input limitation is not repaired by the dev runtime proposal and cannot be silently waived.\n')
save('handoff.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'original_target_root': str(PROJECT / 'src/agents/skills/dev'), 'original_manifest': ref('source-manifest.json'), 'origin': ref('origin-record.json') if (ROOT / 'origin-record.json').exists() else None, 'proposed_spec': ref('revision-spec.md'), 'findings': ref('findings.json'), 'report': ref('validation-report.md'), 'selected_finding_ids': [], 'deferred_finding_ids': [state['new_finding_id'], state['prior_finding_id']], 'proposal_review_state': 'pending', 'review_instruction': 'Review the proposed mandatory literal-output correction REV-001 through REV-004 and separately resolve rejected handoff compatibility. No builder execution is currently authorized.', 'builder_readiness': 'BLOCKED', 'readiness_reasons': ['Selected manual handoff remains rejected; no accepted authored-family execution prerequisite established', 'Mandatory DV-17 failure requires a revised candidate and fresh validation; proposal awaits exact review'], 'baseline_kind': None, 'baseline_reference': None, 'adoption_required': False, 'adoption_capability': 'No adoption requested; do not infer a generated/adopted baseline from authoring artifacts or passing checks', 'permitted_target_root': str(PROJECT / 'src/agents/skills/dev'), 'preservation_requirements': ['No repair under this validation authorization', 'Preserve operational copies, original specifications, packet and all old evidence', 'Later builder limited to reviewed development-source change set', 'Separate fresh validator task after changed bytes'], 'target_package_digest': package})
save('checkpoint.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'assessment_finished': True, 'owned_running_jobs': [], 'remaining_required_coverage': ['Accepted manual handoff for DV-16', 'Fresh revised-candidate DV-17 and full required revalidation'], 'next_safe_action': 'Review proposed literal-output correction and separate handoff compatibility decision; no automatic repair', 'source_package_digest': package})
save('command-log.md', '# Execution accounting\n\nNative command receipts under commands/ contain actual argv, working directory, environment overrides, start/end, timeout, PID, exit and raw streams. Trials retain the predeclared prompt/plan plus before/after manifests. verification/commands/ holds separate validator checks. All seventeen extended CLI sessions exited normally; old 120-second timeouts and startup failure remain in the sealed first-native run. Existing grader regressions and initial bundle execution are copied under inputs/observations/ and inputs/bundle-attempt-001/. Script assembly uses actual hashes and explicit semantic adjudications; it does not fabricate model execution. Exact host tool invocations for auxiliary read-only inspection/assembly are retained in the conversation; no invented timing is assigned to them. The original Node before/after inventories were renamed with -manifest.json suffix only for legacy record classification, with bytes unchanged.\n')
print('REPORT', ROOT / 'validation-report.md')
print('PROPOSAL', ref('revision-spec.md'))
