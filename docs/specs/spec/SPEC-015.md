---
id: SPEC-015
type: spec
title: "Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact"
status: in-review      # draft | in-review | approved | superseded | deprecated
version: 1
created: 2026-10-05
updated: 2026-10-05
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a4f2ade8-0127-4b96-bc22-b3498b2ab3a9"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 11, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 11, hash: null, note: "decisions stay the user's: the handoff records who decided what, in their words, and never turns outstanding work into a decision"}
  - {id: SPEC-013, relation: informed_by, version: 18, hash: null, note: "BEH-02 (version 18): a skill marked untracked opens no run and leaves the open run alone, so the handoff can be written in the middle of a tracked run"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/precompact", "src/tests/precompact", "src/claude/DevForgeAI/evals/precompact", "CLAUDE.md"]
---

# SPEC-015 — Pre-compaction handoff skill: save what the session learned and write a full-fidelity handoff before /compact

> **Status:** version 1 in review (drafted 2026-10-05). The drafting plan and its checkpoints are in
> `tmp/plans/2026-10-05-precompact.md` (local).

## 1. Overview

When a Claude Code session's context window fills (Bryan: "above 80-90%"), its owner runs `/compact`, and the next
part of the session starts from a summary: it may start cold, or with gaps. Bryan's practice until now has been to
paste, before each `/compact`, a request to save what the session learned to memory and to write a document the next
session can start from. This skill does that in one command, `/devforgeai:precompact`.

Bryan, 2026-10-05: "the goal of this skill is to save me from copying & pasting in sessions when context windows grow
above 80-90% asking them to save newfound learnings to memory then create a tasks.md or start-here.md document in
full-fidelity, zero ambiguity for the next session for when I run /compact. the document is to reference files, etc...
as the next session may start cold or have amnesia due to /compact. it is not meant to run between skills although
eventually, it may run with the precompact hook." And: "ensure the resume prompt or start-here.md document is in
full-fidelity, zero ambiguity for next session. include but not limited to 'progressive disclosure' style where
applicable to reference documents or have it search repo when necessary."

The skill:
1. checks the live state of the work (what the repository, its branches and pull requests say now), so the handoff
   states facts, not recollections;
2. saves the session's new, durable learnings to memory, in the format the session's own instructions give;
3. updates a checkpoint list, `devforgeai/handoff/TASKS.md`;
4. writes the master document, `devforgeai/handoff/START-HERE.md`: what the work is, its verified state, the decisions
   and who made them, what to read first and why, what is outstanding and in which order, the traps, and a check to run
   before acting; it points to files and searches rather than copying them in (progressive disclosure);
5. writes the short text the owner pastes after `/compact`, `devforgeai/handoff/RESUME-PROMPT.md`, which sends the next
   session to START-HERE first;
6. checks the three files with a bundled script and fixes what it reports.

It writes in any project that uses DevForgeAI: it reads the project's instructions (its `CLAUDE.md` files and the
session's own instructions) for what matters there, and it names no machine, tab or path of this repository. The
progress tracker ignores the skill (SPEC-013 BEH-02, version 18), so running it in the middle of a brainstorm or
architecture run leaves that run open, and the handoff names it.

**What this can't guarantee.** The handoff is only as good as what the session can still see: what scrolled out of
the context before the skill ran is lost unless it reached a file, memory or the conversation summary. The skill checks
its references and its structure; whether a fact is the right one to keep is the session's judgment. Evals can't see
memory (the eval sandbox seals the home folder), so saving to memory is checked live (VER-07).

## 2. Constraints

- **PRD-001 NFR-001 to NFR-003** (v11): SKILL.md is at most 500 lines and its description at most 1024 characters;
  the frontmatter validates against `skill-frontmatter.schema.json` and `skill.schema.json`; the skill has a
  `claude plugin eval` suite against the no-plugin baseline. Bryan's decision of 2026-10-05 ("Full cycle, 1-run
  evals"): one run per case at 0.8 or above, with the 3-run qualification waived (§9 records the waiver).
- **ADR-001** (v4): built in a worktree from `src/claude/DevForgeAI/`; the owner deploys; evals run from a plain
  terminal.
- **Decisions stay the user's** (PRD-001 FR-003, informed_by). The handoff records each decision with who made it and
  their words; it never records outstanding work as decided, and it asks nothing it can find out by checking.
- **Generic.** The plugin ships to every user, so the skill names no machine, terminal tab, person or path of this
  repository; what a project needs comes from that project's instructions and files.
- **The progress tracker** (SPEC-013 v18, informed_by): BEH-02 tracks every plugin skill except one whose SKILL.md
  marks it untracked (`metadata.devforgeai-tracked: "false"`); this skill is the first.
- **Standard library only** for the check script, like `validate_brn.py` and `find_spec.py`: it runs under
  `python3 -S`.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/precompact/
├── SKILL.md                    # the checklist (BEH-01 to BEH-09), the decisions that are the user's
├── provenance.yaml             # SKL-012, implements SPEC-015
├── scripts/
│   └── check_handoff.py        # IF-01: checks the three files (BEH-08); standard library only
├── references/
│   ├── handoff-rules.md        # the full-fidelity rules, section by section, and the self-check list
│   └── memory.md               # what counts as a learning worth saving, and how to save it
└── assets/
    ├── start-here.md           # the START-HERE.md template (DM-01)
    ├── tasks.md                # the TASKS.md template (DM-02)
    └── resume-prompt.md        # the RESUME-PROMPT.md template (DM-03)
src/claude/DevForgeAI/evals/precompact/<case>/  # one case per automated VER item (§9)
src/tests/precompact/                           # check_handoff.py's tests, make_evals.py (not deployed)
CLAUDE.md                                        # the skill table row (this repository only)
```

```mermaid
flowchart LR
    S[/devforgeai:precompact] --> V[Check live state BEH-02]
    V --> M[Save learnings to memory BEH-03]
    M --> T[Update TASKS.md BEH-04]
    T --> H[Write START-HERE.md BEH-05]
    H --> R[Write RESUME-PROMPT.md BEH-06]
    R --> C[check_handoff.py BEH-08]
    C -->|problems| H
    C -->|clean| P[Report the paths and the prompt BEH-09]
```

## 4. Data model

The skill writes three files in `<project root>/devforgeai/handoff/`, with a `.gitignore` there holding `*`, as the
tracker does for `devforgeai/progress/` (SPEC-013 BEH-15): the handoff is working notes for the next session on this
machine, not a project document. The files are Markdown with fixed second-level headings, which IF-01 checks.

**DM-01. START-HERE.md**, the master document. Its headings, in order:

| Heading | Holds |
|---|---|
| `## 1. What this is` | the work in two or three sentences, the project root, the date and time it was written (UTC) and by which session |
| `## 2. Verified state` | facts checked while writing (BEH-02), each with how it was checked: branch and commit, uncommitted changes, open pull requests, versions, the last test results with the command that gave them; anything not checked is marked `(unverified)` |
| `## 3. Decisions` | each decision that shapes the next work: what, who decided, when, and their words in quotes; open questions listed apart, as open |
| `## 4. Read first` | an ordered list of files to read, each as a path with why and when (progressive disclosure: point, don't copy), and searches to run (`grep -n "<term>" <path>`) where a file is too long to read whole |
| `## 5. Outstanding` | the remaining work in order, each item with its next concrete action (a command, a file and line, a question to ask) and what it waits for (the user's approval, another step) |
| `## 6. Rules and traps` | what cost time in this work and how to avoid it, and the project's rules that apply (cited, not restated, when a file already holds them) |
| `## 7. Before acting` | commands to run first and what each should show if nothing changed since the handoff |

**DM-02. TASKS.md**, the checkpoint list: `## Done` and `## Next` sections; each entry a checkbox line naming the step,
then its evidence (commit, pull request, file, test result) or its next action. An earlier TASKS.md is updated, never
replaced: done entries stay, with their evidence.

**DM-03. RESUME-PROMPT.md**, at most 40 lines: what the work is in one sentence, the instruction to read
`devforgeai/handoff/START-HERE.md` first and then `TASKS.md`, to run START-HERE's "Before acting" check, and to go on
with the first outstanding item, asking the user before anything §3 says is theirs.

**Full fidelity** (BEH-05, BEH-07), for all three files: exact identifiers (commit hashes, branch names, pull request
numbers, versions, document and item IDs, test counts with their command); absolute dates; names instead of pronouns
whose referent the next session can't see ("PR #91", not "the PR"); every referenced path existing, or marked
`(not yet created)` or `(session-only)`; nothing left as a template placeholder.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: precompact
description: Prepares a Claude Code session for /compact. It saves what the session learned to memory, updates a checkpoint list, and writes a full-fidelity handoff in devforgeai/handoff/ (START-HERE.md, TASKS.md and a short RESUME-PROMPT.md to paste after compacting) from the verified state of the repository, the decisions made and who made them, the files to read first and the work outstanding, so the next session can continue with nothing pasted by hand. Use when the context window is nearly full, before running /compact, or when asked to save learnings, write a handoff, a start-here or tasks document, or a resume prompt for the next session. Not for project documentation, release notes or commit messages.
argument-hint: "[focus or note for the next session]"
metadata:
  devforgeai-id: "SKL-012"
  devforgeai-version: "<SKL-012's provenance.yaml version, quoted>"
  devforgeai-tracked: "false"
```

- **The name is `precompact`,** so the command is `/devforgeai:precompact`. An argument is a note from the user for
  the next session (what to focus on, what to leave); START-HERE quotes it in §5.
- **Tools the instructions use:** Bash for read-only checks (`git`, `gh` when present, the project's own test or
  status commands as its instructions name them) and to run `python3 ${CLAUDE_SKILL_DIR}/scripts/check_handoff.py`;
  Read; Write and Edit for the three files, the `.gitignore` and memory files. No other file is changed.
- **Downstream contract:** the next session (after `/compact`, or a new session) needs only RESUME-PROMPT.md's text.

| Item | Command | Behaviour |
| --- | --- | --- |
| IF-01 | `python3 check_handoff.py [--root DIR]` | Checks `DIR/devforgeai/handoff/` (`DIR` is `.` by default): the three files exist; each has its headings (DM-01 to DM-03) in order; START-HERE §5 has at least one item; RESUME-PROMPT.md has at most 40 lines and names `devforgeai/handoff/START-HERE.md`; no file holds a template placeholder (`<...>` from the assets, `TODO`, `TBD`); each path in backticks that holds a `/` or a file extension exists under `DIR`, unless the same line says `(not yet created)` or `(session-only)`, or it is absolute outside `DIR` (reported, not refused); the `.gitignore` exists and holds `*`. Prints one line per problem, `<file>:<line>: <problem>`, then `handoff: <n> problems` or `handoff: clean`. Exit 0 clean, 1 with problems, 2 when it can't run (no `devforgeai/handoff/` folder under `DIR`) |

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Run when the user types /devforgeai:precompact or asks to prepare for /compact, to save learnings before compacting, or to write a handoff, start-here, tasks document or resume prompt for the next session. Work through the checklist in order (BEH-02 to BEH-09), in the main conversation: a subagent can't see the conversation the handoff summarizes. The progress tracker ignores this skill (SPEC-013 BEH-02, version 18), so a tracked run open in the session stays open, and the handoff names it with its step."
  - id: BEH-02
    status: active
    rule: "Check the live state before writing anything, with read-only commands: the repository's branch, last commits and uncommitted changes (git), its open pull requests and their state where gh is available, any tracked run's status the project shows (devforgeai/progress/sessions/<session>/current.json when it exists), and the checks the project's instructions name as its tests, only when they are quick and read-only; otherwise cite their last recorded result with its date and mark it (unverified). Read the project's CLAUDE.md files and any earlier devforgeai/handoff/ files first. A fact the session believes but didn't check now goes into the handoff marked (unverified)."
  - id: BEH-03
    status: active
    rule: "Save the session's new, durable learnings to memory when the session's instructions describe a memory system (a memory location and its format): follow that format exactly (for Claude Code's memory, one fact per file with its frontmatter, an index line, written with Write or Edit), update an existing memory that covers the same fact rather than adding a duplicate, and save only what the repository and its instructions don't already record: decisions with their reasons, verified facts about tools and the environment, practices the user asked for or confirmed, and traps that cost time. When the session has no memory system, put the learnings in START-HERE §6 instead and say so in the report. Never save secrets or credentials."
  - id: BEH-04
    status: active
    rule: "Update devforgeai/handoff/TASKS.md (DM-02) from the template assets/tasks.md when it doesn't exist: mark what this session finished as done, with its evidence (commit, pull request, file or test result), and list what is next with its next action. Keep every done entry of an earlier TASKS.md, with its evidence; never delete history."
  - id: BEH-05
    status: active
    rule: "Write devforgeai/handoff/START-HERE.md (DM-01) from the template assets/start-here.md, replacing an earlier one after carrying over what still holds from it (decisions, rules and traps, outstanding items not finished). Write it in full fidelity (§4): every fact verified or marked (unverified), exact identifiers, absolute dates, no pronoun whose referent the next session can't see. Use progressive disclosure: name files with why and when to read them, and searches to run, instead of copying their content in; copy in only what exists nowhere else (a decision said only in the conversation, a result not saved to a file). Quote the user's words for each decision, with the date. Put the user's argument, if any, at the top of §5."
  - id: BEH-06
    status: active
    rule: "Write devforgeai/handoff/RESUME-PROMPT.md (DM-03) from the template assets/resume-prompt.md: at most 40 lines, sending the next session to START-HERE.md first, then TASKS.md, then START-HERE's 'Before acting' check, then the first outstanding item, asking the user before any decision START-HERE §3 or §5 says is theirs. Write devforgeai/handoff/.gitignore holding * when it is missing."
  - id: BEH-07
    status: active
    rule: "Never turn outstanding work into a decision: an item waiting for the user's choice says so, with the options as the user saw them, and the handoff never records a choice the user didn't make. Follow any further pre-compaction duty the project's or the user's instructions name (for example a log the user keeps), citing the instruction."
  - id: BEH-08
    status: active
    rule: "Run python3 ${CLAUDE_SKILL_DIR}/scripts/check_handoff.py (IF-01) as a command of its own. On exit 1, fix each problem it lists in the file it names and run it again, until it exits 0; on exit 2, the files weren't written: write them (BEH-04 to BEH-06) and run it again. Then read START-HERE.md back against the self-check list in references/handoff-rules.md, which covers what the script can't: facts verified, decisions attributed, the next action of each outstanding item concrete."
  - id: BEH-09
    status: active
    rule: "Report, in the reply: the paths written, the memories saved or updated (or why none), anything left marked (unverified), and the text of RESUME-PROMPT.md in one fenced block, so the user can paste it after /compact. Change no file but the three handoff files, the handoff .gitignore and memory files."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The project isn't a git repository, or git or gh isn't available"
    handling: "Skip those checks, say which in START-HERE §2, and mark the state facts that depend on them (unverified)"
    user_result: "A handoff that says what couldn't be checked"
  - id: ERR-02
    status: active
    condition: "devforgeai/handoff/ can't be written"
    handling: "Say so, quoting the error, and give the three files' content in the reply instead, so the user can save them"
    user_result: "The handoff in the reply"
  - id: ERR-03
    status: active
    condition: "check_handoff.py can't run (no python3)"
    handling: "Say so, and read the three files back against references/handoff-rules.md's full self-check list, including the script's checks"
    user_result: "A handoff checked by reading, and the reason"
  - id: ERR-04
    status: active
    condition: "The session's instructions describe no memory system, or a memory write is refused"
    handling: "Put the learnings in START-HERE §6 and say so in the report (BEH-03)"
    user_result: "The learnings in the handoff, and the reason"
  - id: ERR-05
    status: active
    condition: "An earlier handoff in devforgeai/handoff/ belongs to other work (another branch or topic)"
    handling: "Keep its TASKS.md entries under a heading naming that work, and write START-HERE for the current work, naming the earlier work in §5 as not continued here"
    user_result: "Both lines of work kept, the current one first"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds the checklist and the decisions that are the user's; the full-fidelity rules and the self-check list live in references/handoff-rules.md, the memory guidance in references/memory.md, the shapes in assets/"
    measured_by: "SKILL.md line count (at most 500) and description length (at most 1024 characters)"
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
    response: "One eval case per automated VER item, tagged precompact and ver-NN, run against the no-plugin baseline: one run per case at 0.8 or above (Bryan, 2026-10-05: 'Full cycle, 1-run evals'; the 3-run qualification waived)"
    measured_by: "claude plugin eval --threshold 0.8 --runs 1"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 11, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: this spec against `spec.schema.json` | Not run yet |

Each automated VER item has one eval case under `evals/precompact/`, tagged `precompact` and `ver-NN` and generated by
`src/tests/precompact/make_evals.py`. An eval run starts in an empty workspace with no earlier conversation, so each
case's scaffold builds the work to hand off (a git repository with commits, a plan file, an open task) and its prompt
states what the session did, as a user would before compacting. Eval runs offer no AskUserQuestion and seal the home
folder, so memory and asking are checked live (VER-07).

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "src/tests/precompact/test_check_handoff.py, every case normally and under python3 -S: a complete handoff exits 0 with 'handoff: clean'; each of a missing file, a missing or misordered heading, an empty §5, a 41-line RESUME-PROMPT.md, one that doesn't name START-HERE.md, a leftover placeholder, a backticked path that doesn't exist (and the same path marked (not yet created) or (session-only), which passes), and a missing .gitignore exits 1 with a '<file>:<line>: <problem>' line; no devforgeai/handoff/ folder exits 2"
    level: unit
    covers:
      - IF-01
      - BEH-08
  - id: VER-02
    status: active
    obligation: "Case writes-handoff: a scaffolded git repository with three commits, a plan file and an unfinished task; the prompt says what the session did and asks to prepare for /compact. The three files and the .gitignore are written in devforgeai/handoff/; check_handoff.py exits 0; START-HERE §2 names the branch and the last commit's hash as git reports them; §5 lists the unfinished task with a next action; RESUME-PROMPT.md names START-HERE.md and is at most 40 lines; no file outside devforgeai/handoff/ (and memory) changes"
    level: integration
    covers:
      - BEH-01
      - BEH-02
      - BEH-04
      - BEH-05
      - BEH-06
      - BEH-09
  - id: VER-03
    status: active
    obligation: "Case updates-earlier-handoff: the scaffold holds an earlier TASKS.md with two done entries and an earlier START-HERE.md whose §3 records a decision in the user's words; after the run both done entries remain with their evidence, the session's finished work is added as done, and the decision is still in §3 with its quote"
    level: integration
    covers:
      - BEH-04
      - BEH-05
  - id: VER-04
    status: active
    obligation: "Case decisions-stay-open: the prompt says the user hasn't chosen between two options for the next step; START-HERE records that choice as waiting for the user, with both options, and records no choice; the same case's prompt names a fact the session believes but didn't check, which appears marked (unverified)"
    level: integration
    covers:
      - BEH-02
      - BEH-05
      - BEH-07
  - id: VER-05
    status: active
    obligation: "Case no-git: the scaffold isn't a git repository; the handoff is written, START-HERE §2 says git couldn't be checked, and check_handoff.py exits 0"
    level: integration
    covers:
      - ERR-01
  - id: VER-06
    status: active
    obligation: "Trigger cases: 'I'm at 85% context: save what we learned and write a handoff before I compact.', 'Write a start-here document for the next session.' and 'Prepare for /compact.' load devforgeai:precompact; 'Write release notes for this version.' and 'Summarize this file for me.' don't"
    level: integration
    covers:
      - BEH-01
  - id: VER-07
    status: active
    obligation: "Live, in a real session past 80% context on real work, with Claude Code's memory on and a tracked brainstorm or architecture run open: /devforgeai:precompact leaves the tracked run open (its band unchanged; SPEC-013 VER for BEH-02 v18), saves at least one new learning as a memory file with its index line in the session's memory folder and duplicates none, and writes the handoff; after /compact, pasting RESUME-PROMPT.md's text has the session read START-HERE and TASKS, run the 'Before acting' check, and go on with the first outstanding item without asking the user for anything the handoff holds. Recorded in §9."
    level: manual
    covers:
      - BEH-03
      - BEH-01
      - ERR-04
  - id: VER-08
    status: active
    obligation: "src/tests/precompact/test_structure.py: SKILL.md at most 500 lines, its frontmatter equal to §5's fields and valid per skill-frontmatter.schema.json, metadata devforgeai-tracked 'false', devforgeai-version equal to provenance.yaml's version, provenance valid per skill.schema.json with SKL-012 implementing SPEC-015, every reference and asset SKILL.md names existing, the three assets holding DM-01 to DM-03's headings, and SKILL.md or its references stating ERR-02's, ERR-03's and ERR-05's handling (the handoff in the reply when the folder can't be written; reading back when the script can't run; an earlier handoff of other work kept under its own heading)"
    level: unit
    covers:
      - QR-01
      - QR-02
      - ERR-02
      - ERR-03
      - ERR-05
  - id: VER-09
    status: active
    obligation: "QR-03: every case of VER-02 to VER-06 at 0.8 or above in one run with the no-plugin baseline"
    level: integration
    covers:
      - QR-03
```

## 10. Rollout, migration and rollback

- **New skill, nothing to migrate.** It ships in the next plugin version after approval and build (0.26.0, the next
  free minor, set at merge on Bryan's word), with SPEC-013 version 18. Rolling back is removing `skills/precompact/`,
  its evals and tests, the CLAUDE.md row, and SPEC-013 v18's clause.
- **The tracker.** SPEC-013 version 18 (BEH-02): a skill marked `devforgeai-tracked: "false"` isn't tracked.
- **Codex.** The Codex port isn't changed; a port is for Codex sessions to build.
- **Records.** CLAUDE.md's skill table gains a `precompact` row (SKL-012, SPEC-015).

## 11. Implementation plan

After approval, through `/plugin-dev:skill-development` (and `/plugin-dev:create-plugin`), on branch `docs/precompact`
in `.claude/worktrees/precompact` (ADR-001):
1. Write `src/tests/precompact/test_check_handoff.py` (VER-01) and `test_structure.py` (VER-08), and see them fail.
2. Write `scripts/check_handoff.py` until VER-01 passes, normally and under `python3 -S`.
3. Write the assets (DM-01 to DM-03), `references/handoff-rules.md` and `references/memory.md`, `SKILL.md` from §5
   and §6 (lean, imperative, the checklist first), and `provenance.yaml` as SKL-012; VER-08 passes.
4. SPEC-013 version 18's kit tests first, then BEH-02's untracked skills in `hooks/progress.tsx`.
5. Write `src/tests/precompact/make_evals.py` with the scaffolds and the cases of VER-02 to VER-06; generate them.
6. Run skill-reviewer and plugin-validator; take any finding that would refuse valid work to Bryan.
7. Evaluate cheapest first, then VER-09's one-run suite; run VER-07 live; record the results in §9.

## 12. Alternatives considered

| Option | Why not chosen |
| --- | --- |
| A subagent writes the handoff (as spec-lookup's lookups run) | A subagent sees none of the conversation the handoff must summarize |
| Keep the tracker as is | Typing the skill in the middle of a tracked run would end that run (SPEC-013 BEH-03); Bryan chose "Yes, the tracker ignores it" |
| One START-HERE.md only | Bryan chose the three files ("START-HERE + TASKS + resume prompt"): the paste-in prompt stays short and points to the master |
| `tmp/plans/` or committed `docs/handoff/` | Bryan chose `devforgeai/handoff/`, gitignored: other projects may not ignore `tmp/`, and the handoff is working notes, not a project document |
| Running it from the compaction hook now | Bryan: "eventually, it may run with the precompact hook"; recorded in §13 |

## 13. Open questions

Decided by Bryan on 2026-10-05 (`/plugin-dev:skill-development` Step 1, "generate a skill for the pre-compaction
workflow you performed. name it /devforgeai:precompact. include templates to provide proper guidance for subsequent
sessions such as tasks.md or start-here.md..."): "Full cycle, 1-run evals (Recommended)"; the purpose and content
quoted in §1; "Yes, the tracker ignores it (Recommended)" (SPEC-013 version 18); "devforgeai/handoff/
(Recommended)"; "START-HERE + TASKS + resume prompt (Recommended)".

Recorded for later: running the skill, or a check that the handoff is current, from a compaction hook (Bryan:
"eventually, it may run with the precompact hook"); the tracker's adapter already sees `session.compact` (SPEC-013
BEH-24).

Drafter's choices, for Bryan's accept or challenge: Claude may load the skill on its own when the user's words match
its description (no `disable-model-invocation`), so "prepare for compact" works as well as the command; the template
headings of DM-01 (seven sections, from this session's own handoff of 2026-10-05); the 40-line limit of the resume
prompt; the check script's rules (IF-01), including that an absolute path outside the project is reported, not
refused; the gitignored folder holding working notes only.

## Change Log

| Version | Date | Author | Change | Items affected |
| --- | --- | --- | --- | --- |
| 1 | 2026-10-05 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Drafted from Bryan's decisions of 2026-10-05 (`/plugin-dev:skill-development`, "Full cycle, 1-run evals", the purpose and content in his words, the tracker ignores it, devforgeai/handoff/, three files); status in-review | all |
