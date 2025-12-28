# STORY-140: YAML-Malformed Brainstorm Detection - Test Suite

**Status**: Test suite generated (all tests FAILING - awaiting implementation)
**Created**: 2025-12-28
**Framework**: Jest (JavaScript), Bash (Shell integration)

## Overview

This test suite validates YAML validation functionality for brainstorm file handling in the devforgeai-ideation skill. The tests are designed to FAIL initially (TDD Red phase) until the implementation is complete.

## Test Files

### 1. `/tests/STORY-140/test_brainstorm_validation.js`

**Framework**: Jest
**Purpose**: Unit and integration tests for brainstorm YAML validation
**Test Count**: 40+ test cases

This is the primary test file implementing comprehensive tests following the **AAA pattern** (Arrange, Act, Assert).

**Run with**:
```bash
npm test -- tests/STORY-140/test_brainstorm_validation.js
jest tests/STORY-140/test_brainstorm_validation.js --verbose
```

### 2. `/tests/STORY-140/test_brainstorm_validation.sh`

**Framework**: Bash
**Purpose**: Shell-based integration tests simulating skill execution
**Test Count**: 25+ test cases

This file validates YAML validation through fixture files and shell operations.

**Run with**:
```bash
bash tests/STORY-140/test_brainstorm_validation.sh
bash tests/STORY-140/test_brainstorm_validation.sh --verbose
bash tests/STORY-140/test_brainstorm_validation.sh --stop-on-failure
```

## Test Fixtures

Located in `/tests/fixtures/STORY-140/`:

| Fixture | Purpose | Expected Behavior |
|---------|---------|-------------------|
| `valid-brainstorm.md` | Valid brainstorm with all required fields | Should pass validation |
| `invalid-yaml-missing-delimiter.md` | Missing closing `---` delimiter | Error: "Unclosed YAML frontmatter" |
| `invalid-yaml-mixed-indentation.md` | Tabs mixed with spaces in YAML | Error: "Invalid indentation" |
| `invalid-yaml-duplicate-key.md` | Duplicate `id:` field | Error: "Duplicate key 'id'" |
| `invalid-yaml-bad-date.md` | `created: not-a-date` (invalid format) | Error: "Invalid date format" |
| `invalid-yaml-missing-field.md` | Missing required `id:` field | Error: "Missing required field: id" |
| `empty-file.md` | Empty file (0 bytes) | Error: "Empty file" |
| `binary-file.bin` | Binary data | Error: "Non-text file" or "Encoding error" |

## Acceptance Criteria Coverage

### AC#1: YAML Validation on Brainstorm Load

**Tests**: 3
- `test_ac1_valid_brainstorm_loads()` - Valid file loads successfully
- `test_ac1_invalid_yaml_detected()` - Invalid YAML detected before processing
- `test_ac1_validation_performance()` - Validation completes < 100ms

**What makes tests FAIL**:
- `BrainstormValidator.validate()` not yet implemented in brainstorm-handoff-workflow.md
- YAML parsing logic missing
- No validation response object returned

### AC#2: Clear Error Message on Parse Failure

**Tests**: 2
- `test_ac2_error_format_includes_file_path()` - File path in error message
- `test_ac2_error_includes_line_number()` - Line number when available

**What makes tests FAIL**:
- `YAMLErrorMapper.formatErrorMessage()` not yet implemented
- Error message format specification not met
- Line number detection logic missing

### AC#3: Graceful Fallback to Fresh Ideation

**Tests**: 1
- `test_ac3_invalid_file_does_not_crash()` - Returns error object without crashing

**What makes tests FAIL**:
- No fallback flow implemented
- Missing `canContinueWithoutBrainstorm` flag in error object
- AskUserQuestion integration not implemented

### AC#4: Validation for Common YAML Errors

**Tests**: 5
- `test_ac4_error_missing_delimiter()` - Detects missing `---`
- `test_ac4_error_mixed_indentation()` - Detects tabs mixed with spaces
- `test_ac4_error_duplicate_key()` - Detects duplicate keys
- `test_ac4_error_invalid_date_format()` - Detects invalid date values
- `test_ac4_error_missing_required_field()` - Detects missing required fields

**What makes tests FAIL**:
- YAML parser integration missing
- Error type detection logic not implemented
- Error message mapping for each error type missing

### AC#5: Brainstorm Schema Validation

**Tests**: 9
- Field validation: id pattern, title string, status enum, created date
- Optional field validation: problem_statement, key_challenges, personas
- Fail-fast behavior test

**What makes tests FAIL**:
- Schema validation rules not implemented
- Field type checking missing
- Optional field handling incomplete
- Fail-fast logic not implemented

## Business Rules (BR) Coverage

| BR | Test | Status |
|----|----|--------|
| BR-001 | `test_br001_validation_before_interaction()` | FAILING - Synchronous validation not implemented |
| BR-002 | `test_br002_graceful_error_handling()` | FAILING - Error handling not implemented |
| BR-003 | `test_br003_actionable_error_messages()` | FAILING - Error message templates missing |

## Edge Cases Coverage

| # | Scenario | Test | Status |
|---|----------|------|--------|
| 1 | Empty file | `test_edge_case_empty_file()` | FAILING |
| 2 | Binary file | `test_edge_case_binary_file()` | FAILING |
| 3 | Very large file (>1MB) | (Placeholder in JS) | SKIPPED |
| 4 | Wrong file type | (Placeholder in JS) | SKIPPED |
| 5 | Encoding issues | (Covered in binary test) | FAILING |

## Implementation Requirements

To make these tests PASS, implement the following:

### 1. BrainstormValidator Service

**Location**: `.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md`

**Required Methods**:
```javascript
class BrainstormValidator {
  // Main validation method
  static validate(filePath) {
    // Returns: { valid: boolean, error?: Error, metadata?: object }
  }

  // YAML syntax validation
  static validateYAML(filePath) {
    // Detects syntax errors
  }

  // Schema validation
  static validateSchema(frontmatter) {
    // Validates required fields and types
  }

  // Field validation
  static validateFields(metadata) {
    // Validates individual field constraints
  }
}
```

**Required Logic**:
1. Parse YAML frontmatter from brainstorm file
2. Detect all AC#4 error types (5 error types)
3. Validate schema per AC#5
4. Return structured error object with user-friendly message
5. Implement fail-fast behavior (stop on first error)

### 2. YAMLErrorMapper Service

**Location**: `.claude/skills/devforgeai-ideation/references/error-handling.md`

**Required Methods**:
```javascript
class YAMLErrorMapper {
  // Map YAML parser errors to user messages
  static mapError(yamlError) {
    // Returns: { type, message, lineNumber?, userMessage }
  }

  // Format complete error message
  static formatErrorMessage(error, filePath) {
    // Format per AC#2 specification
  }
}
```

**Required Error Messages**:
```
AC#2 Format Specification:
⚠️ Brainstorm file has invalid YAML

File: {path}
Error: {message}
Line: {line}

The file cannot be loaded in its current state.
```

### 3. Brainstorm Schema Definition

**Location**: `.claude/skills/devforgeai-brainstorming/assets/templates/brainstorm-template.md`

**Required Schema**:
```yaml
Required Fields:
- id: string, pattern: BRAINSTORM-NNN
- title: string (non-empty)
- status: enum [Active, Complete, Abandoned]
- created: date, format: YYYY-MM-DD

Optional Fields:
- problem_statement: string
- key_challenges: array of strings
- personas: array of objects
```

### 4. Skill Integration

**Location**: `.claude/skills/devforgeai-ideation/SKILL.md`

**Phase 1 Step 0**: Call BrainstormValidator.validate(brainstormPath)
- If validation fails:
  - Display error via YAMLErrorMapper
  - Offer AskUserQuestion for fallback
  - Option 1: "Yes, start fresh" → Continue without brainstorm
  - Option 2: "No, I'll fix the file first" → HALT session

## Running All Tests

### Jest Tests Only
```bash
npm test -- tests/STORY-140/
```

### Shell Tests Only
```bash
bash tests/STORY-140/test_brainstorm_validation.sh
```

### All Tests with Coverage
```bash
npm test -- tests/STORY-140/test_brainstorm_validation.js --coverage
```

### Verbose Output
```bash
bash tests/STORY-140/test_brainstorm_validation.sh --verbose
npm test -- tests/STORY-140/ --verbose
```

## Expected Test Results

### BEFORE Implementation
```
FAIL: All 40+ tests
REASON: BrainstormValidator and YAMLErrorMapper not yet implemented
```

### AFTER Implementation
```
PASS: All 40+ tests
Coverage: AC#1 (100%), AC#2 (100%), AC#3 (100%), AC#4 (100%), AC#5 (100%)
Edge Cases: (100%)
Business Rules: (100%)
```

## Test Execution Timeline

### Phase 1: Red (TDD - Current)
1. **Tests Created** ✓ (this README)
2. **Fixtures Created** ✓ (valid and invalid brainstorm files)
3. **All Tests FAIL** ✓ (awaiting implementation)

### Phase 2: Green (Implementation)
1. Implement BrainstormValidator
2. Implement YAMLErrorMapper
3. Integrate into brainstorm-handoff-workflow.md
4. Run tests → verify all PASS

### Phase 3: Refactor
1. Extract common validation logic
2. Optimize performance (ensure <100ms)
3. Improve error messages
4. Run tests again → verify all still PASS

## Troubleshooting

### Test Fixture Not Found
```bash
ls -la tests/fixtures/STORY-140/
# Verify all 8 fixtures exist
```

### Jest Configuration Issue
```bash
npm test -- tests/STORY-140/ --debug
# Check jest.config.js for test pattern matching
```

### Shell Test Permissions
```bash
chmod +x tests/STORY-140/test_brainstorm_validation.sh
bash tests/STORY-140/test_brainstorm_validation.sh
```

### YAML Parsing Library Not Available
- Consider using js-yaml library for Jest tests
- Bash can use `yq` if available, or regex-based parsing

## References

### Story Documentation
- **Story File**: `devforgeai/specs/Stories/STORY-140-yaml-malformed-brainstorm-detection.story.md`
- **AC#1**: YAML Validation on Brainstorm Load
- **AC#2**: Clear Error Message on Parse Failure
- **AC#3**: Graceful Fallback to Fresh Ideation
- **AC#4**: Validation for Common YAML Errors (5 error types)
- **AC#5**: Brainstorm Schema Validation

### Technical Specification
- **BrainstormValidator**: Service for YAML/schema validation
- **YAMLErrorMapper**: Service for error message formatting
- **BrainstormSchema**: Data model with required/optional fields
- **Business Rules**: BR-001 (validation timing), BR-002 (graceful fallback), BR-003 (actionable errors)
- **NFRs**: NFR-001 (performance <100ms), NFR-002 (no crashes)

### Implementation Files to Update
- `.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md` - Add BrainstormValidator
- `.claude/skills/devforgeai-ideation/references/error-handling.md` - Add YAMLErrorMapper
- `.claude/skills/devforgeai-ideation/SKILL.md` - Integrate validation in Phase 1

## Test Quality Metrics

- **Test Coverage**: 40+ test cases covering 5 acceptance criteria + edge cases + business rules
- **Fixtures**: 8 test fixtures (1 valid, 6 invalid with specific error types, 1 empty, 1 binary)
- **Frameworks**: 2 test frameworks (Jest for unit, Bash for integration)
- **Error Scenarios**: 8 distinct error types (missing delimiter, indentation, duplicate key, bad date, missing field, empty file, binary file, encoding)
- **Performance Tests**: 1 (validation must complete <100ms)
- **Integration Tests**: Fallback flow, error message display, AskUserQuestion support

## Status

```
STORY-140 Test Suite Status
============================
Created:       2025-12-28
Last Updated:  2025-12-28
Test Count:    40+
Fixtures:      8
Status:        READY FOR DEVELOPMENT (All tests FAILING - TDD Red phase)

Implementation can proceed. Run tests during development to verify coverage.
```
