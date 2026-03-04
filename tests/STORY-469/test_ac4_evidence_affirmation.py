"""
Test: AC#4 - Evidence-Based Affirmation
Story: STORY-469
Generated: 2026-03-04

Verifies that confidence-building-patterns.md contains evidence-based
affirmation templates referencing user's actual progress data,
NOT generic encouragement.
"""
import pathlib
import re

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "confidence-building-patterns.md"


class TestEvidenceBasedAffirmationExists:
    """Tests that evidence-based affirmation content exists."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_contain_affirmation_templates_when_file_created(self, file_content: str):
        """AC#4: File must contain affirmation templates."""
        # Arrange
        template_pattern = re.compile(
            r"(template|example|sample).{0,30}affirmation",
            re.IGNORECASE,
        )

        # Act
        has_templates = bool(template_pattern.search(file_content))

        # Assert
        assert has_templates, (
            "No affirmation templates found in confidence-building-patterns.md. "
            "AC#4 requires evidence-based affirmation templates."
        )


class TestAffirmationReferencesProgressData:
    """Tests that affirmations reference actual progress data, not generic encouragement."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_reference_milestone_data_when_providing_affirmation(self, file_content: str):
        """AC#4: Affirmation templates must reference milestone or progress data."""
        # Arrange
        progress_pattern = re.compile(
            r"(milestone|progress|completed|achievement|track record|accomplishment)",
            re.IGNORECASE,
        )

        # Act
        has_progress_ref = bool(progress_pattern.search(file_content))

        # Assert
        assert has_progress_ref, (
            "Affirmation templates do not reference progress/milestone data. "
            "AC#4 requires evidence-based affirmations using actual user progress."
        )

    def test_should_contain_progress_data_placeholder_when_providing_affirmation(self, file_content: str):
        """AC#4: Templates should contain placeholders for user-specific data (e.g., {milestone_count})."""
        # Arrange
        placeholder_pattern = re.compile(
            r"(\{[^}]*(?:milestone|progress|count|completed)[^}]*\}|"
            r"\[[^\]]*(?:milestone|progress|count|completed)[^\]]*\]|"
            r"<[^>]*(?:milestone|progress|count|completed)[^>]*>)",
            re.IGNORECASE,
        )

        # Act
        has_placeholder = bool(placeholder_pattern.search(file_content))

        # Assert
        assert has_placeholder, (
            "No progress data placeholders found in affirmation templates. "
            "AC#4 requires templates that reference user's actual data "
            "(e.g., '{milestone_count}', '[completed milestones]')."
        )

    def test_should_not_contain_only_generic_encouragement_when_providing_affirmation(self, file_content: str):
        """BR-002: Affirmations must be evidence-based, not generic."""
        # Arrange
        # Extract the evidence-based-affirmation section
        content_lower = file_content.lower()
        section_start = content_lower.find("evidence-based")
        assert section_start != -1, "evidence-based-affirmation section not found"

        section_content = file_content[section_start:]
        # Find next top-level section to bound the search
        next_section = re.search(r"\n##\s", section_content[1:])
        if next_section:
            section_content = section_content[: next_section.start() + 1]

        # Act - Check that section references concrete data, not just platitudes
        evidence_indicators = re.compile(
            r"(data|metric|milestone|progress|track|measure|evidence|specific|actual)",
            re.IGNORECASE,
        )
        generic_only = not bool(evidence_indicators.search(section_content))

        # Assert
        assert not generic_only, (
            "BR-002 violation: The evidence-based-affirmation section contains "
            "only generic encouragement without references to concrete data, "
            "metrics, or user progress."
        )
