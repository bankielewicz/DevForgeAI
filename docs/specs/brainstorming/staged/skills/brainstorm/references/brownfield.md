# Brownfield runs

What a brainstorm does when the product already exists: it reads the project's own documents first, keeps
ideas out of the BRN that the product already covers or that an earlier brainstorm decided, and revisits the
assumptions earlier brainstorms left open. Everything here is read-only on the project's documents.

## Contents

- [When this file applies](#when-this-file-applies)
- [Read the project's documents](#read-the-projects-documents)
- [Write the Existing product table](#write-the-existing-product-table)
- [Documents you cannot read](#documents-you-cannot-read)
- [Keep covered and decided ideas out](#keep-covered-and-decided-ideas-out)
- [Offer the parked ideas](#offer-the-parked-ideas)
- [Revisit earlier assumptions](#revisit-earlier-assumptions)
- [Extend or new](#extend-or-new)
- [Section 6 shapes](#section-6-shapes)

## When this file applies

Follow it when the project kind ([intake.md](intake.md)) is brownfield, or unresolved and assumed brownfield. When
the run extends a BRN that has no `Project kind:` line, don't follow it. In a greenfield BRN, write none of its
shapes.

## Read the project's documents

Read them in step 1, after the kind is decided and before the clarifying questions. Reach each folder by its path;
never list the project root. Use Read, and Glob and Grep when available. Never write to, edit or repair any of
these documents.

| Kind | Path | Skip when `status` is | Read at most |
|---|---|---|---|
| PRD | `docs/specs/prd/PRD-NNN.md` | `superseded`, `deprecated` | 4 |
| Earlier BRN | `docs/specs/brainstorm/BRN-NNN.md` | `archived` | 4 |
| ARCH | `docs/specs/arch/ARCH-NNN.md` | `superseded`, `deprecated` | 1 |
| Epic | `docs/specs/epic/EPIC-NNN.md` | `superseded`, `deprecated` | 4 |
| ADR | `docs/specs/adr/ADR-NNN.md` | `rejected`, `superseded`, `deprecated` | 3 |

**Order.** Read the documents in the table's order: PRDs, BRNs, ARCH, epics, ADRs. Within a kind:

1. First the documents the request names by ID (`PRD-001`, `BRN-002` and so on). A named document that doesn't
   exist counts as unreadable ([Documents you cannot read](#documents-you-cannot-read)).
2. Then the others, the highest number first.

A named document counts toward its kind's limit. To choose which documents to read, read the first 40 lines of a
candidate for its `status`, and skip it when its status is in the third column. Stop at the limit. When the run
extends a BRN, that BRN is not an earlier BRN: leave it out of the table.

**Say what you left out.** End section 1's prose with one sentence, `Not read:`, listing each skipped document and
the reason in parentheses, `(retired)` for a skipped status or `(over the limit)`. Leave the sentence out when
nothing was skipped.

**Extract** from each document you read, keeping only items whose `status` is `active`:

| Kind | Keep |
|---|---|
| PRD | `title`, `version`; every functional and non-functional requirement's `id` and `statement`; the success metrics' `id` and `metric`; the non-goals of section 4 |
| Earlier BRN | `title`, `version`; every idea's `id`, `idea`, `disposition` and `reason`; every assumption's `id`, `statement`, `validation` and `state` |
| ARCH | `title`, `version`, `outcome` |
| Epic | `title`, `version`; the PRD items its `upstream` links with relation `refines` |
| ADR | `title`, `version`, `status` |

## Write the Existing product table

In section 1, after the context prose and before section 2, write `### Existing product` and this table
(the template's brownfield region):

```markdown
| Document | Version | What it already covers |
|---|---|---|
| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |
```

One row per document read, in the order the table above gives, the highest number first within a kind. `Version` is
the document's `version`. The last cell by kind:

| Kind | Last cell |
|---|---|
| PRD | `<title> (<functional ranges>; <non-functional ranges>)`; leave out a part with no active requirement; `<title> (no active requirement)` when both are empty |
| Earlier BRN | `Earlier brainstorm: <title> (<idea ranges>; <assumption ranges>)` |
| ARCH | `<title> (architecture; outcome <outcome>)`, or `outcome not set` when `outcome` is `null` |
| Epic | `<title> (covers <ranges of the PRD items it refines>)`, or `(covers no requirement)` |
| ADR | `<title> (<status>)` |

Write a **range** of consecutive IDs as `FR-001 to FR-003`; a gap starts a new range, and ranges are separated by
`, `. A single ID stands alone. No cell holds `|`.

**Link each document.** In a new BRN, add to frontmatter `upstream` one record per row:
`{id: PRD-001, relation: informed_by, version: 3, hash: null}`, with the row's ID and version. Add to `sources` one
entry per row: `"document: docs/specs/prd/PRD-001.md v3"`, the path being the folder in the table above and the ID.
When the run extends a BRN, add the `sources` entries but no `upstream` record: a document that cites the extended
BRN would make a cycle.

## Documents you cannot read

A document is **unreadable** when Read fails on it, it is not UTF-8 text, or the request named it and it doesn't
exist. It is **malformed** when any of these holds: its first line is not `---` or its frontmatter has no closing
`---`; its `id` differs from its file name; its `type` is not `prd`, `brainstorm`, `arch`, `epic` or `adr` for its
folder; its `version` is not a positive integer; a `yaml items` fence in it is not closed.

Skip such a document completely: no row, no link, no source, nothing extracted, and no repair. Say so in two
places: add `- [NEEDS CLARIFICATION: PRD-002 could not be read: <reason>]` to section 7's bullets (the reason is
`unreadable` or the first failed condition above in the words used here), and mention it in the discussion of the
final reply. A skipped document doesn't count toward its kind's limit.

**No document at all.** When the kind is brownfield and every document is missing or skipped, replace the table with
the line `No document was found in the project.`, add `- [NEEDS CLARIFICATION: where the existing product is
documented]` to section 7's bullets, write `None.` for every table of [Section 6 shapes](#section-6-shapes), and say
in the discussion that no document was found. Go on with the brownfield question set.

## Keep covered and decided ideas out

Apply these tests to every candidate idea in step 3 before you write it as an item: the ideas you generate and the
ones the user gives.

**The test.** A candidate *restates* a requirement when the requirement, built exactly as written, would already
make the candidate's sentence true. Compare four attributes: who is served, what the product does, when it happens,
and the channel or limit. The candidate restates the requirement only when every attribute the candidate states is
stated, equal or more general, in the requirement. An attribute the candidate states and the requirement doesn't is
an addition, and then the candidate is not a restatement. When in doubt, it is not.

- Candidate "Text reminders before a visit" against `PRD-001#FR-003`, "send a text reminder the day before each
  appointment": who, what, when and channel are all there. It restates it.
- Candidate "A second reminder two days before, with a link to move the visit" against the same requirement: the
  timing and the link are additions. It does not.
- Candidate "Email reminders" against the same requirement: the channel differs. It does not.

Take the checks in this order and stop at the first that applies.

1. **Already covered.** The candidate restates an active functional or non-functional requirement of a PRD you
   read. Don't add it to `ideas`. Add a row to `### Already covered`: the candidate in at most 12 words (the
   user's own words when the user raised it) and the requirement as `PRD-001#FR-003`; several requirements are
   separated by `, `. Tell the user in the reply, and say they can type "add it anyway" under step 5's question
   1 to add it as an idea; if they do, add it as the next idea and remove its row.
2. **Rejected earlier.** The candidate restates an idea of an earlier BRN you read whose `disposition` is
   `rejected`. When the user raised the candidate in this run, add it as an idea in the user's own words and write
   no row; add to section 6's convergence prose the sentence `The user raised it again: BRN-001#IDEA-06 rejected
   it.` (the idea's own reference). Otherwise don't add it; add a row to `### Previously decided` with the idea in
   at most 12 words, `rejected` and the reference `BRN-001#IDEA-06`.
3. **Parked earlier.** The candidate restates an idea whose `disposition` is `parked`. Handle it as the next
   section says.

## Offer the parked ideas

After the problems are framed and before you generate ideas, collect the parked ideas: the earlier BRNs' active
ideas with `disposition: parked` that don't restate an active requirement (the first test above). Order them by BRN
number, highest first, then idea number, lowest first.

When you can ask, and there is at least one, ask one question in one form tagged `devforgeai_step:3` with
`header: "Step 3"`: `Take up any of these parked ideas again?`, with multiple selection. Make one option per idea
for the first three: the label is the reference (`BRN-001#IDEA-03`), the description is the idea followed by
` Parked: ` and its reason. The fourth option is `None of these`. List the ideas beyond the first three in the
reply, under `Not offered:`.

- **Taken up.** Add each selected idea as a new idea of this BRN with the next free number: its text is the earlier
  idea's text (reworded only to fit the new problems), it addresses the problems it fits like any idea, its
  `disposition` is `open`, and an item `upstream` record ties it to the earlier idea:
  `upstream:` with `- {id: BRN-001, item: IDEA-03, relation: informed_by, version: 1, hash: null}`, the version
  being the earlier BRN's. Write no row for it. Taking an idea up doesn't promote it.
- **Not taken up** (not selected, offered and not selected, or not asked). Add a row to `### Previously decided`
  with the idea, `parked` and its reference, for each offered idea and for each parked idea that a candidate
  restated. A parked idea that was neither offered nor restated gets no row.

An answer with no selection decides nothing: take up none, and say so in the reply. When you can't ask, take up none
and write the rows for the ideas a candidate restated.

Rows of `### Previously decided` go in the order of the `Where` cell: BRN number, then idea number.

## Revisit earlier assumptions

Do this in step 3, after the problems are framed and before step 4, in a new BRN. (When the run extends a BRN, see
[Extend or new](#extend-or-new).)

**Which assumptions.** The active assumptions of the earlier BRNs you read whose **effective state** is `open`. The
effective state of an earlier assumption is the `Change` of the last confirmed row for it in the
`### Assumption updates` tables of the BRNs you read (the BRN with the highest number first); it is `validated` or
`invalidated` when such a row exists, and otherwise the assumption's own `state`.

**When to propose.** Propose a new state only when a fact the user gave in this run, or a document you read, states
that the assumption holds (`validated`) or doesn't (`invalidated`). Compare the fact with the assumption's
`statement` and `validation`; when the fact is partial or doesn't settle it, propose nothing. Never propose from your
own belief. Quote the fact in the proposal, with its `sources` entry in parentheses, and add the entry to `sources`
if it isn't there.

**Record each proposal** as a row of `### Assumption updates`: the earlier assumption as `BRN-001#ASM-01`,
`open to validated` or `open to invalidated`, the fact with its entry, and the status. Rows go in the order of the
`Earlier assumption` cell. The status is `proposed, not confirmed` until the user answers, as step 5 says below.
The earlier BRN is never edited by a new BRN's run.

**Carry a belief forward.** When a new assumption of this BRN states the same belief as an open earlier assumption
(the earlier statement is true exactly when the new one is), add an item `upstream` record to the new assumption:
`- {id: BRN-001, item: ASM-02, relation: informed_by, version: 1, hash: null}`.

**Ask in step 5.** When at least one row exists and you can ask, add this question to step 5's form as its last
question, after the first release cut question when that one is asked (SKILL.md step 5; the form holds at most four
questions): `Confirm these assumption updates?`, options `Accept all as proposed` and `Leave them open`, each
option's preview holding the table of `Earlier assumption`, `Change` and `Evidence`; changes come typed under
*Other*.

- *Accept all as proposed*: write `confirmed by <owner> on <today>` as every row's status; `<owner>` is the
  frontmatter `owner`, or `the user` when `owner` is a `[NEEDS CLARIFICATION: owner]` marker.
- *Leave them open*: leave every row `proposed, not confirmed`.
- Typed changes: write the confirmed status only on the rows the text names, leave the others as they are.
- When you can't ask: every row stays `proposed, not confirmed`, and the final reply says the user can confirm
  them later; when they do, follow the same path as for dispositions (SKILL.md, *Decisions that belong to the
  user*).

## Extend or new

The test for a BRN **on the topic** is the same for every kind. **The topic** is the arguments when they are not
empty; otherwise the user's answer to the topic question (step 1, item 1), when it was asked; otherwise the user's
first message in this conversation. The topic's words are the words of at least four letters in the topic,
lower-cased, split on any character that is not a letter, without these: `about`, `after`,
`also`, `because`, `brainstorm`, `brainstorming`, `could`, `from`, `have`, `idea`, `ideas`, `into`, `more`, `need`,
`should`, `that`, `their`, `them`, `then`, `these`, `they`, `this`, `ways`, `what`, `when`, `where`, `which`, `will`,
`with`, `would`, `your`. An earlier BRN is on the topic when its `title`, treated the same way, shares at least two
of those words with the topic.

- **None on the topic:** ask no extend-or-new question and create a new BRN.
- **At least one on the topic:** show the one that shares the most words (ties: the higher BRN number) and ask
  extend or new, as SKILL.md step 1 does, also when the request said to proceed without questions. When you can't
  ask, because the session has no AskUserQuestion and the request said not to ask, create a new BRN.

Examples. The topic "Offer a loyalty scheme for returning customers" and the earlier title "Online appointment
booking for returning patients" share only `returning`: not on the topic, so a new BRN and no question. The topic
"Cut missed visits among patients who book online" and the same title share `patients` and `online`: on the topic,
so ask. The topic "Reduce appointment no-shows at our dental clinic" and the title "Reducing appointment no-shows
at the dental clinic" share `appointment`, `shows`, `dental` and `clinic`: ask.

**New.** The earlier BRN is read like every other document (a row, a link, a source) and is never edited.

**Extend.** The run extends the earlier BRN, so SKILL.md step 6's rules for extending apply, and:

- The extended BRN is not a row of its own `### Existing product`; every other document read is.
- Replace the `### Existing product` table with this run's. Keep the existing rows of `### Previously decided` and
  `### Already covered`, add the new ones and leave out a row that repeats a kept one. Leave `### Assumption updates`
  as it is.
- Revisit only the extended BRN's own open assumptions. On *Accept all as proposed*, or a typed confirmation, edit
  the assumption's `state` in place and name the change in the new Change Log row; on *Leave them open*, or
  when you can't ask, change no `state` and add to section 6's convergence prose the sentence `Proposed, not
  confirmed: BRN-001#ASM-01 open to validated (<the fact, with its entry>).`
- When the extended BRN has no `Project kind:` line, don't follow this file ([When this file
  applies](#when-this-file-applies)).

## Section 6 shapes

Keep the template's brownfield regions: delete only the two marker lines of each. In section 6 the order is the
convergence prose, `### First release cut` (when the BRN has one), `### Already covered`, `### Previously decided`,
`### Assumption updates`. Replace an empty table with the line `None.`. The tables are:

```markdown
### Already covered

| Suggestion | Covered by |
|---|---|
| Text reminders before a visit | PRD-001#FR-003 |

### Previously decided

| Idea | Decision | Where |
|---|---|---|
| Charge a deposit at booking | rejected | BRN-001#IDEA-06 |

### Assumption updates

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | 62% of October 2026 bookings were made online (data: ClinicCore booking source report, October 2026) | confirmed by Dana on 2026-11-18 |
```

Every document cited in these tables has a row in `### Existing product`, and every `Evidence` cell holds one
`sources` entry exactly as written there.
