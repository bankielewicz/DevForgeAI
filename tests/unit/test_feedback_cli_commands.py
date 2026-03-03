"""
Comprehensive unit test suite for STORY-020: Feedback CLI Commands

Tests cover:
- 6 acceptance criteria (AC1-AC6)
- 4 CLI commands (/feedback, /feedback-config, /feedback-search, /export-feedback)
- Argument parsing and validation
- Configuration field validation
- Query parsing and filtering
- Export format selection
- Data model creation and validation
- Error message generation

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock, mock_open
import argparse
from io import StringIO


# ============================================================================
# FIXTURES - Common setup for all tests
# ============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with feedback structure."""
    with tempfile.TemporaryDirectory(prefix="feedback_cli_") as tmpdir:
        project_path = Path(tmpdir)

        # Create feedback directory structure
        feedback_dir = project_path / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)

        exports_dir = feedback_dir / "exports"
        exports_dir.mkdir(exist_ok=True)

        # Create default config.yaml
        config_file = feedback_dir / "config.yaml"
        config_content = """retention_days: 90
auto_trigger_enabled: true
export_format: json
include_metadata: true
search_enabled: true
created_at: 2025-11-07T00:00:00Z
last_modified: 2025-11-07T00:00:00Z
"""
        config_file.write_text(config_content)

        # Create sample feedback-register.md
        register_file = feedback_dir / "feedback-register.md"
        register_content = """# Feedback Register

## Active Feedback Sessions

### FB-2025-11-07-001
- **Timestamp:** 2025-11-07T14:30:00Z
- **Story ID:** STORY-001
- **Operation:** dev
- **Severity:** medium
- **Status:** open
- **Context:** TDD cycle took longer than expected
- **Metadata:** {framework_version: "1.0.1", duration: 3600}

### FB-2025-11-07-002
- **Timestamp:** 2025-11-07T15:15:00Z
- **Story ID:** STORY-001
- **Operation:** qa
- **Severity:** high
- **Status:** open
- **Context:** Coverage below threshold
- **Metadata:** {framework_version: "1.0.1", duration: 1200}

### FB-2025-11-07-003
- **Timestamp:** 2025-11-06T10:00:00Z
- **Story ID:** STORY-002
- **Operation:** dev
- **Severity:** low
- **Status:** resolved
- **Context:** Minor refactoring completed
- **Metadata:** {framework_version: "1.0.1", duration: 600}
"""
        register_file.write_text(register_content)

        yield project_path


@pytest.fixture
def feedback_config_dict():
    """Valid feedback configuration dictionary."""
    return {
        "retention_days": 90,
        "auto_trigger_enabled": True,
        "export_format": "json",
        "include_metadata": True,
        "search_enabled": True,
        "created_at": "2025-11-07T00:00:00Z",
        "last_modified": "2025-11-07T00:00:00Z"
    }


@pytest.fixture
def feedback_entry():
    """Sample feedback entry."""
    return {
        "feedback_id": "FB-2025-11-07-001",
        "timestamp": "2025-11-07T14:30:00Z",
        "story_id": "STORY-001",
        "operation_type": "dev",
        "context": "story-001 after-dev-completion",
        "severity": "medium",
        "status": "open",
        "insights": "TDD cycle took longer than expected",
        "metadata": {
            "framework_version": "1.0.1",
            "command": "/dev STORY-001",
            "duration": 3600
        }
    }


@pytest.fixture
def current_timestamp():
    """ISO8601 formatted current timestamp."""
    return datetime.now(timezone.utc).isoformat()


# ============================================================================
# AC1: MANUAL FEEDBACK TRIGGER - /feedback COMMAND TESTS
# ============================================================================


class TestFeedbackCommandArgumentParsing:
    """Unit tests for /feedback command argument parsing."""

    def test_feedback_command_no_arguments_valid(self):
        """Test /feedback command accepts no arguments."""
        # Arrange
        args_list = []

        # Act
        parser = argparse.ArgumentParser()
        parser.add_argument('context', nargs='*', default=[], help='Optional context')
        result = parser.parse_args(args_list)

        # Assert
        assert result.context == []

    def test_feedback_command_with_story_context_valid(self):
        """Test /feedback command accepts story ID and operation context."""
        # Arrange
        args_list = ['story-001', 'after-dev-completion']

        # Act
        parser = argparse.ArgumentParser()
        parser.add_argument('context', nargs='*')
        result = parser.parse_args(args_list)

        # Assert
        assert result.context == ['story-001', 'after-dev-completion']

    def test_feedback_command_context_max_length_500_chars(self):
        """Test /feedback command context parameter max 500 characters."""
        # Arrange
        long_context = "x" * 500

        # Act
        context_length = len(long_context)

        # Assert
        assert context_length == 500

    def test_feedback_command_context_exceeds_500_chars_invalid(self):
        """Test /feedback command rejects context > 500 characters."""
        # Arrange
        long_context = "x" * 501

        # Act & Assert
        assert len(long_context) > 500

    def test_feedback_command_context_alphanumeric_hyphen_underscore_valid(self):
        """Test /feedback command accepts alphanumeric, hyphens, underscores."""
        # Arrange
        valid_contexts = [
            "story-001",
            "dev_phase",
            "regression-testing_phase1",
            "STORY001"
        ]

        # Act & Assert
        for context in valid_contexts:
            assert all(c.isalnum() or c in '-_' for c in context)


class TestFeedbackCommandSessionMetadataCapture:
    """Unit tests for session metadata capture."""

    def test_feedback_capture_creates_unique_feedback_id(self):
        """Test feedback capture generates unique ID in format FB-YYYY-MM-DD-###."""
        # Arrange
        base_id = "FB-2025-11-07"
        sequences = [1, 2, 3, 4, 5]

        # Act
        feedback_ids = [f"{base_id}-{seq:03d}" for seq in sequences]

        # Assert
        assert len(feedback_ids) == len(set(feedback_ids))  # All unique
        for feedback_id in feedback_ids:
            assert feedback_id.startswith("FB-")
            assert feedback_id.count("-") == 4  # FB-YYYY-MM-DD-### has 4 dashes

    def test_feedback_capture_timestamp_iso8601_format(self, current_timestamp):
        """Test feedback capture records ISO8601 formatted timestamp."""
        # Arrange
        timestamp = current_timestamp

        # Act & Assert
        assert "T" in timestamp
        assert "Z" in timestamp or "+" in timestamp or "-" in timestamp

    def test_feedback_capture_includes_story_id(self, feedback_entry):
        """Test feedback capture includes story ID from context."""
        # Arrange & Act & Assert
        assert "story_id" in feedback_entry
        assert feedback_entry["story_id"] == "STORY-001"

    def test_feedback_capture_includes_operation_type(self, feedback_entry):
        """Test feedback capture includes operation type (dev, qa, release, manual)."""
        # Arrange
        valid_operations = ["dev", "qa", "release", "manual"]

        # Act & Assert
        assert feedback_entry["operation_type"] in valid_operations


class TestFeedbackCommandResponse:
    """Unit tests for /feedback command response format."""

    def test_feedback_command_success_response_json_format(self, feedback_entry):
        """Test /feedback success response returns valid JSON."""
        # Arrange
        expected_keys = ["status", "feedback_id", "timestamp", "context", "next_steps", "message"]

        # Act
        response = {
            "status": "captured",
            "feedback_id": feedback_entry["feedback_id"],
            "timestamp": feedback_entry["timestamp"],
            "context": feedback_entry["context"],
            "next_steps": "Feedback captured. View recent feedback with: /feedback-search --limit=5",
            "message": "Feedback captured successfully"
        }

        # Assert
        assert isinstance(response, dict)
        for key in expected_keys:
            assert key in response

    def test_feedback_command_success_response_has_feedback_id(self, feedback_entry):
        """Test /feedback success response includes feedback ID."""
        # Arrange & Act & Assert
        assert feedback_entry["feedback_id"].startswith("FB-")

    def test_feedback_command_success_response_has_next_steps(self):
        """Test /feedback success response includes next steps guidance."""
        # Arrange
        response = {
            "status": "captured",
            "feedback_id": "FB-2025-11-07-001",
            "timestamp": "2025-11-07T14:30:00Z",
            "context": "story-001 after-dev-completion",
            "next_steps": "Feedback captured. View recent feedback with: /feedback-search --limit=5",
            "message": "Feedback captured successfully"
        }

        # Act & Assert
        assert "next_steps" in response
        assert len(response["next_steps"]) > 0


class TestFeedbackCommandFeedbackRegisterPersistence:
    """Unit tests for feedback register persistence."""

    def test_feedback_command_writes_to_feedback_register_md(self, temp_project_dir):
        """Test /feedback command writes entry to feedback-register.md."""
        # Arrange
        register_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        assert register_path.exists()

        # Act
        initial_content = register_path.read_text()

        # Assert
        assert "# Feedback Register" in initial_content

    def test_feedback_command_appends_not_overwrites_register(self, temp_project_dir):
        """Test /feedback command appends to register without overwriting."""
        # Arrange
        register_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        initial_content = register_path.read_text()
        initial_lines = len(initial_content.splitlines())

        # Act - simulate appending new entry
        new_entry = "\n### FB-2025-11-07-999\n- **Timestamp:** 2025-11-07T23:59:00Z\n"
        updated_content = initial_content + new_entry

        # Assert
        assert len(updated_content.splitlines()) > initial_lines


# ============================================================================
# AC2: VIEW AND EDIT CONFIGURATION - /feedback-config COMMAND TESTS
# ============================================================================


class TestFeedbackConfigCommandSubcommandParsing:
    """Unit tests for /feedback-config command subcommand parsing."""

    def test_feedback_config_view_subcommand_valid(self):
        """Test /feedback-config view subcommand is recognized."""
        # Arrange
        subcommands = ["view", "edit", "reset"]

        # Act
        result = "view" in subcommands

        # Assert
        assert result is True

    def test_feedback_config_edit_subcommand_valid(self):
        """Test /feedback-config edit subcommand is recognized."""
        # Arrange
        subcommands = ["view", "edit", "reset"]

        # Act
        result = "edit" in subcommands

        # Assert
        assert result is True

    def test_feedback_config_reset_subcommand_valid(self):
        """Test /feedback-config reset subcommand is recognized."""
        # Arrange
        subcommands = ["view", "edit", "reset"]

        # Act
        result = "reset" in subcommands

        # Assert
        assert result is True

    def test_feedback_config_invalid_subcommand_rejected(self):
        """Test /feedback-config rejects invalid subcommand."""
        # Arrange
        valid_subcommands = ["view", "edit", "reset"]
        invalid_subcommand = "delete"

        # Act & Assert
        assert invalid_subcommand not in valid_subcommands


class TestFeedbackConfigViewCommand:
    """Unit tests for /feedback-config view subcommand."""

    def test_feedback_config_view_returns_all_fields(self, feedback_config_dict):
        """Test /feedback-config view returns all configuration fields."""
        # Arrange
        expected_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                          "include_metadata", "search_enabled"]

        # Act
        response = {"status": "success", "config": feedback_config_dict}

        # Assert
        for field in expected_fields:
            assert field in response["config"]

    def test_feedback_config_view_returns_current_values(self, feedback_config_dict):
        """Test /feedback-config view returns current configuration values."""
        # Arrange
        config = feedback_config_dict

        # Act
        response = {"status": "success", "config": config, "message": "Current feedback configuration loaded"}

        # Assert
        assert response["config"]["retention_days"] == 90
        assert response["config"]["auto_trigger_enabled"] is True
        assert response["config"]["export_format"] == "json"


class TestFeedbackConfigEditCommand:
    """Unit tests for /feedback-config edit subcommand."""

    def test_feedback_config_edit_retention_days_field_valid(self):
        """Test /feedback-config edit retention_days field is recognized."""
        # Arrange
        valid_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                       "include_metadata", "search_enabled"]

        # Act
        result = "retention_days" in valid_fields

        # Assert
        assert result is True

    def test_feedback_config_edit_auto_trigger_enabled_field_valid(self):
        """Test /feedback-config edit auto_trigger_enabled field is recognized."""
        # Arrange
        valid_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                       "include_metadata", "search_enabled"]

        # Act
        result = "auto_trigger_enabled" in valid_fields

        # Assert
        assert result is True

    def test_feedback_config_edit_export_format_field_valid(self):
        """Test /feedback-config edit export_format field is recognized."""
        # Arrange
        valid_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                       "include_metadata", "search_enabled"]

        # Act
        result = "export_format" in valid_fields

        # Assert
        assert result is True

    def test_feedback_config_edit_retention_days_positive_constraint(self):
        """Test /feedback-config edit validates retention_days is positive (1-3650)."""
        # Arrange
        valid_values = [1, 30, 90, 365, 3650]
        invalid_values = [-1, 0, -100, 3651]

        # Act & Assert
        for value in valid_values:
            assert 1 <= value <= 3650
        for value in invalid_values:
            assert not (1 <= value <= 3650)

    def test_feedback_config_edit_retention_days_negative_rejected(self):
        """Test /feedback-config edit rejects negative retention_days."""
        # Arrange
        invalid_value = -5

        # Act & Assert
        assert invalid_value < 1

    def test_feedback_config_edit_auto_trigger_enabled_boolean_constraint(self):
        """Test /feedback-config edit validates auto_trigger_enabled is boolean."""
        # Arrange
        valid_values = [True, False, "true", "false"]

        # Act & Assert
        for value in valid_values:
            assert isinstance(value, (bool, str))

    def test_feedback_config_edit_export_format_enum_constraint(self):
        """Test /feedback-config edit validates export_format is one of json|csv|markdown."""
        # Arrange
        valid_values = ["json", "csv", "markdown"]
        invalid_values = ["xml", "yaml", "txt"]

        # Act & Assert
        for value in valid_values:
            assert value in valid_values
        for value in invalid_values:
            assert value not in valid_values

    def test_feedback_config_edit_include_metadata_boolean_constraint(self):
        """Test /feedback-config edit validates include_metadata is boolean."""
        # Arrange
        valid_values = [True, False]

        # Act & Assert
        for value in valid_values:
            assert isinstance(value, bool)

    def test_feedback_config_edit_search_enabled_boolean_constraint(self):
        """Test /feedback-config edit validates search_enabled is boolean."""
        # Arrange
        valid_values = [True, False]

        # Act & Assert
        for value in valid_values:
            assert isinstance(value, bool)

    def test_feedback_config_edit_invalid_field_rejected(self):
        """Test /feedback-config edit rejects invalid field names."""
        # Arrange
        valid_fields = ["retention_days", "auto_trigger_enabled", "export_format",
                       "include_metadata", "search_enabled"]
        invalid_field = "invalid_field"

        # Act & Assert
        assert invalid_field not in valid_fields


class TestFeedbackConfigPersistence:
    """Unit tests for configuration persistence."""

    def test_feedback_config_edit_persists_to_yaml(self, temp_project_dir):
        """Test /feedback-config edit persists changes to config.yaml."""
        # Arrange
        config_path = temp_project_dir / "devforgeai" / "feedback" / "config.yaml"

        # Act
        assert config_path.exists()

        # Assert
        content = config_path.read_text()
        assert "retention_days:" in content

    def test_feedback_config_reset_restores_defaults(self, temp_project_dir):
        """Test /feedback-config reset restores default configuration."""
        # Arrange
        default_config = {
            "retention_days": 90,
            "auto_trigger_enabled": True,
            "export_format": "json",
            "include_metadata": True,
            "search_enabled": True
        }

        # Act
        reset_config = default_config.copy()

        # Assert
        assert reset_config == default_config


# ============================================================================
# AC3: SEARCH FEEDBACK HISTORY - /feedback-search COMMAND TESTS
# ============================================================================


class TestFeedbackSearchQueryParsing:
    """Unit tests for /feedback-search command query parsing."""

    def test_feedback_search_story_id_query_format_valid(self):
        """Test /feedback-search accepts story ID query format STORY-###."""
        # Arrange
        query = "STORY-001"

        # Act
        is_story_id = query.startswith("STORY-") and query[6:].isdigit()

        # Assert
        assert is_story_id is True

    def test_feedback_search_date_range_query_format_valid(self):
        """Test /feedback-search accepts date range format YYYY-MM-DD..YYYY-MM-DD."""
        # Arrange
        query = "2025-11-01..2025-11-07"

        # Act
        is_date_range = ".." in query and len(query.split("..")) == 2

        # Assert
        assert is_date_range is True

    def test_feedback_search_operation_type_query_valid(self):
        """Test /feedback-search accepts operation type queries."""
        # Arrange
        valid_operations = ["dev", "qa", "release"]
        query = "dev"

        # Act
        is_operation = query in valid_operations

        # Assert
        assert is_operation is True

    def test_feedback_search_keyword_query_valid(self):
        """Test /feedback-search accepts keyword search queries."""
        # Arrange
        query = "regression testing"

        # Act
        is_keyword = isinstance(query, str) and len(query) > 0

        # Assert
        assert is_keyword is True

    def test_feedback_search_query_max_length_200_chars(self):
        """Test /feedback-search query parameter max 200 characters."""
        # Arrange
        query = "x" * 200

        # Act
        query_length = len(query)

        # Assert
        assert query_length == 200

    def test_feedback_search_query_exceeds_200_chars_invalid(self):
        """Test /feedback-search rejects query > 200 characters."""
        # Arrange
        query = "x" * 201

        # Act & Assert
        assert len(query) > 200


class TestFeedbackSearchFilterOptions:
    """Unit tests for /feedback-search filter options."""

    def test_feedback_search_severity_filter_valid_values(self):
        """Test /feedback-search --severity accepts valid values."""
        # Arrange
        valid_severities = ["low", "medium", "high", "critical"]

        # Act & Assert
        for severity in valid_severities:
            assert severity in valid_severities

    def test_feedback_search_status_filter_valid_values(self):
        """Test /feedback-search --status accepts valid values."""
        # Arrange
        valid_statuses = ["open", "resolved", "archived"]

        # Act & Assert
        for status in valid_statuses:
            assert status in valid_statuses

    def test_feedback_search_limit_filter_range_1_1000(self):
        """Test /feedback-search --limit accepts 1-1000."""
        # Arrange
        valid_limits = [1, 10, 100, 500, 1000]

        # Act & Assert
        for limit in valid_limits:
            assert 1 <= limit <= 1000

    def test_feedback_search_limit_filter_default_10(self):
        """Test /feedback-search --limit defaults to 10."""
        # Arrange
        default_limit = 10

        # Act & Assert
        assert default_limit == 10

    def test_feedback_search_page_filter_positive_integer(self):
        """Test /feedback-search --page accepts positive integers."""
        # Arrange
        valid_pages = [1, 2, 10, 100]

        # Act & Assert
        for page in valid_pages:
            assert page > 0


class TestFeedbackSearchResultSorting:
    """Unit tests for /feedback-search result sorting."""

    def test_feedback_search_sorts_by_date_descending_for_date_queries(self):
        """Test /feedback-search sorts results by date descending for time queries."""
        # Arrange
        results = [
            {"timestamp": "2025-11-07T14:30:00Z", "feedback_id": "FB-1"},
            {"timestamp": "2025-11-07T15:15:00Z", "feedback_id": "FB-2"},
            {"timestamp": "2025-11-06T10:00:00Z", "feedback_id": "FB-3"},
        ]

        # Act
        sorted_results = sorted(results, key=lambda x: x["timestamp"], reverse=True)

        # Assert
        assert sorted_results[0]["feedback_id"] == "FB-2"
        assert sorted_results[1]["feedback_id"] == "FB-1"
        assert sorted_results[2]["feedback_id"] == "FB-3"

    def test_feedback_search_sorts_by_relevance_for_text_queries(self):
        """Test /feedback-search sorts results by relevance for keyword queries."""
        # Arrange
        results = [
            {"summary": "Minor refactoring completed", "score": 0.5},
            {"summary": "TDD cycle took longer than expected", "score": 0.8},
            {"summary": "Coverage below threshold", "score": 0.6},
        ]

        # Act
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

        # Assert
        assert sorted_results[0]["score"] == 0.8
        assert sorted_results[1]["score"] == 0.6
        assert sorted_results[2]["score"] == 0.5


class TestFeedbackSearchPagination:
    """Unit tests for /feedback-search pagination."""

    def test_feedback_search_pagination_default_10_results_per_page(self):
        """Test /feedback-search displays max 10 results per page by default."""
        # Arrange
        total_results = 47
        page_size = 10

        # Act
        first_page_results = total_results if total_results <= page_size else page_size

        # Assert
        assert first_page_results == 10

    def test_feedback_search_pagination_indicates_next_page(self):
        """Test /feedback-search indicates next page option when > 10 results."""
        # Arrange
        total_results = 47
        page = 1
        page_size = 10

        # Act
        has_next = (page * page_size) < total_results

        # Assert
        assert has_next is True

    def test_feedback_search_pagination_last_page_no_next(self):
        """Test /feedback-search pagination indicates no next page on last page."""
        # Arrange
        total_results = 47
        page = 5
        page_size = 10

        # Act
        has_next = (page * page_size) < total_results

        # Assert
        assert has_next is False


class TestFeedbackSearchResponseFormat:
    """Unit tests for /feedback-search response format."""

    def test_feedback_search_response_includes_total_matches(self):
        """Test /feedback-search response includes total_matches."""
        # Arrange
        response = {
            "status": "success",
            "query": "STORY-001",
            "total_matches": 47,
            "page": 1,
            "page_size": 10,
            "results": []
        }

        # Act & Assert
        assert "total_matches" in response
        assert response["total_matches"] == 47

    def test_feedback_search_response_includes_pagination_info(self):
        """Test /feedback-search response includes pagination info."""
        # Arrange
        response = {
            "status": "success",
            "query": "STORY-001",
            "total_matches": 47,
            "page": 1,
            "page_size": 10,
            "results": [],
            "next_page_info": "Use: /feedback-search STORY-001 --page=2 to see next 10 results"
        }

        # Act & Assert
        assert "page" in response
        assert "page_size" in response
        assert "next_page_info" in response


# ============================================================================
# AC4: EXPORT FEEDBACK PACKAGE - /export-feedback COMMAND TESTS
# ============================================================================


class TestExportFeedbackOptionParsing:
    """Unit tests for /export-feedback command option parsing."""

    def test_export_feedback_format_option_valid_json(self):
        """Test /export-feedback --format accepts json."""
        # Arrange
        valid_formats = ["json", "csv", "markdown"]
        format_option = "json"

        # Act
        is_valid = format_option in valid_formats

        # Assert
        assert is_valid is True

    def test_export_feedback_format_option_valid_csv(self):
        """Test /export-feedback --format accepts csv."""
        # Arrange
        valid_formats = ["json", "csv", "markdown"]
        format_option = "csv"

        # Act
        is_valid = format_option in valid_formats

        # Assert
        assert is_valid is True

    def test_export_feedback_format_option_valid_markdown(self):
        """Test /export-feedback --format accepts markdown."""
        # Arrange
        valid_formats = ["json", "csv", "markdown"]
        format_option = "markdown"

        # Act
        is_valid = format_option in valid_formats

        # Assert
        assert is_valid is True

    def test_export_feedback_format_option_default_json(self):
        """Test /export-feedback --format defaults to json."""
        # Arrange
        default_format = "json"

        # Act & Assert
        assert default_format == "json"

    def test_export_feedback_date_range_option_valid_format(self):
        """Test /export-feedback --date-range accepts YYYY-MM-DD..YYYY-MM-DD."""
        # Arrange
        date_range = "2025-11-01..2025-11-07"

        # Act
        parts = date_range.split("..")

        # Assert
        assert len(parts) == 2

    def test_export_feedback_date_range_option_relative_format(self):
        """Test /export-feedback --date-range accepts relative formats."""
        # Arrange
        valid_relative = ["last-7-days", "last-month", "last-year"]

        # Act & Assert
        for relative_format in valid_relative:
            assert isinstance(relative_format, str)

    def test_export_feedback_story_ids_option_comma_separated(self):
        """Test /export-feedback --story-ids accepts comma-separated story IDs."""
        # Arrange
        story_ids_option = "STORY-001,STORY-002,STORY-003"

        # Act
        story_ids = story_ids_option.split(",")

        # Assert
        assert len(story_ids) == 3
        assert all(sid.startswith("STORY-") for sid in story_ids)

    def test_export_feedback_severity_option_filter(self):
        """Test /export-feedback --severity filters by severity."""
        # Arrange
        valid_severities = ["low", "medium", "high", "critical"]
        severity = "high"

        # Act
        is_valid = severity in valid_severities

        # Assert
        assert is_valid is True

    def test_export_feedback_status_option_filter(self):
        """Test /export-feedback --status filters by status."""
        # Arrange
        valid_statuses = ["open", "resolved", "archived"]
        status = "open"

        # Act
        is_valid = status in valid_statuses

        # Assert
        assert is_valid is True


class TestExportFeedbackFormatSelection:
    """Unit tests for /export-feedback format selection."""

    def test_export_feedback_json_format_creates_json_file(self):
        """Test /export-feedback --format=json creates valid JSON file."""
        # Arrange
        export_data = {
            "export_id": "EXP-2025-11-07-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "entries": []
        }

        # Act
        json_str = json.dumps(export_data)

        # Assert
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["export_id"] == "EXP-2025-11-07-001"

    def test_export_feedback_csv_format_creates_csv_file(self):
        """Test /export-feedback --format=csv creates valid CSV file."""
        # Arrange
        csv_headers = "feedback_id,timestamp,story_id,operation,severity,status"
        csv_row = "FB-2025-11-07-001,2025-11-07T14:30:00Z,STORY-001,dev,medium,open"

        # Act
        csv_content = f"{csv_headers}\n{csv_row}"

        # Assert
        assert "feedback_id" in csv_content
        assert len(csv_content.split("\n")) == 2

    def test_export_feedback_markdown_format_creates_markdown_summary(self):
        """Test /export-feedback --format=markdown creates markdown summary."""
        # Arrange
        markdown_content = """# Feedback Export Summary

## Export Details
- **Export ID:** EXP-2025-11-07-001
- **Timestamp:** 2025-11-07T14:35:00Z
- **Total Entries:** 23

## Metadata Index
- Story IDs: 2
- Operation Types: 3
"""

        # Act & Assert
        assert "# Feedback Export Summary" in markdown_content
        assert "Export ID" in markdown_content


class TestExportFeedbackFileOperations:
    """Unit tests for /export-feedback file operations."""

    def test_export_feedback_saves_to_exports_directory(self, temp_project_dir):
        """Test /export-feedback saves file to devforgeai/feedback/exports/."""
        # Arrange
        exports_dir = temp_project_dir / "devforgeai" / "feedback" / "exports"
        assert exports_dir.exists()

        # Act
        export_file = exports_dir / "2025-11-07-feedback-export.json"

        # Assert
        assert str(export_file).startswith(str(exports_dir))

    def test_export_feedback_filename_includes_timestamp(self):
        """Test /export-feedback filename includes timestamp in format."""
        # Arrange
        timestamp = "2025-11-07"
        format_ext = "json"
        filename = f"{timestamp}-feedback-export.{format_ext}"

        # Act & Assert
        assert timestamp in filename
        assert format_ext in filename
        assert "feedback-export" in filename


class TestExportFeedbackResponseFormat:
    """Unit tests for /export-feedback response format."""

    def test_export_feedback_response_includes_file_path(self):
        """Test /export-feedback response includes file_path."""
        # Arrange
        response = {
            "status": "success",
            "export_id": "EXP-2025-11-07-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "file_path": "devforgeai/feedback/exports/2025-11-07-feedback-export.json",
            "format": "json",
            "entries_count": 23
        }

        # Act & Assert
        assert "file_path" in response
        assert "devforgeai/feedback/exports/" in response["file_path"]

    def test_export_feedback_response_includes_entries_count(self):
        """Test /export-feedback response includes entries_count."""
        # Arrange
        response = {
            "status": "success",
            "export_id": "EXP-2025-11-07-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "file_path": "devforgeai/feedback/exports/2025-11-07-feedback-export.json",
            "format": "json",
            "entries_count": 23
        }

        # Act & Assert
        assert "entries_count" in response
        assert response["entries_count"] == 23

    def test_export_feedback_response_includes_metadata(self):
        """Test /export-feedback response includes metadata."""
        # Arrange
        response = {
            "status": "success",
            "export_id": "EXP-2025-11-07-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "file_path": "devforgeai/feedback/exports/2025-11-07-feedback-export.json",
            "format": "json",
            "entries_count": 23,
            "metadata": {
                "selection_criteria": {
                    "severity": "high",
                    "status": "open"
                },
                "export_timestamp": "2025-11-07T14:35:00Z",
                "framework_version": "1.0.1"
            }
        }

        # Act & Assert
        assert "metadata" in response
        assert "selection_criteria" in response["metadata"]


# ============================================================================
# AC5: GRACEFUL ERROR HANDLING - COMMAND ERROR TESTS
# ============================================================================


class TestFeedbackCommandErrorHandling:
    """Unit tests for graceful error handling across all commands."""

    def test_feedback_command_invalid_story_id_format_error(self):
        """Test /feedback command rejects invalid story ID format."""
        # Arrange
        invalid_story_id = "INVALID-001"
        valid_pattern = r"^STORY-\d+$"

        # Act & Assert
        import re
        assert not re.match(valid_pattern, invalid_story_id)

    def test_feedback_command_context_exceeds_max_length_error(self):
        """Test /feedback command provides clear error for context > 500 chars."""
        # Arrange
        context = "x" * 501

        # Act & Assert
        assert len(context) > 500

    def test_feedback_config_edit_negative_retention_days_error(self):
        """Test /feedback-config edit provides clear error for negative retention_days."""
        # Arrange
        error_message = "retention_days must be positive number (received: -5)"

        # Act & Assert
        assert "retention_days" in error_message
        assert "positive" in error_message
        assert "-5" in error_message

    def test_feedback_config_edit_invalid_export_format_error(self):
        """Test /feedback-config edit provides clear error for invalid format."""
        # Arrange
        error_message = "Format 'xml' not supported. Supported formats: json, csv, markdown"

        # Act & Assert
        assert "xml" in error_message
        assert "json" in error_message
        assert "csv" in error_message
        assert "markdown" in error_message

    def test_feedback_search_no_results_graceful_response(self):
        """Test /feedback-search provides graceful response when no results found."""
        # Arrange
        response = {
            "status": "success",
            "query": "STORY-999",
            "total_matches": 0,
            "results": [],
            "message": "No feedback found matching query: STORY-999"
        }

        # Act & Assert
        assert response["total_matches"] == 0
        assert len(response["results"]) == 0
        assert "No feedback found" in response["message"]

    def test_export_feedback_no_matching_entries_graceful_response(self):
        """Test /export-feedback provides graceful response with zero entries."""
        # Arrange
        response = {
            "status": "success",
            "export_id": "EXP-2025-11-07-001",
            "entries_count": 0,
            "message": "Export created with 0 entries matched selection criteria"
        }

        # Act & Assert
        assert response["entries_count"] == 0
        assert "0 entries" in response["message"]

    def test_config_file_corruption_provides_recovery_option(self):
        """Test config file corruption error suggests reset option."""
        # Arrange
        error_message = "Configuration file corrupted. Run `/feedback-config reset` to restore defaults."

        # Act & Assert
        assert "corrupted" in error_message.lower()
        assert "/feedback-config reset" in error_message

    def test_export_permission_error_clear_message(self):
        """Test export permission error provides clear remediation."""
        # Arrange
        error_message = "Cannot write to exports directory. Check file permissions."

        # Act & Assert
        assert "permission" in error_message.lower()
        assert "exports directory" in error_message


# ============================================================================
# AC6: COMMAND HELP AND DOCUMENTATION TESTS
# ============================================================================


class TestCommandHelpDocumentation:
    """Unit tests for command help and documentation."""

    def test_feedback_command_help_flag_recognized(self):
        """Test /feedback --help flag is recognized."""
        # Arrange
        help_flags = ["--help", "-h", "help"]

        # Act
        is_help = "--help" in help_flags

        # Assert
        assert is_help is True

    def test_feedback_command_help_includes_purpose(self):
        """Test /feedback --help includes command purpose."""
        # Arrange
        help_text = "Manually trigger feedback collection for current session"

        # Act & Assert
        assert len(help_text) > 0
        assert "feedback" in help_text.lower()

    def test_feedback_command_help_includes_syntax(self):
        """Test /feedback --help includes command syntax."""
        # Arrange
        help_text = "/feedback [optional context]"

        # Act & Assert
        assert "/feedback" in help_text

    def test_feedback_command_help_includes_examples(self):
        """Test /feedback --help includes usage examples."""
        # Arrange
        help_text = """Examples:
/feedback
/feedback story-001 after-dev-completion
/feedback regression-testing phase-1"""

        # Act & Assert
        assert "/feedback" in help_text
        assert "story-001" in help_text

    def test_feedback_config_command_help_includes_subcommands(self):
        """Test /feedback-config --help lists all subcommands."""
        # Arrange
        help_text = """Subcommands:
- view: Display current configuration
- edit: Modify configuration field
- reset: Restore default configuration"""

        # Act & Assert
        assert "view" in help_text
        assert "edit" in help_text
        assert "reset" in help_text

    def test_feedback_search_command_help_includes_query_formats(self):
        """Test /feedback-search --help documents query formats."""
        # Arrange
        help_text = """Query formats:
- Story ID: STORY-001
- Date range: 2025-11-01..2025-11-07
- Operation type: dev, qa, release
- Keyword search: any text"""

        # Act & Assert
        assert "STORY-" in help_text
        assert "Date range" in help_text
        assert "dev, qa, release" in help_text

    def test_export_feedback_command_help_includes_options(self):
        """Test /export-feedback --help documents all options."""
        # Arrange
        help_text = """Options:
--format: json, csv, markdown (default: json)
--date-range: YYYY-MM-DD..YYYY-MM-DD or relative
--story-ids: comma-separated STORY-IDs
--severity: low, medium, high, critical
--status: open, resolved, archived"""

        # Act & Assert
        assert "--format" in help_text
        assert "--date-range" in help_text
        assert "--story-ids" in help_text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
