# Observation Extractor - Examples

### Example 1: Extract from Test-Automator Coverage Gaps

**Context:** test-automator completed Phase 02 (Red), generated tests but coverage report shows gaps.

```
Task(
  subagent_type="observation-extractor",
  description="Extract observations from test-automator Phase 02 output",
  prompt="""
  Extract observations from the following test-automator output.

  Phase: 02
  Story: STORY-234
  Subagent: test-automator

  Context: {
    "coverage_result": {
      "gaps": [
        {"file": "src/auth.py", "coverage": 72, "target": 95},
        {"file": "src/service.py", "coverage": 68, "target": 95}
      ]
    },
    "test_failures": [
      {"test": "test_login_invalid_credentials", "error": "AssertionError: expected True but got False"}
    ]
  }

  Apply extraction rules for test-automator. Return observations array conforming to output schema.
  """
)
```

**Expected output:**
- 3 observations extracted (2 coverage gaps + 1 test failure)
- Coverage gaps categorized as "gap" with severity "medium"
- Test failure categorized as "friction" with severity "high"
- All observation IDs formatted as `obs-02-001`, `obs-02-002`, etc.

### Example 2: Extract from Code-Reviewer High Severity Issues

**Context:** code-reviewer completed Phase 04 (Review), found security and quality issues.

```
Task(
  subagent_type="observation-extractor",
  description="Extract observations from code-reviewer Phase 04 output",
  prompt="""
  Extract observations from the following code-reviewer output.

  Phase: 04
  Story: STORY-456
  Subagent: code-reviewer

  Context: {
    "issues": [
      {"file": "src/api.py", "line": 42, "severity": "high", "message": "SQL injection risk: user input directly in query"},
      {"file": "src/utils.py", "line": 15, "severity": "medium", "message": "Unused import statement"},
      {"file": "src/config.py", "line": 8, "severity": "high", "message": "Hardcoded API key in source code"}
    ]
  }

  Apply extraction rules for code-reviewer. High severity issues -> friction category. Return observations.
  """
)
```

**Expected output:**
- 3 observations extracted (2 high + 1 medium)
- High severity issues categorized as "friction" with severity "high"
- Medium severity issue categorized as "warning" with severity "medium"
- File paths included in "files" array for each observation
