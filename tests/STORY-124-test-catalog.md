# STORY-124 Test Function Catalog

**Test File:** `/mnt/c/Projects/DevForgeAI2/tests/test_story_124_wsl_documentation.py`
**Total Functions:** 37 (34 failing, 3 passing)
**Framework:** Python pytest
**Status:** RED PHASE (TDD Test-First)

---

## Test Functions by Category

### 1. SECTION EXISTENCE TESTS (TestWSLSectionExists) - 6 Tests

| # | Test Function | AC# | Expected Result | Checks |
|---|---------------|-----|-----------------|--------|
| 1 | `test_should_have_wsl_test_execution_section_header` | AC#1 | FAIL | `"## WSL Test Execution"` header |
| 2 | `test_should_have_path_handling_subsection` | AC#1 | FAIL | `"### Path Handling"` subsection |
| 3 | `test_should_have_environment_setup_subsection` | AC#5 | FAIL | `"### Environment Setup"` subsection |
| 4 | `test_should_have_common_issues_subsection` | AC#2 | FAIL | `"### Common Issues"` subsection |
| 5 | `test_should_have_test_commands_subsection` | AC#3 | FAIL | `"### Test Commands"` subsection |
| 6 | `test_should_have_shell_script_subsection` | AC#4 | FAIL | `"### Shell Script"` subsection |

**Failure Message Example:**
```
AssertionError: Missing '## WSL Test Execution' section header in coding-standards.md
```

---

### 2. MARKDOWN TABLE SYNTAX TESTS (TestMarkdownTableSyntax) - 6 Tests

| # | Test Function | AC# | Validates | Expected Result |
|---|---------------|-----|-----------|-----------------|
| 7 | `test_should_have_properly_formatted_issues_table` | AC#2 | Table separator `\|---\|---\|---\|` | FAIL |
| 8 | `test_should_have_module_not_found_issue_row` | AC#2 | "Module not found" + "PYTHONPATH" | FAIL |
| 9 | `test_should_have_permission_denied_issue_row` | AC#2 | "Permission denied" row | FAIL |
| 10 | `test_should_have_line_ending_errors_issue_row` | AC#2 | Line ending errors (CRLF/`\r`) | FAIL |
| 11 | `test_should_have_slow_file_operations_issue_row` | AC#2 | "Slow file operations" row | FAIL |
| 12 | `test_should_have_pytest_not_found_issue_row` | AC#2 | "pytest not found" + virtual env | FAIL |

**What They Check:**
- Markdown table syntax (pipes and separators)
- All 5 required issues present
- Each issue row has cause and fix columns

---

### 3. CODE BLOCK SYNTAX TESTS (TestCodeBlockSyntax) - 2 Tests

| # | Test Function | AC# | Validates | Expected Result |
|---|---------------|-----|-----------|-----------------|
| 13 | `test_should_have_bash_code_block_with_test_commands` | AC#3 | Bash code block marker ` ```bash ` | FAIL |
| 14 | `test_should_have_environment_setup_code_block` | AC#5 | `export PYTHONPATH` in code block | FAIL |

**What They Check:**
- Code blocks use proper markdown syntax
- Bash commands properly enclosed

---

### 4. PATH ACCURACY TESTS (TestPathAccuracy) - 2 Tests

| # | Test Function | AC# | Validates | Expected Result |
|---|---------------|-----|-----------|-----------------|
| 15 | `test_should_use_mnt_c_paths_not_windows_paths` | AC#1 | `/mnt/c/` present, `C:\\` not recommended | FAIL |
| 16 | `test_should_have_devforgeai2_example_path` | AC#1 | `/mnt/c/Projects/DevForgeAI2` example | FAIL |

**What They Check:**
- WSL paths use Unix format (`/mnt/c/`)
- Example paths are accurate
- Windows paths not recommended for WSL

---

### 5. AC#1 PATH HANDLING INTEGRATION TESTS (TestAC1PathHandling) - 2 Tests

| # | Test Function | Purpose | Expected Result |
|---|---------------|---------|-----------------|
| 17 | `test_should_explain_path_conversion_mnt_c` | Path conversion documented | FAIL |
| 18 | `test_should_mention_python_path_discovery` | pytest uses Unix paths mentioned | FAIL |

**Requirement AC#1:**
> "Use `/mnt/c/` paths in WSL, not `C:\`" with example `/mnt/c/Projects/DevForgeAI2/tests/`

---

### 6. AC#2 COMMON ISSUES INTEGRATION TEST (TestAC2CommonIssues) - 1 Test

| # | Test Function | Required Issues | Expected Result |
|---|---------------|-----------------|-----------------|
| 19 | `test_should_have_all_five_issues_documented` | All 5 documented | FAIL |

**Five Issues Required:**
1. Module not found → PYTHONPATH
2. Permission denied → Windows file locks
3. Line ending errors → CRLF
4. Slow file operations → Filesystem overhead
5. pytest not found → Virtual env not activated

**Requirement AC#2:**
> Table with Issue | Cause | Fix columns covering specific WSL test issues

---

### 7. AC#3 TEST COMMAND INTEGRATION TESTS (TestAC3TestCommands) - 4 Tests

| # | Test Function | Command | Expected Result |
|---|---------------|---------|-----------------|
| 20 | `test_should_have_pytest_run_all_tests_example` | `pytest tests/ -v` | FAIL |
| 21 | `test_should_have_pytest_run_single_file_example` | `pytest tests/test_validators.py -v` | FAIL |
| 22 | `test_should_have_pytest_with_coverage_example` | `pytest tests/ --cov=src --cov-report=term-missing` | FAIL |
| 23 | `test_should_have_pytest_single_test_example` | `pytest tests/file.py::test_name -v` | FAIL |

**Requirement AC#3:**
> Examples for: (1) all tests, (2) single file, (3) with coverage, (4) single test

---

### 8. AC#4 SHELL SCRIPT EXECUTION TEST (TestAC4ShellScriptExecution) - 1 Test

| # | Test Function | Requirement | Expected Result |
|---|---------------|-------------|-----------------|
| 24 | `test_should_document_bash_not_direct_execution` | bash script.sh (not ./script.sh) | FAIL |

**Requirement AC#4:**
> "Always run shell scripts with `bash script.sh`, not `./script.sh`" (explain WSL mount issues)

---

### 9. AC#5 ENVIRONMENT SETUP INTEGRATION TESTS (TestAC5EnvironmentSetup) - 2 Tests

| # | Test Function | Command | Expected Result |
|---|---------------|---------|-----------------|
| 25 | `test_should_document_pythonpath_export` | `export PYTHONPATH=".:$PYTHONPATH"` | FAIL |
| 26 | `test_should_document_cd_to_project_root` | `cd /mnt/c/Projects/DevForgeAI2` | FAIL |

**Requirement AC#5:**
> Commands with exports shown:
> ```bash
> cd /mnt/c/Projects/DevForgeAI2
> export PYTHONPATH=".:$PYTHONPATH"
> ```

---

### 10. BASH COMMAND SYNTAX VALIDATION TESTS (TestBashCommandSyntaxValidity) - 3 Tests

| # | Test Function | Validates | Expected Result |
|---|---------------|-----------|-----------------|
| 27 | `test_export_pythonpath_command_syntax_valid` | Regex validation of export syntax | FAIL |
| 28 | `test_cd_command_syntax_valid` | cd command format | FAIL |
| 29 | `test_all_pytest_commands_have_valid_syntax` | pytest command patterns (3+ found) | FAIL |

**What They Check:**
- Bash syntax validation using regex patterns
- Command structure is valid

---

### 11. SECTION HIERARCHY TESTS (TestSectionHierarchy) - 3 Tests

| # | Test Function | Requirement | Expected Result |
|---|---------------|-------------|-----------------|
| 30 | `test_wsl_section_uses_h2_header` | Main section uses `##` (H2) | FAIL |
| 31 | `test_subsections_use_h3_headers` | Subsections use `###` (H3) - 5+ found | FAIL |
| 32 | `test_no_h1_headers_in_wsl_section` | No `#` (H1) headers in section | FAIL |

**Proper Hierarchy:**
```
## WSL Test Execution          (H2 - main section)
### Path Handling              (H3 - subsection)
### Environment Setup          (H3 - subsection)
### Common Issues and Fixes    (H3 - subsection)
### Test Commands              (H3 - subsection)
### Shell Script Testing       (H3 - subsection)
```

---

### 12. DOCUMENTATION CLARITY TESTS (TestDocumentationClarity) - 2 Tests

| # | Test Function | Requirement | Expected Result |
|---|---------------|-------------|-----------------|
| 33 | `test_examples_marked_as_correct_or_incorrect` | Shows correct vs incorrect patterns | FAIL |
| 34 | `test_section_explains_why_bash_vs_direct_execution` | Explains WSL mount/permission issues | FAIL |

**What They Check:**
- Examples distinguish good/bad approaches
- Reasoning provided for recommendations

---

### 13. EDGE CASE TESTS (TestEdgeCases) - 3 Tests

| # | Test Function | Purpose | Expected Result |
|---|---------------|---------|-----------------|
| 35 | `test_coding_standards_file_is_readable` | File exists and readable | PASS ✓ |
| 36 | `test_wsl_section_not_empty_and_substantial` | Section >100 chars (if exists) | PASS ✓ |
| 37 | `test_no_broken_markdown_links_in_wsl_section` | No incomplete `[text]` links | PASS ✓ |

**Why These Pass:**
- File existence check (file exists regardless of section)
- Edge case handling (section doesn't exist yet, so checks are skipped)
- Link validation (no links exist yet, so check passes)

---

## Test Execution Summary

### Command to Run Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/test_story_124_wsl_documentation.py -v
```

### Current Status (RED PHASE)
```
FAILED: 34
PASSED:  3
TOTAL:  37
```

### After Implementation (GREEN PHASE - Target)
```
FAILED:  0
PASSED: 37
TOTAL:  37
```

---

## Test Organization Map

```
test_story_124_wsl_documentation.py
├── FIXTURES (3)
│   ├── coding_standards_path
│   ├── coding_standards_content
│   └── wsl_section
│
├── TestWSLSectionExists (6 tests)
│   └── Validates section and subsection headers
│
├── TestMarkdownTableSyntax (6 tests)
│   └── Validates table structure and all 5 issue rows
│
├── TestCodeBlockSyntax (2 tests)
│   └── Validates bash code block markers
│
├── TestPathAccuracy (2 tests)
│   └── Validates /mnt/c/ path references
│
├── TestAC1PathHandling (2 tests)
│   └── AC#1 integration validation
│
├── TestAC2CommonIssues (1 test)
│   └── AC#2 integration - all 5 issues
│
├── TestAC3TestCommands (4 tests)
│   └── AC#3 integration - 4 command examples
│
├── TestAC4ShellScriptExecution (1 test)
│   └── AC#4 integration validation
│
├── TestAC5EnvironmentSetup (2 tests)
│   └── AC#5 integration validation
│
├── TestBashCommandSyntaxValidity (3 tests)
│   └── Bash syntax regex validation
│
├── TestSectionHierarchy (3 tests)
│   └── Markdown H1/H2/H3 validation
│
├── TestDocumentationClarity (2 tests)
│   └── Correct/incorrect examples validation
│
└── TestEdgeCases (3 tests)
    └── File existence and edge conditions
```

---

## Quick Reference: Test Names by AC

### AC#1 Coverage
- `test_should_use_mnt_c_paths_not_windows_paths`
- `test_should_have_devforgeai2_example_path`
- `test_should_explain_path_conversion_mnt_c`
- `test_should_mention_python_path_discovery`

### AC#2 Coverage
- `test_should_have_properly_formatted_issues_table`
- `test_should_have_module_not_found_issue_row`
- `test_should_have_permission_denied_issue_row`
- `test_should_have_line_ending_errors_issue_row`
- `test_should_have_slow_file_operations_issue_row`
- `test_should_have_pytest_not_found_issue_row`
- `test_should_have_all_five_issues_documented`

### AC#3 Coverage
- `test_should_have_pytest_run_all_tests_example`
- `test_should_have_pytest_run_single_file_example`
- `test_should_have_pytest_with_coverage_example`
- `test_should_have_pytest_single_test_example`

### AC#4 Coverage
- `test_should_document_bash_not_direct_execution`

### AC#5 Coverage
- `test_should_document_pythonpath_export`
- `test_should_document_cd_to_project_root`
- `test_export_pythonpath_command_syntax_valid`
- `test_cd_command_syntax_valid`
- `test_should_have_environment_setup_code_block`

---

## Implementation Checklist

Use this checklist while implementing the WSL section in coding-standards.md:

### Section Structure
- [ ] Add `## WSL Test Execution` header (H2)
- [ ] Add `### Path Handling` subsection (H3)
- [ ] Add `### Environment Setup` subsection (H3)
- [ ] Add `### Common Issues and Fixes` subsection (H3)
- [ ] Add `### Test Commands` subsection (H3)
- [ ] Add `### Shell Script Testing` subsection (H3)

### Content Requirements
- [ ] Path Handling: Explain /mnt/c/ vs C:\\ conversion
- [ ] Path Handling: Include example `/mnt/c/Projects/DevForgeAI2`
- [ ] Environment Setup: Include `cd /mnt/c/Projects/DevForgeAI2`
- [ ] Environment Setup: Include `export PYTHONPATH=".:$PYTHONPATH"`
- [ ] Common Issues Table: Format as markdown table
- [ ] Common Issues Table: Include all 5 issue/cause/fix rows
- [ ] Test Commands: Include ` ```bash ` code block
- [ ] Test Commands: Include `pytest tests/ -v`
- [ ] Test Commands: Include `pytest tests/test_validators.py -v`
- [ ] Test Commands: Include `pytest tests/ --cov=src --cov-report=term-missing`
- [ ] Test Commands: Include `pytest tests/test_validators.py::test_dod_validation -v`
- [ ] Shell Script: Explain `bash script.sh` (correct)
- [ ] Shell Script: Explain `./script.sh` (incorrect on WSL)
- [ ] Shell Script: Explain WSL mount/permission reasoning

### Quality Checks
- [ ] Run tests: `python3 -m pytest tests/test_story_124_wsl_documentation.py`
- [ ] Result: All 37 tests pass
- [ ] Manual: Copy pytest command from docs, it works
- [ ] Manual: Follow environment setup, Python finds modules
- [ ] Manual: Run shell script with `bash script.sh`, succeeds
- [ ] Review: Non-WSL developer reads and understands

---

## Related Files

- **Test Implementation:** `/mnt/c/Projects/DevForgeAI2/tests/test_story_124_wsl_documentation.py`
- **Test Report:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-124-test-generation-report.md`
- **Target File:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md`
- **Story File:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-124-wsl-test-execution-documentation.story.md`

---

Generated: 2025-12-22 (Test-Automator Skill - TDD Red Phase)
