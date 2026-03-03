"""
Test: AC#3 - Treelint Function Discovery (Phase 2)
Story: STORY-403
Generated: 2026-02-14

Validates that Phase 2 uses treelint search --type function --format json
to discover all function definitions with required fields.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestTreelintFunctionDiscovery:
    """Verify Phase 2 treelint function discovery implementation."""

    def test_should_use_treelint_search_command_when_phase_2_executes(
        self, subagent_content
    ):
        """AC#3: Phase 2 must invoke treelint search --type function."""
        content = subagent_content
        assert re.search(
            r"treelint\s+search\s+--type\s+function", content
        ), "treelint search --type function command not found in Phase 2"

    def test_should_use_json_format_flag_when_treelint_invoked(
        self, subagent_content
    ):
        """AC#3: treelint commands must use --format json for AI consumption."""
        content = subagent_content
        assert re.search(
            r"treelint\s+search.*--format\s+json", content
        ), "--format json flag not found in treelint search command"

    def test_should_extract_name_field_from_treelint_results(
        self, subagent_content
    ):
        """AC#3: Function name must be extracted from treelint results."""
        content = subagent_content
        # The subagent should document extracting 'name' from results
        assert re.search(
            r'(?i)(name|function_name)', content
        ), "Function 'name' field extraction not documented"

    def test_should_extract_file_field_from_treelint_results(
        self, subagent_content
    ):
        """AC#3: File path must be extracted from treelint results."""
        content = subagent_content
        assert re.search(
            r'(?i)"file"', content
        ), "Function 'file' field extraction not documented"

    def test_should_extract_lines_start_from_treelint_results(
        self, subagent_content
    ):
        """AC#3: lines.start must be extracted from treelint results."""
        content = subagent_content
        assert re.search(
            r'(?i)(lines\.start|lines\[.start.\]|"start")', content
        ), "Function 'lines.start' field extraction not documented"

    def test_should_extract_signature_from_treelint_results(
        self, subagent_content
    ):
        """AC#3: Function signature must be extracted from treelint results."""
        content = subagent_content
        assert re.search(
            r'(?i)"signature"', content
        ), "Function 'signature' field extraction not documented"

    def test_should_support_python_typescript_javascript_when_discovering(
        self, subagent_content
    ):
        """AC#3: Function discovery must support Python, TypeScript, JavaScript."""
        content = subagent_content.lower()
        assert "python" in content, "Python language not mentioned for discovery"
        assert re.search(
            r"typescript|\.ts", content
        ), "TypeScript language not mentioned for discovery"
        assert re.search(
            r"javascript|\.js", content
        ), "JavaScript language not mentioned for discovery"
