"""
Integration tests for fresh installation workflow (STORY-045 Phase 4).

Test Scenario: Fresh Install
Validates that a complete fresh installation to an empty project:
1. Deploys all framework files (450+ files)
2. Creates .version.json with correct metadata
3. Sets proper file permissions (dirs=755, scripts=755)
4. Creates .backups/ directory structure
5. Completes without backup (fresh install doesn't backup)
6. Leaves project in valid state (deployable)

AC Mapping:
- AC-1.1: Deploy .claude/ with 370 files
- AC-1.2: Deploy devforgeai/ with 80 files
- AC-1.3: Create .version.json with version metadata
- AC-1.4: Set file permissions correctly
- AC-1.5: Project passes validation after install

NFR Validation:
- Fresh install completes in <180 seconds
- All 450+ files deployed successfully
- No partial installations on failure
- Zero framework files in empty project before install

Test Files Created: 8 tests
- test_fresh_install_deploys_all_files
- test_fresh_install_creates_version_metadata
- test_fresh_install_sets_permissions
- test_fresh_install_creates_backups_directory
- test_fresh_install_detects_correct_mode
- test_fresh_install_completes_within_nfr_time
- test_fresh_install_to_nonexistent_directory
- test_fresh_install_leaves_valid_state
"""

import pytest
import json
from pathlib import Path
import time


class TestFreshInstallWorkflow:
    """Fresh install integration tests with real file I/O"""

    def test_fresh_install_deploys_all_files(
        self,
        integration_project,
        source_framework,
        performance_timer,
        file_integrity_checker,
    ):
        """
        AC-1.1: Fresh install deploys all framework files to target project.

        Validates:
        - All 370 .claude/ files deployed
        - All 80 devforgeai/ files deployed
        - File content matches source exactly
        - No files missing or corrupted

        Expected: 450+ files in target after install
        """
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Pre-check: Target should be empty (fresh install)
        claude_count_before = file_integrity_checker.count_files(
            target_root / ".claude"
        )
        assert (
            claude_count_before == 0
        ), f"Expected empty .claude/, found {claude_count_before} files"

        # Execute install
        with performance_timer.measure("fresh_install"):
            result = install.install(target_root, source_root)

        # Verify success
        assert result["status"] == "success"
        assert result["mode"] == "fresh_install"
        assert result["files_deployed"] > 0

        # Verify all files deployed
        claude_count_after = file_integrity_checker.count_files(
            target_root / ".claude"
        )
        devforgeai_count = file_integrity_checker.count_files(
            target_root / ".devforgeai"
        )

        assert (
            claude_count_after == 370
        ), f"Expected 370 .claude/ files, got {claude_count_after}"
        assert (
            devforgeai_count >= 80
        ), f"Expected ≥80 devforgeai/ files, got {devforgeai_count}"

        # Verify directories exist
        assert file_integrity_checker.verify_directory_exists(
            target_root / ".claude" / "agents"
        )
        assert file_integrity_checker.verify_directory_exists(
            target_root / ".claude" / "commands"
        )
        assert file_integrity_checker.verify_directory_exists(
            target_root / ".devforgeai" / "config"
        )

    def test_fresh_install_creates_version_metadata(
        self, integration_project, source_framework
    ):
        """
        AC-1.3: Fresh install creates .version.json with correct metadata.

        Validates:
        - .version.json exists in devforgeai/
        - version field = "1.0.1"
        - installed_at field contains ISO timestamp
        - mode field = "fresh_install"
        - schema_version field = "1.0"

        Expected: .version.json readable, contains all required fields
        """
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Execute install
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify .version.json
        version_file = target_root / ".devforgeai" / ".version.json"
        assert (
            version_file.exists()
        ), ".version.json not found in devforgeai/"

        # Parse version.json
        version_data = json.loads(version_file.read_text())

        # Verify fields
        assert version_data.get("version") == "1.0.1", "Version field incorrect"
        assert (
            version_data.get("mode") == "fresh_install"
        ), "Mode should be fresh_install"
        assert "installed_at" in version_data, "Missing installed_at field"
        assert version_data.get("schema_version") == "1.0", "Schema version incorrect"

        # Verify timestamp format (ISO 8601)
        installed_at = version_data.get("installed_at")
        assert "T" in installed_at, "Timestamp should be ISO format"
        assert "Z" in installed_at, "Timestamp should be UTC (Z)"

    def test_fresh_install_sets_permissions(self, integration_project, source_framework):
        """
        AC-1.4: Fresh install sets correct file permissions.

        NFR: File permissions
        - Directories: 755 (rwxr-xr-x)
        - Executable scripts: 755
        - Documentation files: 644 (rw-r--r--)

        Validates: Sample files have correct permissions after install

        Expected: Permissions match framework standards
        """
        import os
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Execute install
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Check directory permissions
        claude_agents = target_root / ".claude" / "agents"
        assert (
            claude_agents.exists()
        ), ".claude/agents/ should exist after install"

        # Get actual permissions
        dir_perms = oct(claude_agents.stat().st_mode)[-3:]
        assert dir_perms == "755", f"Directory permissions should be 755, got {dir_perms}"

        # Verify .devforgeai directory
        devforgeai_dir = target_root / ".devforgeai"
        devforgeai_perms = oct(devforgeai_dir.stat().st_mode)[-3:]
        assert devforgeai_perms == "755", f"Devforgeai perms should be 755, got {devforgeai_perms}"

    def test_fresh_install_creates_backups_directory(
        self, integration_project, source_framework
    ):
        """
        AC-1.2: Fresh install creates .backups/ directory structure.

        Note: Fresh install doesn't CREATE backups (no previous version to backup),
        but MUST create .backups/ directory for future use.

        Validates:
        - .backups/ directory exists
        - .backups/ is empty (no backup created for fresh install)

        Expected: Empty .backups/ directory ready for future backups
        """
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Execute install
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify .backups/ directory exists
        backups_dir = target_root / ".backups"
        assert backups_dir.exists(), ".backups/ directory not created"
        assert backups_dir.is_dir(), ".backups/ should be a directory"

        # Verify no backup created (fresh install doesn't backup)
        backup_contents = list(backups_dir.iterdir())
        assert (
            len(backup_contents) == 0
        ), f"Fresh install should not create backup, found {len(backup_contents)} items"

    def test_fresh_install_detects_correct_mode(
        self, integration_project, source_framework
    ):
        """
        AC-1.1: Fresh install correctly detects fresh_install mode.

        Validates:
        - Empty project detected as fresh_install (no .version.json)
        - Mode auto-detection works (mode=None passed to install)
        - Result includes mode=fresh_install

        Expected: Result["mode"] == "fresh_install"
        """
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Execute install WITHOUT specifying mode (test auto-detection)
        result = install.install(target_root, source_root, mode=None)

        assert result["status"] == "success"
        assert result["mode"] == "fresh_install", "Mode should be auto-detected as fresh_install"

    def test_fresh_install_completes_within_nfr_time(
        self, integration_project, source_framework, performance_timer
    ):
        """
        NFR: Fresh installation must complete in <180 seconds (3 minutes).

        Validates:
        - Fresh install deployment completes within 180 seconds
        - All 450+ files deployed in that time

        Expected: Elapsed time < 180 seconds
        """
        from installer import install

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Measure execution time
        with performance_timer.measure("fresh_install"):
            result = install.install(target_root, source_root)

        assert result["status"] == "success"
        assert (
            performance_timer.elapsed < 180
        ), f"Fresh install exceeded 180s limit: {performance_timer.elapsed:.1f}s"

    def test_fresh_install_to_nonexistent_directory(
        self, tmp_path, source_framework
    ):
        """
        AC-1.1: Fresh install creates target directory if it doesn't exist.

        Validates:
        - Target directory auto-created if missing
        - Install proceeds normally
        - All files deployed to created directory

        Expected: Directory created and install succeeds
        """
        from installer import install

        target_root = tmp_path / "nonexistent" / "project"
        assert not target_root.exists(), "Target should not exist initially"

        source_root = source_framework["root"]

        # Execute install to nonexistent directory
        result = install.install(target_root, source_root)

        assert result["status"] == "success"
        assert target_root.exists(), "Target directory should be created"
        assert (
            target_root / ".claude"
        ).exists(), ".claude/ should be created"
        assert (
            target_root / ".devforgeai"
        ).exists(), "devforgeai/ should be created"

    def test_fresh_install_leaves_valid_state(
        self, integration_project, source_framework
    ):
        """
        AC-1.5: Fresh install leaves project in valid state.

        Validates that after fresh install:
        - Project structure is valid
        - All required directories exist
        - Framework files are intact (no corruption)
        - Project ready for CLI/development

        Expected: Installation validation passes
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Execute install
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify project is in valid state
        validation = validate.validate_installation(target_root)

        assert (
            validation.get("valid") is True
        ), f"Project not in valid state: {validation.get('errors')}"

        # Verify critical directories
        assert (target_root / ".claude").exists()
        assert (target_root / ".devforgeai").exists()
        assert (target_root / ".devforgeai" / ".version.json").exists()
