# SKL-006 v3 follow-up: decisions, verification and remaining qualification

This prepares SPEC-007 v3 and SKL-006 v3 from approved v2. Both new revisions remain `in-review`.
Bryan chose the three policies in the 2026-10-01 Codex session; those choices do not approve the
completed implementation or waive native and manual checks. The source plugin candidate is 0.10.1.

## Scope and plan

1. Bind the baseline and preserve the main checkout's existing edits. Work on
   `codex/git-open-items-20261001`, initially based on `b9b1ccca485899e71ac61648f0fdac8373c30ddb`.
2. Add failing Compose tests, then change the scanner. Change the instruction routes and their
   generator-owned eval fixtures; retain all v2 results and thresholds.
3. Verify the committed candidate with the repository's local gates and offline grader controls.
   Record failures individually; offline controls do not execute Claude's instructions.
4. Run the native evaluations and attended manual checks below before qualification and approval.

Decisions and their implementation:

| Requirement | Change | Verification |
|---|---|---|
| ERR-04 before publishing unrelated history | Check the requested branch's merge base before rebase, documentation diff or push; offer a fresh branch based on the remote or stop | VER-06 strengthened with local-ref and no-rebase/merge checks; VER-35 tests an unrelated named branch while checked-out main is in sync |
| D4 on every carrying branch | Inspect `origin/<default>..HEAD`, including commits already pushed on another branch; reuse explicit inclusion | Existing VER-28; new VER-32 and VER-33; VER-26 remains the attended linked-worktree check |
| Narrow Compose password warning | Only basenames `compose.local.yml`, `compose.example.yml`, their `.yaml` forms and `docker-compose.*` equivalents, case-insensitive; mapping and list forms | VER-17 unit tests, including negative filename controls and token/private-key/other-key blocking; new VER-34 |
| No accidental publication of local files | A marked Compose file is a task candidate only when explicitly requested; its warning still needs a yes | BEH-07 and VER-34 |
| Refresh dependent citations | SPEC-008 draft and SPEC-010 in-review v3 cite SPEC-007 v3; QA and posting contracts are unchanged | Schema and link checks; SPEC-010 approval pending |
| Run all source tests together | Make the git tests a package and support both package and direct-file imports | Baseline pytest collection failure, then combined-suite rerun |

## Baseline and test-first evidence

Baseline: `b9b1ccca485899e71ac61648f0fdac8373c30ddb`, clean isolated worktree, before the first edit.

| Check | Status | Evidence |
|---|---|---|
| `python3 -B -m unittest discover -s src/tests/git -p 'test_*.py'` | PASS | Exit 0, 82 tests |
| `python3 -B -m pytest --collect-only -q -p no:cacheprovider src/tests` | FAIL | Exit 2, 468 tests collected; git and prd `test_structure.py` import-name collision |
| New Compose tests against unchanged v2 scanner: `python3 -B src/tests/git/test_scan_staged.py -k compose` | FAIL | 5 tests, 3 failures: marked passwords blocked, password-only exception absent, unquoted/whole-quoted list passwords missed |
| Same focused command after the scanner change | PASS | Exit 0, 5 tests |
| Quoted YAML mapping-key regression, `python3 -B src/tests/git/test_scan_staged.py -k quoted_mapping` | FAIL then PASS | The new test first found no finding in an unmarked production file. After unwrapping quoted Compose keys, the six Compose tests pass, with marked files warning and the production file blocking |
| Native failing test for ERR-04 and D4 instruction changes | NOT_RUN | The v2 historical ERR-04 failures are retained in SPEC-007 §9, but are not a current native red run. New eval cases and scripted negative controls do not establish native behavior |

First candidate `c7f6550ecaa392c7ab322318565f2b59ee32cdae`:

- **FAIL:** git's 87-test suite had two schema failures; combined source pytest had 2 failures,
  474 passes and 371 passing subtests. `approved_by: null` was invalid for this schema; the fix
  uses its existing unapproved value, `""`, in the spec and provenance. No schema or test was relaxed.
- **FAIL:** all 23 scripted good runs passed their checked graders, but the stricter wrapper caught
  two failed commands in `delivers-task-changes`: unset `TMPDIR` sent a temporary hash record to
  `/h`. The simulator now assigns its own `DEVFORGEAI_SIM_TMP` per case. All 25 negative controls
  were rejected by the checked graders; no native LLM grader ran.
- **PASS:** Codex package 287 tests, archive 8 tests, regex tables and strict plugin manifest
  validation. The sandboxed validator attempt encountered a blocked Anthropic startup request;
  the approved outer retry exited 0. This is manifest validation, not native skill qualification.

The original candidate logs and command/commit/hash receipts are retained separately in
`/tmp/devforgeai-git-open-items-evidence-20261001/candidate1-*`.

The main checkout's deployed plugin matched its v2 source during intake (`diff -rq`, excluding
`__pycache__` and `results`, exit 0). This does not establish candidate deployment parity. PR #51
was merged; PR #52 was open and conflicting at intake. Its active worktree is outside this change.

## Candidate verification

The tested implementation is `ea149e047a4135727b612f3937308850c427c8fa`, tree
`08092cf12d0fc269145df344092e3d1aab588047`, clean before and after every recorded command. It includes
current main `229d124595273828bc3c2b375194a723a8929118`: PR #52 merged during this work, and its context
approval is preserved in AGENTS.md and CLAUDE.md. Main's intervening SPEC-004 update is also preserved
unchanged; neither change is authored by this git follow-up. The main checkout's existing edits
were not changed. A later reporting-only commit updates this runbook; its source/spec identity is
checked against the tested implementation.

Receipts and full logs are in `/tmp/devforgeai-git-open-items-evidence-20261001/`. Each JSON receipt
contains the actual command, working directory, before/after commit and tree, exit code and log
SHA-256. `candidate3-*` is the post-merge run; `candidate1-*` and `candidate2-*` remain intact.

| Check | Status | Observed result |
|---|---|---|
| `python3 -B -m unittest discover -s src/tests/git -p 'test_*.py'` | PASS | 88 tests, exit 0 |
| `python3 -B -m pytest -q -p no:cacheprovider src/tests` | PASS | 477 tests and 371 subtests, exit 0; collection collision resolved |
| `python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'` | PASS | 287 tests, exit 0 |
| `python3 -B /tmp/devforgeai-git-v3-controls.py` | PASS | Executes `simulate_runs.py`'s 23 good runs and 25 negative controls, verifies expected exit codes and targeted rejecting graders, and rejects any command failure in a good run. No unexpected outcomes; LLM graders skipped |
| `node src/tests/git/check_patterns.mjs` | PASS | Regex table controls, exit 0 at `d2f07f8`; script and generated git eval bytes unchanged in the merge |
| `python3 -B src/tests/git/make_evals.py` | PASS | 23 cases regenerated at `d2f07f8`, leaving the worktree clean; generator and eval bytes unchanged in the merge |
| `python3 -B /tmp/devforgeai-git-v3-static.py` | PASS | Three spec schemas, unapproved candidate metadata, v3 upstream pins, original Change Logs preserved, both manifest JSONs, whitespace and clean state |
| `python3 -B src/claude/DevForgeAI/skills/documents-updater/scripts/check_docs.py README.md CHANGELOG.md docs/runbooks/git-v3-checks.md` | PASS | Three files, no errors; rerun after this reporting-only edit |
| `claude plugin validate src/claude/DevForgeAI --strict` | PASS | Exit 0 at `c7f6550`; same manifest SHA-256 `c2248233a4e34a283a770f79c09e51ab2a813fb2bb28d6e8a7dcfbb6f6ebee9f` in the tested implementation. Manifest validation only |
| `python3 -B -m unittest discover -s src/tools/session-archive -p 'test_*.py'` | FAIL | Post-merge concurrent run: `test_concurrent_archives` counted 9 sessions instead of 10; 1 failure in 8 tests |
| Same archive command, one isolated diagnostic rerun | PASS | All 8 tests passed on the same `ea149e0`; this does not waive the preceding failure |

**Unresolved finding:** archive concurrency is intermittent in these observations. Its source and
tests are byte-identical to the intake baseline (`git diff b9b1ccc ea149e0 -- src/tools/session-archive`
is empty). The underlying cause has not been established or repaired, and no named exception has
been accepted. The archive failure therefore remains part of the verification record; there is no
claim that every repository gate is unconditionally green. It is outside this change's write scope.

| Acceptance evidence | Local evidence | Native/attended evidence |
|---|---|---|
| ERR-04 routing, VER-06 and VER-35 | PASS: source routes and controlled grader outcomes | NOT_RUN: Claude must execute the revised instructions |
| All-branch carry and explicit inclusion, VER-28/32/33 | PASS: fixtures and controlled grader outcomes | NOT_RUN: Claude behavior; linked-worktree VER-26 remains manual |
| Compose password policy, VER-17/34 | PASS: six new unit tests, existing blocking controls and offline eval controls | NOT_RUN: Claude warning/confirmation behavior |
| SPEC-008 and SPEC-010 citation updates | PASS: schema-valid v3 pins; original authorship and Change Logs retained | SPEC-010 v3 owner approval pending |
| Manual VER-18..22, VER-24, VER-26, VER-31 | NOT_RUN | NOT_RUN: requirements and setup below |

Native evaluation, independent review, owner approval, merge and deployment of **v3** are pending.

## Native evaluation

Run from the candidate worktree in a plain terminal, per CLAUDE.md and ADR-001. Use a clean commit;
`record_revision.sh` refuses dirty `src/` or `docs/` and binds each new results folder to the code,
plugin digest and cases. Do not reuse a v2 folder or replace its results.

```bash
cd /tmp/devforgeai-git-open-items-20261001
P=src/claude/DevForgeAI
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet --threshold 0.8"
C="stops-on-unrelated-histories stops-on-unrelated-feature carry-asks-on-feature-branch"
C="$C carry-includes-named-commit warns-on-marked-compose-passwords"
for c in $C; do
  R=tmp/eval-results/git-v3-pilot-$c-$(date +%Y%m%dT%H%M%S)
  bash src/tests/prd/record_revision.sh "$R" git || break
  claude plugin eval "$P" --case "$c" --runs 1 --ablation none $A --no-publish --output-dir "$R"
done
R=tmp/eval-results/git-v3-1run-$(date +%Y%m%dT%H%M%S)
bash src/tests/prd/record_revision.sh "$R" git
claude plugin eval "$P" --tag git --runs 1 $A -j 4 --no-publish --output-dir "$R"
R=tmp/eval-results/git-v3-3run-$(date +%Y%m%dT%H%M%S)
bash src/tests/prd/record_revision.sh "$R" git
claude plugin eval "$P" --tag git $A -j 4 --no-publish --output-dir "$R"
```

Run the next stage only when the preceding stage's results have been inspected. Check every actor
error and every grader, not only the aggregate. The bar remains at least 0.8 per case over three
runs with the no-plugin baseline. A passing aggregate does not erase a failed grader.

## Attended manual checks

Export a fresh **v3 candidate copy** from the committed candidate, then use only the checklists in
[git-v2-checks.md](git-v2-checks.md) §2, replacing its old v2 setup with this one:

```bash
cd /tmp/devforgeai-git-open-items-20261001
git rev-parse HEAD
GIT_V3_COPY=$(mktemp -d /tmp/devforgeai-git-v3-manual.XXXXXX)
set -o pipefail
git archive HEAD src/claude/DevForgeAI | tar -x -C "$GIT_V3_COPY"
GIT_V3_PLUGIN="$GIT_V3_COPY/src/claude/DevForgeAI"
claude plugin validate "$GIT_V3_PLUGIN" --strict
```

After the owner selects and enters a scratch repository outside DevForgeAI, start
`claude --plugin-dir "$GIT_V3_PLUGIN"`. Record the printed candidate SHA and the actual loaded
plugin path. Do not use this setup for VER-31, which specifically needs this repository's real
EnterWorktree guard and an owner-deployed candidate in a dedicated worktree.

Keep the original v2 table intact and record v3 evidence separately with the candidate SHA, plugin
digest, session, exact fixture, commands and observed state. No item below has run in this session.

| Item | Status | Required environment or evidence |
|---|---|---|
| VER-18 | NOT_RUN | Owner-selected scratch GitHub repository: PR creation, reuse, draft and ID-collision cases |
| VER-19 | NOT_RUN | Scratch PRs with each readiness failure; attended confirmation and chosen merge method |
| VER-20 | NOT_RUN | Scratch squash merge and pruned remote ref, extra-commit control, ignored-file retention |
| VER-21 | NOT_RUN | Claude permission/authentication/error cases; isolate signed-out `gh` in a scratch config rather than signing out the owner's account |
| VER-22 | NOT_RUN | Original post-PR-1 state no longer exists; reconstruction needs a separate owner decision |
| VER-24 | NOT_RUN | Independent QA session and scratch PR through failed, stale and current-head approval states |
| VER-26 | NOT_RUN | Actual Claude linked-worktree session; verify location and refusal handling, plus D4 on its feature branch |
| VER-31 | NOT_RUN | Actual Claude EnterWorktree isolation guard; retain any refusal and never try another path or tool to evade it |

The development session must not issue its own QA verdict or labels. An owner or independent QA
session controls those records. Candidate approval and deployment follow review and qualification;
the existing approved v2 deployment remains the operational copy until then.
