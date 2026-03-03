"""
Test: AC#5 - No Duplicate Scoring or Decomposition Files Remain
Story: STORY-434
Generated: 2026-02-17

Validates that:
- No separate overlapping decomposition files exist
- No duplicate scoring rubrics remain
- Zero content duplication across complexity files
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCH_REFS = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
)


# === No Overlapping Decomposition Files ===

class TestNoOverlappingDecompositionFiles:
    """After merge, only feature-decomposition.md should exist."""

    def test_should_not_have_both_epic_and_feature_decomposition_files(self):
        """epic-decomposition-workflow.md and feature-decomposition-patterns.md
        should not both exist (they should be merged into feature-decomposition.md)."""
        # Arrange
        epic_decomp = os.path.join(ARCH_REFS, "epic-decomposition-workflow.md")
        feature_patterns = os.path.join(ARCH_REFS, "feature-decomposition-patterns.md")
        # Act
        both_exist = os.path.isfile(epic_decomp) and os.path.isfile(feature_patterns)
        # Assert
        assert not both_exist, (
            "Both epic-decomposition-workflow.md and feature-decomposition-patterns.md "
            "still exist - they should be merged into feature-decomposition.md"
        )

    def test_should_have_single_authoritative_decomposition_file(self):
        # Arrange
        merged = os.path.join(ARCH_REFS, "feature-decomposition.md")
        # Act & Assert
        assert os.path.isfile(merged), (
            "Single authoritative feature-decomposition.md not found"
        )


# === No Duplicate Scoring Rubrics ===

class TestNoDuplicateScoringRubrics:
    """technical-assessment-guide.md should not contain a full scoring rubric."""

    def test_should_not_have_full_rubric_in_tech_guide(self):
        # Arrange
        tech_guide = os.path.join(ARCH_REFS, "technical-assessment-guide.md")
        if not os.path.isfile(tech_guide):
            pytest.skip("technical-assessment-guide.md not found")
        with open(tech_guide, "r") as f:
            content = f.read()
        # Act - look for detailed per-band scoring descriptions (old rubric)
        # Old rubric had 5 bands with detailed descriptions
        band_patterns = [
            r"(?i)\btrivial\b.*\d+\s*[-–]\s*\d+",
            r"(?i)\blow\b.*\d+\s*[-–]\s*\d+",
            r"(?i)\bmoderate\b.*\d+\s*[-–]\s*\d+",
            r"(?i)\bhigh\b.*\d+\s*[-–]\s*\d+",
            r"(?i)\bcritical\b.*\d+\s*[-–]\s*\d+",
        ]
        rubric_bands_found = sum(1 for p in band_patterns if re.search(p, content))
        # Assert - should NOT have all 5 bands (that would be a full rubric)
        assert rubric_bands_found < 3, (
            f"technical-assessment-guide.md still contains {rubric_bands_found}/5 "
            "scoring bands - full rubric should be removed (replaced with pointer)"
        )


# === Zero Content Duplication ===

class TestZeroContentDuplication:
    """No substantial content duplication across complexity files."""

    def _get_complexity_files(self):
        """Return list of complexity-related files in architecture references."""
        if not os.path.isdir(ARCH_REFS):
            return []
        complexity_files = []
        for fname in os.listdir(ARCH_REFS):
            if any(kw in fname.lower() for kw in ["complexity", "assessment", "scoring"]):
                fpath = os.path.join(ARCH_REFS, fname)
                if os.path.isfile(fpath):
                    complexity_files.append(fpath)
        return complexity_files

    def _extract_headings(self, content):
        """Extract markdown headings as content fingerprints."""
        return set(re.findall(r"^#{1,4}\s+(.+)$", content, re.MULTILINE))

    def test_should_not_have_duplicate_section_headings_across_files(self):
        """No two complexity files should share more than 30% of section headings."""
        # Arrange
        files = self._get_complexity_files()
        if len(files) < 2:
            pytest.skip("Need at least 2 complexity files to check duplication")

        file_headings = {}
        for fpath in files:
            with open(fpath, "r") as f:
                file_headings[fpath] = self._extract_headings(f.read())

        # Act - check pairwise overlap
        duplicates = []
        file_list = list(file_headings.keys())
        for i in range(len(file_list)):
            for j in range(i + 1, len(file_list)):
                h1 = file_headings[file_list[i]]
                h2 = file_headings[file_list[j]]
                if not h1 or not h2:
                    continue
                overlap = h1 & h2
                overlap_pct = len(overlap) / min(len(h1), len(h2))
                if overlap_pct > 0.3:
                    duplicates.append(
                        f"{os.path.basename(file_list[i])} <-> "
                        f"{os.path.basename(file_list[j])}: "
                        f"{overlap_pct:.0%} heading overlap ({overlap})"
                    )

        # Assert
        assert not duplicates, (
            f"Content duplication detected across complexity files:\n"
            + "\n".join(duplicates)
        )

    def test_should_not_have_multiple_tier_definition_tables(self):
        """Only one file should define the full tier table (matrix)."""
        # Arrange
        files = self._get_complexity_files()
        tier_table_pattern = r"(?i)(?:Trivial|Low|Moderate|High|Critical)\s*[|:]\s*\d+\s*[-–]\s*\d+"

        files_with_tier_tables = []
        for fpath in files:
            with open(fpath, "r") as f:
                content = f.read()
            matches = re.findall(tier_table_pattern, content)
            if len(matches) >= 3:  # At least 3 tier definitions = full table
                files_with_tier_tables.append(os.path.basename(fpath))

        # Assert - only 1 file should have the full tier table
        assert len(files_with_tier_tables) <= 1, (
            f"Multiple files contain full tier definition tables: {files_with_tier_tables}. "
            "Only complexity-assessment-matrix.md should define tiers."
        )
