"""STORY-441: Rename devforgeai-ideation to discovering-requirements.

Shared fixtures and constants for all AC tests.
"""
import os

import pytest

# Project root (two levels up from tests/STORY-441/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Key paths
SRC_NEW = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "discovering-requirements")
SRC_OLD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation")
OPS_NEW = os.path.join(PROJECT_ROOT, ".claude", "skills", "discovering-requirements")
OPS_OLD = os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-ideation")
