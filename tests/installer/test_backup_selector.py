"""
STORY-080: Unit tests for BackupSelector service.

Tests listing, formatting, and selecting available backups.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+ business logic
Test Categories: AC#2, AC#3
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime, timedelta
import json


class TestListBackups:
    """Test listing available backups (AC#3, SVC-009)."""

    def test_list_backups_returns_all_available(self, tmp_path):
        """
        Test: BackupSelector lists all available backups (AC#3, SVC-009).

        Given: Multiple backups exist in backup directory
        When: list() is called
        Then: Returns all available backups
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 5 test backups
        for i in range(5):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
                "size_bytes": 1000000 + i * 100000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        backups = selector.list()

        # Assert
        assert len(backups) == 5

    def test_list_backups_sorted_newest_first(self, tmp_path):
        """
        Test: Backups are sorted by date (newest first) (AC#3, SVC-009).

        Given: Multiple backups with different timestamps
        When: list() is called
        Then: Returns backups sorted by timestamp (newest first)
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create backups with dates 3 days ago, 2 days ago, 1 day ago
        dates = [
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=1)
        ]

        for i, date in enumerate(dates):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": date.isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        backups = selector.list()

        # Assert
        # Newest should be first (index 0)
        assert backups[0].timestamp > backups[1].timestamp
        assert backups[1].timestamp > backups[2].timestamp

    def test_list_backups_with_no_backups_returns_empty(self, tmp_path):
        """
        Test: list() returns empty when no backups exist (edge case).

        Given: No backups in directory
        When: list() is called
        Then: Returns empty list
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        backups = selector.list()

        # Assert
        assert backups == []


class TestFormatBackupInfo:
    """Test formatting backup information for display (AC#3, SVC-010)."""

    def test_format_for_display_includes_version(self, tmp_path):
        """
        Test: Formatted backup includes version number (AC#3, SVC-010).

        Given: A backup with version 1.0.5
        When: format_for_display() is called
        Then: Output includes version "1.0.5"
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        backup_info = BackupInfo(
            id="backup-001",
            version="1.0.5",
            timestamp=datetime.now(),
            size_bytes=5000000,
            reason="UPGRADE"
        )

        selector = BackupSelector(backup_dir=tmp_path / "backups")

        # Act
        formatted = selector.format_for_display(backup_info)

        # Assert
        assert "1.0.5" in formatted

    def test_format_for_display_includes_date(self, tmp_path):
        """
        Test: Formatted backup includes date and time (AC#3, SVC-010).

        Given: A backup with timestamp
        When: format_for_display() is called
        Then: Output includes formatted date/time
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        test_date = datetime(2025, 11, 25, 14, 30, 0)
        backup_info = BackupInfo(
            id="backup-001",
            version="1.0.0",
            timestamp=test_date,
            size_bytes=5000000,
            reason="UPGRADE"
        )

        selector = BackupSelector(backup_dir=tmp_path / "backups")

        # Act
        formatted = selector.format_for_display(backup_info)

        # Assert
        assert "2025" in formatted or "11" in formatted or "25" in formatted

    def test_format_for_display_includes_size(self, tmp_path):
        """
        Test: Formatted backup includes size in MB (AC#3, SVC-010).

        Given: A backup with size 5,000,000 bytes (5 MB)
        When: format_for_display() is called
        Then: Output includes "5 MB" or similar readable format
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        backup_info = BackupInfo(
            id="backup-001",
            version="1.0.0",
            timestamp=datetime.now(),
            size_bytes=5000000,
            reason="UPGRADE"
        )

        selector = BackupSelector(backup_dir=tmp_path / "backups")

        # Act
        formatted = selector.format_for_display(backup_info)

        # Assert
        assert "MB" in formatted or "5" in formatted

    def test_format_for_display_includes_reason(self, tmp_path):
        """
        Test: Formatted backup includes reason (UPGRADE, MANUAL, UNINSTALL) (AC#3, SVC-010).

        Given: A backup created during upgrade
        When: format_for_display() is called
        Then: Output includes reason "UPGRADE"
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        backup_info = BackupInfo(
            id="backup-001",
            version="1.0.0",
            timestamp=datetime.now(),
            size_bytes=5000000,
            reason="UPGRADE"
        )

        selector = BackupSelector(backup_dir=tmp_path / "backups")

        # Act
        formatted = selector.format_for_display(backup_info)

        # Assert
        assert "UPGRADE" in formatted

    def test_format_for_display_includes_path(self, tmp_path):
        """
        Test: Formatted backup includes backup path (AC#3, SVC-010).

        Given: A backup with known path
        When: format_for_display() is called
        Then: Output includes backup path
        """
        # Arrange
        from installer.backup_selector import BackupSelector
        from installer.models import BackupInfo

        backup_path = "backups/backup-001"
        backup_info = BackupInfo(
            id="backup-001",
            version="1.0.0",
            timestamp=datetime.now(),
            size_bytes=5000000,
            reason="UPGRADE",
            path=backup_path
        )

        selector = BackupSelector(backup_dir=tmp_path / "backups")

        # Act
        formatted = selector.format_for_display(backup_info)

        # Assert
        assert "backup-001" in formatted


class TestSelectBackup:
    """Test backup selection (AC#2, SVC-011)."""

    def test_select_backup_by_id_returns_correct_backup(self, tmp_path):
        """
        Test: Select backup by ID returns correct BackupInfo (AC#2, SVC-011).

        Given: Multiple backups exist
        When: select(backup_id="backup-002") is called
        Then: Returns backup with id="backup-002"
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 3 test backups
        for i in range(3):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
                "size_bytes": 1000000,
                "reason": "UPGRADE"
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        selected = selector.select("backup-001")

        # Assert
        assert selected is not None
        assert selected.id == "backup-001"

    def test_select_backup_invalid_id_returns_none(self, tmp_path):
        """
        Test: Select with invalid backup ID returns None (error handling).

        Given: Backup ID does not exist
        When: select(backup_id="invalid-id") is called
        Then: Returns None
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 1 test backup
        backup = backup_dir / "backup-001"
        backup.mkdir()
        metadata = {
            "id": "backup-001",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "size_bytes": 1000000,
            "reason": "UPGRADE"
        }
        (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        selected = selector.select("non-existent-backup")

        # Assert
        assert selected is None
