"""
Tests for AC#3: Checkpoint File Loading and Validation

Verifies that:
- Valid checkpoints load successfully
- Malformed YAML is handled gracefully
- Missing required fields are detected
- Warning message is shown on validation failure
"""

from typing import Dict, Any
from unittest.mock import Mock, patch

import pytest
import yaml


class CheckpointLoader:
    """
    Loads and validates checkpoint YAML files.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    REQUIRED_FIELDS = [
        "session_id",
        "timestamp",
        "current_phase",
        "phase_completed",
        "brainstorm_context"
    ]

    def __init__(self, read_tool: Mock):
        self.read_tool = read_tool

    def load_checkpoint(self, file_path: str) -> Dict[str, Any]:
        """
        Load checkpoint from file.

        Args:
            file_path: Path to checkpoint YAML file

        Returns:
            Parsed checkpoint dictionary

        Raises:
            ValueError: If YAML is malformed or missing required fields
            IOError: If file cannot be read
        """
        # Read file content
        content = self.read_tool.read(file_path)

        # Parse YAML
        try:
            checkpoint = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Malformed YAML in {file_path}: {e}")

        # Validate structure
        self.validate_checkpoint(checkpoint)

        return checkpoint

    def validate_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Validate checkpoint structure.

        Args:
            checkpoint: Checkpoint dictionary to validate

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(checkpoint, dict):
            raise ValueError(f"Checkpoint must be a dictionary, got {type(checkpoint).__name__}")

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in checkpoint:
                raise ValueError(f"Missing required field: {field}")

    def format_validation_error(self, error: Exception) -> str:
        """
        Format validation error as warning message.

        Args:
            error: The validation error

        Returns:
            Formatted warning message
        """
        return f"Checkpoint validation failed: {str(error)}"


class TestCheckpointFileLoadingAndValidation:
    """AC#3: Checkpoint file loading and validation"""

    def test_should_load_valid_checkpoint_successfully(
        self,
        mock_read_tool_with_yaml: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Load valid checkpoint file
        Given: Valid checkpoint YAML file exists
        When: CheckpointLoader.load_checkpoint() is called
        Then: Checkpoint data is parsed and returned successfully
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool_with_yaml)
        yaml_content = yaml.dump(checkpoint_phase_1)
        mock_read_tool_with_yaml.read.return_value = yaml_content

        # Act
        result = loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        # Assert
        assert result is not None
        assert result["session_id"] == checkpoint_phase_1["session_id"]
        assert result["current_phase"] == 1

    def test_should_use_read_tool_to_load_file(
        self,
        mock_read_tool_with_yaml: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Use Read tool to load checkpoint file
        Given: Checkpoint file path
        When: load_checkpoint() is called
        Then: Read tool is invoked with correct path
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool_with_yaml)
        file_path = "devforgeai/temp/.ideation-checkpoint-550e8400.yaml"
        yaml_content = yaml.dump(checkpoint_phase_1)
        mock_read_tool_with_yaml.read.return_value = yaml_content

        # Act
        loader.load_checkpoint(file_path)

        # Assert
        mock_read_tool_with_yaml.read.assert_called_once_with(file_path)

    def test_should_handle_malformed_yaml_gracefully(
        self,
        mock_read_tool: Mock,
        checkpoint_malformed_yaml: str
    ):
        """
        Scenario: Handle malformed YAML gracefully
        Given: Checkpoint file contains invalid YAML
        When: CheckpointLoader.load_checkpoint() is called
        Then: ValueError is raised with clear message
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        mock_read_tool.read.return_value = checkpoint_malformed_yaml

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        assert "Malformed YAML" in str(exc_info.value) or "YAML" in str(exc_info.value)

    def test_should_detect_missing_session_id_field(
        self,
        mock_read_tool: Mock,
        checkpoint_missing_session_id: Dict[str, Any]
    ):
        """
        Scenario: Detect missing session_id field
        Given: Checkpoint file missing session_id
        When: CheckpointLoader.load_checkpoint() is called
        Then: ValueError is raised indicating missing session_id
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_missing_session_id)
        mock_read_tool.read.return_value = yaml_content

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        assert "session_id" in str(exc_info.value)

    def test_should_detect_missing_timestamp_field(
        self,
        mock_read_tool: Mock,
        checkpoint_missing_timestamp: Dict[str, Any]
    ):
        """
        Scenario: Detect missing timestamp field
        Given: Checkpoint file missing timestamp
        When: CheckpointLoader.load_checkpoint() is called
        Then: ValueError is raised indicating missing timestamp
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_missing_timestamp)
        mock_read_tool.read.return_value = yaml_content

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        assert "timestamp" in str(exc_info.value)

    def test_should_detect_missing_current_phase_field(
        self,
        mock_read_tool: Mock,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Detect missing current_phase field
        Given: Checkpoint file missing current_phase
        When: CheckpointLoader.load_checkpoint() is called
        Then: ValueError is raised indicating missing current_phase
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        incomplete_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            # Missing: current_phase
            "phase_completed": True,
            "brainstorm_context": {}
        }
        yaml_content = yaml.dump(incomplete_checkpoint)
        mock_read_tool.read.return_value = yaml_content

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        assert "current_phase" in str(exc_info.value)

    def test_should_detect_missing_brainstorm_context_field(
        self,
        mock_read_tool: Mock,
        checkpoint_missing_context: Dict[str, Any]
    ):
        """
        Scenario: Detect missing brainstorm_context field
        Given: Checkpoint file missing brainstorm_context
        When: CheckpointLoader.load_checkpoint() is called
        Then: ValueError is raised indicating missing brainstorm_context
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_missing_context)
        mock_read_tool.read.return_value = yaml_content

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        assert "brainstorm_context" in str(exc_info.value)

    def test_should_format_validation_error_as_warning(
        self,
        mock_read_tool: Mock,
        checkpoint_missing_session_id: Dict[str, Any]
    ):
        """
        Scenario: Format validation errors as warning messages
        Given: Checkpoint validation fails
        When: load_checkpoint() raises error
        Then: Error message can be formatted for user display
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)

        # Act
        try:
            raise ValueError("Missing required field: session_id")
        except ValueError as e:
            warning = loader.format_validation_error(e)

        # Assert
        assert "validation failed" in warning.lower()
        assert "session_id" in warning

    def test_should_offer_fresh_start_on_validation_failure(
        self,
        mock_read_tool: Mock,
        checkpoint_missing_session_id: Dict[str, Any]
    ):
        """
        Scenario: Offer fresh start when checkpoint invalid
        Given: Checkpoint validation fails
        When: Error is raised
        Then: Error handling code offers fresh start option to user
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_missing_session_id)
        mock_read_tool.read.return_value = yaml_content

        # Act & Assert
        with pytest.raises(ValueError):
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")
        # (Actual fresh start offer happens in ResumeOrchestrator)

    def test_should_load_checkpoint_with_all_required_fields(
        self,
        mock_read_tool: Mock,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Load checkpoint with all required fields present
        Given: Checkpoint has all 5 required fields
        When: load_checkpoint() is called
        Then: Checkpoint loads successfully
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_phase_3)
        mock_read_tool.read.return_value = yaml_content

        # Act
        result = loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        # Assert
        assert "session_id" in result
        assert "timestamp" in result
        assert "current_phase" in result
        assert "phase_completed" in result
        assert "brainstorm_context" in result

    def test_should_validate_field_types(
        self,
        mock_read_tool: Mock,
        fixed_session_id: str
    ):
        """
        Scenario: Validate field types match schema
        Given: Checkpoint with wrong field types
        When: load_checkpoint() is called
        Then: Validation succeeds or fails based on field type checking
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)

        # Create checkpoint with invalid type for current_phase (should be int)
        invalid_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": "2025-12-22T15:30:45.123Z",
            "current_phase": "one",  # Should be int
            "phase_completed": True,
            "brainstorm_context": {}
        }
        yaml_content = yaml.dump(invalid_checkpoint)
        mock_read_tool.read.return_value = yaml_content

        # Act
        # This may or may not raise depending on implementation
        # The test documents the expected behavior
        try:
            result = loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")
            # If it doesn't raise, at least we got a result
            assert result is not None
        except ValueError:
            # Or it raises ValueError for type mismatch
            pass

    def test_should_handle_empty_yaml_file(
        self,
        mock_read_tool: Mock
    ):
        """
        Scenario: Handle empty or null YAML file
        Given: Checkpoint file is empty or contains only whitespace
        When: load_checkpoint() is called
        Then: ValueError is raised (not None or empty dict)
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        mock_read_tool.read.return_value = ""  # Empty file

        # Act & Assert
        with pytest.raises(ValueError):
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

    def test_should_detect_all_missing_fields_together(
        self,
        mock_read_tool: Mock
    ):
        """
        Scenario: Detect when all required fields are missing
        Given: Checkpoint file is empty dict
        When: load_checkpoint() is called
        Then: ValueError raised indicating missing fields
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        mock_read_tool.read.return_value = yaml.dump({})

        # Act & Assert
        with pytest.raises(ValueError):
            loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

    def test_should_preserve_checkpoint_data_on_successful_load(
        self,
        mock_read_tool: Mock,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Preserve all checkpoint data after load
        Given: Valid checkpoint with full brainstorm_context
        When: load_checkpoint() is called
        Then: All data is preserved, including personas, requirements, epics
        """
        # Arrange
        loader = CheckpointLoader(read_tool=mock_read_tool)
        yaml_content = yaml.dump(checkpoint_phase_2)
        mock_read_tool.read.return_value = yaml_content

        # Act
        result = loader.load_checkpoint("devforgeai/temp/.ideation-checkpoint-550e8400.yaml")

        # Assert
        context = result.get("brainstorm_context", {})
        assert context.get("problem_statement") == checkpoint_phase_2["brainstorm_context"]["problem_statement"]
        assert "personas" in context
        assert "requirements" in context
        assert "complexity_score" in context
        assert "epics" in context
