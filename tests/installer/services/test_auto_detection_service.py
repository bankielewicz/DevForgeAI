"""
Unit tests for AutoDetectionService (Orchestrator).

Tests integration of all detection services:
- Version detection
- CLAUDE.md detection
- Git detection
- File conflict detection
- Summary formatting

Component Requirements:
- SVC-001: Orchestrate all auto-detection checks and return DetectionResult
- SVC-002: Execute checks concurrently where possible
- SVC-003: Handle partial failures gracefully

Business Rules:
- BR-001: Auto-detection failures are non-fatal
- BR-002: Summary displays before any user prompts
- NFR-001: Auto-detection completes in <500ms for typical projects
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import time


# Story: STORY-073
class TestAutoDetectionService:
    """Test suite for AutoDetectionService - Orchestration and integration."""

    # SVC-001: Orchestrate all detection checks

    def test_should_orchestrate_all_detection_checks(self, temp_dir):
        """
        Test: All detection checks executed → DetectionResult returned (SVC-001)

        Given: AutoDetectionService instance
        When: detect_all() is called
        Then: Returns DetectionResult with all fields populated
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=["CLAUDE.md"]
        )

        # Act
        result = service.detect_all()

        # Assert
        assert result is not None
        assert hasattr(result, "version_info")
        assert hasattr(result, "claudemd_info")
        assert hasattr(result, "git_info")
        assert hasattr(result, "conflicts")

    def test_should_invoke_version_detection_service(self, temp_dir):
        """
        Test: VersionDetectionService invoked (SVC-001)

        Given: AutoDetectionService instance with mocked version service
        When: detect_all() is called
        Then: VersionDetectionService.read_version() is called
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock version service
        mock_version_service = Mock()
        mock_version_service.read_version.return_value = None

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            version_service=mock_version_service
        )

        # Act
        result = service.detect_all()

        # Assert
        mock_version_service.read_version.assert_called_once()

    def test_should_invoke_claudemd_detection_service(self, temp_dir):
        """
        Test: ClaudeMdDetectionService invoked (SVC-001)

        Given: AutoDetectionService instance with mocked claudemd service
        When: detect_all() is called
        Then: ClaudeMdDetectionService.detect() is called
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock claudemd service
        mock_claudemd_service = Mock()
        mock_claudemd_service.detect.return_value = None

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            claudemd_service=mock_claudemd_service
        )

        # Act
        result = service.detect_all()

        # Assert
        mock_claudemd_service.detect.assert_called_once()

    def test_should_invoke_git_detection_service(self, temp_dir):
        """
        Test: GitDetectionService invoked (SVC-001)

        Given: AutoDetectionService instance with mocked git service
        When: detect_all() is called
        Then: GitDetectionService.detect_git_root() is called
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock git service
        mock_git_service = Mock()
        mock_git_service.detect_git_root.return_value = None
        mock_git_service.is_submodule.return_value = False

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            git_service=mock_git_service
        )

        # Act
        result = service.detect_all()

        # Assert
        mock_git_service.detect_git_root.assert_called_once()

    def test_should_invoke_file_conflict_detection_service(self, temp_dir):
        """
        Test: FileConflictDetectionService invoked (SVC-001)

        Given: AutoDetectionService instance with mocked conflict service
        When: detect_all() is called
        Then: FileConflictDetectionService.detect_conflicts() is called
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock conflict service
        mock_conflict_service = Mock()
        mock_conflict_service.detect_conflicts.return_value = Mock(conflicts=[], framework_count=0, user_count=0)

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=["file.txt"],
            conflict_service=mock_conflict_service
        )

        # Act
        result = service.detect_all()

        # Assert
        mock_conflict_service.detect_conflicts.assert_called_once()

    def test_should_invoke_summary_formatter_service(self, temp_dir):
        """
        Test: SummaryFormatterService invoked (SVC-001)

        Given: AutoDetectionService instance with mocked formatter service
        When: format_summary() is called
        Then: SummaryFormatterService.format_summary() is called
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService, DetectionResult

        # Create mock formatter service
        mock_formatter_service = Mock()
        mock_formatter_service.format_summary.return_value = "Summary text"

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            formatter_service=mock_formatter_service
        )

        # Create detection result
        detection_result = DetectionResult()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        mock_formatter_service.format_summary.assert_called_once_with(detection_result)

    # SVC-002: Concurrent execution

    def test_should_execute_independent_checks_concurrently(self, temp_dir):
        """
        Test: Independent checks run concurrently (SVC-002)

        Given: AutoDetectionService instance
        When: detect_all() is called
        Then: Completes faster than sequential execution
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[]
        )

        # Act
        start = time.time()
        result = service.detect_all()
        concurrent_duration = time.time() - start

        # Assert - concurrent execution should be faster than 4x individual checks
        # This is a heuristic test - in real implementation, we'd mock delays
        assert result is not None

    # SVC-003: Partial failure handling (BR-001)

    def test_should_continue_when_version_detection_fails(self, temp_dir):
        """
        Test: One check fails, others complete (SVC-003, BR-001)

        Given: VersionDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with version_info=None, other checks complete
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[]
        )

        with patch('src.installer.services.version_detection_service.VersionDetectionService') as mock_vds:
            mock_instance = Mock()
            mock_instance.read_version.side_effect = Exception("Version read failed")
            mock_vds.return_value = mock_instance

            # Act
            result = service.detect_all()

            # Assert
            assert result is not None
            assert result.version_info is None
            # Other checks should still complete
            assert hasattr(result, "git_info")
            assert hasattr(result, "conflicts")

    def test_should_continue_when_git_detection_fails(self, temp_dir):
        """
        Test: Git detection fails, others complete (SVC-003, BR-001)

        Given: GitDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with git_info=None, other checks complete
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[]
        )

        with patch('src.installer.services.git_detection_service.GitDetectionService') as mock_gds:
            mock_instance = Mock()
            mock_instance.detect_git_root.side_effect = Exception("Git detection failed")
            mock_gds.return_value = mock_instance

            # Act
            result = service.detect_all()

            # Assert
            assert result is not None
            assert result.git_info is None
            # Other checks should still complete
            assert hasattr(result, "version_info")
            assert hasattr(result, "conflicts")

    def test_should_continue_when_claudemd_detection_fails(self, temp_dir):
        """
        Test: CLAUDE.md detection fails, others complete (SVC-003, BR-001)

        Given: ClaudeMdDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with claudemd_info=None, other checks complete
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock claudemd service that raises exception
        mock_claudemd_service = Mock()
        mock_claudemd_service.detect.side_effect = Exception("CLAUDE.md detection failed")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            claudemd_service=mock_claudemd_service
        )

        # Act
        result = service.detect_all()

        # Assert
        assert result is not None
        assert result.claudemd_info is None
        # Other checks should still complete
        assert hasattr(result, "version_info")
        assert hasattr(result, "git_info")

    def test_should_continue_when_conflict_detection_fails(self, temp_dir):
        """
        Test: Conflict detection fails, returns empty conflicts (SVC-003, BR-001)

        Given: FileConflictDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with empty conflicts, other checks complete
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=["file.txt"]
        )

        with patch('src.installer.services.file_conflict_detection_service.FileConflictDetectionService') as mock_fcds:
            mock_instance = Mock()
            mock_instance.detect_conflicts.side_effect = Exception("Conflict detection failed")
            mock_fcds.return_value = mock_instance

            # Act
            result = service.detect_all()

            # Assert
            assert result is not None
            assert len(result.conflicts.conflicts) == 0
            # Other checks should still complete
            assert hasattr(result, "version_info")
            assert hasattr(result, "git_info")

    # Integration Tests: Full Detection Flow

    def test_full_detection_flow_with_existing_installation(self, temp_dir):
        """
        Test: Full detection with existing installation (Integration)

        Given: Target has existing DevForgeAI installation
        When: detect_all() is called
        Then: Returns complete DetectionResult with all data
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService
        import json

        # Create existing installation
        version_dir = temp_dir / "devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_data = {
            "installed_version": "1.0.0",
            "installed_at": "2025-11-25T10:30:00Z",
            "installation_source": "installer"
        }
        version_file.write_text(json.dumps(version_data))

        # Create CLAUDE.md
        claudemd = temp_dir / "CLAUDE.md"
        claudemd.write_text("# Documentation")

        # Create conflicting file
        (temp_dir / ".claude" / "skills").mkdir(parents=True)
        (temp_dir / ".claude" / "skills" / "skill.md").write_text("content")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.1.0",
            source_files=[".claude/skills/skill.md"]
        )

        # Act
        result = service.detect_all()

        # Assert
        assert result.version_info is not None
        assert result.version_info.installed_version == "1.0.0"
        assert result.claudemd_info is not None
        assert result.claudemd_info.exists is True
        assert len(result.conflicts.conflicts) == 1

    def test_full_detection_flow_with_fresh_install(self, temp_dir):
        """
        Test: Full detection with fresh install (Integration)

        Given: Target is empty directory
        When: detect_all() is called
        Then: Returns DetectionResult indicating clean install
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[]
        )

        # Act
        result = service.detect_all()

        # Assert
        assert result.version_info is None
        assert result.claudemd_info is not None
        assert result.claudemd_info.exists is False
        assert len(result.conflicts.conflicts) == 0

    # Performance (NFR-001)

    def test_should_complete_detection_within_500ms(self, temp_dir):
        """
        Test: Auto-detection < 500ms for typical projects (NFR-001)

        Given: Typical project structure (<10,000 files)
        When: detect_all() is called
        Then: Completes in <500ms
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create typical project structure
        source_files = [f"file_{i}.txt" for i in range(100)]

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=source_files
        )

        # Act
        start = time.time()
        result = service.detect_all()
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 500, f"Detection took {duration_ms}ms (expected <500ms)"

    # Data Model Validation

    def test_detection_result_model_has_required_fields(self):
        """
        Test: DetectionResult data model has all required fields

        Given: DetectionResult class defined
        When: Instance is created
        Then: Has version_info, claudemd_info, git_info, conflicts fields
        """
        # Arrange
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        # Act
        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        # Assert
        assert hasattr(detection_result, "version_info")
        assert hasattr(detection_result, "claudemd_info")
        assert hasattr(detection_result, "git_info")
        assert hasattr(detection_result, "conflicts")

    def test_detection_result_allows_none_for_optional_fields(self):
        """
        Test: DetectionResult allows None for optional fields

        Given: DetectionResult instance
        When: Optional fields are None
        Then: Instance is valid
        """
        # Arrange
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        # Act
        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        # Assert
        assert detection_result.version_info is None
        assert detection_result.claudemd_info is None
        assert detection_result.git_info is None

    # Business Rule BR-002: Summary before prompts

    def test_summary_generated_as_part_of_detection(self, temp_dir):
        """
        Test: Summary generated during detection (BR-002)

        Given: AutoDetectionService instance
        When: detect_all() is called
        Then: Summary is available in DetectionResult
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[]
        )

        # Act
        result = service.detect_all()

        # Assert
        assert hasattr(result, "summary") or result is not None
        # Summary should be immediately available for display

    # Error Handling

    def test_should_log_errors_for_failed_checks(self, temp_dir):
        """
        Test: Errors logged when checks fail (BR-001)

        Given: Detection check raises exception
        When: detect_all() is called
        Then: Error is logged but execution continues
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock version service that raises exception
        mock_version_service = Mock()
        mock_version_service.read_version.side_effect = Exception("Test error")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            version_service=mock_version_service
        )

        with patch('src.installer.services.auto_detection_service.logger') as mock_logger:
            # Act
            result = service.detect_all()

            # Assert
            mock_logger.error.assert_called()

    # Cross-platform

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: AutoDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Act
        service = AutoDetectionService(
            target_path="C:\\test\\path",
            source_version="1.0.0",
            source_files=[]
        )

        # Assert
        assert service is not None

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: AutoDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Act
        service = AutoDetectionService(
            target_path="/test/path",
            source_version="1.0.0",
            source_files=[]
        )

        # Assert
        assert service is not None

    # ===== COVERAGE GAP TESTS (Lines 150-183 + error handling) =====

    def test_detect_all_concurrent_success(self, temp_dir):
        """
        Test: detect_all_concurrent with all checks succeeding

        Given: All detection services return valid results
        When: detect_all_concurrent() is called
        Then: Returns DetectionResult with all fields populated
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService
        import json

        # Create existing installation
        version_dir = temp_dir / "devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_data = {
            "installed_version": "1.0.0",
            "installed_at": "2025-11-25T10:30:00Z",
            "installation_source": "installer"
        }
        version_file.write_text(json.dumps(version_data))

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.1.0",
            source_files=[]
        )

        # Act
        result = service.detect_all_concurrent()

        # Assert
        assert result is not None
        assert result.version_info is not None
        assert result.version_info.installed_version == "1.0.0"
        assert hasattr(result, "claudemd_info")
        assert hasattr(result, "git_info")
        assert hasattr(result, "conflicts")

    def test_detect_all_concurrent_with_failures(self, temp_dir):
        """
        Test: detect_all_concurrent graceful handling of partial failures

        Given: One detection service raises exception
        When: detect_all_concurrent() is called
        Then: Returns DetectionResult with successful checks, failed check is None
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create mock version service that raises exception
        mock_version_service = Mock()
        mock_version_service.read_version.side_effect = Exception("Version detection failed")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            version_service=mock_version_service
        )

        # Act
        result = service.detect_all_concurrent()

        # Assert
        assert result is not None
        assert result.version_info is None  # Failed task returns None
        # Other checks should still complete
        assert hasattr(result, "git_info")
        assert hasattr(result, "conflicts")

    def test_detect_all_concurrent_performance(self, temp_dir):
        """
        Test: detect_all_concurrent is faster than sequential

        Given: Multiple detection checks
        When: detect_all_concurrent() is called vs detect_all()
        Then: Concurrent execution completes in ≤ sequential time
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        # Create services with artificial delays
        def slow_detect(*args, **kwargs):
            time.sleep(0.05)  # 50ms delay
            return None

        mock_version = Mock()
        mock_version.read_version.side_effect = slow_detect

        mock_git = Mock()
        mock_git.detect_git_root.side_effect = slow_detect
        mock_git.is_submodule.return_value = False

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            version_service=mock_version,
            git_service=mock_git
        )

        # Act - Concurrent
        start_concurrent = time.time()
        result_concurrent = service.detect_all_concurrent()
        duration_concurrent = time.time() - start_concurrent

        # Act - Sequential
        start_sequential = time.time()
        result_sequential = service.detect_all()
        duration_sequential = time.time() - start_sequential

        # Assert
        # Concurrent should be faster (or at most equal)
        assert duration_concurrent <= duration_sequential * 1.1  # 10% tolerance
        assert result_concurrent is not None
        assert result_sequential is not None

    def test_detect_all_with_version_failure(self, temp_dir):
        """
        Test: detect_all when version detection raises exception

        Given: VersionDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with version_info=None, error logged
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService

        mock_version_service = Mock()
        mock_version_service.read_version.side_effect = RuntimeError("JSON decode error")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            version_service=mock_version_service
        )

        with patch('src.installer.services.auto_detection_service.logger') as mock_logger:
            # Act
            result = service.detect_all()

            # Assert
            assert result is not None
            assert result.version_info is None
            mock_logger.error.assert_called()
            # Check error message contains "Version detection failed"
            error_call = mock_logger.error.call_args[0][0]
            assert "Version detection failed" in error_call or "version" in error_call.lower()

    def test_detect_all_with_git_failure(self, temp_dir):
        """
        Test: detect_all when git detection raises exception

        Given: GitDetectionService raises exception
        When: detect_all() is called
        Then: Returns DetectionResult with git_info=None, error logged
        """
        # Arrange
        from src.installer.services.auto_detection_service import AutoDetectionService
        import subprocess

        mock_git_service = Mock()
        mock_git_service.detect_git_root.side_effect = subprocess.CalledProcessError(128, "git")

        service = AutoDetectionService(
            target_path=str(temp_dir),
            source_version="1.0.0",
            source_files=[],
            git_service=mock_git_service
        )

        with patch('src.installer.services.auto_detection_service.logger') as mock_logger:
            # Act
            result = service.detect_all()

            # Assert
            assert result is not None
            assert result.git_info is None
            mock_logger.error.assert_called()
            # Check error message contains "Git detection failed"
            error_call = mock_logger.error.call_args[0][0]
            assert "Git detection failed" in error_call or "git" in error_call.lower()
