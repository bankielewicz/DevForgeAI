"""
Shared pytest fixtures for STORY-251: Maintenance Operations tests.

This module provides reusable fixtures for testing maintenance operations:
- Project directory setup with DevForgeAI installation
- Backup directory with sample backups
- Corrupted installation scenarios
- Mock version API responses
- User story files for preservation tests
"""

import pytest
import tempfile
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch


@pytest.fixture
def clean_temp_dir():
    """Create a clean temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def devforgeai_installation(clean_temp_dir):
    """
    Create a complete DevForgeAI installation for testing.

    Structure:
    - .claude/skills/devforgeai-development/SKILL.md
    - .claude/agents/test-automator.md
    - .claude/commands/dev.md
    - devforgeai/specs/context/tech-stack.md
    - devforgeai/specs/Stories/
    - CLAUDE.md
    - .devforgeai_installed
    """
    tmpdir = clean_temp_dir

    # Create .claude/ directory structure
    claude_dir = tmpdir / ".claude"
    (claude_dir / "skills" / "devforgeai-development").mkdir(parents=True)
    (claude_dir / "agents").mkdir(parents=True)
    (claude_dir / "commands").mkdir(parents=True)
    (claude_dir / "memory").mkdir(parents=True)

    # Create skill files
    skill_file = claude_dir / "skills" / "devforgeai-development" / "SKILL.md"
    skill_file.write_text("""# DevForgeAI Development Skill

Version: 1.0.0

TDD workflow implementation for feature development.
""")

    # Create agent file
    agent_file = claude_dir / "agents" / "test-automator.md"
    agent_file.write_text("""---
name: test-automator
description: Generates tests from acceptance criteria
---

# Test Automator Agent
""")

    # Create command file
    command_file = claude_dir / "commands" / "dev.md"
    command_file.write_text("""---
description: Run development workflow
argument-hint: STORY-ID
---

# /dev Command
""")

    # Create devforgeai/ directory structure
    devforgeai_dir = tmpdir / "devforgeai"
    (devforgeai_dir / "specs" / "context").mkdir(parents=True)
    (devforgeai_dir / "specs" / "Stories").mkdir(parents=True)
    (devforgeai_dir / "specs" / "adrs").mkdir(parents=True)
    (devforgeai_dir / "qa").mkdir(parents=True)

    # Create context files
    tech_stack = devforgeai_dir / "specs" / "context" / "tech-stack.md"
    tech_stack.write_text("""# Tech Stack

- Python 3.10+
- pytest
- Claude Code Terminal
""")

    source_tree = devforgeai_dir / "specs" / "context" / "source-tree.md"
    source_tree.write_text("""# Source Tree

Standard DevForgeAI directory structure.
""")

    # Create CLAUDE.md
    claude_md = tmpdir / "CLAUDE.md"
    claude_md.write_text("""# CLAUDE.md

Project instructions for Claude Code Terminal.
""")

    # Create .devforgeai_installed marker
    marker = tmpdir / ".devforgeai_installed"
    marker_data = {
        "version": "1.0.0",
        "installed_at": "2025-01-06T12:00:00Z",
        "updated_at": "2025-01-06T12:00:00Z",
        "components": {
            "core": "1.0.0",
            "cli": "1.0.0",
            "templates": "1.0.0",
            "examples": "1.0.0"
        },
        "installation_id": "test-installation-001",
        "checksums": {}
    }

    # Calculate checksums for all files
    for file_path in tmpdir.rglob("*"):
        if file_path.is_file() and file_path.name != ".devforgeai_installed":
            import hashlib
            content = file_path.read_bytes()
            checksum = hashlib.sha256(content).hexdigest()
            rel_path = str(file_path.relative_to(tmpdir))
            marker_data["checksums"][rel_path] = f"sha256:{checksum}"

    marker.write_text(json.dumps(marker_data, indent=2))

    yield tmpdir


@pytest.fixture
def installation_with_backups(devforgeai_installation):
    """
    Create installation with multiple backup versions.

    Creates backups at:
    - {parent}/.backup-20250105-143000 (v0.9.0)
    - {parent}/.backup-20250101-101500 (v0.8.5)
    - {parent}/.backup-20241215-093000 (v0.8.0, old)
    """
    install_dir = devforgeai_installation
    parent_dir = install_dir.parent

    # Create backups directory within .backups/
    backups_dir = install_dir / ".backups"
    backups_dir.mkdir(exist_ok=True)

    # Backup 1: v0.9.0 from 2025-01-05
    backup1 = backups_dir / "v0.9.0-20250105-143000"
    backup1.mkdir(parents=True)
    (backup1 / ".claude" / "skills" / "devforgeai-development").mkdir(parents=True)
    (backup1 / ".claude" / "skills" / "devforgeai-development" / "SKILL.md").write_text(
        "# DevForgeAI Development Skill\n\nVersion: 0.9.0"
    )
    (backup1 / "manifest.json").write_text(json.dumps({
        "created_at": "2025-01-05T14:30:00Z",
        "reason": "upgrade",
        "from_version": "0.9.0",
        "to_version": "1.0.0"
    }))

    # Backup 2: v0.8.5 from 2025-01-01
    backup2 = backups_dir / "v0.8.5-20250101-101500"
    backup2.mkdir(parents=True)
    (backup2 / ".claude").mkdir(parents=True)
    (backup2 / "manifest.json").write_text(json.dumps({
        "created_at": "2025-01-01T10:15:00Z",
        "reason": "upgrade",
        "from_version": "0.8.5",
        "to_version": "0.9.0"
    }))

    # Backup 3: v0.8.0 from 2024-12-15 (old, for cleanup tests)
    backup3 = backups_dir / "v0.8.0-20241215-093000"
    backup3.mkdir(parents=True)
    (backup3 / ".claude").mkdir(parents=True)
    (backup3 / "manifest.json").write_text(json.dumps({
        "created_at": "2024-12-15T09:30:00Z",
        "reason": "upgrade",
        "from_version": "0.8.0",
        "to_version": "0.8.5"
    }))

    yield install_dir


@pytest.fixture
def corrupted_installation(devforgeai_installation):
    """
    Create an installation with corrupted/missing files.

    Modifications:
    - Delete SKILL.md (missing file)
    - Corrupt tech-stack.md (checksum mismatch)
    """
    install_dir = devforgeai_installation

    # Delete a required file
    skill_file = install_dir / ".claude" / "skills" / "devforgeai-development" / "SKILL.md"
    if skill_file.exists():
        skill_file.unlink()

    # Corrupt a file (change content)
    tech_stack = install_dir / "devforgeai" / "specs" / "context" / "tech-stack.md"
    tech_stack.write_text("# CORRUPTED FILE\n\nThis content does not match the checksum.")

    yield install_dir


@pytest.fixture
def installation_with_user_files(devforgeai_installation):
    """
    Create installation with user-generated files that should be preserved.

    User files:
    - devforgeai/specs/Stories/STORY-001-user-feature.story.md
    - devforgeai/specs/Stories/STORY-002-another-feature.story.md
    - .claude/custom-config.yaml
    - .claude/settings.user.yaml
    """
    install_dir = devforgeai_installation

    # Create user stories
    stories_dir = install_dir / "devforgeai" / "specs" / "Stories"
    (stories_dir / "STORY-001-user-feature.story.md").write_text("""---
id: STORY-001
title: User Feature
type: feature
status: In Development
---

# STORY-001: User Feature

## User Story

As a user, I want this feature.
""")

    (stories_dir / "STORY-002-another-feature.story.md").write_text("""---
id: STORY-002
title: Another Feature
type: feature
status: Backlog
---

# STORY-002: Another Feature

## User Story

As a user, I want another feature.
""")

    # Create custom configuration
    claude_dir = install_dir / ".claude"
    (claude_dir / "custom-config.yaml").write_text("""# Custom user configuration
custom_setting: true
user_preferences:
  theme: dark
  editor: vim
""")

    (claude_dir / "settings.user.yaml").write_text("""# User-specific settings
notification_level: verbose
auto_commit: false
""")

    yield install_dir


@pytest.fixture
def mock_latest_version():
    """Mock the version API to return a newer version."""
    with patch('installer.upgrade.get_latest_version') as mock:
        mock.return_value = {
            "version": "1.1.0",
            "release_date": "2025-01-07",
            "download_url": "https://github.com/devforgeai/releases/v1.1.0.tar.gz",
            "checksum": "sha256:abc123def456789",
            "changelog": "- New features\n- Bug fixes"
        }
        yield mock


@pytest.fixture
def mock_same_version():
    """Mock the version API to return the same version (no update)."""
    with patch('installer.upgrade.get_latest_version') as mock:
        mock.return_value = {
            "version": "1.0.0",
            "release_date": "2025-01-06",
            "download_url": "https://github.com/devforgeai/releases/v1.0.0.tar.gz",
            "checksum": "sha256:xyz789"
        }
        yield mock


@pytest.fixture
def mock_offline_mode():
    """Mock network unavailability for offline mode tests."""
    with patch('installer.network.is_online') as mock:
        mock.return_value = False
        yield mock
