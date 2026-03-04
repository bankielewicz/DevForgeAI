"""
Test: AC#1 - Confidence Patterns Reference File
Story: STORY-469
Generated: 2026-03-04

Verifies confidence-building-patterns.md exists at the correct path
and contains the 4 required sections.
"""
import pathlib

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "confidence-building-patterns.md"


class TestConfidencePatternsFileExists:
    """Tests that the confidence-building-patterns.md file exists."""

    def test_should_exist_at_required_path_when_story_implemented(self):
        """AC#1: File must exist at src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md"""
        # Arrange
        expected_path = TARGET_FILE

        # Act
        exists = expected_path.is_file()

        # Assert
        assert exists, (
            f"confidence-building-patterns.md not found at {expected_path}. "
            "AC#1 requires this file to exist."
        )


class TestConfidencePatternsRequiredSections:
    """Tests that all 4 required sections are present."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_contain_imposter_syndrome_recognition_section_when_file_created(self, file_content: str):
        """AC#1: File must contain imposter-syndrome-recognition section."""
        # Arrange
        section_pattern = "imposter-syndrome-recognition"

        # Act
        content_lower = file_content.lower()
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )

    def test_should_contain_reframing_techniques_section_when_file_created(self, file_content: str):
        """AC#1: File must contain reframing-techniques section."""
        # Arrange
        section_pattern = "reframing-techniques"

        # Act
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )

    def test_should_contain_evidence_based_affirmation_section_when_file_created(self, file_content: str):
        """AC#1: File must contain evidence-based-affirmation section."""
        # Arrange
        section_pattern = "evidence-based-affirmation"

        # Act
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )

    def test_should_contain_momentum_tracking_section_when_file_created(self, file_content: str):
        """AC#1: File must contain momentum-tracking section."""
        # Arrange
        section_pattern = "momentum-tracking"

        # Act
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )


class TestConfidencePatternsNFR:
    """Non-functional requirement: file under 1500 lines."""

    def test_should_have_fewer_than_1500_lines_when_file_created(self):
        """NFR-001: Reference files under 1500 lines each."""
        # Arrange
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        max_lines = 1500

        # Act
        line_count = len(TARGET_FILE.read_text(encoding="utf-8").splitlines())

        # Assert
        assert line_count < max_lines, (
            f"confidence-building-patterns.md has {line_count} lines, "
            f"exceeding the {max_lines} line limit (NFR-001)."
        )
