"""
TDD Red Phase tests for STORY-105: Test Cleanup Fixtures.

These tests verify the behavior of the new cleanup fixtures before implementation.
All tests should FAIL initially (Red phase).
"""

import pytest
import os
import zipfile
from pathlib import Path
import tempfile


class TestTempZipDirFixture:
    """Tests for temp_zip_dir fixture behavior."""

    def test_fixture_creates_directory(self, temp_zip_dir):
        """temp_zip_dir fixture creates a valid directory."""
        assert temp_zip_dir.exists()
        assert temp_zip_dir.is_dir()

    def test_fixture_is_path_object(self, temp_zip_dir):
        """temp_zip_dir returns a Path object."""
        assert isinstance(temp_zip_dir, Path)

    def test_fixture_allows_file_creation(self, temp_zip_dir):
        """Can create files in temp_zip_dir."""
        test_file = temp_zip_dir / "test.txt"
        test_file.write_text("hello")
        assert test_file.exists()

    def test_fixture_allows_zip_creation(self, temp_zip_dir):
        """Can create zip files in temp_zip_dir."""
        zip_path = temp_zip_dir / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("content.txt", "test content")
        assert zip_path.exists()


class TestCreateTestZipFixture:
    """Tests for create_test_zip factory fixture behavior."""

    def test_fixture_creates_valid_zip(self, create_test_zip):
        """create_test_zip creates a valid zip file."""
        zip_path = create_test_zip({
            "file.txt": "content"
        })
        assert zip_path.exists()
        assert zipfile.is_zipfile(zip_path)

    def test_fixture_includes_all_files(self, create_test_zip):
        """create_test_zip includes all specified files."""
        zip_path = create_test_zip({
            "file1.txt": "content1",
            "file2.txt": "content2",
            "subdir/file3.txt": "content3"
        })

        with zipfile.ZipFile(zip_path, 'r') as zf:
            names = zf.namelist()
            assert "file1.txt" in names
            assert "file2.txt" in names
            assert "subdir/file3.txt" in names

    def test_fixture_file_contents_match(self, create_test_zip):
        """create_test_zip preserves file contents."""
        expected_content = "test content 12345"
        zip_path = create_test_zip({
            "test.txt": expected_content
        })

        with zipfile.ZipFile(zip_path, 'r') as zf:
            actual = zf.read("test.txt").decode('utf-8')
            assert actual == expected_content

    def test_fixture_supports_prefix(self, create_test_zip):
        """create_test_zip supports custom prefix."""
        zip_path = create_test_zip(
            {"file.txt": "content"},
            prefix="custom_prefix"
        )
        assert "custom_prefix" in zip_path.name


class TestValidImportZipFixture:
    """Tests for valid_import_zip fixture behavior."""

    def test_fixture_is_valid_zip(self, valid_import_zip):
        """valid_import_zip returns a valid zip file."""
        assert valid_import_zip.exists()
        assert zipfile.is_zipfile(valid_import_zip)

    def test_fixture_contains_required_files(self, valid_import_zip):
        """valid_import_zip contains required import structure."""
        with zipfile.ZipFile(valid_import_zip, 'r') as zf:
            names = zf.namelist()
            # Must have index.json and manifest.json
            assert "index.json" in names
            assert "manifest.json" in names
            # Must have feedback-sessions directory
            assert any("feedback-sessions/" in n for n in names)

    def test_fixture_has_valid_index_json(self, valid_import_zip):
        """valid_import_zip has valid index.json structure."""
        import json

        with zipfile.ZipFile(valid_import_zip, 'r') as zf:
            index_content = zf.read("index.json").decode('utf-8')
            index = json.loads(index_content)

            assert "export_metadata" in index
            assert "sessions" in index
            assert "created_at" in index["export_metadata"]

    def test_fixture_has_valid_manifest_json(self, valid_import_zip):
        """valid_import_zip has valid manifest.json structure."""
        import json

        with zipfile.ZipFile(valid_import_zip, 'r') as zf:
            manifest_content = zf.read("manifest.json").decode('utf-8')
            manifest = json.loads(manifest_content)

            assert "export_version" in manifest
            assert "framework_version" in manifest


class TestCleanupVerification:
    """Tests for cleanup behavior verification."""

    def test_temp_zip_dir_cleaned_after_test(self):
        """Verify temp_zip_dir is cleaned up after test scope."""
        # This test runs after TestTempZipDirFixture
        # We can't directly test cleanup, but we verify no orphaned dirs
        temp_root = Path(tempfile.gettempdir())

        # Should not have excessive test_zip_ prefixed directories
        test_dirs = list(temp_root.glob("test_zip_*"))
        # Allow some (current test might create one), but not many
        assert len(test_dirs) < 5, f"Found {len(test_dirs)} orphaned temp dirs"

    def test_no_orphan_zips_in_project_root(self, verify_no_orphan_zips):
        """verify_no_orphan_zips fixture catches orphaned files."""
        # This fixture should be autouse and fail if orphaned zips exist
        # Just verify fixture exists and runs
        assert True  # Fixture runs as autouse


class TestLargerImportZipFixture:
    """Tests for larger_import_zip fixture (for progress testing)."""

    def test_fixture_creates_larger_zip(self, larger_import_zip):
        """larger_import_zip creates zip with many sessions."""
        with zipfile.ZipFile(larger_import_zip, 'r') as zf:
            # Should have at least 50 session files
            session_files = [n for n in zf.namelist() if "session" in n]
            assert len(session_files) >= 50

    def test_fixture_has_matching_session_count(self, larger_import_zip):
        """larger_import_zip has matching session count in metadata."""
        import json

        with zipfile.ZipFile(larger_import_zip, 'r') as zf:
            session_files = [n for n in zf.namelist()
                           if n.startswith("feedback-sessions/") and n.endswith(".md")]

            index_content = zf.read("index.json").decode('utf-8')
            index = json.loads(index_content)

            assert len(index["sessions"]) == len(session_files)
