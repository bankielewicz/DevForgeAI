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
  log. `schemas/` holds `events.schema.json`, `manifest.schema.json` and `progress.schema.json`; `manifests/` holds one manifest per
  tracked skill: `brainstorm.json` and `architecture.json`.
- `settings.py` resolves `progress.mode` and saves the user's choice in the YAML frontmatter of
  `.claude/devforgeai.local.md` (ADR-003 A3, ADR-006 D6).
- `prune.py` removes run and session folders older than the `retentionDays` setting, once per session
  and project root, at the session's first tracked run.
- Tests: `src/tests/progress/` covers every evaluator rule, the same results under `python3 -S`, the
  goldens, `settings.py`, `prune.py` and the adapter's structure.

## Adapter (`src/claude/DevForgeAI/hooks/`, SPEC-013)

- `hooks.json` declares one module, `./progress.tsx`, a Claude Code mod. It records each tracked skill
  run in `devforgeai/progress/` of the root the run opened in: `runs/<run>/`, and per session
  `sessions/<session-id>/current.json` and `adapter.log`. It evaluates the run and shows it in the
  status line and a band above the prompt.
- Observe mode is the default; the band's button switches to enforce mode through `settings.py`.
- Every use of `$` stays in `progress.tsx`'s top-level functions; `progress-core.ts` is pure.
  `claude plugin validate src/claude/DevForgeAI` checks what Claude Code reads from the module.
- Kit tests: `hooks/*.test.ts`, run by `claude plugin test src/claude/DevForgeAI`. They are not
  deployed.
- Plugin settings (`.claude-plugin/plugin.json` `userConfig`): `tracking` (`on` or `off`, default
  `on`) and `retentionDays` (default 30, from 7 to 3650).

## Loading the mod

- An installed plugin's mod loads only while Claude Code serves the hooks-modules rollout flag
  (`tengu_plugin_hooks_modules`, SPEC-013), and it reports load failures only in the debug log
  (`claude --debug`).
- `claude plugin test` in a folder with no mod prints "no hooks module to load" when mods can load.
- When `claude plugin test` says the switch was saved off, check `tengu_plugin_hooks_modules` in
  `~/.claude.json` and start one `claude -p` from a plain shell: the sandbox can't refresh that file.
- Before changing the adapter, read the saved mods docs in `docs/research/Claude/` (local only) and
  load the built-in `plugin-authoring` skill.
