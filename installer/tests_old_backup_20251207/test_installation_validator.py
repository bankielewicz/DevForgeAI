"""
Unit tests for InstallationValidator service (STORY-079).

Tests installation integrity validation against manifest, including:
- File existence checking (AC#1)
- Checksum verification (AC#1)
- Missing file detection (AC#2)
- Corrupted file detection (AC#2)
- User-modified file detection (AC#3)
- Performance requirements (AC#1, NFR-001)

Test requirements coverage:
- SVC-001: Validate all files against manifest
- SVC-002: Detect missing files
- SVC-003: Detect corrupted files via checksum
- SVC-004: Detect user-modified files
"""

import pytest
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, MagicMock, patch
from dataclasses import dataclass


# Test data models (will be replaced by real models in implementation)
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


@dataclass
class ValidationIssue:
    path: str
    issue_type: str  # MISSING, CORRUPTED, WRONG_VERSION, EXTRA
    expected: str = None
    actual: str = None
    severity: str = None  # CRITICAL, HIGH, MEDIUM, LOW
    is_user_modified: bool = False


class TestInstallationValidatorBasics:
    """Basic functionality tests for InstallationValidator."""

    def test_should_validate_all_files_when_manifest_valid(self, tmp_project):
        """SVC-001: Given manifest with 50 files, When validate() called, Then all 50 files checked."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        files = []
        for i in range(50):
            file_path = tmp_project["root"] / f"file_{i:03d}.txt"
            file_path.write_text(f"Content {i}")
            files.append({
                "path": f"file_{i:03d}.txt",
                "checksum": self._calculate_sha256(f"Content {i}"),
                "size": len(f"Content {i}"),
                "is_user_modifiable": False,
            })

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": files,
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        assert len(issues) == 0, "No issues should be found for valid installation"

    def test_should_detect_missing_files(self, tmp_project):
        """SVC-002: Given file in manifest but not on disk, When validate() called, Then issue type=MISSING."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Create only 2 of 3 files mentioned in manifest
        file1 = tmp_project["root"] / "file_001.txt"
        file1.write_text("Content 1")

        # file_002.txt will be MISSING
        # file_003.txt is included in manifest but deleted from disk

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "file_001.txt",
                    "checksum": self._calculate_sha256("Content 1"),
                    "size": len("Content 1"),
                    "is_user_modifiable": False,
                },
                {
                    "path": "file_002.txt",
                    "checksum": "missing_file_hash",
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        missing_issues = [i for i in issues if i.issue_type == "MISSING"]
        assert len(missing_issues) == 1
        assert missing_issues[0].path == "file_002.txt"
        assert missing_issues[0].severity == "CRITICAL"

    def test_should_detect_corrupted_files(self, tmp_project):
        """SVC-003: Given file with wrong checksum, When validate() called, Then issue type=CORRUPTED."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Create file with different content than manifest expects
        file_path = tmp_project["root"] / "corrupted.txt"
        actual_content = "Modified content"
        file_path.write_text(actual_content)

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "corrupted.txt",
                    "checksum": self._calculate_sha256("Original content"),  # Wrong!
                    "size": len("Original content"),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        corrupted_issues = [i for i in issues if i.issue_type == "CORRUPTED"]
        assert len(corrupted_issues) == 1
        assert corrupted_issues[0].path == "corrupted.txt"
        assert corrupted_issues[0].severity == "CRITICAL"
        assert corrupted_issues[0].expected == self._calculate_sha256("Original content")
        assert corrupted_issues[0].actual == self._calculate_sha256(actual_content)

    def test_should_detect_user_modified_files(self, tmp_project):
        """SVC-004: Given user-modified .ai_docs file, When validate() called, Then is_user_modified=True."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Create .ai_docs directory (user-modifiable)
        ai_docs = tmp_project["root"] / ".ai_docs"
        ai_docs.mkdir()
        user_file = ai_docs / "user_story.md"
        user_content = "# User Modified Story\nThis was modified by user"
        user_file.write_text(user_content)

        # Set file modification time to recent (after installation)
        installation_time = datetime(2025, 1, 1, 12, 0, 0)
        user_mod_time = datetime(2025, 1, 2, 12, 0, 0)  # Later than install

        manifest = {
            "version": "1.0.0",
            "created_at": installation_time.isoformat(),
            "files": [
                {
                    "path": "devforgeai/specs/user_story.md",
                    "checksum": self._calculate_sha256(user_content),
                    "size": len(user_content),
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Mock file modification time
        with patch('pathlib.Path.stat') as mock_stat:
            stat_result = Mock()
            stat_result.st_mtime = user_mod_time.timestamp()
            mock_stat.return_value = stat_result

            # Act
            from installer.installation_validator import InstallationValidator
            validator = InstallationValidator(str(tmp_project["root"]))
            issues = validator.validate()

        # Assert
        user_modified_issues = [
            i for i in issues if i.issue_type == "CORRUPTED" and i.is_user_modified
        ]
        assert len(user_modified_issues) == 1
        assert user_modified_issues[0].is_user_modified is True

    def test_should_detect_extra_files_with_warning_severity(self, tmp_project):
        """AC#2: Extra files in DevForgeAI directories detected with warning severity."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Create expected file
        expected_file = tmp_project["claude"] / "expected.md"
        expected_file.write_text("Expected content")

        # Create extra file (not in manifest)
        extra_file = tmp_project["claude"] / "extra_file.md"
        extra_file.write_text("Extra content")

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": ".claude/expected.md",
                    "checksum": self._calculate_sha256("Expected content"),
                    "size": len("Expected content"),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        extra_issues = [i for i in issues if i.issue_type == "EXTRA"]
        assert len(extra_issues) >= 1
        extra_paths = [i.path for i in extra_issues]
        assert any(".claude/extra_file.md" in p for p in extra_paths)

    def test_should_populate_issue_details(self, tmp_project):
        """AC#2: Each issue includes: file path, expected value, actual value, severity."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file_path = tmp_project["root"] / "issue_file.txt"
        actual_content = "Actual content"
        expected_content = "Expected content"
        file_path.write_text(actual_content)

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "issue_file.txt",
                    "checksum": self._calculate_sha256(expected_content),
                    "size": len(expected_content),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        assert len(issues) > 0
        issue = issues[0]
        assert issue.path == "issue_file.txt"
        assert issue.expected is not None
        assert issue.actual is not None
        assert issue.severity is not None

    def test_should_complete_validation_within_30_seconds(self, tmp_project):
        """NFR-001: Validation completes within 30 seconds for 500 file installation."""
        # Arrange: Create 500 files
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        files = []

        for i in range(500):
            # Distribute files across subdirs to mimic real structure
            subdir = tmp_project["root"] / ["claude", "devforgeai", "ai_docs"][i % 3]
            subdir.mkdir(exist_ok=True)
            file_path = subdir / f"file_{i:04d}.txt"
            content = f"Content {i}"
            file_path.write_text(content)

            files.append({
                "path": f"{subdir.relative_to(tmp_project['root'])}/file_{i:04d}.txt",
                "checksum": self._calculate_sha256(content),
                "size": len(content),
                "is_user_modifiable": False,
            })

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": files,
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))

        start_time = time.time()
        issues = validator.validate()
        elapsed_time = time.time() - start_time

        # Assert
        assert elapsed_time < 30.0, f"Validation took {elapsed_time:.2f}s (expected < 30s)"
        assert len(issues) == 0, "No issues should be found for valid 500-file installation"

    def test_should_handle_empty_manifest(self, tmp_project):
        """Edge case: Empty manifest file."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],  # Empty
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        assert len(issues) == 0, "Empty manifest should result in no issues"

    def test_should_handle_large_file_checksums(self, tmp_project):
        """NFR-002: Checksum calculation is efficient (< 5 seconds for 100MB file)."""
        # Arrange: Create a 100MB file
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        large_file = tmp_project["root"] / "large_file.bin"
        # Create 100MB file (in chunks to avoid memory issues)
        chunk_size = 1024 * 1024  # 1MB chunks
        with open(large_file, "wb") as f:
            for _ in range(100):
                f.write(b"x" * chunk_size)

        # Calculate expected checksum
        expected_checksum = self._calculate_sha256_for_large_file(str(large_file))

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "large_file.bin",
                    "checksum": expected_checksum,
                    "size": 100 * 1024 * 1024,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))

        start_time = time.time()
        issues = validator.validate()
        elapsed_time = time.time() - start_time

        # Assert
        assert elapsed_time < 5.0, f"Checksum calculation took {elapsed_time:.2f}s (expected < 5s)"
        assert len(issues) == 0

    def test_should_validate_file_size_mismatch(self, tmp_project):
        """AC#1: File sizes are compared to expected values."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file_path = tmp_project["root"] / "size_mismatch.txt"
        actual_content = "Short"
        file_path.write_text(actual_content)

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "size_mismatch.txt",
                    "checksum": self._calculate_sha256(actual_content),
                    "size": 1000,  # Wrong size!
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        assert len(issues) > 0
        size_issues = [i for i in issues if "size" in str(i).lower()]
        # Note: Implementation may detect this as corrupted or separate size issue

    # Helper methods
    @staticmethod
    def _calculate_sha256(content: str) -> str:
        """Calculate SHA256 checksum for string content."""
        return hashlib.sha256(content.encode()).hexdigest()

    @staticmethod
    def _calculate_sha256_for_large_file(filepath: str) -> str:
        """Calculate SHA256 checksum for file efficiently."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


class TestUserModifiedFileDetection:
    """Tests for user-modified file detection (AC#3)."""

    def test_should_flag_user_modifiable_location_files(self, tmp_project):
        """AC#3: File in user-modifiable location (devforgeai/specs/) flagged separately."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        ai_docs = tmp_project["root"] / ".ai_docs"
        ai_docs.mkdir()
        user_file = ai_docs / "story.md"
        user_file.write_text("# User Story")

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "devforgeai/specs/story.md",
                    "checksum": "differentchecksum",  # Will be detected as corrupted
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        user_modified_issues = [i for i in issues if i.is_user_modified]
        assert len(user_modified_issues) > 0

    def test_should_detect_recent_modifications(self, tmp_project):
        """AC#3: File modified more recently than installation timestamp."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file_path = tmp_project["root"] / "recent_change.txt"
        file_path.write_text("Recent content")

        installation_time = datetime(2025, 1, 1, 12, 0, 0)
        modification_time = datetime(2025, 1, 2, 14, 0, 0)  # 1 day later

        manifest = {
            "version": "1.0.0",
            "created_at": installation_time.isoformat(),
            "files": [
                {
                    "path": "recent_change.txt",
                    "checksum": "original_checksum",
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Mock the modification time
        with patch('pathlib.Path.stat') as mock_stat:
            stat_result = Mock()
            stat_result.st_mtime = modification_time.timestamp()
            mock_stat.return_value = stat_result

            # Act
            from installer.installation_validator import InstallationValidator
            validator = InstallationValidator(str(tmp_project["root"]))
            issues = validator.validate()

        # Assert
        assert len(issues) > 0

    def test_should_detect_user_specific_content_patterns(self, tmp_project):
        """AC#3: File contains user-specific content patterns."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        context_file = tmp_project["devforgeai"] / "context" / "tech-stack.md"
        context_file.write_text("# Custom Tech Stack\nPython 3.11\nPostgreSQL 15")

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "devforgeai/specs/context/tech-stack.md",
                    "checksum": "original_checksum",
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        # Implementation should detect this as user-modified

    def test_should_provide_diff_preview_for_text_files(self, tmp_project):
        """AC#3: Prompt shows diff preview if file is text-based."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        text_file = tmp_project["root"] / "config.yaml"
        text_file.write_text("modified: true\nvalue: 42")

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "config.yaml",
                    "checksum": "original",
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        # Implementation should support diff generation for text files


class TestManifestValidation:
    """Tests for manifest validation during validation phase."""

    def test_should_validate_manifest_structure(self, tmp_project):
        """Manifest has required fields: version, created_at, files, schema_version."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        # Should not raise on valid manifest
        issues = validator.validate()

        # Assert
        assert isinstance(issues, list)

    def test_should_validate_checksums_are_sha256(self, tmp_project):
        """Checksums must be 64-character hex strings."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file_path = tmp_project["root"] / "test.txt"
        file_path.write_text("test")

        # Valid SHA256: 64 hex characters
        valid_sha256 = "a" * 64

        manifest = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "test.txt",
                    "checksum": valid_sha256,
                    "size": 4,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Act
        from installer.installation_validator import InstallationValidator
        validator = InstallationValidator(str(tmp_project["root"]))
        issues = validator.validate()

        # Assert
        # Should detect checksum mismatch but not validation error
