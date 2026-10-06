# DevForgeAI Drive: the dashboard

**Status:** design proposal, not approved. Nothing here is built into the plugin. It replaces the views, layouts,
graphics and buttons of `devforgeai-progress-ui.md` (its sections 2, 6, 8 and 9). That document's manifests, step
states and gates (its sections 4 and 5) are built, as SPEC-012 and SPEC-013. This document changes no spec, skill or
plugin version: the specs it asks for are listed in section 12.

**Date:** 2026-10-06. **Author:** claude-code (session 7637882f-b2ec-465e-988a-9602340d1023), at Bryan's request,
reviewed with the advisor.

**Sources:**
- the plan, `tmp/plans/2026-10-06-dashboard.md`, which quotes each of Bryan's decisions with its date (local only:
  `tmp/` is gitignored);
- the design canvas "DevForgeAI Drive" (claude.ai artifact `RwsfT8oYuzcebLfvhPtuW1`, private to Bryan): three looks,
  each at 160×48, at 120×36, with the tile menu open and docked at 64×48, plus the colour tokens;
- the working prototype, a throwaway mod in `tmp/probes/drive-probe/` (local only), run live in Bryan's terminal on
  2026-10-06 (section 13);
- the mod API in Claude Code 2.1.291 (the `plugin-authoring` skill and its `claude-code.d.ts`); the API is early
  access and changes between releases;
- `devforgeai-claude-mods.md` (proposal), its design rules (section 3), and SPEC-013 v21 (approved, not built).

## Contents

1. Purpose and the decisions behind it
2. What it shows
3. Layouts
4. Looks
5. The instruments
6. The route and the ETA
7. The agents window
8. The guardrails panel
9. Keys, the tile menu and what reaches the model
10. Commands and settings
11. Where each piece of data comes from
12. The specs this needs
13. Verified and unverified
14. Build order
15. Open questions for the owner

## 1. Purpose and the decisions behind it

Bryan, 2026-10-05: "the dashboard is more appropriate, I feel as it will empower a normal user the ability to drive
claude code from one part of the framework through each phase/skill"; "my tesla's model y's tablet but designed for
claude code with devforgeai as its framework & mods as the guardrails".

The dashboard is one pane. It shows where the project stands in the chain (Brainstorm, PRD, Architecture, Context,
Epic, Story, Spec), what Claude is doing and how hard it is working, how much context is left, which guardrails
are armed, and it starts the next phase's skill when you ask it to. It extends PRD-001 FR-021 ("show the run's
progress to the user"); the instruments, the route and starting skills go beyond FR-021 (open question 7).

Bryan's decisions, all 2026-10-05 or 2026-10-06 (the plan quotes each in full):

| Decision | His words |
| --- | --- |
| Drawn in the terminal, uniform tiles, modern | "Drawn in the terminal": "uniform sized button where each button is the same size/shape. make it look modern like it's from 2026 and not 1990" |
| A tile asks, the pick runs | the click returns a question asking what you'd like; "Run what I pick (Recommended)" |
| Real gauges | "dray actual gauges as this will be a nice add"; RPM and fuel; mileage = "the aggregate of tokens for the entire framework usage" |
| An SVG version for the desktop app | "the design should include an svg version for the desktop app" |
| Terminal first | "option 1 but let's introduce colors into the dashboard to 'liven' it up" (after mods were seen not to load in the desktop app's WSL chat) |
| Three looks, chosen by preference | "perhaps have a configurable option where a user can select via preference ... i love the variety" |
| Docking | "present & configurable in the terminal as in right side with a docking option" |
| Look A's name | "change model y to default for look"; "the look still has the Model Y label" |
| Fuel counts down | "start at 100% when context is cleared and as context is filling up, reduce it. at 30%, provide a warning that precompat will run at 20%" |
| Command name | "/devforgeai:probe as 1st choice but if that cannot happen, /devforgeai-probe is acceptable" |
| The third dial | "Pace (Recommended)" |
| Prototype-only controls removed | "[ fuel: demo ] & [ 3rd dial: pace ] ... if no merit, let's remove them" |
| Enforce as a button | "will enforce be a button we can toggle?" (yes: SPEC-013 BEH-13) |

## 2. What it shows

| Area | Shows |
| --- | --- |
| Header | DevForgeAI Drive, the look's name and `t` |
| Route | seven identical tiles, one per phase: glyph, name, the document it produced, its state, the hotkey `[1]` to `[7]` |
| Navigation | "▼ YOU ARE HERE", the route travelled and still to go, the ETA chip |
| Instruments | RPM, FUEL and PACE dials, the odometer and the trip-computer line (section 5) |
| Agents | the running subagents and their tool calls as a tree (section 7) |
| Guardrails | the armed guardrails and the last hold (section 8) |
| Log (Default, Night drive) or Telemetry (Race telemetry) | the run's recent events, or the session's numbers (wide layout only) |
| Status bar | the current skill and step, the mode chip (ENFORCE or OBSERVE), flags, and the fuel chip |
| Controls | Look, Switch to observe/enforce, Pause, Close, and the phase keys |

The status line, the progress band and the toasts of SPEC-013 stay as they are; the dashboard is the pane they
lead to. All values in the mockups and the prototype are sample data, except where section 13 says a reading was
live.

## 3. Layouts

The layout follows the pane's width (`e.props.bodyColumns`), read at each draw:

| Layout | Size | When | Arrangement |
| --- | --- | --- | --- |
| Docked | 64×48 | the pane is docked (fullscreen layout, terminal at least 110 columns), or narrower than 120 | the seven phases as stacked full-width strips joined by `▼`; you-are-here and ETA; the three dials side by side with the odometer; agents; one guardrails line; status bar |
| Compact | 120×36 | inline, 120 to 159 columns | the seven tiles in a row (15×7 each); navigation; dials and agents side by side; guardrails across the width; status bar |
| Wide | 160×48 | inline, 160 columns or more | the tiles in a row (19×9 each); navigation with start, ship and per-phase times; dials, odometer and agents; guardrails beside the log or telemetry; status bar |

Docked was seen on the **right**, full height, at the width the mod asked for (section 13). The side is Claude
Code's: a mod requests only a width (`$.ui.open` `columns`), and a width the person drags wins. The canvas has every
layout in every look; the prototype draws all of them from one engine.

## 4. Looks

Three looks share one layout and differ only in colour tokens and tile styles. The canvas's "Color tokens" board
lists every token for each look.

| Look | Character | Tiles |
| --- | --- | --- |
| **Default** | graphite, one electric-blue accent | thin rounded borders; the tile in progress tinted blue |
| **Night drive** | navy to violet, neon gradients | heavy borders, a gradient inside each tile, a glow around the current and next tiles, glowing needles |
| **Race telemetry** | black pit wall, amber and lime data | a coloured header strip per tile, numbered dial ticks, a telemetry panel in place of the log |

The canvas still names the first look "Model Y"; it is **Default** everywhere else (Bryan, 2026-10-06).

**Choosing.** A `/config` setting picks the look; Default is its default. `t` cycles the looks while the pane is
open. ADR-006 point 3 says mods are configured only through Claude Code's plugin settings (`userConfig`), so `t`
writes that same setting with `$.config.set` rather than keeping its own copy. `$.config.set` changes a `/config` row
"as if the person did in the menu" (the 2.1.291 types); that it works on a plugin's own `userConfig` row is
unverified (section 13). If it doesn't, `t` changes the look for the session only.

## 5. The instruments

**RPM: output tokens per second.**
- A pass-through `turn.step` hook times each model request: from the first streamed chunk (text, thinking or tool
  input) to the stop chunk. At the stop chunk, the request's `usage.output_tokens` divided by that time is the
  reading.
- While a request streams, the needle follows an estimate from the text so far (four characters a token). After
  the stop it falls back to 0 over five seconds, an engine returning to idle.
- The dial runs 0 to 200, with the redline from 150.
- Only the main loop counts (no `agentId`). The prototype read 81 tok/s live (section 13).

**FUEL: context left.**
- FUEL is 100 minus `context.percent` from `session.measure`. It reads 100 when nothing is measured: a fresh
  session, after `/clear`, and right after a compaction.
- It is amber from 30% and red from 20%. At 30% the fuel chip reads "▲ Fuel 28% · precompact runs at 20%". At 20%
  `/devforgeai:precompact` runs, and the chip reads "● Fuel 18% · running /devforgeai:precompact".
- These are the moments SPEC-013 v21 fixes: `precompactAt` 70 and `precompactRunAt` 80 of the window used are 30%
  and 20% of fuel. The dashboard only counts the other way. Whether v21's own row and settings switch to fuel wording
  is open question 2.
- Fuel is the share of the whole window. On a 1M-token window, 20% fuel is 800k tokens used, which may come after
  an automatic compaction (SPEC-013 v21 §13).

**PACE: progress along the route.**
- PACE is how fast the work advances: the steps reached in the open run per hour of active time, where gaps of more
  than 30 minutes between events don't count (the tracker's idle limit). It is shown as 0 to 100, scaled so 100 is
  one step a minute, with "min/step" under it. With no run open it reads 0.
- **Wheel-spin:** RPM high while PACE stays near 0 means Claude is spending tokens and no step is finishing. The dial
  turns amber and reads "▲ WHEEL-SPIN". That is the condition the tracker's stuck notice (SPEC-013 BEH-25) already
  detects, shown all the time. The exact rule (how high, how long) is open question 9.
- Chosen over cache efficiency, burn ($/hour) and no third dial by the advisor's test (deterministic from data the
  tracker has, distinct from the other instruments, readable at a glance, and something you act on) and by Bryan
  ("Pace (Recommended)").

**The odometer: lifetime tokens.**
- The odometer is every token DevForgeAI's tracked runs have used in this project ("the aggregate of tokens for the
  entire framework usage"). It is drawn as rolling digit drums, with the last digit in the accent colour.
- Runs are pruned after `retentionDays` (SPEC-013 DM-06), so the total lives in a ledger the pruning keeps (section
  11). Which tokens count (input, output, cache reads) is open question 10.

**The trip-computer line.** A line of text under the dials, not a dial: the prompt-cache hit rate, dollars per hour,
time to first token (measured by the same `turn.step` timing), and the session's tokens and cost.

## 6. The route and the ETA

**Tiles.** Each phase's tile draws one of these states:
- done ✓, with steps and time;
- in progress ●, with a progress bar and "step N of M";
- next, as a NEXT chip;
- not started ○, with an estimate;
- not built yet, dashed and "coming soon". Story and Spec are in this state today: the story skill is SPEC-009
  (draft), and only PRD-001 FR-017 covers the Spec step.

A phase's state comes from the project's documents and the tracker's runs: `chain_state.py` (section 11) and the
open run.

**ETA.**
- For each phase still ahead: the median active time of the past runs of that phase's skill in this project.
  Active time is the run's span, less any gap over 30 minutes.
- The ETA is the sum of those medians up to the last phase that has history. The chip reads, for example, "ETA ~1 h
  50 m to Epic · Spec —".
- A phase with no history, or with no built skill, shows "—", never a guess (Bryan's preference for deterministic
  logic).

## 7. The agents window

The tree lists the session's subagents and their tool calls:
- main;
- each agent with a status dot (running yellow, done green, failed red) and its elapsed time;
- under an agent, its recent tool calls.

**Sources:** `agent.spawn` (a new agent, its description and parent), `tool.call` with an `agentId` (its calls),
`turn.complete` with an `agentId` (its end), and `$.agent.list()` for agents that started before the mod loaded.
Reusable code: agent-radar's `adopt()` and `describe()`, and mission-control's tree helpers `lines()`, `took()` and
`icon()` (MIT, claude-code-mods).

**What stays unrecorded.** SPEC-013 DM-01 skips every event with an `agentId`, and that stays. The agents window
lives in the adapter's memory for drawing only, never in a run's events.

## 8. The guardrails panel

It lists only guardrails that exist:
- the write gate (SPEC-013 BEH-08);
- the question gate (BEH-21);
- the exit confirmation (BEH-28);
- the other-mods filter (BEH-33, v21);
- precompact at 20% fuel (BEH-35 and BEH-36, v21).

It also shows the mode (ENFORCE or OBSERVE) and the last hold, from `adapter.log` lines of kind `refused`. The
proposed guards of `devforgeai-claude-mods.md` (A1 dev-guard, B2 document-guard, B3 merge-gate) are not drawn until
they exist. The line "fails open: if the tracker stops, the work goes on and you are told" restates ADR-006 D1.

## 9. Keys, the tile menu and what reaches the model

**Keys first.** Every control has a key, and keys work in every terminal:

| Key | Does |
| --- | --- |
| `1` to `7` | opens that phase's menu |
| `t` | switches the look |
| `m` | switches observe and enforce |
| `a` | pauses or resumes the motion |
| `q` | closes the pane |

**Clicks are a bonus.** Clicks reach a mod's Buttons only where the terminal reports them. In Bryan's cmux terminal
no click reached Claude Code, not even its own pane close button (section 13). The drawn tiles are one Raster, which
can't be pressed. Clickable tiles need each tile drawn as a keyed Box holding a plain Button (open question 1).

**The tile menu.** A key, or a click where clicks arrive, opens `$.ui.ask` with "<Phase>: what would you like to
do?" and the options that apply:
- Continue from step N, when an unfinished run is offered;
- Start a new <phase> run;
- Open <document>;
- Cancel.

Not-built phases toast "the skill isn't built yet". The person's pick is their decision, and `$.command.run` runs
the skill as if they had typed it. SPEC-013's exit confirmation applies as it does to a typed skill.

**This changes a recorded rule.** "Buttons that start work fill the prompt box; they never send it" appears in
`devforgeai-progress-ui.md` §9, in `devforgeai-claude-mods.md` design rule 5, and in SPEC-013's PRD-001 FR-003 link
note ("no button sends a prompt"). The new rule: **a button that starts work asks first, and the person's answer is
the go-ahead.** A button never runs work without an answer. Nothing decides a disposition, status, priority or
approval. The SPEC-013 link note changes with SPEC-013's next version.

**The mode button.** "Switch to observe" / "Switch to enforce" is SPEC-013 BEH-13's switch: it runs IF-02, saves
the choice in the local preference file, changes the mode at once, confirms with a toast, and is unavailable when
the project locks the mode (ADR-006 D3). The dashboard's chips redraw from it.

**What reaches the model.** Nothing new. The dashboard draws and starts skills on your answer; it adds no context
and refuses nothing. The tracker's enforce-mode refusals are the model's only signal, as now.

## 10. Commands and settings

**The command.**
- A mod's own command names allow letters, digits, `_` and `-` (the 2.1.291 types), so `$.command.register` cannot
  give `/devforgeai:<name>`. The prototype is `/devforgeai-probe`.
- Inside the `devforgeai` plugin, a command file (`commands/<name>.md`) would list as `/devforgeai:<name>`, and a
  `command.run` hook could answer it by opening the pane. This is unverified (section 13).
- SPEC-013 v21's `/progress` becomes a way to open the dashboard.
- The command's name is open question 3.

**Settings** (`userConfig`, shown in `/config`, the person's and not policy, like `tracking` and `retentionDays`):

| Setting | Values | Default |
| --- | --- | --- |
| `dashboardTheme` | Default, Night drive, Race telemetry | Default |
| `dashboardWidth` | the docked width asked for, in columns | 66 |
| `dashboardAutoOpen` | open by itself at session start | off; Claude Code seats an unasked pane only from 144 columns, or 110 once the person has opened it before |
| `precompactAt`, `precompactRunAt` | SPEC-013 v21 DM-07, DM-08 | 70, 80 (context used); 30% and 20% of fuel |

## 11. Where each piece of data comes from

The design rests on one split, following `devforgeai-claude-mods.md` rule 2 and SPEC-013 §1 ("the event log is the
truth"):
- **Anything derivable from the event logs goes in the evaluator** (Python, SPEC-012), so the Codex port and
  `progress.html` get it too.
- **Only live host readings stay in the adapter** (SPEC-013).

| Data | Source | Where |
| --- | --- | --- |
| Phase states, documents | `chain_state.py` (planned since SPEC-012 §11, not written): each document under `docs/specs/` by type, status and version | evaluator side, a new script |
| Per-run active time, per-step times | `runs/*/events.jsonl` times, gaps over 30 min removed | evaluator, in `state.json` |
| PACE | steps reached per active hour of the open run | evaluator, in `state.json` |
| ETA | medians of past runs' active time per skill | evaluator, from `runs/*` |
| Per-run token totals | each turn's usage, recorded as an event | adapter records it; evaluator totals it |
| Odometer | a ledger, `devforgeai/progress/odometer.json`, that `prune.py` keeps | evaluator writes, prune keeps |
| RPM, time to first token | `turn.step` timing | adapter, live only |
| FUEL | `session.measure` `context.percent` | adapter, live only |
| Cache hit rate, $/hour | `turn.complete` usage, `$.session.usage().cost` | adapter, live only |
| Agents | `agent.spawn`, `tool.call`/`turn.complete` with `agentId`, `$.agent.list()` | adapter memory, never in events |
| Guardrails, last hold | the mode, `adapter.log` kind `refused` | adapter |

## 12. The specs this needs

| Spec | What it gets |
| --- | --- |
| **SPEC-016** (new) | the dashboard: views, layouts, looks, instruments' definitions, the tile menu, keys, settings, and VER items (kit tests per look and layout, live checks) |
| **SPEC-012**, next free version | `chain_state.py`; active time, per-step times and PACE in `state.json`; a usage event kind and per-run token totals; the odometer ledger; ETA inputs |
| **SPEC-013**, next free version | the pane and its command; the RPM and FUEL readings; the agents window's memory; the settings; the FR-003 link note's new wording; `prune.py` keeping the ledger |

SPEC-013's number depends on the save-the-work cycle, which plans its next change as v22 on top of v21. This
design takes the next free number when its specs are drafted. PRD-001 may need a requirement for the dashboard
(open question 7).

## 13. Verified and unverified

**Verified on 2026-10-06** with Claude Code 2.1.291, in Bryan's terminal (cmux, the worker1 tab), with the
prototype unless noted:

| Fact | How |
| --- | --- |
| A mod pane docks on the right, full height, at the requested width, in the fullscreen layout | `CLAUDE_CODE_NO_FLICKER=1`; the pane said "placed dock · 112 columns · fullscreen true" |
| On the main screen, the pane opens inline above the prompt | "placed inline · 193 columns · fullscreen false" |
| Braille dials, block drums and 24-bit colour render and animate; a 160×48 Raster repaints at 5 a second with `$.ui.blit` | the prototype's dashboard, all three looks, by eye |
| `Image` draws nothing in cmux | `$.ui.blit` refused: "the terminal draws no placeholder images (probe: graphics reply OK, terminal libghostty)" |
| `$.command.run` starts a plugin skill from a Button press | `/devforgeai:spec-lookup SPEC-013` ran; the tracker opened a run |
| The same call works from `session.measure` (SPEC-013 v21 BEH-36's path) | after a turn's end, `/devforgeai:spec-lookup SPEC-014` ran by itself |
| `turn.step` timing gives tokens per second | "218 tok in 2.7 s = 81 tok/s (2.3 s to first token)" |
| `$.ui.ask` from a key draws the engine's question dialog | key 4: "Context: what would you like to do?", Esc cancelled |
| Mouse clicks don't reach Claude Code in cmux | neither a mod Button (a `ui.press` logger saw nothing) nor the pane's own ✕ responded; keys did |
| The desktop app's WSL chat loads no mods | context-bar showed in the terminal "but not in the chat session of claude code desktop app" (Bryan) |
| A mod's command name allows no colon | `CommandSpec.name`: letters, digits, `_`, `-` |

**Unverified**, each with its check:

| Question | Check |
| --- | --- |
| Does `$.config.set` change the plugin's own `userConfig` row, and does the module see it without a reload? | a probe that switches the look with `t` and reads `/config` |
| Does `commands/<name>.md` in the plugin plus a `command.run` hook give `/devforgeai:<name>` that opens the pane without loading a prompt? | a probe in a scratch copy of the plugin |
| Do clicks reach Buttons in Windows Terminal? | the prototype in a Windows Terminal WSL tab |
| Does an `Svg` dashboard draw in the desktop app's Code tab on a Windows-path project, and how does it animate? | a desktop probe on a Windows project |
| Does the pass-through `turn.step` hook slow streaming? | time a long reply with and without it |
| Can the tiles be keyed Boxes holding plain Buttons, beside a Raster for the dials, at 5 redraws a second? | a prototype layout |

## 14. Build order

1. The probes in section 13 that the specs depend on: `$.config.set` and the command route.
2. SPEC-016 and the SPEC-012 and SPEC-013 versions drafted, then a drafts review and Bryan's approval.
3. The evaluator side: `chain_state.py`, active time, PACE, the usage events and the odometer ledger, with tests.
4. The adapter side: the pane, the three layouts and looks, the instruments, the agents window, the guardrails
   panel, keys and the tile menu, with kit tests per look and layout.
5. Live checks in worker1 (docked and inline), then the SVG renderer for the desktop app, then `progress.html`.

## 15. Open questions for the owner

1. **Clickable tiles.** Keys always work. Should the tiles also be clickable boxes (where the terminal reports
   clicks), or keep the key strip only?
2. **Fuel wording in v21.** SPEC-013 v21's row says "Context 72%" and its settings count context used. Should they
   switch to fuel ("Fuel 28% · precompact runs at 20%"), a small change to v21 before it is built?
3. **The command's name.** `/devforgeai:drive` (needs the command-file route, unverified), `/devforgeai-drive`, or
   only v21's `/progress`?
4. **The mascot, emblems and scenes.** The earlier proposal had an animated character (Ember, or Clawd as a skin),
   phase emblems and backdrops (`devforgeai-progress-ui.md` G4 and §8). The dashboard has none. Keep them for a later
   version, or drop them?
5. **Skill health.** The earlier proposal's grid of each skill's steps across recent runs, for dogfooding
   (`devforgeai-progress-ui.md` §6.5). Keep it as a second view, or drop it?
6. **Phases beyond Spec.** The route ends at Spec. The earlier proposal asked whether to show QA and Ship as
   "coming". Add them?
7. **A PRD requirement.** PRD-001 FR-021 covers showing a run's progress; the instruments, the route and starting
   skills go beyond it. Add a requirement to PRD-001 (a draft), or treat the dashboard as part of FR-021?
8. **Opening by itself.** Should the dashboard open at session start when the terminal is wide enough, or only on
   its command?
9. **Wheel-spin's rule.** Proposed: RPM at least 120 while no step event or claim arrives for 3 minutes of active
   time. Accept, or set other numbers?
10. **What the odometer counts.** Input plus output tokens, or output only, or everything billed including cache
    reads?
11. **The prototype's home.** It lives in gitignored `tmp/`. Keep it local, or commit it (for example under
    `src/tools/`) so others can try it?
