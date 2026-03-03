# Why STORY-140 Tests FAIL - Detailed Explanation

**Purpose**: This document explains exactly why each test fails and what implementation is needed to make it pass.

## Test Failure Mechanism (TDD Red Phase)

All tests fail because the required services are NOT YET IMPLEMENTED:

```javascript
// Current behavior when tests run:
BrainstormValidator.validate(filePath);
// Result: Error thrown
// Message: "BrainstormValidator.validate() not yet implemented"
```

## Test Categories and Failure Reasons

### Category 1: AC#1 YAML Validation Tests (4 tests)

#### Test: `test_ac1_valid_brainstorm_loads()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
expect(result.valid).toBe(true);
expect(result.metadata.id).toBe('BRAINSTORM-001');
```

**Why it FAILS**:
1. `BrainstormValidator` class doesn't exist in brainstorm-handoff-workflow.md
2. `validate()` method throws: "not yet implemented"
3. Test expectation never reached

**What's needed to PASS**:
- Implement `BrainstormValidator.validate(filePath)` method
- Read file at filePath
- Extract YAML frontmatter (lines between `---`)
- Parse YAML into object
- Return object with `{ valid: true, metadata: {...} }`

---

#### Test: `test_ac1_invalid_yaml_detected()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(invalidPath);
expect(result.valid).toBe(false);
expect(result.error.type).toBe('YAML_PARSE_ERROR');
```

**Fixture**: `invalid-yaml-missing-delimiter.md`
```markdown
---
id: BRAINSTORM-002
title: Payment Processing System
status: Active
created: 2025-12-20
# ← Missing closing --- here
# File continues with content
```

**Why it FAILS**:
1. YAML parser not invoked (BrainstormValidator doesn't exist)
2. Error detection logic not implemented
3. Missing closing delimiter not detected

**What's needed to PASS**:
- Parse file and count `---` delimiters
- Detect if count is < 2 (missing closing)
- Return error with type: `UNCLOSED_FRONTMATTER` or `YAML_PARSE_ERROR`
- Set `valid: false`

---

#### Test: `test_ac1_validation_performance()`

**What it tests**:
```javascript
const startTime = Date.now();
BrainstormValidator.validate(filePath);
const elapsed = Date.now() - startTime;
expect(elapsed).toBeLessThan(100); // Must be < 100ms
```

**Why it FAILS**:
1. BrainstormValidator doesn't exist (no timing possible)
2. Test never reaches assertion

**What's needed to PASS**:
- Implement efficient validation (synchronous, no I/O loops)
- Use native fs.readFileSync (not async)
- Simple regex/string operations for YAML parsing
- Target: Complete validation in <100ms

---

#### Test: `test_ac1_validation_required_fields()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
expect(result.metadata).toHaveProperty('id');
expect(result.metadata).toHaveProperty('title');
expect(result.metadata).toHaveProperty('status');
expect(result.metadata).toHaveProperty('created');
```

**Why it FAILS**:
1. `validate()` method not implemented
2. Metadata object not returned
3. Field extraction logic missing

**What's needed to PASS**:
- Parse YAML frontmatter from valid brainstorm
- Extract all 4 required fields
- Return in metadata object: `{ id, title, status, created }`

---

### Category 2: AC#2 Error Message Format Tests (2 tests)

#### Test: `test_ac2_error_format_includes_file_path()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(invalidPath);
expect(result.error.message).toContain(invalidPath);
```

**Fixture**: Any invalid YAML file
**Expected message format** (from AC#2):
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/brainstorm.md
Error: Unclosed YAML frontmatter - missing closing ---
Line: 5

The file cannot be loaded in its current state.
```

**Why it FAILS**:
1. Error object not created
2. Message formatting logic doesn't exist
3. File path not included in error

**What's needed to PASS**:
- Implement `YAMLErrorMapper.formatErrorMessage(error, filePath)`
- Include file path in message
- Follow exact format from AC#2 spec
- Return error.userMessage with complete formatted message

---

#### Test: `test_ac2_error_includes_line_number()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.lineNumber).toBeGreaterThan(0);
```

**Fixture**: `invalid-yaml-duplicate-key.md`
```yaml
---
id: BRAINSTORM-004           ← First occurrence (line 2)
title: Real-time Chat System
id: BRAINSTORM-004-DUPLICATE ← Second occurrence (line 4) - DUPLICATE
```

**Why it FAILS**:
1. YAML parser not integrated
2. Line number tracking not implemented
3. Duplicate key detection missing

**What's needed to PASS**:
- When parsing YAML, track line numbers
- Detect duplicate keys during parsing
- Return `error.lineNumber` set to the line of second occurrence
- Example: `{ lineNumber: 4, message: "Duplicate key 'id' at line 4" }`

---

### Category 3: AC#3 Graceful Fallback Tests (3 tests)

#### Test: `test_ac3_invalid_file_does_not_crash()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(invalidPath);
expect(result).toBeDefined();
expect(result.valid).toBe(false);
expect(result.error).toBeDefined();
expect(result.error.canContinueWithoutBrainstorm).toBe(true);
```

**Why it FAILS**:
1. Validator throws error instead of returning error object
2. No try/catch in test mock
3. `canContinueWithoutBrainstorm` flag not present

**What's needed to PASS**:
- Never throw errors in BrainstormValidator
- Always return result object: `{ valid: boolean, error?: object }`
- If validation fails, add flag: `error.canContinueWithoutBrainstorm: true`
- This allows AC#3 fallback: "Continue without brainstorm" option

---

### Category 4: AC#4 Common YAML Error Tests (5 tests)

#### Test: `test_ac4_error_missing_delimiter()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.type).toMatch(/UNCLOSED|MISSING.*DELIMITER/i);
expect(result.error.message).toMatch(/Unclosed YAML frontmatter/i);
```

**Fixture**: `invalid-yaml-missing-delimiter.md` (only 1 `---` instead of 2)

**Why it FAILS**:
1. No YAML parsing (BrainstormValidator not implemented)
2. Delimiter detection logic not implemented
3. Error type classification missing

**What's needed to PASS**:
- Count `---` delimiters at start of file
- If count < 2: error type = `UNCLOSED_FRONTMATTER`
- Error message: "Unclosed YAML frontmatter - missing closing ---"
- Return error object with these values

---

#### Test: `test_ac4_error_mixed_indentation()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.type).toMatch(/INDENTATION/i);
expect(result.error.message).toMatch(/indentation|use spaces only/i);
expect(result.error.lineNumber).toBeGreaterThan(0);
```

**Fixture**: `invalid-yaml-mixed-indentation.md`
```yaml
---
key_challenges:
	- Challenge 1 (TAB indent) ← Line 4 - TAB character
  - Challenge 2 (space indent) ← Line 5 - 2 spaces
  	- Challenge 3 (mixed)     ← Line 6 - both
```

**Why it FAILS**:
1. YAML validation not checking indentation
2. Tab character detection not implemented
3. Line number tracking missing

**What's needed to PASS**:
- Scan YAML frontmatter for TAB characters (U+0009)
- If found: error type = `INVALID_INDENTATION`
- Error message: "Invalid indentation at line {N} - use spaces only"
- Extract line number where tab is first found

---

#### Test: `test_ac4_error_duplicate_key()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.type).toMatch(/DUPLICATE/i);
expect(result.error.message).toMatch(/duplicate key|'id'/i);
expect(result.error.lineNumber).toBeGreaterThan(0);
```

**Fixture**: `invalid-yaml-duplicate-key.md`
```yaml
id: BRAINSTORM-004           ← First id
title: Real-time Chat System
id: BRAINSTORM-004-DUPLICATE ← Duplicate!
```

**Why it FAILS**:
1. YAML parser doesn't detect or report duplicates
2. Duplicate key tracking not implemented
3. Line number of duplicate not recorded

**What's needed to PASS**:
- While parsing YAML, track all keys seen
- If key seen again: error type = `DUPLICATE_KEY`
- Error message: "Duplicate key 'id' at line {N}"
- Set lineNumber to the line of the second occurrence

---

#### Test: `test_ac4_error_invalid_date_format()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.type).toMatch(/DATE|FORMAT/i);
expect(result.error.message).toMatch(/date|YYYY-MM-DD/i);
```

**Fixture**: `invalid-yaml-bad-date.md`
```yaml
---
id: BRAINSTORM-005
title: Analytics Dashboard
status: Active
created: not-a-date  ← Invalid date value
```

**Why it FAILS**:
1. Schema validation not implemented
2. Date format checking not in place
3. No validation of field values

**What's needed to PASS**:
- After parsing YAML, validate 'created' field
- Check if value matches YYYY-MM-DD pattern: `^\d{4}-\d{2}-\d{2}$`
- If not: error type = `INVALID_DATE_FORMAT`
- Error message: "Invalid date format for 'created' field - expected YYYY-MM-DD"

---

#### Test: `test_ac4_error_missing_required_field()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error.type).toMatch(/MISSING|REQUIRED/i);
expect(result.error.message).toMatch(/missing.*id|required field|'id'/i);
```

**Fixture**: `invalid-yaml-missing-field.md`
```yaml
---
title: Search Engine Integration
status: Active
created: 2025-12-20
# ← Missing 'id' field
```

**Why it FAILS**:
1. Schema validation not implemented
2. Required field checking missing
3. No validation after YAML parse

**What's needed to PASS**:
- After parsing YAML, check for all 4 required fields: `id`, `title`, `status`, `created`
- If any missing: error type = `MISSING_REQUIRED_FIELD`
- Error message: "Missing required field: id"
- Implement fail-fast: return on FIRST missing field, not all

---

### Category 5: AC#5 Schema Validation Tests (9 tests)

#### Test: `test_ac5_schema_id_pattern()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
expect(result.metadata.id).toMatch(/^BRAINSTORM-\d+$/);
```

**Why it FAILS**:
1. Metadata not extracted from valid brainstorm
2. No id pattern validation
3. Fixture has valid id (BRAINSTORM-001) but not returned

**What's needed to PASS**:
- Parse valid brainstorm file
- Extract `id` field
- Validate pattern: must start with `BRAINSTORM-` followed by digits
- Return in metadata if valid

---

#### Test: `test_ac5_schema_title_is_string()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
expect(typeof result.metadata.title).toBe('string');
expect(result.metadata.title.length).toBeGreaterThan(0);
```

**Why it FAILS**:
1. Title not extracted from valid brainstorm
2. No type checking
3. Metadata object missing

**What's needed to PASS**:
- Parse YAML and extract title field
- Ensure it's a non-empty string
- Return in metadata

---

#### Test: `test_ac5_schema_status_is_enum()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
const validStatuses = ['Active', 'Complete', 'Abandoned'];
expect(validStatuses).toContain(result.metadata.status);
```

**Why it FAILS**:
1. Status not extracted
2. No enum validation
3. Metadata missing

**What's needed to PASS**:
- Extract status field from YAML
- Validate it's one of: `Active`, `Complete`, or `Abandoned`
- Return in metadata

---

#### Test: `test_ac5_schema_created_is_date()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
expect(result.metadata.created).toMatch(/^\d{4}-\d{2}-\d{2}$/);
```

**Why it FAILS**:
1. Created date not extracted
2. No date format validation for valid files
3. Metadata missing

**What's needed to PASS**:
- Extract created field
- Validate YYYY-MM-DD format
- Return in metadata

---

#### Test: `test_ac5_schema_optional_fields()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(validPath);
if (result.metadata.problem_statement !== undefined) {
  expect(typeof result.metadata.problem_statement).toBe('string');
}
```

**Why it FAILS**:
1. Optional fields not extracted
2. Metadata missing

**What's needed to PASS**:
- If optional fields present in YAML, extract them
- Validate their types (strings or arrays as appropriate)
- Include in metadata if present, omit if not in YAML

---

#### Test: `test_ac5_fail_fast_behavior()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(errorPath);
expect(result.error).toBeDefined();
expect(Array.isArray(result.error)).toBe(false); // Single error, not array
```

**Fixture**: `invalid-yaml-missing-field.md` (missing required id)

**Why it FAILS**:
1. Validation not implemented
2. No fail-fast logic
3. Error object format not defined

**What's needed to PASS**:
- When validation finds an error, STOP immediately
- Return single error object, NOT an array of errors
- Example fail-fast: Check AC#4 error (syntax), if any found → return error
- Don't proceed to AC#5 validation (schema) if YAML syntax is broken

---

### Category 6: Edge Case Tests (2 tests)

#### Test: `test_edge_case_empty_file()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(emptyPath);
expect(result.valid).toBe(false);
expect(result.error).toBeDefined();
```

**Fixture**: `empty-file.md` (0 bytes)

**Why it FAILS**:
1. BrainstormValidator not implemented
2. No empty file detection
3. Error handling missing

**What's needed to PASS**:
- Read file
- Check if file is 0 bytes or contains no YAML frontmatter
- Return error: type = `EMPTY_FILE`, message = "File is empty"

---

#### Test: `test_edge_case_binary_file()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(binaryPath);
expect(result.valid).toBe(false);
expect(result.error.message).toMatch(/binary|encoding|text/i);
```

**Fixture**: `binary-file.bin` (raw binary data)

**Why it FAILS**:
1. BrainstormValidator doesn't detect file type
2. No encoding validation
3. No binary file handling

**What's needed to PASS**:
- Detect if file contains binary data (non-UTF8)
- Return error: type = `BINARY_FILE`, message = "File appears to be binary, not text"
- Could use: Check for null bytes, invalid UTF-8 sequences, or file command

---

### Category 7: Business Rules Tests (3 tests)

#### Test: `test_br001_validation_before_interaction()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(invalidPath);
expect(result).toBeDefined();
expect(result.userPromptShown).toBeUndefined(); // No prompts yet
```

**Why it FAILS**:
1. BrainstormValidator not implemented
2. No validation occurs
3. Can't verify timing requirement

**What's needed to PASS**:
- Implement synchronous validation (no async/await)
- Complete validation BEFORE returning
- Don't show any prompts until validation complete
- Return result object immediately (no AskUserQuestion in validator itself)

---

#### Test: `test_br002_graceful_error_handling()`

**What it tests**:
```javascript
const invalidPaths = [/* multiple invalid files */];
invalidPaths.forEach(path => {
  expect(() => {
    const result = BrainstormValidator.validate(path);
    expect(result.error).toBeDefined();
  }).not.toThrow(); // Must NOT throw
});
```

**Why it FAILS**:
1. Current BrainstormValidator throws errors
2. No try/catch handling
3. No graceful error objects

**What's needed to PASS**:
- Wrap all YAML parsing in try/catch
- Never throw - always return error object
- Return: `{ valid: false, error: { message, type, lineNumber } }`
- Validator should be "fail-safe" - never crashes

---

#### Test: `test_br003_actionable_error_messages()`

**What it tests**:
```javascript
const result = BrainstormValidator.validate(badDatePath);
expect(result.error.message).toMatch(/YYYY-MM-DD|format/i);
expect(result.error.message).not.toMatch(/null|undefined|error code/);
```

**Why it FAILS**:
1. Error messages not generated
2. Messages not actionable
3. User doesn't know how to fix

**What's needed to PASS**:
- Error messages must tell user how to fix the problem
- Include expected format/values
- Example: "Invalid date format for 'created' field - expected YYYY-MM-DD"
- NOT: "Error code 402" or "null reference error"

---

## Summary: What's Needed to Make All Tests PASS

### Core Implementation Required

1. **`BrainstormValidator` class** in brainstorm-handoff-workflow.md
   - Methods: `validate()`, `validateYAML()`, `validateSchema()`
   - Must parse YAML frontmatter
   - Must detect all 5 error types from AC#4
   - Must validate all schema requirements from AC#5
   - Must never throw - always return structured result object
   - Must complete in <100ms

2. **`YAMLErrorMapper` class** in error-handling.md
   - Methods: `mapError()`, `formatErrorMessage()`
   - Must create user-friendly error messages
   - Must follow format specification from AC#2
   - Must include file path and line numbers

3. **YAML Parsing Library**
   - Recommended: `js-yaml` npm package
   - Or: Hand-written YAML parser using regex
   - Must support YAML 1.2 syntax

4. **Skill Integration**
   - Call BrainstormValidator in ideation skill Phase 1 Step 0
   - Display errors using YAMLErrorMapper
   - Implement fallback flow per AC#3

### Test Files Verify Implementation Against

All tests reference these fixtures - implementation must handle them correctly:

| File | Error Type | Implementation must detect |
|------|-----------|---------------------------|
| valid-brainstorm.md | None | Pass validation, return metadata |
| invalid-yaml-missing-delimiter.md | Missing `---` | Detect delimiter count |
| invalid-yaml-mixed-indentation.md | Tabs in YAML | Detect non-space indentation |
| invalid-yaml-duplicate-key.md | Duplicate keys | Detect when key appears twice |
| invalid-yaml-bad-date.md | Bad date value | Validate YYYY-MM-DD format |
| invalid-yaml-missing-field.md | Missing field | Check for required fields |
| empty-file.md | Empty file | Detect zero bytes or no YAML |
| binary-file.bin | Binary content | Detect non-UTF8 data |

**When all fixtures pass their respective tests, all 40+ tests will PASS.**

---

## TDD Workflow Verification

**Red Phase (Current)**: All 40+ tests FAIL ✓
**Green Phase (Next)**: Implement validator → all tests PASS
**Refactor Phase (After)**: Improve code while tests stay GREEN

This test generation completes the Red phase. Next step: Implementation.
