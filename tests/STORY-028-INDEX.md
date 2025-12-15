# STORY-028: Wire Hooks Into /create-epic Command - Test Suite Index

**Story ID**: STORY-028
**Story Title**: Wire Hooks Into /create-epic Command
**Test Generation Date**: 2025-11-16
**Framework**: pytest
**Test Status**: 🔴 RED PHASE (All 72 Tests Failing)

---

## 📁 Test Files

### Unit Tests: `test_create_epic_hooks.py`
**Location**: `tests/unit/test_create_epic_hooks.py`
**Tests**: 37 unit tests
**Lines**: 1,047
**Focus**: Configuration loading, CLI mocking, validation logic

**Test Classes**:
- `TestEpicHookConfigurationLoading` (7 tests) - YAML parsing, defaults, missing files
- `TestEpicHookCLIMocking` (8 tests) - Mock devforgeai CLI responses
- `TestEpicContextValidation` (8 tests) - Epic ID validation, metadata validation, security
- `TestEpicHookPhase4A9Integration` (5 tests) - Phase 4A.9 workflow, budget compliance
- `TestEpicHookExceptionHandling` (4 tests) - Timeout, crash, graceful degradation
- `TestEpicHookMetadataExtraction` (5 tests) - Extract and use epic context

### Integration Tests: `test_create_epic_hooks_e2e.py`
**Location**: `tests/integration/test_create_epic_hooks_e2e.py`
**Tests**: 12 integration tests
**Lines**: 721
**Focus**: End-to-end workflows, CLI integration, logging

**Test Classes**:
- `TestCreateEpicHooksE2E` (8 tests) - Full workflows with and without hooks
- `TestHookCLIIntegration` (2 tests) - Real CLI interaction
- `TestCreateEpicHooksLogging` (2 tests) - Log file validation

### Performance Tests: `test_create_epic_hooks_performance.py`
**Location**: `tests/performance/test_create_epic_hooks_performance.py`
**Tests**: 23 performance tests
**Lines**: 623
**Focus**: Latency, overhead, reliability, budget

**Test Classes**:
- `TestHookCheckPerformance` (2 tests) - Hook check latency
- `TestHookOverheadPerformance` (2 tests) - Total workflow overhead
- `TestEpicCreationLatencyComparison` (3 tests) - With/without hooks latency
- `TestHookFailurePerformance` (2 tests) - Performance under failure
- `TestHookReliability` (3 tests) - Stress tests, success rate
- `TestHookBudgetCompliance` (3 tests) - Character/line budget

---

## 📚 Documentation Files

### STORY-028-TEST-GENERATION-SUMMARY.md
**Overview**: Complete test suite documentation
**Contents**:
- Test metrics (72 tests, breakdown by type)
- AC coverage matrix
- Test design patterns (AAA, mocking, fixtures)
- Running instructions
- Implementation guidance
- References

**Purpose**: Comprehensive reference for understanding test suite

### STORY-028-TEST-QUICK-REFERENCE.md
**Overview**: Quick lookup and execution guide
**Contents**:
- File manifest with test counts
- AC matrix visual
- Quick run commands
- Test class organization
- Coverage statistics
- Implementation hints

**Purpose**: Fast reference for developers during implementation

### STORY-028-TEST-VERIFICATION.md
**Overview**: QA checklist and completion verification
**Contents**:
- Input validation checklist
- AC coverage verification (all 5 ACs confirmed)
- Tech spec coverage verification
- Test quality metrics
- Framework compliance
- Sign-off checklist

**Purpose**: Verify test suite completeness and quality

### STORY-028-INDEX.md
**Overview**: This file - navigation and orientation guide
**Contents**:
- File locations and purposes
- Test count summary
- Quick execution guide
- File relationships

**Purpose**: Orient developers to test suite structure

---

## 🎯 Quick Navigation

### By Purpose

**I want to understand the overall test suite:**
→ Read: `STORY-028-TEST-GENERATION-SUMMARY.md`

**I want to run tests quickly:**
→ Read: `STORY-028-TEST-QUICK-REFERENCE.md` then execute commands

**I want to verify everything was tested:**
→ Read: `STORY-028-TEST-VERIFICATION.md`

**I need to know where files are:**
→ Read: `STORY-028-INDEX.md` (this file)

### By Acceptance Criteria

**AC1 - Automatic Hook Trigger**: 9 tests
- Unit: check-hooks mock, invoke-hooks mock, Phase 4A.9 execution
- Integration: E2E with hooks enabled, hook CLI integration, successful logging
- Performance: (part of other NFRs)

**AC2 - Hook Failure Non-blocking**: 9 tests
- Unit: check-hooks error, invoke-hooks timeout/crash, exception handling
- Integration: E2E hook failure, CLI missing, error logging
- Performance: timeout doesn't hang, exception overhead

**AC3 - Respects Configuration**: 11 tests
- Unit: enabled true/false, missing file, default timeout, skip Phase 4A.9
- Integration: E2E with hooks disabled, disabled check response
- Performance: latency without hooks, zero overhead when disabled

**AC4 - Receives Complete Context**: 13 tests
- Unit: custom questions, CLI with epic-id, epic ID validation, context metadata, metadata extraction
- Integration: E2E metadata extraction, feedback responses, CLI actual responses
- Performance: (covered by other tests)

**AC5 - Preserves Lean Orchestration**: 8 tests
- Unit: command budget, skill responsibility (2 tests)
- Performance: lines added (<20), chars (<15K), logic in skill (3 tests)

### By Test Type

**Unit Tests** (37): `tests/unit/test_create_epic_hooks.py`
**Integration Tests** (12): `tests/integration/test_create_epic_hooks_e2e.py`
**Performance Tests** (23): `tests/performance/test_create_epic_hooks_performance.py`

---

## 📊 Test Statistics

| Metric | Count | Percentage |
|--------|-------|-----------|
| **Total Tests** | **72** | **100%** |
| Unit Tests | 37 | 51% |
| Integration Tests | 12 | 17% |
| Performance Tests | 23 | 32% |
| AC1 Coverage | 9 | 13% |
| AC2 Coverage | 9 | 13% |
| AC3 Coverage | 11 | 15% |
| AC4 Coverage | 13 | 18% |
| AC5 Coverage | 8 | 11% |
| Happy Path | 15 | 21% |
| Error Path | 35 | 49% |
| Edge Case | 15 | 21% |
| Security | 3 | 4% |

---

## 🚀 Quick Start

### Run All Tests (Expect All Failures)
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all 72 tests
pytest tests/unit/test_create_epic_hooks.py \
       tests/integration/test_create_epic_hooks_e2e.py \
       tests/performance/test_create_epic_hooks_performance.py -v

# Expected: 72 failed
```

### Run Tests by Category
```bash
# Unit tests only (37)
pytest tests/unit/test_create_epic_hooks.py -v

# Integration tests only (12)
pytest tests/integration/test_create_epic_hooks_e2e.py -v

# Performance tests only (23)
pytest tests/performance/test_create_epic_hooks_performance.py -v
```

### Run Tests by Acceptance Criteria
```bash
# AC1 tests (9 tests)
pytest -k "AC1" -v

# AC2 tests (9 tests)
pytest -k "AC2" -v

# AC3 tests (11 tests)
pytest -k "AC3" -v

# AC4 tests (13 tests)
pytest -k "AC4" -v

# AC5 tests (8 tests)
pytest -k "AC5" -v
```

### Run with Details
```bash
# Show full output including docstrings
pytest tests/unit/test_create_epic_hooks.py -vv --tb=short

# Show durations (slowest tests)
pytest tests/performance/ -v --durations=10

# Stop on first failure
pytest tests/ -x -v
```

---

## 🔄 TDD Workflow

### Current Phase: RED ✅
- [x] Tests written
- [x] All tests failing (expected)
- [x] AC coverage 100%
- [x] Documentation complete

### Next Phase: GREEN ⏳
1. Implement Phase 4A.9 in orchestration skill
2. Run tests - watch them transition from red to green
3. All 72 tests should pass when implementation complete

### Final Phase: REFACTOR ⏳
1. Keep tests green while improving code
2. Performance optimization
3. Documentation updates

---

## 📝 File Relationships

```
STORY-028: Wire Hooks Into /create-epic Command
    │
    ├─ User Story (acceptance criteria)
    │   └─ devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md
    │
    ├─ Implementation Artifacts (to be created)
    │   ├─ .claude/skills/devforgeai-orchestration/SKILL.md (Phase 4A.9)
    │   └─ .claude/commands/create-epic.md (Phase 4)
    │
    ├─ Test Suite (Generated - 72 tests)
    │   ├─ tests/unit/test_create_epic_hooks.py (37 tests)
    │   ├─ tests/integration/test_create_epic_hooks_e2e.py (12 tests)
    │   └─ tests/performance/test_create_epic_hooks_performance.py (23 tests)
    │
    └─ Documentation (Generated)
        ├─ STORY-028-TEST-GENERATION-SUMMARY.md (comprehensive)
        ├─ STORY-028-TEST-QUICK-REFERENCE.md (quick lookup)
        ├─ STORY-028-TEST-VERIFICATION.md (QA checklist)
        └─ STORY-028-INDEX.md (this file - navigation)
```

---

## 🔗 Related Stories

- **STORY-021**: Implement devforgeai check-hooks CLI command
- **STORY-022**: Implement devforgeai invoke-hooks CLI command
- **STORY-027**: Wire hooks into /create-story command (similar pattern)
- **EPIC-006**: Feedback System Integration Completion

---

## 💡 Key Testing Insights

### What's Being Tested

1. **Configuration Management** (AC3)
   - Loading hooks.yaml with epic-create operation
   - Enabled/disabled state respected
   - Default values applied

2. **Hook Invocation** (AC1, AC4)
   - devforgeai check-hooks called correctly
   - devforgeai invoke-hooks receives epic context
   - Metadata extracted from epic file

3. **Failure Handling** (AC2)
   - Exceptions caught without breaking epic creation
   - Errors logged to hook-errors.log
   - User warned but continues with exit 0

4. **Performance** (NFR-001, NFR-002, NFR-003)
   - Hook check <100ms p95
   - Total overhead <3s p95
   - 99.9%+ success despite failures

5. **Architecture** (AC5)
   - All logic in skill Phase 4A.9
   - Command adds <20 lines
   - Lean orchestration pattern preserved

---

## ✅ Quality Guarantees

- ✅ **100% AC Coverage**: All 5 ACs have multiple tests
- ✅ **Independent Tests**: No shared state, can run in any order
- ✅ **Clear Documentation**: Docstrings explain AC coverage (Given/When/Then)
- ✅ **Isolation**: Mocks prevent external dependencies
- ✅ **Edge Cases**: Timeout, crash, missing file, invalid config all covered
- ✅ **Security**: Command injection prevention tested
- ✅ **Performance**: All NFRs have dedicated tests

---

## 📞 Questions & Answers

**Q: Why are all tests failing?**
A: This is the TDD Red phase. Tests are written before implementation. They define the requirements. When implementation starts, tests will pass incrementally.

**Q: Which file should I read first?**
A: Start with `STORY-028-TEST-QUICK-REFERENCE.md` for quick overview, then `STORY-028-TEST-GENERATION-SUMMARY.md` for comprehensive details.

**Q: How do I run just the AC1 tests?**
A: `pytest -k "AC1" -v` - This runs all 9 tests related to AC1.

**Q: Where should I implement Phase 4A.9?**
A: In `.claude/skills/devforgeai-orchestration/SKILL.md` - The skill is responsible for all hook logic (lean orchestration pattern).

**Q: What's the expected hook latency?**
A: Hook check: <100ms (p95), Total overhead: <3000ms (p95). Tests verify these requirements.

---

## 🎓 Learning Resources

**Test Patterns Used**:
- AAA Pattern (Arrange, Act, Assert)
- Mock/Patch for external dependencies
- Pytest fixtures for setup/teardown
- Parametrized tests (where applicable)
- Test markers for categorization

**For Implementation**:
- See "Implementation Guidance" section in SUMMARY.md
- Tests show exactly what's expected
- Mock return values show expected CLI responses

---

## 📋 Checklist Before Implementation

Before starting implementation, ensure you have:

- [ ] Read STORY-028 in `devforgeai/specs/Stories/`
- [ ] Understood all 5 acceptance criteria
- [ ] Read `STORY-028-TEST-QUICK-REFERENCE.md`
- [ ] Reviewed test class organization
- [ ] Understood Phase 4A.9 location (orchestration skill)
- [ ] Planned implementation phases
- [ ] Set up testing environment (pytest installed)

---

## 🏁 Success Criteria

All tests pass when:
1. Phase 4A.9 implemented in orchestration skill
2. Hook configuration loading works
3. check-hooks and invoke-hooks CLIs called correctly
4. Failures handled gracefully (epic creation succeeds)
5. Performance targets met
6. Command budget maintained
7. All 72 tests passing with zero failures

---

## 📞 Support

**Questions about tests?**
- Review the specific test docstring (explains Given/When/Then)
- Check SUMMARY.md for test design patterns
- Check QUICK-REFERENCE.md for organization

**Questions about implementation?**
- Review "Implementation Guidance" in SUMMARY.md
- Tests show expected behavior in assertions
- Mock return values show expected CLI responses

---

**Test Suite Generated**: 2025-11-16
**Status**: ✅ RED PHASE - Ready for TDD Implementation
**Next**: Implement Phase 4A.9 in orchestration skill

---

*Navigation: [Summary](STORY-028-TEST-GENERATION-SUMMARY.md) | [Quick Ref](STORY-028-TEST-QUICK-REFERENCE.md) | [Verification](STORY-028-TEST-VERIFICATION.md) | [Index](STORY-028-INDEX.md)*
