# Handoff rules

The next session may start cold: after `/compact` it has only a summary, and in a new session it has nothing. It
can read files and run commands, but it can't see this conversation. Write so that it can act without asking about
anything this session knew: full fidelity, zero ambiguity, and pointers instead of copies.

## Where the files go

- **Project root:** the folder the session started in (its working directory then, not a folder a later `cd` moved
  the shell to), or a folder holding it that the user names as the project. START-HERE section 1 states it. Every
  path written or checked is under it unless written absolute.
- **Handoff folder:** `devforgeai/handoff/<branch>/` under the root, one folder per branch, so sessions on different
  branches of one checkout don't overwrite each other. The folder name is the branch name with each run of
  characters other than letters, digits, `.`, `_` and `-` replaced by `-` (`feat/csv-export` becomes
  `feat-csv-export`); `detached-` and the short hash on a detached HEAD; `no-git` when git can't be used for the
  project folder (see "Checking the state").
- **`devforgeai/handoff/.gitignore`** holds the single line `*`: the handoff is working notes for the next session on
  this machine, never committed. Write it, with the folder, before any other file.
- The files: `START-HERE.md` (the master), `RESUME-PROMPT.md` (what the user pastes after `/compact`), `TASKS.md`
  (checkpoints), and `TASKS-archive.md` once TASKS.md has more than 20 done entries.

## The order, and why

1. Check the state. 2. Write START-HERE.md. 3. Write RESUME-PROMPT.md. 4. Update TASKS.md and the session's own plan
file. 5. Save learnings to memory. 6. Run the checker and fix. 7. Report.

The skill spends context too. If the session is cut off before the end (the context limit, with automatic compaction
off), START-HERE.md is written first, so the most important file exists; the next session, given its path, finishes
the rest by running the skill again. Write each file in one Write call.

## Checking the state

Run only small, read-only commands, and don't re-read what the session already holds (its CLAUDE.md files and memory
index are already in context). Read only the handoff folder's earlier files.

```bash
GIT_OPTIONAL_LOCKS=0 git status --porcelain=v2 -b
git log -n 5 --oneline
git diff --stat
git diff --stat --cached
gh pr list --limit 10
```

- Run no test or build command. Cite the last result the session saw, with its date and `(unverified)`, unless the
  user's note asks for a run.
- When git reports an error for the project folder, isn't installed, or finds a repository whose top level
  (`git rev-parse --show-toplevel`) is a parent of the project root (a repository that isn't the project's, such as a
  home folder kept in git, unless the user named that folder as the project), skip the git
  checks, use the folder `no-git` when there is no usable branch, say in section 2 what couldn't be checked, and mark
  what depends on it `(unverified)`. The same when `gh` is missing or fails: skip it and say so.
- When the session's progress tracker has an open run, name it and its step in section 1 (the tracker's
  `devforgeai/progress/sessions/<session>/current.json`, when it exists).

## START-HERE.md, section by section

Start from `assets/start-here.md`. Replace every `[[fill: ...]]`; delete a line the fill says to delete when it
doesn't apply. More `##` sections may follow section 7; `###` headings may go anywhere.

**1. What this is.** Two or three sentences a stranger understands, then the project root, the branch, the time
written (UTC) and the session ID.

**2. Verified state.** One fact per bullet, each ending with how it was checked, or `(unverified: <source>, <date>)`.
- Good: `- PR #12 is open as a draft [checked: gh pr view 12 --json isDraft -> true]`
- Good: `- 214 tests passed (unverified: the session's run of 2026-10-05)`
- Bad: `- Tests pass` (which tests, checked how, when?)

**3. Decisions.** Under `### Decided`, each decision with who decided, the date and their words in double quotes:
`- CSV only, no Excel: Dana, 2026-10-04, "CSV is enough for now"`. Under `### Open`, each question still the user's,
with the options as the user saw them. Never move an open question to Decided because it seems settled: only the
user's words decide it.

**4. Read first.** A numbered list; each item starts with the path in backticks, then why and when to read it. For a
long file, give the search instead of the whole file: `grep -n "delimiter" docs/design.md`. When the
session keeps its own plan or task file, list it here as the source of truth for the steps it lists. End with the
line "When something you need isn't here, search the repository and memory before asking the user."
A path that will exist later says `(not yet created)` on its line; a path valid only until the session ends (a
scratch file) says `(session-only)` on its line or the line above.

**5. Outstanding.** The user's note first, when the skill was given one. Then a numbered list in order:
`1. Fix the delimiter. Next: edit src/export.py:42. Waits for: nothing.` or
`2. Release. Next: ask the user which version. Waits for: the user's choice (section 3, Open).`
With nothing left, the single line `Nothing outstanding.`

**6. Rules, traps and learnings.** What cost time and how to avoid it, the project rules that apply (cite the file,
don't restate it), and this session's learnings. The durable ones also go to memory (`references/memory.md`).

**7. Before acting.** Commands to run first, each with what it shows if nothing changed:
`- git log -n 1 --oneline - shows a1b2c3d`.

**Carrying over an earlier handoff.** When the folder holds an earlier START-HERE.md, keep what still holds: its
decisions, open questions, rules, traps and learnings, and its outstanding items not finished; drop what is done
(TASKS.md keeps it). When the earlier handoff is about other work (another topic on the same branch), keep its
TASKS.md entries under a `##` heading naming that work, after the required ones, write START-HERE for the current
work, and name the earlier work in section 5 as not continued here.

## RESUME-PROMPT.md

Start from `assets/resume-prompt.md`: about 15 lines, at most 40. It names START-HERE.md by its absolute path (a
relative path breaks in a worktree or after a change of directory), tells the next session to stop when the branch
differs from section 1's, to run section 7, to go on with the first item of section 5, to ask before anything section
3 or 5 says is the user's, and to search the repository and memory before asking. It holds no fact START-HERE
doesn't: it only points there.

## TASKS.md and the session's plan file

Start from `assets/tasks.md` when TASKS.md doesn't exist; otherwise update it, never replace it. Mark what this
session finished as done, with its evidence (`- [x] Exporter written: commit 9f8e7d6, 12 tests pass (2026-10-05)`), and
list what is next with its next action. Keep the last 20 done entries; move older ones, oldest first, to
`TASKS-archive.md` in the same folder (create it with a `# Tasks archive` heading), which TASKS.md names once.

When the session keeps a plan, task or checkpoint file of its own (one the project's instructions, memory or the
conversation names), tick its checkpoints with their evidence too, and list it in START-HERE section 4 as the source
of truth for the steps it lists; TASKS.md then holds only what that file doesn't. Change no other project file.

## Running the checker

Run it as a command of its own, with the project root:

```bash
python3 <skill folder>/scripts/check_handoff.py --root <project root> devforgeai/handoff/<branch>
```

- Exit 0: no problem (warnings may remain; fix a warning when it is cheap).
- Exit 1: fix each problem in the file and line it names, then run it again: at most three runs in all. Never change
  a correct reference only to satisfy the script (mark it `(not yet created)` or `(session-only)` when that is
  true). Problems left after the third run go into the report.
- Exit 2: the folder wasn't written. Write the files and run it again.
- When the script can't run (no `python3`), say so, and read the files back against the whole self-check, the
  script's items included.

After the script, read the files back against the self-check's other items (4 to 9).

## When writing fails

When the handoff folder can't be written, say so, quoting the error, and give the files' content in the reply
instead, so the user can save them.

## The self-check

For all three files; the script checks the items marked (script), the session reads back for the rest:
1. every required heading in order, no `[[fill:` left, RESUME-PROMPT within 40 lines naming START-HERE.md by its
   absolute path (script);
2. every §2 bullet ends `[checked: …]` or `(unverified)`, every `### Decided` bullet holds a date and a quote, every §5
   item holds `Next:` and `Waits for:` (script);
3. every §4 path and every Markdown link exists, or its line or the line above says `(not yet created)` or
   `(session-only)` (valid only until the session ends) (script);
4. exact identifiers: commit hashes, branch names, pull request numbers, versions, document and item IDs, test counts
   with the command that gave them;
5. absolute dates, never "today" or "yesterday" (the script warns);
6. names, not pronouns whose referent the next session can't see ("PR #91", not "the PR");
7. each outstanding item's next action concrete enough to do without asking;
8. nothing secret: no token, key or password, even one said in the conversation;
9. START-HERE within about 250 lines, pointing to files instead of copying them (the script warns past 250).
