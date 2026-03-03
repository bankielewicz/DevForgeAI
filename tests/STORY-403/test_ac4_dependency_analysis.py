"""
Test: AC#4 - Treelint Dependency Analysis (Phase 3)
Story: STORY-403
Generated: 2026-02-14

Validates that Phase 3 uses treelint deps --calls to analyze function
dependencies and identify zero-caller functions.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestTreelintDependencyAnalysis:
    """Verify Phase 3 treelint dependency analysis implementation."""

    def test_should_use_treelint_deps_command_when_phase_3_executes(
        self, subagent_content
    ):
        """AC#4: Phase 3 must invoke treelint deps --calls."""
        content = subagent_content
        assert re.search(
            r"treelint\s+deps\s+--calls", content
        ), "treelint deps --calls command not found in Phase 3"

    def test_should_use_symbol_flag_for_function_lookup(
        self, subagent_content
    ):
        """AC#4: treelint deps must use --symbol flag for per-function lookup."""
        content = subagent_content
        assert re.search(
            r"treelint\s+deps.*--symbol", content
        ), "--symbol flag not found in treelint deps command"

    def test_should_extract_callers_array_from_deps_results(
        self, subagent_content
    ):
        """AC#4: callers[] array must be extracted from dependency results."""
        content = subagent_content
        assert re.search(
            r"(?i)callers", content
        ), "callers array not documented in dependency analysis"

    def test_should_extract_callees_array_from_deps_results(
        self, subagent_content
    ):
        """AC#4: callees[] array must be extracted from dependency results."""
        content = subagent_content
        assert re.search(
            r"(?i)callees", content
        ), "callees array not documented in dependency analysis"

    def test_should_flag_zero_caller_functions_as_candidates(
        self, subagent_content
    ):
        """AC#4: Functions with 0 callers must be flagged as dead code candidates."""
        content = subagent_content
        assert re.search(
            r"(?i)(zero.caller|0\s*caller|no\s*caller|caller.*==?\s*0|callers.*empty)",
            content,
        ), "Zero-caller detection logic not documented"

    def test_should_use_json_format_for_deps_output(
        self, subagent_content
    ):
        """AC#4: treelint deps must use --format json for AI consumption."""
        content = subagent_content
        assert re.search(
            r"treelint\s+deps.*--format\s+json", content
        ), "--format json flag not found in treelint deps command"
