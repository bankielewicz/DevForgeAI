"""
Test path resolution for story-scoped test isolation.

Tests AC#1 and AC#2: Story-Scoped Directory Structure
- Story ID to path mapping
- Path traversal prevention
- Invalid story ID rejection
"""
import re
import pytest
from pathlib import Path


def validate_story_id(story_id: str) -> bool:
    """
    Validate story ID format to prevent path traversal attacks.

    Valid: STORY-001, STORY-092, STORY-1234
    Invalid: ../STORY-001, STORY-001/../../etc, STORY 001
    """
    pattern = r'^STORY-\d{1,4}$'
    return bool(re.match(pattern, story_id))


def resolve_story_paths(story_id: str, config: dict) -> dict:
    """
    Generate all story-scoped paths for a given story ID.

    Args:
        story_id: Story identifier (e.g., "STORY-092")
        config: Loaded test-isolation.yaml configuration

    Returns:
        Dictionary with results_dir, coverage_dir, logs_dir paths

    Raises:
        ValueError: If story_id is invalid
    """
    if not validate_story_id(story_id):
        raise ValueError(f"Invalid story ID format: {story_id}")

    paths = config.get("paths", {})

    results_base = paths.get("results_base", "tests/results")
    coverage_base = paths.get("coverage_base", "tests/coverage")
    logs_base = paths.get("logs_base", "tests/logs")

    return {
        "results_dir": f"{results_base}/{story_id}",
        "coverage_dir": f"{coverage_base}/{story_id}",
        "logs_dir": f"{logs_base}/{story_id}"
    }


class TestStoryIdValidation:
    """Tests for story ID validation."""

    def test_valid_story_id_passes(self):
        """Test: Valid story IDs are accepted."""
        valid_ids = [
            "STORY-001",
            "STORY-092",
            "STORY-1234",
            "STORY-1"
        ]

        for story_id in valid_ids:
            assert validate_story_id(story_id), f"{story_id} should be valid"

    def test_invalid_story_id_rejected(self):
        """Test: Invalid story IDs are rejected."""
        invalid_ids = [
            "../STORY-001",           # Path traversal
            "STORY-001/../etc",       # Path traversal
            "STORY 001",              # Space
            "story-001",              # Lowercase
            "STORY-",                 # No number
            "STORY-12345",            # Too many digits
            "STORY-001.md",           # Extension
            "EPIC-001",               # Wrong prefix
            "",                       # Empty
        ]

        for story_id in invalid_ids:
            assert not validate_story_id(story_id), f"{story_id} should be invalid"


class TestPathResolution:
    """Tests for path resolution functionality."""

    @pytest.fixture
    def default_config(self):
        """Default test isolation configuration."""
        return {
            "enabled": True,
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage",
                "logs_base": "tests/logs"
            }
        }

    def test_story_037_returns_correct_path(self, default_config):
        """Test: STORY-037 returns tests/results/STORY-037/."""
        # Given: Story ID STORY-037
        story_id = "STORY-037"

        # When: Resolving paths
        paths = resolve_story_paths(story_id, default_config)

        # Then: Correct paths returned
        assert paths["results_dir"] == "tests/results/STORY-037"
        assert paths["coverage_dir"] == "tests/coverage/STORY-037"
        assert paths["logs_dir"] == "tests/logs/STORY-037"

    def test_story_001_returns_correct_path(self, default_config):
        """Test: STORY-001 returns tests/results/STORY-001/."""
        # Given: Story ID STORY-001
        story_id = "STORY-001"

        # When: Resolving paths
        paths = resolve_story_paths(story_id, default_config)

        # Then: Correct paths returned
        assert paths["results_dir"] == "tests/results/STORY-001"
        assert paths["coverage_dir"] == "tests/coverage/STORY-001"
        assert paths["logs_dir"] == "tests/logs/STORY-001"

    def test_path_traversal_prevented(self, default_config):
        """Test: Path traversal attempts are rejected."""
        # Given: Malicious story IDs
        malicious_ids = [
            "../STORY-001",
            "STORY-001/../../../etc/passwd",
            "STORY-001/../../../../",
        ]

        for malicious_id in malicious_ids:
            # When/Then: ValueError raised
            with pytest.raises(ValueError, match="Invalid story ID"):
                resolve_story_paths(malicious_id, default_config)

    def test_custom_base_paths(self):
        """Test: Custom base paths are respected."""
        # Given: Custom configuration
        custom_config = {
            "paths": {
                "results_base": "output/test-results",
                "coverage_base": "output/coverage",
                "logs_base": "output/logs"
            }
        }

        # When: Resolving paths
        paths = resolve_story_paths("STORY-092", custom_config)

        # Then: Custom paths used
        assert paths["results_dir"] == "output/test-results/STORY-092"
        assert paths["coverage_dir"] == "output/coverage/STORY-092"
        assert paths["logs_dir"] == "output/logs/STORY-092"

    def test_missing_config_uses_defaults(self):
        """Test: Missing config keys use defaults."""
        # Given: Empty configuration
        empty_config = {}

        # When: Resolving paths
        paths = resolve_story_paths("STORY-092", empty_config)

        # Then: Default paths used
        assert paths["results_dir"] == "tests/results/STORY-092"
        assert paths["coverage_dir"] == "tests/coverage/STORY-092"
        assert paths["logs_dir"] == "tests/logs/STORY-092"

    def test_all_story_ids_in_range(self, default_config):
        """Test: All valid story ID formats work."""
        # Given: Range of story IDs
        story_ids = [
            "STORY-1",      # Single digit
            "STORY-99",     # Two digits
            "STORY-001",    # Leading zeros
            "STORY-9999",   # Max digits
        ]

        # When/Then: All resolve correctly
        for story_id in story_ids:
            paths = resolve_story_paths(story_id, default_config)
            assert story_id in paths["results_dir"]
            assert story_id in paths["coverage_dir"]
            assert story_id in paths["logs_dir"]
