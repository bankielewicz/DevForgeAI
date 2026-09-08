# Skill authoring, packaging, and evaluation contract

Status: DRAFT MVP contract with accepted VPR-2 policy transcription, revision 2, 2026-09-08 UTC. This defines the provider migration and subsequent authoring assignments. It does not certify the existing skills. Read it with the [artifact contract](artifact-contract.md) and [execution contract](execution-contract.md). The opt-in amendment below governs only explicitly selected Codex validator v2 assignments; earlier provider and brainstorm obligations remain in force elsewhere.

## Scope and sources

This contract applies to the 12 framework skills and to project-specific skills. A native creator or an operator can run this process before devforge-evaluate-expert itself is implemented. That bootstrap does not fabricate an evaluator invocation or add a thirteenth runtime skill.

The [Agent Skills specification](https://agentskills.io/specification) requires a skill directory and SKILL.md with name/description frontmatter. scripts, references, and assets are optional. Additional directories are permitted. Required evaluation evidence below is a DevForgeAI release convention, not an additional requirement of the open standard. Provider extensions and discovery behavior must be checked against the target client's documentation and observed runtime.

## Sources, ownership, and runtime copies

| Purpose | Canonical location |
| --- | --- |
| Claude framework skills | providers/claude/plugins/devforgeai/skills/SKILL-NAME/ |
| Codex framework skills | providers/codex/plugins/devforgeai/skills/SKILL-NAME/ |
| Claude plugin metadata and subagents | providers/claude/plugins/devforgeai/.claude-plugin/ and agents/ |
| Codex plugin metadata | providers/codex/plugins/devforgeai/.codex-plugin/ |
| Codex standalone subagent definitions | providers/codex/agents/*.toml |
| Per-skill Codex metadata, if needed | SKILL-NAME/agents/openai.yaml; this is not a subagent |
| Common specifications/templates | docs/mvp/ |
| Evaluation outputs | .poc/PROVIDER/SKILL-NAME-workspace/RUN-ID/ in the assigned evaluation root |

The old plugins/devforgeai authoring source is retired. The underlying skill format is portable; separate sources give these authors distinct ownership and independently tracked provider behavior. Never infer support from which model authored the text. Shared templates have one governing source; package-local copies must record and refresh their derivation when that source changes.

The companion installer selects the requested provider source without fallback. Normal project-local installation places skills in .agents/skills for Codex or .claude/skills for Claude and subagents in .codex/agents or .claude/agents. A provider source directory by itself is not a discovered installation.

The explicit --include-experts option still supports the two portable POC expert fixtures in project/experts/SKILL-NAME. It does not create provider-specific project experts or establish cross-provider behavioral support. A future project-expert assignment must specify its source/installation mapping; do not infer one from the portable fixtures.

## Per-skill structure and distribution

```text
SKILL-NAME/
  SKILL.md                    required; focused instructions and activation description
  references/                 conditional knowledge, procedures, version-specific examples
  assets/                     runtime output templates, schemas, images, data
  scripts/                    deterministic helpers when justified
  agents/openai.yaml          optional Codex metadata only
  evals/                      authored cases and fixtures, excluded from runtime export
    evals.json                output-quality requests and expectations
    fixtures/                 reproducible input files (files/ is also acceptable)
    triggers/                 positive/negative queries and fixed train/validation split
```

Create optional resources only when useful. Link them at the phase that needs them; do not load every reference by default. Keep project-specific expertise grounded in accepted constraints, verified version-specific APIs, real examples, and observed corrections. A newer library release is a proposal for a controlled refresh, not permission to replace an approved stack. Record source URLs, applicable versions, retrieval dates, claims supported, and refresh conditions in the package's provenance record.

**Packaging decision:** evals stays in authored source and is omitted from normal installed copies and runtime-only plugin exports. Fixtures must be reproducible from source, not solely available in an ignored workspace. A skill whose user-facing job is evaluation may need reusable evaluation instructions/templates in assets or references; those runtime resources do ship. They are distinct from the tests of that skill under evals.

Use the companion installer's --export-plugin option for native plugin testing. It builds a new directory named devforgeai containing that provider's manifest, skills/runtime resources, and supported agents. It never overwrites an existing export. Its current POC component support is deliberately limited to these components; it rejects unknown plugin components instead of silently omitting them. Run outputs, history, provenance sidecars, Python caches, and evals are not runtime inputs. Exports and project-local copies preserve content bytes; this POC does not preserve executable mode bits, so invoke helpers through their documented interpreter.

An old managed eval file is removed on refresh only when its recorded digest still matches. Local modifications cause a collision, including modifications to files scheduled for removal. Other retired files are not automatically deleted. A partial installation/export is not a passing result; preserve it for inspection and use a new export directory.

## Resource and script paths

References in SKILL.md are relative to the installed skill root. Shell working directories are not implied by Markdown links. Derive the installed root from the actual loaded SKILL.md path and resolve the consuming project's artifact root separately. Prefer an absolute script path and absolute project input/output paths in tool calls. Never hard-code a developer's home directory or depend on docs/mvp being reachable at runtime.

Helpers declare prerequisites, arguments, exit meanings, and bounded output. Provide --help where a script has a command interface; require no interactive prompts. Use the project's approved runtime and pinned dependencies when needed. A stdlib-only helper does not need a package manager. Report execution failures as failures/unavailability, never as successful structural checks. A placeholder/hash helper proves only those facts, not schema correctness, provenance semantics, or idea quality.

## Common authoring workflow

1. Recover the task, actual assignment, selected specification revision, relevant templates, and installed/provider constraints. Preserve the original baseline before edits.
2. Author only within the assigned skill/provider. Resolve substantive specification ambiguities with the integration owner; do not silently reinterpret accepted rules.
3. Define cases from requirements, keep fixtures reproducible, and establish separate candidate and baseline environments. Version expectations before the measured iteration. Diagnostic observations may motivate later tests; do not retroactively change criteria to convert a failed measured run into PASS.
4. Export/install the exact candidate, perform tier C first, then tier B, then tier A. For an explicitly selected VPR-2 validator assignment, apply the reviewed conditional coverage and dependencies below. Failed installation blocks dependent runtime claims, while independent static authoring can continue.
5. Record actual results, limitations, human feedback, and the package identity. A changed candidate, installed copy, source contract, test fixture, baseline, or relevant client configuration invalidates the affected earlier conclusion. Retain prior bytes/results and start a new iteration.
6. Hand the candidate and evidence to the integration owner. An author's grades support scoped review; they are not external acceptance authority. Recheck integrated bytes before adoption or release.

## Three separately reported evaluation tiers

| Tier | Test conditions | Evidence and limits |
| --- | --- | --- |
| A: discovery and activation | Actual installed package in a fresh target terminal. Separate explicit skill invocation, direct domain request, indirect requests, and negative/near-miss queries. | Record discovered/loaded identity and consultation traces. Ordinary implicit-test prompts must not supply the skill path or force its invocation. A direct domain request can say brainstorm without explicitly invoking a skill. |
| B: output quality and boundaries | Supplying the skill path is allowed. Same underlying raw facts and task for candidate and appropriate baseline, separate clean contexts and writable outputs. | Artifacts and requirement-based grades demonstrate behavior after loading, not implicit activation. Baseline labels are old_skill for a preserved previous version or without_skill for no skill. |
| C: installed resources and outputs | Actual exported/plugin or project-local installation in a consuming project where source docs are unavailable. | Templates/references/helper resolve inside the installed package; outputs land in the consuming project's map. A changed working directory alone does not prove source files were inaccessible. Record the isolation actually used. |

Do not blend A/B/C into one pass percentage. A source validator, explicit path-based subagent, or --version probe cannot establish tier A. An exported plugin and a project-local skill copy are different installation modes; identify which was tested. Avoid duplicate user/project/plugin installations that could activate a different copy.

Use realistic positive and near-miss negative trigger queries. For description optimization, preserve a fixed train/validation split and fresh final queries; do not put held-out expected answers into the author or task worker's context. Repeats and sample size should fit the declared time/subscription budget. A small pilot can report counts and limits without statistical claims. Capture token/time metrics only where actually observable.

Review any native creator harness before using it: record its revision, invocation/authentication mode, installed source selection, and how it observes consultation. A tool named run_loop.py is not automatically proof of native plugin discovery or an acceptable subscription-only execution path. Manual fresh terminal runs are a valid MVP method. No model API key or API-backed CI is required by this process.

Each run manifest records tier, provider, client/version/model, installation mode/path/file manifest, source candidate and baseline manifests, specification/case/fixture identities, context isolation, assignment, observed sibling availability, output/transcript locators, and actual outcomes. Use the [run template](templates/skill-authoring/run-manifest.json) and [report template](templates/skill-authoring/evaluation-report.md). Native evaluation files can use their tool's schema; the report binds those exact files as evidence rather than rewriting historical outputs.

NOT_RUN means planned but unattempted. COULD_NOT_RUN means a required observation could not be obtained with a recorded cause. NOT_APPLICABLE means excluded from the stated scope with a reason. A Claude-only evaluation can record Codex as NOT_APPLICABLE to its scope while overall Codex support remains NOT_EVALUATED. Preserve earlier reports' original labels and explain any later classification; do not rewrite their history.

## Opt-in VPR-2 validation policy

This section transcribes the owner-accepted [VPR-2 policy](../skill-authoring/proposals/validation-policy-v1-20260908/policy-revision.md) and [requirement diff](../skill-authoring/proposals/validation-policy-v1-20260908/requirement-diff.md) at DevForgeAI commit `8ede26450ae737a5e928c5f70a945aa995969b30`. Historical proposal labels and results stay unchanged. Policy acceptance authorizes this contract meaning; it does not establish runtime support, native qualification, funding or installation. The [execution contract](execution-contract.md#vpr-2-record-contract) freezes exact v2 record shapes, producer bindings and cross-version rules. The [validator design](../skill-authoring/skill-validator-design.md#vpr-2-accepted-policy-amendment--2026-09-08) freezes requirement-derived discriminators.

Only an external assignment selecting policy version `VPR-2`, its exact accepted source and a v2 delivery contract opts in. A v1 record, another provider, brainstorm or a generic request does not inherit conditional exclusions. Preserve every v1 predicate, including C/B/A ordering. A generic “validate” request is neutral: determine its actual claim, accepted baseline and scope, then select coverage. Resolve only consequential missing facts.

### Claims, selection and lineage

Select `Routine` for a bounded update to an identified owner-accepted baseline within its accepted capability/environment scope, with understood immediate and cumulative dependencies. Select `Full` for first or explicit qualification, a new supported capability/environment, consequential control/authority/enforcement/receiving semantics, a release/support contract requiring Full, or remaining unbounded impact. Adoption, installation, tagging and distribution inside an already accepted scope do not alone select Full. Record the requested claim in its actual words and its qualification requirement.

Routine PASS means the selected update meets complete current required evidence under that coverage. It may support scoped owner acceptance and installation when destination, exact bytes, effective controls and applicable post-install identity/resource/compatibility checks are bound and complete. Carried conditional owner authority can cover this; no per-check approval ceremony is required. A mismatch blocks affected use under the existing recovery arrangement. A Routine result never grants owner authority or qualifies new bytes. Full PASS means complete applicable assertion coverage for the exact candidate/environment, including actual native obligations and receiving transfer; release and human acceptance remain distinct.

Keep `current_routinely_accepted` separate from `qualified_anchor`. The latter is the last fully qualified candidate/environment with its evidence, or explicitly `ABSENT`/`UNKNOWN`. Routine never advances it. If no qualified anchor exists, bind the explicitly accepted unqualified baseline; preserve the missing qualification. Every update binds its immediate diff from the current accepted candidate and cumulative diff from the qualified anchor or that unqualified baseline, including effective configuration, installation and provider/client behavior. Review the union of affected requirements and transitive dependencies across both diffs. The acceptance chain cannot reset the anchor, erase a failure, or manufacture qualification. There is no fixed number of Routine edits after which Full becomes mandatory; unresolved consequential cumulative interaction is the trigger.

### Enforced tasks and reviewed conditional coverage

W1, P1–P6 and T01–T12 remain `Enforced`. Each task records its obligation disposition separately from observations. Native observations excluded by accepted Routine selection remain `NOT_RUN`; only a genuine scope exclusion may be `NOT_APPLICABLE`. Neither is native PASS. Accurate reporting may complete P5/P6 with failed or unavailable evidence.

| Tasks | Required obligation |
| --- | --- |
| T01–T02 | Bind external authority, policy, actual claim, accepted base/scope, candidate/environment, lineage, both diffs, dependency closure and frozen evidence selection. Full accounts for every applicable original assertion. |
| T03 | Preserve all applicable S001–S013 checks and affected deterministic regressions; source checks do not establish installed behavior. |
| T04 | Obtain one actual fresh independent AI review of selection, affected/dependent clauses and all R01–R10 invariants. Full reviews all applicable anchors. Retain separate criterion judgments and observed independence limits; no reviewer per criterion is required. |
| T05 | Complete the selected preparation/readiness obligation. A reviewed no-native selection records no-native disposition, without fabricating a native plan, boundary evidence or launch. The separately authorized workspace preparation branch remains available before native choices are complete. |
| T06–T08 | Record C/B/A observations or exact reviewed conditional/dependency dispositions. Every selected native behavior needs matching installed C and actual readiness. |
| T09 | Adjudicate candidate outcomes, required comparisons, coverage, freshness, compatibility and cumulative lineage. Full target receiving evidence must already exist. |
| T10–T12 | Save honest results, bounded repairs/enhancements and a prepared handoff. Report completion, suitability, owner acceptance, qualification and receiving invocation separately. |

T04 must be selected by the external owner, independent of the author/measured workers, and bind the frozen plan and actual reviewed bytes. A self-declared reviewer or a hash alone does not establish independence or adequate judgment. Missing applicable invariant context remains unavailable. Review selection once at this boundary; do not add per-row approval or recursive review chains.

Selected C failure, missing evidence or stale identity blocks dependent B/A. Under v2 Routine only, a pre-run T04-reviewed `NOT_SELECTED` B disposition permits selected A after matching C. It is never B PASS; an observed selected B failure cannot be relabeled as unselected. An intact B quality FAIL can remain an observed comparison while later independently permissible collection proceeds; candidate suitability still fails for a required candidate violation. Full retains required C/B/A ordering. Later observations cannot repair an earlier admission retroactively.

### Impact and compatibility union

Take every matching CI rule across immediate and cumulative changes, plus all affected regressions and negative branches. Cost targets do not choose applicability.

| Rule | Trigger | Required evidence or disposition |
| --- | --- | --- |
| CI-01 | Spelling/layout/commentary without semantic, metadata, resolution or output-contract change | Applicable D checks and focused independent S review; no native work unless semantic impact is found. |
| CI-02 | Trigger/invocation/selection exposure | Matching C and affected explicit/direct/indirect/near-miss A including adjacent negatives; B when promised behavior changes. |
| CI-03 | Resources/dependencies/helpers/templates/package/output destinations | D resolution/identity/regressions, affected actual installed C and downstream B; A if discovery changes; CI-06 if transfer meaning changes. |
| CI-04 | Bounded workflow/prompt/clarification/quality/failure behavior | C and affected normal/edge/negative B/prior failures; matched candidate/baseline arms for behavior change or a comparative claim; A for selection impact. |
| CI-05 | Consequential authority/permission/trust/enforcement/gate/evidence authenticity | Full before adoption of the changed contract, D denial/identity tests, S meaning review and representative actual native controls. |
| CI-06 | Receiving prerequisites/output meaning/receipt authority/transfer/completion | Full before adoption, producer/consumer contract checks and actual eligible target-to-receiver transfer/failures. Unchanged prose spelling follows CI-01. |
| CI-07 | Client/provider/installation/configuration | Apply CP-01–CP-04 to used capabilities. Names/version strings establish neither compatibility nor incompatibility. |
| CI-08 | Requirement/case/oracle/grading meaning | Explicit specification decision before use; new revision and affected assertion reevaluation; preserve originals and historical outcomes. |
| CI-09 | Unbounded impact/unresolved cumulative interaction | Full or insufficient evidence; no Routine adoption for the affected unbounded claim. |

| Rule | Bound compatibility obligation |
| --- | --- |
| CP-01 | Pin old/new client/provider/installer and effective configuration, applicable official change information/local source evidence, used capabilities, changed/unknown dependencies and affected assertions. Identical relevant bytes are not a behavioral change. |
| CP-02 | Observe affected schema/install/resource/parser/control mechanics and negative inputs using deterministic checks. Documentation and a version probe are insufficient native evidence. |
| CP-03 | Changed executable/provider/installer: observe exact-installed load and a completed bounded task, plus each affected control/selection denial, failure or activation probe. Add paired B for possible provider/model output-quality change; retain source visibility, capture completeness and effective differences. |
| CP-04 | Routine is eligible only for evidenced equivalence within accepted used-capability scope with unchanged trust/control/transfer meaning. New unsupported scope, consequential meaning or remaining unbounded impact selects Full. Unknown changed components stay unresolved. |

Unchanged components may reuse exact fresh evidence with a stated scope. Do not run every compatibility permutation. A post-install check may share an actual load/task observation only when its conditions, identities, timing and required outputs match.

### Assertion evidence, receiving and results

`D` is deterministic mechanical evidence, `S` independent semantic judgment, and `N` actual native observation. D tests of native evidence admission do not supply N. Full completeness means every original applicable case/assertion/variant has its required evidence kinds and independent per-arm/assertion judgment. Preserve all original catalogs, S001–S013, R01–R10 and historical outcomes. No optimized Full call total exists until its complete reviewed observation map exists.

One raw observation can serve compatible assertions only with matching candidate/environment/input, prompt and forcing conditions, arm, visibility, time/freshness and prerequisite order. Disclose shared sample counts and correlation. Opposite arms, incompatible variants and forced-versus-implicit prompts remain distinct. One independent bounded paired/batch grade may assess complete actual raw outputs, retaining each arm/assertion judgment, neutral labels where possible and order/arm leakage. Baseline quality FAIL may complete an intact comparison; absent/mismatched baseline evidence cannot. The pair summary never overwrites candidate judgment. A child-output grade and parent interpretation remain distinct assertions, without a recursive grader campaign.

Validator self-evaluation keeps every explicitly native outer/inner source assertion, including SV-009, SV-012 and SV-024–SV-028 and representative actual nested review/return/failure/receiving integration. A generic validation subtask does not automatically invoke a 17-case inner Full suite. Real compatible bundles may support adjudication assertions; synthetic bundles support only explicitly synthetic/mechanical/error handling assertions, never clean native negatives, installed resources, isolation, callback origin, nested execution or receiving.

Full T09 consumes eligible output actually produced by the measured target, observed receiver loading, and the required completed receiver action or expected negative disposition under the receiving contract. Record evidence before adjudication. The evaluator's own prepared T12 handoff does not invoke or recursively qualify another evaluator. Receipt creation, publication/readback and actual receiver invocation remain separate facts.

Required candidate/protocol FAIL yields `FAIL`; otherwise any required missing/unavailable evidence prevents PASS and yields `INSUFFICIENT_EVIDENCE`. With all required evidence complete and current, select `ROUTINE_PASS` or `FULL_PASS` according to the admitted mode. A complete honest report can carry any of those dispositions. Helpers advise; they do not authenticate observations, grant acceptance or publish protected receipts.

Authentication lifecycle reuse is conceptually separate from independent native evidence state. Supported cached authentication need not mean one login per generation, but credential copying, writable history reuse or unproved global-state isolation is not authorized. Native authentication/transport implementation remains unresolved and outside this amendment's engineering grant.

## SKILL-001 decisions for the resumed pilot

**Sibling availability:** the migrated bundle contains draft brainstorm, project-expert-creator, develop, and review skills. define-product and change remain specified but absent. Tier-A negatives can pass the non-activation requirement independently of a routing target. Report suggested continuation, target discovery, and actual target invocation separately. If a target is absent, explain the capability gap and give a plain-language next task. Do not install a fake change stub to obtain a routing PASS. Observing an installed develop draft does not certify its implementation quality.

**Adoption:** test the same AI proposal with noncommittal feedback and explicit user adoption. Preserve the original AI attribution in both; only actual adoption supplies a decision reference. User-supplied early stack constraints are recorded faithfully as user decisions or stated preferences, with their scope. Brainstorm must not choose a stack itself, erase a user constraint, or require a later phase before recording what the user actually decided.

**B6 staleness:** an operator supplies preserved source bytes/revision and a newer conflicting file. The worker must identify the mismatch and avoid silently substituting it. Grade retained prior identities and the affected continuation, not a blanket requirement to stop all brainstorming.

**B7 ownership:** use an operator-authored session/assignment fixture in a disposable evaluation project that assigns the requested target to another synthetic owner. Give the evaluated worker a distinct identity, the requested write path, and the assignment; do not give it the expected answer. Record fixture provenance in the run manifest and hash the protected tree before/after. Expected result: stop dependent target writes and report the conflict without resetting/deleting work, changing branch, or choosing an unassigned escape path. Saving an evaluation report in an explicitly permitted outbox is allowed. This tests response to ownership evidence; it does not claim to test a live lease service or real simultaneous writers.

The actual Claude author gets a real operator-maintained worktree assignment distinct from the B7 fixture. The absence of a session record does not establish single-writer ownership. Bootstrap discussion can continue without a record; writes require observable assignment/user scope and collision checking. Do not fabricate a session ID or Git base; use null with missing_inputs for genuinely absent facts.

## Completion

The [roster](roster.md) remains the behavioral roadmap. Promote one bounded skill only for the provider, installation mode, and use cases supported by actual evidence. The immediate proof is SKILL-001 in both terminals, then SKILL-002 consuming its ledger. Neither the current migration nor this document completes that proof.
