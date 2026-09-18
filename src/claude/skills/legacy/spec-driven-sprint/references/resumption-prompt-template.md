# Resumption-Prompt & Fill-Contract Template

The mechanical substitution contract for filling
`assets/spec-dashboard-template.html` → `issue-<n>.html` in Phase 03. Source of
truth: the template's own `<!-- TEMPLATE TOKENS -->` manifest (grep-verified
1:1 with the body). **30 unique tokens = 13 GLOBAL + 17 PER_PHASE.**

The token tables below are the canonical enumeration (one token per row).

---

## GLOBAL tokens (substitute once each)

| Token | Description |
|-------|-------------|
| `{{REPO_SLUG}}` | `<org>/<repo>` of the target repository |
| `{{ISSUE_NUMBER}}` | The bare issue number (e.g. `318`) |
| `{{ISSUE_URL}}` | Full URL to the issue |
| `{{SPRINT_TITLE}}` | Human title of the sprint (issue-derived) |
| `{{BRANCH_NAME}}` | The working branch (`<type>/<issue-slug>`) |
| `{{BASE_BRANCH}}` | The base/default branch the PR targets |
| `{{REQUIRED_CHECK}}` | The detected required status check name |
| `{{GENERATED_DATE}}` | Generation date (ISO) |
| `{{GOAL_TEXT}}` | The sprint Goal paragraph (Phase 01) |
| `{{WORKTREE_PATH}}` | Repo-relative worktree path |
| `{{PR_NUMBER}}` | PR number (empty until Phase 06 → `—`) |
| `{{PR_URL}}` | PR URL (empty until Phase 06 → `—`) |
| `{{RESUME_PROMPT_TEXT}}` | The rendered AI resumption prompt (see below) |

## PER_PHASE tokens (one expansion per PHASE_ORDER phase)

| Token | Description |
|-------|-------------|
| `{{PHASE_NUMBER}}` | Spec-sprint phase id — one of the PHASE_ORDER strings: `00`, `01`, `03`, `04`, `05`, `06`, `07` (zero-padded; NOT 1-indexed integers) |
| `{{PHASE_TITLE}}` | Sprint-phase title |
| `{{PHASE_STATUS}}` | `pending`\|`in-progress`\|`blocked`\|`done` (data-status only) |
| `{{PHASE_SUMMARY}}` | One-line card summary (empty auto-hides) |
| `{{PHASE_MISSION}}` | What the card does |
| `{{PHASE_REQUIRED_READS}}` | List slot — files to read first |
| `{{PHASE_VERIFICATION}}` | The named deterministic signal (command + exit) |
| `{{PHASE_FILES}}` | List slot — files to touch |
| `{{PHASE_ACCEPTANCE}}` | List slot — testable acceptance criteria |
| `{{PHASE_REFERENCES}}` | List slot — references |
| `{{PHASE_DATE}}` | Completion-notes: date (`—` if empty) |
| `{{PHASE_COMMIT}}` | Completion-notes: commit SHA (`—` if empty) |
| `{{PHASE_PR}}` | Completion-notes: PR (`—` if empty) |
| `{{PHASE_TESTS}}` | Completion-notes: tests added/total (`—` if empty) |
| `{{PHASE_COVERAGE}}` | Completion-notes: coverage (`—` if empty) |
| `{{PHASE_REVIEW}}` | Completion-notes: review verdict (`—` if empty) |
| `{{PHASE_FOLLOWUP}}` | Completion-notes: follow-up (`—` if empty) |

## Repeat-block markers

Expand BOTH blocks once per PHASE_ORDER phase (7 expansions, in order: 00, 01, 03, 04, 05, 06, 07) — the sidebar nav item and the
main-pane card:

- `PHASE_NAV:START` … `PHASE_NAV:END` (HTML comments, sidebar item)
- `PHASE_CARD:START` … `PHASE_CARD:END` (HTML comments, main-pane section)

**Hook and Phase 03 authorship:** The `spec-sprint-board-render.sh` PostToolUse hook is a
no-op when the board does not yet exist (ISSUE-643 fix) — it does NOT pre-render the board
from the raw template before Phase 03 runs. Phase 03 is the sole initial board author.
After Phase 03 writes the board, the hook re-renders it on each `phase-record`/`phase-complete`
call to patch `data-status` on the nav button and section elements.

---

## The 5 fill-contract rules (advisor-hardened against injection)

**Step 0 (before any substitution):** Delete the `<!-- TEMPLATE TOKENS -->` manifest comment block (template lines 2–12) from the output copy. This ensures the token-grammar VERIFY (`grep -oE '\{\{[A-Z_]+\}\}' <board> | wc -l`) counts only un-substituted `{{UPPER_SNAKE}}` tokens, never comment prose or legitimate brace sequences in content slots.

1. **HTML-escape every TEXT slot.** Trusted ≠ correct: an issue title with `&`, a
   verification command with `<`/`>`/redirects, or a path in angle brackets
   corrupts raw substitution. Escape `& < > "` in all scalar text tokens
   (SPRINT_TITLE, GOAL_TEXT, PHASE_TITLE, PHASE_MISSION, PHASE_VERIFICATION, the
   completion-notes cells, RESUME_PROMPT_TEXT). A content slot that legitimately
   contains a `{{UPPER_SNAKE}}`-shaped brace expression (e.g. a GitHub Actions
   variable reference in a `PHASE_VERIFICATION` slot) must HTML-escape both braces
   to their numeric entities (`{` → `&#123;`, `}` → `&#125;`) so the VERIFY does
   not count it as an unfilled token and the renderer does not collapse it.
2. **List/fragment slots are HTML, not text.** PHASE_REQUIRED_READS, PHASE_FILES,
   PHASE_ACCEPTANCE, PHASE_REFERENCES are injected as programmatically-assembled
   markup (one `<li>`/`<div>` per item) with each item's *inner text* escaped per
   rule 1 — never raw concatenation.
3. **PHASE_STATUS ∈ {pending|in-progress|blocked|done}.** Badge label/icon/color
   derive solely from `data-status`; unknown/empty → renders `pending`. The fill
   program sets only `data-status` — never a separate label.
4. **Progress is computed, never substituted.** No token for done/total/%; the
   inline `<script>` aggregates from `data-status` at load and after each reload.
5. **Empties → `—`.** Empty completion-notes cells substitute an em-dash; an empty
   PHASE_SUMMARY auto-hides.

---

## RESUME_PROMPT_TEXT — what the resume `<pre>` MUST contain

Modeled on the continuation-prompt "PROMPT TO CLAUDE" shape: issue number,
worktree path, branch, required reads, in-flight verification commands, the
"open this dashboard → find the first non-`done` card → run its verification →
continue → STOP-AND-ASK at the gate" instruction, and the current PR number if
open. Two elements are **MANDATORY** (a resumable board is useless without them):

1. **Self-reference path.** State the spec file's own **repo-relative**
   on-disk path (e.g. `tmp/ISSUE-<n>/issue-<n>.html`) so the resuming session can
   `Read`/`Edit` it. Phase 03 always writes to `tmp/${ISSUE_ID}/issue-<n>.html` —
   use that exact path. Repo-relative, OS-agnostic — never a `file:///C:/…`
   URL. The spec must not be moved after authoring; the hook always patches
   `tmp/${ISSUE_ID}/issue-<n>.html` and cannot follow a moved path.
2. **Update mechanism.** State that the `spec-sprint-board-render.sh` PostToolUse hook
   auto-updates `data-status` on BOTH the phase's nav button
   (`<button class="nav-link" data-target="phase-NN" data-status="...">`) AND its
   section (`<section class="phase" data-status="..." id="phase-NN">`) after each
   `phase-record` or `phase-complete` call — where `NN` is the PHASE_ORDER id (e.g.
   `phase-04` for Execute, `phase-05` for QA). A resuming session may also update
   these attributes manually using `Edit`, following `pending`→`in-progress`→`done`.
   State that the inline `<script>` recomputes the progress bar from `data-status` on reload.

---

## Provenance

Token contract grep-verified against `assets/spec-dashboard-template.html`
(manifest == body, 1:1). Fill rules + resume-prompt mandates carried forward from
the build-spec design (the two MANDATORY resume elements were added 2026-06-07
after a cold session could otherwise neither locate nor update the board).
