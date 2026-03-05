"""
Test: AC#1 - TAM/SAM/SOM Output Structure
Story: STORY-535
Generated: 2026-03-04

Validates that the market sizing skill produces output containing
all three tiers (TAM, SAM, SOM) with dollar values, methodology notes,
source citations, and confidence levels.

Tests target src/ tree per CLAUDE.md.
"""
import re
from pathlib import Path

import pytest

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Skill source files
SKILL_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "researching-market"
SKILL_FILE = SKILL_DIR / "SKILL.md"
METHODOLOGY_REF = SKILL_DIR / "references" / "market-sizing-methodology.md"

# Expected output location
OUTPUT_FILE = PROJECT_ROOT / "devforgeai" / "specs" / "business" / "market-research" / "market-sizing.md"


class TestSkillDefinesOutputStructure:
    """Tests that SKILL.md defines the TAM/SAM/SOM output structure."""

    def test_should_have_skill_file_at_expected_path(self):
        """Arrange: Skill directory exists. Act: Check path. Assert: SKILL.md exists."""
        assert SKILL_FILE.exists(), (
            f"SKILL.md not found at {SKILL_FILE}. "
            "The researching-market skill must be created."
        )

    def test_should_reference_tam_section_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: TAM section referenced."""
        content = SKILL_FILE.read_text()
        assert re.search(r"##\s+TAM|TAM.*Total Addressable Market", content, re.IGNORECASE), (
            "SKILL.md must reference TAM (Total Addressable Market) section in output specification."
        )

    def test_should_reference_sam_section_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: SAM section referenced."""
        content = SKILL_FILE.read_text()
        assert re.search(r"##\s+SAM|SAM.*Serviceable Addressable Market", content, re.IGNORECASE), (
            "SKILL.md must reference SAM (Serviceable Addressable Market) section in output specification."
        )

    def test_should_reference_som_section_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: SOM section referenced."""
        content = SKILL_FILE.read_text()
        assert re.search(r"##\s+SOM|SOM.*Serviceable Obtainable Market", content, re.IGNORECASE), (
            "SKILL.md must reference SOM (Serviceable Obtainable Market) section in output specification."
        )


class TestOutputRequiresDollarValues:
    """Tests that output specification requires dollar-value estimates for each tier."""

    def test_should_specify_dollar_value_format_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Dollar value format specified."""
        content = SKILL_FILE.read_text()
        assert re.search(r"\$[\d.,]+[BMKbmk]|\bdollar\b|\bvalue\b.*\bestimate\b", content, re.IGNORECASE), (
            "SKILL.md must specify dollar-value format for market size estimates."
        )


class TestOutputRequiresMethodologyNotes:
    """Tests that each tier includes methodology notes (top-down, bottom-up, or Fermi)."""

    def test_should_specify_methodology_field_in_output(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Methodology field required."""
        content = SKILL_FILE.read_text()
        assert re.search(r"methodology", content, re.IGNORECASE), (
            "SKILL.md must require methodology notes (top-down, bottom-up, or Fermi) for each tier."
        )

    def test_should_reference_valid_methodology_types(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Valid methodology types listed."""
        content = SKILL_FILE.read_text()
        methodologies_found = sum(
            1 for m in ["top-down", "bottom-up", "fermi"]
            if m in content.lower()
        )
        assert methodologies_found >= 2, (
            "SKILL.md must reference at least 2 of: top-down, bottom-up, Fermi methodologies."
        )


class TestOutputRequiresSourceCitations:
    """Tests that data sources are cited in the output."""

    def test_should_require_source_citations_in_output(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Source citation requirement."""
        content = SKILL_FILE.read_text()
        assert re.search(r"source|citation|cited|reference", content, re.IGNORECASE), (
            "SKILL.md must require source citations for data points in market sizing output."
        )


class TestOutputRequiresConfidenceLevels:
    """Tests that each tier has a confidence level (High/Medium/Low)."""

    def test_should_specify_confidence_levels_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Confidence levels defined."""
        content = SKILL_FILE.read_text()
        assert re.search(r"confidence", content, re.IGNORECASE), (
            "SKILL.md must define confidence levels for market sizing estimates."
        )

    def test_should_use_high_medium_low_scale(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: High/Medium/Low scale used."""
        content = SKILL_FILE.read_text()
        levels_found = sum(
            1 for level in ["High", "Medium", "Low"]
            if level in content
        )
        assert levels_found >= 3, (
            "SKILL.md must use High/Medium/Low confidence scale. "
            f"Found {levels_found}/3 levels."
        )


class TestOutputFileTargetPath:
    """Tests that SKILL.md specifies the correct output file path."""

    def test_should_specify_output_path_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Output path defined."""
        content = SKILL_FILE.read_text()
        assert "market-sizing.md" in content, (
            "SKILL.md must specify market-sizing.md as the output file."
        )

    def test_should_target_business_market_research_directory(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Correct output directory."""
        content = SKILL_FILE.read_text()
        assert re.search(r"devforgeai/specs/business/market-research", content), (
            "SKILL.md must target devforgeai/specs/business/market-research/ for output."
        )


class TestBusinessRuleTamSamSomOrdering:
    """BR-001: TAM >= SAM >= SOM > 0 invariant."""

    def test_should_enforce_tam_gte_sam_gte_som_in_skill(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Ordering constraint documented."""
        content = SKILL_FILE.read_text()
        assert re.search(r"TAM.*>=.*SAM.*>=.*SOM|TAM.*SAM.*SOM.*order|invariant", content, re.IGNORECASE), (
            "SKILL.md must document TAM >= SAM >= SOM > 0 invariant (BR-001)."
        )

    def test_should_require_positive_values(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Values must be > 0."""
        content = SKILL_FILE.read_text()
        assert re.search(r">\s*0|positive|non-zero|greater than zero", content, re.IGNORECASE), (
            "SKILL.md must require all tier values to be greater than zero."
        )


class TestBusinessRuleSourceAttribution:
    """BR-002: All data points must have source attribution."""

    def test_should_require_source_for_all_data_points(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Source attribution required."""
        content = SKILL_FILE.read_text()
        assert re.search(r"source.*attribution|all.*data.*source|every.*figure.*source", content, re.IGNORECASE), (
            "SKILL.md must require source attribution for all data points (BR-002)."
        )
