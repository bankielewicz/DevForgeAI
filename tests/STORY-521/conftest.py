"""
Shared fixtures for STORY-521 tests.
Story: STORY-521 - Unify Dev and QA Phase Tracking Under Single CLI Interface
"""

import json
import pytest
from pathlib import Path


@pytest.fixture
def project_root(tmp_path):
    """Create an isolated project root with workflows directory."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True)
    return str(tmp_path)


@pytest.fixture
def phase_state(project_root):
    """Create a PhaseState instance with isolated project root."""
    from devforgeai_cli.phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
