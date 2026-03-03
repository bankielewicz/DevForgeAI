"""
Test: AC#1 - All Seven Reference Files Migrated to Architecture
Story: STORY-432
Generated: 2026-02-17

Verifies that all 7 epic-related reference files exist in the architecture
skill's references/ directory after migration.

Given: The orchestration skill contains 7 epic-related reference files
When: The migration is completed
Then: All 7 files exist at src/claude/skills/devforgeai-architecture/references/
"""
import os
import pytest

from conftest import ARCHITECTURE_REFERENCES_DIR, REFERENCE_FILES


class TestAC1ReferenceFileMigration:
    """AC#1: All seven reference files migrated to architecture."""

    # --- Helper method ---

    def _verify_file_exists_in_architecture(self, filename: str) -> None:
        """Helper: Verify a file exists in architecture references directory.

        Args:
            filename: Name of the file to verify.

        Raises:
            AssertionError: If file does not exist at target location.
        """
        target_path = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
        assert os.path.isfile(target_path), (
            f"{filename} not found at {target_path}. "
            "File must be migrated from orchestration to architecture."
        )

    # --- Parameterized individual file existence tests ---

    def test_should_have_epic_management_in_architecture_when_migration_complete(self):
        """Verify epic-management.md exists in architecture references."""
        self._verify_file_exists_in_architecture("epic-management.md")

    def test_should_have_feature_decomposition_patterns_in_architecture_when_migration_complete(self):
        """Verify feature-decomposition-patterns.md exists in architecture references."""
        self._verify_file_exists_in_architecture("feature-decomposition-patterns.md")

    def test_should_have_feature_analyzer_in_architecture_when_migration_complete(self):
        """Verify feature-analyzer.md exists in architecture references."""
        self._verify_file_exists_in_architecture("feature-analyzer.md")

    def test_should_have_dependency_graph_in_architecture_when_migration_complete(self):
        """Verify dependency-graph.md exists in architecture references."""
        self._verify_file_exists_in_architecture("dependency-graph.md")

    def test_should_have_technical_assessment_guide_in_architecture_when_migration_complete(self):
        """Verify technical-assessment-guide.md exists in architecture references."""
        self._verify_file_exists_in_architecture("technical-assessment-guide.md")

    def test_should_have_epic_validation_checklist_in_architecture_when_migration_complete(self):
        """Verify epic-validation-checklist.md exists in architecture references."""
        self._verify_file_exists_in_architecture("epic-validation-checklist.md")

    def test_should_have_epic_validation_hook_in_architecture_when_migration_complete(self):
        """Verify epic-validation-hook.md exists in architecture references."""
        self._verify_file_exists_in_architecture("epic-validation-hook.md")

    # --- Aggregate test ---

    def test_should_have_all_seven_reference_files_in_architecture_when_migration_complete(self):
        """Verify all 7 reference files exist in architecture references directory."""
        missing_files = []
        for filename in REFERENCE_FILES:
            target_path = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
            if not os.path.isfile(target_path):
                missing_files.append(filename)

        assert len(missing_files) == 0, (
            f"{len(missing_files)} of 7 reference files missing from architecture: "
            f"{missing_files}"
        )

    def test_should_have_exactly_seven_migrated_reference_files_when_counted(self):
        """Verify the count of migrated reference files is exactly 7."""
        found_count = 0
        for filename in REFERENCE_FILES:
            target_path = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
            if os.path.isfile(target_path):
                found_count += 1

        assert found_count == 7, (
            f"Expected 7 migrated reference files in architecture, found {found_count}. "
            f"Missing: {7 - found_count} file(s)."
        )

    # --- Non-empty content test ---

    def test_should_have_nonempty_reference_files_in_architecture_when_migration_complete(self):
        """Verify all migrated reference files have non-zero byte size."""
        empty_files = []
        for filename in REFERENCE_FILES:
            target_path = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
            if os.path.isfile(target_path) and os.path.getsize(target_path) == 0:
                empty_files.append(filename)

        assert len(empty_files) == 0, (
            f"The following migrated reference files are empty (0 bytes): {empty_files}. "
            "Migration must preserve file content."
        )
