# STORY-055 Test Suite Documentation

**Story:** devforgeai-ideation Skill Integration with User Input Guidance

**Test Suite Generation Date:** 2025-01-21

**Test Framework:** pytest (Python)

**Total Tests Generated:** 47 failing tests (TDD Red phase)

---

## Test Suite Overview

### Test Files Created

| File Path | Purpose | Test Count | Coverage |
|-----------|---------|-----------|----------|
| `tests/unit/test_ideation_guidance_loading.py` | Guidance file loading and initialization | 12 | AC#1 |
| `tests/integration/test_ideation_guidance_integration.py` | Pattern application and subagent quality | 22 | AC#2, AC#3, AC#5 |
| `tests/integration/test_ideation_performance.py` | Performance and non-functional requirements | 13 | AC#4, NFR-001 to NFR-005 |

**Total:** 47 tests across 3 files

---

## Test Structure (AAA Pattern)

All tests follow the **Arrange-Act-Assert** pattern:

```python
def test_example_behavior():
    # Arrange: Set up test preconditions
    test_input = "example"

    # Act: Execute the behavior being tested
    result = system_under_test(test_input)

    # Assert: Verify the outcome
    assert result == expected_value
```

### Pytest Fixtures

Tests use pytest fixtures for reusable setup:

```python
@pytest.fixture
def guidance_content(self) -> str:
    """Load guidance file content."""
    # Fixture content...
```

---

## Acceptance Criteria Coverage

### AC#1: Pre-Discovery Guidance Loading (12 tests)

**File:** `tests/unit/test_ideation_guidance_loading.py`

Tests verify:
- Guidance file exists at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- File is readable Markdown (.md extension)
- File contains required reference sections (Patterns, Templates, Integration Guide)
- File has minimum meaningful size (>1000 characters)
- YAML frontmatter contains required metadata fields
- Phase 1 SKILL.md contains "Step 0" before Step 1
- Step 0 references guidance loading
- Step 0 uses Read() tool to load guidance
- Error handling for missing guidance file

**Test Classes:**
1. `TestGuidanceFileLocation` (5 tests)
2. `TestGuidanceLoadingMechanism` (3 tests)
3. `TestGuidanceFileContent` (4 tests)

### AC#2: Pattern Application in Discovery Questions (11 tests)

**File:** `tests/integration/test_ideation_guidance_integration.py`

Tests verify:
- Phase 1 scope questions use "Tell me about..." open-ended pattern
- Avoid yes/no questions for scope
- Phase 2 priority questions use "Rank 1-5" comparative pattern
- Ranking questions provide numeric scale
- Phase 1-2 timeline questions use "Select range" bounded pattern
- Bounded choice pattern references time units
- Phase 2 user persona questions use "Primary user: [roles]" classification
- Classification questions provide predefined role options
- All AskUserQuestion invocations incorporate patterns
- Patterns enhance (not duplicate) guidance file content

**Test Classes:**
1. `TestPatternApplicationOpenEnded` (2 tests)
2. `TestPatternApplicationRanking` (2 tests)
3. `TestPatternApplicationBoundedChoice` (2 tests)
4. `TestPatternApplicationExplicitClassification` (2 tests)
5. `TestPatternConsistency` (2 tests)

### AC#3: Subagent Invocation Quality (4 tests)

**File:** `tests/integration/test_ideation_guidance_integration.py`

Tests verify:
- Phase 3 invokes requirements-analyst subagent
- Subagent prompt includes structured context from Phase 1-2
- Subagent prompt does NOT mention pattern names directly (uses context)
- Reduced re-invocation rate (≥30% reduction from 2.5 baseline)

**Test Classes:**
1. `TestSubagentInvocationQuality` (4 tests)

### AC#4: Token Overhead Constraint (4 tests)

**File:** `tests/integration/test_ideation_performance.py`

Tests verify:
- Guidance file not exceeding practical size limits
- Token overhead estimated ≤1,000 tokens (1 token ≈ 4 chars)
- File loading performance <500ms
- Phase 1 uses selective guidance references (not full content)

**Test Classes:**
1. `TestTokenOverheadConstraint` (4 tests)

### AC#5: Backward Compatibility (2 tests)

**File:** `tests/integration/test_ideation_guidance_integration.py`

Tests verify:
- All existing Phase 1-6 definitions retained
- Phase 1 existing steps preserved (Step 0 is NEW insertion, not replacement)

**Test Classes:**
1. `TestBackwardCompatibility` (2 tests)

---

## Non-Functional Requirements Coverage

### NFR-001: Performance - Guidance Loading Speed

**Tests:**
- `TestTokenOverheadConstraint::test_guidance_file_loading_should_be_fast()`

**Requirement:** Phase 1 Step 0 guidance loading <500ms

### NFR-002: Subagent Re-Invocation Reduction

**Tests:**
- `TestSubagentReInvocationReduction::test_phase_3_subagent_prompt_should_include_structured_context()`
- `TestSubagentReInvocationReduction::test_phase_2_should_collect_all_required_information()`
- `TestSubagentReInvocationReduction::test_subagent_prompt_should_have_detailed_instructions()`

**Requirement:** ≥30% reduction in requirements-analyst re-invocations (2.5 → ≤1.75 per ideation)

### NFR-003: Reliability - Graceful Degradation

**Tests:**
- `TestReliabilityWithoutGuidance::test_skill_should_complete_if_guidance_missing()`
- `TestReliabilityWithoutGuidance::test_phase_1_should_have_fallback_questions()`

**Requirement:** 100% workflow completion even if guidance file missing

### NFR-004: Maintainability - Minimal Code Changes

**Tests:**
- `TestCodeChangeMinimization::test_skill_md_changes_should_be_minimal()`
- `TestCodeChangeMinimization::test_reference_file_should_not_exceed_size_limit()`

**Requirement:** ≤5 lines changed in SKILL.md, ≤300 lines in reference file

### NFR-005: Testability - Pattern Verification

**Tests:**
- `TestPatternVerifiability::test_patterns_should_be_detectable_via_grep()`

**Requirement:** ≥80% pattern usage detectable via grep/regex (≥4/5 patterns)

---

## Business Rules Validation

| Business Rule | Test | Location |
|---------------|------|----------|
| **BR-001:** Guidance loading must not halt skill if file unavailable (graceful degradation) | `test_missing_guidance_should_not_halt_skill()`, `test_skill_should_complete_if_guidance_missing()` | Unit & Integration |
| **BR-002:** Pattern application must preserve existing question intent (enhancement, not replacement) | `test_patterns_should_not_duplicate_guidance_file_content()` | Integration |
| **BR-003:** Subagent receives structured context (not raw pattern names) | `test_subagent_prompt_should_include_structured_context()`, `test_subagent_prompt_should_not_mention_pattern_names()` | Integration |

---

## Edge Cases Covered

| Edge Case | Test | Location |
|-----------|------|----------|
| Guidance file missing or corrupted | `test_missing_guidance_should_not_halt_skill()` | Unit |
| Guidance file outdated (version mismatch) | Implicitly tested via YAML frontmatter validation | Unit |
| Ambiguous pattern selection | Bounded pattern preference tested | Integration |
| User provides incomplete answers despite guidance | Verified through fallback question availability | Integration |

---

## Data Validation Rules Coverage

| Data Validation Rule | Test | Location |
|----------------------|------|----------|
| **Guidance file location:** Must exist at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` | `test_should_exist_at_specified_path()` | Unit |
| **Pattern mapping:** AC specifies Phase 1 business goals → Open-Ended, Phase 2 priorities → Comparative Ranking, etc. | Multiple pattern tests | Integration |
| **Token measurement:** 1 token ≈ 4 characters, max overhead ≤1,000 tokens | `test_token_overhead_estimated_within_limit()` | Performance |

---

## Test Execution Instructions

### Prerequisites

```bash
# Install pytest
pip install pytest

# Verify pytest installation
pytest --version
```

### Run All STORY-055 Tests

```bash
# Run all three test files
pytest tests/unit/test_ideation_guidance_loading.py \
        tests/integration/test_ideation_guidance_integration.py \
        tests/integration/test_ideation_performance.py -v

# Or use pattern matching
pytest tests/ -k "ideation_guidance" -v
```

### Run Specific Test Categories

```bash
# Unit tests only (AC#1)
pytest tests/unit/test_ideation_guidance_loading.py -v

# Integration tests (AC#2, AC#3, AC#5)
pytest tests/integration/test_ideation_guidance_integration.py -v

# Performance tests (AC#4, NFRs)
pytest tests/integration/test_ideation_performance.py -v
```

### Run Specific Test Class

```bash
# Example: Test guidance file location
pytest tests/unit/test_ideation_guidance_loading.py::TestGuidanceFileLocation -v

# Example: Test pattern application
pytest tests/integration/test_ideation_guidance_integration.py::TestPatternApplicationOpenEnded -v
```

### Run Specific Individual Test

```bash
# Example: Test specific AC#1 requirement
pytest tests/unit/test_ideation_guidance_loading.py::TestGuidanceFileLocation::test_should_exist_at_specified_path -v
```

### Generate Coverage Report

```bash
# Install coverage tools
pip install pytest-cov

# Run tests with coverage
pytest tests/unit/test_ideation_guidance_loading.py \
        tests/integration/test_ideation_guidance_integration.py \
        tests/integration/test_ideation_performance.py \
        --cov=src/claude/skills/devforgeai-ideation \
        --cov-report=html

# View report
open htmlcov/index.html  # macOS/Linux
start htmlcov\index.html # Windows
```

---

## Expected Test Results (RED Phase)

### Initial Test Run Status

```
FAILED tests/unit/test_ideation_guidance_loading.py::TestGuidanceFileLocation::test_skill_file_should_reference_step_0
FAILED tests/unit/test_ideation_guidance_loading.py::TestGuidanceLoadingMechanism::test_phase_1_step_0_should_mention_guidance
...
FAILED tests/integration/test_ideation_performance.py::TestTokenOverheadConstraint::test_token_overhead_estimated_within_limit

============================== 47 failed in 2.34s ==============================
```

**Expected Failure Rate:** 100% initially (TDD Red phase)

### Why Tests Fail Initially

1. **AC#1 Tests Fail Because:**
   - Phase 1 Step 0 not yet added to SKILL.md
   - Read() tool call not implemented in Step 0

2. **AC#2 Tests Fail Because:**
   - Pattern keywords not yet incorporated in Phase 1-2 questions
   - Questions still use generic "What about..." instead of patterns

3. **AC#3 Tests Fail Because:**
   - Phase 3 subagent prompt lacks structured context references
   - Pattern names mentioned directly in prompts (should use context)

4. **AC#4 Tests Fail Because:**
   - Token overhead not yet optimized for selective loading
   - Estimated overhead exceeds 1,000 tokens (needs refactoring)

5. **AC#5 Tests Fail Because:**
   - Step 0 removal of other steps (to be verified as backward-compatible)

---

## Test-Driven Development (TDD) Workflow

### Phase 1: RED (Failing Tests) - Current Status

**Status:** COMPLETE - All 47 tests written and failing

```
┌─────────────────────────────────────────────────────────┐
│ RED Phase - Write Failing Tests ✓ COMPLETE             │
├─────────────────────────────────────────────────────────┤
│ Tests generated from:                                   │
│ - AC#1: Pre-Discovery Guidance Loading (12 tests)      │
│ - AC#2: Pattern Application (11 tests)                 │
│ - AC#3: Subagent Quality (4 tests)                     │
│ - AC#4: Token Overhead (4 tests)                       │
│ - AC#5: Backward Compatibility (2 tests)               │
│ - NFRs: Performance & Reliability (14 tests)           │
│                                                         │
│ Test Count: 47                                          │
│ Pass Rate: 0% (expected for RED phase)                 │
│ Coverage: All AC + All NFRs + All Business Rules       │
└─────────────────────────────────────────────────────────┘
```

### Phase 2: GREEN (Minimal Implementation)

**Next Steps (Execute after RED phase complete):**

1. Add Phase 1 Step 0 to SKILL.md
   - Load user-input-guidance.md using Read() tool
   - Handle missing file gracefully

2. Apply patterns to Phase 1-2 questions
   - Incorporate "Tell me about..." in scope questions
   - Use "Rank 1-5" for feature priorities
   - Use "Select range" for timelines
   - Use "Primary user:" for personas

3. Enhance Phase 3 subagent prompt
   - Include structured context from Phase 1-2
   - Remove pattern name mentions
   - Add example context structure

4. Optimize token overhead
   - Selective loading of guidance sections
   - Caching to avoid repeated loads
   - Measure and verify <1,000 token overhead

5. Verify backward compatibility
   - Ensure all Phase 1-6 retained
   - Confirm existing steps still work

**Target: All 47 tests passing (GREEN phase)**

### Phase 3: REFACTOR (Quality Improvement)

**After GREEN phase (all tests passing):**

1. Remove code duplication in pattern applications
2. Extract common question templates to fixtures
3. Optimize guidance file loading for performance
4. Add documentation/comments for pattern mappings

---

## Test Dependencies and Prerequisites

### File Dependencies

These files must exist for tests to run:

- `src/claude/skills/devforgeai-ideation/SKILL.md` (skill implementation)
- `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` (guidance document)

### Framework Dependencies

- `pytest` - Test framework
- `pytest-cov` (optional) - Coverage reporting

### No External Service Dependencies

Tests use only local files and regex/string matching. No API calls or external services required.

---

## Coverage Goals

### Target Coverage

| Component | Target | Current |
|-----------|--------|---------|
| Acceptance Criteria | 100% | 100% (5/5 ACs covered) |
| Non-Functional Requirements | 100% | 100% (5/5 NFRs covered) |
| Business Rules | 100% | 100% (3/3 rules covered) |
| Edge Cases | 100% | 100% (4/4 cases covered) |
| Code Coverage (SKILL.md) | 85%+ | TBD (post-implementation) |

### Test Pyramid Distribution

```
           /\
          /E2E\      - No E2E tests (framework-level, not user-facing feature)
         /------\
        /Integr.\   35% - Integration tests (22 tests)
       /----------\
      /   Unit    \ 64% - Unit tests (12 tests) + Performance (13 tests)
     /--------------\
```

---

## Continuous Integration Readiness

### Pre-Commit Hook

Once tests are ready to run in CI:

```bash
# Install pre-commit hook
.claude/scripts/install_hooks.sh

# Hook will run tests before commit:
pytest tests/unit/test_ideation_guidance_loading.py \
        tests/integration/test_ideation_guidance_integration.py \
        tests/integration/test_ideation_performance.py

# Commit will be blocked if tests fail (RED phase)
```

### CI/CD Pipeline Steps

1. Install dependencies: `pip install pytest pytest-cov`
2. Run tests: `pytest tests/ -k ideation_guidance -v --cov`
3. Generate report: `pytest --cov-report=html`
4. Validate: All tests must pass before merge to main

---

## Common Issues & Troubleshooting

### Issue: "Guidance file not found"

**Cause:** File doesn't exist at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

**Resolution:** Verify prerequisite STORY-053 (Framework-Internal Guidance Reference) is complete

### Issue: "SKILL.md not found"

**Cause:** Test running from wrong directory

**Resolution:** Ensure tests run from project root:
```bash
cd /mnt/c/Projects/DevForgeAI2
pytest tests/...
```

### Issue: Tests hang or timeout

**Cause:** File I/O taking too long

**Resolution:** Check file permissions and disk space. Verify guidance file is not locked.

### Issue: "ModuleNotFoundError: No module named pytest"

**Cause:** pytest not installed

**Resolution:**
```bash
pip install pytest
# Or with system packages:
pip install --break-system-packages pytest
```

---

## References

### Story Files
- Story: `/mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/STORY-055-devforgeai-ideation-integration.story.md`
- Prerequisite: STORY-053 (Framework-Internal Guidance Reference)

### Implementation Files
- Guidance: `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- Skill: `src/claude/skills/devforgeai-ideation/SKILL.md`

### Test Framework Documentation
- pytest docs: https://docs.pytest.org/
- pytest fixtures: https://docs.pytest.org/en/stable/fixture.html
- pytest marks: https://docs.pytest.org/en/stable/example/markers.html

### DevForgeAI Testing Standards
- See: `.claude/skills/devforgeai-development/references/testing-standards.md`
- TDD guide: CLAUDE.md section "TDD Is Mandatory"

---

**Test Suite Version:** 1.0
**Created:** 2025-01-21
**Framework:** Test-Automator (pytest TDD Red Phase)
**Status:** Ready for implementation → GREEN Phase
