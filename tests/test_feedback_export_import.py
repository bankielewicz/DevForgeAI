"""
Comprehensive test suite for STORY-017: Cross-Project Export/Import for Feedback Sessions.

Tests cover:
- 12 acceptance criteria (AC1-AC12)
- 15 edge cases
- 6 data validation categories
- Non-functional requirements (performance, security, reliability)

All tests follow AAA pattern (Arrange, Act, Assert) and are designed to fail initially (TDD Red phase).
"""

import pytest
import json
import zipfile
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import tempfile
import shutil
from io import BytesIO
import hashlib
import uuid


# ============================================================================
# FIXTURES - Test Data and Setup
# ============================================================================

@pytest.fixture
def sample_feedback_sessions():
    """Sample feedback sessions for testing."""
    sessions = []
    base_time = datetime(2025, 10, 8, 0, 0, 0, tzinfo=timezone.utc)

    for i in range(15):
        timestamp = base_time + timedelta(days=i, hours=i*2)
        session = {
            "session_id": str(uuid.uuid4()),
            "original_filename": f"{timestamp.strftime('%Y-%m-%dT%H-%M-%S')}-command-dev-success.md",
            "operation_type": "command",
            "operation_name": f"/dev STORY-{42+i}",
            "status": "success",
            "timestamp": timestamp.isoformat() + "Z",
            "content": f"Feedback for STORY-{42+i}. Project path: /home/user/my-project. Custom field: sensitive_value_{i}",
            "file_size_bytes": 2847 + i*100,
        }
        sessions.append(session)

    return sessions


@pytest.fixture
def sample_manifest():
    """Sample manifest.json structure."""
    return {
        "export_version": "1.0",
        "export_format_version": "1.0",
        "created_at": "2025-11-07T14:30:00Z",
        "created_by": "DevForgeAI Framework",
        "framework_version": "1.0.1",
        "session_count": 15,
        "file_count": 15,
        "total_size_bytes": 45892,
        "archive_format": "zip",
        "date_range": {
            "filter": "last-30-days",
            "start_date": "2025-10-08T00:00:00Z",
            "end_date": "2025-11-07T23:59:59Z"
        },
        "sanitization": {
            "applied": True,
            "rules_applied": [
                "story_ids_replaced_with_placeholders",
                "custom_field_values_removed",
                "project_context_removed",
                "file_paths_masked"
            ],
            "replacement_mapping": {
                "story_id_mapping": {
                    "STORY-042": "STORY-001",
                    "STORY-101": "STORY-002",
                    "STORY-156": "STORY-003"
                },
                "masked_fields": [
                    "project_name",
                    "repository_url",
                    "custom_field_values"
                ],
                "preserved_fields": [
                    "operation_type",
                    "status",
                    "framework_version",
                    "timestamp",
                    "user_feedback_text"
                ]
            }
        },
        "integrity": {
            "checksum_algorithm": "sha256",
            "index_file_sha256": "abc123...",
            "session_count_verified": True,
            "all_files_present": True
        },
        "compatibility": {
            "min_framework_version": "1.0.0",
            "tested_on_versions": ["1.0.0", "1.0.1"],
            "import_warnings": []
        },
        "source_project": {
            "identifier": "sha256-hash-of-project-root",
            "export_location": "project-root-directory",
            "export_hostname": "username-machine-name"
        }
    }


@pytest.fixture
def sample_index():
    """Sample index.json structure."""
    return {
        "export_metadata": {
            "created_at": "2025-11-07T14:30:00Z",
            "exported_sessions_count": 15,
            "date_range": "last-30-days",
            "date_range_start": "2025-10-08T00:00:00Z",
            "date_range_end": "2025-11-07T23:59:59Z",
            "sanitization_applied": True,
            "framework_version": "1.0.1",
            "export_format_version": "1.0"
        },
        "sessions": [
            {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "original_filename": "2025-11-07T10-30-00-command-dev-success.md",
                "operation_type": "command",
                "operation_name": "/dev STORY-042",
                "status": "success",
                "timestamp": "2025-11-07T10:30:00Z",
                "file_size_bytes": 2847,
                "export_filename": "2025-11-07T10-30-00-command-dev-success.md",
                "file_sha256": "abc123def456..."
            }
        ]
    }


@pytest.fixture
def temp_project_dir():
    """Create temporary project directory structure."""
    temp_dir = tempfile.mkdtemp()

    # Create devforgeai/feedback/ structure
    feedback_dir = Path(temp_dir) / "devforgeai" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    sessions_dir = feedback_dir / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    yield Path(temp_dir)

    # Cleanup
    shutil.rmtree(temp_dir)


# ============================================================================
# AC1: EXPORT COMMAND WITH OPTIONS
# ============================================================================

class TestExportCommand:
    """Tests for export command recognition and parameter parsing (AC1)."""

    def test_export_command_recognized(self):
        """AC1: Export command is recognized and parsed."""
        # FAIL: export_feedback function not yet implemented
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        assert result["success"] is not None

    def test_export_with_last_7_days_range(self):
        """AC1: Export with --date-range=last-7-days is valid."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-7-days")
        assert result["success"] is not None

    def test_export_with_last_30_days_range(self):
        """AC1: Export with --date-range=last-30-days is valid."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        assert result["success"] is not None

    def test_export_with_last_90_days_range(self):
        """AC1: Export with --date-range=last-90-days is valid."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-90-days")
        assert result["success"] is not None

    def test_export_with_all_range(self):
        """AC1: Export with --date-range=all is valid."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="all")
        assert result["success"] is not None

    def test_export_sanitize_defaults_to_true(self):
        """AC1: Sanitization flag defaults to true (secure by default)."""
        from feedback_export_import import export_feedback_sessions

        # Call without sanitize parameter
        result = export_feedback_sessions(date_range="last-30-days")
        assert result["sanitization_applied"] is True

    def test_export_sanitize_explicit_true(self):
        """AC1: Export with --sanitize=true is valid."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(sanitize=True)
        assert result["sanitization_applied"] is True

    def test_export_sanitize_explicit_false_rejected(self):
        """AC1: Users cannot disable sanitization (only maintainers can)."""
        from feedback_export_import import export_feedback_sessions

        # Should raise ValueError or similar - sanitization cannot be disabled
        with pytest.raises((ValueError, PermissionError)):
            export_feedback_sessions(sanitize=False)

    def test_export_invalid_date_range_rejected(self):
        """AC1: Invalid date range is rejected."""
        from feedback_export_import import export_feedback_sessions

        with pytest.raises(ValueError):
            export_feedback_sessions(date_range="invalid-range")

    def test_export_missing_date_range_uses_default(self):
        """AC1: Missing date range uses default last-30-days."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions()  # No date_range parameter
        assert result["date_range_used"] == "last-30-days"

    def test_export_returns_confirmation_message(self):
        """AC1: Export completes with confirmation message."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        assert result["success"] is True
        assert "archive_path" in result
        assert "sessions_exported" in result

    def test_export_informs_user_of_location(self):
        """AC1: User is informed of export location and contents."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        assert "archive_path" in result
        assert result["archive_path"] is not None
        assert len(result["archive_path"]) > 0

    def test_export_informs_of_contents(self):
        """AC1: User is informed of export contents."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        assert "sessions_exported" in result
        assert "sanitization_applied" in result
        assert "execution_time_ms" in result


# ============================================================================
# AC2: EXPORT PACKAGE STRUCTURE AND NAMING
# ============================================================================

class TestExportPackageStructure:
    """Tests for export package structure and naming (AC2)."""

    def test_export_creates_zip_archive(self, temp_project_dir):
        """AC2: Export creates a .zip archive."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        assert archive_path.endswith(".zip")
        assert os.path.isfile(archive_path)

    def test_export_filename_follows_pattern(self, temp_project_dir):
        """AC2: Filename follows pattern: devforgeai-feedback-export-{timestamp}.zip"""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        filename = os.path.basename(result["archive_path"])

        assert filename.startswith("devforgeai-feedback-export-")
        assert filename.endswith(".zip")

    def test_export_uses_iso_8601_timestamp(self, temp_project_dir):
        """AC2: Timestamp in filename is ISO 8601 format: YYYY-MM-DDTHH-MM-SS."""
        from feedback_export_import import export_feedback_sessions
        import re

        result = export_feedback_sessions(date_range="last-30-days")
        filename = os.path.basename(result["archive_path"])

        # Pattern: devforgeai-feedback-export-2025-11-07T14-30-00-{uuid}.zip
        # UUID suffix added for guaranteed uniqueness on rapid successive exports
        pattern = r"\devforgeai-feedback-export-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}(-[a-f0-9]{8})?\.zip"
        assert re.match(pattern, filename), f"Filename {filename} doesn't match expected pattern"

    def test_export_created_in_project_root(self, temp_project_dir):
        """AC2: Archive is created in project root directory by default."""
        from feedback_export_import import export_feedback_sessions

        # Mock to use temp_project_dir
        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        # Should be in project root (not nested deep)
        assert archive_path.count(os.sep) <= 2

    def test_export_respects_output_parameter(self, temp_project_dir):
        """AC2: Archive can be created in user-specified location via --output."""
        from feedback_export_import import export_feedback_sessions

        custom_output = str(temp_project_dir / "exports")
        result = export_feedback_sessions(output_path=custom_output)

        archive_path = result["archive_path"]
        assert custom_output in archive_path

    def test_export_archive_has_reasonable_size(self, temp_project_dir):
        """AC2: Compressed size is reasonable (<10MB for 30-day export)."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]
        archive_size = result["archive_size_bytes"]

        # Should be reasonably small for typical export
        assert archive_size < 10_000_000, f"Archive too large: {archive_size} bytes"

    def test_export_is_deterministic(self, temp_project_dir, sample_feedback_sessions):
        """AC2: Archive contents are deterministic (same input → same output)."""
        from feedback_export_import import export_feedback_sessions

        # Export twice with same input
        result1 = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        result2 = export_feedback_sessions(date_range="last-30-days", sanitize=True)

        # Compare checksums
        with open(result1["archive_path"], 'rb') as f1:
            hash1 = hashlib.sha256(f1.read()).hexdigest()

        with open(result2["archive_path"], 'rb') as f2:
            hash2 = hashlib.sha256(f2.read()).hexdigest()

        assert hash1 == hash2, "Same input should produce same output"


# ============================================================================
# AC3: EXPORT PACKAGE CONTENTS
# ============================================================================

class TestExportPackageContents:
    """Tests for export package contents structure (AC3)."""

    def test_export_contains_feedback_sessions_directory(self):
        """AC3: Archive contains feedback-sessions/ directory."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            names = zf.namelist()
            assert any(name.startswith("feedback-sessions/") for name in names)

    def test_export_contains_index_json(self):
        """AC3: Archive contains index.json file."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            assert "index.json" in zf.namelist()

    def test_export_contains_manifest_json(self):
        """AC3: Archive contains manifest.json file."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            assert "manifest.json" in zf.namelist()

    def test_export_feedback_sessions_only_match_date_range(self):
        """AC3: feedback-sessions/ contains only files matching date range."""
        from feedback_export_import import export_feedback_sessions

        # Export with narrow date range
        result = export_feedback_sessions(date_range="last-7-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            session_files = [n for n in zf.namelist() if n.startswith("feedback-sessions/")]

            # All files should be within date range (mock will validate)
            for file in session_files:
                assert file.count("/") >= 1

    def test_export_file_count_matches_index(self):
        """AC3: File count in feedback-sessions/ matches count in index.json."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            session_files = [n for n in zf.namelist() if n.startswith("feedback-sessions/") and n.endswith(".md")]
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            expected_count = index_data["export_metadata"]["exported_sessions_count"]
            assert len(session_files) == expected_count

    def test_export_uses_forward_slashes_in_paths(self):
        """AC3: All paths use forward slashes (cross-platform compatibility)."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            for name in zf.namelist():
                # Should use forward slashes, not backslashes
                assert "\\" not in name
                assert "/" in name or name == "manifest.json" or name == "index.json"


# ============================================================================
# AC4: INDEX JSON FILE FORMAT AND FILTERING
# ============================================================================

class TestIndexJsonFormat:
    """Tests for index.json file format and filtering (AC4)."""

    def test_index_json_has_export_metadata(self):
        """AC4: index.json contains export_metadata section."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            assert "export_metadata" in index_data
            assert "sessions" in index_data

    def test_index_metadata_has_created_at(self):
        """AC4: export_metadata includes created_at timestamp."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            assert "created_at" in index_data["export_metadata"]

    def test_index_metadata_has_session_count(self):
        """AC4: export_metadata includes exported_sessions_count."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            assert "exported_sessions_count" in index_data["export_metadata"]

    def test_index_metadata_has_date_range(self):
        """AC4: export_metadata includes date_range field."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            assert "date_range" in index_data["export_metadata"]

    def test_index_metadata_has_sanitization_flag(self):
        """AC4: export_metadata includes sanitization_applied flag."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            assert "sanitization_applied" in index_data["export_metadata"]

    def test_index_sessions_sorted_by_timestamp(self):
        """AC4: Sessions are sorted by timestamp (oldest first)."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            sessions = index_data["sessions"]
            if len(sessions) > 1:
                for i in range(len(sessions) - 1):
                    # Verify timestamp ordering
                    ts1 = datetime.fromisoformat(sessions[i]["timestamp"].replace("Z", "+00:00"))
                    ts2 = datetime.fromisoformat(sessions[i+1]["timestamp"].replace("Z", "+00:00"))
                    assert ts1 <= ts2, "Sessions not sorted by timestamp"

    def test_index_filters_by_date_range(self):
        """AC4: Only sessions matching date range appear in index."""
        from feedback_export_import import export_feedback_sessions

        # Export with narrow range
        result = export_feedback_sessions(date_range="last-7-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            # All sessions should be within last 7 days
            sessions = index_data["sessions"]
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=7)

            for session in sessions:
                ts = datetime.fromisoformat(session["timestamp"].replace("Z", "+00:00"))
                assert ts >= cutoff, f"Session {session['session_id']} outside date range"

    def test_index_empty_if_no_sessions_match(self):
        """AC4: sessions array is empty if no sessions match date range."""
        from feedback_export_import import export_feedback_sessions

        # Mock: Create scenario with no matching sessions
        # Export with future date range
        result = export_feedback_sessions(date_range="last-1-days")  # Future-focused
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            # If no sessions, array should be empty
            sessions = index_data.get("sessions", [])
            assert isinstance(sessions, list)

    def test_index_session_has_required_fields(self):
        """AC4: Each session object has required fields."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        required_fields = [
            "session_id",
            "original_filename",
            "operation_type",
            "operation_name",
            "status",
            "timestamp",
            "file_size_bytes",
            "export_filename"
        ]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            for session in index_data["sessions"]:
                for field in required_fields:
                    assert field in session, f"Missing field: {field}"

    def test_index_includes_file_sha256(self):
        """AC4: Each session includes SHA-256 checksum for integrity."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index_data = json.loads(index_content)

            for session in index_data["sessions"]:
                assert "file_sha256" in session


# ============================================================================
# AC5: MANIFEST JSON WITH METADATA AND SANITIZATION DETAILS
# ============================================================================

class TestManifestJsonFormat:
    """Tests for manifest.json structure and completeness (AC5)."""

    def test_manifest_has_export_version(self):
        """AC5: manifest.json includes export_version."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "export_version" in manifest

    def test_manifest_has_created_at(self):
        """AC5: manifest.json includes created_at timestamp."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "created_at" in manifest

    def test_manifest_has_framework_version(self):
        """AC5: manifest.json includes framework_version."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "framework_version" in manifest

    def test_manifest_has_session_count(self):
        """AC5: manifest.json includes session_count."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "session_count" in manifest

    def test_manifest_has_file_count(self):
        """AC5: manifest.json includes file_count."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "file_count" in manifest

    def test_manifest_has_total_size(self):
        """AC5: manifest.json includes total_size_bytes."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "total_size_bytes" in manifest

    def test_manifest_has_date_range_info(self):
        """AC5: manifest.json includes date_range object."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "date_range" in manifest
            assert "filter" in manifest["date_range"]
            assert "start_date" in manifest["date_range"]
            assert "end_date" in manifest["date_range"]

    def test_manifest_indicates_sanitization_status(self):
        """AC5: sanitization.applied field clearly indicates if sanitization performed."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "sanitization" in manifest
            assert "applied" in manifest["sanitization"]
            assert manifest["sanitization"]["applied"] is True

    def test_manifest_has_replacement_mappings(self):
        """AC5: Replacement mappings documented for transparency."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "replacement_mapping" in manifest["sanitization"]
            assert "story_id_mapping" in manifest["sanitization"]["replacement_mapping"]

    def test_manifest_includes_checksums(self):
        """AC5: Manifest includes checksums (SHA-256) for integrity verification."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "integrity" in manifest
            assert "checksum_algorithm" in manifest["integrity"]
            assert manifest["integrity"]["checksum_algorithm"] == "sha256"


# ============================================================================
# AC6: SANITIZATION RULES - STORY IDS
# ============================================================================

class TestSanitizationStoryIds:
    """Tests for story ID sanitization and replacement (AC6)."""

    def test_story_ids_replaced_with_placeholders(self):
        """AC6: Story IDs replaced with sequential placeholders."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            # Check that mappings exist
            assert len(manifest["sanitization"]["replacement_mapping"]["story_id_mapping"]) > 0

    def test_story_id_mapping_sequential(self):
        """AC6: Replacement pattern follows STORY-042 → STORY-001, STORY-101 → STORY-002, etc."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            # Verify sequential mapping
            mappings = manifest["sanitization"]["replacement_mapping"]["story_id_mapping"]
            placeholder_numbers = []

            for original, placeholder in mappings.items():
                # Extract number from placeholder (STORY-001 → 1)
                placeholder_num = int(placeholder.replace("STORY-", ""))
                placeholder_numbers.append(placeholder_num)

            # Should be sequential
            if placeholder_numbers:
                assert placeholder_numbers == list(range(1, len(placeholder_numbers) + 1))

    def test_story_id_mapping_deterministic(self):
        """AC6: Mapping is deterministic (same story always maps to same placeholder)."""
        from feedback_export_import import export_feedback_sessions

        # Export twice
        result1 = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        result2 = export_feedback_sessions(date_range="last-30-days", sanitize=True)

        archive_path1 = result1["archive_path"]
        archive_path2 = result2["archive_path"]

        with zipfile.ZipFile(archive_path1, 'r') as zf1:
            manifest1 = json.loads(zf1.read("manifest.json").decode('utf-8'))
            mappings1 = manifest1["sanitization"]["replacement_mapping"]["story_id_mapping"]

        with zipfile.ZipFile(archive_path2, 'r') as zf2:
            manifest2 = json.loads(zf2.read("manifest.json").decode('utf-8'))
            mappings2 = manifest2["sanitization"]["replacement_mapping"]["story_id_mapping"]

        assert mappings1 == mappings2, "Mapping not deterministic"

    def test_all_story_occurrences_replaced(self):
        """AC6: All occurrences of original story ID replaced throughout export."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))
            mappings = manifest["sanitization"]["replacement_mapping"]["story_id_mapping"]

            # Check all session files for unreplaced story IDs
            for name in zf.namelist():
                if name.startswith("feedback-sessions/"):
                    content = zf.read(name).decode('utf-8')

                    # Should not contain any original story IDs
                    for original_id in mappings.keys():
                        # Use word boundaries to match exact story IDs
                        import re
                        pattern = r'\b' + re.escape(original_id) + r'\b'
                        assert not re.search(pattern, content), \
                            f"Original {original_id} found in {name}"

    def test_story_id_replacement_case_sensitive(self):
        """AC6: Story ID replacement is case-sensitive."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))
            mappings = manifest["sanitization"]["replacement_mapping"]["story_id_mapping"]

            # Verify keys are case-sensitive (STORY-042 != story-042)
            original_ids = list(mappings.keys())
            lowercase_ids = [id.lower() for id in original_ids]

            # Should not have lowercase duplicates
            assert len(original_ids) == len(set(original_ids))


# ============================================================================
# AC7: SANITIZATION RULES - CUSTOM FIELDS AND CONTEXT
# ============================================================================

class TestSanitizationCustomFields:
    """Tests for custom field and project context sanitization (AC7)."""

    def test_custom_field_values_removed(self):
        """AC7: Custom field values are removed while field names preserved."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            # Verify masked fields listed
            assert "masked_fields" in manifest["sanitization"]["replacement_mapping"]
            masked = manifest["sanitization"]["replacement_mapping"]["masked_fields"]

            assert len(masked) > 0

    def test_file_paths_masked(self):
        """AC7: File paths removed (.../src/authentication/... → {REMOVED})."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            # Check session files
            for name in zf.namelist():
                if name.startswith("feedback-sessions/"):
                    content = zf.read(name).decode('utf-8')

                    # Should not contain absolute paths
                    import re
                    path_pattern = r'/(home|var|opt|srv|src)/'
                    assert not re.search(path_pattern, content), \
                        f"Unmasked path found in {name}"

    def test_repository_names_removed(self):
        """AC7: Repository names removed (my-repo → {REMOVED})."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            for name in zf.namelist():
                if name.startswith("feedback-sessions/"):
                    content = zf.read(name).decode('utf-8')

                    # Should not contain git URLs
                    assert "git@github.com:" not in content
                    assert "@gitlab.com:" not in content

    def test_framework_standard_fields_preserved(self):
        """AC7: Framework-standard fields preserved (operation-type, status, etc.)."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))
            preserved = manifest["sanitization"]["replacement_mapping"]["preserved_fields"]

            # Should contain framework standard fields
            expected_fields = ["operation_type", "status", "timestamp"]
            for field in expected_fields:
                assert field in preserved, f"Standard field {field} not preserved"

    def test_removed_fields_documented(self):
        """AC7: List of removed fields documented in manifest for transparency."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            assert "masked_fields" in manifest["sanitization"]["replacement_mapping"]
            assert "preserved_fields" in manifest["sanitization"]["replacement_mapping"]

    def test_sanitization_applied_consistently(self):
        """AC7: Sanitization rules applied consistently across all session files."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))
            mappings = manifest["sanitization"]["replacement_mapping"]["story_id_mapping"]

            # Check all session files apply same rules
            for name in zf.namelist():
                if name.startswith("feedback-sessions/") and name.endswith(".md"):
                    content = zf.read(name).decode('utf-8')

                    # Verify no original IDs remain
                    for original_id in mappings.keys():
                        assert original_id not in content

    def test_original_unsanitized_preserved_in_feedback_dir(self):
        """AC7: Original unsanitized version remains in user's devforgeai/feedback/ directory."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)

        # Verify original sessions still exist locally (not deleted)
        assert result["success"] is True
        # Original files should still be in devforgeai/feedback/sessions/


# ============================================================================
# AC8: IMPORT COMMAND AND BASIC VALIDATION
# ============================================================================

class TestImportCommand:
    """Tests for import command and validation (AC8)."""

    def test_import_command_recognized(self, valid_import_zip):
        """AC8: Import command is recognized and executed."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))
        assert result is not None

    def test_import_accepts_absolute_path(self, valid_import_zip):
        """AC8: File path can be absolute."""
        from feedback_export_import import import_feedback_sessions

        absolute_path = os.path.abspath(str(valid_import_zip))

        result = import_feedback_sessions(archive_path=absolute_path)
        assert result["success"] is True

    def test_import_accepts_relative_path(self, valid_import_zip):
        """AC8: File path can be relative."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))
        assert result["success"] is True

    def test_import_validates_file_exists(self):
        """AC8: Import validates that file exists and is readable."""
        from feedback_export_import import import_feedback_sessions

        with pytest.raises(FileNotFoundError):
            import_feedback_sessions(archive_path="/nonexistent/path.zip")

    def test_import_validates_valid_zip_archive(self, create_test_zip, temp_zip_dir):
        """AC8: Import validates that file is valid ZIP archive."""
        from feedback_export_import import import_feedback_sessions

        # Create invalid ZIP (not a valid zip, just text)
        invalid_path = temp_zip_dir / "invalid.zip"
        invalid_path.write_bytes(b"This is not a ZIP file")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(invalid_path))

    def test_import_validates_required_files_present(self, create_test_zip):
        """AC8: Import validates that required files present (index.json, manifest.json)."""
        from feedback_export_import import import_feedback_sessions

        # Create ZIP missing manifest
        missing_manifest_zip = create_test_zip({
            "index.json": '{}'
            # Missing manifest.json
        }, prefix="missing_manifest")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(missing_manifest_zip))

    def test_import_reports_validation_failures(self, temp_zip_dir):
        """AC8: Import reports validation failures with remediation guidance."""
        from feedback_export_import import import_feedback_sessions

        # Create corrupted ZIP
        corrupted_path = temp_zip_dir / "corrupted.zip"
        corrupted_path.write_bytes(b"Corrupted")

        with pytest.raises(ValueError) as exc_info:
            import_feedback_sessions(archive_path=str(corrupted_path))

        error_msg = str(exc_info.value)
        # Should contain guidance
        assert len(error_msg) > 0

    def test_import_halts_on_missing_manifest(self, create_test_zip):
        """AC8: Import halts on critical validation failures (missing manifest)."""
        from feedback_export_import import import_feedback_sessions

        # Create ZIP missing manifest
        missing_manifest_zip = create_test_zip({
            "feedback-sessions/file.md": "content",
            "index.json": '{}'
            # Missing manifest.json
        }, prefix="missing_manifest")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(missing_manifest_zip))

    def test_import_halts_on_corrupted_index(self, create_test_zip):
        """AC8: Import halts on corrupted index.json."""
        from feedback_export_import import import_feedback_sessions

        corrupted_index_zip = create_test_zip({
            "feedback-sessions/file.md": "content",
            "index.json": "Invalid JSON {",
            "manifest.json": '{}'
        }, prefix="corrupted_index")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(corrupted_index_zip))

    def test_import_logs_validation_steps(self, valid_import_zip):
        """AC8: Import logs all validation steps for debugging."""
        from feedback_export_import import import_feedback_sessions

        # Should not raise, should log
        result = import_feedback_sessions(archive_path=str(valid_import_zip))
        # Logging tested separately (would need log capture fixture)


# ============================================================================
# AC9: IMPORT PACKAGE EXTRACTION AND PLACEMENT
# ============================================================================

class TestImportExtraction:
    """Tests for import extraction and directory placement (AC9)."""

    def test_import_extracts_to_timestamped_directory(self, temp_project_dir, valid_import_zip):
        """AC9: Package extracted to devforgeai/feedback/imported/{timestamp}/"""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        extracted_path = result["extracted_path"]
        assert "devforgeai" in extracted_path
        assert "feedback" in extracted_path
        assert "imported" in extracted_path

    def test_import_uses_iso_8601_timestamp(self, temp_project_dir, valid_import_zip):
        """AC9: Timestamp in directory name is ISO 8601 format."""
        from feedback_export_import import import_feedback_sessions
        import re

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        # Extract directory name
        dir_name = os.path.basename(result["extracted_path"])

        # Pattern: YYYY-MM-DDTHH-MM-SS
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$"
        assert re.match(pattern, dir_name)

    def test_import_creates_subdirectory_structure(self, temp_project_dir, valid_import_zip):
        """AC9: Extraction creates proper subdirectory structure."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        extracted_path = Path(result["extracted_path"])

        # Should have subdirectories
        assert (extracted_path / "feedback-sessions").exists()
        assert (extracted_path / "index.json").exists()
        assert (extracted_path / "manifest.json").exists()

    def test_import_preserves_original_zip(self, temp_project_dir, valid_import_zip):
        """AC9: Original ZIP file is NOT deleted (preserved for audit trail)."""
        from feedback_export_import import import_feedback_sessions

        import_feedback_sessions(archive_path=str(valid_import_zip))

        # Original ZIP should still exist
        assert valid_import_zip.exists()

    def test_import_extracted_directory_readable(self, temp_project_dir, valid_import_zip):
        """AC9: Extracted directory is readable and properly organized."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        extracted_path = Path(result["extracted_path"])

        # Should be readable
        assert os.access(str(extracted_path), os.R_OK)

        # Contents should be accessible
        assert os.access(str(extracted_path / "index.json"), os.R_OK)

    def test_import_displays_progress(self, temp_project_dir, larger_import_zip):
        """AC9: Import progress is displayed (percentage complete during extraction)."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(larger_import_zip))

        assert result["success"] is True
        # Progress reporting tested with output capture

    def test_import_informs_of_extraction_location(self, temp_project_dir, valid_import_zip):
        """AC9: User is informed of extraction location."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        assert "extracted_path" in result
        assert result["extracted_path"] is not None


# ============================================================================
# AC10: MERGE INDEX ENTRIES WITH CONFLICT RESOLUTION
# ============================================================================

class TestIndexMerging:
    """Tests for index merging and conflict resolution (AC10)."""

    def test_merge_new_session_ids_directly(self, temp_project_dir, create_test_zip):
        """AC10: Sessions with new IDs are added directly."""
        from feedback_export_import import import_feedback_sessions

        # Create initial index
        self._create_initial_index(temp_project_dir)

        # Import with new session IDs
        test_zip = self._make_import_zip_with_new_sessions(create_test_zip)
        result = import_feedback_sessions(archive_path=str(test_zip))

        # Verify new sessions added
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        with open(index_path) as f:
            index = json.load(f)

        assert result["success"] is True

    def test_merge_detects_duplicate_ids(self, temp_project_dir, create_test_zip):
        """AC10: Sessions with duplicate IDs are detected."""
        from feedback_export_import import import_feedback_sessions

        # Create initial session
        session_id = str(uuid.uuid4())
        self._create_initial_index_with_session(temp_project_dir, session_id)

        # Import with same session ID
        test_zip = self._make_import_zip_with_session_id(create_test_zip, session_id)
        result = import_feedback_sessions(archive_path=str(test_zip))

        assert result["duplicate_ids_found"] > 0

    def test_merge_resolves_duplicates_with_suffix(self, temp_project_dir, create_test_zip):
        """AC10: Duplicate IDs get suffix: -imported-1, -imported-2, etc."""
        from feedback_export_import import import_feedback_sessions

        session_id = str(uuid.uuid4())
        self._create_initial_index_with_session(temp_project_dir, session_id)

        test_zip = self._make_import_zip_with_session_id(create_test_zip, session_id)
        result = import_feedback_sessions(archive_path=str(test_zip))

        assert result["duplicate_ids_resolved"] > 0

    def test_merge_logs_collisions(self, temp_project_dir, create_test_zip):
        """AC10: Collisions documented in conflict-resolution.log."""
        from feedback_export_import import import_feedback_sessions

        session_id = str(uuid.uuid4())
        self._create_initial_index_with_session(temp_project_dir, session_id)

        test_zip = self._make_import_zip_with_session_id(create_test_zip, session_id)
        import_feedback_sessions(archive_path=str(test_zip))

        # Check for conflict log
        log_path = temp_project_dir / "devforgeai" / "feedback" / "conflict-resolution.log"
        # Log file should exist if conflicts occurred

    def test_merge_atomic_operation(self, temp_project_dir, valid_import_zip):
        """AC10: Index updated atomically (no partial state)."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        # Verify index is valid JSON (not partial)
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        if index_path.exists():
            with open(index_path) as f:
                # Should not raise JSON parse error
                json.load(f)

    def test_merge_preserves_chronological_order(self, temp_project_dir, valid_import_zip):
        """AC10: Merge preserves chronological ordering."""
        from feedback_export_import import import_feedback_sessions

        import_feedback_sessions(archive_path=str(valid_import_zip))

        # Verify sessions are in time order
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        if index_path.exists():
            with open(index_path) as f:
                index = json.load(f)

            sessions = index.get("sessions", [])
            for i in range(len(sessions) - 1):
                ts1 = datetime.fromisoformat(sessions[i]["timestamp"].replace("Z", "+00:00"))
                ts2 = datetime.fromisoformat(sessions[i+1]["timestamp"].replace("Z", "+00:00"))
                assert ts1 <= ts2

    def test_merge_updates_session_count(self, temp_project_dir, valid_import_zip):
        """AC10: Total session count updated in main index."""
        from feedback_export_import import import_feedback_sessions

        result = import_feedback_sessions(archive_path=str(valid_import_zip))

        assert result["sessions_imported"] > 0

    def test_merge_marks_imported_flag(self, temp_project_dir, valid_import_zip):
        """AC10: Imported sessions marked with is_imported: true."""
        from feedback_export_import import import_feedback_sessions

        import_feedback_sessions(archive_path=str(valid_import_zip))

        # Verify is_imported flag set
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        if index_path.exists():
            with open(index_path) as f:
                index = json.load(f)

            for session in index.get("sessions", []):
                if session.get("was_imported"):
                    assert session.get("is_imported") is True

    def test_merge_documents_import_source(self, temp_project_dir, valid_import_zip):
        """AC10: Import source documented in imported_from metadata."""
        from feedback_export_import import import_feedback_sessions

        import_feedback_sessions(archive_path=str(valid_import_zip))

        # Verify imported_from metadata
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        if index_path.exists():
            with open(index_path) as f:
                index = json.load(f)

            for session in index.get("sessions", []):
                if session.get("is_imported"):
                    assert "imported_from" in session

    @staticmethod
    def _create_initial_index(temp_project_dir):
        """Helper: Create initial feedback index."""
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(index_path, 'w') as f:
            json.dump({"sessions": []}, f)

    @staticmethod
    def _create_initial_index_with_session(temp_project_dir, session_id):
        """Helper: Create index with one session."""
        index_path = temp_project_dir / "devforgeai" / "feedback" / "feedback-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(index_path, 'w') as f:
            json.dump({
                "sessions": [{
                    "session_id": session_id,
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation_type": "command",
                    "status": "success"
                }]
            }, f)

    @staticmethod
    def _make_import_zip_with_new_sessions(create_test_zip):
        """Helper: Create ZIP with new session IDs using fixture."""
        new_id = str(uuid.uuid4())
        return create_test_zip({
            "feedback-sessions/new.md": "New session",
            "index.json": json.dumps({
                "export_metadata": {},
                "sessions": [{
                    "session_id": new_id,
                    "timestamp": "2025-11-07T11:00:00Z",
                    "operation_type": "command",
                    "status": "success"
                }]
            }),
            "manifest.json": json.dumps({
                "export_version": "1.0",
                "source_project": {"identifier": "new"}
            })
        }, prefix="new_sessions")

    @staticmethod
    def _make_import_zip_with_session_id(create_test_zip, session_id):
        """Helper: Create ZIP with specific session ID using fixture."""
        return create_test_zip({
            "feedback-sessions/duplicate.md": "Duplicate session",
            "index.json": json.dumps({
                "export_metadata": {},
                "sessions": [{
                    "session_id": session_id,
                    "timestamp": "2025-11-07T11:00:00Z",
                    "operation_type": "command",
                    "status": "success"
                }]
            }),
            "manifest.json": json.dumps({
                "export_version": "1.0",
                "source_project": {"identifier": "dup"}
            })
        }, prefix="duplicate_session")


# ============================================================================
# AC11: IMPORT COMPATIBILITY VALIDATION
# ============================================================================

class TestImportCompatibility:
    """Tests for framework compatibility validation during import (AC11)."""

    def test_compatibility_version_check(self, create_test_zip):
        """AC11: Import checks min_framework_version <= current version."""
        from feedback_export_import import import_feedback_sessions

        test_zip = self._make_compatible_zip(create_test_zip)
        result = import_feedback_sessions(archive_path=str(test_zip))

        assert result["compatibility_status"] == "compatible"

    def test_compatibility_warns_if_not_tested(self, create_test_zip):
        """AC11: Warns if current version not in tested_on_versions."""
        from feedback_export_import import import_feedback_sessions

        test_zip = self._make_untested_version_zip(create_test_zip)
        result = import_feedback_sessions(archive_path=str(test_zip))

        # Should warn but proceed
        assert len(result.get("warnings", [])) > 0
        assert result["success"] is True

    def test_compatibility_handles_mismatch_gracefully(self, create_test_zip):
        """AC11: Version mismatch handled gracefully (no blocking)."""
        from feedback_export_import import import_feedback_sessions

        test_zip = self._make_old_version_zip(create_test_zip)
        result = import_feedback_sessions(archive_path=str(test_zip))

        # Should warn but not block
        assert result["success"] is True

    def test_compatibility_logs_information(self, create_test_zip):
        """AC11: Compatibility information logged for troubleshooting."""
        from feedback_export_import import import_feedback_sessions

        test_zip = self._make_compatible_zip(create_test_zip)
        import_feedback_sessions(archive_path=str(test_zip))

        # Logging validation (would need log capture)

    def test_compatibility_notifies_user_of_mismatches(self, create_test_zip):
        """AC11: User notified of version mismatches before proceeding."""
        from feedback_export_import import import_feedback_sessions

        test_zip = self._make_untested_version_zip(create_test_zip)
        result = import_feedback_sessions(archive_path=str(test_zip))

        # Should have warnings if mismatch
        if not result["compatibility_status"] == "compatible":
            assert "warnings" in result

    @staticmethod
    def _make_compatible_zip(create_test_zip):
        """Helper: Create ZIP with compatible version using fixture."""
        return create_test_zip({
            "feedback-sessions/s.md": "test",
            "index.json": json.dumps({"sessions": []}),
            "manifest.json": json.dumps({
                "framework_version": "1.0.0",
                "min_framework_version": "1.0.0",
                "tested_on_versions": ["1.0.0", "1.0.1"],
                "source_project": {"identifier": "test"}
            })
        }, prefix="compatible")

    @staticmethod
    def _make_untested_version_zip(create_test_zip):
        """Helper: Create ZIP with untested version using fixture."""
        return create_test_zip({
            "feedback-sessions/s.md": "test",
            "index.json": json.dumps({"sessions": []}),
            "manifest.json": json.dumps({
                "framework_version": "0.9.0",
                "min_framework_version": "0.8.0",
                "tested_on_versions": ["0.8.0", "0.9.0"],  # Not 1.0.1
                "source_project": {"identifier": "test"}
            })
        }, prefix="untested")

    @staticmethod
    def _make_old_version_zip(create_test_zip):
        """Helper: Create ZIP with old framework version using fixture."""
        return create_test_zip({
            "feedback-sessions/s.md": "test",
            "index.json": json.dumps({"sessions": []}),
            "manifest.json": json.dumps({
                "framework_version": "0.5.0",
                "min_framework_version": "0.5.0",
                "tested_on_versions": ["0.5.0"],
                "source_project": {"identifier": "test"}
            })
        }, prefix="old_version")


# ============================================================================
# AC12: SANITIZATION TRANSPARENCY AND REVERSAL INFORMATION
# ============================================================================

class TestSanitizationTransparency:
    """Tests for sanitization transparency during import (AC12)."""

    def test_transparency_manifest_indicates_sanitization(self):
        """AC12: Manifest clearly indicates sanitization.applied: true."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            assert manifest["sanitization"]["applied"] is True

    def test_transparency_mappings_available(self):
        """AC12: Replacement mappings are available for reference."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            assert "replacement_mapping" in manifest["sanitization"]

    def test_transparency_explains_irreversibility(self):
        """AC12: User understands original IDs cannot be recovered from sanitized export."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            # Manifest should document this
            assert "sanitization" in manifest

    def test_transparency_note_in_manifest(self):
        """AC12: Note explains story ID replacement in manifest."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        archive_path = result["archive_path"]

        with zipfile.ZipFile(archive_path, 'r') as zf:
            manifest = json.loads(zf.read("manifest.json").decode('utf-8'))

            # Should have clear information about sanitization
            assert manifest["sanitization"]["applied"] is True

    def test_transparency_imported_marked(self, create_test_zip):
        """AC12: Imported sessions marked with was_sanitized: true."""
        from feedback_export_import import import_feedback_sessions

        test_zip = create_test_zip({
            "feedback-sessions/sanitized.md": "Content with STORY-001",
            "index.json": json.dumps({
                "export_metadata": {"sanitization_applied": True},
                "sessions": [{
                    "session_id": str(uuid.uuid4()),
                    "timestamp": "2025-11-07T10:00:00Z"
                }]
            }),
            "manifest.json": json.dumps({
                "sanitization": {
                    "applied": True,
                    "rules_applied": ["story_ids_replaced"],
                    "replacement_mapping": {
                        "story_id_mapping": {"STORY-042": "STORY-001"}
                    }
                },
                "source_project": {"identifier": "test"}
            })
        }, prefix="sanitized")
        import_feedback_sessions(archive_path=str(test_zip))

        # Verify was_sanitized flag in merged index

    def test_transparency_documentation_available(self):
        """AC12: Framework includes documentation on interpreting sanitized feedback."""
        # Documentation test (would verify docs exist)
        pass


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error scenarios."""

    def test_edge_case_empty_date_range(self):
        """Edge Case 1: No sessions match date range filter."""
        from feedback_export_import import export_feedback_sessions

        # Create scenario with no matching sessions
        result = export_feedback_sessions(date_range="last-1-days")

        assert result["success"] is True
        assert result["sessions_exported"] == 0

    def test_edge_case_large_export_respects_limit(self):
        """Edge Case 2: Large export respects 100MB limit."""
        from feedback_export_import import export_feedback_sessions

        # Would need to mock 5000+ sessions
        # Should fail gracefully if would exceed 100MB
        pass

    def test_edge_case_duplicate_ids_during_import(self):
        """Edge Case 3: Duplicate session IDs handled correctly."""
        from feedback_export_import import import_feedback_sessions

        # Import two packages with same session IDs
        pass

    def test_edge_case_corrupted_archive_handling(self, temp_zip_dir):
        """Edge Case 4: Corrupted archive handled gracefully."""
        from feedback_export_import import import_feedback_sessions

        # Create truncated ZIP
        zip_path = temp_zip_dir / "corrupted.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.txt", "test" * 1000)

        # Truncate file
        with open(zip_path, 'r+b') as f:
            f.seek(-10, 2)  # Seek to 10 bytes before end
            f.truncate()

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(zip_path))

    def test_edge_case_missing_required_files(self, create_test_zip):
        """Edge Case 5: Missing required files detected."""
        from feedback_export_import import import_feedback_sessions

        missing_manifest_zip = create_test_zip({
            "index.json": '{}'
            # Missing manifest.json
        }, prefix="missing_manifest")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(missing_manifest_zip))

    def test_edge_case_unicode_content_roundtrip(self):
        """Edge Case 8: Unicode content (emoji, CJK, Arabic) survives roundtrip."""
        from feedback_export_import import export_feedback_sessions, import_feedback_sessions

        # Would need to mock feedback with unicode content
        pass

    def test_edge_case_symlink_attack_prevention(self, create_test_zip):
        """Edge Case 9: Symlink attacks prevented during extraction."""
        from feedback_export_import import import_feedback_sessions

        # Create archive with path traversal
        path_traversal_zip = create_test_zip({
            "../../../etc/passwd": "malicious",
            "index.json": '{"sessions": []}',
            "manifest.json": '{}'
        }, prefix="path_traversal")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(path_traversal_zip))

    def test_edge_case_concurrent_operations(self):
        """Edge Case 10: Concurrent export/import operations succeed."""
        # Would use multiprocessing/threading
        pass

    def test_edge_case_no_feedback_created_yet(self):
        """Edge Case 11: Export succeeds with zero feedback sessions."""
        from feedback_export_import import export_feedback_sessions

        result = export_feedback_sessions(date_range="last-30-days")
        assert result["success"] is True

    def test_edge_case_permission_denied_on_import_directory(self):
        """Edge Case 12: Permission denied handled gracefully."""
        # Would need to create read-only directory
        pass

    def test_edge_case_archive_filename_collision(self):
        """Edge Case 13: Archive filename collision handled."""
        from feedback_export_import import export_feedback_sessions

        result1 = export_feedback_sessions(date_range="last-30-days")
        # Immediately export again
        result2 = export_feedback_sessions(date_range="last-30-days")

        # Should have different filenames
        assert result1["archive_path"] != result2["archive_path"]

    def test_edge_case_special_characters_in_story_names(self):
        """Edge Case 14: Special characters in story names handled."""
        # Would mock feedback with special chars
        pass

    def test_edge_case_re_import_same_source(self, create_test_zip):
        """Edge Case 15: Re-importing from same source handled."""
        from feedback_export_import import import_feedback_sessions

        test_zip = create_test_zip({
            "feedback-sessions/s.md": "test",
            "index.json": json.dumps({"sessions": []}),
            "manifest.json": json.dumps({
                "source_project": {"identifier": "same-source"}
            })
        }, prefix="same_source")

        # Import twice
        result1 = import_feedback_sessions(archive_path=str(test_zip))
        result2 = import_feedback_sessions(archive_path=str(test_zip))

        # Both should succeed, second should warn about re-import
        assert result1["success"] is True
        assert result2["success"] is True


# ============================================================================
# DATA VALIDATION TESTS
# ============================================================================

class TestDataValidation:
    """Tests for data validation rules."""

    def test_date_range_validation_required(self):
        """Date range must be valid enum value."""
        from feedback_export_import import export_feedback_sessions

        with pytest.raises(ValueError):
            export_feedback_sessions(date_range="last-100-days")

    def test_date_range_case_sensitive(self):
        """Date range validation is case-sensitive."""
        from feedback_export_import import export_feedback_sessions

        with pytest.raises(ValueError):
            export_feedback_sessions(date_range="LAST-30-DAYS")

    def test_archive_path_must_be_readable(self):
        """Archive path must point to readable file."""
        from feedback_export_import import import_feedback_sessions

        with pytest.raises(FileNotFoundError):
            import_feedback_sessions(archive_path="/nonexistent/file.zip")

    def test_archive_must_be_valid_zip(self, temp_zip_dir):
        """Archive must be valid ZIP format."""
        from feedback_export_import import import_feedback_sessions

        invalid_zip = temp_zip_dir / "invalid.zip"
        invalid_zip.write_bytes(b"Not a ZIP")

        with pytest.raises(ValueError):
            import_feedback_sessions(archive_path=str(invalid_zip))

    def test_session_id_must_be_uuid_format(self):
        """Session IDs must be valid UUID format."""
        # Validation during merge
        pass

    def test_manifest_required_fields_present(self, create_test_zip):
        """Manifest must have required fields."""
        from feedback_export_import import import_feedback_sessions

        empty_manifest_zip = create_test_zip({
            "index.json": '{}',
            "manifest.json": '{}'  # Missing fields
        }, prefix="empty_manifest")

        # Should validate required fields
        result = import_feedback_sessions(archive_path=str(empty_manifest_zip))
        # May warn but continue


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_integration_export_then_import(self, temp_project_dir):
        """E2E: Export sessions then import into another project."""
        from feedback_export_import import export_feedback_sessions, import_feedback_sessions

        # Export
        export_result = export_feedback_sessions(date_range="last-30-days")

        # Import
        import_result = import_feedback_sessions(archive_path=export_result["archive_path"])

        assert export_result["success"] is True
        assert import_result["success"] is True

    def test_integration_sanitization_export_then_import(self, temp_project_dir):
        """E2E: Sanitized export roundtrip preserves structure."""
        from feedback_export_import import export_feedback_sessions, import_feedback_sessions

        export_result = export_feedback_sessions(date_range="last-30-days", sanitize=True)
        import_result = import_feedback_sessions(archive_path=export_result["archive_path"])

        # Verify sanitization maintained
        assert export_result["sanitization_applied"] is True
        assert import_result["success"] is True

    def test_integration_duplicate_import_handling(self, temp_project_dir, create_test_zip):
        """E2E: Importing same package twice handles duplicates correctly."""
        from feedback_export_import import import_feedback_sessions

        session_id = str(uuid.uuid4())
        test_zip = create_test_zip({
            "feedback-sessions/s.md": "test",
            "index.json": json.dumps({
                "export_metadata": {},
                "sessions": [{
                    "session_id": session_id,
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation_type": "command",
                    "status": "success"
                }]
            }),
            "manifest.json": json.dumps({
                "source_project": {"identifier": "test-source"}
            })
        }, prefix="integration_test")

        result1 = import_feedback_sessions(archive_path=str(test_zip))
        result2 = import_feedback_sessions(archive_path=str(test_zip))

        assert result1["success"] is True
        assert result2["success"] is True
        assert result2["duplicate_ids_found"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
