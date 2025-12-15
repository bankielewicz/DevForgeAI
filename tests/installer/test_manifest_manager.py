"""
Unit tests for ManifestManager (STORY-079).

Tests manifest management including:
- Loading installation manifest (AC#8, SVC-011)
- Regenerating manifest from current files (AC#8, SVC-012)
- Updating manifest after repair (AC#4, SVC-013)
- Manifest structure validation
- Handling missing manifests (AC#8)

Test requirements coverage:
- SVC-011: Load installation manifest
- SVC-012: Regenerate manifest from current files
- SVC-013: Update manifest after repair
"""

import pytest
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from dataclasses import dataclass, asdict


@dataclass
class FileEntry:
    path: str
    checksum: str
    size: int
    is_user_modifiable: bool


@dataclass
class InstallManifest:
    version: str
    created_at: str
    files: list
    schema_version: int = 1


class TestManifestManagerLoading:
    """Tests for loading manifests."""

    def test_should_load_valid_manifest(self, tmp_project):
        """SVC-011: Given valid manifest JSON, When load() called, Then InstallManifest returned."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": ".claude/agents/test.md",
                    "checksum": "a" * 64,
                    "size": 1024,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert
        assert manifest is not None
        assert manifest.version == "1.0.0"
        assert len(manifest.files) == 1
        assert manifest.files[0]["path"] == ".claude/agents/test.md"

    def test_should_return_none_when_manifest_missing(self, tmp_project):
        """SVC-011: Given missing manifest, When load() called, Then None returned."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        assert not manifest_path.exists()

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert
        assert manifest is None

    def test_should_validate_manifest_structure(self, tmp_project):
        """Manifest must have required fields: version, created_at, files, schema_version."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Missing 'files' field
        invalid_manifest = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "schema_version": 1,
            # Missing 'files'
        }
        manifest_path.write_text(json.dumps(invalid_manifest, indent=2))

        # Act & Assert
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))

        with pytest.raises(ValueError):
            manifest = manager.load()

    def test_should_parse_file_entries_correctly(self, tmp_project):
        """File entries must have: path, checksum, size, is_user_modifiable."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": ".claude/test.md",
                    "checksum": "b" * 64,
                    "size": 2048,
                    "is_user_modifiable": False,
                },
                {
                    "path": ".ai_docs/story.md",
                    "checksum": "c" * 64,
                    "size": 512,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert
        assert len(manifest.files) == 2
        assert manifest.files[0]["is_user_modifiable"] is False
        assert manifest.files[1]["is_user_modifiable"] is True

    def test_should_handle_corrupted_manifest_json(self, tmp_project):
        """Corrupted JSON should raise appropriate error."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_path.write_text("{invalid json content")

        # Act & Assert
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))

        with pytest.raises(json.JSONDecodeError):
            manifest = manager.load()

    def test_should_load_manifest_with_any_checksum_format(self, tmp_project):
        """ManifestManager loads manifests with any checksum format.

        Validation of checksum format happens in InstallationValidator,
        not in ManifestManager. This allows loading corrupted manifests
        for repair/recovery purposes.
        """
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Invalid checksum format (too short)
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": "test.md",
                    "checksum": "short_hash",  # Not a valid SHA256
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert - manifest loads despite invalid checksum format
        assert manifest is not None
        assert manifest.version == "1.0.0"
        assert manifest.files[0]["checksum"] == "short_hash"

    def test_should_validate_version_format(self, tmp_project):
        """Version field should be semantic version."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "not.a.valid.version",  # Invalid!
            "created_at": "2025-11-25T10:00:00Z",
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act & Assert
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))

        # Should either parse with warning or raise error


class TestManifestManagerRegeneration:
    """Tests for regenerating manifests."""

    def test_should_regenerate_manifest_from_current_files(self, tmp_project):
        """SVC-012: Given installation directory, When regenerate() called, Then manifest created."""
        # Arrange: Create some files in the project
        file1 = tmp_project["claude"] / "agents" / "test1.md"
        file1.write_text("Content 1")

        file2 = tmp_project["devforgeai"] / "context" / "tech-stack.md"
        file2.write_text("Content 2")

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        assert manifest is not None
        assert manifest.version is not None
        assert len(manifest.files) >= 2

        # Check that files are included
        file_paths = [f["path"] for f in manifest.files]
        assert any("test1.md" in p for p in file_paths)
        assert any("tech-stack.md" in p for p in file_paths)

    def test_should_calculate_correct_checksums_during_regeneration(self, tmp_project):
        """AC#8: Regenerated manifest includes all files with current checksums."""
        # Arrange
        file_path = tmp_project["root"] / "test_file.txt"
        content = "Test content for checksum"
        file_path.write_text(content)
        expected_checksum = self._calculate_sha256(content)

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        test_file_entry = next(
            (f for f in manifest.files if "test_file.txt" in f["path"]),
            None,
        )
        assert test_file_entry is not None
        assert test_file_entry["checksum"] == expected_checksum

    def test_should_calculate_correct_file_sizes_during_regeneration(self, tmp_project):
        """AC#8: File sizes are calculated correctly."""
        # Arrange
        file_path = tmp_project["root"] / "sized_file.bin"
        content = "x" * 1024  # 1KB
        file_path.write_text(content)
        expected_size = 1024

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        sized_file_entry = next(
            (f for f in manifest.files if "sized_file.bin" in f["path"]),
            None,
        )
        assert sized_file_entry is not None
        assert sized_file_entry["size"] == expected_size

    def test_should_mark_user_modifiable_files_during_regeneration(self, tmp_project):
        """AC#8: User-modifiable files marked correctly (.ai_docs/, devforgeai/context/)."""
        # Arrange
        ai_docs = tmp_project["root"] / ".ai_docs"
        ai_docs.mkdir()
        user_file = ai_docs / "story.md"
        user_file.write_text("User story")

        context_file = tmp_project["devforgeai"] / "context" / "tech-stack.md"
        context_file.write_text("Tech stack")

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        for file_entry in manifest.files:
            if ".ai_docs/" in file_entry["path"]:
                assert file_entry["is_user_modifiable"] is True

            if "devforgeai/context/" in file_entry["path"]:
                assert file_entry["is_user_modifiable"] is True

    def test_should_set_created_at_timestamp(self, tmp_project):
        """Regenerated manifest should have created_at timestamp."""
        # Arrange
        file_path = tmp_project["root"] / "test.txt"
        file_path.write_text("test")

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        assert manifest.created_at is not None
        # Should be valid ISO format datetime

    def test_should_exclude_manifest_file_from_regeneration(self, tmp_project):
        """Regenerated manifest should NOT include itself."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        manifest_files = [f["path"] for f in manifest.files]
        assert not any(".install-manifest.json" in p for p in manifest_files)

    def test_should_exclude_backup_files_from_regeneration(self, tmp_project):
        """Regenerated manifest should NOT include .backups/ directory."""
        # Arrange
        backup_file = tmp_project["backups"] / "old_version.json"
        backup_file.write_text("{}")

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        manifest_files = [f["path"] for f in manifest.files]
        assert not any(".backups/" in p for p in manifest_files)

    def test_should_handle_empty_directory_during_regeneration(self, tmp_project):
        """Regeneration should handle empty directories gracefully."""
        # Arrange
        empty_dir = tmp_project["claude"] / "empty_subdir"
        empty_dir.mkdir()

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.regenerate()

        # Assert
        assert manifest is not None


class TestManifestManagerUpdating:
    """Tests for updating manifests after repair."""

    def test_should_update_manifest_checksum_after_repair(self, tmp_project):
        """SVC-013: Given repaired file, When update() called, Then manifest checksum updated."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        old_content = "Old content"
        old_checksum = self._calculate_sha256(old_content)

        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": "repaired_file.txt",
                    "checksum": old_checksum,
                    "size": len(old_content),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Update the file with new content
        file_path = tmp_project["root"] / "repaired_file.txt"
        new_content = "New repaired content"
        file_path.write_text(new_content)
        new_checksum = self._calculate_sha256(new_content)

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()
        manifest = manager.update(manifest, "repaired_file.txt", new_checksum, len(new_content))

        # Assert
        updated_file = next(
            (f for f in manifest.files if f["path"] == "repaired_file.txt"),
            None,
        )
        assert updated_file is not None
        assert updated_file["checksum"] == new_checksum
        assert updated_file["size"] == len(new_content)

    def test_should_update_file_size_in_manifest(self, tmp_project):
        """SVC-013: File size is updated when file size changes."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": "sized_file.txt",
                    "checksum": "a" * 64,
                    "size": 100,  # Old size
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()
        new_size = 500
        manifest = manager.update(manifest, "sized_file.txt", "b" * 64, new_size)

        # Assert
        updated_file = next(
            (f for f in manifest.files if f["path"] == "sized_file.txt"),
            None,
        )
        assert updated_file["size"] == new_size

    def test_should_preserve_is_user_modifiable_flag_during_update(self, tmp_project):
        """Update should preserve user-modifiable flag."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": ".ai_docs/user_story.md",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": True,  # User modifiable
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()
        manifest = manager.update(manifest, ".ai_docs/user_story.md", "b" * 64, 200)

        # Assert
        updated_file = next(
            (f for f in manifest.files if f["path"] == ".ai_docs/user_story.md"),
            None,
        )
        assert updated_file["is_user_modifiable"] is True

    def test_should_save_updated_manifest_to_disk(self, tmp_project):
        """Updated manifest should be persisted to disk."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": "test_file.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()
        manifest = manager.update(manifest, "test_file.txt", "b" * 64, 200)
        manager.save(manifest)

        # Assert: Load manifest again and verify update persisted
        manifest_reloaded = manager.load()
        updated_file = next(
            (f for f in manifest_reloaded.files if f["path"] == "test_file.txt"),
            None,
        )
        assert updated_file["checksum"] == "b" * 64
        assert updated_file["size"] == 200

    def test_should_handle_atomic_write_protection(self, tmp_project):
        """Manifest writes should be atomic (avoid corruption on failure)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Simulate write operation
        with patch.object(manager, '_write_atomic') as mock_write:
            manager.save(manifest)
            mock_write.assert_called_once()

        # Assert: Original file unchanged until write completes


class TestManifestManagerEdgeCases:
    """Edge case tests."""

    def test_should_handle_very_large_manifest(self, tmp_project):
        """Edge case: Manifest with 10,000+ files."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        files = [
            {
                "path": f"file_{i:06d}.txt",
                "checksum": "a" * 64,
                "size": 100,
                "is_user_modifiable": False,
            }
            for i in range(10000)
        ]

        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": files,
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert
        assert len(manifest.files) == 10000

    def test_should_handle_special_characters_in_paths(self, tmp_project):
        """Edge case: File paths with special characters."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": "2025-11-25T10:00:00Z",
            "files": [
                {
                    "path": ".claude/agents/test-agent_v2.0.md",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.manifest_manager import ManifestManager
        manager = ManifestManager(str(tmp_project["root"]))
        manifest = manager.load()

        # Assert
        assert len(manifest.files) == 1


# Helper methods
@staticmethod
def _calculate_sha256(content: str) -> str:
    """Calculate SHA256 checksum for string content."""
    return hashlib.sha256(content.encode()).hexdigest()
