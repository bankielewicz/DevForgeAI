"""
Test: AC#2 - Complexity Assessment Files Consolidated
Story: STORY-434
Generated: 2026-02-17

Validates that:
- complexity-assessment-workflow.md contains unified scoring procedure
- complexity-assessment-matrix.md contains unified rubric
- technical-assessment-guide.md scoring section replaced with pointer
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
TECH_GUIDE_FILE = os.path.join(ARCH_REFS, "technical-assessment-guide.md")


@pytest.fixture
def workflow_content():
    with open(WORKFLOW_FILE, "r") as f:
        return f.read()


@pytest.fixture
def matrix_content():
    with open(MATRIX_FILE, "r") as f:
        return f.read()


@pytest.fixture
def tech_guide_content():
    with open(TECH_GUIDE_FILE, "r") as f:
        return f.read()


# === Workflow Consolidation Tests ===

class TestWorkflowUnifiedProcedure:
    """Verify workflow file contains unified scoring procedure."""

    def test_should_contain_unified_keyword_when_consolidated(self, workflow_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)unified", workflow_content
        ), "Workflow file does not contain 'unified' - not yet consolidated"

    def test_should_contain_scoring_procedure_when_consolidated(self, workflow_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:scoring\s+procedure|assessment\s+procedure|how\s+to\s+score)",
            workflow_content,
        ), "Workflow file missing scoring procedure section"

    def test_should_reference_all_4_dimensions_when_consolidated(self, workflow_content):
        # Arrange
        dimensions = ["Functional", "Technical", "Team", "NFR"]
        # Act
        missing = [d for d in dimensions if not re.search(rf"(?i)\b{d}\b", workflow_content)]
        # Assert
        assert not missing, f"Workflow missing dimensions: {missing}"

    def test_should_reference_5_tier_labels_when_consolidated(self, workflow_content):
        # Arrange
        tiers = ["Trivial", "Low", "Moderate", "High", "Critical"]
        # Act
        missing = [t for t in tiers if not re.search(rf"(?i)\b{t}\b", workflow_content)]
        # Assert
        assert not missing, f"Workflow missing tier labels: {missing}"


# === Matrix Consolidation Tests ===

class TestMatrixUnifiedRubric:
    """Verify matrix file contains unified rubric with examples."""

    def test_should_contain_unified_rubric_when_consolidated(self, matrix_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:unified|rubric)", matrix_content
        ), "Matrix file does not contain unified rubric markers"

    def test_should_contain_scoring_examples_when_consolidated(self, matrix_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:example|sample|scenario)", matrix_content
        ), "Matrix file missing scoring examples"

    def test_should_contain_dimension_breakdowns_when_consolidated(self, matrix_content):
        # Arrange - each dimension should have per-dimension scoring criteria
        # Act & Assert
        assert re.search(
            r"(?i)functional.*\d+", matrix_content
        ), "Matrix missing Functional dimension scoring breakdown"
        assert re.search(
            r"(?i)technical.*\d+", matrix_content
        ), "Matrix missing Technical dimension scoring breakdown"


# === Technical Assessment Guide Pointer Tests ===

class TestTechGuidePointer:
    """Verify technical-assessment-guide.md scoring replaced with pointer."""

    def test_should_not_contain_full_scoring_rubric_when_consolidated(self, tech_guide_content):
        """The guide should no longer have its own full scoring rubric."""
        # Arrange - look for detailed scoring bands (old 0-10 rubric)
        old_rubric_pattern = r"(?i)(?:0\s*[-–]\s*2.*trivial|3\s*[-–]\s*4.*low|5\s*[-–]\s*6.*moderate|7\s*[-–]\s*8.*high|9\s*[-–]\s*10.*critical)"
        # Act
        matches = re.findall(old_rubric_pattern, tech_guide_content)
        # Assert
        assert len(matches) == 0, (
            f"Technical assessment guide still contains old 0-10 scoring rubric ({len(matches)} matches)"
        )

    def test_should_contain_reference_pointer_when_consolidated(self, tech_guide_content):
        """The guide should reference the unified scoring files."""
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:see|refer|reference).*complexity-assessment",
            tech_guide_content,
        ), "Technical assessment guide missing reference pointer to unified files"

    def test_should_reference_unified_files_by_name_when_consolidated(self, tech_guide_content):
        # Arrange & Act & Assert
        assert re.search(
            r"complexity-assessment-(?:workflow|matrix)\.md", tech_guide_content
        ), "Technical assessment guide does not reference unified file names"
