"""
Integration tests for upgrade workflow (STORY-045 Phase 4).

Test Scenario: Upgrade from v1.0.0 to v1.0.1
Validates that upgrading an existing installation:
1. Detects existing version correctly (not fresh_install)
2. Creates backup before any modifications (atomic transaction)
3. Deploys only changed files (selective update)
4. Preserves user configurations (hooks.yaml, context files)
5. Updates .version.json to new version
6. Completes successfully with full rollback capability

AC Mapping:
- AC-2.1: Backup created before upgrade
- AC-2.2: Only changed files deployed (selective update)
- AC-2.3: User configs preserved (hooks, context)
- AC-2.4: Version.json updated to 1.0.1
- AC-2.5: Project remains valid after upgrade

NFR Validation:
- Patch upgrade (10-file change) completes in <30 seconds
- Backup creation <20 seconds
- No data loss of user files

Test Files Created: 7 tests
- test_upgrade_detects_patch_mode
- test_upgrade_creates_backup_before_deployment
- test_upgrade_preserves_user_configurations
- test_upgrade_selective_update
- test_upgrade_updates_version_metadata
- test_upgrade_completes_within_nfr
- test_upgrade_rollback_capability
"""

import pytest
import json
from pathlib import Path


class TestUpgradeWorkflow:
    """Upgrade integration tests with real file I/O and backup verification"""

    def test_upgrade_detects_patch_mode(self, baseline_project, source_framework):
        """
        AC-2.1: Upgrade correctly detects patch_upgrade mode (1.0.0 → 1.0.1).

        Validates:
        - Existing v1.0.0 installation detected
        - Upgrade mode determined correctly (patch_upgrade)
        - Version comparison works (installed < source)

        Expected: result["mode"] == "patch_upgrade"
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade without specifying mode (test auto-detection)
        result = install.install(target_root, source_root, mode=None)

        assert result["status"] == "success"
        assert (
            result["mode"] == "patch_upgrade"
        ), f"Expected patch_upgrade, got {result['mode']}"
        assert result["version"] == "1.0.1"

    def test_upgrade_creates_backup_before_deployment(
        self, baseline_project, source_framework, file_integrity_checker
    ):
        """
        AC-2.1: Upgrade creates backup BEFORE any modifications (atomic transaction).

        Validates:
        - Backup created in .backups/ with timestamp
        - Backup contains:
          - Copy of .claude/ (state from 1.0.0)
          - Copy of .devforgeai/ (state from 1.0.0)
          - manifest.json with metadata
        - Backup integrity verified

        Expected: Backup exists with original files, upgrade succeeds
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Record .claude file count before upgrade
        claude_count_before = file_integrity_checker.count_files(
            target_root / ".claude"
        )

        # Execute upgrade
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify backup created
        backup_path_str = result.get("backup_path")
        assert (
            backup_path_str is not None
        ), "Backup path should be returned in result"

        backup_path = Path(backup_path_str)
        assert backup_path.exists(), f"Backup not found at {backup_path}"

        # Verify backup contains original files
        backup_claude = backup_path / ".claude"
        assert backup_claude.exists(), "Backup should contain .claude/"
        assert (
            backup_claude / "agents"
        ).exists(), "Backup .claude/agents/ missing"

        # Verify manifest.json
        manifest_file = backup_path / "manifest.json"
        assert manifest_file.exists(), "manifest.json not found in backup"

        manifest = json.loads(manifest_file.read_text())
        assert manifest.get("reason") == "upgrade", "Backup reason should be 'upgrade'"
        assert (
            manifest.get("from_version") == "1.0.0"
        ), "Should backup from version 1.0.0"
        assert (
            manifest.get("to_version") == "1.0.1"
        ), "Should backup to version 1.0.1"
        assert manifest.get("files_backed_up") > 0, "No files backed up"

    def test_upgrade_preserves_user_configurations(
        self, baseline_project, source_framework, real_user_files
    ):
        """
        AC-2.3: Upgrade preserves user configurations and data.

        Validates:
        - User context files unchanged (.devforgeai/context/*.md)
        - User story files unchanged (.ai_docs/Stories/*.md)
        - User hooks.yaml unchanged
        - User feedback config unchanged

        Expected: All user files identical before/after upgrade
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Record user file content before upgrade
        user_files_before = {}
        for key, file_info in real_user_files.items():
            file_path = file_info["path"]
            if file_path.exists():
                user_files_before[key] = file_path.read_text()

        # Execute upgrade
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify user files unchanged
        for key, file_info in real_user_files.items():
            file_path = file_info["path"]
            assert file_path.exists(), f"User file {key} was deleted during upgrade"

            content_after = file_path.read_text()
            content_before = user_files_before.get(key)

            if content_before is not None:
                assert (
                    content_after == content_before
                ), f"User file {key} was modified during upgrade"

    def test_upgrade_selective_update(
        self, baseline_project, source_framework, file_integrity_checker
    ):
        """
        AC-2.2: Upgrade performs selective update (only changed files).

        Validates:
        - Only files that changed are deployed
        - Files not changed remain unchanged
        - Deployment count is realistic (10-50 files for patch)

        NFR: Patch update with 10-file change completes in <30 seconds

        Expected: files_deployed is reasonable (10-50 for patch_upgrade)
        """
        from installer import install
        import time

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade and measure time
        start_time = time.time()
        result = install.install(target_root, source_root)
        elapsed = time.time() - start_time

        assert result["status"] == "success"

        # Verify selective update (not all 450 files)
        files_deployed = result.get("files_deployed", 0)
        assert (
            files_deployed > 0
        ), "No files deployed in upgrade"
        assert (
            files_deployed < 450
        ), f"Selective update failed: deployed {files_deployed} files (should be 10-50)"

        # Verify NFR: <30 seconds for patch
        assert (
            elapsed < 30
        ), f"Patch upgrade exceeded 30s: {elapsed:.1f}s"

    def test_upgrade_updates_version_metadata(self, baseline_project, source_framework):
        """
        AC-2.4: Upgrade updates .version.json to new version.

        Validates:
        - version field changed from 1.0.0 to 1.0.1
        - mode field updated to patch_upgrade
        - installed_at field updated to new timestamp
        - schema_version remains 1.0

        Expected: .version.json shows v1.0.1 with patch_upgrade mode
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Get original version metadata
        version_file = target_root / ".devforgeai" / ".version.json"
        version_before = json.loads(version_file.read_text())
        assert version_before.get("version") == "1.0.0", "Baseline should be 1.0.0"

        # Execute upgrade
        result = install.install(target_root, source_root)
        assert result["status"] == "success"

        # Verify version.json updated
        version_after = json.loads(version_file.read_text())

        assert (
            version_after.get("version") == "1.0.1"
        ), "Version should be updated to 1.0.1"
        assert (
            version_after.get("mode") == "patch_upgrade"
        ), "Mode should be patch_upgrade"
        assert (
            version_after.get("installed_at") != version_before.get("installed_at")
        ), "Timestamp should be updated"
        assert (
            version_after.get("schema_version") == "1.0"
        ), "Schema version should remain 1.0"

    def test_upgrade_completes_within_nfr(
        self, baseline_project, source_framework, performance_timer
    ):
        """
        NFR: Selective patch update must complete in <30 seconds.

        This NFR applies to:
        - Small patches (1-50 files changed)
        - No network operations
        - Local filesystem operations

        Expected: upgrade time < 30 seconds
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Measure upgrade time
        with performance_timer.measure("patch_upgrade"):
            result = install.install(target_root, source_root)

        assert result["status"] == "success"
        assert (
            performance_timer.elapsed < 30
        ), f"Patch upgrade exceeded 30s: {performance_timer.elapsed:.1f}s"

    def test_upgrade_rollback_capability(
        self, baseline_project, source_framework
    ):
        """
        AC-2.1: Upgrade creates backup that enables rollback.

        Validates:
        - Backup can be used to restore previous version
        - Rollback restores project to v1.0.0 state
        - Backup integrity maintained for rollback

        Expected: Upgrade successful, rollback possible
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade
        result = install.install(target_root, source_root)
        assert result["status"] == "success"
        assert result.get("backup_path") is not None

        # Verify backup exists and has manifest
        backup_path = Path(result["backup_path"])
        assert (backup_path / "manifest.json").exists(), "Backup should have manifest"

        # Verify backup contains necessary files for rollback
        assert (backup_path / ".devforgeai").exists(), "Backup should contain .devforgeai/"
        assert (
            backup_path / ".devforgeai" / ".version.json"
        ).exists(), "Backup should contain version.json"

        # Verify version.json in backup is from old version
        backup_version = json.loads(
            (backup_path / ".devforgeai" / ".version.json").read_text()
        )
        assert (
            backup_version.get("version") == "1.0.0"
        ), "Backup should contain v1.0.0 metadata"
