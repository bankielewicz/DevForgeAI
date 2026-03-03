# Test Specification: STORY-203 - Add source-tree.md Validation to test-automator

**Story ID:** STORY-203
**Implementation Type:** Slash Command / Subagent (.md)
**Output Type:** Test Specification Document (non-executable)
**Target File:** `.claude/agents/test-automator.md`
**Test Date:** 2026-01-11

---

## Test Summary

| AC | Test Name | Status | Evidence |
|----|-----------|--------|----------|
| AC#1 | Step 4.5 marker exists | PASS (GREEN) | Line 549 |
| AC#2 | Test directory extraction logic | PASS (GREEN) | Line 561 |
| AC#3 | HALT pattern before Write | PASS (GREEN) | Line 574 |
| AC#4 | Error message with fix guidance | PASS (GREEN) | Lines 575-591 |
| AC#5 | source-tree.md in References | **FAIL (RED)** | Lines 1238-1243 missing source-tree.md |

---

## Test Cases

### TEST-01: AC#1 - Step 4.5 Marker Exists

**Purpose:** Verify Step 4.5 is added after Step 4 in Phase 2 workflow

**Structural Pattern:**
```regex
^4\.5\.\s+\*\*Read Source Tree
```

**Validation Command:**
```bash
grep -n "4.5.*Read Source Tree" .claude/agents/test-automator.md
```

**Expected:** Match at line ~549 (after Step 4, before Step 5)

**Actual Result:** PASS
```
549:4.5. **Read Source Tree for Test File Locations (MANDATORY)**
```

**Evidence:** Step 4.5 exists at line 549, positioned correctly between Step 4 (line 541) and Step 5 (line 593).

---

### TEST-02: AC#2 - Test Directory Extraction Logic

**Purpose:** Verify source-tree.md Read() invocation and directory extraction

**Structural Pattern:**
```regex
Read\(file_path=.*source-tree\.md
```

**Validation Command:**
```bash
grep -n "Read.*source-tree.md" .claude/agents/test-automator.md
```

**Expected:** Read() call for source-tree.md with extraction logic for installer/tests/

**Actual Result:** PASS
```
552:   Read(file_path="devforgeai/specs/context/source-tree.md")
561:       test_directory = "installer/tests/"  # Per source-tree.md line 378
```

**Evidence:**
- Line 552 contains Read() call for source-tree.md
- Line 561 shows installer/tests/ extraction pattern

---

### TEST-03: AC#3 - HALT Pattern Before Write

**Purpose:** Verify HALT pattern exists for path violations BEFORE Write() calls

**Structural Pattern:**
```regex
HALT test generation
```

**Validation Command:**
```bash
grep -n "HALT test generation" .claude/agents/test-automator.md
```

**Expected:** HALT pattern within Step 4.5 (lines 549-591)

**Actual Result:** PASS
```
574:           HALT test generation
```

**Evidence:** HALT pattern at line 574, within Step 4.5 scope (549-591), confirming validation occurs before Write().

---

### TEST-04: AC#4 - Error Message with Fix Guidance

**Purpose:** Verify error message includes expected directory, attempted location, and fix instructions

**Structural Patterns:**
```regex
Expected directory:
Attempted location:
Fix:
source-tree.md constraint
```

**Validation Commands:**
```bash
grep -n "Expected directory:" .claude/agents/test-automator.md
grep -n "Attempted location:" .claude/agents/test-automator.md
grep -n "source-tree.md constraint" .claude/agents/test-automator.md
```

**Expected:** All four elements present in error message template

**Actual Result:** PASS (verified by reading lines 575-591)

**Evidence from lines 575-591:**
```markdown
           Return error message:
           """
           TEST LOCATION VIOLATION

           Test file location violates source-tree.md constraint:

           Expected directory: {test_directory}
           Attempted location: {test_file_path}

           Fix:
           1. Update planned test paths to start with: {test_directory}
           2. OR update source-tree.md with new pattern
           3. Retry test generation

           source-tree.md constraint (line 378):
           {excerpt from source-tree.md showing correct location}
           """
```

All required elements present:
- [x] Expected directory: {test_directory}
- [x] Attempted location: {test_file_path}
- [x] Fix instructions (3 options)
- [x] source-tree.md constraint excerpt

---

### TEST-05: AC#5 - source-tree.md in References Section (RED - FAILING)

**Purpose:** Verify source-tree.md is added to the References section

**Structural Pattern:**
```regex
## References[\s\S]*source-tree\.md
```

**Validation Command:**
```bash
grep -A 10 "## References" .claude/agents/test-automator.md | grep "source-tree.md"
```

**Expected:** source-tree.md listed in References section

**Actual Result:** FAIL
```
1238:## References
1239:
1240:- **Story Files**: `devforgeai/specs/Stories/*.story.md` (acceptance criteria source)
1241:- **Tech Stack**: `devforgeai/specs/context/tech-stack.md` (test framework choice)
1242:- **Coverage Reports**: `devforgeai/qa/coverage/coverage-report.json`
1243:- **Coverage Thresholds**: `devforgeai/qa/coverage-thresholds.md`
```

**Missing Entry (per AC#5):**
```markdown
- **Source Tree**: `devforgeai/specs/context/source-tree.md` (test file location constraints)
```

**Evidence:** References section at lines 1238-1243 does NOT contain source-tree.md. This is a TDD RED test case.

---

## TDD Red Phase Summary

**Tests Passing (GREEN - Already Implemented):**
- TEST-01: Step 4.5 marker exists (line 549)
- TEST-02: Test directory extraction logic (lines 552, 561)
- TEST-03: HALT pattern before Write (line 574)
- TEST-04: Error message with fix guidance (lines 575-591)

**Tests Failing (RED - Needs Implementation):**
- TEST-05: source-tree.md in References section (lines 1238-1243)

---

## Implementation Required

To make TEST-05 pass, add the following to the References section:

**File:** `.claude/agents/test-automator.md`
**Location:** Line 1243 (after Coverage Thresholds entry)

**Add:**
```markdown
- **Source Tree**: `devforgeai/specs/context/source-tree.md` (test file location constraints)
```

**Expected References Section After Fix:**
```markdown
## References

- **Story Files**: `devforgeai/specs/Stories/*.story.md` (acceptance criteria source)
- **Tech Stack**: `devforgeai/specs/context/tech-stack.md` (test framework choice)
- **Coverage Reports**: `devforgeai/qa/coverage/coverage-report.json`
- **Coverage Thresholds**: `devforgeai/qa/coverage-thresholds.md`
- **Source Tree**: `devforgeai/specs/context/source-tree.md` (test file location constraints)
```

---

## Validation Checklist

| Check | Pattern | Line | Status |
|-------|---------|------|--------|
| Step 4.5 header | `4.5.*Read Source Tree` | 549 | PASS |
| Read() invocation | `Read.*source-tree.md` | 552 | PASS |
| Directory extraction | `installer/tests/` | 561 | PASS |
| HALT pattern | `HALT test generation` | 574 | PASS |
| Error message - expected dir | `Expected directory:` | 580 | PASS |
| Error message - attempted loc | `Attempted location:` | 581 | PASS |
| Error message - fix guidance | `Fix:` | 583 | PASS |
| Error message - constraint excerpt | `source-tree.md constraint` | 589 | PASS |
| References - source-tree.md | `source-tree.md` in References | N/A | **FAIL** |

---

## Technical Specification Coverage

| Requirement ID | Description | Test | Status |
|----------------|-------------|------|--------|
| CFG-001 | Step 4.5 for source-tree.md reading | TEST-01 | PASS |
| CFG-002 | Test directory extraction logic | TEST-02 | PASS |
| CFG-003 | Test path validation with HALT pattern | TEST-03 | PASS |
| CFG-004 | source-tree.md in References section | TEST-05 | FAIL |
| BR-001 | source-tree.md is immutable constraint | TEST-03 | PASS |
| BR-002 | Validation before Write() | TEST-03, TEST-04 | PASS |
| BR-003 | Native Read() tool (not Bash) | TEST-02 | PASS |

---

## References

- **Story File**: `devforgeai/specs/Stories/STORY-203-test-automator-source-tree-validation.story.md`
- **Target File**: `.claude/agents/test-automator.md`
- **Source Tree Constraint**: `devforgeai/specs/context/source-tree.md` (line 602 - test-automator.md location)
- **RCA**: RCA-017 (test-automator source tree constraint violation)
