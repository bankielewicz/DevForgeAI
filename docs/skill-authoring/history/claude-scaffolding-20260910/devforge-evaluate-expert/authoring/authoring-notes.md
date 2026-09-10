# Authoring notes: Claude devforge-evaluate-expert

Worker A2, 2026-09-10 UTC. Phase 1 (port analysis) and phase 2 (authoring) of the coordinator's task packet.

## Assignment and fence

| Field | Value |
| --- | --- |
| Worktree | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` |
| Branch | `author/claude-devforge-evaluate-expert-scaffold-20260910` |
| Base commit, verified before writing | `c17e758417da64928a0f47fc2600304465ac3f3c` |
| Repository | `git rev-parse --git-common-dir` resolves to `framework/DevForgeAI/.git` |
| Write fence | `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/**` and this authoring directory |
| Untouched | the Codex package, the DevForge CLI and its policies, `docs/mvp`, every other Claude skill, the builder's worktree |

## The builder was source-loaded, not discovered

The frozen `devforge-project-expert-creator` was followed as **source-loaded instructions**: its files were read from disk with ordinary read tools. It was **not** installed, **not** discovered by a Claude session, and **not** activated. Nothing here is evidence about that skill's discovery, activation or behaviour.

Read from `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910` at commit `69b6090bde458f48cae0f5751035be65fdb4593c`, all under `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/`:

| File | sha256 |
| --- | --- |
| `SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` |
| `references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| `references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| `references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| `references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| `references/validator-handoff.md` | `0cb2975c440d5df14e14d3b5f875393254eeeb72537684e421a5b740d0945f7f` |
| `assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| `assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |

`assets/expert-spec.md`, `assets/expert-package.md`, `assets/expert-skill.md` and `assets/evaluation-cases.md` were **not** used: they shape a *project expert* deliverable, and the target here is a framework skill whose specification, package record and cases have their own governing templates in `docs/mvp`.

**Dependency to record:** the builder is itself unvalidated. Its bootstrap review (E1) is running in parallel and was deliberately not waited on. If E1 finds a defect in the builder's workflow, this authoring inherits it, and that is a real dependency rather than a formality.

### Builder workflow as actually performed

| Builder phase | What happened here |
| --- | --- |
| 1 Intake | Recovered the specification, contracts, templates, port source and the Claude documentation without asking the user to restate anything. Verified the specification digest against the packet. `devforge expert prepare` was **not** run: there is no consuming project or policy file in this assignment, so it had no input. |
| 2 Selection | Searched the Claude canonical source inventory; found no evaluator. Recorded as **create**, with the search limits stated. See below. |
| 3 Design | Populated the working design spec from the specification and the phase-1 port analysis. **No questions asked** - the packet directed this and supplied every material decision. Proposed defaults where the spec was silent are marked as proposals in §9 of that document. |
| 4 Authoring | Wrote the package inside the fence. |
| 5 Prepared transfer | File manifest, handoff, `Validation status: Not performed.` |

### Selection record

Searched: `providers/claude/plugins/devforgeai/skills/` in the assigned worktree at base `c17e758…` - `devforge-brainstorm`, `devforge-project-expert-creator`, `devforge-develop`, `devforge-review`. Read names and descriptions first, then the plausible candidate (`devforge-project-expert-creator`) in full. None evaluates a skill package; the creator explicitly excludes evaluating or grading, and is the *receiver* of this skill's output.

Not searched, and therefore not claimed empty: any machine-level `~/.claude/skills`, any managed settings directory, any enabled plugin inventory in a live session, any `--add-dir` location. None is reachable from this authoring context.

Result: **no suitable skill found in the searched inventory** - not a claim of global uniqueness. Decision: **create**, porting from the Codex implementation, since canonical sources are provider-specific under the authoring contract.

Destination collision check: `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert` did not exist before this work.

## Governing inputs

| Input | sha256 |
| --- | --- |
| `docs/mvp/specifications/skill-008-devforge-evaluate-expert.md` @ `c17e758…` | `0b3dbb7fe9f5f683d2022c86390e736346189e1ea4d92730c7234d9de1ecec0d` (matches the packet) |
| `docs/mvp/skill-authoring-contract.md` @ `c17e758…` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` |
| `docs/mvp/artifact-contract.md` @ `c17e758…` | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` |
| `docs/mvp/execution-contract.md` @ `c17e758…` | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` |
| `docs/development-language-policy.md` (working tree, read 2026-09-10) | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` |
| `docs/learned-behaviors/bounded-delivery.md` | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` |
| `AGENTS.md` | `959877c80a2611cde4dbf69ebba6304465fd3feada5cdf328344a8453c6539f0` |
| `CLAUDE.md` | `34b546db115af82c2b72cbf508eb8fb7807d3256ab3a6f567633576b39d87931` |

External documentation retrieved **2026-09-10**: `https://code.claude.com/docs/en/skills`, `https://code.claude.com/docs/en/sub-agents`. The specific claims used are recorded in the package's `references/sources.md` and in §2 of the phase-1 port analysis.

## DevForge CLI capability check

Run against `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge` (sha256 `835c32639c0a7df270fe1b9182580f14fc7d0874d3aad1b4037ba7cf420b2b07`) on 2026-09-10: `devforge --help`, `devforge expert --help`, `devforge check --help`, `devforge delivery --help`.

Observed surface: `delivery`, `expert {prepare|bind|status}`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`; `delivery` offers `capabilities|init|status|advance|resume|complete|check|verify|run|hook`.

Neither skill-package structural inspection nor evidence reduction appears. `devforge check` operates on a *project* against a policy and states it does not certify semantic behaviour. Only commands observed in this help output are named as gates anywhere in the package.

## Runner and grader observations

**These are local author observations, not validation.** They establish that the graders discriminate on synthetic inputs. They are not evidence about the authored skill's behaviour, and no tier was evaluated.

`--help` printed the documented prerequisites, arguments and exit meanings; exit 0.

Both passes ran over all thirteen cases in `evals/cases.jsonl` with `--candidate` set to `evals/fixtures`, writing to a scratch directory outside the package. Both exited **0**, meaning the program wrote a complete observations file - not that anything passed.

| Case | Fixture | `--mode source` | `--mode installed` | Intended |
| --- | --- | --- | --- | --- |
| EX-GOOD-001 | conforming package | COMPLETED; A1–A5 all MATCH | same | all MATCH |
| EX-GOOD-002 | populated report | COMPLETED; MATCH, MATCH | same | MATCH |
| EX-GOOD-003 | complete negative transcript | COMPLETED; MATCH | same | MATCH |
| EX-DEF-001 | no closing delimiter | COMPLETED; MISMATCH, MISMATCH | same | MISMATCH |
| EX-DEF-002 | duplicate `name` key | COMPLETED; MISMATCH | same | MISMATCH |
| EX-DEF-003 | unterminated flow sequence | COMPLETED; **INDETERMINATE** | same | INDETERMINATE |
| EX-DEF-004 | missing referenced resource | COMPLETED; MISMATCH | same | MISMATCH |
| EX-DEF-005 | prompt injection | COMPLETED; MATCH (sentinel), INDETERMINATE (routed R06) | same | as intended |
| EX-DEF-006 | self-claimed PASS | COMPLETED; MISMATCH | same | MISMATCH |
| EX-DEF-007 | incomplete negative transcript | **COULD_NOT_RUN**; INDETERMINATE | same | COULD_NOT_RUN |
| EX-DEF-008 | installed copy carrying `evals/` | COMPLETED; **INDETERMINATE** (mode-conditioned) | COMPLETED; **MISMATCH** | mode-conditioned |
| EX-SEM-001 | stack conflict | COMPLETED; INDETERMINATE (routed R04/R03) | same | routed, not graded |
| EX-SEM-002 | fake enforcement claim | COMPLETED; INDETERMINATE (routed R10) | same | routed, not graded |

Reason strings observed verbatim on the three that matter most:

- EX-DEF-003: *"the value of 'name' uses a YAML construct outside the supported scalar subset; a YAML parser is required and this grader does not use one"* - the honest answer in both directions, neither a pass nor a fabricated defect.
- EX-DEF-006: observed `claimed='PASS' evidence=none`, result MISMATCH, reason *"the file asserts an outcome while every declared evidence field is null or empty; the claim is recorded as an observed claim and is not adopted as a result"* - two facts, as designed.
- EX-DEF-007: observed `no-terminal-completion events=[prompt,selection_requested,timeout]`, case `COULD_NOT_RUN` - an unrelated selection event during an incomplete run concluded nothing.

### Error paths and the no-write guarantee

| Probe | Observed |
| --- | --- |
| `--out` already exists | exit 1, "output already exists and is never overwritten" |
| `--out` inside `--candidate` | exit 1, "output must be outside the candidate tree" |
| Missing case file | exit 1, named path |
| `--candidate` not a directory | exit 1, named path |
| Malformed JSONL line | exit 1, with file and line number |
| Unknown grader name | exit 1, naming the grader |
| Unknown `--case-id` | exit 1, naming the id |
| Subset selection | exit 0; the selected case ran, the other twelve recorded `SKIPPED`, and the header recorded `subset: EX-DEF-003` |

The fixture tree was hashed before and after every run: **byte-identical**, and no stray file appeared anywhere under `--candidate`. No aggregate key (`overall`, `coverage_complete`, `passed`, `summary`) exists in either observations file; this was checked programmatically, not by eye.

No defect was observed in the runner or graders, so nothing needed fixing before commit.

## Package self-checks

Author observations, on the authored bytes:

- No exclamation-prefixed shell-injection syntax anywhere in the package. One prose mention in `references/sources.md` was rewritten to remove the character adjacency entirely.
- No developer home path inside the package.
- `SKILL.md` is 143 lines, within the documented 500-line guidance.
- All 16 JSON files parse; the 13 JSONL case lines parse; both Python files compile.
- All 35 local Markdown links inside the package resolve.
- The three verbatim template copies hash equal to their `docs/mvp` sources.

## Decisions and their basis

Coordinator answers Q1–Q6 and the shell-syntax constraint were applied as given; they are tabulated in §9 of the working design spec. Four decisions were mine, recorded as proposals rather than requirements:

1. **Grader vocabulary `MATCH`/`MISMATCH`/`INDETERMINATE`**, deliberately disjoint from `PASS`/`FAIL`/`NOT_RUN`/`COULD_NOT_RUN`/`NOT_APPLICABLE`, so a grader row cannot be pasted into a results record as an authority outcome.
2. **Exit codes describe the program**, never the candidate. This is the single clearest structural difference from the Codex inspector, whose `0/1/2` meant candidate PASS/FAIL/COULD_NOT_RUN.
3. **`graders.py` has no command interface**, so there is exactly one executable and no second entry point resembling a gate.
4. **`worktree-environment.md` merged** into `native-evaluation.md` rather than shipped separately, keeping the reference count below the Codex package's fifteen.

## Deviations from the phase-1 port analysis

- The analysis proposed a separate `references/manual-inspection.md`. It was merged into `references/missing-rust-capabilities.md`; two files for one procedure was unnecessary.
- The analysis listed `assets/test-cases.json` as "port with reduction" and the tree omitted it from the phase-2 count. It is present.
- The analysis's §1 disposition counts were corrected before commit: 7 DROP, 3 RUST-replaced, 23 ported.

## What was not done, and is not claimed

No installation. No export. No tier A, B or C observation. No independent review of this candidate. No skill was discovered or activated. No evaluation of anything was performed - the runner exercised synthetic fixtures only. No commit to any branch other than this worktree's, and nothing pushed.

**Validation status: Not performed.**
**Behavioural status: `NOT_EVALUATED`.**
**Enforcement status: requirements recorded; no gate implemented by this skill.**
