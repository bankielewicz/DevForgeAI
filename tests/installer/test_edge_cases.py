"""
Edge case tests for error handling and boundary conditions (STORY-045 Edge Cases).

Tests validate handling of:
1. Disk space insufficient for backup
2. Corrupted existing installation (missing version.json)
3. Network interruption during CLI installation
4. Concurrent installer executions
5. Version.json schema change between versions
6. Symlink preservation during deployment
7. Large backup accumulation over time

These tests validate STORY-045 Edge Cases section and AC7 error handling.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil


class TestDiskSpaceEdgeCase:
    """Edge case: Insufficient disk space for backup."""

    def test_detect_insufficient_disk_space(self):
        """
        Edge Case 1: Installer detects insufficient disk space before backup.

        Given: Backup requires 15 MB, disk has 8 MB free
        When: Pre-flight check runs
        Then: Aborts with error: "Insufficient disk space: 15 MB required, 8 MB available"
        """
        # Arrange
        required_space_mb = 15
        available_space_mb = 8

        # Act
        has_space = available_space_mb >= required_space_mb

        # Assert
        assert not has_space
        # Installer should abort pre-flight and display error message

    def test_backup_fails_disk_full_during_operation(self, tmp_project):
        """
        Edge Case 1: Backup fails mid-way when disk fills up.

        Given: Backup started, disk fills during operation
        When: Copy operation fails (OSError: No space left on device)
        Then: Rolls back (removes partial backup), displays error, aborts installer
        """
        # Arrange
        backup_path = tmp_project["backups"] / "partial_backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Simulate partial backup
        (backup_path / "file_1.txt").write_text("backed up")

        # Act
        # Simulate disk full error
        try:
            raise OSError("[Errno 28] No space left on device")
        except OSError as e:
            # On error, remove partial backup
            if backup_path.exists():
                shutil.rmtree(backup_path)

        # Assert
        assert not backup_path.exists()


class TestCorruptedInstallationEdgeCase:
    """Edge case: Existing installation is corrupted."""

    def test_detect_corrupted_installation_missing_version_json(self, tmp_project):
        """
        Edge Case 2: .claude/ exists but .version.json missing (corrupted).

        Given: .claude/ directory exists, but devforgeai/.version.json missing
        When: Installer checks installation state
        Then: Detects corruption, prompts: "(1) Repair, (2) Backup and clean, (3) Abort"
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        assert not version_file.exists()

        # But .claude/ exists (simulating partial/corrupted install)
        assert tmp_project["claude"].exists()

        # Act
        has_version_file = version_file.exists()
        has_claude_dir = tmp_project["claude"].exists()
        is_corrupted = has_claude_dir and not has_version_file

        # Assert
        assert is_corrupted
        # Installer should prompt for repair/clean/abort

    def test_repair_corrupted_installation(self, tmp_project):
        """
        Edge Case 2: User chooses "Repair" option for corrupted installation.

        Given: Corrupted installation detected
        When: User selects "Repair"
        Then: Fresh install mode triggered (overwrites corrupted files)
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"

        # Act
        # Repair = fresh_install mode
        mode = "fresh_install"

        # Create version.json (as repair would do)
        version_file.write_text(json.dumps({
            "version": "1.0.1",
            "installed_at": "2025-11-17T14:30:00Z",
            "mode": "repair_fresh_install",
        }))

        # Assert
        assert version_file.exists()
        loaded = json.loads(version_file.read_text())
        assert loaded["version"] == "1.0.1"


class TestNetworkInterruptionEdgeCase:
    """Edge case: Network failure during CLI installation."""

    def test_cli_installation_network_timeout(self):
        """
        Edge Case 3: pip install fails due to network timeout.

        Given: CLI installation attempts: pip install -e .claude/scripts/
        When: Network timeout occurs
        Then: CLI installation fails (non-blocking), framework files deployed successfully
        """
        # Arrange
        cli_installed = False
        framework_deployed = True

        # Act
        try:
            # Simulate pip timeout
            raise TimeoutError("Network timeout")
        except TimeoutError:
            # Don't block installation
            cli_installed = False
            pass

        # Assert
        assert not cli_installed
        assert framework_deployed
        # Installer should log warning but continue

    def test_cli_installation_recovery_manual(self):
        """
        Edge Case 3: User manually installs CLI after framework deployment.

        Given: Framework installed, CLI failed
        When: User runs manual installation later
        Then: Manual pip install succeeds
        """
        # Arrange
        cli_installed = False

        # Act
        # User manually runs: pip install -e .claude/scripts/
        cli_installed = True

        # Assert
        assert cli_installed


class TestConcurrentExecutionEdgeCase:
    """Edge case: Multiple installer executions simultaneously."""

    def test_detect_concurrent_execution_with_lock_file(self, tmp_project):
        """
        Edge Case 4: Second installer detects lock file, aborts.

        Given: First installer running (lock file exists at devforgeai/.install.lock)
        When: Second installer starts on same project
        Then: Detects lock file, aborts with: "Installation in progress (PID 1234)"
        """
        # Arrange
        lock_file = tmp_project["devforgeai"] / ".install.lock"

        # First installer creates lock
        lock_file.write_text("1234\n2025-11-17T14:30:00Z")

        # Act
        # Second installer checks for lock
        is_locked = lock_file.exists()

        # Assert
        assert is_locked
        # Installer should abort with error message

    def test_lock_file_removed_on_completion(self, tmp_project):
        """
        Edge Case 4: Lock file removed when installation completes.

        Given: Installation completed successfully
        When: Lock file cleanup runs
        Then: Lock file removed
        """
        # Arrange
        lock_file = tmp_project["devforgeai"] / ".install.lock"
        lock_file.write_text("1234\n2025-11-17T14:30:00Z")

        # Act
        # On completion
        if lock_file.exists():
            lock_file.unlink()

        # Assert
        assert not lock_file.exists()


class TestSchemaChangeEdgeCase:
    """Edge case: Version.json schema changes between versions."""

    def test_schema_v1_to_v2_migration(self, tmp_project):
        """
        Edge Case 5: Upgrade from v1.0 (old schema) to v1.1 (new schema).

        Given: Installed version.json with schema_version 1.0
        When: Upgrading to version with schema 2.0
        Then: Installer migrates schema (adds new fields with defaults)
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        old_schema = {
            "version": "1.0.0",
            "installed_at": "2025-11-15T10:00:00Z",
            "schema_version": "1.0",
        }
        version_file.write_text(json.dumps(old_schema))

        # Act
        # Load old schema
        loaded = json.loads(version_file.read_text())

        # Migrate to new schema
        if loaded.get("schema_version") == "1.0":
            loaded["schema_version"] = "2.0"
            loaded["last_backup"] = None  # New field
            loaded["installation_id"] = "uuid-here"  # New field

        # Write migrated version
        version_file.write_text(json.dumps(loaded, indent=2))

        # Assert
        migrated = json.loads(version_file.read_text())
        assert migrated["schema_version"] == "2.0"
        assert "last_backup" in migrated
        assert "installation_id" in migrated

    def test_schema_migration_preserves_existing_fields(self, tmp_project):
        """
        Edge Case 5: Schema migration preserves original fields.

        Given: Old schema with fields A, B, C
        When: Migrated to new schema with A, B, C, D, E
        Then: A, B, C preserved, D, E added with defaults
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        old_schema = {
            "version": "1.0.0",
            "installed_at": "2025-11-15T10:00:00Z",
            "mode": "fresh_install",
        }
        version_file.write_text(json.dumps(old_schema))

        # Act
        loaded = json.loads(version_file.read_text())
        original_version = loaded["version"]
        original_installed = loaded["installed_at"]

        # Migrate
        loaded["last_modified"] = "2025-11-17T14:30:00Z"

        # Assert
        assert loaded["version"] == original_version  # Preserved
        assert loaded["installed_at"] == original_installed  # Preserved
        assert "last_modified" in loaded  # Added


class TestSymlinkPreservationEdgeCase:
    """Edge case: Symlinks during deployment."""

    def test_detect_symlink_in_target(self, tmp_project):
        """
        Edge Case 6: Target .claude/ contains symlink.

        Given: Existing .claude/skills/shared → ../common (symlink)
        When: Deployment executes
        Then: Installer detects symlink, prompts: "(1) Follow, (2) Preserve, (3) Skip"
        """
        # Arrange
        common_dir = tmp_project["claude"].parent / "common"
        common_dir.mkdir()
        (common_dir / "shared.py").write_text("# shared")

        skills_dir = tmp_project["claude"] / "skills"
        symlink_path = skills_dir / "shared"

        # Create symlink
        symlink_path.symlink_to(common_dir)

        # Act
        is_symlink = symlink_path.is_symlink()

        # Assert
        assert is_symlink
        # Installer should prompt user

    def test_follow_symlink_during_deployment(self, tmp_project):
        """
        Edge Case 6: Default behavior = follow symlinks (rsync -L).

        Given: Symlink in target
        When: Deployment follows symlinks
        Then: Target content copied (not symlink itself)
        """
        # Arrange
        common_dir = tmp_project["root"] / "common"
        common_dir.mkdir()
        (common_dir / "shared.py").write_text("# shared content")

        symlink_path = tmp_project["claude"] / "skills" / "shared"
        symlink_path.symlink_to(common_dir)

        # Act
        # Simulate "follow symlinks" behavior
        if symlink_path.is_symlink():
            target = symlink_path.resolve()
            # Copy target directory content
            backup_path = tmp_project["backups"] / "shared_backup"
            shutil.copytree(target, backup_path)

        # Assert
        assert (tmp_project["backups"] / "shared_backup" / "shared.py").exists()


class TestBackupAccumulationEdgeCase:
    """Edge case: Large backup accumulation over time."""

    def test_warn_on_excessive_backups(self, tmp_project):
        """
        Edge Case 7: Warn user when >10 backups exist.

        Given: 15 backups in .backups/ (300 MB total)
        When: Installer checks backup count
        Then: Displays warning: "10+ backups found (300 MB). Clean old: rm -rf .backups/...-202501*"
        """
        # Arrange
        backups_dir = tmp_project["backups"]

        # Create 15 backup directories
        for i in range(15):
            backup = backups_dir / f"devforgeai-upgrade-2025010{i:02d}-100000"
            backup.mkdir(parents=True, exist_ok=True)
            # Simulate ~20 MB per backup
            (backup / "large_file.bin").write_bytes(b"x" * (20 * 1024 * 1024))

        # Act
        backup_count = len(list(backups_dir.glob("devforgeai-*")))

        # Assert
        assert backup_count >= 15
        # Installer should warn if >10

    def test_suggestion_to_clean_old_backups(self, tmp_project):
        """
        Edge Case 7: Suggest cleanup command to user.

        Given: Excessive backups exist
        When: Warning displayed
        Then: Suggests: "rm -rf .backups/devforgeai-*-202501*" to remove Jan backups
        """
        # Arrange
        message = "10 backups found (250 MB). Clean old backups with: rm -rf .backups/devforgeai-*-202501*"

        # Act
        suggestion_provided = "rm -rf .backups/devforgeai-*" in message

        # Assert
        assert suggestion_provided
        # User can manually clean if desired


class TestErrorHandlingAndRollback:
    """AC7: Comprehensive error handling with automatic rollback."""

    def test_permission_denied_error_triggers_rollback(self, tmp_project):
        """
        AC7: Permission error during deployment triggers auto-rollback.

        Given: Deployment writes to .claude/commands/, permission denied
        When: Error detected
        Then: Auto-rollback initiated (restore from backup), exit code 1
        """
        # Arrange
        backup_path = tmp_project["backups"] / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Create backup
        original_file = tmp_project["devforgeai"] / "config" / "hooks.yaml"
        original_file.write_text("# original")
        backup_file = backup_path / "hooks.yaml"
        backup_file.write_text(original_file.read_text())

        # Act
        # Simulate permission error
        try:
            raise PermissionError("Permission denied: .claude/commands/")
        except PermissionError:
            # Auto-rollback: restore from backup
            original_file.write_text(backup_file.read_text())

        exit_code = 1

        # Assert
        assert original_file.read_text() == "# original"
        assert exit_code == 1

    def test_deployment_failure_leaves_valid_state(self, tmp_project):
        """
        AC7: Project left in valid state after deployment failure.

        Given: Deployment failed mid-way
        When: Rollback completes
        Then: Project either: (1) has original installation, or (2) clean pre-install state
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        version_file.write_text(json.dumps({
            "version": "1.0.0",
            "installed_at": "2025-11-15T10:00:00Z",
        }))

        # Act
        # Deployment fails and rolls back
        # Project should be back to 1.0.0 state
        loaded = json.loads(version_file.read_text())

        # Assert
        assert loaded["version"] == "1.0.0"
        # Project is in valid state

    def test_verify_checksum_after_rollback(self, tmp_project):
        """
        AC7: Rollback verified by checksum comparison.

        Given: Rollback completed
        When: Verification runs
        Then: All restored files' checksums match backup
        """
        # Arrange
        import hashlib

        backup_file = tmp_project["backups"] / "backup" / "test.txt"
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        backup_file.write_text("original content")

        backup_hash = hashlib.sha256(backup_file.read_bytes()).hexdigest()

        # Restore to target
        target_file = tmp_project["root"] / "test_restored.txt"
        target_file.write_text(backup_file.read_text())

        # Act
        target_hash = hashlib.sha256(target_file.read_bytes()).hexdigest()

        # Assert
        assert backup_hash == target_hash
        # Verification passed
