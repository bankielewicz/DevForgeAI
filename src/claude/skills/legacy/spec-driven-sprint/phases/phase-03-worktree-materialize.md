# Phase 03: Worktree + Materialize HTML Spec

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=01 --to=03 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 01 incomplete → HALT
```

## Contract

PURPOSE: Create the isolated worktree off the remote default tip, then fill the dashboard template at the canonical path `tmp/${ISSUE_ID}/issue-<n>.html`.
DELEGATES TO: `git-worktree-manager` (discover / idle-detect / max-limit — **report-only**; the orchestrator performs the create + verify). Delegation, NOT gate-enforced (#413).
GATE: spec materialized at `tmp/${ISSUE_ID}/issue-<n>.html`.

---

## Mandatory Steps

### Step 1: Create the worktree — discovery delegation, then orchestrator-performed create

EXECUTE — in three ordered actions:

(a) **Discovery delegation (report-only).** `Task(subagent_type="git-worktree-manager", ...)` to DISCOVER only — read its `action_needed ∈ {RESUME, REPAIR, CREATE, NONE}`, the resolved worktree path, and the idle/limit report. `git-worktree-manager` is **report-only by contract** (`.claude/agents/git-worktree-manager.md`: "never run `git worktree create/remove/repair` … the command decides and acts") — it does NOT create the worktree. A `status:SUCCESS` / `action:"CREATE"` report is a *recommendation*, not evidence that a worktree exists.

(a.1) **Limit-reached gate.** After reading the discovery result from step (a), check `result.limit_reached`:
- If `limit_reached == true` **AND** `action_needed == "CREATE"`: **HALT.** Use `AskUserQuestion` to surface the over-cap condition — header: `"Worktree cap reached"`; body: present `active_count` (non-idle worktree count) vs `config.max_worktrees`; if `idle_worktrees` is non-empty, list them (path + days_idle) as low-risk removal candidates, noting that removing an idle worktree does NOT lower `active_count` (idle worktrees are already excluded from the cap count — per `git-worktree-manager.md:106`); options: (1) `"Remove an active worktree"` — run `git worktree list` to select a non-idle worktree, run `git worktree remove <chosen-path>`, then re-run step (a) discovery; (2) `"Proceed anyway"` — explicit user override, continue to step (b); (3) `"Abort sprint"` — HALT without creating the worktree.
- If `limit_reached == false` (or `action_needed != "CREATE"`): proceed to step (b) with no prompt.

(b) **Orchestrator-performed create.** The orchestrator itself runs `git worktree add` branched off `origin/${DEFAULT_BRANCH}` with branch `${ISSUE_TYPE}/<issue-slug>`, NOT off local default (defense in depth — the pre-flight already ff-synced it). Then resolve deps in the worktree (symlink/install `.venv` / `node_modules`).
- **DevForgeAI addendum** (when `$DEVFORGEAI_SENTINELS`): worktree under `worktrees/` (project root — NOT `.claude/worktrees/`). Before `git worktree add`, run: `git check-ignore -q worktrees/probe 2>/dev/null || echo 'worktrees/' >> .git/info/exclude` to ensure consumer repos gitignore the site locally. The `worktrees/<id>` site is inside the project root (`.` is in the sandbox write-allowlist) — no bypass parameter required. A non-fatal `error: could not write config file .git/config: Device or resource busy` may appear (sandbox blocks `.git/config` in the main checkout); the worktree is still created and functional — use the 3-part existence check in step (c) as the authoritative signal. Shared `.git/*.lock` wait-and-retry (never `rm`). See `references/devforgeai-addendum.md`.

(c) **Deterministic existence VERIFY.** Assert ALL of the following before RECORD — a subagent SUCCESS report is NOT sufficient evidence:
  1. `git worktree list --porcelain` contains the resolved worktree path, AND
  2. `test -d <worktree-path>` succeeds, AND
  3. `git -C <worktree-path> rev-parse HEAD` equals `origin/${DEFAULT_BRANCH}`.
If any check fails → HALT (the worktree was not actually created, regardless of what the subagent reported).
RECORD: `devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=03 --subagent=git-worktree-manager --project-root=${PROJECT_ROOT}`
BIND: Set `$WORKTREE_PATH` to the verified path immediately after RECORD (e.g. `WORKTREE_PATH="${PROJECT_ROOT}/worktrees/${ISSUE_ID}"` — absolute, matching the hook's absolute-path comparison). On resume, re-derive via `git worktree list --porcelain | awk '/^worktree /{wt=$2} /ISSUE-/{if (index(wt, ENVIRON["ISSUE_ID"])) {print wt; exit}}'` — session memory does not survive context resets.

### Step 2: Set the canonical board path

EXECUTE: The board is always written to `tmp/${ISSUE_ID}/issue-<n>.html`, where `<n>` is the digit-run from `${ISSUE_ID}` (e.g. `ISSUE-616` → `issue-616.html`). This is the path `render_sprint_board.py:290` hardcodes; the `spec-sprint-board-render.sh` PostToolUse hook cannot follow worktree-commit or hybrid paths. Set `$BOARD_PATH = tmp/${ISSUE_ID}/issue-<n>.html` and create the directory: `mkdir -p tmp/${ISSUE_ID}`.
VERIFY: `$BOARD_PATH` is set and the directory `tmp/${ISSUE_ID}/` exists.

### Step 3: Fill the template

EXECUTE: Call `devforgeai-validate render-sprint-board --init-board ${ISSUE_ID} --title "<HTML-escaped issue title>" --branch "${BRANCH}" --base "${DEFAULT_BRANCH}" --worktree "${WORKTREE_PATH}" [--required-check "${REQUIRED_CHECK}"] --generated-date "YYYY-MM-DD" --project-root=${PROJECT_ROOT}` to initialize the board from the template. The CLI deletes the `<!-- TEMPLATE TOKENS -->` comment block, expands the `PHASE_NAV` and `PHASE_CARD` marker blocks (one copy per PHASE_ORDER phase: 00, 01, 03, 04, 05, 06, 07 — with constant phase titles), fills the 10 automatable GLOBAL tokens (SPRINT_TITLE, BRANCH_NAME, BASE_BRANCH, REQUIRED_CHECK, GENERATED_DATE, WORKTREE_PATH, REPO_SLUG, ISSUE_NUMBER, ISSUE_URL; PR_NUMBER and PR_URL default to `—`), and replaces all remaining tokens (GOAL_TEXT, RESUME_PROMPT_TEXT, per-phase content) with `—`. The `spec-sprint-board-render.sh` hook is a no-op when the board does not yet exist (ISSUE-643 fix); Phase 03 is the sole initial board author. Then use `Edit` to fill: (1) the GOAL_TEXT paragraph, (2) the RESUME_PROMPT_TEXT (see `references/resumption-prompt-template.md` for the two mandatory elements — self-reference path and update mechanism), and (3–9) each of the 7 phases' content slots (PHASE_MISSION, PHASE_REQUIRED_READS, PHASE_VERIFICATION, PHASE_FILES, PHASE_ACCEPTANCE, PHASE_REFERENCES) — one `Edit` per phase, replacing the `—` placeholder in each slot with authored content. On **resume** (Phase 03 already completed in a prior session, board file present), **Read the board first** before Writing — the Write tool requires a prior Read on any file it overwrites. HTML-escape all text in `Edit` calls; assemble list slots as `<li>`/`<div>` with escaped inner text.
VERIFY: 0 `{{TOKEN}}` leak (`grep -oE '\{\{[A-Z_]+\}\}' tmp/${ISSUE_ID}/issue-<n>.html | wc -l` → 0); SPRINT_TITLE slot populated (not `—`); at least one PHASE_MISSION slot populated (not `—`); the inline `<script>` recomputes progress on load.

### Step 4: Preview

EXECUTE: Report the materialized spec's path to the user (e.g. "Spec written at `<path>` — open it in a browser to track progress"). Do NOT invoke a file-send tool — none is registered in Claude Code; present the file by disclosing its on-disk path.
VERIFY: The user has been told the spec's path.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=03 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to Phase 04 | Exit != 0: HALT
```
