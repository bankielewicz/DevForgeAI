# Improve an existing product

## When to use / When not to use

**Use when** the product exists (it is built or in use) and the topic is improving, extending or
fixing it. The ideas start from what the product does today.

**Avoid when** nothing is built or in use yet. Then use `diverge-converge`, or `risk-first-mvp` to
find what to build first.

## Steps

1. **Gather the sources.** List what tells you how the product works today: the project's documents
   that step 1 read, the user's description, data, tickets, interviews. Record each in the BRN's
   `sources`. The user's description in the request counts as a source.
2. **Write the baseline.** From the sources only, list up to seven things the product does today
   that the topic touches, each with the source it comes from. It is a working list. What the BRN
   needs of it goes into section 1 as sentences that each end with their source in parentheses.
   Write nothing about the product that no source says: put a `[NEEDS CLARIFICATION: …]` marker
   instead.
3. **Frame the problems.** From the sources, say who is hurting with the product as it is, and how.
4. **Run SCAMPER.** Record the user's own ideas first, in their words. Then take the seven prompts
   in order. For each, ask its question of the baseline and write at most two ideas. Each idea
   changes something the baseline names and addresses a framed problem.

   | Prompt | Question |
   |---|---|
   | Substitute | What part, step, material or rule could be replaced by another? |
   | Combine | What two parts, steps or audiences could be merged or offered together? |
   | Adapt | What works elsewhere, in this product or another, that could be borrowed here? |
   | Modify | What could be made larger, smaller, more frequent or more visible? |
   | Put to another use | Who else, or what other job, could what exists serve as it is? |
   | Eliminate | What could be removed without hurting the people in the problems? |
   | Reverse | What order, direction or role could be turned around? |

   **A prompt that yields nothing.** When no answer both changes something in the baseline and
   addresses a framed problem, write no idea for that prompt and say why in its section-5 line.
   Never stretch an idea to fill a prompt. The 5-to-15 rule does not apply here: the prompts give
   between 0 and 14 ideas, and the count is what it is. If there is no idea at all, yours or the
   user's, tell the user "Framework: `diverge-converge`, because SCAMPER produced no idea for this
   product." and go on with that framework from its step 2.
5. **Surface assumptions.** Name what must be true for the ideas to work, and how to check it: among
   them, that current users accept the change.
6. **Evaluate.** Rate each idea's value, effort and risk, then compute the score (see the mapping
   below).
7. **Propose.** Propose `promoted` for the ideas with a score of 2 or more, at most three of them:
   the highest score first, then the lower effort, then the lower ID. Propose `rejected` for every
   idea with a score of −1 or less. Propose `parked` for the rest, and for an idea that could not be
   rated. Each proposed reason is one sentence that starts "Score N: ". These are proposals: write a
   disposition only when the user confirms it at step 5.

## Questions to ask

- Sources: "What should I read to learn how it works today: documents, tickets, numbers?"
- Baseline: "Walk me through what a user does today, step by step."
- Problems: "Where does it hurt today, and for whom? What do they do instead?"
- SCAMPER: the question of each prompt, in the table above.
- Ideas: "Do you already have ideas? Tell me in your own words and I'll record them as given."
- Propose: "Here are my proposed dispositions. Which do you confirm or change? Are we done?"

## Mapping to the BRN

| Step | Writes |
|---|---|
| Gather the sources | the frontmatter's `sources` |
| Write the baseline | section 1 prose, each sentence with its source |
| Frame the problems | `problems`: `statement`, `who`, `evidence`, `severity` |
| Run SCAMPER | `ideas`: `idea`, `addresses`, with `disposition: open` and `reason: null`; the seven prompt lines in section 5 |
| Surface assumptions | `assumptions`: `statement`, `validation`, `state: open` |
| Evaluate | `ideas`: `value`, `effort`, `risk`, `score` |
| Propose | section 6 prose; `disposition` and `reason` only once confirmed |

**Idea IDs.** The user's own ideas come first, in the order given; then the prompts' ideas, in the
prompts' order.

**Section 5** holds the method text, then exactly these seven lines, in this order, each ending with
the IDs of that prompt's ideas or with `no idea (` and the reason `)`:

```markdown
- Substitute: IDEA-01
- Combine: no idea (the product has one audience and one flow)
- Adapt: IDEA-02, IDEA-03
- Modify: IDEA-04
- Put to another use: no idea (nothing that exists serves another job as it is)
- Eliminate: IDEA-05
- Reverse: IDEA-06
```

When the user gave ideas of their own, an eighth line follows: `- The user's own: IDEA-07`.

**Ratings.** Write `value`, `effort` and `risk` as the quoted strings `"high"`, `"medium"` or
`"low"`. `value` is the benefit to the people in the problems the idea addresses. `effort` is the
cost to build and run it, with the cost of moving current users and data to it. `risk` is the chance
it fails, causes harm, or breaks something that works for current users.

**Score.** Count high = 3, medium = 2, low = 1, and compute
`score = 2 × value − effort − risk`, an integer from −4 to 4. Write it unquoted. For example, value
high, effort low, risk medium gives 2 × 3 − 1 − 2 = 3. Leave all four fields `null` for an idea you
could not rate, and say why in section 5.

## Evaluation method text

Write this into section 5 as its first paragraph, followed by the seven prompt lines:

> Improve existing (SCAMPER): starting from what the sources say the product does today, the seven
> SCAMPER prompts (substitute, combine, adapt, modify, put to another use, eliminate, reverse) were
> each asked of it, and a prompt with no honest answer was left without an idea. Each idea was rated
> high, medium or low for value, effort and risk. The score is 2 × value − effort − risk, counting
> high = 3, medium = 2 and low = 1 (range −4 to 4); a higher score is a stronger candidate for
> promotion.

## Example

Input: "Improve our class-booking web app for a climbing gym. Members pick a class from a weekly
timetable, pay per class by card and get a confirmation email. Staff cancel a class by editing the
timetable, and members only find out if they look."

Output (excerpt):

```yaml
problems:
  - id: PRB-01
    status: active
    statement: "Members turn up for classes that staff cancelled, because nothing tells them."
    who: "Gym member"
    evidence: "Staff cancel a class by editing the timetable, and members only find out if they look (note: user, conversation of 2026-11-18)"
    severity: high
```

```yaml
ideas:
  - id: IDEA-01
    status: active
    idea: "Replace the silent timetable edit with a Cancel button that emails everyone booked."
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
    idea: "Offer a spot in the next class of the same kind inside the cancellation email."
    addresses:
      - PRB-01
    value: "medium"
    effort: "medium"
    risk: "low"
    score: 1
    disposition: open
    reason: null
  - id: IDEA-03
    status: active
    idea: "Refund the card payment automatically when staff cancel."
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "medium"
    score: 2
    disposition: open
    reason: null
```

Section 5, after the method text:

```markdown
- Substitute: IDEA-01
- Combine: IDEA-02
- Adapt: no idea (no other part of the product sends messages that could be borrowed)
- Modify: no idea (making the timetable more visible still leaves members to look)
- Put to another use: no idea (the confirmation email is sent once and can't carry later news)
- Eliminate: no idea (removing cancellation would hurt members more)
- Reverse: IDEA-03
```

Section 6, before the user confirms:

> Proposed, awaiting confirmation: promote IDEA-01 (Score 4: members are told at once, at low
> effort) and IDEA-03 (Score 2: no member pays for a cancelled class); park IDEA-02 (Score 1: it
> needs IDEA-01 first).
