# DevForgeAI Addendum (sentinel-gated)

**Applies ONLY when BOTH Phase 00 sentinels are present:**

- `devforgeai/specs/context/` (the constitutional context folder), AND
- `.github/workflows/python-cli-tests.yml` (the required-check workflow).

When either sentinel is absent, this file does **not** apply — use the
runtime-detected equivalents in `portable-workflow.md`. Phase 00 sets
`$DEVFORGEAI_SENTINELS` and toggles this addendum accordingly. Everything below
extends (never replaces) the portable core.

---

## Required check & CI

- The branch-protection required status check is **`Run Python CLI Tests`** (ADR-119).
  Detect this via the portable required-check detection; this addendum just names the
  expected value.
- Phase 06 completion still blocks on every non-skipped PR check whose terminal
  state is outside `SUCCESS`, `NEUTRAL`, `SKIPPING`, or `SKIPPED`, including
  non-required checks such as `test-installer`. "Non-required" only means GitHub
  branch protection does not require the check for merge; it does not make the
  check advisory for this skill.
- WSL jest OOM mitigation: run a bounded `unit/v3 + wizard + emit` sweep rather
  than the full jest suite locally; the Linux CI runs the full set.

## Worktree mechanics

- Create worktrees under `worktrees/<slug>` (project root — e.g. `worktrees/ISSUE-<n>`).
  No sandbox bypass parameter is needed — `worktrees/<slug>/.claude/` sits at a different
  absolute location than the protected `.claude/` root and is not in the sandbox
  `denyWithinAllow` list. A non-fatal `error: could not write config file .git/config:
  Device or resource busy` may appear (the sandbox blocks `.git/config` writes in the main
  checkout); the worktree is still created and functional — the 3-part existence check
  (worktree list, directory exists, `rev-parse HEAD`) is authoritative.
- Symlink `node_modules` (and `.venv`) from the main checkout.
- **jest cd-ordering (LEGACY `.claude/worktrees/` only):** for sprints on the old site,
  invoke as `cd <worktree>/.claude/… && npx jest tests/…`. Not needed for the new
  `worktrees/` site since the path contains no `.claude/` segment.
- Sandbox-unsafe git ops (rebase/restore/checkout/reset/pull --rebase) touch
  protected `.claude/` paths — see `operational-safety.md` Rule 4.

## Test placement (hook-fix cards)

- **Shell hook tests → `tests/hooks/`:** when a card's fix surface is `.claude/hooks/`, `src/claude/hooks/`, `.codex/hooks/`, or `src/codex/hooks/`, test-automator writes the failing shell test at `tests/hooks/test_<name>.sh` (depth 1). `hook-tests.yml` discovers tests via `find tests/hooks -maxdepth 1 -name 'test_*.sh'` (`.github/workflows/hook-tests.yml:81`); a test at `tests/${ISSUE_ID}/` is invisible to this harness. All other card tests stay at `tests/${ISSUE_ID}/`.
- The Hook Test Harness (`hook-tests.yml`) is non-required for GitHub branch protection,
  but a failing harness check is still a Phase 06 blocker under the all non-skipped
  checks policy.
- Verification: `devforgeai-validate run-tests ${ISSUE_ID} --path=tests/hooks/test_<name>.sh`.

## Coverage & drift gates

- **90% branch coverage on `src/cli/v3/**`** (ADR-101 D8) — do not add defensive
  fallbacks the engine guarantees (dead branches sink the gate).
- **CLI-reference drift gate** — changing an `install.js` flag requires
  `npm run docs:cli-ref` in the **same commit** or the drift step fails.

## Dual-path mirror & string hygiene

- **Dual-path mirror ownership** — Claude and Codex surfaces are separate ownership
  lanes. Every `src/claude/**` edit must be mirrored byte-identical to `.claude/**`;
  every `src/codex/**` edit must be mirrored byte-identical to `.codex/**`. Do not
  satisfy one lane by copying it over the other lane. `sync-verification.yml` checks
  each lane independently. Use a fresh Pattern-A marker (Edit/Write) or
  `env DEVFORGEAI_ALLOW_OPERATIONAL_EDIT=1 cp` (Bash) per `operational-safety.md`
  Rule 3.
- **Keep `STORY-NNN`/`ISSUE-<n>` ids out of the PR title** — a story-id in the
  title trips `qa-validation.yml`'s quality-gate (fails in PR context). Cite the
  issue number in the body instead.
- **Conviction-gate-safe strings** — a literal `devforgeai-validate phase-complete
  …--phase=X` + `STORY-NNN`/`ISSUE-<n>` inside a quoted arg to `gh`/`git`/`echo`
  can trip command matchers; prefer `--body-file` / split literals.
- **ADR-number collision** — sequential `max+1` ids minted on parallel branches
  can collide; renumber only your own colliding artifact.

## Completion gate (this skill)

When the sentinels are present, phase-05's required artifacts and anchors
(`run-tests`, executable AC transcript anchors, source-AC coverage, `ac-compliance-verifier`,
`anti-pattern-scanner`, and `coverage-analyzer`) plus `phase-complete --phase=05`
are enforced by `spec-sprint-completion-gate.sh` (PreToolUse[Bash], exit 2)
reading `devforgeai/feedback/ai-analysis/<id>/` and `tmp/<id>/`. The Claude hook
lane ships from `src/claude/hooks/` to `.claude/hooks/`; the Codex hook lane ships
from `src/codex/hooks/` to `.codex/hooks/`. See `phases/phase-05-qa.md` for the
exact emission order.

---

## Provenance

DevForgeAI-specific mechanics distilled from cross-session lessons. Each rule is
host-specific and intentionally excluded from `portable-workflow.md` so the
consumer-facing core stays clean.
