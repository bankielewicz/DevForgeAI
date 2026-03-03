"""
Test: AC#2 - Source Files Removed from Ideation
Story: STORY-433
Generated: 2026-02-17

Validates that none of the 6 migrated files remain in the ideation skill's
references directory after migration cleanup.

These tests FAIL initially (TDD Red phase) because source files have not
been removed yet.
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

NON_MIGRATED_FILES = [
    "discovery-workflow.md",
    "requirements-elicitation-workflow.md",
    "requirements-elicitation-guide.md",
    "self-validation-workflow.md",
    "user-interaction-patterns.md",
    "error-handling.md",
    "output-templates.md",
    "validation-checklists.md",
    "domain-specific-patterns.md",
    "completion-handoff.md",
]


class TestAC2SourceCleanup:
    """AC#2: Source files removed from ideation references after migration."""

    # --- Individual File Removal Tests ---

    def test_should_not_have_epic_decomposition_workflow_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify epic-decomposition-workflow.md removed from ideation."""
        source = ideation_refs_dir / "epic-decomposition-workflow.md"
        assert not source.exists(), (
            f"epic-decomposition-workflow.md still exists at {source}. "
            "File must be removed from ideation after successful migration."
        )

    def test_should_not_have_feasibility_analysis_workflow_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify feasibility-analysis-workflow.md removed from ideation."""
        source = ideation_refs_dir / "feasibility-analysis-workflow.md"
        assert not source.exists(), (
            f"feasibility-analysis-workflow.md still exists at {source}. "
            "File must be removed from ideation after successful migration."
        )

    def test_should_not_have_feasibility_analysis_framework_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify feasibility-analysis-framework.md removed from ideation."""
        source = ideation_refs_dir / "feasibility-analysis-framework.md"
        assert not source.exists(), (
            f"feasibility-analysis-framework.md still exists at {source}. "
            "File must be removed from ideation after successful migration."
        )

    def test_should_not_have_complexity_assessment_workflow_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify complexity-assessment-workflow.md removed from ideation."""
        source = ideation_refs_dir / "complexity-assessment-workflow.md"
        assert not source.exists(), (
            f"complexity-assessment-workflow.md still exists at {source}. "
            "File must be removed from ideation after successful migration."
        )

    def test_should_not_have_complexity_assessment_matrix_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify complexity-assessment-matrix.md removed from ideation."""
        source = ideation_refs_dir / "complexity-assessment-matrix.md"
        assert not source.exists(), (
            f"complexity-assessment-matrix.md still exists at {source}. "
            "File must be removed from ideation after successful migration."
        )

    # --- Aggregate Removal Test ---

    def test_should_not_have_any_migrated_files_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify none of the 5 whole-file migrations remain in ideation references."""
        remaining_files = []
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            if source.exists():
                remaining_files.append(filename)

        assert len(remaining_files) == 0, (
            f"{len(remaining_files)} migrated files still in ideation: "
            f"{remaining_files}. All whole-file migrations must be removed."
        )

    # --- BR-002: Source removed only after target verified ---

    def test_should_not_remove_source_before_target_exists_when_br002_enforced(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """BR-002: Source files must only be removed after target is verified.

        This test checks the invariant: if a source file is removed,
        the corresponding target file must exist. This prevents data loss.
        """
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            target = architecture_refs_dir / filename

            if not source.exists():
                # Source was removed -- target MUST exist
                assert target.exists(), (
                    f"BR-002 VIOLATION: {filename} removed from ideation but "
                    f"not found in architecture. Source must only be removed "
                    f"after successful target verification."
                )

    # --- Ideation directory still exists (other files remain) ---

    def test_should_preserve_ideation_references_directory_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify ideation references directory still exists after cleanup.

        Only the 6 migrated files are removed; other reference files
        (discovery-workflow.md, requirements-elicitation-workflow.md, etc.)
        must remain.
        """
        assert ideation_refs_dir.exists(), (
            f"Ideation references directory was deleted at {ideation_refs_dir}. "
            "Only migrated files should be removed, not the entire directory."
        )

    def test_should_preserve_non_migrated_files_in_ideation_when_cleanup_complete(
        self, ideation_refs_dir
    ):
        """Verify non-migrated files still exist in ideation references.

        Files like discovery-workflow.md and requirements-elicitation-workflow.md
        are PM-scope and must remain in ideation.
        """
        for filename in NON_MIGRATED_FILES:
            source = ideation_refs_dir / filename
            assert source.exists(), (
                f"Non-migrated file {filename} was incorrectly removed from "
                f"ideation at {source}. Only the 6 migration files should be removed."
            )
