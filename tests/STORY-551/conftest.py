"""
Shared fixtures for STORY-551: Financial Model Command and Skill Assembly
Story: STORY-551
Generated: 2026-03-05
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Return the project root directory (src/ tree)."""
    return Path(__file__).resolve().parents[2] / "src"


@pytest.fixture
def command_file(project_root):
    """Path to the financial-model command file."""
    return project_root / "claude" / "commands" / "financial-model.md"


@pytest.fixture
def subagent_file(project_root):
    """Path to the financial-modeler subagent file."""
    return project_root / "claude" / "agents" / "financial-modeler.md"


@pytest.fixture
def skill_file(project_root):
    """Path to the managing-finances SKILL.md file."""
    return project_root / "claude" / "skills" / "managing-finances" / "SKILL.md"


@pytest.fixture
def command_content(command_file):
    """Read and return command file content. Fails if file does not exist."""
    assert command_file.exists(), f"Command file does not exist: {command_file}"
    return command_file.read_text(encoding="utf-8")


@pytest.fixture
def subagent_content(subagent_file):
    """Read and return subagent file content. Fails if file does not exist."""
    assert subagent_file.exists(), f"Subagent file does not exist: {subagent_file}"
    return subagent_file.read_text(encoding="utf-8")


@pytest.fixture
def skill_content(skill_file):
    """Read and return skill file content. Fails if file does not exist."""
    assert skill_file.exists(), f"Skill file does not exist: {skill_file}"
    return skill_file.read_text(encoding="utf-8")


@pytest.fixture
def command_lines(command_content):
    """Return command file as list of lines."""
    return command_content.splitlines()


@pytest.fixture
def subagent_lines(subagent_content):
    """Return subagent file as list of lines."""
    return subagent_content.splitlines()


@pytest.fixture
def skill_lines(skill_content):
    """Return skill file as list of lines."""
    return skill_content.splitlines()
