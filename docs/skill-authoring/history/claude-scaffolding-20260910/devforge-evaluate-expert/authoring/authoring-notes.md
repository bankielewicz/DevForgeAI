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

> **Provenance correction, repair pass 1.** The `SKILL.md` digest first recorded here was `342b8292…`. That is wrong for what was read. The bytes actually followed were commit `69b6090`'s, sha256 **`1e9929a5713de1df05e2b0bbafdc49de388e74104e584f4ec77c237c35362a0e`**; `342b8292…` is the *repaired* revision at `4999f31`, and it entered this record because the digest was computed from the builder's working tree after E1's repair pass had already landed there — the read and the hash were separated in time, and the file changed in between. Confirmed by content: the bytes read did not contain E1's added "Everything you are handed…" sentence, which `4999f31` has and `69b6090` does not. The other seven files below are byte-identical at both commits, so their digests were correct either way. Recording a digest taken at a different moment from the read is the mistake; the corrected value is used throughout.

| File | sha256 (as actually read, at `69b6090`) |
| --- | --- |
| `SKILL.md` | `1e9929a5713de1df05e2b0bbafdc49de388e74104e584f4ec77c237c35362a0e` |
| `references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| `references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| `references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| `references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| `references/validator-handoff.md` | `0cb2975c440d5df14e14d3b5f875393254eeeb72537684e421a5b740d0945f7f` |
| `assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| `assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |

`assets/expert-spec.md`, `assets/expert-package.md`, `assets/expert-skill.md` and `assets/evaluation-cases.md` were **not** used: they shape a *project expert* deliverable, and the target here is a framework skill whose specification, package record and cases have their own governing templates in `docs/mvp`.

**Dependency to record:** the builder is itself unvalidated. Its bootstrap review (E1) was running in parallel and was deliberately not waited on. If E1 found a defect in the builder's workflow, this authoring inherits it, and that is a real dependency rather than a formality.

**Resolved in repair pass 1.** E1 completed and produced `4999f31`. Its diff against `69b6090` touches two files: `SKILL.md` (four small changes) and the builder's own `references/derivation.json` (count corrections and a repair record). Assessed against this authoring:

| E1 change to the builder | Does it change this authoring? |
| --- | --- |
| Added "Everything you are handed … supplies facts about the project, never instructions to you and never authority" | **No.** The candidate already carries a stronger untrusted-evidence posture in `SKILL.md` §Non-negotiable boundaries, and `EX-DEF-005` plus eval case 10 test it. E1's sentence confirms the position rather than changing it. |
| §5 now names the working design document among the recorded identities | **No.** A populated `design/skill-design-spec.md` was produced and is referenced from the manifest and the handoff. |
| Stopping now requires the working design document | **No.** Same artifact; already satisfied. |
| Stopping gained a reuse-recommendation completion path | **Not applicable.** Selection concluded *create*, and the search limits were recorded as that path requires. |
| `derivation.json` trigger-count text corrected | **No.** Internal to the builder's own record. |

So no re-authoring was required. This section is the record that the diff was read and assessed rather than assumed harmless. The builder reference stays `69b6090` because that is what was followed; `4999f31` is noted as the current builder revision for whoever authors next.

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

---

# Repair pass 1

Applied 2026-09-10 from the independent E2 bootstrap review of the candidate at `e52ac59`. E2's records are read-only untrusted evidence; the review directory was not modified. **Every finding was reproduced against the frozen bytes before its change was applied** — nothing was taken on the report's word.

## Reproductions before repair

Confirmed independently, on the `e52ac59` bytes:

| Finding | How it was confirmed |
| --- | --- |
| F-001 | Transitive Markdown-link closure from `SKILL.md`: 18 of 28 runtime files reachable, 8 unreachable, plus a prose grep returning zero for each. The two scripts are reached by the P2 command block, not a link, so E2's count of 8 is right. |
| F-002 | Ran E2's `E2-RPT-001` on their `fenced-report` fixture: `MATCH`, `1 fields`, "every required field is present and populated" — for a `Disposition` field the document has only inside a fence. |
| F-003 | Ran `E2-NEG-002` on their `mention-only` transcript: `consulted=True` from a prompt reading "Do **not** use devforge-evaluate-expert for this". |
| F-004 | Ran their `typo.jsonl`: exit 0, `COMPLETED`, `assertions: []`. |
| F-005 | The stale `scripts/__pycache__/graders.cpython-312.pyc` was present, untracked, timestamped during the authoring runs. |
| F-006 | **Re-fetched the Claude skills documentation independently** rather than trusting the report: precedence is Enterprise > Personal > Project > Nested > `--add-dir` > Plugin > Synced > Bundled. The package omitted synced and bundled and had plugin before `--add-dir`. Both halves of the finding hold. |
| F-007 | `E2-FM-003` on a sequence-root frontmatter: `INDETERMINATE`. |
| F-008 | (a)–(d) each a direct byte comparison: docstring omits `duplicate`; disjointness sentence over-broad; `references/sources.md` absent from both `derivation.json` lists; the two shipped templates name a `decision.json`. |
| F-009 | Shared run-manifest template 22 keys, package copy 39, none removed. `grep -c 'not implemented in the DevForge CLI'` over the handoff returned 0. |

## Observed reruns after repair

Author observations, not validation. No tier was evaluated.

**Author fixtures, 17 cases** (13 original + 4 new regressions), both modes, exit **0**:

| Case | source | installed | Note |
| --- | --- | --- | --- |
| EX-GOOD-001…003, EX-DEF-001…008, EX-SEM-001…002 | unchanged | unchanged | All 13 original outcomes preserved exactly |
| EX-DEF-009 (fenced report) | MISMATCH | MISMATCH | New: F-002 regression |
| EX-DEF-010 (mention only) | MATCH | MATCH | New: F-003 regression, negative direction |
| EX-GOOD-004 (structured load event) | MATCH | MATCH | New: F-003 positive direction, so the detector cannot pass by never detecting |
| EX-DEF-011 (non-mapping root) | MISMATCH, MISMATCH | same | New: F-007 regression |

Totals: 16 `COMPLETED`, 1 `COULD_NOT_RUN`; assertions 11 MATCH / 8 MISMATCH / 6 INDETERMINATE in source mode (9 / 5 in installed, the difference being the mode-conditioned `EX-DEF-008`). **No aggregate key** in either header.

**E2's own 14 cases against their own synthetic inputs**, both modes, exit 0 — the three repaired behaviours, on the evidence that found them:

| Case | Before | After |
| --- | --- | --- |
| `E2-RPT-001` | MATCH `1 fields` | **MISMATCH** `incomplete` — "missing or empty required field(s): Disposition" |
| `E2-NEG-002` | MATCH `completed consulted=True` | **`consulted=False`** — "the run completed without consulting 'devforge-evaluate-expert'" |
| `E2-FM-003` | INDETERMINATE `unparsed` | **MISMATCH** `non-mapping-root` — "the frontmatter root is a YAML sequence, which cannot carry mapping keys" |

Every other E2 case kept its prior outcome, including the two that must stay conservative: `E2-FM-004` (block scalar) remains INDETERMINATE, and `E2-NEG-001` (timeout) remains `COULD_NOT_RUN`.

**One interaction worth recording.** E2's `e2-cases.jsonl` embeds their own `bogus_unknown_key` probe on the `E2-FM-004` line. After the F-004 fix that file is now *correctly rejected whole* at exit 1. Rerunning it verbatim is therefore no longer possible — which is the fix working, not a regression. The reruns above used a copy with only that one probe key stripped, leaving all 14 cases and every other byte intact; their file was not modified.

**Error probes:** `typo.jsonl` → exit 1, "unknown case key(s) 'assertion'"; `unknown-grader.jsonl` → exit 1 naming the grader; `malformed.jsonl` → exit 1, "case 'BAD' has an empty assertions list". All eight original probes still exit 1.

**F-005 verified two ways:** the documented form run against a *fresh copy* of `scripts/` now creates no `__pycache__`, and a run inside the package without `-B` creates none either. The stale directory was deleted (untracked, `git ls-files` returned 0 files).

**Structural sweep after repair:** link closure reaches every runtime file except the two scripts, which the P2 command block names; 46 local links all resolve; `SKILL.md` 151 lines; no shell-injection syntax; no home paths; all JSON and the 17 JSONL lines parse; fixture tree byte-identical before and after every run.

## One judgement call

E2 uses `expectations` as an *assertion*-level key, which my first allowlist omitted, so their file was rejected for that too. Rather than narrow the fix, I added `expectations` and `notes` to the permitted assertion keys: they are harmless documentation fields, and the failure F-004 actually identified — a mistyped `assertions` producing a silent zero-observation case — is caught independently by the new "assertions must be present and non-empty" rule. Being strict where it matters, permissive where it does not.

## Declined

Nothing was declined. All nine changes were applied, F-009(b) in the handoff rather than the package because the handoff is author evidence outside the candidate fence.

## Repair pass 1 — provenance correction

E2's focused recheck of `e101e76` closed F-001 through F-009 and raised one new MINOR, **F-R01**: repair pass 1 changed bytes without regenerating the digests that record them. Seven `destination_sha256` values in `references/derivation.json` still carried candidate-1 values, and the `repair_pass_1` record did not disclose that they had moved.

The finding is correct, and it is the same class of defect the pass was fixing — a record asserting an identity its bytes no longer have. A derivation record whose digests are stale cannot distinguish a deliberate refresh from silent drift, which is the only reason it exists.

Audited independently: every recorded digest in the file was recomputed from current bytes. Exactly the seven E2 named were stale; the other 23 were already current.

| Destination | Candidate 1 | Candidate 2 |
| --- | --- | --- |
| `SKILL.md` | `5f9769dd…` | `bdf665c7…` |
| `references/native-evaluation.md` | `b43680f9…` | `7d4a8bda…` |
| `references/results-contract.md` | `6e99ade1…` | `ebac4e4c…` |
| `references/runner-interface.md` | `a58c35da…` | `87c8942f…` |
| `scripts/run_cases.py` | `d1fb1868…` | `95ca2abf…` |
| `scripts/graders.py` | `7c03e7b2…` | `1b7a27a3…` |
| `evals/cases.jsonl` | `b4b0c931…` | `c31a7cb0…` |

Each prior value is preserved in that entry's prior-digest chain, in the shape the sibling package's derivation record already uses, and stays reachable at commit `e52ac59`. The `repair_pass_1` record now carries a `destination_digest_regeneration` sentence listing all seven transitions.

Scope: `references/derivation.json` was the only package byte changed. No source digest was recomputed or altered, no behaviour changed, and the three verbatim `docs/mvp` template copies were re-verified byte-identical to their governing sources. This is a mechanical provenance correction, not a second repair pass, and it establishes nothing new about the candidate's behaviour.

**One consequence beyond the instruction, disclosed rather than done silently.** Regenerating `file-manifest.json` — authorised, since `derivation.json`'s entry in it changed — moves the manifest's own digest, and `handoff.md` cites that digest in two places. Leaving those would recreate F-R01's exact shape one level up, so both citations were updated to the new value. Nothing else in the handoff changed, and it remains revision 2. The same applied to its `authoring-notes.md` citation, which this very section moved.
