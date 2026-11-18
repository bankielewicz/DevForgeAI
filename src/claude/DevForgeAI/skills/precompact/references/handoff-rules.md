# Handoff rules

The next session may start cold: after `/compact` it has only a summary, and in a new session it has nothing. It
can read files and run commands, but it can't see this conversation. Write so that it can act without asking about
anything this session knew: full fidelity, zero ambiguity, and pointers instead of copies. SKILL.md has the steps;
this file has what goes in each section, with examples, and the self-check.

## The folder

- The handoff folder is outside the repository, in the user's home folder:
  `<home>/.devforgeai/<project>/handoff/<session>/`, `<project>` being the main checkout's folder name and a short
  hash of its path. Every worktree of a repository shares it, so a handoff outlives a worktree that is removed
  and a session started anywhere in the project can find it. `scripts/handoff_paths.py` prints the path (SKILL.md
  step 1); don't work it out by hand.
- The fallback folder, `devforgeai/handoff/<session>/` under the project root, is used only when the Write to
  the handoff folder is refused. It needs `devforgeai/handoff/.gitignore` holding the line `*`: the handoff is
  working notes for the next session on this machine, never committed. A handoff there stays with its checkout.
- A handoff folder nobody has written for 30 days is deleted by the script (the user's
  `<home>/.devforgeai/config.json` may set `handoffRetentionDays`; 0 keeps everything). The session deletes none.
- This session's own folder holds
  `START-HERE.md`, `RESUME-PROMPT.md`, `TASKS.md`, and `TASKS-archive.md` once TASKS.md has more than 20 done
  entries (create it with the heading `# Tasks archive`).
- Several sessions may work in one project at once, on one branch or several. Each writes only its own folder,
  so none overwrites another's handoff. Every other handoff folder, in the user's `.devforgeai` folder or in a
  project's `devforgeai/handoff/` (earlier versions of this skill wrote there, per branch), is read-only for
  this session: don't write, move, tidy or delete one, however old it looks.
- A path named in section 4 or in a Markdown link must exist. Mark one that will exist later `(not yet created)` on
  its line, and one valid only until the session ends (a scratch file) `(session-only)` on its line or the line
  above. Give evidence as text (a commit hash, a PR number), not as links, so an old entry never points at a file
  since removed.

## START-HERE.md, section by section

Start from `assets/start-here.md`. Replace every `[[fill: ...]]`; delete a line the fill says to delete when it
doesn't apply. More `##` sections may follow section 7; `###` headings may go anywhere.

**1. What this is.** Two or three sentences a stranger understands, then the project root, the work's branch (with
its worktree's path when the session works in another worktree, and the checkout the session runs in), the time
written (UTC) and the session ID (the folder's name, a `session-...` name included). Write another session's ID
nowhere in this section but inside the `Continues:` path. `Continues:` names the START-HERE.md of the handoff
carried over from another folder, by its path; keep the line on this session's later runs, and delete it when
nothing was carried over. `Other handoffs:` holds the script's `other:` lines (each
handoff's folder, date, branch and title), or says `none`, so the next session knows what other work of this
project is recorded and where, without this session having read it. When the session's
progress tracker has an open run, name it and its step.

**2. Verified state.** One fact per bullet, each ending with how it was checked, or `(unverified: <source>, <date>)`.
- Good: `- PR #12 is open as a draft [checked: gh pr view 12 --json isDraft -> true]`
- Good: `- 214 tests passed (unverified: the session's run of 2026-10-05)`
- Good: `- git isn't used: its top level is a parent folder [checked: git rev-parse --show-toplevel -> a parent folder]`
- Good: `- src/export.py: the delimiter parameter, unfinished; finish it, then commit [checked: git diff --stat -> 1 file]`
- Bad: `- Tests pass` (which tests, checked how, when?)

**3. Decisions.** Under `### Decided`, each decision with who decided, the date and their words in double quotes:
`- CSV only, no Excel: Dana, 2026-10-04, "CSV is enough for now"`. With nothing decided, the line `None.` without a
dash. A fact or a learning the user states is no decision: it goes to section 2 (marked how it was checked) or 6.
Under `### Open`, each question still the user's, with the options as the user saw them. Never move an open
question to Decided because it seems settled, and never write a decision to fill the section: only the user's words
decide.

**4. Read first.** A numbered list; each item starts with the path in backticks, then why and when to read it. For a
long file, give the search after the path: ``2. `docs/design.md` - the export format; run `grep -n "delimiter"
docs/design.md` rather than reading it whole``. When the session keeps its own plan or task file, list it as the
source of truth for the steps it lists. End with the line "When something you need isn't here, search the repository
and memory before asking the user."

**5. Outstanding.** The user's note first, when the skill was given one. Then a numbered list in order:
`1. Fix the delimiter. Next: edit src/export.py:42. Waits for: nothing.` or
`2. Release. Next: ask the user which version. Waits for: the user's choice (section 3, Open).`
With nothing left, the single line `Nothing outstanding.`

**6. Rules, traps and learnings.** What cost time and how to avoid it, approaches tried and dropped with why, the
project rules that apply (cite the file, don't restate it), and this session's learnings. The durable ones also go to
memory (`references/memory.md`).

**7. Before acting.** Commands to run first, each with what it shows if nothing changed:
`- git log -n 1 --oneline - shows a1b2c3d`.

**Carrying over an earlier handoff.** There is one source, in this order: this session's own earlier START-HERE.md
(in the fallback folder, when an earlier run had to use it: name it on `Continues:`);
else the handoff the conversation shows this session resumed from, the START-HERE.md it was given at its start to
continue from and read (in any folder, a project's `devforgeai/handoff/` included). A session that was given no handoff and needs
one, for example after its worktree's session ended, finds it in the `other:` lines by branch and title. Keep what still holds: its decisions,
open questions, rules, traps and learnings, and its outstanding items not finished; drop what is done (TASKS.md
keeps it). A handoff carried over from another folder is copied, never changed: its files stay as they were.
- Good: this session was started with a resume prompt naming another folder's START-HERE.md and read it; its
  decisions go into this session's START-HERE, and section 1 says `Continues:` with that path.
- Bad: the branch's folder holds another session's handoff that this session never read; copying its decisions,
  or editing its TASKS.md, mixes two sessions' work.

When this session's own earlier handoff is about other work (the same session, another topic), keep its
TASKS.md entries under a `##` heading naming that work, after the required ones, write START-HERE for the current
work, and name the earlier work in section 5 as not continued here, in a line before the numbered list.

## TASKS.md

Mark what this session finished as done, with its evidence
(`- [x] Exporter written: commit 9f8e7d6, 12 tests pass (2026-10-05)`), and list what is next with its next action.
Update this session's own earlier TASKS.md, never replace it; on the first run of a session that resumed from
another handoff, copy that handoff's entries in first; keep the last 20 done entries and move older ones, oldest first, to
TASKS-archive.md.

## The checker's warnings

Exit 0 can come with warnings: START-HERE over 250 lines, or `today`, `yesterday`, `tomorrow` or `recently` outside
quotes and code. Fix a warning when it is cheap (write the date; point to a file instead of copying it).

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
