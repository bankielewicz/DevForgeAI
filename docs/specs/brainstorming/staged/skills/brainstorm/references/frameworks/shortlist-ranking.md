# Shortlist ranking

## When to use / When not to use

**Use when** the user already has a shortlist or a backlog and wants it ranked or cut: three or more
candidates in the request, or a list in a file with two or more.

**Avoid when** the options are still open (use `diverge-converge`), or the user asks what to build
first to test an idea (use `risk-first-mvp`).

## Steps

1. **Take the candidates.** Each candidate becomes one idea, in the order the list gives them, in
   the user's own words. Generate no idea of your own: the 5-to-15 rule does not apply here, and a
   list of four stays four. A candidate the user adds during the session joins the list. Take at
   most 99; with more, take the first 99 and say so in section 5.
2. **Frame the problems.** For each candidate, name who it is for and what hurts them today. Merge
   duplicates. Every idea addresses at least one problem.
3. **Surface assumptions.** Name what must be true for the candidates to pay off, and how to check
   it.
4. **Rate.** Give each idea its four inputs (see the mapping below), then compute the score.
5. **Rank.** Highest score first. On a tie, the smaller effort first; then the lower ID. An idea
   that could not be rated gets no rank and goes last, in ID order.
6. **Cut.** Go down the ranking adding up effort. With capacity C in person-weeks, an idea whose
   running total is at most 60% of C is a *must*; at most 80%, a *should*; at most 100%, a *could*;
   beyond that, a *won't*. An unrated idea gets no cut.
7. **Propose.** Propose `promoted` for every *must* and *should*, and `parked` for every *could*,
   *won't* and unrated idea. This framework never proposes `rejected`. The proposed reason is
   "Must in the proposed cut: rank 1 of 4, score 160.0." with the idea's own cut word, rank, count
   of ranked ideas and score; for an unrated idea, "Not rated: " and what is missing. These are
   proposals: write a disposition only when the user confirms it at step 5.

The cut proposes dispositions only. Its words are not a requirement priority, even inside a
`reason`: the PRD sets priority. It is also not the first release cut.

## Questions to ask

Ask these at step 3 of the workflow, in one form, and skip any the request already answers. When
nothing can be asked, or after a switch to this framework, ask none and use the fallbacks in the
mapping.

- Reach: "How many people does each candidate affect, and over what period?"
- Effort: "Do you have an effort estimate for any of these, in person-weeks?"
- Capacity: "How many person-weeks can you spend on this list?"
- Evidence: "What tells you these matter: tickets, numbers, interviews?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Take the candidates | `ideas`: `idea`, with `disposition: open` and `reason: null` |
| Frame the problems | `problems`: `statement`, `who`, `evidence`, `severity`; `ideas`: `addresses` |
| Surface assumptions | `assumptions`: `statement`, `validation`, `state: open` |
| Rate | `ideas`: `value`, `effort`, `risk`, `score`; the inputs table in section 5 |
| Rank and cut | the capacity line and the cut table in section 6 |
| Propose | the proposal paragraph in section 6; `disposition` and `reason` only once confirmed |

**The four inputs.** Where each comes from, and what to do when it is unknown:

| Input | Scale | Source, in this order | When unknown |
|---|---|---|---|
| Reach | A whole number of people, or of events, per period. The unit and period are the user's; with none given, people per quarter | The user's figure for that idea; else a figure in one of the BRN's `sources`. Never your own estimate | If reach is unknown for any rated idea, count reach as 1 for every idea, and say so in section 5 |
| Impact | 3 (massive), 2 (high), 1 (medium), 0.5 (low) or 0.25 (minimal): how much one person reached gains | The user's value; else your estimate | An idea too vague to say what a person reached would do differently is not rated |
| Confidence | 100, 80 or 50 | Computed: 100 when both grounds hold, 80 when one does, 50 when neither. Ground 1: reach is known (not counted as 1). Ground 2: the idea addresses a problem whose `evidence` is not a `[NEEDS CLARIFICATION]` marker | Never unknown |
| Effort | Person-weeks, a multiple of 0.5, at least 0.5 | The user's figure (a person-day is 0.2, a person-month is 4), rounded up to the next 0.5; else your estimate, one of 0.5, 1, 2, 4, 8, 16, 32 | Never unknown for a rated idea |

"Too vague" is a judgment. "Make onboarding better" is too vague; "Add a progress bar to onboarding"
is not.

**Fields.** Numbers in `value`, `effort` and `risk` are written in double quotes, with no thousands
separator and no trailing zeros. `score` is an unquoted number.

- `value` = reach × impact. Reach 400 and impact 2 give `"800"`; reach 150 and impact 0.25 give
  `"37.5"`.
- `effort` = the person-weeks: `"4"`, `"0.5"`.
- `risk` = 100 − confidence: `"0"`, `"20"` or `"50"`.
- `score` = `value` × (100 − `risk`) ÷ 100 ÷ `effort`, computed from the three written values,
  rounded to one decimal with a 5 rounding up, and always written with one decimal. `"800"`, `"20"`
  and `"4"` give 800 × 80 ÷ 100 ÷ 4 = `160.0`; `"9"`, `"50"` and `"2"` give 2.25, written `2.3`.

For an idea that is not rated, leave all four fields `null`.

**Section 5** holds the method text, then the line `Reach unit: accounts per quarter.` (the unit and
period in use; `Reach unit: not known for every candidate, so reach is counted as 1 for all.` when
the fallback applies), then this table, one row per idea in ID order, `not rated: ` and the reason in
the Reach cell of an unrated idea:

```markdown
| Idea | Reach | Impact | Confidence | Effort |
|---|---|---|---|---|
| IDEA-01 | 400 | 1 | 80 | 2 |
```

**Section 6** holds, in this order and before any `###` heading: the proposal paragraph; the
capacity line; the cut table, one row per idea in rank order, then the unrated ideas with `-` in the
Rank, Score, Effort, Cumulative effort and Cut cells; the closing sentence.

- The proposal paragraph, before the user confirms: "Proposed, awaiting confirmation: promote
  IDEA-01 and IDEA-03; park IDEA-04 and IDEA-02." with the IDs in rank order, unrated ideas last, and
  `none` for an empty list. Three or more IDs are joined by commas, with "and" before the last:
  "promote IDEA-01, IDEA-03 and IDEA-04". Once the user has answered step 5, it says what was promoted, parked and
  rejected and why.
- The capacity line: `Capacity: 10 person-weeks (given by the user).` When the user gave none, C is
  half of the rated ideas' summed effort, and the line labels it as an assumption:
  `Capacity: 7.5 person-weeks (assumed: half of the candidates' summed effort).`
- The closing sentence: "The cut proposes dispositions only: it is not the first release cut, and it
  sets no requirement priority."

## Evaluation method text

Write this into section 5 as its first paragraph, followed by the reach line and the inputs table:

> Shortlist ranking (RICE): the candidates are the user's own list and no idea was added. Each was
> rated for reach, impact (3, 2, 1, 0.5 or 0.25), confidence (100, 80 or 50 percent) and effort in
> person-weeks. In the ideas, value is reach × impact, effort is the person-weeks and risk is
> 100 − confidence. The score is value × (100 − risk) ÷ 100 ÷ effort, rounded to one decimal; a
> higher score ranks higher.

## Example

Input: "Rank our invoicing app's backlog. Reach is accounts per quarter. CSV export of invoices
(400 accounts, 2 person-weeks); single sign-on with SAML (60 accounts, 6 person-weeks); dark mode
(900 accounts, 3 person-weeks); an audit log of invoice changes (150 accounts, 4 person-weeks). We
have 10 person-weeks." Only the single sign-on problem has evidence, from support tickets.

Output (excerpt):

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Accountants re-type invoice figures into their own spreadsheets every month."
    who: "Accountant at a customer"
    evidence: "[NEEDS CLARIFICATION: how many accounts export by hand today?]"
    severity: medium
  - id: PRB-02
    status: active
    statement: "IT admins at larger customers manage a separate password for every user."
    who: "IT admin at a customer"
    evidence: "14 support tickets asked for single sign-on in Q3 2026 (ticket: support export, Q3 2026)"
    severity: high
  - id: PRB-03
    status: active
    statement: "People who work late find the bright screen tiring."
    who: "Bookkeeper"
    evidence: "[NEEDS CLARIFICATION: how often is this reported?]"
    severity: low
  - id: PRB-04
    status: active
    statement: "Finance leads can't see who changed an invoice after it was sent."
    who: "Finance lead at a customer"
    evidence: "[NEEDS CLARIFICATION: how many disputes involve a changed invoice?]"
    severity: medium
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "CSV export of invoices"
    addresses:
      - PRB-01
    value: "400"
    effort: "2"
    risk: "20"
    score: 160.0
    disposition: open
    reason: null
  - id: IDEA-02
    status: active
    idea: "Single sign-on with SAML"
    addresses:
      - PRB-02
    value: "180"
    effort: "6"
    risk: "0"
    score: 30.0
    disposition: open
    reason: null
  - id: IDEA-03
    status: active
    idea: "Dark mode"
    addresses:
      - PRB-03
    value: "225"
    effort: "3"
    risk: "20"
    score: 60.0
    disposition: open
    reason: null
  - id: IDEA-04
    status: active
    idea: "An audit log of invoice changes"
    addresses:
      - PRB-04
    value: "300"
    effort: "4"
    risk: "20"
    score: 60.0
    disposition: open
    reason: null
```

Section 5, after the method text:

```markdown
Reach unit: accounts per quarter.

| Idea | Reach | Impact | Confidence | Effort |
|---|---|---|---|---|
| IDEA-01 | 400 | 1 | 80 | 2 |
| IDEA-02 | 60 | 3 | 100 | 6 |
| IDEA-03 | 900 | 0.25 | 80 | 3 |
| IDEA-04 | 150 | 2 | 80 | 4 |
```

IDEA-03 and IDEA-04 tie at 60.0, so the smaller effort ranks first. With 10 person-weeks, the limits
are 6, 8 and 10. Section 6, before the user confirms:

```markdown
Proposed, awaiting confirmation: promote IDEA-01 and IDEA-03; park IDEA-04 and IDEA-02.

Capacity: 10 person-weeks (given by the user).

| Rank | Idea | Score | Effort | Cumulative effort | Cut |
|---|---|---|---|---|---|
| 1 | IDEA-01 | 160.0 | 2 | 2 | must |
| 2 | IDEA-03 | 60.0 | 3 | 5 | must |
| 3 | IDEA-04 | 60.0 | 4 | 9 | could |
| 4 | IDEA-02 | 30.0 | 6 | 15 | won't |

The cut proposes dispositions only: it is not the first release cut, and it sets no requirement
priority.
```
