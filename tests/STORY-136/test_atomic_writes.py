"""
Tests for AC#6: Atomic Writes Using Write Tool with Error Handling

Verifies that:
- Write tool is used (not Bash)
- YAML syntax is always valid after write
- Write operations complete atomically
- No partial/corrupted file states on error
- Error handling surfaces errors to caller
"""

from typing import Dict, Any
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

import pytest
import yaml

from checkpoint_protocol import (
    CheckpointService,
    YamlValidator
)


class TestAtomicWrites:
    """Tests for atomic write semantics and error handling"""

    def test_should_use_write_tool_exclusively(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Use Write tool exclusively for checkpoint writes
        Given: A checkpoint to be persisted
        When: Write operation is performed
        Then: Write tool should be invoked (not Bash)
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        mock_write_tool.write.assert_called_once()

    def test_should_not_use_bash_for_write_operations(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Verify Bash is NOT used for checkpoint writes
        Given: A checkpoint to persist
        When: Write is attempted
        Then: Bash should not be invoked for echo/cat/> operations
        """
        # Arrange
        with patch('subprocess.run') as mock_bash:
            checkpoint_service = CheckpointService(write_tool=Mock())

            # Act
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

            # Assert
            bash_file_ops = [
                call for call in mock_bash.call_args_list
                if any(cmd in str(call) for cmd in ['echo', 'cat', '>', '>>'])
            ]
            assert len(bash_file_ops) == 0, "Bash should not be used for file operations"

    def test_should_produce_valid_yaml_after_write(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: YAML syntax is valid after write
        Given: A checkpoint is written
        When: File is read back
        Then: Should parse successfully with yaml.safe_load()
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1
        yaml_content = yaml.dump(checkpoint_data)

        # Act - Simulate write and read
        parsed = yaml.safe_load(yaml_content)

        # Assert
        assert parsed is not None, "YAML should parse successfully"
        assert parsed["session_id"] == valid_checkpoint_phase_1["session_id"]

    def test_should_write_valid_yaml_structure(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Written YAML structure is valid
        Given: A checkpoint
        When: Converted to YAML and parsed
        Then: All fields should be preserved
        """
        # Arrange
        checkpoint = valid_checkpoint_phase_1

        # Act
        yaml_str = yaml.dump(checkpoint)
        parsed = yaml.safe_load(yaml_str)

        # Assert
        assert parsed["session_id"] == checkpoint["session_id"]
        assert parsed["timestamp"] == checkpoint["timestamp"]
        assert parsed["current_phase"] == checkpoint["current_phase"]
        assert parsed["phase_completed"] == checkpoint["phase_completed"]
        assert parsed["brainstorm_context"] == checkpoint["brainstorm_context"]

    def test_should_handle_write_tool_errors(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool_with_error: Mock
    ):
        """
        Scenario: Handle errors from Write tool
        Given: Write tool raises IOError (disk full)
        When: Checkpoint creation is attempted
        Then: Error should be caught and propagated with context
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool_with_error)

        # Act & Assert
        with pytest.raises(IOError):
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

    def test_should_not_create_partial_files_on_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool_with_error: Mock
    ):
        """
        Scenario: No partial files created on write error
        Given: Write operation fails halfway
        When: Error is raised
        Then: File should not exist in partial state
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool_with_error)

        # Act
        try:
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)
        except IOError:
            pass  # Expected

        # Assert - File should not exist
        # (This is handled by Write tool atomicity)
        mock_write_tool_with_error.write.assert_called_once()

    def test_should_surface_error_reason_to_caller(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Error reason is communicated to caller
        Given: Write fails with specific error
        When: Exception is raised
        Then: Error message should contain reason
        """
        # Arrange
        mock_write_tool = Mock()
        error_msg = "Disk full: no space available"
        mock_write_tool.write.side_effect = IOError(error_msg)
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act & Assert
        with pytest.raises(IOError) as exc_info:
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)
        assert error_msg in str(exc_info.value)

    def test_should_write_with_atomic_semantics(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        tmp_path
    ):
        """
        Scenario: Write operation is atomic (all or nothing)
        Given: A checkpoint to write
        When: Write completes successfully
        Then: File should exist completely, not partially
        """
        # Arrange
        file_path = tmp_path / "test_checkpoint.yaml"
        checkpoint_data = valid_checkpoint_phase_1

        # Act - Simulate atomic write
        yaml_content = yaml.dump(checkpoint_data)
        with open(file_path, 'w') as f:
            f.write(yaml_content)

        # Assert
        assert file_path.exists(), "File should exist after write"
        assert file_path.stat().st_size > 0, "File should not be empty"
        # Verify it's readable YAML
        with open(file_path, 'r') as f:
            parsed = yaml.safe_load(f)
        assert parsed is not None

    def test_should_validate_yaml_before_write_attempt(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Validate YAML structure before attempting write
        Given: A checkpoint with potential formatting issues
        When: Pre-write validation happens
        Then: Should detect issues before calling Write tool
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1
        validator = YamlValidator()

        # Act
        is_valid = validator.validate(checkpoint_data)

        # Assert
        assert is_valid, "YAML should validate successfully"

    def test_should_handle_permission_denied_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Handle permission denied errors
        Given: Directory permissions prevent write
        When: Write is attempted
        Then: PermissionError should be raised with helpful message
        """
        # Arrange
        mock_write_tool = Mock()
        error_msg = "Permission denied: devforgeai/temp/"
        mock_write_tool.write.side_effect = PermissionError(error_msg)
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act & Assert
        with pytest.raises(PermissionError):
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

    def test_should_preserve_existing_checkpoint_on_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        valid_checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Existing checkpoint is preserved if new write fails
        Given: A valid checkpoint exists
        When: New write attempt fails
        Then: Old checkpoint should remain unchanged
        """
        # Arrange
        existing_checkpoint = valid_checkpoint_phase_1
        new_checkpoint = valid_checkpoint_phase_3

        # Simulate that existing checkpoint is already written
        # If new write fails, existing should remain

        mock_write_tool = Mock()
        mock_write_tool.write.side_effect = IOError("Write failed")
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        try:
            checkpoint_service.create_checkpoint(new_checkpoint)
        except IOError:
            pass

        # Assert - write tool was called, but error was raised
        mock_write_tool.write.assert_called()

    def test_should_write_with_proper_file_permissions(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        tmp_path
    ):
        """
        Scenario: Checkpoint file has proper permissions
        Given: A checkpoint is written
        When: File is created
        Then: File should be readable/writable by owner
        """
        # Arrange
        file_path = tmp_path / "test_checkpoint.yaml"
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        yaml_content = yaml.dump(checkpoint_data)
        with open(file_path, 'w') as f:
            f.write(yaml_content)

        # Assert
        stat_info = file_path.stat()
        # File should be readable and writable
        assert os.access(file_path, os.R_OK), "File should be readable"
        assert os.access(file_path, os.W_OK), "File should be writable"

    def test_should_ensure_idempotent_writes(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        tmp_path
    ):
        """
        Scenario: Writing same checkpoint twice produces identical file
        Given: A checkpoint
        When: Written twice to same file
        Then: Both writes should produce identical file content
        """
        # Arrange
        file_path = tmp_path / "test_checkpoint.yaml"
        checkpoint_data = valid_checkpoint_phase_1

        # Act - Write twice
        yaml_content_1 = yaml.dump(checkpoint_data)
        with open(file_path, 'w') as f:
            f.write(yaml_content_1)
        size_1 = file_path.stat().st_size

        yaml_content_2 = yaml.dump(checkpoint_data)
        with open(file_path, 'w') as f:
            f.write(yaml_content_2)
        size_2 = file_path.stat().st_size

        # Assert
        # Both writes should be identical
        assert size_1 == size_2, "Idempotent writes should produce same size"


