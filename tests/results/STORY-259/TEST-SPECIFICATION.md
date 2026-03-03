# Test Specification: STORY-259

**Story:** Add gaps.json Verification to Phase 4 Execution Summary
**Target File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Implementation Type:** Markdown Documentation (non-executable)
**Test Type:** Structural Validation

---

## Test Summary

| AC | Test Count | Validation Type |
|----|------------|-----------------|
| AC#1 | 2 | Checkpoint text exists |
| AC#2 | 2 | Existence check documented |
| AC#3 | 3 | HALT behavior documented |
| AC#4 | 2 | Skip logic documented |
| **Total** | **9** | Structural |

---

## AC#1: Verification Checkpoint Addition

### TEST-001: Checkpoint Item Exists in Step 4.3

**Type:** Structural (Grep pattern match)

**Validation:**
```bash
grep -qE "gaps\.json exists" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** Pattern found in file
**Pass Criteria:** Exit code 0

---

### TEST-002: RCA-002 Reference in Checkpoint

**Type:** Structural (Grep pattern match)

**Validation:**
```bash
grep -qE "\[RCA-002\]|RCA-002" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** RCA-002 reference exists near checkpoint
**Pass Criteria:** Exit code 0

---

## AC#2: gaps.json Existence Check

### TEST-003: File Path Pattern Documented

**Type:** Content validation

**Validation:**
```bash
grep -qE "devforgeai/qa/reports/.*gaps\.json" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** gaps.json path pattern documented
**Pass Criteria:** Exit code 0

---

### TEST-004: FAILED Status Conditional Documented

**Type:** Structural (conditional logic)

**Validation:**
```bash
grep -qE "(IF|WHEN).*(FAILED|overall_status.*FAILED)" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** Conditional check for FAILED status exists
**Pass Criteria:** Exit code 0

---

## AC#3: HALT on Missing gaps.json

### TEST-005: CRITICAL Error Message Documented

**Type:** Content validation

**Validation:**
```bash
grep -qE "CRITICAL.*gaps\.json.*missing|gaps\.json.*missing.*CRITICAL" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** CRITICAL error message text exists
**Pass Criteria:** Exit code 0

---

### TEST-006: HALT Instruction Documented

**Type:** Structural (HALT behavior)

**Validation:**
```bash
grep -qE "HALT.*gaps\.json|Create gaps\.json before" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** HALT instruction with remediation message exists
**Pass Criteria:** Exit code 0

---

### TEST-007: Step 4.3 Contains Verification Checkpoint

**Type:** Structural (section location)

**Validation:**
```bash
grep -A 80 "Step 4\.3" .claude/skills/devforgeai-qa/SKILL.md | grep -qE "gaps\.json"
```

**Expected:** gaps.json reference within Step 4.3 section
**Pass Criteria:** Exit code 0
**Note:** Step 4.3 is ~75 lines, so -A 80 captures full section including Validation Checkpoint

---

## AC#4: Skip Verification for Passing QA

### TEST-008: Skip Logic for PASSED Status

**Type:** Structural (conditional skip)

**Validation:**
```bash
grep -qE "(PASSED|PASS WITH WARNINGS).*skip|skip.*(PASSED|PASS)" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** Skip logic documented for passing QA
**Pass Criteria:** Exit code 0

---

### TEST-009: Conditional Check Structure

**Type:** Structural (IF/ELSE documented)

**Validation:**
```bash
grep -qE "IF.*FAILED.*gaps|ELSE|overall_status.*(PASSED|FAILED)" .claude/skills/devforgeai-qa/SKILL.md
```

**Expected:** Conditional structure (IF FAILED check, ELSE skip)
**Pass Criteria:** Exit code 0

---

## Validation Checklist

**Before implementation is complete, verify:**

- [ ] TEST-001: Checkpoint item "gaps.json exists?" in Step 4.3
- [ ] TEST-002: RCA-002 reference in checkpoint comment
- [ ] TEST-003: File path `devforgeai/qa/reports/{STORY-ID}-gaps.json` documented
- [ ] TEST-004: Conditional check for FAILED status
- [ ] TEST-005: CRITICAL error message text
- [ ] TEST-006: HALT instruction with remediation
- [ ] TEST-007: Verification within Step 4.3 section
- [ ] TEST-008: Skip logic for PASSED/PASS WITH WARNINGS
- [ ] TEST-009: IF/ELSE conditional structure

---

## Expected SKILL.md Changes

**Location:** Step 4.3 Validation Checkpoint section (around line 1160)

**Required Addition:**
```markdown
- [ ] **IF QA FAILED: gaps.json exists?** [RCA-002]

IF overall_status == "FAILED":
    Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
    IF NOT found:
        Display: "CRITICAL: gaps.json missing for failed QA"
        HALT: "Create gaps.json before completing QA workflow"
ELSE:
    # PASSED or PASS WITH WARNINGS - skip gaps.json check
    Display: "gaps.json check skipped (QA passed)"
```

---

## Test Execution

**Manual Validation:**
1. Read target file: `Read(file_path=".claude/skills/devforgeai-qa/SKILL.md")`
2. Execute each grep pattern against file content
3. Mark test PASS if pattern found, FAIL if not found

**Automated (post-implementation):**
```bash
# Run all 9 tests
for test in TEST-001 TEST-002 ... TEST-009; do
    execute_grep_pattern $test
done
```

---

**Test Specification Version:** 1.0
**Created:** 2026-01-16
**Story Template Version:** 2.5
