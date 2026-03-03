# STORY-166 Test Suite - AC Header Documentation Clarification

## Overview

This test suite validates that CLAUDE.md contains proper documentation explaining:
- AC headers are definitions, not progress trackers
- Why AC headers are never marked complete
- Where to find actual completion status (Definition of Done)
- Guidance for older stories with vestigial checkbox format

## Test Status: RED (All Failing)

All tests intentionally FAIL because the required documentation content does not yet exist in CLAUDE.md.

This is the expected **Red Phase** of Test-Driven Development (TDD).

## Test Files

| Test | AC | Purpose |
|------|-----|---------|
| `test-ac1-claude-md-header-clarification.sh` | AC#1 | Validate AC header clarification section exists |
| `test-ac2-comparison-table.sh` | AC#2 | Validate comparison table with 3 rows |
| `test-ac3-historical-story-guidance.sh` | AC#3 | Validate historical story guidance exists |

## Quick Start

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run individual tests
bash tests/STORY-166/test-ac1-claude-md-header-clarification.sh
bash tests/STORY-166/test-ac2-comparison-table.sh
bash tests/STORY-166/test-ac3-historical-story-guidance.sh

# Run all tests with summary
for test in tests/STORY-166/test-*.sh; do
    bash "$test" && echo "✓ ${test##*/}" || echo "✗ ${test##*/}"
done
```

### Run With Exit Code Checking
```bash
# Individual test with explicit failure check
bash tests/STORY-166/test-ac1-claude-md-header-clarification.sh
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "Test passed"
else
    echo "Test failed with exit code $EXIT_CODE"
fi
```

## Expected Test Output (RED Phase)

```
Running: AC#1: CLAUDE.md Updated with AC Header Clarification
===========================================

✓ PASS: CLAUDE.md file exists
✗ FAIL: CLAUDE.md does not contain section explaining AC headers vs tracking
Expected section title containing: 'Acceptance Criteria' and 'Tracking Mechanisms'
```

Exit code: **1** (failure)

This is EXPECTED and CORRECT for the Red phase.

## Test Requirements

### AC#1: Header Clarification
Tests that CLAUDE.md contains:
1. Section explaining AC headers vs. tracking mechanisms
2. Statement that AC headers are definitions, not trackers
3. Explanation why AC headers are never marked complete
4. Reference to Definition of Done (DoD) as completion tracker

### AC#2: Comparison Table
Tests that CLAUDE.md includes a table with:

```markdown
| Element | Purpose | Checkbox Behavior |
|---------|---------|-------------------|
| AC Headers | Define what to test | Never marked complete |
| AC Checklist | Track progress | Marked during TDD |
| Definition of Done | Official record | Marked in Phase 4.5-5 Bridge |
```

### AC#3: Historical Story Guidance
Tests that CLAUDE.md documents:
1. Older stories (template v2.0) may have `### 1. [ ]` format
2. These checkboxes are vestigial (not meant to be checked)
3. Guidance to look at DoD section for actual completion status

## Implementation Guidelines

To make tests pass (Green phase), add to CLAUDE.md:

```markdown
### Acceptance Criteria vs. Tracking Mechanisms

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**:

| Element | Purpose | Checkbox Behavior |
|---------|---------|-------------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable) | **Never marked complete** |
| **AC Verification Checklist** | **Track granular progress** (real-time) | Marked complete during TDD phases |
| **Definition of Done** | **Official completion record** (quality gate) | Marked complete in Phase 4.5-5 Bridge |

**Why AC headers have no checkboxes (as of template v2.1):**
- AC headers are **specifications**, not **progress trackers**
- Marking them "complete" would imply AC is no longer relevant (incorrect)
- Progress tracking happens in AC Checklist (granular) and DoD (official)

**For older stories (template v2.0 and earlier):**
- AC headers may show `### 1. [ ]` checkbox syntax (vestigial)
- These checkboxes are **never meant to be checked**
- Look at DoD section for actual completion status
```

## Test Architecture

### How Tests Work

Tests use **pattern matching** with grep to search CLAUDE.md for:
1. Key concepts (not exact text)
2. Case-insensitive patterns
3. Multiple valid phrasings

### Why Pattern Matching

- **Flexible:** Accommodates different wording
- **Intent-based:** Validates concepts, not exact text
- **Maintainable:** Easy to update patterns
- **Fast:** Simple pattern matching with no dependencies

### Example Pattern
```bash
# Test AC headers are definitions
if ! grep -iq "ac.*headers.*definitions\|definitions.*not.*trackers" "$CLAUDE_MD_PATH"; then
    echo "FAIL: Content not found"
    exit 1
fi
```

## Test Independence

- Each test runs independently
- No shared state or dependencies
- No execution order requirements
- Can run tests in any order

## Debugging

### If Tests Fail (Expected in Red Phase)

1. **Check CLAUDE.md exists**
   ```bash
   ls -la CLAUDE.md
   ```

2. **Search for partial matches**
   ```bash
   grep -i "acceptance criteria" CLAUDE.md
   grep -i "definition of done" CLAUDE.md
   ```

3. **View exact test checks**
   ```bash
   cat tests/STORY-166/test-ac1-claude-md-header-clarification.sh
   ```

### Common Issues

**Issue:** "CLAUDE.md not found"
- Solution: Ensure working directory is project root

**Issue:** "Section not found" (expected in Red phase)
- Solution: Implement documentation to make tests pass

## Test Metrics

| Metric | Value |
|--------|-------|
| Total Test Files | 3 |
| Total Test Cases | 16 |
| Total Assertions | 16 |
| Status | All Failing (RED) |
| Estimated Pass Time | 1-2 hours (implementation) |

## Next Steps

### Phase 2: Green (Make Tests Pass)

1. **Add AC Header Clarification section to CLAUDE.md**
   - Tests 1-5 in test-ac1 should pass

2. **Add Comparison Table to CLAUDE.md**
   - Tests 2-6 in test-ac2 should pass

3. **Add Historical Story Guidance to CLAUDE.md**
   - Tests 2-5 in test-ac3 should pass

### Validation Command

After implementing changes, run tests again:
```bash
bash tests/STORY-166/test-ac1-claude-md-header-clarification.sh && \
bash tests/STORY-166/test-ac2-comparison-table.sh && \
bash tests/STORY-166/test-ac3-historical-story-guidance.sh && \
echo "All tests passed!"
```

All 3 tests should exit with code 0 (success).

## References

- **Story File:** `devforgeai/specs/Stories/STORY-166-rca-012-ac-header-documentation.story.md`
- **Test Generation Report:** `/mnt/c/Projects/DevForgeAI2/STORY-166-TEST-GENERATION-REPORT.md`
- **Tech Stack:** `devforgeai/specs/context/tech-stack.md`
- **RCA Source:** `devforgeai/RCA/RCA-012/ANALYSIS.md` (REC-2)

## Test Execution Checklist

- [x] Tests created
- [x] Tests failing (RED state)
- [x] Failure messages clear
- [x] Test independence verified
- [ ] Tests passing (GREEN state - to do after implementation)
- [ ] Tests refactored (REFACTOR state - optional)

## Contact & Questions

For questions about tests, refer to:
- Test file comments for specific test details
- STORY-166-TEST-GENERATION-REPORT.md for comprehensive overview
- CLAUDE.md Story Progress Tracking section (to be implemented)

---

**TDD Phase:** Red (All tests failing - expected)
**Next Phase:** Green (Implement CLAUDE.md content)
**Story ID:** STORY-166
**Created:** 2025-01-03
