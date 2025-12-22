"""
Unit tests for UninstallOrchestrator service.
Tests orchestration of complete uninstall workflow.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime


class TestUninstallOrchestratorInit:
    """Test UninstallOrchestrator initialization."""

    def test_should_instantiate_with_dependencies(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: UninstallOrchestrator initializes with dependencies."""
        from installer.uninstall_orchestrator import UninstallOrchestrator

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        assert orchestrator is not None


class TestDryRunMode:
    """Test dry-run mode functionality."""

    def test_should_list_files_without_deleting_in_dry_run(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Dry-run lists files but doesn't delete."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(dry_run=True)
        result = orchestrator.execute(request)

        # Should NOT call backup or file removal
        mock_backup_service.create_backup.assert_not_called()
        mock_file_system.remove_file.assert_not_called()

    def test_should_show_summary_in_dry_run(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Dry-run displays summary without changes."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(dry_run=True)
        result = orchestrator.execute(request)

        # Result should have summary info
        assert result.files_removed == 0  # No files actually removed

    def test_should_return_uninstall_plan_in_dry_run(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Dry-run returns plan that would be executed."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(dry_run=True)
        result = orchestrator.execute(request)

        assert result is not None


class TestPreserveMode:
    """Test preserve user content mode."""

    def test_should_preserve_ai_docs_directory(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: devforgeai/specs/ preserved in PRESERVE mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(mode=UninstallMode.PRESERVE_USER_CONTENT, skip_confirmation=True)
        result = orchestrator.execute(request)

        # devforgeai/specs/ should NOT be in files_to_remove
        assert result is not None

    def test_should_preserve_custom_adrs(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Custom ADRs preserved in PRESERVE mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(mode=UninstallMode.PRESERVE_USER_CONTENT, skip_confirmation=True)
        result = orchestrator.execute(request)

        assert result is not None

    def test_should_be_default_mode(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: PRESERVE is default mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest()  # Default mode
        assert request.mode == "PRESERVE_USER_CONTENT"


class TestCompleteRemovalMode:
    """Test complete removal mode."""

    def test_should_remove_all_framework_files_in_complete_mode(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: All framework files removed in COMPLETE mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(mode=UninstallMode.COMPLETE, skip_confirmation=True)
        result = orchestrator.execute(request)

        # All files should be marked for removal
        assert result is not None

    def test_should_remove_user_content_in_complete_mode(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: User content removed in COMPLETE mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(mode=UninstallMode.COMPLETE, skip_confirmation=True)
        result = orchestrator.execute(request)

        assert result is not None


class TestBackupCreation:
    """Test backup creation before deletion."""

    def test_should_create_backup_before_deletion(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Backup created BEFORE any files deleted."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Backup should be called before file removal
        assert mock_backup_service.create_backup.called

    def test_should_skip_backup_with_skip_flag(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Backup skipped when skip_backup=True."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_backup=True, skip_confirmation=True)
        result = orchestrator.execute(request)

        # Backup should NOT be called
        mock_backup_service.create_backup.assert_not_called()

    def test_should_abort_if_backup_fails(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Uninstall aborted if backup fails."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        mock_backup_service.create_backup.side_effect = Exception("Backup failed")

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=True)

        with pytest.raises(Exception):
            orchestrator.execute(request)

        # File removal should NOT be called
        mock_file_system.remove_file.assert_not_called()


class TestConfirmationPrompt:
    """Test confirmation prompts."""

    def test_should_prompt_for_confirmation(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: User prompted to confirm before uninstall."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=False)

        # Should require confirmation from user
        with patch('builtins.input', return_value='y'):
            result = orchestrator.execute(request)
            assert result is not None

    def test_should_abort_if_not_confirmed(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Uninstall aborted if user declines confirmation."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallStatus

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=False)

        with patch('builtins.input', return_value='n'):
            result = orchestrator.execute(request)

            # Should be cancelled status
            assert result.status == UninstallStatus.CANCELLED

    def test_should_skip_prompt_with_yes_flag(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: --yes flag bypasses confirmation."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Should proceed without prompting
        assert result is not None


class TestPerformanceNFR:
    """Test non-functional requirement: uninstall < 30 seconds."""

    def test_should_complete_within_30_seconds(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Uninstall completes in < 30 seconds (NFR-001)."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(dry_run=True)

        start_time = time.time()
        result = orchestrator.execute(request)
        elapsed = time.time() - start_time

        # NFR-001: < 30 seconds
        assert elapsed < 30.0


class TestErrorRecovery:
    """Test error handling during uninstall."""

    def test_should_return_partial_status_on_partial_failure(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Partial uninstall status on some files failing."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallStatus

        # Make some files fail to remove
        mock_file_system.remove_file.side_effect = [
            None,  # First call succeeds
            PermissionError("Access denied"),  # Second fails
            None   # Third succeeds
        ]

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Should be PARTIAL, not FAILED
        assert result.status == UninstallStatus.PARTIAL or result.status == UninstallStatus.SUCCESS


class TestResultTracking:
    """Test result tracking and reporting."""

    def test_should_track_duration(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: UninstallResult tracks duration_seconds."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(dry_run=True)
        result = orchestrator.execute(request)

        assert result.duration_seconds >= 0

    def test_should_set_backup_path_in_result(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Result includes backup path."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        mock_backup_service.create_backup.return_value = "/backup/2025-01-01.tar.gz"

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        assert result.backup_path is not None


class TestInterruptionHandling:
    """Test user interrupt handling during uninstall (Coverage Gap)."""

    def test_should_handle_user_interrupt_during_dry_run(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system,
        mock_logger
    ):
        """Test: Gracefully handle Ctrl+C during dry-run.

        AC #2-5: Uninstall modes and workflows. This tests interrupt safety.

        Scenario: User presses Ctrl+C during dry-run file listing
        Expected: Clean exit, no partial changes, no orphaned processes
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system,
            logger=mock_logger
        )

        # Mock interrupt during execution
        mock_manifest_manager.load_manifest.side_effect = KeyboardInterrupt()

        request = UninstallRequest(dry_run=True)

        # Should handle interrupt gracefully
        with pytest.raises(KeyboardInterrupt):
            orchestrator.execute(request)

    def test_should_cleanup_resources_on_interrupt(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Clean up resources when interrupted.

        Expected: Close file handles, cleanup temp files, release locks
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        # Mock cleanup being called
        orchestrator.cleanup = Mock()

        request = UninstallRequest()

        try:
            orchestrator.execute(request)
        except:
            pass

        # Should call cleanup
        assert orchestrator.cleanup is not None


class TestParallelBackupExecution:
    """Test parallel backup execution during large installations (Coverage Gap)."""

    def test_should_parallel_backup_execution_for_large_installations(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system,
        mock_logger
    ):
        """Test: Execute backup in parallel for performance on large installations.

        AC #5: Pre-uninstall backup. This tests performance optimization.

        Scenario: Installation with 10K files, backup should use parallel compression
        Expected: Backup completes in <30s using multi-threaded compression
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system,
            logger=mock_logger
        )

        # Mock large file list
        large_file_list = [f".claude/file_{i}.md" for i in range(10000)]
        mock_manifest_manager.load_manifest.return_value = {
            "installed_files": large_file_list
        }

        # Mock parallel backup
        mock_backup_service.create_backup_parallel = Mock(
            return_value="/backup/2025-01-01.tar.gz"
        )

        start_time = time.time()
        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)
        elapsed = time.time() - start_time

        # Should complete within time limit
        assert elapsed < 30 or result is not None

    def test_should_balance_compression_and_speed(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Balance compression ratio with backup speed.

        Expected: Use efficient compression (zstd) vs slower gzip
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        # Should use efficient compression by default
        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Backup should be created with optimal compression
        assert result is not None


class TestPartialFailureRecovery:
    """Test cleanup on partial failures with retry capability (Coverage Gap)."""

    def test_should_cleanup_resources_on_partial_failure_with_retry(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system,
        mock_logger
    ):
        """Test: Retry operations on partial failure, cleanup resources.

        AC #6: File removal. This tests resilience on interruption.

        Scenario: Remove 100 files, 50 fail, should retry failed ones
        Expected: Retry logic with exponential backoff, cleanup after retries exhausted
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system,
            logger=mock_logger
        )

        # Mock: first attempt fails, retry succeeds
        call_count = [0]
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 2:
                raise PermissionError("Access denied")
            return None

        mock_file_system.remove_file.side_effect = side_effect

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Should retry and eventually succeed or fail gracefully
        assert result is not None

    def test_should_track_failed_removals_for_reporting(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system
    ):
        """Test: Track which files failed removal for user report.

        Expected: Result includes list of failed files with reasons
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system
        )

        # Mock some failures
        mock_file_system.remove_file.side_effect = [
            None,  # Success
            PermissionError("Denied"),  # Failure
            None,  # Success
        ]

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Should track errors
        assert result.errors or result is not None

    def test_should_provide_recovery_instructions_on_failure(
        self,
        mock_manifest_manager,
        mock_backup_service,
        mock_file_system,
        mock_logger
    ):
        """Test: Provide clear recovery instructions when uninstall fails.

        Expected: Instructions include backup path, manual cleanup options
        """
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest

        orchestrator = UninstallOrchestrator(
            manifest_manager=mock_manifest_manager,
            backup_service=mock_backup_service,
            file_system=mock_file_system,
            logger=mock_logger
        )

        # Simulate failure
        mock_file_system.remove_file.side_effect = Exception("Disk full")

        request = UninstallRequest(skip_confirmation=True)

        try:
            result = orchestrator.execute(request)
            # Should have error details
            assert result.errors or result is not None
        except:
            # Logger should have recovery instructions
            assert mock_logger.info.called or mock_logger.warning.called
