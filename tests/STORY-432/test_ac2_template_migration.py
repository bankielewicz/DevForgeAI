"""
Test: AC#2 - Epic Template Migrated to Architecture Assets
Story: STORY-432
Generated: 2026-02-17

Verifies that the epic-template.md file is migrated from orchestration
assets/templates/ to architecture assets/templates/.

Given: The epic template exists at orchestration assets/templates/epic-template.md
When: The migration is completed
Then: The epic template exists at architecture assets/templates/epic-template.md
"""
import os
import pytest

from conftest import (
    ARCHITECTURE_TEMPLATES_DIR,
    TEMPLATE_FILE,
)


class TestAC2TemplateMigration:
    """AC#2: Epic template migrated to architecture assets."""

    def test_should_have_templates_directory_in_architecture_when_migration_complete(self):
        """Verify architecture assets/templates/ directory exists."""
        assert os.path.isdir(ARCHITECTURE_TEMPLATES_DIR), (
            f"Architecture templates directory not found at {ARCHITECTURE_TEMPLATES_DIR}. "
            "Directory must be created during migration (BR-004)."
        )

    def test_should_have_epic_template_in_architecture_when_migration_complete(self):
        """Verify epic-template.md exists in architecture assets/templates/."""
        target_path = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        assert os.path.isfile(target_path), (
            f"epic-template.md not found at {target_path}. "
            "Template must be migrated from orchestration to architecture."
        )

    def test_should_have_nonempty_epic_template_in_architecture_when_migration_complete(self):
        """Verify the migrated epic-template.md is not empty."""
        target_path = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        if not os.path.isfile(target_path):
            pytest.fail(f"epic-template.md does not exist at {target_path}")

        file_size = os.path.getsize(target_path)
        assert file_size > 0, (
            f"epic-template.md at {target_path} is empty (0 bytes). "
            "Migration must preserve file content."
        )

    def test_should_have_epic_template_with_minimum_expected_size_when_migration_complete(self):
        """Verify the migrated epic-template.md has a reasonable file size (~265 lines expected)."""
        target_path = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        if not os.path.isfile(target_path):
            pytest.fail(f"epic-template.md does not exist at {target_path}")

        file_size = os.path.getsize(target_path)
        # Epic template is ~265 lines. A minimum of 500 bytes is reasonable
        # to ensure content was not truncated.
        assert file_size >= 500, (
            f"epic-template.md is suspiciously small ({file_size} bytes). "
            "Expected at least 500 bytes for a ~265 line template. "
            "Content may have been truncated during migration."
        )

    def test_should_have_assets_directory_in_architecture_when_migration_complete(self):
        """Verify the architecture assets/ parent directory exists."""
        assets_dir = os.path.dirname(ARCHITECTURE_TEMPLATES_DIR)
        assert os.path.isdir(assets_dir), (
            f"Architecture assets directory not found at {assets_dir}. "
            "Parent directory structure must exist for template migration."
        )
