"""
TDD Red Phase tests for feedback indexer reindex_all_feedback function.

Tests cover:
- Scanning ai-analysis STORY/EPIC/RCA folders for JSON and MD files
- Scanning code-review and code-reviews directories for markdown files
- Scanning root-level feedback report files
- Graceful handling of missing directories
- Unified index generation with version, source_summary, and entries
- Source type field population for each entry
- Graceful skipping of malformed JSON files
- Exclusion of documentation, config, index, and register files

All tests use tmp_path fixture to create isolated directory structures.
Each test calls reindex_all_feedback(str(tmp_path)) and reads the
generated devforgeai/feedback/index.json to verify entries.
"""

import json
from pathlib import Path

import pytest

from devforgeai_cli.feedback.feedback_indexer import reindex_all_feedback


def _read_index(tmp_path):
    """Read the generated index.json and return parsed dict."""
    index_path = Path(tmp_path) / "devforgeai" / "feedback" / "index.json"
    assert index_path.exists(), f"Index not created at {index_path}"
    with open(index_path) as f:
        return json.load(f)


class TestFeedbackIndexer:
    """Unit tests for reindex_all_feedback function."""

    def test_scans_ai_analysis_story_folders(self, tmp_path):
        """Verify that ai-analysis STORY folders are scanned and both JSON files indexed."""
        # Arrange
        story_dir = tmp_path / "devforgeai" / "feedback" / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)

        consolidated = {
            "story_id": "STORY-001",
            "workflow_type": "dev",
            "analysis_date": "2026-01-01T00:00:00Z",
            "what_worked_well": [],
            "recommendations": [],
        }
        with open(story_dir / "consolidated-analysis.json", "w") as f:
            json.dump(consolidated, f)

        phase_data = {
            "subagent": "test-automator",
            "phase": "02",
            "story_id": "STORY-001",
            "timestamp": "2026-01-01T00:00:00Z",
            "observations": [],
        }
        with open(story_dir / "phase-02-test-automator.json", "w") as f:
            json.dump(phase_data, f)

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0, f"Expected exit code 0, got {result}"
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) >= 2, (
            f"Expected at least 2 entries, got {len(index['feedback-sessions'])}"
        )
        file_paths = [entry["file-path"] for entry in index["feedback-sessions"]]
        assert any("consolidated-analysis.json" in fp for fp in file_paths), (
            "consolidated-analysis.json not found in index entries"
        )
        assert any("phase-02-test-automator.json" in fp for fp in file_paths), (
            "phase-02-test-automator.json not found in index entries"
        )

    def test_scans_ai_analysis_epic_folders(self, tmp_path):
        """Verify that ai-analysis EPIC folders are scanned and JSON files indexed."""
        # Arrange
        epic_dir = tmp_path / "devforgeai" / "feedback" / "ai-analysis" / "EPIC-001"
        epic_dir.mkdir(parents=True, exist_ok=True)

        epic_data = {
            "ai_analysis": {
                "operation": "epic-creation",
                "epic_id": "EPIC-001",
                "timestamp": "2026-01-01T00:00:00Z",
                "what_worked_well": [],
            }
        }
        with open(epic_dir / "2026-01-01-ai-analysis.json", "w") as f:
            json.dump(epic_data, f)

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) >= 1, (
            f"Expected at least 1 entry, got {len(index['feedback-sessions'])}"
        )
        file_paths = [entry["file-path"] for entry in index["feedback-sessions"]]
        assert any("EPIC-001" in fp for fp in file_paths), (
            "No entry with EPIC-001 found in index"
        )

    def test_scans_ai_analysis_rca_folders(self, tmp_path):
        """Verify that ai-analysis RCA folders are scanned and JSON files indexed."""
        # Arrange
        rca_dir = tmp_path / "devforgeai" / "feedback" / "ai-analysis" / "RCA-001"
        rca_dir.mkdir(parents=True, exist_ok=True)

        rca_data = {
            "timestamp": "2026-01-01T00:00:00Z",
            "recommendations": [],
        }
        with open(rca_dir / "20260101-recommendations.json", "w") as f:
            json.dump(rca_data, f)

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) == 1, (
            f"Expected 1 entry, got {len(index['feedback-sessions'])}"
        )
        file_paths = [entry["file-path"] for entry in index["feedback-sessions"]]
        assert any("RCA-001" in fp for fp in file_paths), (
            "No entry with RCA-001 found in index"
        )

    def test_scans_code_review_files(self, tmp_path):
        """Verify both code-review/ and code-reviews/ directories are scanned."""
        # Arrange
        cr_dir = tmp_path / "devforgeai" / "feedback" / "code-review"
        cr_dir.mkdir(parents=True, exist_ok=True)
        (cr_dir / "STORY-001-code-review.md").write_text(
            "# Code Review\n\nSTORY-001"
        )

        crs_dir = tmp_path / "devforgeai" / "feedback" / "code-reviews"
        crs_dir.mkdir(parents=True, exist_ok=True)
        (crs_dir / "STORY-002-code-review.md").write_text(
            "# Code Review\n\nSTORY-002"
        )

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) == 2, (
            f"Expected 2 entries, got {len(index['feedback-sessions'])}"
        )
        for entry in index["feedback-sessions"]:
            assert entry["source_type"] == "code-review", (
                f"Expected source_type 'code-review', got '{entry['source_type']}'"
            )

    def test_scans_root_report_files(self, tmp_path):
        """Verify root-level feedback report files are scanned with source_type 'report'."""
        # Arrange
        feedback_dir = tmp_path / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)

        (feedback_dir / "code-review-STORY-003.md").write_text("# Code Review")
        (feedback_dir / "integration-test-report-STORY-004.md").write_text(
            "# Integration Test"
        )

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        report_entries = [
            e for e in index["feedback-sessions"] if e["source_type"] == "report"
        ]
        assert len(report_entries) == 2, (
            f"Expected 2 report entries, got {len(report_entries)}"
        )

    def test_handles_missing_sessions_dir_gracefully(self, tmp_path):
        """Verify no exception when sessions/ directory does not exist."""
        # Arrange - create ai-analysis but NOT sessions/
        story_dir = tmp_path / "devforgeai" / "feedback" / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)

        valid_data = {
            "story_id": "STORY-001",
            "timestamp": "2026-01-01T00:00:00Z",
        }
        with open(story_dir / "valid.json", "w") as f:
            json.dump(valid_data, f)

        # Verify sessions/ does NOT exist
        sessions_dir = tmp_path / "devforgeai" / "feedback" / "sessions"
        assert not sessions_dir.exists(), "sessions/ should not exist for this test"

        # Act - must NOT raise exception
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0, f"Expected exit code 0, got {result}"
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) >= 1, (
            "Expected at least 1 entry from ai-analysis"
        )

    def test_mixed_sources_unified_index(self, tmp_path):
        """Verify mixed source types produce unified index with correct structure."""
        # Arrange - create files from all source types
        feedback_dir = tmp_path / "devforgeai" / "feedback"

        # ai-analysis STORY
        story_dir = feedback_dir / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)
        with open(story_dir / "valid.json", "w") as f:
            json.dump({"story_id": "STORY-001", "timestamp": "2026-01-01T00:00:00Z"}, f)

        # ai-analysis EPIC
        epic_dir = feedback_dir / "ai-analysis" / "EPIC-001"
        epic_dir.mkdir(parents=True, exist_ok=True)
        with open(epic_dir / "valid.json", "w") as f:
            json.dump({"epic_id": "EPIC-001", "timestamp": "2026-01-01T00:00:00Z"}, f)

        # code-review
        cr_dir = feedback_dir / "code-review"
        cr_dir.mkdir(parents=True, exist_ok=True)
        (cr_dir / "STORY-002-code-review.md").write_text("# Code Review\n\nSTORY-002")

        # root report
        (feedback_dir / "code-review-STORY-003.md").write_text("# Code Review")

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        assert index["version"] == "2.0", (
            f"Expected version '2.0', got '{index['version']}'"
        )
        assert "source_summary" in index, "Missing 'source_summary' in index"
        summary = index["source_summary"]
        for key in ("ai-analysis", "session", "code-review", "report"):
            assert key in summary, f"Missing '{key}' in source_summary"
        assert len(index["feedback-sessions"]) == 4, (
            f"Expected 4 total entries, got {len(index['feedback-sessions'])}"
        )

    def test_source_type_field_populated(self, tmp_path):
        """Verify source_type field is present and valid for each entry type."""
        # Arrange
        feedback_dir = tmp_path / "devforgeai" / "feedback"

        # ai-analysis JSON
        story_dir = feedback_dir / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)
        with open(story_dir / "analysis.json", "w") as f:
            json.dump({"story_id": "STORY-001", "timestamp": "2026-01-01T00:00:00Z"}, f)

        # code-review MD
        cr_dir = feedback_dir / "code-review"
        cr_dir.mkdir(parents=True, exist_ok=True)
        (cr_dir / "review.md").write_text("# Review")

        # root report MD
        (feedback_dir / "code-review-STORY-002.md").write_text("# Report")

        valid_source_types = {"ai-analysis", "session", "code-review", "report"}

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        for entry in index["feedback-sessions"]:
            assert "source_type" in entry, (
                f"Missing 'source_type' in entry: {entry}"
            )
            assert entry["source_type"] in valid_source_types, (
                f"Invalid source_type '{entry['source_type']}', "
                f"expected one of {valid_source_types}"
            )

    def test_json_parse_errors_skip_gracefully(self, tmp_path, capsys):
        """Verify malformed JSON files are skipped and counted as errors."""
        # Arrange
        story_dir = tmp_path / "devforgeai" / "feedback" / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)

        # Broken JSON file
        (story_dir / "broken.json").write_text("{invalid json!!")

        # Valid JSON file
        with open(story_dir / "valid.json", "w") as f:
            json.dump({"story_id": "STORY-001", "timestamp": "2026-01-01T00:00:00Z"}, f)

        # Act
        result = reindex_all_feedback(str(tmp_path), output_format="json")

        # Assert - parse stdout JSON output
        captured = capsys.readouterr()
        stdout_data = json.loads(captured.out)
        assert stdout_data["error_count"] >= 1, (
            f"Expected error_count >= 1, got {stdout_data['error_count']}"
        )
        assert stdout_data["indexed_count"] >= 1, (
            f"Expected indexed_count >= 1, got {stdout_data['indexed_count']}"
        )

    def test_ignores_documentation_files(self, tmp_path):
        """Verify all documentation, config, index, and register files are excluded."""
        # Arrange
        feedback_dir = tmp_path / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)

        # All excluded documentation files
        excluded_docs = [
            "USER-GUIDE.md",
            "MAINTAINER-GUIDE.md",
            "GRACEFUL-DEGRADATION.md",
            "RETENTION-POLICY.md",
            "IMPLEMENTATION-COMPLETE.md",
            "QUESTION-BANK-COMPLETION-SUMMARY.md",
            "questions.md",
        ]
        for doc in excluded_docs:
            (feedback_dir / doc).write_text(f"# {doc}")

        # All excluded config files
        excluded_configs = [
            "config.yaml",
            "schema.json",
            "questions.yaml",
            "question-defaults.yaml",
        ]
        for cfg in excluded_configs:
            (feedback_dir / cfg).write_text(f"# {cfg}")

        # Excluded index files
        (feedback_dir / "index.json").write_text("{}")
        (feedback_dir / "feedback-index.json").write_text("{}")

        # Excluded register
        (feedback_dir / "feedback-register.md").write_text("# Register")

        # ONE valid feedback file that SHOULD be indexed
        story_dir = feedback_dir / "ai-analysis" / "STORY-001"
        story_dir.mkdir(parents=True, exist_ok=True)
        with open(story_dir / "valid.json", "w") as f:
            json.dump({"story_id": "STORY-001", "timestamp": "2026-01-01T00:00:00Z"}, f)

        # Act
        result = reindex_all_feedback(str(tmp_path))

        # Assert
        assert result == 0
        index = _read_index(tmp_path)
        assert len(index["feedback-sessions"]) == 1, (
            f"Expected exactly 1 entry (valid.json only), "
            f"got {len(index['feedback-sessions'])}"
        )

        # Verify no excluded file appears in any entry
        all_excluded = excluded_docs + excluded_configs + [
            "index.json", "feedback-index.json", "feedback-register.md"
        ]
        for entry in index["feedback-sessions"]:
            entry_filename = Path(entry["file-path"]).name
            assert entry_filename not in all_excluded, (
                f"Excluded file '{entry_filename}' found in index entries"
            )
