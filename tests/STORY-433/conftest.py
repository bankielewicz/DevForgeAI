"""
Shared fixtures for STORY-433: Move Epic Analysis References from Ideation to Architecture.

Story: STORY-433
Generated: 2026-02-17
"""

import hashlib
import os
from pathlib import Path

import pytest

# Project root (DevForgeAI2/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Source and target directories (src/ tree per dual-path architecture)
IDEATION_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-ideation" / "references"
ARCHITECTURE_REFS_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-architecture" / "references"

# The 6 files to migrate (5 whole-file + 1 section extraction)
WHOLE_FILE_MIGRATIONS = [
    "epic-decomposition-workflow.md",
    "feasibility-analysis-workflow.md",
    "feasibility-analysis-framework.md",
    "complexity-assessment-workflow.md",
    "complexity-assessment-matrix.md",
]

# artifact-generation.md requires section extraction (BR-003)
SECTION_EXTRACTION_FILE = "artifact-generation.md"

# All 6 files being migrated
ALL_MIGRATED_FILES = WHOLE_FILE_MIGRATIONS + [SECTION_EXTRACTION_FILE]

# Expected line counts per story specification
EXPECTED_LINE_COUNTS = {
    "epic-decomposition-workflow.md": 309,
    "feasibility-analysis-workflow.md": 543,
    "feasibility-analysis-framework.md": 600,  # approximate
    "complexity-assessment-workflow.md": 333,
    "complexity-assessment-matrix.md": 800,  # approximate
    "artifact-generation.md": 350,  # epic sections only, approximate
}

# Epic-related section headers in artifact-generation.md
# These sections should be migrated to architecture
EPIC_SECTION_HEADERS = [
    "## Step 6.1: Generate Epic Document(s)",
    "## Load Constitutional Epic Template",
    "## Integration with Phase 4 Decomposition",
    "## Directory Structure Requirements",
    "## Epic Numbering Convention",
    "## Epic Status Field",
]

# Requirements-related section headers in artifact-generation.md
# These sections should REMAIN in ideation
REQUIREMENTS_SECTION_HEADERS = [
    "## Step 6.2: Generate Requirements Specification (Optional)",
    "## Step 6.3: Transition to Architecture Skill",
    "## Common Issues and Recovery",
    "## Output from Steps 6.1-6.3",
]

# Non-migrated files that must remain in ideation
NON_MIGRATED_FILES = [
    "discovery-workflow.md",
    "requirements-elicitation-workflow.md",
    "requirements-elicitation-guide.md",
    "self-validation-workflow.md",
    "user-interaction-patterns.md",
    "error-handling.md",
    "output-templates.md",
    "validation-checklists.md",
    "domain-specific-patterns.md",
    "completion-handoff.md",
]

# Known STORY-432 files (from EPIC-068 Feature 1)
STORY_432_EXPECTED_FILES = [
    "dependency-graph.md",
    "epic-management.md",
    "epic-validation-checklist.md",
    "epic-validation-hook.md",
    "feature-analyzer.md",
    "feature-decomposition-patterns.md",
]

# Pre-migration count of .md files in ideation references
PRE_MIGRATION_IDEATION_MD_COUNT = 31


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 checksum of a file.

    Args:
        file_path: Path to the file.

    Returns:
        Hex-encoded SHA-256 digest string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_md_files(directory: Path) -> int:
    """Count .md files in a directory (non-recursive).

    Args:
        directory: Path to the directory to count files in.

    Returns:
        Number of .md files found.
    """
    if not directory.exists():
        return 0
    return len([f for f in directory.iterdir() if f.suffix == ".md" and f.is_file()])


# --- Pytest Fixtures ---


@pytest.fixture
def project_root():
    """Return the project root path."""
    return PROJECT_ROOT


@pytest.fixture
def ideation_refs_dir():
    """Return the ideation references directory path."""
    return IDEATION_REFS_DIR


@pytest.fixture
def architecture_refs_dir():
    """Return the architecture references directory path."""
    return ARCHITECTURE_REFS_DIR


@pytest.fixture
def whole_file_migrations():
    """Return list of files that should be copied whole (not section-extracted)."""
    return WHOLE_FILE_MIGRATIONS


@pytest.fixture
def all_migrated_files():
    """Return list of all 6 files being migrated."""
    return ALL_MIGRATED_FILES


@pytest.fixture
def section_extraction_file():
    """Return the filename that requires section extraction."""
    return SECTION_EXTRACTION_FILE
