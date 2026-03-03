"""
Conftest for STORY-442 tests.
Story: STORY-442 - Rename Brainstorming Skill - Drop devforgeai- Prefix
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT
