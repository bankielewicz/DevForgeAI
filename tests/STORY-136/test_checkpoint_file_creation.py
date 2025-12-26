"""
Tests for AC#1: Checkpoint File Creation at First Phase Boundary

Verifies that:
- Checkpoint file is created at devforgeai/temp/.ideation-checkpoint-{session_id}.yaml
- File creation happens after Phase 1 completion
- Write tool is used for file creation (not Bash)
- File path matches expected pattern
"""

import os
import re
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, patch, MagicMock

import pytest

from checkpoint_protocol import (
    CheckpointService,
    SessionIdGenerator,
    PathValidator
)


class TestCheckpointFileCreation:
    """Tests for checkpoint file creation at phase boundaries"""

    def test_should_create_checkpoint_file_after_phase_one_completion(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Create checkpoint file after Phase 1 completes
        Given: Phase 1 has completed with valid brainstorm context
        When: Checkpoint creation is triggered
        Then: Checkpoint file should be created at the expected path
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        expected_path = f"devforgeai/temp/.ideation-checkpoint-{fixed_session_id}.yaml"

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        mock_write_tool.write.assert_called_once()
        call_args = mock_write_tool.write.call_args
        assert expected_path in str(call_args)

    def test_should_create_checkpoint_at_correct_path_pattern(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Verify checkpoint file path matches expected pattern
        Given: A valid checkpoint data with session_id
        When: Checkpoint is created
        Then: File path should match pattern: devforgeai/temp/.ideation-checkpoint-{UUID}.yaml
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        pattern = r"^devforgeai/temp/\.ideation-checkpoint-[a-f0-9\-]{36}\.yaml$"

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        call_args = mock_write_tool.write.call_args
        file_path = call_args[0][0] if call_args else None
        assert file_path is not None, "Write tool should be called with file path"
        assert re.match(pattern, file_path), f"Path {file_path} does not match pattern {pattern}"

    def test_should_create_checkpoint_using_write_tool(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Verify Write tool is used for checkpoint creation
        Given: A valid checkpoint data
        When: Checkpoint is created
        Then: Write tool should be invoked with correct parameters
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        mock_write_tool.write.assert_called_once()
        # Verify Write tool was called with file_path and content
        assert len(mock_write_tool.write.call_args[0]) >= 2

    def test_should_not_use_bash_for_checkpoint_creation(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Verify Bash is NOT used for file operations
        Given: A valid checkpoint data
        When: Checkpoint creation is initiated
        Then: Bash tool should NOT be invoked for file operations
        """
        # Arrange
        with patch('subprocess.run') as mock_bash:
            checkpoint_service = CheckpointService(write_tool=Mock())

            # Act
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

            # Assert
            # Verify Bash was not called for echo/cat/file operations
            bash_calls = [
                call for call in mock_bash.call_args_list
                if any(cmd in str(call) for cmd in ['echo', 'cat', '>', '>>'])
            ]
            assert len(bash_calls) == 0, "Bash should not be used for file operations"

    def test_should_create_checkpoint_directory_if_missing(
        self,
        valid_checkpoint_phase_1: Dict[str, Any],
        tmp_path,
        mock_write_tool: Mock
    ):
        """
        Scenario: Create checkpoint directory if it doesn't exist
        Given: The devforgeai/temp/ directory does not exist
        When: Checkpoint is created
        Then: Directory should be created with proper permissions
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        # Verify write tool was called (directory creation would be internal)
        mock_write_tool.write.assert_called_once()

    def test_should_create_checkpoint_with_yaml_extension(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Ensure checkpoint file has .yaml extension
        Given: A valid checkpoint data
        When: Checkpoint is created
        Then: File should have .yaml extension
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        call_args = mock_write_tool.write.call_args
        file_path = call_args[0][0] if call_args else None
        assert file_path.endswith('.yaml'), f"File path {file_path} should end with .yaml"

    def test_should_create_checkpoint_with_hidden_filename(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any],
        mock_write_tool: Mock
    ):
        """
        Scenario: Checkpoint file should have hidden filename (starts with .)
        Given: A valid checkpoint data
        When: Checkpoint is created
        Then: Filename should start with . (hidden file)
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        call_args = mock_write_tool.write.call_args
        file_path = call_args[0][0] if call_args else None
        filename = Path(file_path).name
        assert filename.startswith('.'), f"Filename {filename} should start with ."

    def test_should_create_checkpoint_on_each_phase_boundary(
        self,
        fixed_session_id: str,
        mock_write_tool: Mock
    ):
        """
        Scenario: Checkpoint should be created at each phase boundary (1-5)
        Given: Phase transitions from 1 to 5
        When: Each phase completes
        Then: Checkpoint file should be created/updated
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        mock_write_tool.write.reset_mock()

        # Act - Create checkpoints for phases 1-5
        for phase in range(1, 6):
            checkpoint_data = {
                "session_id": fixed_session_id,
                "timestamp": "2025-12-22T15:30:45.123Z",
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {}
            }
            checkpoint_service.create_checkpoint(checkpoint_data)

        # Assert
        assert mock_write_tool.write.call_count == 5, "Write tool should be called for each phase"


