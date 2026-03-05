"""
Shared fixtures for STORY-540: Positioning & Messaging Framework tests.
"""
import os
import pytest

# Project root (two levels up from tests/STORY-540/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Source file under test
POSITIONING_STRATEGY_FILE = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "marketing-business", "references",
    "positioning-strategy.md",
)

# Output file path documented in the story
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "devforgeai", "specs", "business", "marketing", "positioning.md",
)


@pytest.fixture
def strategy_path():
    """Return the absolute path to the positioning-strategy.md source file."""
    return POSITIONING_STRATEGY_FILE


@pytest.fixture
def strategy_content(strategy_path):
    """Read and return the full text of positioning-strategy.md.

    This fixture will FAIL if the file does not exist (TDD Red).
    """
    assert os.path.isfile(strategy_path), (
        f"Implementation file does not exist yet: {strategy_path}"
    )
    with open(strategy_path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def strategy_lines(strategy_content):
    """Return positioning-strategy.md content as a list of lines."""
    return strategy_content.splitlines()


@pytest.fixture
def output_path():
    """Return the absolute path to the generated positioning.md output file."""
    return OUTPUT_FILE
