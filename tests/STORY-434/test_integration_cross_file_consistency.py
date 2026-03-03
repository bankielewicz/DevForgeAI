"""Integration tests for STORY-434: Cross-file consistency validation.

Tests verify:
1. Cross-file reference integrity (correct references between complexity files)
2. Content consistency (tier names and ranges match across all files)
3. File system state (deleted files gone, new files exist)
"""

import os
import re
from pathlib import Path


class TestCrossFileReferenceIntegrity:
    """Validate cross-file references are correct and unbroken."""

    ARCHITECTURE_REFS = Path("src/claude/skills/devforgeai-architecture/references")

    def test_workflow_references_matrix_by_name(self):
        """When workflow.md references matrix, reference name must match actual file."""
        workflow_path = self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md"
        matrix_path = self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md"

        assert workflow_path.exists(), f"Workflow file missing: {workflow_path}"
        assert matrix_path.exists(), f"Matrix file missing: {matrix_path}"

        workflow_content = workflow_path.read_text()
        # Check for reference by filename
        assert "complexity-assessment-matrix.md" in workflow_content, \
            "Workflow must reference complexity-assessment-matrix.md by name"

    def test_tech_guide_references_unified_files(self):
        """When tech guide references unified files, names must match actual files."""
        tech_guide_path = self.ARCHITECTURE_REFS / "technical-assessment-guide.md"
        workflow_path = self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md"
        matrix_path = self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md"

        assert tech_guide_path.exists(), f"Tech guide missing: {tech_guide_path}"

        tech_guide_content = tech_guide_path.read_text()
        # Should reference both unified files
        assert "complexity-assessment-workflow.md" in tech_guide_content, \
            "Tech guide must reference workflow file"
        assert "complexity-assessment-matrix.md" in tech_guide_content, \
            "Tech guide must reference matrix file"

    def test_no_broken_cross_references(self):
        """No file references non-existent files."""
        workflow = (self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md").read_text()
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()
        tech_guide = (self.ARCHITECTURE_REFS / "technical-assessment-guide.md").read_text()

        all_content = workflow + matrix + tech_guide

        # Look for markdown file references
        file_refs = re.findall(r'`?([a-z\-]+\.md)`?', all_content)
        for ref in file_refs:
            if ref in ["complexity-assessment-workflow.md", "complexity-assessment-matrix.md",
                       "technical-assessment-guide.md", "feature-decomposition.md"]:
                expected_path = self.ARCHITECTURE_REFS / ref
                assert expected_path.exists(), \
                    f"Cross-reference broken: {ref} referenced but file missing"


class TestContentConsistencyAcrossFiles:
    """Validate tier names and ranges match across all files."""

    ARCHITECTURE_REFS = Path("src/claude/skills/devforgeai-architecture/references")
    EXPECTED_TIERS = ["Trivial", "Low", "Moderate", "High", "Critical"]
    EXPECTED_RANGES = {
        "Trivial": "0-10",
        "Low": "11-20",
        "Moderate": "21-35",
        "High": "36-50",
        "Critical": "51-60",
    }

    def test_all_tier_names_consistent_across_workflow_and_matrix(self):
        """Tier names must be identical in workflow and matrix."""
        workflow = (self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md").read_text()
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        for tier_name in self.EXPECTED_TIERS:
            assert tier_name in workflow, f"Tier '{tier_name}' missing in workflow.md"
            assert tier_name in matrix, f"Tier '{tier_name}' missing in matrix.md"

    def test_tier_ranges_match_in_workflow_and_matrix(self):
        """Tier ranges (0-10, 11-20, etc.) must be consistent in both files."""
        workflow = (self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md").read_text()
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        for tier_name, tier_range in self.EXPECTED_RANGES.items():
            # Check that both files contain the tier with its range
            workflow_has = f"{tier_name}" in workflow and tier_range in workflow
            matrix_has = f"{tier_name}" in matrix and tier_range in matrix

            assert workflow_has, \
                f"Workflow missing tier '{tier_name}' with range '{tier_range}'"
            assert matrix_has, \
                f"Matrix missing tier '{tier_name}' with range '{tier_range}'"

    def test_dimension_count_consistent(self):
        """Both workflow and matrix must reference exactly 4 dimensions."""
        workflow = (self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md").read_text()
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        expected_dims = [
            "Functional",
            "Technical",
            "Team/Org",
            "NFR"
        ]

        for dim in expected_dims:
            assert dim in workflow, f"Dimension '{dim}' missing in workflow.md"
            assert dim in matrix, f"Dimension '{dim}' missing in matrix.md"

    def test_tech_guide_no_duplicate_full_rubric(self):
        """Tech guide should NOT contain full scoring rubric (should reference instead)."""
        tech_guide = (self.ARCHITECTURE_REFS / "technical-assessment-guide.md").read_text()

        # Check that tech guide doesn't have detailed scoring tables that duplicate matrix
        # It should have "See complexity-assessment-matrix.md" type references instead
        has_reference = "complexity-assessment-matrix" in tech_guide
        assert has_reference, "Tech guide must reference unified files, not duplicate rubric"

    def test_no_conflicting_scale_definitions(self):
        """Files must not contain conflicting scale definitions (e.g., 0-10 vs 0-60)."""
        workflow = (self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md").read_text()
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        # Look for scale definitions - both should use 0-60
        workflow_scale_match = re.search(r'(?:range|scale):\s*(\d+)-(\d+)', workflow, re.IGNORECASE)
        matrix_scale_match = re.search(r'(?:range|scale):\s*(\d+)-(\d+)', matrix, re.IGNORECASE)

        if workflow_scale_match:
            workflow_range = f"{workflow_scale_match.group(1)}-{workflow_scale_match.group(2)}"
            assert workflow_range == "0-60", f"Workflow defines conflicting scale: {workflow_range}"

        if matrix_scale_match:
            matrix_range = f"{matrix_scale_match.group(1)}-{matrix_scale_match.group(2)}"
            assert matrix_range == "0-60", f"Matrix defines conflicting scale: {matrix_range}"


class TestFileSystemState:
    """Verify deleted files are gone, new files exist, modified files are present."""

    ARCHITECTURE_REFS = Path("src/claude/skills/devforgeai-architecture/references")

    def test_unified_complexity_workflow_exists(self):
        """Modified: complexity-assessment-workflow.md must exist."""
        path = self.ARCHITECTURE_REFS / "complexity-assessment-workflow.md"
        assert path.exists(), "Unified workflow file missing"
        assert path.stat().st_size > 5000, "Workflow file appears empty or corrupted"

    def test_unified_complexity_matrix_exists(self):
        """Modified: complexity-assessment-matrix.md must exist."""
        path = self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md"
        assert path.exists(), "Unified matrix file missing"
        assert path.stat().st_size > 10000, "Matrix file appears empty or corrupted"

    def test_technical_assessment_guide_exists(self):
        """Modified: technical-assessment-guide.md must exist and reference unified files."""
        path = self.ARCHITECTURE_REFS / "technical-assessment-guide.md"
        assert path.exists(), "Technical assessment guide missing"
        content = path.read_text()
        assert "complexity-assessment" in content.lower(), \
            "Tech guide should reference unified complexity files"

    def test_feature_decomposition_exists(self):
        """New: feature-decomposition.md must exist (merged from two sources)."""
        path = self.ARCHITECTURE_REFS / "feature-decomposition.md"
        assert path.exists(), "Merged feature-decomposition.md missing"
        assert path.stat().st_size > 8000, "Feature decomposition file appears empty"

    def test_epic_decomposition_workflow_deleted(self):
        """Should NOT exist: epic-decomposition-workflow.md (merged into feature-decomposition.md)."""
        path = self.ARCHITECTURE_REFS / "epic-decomposition-workflow.md"
        assert not path.exists(), \
            "epic-decomposition-workflow.md should be deleted (content merged)"

    def test_feature_decomposition_patterns_deleted(self):
        """Should NOT exist: feature-decomposition-patterns.md (merged into feature-decomposition.md)."""
        path = self.ARCHITECTURE_REFS / "feature-decomposition-patterns.md"
        assert not path.exists(), \
            "feature-decomposition-patterns.md should be deleted (content merged)"

    def test_merged_file_contains_process_from_epic_workflow(self):
        """Verify feature-decomposition.md contains process content from epic workflow."""
        merged_path = self.ARCHITECTURE_REFS / "feature-decomposition.md"
        content = merged_path.read_text()

        # Look for process-related keywords from epic workflow
        assert "process" in content.lower() or "step" in content.lower() or \
               "identify" in content.lower() or "decompos" in content.lower(), \
            "Merged file must contain decomposition process"

    def test_merged_file_contains_domain_patterns(self):
        """Verify feature-decomposition.md contains domain pattern content."""
        merged_path = self.ARCHITECTURE_REFS / "feature-decomposition.md"
        content = merged_path.read_text()

        # Look for domain keywords
        assert "domain" in content.lower() or "pattern" in content.lower() or \
               "e-commerce" in content.lower() or "saas" in content.lower(), \
            "Merged file must contain domain patterns"


class TestBackwardCompatibilityMapping:
    """Verify legacy scale mapping is present and correct."""

    ARCHITECTURE_REFS = Path("src/claude/skills/devforgeai-architecture/references")

    def test_mapping_table_for_old_010_scale(self):
        """Matrix must contain mapping from old 0-10 scale to unified scale."""
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        # Look for mapping table or mapping section
        assert "mapping" in matrix.lower() or "legacy" in matrix.lower() or \
               "0-10" in matrix, \
            "Matrix must document legacy 0-10 scale mapping"

    def test_mapping_table_for_old_060_tiers(self):
        """Matrix must contain mapping from old 0-60 tier labels."""
        matrix = (self.ARCHITECTURE_REFS / "complexity-assessment-matrix.md").read_text()

        # Old tier names from ideation scale
        legacy_tiers = ["Simple", "Moderate", "Complex", "Enterprise"]
        found_legacy = sum(1 for tier in legacy_tiers if tier in matrix)

        assert found_legacy >= 2, \
            "Matrix should reference legacy tier names for backward compatibility"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
