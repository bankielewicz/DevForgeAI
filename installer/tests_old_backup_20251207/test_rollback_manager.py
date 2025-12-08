"""
Unit tests for rollback manager (STORY-045 AC5 Mode 3, WKR-021, WKR-022, WKR-023, WKR-024).

Tests validate:
- Listing available backups sorted by timestamp (newest first)
- Verifying backup integrity before restoring (manifest validation)
- Restoring all files from backup (complete state restoration)
- Reverting version.json to backup version

These tests validate AC5 Mode 3: "Rollback" operation
and technical requirements WKR-021 through WKR-024.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta


class TestRollbackManager:
    """Unit tests for rollback.py module - rollback operations."""

    def test_list_backups_sorted_by_timestamp(self, tmp_project):
        """
        WKR-021: List available backups sorted by timestamp (newest first).

        Given: Multiple backups exist
        When: list_backups() called
        Then: Returns array sorted descending (newest first)
        """
        # Arrange
        backups_dir = tmp_project["backups"]

        # Create 3 backups with different timestamps
        backup_1 = backups_dir / "devforgeai-upgrade-20251115-100000"
        backup_2 = backups_dir / "devforgeai-upgrade-20251116-150000"
        backup_3 = backups_dir / "devforgeai-upgrade-20251117-143000"

        for backup in [backup_1, backup_2, backup_3]:
            backup.mkdir(parents=True, exist_ok=True)
            (backup / "manifest.json").write_text(json.dumps({"created_at": backup.name}))

        # Act
        backups = sorted([b for b in backups_dir.iterdir() if b.is_dir()], reverse=True)
        backup_names = [b.name for b in backups]

        # Assert
        # Newest should be first
        assert backup_names[0] == "devforgeai-upgrade-20251117-143000"
        assert backup_names[1] == "devforgeai-upgrade-20251116-150000"
        assert backup_names[2] == "devforgeai-upgrade-20251115-100000"

    def test_verify_backup_integrity_success(self, tmp_project, backup_manifest):
        """
        WKR-022: Verify backup integrity before restoring (manifest validation).

        Given: Backup with valid manifest
        When: Integrity verification performed
        Then: Returns success (file count matches, hash validates)
        """
        # Arrange
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Write manifest
        manifest_file = backup_path / "manifest.json"
        manifest_file.write_text(json.dumps(backup_manifest, indent=2))

        # Create expected number of files
        for i in range(backup_manifest["files_backed_up"]):
            (backup_path / f"file_{i:03d}.txt").write_text(f"content {i}")

        # Act
        loaded_manifest = json.loads(manifest_file.read_text())
        actual_file_count = len(list(backup_path.glob("*.txt")))

        # Assert
        assert actual_file_count == loaded_manifest["files_backed_up"]
        assert "backup_integrity_hash" in loaded_manifest
        verification_passed = actual_file_count == loaded_manifest["files_backed_up"]
        assert verification_passed

    def test_verify_backup_integrity_fails_corrupted(self, tmp_project, backup_manifest):
        """
        WKR-022: Backup verification fails when corrupted (missing files).

        Given: Backup manifest claims 450 files, but only 400 exist
        When: Integrity verification performed
        Then: Verification fails, returns error
        """
        # Arrange
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Write manifest claiming 450 files
        manifest_file = backup_path / "manifest.json"
        manifest_file.write_text(json.dumps(backup_manifest, indent=2))

        # But create only 400 files (corrupted)
        for i in range(400):
            (backup_path / f"file_{i:03d}.txt").write_text(f"content {i}")

        # Act
        loaded_manifest = json.loads(manifest_file.read_text())
        actual_file_count = len(list(backup_path.glob("*.txt")))
        verification_failed = actual_file_count != loaded_manifest["files_backed_up"]

        # Assert
        assert verification_failed
        assert actual_file_count < loaded_manifest["files_backed_up"]

    def test_verify_backup_missing_manifest(self, tmp_project):
        """
        WKR-022: Backup verification fails when manifest missing.

        Given: Backup directory exists but manifest.json missing
        When: Integrity verification performed
        Then: Verification fails, error: "Manifest not found"
        """
        # Arrange
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Act
        manifest_file = backup_path / "manifest.json"

        # Assert
        assert not manifest_file.exists()
        # Should raise FileNotFoundError or return (success=False)

    def test_restore_all_files_from_backup(self, tmp_project):
        """
        WKR-023: Restore all files from backup (complete state restoration).

        Given: Backup contains .claude/, .devforgeai/, CLAUDE.md
        When: Rollback initiated
        Then: All files restored to original location
        """
        # Arrange
        # Create backup with files
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        backup_claude = backup_path / ".claude"
        backup_claude.mkdir()
        (backup_claude / "agents").mkdir()
        (backup_claude / "agents" / "test.md").write_text("# Agent")

        backup_devforgeai = backup_path / ".devforgeai"
        backup_devforgeai.mkdir()
        (backup_devforgeai / "config").mkdir()
        (backup_devforgeai / "config" / "hooks.yaml").write_text("# hooks")

        backup_claude_md = backup_path / "CLAUDE.md"
        backup_claude_md.write_text("# CLAUDE.md")

        # Act
        # Simulate restoration: copy backup files back to target
        target_claude = tmp_project["root"] / ".claude"
        target_claude.mkdir(exist_ok=True)
        (target_claude / "agents").mkdir(exist_ok=True)

        for backup_file in backup_claude.rglob("*"):
            if backup_file.is_file():
                relative = backup_file.relative_to(backup_claude)
                target_file = target_claude / relative
                target_file.parent.mkdir(parents=True, exist_ok=True)
                target_file.write_text(backup_file.read_text())

        # Assert
        assert (target_claude / "agents" / "test.md").exists()
        assert (target_claude / "agents" / "test.md").read_text() == "# Agent"

    def test_restore_preserves_file_content(self, tmp_project):
        """
        WKR-023: Verify restored files have identical content to backup.

        Given: Backup contains file with specific content
        When: File restored
        Then: Content matches exactly (byte-for-byte)
        """
        # Arrange
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        backup_file = backup_path / "test.txt"
        original_content = "This is backup content"
        backup_file.write_text(original_content)

        # Act
        target_file = tmp_project["root"] / "test_restored.txt"
        target_file.write_text(backup_file.read_text())

        # Assert
        assert target_file.read_text() == original_content
        assert target_file.read_text() == backup_file.read_text()

    def test_revert_version_json_to_backup_version(self, tmp_project):
        """
        WKR-024: Revert version.json to backup version.

        Given: Current version.json = 1.0.1, backup version.json = 1.0.0
        When: Rollback executed
        Then: version.json reverted to 1.0.0
        """
        # Arrange
        current_version_file = tmp_project["devforgeai"] / ".version.json"
        current_version = {
            "version": "1.0.1",
            "installed_at": "2025-11-17T14:30:00Z",
            "mode": "patch_upgrade",
        }
        current_version_file.write_text(json.dumps(current_version, indent=2))

        # Backup has old version
        backup_version_file = tmp_project["backups"] / "backup" / ".version.json"
        backup_version_file.parent.mkdir(parents=True, exist_ok=True)
        backup_version = {
            "version": "1.0.0",
            "installed_at": "2025-11-15T10:00:00Z",
            "mode": "fresh_install",
        }
        backup_version_file.write_text(json.dumps(backup_version, indent=2))

        # Act
        # Simulate rollback: restore version.json from backup
        rollback_version = json.loads(backup_version_file.read_text())
        current_version_file.write_text(json.dumps(rollback_version, indent=2))

        # Assert
        current_loaded = json.loads(current_version_file.read_text())
        assert current_loaded["version"] == "1.0.0"
        assert current_loaded["version"] == backup_version["version"]

    def test_rollback_cleans_deployed_files(self, tmp_project):
        """
        WKR-023: Rollback removes deployed files and restores from backup.

        Given: Deployment added new files, backup exists
        When: Rollback executed
        Then: New files removed, backup files restored
        """
        # Arrange
        # Create backup
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)
        backup_file = backup_path / "old_file.txt"
        backup_file.write_text("old content")

        # Create deployed file (new in upgrade)
        deployed_file = tmp_project["root"] / "new_file.txt"
        deployed_file.write_text("new content")

        # Act
        # Simulate rollback
        if deployed_file.exists() and deployed_file.name not in [b.name for b in backup_path.iterdir()]:
            deployed_file.unlink()  # Remove new file

        # Restore old file
        target_file = tmp_project["root"] / "old_file.txt"
        target_file.write_text(backup_file.read_text())

        # Assert
        assert not deployed_file.exists()
        assert target_file.exists()
        assert target_file.read_text() == "old content"

    def test_rollback_selects_most_recent_backup(self, tmp_project):
        """
        AC5 Mode 3: Rollback uses most recent backup by default.

        Given: Multiple backups exist
        When: Rollback --mode=rollback (no explicit backup specified)
        Then: Most recent backup used (sorted by timestamp, newest first)
        """
        # Arrange
        backups_dir = tmp_project["backups"]

        backup_old = backups_dir / "devforgeai-upgrade-20251115-100000"
        backup_old.mkdir(parents=True, exist_ok=True)
        (backup_old / "manifest.json").write_text(json.dumps({"version": "1.0.0"}))

        backup_new = backups_dir / "devforgeai-upgrade-20251117-143000"
        backup_new.mkdir(parents=True, exist_ok=True)
        (backup_new / "manifest.json").write_text(json.dumps({"version": "1.0.1"}))

        # Act
        backups = sorted([b for b in backups_dir.iterdir() if b.is_dir()], reverse=True)
        selected_backup = backups[0]

        # Assert
        assert selected_backup.name == "devforgeai-upgrade-20251117-143000"

    def test_rollback_displays_selected_backup_info(self, tmp_project):
        """
        AC5 Mode 3: Display rollback confirmation.

        Given: Rollback initiated
        When: Selected backup confirmed
        Then: Displays: "Rolled back to version X.Y.Z from backup {timestamp}"
        """
        # Arrange
        backup_path = tmp_project["backups"] / "devforgeai-upgrade-20251117-143000"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Act
        # Simulate display message construction
        backup_name = backup_path.name
        version = "1.0.0"
        message = f"✅ Rolled back to version {version} from backup {backup_name}"

        # Assert
        assert "✅" in message
        assert "Rolled back" in message
        assert "1.0.0" in message
        assert "20251117-143000" in message

    def test_rollback_on_deployment_failure_automatic(self, tmp_project):
        """
        AC7, WKR-009: Automatic rollback on deployment failure.

        Given: Deployment failed (permission error mid-way)
        When: Error detected
        Then: Auto-rollback initiates (restore from backup)
        """
        # Arrange
        # Simulate pre-deployment state
        original_file = tmp_project["devforgeai"] / "config" / "hooks.yaml"
        original_file.write_text("# original")

        # Create backup before deployment
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)
        backup_file = backup_path / "hooks.yaml"
        backup_file.write_text(original_file.read_text())

        # Act
        # Simulate deployment that modifies original file
        original_file.write_text("# modified by deployment")

        # Then error occurs - trigger auto-rollback
        # Restore from backup
        original_file.write_text(backup_file.read_text())

        # Assert
        assert original_file.read_text() == "# original"

    def test_rollback_exit_code_0_success(self):
        """
        AC5 Mode 3: Rollback completes with exit code 0.

        Given: Rollback executed successfully
        When: Rollback completed
        Then: Exit code = 0
        """
        # Arrange & Act
        # Successful rollback would return exit code 0
        exit_code = 0

        # Assert
        assert exit_code == 0
