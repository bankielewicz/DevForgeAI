"""
Test: AC#5 - Architecture Skill Directory Structure Valid
Story: STORY-432
Generated: 2026-02-17

Verifies that the architecture skill directory structure is valid after
migration, with references/ containing all 7 migrated files and
assets/templates/ containing epic-template.md.

Given: The migration is complete
When: The architecture skill directory structure is inspected
Then: references/ contains all migrated files AND assets/templates/ contains
      the epic template, following source-tree.md conventions
"""
import os
import pytest

from conftest import (
    ARCHITECTURE_REFERENCES_DIR,
    ARCHITECTURE_TEMPLATES_DIR,
    PROJECT_ROOT,
    REFERENCE_FILES,
    TEMPLATE_FILE,
)


class TestAC5DirectoryStructure:
    """AC#5: Architecture skill directory structure valid."""

    # --- Directory existence tests ---

    def test_should_have_architecture_skill_root_directory(self):
        """Verify the architecture skill root directory exists."""
        arch_root = os.path.join(
            PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture"
        )
        assert os.path.isdir(arch_root), (
            f"Architecture skill root not found at {arch_root}."
        )

    def test_should_have_references_directory_in_architecture(self):
        """Verify architecture skill has a references/ subdirectory."""
        assert os.path.isdir(ARCHITECTURE_REFERENCES_DIR), (
            f"references/ directory not found at {ARCHITECTURE_REFERENCES_DIR}."
        )

    def test_should_have_assets_templates_directory_in_architecture(self):
        """Verify architecture skill has an assets/templates/ subdirectory."""
        assert os.path.isdir(ARCHITECTURE_TEMPLATES_DIR), (
            f"assets/templates/ directory not found at {ARCHITECTURE_TEMPLATES_DIR}. "
            "Directory must be created during migration."
        )

    # --- References directory content tests ---

    def test_should_have_seven_migrated_files_in_references_directory(self):
        """Verify the references/ directory contains all 7 migrated reference files."""
        missing = []
        for filename in REFERENCE_FILES:
            filepath = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
            if not os.path.isfile(filepath):
                missing.append(filename)

        assert len(missing) == 0, (
            f"Architecture references/ is missing {len(missing)} migrated file(s): {missing}"
        )

    def test_should_have_all_references_as_markdown_files(self):
        """Verify all migrated reference files have .md extension (source-tree.md convention)."""
        non_md_files = []
        for filename in REFERENCE_FILES:
            if not filename.endswith(".md"):
                non_md_files.append(filename)

        assert len(non_md_files) == 0, (
            f"Non-markdown files found in migration manifest: {non_md_files}. "
            "All reference files must be .md per source-tree.md conventions."
        )

    # --- Templates directory content tests ---

    def test_should_have_epic_template_in_assets_templates(self):
        """Verify assets/templates/ contains epic-template.md."""
        filepath = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        assert os.path.isfile(filepath), (
            f"epic-template.md not found at {filepath}. "
            "Template must exist in architecture assets/templates/."
        )

    # --- Source tree convention compliance ---

    def test_should_follow_skill_directory_naming_convention(self):
        """Verify architecture skill uses lowercase-hyphenated naming (source-tree.md)."""
        skill_dir_name = "devforgeai-architecture"
        skill_path = os.path.join(
            PROJECT_ROOT, "src", "claude", "skills", skill_dir_name
        )
        assert os.path.isdir(skill_path), (
            f"Skill directory '{skill_dir_name}' not found at expected path. "
            "Skill directories must use lowercase-hyphenated naming per source-tree.md."
        )

    def test_should_have_references_subdirectory_not_nested_deeper(self):
        """Verify references/ is a direct child of the skill directory, not nested deeper."""
        expected_path = os.path.join(
            PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
        )
        assert ARCHITECTURE_REFERENCES_DIR == expected_path, (
            f"references/ directory path mismatch. "
            f"Expected: {expected_path}, Got: {ARCHITECTURE_REFERENCES_DIR}"
        )

    def test_should_have_assets_templates_at_correct_nesting_level(self):
        """Verify assets/templates/ is at the correct nesting level under the skill."""
        expected_path = os.path.join(
            PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture",
            "assets", "templates"
        )
        assert ARCHITECTURE_TEMPLATES_DIR == expected_path, (
            f"assets/templates/ directory path mismatch. "
            f"Expected: {expected_path}, Got: {ARCHITECTURE_TEMPLATES_DIR}"
        )

    # --- Dual-path architecture compliance (BR-003) ---

    def test_should_target_src_tree_not_operational_directory(self):
        """Verify migration targets src/ tree per dual-path architecture (BR-003)."""
        # The architecture references dir should be under src/, not under .claude/
        assert "src" in ARCHITECTURE_REFERENCES_DIR.split(os.sep), (
            f"Migration target {ARCHITECTURE_REFERENCES_DIR} is not under src/ tree. "
            "Per BR-003 and CLAUDE.md, src/ is the source of truth for framework development."
        )
        assert ".claude" not in ARCHITECTURE_REFERENCES_DIR.split(os.sep), (
            f"Migration target {ARCHITECTURE_REFERENCES_DIR} is under .claude/ (operational). "
            "Per BR-003, migration must target src/ tree, not operational directories."
        )

    # --- Combined structure validation ---

    def test_should_have_complete_post_migration_structure(self):
        """Verify the complete post-migration directory structure is valid.

        Checks:
        1. references/ contains all 7 migrated files
        2. assets/templates/ contains epic-template.md
        3. Both directories are at correct nesting levels
        """
        errors = []

        # Check references/
        if not os.path.isdir(ARCHITECTURE_REFERENCES_DIR):
            errors.append("references/ directory does not exist")
        else:
            for filename in REFERENCE_FILES:
                if not os.path.isfile(os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)):
                    errors.append(f"references/{filename} missing")

        # Check assets/templates/
        if not os.path.isdir(ARCHITECTURE_TEMPLATES_DIR):
            errors.append("assets/templates/ directory does not exist")
        else:
            template_path = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
            if not os.path.isfile(template_path):
                errors.append(f"assets/templates/{TEMPLATE_FILE} missing")

        assert len(errors) == 0, (
            f"Post-migration directory structure invalid. {len(errors)} issue(s): "
            f"{errors}"
        )
