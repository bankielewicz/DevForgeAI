# Problem reframing

## When to use / When not to use

**Use when** the topic is a symptom ("sign-ups are flat"), a goal ("grow revenue by 20%") or a
solution ("build a chatbot"): nobody's problem is stated yet, so ideas would have nothing to aim at.

**Avoid when** the request already says who is affected and what hurts them. Then use
`diverge-converge`.

## Steps

1. **List the start points.** Write down each symptom, goal or solution the request states, in the
   user's words. Each gets one why chain.
2. **Ask why, up to five times.** For each start point ask "Why does that happen?" (for a goal or a
   solution: "Why does that matter?"), then ask the same of the answer. An answer comes from the
   user, from a source, or, when neither has one, from you: then record it as an assumption ("We
   believe that …") and mark it in the chain. Stop the chain at the first of: five answers; the user
   says they don't know; two answers in a row are your own assumptions. The last answer is the root
   cause.
3. **Frame the problems.** Each chain gives one problem, stated from the affected person's side with
   its root cause. Two chains that end in the same root cause share one problem.
4. **State the job.** For each problem, one sentence: "When *situation*, *who* wants to *motivation*,
   so that *outcome*."
5. **Ask How-Might-We.** For each problem write one to three questions that start "How might we".
   Each names the person and the root cause, and holds no solution. Number them `HMW-01` onward
   across the document.
6. **Generate ideas.** First the user's own ideas, in their words. Then yours, until every HMW has
   at least one idea and there are between 5 and 15 in all. Each idea addresses the problem of the
   HMW it answers.
7. **Evaluate.** Rate each idea's value, effort and risk, then compute the score (see the mapping
   below).
8. **Propose.** Propose `promoted` for the ideas with a score of 2 or more, at most three of them:
   the highest score first, then the lower effort, then the lower ID. Propose `rejected` for every
   idea with a score of −1 or less. Propose `parked` for the rest, and for an idea that could not be
   rated. Each proposed reason is one sentence that starts "Score N: ". These are proposals: write a
   disposition only when the user confirms it at step 5.

## Questions to ask

- Start points: "What made you raise this now? What did you see?"
- Why: "Why does that happen?" and, of each answer, "And why is that?"
- Why, for a goal or a solution: "Why does that matter? What would it change, and for whom?"
- Job: "When does this come up for them, and what are they trying to get done?"
- Ideas: "Do you already have ideas? Tell me in your own words and I'll record them as given."
- Propose: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Ask why | `assumptions`: one per answer of your own, `statement` "We believe that …", `validation`, `state: open`; the why-chain line in section 5 |
| Frame the problems | `problems`: `statement`, `who`, `evidence`, `severity` |
| State the job | the job line in section 5 |
| Ask How-Might-We | the HMW line in section 5 |
| Generate ideas | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null`; the idea IDs on the HMW line |
| Evaluate | `ideas`: `value`, `effort`, `risk`, `score` |
| Propose | section 6 prose; `disposition` and `reason` only once confirmed |

**Problems.** `statement` is one sentence: who, what hurts, and "because" with the root cause. `who`
is the person in it. `evidence` is the chain's last answer that is not your own assumption, with its
source; when the root cause is your own assumption, it is
`"[NEEDS CLARIFICATION: is it true that <the first assumed answer>?]"`.

**Section 5** holds the method text, then these lines, grouped by problem in ID order:

```markdown
- Why chain for PRB-01: <start point> → because <answer 1> → because <answer 2> (assumed: ASM-01)
- Job for PRB-01: When <situation>, <who> wants to <motivation>, so that <outcome>.
- HMW-01 (PRB-01): How might we <question>? Ideas: IDEA-01, IDEA-02.
```

One why-chain line for each chain that ends in the problem, one job line, and one HMW line for each
of its questions. `(assumed: ASM-NN)` follows each answer that is your own. A user's idea that
answers no HMW goes on a last line, `- No HMW (the user's own): IDEA-07.`

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`. `value`: high when the idea removes the root cause of a problem it addresses, medium when
it weakens the root cause, low when it only treats the start point. `effort` is the cost to build
and run it. `risk` is the chance it fails or causes harm.

**Score.** Count high = 3, medium = 2, low = 1, and compute
`score = 2 × value − effort − risk`, an integer from −4 to 4. Write it unquoted. For example, value
high, effort medium, risk low gives 2 × 3 − 2 − 1 = 3. Leave all four fields `null` for an idea you
could not rate, and say why in section 5.

## Evaluation method text

Write this into section 5 as its first paragraph, followed by the why-chain, job and HMW lines:

> Problem reframing: each start point was asked "why" up to five times to reach a root cause, each
> problem was restated as a job to be done and as How-Might-We questions, and the ideas answer those
> questions. Each idea was rated high, medium or low for value (how far it removes the root cause),
> effort and risk. The score is 2 × value − effort − risk, counting high = 3, medium = 2 and low = 1
> (range −4 to 4); a higher score is a stronger candidate for promotion.

## Example

Input: "Sign-ups for our language-exchange meetup app have been flat for six months." The user adds
that most visitors leave on the page that asks for a home address.

Output (excerpt):

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Newcomers abandon sign-up because the app asks for a home address before it shows any meetup."
    who: "Newcomer to the city"
    evidence: "[NEEDS CLARIFICATION: is it true that newcomers distrust giving an address before seeing a meetup?]"
    severity: high
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Show this week's meetups before asking for anything."
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: 3
    disposition: open
    reason: null
  - id: IDEA-02
    status: active
    idea: "Ask for a neighbourhood instead of a full address."
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
    statement: "We believe that newcomers distrust giving a home address before they have seen a meetup."
    validation: "Interview five people who left on the address page."
    state: open
```

Section 5, after the method text:

```markdown
- Why chain for PRB-01: Sign-ups have been flat for six months → because most visitors leave on the address page → because they distrust giving a home address before they have seen a meetup (assumed: ASM-01)
- Job for PRB-01: When they are new in a city, a newcomer wants to find a meetup this week, so that they start speaking the language with people nearby.
- HMW-01 (PRB-01): How might we let a newcomer see meetups before we ask where they live? Ideas: IDEA-01, IDEA-02.
```

Section 6, before the user confirms:

> Proposed, awaiting confirmation: promote IDEA-01 (Score 3: it removes the root cause) and IDEA-02
> (Score 2: it weakens the root cause at low effort).
