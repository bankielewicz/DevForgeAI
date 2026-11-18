# Intake and evidence

How step 1 decides whether the product exists, which questions it asks, and how every input the user gives
becomes a source, a problem's evidence, a Target users row and a success signal. A BRN that carries a
`Project kind:` line follows every rule here; a BRN without that line is an earlier BRN and none of these shapes
applies to it.

## Contents

- [The words in this file](#the-words-in-this-file)
- [Decide the project kind](#decide-the-project-kind)
- [Ask the kind question](#ask-the-kind-question)
- [Ask the clarifying questions](#ask-the-clarifying-questions)
- [Record sources](#record-sources)
- [Write each problem's evidence](#write-each-problems-evidence)
- [Section 3: Target users](#section-3-target-users)
- [Section 8: Candidate success signals](#section-8-candidate-success-signals)
- [Extending a BRN](#extending-a-brn)
- [Before step 7](#before-step-7)

## The words in this file

- **The request** is the arguments plus every message the user has written in this conversation so far.
- **Can ask** means the session has AskUserQuestion, or a user is there to answer in plain text, and the request
  did not say to proceed without questions (or the user answered *Ask me as usual* to the waiver question).
  **Can't ask** is every other case, the waiver answered *Proceed without questions* included.
- **Today** is today's date as `YYYY-MM-DD`.

## Decide the project kind

Decide it once, in step 1, after the topic and after the extend-or-new answer. Take the first rule that decides.

**K0. Extending.** When the run extends an existing BRN and that BRN has a first line of section 1 reading
`Project kind: greenfield` or `Project kind: brownfield`, that kind stands. Stop. When that BRN has no
`Project kind:` line, decide no kind and write none of this file's shapes ([Extending a
BRN](#extending-a-brn)). When its line holds the `[NEEDS CLARIFICATION: greenfield or brownfield]` marker, go on
to K1.

**K1. The user's words.** Search the request, case-insensitively and on whole words, for these phrases.

Greenfield phrases: `greenfield`, `from scratch`, `brand new`, `new product`, `new app`, `new service`,
`new system`, `nothing built yet`, `not built yet`, `haven't built`, `have not built`, `no product yet`,
`idea stage`, `starting a new`.

Brownfield phrases: `brownfield`, `existing` followed by a space and one of `product`, `app`, `application`,
`system`, `service`, `platform`, `site`, `website`, `codebase`, `software`, `tool`, `feature`; `already live`,
`already built`, `already launched`, `already released`, `already in production`, `already in use`,
`in production`, `we launched`, `we shipped`, `we released`, `our live`, `improve our`, `improving our`,
`improvements to our`, `extend our`, `add to our`, `next release of`.

When phrases of exactly one list occur, that is the kind. Stop. When phrases of both lists occur, or of neither,
go on to K2. The folder never overrides the words.

- "Brainstorm improvements to our existing booking app" → `existing app` and `improvements to our`: brownfield.
- "We are building a brand new booking app" → `brand new` and `new app`: greenfield.
- "A brand new booking app, separate from our existing website" → `brand new` (greenfield) and `existing website`
  (brownfield): both, so K2.
- "Our existing customers keep asking for this" → `existing customers` is in neither list: neither, so K2.

**K2. The folder.** Glob `docs/specs/prd/PRD-*.md`, a path, never a listing of the project root. `has_prd` is true
when at least one file matches. Use it only in K3 and K4.

**K3. Ask.** When you can ask, ask the kind question ([Ask the kind question](#ask-the-kind-question)). The answer
is the kind. When the answer is typed under *Other*, apply K1 to the typed text; when K1 doesn't decide, go on to
K4. A dismissal goes on to K4.

**K4. Unresolved.** Write the first line of section 1 as
`Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`. The **assumed kind** is brownfield when `has_prd`
is true and greenfield when it is false. The assumed kind decides the clarifying question set, whether
[brownfield.md](brownfield.md) is followed (when that file exists), and the framework rule that names brownfield; it is never written
into the document as the kind. Add `- [NEEDS CLARIFICATION: greenfield or brownfield]` to section 7's bullets.

Where the kind is decided by K0 to K3, the first line of section 1 is `Project kind: greenfield` or
`Project kind: brownfield`, then a blank line, then the context prose.

| Request | Folder | Can ask | Written | Assumed |
|---|---|---|---|---|
| "…our existing booking app…" | any | any | `Project kind: brownfield` | none |
| "Ways to cut no-shows at our clinic" | holds PRD-001 | yes, answered "Yes, it exists" | `Project kind: brownfield` | none |
| the same | holds PRD-001 | no | the NEEDS CLARIFICATION line | brownfield |
| the same | no PRD | no | the NEEDS CLARIFICATION line | greenfield |
| "A brand new booking app" | holds PRD-001 | any | `Project kind: greenfield` | none |

## Ask the kind question

Ask it alone, in its own form, with step 1 marked in progress. Tag it `metadata: {"source": "devforgeai_step:1"}`
with `header: "Step 1"`. It takes none of the four slots of the clarifying form.

- Question: `Does the product this brainstorm is about already exist?`
- Option 1, label `Yes, it exists`, description `It is built or in use, or the project holds a PRD for it. I will
  read the project's documents first.`
- Option 2, label `No, it is new`, description `Nothing is built yet. I will start from the problem.`

Add ` (Recommended)` to the label of option 1 when `has_prd` is true, otherwise to the label of option 2.

Without AskUserQuestion, ask in plain text, in one message holding only this question and its two answers, and end
your turn.

## Ask the clarifying questions

Ask at most four questions, in one form, tagged `metadata: {"source": "devforgeai_step:1"}` with
`header: "Step 1"` on each. Use the set for the decided or assumed kind. Ask the questions in the order listed,
leaving out the ones you skip. Each question has the options listed, and the user types details under *Other*.
Without AskUserQuestion, ask the same questions in plain text, numbered, in one message, and end your turn.
When you can't ask, ask none.

**Skip a question** only when you can quote a clause of the request that answers it. A question is answered by a
clause that states the thing the question asks, with enough detail to write the cell or sentence it feeds.
Record the clause's content in the place the answer would go.

- "About one in eight booked appointments ends in a no-show, and it's costing us real money." answers question 1
  (a number shows the gap). It does not answer questions 3 or 4.
- "I run a small dental clinic with two dentists." answers none of them: it says who runs the clinic, not who is
  affected or what hurts.

**Greenfield set** (kind greenfield, or assumed greenfield):

1. `What triggered this brainstorm?` Options: `A problem someone reported` (a complaint, incident or request from
   people who would use it); `Numbers that look wrong` (a metric or report that shows a gap); `An opportunity`
   (something new we could do, with no problem yet); `A decision is due` (a deadline or a choice that needs ideas
   first).
2. `Who is affected, and how do they cope today?` Options: `Customers or end users`; `Our own staff`; `Both`;
   `Not sure yet` (I will leave it open and mark it).
3. `What constraints apply?` Options: `A deadline`; `A budget or team size`; `A platform or tool we must use`;
   `None that I know of`.
4. `What evidence do you already have?` Options: `Documents` (a file or report I can read or you can name);
   `Numbers` (counts, rates or costs you can quote); `Tickets or interviews`; `None yet` (I will mark each
   problem's evidence as unknown).

**Brownfield set** (kind brownfield, or assumed brownfield):

1. `What triggered this brainstorm about the existing product?` Options: `A defect or complaint`; `A request for
   more` (people ask for something it does not do); `A metric moved` (usage, cost or quality changed);
   `A business goal` (a target the product must now help meet).
2. `Which users of the product are affected, and how do they cope today?` Options: `Customers or end users`;
   `Our own staff`; `Both`; `Not sure yet`.
3. `What must stay as it is?` Options: `Data and integrations`; `Users' workflows`; `Price or contract terms`;
   `Nothing in particular`.
4. `What shows how the product is used today?` Options: `Usage reports`; `Tickets or complaints`;
   `Interviews or notes`; `Nothing yet`.

**Where each answer goes.**

| Answer to | Written in |
|---|---|
| 1 | One sentence of section 1's prose that starts `Trigger:` |
| 2 | Each problem's `who`; and the Job to be done, Current workaround and Pain cells of section 3 |
| 3 | One sentence of section 1's prose that starts `Constraints:` (greenfield) or `Must stay as it is:` (brownfield) |
| 4 | `sources` entries ([Record sources](#record-sources)); a choice of `None yet` or `Nothing yet` adds none |

An option chosen with no detail typed gives only the option's meaning. Where a cell or an evidence value needs a
detail the user did not give, write `[NEEDS CLARIFICATION: <what is missing>]`; never guess.

## Record sources

An **input** is anything the user states or supplies that the BRN's text relies on: a number, a date, a quotation,
a file, a link, a ticket, an interview. Your own knowledge, ideas you generated and proposals you made are not
inputs. Never add a source for something the user did not give you or you did not read in this run, and never
fetch a URL: record one only when the user gave it.

Add one entry to frontmatter `sources` for each input. Write it as a double-quoted string,
`"<kind>: <reference>"`, with the kind and its reference in these forms.

| Kind | When | Reference | Example entry |
|---|---|---|---|
| `document` | A file of the project that you read and the BRN relies on | The path from the project root, a space and `v` and the file's `version` when its frontmatter has one | `"document: docs/specs/prd/PRD-001.md v3"` |
| `data` | The user names a report, export or dataset | Its name as the user gave it and its period | `"data: ClinicCore attendance report, October 2026"` |
| `ticket` | The user names a ticket or a set of them | The ID or title as given | `"ticket: SUP-114"` |
| `interview` | The user reports what a person said | Who and when, as given | `"interview: front-desk lead, 2026-11-12"` |
| `url` | The user gives a link as evidence | The URL as given | `"url: https://example.com/report"` |
| `note` | The user states a fact in the request or in an answer, with no file behind it | `the user's request, ` or `the user's answers to the intake questions, ` and today | `"note: the user's request, 2026-11-18"` |

Rules for every entry:

- One entry per input and no repeats; the same note text is one entry however many facts it carries.
- Write no double quote inside an entry; use single quotes. The only backslash sequences allowed are `\"` and `\\`.
- A number the user stated is carried in the evidence text, never in the entry: the entry points at where it came
  from.
- With no input at all, `sources` is `[]`.

## Write each problem's evidence

Each active problem's `evidence` is one of three forms, and nothing else:

1. A short claim and one `sources` entry in parentheses, with the entry copied character for character:
   `"12% of October 2026 visits were missed (data: ClinicCore attendance report, October 2026)"`.
2. One `sources` entry alone: `"note: the user's request, 2026-11-18"`.
3. A marker: `"[NEEDS CLARIFICATION: how often it happens]"`.

Wrong: `"12% of visits were missed (attendance report)"` (the parentheses don't hold a `sources` entry) and
`"Staff say it happens a lot"` (no entry, no marker). Use form 3 for every problem the user described without a
fact, a file or a number.

## Section 3: Target users

Gather in step 1 (answer 2) and step 3 (after the problems are framed, every `who` is known). Write at step 6. The
section holds only this table and no prose:

```markdown
| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets, then pays a missed-visit fee |
```

- **Rows.** One row per distinct `who` value among the problems whose `status` is `active`, in the order the
  values first appear in section 2. The Persona cell is the value character for character. A problem with a
  different spelling of the same persona is a different row: use one spelling for one persona in section 2.
- **Job to be done.** A phrase of at most 15 words that starts with a verb, from the user's words in the request
  or answers, else from the goal in the persona's problem statements. When neither states it, write
  `[NEEDS CLARIFICATION: job of <persona>]`. With the `problem-reframing` framework, write the cell in that
  framework's own form, `When [situation], I want to [motivation], so I can [outcome].`, with no word limit.
- **Current workaround.** At most 15 words, from the user's answer. When the user said there is none, write
  `Nothing; the user said so`. When the user didn't say, write `[NEEDS CLARIFICATION: current workaround of
  <persona>]`.
- **Pain.** At most 15 words, from the user's words. Without them, restate the `statement` of the persona's
  active problem with the highest `severity` (high before medium before low; ties go to the lower ID). Never
  empty.
- A cell never holds `|`: write `/` instead. A cell is never empty.
- With no active problem, the table keeps its header and separator and has no row.

## Section 8: Candidate success signals

Gather in step 3 (every number the user gives about a problem is a possible baseline) and in step 5 (the ideas
proposed for promotion). Write at step 6. One bullet per first-release idea, in ID order, in this shape:

```markdown
- IDEA-01: fewer missed visits among patients who got a reminder; baseline 12% of October 2026 visits missed (data: ClinicCore attendance report, October 2026)
```

that is `- <idea ID>: <observable outcome>; baseline <value>`.

- **The first-release ideas** are the ideas whose row in section 6's `### First release cut` table says `yes`.
  While the BRN has no such table, they are the ideas that are promoted or proposed for promotion.
- **Observable outcome.** What a person could count or time that changes if the idea works. It starts with one of
  `fewer`, `more`, `less`, `faster`, `shorter`, `longer`, `higher`, `lower`, `share of`, `number of`, `time to`
  or `rate of`, and contains no `;`. It states no target number: the PRD's interview asks for targets.
- **Baseline.** The current value, copied from the evidence of the problem the idea addresses, with its `sources`
  entry in parentheses, or `[NEEDS CLARIFICATION: <the current value of the measure>]`. Words such as `unknown`
  or `none` are not baselines.
- With no first-release idea, the section holds the single line `- None.`

Wrong: `- IDEA-01: improve the experience; baseline unknown` (not observable, not a baseline), and
`- IDEA-01: missed visits fall below 5%; baseline 12%` (a target; the baseline has no source).

## Extending a BRN

When the user chose to extend an existing BRN:

- A BRN that has the `Project kind:` line is extended with the shapes it has. Keep its kind line. Keep every
  existing source and add the new ones. Check each new or changed problem's evidence, Target users row and
  success-signal bullet against the rules above.
- A BRN that has no `Project kind:` line stays as it is: add no kind line, no table, no source in the new form and
  no section 3 or section 8 shape. Extend it as SKILL.md step 6 says, and tell the user in one sentence that the
  BRN kept its earlier shape and that a new BRN would use the new shapes. Its sources, such as
  `"Front-desk call log, August 2026"`, stay as written.

## Before step 7

Read the written file and check that its first line of section 1 is a `Project kind:` line, unless the run
extended a BRN that had none. The validator applies every rule above only to a BRN that has that line, so a BRN
that lost the line passes the validator without them.
