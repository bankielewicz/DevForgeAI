# Validation Workflow

**Purpose:** Define the post-generation validation steps to ensure the generated CLI and skill are correct, aligned, and functional.

---

## Validation Phases

### 1. CLI Entry Point Validation

**Goal:** Verify the CLI script loads and responds to `--help`.

```
EXECUTE: Bash("python ${OUTPUT_DIR}/cli.py --help 2>&1")
EXPECTED: Exit code 0, output contains subcommand help text
FAILURE: Import error, syntax error, missing dependencies
```

**Common Issues:**
- Missing `__init__.py` in adapters/ or utils/
- Import path issues (relative vs absolute)
- Missing dependencies in requirements.txt

**Recovery:**
- Fix import paths
- Add missing `__init__.py` files
- Add missing packages to requirements.txt
- Retry once; if still failing, HALT

---

### 2. Pattern-Specific Smoke Test

**Goal:** Verify pattern-specific functionality works.

#### API Wrapper Smoke Test

```
EXECUTE: Test one command with mock/sample data
VERIFY: Command executes without import errors
NOTE: Actual tool call may fail (NotImplementedError) — that's expected for stubs
```

#### State-Based Smoke Test

```
EXECUTE: Full session lifecycle test
  1. python cli.py session create --name "test"
     → Must return session_id
  2. python cli.py session list
     → Must show the created session
  3. python cli.py session destroy --session <id>
     → Must succeed

VERIFY: All three operations complete without errors
```

#### Custom Pattern Smoke Test

```
EXECUTE: python cli.py --help
VERIFY: Custom commands appear in help text
```

---

### 3. Skill-to-CLI Interface Alignment

**Goal:** Every command documented in the generated skill exists as a CLI subparser.

```
EXTRACT from SKILL.md:
  - All command names mentioned in "Available Commands" section
  - All commands in code blocks

EXTRACT from cli.py:
  - All subparser names registered via add_parser()

COMPARE:
  - Every skill command must exist in CLI
  - Missing commands = FAIL (alignment broken)
  - Extra CLI commands not in skill = WARNING (undocumented)
```

**Alignment Score:**
- 100%: All skill commands exist in CLI
- 80-99%: Most commands aligned, minor gaps
- <80%: Significant misalignment, investigate

---

### 4. Integration Validation

**Goal:** Comprehensive cross-validation of CLI + skill using integration-tester subagent.

**Checks:**
1. Command names match (skill ↔ CLI)
2. Parameter names match (skill docs ↔ argparse definitions)
3. Output format documentation matches actual CLI output format
4. Error codes in skill match CLI error handling
5. Session lifecycle documented correctly (state-based only)

---

### 5. Test Suite Execution

**Goal:** Run generated test stubs to verify basic functionality.

```
EXECUTE: Bash("pytest ${OUTPUT_DIR}/tests/ -v 2>&1")
EXPECTED: Exit code 0, or expected NotImplementedError for stub tests
```

**Acceptable Failures:**
- `NotImplementedError` from stub adapter methods (expected)
- Import warnings (non-critical)

**Unacceptable Failures:**
- Syntax errors in generated code
- Import errors (missing modules)
- Test infrastructure failures

---

## Validation Report Schema

```json
{
  "convert_id": "CONVERT-YYYYMMDD-HHMMSS",
  "validation_timestamp": "ISO 8601",
  "cli_help_ok": true,
  "smoke_test_passed": true,
  "interface_aligned": true,
  "alignment_score": 100,
  "integration_validation": "PASS",
  "tests_executed": true,
  "test_results": {
    "passed": 2,
    "failed": 0,
    "errors": 0,
    "skipped": 1
  },
  "overall_status": "PASS",
  "issues": []
}
```

### Overall Status Determination

- **PASS**: All validations pass
- **PARTIAL**: Minor issues (warnings, undocumented commands)
- **FAIL**: Critical issues (CLI won't load, interface misaligned, tests error out)

---

## Retry Policy

| Validation | Max Retries | On Failure |
|-----------|-------------|------------|
| CLI help | 1 (fix + retry) | HALT |
| Smoke test | 0 | Record as warning |
| Interface alignment | 0 | HALT if < 80% |
| Test suite | 0 | Record results |
