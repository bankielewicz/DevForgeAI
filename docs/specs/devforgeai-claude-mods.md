# DevForgeAI and Claude Code mods

**Status:** proposal, not approved. Nothing here is built, and no spec, skill or plugin version changes because of it. Each item needs the owner's decision first (section 10).

**Date:** 2026-10-02. **Author:** claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9), at Bryan's request, reviewed with the advisor.

**Sources:**
- the mod API as Claude Code 2.1.287 describes it: its bundled `plugin-authoring` skill, that skill's `reference.md`, and the `claude-code.d.ts` declarations the engine generates for that build;
- the `/insights` report of 2026-10-02 (132 of 349 sessions analysed, 2026-09-10 to 2026-10-02);
- `CLAUDE.md`, `AGENTS.md`, `.claude/rules/` and `~/code/papercuts.md`;
- Anthropic's announcement, "Claude Code mods" (claude.com/blog/claude-code-mods), read after the first draft. It says mods ship inside plugins and are installed from the Claude directory or with `/plugin`; authors can submit them to the directory; mods are not sandboxed, so install them only from sources you trust; and on Team and Enterprise plans a built-in `sec-default` mod loads first.

The mod API is early access and changes between releases. Every API claim below was read in the 2.1.287 declarations, except those section 7 lists as unverified. Recheck them against the build you build on: a loaded mod gets that build's declarations in its `.claude-plugin/types/` folder.

## Contents

1. Purpose
2. Mods in brief
3. Design rules
4. UI building blocks and mockup conventions
5. Part A: mods for developing and dogfooding DevForgeAI
6. Part B: mods shipped with the framework
7. Verified and unverified
8. Placement, loading and tests
9. Suggested order
10. Open questions for the owner

## 1. Purpose

Most of DevForgeAI's rules live in text: specs, skills, `CLAUDE.md` and `.claude/rules/`. A Claude session follows them when it remembers to. The /insights report shows where it didn't:
- reviews drifted out of scope;
- documents were written before validation;
- a skill fix was committed outside `/plugin-dev:create-plugin`;
- pasted feedback was lost to `/compact`;
- pushes failed in the sandbox.

A mod is code that runs inside Claude Code and sees each tool call, prompt and drawing. So it can hold a session to a rule while the session works, and it can show the state of the work on screen.

This document proposes mods for two audiences:

| Part | Serves | Lives in | Needs |
| --- | --- | --- | --- |
| A (section 5) | the owner, and Claude sessions developing DevForgeAI in this repository | `src/tools/mods/<name>/`, outside the plugin, like `src/tools/session-archive/` | the owner's go-ahead |
| B (section 6) | anyone building a project with the `devforgeai` plugin | `src/claude/DevForgeAI/hooks/`, inside the plugin | a spec change, the create-plugin workflow, evals and the owner's approval |

**Superseded split.** The Part A / Part B split below (development mods outside the plugin, framework mods inside it) is superseded by the layered view of ADR-006 (accepted). There is one mod, and its rules come from the framework, then organization and project, then personal settings. DevForgeAI's own repository is a project whose project layer holds its own rules, such as the traps in A1. The individual mods below still describe what each feature does.

Mods don't replace the eval suites. A skill's evals stay the proof that it works (`CLAUDE.md`, "What this workspace is").

## 2. Mods in brief

A mod is a plugin folder with three parts:
- `.claude-plugin/plugin.json`;
- `hooks/hooks.json`, naming one module;
- that module (TypeScript or JavaScript), which exports `register(on, options)`.

Each `on(event, matcher?, hook)` call adds a hook of the shape `($, e, next)`:

- `e` is the event's input. `$` is the engine interface: UI, prompt, session, tools, files, processes, model, store and clock.
- `next(e)` runs the plugins beneath this one, then Claude Code's own behaviour, and resolves to the result. A hook can act before calling it, call it with a changed input, inspect the result afterwards, or answer without calling it.

```ts
on('tool.call', { tool: 'Bash' }, ($, e, next) =>
  /^\s*git add (-A|--all|\.)(\s|$)/.test(e.command)
    ? { deny: 'Stage files by path (CLAUDE.md, Traps).' }
    : next(e),
)
```

What a mod can do beyond a `settings.json` hook:

| Need | settings.json hook | Mod |
| --- | --- | --- |
| Refuse a tool call | yes (PreToolUse) | yes: `tool.call` answers `{ deny }` |
| Add a note the model reads after a tool's result | yes (PostToolUse context) | yes: the result's `context` list |
| Change a skill's prompt as it loads | no | `skill.prompt` |
| Add, replace or drop system-prompt sections | no | `prompt.compose` |
| Draw a band, pane, status entry or toast, or redraw a dialog | no | `ui.render`, `$.ui.*` |
| Put a draft in the prompt box, or a Tab suggestion | no | `$.prompt.fill`, `$.prompt.suggest` |
| Register a slash command answered in code | no | `$.command.register` |
| Keep state | files only | `$.state` (session), `$.store` (across sessions) |
| Test against the engine | no | `claude plugin test` |

The old hook events are still available inside a mod as `classic.<Event>`, for example `classic.PreCompact`. Where a settings hook is enough, use one: the `cd` block that /insights suggested needs no mod.

When a hook throws, Claude Code skips it and runs the rest of the chain, unless the hook's registration has a `.catch` that answers in its place. Two commands check a mod:
- `claude plugin validate <folder>` reports what the module hooks and calls, and what the engine would refuse;
- `claude plugin test <folder>` runs its `*.test.ts` files against the engine.

## 3. Design rules

Every mod proposed here follows these rules.

1. **Evals stay the proof.** A mod can make a session follow a rule, but it can't qualify a skill. No §9 record cites a mod.
2. **Wrap the existing scripts.** A check runs the repository's own script through `$.process.run`: `validate_brn.py`, `context_check.py`, `validate_policy.py`, `check_docs.py`, `qa_state.py`, `repo_state.py` or `scan_staged.py`. A shipped mod finds them under `$.plugin.root`. A rule with no script gets a new Python script, not TypeScript, so each rule has one copy and the Codex port can use it too.
3. **Guards fail closed.** Each guard registers a `.catch` that answers `{ deny }` with the error, so a crashed guard refuses instead of silently letting calls through. A path guard checks the `realPath` from `$.fs.stat(path, { resolve: true })` against a list of allowed paths. A list of forbidden spellings is best effort only.
4. **Observe or enforce.** Each guard has a `mode` setting: a `userConfig` picker over `observe` and `enforce`, shown in `/config`. In observe mode it logs each refusal it would have made and lets the call through; in enforce mode it refuses. Use observe while dogfooding: a guard that corrects a skill hides the defect the dogfood run should find, and each logged refusal is a finding for that skill. Use enforce for real work.
5. **Judgment calls stay the user's.** A mod enforces form, never content. It never sets a disposition, status, priority or approval. A button that starts the next step fills the prompt box (`$.prompt.fill`) or offers a Tab suggestion (`$.prompt.suggest`), and the person sends it. A mod never submits a prompt on its own (`CLAUDE.md`, "Judgment calls are the user's").
6. **Hand-offs stay as specified.** No mod recommends or starts `documents-updater`. Only the chain's last skill and `git` may recommend it (SPEC-006 §13, SPEC-007 BEH-19).
7. **Two channels.**
   - For the model: the refusal's text, or the result's `context`.
   - For the person: a status entry, toast, band or pane.

   `$.ui.notice` draws only under a permission dialog that is open. It never appears in auto mode or for an allowed tool, so nothing important goes there alone.
8. **Codex parity.** The Codex port can't run mods. Every rule a mod enforces stays written in the skill and its spec. A shipped mod's behaviour is a Claude-only difference, for Codex sessions to record in their import reports.
9. **Commands for the owner's shell.** A "Copy" button copies lines the owner can paste into a plain shell. Following `CLAUDE.md`, Traps: no leading `!`, no `\` continuations, each line under 100 characters, long flags in variables.

## 4. UI building blocks and mockup conventions

Where a mod can draw in 2.1.287:

| Site | API | Notes |
| --- | --- | --- |
| Status line entry | `$.ui.status(text)` | one line; `undefined` clears it |
| Toast | `$.ui.toast(text)` | disappears by itself |
| Band above the prompt | `ui.render` on `AbovePrompt` | the hook returns `next(e)` when there's nothing to show, so the band takes no rows |
| Pane | `$.ui.open({ id, title })`, drawn by `ui.render` on `Pane` | opened by a command or button, it shows at any width; opened unasked, it needs 144 columns and docks beside the transcript in the fullscreen layout |
| Command output row | `command.run` answers `{ text }`; `ui.render` on `CommandOutput` draws it | inline in the transcript; `text` is also what the model reads |
| Line under a permission dialog | `$.ui.notice(tool_use_id, text)` | only while that call's dialog is open |
| AskUserQuestion dialog | `ui.render` on `AskUserQuestion`, rewriting `questions` | a rewrite that doesn't fit the tool's schema is dropped, and the original is drawn |
| Prompt box | `$.prompt.fill`, `$.prompt.suggest` | a draft, or a dim Tab suggestion; the person sends it |
| Clipboard | `$.ui.copy({ text, surface })` | the terminal copies through the system clipboard tool and OSC 52 |

Elements available in the terminal include `Box`, `Text`, `Button`, `Input`, `Select`, `Link`, `Code`, `Markdown`, `Raster` and `Image`. The desktop app has `Svg` instead of `Raster` and `Image`. Limits that shape the mockups:

- `Link` opens only `https:` URLs (and `http://localhost`), such as GitHub PRs and issues. A local file opens through a `file:` link inside a `Markdown` element.
- A `Markdown` element holds at most 10,000 characters, and `$.fs.read` reads at most 4 MiB. So a pane over eval results reads one run's files at a time and pages long lists.
- A Button draws as `[ label ]`, or as `1: label` when it's `plain` with a hotkey. `variant: 'primary'` draws the main action in the accent colour.

Conventions in the mockups:

| Mockup | Means |
| --- | --- |
| `[ Label ]` | Button |
| `[ Label ]*` | the primary Button |
| `1: Label` | plain Button with hotkey 1 |
| `PR #57 ↗` | `Link` to an `https:` URL |
| `‹PRD-001›` | `file:` link in a `Markdown` element |
| `epic ▾` | `Select` |
| `╭─ name ─╮` | the frame of a pane or band |

The mockups show the terminal; the desktop app draws the same tree with its own controls. Values in the mockups are made up unless the text says otherwise.

## 5. Part A: mods for developing and dogfooding DevForgeAI

| ID | Mod | Friction it answers (source) | Main hooks |
| --- | --- | --- | --- |
| A1 | dev-guard | `CLAUDE.md` traps, ADR-005 D7, failed pushes (papercuts.md) | `tool.call` |
| A2 | spec-preflight | ARCH-001 amendments written, then rolled back; an architecture run with PRD-001 missing (/insights) | `tool.call`, `$.process.run` |
| A3 | skill-gate | skill fix 444a38c committed outside create-plugin (/insights) | `skill.prompt`, `tool.call` |
| A4 | review-scope | review sessions drifting out of scope, and messaging other sessions directly (/insights) | `command.run`, `prompt.compose`, `tool.call`, `AbovePrompt` |
| A5 | paste-keeper | pasted feedback lost to `/compact` (/insights) | `prompt.submit`, `session.append` |
| A6 | eval-board | eval results read by hand from folders; results bound to an older commit | `command.run`, `Pane`, `$.ui.copy` |
| A7 | deploy-drift | dogfooding a stale deployed copy (`CLAUDE.md`, "Source and deployed copy") | `session.start`, `skill.prompt`, status line |
| A8 | question-summary | a summary written just before AskUserQuestion goes unseen (the owner's standing instruction) | `ui.render` on `AskUserQuestion` |

### A1. dev-guard

**Friction.** Claude keeps several `CLAUDE.md` rules only by remembering them, and papercuts.md records what it cost when it didn't:
- a compound `git commit … && git push` ran sandboxed and hit the dead proxy (2026-09-28);
- a push passed with `allowed_domains` did the same;
- `gh pr create --head` failed (/insights).

**Behaviour.** A `tool.call` hook on Bash, Write and Edit checks each call against the table below. In enforce mode it refuses with the reason and where the rule comes from. In observe mode it logs the refusal it would have made and lets the call run.

| Call | Rule | Source |
| --- | --- | --- |
| Bash: `git add -A`, `--all` or `.` | stage files by path, or the sandbox's character devices get staged | `CLAUDE.md`, Traps |
| Bash: `git stash`, `git reset --hard`, `git clean`, `git checkout -- <path>`, `git restore <path>` (not `--staged`) | never change the working tree to investigate a failing test | ADR-005 D7 |
| Bash: a command that contains `git push` or `gh pr` but doesn't start with it | only a command that starts with them runs outside the sandbox | `CLAUDE.md`, Traps; papercuts.md, 2026-09-28 |
| Bash: `git push` or `gh pr` with `allowed_domains` | it runs sandboxed through the proxy, which is often down | `CLAUDE.md`, Traps |
| Bash: `gh pr create --head` | `gh pr create` already uses the current branch | /insights |
| Write or Edit under `src/codex/` | the Codex port is built by Codex sessions | `CLAUDE.md` |
| Write or Edit under `.claude/skills/devforgeai/` | edit `src/claude/DevForgeAI/` only | `CLAUDE.md` |

After any Bash call that fails, the hook searches `~/code/papercuts.md` for an entry that matches the error, such as `port 3128` or `config.lock`. It adds the matching entry to the result's `context`, so the model reads the known fix with the error. This makes "check this file first when tooling fails" automatic.

ADR-005 D7 forbids its commands only while investigating a failing test; other work may need them. Run dev-guard in observe mode first, and check the `git` skill's commands in SPEC-007 before enforcing the D7 row.

**UI.** A refusal in the transcript (enforce mode):

```
● Bash(git commit --amend --no-edit && git push origin docs/claude-mods)
  ⎿  Refused by dev-guard: `git push` runs outside the sandbox only when the command
     starts with it. Commit first, then run `git push` as its own Bash call.
     (CLAUDE.md, Traps; papercuts.md 2026-09-28)
```

When a call fails, the person sees the error. The matching papercut goes into the result's `context`, which only the model reads:

```
● Bash(git push -u origin docs/claude-mods)
  ⎿  Error: Failed to connect to localhost port 3128: Couldn't connect to server

  model only, not drawn:
  papercuts.md 2026-09-28 · run `git push` as its own Bash call and never pass
  allowed_domains; if the classifier blocks a push, get the owner's go-ahead in
  the conversation, then retry once · DevForgeAI
```

Status line (observe mode):

```
dev-guard observe · 2 would refuse · /dev-guard
```

The `/dev-guard` command's output row:

```
> /dev-guard

  dev-guard · mode: observe (change it in /config) · this session
  ──────────────────────────────────────────────────────────────────────────────
  08:41  Bash  git stash                     would refuse   ADR-005 D7
  08:52  Bash  git add -A                    would refuse   CLAUDE.md, Traps
  09:03  Bash  gh pr create --head feat/x    would refuse   /insights
  ──────────────────────────────────────────────────────────────────────────────
  [ Copy as findings ]*   [ Fill prompt: log a papercut ]   [ Clear ]
```

"Copy as findings" copies a Markdown list for the skill's backlog. "Fill prompt: log a papercut" puts a request in the prompt box, so Claude writes the entry the way the owner's `CLAUDE.md` asks.

### A2. spec-preflight

**Friction.** Two ARCH-001 amendments replacing Auth0 were written in full, then rolled back. Validation failed on an inconsistency that was already there: ERR-05, from CMP-01's status. Another architecture run stopped late because PRD-001 was missing (/insights).

**What a script can check today.** Scripts already validate:
- BRN documents (`validate_brn.py`);
- context documents and ambiguity logs (`context_check.py check`);
- policy (`validate_policy.py`).

ERR-05 has no script. It comes from the architecture skill's own self-check (its `SKILL.md`, step 10), which the model runs. So the gate for PRD, ARCH, ADR and epic documents comes in two stages:

- **Now:** check that the inputs exist. Before the first write to a document, every `upstream` ID in its frontmatter must resolve to a file in its typed folder.
- **Later:** once the architecture self-check, or part of it, exists as a script, run it on the current documents before the first write. Extracting it is a SPEC-003 change, so it's the owner's call.

**Behaviour.** A `tool.call` hook on Write and Edit under `docs/specs/`:

1. On the session's first write to a document type, run that type's script on the current files, before the change. If they already fail, refuse with the script's output, and tell the model to report it and ask the user how to proceed. Nothing has been written, so nothing needs rolling back.
2. Check that the `upstream` IDs in the new content resolve. A small proposed helper, `spec_refs.py`, reads the frontmatter and prints JSON, so the mod doesn't parse YAML itself.
3. After the write, run the script again and add its output to the result's `context`.

B2 ships the same checks for users' projects.

**UI.** A refusal:

```
● Write(docs/specs/adr/ADR-006.md)
  ⎿  Refused by spec-preflight: ADR-006 cites PRD-001 in upstream, and there is no
     docs/specs/prd/PRD-001.md. Report this to the user and ask how to proceed;
     nothing has been written.
```

A band, shown while the current documents fail:

```
╭─ spec-preflight ─────────────────────────────────────────────────────────────╮
│ The context documents fail context_check.py before any change (1 error):     │
│   testing.md: an approved document holds a [NEEDS ADR marker (approval)      │
│ Writes under docs/specs/context/ are refused until it's fixed or waived.     │
│ [ Fill prompt: fix the existing error first ]*   [ Show full output ]        │
│ [ Allow writes this session ]   [ Dismiss ]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

"Allow writes this session" is the person's waiver; the mod never waives on its own. "Show full output" opens a pane with the script's output in a `Code` element.

### A3. skill-gate

**Friction.** A follow-up fix to the prd skill was committed as 444a38c without going through `/plugin-dev:create-plugin`. That breaks the owner's rule that every skill change goes through that workflow (/insights).

**Behaviour.**
- A `skill.prompt` hook records in `$.state` when the create-plugin skill loads in the session.
- Until it has loaded, a `tool.call` hook on Write and Edit refuses changes under `src/claude/DevForgeAI/skills/`, `src/claude/DevForgeAI/evals/` and `src/claude/DevForgeAI/.claude-plugin/`.
- Edits made through Bash (`sed -i`, redirections) are matched best effort only.

**UI.** The band appears after the first refusal and goes away once the skill has loaded:

```
╭─ skill-gate ─────────────────────────────────────────────────────────────────╮
│ Skill files are locked: /plugin-dev:create-plugin hasn't run this session.   │
│ [ Fill prompt: /plugin-dev:create-plugin ]*   [ Why? ]                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### A4. review-scope

**Friction.** This was the most frequent correction in /insights. Review sessions commented on skills other sessions owned, such as prd during an epic review, or a git eval during a documents-updater review. One session also messaged another session directly, instead of handing the owner a paste-ready block.

**Behaviour.**
- `/review-scope <skill>`, a registered command, records the skill in scope in `$.state`. Its paths come from the skill's spec (`components`) and its folders under `src/claude/DevForgeAI/skills/`, `evals/` and `src/tests/`.
- `prompt.compose` adds a system-prompt section that sets the rules:
  - this is a validation session for that one skill;
  - findings about other skills get one line for the owner and are not developed;
  - every claim is reproduced;
  - the advisor is consulted before the hand-off;
  - the hand-off is a self-contained, paste-ready block.
- `tool.call` refuses `SendMessage`, and refuses Write or Edit outside the session's scratchpad and `tmp/`.
- If the advisor's calls pass through `tool.call` (unverified, section 7), the band shows whether the advisor has been consulted since the last draft.

**UI.** The band:

```
╭─ review-scope ───────────────────────────────────────────────────────────────╮
│ VALIDATION session · in scope: epic (SKL-004, SPEC-004)                      │
│ Other sessions own: prd, architecture, git, context, documents-updater       │
│ Advisor since last draft: not yet                                            │
│ Scope: epic ▾   [ Fill prompt: draft the hand-off ]*   [ End review ]        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

"Draft the hand-off" fills the prompt box with: "Draft the paste-ready hand-off for the epic session: only reproduced epic findings, self-contained, after consulting the advisor."

A refusal:

```
● SendMessage(to: "worker2")
  ⎿  Refused by review-scope: a review session hands the owner a paste-ready
     block; it never messages another session.
```

### A5. paste-keeper

**Friction.** Twice a session ran out of context, and after `/compact` the owner had to paste the Codex feedback and the in-progress state again (/insights).

**Behaviour.**
- On `prompt.submit`, a pasted block over a size limit (2 KB, say) is saved to `tmp/session-notes/<session-id>/paste-<n>.md`, with a toast. `tmp/` is gitignored.
- After a compaction (a `session.append` row whose door is `compaction`), `$.session.append` adds two rows:
  - a row the model reads, listing the saved files with one line each;
  - a notice row the person sees.

**UI.** The toast:

```
✓ paste-keeper: saved a 6.2 KB paste → tmp/session-notes/a4f2ade8/paste-1.md
```

After a compaction, the notice row (plain text, as notice rows are):

```
✻ Conversation compacted
paste-keeper: 2 pastes from before the compaction are on disk, and the model was told:
  tmp/session-notes/a4f2ade8/paste-1.md   Codex feedback on SKL-002 · 6.2 KB
  tmp/session-notes/a4f2ade8/paste-2.md   hand-off draft · 2.9 KB
```

### A6. eval-board

**Friction.** Evals run in a plain terminal (`CLAUDE.md`, "Evaluating a skill"), and their results are read by opening folders under `tmp/eval-results/` by hand. A run is bound to a commit (`REVISION`) and a plugin digest (`PLUGIN-DIGEST`), and says nothing about later commits.

**Behaviour.** `/evals` opens a pane listing the runs under `tmp/eval-results/`, newest first. It reads each run folder's `STARTED`, `REVISION` and `aggregate-result.json`: `costUsd`, `partial`, `suite.threshold`, `aggregates.casesPassed` and `casesTotal`, and each case's arms and aggregates.
- A folder with `STARTED` and no `aggregate-result.json` shows as running; `$.clock.every` refreshes it.
- For the selected run, the pane shows each case's score with the plugin and without it, and the difference.
- It also shows whether anything under `src/` or `docs/` changed since the bound commit, using `git diff --quiet <REVISION> HEAD -- src docs`.

Three copy buttons follow `CLAUDE.md`'s "cheapest first": one case with one run, the whole suite with one run, then three runs against the baseline. Each copies the `CLAUDE.md` commands with the run's tag filled in. For example, the 3-run button copies:

```
P=src/claude/DevForgeAI; O=tmp/eval-results/$(date +%Y%m%dT%H%M%S)
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet"
bash src/tests/prd/record_revision.sh $O prd
claude plugin eval $P --tag prd $A --threshold 0.8 -j 4 --output-dir $O
```

**UI.**

```
╭─ Evals · tmp/eval-results ───────────────────────────── [ Refresh ] [ Close ] ─╮
│ RUN                                    CASES    COST     BOUND TO   SINCE      │
│ prd-v4-requal-20261001T170412          33/33    $41.06   0814763    changed    │
│ architecture-v6-20261001T093015        21/21    $38.70   d0ac040    no change  │
│ git-v3-quick-20261002T071144           running                                 │
│                                                                                │
│ prd-v4-requal-20261001T170412 · threshold 0.8 · 3 runs · with vs without       │
│   CASE                              WITH   WITHOUT    Δ      RUNS              │
│   writes-valid-prd                  1.00    0.41    +0.59    ███               │
│   warns-unconverged                 0.92    0.33    +0.59    ██▆               │
│   revisited-brainstorm-extends      1.00    0.50    +0.50    ███               │
│   1–3 of 33   [ Next page ]                                                    │
│ src/ or docs/ changed since 0814763: these results don't cover HEAD a79ad0d.   │
│ ‹report.html›   [ Copy 1-case run ]   [ Copy suite, 1 run ]   [ Copy 3-run ]*  │
╰────────────────────────────────────────────────────────────────────────────────╯
```

### A7. deploy-drift

**Friction.** `/devforgeai:<skill>` runs the deployed copy in `.claude/skills/devforgeai/`, and only the owner deploys. So a session that edits `src/` and then dogfoods the skill runs the old copy (`CLAUDE.md`, "Source and deployed copy").

**Behaviour.**
- At `session.start`, and after any turn that changed files under `src/claude/DevForgeAI/`, compare the two copies (`diff -rq`, excluding `__pycache__` and `results`) and their `plugin.json` versions.
- The status line shows the result.
- When a `devforgeai` skill loads (`skill.prompt`) while the copies differ, a band says so.

**UI.** The status line:

```
devforgeai src 0.10.1 · deployed 0.10.0 · 7 files differ
```

The band:

```
╭─ deploy-drift ───────────────────────────────────────────────────────────────╮
│ /devforgeai:git is running the deployed 0.10.0; src/ is 0.10.1 (7 differ).   │
│ [ Copy deploy command ]*   [ Show differing files ]   [ Dismiss ]            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

"Copy deploy command" copies `CLAUDE.md`'s deploy line for the owner's shell. The sandbox denies Claude's writes to `.claude/skills/`, so deploying stays the owner's step.

### A8. question-summary

**Friction.** While the AskUserQuestion dialog is open, the text Claude wrote just before it can't be seen, so a summary placed there goes unseen. The owner's standing instruction is to put the summary in the question or in an option's preview.

**Behaviour.** A `ui.render` hook on `AskUserQuestion` reads the turn's last assistant text with `$.session.messages()`. If that text is longer than a line, and a single-select question has options without a `preview`, the hook fills those previews with the text before the dialog is drawn. It changes only the drawing; the answer the model gets back is the same.

Previews exist only on single-select questions, and a rewrite that doesn't fit the tool's schema is silently dropped, so multi-select questions are left alone.

**UI.** The engine draws the dialog; the mod only fills `preview`:

```
 ☐ Scope

 Which skill does this review cover?

 ❯ 1. epic (Recommended)        │ Reproduced 4 of 5 findings in a scratch repo.
   2. prd                       │ Finding 3 is pre-existing (issue #41), not a
   3. Other                     │ regression. The advisor agreed with the triage
                                │ and asked for one more check on finding 5.
```

## 6. Part B: mods shipped with the framework

These would ship in the `devforgeai` plugin (`src/claude/DevForgeAI/hooks/`), for people building their own projects with it. A skill governs a session only while it runs. These mods also cover edits made outside a skill, and they show where the project stands in the chain.

Each one is a requirement change. It needs:
- a spec, or spec amendments;
- the create-plugin workflow;
- evals and `claude plugin test` tests;
- the owner's approval;
- a plugin version bump.

This repository's own specs follow the same rules, so B2 can run here in observe mode before it ships.

| ID | Mod | What it holds a session to | Main hooks |
| --- | --- | --- | --- |
| B1 | chain-navigator | where the project stands in the chain, and the next step | `AbovePrompt`, `Pane`, `$.prompt.fill`, `$.prompt.suggest` |
| B2 | document-guard | document paths and IDs, changes to approved documents, upstream links | `tool.call` |
| B3 | merge-gate | merging only with QA's verdict for the head commit and the `merge-approved` label | `tool.call`, `qa_state.py` |
| B4 | trace | requirements → components → epics → stories, with the gaps marked | `Pane` |

Not proposed:
- a reminder to run `documents-updater`. Only the chain's last skill and `git` may recommend it, and it never starts itself (SPEC-006 §13, SPEC-007 BEH-19).
- any mod that writes a disposition, status, priority or approval.

The chain order the mods follow is Brainstorm → PRD → Architecture Definition → Context → Epic → Story → Spec. ADR-004 D5 places the context step after Architecture Definition and before epics and stories.

### B1. chain-navigator

Expanded into its own design: `devforgeai-progress-ui.md`, whose views are now replaced by `devforgeai-dashboard.md` (2026-10-06). That design adds a Journey through the framework's phases and the running skill's steps, judged by evidence so skipped steps show, with pixel-art graphics and an animated mascot. It keeps this entry's `chain_state.py` helper, its `file:` links, and its rule that buttons fill the prompt box and never send it.

### B2. document-guard

**Behaviour.** A `tool.call` hook on Write and Edit under `docs/specs/`. It shares A2's preflight: the inputs exist, and the type's script passes before the first write.

Before the write, it works out the resulting file: a Write's content, or an Edit applied to the current text. It passes the old and new text to a proposed helper, `check_change.py`, which adds three checks:

- **Path and ID.** A document goes to `docs/specs/<type>/<ID>.md`, its `id` equals the file name, and a new file's ID isn't already in use (`CLAUDE.md`, "Rules a change must not break": skills allocate IDs and never take a file name from the user).
- **Approved documents.** A change to an `approved` document must:
  - bump `version`;
  - set a new `updated` date;
  - append two Change Log rows: the change, authored `claude-code (session <ID>)`, and the owner's approval;
  - leave every earlier row as it was.
- **Upstream links.** After a version bump, the documents whose `upstream` still cites the old version are listed in the result's `context` and in the B1 pane.

In observe mode, if a permission dialog is open for the call, the finding shows as a line under it.

**UI.** A refusal:

```
● Edit(docs/specs/spec/SPEC-011.md)
  ⎿  Refused by document-guard: SPEC-011 is approved. This edit changes §6 but
     keeps version 3 and `updated` 2026-10-01, and it rewrites Change Log row 4.
     Bump the version, set `updated`, append rows; never rewrite earlier rows.
```

The line under a permission dialog (observe mode, dialog open):

```
 Edit file  docs/specs/spec/SPEC-011.md
 ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
  (diff)
 document-guard (observe): approved document, version unchanged; would refuse
 Do you want to make this edit to SPEC-011.md?
 ❯ 1. Yes
   2. Yes, allow all edits during this session
   3. No
```

### B3. merge-gate

**Behaviour.** A `tool.call` hook on Bash calls that match `gh pr merge`:
1. It runs `gh pr view <n> --json labels,comments,headRefOid` and pipes the JSON to the `git` skill's `qa_state.py`.
2. `qa_state.py` reports the QA state (`pending`, `unverified`, `conflicting`, `stale`, `approved` or `failed`) and `merge_allowed`.
3. The hook refuses the merge unless `merge_allowed` is true.

So the rule holds even when someone merges without `/devforgeai:git` (SPEC-007; SPEC-008's stub fixes the verdict comment and the labels). The gate only refuses; it never approves. The owner's authorization stays a person's answer.

**UI.** A refusal:

```
● Bash(gh pr merge 57 --merge)
  ⎿  Refused by merge-gate: PR #57's head is 3f2c1aa; the latest QA verdict names
     a79ad0d (state: stale), and the merge-approved label is missing.
```

The band, where `PR #57 ↗` links to the PR on GitHub:

```
╭─ merge-gate ─────────────────────────────────────────────────────────────────╮
│ PR #57 ↗ · head 3f2c1aa · QA verdict for a79ad0d (stale) · label: none       │
│ [ Fill prompt: ask QA to review 3f2c1aa ]*   [ Dismiss ]                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### B4. trace

**Behaviour.** `/trace` opens a pane built from a proposed helper, `trace.py`. For each requirement in the PRD it shows:
- its release (current or later);
- the ARCH components that cover it;
- its readiness;
- the epics and stories that cite it.

Gaps are marked. A `Select` filters the list: all, gaps only, or the current release.

**UI.**

```
╭─ Trace · ‹PRD-001› v3 ──────────────────────────────────────────── [ Close ] ─╮
│ Show: gaps ▾                                                                  │
│ REQUIREMENT  RELEASE  COMPONENTS (ARCH-001)  READINESS         EPIC   STORY   │
│ FR-004       current  CMP-02 scheduler       ready             none   ← gap   │
│ FR-007       current  CMP-01, CMP-03         NEEDS ADR DEC-03  none           │
│ NFR-002      current  none                   not covered       none   ← gap   │
│ 3 of 21 shown   [ Fill prompt: /devforgeai:epic ]*                            │
╰───────────────────────────────────────────────────────────────────────────────╯
```

## 7. Verified and unverified

**Corrections from the mods docs** (read on 2026-10-02 against SPEC-013 v2; the saved copy is in `docs/research/Claude/mods/`):
- `Button` has no `variant` prop, and an element given a prop it doesn't take makes Claude Code draw its own site instead, so the `[ Label ]*` convention in the mockups can't be drawn as written.
- A tool call's result has no documented `context` list. A mod reaches the model through a refusal's text, a prompt's `context` (`prompt.submit`), a command's output, or a skill's or the system prompt's text.
- `$.ui.notice` is listed but not described, and a mod can't change what the permission prompt shows.
- Commands are bare names: `/changes`, not `/devforgeai:changes`.
- `$.store` is one store per plugin, shared by every session on the machine, 4 MiB in all; `$.state` empties on `/clear`, `/resume` and `/branch`.
- A `userConfig` picker in `/config` isn't documented; an option that fails validation stops the module loading.
- Mods draw only on the terminal and desktop surfaces; VS Code's chat panel runs hooks and draws nothing.
- Mods run outside Claude's sandbox: the probe's mod wrote under `.claude/skills/`, and the docs say a mod's processes run outside it (SPEC-013 §9, P2).

**Verified.** These were read in the 2.1.287 declarations or `reference.md`:
- **Events:** `tool.call` (refusing, rewriting, a result's `context`), `prompt.submit`, `prompt.compose`, `skill.prompt`, `session.append` (with its `compaction` door), `session.start`, the `classic.*` events, and `ui.render` on `AbovePrompt`, `Pane`, `CommandOutput` and `AskUserQuestion`.
- **UI:** `$.ui.status`, `toast`, `open`, `notice` and `copy`; `$.prompt.fill` and `suggest`.
- **Other `$` calls:** `$.process.run`; `$.fs` (`read` at most 4 MiB, `write`, `list`, `stat` with `realPath`); `$.state`, `$.store`, `$.command.register` and `$.session.messages`.
- **Settings and errors:** `userConfig` pickers in `/config`; `.catch` answering for a failed hook.
- **Elements:** each surface's element table, `Link`'s `https:`-only rule, and `Markdown`'s 10,000-character limit.
- **Checks:** `claude plugin validate` and `claude plugin test`.

**Unverified.** Each has a check:

| Question | Why it matters | Check |
| --- | --- | --- |
| Do mods load in `claude plugin eval`'s child runs? | A mod shipped in the plugin would act only in the with-plugin arm, and could hide a skill that drifted from its text. A mod from `CLAUDE_CODE_PLUGIN_DIRS` might act in both arms. | the probe below |
| What can an unsandboxed mod's `$.fs` and `$.process.run` reach? The announcement says mods are not sandboxed, but not whether the session's sandbox settings apply to these calls. | A mod may write where Bash can't (`.claude/skills/`), so review each mod as unsandboxed code. B3 needs `gh` to reach GitHub. | in a scratch repo, a probe mod writes under `.claude/skills/` and runs `gh auth status` |
| Is `$.store` consistent across parallel sessions? | coordination between the cmux sessions | two sessions write the same key |
| Does the advisor's call pass through `tool.call`? | A4's "advisor since last draft" line | a logging hook on `tool.call` with no matcher |
| How does a pasted block reach `prompt.submit`? | A5 | log `e` for one paste |
| How does `skill.prompt` spell a plugin skill's name? | the matchers in A3 and A7 | log `e.skill` when `/plugin-dev:create-plugin` loads |
| Are a plugin's registered commands namespaced (`/devforgeai:chain` or `/chain`)? | command names in B1 and B4 | `claude plugin validate`, or `command.list` |
| How does the terminal draw a `Select`? | the mockups | a test that mounts one |

**The eval probe.**
1. Copy the plugin to `tmp/mod-probe/DevForgeAI/`. Add a hooks module whose `session.start` writes a `MOD-PROBE` file, containing the session ID, into the working directory.
2. Run one case without the baseline, keeping the scaffold folders:

   ```
   P=tmp/mod-probe/DevForgeAI; O=tmp/eval-results/mod-probe-$(date +%Y%m%dT%H%M%S)
   A="--allow-tools Write Edit Bash --scaffold --keep-temp"
   claude plugin eval $P --case writes-valid-brn --runs 1 --ablation none $A --output-dir $O
   ```

3. Look for `MOD-PROBE` in the kept scaffold folders. If it's there, mods shipped in a plugin run during its evals.
4. Repeat with the probe in a separate folder named in `CLAUDE_CODE_PLUGIN_DIRS`, exported in the shell rather than set in settings, and with the baseline arm on (`--ablation with-without`). This shows whether a personal mod reaches either arm.

## 8. Placement, loading and tests

**Part A.**
- Keep the source in `src/tools/mods/<name>/`:
  - `.claude-plugin/plugin.json`;
  - `hooks/hooks.json`;
  - `hooks/register.ts`, or `.tsx` when the mod draws;
  - `types/index.d.ts` when it keeps `$.state`;
  - its `*.test.ts` files.

  It stays outside the plugin and is never deployed with it, like `src/tools/session-archive/`.
- Load it from source for a session: `claude --plugin-dir src/tools/mods/dev-guard`, repeating the flag for each mod. An interactive session watches the folder, so a saved change reloads without a restart, and there's no deployed copy to drift.
- At each load, the engine writes generated types into `<mod>/.claude-plugin/types/`. Add `src/tools/mods/*/.claude-plugin/types/` to `.gitignore`.
- Don't use `.claude/skills/<name>/`. Only `.claude/skills/devforgeai/` is gitignored, the sandbox denies Claude's writes there, and it would add a deploy step.
- Don't put mods in `CLAUDE_CODE_PLUGIN_DIRS` in `~/.claude/settings.json` until the eval probe shows whether eval child runs inherit it.
- To try an idea, a Claude session can write a mod into that session's own mods folder (the `plugin-authoring` skill's route). It loads once the person turns on hot reloading for that session. A mod worth keeping moves to `src/tools/mods/`.

**Part B.**
- The plugin gets `src/claude/DevForgeAI/hooks/hooks.json`, naming one module that may import the plugin's other files.
- The helper scripts (`chain_state.py`, `check_change.py`, `spec_refs.py`, `trace.py`) run from `$.plugin.root`. Their location in the plugin is for the spec to decide.
- It deploys with the plugin through the existing `rsync` line, and is tested with `claude plugin test src/claude/DevForgeAI`. Evaluating it with `claude plugin eval` depends on what the probe shows.
- Mods reach users inside plugins. So once the plugin carries a hooks module, anyone who installs `devforgeai` gets its mods, whether from the Claude directory (if the plugin is submitted there) or with `/plugin`.

**Tests.** Every mod has `*.test.ts` files that `claude plugin test <folder>` runs. They cover:
- its refusals in both modes;
- its `.catch` failing closed;
- for a mod that draws, each tree on both `terminal` and `desktop`, using the test kit's `mount`.

Before a commit, run `claude plugin validate <folder>`, and `tsc -p <folder>` once the mod has loaded. When the mods are built, these commands join the Commands section of `CLAUDE.md`.

## 9. Suggested order

1. Run the eval probe (section 7). It decides how Part A is loaded and how Part B is evaluated.
2. Build A1 dev-guard and A2 spec-preflight in observe mode, with A7 deploy-drift. Review a week of observe-mode findings before switching any guard to enforce.
3. Build A4 review-scope, A6 eval-board, A8 question-summary and A5 paste-keeper.
4. Write a spec for Part B:
   - B1 chain-navigator first. It only reads and draws, so it's the least risky for users.
   - Then B2 document-guard and B3 merge-gate, which refuse calls.
   - Then B4 trace.
5. Separately, the owner may decide to turn the architecture self-check behind ERR-05 into a script (SPEC-003). A2 and B2 would then check ARCH and ADR documents before the first write.

## 10. Open questions for the owner

1. Should this proposal stay here, or become a typed spec under `docs/specs/spec/` when Part B is taken up?
2. Should any guard start in enforce mode rather than observe?
3. Where should observe-mode findings go: a file per session under `tmp/`, or each skill's backlog?
4. Should Part B wait until the mod API leaves early access?
5. Should the architecture self-check behind ERR-05 become a script, so A2 and B2 can run it before a write?
6. Which of the `git` skill's own commands must dev-guard allow under ADR-005 D7?
