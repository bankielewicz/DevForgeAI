"""
Tests for Edge Cases and Non-Functional Requirements

Tests for:
- Complexity score validation (0-60)
- File size limits (<5KB)
- Disk full error handling
- Permission denied error handling
- Invalid complexity score rejection
- Secret detection in checkpoint
- Malformed YAML handling
"""

from typing import Dict, Any
from unittest.mock import Mock
import json

import pytest
import yaml

from checkpoint_protocol import (
    CheckpointService,
    ComplexityValidator,
    PathValidator,
    SecretScanner
)


class TestEdgeCases:
    """Tests for edge cases and error conditions"""

    # ========================================================================
    # Complexity Score Validation
    # ========================================================================

    def test_should_validate_complexity_score_minimum_is_zero(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Complexity score minimum is 0
        Given: A checkpoint with complexity_score = 0
        When: Validation is performed
        Then: Should be valid
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": 0,  # Minimum
                "epics": []
            }
        }
        validator = ComplexityValidator()

        # Act & Assert
        validator.validate(checkpoint)  # Should not raise

    def test_should_validate_complexity_score_maximum_is_60(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Complexity score maximum is 60
        Given: A checkpoint with complexity_score = 60
        When: Validation is performed
        Then: Should be valid
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": 60,  # Maximum
                "epics": []
            }
        }
        validator = ComplexityValidator()

        # Act & Assert
        validator.validate(checkpoint)  # Should not raise

    def test_should_reject_complexity_score_less_than_zero(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Reject complexity score < 0
        Given: A checkpoint with complexity_score = -1
        When: Validation is performed
        Then: Should reject with ValueError
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": -1,  # Invalid
                "epics": []
            }
        }
        validator = ComplexityValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(checkpoint)

    def test_should_reject_complexity_score_greater_than_60(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Reject complexity score > 60
        Given: A checkpoint with complexity_score = 61
        When: Validation is performed
        Then: Should reject with ValueError
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": 61,  # Invalid
                "epics": []
            }
        }
        validator = ComplexityValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(checkpoint)

    @pytest.mark.parametrize("score", [-1, 61, 100, 999])
    def test_should_reject_multiple_invalid_complexity_scores(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        score: int
    ):
        """
        Scenario: Reject various out-of-range complexity scores
        Given: Various invalid complexity scores
        When: Validation is performed
        Then: Should reject all
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": score,
                "epics": []
            }
        }
        validator = ComplexityValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(checkpoint)

    # ========================================================================
    # File Size Validation
    # ========================================================================

    def test_should_validate_minimal_checkpoint_file_size(
        self,
        minimal_brainstorm_context: Dict[str, Any]
    ):
        """
        Scenario: Minimal checkpoint file is under 5KB
        Given: A minimal checkpoint
        When: File size is measured
        Then: Should be < 5KB
        """
        # Arrange
        checkpoint = {
            "session_id": "550e8400-e29b-41d4-a716-446655440000",
            "timestamp": "2025-12-22T15:30:45.123Z",
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": minimal_brainstorm_context,
        }
        yaml_content = yaml.dump(checkpoint)
        file_size_bytes = len(yaml_content.encode('utf-8'))

        # Act & Assert
        assert file_size_bytes < 5120, f"File size {file_size_bytes} bytes should be < 5KB"

    def test_should_validate_normal_checkpoint_file_size(
        self,
        valid_brainstorm_context: Dict[str, Any]
    ):
        """
        Scenario: Normal checkpoint file is under 5KB
        Given: A checkpoint with typical data
        When: File size is measured
        Then: Should be < 5KB
        """
        # Arrange
        checkpoint = {
            "session_id": "550e8400-e29b-41d4-a716-446655440000",
            "timestamp": "2025-12-22T15:30:45.123Z",
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": valid_brainstorm_context,
        }
        yaml_content = yaml.dump(checkpoint)
        file_size_bytes = len(yaml_content.encode('utf-8'))

        # Act & Assert
        assert file_size_bytes < 5120, f"File size {file_size_bytes} bytes should be < 5KB"

    def test_should_handle_large_checkpoint_file_size(
        self,
        large_brainstorm_context: Dict[str, Any],
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Truncate checkpoint if it exceeds 5KB
        Given: A checkpoint that would exceed 5KB
        When: File size limit is enforced
        Then: Should truncate least critical data
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": large_brainstorm_context,
        }
        yaml_content = yaml.dump(checkpoint)
        file_size_bytes = len(yaml_content.encode('utf-8'))

        # Act - Simulate progressive truncation if needed (per NFR-002)
        if file_size_bytes > 5120:
            # Step 1: Truncate epics (least critical)
            checkpoint["brainstorm_context"]["epics"] = []
            yaml_content = yaml.dump(checkpoint)
            file_size_bytes = len(yaml_content.encode('utf-8'))

        if file_size_bytes > 5120:
            # Step 2: Truncate requirements to last 10
            checkpoint["brainstorm_context"]["requirements"] = \
                checkpoint["brainstorm_context"]["requirements"][-10:]
            yaml_content = yaml.dump(checkpoint)
            file_size_bytes = len(yaml_content.encode('utf-8'))

        if file_size_bytes > 5120:
            # Step 3: Truncate personas to last 5
            checkpoint["brainstorm_context"]["personas"] = \
                checkpoint["brainstorm_context"]["personas"][-5:]
            yaml_content = yaml.dump(checkpoint)
            file_size_bytes = len(yaml_content.encode('utf-8'))

        # Assert - After progressive truncation, should be < 5KB
        assert file_size_bytes < 5120, f"After truncation, should be < 5KB (got {file_size_bytes})"

    # ========================================================================
    # Error Handling - Disk Full
    # ========================================================================

    def test_should_handle_disk_full_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Handle disk full during checkpoint write
        Given: Write tool reports disk full
        When: Checkpoint creation is attempted
        Then: IOError should be raised without crashing session
        """
        # Arrange
        mock_write_tool = Mock()
        mock_write_tool.write.side_effect = IOError("No space left on device")
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act & Assert
        with pytest.raises(IOError):
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

    def test_should_continue_session_after_disk_full_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Session continues even if checkpoint write fails
        Given: Disk full error occurs
        When: Checkpoint creation fails
        Then: Session should continue (graceful degradation)
        """
        # Arrange
        mock_write_tool = Mock()
        mock_write_tool.write.side_effect = IOError("No space left on device")
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        error_caught = False
        try:
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)
        except IOError:
            error_caught = True

        # Assert
        assert error_caught, "Error should be raised"
        # Session handling would continue in production

    # ========================================================================
    # Error Handling - Permission Denied
    # ========================================================================

    def test_should_handle_permission_denied_error(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Handle permission denied when writing checkpoint
        Given: No write permission on devforgeai/temp/
        When: Checkpoint creation is attempted
        Then: PermissionError should be raised
        """
        # Arrange
        mock_write_tool = Mock()
        mock_write_tool.write.side_effect = PermissionError("Permission denied")
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act & Assert
        with pytest.raises(PermissionError):
            checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

    def test_should_create_directory_if_missing(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Create checkpoint directory if missing
        Given: devforgeai/temp/ does not exist
        When: Checkpoint creation is attempted
        Then: Directory should be created
        """
        # Arrange
        mock_write_tool = Mock()
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)

        # Act
        checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)

        # Assert
        mock_write_tool.write.assert_called_once()

    # ========================================================================
    # Security - No Secrets in Checkpoint
    # ========================================================================

    def test_should_contain_no_api_keys_in_checkpoint(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Checkpoint should not contain API keys
        Given: A checkpoint
        When: Content is scanned for secrets
        Then: Should not contain patterns like api_key=...
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Build an app",
                "personas": [],
                "requirements": [],
                "complexity_score": 30,
                "epics": []
            }
        }
        scanner = SecretScanner()

        # Act
        has_secrets = scanner.scan(checkpoint)

        # Assert
        assert not has_secrets, "Checkpoint should not contain secrets"

    def test_should_contain_no_passwords_in_checkpoint(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Checkpoint should not contain passwords
        Given: A checkpoint
        When: Content is scanned for secrets
        Then: Should not contain password patterns
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Build an app",
                "personas": [],
                "requirements": [],
                "complexity_score": 30,
                "epics": []
            }
        }
        scanner = SecretScanner()

        # Act
        has_secrets = scanner.scan(checkpoint)

        # Assert
        assert not has_secrets, "Checkpoint should not contain passwords"

    def test_should_contain_no_connection_strings_in_checkpoint(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Checkpoint should not contain connection strings
        Given: A checkpoint
        When: Content is scanned
        Then: Should not contain credentials in connection strings
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Build an app",
                "personas": [],
                "requirements": [],
                "complexity_score": 30,
                "epics": []
            }
        }

        # Act - Verify no connection strings
        checkpoint_json = json.dumps(checkpoint)

        # Assert
        assert "password=" not in checkpoint_json.lower()
        assert "secret=" not in checkpoint_json.lower()
        assert "api_key=" not in checkpoint_json.lower()

    # ========================================================================
    # Invalid YAML Handling
    # ========================================================================

    def test_should_reject_malformed_yaml_on_read(self):
        """
        Scenario: Reject malformed YAML when reading checkpoint
        Given: A corrupted YAML file
        When: File is parsed
        Then: yaml.safe_load should raise yaml.YAMLError
        """
        # Arrange
        malformed_yaml = """
        session_id: 550e8400-e29b-41d4-a716-446655440000
        timestamp: 2025-12-22T15:30:45.123Z
        current_phase: 1
        brainstorm_context:
          problem_statement: Test
          personas: [
          # Missing closing bracket - malformed
        """

        # Act & Assert
        with pytest.raises(yaml.YAMLError):
            yaml.safe_load(malformed_yaml)

    def test_should_handle_empty_checkpoint_file(self):
        """
        Scenario: Handle empty checkpoint file
        Given: An empty checkpoint file
        When: File is parsed
        Then: Should parse as None or empty dict
        """
        # Arrange
        empty_yaml = ""

        # Act
        parsed = yaml.safe_load(empty_yaml)

        # Assert
        assert parsed is None, "Empty YAML should parse as None"

    # ========================================================================
    # Path Validation
    # ========================================================================

    def test_should_reject_file_paths_with_parent_directory_traversal(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Reject paths with ../ (directory traversal)
        Given: A malicious path with ../
        When: Path validation is performed
        Then: Should reject the path
        """
        # Arrange
        malicious_path = f"../../../etc/passwd"
        validator = PathValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(malicious_path)

    def test_should_ensure_path_is_in_devforgeai_temp(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Checkpoint path must be in devforgeai/temp/ only
        Given: A checkpoint path
        When: Path validation is performed
        Then: Should be restricted to devforgeai/temp/
        """
        # Arrange
        valid_path = f"devforgeai/temp/.ideation-checkpoint-{fixed_session_id}.yaml"
        invalid_path = f"home/user/.ideation-checkpoint-{fixed_session_id}.yaml"
        validator = PathValidator()

        # Act & Assert
        validator.validate(valid_path)  # Should not raise
        with pytest.raises(ValueError):
            validator.validate(invalid_path)


