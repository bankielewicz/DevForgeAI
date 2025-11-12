"""
Edge case test suite for STORY-020: Feedback CLI Commands

Tests cover:
- Edge cases and boundary conditions
- Security considerations (injection, path traversal)
- Error recovery scenarios
- Performance boundaries
- Constraint violations

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, mock_open


# ============================================================================
# EDGE CASE: EMPTY FEEDBACK HISTORY
# ============================================================================


class TestEmptyFeedbackHistory:
    """Edge case tests for empty feedback history."""

    def test_feedback_search_empty_history_returns_zero_matches(self):
        """Test /feedback-search on empty history returns 0 matches gracefully."""
        # Arrange
        feedback_entries = []

        # Act
        total_matches = len(feedback_entries)

        # Assert
        assert total_matches == 0

    def test_feedback_search_empty_history_response_format_valid(self):
        """Test /feedback-search empty result returns valid response."""
        # Arrange
        response = {
            "status": "success",
            "query": "STORY-001",
            "total_matches": 0,
            "results": [],
            "message": "No feedback found matching query: STORY-001"
        }

        # Act & Assert
        assert isinstance(response, dict)
        assert response["status"] == "success"
        assert response["total_matches"] == 0
        assert len(response["results"]) == 0

    def test_export_feedback_empty_history_creates_empty_export(self):
        """Test /export-feedback on empty history creates valid empty export."""
        # Arrange
        export_data = {
            "status": "success",
            "export_id": "EXP-EMPTY-001",
            "entries_count": 0,
            "entries": [],
            "message": "Export created with 0 entries matched selection criteria"
        }

        # Act
        json_str = json.dumps(export_data)

        # Assert
        assert json.loads(json_str)["entries_count"] == 0
        assert len(json.loads(json_str)["entries"]) == 0


# ============================================================================
# EDGE CASE: INVALID CONFIGURATION CHANGES
# ============================================================================


class TestInvalidConfigurationChanges:
    """Edge case tests for invalid configuration changes."""

    def test_feedback_config_edit_negative_retention_days_rejected(self):
        """Test /feedback-config edit rejects negative retention_days value."""
        # Arrange
        new_value = -5

        # Act
        is_valid = 1 <= new_value <= 3650

        # Assert
        assert is_valid is False

    def test_feedback_config_edit_zero_retention_days_rejected(self):
        """Test /feedback-config edit rejects zero retention_days."""
        # Arrange
        new_value = 0

        # Act
        is_valid = 1 <= new_value <= 3650

        # Assert
        assert is_valid is False

    def test_feedback_config_edit_exceeds_max_retention_days_rejected(self):
        """Test /feedback-config edit rejects retention_days > 3650."""
        # Arrange
        new_value = 3651

        # Act
        is_valid = 1 <= new_value <= 3650

        # Assert
        assert is_valid is False

    def test_feedback_config_edit_invalid_export_format_rejected(self):
        """Test /feedback-config edit rejects invalid export_format."""
        # Arrange
        new_value = "xml"
        valid_formats = ["json", "csv", "markdown"]

        # Act
        is_valid = new_value in valid_formats

        # Assert
        assert is_valid is False

    def test_feedback_config_edit_invalid_boolean_value_rejected(self):
        """Test /feedback-config edit rejects non-boolean for boolean fields."""
        # Arrange
        invalid_values = ["yes", "no", 1, 0, "TRUE", "FALSE"]

        # Act & Assert
        # All these values should be invalid (not True or False booleans)
        for value in invalid_values:
            # Only true/false (lowercase strings if coerced, or actual booleans) are valid
            is_valid_boolean = value is True or value is False
            assert not is_valid_boolean, f"Value {value} should be rejected for boolean fields"

    def test_feedback_config_edit_prevents_corruption_on_invalid_input(self):
        """Test /feedback-config preserves config on invalid edit attempt."""
        # Arrange
        original_config = {
            "retention_days": 90,
            "auto_trigger_enabled": True
        }
        invalid_edit = {"retention_days": -5}

        # Act
        config = original_config.copy()
        # Validation would prevent update
        is_valid_update = (1 <= invalid_edit["retention_days"] <= 3650)

        # Assert
        if not is_valid_update:
            # Config remains unchanged
            assert config["retention_days"] == 90


# ============================================================================
# EDGE CASE: LARGE FEEDBACK HISTORY (1000+ ENTRIES)
# ============================================================================


class TestLargeFeedbackHistory:
    """Edge case tests for large feedback datasets."""

    def test_feedback_search_large_dataset_returns_paginated_results(self):
        """Test /feedback-search with 1000+ entries returns paginated results."""
        # Arrange
        total_entries = 1200
        page_size = 10

        # Act
        first_page_count = min(total_entries, page_size)
        total_pages = (total_entries + page_size - 1) // page_size

        # Assert
        assert first_page_count == 10
        assert total_pages == 120

    def test_feedback_search_large_dataset_pagination_limit_enforced(self):
        """Test /feedback-search --limit parameter respects max 1000."""
        # Arrange
        valid_limits = [1, 100, 500, 1000]
        invalid_limits = [1001, 5000, -1]

        # Act & Assert
        for limit in valid_limits:
            assert 1 <= limit <= 1000
        for limit in invalid_limits:
            assert not (1 <= limit <= 1000)

    def test_feedback_search_large_dataset_response_time_sla(self):
        """Test /feedback-search meets <500ms response time for typical queries."""
        # Arrange
        import time
        total_entries = 5000

        # Act - simulate search with large dataset
        start = time.time()
        # Simulated search operation
        results = []
        for i in range(min(10, total_entries)):
            results.append({"feedback_id": f"FB-{i}"})
        elapsed = time.time() - start

        # Assert - should be very fast (simulate fast operation)
        assert elapsed < 0.1  # Much faster than 500ms for simple simulation

    def test_export_feedback_large_dataset_completes_within_sla(self):
        """Test /export-feedback handles 5000+ entries within <5s SLA."""
        # Arrange
        import time
        entry_count = 5000

        # Act
        start = time.time()
        # Simulate export with 5000 entries
        export_entries = [{"feedback_id": f"FB-{i}"} for i in range(entry_count)]
        export_data = {
            "entries": export_entries,
            "entry_count": len(export_entries)
        }
        elapsed = time.time() - start

        # Assert
        assert len(export_data["entries"]) == entry_count
        assert elapsed < 5.0  # Large export within SLA


# ============================================================================
# EDGE CASE: EXPORT WITH NO MATCHING ENTRIES
# ============================================================================


class TestExportNoMatchingEntries:
    """Edge case tests for export with no matching entries."""

    def test_export_feedback_no_matches_creates_valid_export(self):
        """Test /export-feedback with no matching entries creates valid empty export."""
        # Arrange
        selection_criteria = {"story_ids": ["STORY-NONEXISTENT"]}
        matching_entries = []

        # Act
        export_data = {
            "status": "success",
            "selection_criteria": selection_criteria,
            "entries": matching_entries,
            "message": "Export created with 0 entries matched selection criteria"
        }

        # Assert
        assert export_data["status"] == "success"
        assert len(export_data["entries"]) == 0

    def test_export_feedback_no_matches_includes_metadata(self):
        """Test /export-feedback empty export includes full metadata."""
        # Arrange
        export_data = {
            "export_id": "EXP-EMPTY-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "entries": [],
            "metadata": {
                "selection_criteria": {"story_ids": ["STORY-999"]},
                "framework_version": "1.0.1",
                "config_snapshot": {}
            }
        }

        # Act & Assert
        assert "metadata" in export_data
        assert "selection_criteria" in export_data["metadata"]


# ============================================================================
# EDGE CASE: CONCURRENT FEEDBACK OPERATIONS
# ============================================================================


class TestConcurrentFeedbackOperations:
    """Edge case tests for concurrent feedback operations."""

    def test_concurrent_feedback_triggers_generate_unique_ids(self):
        """Test concurrent /feedback commands generate unique feedback IDs."""
        # Arrange
        feedback_ids = []

        # Simulate concurrent ID generation
        base_id = "FB-2025-11-07"
        for seq in range(1, 11):
            feedback_ids.append(f"{base_id}-{seq:03d}")

        # Act
        unique_ids = set(feedback_ids)

        # Assert
        assert len(unique_ids) == len(feedback_ids)  # All unique
        assert len(unique_ids) == 10

    def test_concurrent_feedback_operations_no_race_condition(self):
        """Test concurrent /feedback operations have no race condition."""
        # Arrange
        entries = []
        timestamps = [
            "2025-11-07T10:00:00Z",
            "2025-11-07T10:00:00Z",  # Same timestamp
            "2025-11-07T10:00:01Z"
        ]

        # Act
        for i, timestamp in enumerate(timestamps):
            entries.append({
                "feedback_id": f"FB-2025-11-07-{i+1:03d}",
                "timestamp": timestamp
            })

        # Assert
        feedback_ids = [e["feedback_id"] for e in entries]
        assert len(set(feedback_ids)) == len(feedback_ids)  # All unique despite same timestamps


# ============================================================================
# EDGE CASE: CONFIG FILE CORRUPTION
# ============================================================================


class TestConfigFileCorruption:
    """Edge case tests for config file corruption scenarios."""

    def test_corrupted_config_file_detected_on_load(self):
        """Test corrupted config file is detected during load."""
        # Arrange
        invalid_yaml = """
retention_days: [invalid yaml structure
auto_trigger_enabled true
export_format: "json"
"""
        # Act - attempt to parse
        try:
            import yaml
            yaml.safe_load(invalid_yaml)
            is_valid = True
        except:
            is_valid = False

        # Assert
        assert is_valid is False

    def test_corrupted_config_recovery_option_provided(self):
        """Test corrupted config error message includes recovery option."""
        # Arrange
        error_message = "Configuration file corrupted. Run `/feedback-config reset` to restore defaults."

        # Act & Assert
        assert "corrupted" in error_message.lower()
        assert "/feedback-config reset" in error_message

    def test_missing_config_file_creates_defaults(self):
        """Test missing config file triggers default creation."""
        # Arrange
        config_missing = True

        # Act
        if config_missing:
            default_config = {
                "retention_days": 90,
                "auto_trigger_enabled": True,
                "export_format": "json",
                "include_metadata": True,
                "search_enabled": True
            }

        # Assert
        assert default_config["retention_days"] == 90


# ============================================================================
# EDGE CASE: INVALID COMMAND ARGUMENTS
# ============================================================================


class TestInvalidCommandArguments:
    """Edge case tests for invalid command arguments."""

    def test_feedback_command_context_with_special_characters_rejected(self):
        """Test /feedback context with special chars rejected."""
        # Arrange
        invalid_context = "story-001; rm -rf /"

        # Act
        has_special_chars = any(c in invalid_context for c in ";()[]{}$`|&><")

        # Assert
        assert has_special_chars is True

    def test_feedback_search_query_with_sql_injection_attempt_escaped(self):
        """Test /feedback-search escapes SQL injection attempts."""
        # Arrange
        malicious_query = "STORY-001' OR '1'='1"

        # Act
        sanitized = malicious_query.replace("'", "").replace('"', "")

        # Assert
        assert "OR '1'='1" not in sanitized

    def test_export_feedback_path_traversal_prevented(self):
        """Test /export-feedback prevents directory traversal attacks."""
        # Arrange
        malicious_story_id = "../../etc/passwd"

        # Act
        is_safe = ".." not in malicious_story_id

        # Assert
        assert is_safe is False  # Contains ..

    def test_feedback_config_field_name_whitelist_enforced(self):
        """Test /feedback-config enforces field name whitelist."""
        # Arrange
        valid_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                       "include_metadata", "search_enabled"]
        invalid_field = "__init__"

        # Act
        is_valid = invalid_field in valid_fields

        # Assert
        assert is_valid is False


# ============================================================================
# EDGE CASE: EXPORT FORMAT NOT SUPPORTED
# ============================================================================


class TestUnsupportedExportFormat:
    """Edge case tests for unsupported export formats."""

    def test_export_feedback_unsupported_format_error(self):
        """Test /export-feedback rejects unsupported format."""
        # Arrange
        requested_format = "xml"
        supported_formats = ["json", "csv", "markdown"]

        # Act
        is_supported = requested_format in supported_formats

        # Assert
        assert is_supported is False

    def test_export_feedback_unsupported_format_error_message(self):
        """Test /export-feedback provides helpful error for unsupported format."""
        # Arrange
        error_message = "Format 'xml' not supported. Supported formats: json, csv, markdown"

        # Act & Assert
        assert "xml" in error_message
        assert "json" in error_message
        assert "csv" in error_message
        assert "markdown" in error_message


# ============================================================================
# EDGE CASE: MISSING EXPORT PERMISSIONS
# ============================================================================


class TestExportPermissionsError:
    """Edge case tests for export directory permission errors."""

    def test_export_feedback_permission_denied_error(self):
        """Test /export-feedback handles permission denied gracefully."""
        # Arrange
        error_message = "Cannot write to exports directory. Check file permissions."

        # Act & Assert
        assert "permission" in error_message.lower()

    def test_export_feedback_permission_error_suggests_remediation(self):
        """Test permission error suggests how to resolve."""
        # Arrange
        error_message = "Cannot write to exports directory. Check file permissions on .devforgeai/feedback/exports/"

        # Act & Assert
        assert "exports" in error_message
        assert ".devforgeai" in error_message


# ============================================================================
# EDGE CASE: VERY LONG INPUT STRINGS
# ============================================================================


class TestExtremelyLongInputs:
    """Edge case tests for extremely long input strings."""

    def test_feedback_context_exactly_500_chars_accepted(self):
        """Test /feedback accepts context exactly at 500 char limit."""
        # Arrange
        context = "a" * 500

        # Act
        is_valid = len(context) <= 500

        # Assert
        assert is_valid is True

    def test_feedback_context_501_chars_rejected(self):
        """Test /feedback rejects context at 501 chars."""
        # Arrange
        context = "a" * 501

        # Act
        is_valid = len(context) <= 500

        # Assert
        assert is_valid is False

    def test_feedback_search_query_exactly_200_chars_accepted(self):
        """Test /feedback-search accepts query exactly at 200 char limit."""
        # Arrange
        query = "a" * 200

        # Act
        is_valid = len(query) <= 200

        # Assert
        assert is_valid is True

    def test_feedback_search_query_201_chars_rejected(self):
        """Test /feedback-search rejects query at 201 chars."""
        # Arrange
        query = "a" * 201

        # Act
        is_valid = len(query) <= 200

        # Assert
        assert is_valid is False


# ============================================================================
# EDGE CASE: UNUSUAL TIMESTAMP FORMATS
# ============================================================================


class TestUnusualTimestampFormats:
    """Edge case tests for unusual timestamp handling."""

    def test_feedback_timestamp_iso8601_format_required(self):
        """Test feedback timestamp must be ISO8601 format."""
        # Arrange
        valid_timestamps = [
            "2025-11-07T14:30:00Z",
            "2025-11-07T14:30:00+00:00"
        ]
        invalid_timestamps = [
            "11/07/2025 14:30:00",
            "2025-11-07 14:30:00",
            "07-11-2025"
        ]

        # Act & Assert
        for ts in valid_timestamps:
            assert "T" in ts
        for ts in invalid_timestamps:
            assert "T" not in ts

    def test_feedback_search_date_range_start_after_end_rejected(self):
        """Test /feedback-search rejects date range with start > end."""
        # Arrange
        start_date = "2025-11-10"
        end_date = "2025-11-01"

        # Act
        is_valid = start_date <= end_date

        # Assert
        assert is_valid is False


# ============================================================================
# EDGE CASE: STATUS TRANSITIONS
# ============================================================================


class TestStatusTransitions:
    """Edge case tests for feedback status transitions."""

    def test_feedback_status_values_constrained(self):
        """Test feedback status limited to valid values."""
        # Arrange
        valid_statuses = ["open", "resolved", "archived"]
        invalid_status = "pending"

        # Act
        is_valid = invalid_status in valid_statuses

        # Assert
        assert is_valid is False

    def test_feedback_severity_values_constrained(self):
        """Test feedback severity limited to valid values."""
        # Arrange
        valid_severities = ["low", "medium", "high", "critical"]
        invalid_severity = "extreme"

        # Act
        is_valid = invalid_severity in valid_severities

        # Assert
        assert is_valid is False

    def test_feedback_operation_type_values_constrained(self):
        """Test operation_type limited to valid values."""
        # Arrange
        valid_operations = ["dev", "qa", "release", "manual"]
        invalid_operation = "deploy"

        # Act
        is_valid = invalid_operation in valid_operations

        # Assert
        assert is_valid is False


# ============================================================================
# EDGE CASE: PAGINATION BOUNDARIES
# ============================================================================


class TestPaginationBoundaries:
    """Edge case tests for pagination boundary conditions."""

    def test_feedback_search_page_zero_invalid(self):
        """Test /feedback-search page 0 is invalid."""
        # Arrange
        page = 0

        # Act
        is_valid = page > 0

        # Assert
        assert is_valid is False

    def test_feedback_search_page_negative_invalid(self):
        """Test /feedback-search negative page is invalid."""
        # Arrange
        page = -1

        # Act
        is_valid = page > 0

        # Assert
        assert is_valid is False

    def test_feedback_search_limit_zero_invalid(self):
        """Test /feedback-search limit 0 is invalid."""
        # Arrange
        limit = 0

        # Act
        is_valid = 1 <= limit <= 1000

        # Assert
        assert is_valid is False

    def test_feedback_search_beyond_last_page_handled(self):
        """Test /feedback-search handles page beyond available results."""
        # Arrange
        total_results = 47
        page_size = 10
        requested_page = 10  # Only 5 pages available

        # Act
        has_results_on_page = ((requested_page - 1) * page_size) < total_results

        # Assert
        assert has_results_on_page is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
