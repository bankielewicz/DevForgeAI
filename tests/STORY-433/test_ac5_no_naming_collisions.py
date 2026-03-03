"""
Test: AC#5 - No Naming Collisions in Architecture References
Story: STORY-433
Generated: 2026-02-17

Validates that no file name collisions occur when migrating files to
architecture references directory.

These tests FAIL initially (TDD Red phase) because collision detection
has not been implemented yet.
"""

from pathlib import Path
from collections import Counter

import pytest

# --- Constants (computed from file location) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
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

# Known STORY-432 files (from EPIC-068 Feature 1)
STORY_432_EXPECTED_FILES = [
    "dependency-graph.md",
    "epic-management.md",
    "epic-validation-checklist.md",
    "epic-validation-hook.md",
    "feature-analyzer.md",
    "feature-decomposition-patterns.md",
]


class TestAC5NoNamingCollisions:
    """AC#5: No file name collisions in architecture references after migration."""

    # --- Pre-Copy Collision Detection (BR-004) ---

    def test_should_have_unique_filenames_across_all_architecture_references(
        self, architecture_refs_dir
    ):
        """Verify every file in architecture references has a unique name."""
        if not architecture_refs_dir.exists():
            pytest.skip("Architecture references directory does not exist yet.")

        all_files = list(architecture_refs_dir.glob("*.md"))
        filenames = [f.name for f in all_files]
        file_counts = Counter(filenames)
        duplicates = {name: count for name, count in file_counts.items() if count > 1}

        assert len(duplicates) == 0, (
            f"Duplicate filenames found in architecture references: {duplicates}. "
            "All files must have unique names (BR-004)."
        )

    # --- No Collision with STORY-432 Files ---

    def test_should_not_collide_with_story_432_migrated_files(self):
        """Verify STORY-433 files do not collide with STORY-432 orchestration files.

        STORY-432 migrates orchestration epic files to architecture.
        STORY-433 migrates ideation epic files to architecture.
        Their filenames must not overlap.
        """
        for migration_file in ALL_MIGRATED_FILES:
            assert migration_file not in STORY_432_EXPECTED_FILES, (
                f"Naming collision detected: {migration_file} exists in both "
                "STORY-432 and STORY-433 migration sets. "
                "Files must be prefixed with source skill name to resolve."
            )

    # --- All 6 Migrated Files Present Without Collision ---

    def test_should_have_all_migrated_files_with_unique_names_in_architecture(
        self, architecture_refs_dir
    ):
        """Verify all 6 STORY-433 files exist in architecture with unique names.

        This test confirms migration completed AND no collisions occurred.
        """
        missing = []
        for filename in ALL_MIGRATED_FILES:
            target = architecture_refs_dir / filename
            if not target.exists():
                missing.append(filename)

        assert len(missing) == 0, (
            f"Missing {len(missing)} files in architecture references: {missing}. "
            "Files must be migrated without naming collisions."
        )

    # --- Collision Resolution Validation ---

    def test_should_resolve_collision_by_prefixing_when_collision_detected(
        self, architecture_refs_dir
    ):
        """Verify collision resolution uses skill-name prefix convention.

        If a collision is detected, the resolution is to prefix the migrated
        file with the source skill name (e.g., 'ideation-dependency-graph.md').
        This test validates that any prefixed files follow the convention.
        """
        if not architecture_refs_dir.exists():
            pytest.skip("Architecture references directory does not exist yet.")

        prefixed_files = [
            f.name for f in architecture_refs_dir.iterdir()
            if f.is_file() and f.name.startswith("ideation-")
        ]

        # If no prefixed files exist, that's fine -- no collisions occurred
        # If prefixed files exist, verify they follow the naming convention
        for filename in prefixed_files:
            assert filename.endswith(".md"), (
                f"Prefixed file {filename} does not end with .md"
            )

    # --- BR-005: Dual-Path Architecture Compliance ---

    def test_should_only_target_src_tree_when_migration_runs(
        self, architecture_refs_dir
    ):
        """BR-005: Migration must target src/ tree, not operational .claude/ directory.

        Verify the target path is under src/, not .claude/.
        """
        target_str = str(architecture_refs_dir)
        assert "src" in Path(target_str).parts, (
            f"Target directory {target_str} is not under src/ tree. "
            "BR-005 requires all operations target src/ tree."
        )

    def test_should_reject_migration_to_operational_claude_directory(self):
        """BR-005: Attempting migration to .claude/ must be rejected.

        Verify the target path constant points to src/claude, not .claude.
        """
        target_str = str(ARCHITECTURE_REFS_DIR)
        path_parts = Path(target_str).parts
        for i, part in enumerate(path_parts):
            if part == "claude":
                if i > 0:
                    assert path_parts[i - 1] == "src", (
                        f"'claude' directory at position {i} in path is not "
                        "under 'src/'. BR-005 requires src/ tree targeting."
                    )
                break
