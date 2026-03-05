"""
Test: AC#4 - Graceful Degradation When EPIC-074 Market Research Data Unavailable
Story: STORY-549
Generated: 2026-03-04

Validates graceful degradation when market research data is missing or unparseable:
clear message, manual entry fallback, workflow completes without error.
"""
import os
import re
import pytest

FRAMEWORK_FILE = "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture
def framework_content():
    """Arrange: Read the pricing-strategy-framework.md file content."""
    path = os.path.join(PROJECT_ROOT, FRAMEWORK_FILE)
    assert os.path.exists(path), f"Source file does not exist: {FRAMEWORK_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestMissingDataMessage:
    """Tests that a clear message is shown when market data is unavailable."""

    def test_should_display_unavailable_message_when_file_missing(self, framework_content):
        """AC4: Clear message when competitive-landscape.md is absent."""
        assert re.search(
            r"(unavailable|not\s+found|missing|absent).*market\s*(research|data)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"market\s*(research|data).*(unavailable|not\s+found|missing|absent)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No clear message for missing market research data documented"
        )

    def test_should_handle_unparseable_file_when_file_corrupt(self, framework_content):
        """AC4: Workflow handles unparseable/malformed market research file."""
        assert re.search(
            r"(unparseable|malformed|corrupt|invalid|parse\s*error)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No handling for unparseable market research file documented"
        )


class TestManualEntryFallback:
    """Tests that manual entry fallback activates when data unavailable."""

    def test_should_fallback_to_manual_entry_when_data_unavailable(self, framework_content):
        """AC4: Manual entry mode must activate as fallback."""
        assert re.search(
            r"manual\s*(entry|input|mode)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No manual entry fallback documented in framework"
        )

    def test_should_allow_user_to_enter_competitor_names_when_in_manual_mode(self, framework_content):
        """AC4: User can enter competitor names directly in manual mode."""
        assert re.search(
            r"(enter|input|provide).*competitor\s*name",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"competitor\s*name.*(enter|input|provide)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No instruction for manual competitor name entry documented"
        )

    def test_should_allow_user_to_enter_price_points_when_in_manual_mode(self, framework_content):
        """AC4: User can enter competitor price points directly in manual mode."""
        assert re.search(
            r"(enter|input|provide).*price\s*point",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"price\s*point.*(enter|input|provide)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No instruction for manual price point entry documented"
        )


class TestWorkflowCompletion:
    """Tests that workflow completes without error in degradation scenarios."""

    def test_should_complete_without_error_when_file_missing(self, framework_content):
        """AC4: Workflow must complete successfully when file is absent."""
        # Look for language indicating workflow continues/completes despite missing data
        assert re.search(
            r"(continue|proceed|complete|finish).*without\s*(error|fail)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"graceful\s*(degradation|fallback)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No documentation that workflow completes without error when data missing"
        )

    def test_should_complete_without_error_when_file_unparseable(self, framework_content):
        """AC4: Workflow must complete successfully when file is unparseable."""
        # Same graceful degradation should cover both missing and corrupt files
        assert re.search(
            r"(unparseable|malformed|corrupt).*(fallback|manual|continue|degrade)",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"(fallback|manual|continue|degrade).*(unparseable|malformed|corrupt)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No documentation that workflow handles unparseable file gracefully"
        )


class TestGracefulDegradationBR003:
    """BR-003: EPIC-074 integration must degrade gracefully."""

    def test_should_document_graceful_degradation_pattern_when_framework_loaded(self, framework_content):
        """BR-003: Explicit graceful degradation pattern must be documented."""
        assert re.search(r"graceful", framework_content, re.IGNORECASE), (
            "No graceful degradation pattern documented (BR-003)"
        )
