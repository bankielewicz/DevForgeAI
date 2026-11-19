# Intake: project kind, questions, sources, sections 3 and 8

Read this at step 1, before deciding the project kind. It applies to a new BRN and to a BRN that already
has the `Project kind:` line. A BRN without that line keeps its earlier shape when extended: decide no
kind, write none of the shapes below into it, and ask the greenfield question set.

## Contents

- [Project kind](#project-kind)
- [The kind question](#the-kind-question)
- [Clarifying questions](#clarifying-questions)
- [Sources](#sources)
- [Citing a source](#citing-a-source)
- [Target users (section 3)](#target-users-section-3)
- [Candidate success signals (section 8)](#candidate-success-signals-section-8)

## Project kind

*Brownfield*: the product the topic is about exists (it is built or in use). *Greenfield*: it does not.
The product is what the ideas would be built into or would change: a software product, a service or a
process. A new feature for a product that exists is brownfield.

Decide after the topic and extend-or-new (Intake 1 and 2). Take the first rule that matches:

1. **Already decided.** The BRN being extended, or the work file of a continued run, has the line
   `Project kind: greenfield` or `Project kind: brownfield`: keep that kind. Ask nothing. One exception,
   when extending: a `greenfield` line becomes `brownfield` when the user's words in this run say the
   product exists.
2. **The user's words say the product exists**: brownfield.
3. **The user's words say it does not exist**: greenfield.
4. **You can ask, and this is not a continued run**: ask [the kind question](#the-kind-question).
   *It exists* is brownfield; *It doesn't exist yet* is greenfield; to typed text apply rules 2 and 3; a
   dismissal, or typed text that matches neither or both, goes to rule 5. A continued run never asks
   it again: its work file already holds the line.
5. **Otherwise the kind is not decided.** Write the line
   `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]` and work with a kind for the rest of
   the run: brownfield when `docs/specs/prd/PRD-*.md` matches at least one file, else greenfield. The
   kind you work with chooses the question set, the framework rule that reads the kind (step 2), the
   template's brownfield-only parts and whether [brownfield.md](brownfield.md) applies. It is never
   written as the project kind.

When both rule 2 and rule 3 match, neither does: go to rule 4.

**Record an undecided kind in three places**, so nobody reads the kind you worked as for a decision:

1. The kind line: `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`.
2. Section 7, as the first of its bullets, exactly
   `- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]`, or the same with
   `worked as brownfield`. Write it into the work file from its first save.
3. The final reply's discussion, one sentence: "The project kind is not decided: I worked as brownfield
   because this project has a PRD. Tell me whether the product exists and I will update BRN-NNN." (or
   "as greenfield because this project has no PRD").

Write the bullet only while the kind line is the NEEDS CLARIFICATION line. When the kind is decided later, in
this run, after the BRN is written or in an extension, set the kind line and remove the bullet in the same
edit; after the BRN is written, edit it in place, validate it again and report.

**Extending a BRN that has the line.** The line changes only towards brownfield, and nothing is ever
removed from the BRN except section 7's worked-as bullet, which goes once the line is decided:

| The BRN's line | This run | Result |
|---|---|---|
| `greenfield` | the user's words say the product exists | `brownfield`; do the brownfield reading and add the brownfield parts ([brownfield.md](brownfield.md)) |
| `greenfield` | anything else | stays `greenfield`; ask nothing |
| the NEEDS CLARIFICATION line | rules 2 to 5 decide | `greenfield` or `brownfield`; when the BRN already holds the four brownfield headings, only `brownfield` |
| `brownfield` | anything | stays `brownfield` |

When the user's words say the product does not exist and the line can't follow them (a `brownfield` line,
or the NEEDS CLARIFICATION line with the four brownfield headings), say "BRN-NNN records this product as
brownfield. To brainstorm it as a new product, create a new BRN.", keep the line, and go on with the
extension unless the user asks for a new BRN.

An explicit statement the user makes later, before the BRN is written, replaces the kind. On a change to
brownfield, do the brownfield reading before the next step's work.

**The user's words** are the arguments, the user's messages in this conversation, and the answer to the
topic question. Nothing else decides: not a file in the project, not what you know about the product.

**The test for rules 2 and 3.** Only an explicit statement counts, never an inference.
- *Exists*: the words name the product and say it is built, released, live, in production or in use; or
  that it has users, customers, data, issues or a version today; or they ask to improve, extend, fix,
  speed up, migrate or replace it as something they have now.
- *Does not exist*: the words say it is new, not built yet, to be built from scratch, an idea or a concept,
  or that nothing exists yet.
- A request that names only a goal or a symptom, and no product, says neither.

| The user's words | Kind | Why |
|---|---|---|
| "Brainstorm improvements to our patient booking site, which went live in March." | brownfield | "went live" |
| "Our open-source CLI tool has 400 open GitHub issues. Brainstorm how to get triage under control." | brownfield | the tool has issues today |
| "Brainstorm ideas for making our internal expense-report approvals faster; right now an approval takes about nine working days." | brownfield | the process is named and in use now |
| "We want to build a new booking app for our clinic; nothing exists yet." | greenfield | "nothing exists yet" |
| "Brainstorm ideas for a feature that helps remote teams run better stand-ups in Slack." | not decided | it does not say whether the product the feature belongs to exists |
| "I run a small dental clinic. Brainstorm ways we could cut down on no-shows." | not decided | a goal, no product named |
| "We have a prototype nobody uses yet; brainstorm what the real product should be." | not decided | built, and not in use: both rules match |

**You can ask** unless the request says to proceed without questions and the waiver was answered
*Proceed without questions* or couldn't be asked (SKILL.md, Intake). After *Proceed without questions*
the kind question is never asked: rule 5 applies.

## The kind question

Ask it alone in its own form, tagged step 1 (`metadata: {"source": "devforgeai_step:1"}`,
`header: "Step 1"`), before the clarifying questions:

- Question: "Does the product this brainstorm is about already exist?"
- Option 1: `It exists`, description "Brownfield: it is built or in use. I read the project's documents
  and earlier brainstorms before we start."
- Option 2: `It doesn't exist yet`, description "Greenfield: nothing is built or in use."

When `docs/specs/prd/PRD-*.md` matches at least one file, option 1's label is `It exists (Recommended)`
and its description ends with " This project has a PRD." A PRD never decides the kind: it only makes
brownfield the recommended answer.

Without AskUserQuestion, ask the question in plain text with the two answers, alone, and end your turn.

## Clarifying questions

Ask at most four, in one form tagged step 1, each with `header: "Step 1"` and `multiSelect: true`: the
set for the kind (decided, or worked with), in this order and wording. The user types detail under Other.

**Greenfield set**

| # | Question | Options |
|---|---|---|
| 1 | "What triggered this brainstorm?" | `A problem we keep hitting`, `A request from users or customers`, `A new opportunity`, `A deadline or outside change` |
| 2 | "Who is affected, and what do they do today instead?" | `Customers or end users`, `Our own staff`, `Another team or partner` |
| 3 | "What constraints apply?" | `A fixed deadline`, `A fixed budget`, `Technology we must use`, `Rules or regulation` |
| 4 | "What evidence should I use?" | `Numbers or reports`, `Support tickets or complaints`, `Interviews or feedback`, `None yet` |

**Brownfield set**

| # | Question | Options |
|---|---|---|
| 1 | "What triggered this brainstorm about the existing product?" | `A problem users keep hitting`, `A request from users or customers`, `A metric that moved`, `A new opportunity` |
| 2 | "Which users of the product are affected, and what do they do today instead?" | `Existing customers or end users`, `People who tried it and left`, `Our own staff` |
| 3 | "What must stay as it is?" | `Behaviour users rely on`, `Existing data and integrations`, `Commitments already made`, `Nothing is fixed` |
| 4 | "What evidence from the product in use should I use?" | `Usage data or reports`, `Support tickets or complaints`, `Interviews or feedback`, `None yet` |

**Skip a question the user's words already answer.** The test, per question:

| # | Skip when the words | Skipped | Asked |
|---|---|---|---|
| 1 | give a reason for brainstorming now: an event, a number, a complaint, a request or a deadline | "one in eight booked appointments ends in a no-show, and it's costing us real money" | "Brainstorm ideas for a loyalty scheme." |
| 2 | name at least one group of affected people | "helps remote teams run better stand-ups" | "ways we could cut down on no-shows" |
| 3 | state at least one limit: a deadline, a budget, a technology, a rule, or something that must not change | "There are only two of us maintaining it, in our spare time." | "Brainstorm how to get issue triage under control." |
| 4 | name at least one source other than the user's own statement: a document, a dataset or report, a ticket, an interview or a URL | "the front-desk no-show log for August shows one in eight" | "about one in eight appointments is missed" |

When every question is skipped, show no form. Ask no follow-up question in step 1: four is the limit.

**Ask none** when the request says to proceed without questions and the waiver was answered *Proceed
without questions* or couldn't be asked.

**Without AskUserQuestion** (and no such request), ask the same questions as a numbered plain-text list,
without the options, in one message, and end your turn.

**What each answer fills.** Record the user's words, never your expansion of them.

| # | Fills | Unknown after the answer |
|---|---|---|
| 1 | Section 1's context prose | `[NEEDS CLARIFICATION: what triggered this brainstorm]` in the prose |
| 2 | Each problem's `who`, and section 3's cells | The markers [section 3](#target-users-section-3) gives |
| 3 | Section 1's context prose | `[NEEDS CLARIFICATION: constraints]` in the prose |
| 4 | `sources` and each problem's `evidence` | The marker [Citing a source](#citing-a-source) gives |

An option picked with nothing typed is recorded as the option's words, and its missing detail as a
marker: `A fixed deadline` gives "A fixed deadline applies: [NEEDS CLARIFICATION: the deadline's date]".
`None yet` and `Nothing is fixed` record nothing.

## Sources

A source is an input this brainstorm used: something the user gave or named, the user's own statement,
or a project document you read in this run. Write one `sources` entry per source, in the frontmatter, as
a quoted string `"<kind>: <reference>"`. Take the first kind that fits:

| Kind | What it is | Reference | Example entry |
|---|---|---|---|
| `ticket` | An issue or support ticket, given by ID or link | The tracker and ID, or the link, as the user gave it | `"ticket: GitHub issue 412"` |
| `data` | Numbers (counts, rates, measurements) from a dataset, report, log, survey or analytics tool | Its name as the user gave it, then `, ` and the period or date when given | `"data: front-desk no-show log, August 2026"` |
| `interview` | What a named person or group said in words when asked, with no count | Who, by the name or role given, then `, ` and the date or month when given | `"interview: three hygienists, October 2026"` |
| `document` | A file or a named document | A project file: its path from the project root, then ` v` and the `version` of its frontmatter when it has one. Any other document: its title as the user gave it | `"document: docs/specs/prd/PRD-001.md v3"` |
| `url` | A web address not covered above | The address exactly as given | `"url: https://example.com/no-show-study"` |
| `note` | The user's own statement in this conversation, with no other source named | The owner's name, or `user` when the owner is unknown, then `, conversation of ` and today's date | `"note: Dana, conversation of 2026-11-18"` |

A survey's counts are `data`: "in our contributor survey of October 2026, 12 of 20 contributors said they
gave up" gives `"data: contributor survey, October 2026"`. What people said, with no count, is `interview`:
"three hygienists told us in October that the reminder cards get lost" gives
`"interview: three hygienists, October 2026"`.

Rules:

- **Never invent a source.** Write an entry only for an input that is in the conversation or that you
  read. What you know yourself is not a source: a fact from your own knowledge is written as a
  NEEDS CLARIFICATION marker, never with an entry.
- **Never fetch one.** Don't open a URL, search the web or call any tool to obtain a source. Record the
  URL and use only what the user said it shows.
- **Read a project file the user names as a source**, and no other file on your own account. A project
  file is a path in the user's words that, taken from the project root when it is relative, resolves to a
  regular file inside the project folder and outside its `.git` folder. A path that leaves the folder, a
  folder, and a pattern with a wildcard are not: don't read them. Read the file whole with the Read tool,
  once, when it is named. Never edit, move, delete or run it. Write its entry as
  `"document: <path from the project root>"`, with ` v<version>` when its frontmatter has an integer
  `version`, and cite that entry for every fact you take from the file, in the file's terms.

  | The user's words | Do |
  |---|---|
  | "the survey results are in docs/contributor-survey.md" | Read it; `"document: docs/contributor-survey.md"` |
  | "it's all in ../shared/handbook.pdf" | Don't read it; `"document: ../shared/handbook.pdf"`; use only what the user said it shows |
  | "look through the notes folder" | Read nothing; no entry |

- **When a named project file can't be read** (it does not exist, it is not text, or the Read tool fails or
  is refused): write `"document: <its path from the project root>"` with no version, use only what the user
  said about it, try no other file or tool in its place, and say in the reply "I could not read <path>, so
  I used only what you said about it."
- **One `note` entry per run**, however many statements the user makes.
- **Clean the reference**: one line, no leading or trailing space, runs of spaces collapsed, `"`
  replaced by `'`, `|` replaced by `/`, no final period.
- **Order and duplicates**: entries stand in the order the sources were first given or read; write each
  entry once. When extending, keep the existing entries as they are and append.
- Record a source when it is given, at step 1 or later, and save it in the work file's frontmatter.

## Citing a source

A fact written into a problem's `evidence` or a section 8 baseline is either a single marker or a
statement that ends with one `sources` entry, without its quotes, in parentheses after one space. An
Assumption updates evidence cell is always such a statement, never a marker (brownfield.md):

```yaml
evidence: "One in eight booked visits was missed (data: front-desk no-show log, August 2026)"
evidence: "[NEEDS CLARIFICATION: how many callers hang up before booking]"
```

- State the fact in the source's or the user's terms: no number the source did not give.
- Cite exactly one entry. When two sources state the fact, cite the one that stands first in `sources`.
- A problem with no fact from any source gets one marker and nothing else: the missing fact as a noun
  phrase, such as `[NEEDS CLARIFICATION: current no-show rate]`.

## Target users (section 3)

Gather at step 1 (question 2) and step 3 (framing the problems); write at step 6, and in the work file
from its first save. Section 3 holds exactly this table and nothing else:

```markdown
| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets, then pays a missed-visit fee |
```

- One row per distinct `who` value of the active problems, in the order the values first appear. The
  Persona cell equals the `who` value character for character, so give each persona one spelling in every
  problem, and never put `|` in a `who` value.
- Each other cell holds what the user's words or a source say about that persona, in at most 15 words and
  with no `|`. Add no citation in this table.
- A cell nobody stated holds its marker: `[NEEDS CLARIFICATION: job to be done of <persona>]`,
  `[NEEDS CLARIFICATION: current workaround of <persona>]` or `[NEEDS CLARIFICATION: pain of <persona>]`.
  Never fill one from a problem's `statement` or from what such users usually do.

## Candidate success signals (section 8)

Gather at step 5, once the first release cut is proposed; write at step 6, and in the work file at the
step-5 save. One bullet per first-release idea (an idea whose row in section 6's *First release cut* table
says `yes`), in ID order:

```markdown
- IDEA-01: fewer missed visits among patients who got a reminder; baseline [NEEDS CLARIFICATION: current no-show rate]
```

- The form is `- IDEA-NN: <observable outcome>; baseline <value>`.
- **Outcome**: one clause naming what would be seen to change for the persona of a problem the idea
  addresses if the idea works. It states a direction (more, fewer, faster), never a target number, and
  never contains `; baseline `.
- **Baseline**: today's value of that outcome, as [Citing a source](#citing-a-source) says: a fact ending
  with one `sources` entry in parentheses, or the marker `[NEEDS CLARIFICATION: current <what is measured>]`.
- With no first-release idea, or no *First release cut* table in section 6, the section holds the one
  line `- None.`
