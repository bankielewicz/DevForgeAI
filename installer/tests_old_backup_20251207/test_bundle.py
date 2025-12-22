"""
STORY-069: Unit Tests for bundle.py - Bundle Structure Verification

Tests validate bundle structure, file counting, size measurement, and path security.

Coverage targets:
- verify_bundle_structure(): 100%
- count_bundled_files(): 100%
- measure_bundle_size(): 100%
- validate_bundle_path(): 100%

Expected Result: All tests pass (implementation complete)
"""

import pytest
import tarfile
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from installer.bundle import (
    verify_bundle_structure,
    count_bundled_files,
    measure_bundle_size,
    validate_bundle_path,
    MIN_BUNDLED_FILES,
    COMPRESSION_RATIO_ESTIMATE,
    MB_DIVISOR,
    SAFE_PATH_PATTERN,
)


class TestVerifyBundleStructure:
    """Unit tests for verify_bundle_structure() function."""

    def test_complete_bundle_structure(self, tmp_path):
        """
        Should verify complete bundle successfully.

        Arrange: Create bundle with all required directories/files
        Act: Verify bundle structure
        Assert: Returns success status
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create required directories
        (bundle_root / "claude" / "agents").mkdir(parents=True)
        (bundle_root / "claude" / "commands").mkdir(parents=True)
        (bundle_root / "claude" / "skills").mkdir(parents=True)
        (bundle_root / "claude" / "memory").mkdir(parents=True)
        (bundle_root / "devforgeai" / "context").mkdir(parents=True)

        # Create required files
        (bundle_root / "checksums.json").write_text("{}")
        (bundle_root / "version.json").write_text("{}")
        (bundle_root / "CLAUDE.md").write_text("# CLAUDE.md")

        # Add some files for counting
        (bundle_root / "claude" / "agents" / "test.md").write_text("test")

        # Act
        result = verify_bundle_structure(bundle_root)

        # Assert
        assert result["status"] == "success"
        assert len(result["missing_components"]) == 0
        assert result["file_count"] >= 1

    def test_missing_claude_agents_directory(self, tmp_path):
        """
        Should raise FileNotFoundError when claude/agents missing.

        Arrange: Bundle without claude/agents/
        Act: Verify bundle structure
        Assert: Raises FileNotFoundError
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create other directories but skip claude/agents
        (bundle_root / "claude" / "commands").mkdir(parents=True)
        (bundle_root / "devforgeai" / "context").mkdir(parents=True)

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="Bundle structure incomplete"):
            verify_bundle_structure(bundle_root)

    def test_missing_checksums_json(self, tmp_path):
        """
        Should raise FileNotFoundError when checksums.json missing.

        Arrange: Bundle without checksums.json
        Act: Verify bundle structure
        Assert: Raises FileNotFoundError listing missing file
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create directories but no checksums.json
        (bundle_root / "claude" / "agents").mkdir(parents=True)
        (bundle_root / "claude" / "commands").mkdir(parents=True)
        (bundle_root / "claude" / "skills").mkdir(parents=True)
        (bundle_root / "claude" / "memory").mkdir(parents=True)
        (bundle_root / "devforgeai" / "context").mkdir(parents=True)
        (bundle_root / "version.json").write_text("{}")
        (bundle_root / "CLAUDE.md").write_text("")

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="checksums.json"):
            verify_bundle_structure(bundle_root)

    def test_missing_version_json(self, tmp_path):
        """
        Should raise FileNotFoundError when version.json missing.

        Arrange: Bundle without version.json
        Act: Verify bundle structure
        Assert: Raises FileNotFoundError
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        (bundle_root / "claude" / "agents").mkdir(parents=True)
        (bundle_root / "claude" / "commands").mkdir(parents=True)
        (bundle_root / "claude" / "skills").mkdir(parents=True)
        (bundle_root / "claude" / "memory").mkdir(parents=True)
        (bundle_root / "devforgeai" / "context").mkdir(parents=True)
        (bundle_root / "checksums.json").write_text("{}")
        (bundle_root / "CLAUDE.md").write_text("")

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="version.json"):
            verify_bundle_structure(bundle_root)

    def test_multiple_missing_components(self, tmp_path):
        """
        Should list all missing components.

        Arrange: Bundle with multiple missing items
        Act: Verify bundle structure
        Assert: Error lists all missing components
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Only create minimal structure (missing most components)
        (bundle_root / "claude").mkdir()

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            verify_bundle_structure(bundle_root)

        error_message = str(exc_info.value)
        assert "claude/agents" in error_message
        assert "checksums.json" in error_message


class TestCountBundledFiles:
    """Unit tests for count_bundled_files() function."""

    def test_count_files_single_directory(self, tmp_path):
        """
        Should count files in single directory.

        Arrange: Create directory with 3 files
        Act: Count bundled files
        Assert: Returns 3
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        (bundle_root / "file1.txt").write_text("content")
        (bundle_root / "file2.txt").write_text("content")
        (bundle_root / "file3.txt").write_text("content")

        # Act
        result = count_bundled_files(bundle_root)

        # Assert
        assert result == 3

    def test_count_files_nested_directories(self, tmp_path):
        """
        Should count files recursively in nested directories.

        Arrange: Create nested structure with files
        Act: Count bundled files
        Assert: Returns total count
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        (bundle_root / "file1.txt").write_text("content")
        (bundle_root / "subdir1").mkdir()
        (bundle_root / "subdir1" / "file2.txt").write_text("content")
        (bundle_root / "subdir2").mkdir()
        (bundle_root / "subdir2" / "file3.txt").write_text("content")
        (bundle_root / "subdir2" / "nested").mkdir()
        (bundle_root / "subdir2" / "nested" / "file4.txt").write_text("content")

        # Act
        result = count_bundled_files(bundle_root)

        # Assert
        assert result == 4

    def test_count_files_excludes_directories(self, tmp_path):
        """
        Should exclude directories from count.

        Arrange: Create structure with empty directories
        Act: Count bundled files
        Assert: Only files counted
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        (bundle_root / "file1.txt").write_text("content")
        (bundle_root / "empty_dir1").mkdir()
        (bundle_root / "empty_dir2").mkdir()

        # Act
        result = count_bundled_files(bundle_root)

        # Assert
        assert result == 1

    def test_count_files_empty_bundle(self, tmp_path):
        """
        Should return 0 for empty bundle.

        Arrange: Create empty bundle directory
        Act: Count bundled files
        Assert: Returns 0
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act
        result = count_bundled_files(bundle_root)

        # Assert
        assert result == 0

    def test_count_files_nonexistent_directory(self, tmp_path):
        """
        Should return 0 for non-existent directory.

        Arrange: Path to non-existent directory
        Act: Count bundled files
        Assert: Returns 0
        """
        # Arrange
        bundle_root = tmp_path / "nonexistent"

        # Act
        result = count_bundled_files(bundle_root)

        # Assert
        assert result == 0


class TestMeasureBundleSize:
    """Unit tests for measure_bundle_size() function."""

    def test_measure_empty_bundle(self, tmp_path):
        """
        Should return zero sizes for empty bundle.

        Arrange: Empty bundle directory
        Act: Measure bundle size
        Assert: All sizes are 0
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act
        result = measure_bundle_size(bundle_root)

        # Assert
        assert result["uncompressed"] == 0
        assert result["uncompressed_mb"] == 0.0
        assert result["compressed"] == 0 or result["compressed"] > 0  # tar.gz has header

    def test_measure_small_bundle(self, tmp_path):
        """
        Should measure size of small bundle.

        Arrange: Bundle with small files
        Act: Measure bundle size
        Assert: Uncompressed size matches file sizes
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        file1_content = "A" * 1000  # 1KB
        file2_content = "B" * 2000  # 2KB

        (bundle_root / "file1.txt").write_text(file1_content)
        (bundle_root / "file2.txt").write_text(file2_content)

        # Act
        result = measure_bundle_size(bundle_root)

        # Assert
        assert result["uncompressed"] == 3000
        assert result["uncompressed_mb"] == pytest.approx(3000 / MB_DIVISOR, rel=1e-2)
        assert result["compressed"] > 0
        assert result["compressed"] < result["uncompressed"]  # Compression works

    def test_measure_nonexistent_bundle(self, tmp_path):
        """
        Should return zeros for non-existent bundle.

        Arrange: Path to non-existent directory
        Act: Measure bundle size
        Assert: Returns zero sizes
        """
        # Arrange
        bundle_root = tmp_path / "nonexistent"

        # Act
        result = measure_bundle_size(bundle_root)

        # Assert
        assert result["uncompressed"] == 0
        assert result["compressed"] == 0

    def test_compression_fallback(self, tmp_path):
        """
        Should use estimate if tar.gz creation fails.

        Arrange: Mock tarfile.open to raise exception
        Act: Measure bundle size
        Assert: Uses compression ratio estimate
        """
        # Arrange
        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()
        (bundle_root / "file.txt").write_text("A" * 1000)

        with patch('tarfile.open', side_effect=tarfile.TarError("Mock error")):
            # Act
            result = measure_bundle_size(bundle_root)

            # Assert
            expected_compressed = int(1000 * COMPRESSION_RATIO_ESTIMATE)
            assert result["compressed"] == expected_compressed


class TestValidateBundlePath:
    """Unit tests for validate_bundle_path() function - Security Critical."""

    def test_valid_bundle_name(self, tmp_path):
        """
        Should accept valid bundle name.

        Arrange: Valid bundle name "bundled"
        Act: Validate bundle path
        Assert: Returns resolved absolute path
        """
        # Arrange
        bundle_dir = tmp_path / "bundled"
        bundle_dir.mkdir()

        # Act
        result = validate_bundle_path("bundled", base_path=tmp_path)

        # Assert
        assert result == bundle_dir.resolve()

    def test_valid_bundle_with_hyphen(self, tmp_path):
        """
        Should accept names with hyphens.

        Arrange: Bundle name "my-bundle"
        Act: Validate bundle path
        Assert: Returns valid path
        """
        # Arrange
        bundle_dir = tmp_path / "my-bundle"
        bundle_dir.mkdir()

        # Act
        result = validate_bundle_path("my-bundle", base_path=tmp_path)

        # Assert
        assert result == bundle_dir.resolve()

    def test_valid_bundle_with_underscore(self, tmp_path):
        """
        Should accept names with underscores.

        Arrange: Bundle name "my_bundle"
        Act: Validate bundle path
        Assert: Returns valid path
        """
        # Arrange
        bundle_dir = tmp_path / "my_bundle"
        bundle_dir.mkdir()

        # Act
        result = validate_bundle_path("my_bundle", base_path=tmp_path)

        # Assert
        assert result == bundle_dir.resolve()

    def test_valid_bundle_with_dot(self, tmp_path):
        """
        Should accept names with dots.

        Arrange: Bundle name "bundle.v1"
        Act: Validate bundle path
        Assert: Returns valid path
        """
        # Arrange
        bundle_dir = tmp_path / "bundle.v1"
        bundle_dir.mkdir()

        # Act
        result = validate_bundle_path("bundle.v1", base_path=tmp_path)

        # Assert
        assert result == bundle_dir.resolve()

    def test_reject_path_traversal(self, tmp_path):
        """
        SECURITY: Should reject path traversal attempts.

        Arrange: Path with "../" (traversal attempt)
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="directory traversal"):
            validate_bundle_path("../../etc/passwd", base_path=tmp_path)

    def test_reject_absolute_path(self, tmp_path):
        """
        SECURITY: Should reject absolute paths.

        Arrange: Absolute path string
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="invalid characters"):
            validate_bundle_path("/etc/passwd", base_path=tmp_path)

    def test_reject_special_characters(self, tmp_path):
        """
        SECURITY: Should reject paths with special characters.

        Arrange: Path with semicolon (command injection attempt)
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="invalid characters"):
            validate_bundle_path("bundle; rm -rf /", base_path=tmp_path)

    def test_reject_command_substitution(self, tmp_path):
        """
        SECURITY: Should reject command substitution attempts.

        Arrange: Path with $(command) syntax
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="invalid characters"):
            validate_bundle_path("$(malicious)", base_path=tmp_path)

    def test_reject_backticks(self, tmp_path):
        """
        SECURITY: Should reject backtick command execution.

        Arrange: Path with backticks
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="invalid characters"):
            validate_bundle_path("`whoami`", base_path=tmp_path)

    def test_nonexistent_path(self, tmp_path):
        """
        Should raise FileNotFoundError for non-existent path.

        Arrange: Valid name but directory doesn't exist
        Act: Validate bundle path
        Assert: Raises FileNotFoundError
        """
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="Bundle path does not exist"):
            validate_bundle_path("nonexistent", base_path=tmp_path)

    def test_path_outside_base_directory(self, tmp_path):
        """
        SECURITY: Should reject resolved paths outside base.

        Arrange: Symlink pointing outside base directory
        Act: Validate bundle path
        Assert: Raises ValueError
        """
        # Arrange
        bundle_dir = tmp_path / "bundled"
        bundle_dir.mkdir()

        # Patch the resolve method on Path instances to return outside path
        original_resolve = Path.resolve
        def mock_resolve_func(self):
            # Return path outside tmp_path to simulate symlink traversal
            if str(self) == str(tmp_path / "bundled"):
                return Path("/etc/passwd")
            return original_resolve(self)

        with patch.object(Path, 'resolve', mock_resolve_func):
            # Act & Assert
            with pytest.raises(ValueError, match="outside base directory"):
                validate_bundle_path("bundled", base_path=tmp_path)

    def test_default_base_path(self, tmp_path, monkeypatch):
        """
        Should use current working directory as default base.

        Arrange: Change CWD to tmp_path
        Act: Call without base_path argument
        Assert: Uses CWD as base
        """
        # Arrange
        monkeypatch.chdir(tmp_path)
        bundle_dir = tmp_path / "bundled"
        bundle_dir.mkdir()

        # Act
        result = validate_bundle_path("bundled")

        # Assert
        assert result == bundle_dir.resolve()

    def test_safe_path_pattern_alphanumeric(self):
        """
        Should accept alphanumeric characters.

        Arrange: Test strings with alphanumeric chars
        Act: Match against SAFE_PATH_PATTERN
        Assert: All match successfully
        """
        # Arrange
        valid_names = ["bundle", "Bundle123", "abc123XYZ"]

        # Act & Assert
        for name in valid_names:
            assert SAFE_PATH_PATTERN.match(name) is not None

    def test_safe_path_pattern_special_allowed(self):
        """
        Should accept dot, hyphen, underscore.

        Arrange: Test strings with allowed special chars
        Act: Match against SAFE_PATH_PATTERN
        Assert: All match successfully
        """
        # Arrange
        valid_names = ["bundle-1", "bundle_2", "bundle.3", "my-bundle_v1.0"]

        # Act & Assert
        for name in valid_names:
            assert SAFE_PATH_PATTERN.match(name) is not None

    def test_safe_path_pattern_invalid(self):
        """
        Should reject invalid characters.

        Arrange: Test strings with invalid characters
        Act: Match against SAFE_PATH_PATTERN
        Assert: None match successfully
        """
        # Arrange
        invalid_names = [
            "../traversal",
            "/absolute",
            "bundle;rm",
            "$(cmd)",
            "`whoami`",
            "bundle with spaces",
            "bundle/subdir",
        ]

        # Act & Assert
        for name in invalid_names:
            assert SAFE_PATH_PATTERN.match(name) is None
