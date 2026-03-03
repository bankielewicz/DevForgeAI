"""
Tests for STORY-500: Add C++ Coverage Support to QA Workflow via OpenCppCoverage

TDD Red Phase - All tests MUST FAIL before implementation.
Tests validate against src/claude/skills/devforgeai-qa/ tree.
"""
import os
import re
import pytest

# Base path for all target files
BASE = "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-qa"

COVERAGE_WORKFLOW = os.path.join(BASE, "references", "coverage-analysis-workflow.md")
DEEP_VALIDATION = os.path.join(BASE, "references", "deep-validation-workflow.md")
COVERAGE_ANALYSIS = os.path.join(BASE, "references", "coverage-analysis.md")
LANG_TOOLING = os.path.join(BASE, "references", "language-specific-tooling.md")
SMOKE_TESTS = os.path.join(BASE, "assets", "language-smoke-tests.yaml")

EXISTING_LANGUAGES = [".NET", "Python", "Node.js", "Go", "Rust", "Java"]


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# AC#1: C++ branch in 3 workflow files
# ---------------------------------------------------------------------------

class TestAC1CppBranchInWorkflowFiles:
    """AC#1: Add C++ Branch to Coverage Step 2 in All 3 Workflow Files."""

    def test_ac1_coverage_workflow_has_cpp_branch(self):
        """coverage-analysis-workflow.md should contain a C++ IF branch."""
        content = _read(COVERAGE_WORKFLOW)
        assert re.search(r'C\+\+', content), \
            "coverage-analysis-workflow.md missing C++ branch"

    def test_ac1_coverage_workflow_has_opencppcoverage(self):
        """coverage-analysis-workflow.md C++ branch should reference OpenCppCoverage."""
        content = _read(COVERAGE_WORKFLOW)
        assert "OpenCppCoverage" in content, \
            "coverage-analysis-workflow.md missing OpenCppCoverage command"

    def test_ac1_deep_validation_has_cpp_branch(self):
        """deep-validation-workflow.md should contain C++ in Step 2."""
        content = _read(DEEP_VALIDATION)
        assert re.search(r'C\+\+', content), \
            "deep-validation-workflow.md missing C++ branch"

    def test_ac1_deep_validation_has_opencppcoverage(self):
        """deep-validation-workflow.md should reference OpenCppCoverage."""
        content = _read(DEEP_VALIDATION)
        assert "OpenCppCoverage" in content, \
            "deep-validation-workflow.md missing OpenCppCoverage command"

    def test_ac1_coverage_analysis_has_cpp_branch(self):
        """coverage-analysis.md should contain a C++ IF branch."""
        content = _read(COVERAGE_ANALYSIS)
        assert re.search(r'C\+\+', content), \
            "coverage-analysis.md missing C++ branch"

    def test_ac1_coverage_analysis_has_opencppcoverage(self):
        """coverage-analysis.md C++ branch should reference OpenCppCoverage."""
        content = _read(COVERAGE_ANALYSIS)
        assert "OpenCppCoverage" in content, \
            "coverage-analysis.md missing OpenCppCoverage command"

    def test_ac1_all_three_files_have_sources_flag(self):
        """All 3 workflow files should include --sources flag in C++ command."""
        for path in [COVERAGE_WORKFLOW, DEEP_VALIDATION, COVERAGE_ANALYSIS]:
            content = _read(path)
            # Only check if C++ section exists; must have --sources
            cpp_match = re.search(r'C\+\+.*?(?=IF language|$)', content, re.DOTALL)
            assert cpp_match and "--sources" in cpp_match.group(), \
                f"{os.path.basename(path)} C++ branch missing --sources flag"

    def test_ac1_all_three_files_have_modules_flag(self):
        """All 3 workflow files should include --modules flag in C++ command."""
        for path in [COVERAGE_WORKFLOW, DEEP_VALIDATION, COVERAGE_ANALYSIS]:
            content = _read(path)
            cpp_match = re.search(r'C\+\+.*?(?=IF language|$)', content, re.DOTALL)
            assert cpp_match and "--modules" in cpp_match.group(), \
                f"{os.path.basename(path)} C++ branch missing --modules flag"

    def test_ac1_all_three_files_have_export_type_cobertura(self):
        """All 3 workflow files should include --export_type cobertura."""
        for path in [COVERAGE_WORKFLOW, DEEP_VALIDATION, COVERAGE_ANALYSIS]:
            content = _read(path)
            cpp_match = re.search(r'C\+\+.*?(?=IF language|$)', content, re.DOTALL)
            assert cpp_match and "export_type" in cpp_match.group() and "cobertura" in cpp_match.group(), \
                f"{os.path.basename(path)} C++ branch missing --export_type cobertura"

    def test_ac1_all_three_files_have_debug_config(self):
        """All 3 workflow files should reference Debug build config."""
        for path in [COVERAGE_WORKFLOW, DEEP_VALIDATION, COVERAGE_ANALYSIS]:
            content = _read(path)
            cpp_match = re.search(r'C\+\+.*?(?=IF language|$)', content, re.DOTALL)
            assert cpp_match and "Debug" in cpp_match.group(), \
                f"{os.path.basename(path)} C++ branch missing Debug config reference"

    def test_ac1_consistency_identical_flag_pattern(self):
        """All 3 workflow files should use identical OpenCppCoverage flag patterns."""
        contents = [_read(p) for p in [COVERAGE_WORKFLOW, DEEP_VALIDATION, COVERAGE_ANALYSIS]]
        patterns = []
        for content in contents:
            match = re.search(r'OpenCppCoverage\s+(--sources\s+\{source_dir\}\s+--modules\s+\{debug_build_dir\}\s+--export_type\s+cobertura:\{coverage_dir\}/coverage\.cobertura\.xml\s+--\s+\{test_executable\})', content)
            assert match, "OpenCppCoverage command not found in one of the 3 files"
            patterns.append(match.group(1).strip())
        assert len(set(patterns)) == 1, \
            f"Inconsistent OpenCppCoverage patterns across 3 files: {patterns}"


# ---------------------------------------------------------------------------
# AC#2: C++ section in language-specific-tooling.md
# ---------------------------------------------------------------------------

class TestAC2LanguageToolingCppSection:
    """AC#2: Add C++ Section to Language-Specific Tooling Reference."""

    def test_ac2_tooling_has_cpp_section(self):
        """language-specific-tooling.md should have a C++ section."""
        content = _read(LANG_TOOLING)
        assert re.search(r'#+\s+C\+\+', content), \
            "language-specific-tooling.md missing C++ section header"

    def test_ac2_tooling_has_opencppcoverage(self):
        """C++ section should document OpenCppCoverage."""
        content = _read(LANG_TOOLING)
        assert "OpenCppCoverage" in content, \
            "language-specific-tooling.md missing OpenCppCoverage reference"

    def test_ac2_tooling_has_debug_requirement(self):
        """C++ section should document Debug build requirement."""
        content = _read(LANG_TOOLING)
        # Find C++ section and check for Debug mention
        cpp_start = content.find("C++")
        assert cpp_start != -1, "No C++ content found"
        cpp_section = content[cpp_start:cpp_start + 3000]
        assert "Debug" in cpp_section, \
            "C++ section missing Debug build requirement documentation"

    def test_ac2_quick_reference_matrix_has_7_rows(self):
        """Quick Reference Matrix table should have 7 language rows (6 existing + C++)."""
        content = _read(LANG_TOOLING)
        # Find the Quick Reference Matrix section (allow blank lines between heading and table)
        matrix_match = re.search(r'Quick Reference Matrix.*?\n\n?((?:\|.*\n)+)', content, re.IGNORECASE)
        assert matrix_match, "Quick Reference Matrix section not found"
        table_text = matrix_match.group(1)
        # Count data rows (exclude header and separator rows)
        rows = [line for line in table_text.strip().split('\n')
                if line.startswith('|') and '---' not in line]
        # Subtract header row
        data_rows = rows[1:] if rows else []
        assert len(data_rows) == 7, \
            f"Quick Reference Matrix has {len(data_rows)} data rows, expected 7"

    def test_ac2_quick_reference_matrix_has_cpp_row(self):
        """Quick Reference Matrix should include a C++ row."""
        content = _read(LANG_TOOLING)
        matrix_match = re.search(r'Quick Reference Matrix.*?\n\n?((?:\|.*\n)+)', content, re.IGNORECASE)
        assert matrix_match, "Quick Reference Matrix section not found"
        assert re.search(r'C\+\+', matrix_match.group(1)), \
            "Quick Reference Matrix missing C++ row"

    def test_ac2_story_scoped_commands_has_7_rows(self):
        """Story-Scoped Coverage Commands table should have 7 language rows."""
        content = _read(LANG_TOOLING)
        scoped_match = re.search(r'Story-Scoped Coverage Commands.*?\n(?:.*\n)*?((?:\|.*\n)+)', content, re.IGNORECASE)
        assert scoped_match, "Story-Scoped Coverage Commands section not found"
        table_text = scoped_match.group(1)
        rows = [line for line in table_text.strip().split('\n')
                if line.startswith('|') and '---' not in line]
        data_rows = rows[1:] if rows else []
        assert len(data_rows) == 7, \
            f"Story-Scoped Coverage Commands has {len(data_rows)} data rows, expected 7"

    def test_ac2_cobertura_xml_format_documented(self):
        """C++ section should note Cobertura XML reuses .NET parsing logic."""
        content = _read(LANG_TOOLING)
        cpp_start = content.find("C++")
        assert cpp_start != -1, "No C++ content found"
        cpp_section = content[cpp_start:cpp_start + 3000]
        assert "Cobertura" in cpp_section, \
            "C++ section missing Cobertura XML format documentation"


# ---------------------------------------------------------------------------
# AC#3: cpp entry in smoke tests YAML
# ---------------------------------------------------------------------------

class TestAC3SmokeTestsCppEntry:
    """AC#3: Add C++ Entry to Language Smoke Tests Configuration."""

    def test_ac3_smoke_tests_has_cpp_entry(self):
        """language-smoke-tests.yaml should have a cpp: top-level entry."""
        content = _read(SMOKE_TESTS)
        assert re.search(r'^\s*cpp:', content, re.MULTILINE), \
            "language-smoke-tests.yaml missing cpp: entry"

    def test_ac3_cpp_has_detection_pattern(self):
        """cpp entry should have detection_pattern field."""
        content = _read(SMOKE_TESTS)
        cpp_start = content.find("cpp:")
        assert cpp_start != -1, "No cpp: entry found"
        cpp_section = content[cpp_start:cpp_start + 500]
        assert "detection_pattern" in cpp_section, \
            "cpp entry missing detection_pattern field"

    def test_ac3_cpp_has_entry_point_source(self):
        """cpp entry should have entry_point_source field referencing CMakeLists.txt."""
        content = _read(SMOKE_TESTS)
        cpp_start = content.find("cpp:")
        assert cpp_start != -1, "No cpp: entry found"
        cpp_section = content[cpp_start:cpp_start + 500]
        assert "entry_point_source" in cpp_section, \
            "cpp entry missing entry_point_source field"
        assert "CMakeLists" in cpp_section, \
            "cpp entry_point_source should reference CMakeLists.txt"

    def test_ac3_cpp_has_smoke_test_command(self):
        """cpp entry should have smoke_test_command field."""
        content = _read(SMOKE_TESTS)
        cpp_start = content.find("cpp:")
        assert cpp_start != -1, "No cpp: entry found"
        cpp_section = content[cpp_start:cpp_start + 500]
        assert "smoke_test_command" in cpp_section, \
            "cpp entry missing smoke_test_command field"

    def test_ac3_cpp_has_timeout_seconds(self):
        """cpp entry should have timeout_seconds field."""
        content = _read(SMOKE_TESTS)
        cpp_start = content.find("cpp:")
        assert cpp_start != -1, "No cpp: entry found"
        cpp_section = content[cpp_start:cpp_start + 500]
        assert "timeout_seconds" in cpp_section, \
            "cpp entry missing timeout_seconds field"

    def test_ac3_cpp_has_remediation(self):
        """cpp entry should have remediation guidance."""
        content = _read(SMOKE_TESTS)
        cpp_start = content.find("cpp:")
        assert cpp_start != -1, "No cpp: entry found"
        cpp_section = content[cpp_start:cpp_start + 500]
        assert "remediation" in cpp_section.lower(), \
            "cpp entry missing remediation guidance"


# ---------------------------------------------------------------------------
# AC#4: Backward compatibility
# ---------------------------------------------------------------------------

class TestAC4BackwardCompatibility:
    """AC#4: Existing 6 language branches remain unchanged."""

    def test_ac4_dotnet_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert ".NET" in content, "coverage-analysis-workflow.md missing .NET branch"

    def test_ac4_python_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert "Python" in content, "coverage-analysis-workflow.md missing Python branch"

    def test_ac4_nodejs_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert "Node" in content, "coverage-analysis-workflow.md missing Node.js branch"

    def test_ac4_go_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert "Go" in content, "coverage-analysis-workflow.md missing Go branch"

    def test_ac4_rust_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert "Rust" in content, "coverage-analysis-workflow.md missing Rust branch"

    def test_ac4_java_branch_exists_in_coverage_workflow(self):
        content = _read(COVERAGE_WORKFLOW)
        assert "Java" in content, "coverage-analysis-workflow.md missing Java branch"

    def test_ac4_dotnet_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert ".NET" in content, "deep-validation-workflow.md missing .NET branch"

    def test_ac4_python_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert "Python" in content, "deep-validation-workflow.md missing Python branch"

    def test_ac4_nodejs_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert "Node" in content, "deep-validation-workflow.md missing Node.js branch"

    def test_ac4_go_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert "Go" in content, "deep-validation-workflow.md missing Go branch"

    def test_ac4_rust_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert "Rust" in content, "deep-validation-workflow.md missing Rust branch"

    def test_ac4_java_branch_exists_in_deep_validation(self):
        content = _read(DEEP_VALIDATION)
        assert "Java" in content, "deep-validation-workflow.md missing Java branch"

    def test_ac4_dotnet_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert ".NET" in content, "coverage-analysis.md missing .NET branch"

    def test_ac4_python_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert "Python" in content, "coverage-analysis.md missing Python branch"

    def test_ac4_nodejs_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert "Node" in content, "coverage-analysis.md missing Node.js branch"

    def test_ac4_go_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert "Go" in content, "coverage-analysis.md missing Go branch"

    def test_ac4_rust_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert "Rust" in content, "coverage-analysis.md missing Rust branch"

    def test_ac4_java_branch_exists_in_coverage_analysis(self):
        content = _read(COVERAGE_ANALYSIS)
        assert "Java" in content, "coverage-analysis.md missing Java branch"

    def test_ac4_smoke_tests_has_existing_6_languages(self):
        """Smoke tests YAML should still have all 6 existing language entries."""
        content = _read(SMOKE_TESTS)
        for lang_key in ["dotnet:", "python:", "nodejs:", "go:", "rust:", "java:"]:
            assert lang_key in content, \
                f"language-smoke-tests.yaml missing existing {lang_key} entry"

    def test_ac4_tooling_has_existing_6_languages(self):
        """language-specific-tooling.md should still have all 6 existing language sections."""
        content = _read(LANG_TOOLING)
        for lang in EXISTING_LANGUAGES:
            assert lang in content, \
                f"language-specific-tooling.md missing existing {lang} section"
