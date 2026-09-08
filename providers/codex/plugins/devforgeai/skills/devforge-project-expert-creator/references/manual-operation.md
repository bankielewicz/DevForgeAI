# Manual expert workflow

The user initiates each skill and relevant command. These packages preserve implicit discovery but do not schedule each other. Creator authoring, evaluation, test operation and integration are distinct responsibilities. A user may authorize several responsibilities in one maintenance assignment; an author still cannot independently judge its own candidate.

## Artifact mapping

Use the creator's assets/skill-design-spec.md as the detailed design. XSPEC wraps or references its exact capability scope, authority, source/API versions, decisions and requirement sections. XPKG records the exact canonical and intended installed package maps, source provenance and candidate file manifest. Do not maintain a second independent design. The evaluator's validation-plan.json is the detailed EVPLAN content; verification-results.md, validation-results.json and decision.json are EVREPORT content. Standard envelope records link these exact artifacts where downstream consumers require XSPEC/XPKG/EVPLAN/EVREPORT. Preserve the repair specification and both producer handoffs. Never assign a document its own complete-byte digest.

Creator exit: candidate + design/XSPEC + XPKG + change record + prepared evaluator handoff. Receiving prompt: `Use $devforge-evaluate-expert. Read the supplied creator handoff; verify its exact candidate/specification references, preserve its scope and perform the authorized evaluation. Save results, a bounded repair specification and the creator handoff.`

Evaluator exit: EVPLAN + EVREPORT/evidence + repair specification + prepared creator handoff. Receiving prompt: `Use $devforge-project-expert-creator. Read the supplied evaluator handoff and bounded repair specification. Recheck the frozen candidate and findings; apply only authorized corrections to the selected canonical source, preserve unrelated behavior and old evidence, and prepare the next evaluator handoff.`

These prompts become concrete when the producer supplies its saved handoff path. Sending a recommendation, writing a receiver prompt or calling a reviewer is not actual user-mediated transfer. Each receiver must load the producer's real artifacts; record exact inputs, outputs, outcome, remaining work and next invocation. The creator never runs target evaluation or installation.

## Supported command boundaries

Use absolute paths. Resolve the evaluator root from its loaded SKILL.md; project/policy paths come from the actual assignment. Inspect the selected executable help before use.

| Owner/action | Command | Predicate/output and failure meaning |
| --- | --- | --- |
| Operator supplies project context | `devforge --project PROJECT --policy POLICY expert prepare` | Loads policy/project and returns grounding inputs. Invalid/missing input refuses; no phase completion proof. |
| Evaluator checks package | `python3 EVALUATOR/scripts/inspect_skill.py --skill-root PACKAGE --specification SPEC --mode source --output NEW/structure.json` | S001–S013 package predicates and exact manifest; installed checks use `--mode installed`. Does not execute candidate behavior. Exit 0 PASS; 1 findings; 2 unavailable/invalid input. |
| Evaluator reduces evidence | `python3 EVALUATOR/scripts/assess_evidence.py --plan PLAN --results RESULTS --output NEW/decision.json` | Checks planned coverage, evidence identity, freshness and declared judgments. Exit 0 scoped success; 1 required failure; 2 invalid/unavailable evidence. Advisory only; never protected admission or acceptance. |
| Integration owner binds a project expert | `devforge --project PROJECT --policy POLICY --expert RELATIVE_DIR expert bind` | Records exact policy/upstream/package hashes and history, not evaluation. Missing input/collision refuses. |
| Operator checks freshness | `devforge --project PROJECT --policy POLICY expert status` | MISSING/CURRENT/STALE, independently NOT_EVALUATED behavior. |
| Operator gates a project candidate | `devforge --project PROJECT --policy POLICY check` | Checks approved dependencies/layout/tooling and expert provenance. Does not check creator/evaluator phases or semantic adequacy. |
| Integration owner exports reviewed runtime files | `python3 INSTALLER --framework FRAMEWORK --provider codex --export-plugin NEW/devforgeai` | New destination only; omits evals/history/caches. Collision or unsupported component refuses. Export reports NOT_ACCEPTED_STAGING and is not operational adoption or native resource evidence. This permits isolated native-resource evaluation before final adoption. |
| Integration owner installs | `python3 INSTALLER --framework FRAMEWORK --provider codex --project PROJECT --manual-experts-only --manual-evidence ADOPTION_RECORD` | Refreshes only the two promoted Codex skills, preserving unrelated skills, agents, hooks and runtime inventories; enforces the manual evidence prerequisite and existing file collisions. Inspect overwrite/removal behavior first. Retire only identified obsolete prototypes after preserving their bytes. |

`INSTALLER` denotes the selected DevForge scripts/install_framework.py, not a packaged helper. Integration needs that trusted tool; the skills' own resources do not need the framework checkout. The installer refreshes managed files using recorded identities, removes only unchanged obsolete eval files, and does not automatically retire other old files or skill directories.

## Enforced requirements and gaps

Creator Intake/Selection/Design/Authoring/PreparedTransfer and evaluator W1/P1–P6/T01–T12 remain Enforced. Existing commands above implement their stated predicates only. They do not guard all actual manual authoring, receiving, native execution against phase/task evidence. Missing/stale/invalid package evidence prevents the corresponding helper verdict; semantic quality requires the separate independent review. Do not present either helper as universal enforcement.

The supported installer implements the manual-expert-adoption/v1 predicate for the two recognized Codex identities. It consumes --manual-evidence before writes: exact planned runtime manifest, creator five-phase evidence, evaluator fixed twelve-task coverage, original case assertion projection, plan/results/decision, separately assigned review and owner-selected acceptance. Missing, stale, invalid or insufficient evidence refuses operational installation; final preflight rechecks pins and prevents installation from invalidating its own evidence. This enforces an adoption prerequisite for all named Enforced phases/tasks; it is not phase-order interception, an editor restriction or automatic receiving enforcement. Actual semantic/native truth requires independent review and operator-observed evidence. Failure reporting and prepared repair handoffs remain possible. Do not simulate admission or use managed advance/resume/complete as fallback.

## Evaluation policy and environment

Read [accepted Routine/Full policy](contracts/skill-authoring-contract.md#accepted-vpr-2-validation-policy-for-manual-mode). Installation and the word validate do not force Full. Bounded maintenance requires an accepted baseline/scope, immediate and cumulative impact, compatibility and independent reviewed coverage. Consequential enforcement/transfer changes and first qualification require Full. Routine never moves a qualified anchor. Keep report completion, validation disposition, acceptance and installation separate.

Retain existing environment, create Git worktrees and static-only choices. Reuse settled choices. Preparation may proceed under its frozen bounded allocation before native readiness. Native work requires observed source/history/output boundaries and authorized authentication; no credential copying or global client-state changes. Static-only finishes reporting with unavailable native claims. Source-only evals preserve their IDs; record manual applicability and reasons without erasing original assertions. G8 funded automation stays deferred with its original defect.

The trust boundary is the operator-selected evidence and trusted installer. The installer does not authenticate a human decision from a name string or infer real native execution from JSON. An independent operator must preserve actual observations and select the final install-acceptance record; conditional authority from the original user task is carried forward without another routine approval. Synthetic gate fixtures never supply this operational evidence.
