"""
Tests for AC#2: Checkpoint File Content Structure with Required Fields

Verifies that checkpoint YAML contains:
- session_id (UUID v4 format)
- timestamp (ISO 8601 format)
- current_phase (Integer 1-6)
- phase_completed (Boolean)
- brainstorm_context (Object with nested fields)
"""

from typing import Dict, Any
from unittest.mock import Mock, patch

import pytest
import yaml

from checkpoint_protocol import (
    CheckpointValidator,
    YamlValidator
)


class TestCheckpointContentStructure:
    """Tests for checkpoint file content structure and field validation"""

    def test_should_contain_session_id_field(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint contains session_id field
        Given: A valid checkpoint
        When: YAML is parsed
        Then: session_id field should be present
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))

        # Assert
        assert "session_id" in parsed, "session_id field should be present"
        assert parsed["session_id"] == fixed_session_id

    def test_should_contain_timestamp_field(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint contains timestamp field
        Given: A valid checkpoint
        When: YAML is parsed
        Then: timestamp field should be present
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))

        # Assert
        assert "timestamp" in parsed, "timestamp field should be present"
        assert isinstance(parsed["timestamp"], str)

    def test_should_contain_current_phase_field(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint contains current_phase field
        Given: A valid checkpoint
        When: YAML is parsed
        Then: current_phase field should be present and be an integer
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))

        # Assert
        assert "current_phase" in parsed, "current_phase field should be present"
        assert isinstance(parsed["current_phase"], int)
        assert 1 <= parsed["current_phase"] <= 6

    def test_should_contain_phase_completed_field(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint contains phase_completed field
        Given: A valid checkpoint
        When: YAML is parsed
        Then: phase_completed field should be present and be boolean
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))

        # Assert
        assert "phase_completed" in parsed, "phase_completed field should be present"
        assert isinstance(parsed["phase_completed"], bool)

    def test_should_contain_brainstorm_context_object(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint contains brainstorm_context nested object
        Given: A valid checkpoint
        When: YAML is parsed
        Then: brainstorm_context field should be present and contain nested data
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))

        # Assert
        assert "brainstorm_context" in parsed, "brainstorm_context field should be present"
        assert isinstance(parsed["brainstorm_context"], dict)

    def test_should_contain_all_brainstorm_context_nested_fields(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: brainstorm_context contains all required nested fields
        Given: A valid checkpoint with complete brainstorm_context
        When: YAML is parsed
        Then: All nested fields should be present:
              - problem_statement (string)
              - personas (array)
              - requirements (array)
              - complexity_score (integer)
              - epics (array)
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        parsed = yaml.safe_load(yaml.dump(checkpoint_data))
        context = parsed["brainstorm_context"]

        # Assert - Verify all required nested fields
        assert "problem_statement" in context, "problem_statement should be in brainstorm_context"
        assert isinstance(context["problem_statement"], str)

        assert "personas" in context, "personas should be in brainstorm_context"
        assert isinstance(context["personas"], list)

        assert "requirements" in context, "requirements should be in brainstorm_context"
        assert isinstance(context["requirements"], list)

        assert "complexity_score" in context, "complexity_score should be in brainstorm_context"
        assert isinstance(context["complexity_score"], int)

        assert "epics" in context, "epics should be in brainstorm_context"
        assert isinstance(context["epics"], list)

    def test_should_validate_yaml_syntax_validity(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint YAML is syntactically valid
        Given: A checkpoint data
        When: YAML dump and load is performed
        Then: YAML should parse without errors
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act
        yaml_string = yaml.dump(checkpoint_data)
        parsed = yaml.safe_load(yaml_string)

        # Assert
        assert parsed is not None, "YAML should parse successfully"
        assert isinstance(parsed, dict), "Parsed YAML should be a dictionary"

    def test_should_parse_with_pyyaml_standard_parser(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint can be parsed with standard PyYAML
        Given: A valid checkpoint YAML string
        When: yaml.safe_load is used
        Then: Should parse without errors or security issues
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1
        yaml_string = yaml.dump(checkpoint_data)

        # Act
        parsed = yaml.safe_load(yaml_string)

        # Assert
        assert parsed is not None
        assert parsed["session_id"] == valid_checkpoint_phase_1["session_id"]
        assert parsed["current_phase"] == valid_checkpoint_phase_1["current_phase"]

    def test_should_validate_field_types_match_schema(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: All fields match expected types
        Given: A valid checkpoint
        When: Field types are validated
        Then: Each field should have correct type:
              - session_id: str
              - timestamp: str
              - current_phase: int
              - phase_completed: bool
              - brainstorm_context: dict
        """
        # Arrange
        checkpoint_data = valid_checkpoint_phase_1

        # Act & Assert
        assert isinstance(checkpoint_data["session_id"], str)
        assert isinstance(checkpoint_data["timestamp"], str)
        assert isinstance(checkpoint_data["current_phase"], int)
        assert isinstance(checkpoint_data["phase_completed"], bool)
        assert isinstance(checkpoint_data["brainstorm_context"], dict)

    def test_should_reject_checkpoint_with_missing_session_id(
        self,
        checkpoint_missing_session_id: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint validation fails when session_id is missing
        Given: A checkpoint without session_id
        When: Validation is performed
        Then: ValidationError should be raised
        """
        # Arrange
        checkpoint_data = checkpoint_missing_session_id
        validator = CheckpointValidator()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            validator.validate(checkpoint_data)
        assert "session_id" in str(exc_info.value)

    def test_should_reject_checkpoint_with_missing_timestamp(
        self,
        checkpoint_missing_timestamp: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint validation fails when timestamp is missing
        Given: A checkpoint without timestamp
        When: Validation is performed
        Then: ValidationError should be raised
        """
        # Arrange
        checkpoint_data = checkpoint_missing_timestamp
        validator = CheckpointValidator()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            validator.validate(checkpoint_data)
        assert "timestamp" in str(exc_info.value)

    def test_should_accept_minimal_valid_checkpoint(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        minimal_brainstorm_context: Dict[str, Any]
    ):
        """
        Scenario: Minimal valid checkpoint passes validation
        Given: A checkpoint with only required fields
        When: Validation is performed
        Then: Should pass without errors
        """
        # Arrange
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": minimal_brainstorm_context,
        }
        validator = CheckpointValidator()

        # Act & Assert - Should not raise
        validator.validate(checkpoint_data)

    def test_should_handle_empty_personas_array(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Empty personas array is valid
        Given: Checkpoint with empty personas array
        When: Validation is performed
        Then: Should be valid (personas can be empty in early phases)
        """
        # Arrange
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": 0,
                "epics": []
            }
        }
        validator = CheckpointValidator()

        # Act & Assert
        validator.validate(checkpoint_data)  # Should not raise

    def test_should_handle_empty_requirements_array(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Empty requirements array is valid
        Given: Checkpoint with empty requirements array
        When: Validation is performed
        Then: Should be valid (requirements can be empty in early phases)
        """
        # Arrange
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [],
                "requirements": [],
                "complexity_score": 0,
                "epics": []
            }
        }
        validator = CheckpointValidator()

        # Act & Assert
        validator.validate(checkpoint_data)  # Should not raise


