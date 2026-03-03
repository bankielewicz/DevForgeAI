# STORY-121: Test Suite - Quick Start

## TDD RED Phase - Tests Ready for Execution

**Total Tests**: 11 (4 unit + 4 integration + 3 edge case)
**Status**: All FAILING (as expected for RED phase)
**Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-121/`

---

## Quick Commands

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2/tests/STORY-121
bash run_all_tests.sh
```

### Expected Output (RED Phase)
```
═════════════════════════════════════════════════════════════════
STORY-121: Story-Scoped Pre-Commit Validation - Test Suite
═════════════════════════════════════════════════════════════════

Status: TDD RED PHASE - Tests expected to FAIL

[... 11 tests run ...]

Test Summary:
  Total:   11
  Passed:  0
  Failed:  11
  Skipped: 0

TDD RED PHASE: Implementation required to make tests pass
```

---

## Test Structure

### Unit Tests (4)
- `test_scoped_filtering.sh` - Hook filters when DEVFORGEAI_STORY set
- `test_unscoped_fallback.sh` - Fallback validates all when unset
- `test_scoped_message.sh` - Shows "Scoped to:" message
- `test_unscoped_message.sh` - No message in unscoped mode

### Integration Tests (4)
- `test_scoped_commit_blocks_other.sh` - Scoped allows other errors
- `test_unscoped_blocks_all.sh` - Unscoped blocks all errors
- `test_multiple_stories_scoped.sh` - Multi-story filtering
- `test_explicit_story_id.sh` - Explicit ID scoping

### Edge Cases (3)
- `test_invalid_format.sh` - Invalid format handling
- `test_empty_env_var.sh` - Empty variable behavior
- `test_case_sensitivity.sh` - Case sensitivity

---

## Implementation Checklist

These tests verify implementation of:

- [ ] Pre-commit hook scoping logic (`.git/hooks/pre-commit` lines 44-58)
- [ ] Hook template update (`src/claude/scripts/install_hooks.sh`)
- [ ] Documentation file (`devforgeai/docs/STORY-SCOPED-COMMITS.md`)

---

## Key Test Assertions

Each test verifies specific aspects:

**Scoped Mode** (`[ -n "$DEVFORGEAI_STORY" ]`)
- Hook contains conditional check for environment variable
- Grep filters files by story ID: `grep "${DEVFORGEAI_STORY}"`
- Console output shows: `"Scoped to: STORY-120"`
- Only target story validated

**Unscoped Mode** (variable unset/empty)
- Hook has else block for fallback
- Grep filters by pattern: `grep '\.story\.md$'`
- No "Scoped to:" message displayed
- All .story.md files validated

**Edge Cases**
- Invalid formats handled gracefully
- Empty variable defaults to unscoped
- Case sensitivity respected

---

## Documentation Files

- **TEST-SUITE-README.md** - Complete test documentation
- **EXECUTION-SUMMARY.md** - Detailed implementation roadmap
- **QUICK-START.md** - This file

---

## Next Phase: GREEN

After implementation, tests should:

1. All 11 tests PASS ✓
2. Pre-commit hook respects `DEVFORGEAI_STORY`
3. Backward compatibility maintained
4. Clear scoping messages displayed

---

**Ready to execute!** Run `bash run_all_tests.sh` to start RED phase validation.
