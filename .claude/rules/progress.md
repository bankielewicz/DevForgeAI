---
paths:
  - "src/claude/DevForgeAI/progress/**"
  - "src/claude/DevForgeAI/hooks/**"
  - "src/tests/progress/**"
---

# The progress tracker

The progress tracker is part of the `devforgeai` plugin, not a skill. ADR-006 sets its place in the
layered model; SPEC-012 specifies the core and SPEC-013 the Claude Code adapter. Their §9 tables list
each build's results and departures, and their Change Logs the history.

## Core (`src/claude/DevForgeAI/progress/`, SPEC-012)

- `evaluate.py` (standard library only) judges a skill run's checklist steps by evidence from an event
  log, and adds the run's `timing` and `usage` and each step's `reached` to its state (SPEC-012 v17, v18).
  `schemas/` holds six schemas, SPEC-012's DM-01 to DM-06 blocks, which a test keeps equal to the spec:
  `manifest`, `events`, `progress`, `odometer` (a ledger line), `chain` (`chain_state.py`'s output) and
  `history` (`history.py`'s); `manifests/` holds one manifest per tracked skill: `brainstorm.json` and
  `architecture.json`.
- `chain_state.py` (IF-03) lists the documents under `docs/specs/` with their id, status, version and
  upstream IDs; `history.py` (IF-04) totals the runs' states and the odometer ledger. Both are read-only,
  standard library only, and exit 0 when they print and 2 when they can't run. The dashboard (SPEC-016,
  not built yet) runs them.
- `settings.py` resolves `progress.mode` and saves the user's choice in the YAML frontmatter of
  `.claude/devforgeai.local.md` (ADR-003 A3, ADR-006 D6).
- `prune.py` removes run and session folders older than the `retentionDays` setting, once per session
  and project root, at the session's first tracked run. It never touches `odometer/`.
- Tests: `src/tests/progress/` covers every evaluator rule, the same results under `python3 -S`, the
  goldens, `settings.py`, `prune.py` and the adapter's structure.

## Adapter (`src/claude/DevForgeAI/hooks/`, SPEC-013)

- `hooks.json` declares one module, `./progress.tsx`, a Claude Code mod. It records each tracked skill
  run in `devforgeai/progress/` of the root the run opened in: `runs/<run>/`, and per session
  `sessions/<session-id>/current.json` and `adapter.log`. It evaluates the run and shows it in the
  status line and a band above the prompt.
- Observe mode is the default; the band's button switches to enforce mode through `settings.py`.
- Another plugin's `$.tool.call` is not recorded and ends no run (BEH-33). `/progress` prints the open
  run's progress (BEH-34). A row above the prompt warns when the context window's fuel is at or below
  `precompactWarnFuel`, and at `precompactRunFuel` the adapter runs `/devforgeai:precompact` once by
  itself through `$.command.run` (BEH-35, BEH-36); BEH-41's set of pending names makes that run's turn
  count as typed, so the handoff's work stays out of the open run.
- Each main-loop `turn.complete` with usage adds a `usage` event to the open run (BEH-40). Once a run has
  opened a root, the adapter also writes the session's odometer ledger,
  `devforgeai/progress/odometer/<session-id>.jsonl`, whole at each turn (SPEC-016 BEH-10, ERR-06); the
  dashboard pane itself is not built.
- Every use of `$` stays in `progress.tsx`'s top-level functions; `progress-core.ts` is pure.
  `claude plugin validate src/claude/DevForgeAI` checks what Claude Code reads from the module.
- Kit tests: `hooks/*.test.ts`, run by `claude plugin test src/claude/DevForgeAI`. They are not
  deployed.
- Plugin settings (`.claude-plugin/plugin.json` `userConfig`): `tracking` (`on` or `off`, default
  `on`), `retentionDays` (default 30, from 7 to 3650), and `precompactWarnFuel` (default 30) and
  `precompactRunFuel` (default 20), the share of the context window left, from 0 to 95 (0 turns the row
  off, or never runs the skill). A setting applies after `/reload-plugins`.

## Loading the mod

- An installed plugin's mod loads only while Claude Code serves the hooks-modules rollout flag
  (`tengu_plugin_hooks_modules`, SPEC-013), and it reports load failures only in the debug log
  (`claude --debug`).
- `claude plugin test` in a folder with no mod prints "no hooks module to load" when mods can load.
- When `claude plugin test` says the switch was saved off, check `tengu_plugin_hooks_modules` in
  `~/.claude.json` and start one `claude -p` from a plain shell: the sandbox can't refresh that file.
- Before changing the adapter, read the saved mods docs in `docs/research/Claude/` (local only) and
  load the built-in `plugin-authoring` skill.
