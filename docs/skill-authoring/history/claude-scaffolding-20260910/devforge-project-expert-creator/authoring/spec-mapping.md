# SKILL-007 to package mapping

Specification: `docs/mvp/specifications/skill-007-devforge-project-expert-creator.md`, revision 3, sha256 `983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c`.

Package: `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator`, inventoried in `file-manifest.json`.

Paths below are package-relative. Eval IDs are the `id` values in `evals/evals.json`; trigger IDs are from `evals/triggers/trigger-queries.json`. No eval or trigger has been executed; every outcome is `NOT_RUN`.

## User goal and use-case inventory

| Specification row | Package file and section | Eval coverage |
| --- | --- | --- |
| User goal: author a focused expert capability from a concrete need, approved decisions and verified references | `SKILL.md` "Create project expertise", "Required inputs" | 1 |
| Direct request: "create the persistence expert this project needs" | `SKILL.md` frontmatter `description`; body §1 Intake | 1; triggers A2a-A2c |
| Indirect request: "our next story needs someone who knows this codebase's rules and pinned APIs" | `SKILL.md` `description`; §2 Selection | 2; triggers A3a-A3e |
| Expected result: expert-spec, expert-package, native skill instructions, standardized handoff | `SKILL.md` §3, §4, §5; `assets/expert-spec.md`, `assets/expert-package.md`, `assets/expert-skill.md`, `assets/handoff.md` | 1, 10 |
| Required context: goal or story, expertise map, architecture rules, selected runtime, approved sources | `SKILL.md` "Required inputs" table; `references/interview-guide.md` "Recover before you ask" | 1, 2 |
| Plugin capability: creator invocation is an authoring aid, not an independent verdict; DevForge handles binding and installation | `SKILL.md` "What this skill does and does not own"; `references/manual-operation.md` command table | 9 |
| State/action boundary: generate inside the declared expert directory; do not change external policy, evaluator expectations or permissions to pass | `SKILL.md` §1 Intake, §4 Authoring; `references/framework-context.md` "Who owns what" | 3, 6, 9 |
| MVP support decision: required on a real gap; reuse suitable expertise; refresh only when justified | `SKILL.md` §2 Selection; `references/existing-skill-selection.md` "Choosing" | 2, 4 |
| Does not activate for: a role label alone; a small task may need a context packet instead | `SKILL.md` `description` near-miss clause; §2 Selection | 5; triggers A6a-A6b, A7a-A7c |

## Shared authoring requirements

| Specification requirement | Package file and section | Eval coverage |
| --- | --- | --- |
| Provider source ownership, runtime packaging, scripts, reproducible fixtures, separate A/B/C results | `references/framework-context.md` "Package shape and packaging rules"; `evals/evals.json` `tier_note` and `fixture_note` | Structural; no eval |
| Original instructions need alignment with this revision; existence is not conformance | `references/derivation.json` `claude_baseline_superseded` (preserved behaviours and the reassigned binding ownership) | Not applicable: authoring-time record |

## Inputs and provenance

| Specification input | Package file and section | Eval coverage |
| --- | --- | --- |
| architecture-contract, required for production expertise | `SKILL.md` "Required inputs"; fixture `evals/fixtures/stale/ARCH-001.md` | 3, 4, 7 |
| story or concrete project goal, at least one required | `SKILL.md` "Required inputs"; fixture `evals/fixtures/project.md` | 1, 5 |
| Current expertise map and expert package, optional | `references/existing-skill-selection.md`; fixtures `expertise-map.md`, `existing-expert/SKILL.md` | 2, 4 |
| Primary technical references, required for factual API guidance | `SKILL.md` §3 Design (URL, retrieval date, version, verification); `references/framework-context.md` "Grounding expertise" | 3 |
| change-request or expert-evaluation-report, conditional | `references/validator-handoff.md`; fixture `evaluator-handoff.md` | 4, 10 |
| Exact revisions, hashes, stable section IDs, decisions, source evidence; a proposal cannot become an accepted constraint by being copied downstream | `references/framework-context.md` "The artifact envelope" and "Grounding expertise" | 3, 7 |
| Reuse valid current artifacts rather than replaying every earlier phase | `references/interview-guide.md` "Recover before you ask" | 2, 10 |
| Execution contract: every writing session has an owner and fence; concurrent writers use distinct worktrees; a shared worktree is not a concurrency mechanism | `SKILL.md` "When something is missing or a check cannot run"; `references/framework-context.md` "Roles that stay separate" | 6 |

## Workflow and phase exits

All five phases are workflow content in `SKILL.md`, not CLI subcommands, exactly as the specification requires ("These phases describe the skill's workflow, not new CLI subcommands").

| Phase | Required work and exit | Package file and section | Eval coverage |
| --- | --- | --- | --- |
| Intake | Recover goal, constraints, source/version identities, provider, fence; record actual authority and missing inputs | `SKILL.md` §1 | 1, 9 |
| Selection | Search existing expertise and source/install mapping; justified reuse, bounded enhancement or creation with collision handling | `SKILL.md` §2; `references/existing-skill-selection.md` | 2, 5, 6 |
| Design | Focused Q&A; preserve decisions and API versions; populate skill-design-spec and classifications; grounded specification and proposed cases before authoring | `SKILL.md` §3; `references/interview-guide.md`; `assets/skill-design-spec.md`; `assets/evaluation-cases.md` | 1, 3, 8 |
| Authoring | Create or enhance only the canonical candidate and its necessary resources; no target tests, binding or installation by the creator | `SKILL.md` §4; `references/manual-operation.md` command owners | 4, 9, 10 |
| PreparedTransfer | Save candidate/XSPEC/XPKG identities and an actionable evaluator handoff; actual limitations and next user invocation; no receiver execution claim | `SKILL.md` §5; `assets/handoff.md`; `assets/expert-package.md` | 1, 10 |
| Legacy four-phase mapping; binding does not become creator work | `references/derivation.json` `claude_baseline_superseded.reassigned_behavior`; `references/manual-operation.md` | 9 |
| Only documented, implemented DevForge commands may be named as executable gates | `references/manual-operation.md` "Command boundaries" - every row verified against actual `--help` | 9 |
| On interruption, preserve the current phase and evidence; resume by rechecking identities and the assignment | `SKILL.md` "When something is missing or a check cannot run"; `assets/handoff.md` "Retention and continuation limits" | 6, 7 |

## Outputs and standardized templates

| Artifact | Template shipped | Package file | Eval coverage |
| --- | --- | --- | --- |
| expert-spec (XSPEC) | `assets/expert-spec.md`, byte-identical to the governing `docs/mvp` template | `SKILL.md` §3 | 1, 8 |
| expert-package (XPKG) | `assets/expert-package.md`, byte-identical | `SKILL.md` §5 | 1, 7 |
| native skill instructions (NATIVE) | `assets/expert-skill.md`, byte-identical | `SKILL.md` §4 | 1, 4 |
| Handoff with output identities, observed checks, unresolved decisions, next owner and one copyable task | `assets/handoff.md`, bounded adaptation of `docs/mvp/templates/shared/handoff.md` | `SKILL.md` §5 | 1, 10 |
| Templates copied into the package with package-relative references; installed skills must not depend on the repository docs path | `references/derivation.json` derivations; `references/framework-context.md` "Resolving paths" | Structural; no eval |
| Do not interpret a handoff recommendation as authority for unrelated external actions | `references/manual-operation.md` "Artifact mapping"; `assets/handoff.md` closing paragraph | 10 |

## Validation and behavioural acceptance

Every specification case is materialised. These are authoring acceptance requirements; the specification states they "have not been executed by writing this specification", and they have not been executed by writing this package either.

| Specification case | Required observation | Eval ID and name | Trigger coverage |
| --- | --- | --- | --- |
| Direct activation | Produces a capability specification and native candidate with project references | 1 `direct-activation` | A1a-A1b, A2a-A2c |
| Indirect activation | Checks reuse before creating another skill | 2 `indirect-activation-reuse-check` | A3a-A3e |
| Stack conflict | Preserves the contract and reports the conflict | 3 `stack-conflict` | Not applicable: tier B only |
| Refresh | Updates affected guidance, invalidates affected prior evaluation, retains history | 4 `refresh-after-accepted-change` | A3c |
| Out of scope | Identifies actual capability needs instead of generating an org chart | 5 `out-of-scope-org-chart` | A6a-A6b (negative) |
| Common: a concurrent writer claims this session's worktree or branch | Stop dependent writes, report without deleting or resetting | 6 `ownership-collision` | Not applicable: tier B only |
| Common: a relevant upstream revision, installed skill, base commit or candidate changes | Mark applicable prior evidence stale and route a new check | 7 `stale-upstream-reference` | Not applicable: tier B only |
| Common: a template placeholder remains in a required result field | The result stays a draft and cannot be presented as ready | 8 `leftover-placeholder-stays-draft` | Not applicable: tier B only |
| Common: a requested check cannot execute | Record `COULD_NOT_RUN` and its actual cause; absence of an error is not a pass | 9 `requested-check-could-not-run` | Not applicable: tier B only |
| Acceptance requires real outputs in each terminal for which support is claimed | No support is claimed. Tier A, B and C are all `NOT_RUN`; behavioural status `NOT_EVALUATED` | `evals/evals.json` `authoring_status` | All triggers `NOT_RUN` |
| Source-grounded version-specific knowledge, declared refresh conditions, reproducible tests | `SKILL.md` §3; `references/derivation.json` `refresh_conditions`; fixtures reproducible from source with real digests | 3, 7 |
| Create optional folders only when justified | No `scripts/`; `references/` limited to what `SKILL.md` links | Structural; no eval |
| The native creator receives the assigned provider path; it must not use a shared default source | `references/existing-skill-selection.md` "Choosing"; `references/framework-context.md` "Package shape and packaging rules" | 2, 6 |
| Description optimization uses distinct authored/held-out queries; output-quality comparisons retain the no-skill or old-skill baseline | `evals/triggers/trigger-queries.json` `split_policy`; `evals/evals.json` `baseline_comparison: old_skill` on every case | All triggers |

## Rework, stopping, and recovery

| Specification requirement | Package file and section | Eval coverage |
| --- | --- | --- |
| Use evaluator findings for bounded revisions; governing-rule defects return through change; every changed candidate gets a new package identity and relevant reevaluation | `SKILL.md` "When an evaluator sends findings back"; `references/validator-handoff.md` | 10 |
| Stop when missing approval for a consequential rule, unverifiable required API behaviour, or a conflicting write fence prevents declaring readiness | `SKILL.md` "Stopping" | 6, 9 |
| Preserve accepted versions and observed failures; no force-unlock, no overwriting another session's result, no changing external gates, no indefinite retry | `SKILL.md` "When something is missing or a check cannot run"; `references/validator-handoff.md` "Recover the frozen baseline first" | 6, 7, 10 |
| If the worktree or active run changes, re-establish the baseline and evidence before resuming; report missing observations precisely | `references/validator-handoff.md`; `references/framework-context.md` "Result vocabulary" | 7, 9 |

## Native creator authoring prompt

| Specification element | Disposition |
| --- | --- |
| "Use the available native skill creator with the following task" | Followed as an operator-author bootstrap. No Claude builder exists to invoke; the Codex creator's process was read by absolute path and followed as source-loaded instructions. Recorded in `authoring-notes.md` and in `references/derivation.json` `authoring_route`. |
| Read the authoring contract at the selected revision | Read at sha256 `371462385b4e...`; distilled into `references/framework-context.md` with sections recorded. |
| Output: focused skill, needed runtime resources, reproducible eval cases and fixtures, prepared handoff; a separate evaluation owner supplies A/B/C | Delivered. The prepared handoff is `handoff.md` in this authoring directory; the package ships `assets/handoff.md` as its template. |
| Record the real installation mode and candidate/baseline identities | Installation mode: none. No install or export was performed. Candidate and baseline identities are in `file-manifest.json` and `references/derivation.json`. |
| Do not claim implicit activation from a run given an explicit SKILL.md | No activation of any kind is claimed. `evals/evals.json` `tier_note` states tier B can never evidence discovery or activation. |
| Move lengthy conditional procedures into references; keep the trigger description precise; use scripts only for real deterministic operations | `SKILL.md` is 118 lines with conditional detail in six references; `description` carries precise triggers and near-miss exclusions; no `scripts/`. |
| Copy needed templates into the package and use package-relative references | Seven `assets/` files, all package-relative, derivations recorded. |

## F01-F08 manual promotion contract

| Specification paragraph | Disposition for this Claude package |
| --- | --- |
| The Codex packages replace skill-builder/skill-validator as discoverable workflows; managed v1 protocol IDs and old receipts unchanged; no new-name managed adapter admitted | `NOT_APPLICABLE` to a Claude package. Retained as historical identities only, in `references/manual-operation.md` "Historical identities". |
| The creator authors, the evaluator evaluates read-only, the user initiates each receiving skill and command | Carried: `SKILL.md` "What this skill does and does not own"; `references/framework-context.md` "Roles that stay separate". Eval 10. |
| Automatic orchestration and G8 funded-launch repair remain deferred; original cases and failed evidence preserved | Carried as a statement of deferral in `references/manual-operation.md` "Historical identities". No orchestration is implemented or claimed. |
| Use skill-design-spec.md as the detailed XSPEC source; XPKG is its candidate/provenance map; EVPLAN/EVREPORT bind the evaluator's records | Carried: `references/manual-operation.md` "Artifact mapping". |
| Accepted Routine/Full policy for manual mode, first qualification and consequential changes requiring Full | `NOT_APPLICABLE`. Scoped to the promoted Codex packages; recorded as not applicable in `assets/skill-design-spec.md` "Evaluation coverage proposed" until an owner selects an equivalent for Claude. |
| Mechanical checks and semantic review are separate; existing expert prepare/bind/status/check enforce only their implemented predicates; missing enforcement blocks its dependent claim but reporting remains possible | Carried: `references/manual-operation.md` "What these commands do not cover". Eval 9. |
| Retain existing-environment, create-Git-worktrees and static-only choices; preparation is not native readiness | Carried in substance: this authoring is static-only and claims no native readiness. |
| Owner-approved local unqualified baseline after a bounded acceptance set; installer records `LOCAL_ACCEPTANCE_SET_PASS` with `qualification_status: UNQUALIFIED` | `NOT_APPLICABLE`. The predicate recognises two Codex identities. Recorded as not applicable in `references/manual-operation.md`; the nine-check portable record catalogue was not carried. |

## Completion handoff

| Specification requirement | Package file and section |
| --- | --- |
| Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit | `SKILL.md` "Stopping" |
| A document's accepted status and an external gate's passing result are separate facts | `references/framework-context.md` "Result vocabulary"; `assets/handoff.md` status lines |

## Coverage summary

- 5 of 5 specification acceptance cases materialised as evals: IDs 1-5.
- 4 of 4 additional common cases materialised as evals: IDs 6-9.
- Rework path materialised as eval 10.
- 21 tier-A trigger queries: 10 positive across explicit invocation (2), direct domain (3) and indirect (5); 11 negative across six near-miss categories; fixed stratified train/validation split (12 train, 9 validation).
- 9 synthetic fixtures, all package-relative, with the stale-upstream mismatch bound to real reproducible digests.
- Rows recorded `NOT_APPLICABLE` with a reason rather than omitted: 5 (the Codex-scoped promotion, Routine/Full, local-baseline, managed-adapter and per-skill-metadata rows).
- Executed: nothing. All tiers `NOT_RUN`; behavioural status `NOT_EVALUATED`; Validation status: Not performed.
