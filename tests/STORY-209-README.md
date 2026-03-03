# STORY-209: Phase Resumption Protocol Tests

**Story**: STORY-209 - Document Phase Resumption Protocol for Interrupted Workflows
**Test Type**: Documentation Specification Tests (Bash/Grep validation)
**Status**: TDD Red Phase Complete - Ready for Green Phase
**Generated**: 2026-01-13

---

## Overview

This directory contains comprehensive tests for STORY-209, which documents how users and Claude detect and recover from interrupted /dev workflows.

The test suite validates that all 5 acceptance criteria are properly documented in `.claude/skills/devforgeai-development/SKILL.md` with correct structure, section headers, and required content.

---

## Files in This Directory

### Test Execution Files

**`STORY-209-phase-resumption-protocol-tests.sh`** (Executable)
- Main test suite with 25 documentation validation tests
- Uses Bash and grep for pattern-based validation
- Color-coded output (GREEN pass, RED fail, YELLOW test marker)
- Provides detailed failure reasons and guidance
- Exit code: 0 = all pass, 1 = any fail

**`STORY-209-test-execution-log.txt`**
- Sample output from test execution
- Shows current state: 13/25 passing, 12/25 failing
- Demonstrates TDD Red phase (tests fail before implementation)

### Documentation Files

**`STORY-209-TEST-GENERATION-SUMMARY.md`** (This Documentation)
- Comprehensive test generation report
- Covers all 5 AC with detailed analysis
- Lists failing tests with implementation guidance
- Provides test metrics and quality assurance notes

**`.claude/plans/STORY-209-test-generation-plan.md`**
- Detailed project plan with task breakdown
- Implementation tasks for TDD Green phase
- Dependencies and success criteria
- Change log and references

---

## Quick Start

### Run Tests
```bash
chmod +x tests/STORY-209-phase-resumption-protocol-tests.sh
./tests/STORY-209-phase-resumption-protocol-tests.sh
```

### Expected Output
```
Tests run:     25
Tests passed:  13
Tests failed:  12

12 test(s) failed - Phase Resumption Protocol sections need to be added
```

### Interpret Results
- **TDD Red Phase** (expected): 12+ tests failing
- **TDD Green Phase** (goal): All 25 tests passing
- **TDD Refactor** (optional): All tests pass + improved clarity

---

## Test Coverage by Acceptance Criteria

### AC#1: User Detection Indicators (5 tests, 2/5 passing)
Tests validate documentation of:
- TodoWrite status shows phases as pending/in_progress ✓
- DoD completion percentage drops below 100% ✗
- Story status doesn't update as expected ✓
- No git commit of story file ✗
- Section header exists ✗

### AC#2: User Recovery Command (4 tests, 1/4 passing)
Tests validate documentation of:
- Recovery command template (e.g., `/dev STORY-XXX --resume`) ✗
- References pending phases list ✓
- "Resume execution now" action phrase ✗
- Section header exists ✗

### AC#3: Claude Resumption Steps (7 tests, 6/7 passing)
Tests validate documentation of:
- Step 1: Check TodoWrite State ✓
- Step 2: Verify Previous Phases ✓
- Step 3: Load Phase Reference ✓
- Step 4: Execute Remaining Phases ✓
- Step 5: Final Validation ✓
- Multiple numbered steps (found 13 total) ✓
- Section header exists ✗

### AC#4: Resumption Validation Checklist (5 tests, 3/5 passing)
Tests validate documentation of:
- Checklist section exists ✓
- User confirmed resumption item ✗
- Previous phases completion evidence ✓
- No conflicting git changes ✓
- Story file readable item ✗

### AC#5: Fresh Start vs Resume Decision (4 tests, 1/4 passing)
Tests validate documentation of:
- Decision guidance section exists ✗
- "Start fresh" recommendation ✗
- Recommendation for unclear state ✗
- Table/matrix format ✓

---

## Implementation Tasks (TDD Green Phase)

To make all tests pass, add these sections to `.claude/skills/devforgeai-development/SKILL.md`:

### Task 1: User Detection Indicators Section
Add after "Phase Orchestration Loop" section:
```markdown
## User Detection Indicators

When your /dev workflow is interrupted, you'll notice these indicators:

1. **TodoWrite list shows phases as pending or in_progress**
   - Some phases haven't reached "completed" status
   - Indicates workflow interrupted mid-execution

2. **DoD completion percentage <100%**
   - Definition of Done checklist is not fully checked
   - Story file shows incomplete acceptance criteria verification

3. **Story status hasn't updated**
   - Story still shows "In Development" instead of "Dev Complete"
   - Status file timestamp is older than expected

4. **No git commit of story file**
   - Story file not committed to branch
   - Git log shows no recent commit for this story

5. **Phase state file timestamp mismatch**
   - `devforgeai/workflows/STORY-XXX-phase-state.json` shows old timestamp
   - Current session is newer than last phase completion
```

### Task 2: User Recovery Command Section
Add after User Detection Indicators:
```markdown
## User Recovery Command

When you detect an interrupted workflow, resume it with:

```
Continue /dev workflow for STORY-XXX from Phase Y

Pending phases: Phase Y, Phase Y+1, ... Phase 10

Resume execution now: /dev STORY-XXX --resume
```

The `--resume` flag tells Claude to:
1. Check which phases were completed
2. Skip already-completed phases
3. Continue from first pending phase
4. Complete remaining phases in sequence
```

### Task 3: Claude Resumption Steps Section
Consolidate existing scattered steps:
```markdown
## Claude Resumption Steps

When a user runs `/dev STORY-XXX --resume`, Claude follows these steps:

1. **Check TodoWrite State**
   - Read TodoWrite list to identify completed phases
   - Determine which phases have "completed" status

2. **Verify Previous Phases**
   - Load phase-state.json to see completion evidence
   - Confirm no Critical/High violations from previous phases

3. **Load Phase Reference**
   - Read the next pending phase file from `phases/` directory
   - Load subagent documentation for that phase

4. **Execute Remaining Phases**
   - Execute phases from pending phase through Phase 10
   - Mark each phase "completed" after exit gate passes

5. **Final Validation**
   - Verify all 10 phases have "completed" status
   - Confirm story status updated to "Dev Complete"
   - Update DoD checklist completion percentage

6. **Record Resumption**
   - Add changelog entry: "resumed from Phase N"
   - Commit resumption record (if applicable)
```

### Task 4: Resumption Validation Checklist
Add after Claude Resumption Steps:
```markdown
## Resumption Pre-Flight Checklist

Before resuming your workflow, verify:

- [ ] You confirmed resumption was intentional
- [ ] Previous phases have completion evidence in phase-state.json
- [ ] No conflicting git changes (clean working directory or stashed)
- [ ] Story file exists and is readable
- [ ] Phase state file is not corrupted
- [ ] Phase state file last_iteration_date is reasonable
- [ ] All dependencies (packages, tools) still available
```

### Task 5: Fresh Start vs Resume Decision Matrix
Add after Resumption Validation Checklist:
```markdown
## Fresh Start vs Resume Decision Matrix

Use this matrix to decide whether to resume or start fresh:

| Scenario | Condition | Recommendation |
|----------|-----------|-----------------|
| Clean interruption | All previous phases completed, no conflicts, state clear | **Resume** |
| Partial completion | Some phases done, clear what's pending | **Resume to Phase N+1** |
| Phase state corrupted | phase-state.json is invalid or incomplete | **Start fresh** |
| Git conflicts | Conflicting changes detected, unclear merged state | **Start fresh** |
| Unclear state | Can't determine which phases completed | **Start fresh** |
| Long time elapsed | Last phase completed >24 hours ago | **Review before resume** |

**When in doubt, start fresh.** It's safer to rerun all phases than to resume in an unclear state.
```

---

## Test Execution Examples

### Running All Tests
```bash
$ ./tests/STORY-209-phase-resumption-protocol-tests.sh

STORY-209: Phase Resumption Protocol Documentation Tests

Target file: .claude/skills/devforgeai-development/SKILL.md

[✓] Target file exists

AC#1: User Detection Indicators Documented
================================================

[TEST] AC#1.1: Section 'User Detection Indicators' exists
[✗ FAIL]: Section header not found

[TEST] AC#1.2: TodoWrite pending/in_progress documented
[✓ PASS]: TodoWrite pending/in_progress indicator documented

...

TEST SUMMARY
================================================

Tests run:     25
Tests passed:  13
Tests failed:  12
```

### Running Specific AC Tests
```bash
# Filter to AC#1 tests
grep "AC#1" tests/STORY-209-phase-resumption-protocol-tests.sh | head -20

# Count total tests
grep -c "test_start" tests/STORY-209-phase-resumption-protocol-tests.sh
# Output: 25
```

---

## Test Implementation Details

### Test Framework
- **Language**: Bash (shell scripting)
- **Pattern matching**: Grep with case-insensitive regex
- **No external dependencies**: Uses only standard Unix utilities
- **WSL compatible**: LF line endings (per tech-stack.md)

### Test Pattern Examples

```bash
# Check if section header exists
grep -qiE "^(#{1,4}) .*(User Detection Indicators)" "$TARGET_FILE"

# Check if pattern exists (case-insensitive)
grep -qi "TodoWrite.*pending\|in_progress" "$TARGET_FILE"

# Count matching lines
grep -c "^[[:space:]]*[0-9]\." "$TARGET_FILE"
```

### Helper Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `test_start()` | Mark test as started | `test_start "AC#1.1: Section exists"` |
| `test_pass()` | Record passing test | `test_pass "Test name"` |
| `test_fail()` | Record failing test with reason | `test_fail "Test name" "Reason"` |
| `section_exists()` | Check section header | `section_exists "User Detection" "$FILE"` |
| `contains_pattern()` | Case-insensitive grep | `contains_pattern "pattern" "$FILE"` |
| `contains_text()` | Case-sensitive grep | `contains_text "exact text" "$FILE"` |
| `count_matches()` | Count matching lines | `count_matches "pattern" "$FILE"` |

---

## TDD Workflow Alignment

### Phase 1: Red (Complete ✓)
- Tests written to define requirements
- Tests fail because features don't exist yet
- Provides clear feedback on what to implement

**Checkpoint**: All tests run successfully with expected failures

### Phase 2: Green (Next)
- Implement documentation sections in SKILL.md
- Run tests after each implementation
- Stop when all 25 tests pass

**Checkpoint**: All 25 tests passing

### Phase 3: Refactor (Optional)
- Improve documentation clarity
- Add examples and cross-references
- Keep tests passing throughout

**Checkpoint**: Tests still pass, documentation is better

---

## Test Metrics

```
Test Statistics:
  Total tests:        25
  Tests per AC:       3-7 (avg 5)
  Initial pass rate:  52% (13/25)
  Initial fail rate:  48% (12/25)

Failure Analysis by AC:
  AC#1 (Detection):     40% pass (2/5 passing)
  AC#2 (Command):       25% pass (1/4 passing)
  AC#3 (Steps):         86% pass (6/7 passing)
  AC#4 (Checklist):     60% pass (3/5 passing)
  AC#5 (Decision):      25% pass (1/4 passing)

Coverage:
  Section headers:      5 needed (3 exist)
  Content indicators:   15 patterns (10 exist)
  Structure validation: 5 format checks (4 exist)
```

---

## Anti-Patterns & Quality Assurance

### Anti-Patterns Avoided
✓ No narrative text matching (uses structural validation)
✓ No hardcoded line numbers (pattern-based detection)
✓ No brittle regex (case-insensitive matching)
✓ No test interdependencies (all tests independent)

### Quality Assurance
✓ Each test has descriptive name and failure reason
✓ Tests are independent (no execution order dependency)
✓ All 5 AC thoroughly covered (3-7 tests each)
✓ Clear guidance provided on failures
✓ Exit codes properly set (0 = pass, 1 = fail)

---

## Troubleshooting

### Tests Not Running
```bash
# Ensure file is executable
chmod +x tests/STORY-209-phase-resumption-protocol-tests.sh

# Check target file exists
test -f .claude/skills/devforgeai-development/SKILL.md && echo "File exists"
```

### Understanding Test Failures
Each failure shows:
1. **Test name**: Which AC and requirement
2. **Reason**: Why it failed (e.g., "Section header not found")
3. **Expected pattern**: What to look for (e.g., "### User Detection Indicators")

### Adding Missing Content
The test output provides a checklist of missing sections. Follow the "Implementation Tasks" section above to add each section.

---

## References

### Story Documentation
- **Story file**: `devforgeai/specs/Stories/STORY-209-document-phase-resumption-protocol.story.md` (will be created)
- **Acceptance Criteria**: 5 total (all covered by 25 tests)

### Source Files
- **Target file**: `.claude/skills/devforgeai-development/SKILL.md`
- **Test file**: `tests/STORY-209-phase-resumption-protocol-tests.sh`
- **Plan file**: `.claude/plans/STORY-209-test-generation-plan.md`

### Framework References
- **TDD Guide**: `.claude/skills/devforgeai-development/references/tdd-patterns.md`
- **Tech Stack**: `devforgeai/specs/context/tech-stack.md` (Bash testing rules)
- **Source Tree**: `devforgeai/specs/context/source-tree.md` (test location rules)

---

## Success Criteria

Implementation is complete when:
- [x] 25 tests created and executable
- [x] Tests demonstrate TDD Red phase (12 failures)
- [ ] All 5 AC sections added to SKILL.md (Green phase)
- [ ] All 25 tests passing (Green phase checkpoint)
- [ ] Documentation is clear and complete (Refactor phase)

---

## Next Steps

### For Development Team
1. Review this README and test output
2. Proceed to TDD Green phase: implement documentation sections
3. Run tests after each section: `./tests/STORY-209-phase-resumption-protocol-tests.sh`
4. All tests should pass when complete
5. Continue to Phase 04 (Refactoring) in devforgeai-development skill workflow

### Test Maintenance
- Update patterns if section names change
- Add tests for new AC if requirements expand
- Keep test output logs for regression detection

---

## Questions?

Refer to:
- **Test output**: Run `./tests/STORY-209-phase-resumption-protocol-tests.sh` for detailed feedback
- **Implementation guide**: See "Implementation Tasks" section above
- **Plan document**: `.claude/plans/STORY-209-test-generation-plan.md` for detailed planning
- **Summary report**: `tests/STORY-209-TEST-GENERATION-SUMMARY.md` for comprehensive analysis

---

**Generated**: 2026-01-13
**Test Framework**: Bash with Grep pattern validation
**Type**: Documentation Specification Tests (TDD Red Phase)
**Status**: Ready for Green Phase Implementation
