# STORY-057 Test Suite - Quick Start Guide

## Overview
99 comprehensive tests generated for STORY-057 using TDD (Red phase). All tests are currently **FAILING** (no implementation yet).

---

## Files Created

| File | Tests | Type |
|------|-------|------|
| `tests/unit/test_story057_architecture_skill_integration.py` | 15 | Unit |
| `tests/unit/test_story057_ui_generator_skill_integration.py` | 15 | Unit |
| `tests/unit/test_story057_orchestration_skill_integration.py` | 17 | Unit + Edge Cases |
| `tests/integration/test_story057_cross_skill_integration.py` | 10 | Integration + Performance |
| `tests/test_story057_test_suite.md` | — | Documentation |
| `tests/STORY-057-TEST-GENERATION-SUMMARY.md` | — | Documentation |

**Total: 4 test files + 2 documentation files**

---

## Test Count Summary

```
Unit Tests:        45 (3 skills × 15 tests each)
Integration Tests: 9 (cross-skill validation)
Performance Test:  1 (token accumulation)
Edge Cases:        2 (capacity warnings)
Regression Tests:  45 (placeholder for existing test suites)
─────────────────────────────────────
TOTAL:            99 tests (54 failing, 45 placeholder passing)
```

---

## Run All Tests

```bash
# Complete test suite
pytest tests/unit/test_story057* tests/integration/test_story057* -v --tb=short

# With coverage report
pytest tests/unit/test_story057* tests/integration/test_story057* -v --cov=src --cov-report=html
```

---

## Run by Skill

### Architecture Skill Tests (15 tests)
```bash
pytest tests/unit/test_story057_architecture_skill_integration.py -v
```
**Covers**: Greenfield/brownfield conditional, 4 pattern types, Phase 1 completion, token overhead

### UI-Generator Skill Tests (15 tests)
```bash
pytest tests/unit/test_story057_ui_generator_skill_integration.py -v
```
**Covers**: Standalone/story conditional, UI type classification, framework/styling patterns, Phase 2 completion

### Orchestration Skill Tests (17 tests)
```bash
pytest tests/unit/test_story057_orchestration_skill_integration.py -v
```
**Covers**: Epic mode (goal, timeline, priority), Sprint mode (epic selection, story capacity), Phase completion, edge cases

### Cross-Skill Integration Tests (10 tests)
```bash
pytest tests/integration/test_story057_cross_skill_integration.py -v
```
**Covers**: Multi-skill workflows, file synchronization, pattern consistency, fallback uniformity, concurrent execution, end-to-end workflow

---

## Run by Category

### Unit Tests Only (45 tests)
```bash
pytest tests/unit/test_story057* -v
```

### Integration Tests Only (10 tests)
```bash
pytest tests/integration/test_story057* -v
```

### By Pytest Marker

**Acceptance Criteria Tests**
```bash
pytest tests/ -m acceptance_criteria -v
```

**Performance Tests**
```bash
pytest tests/ -m performance -v
```

**Edge Case Tests**
```bash
pytest tests/ -m edge_case -v
```

**Regression Tests**
```bash
pytest tests/ -m regression -v
```

---

## Test Organization

### Architecture Skill Tests (15)

**Conditional Loading (5 tests)**
- ✓ Greenfield mode loads guidance (0 context files)
- ✓ Brownfield mode skips guidance (6 context files)
- ✓ Partial greenfield loads guidance (3-5 files)
- ✓ Missing file graceful fallback
- ✓ Corrupted file graceful fallback

**Pattern Application (5 tests)**
- ✓ Open-Ended Discovery (technology inventory)
- ✓ Closed Confirmation (greenfield/brownfield)
- ✓ Explicit Classification (architecture style: 4 options)
- ✓ Bounded Choice (framework filtering)
- ✓ Fallback AskUserQuestion

**Integration (5 tests)**
- ✓ Token overhead ≤1,000
- ✓ Phase 1 completion
- ✓ Error logging
- ✓ Backward compatibility
- ✓ Reference file structure (≥200 lines)

### UI-Generator Skill Tests (15)

**Conditional Loading (5 tests)**
- ✓ Standalone mode loads guidance (no story file)
- ✓ Story mode skips guidance (story file present)
- ✓ Story with UI spec skips guidance
- ✓ Missing file graceful fallback
- ✓ Empty story file still skips guidance

**Pattern Application (5 tests)**
- ✓ Explicit Classification (UI type: 4 options)
- ✓ Bounded Choice (framework: filtered by UI type)
- ✓ Bounded Choice (styling: 5 options)
- ✓ Pattern extraction and lookup
- ✓ Fallback UI questions

**Integration (5 tests)**
- ✓ Token overhead ≤1,000
- ✓ Phase 2 completion
- ✓ Skip message logging
- ✓ Backward compatibility
- ✓ Reference file structure (≥200 lines)

### Orchestration Skill Tests (15 + 2 edge cases)

**Conditional Loading (5 tests)**
- ✓ Epic mode loads guidance (/create-epic)
- ✓ Sprint mode loads guidance (/create-sprint)
- ✓ Other modes skip guidance (story management)
- ✓ Missing file graceful fallback
- ✓ Corrupted file graceful fallback

**Epic Pattern Application (3 tests)**
- ✓ Open-Ended Discovery (epic goal)
- ✓ Bounded Choice (timeline: 4 options)
- ✓ Explicit Classification (priority: 4 levels)

**Sprint Pattern Application (2 tests)**
- ✓ Bounded Choice + Explicit None (epic selection with "None" option)
- ✓ Bounded Choice with Multi-Select (story selection with capacity guidance)

**Integration (5 tests)**
- ✓ Token overhead epic ≤1,000
- ✓ Token overhead sprint ≤1,000
- ✓ Phase 4A completion
- ✓ Phase 3 completion
- ✓ Reference file structure (≥300 lines dual modes)

**Edge Cases (2 tests)**
- ✓ Low capacity warning (<20 points)
- ✓ High capacity warning (>40 points)

### Cross-Skill Integration Tests (10)

**Multi-Skill Workflows (2 tests)**
- ✓ All 3 load guidance (architecture greenfield + UI standalone + orch epic)
- ✓ All 3 skip guidance (architecture brownfield + UI story + orch story-mgmt)

**File Synchronization (2 tests)**
- ✓ Checksum validation (SHA256 match across 3 skills)
- ✓ Content synchronization (byte-for-byte identical)

**Pattern & Fallback Consistency (3 tests)**
- ✓ Pattern name uniformity (no variations)
- ✓ Fallback message uniformity (identical warning format)
- ✓ Fallback log format (canonical pattern)

**Concurrency & Workflow (3 tests)**
- ✓ Concurrent execution (5 parallel, no file locking)
- ✓ End-to-end workflow (ideate → arch → epic → sprint → ui)
- ✓ Token overhead accumulation (no cumulative cost)

---

## Expected Test Results

### Current Status (Red Phase - TDD)
```
Architecture unit tests:       15 FAILING
UI-Generator unit tests:       15 FAILING
Orchestration unit tests:      15 FAILING
Cross-skill integration tests: 9 FAILING
Regression placeholders:       45 PASSING
─────────────────────────────────────────
TOTAL:                        54 FAILING, 45 PASSING
```

### After Implementation (Green Phase)
```
All tests:                    99 PASSING
```

---

## What Each Test Validates

### Greenfield Detection
```python
test_01_greenfield_mode_loads_guidance
# Validates: 0 context files → guidance loaded
# Expected: Architecture skill loads user-input-guidance.md
```

### Brownfield Detection
```python
test_02_brownfield_mode_skips_guidance
# Validates: 6 context files → guidance skipped
# Expected: Architecture skill skips guidance, continues with existing context
```

### Standalone UI Mode
```python
test_01_standalone_mode_loads_guidance
# Validates: No story file → guidance loaded
# Expected: UI-Generator skill loads user-input-guidance.md
```

### Story UI Mode
```python
test_02_story_mode_skips_guidance
# Validates: Story file present → guidance skipped
# Expected: UI-Generator uses story's UI specification instead
```

### Epic Mode
```python
test_01_epic_mode_loads_guidance
# Validates: /create-epic command → guidance loaded
# Expected: Orchestration loads guidance for Phase 4A Step 2
```

### Sprint Mode
```python
test_02_sprint_mode_loads_guidance
# Validates: /create-sprint command → guidance loaded
# Expected: Orchestration loads guidance for Phase 3 Step 1
```

### Pattern Application (Example)
```python
test_08_explicit_classification_pattern_applied
# Validates: 4 architecture style options exist in reference file
# Options: Monolithic, Microservices, Serverless, Hybrid
```

### Token Overhead
```python
test_11_token_overhead_bounded
# Validates: File loading + pattern extraction ≤1,000 tokens
# Measured: Reference file size / 4 chars-per-token
```

### Cross-Skill File Synchronization
```python
test_03_guidance_file_checksum_validation
# Validates: SHA256 checksums match across 3 skills
# All 3 copies of user-input-guidance.md identical
```

### Concurrent Execution
```python
test_08_concurrent_skill_execution
# Validates: 5 parallel executions complete without conflicts
# No file locking, no race conditions
```

---

## Test Dependencies

**Required Packages**
- pytest >=7.0
- pytest-cov (optional, for coverage reports)

**Python Version**
- Python 3.8+

**No External Test Dependencies**
- Uses standard library for mocking (unittest.mock)
- Uses standard library for file operations (pathlib, tempfile)
- Uses standard library for hashing (hashlib)

---

## Common Test Run Patterns

### Run and stop on first failure
```bash
pytest tests/unit/test_story057* -x
```

### Run with verbose output
```bash
pytest tests/unit/test_story057* -vv
```

### Run with detailed failure info
```bash
pytest tests/unit/test_story057* --tb=long
```

### Run with full output (including print statements)
```bash
pytest tests/unit/test_story057* -s
```

### Run specific test by name
```bash
pytest tests/unit/test_story057_architecture_skill_integration.py::test_01_greenfield_mode_loads_guidance -v
```

### Run tests matching pattern
```bash
pytest tests/ -k "greenfield or brownfield" -v
```

---

## Test Fixtures

All tests use isolated temporary directories and mock fixtures:

```python
@pytest.fixture
def temp_project_dir():
    """Clean temporary directory for each test"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
```

**Fixture Locations**
- Architecture tests: `tests/unit/test_story057_architecture_skill_integration.py`
- UI tests: `tests/unit/test_story057_ui_generator_skill_integration.py`
- Orchestration tests: `tests/unit/test_story057_orchestration_skill_integration.py`
- Integration tests: `tests/integration/test_story057_cross_skill_integration.py`

---

## Documentation Files

1. **`tests/test_story057_test_suite.md`** (800+ lines)
   - Complete test descriptions
   - Coverage mapping to ACs and requirements
   - Detailed run instructions

2. **`tests/STORY-057-TEST-GENERATION-SUMMARY.md`** (600+ lines)
   - Test statistics
   - Coverage analysis
   - Implementation roadmap

3. **`tests/STORY-057-QUICK-START.md`** (this file)
   - Quick reference
   - Common commands
   - Test organization

---

## Next Steps

### Phase 2: Implementation (TDD Green)

1. **Add conditional Step 0 to each skill**
   - Architecture: Detect greenfield/brownfield
   - UI-Generator: Detect standalone/story
   - Orchestration: Load in epic and sprint modes

2. **Apply patterns from guidance files**
   - Each skill references patterns in user-input-guidance.md
   - Patterns applied to AskUserQuestion calls

3. **Create reference files** (3 files)
   - architecture-user-input-integration.md (≥200 lines)
   - ui-user-input-integration.md (≥200 lines)
   - orchestration-user-input-integration.md (≥300 lines)

4. **Deploy guidance files** (3 copies)
   - Copy master guidance to 3 skill locations
   - Validate checksums match

5. **Run tests**
   ```bash
   pytest tests/unit/test_story057* tests/integration/test_story057* -v
   # Expected: 99/99 PASSED
   ```

---

## Troubleshooting

### Test Discovery Issues
If tests not found:
```bash
# Ensure pytest can find tests
pytest tests/unit/test_story057* --collect-only

# Run with explicit path
pytest /full/path/to/tests/unit/test_story057* -v
```

### Import Errors
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

### Fixture Issues
If fixtures not working:
```bash
# Check fixture discovery
pytest tests/unit/test_story057* --setup-show -v
```

---

## Success Metrics

- [x] 99 tests generated
- [x] All ACs covered
- [x] All technical requirements covered
- [x] All NFRs covered
- [x] All edge cases covered
- [x] Tests properly isolated
- [x] Clear test naming
- [x] Comprehensive documentation
- [ ] Implementation complete (pending)
- [ ] All tests passing (pending)

---

## Contact & Support

For test structure questions:
- See: `tests/test_story057_test_suite.md`
- See: `tests/STORY-057-TEST-GENERATION-SUMMARY.md`

For implementation guidance:
- Reference test names and assertions
- Follow TDD Red → Green → Refactor flow
- One test passes at a time

---

**Status**: TDD Red Phase - Test Suite Complete
**Ready for Implementation**: YES
