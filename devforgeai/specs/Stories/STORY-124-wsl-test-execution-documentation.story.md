---
id: STORY-124
title: WSL Test Execution Documentation
epic: EPIC-024
sprint: Sprint-8
status: Backlog
points: 2
depends_on: []
priority: Low
assigned_to: TBD
created: 2025-12-20
format_version: "2.2"
---

# Story: WSL Test Execution Documentation

## Description

**As a** developer on Windows/WSL,
**I want** clear guidance on pytest execution patterns and common WSL issues,
**So that** I can run tests without confusion about path conversion or permission errors.

This story implements EPIC-024 Feature 5: Add WSL testing section to coding standards with path handling, common issues, and test commands.

## Acceptance Criteria

### AC#1: Path Handling Documentation

**Given** a developer new to WSL doesn't know path conversion,
**When** they read coding-standards.md,
**Then** they find: "Use `/mnt/c/` paths in WSL, not `C:\`" with example `/mnt/c/Projects/DevForgeAI2/tests/`.

---

### AC#2: Common Issues Table with Solutions

**Given** developers encounter WSL-specific test failures,
**When** they search for help in coding-standards.md,
**Then** they find a table with Issue | Cause | Fix columns covering:
- "Module not found" → PYTHONPATH not set
- "Permission denied on .sh" → Windows file locks
- "Line ending errors (`$'\r': command not found`)" → CRLF in shell scripts
- "Slow file operations" → Windows filesystem overhead
- "pytest not found" → Virtual env not activated

---

### AC#3: Test Command Examples Documented

**Given** a developer needs to run tests,
**When** they reference coding-standards.md,
**Then** they find examples:
- `pytest tests/ -v` (run all tests)
- `pytest tests/test_validators.py -v` (run single file)
- `pytest tests/ --cov=src --cov-report=term-missing` (with coverage)
- `pytest tests/test_validators.py::test_dod_validation -v` (single test)

---

### AC#4: Shell Script Execution Guidance

**Given** developers execute shell scripts on WSL,
**When** they check coding-standards.md,
**Then** they find: "Always run shell scripts with `bash script.sh`, not `./script.sh`" (explain WSL mount issues).

---

### AC#5: Environment Setup Commands Documented

**Given** a developer setting up WSL environment,
**When** they consult coding-standards.md,
**Then** they find:
```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "WSL Test Execution Section"
      file_path: "devforgeai/specs/context/coding-standards.md"
      insertion_point: "New section ## WSL Test Execution"
      subsections:
        - subsection: "### Path Handling"
          content:
            - "Use `/mnt/c/` paths in WSL, not `C:\`"
            - "pytest discovers tests from Unix-style paths"
            - "Coverage reports use Unix paths"
            - "Example: `/mnt/c/Projects/DevForgeAI2/tests/` not `C:\Projects\DevForgeAI2\tests\`"

        - subsection: "### Environment Setup"
          content:
            - "Command: cd /mnt/c/Projects/DevForgeAI2"
            - "Command: export PYTHONPATH=\".:$PYTHONPATH\""
            - "Explanation: Required for pytest to find modules"

        - subsection: "### Common Issues and Fixes"
          format: "| Issue | Cause | Fix | table"
          rows:
            - issue: "Module not found"
              cause: "PYTHONPATH not set"
              fix: "export PYTHONPATH=\".:$PYTHONPATH\""
            - issue: "Permission denied on .sh"
              cause: "Windows file locks"
              fix: "Close file in other programs, or chmod +x script.sh"
            - issue: "Line ending errors (`$'\r': command not found`)"
              cause: "CRLF in shell scripts"
              fix: "dos2unix script.sh or sed -i 's/\r$//' script.sh"
            - issue: "Slow file operations"
              cause: "Windows filesystem overhead"
              fix: "Run tests from WSL native filesystem if possible"
            - issue: "pytest not found"
              cause: "Virtual env not activated"
              fix: "source venv/bin/activate or pip install pytest"

        - subsection: "### Test Commands"
          format: "Bash code block with examples"
          commands:
            - "pytest tests/ -v              # Run all tests"
            - "pytest tests/test_validators.py -v  # Run specific file"
            - "pytest tests/ --cov=src --cov-report=term-missing  # With coverage"
            - "pytest tests/test_validators.py::test_dod_validation -v  # Single test"

        - subsection: "### Shell Script Testing"
          format: "Best practices with examples"
          practices:
            - "Always run shell scripts with bash, not direct execution"
            - "Example (correct): bash path/to/test.sh"
            - "Example (incorrect): ./path/to/test.sh (may fail on WSL mounts)"
            - "Fix line endings before running: dos2unix path/to/test.sh && bash path/to/test.sh"

  format_constraints:
    - "Use markdown table format for issues"
    - "Code blocks with bash syntax highlighting"
    - "Clear section headers (###)"
    - "Examples with both correct and incorrect patterns"
```

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| Documentation clarity | Clear for WSL beginners | Eliminate confusion for new developers |
| Example accuracy | Tested and verified | Examples must work without modification |
| Coverage | All common WSL issues | Prevent developers from getting stuck |

## Test Strategy

### Unit Tests
- **Test 1:** All markdown syntax is valid (code blocks, tables, headers)
- **Test 2:** All bash commands in examples are syntactically correct
- **Test 3:** All file paths are accurate (e.g., /mnt/c/Projects/DevForgeAI2)

### Integration Tests
- **Test 4:** Developer reads path handling section, understands /mnt/c/ conversion
- **Test 5:** Developer finds solution in common issues table for "Module not found"
- **Test 6:** Developer runs all 4 test command examples successfully
- **Test 7:** Developer runs shell script with `bash script.sh` (not direct execution)

### Verification Tests
- **Test 8:** Manual test: Run pytest on WSL using documented commands
- **Test 9:** Manual test: Execute shell script using documented pattern
- **Test 10:** Manual test: All examples in documentation work without modification

## Definition of Done

### Implementation
- [ ] "## WSL Test Execution" section added to devforgeai/specs/context/coding-standards.md
- [ ] All 5 subsections implemented (Path Handling, Environment Setup, Common Issues, Test Commands, Shell Script Testing)
- [ ] Common Issues table includes all 5 problem/cause/fix rows
- [ ] Test commands include all 4 examples
- [ ] Bash code blocks properly formatted

### Quality
- [ ] All unit tests passing (3 tests)
- [ ] All integration tests passing (4 tests)
- [ ] All verification tests passing (3 tests)
- [ ] Markdown syntax valid (no broken tables or code blocks)
- [ ] All file paths accurate

### Testing
- [ ] Manual test: Paste pytest command from docs, it works
- [ ] Manual test: Follow environment setup, Python finds modules
- [ ] Manual test: Run shell script with `bash script.sh`, succeeds (not direct execution)
- [ ] Manual test: Developer new to WSL can self-serve using docs

### Documentation
- [ ] Section has clear hierarchy (## > ### subsections)
- [ ] Examples marked as "Correct" and "Incorrect" where applicable
- [ ] Inline comments explain "why" (e.g., "WSL mount points may not preserve execute permission")
- [ ] Links to related sections (e.g., ".gitattributes" from STORY-122 for line endings)

### Release
- [ ] All tests passing
- [ ] Documentation clarity verified by non-WSL developer reading it
- [ ] Ready for QA validation
