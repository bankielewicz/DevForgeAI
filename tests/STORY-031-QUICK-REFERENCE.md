# STORY-031 Integration Tests - Quick Reference

## Test File Location

```
tests/integration/test_story_031_ideate_hooks_integration.py
```

**Stats:** 34 tests, 8 test classes, 1,100+ lines, AAA pattern

## Quick Start

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all STORY-031 tests
pytest tests/integration/test_story_031_ideate_hooks_integration.py -v

# Expected: All 34 tests FAIL (Red Phase - tests written before implementation)
```

### Run Specific Test Classes

```bash
# Hook eligibility check logic (5 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestHookEligibilityCheck -v

# Hook invocation conditional logic (4 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestHookInvocationLogic -v

# Full command integration (10 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateWithHooksIntegration -v

# Edge cases (5 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksEdgeCases -v

# Context passing (4 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateContextPassing -v

# Performance (2 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksPerformance -v

# Pattern consistency (3 tests)
pytest tests/integration/test_story_031_ideate_hooks_integration.py::TestIdeateHooksPatternConsistency -v
```

### Run by Marker

```bash
# Run all STORY-031 tests via marker
pytest -m story_031 -v
```

## Test Coverage Breakdown

| Coverage | Tests |
|----------|-------|
| **AC1** - Hook Eligibility Check | 5 tests |
| **AC2** - Feedback Invocation | 4 tests |
| **AC3** - Graceful Degradation | 5 tests |
| **AC4** - Context Awareness | 5 tests |
| **AC5** - Pattern Consistency | 3 tests |
| **Edge Cases** | 5 tests |
| **Performance** | 2 tests |
| **Reliability** | 1 test |
| **Pattern Validation** | 3 tests |
| **TOTAL** | **34 tests** |

## Test Execution with Output

### Verbose Output

```bash
pytest tests/integration/test_story_031_ideate_hooks_integration.py -v --tb=short
```

### With Code Coverage

```bash
pytest tests/integration/test_story_031_ideate_hooks_integration.py --cov=.claude/commands --cov-report=term
```

## Performance Expectations

| Phase | Duration |
|-------|----------|
| **Unit Tests** | ~100ms |
| **Integration Tests** | ~500ms |
| **Edge Cases** | ~200ms |
| **Context Tests** | ~100ms |
| **Performance Tests** | ~2s |
| **Reliability Tests** | ~500ms |
| **Pattern Tests** | ~50ms |
| **TOTAL SUITE** | ~5-10s |

## Success Criteria

### Red Phase (Current)
- ✓ All 34 tests written
- ✓ All tests FAIL (not yet implemented)
- ✓ Syntax valid

### Green Phase (After Implementation)
- ✓ All 34 tests PASS
- ✓ Coverage >95%

## References

**Story File:**
- `.ai_docs/Stories/STORY-031-wire-hooks-into-ideate-command.story.md`

**Command to Implement:**
- `.claude/commands/ideate.md` (Phase N)

**Detailed Summary:**
- `tests/STORY-031-TEST-SUITE-SUMMARY.md`

---

**Status:** Red Phase (Ready for Implementation)
**Date:** 2025-11-17
