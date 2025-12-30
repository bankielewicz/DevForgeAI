# STORY-155 Test Suite Index

**Story**: STORY-155 - RCA Document Parsing
**Generated**: 2025-12-30
**Phase**: Phase 02 (TDD Red - Test First)
**Total Tests**: 75 (all failing)
**Total Test Code**: 2,876 lines of Bash

---

## Test Files Generated

### 1. AC#1: Frontmatter Parsing
**File**: `test-rca-parser-ac1-frontmatter.sh` (335 lines)

Tests for parsing YAML frontmatter from RCA markdown files.

- Extract `id`, `title`, `date`, `severity`, `status`, `reporter`
- Validate enum values (severity, status)
- Validate formats (id=RCA-NNN, date=YYYY-MM-DD)
- Handle malformed/missing frontmatter

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Key Tests**:
- `test_parse_frontmatter_extracts_id`
- `test_frontmatter_severity_enum_validation`
- `test_frontmatter_malformed_yaml`
- `test_frontmatter_missing_frontmatter_markers`

**Run**:
```bash
bash test-rca-parser-ac1-frontmatter.sh
```

---

### 2. AC#2: Recommendation Extraction
**File**: `test-rca-parser-ac2-recommendations.sh` (442 lines)

Tests for extracting recommendation sections from RCA markdown.

- Parse `### REC-N: PRIORITY - Title` format
- Extract id, priority, title, description
- Maintain document order
- Handle multiple recommendations
- Detect malformed headers

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Key Tests**:
- `test_extract_multiple_recommendations`
- `test_extract_recommendations_in_document_order`
- `test_validate_recommendation_priority_enum`
- `test_detect_duplicate_recommendation_ids`

**Run**:
```bash
bash test-rca-parser-ac2-recommendations.sh
```

---

### 3. AC#3: Effort Estimation
**File**: `test-rca-parser-ac3-effort.sh` (503 lines)

Tests for extracting and converting effort estimates.

- Parse hours: `**Effort Estimate:** 8 hours`
- Parse story points: `**Effort Estimate:** 5 story points`
- Convert points to hours (1 point = 4 hours)
- Handle mixed units, decimals, edge cases

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Key Tests**:
- `test_extract_effort_hours`
- `test_convert_story_points_to_hours`
- `test_filter_with_story_point_conversion`
- `test_conversion_calculation`

**Business Rules**:
- BR-003: Story Point Conversion (1 point = 4 hours)

**Run**:
```bash
bash test-rca-parser-ac3-effort.sh
```

---

### 4. AC#4: Success Criteria
**File**: `test-rca-parser-ac4-success-criteria.sh` (528 lines)

Tests for extracting success criteria checklists.

- Parse `**Success Criteria:**` section
- Extract checkbox items: `- [ ] Item`
- Associate with parent recommendation
- Handle various list formats
- Strip checkbox markers

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Key Tests**:
- `test_extract_success_criteria_basic`
- `test_associate_criteria_with_recommendation`
- `test_success_criteria_with_markdown_formatting`
- `test_numbered_list_success_criteria`

**Run**:
```bash
bash test-rca-parser-ac4-success-criteria.sh
```

---

### 5. AC#5: Filtering & Sorting
**File**: `test-rca-parser-ac5-filtering.sh` (575 lines)

Tests for filtering by effort threshold and sorting by priority.

- Filter recommendations by effort_hours >= threshold
- Sort by priority: CRITICAL > HIGH > MEDIUM > LOW
- Apply story point conversion before threshold
- Maintain document order within priority groups

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Business Rules**:
- BR-001: Effort Threshold Filter
- BR-002: Priority Sorting
- BR-003: Story Point Conversion

**Key Tests**:
- `test_filter_recommendations_threshold_2`
- `test_sort_critical_first`
- `test_filter_with_story_point_conversion`
- `test_verify_priority_order_output`

**Run**:
```bash
bash test-rca-parser-ac5-filtering.sh
```

---

### 6. Integration Tests
**File**: `test-rca-parser-integration.sh` (493 lines)

End-to-end integration tests validating complete workflows.

- Parse complete RCA with all components
- Filter and sort in single workflow
- Verify data model relationships
- Validate error handling
- Test performance (<500ms for 100 recommendations)

**Test Count**: 15
**Tests Status**: All FAILING (ready to implement)

**Key Tests**:
- `test_parse_complete_rca_structure`
- `test_filter_sort_complete_rca`
- `test_performance_large_rca`
- `test_end_to_end_parsing_workflow`

**Run**:
```bash
bash test-rca-parser-integration.sh
```

---

## Quick Reference

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2/tests/results/STORY-155/

# Run each test file in sequence
bash test-rca-parser-ac1-frontmatter.sh
bash test-rca-parser-ac2-recommendations.sh
bash test-rca-parser-ac3-effort.sh
bash test-rca-parser-ac4-success-criteria.sh
bash test-rca-parser-ac5-filtering.sh
bash test-rca-parser-integration.sh
```

### Run By Category
```bash
# All frontmatter tests
bash test-rca-parser-ac1-frontmatter.sh

# All recommendation extraction tests
bash test-rca-parser-ac2-recommendations.sh

# All effort estimation tests
bash test-rca-parser-ac3-effort.sh

# All success criteria tests
bash test-rca-parser-ac4-success-criteria.sh

# All filtering/sorting tests
bash test-rca-parser-ac5-filtering.sh

# All integration tests
bash test-rca-parser-integration.sh
```

---

## Test Statistics

### By Acceptance Criteria
| AC | Tests | Lines | Status |
|----|-------|-------|--------|
| AC#1 | 15 | 335 | FAILING |
| AC#2 | 15 | 442 | FAILING |
| AC#3 | 15 | 503 | FAILING |
| AC#4 | 15 | 528 | FAILING |
| AC#5 | 15 | 575 | FAILING |
| Integration | 15 | 493 | FAILING |
| **TOTAL** | **75** | **2,876** | **FAILING** |

### Coverage Distribution
- **Unit Tests** (AC#1-#4): 60 tests (80%)
- **Integration Tests**: 15 tests (20%)

### Test Types
- **Component Tests**: 45 tests (parse, extract, validate)
- **Business Logic Tests**: 15 tests (filter, sort, convert)
- **Integration Tests**: 15 tests (end-to-end workflows)

---

## Documentation Files

### Core Documentation
- **TEST-GENERATION-SUMMARY.md** - Detailed test breakdown with implementation checklist
- **RUN-ALL-TESTS.md** - Test execution guide with examples
- **INDEX.md** - This file (quick reference)

### Story File
- `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-155-rca-document-parsing.story.md`

### Tech Stack Reference
- `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md`

### Source Tree Reference
- `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/source-tree.md`

---

## Implementation Roadmap

### Phase 02 ✓ (Complete - Test First)
- [x] Generate 75 failing tests
- [x] Cover all 5 acceptance criteria
- [x] Include integration tests
- [x] Document test infrastructure

### Phase 03 (Next - Implementation)
- [ ] Implement RCAParser service
- [ ] Implement RCADocument model
- [ ] Implement Recommendation model
- [ ] Parse frontmatter (AC#1)
- [ ] Extract recommendations (AC#2)
- [ ] Handle effort estimates (AC#3)
- [ ] Extract success criteria (AC#4)
- [ ] Implement filtering & sorting (AC#5)
- [ ] Make all 75 tests pass

### Phase 04 (Refactoring)
- [ ] Improve code quality
- [ ] Reduce complexity
- [ ] Enhance maintainability
- [ ] Keep tests passing

### Phase 05 (Integration Testing)
- [ ] Test with real RCA files
- [ ] Validate against devforgeai/RCA/ directory
- [ ] Verify performance requirements
- [ ] Test error handling

---

## Test Data

All tests create temporary test files in `/tmp/`:

- `test-rca-valid.md` - Valid RCA with all fields
- `test-rca-recommendations.md` - 4 recommendations with varied priorities
- `test-rca-effort-hours.md` - Effort in hours
- `test-rca-story-points.md` - Effort in story points
- `test-rca-success-criteria.md` - With checklist items
- `test-rca-filter.md` - For filtering tests
- `test-rca-integration.md` - Comprehensive RCA
- And 10+ additional test data files

---

## Business Rules Tested

### BR-001: Effort Threshold Filter
Filter recommendations where effort_hours >= threshold

Tests: 18 across AC#5 and integration

### BR-002: Priority Sorting
Sort by priority: CRITICAL > HIGH > MEDIUM > LOW

Tests: 9 across AC#5 and integration

### BR-003: Story Point Conversion
Convert story points to hours: 1 point = 4 hours

Tests: 8 across AC#3, AC#5, and integration

---

## Non-Functional Requirements Tested

### Performance
- Parse single RCA file in <500ms
- Test: `test_performance_large_rca`
- Validates parsing 100 recommendations

### Reliability
- Graceful degradation on malformed sections
- No exceptions on missing optional fields
- Tests: Multiple malformed input tests

### Maintainability
- Parser logic in command markdown
- No external dependencies
- Uses only native Claude Code tools

---

## Acceptance Criteria Verification

### AC#1: Parse RCA Frontmatter ✓
- 15 tests covering frontmatter parsing
- Validates all required fields
- Tests enum and format validation
- All FAILING (ready to implement)

### AC#2: Extract Recommendations ✓
- 15 tests covering recommendation extraction
- Tests multi-recommendation handling
- Validates document order preservation
- All FAILING (ready to implement)

### AC#3: Extract Effort Estimates ✓
- 15 tests covering effort extraction
- Tests story point conversion (1 point = 4 hours)
- Tests mixed units handling
- All FAILING (ready to implement)

### AC#4: Extract Success Criteria ✓
- 15 tests covering success criteria extraction
- Tests parent-child association
- Tests various list formats
- All FAILING (ready to implement)

### AC#5: Filter & Sort ✓
- 15 tests covering filtering and sorting
- Tests business rules (BR-001, BR-002, BR-003)
- Tests edge cases
- All FAILING (ready to implement)

---

## TDD Workflow Status

### Red Phase (COMPLETE)
- [x] 75 failing tests written
- [x] All acceptance criteria covered
- [x] All edge cases documented
- [x] Tests ready for implementation

### Green Phase (NEXT)
- [ ] Implementation to make tests pass
- [ ] Code must satisfy all test requirements
- [ ] All 75 tests should pass

### Refactor Phase (AFTER GREEN)
- [ ] Improve code quality
- [ ] Reduce complexity
- [ ] Enhance maintainability
- [ ] Tests remain passing

---

## Getting Started

1. **Read the story**: `STORY-155-rca-document-parsing.story.md`
2. **Review test summary**: `TEST-GENERATION-SUMMARY.md`
3. **Run tests to see what's needed**: `bash test-rca-parser-ac1-frontmatter.sh`
4. **Implement parser** to make tests pass
5. **Verify all 75 tests pass** before moving to refactoring

---

## Contact & References

- **Story Location**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-155-rca-document-parsing.story.md`
- **Test Location**: `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-155/`
- **Tech Stack**: See `devforgeai/specs/context/tech-stack.md`

---

**Test Suite Status**: Ready for Phase 03 (Green - Implementation)
**Last Updated**: 2025-12-30
**TDD Phase**: Red (Test First)
