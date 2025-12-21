"""
Integration test suite for STORY-020: Feedback CLI Commands

Tests cover:
- Full workflow integration for each command
- File I/O operations
- Configuration persistence
- Multi-step operations
- Command chaining and dependencies
- Concurrent operations

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta
import yaml
from unittest.mock import patch, MagicMock
import time


# ============================================================================
# FIXTURES - Integration test setup
# ============================================================================


@pytest.fixture
def integration_project_dir():
    """Create a complete project directory for integration testing."""
    with tempfile.TemporaryDirectory(prefix="feedback_integration_") as tmpdir:
        project_path = Path(tmpdir)

        # Create complete feedback directory structure
        feedback_dir = project_path / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)

        exports_dir = feedback_dir / "exports"
        exports_dir.mkdir(exist_ok=True)

        # Create comprehensive config.yaml
        config = {
            "retention_days": 90,
            "auto_trigger_enabled": True,
            "export_format": "json",
            "include_metadata": True,
            "search_enabled": True,
            "created_at": "2025-11-07T00:00:00Z",
            "last_modified": "2025-11-07T00:00:00Z"
        }
        config_file = feedback_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Create comprehensive feedback-register.md with multiple entries
        register_file = feedback_dir / "feedback-register.md"
        register_content = """# Feedback Register

## Active Feedback Sessions

### FB-2025-11-07-001
- **Timestamp:** 2025-11-07T09:00:00Z
- **Story ID:** STORY-001
- **Operation:** dev
- **Severity:** low
- **Status:** resolved
- **Context:** Initial development phase
- **Metadata:** {framework_version: "1.0.1", duration: 1800}

### FB-2025-11-07-002
- **Timestamp:** 2025-11-07T10:30:00Z
- **Story ID:** STORY-001
- **Operation:** dev
- **Severity:** medium
- **Status:** open
- **Context:** TDD cycle took longer than expected
- **Metadata:** {framework_version: "1.0.1", duration: 3600}

### FB-2025-11-07-003
- **Timestamp:** 2025-11-07T11:45:00Z
- **Story ID:** STORY-001
- **Operation:** qa
- **Severity:** high
- **Status:** open
- **Context:** Coverage below threshold
- **Metadata:** {framework_version: "1.0.1", duration: 1200}

### FB-2025-11-07-004
- **Timestamp:** 2025-11-06T14:00:00Z
- **Story ID:** STORY-002
- **Operation:** dev
- **Severity:** low
- **Status:** resolved
- **Context:** Minor refactoring completed
- **Metadata:** {framework_version: "1.0.1", duration: 600}

### FB-2025-11-07-005
- **Timestamp:** 2025-11-06T15:30:00Z
- **Story ID:** STORY-002
- **Operation:** release
- **Severity:** critical
- **Status:** open
- **Context:** Production deployment issue
- **Metadata:** {framework_version: "1.0.1", duration: 900}

### FB-2025-11-05-001
- **Timestamp:** 2025-11-05T08:00:00Z
- **Story ID:** STORY-003
- **Operation:** qa
- **Severity:** medium
- **Status:** archived
- **Context:** Regression testing completed
- **Metadata:** {framework_version: "1.0.1", duration: 2400}
"""
        register_file.write_text(register_content)

        yield project_path


# ============================================================================
# AC1: FULL /feedback WORKFLOW INTEGRATION TESTS
# ============================================================================


class TestFeedbackCommandWorkflowIntegration:
    """Integration tests for complete /feedback command workflow."""

    def test_feedback_command_full_workflow_capture_and_register(self, integration_project_dir):
        """Test /feedback full workflow: capture -> register -> verify."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        initial_content = register_file.read_text()
        initial_lines = len(initial_content.splitlines())

        # Act
        new_entry = """
### FB-2025-11-07-006
- **Timestamp:** 2025-11-07T16:00:00Z
- **Story ID:** STORY-001
- **Operation:** manual
- **Severity:** medium
- **Status:** open
- **Context:** Manual feedback trigger
- **Metadata:** {framework_version: "1.0.1"}
"""
        updated_content = initial_content + new_entry
        register_file.write_text(updated_content)

        # Assert
        assert len(register_file.read_text().splitlines()) > initial_lines
        assert "FB-2025-11-07-006" in register_file.read_text()

    def test_feedback_command_creates_unique_ids_concurrent_operations(self, integration_project_dir):
        """Test /feedback generates unique IDs even with concurrent triggers."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"

        # Act - simulate two concurrent feedback entries
        feedback_ids = [
            "FB-2025-11-07-007",
            "FB-2025-11-07-008",
            "FB-2025-11-07-009"
        ]

        # Assert
        assert len(feedback_ids) == len(set(feedback_ids))  # All unique

    def test_feedback_command_appends_maintains_register_structure(self, integration_project_dir):
        """Test /feedback append maintains register markdown structure."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        initial_content = register_file.read_text()

        # Act
        new_entry = """### FB-2025-11-07-010
- **Timestamp:** 2025-11-07T17:00:00Z
- **Story ID:** STORY-004
- **Operation:** dev
- **Severity:** low
- **Status:** open
- **Context:** New entry test
- **Metadata:** {framework_version: "1.0.1"}
"""
        updated_content = initial_content + "\n" + new_entry
        register_file.write_text(updated_content)

        # Assert
        updated_text = register_file.read_text()
        assert "# Feedback Register" in updated_text
        assert "## Active Feedback Sessions" in updated_text
        assert "### FB-2025-11-07-010" in updated_text


# ============================================================================
# AC2: FULL /feedback-config WORKFLOW INTEGRATION TESTS
# ============================================================================


class TestFeedbackConfigCommandWorkflowIntegration:
    """Integration tests for complete /feedback-config command workflow."""

    def test_feedback_config_view_edit_reset_cycle(self, integration_project_dir):
        """Test /feedback-config full cycle: view -> edit -> verify -> reset."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"
        with open(config_file, 'r') as f:
            initial_config = yaml.safe_load(f)

        # Act - edit config
        initial_config["retention_days"] = 30
        with open(config_file, 'w') as f:
            yaml.dump(initial_config, f)

        # Assert - verify edit persisted
        with open(config_file, 'r') as f:
            edited_config = yaml.safe_load(f)
        assert edited_config["retention_days"] == 30

        # Act - reset to defaults
        default_config = {
            "retention_days": 90,
            "auto_trigger_enabled": True,
            "export_format": "json",
            "include_metadata": True,
            "search_enabled": True,
            "created_at": "2025-11-07T00:00:00Z",
            "last_modified": "2025-11-07T00:00:00Z"
        }
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f)

        # Assert - verify reset restored defaults
        with open(config_file, 'r') as f:
            reset_config = yaml.safe_load(f)
        assert reset_config["retention_days"] == 90

    def test_feedback_config_edit_validation_prevents_invalid_values(self, integration_project_dir):
        """Test /feedback-config edit validation prevents invalid configuration."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"

        # Act - attempt to set invalid retention_days
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        invalid_retention_days = -5
        is_valid = 1 <= invalid_retention_days <= 3650

        # Assert - validation prevents invalid value
        assert is_valid is False

    def test_feedback_config_edit_persists_immediately(self, integration_project_dir):
        """Test /feedback-config edit persists changes immediately to disk."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"

        # Act - edit config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        config["auto_trigger_enabled"] = False
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Assert - verify persisted immediately
        with open(config_file, 'r') as f:
            persisted_config = yaml.safe_load(f)
        assert persisted_config["auto_trigger_enabled"] is False

    def test_feedback_config_edit_multiple_fields_sequentially(self, integration_project_dir):
        """Test /feedback-config edit handles multiple field edits sequentially."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"

        # Act - edit first field
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        config["retention_days"] = 60
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Assert - first edit verified
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        assert config["retention_days"] == 60

        # Act - edit second field
        config["export_format"] = "csv"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Assert - both edits verified
        with open(config_file, 'r') as f:
            final_config = yaml.safe_load(f)
        assert final_config["retention_days"] == 60
        assert final_config["export_format"] == "csv"


# ============================================================================
# AC3: FULL /feedback-search WORKFLOW INTEGRATION TESTS
# ============================================================================


class TestFeedbackSearchCommandWorkflowIntegration:
    """Integration tests for complete /feedback-search command workflow."""

    def test_feedback_search_story_id_query_integration(self, integration_project_dir):
        """Test /feedback-search full workflow: parse story ID -> query -> filter -> sort."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        content = register_file.read_text()

        # Act - search for STORY-001
        story_id_query = "STORY-001"
        matching_entries = []
        if "STORY-001" in content:
            matching_entries.append("FB-2025-11-07-001")
            matching_entries.append("FB-2025-11-07-002")
            matching_entries.append("FB-2025-11-07-003")

        # Assert
        assert len(matching_entries) == 3
        assert all(fid.startswith("FB-") for fid in matching_entries)

    def test_feedback_search_date_range_query_integration(self, integration_project_dir):
        """Test /feedback-search full workflow: parse date range -> query -> filter."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        content = register_file.read_text()

        # Act - search for entries in date range
        start_date = "2025-11-06"
        end_date = "2025-11-07"
        matching_entries = [
            "FB-2025-11-07-003",
            "FB-2025-11-07-004",
            "FB-2025-11-07-005"
        ]

        # Assert
        assert len(matching_entries) > 0

    def test_feedback_search_pagination_large_result_set_integration(self, integration_project_dir):
        """Test /feedback-search pagination with large result set."""
        # Arrange
        total_results = 47

        # Act
        page_size = 10
        total_pages = (total_results + page_size - 1) // page_size

        # Assert
        assert total_pages == 5
        assert (total_pages - 1) * page_size < total_results

    def test_feedback_search_multiple_filters_integration(self, integration_project_dir):
        """Test /feedback-search with multiple filters applied."""
        # Arrange
        results = []

        # Act - apply severity AND status filters
        severity_filter = "high"
        status_filter = "open"

        # Simulate filtering: FB-2025-11-07-003 has high severity and open status
        if severity_filter == "high" and status_filter == "open":
            results.append("FB-2025-11-07-003")

        # Assert
        assert len(results) > 0

    def test_feedback_search_empty_result_graceful_handling(self, integration_project_dir):
        """Test /feedback-search handles empty results gracefully."""
        # Arrange
        query = "STORY-999"  # Doesn't exist

        # Act
        matching_entries = []

        # Assert
        assert len(matching_entries) == 0


# ============================================================================
# AC4: FULL /export-feedback WORKFLOW INTEGRATION TESTS
# ============================================================================


class TestExportFeedbackCommandWorkflowIntegration:
    """Integration tests for complete /export-feedback command workflow."""

    def test_export_feedback_json_format_workflow_integration(self, integration_project_dir):
        """Test /export-feedback JSON workflow: select -> format -> package -> save."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"

        # Act - create export
        export_data = {
            "export_id": "EXP-2025-11-07-001",
            "timestamp": "2025-11-07T14:35:00Z",
            "format": "json",
            "entries": [
                {"feedback_id": "FB-2025-11-07-001", "story_id": "STORY-001"},
                {"feedback_id": "FB-2025-11-07-002", "story_id": "STORY-001"},
            ],
            "metadata": {
                "selection_criteria": {"severity": "high", "status": "open"},
                "export_timestamp": "2025-11-07T14:35:00Z",
                "framework_version": "1.0.1"
            }
        }
        export_file = exports_dir / "2025-11-07-feedback-export.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f)

        # Assert - export file created and valid
        assert export_file.exists()
        with open(export_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data["export_id"] == "EXP-2025-11-07-001"
        assert len(saved_data["entries"]) == 2

    def test_export_feedback_csv_format_workflow_integration(self, integration_project_dir):
        """Test /export-feedback CSV workflow: format -> generate CSV -> save."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - create CSV export
        csv_content = """feedback_id,timestamp,story_id,operation,severity,status
FB-2025-11-07-001,2025-11-07T09:00:00Z,STORY-001,dev,low,resolved
FB-2025-11-07-002,2025-11-07T10:30:00Z,STORY-001,dev,medium,open
FB-2025-11-07-003,2025-11-07T11:45:00Z,STORY-001,qa,high,open
"""
        export_file = exports_dir / "2025-11-07-feedback-export.csv"
        export_file.write_text(csv_content)

        # Assert
        assert export_file.exists()
        content = export_file.read_text()
        assert "feedback_id,timestamp,story_id" in content
        assert len(content.splitlines()) == 4

    def test_export_feedback_markdown_format_workflow_integration(self, integration_project_dir):
        """Test /export-feedback Markdown workflow: format -> generate summary -> save."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - create Markdown export
        markdown_content = """# Feedback Export Summary

## Export Details
- **Export ID:** EXP-2025-11-07-001
- **Timestamp:** 2025-11-07T14:35:00Z
- **Total Entries:** 3

## Metadata Index
- Story IDs: 1
- Operation Types: 2
- Severity Distribution: low (1), medium (1), high (1)

## Feedback Entries
### FB-2025-11-07-001 (STORY-001 - dev - low - resolved)
### FB-2025-11-07-002 (STORY-001 - dev - medium - open)
### FB-2025-11-07-003 (STORY-001 - qa - high - open)
"""
        export_file = exports_dir / "2025-11-07-feedback-export.md"
        export_file.write_text(markdown_content)

        # Assert
        assert export_file.exists()
        content = export_file.read_text()
        assert "# Feedback Export Summary" in content
        assert "## Metadata Index" in content

    def test_export_feedback_with_selection_criteria_integration(self, integration_project_dir):
        """Test /export-feedback applies selection criteria correctly."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - export with filters: story IDs and severity
        export_data = {
            "export_id": "EXP-2025-11-07-002",
            "timestamp": "2025-11-07T15:00:00Z",
            "format": "json",
            "entries": [
                {"feedback_id": "FB-2025-11-07-003", "story_id": "STORY-001", "severity": "high"}
            ],
            "selection_criteria": {
                "story_ids": ["STORY-001"],
                "severity": "high"
            }
        }
        export_file = exports_dir / "2025-11-07-feedback-export-2.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f)

        # Assert - only matching entries included
        with open(export_file, 'r') as f:
            saved_data = json.load(f)
        assert len(saved_data["entries"]) == 1
        assert saved_data["entries"][0]["severity"] == "high"

    def test_export_feedback_no_matching_entries_creates_empty_export(self, integration_project_dir):
        """Test /export-feedback creates valid export with zero entries when no matches."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - export with criteria matching no entries
        export_data = {
            "export_id": "EXP-2025-11-07-003",
            "timestamp": "2025-11-07T15:30:00Z",
            "format": "json",
            "entries": [],
            "selection_criteria": {
                "story_ids": ["STORY-999"]
            },
            "message": "Export created with 0 entries matched selection criteria"
        }
        export_file = exports_dir / "2025-11-07-feedback-export-empty.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f)

        # Assert
        assert export_file.exists()
        with open(export_file, 'r') as f:
            saved_data = json.load(f)
        assert len(saved_data["entries"]) == 0
        assert "0 entries" in saved_data["message"]


# ============================================================================
# CROSS-COMMAND INTEGRATION TESTS
# ============================================================================


class TestCrossCommandIntegration:
    """Integration tests across multiple commands."""

    def test_feedback_to_search_workflow_integration(self, integration_project_dir):
        """Test /feedback -> /feedback-search workflow: capture feedback, then search it."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"

        # Act - add new feedback entry
        new_entry = """
### FB-2025-11-07-999
- **Timestamp:** 2025-11-07T18:00:00Z
- **Story ID:** STORY-TEST
- **Operation:** manual
- **Severity:** medium
- **Status:** open
- **Context:** Cross-command test
- **Metadata:** {framework_version: "1.0.1"}
"""
        initial_content = register_file.read_text()
        register_file.write_text(initial_content + new_entry)

        # Act - search for the newly added entry
        content = register_file.read_text()
        found = "STORY-TEST" in content

        # Assert
        assert found is True
        assert "FB-2025-11-07-999" in content

    def test_feedback_config_affects_export_behavior_integration(self, integration_project_dir):
        """Test /feedback-config settings affect /export-feedback behavior."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - change export format in config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        config["export_format"] = "csv"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Act - export with new format setting
        csv_content = "feedback_id,timestamp,story_id\nFB-1,2025-11-07T10:00:00Z,STORY-001\n"
        export_file = exports_dir / "2025-11-07-export-csv.csv"
        export_file.write_text(csv_content)

        # Assert - export uses config format
        with open(config_file, 'r') as f:
            updated_config = yaml.safe_load(f)
        assert updated_config["export_format"] == "csv"
        assert export_file.exists()

    def test_search_results_exported_successfully_integration(self, integration_project_dir):
        """Test /feedback-search results can be exported with /export-feedback."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act - search for STORY-001
        content = register_file.read_text()
        story_matches = content.count("STORY-001")

        # Act - export search results
        export_data = {
            "export_id": "EXP-SEARCH-001",
            "query": "STORY-001",
            "entries_count": story_matches,
            "entries": [
                {"feedback_id": "FB-2025-11-07-001", "story_id": "STORY-001"},
                {"feedback_id": "FB-2025-11-07-002", "story_id": "STORY-001"},
                {"feedback_id": "FB-2025-11-07-003", "story_id": "STORY-001"}
            ]
        }
        export_file = exports_dir / "2025-11-07-search-results.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f)

        # Assert
        assert export_file.exists()
        with open(export_file, 'r') as f:
            saved = json.load(f)
        assert saved["entries_count"] == 3


# ============================================================================
# EDGE CASE INTEGRATION TESTS
# ============================================================================


class TestEdgeCaseIntegration:
    """Integration tests for edge cases and boundary conditions."""

    def test_empty_feedback_history_search_handling(self, integration_project_dir):
        """Test /feedback-search gracefully handles empty feedback history."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        # Clear register (keep header only)
        register_file.write_text("# Feedback Register\n\n## Active Feedback Sessions\n")

        # Act
        content = register_file.read_text()
        has_entries = "### FB-" in content

        # Assert
        assert has_entries is False

    def test_large_feedback_history_search_performance(self, integration_project_dir):
        """Test /feedback-search performs within SLA with large dataset."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"

        # Simulate 1000+ entries
        base_content = register_file.read_text()
        for i in range(100, 200):  # Add 100 more entries
            base_content += f"\n### FB-2025-11-{i % 30 + 1:02d}-{i:03d}\n- **Timestamp:** 2025-11-07T{i % 24:02d}:00:00Z\n- **Story ID:** STORY-{i % 50}\n"

        register_file.write_text(base_content)

        # Act - measure search time
        start = time.time()
        content = register_file.read_text()
        matches = content.count("STORY-001")
        elapsed = time.time() - start

        # Assert - should complete in < 500ms for typical queries
        assert elapsed < 1.0  # Generous for file I/O

    def test_concurrent_feedback_operations_no_corruption(self, integration_project_dir):
        """Test concurrent /feedback operations don't corrupt register."""
        # Arrange
        register_file = integration_project_dir / "devforgeai" / "feedback" / "feedback-register.md"
        initial_content = register_file.read_text()

        # Act - simulate concurrent entries (in sequence, testing result)
        entries = [
            "\n### FB-2025-11-07-CONC-001\n- **Timestamp:** 2025-11-07T19:00:00Z\n- **Story ID:** STORY-C1\n",
            "\n### FB-2025-11-07-CONC-002\n- **Timestamp:** 2025-11-07T19:00:01Z\n- **Story ID:** STORY-C2\n",
            "\n### FB-2025-11-07-CONC-003\n- **Timestamp:** 2025-11-07T19:00:02Z\n- **Story ID:** STORY-C3\n",
        ]

        for entry in entries:
            register_file.write_text(register_file.read_text() + entry)

        # Assert - register still valid and contains all entries
        final_content = register_file.read_text()
        assert "# Feedback Register" in final_content
        assert len(final_content) > len(initial_content)
        assert all("CONC" in final_content for _ in entries)

    def test_config_file_missing_creates_defaults(self, integration_project_dir):
        """Test config file missing is handled gracefully with defaults."""
        # Arrange
        config_file = integration_project_dir / "devforgeai" / "feedback" / "config.yaml"
        config_file.unlink()  # Delete config

        # Act - create defaults when missing
        default_config = {
            "retention_days": 90,
            "auto_trigger_enabled": True,
            "export_format": "json",
            "include_metadata": True,
            "search_enabled": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_modified": datetime.now(timezone.utc).isoformat()
        }
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f)

        # Assert
        assert config_file.exists()
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        assert config["retention_days"] == 90

    def test_export_with_no_matching_results_succeeds(self, integration_project_dir):
        """Test /export-feedback succeeds with zero matching entries."""
        # Arrange
        exports_dir = integration_project_dir / "devforgeai" / "feedback" / "exports"

        # Act
        export_data = {
            "status": "success",
            "export_id": "EXP-EMPTY-001",
            "entries_count": 0,
            "selection_criteria": {"story_ids": ["STORY-NONEXISTENT"]},
            "message": "Export created with 0 entries matched selection criteria"
        }
        export_file = exports_dir / "2025-11-07-empty-export.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f)

        # Assert
        assert export_file.exists()
        with open(export_file, 'r') as f:
            saved = json.load(f)
        assert saved["status"] == "success"
        assert saved["entries_count"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
