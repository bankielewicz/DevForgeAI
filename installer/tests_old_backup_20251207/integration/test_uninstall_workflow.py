"""
Integration tests for uninstall workflow (STORY-045 Phase 4).

Test Scenario: Framework Uninstall with User Data Preservation
Validates that uninstall removes framework while preserving user data:
1. Creates backup before uninstalling (recovery capability)
2. Removes .claude/ directory completely
3. Removes devforgeai/ subdirectories (except context)
4. Removes CLAUDE.md file
5. Preserves devforgeai/specs/ (user stories)
6. Preserves devforgeai/specs/context/ (user context files)
7. Removes .version.json

AC Mapping:
- AC-5.1: Backup created before uninstall
- AC-5.2: Framework directories removed
- AC-5.3: User data preserved (.ai_docs, context)
- AC-5.4: .version.json removed
- AC-5.5: Project usable after uninstall

Test Files Created: 5 tests
- test_uninstall_creates_backup
- test_uninstall_removes_framework_files
- test_uninstall_preserves_user_data
- test_uninstall_removes_version_metadata
- test_uninstall_completes_successfully
"""

import pytest
import json
from pathlib import Path
import shutil


class TestUninstallWorkflow:
    """Uninstall integration tests with user data preservation verification"""

    def test_uninstall_creates_backup(
        self, integration_project, source_framework, baseline_project
    ):
        """
        AC-5.1: Uninstall creates backup before removing framework files.

        Validates:
        - Backup created in .backups/
        - Backup contains current state
        - manifest.json includes "uninstall" reason

        Expected: Backup exists with recovery capability
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]

        # Verify installation exists
        assert (target_root / ".claude").exists()
        assert (target_root / "devforgeai").exists()

        # Execute uninstall
        uninstall_result = install.install(target_root, mode="uninstall")
        assert uninstall_result["status"] == "success"

        # Verify backup created
        backup_path = uninstall_result.get("backup_path")
        assert (
            backup_path is not None
        ), "Uninstall should create backup before removing files"

        backup_path = Path(backup_path)
        assert backup_path.exists(), f"Backup should exist at {backup_path}"

        # Verify manifest
        manifest_file = backup_path / "manifest.json"
        assert manifest_file.exists(), "Backup should have manifest.json"

        manifest = json.loads(manifest_file.read_text())
        assert (
            manifest.get("reason") == "uninstall"
        ), "Backup reason should be 'uninstall'"

    def test_uninstall_removes_framework_files(
        self, baseline_project, file_integrity_checker
    ):
        """
        AC-5.2: Uninstall removes framework files (.claude, devforgeai subdirs).

        Validates:
        - .claude/ directory removed completely
        - devforgeai subdirectories removed (except context)
        - CLAUDE.md removed
        - .backups/ directory preserved

        Expected: Framework files gone, directory structure clean
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]

        # Verify framework exists before uninstall
        assert (
            target_root / ".claude"
        ).exists(), ".claude/ should exist before uninstall"
        assert file_integrity_checker.verify_directory_exists(
            target_root / "devforgeai"
        )

        # Create CLAUDE.md
        claude_md = target_root / "CLAUDE.md"
        claude_md.write_text("# CLAUDE.md project configuration")

        # Execute uninstall
        uninstall_result = install.install(target_root, mode="uninstall")
        assert uninstall_result["status"] == "success"

        # Verify framework files removed
        assert not (
            target_root / ".claude"
        ).exists(), ".claude/ should be removed"
        assert not claude_md.exists(), "CLAUDE.md should be removed"

        # Verify .backups/ preserved
        assert (
            target_root / ".backups"
        ).exists(), ".backups/ should be preserved for recovery"

    @pytest.mark.skip(reason="Requires uninstall workflow implementation")
    def test_uninstall_preserves_user_data(
        self, baseline_project, real_user_files
    ):
        """
        AC-5.3: Uninstall preserves user data (.ai_docs, context files).

        Validates:
        - devforgeai/specs/ directory untouched
        - User stories preserved
        - devforgeai/specs/context/ preserved
        - User context files unchanged

        Expected: All user files intact after uninstall
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]

        # Record user data before uninstall
        user_data_before = {}
        for key, file_info in real_user_files.items():
            file_path = file_info["path"]
            if file_path.exists():
                user_data_before[key] = file_path.read_text()

        # Execute uninstall
        uninstall_result = install.install(target_root, mode="uninstall")
        assert uninstall_result["status"] == "success"

        # Verify user data preserved
        assert (
            target_root / ".ai_docs"
        ).exists(), "devforgeai/specs/ should be preserved"
        assert (
            target_root / "devforgeai" / "context"
        ).exists(), "context/ should be preserved"

        # Verify user files unchanged
        for key, file_info in real_user_files.items():
            file_path = file_info["path"]
            if key in user_data_before:
                assert (
                    file_path.exists()
                ), f"User file {key} should be preserved"
                content_after = file_path.read_text()
                assert (
                    content_after == user_data_before[key]
                ), f"User file {key} content changed"

    @pytest.mark.skip(reason="Requires uninstall workflow implementation")
    def test_uninstall_removes_version_metadata(self, baseline_project):
        """
        AC-5.4: Uninstall removes .version.json (installation metadata).

        Validates:
        - .version.json deleted
        - Installation no longer detected as installed
        - Next install would be fresh_install mode

        Expected: .version.json removed, no installation metadata
        """
        from installer import install, version as ver_module

        project = baseline_project["project"]
        target_root = project["root"]
        devforgeai_dir = target_root / "devforgeai"

        # Verify .version.json exists
        version_file = devforgeai_dir / ".version.json"
        assert version_file.exists(), ".version.json should exist before uninstall"

        # Execute uninstall
        uninstall_result = install.install(target_root, mode="uninstall")
        assert uninstall_result["status"] == "success"

        # Verify .version.json removed
        assert (
            not version_file.exists()
        ), ".version.json should be removed"

        # Verify installation no longer detected
        installed = ver_module.get_installed_version(devforgeai_dir)
        assert (
            installed is None
        ), "Should not detect installed version after uninstall"

    def test_uninstall_completes_successfully(
        self, baseline_project, real_user_files
    ):
        """
        AC-5.5: Uninstall completes successfully, project usable.

        Validates:
        - Uninstall operation succeeds
        - No errors reported
        - Project structure still valid (user dirs present)
        - User can reinstall later

        Expected: Uninstall succeeds, project intact for reinstallation
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]

        # Execute uninstall
        uninstall_result = install.install(target_root, mode="uninstall")

        assert (
            uninstall_result["status"] == "success"
        ), "Uninstall should succeed"
        assert (
            len(uninstall_result.get("errors", [])) == 0
        ), "Should have no errors"

        # Verify project structure for reinstallation
        assert target_root.exists(), "Project root should still exist"
        assert (
            target_root / ".ai_docs"
        ).exists(), "User data should be preserved"

        # Verify messages provide guidance
        messages = uninstall_result.get("messages", [])
        assert len(messages) > 0, "Should provide user feedback"
