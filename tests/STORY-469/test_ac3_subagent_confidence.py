"""
Test: AC#3 - Business-Coach Subagent Integration
Story: STORY-469
Generated: 2026-03-04

Verifies business-coach.md contains instructions to detect confidence-related
language and load the appropriate reference files.
"""
import pathlib
import re

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "agents" / "business-coach.md"


class TestBusinessCoachFileExists:
    """Tests that the business-coach.md subagent file exists."""

    def test_should_exist_at_required_path_when_story_implemented(self):
        """AC#3: business-coach.md must exist."""
        # Arrange
        expected_path = TARGET_FILE

        # Act
        exists = expected_path.is_file()

        # Assert
        assert exists, (
            f"business-coach.md not found at {expected_path}. "
            "AC#3 requires this subagent file to exist."
        )


class TestBusinessCoachConfidenceDetection:
    """Tests that the subagent has confidence detection instructions."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_contain_confidence_detection_instructions_when_updated(self, file_content: str):
        """AC#3: Must contain instructions to detect confidence-related language."""
        # Arrange
        detection_pattern = re.compile(
            r"(detect|identify|recognize|watch for).{0,50}confidence",
            re.IGNORECASE,
        )

        # Act
        has_detection = bool(detection_pattern.search(file_content))

        # Assert
        assert has_detection, (
            "business-coach.md does not contain instructions to detect "
            "confidence-related language."
        )

    def test_should_reference_confidence_building_patterns_file_when_updated(self, file_content: str):
        """AC#3: Must reference confidence-building-patterns.md."""
        # Arrange
        reference = "confidence-building-patterns.md"

        # Act
        has_reference = reference in file_content

        # Assert
        assert has_reference, (
            f"business-coach.md does not reference '{reference}'. "
            "AC#3 requires loading this file for confidence techniques."
        )

    def test_should_reference_imposter_syndrome_interventions_file_when_updated(self, file_content: str):
        """AC#3: Must reference imposter-syndrome-interventions.md."""
        # Arrange
        reference = "imposter-syndrome-interventions.md"

        # Act
        has_reference = reference in file_content

        # Assert
        assert has_reference, (
            f"business-coach.md does not reference '{reference}'. "
            "AC#3 requires loading this file for imposter syndrome cases."
        )

    def test_should_contain_technique_application_instructions_when_updated(self, file_content: str):
        """AC#3: Must contain instructions to apply the relevant technique."""
        # Arrange
        technique_pattern = re.compile(
            r"(apply|use|follow|execute).{0,50}(technique|pattern|intervention)",
            re.IGNORECASE,
        )

        # Act
        has_technique = bool(technique_pattern.search(file_content))

        # Assert
        assert has_technique, (
            "business-coach.md does not contain instructions to apply "
            "confidence techniques or interventions."
        )
