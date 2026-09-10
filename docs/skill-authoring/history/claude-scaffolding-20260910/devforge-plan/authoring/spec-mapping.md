# SKILL-006 → devforge-plan coverage map

Governing specification: `docs/mvp/specifications/skill-006-devforge-plan.md`, DRAFT revision 2,
refreshed 2026-09-05 UTC, SHA-256 `149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b`
(verified before authoring).

Package paths are relative to `providers/claude/plugins/devforgeai/skills/devforge-plan/`. Eval case IDs
are `evals/evals.json` `id` values (tier B), `evals/cases.jsonl` `case_id` values (deterministic and
routed rows), and `evals/triggers/trigger-queries.json` `category` values (tier A).

This map records where each requirement was addressed. It is not evidence that the address is correct,
and no case in it has been run.

## User goal and use-case inventory

| Specification row | Where it landed | Eval coverage |
| --- | --- | --- |
| User goal — dependency-ordered epics and bounded stories with traceable acceptance criteria and the expertise each story needs | `SKILL.md` title, opening, and phases 2 and 3 | evals id 0; cases `PL-B-001`, `PL-C-001`, `PL-C-002` |
| Direct request — "Use DevForgeAI to turn this product brief into epics and stories" | `SKILL.md` frontmatter `description`, direct-domain phrasing | triggers `direct_domain` T2a–T2e; evals id 0 |
| Indirect request — "What should we implement first, and what does done mean for each change?" | `SKILL.md` `description`, indirect phrasing; phase 4 readiness reading | triggers `indirect` T3a–T3g; evals id 1; case `PL-B-002` |
| Expected result — epic; story plus a standardized handoff | `SKILL.md` **Outputs** table; `assets/epic.md`, `assets/story.md`, `assets/handoff.md` | cases `PL-C-001`, `PL-C-002`, `PL-C-003`; `PL-PKG-002` A1–A3 |
| Required context — adopted requirements and architecture, relevant accepted design, experiment dispositions, existing backlog | `SKILL.md` **Required inputs** table; `references/upstream-resolution.md` §"Resolve before you partition" | evals ids 0, 1, 9; fixtures `shared/`, `backlog/` |
| Plugin capability — skill and local templates; deterministic graph and provenance checks belong to DevForge; no sprint scheduler or issue-tracker integration | `SKILL.md` §"What this skill owns and what it does not"; `references/readiness-check.md` §"What this check actually is"; design spec §6 routes R1–R3 | evals id 1 graded observation on sprint invention; case `PL-B-002` A2 |
| State/action boundary — may propose missing behavior but cannot silently add requirements, broaden permissions or rewrite the stack; sprint grouping optional | `SKILL.md` §"Decisions, proposals, and what you may not do"; phase 2 sprint paragraph | evals ids 2, 3; cases `PL-B-003`, `PL-B-004` |
| MVP support decision — required for a delivery slice; revises affected stories without regenerating an entire backlog | `SKILL.md` §"Decisions, proposals…" amendment paragraph; `references/upstream-resolution.md` §"Revising rather than regenerating" | evals id 9; case `PL-B-008` |
| Does not activate for — execute a ready story belongs to develop; product value belongs to define-product | `SKILL.md` `description` exclusions naming `devforge-develop` and `devforge-define-product`; design spec §2 table | triggers `negative_execute_ready_story` T4a–T4b, `negative_product_value` T5a–T5c |

## Shared authoring requirements

| Specification row | Where it landed |
| --- | --- |
| Use the skill authoring contract for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, separate A/B/C results | Canonical source under `providers/claude/…`; `references/derivation.json` `packaging` block; `evals/fixtures/` reproducible from source; `evals/evals.json` tier note and `evals/triggers/…` tier-A note keep the tiers separate |
| Original instructions need alignment; existence is not evidence of conformance | No prior instructions existed — `package-index.json` records SKILL-006 Claude as `NOT_IMPLEMENTED` with a null source. Recorded in design spec §9 search table |

## Inputs and provenance

| Input row | Where it landed | Eval coverage |
| --- | --- | --- |
| `product-brief` — required; consume selected requirement IDs and delivery non-goals | `SKILL.md` inputs table row 1; phase 1 | fixture `shared/PROD-001.md`; evals ids 0, 2, 3 |
| `architecture-contract` — required for production stories; consume rule IDs, test policy, source roots, capability requirements | `SKILL.md` inputs table row 2; phase 3 scope and expertise paragraphs | fixture `shared/ARCH-001.md`; evals ids 0, 2, 10 |
| `design-spec` or `prototype-report` — conditional; consume relevant flows, states, observations, hardening disposition | `SKILL.md` inputs table row 3; `references/recording-rules.md` §"Proposals, decisions and status" final paragraph | fixture `shared/UX-001.md` (`status: proposed`); evals id 0 graded observation 6 |
| Existing epics/stories and change-request — conditional; consume dependencies, completed work, accepted amendment | `SKILL.md` inputs table row 4 | fixtures `backlog/`; evals ids 1, 9; cases `PL-B-002`, `PL-B-008` |
| Artifact contract — exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` §"The envelope" and §"Identity and digests" | cases `PL-C-003` A2 (cited digests still describe the bytes), `PL-C-005` A3 |
| A proposed source cannot become an accepted production constraint by being copied downstream | `SKILL.md` inputs section closing paragraph; `references/recording-rules.md` §"Proposals, decisions and status" | fixture `shared/UX-001.md`; evals id 0 |
| Reuse valid current artifacts rather than replaying every earlier phase | `SKILL.md` phase 1 "Recover what already exists first"; `references/upstream-resolution.md` §"Revising rather than regenerating" | evals id 9 |
| Execution contract — every writing session has an owner and fence; concurrent writers use distinct worktrees and branches; a shared worktree is not a concurrency mechanism | `SKILL.md` §"When something is missing or a check cannot run" collision bullet; `references/readiness-check.md` §"When another writer owns the destination" | fixture `collision/SESSION-042.md`; evals id 5; case `PL-B-006` |

## Workflow and phase exits

| Phase | Work | Exit condition | Where it landed | Eval coverage |
| --- | --- | --- | --- | --- |
| 1. Select | Identify the delivery outcome and exact accepted source revisions | Scope and non-goals are traceable | `SKILL.md` §"1. Select" with a stated **Exit**; `references/upstream-resolution.md` | evals id 0; case `PL-B-001` |
| 2. Partition | Outcome-oriented epics and small, independently checkable stories | Each story has a useful outcome and explicit dependencies | `SKILL.md` §"2. Partition" with a stated **Exit** | evals ids 0, 1; case `PL-C-001` A2 |
| 3. Specify | Behavioural acceptance criteria, negative cases, write scope, test policy, expertise needs; only relevant excerpts | A developer can identify what to change, how to verify it, and what not to infer | `SKILL.md` §"3. Specify" with a stated **Exit**; `references/upstream-resolution.md` §"The bounded context packet" | evals ids 2, 3, 10; cases `PL-C-002` A2–A3 |
| 4. Check readiness | Coverage, cycles, unresolved decisions, source freshness, capability gaps | Separate ready from blocked without pretending a missing expert exists | `SKILL.md` §"4. Check readiness" with a stated **Exit**; `references/readiness-check.md` §"The five readings" and §"Separating ready from blocked" | evals ids 7, 8, 10; cases `PL-B-007`, `PL-B-009`, `PL-C-004` |
| These phases are the skill's workflow, not new CLI subcommands | — | — | `SKILL.md` §"What this skill owns and what it does not"; `references/readiness-check.md` opening | case `PL-B-007` A2 |
| Only documented, implemented DevForge commands may be named as executable gates | — | — | `SKILL.md` names **no** DevForge command as a planning gate and states the missing integration; `references/readiness-check.md` records the observed command surface and what `devforge check` actually checks | — |
| On interruption, preserve the current phase and evidence; resume by checking identities and the session assignment again | — | — | `assets/handoff.md` §"Resume and custody" (invalidating conditions, worktree disposition); `references/upstream-resolution.md` §"When a cited revision no longer matches" | — |

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template | Where it landed | Eval coverage |
| --- | --- | --- | --- | --- | --- |
| epic | EPIC | Outcome, requirement coverage, ordered story membership, explicit deferred scope | `templates/devforge-plan/epic.md` | `assets/epic.md` — exact copy, digest `48f8b069…` verified equal to the governing source | `PL-C-001`; fixture `good/EPIC-001.md` |
| story | STORY | Observable acceptance cases, relevant rule references, bounded scope, dependencies, required expert capabilities | `templates/devforge-plan/story.md` | `assets/story.md` — exact copy, digest `a19ccd7f…` verified equal | `PL-C-002`; fixture `good/STORY-001.md` |
| handoff with output identities, observed checks, unresolved decisions, next owner, one copyable task prompt | HANDOFF | — | `templates/shared/handoff.md` | `assets/handoff.md` — bounded adaptation recorded in `references/derivation.json` | `PL-C-003`; fixture `good/HANDOFF-001.md` |
| Consumer coverage — epic → plan, review, release, change; story → project-expert-creator, evaluate-expert, develop, review, release, change | — | — | — | `SKILL.md` **Outputs** section closing paragraph, with the caution that most consumers are unimplemented | evals id 10 |
| Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions | — | — | — | `SKILL.md` §"What this skill owns…" final paragraph; `assets/handoff.md` closing line | evals id 4 |

## Validation and behavioral acceptance

| Case | Required observation | Where the behaviour is instructed | Eval case IDs |
| --- | --- | --- | --- |
| Direct activation | Produces linked epic and story documents | `SKILL.md` phases 1–3 and Outputs | evals id 0; `PL-B-001`; triggers `direct_domain` |
| Indirect activation | Uses dependencies and readiness rather than inventing a sprint requirement | `SKILL.md` phase 2 sprint paragraph; phase 4 | evals id 1; `PL-B-002`; triggers `indirect` |
| Missing behavior | Marks the dependent acceptance criterion unresolved and routes clarification | `SKILL.md` phase 3 paragraph 2; `references/readiness-check.md` §"Unresolved decisions" | evals id 2; `PL-B-003` |
| Traceability | Identifies an unsupported criterion as a new proposal, not an inherited requirement | `SKILL.md` phase 3 paragraph 1 and §"Decisions, proposals…"; `references/recording-rules.md` §"Proposals, decisions and status" | evals id 3; `PL-B-004` |
| Out of scope | Routes to brainstorm or define-product | `SKILL.md` `description` exclusions; §"Stopping" | evals id 4; `PL-B-005`; triggers `negative_unscoped_exploration` |

## Additional common cases

| Case | Required behaviour | Where it landed | Eval case IDs |
| --- | --- | --- | --- |
| A concurrent writer claims this session's worktree or branch | Stop dependent writes and report the collision without deleting or resetting anyone's work | `SKILL.md` error list bullet 3; `references/readiness-check.md` §"When another writer owns the destination" | evals id 5; `PL-B-006`; fixture `collision/SESSION-042.md` |
| A relevant upstream revision, installed skill, base commit or candidate changes | Mark the applicable prior evidence stale and route a new check or run | `SKILL.md` error list bullet 2; `references/upstream-resolution.md` §"When a cited revision no longer matches" | evals id 6; `PL-C-005`; fixtures `stale-upstream/` |
| A template placeholder remains in a required result field | The result stays a draft and cannot be presented as ready | `SKILL.md` phase 4 placeholder paragraph and error list bullet 4; `references/recording-rules.md` §"Placeholders and missing facts" | evals id 7; `PL-C-004`; fixture `draft-placeholder/STORY-009.md` |
| A requested check cannot execute | Record COULD_NOT_RUN and its actual cause; absence of an error is not PASS | `SKILL.md` error list bullet 5 and the vocabulary paragraph; `references/readiness-check.md` §"When a check cannot run" | evals id 8; `PL-B-007`; fixture `could-not-run/STORY-007.md` |
| Acceptance requires real outputs from representative requests in each terminal for which support is claimed | Not satisfied by authoring | No terminal support is claimed. Tiers A, B and C are `NOT_RUN`; recorded in `evals/*.json` status notes, the design spec's evaluation-coverage section and the authoring handoff | — |

## Rework, stopping, and recovery

| Specification statement | Where it landed | Eval coverage |
| --- | --- | --- |
| Story defects return here; product or architecture contradictions route through change to their owner | `SKILL.md` §"Decisions, proposals…" paragraph 2; `references/readiness-check.md` §"Stop and hand back when" | evals id 9 |
| Revisions preserve prior acceptance criteria and invalidate affected downstream evidence | `SKILL.md` amendment paragraph; `references/upstream-resolution.md` §"Revising rather than regenerating" | evals id 9 artifact assertions; `PL-B-008` |
| Stop when a story cannot be implementation-ready with unresolved acceptance behaviour, stale governing inputs, dependency cycles, or required missing expertise | `SKILL.md` §"Stopping"; `references/readiness-check.md` §"Stop and hand back when" | evals ids 2, 6, 10 |
| Preserve accepted versions and observed failures; do not force-unlock, overwrite another session's result, change external gates, or retry indefinitely | `SKILL.md` collision bullet; `references/readiness-check.md` §"When another writer owns the destination"; `references/recording-rules.md` §"Identity and digests" preservation rule | evals id 5 |
| If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming | `assets/handoff.md` §"Resume and custody" invalidating conditions | — |
| Report missing observations precisely | `SKILL.md` fixed-vocabulary paragraph; `references/recording-rules.md` §"Result vocabulary" | evals id 8 artifact assertions |

## Native creator authoring prompt

| Specification instruction | What was actually done |
| --- | --- |
| "Use the available native skill creator with the following task" | No Claude native skill-creator skill was installed or invoked. The assignment named the Claude `devforge-project-expert-creator` package at commit `4999f31` as the builder to follow; it was **source-loaded** — read by absolute path and followed as instructions — not installed and not invoked as a skill. Recorded in `references/derivation.json` `authoring_route` and in `authoring-notes.md`, per the authoring contract's requirement to record whether the assigned creator instructions were actually used. |
| Use the operator-supplied worktree, provider, write fence and base | Worktree `claude-scaffold-plan-20260910`, branch `author/claude-devforge-plan-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c` verified before writing; fence limited to the package and this authoring directory |
| Read skill-authoring-contract.md at the selected revision | Read at digest `371462385b4e…`; recorded in the design spec §10 |
| Read this specification, its named templates, and only the relevant sections of the shared contracts | Done; sections used are recorded per derivation entry |
| Output: a focused skill in the assigned provider source, its needed runtime resources, reproducible eval cases/fixtures, separate A/B/C observations | Package authored; fixtures reproducible from source; A/B/C kept separate and all `NOT_RUN` |
| Record the real installation mode and candidate/baseline identities | Installation mode: **none**. Candidate identity: `file-manifest.json`. Baseline: none exists — `without_skill` for every tier-B case |
| Do not claim implicit activation from a run explicitly supplied SKILL.md | No activation of any kind is claimed. Tier-B cases carry an explicit `activation_claim` of NONE where the distinction is easy to blur |
| Copy needed templates into the package and use package-relative references | Three templates copied into `assets/`; every link in the package is package-relative and no path reaches `docs/mvp` |

## Completion handoff

| Specification statement | Where it landed |
| --- | --- |
| "You are here: Derive epics and implementable stories" | `SKILL.md` title and opening |
| Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit | `SKILL.md` §"Stopping"; `assets/handoff.md` continuation directory and copyable next task |
| A document's accepted status and an external gate's passing result are separate facts | `references/recording-rules.md` §"Proposals, decisions and status" and §"Result vocabulary"; `assets/handoff.md` Observed verification note |

## Requirements deliberately not implemented in the package

| Requirement | Why, and where it is recorded |
| --- | --- |
| Deterministic graph and provenance checks belonging to DevForge | Not implemented in the CLI at this revision. Recorded as enforcement routes R1, R2 and R3 in the design spec §6 with status "Enforcement requested; not confirmed available", routed to the integration owner. `SKILL.md` and `references/readiness-check.md` name the missing integration instead of describing a gate. |
| Sprint scheduler or issue-tracker integration | The specification excludes both from the MVP. `SKILL.md` phase 2 states sprint grouping is optional and only on request. |
| Terminal acceptance evidence | Requires a run. Tiers A, B and C are `NOT_RUN`; no installation exists. |
| `package-index.json` status update for SKILL-006 | Outside the assignment's fence. Recorded as a coordinator item in `authoring-notes.md` and the authoring handoff. |
