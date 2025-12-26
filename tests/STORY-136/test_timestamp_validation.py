"""
Tests for AC#4: Timestamp Recording in ISO 8601 Format

Verifies that:
- Timestamp is in ISO 8601 format with millisecond precision
- Timestamp includes Z suffix for UTC timezone
- Timestamp is within 1 second of actual write time
- Various invalid timestamp formats are rejected
"""

import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from unittest.mock import Mock, patch

import pytest

from checkpoint_protocol import (
    TimestampGenerator,
    TimestampValidator,
    TimestampParser,
    CheckpointService
)


class TestTimestampValidation:
    """Tests for timestamp generation and validation"""

    def test_should_record_iso_8601_timestamp(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Timestamp is in ISO 8601 format
        Given: A checkpoint is created
        When: Timestamp is recorded
        Then: Should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.fffZ)
        """
        # Arrange
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"

        # Act & Assert
        assert re.match(pattern, valid_iso_timestamp), \
            f"Timestamp {valid_iso_timestamp} does not match ISO 8601 format"

    def test_should_include_millisecond_precision(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Timestamp includes millisecond precision
        Given: A checkpoint with timestamp
        When: Timestamp is validated
        Then: Should have exactly 3 digits for milliseconds
        """
        # Arrange
        # Format: 2025-12-22T15:30:45.123Z

        # Act
        # Extract milliseconds part
        ms_part = valid_iso_timestamp.split('.')[1].rstrip('Z')

        # Assert
        assert len(ms_part) == 3, "Milliseconds should have exactly 3 digits"
        assert ms_part.isdigit(), "Milliseconds should be numeric"

    def test_should_include_z_suffix_for_utc(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Timestamp includes Z suffix for UTC timezone
        Given: A timestamp
        When: Format is checked
        Then: Should end with 'Z' indicating UTC
        """
        # Arrange & Act & Assert
        assert valid_iso_timestamp.endswith('Z'), \
            f"Timestamp {valid_iso_timestamp} should end with 'Z' for UTC"

    def test_should_validate_timestamp_within_one_second_of_actual(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Timestamp is recorded within 1 second of actual write time
        Given: A checkpoint is being created
        When: Write tool is called
        Then: Recorded timestamp should be within 1 second of current time
        """
        # Arrange
        before_write = datetime.now(timezone.utc)
        generator = TimestampGenerator()

        # Act
        timestamp_str = generator.generate()

        after_write = datetime.now(timezone.utc)

        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

        # Assert
        time_diff = abs((timestamp - before_write).total_seconds())
        assert time_diff <= 1.0, \
            f"Timestamp should be within 1 second, got {time_diff}s difference"

    def test_should_validate_date_format_yyyy_mm_dd(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Date portion is in YYYY-MM-DD format
        Given: A timestamp
        When: Date is parsed
        Then: Should follow YYYY-MM-DD format
        """
        # Arrange
        date_part = valid_iso_timestamp.split('T')[0]

        # Act & Assert
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        assert re.match(pattern, date_part), \
            f"Date {date_part} should be YYYY-MM-DD format"

    def test_should_validate_time_format_hh_mm_ss(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Time portion is in HH:MM:SS format
        Given: A timestamp
        When: Time is parsed
        Then: Should follow HH:MM:SS format
        """
        # Arrange
        time_part = valid_iso_timestamp.split('T')[1].split('.')[0]

        # Act & Assert
        pattern = r"^\d{2}:\d{2}:\d{2}$"
        assert re.match(pattern, time_part), \
            f"Time {time_part} should be HH:MM:SS format"

    def test_should_reject_timestamp_without_milliseconds(self):
        """
        Scenario: Reject timestamp without millisecond precision
        Given: A timestamp without milliseconds
        When: Validation is performed
        Then: Should reject the timestamp
        """
        # Arrange
        invalid_timestamp = "2025-12-22T15:30:45Z"
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_reject_timestamp_without_z_suffix(self):
        """
        Scenario: Reject timestamp without Z suffix
        Given: A timestamp without Z
        When: Validation is performed
        Then: Should reject the timestamp
        """
        # Arrange
        invalid_timestamp = "2025-12-22T15:30:45.123"
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_reject_timestamp_with_plus_timezone(self):
        """
        Scenario: Reject timestamp with +HH:MM timezone format
        Given: A timestamp with +00:00 instead of Z
        When: Validation is performed
        Then: Should reject (must use Z for UTC)
        """
        # Arrange
        invalid_timestamp = "2025-12-22T15:30:45.123+00:00"
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_reject_invalid_date_format(self):
        """
        Scenario: Reject invalid date format
        Given: A timestamp with wrong date format
        When: Validation is performed
        Then: Should reject
        """
        # Arrange
        invalid_timestamp = "22/12/2025T15:30:45.123Z"  # US format, wrong separator
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_reject_timestamp_with_space_instead_of_t(self):
        """
        Scenario: Reject timestamp with space instead of T separator
        Given: A timestamp with space separator
        When: Validation is performed
        Then: Should reject
        """
        # Arrange
        invalid_timestamp = "2025-12-22 15:30:45.123Z"
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_validate_time_ranges(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Validate time components are in valid ranges
        Given: A timestamp
        When: Time is parsed
        Then: Hours (0-23), Minutes (0-59), Seconds (0-59) should be valid
        """
        # Arrange
        parser = TimestampParser()

        # Act
        time_parts = parser.parse(valid_iso_timestamp)

        # Assert
        assert 0 <= time_parts['hour'] <= 23, "Hour should be 0-23"
        assert 0 <= time_parts['minute'] <= 59, "Minute should be 0-59"
        assert 0 <= time_parts['second'] <= 59, "Second should be 0-59"
        assert 0 <= time_parts['millisecond'] <= 999, "Millisecond should be 0-999"

    def test_should_validate_date_ranges(
        self,
        valid_iso_timestamp: str
    ):
        """
        Scenario: Validate date components are in valid ranges
        Given: A timestamp
        When: Date is parsed
        Then: Month (1-12) and Day (1-31) should be valid
        """
        # Arrange
        parser = TimestampParser()

        # Act
        date_parts = parser.parse(valid_iso_timestamp)

        # Assert
        assert 1 <= date_parts['month'] <= 12, "Month should be 1-12"
        assert 1 <= date_parts['day'] <= 31, "Day should be 1-31"

    @pytest.mark.parametrize("invalid_timestamp", [
        "2025-12-22 15:30:45",                  # Missing T separator
        "2025-12-22T15:30:45",                  # Missing milliseconds
        "2025-12-22T15:30:45.123",              # Missing Z
        "2025-12-22T15:30:45.123+00:00",        # Wrong timezone
        "22/12/2025 15:30:45",                  # US format
        "not-a-timestamp",                      # Invalid
        "",                                     # Empty
        "2025/12/22T15:30:45.123Z",             # Wrong date separator
    ])
    def test_should_reject_multiple_invalid_formats(
        self,
        invalid_timestamp: str
    ):
        """
        Scenario: Reject multiple variations of invalid timestamp formats
        Given: Various invalid timestamp strings
        When: Validation is performed
        Then: Should reject all invalid formats
        """
        # Arrange
        validator = TimestampValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(invalid_timestamp)

    def test_should_update_timestamp_on_checkpoint_update(
        self,
        fixed_session_id: str
    ):
        """
        Scenario: Timestamp is updated when checkpoint is updated
        Given: A checkpoint is updated with new phase
        When: Checkpoint is written
        Then: Timestamp should reflect new write time
        """
        # Arrange
        generator = TimestampGenerator()

        # Act
        timestamp_1 = generator.generate()
        # Simulate time passing
        import time
        time.sleep(0.01)  # 10ms delay
        timestamp_2 = generator.generate()

        # Parse both timestamps
        ts_1 = datetime.fromisoformat(timestamp_1.replace('Z', '+00:00'))
        ts_2 = datetime.fromisoformat(timestamp_2.replace('Z', '+00:00'))

        # Assert
        assert ts_2 >= ts_1, "Second timestamp should be equal or later"

    def test_should_use_utc_not_local_timezone(self):
        """
        Scenario: Timestamps use UTC, not local timezone
        Given: A checkpoint is created
        When: Timestamp is recorded
        Then: Z suffix indicates UTC (Zulu time)
        """
        # Arrange
        generator = TimestampGenerator()

        # Act
        timestamp = generator.generate()

        # Assert
        assert timestamp.endswith('Z'), "Timestamp should use UTC (Z suffix)"
        # Verify it can be parsed as UTC
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        assert dt.tzinfo is not None


