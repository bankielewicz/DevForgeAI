# Runbook: manual test of the brainstorm skill

Tests the `devforgeai` plugin's `brainstorm` skill (SKL-001, SPEC-001) interactively, in a cmux tab.
The automated eval suite (`src/claude/DevForgeAI/evals/brainstorm/`) covers the
non-interactive paths; section 4 says how to run it and how to add cases with
`claude plugin eval init`. Sections 0–3 cover what needs a person answering: user confirmation,
the extend flow, framework selection (VER-05), and stopping mid-session (VER-09).

Record each result in the table at the end: **pass**, **fail** (with what happened), or
**not run** (with why).

## 0. Setup (once)

Run in a plain shell in the test tab (not inside Claude):

```bash
PROJECT=~/Projects/DevForgeAI
PLUGIN=$PROJECT/src/claude/DevForgeAI
TEST=/tmp/brainstorm-test           # outside the project: no parent CLAUDE.md, AGENTS.md or .claude/skills

rm -rf "$TEST" && mkdir -p "$TEST/ws"
cp -r "$PLUGIN" "$TEST/plugin"      # a copy, so T5-T6 can add and remove a framework safely
cd "$TEST/ws"
```

- `ws/` is an empty project. The skill writes to `ws/docs/specs/brainstorm/`. It sits outside
  `~/Projects/DevForgeAI` on purpose: inside it, the test session would also load the project's
  `CLAUDE.md` and `AGENTS.md` (which spell out the skill's rules) and the deployed
  `.claude/skills/devforgeai`, which may be older than `src/`.
- `plugin/` is a copy of the plugin source. The real source under `src/` is never edited.

Start Claude with the copied plugin loaded:

```bash
claude --plugin-dir "$TEST/plugin"
```

Answer yes if Claude asks whether you trust the folder.

**Check:** type `/devforgeai:` and confirm `brainstorm` appears in the completion list, once.
If it does not, stop: the plugin did not load.

To restart between tests: `/exit`, then run the same `claude --plugin-dir …` line again from `ws/`.

Your user-level `~/.claude/CLAUDE.md` and settings still load in the test session. If they tell
Claude to log problems somewhere (such as a papercuts file), the deliberate failures in T5–T6 can
end up there; remove those entries afterwards.

## 1. Tests

### T1. Natural trigger, interactive happy path (BEH-01, 03, 05, 06, 07, 08, 09, 10)

Say (no slash command):

> Let's brainstorm ways to reduce appointment no-shows at our dental clinic.

Answer its clarifying questions briefly. When it shows proposed dispositions:
- confirm all but one;
- change one (for example, "park IDEA-02 instead, we have no budget");
- say the brainstorm is done.

**Expect:**
- The skill loads (a Skill call to `devforgeai:brainstorm`), and it asks at most 3 clarifying questions.
- It names the framework (`diverge-converge`) and why.
- It writes `docs/specs/brainstorm/BRN-001.md` and says that it created the directory.
- In the file:
  - the confirmed dispositions and reasons, and your change, are recorded exactly;
  - `status: converged`;
  - `generated_by` is filled;
  - `reviewed_by: []`;
  - the Change Log row's author is `claude-code (session <ID>)`, with the same ID as
    `generated_by.session`;
  - every `hash` is `null`;
  - no `<!--` or placeholders remain.
- It runs `scripts/validate_brn.py` on the file and gets `OK`. You can also run it yourself:
  `python3 "$TEST/plugin/skills/brainstorm/scripts/validate_brn.py" docs/specs/brainstorm/BRN-001.md`.
- The final reply starts with the report block (path, framework, counts, promoted ideas, open
  questions), then any discussion, and ends with a paragraph outside any code block that starts
  with "Next step": run `/devforgeai:prd BRN-001` (the ID, never a path), with the BRN at
  `docs/specs/brainstorm/BRN-001.md` as its input. Nothing follows that paragraph. It writes no PRD.

### T2. Convergence not confirmed (BEH-06)

`/exit`, restart, then:

> /devforgeai:brainstorm onboarding new volunteers at a food bank

Confirm the dispositions, but when asked whether it is done, say "not yet".

**Expect:**
- A new file, `BRN-002.md`, not a change to BRN-001.
- The confirmed dispositions are recorded, and `status: draft`.

### T3. Extend an existing BRN (ERR-01, BEH-11)

Restart, then:

> /devforgeai:brainstorm dental appointment no-shows

**Expect:** it shows BRN-001 and asks whether to extend it or create a new BRN, and writes
nothing yet. Answer "extend", and add one new idea of your own in your words.

**Expect after writing:**
- BRN-001 now has `version: 2` and `updated` set to today.
- There is a new Change Log row naming this session, `claude-code (session <ID>)`, and
  `generated_by.session` is that same ID. The version 1 row, with its session, is unchanged.
- Every existing ID and its text is unchanged.
- The new idea is the next free `IDEA-NN`, in your wording.
- Nothing was renumbered or deleted.

### T4. No topic (BEH-01, VER-07 by hand)

Restart, then `/devforgeai:brainstorm` with no argument.

**Expect:** it asks what topic to brainstorm, and no new file appears. Then answer `/exit`.

### T5. New framework is selected, SKILL.md unchanged (VER-05, part 1)

In a plain shell (not in Claude), add a test framework to the **copy**:

```bash
cd "$TEST/plugin/skills/brainstorm/references/frameworks"
cat > reverse-brainstorm.md <<'FW'
# Reverse brainstorm

## When to use / When not to use

**Use when** the user wants to find how something could fail or get worse, then turn those
failures into ideas. **Avoid when** nothing exists yet to break and the options are wide open.

## Steps

1. Ask how the situation could be made worse, from the affected user's side. List the ways.
2. Keep the worsenings that already happen; each becomes a problem.
3. Invert each worsening into an idea that prevents it.
4. Rate each idea's value, effort and risk, then score it.

## Questions to ask

- "What would guarantee this fails for the user?"
- "Which of these failures already happen today?"

## Mapping to the BRN

- Worsenings that already happen fill `problems`.
- Inversions fill `ideas`, with `addresses` naming the problem inverted and `disposition: open`.
- Beliefs that a worsening is rare or common fill `assumptions`.
- `value`, `effort` and `risk` are the quoted strings "high", "medium" or "low";
  `score = 2 × value − effort − risk`, counting high = 3, medium = 2, low = 1.

## Evaluation method text

> Reverse brainstorm: we listed ways to make the problem worse, kept those already happening as
> problems, and inverted each into an idea. Ideas were rated high, medium or low for value,
> effort and risk and scored 2 × value − effort − risk.

## Example

"How could we make checkout abandonment worse?" gives "hide shipping costs until the last step".
That becomes the problem "Shoppers meet surprise shipping costs at the last step" and the idea
"Show the shipping cost on the cart page".
FW
sed -i '/^| diverge-converge |/a | reverse-brainstorm | [reverse-brainstorm.md](reverse-brainstorm.md) | The user wants to find ways a thing could fail, then invert them | Open-ended idea generation |' INDEX.md
sed -n '/^| framework/,/^$/p' INDEX.md          # expect the table with both rows
cmp "$PLUGIN/skills/brainstorm/SKILL.md" "$TEST/plugin/skills/brainstorm/SKILL.md" && echo "SKILL.md unchanged"
cd "$TEST/ws"
```

Restart Claude, then:

> /devforgeai:brainstorm use the reverse-brainstorm framework: why might customers abandon our checkout

**Expect:** it reads `INDEX.md`, says it chose `reverse-brainstorm` (named) and why, and
proceeds. Stop it after the framework message: say "stop here" and decline the draft save.

### T6. Missing framework file falls back (VER-05, part 2; ERR-04)

In a plain shell:

```bash
rm "$TEST/plugin/skills/brainstorm/references/frameworks/reverse-brainstorm.md"
```

Leave the index row in place. Restart Claude and repeat the T5 prompt. If the session offers to
record the missing file anywhere (a papercuts log, an issue), decline: it was removed on purpose.

**Expect:**
- It says `reverse-brainstorm.md` is missing, names the file, and falls back to `diverge-converge`.
- The session continues.

Stop it and decline the draft save.

### T7. Stop mid-session (ERR-02, VER-09)

Restart, then:

> /devforgeai:brainstorm reducing meeting overload for a 12-person engineering team

After it lists some ideas, say "let's stop here".

- **Expect:** it asks whether to save a draft. Answer **yes**. It writes the next `BRN-NNN.md`
  with every `disposition: open` and `status: draft`.
- Repeat on a new topic and answer **no**. **Expect:** no new file.

### T8. Validation failure after three attempts (ERR-05, VER-09)

Can't be reproduced reliably by hand: the skill fixes ordinary errors on its own. Record it as
**not run**, unless a real validation failure appears in another test. In that case check that
the file is left `status: draft` and the remaining errors are listed.

### T9. Static checks (VER-09, QR-01, QR-02)

In a plain shell:

```bash
wc -l "$PLUGIN/skills/brainstorm/SKILL.md"                     # expect < 500
python3 -c "import yaml,sys; t=open(sys.argv[1]).read().split('---')[1]; print(sorted(yaml.safe_load(t)))" \
  "$PLUGIN/skills/brainstorm/SKILL.md"                          # expect ['argument-hint', 'description', 'metadata', 'name']
python3 -m json.tool "$PLUGIN/.claude-plugin/plugin.json" >/dev/null && echo manifest ok
```

## 2. Cleanup

```bash
rm -rf /tmp/brainstorm-test
```

## 3. Results

| Test | Covers | Result | Notes |
|---|---|---|---|
| T1 | BEH-01, 03, 05–10 | | |
| T2 | BEH-06 | | |
| T3 | ERR-01, BEH-11 | | |
| T4 | BEH-01 (VER-07) | | |
| T5 | VER-05 part 1 | | |
| T6 | VER-05 part 2, ERR-04 | | |
| T7 | ERR-02 (VER-09) | | |
| T8 | ERR-05 (VER-09) | not run | not reproducible by hand |
| T9 | VER-09, QR-01, QR-02 | | |

## 4. Automated evals (`claude plugin eval`)

Reference: https://code.claude.com/docs/en/plugin-evals. Needs Claude Code v2.1.269 or later.
Every run and every `llm` grader is a real model call counted against your plan. The full
brainstorm suite (8 cases × 3 runs × 2 arms) is about $10 at list price.

Run evals from a plain terminal at the project root, not from inside a Claude session
(CLAUDE.md, SPEC-004 §2).

### 4.1 Run the existing suite

```bash
cd ~/Projects/DevForgeAI
claude plugin eval src/claude/DevForgeAI \
  --allow-tools Write Edit Bash --scaffold --threshold 0.8 \
  --judge-model sonnet --no-publish \
  --output-dir tmp/eval-results/$(date +%Y%m%dT%H%M%S)
```

What each option does:

- `--allow-tools Write Edit Bash`: the cases write a BRN and run `scripts/validate_brn.py`. A tool
  you don't grant is removed from the run, and the progress line shows it as `not granted`.
  Granting Bash runs every command under the OS sandbox; on Linux that needs `bubblewrap` and `socat`.
- `--scaffold`: runs `existing-brn/scaffold.sh`, which seeds BRN-001. Without it, VER-08 has nothing to find.
- `--threshold 0.8`: the framework bar. The default of 1.0 makes the command exit 1 on any
  imperfect case.
- `--judge-model sonnet`: in the first pilot, the default small judge failed a correct
  "What topic should we brainstorm?" reply, and it is noisy on 15k-character BRN files.
- `--output-dir`: by default, results go to `evals/results/` inside the plugin source, and from
  there into the deployed copy. Keep them under `tmp/`.
- First run in a directory: answer `y` to `Trust this plugin directory?`, or add `--trust-plugin`.

For a cheap check of one case, run a single arm once. It's noisy, so confirm any change with the
full command:

```bash
claude plugin eval src/claude/DevForgeAI --case writes-valid-brn --runs 1 --ablation none \
  --allow-tools Write Edit Bash --no-publish --output-dir tmp/eval-results/quick
```

Narrow a run with `--case <glob>` or `--tag ver-04`. Put the target before `--tag` and
`--allow-tools`.

### 4.2 Read the result

- The summary table has these columns:
  - `WITH`: the score with the plugin loaded.
  - `W/OUT`: the no-plugin baseline.
  - `Δ`: what the plugin added.
  - `NOTES`: the worst failing grader, or the run's error.

  `Δ 0` is correct for `ignores-unrelated-request` (VER-06) and `asks-for-topic` (VER-07).
- `report.html` in the output directory shows each run's grader verdicts, and for `llm` graders
  the judge's votes and the evidence it saw.
- `aggregate-result.json`: before trusting a low score, check `cases[].arms.with[].error`. A usage
  limit, rate limit or `401 OAuth access token has been revoked` (seen once in this suite) makes
  runs score 0 without being a regression. Also check that `suite.plugins` lists `devforgeai`.
- Graders marked `plugin-fired indicator` (`tool_used: Skill`) never count toward the score.
- Exit codes:
  - 0: every case met the threshold.
  - 1: a case fell below the threshold, a case file failed to load, or the directory isn't trusted.
  - 2: partial run (cost ceiling or credential rejected).
- To see what a run actually wrote, add `--keep-temp`. The run's workspace is sealed afterwards,
  but `out/trace.jsonl` keeps every Write call's content.

### 4.3 Add cases with `claude plugin eval init`

`init` opens an interactive Claude session that:

- reads the plugin and asks what a good and a bad result look like;
- proposes prompts that should and shouldn't trigger it;
- designs graders, pilots them once, and writes one case directory per prompt.

It never edits the plugin itself, only the eval directory. It needs a terminal, so it can't run in CI.

Use it for what the current suite doesn't measure: **trigger rate**. The skill-building guide's
target is loading on 90% of relevant requests, measured with 10–20 phrasings (paraphrases,
casual wording, and near-misses that must not trigger). Keep the new cases beside the existing
ones by pointing both commands at the same eval directory:

```bash
cd ~/Projects/DevForgeAI/src/claude/DevForgeAI
claude plugin eval init --eval-dir evals/brainstorm
```

In the interview, name the `brainstorm` skill and ask for trigger cases:

- 8 or more realistic "should trigger" phrasings that don't name the skill;
- 4 or more near-misses that share its vocabulary but need something else, like the PR-review case.

Tag each case `brainstorm` and `trigger`. After `init`, run just those cases:

```bash
claude plugin eval . --tag trigger --eval-dir evals/brainstorm --allow-tools Write Edit Bash \
  --threshold 0.8 --judge-model sonnet --no-publish --output-dir ../../../tmp/eval-results/trigger
```

With `--eval-dir evals/brainstorm`, results default to `evals/brainstorm/results/`. That's why
the command above sends them to `tmp/` instead.

For a blank case to fill in by hand, use `claude plugin eval init --bare <case-name>`. It writes
`prompt.md` and one grader and runs nothing. `prompt.md` accepts only these keys:

- `schema_version`, `name`, `description`, `tags`, `plugins`, `runs`, `expected_outcome`
- `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, `env`

The grader types are `regex`, `tool_used`, `tool_order`, `file_exists`, `llm` and `baseline`.
`file_exists` sees only files created during the run, so grade a seeded file's contents with
`target: {source: file, path: …}`.
