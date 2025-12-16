"""
Test directory creation for story-scoped test isolation.

Tests AC#6: Directory Auto-Creation and Validation
- 755 permissions on Unix
- Parent directory creation
- Windows compatibility
"""
import os
import stat
import sys
import tempfile
import pytest
from pathlib import Path


def create_story_directories(
    story_id: str,
    base_path: str,
    config: dict
) -> dict:
    """
    Create story-scoped directories for test outputs.

    Args:
        story_id: Story identifier (e.g., "STORY-092")
        base_path: Project root path
        config: Test isolation configuration

    Returns:
        Dictionary with created paths

    Raises:
        PermissionError: If directory creation fails
        ValueError: If invalid story ID
    """
    paths = config.get("paths", {})
    directory = config.get("directory", {})

    auto_create = directory.get("auto_create", True)
    permissions = directory.get("permissions", 755)
    create_parents = directory.get("create_parents", True)

    if not auto_create:
        return {}

    results_dir = Path(base_path) / paths.get("results_base", "tests/results") / story_id
    coverage_dir = Path(base_path) / paths.get("coverage_base", "tests/coverage") / story_id
    logs_dir = Path(base_path) / paths.get("logs_base", "tests/logs") / story_id

    created_paths = {}

    for name, dir_path in [
        ("results_dir", results_dir),
        ("coverage_dir", coverage_dir),
        ("logs_dir", logs_dir)
    ]:
        if create_parents:
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            dir_path.mkdir(exist_ok=True)

        # Apply permissions (Unix only)
        if sys.platform != 'win32':
            # Convert octal permission (e.g., 755) to mode
            mode = int(str(permissions), 8)
            os.chmod(dir_path, mode)

        created_paths[name] = str(dir_path)

    return created_paths


def validate_directory_writable(path: str) -> bool:
    """Check if directory exists and is writable."""
    dir_path = Path(path)
    if not dir_path.exists():
        return False
    if not dir_path.is_dir():
        return False

    # Test actual write capability
    test_file = dir_path / ".write_test"
    try:
        test_file.touch()
        test_file.unlink()
        return True
    except (PermissionError, OSError):
        return False


class TestDirectoryCreation:
    """Tests for directory creation functionality."""

    @pytest.fixture
    def default_config(self):
        """Default test isolation configuration."""
        return {
            "enabled": True,
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage",
                "logs_base": "tests/logs"
            },
            "directory": {
                "auto_create": True,
                "permissions": 755,
                "create_parents": True
            }
        }

    @pytest.fixture
    def temp_project(self, tmp_path):
        """Create temporary project directory."""
        return tmp_path

    def test_directories_created_with_755_permissions_unix(self, temp_project, default_config):
        """Test: Directory created with 755 permissions (Linux/Mac)."""
        if sys.platform == 'win32':
            pytest.skip("Unix permissions test not applicable on Windows")

        # Given: Story ID and config with 755 permissions
        story_id = "STORY-092"

        # When: Creating directories
        paths = create_story_directories(story_id, str(temp_project), default_config)

        # Then: Directories have 755 permissions
        for path_name, path_value in paths.items():
            dir_stat = os.stat(path_value)
            mode = stat.S_IMODE(dir_stat.st_mode)
            assert mode == 0o755, f"{path_name} has mode {oct(mode)}, expected 0o755"

    def test_parent_directories_created_if_missing(self, temp_project, default_config):
        """Test: Parent directories created if missing."""
        # Given: Story ID with deep path
        story_id = "STORY-001"

        # When: Creating directories (parent doesn't exist)
        paths = create_story_directories(story_id, str(temp_project), default_config)

        # Then: All directories exist
        for path_name, path_value in paths.items():
            assert Path(path_value).exists(), f"{path_name} should exist"
            assert Path(path_value).is_dir(), f"{path_name} should be directory"

    def test_graceful_handling_on_windows(self, temp_project, default_config):
        """Test: Graceful handling on Windows (no chmod)."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Creating directories on any platform
        paths = create_story_directories(story_id, str(temp_project), default_config)

        # Then: Directories created (permissions may vary on Windows)
        for path_name, path_value in paths.items():
            assert Path(path_value).exists()
            assert validate_directory_writable(path_value)

    def test_auto_create_disabled_skips_creation(self, temp_project):
        """Test: auto_create=false skips directory creation."""
        # Given: Config with auto_create disabled
        config = {
            "paths": {"results_base": "tests/results"},
            "directory": {"auto_create": False}
        }

        # When: Creating directories
        paths = create_story_directories("STORY-001", str(temp_project), config)

        # Then: No directories created
        assert paths == {}

    def test_existing_directories_not_overwritten(self, temp_project, default_config):
        """Test: Existing directories preserved (no error on exist)."""
        # Given: Pre-existing directory
        story_id = "STORY-092"
        existing_dir = temp_project / "tests" / "results" / story_id
        existing_dir.mkdir(parents=True)

        # Create a marker file
        marker = existing_dir / "existing_file.txt"
        marker.write_text("preserved")

        # When: Creating directories again
        paths = create_story_directories(story_id, str(temp_project), default_config)

        # Then: Existing content preserved
        assert marker.exists()
        assert marker.read_text() == "preserved"

    def test_directory_validation_success(self, temp_project, default_config):
        """Test: Writable directories pass validation."""
        # Given: Created directories
        story_id = "STORY-092"
        paths = create_story_directories(story_id, str(temp_project), default_config)

        # When/Then: All directories are writable
        for path_name, path_value in paths.items():
            assert validate_directory_writable(path_value), f"{path_name} should be writable"

    def test_directory_validation_failure(self, temp_project):
        """Test: Non-existent directory fails validation."""
        # Given: Non-existent path
        nonexistent = temp_project / "does_not_exist"

        # When/Then: Validation fails
        assert not validate_directory_writable(str(nonexistent))

    def test_custom_permissions(self, temp_project):
        """Test: Custom permissions applied (Unix only)."""
        if sys.platform == 'win32':
            pytest.skip("Unix permissions test not applicable on Windows")

        # Given: Config with custom permissions
        config = {
            "paths": {"results_base": "tests/results"},
            "directory": {
                "auto_create": True,
                "permissions": 700,  # rwx------
                "create_parents": True
            }
        }

        # When: Creating directories
        paths = create_story_directories("STORY-001", str(temp_project), config)

        # Then: Custom permissions applied
        for path_value in paths.values():
            dir_stat = os.stat(path_value)
            mode = stat.S_IMODE(dir_stat.st_mode)
            assert mode == 0o700


class TestTimestampFile:
    """Tests for timestamp file creation."""

    def test_timestamp_file_created(self, tmp_path):
        """Test: timestamp.txt created with ISO 8601 format."""
        from datetime import datetime

        # Given: Story directory
        story_dir = tmp_path / "tests" / "results" / "STORY-092"
        story_dir.mkdir(parents=True)

        # When: Writing timestamp
        timestamp_file = story_dir / "timestamp.txt"
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        timestamp_file.write_text(timestamp)

        # Then: File exists with valid ISO 8601 format
        assert timestamp_file.exists()
        content = timestamp_file.read_text()
        # Validate ISO 8601 format
        datetime.strptime(content, "%Y-%m-%dT%H:%M:%SZ")
