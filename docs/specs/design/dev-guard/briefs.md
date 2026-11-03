# Dev-guard mockups: the briefs for Claude Design

SPEC-019 v2 BEH-16 and BEH-17 (approved 2026-11-02). Four surfaces, one canvas, three directions each. A brief gives the
goal, the context, the real content, the states and two to four must-haves, with a style reference; it never prescribes a
layout or tokens (Bryan, 2026-10-10). Every board is a **terminal** surface drawn at three widths: full (60 columns or
more), medium (40 to 59) and compact (under 40). The mod draws with Claude Code's mods widgets (`Box`, `Text`, a
`Raster` for charts), so each board is monospaced text in a dark terminal. The canvas stays private unless Bryan shares
it. The exported boards go in `boards/` beside this file and are listed in SPEC-019 Appendix A with their sha256.

How to use a brief: paste one brief per request into Claude Design (`/design` followed by the brief), ask for three
directions, iterate, then export the chosen direction's board at each width. The session can do the same through the
Artifact tool's Design type.

Shared style reference for all four: Claude Code's own terminal surfaces (the status line, a tool-call block, an
AskUserQuestion dialog) and mod-builder's design bar, "dark, minimal, premium": thin `─` rules, a letter-spaced
masthead such as `D E V - G U A R D`, one accent colour, dim secondary text, no emoji, no rainbow, nothing that
flashes. Colour roles: accent, success, warn, error, dim.

---

## Brief 1: the refusal reason (SPEC-019 BEH-05)

**Goal.** When the guard refuses a tool call, the person reading the transcript sees in one glance which rule refused,
which file, and what to do next, so the next action is obvious and nobody argues with the guard.

**Context.** Claude Code's transcript shows a refused tool call as a block under the call. The text is read by the
model first and by the person second. It appears inside a long transcript, between other tool calls, so it must stand
out without shouting. It can be a few lines; it is not a pane.

**Real content.** The reason names three things, always in this order, and nothing else:
- the rule: `R1 (file tool)`, `R2 (Bash)` or `R3 (git commit)`;
- the first protected path, for example `src/claude/DevForgeAI/skills/ui/SKILL.md`;
- the remedy, which depends on the state:
  - no ticket: `Invoke /plugin-dev:create-plugin with the iteration's scope, then /plugin-dev:skill-development, and read each requiredReads file.`
  - a ticket that doesn't permit yet: what it lacks, one line each: `skill-development not loaded`; `not read in this ticket: docs/research/Claude/skills/skills.md`; `the main checkout's copy of docs/research/Claude/… was not found: capture it by its PROVENANCE.md recipe`.
  - the two protected files: `A person edits guard.json outside Claude Code; the mod's close writes ledger.jsonl.`
  - a worktree mismatch: `This ticket belongs to /home/bryan/Projects/DevForgeAI/.claude/worktrees/x; load the iteration from a session whose working directory is that worktree.`
  Sample, full:
  `dev-guard refused R1 (file tool): src/claude/DevForgeAI/skills/ui/SKILL.md is protected and no ticket permits it in this checkout. Invoke /plugin-dev:create-plugin with the iteration's scope, then /plugin-dev:skill-development, and read each requiredReads file.`

**States.** No ticket; a ticket that doesn't permit yet (with one, two or three missing items); the protected files;
the worktree mismatch; a guard failure (`guard.json` missing or invalid: `dev-guard refused: docs/process/plugin-workflow/guard.json is missing; a person restores it`); a hook error (`dev-guard refused (the guard failed closed): <error>`).

**Must-haves.**
1. Rule, path and remedy are each on their own visual line, in that order, at every width.
2. The remedy is copyable as typed commands (`/plugin-dev:create-plugin …`), not prose only.
3. At the compact width the path may wrap but is never cut.

**Three directions:** a plain three-line block; a bordered box with the rule as its title; a one-line summary with the
remedy folded beneath it.

---

## Brief 2: `/dev-guard`, the ticket pane (SPEC-019 IF-01)

**Goal.** A person types `/dev-guard` and sees, without reading the spec, whether plugin edits are allowed right now in
this checkout, and if not, exactly what is still missing.

**Context.** A pane in Claude Code's terminal, opened mid-turn (`immediate: true`), beside the conversation. It shows
and never writes. The checkout is a worktree under `.claude/worktrees/` or the main checkout. The pane is also what
the person opens after a refusal to see the state the refusal described.

**Real content.**
- Masthead: `D E V - G U A R D` and the checkout's branch and top level: `docs/spec-019-dev-guard · .claude/worktrees/spec-019`.
- The ticket: `pw-20261102T201500Z`, scope `ui v3 cycle C`, opened `2026-11-02 20:15 UTC` by session `1c98fbaa…`.
- The permit, as a checklist with a tick or a cross per line:
  - `create-plugin loaded 20:15:03`
  - `skill-development loaded 20:16:40` or `not loaded`
  - `read: Skill-authoring-best-practices.md (Read, 20:17:02)`
  - `read: The-Complete-Guide-to-Building-Skill-for-Claude.pdf (not yet)`
  - `read: skills/skills.md (Bash cat, 20:17:30)`
  - `reviewers observed: plugin-validator 20:40:12 · skill-reviewer not yet`
  - `refusals this ticket: 2`
- The verdict line: `Permits plugin edits in this checkout` or `Does not permit yet: 1 read missing, skill-reviewer not observed`.
- With no ticket: `No ticket for this checkout. Invoke /plugin-dev:create-plugin with the iteration's scope.`

**States.** Empty (no ticket); idle, not permitting (with what is missing); idle, permitting; done (just closed: `Closed 20:52:10, ledger line written`); error (`guard.json` missing or invalid, with the file named); folded (the status-line badge, for example `dev-guard · permits` or `dev-guard · 2 missing`); too narrow (the toast `Dev-guard needs a wider window. Widen it to see the pane, or watch the status line.`); focus (the pane focused: hotkeys `c` close, `l` log, `Esc`).

**Must-haves.**
1. The verdict (permits or not) is the first thing the eye lands on.
2. Each missing item is its own line with the remedy implied by its text.
3. The compact width keeps the verdict and the missing items only.
4. Nothing in the pane is a button that writes; `close` is a typed command.

**Three directions:** a checklist card; a two-column state board (ticket facts left, permit right); a single
status column with the verdict as a banner.

---

## Brief 3: `/dev-guard close` (SPEC-019 IF-02, BEH-09)

**Goal.** When a person types `/dev-guard close`, they see either that the iteration closed and what evidence the ledger
line carries, or every condition that failed, so they can fix each and type the command again.

**Context.** The same pane as Brief 2, shown after the typed command (never immediate: it writes). A close checks
seven conditions in order; a refusal lists each failing one. A success appends one line to `ledger.jsonl` and shows
the refusals of the iteration for review (Brief 4 follows).

**Real content.**
- Refused:
  - `Not closed. 3 conditions fail:`
  - `✕ origin: run from a nested claude -p (sdk); type the command yourself`
  - `✕ reviewers: skill-reviewer not observed in this ticket`
  - `✕ reports: no skill-reviewer report in docs/process/plugin-workflow/reviews/ with tree 1744e6c…`
  - `✕ plugin tree: 2 files modified, not committed: skills/ui/SKILL.md, skills/ui/references/briefs.md`
  - passing conditions shown ticked: `✓ skill-development loaded`, `✓ 3 of 3 required files read`, `✓ plugin-validator observed 20:40:12`.
- Succeeded:
  - `Closed pw-20261102T201500Z at 20:52:10 UTC.`
  - `Ledger line: tree 1744e6c3…, commit 26c4cfd…, reports 20261102T2040Z-plugin-validator-26c4cfd.md and 20261102T2047Z-skill-reviewer-26c4cfd.md, 2 refusals.`
  - `Next: commit docs/process/plugin-workflow/ledger.jsonl with the two reports (git add and git commit run without a ticket).`
  - then the refusal review (Brief 4).

**States.** Refused (one, several or all conditions failing); succeeded; error (the ledger couldn't be written: `ledger.jsonl could not be written: <error>; nothing was closed`); no ticket (`No ticket to close in this checkout`); too narrow; folded (`dev-guard · closed`).

**Must-haves.**
1. Every failing condition is a line that says what to do, and passing ones are visibly ticked, so the person sees progress across attempts.
2. The success shows the ledger line's evidence (tree, commit, both reports, the refusal count) and the next command.
3. The verdict word (`Closed` or `Not closed`) is unmistakable at every width.

**Three directions:** a checklist with ticks and crosses; a receipt-style card for the success; a compact
condition table.

---

## Brief 4: `/dev-guard log`, the refusal view (SPEC-019 IF-04, the data view)

**Goal.** A person reviewing an iteration (at its close, or any time) sees what the guard refused, how often, and by
which rule, and can tell a right refusal from an allowlist gap at a glance.

**Context.** A pane. The data comes from the per-session refusal logs (one JSON line per refusal: time, rule, tool,
path, full command, ticket, reason). This is the one surface with charts, and its charts follow the **dataviz** skill's
guidance: a brand-neutral palette, accessible contrast in light and dark, one form per question, no decoration.
Charts in a terminal are rows of cells (`Raster`) or bars of characters, at most a few colours.

**Real content.**
- Masthead: `D E V - G U A R D · L O G` and the checkout.
- Counts for the open ticket and for the last seven days, by rule (`R1 4 · R2 7 · R3 1 · catch 0 · guard.json 0`) and by tool (`Edit 3 · Write 1 · Bash 8`).
- A seven-day timeline: refusals per day as a small bar row, today at the right.
- The list, newest first, one refusal per row: time, rule, the first protected path, the command's first 60 characters; a row expands (Enter) to the full command text and the reason.
- A marker on rows the person can act on: `allowlist?` where the command matched no entry and was read-only in spirit (a `diff`, a `cat` with a redirect), so the close review can turn it into a `guard.json` change.

**States.** Empty (no refusals: `No refusals in this checkout yet.`); idle (the list and counts); live (a new refusal arrives while open: the row is added, the counts tick, nothing flashes); done (n/a: the log has no end); error (a log file that can't be read is named and skipped); folded (`dev-guard · 12 refusals`); too narrow; focus (row selection, `Enter` expands, `Esc` returns).

**Must-haves.**
1. The counts by rule and the seven-day bars are readable without colour (shape and label carry the meaning).
2. A row shows the full command text on demand, never truncated silently.
3. The compact width keeps the counts and the newest three rows.
4. The palette follows the dataviz skill's categorical and sequential guidance; the error role is reserved for `catch` and `guard.json` refusals.

**Three directions:** a dashboard (counts and bars on top, the list below); a list-first view with a thin summary
line; a timeline-first view where each day expands into its rows.
