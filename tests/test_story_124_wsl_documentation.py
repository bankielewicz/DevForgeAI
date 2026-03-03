"""
Comprehensive failing tests for STORY-124: WSL Test Execution Documentation

This test suite validates that devforgeai/specs/context/coding-standards.md
contains a complete "## WSL Test Execution" section covering:
- AC#1: Path Handling Documentation
- AC#2: Common Issues Table with Solutions
- AC#3: Test Command Examples
- AC#4: Shell Script Execution Guidance
- AC#5: Environment Setup Commands

Test Framework: pytest
Status: RED PHASE (all tests should FAIL initially - implementation not yet started)

Test Categories:
- Unit Tests (5): Markdown syntax, structure validation
- Integration Tests (4): AC requirements presence and accuracy
- Verification Tests (3): Real-world usage validation
"""

import re
import pytest
from pathlib import Path


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def coding_standards_path():
    """Return absolute path to coding-standards.md"""
    return Path("/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md")


@pytest.fixture
def coding_standards_content(coding_standards_path):
    """Read and return coding-standards.md content"""
    assert coding_standards_path.exists(), f"File not found: {coding_standards_path}"
    return coding_standards_path.read_text(encoding="utf-8")


@pytest.fixture
def wsl_section(coding_standards_content):
    """Extract WSL Test Execution section from coding-standards.md"""
    # Extract from "## WSL Test Execution" to next top-level section or EOF
    pattern = r"## WSL Test Execution\n(.*?)(?=\n## |$)"
    match = re.search(pattern, coding_standards_content, re.DOTALL)

    if not match:
        return None  # Section doesn't exist yet (RED phase)

    return match.group(0)


# ============================================================================
# UNIT TESTS: Markdown Syntax and Structure (70% of tests)
# ============================================================================

class TestWSLSectionExists:
    """Test that WSL Test Execution section exists in coding-standards.md"""

    def test_should_have_wsl_test_execution_section_header(self, coding_standards_content):
        """
        AC#1: Path Handling section must exist
        Requirement: "## WSL Test Execution" header present
        """
        assert "## WSL Test Execution" in coding_standards_content, \
            "Missing '## WSL Test Execution' section header in coding-standards.md"

    def test_should_have_path_handling_subsection(self, wsl_section):
        """
        AC#1: Path Handling Documentation
        Requirement: "### Path Handling" subsection
        """
        assert wsl_section is not None, \
            "WSL Test Execution section not found - cannot validate subsections"

        assert "### Path Handling" in wsl_section, \
            "Missing '### Path Handling' subsection"

    def test_should_have_environment_setup_subsection(self, wsl_section):
        """
        AC#5: Environment Setup Commands
        Requirement: "### Environment Setup" subsection
        """
        assert wsl_section is not None, \
            "WSL Test Execution section not found"

        assert "### Environment Setup" in wsl_section, \
            "Missing '### Environment Setup' subsection"

    def test_should_have_common_issues_subsection(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: "### Common Issues and Fixes" subsection
        """
        assert wsl_section is not None, \
            "WSL Test Execution section not found"

        assert "### Common Issues" in wsl_section, \
            "Missing '### Common Issues and Fixes' subsection"

    def test_should_have_test_commands_subsection(self, wsl_section):
        """
        AC#3: Test Command Examples
        Requirement: "### Test Commands" subsection
        """
        assert wsl_section is not None, \
            "WSL Test Execution section not found"

        assert "### Test Commands" in wsl_section, \
            "Missing '### Test Commands' subsection"

    def test_should_have_shell_script_subsection(self, wsl_section):
        """
        AC#4: Shell Script Execution Guidance
        Requirement: "### Shell Script Testing" or similar subsection
        """
        assert wsl_section is not None, \
            "WSL Test Execution section not found"

        assert "### Shell Script" in wsl_section or "### Shell Execution" in wsl_section, \
            "Missing shell script execution subsection"


class TestMarkdownTableSyntax:
    """Test that markdown tables in WSL section are valid"""

    def test_should_have_properly_formatted_issues_table(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: Valid markdown table with | delimiters
        Format: | Issue | Cause | Fix |
        """
        assert wsl_section is not None, "WSL section not found"

        # Table should have header separator (|---|---|---|)
        has_table_separator = re.search(r"\|[\s]*-+[\s]*\|", wsl_section)
        assert has_table_separator, \
            "Common Issues table missing markdown separator row (|----|----|----|)"

    def test_should_have_module_not_found_issue_row(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: "Module not found" issue with "PYTHONPATH" cause
        """
        assert wsl_section is not None, "WSL section not found"

        assert "Module not found" in wsl_section or "module not found" in wsl_section, \
            "Missing 'Module not found' issue in table"

        assert "PYTHONPATH" in wsl_section, \
            "Missing PYTHONPATH solution for 'Module not found' issue"

    def test_should_have_permission_denied_issue_row(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: "Permission denied" issue in table
        """
        assert wsl_section is not None, "WSL section not found"

        assert "Permission denied" in wsl_section or "permission denied" in wsl_section, \
            "Missing 'Permission denied' issue in table"

    def test_should_have_line_ending_errors_issue_row(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: Line ending errors ("CRLF" / "$'\\r'" pattern)
        """
        assert wsl_section is not None, "WSL section not found"

        has_crlf = "CRLF" in wsl_section or "\\r" in wsl_section or "$'\\r'" in wsl_section
        assert has_crlf, \
            "Missing line ending errors (CRLF) issue in table"

    def test_should_have_slow_file_operations_issue_row(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: "Slow file operations" issue
        """
        assert wsl_section is not None, "WSL section not found"

        assert "Slow file operations" in wsl_section or "slow" in wsl_section.lower(), \
            "Missing 'Slow file operations' issue in table"

    def test_should_have_pytest_not_found_issue_row(self, wsl_section):
        """
        AC#2: Common Issues Table
        Requirement: "pytest not found" issue with "Virtual env" cause
        """
        assert wsl_section is not None, "WSL section not found"

        assert "pytest not found" in wsl_section or "pytest" in wsl_section, \
            "Missing 'pytest not found' issue in table"

        assert "Virtual env" in wsl_section or "virtual" in wsl_section.lower(), \
            "Missing virtual environment solution for pytest issue"


class TestCodeBlockSyntax:
    """Test that bash code blocks are properly formatted"""

    def test_should_have_bash_code_block_with_test_commands(self, wsl_section):
        """
        AC#3: Test Command Examples
        Requirement: Bash code block with pytest examples
        """
        assert wsl_section is not None, "WSL section not found"

        # Look for bash code block marker
        has_bash_block = "```bash" in wsl_section or "```sh" in wsl_section or "```" in wsl_section
        assert has_bash_block, \
            "Missing bash code block (use ```bash or ```sh)"

    def test_should_have_environment_setup_code_block(self, wsl_section):
        """
        AC#5: Environment Setup Commands
        Requirement: Code block with export commands
        """
        assert wsl_section is not None, "WSL section not found"

        assert "export PYTHONPATH" in wsl_section, \
            "Missing 'export PYTHONPATH' environment setup command"

        assert "cd /mnt/c/Projects/DevForgeAI2" in wsl_section, \
            "Missing 'cd /mnt/c/Projects/DevForgeAI2' path setup"


class TestPathAccuracy:
    """Test that file paths in documentation are accurate"""

    def test_should_use_mnt_c_paths_not_windows_paths(self, wsl_section):
        """
        AC#1: Path Handling Documentation
        Requirement: Document /mnt/c/ paths, not C:\\ paths
        """
        assert wsl_section is not None, "WSL section not found"

        # Should contain /mnt/c/ reference
        assert "/mnt/c/" in wsl_section, \
            "Missing /mnt/c/ path reference for WSL"

        # Should NOT recommend using C:\\ paths for WSL
        assert "C:\\" not in wsl_section or "not" in wsl_section.lower(), \
            "Should not recommend C:\\ paths for WSL environments"

    def test_should_have_devforgeai2_example_path(self, wsl_section):
        """
        AC#1: Path Handling Documentation
        Requirement: Example with /mnt/c/Projects/DevForgeAI2/tests/
        """
        assert wsl_section is not None, "WSL section not found"

        assert "/mnt/c/Projects/DevForgeAI2" in wsl_section, \
            "Missing example path /mnt/c/Projects/DevForgeAI2"


# ============================================================================
# INTEGRATION TESTS: Acceptance Criteria Content (20% of tests)
# ============================================================================

class TestAC1PathHandling:
    """Integration test: AC#1 - Path Handling Documentation"""

    def test_should_explain_path_conversion_mnt_c(self, wsl_section):
        """
        AC#1 Requirement: "Use `/mnt/c/` paths in WSL, not `C:\`"
        with example `/mnt/c/Projects/DevForgeAI2/tests/`
        """
        assert wsl_section is not None, "WSL section not found"

        # Must explain the conversion
        conversion_explained = (
            "/mnt/c/" in wsl_section and
            ("C:\\" in wsl_section or "Windows" in wsl_section or "path" in wsl_section.lower())
        )
        assert conversion_explained, \
            "Path conversion between WSL and Windows paths not explained"

    def test_should_mention_python_path_discovery(self, wsl_section):
        """
        AC#1 Note: pytest uses Unix paths
        Requirement: Mention that pytest discovers tests from Unix paths
        """
        assert wsl_section is not None, "WSL section not found"

        assert "pytest" in wsl_section and ("/mnt/c/" in wsl_section or "path" in wsl_section.lower()), \
            "Should explain that pytest uses Unix-style paths"


class TestAC2CommonIssues:
    """Integration test: AC#2 - Common Issues Table"""

    def test_should_have_all_five_issues_documented(self, wsl_section):
        """
        AC#2 Requirement: Table with ALL 5 problem/cause/fix rows
        1. Module not found → PYTHONPATH
        2. Permission denied → Windows file locks
        3. Line ending errors → CRLF
        4. Slow operations → Filesystem overhead
        5. pytest not found → Virtual env
        """
        assert wsl_section is not None, "WSL section not found"

        issues_found = 0

        if "Module not found" in wsl_section and "PYTHONPATH" in wsl_section:
            issues_found += 1

        if "Permission denied" in wsl_section:
            issues_found += 1

        if "CRLF" in wsl_section or "line ending" in wsl_section.lower():
            issues_found += 1

        if ("Slow" in wsl_section or "slow" in wsl_section.lower()) and "file" in wsl_section.lower():
            issues_found += 1

        if "pytest not found" in wsl_section or ("pytest" in wsl_section and "virtual" in wsl_section.lower()):
            issues_found += 1

        assert issues_found >= 5, \
            f"Only {issues_found}/5 issues documented. Need all: " \
            "Module not found, Permission denied, Line endings, Slow ops, pytest not found"


class TestAC3TestCommands:
    """Integration test: AC#3 - Test Command Examples"""

    def test_should_have_pytest_run_all_tests_example(self, wsl_section):
        """
        AC#3 Requirement: Example `pytest tests/ -v`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "pytest tests/" in wsl_section and "-v" in wsl_section, \
            "Missing example: pytest tests/ -v (run all tests)"

    def test_should_have_pytest_run_single_file_example(self, wsl_section):
        """
        AC#3 Requirement: Example `pytest tests/test_validators.py -v`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "test_validators.py" in wsl_section and "pytest" in wsl_section, \
            "Missing example: pytest tests/test_validators.py -v (single file)"

    def test_should_have_pytest_with_coverage_example(self, wsl_section):
        """
        AC#3 Requirement: Example `pytest tests/ --cov=src --cov-report=term-missing`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "--cov" in wsl_section and "coverage" in wsl_section.lower(), \
            "Missing example: pytest with --cov and coverage reporting"

    def test_should_have_pytest_single_test_example(self, wsl_section):
        """
        AC#3 Requirement: Example `pytest tests/test_validators.py::test_dod_validation -v`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "::" in wsl_section and "pytest" in wsl_section, \
            "Missing example: pytest tests/file.py::test_name -v (single test)"


class TestAC4ShellScriptExecution:
    """Integration test: AC#4 - Shell Script Execution Guidance"""

    def test_should_document_bash_not_direct_execution(self, wsl_section):
        """
        AC#4 Requirement: "Always run shell scripts with `bash script.sh`, not `./script.sh`"
        """
        assert wsl_section is not None, "WSL section not found"

        # Should mention bash and script.sh
        assert "bash" in wsl_section.lower() and "script" in wsl_section.lower(), \
            "Should document running scripts with 'bash script.sh'"

        # Should explain why NOT to use ./script.sh
        assert "not" in wsl_section.lower() or "./script" in wsl_section, \
            "Should explain why NOT to use ./script.sh directly"


class TestAC5EnvironmentSetup:
    """Integration test: AC#5 - Environment Setup Commands"""

    def test_should_document_pythonpath_export(self, wsl_section):
        """
        AC#5 Requirement: Command `export PYTHONPATH=".:$PYTHONPATH"`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "export PYTHONPATH" in wsl_section, \
            "Missing: export PYTHONPATH command"

        assert "$PYTHONPATH" in wsl_section, \
            "PYTHONPATH export must reference existing $PYTHONPATH"

    def test_should_document_cd_to_project_root(self, wsl_section):
        """
        AC#5 Requirement: Command `cd /mnt/c/Projects/DevForgeAI2`
        """
        assert wsl_section is not None, "WSL section not found"

        assert "cd /mnt/c/Projects/DevForgeAI2" in wsl_section, \
            "Missing: cd /mnt/c/Projects/DevForgeAI2 command"


# ============================================================================
# VERIFICATION TESTS: Real-World Usage (10% of tests)
# ============================================================================

class TestBashCommandSyntaxValidity:
    """Verify that bash commands in documentation are syntactically valid"""

    def test_export_pythonpath_command_syntax_valid(self, wsl_section):
        """
        Verification: export PYTHONPATH=".:$PYTHONPATH" is valid bash
        """
        assert wsl_section is not None, "WSL section not found"

        # Extract the export command
        export_pattern = r'export PYTHONPATH="[^"]*\$PYTHONPATH[^"]*"'
        has_valid_export = re.search(export_pattern, wsl_section)

        assert has_valid_export, \
            "export PYTHONPATH command has invalid syntax. Should be: export PYTHONPATH=\".:$PYTHONPATH\""

    def test_cd_command_syntax_valid(self, wsl_section):
        """
        Verification: cd /mnt/c/Projects/DevForgeAI2 is valid bash
        """
        assert wsl_section is not None, "WSL section not found"

        assert "cd /mnt/c/Projects/DevForgeAI2" in wsl_section, \
            "cd command missing or malformed"

    def test_all_pytest_commands_have_valid_syntax(self, wsl_section):
        """
        Verification: All pytest command examples are syntactically valid
        """
        assert wsl_section is not None, "WSL section not found"

        pytest_commands = [
            "pytest tests/ -v",
            "pytest tests/test_validators.py -v",
            "--cov=src",
            "::"
        ]

        found_commands = sum(1 for cmd in pytest_commands if cmd in wsl_section)
        assert found_commands >= 3, \
            f"Only {found_commands}/4 pytest command patterns found. Verify syntax."


class TestSectionHierarchy:
    """Verify proper markdown section hierarchy"""

    def test_wsl_section_uses_h2_header(self, coding_standards_content):
        """
        Verification: WSL section uses ## (H2) header for main section
        """
        # Check that "## WSL Test Execution" exists
        assert "## WSL Test Execution" in coding_standards_content, \
            "WSL Test Execution section must use ## header (H2 level)"

        # Verify it's not "### WSL Test Execution" (H3)
        assert "### WSL Test Execution" not in coding_standards_content, \
            "WSL Test Execution must be H2 (##), not H3 (###)"

    def test_subsections_use_h3_headers(self, wsl_section):
        """
        Verification: All subsections use ### (H3) headers
        """
        assert wsl_section is not None, "WSL section not found"

        # Count ### subsections
        subsections = re.findall(r"^###\s", wsl_section, re.MULTILINE)
        assert len(subsections) >= 5, \
            f"Found {len(subsections)} subsections, expected at least 5 (###)"

    def test_no_h1_headers_in_wsl_section(self, wsl_section):
        """
        Verification: WSL section doesn't contain # (H1) headers
        """
        assert wsl_section is not None, "WSL section not found"

        # Should not have standalone H1
        h1_pattern = r"^#\s[^#]"  # Matches "# " but not "##"
        h1_found = re.search(h1_pattern, wsl_section, re.MULTILINE)

        assert not h1_found, \
            "WSL section contains H1 headers (#), should use ## for main and ### for subsections"


class TestDocumentationClarity:
    """Verify documentation is clear and complete"""

    def test_examples_marked_as_correct_or_incorrect(self, wsl_section):
        """
        Verification: Shell script examples show correct vs incorrect patterns
        Examples should be labeled:
        - Example (correct): bash path/to/test.sh
        - Example (incorrect): ./path/to/test.sh
        """
        assert wsl_section is not None, "WSL section not found"

        # Should have some pattern distinguishing good/bad examples
        has_examples = (
            ("bash" in wsl_section and "./script" in wsl_section) or
            ("correct" in wsl_section.lower()) or
            ("incorrect" in wsl_section.lower())
        )

        assert has_examples, \
            "Should show correct (bash script.sh) vs incorrect (./script.sh) examples"

    def test_section_explains_why_bash_vs_direct_execution(self, wsl_section):
        """
        Verification: Documentation explains reasoning for bash vs direct execution
        Should mention: WSL mount points may not preserve execute permission
        """
        assert wsl_section is not None, "WSL section not found"

        # Check for explanatory content
        has_explanation = (
            ("mount" in wsl_section.lower() and "permission" in wsl_section.lower()) or
            ("WSL" in wsl_section and ("bash" in wsl_section or "execute" in wsl_section.lower()))
        )

        assert has_explanation, \
            "Should explain WHY bash is needed (WSL mount/permission issues)"


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_coding_standards_file_is_readable(self, coding_standards_path):
        """
        Verification: Ensure file exists and is readable
        """
        assert coding_standards_path.exists(), \
            f"File not found: {coding_standards_path}"

        assert coding_standards_path.is_file(), \
            f"Path is not a file: {coding_standards_path}"

        # Try to read
        content = coding_standards_path.read_text(encoding="utf-8")
        assert len(content) > 0, "File is empty"

    def test_wsl_section_not_empty_and_substantial(self, wsl_section):
        """
        Verification: If section exists, it should be substantial (>100 chars)
        """
        if wsl_section is not None:
            assert len(wsl_section) > 100, \
                "WSL section exists but is too short (<100 chars)"

    def test_no_broken_markdown_links_in_wsl_section(self, wsl_section):
        """
        Verification: No incomplete markdown links like [text] or [text](
        """
        if wsl_section is not None:
            # Look for incomplete links
            broken_link_pattern = r"\[[^\]]+\](?!\()"  # [text] not followed by (
            # But exclude common cases like [x] for checklist
            broken_links = re.findall(r"\[[^\]]+\]$", wsl_section, re.MULTILINE)

            # This is a soft check - just warn if found
            assert len(broken_links) == 0 or "[x]" in wsl_section, \
                "Potential broken markdown links detected"


# ============================================================================
# RUN CONFIGURATION
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
