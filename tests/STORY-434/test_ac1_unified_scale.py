"""
Test: AC#1 - Unified Scoring Scale Defined
Story: STORY-434
Generated: 2026-02-17

Validates that the unified complexity scoring system has:
- 4 dimensions (Functional, Technical, Team/Org, NFR)
- 5 tiers with labels (Trivial, Low, Moderate, High, Critical)
- Tier boundaries covering full 0-60 range with no gaps or overlaps
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCH_REFS = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
)
WORKFLOW_FILE = os.path.join(ARCH_REFS, "complexity-assessment-workflow.md")
MATRIX_FILE = os.path.join(ARCH_REFS, "complexity-assessment-matrix.md")


@pytest.fixture
def workflow_content():
    """Read the unified complexity assessment workflow file."""
    with open(WORKFLOW_FILE, "r") as f:
        return f.read()


@pytest.fixture
def matrix_content():
    """Read the unified complexity assessment matrix file."""
    with open(MATRIX_FILE, "r") as f:
        return f.read()


# === Dimension Tests ===

class TestDimensionsPresent:
    """Verify all 4 scoring dimensions are defined in the unified workflow."""

    def test_should_contain_functional_dimension_when_unified_scale_defined(self, workflow_content):
        # Arrange
        expected_dimension = "Functional"
        # Act & Assert
        assert re.search(
            r"(?i)functional.*(?:0\s*[-–]\s*20|dimension|scoring)", workflow_content
        ), f"Dimension '{expected_dimension}' with scoring range not found in workflow"

    def test_should_contain_technical_dimension_when_unified_scale_defined(self, workflow_content):
        # Arrange
        expected_dimension = "Technical"
        # Act & Assert
        assert re.search(
            r"(?i)technical.*(?:0\s*[-–]\s*20|dimension|scoring)", workflow_content
        ), f"Dimension '{expected_dimension}' with scoring range not found in workflow"

    def test_should_contain_team_org_dimension_when_unified_scale_defined(self, workflow_content):
        # Arrange
        expected_dimension = "Team/Org"
        # Act & Assert
        assert re.search(
            r"(?i)team[/\s]org.*(?:0\s*[-–]\s*10|dimension|scoring)", workflow_content
        ), f"Dimension '{expected_dimension}' with scoring range not found in workflow"

    def test_should_contain_nfr_dimension_when_unified_scale_defined(self, workflow_content):
        # Arrange
        expected_dimension = "NFR"
        # Act & Assert
        assert re.search(
            r"(?i)(?:NFR|non[- ]functional).*(?:0\s*[-–]\s*10|dimension|scoring)", workflow_content
        ), f"Dimension '{expected_dimension}' with scoring range not found in workflow"

    def test_should_have_exactly_4_dimensions_when_unified_scale_defined(self, workflow_content):
        # Arrange
        dimension_patterns = [
            r"(?i)functional",
            r"(?i)technical",
            r"(?i)team[/\s]org",
            r"(?i)(?:NFR|non[- ]functional)",
        ]
        # Act
        found = sum(1 for p in dimension_patterns if re.search(p, workflow_content))
        # Assert
        assert found == 4, f"Expected 4 dimensions, found {found}"


# === Tier Tests ===

class TestTiersDefined:
    """Verify all 5 tiers with labels are defined."""

    TIER_LABELS = ["Trivial", "Low", "Moderate", "High", "Critical"]

    @pytest.mark.parametrize("tier_label", TIER_LABELS)
    def test_should_contain_tier_label_when_unified_scale_defined(self, matrix_content, tier_label):
        # Arrange & Act & Assert
        assert re.search(
            rf"(?i)\b{tier_label}\b", matrix_content
        ), f"Tier label '{tier_label}' not found in matrix"

    def test_should_have_exactly_5_tiers_when_unified_scale_defined(self, matrix_content):
        # Arrange
        tier_count = 0
        for label in self.TIER_LABELS:
            if re.search(rf"(?i)\b{label}\b.*\d+\s*[-–]\s*\d+", matrix_content):
                tier_count += 1
        # Assert
        assert tier_count == 5, f"Expected 5 tiers with numeric ranges, found {tier_count}"


# === Range Coverage Tests ===

class TestTierBoundaries:
    """Verify tier boundaries cover 0-60 with no gaps or overlaps."""

    def _extract_tier_ranges(self, content):
        """Extract (lower, upper) tuples from tier definitions."""
        # Match patterns like "Trivial: 0-10" or "| Trivial | 0-10 |"
        matches = re.findall(
            r"(?:Trivial|Low|Moderate|High|Critical)\s*[:|]\s*(\d+)\s*[-–]\s*(\d+)",
            content,
            re.IGNORECASE,
        )
        return [(int(lo), int(hi)) for lo, hi in matches]

    def test_should_start_at_zero_when_tier_ranges_defined(self, matrix_content):
        # Arrange
        ranges = self._extract_tier_ranges(matrix_content)
        # Act
        min_val = min(lo for lo, _ in ranges) if ranges else None
        # Assert
        assert ranges, "No tier ranges found in matrix"
        assert min_val == 0, f"Tier ranges start at {min_val}, expected 0"

    def test_should_end_at_60_when_tier_ranges_defined(self, matrix_content):
        # Arrange
        ranges = self._extract_tier_ranges(matrix_content)
        # Act
        max_val = max(hi for _, hi in ranges) if ranges else None
        # Assert
        assert ranges, "No tier ranges found in matrix"
        assert max_val == 60, f"Tier ranges end at {max_val}, expected 60"

    def test_should_have_no_gaps_when_tier_ranges_defined(self, matrix_content):
        # Arrange
        ranges = sorted(self._extract_tier_ranges(matrix_content))
        # Act & Assert
        assert len(ranges) >= 2, f"Need at least 2 ranges to check gaps, found {len(ranges)}"
        for i in range(1, len(ranges)):
            prev_hi = ranges[i - 1][1]
            curr_lo = ranges[i][0]
            assert curr_lo == prev_hi + 1, (
                f"Gap between tier ending at {prev_hi} and tier starting at {curr_lo}"
            )

    def test_should_have_no_overlaps_when_tier_ranges_defined(self, matrix_content):
        # Arrange
        ranges = sorted(self._extract_tier_ranges(matrix_content))
        # Act & Assert
        assert len(ranges) >= 2, f"Need at least 2 ranges to check overlaps, found {len(ranges)}"
        for i in range(1, len(ranges)):
            prev_hi = ranges[i - 1][1]
            curr_lo = ranges[i][0]
            assert curr_lo > prev_hi, (
                f"Overlap: tier ending at {prev_hi} overlaps with tier starting at {curr_lo}"
            )
