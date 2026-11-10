# The test-first agents' live run (SPEC-020 VER-02)

One full run of `tdd-test-writer`, `tdd-implementer` and `tdd-verifier` on a scratch repository, before the agents
are released. VER-02 gates the first release (Bryan, 2026-11-09); VER-03's failure paths don't, and aren't in this
runbook. Results go in SPEC-020 §9.

Run it from a plain terminal, not inside a Claude session that is working on DevForgeAI.

The session runs inside Claude Code's command sandbox, in the scratch repository, so `git status` there lists the
sandbox's placeholders (untracked character devices such as `.bashrc`). The first run, on version 2, stopped on
them (SPEC-020 §9); from version 3 the agents don't count them (BEH-13), and this run is that rule's first test.

## 1. Set up

From the repository root, on the commit under test. `S` must be a new folder outside every project.

```bash
S=$HOME/tmp/tdd-ver-02-$(date +%Y%m%dT%H%M%S)
C=$S/plugin
bash src/tests/tdd-agents/make_scratch.sh $S
X=(--exclude=__pycache__ --exclude=results --exclude='*.test.ts' --exclude='*.test.tsx')
rsync -a "${X[@]}" src/claude/DevForgeAI/ $C/
git rev-parse HEAD
cd $S/repo && claude --plugin-dir $C
```

The script prints the worktree, the base commit and the input document's path. `git rev-parse HEAD` is the commit
under test: record it.

If the session lists `devforgeai:tdd-test-writer` from another copy of the plugin (the user-scope marketplace
install takes the name: CLAUDE.md, "Traps"), say so in the record: the agents then ran from that copy, and the run
doesn't count.

## 2. The prompt

Paste this as the session's first message, with the three values the script printed:

```text
Carry out one test-first change with the devforgeai plugin's three agents. Follow these rules exactly.

Input document: <input document>
Worktree: <worktree>
Base commit: <base commit>

1. Run the agents in this order: devforgeai:tdd-test-writer, devforgeai:tdd-implementer, devforgeai:tdd-verifier.
   Start each as a new agent, with only the task-message lines its description names, and wait for its reply.
   Pass no model. Never pass one agent's reply to another, and never continue a finished agent.
2. The red commit is the test-writer's HEAD: line. The green commit is the implementer's GREEN: line. The final
   commit is the implementer's HEAD: line.
3. After each agent returns and before starting the next, decide yourself whether the worktree's status is empty,
   and run `git -C <worktree> diff --name-only <previous commit> HEAD`, each as its own command, and compare the
   paths with the input document's allowed set for that step. The status is decided this way: run
   `git -C <worktree> status --porcelain --untracked-files=all`; if it prints nothing it is empty; if any line
   doesn't start with `??` it is not; otherwise run `cd <worktree> && stat -c '%F %t,%T %n' <every path listed>`,
   and it is empty only when every line printed starts with `character special file 1,3` (the command sandbox's
   placeholders). A status that isn't empty stops the run: show me the replies.
4. If an agent's STOPPED line isn't `no`, or its reply is a single line, or the verifier's VERDICT isn't PASS, stop
   and show me every reply. Do not run anything again.
5. At the end, show me every reply exactly as returned, not a summary, then the output of
   `git -C <worktree> log --oneline`, `git -C <worktree> status --porcelain --untracked-files=all` and
   `git -C <worktree> worktree list`.
6. Never push.
```

While each agent runs, open `/tasks` and note the model and effort its row shows. Note every permission prompt and
the command it was for.

## 3. Pass conditions

All of (a) to (d):

| | Condition |
|---|---|
| (a) | The three agents ran in order, each from a new context, and each reply has exactly its headings, with nothing before the first or after the last |
| (b) | The red commit changes only `tests/test_slug.py`, and at it `test_folds_accented_letters` fails and `test_spaces_become_hyphens` passes |
| (c) | The green commit changes no test file; the refactor step made a separate commit, or changed nothing |
| (d) | The verifier's VERDICT is `PASS`, with the fixed CHECKS lines (`start`, `commits`, `red`, `command 1`, `paths`, `end`) and one per point of each criterion; the red result was reproduced in a disposable worktree (`git worktree add --detach` in its COMMANDS), once: criterion 1's lines cite the same command as the `red` lines, and criterion 2's the same as `command 1`; afterwards the status is empty by the prompt's rule (the sandbox's placeholders not counted), HEAD is the final commit, and `git worktree list` shows only the repository |

## 4. Record, pass or not

- The commit under test, the Claude Code version (`claude --version`) and the date.
- Each agent's model and effort from `/tasks` (SPEC-020 §13 item 3).
- Whether a command starting with `cd <folder> && ` raised a permission prompt in an agent, and how many prompts
  there were in all; or "not applicable in auto mode" when the session ran in auto mode.
- Whether the sandbox let the verifier's `git worktree add` write to the disposable folder outside the
  repository. If it refused: the error, and the `NOT RUN` lines the verifier gave. Bryan then decides where
  disposable folders should live.
- Whether each reply's status came with a `placeholders: <number>, not counted` line, and the number.
- Whether `tests/test_slug.py` at the red commit holds the `é` escape or the letter: in the scratch repository,
  `git show <red commit>:tests/test_slug.py | grep -c 'u00e9'` prints `1` for the escape.
- Whether there was a refactor commit.
- Every reply as returned.

Then remove the scratch folder yourself; nothing else refers to it.
