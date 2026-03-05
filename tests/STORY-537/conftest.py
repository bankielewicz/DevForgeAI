"""Shared fixtures for STORY-537 tests."""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SKILL_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "researching-market", "SKILL.md"
)
REFERENCE_FILE = os.path.join(
    PROJECT_ROOT,
    "src",
    "claude",
    "skills",
    "researching-market",
    "references",
    "customer-interview-guide.md",
)
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "devforgeai",
    "specs",
    "business",
    "market-research",
    "customer-interviews.md",
)


@pytest.fixture
def skill_content():
    """Read SKILL.md content. Fails if file missing or lacks interview phase."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found at {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def reference_content():
    """Read customer-interview-guide.md content."""
    assert os.path.isfile(REFERENCE_FILE), f"Reference file not found at {REFERENCE_FILE}"
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def output_content():
    """Read customer-interviews.md output content."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        return f.read()
