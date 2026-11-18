# Risk-first MVP

## When to use / When not to use

**Use when** the request asks what to build first, for an MVP or a prototype, or what could make the
idea fail. It starts from the ways the idea could fail, ranks the beliefs it depends on by risk, and
makes the ideas the smallest things that test the riskiest beliefs.

**Avoid when** the user has a list to rank: use `shortlist-ranking`. Avoid it too when the product
exists and the topic is improving it: use `improve-existing`.

When `${CLAUDE_SKILL_DIR}/references/mvp-path.md` exists, it says how the assumption risk ranking
and the first release cut are written into the BRN. This framework only produces their inputs and
does not write either shape.

## Steps

1. **Name the bet.** Write one sentence in section 1: who has what problem, and the idea expected to
   solve it. State the problem from the user's side. It is the first problem.
2. **Run the pre-mortem.** Say: "It is six months after launch and it failed. Why?" Ask the user
   first, then add reasons of your own, 5 to 10 in all, one sentence each, covering these five
   causes: nobody wanted it; people did not change what they do; it could not be built or run; money
   or time ran out; something outside the team's control changed. Your own reasons are possibilities,
   not findings: they carry no evidence.
3. **Sort the reasons.** A reason that names a kind of person and a hurt they suffer today is a
   problem. Every other reason becomes an assumption: write its opposite as "We believe that ...",
   one assumption for each reason, merging equal ones. Record each reason and what it became in the
   pre-mortem block of section 5.
4. **Rate and rank the assumptions.** For each assumption set the **severity if wrong**, the
   **confidence** and the **riskiness**, as the mapping below says. Rank them by riskiness. Write the
   cheapest test that could show the assumption false as its `validation`, in two sentences: the first
   is the test, the second the pass line, the result that would show the assumption true. Ask, fake it
   by hand or use something that exists before building anything.
5. **Design the tests.** For each of the three highest-ranked assumptions, write one idea that is
   its cheapest test; add a stronger second test where one exists. Fewer than three assumptions
   means fewer tests. Each test idea starts with "Test ASM-NN: " and tests exactly one assumption.
   Record the user's own ideas as given, whether or not they test an assumption. When the ideas
   number fewer than five, add further tests for the highest-ranked assumption until there are five.
   Aim for no more than 15.
6. **Evaluate.** Rate each idea's value, effort and risk, then compute the score (see the mapping).
7. **Converge.** Propose dispositions by the rule in the mapping. Ask the user to confirm.

## Questions to ask

- Bet: "Who has the problem, and what do you expect to build for them?"
- Pre-mortem: "Imagine it is six months after launch and it has failed. What happened?"
- Pre-mortem: "What would have to be true about people, about us and about the world for it to work?"
- Assumptions: "What do you already know about this, and how do you know it?"
- Tests: "What is the least we could do, this week, to find out whether that is true?"
- Converge: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Name the bet | Section 1, in prose; `problems`: the first problem |
| Run the pre-mortem, sort | Section 5: the pre-mortem block; `problems` for the reasons that are problems; `assumptions`: `statement`, `validation`, `state: open` |
| Rate and rank the assumptions | Section 5: the riskiness table; each assumption's `validation`, a test and a pass line |
| Design the tests | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null` |
| Evaluate | `ideas`: `value`, `effort`, `risk`, `score` |
| Converge | `ideas`: `disposition`, `reason`, only for user-confirmed values |

**Problems.** `statement` from the user's side, `who` the kind of person, `evidence` the source or
`"[NEEDS CLARIFICATION: ...]"`. Set `severity` to `high` when the user said it stops people doing
what they came to do, costs money or harms someone; `low` when they called it an annoyance;
otherwise `medium`, and say in section 5 that the severity was not given. A test idea `addresses` the
first problem, and every other problem the tested assumption bears on.

**Pre-mortem block.** In section 5, after the method text, one bullet for each reason, in the order
asked, each on one unwrapped line ending with the ID of the problem or assumption it became in
parentheses.

```markdown
### Pre-mortem

- Neighbours would not lend tools to people they barely know. (ASM-01)
```

**Riskiness table.** The riskiness table is this framework's own working: it rates the test ideas and
nothing else, and it is never copied into the assumption risk ranking, which is the only ranking that
decides the first release cut. In section 5, after the pre-mortem block, one row for each active assumption
whose `state` is `open`, in rank order. The columns are the rank, the assumption's ID, one sentence on
what happens if it is wrong, its severity if wrong, its confidence and its riskiness.

- **Severity if wrong:** `high` when, if it were false, no idea in the first release would work or
  people would be harmed; `medium` when the release would work only after a large change; `low` when
  a small change would fix it. Count high = 3, medium = 2, low = 1.
- **Confidence** that it is true: `high` when the user gave data or a direct observation of this
  very thing (a problem's `evidence` that is not a marker, or a `sources` entry, states it);
  `medium` for indirect evidence, such as a similar product or an anecdote, or the user's own
  statement from experience; `low` when there is none, which is always the case for an assumption
  you added. Its uncertainty counts low = 3, medium = 2, high = 1.
- **Riskiness** = severity points × uncertainty points, an integer from 1 to 9.
- **Rank** by riskiness, highest first; break a tie by the lower assumption number.

```markdown
### Assumption riskiness

| Rank | Assumption | If wrong | Severity | Confidence | Riskiness |
|---|---|---|---|---|---|
| 1 | ASM-01 | Nobody lends, so no idea works | high | low | 9 |
```

For example, severity high and confidence low give 3 × 3 = 9; severity high and confidence medium
give 3 × 2 = 6.

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`:

- `value` is what the test teaches: `high` when it tests the assumption ranked 1, `medium` when it
  tests one ranked 2 or 3, and `low` when it tests one ranked 4 or lower, or none.
- `effort` is the work to run the test: `low` at most 5 working days of one person, `medium` 6 to
  20, `high` more than 20.
- `risk` is the chance the test misleads or harms real people: `low` when nobody outside the team
  is asked to take part and the result is hard to misread; `medium` when outsiders take part or the
  result could be misread; `high` when real money, property or safety is at stake.

**Score.** Count high = 3, medium = 2, low = 1, and compute
`score = 2 × value − effort − risk`, an integer from −4 to 4. Write it unquoted. For example,
value high, effort low, risk low gives 2 × 3 − 1 − 1 = 4. Leave all four fields `null` for an idea
you could not rate, and say why in section 5.

**Proposals.** For each of the three highest-ranked assumptions, propose `promoted` for the idea
that tests it with the highest score; break ties by the lower effort (low before medium before
high), then by the lower idea number. Propose `parked` for every other idea with a score of 1 or
more, and `rejected` for every idea with a score of 0 or less. An idea left unrated is proposed
`parked`, with "Not rated" and the reason. These are proposals: write a disposition only for a value
the user confirmed.

## Evaluation method text

Write this into section 5, followed by the pre-mortem block, the riskiness table and any discussion
the numbers do not capture:

> Risk-first MVP: a pre-mortem, "it failed in six months: why?", produced the problems and the
> assumptions. Each assumption was rated for how bad it is if wrong (high = 3, medium = 2, low = 1)
> and how uncertain it is (confidence low = 3, medium = 2, high = 1); riskiness is their product, and
> the assumptions are ranked by it. Each idea is the smallest test of one assumption, rated high,
> medium or low for value (what it teaches, by the assumption's rank), effort and risk. The score is
> 2 × value − effort − risk, counting high = 3, medium = 2 and low = 1 (range −4 to 4); a higher
> score is a stronger candidate for promotion.

## Example

Input: "Brainstorm a mobile app where neighbours lend each other tools. What could make it fail, and
what should we test first?"

Output (excerpt). Section 5, after the method text:

```markdown
### Pre-mortem

- Neighbours would not lend tools to people they barely know. (ASM-01)
- Borrowers would not return tools in working order. (ASM-02)
- Too few neighbours own tools worth lending. (ASM-03)
- People would not install an app to borrow a tool once a year. (ASM-04)
- Homeowners who need a tool for a job today cannot find one nearby to borrow. (PRB-02)

### Assumption riskiness

| Rank | Assumption | If wrong | Severity | Confidence | Riskiness |
|---|---|---|---|---|---|
| 1 | ASM-01 | Nobody lends, so no idea works | high | low | 9 |
| 2 | ASM-02 | Lenders stop lending after the first loss | high | medium | 6 |
| 3 | ASM-04 | Borrowers never arrive | medium | low | 6 |
| 4 | ASM-03 | The shelf stays too small to be useful | medium | medium | 4 |
```

The last reason names a person and a hurt they suffer today, so it became a problem, PRB-02; the others
became assumptions. ASM-02 and ASM-04 tie at 6, so the lower number ranks first. The assumption and the test:

```yaml
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that neighbours will lend tools to people they barely know."
    validation: "Ask 20 neighbours on one street, by a note through the door, whether they would lend a drill. The assumption holds if at least 10 say yes."
    state: open
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Test ASM-01: put a note through 20 doors on one street asking whether the neighbour would lend a drill to someone they know by sight."
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: open
    reason: null
```

Section 6, before the user confirms:

> Proposed, awaiting confirmation: promote IDEA-01 (the cheapest test of the riskiest assumption);
> park IDEA-02 (a stronger test of the same assumption, score 2).
