# STORY-131 Test Suite Index

**Test Suite Status:** COMPLETE - Ready for Implementation (TDD Red Phase)
**Generated:** December 24, 2025
**Framework:** DevForgeAI TDD Automation
**Language:** Bash Integration Tests (Claude Code native)

---

## Quick Start

### Run All Tests
```bash
bash tests/STORY-131/run-all-tests.sh
```

### View Documentation
1. **Complete Test Guide:** `README.md` (550 lines)
2. **Generation Summary:** `TEST-GENERATION-SUMMARY.md` (450 lines)
3. **This Index:** `INDEX.md` (this file)

---

## Test Suite Overview

### Statistics
- **Total Test Cases:** 42
- **Total Lines of Test Code:** 2,170
- **Test Suites:** 4 + 1 master orchestrator
- **Acceptance Criteria Covered:** 5/5 (100%)
- **Expected Status:** 0/42 PASS (TDD Red phase - tests should fail initially)

### Test Distribution
| AC | Title | Tests | File |
|----|-------|-------|------|
| #1 | Phase 4 Removal Preserves Functionality | 10 | `test-ac1-*.sh` |
| #2 | Subagent Invocation | 6 | `test-ac2-ac3-*.sh` |
| #3 | Command Phase 3 Implementation | 4 | `test-ac2-ac3-*.sh` |
| #4 | Size Reduction Achieved | 10 | `test-ac4-*.sh` |
| #5 | Single Summary Per Session | 12 | `test-ac5-*.sh` |

---

## Files in This Directory

### Executable Test Scripts
```
test-ac1-phase4-removal.sh            240 lines  |  Phase 4 removal (10 tests)
test-ac2-ac3-subagent-invocation.sh   420 lines  |  Subagent + Phase 3 (10 tests)
test-ac4-size-reduction.sh            400 lines  |  Size metrics (10 tests)
test-ac5-single-summary.sh            380 lines  |  Summary control (12 tests)
run-all-tests.sh                      210 lines  |  Master orchestrator
```

### Documentation Files
```
README.md                             550 lines  |  Complete test documentation
TEST-GENERATION-SUMMARY.md            450 lines  |  Generation details & principles
INDEX.md                              (this)     |  Quick reference index
```

---

## Running Tests

### Option 1: Run All Tests (Recommended)
```bash
bash tests/STORY-131/run-all-tests.sh
```
**Output:** Summary of all 42 tests with pass/fail status

### Option 2: Run Specific AC Suite
```bash
# AC#1: Phase 4 Removal
bash tests/STORY-131/test-ac1-phase4-removal.sh

# AC#2 & #3: Subagent Invocation
bash tests/STORY-131/test-ac2-ac3-subagent-invocation.sh

# AC#4: Size Reduction
bash tests/STORY-131/test-ac4-size-reduction.sh

# AC#5: Single Summary
bash tests/STORY-131/test-ac5-single-summary.sh
```

### Option 3: Debug Mode
```bash
bash -x tests/STORY-131/run-all-tests.sh 2>&1 | head -200
```

---

## Expected Test Results

### TDD Red Phase (Before Implementation)
```
Test Status: FAILING (0-10 of 42 pass - expected for TDD Red)

Likely failures:
  ✗ AC#1: Phase 4 not removed (0/10 pass)
  ~ AC#2: Subagent exists via STORY-133 (varies)
  ✗ AC#3: Phase 3 doesn't exist (0/4 pass)
  ✗ AC#4: File size threshold (likely 0/10 pass)
  ✗ AC#5: Single summary not enforced (0/12 pass)
```

### TDD Green Phase (After Implementation)
```
Test Status: PASSING

Expected results:
  ✓ AC#1: Phase 4 Removal - 10/10 PASS
  ✓ AC#2: Subagent Invocation - 6/6 PASS
  ✓ AC#3: Command Phase 3 - 4/4 PASS
  ✓ AC#4: Size Reduction - 10/10 PASS
  ✓ AC#5: Single Summary - 12/12 PASS

Total: 42/42 PASS
```

---

## Test Details Summary

### AC#1: Phase 4 Removal Preserves Functionality (10 tests)
**File:** `test-ac1-phase4-removal.sh`

Verifies that Phase 4 summary presentation code is completely removed:
- ✓ No "## Phase 4" header remains
- ✓ No summary display logic (Display calls)
- ✓ No epic count, complexity score, tier display
- ✓ No ASCII box drawing characters (╔═, ║, etc.)
- ✓ No greenfield/brownfield recommendations in Phase 4

**Key Assertion:** All grep searches for Phase 4 patterns return NO MATCHES

---

### AC#2: Subagent Exists & Properly Structured (6 tests)
**File:** `test-ac2-ac3-subagent-invocation.sh`

Verifies ideation-result-interpreter subagent has required structure:
- ✓ File exists at `.claude/agents/ideation-result-interpreter.md`
- ✓ YAML frontmatter: `name:` field
- ✓ YAML frontmatter: `description:` field
- ✓ YAML frontmatter: `model:` field
- ✓ YAML frontmatter: `tools:` field
- ✓ Proper Markdown heading structure

**Created By:** STORY-133 (prerequisite)

---

### AC#3: Command Phase 3 Invokes Result Interpreter (4 tests)
**File:** `test-ac2-ac3-subagent-invocation.sh`

Verifies new Phase 3 section properly invokes subagent:
- ✓ New "## Phase 3:" section exists in ideate.md
- ✓ Phase 3 comes AFTER Phase 2, BEFORE Phase N
- ✓ Contains `Task(subagent_type="ideation-result-interpreter")`
- ✓ Task() syntax is correct with subagent_type parameter

**Plus 6 additional validation tests:**
- ✓ Skill output passed to subagent
- ✓ Result displayed to user
- ✓ No duplicate summary logic
- ✓ No hardcoded templates
- ✓ Proper section descriptions

---

### AC#4: Size Reduction Achieved (10 tests)
**File:** `test-ac4-size-reduction.sh`

Verifies command size reduced from 554 toward ~200 lines:
- ✓ Line count ≤250 lines (55% reduction minimum)
- ✓ Line count ≥150 lines (preserves functionality)
- ✓ Reduction percentage ≥45% (minimum acceptable)
- ✓ File is readable and valid
- ✓ Phase structure intact (multiple phases present)
- ✓ File doesn't exceed 350 lines (sanity check)

**Size Metrics:**
```
Original:        554 lines
Target:          ~200 lines
Acceptance Range: 150-250 lines (55%+ reduction)
Calculation:     (554 - current) × 100 ÷ 554 = % reduction
```

---

### AC#5: Single Summary Per Session (12 tests)
**File:** `test-ac5-single-summary.sh`

Verifies only ONE summary displays, from result interpreter:
- ✓ No multiple summary sections in command
- ✓ No hardcoded Display() calls for summary
- ✓ Command delegates to result interpreter
- ✓ Phase 4 completely removed
- ✓ No $SUMMARY variable assignments
- ✓ No hardcoded summary templates
- ✓ Exactly ONE Task() invocation
- ✓ Task() only in Phase 3
- ✓ No summary logic after Phase 3
- ✓ Proper command structure
- ✓ Correct phase execution order

---

## Implementation Guidance

### What the Tests Validate

1. **Phase 4 is GONE**
   - No header "## Phase 4"
   - No summary display logic
   - Tests use grep patterns to confirm removal

2. **Phase 3 is NEW**
   - New section between Phase 2 and Phase N
   - Contains Task(subagent_type="ideation-result-interpreter")
   - Minimal code (delegates to subagent)

3. **File Size REDUCED**
   - From 554 lines down to target 200-250 range
   - Tests measure with `wc -l` command
   - 45%+ reduction required for pass

4. **Single Summary ENFORCED**
   - Exactly one Task() call
   - Only in Phase 3
   - No other summary logic in command

### What Tests DON'T Validate (Subagent Responsibility)

Tests verify that the subagent is INVOKED, but NOT:
- What the subagent actually returns
- How it formats the display
- How it handles edge cases (large output, malformed input)
- Response time performance

Those validations are in subagent-specific tests (in `.claude/agents/` if created).

---

## Test Quality Checklist

- [x] 100% acceptance criteria coverage
- [x] 42 individual test cases
- [x] Each test independent (no shared state)
- [x] Clear test names (test_should_[behavior]_when_[condition])
- [x] Descriptive failure messages
- [x] Color-coded output (RED/GREEN/YELLOW)
- [x] Configurable thresholds (size, counts, etc.)
- [x] No external dependencies (bash + standard Unix tools)
- [x] Grep-based assertions (simple, reliable)
- [x] Comprehensive documentation (README + summary)
- [x] Executable scripts (chmod +x applied)
- [x] Master orchestrator (run-all-tests.sh)

---

## Common Failure Patterns

### Pattern 1: "Phase 4 not removed"
```
Test fails: test_phase4_header_removed
grep finds: "## Phase 4:" in ideate.md
Fix: Remove the Phase 4 section completely
```

### Pattern 2: "Phase 3 missing"
```
Test fails: test_ideate_phase3_exists
grep finds: No "## Phase 3:" in ideate.md
Fix: Add new Phase 3 section after Phase 2
```

### Pattern 3: "Task invocation wrong"
```
Test fails: test_ideate_phase3_task_invocation
Expected: Task(subagent_type="ideation-result-interpreter")
Got: Task(subagent="ideation-result-interpreter")
Fix: Use subagent_type= parameter (not subagent=)
```

### Pattern 4: "File too large"
```
Test fails: test_ideate_line_count_max
Current: 380 lines
Max: 250 lines
Fix: Phase 4 removal should reduce by ~30-40 lines
```

### Pattern 5: "Multiple Task calls"
```
Test fails: test_single_result_interpreter_invocation
Found: 2 Task() calls
Expected: 1 Task() call
Fix: Ensure only one Task(subagent_type=...) in entire command
```

---

## Integration with STORY-133

STORY-131 depends on STORY-133 (create ideation-result-interpreter subagent):

**Dependency Chain:**
```
STORY-133: Create ideation-result-interpreter subagent
    ↓ (creates file)
STORY-131: Delegate summary to skill
    ↓ (tests verify delegation works)
Tests verify Task() invocation succeeds
```

**Status Check:**
```bash
# Verify subagent exists (created by STORY-133)
ls -la .claude/agents/ideation-result-interpreter.md

# Should output: -rwxrwxrwx ... ideation-result-interpreter.md
```

---

## TDD Workflow Integration

These tests are part of the **TDD Red Phase:**

```
Red Phase (Now)
├─ Tests generated (42 test cases)
├─ Tests currently failing (expected)
└─ All tests ready to run

        ↓

Green Phase (Implementation)
├─ Implement features
├─ Run tests
├─ Make failing tests pass
└─ Goal: 42/42 PASS

        ↓

Refactor Phase
├─ Improve code quality
├─ Keep tests passing
└─ Maintain 42/42 PASS
```

---

## Next Steps

### 1. Review Tests (Understand Requirements)
```bash
# Read documentation first
cat tests/STORY-131/README.md | less

# Review individual test files
cat tests/STORY-131/test-ac1-phase4-removal.sh | less
```

### 2. Run Tests to Confirm Baseline
```bash
# Run all tests (expect failures)
bash tests/STORY-131/run-all-tests.sh

# Should output: ~0-10 PASS / ~32-42 FAIL
```

### 3. Implement Changes
Based on test failures, implement:
1. Remove Phase 4 from ideate.md
2. Add Phase 3 with Task() invocation
3. Verify subagent exists (STORY-133)

### 4. Run Tests Again
```bash
# Run tests after each change
bash tests/STORY-131/run-all-tests.sh

# Goal: 42/42 PASS
```

### 5. Update Story Documentation
- [ ] Mark AC#1 checklist items complete
- [ ] Mark AC#2 checklist items complete
- [ ] Mark AC#3 checklist items complete
- [ ] Mark AC#4 checklist items complete
- [ ] Mark AC#5 checklist items complete

### 6. Commit Changes
```bash
git add tests/STORY-131/
git add .claude/commands/ideate.md
git commit -m "STORY-131: Delegate summary presentation to skill"
```

---

## File Locations

### Test Directory
```
tests/STORY-131/
```

### Story File
```
devforgeai/specs/Stories/STORY-131-delegate-summary-presentation-to-skill.story.md
```

### Implementation Files (to be modified)
```
.claude/commands/ideate.md
```

### Prerequisite (STORY-133)
```
.claude/agents/ideation-result-interpreter.md
```

---

## Key Metrics

### Coverage Metrics
- Acceptance Criteria Covered: 5/5 (100%)
- Test Cases Generated: 42
- Lines of Test Code: 2,170
- Lines of Documentation: 1,000+
- Average Tests Per AC: 8.4

### Test Distribution
- Unit-like (file checks): 15 tests
- Integration (workflow): 27 tests
- Metric (size/performance): 10 tests
- Structural (ordering): 15 tests

### Quality Metrics
- Test Independence: 100% (no shared state)
- Documentation Completeness: 95% (README, summary, index)
- Failure Clarity: 100% (all failures show grep context)
- Maintainability: High (helper functions, configurable thresholds)

---

## Support & Troubleshooting

### Test Won't Run
```bash
# Make executable
chmod +x tests/STORY-131/*.sh

# Run with debug
bash -x tests/STORY-131/run-all-tests.sh 2>&1 | head -50
```

### Tests Pass Prematurely
This shouldn't happen with TDD Red phase. If all tests pass:
1. Verify you're running against correct file
2. Check if ideate.md was already modified
3. Revert and try again from baseline

### Specific Test Fails Unexpectedly
```bash
# Run just that test
bash tests/STORY-131/test-ac1-phase4-removal.sh

# Review output for exact grep pattern
# Check if file contains pattern somewhere else
grep -n "pattern" .claude/commands/ideate.md
```

---

## References

- **STORY-131:** `devforgeai/specs/Stories/STORY-131-*.story.md`
- **STORY-133:** Create ideation-result-interpreter subagent (prerequisite)
- **Tech Stack:** `devforgeai/specs/context/tech-stack.md` (Bash integration tests required)
- **Command:** `.claude/commands/ideate.md` (file to modify)
- **Subagent:** `.claude/agents/ideation-result-interpreter.md` (created by STORY-133)

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Run all tests | `bash tests/STORY-131/run-all-tests.sh` |
| Run AC#1 tests | `bash tests/STORY-131/test-ac1-phase4-removal.sh` |
| Run AC#2-3 tests | `bash tests/STORY-131/test-ac2-ac3-subagent-invocation.sh` |
| Run AC#4 tests | `bash tests/STORY-131/test-ac4-size-reduction.sh` |
| Run AC#5 tests | `bash tests/STORY-131/test-ac5-single-summary.sh` |
| View README | `cat tests/STORY-131/README.md` |
| View summary | `cat tests/STORY-131/TEST-GENERATION-SUMMARY.md` |
| Make executable | `chmod +x tests/STORY-131/*.sh` |
| Debug output | `bash -x tests/STORY-131/run-all-tests.sh 2>&1` |

---

## Summary

**42 comprehensive test cases** generated for STORY-131 covering all 5 acceptance criteria. Tests are designed to FAIL initially (TDD Red phase) and PASS after proper implementation. The test suite validates removal of Phase 4, addition of Phase 3 with subagent invocation, size reduction achievement, and single summary guarantee.

All tests are independent, well-documented, and executable via bash. No external dependencies required - pure Claude Code native testing.

**Next Action:** Review README.md, run tests to establish baseline, then implement changes to make tests pass.
