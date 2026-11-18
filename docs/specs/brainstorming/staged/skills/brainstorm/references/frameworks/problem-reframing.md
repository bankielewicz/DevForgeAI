# Problem reframing

## When to use / When not to use

**Use when** the topic, after intake, is a symptom ("sales are down"), a goal ("we want 10,000
users") or a solution ("add dark mode") and no problem can yet be stated with an affected person and
what hurts them. It finds the root causes and the jobs behind the topic, turns them into
how-might-we questions, and only then generates ideas.

**Avoid when** a problem can already be stated with a person and what hurts them. Then the
reframing adds nothing: use `diverge-converge`. Avoid it too when the user has a list to rank: use
`shortlist-ranking`.

## Steps

1. **State the starting point.** Write it in section 1 in the user's own words, and say whether it is
   a symptom, a goal or a solution.
2. **Five whys.** Take at most three starting points. For each, ask "why?" up to five times, one
   answer at a time. When the starting point is a goal or a solution, the first question is "What
   problem does this address, and for whom?" and its answer is why 1. Every answer must come from the
   user's words or from a source they named. When an answer is unknown, write
   `[NEEDS CLARIFICATION: <the question>]` as that why and stop the chain. Stop earlier when an
   answer is a cause the user could act on directly and a further "why?" would only restate it. The
   **root cause** is the last answered why. A chain that stopped on an unknown has a root cause that
   is not confirmed.
3. **Jobs to be done.** For each kind of person a root cause hurts, write the job in this form: "When
   [situation], I want to [motivation], so I can [outcome]." Use the user's words for the situation
   and the outcome.
4. **Write the problems.** Each root cause is one problem. Each job whose unmet state is not already
   a root cause's problem is another. A job and a root cause that name the same person and the same
   pain are one problem. Set `severity` to `high` when the user said it stops people doing what they
   came to do, costs money or harms someone; `low` when they called it an annoyance; otherwise
   `medium`, and say in section 5 that the severity was not given.
5. **How-might-we questions.** Write one for each problem, in the fixed shape below.
6. **Diverge.** Generate ideas, the user's own first, in their words, then yours. Aim for 5 to 15.
   Each idea answers at least one how-might-we question; link it to the problems of those questions.
7. **Surface assumptions.** For the ideas with the most promise, name what must be true for them to
   work, and how to check it.
8. **Evaluate.** Rate each idea's value, effort and risk, then compute the score (see the mapping).
9. **Converge.** Propose dispositions by the rule in the mapping. Ask the user to confirm.

## Questions to ask

- Starting point: "Is this something you see happening, something you want, or something you want
  to build?"
- Whys: "Why do you think that happens? What do you see that tells you so?"
- Whys: "Is that the cause, or does something else cause it?"
- Jobs: "When this happens to [person], what are they trying to get done?"
- Diverge: "Do you already have ideas? Tell me in your own words and I'll record them as given."
- Assumptions: "What has to be true for this idea to work? How could we find out cheaply?"
- Converge: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| State the starting point | Section 1, in prose |
| Five whys | Section 5: the "Five whys" block below |
| Jobs to be done | Section 3's table, one row for each kind of person, with the header `| Persona | Job to be done | Current workaround | Pain |` |
| Write the problems | `problems`: `statement`, `who`, `evidence`, `severity` |
| How-might-we questions | Section 5: the "How-might-we questions" block below |
| Diverge | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null` |
| Surface assumptions | `assumptions`: `statement`, `validation`, `state: open` |
| Evaluate | `ideas`: `value`, `effort`, `risk`, `score` |
| Converge | `ideas`: `disposition`, `reason`, only for user-confirmed values |

**Section 3.** One row for each distinct `who` among the active problems, in the order the values first appear in
section 2, the Persona cell equal to that value (when `references/intake.md` exists it gives the rule for the
other cells). The Job to be done cell holds that person's job in the form of step 3.

**Problems.** A root cause becomes `statement` "[Who] [suffers what] because [the root cause]." A
job becomes `statement` "[Who] wants to [outcome] but [the obstacle]." `who` is the kind of person.
`evidence` is the source behind the last answered why, or `"[NEEDS CLARIFICATION: ...]"`.

**Five whys block.** In section 5, after the method text, this shape, one chain for each starting
point, in this order. Each why is one sentence. The chain line and every bullet are one unwrapped
line. The last line names the problem the root cause became, and ends with ` (not confirmed)` when
the chain stopped on an unknown.

```markdown
### Five whys

Chain 1, starting point: "Sales are down 20% since spring"

- Why 1: Fewer visitors finish checkout.
- Why 2: Visitors must create an account before they can pay.
- Root cause: PRB-01
```

**How-might-we block.** In section 5, after the five whys, one bullet for each problem in ID order,
each in the shape `- PRB-NN: How might we [verb] [the person] [outcome]?` It is one sentence, starts
with a verb such as help, let or make, names the person, states the outcome and names no solution.

```markdown
### How-might-we questions

- PRB-01: How might we help an occasional customer complete a purchase in one visit?
```

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`. `value` is the benefit to the people in the problems it addresses. `effort` is the cost to
build and run it. `risk` is the chance it fails or causes harm.

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

Write this into section 5, followed by the two blocks above and any discussion the numbers do not
capture:

> Problem reframing: the topic was taken as a starting point, not as the problem. Five whys found
> the root causes, jobs to be done described what the affected people are trying to get done, and a
> how-might-we question was written for each problem before any idea was generated. Each idea was
> then rated high, medium or low for value, effort and risk. The score is 2 × value − effort − risk,
> counting high = 3, medium = 2 and low = 1 (range −4 to 4); a higher score is a stronger candidate
> for promotion.

## Example

Input: "Our online shop's sales are down 20% since spring. Visits are flat, but fewer visitors finish
checkout. In April we began to make customers create an account before paying, and customers who
emailed support said they did not want another password."

Output (excerpt). Section 3:

```markdown
| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| Occasional customer | When I find something I want, I want to pay in one step, so I can have it without another login | Gives up, or emails support | Abandons the purchase |
```

Section 5, after the method text:

```markdown
### Five whys

Chain 1, starting point: "Sales are down 20% since spring"

- Why 1: Fewer visitors finish checkout, while visits are flat.
- Why 2: Visitors must create an account before they can pay, a step added in April.
- Why 3: Customers do not want another password, as support emails say.
- Root cause: PRB-01

### How-might-we questions

- PRB-01: How might we help an occasional customer complete a purchase in one visit?
```

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Occasional customers abandon checkout because they must create an account and a password before paying."
    who: "Occasional customer"
    evidence: "Customers who emailed support said they did not want another password (note: the user's request, 2026-11-18)"
    severity: high
```

The frontmatter `sources` holds the entry that `evidence` quotes: `"note: the user's request, 2026-11-18"`.

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Offer guest checkout that asks only for an email address."
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

> Proposed, awaiting confirmation: promote IDEA-01 (score 4, cheap to try).
