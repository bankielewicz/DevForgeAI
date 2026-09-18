# Phase 3.3: Self-Validation Workflow

Execute comprehensive validation checks on generated requirements.md with self-healing for correctable issues.

---

## Table of Contents

- [Overview](#overview)
- [Validation Strategy](#validation-strategy)
- [Load Validation Checklists](#load-validation-checklists)
- [Validation Sequence](#validation-sequence)
  - [Step 1: Verify Artifact Creation](#step-1-verify-artifact-creation)
  - [Step 2: Validate F4 Schema Compliance](#step-2-validate-f4-schema-compliance)
  - [Step 3: Validate Requirements Content Quality](#step-3-validate-requirements-content-quality)
  - [Step 4: Validate Handoff Readiness](#step-4-validate-handoff-readiness)
- [Validation Success Criteria](#validation-success-criteria)
- [Output from Step 3.3](#output-from-step-33)
- [References Used in Phase 3.3](#references-used-in-phase-33)
- [Success Criteria](#success-criteria)

---

## Overview

Phase 3.3 validates the requirements.md artifact meets DevForgeAI quality standards and F4 schema compliance before presenting to user. This phase includes automatic correction of common issues and halts on critical failures requiring user intervention.

**Duration:** 2-5 minutes
**Output:** Validation status, auto-corrected issues list, remaining issues for user resolution

---

## Validation Strategy

**Three-tier validation approach:**

1. **Auto-correctable issues** - Fix automatically, report what was fixed
2. **User-resolvable issues** - Report to user with remediation guidance, continue
3. **Critical failures** - HALT workflow, require user intervention before proceeding

**Key principle:** Self-healing improves UX by fixing obvious issues automatically (unlike ui-generator Phase 7 which requires user resolution for all issues).

---

## Load Validation Checklists

<!-- validation-checklists.md is loaded directly by SKILL.md Phase 3.3 (STORY-453) -->

This reference provides comprehensive validation logic for:
- Artifact creation verification (requirements.md)
- Requirements content quality standards
- F4 schema compliance validation
- Handoff readiness criteria

**See validation-checklists.md for complete validation procedures.**

---

## Validation Sequence

### Step 1: Verify Artifact Creation

**Check requirements.md exists:**

```
req_files = Glob(pattern="devforgeai/specs/requirements/*.md")

if len(req_files) == 0:
    # CRITICAL failure
    ERROR: No requirements.md created

    Self-healing attempt:
    1. Regenerate requirements.md from Phase 2 data
    2. Retry validation

    If still failing after 1 retry:
        HALT: Report to user - "Requirements generation failed. Manual intervention required."
```

---

### Step 2: Validate F4 Schema Compliance

**Validate requirements.md follows F4 schema structure:**

```
req_file = req_files[0]
Read(file_path=req_file)

# F4 Schema Required Fields
F4_REQUIRED_FIELDS = [
    "functional_requirements",
    "non_functional_requirements",
    "constraints",
    "dependencies"
]

# Check YAML structure
for field in F4_REQUIRED_FIELDS:
    if field not in req_content:
        missing_fields.append(field)

if len(missing_fields) > 0:
    # CRITICAL failure
    CRITICAL: F4 schema compliance failed - missing fields: {missing_fields}

    # Determine remediation path
    if len(missing_fields) <= 2:
        # Self-heal: Add empty field structures
        for field in missing_fields:
            add_empty_field(req_file, field)
        auto_corrected.append(f"Added empty fields: {missing_fields}")
    else:
        # Too many missing - cannot self-heal
        HALT: Requirements.md missing critical F4 fields
        Recommend: Regenerate using /ideate command
```

#### Validate YAML Structure

```
# Check for valid YAML syntax
try:
    yaml.safe_load(req_content)
except YAMLError as e:
    CRITICAL: Invalid YAML syntax in requirements.md
    HALT: Fix YAML syntax errors before proceeding
```

---

### Step 3: Validate Requirements Content Quality

**Validate requirements.md content:**

```
req_file = req_files[0]
Read(file_path=req_file)

Validate structure:
- [ ] functional_requirements has at least 5 items
- [ ] non_functional_requirements quantified (no vague "fast", "scalable")
- [ ] constraints section present
- [ ] dependencies section present

# Check for vague NFRs
vague_terms = Grep(pattern="fast|slow|scalable|secure|reliable", path=req_file, output_mode="count")

if vague_terms > 0:
    # MEDIUM issue (user-resolvable, not critical)
    WARNING: Requirements contains {vague_terms} vague NFR terms
    Recommend: Quantify NFRs before creating epics
    # Continue (not HALT-worthy)

# Check for placeholder content
placeholders = Grep(pattern="TODO|TBD|FIXME|\[.*\]", path=req_file, output_mode="count")

if placeholders > 5:
    # HIGH issue
    WARNING: Requirements has {placeholders} placeholders
    Recommend: Complete requirements before proceeding to epic creation
    # Continue (will be caught in architecture phase)
```

---

### Step 4: Validate Handoff Readiness

**Final checklist before completion:**

```
- [ ] requirements.md created and validated
- [ ] F4 schema compliance verified (functional_requirements, non_functional_requirements, constraints, dependencies)
- [ ] No critical ambiguities remain (all resolved via AskUserQuestion)
- [ ] All assumptions documented with validation flags
```

**If all validations pass:**

```
✅ Validation complete - All quality checks passed

Auto-corrected issues ({count}):
{list of auto-corrected issues}

→ Proceed to Phase 3.4 (Completion Summary)
```

**If validation fails after self-healing:**

```
⚠️ Validation issues detected

Auto-corrected ({auto_count}):
{list of auto-corrected issues}

Remaining issues ({remaining_count}):
{list with severity and remediation guidance}

CRITICAL issues: {count}
HIGH issues: {count}
MEDIUM issues: {count}

Action required:
- CRITICAL: Fix before proceeding
- HIGH: Strongly recommend fixing
- MEDIUM: Can defer to epic creation phase

→ Fix issues or proceed with warnings
```

---

## Validation Success Criteria

**Zero CRITICAL failures:**
- Missing requirements.md artifact
- Invalid YAML structure
- Missing F4 schema required fields (functional_requirements, non_functional_requirements, constraints, dependencies)

**Zero HIGH failures:**
- Vague requirements (>10 instances of "fast", "scalable", etc.)
- Insufficient functional requirements (<5 items)
- Missing constraints or dependencies sections

**MEDIUM/LOW failures documented with self-healing attempts:**
- Minor placeholder content (<5 instances)
- Missing optional fields (auto-added if possible)

---

## Output from Step 3.3

**Validation Report (internal):**

```markdown
## Validation Results

**Status:** {PASSED|PASSED WITH WARNINGS|FAILED}

### Auto-Corrected Issues ({count})
1. {Issue 1}: {What was fixed}
2. {Issue 2}: {What was fixed}

### Remaining Issues ({count})

**CRITICAL ({count}):**
- {Issue}: {Remediation guidance}

**HIGH ({count}):**
- {Issue}: {Remediation guidance}

**MEDIUM ({count}):**
- {Issue}: {Can defer to epic creation phase}

### Validation Summary
- requirements.md created: {PASS|FAIL}
- F4 schema compliance: {PASS|FAIL}
- Handoff readiness: {READY|NOT READY}
```

**Decision:**
- If PASSED or PASSED WITH WARNINGS → Proceed to Phase 3.4
- If FAILED with CRITICAL issues → HALT, report to user, require fixes

---

## References Used in Phase 3.3

**Primary:**
- **validation-checklists.md** (569 lines) - Complete validation procedures

**On Error:**
- **error-handling.md** - Validation failure recovery procedures

---

## Success Criteria

Validation complete when:
- [ ] requirements.md created and validated
- [ ] F4 schema compliance verified
- [ ] Auto-correctable issues fixed
- [ ] CRITICAL issues resolved (or halted)
- [ ] Validation report generated
- [ ] Ready to proceed to completion summary

**Token Budget:** ~2,000-4,000 tokens (load checklists, validate, auto-correct)

---

**Next Step:** Phase 3.4 (Present Completion Summary) - Load completion-handoff.md
