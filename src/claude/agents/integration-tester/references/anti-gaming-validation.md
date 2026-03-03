# Anti-Gaming Validation (Step 0)

**Purpose:** Prevent coverage gaming BEFORE test execution.

**CRITICAL:** This step MUST complete BEFORE running any tests. Coverage metrics are meaningless if tests are gamed.

**Why This Runs First:**
- Skipped tests don't run but aren't counted as failures
- Empty tests pass automatically, inflating pass rate
- Over-mocked tests don't test real behavior
- By validating BEFORE test execution, we ensure coverage scores are authentic

---

## 0.1 Scan for Skip Decorators

```
skip_matches = Grep(pattern="@skip|@pytest\.mark\.skip|@unittest\.skip|@pytest\.mark\.skipif|@Ignore|@Disabled|\[Fact\(Skip|test\.skip|it\.skip|xit\(|xdescribe\(|describe\.skip",
                   glob="**/test*/**",
                   output_mode="files_with_matches")
```

## 0.2 Scan for Empty Tests

```
# Python
empty_python = Grep(pattern="def test_.*:\s*(pass|\.\.\.)", glob="**/test*.py", output_mode="files_with_matches", multiline=true)

# JavaScript
empty_js = Grep(pattern="(test|it)\s*\([^)]+,\s*\(\)\s*=>\s*\{\s*\}\)", glob="**/*.test.{js,ts}", output_mode="files_with_matches")

# C#
empty_csharp = Grep(pattern="\[Fact\].*\{\s*\}", glob="**/*Test*.cs", output_mode="files_with_matches", multiline=true)
```

## 0.3 Scan for TODO/FIXME Placeholders

```
todo_matches = Grep(pattern="TODO|FIXME|XXX|HACK|NotImplemented|pass\s*#|raise NotImplementedError",
                   glob="**/test*/**",
                   output_mode="files_with_matches")
```

**Placeholder Patterns:**
- `TODO:` - Work not completed
- `FIXME:` - Known broken code
- `NotImplementedError` - Stub exception

## 0.4 Calculate Mock Ratio

```
FOR each test_file in test_files:
    mock_count = Grep(pattern="mock|Mock|stub|Stub|spy|Spy|MagicMock|patch|jest\.fn|sinon|NSubstitute|Moq",
                     path=test_file, output_mode="count")
    test_count = Grep(pattern="def test_|it\(|test\(|\[Fact\]|\[Test\]|@Test",
                     path=test_file, output_mode="count")

    IF mock_count > test_count * 2:
        excessive_mocking_files.append(test_file)
```

## 0.5 HALT if Violations Found

IF skip_matches OR empty_tests OR todo_matches OR excessive_mocking_files:

```markdown
==============================================================
TEST GAMING DETECTED - CANNOT PROCEED TO COVERAGE ANALYSIS
==============================================================

Phase 4 Integration Testing BLOCKED due to test gaming:

Skip Decorators: {len(skip_matches)} files
  - {list files}

Empty Tests: {len(empty_tests)} files
  - {list files}

TODO/FIXME Placeholders: {len(todo_matches)} files
  - {list files}

Excessive Mocking: {len(excessive_mocking_files)} files
  - {file}: {mock_count} mocks for {test_count} tests (max: {test_count * 2})

ACTION REQUIRED:
1. Remove all @skip/@Ignore decorators (or create ADR explaining why skip is necessary)
2. Add real assertions to empty tests
3. Remove ALL TODO/FIXME placeholders - implement the actual test logic
4. Reduce mock usage to <=2x test count

Cannot calculate authentic coverage with gaming patterns present.
==============================================================
```

RETURN:
```json
{
  "status": "BLOCKED",
  "reason": "TEST_GAMING_DETECTED",
  "violations": {
    "skip_decorators": [...],
    "empty_tests": [...],
    "todo_placeholders": [...],
    "excessive_mocking": [...]
  }
}
```

## 0.6 Proceed Only on PASS

IF no violations:
```
Display: "Anti-gaming validation passed - coverage will be authentic"
PROCEED to Step 1 (Analyze Integration Points)
```
