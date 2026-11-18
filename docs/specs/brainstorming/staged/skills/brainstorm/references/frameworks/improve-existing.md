# Improve existing

## When to use / When not to use

**Use when** the product the topic is about already exists (it is built, in use, or the project holds
a PRD for it) and the topic is improving, extending or fixing it. It starts from evidence about how
the product works today and applies SCAMPER's seven prompts to it.

**Avoid when** the product does not exist yet: use `diverge-converge`. Avoid it too when the user has
a list of improvements to rank: use `shortlist-ranking`.

## Steps

1. **Start from the evidence.** List what is known about how the existing product works today and
   where it hurts, with the source of each fact. A source is a document, data, a ticket, an
   interview, a URL or the user's own note. Add each source used to the BRN's `sources`, as one
   quoted string in the form `"<kind>: <reference>"`, where the kind is `document`, `data`, `ticket`,
   `interview`, `url` or `note`; the user's own description is a `note`. When
   `${CLAUDE_SKILL_DIR}/references/brownfield.md` exists, follow it for reading the project's own
   documents and earlier BRNs. When there is no evidence at all, say so in section 5, and write
   `[NEEDS CLARIFICATION: ...]` as every problem's `evidence`.
2. **Frame the problems.** State each from the user's side, with the evidence that shows it. Set
   `severity` to `high` when the evidence shows it stops people doing what they came to do, costs
   money or harms someone; `low` when it is called an annoyance; otherwise `medium`, and say in
   section 5 that the severity was not given.
3. **Apply the seven prompts, in this order.** Apply each prompt to the existing product, in the
   order of the problems' severity, highest first, trying at most the three most severe problems.
   Name the part of the product the idea changes in the idea itself. Attempt every prompt:
   - **Substitute:** "What in the product, the flow or the rules could be replaced by something
     simpler or better?"
   - **Combine:** "What steps, features or screens could be merged, or joined with something users
     already use?"
   - **Adapt:** "What works well in another product or field that we could adapt here?"
   - **Modify:** "What could be made bigger, smaller, faster, slower or different in form?"
   - **Put to another use:** "Who else, or what else, could the product serve as it stands?"
   - **Eliminate:** "What could be removed, skipped or automated away without loss?"
   - **Reverse:** "What if the order were reversed, or the user and the product swapped roles?"
4. **Record each prompt.** A prompt that gives an idea lists it. A prompt that gives none is
   recorded as none, with one sentence saying why, and counts as attempted. Never write an idea only
   to fill a prompt. An idea that the project's existing documents already cover is not an idea
   here; it is recorded as none, with the document that covers it. When all seven prompts give none,
   write one idea: the smallest change to the existing product that addresses the most severe
   problem.
5. **Surface assumptions.** For each idea, name what must be true for it to work on the existing
   product, and how to check it.
6. **Evaluate.** Rate each idea's value, effort and risk, then compute the score (see the mapping).
7. **Converge.** Propose dispositions by the rule in the mapping. Ask the user to confirm.

## Questions to ask

- Evidence: "How does the product work today, and what do people do when it doesn't?"
- Evidence: "What do you have that shows it: numbers, tickets, interviews, a document?"
- Framing: "Who is hurt most, and what do they do instead?"
- Prompts: "Is there a part of the product you consider off limits to change?"
- Assumptions: "What has to be true for this to work on top of what exists? How could we check?"
- Converge: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Start from the evidence | `sources`; section 1, in prose |
| Frame the problems | `problems`: `statement`, `who`, `evidence`, `severity` |
| Apply the prompts, record each | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null`; section 5: the SCAMPER block below |
| Surface assumptions | `assumptions`: `statement`, `validation`, `state: open` |
| Evaluate | `ideas`: `value`, `effort`, `risk`, `score` |
| Converge | `ideas`: `disposition`, `reason`, only for user-confirmed values |

**Evidence.** Each problem's `evidence` is the text of one `sources` entry, such as
`"data: checkout analytics, March"`, or `"[NEEDS CLARIFICATION: ...]"`.

**SCAMPER block.** In section 5, after the method text, exactly this table: seven rows in this
order, the first column as written, the second the idea IDs separated by commas or `none`, the third
one sentence that is never empty.

```markdown
### SCAMPER prompts

| Prompt | Ideas | Note |
|---|---|---|
| Substitute | IDEA-01 | The date picker becomes a list of free times |
| Combine | none | No two steps of the flow can be merged |
| Adapt | none | Covered by PRD-001, FR-004 |
| Modify | none | Nothing to resize |
| Put to another use | none | No other audience in the evidence |
| Eliminate | IDEA-02 | Removes ten of the form's fields |
| Reverse | none | The flow has one order |
```

**Number of ideas.** Between 5 and 15, with this exception: when fewer than five prompts give an
idea, write the ideas that exist (at least one), add no others, and say in section 5, in a
sentence that begins "The existing product left fewer than five improvements", how many ideas
there are and how many prompts gave none.

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`. `value` is the benefit to the people in the problems it addresses. `effort` is the cost to
build and run it on top of the existing product, migration of existing users and data included.
`risk` is the chance it fails or causes harm, including breaking what users rely on today.

**Score.** Count high = 3, medium = 2, low = 1, and compute
`score = 2 × value − effort − risk`, an integer from −4 to 4. Write it unquoted. For example,
value high, effort low, risk medium gives 2 × 3 − 1 − 2 = 3. Leave all four fields `null` for an
idea you could not rate, and say why in section 5. These are the same ratings and the same formula
as the default framework, so scores compare across brainstorms.

**Proposals.** Propose `promoted` for the up to three ideas with the highest scores, each only when
its score is 3 or more. Propose `parked` for every other idea with a score of 1 or more, and
`rejected` for every idea with a score of 0 or less. Break ties by the lower effort (low before
medium before high), then by the lower idea number. An idea left unrated is proposed `parked`, with
"Not rated" and the reason. These are proposals: write a disposition only for a value the user
confirmed.

## Evaluation method text

Write this into section 5, followed by the SCAMPER block and any discussion the numbers do not
capture:

> Improve existing: the product already exists, so the problems were taken from evidence about how
> it works today, and ideas came from SCAMPER's seven prompts (substitute, combine, adapt, modify,
> put to another use, eliminate, reverse) applied to it. Each idea was rated high, medium or low for
> value, effort and risk, with effort and risk counted on top of what exists. The score is
> 2 × value − effort − risk, counting high = 3, medium = 2 and low = 1 (range −4 to 4); a higher
> score is a stronger candidate for promotion.

## Example

Input: "Brainstorm improvements to our clinic's booking site. In March, 40% of the people who started
the booking form never finished it. The form asks for 14 fields, and a patient can't reschedule
without phoning."

Output (excerpt). Frontmatter:

```yaml
sources:
  - "note: the user's request, 2026-11-18"
  - "data: booking form analytics, March"
```

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Patients give up on the booking form before they finish it."
    who: "Patient booking online"
    evidence: "data: booking form analytics, March"
    severity: high
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Cut the booking form from 14 fields to the four the clinic needs to hold a slot."
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: open
    reason: null
```

Section 5, after the method text:

```markdown
### SCAMPER prompts

| Prompt | Ideas | Note |
|---|---|---|
| Substitute | none | Nothing in the flow is worth replacing: the evidence points at the form |
| Combine | none | The form is a single screen already |
| Adapt | IDEA-02 | A change link on the confirmation page, adapted from other booking sites |
| Modify | IDEA-03 | The half-filled form is kept for seven days |
| Put to another use | none | No other audience in the evidence |
| Eliminate | IDEA-01 | Removes ten of the form's fields |
| Reverse | none | The flow has one sensible order |

The existing product left fewer than five improvements: three ideas, and four prompts gave none.
```

Section 6, before the user confirms:

> Proposed, awaiting confirmation: promote IDEA-01 (score 4, cheap to try); park IDEA-02 and IDEA-03
> (score 1 each).
