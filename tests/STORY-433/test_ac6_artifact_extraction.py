"""
Test: AC#6 - Artifact Generation Epic Sections Extracted
Story: STORY-433
Generated: 2026-02-17

Validates that artifact-generation.md is properly split: epic sections
migrated to architecture, requirements sections remain in ideation.

These tests FAIL initially (TDD Red phase) because section extraction
has not been performed yet.
"""

from pathlib import Path

import pytest

# --- Constants (computed from file location) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IDEATION_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-ideation" / "references"
ARCHITECTURE_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-architecture" / "references"

SECTION_EXTRACTION_FILE = "artifact-generation.md"

# Epic-related section headers that should be migrated to architecture
EPIC_SECTION_HEADERS = [
    "## Step 6.1: Generate Epic Document(s)",
    "## Load Constitutional Epic Template",
    "## Integration with Phase 4 Decomposition",
    "## Directory Structure Requirements",
    "## Epic Numbering Convention",
    "## Epic Status Field",
]

# Requirements-related section headers that should REMAIN in ideation
REQUIREMENTS_SECTION_HEADERS = [
    "## Step 6.2: Generate Requirements Specification (Optional)",
    "## Step 6.3: Transition to Architecture Skill",
    "## Common Issues and Recovery",
    "## Output from Steps 6.1-6.3",
]


class TestAC6ArtifactExtraction:
    """AC#6: artifact-generation.md epic sections extracted to architecture."""

    # --- Epic Sections in Architecture ---

    def test_should_have_artifact_generation_in_architecture_when_extraction_complete(
        self, architecture_refs_dir
    ):
        """Verify artifact-generation.md exists in architecture with epic content."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), (
            f"artifact-generation.md not found at {target}. "
            "Epic sections must be extracted to architecture."
        )

    def test_should_contain_epic_template_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Load Constitutional Epic Template'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Load Constitutional Epic Template" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Load Constitutional Epic Template' section. "
            "Epic sections must be present in architecture."
        )

    def test_should_contain_generate_epic_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Step 6.1: Generate Epic Document(s)'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Step 6.1: Generate Epic Document(s)" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Step 6.1: Generate Epic Document(s)' section."
        )

    def test_should_contain_epic_numbering_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Epic Numbering Convention'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Epic Numbering Convention" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Epic Numbering Convention' section."
        )

    def test_should_contain_epic_status_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Epic Status Field'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Epic Status Field" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Epic Status Field' section."
        )

    def test_should_contain_directory_structure_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Directory Structure Requirements'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Directory Structure Requirements" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Directory Structure Requirements' section."
        )

    def test_should_contain_phase4_decomposition_section_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy contains 'Integration with Phase 4 Decomposition'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        assert "## Integration with Phase 4 Decomposition" in content, (
            "Architecture's artifact-generation.md missing "
            "'## Integration with Phase 4 Decomposition' section."
        )

    # --- Requirements Sections Remain in Ideation ---

    def test_should_keep_artifact_generation_in_ideation_when_extraction_complete(
        self, ideation_refs_dir
    ):
        """Verify artifact-generation.md still exists in ideation with requirements content.

        BR-003: Requirements generation sections must remain in ideation.
        The file is not fully removed -- only epic sections are extracted.
        """
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        assert source.exists(), (
            f"artifact-generation.md was removed from ideation at {source}. "
            "Only epic sections should be extracted; requirements sections "
            "must remain in ideation."
        )

    def test_should_contain_requirements_specification_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy retains 'Step 6.2: Generate Requirements Specification'."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        assert source.exists(), f"Source file does not exist: {source}"

        content = source.read_text(encoding="utf-8")
        assert "## Step 6.2: Generate Requirements Specification" in content, (
            "Ideation's artifact-generation.md missing "
            "'## Step 6.2: Generate Requirements Specification' section. "
            "Requirements sections must remain in ideation (BR-003)."
        )

    def test_should_contain_transition_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy retains 'Step 6.3: Transition to Architecture Skill'."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        assert source.exists(), f"Source file does not exist: {source}"

        content = source.read_text(encoding="utf-8")
        assert "## Step 6.3: Transition to Architecture Skill" in content, (
            "Ideation's artifact-generation.md missing "
            "'## Step 6.3: Transition to Architecture Skill' section. "
            "Requirements sections must remain in ideation (BR-003)."
        )

    def test_should_contain_common_issues_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy retains 'Common Issues and Recovery'."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        assert source.exists(), f"Source file does not exist: {source}"

        content = source.read_text(encoding="utf-8")
        assert "## Common Issues and Recovery" in content, (
            "Ideation's artifact-generation.md missing "
            "'## Common Issues and Recovery' section."
        )

    # --- Epic Sections NOT in Ideation (Post-Extraction) ---

    def test_should_not_contain_epic_template_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy no longer has 'Load Constitutional Epic Template'.

        After extraction, epic sections should be removed from ideation.
        """
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        if not source.exists():
            pytest.skip("Source file already removed (whole-file migration path).")

        content = source.read_text(encoding="utf-8")
        assert "## Load Constitutional Epic Template" not in content, (
            "Ideation's artifact-generation.md still contains "
            "'## Load Constitutional Epic Template'. "
            "Epic sections must be extracted from ideation."
        )

    def test_should_not_contain_generate_epic_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy no longer has 'Step 6.1: Generate Epic Document(s)'."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        if not source.exists():
            pytest.skip("Source file already removed.")

        content = source.read_text(encoding="utf-8")
        assert "## Step 6.1: Generate Epic Document(s)" not in content, (
            "Ideation's artifact-generation.md still contains "
            "'## Step 6.1: Generate Epic Document(s)'. "
            "Epic sections must be extracted from ideation."
        )

    def test_should_not_contain_epic_numbering_section_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy no longer has 'Epic Numbering Convention'."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        if not source.exists():
            pytest.skip("Source file already removed.")

        content = source.read_text(encoding="utf-8")
        assert "## Epic Numbering Convention" not in content, (
            "Ideation's artifact-generation.md still contains "
            "'## Epic Numbering Convention'. "
            "Epic sections must be extracted from ideation."
        )

    # --- Requirements Sections NOT in Architecture ---

    def test_should_not_contain_requirements_specification_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy does NOT have requirements sections."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        if not target.exists():
            pytest.skip("Target file does not exist yet.")

        content = target.read_text(encoding="utf-8")
        assert "## Step 6.2: Generate Requirements Specification" not in content, (
            "Architecture's artifact-generation.md contains "
            "'## Step 6.2: Generate Requirements Specification'. "
            "Requirements sections must stay in ideation, not architecture."
        )

    def test_should_not_contain_common_issues_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy does NOT have 'Common Issues and Recovery'."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        if not target.exists():
            pytest.skip("Target file does not exist yet.")

        content = target.read_text(encoding="utf-8")
        assert "## Common Issues and Recovery" not in content, (
            "Architecture's artifact-generation.md contains "
            "'## Common Issues and Recovery'. "
            "This section should remain in ideation only."
        )

    # --- Line Count Validation ---

    def test_should_have_approximately_350_lines_of_epic_content_in_architecture(
        self, architecture_refs_dir
    ):
        """Verify architecture copy has ~350 lines of epic content.

        Story specification says epic sections are approximately 350 lines.
        Allow variance for extraction differences.
        """
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        assert target.exists(), f"Target file does not exist: {target}"

        content = target.read_text(encoding="utf-8")
        line_count = len(content.splitlines())

        assert 190 <= line_count <= 500, (
            f"Architecture's artifact-generation.md has {line_count} lines. "
            f"Expected approximately 200-350 lines (190-500 range). "
            f"Epic sections may be incorrectly extracted."
        )

    # --- Content Coherence ---

    def test_should_have_valid_markdown_headers_in_architecture_when_extracted(
        self, architecture_refs_dir
    ):
        """Verify architecture copy has valid markdown structure."""
        target = architecture_refs_dir / SECTION_EXTRACTION_FILE
        if not target.exists():
            pytest.fail(f"Target file does not exist: {target}")

        content = target.read_text(encoding="utf-8")
        lines = content.splitlines()

        headers = [line for line in lines if line.startswith("# ") or line.startswith("## ")]
        assert len(headers) >= 1, (
            "Architecture's artifact-generation.md has no markdown headers. "
            "Extracted content must maintain valid markdown structure."
        )

    def test_should_have_valid_markdown_headers_in_ideation_when_extracted(
        self, ideation_refs_dir
    ):
        """Verify ideation copy still has valid markdown structure."""
        source = ideation_refs_dir / SECTION_EXTRACTION_FILE
        if not source.exists():
            pytest.skip("Source file already removed.")

        content = source.read_text(encoding="utf-8")
        lines = content.splitlines()

        headers = [line for line in lines if line.startswith("# ") or line.startswith("## ")]
        assert len(headers) >= 1, (
            "Ideation's artifact-generation.md has no markdown headers after extraction. "
            "Requirements sections must maintain valid markdown structure."
        )
