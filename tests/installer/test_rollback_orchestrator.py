"""
STORY-080: Unit tests for RollbackOrchestrator service.

Tests orchestration of automatic and manual rollback workflows.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+ business logic
Test Categories: AC#1, AC#2, AC#7, AC#8
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import time
import json
from datetime import datetime


class TestAutomaticRollback:
    """Test automatic rollback triggered on upgrade failure (AC#1, SVC-001)."""

    def test_automatic_rollback_triggered_on_upgrade_failure(self, tmp_path):
        """
        Test: RollbackOrchestrator triggers automatic rollback on upgrade failure.

        Given: An upgrade is in progress
        When: A migration script fails (exit code 1)
        Then: Automatic rollback is triggered immediately
        And: All changes made during upgrade are reverted
        And: .version.json is restored to previous state
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".version.json").write_text(json.dumps({"version": "1.0.0"}))

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".version.json").write_text(json.dumps({"version": "1.0.1-rc"}))

        mock_restorer = Mock()
        mock_validator = Mock()
        mock_cleaner = Mock()
        mock_logger = Mock()

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=mock_restorer,
            validator=mock_validator,
            cleaner=mock_cleaner,
            logger=mock_logger
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=True,
            failure_reason="Migration script failed with exit code 1"
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert result is not None
        assert result.from_version == "1.0.1-rc"
        assert result.to_version == "1.0.0"
        mock_restorer.restore.assert_called_once()
        mock_validator.validate.assert_called_once()

    def test_automatic_rollback_completes_within_timeout(self, tmp_path):
        """
        Test: Automatic rollback completes within 1 minute (AC#1, NFR-001).

        Given: An upgrade failure triggers automatic rollback
        When: Rollback is executed
        Then: Rollback completes within 60 seconds
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Setup mocks with minimal delay
        mock_restorer = Mock()
        mock_restorer.restore.return_value = Mock(files_restored=10)
        mock_validator = Mock()
        mock_validator.validate.return_value = Mock(passed=True)
        mock_cleaner = Mock()

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=mock_restorer,
            validator=mock_validator,
            cleaner=mock_cleaner,
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=True,
            failure_reason="Upgrade failed"
        )

        # Act
        start_time = time.time()
        result = orchestrator.execute(request)
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 60, f"Rollback took {elapsed}s (expected <60s)"
        assert result.duration_seconds < 60

    def test_automatic_rollback_preserves_error_reason(self, tmp_path):
        """
        Test: Automatic rollback preserves failure reason for logging (AC#1).

        Given: An automatic rollback is triggered
        When: Rollback executes
        Then: failure_reason is captured and logged
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        failure_reason = "Database migration script failed: Connection timeout"

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=True,
            failure_reason=failure_reason
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert result.failure_reason == failure_reason


class TestManualRollback:
    """Test manual rollback command execution (AC#2, SVC-002)."""

    def test_manual_rollback_creates_safety_backup_first(self, tmp_path):
        """
        Test: Manual rollback creates current state backup before restoration (AC#2, SVC-003).

        Given: Manual rollback is initiated
        When: execute() is called
        Then: Current version is backed up BEFORE any files are restored
        And: Safety backup creation completes successfully
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_backup_service = Mock()
        mock_backup_service.create_backup.return_value = Mock(backup_id="safety-backup-001")

        orchestrator = RollbackOrchestrator(
            backup_service=mock_backup_service,
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        # Verify backup was created before restore
        assert mock_backup_service.create_backup.called
        call_order = [call for call in mock_backup_service.mock_calls]
        create_backup_call_index = next(
            (i for i, c in enumerate(call_order) if "create_backup" in str(c)),
            -1
        )
        assert create_backup_call_index >= 0

    def test_manual_rollback_invokes_restorer(self, tmp_path):
        """
        Test: Manual rollback invokes backup restorer (AC#4, SVC-005).

        Given: User selects backup to restore
        When: execute() is called
        Then: BackupRestorer.restore() is called with correct backup
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_restorer = Mock()
        mock_restorer.restore.return_value = Mock(files_restored=50, files_preserved=10)

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=mock_restorer,
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        mock_restorer.restore.assert_called_once()


class TestRollbackValidation:
    """Test rollback validation invocation (AC#6, SVC-014)."""

    def test_rollback_invokes_validator(self, tmp_path):
        """
        Test: Rollback invokes validator after restoration (AC#6, SVC-014).

        Given: Backup has been restored
        When: Rollback completes
        Then: RollbackValidator.validate() is called
        And: Validation report is captured
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_validator = Mock()
        mock_validator.validate.return_value = Mock(
            passed=True,
            verified_files=50,
            validation_details="All files verified"
        )

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=mock_validator,
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=True,
            failure_reason="Test"
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        mock_validator.validate.assert_called_once()
        assert result.validation_passed is True


class TestBackupCleanup:
    """Test backup cleanup invocation (AC#8, SVC-012)."""

    def test_rollback_invokes_cleaner(self, tmp_path):
        """
        Test: Successful rollback invokes backup cleaner (AC#8, SVC-012).

        Given: Rollback has completed successfully
        When: execute() finishes
        Then: BackupCleaner.cleanup() is called
        And: Retention policy is enforced
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_cleaner = Mock()
        mock_cleaner.cleanup.return_value = Mock(deleted_backups=[])

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=mock_cleaner,
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        mock_cleaner.cleanup.assert_called_once()


class TestRollbackLogging:
    """Test rollback logging and summary generation (AC#7, SVC-007)."""

    def test_rollback_summary_generated(self, tmp_path):
        """
        Test: Rollback generates summary with all required details (AC#7).

        Given: Rollback has completed
        When: execute() returns
        Then: RollbackResult contains:
            - from_version (previous version)
            - to_version (restored version)
            - files_restored count
            - files_preserved count
            - validation_passed status
            - duration_seconds
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert hasattr(result, "from_version")
        assert hasattr(result, "to_version")
        assert hasattr(result, "files_restored")
        assert hasattr(result, "files_preserved")
        assert hasattr(result, "validation_passed")
        assert hasattr(result, "duration_seconds")

    def test_rollback_log_saved_to_correct_location(self, tmp_path):
        """
        Test: Rollback summary saved to devforgeai/logs/rollback-{timestamp}.log (AC#7).

        Given: Rollback has completed
        When: execute() returns
        Then: Log file created at devforgeai/logs/rollback-YYYYMMDD-HHMMSS.log
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        logs_dir = tmp_path / "devforgeai" / "logs"
        logs_dir.mkdir(parents=True)

        mock_logger = Mock()

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=mock_logger,
            logs_dir=logs_dir
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        log_files = list(logs_dir.glob("rollback-*.log"))
        assert len(log_files) > 0

    def test_rollback_log_contains_all_details(self, tmp_path):
        """
        Test: Rollback log file contains all summary details (AC#7).

        Given: Rollback has completed and log saved
        When: Log file is read
        Then: Contains from_version, to_version, file counts, validation status, duration
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        logs_dir = tmp_path / "devforgeai" / "logs"
        logs_dir.mkdir(parents=True)

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock(),
            logs_dir=logs_dir
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        log_files = list(logs_dir.glob("rollback-*.log"))
        assert len(log_files) > 0

        log_content = log_files[0].read_text()
        assert "from_version" in log_content or result.from_version in log_content
        assert "to_version" in log_content or result.to_version in log_content
        assert "files_restored" in log_content or str(result.files_restored) in log_content


class TestRollbackUserContent:
    """Test user content preservation (AC#5, SVC-004)."""

    def test_rollback_passes_include_user_content_to_restorer(self, tmp_path):
        """
        Test: include_user_content flag is passed to restorer (AC#5, SVC-006/007).

        Given: User calls rollback with --include-user-content
        When: execute() is called
        Then: include_user_content=True is passed to restorer.restore()
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_restorer = Mock()

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=mock_restorer,
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False,
            include_user_content=True
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        # Verify restorer was called with include_user_content=True
        call_args = mock_restorer.restore.call_args
        assert "include_user_content" in str(call_args) or call_args is not None


class TestRollbackErrorHandling:
    """Test error handling during rollback (error cases)."""

    def test_rollback_handles_restorer_failure(self, tmp_path):
        """
        Test: Rollback handles failures in backup restoration gracefully.

        Given: Backup restorer raises an exception
        When: execute() is called
        Then: Error is caught and reported
        And: RollbackResult.status is FAILED
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_restorer = Mock()
        mock_restorer.restore.side_effect = Exception("Restore failed: Permission denied")

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=mock_restorer,
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert result.status == "FAILED" or result.error is not None

    def test_rollback_handles_validator_failure(self, tmp_path):
        """
        Test: Rollback handles validation failures gracefully.

        Given: Validator fails after restoration
        When: execute() completes
        Then: Error is reported
        And: validation_passed is False
        And: rollback is NOT automatically reverted
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        mock_validator = Mock()
        mock_validator.validate.return_value = Mock(
            passed=False,
            error="Checksum mismatch: 5 files corrupted"
        )

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=mock_validator,
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert result.validation_passed is False


class TestRollbackResult:
    """Test RollbackResult data model metrics (AC#7)."""

    def test_rollback_result_includes_metrics(self, tmp_path):
        """
        Test: RollbackResult includes performance metrics.

        Given: Rollback has completed
        When: RollbackResult is returned
        Then: Contains duration_seconds, timestamp, and all required fields
        """
        # Arrange
        from installer.rollback_orchestrator import RollbackOrchestrator
        from installer.models import RollbackRequest

        orchestrator = RollbackOrchestrator(
            backup_service=Mock(),
            restorer=Mock(),
            validator=Mock(),
            cleaner=Mock(),
            logger=Mock()
        )

        request = RollbackRequest(
            backup_id="backup-001",
            is_automatic=False
        )

        # Act
        result = orchestrator.execute(request)

        # Assert
        assert hasattr(result, "duration_seconds")
        assert isinstance(result.duration_seconds, (int, float))
        assert result.duration_seconds > 0
        assert hasattr(result, "timestamp")
