"""
Test: AC#5 - Entry Point Exclusion (Phase 4)
Story: STORY-403
Generated: 2026-02-14

Validates that Phase 4 excludes entry point functions from the dead code
report: main(), @route, @pytest.fixture, @click.command, test_*, __init__, etc.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestEntryPointExclusion:
    """Verify Phase 4 entry point exclusion logic."""

    def test_should_exclude_main_function_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: main() must be excluded from dead code report."""
        content = subagent_content
        assert re.search(
            r"(?i)main\(\)", content
        ), "main() not listed as entry point exclusion"

    def test_should_exclude_route_decorator_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: @route / @app.route must be excluded from dead code report."""
        content = subagent_content
        assert re.search(
            r"(?i)@(app\.)?route", content
        ), "@route not listed as entry point exclusion"

    def test_should_exclude_pytest_fixture_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: @pytest.fixture must be excluded from dead code report."""
        content = subagent_content
        assert re.search(
            r"(?i)@pytest\.fixture", content
        ), "@pytest.fixture not listed as entry point exclusion"

    def test_should_exclude_click_command_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: @click.command must be excluded from dead code report."""
        content = subagent_content
        assert re.search(
            r"(?i)@click\.command", content
        ), "@click.command not listed as entry point exclusion"

    def test_should_exclude_test_prefixed_functions_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: test_* functions must be excluded from dead code report."""
        content = subagent_content
        assert re.search(
            r"(?i)test_\*", content
        ), "test_* pattern not listed as entry point exclusion"

    def test_should_exclude_dunder_init_when_zero_callers(
        self, subagent_content
    ):
        """AC#5: __init__ must be excluded (dunder methods called implicitly)."""
        content = subagent_content
        assert re.search(
            r"(?i)__init__", content
        ), "__init__ not listed as entry point exclusion"

    def test_should_have_entry_point_patterns_reference_file(
        self, entry_point_patterns_content
    ):
        """AC#5: Entry point patterns must be in a dedicated reference file."""
        content = entry_point_patterns_content
        assert len(content) > 0, "Entry point patterns reference file is empty"

    def test_should_list_python_entry_points_in_reference_file(
        self, entry_point_patterns_content
    ):
        """AC#5: Reference file must include Python entry point patterns."""
        content = entry_point_patterns_content.lower()
        assert "python" in content, "Python entry points not documented"
        assert "main()" in content or "main" in content, (
            "main() not in Python patterns"
        )
        assert "pytest.fixture" in content, (
            "@pytest.fixture not in Python patterns"
        )

    def test_should_list_typescript_entry_points_in_reference_file(
        self, entry_point_patterns_content
    ):
        """AC#5: Reference file must include TypeScript entry point patterns."""
        content = entry_point_patterns_content.lower()
        assert "typescript" in content, "TypeScript entry points not documented"

    def test_should_exclude_dunder_methods_from_dead_code_report(
        self, subagent_content
    ):
        """BR-003: Dunder methods (__str__, __repr__, etc.) must be excluded."""
        content = subagent_content
        assert re.search(
            r"(?i)(dunder|__\w+__)", content
        ), "Dunder method exclusion not documented"
