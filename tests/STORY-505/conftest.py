"""
Shared fixtures for STORY-505 operational safety rules tests.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

OPERATIONAL_SAFETY_PATH = os.path.join(
    PROJECT_ROOT, ".claude", "rules", "workflow", "operational-safety.md"
)
GITIGNORE_PATH = os.path.join(PROJECT_ROOT, ".gitignore")
RULES_README_PATH = os.path.join(PROJECT_ROOT, ".claude", "rules", "README.md")
ANTI_PATTERNS_PATH = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "context", "anti-patterns.md"
)
CRITICAL_RULES_PATH = os.path.join(
    PROJECT_ROOT, ".claude", "rules", "core", "critical-rules.md"
)


@pytest.fixture
def rule_file_content():
    """Read the operational-safety.md file content."""
    with open(OPERATIONAL_SAFETY_PATH, "r") as f:
        return f.read()


@pytest.fixture
def rule_file_lines(rule_file_content):
    """Return lines of the operational-safety.md file."""
    return rule_file_content.splitlines()


@pytest.fixture
def gitignore_content():
    """Read the .gitignore file content."""
    with open(GITIGNORE_PATH, "r") as f:
        return f.read()


@pytest.fixture
def rules_readme_content():
    """Read the Rules README content."""
    with open(RULES_README_PATH, "r") as f:
        return f.read()
