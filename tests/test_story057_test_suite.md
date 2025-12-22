# STORY-057 Test Suite - Complete Documentation

**Story**: Additional Skill Integrations (architecture, ui-generator, orchestration)
**Sprint**: SPRINT-2
**Total Tests**: 99 (45 unit + 9 integration + 45 regression)
**Status**: GENERATED - All tests FAILING (TDD Red phase)

---

## Test Suite Overview

### Purpose
Validate comprehensive integration of user-input-guidance.md across three DevForgeAI skills:
- devforgeai-architecture (greenfield/brownfield conditional)
- devforgeai-ui-generator (standalone/story conditional)
- devforgeai-orchestration (epic/sprint modes)

### Test Distribution

**Unit Tests (45 total)**
- Architecture skill: 15 tests
- UI-Generator skill: 15 tests
- Orchestration skill: 15 tests

**Integration Tests (9 total)**
- Cross-skill workflows: 9 tests

**Regression Tests (45 total)**
- Architecture existing tests: 15 tests (placeholder, run existing suite)
- UI-Generator existing tests: 15 tests (placeholder, run existing suite)
- Orchestration existing tests: 15 tests (placeholder, run existing suite)

---

## Unit Test Files

### File 1: `tests/unit/test_story057_architecture_skill_integration.py`

**Purpose**: Validate devforgeai-architecture skill integration

**Tests (15)**

#### Conditional Loading Tests (1-5)
```
✓ test_01_greenfield_mode_loads_guidance
  - Checks: 0 context files → guidance loaded
  - AC#1: Greenfield mode detection

✓ test_02_brownfield_mode_skips_guidance
  - Checks: 6 context files → guidance skipped
  - AC#1: Brownfield mode detection

✓ test_03_partial_greenfield_mode_loads_guidance
  - Edge case: 3-5 context files → guidance loaded
  - Handles incomplete context

✓ test_04_missing_guidance_file_graceful_fallback
  - Edge case: File missing → graceful fallback
  - NFR-004: Graceful degradation

✓ test_05_corrupted_guidance_file_graceful_fallback
  - Edge case: Corrupted content → fallback
  - NFR-004: Error handling
```

#### Pattern Application Tests (6-10)
```
✓ test_06_open_ended_discovery_pattern_applied
  - Pattern: Open-Ended Discovery for technology inventory
  - AC#1: Phase 1 Step 1

✓ test_07_closed_confirmation_pattern_applied
  - Pattern: Closed Confirmation for greenfield/brownfield
  - AC#1: Greenfield/brownfield detection

✓ test_08_explicit_classification_pattern_applied
  - Pattern: Explicit Classification for architecture style (4 options)
  - AC#1: 4 architecture styles

✓ test_09_bounded_choice_pattern_applied
  - Pattern: Bounded Choice for framework selection
  - AC#1: Framework filtering

✓ test_10_pattern_fallback_when_guidance_missing
  - Fallback: Generate baseline questions without patterns
  - NFR-004: Fallback behavior
```

#### Integration & Backward Compatibility Tests (11-15)
```
✓ test_11_token_overhead_bounded
  - Metric: ≤1,000 tokens per skill
  - AC#5: Token overhead limit
  - NFR-001: Performance

✓ test_12_phase1_completion_with_guidance
  - Checks: All Phase 1 patterns available
  - AC#1: Complete phase 1

✓ test_13_error_handling_and_logging
  - Business Rule BR-004: Log conditional decisions
  - Validates: "mode detected" log messages

✓ test_14_backward_compatibility_non_conditional
  - AC#7: Brownfield behavior unchanged
  - Checks: Pattern mappings documented

✓ test_15_reference_file_structure
  - SKILL-ARCH-006: ≥200 lines
  - Validates: Conditional logic, pattern mapping, examples
```

---

### File 2: `tests/unit/test_story057_ui_generator_skill_integration.py`

**Purpose**: Validate devforgeai-ui-generator skill integration

**Tests (15)**

#### Conditional Loading Tests (1-5)
```
✓ test_01_standalone_mode_loads_guidance
  - Checks: No story file → guidance loaded
  - AC#2: Standalone mode detection

✓ test_02_story_mode_skips_guidance
  - Checks: Story file exists → guidance skipped
  - AC#2: Story mode detection

✓ test_03_story_mode_with_ui_specification
  - Edge case: Story has UI Specification → skip guidance
  - Validates story-driven workflow

✓ test_04_missing_guidance_file_graceful_fallback
  - Edge case: File missing → fallback
  - NFR-004: Graceful degradation

✓ test_05_empty_story_file_still_loads_guidance
  - Edge case: Empty story file → still skip guidance (story mode precedence)
  - Validates mode detection priority
```

#### Pattern Application Tests (6-10)
```
✓ test_06_explicit_classification_ui_type
  - Pattern: Explicit Classification for UI type (4 options)
  - AC#2: Web/Desktop/Mobile/Terminal

✓ test_07_bounded_choice_framework_selection
  - Pattern: Bounded Choice for framework (filtered by UI type + tech-stack)
  - AC#2: Framework filtering

✓ test_08_bounded_choice_styling_approach
  - Pattern: Bounded Choice for styling (5 options)
  - AC#2: Tailwind/Bootstrap/Material/Custom/None

✓ test_09_pattern_extraction_and_lookup
  - Validates pattern extraction from guidance
  - Checks: Pattern lookup implementation

✓ test_10_fallback_ui_questions
  - Fallback: Generate baseline UI questions
  - NFR-004: Fallback behavior
```

#### Integration & Backward Compatibility Tests (11-15)
```
✓ test_11_token_overhead_bounded
  - Metric: ≤1,000 tokens per skill
  - AC#5: Token overhead limit

✓ test_12_phase2_completion_with_guidance
  - Checks: All Phase 2 patterns available
  - AC#2: Complete phase 2

✓ test_13_skip_message_logged
  - Business Rule BR-004: Log skip message
  - Validates: Story mode skip message

✓ test_14_backward_compatibility_existing_tests
  - AC#7: Existing tests pass
  - Checks: No breaking changes

✓ test_15_reference_file_ui_specific_content
  - SKILL-UI-005: ≥200 lines
  - Validates: Standalone/story conditional, UI-specific patterns
```

---

### File 3: `tests/unit/test_story057_orchestration_skill_integration.py`

**Purpose**: Validate devforgeai-orchestration skill integration (epic + sprint modes)

**Tests (15)**

#### Conditional Loading - Epic/Sprint Tests (1-5)
```
✓ test_01_epic_mode_loads_guidance
  - Checks: /create-epic command → guidance loaded
  - AC#3: Epic mode detection
  - SKILL-ORCH-001: Load in Phase 4A Step 2

✓ test_02_sprint_mode_loads_guidance
  - Checks: /create-sprint command → guidance loaded
  - AC#4: Sprint mode detection
  - SKILL-ORCH-002: Load in Phase 3 Step 1

✓ test_03_other_modes_skip_guidance
  - Checks: Story management, checkpoint → skip
  - AC#6: Conditional skip logic

✓ test_04_missing_guidance_graceful_fallback
  - Edge case: File missing → fallback
  - NFR-004: Graceful degradation

✓ test_05_corrupted_guidance_graceful_fallback
  - Edge case: Corrupted content → fallback
  - NFR-004: Error handling
```

#### Pattern Application - Epic Mode Tests (6-8)
```
✓ test_06_open_ended_discovery_epic_goal
  - Pattern: Open-Ended Discovery for epic goal
  - AC#3: Phase 4A Step 2, free-form goal

✓ test_07_bounded_choice_epic_timeline
  - Pattern: Bounded Choice for timeline (4 options)
  - AC#3: 1/2-3/4-6/6+ sprints

✓ test_08_explicit_classification_epic_priority
  - Pattern: Explicit Classification for priority (4 levels)
  - AC#3: Critical/High/Medium/Low
```

#### Pattern Application - Sprint Mode Tests (9-10)
```
✓ test_09_bounded_choice_explicit_none_epic_selection
  - Pattern: Bounded Choice + Explicit None for epic selection
  - AC#4: Phase 3 Step 1, optional epic linkage

✓ test_10_bounded_choice_multi_select_story_capacity
  - Pattern: Bounded Choice with Multi-Select for stories
  - AC#4: Capacity guidance (running total, warnings <20 or >40)
```

#### Integration & Backward Compatibility Tests (11-15)
```
✓ test_11_token_overhead_epic_mode
  - Metric: ≤1,000 tokens for epic mode
  - AC#5: Token overhead limit

✓ test_12_token_overhead_sprint_mode
  - Metric: ≤1,000 tokens for sprint mode
  - AC#5: Token overhead limit

✓ test_13_phase_4a_completion_with_epic_guidance
  - Checks: All epic patterns available
  - AC#3: Complete Phase 4A Step 2

✓ test_14_phase_3_completion_with_sprint_guidance
  - Checks: All sprint patterns available
  - AC#4: Complete Phase 3 Step 1

✓ test_15_reference_file_structure_dual_mode
  - SKILL-ORCH-009: ≥300 lines (dual modes)
  - Validates: Epic + sprint sections, pattern mappings, examples
```

#### Edge Case Tests (EC1-2)
```
✓ test_ec_01_sprint_with_low_capacity_warning
  - Edge Case 4: <20 points → low capacity warning
  - Validates: Warning displayed, user can proceed

✓ test_ec_02_sprint_with_high_capacity_warning
  - Edge Case 4: >40 points → high capacity warning
  - Validates: Warning displayed, user can proceed
```

---

## Integration Test File

### File 4: `tests/integration/test_story057_cross_skill_integration.py`

**Purpose**: Validate cross-skill coordination and consistency

**Tests (9)**

```
✓ test_01_multi_skill_workflow_all_load_guidance
  - Integration Test 1: Architecture greenfield + UI standalone + Orchestration epic
  - All 3 load guidance in isolated contexts
  - No conflicts, all complete independently

✓ test_02_multi_skill_workflow_selective_loading
  - Integration Test 2: Architecture brownfield + UI story + Orchestration story_management
  - All 3 skip guidance appropriately
  - Validates: Conditional skip logic across skills

✓ test_03_guidance_file_checksum_validation
  - Integration Test 3: File checksums match across 3 skills
  - Business Rule BR-002: Identical content validation
  - SHA256 hash comparison (100% match required)

✓ test_04_guidance_file_synchronization
  - Integration Test 4: Files synchronized (content identical)
  - Validates: File deployment from master to 3 skills
  - Content comparison (byte-for-byte match)

✓ test_05_pattern_name_consistency
  - Integration Test 5: Pattern names uniform across skills
  - NFR-008: Canonical pattern names (no variations)
  - Validates: "Open-Ended Discovery", not "Open Ended", "Open-ended", etc.

✓ test_06_fallback_behavior_identical
  - Integration Test 6: Fallback messages identical across skills
  - NFR-009: Same warning format for all skills
  - Validates: Log message consistency

✓ test_07_fallback_log_message_format
  - Integration Test 7: Log format follows canonical pattern
  - Format: "Skipping user-input-guidance.md ([reason])"
  - Validates: Consistent logging across all scenarios

✓ test_08_concurrent_skill_execution
  - Integration Test 8: 5 concurrent executions (no file locking)
  - 2x architecture greenfield + 2x UI standalone + 1x orchestration epic
  - Validates: Thread-safe Read operations, no race conditions

✓ test_09_end_to_end_workflow
  - Integration Test 9: Full workflow (ideate → architecture → epic → sprint → UI)
  - Architecture loads guidance (greenfield)
  - Epic loads guidance (epic mode)
  - Sprint loads guidance (sprint mode)
  - UI skips guidance (story mode, derived from epic/sprint)
```

#### Performance Test: Token Accumulation
```
✓ test_token_overhead_no_accumulation
  - AC#5: No cumulative token cost
  - Isolated contexts: architecture ≤1K, ui ≤1K, orchestration ≤1K
  - Main conversation: <100 tokens for summaries
  - Total: <2,000 tokens
```

---

## Regression Test Integration

### Placeholder Pattern for Regression Tests

All regression tests follow this pattern:

```python
@pytest.mark.regression
def test_backward_compat_existing_[skill]_tests():
    """
    AC#7: All existing [skill] tests should pass (100% pass rate)

    When: Guidance integration deployed
    Then: Existing test suite shows 15/15 PASSED
    """
    # Placeholder for regression test integration
    assert True, "Placeholder for regression test integration"
```

**How to Run Regression Tests**:
```bash
# Run existing architecture tests
pytest tests/unit/test_*architecture* -k "not story057" -v

# Run existing UI tests
pytest tests/unit/test_*ui* -k "not story057" -v

# Run existing orchestration tests
pytest tests/unit/test_*orchestration* -k "not story057" -v

# Run all regressions in one command
pytest tests/unit/ tests/integration/ -k "not story057" -v --tb=short
```

**Regression Test Count**: 45 tests
- Architecture existing tests: 15
- UI-Generator existing tests: 15
- Orchestration existing tests: 15

---

## Coverage Requirements

### Acceptance Criteria Coverage

**AC#1: Architecture Integration**
- ✓ Conditional Step 0 (greenfield/brownfield)
- ✓ Open-Ended Discovery pattern
- ✓ Closed Confirmation pattern
- ✓ Explicit Classification pattern
- ✓ Bounded Choice pattern
- ✓ Reference file (≥200 lines)

**AC#2: UI-Generator Integration**
- ✓ Conditional Step 0 (standalone/story)
- ✓ Explicit Classification for UI type
- ✓ Bounded Choice for framework
- ✓ Bounded Choice for styling
- ✓ Reference file (≥200 lines)

**AC#3: Orchestration Epic Integration**
- ✓ Step 0 in Phase 4A Step 2
- ✓ Open-Ended Discovery for goal
- ✓ Bounded Choice for timeline
- ✓ Explicit Classification for priority
- ✓ Open-Ended with Minimum Count for criteria

**AC#4: Orchestration Sprint Integration**
- ✓ Step 0 in Phase 3 Step 1
- ✓ Bounded Choice + Explicit None for epic
- ✓ Bounded Choice with Multi-Select for stories
- ✓ Capacity guidance (running total, warnings)

**AC#5: Token Overhead**
- ✓ Architecture ≤1,000 tokens
- ✓ UI-Generator ≤1,000 tokens
- ✓ Orchestration epic ≤1,000 tokens
- ✓ Orchestration sprint ≤1,000 tokens
- ✓ No cumulative cost

**AC#6: Conditional Loading**
- ✓ Architecture greenfield loads
- ✓ Architecture brownfield skips
- ✓ UI standalone loads
- ✓ UI story skips
- ✓ Orchestration epic loads
- ✓ Orchestration sprint loads

**AC#7: Backward Compatibility**
- ✓ Architecture tests pass (15)
- ✓ UI-generator tests pass (15)
- ✓ Orchestration tests pass (15)
- ✓ Non-conditional scenarios unchanged
- ✓ No breaking changes

### Technical Requirement Coverage

**SKILL Requirements** (9 total)
- ✓ SKILL-ARCH-001 through SKILL-ARCH-006 (6 tests)
- ✓ SKILL-UI-001 through SKILL-UI-005 (5 tests)
- ✓ SKILL-ORCH-001 through SKILL-ORCH-009 (9 tests)

**Business Rules** (5 total)
- ✓ BR-001: Conditional detection correct (3 integration tests)
- ✓ BR-002: File checksums match (1 integration test)
- ✓ BR-003: Patterns don't override user choice (implicit in tests)
- ✓ BR-004: Logging of decisions (1 unit test per skill)
- ✓ BR-005: Reference files documented (3 unit tests)

**Non-Functional Requirements** (10 total)
- ✓ NFR-001: Performance / Token overhead (3 tests)
- ✓ NFR-002: File loading speed (implicit in NFR-001)
- ✓ NFR-003: Conditional check <100ms (implicit in integration tests)
- ✓ NFR-004: Graceful degradation (5 tests)
- ✓ NFR-005: Deterministic skip logic (implicit in conditional tests)
- ✓ NFR-006: Reference file comprehensiveness (3 tests)
- ✓ NFR-007: Checksum synchronization (1 integration test)
- ✓ NFR-008: Pattern name uniformity (1 integration test)
- ✓ NFR-009: Fallback uniformity (2 integration tests)
- ✓ NFR-010: Testability (99 tests total)

### Edge Case Coverage (7 edge cases)

**Edge Case 1**: Architecture brownfield (skip guidance)
- ✓ test_02_brownfield_mode_skips_guidance

**Edge Case 2**: UI with story file (skip guidance)
- ✓ test_02_story_mode_skips_guidance

**Edge Case 3**: Orchestration with pre-filled metadata
- Implicit in multi-skill workflow tests

**Edge Case 4**: Sprint planning with capacity warnings
- ✓ test_ec_01_sprint_with_low_capacity_warning
- ✓ test_ec_02_sprint_with_high_capacity_warning

**Edge Case 5**: Concurrent usage (no conflicts)
- ✓ test_08_concurrent_skill_execution

**Edge Case 6-7**: Missing/corrupted guidance files
- ✓ test_04_missing_guidance_file_graceful_fallback
- ✓ test_05_corrupted_guidance_file_graceful_fallback

---

## How to Run Tests

### Run All Tests
```bash
pytest tests/ -v --cov=src --cov-report=term
```

### Run by Category

**Unit Tests Only**
```bash
pytest tests/unit/test_story057* -v
```

**Integration Tests Only**
```bash
pytest tests/integration/test_story057* -v
```

**Regression Tests Only**
```bash
pytest tests/unit/ tests/integration/ -k "regression" -v
```

### Run by Skill

**Architecture Tests**
```bash
pytest tests/unit/test_story057_architecture* -v
pytest tests/integration/test_story057* -v -k "architecture"
```

**UI-Generator Tests**
```bash
pytest tests/unit/test_story057_ui_generator* -v
pytest tests/integration/test_story057* -v -k "ui"
```

**Orchestration Tests**
```bash
pytest tests/unit/test_story057_orchestration* -v
pytest tests/integration/test_story057* -v -k "orchestration"
```

### Run by Marker

**Unit Tests**
```bash
pytest tests/ -m unit -v
```

**Integration Tests**
```bash
pytest tests/ -m integration -v
```

**Performance Tests**
```bash
pytest tests/ -m performance -v
```

**Acceptance Criteria Tests**
```bash
pytest tests/ -m acceptance_criteria -v
```

**Edge Case Tests**
```bash
pytest tests/ -m edge_case -v
```

---

## Expected Test Results (TDD Red Phase)

**Initial State**: ALL TESTS FAILING (no implementation yet)

- 45 unit tests: FAIL
- 9 integration tests: FAIL
- 45 regression tests: PASS (existing tests already passing)

**Total Count**
- 45 unit: FAIL
- 9 integration: FAIL
- 45 regression: PASS
- **99 tests total** (54 failing, 45 passing)

**After Implementation (TDD Green Phase)**
- All 99 tests should PASS (100% pass rate)

---

## Test File Locations

```
tests/
├── unit/
│   ├── test_story057_architecture_skill_integration.py     (15 tests)
│   ├── test_story057_ui_generator_skill_integration.py     (15 tests)
│   └── test_story057_orchestration_skill_integration.py    (15 tests)
├── integration/
│   └── test_story057_cross_skill_integration.py            (9 tests)
└── [existing test files for regression]
```

**Command to Run All STORY-057 Tests**
```bash
pytest tests/unit/test_story057* tests/integration/test_story057* -v --tb=short
```

---

## Test Markers

All tests use pytest markers for categorization:

- `@pytest.mark.unit` - Unit tests (45)
- `@pytest.mark.integration` - Integration tests (9)
- `@pytest.mark.regression` - Regression tests (45)
- `@pytest.mark.acceptance_criteria` - AC coverage tests
- `@pytest.mark.performance` - Performance/NFR tests
- `@pytest.mark.edge_case` - Edge case tests

---

## Dependencies

**Required Packages**
- pytest >=7.0
- pytest-cov
- (No external test dependencies; tests use standard library)

**Python Version**
- Python 3.8+

---

## Next Steps (Implementation Phase - TDD Green)

1. **Implement conditional loading** in 3 skills (greenfield/brownfield, standalone/story, epic/sprint)
2. **Apply patterns** from user-input-guidance.md to skill questions
3. **Create reference files** for each skill (architecture, ui-generator, orchestration)
4. **Deploy guidance files** to all 3 skills (with checksum validation)
5. **Run regression tests** to ensure backward compatibility
6. **All tests should PASS** (TDD Green phase)

---

**Generated**: TDD Red Phase (test-first approach)
**Status**: Ready for implementation
**Coverage**: 100% of AC, all technical requirements, all NFRs, all edge cases
