"""
Shared fixtures for STORY-403: Create Dead-Code-Detector Subagent.

Provides common paths and file reading utilities for all AC test files.
"""
import os
import pytest


# Project root (DevForgeAI2/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Source files under test (to be created in Phase 03)
SUBAGENT_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "agents", "dead-code-detector.md"
)
ENTRY_POINT_PATTERNS_FILE = os.path.join(
    PROJECT_ROOT,
    "src",
    "claude",
    "agents",
    "dead-code-detector",
    "references",
    "entry-point-patterns.md",
)
ADR_016_FILE = os.path.join(
    PROJECT_ROOT,
    "devforgeai",
    "specs",
    "adrs",
    "ADR-016-dead-code-detector-read-only.md",
)
CLAUDE_MD_FILE = os.path.join(PROJECT_ROOT, "src", "CLAUDE.md")


@pytest.fixture
def subagent_content():
    """Read the dead-code-detector subagent definition file.

    This fixture will FAIL if the file does not exist yet (TDD Red phase).
    """
    assert os.path.exists(SUBAGENT_FILE), (
        f"Subagent file not found: {SUBAGENT_FILE}. "
        "This file must be created in Phase 03 (Implementation)."
    )
    with open(SUBAGENT_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def entry_point_patterns_content():
    """Read the entry-point-patterns reference file.

    This fixture will FAIL if the file does not exist yet (TDD Red phase).
    """
    assert os.path.exists(ENTRY_POINT_PATTERNS_FILE), (
        f"Entry point patterns file not found: {ENTRY_POINT_PATTERNS_FILE}. "
        "This file must be created in Phase 03 (Implementation)."
    )
    with open(ENTRY_POINT_PATTERNS_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def adr_016_content():
    """Read the ADR-016 document.

    This fixture will FAIL if the file does not exist yet (TDD Red phase).
    """
    assert os.path.exists(ADR_016_FILE), (
        f"ADR-016 file not found: {ADR_016_FILE}. "
        "This file must be created in Phase 03 (Implementation)."
    )
    with open(ADR_016_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def claude_md_content():
    """Read the src/CLAUDE.md file for registry validation.

    This fixture will FAIL if the registry entry is not present (TDD Red phase).
    """
    assert os.path.exists(CLAUDE_MD_FILE), (
        f"CLAUDE.md file not found: {CLAUDE_MD_FILE}."
    )
    with open(CLAUDE_MD_FILE, "r", encoding="utf-8") as f:
        return f.read()
