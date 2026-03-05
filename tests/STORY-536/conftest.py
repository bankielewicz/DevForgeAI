"""Shared fixtures for STORY-536 tests."""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture
def project_root():
    return PROJECT_ROOT


@pytest.fixture
def subagent_path(project_root):
    return os.path.join(project_root, "src", "claude", "agents", "market-analyst.md")


@pytest.fixture
def output_path(project_root):
    return os.path.join(
        project_root, "devforgeai", "specs", "business", "market-research", "competitive-analysis.md"
    )


@pytest.fixture
def skill_path(project_root):
    return os.path.join(project_root, "src", "claude", "skills", "researching-market", "SKILL.md")


@pytest.fixture
def subagent_content(subagent_path):
    """Read subagent file content. Returns empty string if file missing."""
    if os.path.exists(subagent_path):
        with open(subagent_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


@pytest.fixture
def output_content(output_path):
    """Read output file content. Returns empty string if file missing."""
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


@pytest.fixture
def skill_content(skill_path):
    """Read skill file content. Returns empty string if file missing."""
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
