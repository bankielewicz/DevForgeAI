# Skill authoring, packaging, and evaluation contract

Status: DRAFT MVP contract, revision 1, 2026-09-05 UTC. This defines the provider migration and subsequent authoring assignments. It does not certify the existing skills. Read it with the [artifact contract](artifact-contract.md) and [execution contract](execution-contract.md).

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
4. Export/install the exact candidate, perform tier C first, then tier B, then tier A. Failed installation blocks dependent runtime claims, while independent static authoring can continue.
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

## SKILL-001 decisions for the resumed pilot

**Sibling availability:** the migrated bundle contains draft brainstorm, project-expert-creator, develop, and review skills. define-product and change remain specified but absent. Tier-A negatives can pass the non-activation requirement independently of a routing target. Report suggested continuation, target discovery, and actual target invocation separately. If a target is absent, explain the capability gap and give a plain-language next task. Do not install a fake change stub to obtain a routing PASS. Observing an installed develop draft does not certify its implementation quality.

**Adoption:** test the same AI proposal with noncommittal feedback and explicit user adoption. Preserve the original AI attribution in both; only actual adoption supplies a decision reference. User-supplied early stack constraints are recorded faithfully as user decisions or stated preferences, with their scope. Brainstorm must not choose a stack itself, erase a user constraint, or require a later phase before recording what the user actually decided.

**B6 staleness:** an operator supplies preserved source bytes/revision and a newer conflicting file. The worker must identify the mismatch and avoid silently substituting it. Grade retained prior identities and the affected continuation, not a blanket requirement to stop all brainstorming.

**B7 ownership:** use an operator-authored session/assignment fixture in a disposable evaluation project that assigns the requested target to another synthetic owner. Give the evaluated worker a distinct identity, the requested write path, and the assignment; do not give it the expected answer. Record fixture provenance in the run manifest and hash the protected tree before/after. Expected result: stop dependent target writes and report the conflict without resetting/deleting work, changing branch, or choosing an unassigned escape path. Saving an evaluation report in an explicitly permitted outbox is allowed. This tests response to ownership evidence; it does not claim to test a live lease service or real simultaneous writers.

The actual Claude author gets a real operator-maintained worktree assignment distinct from the B7 fixture. The absence of a session record does not establish single-writer ownership. Bootstrap discussion can continue without a record; writes require observable assignment/user scope and collision checking. Do not fabricate a session ID or Git base; use null with missing_inputs for genuinely absent facts.

## Completion

The [roster](roster.md) remains the behavioral roadmap. Promote one bounded skill only for the provider, installation mode, and use cases supported by actual evidence. The immediate proof is SKILL-001 in both terminals, then SKILL-002 consuming its ledger. Neither the current migration nor this document completes that proof.

## Codex expert foundation manual selection

For promoted SKILL-007/008, the accepted September 8 Routine/Full policy governs manual evaluation: see the [portable policy](../../providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/contracts/skill-authoring-contract.md#accepted-vpr-2-validation-policy-for-manual-mode) and [record shapes](../../providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/manual-records.md). Source selection preserves 8ede26450ae737a5e928c5f70a945aa995969b30 and relevant policy material from 22e864951066c71a46873321f9bde2220aba653a; the implementation handoff records subsequent acceptance despite the preserved proposal's historical draft label.

All five creator phases and evaluator W1/P1–P6/T01–T12 remain Enforced. The supported installer gates operational adoption on current evidence for these obligations, including original case coverage, separate semantic review and actual owner-selected acceptance. This is an adoption prerequisite, not universal phase-order/editor/hook enforcement. Independent semantic and actual native observations remain required where selected.

The earlier `--runtime` and hook-merging requirements govern delivery-aware project installation. The separate Codex `--manual-experts-only --manual-evidence PATH` mode refreshes only these two promoted workflows through their adoption-evidence gate; it does not require `--runtime` or change installed agents, hooks or runtime inventories.

Routine may support a bounded accepted-scope update after complete selected checks, immediate/cumulative impact and compatible environment evidence, without claiming Full for new bytes. First qualification and consequential control/receiving changes require Full. The words validate, install and release do not alone select Full. User-initiated receiving transfers use real producer artifacts and observed receiver action; T12 merely prepares the evaluator's handoff and does not recursively qualify a receiver.

Automated receiver invocation, scheduling, background continuation and repair loops remain deferred. The G8 funded-launch defect, original assertions and frozen failures are preserved; automatic funded-launch accounting does not become a universal prerequisite for manual work. Export remains unaccepted staging for required pre-adoption native resource tests.


## Owner-approved local unqualified baseline

A distinct owner-selected local adoption claim is permitted for the exact manual-mode creator/evaluator packages after a predefined bounded acceptance set passes. Require deterministic package/resource checks, independent semantic review, representative actual creation/reuse/enhancement and missing-evidence behavior, both actual user-mediated handoffs, current source/runtime identities and owner acceptance. The supported installer records `LOCAL_ACCEPTANCE_SET_PASS` with `qualification_status: UNQUALIFIED`. This permission applies even when the candidate has changes that would require Full evidence for a qualification claim; it does not make those changes qualified.

All original creator phases and evaluator phases/tasks retain their Enforced classification and author/evaluator separation. The local installation gate measures its named acceptance set, not universal phase interception. Preserve all historical failures and leave the remaining qualification catalog NOT_RUN. Full qualification, its original assertions, controls, comparison arms and selection rules remain separate. An unqualified local baseline neither creates a qualified anchor nor automatically becomes a Routine acceptance chain. Conditional owner installation authority can be used after its actual conditions pass; no automatic orchestration or native launch is implied.
