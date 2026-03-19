# Phase 05: Recommendation Generation (Strategic Mode Only)

**Purpose:** Generate actionable, prioritized recommendations with exact implementation details.
**Applies to:** Strategic mode only.

---

## Step 05.1: Load Recommendation Framework [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/references/recommendation-framework.md")
```

Use: Priority criteria, structure requirements, implementation details.

### VERIFY

- Reference file content is in context
- Priority decision tree visible

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.1
```

---

## Step 05.2: Load Recommendation Template [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/assets/recommendation-template.md")
```

### VERIFY

- Template structure visible with all mandatory subsections

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.2
```

---

## Step 05.3: Identify Solutions from Root Cause [MANDATORY]

### EXECUTE

From 5 Whys analysis:
```
root_cause = why_5.answer
contributing_factors = [why_4.answer, why_3.answer] (if significant)

FOR each cause (root + contributing):
    Identify solution that fixes cause:
        - Add missing validation
        - Fix broken logic
        - Update documentation
        - Create new component
        - Refactor existing component
        - Add enforcement mechanism
```

### VERIFY

- At least 1 solution identified for root cause
- Contributing factors assessed for separate solutions

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.3
```

---

## Step 05.4: Categorize Priority [MANDATORY]

### EXECUTE

Apply priority decision tree from recommendation-framework.md:

```
FOR each solution:
    Does fix prevent CRITICAL framework failure?
    +-- YES -> priority = CRITICAL
    +-- NO  -> Does fix prevent quality degradation?
                +-- YES -> priority = HIGH
                +-- NO  -> Does fix improve UX or quality?
                            +-- YES -> priority = MEDIUM
                            +-- NO  -> priority = LOW
```

### VERIFY

- Each solution has a priority assigned
- Priority assignments follow the decision tree logic

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.4
```

---

## Step 05.5: Specify Exact Implementation [MANDATORY]

### EXECUTE

```
FOR each solution:
    FROM evidence in Phase 04:
        Extract: exact_file_path
        Extract: exact_section (Phase X, Step Y, Lines Z-W)
        Identify: change_type (Add | Modify | Delete)

    IF change_type == "Add":
        Write: exact_text_to_add (copy-paste ready)
        Specify: insertion_point (after Step X)

    IF change_type == "Modify":
        Write: old_text (current incorrect text)
        Write: new_text (corrected text)

    IF change_type == "Delete":
        Specify: lines_to_remove
        Explain: why deletion fixes issue
```

### VERIFY

- Each solution has exact file paths (not placeholders)
- Each solution has copy-paste ready code or text
- Change type is specified for each

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.5
```

---

## Step 05.6: Write Rationale and Testing [MANDATORY]

### EXECUTE

**For each recommendation:**

**Rationale (4 parts):**
1. Why this solution? (mechanism of how it fixes the issue)
2. How does it prevent recurrence?
3. What evidence supports this? (reference Phase 04 evidence)
4. What are trade-offs? (if any)

**Testing Procedures (mandatory table format):**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Setup/precondition | Test scenario created |
| 2 | Execute action | Command/operation runs |
| 3 | Verify result | Expected outcome achieved |
| 4 | Edge case check | No regressions |

**Success Criteria (mandatory checkboxes):**
```
- [ ] {specific success criterion 1}
- [ ] {specific success criterion 2}
- [ ] {specific success criterion 3}
```

### VERIFY

- Each recommendation has 4-part rationale
- Each recommendation has test specification table
- Each recommendation has 3+ success criteria checkboxes

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.6
```

---

## Step 05.7: Estimate Effort and Impact [MANDATORY]

### EXECUTE

**Effort Estimation:**
```
FOR each recommendation:
    Calculate: base_effort = change_complexity + testing_time + documentation_time

    Complexity guide:
        Simple add: 15-30 min
        Complex add: 30-60 min
        Modify logic: 1-2 hours
        Refactor: 2-4 hours
        New component: 2-3 hours

    Add testing time: ~1 hour
    Add documentation time: ~30 min

    Format: **Time: {N} hours** (mandatory parseable format)
    Dependencies: List other recommendations needed first
```

**Impact Analysis:**
```
FOR each recommendation:
    Benefit: What improves? How much? Who benefits?
    Risk: What could go wrong? How to mitigate?
    Scope: Files affected count, workflows affected, users affected
```

### VERIFY

- Each recommendation has `**Time: {N} hours**` format
- Each recommendation has benefit/risk/scope analysis

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.7
```

---

## Step 05.8: Sort and Assign IDs [MANDATORY]

### EXECUTE

```
Group by priority: CRITICAL, HIGH, MEDIUM, LOW

Within each priority:
    Sort by dependencies (foundation first, dependent second)
    Then by effort (quick wins first)

Assign recommendation IDs: REC-1, REC-2, REC-3...
```

### VERIFY

- Recommendations sorted by priority then dependencies
- Each has unique REC-N identifier
- No ID gaps or duplicates

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.8
```

---

## Step 05.9: Per-Recommendation Validation [MANDATORY]

### EXECUTE

For EACH recommendation, validate mandatory subsections:

```
FOR each REC-N:
    [ ] Has "**Addresses:** Why #{N}" (evidence traceability)
    [ ] Has "**Conditional:**" marker (Unconditional or Conditional + condition)
    [ ] Has "#### Current Code Context" with 5-30 line excerpt
        (OR "N/A - documentation-only change")
    [ ] Has "#### Test Specification" with markdown table
    [ ] Has "**Time:** {N} hours" in Effort Estimate
    [ ] Has "#### Success Criteria" with at least 1 "- [ ]" checkbox
    [ ] Has "#### Architecture Constraints" with citation
        (IF modifies .rs files, OR "N/A - no Rust code changes")

IF any validation fails:
    HALT: "REC-{N} incomplete: {missing field}"
    Complete the missing field before proceeding
```

### VERIFY

- All recommendations pass per-recommendation validation
- No HALT conditions triggered (or all resolved)

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.9
```

---

## Step 05.10: Phase 05 Summary [MANDATORY]

### EXECUTE

```
PHASE 05 COMPLETE (RECOMMENDATIONS)
=====================================
Recommendations Generated: {total}
  - CRITICAL: {count}
  - HIGH: {count}
  - MEDIUM: {count}
  - LOW: {count}

All recommendations have:
  - Exact file paths
  - Specific sections
  - Copy-paste ready code/text
  - Evidence-based rationale
  - Testing procedures (table format)
  - Effort estimates (**Time:** format)
  - Success criteria (checkboxes)

Proceeding to Phase 06: RCA Document Creation...
```

### VERIFY

- Summary displayed with accurate counts

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=05 --step=05.10
```
