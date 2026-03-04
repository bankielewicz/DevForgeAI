"""
Test: AC#2 - Imposter Syndrome Interventions Reference
Story: STORY-469
Generated: 2026-03-04

Verifies imposter-syndrome-interventions.md exists with required sections
and contains the "Never dismisses feelings; validates then redirects" principle.
"""
import pathlib
import re

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "imposter-syndrome-interventions.md"


class TestImposterSyndromeFileExists:
    """Tests that the imposter-syndrome-interventions.md file exists."""

    def test_should_exist_at_required_path_when_story_implemented(self):
        """AC#2: File must exist at the specified path."""
        # Arrange
        expected_path = TARGET_FILE

        # Act
        exists = expected_path.is_file()

        # Assert
        assert exists, (
            f"imposter-syndrome-interventions.md not found at {expected_path}. "
            "AC#2 requires this file to exist."
        )


class TestImposterSyndromeRequiredSections:
    """Tests that required sections are present."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_contain_recognition_triggers_section_when_file_created(self, file_content: str):
        """AC#2: File must contain recognition-triggers section."""
        # Arrange
        section_pattern = "recognition-triggers"

        # Act
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )

    def test_should_contain_validate_then_redirect_section_when_file_created(self, file_content: str):
        """AC#2: File must contain validate-then-redirect section."""
        # Arrange
        section_pattern = "validate-then-redirect"

        # Act
        headers = [line for line in file_content.splitlines() if line.strip().startswith("#")]
        has_section = any(section_pattern in h.lower().replace(" ", "-") for h in headers)

        # Assert
        assert has_section, (
            f"Section '{section_pattern}' not found in any header. "
            f"Found headers: {headers[:10]}"
        )


class TestImposterSyndromePrinciple:
    """Tests that the core principle is documented."""

    @pytest.fixture
    def file_content(self) -> str:
        """Read the target file content."""
        assert TARGET_FILE.is_file(), f"File not found: {TARGET_FILE}"
        return TARGET_FILE.read_text(encoding="utf-8")

    def test_should_contain_never_dismiss_feelings_principle_when_file_created(self, file_content: str):
        """AC#2: Must contain principle 'Never dismisses feelings; validates then redirects'."""
        # Arrange
        principle_pattern = re.compile(r"never\s+dismiss", re.IGNORECASE)

        # Act
        has_principle = bool(principle_pattern.search(file_content))

        # Assert
        assert has_principle, (
            "Principle 'Never dismisses feelings; validates then redirects' "
            "not found in imposter-syndrome-interventions.md."
        )

    def test_should_mention_validate_before_redirect_when_file_created(self, file_content: str):
        """BR-001: 'validate' must appear before 'redirect' in intervention flow."""
        # Arrange
        content_lower = file_content.lower()

        # Act
        validate_pos = content_lower.find("validate")
        redirect_pos = content_lower.find("redirect")

        # Assert
        assert validate_pos != -1, "'validate' not found in file content."
        assert redirect_pos != -1, "'redirect' not found in file content."
        assert validate_pos < redirect_pos, (
            f"BR-001 violation: 'validate' (pos {validate_pos}) must appear "
            f"before 'redirect' (pos {redirect_pos}) in the intervention flow."
        )


class TestImposterSyndromeNFR:
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
            f"imposter-syndrome-interventions.md has {line_count} lines, "
            f"exceeding the {max_lines} line limit (NFR-001)."
        )
