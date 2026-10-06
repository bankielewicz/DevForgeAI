# DevForgeAI Drive: the dashboard

**Status:** design proposal, not approved. Nothing here is built into the plugin. It supersedes the views, layouts,
graphics and buttons of `devforgeai-progress-ui.md` (its sections 2, 6, 8 and 9). That document's manifests, step
states and gates (its sections 4 and 5) are built, as SPEC-012 and SPEC-013. This document changes no spec, skill or
plugin version: the changes it asks for are listed in section 13.

**Stacked on unbuilt work.** It builds on SPEC-013 v21, approved but not built: the other-mods filter (BEH-33),
`/progress` (BEH-34), the precompact row and run (BEH-35, BEH-36, DM-07, DM-08). v21 is on the branch
`docs/progress-v21` (PR #96), stacked on the save-the-work cycle (PR #95, SPEC-013 v20). Where this document says
"v21", read "once v21 is built"; its numbers move if another SPEC-013 version lands first.

**Date:** 2026-10-06. **Author:** claude-code (session 7637882f-b2ec-465e-988a-9602340d1023), at Bryan's request.

**Sources:**
- Bryan's decisions, quoted in section 1, as recorded in the plan `tmp/plans/2026-10-06-dashboard.md` (local only:
  `tmp/` is gitignored);
- the design canvas "DevForgeAI Drive" (claude.ai artifact `RwsfT8oYuzcebLfvhPtuW1`, private to Bryan): three looks,
  each at 160×48, at 120×36, with the tile menu open and docked at 64×48, plus the colour tokens;
- the working prototype, a throwaway mod in `tmp/probes/drive-probe/` (local only), run live in Bryan's terminal on
  2026-10-06. Its findings are in section 14 and in the memory note `claude-code-verified-facts.md`; a reviewer
  without them should rerun the prototype, which is to be committed (section 16);
- the mod API in Claude Code 2.1.291 (the `plugin-authoring` skill and its `claude-code.d.ts`); the API is early
  access and changes between releases;
- `devforgeai-claude-mods.md` (proposal) and its design rules (section 3).

**Terms.** A *Raster* is a mod's grid of character cells, each a glyph with a foreground and background colour.
*Blit* repaints a mounted Raster in place without redrawing the pane. A *keyed Box* is a layout box with an
address, so a hover style can apply to it. The *trip computer* is a line of text under the dials. *Wheel-spin* is
defined in section 5.

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
11. Renderers: terminal, desktop and the rest
11a. The character
12. When it can't draw everything
13. Where each piece of data comes from, and the specs this needs
14. Verified and unverified
15. Build order
16. Decisions on the open questions, and what is still open

## 1. Purpose and the decisions behind it

Bryan, 2026-10-05: "the dashboard is more appropriate, I feel as it will empower a normal user the ability to drive
claude code from one part of the framework through each phase/skill"; "my tesla's model y's tablet but designed for
claude code with devforgeai as its framework & mods as the guardrails".

The dashboard is one pane. It shows:
- where the project stands in the chain (Brainstorm, PRD, Architecture, Context, Epic, Story, Spec);
- what Claude is doing and how hard it is working;
- how much context is left;
- which guardrails are armed.

It also starts the next phase's skill when you ask it to. It extends PRD-001 FR-021 ("show the run's progress to
the user"); the instruments, the route and starting skills go beyond FR-021, so PRD-001 gets a new requirement (section 16).

Bryan's decisions, 2026-10-05 and 2026-10-06:

| Decision | His words |
| --- | --- |
| Drawn in the terminal, uniform tiles, modern | "Drawn in the terminal": "uniform sized button where each button is the same size/shape. make it look modern like it's from 2026 and not 1990" |
| A tile asks, the pick runs | the click returns a question asking what you'd like; "Run what I pick" |
| Real gauges | "dray [sic] actual gauges as this will be a nice add"; RPM and fuel; mileage = "the aggregate of tokens for the entire framework usage" |
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

Everything else in this document is proposed and marked so, or is an open question in section 16.

## 2. What it shows

| Area | Shows |
| --- | --- |
| Header | DevForgeAI Drive, the look's name and its key |
| Route | seven identical tiles, one per phase: glyph, name, the document it produced, its state, its key `[1]` to `[7]` |
| Navigation | "▼ YOU ARE HERE", the route travelled and still to go, the ETA chip |
| Instruments | the RPM, FUEL and PACE dials, the odometer and the trip computer (section 5) |
| Agents | the running subagents and their tool calls as a tree (section 7) |
| Guardrails | the armed guardrails and the last hold (section 8) |
| Log (Default, Night drive) or Telemetry (Race telemetry) | the run's recent events, or the session's numbers (wide layout only) |
| Status bar | the current skill and step, the mode chip (ENFORCE or OBSERVE), flags, and the fuel chip |
| Controls | Look, Switch to observe/enforce, Pause, Close, and the phase keys |

The status line, the progress band and the toasts of SPEC-013 stay as they are; the dashboard is the pane they
lead to. Every value in the mockups and the prototype is sample data, except the live readings named in section 14.

## 3. Layouts

The layout follows where the pane sits and its width (`e.props.placement`, `e.props.bodyColumns`), read at each
draw (proposed):

| Layout | Size | When | Arrangement |
| --- | --- | --- | --- |
| Docked | 64×48 | the pane is docked (the fullscreen layout, terminal at least 110 columns wide), at any dock width | the seven phases as stacked full-width strips joined by `▼`; you-are-here and ETA; the three dials side by side with the odometer; agents; one guardrails line; status bar |
| Compact | 120×36 | inline, 120 to 159 columns | the seven tiles in a row (15×7 each); navigation; dials and agents side by side; guardrails across the width; status bar |
| Wide | 160×48 | inline, 160 columns or more | the tiles in a row (19×9 each); navigation with start, ship and per-phase times; dials, odometer and agents; guardrails beside the log or telemetry; status bar |

A dock dragged wider than 64 columns keeps the docked layout, centred. (The prototype picked by width alone, so a
130-column dock drew Compact; the build follows this table.) Docked was seen on the **right**, full height, at the
width the mod asked for (section 14). The side is Claude Code's: a mod requests only a width (`$.ui.open`
`columns`), and a width the person drags wins. The canvas has every layout in every look.

## 4. Looks

Three looks share one layout and differ only in colour tokens and tile styles. The canvas's "Color tokens" board
lists every token for each look.

| Look | Character | Tiles |
| --- | --- | --- |
| **Default** | graphite, one electric-blue accent | thin rounded borders; the tile in progress tinted blue |
| **Night drive** | navy to violet, neon gradients | heavy borders, a gradient inside each tile, a glow around the current and next tiles, glowing needles |
| **Race telemetry** | black pit wall, amber and lime data | a coloured header strip per tile, numbered dial ticks, a telemetry panel in place of the log |

The canvas still names the first look "Model Y"; it is **Default** everywhere else (Bryan, 2026-10-06).

**Choosing.**
- A `/config` setting, `dashboardTheme`, sets the starting look; Default is its default. It is a display setting,
  which ADR-006 D6 leaves to the host's own mechanism, here the plugin's `userConfig`.
- `t` cycles the looks while the pane is open and writes the pick into that same `/config` setting with
  `$.config.set`, so there is one stored value (Bryan, 2026-10-06: "Write /config"). That the call works on a
  plugin's own `userConfig` row, and that the module sees the change without a reload, is unverified (section 14).
  If it doesn't work, `t` remembers the pick in `$.store` instead, which then wins over the `/config` default.

## 5. The instruments

**RPM: output tokens per second.**
- A pass-through `turn.step` hook times each model request of the main loop (no `agentId`): from the first streamed
  chunk (text, thinking or tool input) to the stop chunk. The reading is the stop chunk's `usage.output_tokens`
  divided by that time.
- While a request streams, the needle follows an estimate from the text so far (four characters a token). After
  the stop it falls to 0 over five seconds, like an engine returning to idle.
- The dial's range 0 to 200 and its redline from 150 are proposed; the one live reading so far was 81 tok/s
  (section 14).
- When the pane is closed, the hook only passes the stream on (one check per chunk, no timing).

**FUEL: context left.**
- FUEL is 100 minus `context.percent` from `session.measure`. With no measurement it reads 100: in a fresh session,
  after `/clear`, and after a compaction until the next measurement, when it reads from that.
- It turns amber from 30% and red from 20%. At 30% the fuel chip reads "▲ Fuel 28% · precompact runs at 20%". At
  20% `/devforgeai:precompact` runs (v21 BEH-36), and the chip reads "● Fuel 18% · running /devforgeai:precompact".
- These are the moments v21 fixes: `precompactAt` 70 and `precompactRunAt` 80 of the window used are 30% and 20% of
  fuel. The dashboard only counts the other way. v21's own row and settings switch to fuel wording before it is built (section 13).
- Fuel is the share of the whole window. On a 1M-token window, 20% fuel is 800k tokens used, which may come after
  an automatic compaction (v21 §13).

**PACE: progress along the route** (Bryan chose it: "Pace (Recommended)").
- PACE is how fast the open run advances: the steps it has reached, per hour of its active time. Active time is the
  run's span with every gap of more than 30 minutes between consecutive events removed. The 30 minutes is proposed:
  today it is only the adapter's stuck-notice timer (`IDLE_MS`), and no spec states it.
- The dial runs 0 to 100, where 100 is 12 steps an hour (5 minutes a step), as the prototype draws it; "min/step"
  is shown under the value. The scale is proposed and should be checked against recorded runs before the spec
  fixes it.
- A step counts when it is first reached (claimed, evidenced or evented). Several steps reached together count
  once each. A carried step (SPEC-012 v14) doesn't count: it was reached in the earlier run.
- PACE shows "—" until the run has 5 minutes of active time, and 0 with no run open.
- **Wheel-spin** is a new detector, not the tracker's stuck notice. (BEH-25 counts enforce-mode refusals and knows
  nothing of RPM.) The rule (Bryan, 2026-10-06: "Accept 120 / 3 min"): RPM at least 120 while the open run reaches
  no new step for 3 minutes of active time, to be checked against recorded runs before the spec fixes it. Then the PACE dial turns amber and reads "▲ WHEEL-SPIN". It works in both modes, refuses nothing and tells
  the model nothing.
- The reasoning for PACE over the alternatives (cache efficiency, dollars per hour, or no third dial): it can be
  computed from data the tracker has, says something the other instruments don't, reads at a glance, and is
  something you act on.

**The odometer: lifetime tokens.**
- The odometer totals the tokens DevForgeAI has used in this project ("the aggregate of tokens for the entire
  framework usage"). It is drawn as rolling digit drums, with the last digit in the accent colour.
- It counts every turn in the project, the main loop's and subagents', input and output with cache reads and
  writes, since all are billed (Bryan, 2026-10-06: "All tokens, incl. agents"). Subagents' tokens are added as
  counts only: SPEC-013 DM-01 still keeps their events out of runs.
- The counts live in a ledger the pruning keeps (section 13), since runs are pruned after `retentionDays` (SPEC-013
  DM-06).

**The trip computer.** A line of text under the dials, not a dial:
- the prompt-cache hit rate, from `turn.complete`'s `usage`: cache reads over all input tokens;
- dollars per hour, from `$.session.usage().cost`, left out where the host keeps no cost;
- time to first token, from the same `turn.step` timing;
- the session's tokens and cost.

## 6. The route and the ETA

**Tiles.** Each phase's tile draws one of these states:
- done ✓, with steps and time;
- in progress ●, with a progress bar and "step N of M";
- next, as a NEXT chip;
- not started ○, with an estimate;
- not built yet, dashed and "coming soon". Story and Spec are in this state today: the story skill is SPEC-009
  (draft), and only PRD-001 FR-017 covers the Spec step.

A phase's state comes from the project's documents (`chain_state.py`, section 13) and the open run. A phase with
several documents shows the latest by `updated` date; a document with no `status` counts as draft.

**ETA** (proposed):
- For each phase still ahead, the estimate is the median active time of the past runs of that phase's skill in
  this project. Past runs are those that ended with every step reached; stopped and unfinished runs, and runs that
  continued another, don't count. It needs at least 2 such runs.
- For the phase in progress, the estimate is its median less the open run's active time so far, never below 0.
- The ETA is the sum of the estimates for every phase ahead that has a built skill. If any of those phases has no
  estimate, the chip reads "ETA —". A total is never shown with a phase silently left out (Bryan's preference for
  deterministic logic). Phases whose skill isn't built (Story, Spec) are named instead: "ETA ~1 h 50 m to Epic ·
  Spec —".

## 7. The agents window

The tree lists the session's subagents and their tool calls:
- main;
- each agent with its state as a glyph and a colour: ◐ running (yellow), ✓ done (green), ✗ failed (red); and its
  elapsed time;
- under an agent, its recent tool calls.

**Sources:**
- `agent.spawn`: a new agent, its description and parent;
- `tool.call` with an `agentId`: its calls;
- `turn.complete` with an `agentId`: its end;
- `$.agent.list()`: agents that started before the mod loaded.

Reusable code: agent-radar's `adopt()` and `describe()`, and mission-control's tree helpers `lines()`, `took()` and
`icon()` (MIT, claude-code-mods).

**What stays unrecorded.** SPEC-013 DM-01 skips every event with an `agentId`, and that stays. The agents window
lives in the adapter's memory for drawing only, never in a run's events.

## 8. The guardrails panel

It lists only guardrails that exist, with what each does in each mode:

| Guardrail | Observe | Enforce |
| --- | --- | --- |
| Write gate (SPEC-013 BEH-08) | flags and logs | refuses the write |
| Question gate (BEH-21) | flags and logs | refuses the question |
| Exit confirmation (BEH-28) | asks before /clear, /exit, /resume | the same |
| Other-mods filter (v21 BEH-33) | records nothing from another mod | the same |
| Precompact at 20% fuel (v21 BEH-35, BEH-36) | warns, then runs it | the same |

The panel shows the mode (ENFORCE or OBSERVE), and in observe mode marks the two gates "flag only". The last hold
comes from `adapter.log` lines of kind `refused`. The proposed guards of `devforgeai-claude-mods.md` (A1 dev-guard,
B2 document-guard, B3 merge-gate) aren't drawn until they exist. The line "fails open: if the tracker stops, the
work goes on and you are told" restates ADR-006 D1.

## 9. Keys, the tile menu and what reaches the model

**Keys first.** Every control has a key, and keys work in every terminal. `1` to `7` and `m` follow Bryan's
decisions; `t`, `a` and `q` are proposed (from the prototype).

| Key | Does |
| --- | --- |
| `1` to `7` | opens that phase's menu |
| `t` | switches the look |
| `m` | switches observe and enforce |
| `a` | pauses or resumes the animation |
| `q` | closes the pane |

**Clickable tiles** (Bryan, 2026-10-06: "Clickable tiles"). Each tile is drawn as a keyed Box holding a plain
Button over the tile's text, not as part of the Raster, so a click on it opens its menu where the terminal reports
clicks. The dials, odometer and character stay in Rasters. A Box has one background colour, so Night drive's
gradient inside a tile becomes a solid tint with a gradient border; the layout prototype settles the look (section
14). Clicks reach a mod's Buttons only where the terminal reports them: in Bryan's cmux terminal no click reached
Claude Code, not even its own pane close button. So the keys stay the guaranteed path.

**The tile menu.** A key, or a click where clicks arrive, opens `$.ui.ask` with "<Phase>: what would you like to
do?":
- For a phase with a built skill: **Start <phase>** and **Cancel**.
- When a run of another skill is open and unfinished, the question also says so: "<skill> is at step k of m and
  unfinished; starting <phase> ends it." The Start option then reads **Start <phase> anyway**.
- For Story and Spec: no question, a toast "the skill isn't built yet".
- **Start** runs the skill with `$.command.run`, as if the person had typed it.
- If that skill's latest run ended unfinished, SPEC-013's offer to continue (BEH-31) should then ask "Continue from
  step N / Start fresh", as it does for a typed skill. BEH-31 counts only a load the person typed (origin `composer`
  or `bridge`), and a mod's `$.command.run` has origin `plugin`. So SPEC-013 needs one change: a start from the
  dashboard counts as typed. It was the person's pick (section 13).
- An "Open <document>" option is left out for now. No call opens a file in the editor, and a `file:` link needs a
  click, which cmux doesn't pass on (open question 1).

**This changes a recorded rule.** "Buttons fill the prompt box and never send it" is written in five places:
- `devforgeai-progress-ui.md` §9;
- `devforgeai-claude-mods.md` design rule 5, and its B1 entry (line 460);
- SPEC-013 §2 ("No button sends a prompt");
- SPEC-013 §12;
- SPEC-013's PRD-001 FR-003 link note ("no button sends a prompt").

The new rule: **a button that starts work asks first, and the person's answer is the go-ahead.** The mode button,
the progress band's controls and v21's precompact row still send nothing. No button decides a disposition, status,
priority or approval. The SPEC-013 places change with its next version; the two proposals get a pointer to this
section.

**The mode button.** "Switch to observe" / "Switch to enforce" is SPEC-013 BEH-13's switch: it runs IF-02, saves the
choice in the local preference file, changes the mode at once, and confirms with a toast. ADR-006 D3 says a mode the
project locks makes the button unavailable. That case isn't reachable yet: BEH-13 handles only IF-02's exit codes,
and the lock waits on the shared-schema change ADR-006 D3 names.

**What reaches the model.** Nothing new. The dashboard draws, and starts skills on your answer; it adds no context
and refuses nothing. The tracker's enforce-mode refusals stay the model's only signal.

## 10. Commands and settings

**The command.**
- A mod's own command names allow letters, digits, `_` and `-` (the 2.1.291 types), so `$.command.register` can't
  give `/devforgeai:<name>`. The prototype is `/devforgeai-probe`.
- Inside the `devforgeai` plugin, a command file (`commands/<name>.md`) would list as `/devforgeai:<name>`, and a
  `command.run` hook could answer it by opening the pane. That is unverified (section 14).
- The command is **`/devforgeai:drive`**, through that command file (Bryan, 2026-10-06), if the probe shows it opens
  the pane without loading a prompt; otherwise **`/devforgeai-drive`**, registered by the mod.
- v21's `/progress` stays, printing the run as text (section 12), and also opens the dashboard.

**Settings** (`userConfig`, shown in `/config`; the person's and not policy, like `tracking` and `retentionDays`):

| Setting | Values | Default |
| --- | --- | --- |
| `dashboardTheme` | Default, Night drive, Race telemetry | Default |
| `dashboardWidth` | the docked width asked for, in columns, from 64 to 160 | 66: the 64-column layout plus a column each side |
| `dashboardAutoOpen` | open by itself at session start | off (Bryan, 2026-10-06). When on, Claude Code seats an unasked pane only from 144 columns, or from 110 once the person has opened it before |
| `dashboardCharacter` | Ember, Clawd, none | Ember (section 11a) |
| the precompact settings | v21 DM-07, DM-08, reworded to fuel left (section 13) | warn at 30% fuel, run at 20% |

A stored value outside a `userConfig` field's range stops the whole module from loading (verified 2026-10-02), so
every number field has `min` and `max`.

## 11. Renderers: terminal, desktop and the rest
11a. The character

**One view model, several renderers.** A pure module (proposed `dashboard-core.ts`, no `$`) turns the readings and
states into a view model: the tiles, the dial values, the route, the ETA, the agents, the chips. Each renderer only
draws that model, so the looks, the layouts and the data stay the same across surfaces.

| Surface | What draws | Status |
| --- | --- | --- |
| Terminal (any) | one `Raster` per layout, repainted with `$.ui.blit` up to 5 times a second while the pane shows | built in the prototype; first (Bryan: "option 1") |
| Desktop app, Code tab, on a Windows-path project | `Svg`: the same model as vector shapes, `isInteractive` for hover and animated needles; at most 131,072 characters of source; presses go on Buttons around the drawing, since presses inside an `Svg` aren't reported | second (Bryan: "the design should include an svg version for the desktop app"); no prototype yet |
| Desktop app on a WSL project | nothing: plugins don't load there (section 14) | — |
| kitty, Ghostty and other terminals that show images | an `Image` tier (the SVG rasterised) was considered | dropped for now: it draws nothing in cmux, and braille dials look clean there |
| VS Code chat panel | nothing: hooks run, nothing draws. VS Code users are pointed to Claude Code in VS Code's terminal (the full dashboard), and to `progress.html` in VS Code's browser once it exists (Bryan, 2026-10-06: "Both") | — |
| Any browser | `progress.html`, a static page from the same model | later (SPEC-012 §11 plans it) |

Testing the desktop renderer needs a project on a Windows path opened in the desktop app; the kit can draw the
`desktop` surface for automated checks.

## 11a. The character

Bryan, 2026-10-06: build the character now, "with configuration for either ember or clawd" (the earlier proposal's
G4 and §8, which this section brings forward).

- **Choice.** `dashboardCharacter`: **Ember**, a small forge spark and the framework's own character, the default;
  **Clawd**, Claude Code's mascot; or none. A risk to record: a plugin that draws Anthropic's mascot could read as
  endorsed by Anthropic, and the mods announcement gives no guidance (`devforgeai-progress-ui.md` §8). Clawd ships
  only if that's acceptable when the plugin is published.
- **What it does.** The character acts out the current step's kind, from the step manifests (SPEC-012): reading a
  book (`read`), a thought bubble (`think`), a `?` sign (`ask`), hammering at an anvil (`forge`), a magnifier
  (`inspect`), a scroll (`report`); waving under `!` on your turn; confetti when a phase is done; a sweat drop when
  flagged; dozing when idle; spinning wheels during wheel-spin. Each loop is about a second.
- **Where.** A scene beside the instruments in the wide and compact layouts, and a small sprite in the docked
  layout's header. Exact sizes come from a layout prototype.
- **How it's drawn.** One SVG source per character, with named moving parts and small timelines as data
  (`devforgeai-progress-ui.md` §8). The terminal draws cell-fitted frames built ahead of time (a mod can't rasterise
  SVG while it runs), repainted with `$.ui.blit`; the desktop draws the SVG with its animation. `a` pauses it with
  the rest of the motion.

## 12. When it can't draw everything

| Situation | What it does (proposed) |
| --- | --- |
| Pane narrower than 64 columns, or shorter than the layout | one text line: "Widen the pane to at least 64 columns, or use /progress"; the status bar still draws if 1 row fits |
| No run open | tiles from the documents alone; PACE 0; ETA from history; RPM and FUEL as usual |
| Tracking off (`tracking`), stopped (SPEC-013 ERR-03), or the evaluator failing | RPM and FUEL as usual (they need no tracker); tiles, PACE, ETA and the guardrails panel replaced by "progress tracking is off: <reason>" |
| Headless session (`claude -p`) | nothing draws and no pane opens; the hooks stay cheap |
| No cost from the host | the trip computer leaves out dollars |
| Screen readers | a Raster isn't readable as text; `/progress` prints the run as text (v21 BEH-34), and the status line stays |
| Pane closed or paused | no timer and no blits; the `turn.step` hook only passes the stream on |

**Colour.** State is never shown by colour alone: tiles, agents and chips carry a glyph (✓ ● ○ ◐ ✗ ▲). Each look's
text and status colours should meet 4.5:1 contrast against its panel, which the spec checks per token. A Raster
paints about 1,024 colour pairs at once and rounds the rest. Night drive's gradients must stay within that, which
the prototype didn't measure (section 14). No light-terminal or 16-colour fallback is planned; that is part of open
question 11.

## 13. Where each piece of data comes from, and the specs this needs

**The split.** The evaluator, `evaluate.py`, reads one run's events and writes one output (SPEC-012 IF-01; PRD-001
NFR-007), and an evaluator that keeps state or reads a clock was rejected (SPEC-012 §12). So:
- **Per-run** figures go in `evaluate.py`'s `state.json`: they come from one run's events.
- **Cross-run** figures go in a new script, proposed `history.py`, which the adapter runs. It reads the run folders
  and writes the ledger, under its own NFR-007-style rule.
- **Live** readings stay in the adapter.

| Data | Source | Where |
| --- | --- | --- |
| Phase states, documents | `chain_state.py` (planned since SPEC-012 §11, not written): each document under `docs/specs/` by type, status, version and date | new script |
| Active time, per-step times, steps reached, PACE | one run's `events.jsonl` times | `evaluate.py`, in `state.json` |
| Per-run token totals | a new `usage` event kind (each main-loop turn's usage), recorded by the adapter | adapter records, `evaluate.py` totals |
| ETA medians | the ended runs' `state.json` files | `history.py` |
| Odometer | a ledger, `devforgeai/progress/odometer.jsonl`: one line per turn (session ID, turn ID, main or agent, token counts), appended by the adapter at each turn's end, read with duplicates by session and turn ignored, so a reload or several sessions count each turn once | adapter appends; `history.py` totals; `prune.py` keeps it |
| RPM, time to first token | `turn.step` timing | adapter, live only |
| FUEL | `session.measure` `context.percent` | adapter, live only |
| Cache hit rate, $/hour | `turn.complete` usage, `$.session.usage().cost` | adapter, live only |
| Agents | `agent.spawn`, `tool.call` and `turn.complete` with an `agentId`, `$.agent.list()` | adapter memory, never in events |
| Wheel-spin | RPM and the open run's last step time | adapter |
| Guardrails, last hold | the mode, `adapter.log` kind `refused` | adapter |

**The specs this needs:**

| Spec | What it gets |
| --- | --- |
| **SPEC-016** (new) | the dashboard: views, layouts, looks, the instruments' definitions, wheel-spin, clickable tiles and the tile menu with its own unfinished-run question, keys, settings, the character and its assets, the fallbacks of section 12, renderers, and VER items (kit tests per look and layout; live checks docked and inline) |
| **SPEC-012**, next free version | `usage` in DM-02's event kinds and `events.schema.json`; active time, per-step times, steps reached and PACE in DM-03's state; `chain_state.py` and `history.py` with their own read-only rules; the odometer ledger |
| **SPEC-013**, next free version | the pane and its command; recording `usage` events (DM-01); the RPM and FUEL readings; the agents window's memory; the settings; the dashboard's start counting as typed for BEH-31; `prune.py` keeping the ledger; the button rule's new wording in §2, §12 and the FR-003 link note |
| **PRD-001** (draft) | a new requirement for the dashboard (Bryan, 2026-10-06: "Add an FR"); NFR-007 kept as is, by putting cross-run work in `history.py` |
| **SPEC-013 v21** (approved, not built) | reworded to fuel before it is built (Bryan, 2026-10-06: "Switch to fuel"): the row reads "▲ Fuel 28% · precompact runs at 20%", and DM-07/DM-08 count fuel left (warn 30, run 20). The same moments; a Change Log revision and re-approval |

The save-the-work cycle plans its next change as SPEC-013 v22, on top of v21; this design takes the next free
number when its specs are drafted.

## 14. Verified and unverified

**Verified on 2026-10-06** with Claude Code 2.1.291, in Bryan's terminal (cmux, the worker1 tab), with the
prototype unless noted:

| Fact | How |
| --- | --- |
| A mod pane docks on the right, full height, at the requested width, in the fullscreen layout | `CLAUDE_CODE_NO_FLICKER=1`; the pane said "placed dock · 112 columns · fullscreen true" |
| On the main screen, the pane opens inline above the prompt | "placed inline · 193 columns · fullscreen false" |
| Braille dials, block drums and 24-bit colour render and animate in all three looks | read back from the screen, and colours judged by Bryan's eye; the repaint was set to 5 a second, not measured |
| `Image` draws nothing in cmux | `$.ui.blit` refused: "the terminal draws no placeholder images (probe: graphics reply OK, terminal libghostty)" |
| `$.command.run` starts a plugin skill from a Button's key | key `0` ran `/devforgeai:spec-lookup SPEC-013`; the tracker opened a run |
| The same call works from `session.measure`, v21 BEH-36's path | after a turn's end, `/devforgeai:spec-lookup SPEC-014` ran by itself |
| `turn.step` timing gives tokens per second | one reading: "218 tok in 2.7 s = 81 tok/s (2.3 s to first token)" |
| `$.ui.ask` from a key draws the engine's question dialog | key `4`: "Context: what would you like to do?"; Esc cancelled |
| Mouse clicks don't reach Claude Code in cmux | neither a mod Button (a `ui.press` logger saw nothing) nor the pane's own ✕ responded; keys did |
| The desktop app's WSL chat loads no mods | context-bar showed in the terminal "but not in the chat session of claude code desktop app" (Bryan) |
| A mod's command name allows no colon | `CommandSpec.name`: letters, digits, `_`, `-` |

**Unverified**, each with its check:

| Question | Check |
| --- | --- |
| Does `$.config.set` change the plugin's own `userConfig` row, and does the module see it without a reload? | a probe that writes `dashboardTheme` and reads `/config` |
| Does `commands/<name>.md` in the plugin plus a `command.run` hook give `/devforgeai:<name>` that opens the pane without loading a prompt? | a probe in a scratch copy of the plugin |
| Do clicks reach Buttons in Windows Terminal? | the prototype in a Windows Terminal WSL tab |
| Does an `Svg` dashboard draw in the desktop app's Code tab on a Windows-path project, and how does it animate? | a desktop probe |
| Does the pass-through `turn.step` hook slow streaming? | time a long reply with and without it |
| Can tiles be keyed Boxes holding plain Buttons, beside Rasters for the dials and the character, at 5 redraws a second, and how do the looks survive solid tile fills? | a layout prototype (next) |
| Does the command file route give `/devforgeai:drive`? | as above |
| Does a `$.ui.ask` opened while Claude is mid-turn, and a `$.command.run` queued then, behave (it runs "once the session is idle")? | press a tile key during a turn |
| Do Night drive's gradients stay within a Raster's colour pairs? | count the distinct pairs per frame in a kit test |
| Is PACE's scale right on real runs? | compute it over the recorded runs in `devforgeai/progress/runs/` |

## 15. Build order

1. The probes the specs depend on: `$.config.set`, the command route, a tile key mid-turn, colour pairs; and the
   layout prototype for clickable tiles and the character.
2. SPEC-016 and the SPEC-012 and SPEC-013 versions drafted, then a drafts review and Bryan's approval.
3. The scripts: `chain_state.py`, `history.py`, and the per-run figures in `evaluate.py`, with tests.
4. The adapter: the pane, the three layouts and looks, the instruments, the agents window, the guardrails panel,
   keys and the tile menu, with kit tests per look and layout.
5. The character's assets and its terminal frames.
6. Live checks in worker1, docked and inline. Then the desktop `Svg` renderer, then `progress.html`.

## 16. Decisions on the open questions, and what is still open

Bryan answered the review round's questions on 2026-10-06:

| Question | Answer |
| --- | --- |
| Clickable tiles | "Clickable tiles": keyed Boxes with Buttons (section 9) |
| Fuel wording in v21 | "Switch to fuel": v21 reworded before it is built (section 13) |
| Where `t` stores the look | "Write /config", with `$.store` as the fallback (section 4) |
| The command's name | "/devforgeai:drive", with `/devforgeai-drive` as the fallback (section 10) |
| VS Code | "Both": the integrated terminal, and `progress.html` once built (section 11) |
| A PRD requirement | "Add an FR" (section 13) |
| Opening by itself | "Setting, off by default" (section 10) |
| Wheel-spin's numbers | "Accept 120 / 3 min" (section 5) |
| What the odometer counts | "All tokens, incl. agents" (section 5) |
| The character | build it now, "with configuration for either ember or clawd" (section 11a) |
| Skill health | "Keep skill health (later)": recorded, not in this version |
| The prototype's home | "Commit the prototype": into the repository, for example `src/tools/drive-probe/` |
| Phases beyond Spec | "Stop at Spec" |

Still open:
1. **Opening a document from a tile.** Left out for now. Revisit when clicks or an editor call allow it.
