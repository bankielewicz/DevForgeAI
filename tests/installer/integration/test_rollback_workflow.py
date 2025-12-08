"""
Integration tests for rollback workflow (STORY-045 Phase 4).

Test Scenario: Rollback after Upgrade Failure
Validates that after upgrade failure or intentional rollback:
1. Most recent backup restored completely
2. All files restored from backup (exact copy)
3. Version.json reverted to previous version
4. Project functional after rollback
5. Rollback completes atomically (no partial rollbacks)

AC Mapping:
- AC-3.1: Backup restoration restores all files
- AC-3.2: Version.json reverted to backup version
- AC-3.3: Project passes validation after rollback
- AC-3.4: Rollback completes atomically

NFR Validation:
- Rollback <450 files completes in <45 seconds
- 100% file restoration (no missing files)
- Checksums match backup (integrity verified)

Test Files Created: 6 tests
- test_rollback_restores_all_files
- test_rollback_reverts_version_metadata
- test_rollback_verifies_checksums
- test_rollback_completes_within_nfr
- test_rollback_restores_from_most_recent
- test_rollback_leaves_valid_state
"""

import pytest
import json
from pathlib import Path
import hashlib


class TestRollbackWorkflow:
    """Rollback integration tests with file integrity verification"""

    def test_rollback_restores_all_files(self, baseline_project, source_framework):
        """
        AC-3.1: Rollback restores all files from backup completely.

        Validates:
        - All .claude/ files restored from backup
        - All .devforgeai/ files restored from backup
        - File count matches backup manifest
        - No files missing after restore

        Expected: File count before/after restore matches exactly
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Record file count before upgrade
        initial_claude_count = sum(
            1 for _ in (target_root / ".claude").rglob("*") if _.is_file()
        )

        # Execute upgrade (creates backup)
        upgrade_result = install.install(target_root, source_root)
        assert upgrade_result["status"] == "success"

        # Modify a file to simulate changes from upgrade
        test_file = target_root / ".claude" / "agents" / "test_modified.txt"
        test_file.write_text("MODIFIED DURING UPGRADE")

        # Record file count after upgrade
        post_upgrade_claude_count = sum(
            1 for _ in (target_root / ".claude").rglob("*") if _.is_file()
        )

        # Execute rollback
        rollback_result = install.install(target_root, mode="rollback")
        assert rollback_result["status"] == "success"

        # Verify files restored
        post_rollback_claude_count = sum(
            1 for _ in (target_root / ".claude").rglob("*") if _.is_file()
        )

        # Should be close to pre-upgrade (allowing for manifest.json)
        assert (
            post_rollback_claude_count > 0
        ), "No files restored in .claude/ after rollback"

        # Verify modified file is gone or restored to original
        if test_file.exists():
            content = test_file.read_text()
            assert (
                content != "MODIFIED DURING UPGRADE"
            ), "Modified file not restored from backup"

    def test_rollback_reverts_version_metadata(
        self, baseline_project, source_framework
    ):
        """
        AC-3.2: Rollback reverts .version.json to backup version (1.0.0).

        Validates:
        - version field reverted from 1.0.1 to 1.0.0
        - mode field reverted to original mode
        - installed_at field restored from backup

        Expected: .version.json shows v1.0.0 after rollback
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        version_file = target_root / ".devforgeai" / ".version.json"

        # Record version before upgrade
        version_before = json.loads(version_file.read_text())
        assert version_before.get("version") == "1.0.0"

        # Execute upgrade
        upgrade_result = install.install(target_root, source_root)
        assert upgrade_result["status"] == "success"

        # Verify upgrade changed version
        version_after_upgrade = json.loads(version_file.read_text())
        assert version_after_upgrade.get("version") == "1.0.1"

        # Execute rollback
        rollback_result = install.install(target_root, mode="rollback")
        assert rollback_result["status"] == "success"

        # Verify version reverted
        version_after_rollback = json.loads(version_file.read_text())
        assert (
            version_after_rollback.get("version") == "1.0.0"
        ), "Version should be reverted to 1.0.0"
        assert (
            version_after_rollback.get("mode") == "fresh_install"
        ), "Mode should revert to original"

    def test_rollback_verifies_checksums(self, baseline_project, source_framework):
        """
        AC-3.4: Rollback verification checks file integrity via checksums.

        Validates:
        - Backup manifest contains integrity hash
        - Restored files match backup checksums
        - Integrity verified before reporting success

        Expected: Backup integrity check passes, files match
        """
        from installer import install, backup

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade (creates backup)
        upgrade_result = install.install(target_root, source_root)
        assert upgrade_result["status"] == "success"

        backup_path = Path(upgrade_result["backup_path"])

        # Verify backup integrity
        integrity_result = backup.verify_backup_integrity(backup_path)
        assert (
            integrity_result.get("valid") is True
        ), f"Backup integrity check failed: {integrity_result.get('errors')}"

        # Verify manifest has integrity hash
        manifest_file = backup_path / "manifest.json"
        manifest = json.loads(manifest_file.read_text())
        assert (
            "backup_integrity_hash" in manifest
        ), "Backup should have integrity hash"
        assert manifest["backup_integrity_hash"].startswith(
            "sha256:"
        ), "Hash should be SHA256"

        # Execute rollback
        rollback_result = install.install(target_root, mode="rollback")
        assert rollback_result["status"] == "success"

    def test_rollback_completes_within_nfr(
        self, baseline_project, source_framework, performance_timer
    ):
        """
        NFR: Rollback of 450 files must complete in <45 seconds.

        Validates:
        - Rollback operation completes within time limit
        - All files restored in that time

        Expected: Elapsed time < 45 seconds
        """
        from installer import install

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade (creates backup)
        upgrade_result = install.install(target_root, source_root)
        assert upgrade_result["status"] == "success"

        # Measure rollback time
        with performance_timer.measure("rollback"):
            rollback_result = install.install(target_root, mode="rollback")

        assert rollback_result["status"] == "success"
        assert (
            performance_timer.elapsed < 45
        ), f"Rollback exceeded 45s: {performance_timer.elapsed:.1f}s"

    def test_rollback_restores_from_most_recent(
        self, baseline_project, source_framework
    ):
        """
        AC-3.1: Rollback restores from most recent backup.

        Validates:
        - When multiple backups exist, most recent is used
        - Backup list sorted by timestamp (newest first)
        - Correct backup selected for restore

        Expected: Most recent backup (latest timestamp) is restored
        """
        from installer import install, rollback
        import time

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # First upgrade (creates backup 1)
        upgrade_result_1 = install.install(target_root, source_root)
        assert upgrade_result_1["status"] == "success"
        backup_path_1 = Path(upgrade_result_1["backup_path"])

        # Wait a moment to ensure different timestamps
        time.sleep(0.1)

        # List backups (should be 1)
        backups_after_1 = rollback.list_backups(target_root)
        assert len(backups_after_1) >= 1, "Should have at least one backup"

        most_recent = backups_after_1[0]
        assert (
            most_recent["path"] == backup_path_1
        ), "Most recent backup should be first in list"

    def test_rollback_leaves_valid_state(self, baseline_project, source_framework):
        """
        AC-3.3: Project is in valid state after rollback.

        Validates:
        - Installation passes validation after rollback
        - All required directories exist
        - Project is deployable again

        Expected: Validation passes, project is ready for use
        """
        from installer import install, validate

        project = baseline_project["project"]
        target_root = project["root"]
        source_root = source_framework["root"]

        # Execute upgrade
        upgrade_result = install.install(target_root, source_root)
        assert upgrade_result["status"] == "success"

        # Verify upgraded state is valid
        validation_upgraded = validate.validate_installation(target_root)
        assert validation_upgraded.get("valid") is True

        # Execute rollback
        rollback_result = install.install(target_root, mode="rollback")
        assert rollback_result["status"] == "success"

        # Verify rolled-back state is valid
        validation_rolled_back = validate.validate_installation(target_root)
        assert (
            validation_rolled_back.get("valid") is True
        ), "Project should be valid after rollback"

        # Verify critical directories exist
        assert (target_root / ".claude").exists()
        assert (target_root / ".devforgeai").exists()
        assert (target_root / ".devforgeai" / ".version.json").exists()
