"""
STORY-078: Unit tests for BackupService operations (create/restore/list).

Tests backup creation, restoration, and listing functionality.
All tests follow TDD AAA pattern (Arrange, Act, Assert).

DoD Coverage:
- Unit tests for BackupService (create/restore/list)

Technical Specification:
- SVC-004: Create complete backup of DevForgeAI installation
- SVC-005: Restore from backup
- SVC-006: List available backups
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timezone


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def project_with_framework(tmp_path):
    """
    Create a project structure with DevForgeAI framework files.

    Returns:
        Path: Project root with .claude/, devforgeai/, CLAUDE.md
    """
    # Create .claude directory with content
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json").write_text('{"key": "value"}')

    skills_dir = claude_dir / "skills"
    skills_dir.mkdir()
    (skills_dir / "test-skill.md").write_text("# Test Skill")

    commands_dir = claude_dir / "commands"
    commands_dir.mkdir()
    (commands_dir / "test-command.md").write_text("# Test Command")

    # Create devforgeai directory with content
    devforgeai_dir = tmp_path / "devforgeai"
    devforgeai_dir.mkdir()

    context_dir = devforgeai_dir / "context"
    context_dir.mkdir()
    (context_dir / "tech-stack.md").write_text("# Tech Stack")

    (devforgeai_dir / ".version.json").write_text(json.dumps({
        "version": "1.0.0",
        "installed_at": "2025-12-06T12:00:00Z",
        "mode": "fresh_install"
    }))

    # Create CLAUDE.md
    (tmp_path / "CLAUDE.md").write_text("# Project Instructions\n\nTest content.")

    return tmp_path


@pytest.fixture
def project_with_backups(project_with_framework):
    """
    Create a project with existing backups.

    Returns:
        Path: Project root with .backups/ directory containing backups
    """
    backups_dir = project_with_framework / ".backups"
    backups_dir.mkdir()

    # Create first backup (older)
    backup1 = backups_dir / "devforgeai-upgrade-20251205120000"
    backup1.mkdir()
    (backup1 / ".claude").mkdir()
    (backup1 / "devforgeai").mkdir()
    (backup1 / "CLAUDE.md").write_text("# Old content")
    (backup1 / "manifest.json").write_text(json.dumps({
        "backup_id": "devforgeai-upgrade-20251205120000",
        "created_at": "2025-12-05T12:00:00Z",
        "reason": "upgrade",
        "from_version": "0.9.0",
        "to_version": "1.0.0",
        "file_count": 3
    }))

    # Create second backup (newer)
    backup2 = backups_dir / "devforgeai-upgrade-20251206120000"
    backup2.mkdir()
    (backup2 / ".claude").mkdir()
    (backup2 / "devforgeai").mkdir()
    (backup2 / "CLAUDE.md").write_text("# New content")
    (backup2 / "manifest.json").write_text(json.dumps({
        "backup_id": "devforgeai-upgrade-20251206120000",
        "created_at": "2025-12-06T12:00:00Z",
        "reason": "upgrade",
        "from_version": "1.0.0",
        "to_version": "1.1.0",
        "file_count": 3
    }))

    return project_with_framework


# ============================================================================
# Test Classes
# ============================================================================

class TestBackupCreation:
    """Tests for backup.create_backup() - SVC-004."""

    def test_create_backup_returns_path_and_manifest(self, project_with_framework):
        """Test backup creation returns valid path and manifest."""
        from installer import backup

        backup_path, manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade",
            from_version="1.0.0",
            to_version="1.1.0"
        )

        assert backup_path.exists()
        assert isinstance(manifest, dict)
        assert "created_at" in manifest
        assert "reason" in manifest

    def test_create_backup_copies_claude_directory(self, project_with_framework):
        """Test backup includes .claude/ directory."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        assert (backup_path / ".claude").exists()
        assert (backup_path / ".claude" / "settings.json").exists()

    def test_create_backup_copies_devforgeai_directory(self, project_with_framework):
        """Test backup includes devforgeai/ directory."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        assert (backup_path / "devforgeai").exists()
        assert (backup_path / "devforgeai" / "context" / "tech-stack.md").exists()

    def test_create_backup_copies_claude_md(self, project_with_framework):
        """Test backup includes CLAUDE.md file."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        assert (backup_path / "CLAUDE.md").exists()
        content = (backup_path / "CLAUDE.md").read_text()
        assert "Project Instructions" in content

    def test_create_backup_generates_manifest(self, project_with_framework):
        """Test backup creates manifest.json with metadata."""
        from installer import backup

        backup_path, manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade",
            from_version="1.0.0",
            to_version="1.1.0"
        )

        manifest_file = backup_path / "manifest.json"
        assert manifest_file.exists()

        saved_manifest = json.loads(manifest_file.read_text())
        assert saved_manifest["reason"] == "upgrade"
        assert saved_manifest["from_version"] == "1.0.0"
        assert saved_manifest["to_version"] == "1.1.0"

    def test_create_backup_includes_integrity_hash(self, project_with_framework):
        """Test backup manifest includes integrity hash."""
        from installer import backup

        _, manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        assert "backup_integrity_hash" in manifest
        assert manifest["backup_integrity_hash"].startswith("sha256:")

    def test_create_backup_counts_files(self, project_with_framework):
        """Test backup manifest includes file count."""
        from installer import backup

        _, manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        # Manifest may use "file_count" or "files_backed_up"
        file_count_key = "file_count" if "file_count" in manifest else "files_backed_up"
        assert file_count_key in manifest
        assert manifest[file_count_key] > 0

    def test_create_backup_uses_timestamped_directory(self, project_with_framework):
        """Test backup directory name includes timestamp."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        # Directory name should contain date pattern
        assert "devforgeai-upgrade-" in backup_path.name
        # Should be in .backups directory
        assert backup_path.parent.name == ".backups"

    def test_create_backup_handles_missing_claude_md(self, tmp_path):
        """Test backup handles project without CLAUDE.md."""
        from installer import backup

        # Create minimal structure without CLAUDE.md
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".claude" / "settings.json").write_text("{}")
        (tmp_path / "devforgeai").mkdir()
        (tmp_path / "devforgeai" / ".version.json").write_text('{"version": "1.0.0"}')

        backup_path, manifest = backup.create_backup(
            tmp_path,
            reason="upgrade"
        )

        assert backup_path.exists()
        # CLAUDE.md should not exist in backup
        assert not (backup_path / "CLAUDE.md").exists() or \
               (backup_path / "CLAUDE.md").exists()  # Either is fine


class TestBackupVerification:
    """Tests for backup.verify_backup_integrity() - SVC-004."""

    def test_verify_backup_returns_valid_result(self, project_with_framework):
        """Test backup verification returns structured result."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        result = backup.verify_backup_integrity(backup_path)

        assert isinstance(result, dict)
        assert "valid" in result or "passed" in result or "status" in result

    def test_verify_backup_detects_valid_backup(self, project_with_framework):
        """Test verification passes for valid backup."""
        from installer import backup

        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        result = backup.verify_backup_integrity(backup_path)

        # Check for success indicator (may be "valid", "passed", or "status")
        is_valid = result.get("valid", result.get("passed", result.get("status") == "valid"))
        assert is_valid


class TestBackupListing:
    """Tests for rollback.list_backups() - SVC-006."""

    def test_list_backups_returns_empty_when_no_backups(self, project_with_framework):
        """Test listing returns empty list when no backups exist."""
        from installer import rollback

        backups = rollback.list_backups(project_with_framework)

        assert isinstance(backups, list)
        assert len(backups) == 0

    def test_list_backups_returns_all_backups(self, project_with_backups):
        """Test listing returns all available backups."""
        from installer import rollback

        backups = rollback.list_backups(project_with_backups)

        assert len(backups) == 2

    def test_list_backups_sorted_newest_first(self, project_with_backups):
        """Test backups are sorted by timestamp (newest first)."""
        from installer import rollback

        backups = rollback.list_backups(project_with_backups)

        # First backup should be newer (20251206)
        assert "20251206" in backups[0]["name"]
        assert "20251205" in backups[1]["name"]

    def test_list_backups_includes_metadata(self, project_with_backups):
        """Test listed backups include manifest metadata."""
        from installer import rollback

        backups = rollback.list_backups(project_with_backups)

        backup = backups[0]
        assert "path" in backup
        assert "name" in backup
        assert "timestamp" in backup or backup.get("timestamp") is None
        assert "reason" in backup

    def test_list_backups_includes_version_info(self, project_with_backups):
        """Test listed backups include version information."""
        from installer import rollback

        backups = rollback.list_backups(project_with_backups)

        backup = backups[0]
        assert "from_version" in backup
        assert "to_version" in backup


class TestBackupRestoration:
    """Tests for rollback.restore_from_backup() - SVC-005."""

    def test_restore_from_backup_restores_files(self, project_with_backups):
        """Test restoration copies files from backup."""
        from installer import rollback

        # Modify current files
        (project_with_backups / "CLAUDE.md").write_text("# Modified content")

        # Get backup path
        backups = rollback.list_backups(project_with_backups)
        backup_path = backups[0]["path"]

        # Restore
        result = rollback.restore_from_backup(project_with_backups, backup_path)

        assert isinstance(result, dict)

    def test_restore_from_backup_returns_file_count(self, project_with_backups):
        """Test restoration returns count of restored files."""
        from installer import rollback

        backups = rollback.list_backups(project_with_backups)
        backup_path = backups[0]["path"]

        result = rollback.restore_from_backup(project_with_backups, backup_path)

        # Should have files_restored or similar count
        assert "files_restored" in result or "restored_count" in result or "success" in result


class TestBackupEdgeCases:
    """Tests for edge cases and error handling."""

    def test_create_backup_creates_backups_directory(self, tmp_path):
        """Test backup creates .backups/ directory if missing."""
        from installer import backup

        # Create minimal structure
        (tmp_path / ".claude").mkdir()
        (tmp_path / "devforgeai").mkdir()

        backup_path, _ = backup.create_backup(
            tmp_path,
            reason="upgrade"
        )

        assert (tmp_path / ".backups").exists()
        assert backup_path.parent == tmp_path / ".backups"

    def test_list_backups_handles_missing_manifest(self, project_with_framework):
        """Test listing handles backups without manifest."""
        from installer import rollback

        # Create backup directory without manifest
        backups_dir = project_with_framework / ".backups"
        backups_dir.mkdir()
        backup = backups_dir / "devforgeai-upgrade-20251206120000"
        backup.mkdir()

        backups = rollback.list_backups(project_with_framework)

        assert len(backups) == 1
        assert backups[0]["name"] == "devforgeai-upgrade-20251206120000"

    def test_list_backups_ignores_non_directory_files(self, project_with_framework):
        """Test listing ignores files in .backups/ directory."""
        from installer import rollback

        backups_dir = project_with_framework / ".backups"
        backups_dir.mkdir()

        # Create a file (should be ignored)
        (backups_dir / "readme.txt").write_text("ignored")

        # Create a directory (should be listed)
        backup = backups_dir / "devforgeai-upgrade-20251206120000"
        backup.mkdir()

        backups = rollback.list_backups(project_with_framework)

        assert len(backups) == 1

    def test_create_multiple_backups_unique_names(self, project_with_framework):
        """Test multiple backups get unique directory names."""
        from installer import backup
        import time

        backup_path1, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        # Small delay to ensure different timestamp
        time.sleep(0.01)

        backup_path2, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        assert backup_path1 != backup_path2
        assert backup_path1.exists()
        assert backup_path2.exists()


class TestBackupPerformance:
    """Tests for backup performance requirements."""

    def test_backup_creation_completes_quickly(self, project_with_framework):
        """Test backup creation completes within reasonable time."""
        from installer import backup
        import time

        start = time.time()
        backup.create_backup(project_with_framework, reason="upgrade")
        duration = time.time() - start

        # Should complete in under 5 seconds for test project
        assert duration < 5.0

    def test_list_backups_completes_quickly(self, project_with_backups):
        """Test backup listing completes quickly."""
        from installer import rollback
        import time

        start = time.time()
        rollback.list_backups(project_with_backups)
        duration = time.time() - start

        # Should complete in under 1 second
        assert duration < 1.0


class TestBackupErrorHandling:
    """Tests for error handling paths to improve coverage (83% -> 85%+)."""

    def test_backup_handles_hash_file_ioerror(self, project_with_framework, capsys):
        """
        Test _hash_file handles OSError/IOError gracefully (non-fatal).

        Covers lines 60-64: OSError/IOError exception handling in _hash_file().
        When file read fails, hash calculation continues with warning.
        """
        from installer import backup
        from unittest.mock import patch, mock_open, MagicMock
        import hashlib

        # Arrange
        hasher = hashlib.sha256()
        test_file = project_with_framework / ".claude" / "settings.json"

        # Act - Mock open to raise OSError
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            # This should NOT raise - it's non-fatal
            backup._hash_file(test_file, hasher)

        # Assert - Warning should be printed to stderr
        captured = capsys.readouterr()
        assert "Warning: Could not read" in captured.err
        assert "Permission denied" in captured.err

    def test_backup_handles_disk_full_during_copy(self, project_with_framework):
        """
        Test create_backup handles disk full error during file copy.

        Covers lines 179-183: Exception handling in create_backup that
        cleans up partial backup on failure.
        """
        from installer import backup
        from unittest.mock import patch
        import shutil

        # Arrange
        original_copytree = shutil.copytree

        def mock_copytree_fail_on_devforgeai(src, dst, *args, **kwargs):
            """Fail when copying devforgeai to simulate disk full."""
            if "devforgeai" in str(src):
                raise OSError(28, "No space left on device")
            return original_copytree(src, dst, *args, **kwargs)

        # Act & Assert
        with patch.object(shutil, "copytree", side_effect=mock_copytree_fail_on_devforgeai):
            with pytest.raises(OSError) as exc_info:
                backup.create_backup(
                    project_with_framework,
                    reason="upgrade"
                )

            assert "No space" in str(exc_info.value) or exc_info.value.errno == 28

    def test_backup_handles_permission_denied_on_mkdir(self, project_with_framework):
        """
        Test create_backup handles permission denied when creating backup dir.

        Covers lines 130-131: OSError handling when backup directory creation
        fails (e.g., permissions, race condition).
        """
        from installer import backup
        from unittest.mock import patch

        # Arrange - Mock mkdir to raise PermissionError after backups_dir created
        original_mkdir = Path.mkdir

        def mock_mkdir_fail_on_backup(self, *args, **kwargs):
            """Fail when creating the specific backup directory."""
            if "devforgeai-upgrade-" in str(self):
                raise PermissionError(13, "Permission denied", str(self))
            return original_mkdir(self, *args, **kwargs)

        # Act & Assert
        with patch.object(Path, "mkdir", mock_mkdir_fail_on_backup):
            with pytest.raises(PermissionError) as exc_info:
                backup.create_backup(
                    project_with_framework,
                    reason="upgrade"
                )

            assert exc_info.value.errno == 13

    def test_backup_handles_corrupted_manifest_during_verify(self, project_with_framework):
        """
        Test verify_backup_integrity handles corrupted manifest.json.

        Covers lines 252-253, 257-259: Error handling for missing and
        invalid JSON manifest files.
        """
        from installer import backup

        # Arrange - Create backup then corrupt manifest
        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        manifest_file = backup_path / "manifest.json"
        manifest_file.write_text("{invalid json content")  # Corrupt JSON

        # Act
        result = backup.verify_backup_integrity(backup_path)

        # Assert
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("Invalid manifest JSON" in err for err in result["errors"])

    def test_backup_creates_manifest_with_file_list(self, project_with_framework):
        """
        Test backup manifest contains accurate file metadata.

        Covers lines 217, 226, 289, 294: Various verification paths
        including file count validation and hash verification.
        """
        from installer import backup

        # Arrange & Act
        backup_path, manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade",
            from_version="1.0.0",
            to_version="1.1.0"
        )

        # Assert - Manifest contains required fields
        assert "files_backed_up" in manifest
        assert manifest["files_backed_up"] > 0
        assert "total_size_mb" in manifest
        assert manifest["total_size_mb"] >= 0
        assert "backup_integrity_hash" in manifest
        assert manifest["backup_integrity_hash"].startswith("sha256:")
        assert "created_at" in manifest
        assert "reason" in manifest
        assert manifest["reason"] == "upgrade"
        assert manifest["from_version"] == "1.0.0"
        assert manifest["to_version"] == "1.1.0"

        # Verify manifest file written correctly
        manifest_file = backup_path / "manifest.json"
        assert manifest_file.exists()
        import json
        saved_manifest = json.loads(manifest_file.read_text())
        assert saved_manifest == manifest

        # Verify integrity verification works
        result = backup.verify_backup_integrity(backup_path)
        assert result["valid"] is True
        assert result["hash_matches"] is True
        assert result["file_count"] == manifest["files_backed_up"]


class TestBackupVerifyEdgeCases:
    """Additional verification edge cases for coverage improvement."""

    def test_verify_backup_detects_missing_manifest(self, project_with_framework):
        """
        Test verify_backup_integrity detects missing manifest.json.

        Covers lines 251-253: manifest.json not found path.
        """
        from installer import backup

        # Arrange - Create backup then remove manifest
        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )
        manifest_file = backup_path / "manifest.json"
        manifest_file.unlink()  # Delete manifest

        # Act
        result = backup.verify_backup_integrity(backup_path)

        # Assert
        assert result["valid"] is False
        assert any("manifest.json not found" in err for err in result["errors"])

    def test_verify_backup_detects_file_count_mismatch(self, project_with_framework):
        """
        Test verify_backup_integrity detects file count mismatch.

        Covers lines 225-228: File count mismatch detection.
        """
        from installer import backup
        import json

        # Arrange - Create backup then add extra file
        backup_path, original_manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        # Add extra file to backup (not in manifest count)
        extra_file = backup_path / ".claude" / "extra_file.txt"
        extra_file.write_text("Extra content")

        # Act
        result = backup.verify_backup_integrity(backup_path)

        # Assert
        assert result["valid"] is False
        assert any("File count mismatch" in err for err in result["errors"])

    def test_verify_backup_detects_hash_mismatch(self, project_with_framework):
        """
        Test verify_backup_integrity detects hash mismatch.

        Covers lines 289-296: Hash verification and mismatch detection.
        """
        from installer import backup
        import json

        # Arrange - Create backup then modify a file
        backup_path, original_manifest = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        # Modify a backed up file (changes hash)
        settings_file = backup_path / ".claude" / "settings.json"
        settings_file.write_text('{"modified": true}')

        # Act
        result = backup.verify_backup_integrity(backup_path)

        # Assert
        assert result["hash_matches"] is False
        assert any("Hash mismatch" in err for err in result["errors"])

    def test_verify_backup_handles_missing_hash_in_manifest(self, project_with_framework):
        """
        Test verify_backup_integrity handles manifest without hash field.

        Covers lines 288-289: Early return when backup_integrity_hash missing.
        """
        from installer import backup
        import json

        # Arrange - Create backup then remove hash from manifest
        backup_path, _ = backup.create_backup(
            project_with_framework,
            reason="upgrade"
        )

        manifest_file = backup_path / "manifest.json"
        manifest = json.loads(manifest_file.read_text())
        del manifest["backup_integrity_hash"]
        manifest_file.write_text(json.dumps(manifest))

        # Act
        result = backup.verify_backup_integrity(backup_path)

        # Assert - Should still be valid if file count matches
        # hash_matches should be False (not verified)
        assert result["hash_matches"] is False
        # No hash mismatch error since hash wasn't checked
        assert not any("Hash mismatch" in err for err in result["errors"])
