# Phase 02: Investigation

**Purpose:** Cross-reference failure against constitutional context files, trace code-level causation, and (strategic mode) perform 5 Whys analysis.
**Applies to:** Both tactical and strategic modes.
**Required Subagent:** diagnostic-analyst

**HALT: NO FIX ATTEMPTS UNTIL THIS PHASE COMPLETES.** Any code changes targeting production or test files are FORBIDDEN until the investigation report is produced. Violation constitutes shotgun debugging and invalidates the diagnosis.

---

## Step 02.1: Load Investigation Reference [MANDATORY]

### EXECUTE

**Tactical Mode:**
```
Read(file_path=".claude/skills/spec-driven-rca/references/investigation-patterns.md")
```
Use the 6 failure category taxonomy to guide investigation.

**Strategic Mode:**
```
Read(file_path=".claude/skills/spec-driven-rca/references/5-whys-methodology.md")
```
Use the "How to Ask Effective Why Questions" section.

### VERIFY

- Reference file content is in context
- Tactical: 6 failure categories visible
- Strategic: 5 Whys methodology guidance visible

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.1
```

---

## Step 02.2: Invoke Diagnostic-Analyst Subagent [MANDATORY]

### EXECUTE

This step is MANDATORY for BOTH modes. The diagnostic-analyst runs in isolated read-only context, checking all 6 constitutional context files for spec drift and constraint violations.

```
Task(
    subagent_type="diagnostic-analyst",
    description="Investigate failure against constitutional context files",
    prompt="Analyze failure artifacts for spec drift and constraint violations.

    Error/Issue: {error_message OR issue_description}
    File: {failing_file OR primary_file}
    Phase: {workflow_phase OR 'RCA'}

    Check all 6 context files:
    1. devforgeai/specs/context/tech-stack.md - unapproved technology?
    2. devforgeai/specs/context/source-tree.md - file in wrong location?
    3. devforgeai/specs/context/dependencies.md - wrong version?
    4. devforgeai/specs/context/coding-standards.md - naming/pattern violation?
    5. devforgeai/specs/context/architecture-constraints.md - layer boundary violation?
    6. devforgeai/specs/context/anti-patterns.md - forbidden pattern detected?

    Return structured diagnosis with:
    - spec_compliance: PASS or FAIL with details per file
    - code_trace: root_location, call_chain, data_flow
    - contributing_factors: list of secondary issues
    - hypotheses: ranked by confidence (0.0-1.0)"
)
```

Store diagnostic-analyst output as `subagent_diagnosis`.

### VERIFY

- Task() invocation completed (subagent returned results)
- subagent_diagnosis contains spec_compliance assessment
- subagent_diagnosis contains at least one finding or "all clear"

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.2
```

---

## Step 02.3: Code-Level Tracing [MANDATORY]

### EXECUTE

**Tactical Mode — Trace the failure through code:**

1. **Read the failing test** — Understand what behavior is expected
```
Read(file_path="{test_file}")
```

2. **Read the implementation** — Understand what behavior is produced
```
Read(file_path="{implementation_file}")
```

3. **Trace the gap** — Identify where expected diverges from actual

4. **Check imports/dependencies** — Verify all imports resolve
```
Grep(pattern="import|from|require", path="{failing_file}", output_mode="content")
```

5. **Check data flow** — Trace input through transformations to output

**Strategic Mode — Trace the framework issue:**

1. **Read the primary component** (already done in Phase 01)
2. **Read its integration points** — How is this component invoked?
3. **Trace the workflow** — What was the expected vs actual execution path?
4. **Check for pattern compliance** — Does the component follow documented patterns?
5. **Check for missing validation** — Where should a check have caught this?

### VERIFY

- At least 2 files read during tracing
- Gap between expected and actual behavior identified
- Root location narrowed to specific file and area

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.3
```

---

## Step 02.4: Investigation Report (Tactical Mode) [CONDITIONAL]

### EXECUTE

**Condition:** Tactical mode only. Strategic mode skips to Step 02.5.

Produce structured investigation report:

```
INVESTIGATION REPORT
====================
Spec Compliance: {PASS | FAIL with details from diagnostic-analyst}
Context Violations: {list of violated context files, or "None"}
Code Trace:
    Expected: {what the test expects}
    Actual: {what the implementation produces}
    Gap: {where they diverge}
Root Location: {file:line where root cause exists}
Contributing Factors: {list of secondary issues}
```

This report is the input for Phase 03 (Prescription).

### VERIFY

- Report contains all fields (Spec Compliance, Context Violations, Code Trace, Root Location, Contributing Factors)
- Root Location is specific (not vague "somewhere in the code")

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.4
```

---

## Step 02.5: Load 5 Whys Template (Strategic Mode) [CONDITIONAL]

### EXECUTE

**Condition:** Strategic mode only. Tactical mode already completed this phase at Step 02.4.

```
Read(file_path=".claude/skills/spec-driven-rca/assets/5-whys-template.md")
```

### VERIFY

- Template structure visible in context
- Contains Why #1 through Why #5 sections

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.5
```

---

## Step 02.6: Perform 5 Whys Analysis (Strategic Mode) [CONDITIONAL]

### EXECUTE

**Condition:** Strategic mode only.

Perform 5 successive "why" questions, each building on the previous answer. Each why must have evidence from files examined.

**Why #1 (Surface Level):**
```
Question: "Why did {issue from ISSUE_DESCRIPTION} happen?"
Answer: {Immediate cause based on evidence from Phase 01}
Evidence: {File path}:{line range} - {quote showing immediate cause}
```

**Why #2 (First Layer Deeper):**
```
Question: "Why did {answer from Why #1} occur?"
Answer: {Deeper cause — what allowed the trigger}
Evidence: {File path}:{line range} - {quote showing deeper cause}
```

**Why #3 (Second Layer Deeper):**
```
Question: "Why did {answer from Why #2} occur?"
Answer: {What assumption or design decision led to this}
Evidence: {File path}:{line range} - {quote showing assumption}
```

**Why #4 (Third Layer Deeper):**
```
Question: "Why did {answer from Why #3} occur?"
Answer: {Process gap that allowed this}
Evidence: {File path}:{line range} - {quote showing process gap}
```

**Why #5 (ROOT CAUSE):**
```
Question: "Why did {answer from Why #4} occur?"
Answer: **ROOT CAUSE:** {Fundamental underlying issue}
Evidence: {File path}:{line range} - {quote showing root cause}
```

### VERIFY

- All 5 Whys answered with evidence references
- Each "why" builds logically on the previous answer
- Why #5 is marked as ROOT CAUSE

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.6
```

---

## Step 02.7: Validate Root Cause (Strategic Mode) [CONDITIONAL]

### EXECUTE

**Condition:** Strategic mode only.

Apply 4 validation criteria from 5-whys-methodology.md:

**Q1: Would fixing this prevent recurrence?**
- Search evidence for proof that fix would work
- Check similar patterns in related RCAs

**Q2: Does this explain all symptoms?**
- Review issue description symptoms
- Verify root cause explains each symptom

**Q3: Is this within framework control?**
- Not external dependency
- Not user error beyond framework scope
- Framework can fix this

**Q4: Is this evidence-based?**
- Not assumption or speculation
- Backed by file examination
- Provable from evidence collected

IF any validation fails:
```
HALT Phase 02

Display:
"Root cause validation failed:
- {Which validation question failed}
- {Why it failed}

Reconsidering Why #5..."

Revise why_5 with stronger evidence or different root cause
Re-validate
```

### VERIFY

- All 4 validation questions answered YES
- Root cause is specific, actionable, and evidence-based
- If revision occurred, revised root cause passes all 4 checks

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.7
```

---

## Step 02.8: Phase 02 Summary [MANDATORY]

### EXECUTE

**Tactical Mode:**
```
PHASE 02 COMPLETE (TACTICAL)
=============================
Spec Compliance: {PASS/FAIL}
Context Violations: {count or "None"}
Root Location: {file:line}
Contributing Factors: {count}

Proceeding to Phase 03: Prescription...
```

**Strategic Mode:**
```
PHASE 02 COMPLETE (STRATEGIC)
==============================
Spec Compliance: {PASS/FAIL}
5 Whys Analysis:
  Why #1: {answer summary}
  Why #2: {answer summary}
  Why #3: {answer summary}
  Why #4: {answer summary}
  Why #5 (ROOT CAUSE): {root cause summary}

Root Cause Validated:
  - Prevents recurrence? YES
  - Explains all symptoms? YES
  - Within framework control? YES
  - Evidence-based? YES

Proceeding to Phase 04: Evidence Organization...
```

### VERIFY

- Summary displayed to user
- Correct next phase identified based on mode

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=02 --step=02.8
```
