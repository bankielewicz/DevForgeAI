"""
Shared fixtures for STORY-356 audit tests.

Provides common path constants and the command-to-skill mapping
for auditing Skill(command="...") invocation patterns in command files.
"""
from pathlib import Path
from typing import Dict

import pytest


# ---------------------------------------------------------------------------
# Project root & source-tree path constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/mnt/c/Projects/DevForgeAI2")
SRC_COMMANDS_DIR = PROJECT_ROOT / "src" / "claude" / "commands"

# Mapping of command name -> expected skill invocation pattern
COMMAND_SKILL_MAP: Dict[str, str] = {
    "ideate": "devforgeai-ideation",
    "create-context": "devforgeai-architecture",
    "create-epic": "devforgeai-orchestration",
    "brainstorm": "devforgeai-brainstorming",
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def project_root() -> Path:
    """Return the absolute project root path."""
    return PROJECT_ROOT


@pytest.fixture
def src_commands_dir() -> Path:
    """Return the src/claude/commands/ directory path."""
    return SRC_COMMANDS_DIR


@pytest.fixture
def command_skill_map() -> Dict[str, str]:
    """Return the command-to-skill mapping dictionary."""
    return COMMAND_SKILL_MAP
