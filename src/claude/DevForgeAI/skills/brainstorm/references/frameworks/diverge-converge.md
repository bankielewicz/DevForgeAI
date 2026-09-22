# Diverge-converge

The default framework. First widen the space (problems, then ideas) without judging. Then
narrow it with an impact/effort evaluation, and end with dispositions the user confirms.

## When to use / When not to use

**Use when** the topic is open: a new product or feature, a pain point, or a set of options to
explore and narrow down. It is also the fallback when no other framework fits.

**Don't use when** the user already has one fixed solution and only wants it critiqued or planned.
Say so, and ask whether they still want a brainstorm. In a non-interactive session, note it in
section 1 of the BRN and proceed.

## Steps

1. **Frame.** State the topic in one sentence, with the trigger, affected users and constraints from intake.
2. **Diverge on problems.** List the problems behind the topic from the user's side. Include the user's
   own problems in their words. Don't evaluate yet.
3. **Diverge on ideas.** For each problem, generate ideas. Aim for range: quick fixes, bigger bets,
   non-software options and "do nothing". Record the user's ideas in their own words next to yours.
   Don't evaluate yet.
4. **Surface assumptions.** For the most promising ideas, name what must be true for them to work,
   and how each could be checked.
5. **Evaluate.** Rate each idea on value, effort and risk (high, medium or low) and compute a score
   (below). Show the user a table sorted by score.
6. **Converge.** Propose a disposition and a one-line reason for each idea:
   `promoted` (take into the PRD), `parked` (worth keeping, not now) or `rejected`. Ask the user to
   confirm or change them, and whether the brainstorm has converged.

## Questions to ask

| Step | Questions |
|---|---|
| Frame | What triggered this now? Who is affected? What constraints (time, budget, platform, policy) apply? |
| Diverge on problems | What goes wrong for them today? What do they do instead? How do we know? |
| Diverge on ideas | What would you try first? What's the smallest thing that could help? What would a bold version look like? |
| Surface assumptions | What would have to be true for this idea to work? How could we check that cheaply? |
| Evaluate | Do these ratings match your sense of value and effort? Anything I've misjudged? |
| Converge | Do you accept these dispositions? Which would you change? Can I mark the brainstorm converged? |

Skip any question the request or conversation has already answered.

## Mapping to the BRN

| Step | Fills |
|---|---|
| Frame | Section 1 (Context) and section 3 (Target users) prose |
| Diverge on problems | `problems`: `statement` from the user's side, `who`, `evidence` (source, or `[NEEDS CLARIFICATION: …]`), `severity` |
| Diverge on ideas | `ideas`: `idea`, `addresses` (the `PRB-NN` it helps), `disposition: open`, `reason: null` |
| Surface assumptions | `assumptions`: `statement` ("We believe that…"), `validation`, `state: open` |
| Evaluate | On each idea: `value`, `effort` and `risk` as quoted `"high"`, `"medium"` or `"low"`; `score` as a number |
| Converge | On each idea: `disposition` and `reason`, **only as the user confirmed them**. Section 6 prose |

**Score:** value (high 3, medium 2, low 1) × 2, minus effort (high 3, medium 2, low 1), minus
risk (high 2, medium 1, low 0). The range is −3 to 5. Higher is better. Write the number unquoted.

## Evaluation method text

Write this into section 5 of the BRN, then add any discussion the numbers don't capture:

> Diverge-converge with an impact/effort lens. Each idea was rated high, medium or low for value,
> effort and risk. Score = 2 × value − effort − risk, with high = 3, medium = 2 and low = 1 for value
> and effort, and high = 2, medium = 1 and low = 0 for risk (range −3 to 5).

## Example

Input: "Brainstorm ways to cut onboarding drop-off in our mobile banking app. New users abandon at
identity verification. Constraint: no new vendors this quarter."

Output (excerpt):

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Let users save progress and resume verification later by email link"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: 4
    disposition: open
    reason: null
```

Proposed at convergence, not yet written: `IDEA-01 → promoted`, reason "biggest drop-off point,
no new vendor needed". It is written only after the user confirms it.
