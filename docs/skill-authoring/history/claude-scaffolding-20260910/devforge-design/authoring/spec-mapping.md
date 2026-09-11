# Specification mapping: SKILL-003 to the devforge-design package

Governing source: `docs/mvp/specifications/skill-003-devforge-design.md` at revision `c17e758417da64928a0f47fc2600304465ac3f3c`, SHA-256 `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb` (re-computed during authoring; matches the digest the assignment declared).

Package paths are relative to `providers/claude/plugins/devforgeai/skills/devforge-design/`. Eval case IDs refer to `evals/evals.json` (numeric `id`) and `evals/cases.jsonl` (`case_id`).

This table records where each requirement was addressed. **It is not evidence that any of it works.** Every eval outcome is `NOT_RUN`.

## User goal and use-case inventory

| Spec row | Where addressed | Eval case |
| --- | --- | --- |
| User goal: make selected requirements reviewable as journeys, screen states and local mockups before committing to implementation behaviour | `SKILL.md` opening and phases 1-3 | 2, 3 (`DX-B-002`, `DX-B-003`) |
| Direct request: "Use DevForgeAI to design mockups for this MVP" | `SKILL.md` description; `evals/triggers/trigger-queries.json` `A2a` (verbatim) | 2 (`DX-B-002`); trigger `A2a` |
| Indirect request: "Show how a customer would complete signup, including errors and empty states" | `SKILL.md` description; trigger `A3a` (verbatim) | 3 (`DX-B-003`); trigger `A3a` |
| Expected result: design-spec plus a standardized handoff | `SKILL.md` "Outputs"; `assets/design-spec.md`; `assets/handoff.md` | 1, 2 (`DX-C-001`, `DX-B-002`) |
| Required context: accepted requirements, existing UI conventions, target device constraints, prior user feedback | `SKILL.md` "Required and optional inputs" table (last three rows added from this line) | 2, 5 (`DX-B-002`, `DX-B-005`) |
| Plugin capability: skill and local files; browser tools may help; generated imagery and MCP UI are optional | `references/mockups-and-preview.md` "What to build"; no tool dependency is declared and no `allowed-tools` is used | 4 (`DX-B-004`) |
| State/action boundary: a declared local design directory; a mockup does not establish backend functionality, accessibility conformance or production readiness | `SKILL.md` "Where the artifacts go" (declared design directory) and opening framing; `references/mockups-and-preview.md` "What a mockup does not establish" | 4 (`DX-B-004`) |
| MVP support decision: conditional for UI or interaction changes; pure backend stories can record why design is not applicable | `SKILL.md` phase 1 and "Stopping" (the recorded not-applicable result) | 6 (`DX-B-006`) |
| Does not activate for: technical uncertainty needing execution belongs to prototype; a production patch belongs to develop | `SKILL.md` description (both named); trigger negatives `A5a`, `A5b` (prototype) and `A6a`, `A6b` (develop) | triggers `A5a`, `A5b`, `A6a`, `A6b` |

Author's addition beyond the specification, recorded as a proposal: `devforge-define-product` and `devforge-change` are also named as near-miss owners (roster provenance flow), and non-UI "design" - schema, API, class structure, pattern, system design - is excluded by name. Triggers `A4a`-`A4d`, `A7a`, `A7b`.

## Shared authoring requirements

| Spec statement | Where addressed |
| --- | --- |
| Use the skill-authoring contract for provider source ownership, runtime packaging, scripts, reproducible eval fixtures and separate A/B/C results | Package lives under the Claude canonical source path; `evals/` is source-only; no `scripts/`; fixtures are reproducible from source; `evals/evals.json` `tier_note` keeps tiers separate; `references/derivation.json` records every copy |
| Existence of prior instructions is not evidence of conformance | No prior `devforge-design` existed; recorded in `design/skill-design-spec.md` section 9 |

## Inputs and provenance

| Spec input | Requirement | Where addressed | Eval case |
| --- | --- | --- | --- |
| product-brief | Required | `SKILL.md` inputs table; the no-product-brief default in `SKILL.md` and `references/recording-rules.md` | 2 (`DX-B-002`) |
| architecture-contract | Optional; do not invent a replacement | `SKILL.md` inputs table ("Do not invent a replacement"); `references/mockups-and-preview.md` "Using the project's conventions" | 5 (`DX-B-005`) |
| design-spec (existing) | Optional | `SKILL.md` inputs table; `references/recording-rules.md` `supersedes` guidance | 8 (`DX-B-008`) |
| prototype-report or change-request | Conditional | `SKILL.md` inputs table; phase 4 | 8 (`DX-B-008`) |
| Artifact contract: exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` "The envelope", "Upstream references", "Ordering" | 2, 8 (`DX-B-002`, `DX-B-008`) |
| A proposed source cannot become an accepted production constraint by being copied downstream | `SKILL.md` "Decisions versus proposals"; `references/recording-rules.md` adoption-authority paragraph | 8 (`DX-B-008`) |
| For an established project, reuse valid current artifacts rather than replaying every earlier phase | `SKILL.md` phase 1 ("Read before asking") | 5 (`DX-B-005`) |
| Execution contract: every writing session has an owner and fence; concurrent writers use distinct worktrees and branches; a shared worktree is not a concurrency mechanism | `SKILL.md` "Where the artifacts go" and the concurrent-writer bullet | 7 (`DX-B-007`) |
| Session template records the authority-selected assignment | `references/recording-rules.md` `execution_ref` row (null plus `missing_inputs` when absent) | 7 (`DX-B-007`) |

## Workflow and phase exits

| Spec phase | Exit condition | Where addressed | Eval case |
| --- | --- | --- | --- |
| 1. Frame | Design scope and missing decisions are explicit | `SKILL.md` "1. Frame", exit line | 2, 6 (`DX-B-002`, `DX-B-006`) |
| 2. Model | The flow covers the meaningful success and failure paths | `SKILL.md` "2. Model", exit line | 3 (`DX-B-003`) |
| 3. Render | Actual mockup files exist and can be inspected, or an execution limitation is recorded | `SKILL.md` "3. Render", exit line; `references/mockups-and-preview.md` inspection table | 4 (`DX-B-004`) |
| 4. Iterate | The accepted design revision and its remaining uncertainties are identifiable | `SKILL.md` "4. Iterate", exit line | 8 (`DX-B-008`) |
| These phases are not new CLI subcommands | `SKILL.md` "What this skill owns, and what it does not" | 10 (`DX-B-010`) |
| Only documented, implemented DevForge commands may be named as executable gates | `SKILL.md` names the observed subcommand surface and states that none of it reads a design-spec; `references/sources.md` records the observation and its date | 10 (`DX-B-010`) |
| The user can invoke the skill in an ordinary subscribed terminal once installed and discovered | No managed-runtime section; no delivery or receipt helper is called; `references/sources.md` records the discovery paths | 1 (`DX-C-001`) |
| On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again | `SKILL.md` "When something is missing or a check cannot run", the interrupted-and-resumed bullet (added in repair pass 1 for F-003); `references/recording-rules.md` read-back step 4 | 8 (`DX-B-008`) |

## Outputs and standardized templates

| Spec row | Where addressed | Eval case |
| --- | --- | --- |
| design-spec, ID prefix `UX`, template `templates/devforge-design/design-spec.md` | `SKILL.md` outputs table; `assets/design-spec.md` is an exact byte copy of that template; `references/derivation.json` records the derivation | 1, 2 (`DX-C-001`, `DX-B-002`) |
| Required content: flows and screen-state decisions, linked mockup assets, requirement coverage, feedback disposition | `SKILL.md` "Outputs" paragraph; the template's own four tables | 2, 3 (`DX-B-002`, `DX-B-003`) |
| Consumer coverage: design-spec to prototype, architect, plan, review, change | `SKILL.md` "Outputs", with the honest note that none of those is installed and develop and review are drafts | 10 (`DX-B-010`) |
| Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner and one copyable task prompt | `SKILL.md` outputs table and write-ordering paragraph; `assets/handoff.md` is an exact byte copy of the shared template | 1 (`DX-C-001`) |
| Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions | `SKILL.md` "Outputs" (suggested / installed / invoked separation) | 6, 10 (`DX-B-006`, `DX-B-010`) |

## Validation and behavioral acceptance

Every row below has a case. Every outcome is `NOT_RUN`.

| Spec case | Required observation | `evals.json` id | `cases.jsonl` | Deterministic grader |
| --- | --- | --- | --- | --- |
| Direct activation | Creates assets and a design record linked to requirement IDs | 2 | `DX-B-002` | none; routed to AI review |
| Indirect activation | Includes a concrete error state and recovery path | 3 | `DX-B-003` | none; routed to AI review |
| Missing tooling | Supplies files and truthful manual preview steps; does not claim visual inspection | 4 | `DX-B-004` | `claim_evidence_binding` on `fixtures/unverified-inspection/inspection-claim.json` |
| Scope preservation | Uses the approved UI stack's conventions or records an explicit proposal | 5 | `DX-B-005` | none; routed to AI review |
| Out of scope | Does not manufacture a UI design task | 6 | `DX-B-006` | none; routed to AI review |
| Common: concurrent writer claims the worktree or branch | Stop dependent writes; report the collision; delete or reset nothing | 7 | `DX-B-007` | `artifact_side_effect`, sentinel `fixtures/ownership-collision/sentinel/UX-004.md` |
| Common: a relevant upstream revision, installed skill, base commit or candidate changes | Mark the applicable prior evidence stale and route a new check or run | 8 | `DX-B-008` | `path_present` plus `artifact_side_effect` on the preserved revision-2 bytes |
| Common: a template placeholder remains in a required result field | The result stays a draft and cannot be presented as ready | 9 | `DX-B-009` | `required_report_fields` on `fixtures/placeholder/UX-006.md` |
| Common: a requested check cannot execute | Record `COULD_NOT_RUN` and its actual cause; absence of an error is not `PASS` | 10 | `DX-B-010` | none; routed to AI review |
| Acceptance requires real outputs from representative requests in each terminal for which support is claimed | Not satisfied. No terminal run was performed; no support is claimed | 1 covers installed-resource resolution only | `DX-C-001` | `frontmatter_present`, `frontmatter_fields`, `package_relative_links` x3, `path_present` x2, `path_absent` |

The specification's closing line on this section - "These cases are authoring acceptance requirements; they have not been executed by writing this specification" - applies identically to this package. Writing the cases did not run them.

## Rework, stopping, and recovery

| Spec statement | Where addressed | Eval case |
| --- | --- | --- |
| Rework: revise mockups for feedback | `SKILL.md` "4. Iterate" | 8 (`DX-B-008`) |
| Product-scope conflicts return to define-product via change | `SKILL.md` "4. Iterate", the subsection "When the design would need an accepted requirement to change" (added in repair pass 1 for F-001), and its exit line | 11 (`DX-B-011`) |
| Uncertain behaviour becomes a bounded prototype | `SKILL.md` "4. Iterate", second paragraph; `references/mockups-and-preview.md` "Not a resolved technical uncertainty" | 8 (`DX-B-008`); triggers `A5a`, `A5b` |
| Stop when missing requirements that materially change a flow prevent declaring it ready | `SKILL.md` "Stopping" | 2 (`DX-B-002`) |
| Unavailable visual tooling does not become a successful visual check | `SKILL.md` "3. Render"; `references/mockups-and-preview.md` inspection table | 4 (`DX-B-004`) |
| Preserve accepted versions and observed failures; do not force-unlock, overwrite another session's result, change external gates, or retry indefinitely | `SKILL.md` "When something is missing or a check cannot run", collision bullet | 7 (`DX-B-007`) |
| If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming | `SKILL.md` upstream-changed bullet; `references/recording-rules.md` "Upstream references" | 8 (`DX-B-008`) |
| Report missing observations precisely | `SKILL.md` result-vocabulary paragraph; `references/recording-rules.md` "Result vocabulary" | 4, 10 (`DX-B-004`, `DX-B-010`) |

## Native creator authoring prompt

| Spec instruction | How it was honoured |
| --- | --- |
| Use the operator-supplied worktree, provider, write fence and base | Worktree `claude-scaffold-design-20260910`, branch `author/claude-devforge-design-scaffold-20260910`, base `c17e758` verified before writing and before commit; writes confined to the package and this evidence directory |
| Read skill-authoring-contract.md at the selected revision | Read at `c17e758`, digest `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` |
| Read this specification, its named templates, and only the relevant sections of the shared artifact and execution contracts | Recorded in `references/derivation.json` `selected_inputs` and `references/sources.md` |
| Output: a focused skill in the assigned provider source, its needed runtime resources, reproducible eval cases and fixtures, and separate A/B/C observations | Package authored; A/B/C are reported separately and all are `NOT_RUN` |
| Record the real installation mode and candidate/baseline identities | Installation mode: none - source authoring only, recorded in `authoring-notes.md`. Candidate identity: `file-manifest.json`. No baseline exists for a new skill; tier B proposes `without_skill` |
| Do not claim implicit activation from a run explicitly supplied SKILL.md | No activation claim of any kind is made. The trigger file separates `explicit_invocation` from implicit categories and says explicit entries are never counted as implicit activation evidence |
| Preserve user scope and existing approval; keep DevForge authority external; respect the assigned worktree; report unavailable checks truthfully | `SKILL.md` "What this skill owns, and what it does not"; the missing-integration statement; `authoring-notes.md` "What this authoring does not claim" |
| Move lengthy conditional procedures into references | Two prose references, each linked at the phase that needs it |
| Keep the trigger description precise | 950-character description with explicit, direct, indirect and near-miss content; 23 trigger queries across three positive and six negative categories (the sixth, `negative_change`, was added in repair pass 1 for F-011) |
| Use scripts only for real deterministic operations | No `scripts/` |
| Copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path | Both templates copied byte-for-byte into `assets/`; every link is package-relative and resolves; no `docs/mvp` runtime dependency; no developer home path anywhere in the package |

## Completion handoff

| Spec statement | Where addressed |
| --- | --- |
| You are here: design and iterate the user experience | `SKILL.md` title and opening |
| Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit | `SKILL.md` "Stopping" |
| A document's accepted status and an external gate's passing result are separate facts | `SKILL.md` "Decisions versus proposals" and the missing-integration statement; `references/recording-rules.md` "Result vocabulary" |

## Coverage summary

Every row of every table in SKILL-003 is mapped above. All five acceptance-case rows and all four additional common cases have a case in `evals/evals.json` and a corresponding entry in `evals/cases.jsonl`, plus one tier-C case for installed-resource resolution and one case for the product-scope-conflict route: eleven cases in total. Five of the eleven carry at least one deterministic grader assertion; six route entirely to independent review, because no program can establish whether a flow is coherent, whether a stack rule was respected, whether a scope boundary was honoured, or whether a conflict was routed rather than absorbed, by reading bytes.

Counts in this file were recomputed from the bytes after repair pass 1 rather than carried forward. The counts in revision 1 of this document were wrong - 24 triggers where the file held 23, and four deterministic cases where it held five - and are corrected here; the revision-1 bytes remain at commit `9ad38de`.

Nothing here has been executed. Tiers A, B and C are `NOT_RUN`; behavioural status is `NOT_EVALUATED`.
