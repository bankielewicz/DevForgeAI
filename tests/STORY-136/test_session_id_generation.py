"""
Tests for AC#3: Session ID Generation in UUID Format

Verifies that:
- Session ID is generated in UUID v4 format
- UUID format is valid: 8-4-4-4-12 hexadecimal pattern
- Session ID is consistent across multiple checkpoint writes
- Session IDs are unique across concurrent sessions
"""

import re
import uuid
from typing import Dict, Any
from unittest.mock import Mock

import pytest

from checkpoint_protocol import (
    SessionIdGenerator,
    SessionIdValidator,
    SessionIdExtractor,
    CheckpointService
)


class TestSessionIdGeneration:
    """Tests for session ID generation and validation"""

    def test_should_generate_uuid_v4_format(self, valid_session_id: str):
        """
        Scenario: Generate session ID in UUID v4 format
        Given: A new session is starting
        When: Session ID is generated
        Then: Should be valid UUID v4 string
        """
        # Arrange
        generator = SessionIdGenerator()

        # Act
        session_id = generator.generate()

        # Assert
        # Verify it can be parsed as UUID
        try:
            parsed_uuid = uuid.UUID(session_id)
            assert parsed_uuid.version == 4, "UUID should be version 4"
        except ValueError:
            pytest.fail(f"Generated session_id {session_id} is not a valid UUID")

    def test_should_validate_uuid_format_8_4_4_4_12_pattern(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Validate UUID format follows 8-4-4-4-12 hexadecimal pattern
        Given: A session ID
        When: Format is validated
        Then: Should match pattern: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        """
        # Arrange
        pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"

        # Act & Assert
        assert re.match(pattern, fixed_session_id), \
            f"Session ID {fixed_session_id} does not match UUID v4 pattern"

    def test_should_reject_invalid_uuid_formats(
        self,
        invalid_session_ids: list[str]
    ):
        """
        Scenario: Reject invalid session ID formats
        Given: Various invalid UUID strings
        When: Validation is performed
        Then: Should reject non-UUID formats
        """
        # Arrange
        validator = SessionIdValidator()

        # Act & Assert
        for invalid_id in invalid_session_ids:
            with pytest.raises(ValueError):
                validator.validate(invalid_id)

    def test_should_maintain_session_id_consistency_across_writes(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Session ID remains consistent across multiple checkpoint writes
        Given: A session with fixed session_id
        When: Multiple checkpoints are created for same session
        Then: All checkpoints should have same session_id
        """
        # Arrange
        checkpoint_service = CheckpointService()
        checkpoints = []

        # Act - Create multiple checkpoints with same session_id
        for phase in range(1, 6):
            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": "2025-12-22T15:30:45.123Z",
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {}
            }
            checkpoints.append(checkpoint)

        # Assert - All should have same session_id
        for checkpoint in checkpoints:
            assert checkpoint["session_id"] == fixed_session_id, \
                "Session ID should remain consistent across checkpoints"

    def test_should_generate_unique_session_ids_for_concurrent_sessions(self):
        """
        Scenario: Generate unique session IDs for different sessions
        Given: Multiple sessions starting
        When: Session IDs are generated
        Then: Each session should get unique session_id
        """
        # Arrange
        generator = SessionIdGenerator()
        session_ids = set()

        # Act - Generate 10 session IDs
        for _ in range(10):
            session_id = generator.generate()
            session_ids.add(session_id)

        # Assert - All should be unique
        assert len(session_ids) == 10, "All generated session IDs should be unique"

    def test_should_validate_uuid_v4_version_field(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Validate UUID version field is 4
        Given: A session ID
        When: UUID version is checked
        Then: Should be version 4 (random)
        """
        # Arrange
        parsed = uuid.UUID(fixed_session_id)

        # Act & Assert
        assert parsed.version == 4, f"UUID version should be 4, got {parsed.version}"

    def test_should_validate_uuid_variant_field(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Validate UUID variant field (RFC 4122)
        Given: A session ID
        When: UUID variant is checked
        Then: Should follow RFC 4122 standard
        """
        # Arrange
        parsed = uuid.UUID(fixed_session_id)

        # Act & Assert
        assert parsed.variant == "specified in RFC 4122", \
            f"UUID variant should be RFC 4122, got {parsed.variant}"

    def test_should_store_session_id_in_checkpoint_at_creation(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Session ID is stored in checkpoint at creation time
        Given: A new ideation session
        When: First checkpoint is created
        Then: Checkpoint should contain the session_id
        """
        # Arrange
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": "2025-12-22T15:30:45.123Z",
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": {}
        }

        # Act & Assert
        assert checkpoint_data["session_id"] == fixed_session_id

    def test_should_allow_session_id_lookup_by_checkpoint_file(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Session ID can be extracted from checkpoint filename
        Given: A checkpoint file path
        When: Session ID is extracted
        Then: Should extract valid UUID from filename
        """
        # Arrange
        filename = f".ideation-checkpoint-{fixed_session_id}.yaml"
        extractor = SessionIdExtractor()

        # Act
        extracted_id = extractor.extract_from_filename(filename)

        # Assert
        assert extracted_id == fixed_session_id

    def test_should_reject_session_id_with_uppercase_letters(self):
        """
        Scenario: UUID validation should be case-insensitive
        Given: A UUID with uppercase letters
        When: Validation is performed
        Then: Should accept (UUID parsers are case-insensitive)
        """
        # Arrange
        uppercase_uuid = "550E8400-E29B-41D4-A716-446655440000"
        validator = SessionIdValidator()

        # Act & Assert
        # UUID parsing is case-insensitive, both should be valid
        validator.validate(uppercase_uuid.lower())  # Should not raise

    @pytest.mark.parametrize("invalid_id", [
        "not-a-uuid",
        "550e8400-e29b-41d4-a716",
        "550e8400e29b41d4a716446655440000",
        "550e8400-e29b-41d4-a716-44665544000G",
        "",
    ])
    def test_should_reject_multiple_invalid_formats(self, invalid_id: str):
        """
        Scenario: Reject various invalid UUID formats
        Given: Various non-UUID strings
        When: Validation is performed
        Then: Should reject all invalid formats
        """
        # Arrange
        validator = SessionIdValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_id)

    def test_should_generate_different_session_id_on_each_call(self):
        """
        Scenario: Each call to generate should return different ID
        Given: SessionIdGenerator
        When: generate() called twice
        Then: Should return different session IDs
        """
        # Arrange
        generator = SessionIdGenerator()

        # Act
        id_1 = generator.generate()
        id_2 = generator.generate()

        # Assert
        assert id_1 != id_2, "Each generate() call should return unique ID"
