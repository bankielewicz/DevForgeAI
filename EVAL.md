# EVAL.md: the pass/fail checks for DevForgeAI's proposed work

Written 2026-10-31 by session 7637882f, at Bryan's request: "Before the start of any development, create an eval.md
… to pass a 'check' to determine as validation or failure metric based on proposed works." It covers the work after
PR #126's close, in this order: the plugin-workflow gate (issue #137: C, the ADR, probes P1-P8, A, B), then the ui v3
redo (SPEC-017 v3, ADR-007 v3, SKL-013 v3). Bryan's decisions are quoted where they apply, and the plan's decision
ledger (`tmp/plans/2026-10-31-ui-v3-redo-plan-design.md` §11, local) holds them all. Cells marked **[Bryan]** still
wait for him; this file decides nothing.

## How the check works

- **One check per work item.** A work item passes its gate when every one of its rows is PASS on one commit, the
  commit the gate names. There is no partial pass.
- **Each row is binary.** PASS or FAIL, from the command or the evidence named in the row. A row that couldn't run
  is NOT_RUN, and NOT_RUN is not a pass (AGENTS.md, "Testing Guidelines").
- **Waivers are Bryan's.** A row passes by waiver only when Bryan's words, their date and when the waiver ends are
  recorded in the spec's §9 or the plan's decision ledger (§11).
- **Evidence is bound to a commit.** It names the short hash it ran on. Evidence from an earlier commit counts only
  when the rerun matrix below says the change since then needs no rerun.
- **A failed row** is fixed and rerun. A fix under `src/claude/DevForgeAI/` starts a new plugin-dev iteration (G5).
- **Who checks.** The working session runs the rows and records them. The close review verifies them (REVIEW.md).

## G. Rows for every change

| ID | Check | PASS when | Evidence |
|---|---|---|---|
| G1 | Looked up before built | Every new or changed behaviour cites a spec, ADR or Bryan's recorded words, or `find_spec.py`'s "no match" plus Bryan's answer | the PR body or the plan |
| G2 | Python tests | `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests` exits 0 and its count is at least the baseline taken before the first change (ADR-005 D7) | both counts, with hashes |
| G3 | Plugin kit and manifests (when the plugin changed) | `claude plugin test src/claude/DevForgeAI`, `claude plugin validate src/claude/DevForgeAI` and `claude plugin validate .` each exit 0 | the three outputs' last lines |
| G4 | Approved documents | Each approved document the branch changes has a new `version`, a new `updated`, two new Change Log rows (the change; Bryan's approval) and every citing `upstream` link moved (CLAUDE.md, "Rules a change must not break") | `git diff origin/main...HEAD -- docs/specs` |
| G5 | The plugin workflow | Every commit touching `src/claude/DevForgeAI/` lies inside an iteration: `/plugin-dev:create-plugin` with the iteration's scope and `/plugin-dev:skill-development` invoked before its first edit, and plugin-validator and skill-reviewer reports bound to the iteration's last commit, committed on the branch as `docs/process/plugin-workflow/reviews/<UTC>-{plugin-validator,skill-reviewer}-<hash>.md` (Bryan, 2026-10-31: `tmp/` is gitignored, so a report there can't be verified from the PR). No hand-written `ledger.jsonl` lines: the mod writes those. Until B ships, the session transcript's Skill calls show the invocations. After B: `src/tests/process/test_plugin_workflow.py` passes | transcript lines; report paths |
| G6 | One version | `plugin.json`, `.claude-plugin/marketplace.json` and the pin in `src/tests/progress/test_adapter_structure.py` show the same version | `grep -n '"version"'` on both manifests; the pin line |
| G7 | Whitespace | `git diff --check origin/main...HEAD` prints nothing | its output |
| G8 | No secrets | No token, key or password in the diff | the review's finding list |
| G9 | Reviewed | The close review (REVIEW.md) ran on the final commit, every finding is fixed or filed, and every Codex comment on the PR is answered | the review report; the PR's threads |

## Work items

### C. The CLAUDE.md rule (#137)

| ID | Check | PASS when |
|---|---|---|
| C1 | The rule is on main | `grep -c 'Plugin changes go through' CLAUDE.md` on main is 1, and the bullet's text, its line breaks joined, equals #137's "Enhancement C" block |

### ADR. The guard's ADR (ADR-008, proposed)

| ID | Check | PASS when |
|---|---|---|
| ADR1 | Accepted | `docs/specs/adr/ADR-008.md` has `status: accepted` and a Change Log row quoting Bryan's approval |
| ADR2 | Records what #137 left open | It records Bryan's answers to #137's decisions 1 to 3 (2026-10-31: the mod in `src/tools/mods/dev-guard/`; records in `docs/process/plugin-workflow/`; a CI job for B), and whether the guard is the tracker's hook or a separate guard under ADR-006 D1 |
| ADR3 | Probes recorded | P1 to P8 each have a result, the Claude Code version and the date |
| ADR4 | Drafts reviewed | An independent review's report is saved and each finding is answered before Bryan's approval |

### P. Probes (#137's table; each in a scratch repository, the mod loaded by `--plugin-dir`)

| ID | PASS when (#137's words) |
|---|---|
| P1 | Logged values recorded. The opening rule uses whichever signal fires. |
| P2 | Both logged with `agentId` |
| P3 | `true`, absent, absent |
| P4 | `/dev-guard` answers in all three |
| P5 | Recorded. A.1 keeps it inert there either way. |
| P6 | The second session reads the value |
| P7 | Recorded. If it can, the close also requires the person's typed command. |
| P8 | `git diff --cached --name-only` returns the staged list |

### A. The dev-guard mod (#137 "Acceptance")

| ID | Check | PASS when |
|---|---|---|
| A1 | Kit tests | A.7's tests pass under `claude plugin test <mod>` |
| A2 | Strict validation | `claude plugin validate --strict <mod>` exits 0 |
| A3 | R1 live | With no ticket, an Edit to `src/claude/DevForgeAI/skills/ui/SKILL.md` in `.claude/worktrees/<name>/` is refused with R1's reason |
| A4 | Subagent | With no ticket, a subagent's Write there is refused |
| A5 | R2 live | With no ticket, `python3 src/tests/ui/make_evals.py` is refused |
| A6 | R3 live | With no ticket, a `git commit` with a staged plugin file is refused |
| A7 | Permit | After `/plugin-dev:create-plugin`, `/plugin-dev:skill-development` and Reads of the `requiredReads` files, A3's Edit is allowed |
| A8 | Close | `/dev-guard close` refuses without the two reports for HEAD, and writes the ledger line with them |

### B. The commit check (#137)

| ID | Check | PASS when |
|---|---|---|
| B1 | Catches a miss | `test_plugin_workflow.py` fails on a branch whose plugin commit is missing from the ledger |
| B2 | Passes a listed commit | It passes once that commit is listed in a closed ticket |
| B3 | Runs with the suite | `pytest src/tests` collects it |
| B4 | CI job (Bryan, 2026-10-31, "docs/process + CI job") | A GitHub Actions job runs the test on a PR touching `src/claude/DevForgeAI/**` and shows in the PR's checks |

### S. SPEC-017 v3 and ADR-007 v3, redrafted from main

| ID | Check | PASS when |
|---|---|---|
| S1 | Issues covered | Each of #115, #116, #117, #118, #121 and #125 maps to a BEH, ERR or VER item, or to an out-of-scope line carrying Bryan's words |
| S2 | Rulings carried | START-HERE §3's carried rulings (graders, the brief judge, BEH-01 step 10, BEH-18's Next step) are in the text |
| S3 | Reviewed | The drafts review's report is saved and every finding answered |
| S4 | Approved | G4 holds for both, and the test pins and links a spec bump moves are moved |

### U. SKL-013 v3, built from main

| ID | Check | PASS when |
|---|---|---|
| U1 | Workflow | G5 holds for every round, review fixes included |
| U2 | Tests first | Each new test was seen failing before the code it tests: a recorded failing run, with its hash |
| U3 | Structure | The structure pins pass, QR-01's body word cap among them from the first build commit |
| U4 | Script | `dsn_check.py`'s tests pass |
| U5 | Grader mutations | Every mutation class in plan §6 fails its named grader in `check_graders.py`, which exits 0 |
| U6 | Real replies | Every grader passes the replies on file (plan §3), before the first paid run |
| U7 | Bound runs | `record_revision.sh` ran on a clean tree, into a new folder, before each paid run |
| U8 | Qualification | Once, on the commit to be merged: the ui suite with `--runs 3`, the no-plugin baseline, `--model claude-sonnet-5-5`, `--judge-model sonnet`, `--threshold 0.8`, `--max-cost-usd 90` and `--keep-temp` (the rerun matrix needs its traces). The command exits 0, every case scores at least 0.8, every `cases[].arms.with[].error` is null, and `partial` is false. No waiver (Bryan, 2026-10-31, "Sonnet, 3 runs + baseline") |
| U9 | Plugin effect | Every case the skill's output decides has Δ above 0; a case at 1.00 in both arms is listed as not showing the plugin's effect (plugin-evals.md, "The no-plugin baseline") |
| U10 | Triggering | The trigger cases (should and shouldn't trigger) pass on `claude-sonnet-5-5` and on `claude-opus-5-5`, measured apart from the output cases (skills.md, "Evaluate and iterate on a skill"). Haiku is not a target model (Bryan, 2026-10-31, "Sonnet and Opus only") |
| U11 | Live checks | Plan §5 step 2.7's list, run on the build commit with `--plugin-dir`, each recorded in SPEC-017 §9 |
| U12 | Cost | Every paid run passes `--max-cost-usd`, and the ledger's sum for the build phase stays at or under $100. A run that exits 2, or whose result has `partial: true` or `skippedPaidGraders`, is NOT_RUN |
| U13 | Record | SPEC-017 §9 holds the results folders, the commit, the plugin digest, the models, the scores and the cost |

### R. Records and deploy

| ID | Check | PASS when |
|---|---|---|
| R1 | Deployed copy | CLAUDE.md's `diff -rq` of the source and `.claude/skills/devforgeai` prints nothing |
| R2 | Marketplace copy | After `claude plugin update devforgeai@devforgeai`, a session's skill base directory names the new version |
| R3 | Records PR | The records went out as their own PR, after the build PR merged |

## Paid runs: smoke, then one qualification

- **Smoke, on each change:** only the cases the change touches, with `--runs 1 --ablation none --model
  claude-sonnet-5-5` and judge-free graders where they suffice. A smoke run is evidence for the next step, never a
  qualification ("A single run is noisy, so confirm any change at the default three runs before you trust it",
  plugin-evals.md).
- **Qualification, once, before the merge:** U8.
- **A change after qualification** reruns what the matrix below says.

## Rerun matrix (plan §6; Bryan, 2026-10-31, approved with changes)

Qualify last. Every rerun goes into a new results folder through `record_revision.sh`, and gets a cost-ledger line and
a SPEC-017 §9 row.

| Change after qualification | Rerun |
|---|---|
| SKILL.md, or a reference the eval paths read | U8 again, in full. A second U8 can't fit under the $100 ceiling, so the edit goes to Bryan as a budget decision for that event |
| A reference only live runs reach (Artifact) | the live check only, with evidence: no Read of that path in the qualification run's transcripts |
| A grader | offline first: `check_graders.py` on the mutations and the real-reply corpus, and a re-grade of the qualification run's saved outputs. A paid rerun of the affected cases only if those outputs can't be re-graded. The two-number §9 rule applies |
| `dsn_check.py` | pytest, and the cases that exercise the script, at U8's settings |
| `make_evals.py` or a case file | the changed or new cases at U8's settings. A case whose prompt changed has no evidence until then |
| A version bump only (`plugin.json`, `marketplace.json`, the pin) | none beyond G6 |
| Docs or records | none, provided nothing under `src/claude/DevForgeAI/` changed |

Rows 2 and 3 need the qualification run's transcripts and outputs, so U8 runs with `--keep-temp`, and its
`/tmp/claude-eval-*` traces are copied into the results folder before the OS clears them.

## Cost ledger

One line per paid run: date, results folder, commit, `--max-cost-usd`, `costUsd` from `aggregate-result.json`. Quote
a total only from that sum. The closed cycle spent $97.73. Its three full ui suites were 50 cases, 1 run each, with
no baseline, on the unpinned default model (Opus): $26.15, $25.52 and $25.47, about $0.52 a run, of which the
judge was $0.09 a suite. Sonnet 5.5's list price per token is half Opus 5.5's. The build phase's ceiling is $100
(Bryan, 2026-10-31). On a claude.ai subscription, `costUsd` is a list-price estimate of plan usage, not a charge.
