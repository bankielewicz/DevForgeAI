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
upstream: []           # brownfield: one informed_by record per document read; else usually empty
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: []
sources: []            # one "kind: reference" string per input used; kind is document | data | ticket | interview | url | note
---

# BRN-000 — <topic>

<!-- A brainstorm is divergent and non-binding. Nothing here is a commitment.
     Its job is to produce clearly identified problems (PRB-), ideas (IDEA-) and
     assumptions (ASM-) that a PRD can cite. Item blocks follow README §1.1:
     quote free text, never delete or renumber items.

     Brownfield-only parts sit between the comment lines "brownfield only: start" and
     "brownfield only: end". Greenfield: delete both lines and everything between them.
     Brownfield: keep what is between them and delete the two lines. Project kind not
     decided: do as for the kind the run worked with (references/intake.md). -->

## 1. Context

Project kind: <greenfield or brownfield>

<!-- The line above is the first line of this section. After "Project kind: " it holds exactly
     greenfield, brownfield or [NEEDS CLARIFICATION: greenfield or brownfield].
     Then a blank line, then the context prose: why are we brainstorming now? What triggered
     it (incident, request, metric, opportunity)? Which constraints apply? -->

<!-- brownfield only: start -->
### Existing product

<!-- One row per document read, in the order read. With none read, replace the table by the
     line: No document was found in the project.
     A document that was skipped gets a line after the table: Skipped: path (reason) -->

| Document | Version | What it already covers |
|---|---|---|
| PRD-001 | 1 | <its title (first requirement ID to last)> |
<!-- brownfield only: end -->

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "<one sentence, from the user's side>"
    who: "<persona>"
    evidence: "<fact (one sources entry), or a NEEDS CLARIFICATION marker>"
    severity: medium          # high | medium | low
```

## 3. Target users

<!-- Exactly this table and nothing else: one row per distinct who value of the active problems,
     in the order the values first appear, the Persona cell equal to that value character for
     character. An unknown cell holds a [NEEDS CLARIFICATION: ...] marker. -->

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
    value: null               # a quoted rating or number, per the framework named in section 5
    effort: null
    risk: null
    score: null
    disposition: open         # open | promoted | parked | rejected
    reason: null              # why promoted / parked / rejected
```

## 5. Evaluation method

<!-- The framework's evaluation method text, then any discussion that the numbers do not capture. -->

## 6. Convergence

<!-- What was promoted, parked and rejected and why, in prose. Dispositions live on the ideas.
     Before the user confirms: a paragraph starting "Proposed, awaiting confirmation:". -->

### First release cut

<!-- The status line is exactly "First release cut: proposed, not confirmed" or
     "First release cut: confirmed on YYYY-MM-DD". One row per idea that is promoted or proposed
     for promotion, in ID order; the second cell is yes or no; the Why cell is one of the fixed
     sentences of references/mvp-path.md. With no such idea, replace the table by the line:
     No idea is promoted or proposed for promotion. -->

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | <one of the fixed sentences> |

<!-- brownfield only: start -->
### Already covered

<!-- Suggestions kept out of the ideas because a document read already covers them.
     Covered by is DOCUMENT-ID#ITEM-ID. With no row, replace the table by the line: None. -->

| Suggestion | Covered by |
|---|---|
| <suggestion> | PRD-001#FR-001 |

### Previously decided

<!-- Ideas an earlier BRN rejected or parked, kept out of the ideas. Decision is rejected or
     parked; Where is BRN-NNN#IDEA-NN. With no row, replace the table by the line: None. -->

| Idea | Decision | Where |
|---|---|---|
| <idea> | rejected | BRN-001#IDEA-01 |

### Assumption updates

<!-- Change is "open to validated" or "open to invalidated". Evidence is a fact that ends with one
     sources entry in parentheses. Status is "proposed, not confirmed" or
     "confirmed on YYYY-MM-DD". With no row, replace the table by the line: None. -->

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | <fact (one sources entry)> | proposed, not confirmed |
<!-- brownfield only: end -->

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

<!-- One row per active assumption whose state is open, ranks 1 to n with no gap. If wrong starts
     with Fatal, Serious or Minor; Confidence is high, medium or low; Cheapest test starts with Data,
     Prototype or Interview (references/mvp-path.md gives each cell). With none: the line None. -->

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | <if wrong: Fatal, Serious or Minor, then what fails> | low | <cheapest test: Data, Prototype or Interview, then the test> |

- [NEEDS CLARIFICATION: <question>]

## 8. Candidate success signals

<!-- One bullet per first-release idea (a yes row of the First release cut), in ID order.
     Rough outcome indicators: the PRD turns these into success metrics (SM-). They are not
     acceptance criteria. With no first-release idea, the section holds the line: - None. -->

- IDEA-01: <observable outcome>; baseline <value (one sources entry), or a NEEDS CLARIFICATION marker>

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | YYYY-MM-DD | | Initial draft |
