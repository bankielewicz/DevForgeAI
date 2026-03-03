"""
Test: AC#4 - Tier Mapping Backward Compatible
Story: STORY-434
Generated: 2026-02-17

Validates that:
- 0-10 to unified mapping table is documented
- 0-60 to unified mapping table is documented
- Each legacy value maps to exactly one unified tier
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCH_REFS = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
)
MATRIX_FILE = os.path.join(ARCH_REFS, "complexity-assessment-matrix.md")


@pytest.fixture
def matrix_content():
    with open(MATRIX_FILE, "r") as f:
        return f.read()


# === 0-10 Legacy Mapping ===

class TestLegacy010Mapping:
    """Verify 0-10 orchestration scale mapping to unified tiers."""

    def test_should_contain_010_mapping_table_when_documented(self, matrix_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)0\s*[-–]\s*10.*(?:map|legacy|orchestration|conversion)",
            matrix_content,
        ), "Matrix missing 0-10 legacy mapping table"

    def test_should_map_all_010_values_when_documented(self, matrix_content):
        """Every integer 0-10 should appear in or be covered by the mapping."""
        # Arrange - extract mapping ranges for 0-10
        mapping_section = re.search(
            r"(?i)(0\s*[-–]\s*10.*?(?:\n\n|\Z))", matrix_content, re.DOTALL
        )
        # Act & Assert
        assert mapping_section, "Cannot find 0-10 mapping section"
        section_text = mapping_section.group(1)
        # Verify ranges cover 0 through 10
        ranges = re.findall(r"(\d+)\s*[-–]\s*(\d+)", section_text)
        covered = set()
        for lo, hi in ranges:
            for v in range(int(lo), int(hi) + 1):
                covered.add(v)
        missing = set(range(0, 11)) - covered
        assert not missing, f"0-10 mapping missing values: {sorted(missing)}"


# === 0-60 Legacy Mapping ===

class TestLegacy060Mapping:
    """Verify 0-60 ideation scale mapping to unified tiers."""

    def test_should_contain_060_mapping_table_when_documented(self, matrix_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)0\s*[-–]\s*60.*(?:map|legacy|ideation|conversion)",
            matrix_content,
        ), "Matrix missing 0-60 legacy mapping table"

    def test_should_map_all_060_tiers_when_documented(self, matrix_content):
        """Old ideation tiers (Simple, Moderate, Complex, Enterprise) should map to unified."""
        # Arrange
        old_tiers = ["Simple", "Moderate", "Complex", "Enterprise"]
        # Act
        missing = [
            t for t in old_tiers
            if not re.search(rf"(?i)\b{t}\b", matrix_content)
        ]
        # Assert
        assert not missing, f"0-60 mapping missing old tier labels: {missing}"


# === Uniqueness of Mapping ===

class TestMappingUniqueness:
    """Verify each legacy value maps to exactly one unified tier."""

    UNIFIED_TIERS = ["Trivial", "Low", "Moderate", "High", "Critical"]

    def test_should_map_each_010_value_to_exactly_one_tier(self, matrix_content):
        """No 0-10 value should appear in multiple unified tier mappings."""
        # Arrange - extract mapping entries
        # Look for patterns like "0-2 -> Trivial" or "| 0-2 | Trivial |"
        mappings = re.findall(
            r"(\d+)\s*[-–]\s*(\d+)\s*(?:[|→\->:]+)\s*(Trivial|Low|Moderate|High|Critical)",
            matrix_content,
            re.IGNORECASE,
        )
        # Act - check for overlapping ranges
        value_to_tier = {}
        duplicates = []
        for lo, hi, tier in mappings:
            for v in range(int(lo), int(hi) + 1):
                if v in value_to_tier and value_to_tier[v].lower() != tier.lower():
                    duplicates.append(f"Value {v} maps to both {value_to_tier[v]} and {tier}")
                value_to_tier[v] = tier
        # Assert
        assert mappings, "No tier mappings found in matrix"
        assert not duplicates, f"Ambiguous mappings: {duplicates}"

    def test_should_have_mapping_section_header_when_documented(self, matrix_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:backward|legacy|mapping|compatibility)",
            matrix_content,
        ), "Matrix missing backward compatibility/mapping section"
