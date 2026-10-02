# Runbook: SPEC-013 probe (VER-01), as run on 2026-10-02

Records the runtime probe that SPEC-013's VER-01 asks for: how it was run, and the raw shapes Claude Code 2.1.287
delivered. SPEC-013 §9 summarises the answers; the adapter's parsing rules (DM-01's `answered`, `exit`, `reply`) are
written against the shapes below, so keep them here when the probe's own logs are gone.

## 1. How it was run

- **The probe:** a throwaway mod, `progress-probe` (`tmp/mod-probe/progress-probe/` while it lasts, gitignored): a
  hooks module that logs `session.start`, `prompt.compose`, `skill.prompt`, `tool.call`, `prompt.submit`,
  `turn.start`, `turn.complete`, `session.append` (door `response`) and `session.end` to
  `<root>/devforgeai-probe/log.jsonl`, with side files for skill texts and ticked replies, and a 30-second heartbeat
  in its own file. It refuses one Write on purpose (P13). `claude plugin validate` passed it.
- **The workspace:** `/tmp/devforgeai-probe-ws`, a fresh git repository outside this one, with the plugin's source
  (`src/claude/DevForgeAI/`) and the probe copied into `.claude/skills/devforgeai/` and `.claude/skills/progress-probe/`
  as skills-dir plugins.
- **The sessions** (Bryan's shell, then the cmux tab `devforgeai-worker1`):
  1. `claude --debug`: `/devforgeai:brainstorm a sticker for a team laptop` to the end (BRN-001 written and validated);
     three AskUserQuestion calls, one question each (all answered); one dismissed with Esc; one answered by typing;
     `exit 3` in Bash; a Write of `probe-deny-test.txt` (refused by the probe); `/clear`, `hi`, a one-minute wait.
  2. `claude -p "say hi" --debug` (`--debug` takes an optional filter, so it goes after the prompt).
  3. `claude`: one prompt that writes `- [x] 1. probe tick`, runs `echo hi`, then writes `- [x] 2. second tick`.

## 2. Raw shapes

**The rollout flag (session 1's first start, debug log):**

```
installed plugins' hooks modules not loaded: rollout flag (tengu_plugin_hooks_modules) is off, from GrowthBook (the disk cache of an earlier session); built-in plugins load regardless
hooks module progress-probe@skills-dir not loaded: hooks modules are turned off for installed plugins in this process: the rollout switch served off; built-in plugins load regardless
```

The same process refreshed `~/.claude.json`'s `cachedGrowthBookFeatures.tengu_plugin_hooks_modules` to `true`, and
every later process loaded the probe:

```
hooks module progress-probe@skills-dir loaded (worker, environment 1, tier user); events: session.start,prompt.compose,skill.prompt,tool.call,prompt.submit,turn.start,turn.complete,session.end
```

**P3, P4 (`skill.prompt`):** `e.skill` was `devforgeai:brainstorm`; `e.text` and the text `next(e)` resolved to were
identical (11,964 bytes), began `Base directory for this skill: /tmp/devforgeai-probe-ws/.claude/skills/devforgeai/skills/brainstorm`,
and had no frontmatter. `evaluate.py check --skill brainstorm` on that text printed
`matched sha256:e3ba73ab7f99076b9b2bd02d134049737380e82e16e0f76ceb314693f3aa3129`.

**P5 (AskUserQuestion's result, as `tool.call`'s `next(e)` resolved):**

Answered by picking an option:

```
isError: false   keys: ref, result, text, isReadOnly
result: {"questions":[{"question":"Does the team already have a name?", …}],
         "answers":{"Does the team already have a name?":"Yes"},"annotations":{}}
text:   "Your questions have been answered: \"Does the team already have a name?\"=\"Yes\". …"
```

Answered by typing: the same shape, with `"answers":{"…":"not sure"}` and a text beginning `The user answered:`.

Dismissed with Esc:

```
isError: true    keys: ref, result, text, isError
result: "Error: The user doesn't want to proceed with this tool use. The tool use was rejected …"
text:   "The user doesn't want to proceed with this tool use. …"
```

**P6 (Bash `exit 3`):**

```
isError: true    keys: ref, result, text, isError
result: "Error: Exit code 3"
text:   "Exit code 3"
```

**P7 (`turn.complete`):** the whole brainstorm was one turn; its `answer` held only the final summary (1,557
characters, no ticks). **P7b (`session.append`, door `response`, session 3):** one row per kept block, in order:

```
n10  blockTypes: ["text"]      text: "- [x] 1. probe tick"
n11  blockTypes: ["tool_use"]  (no text)
n14  blockTypes: ["text"]      text: "- [x] 2. second tick"
then turn.complete answer: "- [x] 2. second tick"
```

A row can also hold only a `thinking` block (session 2), so only `text` blocks are read. No row carried an `agentId`.

**P8 (`prompt.compose`):** interactive: `traits: ["lean","skills"]`, `surfaces: ["terminal"]`, after `prompt.submit`
and `turn.start` and before `skill.prompt`. Under `-p`: `traits: ["lean","print","skills"]`, `surfaces: []`, before
`prompt.submit`. An earlier plain `claude -p "say hi"`, run without `--debug`, logged nothing; the cause wasn't found.

**P11 (`/clear`):** `session.end` with `reason: "clear"`, then no `session.start`. The heartbeat went on under the same
module load, the session ID changed, and `$.state` read empty:

```
18:44:31Z  sessionId 43ed2e4b-…  boots 1  bootsVersion 1  marker "set by load c0bdad2b"
18:45:01Z  sessionId b14e8f36-…  bootsVersion 0            (boots and marker absent)
```

A background task's notification arrived at `prompt.submit` like a prompt (`<task-notification>…`), which is why
SPEC-013 v2 records a prompt only when its origin is the person's.

**P2:** the probe's `$.fs.write` to `.claude/skills/devforgeai/.probe-fs` and a `$.process.run` of
`sh -c 'touch .claude/skills/devforgeai/.probe-proc'` both succeeded (7 ms); `python3 --version` gave `Python 3.12.3`
in 3 ms; `python --version` rejected with `failed to start: ENOENT: Executable not found in $PATH: "python"`;
`evaluate.py check` through `$.process.run` took 38 ms.

**P10:** no `.claude-plugin/types/` appeared in either skills-dir copy. **P12:** see SPEC-013 §9 (a test answers
`fs.read` with `{ value }`). **P13:** the model's reply quoted the refusal: "The write was refused by a hook in this
session, with the message: 'progress-probe refused this write on purpose (SPEC-013 probe P13).'"

## 3. Running it again

Rebuild the workspace with the probe and the plugin's source, as in section 1, and repeat the sessions on a new
Claude Code build. Compare each shape above; a change in P5, P6, P7b or P8 changes DM-01 or BEH-01. Remove the
workspace afterwards (`rm -rf /tmp/devforgeai-probe-ws`).
