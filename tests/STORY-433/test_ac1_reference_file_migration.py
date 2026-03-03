"""
Test: AC#1 - All Six Reference Files Migrated to Architecture
Story: STORY-433
Generated: 2026-02-17

Validates that all 6 epic-related reference files exist in the architecture
skill's references directory after migration.

These tests FAIL initially (TDD Red phase) because files have not been
migrated yet.
"""

from pathlib import Path

import pytest

# --- Constants (computed from file location) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IDEATION_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-ideation" / "references"
ARCHITECTURE_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-architecture" / "references"

WHOLE_FILE_MIGRATIONS = [
    "epic-decomposition-workflow.md",
    "feasibility-analysis-workflow.md",
    "feasibility-analysis-framework.md",
    "complexity-assessment-workflow.md",
    "complexity-assessment-matrix.md",
]
SECTION_EXTRACTION_FILE = "artifact-generation.md"
ALL_MIGRATED_FILES = WHOLE_FILE_MIGRATIONS + [SECTION_EXTRACTION_FILE]


class TestAC1ReferenceFileMigration:
    """AC#1: All six reference files exist in architecture references."""

    # --- Happy Path Tests ---

    def test_should_have_epic_decomposition_workflow_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify epic-decomposition-workflow.md exists in architecture references."""
        target = architecture_refs_dir / "epic-decomposition-workflow.md"
        assert target.exists(), (
            f"epic-decomposition-workflow.md not found at {target}. "
            "File must be migrated from ideation to architecture."
        )

    def test_should_have_feasibility_analysis_workflow_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify feasibility-analysis-workflow.md exists in architecture references."""
        target = architecture_refs_dir / "feasibility-analysis-workflow.md"
        assert target.exists(), (
            f"feasibility-analysis-workflow.md not found at {target}. "
            "File must be migrated from ideation to architecture."
        )

    def test_should_have_feasibility_analysis_framework_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify feasibility-analysis-framework.md exists in architecture references."""
        target = architecture_refs_dir / "feasibility-analysis-framework.md"
        assert target.exists(), (
            f"feasibility-analysis-framework.md not found at {target}. "
            "File must be migrated from ideation to architecture."
        )

    def test_should_have_complexity_assessment_workflow_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify complexity-assessment-workflow.md exists in architecture references."""
        target = architecture_refs_dir / "complexity-assessment-workflow.md"
        assert target.exists(), (
            f"complexity-assessment-workflow.md not found at {target}. "
            "File must be migrated from ideation to architecture."
        )

    def test_should_have_complexity_assessment_matrix_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify complexity-assessment-matrix.md exists in architecture references."""
        target = architecture_refs_dir / "complexity-assessment-matrix.md"
        assert target.exists(), (
            f"complexity-assessment-matrix.md not found at {target}. "
            "File must be migrated from ideation to architecture."
        )

    def test_should_have_artifact_generation_epic_content_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify artifact-generation.md (epic sections) exists in architecture references."""
        target = architecture_refs_dir / "artifact-generation.md"
        assert target.exists(), (
            f"artifact-generation.md not found at {target}. "
            "Epic sections must be extracted and migrated to architecture."
        )

    # --- Aggregate Tests ---

    def test_should_have_all_six_files_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify all 6 migrated files exist in architecture references directory."""
        missing_files = []
        for filename in ALL_MIGRATED_FILES:
            target = architecture_refs_dir / filename
            if not target.exists():
                missing_files.append(filename)

        assert len(missing_files) == 0, (
            f"Missing {len(missing_files)} files in architecture references: "
            f"{missing_files}. All 6 files must be migrated."
        )

    def test_should_have_nonempty_files_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify migrated files are not empty (have actual content)."""
        empty_files = []
        for filename in ALL_MIGRATED_FILES:
            target = architecture_refs_dir / filename
            if target.exists() and target.stat().st_size == 0:
                empty_files.append(filename)

        assert len(empty_files) == 0, (
            f"Empty files found in architecture references: {empty_files}. "
            "Migrated files must contain content."
        )

    # --- Source Directory Validation ---

    @pytest.mark.skip(reason="Pre-condition test - expected to fail after migration is complete")
    def test_should_have_source_files_available_before_migration(
        self, ideation_refs_dir
    ):
        """Verify source files exist in ideation references (pre-migration baseline).

        This test validates the precondition: source files must exist before migration.
        It should PASS before migration starts, but FAIL after migration is complete
        (because files have been moved to architecture).
        """
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            assert source.exists(), (
                f"Source file {filename} not found at {source}. "
                "Cannot migrate file that does not exist in source."
            )

    # --- Target Directory Exists ---

    def test_should_have_architecture_references_directory_when_migration_runs(
        self, architecture_refs_dir
    ):
        """Verify architecture references directory exists."""
        assert architecture_refs_dir.exists(), (
            f"Architecture references directory not found at {architecture_refs_dir}. "
            "Target directory must exist before migration."
        )
        assert architecture_refs_dir.is_dir(), (
            f"{architecture_refs_dir} exists but is not a directory."
        )
