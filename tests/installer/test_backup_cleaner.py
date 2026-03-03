"""
STORY-080: Unit tests for BackupCleaner service.

Tests retention-based backup cleanup and deletion.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+ business logic
Test Categories: AC#8
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime, timedelta
import json


class TestBackupCleanup:
    """Test backup cleanup with retention policy (AC#8, SVC-012/013)."""

    def test_cleanup_deletes_oldest_backups(self, tmp_path):
        """
        Test: BackupCleaner deletes oldest backups when limit exceeded (AC#8, SVC-012).

        Given: 7 backups exist with retention limit=5
        When: cleanup() is called
        Then: 2 oldest backups are deleted
        And: 5 newest backups remain
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 7 backups with different ages
        backup_ids = []
        for i in range(7):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=7-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))
            backup_ids.append(f"backup-{i:03d}")

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        result = cleaner.cleanup()

        # Assert
        remaining_backups = list(backup_dir.glob("backup-*"))
        assert len(remaining_backups) == 5
        assert result.deleted_count == 2

    def test_cleanup_keeps_retention_count(self, tmp_path):
        """
        Test: cleanup() keeps exact retention count (AC#8, SVC-012).

        Given: 7 backups with retention_count=5
        When: cleanup() is called
        Then: Exactly 5 backups remain (newest)
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 7 backups
        for i in range(7):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=7-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        result = cleaner.cleanup()

        # Assert
        remaining_backups = list(backup_dir.glob("backup-*"))
        assert len(remaining_backups) == 5

    def test_cleanup_with_retention_1_keeps_one_backup(self, tmp_path):
        """
        Test: cleanup() with retention_count=1 keeps only newest (AC#8).

        Given: 5 backups with retention_count=1
        When: cleanup() is called
        Then: Only newest backup remains
        And: 4 oldest backups deleted
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 5 backups
        for i in range(5):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=5-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=1)

        # Act
        result = cleaner.cleanup()

        # Assert
        remaining_backups = list(backup_dir.glob("backup-*"))
        assert len(remaining_backups) == 1
        assert result.deleted_count == 4

    def test_cleanup_with_retention_5_keeps_five_backups(self, tmp_path):
        """
        Test: cleanup() with retention_count=5 keeps exactly 5 (AC#8).

        Given: 10 backups with retention_count=5
        When: cleanup() is called
        Then: Exactly 5 newest backups remain
        And: 5 oldest backups deleted
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 10 backups
        for i in range(10):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=10-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        result = cleaner.cleanup()

        # Assert
        remaining_backups = list(backup_dir.glob("backup-*"))
        assert len(remaining_backups) == 5
        assert result.deleted_count == 5

    def test_cleanup_never_deletes_excluded_backup(self, tmp_path):
        """
        Test: cleanup() preserves backup being restored (AC#8, SVC-013).

        Given: cleanup_excluded_backup_id="backup-005" and 7 backups
        When: cleanup() is called
        Then: backup-005 is NEVER deleted (even if oldest)
        And: Other backups are deleted to reach retention count
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 7 backups
        for i in range(7):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=7-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(
            backup_dir=backup_dir,
            retention_count=5,
            cleanup_excluded_backup_id="backup-000"  # Oldest backup - should be preserved
        )

        # Act
        result = cleaner.cleanup()

        # Assert
        assert (backup_dir / "backup-000").exists()
        assert "backup-000" not in result.deleted_backup_ids

    def test_cleanup_only_after_successful_rollback(self, tmp_path):
        """
        Test: cleanup() only runs after successful rollback (AC#8, SVC-012).

        Given: Rollback is in progress or failed
        When: cleanup() is called with skip_if_rollback_failed=True
        Then: Returns without deleting if rollback failed
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 7 backups
        for i in range(7):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=7-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        # Skip cleanup because rollback failed
        result = cleaner.cleanup(skip_if_condition_met=True, condition_met=False)

        # Assert
        # All 7 backups should still exist
        remaining_backups = list(backup_dir.glob("backup-*"))
        assert len(remaining_backups) == 7

    def test_cleanup_returns_deleted_backup_names(self, tmp_path):
        """
        Test: cleanup() returns list of deleted backup IDs (AC#8).

        Given: 7 backups with retention=5
        When: cleanup() is called
        Then: Returns CleanupResult with deleted_backup_ids list
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 7 backups
        for i in range(7):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=7-i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        result = cleaner.cleanup()

        # Assert
        assert hasattr(result, "deleted_backup_ids")
        assert len(result.deleted_backup_ids) == 2
        assert isinstance(result.deleted_backup_ids, list)

    def test_cleanup_with_no_backups_succeeds(self, tmp_path):
        """
        Test: cleanup() handles no backups gracefully (edge case).

        Given: No backups exist in directory
        When: cleanup() is called
        Then: Returns success with deleted_count=0
        """
        # Arrange
        from installer.backup_cleaner import BackupCleaner

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        cleaner = BackupCleaner(backup_dir=backup_dir, retention_count=5)

        # Act
        result = cleaner.cleanup()

        # Assert
        assert result.deleted_count == 0
        assert result.deleted_backup_ids == []
