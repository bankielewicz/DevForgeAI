# The work file

A copy of the brainstorm as it stands, saved as the session goes, so that a run the progress tracker
continues later has the problems, ideas, scores and proposals, not only the step it stopped at. It is
a work copy, never the BRN: nothing downstream reads it, the validator doesn't check it, and the
skill never deletes it (the progress tracker does, once the BRN validates, and removes old ones).

## Contents

- [Where it lives](#where-it-lives)
- [When to write it](#when-to-write-it)
- [Its shape](#its-shape)
- [Continuing a run](#continuing-a-run)

## Where it lives

The path SKILL.md's *Inputs* gives: `devforgeai/drafts/brainstorm/<session ID>.md`, with the same
session ID as the BRN's `generated_by.session`. Never under `docs/specs/`: the progress tracker treats a write there as the
BRN's own (step 6) and would refuse it in enforce mode.

Before the first write, when `devforgeai/drafts/.gitignore` is missing, write it with the single line
`*`, so no work file reaches git.

## When to write it

Write the whole file with the Write tool, three times:

1. After marking step 3 completed and before marking step 4 in progress: problems, ideas and
   assumptions.
2. After marking step 4 completed and before marking step 5 in progress: the evaluation and scores
   added.
3. With step 5 in progress, once the proposals are made: before asking step 5's question, or, when no
   question is asked (the waiver's *Proceed without questions*, or no AskUserQuestion), right away.

When ERR-02's draft BRN is saved on a stop (step 5's stop question), write the work file once more
with its `id` set to that BRN's ID, so a continued run extends that BRN instead of allocating another.

## Its shape

Build it from `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`, as step 6 builds the BRN, except:

- `id`: `BRN-000` (the template's placeholder) for a new BRN. When extending an existing BRN, or after
  ERR-02 saved a draft BRN, that BRN's ID: this is what tells a continued run to extend it.
- `title`: the topic. `status: draft`. `version`: 1 for a new BRN, or the extended BRN's version.
- `generated_by.session` and one Change Log row: this session's, as step 6 writes them.
- Every idea `disposition: open`, `reason: null`. A proposal is never a disposition value.
- Sections not reached yet hold `[NEEDS CLARIFICATION: not reached]`.
- Step 5's proposals, once made, as a table in section 6 (Convergence): idea ID, title, proposed
  disposition, reason. Write it in table cells only, never as a `disposition:` line.
- No HTML comments.

When extending, start from the existing BRN's content with every item ID kept.

## Continuing a run

When the text of this skill ends with the progress tracker's line that continues an earlier brainstorm
run (it begins "This run continues the earlier brainstorm run"):

1. Read no work file when the line's step to continue at is past step 6, or when it carries step 5 as
   decided (no "confirm each with the user again" sentence naming step 5): the BRN was written.
2. Otherwise, take the last path under `devforgeai/drafts/brainstorm/` that the line's "Files it
   wrote" names, and read it. If none is named or it can't be read, continue as the line says without
   it.
3. Before anything else, write its content unchanged to this session's work file path, so a later
   continuation finds it.
4. Work from it: keep its problems, ideas, assumptions, scores and IDs. When its `id` is a BRN's ID,
   step 6 extends that BRN (version + 1, a Change Log row for this session) without asking
   extend-or-new again; otherwise step 6 allocates the ID as usual.
5. When the line asks to confirm step 5 again and the file holds step 5's proposals, ask step 5's
   question with those same proposals.

A run that is not continued (no such line, or the user chose Start fresh) reads no work file, and no
run ever reads another session's work file except the one its line names.
