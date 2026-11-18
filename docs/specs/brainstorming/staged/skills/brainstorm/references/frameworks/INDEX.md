# Brainstorming frameworks

This index lists five frameworks. Choose one with the selection rules below: take the first rule that
matches the request, and use the framework in its last column. Then read that framework's file, which
sits next to this index.

## Selection rules

| # | When | Framework |
|---|---|---|
| 1 | The user names a framework that the index lists | that one |
| 2 | The request supplies three or more candidate ideas, or names a backlog or list to use, and asks to rank, prioritise, choose among or cut them | `shortlist-ranking` |
| 3 | The request asks what to build first, for an MVP or a prototype, or what could make the idea fail | `risk-first-mvp` |
| 4 | Project kind is brownfield and the topic is improving, extending or fixing the existing product | `improve-existing` |
| 5 | After intake, no problem can be stated with an affected person and what hurts them (the topic is a symptom, a goal or a solution) | `problem-reframing` |
| 6 | Otherwise | `diverge-converge` |

Terms the rules use:

- **Names a framework:** the request uses the framework's name from the table below, written with a
  hyphen or a space, in any case. A phrase that only resembles a name does not count.
- **Candidate ideas:** separate options the user lists in the request or in a file or issue list the
  request names.
- **Project kind:** the kind that step 1 wrote on the first line of section 1 of the BRN (`Project kind:
  greenfield` or `Project kind: brownfield`), when there is one; the line's `[NEEDS CLARIFICATION: ...]` form
  counts as the assumed kind below. Without such a line, decide it from the request (the arguments and every
  message the user has written in this conversation), case-insensitively and on whole words. Phrases of exactly
  one list below give that kind. Phrases of both lists, or of neither, give the assumed kind: brownfield when a
  Glob of `docs/specs/prd/PRD-*.md` matches at least one file (never a listing of the project root), greenfield
  when it matches none.
  - Greenfield phrases: `greenfield`, `from scratch`, `brand new`, `new product`, `new app`, `new service`,
    `new system`, `nothing built yet`, `not built yet`, `haven't built`, `have not built`, `no product yet`,
    `idea stage`, `starting a new`.
  - Brownfield phrases: `brownfield`, `existing` followed by a space and one of `product`, `app`, `application`,
    `system`, `service`, `platform`, `site`, `website`, `codebase`, `software`, `tool`, `feature`; `already live`,
    `already built`, `already launched`, `already released`, `already in production`, `already in use`,
    `in production`, `we launched`, `we shipped`, `we released`, `our live`, `improve our`, `improving our`,
    `improvements to our`, `extend our`, `add to our`, `next release of`.
- **A problem can be stated:** the request or the user's answers give both a kind of person and a
  difficulty, cost or harm that person suffers. A drop in a number, a target or a feature does not.

When the user names a framework that this index does not list, say so in one sentence, name the five
frameworks it lists, and choose by rules 2 to 6.

When the user names `shortlist-ranking` and neither the request nor the conversation holds any candidate
idea, ask for the list when you may ask; when you may not, use `diverge-converge` and give the clause
"you named shortlist-ranking but gave no list, so I'm using diverge-converge instead".

## Telling the user

After choosing, and before step 3, tell the user in one sentence: "I'm using `name`, because clause."
Here `name` is the framework's name from the table below and `clause` is the clause of the rule that
matched, word for word:

| Rule | Clause |
|---|---|
| 1 | you named it |
| 2 | you gave candidate ideas to rank or choose among |
| 3 | you asked what to build first or what could make it fail |
| 4 | the product exists and the topic is improving it |
| 5 | no problem with an affected person and a hurt could be stated yet |
| 6 | no more specific rule matched |

## Frameworks

| framework | file | use when | avoid when |
|---|---|---|---|
| shortlist-ranking | [shortlist-ranking.md](shortlist-ranking.md) | The user has a shortlist or backlog of candidate ideas and wants them ranked, prioritised, chosen among or cut | The user has no list yet, or wants new ideas as well |
| risk-first-mvp | [risk-first-mvp.md](risk-first-mvp.md) | The request asks what to build first, for an MVP or a prototype, or what could make the idea fail | The user has a list to rank, or the product exists and the topic is improving it |
| improve-existing | [improve-existing.md](improve-existing.md) | The product exists and the topic is improving, extending or fixing it | The product does not exist yet, or the user has a list to rank |
| problem-reframing | [problem-reframing.md](problem-reframing.md) | After intake the topic is a symptom, a goal or a solution, and no problem can be stated with a person and a hurt | A problem can already be stated, or the user has a list to rank |
| diverge-converge | [diverge-converge.md](diverge-converge.md) | A new product, feature or problem space where options are wide open; the default | The user already has a fixed shortlist and only wants it ranked: use shortlist-ranking |

## Required sections

Every framework file has these sections, in this order. A file that lacks one is malformed:
use `diverge-converge` instead and tell the user which file was the problem.

1. When to use / When not to use
2. Steps
3. Questions to ask
4. Mapping to the BRN
5. Evaluation method text
6. Example

To add a framework, add its file here, one row to the Frameworks table and, when it should be chosen
without being named, one row to the selection rules. `SKILL.md` does not change.
