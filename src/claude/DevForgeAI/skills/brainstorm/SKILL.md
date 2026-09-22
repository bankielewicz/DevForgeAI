---
name: brainstorm
description: Runs a structured brainstorming session and writes a DevForgeAI brainstorm (BRN) document with identified problems, ideas, assumptions and user-confirmed dispositions. Use when the user wants to brainstorm, explore ideas or options, generate ideas for a product or feature, or start the DevForgeAI planning chain before a PRD.
argument-hint: "[topic]"
metadata:
  devforgeai-id: "SKL-001"
  devforgeai-version: "1"
---

# Brainstorm

Run a brainstorming session on one topic and write it as a BRN document,
`docs/specs/brainstorms/BRN-NNN-<slug>.md`, that a PRD can cite item by item.

## Inputs

- `$ARGUMENTS`: the topic. When it is empty, take the topic from the conversation. If there is
  none, ask for it (step 1).
- `docs/specs/brainstorms/`: existing BRN files, read for ID allocation and duplicate topics.
- `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`: the BRN template.
- `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md`: the framework catalog.
- `${CLAUDE_SKILL_DIR}/references/output-rules.md`: the rules the written file must satisfy.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Take in the topic
- [ ] 2. Check existing BRNs and allocate the ID
- [ ] 3. Select the framework
- [ ] 4. Diverge: problems, ideas, assumptions
- [ ] 5. Evaluate and propose dispositions
- [ ] 6. Write the BRN
- [ ] 7. Validate the BRN
- [ ] 8. Report and hand off
```

**Interactive or not.** The session is *non-interactive* when the request says to proceed without
questions, or when no one can answer (for example, in an automated run). In a non-interactive
session, ask no clarifying questions, and write the BRN with every disposition `open` and `status: draft`.
Two questions are never skipped: the topic when there is none (step 1), and extend-or-new when a
similar BRN exists (step 2). Both stop the session until they are answered, and nothing is written meanwhile.

### 1. Take in the topic

1. Find the topic in `$ARGUMENTS` or the conversation. If there is none, ask "What topic should we
   brainstorm?" and **end your turn**. Write no file and create no directory until a topic is given.
2. Ask at most three clarifying questions, in one message: what triggered this, who is affected, and
   what constraints apply. Skip any the request already answers. If you ask, end your turn and wait for the
   answers. Ask none in a non-interactive session.
3. Record whatever is still unknown as `[NEEDS CLARIFICATION: <question>]`, with the question written out.
   Never guess.

### 2. Check existing BRNs and allocate the ID

1. Glob `docs/specs/brainstorms/BRN-*.md`. Read the `title` of each match.
2. If one covers the same or a closely similar topic (by title or slug, not only an exact match),
   show its path and title, and ask: **extend it** (its `version` goes up by one, with a Change Log
   entry) **or create a new BRN**? End your turn and wait for the answer. Never overwrite a BRN, and
   never pick either option yourself.
3. For a new BRN, take the highest `BRN-NNN` number found plus one, or `BRN-001` if there is none. Derive the
   slug from the topic: lowercase, hyphenated, at most five words. If the user names the file, use that name,
   provided it has this form and the allocated number. If `docs/specs/brainstorms/` is missing,
   create it when you write the file (step 6), and tell the user it was created.
4. When extending, keep every existing item ID and its meaning. New items take the next free number in their
   collection. Retire an item with `status: deprecated`; never delete or renumber one, because PRD
   requirements cite these IDs.

### 3. Select the framework

1. Read `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md`. Use the framework the user named, or else the
   row whose *use when* best fits the topic. Use `diverge-converge` when nothing fits better.
2. Read the chosen framework file from the same directory, and follow its steps, questions and BRN mapping.
3. Tell the user which framework you chose, in one sentence with the reason. Switch if they ask.
4. If the index is missing, or the chosen file is missing or lacks one of the sections the index lists, use
   `${CLAUDE_SKILL_DIR}/references/frameworks/diverge-converge.md`, and name the file that was the problem.

### 4. Diverge: problems, ideas, assumptions

1. Capture the problems behind the topic, from the affected users' side.
2. Capture ideas. Record the user's own ideas in their words, next to generated ones. Generate
   5 to 15 ideas in total unless the user asks for another number. Every idea starts `disposition: open`.
3. Capture the assumptions the promising ideas depend on, each with a way to validate it.

Whatever the framework, write only into the `problems`, `ideas` and `assumptions` collections and their
defined fields. Framework-specific reasoning goes in the prose of sections 5 and 6, never in new YAML keys.

### 5. Evaluate and propose dispositions

1. Fill `value`, `effort`, `risk` and `score` on each idea, as the framework's mapping says.
2. For each idea, propose a disposition (`promoted`, `parked` or `rejected`) with a one-line reason.
3. **Interactive:** show the proposals and ask the user to confirm or change them, and whether the brainstorm
   has converged. Wait for the answer.
4. **Non-interactive:** don't wait. Keep every disposition `open` and `reason: null` in the file, and list
   the proposals in your final reply as awaiting confirmation.

### 6. Write the BRN

1. Read `${CLAUDE_SKILL_DIR}/references/output-rules.md` if you haven't already.
2. **New BRN:** if the target path already exists, stop and ask; never overwrite. Otherwise build the file from
   `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`. Keep every section heading. Replace every placeholder, or mark it
   `[NEEDS CLARIFICATION: <question>]` with the question written out. Delete every HTML author comment.
3. Fill the frontmatter:
   - `id` is the allocated `BRN-NNN`. `title` is the topic. `created` and `updated` are today's date.
   - `generated_by.tool` is `claude-code`, `generated_by.model` is your current model ID, and
     `generated_by.session` is `${CLAUDE_SESSION_ID}`.
   - `authors` is the user's name and `claude-code`. `owner` is the user's name. Ask for it only if the
     conversation doesn't give it. In a non-interactive session without it, write `authors: ["claude-code"]`
     and `owner: "[NEEDS CLARIFICATION: owner]"`.
   - `reviewed_by: []`. Every `hash` is `null`. `approved_by: ""`, `approved_on: null`.
   - `status` is `converged` only if the user confirmed convergence. Otherwise it is `draft`.
4. Write each `disposition` and `reason` **only as the user confirmed it**. Every other idea stays `open`
   with `reason: null`.
5. Record the evaluation method (the framework's *Evaluation method text*) in section 5. In section 6, record the
   proposals and what the user confirmed. Fill section 8 with outcome signals drawn from the promoted (or
   proposed) ideas, or one `[NEEDS CLARIFICATION: …]` marker. In section 7, delete the marker bullet if no
   question is open.
6. **Extending a BRN** (the user chose it in step 2): edit the existing file in place. Keep `id`, `created` and
   every existing item. Set `updated` to today, add 1 to `version`, and append a Change Log row. Keep every
   disposition already in the file, and apply only the ones the user confirmed in this session.

### 7. Validate the BRN

1. If you can run shell commands, run `devforgeai check --json <file>`. If it prints JSON (whatever the exit
   code), fix every error it lists. If it prints no JSON (not found, or some other program), or you can't run
   commands, check the file instead against the **Self-check list** in `output-rules.md`, reading the file back first.
2. Fix every problem found, then check again. Stop after three attempts.
3. If errors remain after three attempts, leave `status: draft`, and list the file path and the remaining errors
   in your reply.

### 8. Report and hand off

1. Report: the BRN path; the framework used, by name; how many problems, ideas and assumptions it holds; the ideas promoted (or, if none
   were confirmed, the proposed dispositions awaiting confirmation); and the open questions (`[NEEDS CLARIFICATION]` markers).
2. Name the next step. Check whether `${CLAUDE_PLUGIN_ROOT}/skills/prd/SKILL.md` exists.
   - If it does: tell the user to run `/devforgeai:prd <BRN path>`.
   - If it doesn't: say the PRD step isn't available yet: the PRD workflow, planned as `/devforgeai:prd`, isn't
     built. Say this BRN is its input, and give the path. Don't present it as a command to run now.
3. Never start writing a PRD.

## Stopping early

If the user stops mid-session, ask whether to save what has been captured as a draft BRN. If yes, write it
(steps 6 and 7) with `status: draft` and every disposition `open`. If no, write nothing.

## Decisions that need the user

- **Dispositions and convergence:** propose them, and write only what the user confirms (step 5).
- **Extend or new** when a similar BRN exists: ask, and never overwrite (step 2).
- **The topic**, when none is given: ask, and write nothing until it arrives (step 1).
- **Saving a draft** when the user stops early: ask (Stopping early).
- **The owner**, when the conversation doesn't give it (step 6).

You decide on your own: the framework (the user can override it), the BRN number and slug, the generated ideas,
and the proposed ratings.

## Output contract

- Path: `docs/specs/brainstorms/BRN-NNN-<slug>.md`, with the ID from step 2.
- Content: the template `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`, filled in, with every heading kept.
- Item blocks: only `problems` (`PRB-NN`), `ideas` (`IDEA-NN`) and `assumptions` (`ASM-NN`), with the fields in
  `output-rules.md`. At least one problem and one idea.
- Provenance: `generated_by` complete, `reviewed_by: []`, every `hash: null`.
- Dispositions other than `open` exist only when confirmed. `status: converged` only when convergence was confirmed.
- The PRD workflow consumes this file and cites its item IDs, so an ID never changes meaning.

## References

- [frameworks/INDEX.md](references/frameworks/INDEX.md): read in step 3, every session.
- [output-rules.md](references/output-rules.md): read before writing (step 6) and when validating (step 7).
