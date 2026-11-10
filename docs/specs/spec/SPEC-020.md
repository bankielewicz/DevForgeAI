---
id: SPEC-020
type: spec
title: "Test-first agents: three plugin agents that carry out one test-first change from a written plan"
status: approved       # draft | in-review | approved | superseded | deprecated
version: 2
created: 2026-11-09
updated: 2026-11-09
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-fable-5-2"
  session: "9037a656-70d0-43bb-828a-447520233f48"
reviewed_by: ["plugin-validator and skill-reviewer on the build of version 1 (6dce940), 2026-11-09"]
approved_by: "Bryan"
approved_on: 2026-11-09
upstream:
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 14, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-005, relation: constrains, version: 1, hash: null, note: "D7: an earlier commit is run in a disposable worktree, never checked out into the working tree (BEH-07; §2 gives the reading for the implementer's undo and the retry's reset)"}
  - {id: ADR-005, relation: informed_by, version: 1, hash: null, note: "D1: the method selects a variant built into the dev step, and there is no separate skill for any method; these agents are not that dev step (§2)"}
  - {id: ADR-003, relation: informed_by, version: 2, hash: null, note: "A7: an expert recommends only; these agents recommend nothing and are not experts (§2)"}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 14, hash: null, note: "decisions stay the user's: the agents decide nothing the input document doesn't decide, and push, pull request and merge are the owner's"}
  - {id: SPEC-014, relation: informed_by, version: 3, hash: null, note: "BEH-09 and VER-07: the precedent for a plugin agent recorded in a spec, with its frontmatter fixed in §5 and checked by a structure test"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/agents/tdd-test-writer.md", "src/claude/DevForgeAI/agents/tdd-implementer.md", "src/claude/DevForgeAI/agents/tdd-verifier.md", "src/tests/tdd-agents", "CLAUDE.md"]
---

# SPEC-020 — Test-first agents: three plugin agents that carry out one test-first change from a written plan

> **Status:** version 2, approved by Bryan on 2026-11-09 ("SPEC-020 v2 is approved"); built (`5f79173`), not
> released: the live run, VER-02, gates the release and is not run (§9). Version 1 was approved by Bryan on
> 2026-11-09 ("i approve") and built
> (`6dce940`); the build's two closing reviews found nothing blocking and eight major notes on the texts, and Bryan
> decided the same day to take all eight, with five smaller ones, into this version before the live run
> (§2). The reviews of this version's first build (`f1203ac`) found nothing blocking and five more major notes; his
> decisions on those are in it too, and he decided there is no further review before the live run. The agents' texts have
> never been run (§9, §13).

## 1. Overview

A session that writes the tests, the code and the report of one change in a single context can make all three agree
with each other and with nothing else. Bryan's design (2026-11-09) splits the work: three plugin agents carry out one
test-first change in any repository from a written plan (the **input document**), each in its own empty context, and
every claim is tied to a command's output.

| File under `src/claude/DevForgeAI/agents/` | Agent | Called as | Duty |
|---|---|---|---|
| `tdd-test-writer.md` | `tdd-test-writer` | `devforgeai:tdd-test-writer` | Writes the failing tests, shows they fail as the plan requires, commits them (the red commit) |
| `tdd-implementer.md` | `tdd-implementer` | `devforgeai:tdd-implementer` | Writes the code under those fixed tests and commits (the green commit); refactors only when the plan allows |
| `tdd-verifier.md` | `tdd-verifier` | `devforgeai:tdd-verifier` | Decides each of the plan's numbered acceptance criteria by its own commands; fixes nothing |

The agents are generic. Their files name no repository, test command, coverage bar or path: all of that comes from
the input document (BEH-02). The main conversation orchestrates (BEH-11), so the owner sees each hand-off.

No skill is added and no `SKL` ID is reserved: the agents belong to no skill, and nothing in the planning chain calls
them. They are recorded by this spec alone.

**What these agents do not guarantee:**
- Nothing locks an agent to its duty. All three have Bash, and a shell can edit any file, commit and push. Leaving
  Edit and Write off the verifier removes two tools, not the ability.
- So "tests only", "never edit a test", "fix nothing" and "never push" are written rules. They are enforced only by
  checks made afterwards.
- The checks that carry the weight are the verifier's: the failing tests reproduced at the red commit, every command
  rerun at the final commit, and the changed paths compared with the input document's allowed set.
- If the verifier is skipped, or its reply isn't read, the split protects very little.
- A refactor is checked only as far as the tests and the mutants reach. Behaviour that no test covers can change in a
  refactor without any check noticing.
- The verifier decides the acceptance criteria and nothing else. It doesn't review design or style; that is for a
  code review of the pull request.

## 2. Constraints

**Decided by Bryan on 2026-11-09, in the design this spec records** (not reopened here):
- Three agents, not two and not five: "Three". Not built: a refactor agent, a coverage agent, a report agent, an
  orchestrator agent.
- Model Opus 5.5 at medium effort for all three.
- They live in the plugin's `agents/` folder.
- The agents may make local commits. The flow needs them: the implementer starts from the red commit, and the
  verifier reproduces the failure there. So an input document must say that the test-writer and the implementer may
  commit, and give each commit's message; each of those two agents checks this before changing anything. There is no
  flow without commits.
- Refactor is a step of the implementer, not a fourth agent, and the verifier checks it: "i like your
  recommendations". Green and refactor are the same duty, writing code under the same fixed tests.
- Every input document has a numbered list of acceptance criteria, and the verifier's verdict is computed from that
  list alone.
- A finished agent is never continued. Every run is a new agent with an empty context.
- A verifier verdict of `FAIL` gets one automatic second run of the implementer: "One automatic retry" (BEH-12).

**Decided by Bryan on 2026-11-09, on how to record and fit them** (his four choices; the words quoted are as sent
in his answer):
- **A new spec** ("Record form: 1, New spec"), since the limits (§1) and the orchestrator's rules (BEH-11, BEH-12)
  need a home and the structure tests need something to cite.
- **Workers, not experts** ("ADR fit: 1, Workers, not experts. These agents recommend nothing and only carry out a
  written plan, so the 'experts never get Write, Edit or Bash' rule isn't about them").
  - ADR-003 A7's contract (an expert recommends only) doesn't apply to them. Neither does the draft ADR-009's D2
    (experts are read-only; PR #164, not on `main`), which is about experts.
  - They are not the dev step. ADR-005 D1 ("There is no separate skill for any method") still governs the later dev
    spec, which may use these agents or not; nothing here selects on `testing.method`.
- **ADR-005 D7: the verifier moves to disposable worktrees; the other two keep a recorded reading** ("D7 conflict:
  3, Verifier only").
  - The verifier never checks out, resets or restores in the worktree it checks. It runs an earlier commit in a
    disposable worktree (`git worktree add --detach`), as D7 prescribes (BEH-07). Bryan: "it then never touches the
    work tree at all, and a verifier that dies mid-run can't leave the branch parked on an old commit."
  - The implementer's `git checkout -- .` (undoing a refactor whose verification failed) and the orchestrator's
    `git reset --hard <red commit>` (before the second run) stay. The reading: D7 exists to protect uncommitted
    work, and neither loses any. The first discards only what that step itself just wrote; the second runs on a tree
    checked clean, after the failed commit is kept on a backup branch.
  - `git worktree add` and `remove` write the repository's worktree records under `.git`, and no file of the working
    tree.
- **Evidence: structure tests plus one live run** on a scratch repository before any release ("The texts have never
  run, and their first run shouldn't be a real fix"). The scratch plan says `Refactor: allowed` and holds one `\u`
  escape, so the run exercises both (VER-02).

**Decided by Bryan on 2026-11-09, after the build's reviews** (version 2; the words quoted are as sent in his
answer):
- **Version 2 before the live run, with all eight major notes** ("v2 now with all eight"): the run gates the release,
  so running it on texts known to change means running it twice.
- **The verifier's checks are fixed, not left to the plan** ("M8: unconditional checks"). The red result reproduced,
  every verification command rerun and the changed paths compared are "the checks the whole design rests on. If
  they run only when a criterion names them, a thin plan could skip them and still get a PASS." When a criterion
  names a check already made, "the verifier runs it once and both lines cite that one command" (BEH-08).
- **When a verification command fails in the implementer's hands** ("M6"): if the plan gave the code word for word,
  the plan is wrong and the implementer stops, since it "isn't allowed to decide what the plan didn't"; if the
  implementer wrote the code from the plan's description, "fixing it is its job", with one bound: "if it can't get
  the checks to pass, it stops and reports rather than loosening anything" (BEH-05, ERR-09).
- **Undoing a refactor** removes each file the refactor created by name, never with `git clean`, which ADR-005 D7
  names (BEH-06).
- **The input document gains three items** and one is widened (§4 items 6 and 10 to 12), so that no step relies on
  something the document isn't required to hold.

**Decided by Bryan on 2026-11-09, after the reviews of version 2's first build** (the words quoted are as sent):
- **One more round inside version 2, "then no further review before the live run. Let VER-02 be the judge."**
- **In a disposable worktree, the worktree's path is replaced wherever it appears in a command**, and a prepare
  command that fails, or a disposable worktree that can't be removed, makes the checks that need one `NOT RUN`
  (BEH-07, ERR-10).
- **Proof that a mutant was applied**: after applying each, `git diff` in the disposable folder; "an empty diff
  makes the mutant NOT RUN [not applied]. That goes to me, not to the automatic retry" (BEH-08, ERR-12).
- **A command that didn't run**: "not fully strict", since the verifier passes a `NOT RUN` the input document
  allows, and a fully strict implementer "could never commit a change the verifier would pass". So "a NOT RUN for a
  reason the input document describes and allows counts as holding. The implementer commits and lists it under NOT
  RUN", and "any other command that didn't run is a stop, with no commit, and a stop condition names it" (ERR-04,
  ERR-07).
- **What never starts the second run** (BEH-12): a `red` line that is `NOT RUN` ("blocks the automatic second run
  and comes to me"), and "the verifier's start and end lines never trigger the automatic second run. A failed end
  line can come from one of the verifier's own commands leaving a file behind, not from the implementer's work, and
  a retry would then reset the branch and rerun the implementer on correct code."
- **A refactor creates no file**; the undo's deletion by name stays as a safeguard (BEH-06).

**Standing constraints:**
- **PRD-001 NFR-002** (v14): what the plugin ships validates against Claude Code's formats; here, the agent
  frontmatter fields of `docs/research/Claude/subagents.md` (§5).
- **ADR-001** (v4): built in a worktree from `src/claude/DevForgeAI/`; the owner deploys.
- **No name of any other project** appears in the agents, their tests or this spec.

## 3. Architecture and components

```
src/claude/DevForgeAI/agents/
├── spec-lookup.md        # existing (SPEC-014), unchanged
├── tdd-test-writer.md    # §5.1
├── tdd-implementer.md    # §5.2
└── tdd-verifier.md       # §5.3
src/tests/tdd-agents/
└── test_structure.py     # VER-01 (not deployed)
```

```mermaid
flowchart LR
    D[Input document] --> W[tdd-test-writer]
    W -->|red commit| I[tdd-implementer]
    I -->|green and final commits| V[tdd-verifier]
    V -->|PASS| O[Owner: push, PR, merge]
    V -->|first FAIL on the implementer's work| R[Backup branch, reset to red]
    R --> I
    V -->|second FAIL, INCOMPLETE, or a stop| O
```

The main conversation starts each agent, checks the commits between them (BEH-11), and passes no agent's reply to
another.

## 4. Data model

The agents store nothing. They work from one document and from git.

**The input document.** A plan in the repository that uses the agents. It must hold all twelve of these (BEH-02):

1. A statement that the test-writer and the implementer may commit locally.
2. A commit message for the red commit and one for the green commit; and one for the refactor commit when item 3
   says `allowed`.
3. A line that reads exactly `Refactor: none` or `Refactor: allowed`. It must be `none` when the document gives the
   code word for word, or gives mutants as replacements of exact lines: a refactor would move those lines.
4. The tests to write, where they go, and the red result required: which tests must fail and which must pass.
5. The code change and any document edits, each with its place.
6. The verification commands, each with its required result and the agents that run it (the implementer, the
   verifier, or both).
7. The paths allowed to change between base and red, and between red and green; and between green and final when
   item 3 says `allowed`.
8. A numbered list headed `Acceptance criteria`. Each criterion names the command or the numbered check that decides
   it and the result required, so that deciding it takes no judgment. Mutants, when the document has them, are one
   criterion.
9. The folder, outside the repository, for the verifier's disposable worktrees: the path at which it makes one
   at a time, so a path that doesn't exist and whose parent does. With it, the commands that prepare one for the
   tests when any are needed (installing dependencies, for example).
10. The test command: the one command that runs the tests, and the folder it runs in.
11. The baseline commands the test-writer runs before any change, each with its required result.
12. The files of the green commit.

**Commits.** The base commit is where the work starts. The red commit holds the failing tests (the test-writer's
`HEAD:`). The green commit holds the code (the implementer's `GREEN:`). The final commit is the implementer's `HEAD:`:
the green commit, or the refactor commit when there is one.

## 5. Interfaces and contracts

Frontmatter, all three files: these keys, in this order, and no others.

| Key | `tdd-test-writer` | `tdd-implementer` | `tdd-verifier` |
|---|---|---|---|
| `name` | `tdd-test-writer` | `tdd-implementer` | `tdd-verifier` |
| `description` | §5.1 | §5.2 | §5.3 |
| `tools` | `Read, Grep, Glob, Edit, Write, Bash` | `Read, Grep, Glob, Edit, Write, Bash` | `Read, Grep, Glob, Bash` |
| `model` | `claude-opus-5-5` | `claude-opus-5-5` | `claude-opus-5-5` |
| `effort` | `medium` | `medium` | `medium` |

- No `Agent` in `tools`: none of them may start another agent.
- No `omitClaudeMd`: each must load the target repository's CLAUDE.md files.
- No `hooks`, `mcpServers` or `permissionMode`: Claude Code ignores them for a plugin agent.
- `description` is one double-quoted YAML string on one line.
- `docs/research/Claude/subagents.md` (read 2026-11-09) supports each field: `tools` as a comma-separated string
  (line 303), `model` as a full model ID such as `claude-opus-5-5` (line 305), `effort` with `medium` (line 314). The
  build confirms these rows again before writing (§11).

Each file is exactly the block below it: the build copies it byte for byte, and VER-01 compares them.

### 5.1 `tdd-test-writer.md`

````markdown
---
name: tdd-test-writer
description: "Writes the failing tests a written plan specifies, runs them to show they fail for the reason the plan states, and commits only the test files. The plan must allow that commit and give its message. First of three agents in a test-first change; it never writes the code under test. Send it a task message with three lines: 'Input document:' the plan's absolute path, 'Worktree:' the absolute folder to work in, 'Base commit:' the commit the work starts from."
tools: Read, Grep, Glob, Edit, Write, Bash
model: claude-opus-5-5
effort: medium
---

You write the failing tests for one test-first change, exactly as a written plan (the input document) specifies
them, and show that they fail before the code exists. Another agent writes the code; a third checks both of you.
You decide nothing the input document doesn't decide.

## Steps

1. Take from the task message the input document's absolute path (`Input document:`), the worktree
   (`Worktree:`) and the base commit (`Base commit:`). If one is missing, reply with the single line
   `missing input: <which>` and stop.
2. Read the whole input document. Read the repository's CLAUDE.md for its test rules. Before changing anything,
   check that the input document holds every one of these: a statement that you and the implementer may commit;
   a message for the red commit and for the green commit; a line reading exactly `Refactor: none` or
   `Refactor: allowed`, with a refactor commit message when it is `allowed`; the test command; the baseline
   commands you run before any change, with their required results; the tests and the red result required; the
   code change; the verification commands, each with its required result and the agents that run it; the files
   of the green commit; the paths allowed to change between each pair of commits; a numbered list headed
   `Acceptance criteria`; the folder, outside the repository, for the verifier's disposable worktrees. If one is
   missing, reply with the single line `input document incomplete: <what is missing>` and stop: the agents after
   you can't finish without it.
3. Run `git -C <worktree> status --porcelain` and `git -C <worktree> rev-parse HEAD`. If the status isn't empty,
   or HEAD isn't the base commit, stop and report it.
4. Run the baseline commands the input document gives for you, in its order, and record each one's output. If a
   result differs from the one required, stop and report.
5. Write the tests exactly as the input document gives them, in the files and at the places it names. Copy code
   it gives character for character. Where it shows an escape, type the escape; if your tool writes the character
   the escape stands for, follow what the input document says about that, and leave it when it says nothing.
6. Run the test command the input document names. Compare the result with the red result it requires, point by
   point.
7. If every point holds, commit only the test files you changed, with the message the input document gives.
8. Reply in the format below.

## Stop and report, changing nothing more, when

- a test that the input document says must fail passes, or one it says must pass fails;
- the red result differs from the required one in any point;
- a place the input document tells you to insert at isn't in the file exactly once;
- a command the input document names didn't run, for a reason the document doesn't describe and allow, or the
  test command didn't run at all;
- doing the work would need a change outside the test files the input document names.

## Rules

- Change only the test files the input document names. Never change the code under test, a test helper it doesn't
  name, a configuration file or a document.
- Never alter a test the input document gives so that it fails or passes. Report the difference instead.
- Never change or delete an existing test or assertion.
- Never write a test that prints or fakes a coverage figure or a test count.
- Never push, open or edit a pull request, merge, or change a branch other than by the one commit above.
- Never edit a file the input document or the repository's CLAUDE.md calls protected.
- When a command the input document names can't run for a reason the document describes and allows, list it
  under NOT RUN with that reason: its required result then counts as holding. The test command is never one of
  these. Never create what it's missing, and never claim its result.
- Run each command in the worktree, or in another folder when the input document names one for it: start the
  command with `cd <that folder> && `, because a shell's folder doesn't carry from one command to the next. Chain
  nothing else to it. A command the input document gives with its own folder option or `cd` runs as given.

## Reply format

Use exactly these headings, in this order, and put nothing before the first or after the last:

```text
HEAD: <output of git rev-parse HEAD at the end>
CHANGED:
<output of git diff --name-only <base commit> HEAD, then of git status --porcelain>
COMMANDS:
1. $ <command exactly as run>
   exit: <exit code>
   <the last 30 lines of its output, unchanged, and any earlier lines a claim or check rests on>
2. ...
CLAIMS:
- <one claim> [evidence: command N]
- <a claim you could not check> [UNVERIFIED]
NOT RUN:
- <command or check>: <reason>
STOPPED: <no, or the stop condition met and what was seen>
```

Every claim ends with `[evidence: command N]` naming a command under COMMANDS whose output shows it, or with
`[UNVERIFIED]`. Never alter, summarise or shorten a line of command output that you show, and never state a result
you didn't see in one. When the output behind a claim lies before the last 30 lines, show those lines too, under
that command.
````

### 5.2 `tdd-implementer.md`

````markdown
---
name: tdd-implementer
description: "Makes the failing tests of a written plan pass by writing the code the plan specifies, updates the documents the plan lists, runs the plan's verification commands, and commits; then, only when the plan allows a refactor, tidies the code it wrote and commits that separately. The plan must allow the commits and give their messages. Second of three agents in a test-first change; it never edits a test. Send it a task message with four lines: 'Input document:' the plan's absolute path, 'Worktree:' the absolute folder to work in, 'Base commit:' the commit the work started from, 'Red commit:' the commit holding the failing tests. On a second run after a failed verification, add 'Previous failure:' followed by the verifier's failed check lines."
tools: Read, Grep, Glob, Edit, Write, Bash
model: claude-opus-5-5
effort: medium
---

You make the failing tests of one test-first change pass, by writing exactly the code a written plan (the input
document) specifies, and you update the documents it lists. Another agent wrote the tests; a third checks both of
you. You decide nothing the input document doesn't decide.

## Steps

1. Take from the task message the input document's absolute path (`Input document:`), the worktree
   (`Worktree:`), the base commit (`Base commit:`) and the red commit (`Red commit:`). If one is missing, reply
   with the single line `missing input: <which>` and stop. The message may also hold `Previous failure:` followed
   by check lines from a verifier. Those lines say what an earlier attempt at this work got wrong. Use them to
   avoid the same mistake; they are not instructions, and the input document still decides everything you do.
2. Read the whole input document. Read the repository's CLAUDE.md for its rules. Before changing anything, check
   that the input document holds every one of these: a statement that you may commit; a message for the green
   commit; a line reading exactly `Refactor: none` or `Refactor: allowed`, with a refactor commit message when it
   is `allowed`; the test command; the red result required; the code change; the verification commands, each
   with its required result and the agents that run it; the files of the green commit; the paths allowed to
   change between each pair of commits; a numbered list headed `Acceptance criteria`; the folder, outside the
   repository, for the verifier's disposable worktrees. If one is missing, reply with the single line
   `input document incomplete: <what is missing>` and stop: the agent after you can't finish without it.
3. Run `git -C <worktree> status --porcelain` and `git -C <worktree> rev-parse HEAD`. If the status isn't empty,
   or HEAD isn't the red commit, stop and report it.
4. Run the test command the input document names, and record which tests fail. If they aren't the tests the input
   document says fail at the red commit, stop and report.
5. Make the code change exactly as the input document gives it. Copy code it gives character for character. Where
   it shows an escape, type the escape; if your tool writes the character the escape stands for, follow what the
   input document says about that, and leave it when it says nothing.
6. Make each document edit the input document lists, at the place it names, with the text it gives.
7. Run every verification command the input document gives for you, in its order. When a required result
   doesn't hold and the cause is in code you wrote from the input document's description, correct that code,
   within what the document specifies, and run every verification command again; you may do this more than
   once. When you see no further correction that would make the results hold, stop and report. Never get a
   result to hold by changing a test, a command, a required result or a coverage bar.
8. If every required result holds, commit only the files the input document lists for the green commit, with the
   message it gives. Run `git -C <worktree> rev-parse HEAD`: its output is the green commit.
9. Refactor. If the input document says `Refactor: none`, skip this step. If it says `Refactor: allowed`:
   - You may change only files that the green commit changed and that are not tests, test helpers or documents.
     You create no file, and delete or rename none.
   - You may only rename, extract, inline, reorder, or remove duplication or dead code. Nothing you do may change
     what the code does, add a feature, or change a public name the input document gives.
   - If you see nothing that needs it, change nothing and make no second commit.
   - If you change anything, run every verification command again, in the input document's order. If every
     required result holds, commit only the files you changed, with the refactor message the input document
     gives. If one doesn't, undo your refactor: run `git -C <worktree> checkout -- .`, then, as a safeguard,
     delete by name any file your refactor created all the same, one `rm <file>` each, and
     never with `git clean`. Confirm with
     `git -C <worktree> status --porcelain` that nothing is left; if something is, stop and report it. Say
     under CLAIMS that the refactor was abandoned and why.
10. Reply in the format below.

## Stop and report, changing nothing more, when

- a test can't pass without changing a test or a test helper;
- a verification command's result differs from the one required, and the cause isn't in code the input document
  tells you to write;
- a verification command's result differs from the one required, and the cause is in code the input document
  gave you to copy: the document is then wrong, and correcting its code is not yours to decide;
- you see no further correction, within what the document specifies, to code you wrote from its description
  that would make the required results hold;
- a command the input document names didn't run, for a reason the document doesn't describe and allow, or the
  test command didn't run at all;
- the coverage bar the input document names can't be met by the change it specifies;
- a text the input document tells you to replace or insert after isn't in the file exactly once;
- doing the work would need a change to a file the input document doesn't list.

## Rules

- Never edit, add or delete a test file or a test helper. `git diff --name-only <red commit> HEAD` must show none.
- Never hard-code a value a test expects, and never make code behave differently under test.
- Never lower a coverage bar, exclude a file from it, or add an exemption.
- Never edit a file the input document or the repository's CLAUDE.md calls protected, and never look for another
  way to write one.
- Never push, open or edit a pull request, merge, or change a branch other than by the green commit and, when
  step 9 makes one, the refactor commit.
- When a command the input document names can't run for a reason the document describes and allows, list it
  under NOT RUN with that reason: its required result then counts as holding. The test command is never one of
  these. Never create what it's missing, and never claim its result.
- Run each command in the worktree, or in another folder when the input document names one for it: start the
  command with `cd <that folder> && `, because a shell's folder doesn't carry from one command to the next. Chain
  nothing else to it. A command the input document gives with its own folder option or `cd` runs as given.

## Reply format

Use exactly these headings, in this order, and put nothing before the first or after the last:

```text
GREEN: <the green commit from step 8, or none when you stopped before making it>
HEAD: <output of git rev-parse HEAD at the end; the same as GREEN when there is no refactor commit>
CHANGED:
<output of git diff --name-only <red commit> HEAD, then of git status --porcelain>
COMMANDS:
1. $ <command exactly as run>
   exit: <exit code>
   <the last 30 lines of its output, unchanged, and any earlier lines a claim or check rests on>
2. ...
CLAIMS:
- <one claim> [evidence: command N]
- <a claim you could not check> [UNVERIFIED]
NOT RUN:
- <command or check>: <reason>
STOPPED: <no, or the stop condition met and what was seen>
```

Every claim ends with `[evidence: command N]` naming a command under COMMANDS whose output shows it, or with
`[UNVERIFIED]`. Never alter, summarise or shorten a line of command output that you show, and never state a result
you didn't see in one. When the output behind a claim lies before the last 30 lines, show those lines too, under
that command.
````

### 5.3 `tdd-verifier.md`

````markdown
---
name: tdd-verifier
description: "Checks a finished test-first change against its written plan from a fresh context, by its own commands: the failing tests reproduced at the red commit in a disposable worktree, every verification command rerun at the final commit, the changed paths compared with the plan's allowed set, any refactor checked, each of the plan's numbered acceptance criteria decided, and the plan's mutants run. Third of three agents; it fixes nothing and never changes the folder it checks. Send it a task message with six lines: 'Input document:' the plan's absolute path, 'Worktree:' the absolute folder, 'Base commit:', 'Red commit:', 'Green commit:' and 'Final commit:' (green and final are the same commit when there was no refactor)."
tools: Read, Grep, Glob, Bash
model: claude-opus-5-5
effort: medium
---

You check one finished test-first change against its written plan (the input document). Two other agents wrote
the tests and the code. You have not seen their work or their replies, and you take nothing from them on trust:
what you report is what your own commands showed. You fix nothing.

## Steps

1. Take from the task message the input document's absolute path (`Input document:`), the worktree
   (`Worktree:`), and the base, red, green and final commits (`Base commit:`, `Red commit:`, `Green commit:`,
   `Final commit:`). If one is missing, reply with the single line `missing input: <which>` and stop.
2. Read the whole input document. Read the repository's CLAUDE.md for its rules. Check that the input document
   holds every one of these: a line reading exactly `Refactor: none` or `Refactor: allowed`; the test command;
   the red result required; the verification commands, each with its required result and the agents that run
   it; the paths allowed to change between each pair of commits; a numbered list headed `Acceptance criteria`;
   the folder, outside the repository, for your disposable worktrees. If one is missing, reply with the single
   line `input document incomplete: <what is missing>` and stop.
3. Start. Run `git -C <worktree> status --porcelain` and `git -C <worktree> rev-parse HEAD`. The status must be
   empty and HEAD the final commit. If not, run nothing more: reply in the format below with the `start` line
   `NOT REPRODUCED` and every other CHECKS line `NOT RUN [stopped at start]`.
4. Commits. Run `git -C <worktree> rev-parse <green commit> <final commit>`. With `Refactor: none`, the two must
   be the same commit. With `Refactor: allowed`, they may differ; when they do, run the input document's test
   command at the green commit in a disposable worktree (see "Disposable worktrees"). It must show no failed
   test.
5. Red. Run the input document's test command at the red commit in a disposable worktree, and compare the
   result with the red result it requires, point by point.
6. Commands. At the final commit, in the worktree, run every verification command the input document gives for
   you, in its order, and compare each result with the one required.
7. Paths. Run `git -C <worktree> diff --name-only <base commit> <red commit>`, the same for the red and green
   commits and, when they differ, for the green and final commits. Every path printed must be in the input
   document's allowed set for that pair.
8. Criteria. Work through the acceptance criteria in their numbered order. For each one, run the commands or
   checks it names, exactly as the input document gives them, and compare what you see with the result it
   requires, point by point. A criterion about an earlier commit you decide in a disposable worktree at that
   commit. When a criterion names a command you already ran at the same commit in steps 4 to 7, don't run it
   again: its line cites that command. Where the input document says a failed criterion ends your work, go
   straight to step 10, with the lines you didn't reach `NOT RUN [stopped at criterion <number>]`.
9. Mutants, when a criterion names them: run them in a disposable worktree at the final commit, never in the
   worktree. Apply each as the input document says, then run `git -C <folder> diff`. If it prints nothing, the
   mutant was not applied: its line is `NOT RUN [not applied]`, and you don't run the tests for it. Otherwise
   run the test command and record the tests that failed. Before the next mutant, remove that disposable
   worktree and add a new one. A mutant that leaves every test passing makes that criterion `NOT REPRODUCED`;
   a mutant that is `NOT RUN` makes it `NOT RUN`, with the mutant's reason, unless another mutant already made
   it `NOT REPRODUCED`.
10. End. Remove any disposable worktree you added and still have. Run `git -C <worktree> status --porcelain`,
    `git -C <worktree> rev-parse HEAD` and `git -C <worktree> worktree list`. The status must be empty, HEAD the
    final commit, and the list must show no folder you added.
11. Reply in the format below.

## Disposable worktrees

You never move the worktree to another commit, and you never apply a mutant in it. For those you use one
disposable worktree at a time:

1. The folder is the path the input document names for your disposable worktrees, outside the repository: the
   worktree is made at exactly that path. Run `git -C <worktree> worktree list` first. If it shows that path,
   another run left it or still uses it: don't remove it. Every check that needs a disposable worktree is then
   `NOT RUN [the disposable worktree's folder is in use]`.
2. `git -C <worktree> worktree add --detach <folder> <commit>`. If it fails, the checks that need it are
   `NOT RUN`, with its error as the reason.
3. Run the commands the input document gives to prepare such a folder for the tests, when it gives any, each
   starting with `cd <folder> && `. If one fails, the checks that need the folder are `NOT RUN`, with its error
   as the reason: go to step 5.
4. Run the check's commands there. In every command, wherever the worktree's path appears, in a `cd`, in a
   folder option or inside any other argument, put the disposable folder in its place and keep whatever follows
   it, so `<worktree>/pkg` becomes `<folder>/pkg`. A command with no folder of its own starts with
   `cd <folder> && `, or with the matching subfolder when the input document names one of the worktree's for
   it. This wins over the last rule under "Rules": nothing meant for another commit runs in the worktree or
   reads its files.
5. `git -C <worktree> worktree remove --force <folder>`, then `git -C <worktree> worktree list`, which must no
   longer show it. Do this before adding another one. Remove only a folder you added in this run. If the list
   still shows it, add no other: every check that still needs a disposable worktree is
   `NOT RUN [a disposable worktree could not be removed]`.

Where the input document tells you to move the worktree itself to an earlier commit, or to apply a mutant in it,
use a disposable worktree instead, as above.

## Rules

- Never change the worktree: fix, edit, add or delete nothing in it, never commit, and never run `git checkout`,
  `git switch`, `git reset`, `git restore`, `git stash` or `git clean` in it. All you run there are the input
  document's commands at the final commit, git commands that only read, and the `git worktree` commands of
  "Disposable worktrees", which change no file in it. Files you change go only in a disposable worktree.
- Never mark a check `REPRODUCED` on the strength of anything but your own command's output in this run.
- Decide a criterion only by the command or check it names. Give no opinion on the design, the style or the
  wording of the change, and add no criterion of your own.
- Never push, open or edit a pull request, or merge.
- When a command the input document names can't run, its line is `NOT RUN` with the reason, and never
  `NOT REPRODUCED`: you saw no result. Never create what it's missing, and never claim its result.
- Run each command in the worktree, or in another folder when the input document names one for it: start the
  command with `cd <that folder> && `, because a shell's folder doesn't carry from one command to the next. Chain
  nothing else to it. A command the input document gives with its own folder option or `cd` runs as given.

## Reply format

Use exactly these headings, in this order, and put nothing before the first or after the last:

```text
HEAD: <output of git rev-parse HEAD at the end>
STATUS: <output of git status --porcelain at the end, or "clean">
COMMANDS:
1. $ <command exactly as run>
   exit: <exit code>
   <the last 30 lines of its output, unchanged, and any earlier lines a claim or check rests on>
2. ...
CHECKS:
- start: <result>
- commits: <result>
- red, <each point of the red result>: <result>
- command <number>: <result>
- paths, <base to red | red to green | green to final>: <result>
- criterion <number>, <each point it requires>: <result>
- end: <result>
MUTANTS:
- mutant <name>: FAILED A TEST (<test names>) [evidence: command N] | SURVIVED [evidence: command N] | NOT RUN [<reason>]
VERDICT: PASS | FAIL | INCOMPLETE
```

A `<result>` is `REPRODUCED [evidence: command N]`, `NOT REPRODUCED [evidence: command N]` or
`NOT RUN [<reason>]`, where command N is one under COMMANDS whose output shows it. One CHECKS line for each of
steps 3 and 4, one for every point of the red result, one for each verification command given for you, one for
each pair of commits compared, one for every point of every criterion in the criteria's order, and one for
step 10. Leave MUTANTS empty when the input document has none; on an early stop, the mutants you didn't reach
are `NOT RUN` too. The verdict is computed from the CHECKS lines and nothing else: `INCOMPLETE` when the `start`
line is `NOT REPRODUCED`; otherwise `FAIL` when any line is `NOT REPRODUCED`; `PASS` when every line is
`REPRODUCED`, or `NOT RUN` for a reason the input document describes and allows; otherwise `INCOMPLETE`. Never
alter, summarise or shorten a line of command output that you show. When the output behind a
check lies before the last 30 lines, show those lines too, under that command.
````

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "The plugin ships three agents, agents/tdd-test-writer.md, agents/tdd-implementer.md and agents/tdd-verifier.md, each byte for byte the block §5 gives for it. Frontmatter keys are name, description, tools, model and effort, in that order and no others; model claude-opus-5-5 and effort medium; the test-writer's and the implementer's tools are Read, Grep, Glob, Edit, Write and Bash, and the verifier's Read, Grep, Glob and Bash. None has Agent, so none starts another agent, and none sets omitClaudeMd, so each loads the target repository's CLAUDE.md files."
  - id: BEH-02
    status: active
    rule: "The agents work only from an input document that holds §4's twelve items. Before changing anything, the test-writer checks for all twelve, and the implementer and the verifier each check for the items their text lists: every item a step of theirs uses. An agent that finds one missing replies with the single line 'input document incomplete: <what is missing>' and stops."
  - id: BEH-03
    status: active
    rule: "The agents are generic: their bodies name no repository, owner, absolute path, test command or coverage figure. Everything specific to a change comes from the input document, and each agent decides nothing the input document doesn't decide."
  - id: BEH-04
    status: active
    rule: "The test-writer starts only from a clean tree at the base commit, runs the baseline commands and stops when a result differs from the one required, writes the tests exactly as the input document gives them, runs the test command, compares the result with the required red result point by point and, only when every point holds, commits only the test files it changed, with the message given. It never changes the code under test, an existing test or assertion, a helper the document doesn't name, a configuration file or a document."
  - id: BEH-05
    status: active
    rule: "The implementer starts only from a clean tree at the red commit, confirms the tests that fail there are the ones the input document says, makes the code change and the document edits exactly as given, runs every verification command the document gives for it in order and, only when every required result holds, commits the files listed for the green commit. When a required result doesn't hold and the cause is in code it wrote from the document's description, it corrects that code within what the document specifies and runs every verification command again, more than once if need be; when the cause is in code the document gave it to copy, or it sees no further correction that would make the results hold, it stops and reports (ERR-09). A command that can't run for a reason the document describes and allows is listed under NOT RUN and its result counts as holding; any other command that didn't run, and the test command always, is a stop with no commit (ERR-04, ERR-07). It never gets a result to hold by changing a test, a command, a required result or a coverage bar, and never edits, adds or deletes a test file or a test helper, hard-codes an expected value, or makes code behave differently under test."
  - id: BEH-06
    status: active
    rule: "Refactor is a step of the implementer, taken only when the input document says 'Refactor: allowed'. It may change only non-test, non-document files the green commit changed, and only by renaming, extracting, inlining, reordering, or removing duplication or dead code, with no change in what the code does, and creates, deletes and renames no file. A change is followed by every verification command again; when all hold it is committed separately with the refactor message, and when one doesn't the implementer undoes it: git checkout -- ., then, as a safeguard, any file the refactor created all the same deleted by name and never with git clean, then a status check; if anything is left it stops and reports. It reports the refactor abandoned and why. That undo discards only what the step itself just wrote (§2's reading of ADR-005 D7)."
  - id: BEH-07
    status: active
    rule: "The verifier never changes the worktree it checks: no edit, no commit, and no checkout, switch, reset, restore, stash or clean there (ADR-005 D7). All it runs there are the input document's commands at the final commit, git commands that only read, and the git worktree commands below, which change no file in it. To run anything at another commit, and to apply any mutant, it uses one disposable worktree at a time, made with git worktree add --detach at exactly the path the input document names, outside the repository, and prepared as the document says. Every command for that check runs there: wherever the worktree's path appears in a command, in a cd, a folder option or any other argument, the disposable folder takes its place, with whatever follows it kept. It removes each before adding another, removes only a folder it added in that run, and never removes a folder the worktree list already showed. A prepare command that fails, or a disposable worktree that can't be removed, makes the checks that need one NOT RUN (ERR-10). At its end the status is empty, HEAD is the final commit, and git worktree list shows no folder it added."
  - id: BEH-08
    status: active
    rule: "The verifier makes the same fixed checks for every input document, from its own commands' output in that run and nothing else: start (a clean tree at the final commit); commits (with 'Refactor: none' the green and final commits are the same; when they differ under 'Refactor: allowed', the tests show no failure at the green commit); red (the test command at the red commit gives the required red result, point by point); every verification command the document gives for it, rerun at the final commit; the paths changed between base and red, red and green, and green and final, each within the document's allowed set; then each numbered acceptance criterion, by the command or check it names; the mutants; and the end state of BEH-07. A criterion that names a command already run at the same commit is not run again: its line cites that command. It has seen no other agent's reply, gives no opinion on design, style or wording, and adds no criterion. After applying each mutant it runs git diff in the disposable folder: an empty diff means the mutant was not applied, its line is NOT RUN [not applied] and its tests aren't run. A mutant that leaves every test passing makes its criterion NOT REPRODUCED; one that is NOT RUN makes it NOT RUN unless another already made it NOT REPRODUCED. A command that can't run is NOT RUN with the reason, never NOT REPRODUCED. The verdict is computed from the CHECKS lines alone: INCOMPLETE when the start line is NOT REPRODUCED; otherwise FAIL when any line is NOT REPRODUCED; PASS when every one is REPRODUCED, or NOT RUN for a reason the input document describes and allows; otherwise INCOMPLETE."
  - id: BEH-09
    status: active
    rule: "Every reply has exactly the headings §5 gives for that agent, in that order, with nothing before the first or after the last. Each command is shown as run, with its exit code and the last 30 lines of its output unchanged, plus any earlier lines a claim or check rests on. Every claim of the test-writer and the implementer ends with [evidence: command N] or [UNVERIFIED]. Every CHECKS line of the verifier ends with [evidence: command N], or is NOT RUN with its reason in brackets; a verifier that stops early still replies in full, with the lines it didn't reach NOT RUN. The implementer's GREEN: is 'none' when it stopped before the green commit. No agent alters, summarises or shortens an output line it shows, or states a result it didn't see in one."
  - id: BEH-10
    status: active
    rule: "No agent pushes, opens or edits a pull request, or merges, and none changes a branch other than by the commits its text names. Push, pull request and merge are the owner's to approve, each separately."
  - id: BEH-11
    status: active
    rule: "The main conversation orchestrates. It runs the agents in order, test-writer, implementer, verifier, each as a new agent given only the task-message lines its description names; it never passes one agent's reply to another and never continues a finished agent. The red commit is the test-writer's HEAD:, the green commit the implementer's GREEN:, the final commit the implementer's HEAD:. After each agent returns and before starting the next, it runs git status --porcelain and git diff --name-only <previous commit> HEAD itself and compares the paths with the input document's allowed set for that step, not relying on the agent's CHANGED section. The test-writer's and the implementer's STOPPED lines must be 'no'. The change is not done, and is not reported as done, until the verifier's VERDICT is PASS and that check after the verifier shows a clean status at the final commit. It gives the owner every reply as returned, both attempts' when there was a second run, not a summary."
  - id: BEH-12
    status: active
    rule: "One automatic second run, and only one. It is made on the first FAIL when all of these hold: every NOT REPRODUCED line concerns the implementer's work (the commits line, a command line, a paths line after the red commit, a criterion about the green or final commit, or the mutants criterion); the start, red and end lines are REPRODUCED; and no CHECKS or MUTANTS line is NOT RUN for a reason the input document doesn't describe and allow. A failed start or end line never starts it: an end line can fail because one of the verifier's own commands left a file behind, and a second run would then reset the branch and rerun the implementer on correct code. A red line that is NOT RUN doesn't start it, and neither does a mutant that was not applied. All of those go to the owner (ERR-03, ERR-06, ERR-10 to ERR-12). When they hold, the main conversation, running each command alone: (1) keeps the failed commit with git branch <branch>-attempt-1 <final commit>; (2) runs git worktree list and removes, with git worktree remove --force, any folder the input document names for the verifier's disposable worktrees or its mutants; (3) runs git reset --hard <red commit>, after which the status must be empty and HEAD the red commit; (4) starts a new implementer with the same four lines plus 'Previous failure:' and, under it, the verifier's NOT REPRODUCED lines with the output lines they cite, copied unchanged, and nothing else from any reply; (5) starts a new verifier with the new green and final commits and no word of the first attempt. The reset runs only after step 1 has kept the commit, on a tree the preceding check showed clean (§2's reading of ADR-005 D7). The backup branch is never pushed; the owner is told it exists, and deleting it is the owner's."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "A task message lacks a line the agent's description names"
    handling: "The agent replies with the single line 'missing input: <which>' and stops, changing nothing"
    user_result: "The main conversation gives the owner the reply and stops; no second run"
  - id: ERR-02
    status: active
    condition: "The input document lacks an item the agent checks for (BEH-02)"
    handling: "The agent replies with the single line 'input document incomplete: <what is missing>' and stops, changing nothing"
    user_result: "The owner sees what the input document lacks; no second run"
  - id: ERR-03
    status: active
    condition: "The worktree's status isn't empty at an agent's start, or HEAD isn't the base commit (test-writer), the red commit (implementer) or the final commit (verifier)"
    handling: "The test-writer and the implementer stop and report the status and HEAD, changing nothing. The verifier runs nothing more and replies in full, with the start line NOT REPRODUCED, every other line NOT RUN and the verdict INCOMPLETE"
    user_result: "The replies so far; no second run. A verifier's failed start line goes to the owner and never starts the second run (BEH-12)"
  - id: ERR-04
    status: active
    condition: "A stop condition of the test-writer or the implementer is met: a baseline or test result differs from the required one, a place to insert at or a text to replace isn't in the file exactly once, a test can't pass without changing a test or a helper, a coverage bar can't be met by the change specified, or the work would need a file the input document doesn't list; or a command the document names didn't run for a reason the document doesn't describe and allow, or the test command didn't run at all"
    handling: "The agent stops, changes nothing more, and reports the condition and what it saw on its STOPPED line"
    user_result: "The main conversation gives the owner the replies so far and stops. No second run: a stop means the input document and the repository disagree, and a second run would stop the same way"
  - id: ERR-05
    status: active
    condition: "The verifier's verdict is INCOMPLETE"
    handling: "The main conversation gives the owner the replies so far and stops, with no second run"
    user_result: "The replies, with the checks that were NOT RUN and why"
  - id: ERR-06
    status: active
    condition: "The verifier's verdict is FAIL and: a NOT REPRODUCED line is the red line, the base-to-red paths line, the end line or a criterion about the red commit or the tests; or the red line, or any other CHECKS or MUTANTS line, is NOT RUN for a reason the input document doesn't describe and allow; or the verdict is FAIL for the second time"
    handling: "The main conversation gives the owner every reply and stops, with no second run (BEH-12). The tests are then in doubt, or a check was never made, or the worktree was left in a state the implementer didn't cause; the implementer may not change the tests, and a second run would start from a wrong premise"
    user_result: "Every reply, and the name of the backup branch when there was a second run"
  - id: ERR-07
    status: active
    condition: "A command the input document names can't run for a reason the document describes and allows, in any of the three agents"
    handling: "The test-writer and the implementer list it under NOT RUN with that reason, and its required result counts as holding, so the commit is still made; the verifier marks its line NOT RUN with the reason, which doesn't prevent PASS. No agent creates what the command is missing or claims its result. The test command is never such a command for the test-writer or the implementer: if it can't run, they stop (ERR-04). A command that didn't run for any other reason is a stop with no commit for those two (ERR-04), and for the verifier a NOT RUN line that makes the verdict INCOMPLETE, or FAIL with no second run when another line is NOT REPRODUCED (ERR-06)"
    user_result: "The command and the reason, in the reply"
  - id: ERR-08
    status: active
    condition: "The implementer's refactor fails a verification command"
    handling: "It undoes the refactor (git checkout -- ., then each file the refactor created deleted by name), confirms the tree is clean at the green commit, makes no second commit, and says under CLAIMS that the refactor was abandoned and why (BEH-06). If the tree isn't clean after the undo, it stops and reports what is left"
    user_result: "A change whose final commit is the green commit, with the abandoned refactor reported"
  - id: ERR-09
    status: active
    condition: "A verification command's result differs from the one required, in the implementer's hands, and the cause is in code the input document gave it to copy; or it is in code the implementer wrote from the document's description and its corrections don't make the results hold"
    handling: "The implementer stops, makes no commit, and reports the command, the result and the cause on its STOPPED line, with GREEN: none. It never loosens a test, a command, a required result or a coverage bar"
    user_result: "The replies so far; no second run. A plan whose own code fails is the owner's to correct"
  - id: ERR-10
    status: active
    condition: "The folder the input document names for the verifier's disposable worktrees is already in the worktree list; or git worktree add fails; or a command that prepares the folder fails; or a disposable worktree the verifier added can't be removed"
    handling: "The verifier removes nothing it didn't add, and adds no other disposable worktree while one it added is still listed. Every check that needs one is NOT RUN with the reason. The verdict then follows from the CHECKS lines as always: INCOMPLETE, or FAIL when another line is NOT REPRODUCED. Either way there is no second run, since a NOT RUN line blocks it (BEH-12, ERR-06)"
    user_result: "The reply, naming the folder; the owner clears it"
  - id: ERR-11
    status: active
    condition: "At the verifier's end the status isn't empty, HEAD isn't the final commit, or the worktree list shows a folder it added"
    handling: "The end line is NOT REPRODUCED and the verdict FAIL. The verifier deletes nothing in the worktree to get there"
    user_result: "Every reply, with no second run: a failed end line never starts one (BEH-12, ERR-06). Something the plan's commands leave behind is the plan's to ignore or clean"
  - id: ERR-12
    status: active
    condition: "After the verifier applies a mutant, git diff in the disposable folder prints nothing"
    handling: "The mutant was not applied: its MUTANTS line is NOT RUN [not applied], its tests aren't run, and its criterion is NOT RUN unless another mutant already made it NOT REPRODUCED"
    user_result: "Every reply, with no second run (BEH-12): the owner corrects how the plan gives the mutant"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "Each agent file's frontmatter uses only fields Claude Code's subagent documentation supports for a plugin agent, with the values §5 fixes, and the plugin still validates with the three files present"
    measured_by: "src/tests/tdd-agents/test_structure.py, and claude plugin validate src/claude/DevForgeAI"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 14, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: this spec against `spec.schema.json` | Passes, with every BEH, ERR and QR item covered (checked 2026-11-09, version 2) |
| Version 1's build | `6dce940` (2026-11-09): the three files byte for byte from version 1's §5; VER-01 as version 1 gave it, 10 tests, failing before the files existed and passing after; `pytest src/tests` 1742 passed, 1 skipped; `claude plugin validate` passes. plugin-validator: nothing blocking. skill-reviewer: nothing critical, eight major and thirteen minor notes on the texts; Bryan took all eight majors and five smaller notes into version 2. Not released, and VER-02 not run on it |
| Version 2's first build | `f1203ac` (2026-11-09): VER-01 as it then stood, 11 tests; `pytest src/tests` 1743 passed, 1 skipped; `claude plugin validate` passes. plugin-validator: nothing blocking, six notes. skill-reviewer: nothing critical; the eight first-round notes resolved except M3 and M5 in part; five more major notes. Bryan decided all five and six smaller notes into this version, and no further review before VER-02 |
| VER-01 | Version 2, `5f79173` (2026-11-09): `src/tests/tdd-agents/test_structure.py`, 14 tests, pass; `pytest src/tests` 1746 passed, 1 skipped; `claude plugin validate` passes; plugin-validator, for loading and fields only: pass. No text review of this build, on Bryan's decision |
| VER-02 | Not run: Bryan runs it from a plain terminal, by `docs/runbooks/tdd-agents-ver-02.md` |
| VER-03 | Not run; it doesn't gate the release (§13 item 1) |

There is no eval suite. The agents belong to no skill, and no eval case here has exercised a plugin agent (SPEC-014
§13 item 7: "no case allows the Agent tool"). Whether an eval run can start these agents and let them commit is not
verified; a suite is §13's question. This spec specifies no story, so its VER items carry no `upstream`.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "src/tests/tdd-agents/test_structure.py, for each of the three files: the file equals §5's block for it byte for byte; the frontmatter keys are exactly name, description, tools, model, effort, in that order; name equals the file name without .md; tools, split on commas and trimmed, equals §5's list, and Agent is in none; model is claude-opus-5-5 and effort is medium; the description is one double-quoted line; the body holds none of these strings in any case: /home/, bankielewicz, npm run, claude plugin, 95; the body holds the headings ## Steps, ## Rules and ## Reply format, and the test-writer's and the implementer's also ## Stop and report, changing nothing more, when; the body holds [evidence: command N], and [UNVERIFIED] (test-writer, implementer) or NOT REPRODUCED (verifier); the body holds Refactor: none, Refactor: allowed, input document incomplete: and missing input:, and the rule against creating what a command that can't run is missing; the test-writer's and the implementer's bodies say a command that can't run for a reason the document describes and allows counts as holding, and name a command that didn't run as a stop condition; the implementer's body holds GREEN: with none for an early stop, and names git clean only to forbid it; the verifier's body holds Green commit:, criterion <number> and the fixed CHECKS lines start, commits, red, command, paths and end; the descriptions hold 'three lines' (test-writer), 'four lines' (implementer) and 'six lines' (verifier); the verifier's body holds git worktree add --detach, ## Disposable worktrees, the git diff after each mutant with NOT RUN [not applied], the replacement of the worktree's path in a disposable worktree's commands, and no separate NOT RUN: heading, and names git checkout, git switch, git reset, git restore, git stash and git clean only in the one rule that forbids them. Also: the three files exist in the agents folder; this spec validates against spec.schema.json and every BEH, ERR and QR item is covered by a VER item."
    level: unit
    covers:
      - BEH-01
      - BEH-03
      - BEH-07
      - QR-01
  - id: VER-02
    status: active
    obligation: "Live, before any release, in a plain Claude Code session started with --plugin-dir on a copy of the build, on a scratch git repository made for the run, outside every project. The scratch input document holds §4's twelve items, says 'Refactor: allowed', gives test code holding one \\u escape, and has one criterion about the red commit and no mutant (§4 item 3: mutants given as replacements of exact lines need 'Refactor: none'; VER-03 (e) runs one). The main conversation follows BEH-11. Pass when: (a) the three agents run in order from new contexts and each reply has exactly its headings; (b) the test-writer's commit holds only the test files and the tests fail as required; (c) the implementer's green commit holds no test file, and its refactor step either commits separately or changes nothing; (d) the verifier's VERDICT is PASS, with the fixed CHECKS lines and one per point of each criterion, a command a criterion shares with a fixed check run once, the red failure reproduced in a disposable worktree, and afterwards a clean status at the final commit and no leftover worktree. Recorded with it, pass or not: whether the committed test file holds the \\u escape as the input document gives it, or the character it stands for; each agent's model and effort as its row in /tasks shows them; whether a command starting with cd <folder> && raises a permission prompt in a subagent; every reply as returned."
    level: manual
    covers:
      - BEH-02
      - BEH-04
      - BEH-05
      - BEH-06
      - BEH-07
      - BEH-08
      - BEH-09
      - BEH-10
      - BEH-11
  - id: VER-03
    status: active
    obligation: "Live, on the same scratch repository, the failure paths: (a) an input document lacking one of §4's items gets the single line 'input document incomplete: …' from the test-writer and no change; (b) a task message lacking a line gets 'missing input: …'; (c) a dirty worktree stops an agent with its status reported; (d) an input document whose required red result the repository can't give makes the test-writer stop with no commit, and one whose named command can't run for a reason it describes gets a NOT RUN line; (e) a verifier given an implementer's commit that a mutant survives returns FAIL, and the main conversation makes the backup branch, resets to the red commit, and starts a new implementer with only the NOT REPRODUCED lines, then a new verifier; a second FAIL, a FAIL on the red commit, and an INCOMPLETE each go to the owner with every reply and no further run; (f) a refactor that fails a verification command is undone, with the green commit left as the final one; (g) an implementer given code to copy that fails a verification command stops with no commit and GREEN: none; (h) a verifier whose disposable folder is already a registered worktree removes nothing and returns INCOMPLETE; (i) a verification command that leaves an untracked file in the worktree gives an end line NOT REPRODUCED and FAIL, with no second run; (j) a mutant whose replacement matches nothing is NOT RUN [not applied], and no second run follows; (k) a prepare command that fails, and a plan command that names the worktree's path as a plain argument, each behave as BEH-07 says; (l) an implementer whose verification command can't run for a reason the document allows commits with it under NOT RUN, and one whose command didn't run for another reason stops with no commit."
    level: manual
    covers:
      - BEH-12
      - ERR-01
      - ERR-02
      - ERR-03
      - ERR-04
      - ERR-05
      - ERR-06
      - ERR-07
      - ERR-08
      - ERR-09
      - ERR-10
      - ERR-11
      - ERR-12
```

VER-02 gates the first release; VER-03 doesn't, and stays recorded as not run until it is (Bryan, 2026-11-09; §13
item 1).

## 10. Rollout, migration and rollback

- **New files, nothing to migrate.** They ship in the next plugin version after approval, the build and VER-02; the
  version number is set at merge, on Bryan's word. Rolling back is removing the three files and
  `src/tests/tdd-agents/`.
- **Before a session in another repository can call them**, each step Bryan's to approve:
  1. the three files are merged;
  2. the `devforgeai` plugin is released with them;
  3. the plugin is updated on the machine (CLAUDE.md, "Traps": the marketplace install, not the deployed copy, is
     what runs), and a new Claude Code session lists `devforgeai:tdd-test-writer`, `devforgeai:tdd-implementer`
     and `devforgeai:tdd-verifier` among its agent types.
- **The tracker.** No change: a subagent's tool calls are recorded in no run (SPEC-013 DM-01), and no tracked skill
  calls these agents.
- **Codex.** Not ported; a port is for Codex sessions.
- **Records.** CLAUDE.md gains a row for the agents (SPEC-020).

## 11. Implementation plan

After approval, inside one `/plugin-dev:create-plugin` iteration with the scope "add three plugin agents:
tdd-test-writer, tdd-implementer, tdd-verifier", with `/plugin-dev:skill-development` and
`/plugin-dev:agent-development`, on its own branch and worktree (ADR-001):
1. Read `docs/research/Claude/subagents.md` and confirm §5's frontmatter rows are still supported. If one isn't,
   stop and ask Bryan.
2. Write `src/tests/tdd-agents/test_structure.py` (VER-01) and see it fail.
3. Write the three files from §5's blocks, byte for byte. VER-01 passes, with the full test suite and
   `claude plugin validate`.
4. Run plugin-validator and skill-reviewer on the final commit; take any finding that would change §5's texts to
   Bryan, since a text change is a spec change.
5. Run VER-02 on a scratch repository and record the results in §9. VER-03 doesn't gate the release (§13 item 1).
6. Commit, push, pull request, version bump and release only on Bryan's go-ahead, each separately.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| Two agents (writer and checker) | Bryan chose three: the tests and the code are then written by contexts that can't fit one to the other |
| A separate refactor agent | Green and refactor are the same duty, writing code under the same fixed tests; a separate agent would check nothing and would lack the reasons behind the code |
| An orchestrator agent | The main conversation orchestrates, so the owner sees each hand-off; and a plugin agent with `Agent` could start others unseen |
| Continuing a finished agent for a second attempt | Every run is a new agent with an empty context; a continued one carries the failed attempt's reasoning |
| Passing the implementer's reply to the verifier | The verifier must come to the work cold, and report only what its own commands showed |
| The verifier checking out earlier commits in the worktree | ADR-005 D7; and a verifier that dies mid-run would leave the branch on an old commit |
| Recording them under the experts work (ADR-003 A7) | They recommend nothing and carry out a written plan; Bryan: workers, not experts |
| Making them the dev step's `tdd` variant | No dev spec exists, and ADR-005 D1 governs it; that would turn a small job into settling the whole dev step |
| A recorded decision in CLAUDE.md with no spec | The limits and the orchestrator's rules would have no home, and the structure tests nothing to cite |

## 13. Open questions

For Bryan, in order. None of these is a requirement until he decides it.

1. **Resolved (Bryan, 2026-11-09): only VER-02 gates the first release.** VER-03 stays recorded as not run. As
   sent: running it "means staging six failure scenarios by hand", and the riskiest path, the automatic second run,
   "keeps the failed commit on a backup branch, so a broken retry" on a real change "costs time, not work".
2. **§4 item 9 and the two texts it touches.** Moving the verifier to disposable worktrees needs the input document
   to name their folder and how to prepare one. This draft adds that as item 9, and adds it to the lists the
   test-writer and the implementer check, so a missing folder stops the work at its start and not at its end. **Resolved
   (Bryan, 2026-11-09): confirmed**, with the verifier's wording in §5.3. As sent: "otherwise a missing folder is
   discovered only after the tests and code are already committed."
3. **Not verified** (VER-02 records the first three):
   - that `effort: medium` and a full model ID take effect for a plugin agent on the installed Claude Code build
     (source: `docs/research/Claude/subagents.md`, read 2026-11-09; not tried);
   - whether a command that starts with `cd <folder> && ` raises a permission prompt in a subagent. If it does, the
     owner sees a prompt per command; the agents' rule isn't changed for it without his say;
   - whether an agent's Edit or Write turns a `\u` escape into the character it stands for;
   - that a repository's Stop hooks run, or don't, for a subagent's turns.
4. **Enforcement.** §1's limits say the duties are written rules. Bryan's direction of 2026-11-09 for the experts
   work is "gates in mods over ceremonial skill text". Whether a mod gate should hold these agents to their paths
   is not asked for here; a separate decision.
5. **The orchestrator's rules have no carrier.** BEH-11 and BEH-12 bind the main conversation, which in another
   repository sees only the three descriptions. Until something carries them (a skill, a reference file the
   descriptions point to, or the input document itself), each input document or its session must restate them.
   Bryan, 2026-11-09: this doesn't block the first use, whose plan states the run order, the checks between agents
   and the second run itself and points at this spec; before the agents are used in a further repository the rules
   should ship with the plugin, as a small skill or a reference file. Which of the two is undecided.
6. **An eval suite.** None is specified (§9). A probe would show whether an eval run can start a plugin agent, and
   whether the agents can commit in a repository the run makes itself.
7. **The dev step.** Whether the later dev spec (ADR-005 D1) uses these agents for its `tdd` variant.
8. **Reviewer notes not taken into version 2** (the skill-reviewer's minors on version 1; none blocks, and they
   stay open notes: Bryan, 2026-11-09): a plan that
   changes an existing test meets the test-writer's "never change or delete an existing test"; "leave it" for an
   escape the tool converted doesn't say to look at what was written; no instruction for a repository with no
   CLAUDE.md, or one whose rules conflict with the input document; and a multi-line commit message under "chain
   nothing else to it". From the second review, also not taken: a CHECKS line cites one command where several
   decided it; the mutants criterion's place in the run order when it isn't the last criterion; and the
   green-to-final paths line when `Refactor: none` and the two commits differ (the verdict is already FAIL).
9. **"The test command is never one of these."** The rule that a `NOT RUN` the document allows counts as holding
   excepts the test command for the test-writer and the implementer: without its result there is no red result to
   show and no failing tests to confirm. Bryan's answer didn't name that exception; it was this draft's reading.
   **Resolved (Bryan, 2026-11-09): confirmed.** As sent: "Without the test command's result there is no red result
   to show, so a stop is right."

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-11-09 | claude-code (session 9037a656-70d0-43bb-828a-447520233f48) | Initial draft, from Bryan's design of 2026-11-09 for three test-first agents and his answers of the same day: a new spec; workers, not experts; the verifier in disposable worktrees with a recorded reading of ADR-005 D7 for the implementer's undo and the retry's reset; structure tests plus one live run on a scratch repository | all |
| 1 | 2026-11-09 | claude-code (session 9037a656-70d0-43bb-828a-447520233f48) | Before approval, Bryan's answers to §13 items 1, 2 and 5: only VER-02 gates the first release; §4 item 9 and its two checks confirmed, with the verifier's wording; the orchestrator's rules are restated by the first plan and ship with the plugin before a further repository uses the agents | §9, §11, §13 |
| 1 | 2026-11-09 | Bryan | Approved ("i approve"), with only VER-02 gating the first release | status |
| 2 | 2026-11-09 | claude-code (session 9037a656-70d0-43bb-828a-447520233f48) | Bryan's decisions of 2026-11-09 on the build's reviews ("v2 now with all eight"): the verifier's checks fixed for every plan, with a shared command run once (M8); its end state a CHECKS line and a full reply on an early stop (M2); in a disposable worktree every command runs there (M3); mutants in a disposable worktree at the final commit (M4); the folder is the worktree's own path, an add that fails, where to prepare, and removing only what it added (M5); the test-writer's rule for a command that can't run, and its HEAD checked against the base commit (M1); the implementer stops when the plan's own code fails and corrects only code it wrote, loosening nothing (M6); §4 items 10 to 12 and item 6 widened (M7); GREEN: none on an early stop; a refactor's undo deletes created files by name, never with git clean; ERR-09 to ERR-11; status in-review | frontmatter, §2, §4, §5, BEH-02, BEH-04 to BEH-09, BEH-12, ERR-03, ERR-04, ERR-06 to ERR-11, VER-01 to VER-03, §9, §13 |
| 2 | 2026-11-09 | claude-code (session 9037a656-70d0-43bb-828a-447520233f48) | Before approval, Bryan's decisions of 2026-11-09 on the reviews of version 2's first build (f1203ac): in a disposable worktree the worktree's path is replaced wherever a command names it; a failed prepare command or removal makes the checks NOT RUN; git diff proves each mutant was applied, else NOT RUN [not applied]; a NOT RUN the document describes and allows counts as holding for the test-writer and the implementer, and any other command that didn't run is a stop; the second run needs the start, red and end lines REPRODUCED and no unallowed NOT RUN; ERR-10 reworded, ERR-12 added; a refactor creates no file; corrections may repeat; the verifier's separate NOT RUN heading removed; no further review before VER-02 | §2, §5, BEH-05 to BEH-08, BEH-12, ERR-03, ERR-04, ERR-06, ERR-07, ERR-10 to ERR-12, VER-01, VER-03, §9, §13 |
| 2 | 2026-11-09 | Bryan | Approved ("SPEC-020 v2 is approved"), with the test-command exception confirmed (§13 item 9) and §13 item 8's notes left open | status, §13 |
