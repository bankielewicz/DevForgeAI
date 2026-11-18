# Shortlist ranking

## When to use / When not to use

**Use when** the user already has a list of candidate ideas, or names a backlog or a file of them, and
asks to rank, prioritise, choose among or cut them. The ideas are the user's: this framework rates
them and proposes a cut. It does not generate ideas.

**Avoid when** the user has no list yet, or wants new ideas as well as a ranking. Use
`diverge-converge`, then rank its ideas.

**The 5-to-15 rule does not apply.** The number of ideas is the number of candidates the user gave,
from 1 to 30. When the list holds more than 30 candidates, take the first 30 in the order given and
say in section 5 how many were left out and which was the first.

## Steps

1. **Take the list as given.** Record each candidate as an idea in the user's own words, in the order
   given, with `disposition: open`. Add no idea, merge none and split none. When two candidates are
   the same, keep both and say so in section 5. When the list is in a file or an issue list the user
   named, read it and take its items.
2. **Frame the problems.** Every idea must address at least one problem. Take each problem from the
   user's stated goal and from what each candidate is meant to fix: one problem per distinct pain,
   stated from the affected person's side, shared by the candidates that fix the same pain. Set
   `severity` to `high` when the user said it stops people doing what they came to do, costs money or
   harms someone; `low` when they called it an annoyance; otherwise `medium`, and say in section 5
   that the severity was not given.
3. **Surface assumptions.** For each idea, name the one belief its reach or its impact rests on, in
   "We believe that ..." form, with how to check it. Ideas that rest on the same belief share one
   assumption.
4. **Gather the figures.** For each idea you need two figures from the user or from a source they
   named, never from your own estimate:
   - **Reach:** how many people, in the `who` of the problems the idea addresses, it reaches in one
     quarter (three months). Convert a weekly figure by × 13, a monthly one by × 3 and a yearly one
     by ÷ 4, rounding half up to a whole number.
   - **Effort:** the work to build and run it, in person-weeks (one person's five working days),
     rounded up to the next 0.5, never below 0.5.

   An idea missing either figure is **not rated**: leave `value`, `effort`, `risk` and `score` all
   `null` and write `[NEEDS CLARIFICATION: reach]` or `[NEEDS CLARIFICATION: effort]` for the missing
   figure in section 5's table.
5. **Rate and compute.** For each rated idea:
   - **Impact**, your rating of how far the idea removes the pain of the problems it addresses, for
     the people it reaches: 3 (massive: removes it), 2 (high: removes most), 1 (medium: removes about
     half), 0.5 (low: a noticeable reduction) or 0.25 (minimal: barely noticeable).
   - **Confidence**, from the evidence only: 100 when the reach or effort figure comes from a source
     the user named (a document, data or a ticket) and every addressed problem's `evidence` is not a
     marker; 80 when the figures are the user's own estimates and every addressed problem's `evidence`
     is not a marker; 50 in every other case.
   - Then work out the four fields as the mapping below says.
6. **Rank.** Sort the rated ideas by score, highest first. Break a tie by the lower effort, then by
   the lower idea number. Number the ranks from 1. Not-rated ideas have no rank.
7. **Cut.** Give each rated idea one of must, should, could or won't, as the mapping below says. The
   cut is a proposal, written in section 6 prose. It is never a field: priority stays with the PRD.
8. **Propose dispositions.** Map the cut to proposals as the mapping below says, and ask the user to
   confirm them.

## Questions to ask

- Framing: "What is each of these meant to fix, and for whom?"
- Figures: "About how many of those people would each idea reach in a quarter? Where does the number
  come from?"
- Figures: "How many person-weeks would each take to build and run?"
- Figures: "How many person-weeks can you spend in this period?" (the capacity; skip it when the
  user has given one or has said there is none)
- Assumptions: "What has to be true for this idea to reach that many people, and how could we check?"
- Converge: "Here is my proposed cut and the dispositions that follow from it. Which do you confirm
  or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Take the list | `ideas`: `idea`, `disposition: open`, `reason: null` |
| Frame the problems | `problems`: `statement`, `who`, `evidence`, `severity`; then each idea's `addresses` |
| Surface assumptions | `assumptions`: `statement`, `validation`, `state: open` |
| Gather the figures, rate | `ideas`: `value`, `effort`, `risk`, `score`; section 5: the rating table |
| Cut | Section 6 prose only: the priority cut table |
| Propose dispositions | The step-5 proposals; `disposition` only for user-confirmed values |

**The four fields.** Reach and impact, which have no field of their own, are folded into `value` and
kept in section 5's table, so that every score can be worked out again from the BRN.

| Field | Holds | Unit and form |
|---|---|---|
| `value` | reach × impact | Impact-weighted people per quarter. A quoted number: `"1800"` |
| `effort` | The effort of step 4 | Person-weeks. A quoted number: `"2.5"` |
| `risk` | 100 − confidence | The chance, in per cent, that the idea does not deliver its impact: `"0"`, `"20"` or `"50"` |
| `score` | value × (100 − risk) ÷ 100 ÷ effort | Impact-weighted people per quarter, per person-week; an unquoted number with exactly one decimal: `720.0` |

Write `value`, `effort` and `risk` as quoted strings, so that they also satisfy the brainstorm
schema, which types them as strings. Write a number without trailing zeros (`"2.5"`, `"4"`), except
`score`, which always has one decimal place, rounded half up (12.25 becomes 12.3). Leave all four
fields `null` for an idea that is not rated.

**Worked example.** Reach 900, impact 2, confidence 80, effort 2: value = 900 × 2 = 1800; risk =
100 − 80 = 20; score = 1800 × (100 − 20) ÷ 100 ÷ 2 = 1800 × 0.8 ÷ 2 = 720.0. The fields are
`value: "1800"`, `effort: "2"`, `risk: "20"`, `score: 720.0`. A second idea: reach 600, impact 0.5,
confidence 100, effort 8: value 300, risk 0, score = 300 × 1 ÷ 8 = 37.5.

**The cut.** Rank the rated ideas as step 6 says. Then:

- **With a capacity** (person-weeks the user gave): add the efforts down the ranking, so that each
  idea has a running total that includes its own effort. The idea is a **must** when its running total
  is at most 0.6 × capacity, a **should** when it is above that and at most 0.8 × capacity, a
  **could** when it is above that and at most the capacity, and a **won't** when it is above the
  capacity.
- **Without a capacity:** let k be the number of rated ideas divided by 4, rounded up. Ranks 1 to k
  are musts, k + 1 to 2k shoulds, 2k + 1 to 3k coulds and the rest won'ts. Say in section 5 that no
  capacity was given.

**From the cut to proposals.** A must or a should is proposed `promoted`. A could is proposed
`parked`. A won't is proposed `rejected` when its score is below one tenth of the highest score, and
`parked` otherwise. A not-rated idea is proposed `parked`, with the missing figure as its reason. Each
proposal's reason names the cut and the score, for example "Must: rank 1, score 720.0". These are
proposals: write a disposition only for a value the user confirmed.

**Where the cut goes.** Section 6, after any other shape that section holds, as this block. The
status line never changes: a confirmed disposition is recorded in the convergence prose, and the cut
stays a proposal. One row for each idea: the ranked ideas first, in rank order, then the not-rated
ideas in ID order. The Rank cell is the rank number, or `-` for a not-rated idea. The Cut cell is
exactly `Must`, `Should`, `Could`, `Won't` or `Not rated`. The Proposed disposition cell is exactly
`promoted`, `parked` or `rejected`. Every row is one unwrapped line.

```markdown
### Priority cut

Priority cut: a proposal; priority stays with the PRD

| Rank | Idea | Cut | Proposed disposition | Why |
|---|---|---|---|---|
| 1 | IDEA-01 | Must | promoted | Must: rank 1, score 720.0 |
| - | IDEA-05 | Not rated | parked | Not rated: reach is missing |
```

## Evaluation method text

Write this into section 5, then the capacity line, then the rating table below it, then any
discussion the numbers do not capture:

> Shortlist ranking: the ideas are the user's own shortlist; none were added. Each was rated with
> a RICE-style method. Reach is the number of people the idea reaches in one quarter. Impact is 3, 2,
> 1, 0.5 or 0.25. Value is reach × impact. Confidence is 100, 80 or 50 per cent, and risk is
> 100 − confidence. Effort is in person-weeks. The score is value × (100 − risk) ÷ 100 ÷ effort,
> rounded to one decimal; a higher score ranks higher. The cut in section 6 into must, should, could
> and won't is a proposal only: priority stays with the PRD.

The capacity line is `Capacity: N person-weeks` or `Capacity: not given`. The rating table has
this header, one row per idea in ID order, with `[NEEDS CLARIFICATION: ...]` in a missing cell:

```markdown
| Idea | Reach | Impact | Confidence | Effort | Value | Risk | Score |
|---|---|---|---|---|---|---|---|
```

## Example

Input: "Our dental clinic has four ideas to cut no-shows; rank them. Patients reached per quarter:
text reminders 900, a deposit at booking 900, a waiting list 300, reminder calls 600. Person-weeks:
2, 5, 2.5 and 8. We have 12 person-weeks. We miss one in eight booked appointments by our own count;
the reminder-call figures are from our call log." The ideas are the user's. PRB-01's `evidence` is
that count, not a marker. Confidence is 80 for the three ideas whose figures are the user's own
estimates, and 100 for the reminder calls, whose figures come from a named source.

Output (excerpt). Section 5, after the method text:

```markdown
Capacity: 12 person-weeks

| Idea | Reach | Impact | Confidence | Effort | Value | Risk | Score |
|---|---|---|---|---|---|---|---|
| IDEA-01 | 900 | 2 | 80 | 2 | 1800 | 20 | 720.0 |
| IDEA-02 | 900 | 3 | 80 | 5 | 2700 | 20 | 432.0 |
| IDEA-03 | 300 | 1 | 80 | 2.5 | 300 | 20 | 96.0 |
| IDEA-04 | 600 | 0.5 | 100 | 8 | 300 | 0 | 37.5 |
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Text a reminder before the visit."
    addresses:
      - PRB-01
    value: "1800"
    effort: "2"
    risk: "20"
    score: 720.0
    disposition: open
    reason: null
```

Section 6, before the user confirms (running totals 2, 7, 9.5 and 17.5, against limits 7.2, 9.6 and
12; one tenth of 720.0 is 72.0):

```markdown
Proposed, awaiting confirmation: promote IDEA-01, IDEA-02 and IDEA-03; reject IDEA-04.

### Priority cut

Priority cut: a proposal; priority stays with the PRD

| Rank | Idea | Cut | Proposed disposition | Why |
|---|---|---|---|---|
| 1 | IDEA-01 | Must | promoted | Must: rank 1, score 720.0 |
| 2 | IDEA-02 | Must | promoted | Must: rank 2, score 432.0 |
| 3 | IDEA-03 | Should | promoted | Should: rank 3, score 96.0 |
| 4 | IDEA-04 | Won't | rejected | Won't: rank 4, score 37.5, below 72.0 |
```
