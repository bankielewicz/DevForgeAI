# STORY-158: RCA-Story Linking - Test Generation Plan

**Status**: In Progress (Phase 02 - Test-First Design)
**Created**: 2025-12-31
**Story ID**: STORY-158
**Depends on**: STORY-157 (QA Approved)

---

## Objective

Generate failing tests for STORY-158: RCA-Story Linking feature that updates RCA documents with created story references.

---

## Test Generation Scope

### Acceptance Criteria to Test
- **AC#1**: Update RCA Implementation Checklist with Story References
  - Format: `- [ ] REC-1: See STORY-155`
- **AC#2**: Add Story ID to Recommendation Sections
  - Format: `**Implemented in:** STORY-NNN` after recommendation header
- **AC#3**: Preserve Original RCA Content
  - All original content (5 Whys, evidence) preserved unchanged
- **AC#4**: Handle Partial Story Creation
  - Only link successfully created stories; failures remain unmarked
- **AC#5**: Update RCA Status Field
  - Status changes to "IN_PROGRESS" when all recommendations have stories

### Business Rules to Test
- **BR-001**: Traceability - Every created story must be linked back to source RCA
- **BR-002**: Idempotency - Re-running does not duplicate links
- **BR-003**: Status Transition - RCA status changes only when all recommendations have stories

---

## Test Files to Create

```
tests/results/STORY-158/
├── fixtures/
│   └── sample-rca.md                          # Test RCA document with recommendations
├── test-ac1-implementation-checklist.sh       # AC#1: Checklist update with story refs
├── test-ac2-inline-story-reference.sh         # AC#2: Inline recommendation updates
├── test-ac3-content-preservation.sh           # AC#3: Original content not lost
├── test-ac4-partial-creation.sh               # AC#4: Handle partial creation
├── test-ac5-status-update.sh                  # AC#5: Status field changes correctly
└── test-br002-idempotency.sh                  # BR-002: Idempotent re-running
```

**Total Files**: 7 (1 fixture + 6 test scripts)

---

## Test Design Strategy

### Test Framework
- **Language**: Bash (aligned with STORY-157 pattern)
- **Pattern**: Given/When/Then scenario tests
- **Assertion Method**: File content comparison using `grep`, `diff`

### Sample RCA Fixture
File: `tests/results/STORY-158/fixtures/sample-rca.md`

```markdown
---
id: RCA-TEST-001
title: Test RCA Document
status: OPEN
---

# RCA-TEST-001: Test Issue

## Five Whys Analysis
1. Why: Initial reason
2. Why: Secondary reason
3. Why: Tertiary reason
...

## Evidence
- Evidence point 1
- Evidence point 2

## Recommendations

### REC-1: First Recommendation
Description of first recommendation.

### REC-2: Second Recommendation
Description of second recommendation.

### REC-3: Third Recommendation
Description of third recommendation.

## Implementation Checklist
- [ ] REC-1
- [ ] REC-2
- [ ] REC-3
```

### Test Implementation Pattern

Each test script follows Bash AAA pattern:

```bash
#!/bin/bash

# Arrange: Set up test fixtures
setup_test() {
    # Create temporary test directory
    # Copy sample RCA
    # Create story reference mapping (simulated from STORY-157)
}

# Act: Execute the RCA linking command
execute_linking() {
    # Call the RCA linking function/script
    # Capture result
}

# Assert: Verify expected outcomes
assert_results() {
    # Check file content
    # Verify no content loss
    # Validate link format
}

# Run test
setup_test
execute_linking
assert_results
```

---

## Test Specifications

### Test AC#1: Implementation Checklist Update

**Test File**: `test-ac1-implementation-checklist.sh`

**Acceptance Criteria**:
- Given: RCA has "Implementation Checklist" section with `- [ ] REC-1`, `- [ ] REC-2`
- When: Linking is executed with story map: REC-1→STORY-155, REC-2→STORY-156
- Then: Checklist is updated to `- [ ] REC-1: See STORY-155` and `- [ ] REC-2: See STORY-156`

**Assertions**:
```bash
assert_contains "- [ ] REC-1: See STORY-155"
assert_contains "- [ ] REC-2: See STORY-156"
assert_not_contains "- [ ] REC-1\$"  # Original format gone
```

### Test AC#2: Inline Story Reference

**Test File**: `test-ac2-inline-story-reference.sh`

**Acceptance Criteria**:
- Given: Recommendation section exists: `### REC-1: First Recommendation`
- When: Linking is executed with REC-1→STORY-155
- Then: Section is updated with `**Implemented in:** STORY-155` after header

**Assertions**:
```bash
assert_contains "### REC-1: First Recommendation"
assert_contains "**Implemented in:** STORY-155"
assert_regex "### REC-1:.*\n.*\*\*Implemented in:\*\*"  # Correct position
```

### Test AC#3: Content Preservation

**Test File**: `test-ac3-content-preservation.sh`

**Acceptance Criteria**:
- Given: RCA with Five Whys, Evidence, and original recommendation descriptions
- When: Linking is executed
- Then: All original content is preserved, only links are added

**Assertions**:
```bash
# Original sections must exist unchanged
assert_contains "## Five Whys Analysis"
assert_contains "## Evidence"
assert_contains "Description of first recommendation"

# File size should only increase by link additions
# No original lines should be removed
```

### Test AC#4: Partial Story Creation

**Test File**: `test-ac4-partial-creation.sh`

**Acceptance Criteria**:
- Given: RCA with REC-1, REC-2, REC-3; but only REC-1 and REC-2 have stories
- When: Linking is executed with partial story map: REC-1→STORY-155, REC-2→STORY-156
- Then: Only REC-1 and REC-2 are linked; REC-3 remains unmarked

**Assertions**:
```bash
assert_contains "- [ ] REC-1: See STORY-155"
assert_contains "- [ ] REC-2: See STORY-156"
assert_contains "- [ ] REC-3\$"  # Unchanged
assert_not_contains "STORY-"  # Only 2 stories referenced
```

### Test AC#5: Status Field Update

**Test File**: `test-ac5-status-update.sh`

**Acceptance Criteria**:
- Given: RCA with status: OPEN and all recommendations have stories assigned
- When: Linking is executed with complete story map
- Then: YAML frontmatter status field is updated to: status: IN_PROGRESS

**Assertions**:
```bash
# Before: status: OPEN
# After: status: IN_PROGRESS
assert_grep "^status: IN_PROGRESS"  # Regex check for YAML frontmatter
```

### Test BR#002: Idempotency

**Test File**: `test-br002-idempotency.sh`

**Acceptance Criteria**:
- Given: RCA with linking already applied
- When: Linking command is run again
- Then: File remains unchanged; no duplicate links added

**Assertions**:
```bash
# Run linking twice
run_linking_pass_1  # Create links
run_linking_pass_2  # Re-run

# Compare results
assert_files_identical $file_after_pass1 $file_after_pass2
assert_no_duplicates "STORY-"  # No duplicate story references
```

---

## Execution Checklist

- [x] Create `tests/results/STORY-158/` directory
- [x] Create `tests/results/STORY-158/fixtures/` directory
- [x] Write `sample-rca.md` fixture with all test scenarios
- [x] Write `test-ac1-implementation-checklist.sh` - FAILING initially
- [x] Write `test-ac2-inline-story-reference.sh` - FAILING initially
- [x] Write `test-ac3-content-preservation.sh` - FAILING initially
- [x] Write `test-ac4-partial-creation.sh` - FAILING initially
- [x] Write `test-ac5-status-update.sh` - FAILING initially
- [x] Write `test-br002-idempotency.sh` - FAILING initially
- [x] Run all tests to verify they FAIL (TDD Red phase)
- [ ] Commit test files to git (pending user approval)

---

## Success Criteria

- [ ] All 6 test scripts created and placed in `tests/results/STORY-158/`
- [ ] All tests FAIL initially (no implementation exists)
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Tests are independent (can run in any order)
- [ ] Fixture file contains realistic RCA structure
- [ ] All AC#1-5 and BR#002 are covered
- [ ] Test files are executable (chmod +x)
- [ ] Tests produce clear pass/fail messages

---

## References

**Story File**: `devforgeai/specs/Stories/STORY-158-rca-story-linking.story.md`
- AC#1: Update RCA Implementation Checklist (lines 23-27)
- AC#2: Add Story ID to Recommendation Sections (lines 29-33)
- AC#3: Preserve Original RCA Content (lines 35-39)
- AC#4: Handle Partial Story Creation (lines 41-45)
- AC#5: Update RCA Status Field (lines 47-51)
- BR#002: Idempotency (lines 86-89)

**Depends On**: STORY-157 (Batch Story Creation) - QA Approved
- Provides: Story creation results mapping recommendations to story IDs

**Technology Stack**: Bash scripts (per tech-stack.md - Framework-agnostic)
**Source Tree**: tests/results/STORY-{ID}/ pattern (per source-tree.md, line 341)

---

## Next Steps (Phase 03 - Implementation)

After tests are confirmed FAILING:
1. Implement RCA linking logic in `.claude/commands/create-stories-from-rca.md` or new command
2. Tests should PASS when implementation correctly:
   - Parses recommendation IDs from RCA
   - Maps recommendations to created story IDs
   - Updates Implementation Checklist with story references
   - Adds inline `**Implemented in:**` markers
   - Preserves all original content
   - Handles partial story creation
   - Updates YAML frontmatter status
   - Maintains idempotency

---

## Notes

- **TDD Philosophy**: Tests define the contract; implementation must satisfy test assertions
- **Test Independence**: Each test can run independently in any order
- **Bash Pattern**: Leverages standard Unix tools (grep, diff, sed) for portability
- **Fixture Reusability**: Single sample-rca.md fixture can be copied/modified for each test case
