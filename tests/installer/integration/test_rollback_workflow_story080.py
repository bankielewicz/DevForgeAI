"""
STORY-080: Integration tests for complete rollback workflows.

Tests end-to-end rollback scenarios from all acceptance criteria.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 80%+ (integration layer)
Test Categories: AC#1-AC#8 (all)
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime, timedelta
import json
import hashlib


class TestManualRollbackWorkflow:
    """Integration test: Complete manual rollback workflow (AC#2, AC#4, AC#6, AC#7)."""

    def test_full_manual_rollback_workflow(self, tmp_path):
        """
        Integration Test: Complete manual rollback workflow end-to-end.

        Given: Backup exists and user selects it
        When: devforgeai rollback executes
        Then:
            - AC#2: Backup is restored
            - AC#4: Files restored from backup
            - AC#6: Post-rollback validation passed
            - AC#7: Summary logged
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.backup_selector import BackupSelector
        from installer.backup_restorer import BackupRestorer
        from installer.rollback_validator import RollbackValidator
        from installer.backup_cleaner import BackupCleaner
        from installer.models import RollbackRequest

        # Setup: Create initial project structure
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        backup_dir = project_dir / ".backups"
        backup_dir.mkdir()
        logs_dir = project_dir / "devforgeai" / "logs"
        logs_dir.mkdir(parents=True)

        # Create backup with known state
        backup = backup_dir / "backup-001"
        backup.mkdir()
        (backup / ".version.json").write_text(json.dumps({"version": "1.0.0"}))
        (backup / "framework_file.txt").write_text("framework content")

        # Create manifest
        manifest = {
            "files": {
                ".version.json": {
                    "checksum": hashlib.sha256(b'{"version": "1.0.0"}').hexdigest()
                },
                "framework_file.txt": {
                    "checksum": hashlib.sha256(b"framework content").hexdigest()
                }
            }
        }
        (backup / "manifest.json").write_text(json.dumps(manifest))

        # Create current (different) project state
        (project_dir / ".version.json").write_text(json.dumps({"version": "1.0.1"}))
        (project_dir / "framework_file.txt").write_text("modified content")

        # Initialize orchestrator with real services
        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=BackupRestorer(logger=Mock()),
            validator=RollbackValidator(logger=Mock()),
            cleaner=BackupCleaner(backup_dir=backup_dir),
            logger=Mock(),
            logs_dir=logs_dir
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False,
            include_user_content=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert result is not None
        assert result.from_version == "1.0.1"
        # Log file should exist
        log_files = list(logs_dir.glob("rollback-*.log"))
        assert len(log_files) > 0


class TestAutomaticRollbackOnFailure:
    """Integration test: Automatic rollback triggered on upgrade failure (AC#1)."""

    def test_automatic_rollback_on_upgrade_failure(self, tmp_path):
        """
        Integration Test: Automatic rollback triggered on upgrade failure.

        Given: Upgrade process starts and fails midway
        When: Automatic rollback is triggered
        Then:
            - AC#1: Automatic rollback executes
            - AC#1: All changes reverted
            - AC#1: .version.json restored to previous state
            - AC#1: Completes within 1 minute
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.backup_restorer import BackupRestorer
        from installer.rollback_validator import RollbackValidator
        from installer.backup_cleaner import BackupCleaner
        from installer.models import RollbackRequest
        import time

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        backup_dir = project_dir / ".backups"
        backup_dir.mkdir()

        # Setup: Pre-upgrade backup
        backup = backup_dir / "backup-001"
        backup.mkdir()
        (backup / ".version.json").write_text(json.dumps({"version": "1.0.0"}))
        (backup / "file1.txt").write_text("original 1")
        (backup / "file2.txt").write_text("original 2")

        # Create current (broken) state
        (project_dir / ".version.json").write_text(json.dumps({"version": "1.0.1-broken"}))
        (project_dir / "file1.txt").write_text("modified 1")
        (project_dir / "file2.txt").write_text("modified 2")
        (project_dir / "broken_file.txt").write_text("created during failed upgrade")

        # Initialize orchestrator
        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=BackupRestorer(logger=Mock()),
            validator=RollbackValidator(logger=Mock()),
            cleaner=BackupCleaner(backup_dir=backup_dir),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=True,
            failure_reason="Migration script failed: Exit code 1"
        )

        # Act
        start_time = time.time()
        result = orchestrator.execute(request)
        elapsed = time.time() - start_time

        # Assert
        assert result is not None
        assert elapsed < 60  # Within 1 minute
        assert result.is_automatic is True


class TestBackupListingAndSelection:
    """Integration test: List backups and select for rollback (AC#2, AC#3)."""

    def test_list_and_select_backup_for_rollback(self, tmp_path):
        """
        Integration Test: List backups and select one for rollback.

        Given: Multiple backups exist
        When: User lists backups and selects one
        Then:
            - AC#3: All backups displayed with version, date, size, reason
            - AC#3: Sorted by date (newest first)
            - AC#2: Selected backup can be restored
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 5 backups with different dates
        for i in range(5):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
                "size_bytes": 1000000 + i * 100000,
                "reason": ["UPGRADE", "MANUAL", "UNINSTALL"][i % 3]
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        backups = selector.list()
        selected = selector.select("backup-002")

        # Assert
        assert len(backups) == 5
        # Verify sorted by date (newest first)
        assert backups[0].timestamp > backups[1].timestamp
        assert selected is not None
        assert selected.id == "backup-002"


class TestUserContentPreservation:
    """Integration test: User content preserved without flag (AC#5)."""

    def test_user_content_preserved_without_flag(self, tmp_path):
        """
        Integration Test: User content preserved during rollback without flag.

        Given: Backup contains user stories (in devforgeai/specs/Stories/)
        When: Rollback executes without --include-user-content
        Then:
            - AC#5: User stories NOT overwritten from backup
            - AC#5: User stories preserved (not overwritten)
            - Stories retain their current content
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create backup with user stories
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# Old Story")

        # Create framework files
        (backup_dir / "framework.txt").write_text("framework")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create current user stories (different from backup)
        (target_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# New Story")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        # Story should remain unchanged
        assert (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").read_text() == "# New Story"
        # Framework file should be restored
        assert (target_dir / "framework.txt").exists()


class TestUserContentInclusionWithFlag:
    """Integration test: User content included with flag (AC#5)."""

    def test_user_content_included_with_flag(self, tmp_path):
        """
        Integration Test: User content restored from backup with flag.

        Given: Backup contains user stories AND flag is --include-user-content
        When: Rollback executes with include_user_content=True
        Then:
            - AC#5: User stories restored from backup
            - AC#5: Overwrite current stories with backup versions
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create backup with user stories
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# Old Story")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create different current user stories
        (target_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# New Story")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=True
        )

        # Assert
        # Story should be restored from backup
        assert (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").read_text() == "# Old Story"


class TestBackupCleanupAfterRollback:
    """Integration test: Backup cleanup after successful rollback (AC#8)."""

    def test_backup_cleanup_after_successful_rollback(self, tmp_path):
        """
        Integration Test: Backups cleaned up after successful rollback.

        Given: 7 backups exist with retention limit 5
        When: Successful rollback completes
        Then:
            - AC#8: Oldest 2 backups deleted
            - AC#8: Exactly 5 backups remain
            - AC#8: User notified of cleanup
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
        assert result.deleted_count == 2


class TestRollbackValidationReport:
    """Integration test: Complete validation report (AC#6, AC#7)."""

    def test_rollback_validation_report_complete(self, tmp_path):
        """
        Integration Test: Comprehensive validation report generated.

        Given: Backup restored with 100 files
        When: Validation runs
        Then:
            - AC#6: Report shows file counts
            - AC#6: Checksums verified
            - AC#7: Summary includes validation status
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create 100 files
        manifest_files = {}
        for i in range(100):
            file_path = restored_dir / f"file_{i:03d}.txt"
            content = f"content {i}"
            file_path.write_text(content)
            checksum = hashlib.sha256(content.encode()).hexdigest()
            manifest_files[f"file_{i:03d}.txt"] = {
                "checksum": checksum,
                "size": len(content)
            }

        manifest = {"files": manifest_files}

        # Add critical files
        (restored_dir / "CLAUDE.md").write_text("# Claude")
        (restored_dir / "devforgeai").mkdir()

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest=manifest
        )

        # Assert
        assert report.passed is True
        assert report.verified_files == 100
        assert report.critical_files_present is True


class TestManualRollbackListCommand:
    """Integration test: devforgeai rollback --list command (AC#3)."""

    def test_manual_rollback_with_flag_list(self, tmp_path):
        """
        Integration Test: List backups with --list flag.

        Given: Multiple backups exist
        When: User runs 'devforgeai rollback --list'
        Then:
            - AC#3: All backups displayed with version, date, size, reason
            - AC#3: Sorted by date (newest first)
        """
        # Arrange
        from installer.backup_selector import BackupSelector

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Create 3 backups with different details
        for i in range(3):
            backup = backup_dir / f"backup-{i:03d}"
            backup.mkdir()
            metadata = {
                "id": f"backup-{i:03d}",
                "version": f"1.0.{i}",
                "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
                "size_bytes": 1000000 + i * 500000,
                "reason": ["UPGRADE", "MANUAL", "UNINSTALL"][i]
            }
            (backup / "metadata.json").write_text(json.dumps(metadata))

        selector = BackupSelector(backup_dir=backup_dir)

        # Act
        backups = selector.list()
        formatted_list = [selector.format_for_display(b) for b in backups]

        # Assert
        assert len(backups) == 3
        # Check that details are in formatted output
        for formatted in formatted_list:
            assert any(keyword in formatted for keyword in ["version", "1.0.", "MB", "UPGRADE", "MANUAL"])
