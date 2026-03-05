"""
Test: AC#5 - Skill File Structure Compliance
Story: STORY-535
Generated: 2026-03-04

Validates that SKILL.md is under 1000 lines, has YAML frontmatter,
and required reference files exist.

Tests target src/ tree per CLAUDE.md.
"""
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "researching-market"
SKILL_FILE = SKILL_DIR / "SKILL.md"
REFERENCES_DIR = SKILL_DIR / "references"


class TestSkillFileExists:
    """Tests that the skill file exists at the correct path."""

    def test_should_have_skill_md_at_expected_path(self):
        """Arrange: Expected path. Act: Check existence. Assert: File exists."""
        assert SKILL_FILE.exists(), (
            f"SKILL.md not found at {SKILL_FILE}. "
            "The researching-market skill must be created."
        )

    def test_should_have_references_directory(self):
        """Arrange: Skill directory. Act: Check references dir. Assert: Directory exists."""
        assert REFERENCES_DIR.exists() and REFERENCES_DIR.is_dir(), (
            f"references/ directory not found at {REFERENCES_DIR}."
        )


class TestSkillFileLineCount:
    """Tests that SKILL.md is under 1000 lines."""

    def test_should_be_under_1000_lines(self):
        """Arrange: SKILL.md exists. Act: Count lines. Assert: Under 1000."""
        content = SKILL_FILE.read_text()
        line_count = len(content.splitlines())
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines, exceeding the 1000-line limit. "
            "Extract content to reference files."
        )


class TestYamlFrontmatter:
    """Tests that SKILL.md has valid YAML frontmatter."""

    def test_should_start_with_yaml_frontmatter(self):
        """Arrange: SKILL.md exists. Act: Read start. Assert: Starts with ---."""
        content = SKILL_FILE.read_text()
        assert content.startswith("---"), (
            "SKILL.md must start with YAML frontmatter (---). "
            "All skills require YAML frontmatter metadata."
        )

    def test_should_have_closing_yaml_delimiter(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Closing --- present."""
        content = SKILL_FILE.read_text()
        # Find second occurrence of ---
        first_end = content.index("---") + 3
        remaining = content[first_end:]
        assert "---" in remaining, (
            "SKILL.md YAML frontmatter must have closing --- delimiter."
        )

    def test_should_have_name_in_frontmatter(self):
        """Arrange: SKILL.md exists. Act: Parse frontmatter. Assert: name field present."""
        content = SKILL_FILE.read_text()
        # Extract frontmatter between first two ---
        parts = content.split("---", 2)
        frontmatter = parts[1] if len(parts) >= 3 else ""
        assert re.search(r"^name:", frontmatter, re.MULTILINE), (
            "SKILL.md YAML frontmatter must include a 'name' field."
        )


class TestMarketSizingMethodologyReference:
    """Tests that references/market-sizing-methodology.md exists."""

    def test_should_have_market_sizing_methodology_file(self):
        """Arrange: References dir. Act: Check file. Assert: File exists."""
        methodology_file = REFERENCES_DIR / "market-sizing-methodology.md"
        assert methodology_file.exists(), (
            f"market-sizing-methodology.md not found at {methodology_file}. "
            "Market sizing methodology must be documented in a reference file."
        )

    def test_should_have_content_in_methodology_file(self):
        """Arrange: File exists. Act: Read content. Assert: Non-empty with relevant content."""
        methodology_file = REFERENCES_DIR / "market-sizing-methodology.md"
        content = methodology_file.read_text()
        assert len(content.strip()) > 100, (
            "market-sizing-methodology.md must contain substantive methodology documentation."
        )

    def test_should_cover_tam_sam_som_in_methodology(self):
        """Arrange: File exists. Act: Read content. Assert: All tiers covered."""
        methodology_file = REFERENCES_DIR / "market-sizing-methodology.md"
        content = methodology_file.read_text()
        for tier in ["TAM", "SAM", "SOM"]:
            assert tier in content, (
                f"market-sizing-methodology.md must document {tier} methodology."
            )


class TestFermiEstimationReference:
    """Tests that references/fermi-estimation.md exists."""

    def test_should_have_fermi_estimation_file(self):
        """Arrange: References dir. Act: Check file. Assert: File exists."""
        fermi_file = REFERENCES_DIR / "fermi-estimation.md"
        assert fermi_file.exists(), (
            f"fermi-estimation.md not found at {fermi_file}. "
            "Fermi estimation guidance must be documented in a reference file."
        )

    def test_should_have_content_in_fermi_file(self):
        """Arrange: File exists. Act: Read content. Assert: Non-empty with relevant content."""
        fermi_file = REFERENCES_DIR / "fermi-estimation.md"
        content = fermi_file.read_text()
        assert len(content.strip()) > 100, (
            "fermi-estimation.md must contain substantive Fermi estimation guidance."
        )

    def test_should_explain_fermi_estimation_method(self):
        """Arrange: File exists. Act: Read content. Assert: Fermi method explained."""
        fermi_file = REFERENCES_DIR / "fermi-estimation.md"
        content = fermi_file.read_text()
        assert re.search(r"fermi", content, re.IGNORECASE), (
            "fermi-estimation.md must explain the Fermi estimation method."
        )


class TestSkillReferencesFromSkillFile:
    """Tests that SKILL.md references its reference files."""

    def test_should_reference_methodology_file_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: References methodology."""
        content = SKILL_FILE.read_text()
        assert "market-sizing-methodology" in content, (
            "SKILL.md must reference references/market-sizing-methodology.md."
        )

    def test_should_reference_fermi_file_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: References Fermi."""
        content = SKILL_FILE.read_text()
        assert "fermi-estimation" in content, (
            "SKILL.md must reference references/fermi-estimation.md."
        )
