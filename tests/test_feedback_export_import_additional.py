"""
Additional test cases for coverage of missing lines in feedback_export_import.py

Targets:
- Line 157, 164, 175: Error handling paths in validation functions
- Lines 189-190, 204-208: Validation error paths
- Line 226, 250: Edge case handling
- Lines 341-342, 374: Sanitization edge cases
- Line 452, 466-467, 479, 501: Import error paths
- Lines 558-560, 575-576: Conflict resolution edge cases
- Lines 608-609: Timestamp parsing edge cases
- Lines 1008-1009: Final error handling

All tests follow AAA pattern and are designed for 95%+ coverage.
"""

import pytest
import json
import zipfile
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import uuid

# =============================================================================
# COVERAGE TESTS - VALIDATION ERROR PATHS
# =============================================================================

class TestValidationErrorHandling:
    """Tests for validation function error handling (lines 157, 164, 175, 189-190)."""

    def test_validate_zip_archive_file_not_found(self):
        """Line 157: FileNotFoundError raised when file doesn't exist."""
        from feedback_export_import import import_feedback_sessions

        with pytest.raises(FileNotFoundError) as exc_info:
            import_feedback_sessions(archive_path="/nonexistent/path/file.zip")

        assert "not found" in str(exc_info.value).lower()

    def test_validate_zip_archive_corrupted_internal_file(self):
        """Line 164: ValueError raised for corrupted ZIP with bad internal file."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("index.json", "{}")
                zf.writestr("manifest.json", "{}")

            # Truncate to corrupt the ZIP
            with open(tmp_path, 'r+b') as f:
                f.seek(0, 2)  # Go to end
                size = f.tell()
                f.seek(size - 10)
                f.truncate()

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            error_msg = str(exc_info.value).lower()
            assert "corrupted" in error_msg or "bad" in error_msg or "invalid" in error_msg
        finally:
            os.unlink(tmp_path)

    def test_validate_zip_contents_missing_index_json(self):
        """Line 175: ValueError raised when index.json is missing."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("manifest.json", "{}")
                # Missing index.json

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            assert "index.json" in str(exc_info.value)
        finally:
            os.unlink(tmp_path)

    def test_validate_zip_contents_corrupted_index_json(self):
        """Lines 189-190: ValueError raised when index.json is invalid JSON."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("index.json", "{ INVALID JSON ")
                zf.writestr("manifest.json", "{}")

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            assert "index.json" in str(exc_info.value).lower()
        finally:
            os.unlink(tmp_path)

    def test_validate_zip_contents_corrupted_manifest_json(self):
        """Lines 204-208: ValueError raised when manifest.json is invalid JSON."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("index.json", '{}')
                zf.writestr("manifest.json", "{ INVALID JSON MANIFEST ")

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            assert "manifest.json" in str(exc_info.value).lower()
        finally:
            os.unlink(tmp_path)


# =============================================================================
# COVERAGE TESTS - TIMESTAMP PARSING EDGE CASES
# =============================================================================

class TestTimestampParsingEdgeCases:
    """Tests for timestamp parsing edge cases (lines 226, 250, 608-609, 466-467)."""

    def test_parse_iso_timestamp_empty_string(self):
        """Line 226: Empty timestamp returns EPOCH_DATE."""
        from feedback_export_import import _parse_iso_timestamp, EPOCH_DATE

        result = _parse_iso_timestamp("")
        assert result == EPOCH_DATE

    def test_parse_iso_timestamp_none_value(self):
        """Line 226: None timestamp returns EPOCH_DATE."""
        from feedback_export_import import _parse_iso_timestamp, EPOCH_DATE

        result = _parse_iso_timestamp(None)
        assert result == EPOCH_DATE

    def test_format_iso_timestamp_with_timezone(self):
        """Line 250: Format removes microseconds and timezone."""
        from feedback_export_import import _format_iso_timestamp

        dt = datetime(2025, 11, 7, 14, 30, 45, 123456, tzinfo=timezone.utc)
        result = _format_iso_timestamp(dt)

        assert "Z" in result
        assert "." not in result  # No microseconds
        assert "123456" not in result

    def test_extract_timestamp_from_filename_no_timestamp(self):
        """Line 452: Returns None when filename doesn't match pattern."""
        from feedback_export_import import _extract_timestamp_from_filename

        result = _extract_timestamp_from_filename("invalid-filename-without-timestamp.md")
        assert result is None

    def test_extract_timestamp_from_filename_invalid_date(self):
        """Lines 466-467: Returns None on ValueError for invalid datetime."""
        from feedback_export_import import _extract_timestamp_from_filename

        # Filename with pattern but invalid date (e.g., 2025-13-45 is invalid)
        result = _extract_timestamp_from_filename("2025-13-45T25-61-61-command-dev.md")
        assert result is None

    def test_determine_export_timestamp_invalid_session_timestamp(self):
        """Lines 608-609: Falls back to current time on ValueError."""
        from feedback_export_import import _determine_export_timestamp

        sessions = [{
            "timestamp": "INVALID_TIMESTAMP_FORMAT"
        }]

        result = _determine_export_timestamp(sessions)

        # Should return current time (not raise error)
        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc


# =============================================================================
# COVERAGE TESTS - CONFLICT RESOLUTION EDGE CASES
# =============================================================================

class TestConflictResolutionEdgeCases:
    """Tests for conflict resolution edge cases (lines 341-342, 374, 558-560, 575-576)."""

    def test_generate_unique_session_id_many_collisions(self):
        """Lines 341-342: Handles multiple collision attempts."""
        from feedback_export_import import _generate_unique_session_id

        base_id = str(uuid.uuid4())
        existing_ids = {base_id}

        # Add many pre-existing -imported-{n} IDs to force iteration
        for i in range(1, 10):
            existing_ids.add(f"{base_id}-imported-{i}")

        result = _generate_unique_session_id(base_id, existing_ids)

        # Should create -imported-10 (first available)
        assert result == f"{base_id}-imported-10"
        assert result not in existing_ids

    def test_merge_indices_duplicate_resolution_increments_counter(self):
        """Line 374: Duplicate resolution increments counter properly."""
        from feedback_export_import import _merge_indices

        base_id = str(uuid.uuid4())
        main_index = {
            "sessions": [
                {"session_id": base_id, "timestamp": "2025-11-07T10:00:00Z"}
            ]
        }
        imported_index = {
            "export_metadata": {"created_at": "2025-11-07T14:00:00Z"},
            "sessions": [
                {"session_id": base_id, "timestamp": "2025-11-07T11:00:00Z"}
            ]
        }

        merged, dup_count, res_count = _merge_indices(main_index, imported_index)

        assert dup_count == 1
        assert res_count == 1
        # Verify ID was changed
        session_ids = [s["session_id"] for s in merged["sessions"]]
        assert "-imported-" in session_ids[1]

    def test_process_feedback_file_read_error_handling(self):
        """Lines 558-560: Handles file read errors gracefully."""
        from feedback_export_import import _process_feedback_file

        # Create a directory instead of file to cause read error
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_file = Path(temp_dir) / "test.md"
            fake_file.mkdir()

            result = _process_feedback_file(
                fake_file,
                datetime(2025, 11, 1, tzinfo=timezone.utc),
                datetime(2025, 11, 30, tzinfo=timezone.utc)
            )

            # Should return None on error, not raise
            assert result is None

    def test_get_feedback_sessions_directory_not_found(self):
        """Lines 575-576: Handles missing feedback directory gracefully."""
        from feedback_export_import import _get_feedback_sessions

        # Temporarily patch the FEEDBACK_SESSIONS_DIR to non-existent path
        with patch('feedback_export_import.FEEDBACK_SESSIONS_DIR', Path("/nonexistent/path")):
            result = _get_feedback_sessions(date_range="last-30-days")

            # Should return empty list, not raise
            assert result == []
            assert isinstance(result, list)


# =============================================================================
# COVERAGE TESTS - SANITIZATION EDGE CASES
# =============================================================================

class TestSanitizationEdgeCases:
    """Tests for sanitization function edge cases (lines 341-342, 374)."""

    def test_sanitize_content_with_story_ids(self):
        """Story IDs are replaced in content."""
        from feedback_export_import import _sanitize_content, SanitizationConfig

        content = "STORY-042 is broken. See STORY-042 for details."

        mapping = SanitizationConfig(
            story_id_mapping={"STORY-042": "STORY-001"},
            masked_fields=["project_name"],
            preserved_fields=["status"]
        )

        result = _sanitize_content(content, mapping)

        # All occurrences should be replaced
        assert "STORY-042" not in result
        assert "STORY-001" in result

    def test_sanitize_content_no_story_ids(self):
        """Content without story IDs returns with patterns applied."""
        from feedback_export_import import _sanitize_content, SanitizationConfig

        content = "This feedback has no story IDs but has /home/user/path"

        mapping = SanitizationConfig(
            story_id_mapping={},
            masked_fields=["project_name"],
            preserved_fields=["status"]
        )

        result = _sanitize_content(content, mapping)

        # Should apply standard sanitization patterns
        assert isinstance(result, str)

    def test_build_story_id_mapping_multiple_ids(self):
        """Correctly builds mapping for multiple story IDs."""
        from feedback_export_import import _build_story_id_mapping

        content_list = [
            "STORY-042 is broken",
            "STORY-101 is working",
            "STORY-156 needs review"
        ]

        mapping = _build_story_id_mapping(content_list)

        # Should map unique IDs
        assert "STORY-042" in mapping
        assert "STORY-101" in mapping
        assert "STORY-156" in mapping
        assert mapping["STORY-042"] == "STORY-001"
        assert mapping["STORY-101"] == "STORY-002"
        assert mapping["STORY-156"] == "STORY-003"

    def test_build_story_id_mapping_no_ids(self):
        """Empty mapping when no story IDs found."""
        from feedback_export_import import _build_story_id_mapping

        content_list = [
            "This has no story IDs",
            "Neither does this one"
        ]

        mapping = _build_story_id_mapping(content_list)

        assert mapping == {}


# =============================================================================
# COVERAGE TESTS - IMPORT ERROR HANDLING
# =============================================================================

class TestImportErrorHandling:
    """Tests for import function error handling (line 479, 501, 1008-1009)."""

    def test_parse_session_timestamp_attribute_error(self):
        """Line 501: Falls back to file modification time on AttributeError."""
        from feedback_export_import import _parse_session_timestamp

        fake_file = Path("/tmp/nonexistent.md")

        with patch('feedback_export_import._extract_timestamp_from_filename', return_value=None):
            with patch('feedback_export_import._get_file_modification_time') as mock_mtime:
                expected_time = datetime(2025, 11, 7, 10, 0, 0, tzinfo=timezone.utc)
                mock_mtime.return_value = expected_time

                result = _parse_session_timestamp("test.md", fake_file)

                assert result == expected_time

    def test_import_feedback_sessions_path_traversal_detection(self):
        """Detects and rejects path traversal attempts in archive."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                # Path traversal attempt
                zf.writestr("../../../etc/passwd", "malicious")
                zf.writestr("index.json", '{"sessions": []}')
                zf.writestr("manifest.json", '{}')

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            assert "path traversal" in str(exc_info.value).lower()
        finally:
            os.unlink(tmp_path)

    def test_import_feedback_sessions_parent_directory_traversal(self):
        """Rejects archive entries with parent directory references."""
        from feedback_export_import import import_feedback_sessions

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("feedback-sessions/../../../etc/passwd", "malicious")
                zf.writestr("index.json", '{"sessions": []}')
                zf.writestr("manifest.json", '{}')

        try:
            with pytest.raises(ValueError) as exc_info:
                import_feedback_sessions(archive_path=tmp_path)
            assert "path traversal" in str(exc_info.value).lower()
        finally:
            os.unlink(tmp_path)


# =============================================================================
# COVERAGE TESTS - ARCHIVE EXTRACTION AND VALIDATION
# =============================================================================

class TestArchiveExtraction:
    """Tests for archive extraction and validation functions."""

    def test_extract_archive_to_import_dir_creates_timestamped_dir(self):
        """Creates extraction directory with ISO 8601 timestamp."""
        from feedback_export_import import _extract_archive_to_import_dir
        import re

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("feedback-sessions/session1.md", "content")
                zf.writestr("index.json", '{}')
                zf.writestr("manifest.json", '{}')

        try:
            result = _extract_archive_to_import_dir(tmp_path)

            # Should be a path string
            assert isinstance(result, str)
            # Should contain timestamp pattern
            assert re.search(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}', result)
        finally:
            os.unlink(tmp_path)

    def test_validate_archive_for_import_success(self):
        """Successful validation of valid archive."""
        from feedback_export_import import _validate_archive_for_import

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
            with zipfile.ZipFile(tmp_path, 'w') as zf:
                zf.writestr("feedback-sessions/session1.md", "content")
                zf.writestr("index.json", '{}')
                zf.writestr("manifest.json", '{}')

        try:
            # Should not raise
            _validate_archive_for_import(tmp_path)
        finally:
            os.unlink(tmp_path)


# =============================================================================
# COVERAGE TESTS - INDEX LOADING AND WRITING
# =============================================================================

class TestIndexLoadingAndWriting:
    """Tests for atomic index operations."""

    def test_load_or_create_main_index_exists(self, temp_project_dir):
        """Loads existing index when it exists."""
        from feedback_export_import import _load_or_create_main_index

        # Create index file
        feedback_dir = temp_project_dir / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)
        index_path = feedback_dir / "feedback-index.json"

        test_data = {"sessions": [{"id": "test"}]}
        with open(index_path, 'w') as f:
            json.dump(test_data, f)

        with patch('feedback_export_import.FEEDBACK_INDEX_FILE', index_path):
            result = _load_or_create_main_index()

            assert result == test_data

    def test_load_or_create_main_index_create_new(self, temp_project_dir):
        """Creates new index when none exists."""
        from feedback_export_import import _load_or_create_main_index

        feedback_dir = temp_project_dir / "devforgeai" / "feedback"
        index_path = feedback_dir / "feedback-index.json"

        with patch('feedback_export_import.FEEDBACK_INDEX_FILE', index_path):
            result = _load_or_create_main_index()

            assert "sessions" in result
            assert result["sessions"] == []

    def test_write_merged_index_atomically_creates_parent_dir(self, temp_project_dir):
        """Creates parent directory if it doesn't exist."""
        from feedback_export_import import _write_merged_index_atomically

        feedback_dir = temp_project_dir / "devforgeai" / "feedback" / "deep" / "nested"
        index_path = feedback_dir / "feedback-index.json"

        test_data = {"sessions": []}

        with patch('feedback_export_import.FEEDBACK_INDEX_FILE', index_path):
            _write_merged_index_atomically(test_data)

            # Verify file was created
            assert index_path.exists()
            with open(index_path) as f:
                loaded = json.load(f)
            assert loaded == test_data

    def test_write_merged_index_atomically_overwrites_existing(self, temp_project_dir):
        """Overwrites existing index atomically."""
        from feedback_export_import import _write_merged_index_atomically

        feedback_dir = temp_project_dir / "devforgeai" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)
        index_path = feedback_dir / "feedback-index.json"

        # Create initial content
        with open(index_path, 'w') as f:
            json.dump({"sessions": ["old"]}, f)

        new_data = {"sessions": ["new1", "new2"]}

        with patch('feedback_export_import.FEEDBACK_INDEX_FILE', index_path):
            _write_merged_index_atomically(new_data)

            with open(index_path) as f:
                loaded = json.load(f)
            assert loaded == new_data


# =============================================================================
# COVERAGE TESTS - SUMMARY BUILDING
# =============================================================================

class TestSummaryBuilding:
    """Tests for import summary building."""

    def test_build_import_summary_with_duplicates(self):
        """Correctly reports duplicate resolution."""
        from feedback_export_import import _build_import_summary

        imported_index = {
            "export_metadata": {"exported_sessions_count": 5},
            "sessions": [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        }
        merged_index = {
            "sessions": [
                {"id": "old"},
                {"id": "1"},
                {"id": "2"},
                {"id": "3"},
                {"id": "1-imported-1"}
            ]
        }

        summary = _build_import_summary(imported_index, merged_index, 1, 1)

        assert summary["exported_sessions"] == 5
        assert summary["imported_sessions"] == 3
        assert summary["duplicate_ids_found"] == 1
        assert summary["duplicate_ids_resolved"] == 1
        assert summary["current_total_sessions"] == 5

    def test_build_import_summary_no_sessions(self):
        """Handles empty indices gracefully."""
        from feedback_export_import import _build_import_summary

        imported_index = {"export_metadata": {}, "sessions": []}
        merged_index = {"sessions": []}

        summary = _build_import_summary(imported_index, merged_index, 0, 0)

        assert summary["imported_sessions"] == 0
        assert summary["duplicate_ids_found"] == 0
        assert summary["current_total_sessions"] == 0


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_project_dir():
    """Create temporary project directory structure."""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    # Create devforgeai/feedback/ structure
    feedback_dir = Path(temp_dir) / "devforgeai" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    sessions_dir = feedback_dir / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    yield Path(temp_dir)

    # Cleanup
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
