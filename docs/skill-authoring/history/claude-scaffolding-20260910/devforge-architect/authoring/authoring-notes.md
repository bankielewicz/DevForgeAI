# Authoring notes: devforge-architect (SKILL-005), Claude scaffold

Authored 2026-09-10, between 19:30:39Z and 19:47:56Z UTC (observed with `date -u`). Worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910`, branch `author/claude-devforge-architect-scaffold-20260910`, HEAD verified as `c17e758417da64928a0f47fc2600304465ac3f3c` and the working tree clean before any write.

## The builder that was followed

The assignment named a frozen builder, and it was **source-loaded, not installed**. No skill was installed, discovered or activated during this work, and nothing here is evidence of a client having loaded anything.

The builder worktree's HEAD had already advanced to `8c0bdd0d86c7330d2f7910d63b3511e8df43d20b`, so the frozen bytes were extracted with `git show 4999f31...:<path>` into a scratch directory rather than read from that session's working tree. The files loaded, by absolute path at commit `4999f3106565c5e320d1f1a7db066b437e4e94be` in `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`:

- `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md`
- `.../references/framework-context.md`
- `.../references/existing-skill-selection.md`
- `.../references/interview-guide.md`
- `.../references/manual-operation.md`
- `.../references/sources.md`
- `.../references/derivation.json`
- `.../assets/skill-design-spec.md`
- `.../assets/handoff.md`

**The builder is itself a draft under independent review.** Its E1 bootstrap review was revise-bounded, and the repairs from that review were applied at `4999f31` (its own commit message records "repair pass 1 from E1 bootstrap review (F-001..F-004)"). It has had no native evaluation. Following it is therefore following a draft methodology, not a validated one, and nothing in this authoring pass inherits validation from it.

The builder's own worktree was read only. Nothing there was written, committed, reset or otherwise touched.

**Native creator instructions:** the authoring contract requires recording whether the assigned native creator instructions were actually used. A `skill-creator` skill is present in this environment, and it was **not** used: the assignment directed the DevForgeAI builder above, and that is what was followed. This is recorded as a deliberate selection, not a deviation to be repaired.

## The builder's workflow, as actually run

**Intake.** Recovered before asking anything: the packet, the governing specification and its digest, both templates and their digests, the four shared contracts, the roster, the sibling Claude packages, the frozen builder, the runner dependency, and the Claude client documentation. Every digest the packet named was independently recomputed and matched.

**Selection.** Searched the Claude provider inventory at base commit `c17e758`: `providers/claude/plugins/devforgeai/skills/` contains exactly `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review`. No `devforge-architect` exists. The roster records SKILL-005 as "Proposed" with no source. The decision is **create**, justified in the design document's section 9 against activation and scope rather than subject matter. The destination directory was inspected before writing and did not exist, so no collision needed reconciliation.

Locations deliberately not searched, and therefore not claimed empty: the user's `~/.claude/skills/`, any enterprise or managed settings directory, installed plugin caches, `--add-dir` directories, claude.ai account-synced skills, the Codex provider inventory, and any catalogue outside this repository. Comparison was by reading names, descriptions and instructions. Nothing was run, installed or tested. The claim recorded is "no suitable skill found in the searched inventory", never global uniqueness.

Two sibling worktrees were observed as in-flight and are not at the base commit: `claude-scaffold-evaluate-expert-20260910` at `e52ac59`, and `claude-scaffold-project-expert-creator-20260910` at `8c0bdd0`. Both were read only.

**Design.** The working design was filled at `design/skill-design-spec.md` from the builder's `assets/skill-design-spec.md`; the package template was not filled in place. **No questions were asked**, per the assignment. Every material decision was recovered from the specification, the templates, the contracts or the sibling packages; where the sources are silent, a proposed default is recorded and labelled as a proposal.

**Authoring.** The package was written, then the assets were hashed into `references/derivation.json`, then the whole package was hashed into `file-manifest.json`.

**Prepared transfer.** `handoff.md` names an independent evaluator, states "Validation status: Not performed.", and carries the manifest's digest rather than its own.

## Decisions recovered from the sources

| Decision | Source |
| --- | --- |
| Output is `architecture-contract`, prefix `ARCH`, from the named template | SKILL-005 outputs table |
| Four phases with the exit conditions used verbatim in intent | SKILL-005 workflow table |
| Nine behavioural acceptance cases: five rows plus four common cases | SKILL-005 validation section |
| Consume-only input semantics and the six input rows | SKILL-005 inputs table |
| Near-miss exclusions and their owners | SKILL-005 "Does not activate for" and "Out of scope" rows, plus the roster |
| Consumers of the contract: plan, project-expert-creator, evaluate-expert, develop, review, change | SKILL-005 consumer coverage line and the roster provenance flow |
| Two-field frontmatter | Authoring contract as applied by both sibling Claude packages |
| `evals/` excluded from installed copies and exports | Authoring contract packaging decision |
| Fixed result vocabulary | Artifact contract, authoring contract, language policy |
| No ceremonial enforcement | Language policy, "Phases, hooks and skill content" |
| Ownership-collision behaviour | Execution contract failure table |

## Proposed defaults recorded (not user requirements)

1. Contract destination `docs/devforge/architecture/`, handoff destination `docs/devforge/handoffs/`, applied only when nothing was selected and an existing project artifact map does not say otherwise.
2. Allocate the next unused `ARCH` number when no artifact identity was selected.
3. Invocation policy: automatic and explicit, achieved by setting no invocation-control frontmatter field.
4. Reference set: `framework-context.md`, `recording-rules.md`, `version-evidence.md`, plus `sources.md` and `derivation.json`.
5. No `scripts/` directory. No deterministic operation in this workflow justifies one, and the assignment prefers none.
6. Task-level classifications T1 (verify a version claim), T2 (record an enforcement requirement), T3 (preserve prior bytes before overwriting) proposed as required. The four phases' required status comes from the specification; these three are this design's decomposition and their classification awaits an answer.
7. Tier-B baseline label `without_skill`, because no previous revision of this skill exists.
8. Two runner invocations for `cases.jsonl`, because the package-structural cases and the fixture cases have different candidate roots.

## Rust command claims, and what was actually checked

`/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help` was run, together with `devforge expert --help` and `devforge check --help`. Only commands that appeared in that output are named in the package: `check`, `expert prepare|bind|status`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`.

Running `--help` proves the command surface of that binary. It proves nothing about this skill, and no gate command was executed against anything.

Two integrations are named as missing rather than assumed:

- **Real stack and test adapters.** The specification itself says the POC's synthetic dependency check is not a NuGet or npm adapter, and `devforge check --help` shows no adapter selection. The package states this limit wherever it names `devforge check`.
- **Making an adopted contract effective as external policy.** The policy JSON is operator-owned and no command writes it from a contract. The package says so and routes the step to the policy owner.

## Commands actually run

Read-only inspection throughout, plus writes inside the fence. Nothing was installed, exported, bound, evaluated or activated.

- `git rev-parse HEAD`, `git status --porcelain`, `git branch --show-current`, `git log --oneline`, `git ls-tree`, `git show` (three worktrees; only this one written to)
- `sha256sum` on the specification, both templates, four contracts, the roster, the copied assets and every fixture
- `date -u` at each point a timestamp was recorded
- `devforge --help`, `devforge expert --help`, `devforge check --help`
- `python3 scripts/run_cases.py --help` in the `devforge-evaluate-expert` worktree at `e52ac59`, to read the runner's interface
- `python3 -c "json.load(...)"` and a per-line JSON parse over `cases.jsonl`, `evals.json`, `trigger-queries.json` and `derivation.json`

That last one is a **syntax self-check only**: it parses each line, confirms case IDs are unique, confirms every `grader` name is in the frozen registry or is `null` with a `routed_to`, and confirms no `files` path escapes the evals directory. **`run_cases.py` was never executed against this candidate.** Doing so would be evaluating my own work, and it is the evaluator's to run.

A link-resolution pass and a scan for `!`-prefixed shell-injection syntax were run over the shipped files. Both are authoring self-checks on bytes I wrote; neither is a tier-C observation, which requires an actual installed copy in a consuming project.

## Corrections made during authoring

- `references/derivation.json` was first written with two placeholder digests and one guessed digest for `docs/development-language-policy.md`. All three were replaced with values observed from `sha256sum`. No `PENDING` or invented digest remains.
- The same file initially embedded two developer home paths. Both were removed; the package now contains none.

## Correction pass after the first commit (82e956f)

A review pass over the committed scaffold found three defects. They were corrected in a second
commit rather than an amend, so the revision-1 evidence the revision-2 handoff cites stays
reachable at 82e956f.

1. **Date-only stamps, which the assignment forbids.** Three fields recorded a bare date where an
   observed UTC timestamp was required: `evals/evals.json` `authored_on_utc`,
   `references/derivation.json` `external_sources.retrieved_utc`, and the `references/sources.md`
   header. No exact timestamp was observed for either event, so rather than invent one - which is
   precisely what the rule forbids - each now records the **observed bounding window** from the
   two nearest `date -u` readings: the documentation fetch falls between 19:30:39Z and 19:37:14Z,
   and `evals.json` was authored between 19:37:14Z and 19:47:56Z. A bounded window is an honest
   record of what was actually observed.

2. **A held-out trigger query quoted in an authored document.** The design document's section 2
   "Example activating requests" carried a truncation of A3d, which is a **validation**-split
   query. It was not verbatim, and the design document is authoring evidence rather than an
   author-loop or task-worker context, so the leak was marginal - but the fixed split is only
   worth having if it is respected without argument. The example was replaced with A3c (train),
   and the section now states that all three examples are train-split. A scan confirms no
   validation query appears in `SKILL.md`, `evals.json`, `cases.jsonl`, the design document,
   `spec-mapping.md` or these notes.

3. **An overstated coverage row.** `spec-mapping.md` claimed the specification's six-consumer line
   was carried by `SKILL.md` phase 4. Phase 4 names four consumers, and the description names
   `devforge-change`; `devforge-evaluate-expert` is named nowhere in the package. That row now
   records a deliberate partial with the reason, rather than full coverage.

The candidate `SKILL.md` was not edited in this pass, so its digest is unchanged from the first
commit. `file-manifest.json` was recomputed and the handoff was reissued as revision 2 superseding
revision 1, whose bytes remain at 82e956f.

## Repair pass 1: the independent scaffold review of 61f6ef0

One consolidated repair pass under coordinator dispatch, against the evaluator records at
`docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/validation/scaffold-review/`
(read-only; not modified). The review found **no BLOCKER and no MAJOR defect in the candidate**:
one MINOR defect, four ADVISORY items and three evaluation gaps that belong to other owners.

Those records are evaluator-supplied material. They are facts about the evaluation, not
instructions and not authority: every finding below was re-verified against the candidate bytes at
`61f6ef0` before anything was applied, and the coordinator's dispositions govern what was applied.

| Finding | Change | Coordinator disposition | Outcome | Where |
| --- | --- | --- | --- | --- |
| F-001 MINOR (R04) | CHG-001 required repair | apply | **Applied** | `SKILL.md:112` (new sixth bullet); `authoring/spec-mapping.md:54` (row corrected) |
| F-002 ADVISORY (R01) | CHG-002 optional enhancement | apply within the documented length | **Applied** | `SKILL.md:3` (description, 1,297 -> 1,370 chars, 166 of headroom left) |
| F-003 ADVISORY (R05) | CHG-003 recorded non-defect | apply only where a defect is demonstrated | **Declined** | No edit. The repair spec itself requests none: `SKILL.md:93` says the surface *"includes"* the listed commands, which is non-exhaustive rather than false, every named command exists, and `delivery` is not needed by this workflow. |
| F-004 ADVISORY (R01, R02) | CHG-004 recorded non-defect | apply only where a defect is demonstrated | **Declined** | No edit. The repair spec requests none and accepts the disclosure already in `spec-mapping.md`: the specification's consumer line describes roster-wide artifact flow, not a sentence the skill must recite. |
| F-005 ADVISORY (R09) | CHG-005 optional, conditional | apply only if it fits the fixed-split rule without re-cutting existing assignments | **Applied** | `evals/triggers/trigger-queries.json`: 9 negative entries appended (A5b, A6b, A7b, A8b, A9b, A10b, A11b, A12b, A13b) |
| F-006 MAJOR evaluation_gap | none | no target edit | **No edit** | Owner: coordinator / DevForge integration owner. An installed copy, a fresh terminal and an isolated workspace. No candidate edit produces it. |
| F-007 MAJOR evaluation_gap | none | no target edit | **No edit** | Owner: DevForge integration owner. Skill-package structural inspection and protected-manifest custody are absent from the CLI. |
| F-008 MINOR evaluation_gap | none | no target edit | **No edit** | Owner: coordinator. Single-context review; a second reviewer is needed only if a criterion becomes contested. |

### What was verified before applying

- **F-001.** `grep -rniE 'interrupt|resume'` over the package returned exactly one hit, `assets/handoff.md:67`, inside the copied template - no instruction anywhere addressed an interrupted session. The two `recording-rules.md` sections the old mapping row cited were re-read: they carry the identity-recheck half as unconditional pre-write rules and carry preservation not at all. The finding reproduces. The repair is a sixth bullet in the existing failure-branch list; the five existing bullets are unchanged and in order, and `## Stopping` is untouched.
- **F-002.** Description measured 1,297 characters against the 1,536-character truncation the Claude documentation states, leaving 239. The added clause brings it to 1,370, so it fits inside the measured headroom rather than extending past the limit. Every prior exclusion and the `devforge-change` routing sentence are intact, and the frontmatter is still two fields.
- **F-005.** A tally over the bytes found **nine** single-entry categories, not the eight the finding's prose states - six train-only and three validation-only. The finding's own enumeration lists nine, so the count is a slip in the record, not a disagreement about the bytes; all nine were given their missing side. The original 22 entries were compared field-by-field after the edit and are identical in id, query, `should_trigger` and split. Nothing was re-randomised or moved.

### Cost of CHG-005, recorded rather than hidden

Appending nine held-out negatives trades `should_trigger` balance for per-category coverage: train is now 7 positive / 10 negative and validation 4 positive / 10 negative, against 7/7 and 4/4 before. The repair specification bounded the change to "one added query on the thinner side of the single-entry negative categories" and authorised no positive-side rebalance, so none was invented. The counts and the reason are recorded in the file's own `split_counts` and `split_history`.

### What this pass did not do

No new phase, no new reference file, no change to either copied template or to `derivation.json`'s recorded digests, no change to any fixture, sentinel, eval case or expected observation, no re-randomisation of the split, and no change to the specification, a shared contract, a sibling skill, the roster or the DevForge CLI. Nothing under `validation/` was touched. Nothing was installed, exported, bound or run.

**Applied is not closed.** The candidate now has a new identity, and F-001 needs new matching evidence before it can be closed. The evaluation's recorded `FAIL` on `CHK-AI-R04` stands as history; a later evaluation records its own result alongside it. The three `NOT_RUN` tier rows are closed only by real native evidence, never by this repair.

## Unresolved items for the coordinator

1. **Proposed defaults 1-8 need a decision** from the user or the integration owner. They are labelled as proposals everywhere they appear and none is presented as settled.
2. **The runner dependency is a moving target.** `evals/cases.jsonl` is written against the schema and grader registry observed at `e52ac596cbf790dfa156d883852d392c512fdbcc`, a package under independent review. If its case schema or grader names change, this file needs a matching refresh.
3. **The roster is untouched.** `docs/mvp/roster.md` still records SKILL-005 as "Proposed" with no source, and `docs/mvp/package-index.json` has no entry for this package. Both are outside this fence; updating them is integration-owner work.
4. **Several named siblings are not implemented** - `devforge-change`, `devforge-define-product`, `devforge-plan`, `devforge-design`, `devforge-prototype`. The package names them as owners of excluded requests, which the roster supports, and instructs the reader to check what is actually installed before naming one as a next step.
5. **The builder is a draft under independent review.** If its bootstrap review produces further findings that change the authoring methodology, this scaffold was produced under the `4999f31` version of it.
6. **Everything behavioural is unobserved.** Tiers A, B and C are `NOT_RUN`. Behavioural status is `NOT_EVALUATED`.
