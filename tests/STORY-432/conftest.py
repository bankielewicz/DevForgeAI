"""
Shared fixtures for STORY-432: Move Epic Creation References from Orchestration to Architecture.

Provides common constants and path configurations used across all AC test files.
"""
import os
import pytest

# Project root (two levels up from tests/STORY-432/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Source paths (orchestration - files should be REMOVED after migration)
ORCHESTRATION_REFERENCES_DIR = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration", "references"
)
ORCHESTRATION_TEMPLATES_DIR = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-orchestration", "assets", "templates"
)

# Target paths (architecture - files should EXIST after migration)
ARCHITECTURE_REFERENCES_DIR = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references"
)
ARCHITECTURE_TEMPLATES_DIR = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "assets", "templates"
)

# The 7 reference files to migrate
REFERENCE_FILES = [
    "epic-management.md",
    "feature-decomposition-patterns.md",
    "feature-analyzer.md",
    "dependency-graph.md",
    "technical-assessment-guide.md",
    "epic-validation-checklist.md",
    "epic-validation-hook.md",
]

# The 1 template file to migrate
TEMPLATE_FILE = "epic-template.md"

# All 8 files combined (7 references + 1 template)
ALL_MIGRATED_FILES = REFERENCE_FILES + [TEMPLATE_FILE]


@pytest.fixture
def project_root():
    """Return the absolute path to the project root."""
    return PROJECT_ROOT


@pytest.fixture
def orchestration_references_dir():
    """Return the orchestration references directory path."""
    return ORCHESTRATION_REFERENCES_DIR


@pytest.fixture
def orchestration_templates_dir():
    """Return the orchestration templates directory path."""
    return ORCHESTRATION_TEMPLATES_DIR


@pytest.fixture
def architecture_references_dir():
    """Return the architecture references directory path."""
    return ARCHITECTURE_REFERENCES_DIR


@pytest.fixture
def architecture_templates_dir():
    """Return the architecture templates directory path."""
    return ARCHITECTURE_TEMPLATES_DIR


@pytest.fixture
def reference_files():
    """Return the list of 7 reference files to migrate."""
    return REFERENCE_FILES


@pytest.fixture
def template_file():
    """Return the template file name to migrate."""
    return TEMPLATE_FILE


@pytest.fixture
def all_migrated_files():
    """Return all 8 files to migrate (7 references + 1 template)."""
    return ALL_MIGRATED_FILES
