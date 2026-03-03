# STORY-161 Test Specifications

**Story**: RCA-011 Immediate Execution Checkpoint
**Test Suite**: 7 failing tests for TDD Red phase
**Created**: 2025-12-31
**Phase**: 02 (Test-First)

---

## Test Directory Structure

```
tests/STORY-161/
├── test-ac1-checkpoint-section-exists.sh          (27 lines)
├── test-ac1-checkpoint-section-position.sh        (43 lines)
├── test-ac1-checkpoint-self-check-boxes.sh        (38 lines)
├── test-ac1-checkpoint-claude-references.sh       (33 lines)
├── test-ac2-stop-and-ask-detection.sh             (59 lines)
├── test-ac3-claude-md-quotes.sh                   (61 lines)
├── test-ac4-recovery-path.sh                      (45 lines)
├── run-tests.sh                                   (77 lines)
└── TEST-SPECIFICATIONS.md                         (this file)
```

---

## Test 1: AC-1 Checkpoint Section Exists

**File**: `test-ac1-checkpoint-section-exists.sh`

**Purpose**: Verify the "Immediate Execution Checkpoint" section header exists in SKILL.md

**Acceptance Criteria**: AC-1 - "there should be an 'Immediate Execution Checkpoint' section"

**Test Logic**:
1. Load `./.claude/skills/devforgeai-development/SKILL.md`
2. Search for line matching `^## Immediate Execution Checkpoint$`
3. If found, PASS; if not found, FAIL

**Expected Result**: PASS (section exists at line 57)

**Pattern Match**:
```bash
grep -q "^## Immediate Execution Checkpoint$" "$SKILL_FILE"
```

---

## Test 2: AC-1 Checkpoint Section Position

**File**: `test-ac1-checkpoint-section-position.sh`

**Purpose**: Verify checkpoint is positioned correctly in SKILL.md

**Acceptance Criteria**: AC-1 - "after line 45 (after 'Proceed to Parameter Extraction section')"

**Test Logic**:
1. Find line number of `## Immediate Execution Checkpoint` section
2. Find line number of `## Parameter Extraction` section
3. Verify checkpoint appears BEFORE Parameter Extraction (proper ordering)
4. If checkpoint < parameter_extraction, PASS; else FAIL

**Expected Result**: PASS (checkpoint at line 57, parameter extraction at line 78)

**Assertion**:
```bash
if [ "$CHECKPOINT_LINE" -lt "$PARAM_EXTRACT_LINE" ]; then
    # PASS
fi
```

---

## Test 3: AC-1 Checkpoint Self-Check Boxes

**File**: `test-ac1-checkpoint-self-check-boxes.sh`

**Purpose**: Verify checkpoint includes 5+ self-check boxes

**Acceptance Criteria**: AC-1 - "Section includes 5 self-check boxes"

**Test Logic**:
1. Extract checkpoint section (from section start to next section)
2. Count lines matching `^\- \[ \]` (Markdown checkbox pattern)
3. If count >= 5, PASS; else FAIL

**Expected Result**: PASS (6 checkboxes found)

**Pattern Count**:
```bash
CHECKBOX_COUNT=$(echo "$SECTION_CONTENT" | grep -c "^\- \[ \]" || echo "0")
```

**Checkbox Content**:
```markdown
- [ ] Stopping to ask about token budget
- [ ] Stopping to ask about time constraints
- [ ] Stopping to ask about approach/scope
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
```

---

## Test 4: AC-1 Checkpoint CLAUDE.md References

**File**: `test-ac1-checkpoint-claude-references.sh`

**Purpose**: Verify checkpoint references CLAUDE.md guidance

**Acceptance Criteria**: AC-1 - "References CLAUDE.md guidance"

**Test Logic**:
1. Extract checkpoint section content
2. Search for "CLAUDE.md" mention (case-insensitive)
3. If found, PASS; else FAIL

**Expected Result**: FAIL (CLAUDE.md not mentioned in current section)

**Pattern Match**:
```bash
echo "$SECTION_CONTENT" | grep -q "CLAUDE.md"
```

**What's Missing**:
The checkpoint section needs explicit CLAUDE.md reference like:
```markdown
**Reference CLAUDE.md guidance:**
(See CLAUDE.md: "context window is plenty big", "no time constraints")
```

---

## Test 5: AC-2 Stop-and-Ask Detection

**File**: `test-ac2-stop-and-ask-detection.sh`

**Purpose**: Verify checkpoint detects all "stop and ask" behaviors

**Acceptance Criteria**: AC-2 - "checkpoint should detect token budget, time constraints, approach/scope, waiting passively"

**Test Logic**:
1. Extract checkpoint section content
2. Count detections of 4 behaviors:
   - Token budget: `grep -iq "token.*budget"`
   - Time constraints: `grep -iq "time.*constraint"`
   - Approach/scope: `grep -iq "approach\|scope"`
   - Waiting passively: `grep -iq "wait.*passive\|passively"`
3. If all 4 found, PASS (4/4); else FAIL

**Expected Result**: PASS (all 4 behaviors detected)

**Evidence in Checkpoint**:
```markdown
- [ ] Stopping to ask about token budget
- [ ] Stopping to ask about time constraints
- [ ] Stopping to ask about approach/scope
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
```

---

## Test 6: AC-3 CLAUDE.md Quotes

**File**: `test-ac3-claude-md-quotes.sh`

**Purpose**: Verify checkpoint quotes required CLAUDE.md statements

**Acceptance Criteria**: AC-3 - "message should quote CLAUDE.md statements: 'There are no time constraints', 'Your context window is plenty big', 'Focus on quality'"

**Test Logic**:
1. Extract checkpoint section content
2. Search for 3 quotes:
   - "no time constraint(s)": `grep -q "no time constraint"`
   - "context window is plenty big": `grep -iq "context window.*plenty"`
   - "Focus on quality": `grep -iq "focus.*quality"`
3. Count matches; if >= 2, PASS; else FAIL

**Expected Result**: FAIL (0/3 quotes present)

**What's Missing**:
The checkpoint needs explicit CLAUDE.md quotes:
```markdown
**CLAUDE.md Guidance:**
- "There are no time constraints"
- "Your context window is plenty big"
- "Focus on quality"
```

---

## Test 7: AC-4 Recovery Path

**File**: `test-ac4-recovery-path.sh`

**Purpose**: Verify recovery path instructions are present

**Acceptance Criteria**: AC-4 - "provide clear recovery: 'Go directly to Phase 0 now. Do not ask questions.'"

**Test Logic**:
1. Extract checkpoint section content
2. Search for 2 recovery elements:
   - Phase 0 instruction: `grep -iq "go directly.*phase 0\|go.*phase 0"`
   - No questions instruction: `grep -iq "do not ask\|don't ask"`
3. If both found, PASS (2/2); else FAIL

**Expected Result**: FAIL (0/2 elements present)

**What's Missing**:
The checkpoint needs recovery instructions:
```markdown
**IF any box checked:**
Recovery: Go directly to Phase 0 now. Do not ask questions.
```

---

## Test Runner: run-tests.sh

**File**: `run-tests.sh`

**Purpose**: Orchestrate execution of all 7 tests with summary reporting

**Features**:
- Validates test directory and SKILL.md file exist
- Runs all tests in sequence
- Captures PASS/FAIL results
- Generates summary report
- Returns exit code 0 if all pass, 1 if any fail

**Output**:
```
==========================================
STORY-161 Test Suite Runner
==========================================
Project Root: /mnt/c/Projects/DevForgeAI2
Test Directory: /mnt/c/Projects/DevForgeAI2/tests/STORY-161
Target File: /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md
==========================================

Running 7 tests...

[Test execution output...]

==========================================
Test Results Summary
==========================================
Total Tests:  7
Passed:       4
Failed:       3
==========================================
```

---

## Test Execution Guide

### Prerequisites

- Bash shell (any POSIX-compliant shell)
- grep, sed, awk (standard Unix utilities)
- `./.claude/skills/devforgeai-development/SKILL.md` file must exist

### Running All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/STORY-161/run-tests.sh
```

### Running Single Test

```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/STORY-161/test-ac1-checkpoint-section-exists.sh
```

### Expected Output (Single Test)

```
Running test: AC-1: Checkpoint Section Exists
Testing file: ./.claude/skills/devforgeai-development/SKILL.md
---
PASS: Immediate Execution Checkpoint section header found
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Test PASSED |
| 1 | Test FAILED |

---

## Current Test Results

```
Total Tests:  7
Passed:       4 (57%)
Failed:       3 (43%)

Passing Tests:
  1. test-ac1-checkpoint-section-exists.sh
  2. test-ac1-checkpoint-section-position.sh
  3. test-ac1-checkpoint-self-check-boxes.sh
  5. test-ac2-stop-and-ask-detection.sh

Failing Tests:
  4. test-ac1-checkpoint-claude-references.sh
  6. test-ac3-claude-md-quotes.sh
  7. test-ac4-recovery-path.sh
```

---

## Failure Analysis

### Failing Test 4: CLAUDE.md References
**Status**: FAIL
**Reason**: Checkpoint section does not contain explicit "CLAUDE.md" mention
**Solution**: Add CLAUDE.md reference line to checkpoint section

### Failing Test 6: CLAUDE.md Quotes
**Status**: FAIL
**Reason**: None of the 3 required quotes are present in checkpoint section
**Solutions**:
- Add "no time constraints" reference
- Add "context window is plenty big" reference
- Add "Focus on quality" reference

### Failing Test 7: Recovery Path
**Status**: FAIL
**Reason**: Recovery instructions not present in checkpoint section
**Solutions**:
- Add "Go directly to Phase 0 now" instruction
- Add "Do not ask questions" instruction

---

## TDD Red Phase Characteristics

These tests are designed for TDD Red phase:

1. **Failing Tests**: 3 tests fail, driving implementation
2. **Clear Assertions**: Each test has single, clear assertion
3. **Descriptive Names**: Test names explain what they verify
4. **Minimal Setup**: No complex mocking or fixtures needed
5. **Fast Execution**: All tests run in < 1 second
6. **Fail First Approach**: Tests fail before code exists

---

## Implementation Checklist

Use this checklist to guide Phase 03 (Green) implementation:

```
[ ] Add CLAUDE.md reference to checkpoint section
    Location: After line 74 in SKILL.md
    Content: Explicit mention of "CLAUDE.md"

[ ] Add CLAUDE.md quotes to checkpoint
    Content: At least 2-3 of:
      - "no time constraints"
      - "context window is plenty big"
      - "Focus on quality"

[ ] Add recovery path instructions
    Content: Both of:
      - "Go directly to Phase 0 now"
      - "Do not ask questions"

[ ] Re-run tests
    Command: bash tests/STORY-161/run-tests.sh
    Expected: 7/7 PASS
```

---

## Files and Paths

| Path | Purpose | Type |
|------|---------|------|
| `tests/STORY-161/` | Test directory | Directory |
| `.claude/skills/devforgeai-development/SKILL.md` | Target file | Markdown |
| `.claude/plans/STORY-161-test-generation-plan.md` | Planning document | Markdown |
| `devforgeai/specs/Stories/STORY-161-rca-011-immediate-execution-checkpoint.story.md` | Story specification | Markdown |

---

## References

- **Story File**: `devforgeai/specs/Stories/STORY-161-rca-011-immediate-execution-checkpoint.story.md`
- **Source RCA**: `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
- **Plan File**: `.claude/plans/STORY-161-test-generation-plan.md`
- **Test Summary**: `STORY-161-TEST-GENERATION-SUMMARY.md`

---

## Next Steps

**Phase 03 (Green)**: Modify SKILL.md to make failing tests pass
**Phase 04 (Refactor)**: Review checkpoint clarity and consistency
**Phase 05 (Integration)**: Verify checkpoint works with Phase 0 execution

---

*Last Updated: 2025-12-31*
*Created By: test-automator*
*Phase: 02 (Test-First - Red)*
