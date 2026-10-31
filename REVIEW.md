# REVIEW.md: reviewing a change to DevForgeAI

This file tells a reviewer what to find and report on a pull request that changes DevForgeAI itself. Two reviewers
use it:
- GitHub's managed Code Review, which reads `REVIEW.md` at the repository root from the default branch.
- The local `/code-review`, which reads only `CLAUDE.md`. CLAUDE.md's "Loaded on demand" table tells it to read
  this file before the close review.

DevForgeAI is built with its own method: spec first, decisions are Bryan's, and the evidence is bound to a commit.
A review of a change to it checks the code, and it checks that the change went through that cycle. PR #126 was
closed unmerged on 2026-10-31 for skipping one step of the cycle (issue #137), after its code reviews had passed.

This file doesn't define the `qa` skill's review criteria for a user's project. Those are SPEC-008 §13's open
question.

## When reviews run in the cycle

| Stage | Review | Before |
|---|---|---|
| Spec drafts | An independent drafts review of the spec or ADR | Bryan's approval |
| Each plugin iteration | plugin-validator and skill-reviewer (Phase 6 of `/plugin-dev:create-plugin`) on the iteration's last commit | the push |
| Each push | Codex's inline review, and `/code-review` on the PR | the paid eval run |
| Close review | `/code-review` on the final commit, with this file and the work item's rows in `EVAL.md` | the merge |

## What to check

1. **Correctness.** The change does what the cited BEH, ERR or VER items say, and introduces no bug. Name the item
   for each finding.
2. **EVAL.md.** Each row for the work item is PASS on the reviewed commit, or waived in Bryan's words recorded in
   the spec's §9. A row with no evidence, or with evidence from another commit that the rerun matrix doesn't cover,
   is a finding.
3. **The plugin workflow** (EVAL.md G5). A commit that changes `src/claude/DevForgeAI/` outside a
   `/plugin-dev:create-plugin` iteration blocks the merge. A subagent's edit and a review-fix round are iterations
   too.
4. **Decisions are Bryan's.** No new behaviour without a spec, ADR or recorded decision (CLAUDE.md, "Look it up
   before building it"). A choice settled "by my reading" where the spec is silent is a finding.
5. **Approved documents.** A changed approved document carries a version bump, a new `updated` date, two Change Log
   rows and moved `upstream` links. Earlier Change Log rows are untouched.
6. **Numbers.** Every score, count and cost the PR quotes matches its source file (`aggregate-result.json`, the
   pytest output). A grader widened after its results follows the two-number §9 rule: the score under the old grader
   first, then the correction, then the new score.
7. **Tests.** New tests were seen failing first. No failing test was investigated by changing the working tree
   (ADR-005 D7).
8. **Scope.** The PR does what its plan and spec say, and no more. Spec, build and records go in separate PRs.
9. **Guards.** A guard fails closed (ADR-006 D1), and watching without blocking stays possible (ADR-006, the
   dogfooding constraint).
10. **Secrets.** No token, key or password anywhere in the diff.

## Inputs

- The diff against `origin/main`, and the PR body with its cited IDs.
- `EVAL.md`, the work item's rows, and their evidence.
- Codex's review comments on the PR: `gh api repos/bankielewicz/DevForgeAI/pulls/<N>/comments` and `.../reviews`.
  Bryan, 2026-10-31: "include in your code review the codex reviews in the pr".
- Bryan's words, as EVAL.md, the spec's §9 and the PR body quote them. The plan under `tmp/` is local, so a
  reviewer can't check anything that only the plan holds, and a claim that rests on the plan alone is a finding.
- For check 3: the Phase 6 reports committed on the branch in `docs/process/plugin-workflow/reviews/`, named
  `<UTC>-<tool>-<hash>.md`, and, until issue #137's ledger exists, the PR body's list of each iteration's
  invocations (EVAL.md G5).

## Where a finding goes

- **The PR introduced it:** fix it in the PR. A fix under `src/claude/DevForgeAI/` starts a new plugin-dev
  iteration.
- **It was already on main:** file a GitHub issue and link it from the PR.
- **A rule the PR follows is hitting valid work:** it goes to Bryan before the merge, never recorded as the rule
  working.
- **Notes that block nothing:** one summary at the end of the review, each note marked accepted or challenged.

## What blocks the merge

- any EVAL.md row for the work item that is FAIL or NOT_RUN without a recorded waiver
- a plugin commit outside an iteration
- an unanswered review comment, Codex's included
- a decision Bryan didn't make
- an approved document changed without its bump

## The report

List the findings most severe first. Give each its `file:line`, the check above or the EVAL.md row it breaks, and
where it goes. Name the reviewed commit's short hash. Save the report as
`docs/process/plugin-workflow/reviews/<UTC>-code-review-<hash>.md` and commit it on the PR's branch, next to the
Phase 6 reports. The review still counts as one of the final commit when `git diff --name-only <reviewed hash> HEAD`
lists only files in that folder (EVAL.md, "How the check works"). Any other change after the reviewed hash needs a
new review.
