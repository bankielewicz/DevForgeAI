# EVAL.md: the pass/fail checks for DevForgeAI's proposed work

Written 2026-10-31 by session 7637882f, at Bryan's request: "Before the start of any development, create an eval.md
… to pass a 'check' to determine as validation or failure metric based on proposed works." It covers the work after
PR #126's close, in this order: the plugin-workflow gate (issue #137: C, the ADR, probes P1-P8, A, B), then the ui v3
redo (SPEC-017 v3, ADR-007 v3, SKL-013 v3). This file makes no decision. It records Bryan's, each quoted with its
date, and that quote is the record a reviewer checks until a spec carries the decision. The plan's decision ledger
(`tmp/plans/2026-10-31-ui-v3-redo-plan-design.md` §11) is a local copy only. Cells marked **[Bryan]** still wait for
him.

## How the check works

- **One check per work item.** A work item passes its gate when every one of its rows is PASS on one commit, the
  commit the gate names. There is no partial pass. Later commits keep that evidence only when `git diff --name-only
  <evidence hash> HEAD` lists nothing but files under `docs/process/plugin-workflow/reviews/` and §9 status rows
  (built, evaluated, merged: the rows CLAUDE.md lets change without a version bump). The rerun matrix's last row says
  those need no rerun, and G4 still applies to anything else in a spec. The R rows are their own work item, checked on
  main after the merge.
- **Each row is binary.** PASS or FAIL, from the command or the evidence named in the row. A row that couldn't run
  is NOT_RUN, and NOT_RUN is not a pass (AGENTS.md, "Testing Guidelines").
- **Waivers and decisions are Bryan's.** A row passes by waiver only when Bryan's words, their date and when the
  waiver ends are recorded in the spec's §9 (CLAUDE.md, "Evaluating a skill"), where the PR shows them. A decision
  that changes a row, such as the tiered ui suite, is not a waiver. It is quoted here with its date until its spec
  carries it (S5). The plan under `tmp/` is local and can't be checked from a PR.
- **Evidence is bound to a commit.** It names the short hash it ran on. Evidence from an earlier commit counts only
  when the rerun matrix below says the change since then needs no rerun.
- **A failed row** is fixed and rerun. A fix under `src/claude/DevForgeAI/` starts a new plugin-dev iteration (G5).
- **Who checks.** The working session runs the rows and records them. The close review verifies them (REVIEW.md).

## G. Rows for every change

| ID | Check | PASS when | Evidence |
|---|---|---|---|
| G1 | Looked up before built | Every new or changed behaviour cites a spec, ADR or Bryan's recorded words, or `find_spec.py`'s "no match" plus Bryan's answer | the PR body |
| G2 | Python tests | `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests` exits 0 and its count is at least the baseline taken before the first change (ADR-005 D7) | both counts, with hashes |
| G3 | Plugin kit and manifests (when the plugin changed) | `claude plugin test src/claude/DevForgeAI`, `claude plugin validate src/claude/DevForgeAI` and `claude plugin validate .` each exit 0 | the three outputs' last lines |
| G4 | Approved documents | Each approved document the branch changes has a new `version`, a new `updated`, two new Change Log rows (the change; Bryan's approval) and every citing `upstream` link moved (CLAUDE.md, "Rules a change must not break") | `git diff origin/main...HEAD -- docs/specs` |
| G5 | The plugin workflow | Every commit touching `src/claude/DevForgeAI/` lies inside an iteration: `/plugin-dev:create-plugin` with the iteration's scope and `/plugin-dev:skill-development` invoked before its first edit, and plugin-validator and skill-reviewer reports bound to the iteration's last commit, committed on the branch as `docs/process/plugin-workflow/reviews/<UTC>-{plugin-validator,skill-reviewer}-<hash>.md` (Bryan, 2026-10-31: `tmp/` is gitignored, so a report there can't be verified from the PR). No hand-written `ledger.jsonl` lines: the mod writes those. In the order Bryan set (2026-10-31: the docs PR, ADR-008 and the probes, A, B, then the ui redo), no plugin change is made before A and B ship. If one has to be, the PR body lists each iteration's two invocations (session ID, UTC time, the scope argument), because a session transcript can't be checked from the PR. After B: `src/tests/process/test_plugin_workflow.py` passes | the PR body; report paths; after B, the test |
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
| A8 | Close | `/dev-guard close`, typed by a person, refuses unless both reviewers' Agent calls were observed during the ticket and their reports exist for a commit whose plugin subtree hash equals HEAD's; it writes the ledger line with that evidence (ADR-008 D6) |

### B. The commit check (#137)

| ID | Check | PASS when |
|---|---|---|
| B1 | Catches a miss | `test_plugin_workflow.py` fails on a branch whose head's plugin subtree hash differs from its merge base's and matches no valid ledger line (ADR-008 D8) |
| B2 | Passes a closed iteration | It passes once a valid ledger line carries that subtree hash, and it passes at once on a branch that leaves the plugin unchanged |
| B3 | Runs in CI | The CI job runs it on every PR with its marker selected; `pytest src/tests` skips it by default (ADR-008 D8) |
| B4 | CI job (Bryan, 2026-10-31, "docs/process + CI job") | A GitHub Actions job runs the test on a PR touching `src/claude/DevForgeAI/**`, shows in the PR's checks, and is a required check once B ships (Bryan, 2026-10-31: "Decide now: B's CI job becomes a required check when B ships."; ADR-008 D8) |

### S. SPEC-017 v3 and ADR-007 v3, redrafted from main

| ID | Check | PASS when |
|---|---|---|
| S1 | Issues covered | Each of #115, #116, #117, #118, #121 and #125 maps to a BEH, ERR or VER item, or to an out-of-scope line carrying Bryan's words |
| S2 | Rulings carried | Bryan's rulings of 2026-10-30 are in the text: the brief judge at weight 0.5, with "the pre-build replay stays the gate for the judge's wording", and one-flow's grouping "settled by the request, the brief is unconfirmed"; BEH-01's step 10 on a turn that ends on a question: "those turns pause the run; step 10 stays unticked with no skipped marker; the checklist is repeated only when the run truly ends"; BEH-18: "after a failed approval check it says /devforgeai:ui BRN-NNN (the amend run), and the prd hand-off follows a successful approval only. Same for approve-plus-change." |
| S3 | Reviewed | The drafts review's report is saved and every finding answered |
| S4 | Approved | G4 holds for both, and the test pins and links a spec bump moves are moved |
| S5 | Three eval sets | QR-03 and VER-26 name the three sets (the core set at 3 runs with the baseline, the regression set once with regex graders, the trigger set per QR-04). They record the regression set as a departure from PRD-001 NFR-003's "every case … over 3 runs" in Bryan's words of 2026-10-31, as QR-04 records the negative triggers' 10 runs |

### U. SKL-013 v3, built from main

| ID | Check | PASS when |
|---|---|---|
| U1 | Workflow | G5 holds for every round, review fixes included |
| U2 | Tests first | Each new test was seen failing before the code it tests: a recorded failing run, with its hash |
| U3 | Structure | The structure pins pass, QR-01's body word cap among them from the first build commit |
| U4 | Script | `dsn_check.py`'s tests pass |
| U5 | Grader mutations | Each of these bad runs fails its named grader in `check_graders.py`, which exits 0. VER-39 (briefs): an unquoted idea; an invented state or screen; a layout word in each part; a token, hex value or px size in Style; a missing screen (one-flow); a missing closing line; two briefs in one fence; a quote not from the BRN. VER-33: only the checklist's "import its boards"; a change "shows up in the DSN" with no run or tool named. VER-36: an approval-only failure with no "not approved" block. VER-50: a skipped step written as prose; an unticked box |
| U6 | Real replies | Every grader passes the real replies kept from the closed cycle (the 19 brief replies and the 03aa89a suite replies, local under `tmp/`), before the first paid run; SPEC-017 §9 records the run |
| U7 | Bound runs | `record_revision.sh` ran on a clean tree, into a new folder, before each paid run |
| U8 | Qualification | Once, on the commit to be merged: the core set with `--runs 3`, the no-plugin baseline, `--model claude-sonnet-5-5`, `--judge-model sonnet`, `--threshold 0.8`, `--max-cost-usd 25` and `--keep-temp` (the rerun matrix needs its traces). The command exits 0, every case scores at least 0.8, every `cases[].arms.with[].error` is null, and `partial` is false. No waiver (Bryan, 2026-10-31, "Sonnet, 3 runs + baseline"). The core set is a decision, not a waiver (Bryan, 2026-10-31, "Approve these 11"): one case per distinct behaviour, tagged `ui-core` by the generator and run with `--tag ui-core`. The cases are writes-dsn (VER-01, VER-20, VER-50), unconfirmed-stays-null (VER-03), approve-on-explicit-words (VER-19), plain-run-never-approves (VER-35), approval-blocked-by-changed-board (VER-36), amend-changed-board (VER-10, VER-20), amend-prd-requirement (VER-31), amend-nothing-to-do (VER-33, VER-50), brief-drafted (VER-39), no-mockup-no-design-skill (VER-41) and no-boards-stops (VER-04, VER-50). Names and numbers follow the redraft if it changes them |
| U9 | Plugin effect | In U8's run, every core-set case has Δ above 0; a case at 1.00 in both arms is listed as not showing the plugin's effect (plugin-evals.md, "The no-plugin baseline"). The regression set (U14) and the trigger set (U10) run without a baseline, so they have no Δ and U9 doesn't apply to them (Bryan's tiering, 2026-10-31) |
| U10 | Triggering | The trigger cases (should and shouldn't trigger) pass on `claude-sonnet-5-5` and on `claude-opus-5-5`, measured apart from the output cases (skills.md, "Evaluate and iterate on a skill"). Haiku is not a target model (Bryan, 2026-10-31, "Sonnet and Opus only") |
| U11 | Live checks | Run on the build commit with `--plugin-dir`, each recorded in SPEC-017 §9: the briefs and the preview shown before the question; the rebuild after a refused publish (edit the canvas during "Draw it now"); the sharing line; VER-43 to VER-46, VER-48 and VER-49 (c). The redraft's BEH numbers name them |
| U12 | Cost | Every paid run passes `--max-cost-usd`. Before a paid run starts, the ledger's sum plus that run's `--max-cost-usd` must be at most $80; if not, the run goes to Bryan first, a repeated run included. The ledger's sum for the build phase stays at or under $80 (Bryan, 2026-10-31, "$80", after the core set; estimate about $69: U8 about $19, U10 $28.55 measured, the regression set once about $9.50, the measuring run about $1.50, smoke runs about $10). A run that exits 2, or whose result has `partial: true` or `skippedPaidGraders`, is NOT_RUN |
| U13 | Record | SPEC-017 §9 holds the results folders, the commit, the plugin digest, the models, the scores and the cost |
| U14 | Regression set | Every ui case outside the core set and the trigger set has regex graders only. It runs once (`--runs 1 --ablation none --model claude-sonnet-5-5 --threshold 0.8`) when the VER item it covers changes, which in this build means once each, and never at qualification. Each scores at least 0.8 on the commit it ran on, and the rerun matrix carries it forward |
| U15 | The sets are what they claim | A test in `src/tests/ui/` (written first, seen failing) checks the generated cases. Exactly the 11 core cases carry `ui-core`. Every ui case outside `ui-core` and the trigger set has no `llm` or `baseline` grader. The trigger cases carry no `ui` tag (QR-03) |

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
- **Measure, before U8:** two or three representative cases with `--runs 1`, the baseline on and `--model
  claude-sonnet-5-5`. Project U8's cost from the measured cost per run in each arm. If the projection, with 15%
  headroom, is above U8's `--max-cost-usd`, it goes to Bryan before U8 starts: U8 has only been estimated so far,
  from halved Opus runs.
- **Regression set, once per change to the VER item each case covers:** U14. Never at qualification.
- **Trigger set:** U10, as SPEC-017's QR-04 sets it.
- **Qualification, once, before the merge:** U8, the core set only.
- **A change after qualification** reruns what the matrix below says.

## Rerun matrix (Bryan, 2026-10-31: "Rerun matrix. Approved with these changes")

Qualify last. Every rerun goes into a new results folder through `record_revision.sh`, and gets a cost-ledger line and
a SPEC-017 §9 row.

| Change after qualification | Rerun |
|---|---|
| SKILL.md, or a reference the eval paths read | U8 again, in full, on the core set (about $19). About $69 of the $80 ceiling is already planned, so a second U8 doesn't fit, and the edit goes to Bryan as a budget decision for that event |
| A reference only live runs reach (Artifact) | the live check only, with evidence: no Read of that path in the qualification run's transcripts |
| A grader | offline first: `check_graders.py` on the mutations and the real-reply corpus, and a re-grade of the qualification run's saved outputs. A paid rerun of the affected cases only if those outputs can't be re-graded. The two-number §9 rule applies: §9 gives the score under the old grader first, then the correction, then the new score |
| `dsn_check.py` | pytest, and the cases that exercise the script, at U8's settings |
| `make_evals.py` or a case file | the changed or new cases at U8's settings. A case whose prompt changed has no evidence until then |
| A version bump only (`plugin.json`, `marketplace.json`, the pin) | none beyond G6 |
| Docs or records | none, provided nothing under `src/claude/DevForgeAI/` changed |

Rows 2 and 3 need the qualification run's transcripts and outputs, so U8 runs with `--keep-temp`, and its
`/tmp/claude-eval-*` traces are copied into the results folder before the OS clears them. Where a row says U8's
settings, a case in the regression set runs at U14's settings instead, and a trigger case at U10's.

## Cost ledger

One line per paid run: date, results folder, commit, `--max-cost-usd`, `costUsd` from `aggregate-result.json`. Quote
a total only from that sum. The closed cycle spent $97.73. Its three full ui suites were 50 cases, 1 run each, with
no baseline, on the unpinned default model (Opus): $26.15, $25.52 and $25.47, about $0.52 a run, of which the
judge was $0.09 a suite. Sonnet 5.5's list price per token is half Opus 5.5's. The build phase's ceiling is $80
(Bryan, 2026-10-31), set after the core set cut what qualifies from 50 cases to 11. One run of all 11 cost $6.41 on
Opus in the closed cycle, which is costlier than the 50-case average. Halving that gives about $3.21 on Sonnet. This is
an estimate, not a measurement: Sonnet's turn count and the baseline arm are unmeasured, so the measuring run before
U8 checks it. On a claude.ai subscription, `costUsd` is a list-price estimate of plan
usage, not a charge.
