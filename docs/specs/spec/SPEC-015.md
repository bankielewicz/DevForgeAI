---
id: SPEC-015
type: spec
title: "Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact"
status: approved      # draft | in-review | approved | superseded | deprecated
version: 4
created: 2026-10-05
updated: 2026-11-17
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a4f2ade8-0127-4b96-bc22-b3498b2ab3a9"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-10-05
upstream:
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 11, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 11, hash: null, note: "decisions stay the user's: the handoff records who decided what, in their words, and never turns outstanding work into a decision"}
  - {id: SPEC-013, relation: informed_by, version: 28, hash: null, note: "BEH-02 (versions 18 and 19): an untracked skill opens no run, and the turn that loads it records no further tool event or reply in the open run, so the handoff can be written in the middle of a tracked run"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/precompact", "src/tests/precompact", "src/claude/DevForgeAI/evals/precompact", "src/schemas/skill-frontmatter.schema.json", "CLAUDE.md"]
---

# SPEC-015 — Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact

> **Status:** version 4 approved by Bryan on 2026-11-17, not built: the handoffs move out of the repository to
> `~/.devforgeai/<project>/handoff/<session>/`, with a fallback in the project, pruning after 30 days and a rule
> for shared plan files (Bryan, 2026-11-17, §13). Version 3 approved by Bryan on 2026-11-17, built as a draft
> (SKL-012 v2, PR #167) and never deployed: one handoff folder per session, under its
> branch, which no other session writes, and memory changed only by adding (Bryan, 2026-11-17, §13); SKL-012 v1,
> the skill deployed today, implements version 2. Version 2 approved by Bryan on 2026-10-05 (version 1 the same day); SKL-012 v1 merged in PR #93 (`909a252`) and
> deployed as plugin 0.26.0; version 2 fixes §5's description,
> which the build found holding `<branch>`, refused by the frontmatter schema, and §4's project root, which
> contradicted ERR-01. The drafting plan and its checkpoints
> are in `tmp/plans/2026-10-05-precompact.md` (local); the review is `tmp/plans/precompact/review-drafts.md` (local).

## 1. Overview

When a Claude Code session's context window fills, its owner runs `/compact`, and the next part of the session starts
from a summary: it may start cold, or with gaps. Bryan's practice until now has been to paste, before each `/compact`,
a request to save what the session learned to memory and to write a document the next session can start from. This
skill does that in one command, `/devforgeai:precompact`.

Bryan, 2026-10-05: "the goal of this skill is to save me from copying & pasting in sessions when context windows grow
above 80-90% asking them to save newfound learnings to memory then create a tasks.md or start-here.md document in
full-fidelity, zero ambiguity for the next session for when I run /compact. the document is to reference files, etc...
as the next session may start cold or have amnesia due to /compact. it is not meant to run between skills although
eventually, it may run with the precompact hook." And: "ensure the resume prompt or start-here.md document is in
full-fidelity, zero ambiguity for next session. include but not limited to 'progressive disclosure' style where
applicable to reference documents or have it search repo when necessary." His original request also said: "if you're
keeping a tasks.md related to the design and architecture of devforgeai, update it with progress checkpoints."

The skill, in this order, so that a session cut off midway still leaves the most important file:
1. checks the live state of the work cheaply (branch, commits, uncommitted changes, open pull requests), so the
   handoff states facts, not recollections;
2. writes the master document, `START-HERE.md`: what the work is, its verified state, the decisions and who made them,
   what to read first and why (pointing to files and searches rather than copying them: progressive disclosure), what
   is outstanding and its next action, the traps and the learnings, and a check to run before acting;
3. writes `RESUME-PROMPT.md`, about 15 lines the owner pastes after `/compact`, sending the next session to START-HERE;
4. updates `TASKS.md`, the checkpoint list, and ticks the session's own plan or task file when it keeps one;
5. saves the new, durable learnings to memory, in the format the session's own instructions give;
6. checks the files with a bundled script, fixes what it reports, and reports.

The files live outside the repository, in `~/.devforgeai/<project>/handoff/<session>/` (version 4; on Windows the
same folder under the user's profile), one folder per session, so a handoff outlives a worktree that is removed and
a session started anywhere in the project can read it; a folder nobody has written for 30 days is pruned. Where
that folder can't be written, the files go to `devforgeai/handoff/<session>/` in the project (gitignored). A
session writes only its own folder and never changes another's, so sessions working at the same
time, on one branch or on several, can't overwrite each other's handoff (version 3; until version 2 the folder was
the branch's, and two sessions with work on one branch rewrote the same three files). The skill works in any project that uses DevForgeAI: it
uses the project's own instructions, and its text names no machine, tab or path of this repository. The progress
tracker ignores the skill (SPEC-013 BEH-02, version 18): running it in the middle of a brainstorm or architecture run
leaves that run open and records nothing of the handoff's work in it.

**When to run it.** The skill spends context too: its instructions load, and the files take room to write. Run it at
70 to 80 percent of the context window, not later; with automatic compaction off, a run that hits the limit stops
midway, and the order above keeps START-HERE.md, written first.

**What this can't guarantee.** The handoff is only as good as what the session can still see: what scrolled out of
the context before the skill ran is lost unless it reached a file, memory or the conversation summary. The script
checks structure and references; whether a fact is the right one to keep is the session's judgment. Evals can't see
memory (the eval sandbox seals the home folder), so saving to memory is checked live (VER-07).

## 2. Constraints

- **PRD-001 NFR-001 to NFR-003** (v11): SKILL.md is at most 500 lines and its description at most 1024 characters;
  the frontmatter validates against `skill-frontmatter.schema.json` and `skill.schema.json`; the skill has a
  `claude plugin eval` suite against the no-plugin baseline at 0.8 or above per case over 3 runs, unless Bryan records
  a waiver in §9. He decided one run per case ("Full cycle, 1-run evals", 2026-10-05); §9 records it at approval.
- **ADR-001** (v4): built in a worktree from `src/claude/DevForgeAI/`; the owner deploys; evals run from a plain
  terminal.
- **Decisions stay the user's** (PRD-001 FR-003, informed_by). The handoff records each decision with who made it and
  their words; it never records outstanding work as decided. The skill asks the user nothing: what it can't establish
  goes into START-HERE §3 as an open question.
- **No requirement in PRD-001 covers a pre-compaction handoff.** This spec follows Bryan's decision of 2026-10-05
  directly; whether PRD-001 gains such a requirement is his decision (§13).
- **No hand-offs.** No skill hands off to this one and it hands off to none (Bryan: "not meant to run between
  skills"); its next step is the user's `/compact`.
- **Generic.** The plugin ships to every user, so the skill's text names no machine, terminal tab, person or path of
  this repository; what a project needs comes from that project's instructions and files.
- **The progress tracker** (SPEC-013 v19, informed_by): BEH-02 tracks every plugin skill except one whose SKILL.md
  metadata has `devforgeai-tracked: "false"`; this skill is the first.
- **Standard library only** for the check script, like `validate_brn.py` and `find_spec.py`: it runs under
  `python3 -S`.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/precompact/
├── SKILL.md                    # the checklist (BEH-01 to BEH-09), when to run it, what it never decides
├── provenance.yaml             # SKL-012, implements SPEC-015
├── scripts/
│   ├── check_handoff.py        # IF-01: checks a handoff folder (BEH-08); standard library only
│   └── handoff_paths.py        # IF-02 (version 4): the store's folder, the fallback, other handoffs, pruning
├── references/
│   ├── handoff-rules.md        # the full-fidelity rules section by section, the self-check list (§4), examples
│   └── memory.md               # what counts as a learning worth saving, and how to save it
└── assets/
    ├── start-here.md           # the START-HERE.md template (DM-01)
    ├── tasks.md                # the TASKS.md template (DM-02)
    └── resume-prompt.md        # the RESUME-PROMPT.md template (DM-03)
src/claude/DevForgeAI/evals/precompact/<case>/  # one case per automated VER item (§9)
src/tests/precompact/                           # check_handoff.py's tests, test_structure.py, make_evals.py
src/schemas/skill-frontmatter.schema.json       # metadata devforgeai-tracked: const "false" (a typo fails validation)
CLAUDE.md                                        # the skill table row (this repository only)
```

```mermaid
flowchart LR
    S[/devforgeai:precompact] --> V[Check state BEH-02]
    V --> H[START-HERE.md BEH-03]
    H --> R[RESUME-PROMPT.md BEH-04]
    R --> T[TASKS.md, the plan file BEH-05]
    T --> M[Memory BEH-06]
    M --> C[check_handoff.py BEH-08]
    C -->|problems, at most 3 runs| H
    C -->|clean| P[Report BEH-09]
```

## 4. Data model

**The project root** is the folder the session started in (its working directory then, not a folder a later `cd`
moved the shell to), or a folder holding it that the user names as the project. When git's top level for it is
another folder, a parent repository that isn't the project's (such as a home folder kept in git), git isn't used for
it (ERR-01). START-HERE §1 states the root, and every path the skill writes or checks is under it unless written
absolute.

**The work's branch** is the branch of the worktree the session's work is in: the one it edits or commits to (for
example with `git -C .claude/worktrees/<name>`), or, when it works in its own checkout, that checkout's branch. With
work in several worktrees, it is the one with the outstanding work, and START-HERE §1 names the others (version 2;
Bryan, 2026-10-05: "Folder follows the work's branch", on a side note that sessions running on `main` and editing
worktrees would all share `main`'s folder). The state checks (BEH-02) run in that worktree.

**The store** (version 4; Bryan, 2026-11-17: "a place that's 'more durable' that gets pruned", "if a worktree is
deleted or pruned or session starts in the project folder, it will be able to read the files") is
`<home>/.devforgeai/`, `<home>` being the user's home folder (`~` on Linux and macOS, `C:\Users\<user>` on Windows;
Python's `os.path.expanduser("~")`). `<home>/.devforgeai/config.json`, when it exists, holds the settings (below).

**The project's key**, `<project>`, is the name of the project's main folder and the first 8 hexadecimal
characters of the SHA-256 of that folder's absolute path, joined by `-` (`DevForgeAI-3f9a1c2e`; Bryan, 2026-11-17,
"Folder name plus short hash (Recommended)"). The main folder is the main checkout of the repository the project
root is in (the folder holding git's common directory, `git rev-parse --path-format=absolute --git-common-dir`), so
every worktree of one repository has one key and a separate clone has its own; where git isn't used for the
project (ERR-01), it is the project root. In the name, each run of characters other than letters, digits, `.`, `_`
and `-` becomes `-`.

**The handoff folder** is `<home>/.devforgeai/<project>/handoff/<session>/` (version 4; in version 3,
`<root>/devforgeai/handoff/<branch>/<session>/`). There is no branch level: START-HERE §1 names the branch. Nothing
but handoff folders is kept under `handoff/` (Bryan, 2026-11-17, "Add handoff/ (Recommended)"), so other data may
later live beside it. **The fallback folder** is `<root>/devforgeai/handoff/<session>/`, used only when the
handoff folder can't be written (ERR-08). `<session>` is the session's ID, which Claude Code substitutes for `${CLAUDE_SESSION_ID}` in
SKILL.md; when it arrives unsubstituted or empty, `session-<YYYYMMDDTHHMMSSZ>` from the first run's `date -u`, and
a later run of the same session uses the folder the conversation shows it wrote before.

**One rule for writing** (version 3; Bryan, 2026-11-17, "Per session (Recommended)"): a session writes handoff
files only in its own folder. Every other handoff folder is another session's and is only read: another session's
folder in the store or in a project's `devforgeai/handoff/`, and the folders and files versions 1 to 3 wrote there
(`<branch>/` with the three files, `<branch>/<session>/`). The session never moves, merges or deletes one; only
IF-02's pruning deletes, by age.

**Pruning** (version 4; Bryan, 2026-11-17, "30 days, configurable (Recommended)"). IF-02 deletes a folder directly
under `<home>/.devforgeai/<project>/handoff/` when it is a real directory (not a link), holds a START-HERE.md, isn't
the running session's, and no file in it has been written for `handoffRetentionDays` days: the number in
`<home>/.devforgeai/config.json` ("~/.devforgeai/config.json (Recommended)"), 30 when the file or the key is
absent or isn't a number, and never when it is 0. Nothing in a project's `devforgeai/handoff/` is pruned. Pruning is
best effort: a folder that can't be deleted is left and named, and the run goes on.

**The handoff carried over** is, in this order: the earlier files of the session's own folder; else the handoff
the conversation shows this session resumed from (the START-HERE.md whose path it was given and read, in any
folder, the old layout's included). Its content that still holds is copied into the session's own files, and the
source is left as it was. A handoff the session didn't resume from is never carried over, whatever its branch.
When the fallback folder is used, `<root>/devforgeai/handoff/.gitignore` holds `*`, as the tracker's
`devforgeai/progress/` does (SPEC-013 BEH-15): the handoff is working notes for the next session on this machine,
not a project document. The store needs none.

The files are Markdown with fixed second-level headings, which IF-01 checks; more `##` headings may follow the last
required one, and `###` headings may appear anywhere. A value the template leaves to fill has the form `[[fill: what]]`,
the only placeholder form; IF-01 refuses any left in a written file.

**DM-01. START-HERE.md**, the master document. Its headings and line shapes, in order:

| Heading | Holds |
|---|---|
| `## 1. What this is` | the work in two or three sentences; the project root; the work's branch, with its worktree's path when that isn't the root, and the checkout the session runs in; the date and time written (UTC) and the session that wrote it; `Continues:` with the path of the handoff carried over from another folder, when there is one; `Other handoffs:` with IF-02's listing of the project's other handoffs, in the store and in the project's `devforgeai/handoff/` (each with its folder, the date it was written, its branch and its title; the 10 newest), or `none`; the session reads none of them |
| `## 2. Verified state` | facts checked while writing (BEH-02), one per bullet, each ending `[checked: <command> -> <what it showed>]` or `(unverified)` with where the fact came from and its date |
| `## 3. Decisions` | `### Decided`: each decision as a bullet with who decided, the date as YYYY-MM-DD and their words in quotes; `### Open`: the questions still the user's, each with the options as the user saw them |
| `## 4. Read first` | a numbered list, each item starting with the path in backticks, then why and when to read it; searches to run (`grep -n "<term>" <path>`) where a file is too long to read whole; a closing line: when something needed isn't here, search the repository and memory before asking the user |
| `## 5. Outstanding` | a numbered list in order, each item `N. <what>. Next: <a command, a file:line or a question>. Waits for: <what, or nothing>.`; the user's note (the skill's argument) first when given; or the single line `Nothing outstanding.` |
| `## 6. Rules, traps and learnings` | what cost time and how to avoid it; the project's rules that apply, cited, not restated, when a file already holds them; the session's new learnings (BEH-06 saves the durable ones to memory) |
| `## 7. Before acting` | commands to run first, each with what it should show if nothing changed since the handoff |

**DM-02. TASKS.md**, the checkpoint list: `## Done` and `## Next`. Each entry is a checkbox line naming the step, then
its evidence (commit, pull request, file, test result with its date) or its next action. The session's own earlier TASKS.md is
updated, never replaced, and on the first run of a session that resumed from another handoff its entries are
copied in first (the handoff carried over); past 20 done entries, the oldest move to `TASKS-archive.md` in the same folder, which TASKS.md
names once and RESUME-PROMPT.md doesn't send the next session to.

**DM-03. RESUME-PROMPT.md**, about 15 lines and at most 40, with no required headings: the work in one sentence; the
absolute path of START-HERE.md, to be read first, then TASKS.md; to stop and tell the user when the work's branch (checked
in the worktree §1 names, `git -C <worktree> branch --show-current`) isn't the one START-HERE §1 names; to run START-HERE §7; to go on with the first item of §5, asking the user before
anything §3 or §5 says is theirs; and, when something needed isn't in the handoff, to search the repository (with the
project's spec lookup where it has one) and the memory index before asking.

**The self-check** (BEH-08), for all three files; IF-01 checks the items marked (script), the session reads back for
the rest:
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

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: precompact
description: Prepares a Claude Code session for /compact, so the next session can continue with nothing pasted by hand. It writes a full-fidelity handoff outside the repository, in the user's .devforgeai folder, one folder per project and session, which no other session writes (START-HERE.md with the verified state, decisions and who made them, files to read first and the work outstanding; TASKS.md; a short RESUME-PROMPT.md to paste after compacting), ticks the session's plan file, and saves the session's new learnings to memory. Use before running /compact, ideally at 70 to 80 percent of the context window, or when asked to save learnings and write a handoff, start-here document or resume prompt for the next session after compacting. Not for project documentation, release notes, commit messages or a backlog.
argument-hint: "[note for the next session]"
metadata:
  devforgeai-id: "SKL-012"
  devforgeai-version: "<SKL-012's provenance.yaml version, quoted>"
  devforgeai-tracked: "false"
```

- **The name is `precompact`,** so the command is `/devforgeai:precompact`. Claude may also load it when the user asks
  for what the description says. An argument is a note for the next session; START-HERE §5 puts it first.
- **Tools the instructions use:** Bash for read-only checks and to run the script; Read; Write and Edit for the handoff
  files, the `.gitignore`, the session's plan or task file (BEH-05) and memory files. No AskUserQuestion: the skill asks
  nothing (§2).
- **Downstream contract:** the next session (after `/compact`, or a new session) needs only RESUME-PROMPT.md's text.

| Item | Command | Behaviour |
| --- | --- | --- |
| IF-01 | `python3 check_handoff.py [--root DIR] [--session ID] HANDOFF_DIR` | Checks the handoff folder `HANDOFF_DIR` (relative to `DIR`, which is `.` by default) against the self-check's script items (§4), reading only START-HERE.md, RESUME-PROMPT.md and TASKS.md (never TASKS-archive.md or another file): the three files exist; START-HERE.md and TASKS.md have their headings in order (DM-01, DM-02); RESUME-PROMPT.md has at most 40 lines and holds the absolute path of `HANDOFF_DIR/START-HERE.md` as a whole path (not part of a longer one); no file holds `[[fill:` outside code (a code span or a fenced block quotes the form; the assets never put a placeholder in backticks); §2's bullets, §3's `### Decided` bullets and §5's items have their shapes (DM-01): a §2 bullet's own text, before any nested list and with emphasis marks ignored, ends with its marker; a `### Decided` bullet may instead be `- None.`; §5 has at least one item or a line starting `Nothing outstanding`; an item runs on over indented lines, blank lines and fences; each path a reference names exists, a reference being a Markdown link's target that isn't a URL, an anchor or `mailto:`, or the first backticked token of an item of START-HERE §4, read after removing a trailing `:LINE`, `:LINE-LINE`, `:LINE:COL` or `#Lnn` (a link's target also URL-decoded), expanding a leading `~/` and any set variable, and resolved against `DIR`, or beside the file that names it, when relative (a link starting `/` may also be read from `DIR`), unless its line or the line above says `(not yet created)` or `(session-only)`, or, for a §4 item, any of the item's lines does; a path holding a variable that isn't set isn't checked; no other backticked text is checked; when `HANDOFF_DIR` is under `DIR/devforgeai/handoff/` (the fallback folder, or a folder of versions 1 to 3), `DIR/devforgeai/handoff/.gitignore` holds `*` (not checked for a folder in the store, version 4); with `--session ID` (version 3), `HANDOFF_DIR`'s last path component is `ID`, and the line of START-HERE §1 that holds `by session` names `ID` and no other session (a problem each: the folder is another session's, or the file was written by another); without `--session` neither is checked, so a folder of the old layout checks as before. Prints one line per problem, `<file>:<line>: <problem>` (line 0 for the file as a whole), and per warning, `<file>:<line>: warning: <text>` (START-HERE over 250 lines; `today`, `yesterday`, `tomorrow` or `recently` outside quotes and code), then `handoff: clean` when there is neither, else `handoff: <n> problems, <m> warnings`. Exit 0 with no problem (warnings allowed), 1 with problems, 2 when it can't run (`HANDOFF_DIR` missing or unreadable) |
| IF-02 | `python3 handoff_paths.py --root DIR --session ID [--home DIR] [--no-prune]` | (Version 4.) Names where this session's handoff goes and what else the project has, and prunes. It writes nothing but what pruning deletes, and creates no folder. Prints, one per line: `project: <key>` (§4); `session: <name>`, which is `ID`, or `session-<YYYYMMDDTHHMMSSZ>` when `ID` is empty or begins with `${`; `folder: <the handoff folder's absolute path>`; `fallback: <the fallback folder's absolute path>`; `other: <folder's absolute path> | <YYYY-MM-DD of its newest file> | <branch> | <title>` for each other handoff of the project, newest first and at most 10, taken from the store's `handoff/` and from `DIR/devforgeai/handoff/` (a folder there with START-HERE.md in it or one level below), the branch and the title read from START-HERE.md's first `# ` line and §1's `Branch:` line, `?` when missing; `pruned: <folder>` for each folder deleted (§4, Pruning), or `prune: skipped: <reason>` when a folder couldn't be deleted or `--no-prune` was given. `--home` replaces the user's home folder (tests). Exit 0 unless `DIR` isn't a folder (exit 2). Standard library only: it runs under `python3 -S` |

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Run when the user types /devforgeai:precompact or asks, before /compact, to save the session's learnings and write a handoff, start-here document or resume prompt for the next session. Work through the checklist in order (BEH-02 to BEH-09) in the main conversation: a subagent can't see the conversation the handoff summarizes. Ask the user nothing; put what can't be established into START-HERE §3 as open. The progress tracker ignores this skill (SPEC-013 BEH-02, version 18): a tracked run open in the session stays open, and the handoff names it with its step (from the tracker's current.json for the session, when it exists)."
  - id: BEH-02
    status: active
    rule: "Check the live state first, cheaply and read-only: don't re-read what the session already holds (its CLAUDE.md files and the memory index are in its context); run python3 ${CLAUDE_SKILL_DIR}/scripts/handoff_paths.py --root <project root> --session <session> (IF-02) once, as a command of its own, for the handoff folder, the fallback folder and the listing of other handoffs; read only the earlier files of the session's own handoff folder and, when the session resumed from another handoff, that handoff's files (§4, the handoff carried over), and none of the others listed. Keep each command's output small: the branch and its upstream (GIT_OPTIONAL_LOCKS=0 git status --porcelain=v2 -b), the last commits (git log -n 5 --oneline), uncommitted changes (git diff --stat and git diff --stat --cached), open pull requests where gh works (gh pr list --limit 10). Run no test or build command: cite the last result the session saw, with its date and (unverified), unless the user's argument says to run one. Write, move or delete nothing in any other handoff folder, in the store or in a project (§4, one rule for writing); deleting old folders is IF-02's alone. A fact the session believes but didn't check now goes into the handoff marked (unverified)."
  - id: BEH-03
    status: active
    rule: "Write START-HERE.md (DM-01) from the template assets/start-here.md in one write, first of the files, so a session cut off later still leaves it: with the Write tool, to the handoff folder IF-02 names, which the write creates. When that write is refused (ERR-08), write it to the fallback folder instead, with devforgeai/handoff/.gitignore holding * written first when it is missing, and use that folder for the rest of the run. Carry over what still holds (decisions, open questions, rules, traps and learnings, outstanding items not finished) from the handoff carried over (§4): the session's own earlier START-HERE, else the one it resumed from, which is read and left unchanged and named in §1's Continues line. Carry over nothing from a handoff the session didn't resume from. Write in full fidelity (the self-check, §4). Use progressive disclosure: name files with why and when to read them, and searches to run, instead of copying their content; copy in only what exists nowhere else (a decision said only in the conversation, a result not saved to a file). Quote the user's words for each decision, with the date. Put the user's argument, if any, first in §5. Never write a secret: no token, key or password, even one said in the conversation."
  - id: BEH-04
    status: active
    rule: "Write RESUME-PROMPT.md (DM-03) from the template assets/resume-prompt.md: about 15 lines and at most 40, naming START-HERE.md by its absolute path, with the branch check, the 'Before acting' step, the first outstanding item, asking before any decision §3 or §5 says is the user's, and searching the repository and memory before asking."
  - id: BEH-05
    status: active
    rule: "Update the session's own TASKS.md (DM-02), written from the template assets/tasks.md when it doesn't exist, with the entries of the handoff carried over copied in first (§4): mark what this session finished as done, with its evidence (commit, pull request, file or test result with its date), and list what is next with its next action; keep every done entry, moving the oldest past 20 to TASKS-archive.md. When the session keeps a plan, task or checkpoint file of its own (one the project's instructions, memory or the conversation name), tick its checkpoints with their evidence too, and name it in START-HERE §4 as the source of truth for the steps it lists; TASKS.md then holds only what that file doesn't. Other sessions may share that file (a backlog, a plan), so change it only by adding (version 4; Bryan, 2026-11-17, 'Yes, add it to v4 (Recommended)'): read it again immediately before changing it; with Edit only, tick the checkpoints this session finished and add their evidence; never use Write on it; never rewrite, reorder or delete an entry, and never tick or change one this session didn't work on."
  - id: BEH-06
    status: active
    rule: "Save the session's new, durable learnings to memory when the session's instructions describe a memory system (a memory location and its format): follow that format exactly (for example, in Claude Code's memory, one fact per file with its frontmatter, an index line), update an existing memory that covers the same fact rather than adding a duplicate, and save only what the repository and its instructions don't already record: decisions with their reasons, verified facts about tools and the environment, practices the user asked for or confirmed, and traps that cost time. Never save a secret. Memory is shared by every session of the project, so change it only by adding (version 3; Bryan, 2026-11-17, 'Yes, add rules (Recommended)'): read a memory file or the index again immediately before changing it; change an existing one only with Edit, adding lines or amending lines this session wrote; never use Write on an existing memory file or on the index; never delete, reorder or reword what another session wrote, and when that content is wrong or out of date, add a dated line saying so. When the session has no memory system, a memory write is refused, or an Edit fails because the file changed, the learnings stay in START-HERE §6, and the report says so."
  - id: BEH-07
    status: active
    rule: "Never turn outstanding work into a decision: an item waiting for the user's choice says so under ### Open, with the options as the user saw them, and the handoff records no choice the user didn't make."
  - id: BEH-08
    status: active
    rule: "Run python3 ${CLAUDE_SKILL_DIR}/scripts/check_handoff.py --root <project root> --session <session> <the folder written, by its absolute path> (IF-01) as a command of its own. On exit 1, fix each problem it lists in the file it names, and run it again, at most three runs in all; never change a correct reference only to satisfy the script. Problems left after the third run go into the report. On exit 2, the folder wasn't written: write the files and run it again. Then read the files back against the self-check's other items (§4, and references/handoff-rules.md)."
  - id: BEH-09
    status: active
    rule: "Report in the reply: the folder and the files written, the plan or task file ticked, the memories saved or updated (or why none), anything left marked (unverified), any problem the script still reports, and the text of RESUME-PROMPT.md in a fence longer than any fence inside it, so the user can paste it after /compact. Say which folder holds the handoff, and when it is the fallback, why. Change no file but the files of the session's own handoff folder, devforgeai/handoff/.gitignore when the fallback is used, the plan or task file BEH-05 names (by its rules) and memory files (BEH-06's rules)."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "git reports an error for the project folder, git isn't installed, or the repository git finds is a parent of the project folder (its top level, git rev-parse --show-toplevel, isn't the working directory or a folder holding it that the user named); or gh isn't available or fails"
    handling: "Skip those checks, use the folder no-git when there is no usable branch, say in START-HERE §2 what couldn't be checked, and mark the facts that depend on it (unverified)"
    user_result: "A handoff that says what couldn't be checked"
  - id: ERR-02
    status: active
    condition: "Neither the handoff folder nor the fallback folder can be written"
    handling: "Say so, quoting the error, and give the files' content in the reply instead, so the user can save them"
    user_result: "The handoff in the reply"
  - id: ERR-03
    status: active
    condition: "check_handoff.py can't run (no python3)"
    handling: "Say so, and read the files back against the whole self-check (§4), the script's items included"
    user_result: "A handoff checked by reading, and the reason"
  - id: ERR-04
    status: active
    condition: "The session's instructions describe no memory system, or a memory write is refused"
    handling: "The learnings stay in START-HERE §6, and the report says why (BEH-06)"
    user_result: "The learnings in the handoff, and the reason"
  - id: ERR-05
    status: active
    condition: "The session's own handoff folder holds its earlier handoff of other work (the same session, another topic)"
    handling: "Keep its TASKS.md entries under a ## heading naming that work, after the required ones; write START-HERE for the current work, naming the earlier work in §5 as not continued here"
    user_result: "Both lines of work kept, the current one first"
  - id: ERR-06
    status: active
    condition: "The session is cut off (the context limit) before the skill finishes"
    handling: "Nothing to do in the run; the order (BEH-03 first) leaves START-HERE.md written; the next session, given its path, finishes the rest by running the skill again"
    user_result: "At least START-HERE.md"
  - id: ERR-07
    status: active
    condition: "The folder the skill is about to write isn't the session's own: its name isn't the session's ID (§4), or the START-HERE.md in it says in §1 that another session wrote it (another session's folder, or files of the old layout directly in <branch>/)"
    handling: "Write nothing there and change nothing in it. Use the session's own folder (§4), carrying the other handoff over only when this session resumed from it (§4), and say in the report which folder was left untouched"
    user_result: "The other session's handoff unchanged, this session's beside it"
  - id: ERR-08
    status: active
    condition: "The Write of START-HERE.md to the handoff folder in the store is refused (a sandbox that allows writes only in the project, a read-only home folder, an eval run)"
    handling: "Write the handoff to the fallback folder, <root>/devforgeai/handoff/<session>/, once and for the rest of the run, with devforgeai/handoff/.gitignore holding * (BEH-03); say in START-HERE §2 and in the report that the store couldn't be written and that this handoff stays with this checkout. Decide by the Write tool's result, never by a Bash test: either may be refused where the other isn't"
    user_result: "The handoff in the project, and the reason"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds the checklist, when to run it and what it never decides; the full-fidelity rules, the self-check and examples live in references/handoff-rules.md, the memory guidance in references/memory.md, the shapes in assets/; the skill's own context use stays small (SKILL.md under about 150 lines, references read only when needed)"
    measured_by: "SKILL.md line count (at most 500, target 150) and description length (at most 1024 characters)"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 11, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version"
    measured_by: "skill-frontmatter.schema.json and skill.schema.json, and comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 11, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged precompact and ver-NN, run against the no-plugin baseline at 0.8 or above per case over 3 runs, or as Bryan's waiver recorded in §9 says"
    measured_by: "claude plugin eval --threshold 0.8"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 11, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: this spec against `spec.schema.json` | Passes, with every BEH, ERR and QR item covered (checked 2026-10-05, version 1 draft) |
| Qualification (QR-03) | The 3-run bar is waived by Bryan, 2026-10-05: "Full cycle, 1-run evals (Recommended)"; one run of the suite is the record |
| Build (SKL-012 v1, approved) | Merged in PR #93 (`909a252`, 2026-10-06 00:37 UTC) and deployed as plugin 0.26.0 the same night (the deployed copy matches the source; `diff -rq` exit 0). On branch `docs/precompact` (draft PR #93) through `/plugin-dev:skill-development`, 2026-10-05: VER-01's tests first (`d9f8416`, 29 cases, seen failing), then `check_handoff.py`; VER-08's structure tests first, then SKILL.md, the three assets, `references/handoff-rules.md` and `references/memory.md`, provenance and the schema's const (`4944f5b`). The structure test found §5's description holding `<branch>`, which the schema refuses, and writing the no-git case found §4's project root contradicting ERR-01: both fixed in version 2 (draft). Bryan's side note decision ('Folder follows the work's branch', `a62e995`) is in version 2 too. skill-reviewer (`3420226`: an empty Decided list had no valid form; session ID, current.json and the UTC time; duplication in handoff-rules.md cut from 153 to 91 lines), plugin-validator (`3b7d6e8`: no-git named for a parent repository; the plugin description; evals.md) and an adversarial review with probes (`16183e2`: 13 valid shapes the checker refused, among them nested bullets under a checked fact, `(session-only)` on a wrapped item line, `- None.`, a loose item; it now reads only the three files; 42 tests; the checklist unnumbered so a reply's tick can't count for an open tracked run). `src/tests` 757 pass; kit 278 pass (SPEC-013 v18) |
| VER-01, VER-08 | Pass: `src/tests/precompact/test_check_handoff.py` 42 tests, normally and under `python3 -S`; `test_structure.py` 20 tests |
| Pilot (diagnostic, unbound) | `tmp/eval-results/precompact-pilot-20261005T190417`, writes-handoff 1 run, no baseline, 0.93, $0.45. The only failing grader was the commit hash: the premise check had committed its own scaffold.sh, so its hash differed (`a1f206a`: scaffolds commit only the files they name; head 905e9bb). It showed the memory branch an eval child takes: it has memory instructions, but its memory write is denied, so ERR-04's refused arm (§6 and the report) applies. The checker took two runs to clean, and the order grader was proven both ways on the real trace |
| VER-02 to VER-05 (1 run, with baseline) | `tmp/eval-results/precompact-v1-20261005T194821` (commit `1e76614`, digest `e2d7b5b9`): writes-handoff 1.00 (baseline 0.07), decisions-stay-open 1.00 (0.07), no-git 1.00 (0.00); updates-earlier-handoff 0.73 (0.55), its with-plugin arm failing only file_exists, which counts only files a run creates, on the scaffold's earlier files: graders fixed (`429873f`) and rerun in `tmp/eval-results/precompact-v1-ver03-20261005T195113` (commit `429873f`, digest `6bc11ee9`): 1.00 (0.75). $2.39 and $0.66 |
| VER-06 (1 run, with baseline) | `tmp/eval-results/precompact-v1-triggers-20261005T195400` (commit `429873f`, digest `6bc11ee9`): 8 of 8 at 1.00; the three positives load the skill, the five near-misses don't. $2.34. `--tag precompact-trigger` found no cases; `--case "precompact-trigger-*"` did |
| VER-09 | Met under the waiver: every case of VER-02 to VER-06 at 1.00 in one run. Total evaluation cost $5.84 with the pilot |
| Version 4 | Approved by Bryan on 2026-11-17 ('Approve as drafted'); drafted the same day on branch `docs/spec-015-v3` (PR #166); not built. VER-12 is new and not run; VER-11 gains (e) and (f). An eval run can't write its home folder (the pilot of 2026-10-05), so the cases of VER-02 to VER-05 and VER-10 reach the fallback folder, and their graders accept a Write to either folder. **Builder's readings 3 to 6** (the rebuild, 2026-11-17, from the reviews of `4d76e83`; for Bryan's accept or challenge): (3) `handoffRetentionDays` must be a finite number, so NaN and Infinity mean 30, and a positive value below 1 means 1 day, since a fraction of a day would delete live sessions' folders (§4 says only 'a number'); (4) IF-02 gains `--keep PATH`, repeatable, for the handoff the session resumed from, which is otherwise pruned before its entries are copied when it is older than the retention; (5) nothing is pruned when the store's `handoff/` is reached through a symbolic link (§4 speaks only of a linked session folder); (6) a folder whose age can't be read counts as new |
| Version 3 | Approved by Bryan on 2026-11-17 ('Approve as drafted'); drafted the same day on branch `docs/spec-015-v3` (PR #166); not built (SKL-012 v2). VER-01's and VER-08's new cases, VER-10 and VER-11 are not run; the cases of VER-02 to VER-05 are to be regenerated for the session's folder, whose name a grader can't know, so their content graders read the trace's Write calls. **Builder's reading 1** (SKL-012 v2, 2026-11-17, for Bryan's accept or challenge): IF-01's 'the line of START-HERE §1 that holds `by session`' is read as the statement that says who wrote the file, `Written ... by session <id>`, on one line or wrapped; `by session` elsewhere in §1 (prose about an earlier session) isn't read, since the skill-reviewer showed it would fail a session's own folder. **Reading 2:** with the `session-<time>` fallback, that folder name is the ID wherever one is asked for (§1's Written line and `--session`) |
| Build (SKL-012 v2, draft) | On branch `feat/precompact-skl-012-v2`, 2026-11-17, through `/plugin-dev:create-plugin` and `/plugin-dev:skill-development`: VER-01's `--session` cases and VER-08's new checks first, seen failing (`f0d00d9`: 5 checker cases, 7 structure checks), then `check_handoff.py`, SKILL.md, the references, the asset and provenance version 2 (`d9bad2a`), plugin 0.33.0 (`eefc1bc`), the cases regenerated with `leaves-other-session-handoff` (`d416d5b`), and one review-fix round (`933c802`). At `933c802`, run by a second session on a clean tree: `src/tests` 1743 passed, 1 skipped; kit 623 pass; both `claude plugin validate` runs pass; `git diff --check origin/main...HEAD` empty. skill-reviewer and plugin-validator on `933c802`: nothing critical, nothing blocking; their open minors and the one open warning are in `docs/process/plugin-workflow/reviews/` (the report named for `933c802`). That build implemented version 3 and was never deployed. **Rebuilt for version 4** the same day, in three more iterations: VER-12's tests first (`f750873`), `handoff_paths.py` and the skill's text (`4880b7e`), the cases regenerated with graders that accept either folder (`4d76e83`), and two review-fix rounds, each with its tests first (`b58476d`: the retention a finite number of at least a day, no pruning through a link, `--keep`; `921e165`: two crashes). At `921e165`, run by a second session on a clean tree: `src/tests` 1765 passed, 1 skipped; kit 623 pass; both `claude plugin validate` runs pass; `git diff --check origin/main...HEAD` empty; nothing created under the real `~/.devforgeai`. skill-reviewer and plugin-validator on `921e165`: nothing critical, nothing blocking; what is left open is in `docs/process/plugin-workflow/reviews/` (the report named for `921e165`). **Not run:** any paid eval (the regenerated graders were checked against simulated calls only, for both folders), VER-10, VER-11; no session has run the rebuilt skill. Not merged, not deployed |
| VER-07 (live) | worker1, `claude --plugin-dir` on a scratch copy of the build, 2026-10-05 (setup in the session's scratchpad, `v07-setup.sh`). (a) PASS in observe mode: with a brainstorm run open at step 3, `/devforgeai:precompact` added only its turn's start, replies and end to the run's log (42 → 48 events), no run-end, no switch line, current.json still step 3, band unchanged; enforce mode was ignored because the setup's preference file lacked `devforgeai_local: 1` (SPEC-013 VER-50 (c) covers enforce). (b) Memory on PASS: one new memory with its index line, no duplicate of the two the session had saved itself. Memory off (`autoMemoryEnabled: false`): the first run kept the learning in §6 but also appended it to the user's global papercuts log, a file outside BEH-09's list; fixed (`1e76614`: memory is the memory system only; another instruction's log is named in the report) and rerun: PASS, the log unchanged (same checksum), the learning in §6 only, the report naming the log. (c) Cold start PASS: after `/compact`, the pasted resume prompt checked the branch and §7 and went on with §5's first item, quoting §3; in a new session it quoted §3 Open's two unanswered questions with their options (written nowhere but START-HERE), then re-ran the brainstorm and continued it from step 3. Observed: two runs filed a learning the user stated under Decided; fixed in the skill text (`1e76614`) |

Each automated VER item has one eval case under `evals/precompact/`, tagged `precompact` and `ver-NN` and generated by
`src/tests/precompact/make_evals.py`. An eval run starts in an empty workspace (home/cwd, where home/ is itself a git
repository, `.claude/rules/evals.md`) with no earlier conversation, so each case's scaffold builds the work to hand off
(its own git repository with commits whose author, committer and dates are fixed, so their hashes are known; a plan
file; an unfinished task) and its prompt states what the session did, as a user would before compacting. Graders are
regexes on the written files and the trace, `tool_used` with `input_match`, and an `llm` grader on the reply only; no
grader runs a script, so check_handoff.py's verdict is graded as its call and its printed `handoff: clean` line. Eval
runs offer no AskUserQuestion and seal the home folder, so memory is checked live (VER-07); a `--keep-temp` pilot
before the suite shows which memory branch (BEH-06) an eval child takes, and VER-02's grader accepts the one it shows.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "src/tests/precompact/test_check_handoff.py, every case normally and under python3 -S. A complete handoff exits 0 with 'handoff: clean'. A valid handoff holding the forms references take in practice also exits 0: commands, globs, URLs, slash commands, branch names with '/', versions, ~/ paths, path:LINE and path#Lnn references, <...> command templates, all in backticks, and a reference marked (session-only) on the line above. Each of a missing file, a missing or misordered heading, a §2 bullet with no [checked: or (unverified), a ### Decided bullet with no date or no quote, a §5 item with no Next: or no Waits for:, an empty §5, a 41-line RESUME-PROMPT.md, one without START-HERE.md's absolute path, a leftover [[fill:, a §4 path or a link target that doesn't exist, a missing .gitignore, and, with --session, a HANDOFF_DIR whose last component isn't the ID or a START-HERE §1 'by session' line naming another session, exits 1 with a '<file>:<line>: <problem>' line; with --session and both matching, and without --session for a folder of the old layout, the complete handoff still exits 0; a START-HERE over 250 lines and the word yesterday outside quotes give warnings and exit 0; a missing HANDOFF_DIR exits 2"
    level: unit
    covers:
      - IF-01
      - BEH-08
  - id: VER-02
    status: active
    obligation: "Case writes-handoff: a scaffolded git repository on branch feat/export with three commits (fixed author, committer and dates), a plan file with checkpoints and an unfinished task; the prompt says what the session did and asks to prepare for /compact. Graded: one folder, the session's in the store or the fallback's devforgeai/handoff/<session>/, receives START-HERE.md, TASKS.md and RESUME-PROMPT.md (the Write calls: neither the folder's name nor which of the two it is is known to a grader), and when it is the fallback devforgeai/handoff/.gitignore holds *; handoff_paths.py was called; START-HERE names the branch and the last commit's first 7 hex characters (computed by make_evals.py); §5 holds the unfinished task with Next:; RESUME-PROMPT.md names START-HERE.md by an absolute path; the plan file's finished checkpoint is ticked; check_handoff.py was called and printed 'handoff: clean'; START-HERE.md was written before TASKS.md (tool_order); the learnings are in memory or in §6 with the report saying why (the branch the pilot shows)"
    level: e2e
    covers:
      - BEH-01
      - BEH-02
      - BEH-03
      - BEH-04
      - BEH-05
      - BEH-09
      - ERR-04
      - ERR-08
  - id: VER-03
    status: active
    obligation: "Case updates-earlier-handoff: devforgeai/handoff/feat-export/ holds, in the old layout, an earlier TASKS.md with two done entries and an earlier START-HERE.md whose ### Decided records a decision in the user's words, and the prompt says the session started from that handoff. After the run the session's own folder beside them holds both done entries with their evidence, the session's finished work added as done, and the decision with its quote (the trace's Write calls), §1 names the earlier START-HERE as continued, and the earlier files are unchanged"
    level: e2e
    covers:
      - BEH-03
      - BEH-05
  - id: VER-04
    status: active
    obligation: "Case decisions-stay-open: the prompt says the user hasn't chosen between two named options for the next step, names a fact the session believes but didn't check, and quotes an API key the user pasted earlier; START-HERE puts the choice under ### Open with both options and records neither as decided (regex on the options, llm on the reply), marks the fact (unverified), and no handoff file holds the key's text"
    level: e2e
    covers:
      - BEH-02
      - BEH-03
      - BEH-07
  - id: VER-05
    status: active
    obligation: "Case no-git: the scaffold creates no repository, so git's top level is the eval home, a parent of the project folder (make_evals.py checks this premise inside a parent repository); the handoff is written to the session's folder (the store's or the fallback's), its project key the project folder's, START-HERE §2 says git couldn't be used for the project, and check_handoff.py prints 'handoff: clean'"
    level: e2e
    covers:
      - ERR-01
  - id: VER-06
    status: active
    obligation: "Trigger cases, every grader a tool_used Skill with input_match precompact: 'I'm at 75% context: save what we learned and write a handoff before I compact.', 'Write a start-here document and a resume prompt for the next session after /compact.' and 'Prepare for /compact.' load devforgeai:precompact (min 1); 'Summarize what we did so far in this conversation.', 'Save this to memory: I prefer tabs.', 'Create a TASKS.md listing this feature's backlog.', 'How does /compact work?' and 'Update the README with what changed.' don't (min 0, max 0)"
    level: e2e
    covers:
      - BEH-01
  - id: VER-07
    status: active
    obligation: "Live, in Bryan's worker1 tab with --plugin-dir on the build, recorded in §9: (a) tracker, enforce mode, a brainstorm run open at step 3 or later: after /devforgeai:precompact the run's events.jsonl has no run-end and none of the handoff turn's tool events, the band is unchanged and adapter.log has no switch (the live counterpart of SPEC-013 VER-50); (b) memory, Claude Code's memory on: at least one new learning saved as a memory file with its index line, none duplicated; and with memory off, the learning in START-HERE §6 and the report saying why; (c) cold start: in a new session, paste RESUME-PROMPT.md's text; the session reads START-HERE and TASKS and runs §7's check; asked about a decision recorded only in START-HERE (a seeded canary), it answers from §3; then the same after /compact"
    level: manual
    covers:
      - BEH-06
      - BEH-01
      - ERR-04
  - id: VER-08
    status: active
    obligation: "src/tests/precompact/test_structure.py: SKILL.md at most 500 lines, its frontmatter equal to §5's fields and valid per skill-frontmatter.schema.json, metadata devforgeai-tracked 'false', devforgeai-version equal to provenance.yaml's version, provenance valid per skill.schema.json with SKL-012 implementing SPEC-015; every reference and asset SKILL.md names exists; the assets hold DM-01's and DM-02's headings and use only [[fill: placeholders; references/handoff-rules.md holds every item of the self-check (§4); SKILL.md or its references state ERR-02's, ERR-03's, ERR-05's, ERR-06's and ERR-07's handling, the one rule for writing (§4) and BEH-06's rules for changing memory; SKILL.md passes --session to the checker and its description doesn't say 'one folder per branch'; (version 4) SKILL.md runs handoff_paths.py, states ERR-08's handling and BEH-05's rule for a shared plan file, and the skill's folder holds scripts/handoff_paths.py; and SKILL.md, the references and the assets hold no absolute path, no /home/ and no person's name"
    level: unit
    covers:
      - QR-01
      - QR-02
      - ERR-02
      - ERR-03
      - ERR-05
      - ERR-06
      - ERR-07
      - ERR-08
  - id: VER-09
    status: active
    obligation: "QR-03: every case of VER-02 to VER-06 at 0.8 or above against the no-plugin baseline, over the runs Bryan's waiver in §9 sets"
    level: e2e
    covers:
      - QR-03
  - id: VER-10
    status: active
    obligation: "Case leaves-other-session-handoff (version 3): devforgeai/handoff/ holds another session's folder, named by a fixed session ID, with a complete handoff of other work on the same branch, and the prompt doesn't say the session started from it. After the run that folder's three files are unchanged (each still holds its seeded line and nothing of this session's work), no Write or Edit names a path in it (tool_used, max 0), the session's START-HERE.md is written to another folder and names the other folder under 'Other handoffs', the other session's decision isn't in this session's ### Decided, and check_handoff.py was called with --session and printed 'handoff: clean'"
    level: e2e
    covers:
      - BEH-02
      - BEH-03
      - BEH-08
      - ERR-07
  - id: VER-11
    status: active
    obligation: "Live, two sessions at once (version 3), with --plugin-dir on the build in a scratch repository on one branch, recorded in §9: (a) each session runs /devforgeai:precompact; two folders exist under the project's handoff/ in the store, each START-HERE §1 names its own session and the other folder, and the first session's three files have the same checksums after the second's run as before it; (b) the first session runs the skill again, and only its own folder's files change; (c) memory on, each session saves a learning that touches the same memory file and the index: both sessions' lines are there afterwards, none removed or reworded; (d) after /compact in one session, a third run goes to the same folder (the session ID is kept), or §9 records that it isn't and that the handoff was carried over as §4 says; (e) (version 4) one session works in a worktree and runs the skill, the worktree is removed, and a new session started in the main checkout, given only handoff_paths.py's listing, finds that handoff by its branch and title, reads it and carries it over; (f) with handoffRetentionDays 1 in a scratch home's config.json and a folder whose files are two days old, the next run prints it as pruned, it is gone, and a folder one hour old stays; (g) with the store not writable, the handoff goes to the fallback folder and the report says why"
    level: manual
    covers:
      - BEH-05
      - BEH-06
      - ERR-07
      - ERR-08
  - id: VER-12
    status: active
    obligation: "src/tests/precompact/test_handoff_paths.py (version 4), every case normally and under python3 -S, with --home and HOME pointing at a temporary folder so no test reads or deletes anything under the real home: the key is the main checkout's folder name and 8 characters of the SHA-256 of its path, the same from the main checkout and from a worktree of it, different for a clone, and the project root's where git isn't used or its top level is a parent repository; the folder and fallback lines; an empty --session and one beginning with ${ give session-<time>; the listing holds the other handoffs of the store and of DIR/devforgeai/handoff/ (the old layouts included) with date, branch and title, newest first, at most 10, never the session's own; pruning deletes a folder older than the retention with a START-HERE.md and prints it, and leaves a newer one, the session's own, a folder without START-HERE.md, a symbolic link, every folder when the setting is 0 or --no-prune is given, and everything under DIR/devforgeai/handoff/; config.json absent, unreadable or without a number means 30; a folder that can't be deleted is named as skipped and the exit is 0; the script creates no folder and no file; a missing DIR exits 2"
    level: unit
    covers:
      - IF-02
      - BEH-02
```

## 10. Rollout, migration and rollback

- **New skill, nothing to migrate.** It ships in the next plugin version after approval and build (0.26.0, the next
  free minor, set at merge on Bryan's word), with SPEC-013 version 18. Rolling back is removing `skills/precompact/`,
  its evals and tests, the CLAUDE.md row, the schema's const, and SPEC-013 v18's clause.
- **The tracker.** SPEC-013 versions 18 and 19 (BEH-02). After the deploy, an open session needs `/reload-plugins` before the
  key takes effect: until then typing the skill would end the open run, as any plugin skill did.
- **Version 3, nothing to migrate.** The folders versions 1 and 2 wrote (`devforgeai/handoff/<branch>/` with the
  three files directly in it) stay where they are and are only read: a session that resumed from one carries it
  over into its own folder (§4). Old folders collect until the owner deletes them; the skill deletes none. Until a
  session runs the new plugin version (the marketplace update and a restart), it still writes the branch's folder.
- **Version 4, nothing to migrate.** Handoffs written under a project's `devforgeai/handoff/` by versions 1 to 3
  stay there, are listed by IF-02, are only read, and are never pruned. A session whose sandbox allows writes only
  in the project stays on the fallback folder until the owner allows `~/.devforgeai` for writing; that setting is
  the owner's. Rolling back to version 3 leaves the store in place; nothing reads it.
- **Codex.** The Codex port isn't changed; a port is for Codex sessions to build.
- **Records.** CLAUDE.md's skill table gains a `precompact` row (SKL-012, SPEC-015); `src/templates/skill/README.md`
  and `.claude/rules/skills.md` name the third metadata key; SPEC-014's text and link that say every plugin skill is
  tracked move to SPEC-013 v18 at approval.

## 11. Implementation plan

After approval, through `/plugin-dev:skill-development` (and `/plugin-dev:create-plugin`), on branch `docs/precompact`
in `.claude/worktrees/precompact` (ADR-001):
1. Write `src/tests/precompact/test_check_handoff.py` (VER-01) and `test_structure.py` (VER-08), and see them fail.
2. Write `scripts/check_handoff.py` until VER-01 passes, normally and under `python3 -S`.
3. Write the assets (DM-01 to DM-03), `references/handoff-rules.md` and `references/memory.md`, `SKILL.md` from §5
   and §6 (lean, imperative, the checklist first), `provenance.yaml` as SKL-012, and the schema's const; VER-08
   passes. Run skill-reviewer.
4. SPEC-013 version 18's kit tests first (VER-50), then BEH-02's untracked skills in `hooks/progress.tsx`.
5. Write `src/tests/precompact/make_evals.py` with the scaffolds and the cases of VER-02 to VER-06; one `--keep-temp`
   pilot of writes-handoff settles the memory branch (BEH-06) and the git premise (VER-05); generate the cases.
6. Run plugin-validator and an adversarial review; take any finding that would refuse valid work to Bryan.
7. Evaluate cheapest first, then VER-09's suite as the waiver sets; run VER-07 live; record the results in §9.

## 12. Alternatives considered

| Option | Why not chosen |
| --- | --- |
| A subagent writes the handoff (as spec-lookup's lookups run) | A subagent sees none of the conversation the handoff must summarize |
| Keep the tracker as is | Typing the skill in the middle of a tracked run would end that run (SPEC-013 BEH-03); Bryan chose "Yes, the tracker ignores it" |
| One START-HERE.md only | Bryan chose the three files ("START-HERE + TASKS + resume prompt"): the paste-in prompt stays short and points to the master |
| `tmp/plans/` or committed `docs/handoff/` | Bryan chose `devforgeai/handoff/`, gitignored: other projects may not ignore `tmp/`, and the handoff is working notes |
| One folder for every branch, or one per branch (versions 1 and 2) | Bryan chose "One handoff per branch" on 2026-10-05; two sessions with work on one branch then rewrote the same three files, and ERR-05 told each to write over the other's START-HERE. Version 3 keys the folder by session under the branch (Bryan, 2026-11-17, "Per session (Recommended)") |
| Keeping the handoffs in the project, `devforgeai/handoff/` (versions 1 to 3) | Bryan chose that folder on 2026-10-05. A session started in a worktree wrote its handoff inside the worktree, and lost it when the worktree was removed; version 4 moves the handoffs to the user's home folder (Bryan, 2026-11-17) and keeps the project folder as the fallback |
| The store without a `handoff/` level, `~/.devforgeai/<project>/<session>/` | Bryan's first wording; he then chose "Add handoff/ (Recommended)", so the pruner looks only at handoff folders and other data can share the project's folder |
| The model, not a script, working out the folder and deleting old ones | The key needs a hash and git's common directory, and deleting by age must not depend on a session's judgment at 80 percent of its context |
| The branch's folder for the first session, and `<branch>--<short session ID>/` for a session that finds another's handoff there (version 3) | The skill would judge whether a folder is its own before writing it, and a wrong judgment overwrites a file; with a folder per session a wrong call leaves an extra folder or a missed carry-over |
| A checker that verifies every backticked path, and `<...>`, TODO or TBD as placeholders | The drafts review ran those rules over the two handoffs written by hand on 2026-10-05: 75 valid references and 22 command templates would have been refused, and the fix loop had no end |
| Typed only (disable-model-invocation) | Bryan chose "Typed or asked": asking for a handoff before /compact works as well as the command |
| Running it from the compaction hook now | Bryan: "eventually, it may run with the precompact hook"; recorded in §13 |

## 13. Open questions

Decided by Bryan on 2026-10-05 (`/plugin-dev:skill-development` Step 1, "generate a skill for the pre-compaction
workflow you performed. name it /devforgeai:precompact. include templates to provide proper guidance for subsequent
sessions such as tasks.md or start-here.md..."): "Full cycle, 1-run evals (Recommended)"; the purpose and content
quoted in §1; "Yes, the tracker ignores it (Recommended)" (SPEC-013 version 18); "devforgeai/handoff/
(Recommended)"; "START-HERE + TASKS + resume prompt (Recommended)". After the drafts review: "Record nothing after the
load (Recommended)" (SPEC-013 BEH-02); "Key in SKILL.md; unreadable = tracked (Recommended)"; "One handoff per branch
(Recommended)", with the folder following the work's branch ("Folder follows the work's branch", §4); "Typed or asked; run at 70-80% (Recommended)", on a side note that the skill spends context itself and
a run cut off at the limit (automatic compaction off) would leave the handoff half-written.

Decided by Bryan on 2026-11-17 (version 3), after reporting that one session's `/devforgeai:precompact` had
modified another session's handoff files ("if there are more than one sessions working in a project, i believe the
same issue exists where they 'stomp' on each other"): the folder key, "Per session (Recommended)"
(`devforgeai/handoff/<branch>/<session-id>/`: a session writes only its own folder and treats every other folder as
read-only; a new session that resumed from a handoff carries it over into its own folder), in place of "One handoff
per branch"; and memory writes in scope, "Yes, add rules (Recommended)" (read again before changing, Edit only,
never delete or rewrite another session's content, never Write over an existing memory file). Drafter's choices in
version 3, shown in the approval question and accepted with it ('Approve as drafted', 2026-11-17): the fallback folder name `session-<time>` when the session ID isn't
substituted; `Continues:` and `Other handoffs on this branch:` in START-HERE §1; the checker's `--session`; ERR-05
kept for the session's own folder and ERR-07 added; old folders left in place and never deleted by the skill; a
wrong or stale memory line of another session answered by a dated line, not an edit of it.

Decided by Bryan on 2026-11-17 (version 4): "how about a place that's 'more durable' that gets pruned every 7 days
or so? perhaps in ~/.devforgeai/<project>/<session id>/ if a worktree is deleted or pruned or session starts in the
project folder, it will be able to read the files. in windows, the same is true
c:\users\<user id>\.devforgeai\<project>\<session id>\..."; then "Yes, fold into this stack (Recommended)";
"30 days, configurable (Recommended)" in place of the 7 days, counted from the last write in the folder; "Fall back
to the project (Recommended)" when the store can't be written; "Folder name plus short hash (Recommended)" for the
project's key; "Add handoff/ (Recommended)" for the store's layout; "~/.devforgeai/config.json (Recommended)" for
the setting; and "Yes, add it to v4 (Recommended)" for a rule on plan files that sessions share. Drafter's choices
in version 4, named in the approval question and accepted with it ('Approve as drafted', 2026-11-17): no branch level in the folder; the script `handoff_paths.py` (IF-02)
that names the folders, lists the other handoffs and prunes, and the model never deleting; the fallback decided by
the Write tool's result and not by a test in Bash; the setting's name `handoffRetentionDays`, with 0 for never; a
pruned folder being one that holds a START-HERE.md; the listing's 10 newest; nothing pruned in a project's
`devforgeai/handoff/`; `Other handoffs:` replacing version 3's `Other handoffs on this branch:`.

Recorded for later: running the skill, or a check that the handoff is current, from a compaction hook (Bryan:
"eventually, it may run with the precompact hook"); the tracker's adapter already sees `session.compact` (SPEC-013
BEH-24). Whether PRD-001 gains a requirement for the handoff (§2). Whether spec-lookup, marked untracked, could load in
the main conversation during a run instead of its agent (SPEC-014 §13).

- Record (2026-10-08, no version bump): SPEC-013 version 21 (BEH-36; counted as fuel from version 23) runs this skill automatically, once between two compactions and as if the person had typed it, when the context window's fuel left falls to `precompactRunFuel` (20% by default, which is 80% of the window used), and with version 25's set of pending names (BEH-41, approved) the handoff's turn is marked as SPEC-013 BEH-02 says; version 26 (in review) adds a one-shot pending mark in $.state (BEH-36, BEH-02) as a second path to that mark. That is the 'eventually, it may run with the precompact hook' item recorded above for later. Versions 21 and 23 to 25 are built on branch `feat/dashboard-build` (plugin 0.28.0, not merged); version 26 will be built there too.

Drafter's choices, for Bryan's accept or challenge: the seven START-HERE sections and their line shapes (DM-01), taken
from this session's own handoff of 2026-10-05; the 40-line limit and about 15 lines for the resume prompt; the 20 done
entries kept in TASKS.md before archiving (it changes "progress checkpoints" kept forever into a recent list plus an
archive); the 250-line warning; the three runs of the script; the argument as a note put first in §5; the checker's
reference rule (links and §4's first tokens only) and the `[[fill: ...]]` placeholder form; the branch-folder slug
(`detached-<hash>`, `no-git`); the order of the steps; running no tests; asking nothing; the example memory format
named in BEH-06.

## Change Log

| Version | Date | Author | Change | Items affected |
| --- | --- | --- | --- | --- |
| 1 | 2026-10-05 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Drafted from Bryan's decisions of 2026-10-05 (`/plugin-dev:skill-development`, "Full cycle, 1-run evals", the purpose and content in his words, the tracker ignores it, devforgeai/handoff/, three files); status in-review | all |
| 1 | 2026-10-05 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Before approval, the drafts review's fixes (2 critical: the checker's rules narrowed so valid handoffs pass and the fix loop ends; ERR-01 decided by git's top level, VER-05's premise in a parent repository) and Bryan's answers (one folder per branch; typed or asked, run at 70 to 80 percent, START-HERE written first, memory last; the session's plan file ticked; line shapes and the self-check in the spec; the resume prompt's absolute path and branch check; no tests run; no secrets; ERR-06) | §1 to §13 |
| 1 | 2026-10-05 | Bryan | Approved ('Approve both (Recommended)', with the summary and the drafter's choices shown in its preview, the run at 70-80% flagged as a departure from his 80-90%) | status |
| 2 | 2026-10-05 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | The build's structure test found that §5's description holds `<branch>`, which skill-frontmatter.schema.json refuses (a description holds no < or >; PRD-001 NFR-002, §2): it now says 'in devforgeai/handoff/, one folder per branch'. Writing the no-git eval case (VER-05) found §4's project root (the git top level when a parent of the working directory) contradicting ERR-01 (a parent repository the user didn't name means git isn't used): the root is now the folder the session started in, or a folder holding it that the user names; status in-review; on a side note Bryan relayed (sessions on main that edit worktrees with git -C would share main's folder), he chose 'Folder follows the work's branch': the folder and the state checks follow the branch of the worktree the session's work is in; §1 names it and its worktree; the resume prompt checks that worktree's branch; IF-01 states the checker's readings that the build's reviews settled (only the three files read; `[[fill:` outside code; a §2 bullet's own text before a nested list; `- None.` under Decided; `Nothing outstanding` with a note; items over blank lines and fences; `:LINE:COL`, URL-decoded and root-relative links; a relative path beside its file too; the markers on any line of a §4 item; unset variables skipped; the resume path matched whole; an unreadable folder exits 2) | §4, §5, IF-01, DM-01, DM-03, §13 |
| 2 | 2026-10-05 | Bryan | Approved ('Approve v2 (Recommended)', with the four changes shown in its preview); the SPEC-013 link moved to version 19 on his 'Fix now as SPEC-013 v19' | status, §2, §10 |
| 2 | 2026-10-05 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: SKL-012 v1 approved, merged in PR #93 (`909a252`) and deployed as plugin 0.26.0 (§9, blockquote) | §9, blockquote |
| 2 | 2026-10-08 | claude-code (session 7637882f-b2ec-465e-988a-9602340d1023) | Record-only update, with no version bump: §13 records that SPEC-013 version 21 (BEH-36), with version 25's set of pending names, runs this skill automatically at precompactRunFuel (20% fuel left by default), the 'eventually, it may run with the precompact hook' item §13 recorded for later; to be built with the dashboard (SPEC-016) | §13 |
| 2 | 2026-10-08 | claude-code (session 7637882f-b2ec-465e-988a-9602340d1023) | Record-only update, with no version bump: §13's note on the automatic run points to SPEC-013 version 26's pending mark (in review) and says versions 21 and 23 to 25 are built on branch `feat/dashboard-build` (plugin 0.28.0, not merged) | §13 |
| 3 | 2026-11-17 | claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) | Bryan reported one session's precompact run modifying another session's handoff files. The cause: one folder per branch (§4) shared by every session with work on that branch, and ERR-05 telling each to write its START-HERE over the other's. On his decisions of 2026-11-17 ('Per session (Recommended)', 'Yes, add rules (Recommended)'): the handoff folder is devforgeai/handoff/<branch>/<session>/, a session writes only its own folder and only reads any other, a handoff is carried over only by the session that resumed from it; START-HERE §1 gains the Continues and Other handoffs lines; check_handoff.py gains --session; ERR-05 narrowed to the session's own folder and ERR-07 added; memory is changed only by adding (BEH-06); VER-01, VER-02, VER-03, VER-05 and VER-08 reworded, VER-10 and VER-11 added; status in-review, not built | status, §1, §4, §5, BEH-02, BEH-03, BEH-05, BEH-06, BEH-08, BEH-09, ERR-05, ERR-07, VER-01, VER-02, VER-03, VER-05, VER-08, VER-10, VER-11, §9, §10, §12, §13 |
| 3 | 2026-11-17 | Bryan | Approved ('Approve as drafted', with the drafter's choices named in the question: the session-<time> fallback folder name, START-HERE §1's Continues and Other handoffs lines, check_handoff.py --session, ERR-07, old folders never deleted by the skill, another session's wrong memory line answered by a new dated line) | status |
| 4 | 2026-11-17 | claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) | On Bryan's decisions of 2026-11-17 (§13), before version 3 was deployed: the handoff folder moves to <home>/.devforgeai/<project>/handoff/<session>/, outside the repository, so it outlives a removed worktree and any session of the project can read it; the project's key is the main checkout's folder name and a short hash of its path; the branch level is dropped; the fallback folder <root>/devforgeai/handoff/<session>/ is used when the store's Write is refused (ERR-08); handoff_paths.py (IF-02) names the folders, lists the project's other handoffs with date, branch and title, and prunes a folder not written for handoffRetentionDays (30; ~/.devforgeai/config.json); a plan file other sessions share is changed only by adding (BEH-05); the description, IF-01's .gitignore check, BEH-02, BEH-03, BEH-08, BEH-09, ERR-02, ERR-07, DM-01 and the VER items follow; VER-12 added; status in-review, not built | status, §1, §3, §4, §5, IF-01, IF-02, BEH-02, BEH-03, BEH-05, BEH-08, BEH-09, ERR-02, ERR-07, ERR-08, VER-02, VER-05, VER-08, VER-10, VER-11, VER-12, §9, §10, §12, §13 |
| 4 | 2026-11-17 | Bryan | Approved ('Approve as drafted', with the drafter's choices named in the question: no branch level; handoff_paths.py naming the folders, listing the other handoffs and pruning, the model never deleting; the fallback decided by the Write tool's refusal; handoffRetentionDays with 0 for never; only folders holding a START-HERE.md pruned and nothing in a project's devforgeai/handoff/; sandboxed sessions staying on the fallback until ~/.devforgeai is allowed) | status |
