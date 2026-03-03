"""STORY-443: Update Context Files and Codebase Sweep.

Shared fixtures and constants for all AC tests.
All tests validate that constitutional context files have been updated
to reflect new skill names per ADR-017 gerund naming convention.
"""
import os

import pytest

# Project root (two levels up from tests/STORY-443/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Context file paths (canonical versions)
SOURCE_TREE_MD = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md")
ARCH_CONSTRAINTS_MD = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "architecture-constraints.md")
CODING_STANDARDS_MD = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "coding-standards.md")

# Memory file paths — both src/ (source of truth) and .claude/ (operational)
SRC_SKILLS_REF = os.path.join(PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md")
OPS_SKILLS_REF = os.path.join(PROJECT_ROOT, ".claude", "memory", "skills-reference.md")

# Root CLAUDE.md
CLAUDE_MD = os.path.join(PROJECT_ROOT, "CLAUDE.md")

# Sweep report
SWEEP_REPORT = os.path.join(PROJECT_ROOT, "devforgeai", "reports", "STORY-443-sweep-report.md")

# Old skill names that must NOT appear in active (non-historical) files
OLD_SKILL_NAMES = [
    "devforgeai-brainstorming",
    "devforgeai-ideation",
    "devforgeai-development",
]

# New skill names that MUST appear in updated files
NEW_SKILL_NAMES = [
    "brainstorming",
    "discovering-requirements",
    "implementing-stories",
    "designing-systems",
]

# Historical/archive directories excluded from the active sweep
HISTORICAL_DIRS = [
    "devforgeai/feedback",
    "devforgeai/RCA",
    "devforgeai/specs/Stories",
    "devforgeai/specs/Epics",
    "devforgeai/specs/brainstorms",
    "devforgeai/specs/adrs",
    ".backup",
    "/backup/",
    ".deprecated",
    "MIGRATION-NOTES",
    "tests/STORY-443",
]

# Active directories that MUST have zero stale references
ACTIVE_DIRS = [
    os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context"),
    os.path.join(PROJECT_ROOT, ".claude", "skills"),
    os.path.join(PROJECT_ROOT, ".claude", "commands"),
    os.path.join(PROJECT_ROOT, ".claude", "memory"),
    os.path.join(PROJECT_ROOT, "src", "claude"),
]
