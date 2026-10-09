---
id: SPEC-015
type: spec
title: "Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact"
status: approved      # draft | in-review | approved | superseded | deprecated
version: 2
created: 2026-10-05
updated: 2026-10-08
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
  - {id: SPEC-013, relation: informed_by, version: 26, hash: null, note: "BEH-02 (versions 18 and 19): an untracked skill opens no run, and the turn that loads it records no further tool event or reply in the open run, so the handoff can be written in the middle of a tracked run"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/precompact", "src/tests/precompact", "src/claude/DevForgeAI/evals/precompact", "src/schemas/skill-frontmatter.schema.json", "CLAUDE.md"]
---

# SPEC-015 — Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact

> **Status:** version 2 approved by Bryan on 2026-10-05 (version 1 the same day); SKL-012 v1 merged in PR #93 (`909a252`) and
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

The files live in `devforgeai/handoff/<branch>/`, one folder per branch (gitignored), so sessions on different
branches of one checkout don't overwrite each other's handoff. The skill works in any project that uses DevForgeAI: it
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
│   └── check_handoff.py        # IF-01: checks a handoff folder (BEH-08); standard library only
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

**The handoff folder** is `<root>/devforgeai/handoff/<branch>/`, `<branch>` being the work's branch name with each
run of characters other than letters, digits, `.`, `_` and `-` replaced by `-` (`docs/precompact` becomes
`docs-precompact`); `detached-<short hash>` on a detached HEAD; `no-git` where git can't be used (ERR-01).
`<root>/devforgeai/handoff/.gitignore` holds `*`, as the tracker's `devforgeai/progress/` does (SPEC-013 BEH-15): the
handoff is working notes for the next session on this machine, not a project document.

The files are Markdown with fixed second-level headings, which IF-01 checks; more `##` headings may follow the last
required one, and `###` headings may appear anywhere. A value the template leaves to fill has the form `[[fill: what]]`,
the only placeholder form; IF-01 refuses any left in a written file.

**DM-01. START-HERE.md**, the master document. Its headings and line shapes, in order:

| Heading | Holds |
|---|---|
| `## 1. What this is` | the work in two or three sentences; the project root; the work's branch, with its worktree's path when that isn't the root, and the checkout the session runs in; the date and time written (UTC) and the session that wrote it |
| `## 2. Verified state` | facts checked while writing (BEH-02), one per bullet, each ending `[checked: <command> -> <what it showed>]` or `(unverified)` with where the fact came from and its date |
| `## 3. Decisions` | `### Decided`: each decision as a bullet with who decided, the date as YYYY-MM-DD and their words in quotes; `### Open`: the questions still the user's, each with the options as the user saw them |
| `## 4. Read first` | a numbered list, each item starting with the path in backticks, then why and when to read it; searches to run (`grep -n "<term>" <path>`) where a file is too long to read whole; a closing line: when something needed isn't here, search the repository and memory before asking the user |
| `## 5. Outstanding` | a numbered list in order, each item `N. <what>. Next: <a command, a file:line or a question>. Waits for: <what, or nothing>.`; the user's note (the skill's argument) first when given; or the single line `Nothing outstanding.` |
| `## 6. Rules, traps and learnings` | what cost time and how to avoid it; the project's rules that apply, cited, not restated, when a file already holds them; the session's new learnings (BEH-06 saves the durable ones to memory) |
| `## 7. Before acting` | commands to run first, each with what it should show if nothing changed since the handoff |

**DM-02. TASKS.md**, the checkpoint list: `## Done` and `## Next`. Each entry is a checkbox line naming the step, then
its evidence (commit, pull request, file, test result with its date) or its next action. An earlier TASKS.md is
updated, never replaced; past 20 done entries, the oldest move to `TASKS-archive.md` in the same folder, which TASKS.md
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
description: Prepares a Claude Code session for /compact, so the next session can continue with nothing pasted by hand. It writes a full-fidelity handoff in devforgeai/handoff/, one folder per branch (START-HERE.md with the verified state, decisions and who made them, files to read first and the work outstanding; TASKS.md; a short RESUME-PROMPT.md to paste after compacting), ticks the session's plan file, and saves the session's new learnings to memory. Use before running /compact, ideally at 70 to 80 percent of the context window, or when asked to save learnings and write a handoff, start-here document or resume prompt for the next session after compacting. Not for project documentation, release notes, commit messages or a backlog.
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
| IF-01 | `python3 check_handoff.py [--root DIR] HANDOFF_DIR` | Checks the handoff folder `HANDOFF_DIR` (relative to `DIR`, which is `.` by default) against the self-check's script items (§4), reading only START-HERE.md, RESUME-PROMPT.md and TASKS.md (never TASKS-archive.md or another file): the three files exist; START-HERE.md and TASKS.md have their headings in order (DM-01, DM-02); RESUME-PROMPT.md has at most 40 lines and holds the absolute path of `HANDOFF_DIR/START-HERE.md` as a whole path (not part of a longer one); no file holds `[[fill:` outside code (a code span or a fenced block quotes the form; the assets never put a placeholder in backticks); §2's bullets, §3's `### Decided` bullets and §5's items have their shapes (DM-01): a §2 bullet's own text, before any nested list and with emphasis marks ignored, ends with its marker; a `### Decided` bullet may instead be `- None.`; §5 has at least one item or a line starting `Nothing outstanding`; an item runs on over indented lines, blank lines and fences; each path a reference names exists, a reference being a Markdown link's target that isn't a URL, an anchor or `mailto:`, or the first backticked token of an item of START-HERE §4, read after removing a trailing `:LINE`, `:LINE-LINE`, `:LINE:COL` or `#Lnn` (a link's target also URL-decoded), expanding a leading `~/` and any set variable, and resolved against `DIR`, or beside the file that names it, when relative (a link starting `/` may also be read from `DIR`), unless its line or the line above says `(not yet created)` or `(session-only)`, or, for a §4 item, any of the item's lines does; a path holding a variable that isn't set isn't checked; no other backticked text is checked; `DIR/devforgeai/handoff/.gitignore` holds `*`. Prints one line per problem, `<file>:<line>: <problem>` (line 0 for the file as a whole), and per warning, `<file>:<line>: warning: <text>` (START-HERE over 250 lines; `today`, `yesterday`, `tomorrow` or `recently` outside quotes and code), then `handoff: clean` when there is neither, else `handoff: <n> problems, <m> warnings`. Exit 0 with no problem (warnings allowed), 1 with problems, 2 when it can't run (`HANDOFF_DIR` missing or unreadable) |

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Run when the user types /devforgeai:precompact or asks, before /compact, to save the session's learnings and write a handoff, start-here document or resume prompt for the next session. Work through the checklist in order (BEH-02 to BEH-09) in the main conversation: a subagent can't see the conversation the handoff summarizes. Ask the user nothing; put what can't be established into START-HERE §3 as open. The progress tracker ignores this skill (SPEC-013 BEH-02, version 18): a tracked run open in the session stays open, and the handoff names it with its step (from the tracker's current.json for the session, when it exists)."
  - id: BEH-02
    status: active
    rule: "Check the live state first, cheaply and read-only: don't re-read what the session already holds (its CLAUDE.md files and the memory index are in its context); read only the handoff folder's earlier files. Keep each command's output small: the branch and its upstream (GIT_OPTIONAL_LOCKS=0 git status --porcelain=v2 -b), the last commits (git log -n 5 --oneline), uncommitted changes (git diff --stat and git diff --stat --cached), open pull requests where gh works (gh pr list --limit 10). Run no test or build command: cite the last result the session saw, with its date and (unverified), unless the user's argument says to run one. Write the handoff folder and devforgeai/handoff/.gitignore before any other file. A fact the session believes but didn't check now goes into the handoff marked (unverified)."
  - id: BEH-03
    status: active
    rule: "Write START-HERE.md (DM-01) from the template assets/start-here.md in one write, first of the files, so a session cut off later still leaves it. Carry over from an earlier START-HERE in the same folder what still holds (decisions, open questions, rules, traps and learnings, outstanding items not finished). Write in full fidelity (the self-check, §4). Use progressive disclosure: name files with why and when to read them, and searches to run, instead of copying their content; copy in only what exists nowhere else (a decision said only in the conversation, a result not saved to a file). Quote the user's words for each decision, with the date. Put the user's argument, if any, first in §5. Never write a secret: no token, key or password, even one said in the conversation."
  - id: BEH-04
    status: active
    rule: "Write RESUME-PROMPT.md (DM-03) from the template assets/resume-prompt.md: about 15 lines and at most 40, naming START-HERE.md by its absolute path, with the branch check, the 'Before acting' step, the first outstanding item, asking before any decision §3 or §5 says is the user's, and searching the repository and memory before asking."
  - id: BEH-05
    status: active
    rule: "Update TASKS.md (DM-02) from the template assets/tasks.md when it doesn't exist: mark what this session finished as done, with its evidence (commit, pull request, file or test result with its date), and list what is next with its next action; keep every done entry, moving the oldest past 20 to TASKS-archive.md. When the session keeps a plan, task or checkpoint file of its own (one the project's instructions, memory or the conversation name), tick its checkpoints with their evidence too, and name it in START-HERE §4 as the source of truth for the steps it lists; TASKS.md then holds only what that file doesn't."
  - id: BEH-06
    status: active
    rule: "Save the session's new, durable learnings to memory when the session's instructions describe a memory system (a memory location and its format): follow that format exactly (for example, in Claude Code's memory, one fact per file with its frontmatter, an index line, written with Write or Edit), update an existing memory that covers the same fact rather than adding a duplicate, and save only what the repository and its instructions don't already record: decisions with their reasons, verified facts about tools and the environment, practices the user asked for or confirmed, and traps that cost time. Never save a secret. When the session has no memory system, or a memory write is refused, the learnings stay in START-HERE §6, and the report says so."
  - id: BEH-07
    status: active
    rule: "Never turn outstanding work into a decision: an item waiting for the user's choice says so under ### Open, with the options as the user saw them, and the handoff records no choice the user didn't make."
  - id: BEH-08
    status: active
    rule: "Run python3 ${CLAUDE_SKILL_DIR}/scripts/check_handoff.py --root <project root> devforgeai/handoff/<branch> (IF-01) as a command of its own. On exit 1, fix each problem it lists in the file it names, and run it again, at most three runs in all; never change a correct reference only to satisfy the script. Problems left after the third run go into the report. On exit 2, the folder wasn't written: write the files and run it again. Then read the files back against the self-check's other items (§4, and references/handoff-rules.md)."
  - id: BEH-09
    status: active
    rule: "Report in the reply: the folder and the files written, the plan or task file ticked, the memories saved or updated (or why none), anything left marked (unverified), any problem the script still reports, and the text of RESUME-PROMPT.md in a fence longer than any fence inside it, so the user can paste it after /compact. Change no file but the handoff folder's files, devforgeai/handoff/.gitignore, the plan or task file BEH-05 names and memory files."
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
    condition: "The handoff folder can't be written"
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
    condition: "The handoff folder holds an earlier handoff of other work (another topic on the same branch)"
    handling: "Keep its TASKS.md entries under a ## heading naming that work, after the required ones; write START-HERE for the current work, naming the earlier work in §5 as not continued here"
    user_result: "Both lines of work kept, the current one first"
  - id: ERR-06
    status: active
    condition: "The session is cut off (the context limit) before the skill finishes"
    handling: "Nothing to do in the run; the order (BEH-03 first) leaves START-HERE.md written; the next session, given its path, finishes the rest by running the skill again"
    user_result: "At least START-HERE.md"
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
    obligation: "src/tests/precompact/test_check_handoff.py, every case normally and under python3 -S. A complete handoff exits 0 with 'handoff: clean'. A valid handoff holding the forms references take in practice also exits 0: commands, globs, URLs, slash commands, branch names with '/', versions, ~/ paths, path:LINE and path#Lnn references, <...> command templates, all in backticks, and a reference marked (session-only) on the line above. Each of a missing file, a missing or misordered heading, a §2 bullet with no [checked: or (unverified), a ### Decided bullet with no date or no quote, a §5 item with no Next: or no Waits for:, an empty §5, a 41-line RESUME-PROMPT.md, one without START-HERE.md's absolute path, a leftover [[fill:, a §4 path or a link target that doesn't exist, and a missing .gitignore exits 1 with a '<file>:<line>: <problem>' line; a START-HERE over 250 lines and the word yesterday outside quotes give warnings and exit 0; a missing HANDOFF_DIR exits 2"
    level: unit
    covers:
      - IF-01
      - BEH-08
  - id: VER-02
    status: active
    obligation: "Case writes-handoff: a scaffolded git repository on branch feat/export with three commits (fixed author, committer and dates), a plan file with checkpoints and an unfinished task; the prompt says what the session did and asks to prepare for /compact. Graded: devforgeai/handoff/feat-export/ holds START-HERE.md, TASKS.md and RESUME-PROMPT.md and devforgeai/handoff/.gitignore holds *; START-HERE names the branch and the last commit's first 7 hex characters (computed by make_evals.py); §5 holds the unfinished task with Next:; RESUME-PROMPT.md names START-HERE.md by an absolute path; the plan file's finished checkpoint is ticked; check_handoff.py was called and printed 'handoff: clean'; START-HERE.md was written before TASKS.md (tool_order); the learnings are in memory or in §6 with the report saying why (the branch the pilot shows)"
    level: e2e
    covers:
      - BEH-01
      - BEH-02
      - BEH-03
      - BEH-04
      - BEH-05
      - BEH-09
      - ERR-04
  - id: VER-03
    status: active
    obligation: "Case updates-earlier-handoff: the handoff folder holds an earlier TASKS.md with two done entries and an earlier START-HERE.md whose ### Decided records a decision in the user's words; after the run both done entries remain with their evidence, the session's finished work is added as done, and the decision is still there with its quote"
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
    obligation: "Case no-git: the scaffold creates no repository, so git's top level is the eval home, a parent of the project folder (make_evals.py checks this premise inside a parent repository); the handoff is written to devforgeai/handoff/no-git/, START-HERE §2 says git couldn't be used for the project, and check_handoff.py prints 'handoff: clean'"
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
    obligation: "src/tests/precompact/test_structure.py: SKILL.md at most 500 lines, its frontmatter equal to §5's fields and valid per skill-frontmatter.schema.json, metadata devforgeai-tracked 'false', devforgeai-version equal to provenance.yaml's version, provenance valid per skill.schema.json with SKL-012 implementing SPEC-015; every reference and asset SKILL.md names exists; the assets hold DM-01's and DM-02's headings and use only [[fill: placeholders; references/handoff-rules.md holds every item of the self-check (§4); SKILL.md or its references state ERR-02's, ERR-03's, ERR-05's and ERR-06's handling; and SKILL.md, the references and the assets hold no absolute path, no /home/ and no person's name"
    level: unit
    covers:
      - QR-01
      - QR-02
      - ERR-02
      - ERR-03
      - ERR-05
      - ERR-06
  - id: VER-09
    status: active
    obligation: "QR-03: every case of VER-02 to VER-06 at 0.8 or above against the no-plugin baseline, over the runs Bryan's waiver in §9 sets"
    level: e2e
    covers:
      - QR-03
```

## 10. Rollout, migration and rollback

- **New skill, nothing to migrate.** It ships in the next plugin version after approval and build (0.26.0, the next
  free minor, set at merge on Bryan's word), with SPEC-013 version 18. Rolling back is removing `skills/precompact/`,
  its evals and tests, the CLAUDE.md row, the schema's const, and SPEC-013 v18's clause.
- **The tracker.** SPEC-013 versions 18 and 19 (BEH-02). After the deploy, an open session needs `/reload-plugins` before the
  key takes effect: until then typing the skill would end the open run, as any plugin skill did.
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
| One folder for every branch, or one per session | Bryan chose "One handoff per branch": sessions on different branches don't overwrite each other, and the next session finds the folder from its branch |
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
