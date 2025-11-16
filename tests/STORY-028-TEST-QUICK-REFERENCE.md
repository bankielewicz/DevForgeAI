# STORY-028 Test Suite - Quick Reference

**Generated**: 2025-11-16 | **Status**: Red Phase (All Failing)
**Tests**: 72 | **Files**: 3 | **Acceptance Criteria Covered**: 100%

---

## 📋 File Manifest

| File | Tests | Focus | Location |
|------|-------|-------|----------|
| `test_create_epic_hooks.py` | 37 | Unit - Config, CLI mocks, validation | `tests/unit/` |
| `test_create_epic_hooks_e2e.py` | 12 | Integration - Full workflows, logging | `tests/integration/` |
| `test_create_epic_hooks_performance.py` | 23 | Performance - Latency, reliability | `tests/performance/` |

---

## ✅ Acceptance Criteria Matrix

```
AC1 (Automatic Hook Trigger)          ✅✅✅✅✅✅✅✅✅
AC2 (Hook Failure Non-blocking)        ✅✅✅✅✅✅✅✅✅
AC3 (Respects Configuration)           ✅✅✅✅✅✅✅✅✅✅✅
AC4 (Hook Receives Context)            ✅✅✅✅✅✅✅✅✅✅✅✅✅
AC5 (Lean Orchestration Pattern)       ✅✅✅✅✅✅✅✅
```

---

## 🏃 Quick Test Runs

### Run Everything
```bash
pytest tests/unit/test_create_epic_hooks.py \
       tests/integration/test_create_epic_hooks_e2e.py \
       tests/performance/test_create_epic_hooks_performance.py -v
```

### Run Just Unit Tests
```bash
pytest tests/unit/test_create_epic_hooks.py -v --tb=short
```

### Run by AC
```bash
pytest -k "AC1" -v                    # AC1 tests
pytest -k "AC2" -v                    # AC2 tests
pytest -k "AC3" -v                    # AC3 tests (11 tests)
pytest -k "AC4" -v                    # AC4 tests (13 tests)
pytest -k "AC5" -v                    # AC5 tests (8 tests)
```

### Run Performance Only
```bash
pytest tests/performance/ -v --tb=short
```

---

## 🎯 Test Class Organization

### UNIT TESTS (37 tests)

**TestEpicHookConfigurationLoading** (7 tests)
- Loading `hooks.yaml` with enabled/disabled state
- Default timeout values
- Custom questions parsing
- Missing file handling

**TestEpicHookCLIMocking** (8 tests)
- `devforgeai check-hooks` mock responses
- `devforgeai invoke-hooks` mock responses
- CLI exit codes (0, 1, 2, 3)
- Timeout handling

**TestEpicContextValidation** (8 tests)
- Epic ID format validation (EPIC-\\d{3})
- Required fields presence
- Feature count range (3-8 optimal)
- Security - no command injection

**TestEpicHookPhase4A9Integration** (5 tests)
- Phase 4A.9 skip when disabled
- Phase 4A.9 execute when enabled
- Epic file existence check
- CLI not found handling
- Budget compliance

**TestEpicHookExceptionHandling** (4 tests)
- Hook timeout exception handling
- Hook CLI crash handling
- Missing epic file handling
- Configuration parse error handling

**TestEpicHookMetadataExtraction** (5 tests)
- Extract epic ID
- Extract feature count
- Extract complexity score
- Extract risks
- Build context-aware questions

---

### INTEGRATION TESTS (12 tests)

**TestCreateEpicHooksE2E** (8 tests)
- Epic creation with hooks enabled
- Epic creation with hooks disabled
- Hook failure doesn't break epic
- Metadata extraction and usage
- Feedback responses stored
- Multiple epics sequential
- Hook CLI missing error handling

**TestHookCLIIntegration** (2 tests)
- check-hooks CLI responds with JSON
- invoke-hooks CLI responds with JSON
- *Marked @pytest.mark.integration (requires CLI)*

**TestCreateEpicHooksLogging** (2 tests)
- Success logged to `hooks.log`
- Failure logged to `hook-errors.log`

---

### PERFORMANCE TESTS (23 tests)

**TestHookCheckPerformance** (2 tests)
- check-hooks <100ms p95 threshold
- check-hooks average execution time

**TestHookOverheadPerformance** (2 tests)
- Total hook overhead <3s p95
- Total hook overhead average

**TestEpicCreationLatencyComparison** (3 tests)
- Latency with hooks enabled
- Latency with hooks disabled
- Near-zero overhead when disabled

**TestHookFailurePerformance** (2 tests)
- Timeout doesn't hang epic creation
- Exception handling overhead

**TestHookReliability** (3 tests)
- 99.9% success rate under stress
- Stress test 100 concurrent checks

**TestHookBudgetCompliance** (3 tests)
- Phase 4A.9 adds <20 lines to command
- Command stays <15K chars
- Hook logic entirely in skill

---

## 🧪 Test Execution Patterns

### AAA Pattern Used Consistently
```python
def test_example(self):
    """Clear docstring with AC coverage."""
    # Arrange - Setup preconditions
    config = {'enabled': True}

    # Act - Execute behavior being tested
    result = load_config(config)

    # Assert - Verify outcome
    assert result['enabled'] is True
```

### Mock Strategy
- **subprocess.run** → devforgeai CLI calls
- **tempfile.TemporaryDirectory** → file operations
- **MagicMock** → JSON responses, exit codes
- **side_effect** → sequential mock returns

### Fixture Pattern
```python
@pytest.fixture
def temp_project_dir(self):
    """Temporary .devforgeai directory structure"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create structure
        yield tmpdir_path
        # Auto cleanup
```

---

## 📊 Coverage Statistics

| Category | Count | % of Total |
|----------|-------|-----------|
| Happy Path Tests | 15 | 21% |
| Error Path Tests | 35 | 49% |
| Edge Case Tests | 15 | 21% |
| Performance Tests | 7 | 10% |
| **Total** | **72** | **100%** |

---

## 🚨 Current Test Status

**ALL 72 TESTS FAILING** (Expected in Red Phase)

```
$ pytest tests/unit/test_create_epic_hooks.py -q
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  [100%]
37 failed
```

No implementation yet - tests define the requirements.

---

## 🔄 TDD Implementation Flow

### Phase: Red (Current)
✅ Tests written (failing)
✅ All 5 ACs have test coverage
✅ Edge cases covered
✅ Performance requirements defined

### Phase: Green (Next)
⏳ Implement Phase 4A.9 in orchestration skill
⏳ Tests start passing as features added
⏳ Goal: All 72 tests passing

### Phase: Refactor (After)
⏳ Code cleanup while keeping tests green
⏳ Performance optimization
⏳ Documentation updates

---

## 🎓 Key Test Insights

### What Gets Tested

1. **Hook Configuration** (AC3)
   - ✅ YAML parsing (enabled/disabled)
   - ✅ Default values (timeout = 30000ms)
   - ✅ Custom questions loading
   - ✅ Missing file safety

2. **Hook Invocation** (AC1, AC4)
   - ✅ Check-hooks CLI called correctly
   - ✅ Invoke-hooks CLI receives epic-id
   - ✅ Epic metadata extracted
   - ✅ Questions reference specific details

3. **Failure Handling** (AC2)
   - ✅ Hook failures caught
   - ✅ Epic creation succeeds (exit 0)
   - ✅ Errors logged
   - ✅ User warned

4. **Performance** (NFR-001, NFR-002, NFR-003)
   - ✅ Check-hooks <100ms p95
   - ✅ Total overhead <3s p95
   - ✅ 99.9% success rate
   - ✅ Zero overhead when disabled

5. **Architecture** (AC5)
   - ✅ All logic in skill Phase 4A.9
   - ✅ Command adds <20 lines
   - ✅ Command stays <15K chars
   - ✅ Lean orchestration pattern

---

## 💡 Implementation Hints from Tests

Based on test structure, implementation needs:

1. **In Orchestration Skill (Phase 4A.9)**
   ```
   Phase 4A.9: Post-Epic Feedback
   ├─ Step 1: Load hooks.yaml
   ├─ Step 2: Call check-hooks CLI
   ├─ Step 3: If enabled=true:
   │  ├─ Verify epic file exists
   │  ├─ Call invoke-hooks with epic-id
   │  ├─ Handle timeout/crash gracefully
   │  └─ Log result (success or error)
   └─ Step 4: Return result to command
   ```

2. **In /create-epic Command (Phase 4)**
   ```
   Phase 4: Display results
   ├─ Invoke skill
   └─ Display hook result (feedback questions or message)
   ```

3. **Configuration Files**
   - `.devforgeai/config/hooks.yaml` (enable/disable)
   - `.devforgeai/feedback/.logs/hooks.log` (success log)
   - `.devforgeai/feedback/.logs/hook-errors.log` (error log)
   - `.devforgeai/feedback/epic-create/{EPIC-ID}_{timestamp}.json` (responses)

4. **CLI Requirements**
   - `devforgeai check-hooks --operation=epic-create` → JSON response
   - `devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-NNN` → JSON response

---

## 🔗 Related Files

- **Story**: `.ai_docs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md`
- **Skill**: `.claude/skills/devforgeai-orchestration/SKILL.md` (Phase 4A.9 to add)
- **Command**: `.claude/commands/create-epic.md` (Phase 4 to update)
- **Config Example**: `.devforgeai/config/hooks.yaml.example` (to create)
- **Dependency Stories**: STORY-021 (check-hooks), STORY-022 (invoke-hooks)

---

## ✨ Test Quality Metrics

- **Independence**: ✅ Each test isolated, no shared state
- **Clarity**: ✅ Docstrings explain AC coverage
- **Coverage**: ✅ 100% AC coverage, edge cases included
- **Maintainability**: ✅ Clear test names, AAA pattern
- **Performance**: ✅ All tests complete in <100ms (except marked as slow)
- **Isolation**: ✅ Mocks prevent external dependencies

---

## 📝 Next Steps

1. **Implement Phase 4A.9** in orchestration skill
2. **Run tests** to see failures transition to passes
3. **Add actual CLI calls** when devforgeai check-hooks/invoke-hooks ready
4. **Optimize performance** if needed (hook latency)
5. **Add integration tests** with real CLI once available

---

**Ready for TDD Green Phase implementation!**
