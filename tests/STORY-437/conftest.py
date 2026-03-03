"""Shared fixtures for STORY-437 tests."""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SKILL_MD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration", "SKILL.md")
MODE_DETECTION_MD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration", "references", "mode-detection.md")
SUBAGENT_REGISTRY_MD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration", "references", "subagent-registry.md")
ORCHESTRATION_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration")


@pytest.fixture
def skill_md_content():
    """Read SKILL.md content."""
    with open(SKILL_MD, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def mode_detection_content():
    """Read mode-detection.md content."""
    with open(MODE_DETECTION_MD, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def subagent_registry_content():
    """Read subagent-registry.md content."""
    with open(SUBAGENT_REGISTRY_MD, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def all_orchestration_files():
    """Read all markdown files in orchestration directory."""
    contents = {}
    for root, _dirs, files in os.walk(ORCHESTRATION_DIR):
        for fname in files:
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    contents[fpath] = f.read()
    return contents
