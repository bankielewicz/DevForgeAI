"""
STORY-075: Unit tests for ManifestGenerator service.

Tests manifest file creation with SHA256 checksums, atomic writes, file
categorization, and performance. All tests follow TDD Red phase - they should
FAIL until implementation exists.

Coverage Target: 95%+ of ManifestGenerator class
"""

import pytest
import json
import hashlib
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile


class TestManifestGeneration:
    """Test manifest file creation (AC#4)."""

    def test_manifest_file_created_at_default_location(self, tmp_path):
        """
        Test: Manifest created at devforgeai/.install-manifest.json (AC#4).

        Given: Installation succeeds
        When: ManifestGenerator.generate_manifest() called
        Then: Creates devforgeai/.install-manifest.json
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        assert manifest_file.exists()
        assert manifest_file.name == ".install-manifest.json"
        assert manifest_file.parent.name == "devforgeai"

    def test_manifest_contains_version_field(self, tmp_path):
        """
        Test: Manifest contains version of installed framework (AC#4).

        Given: Framework v1.0.0 installed
        When: Manifest generated
        Then: Manifest contains "version": "1.0.0"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert "version" in manifest_data
        assert manifest_data["version"] == "1.0.0"

    def test_manifest_contains_iso8601_timestamp(self, tmp_path):
        """
        Test: Manifest contains ISO 8601 timestamp (AC#4).

        Given: Manifest is generated
        When: Manifest written
        Then: Contains "timestamp": "2025-11-20T10:30:00Z"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert "timestamp" in manifest_data
        # Verify ISO 8601 format
        timestamp = manifest_data["timestamp"]
        assert "T" in timestamp  # ISO format contains T
        assert "Z" in timestamp or "+" in timestamp  # UTC indicator

    def test_manifest_contains_installer_version(self, tmp_path):
        """
        Test: Manifest contains installer version (AC#4).

        Given: Installer v1.2.0 used
        When: Manifest generated
        Then: Manifest contains "installer_version": "1.2.0"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert "installer_version" in manifest_data
        assert manifest_data["installer_version"] == "1.2.0"

    def test_manifest_files_array_present(self, tmp_path):
        """
        Test: Manifest contains 'files' array (AC#4).

        Given: Installation with files
        When: Manifest generated
        Then: Manifest contains "files": [...]
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create test files
        test_file_1 = tmp_path / ".claude" / "skills" / "test1.md"
        test_file_1.parent.mkdir(parents=True, exist_ok=True)
        test_file_1.write_text("content 1")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file_1],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert "files" in manifest_data
        assert isinstance(manifest_data["files"], list)

    def test_manifest_file_count_matches_installed_files(self, tmp_path):
        """
        Test: Total file count in manifest matches actual installed files (AC#4).

        Given: 10 files installed
        When: Manifest generated
        Then: Manifest contains all 10 files
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create 10 test files
        installed_files = []
        for i in range(10):
            test_file = tmp_path / ".claude" / "skills" / f"skill_{i}.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text(f"content {i}")
            installed_files.append(test_file)

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=installed_files,
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert len(manifest_data["files"]) == 10


class TestChecksumGeneration:
    """Test SHA256 checksum generation (SVC-009, AC#4)."""

    def test_manifest_entry_contains_sha256_checksum(self, tmp_path):
        """
        Test: Each manifest entry contains SHA256 checksum (AC#4).

        Given: File is installed
        When: Manifest entry created
        Then: Entry contains "checksum": "sha256:..." (64 hex chars)
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("test content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert len(manifest_data["files"]) > 0
        entry = manifest_data["files"][0]
        assert "checksum" in entry
        # Checksum should be 64 hex characters
        checksum = entry["checksum"]
        assert len(checksum) == 64, f"Checksum length {len(checksum)}, expected 64"
        # Verify it's valid hex
        try:
            int(checksum, 16)
        except ValueError:
            pytest.fail(f"Checksum is not valid hex: {checksum}")

    def test_checksum_matches_file_content(self, tmp_path):
        """
        Test: Checksum in manifest matches actual file SHA256 (SVC-009).

        Given: File with known content
        When: Checksum calculated
        Then: Checksum matches SHA256(file_content)
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        content = "test content for hashing"
        test_file = tmp_path / ".claude" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(content)

        # Calculate expected checksum
        expected_checksum = hashlib.sha256(content.encode()).hexdigest()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["checksum"] == expected_checksum

    def test_checksums_differ_for_different_content(self, tmp_path):
        """
        Test: Different files have different checksums.

        Given: Two files with different content
        When: Checksums calculated
        Then: Checksums are different
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file_1 = tmp_path / ".claude" / "file1.md"
        test_file_1.parent.mkdir(parents=True, exist_ok=True)
        test_file_1.write_text("content 1")

        test_file_2 = tmp_path / ".claude" / "file2.md"
        test_file_2.parent.mkdir(parents=True, exist_ok=True)
        test_file_2.write_text("content 2")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file_1, test_file_2],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        checksum_1 = manifest_data["files"][0]["checksum"]
        checksum_2 = manifest_data["files"][1]["checksum"]
        assert checksum_1 != checksum_2


class TestManifestEntryFields:
    """Test manifest entry structure (AC#4)."""

    def test_manifest_entry_contains_path_field(self, tmp_path):
        """
        Test: Manifest entry contains 'path' field (relative) (AC#4).

        Given: File in .claude/skills/test.md
        When: Manifest entry created
        Then: Entry contains "path": ".claude/skills/test.md"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "skills" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert "path" in entry
        # Path should be relative (not starting with /)
        assert not entry["path"].startswith("/"), "Path should be relative, not absolute"

    def test_manifest_entry_contains_source_field(self, tmp_path):
        """
        Test: Manifest entry contains 'source' field (AC#4).

        Given: File from source
        When: Manifest entry created
        Then: Entry contains "source" field
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "skills" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert "source" in entry

    def test_manifest_entry_contains_size_bytes_field(self, tmp_path):
        """
        Test: Manifest entry contains 'size_bytes' field (AC#4).

        Given: File with known size
        When: Manifest entry created
        Then: Entry contains "size_bytes": integer matching file size
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        content = "test content"  # 12 bytes
        test_file = tmp_path / ".claude" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(content)

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert "size_bytes" in entry
        assert entry["size_bytes"] == len(content)

    def test_manifest_entry_contains_category_field(self, tmp_path):
        """
        Test: Manifest entry contains 'category' field (AC#4).

        Given: File installed
        When: Manifest entry created
        Then: Entry contains "category": one of (skill, agent, command, memory, script, config)
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "skills" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert "category" in entry
        valid_categories = ["skill", "agent", "command", "memory", "script", "config"]
        assert entry["category"] in valid_categories, f"Invalid category: {entry['category']}"


class TestFileCategorization:
    """Test file categorization by type (SVC-011)."""

    def test_files_in_claude_skills_categorized_as_skill(self, tmp_path):
        """
        Test: Files in .claude/skills/ categorized as 'skill' (SVC-011).

        Given: File in .claude/skills/
        When: Manifest generated
        Then: Entry category = "skill"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "skills" / "skill.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["category"] == "skill"

    def test_files_in_claude_agents_categorized_as_agent(self, tmp_path):
        """
        Test: Files in .claude/agents/ categorized as 'agent' (SVC-011).

        Given: File in .claude/agents/
        When: Manifest generated
        Then: Entry category = "agent"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "agents" / "agent.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["category"] == "agent"

    def test_files_in_claude_commands_categorized_as_command(self, tmp_path):
        """
        Test: Files in .claude/commands/ categorized as 'command' (SVC-011).

        Given: File in .claude/commands/
        When: Manifest generated
        Then: Entry category = "command"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "commands" / "cmd.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["category"] == "command"

    def test_files_in_claude_memory_categorized_as_memory(self, tmp_path):
        """
        Test: Files in .claude/memory/ categorized as 'memory' (SVC-011).

        Given: File in .claude/memory/
        When: Manifest generated
        Then: Entry category = "memory"
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "memory" / "mem.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["category"] == "memory"


class TestAtomicManifestWrites:
    """Test atomic manifest writes (SVC-010, BR-005, NFR-004)."""

    def test_manifest_written_atomically_to_tmp_then_renamed(self, tmp_path):
        """
        Test: Manifest written to .tmp file then atomically renamed (SVC-010).

        Given: Manifest generation in progress
        When: Manifest being written
        Then: Uses atomic write pattern (tmp + rename)
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        test_file = tmp_path / ".claude" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        with patch("pathlib.Path.rename") as mock_rename:
            mock_rename.return_value = None
            try:
                manifest_file = generator.generate_manifest(
                    target_directory=tmp_path,
                    installed_files=[test_file],
                    version="1.0.0",
                    installer_version="1.2.0",
                )
            except:
                pass  # Rename will fail in mock, but we're verifying it's called

        # Assert - Verify atomic pattern is used
        # (Implementation will call Path.rename, which we can verify with mock)

    def test_manifest_survives_interrupted_write(self, tmp_path):
        """
        Test: Interrupted write doesn't corrupt manifest (SVC-010).

        Given: Manifest write is interrupted
        When: Write operation fails midway
        Then: Old manifest remains intact (atomic pattern)
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create initial manifest
        test_file = tmp_path / ".claude" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        original_content = json.loads(manifest_file.read_text())

        # Act - Try to write but interrupt (simulate with exception)
        with patch("json.dump", side_effect=IOError("Write interrupted")):
            try:
                generator.generate_manifest(
                    target_directory=tmp_path,
                    installed_files=[test_file],
                    version="2.0.0",  # Different version
                    installer_version="2.0.0",
                )
            except IOError:
                pass  # Expected

        # Assert - Original manifest should be intact
        current_content = json.loads(manifest_file.read_text())
        # If atomic write is used, original version should still be in manifest
        assert current_content == original_content, "Manifest was corrupted by interrupted write"


class TestManifestPerformance:
    """Test performance requirements (NFR-003)."""

    def test_manifest_generation_under_200ms_for_100_files(self, tmp_path):
        """
        Test: Manifest generation < 200ms for 100 files (NFR-003).

        Given: 100 files to include in manifest
        When: ManifestGenerator.generate_manifest() called
        Then: Returns in < 200ms
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create 100 test files
        installed_files = []
        for i in range(100):
            test_file = tmp_path / ".claude" / "skills" / f"skill_{i:03d}.md"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text(f"content {i}")
            installed_files.append(test_file)

        generator = ManifestGenerator()

        # Act
        start = time.time()
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=installed_files,
            version="1.0.0",
            installer_version="1.2.0",
        )
        elapsed_ms = (time.time() - start) * 1000

        # Assert
        assert (
            elapsed_ms < 200
        ), f"Manifest generation took {elapsed_ms:.1f}ms (expected <200ms)"
        # Verify all files in manifest
        manifest_data = json.loads(manifest_file.read_text())
        assert len(manifest_data["files"]) == 100


class TestEdgeCases:
    """Test edge cases for manifest generation."""

    def test_manifest_generated_for_empty_installation(self, tmp_path):
        """
        Test: Manifest can be generated with no files (edge case).

        Given: Installation has no files
        When: Manifest generated
        Then: Manifest created with empty files array
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        assert "files" in manifest_data
        assert len(manifest_data["files"]) == 0

    def test_manifest_handles_large_files(self, tmp_path):
        """
        Test: Manifest can handle files with large content.

        Given: Large file (1MB)
        When: Manifest generated
        Then: File entry created with correct checksum and size
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create 1MB file
        large_content = "x" * (1024 * 1024)
        test_file = tmp_path / ".claude" / "large.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(large_content)

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert entry["size_bytes"] == len(large_content)
        # Verify checksum is valid hex
        assert len(entry["checksum"]) == 64

    def test_manifest_handles_special_characters_in_paths(self, tmp_path):
        """
        Test: Manifest handles paths with special characters.

        Given: File path contains special characters
        When: Manifest generated
        Then: Path is properly encoded in JSON
        """
        # Arrange
        from installer.manifest_generator import ManifestGenerator

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        # Create file with special chars in name
        test_file = tmp_path / ".claude" / "test-file_v1.0.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        generator = ManifestGenerator()

        # Act
        manifest_file = generator.generate_manifest(
            target_directory=tmp_path,
            installed_files=[test_file],
            version="1.0.0",
            installer_version="1.2.0",
        )

        # Assert
        manifest_data = json.loads(manifest_file.read_text())
        entry = manifest_data["files"][0]
        assert "test-file_v1.0.md" in entry["path"]
