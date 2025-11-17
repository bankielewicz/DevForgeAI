# STORY-049 Test Suite - Quick Reference Guide

**Story ID:** STORY-049
**Title:** Refactor /create-context command budget compliance
**Test Files:**
- `tests/unit/test_story_049_create_context_refactoring.py` (58 unit tests)
- `tests/integration/test_story_049_create_context_integration.py` (38 integration tests)
**Total Tests:** 96

---

## TDD Workflow Status

### Current Phase: RED ✅

```
TDD Red Phase: Tests written, failing initially (expected)
├─ All 96 tests ready for execution
├─ Tests follow AAA pattern (Arrange, Act, Assert)
├─ All tests marked @pytest.mark.xfail (expected to fail)
└─ Ready for developer implementation (Green phase)
```

---

## Quick Commands

### Run All Tests (Verbose)
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py \
                   tests/integration/test_story_049_create_context_integration.py -v
```

### Run Only Unit Tests
```bash
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py -v
```

### Run Only Integration Tests
```bash
python3 -m pytest tests/integration/test_story_049_create_context_integration.py -v
```

### Run Specific Test Class (Example)
```bash
# Character budget tests only
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py::TestAC1CharacterBudgetReduction -v

# Hook workflow tests only
python3 -m pytest tests/integration/test_story_049_create_context_integration.py::TestHookIntegrationWorkflow -v
```

### Run Single Test
```bash
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py::TestAC1CharacterBudgetReduction::test_character_count_below_14000 -v
```

### Run with Short Output
```bash
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py \
                   tests/integration/test_story_049_create_context_integration.py -q
```

### Run with Detailed Traceback
```bash
python3 -m pytest tests/unit/test_story_049_create_context_refactoring.py \
                   tests/integration/test_story_049_create_context_integration.py -vv --tb=long
```

---

## Interpreting Test Results

### XFAIL (Expected Fail) ✅
- Test is **expected to fail** (marked with `@pytest.mark.xfail`)
- This is the **correct status** in RED phase
- Means: "Waiting for implementation"
- **Action:** None - this is expected

### XPASS (Unexpected Pass) ⚠️
- Test is **marked expected fail but passed anyway**
- Happens when current code partially satisfies test criteria
- Means: "Test criteria already partially met by current implementation"
- **Action:** None - just informational, will resolve during Green phase

### FAIL (Failure) ❌
- Test **failed** and was **not** marked `@pytest.mark.xfail`
- Means: "Something is wrong with the test itself"
- **Action:** Review test implementation (syntax error, logic error)

### PASS (Success) ✅
- Test **passed** normally (not marked `@pytest.mark.xfail`)
- Means: "This test criterion is already met"
- **Action:** None - this is expected for many tests in RED phase

---

## Understanding Test Failures (Green Phase)

Once implementation starts, tests will transition from XFAIL to FAIL or PASS.

### Test Failure Example

```
FAILED tests/unit/test_story_049_create_context_refactoring.py::TestAC1CharacterBudgetReduction::test_character_count_below_14000

AssertionError: Command exceeds budget: 16210 chars (target: ≤14,000, budget: 108.1%)
```

**Interpretation:**
- Command is currently 16,210 characters
- Must be reduced to ≤14,000 characters
- Currently at 108% of budget (8% over)
- Need to extract ~2,210 characters (per AC1)

**Fix Strategy:**
1. Extract Phase N pattern documentation to external file
2. Condense inline comments
3. Reference pattern file via Read tool
4. Re-measure character count
5. Re-run test until PASS

---

## Test Organization by Acceptance Criteria

### AC1: Character Budget Reduction
**Tests:** 5 in `TestAC1CharacterBudgetReduction`
**Key Tests:**
- `test_character_count_below_14000` - Character count ≤14K
- `test_budget_compliance_percentage` - Usage ≤93% of budget

**Expected Behavior in Green Phase:**
- These 5 tests will change from XFAIL to FAIL (until implementation)
- Then from FAIL to PASS (once characters reduced)

### AC2: Hook Integration Workflow Preserved
**Tests:** 14 total (7 unit + 7 integration)
**Key Tests:**
- `test_all_four_workflow_steps_present` - Steps 1-4 documented
- `test_phase_n_references_pattern_file` - Read tool used

**Expected Behavior:**
- Most already XPASS (workflow already exists)
- Key ones XFAIL: pattern file reference

### AC3: Pattern Documentation Externalized
**Tests:** 9 in `TestAC3PatternDocumentationExternalized`
**Key Tests:**
- `test_pattern_file_exists` - File must exist
- `test_pattern_file_contains_implementation_steps` - 4 steps documented
- `test_command_references_pattern_file_with_read_tool` - Read tool used

**Expected Behavior:**
- Pattern file tests: XFAIL until pattern file created/linked
- After implementation: All PASS

### AC4: Backward Compatibility Maintained
**Tests:** 13 total (10 unit + 6 integration)
**Key Tests:**
- `test_architecture_skill_invocation_preserved` - Skill still invoked
- `test_no_critical_sections_removed` - All sections intact

**Expected Behavior:**
- Most already XPASS (existing code intact)
- Should remain PASS throughout implementation

### AC5: Framework Compliance Validated
**Tests:** 10 in `TestAC5FrameworkComplianceValidated`
**Key Tests:**
- `test_lean_orchestration_pattern_applied` - Pattern followed
- `test_audit_budget_compliant` - Budget audit passes

**Expected Behavior:**
- `test_audit_budget_compliant`: XFAIL → PASS (when chars ≤14K)
- Others: XPASS → PASS (already mostly compliant)

---

## Typical Red Phase Output

```
========================= test session starts ==========================
collected 96 items

tests/unit/test_story_049_create_context_refactoring.py::TestAC1...::test_character_count_below_14000 XFAIL [ 1%]
tests/unit/test_story_049_create_context_refactoring.py::TestAC1...::test_character_count_below_15000_hard_limit XFAIL [ 3%]
tests/unit/test_story_049_create_context_refactoring.py::TestAC1...::test_budget_compliance_percentage XFAIL [ 5%]
... (many XPASS tests for existing functionality)
tests/integration/test_story_049_create_context_integration.py::TestPatternFileIntegration::test_pattern_file_path_correct XFAIL [ 94%]
tests/integration/test_story_049_create_context_integration.py::TestPatternFileIntegration::test_pattern_file_read_in_hook_phase XFAIL [ 95%]

========================== 9 xfailed, 87 xpassed in 1.80s ==========================
```

**Interpretation:**
- ✅ All 96 tests collected successfully
- ✅ 9 tests XFAIL (critical ones waiting for implementation)
- ✅ 87 tests XPASS (existing code partially satisfies criteria)
- ✅ Red phase is working correctly

---

## Test Failure Troubleshooting

### Issue: "AssertionError: Character exceeds budget"

```
FAILED test_character_count_below_14000
AssertionError: Command exceeds budget: 16210 chars (target: ≤14,000, budget: 108.1%)
```

**Solution:**
1. Current: 16,210 chars
2. Target: ≤14,000 chars
3. Need to reduce: 2,210+ chars
4. **Action:** Extract Phase N pattern documentation (expected ~2,500 chars)

**How to Extract:**
```
Phase N section contains:
  ├─ Step 1-4 (keep - workflow critical)
  ├─ Key Characteristics section (MOVE to pattern file)
  ├─ Pattern Consistency notes (MOVE to pattern file)
  ├─ Verbose comments (CONDENSE)
  └─ Read(file_path="...") reference (ADD)
```

### Issue: "Pattern file references not found"

```
FAILED test_pattern_file_path_correct
AssertionError: Incorrect pattern file path or missing Read tool reference
```

**Solution:**
1. Add Phase N section with: `Read(file_path=".devforgeai/protocols/hook-integration-pattern.md")`
2. Path must be exact: `.devforgeai/protocols/hook-integration-pattern.md`
3. File already exists (created in STORY-030)

### Issue: "Phase N not found"

```
FAILED test_phase_n_section_exists
AssertionError: Phase N section not found
```

**Solution:**
1. Verify Phase N exists in command
2. Should be titled like: `### Phase N: Feedback Hook Integration`
3. Comes after Phase 6 (Final Validation)
4. Comes before Phase 7 (Success Report)

---

## Implementation Checklist

Use this checklist while implementing (Green phase):

**Preparation:**
- [ ] Read STORY-049 acceptance criteria
- [ ] Review test suite (this file + test comments)
- [ ] Measure baseline: `wc -c .claude/commands/create-context.md` (expected: ~16K)

**Implementation:**
- [ ] Extract Phase N pattern documentation from command
- [ ] Create/verify `.devforgeai/protocols/hook-integration-pattern.md` exists
- [ ] Update Phase N in command to reference pattern file via Read tool
- [ ] Condense inline comments in Phase N (~300 chars reduction)
- [ ] Verify all 4 workflow steps still present (Steps 1-4)
- [ ] Measure final size: `wc -c .claude/commands/create-context.md` (target: ≤14K)

**Testing:**
- [ ] Run unit tests: `pytest tests/unit/test_story_049_create_context_refactoring.py -v`
- [ ] Run integration tests: `pytest tests/integration/test_story_049_create_context_integration.py -v`
- [ ] Verify: 96/96 tests passing
- [ ] Verify: Character count ≤14,000
- [ ] Verify: /audit-budget shows COMPLIANT status

**Quality:**
- [ ] Code review (score ≥90/100)
- [ ] Manual testing: Greenfield mode
- [ ] Manual testing: Brownfield mode
- [ ] Manual testing: Hook registration workflow
- [ ] Documentation review: Phase N clarity

**Sign-off:**
- [ ] All tests passing (96/96)
- [ ] Budget compliance verified
- [ ] Backward compatibility confirmed
- [ ] Ready for QA validation

---

## Test Metrics at a Glance

| Metric | Value |
|--------|-------|
| **Total Tests** | 96 |
| **Unit Tests** | 58 |
| **Integration Tests** | 38 |
| **AC1 Tests** | 5 |
| **AC2 Tests** | 14 |
| **AC3 Tests** | 9 |
| **AC4 Tests** | 13 |
| **AC5 Tests** | 10 |
| **Edge Case Tests** | 6 |
| **Quality Tests** | 6 |
| **Integration Tests** | 8 |
| **Expected Red Phase Xfails** | 9 |
| **Expected Red Phase Xpasses** | 87 |
| **Total Assertions** | 200+ |

---

## Key Test Files

### Main Test Files
- `tests/unit/test_story_049_create_context_refactoring.py` - Unit tests (58)
- `tests/integration/test_story_049_create_context_integration.py` - Integration tests (38)

### Documentation
- `tests/STORY-049-TEST-SUITE-SUMMARY.md` - Comprehensive test suite overview
- `tests/STORY-049-QUICK-REFERENCE.md` - This file

### Related Story Files
- `.ai_docs/Stories/STORY-049-refactor-create-context-budget-compliance.story.md` - Story details
- `.claude/commands/create-context.md` - Command to refactor
- `.devforgeai/protocols/hook-integration-pattern.md` - Pattern file (reference)

---

## Next Steps for Developers

1. **Understand Requirements**
   - Read STORY-049 story file (AC1-AC5)
   - Review this quick reference
   - Review test summary document

2. **Run Tests (Red Phase)**
   ```bash
   pytest tests/unit/test_story_049_create_context_refactoring.py \
           tests/integration/test_story_049_create_context_integration.py -v
   ```

3. **Implement Refactoring (Green Phase)**
   - Follow implementation checklist above
   - Extract pattern documentation (~2,500 chars)
   - Condense comments (~300 chars)
   - Add Read tool reference
   - Target: ≤14,000 chars

4. **Run Tests (Green Phase)**
   - Re-run same test command
   - Expect: 96/96 tests PASS
   - Verify character count ≤14K

5. **Code Quality & Review**
   - Code review (≥90/100)
   - Manual scenario testing
   - Get approvals

6. **Mark Complete**
   - All tests passing
   - All checklist items done
   - Ready for QA validation

---

## Still Have Questions?

### Test Not Making Sense?
- Read the test's **docstring** (explains what it tests)
- Read the test's **assertion message** (explains expected value)
- Review relevant **acceptance criteria** in story file

### How to Debug Test?
```bash
# Run with very verbose output
pytest -vv --tb=long tests/unit/test_story_049_create_context_refactoring.py::TestAC1CharacterBudgetReduction::test_character_count_below_14000

# Run with print statements (add print() in test, use -s flag)
pytest -s tests/unit/test_story_049_create_context_refactoring.py::TestAC1CharacterBudgetReduction::test_character_count_below_14000
```

### Need to Skip Tests?
```bash
# Skip integration tests
pytest tests/unit/test_story_049_create_context_refactoring.py -v

# Skip specific test
pytest tests/unit/test_story_049_create_context_refactoring.py -v -k "not test_character_count_below_14000"
```

---

**Test Suite Version:** 1.0
**Created:** 2025-11-17
**TDD Phase:** RED (Ready for implementation)
**Status:** ✅ All 96 tests collected and ready
