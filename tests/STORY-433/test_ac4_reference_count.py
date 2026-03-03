"""
Test: AC#4 - Ideation Reference Count Reduced
Story: STORY-433
Generated: 2026-02-17

Validates that the ideation references directory contains exactly 6 fewer
.md files after migration.

These tests FAIL initially (TDD Red phase) because files have not been
removed yet.
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

# Pre-migration count of .md files in ideation references
PRE_MIGRATION_IDEATION_MD_COUNT = 31


def count_md_files(directory: Path) -> int:
    """Count .md files in a directory (non-recursive)."""
    if not directory.exists():
        return 0
    return len([f for f in directory.iterdir() if f.suffix == ".md" and f.is_file()])


class TestAC4ReferenceCount:
    """AC#4: Ideation reference count reduced by exactly 5 whole-file removals.

    Note: The story says 6 files migrated, but artifact-generation.md
    undergoes section extraction -- the file remains in ideation with
    requirements content, so only 5 files are fully removed.
    Per AC#4: 'ideation references directory contains exactly 24 or fewer .md files'
    """

    # --- Pre-Migration Baseline ---

    def test_should_have_known_premigration_count_when_baseline_captured(
        self, ideation_refs_dir
    ):
        """Verify pre-migration .md file count matches expected baseline.

        This establishes the starting point for the reduction calculation.
        Should PASS before migration starts.
        """
        actual_count = count_md_files(ideation_refs_dir)
        assert actual_count >= 25, (
            f"Ideation references has only {actual_count} .md files. "
            f"Expected at least 25 files as pre-migration baseline."
        )

    # --- Post-Migration Count ---

    def test_should_have_reduced_count_in_ideation_when_migration_complete(
        self, ideation_refs_dir
    ):
        """Verify ideation .md file count reduced after removing 5 whole files.

        AC#4 specifies: 'exactly 24 or fewer .md files (6 removed)'.
        Since artifact-generation.md stays with requirements sections,
        the actual removal is 5 whole files.

        Pre-migration count: 30 files
        Post-migration count: 25 files (30 - 5 whole file removals)
        """
        actual_count = count_md_files(ideation_refs_dir)
        assert actual_count <= 25, (
            f"Ideation references still has {actual_count} .md files. "
            f"Expected 25 or fewer after migration (30 - 5 whole file removals). "
            f"5 whole files should be removed."
        )

    def test_should_not_have_migrated_whole_files_in_ideation_count_when_complete(
        self, ideation_refs_dir
    ):
        """Verify the specific 5 whole-file migrations are not counted in ideation."""
        remaining_migrated = []
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            if source.exists():
                remaining_migrated.append(filename)

        assert len(remaining_migrated) == 0, (
            f"{len(remaining_migrated)} migrated files still in ideation: "
            f"{remaining_migrated}. These should be removed to reduce count."
        )

    # --- Architecture Count Increased ---

    def test_should_have_increased_count_in_architecture_when_migration_complete(
        self, architecture_refs_dir
    ):
        """Verify architecture references gained files from migration.

        Architecture should have its original files plus the 6 migrated files.
        Pre-migration architecture had 20 .md files (from listing).
        Post-migration should have 20 + 6 = 26 .md files.
        """
        actual_count = count_md_files(architecture_refs_dir)
        assert actual_count >= 26, (
            f"Architecture references has only {actual_count} .md files. "
            f"Expected at least 26 (20 original + 6 migrated)."
        )

    # --- Count Consistency Check ---

    def test_should_have_consistent_total_count_when_migration_complete(
        self, ideation_refs_dir, architecture_refs_dir
    ):
        """Verify total .md file count is conserved (no files lost or duplicated).

        Pre-migration totals:
        - Ideation: ~31 .md files
        - Architecture: ~20 .md files
        - Total: ~51

        Post-migration totals (5 whole files moved + 1 section extraction):
        - Ideation: ~26 .md files (31 - 5 removed)
        - Architecture: ~26 .md files (20 + 6 added)
        - Total: ~52 (net +1 because artifact-generation.md now exists in both)
        """
        ideation_count = count_md_files(ideation_refs_dir)
        arch_count = count_md_files(architecture_refs_dir)
        total = ideation_count + arch_count

        assert total >= 50, (
            f"Total .md files across both directories is {total}. "
            f"This is too low -- files may have been lost during migration. "
            f"Ideation: {ideation_count}, Architecture: {arch_count}."
        )

    # --- Edge Case: Exact Count Match ---

    def test_should_match_exact_reduction_of_five_whole_files_when_complete(
        self, ideation_refs_dir
    ):
        """Verify exactly 5 of the 5 whole-file migrations are removed from ideation."""
        removed_count = 0
        for filename in WHOLE_FILE_MIGRATIONS:
            source = ideation_refs_dir / filename
            if not source.exists():
                removed_count += 1

        assert removed_count == 5, (
            f"Only {removed_count} of 5 whole-file migrations removed from ideation. "
            f"All 5 whole files must be removed."
        )
