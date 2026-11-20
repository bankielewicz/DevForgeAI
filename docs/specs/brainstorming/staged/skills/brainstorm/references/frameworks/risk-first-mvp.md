# Risk-first MVP

## When to use / When not to use

**Use when** the user asks what to build first, for an MVP or a prototype, or what could make the
idea fail. The ideas are small things that would show whether the idea can work.

**Avoid when** the user only wants an existing list ranked (use `shortlist-ranking`), or wants a
wide range of options (use `diverge-converge`).

## Steps

1. **State the bet.** One sentence: what is to be built, for whom, and what it should change for
   them. Frame the problems it is meant to solve, from the affected person's side.
2. **Run the pre-mortem.** Say: "It is six months after launch and this has failed. Why?" Record the
   user's reasons first, in their words, and keep them all. Add your own until there are at least
   three, and stop adding at seven.
3. **Sort each reason.** Ask of each: "Is this true today, for a person, whether or not we build
   anything?" If yes, it is a problem: frame it, or point to the problem that already says it. If
   no, it is an assumption: write the belief that must hold for the reason not to happen, starting
   "We believe that", with how to check it. "Front-desk staff have no time to learn a new tool" is
   true today: a problem. "Patients won't open texts from the clinic" is about what happens once it
   is built: the assumption "We believe that patients open texts from the clinic."
4. **Generate test ideas.** Record the user's own ideas first, in their words. Then, for each
   assumption in ID order, write one idea: the smallest thing the team could put in front of the
   affected people that would show whether the assumption holds. Of the candidates you can think of
   for an assumption, the smallest is the one that takes the least time to give a result. If there
   are fewer than 5 ideas, go through the assumptions again in ID order and add a second, different
   test for each until there are 5. Stop at 15.
5. **Evaluate.** For each idea, list the assumptions it tests: those its result would move to
   validated or invalidated. Then rate its value, effort and risk and compute the score (see the
   mapping below).
6. **Propose.** Propose `promoted` for the ideas with a score of 2 or more, at most three of them:
   the highest score first, then the lower effort, then the lower ID. Propose `rejected` for every
   idea with a score of −1 or less. Propose `parked` for the rest, and for an idea that could not be
   rated. Each proposed reason is one sentence that starts "Score N: ". These are proposals: write a
   disposition only when the user confirms it at step 5.

This framework does not say which assumption is riskiest and does not choose the first release. The
workflow's step 5 ranks the assumptions and proposes the first release cut from that ranking, for
every framework. Here, each assumption gets a test idea, whatever its rank will be.

## Questions to ask

- Bet: "What do you want to build, for whom, and what should it change for them?"
- Pre-mortem: "It is six months after launch and this has failed. Why?"
- Pre-mortem: "What would have to be true for it to work that you haven't checked?"
- Test ideas: "What is the smallest thing you could put in front of them to find out?"
- Ideas: "Do you already have ideas? Tell me in your own words and I'll record them as given."
- Propose: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| State the bet | `problems`: `statement`, `who`, `evidence`, `severity`; the bet line in section 5 |
| Run the pre-mortem | the reason lines in section 5 |
| Sort each reason | `problems`, or `assumptions`: `statement`, `validation`, `state: open`; the item's ID on the reason line |
| Generate test ideas | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null` |
| Evaluate | the tests lines in section 5; `ideas`: `value`, `effort`, `risk`, `score` |
| Propose | section 6 prose; `disposition` and `reason` only once confirmed |

**Section 5** holds the method text, then these lines: the bet; one line per reason, numbered from
1, the user's first, each ending with the ID of the one problem or assumption it became; one line
per idea in ID order, naming the assumptions it tests in ID order, or `no assumption`.

```markdown
- Bet: <what is built> for <who>, so that <what changes for them>.
- Reason 1: <the reason> (ASM-01)
- Reason 2: <the reason> (PRB-02)
- IDEA-01 tests ASM-01, ASM-03
- IDEA-02 tests no assumption
```

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`.

- `value`: high when the idea tests two or more assumptions, medium when it tests one, low when it
  tests none.
- `effort`: the time until its result is known, for the people the user has: low is two weeks or
  less, medium is up to six weeks, high is more.
- `risk`: the chance that the result is unclear, or that trying it harms the affected people or the
  user's name with them.

**Score.** Count high = 3, medium = 2, low = 1, and compute
`score = 2 × value − effort − risk`, an integer from −4 to 4. Write it unquoted. For example, value
medium, effort low, risk low gives 2 × 2 − 1 − 1 = 2. Leave all four fields `null` for an idea you
could not rate, and say why in section 5.

## Evaluation method text

Write this into section 5 as its first paragraph, followed by the bet, reason and tests lines:

> Risk-first MVP: a pre-mortem listed the reasons the idea could fail; each reason became a problem
> that exists today or an assumption that must hold, and the ideas are the smallest things that
> would test those assumptions. Each idea was rated high, medium or low for value (how many
> assumptions it tests), effort (the time until its result is known) and risk. The score is
> 2 × value − effort − risk, counting high = 3, medium = 2 and low = 1 (range −4 to 4); a higher
> score is a stronger candidate for promotion.

## Example

Input: "What should the MVP be for text reminders at our dental clinic? We want fewer no-shows."

Output (excerpt):

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Patients forget appointments booked weeks ahead."
    who: "Returning patient"
    evidence: "[NEEDS CLARIFICATION: current no-show rate]"
    severity: high
  - id: PRB-02
    status: active
    statement: "Front-desk staff have no time in the day to learn or run a new tool."
    who: "Front-desk staff"
    evidence: "[NEEDS CLARIFICATION: how many hours a week does the front desk spend on calls?]"
    severity: medium
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "For two weeks, text each patient by hand from the front-desk phone two days before the visit, with a reply-to-rebook line."
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: open
    reason: null
  - id: IDEA-02
    status: active
    idea: "Ask ten patients at check-out whether they would want a text from the clinic, and on which number."
    addresses:
      - PRB-01
    value: "medium"
    effort: "low"
    risk: "low"
    score: 2
    disposition: open
    reason: null
```

```yaml
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that patients open texts from the clinic."
    validation: "Count the replies to two weeks of hand-sent reminders."
    state: open
  - id: ASM-02
    status: active
    statement: "We believe that a patient who can't come will rebook by text instead of staying silent."
    validation: "Count the rebooking replies among the reminded patients who did not come."
    state: open
```

Section 5, after the method text:

```markdown
- Bet: text reminders for returning patients, so that fewer of them miss a visit.
- Reason 1: Patients won't open texts from the clinic (ASM-01)
- Reason 2: Front-desk staff have no time to learn a new tool (PRB-02)
- Reason 3: Patients who can't come still won't tell us (ASM-02)
- IDEA-01 tests ASM-01, ASM-02
- IDEA-02 tests ASM-01
```

Section 6, before the user confirms:

> Proposed, awaiting confirmation: promote IDEA-01 (Score 4: one hand-run fortnight tests both
> assumptions) and IDEA-02 (Score 2: a day's asking tests ASM-01).
