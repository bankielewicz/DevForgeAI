"""
Shared test fixtures and configuration for STORY-045 test suite.

This module provides common test fixtures (mocked file systems, version.json data,
directory structures) used across all test modules to ensure consistency and reduce
duplication.

Fixtures:
- tmp_project: Temporary project directory structure
- version_data: Sample version.json data
- backup_manifest: Sample backup manifest
- mock_source_files: Mock source file structure
"""

import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone


@pytest.fixture
def tmp_project(tmp_path):
    """
    Create a temporary project directory with DevForgeAI framework installed.

    Returns:
        dict: Contains 'root' (project root), 'claude' (.claude/), 'devforgeai' (.devforgeai/)
    """
    root = tmp_path / "test_project"
    root.mkdir()

    # Create .claude/ structure
    claude_dir = root / ".claude"
    claude_dir.mkdir()
    (claude_dir / "agents").mkdir()
    (claude_dir / "commands").mkdir()
    (claude_dir / "memory").mkdir()
    (claude_dir / "scripts").mkdir()
    (claude_dir / "skills").mkdir()

    # Create .devforgeai/ structure
    devforgeai_dir = root / ".devforgeai"
    devforgeai_dir.mkdir()
    (devforgeai_dir / "config").mkdir()
    (devforgeai_dir / "context").mkdir()
    (devforgeai_dir / "protocols").mkdir()
    (devforgeai_dir / "specs").mkdir()
    (devforgeai_dir / "qa").mkdir()
    (devforgeai_dir / "adrs").mkdir()

    # Create backup directory (for tests that check backup paths)
    backups_dir = root / ".backups"
    backups_dir.mkdir()

    return {
        "root": root,
        "claude": claude_dir,
        "devforgeai": devforgeai_dir,
        "backups": backups_dir,
    }


@pytest.fixture
def installed_version_1_0_0(tmp_project):
    """
    Create version.json for an installed version 1.0.0 in test project.

    Returns:
        dict: Version metadata for 1.0.0
    """
    version_data = {
        "version": "1.0.0",
        "installed_at": "2025-11-15T10:00:00Z",
        "mode": "fresh_install",
        "schema_version": "1.0",
    }

    version_file = tmp_project["devforgeai"] / ".version.json"
    version_file.write_text(json.dumps(version_data, indent=2))

    return version_data


@pytest.fixture
def source_version_1_0_1():
    """
    Create source version 1.0.1 data (would come from src/devforgeai/version.json).

    Returns:
        dict: Version metadata for 1.0.1 (source)
    """
    return {
        "version": "1.0.1",
        "released_at": "2025-11-17T12:00:00Z",
        "schema_version": "1.0",
        "changes": ["Bug fix 1", "Bug fix 2"],
    }


@pytest.fixture
def backup_manifest():
    """
    Create a sample backup manifest (manifest.json from backup directory).

    Returns:
        dict: Complete backup manifest with integrity data
    """
    return {
        "created_at": "2025-11-17T14:30:00Z",
        "reason": "upgrade",
        "from_version": "1.0.0",
        "to_version": "1.0.1",
        "files_backed_up": 450,
        "total_size_mb": 15.2,
        "backup_integrity_hash": "sha256:abcdef123456789abcdef123456789abcdef123456789abcdef123456789ab",
    }


@pytest.fixture
def mock_source_files(tmp_path):
    """
    Create mock source file structure (simulating src/ directory).

    Creates:
    - src/claude/ with 370 mock files
    - src/devforgeai/ with 80 mock files
    - src/devforgeai/version.json with v1.0.1

    Returns:
        dict: Paths to source structure {'root', 'claude', 'devforgeai', 'version_file'}
    """
    src_root = tmp_path / "mock_src"
    src_root.mkdir()

    # Create src/claude structure
    src_claude = src_root / "claude"
    src_claude.mkdir()
    (src_claude / "agents").mkdir()
    (src_claude / "commands").mkdir()
    (src_claude / "memory").mkdir()
    (src_claude / "scripts").mkdir()
    (src_claude / "skills").mkdir()

    # Create mock files in src/claude
    for i in range(370):
        subdir = src_claude / ["agents", "commands", "memory", "skills"][i % 4]
        (subdir / f"file_{i:03d}.md").write_text(f"Mock file {i}")

    # Create src/devforgeai structure
    src_devforgeai = src_root / "devforgeai"
    src_devforgeai.mkdir()
    (src_devforgeai / "config").mkdir()
    (src_devforgeai / "protocols").mkdir()
    (src_devforgeai / "specs").mkdir()
    (src_devforgeai / "tests").mkdir()

    # Create mock files in src/devforgeai
    for i in range(80):
        subdir = src_devforgeai / ["config", "protocols", "specs", "tests"][i % 4]
        (subdir / f"spec_{i:03d}.md").write_text(f"Mock spec {i}")

    # Create version.json
    version_file = src_devforgeai / "version.json"
    version_file.write_text(
        json.dumps(
            {
                "version": "1.0.1",
                "released_at": "2025-11-17T12:00:00Z",
                "schema_version": "1.0",
            },
            indent=2,
        )
    )

    return {
        "root": src_root,
        "claude": src_claude,
        "devforgeai": src_devforgeai,
        "version_file": version_file,
    }


@pytest.fixture
def mock_user_config(tmp_project):
    """
    Create user configuration files that should be preserved during upgrade.

    Returns:
        dict: Paths to user config files
    """
    hooks_file = tmp_project["devforgeai"] / "config" / "hooks.yaml"
    hooks_file.write_text("# User custom hooks\ncustom_hook: value\n")

    feedback_file = tmp_project["devforgeai"] / "feedback" / "config.yaml"
    (tmp_project["devforgeai"] / "feedback").mkdir(exist_ok=True)
    feedback_file.write_text("# User feedback config\nfeedback_enabled: true\n")

    context_file = tmp_project["devforgeai"] / "context" / "tech-stack.md"
    context_file.write_text("# User tech stack\n- Python 3.8+\n- pytest\n")

    return {
        "hooks": hooks_file,
        "feedback": feedback_file,
        "context": context_file,
    }


@pytest.fixture
def fixed_timestamp():
    """
    Provide a fixed timestamp for deterministic testing (no random time).

    Returns:
        str: ISO format timestamp "2025-11-17T14:30:00Z"
    """
    return "2025-11-17T14:30:00Z"


@pytest.fixture
def mock_datetime(fixed_timestamp):
    """
    Mock datetime.datetime.now() to return fixed timestamp for deterministic tests.

    Yields:
        MagicMock: Patched datetime that returns fixed time
    """
    fixed_dt = datetime.fromisoformat(fixed_timestamp.replace("Z", "+00:00"))

    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_dt
        mock_dt.utcnow.return_value = fixed_dt
        mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        yield mock_dt


@pytest.fixture
def installation_states():
    """
    Provide different installation states for testing mode detection.

    Returns:
        dict: Installation state configurations for different scenarios
    """
    return {
        "fresh": {
            "has_version_file": False,
            "has_claude_dir": False,
            "has_devforgeai_dir": False,
        },
        "existing_1_0_0": {
            "has_version_file": True,
            "version": "1.0.0",
            "has_claude_dir": True,
            "has_devforgeai_dir": True,
        },
        "existing_1_0_1": {
            "has_version_file": True,
            "version": "1.0.1",
            "has_claude_dir": True,
            "has_devforgeai_dir": True,
        },
        "corrupted": {
            "has_version_file": False,  # Missing version.json
            "has_claude_dir": True,  # But .claude/ exists
            "has_devforgeai_dir": True,  # And .devforgeai/ exists
        },
    }


@pytest.fixture
def error_scenarios():
    """
    Provide error scenarios for error handling testing.

    Returns:
        dict: Error configuration and expected responses
    """
    return {
        "permission_denied": {
            "error": PermissionError("Permission denied: .claude/commands/"),
            "message": "Permission denied writing to .claude/commands/",
        },
        "disk_full": {
            "error": OSError("[Errno 28] No space left on device"),
            "message": "Insufficient disk space for deployment",
        },
        "corrupted_backup": {
            "error": ValueError("Backup manifest validation failed"),
            "message": "Backup integrity check failed",
        },
        "network_timeout": {
            "error": TimeoutError("Network timeout during pip install"),
            "message": "CLI installation failed (network timeout)",
        },
        "invalid_version": {
            "error": ValueError("Invalid version format"),
            "message": "Invalid version in source",
        },
    }
