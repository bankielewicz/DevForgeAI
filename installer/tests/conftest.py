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
