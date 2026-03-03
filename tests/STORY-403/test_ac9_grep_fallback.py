"""
Test: AC#9 - Grep Fallback for Unsupported Languages
Story: STORY-403
Generated: 2026-02-14

Validates that Grep-based function discovery and usage search activate
as fallback for languages unsupported by Treelint (.cs, .java, .go).

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestGrepFallback:
    """Verify Grep fallback for unsupported languages."""

    def test_should_document_grep_fallback_mechanism(
        self, subagent_content
    ):
        """AC#9: Grep fallback mechanism must be documented."""
        content = subagent_content
        assert re.search(
            r"(?i)fallback", content
        ), "Fallback mechanism not documented"

    def test_should_fallback_for_csharp_files_when_treelint_unsupported(
        self, subagent_content
    ):
        """AC#9: Grep fallback must activate for .cs (C#) files."""
        content = subagent_content
        assert re.search(
            r"(?i)(\.cs\b|c\s*#|csharp)", content
        ), "C# (.cs) not listed as unsupported/fallback language"

    def test_should_fallback_for_java_files_when_treelint_unsupported(
        self, subagent_content
    ):
        """AC#9: Grep fallback must activate for .java files."""
        content = subagent_content
        assert re.search(
            r"(?i)(\.java\b|java)", content
        ), "Java (.java) not listed as unsupported/fallback language"

    def test_should_fallback_for_go_files_when_treelint_unsupported(
        self, subagent_content
    ):
        """AC#9: Grep fallback must activate for .go files."""
        content = subagent_content
        assert re.search(
            r"(?i)(\.go\b|\bgo\b)", content
        ), "Go (.go) not listed as unsupported/fallback language"

    def test_should_use_grep_for_function_discovery_in_fallback(
        self, subagent_content
    ):
        """AC#9: Grep fallback must include function discovery patterns."""
        content = subagent_content
        assert re.search(
            r"(?i)(grep.*def\s|grep.*function\s|grep.*func\s|Grep\(pattern)",
            content,
        ), "Grep-based function discovery patterns not documented"

    def test_should_use_grep_for_usage_search_in_fallback(
        self, subagent_content
    ):
        """AC#9: Grep fallback must include usage/caller search."""
        content = subagent_content
        # Verify that fallback includes searching for function callers
        assert re.search(
            r"(?i)(usage\s*search|caller.*search|grep.*caller|reference.*search)",
            content,
        ), "Grep-based usage/caller search not documented for fallback"

    def test_should_not_halt_when_treelint_unavailable(
        self, subagent_content
    ):
        """NFR-003: Subagent must complete when Treelint is missing (graceful degradation)."""
        content = subagent_content
        assert re.search(
            r"(?i)(graceful|degrad|continue|fallback.*grep|without.*halt)",
            content,
        ), "Graceful degradation behavior not documented"
