# Phase 08: Architecture Review

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Independent architecture review of all context files for soundness, coherence, completeness, and practicality |
| **REFERENCES** | `.claude/skills/spec-driven-architecture/references/architecture-review-workflow.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] architect-reviewer subagent invoked and returned structured findings
- [ ] All HIGH findings resolved (accepted, rejected with justification, or deferred to story)
- [ ] All MEDIUM findings presented and user decisions recorded
- [ ] Approved changes applied and re-validated (single round, no loop)
**IF any criterion is unmet: HALT. Do NOT proceed to the next phase.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-architecture/references/architecture-review-workflow.md")
```

Do NOT rely on memory of previous reads. Load fresh every time.

---

## Mandatory Steps

### Step 8.1: Invoke architect-reviewer Subagent

**EXECUTE:**
```
Task(
  subagent_type="architect-reviewer",
  prompt="Review all 6 context files in devforgeai/specs/context/ for architectural quality.

    Files to review:
    - tech-stack.md
    - source-tree.md
    - dependencies.md
    - coding-standards.md
    - architecture-constraints.md
    - anti-patterns.md

    Evaluate against 5 criteria:
    1. SOUNDNESS — Do the architectural patterns support the stated requirements?
       Check: patterns in architecture-constraints.md are appropriate for the tech stack
    2. COHERENCE — Do all technology choices work well together?
       Check: no conflicting frameworks, compatible versions, sensible pairings
    3. COMPLETENESS — Are there gaps in the architecture?
       Check: every layer has defined constraints, every dependency has a purpose
    4. CONSISTENCY — Are there contradictions between files?
       Check: pairwise comparison of all 6 files for conflicting statements
    5. PRACTICALITY — Is this realistic for the team and project scope?
       Check: complexity appropriate, no over-engineering, achievable constraints

    Return structured JSON:
    {
      findings: [{
        criterion: 'SOUNDNESS' | 'COHERENCE' | 'COMPLETENESS' | 'CONSISTENCY' | 'PRACTICALITY',
        severity: 'HIGH' | 'MEDIUM' | 'LOW',
        file: '<affected context file>',
        line_range: '<start>-<end>',
        description: '<what was found>',
        recommendation: '<specific action to take>',
        evidence: '<quoted text supporting the finding>'
      }]
    }"
)
```
This is a BLOCKING task. Wait for result before proceeding.

**VERIFY:**
- Task returned a result (not error, not timeout)
- Result contains a `findings` array
- Each finding has all required fields: criterion, severity, file, description, recommendation
- Findings are sorted by severity (HIGH first)

**RECORD:**
```json
checkpoint.phase_08.step_8_1 = {
  "subagent_invoked": true,
  "subagent_result_received": true,
  "findings_by_severity": { "HIGH": <n>, "MEDIUM": <n>, "LOW": <n> },
  "findings_by_criterion": {
    "SOUNDNESS": <n>, "COHERENCE": <n>, "COMPLETENESS": <n>,
    "CONSISTENCY": <n>, "PRACTICALITY": <n>
  },
  "raw_findings": [ ... ]
}
```

---

### Step 8.2: Present Review Findings

**EXECUTE:**

**HIGH-severity findings (BLOCKING):**
For each HIGH finding, present individually:
```
AskUserQuestion(
  question="HIGH architecture finding [<criterion>]:\n\n  File: <file> (lines <line_range>)\n  Issue: <description>\n  Evidence: '<evidence>'\n  Recommendation: <recommendation>\n\nHow should this be handled?",
  options=[
    { "label": "Accept recommendation", "description": "Apply the suggested change to <file>" },
    { "label": "Reject with justification", "description": "Keep current architecture — provide reason" },
    { "label": "Defer to story", "description": "Create a future story to address this finding" }
  ]
)
```

**MEDIUM-severity findings (NON-BLOCKING):**
Present as a batch after all HIGHs are resolved:
```
AskUserQuestion(
  question="MEDIUM architecture findings:\n\n<numbered list of findings with file, criterion, description>\n\nSelect findings to address now (others will be logged).",
  options=[
    { "label": "Address all", "description": "Apply all <N> recommendations" },
    { "label": "Select individually", "description": "Choose which to address" },
    { "label": "Log all for later", "description": "Record findings but take no action now" }
  ]
)
```

**LOW-severity findings:**
Log without user interaction. Include in final report.

**VERIFY:**
- Every HIGH finding has a user decision (accept, reject, or defer)
- Rejected HIGHs have justification text (non-empty)
- MEDIUM finding batch presented and user responded
- All decisions recorded

**RECORD:**
```json
checkpoint.phase_08.step_8_2 = {
  "high_findings": {
    "total": <n>,
    "accepted": <n>,
    "rejected": <n>,
    "deferred": <n>,
    "rejections": [{ "finding": "<desc>", "justification": "<reason>" }],
    "deferrals": [{ "finding": "<desc>", "story_note": "<text>" }]
  },
  "medium_findings": {
    "total": <n>,
    "addressed": <n>,
    "logged": <n>
  },
  "low_findings_logged": <n>
}
```

---

### Step 8.3: Apply Approved Changes

**EXECUTE:**

For each accepted HIGH recommendation and each addressed MEDIUM recommendation:
1. Read the target context file:
   ```
   Read(file_path="devforgeai/specs/context/<file>")
   ```
2. Apply the change:
   ```
   Edit(
     file_path="devforgeai/specs/context/<file>",
     old_string="<current content>",
     new_string="<updated content per recommendation>"
   )
   ```
3. If the change is significant (alters architectural constraints, modifies technology choices, or changes dependency rules):
   ```
   Write(
     file_path="devforgeai/specs/adrs/ADR-<NNN>-architecture-review-<topic>.md",
     content=<ADR documenting: context, decision, rationale, consequences>
   )
   ```

After ALL edits applied, re-validate changed files (SINGLE ROUND — do NOT loop):
- Read each modified file
- Verify the edit was applied correctly (new content present, old content absent)
- Check that the edit did not introduce new contradictions with adjacent content
- If re-validation finds a new issue: log it as a finding for future work, do NOT re-enter the edit cycle

**VERIFY:**
- Every accepted recommendation has a corresponding Edit applied
- Every significant change has an ADR created
- Re-validation completed (single round only)
- No edit errors (all Edit calls returned successfully)

**RECORD:**
```json
checkpoint.phase_08.step_8_3 = {
  "edits_applied": <count>,
  "edits_successful": <count>,
  "edits_failed": <count>,
  "adrs_created": [{ "path": "devforgeai/specs/adrs/ADR-<NNN>-...", "topic": "<summary>" }],
  "revalidation_passed": <boolean>,
  "revalidation_new_issues": <count>,
  "phase_complete": true
}
```

---

## Phase Transition Display

```
============================================================
  PHASE 08 COMPLETE: Architecture Review
============================================================
  Findings:    <H> HIGH, <M> MEDIUM, <L> LOW
  Accepted:    <N> recommendations applied
  Rejected:    <N> with justification
  Deferred:    <N> to future stories
  ADRs created: <N>
  Re-validation: [PASS/ISSUES LOGGED]
------------------------------------------------------------
  Architecture specification complete.
============================================================
```
