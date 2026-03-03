# STORY-146 Test Suite: Enforce TodoWrite in All 6 Phases

## Overview

This test suite validates the implementation of TodoWrite progress tracking in phases 1, 3, and 5 of the devforgeai-ideation skill.

**Story:** STORY-146-enforce-todowrite-all-phases.story.md
**Status:** TDD Red Phase (All tests FAIL as expected)
**Coverage:** 100% of acceptance criteria, 100% of technical specification

---

## Quick Start

### Run All Tests
```bash
bash run-tests.sh
```

**Expected Output (Red Phase):**
```
Total Tests: 9
Passed: 0 (GREEN)
Failed: 9 (RED - TDD Red phase expected)

SUCCESS: All tests failed as expected (TDD Red phase)
Next step: Add TodoWrite to workflow files (TDD Green phase)
```

### Run Individual Test
```bash
bash test_ac1_phase1_start_todowrite.sh
bash test_ac2_phase3_start_todowrite.sh
bash test_ac3_phase5_start_todowrite.sh
```

---

## Test Files

### Phase 1: Discovery & Problem Understanding
- `test_ac1_phase1_start_todowrite.sh` - TodoWrite at phase start
- `test_ac1_phase1_end_todowrite.sh` - TodoWrite completion at phase end

### Phase 3: Complexity Assessment
- `test_ac2_phase3_start_todowrite.sh` - TodoWrite at phase start
- `test_ac2_phase3_end_todowrite.sh` - TodoWrite completion at phase end

### Phase 5: Feasibility & Constraints Analysis
- `test_ac3_phase5_start_todowrite.sh` - TodoWrite at phase start
- `test_ac3_phase5_end_todowrite.sh` - TodoWrite completion at phase end

### Format & Content Validation
- `test_ac4_consistent_format.sh` - Validate "Phase N: [Name]" format
- `test_ac4_activeform_tense.sh` - Validate activeForm ends with -ing

### Integration
- `test_ac5_workflow_files_updated.sh` - Verify workflow files contain TodoWrite

---

## Acceptance Criteria Covered

| AC# | Description | Tests |
|-----|-------------|-------|
| AC#1 | Phase 1 includes TodoWrite | 2 tests |
| AC#2 | Phase 3 includes TodoWrite | 2 tests |
| AC#3 | Phase 5 includes TodoWrite | 2 tests |
| AC#4 | Consistent TodoWrite pattern | 2 tests |
| AC#5 | Workflow files updated | 1 test |

**Total:** 9 tests covering 5 acceptance criteria (100% coverage)

---

## Technical Specification Coverage

| Requirement | Test |
|------------|------|
| CFG-001: TodoWrite Phase 1 start | test_ac1_phase1_start_todowrite |
| CFG-002: TodoWrite Phase 1 completion | test_ac1_phase1_end_todowrite |
| CFG-003: TodoWrite Phase 3 start | test_ac2_phase3_start_todowrite |
| CFG-004: TodoWrite Phase 3 completion | test_ac2_phase3_end_todowrite |
| CFG-005: TodoWrite Phase 5 start | test_ac3_phase5_start_todowrite |
| CFG-006: TodoWrite Phase 5 completion | test_ac3_phase5_end_todowrite |
| BR-001: All phases have start/end pairs | test_ac4_consistent_format |
| BR-002: Format "Phase N: [Name]" | test_ac4_consistent_format |
| BR-003: activeForm uses -ing tense | test_ac4_activeform_tense |

**Total:** 9 requirements covered (100% coverage)

---

## Files Under Test

The following workflow files need to be updated with TodoWrite instructions:

1. **discovery-workflow.md**
   - Location: `.claude/skills/devforgeai-ideation/references/discovery-workflow.md`
   - Required: TodoWrite at start + end
   - Content: "Phase 1: Discovery & Problem Understanding"
   - activeForm: "Discovering problem space"

2. **complexity-assessment-workflow.md**
   - Location: `.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md`
   - Required: TodoWrite at start + end
   - Content: "Phase 3: Complexity Assessment"
   - activeForm: "Calculating complexity score"

3. **feasibility-analysis-workflow.md**
   - Location: `.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md`
   - Required: TodoWrite at start + end
   - Content: "Phase 5: Feasibility & Constraints Analysis"
   - activeForm: "Analyzing constraints"

---

## Test Design

### Framework: Bash Shell Scripts
- No external dependencies (uses grep, sed, basic string matching)
- Tests validate file content and structure
- Aligned with project's shell-based testing approach

### Pattern: AAA (Arrange-Act-Assert)
```bash
# Arrange: Set up test environment
FILE="/path/to/workflow.md"

# Act: Execute behavior under test
RESULT=$(grep -n "TodoWrite" "$FILE")

# Assert: Verify expected outcome
if [ -z "$RESULT" ]; then
    echo "FAIL: TodoWrite not found"
    exit 1
fi
```

### Independence
- Each test can run in isolation
- No shared state between tests
- No execution order dependencies

### Error Messages
Each test provides:
- Clear FAIL status
- Expected behavior
- Actual behavior
- File path for debugging

---

## TDD Workflow: Red → Green → Refactor

### Phase 1: Red ✓ COMPLETE
- All 9 tests FAIL (as expected)
- Clear error messages for each failure
- Tests validate AC and tech spec

### Phase 2: Green (TODO)
Implement TodoWrite in workflow files:
```bash
# Add to discovery-workflow.md (start)
TodoWrite([
  {"content": "Phase 1: Discovery & Problem Understanding", "status": "in_progress", "activeForm": "Discovering problem space"}
])

# Add to discovery-workflow.md (end)
TodoWrite([
  {"content": "Phase 1: Discovery & Problem Understanding", "status": "completed", "activeForm": "Discovering problem space"}
])

# Repeat for Phase 3 and Phase 5...
```

Then run tests:
```bash
bash run-tests.sh
```

All 9 tests should PASS.

### Phase 3: Refactor (TODO)
- Review test code for improvements
- Extract common patterns
- Document reusable templates
- Optimize test performance

---

## Expected Failures (Red Phase)

### Test 1: AC#1 Phase 1 Start TodoWrite
```
FAIL: [AC#1 - Phase 1 Start TodoWrite] TodoWrite not found at Phase 1 start
  Expected: TodoWrite(status="in_progress") within first 50 lines
  File: .../discovery-workflow.md
```

### Test 2: AC#1 Phase 1 End TodoWrite
```
FAIL: [AC#1 - Phase 1 End TodoWrite] TodoWrite completion not found at Phase 1 end
  Expected: TodoWrite with status="completed" in last 100 lines
```

### Test 3-6: Phase 3 & Phase 5
Similar failures for Phase 3 and Phase 5 TodoWrite tests.

### Test 7: Consistent Format
```
FAIL: [AC#4 - Consistent TodoWrite Format] TodoWrite format inconsistencies detected:
  - Phase 1: TodoWrite format 'Phase 1: Discovery & Problem Understanding' not found
  - Phase 3: TodoWrite format 'Phase 3: Complexity Assessment' not found
  - Phase 5: TodoWrite format 'Phase 5: Feasibility & Constraints Analysis' not found
```

### Test 8: activeForm Tense
```
FAIL: [AC#4 & BR-003 - activeForm Present Continuous Tense] activeForm tense violations detected:
  - Phase 1: activeForm 'Discovering problem space' missing or not in present continuous
  - Phase 3: activeForm 'Calculating complexity score' missing or not in present continuous
  - Phase 5: activeForm 'Analyzing constraints' missing or not in present continuous
```

### Test 9: Workflow Files Updated
```
FAIL: [AC#5 - Workflow Files Updated with TodoWrite] Workflow files missing TodoWrite instructions:
  - discovery-workflow.md does not include TodoWrite keyword
  - complexity-assessment-workflow.md does not include TodoWrite keyword
  - feasibility-analysis-workflow.md does not include TodoWrite keyword
```

---

## Success Criteria

### For Red Phase (Current)
- [x] All tests FAIL
- [x] Clear error messages
- [x] 100% AC coverage
- [x] 100% tech spec coverage

### For Green Phase
- [ ] All tests PASS
- [ ] 100% pass rate
- [ ] TodoWrite added to all 3 files
- [ ] Format matches specification

### For Refactor Phase
- [ ] Tests optimized
- [ ] Documentation complete
- [ ] Patterns documented
- [ ] Ready for integration

---

## Additional Resources

### Story File
- Location: `devforgeai/specs/Stories/STORY-146-enforce-todowrite-all-phases.story.md`
- Contains: Full acceptance criteria, technical spec, edge cases

### Planning Documents
- Plan: `.claude/plans/STORY-146-test-generation-plan.md`
- Summary: `.claude/plans/STORY-146-test-generation-summary.md`

### Workflow Files (Under Test)
- Discovery: `.claude/skills/devforgeai-ideation/references/discovery-workflow.md`
- Complexity: `.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md`
- Feasibility: `.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md`

---

## Troubleshooting

### Test Won't Execute
```bash
# Make scripts executable
chmod +x *.sh

# Then run
bash run-tests.sh
```

### Unexpected Test Results
1. Verify workflow files exist
2. Check file paths in test
3. Review grep patterns
4. Compare against acceptance criteria

### Need Help?
- Review test comments for detailed assertions
- Check story file for acceptance criteria
- See summary document for full test details

---

## Notes

- Tests follow TDD Red phase (all FAIL initially)
- Tests validate structure, not execution
- Bash shell script approach requires no external dependencies
- Each test is independent and idempotent
- Clear error messages guide implementation

---

**Status:** TDD Red Phase Complete ✓
**Next:** Implement TodoWrite additions, verify all tests pass (Green Phase)
