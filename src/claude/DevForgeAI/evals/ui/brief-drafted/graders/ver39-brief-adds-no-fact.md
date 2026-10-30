---
type: llm
weight: 0.5
---

The agent was asked to design the UI for a brainstorm (BRN-001, Shiftlog: record shifts) in a session with no Artifact tool, so it
could only draft briefs for Claude Design. Each brief has a lead line, then Context, Content, Must-haves, Style and a closing line;
labels may be bold, plain or followed by a colon, and a brief may sit in a code block.
Judge ONLY the text after "Context:" and after "Content:" in each brief, each up to the next label. The lead line, the Must-haves,
the Style, the closing line and the rest of the reply are judged by other graders.
PASS when no Context and no Content states a fact about the product, its users, their work or their problem that the brainstorm
below does not state or directly imply. Paraphrase is fine; so is restating in plain words what an idea lets the user do, naming
the screens the promoted ideas name (List, Add, Report), the surface an idea implies (IDEA-01 and IDEA-02 are a terminal tool;
IDEA-03 and IDEA-06 a web page), and states those ideas could show (none recorded yet; some recorded; a week with or without shifts).
Quoted wording must be the brainstorm's own words.
FAIL when any Context or Content adds such a fact (a figure, a name, a device, a habit, a feature, a field, a cause, a number of
users, a place). When you answer FAIL, write FAIL followed by a colon and the added fact, quoted from the brief.

The brainstorm, in full (everything a brief may rest on):

# BRN-001 — Shiftlog: record shifts

## 1. Context

Shift workers record when they start and stop work, and want to see the hours they worked each week.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Workers lose track of the hours they worked each week"
    who: "Shift worker"
    evidence: "Interview notes"
    severity: high
```

## 3. Target users

Shift workers.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Add a shift from the terminal"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Decided with the owner"
  - id: IDEA-02
    status: active
    idea: "List shifts in a table"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Decided with the owner"
  - id: IDEA-03
    status: active
    idea: "A weekly report page"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Decided with the owner"
  - id: IDEA-04
    status: active
    idea: "Export shifts as CSV"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Decided with the owner"
  - id: IDEA-05
    status: active
    idea: "Sync to a server"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: parked
    reason: "Decided with the owner"
  - id: IDEA-06
    status: active
    idea: "A dark theme for the report page"
    addresses: ["PRB-01"]
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Decided with the owner"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the owner.

## 6. Convergence

The owner decided each idea's disposition.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that workers will record shifts every day."
    validation: "Shifts recorded each week"
    state: open
```

- None.

## 8. Candidate success signals

- The hours worked each week are right.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-10-02 | claude-code (session 00000000-0000-0000-0000-000000000000) | Converged |
