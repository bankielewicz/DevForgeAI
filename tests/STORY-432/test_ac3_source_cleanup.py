"""
Test: AC#3 - Source Files Removed from Orchestration
Story: STORY-432
Generated: 2026-02-17

Verifies that all 8 migrated files (7 references + 1 template) are removed
from the orchestration skill directories after migration.

Given: All 8 files have been copied to architecture
When: The cleanup phase completes
Then: None of the 8 migrated files exist in orchestration skill directories
"""
import os
import pytest

from conftest import (
    ORCHESTRATION_REFERENCES_DIR,
    ORCHESTRATION_TEMPLATES_DIR,
    REFERENCE_FILES,
    TEMPLATE_FILE,
)


class TestAC3SourceCleanup:
    """AC#3: Source files removed from orchestration."""

    # --- Helper method ---

    def _verify_file_removed_from_orchestration(self, filename: str) -> None:
        """Helper: Verify a file is removed from orchestration references directory.

        Args:
            filename: Name of the file to verify.

        Raises:
            AssertionError: If file still exists at source location.
        """
        source_path = os.path.join(ORCHESTRATION_REFERENCES_DIR, filename)
        assert not os.path.exists(source_path), (
            f"{filename} still exists at {source_path}. "
            "File must be removed from orchestration after successful migration."
        )

    # --- Parameterized individual reference file removal tests ---

    def test_should_not_have_epic_management_in_orchestration_when_cleanup_complete(self):
        """Verify epic-management.md is removed from orchestration references."""
        self._verify_file_removed_from_orchestration("epic-management.md")

    def test_should_not_have_feature_decomposition_patterns_in_orchestration_when_cleanup_complete(self):
        """Verify feature-decomposition-patterns.md is removed from orchestration."""
        self._verify_file_removed_from_orchestration("feature-decomposition-patterns.md")

    def test_should_not_have_feature_analyzer_in_orchestration_when_cleanup_complete(self):
        """Verify feature-analyzer.md is removed from orchestration references."""
        self._verify_file_removed_from_orchestration("feature-analyzer.md")

    def test_should_not_have_dependency_graph_in_orchestration_when_cleanup_complete(self):
        """Verify dependency-graph.md is removed from orchestration references."""
        self._verify_file_removed_from_orchestration("dependency-graph.md")

    def test_should_not_have_technical_assessment_guide_in_orchestration_when_cleanup_complete(self):
        """Verify technical-assessment-guide.md is removed from orchestration."""
        self._verify_file_removed_from_orchestration("technical-assessment-guide.md")

    def test_should_not_have_epic_validation_checklist_in_orchestration_when_cleanup_complete(self):
        """Verify epic-validation-checklist.md is removed from orchestration."""
        self._verify_file_removed_from_orchestration("epic-validation-checklist.md")

    def test_should_not_have_epic_validation_hook_in_orchestration_when_cleanup_complete(self):
        """Verify epic-validation-hook.md is removed from orchestration."""
        self._verify_file_removed_from_orchestration("epic-validation-hook.md")

    # --- Template removal test ---

    def test_should_not_have_epic_template_in_orchestration_when_cleanup_complete(self):
        """Verify epic-template.md is removed from orchestration assets/templates/."""
        source_path = os.path.join(ORCHESTRATION_TEMPLATES_DIR, TEMPLATE_FILE)
        assert not os.path.exists(source_path), (
            f"epic-template.md still exists at {source_path}. "
            "Template must be removed from orchestration after successful migration."
        )

    # --- Aggregate tests ---

    def test_should_not_have_any_migrated_reference_files_in_orchestration_when_cleanup_complete(self):
        """Verify none of the 7 reference files remain in orchestration."""
        remaining_files = []
        for filename in REFERENCE_FILES:
            source_path = os.path.join(ORCHESTRATION_REFERENCES_DIR, filename)
            if os.path.exists(source_path):
                remaining_files.append(filename)

        assert len(remaining_files) == 0, (
            f"{len(remaining_files)} of 7 reference files still in orchestration: "
            f"{remaining_files}. All must be removed after migration."
        )

    def test_should_not_have_any_of_eight_migrated_files_in_orchestration_when_cleanup_complete(self):
        """Verify none of the 8 migrated files (7 refs + 1 template) remain in orchestration."""
        remaining_files = []

        # Check 7 reference files
        for filename in REFERENCE_FILES:
            source_path = os.path.join(ORCHESTRATION_REFERENCES_DIR, filename)
            if os.path.exists(source_path):
                remaining_files.append(f"references/{filename}")

        # Check 1 template file
        template_path = os.path.join(ORCHESTRATION_TEMPLATES_DIR, TEMPLATE_FILE)
        if os.path.exists(template_path):
            remaining_files.append(f"assets/templates/{TEMPLATE_FILE}")

        assert len(remaining_files) == 0, (
            f"{len(remaining_files)} of 8 migrated files still in orchestration: "
            f"{remaining_files}. All must be removed after migration."
        )
