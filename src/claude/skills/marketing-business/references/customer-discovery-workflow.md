---
name: customer-discovery-workflow
description: Customer discovery workflow reference for interview loading, synthesis, and milestone tracking with EPIC-074 integration
story: STORY-542
epic: EPIC-075
---

# Customer Discovery Workflow

Reference for the customer discovery skill. Guides interview loading, synthesis, and milestone tracking integrated with EPIC-074 market research outputs.

---

## Phase 1: Load Interview Questions from EPIC-074

Load interview questions from EPIC-074 market research outputs. Import the structured question sets generated during market research.

Check for EPIC-074 output files at the expected path. If files exist, load and parse the interview question sets organized by theme.

### Question Themes

Organize interview questions into 3 themes:

1. **Problem Validation** — Questions that validate whether the target customer actually experiences the problem your product solves.
2. **Solution Fit** — Questions that assess whether your proposed solution addresses the customer's needs effectively.
3. **Pricing** — Questions that explore willingness to pay, budget constraints, and perceived value.

### Customer Segments

Prompt the user to define target customer segments for interview outreach.

- Require at least 3 customer segments to ensure adequate coverage.
- Enforce a maximum of 10 customer segments to maintain focus (BR-004).
- Each segment must have a clear description and target interview count.

---

## Phase 2: Fallback Interview Templates (BR-001)

When EPIC-074 outputs are unavailable, apply graceful degradation. Do not HALT. Instead, proceed with default fallback templates.

Display warning message:

> Market research outputs not found

Continue the workflow using 5 fallback topics as default templates:

1. **Core Problem** — What is the biggest challenge you face in [domain]?
2. **Current Solutions** — How do you currently solve this problem?
3. **Pain Points** — What frustrates you about existing solutions?
4. **Ideal Outcome** — What would a perfect solution look like?
5. **Budget and Priority** — How much do you spend on this problem today?

Graceful degradation: workflow proceeds without blocking on missing EPIC-074 data.

---

## Phase 3: Conduct Interviews and Record Feedback

Guide the user through conducting interviews and recording structured feedback for each session.

### Interview Recording Fields

For each interview, capture:

- Interviewee name/identifier and customer segment
- Date conducted (YYYY-MM-DD format)
- Responses organized by theme (problem validation, solution fit, pricing)
- Key quotes and observations
- Assumptions validated or invalidated

---

## Phase 4: Feedback Synthesis

Synthesize interview feedback into 4 categories:

1. **Validated Assumptions** — Assumptions confirmed by interview evidence across multiple segments.
2. **Invalidated Assumptions** — Assumptions disproven or contradicted by interview data.
3. **Recurring Pain Points** — Problems mentioned independently by multiple interviewees.
4. **Surprising Insights** — Unexpected findings not anticipated in the original hypothesis.

### Minimum Interview Requirement (BR-002)

At least 1 interview must be conducted before synthesis can proceed. Zero interviews cannot block the workflow silently — if no interviews have been conducted, the workflow must prevent synthesis and redirect the user back to outreach planning.

When zero interviews are detected, return to the outreach phase and display a message explaining that at minimum 1 interview is required before synthesis.

### Business Plan Integration

Write the synthesis summary to the business plan document. Append the results under the Customer Discovery milestone section. Add the following structured data:

- Summary of validated assumptions
- Summary of invalidated assumptions
- Key recurring pain points
- Notable surprising insights
- Recommended next steps

---

## Phase 5: Milestone Tracking

Write a Customer Discovery milestone entry to the business plan.

### Milestone Fields

Each milestone entry contains:

| Field | Format | Description |
|-------|--------|-------------|
| Completion Date | YYYY-MM-DD | Date the discovery round completed |
| Interviews Conducted | Integer count | Number of interviews conducted |
| Top 3 Validated Assumptions | Ranked list | Three highest-confidence validated assumptions |
| Top 3 Invalidated Assumptions | Ranked list | Three most significant invalidated assumptions |
| Confidence Score | Percentage (%) | Overall discovery confidence score |

### Confidence Score Calculation

Calculate the confidence score from the validated/total ratio:

```
confidence = (validated_count / total_assumptions_tested) * 100
```

Result: confidence percentage between 0% and 100% based on validated/total ratio.

### Duplicate Milestone Detection (BR-003)

Before writing, check if a Customer Discovery milestone already exists in the business plan. If a duplicate milestone is detected, prompt the user to choose one of 3 options:

1. **Append** — Add the new milestone alongside the existing one (preserves history).
2. **Replace** — Overwrite the existing milestone with new data.
3. **Cancel** — Abort the milestone write operation.

Never silently overwrite an existing milestone. Always ask the user to choose their preferred action.

---

## Phase 6: Partial Progress Persistence

### State File Management

Save workflow progress to a discovery-state file after each phase completes. On exit or partial completion, save the current state so progress is not lost.

State file location: `tmp/{story-id}/discovery-state.json`

### State Detection on Re-invocation

When the workflow is invoked, check if an existing discovery-state file exists. Detect partial progress by reading the state file and determining which phases have been completed.

If a partial state is detected, offer the user two options:

1. **Resume** — Continue from the last completed step.
2. **Restart** — Start over with a fresh workflow from the beginning.

### Corrupted State Handling (NFR-001)

If the discovery-state file is corrupt (malformed JSON, missing required fields), log a warning message indicating the corruption was detected. Fall back to a clean fresh start rather than crashing. The warning should inform the user that their previous progress could not be recovered.
