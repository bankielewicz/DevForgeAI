---
id: BRN-000
type: brainstorm
title: ""
status: draft          # draft | converged | archived
version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: ""
authors: []
generated_by:
  tool: ""
  model: ""
  session: ""
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []           # usually empty; use relation: informed_by for research, interviews, tickets and, in a brownfield BRN, each document read
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: []
sources: []            # one quoted string per input used, "<kind>: <reference>"; kind is document, data, ticket, interview, url or note
---

# BRN-000 — <topic>

<!-- A brainstorm is divergent and non-binding. Nothing here is a commitment.
     Its job is to produce clearly identified problems (PRB-), ideas (IDEA-) and
     assumptions (ASM-) that a PRD can cite. Item blocks follow README §1.1:
     quote free text, never delete or renumber items.

     Fixed shapes: the shapes in this template (the Project kind line, the tables and the bullets) are
     written exactly as shown. Their rules are in references/intake.md and, for a brownfield BRN,
     references/brownfield.md. Replace every <placeholder> with content or with a
     [NEEDS CLARIFICATION: ...] marker, and delete every comment.

     Brownfield parts: a region between a marker line that reads BROWNFIELD START and one that reads
     BROWNFIELD END (each is an HTML comment on a line of its own) is for a brownfield BRN only. When the
     project kind is brownfield, or unresolved and assumed brownfield, delete the two marker lines and keep
     the region between them. Otherwise delete the whole region, both marker lines included. -->

## 1. Context

<!-- The first line is the project kind, exactly one of these three lines, then a blank line, then the prose:
     Project kind: greenfield
     Project kind: brownfield
     Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]
     Prose: why are we brainstorming now? What triggered it (incident, request, metric, opportunity)?
     Name the source of every number you state, as a sources entry. -->

Project kind: <greenfield, brownfield or the NEEDS CLARIFICATION line>

<context prose>

<!-- BROWNFIELD START -->

### Existing product

<!-- One row per document read, in the order PRD, BRN, ARCH, EPIC, ADR and the highest number first within a
     kind. Version is the document's version. If no document was found, replace the table with the line
     No document was found in the project. -->

| Document | Version | What it already covers |
|---|---|---|
| PRD-000 | 1 | <title> (FR-001 to FR-003; NFR-001) |

<!-- BROWNFIELD END -->

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "<one sentence, from the user's side>"
    who: "<persona>"
    evidence: "<one entry of sources, or a short claim followed by that entry in parentheses>"
    severity: medium          # high | medium | low
```

## 3. Target users

<!-- Exactly this table: one row per distinct who value of the active problems, in the order the values first
     appear in section 2. The Persona cell is that value, character for character. A cell the user did not
     answer holds a [NEEDS CLARIFICATION: ...] marker, never a guess. No prose in this section. -->

| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| <persona> | <job to be done> | <current workaround> | <pain> |

## 4. Ideas

<!-- Capture every idea first with disposition: open. Fill value/effort/risk/score
     during evaluation (section 5), then set disposition at convergence (section 6).
     Do not record which PRD picked an idea up; that view is GENERATED. -->

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "<idea>"
    addresses:
      - PRB-01
    value: null               # e.g. "high", or a number, per the method in section 5
    effort: null
    risk: null
    score: null
    disposition: open         # open | promoted | parked | rejected
    reason: null              # why promoted / parked / rejected
```

## 5. Evaluation method

<!-- Name the lens used to fill value/effort/risk/score: impact/effort, RICE, MoSCoW,
     or dot-voting. Add any discussion that the numbers do not capture. -->

## 6. Convergence

<!-- Summary of what was promoted and why, in prose. Dispositions live on the ideas. Before the user confirms,
     write the paragraph that starts Proposed, awaiting confirmation: and say nothing is decided. -->

### First release cut

<!-- The first line is First release cut: proposed, not confirmed, or, after the user confirms,
     First release cut: confirmed by NAME on the date. One row per idea that is promoted or proposed for
     promotion, in ID order; the second column is yes or no. With no such idea, replace the table with the
     line No idea is promoted or proposed for promotion. -->

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | <yes or no> | <why> |

<!-- BROWNFIELD START -->

### Already covered

<!-- A suggestion (the user's or yours) that restates an active PRD requirement and adds nothing to it. One
     row each, in the order raised. Covered by is the requirement written PRD-001#FR-003; several are
     separated by a comma and a space. With no row, replace the table with the line None. -->

| Suggestion | Covered by |
|---|---|
| <suggestion in at most 12 words> | PRD-000#FR-001 |

### Previously decided

<!-- An idea of an earlier BRN that was rejected or parked and that this run did not take up. Decision is
     rejected or parked. Where is the earlier idea written BRN-001#IDEA-06. Rows go in the order of Where.
     With no row, replace the table with the line None. -->

| Idea | Decision | Where |
|---|---|---|
| <idea in at most 12 words> | rejected | BRN-000#IDEA-01 |

### Assumption updates

<!-- A new state proposed for an assumption of an earlier BRN. Change is open to validated or open to
     invalidated. Evidence quotes one entry of sources. Status is proposed, not confirmed, or, after the user
     confirms, confirmed by NAME on the date. Rows go in the order of Earlier assumption. With no row,
     replace the table with the line None. Never edit the earlier BRN for this. -->

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-000#ASM-01 | open to validated | <fact, with the sources entry in parentheses> | proposed, not confirmed |

<!-- BROWNFIELD END -->

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "<we believe that…>"
    validation: "<experiment, interview or data that would confirm it>"
    state: open               # open | validated | invalidated
```

### Assumption risk ranking

<!-- One row per active assumption whose state is open, rank 1 the riskiest. Confidence is high, medium or
     low. With no such assumption, replace the table with the line None. -->

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | <what breaks if it is wrong> | <high, medium or low> | <cheapest test> |

- [NEEDS CLARIFICATION: <question>]

## 8. Candidate success signals

<!-- Rough outcome indicators. The PRD turns these into success metrics (SM-).
     They are not acceptance criteria. One bullet per first-release idea, in ID order, in exactly this
     shape: the idea ID, a colon, what a person could observe change if the idea works, a semicolon,
     the word baseline and the current value with its source (a sources entry) or a
     [NEEDS CLARIFICATION: ...] marker. State no target number. With no first-release idea, the section
     holds the single line - None. -->

- <idea ID>: <observable outcome>; baseline <current value with its source>

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | YYYY-MM-DD | | Initial draft |
