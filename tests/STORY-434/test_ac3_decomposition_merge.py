"""
Test: AC#3 - Feature Decomposition Content Merged
Story: STORY-434
Generated: 2026-02-17

Validates that:
- Process sections merged from epic-decomposition-workflow.md
- Domain patterns preserved from feature-decomposition-patterns.md
- Single authoritative feature-decomposition.md created
- Redundant source files removed after merge
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCH_REFS = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
)
MERGED_FILE = os.path.join(ARCH_REFS, "feature-decomposition.md")
OLD_EPIC_DECOMP = os.path.join(ARCH_REFS, "epic-decomposition-workflow.md")
OLD_FEATURE_PATTERNS = os.path.join(ARCH_REFS, "feature-decomposition-patterns.md")


@pytest.fixture
def merged_content():
    """Read the merged feature decomposition file."""
    with open(MERGED_FILE, "r") as f:
        return f.read()


# === Merged File Existence ===

class TestMergedFileExists:
    """Verify the single authoritative file exists."""

    def test_should_exist_when_merge_complete(self):
        # Arrange & Act & Assert
        assert os.path.isfile(MERGED_FILE), (
            f"Merged file not found: {MERGED_FILE}"
        )


# === Process Content Merged ===

class TestProcessContentMerged:
    """Verify process sections from epic-decomposition-workflow.md are present."""

    def test_should_contain_process_section_when_merged(self, merged_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:process|workflow|step[s]?\s*\d|procedure)",
            merged_content,
        ), "Merged file missing process/workflow section from epic-decomposition-workflow.md"

    def test_should_contain_epic_identification_when_merged(self, merged_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)epic\s+identification", merged_content
        ), "Merged file missing 'epic identification' content from source"

    def test_should_contain_feature_grouping_when_merged(self, merged_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)feature\s+group", merged_content
        ), "Merged file missing 'feature grouping' content from source"


# === Domain Patterns Preserved ===

class TestDomainPatternsPreserved:
    """Verify domain patterns from feature-decomposition-patterns.md are present."""

    EXPECTED_DOMAIN_PATTERNS = ["e-commerce", "SaaS"]

    @pytest.mark.parametrize("domain", EXPECTED_DOMAIN_PATTERNS)
    def test_should_contain_domain_pattern_when_merged(self, merged_content, domain):
        # Arrange & Act & Assert
        assert re.search(
            rf"(?i){re.escape(domain)}", merged_content
        ), f"Merged file missing domain pattern: {domain}"

    def test_should_contain_domain_patterns_section_when_merged(self, merged_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:domain\s+pattern|pattern)", merged_content
        ), "Merged file missing domain patterns section"

    def test_should_contain_decomposition_principles_when_merged(self, merged_content):
        # Arrange & Act & Assert
        assert re.search(
            r"(?i)(?:decomposition\s+principle|sizing|breakdown)", merged_content
        ), "Merged file missing decomposition principles content"


# === Redundant Files Removed ===

class TestRedundantFilesRemoved:
    """Verify old source files no longer exist after merge."""

    def test_should_not_have_epic_decomposition_workflow_when_merged(self):
        # Arrange & Act & Assert
        assert not os.path.isfile(OLD_EPIC_DECOMP), (
            f"Redundant file still exists: {OLD_EPIC_DECOMP}"
        )

    def test_should_not_have_feature_decomposition_patterns_when_merged(self):
        # Arrange & Act & Assert
        assert not os.path.isfile(OLD_FEATURE_PATTERNS), (
            f"Redundant file still exists: {OLD_FEATURE_PATTERNS}"
        )


# === Line Count Limit (BR-005) ===

class TestLineLimitCompliance:
    """Verify merged file stays under 1000 lines."""

    def test_should_be_under_1000_lines_when_merged(self, merged_content):
        # Arrange
        line_count = len(merged_content.splitlines())
        # Act & Assert
        assert line_count < 1000, (
            f"Merged file has {line_count} lines, exceeds 1000-line limit"
        )
