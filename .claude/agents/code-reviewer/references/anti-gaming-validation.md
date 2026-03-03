# Anti-Gaming Validation for Code Reviewer

**Version**: 1.0 | **Status**: Reference | **Agent**: code-reviewer
**Priority**: BLOCKING - violations halt workflow

---

## Purpose

Detect test gaming patterns that artificially inflate coverage/pass rates. This validation BLOCKS workflow if violations found.

---

## 1. Skip Decorators

Scan all test files for skip/ignore patterns:

```
Grep(pattern="@skip|@pytest\.mark\.skip|@unittest\.skip|@pytest\.mark\.skipif|@Ignore|@Disabled|\[Fact\(Skip|test\.skip|it\.skip|xit\(|xdescribe\(|describe\.skip",
     glob="**/test*/**",
     output_mode="content")
```

**Language-Specific Patterns:**
- **Python:** `@skip`, `@pytest.mark.skip`, `@unittest.skip`, `@pytest.mark.skipif`
- **JavaScript:** `test.skip`, `it.skip`, `describe.skip`, `xit(`, `xdescribe(`
- **C#/.NET:** `[Fact(Skip="...")]`, `[Theory(Skip="...")]`, `[Ignore]`
- **Java:** `@Disabled`, `@Ignore`

## 2. Empty Tests

Scan for tests with no assertions:

**Python:**
```
Grep(pattern="def test_.*:\s*(pass|\.\.\.)\s*$", glob="**/test*.py", output_mode="content", multiline=true)
```

**JavaScript:**
```
Grep(pattern="(test|it)\s*\([^)]+,\s*\(\)\s*=>\s*\{\s*\}\)", glob="**/*.test.{js,ts}", output_mode="content")
```

**C#:**
```
Grep(pattern="\[Fact\].*public\s+void\s+\w+\(\)\s*\{\s*\}", glob="**/*Test*.cs", output_mode="content", multiline=true)
```

## 3. TODO/FIXME Placeholders

```
Grep(pattern="TODO|FIXME|XXX|HACK|NotImplemented|pass\s*#|raise NotImplementedError",
     glob="**/test*/**",
     output_mode="content")
```

## 4. Excessive Mocking

```
FOR each test_file in test_files:
    mock_count = Grep(pattern="mock|Mock|stub|Stub|spy|Spy|MagicMock|patch|jest\.fn|sinon|NSubstitute|Moq",
                     path=test_file, output_mode="count")
    test_count = Grep(pattern="def test_|it\(|test\(|\[Fact\]|\[Test\]|@Test",
                     path=test_file, output_mode="count")

    IF mock_count > (test_count * 2):
        Flag as excessive mocking
```

**Threshold:** Mock count MUST be <= 2x test count

## HALT on Gaming Violations

**If ANY gaming violations detected:**

```markdown
## TEST GAMING DETECTED - WORKFLOW BLOCKED

**ACTION REQUIRED:**
1. Remove ALL skip decorators (or create ADR explaining why skip is necessary)
2. Add real assertions to ALL empty tests
3. Remove ALL TODO/FIXME placeholders - implement actual test logic
4. Reduce mock count to <=2x test count
5. Ensure tests verify real behavior, not just stub returns

**WORKFLOW HALTED:** Fix all test gaming violations before proceeding.
```

## Return Gaming Validation Status

```json
{
  "gaming_validation": {
    "status": "PASS|FAIL",
    "violations": [
      {"type": "SKIP_DECORATOR", "severity": "CRITICAL", "count": 0, "files": []},
      {"type": "EMPTY_TEST", "severity": "CRITICAL", "count": 0, "files": []},
      {"type": "TODO_PLACEHOLDER", "severity": "CRITICAL", "count": 0, "files": []},
      {"type": "EXCESSIVE_MOCKING", "severity": "CRITICAL", "count": 0, "files": []}
    ]
  }
}
```

**Integration:** IF `gaming_validation.status == "FAIL"`: HALT workflow. IF `gaming_validation.status == "PASS"`: Proceed to next phase.
