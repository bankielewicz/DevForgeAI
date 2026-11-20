# Brownfield: brainstorming about a product that exists

Read this at step 1 when the project kind is brownfield, decided or worked with
([intake.md](intake.md#project-kind)). It never applies to a BRN without the `Project kind:` line.
Everything you read here is read-only: never edit, repair, move or delete a document you read, an earlier
BRN included.

## Contents

- [Extend or new](#extend-or-new)
- [What to read](#what-to-read)
- [Existing product (section 1)](#existing-product-section-1)
- [Already covered](#already-covered)
- [Previously decided](#previously-decided)
- [Reporting what was kept out, and the override](#reporting-what-was-kept-out-and-the-override)
- [Parked ideas](#parked-ideas)
- [Earlier assumptions](#earlier-assumptions)
- [Assumption updates](#assumption-updates)
- [Extending a brownfield BRN](#extending-a-brownfield-brn)
- [When nothing can be asked](#when-nothing-can-be-asked)

## Extend or new

When the user's words say the product exists (intake.md, rule 2), a BRN is "on the same topic" at
Intake 2 only when both hold: its `title` covers the same or a closely similar topic, and its `status` is
`draft`. Ask extend-or-new for such a BRN only. A `converged` or `archived` BRN is never extended on
your own motion: it is an earlier brainstorm to read, and this run writes a new BRN. When the user asks
in words to extend a BRN by its ID, extend it, whatever its status.

| Earlier BRN | Request | Result |
|---|---|---|
| BRN-001, `converged`, "Reducing appointment no-shows at the dental clinic" | "Our booking site is live. Brainstorm how to reduce no-shows further." | No question. New BRN-002; BRN-001 is read |
| BRN-003, `draft`, "What to improve next in online booking" | "Our booking site is live. Brainstorm what to improve next in online booking." | Ask: extend BRN-003, or create a new BRN |

## What to read

Right after the kind is decided or worked with, and before the clarifying questions, select files by
name with Glob, then read each selected file whole with the Read tool, in this order:

| Order | Glob | Take | At most |
|---|---|---|---|
| 1 | `docs/specs/brainstorm/BRN-*.md` | the highest numbers, highest first; never the BRN being extended | 3 |
| 2 | `docs/specs/prd/PRD-*.md` | the highest numbers, highest first | 2 |
| 3 | `docs/specs/epic/EPIC-*.md` | the highest numbers, highest first | 4 |
| 4 | `docs/specs/arch/ARCH-*.md` | the highest number | 1 |

Only a file named `<PREFIX>-NNN.md` (three digits) is selected. Read nothing else for this purpose: never
read a story, a spec, an ADR or source code on your own account, and never glob `docs/specs/story/` or
`docs/specs/spec/`. Ten documents is the cap; a file beyond a row's limit is not read. A file the user names
as a source is another matter: read it as [intake.md](intake.md#sources) says. It gets a `document` entry in
`sources` and never a row of *Existing product*.

**Skip a document you can't use**, and never repair it. Test in this order and stop at the first that
fails; the words in parentheses are the reason you record:

1. the Read tool returns its content (`could not be read`);
2. it starts with a `---` line and has a closing `---` line (`no frontmatter`);
3. its frontmatter `id` equals the file name without `.md` (`id does not match the file name`);
4. its frontmatter `version` is a positive integer (`no version`).

A skipped document is not replaced by another, gets no `upstream` record and no `sources` entry, and is
named in section 1 and in the final reply.

**What you take from each document read:**

| Document | Take |
|---|---|
| BRN | `title`, `version`; each active idea's `id`, `idea`, `disposition`, `reason`; each active assumption's `id`, `statement`, `validation`, `state` |
| PRD | `title`, `version`; section 1 (Summary); each active functional and non-functional requirement's `id`, `statement`, `priority` |
| EPIC | `title`, `version`; each active `done_when` item's `id`, `criterion` |
| ARCH | `title`, `version`; each active component's `id`, `name`, `responsibility` |

Copy no disposition, priority or decision from them into this BRN's items.

**Record each document read**, in the order read:

- one frontmatter `upstream` record, with no `item`:
  `- {id: PRD-001, relation: informed_by, version: 3, hash: null}`;
- one `sources` entry, `"document: docs/specs/prd/PRD-001.md v3"` (the folder is `brainstorm`, `prd`,
  `epic` or `arch`). In a BRN this run creates, put these entries before every other `sources` entry;
  when extending, append them ([Extending a brownfield BRN](#extending-a-brownfield-brn)).

## Existing product (section 1)

After the context prose, write:

```markdown
### Existing product

| Document | Version | What it already covers |
|---|---|---|
| BRN-001 | 1 | Reducing appointment no-shows at the dental clinic: 6 ideas (2 promoted, 2 parked, 2 rejected, 0 open) |
| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006) |

Skipped: docs/specs/prd/PRD-002.md (no frontmatter)
```

- One row per document read, in the order read. `Document` is its ID, `Version` its `version`.
- The third cell, with any `|` in a title replaced by `/`:
  - BRN: `<title>: <n> ideas (<p> promoted, <k> parked, <r> rejected, <o> open)`, counting active ideas;
  - PRD: `<title> (<first FR ID> to <last FR ID>)`, counting active functional requirements; with one,
    `(<its ID>)`; with none, `(no functional requirement)`;
  - EPIC: `<title> (<first DW ID> to <last DW ID>)`, by the same rule, else `(no done-when item)`;
  - ARCH: `<title> (<first CMP ID> to <last CMP ID>)`, by the same rule, else `(no component)`.
- With no document read, write the line `No document was found in the project.` in place of the table,
  and tell the user once: "I found no DevForgeAI document in this project, so I work from what you tell me
  about the product."
- After the table or that line and one blank line, one line per skipped document, in the order met:
  `Skipped: <path from the project root> (<reason>)`.

The context prose says what the product does today only from a PRD's Summary or the user's words;
otherwise write `[NEEDS CLARIFICATION: what the product does today]`.

## Already covered

At step 3, test every candidate idea before it gets an ID: each suggestion of the user's, and each idea
you generate. A candidate is **covered** when one item you took from a PRD, EPIC or ARCH, read as it is
written, already gives the same people the same result. The items that count are active functional and
non-functional requirements whose `priority` is not `wont`, active done-when items, and active
components. Check PRD items first, then EPIC, then ARCH, each in ID order, and cite the first that
covers it. This is a judgment; apply it this way:

| Candidate | Item | Covered? |
|---|---|---|
| "Text reminders before a visit" | FR-003 "The system shall send a text reminder two days before each booked visit." | Yes |
| "Remind patients by text and by email" | the same FR-003 | No: the email half is not covered. The whole candidate becomes an idea |
| "Let new patients book online" | FR-001 "The system shall let a returning patient book a free slot online." | No: other people |

A covered candidate is not added to `ideas`, even when the user suggested it. List it in section 6:

```markdown
### Already covered

| Suggestion | Covered by |
|---|---|
| Text reminders before a visit | PRD-001#FR-003 |
```

- `Suggestion`: the user's words, or your candidate's wording, with `|` replaced by `/`.
- `Covered by`: `<document ID>#<item ID>`. A document with no item that covers the candidate covers
  nothing: the candidate becomes an idea.
- Rows in the order the candidates came up. With no row, the line `None.` replaces the table.

Generate as the framework's *Steps* say (5 to 15 ideas unless they set their own count); covered and
previously decided candidates don't count toward it. A framework that generates no idea of its own
(`shortlist-ranking`) generates none in place of a candidate kept out: test each candidate of the user's
list the same way, keep a covered or previously decided one out, and list it.

## Previously decided

Test every candidate against each active idea of the BRNs read whose `disposition` is `rejected`: it is
the **same idea** when it proposes the same action for the same people. Such a candidate is not added
to `ideas`, even when the user suggested it.

| Candidate | Earlier idea | Same? |
|---|---|---|
| "Take a deposit when a patient books" | BRN-001#IDEA-06 "Charge a deposit at booking." (rejected) | Yes |
| "Charge a fee for a missed visit" | the same IDEA-06 | No: charged after, not at booking |

List in section 6 each rejected idea that came up again, and each parked idea that was not taken up
([Parked ideas](#parked-ideas)):

```markdown
### Previously decided

| Idea | Decision | Where |
|---|---|---|
| Open a waitlist for freed slots. | parked | BRN-001#IDEA-05 |
| Charge a deposit at booking. | rejected | BRN-001#IDEA-06 |
```

- `Idea`: the earlier idea's `idea` text, with `|` replaced by `/`. `Decision`: `rejected` or `parked`.
  `Where`: `BRN-NNN#IDEA-NN`.
- Rows ordered by `Where`. With no row, the line `None.` replaces the table.

## Reporting what was kept out, and the override

**Report with the exact ID, and ask nothing.** When step 3's work is done, write one line in the reply for
each candidate kept out, in the order they came up, then the last sentence once:

```text
Not added, already covered by PRD-001#FR-003: "text reminders before a visit"
Not added, rejected in BRN-001#IDEA-06: "taking a deposit when a patient books"
Say "add it anyway" to add one.
```

- A covered candidate: `Not added, already covered by <document ID>#<item ID>: "<the suggestion>"`.
- A previously decided one: `Not added, rejected in BRN-NNN#IDEA-NN: "<the suggestion>"`.
- Repeat the lines and the sentence in the final reply's discussion for every candidate still kept out.
- Never ask about a kept-out candidate, in a form or in text, and never wait for an answer: go on.

**The user overrides by saying so**, at any time after a report. An override is a message that tells you to
add a kept-out candidate:

| The user's message | Do |
|---|---|
| "add the text reminders anyway", or one that names the candidate by its ID | Add that candidate |
| "add it anyway", with exactly one candidate kept out | Add it |
| "add them anyway", "add both", "add all" | Add every candidate kept out |
| "add it anyway", with several kept out and none named | Add nothing. Say: Several suggestions were kept out. Name the one to add, for example "add the text reminders anyway". |
| "why is it covered?", "ok" | Add nothing; answer the question when there is one |

**An override writes this:**

- the candidate becomes an idea, in the user's words (your wording for a candidate of your own), with the
  next free ID and `disposition: open`; rate it at step 4 like any other;
- its row is removed from its table, which becomes the line `None.` when that was the last row;
- a previously decided idea gets the item-level link shown under [Parked ideas](#parked-ideas);
- section 6's prose gains one sentence: `IDEA-NN was added at the user's request although
  <document ID>#<item ID> covers it.` or `IDEA-NN was added at the user's request although
  BRN-NNN#IDEA-NN rejected it.` Write "the user's" as it stands, never a name.

Before the BRN is written, do this in the work as it stands. After it is written, in the same session, edit
the BRN in place as SKILL.md's *Decisions that belong to the user* says for a later confirmation: mark step
6, edit, validate again at step 7 and report at step 8. Don't ask step 5's form again: the new idea is
`open`. In a later session it is an extension of that BRN.

## Parked ideas

Offer once, at step 3, after the problems are framed and before you generate ideas, when the BRNs read
hold at least one active idea with `disposition: parked` and you can ask. One form tagged step 3
(`metadata: {"source": "devforgeai_step:3"}`), one question with `header: "Step 3"`:

- Question: "Take up parked ideas from earlier brainstorms?"
- Options, in this order: `Take up none` and `Take up all`. Each option's `preview` lists every parked
  idea, one per line, as `BRN-001#IDEA-04: <its idea text>`. Names typed under Other take up those
  ideas only: a qualified `BRN-NNN#IDEA-NN`, or a bare `IDEA-NN` that matches exactly one idea listed.
- A bare ID that matches parked ideas of more than one BRN: ask once more, in a form with the same tag
  and header, "Which IDEA-NN do you mean?" (with the ID), one option per matching idea labelled with its
  qualified form, `multiSelect: true`. When you can't ask, or it is dismissed or not answered, don't
  take that idea up: it stays a `parked` row of *Previously decided*.

Without AskUserQuestion, list them in plain text, ask the same question and end your turn. A dismissal
takes up none.

Each idea taken up becomes a new idea of this BRN: the next free ID, `idea` copied word for word,
`addresses` naming the problems of this BRN it bears on, `value`, `effort`, `risk` and `score` rated
afresh at step 4, `disposition: open`, and an item-level link to where it came from:

```yaml
    upstream:
      - {id: BRN-001, item: IDEA-04, relation: informed_by, version: 1, hash: null}
```

An idea taken up that bears on no problem of this BRN is not added: it stays in *Previously decided*,
and you say so. Ideas taken up don't count toward the framework's idea count. An idea that has the link is
never also a row of *Previously decided*.

## Earlier assumptions

At step 3, after the problems, show in the reply each active assumption of the BRNs read whose `state`
is `open`, one per line: `BRN-001#ASM-01: <statement> (to validate: <validation>)`. Ask nothing about
them.

## Assumption updates

At step 5, before the form, propose a change of state only from a stated fact with a source. For each
assumption shown at step 3, look through this run's `sources` for a fact that reports the result the
assumption's `validation` asks for:

| The fact | Proposal |
|---|---|
| reports that result and agrees with the `statement` | `open to validated` |
| reports that result and contradicts the `statement` | `open to invalidated` |
| is missing, is about something else, or is an opinion and not the result | no row |

Example: ASM-01 "We believe that patients read texts from the clinic within a day", validation "Send
reminder texts for one month and count how many are opened." The fact "8 of 10 reminder texts were
opened within a day (data: reminder pilot export, October 2026)" gives `open to validated`. The fact
"patients say they like the texts (note: Dana, conversation of 2026-11-18)" gives no row: it is not the
count.

Write section 6's last subsection:

```markdown
### Assumption updates

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | 8 of 10 reminder texts were opened within a day (data: reminder pilot export, October 2026) | proposed, not confirmed |
```

- `Evidence`: the fact, ending with one `sources` entry in parentheses (intake.md, *Citing a source*).
  Never a marker: with no fact there is no row.
- Rows ordered by `Earlier assumption`. With no row, the line `None.` replaces the table.
- Save the work file with every row `proposed, not confirmed`.

When the table has a row, add this question last in step 5's form, with `header: "Step 5"`:
"Confirm these assumption updates?", options `Accept all as proposed` and `Leave them proposed`, each
option's `preview` holding the table with each assumption's statement. Changes come typed under Other.

| Answer | Write |
|---|---|
| `Accept all as proposed` | every row's Status `confirmed on <today's date>` |
| `Leave them proposed`, a dismissal, or no question could be asked | every row `proposed, not confirmed` |
| typed text | `confirmed on …` only on the rows the text confirms; remove a row the text rejects; leave the rest proposed |

The date is today's, as `YYYY-MM-DD`. A Status cell names nobody: never add a name to it, and never ask
for one.

**Where a confirmed change lives.** In this BRN's row, and nowhere else: never edit the earlier BRN. A
later PRD run reads the row.

## Extending a brownfield BRN

When this run extends a BRN that has `Project kind: brownfield`:

- Read the documents again by [What to read](#what-to-read) and rebuild *Existing product* from this
  reading. Update each `upstream` record's `version`. Append this run's new `sources` entries (a
  document read for the first time, or at a new version) after the existing ones, in the reading order
  among themselves. Never reorder or remove an existing entry.
- Keep the rows of *Already covered*, *Previously decided* and *Assumption updates*; add new rows by the
  rules above.
- The BRN's own active assumptions with `state: open` are candidates for an update too. Their row names
  this BRN (`BRN-002#ASM-01`). On confirmation, set that assumption's `state` to `validated` or
  `invalidated` in the same edit; while the row is `proposed, not confirmed`, the `state` stays `open`.
  An assumption set this way is no longer ranked: [mvp-path.md](mvp-path.md), *Confirm the cut*, says how
  the ranking and the cut are made again.

**When the extension turns the kind to brownfield** (intake.md: the BRN's line said `greenfield`, or was
the NEEDS CLARIFICATION line of a BRN without the four headings): read the documents, add
`### Existing product` in section 1 after the context prose and `### Already covered`,
`### Previously decided` and `### Assumption updates` in section 6 after the first release cut, each filled
by the rules above or holding its replacement line, add the `upstream` records and append the `sources`
entries. Remove nothing that the BRN already holds, except section 7's bullet that says which kind an
undecided run worked as: it goes once the kind line is decided (intake.md).

## When nothing can be asked

After the waiver's *Proceed without questions*, or when no question tool exists and the request says
to proceed without questions: read the documents as above; take up no parked idea (each is listed in
*Previously decided*); leave every assumption update `proposed, not confirmed`; still report each
candidate kept out with its ID, in the final reply.

A continued run (SKILL.md, *Continuing an earlier run*) reads the documents again, keeps the work file's
rows, and offers the parked ideas again only when the work file has no `### Previously decided` heading.
