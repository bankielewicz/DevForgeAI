# STORY-146 Test Generation Plan

**Status:** In Progress
**Story ID:** STORY-146
**Title:** Enforce TodoWrite in All 6 Phases
**Created:** 2025-12-29

---

## Objective

Generate comprehensive failing test suite (TDD Red phase) to validate TodoWrite integration in discovering-requirements workflow files:
- discovery-workflow.md (Phase 1)
- complexity-assessment-workflow.md (Phase 3)
- feasibility-analysis-workflow.md (Phase 5)

---

## Test Scope Analysis

### Files Under Test
1. `.claude/skills/discovering-requirements/references/discovery-workflow.md`
2. `.claude/skills/discovering-requirements/references/complexity-assessment-workflow.md`
3. `.claude/skills/discovering-requirements/references/feasibility-analysis-workflow.md`

### Acceptance Criteria Mapped to Test Cases

| AC# | Requirement | Test Case | Expected File Pattern |
|-----|-------------|-----------|----------------------|
| AC#1 | Phase 1 start TodoWrite | test_ac1_phase1_start_todowrite | Contains `TodoWrite.*Phase 1` at start |
| AC#1 | Phase 1 end TodoWrite | test_ac1_phase1_end_todowrite | Contains `TodoWrite.*completed` at end |
| AC#2 | Phase 3 start TodoWrite | test_ac2_phase3_start_todowrite | Contains `TodoWrite.*Phase 3` at start |
| AC#2 | Phase 3 end TodoWrite | test_ac2_phase3_end_todowrite | Contains `TodoWrite.*complexity score` at end |
| AC#3 | Phase 5 start TodoWrite | test_ac3_phase5_start_todowrite | Contains `TodoWrite.*Phase 5` at start |
| AC#3 | Phase 5 end TodoWrite | test_ac3_phase5_end_todowrite | Contains `TodoWrite.*completed` at end |
| AC#4 | Consistent format | test_ac4_consistent_format | All TodoWrite follow "Phase N: [Name]" |
| AC#5 | activeForm tense | test_ac4_activeform_tense | All activeForm end with "-ing" |

### Technical Specification Coverage

| Requirement | Test Coverage |
|-------------|--------------|
| CFG-001: TodoWrite Phase 1 start | test_ac1_phase1_start_todowrite |
| CFG-002: TodoWrite Phase 1 completion | test_ac1_phase1_end_todowrite |
| CFG-003: TodoWrite Phase 3 start | test_ac2_phase3_start_todowrite |
| CFG-004: TodoWrite Phase 3 completion | test_ac2_phase3_end_todowrite |
| CFG-005: TodoWrite Phase 5 start | test_ac3_phase5_start_todowrite |
| CFG-006: TodoWrite Phase 5 completion | test_ac3_phase5_end_todowrite |
| BR-001: All phases have start/end pairs | test_ac4_all_phases_paired |
| BR-002: Format "Phase N: [Name]" | test_ac4_consistent_format |
| BR-003: activeForm uses -ing tense | test_ac4_activeform_tense |

---

## Test Framework Decision

**Decision:** Bash shell scripts (`.sh`)
**Rationale:** Project uses shell-based testing for documentation validation (markdown/YAML inspection)
**Location:** `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-146/`
**Naming:** `test_ac{N}_{scenario}.sh`

---

## Test Strategy (TDD Red Phase)

### Phase 1: Write Failing Tests
- All tests WILL FAIL initially (no implementation yet)
- Tests validate file content structure using `grep`
- Tests verify TodoWrite patterns, format, content

### Phase 2: Implementation (Green Phase)
- Add TodoWrite calls to workflow files
- Update discovery-workflow.md
- Update complexity-assessment-workflow.md
- Update feasibility-analysis-workflow.md
- Implementation happens AFTER tests pass validation

### Phase 3: Refactoring & Validation
- Ensure all tests pass (100% pass rate)
- Verify test naming clarity
- Document any limitations

---

## Test Structure (Bash Shell Pattern)

All tests follow AAA pattern:

```bash
#!/bin/bash

# Test: [AC#] [Scenario]
# Validates: [Specific requirement]

# Arrange
DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/discovering-requirements/references/discovery-workflow.md"

# Act
RESULT=$(grep -n "TodoWrite.*Phase 1" "$DISCOVERY_FILE" | head -1)

# Assert
if [ -z "$RESULT" ]; then
    echo "FAIL: TodoWrite Phase 1 start not found"
    exit 1
fi

echo "PASS: TodoWrite Phase 1 start found at line: $(echo $RESULT | cut -d: -f1)"
exit 0
```

---

## Test Files to Create

### File 1: test_ac1_phase1_todowrite_start.sh
Tests AC#1: Phase 1 (Discovery) includes TodoWrite at start

**Assertions:**
- File contains TodoWrite with status "in_progress"
- Content matches "Phase 1: Discovery & Problem Understanding"
- activeForm contains "Discovering problem space"
- Found within first 100 lines (start of file)

### File 2: test_ac1_phase1_todowrite_end.sh
Tests AC#1: Phase 1 includes TodoWrite at end

**Assertions:**
- File contains TodoWrite with status "completed"
- Content matches "Phase 1: Discovery & Problem Understanding"
- Found near end of file

### File 3: test_ac2_phase3_todowrite_start.sh
Tests AC#2: Phase 3 (Complexity Assessment) includes TodoWrite at start

**Assertions:**
- File contains TodoWrite with status "in_progress"
- Content matches "Phase 3: Complexity Assessment"
- activeForm contains "Calculating complexity score"
- Found within first 100 lines (start of file)

### File 4: test_ac2_phase3_todowrite_end.sh
Tests AC#2: Phase 3 includes TodoWrite with complexity score at end

**Assertions:**
- File contains TodoWrite with status "completed"
- Content matches "Phase 3: Complexity Assessment"
- activeForm contains "complexity score"

### File 5: test_ac3_phase5_todowrite_start.sh
Tests AC#3: Phase 5 (Feasibility) includes TodoWrite at start

**Assertions:**
- File contains TodoWrite with status "in_progress"
- Content matches "Phase 5: Feasibility & Constraints Analysis"
- activeForm contains "Analyzing constraints"
- Found within first 100 lines (start of file)

### File 6: test_ac3_phase5_todowrite_end.sh
Tests AC#3: Phase 5 includes TodoWrite at end

**Assertions:**
- File contains TodoWrite with status "completed"
- Content matches "Phase 5: Feasibility & Constraints Analysis"

### File 7: test_ac4_consistent_format.sh
Tests AC#4: All phases use consistent format "Phase N: [Name]"

**Assertions:**
- Validates format across all 3 workflow files
- Counts occurrences of "Phase N:" pattern
- Verifies consistency with other phases (2, 4, 6)

### File 8: test_ac4_activeform_tense.sh
Tests AC#4 & BR-003: activeForm uses present continuous (-ing) tense

**Assertions:**
- All activeForm values end with "-ing"
- No exceptions found
- Validates pattern across all TodoWrite instances

### File 9: test_ac5_workflow_files_updated.sh
Tests AC#5: Workflow files include TodoWrite instructions

**Assertions:**
- discovery-workflow.md includes TodoWrite
- complexity-assessment-workflow.md includes TodoWrite
- feasibility-analysis-workflow.md includes TodoWrite
- All three files contain TodoWrite keyword

---

## Progress Tracking

- [x] Story analysis
- [x] Test scope definition
- [x] Test structure planning
- [ ] Test file generation (Phase 1)
- [ ] Test file validation (Phase 2)
- [ ] Implementation (Phase 3)
- [ ] Test execution (Phase 4)
- [ ] Coverage validation (Phase 5)

---

## Success Criteria

**All tests MUST fail initially (TDD Red phase):**
- [ ] 9 test files created in `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-146/`
- [ ] All tests fail with clear error messages
- [ ] All tests follow consistent naming: `test_ac{N}_{scenario}.sh`
- [ ] All tests use grep/sed for content validation
- [ ] All tests output "PASS" or "FAIL" with reason
- [ ] All tests are executable (chmod +x)
- [ ] All tests follow AAA pattern

---

## References

- Story: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-146-enforce-todowrite-all-phases.story.md`
- Test framework: Bash shell (`grep`, `sed`, basic string matching)
- Target directory: `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-146/`
- Workflow files: `.claude/skills/discovering-requirements/references/`

---

## Notes

- Tests validate **file structure and content**, not execution behavior
- Phase 2 (Green) will add TodoWrite calls to make tests pass
- No external dependencies required (Bash + core Unix tools)
- Tests are idempotent (can run multiple times without side effects)
