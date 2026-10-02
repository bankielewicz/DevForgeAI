# DevForgeAI progress UI

**Status:** design proposal, not approved. Nothing here is built. It expands B1 (chain-navigator) of `devforgeai-claude-mods.md` and follows that document's design rules (its section 3). It changes no spec, skill or plugin version.

**Goal:** the framework is open source and portable. It is dogfooded now in the Claude Code CLI; the target hosts are also the Claude desktop app and VS Code, and other tools later. Sections 7 and 8 are written for that.

**Date:** 2026-10-02. **Author:** claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9), at Bryan's request, reviewed with the advisor.

**Sources:**
- the mod API in Claude Code 2.1.287 (its `plugin-authoring` skill and generated `claude-code.d.ts`). The API is early access and changes between releases.
- the Workflow section of each skill's `SKILL.md` in `src/claude/DevForgeAI/skills/`;
- the `/insights` report of 2026-10-02;
- Anthropic's announcement, "Claude Code mods" (claude.com/blog/claude-code-mods). It says mods ship inside plugins, are installed from the Claude directory or with `/plugin`, can be submitted to the directory, and are not sandboxed;
- community mods shown on X on 2026-10-01: an animated Clawd for each session, whose animation changes with each hook, and Clawd characters in costumes for different work.

Section 10 lists what is still unverified.

## Contents

1. The problem
2. The views
3. Where the data comes from
4. Step manifests
5. Step states and skip detection
6. The Journey and Workflow pane
7. Portability: one core, many hosts
8. Graphics
9. Buttons, links and what reaches the model
10. Verified and unverified
11. Build order
12. Open questions for the owner

## 1. The problem

Every DevForgeAI skill has a numbered checklist in its Workflow section. The skill tells Claude to copy the checklist into its reply and tick items off as it goes. In practice:

- **Claude skips steps, and the only record is Claude's own word.** In one dogfood run, Claude was asked to brainstorm getting teens into a library with "no questions asked". It wrote BRN-001 without asking a single question. A second run of the same prompt left every decision open (/insights, 2026-10-02).
- **The checklist scrolls away.** It lives in the reply text, so watching a long run means scrolling back to find it, and its ticks are self-reported.
- **Phases are skipped the same way.** Nothing on screen shows that an architecture run started without a PRD, or that epics are being written before the context documents exist.

The design has four goals:

| ID | Goal |
| --- | --- |
| G1 | Show where the project stands in the framework, phase by phase (the Journey). |
| G2 | Show the running skill's steps, where Claude is, and what it's doing (the Workflow). |
| G3 | Make a skipped step visible as it happens, judged by evidence rather than Claude's ticks. |
| G4 | Be pleasant to look at, with a picture for each phase and each kind of work, and an animated mascot doing the current step. |

Non-goals:
- deciding anything for the user;
- replacing evals: a skill's eval suite stays the proof that the skill works;
- building other tools' adapters here: Codex can't run Claude Code mods, so a Codex adapter is for Codex sessions to build, against the contracts in section 7.

## 2. The views

| View | Where | Shows | Always on? |
| --- | --- | --- | --- |
| Status line entry | status line | `architecture 7/11 · your turn` | while a DevForgeAI skill runs |
| Journey band | above the prompt, 2 rows | mini phase emblems, the current skill's step count and state, a button to open the pane | while a skill runs, or when a phase needs attention; otherwise the hook returns `next(e)` and the band takes no rows |
| Journey and Workflow pane | docked beside the transcript, or inline | the phases as a vertical path; finished phases collapsed; the current phase expanded into its step list, mascot scene and current step | opened by the band's button or `/progress`; opens by itself only when the terminal is in fullscreen and at least 144 columns wide |
| Wide layout | the same pane, 120 columns or more | the phases in a horizontal row with large emblems, and the Workflow in two columns below | when the pane is that wide |
| Skill health | a pane | for one skill, a grid of its steps across its recent runs, coloured by state | opened by a button (Part A, for dogfooding) |
| Toasts | bottom of the screen | step milestones, and each flag as it's raised | events only |

A pane that opens without being asked docks only in the fullscreen layout from 144 columns. So the status line and the band are the views that are always available, and the pane opens on request.

## 3. Where the data comes from

| Signal | Event or call | What it gives |
| --- | --- | --- |
| Project phases | `chain_state.py`, run with `$.process.run` at `session.start` and after any write under `docs/specs/` | every document's ID, type, status and version; `[NEEDS ADR` and `[NEEDS CLARIFICATION` markers; stale upstream links (`devforgeai-claude-mods.md`, B1) |
| Run history | the progress state file (section 7); `$.store`, keyed by `$.session.root()`, only as a cache | the project's past skill runs, each with its step states, evidence and flags |
| Step list | `skill.prompt`: `e.skill` and `e.text` | the skill's checklist block (`- [ ] N. Title`), taken from the prompt the deployed skill actually sent, plus a hash of that block |
| Claims | `session.append`, rows with door `response` | the ticks in Claude's replies (`- [x] N.`), and `(skipped: <reason>)` (the git skill's form of a legitimate skip) |
| Evidence | `tool.call`, calling `await next(e)` and reading the result | scripts run and their outcome, files read, globbed or written, AskUserQuestion answers |
| Your answers | `prompt.submit`, and AskUserQuestion results | that you replied after a proposal; the run's user-owned steps need this |
| Turns | `turn.start`, `turn.complete` | when a step is waiting on you, and when a run goes idle |

Two limits:
- **The context skill gives no claims.** It keeps its checklist in its working notes rather than the reply (its `SKILL.md`, Workflow), so the tracker follows it by evidence alone.
- **The step list is the one that ran.** It comes from the skill's prompt as it loads, not from `src/`. If the deployed copy is stale, the tracker shows the deployed copy's steps, and A7 (deploy-drift) in `devforgeai-claude-mods.md` reports the gap.

## 4. Step manifests

The checklist gives each step's number and title. A manifest adds what the tracker needs to judge the step:

| Field | Values | Meaning |
| --- | --- | --- |
| `kind` | `read`, `think`, `ask`, `forge`, `inspect`, `report` | picks the mascot's activity (section 8) |
| `need` | `required`, `conditional`, `text-only` | a `conditional` step can be not applicable on one of the skill's own branches; a `text-only` step has nothing to show but a tick |
| `evidence` | a list of rules | what counts as proof, and how strong it is (below) |
| `gate` | `write`, `report`, or none | where the tracker checks the steps before it (section 5) |
| `userOwned` | true or false | the step's decision belongs to the user, so it needs your answer as evidence |

Evidence rules, strongest first:

| Rule | Example | Strength |
| --- | --- | --- |
| `script` | `validate_brn.py <the written BRN>` ran and exited 0 | strong |
| `answer` | an AskUserQuestion answer, or a prompt from you after the proposal | strong |
| `write` | Write or Edit to `docs/specs/brainstorm/BRN-*.md` | medium |
| `read` | Read, Glob or Grep under a path | medium |
| `none` | a text-only step | the tick is all there is |

**Brainstorm** (from its `SKILL.md`):

```yaml
skill: devforgeai:brainstorm
checklistHash: <sha256 of the checklist block>
steps:
  1: { kind: read,    need: required,  evidence: [read: docs/specs/brainstorm/] }
  2: { kind: think,   need: text-only }
  3: { kind: think,   need: text-only }
  4: { kind: think,   need: text-only }
  5: { kind: ask,     need: required,  userOwned: true, evidence: [answer] }
  6: { kind: forge,   need: required,  gate: write,
       evidence: [write: docs/specs/brainstorm/BRN-*.md] }
  7: { kind: inspect, need: required,  evidence: [script: validate_brn.py] }
  8: { kind: report,  need: required,  gate: report }
```

**Architecture** (from its `SKILL.md`):

```yaml
skill: devforgeai:architecture
checklistHash: <sha256 of the checklist block>
steps:
  1:  { kind: read,    need: required,    evidence: [script: validate_policy.py] }
  2:  { kind: read,    need: required,    evidence: [read: docs/specs/prd/] }
  3:  { kind: read,    need: required,    evidence: [read: docs/specs/prd/PRD-*.md] }
  4:  { kind: read,    need: required,    evidence: [read: docs/specs/arch/] }
  5:  { kind: read,    need: conditional, when: "the user named paths to inspect",
        evidence: [read: outside docs/specs/] }
  6:  { kind: think,   need: text-only }
  7:  { kind: ask,     need: conditional, userOwned: true,
        when: "a question isn't settled by mandated policy", evidence: [answer] }
  8:  { kind: ask,     need: required,    userOwned: true, evidence: [answer] }
  9:  { kind: forge,   need: required,    gate: write,
        evidence: [write: docs/specs/arch/ARCH-*.md, write: docs/specs/adr/ADR-*.md] }
  10: { kind: inspect, need: required,    evidence: [read: each file written at step 9] }
  11: { kind: report,  need: required,    gate: report }
```

Architecture's step 10 is weak. ERR-05 comes from the skill's own self-check, which has no script, so re-reading each written file is the only evidence available. A script for that check would make step 10 strong; that's open question 5 in `devforgeai-claude-mods.md`.

The other skills' gates, from their checklists:

| Skill | User-owned steps | Write gate | Strong evidence |
| --- | --- | --- | --- |
| prd | 4 (new PRD or extend), 7 (interview the gaps, settle quality categories) | 8 | 1 (`validate_policy.py`) |
| epic | 6 (propose and confirm the grouping) | 7 | none; 8 has no script |
| context | 6 (interview), 9 (approve only on explicit words) | 7 | 8 (`context_check.py check`); claims unavailable (section 3) |
| documents-updater | the user's choices in steps 3 and 4 when asked | 5 | 6 (`check_docs.py`) |
| git | the merge go-ahead (7), and blocked or unrelated paths (5) | 5 (commit) | 5 (`scan_staged.py`), 1 (`repo_state.py`), 7 (`qa_state.py`) |

**Where manifests live.**
- **Part A (dogfooding):** the plugin's progress component holds them, as JSON in `src/claude/DevForgeAI/progress/manifests/`, keyed by skill and checklist hash (SPEC-012). When a skill's checklist changes, its hash no longer matches. The tracker then falls back to claims only and shows "manifest out of date" until someone updates it.
- **Part B (shipped):** each skill would carry its own manifest, for example `skills/<skill>/references/progress.json`, written in the skill's spec, so the Codex port could use it too.

## 5. Step states and skip detection

| Glyph | State | Colour | Meaning |
| --- | --- | --- | --- |
| `○` | pending | dim | not reached |
| `◉` | current | accent, animated | the first required step without a claim or evidence |
| `◆` | your turn | blue | a user-owned step is waiting for your answer |
| `✓` | done | green | evidenced, or ticked if the step is text-only |
| `✓?` | claimed | amber | ticked, but the evidence its rules require hasn't been seen |
| `⤼` | skipped, with reason | grey | Claude marked it `(skipped: <reason>)`; the reason is shown |
| `–` | not applicable | dim | a conditional step whose condition doesn't hold; the condition is shown |
| `✗` | skipped | red | at a gate, a required step had neither a claim nor evidence |
| `!` | rule broken | red | a gate found content that needed a step which didn't happen |
| `?` | unconfirmed | dim | a text-only step with no tick: nothing could show it happened, so it's never flagged (added by SPEC-012) |

**Flags are raised only at gates.** Claude ticks late and works on neighbouring steps together. If the tracker marked a step skipped the moment a later step showed evidence, it would raise false alarms and you would stop trusting the pane. So during a run, steps that haven't been seen stay `○`, with no flag. There are three gates:

1. **Write gate.** At the step's first Write or Edit, every required step before it must be done or claimed. A claimed step whose evidence rule is `script` or `answer` must be evidenced.
2. **Report gate.** At the reply that ticks the report step, every required step before it, including validation, must be done.
3. **Run end.** When another skill loads, the session ends or is cleared, or the run sits idle past a limit, the tracker evaluates the whole run and stores it.

A step done out of order is recorded in the run log, not flagged.

**User-owned steps check what was written, not just the order.** The brainstorm rule is that dispositions and convergence are written only when you confirmed them; otherwise they stay `disposition: open`, `reason: null` and `status: draft` (`CLAUDE.md`, "Rules a change must not break"; VER-02). So at brainstorm's write gate the tracker reads the BRN being written, which is in the Write call's input:

| Step 5 has an answer? | The BRN being written | Result |
| --- | --- | --- |
| yes | any dispositions | fine |
| no | every disposition `open`, `status: draft` | fine: the skill's own path when you haven't confirmed; step 5 shows `–` "no confirmation; left open" |
| no | any disposition other than `open`, or `status` beyond `draft` | `!` on step 6, `✗` on step 5 |

The other skills' user-owned steps work the same way: architecture's accepted ADRs and confirmed outcome, epic's confirmed grouping, and context's approval on your explicit words.

**Observe and enforce** (`devforgeai-claude-mods.md`, rule 4):

| Mode | At a flag | Use it for |
| --- | --- | --- |
| observe | shows the flag to you (band, pane, toast) and logs it; tells the model nothing | dogfooding: Claude's skip stays visible as a finding for the skill |
| enforce | also refuses the gate's tool call with the reason, and adds a note to the model's context listing the steps that are missing | real work |

In enforce mode, the brainstorm example above would be refused. The Write of a BRN that sets dispositions without your answer doesn't happen, and Claude is told that step 5 needs your confirmation first.

**Phase skips.** The Journey checks each phase's prerequisites when the phase's skill loads:
- **Architecture with no PRD**, or **epics with no ARCH**: a red `!` on that segment of the path. The skill itself stops in these cases, and the Journey shows why.
- **Epics before the context documents**: an amber note. ADR-004 D5 places context after Architecture Definition and before epics and stories, and the story step reports missing context documents.
- **Phases not built yet** (stories, QA) draw as "coming", never as skipped.

## 6. The Journey and Workflow pane

The mockups show layout; the pictures are placeholders here, and the prototype (section 8) draws them. Conventions are those of `devforgeai-claude-mods.md`, section 4: `[ Label ]` is a button, `[ Label ]*` the primary one, `‹ID›` a `file:` link, `↗` an `https:` link. Values are made up, for a project named dental-no-shows.

### 6.1 Docked pane during an architecture run (about 58 columns)

Finished phases are collapsed, the current phase is expanded, and future phases are dim:

```
╭─ DevForgeAI · dental-no-shows ──────────────── [ Close ] ─╮
│ [bulb ]  Brainstorm     ✓ approved   ‹BRN-001›   09-30    │
│    │                                                      │
│ [scroll] PRD            ✓ approved   ‹PRD-001› v2  10-01  │
│    │                                                      │
│ [blue- ] Architecture   ◉ step 7 of 11 · ARCH-001 (new)   │
│ [print ] ┌────────────────────────────────────────────┐   │
│    │     │ [scene: Clawd in a hard hat holds up a "?" │   │
│    │     │  sign on a blueprint grid · 32×16 px]      │   │
│    │     └────────────────────────────────────────────┘   │
│    │      ✓ 1  Resolve policy          policy script ok   │
│    │      ✓ 2  Select the PRD          PRD-001            │
│    │      ✓ 3  Read the PRD            read               │
│    │      ✓ 4  Select or create ARCH   new ARCH-001       │
│    │      –  5  Inspect within scope    no paths named    │
│    │      ✓ 6  Identify questions      text               │
│    │      ◆ 7  Resolve each question   your turn: DEC-03  │
│    │      ○ 8  Propose and confirm                        │
│    │      ○ 9  Write ARCH and ADRs                        │
│    │      ○ 10 Validate every file                        │
│    │      ○ 11 Readiness and report                       │
│    │      Now: Claude asks where reminders should run     │
│    │      (3 options). Answer in the dialog.              │
│    ┆                                                      │
│ [map  ]  Context        ○ next: /devforgeai:context       │
│ [mount]  Epics          ○                                 │
│ [book ]  Stories        coming (SPEC-009)                 │
│                                                           │
│ [ Run log ]   [ Skill health ]   [ Hide band ]            │
╰───────────────────────────────────────────────────────────╯
```

Pressing a finished phase's row expands its last run, from `$.store`: steps, flags and date.

### 6.2 The same pane after a skip at brainstorm's write gate

This is the teen library run from /insights, in observe mode:

```
│ [bulb ]  Brainstorm     ! flagged · step 6 of 8           │
│ [     ]  ┌────────────────────────────────────────────┐   │
│    │     │ [scene: Clawd, worried, sweat drop and "!" │   │
│    │     │  beside the anvil]                         │   │
│    │     └────────────────────────────────────────────┘   │
│    │      ✓ 1  Intake                  BRN-*.md listed    │
│    │      ✓ 2  Select a framework      text               │
│    │      ✓ 3  Diverge                 text               │
│    │      ✓ 4  Evaluate                text               │
│    │      ✗ 5  Propose dispositions    no answer from you │
│    │      ! 6  Write the BRN           ‹BRN-002› sets 9   │
│    │                                   of 15 dispositions │
│    │                                   you never confirmed│
│    │      ○ 7  Validate the BRN                           │
│    │      ○ 8  Report and hand off                        │
│    │      [ Why flagged? ]   [ Fill prompt: back to 5 ]*  │
│    │      [ Copy as finding ]                             │
```

- "Why flagged?" expands the evidence: which calls were seen, and the gate's rule with its source.
- "Fill prompt: back to 5" puts "Go back to step 5: propose the dispositions and ask me to confirm them before writing." in the prompt box. You send it, or don't.

### 6.3 Journey band (2 rows, above the prompt)

```
 ▣ ▣ ◉ ▢ ▢ ▢  Architecture 7/11 · ◆ your turn: answer the question above   [ Open ]
              ✓ policy · PRD-001 · ARCH-001 new                    1: Open pane
```

The six marks are mini phase emblems, 4×4 pixels each (`Raster`). Finished phases are lit, the current one pulses, and the later ones are outlines. When a flag is up, the second row shows it in red instead, for example `✗ step 5 skipped · ! BRN-002 sets unconfirmed dispositions`.

### 6.4 Wide layout (inline pane, 120 columns or more)

```
╭─ DevForgeAI · dental-no-shows ──────────────────────────────────────────────────────── [ Close ] ─╮
│  [ bulb   ]       [ scroll ]       [ blue-  ]       [  map   ]       [ mount- ]       [  book  ]  │
│  [ 16×16  ]━━━━━━━[ 16×16  ]━━━━━━━[ print  ]┄┄┄┄┄┄┄[ 16×16  ]┄┄┄┄┄┄┄[  ain   ]┄┄┄┄┄┄┄[ coming ]  │
│  Brainstorm ✓     PRD ✓            Architecture ◉   Context          Epics            Stories     │
│  ‹BRN-001›        ‹PRD-001› v2     7 of 11          next                                          │
│ ───────────────────────────────────────────────────────────────────────────────────────────────── │
│  STEPS                                    │  [scene: Clawd, "?" sign, blueprint, 48×24]           │
│  ✓ 1  Resolve policy    policy script ok  │                                                       │
│  ✓ 2  Select the PRD    PRD-001           │  Now: asking where reminders should run               │
│  …                                        │  Evidence so far: 6 of 6 required steps               │
│  ◆ 7  Resolve each question  DEC-03       │  [ Run log ]  [ Skill health ]                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 6.5 Skill health (Part A, for dogfooding)

One skill's steps across its recent runs, drawn as a `Raster` grid with one cell per run (oldest left):

```
╭─ Skill health · brainstorm · last 12 runs ─────────────────────── [ Close ] ─╮
│ STEP                              RUNS                                       │
│ 1  Intake                         ████████████                               │
│ 5  Propose dispositions, confirm  ██▓▓█░██░███   3 skipped, 2 left open      │
│ 6  Write the BRN                  ████████▒███   1 rule broken               │
│ 7  Validate the BRN               ██████████▒█   1 claimed, not run          │
│ █ evidenced  ▓ text-only or not applicable  ▒ claimed only  ░ skipped        │
│ [ Copy as findings ]*   [ Choose skill ▾ ]                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

This shows which steps Claude skips most often, and so which parts of a skill's text need work. It reads the run history in `$.store`.

### 6.6 Status line and toasts

```
architecture 7/11 · your turn
brainstorm 6/8 · 1 flag
```

```
✓ Step 6 done: ‹BRN-002› written
✗ Step 5 skipped: BRN-002 was written without your confirmation
✓ PRD phase complete: PRD-001 v2 approved
```

## 7. Portability: one core, many hosts

Claude Code's mod API reaches the CLI, the desktop app and VS Code with one module; each draws on its own surface. Other tools don't have that API. So everything except drawing and listening stays out of the mod:

| Layer | What it is | Written in | Used by |
| --- | --- | --- | --- |
| Manifests | each skill's steps, kinds, evidence rules and gates (section 4) | JSON | every host |
| Evaluator | turns a manifest and an event log into step states, gates and flags (section 5) | Python, like the skills' validators | every host |
| Host adapter | listens to the host's own events, writes them as events, calls the evaluator, and refuses at gates in enforce mode | the host's extension language: a TypeScript mod for Claude Code | one host each |
| Renderer | draws a progress state | `Svg`, `Image` or `Raster` in Claude Code (section 8); a static HTML page anywhere | any host that can show it |
| Assets | characters, props, emblems, backdrops and animation timelines | SVG and JSON | every renderer |

**Three contracts.** Each is a versioned JSON format with a `format` field, as the prototype's sprite block already has:
- **`devforgeai-events/1`** is what an adapter writes, one JSON object per line. Each object has a kind (skill loaded, tool call, answer, claim, turn), a time, the skill, and that kind's fields: the tool, path and exit code; the ticked step number; whether a question was answered. Claude Code's adapter fills it from `skill.prompt`, `tool.call`, `session.append`, `prompt.submit` and `turn.*` (section 3).
- **`devforgeai-progress/1`** is what the evaluator writes: the project's phases (from `chain_state.py`), the current run's steps with their states, evidence and notes, the flags, and the next step. Renderers read only this.
- **The manifest format** of section 4.

**The evaluator is Python,** at `src/claude/DevForgeAI/progress/evaluate.py`, with its tests in `src/tests/progress/` (SPEC-012). Rule 2 of `devforgeai-claude-mods.md` applies: one copy of each rule, which the Codex port can share. The mod calls it with `$.process.run` at gates and when an event matches an evidence rule, not on every tool call. Python is already a dependency of the skills' validators.

**State is a file.** Other tools can't read `$.store`, so each run's files live in the project root's `devforgeai/` folder, where DevForgeAI keeps operational files: `devforgeai/progress/runs/<run>/events.jsonl` and `state.json`, plus `devforgeai/progress/current.json` for renderers (SPEC-012 §4). `$.store` is only a cache.

**Hosts:**
- **Claude Code CLI:** the mod, drawing `Raster` cells, or `Image` in kitty and Ghostty. Dogfooding happens here first.
- **Claude desktop app and VS Code:** the same mod, drawing `Svg`. How a `Pane` appears in VS Code (docked, inline or a separate panel) is unverified (section 10).
- **Codex and other tools:** an adapter of their own that writes `devforgeai-events/1`, built by those tools' sessions (`src/codex/` is Codex sessions' work). Until an adapter exists, any tool can run the evaluator and open `progress.html`.
- **`progress.html`:** a static page the evaluator writes beside the state file. It draws `devforgeai-progress/1` with the same SVG assets and needs no mod API, so it works with any tool and any browser. The prototype page is already a renderer of this kind.

**Rules come in layers** (ADR-006, accepted, extending ADR-003). This is DevForgeAI's adaptive model: a core set of skills and rules, then the project's own, then personal settings.
- **Framework:** the manifests the plugin ships; their content rules for decisions that belong to the user can't be weakened by any layer.
- **Organization and project:** they may add rules to a framework manifest and supply manifests for their own skills, never remove or relax a rule (SPEC-012 BEH-17).
- **Personal:** `progress.mode` (observe or enforce) in the local preference file, when the project allows it; display settings (character, animation) in each host's own settings.

DevForgeAI's own repository is just a project with a richer project layer.

**The character travels with the framework.** Because the framework runs outside Claude Code, its default character is Ember, its own. Clawd is a skin offered only when the host is Claude Code (open question 1).

## 8. Graphics

**One vector source.** Every asset is drawn once as SVG: both characters and their props, the eight emblems and the six backdrops. The parts that move are named groups (`#eyes`, `#arm-right`, `#hammer`), so an animation is a set of transforms on groups. Scenes are designed at the shape of a 40×10-cell box, about 1.75:1, so they fit the terminal and the desktop app alike.

**Animation as data.** Each activity has a small timeline: for each group, keyframes of position, rotation, scale or opacity over a loop of about one second. Every renderer uses the same timeline. The SVG renderer turns it into SMIL animation, and the cell renderer samples it at each frame time.

**Renderers by surface:**

| Surface | Element | How it's drawn |
| --- | --- | --- |
| desktop app, VS Code, mobile | `Svg` | the SVG with SMIL animation, which needs `isInteractive: true`; the source may be at most 131,072 characters |
| kitty, Ghostty | `Image` | PNG frames rasterized from the SVG, swapped with `$.ui.blit` |
| other terminals, including Windows Terminal | `Raster` | cells fitted to the rasterized art (below) |
| any browser | `progress.html` | the SVG directly |

The mod chooses by surface. `e.surface` separates the desktop app, VS Code and mobile from the terminal. In a terminal the mod tries `Image` first, and switches to `Raster` when `$.ui.blit` refuses because the terminal can show only the image's alt text.

**Smooth cells.** The mod can't rasterize SVG while it runs, because it has no DOM and no Node. So a build script renders each layer (backdrop, character frame, prop) from the SVG to RGBA at the scene's cell grid. It supersamples and averages, so edges blend instead of stair-stepping, and ships the results as assets. While running, the mod composites the current frame's layers and fits each cell:

- A cell shows one glyph and two colours. The quadrant glyphs (`▘▝▖▗▚▞▛▜▙▟▀▄▌▐█`, and a space) cover all 16 patterns of a 2×2 grid of sub-pixels.
- For each cell, the fit tries every pattern, colours each side with the average of its sub-pixels, and keeps the pattern that differs least from the art.
- A sub-pixel is half a cell wide and half a cell tall, so it's tall rather than square. That's why the source is rendered at the cell grid's shape.
- A partly transparent edge can only blend against a known colour. So scenes have opaque backdrops, and emblems drawn on the terminal's own background keep hard edges.
- At 8×4 cells and smaller, emblems use hand-drawn pixel versions instead of a fit. In the prototype, fitted emblems turned into blobs at the band's 4×2 cells and were muddy at the pane's 8×4. Icon sets hand-tune their smallest sizes for the same reason.

Finer block characters (2×3 sextants and 2×4 octants) are outside what a `Raster` accepts: one character from the Basic Multilingual Plane per cell. A WASM rasterizer inside the mod would allow rendering while the mod runs; whether a hooks module can load WASM is unverified (section 10).

**Pixel style.** The first prototype's 16×16 pixel art stays as a `style: pixel` setting. It's the cheapest to draw, and some people prefer the look.

**Animation timing.**
- In the terminal, one `$.clock.every` timer started at `session.start` swaps 8 to 10 frames a second with `$.ui.blit` (`requestId`, `key`, `cells`, `columns`, `rows`). Up to 120 blits a second are taken.
- With `Svg`, the SMIL animation runs inside the element, so the mod draws again only when the state changes.
- Animation pauses when nothing is mounted and when the run is idle (the character dozes).
- The drawing reads its state from `$.state`, which survives a hot reload; module variables don't.
- An `animation` setting (`on`, `reduced`, `off`) holds the character on one frame, or turns the scenes off and keeps the emblems.

**The character.** A `character` setting with two choices:
- **Ember**, a small forge spark, drawn from DevForge's forge metaphor. It's the framework's own character, and the default in every host.
- **Clawd**, Claude Code's mascot, offered only when the host is Claude Code. Community mods already draw it, including a Clawd that animates differently for each hook and Clawds in costumes for different work. For a plugin published to the Claude directory, the announcement gives no guidance on using Clawd, and a plugin carrying Anthropic's mascot could read as endorsed by Anthropic.

Either character does each step's kind of work in front of the phase's backdrop, with a prop or costume for the activity. Each loop lasts about a second:

| Step kind | Activity | Prop or costume |
| --- | --- | --- |
| `read` | eyes move across an open book | book |
| `think` | dots appear one by one in a thought bubble | thought bubble |
| `ask` | holds up a `?` sign, bobbing | sign |
| your turn | waves at you under a `!` bubble | none |
| `forge` | hammers on an anvil, sparks fly | hammer, anvil |
| `inspect` | sweeps a magnifying glass, sparkle on success | magnifier |
| `report` | holds up a scroll and bows | scroll |
| phase done | jumps under confetti | none |
| flagged | sweat drop, `!` | none |
| idle | dozes, `z` drifting up | none |

Each phase can also add a hat: a hard hat for Architecture, for example.

Phase emblems are drawn at three sizes: 16×8 cells for the wide layout, 8×4 cells for the pane's phase rows, and 4×2 cells for the band. The emblems and backdrops:

| Phase | Emblem | Colours | Backdrop |
| --- | --- | --- | --- |
| Brainstorm | lightbulb with sparks | yellow, white glow | night sky with stars |
| PRD | scroll with three check lines | parchment, ink | writing desk |
| Architecture | blueprint with a columned building | blueprint blue, white lines | blueprint grid |
| Context | folded map with a pin | green, cream | library shelves |
| Epics | mountain with a flag | purple, snow | mountain range |
| Stories | open storybook | teal, cream | book pages |
| QA | magnifier with a check | rose, green | (coming) |
| Ship | rocket | orange, steel | (coming) |

The colours are saturated mid-tones, so they read on dark and light themes alike. The prototype has a render switch: **Vector** is what the desktop app and VS Code draw, **Smooth cells** is what Windows Terminal draws, and **Pixel** is the first draft. It rasterizes the SVG live in the browser's canvas; that's a prototype shortcut, not the mod's path, which uses assets built ahead of time.

## 9. Buttons, links and what reaches the model

- **Buttons that start work fill the prompt box; they never send it.** Examples: "Fill prompt: back to 5", and `/devforgeai:context` from the Journey. Each phase's next step is also offered as a Tab suggestion when a skill's run ends.
- **The mode button:** the band and pane show observe or enforce, with **Switch to enforce** or **Switch to observe**. Pressing it saves your choice in your local preference file; when the project locks the mode, the button is unavailable and the band names the setting that locks it (ADR-006 D3).
- **Buttons that only show something act at once:** "Why flagged?", "Run log", "Skill health", "Copy as finding".
- **Links:** documents are `file:` links in `Markdown` (`‹PRD-001›`). A PR or issue is a `Link` to GitHub, which allows `https:` only.
- **`/progress`** opens the pane. **`/progress log`** prints the current run's log as a command output row; Claude can read that row too, which helps when asking it to explain a flag.
- **The model hears about flags only in enforce mode**, at a gate, through the refused call's reason and the result's `context`. In observe mode the tracker never nudges, so dogfooding keeps finding what Claude skips.
- **You can override a step's state** from the pane, for example marking a step not applicable. The override is recorded in the run log with your name for it, and the tracker never makes that choice itself.

## 10. Verified and unverified

**Verified** in the 2.1.287 declarations:
- **Events:** `skill.prompt` (`skill`, `text`), `session.append` (door `response`, content blocks), `tool.call` results, `prompt.submit`, `turn.start` and `turn.complete`.
- **Graphics:** `Raster` (`columns`, `rows`, `cells` as `[codePoint, fg, bg]` triplets, `0x01000000` for the default colour, 1,024 colour pairs); `$.ui.blit` for a `Raster` (`requestId`, `key`, `cells`, `columns`, `rows`; up to 120 a second); `Image` limited to kitty and Ghostty; `$.ui.blit` refusing when an `Image` draws its alt text; `Svg` in the desktop app, VS Code and mobile element tables, with SMIL animation when `isInteractive` and a 131,072-character source limit; `Raster` accepting one Basic Multilingual Plane character per cell.
- **Layout:** `Box` flex layout, borders and background colours; the pane's 144-column rule for opening by itself.
- **State and calls:** `$.state`, `$.store`, `$.session.root()`, `$.clock.every`.

**Unverified.** Each has a check:

| Question | Check |
| --- | --- |
| Does `skill.prompt`'s `e.text` include the checklist block as written? | log `e.text` when `/devforgeai:brainstorm` loads |
| Are the ticks in replies readable from `session.append` content as Claude writes them, including in long replies? | log the rows of one run |
| How does `skill.prompt` spell plugin skill names (`devforgeai:brainstorm`)? | log `e.skill` |
| Can the tracker tell an AskUserQuestion answer from a dismissed dialog? | log `tool.call` results for both |
| How much of `$.store`'s 4 MiB does a run history use? | measure 20 stored runs; keep the last N per project |
| Does Windows Terminal draw the quadrant glyphs as exact fractions of a cell, without seams? | the prototype's Smooth cells, then a test mod |
| Can a hooks module load WASM, for rasterizing SVG while the mod runs? | a probe module that instantiates a tiny WASM file |
| How does SMIL in an interactive `Svg` perform at 8 to 12 frames a second, when the scene is drawn again on each state change? | a desktop-app probe |
| How does a `Pane` appear on the `vscode` surface: docked, inline or a separate panel? | a VS Code probe |
| Is the delay of one `$.process.run` per evidence event acceptable? | time the evaluator over one recorded run |

## 11. Build order

1. **A logging probe with no UI**: settle the unverified items above. SPEC-013 runs it as its VER-01, before the adapter is built.
2. **Contracts and evaluator** (SPEC-012, approved): `devforgeai-events/1`, `devforgeai-progress/1`, `devforgeai-manifest/1`, the brainstorm and architecture manifests, and the Python evaluator, with tests that feed recorded event logs in and check the progress states that come out.
3. **Claude Code adapter** (SPEC-013, draft): events from the hooks, evaluator calls at gates, observe mode, the status line and a text-only band.
4. **The pane as text**: Journey path and step list, with glyphs only.
5. **Graphics**: SVG assets and timelines; the `Svg` renderer for the desktop app and VS Code; the build script for cell assets and the `Raster` renderer; `Image` for kitty and Ghostty; the `animation` and `character` settings.
6. **`progress.html`**, the renderer for any tool.
7. **Skill health** for dogfooding.
8. **Enforce mode** at gates, once observe mode has run long enough to trust its flags. Its mechanics are specified and tested with the adapter (SPEC-013, as ADR-006's follow-up asks; Bryan, 2026-10-02), off by default; this step is when to recommend switching it on.
9. **Part B**: a spec that moves the manifests into the skills and ships the mod (`devforgeai-claude-mods.md`, Part B).

## 12. Open questions for the owner

1. The character: the recommendation is now Ember as the default everywhere, with Clawd as a skin offered only in Claude Code, because the framework runs in other tools too. Do you agree?
2. Which phases should the Journey show: stop at Stories, or include QA and Ship as "coming"?
3. Should `devforgeai/progress/` be gitignored by default in users' projects? (The location is settled: operational files live in the project root's `devforgeai/` folder. SPEC-012 §13 asks the same question.)
4. Should skills print a marker when they start a step (`▶ Step 7`), so the current step is known rather than inferred? It would be a small change to each skill's Workflow text, and so a spec change.
5. Where should Part B's manifests live: in the progress component, as SPEC-012 puts them, or in each skill's `references/`?
6. How long may a run sit idle before the tracker evaluates it as ended? Decided by Bryan on 2026-10-02: no idle limit; a run ends when another tracked skill loads, on `/clear`, or at the session's end (SPEC-013 BEH-05).
7. Source lives in each plugin (settled 2026-10-02). Should the Codex port carry a byte-identical copy of `progress/`, kept equal by a test? (SPEC-012 §13 asks the same question.)
