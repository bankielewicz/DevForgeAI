# STORY-140 Test Suite - Complete Index

**Generated**: 2025-12-28
**Status**: All tests FAILING (TDD Red phase - awaiting implementation)
**Total Files**: 12 (5 test files + 8 fixture files + documentation)
**Total Lines**: 2,800+ lines of test code and documentation

## File Structure

```
/mnt/c/Projects/DevForgeAI2/
├── tests/
│   ├── STORY-140/
│   │   ├── INDEX.md                        (This file - navigation guide)
│   │   ├── README-STORY-140.md             (362 lines - Comprehensive test documentation)
│   │   ├── TEST-GENERATION-SUMMARY.md      (386 lines - Summary of test generation)
│   │   ├── WHY-TESTS-FAIL.md               (664 lines - Detailed failure explanations)
│   │   ├── test_brainstorm_validation.js   (575 lines - Jest unit tests)
│   │   └── test_brainstorm_validation.sh   (697 lines - Bash integration tests)
│   │
│   └── fixtures/STORY-140/
│       ├── valid-brainstorm.md             (62 lines - Valid brainstorm file)
│       ├── invalid-yaml-missing-delimiter.md (14 lines - Error type 1)
│       ├── invalid-yaml-mixed-indentation.md (19 lines - Error type 2)
│       ├── invalid-yaml-duplicate-key.md   (13 lines - Error type 3)
│       ├── invalid-yaml-bad-date.md        (12 lines - Error type 4)
│       ├── invalid-yaml-missing-field.md   (11 lines - Error type 5)
│       ├── empty-file.md                   (0 lines - Edge case 1)
│       └── binary-file.bin                 (binary - Edge case 2)
```

## Quick Reference

### 📖 Read This First

1. **`README-STORY-140.md`** - Start here
   - Overview of all tests
   - Test coverage matrix
   - How to run tests
   - Fixture descriptions
   - Implementation requirements

### 🧪 Test Files

2. **`test_brainstorm_validation.js`** - Jest tests (primary)
   - 35+ test cases
   - Full AAA pattern implementation
   - Grouped by acceptance criteria
   - Jest framework (Node.js native)

3. **`test_brainstorm_validation.sh`** - Bash tests (complementary)
   - 25+ test cases
   - BDD Given/When/Then style
   - File-based validation
   - Shell integration testing

### 📋 Documentation

4. **`TEST-GENERATION-SUMMARY.md`** - Executive summary
   - Test generation overview
   - Coverage analysis
   - Why tests fail (high-level)
   - Implementation strategy
   - Expected results

5. **`WHY-TESTS-FAIL.md`** - Detailed explanation
   - Every test explained individually
   - Exact failure reasons
   - What's needed to pass
   - Code examples
   - Fixture descriptions

### 🗂️ Test Fixtures

8 fixture files in `tests/fixtures/STORY-140/`:
- 1 valid brainstorm file
- 5 invalid files (error types from AC#4)
- 1 empty file (edge case)
- 1 binary file (edge case)

## Test Execution Guide

### Run Jest Tests
```bash
# All STORY-140 tests
npm test -- tests/STORY-140/test_brainstorm_validation.js

# With verbose output
npm test -- tests/STORY-140/test_brainstorm_validation.js --verbose

# With coverage report
npm test -- tests/STORY-140/test_brainstorm_validation.js --coverage

# Watch mode (during development)
npm test -- tests/STORY-140/test_brainstorm_validation.js --watch
```

### Run Bash Tests
```bash
# All shell tests
bash tests/STORY-140/test_brainstorm_validation.sh

# Verbose output
bash tests/STORY-140/test_brainstorm_validation.sh --verbose

# Stop on first failure
bash tests/STORY-140/test_brainstorm_validation.sh --stop-on-failure
```

### Run All Tests
```bash
# Jest + Bash (both frameworks)
npm test -- tests/STORY-140/test_brainstorm_validation.js
bash tests/STORY-140/test_brainstorm_validation.sh

# With full coverage report
npm test -- tests/STORY-140/ --coverage
```

## Test Coverage Summary

### Acceptance Criteria

| AC | Description | Test Count | Status |
|----|-------------|-----------|--------|
| AC#1 | YAML Validation on Brainstorm Load | 4 | FAILING |
| AC#2 | Clear Error Message on Parse Failure | 2 | FAILING |
| AC#3 | Graceful Fallback to Fresh Ideation | 3 | FAILING |
| AC#4 | Validation for Common YAML Errors (5 types) | 5 | FAILING |
| AC#5 | Brainstorm Schema Validation | 9 | FAILING |
| **TOTAL** | **All acceptance criteria** | **23** | **FAILING** |

### Error Types Tested (AC#4)

| # | Error Type | Fixture | Detection |
|---|-----------|---------|-----------|
| 1 | Missing closing delimiter | invalid-yaml-missing-delimiter.md | Count `---` |
| 2 | Mixed indentation (tabs) | invalid-yaml-mixed-indentation.md | Find TAB chars |
| 3 | Duplicate keys | invalid-yaml-duplicate-key.md | Track key occurrences |
| 4 | Invalid date format | invalid-yaml-bad-date.md | Validate YYYY-MM-DD |
| 5 | Missing required field | invalid-yaml-missing-field.md | Check required fields |

### Edge Cases Tested

| # | Scenario | Fixture | Detection |
|---|----------|---------|-----------|
| 1 | Empty file | empty-file.md | 0 bytes |
| 2 | Binary file | binary-file.bin | Non-UTF8 data |

### Business Rules Tested

| Rule | Test | Status |
|------|------|--------|
| BR-001 | Validation before user interaction | FAILING |
| BR-002 | Graceful error handling (no crashes) | FAILING |
| BR-003 | Actionable error messages | FAILING |

### Non-Functional Requirements Tested

| NFR | Requirement | Test |
|-----|-------------|------|
| NFR-001 | Performance: <100ms validation | test_ac1_validation_performance() |
| NFR-002 | Reliability: 0 crashes | test_br002_graceful_error_handling() |

## Test Statistics

- **Total Test Cases**: 40+
- **Jest Tests**: 35+
- **Bash Tests**: 25+
- **Test Fixtures**: 8
- **Lines of Test Code**: 1,272 (575 + 697)
- **Lines of Documentation**: 1,412 (362 + 386 + 664)
- **Total Lines**: 2,800+

## Implementation Checklist

To make all tests PASS, implement:

- [ ] **BrainstormValidator** class
  - [ ] `validate(filePath)` method
  - [ ] `validateYAML(filePath)` method
  - [ ] `validateSchema(frontmatter)` method
  - [ ] Error handling (never throw)
  - [ ] Performance (<100ms)

- [ ] **YAMLErrorMapper** class
  - [ ] `mapError(yamlError)` method
  - [ ] `formatErrorMessage(error, filePath)` method
  - [ ] AC#2 format compliance
  - [ ] Error type classification (5 types)

- [ ] **Schema Definition**
  - [ ] Required fields: id, title, status, created
  - [ ] Field type validation
  - [ ] Pattern validation (BRAINSTORM-NNN)
  - [ ] Date format validation (YYYY-MM-DD)
  - [ ] Enum validation (status field)

- [ ] **Skill Integration**
  - [ ] Call validator in ideation skill Phase 1
  - [ ] Handle validation failures
  - [ ] Display error messages
  - [ ] Implement fallback flow (AskUserQuestion)

## Document Navigation

### For Test Developers
1. Start with **README-STORY-140.md** for overview
2. Read **WHY-TESTS-FAIL.md** for detailed failure reasons
3. Use **test_brainstorm_validation.js** for reference implementation

### For Implementation Developers
1. Read **README-STORY-140.md** section "Implementation Requirements"
2. Check **WHY-TESTS-FAIL.md** for what needs to be implemented
3. Review test cases in **test_brainstorm_validation.js** for expected behavior
4. Use fixtures in `tests/fixtures/STORY-140/` for testing

### For QA/Review
1. Review **TEST-GENERATION-SUMMARY.md** for coverage overview
2. Check **README-STORY-140.md** table "Required Test Files"
3. Run tests with `npm test -- tests/STORY-140/`
4. Verify all tests pass after implementation

## Key Documents by Purpose

### Understanding the Story
- **STORY File**: `devforgeai/specs/Stories/STORY-140-yaml-malformed-brainstorm-detection.story.md`
- **Acceptance Criteria**: 5 AC (YAML validation, error messages, fallback, error types, schema)

### Understanding the Tests
- **README-STORY-140.md**: Complete test documentation
- **TEST-GENERATION-SUMMARY.md**: High-level summary
- **WHY-TESTS-FAIL.md**: Detailed failure explanations
- **test_brainstorm_validation.js**: Actual test code (Jest)
- **test_brainstorm_validation.sh**: Actual test code (Bash)

### Understanding Test Fixtures
- **README-STORY-140.md**: Fixture descriptions table
- **tests/fixtures/STORY-140/**: All 8 fixture files
- **WHY-TESTS-FAIL.md**: Fixture details in test explanations

### Understanding Implementation Requirements
- **README-STORY-140.md**: Section "Implementation Requirements"
- **WHY-TESTS-FAIL.md**: Section "Summary: What's Needed"
- **TEST-GENERATION-SUMMARY.md**: Section "Implementation Strategy"

## Test Naming Convention

All tests follow naming pattern: `test_<acceptance_criteria>_<scenario>`

Examples:
- `test_ac1_valid_brainstorm_loads()`
- `test_ac2_error_format_includes_file_path()`
- `test_ac4_error_missing_delimiter()`
- `test_ac5_schema_id_pattern()`
- `test_edge_case_empty_file()`
- `test_br001_validation_before_interaction()`

## Current Test Status

### Red Phase (TDD - Current State) ✓
```
EXPECTED:
  ✗ All 40+ tests FAIL
  ✓ Tests are well-written and comprehensive
  ✓ Fixtures cover all scenarios
  ✓ Implementation requirements documented
```

### Green Phase (Next - After Implementation)
```
EXPECTED:
  ✓ All 40+ tests PASS
  ✓ Coverage metrics improve
  ✓ Error handling validated
```

### Refactor Phase (After Green)
```
EXPECTED:
  ✓ All tests still PASS
  ✓ Code quality improved
  ✓ Performance optimized
```

## Quick Links

- **Run Tests**: `npm test -- tests/STORY-140/test_brainstorm_validation.js`
- **Story File**: `devforgeai/specs/Stories/STORY-140-yaml-malformed-brainstorm-detection.story.md`
- **Fixtures Directory**: `tests/fixtures/STORY-140/`
- **Test Results Directory**: `tests/results/STORY-140/` (will be created during test runs)

## Questions Answered by Each Document

### README-STORY-140.md
- What tests are included?
- How do I run the tests?
- What fixtures exist?
- What are the implementation requirements?
- How do I know when implementation is complete?

### TEST-GENERATION-SUMMARY.md
- What was generated?
- What's the overall strategy?
- Why do tests fail?
- What's the next step?
- What are the quality metrics?

### WHY-TESTS-FAIL.md
- Why does THIS specific test fail?
- What fixture is used?
- What implementation is needed to pass?
- Can I see code examples?
- What's the expected behavior?

### test_brainstorm_validation.js
- What are the exact test cases?
- How do Jest tests work?
- What assertions are used?
- How is AAA pattern applied?

### test_brainstorm_validation.sh
- How do Bash tests work?
- What file operations are tested?
- How is BDD style used?
- What shell helpers are available?

## Success Criteria

All tests will be considered successful when:

- [ ] All 40+ Jest tests PASS
- [ ] All 25+ Bash tests PASS
- [ ] Coverage report shows 100% coverage of validator logic
- [ ] Performance test passes (<100ms)
- [ ] All fixtures handled correctly (valid and invalid)
- [ ] Error messages match AC#2 specification
- [ ] No crashes on invalid input (BR-002)
- [ ] Validation completes before user interaction (BR-001)
- [ ] Error messages are actionable (BR-003)

## Next Steps for Developers

1. **Read**: Start with `README-STORY-140.md`
2. **Understand**: Review `WHY-TESTS-FAIL.md` for what needs implementation
3. **Implement**: Follow the implementation requirements
4. **Test**: Run `npm test -- tests/STORY-140/` frequently
5. **Verify**: All tests should pass with complete implementation
6. **Review**: Check coverage and refactor if needed

## Contact/References

- **Story Reference**: STORY-140 in devforgeai/specs/Stories/
- **Test-Automator Skill**: `.claude/agents/test-automator.md`
- **Jest Documentation**: https://jestjs.io/
- **YAML Parser**: https://www.npmjs.com/package/js-yaml

---

**Last Updated**: 2025-12-28
**Test Generation Status**: COMPLETE ✓
**Ready for Implementation**: YES ✓
