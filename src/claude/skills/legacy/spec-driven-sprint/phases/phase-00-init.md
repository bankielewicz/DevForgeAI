# Phase 00: Init + Pre-Flight

## Entry Gate

```bash
# Phase 00 has no predecessor — phase-init IS the entry gate; skip phase-check.
devforgeai-validate phase-init ${ISSUE_ID} --workflow=spec-sprint --project-root=${PROJECT_ROOT}
# Exit 0: state created at phase 00 | Exit 2: invalid workflow/id
```

`${ISSUE_ID}` is `ISSUE-<n>`, derived from the issue argument in Step 1.

## Contract

PURPOSE: Parse the issue argument, fetch the issue, clear explicit dependencies through the CLI parser, compute the sprint branch before `/claim`, detect repo context (portable), toggle the DevForgeAI addendum, and run the ordered git/worktree pre-flight BEFORE any worktree is created in Phase 03.
DELEGATES TO: `tech-stack-detector` (langs/frameworks/test-runner/build-tool), `git-validator` (git availability, repo status, fallback). These are delegations, NOT gate-enforced — delegation compliance (a fabricated-subagent dispatch gate) is tracked by #413.
GATE: issue dependencies closed/merged, git remote reachable, and the local default branch is fast-forward-synced to `origin/<default>` (HALT if diverged).

---

## Mandatory Steps

### Step 1: Parse the issue argument, fetch the issue, clear dependencies, and compute BRANCH

EXECUTE: Parse `$ISSUE_ARG` (a URL like `https://github.com/<org>/<repo>/issues/318` or `#318` / `318`) into the bare number `<n>`. Set `$ISSUE_NUMBER = <n>` and `$ISSUE_ID = ISSUE-<n>`.
VERIFY: `$ISSUE_ID` matches `^ISSUE-[0-9]+$`. If the argument is missing or unparseable → HALT → AskUserQuestion.

EXECUTE: Create `tmp/${ISSUE_ID}/`, then fetch the issue into `tmp/${ISSUE_ID}/issue.json`:

```bash
gh issue view ${ISSUE_NUMBER} --json number,title,body,labels,state,url > tmp/${ISSUE_ID}/issue.json
```

VERIFY: `tmp/${ISSUE_ID}/issue.json` exists and `.state == "OPEN"`. If the issue is closed or cannot be fetched, HALT and AskUserQuestion.

EXECUTE: Parse and verify dependencies through the CLI, not by hand:

```bash
devforgeai-validate parse-issue-dependencies ${ISSUE_ID} --issue-json tmp/${ISSUE_ID}/issue.json --project-root=${PROJECT_ROOT}
```

VERIFY: `tmp/${ISSUE_ID}/dependencies.json` exists, its `issue_json_sha256` matches the current `tmp/${ISSUE_ID}/issue.json`, and `.blocked == false`. If the command exits non-zero, HALT before `/claim` and display the blocking dependency list from the artifact. The Phase 00 completion hook independently enforces the same file, hash, and `.blocked == false` checks.

EXECUTE: Derive `$ISSUE_TYPE` and `$BRANCH` from `tmp/${ISSUE_ID}/issue.json` before posting `/claim`:
- `$ISSUE_TYPE = fix` when a label lower-cases to `bug`, `fix`, `type:bug`, or `type:fix`, or the title starts with `fix:` / `bug:`.
- `$ISSUE_TYPE = feat` when a label lower-cases to `enhancement`, `feature`, `type:enhancement`, `type:feature`, or `type:feat`, or the title starts with `feat:` / `feature:`.
- Otherwise `$ISSUE_TYPE = chore`.
- `$ISSUE_SLUG` is the issue title lower-cased, ASCII-normalized, with non `[a-z0-9]` runs collapsed to `-`, trimmed of leading/trailing `-`, and truncated to 48 characters without a trailing `-`. If the normalized title has no `[a-z0-9]` characters, use `work`.
- `$BRANCH = ${ISSUE_TYPE}/issue-${ISSUE_NUMBER}-${ISSUE_SLUG}`.

Write `$BRANCH` to `tmp/${ISSUE_ID}/branch.txt`.
VERIFY: `$BRANCH` matches `^(feat|fix|chore)/issue-[0-9]+-[a-z0-9][a-z0-9-]{0,47}$` and `tmp/${ISSUE_ID}/branch.txt` contains exactly that value.

### Step 2: Detect repo context (portable) — delegate tech-stack-detector

EXECUTE: `Task(subagent_type="tech-stack-detector", ...)` to detect languages, frameworks, the test runner, and the build tool. Independently detect:
- `$DEFAULT_BRANCH` ← `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'`; if empty → `git remote show origin | awk '/HEAD branch/ {print $NF}'`.
- `$REQUIRED_CHECK` ← `gh pr checks` / branch-protection API (the check(s) that must be green to merge).
- `$TEST_RUNNER` ← from the detector (npm / pytest / cargo / …).
EXECUTE: Persist the detected stack to the phase-state file (fill `<L>`/`<F>`/`<P>` from the detector's findings) — without `--workflow=spec-sprint` the CLI fails "State file not found":
`devforgeai-validate phase-set-tech-stack ${ISSUE_ID} --json '{"language":"<L>","test_framework":"<F>","package_manager":"<P>"}' --workflow=spec-sprint --project-root=${PROJECT_ROOT}`
VERIFY: `$DEFAULT_BRANCH` is non-empty. If the remote default cannot be resolved → HALT → AskUserQuestion. Confirm the phase-state file now contains `detected_tech_stack` (else Phase 04's `build-test-contract` halts H-PHASE01-INCOMPLETE).
RECORD: `devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=00 --subagent=tech-stack-detector --project-root=${PROJECT_ROOT}`

### Step 3: Detect DevForgeAI sentinels → toggle the addendum

EXECUTE: Set `$DEVFORGEAI_SENTINELS = true` only if BOTH exist:
- `devforgeai/specs/context/` (directory), and
- `.github/workflows/python-cli-tests.yml` (file).
When true, apply `references/devforgeai-addendum.md` mechanics in later phases; otherwise use the runtime-detected equivalents in `references/portable-workflow.md`.
VERIFY: Display `"DevForgeAI addendum: ON"` or `"DevForgeAI addendum: OFF (portable mode)"`.

### Step 4: Ordered git/worktree pre-flight — delegate git-validator

EXECUTE: `Task(subagent_type="git-validator", ...)` for git availability + repo status + fallback. Then run the ordered pre-flight (full enumeration + the 4 pristine-main rules: `references/portable-workflow.md`):
1. **Connectivity + auth** — git remote reachable; if a PR will open, `gh auth status` authenticated. HALT→AskUserQuestion if not.
2. **Fetch** — `git fetch origin --prune`.
3. **Sync the local default (fast-forward ONLY)** — ff local `<default>` to `origin/<default>`. If it cannot fast-forward (diverged) → **HALT** (do not reset/force).
   **Untracked-collision recovery (distinct from divergence):** when `git merge --ff-only` exits non-zero with stderr matching `untracked working tree files would be overwritten`, this is NOT divergence — verify with `git rev-list --count origin/<default>..HEAD` = 0. Recovery: (a) for each named colliding file, `mkdir -p tmp/_framework/preflight-collision/ && mv <file> tmp/_framework/preflight-collision/<file-basename>`; (b) retry `git merge --ff-only origin/<default>`; (c) for each relocated file, `diff tmp/_framework/preflight-collision/<file-basename> <merged-path>`; (d) if diff exits 0 (byte-identical), `rm tmp/_framework/preflight-collision/<file-basename>`; else → HALT → AskUserQuestion (the relocated copy differs from the merged version — manual review required).
4. **Working-tree sanity** — abort if a merge/rebase/cherry-pick is in progress; stage with explicit paths, **NEVER `git add -A`**.
5. **Worktree hygiene + resume** — `git worktree prune`; then run the rehydration gate:
   `devforgeai-validate sprint-resume ${ISSUE_ID} --project-root=${PROJECT_ROOT} --format=json`
   - **Exit 0, `next_phase` != `"00"`** → bind `$WORKTREE_PATH`/`$BRANCH` from the JSON output;
     jump to the orchestration loop starting at `next_phase` (Phase 00 pre-flight still completes
     first — git/auth checks run regardless); skip Phase 03 worktree creation (already present).
   - **Exit 1** (no state file, truly fresh sprint) → continue with a standard Phase 00 flow.
   If a worktree/branch already exists for this issue with no checkpoint → RESUME it (idempotent).
VERIFY: git remote reachable AND local `<default>` is `0/0` with `origin/<default>`. Else HALT.
RECORD: `devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=00 --subagent=git-validator --project-root=${PROJECT_ROOT}`

> The worktree itself is created in Phase 03 (off the remote tip), NOT here.

### Step 5: Claim the issue

EXECUTE: (a) `gh issue view ${ISSUE_NUMBER} --json state,comments` — HALT via AskUserQuestion if not OPEN; (b) active-claim scan: a comment starting with `/claim` with no later `/release` from the same session and no merged linked PR → HALT/yield, reporting holder and timestamp; (c) otherwise write the claim body to `tmp/${ISSUE_ID}/claim-comment.md` and post via `gh issue comment ${ISSUE_NUMBER} --body-file tmp/${ISSUE_ID}/claim-comment.md` with body `/claim — spec-sprint session on branch <branch>, started <UTC ISO 8601>. Will /release on PR open or abandonment.`; (d) race-check: re-read comments; earliest `created_at` /claim wins; loser posts `/release — yielding to earlier claim` and HALTs; (e) write `tmp/${ISSUE_ID}/claim.json {issue_number, claimed_at, comment_url, branch, released: false}`.
VERIFY: `tmp/${ISSUE_ID}/claim.json` exists.
DEGRADATION: If `gh` is unavailable → log `WARNING: claim protocol skipped (gh unavailable)`; write `tmp/${ISSUE_ID}/claim.json {"skipped":"gh-unavailable"}`; continue — never block the sprint on a missing claim.

Full algorithm and race rule: `references/claim-protocol.md`.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=00 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to Phase 00.5 | Exit != 0: HALT
```
