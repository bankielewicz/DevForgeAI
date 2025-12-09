"""
Shared test fixtures and configuration for uninstall module tests.
All tests will FAIL until implementation is complete (TDD Red phase).
"""
import os
import sys
import json
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from unittest.mock import Mock, MagicMock, patch

import pytest

# Add parent directory to path so 'installer' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def temp_install_dir():
    """Create a temporary installation directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create framework directories
        (tmpdir / ".claude").mkdir()
        (tmpdir / ".claude" / "skills").mkdir(parents=True)
        (tmpdir / ".claude" / "agents").mkdir(parents=True)
        (tmpdir / ".claude" / "commands").mkdir(parents=True)

        (tmpdir / ".devforgeai").mkdir()
        (tmpdir / ".devforgeai" / "context").mkdir(parents=True)
        (tmpdir / ".devforgeai" / "qa").mkdir(parents=True)
        (tmpdir / ".devforgeai" / "adrs").mkdir(parents=True)

        # Create user content directories
        (tmpdir / ".ai_docs").mkdir()
        (tmpdir / ".ai_docs" / "Stories").mkdir(parents=True)
        (tmpdir / ".ai_docs" / "Epics").mkdir(parents=True)
        (tmpdir / ".ai_docs" / "Sprints").mkdir(parents=True)

        # Create CLAUDE.md
        (tmpdir / "CLAUDE.md").write_text("# Claude Config")

        # Create manifest
        manifest = {
            "version": "1.0.0",
            "installed_files": [
                ".claude/skills/test-skill/SKILL.md",
                ".claude/agents/test-agent.md",
                ".devforgeai/context/tech-stack.md",
                "CLAUDE.md"
            ]
        }
        (tmpdir / ".devforgeai" / ".install-manifest.json").write_text(json.dumps(manifest))

        yield tmpdir


@pytest.fixture
def temp_backup_dir():
    """Create a temporary backup directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_manifest_manager():
    """Mock ManifestManager for dependency injection."""
    manager = Mock()
    manager.load_manifest = Mock(return_value={
        "version": "1.0.0",
        "installed_files": [
            ".claude/skills/test-skill/SKILL.md",
            ".claude/agents/test-agent.md",
            ".devforgeai/context/tech-stack.md",
            "CLAUDE.md"
        ]
    })
    manager.save_manifest = Mock()
    return manager


@pytest.fixture
def mock_backup_service():
    """Mock BackupService for dependency injection."""
    service = Mock()
    service.create_backup = Mock(return_value="/backup/path/backup-2025-01-01.tar.gz")
    service.restore_backup = Mock()
    return service


@pytest.fixture
def mock_file_system():
    """Mock file system operations."""
    fs = Mock()
    fs.exists = Mock(return_value=True)
    fs.is_file = Mock(return_value=True)
    fs.is_dir = Mock(return_value=True)
    fs.get_size = Mock(return_value=1024)
    fs.remove_file = Mock()
    fs.remove_dir = Mock()
    fs.list_files = Mock(return_value=[])
    fs.get_file_hash = Mock(return_value="abc123def456")
    return fs


@pytest.fixture
def mock_logger():
    """Mock logger for capturing log output."""
    logger = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


# ============================================================================
# STORY-082: Version-Aware Configuration Management Fixtures
# ============================================================================


@pytest.fixture
def sample_install_config():
    """
    Sample valid installation configuration (STORY-082).

    This config represents a typical user setup with all required fields.
    """
    return {
        "schema_version": 1,
        "target_path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "optional_features": ["cli", "hooks"],
        "installed_at": "2025-11-25T10:30:00Z",
        "last_upgraded_at": None,
    }


@pytest.fixture
def minimal_install_config():
    """Minimal valid configuration with only required fields."""
    return {
        "schema_version": 1,
        "target_path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "optional_features": [],
        "installed_at": "2025-11-25T10:30:00Z",
    }


@pytest.fixture
def config_with_sensitive_data():
    """
    Configuration that includes sensitive data to test filtering.

    Used to verify that export excludes sensitive keys.
    """
    return {
        "schema_version": 1,
        "target_path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "optional_features": ["cli"],
        "installed_at": "2025-11-25T10:30:00Z",
        "api_token": "secret-token-12345",
        "database_password": "super-secret-password",
        "jwt_secret": "jwt-secret-key",
    }


@pytest.fixture
def v1_config():
    """Schema v1 configuration for migration testing."""
    return {
        "schema_version": 1,
        "path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "installed_at": "2025-11-01T10:00:00Z",
    }


@pytest.fixture
def v2_expected_config():
    """Expected v2 configuration after migration from v1."""
    return {
        "schema_version": 2,
        "target_path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "optional_features": [],
        "installed_at": "2025-11-01T10:00:00Z",
        "install_date": "2025-11-01",
    }


@pytest.fixture
def invalid_configs():
    """Collection of invalid configurations for validation testing."""
    return {
        "missing_target_path": {
            "schema_version": 1,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        },
        "missing_merge_strategy": {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        },
        "missing_installed_at": {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
        },
        "invalid_merge_strategy": {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "INVALID_STRATEGY",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        },
        "optional_features_not_array": {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": "cli,hooks",
            "installed_at": "2025-11-25T10:30:00Z",
        },
        "invalid_datetime": {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-13-45T99:99:99Z",
        },
    }


@pytest.fixture
def config_file_path(temp_install_dir):
    """Path to configuration file in test directory."""
    return temp_install_dir / ".devforgeai" / ".install-config.json"


@pytest.fixture
def backup_file_path(temp_install_dir):
    """Path to backup configuration file."""
    return temp_install_dir / ".devforgeai" / ".install-config.backup"


@pytest.fixture
def existing_config_file(config_file_path, sample_install_config):
    """Create an existing configuration file."""
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file_path, "w") as f:
        json.dump(sample_install_config, f)
    return config_file_path


@pytest.fixture
def corrupted_config_file(config_file_path):
    """Create a corrupted (invalid JSON) configuration file."""
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file_path, "w") as f:
        f.write("{ invalid json content }")
    return config_file_path


@pytest.fixture
def empty_config_file(config_file_path):
    """Create an empty configuration file."""
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    config_file_path.touch()
    return config_file_path


@pytest.fixture
def valid_validation_result():
    """Valid ValidationResult with no errors."""
    return {
        "is_valid": True,
        "errors": [],
        "warnings": [],
    }


@pytest.fixture
def invalid_validation_result():
    """Invalid ValidationResult with errors."""
    return {
        "is_valid": False,
        "errors": [
            "Missing required key: target_path",
            "Invalid type for 'optional_features': expected array, got string",
        ],
        "warnings": ["Unknown key 'foo' - will be ignored"],
    }


@pytest.fixture
def migration_result_v1_to_v2():
    """MigrationResult for v1 -> v2 migration."""
    return {
        "from_version": 1,
        "to_version": 2,
        "keys_renamed": {"path": "target_path"},
        "keys_added": ["optional_features", "install_date"],
        "keys_removed": [],
    }


@pytest.fixture
def large_config():
    """Large configuration with many optional features for performance testing."""
    return {
        "schema_version": 1,
        "target_path": "/home/user/project",
        "merge_strategy": "SMART_MERGE",
        "optional_features": [f"feature-{i}" for i in range(100)],
        "installed_at": "2025-11-25T10:30:00Z",
    }


# Configuration constants for validation
VALID_MERGE_STRATEGIES = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
SENSITIVE_KEYS = ["api_token", "database_password", "jwt_secret", "oauth_token"]
REQUIRED_KEYS = ["schema_version", "target_path", "merge_strategy", "installed_at"]
