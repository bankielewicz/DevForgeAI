---
id: SPEC-013
type: spec
title: "Progress tracker adapter for Claude Code: events, gates, modes and the status line"
status: approved    # draft | in-review | approved | superseded | deprecated
version: 2
created: 2026-10-02
updated: 2026-10-02
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a4f2ade8-0127-4b96-bc22-b3498b2ab3a9"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-10-02
upstream:
  - {id: ADR-006, relation: constrains, version: 1, hash: null, note: "D1 (a hook blocks only at a gate, only in enforce mode; the tracker fails open), D3 (progress.mode, resolved at session start, and the button that switches it) and D6 (the local preference file); its follow-up gives D1, D3 and D6 to this spec"}
  - {id: ADR-003, relation: constrains, version: 2, hash: null, note: "A3's local preference format, in which progress.mode is one entry; an entry that can't be used is ignored and reported, never fatal"}
  - {id: SPEC-012, relation: constrains, version: 1, hash: null, note: "the event log (DM-02) this adapter writes, the state (DM-03) it reads, IF-01's command line, the gate and refuse (BEH-11), run-end (BEH-12), the operational files and the run ID (§4)"}
  - {id: PRD-001, item: FR-021, relation: informed_by, version: 11, hash: null, note: "progress tracking by evidence; this spec brings the core of SPEC-012 into Claude Code sessions"}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 11, hash: null, note: "decisions are the user's: enforce mode refuses a write that records a user-owned decision without the user's answer, and no button sends a prompt"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/hooks", "src/claude/DevForgeAI/types", "src/claude/DevForgeAI/progress/settings.py", "src/claude/DevForgeAI/.claude-plugin/plugin.json", "src/tests/progress"]
---

# SPEC-013 — Progress tracker adapter for Claude Code: events, gates, modes and the status line

## 1. Overview

SPEC-012 built the progress tracker's core: the formats, the brainstorm and architecture manifests, and
`evaluate.py`, which turns a skill run's event log into a progress state (merged in PR #59, plugin 0.12.0).
Nothing runs it in a session yet. This spec builds the Claude Code adapter, step 3 of the design proposal's
build order (`docs/specs/devforgeai-progress-ui.md` §11): a hooks module (a mod) in the `devforgeai` plugin that
- records each run of a tracked skill as an event log (SPEC-012 DM-02), from Claude Code's hooks;
- runs the evaluator and keeps the run's state;
- shows the run's progress in the status line, a two-row text band above the prompt, and toasts;
- in enforce mode, refuses the write gate's tool call when that gate raised flags, and gives the model the
  report gate's flags with the user's next prompt;
- fails open: when it can't run, the work goes on and the user is told.

It also adds `progress/settings.py`, which resolves `progress.mode` and saves the user's choice.

**The approach.** The event log is the truth. The adapter writes down what happened, as it happens, and
interprets nothing: it parses no tick and applies no rule. The evaluator, a pure function, computes the state
from the whole log each time (SPEC-012 BEH-01). So the adapter carries no copy of any rule (the mods proposal's
rule 2), a state that is lost or stale can be computed again from the log, and another tool's adapter shares
the same evaluator.

**Out of scope,** each for a later spec:
- the Journey and Workflow pane, and its graphics (`Svg`, `Image`, `Raster`), characters and animation settings;
- `progress.html`, `chain_state.py` and the project's phases, and Skill health;
- manifests for the other skills;
- locking `progress.mode` at project level, which arrives with the shared-schema change (ADR-006 D3);
- guards that refuse commands or paths (ADR-006, "Out of scope");
- offering the chain's next skill as a Tab suggestion;
- the Codex port's adapter, and moving manifests into the skills (the mods proposal's Part B).

## 2. Constraints

- **ADR-006** (accepted 2026-10-02), whose follow-up gives this spec D1, D3 and D6:
  - D1: a hook blocks only at one of the tracker's gates, only in enforce mode, by refusing the gate's tool
    call with a reason the model reads. The tracker fails open: when the evaluator can't run, the call proceeds,
    the user sees a notice, and the adapter logs it. A rule that can't be checked is not a flag.
  - D3: `progress.mode` is `observe` or `enforce`, `observe` by default; the adapter resolves it at session
    start and records the value and its source in the run's event log; until the shared-schema change, it applies
    the framework default and honours an entry in the local preference file; the band's button writes that entry.
  - D6: the user's entry lives in `.claude/devforgeai.local.md` (ADR-003 A3's format); display settings stay in
    Claude Code's own plugin settings.
- **SPEC-012's contracts** (approved, v1): the adapter writes DM-02 events and nothing the format doesn't allow,
  reads the DM-03 state, runs IF-01, follows the run ID format and the operational files of §4, and writes the
  rule that keeps `devforgeai/progress/` out of git (SPEC-012 §4 gives that to this spec).
- **Decisions are the user's** (PRD-001 FR-003; the mods proposal's rule 5). The adapter writes no document and
  changes no skill text. No button sends a prompt. The mode changes only when the user presses its button.
- **Evals stay the proof** (the mods proposal's rule 1). A headless session, which includes every child run of
  `claude plugin eval`, is left untouched (BEH-01).
- **The mod API is early access.** Every API claim here was read in Claude Code 2.1.287's declarations and the
  `plugin-authoring` skill's `reference.md`, among them: `$.plugin.root` (the plugin's folder, absolute),
  `$.session.root()` and `$.session.version()`; `$.process.run(argv, { timeoutMs })` (30 seconds by default; it
  rejects when the command is still running then); `$.fs` (read, write, list, exists, stat; no append); a `.catch`
  handler receives a replay-safe `next`; `tool.call`, `session.append` and `turn.complete` carry `agentId` only for
  a subagent; `session.append`'s door `response`, one row per kept block of Claude's; `session.end`'s reasons,
  `clear` with no `session.start` after it; `session.start`'s `isInteractive` and `surface`; `prompt.compose`'s
  trait `print`; `next.origin` and `next.budget`; `$.ui.log`, a dim line in the transcript; and
  `crypto.getRandomValues`. The probe (VER-01, run on 2026-10-02) checked what the declarations
  couldn't settle; §9 records its answers, and this version applies them. The build rechecks the declarations
  on the build it runs on.
- **Installed plugins' mods load only while Anthropic serves them.** Claude Code loads an installed plugin's
  hooks module only while the rollout flag `tengu_plugin_hooks_modules` is on; built-in mods load regardless. A
  process reads the flag from the cache the previous session left in `~/.claude.json`, so a newly served value
  takes effect in the next process (the probe's first session, §9). With the flag off, the module doesn't load,
  the skills work as before, and `claude plugin test` refuses to run its tests.
- **Bryan's decisions** (2026-10-02):
  - the adapter lives in the plugin, `src/claude/DevForgeAI/hooks/` (ADR-006's "one mod", and source in each
    plugin), not in `src/tools/mods/`;
  - enforce mode is specified and tested here, as ADR-006's follow-up says, though it is off by default;
  - no idle limit ends a run (BEH-05);
  - nothing is recorded in headless sessions (BEH-01).
- **Repository conventions.** Source lives in the plugin. `claude plugin test [dir]` runs "every `*.test.ts` and
  `*.test.tsx` under dir", so the module's tests sit beside it in `hooks/`, and the deploy command excludes them
  (§10); Python tests live in `src/tests/progress/`, which doesn't deploy.
- **The standard library only** for `settings.py`, which must run under `python3 -S`, like `evaluate.py`.
- **The mods docs' rules and limits** (the saved copy in `docs/research/Claude/mods/`, local, checked on
  2026-10-02):
  - `$` may be passed only to a function declared at the top level of the same file; passing it to a method, an
    inner function or an imported function fails `claude plugin validate`, and so does `const ui = $.ui`. Every use
    of `$` therefore stays in `hooks/progress.tsx`, and any other file of the adapter holds pure functions of data.
  - A hook's own time is limited to 10 seconds (time inside `next` or a mods API call doesn't count), a `.catch`
    handler's to 1 second, and all `session.end` hooks together to 1.5 seconds; `$.fs.read` and `$.fs.write` hold
    4 MiB a file, and `$.fs.write` isn't atomic.
  - Mods draw only on the `terminal` and `desktop` surfaces. The VS Code extension's chat panel runs hooks and draws
    nothing, a `-p` run draws nothing, and a desktop session in WSL loads no plugins. Bryan chose tracking only for
    VS Code for now (2026-10-02): the adapter records and enforces there and writes its notices to the transcript
    (BEH-01); `progress.html`, a page to open beside it, is a later spec.
  - In auto mode, a tool call whose input a hook changed is denied, so the adapter passes every event on unchanged.

## 3. Architecture and components

```mermaid
flowchart LR
    H["Claude Code hooks<br/>skill.prompt, tool.call, prompt.submit,<br/>turn.*, session.*"] --> A["hooks/progress.tsx<br/>(the adapter)"]
    A -->|writes| EV["devforgeai/progress/runs/&lt;run&gt;/events.jsonl<br/>SPEC-012 DM-02"]
    EV --> E["progress/evaluate.py<br/>SPEC-012 IF-01"]
    E -->|writes| ST["runs/&lt;run&gt;/state.json<br/>SPEC-012 DM-03"]
    ST --> A
    A -->|draws| UI["status line, band, toasts"]
    A -->|enforce: deny or context| M["the model"]
    A <-->|IF-01, IF-02| S["progress/settings.py"]
    S <--> L[".claude/devforgeai.local.md"]
```

| Path | Holds | Deploys |
| --- | --- | --- |
| `src/claude/DevForgeAI/hooks/hooks.json` | `{ "modules": ["./progress.tsx"] }` | yes |
| `src/claude/DevForgeAI/hooks/progress.tsx` | the adapter | yes |
| `src/claude/DevForgeAI/hooks/*.test.ts` | its tests, run by `claude plugin test src/claude/DevForgeAI` | no: the deploy command excludes them (§10) |
| `src/claude/DevForgeAI/types/index.d.ts` | the `$.state` contract (DM-03), named by `plugin.json`'s `types` | yes |
| `src/claude/DevForgeAI/progress/settings.py` | IF-01 and IF-02 | yes |
| `src/claude/DevForgeAI/.claude-plugin/plugin.json` | gains `types` and the `tracking` setting (DM-05) | yes |
| `src/tests/progress/test_settings.py`, `test_adapter_structure.py` | settings.py's tests (VER-02, VER-03) and the structure checks, which read VER-04's expected lines from `hooks/progress.test.ts` (VER-16) | no |

`evaluate.py`, its schemas and its manifests don't change. Every use of `$` stays in top-level functions of
`hooks/progress.tsx` (§2); a helper file next to it may hold pure functions (formatting the status text, the band's
rows, an Edit's resulting file), which its tests can call directly.

| Hook | What the adapter does |
| --- | --- |
| `session.start` | tells a headless session apart by `isInteractive` (BEH-01), resolves the mode (BEH-16), starts the evaluation timer (BEH-06), and keeps an open run across a reload (BEH-17) |
| `classic.SessionStart` with `source` `clear`, `resume` or `fork` | resolves the mode and restarts the timer after `/clear`, `/resume` or `/branch`, which fire no `session.start` (BEH-06, BEH-16) |
| `prompt.compose` | a second headless signal, the trait `print` (BEH-01) |
| `skill.prompt` | starts and ends runs (BEH-02, BEH-03, BEH-05) |
| `tool.call` | records tool calls and answers (BEH-04); in enforce mode, checks the write gate before the call (BEH-08) |
| `prompt.submit` | records the user's prompts; in enforce mode, gives the model the report gate's flags (BEH-09) |
| `session.append` with door `response` | records Claude's text as it is kept, ticks included (BEH-04) |
| `turn.start`, `turn.complete` | records turns (BEH-04) |
| `session.end` | ends the run (BEH-05) |
| `ui.render` on `AbovePrompt` | draws the band (BEH-11) |

## 4. Data model

**DM-01. The events the adapter writes.** Every event carries SPEC-012 DM-02's `run`, `seq` (1, 2, 3 … within
the run, with no gaps), `time` (UTC, ISO 8601) and `kind`. Only the main loop is recorded: a `tool.call`,
`session.append` or `turn.complete` whose input carries an `agentId` is a subagent's, and is skipped (no
DevForgeAI skill uses subagents today).

| Claude Code | When | Event |
| --- | --- | --- |
| `skill.prompt` for a tracked skill (BEH-02) | as it loads | `skill-loaded`: `format` `devforgeai-events/1`; `skill`, the name without a `<plugin>:` prefix; `checklist`, the text that `next(e)` resolves to, which is what the model reads; `host`, `claude-code <version>` from `$.session.version()`; and two fields DM-02 allows but the evaluator doesn't read: `mode` and `modeSource` (ADR-006 D3) |
| `tool.call`, any tool but AskUserQuestion | after `next(e)` resolves | `tool`: `tool`; `path` (below); `command` for Bash; `exit`; `error`; `content` for Write and Edit (below) |
| `tool.call` of AskUserQuestion that Claude Code fired (`next.origin.plugin` is `engine`; a mod's `$.ui.ask` arrives the same way and isn't recorded) | after `next(e)` resolves | `answer`: `answered` true when the call didn't fail and the result's `answers` holds at least one entry, an option picked or an answer typed; false when it failed, as a dismissal does (§9, P5) |
| `prompt.submit` that the person sent (`e.origin.kind` `composer` or `bridge`; a task notification, a scheduled prompt, a peer's message, an SDK turn or a plugin's prompt isn't recorded) | as it is submitted | `prompt` |
| `turn.start` | | `turn` with `phase` `start` |
| `session.append` with door `response` | as each row is kept | `reply` with `text`, the row's text blocks joined by newlines, when it has any; a row that holds only a tool call gives none. Each row arrives as it is kept, so ticks written between tool calls are recorded; `turn.complete`'s `answer` holds only the turn's last text, and a whole skill run can be one turn (§9, P7) |
| `turn.complete` | | `turn` with `phase` `end` |
| `session.end` | | `run-end`, `reason` `clear` when the session ends by `/clear`, otherwise `session-end` |
| a tracked skill loading while a run is open | before the new run's `skill-loaded` | `run-end` with `reason` `another-skill`, in the old run |

The fields of a `tool` event:
- **`path`**, relative to the project root with `/` separators: Read, Write and Edit's `file_path`; Glob's
  `pattern`, joined to its `path` when one is given; Grep's `path`, or `.` when none is given. A path outside the
  project root is kept absolute.
- **`exit`**: Bash's result has no exit-code field (§9, P6). A failed call's text reads `Exit code <n>`, so `exit`
  is that number when the call failed and the text has it, 0 when the call succeeded, and null otherwise.
- **`error`**: true when the result has `isError` or is a `{ deny }`: a call refused by the permission dialog, a
  settings hook, a mod after this one, or the adapter itself (BEH-08) never ran, so it is never evidence. A mod before
  this one that refuses a call keeps the adapter from seeing it at all.
- **`content`**: a Write's `content`, or for an Edit the whole file the Edit will leave: the current file with
  `old_string` replaced by `new_string` once, or everywhere with `replace_all`. Left out when it can't be computed
  (ERR-06) or is over 64 KiB, and left out of every event once events.jsonl passes 3 MiB (ERR-11).

**DM-02. The files the adapter writes,** all under the project root's `devforgeai/progress/` (SPEC-012 §4):

| File | Written | Holds |
| --- | --- | --- |
| `.gitignore` | once, when the adapter creates the folder | the line `*`, which keeps the folder and everything in it out of git; the project's own `.gitignore` is never edited |
| `runs/<run>/events.jsonl` | after each event | the run's events (DM-01), one JSON object per line, rewritten whole from the run's lines in `$.state` (`$.fs` has no append) |
| `runs/<run>/state.json` | by the evaluator | SPEC-012 DM-03, through IF-01's `--out` |
| `runs/<run>/pending.jsonl`, `pending.json` | during an enforce check (BEH-08) | the run's events plus the pending one, and the provisional state; overwritten at the next check, since `$.fs` can't delete |
| `current.json` | after each evaluation | a copy of the open run's `state.json`, for renderers; the last run's stays after it ends |
| `adapter.log` | on each notice | one line per entry: `<UTC time> <run or -> <kind>: <text>`, kind one of `mode`, `switch`, `ignored`, `refused`, `context`, `fail-open`, `error` |

**DM-03. The adapter's session state,** in `$.state`, declared in `types/index.d.ts` under the plugin's name.
`$.state` survives a reload of the module; module variables don't (BEH-17). `/clear`, `/resume` and `/branch` empty
it (§9, P11). Two values are module variables instead, since they belong to the process: whether the session is
interactive (BEH-01) and the evaluation timer (BEH-06). The status line isn't drawn from `$.state`: BEH-10 calls
`$.ui.status`.
`claude plugin validate` reads the contract strictly: it exports types and nothing else (no `export {}`), and the
state's keys are written inline under `interface PluginState`, since a type alias there hides them (found with
the probe).

```ts
interface ProgressState {
  run: { id: string; skill: string; seq: number; lines: string[]; dir: string } | null
  mode: 'observe' | 'enforce'
  modeSource: 'framework-default' | 'local'
  summary: { skill: string; current: number | null; steps: number; flags: number; yourTurn: boolean;
             ended: string | null; manifest: 'matched' | 'stale' | 'none' | 'unverified';
             states: string[]; currentTitle: string | null; lastFlag: string | null } | null
  lastEventAt: number          // ms since the epoch, for the idle display
  marked: boolean              // the run has events the evaluator hasn't seen
  shown: string[]              // flags already toasted, as "<step>:<type>:<seq>"
  contextSent: number[]        // report-gate seqs whose flags the model was given
  off: string | null           // why tracking is off for this session, or null
}
```

**DM-04. The local preference entry** (ADR-003 A3; ADR-006 D6). `.claude/devforgeai.local.md`, whose YAML
frontmatter is its entire content:

```
---
devforgeai_local: 1
progress.mode: enforce
---
```

**DM-05. The `tracking` setting,** a `userConfig` field in `plugin.json`: a string picker over `on` and `off`,
default `on`, shown in `/config`. It is a display-level switch for the person, not policy (ADR-006 D6): `off`
turns the whole adapter off for that user, in every project. The build checks the field's exact shape with
`claude plugin validate`.

## 5. Interfaces and contracts

`settings.py` is run as `python3 <plugin root>/progress/settings.py <command> …`:

| Item | Command | Behaviour |
| --- | --- | --- |
| IF-01 | `mode --root DIR` | Resolves `progress.mode` for the project at `DIR` (BEH-18): prints `observe framework-default`, `observe local` or `enforce local`. Each entry it can't use goes to stderr as `ignored .claude/devforgeai.local.md progress.mode (<reason>)`, the wording the skills use for ignored entries. Exit 0; exit 2 when `DIR` isn't a folder |
| IF-02 | `set-mode --root DIR --value observe\|enforce` | Saves the entry in `DIR/.claude/devforgeai.local.md` (BEH-18) and prints `saved progress.mode=<value> to .claude/devforgeai.local.md`. Exit 0 when saved; 1 when it refuses to change a file that isn't frontmatter-only; 2 when it can't write |
| IF-03 | the evaluator call | `<python> <plugin root>/progress/evaluate.py evaluate --manifests <plugin root>/progress/manifests [--manifests <root>/devforgeai/manifests/organization] [--manifests <root>/devforgeai/manifests] --events <events file> --out <state file> --root <root>`, SPEC-012 IF-01. A layer folder that doesn't exist is left out, since a `--manifests` that isn't a folder stops the evaluator (SPEC-012 ERR-04). `<python>` is the first of `python3` and `python` that runs (ERR-01) |

`<plugin root>` is `$.plugin.root`; `<root>` is `$.session.root()`. Both scripts are run through `$.process.run`
with an argv, never a shell string. `evaluate.py` isn't executable, so the interpreter is always named.

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "The adapter acts only in an interactive session with the tracking setting on (DM-05). When session.start's isInteractive is false (claude -p, the Agent SDK, and every child run of claude plugin eval), or a prompt.compose's traits include print (§9, P8), the adapter records, writes, draws and refuses nothing for the rest of the process. It keeps that answer in a module variable, since $.state empties on /clear, /resume and /branch. It writes no file before session.start has said the session is interactive. Where nothing draws (the VS Code extension's chat panel, where $.session.surfaces() is empty), it records and enforces as elsewhere, and every notice that would be a toast or the status line also goes to the transcript as a dim $.ui.log line (Bryan, 2026-10-02). With tracking off it does nothing at all."
  - id: BEH-02
    status: active
    rule: "A skill is tracked when it is one of the plugin's own skills (a folder under <plugin root>/skills/) or a <name>.json exists in <root>/devforgeai/manifests/ or <root>/devforgeai/manifests/organization/ (a project's own skill, ADR-006 D4). Its name is skill.prompt's skill without a '<plugin>:' prefix. Loading any other skill neither starts nor ends a run."
  - id: BEH-03
    status: active
    rule: "When skill.prompt fires for a tracked skill, the adapter calls next(e) first and never changes the text. It ends any open run with run-end another-skill, the same skill loading again included. It then opens a run: an ID of the UTC time from $.clock.now() as yyyymmddThhmmssZ, the skill's name and 8 hex digits from crypto.getRandomValues (SPEC-012 §4), and a skill-loaded event as the run's first (DM-01). The run's folder, devforgeai/progress/runs/<run>/, is created when its events are first written (BEH-15). Every skill of the plugin opens a run, git and documents-updater included: having no manifest, they are tracked by ticks only (SPEC-012 BEH-04's none), and the status line says so (BEH-10)."
  - id: BEH-04
    status: active
    rule: "While a run is open, the adapter turns each main-loop host event of DM-01 into its event, with the next seq, the UTC time from $.clock.now() and the run's ID, adds it to the run's lines in $.state and rewrites events.jsonl from them. Events while no run is open, and events that carry an agentId, are not recorded. An answer counts only when Claude Code fired the AskUserQuestion call (next.origin.plugin is 'engine'), and a prompt only when the person sent it (e.origin.kind composer or bridge), since a mod can ask through $.ui.ask, submit a prompt as the user's, and a background task's notification arrives as a prompt (§9, P11). Every event goes on unchanged: auto mode denies a tool call whose input a hook changed."
  - id: BEH-05
    status: active
    rule: "A run ends with run-end another-skill when a tracked skill loads; clear on session.end with reason clear; and session-end on session.end with any other reason (exit, /resume and /branch, which report resume, logout, the end of a -p run, a signal). Nothing else ends a run; there is no idle limit (Bryan, 2026-10-02). All session.end hooks share 1.5 seconds, so the run-end line is written first, and the final evaluation runs only when next.budget.remainingMs leaves room for it, with its timeoutMs taken from what is left: the log alone reproduces the state."
  - id: BEH-06
    status: active
    rule: "After a tool, answer, prompt, reply or run-end event, the run is marked. A timer runs IF-03 every half second when the run is marked and no timer-driven evaluation is running; it clears the mark as it starts. The timer starts at session.start, at classic.SessionStart with source clear, resume or fork (no session.start follows /clear, /resume or /branch), and at a skill.prompt when none is running. So at most one timer-driven evaluation runs at a time (an enforce check, BEH-08, runs apart from it on its own files), and a burst of events gives at most two evaluations. The timer's callback catches its own errors (ERR-10). After exit 0 the adapter copies state.json to current.json, updates the summary in $.state, which redraws the band, and calls $.ui.status when the status text has changed (BEH-10). In observe mode no tool call waits for an evaluation."
  - id: BEH-07
    status: active
    rule: "In observe mode the adapter never refuses a call and never adds text the model reads. Flags reach the user only: the status line, the band and toasts (BEH-10 to BEH-12)."
  - id: BEH-08
    status: active
    rule: "In enforce mode, for each main-loop Write or Edit while a run is open, the adapter checks before calling next(e). It writes the run's lines plus the pending tool event, with its content, to runs/<run>/pending.jsonl and runs IF-03 on it with --out runs/<run>/pending.json. When that state's gate has kind write, seq equal to the pending event's seq and refuse true, the adapter answers { deny } without calling next(e). The text says that DevForgeAI's progress tracker refused the write at the write gate, lists the messages of the flags raised at that seq, and says that the user decides these; where nothing draws, the same text also goes to $.ui.log. The call is recorded as a tool event with error true, which is never evidence (SPEC-012 BEH-06), so the write gate is checked again when the write is retried. Otherwise the adapter calls next(e) and records the event as in observe mode. $.fs can't delete a file, so the two pending files are overwritten at the next check."
  - id: BEH-09
    status: active
    rule: "In enforce mode, when an evaluation's gate has kind report and refuse true, the adapter adds the messages of the flags raised at that gate, once per gate seq, to the context of the user's next prompt.submit, so the model reads them with that prompt. It doesn't add them to a prompt that starts with '/', which usually loads the next skill, and drops them once the run has ended: the user has moved on. A run-end gate's flags reach the user only, since the conversation that would read them has ended. Neither gate has a tool call to refuse."
  - id: BEH-10
    status: active
    rule: "While a run is open, and after it ends until another run opens, the status line shows the summary: '<skill> <current>/<steps>' while a step is current; '<skill> done' when every step is reached; '<skill> ended' after run-end. Then, in this order and only when they apply: ' · your turn' when the current step shows your-turn; ' · <n> flag' or ' · <n> flags'; ' · ticks only' when the manifest is stale or none; ' · idle' when 30 minutes have passed with no event and no turn running; ' · enforce' in enforce mode. While tracking is off for the session (BEH-14, ERR-03), it shows 'progress: off (<reason>)' instead. The adapter sets it with $.ui.status(text), called only when the text changes, and Claude Code draws it as '⚠ devforgeai: <text>' (use-the-mods-API, $.ui.status)."
  - id: BEH-11
    status: active
    rule: "While a run is open, a ui.render hook on AbovePrompt draws two rows of text. Row 1: the skill, one glyph per step in order (done ●, current ◆, your-turn ?, pending ○, claimed ◐, unconfirmed ·, skipped-with-reason ⊘, not-applicable –, skipped ✗, rule-broken ✗) and 'step <current> of <steps>: <title>'. Row 2: 'observe mode' or 'enforce mode', a button 'Switch to enforce' or 'Switch to observe' (BEH-13), and the newest flag's message, or 'no flags'. The hook draws a Box holding its rows and then what await next(e) resolves to, so the mods after it still draw; it draws at most e.props.maxRows of its own rows (row 2 goes first) and cuts each to e.props.bodyColumns. It returns next(e), drawing nothing of its own, while e.props.hasSurvey is true, and when no run is open. Each draw waits for the one before it to finish, since after a reload the band can be asked for twice at once. The button has the key 'progress-mode' and no hotkey: a digit hotkey on a band button also fires when the user types that digit alone into an empty prompt."
  - id: BEH-12
    status: active
    rule: "Each flag shows one toast, '✗ Step <step> <type>: <message>', the first time an evaluation reports it. When the run's last step is reached without run-end, one toast says '✓ <skill>: all steps reached'. Toasts are the same in both modes; where nothing draws, each also goes to $.ui.log (BEH-01)."
  - id: BEH-13
    status: active
    rule: "Pressing the band's button runs IF-02 with the other mode. On exit 0 the mode changes for the session at once, its source becomes local, a toast confirms it, and adapter.log records the switch with the run's ID and last seq, because DM-02 has no event for it. On exit 1 or 2 the mode stays as it was and a toast gives IF-02's reason. The button never sends a prompt."
  - id: BEH-14
    status: active
    rule: "The adapter fails open (ADR-006 D1). A hook that fails before calling next is skipped and the event goes on, and one that fails after next leaves that result standing. Each hook is also registered with a .catch whose handler, within its 1-second limit, writes the error to adapter.log, shows a toast once per distinct error, and returns next(e): in a .catch, next is replay-safe, so when the hook had already called it (next.called), the result it got stands. When the evaluator can't run (ERR-01, ERR-02, ERR-07), the tool call proceeds, the status line shows 'progress: off (<reason>)' until an evaluation succeeds, and events are still recorded, so the state can be computed later. Claude Code reports an installed plugin's load failures and skipped hooks only in its debug log (claude --debug), so a missing band is the visible sign during dogfooding. The adapter registers no guard: a guard's fail-closed .catch (D1) belongs to the guard's own spec."
  - id: BEH-15
    status: active
    rule: "The adapter writes only under <root>/devforgeai/progress/ (DM-02), and .claude/devforgeai.local.md only through IF-02 when the user presses the button. It creates devforgeai/progress/ with its .gitignore holding '*' the first time it writes a run's events, which is only after BEH-01 has found the session interactive, and never edits the project's own .gitignore. $.fs.write isn't atomic and holds at most 4 MiB a file: the adapter is the only writer of its files, starts an evaluation only after the write it depends on has finished, keeps each Write or Edit's content to 64 KiB, and stops adding content once events.jsonl passes 3 MiB (ERR-11). It reads the plugin's files, the manifest folders, the local preference file through IF-01, and a file an Edit names (DM-01). It opens no network connection."
  - id: BEH-16
    status: active
    rule: "At session.start, at classic.SessionStart with source clear, resume or fork, and at a skill.prompt when $.state holds no mode, the adapter runs IF-01 with timeoutMs 3000, since Claude Code holds the first prompt until session.start's hooks finish, and keeps the mode and its source in $.state; it writes each entry IF-01 reports as ignored to adapter.log and shows them in one toast. Every skill-loaded event carries the mode and source in force when the run opened (ADR-006 D3). Until the shared-schema change brings progress.mode into policy, only the framework default and the local entry apply, and the button is always available."
  - id: BEH-17
    status: active
    rule: "A reload of the module (a hot reload, /reload-plugins, or a change to the tracking setting) keeps an open run: its ID, seq, lines, the mode and the summary are in $.state, and session.start fires again. The evaluation timer starts again there, and the adapter marks the run so the state is computed again. $.state belongs to the session: /clear, /resume and /branch empty it and change the session ID while the module and its timer go on (§9, P11), after the run has already ended with run-end clear or session-end (BEH-05)."
  - id: BEH-18
    status: active
    rule: "settings.py reads .claude/devforgeai.local.md only as frontmatter: the file must start with a line '---' and end with the next '---' line, with nothing after it but blank lines. IF-01 uses the progress.mode entry when the file is frontmatter-only, devforgeai_local is 1, and the value is observe or enforce, quoted or not; otherwise the mode is observe from the framework default, and each reason is reported (ERR-04). IF-02 creates .claude/ and the file when they are missing, with devforgeai_local: 1 and the entry; in an existing frontmatter-only file it replaces the progress.mode line, or adds it before the closing '---', and keeps every other line as it was. It writes a temporary file beside the target and renames it over the target. It reads no other entry: the skills apply the rest (ADR-003 A3)."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "Neither python3 nor python runs: at session.start, $.process.run of '<name> --version', with timeoutMs 3000, rejects for both (a missing program rejects with 'Executable not found', §9, P2) or exits non-zero."
    handling: "Keep recording events; skip every evaluation and every enforce check, so every call proceeds (BEH-14); write adapter.log once."
    user_result: "The status line shows 'progress: off (python not found)', and one toast says so."
  - id: ERR-02
    status: active
    condition: "IF-03 exits 2, or is still running when its timeout ends: 5 seconds, or at session.end what next.budget.remainingMs leaves; $.process.run rejects then."
    handling: "Leave the earlier state and current.json as they were; let the call proceed when this was an enforce check; write the evaluator's stderr line, or 'timed out', to adapter.log."
    user_result: "The status line shows 'progress: off (<reason>)' until an evaluation succeeds, and a toast shows each distinct reason once per session."
  - id: ERR-03
    status: active
    condition: "devforgeai/progress/ or a run's folder can't be created or written."
    handling: "Stop tracking for the session: drop the run and record nothing more."
    user_result: "The status line shows 'progress: off (cannot write devforgeai/progress)', and one toast says so."
  - id: ERR-04
    status: active
    condition: "The local preference file exists but isn't frontmatter-only, lacks devforgeai_local: 1, or gives progress.mode a value other than observe or enforce."
    handling: "Use observe from the framework default; IF-01 reports the reason (BEH-18); the adapter writes it to adapter.log. Never fatal (ADR-003 A3)."
    user_result: "One toast: 'ignored .claude/devforgeai.local.md progress.mode (<reason>)'."
  - id: ERR-05
    status: active
    condition: "IF-02 refuses (exit 1: the file isn't frontmatter-only) or can't write (exit 2) when the button is pressed."
    handling: "Keep the mode as it was; write IF-02's reason to adapter.log."
    user_result: "A toast gives the reason; the button still shows the same choice."
  - id: ERR-06
    status: active
    condition: "An Edit's resulting file can't be computed: the file can't be read, is over 64 KiB, or old_string doesn't occur, or occurs more than once without replace_all."
    handling: "Record the tool event without content. After the write, the evaluator reads the file under --root; an enforce check before the write can't see the field, so its content rules raise no flag and the call proceeds (SPEC-012 ERR-05)."
    user_result: "Nothing extra; the state may carry SPEC-012's note 'content not available; rule not checked'."
  - id: ERR-07
    status: active
    condition: "IF-03 exits 0 but its --out can't be read or isn't JSON."
    handling: "Treat it as ERR-02."
    user_result: "As ERR-02."
  - id: ERR-08
    status: active
    condition: "A tracked skill loads before any session.start has reached the module, so whether the session is interactive is unknown."
    handling: "Treat the session as not interactive until a session.start says otherwise: record and write nothing, as BEH-01 does, so an eval child run is never touched by mistake."
    user_result: "No status line or band until the session is known to be interactive."
  - id: ERR-09
    status: active
    condition: "Claude Code's hooks worker crashes, and Claude Code turns off the mods that run in it for the session ('mods that run in the hooks worker are off for this session')."
    handling: "Nothing the adapter can do: its hooks no longer run. The event log ends where the crash left it; /reload-plugins or the next session tracks again, and the run's state can still be computed from the log."
    user_result: "Claude Code's own notice; the status line and band stop updating."
  - id: ERR-10
    status: active
    condition: "The evaluation timer's callback throws."
    handling: "The callback catches every error itself, writes it to adapter.log and treats it as ERR-02; an error it let escape would reach only Claude Code's debug log, and the timer would run again with no notice."
    user_result: "As ERR-02."
  - id: ERR-11
    status: active
    condition: "events.jsonl passes 3 MiB, or a write would take it past $.fs.write's 4 MiB."
    handling: "From 3 MiB, new tool events carry no content: the evaluator reads written files under --root, and an enforce check before a write sees no content, so its content rules raise no flag (SPEC-012 ERR-05). At 4 MiB the adapter stops recording that run: it writes nothing more to its files, and the next tracked skill opens a new run as usual. The log so far still gives the run's state."
    user_result: "From 4 MiB until another run opens, the status line shows 'progress: off (event log full)', and one toast says so."
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "In observe mode a tool call waits for no process: recording an event is in-memory work plus one file write, and evaluation runs on the timer (BEH-06)."
    measured_by: "VER-06 checks that no tool.call hook awaits $.process.run in observe mode; VER-15 records the time a recorded Write takes on the owner's machine."
    upstream:
      - {id: PRD-001, item: NFR-006, relation: informed_by, version: 11, hash: null}
  - id: QR-02
    status: active
    response: "In enforce mode each Write or Edit during a run costs one evaluator run before the call: the target is under 500 ms on the owner's machine, and 5 seconds is the limit after which the check fails open (ERR-02)."
    measured_by: "VER-15 records the time of an enforce check on the owner's machine; VER-09 covers the limit."
    upstream:
      - {id: PRD-001, item: NFR-006, relation: informed_by, version: 11, hash: null}
  - id: QR-03
    status: active
    response: "The adapter writes only under devforgeai/progress/ and, on the user's press, .claude/devforgeai.local.md; it reads only the files BEH-15 lists, and opens no network connection."
    measured_by: "VER-11 checks the files written in a scripted session; VER-16 checks that claude plugin validate lists no network call; code review at build time, recorded in §9."
    upstream:
      - {id: PRD-001, item: NFR-007, relation: informed_by, version: 11, hash: null}
  - id: QR-04
    status: active
    response: "settings.py imports only the Python standard library and runs under python3 -S."
    measured_by: "VER-02 and VER-03 run every case normally and under python3 -S."
    upstream:
      - {id: PRD-001, item: NFR-004, relation: informed_by, version: 11, hash: null}
```

## 9. Verification

| Kind | Status |
| --- | --- |
| Structural: this spec against `src/schemas/spec.schema.json` | Passes, checked 2026-10-02 with the helpers of `src/tests/context/test_structure.py`: the frontmatter and every item block, with QR-01 to QR-04 linked to PRD-001 v11's NFRs; every BEH, ERR and QR item is covered by a VER item |
| Probe (VER-01) | Run on 2026-10-02 with Claude Code 2.1.287, by Bryan in his shell and in a cmux tab, in a throwaway workspace (`/tmp/devforgeai-probe-ws`) with the plugin's source and the probe as skills-dir plugins: P1 to P8 and P10 to P13 answered (below); P9 not run. P7 contradicted DM-01, so version 2 reads replies from `session.append` |
| Docs check | 2026-10-02: the mods docs, saved in `docs/research/Claude/mods/` (local, as `CLAUDE.md` says of `docs/research/Claude/`), were read against this version; the second version-2 Change Log row lists what changed. They confirm P1, P5 to P8 and P10 to P13 |
| Build | Built on branch `feat/spec-013-progress-adapter` (worktree), not merged, by session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9 through `/plugin-dev:create-plugin`. Files: `progress/settings.py`, `hooks/hooks.json`, `hooks/progress.tsx`, `hooks/progress-core.ts`, `hooks/core.test.ts`, `hooks/progress.test.ts`, `types/index.d.ts`, the `plugin.json` keys, `src/tests/progress/test_settings.py` and `test_adapter_structure.py`. Results at the build's head: `claude plugin test src/claude/DevForgeAI` 50 pass, 0 fail (13 core tests of the pure helpers, 37 kit tests: VER-04 to VER-14); `src/tests/progress` 99 passed, 173 subtests (the evaluator's 51, `settings.py`'s 44 under normal and `python3 -S`, the 4 structure checks of VER-16); `claude plugin validate`: passed, 11 hooks, the nine state keys, no `$.http`, `$.mcp` or `$.env.set` call (QR-03). VER-01 ran before the build. Not run: VER-15 (the CLI dogfood, Bryan's session, through `--plugin-dir` before merge) and the eval check that the plugin with a hooks module still loads in `claude plugin eval` (one case, Bryan's terminal). Plugin version: set at merge (main is 0.12.1) |

**The probe (VER-01).** A throwaway mod, outside the plugin, logs what the declarations can't settle. It needs
an interactive session, so the owner runs it. Each line is a pass criterion; when one fails, this spec is revised
before step 2 of §11.

| # | Question | Passes when |
| --- | --- | --- |
| P1 | Does a hooks module in a skills-dir plugin load? `.claude/skills/devforgeai/` loads as `devforgeai@skills-dir` | the probe's `session.start` runs from a copy deployed there |
| P2 | Do `$.fs` and `$.process.run` run under the session's sandbox? | the probe writes `devforgeai/progress/` in a scratch project and runs `python3 --version` |
| P3 | How does `skill.prompt` spell a plugin skill? Does it fire for a preload, or inside a subagent? | `e.skill` is `devforgeai:brainstorm` or `brainstorm` for `/devforgeai:brainstorm`; no `skill.prompt` fires for a devforgeai skill the user didn't load |
| P4 | Is the checklist in the text the model reads, as written? | IF-02 of SPEC-012 (`check`) reports `matched` for the logged text of brainstorm and architecture |
| P5 | How does AskUserQuestion's result show an answer and a dismissal? | the two logged results differ in a field the adapter can read |
| P6 | Does Bash's result carry the exit code? | the logged result of `exit 3` shows 3, or `isError` alone (then `exit` follows DM-01's fallback) |
| P7 | Does `turn.complete`'s `answer` hold the whole reply, ticks included? | a reply with a ticked checklist arrives whole |
| P8 | Does the first `prompt.compose` come before the first `skill.prompt` of a session started with `/devforgeai:brainstorm`, and does `claude -p` show the trait `print`? | the order is logged, and `print` appears only under `-p` |
| P9 | Does a mod in the plugin run in `claude plugin eval`'s child runs? | logged either way; BEH-01 keeps them untouched in both cases |
| P10 | Does the engine write `.claude-plugin/types/` into the deployed copy when it loads the module? | logged either way; §10 adjusts the deploy check |
| P11 | What happens to `$.state` and running timers after `/clear`, which fires `session.end` with no `session.start` after it? | logged either way; BEH-06 and BEH-16 restart the timer and resolve the mode at the next `skill.prompt` in both cases |
| P12 | Can a `claude plugin test` file read a file outside the plugin through `$.fs` (VER-04's expected lines)? | the test reads `src/tests/progress/adapter/events.jsonl`; if not, the build keeps the lines in the test and the Python test reads them from there |
| P13 | Does a `tool.call` hook's `{ deny }` reach the model as the call's error result (BEH-08's mechanism)? Added during the probe | the model reports the refusal's text |

**Build decisions and departures (2026-10-02), for Bryan to approve or reverse.** Each names where it shows; a SPEC-013
v3 could adopt the wording.

- **Departure, DM-03 and BEH-17: a run's event lines aren't in `$.state`.** One `$.state` value holds at most 4,194,304
  characters, which the docs don't say; the kit's ERR-11 test found it ("`$.state.set`: the value is 4195926
  characters, over the 4194304 limit"), since a run's escaped lines pass it before `events.jsonl` reaches `$.fs`'s
  4 MiB. `$.state` keeps the run's ID, skill, seq and folder; the lines are a module variable, read back from
  `events.jsonl` after a reload, and a failed read is never cached, so a fresh log can't overwrite the real one.
- **Reading, IF-02:** `set-mode` adds `devforgeai_local: 1` when the file has none, since IF-01 would otherwise ignore
  the saved entry; it refuses (exit 1) a file declaring another format version, as it refuses one that isn't
  frontmatter-only. IF-01 reports an ignored entry only when the file has a `progress.mode` line.
- **Reading, VER-11:** `state.json` is written by the evaluator's process, not by `$.fs.write`, so the test checks the
  module's own writes (`.gitignore`, `events.jsonl`, `current.json`, `adapter.log`) and the evaluator's `--out`.
- **Reading, DM-02:** `adapter.log` gets a `mode` line each time the mode is resolved, with its source (ADR-006 D3).
- **Reading, DM-01:** `exit` is recorded for every tool event, 0 for any call that succeeded, as the table lists it.
- **Build note, `session.append`:** the test kit answers nothing beneath it, so the adapter records the reply before
  calling `next(e)`, as BEH-04 allows, and the kit tests catch the call's rejection.
- **Build note, enforce:** the pending event's seq is the run's next seq, which is the provisional state's `gate.seq`
  when the Write is the write gate; the refused call is recorded with `error` true, never evidence and closing no
  answer window, so the retry after the user's answer goes through (VER-07).
- **Build note, BEH-14:** in a live session `next(e)` doesn't reject, so a failure after it is the adapter's own:
  `tool.call` and `skill.prompt` wrap that work and report it, keeping the result; the `.catch` handlers report only
  failures before `next`, which keeps the kit's `session.append` rejection quiet.
- **The kit's limits:** its mock clock runs at most 10,000 waits in one advance, so VER-05's idle test advances 31
  minutes, not 24 hours; it doesn't simulate `session.end`'s shared 1.5 seconds, so `finalTimeout` is unit-tested; it
  can't reload a module, so VER-13 fires `session.start` again with the module's variables kept; a failed
  `$.ui.status` is dropped, not thrown, so ERR-10's test fails an `fs.exists` inside the evaluation.
- **Test order:** `settings.py`'s tests and the Phase 4 kit tests (VER-04, 05, 10, 11, 13, 14) came before their code
  and failed first; the pure helpers' tests and the Phase 5 and 6 kit tests (VER-06, 07, 08, 09, 12) came after the
  module, which was written in one piece.

**The probe's answers** (2026-10-02, Claude Code 2.1.287). `docs/runbooks/spec-013-probe.md` records how the probe
ran and the raw shapes behind each answer; the probe's own logs weren't kept:

| # | Answer | What version 2 does with it |
| --- | --- | --- |
| P1 | Yes. The debug log reads "hooks module progress-probe@skills-dir loaded (worker, environment 1, tier user)" | Nothing: the module ships in the plugin's skills-dir copy |
| P2 | The probe's `$.fs.write` and a `$.process.run` of `sh -c touch` both wrote under `.claude/skills/devforgeai/`, a path Claude's Bash sandbox denies to Bash in this repository's sessions; the probe session's own Bash wasn't tried there, and the mods docs say a mod's processes run outside the sandbox. `python3 --version` ran in 3 ms; `python` isn't installed, and `$.process.run` rejected with "Executable not found in $PATH"; `evaluate.py check` through `$.process.run` took 38 ms | ERR-01 names the rejection |
| P3 | `e.skill` is `devforgeai:brainstorm`; `skill.prompt` fired once, for the user's load only. No preload or subagent load occurred | Nothing: BEH-02 strips the prefix |
| P4 | Yes. The text, both as given and as the model reads it (they were identical), begins with "Base directory for this skill: …" and has no frontmatter, and `check` reports `matched sha256:e3ba73ab…` for brainstorm. Architecture wasn't loaded | Nothing |
| P5 | Dismissed with Esc: `isError` true and an error text ("The user doesn't want to proceed with this tool use…"), no `answers`. Answered by picking an option or typing one: `isError` false and `answers` maps each question to its answer | DM-01's `answered` rule |
| P6 | No exit-code field: `exit 3` gives `isError` true, result "Error: Exit code 3" and text "Exit code 3" | DM-01's `exit` rule |
| P7 | No. The whole brainstorm (skill load, two AskUserQuestion rounds, the Write, validation) was one turn, and `turn.complete`'s `answer` held only its last text, with no ticks. In a second session, `session.append` with door `response` gave one row per text block as it was kept: `- [x] 1. probe tick` before a Bash call, the call's own row with no text, then `- [x] 2. second tick` | DM-01 takes `reply` events from `session.append` |
| P8 | Interactive: `prompt.submit`, `turn.start`, then the first `prompt.compose` (traits `lean`, `skills`), then `skill.prompt`. Under `claude -p` the module loaded too, and the first `prompt.compose` (traits `lean`, `print`, `skills`) came before `prompt.submit`. One earlier `claude -p` run without `--debug` logged nothing, unexplained | Nothing: BEH-01's check comes before any run opens |
| P9 | Not run (one paid eval case). Mods do load under `-p` (P8), so they may load in eval child runs; BEH-01 leaves those untouched either way | Nothing |
| P10 | No `.claude-plugin/types/` was written into either skills-dir copy | §10 drops the deploy-check exclusion it anticipated |
| P11 | After `/clear`: the same module load and its timer went on, no `session.start` fired, the session ID changed, and `$.state` was empty | BEH-17 says so; BEH-06 and BEH-16 already restart at the next `skill.prompt` |
| P12 | No. A test's `$` holds event calls only, and even an inline plugin's `$.fs.read` is an event nothing answers ("no implementation for fs.read"). A test answers `fs.read` with `{ value }` and captures `fs.write` itself, so tests run in memory | VER-04, VER-11 and VER-16: expected lines live in the test file |
| P13 | Yes. The model said the write "was refused by a hook" and quoted the refusal | Nothing |

Before the probe's sessions could load the module, Claude Code served the hooks-modules rollout flag off from an
earlier cache; the same session refreshed it to on, and every later process loaded the probe (§2).

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "The probe answers P1 to P13 as the table above says (P9 optional), and the answers are recorded in §9 with the Claude Code version. Any answer that contradicts DM-01, BEH-01, BEH-02 or BEH-03 revises this spec before the adapter is built."
    level: manual
    covers:
      - BEH-01
      - BEH-02
      - BEH-03
      - ERR-08
  - id: VER-02
    status: active
    obligation: "test_settings.py runs IF-01 on: no file (observe framework-default); progress.mode: enforce (enforce local); a quoted value; a bad value, a missing devforgeai_local, and a file with text after the frontmatter (each observe framework-default with its ignored line on stderr); and a root that isn't a folder (exit 2). Every case passes normally and under python3 -S."
    level: unit
    covers:
      - BEH-18
      - ERR-04
      - QR-04
  - id: VER-03
    status: active
    obligation: "test_settings.py runs IF-02: it creates .claude/ and the file when missing; replaces an existing progress.mode line and adds one when absent, leaving every other line and its order unchanged; refuses a file that isn't frontmatter-only with exit 1 and leaves it byte for byte; and leaves no temporary file behind. Every case passes normally and under python3 -S."
    level: unit
    covers:
      - BEH-18
      - ERR-05
      - QR-04
  - id: VER-04
    status: active
    obligation: "A claude plugin test script plays a session on a mock clock: /devforgeai:brainstorm loads, then a Read, a Bash run of validate_brn.py, an AskUserQuestion answered by an option, one answered by typing, one dismissed, and one that another inline plugin asks through $.ui.ask; a failed Bash whose text reads 'Exit code 3'; a Write that a stub beneath refuses with { deny }; one turn whose response rows tick a step before and after a tool call, with a row holding only a thinking block; a Write; a prompt from the composer and one from a task notification; and a subagent's Write and response. A test touches no disk (§9, P12): it answers the plugin's fs.read and fs.exists calls and captures each fs.write. The last events.jsonl written equals, byte for byte once the run ID's 8 random hex digits are normalised, the expected lines kept in the test file between marker comments: each DM-01 field (path forms, exit, error, content), error true and exit null for the refused Write, one reply per response row with text, no answer for the mod's question, no prompt for the notification, and no subagent event; test_adapter_structure.py reads those lines from hooks/progress.test.ts and validates each against events.schema.json."
    level: integration
    covers:
      - BEH-04
  - id: VER-05
    status: active
    obligation: "Scripted sessions show: a second tracked skill ends the first run with run-end another-skill and opens a new one; the same skill loading again does the same; an untracked skill and a skill with only a project manifest are told apart (BEH-02); session.end with reason clear writes run-end clear and any other reason (resume included) run-end session-end; after /clear, /resume or /branch, classic.SessionStart with source clear, resume or fork resolves the mode and starts the timer, and without it the next tracked skill does (BEH-06, BEH-16); with the clock advanced 24 hours and no events, no run-end is written and the status text ends in ' · idle'; run IDs match SPEC-012's pattern; at session.end with little of next.budget.remainingMs left, run-end is written and the final evaluation is skipped."
    level: integration
    covers:
      - BEH-02
      - BEH-03
      - BEH-05
      - BEH-16
  - id: VER-06
    status: active
    obligation: "With $.process.run mocked, the evaluator runs with IF-03's argv, including each layer folder only when it exists; a burst of five events gives at most two runs; after exit 0, current.json equals state.json and the status line and band redraw; in observe mode no tool.call hook awaits $.process.run."
    level: integration
    covers:
      - BEH-06
      - QR-01
  - id: VER-07
    status: active
    obligation: "In enforce mode with a mocked provisional state whose gate is write at the pending seq with refuse true, the Write is refused with a text naming the flags, next(e) isn't called, the event is recorded with error true, and pending.jsonl and pending.json are the only files the check wrote; with refuse false, or a gate at another seq, the call proceeds. With $.session.surfaces() empty, the refusal's text also goes to $.ui.log. In observe mode the same state refuses nothing and adds no context."
    level: integration
    covers:
      - BEH-07
      - BEH-08
  - id: VER-08
    status: active
    obligation: "In enforce mode, a state whose gate is report with refuse true puts the flag messages in the context of the next prompt.submit once, and not in a later one; a next prompt that starts with '/' gets none, and none is added after the run ends; a run-end gate adds no context; observe mode adds none."
    level: integration
    covers:
      - BEH-09
  - id: VER-09
    status: active
    obligation: "With python missing, an evaluator exit 2, a run past its timeout, an --out that isn't JSON, and a timer callback that throws, every tool call proceeds in both modes, events are still recorded, the status text shows 'progress: off (<reason>)', one toast per distinct reason appears, and adapter.log has the line. A hook that throws before next passes its event on unchanged, and one that throws after next keeps the result (ADR-006 D1's fail-open test). A test can't crash the hooks worker, so ERR-09 is checked by review, recorded in §9."
    level: integration
    covers:
      - BEH-14
      - ERR-01
      - ERR-02
      - ERR-07
      - ERR-09
      - ERR-10
      - QR-02
  - id: VER-10
    status: active
    obligation: "A session whose session.start has isInteractive false writes no file under devforgeai/ and draws nothing, and so does one whose first prompt.compose carries print; a tracked skill that loads before any session.start records nothing (ERR-08); with tracking off, nothing is written or drawn; with $.session.surfaces() empty, the adapter records as usual and each toast and status text also goes to $.ui.log."
    level: integration
    covers:
      - BEH-01
      - ERR-08
  - id: VER-11
    status: active
    obligation: "After a scripted run, the fs.write calls the test captures name exactly devforgeai/progress/.gitignore (holding '*'), the run's events.jsonl and state.json, current.json and adapter.log, and none names the project's .gitignore; a Write over 64 KiB is recorded without content; once the captured events.jsonl passes 3 MiB, new events carry no content, and at 4 MiB writing stops with 'progress: off (event log full)'; with fs.write refused under devforgeai/progress/, tracking stops for the session with ERR-03's status text and no further writes."
    level: integration
    covers:
      - BEH-15
      - ERR-03
      - ERR-11
      - QR-03
  - id: VER-12
    status: active
    obligation: "For mocked states, the text the adapter passes to $.ui.status reads 'brainstorm 6/8 · 1 flag', 'architecture 7/11 · your turn', 'brainstorm done', 'brainstorm ended', with ' · ticks only' and ' · enforce' where they apply, and $.ui.status isn't called again while the text stays the same. The band, mounted on terminal and desktop with a ui.render stub standing for the mods after it: shows the glyph row and the mode with its button, and the stub's element after them; shows none of its own rows while hasSurvey is true or no run is open; draws only row 1 when maxRows is 1, and no row wider than bodyColumns. The button has the key 'progress-mode' and no hotkey; a press runs IF-02 with the other mode and switches it, and a failed save keeps it; each flag is toasted once; ignored local entries give one toast at session.start."
    level: integration
    covers:
      - BEH-10
      - BEH-11
      - BEH-12
      - BEH-13
      - BEH-16
      - ERR-04
      - ERR-05
  - id: VER-13
    status: active
    obligation: "A run open before a reload continues after it with the next seq and the same ID, the timer evaluates it again, and no second run-end or skill-loaded is written."
    level: integration
    covers:
      - BEH-17
  - id: VER-14
    status: active
    obligation: "An Edit's content is the file it will leave, for one replacement and for replace_all; an Edit whose old_string is missing, repeated without replace_all, or in a file over 256 KiB is recorded without content."
    level: integration
    covers:
      - ERR-06
  - id: VER-15
    status: active
    obligation: "Dogfood in the CLI with the deployed plugin: a brainstorm run that writes the BRN without asking (observe mode) shows the status line, as '⚠ devforgeai: brainstorm …', and the band, and flags step 5 at the write gate, with no refusal; after 'Switch to enforce', a run that tries to write a non-open disposition without an answer is refused, and its retry after the user answers goes through. In a long architecture run, one /compact mid-run leaves no reply event twice in the log, and the time a recorded event takes late in the run is noted. Each run's events.jsonl validates against events.schema.json, and its manifest state is matched. The times of a recorded Write, of a late event and of an enforce check are recorded in §9."
    level: manual
    covers:
      - BEH-07
      - BEH-08
      - BEH-10
      - BEH-11
      - QR-01
      - QR-02
  - id: VER-16
    status: active
    obligation: "test_adapter_structure.py checks that hooks/hooks.json names one module that exists, plugin.json names types and the tracking setting (DM-05), CLAUDE.md's deploy command excludes *.test.ts, *.test.tsx, tsconfig.json and .claude-plugin/types, and VER-04's expected lines, read from hooks/progress.test.ts, validate against events.schema.json. claude plugin validate src/claude/DevForgeAI reports nothing refused, and its calls line names no $.http, $.mcp or $.env.set call (no network, QR-03); the result is recorded in §9."
    level: unit
    covers:
      - BEH-04
      - BEH-15
```

## 10. Rollout, migration and rollback

- **Order.** The probe (VER-01) ran first, on 2026-10-02, as a throwaway mod outside the plugin (§9). Version 2
  applies its answers; the build follows once Bryan approves it.
- **Branch.** The build runs on its own branch and worktree (ADR-001).
- **Plugin version.** The plugin's folder changes, so `plugin.json` takes the next free minor version at merge.
- **Repository records** (`CLAUDE.md`):
  - the deploy command excludes the module's tests, with the list in a variable so each line pastes under 100
    characters (`CLAUDE.md`, Traps):

    ```bash
    X=(--exclude=__pycache__ --exclude=results --exclude='*.test.ts' --exclude='*.test.tsx')
    X+=(--exclude=/tsconfig.json --exclude=/.claude-plugin/types/)
    rsync -a --delete "${X[@]}" src/claude/DevForgeAI/ .claude/skills/devforgeai/
    ```
  - the source-and-deploy `diff -rq` check excludes the same; the engine wrote no `.claude-plugin/types/` into a
    skills-dir copy (§9, P10), so nothing else;
  - Commands gains `claude plugin test src/claude/DevForgeAI`, `claude plugin validate src/claude/DevForgeAI` and
    `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress`;
  - `.gitignore` gains `src/claude/DevForgeAI/.claude-plugin/types/` and `src/claude/DevForgeAI/tsconfig.json`: loading
    the plugin from source with `--plugin-dir` writes the generated types, and a `tsconfig.json` at the plugin's root
    when there is none (create-a-mod); P10 checked only the skills-dir copies;
  - after a redeploy, an open session loads the new module with `/reload-plugins`;
  - a check that mods can load at all: `claude plugin test` in a folder with no mod prints "no hooks module to
    load" when they can, and "turned off" with the reason when they can't (troubleshoot); `/plugin` shows
    `N mod active · devforgeai` in a session that loaded it.
- **Who gets it.** Everyone who installs `devforgeai` gets the adapter in observe mode, which never blocks, once
  their Claude Code serves the hooks-modules rollout flag (§2); until then it doesn't load and nothing changes.
  `--safe-mode`, `--bare` and `disableAllHooks` also stop it, and on a managed machine an organization can refuse it
  (`allowManagedModsOnly`, or its own guard). In VS Code's chat panel it tracks and enforces but draws nothing (§2).
  The `tracking` setting turns it off; enforce mode is the user's choice, through the band's button.
- **Codex parity.** The Codex port can't run mods; the adapter is a Claude-only difference for Codex sessions to
  record in their import reports (the mods proposal's rule 8). The formats and `settings.py`'s rules are the
  shared contract.
- **Rollback.** Remove `hooks/`, `types/` and the two `plugin.json` keys; `settings.py` then has no caller.
  `devforgeai/progress/` in any project holds only ignored working data and can be deleted.
- **Pointers.** The design proposal's build order step 3 points here; when this is built, PRD-001 §11's FR-021
  row records it.

## 11. Implementation plan

1. Run the probe and record P1 to P13 (VER-01): done on 2026-10-02 (§9), and version 2 applies the answers.
2. Write `settings.py`'s tests, then `settings.py` (IF-01, IF-02, BEH-18; VER-02, VER-03).
3. Add `hooks/hooks.json`, `types/index.d.ts` and the `plugin.json` keys; check them with `claude plugin validate`.
4. Check that the test kit fires `skill.prompt`, `session.append`, `prompt.compose`, `session.end` and
   `classic.SessionStart` as `$` calls (the docs show `tool.call`, `prompt.submit`, `session.start`, `turn.complete`
   and `classic.*`); where one can't be fired, the test drives that hook another way and §9 says so. Then write the
   tests, then the recording: activation, runs, events and files (BEH-01 to BEH-05, BEH-15, BEH-17;
   VER-04, VER-05, VER-10, VER-11, VER-13, VER-14).
5. Write the tests, then evaluation and display: the timer, status line, band, toasts, mode and button (BEH-06,
   BEH-10 to BEH-13, BEH-16; VER-06, VER-12).
6. Write the tests, then enforce mode and failing open (BEH-07 to BEH-09, BEH-14; VER-07 to VER-09).
7. Add `test_adapter_structure.py` (VER-16), run plugin-validator, dogfood in the CLI (VER-15), and record the
   results and the `CLAUDE.md` changes (§9, §10).

## 12. Alternatives considered

- **An idle limit that ends a run.** Ending a run fires its end gate, so a pause would flag a half-done run and
  lose the answers given after it. Rejected by Bryan (2026-10-02): runs end at another skill, `/clear` or the
  session's end.
- **An entry in the project's `.gitignore`.** It edits a file the user tracks and shows as a change in every
  project and every eval scaffold. A `.gitignore` holding `*` inside `devforgeai/progress/` ignores the folder
  with no edit.
- **Parsing ticks or rules in the module.** Each adapter would carry its own copy. The evaluator holds the only
  copy (SPEC-012 §12).
- **Reading the local preference file in TypeScript.** Rules go in Python, one copy per port (the mods
  proposal's rule 2); `settings.py` is that copy for this plugin.
- **The module outside the plugin, in `src/tools/mods/`.** It would reach only this repository until a later
  spec moved it. Bryan chose the plugin (2026-10-02).
- **Observe mode only, enforce later.** ADR-006 gives D1 to this spec; Bryan kept it here (2026-10-02). The
  default stays observe.
- **Recording headless sessions.** It would add files to every eval scaffold and could change what graders see;
  evals must measure the skill alone.
- **Evaluating on every tool call before it proceeds.** It would slow every call in observe mode for nothing;
  only enforce mode's write gate needs an answer before the call.
- **A DM-02 event for a mode switch.** It would let the log carry mid-run switches, but DM-02 is approved and has
  no such kind; `adapter.log` records them until a SPEC-012 v2 adds one.

## 13. Open questions

Decided by Bryan on 2026-10-02:
- The adapter lives in the plugin (`src/claude/DevForgeAI/hooks/`).
- Enforce mode is specified and tested here; the default stays observe.
- No idle limit ends a run.
- Headless sessions are left untouched.
- VS Code: tracking only for now, with notices in the transcript (BEH-01); `progress.html` is a later spec.
  BEH-01 assumes VS Code's chat panel starts with `isInteractive` true and no surface; that is untested until
  someone runs the adapter there.

Notes:
- A mode switch during a run is in `adapter.log`, not in the event log, because DM-02 has no kind for it.
- Locking the mode at project level arrives with the shared-schema change (ADR-006 D3). Until then the button is
  always available.
- The probe ran on 2026-10-02 (§9). P9 wasn't run: whether mods run in `claude plugin eval`'s child runs is
  untested, and BEH-01 leaves headless sessions untouched either way.
- The button saves `.claude/devforgeai.local.md` in the project. This repository's `.gitignore` already ignores it
  (ADR-003); in a project whose `.gitignore` doesn't, git shows it as untracked, and the user adds the entry. The
  adapter never edits a `.gitignore` of the project's.
- `git` and `documents-updater` have no manifest, so their runs are tracked by ticks only, and loading either one
  ends the run before it (BEH-03). A `/devforgeai:git commit` after a brainstorm therefore shows
  `git <n>/<m> · ticks only`, and the brainstorm's run ends with `another-skill`.
- **your-turn is rarer than the design's mockups suggest.** SPEC-012 shows your-turn only when the last event is a
  turn's end. An AskUserQuestion wait happens inside a turn (§9, P7), so the status line says '· your turn' only
  when Claude ends its turn asking in prose; while the dialog is open, the dialog itself is the sign.
- **Compaction is untested.** Whether `/compact` re-delivers earlier response rows to `session.append`, which would
  record replies twice, wasn't tried; the mods docs don't say. The build checks it with one compaction during VER-15.
- **The event log grows with every event,** and BEH-04 rewrites it whole each time, since `$.fs` can't append. BEH-15
  bounds it (64 KiB of content an event, none after 3 MiB, nothing after 4 MiB); VER-15 times an event late in a long
  architecture run, not only a single Write.
- Toasts for flags appear in both modes. If they distract during dogfooding, a later display setting can quiet
  them; they never reach the model in observe mode.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-10-02 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | First draft, on Bryan's direction of 2026-10-02 and his four decisions: the adapter in the plugin, enforce mode specified here, no idle limit, headless sessions left untouched | all |
| 1 | 2026-10-02 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Before approval, after the advisor's review: no file before the session is known to be interactive (BEH-03, BEH-15); after a /clear the mode and timer start at the next tracked skill (BEH-06, BEH-16); a .catch returns its replay-safe next(e) (BEH-14); one timer-driven evaluation at a time (BEH-06); ERR-02's limit is $.process.run's timeoutMs; report-gate flags skip prompts starting with '/' and ended runs (BEH-09); every plugin skill opens a run (BEH-03); probe items P11 and P12; the deploy command as an array; §2's checked API list | BEH-03, BEH-06, BEH-09, BEH-14, BEH-15, BEH-16, ERR-02, VER-01, VER-04, VER-05, VER-08, §2, §9, §10, §13 |
| 1 | 2026-10-02 | Bryan | Approved | status |
| 2 | 2026-10-02 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | The probe (VER-01) ran on 2026-10-02, and §9 records its answers. P7 contradicted DM-01: a whole skill run can be one turn, and turn.complete's answer holds only its last text, so reply events now come from session.append rows with door response (DM-01, §3). Also from the probe: AskUserQuestion's answered rule (P5) and Bash's exit from 'Exit code N' (P6) in DM-01; ERR-01 names a missing program's rejection (P2); BEH-17 says a /clear empties $.state (P11); tests run in memory, with VER-04's expected lines in the test file (P12); the hooks-modules rollout flag (§2, §10); DM-03's contract rules from claude plugin validate; P13 added | §2, §3, DM-01, DM-03, BEH-17, ERR-01, VER-01, VER-04, VER-11, VER-16, §9, §10, §11, §13 |
| 2 | 2026-10-02 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Before approval, after the mods docs (saved in docs/research/Claude/mods/) were read against this version, the advisor's review, and Bryan's choices of 2026-10-02 (tracking only in VS Code; the recommendations): a refused call ({ deny }) is error true, never evidence (DM-01); answers and prompts count only from Claude Code and the person (next.origin, e.origin.kind) (DM-01, BEH-04); headless by session.start's isInteractive, notices to the transcript where nothing draws (BEH-01); the status line through $.ui.status, drawn as '⚠ devforgeai: …' (BEH-10); the band keeps later mods' drawing, fits maxRows and bodyColumns, gives way to a survey, serialises its draws, and its button has a key and no hotkey (BEH-11); /resume and /branch handled like /clear, with classic.SessionStart (BEH-05, BEH-06, BEH-16, BEH-17); timeouts sized to the documented limits, including session.end's shared 1.5 seconds (BEH-05, BEH-16, ERR-01, ERR-02); pending files overwritten, content capped, the log bounded under 4 MiB (BEH-08, BEH-15, ERR-06, new ERR-11); a worker crash and a throwing timer (new ERR-09, ERR-10); ERR-08 rewritten for a skill before session.start; $ only in top-level functions of progress.tsx (§2, §3); tests and records (VER-04, VER-05, VER-07, VER-09 to VER-12, VER-16, QR-03); the probe's raw shapes in docs/runbooks/spec-013-probe.md (§9); deploy exclusions, /reload-plugins and a can-mods-load check (§10); a test-kit check (§11); notes on your-turn, compaction and log growth (§13); after the advisor's last review, the run ID's time from $.clock.now() (BEH-03), ERR-11 scoped to the run, VER-15 covering /compact and a late event | DM-01, DM-02, DM-03, BEH-01, BEH-03 to BEH-06, BEH-08, BEH-10 to BEH-12, BEH-14 to BEH-17, ERR-01, ERR-02, ERR-06, ERR-08 to ERR-11, VER-04, VER-05, VER-07, VER-09 to VER-12, VER-15, VER-16, QR-03, §2, §3, §9, §10, §11, §13 |
| 2 | 2026-10-02 | Bryan | Approved | status |
| 2 | 2026-10-02 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records the build on `feat/spec-013-progress-adapter`, its results, and the build decisions and departures for Bryan's review | §9 |
