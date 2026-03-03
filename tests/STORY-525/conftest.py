"""
Shared fixtures for STORY-525 tests.
Story: STORY-525 - Phase Steps Registry + Step-Level Tracking
Generated: 2026-03-02
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src tree to path for imports
SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "claude" / "scripts"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from devforgeai_cli.phase_state import PhaseState


@pytest.fixture
def project_root(tmp_path):
    """Create a temporary project root with workflows directory."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def phase_state(project_root):
    """Create a PhaseState instance with temporary project root."""
    return PhaseState(project_root=project_root)


@pytest.fixture
def initialized_state(phase_state):
    """Create and return a PhaseState with STORY-525 initialized."""
    phase_state.create("STORY-525")
    return phase_state


@pytest.fixture
def sample_registry():
    """Return a minimal valid registry for testing."""
    return {
        "02": {
            "name": "Test-First (Red)",
            "entry_gate": "devforgeai-validate phase-check STORY-XXX --from=01 --to=02",
            "exit_gate": "devforgeai-validate phase-complete STORY-XXX --phase=02 --checkpoint-passed",
            "steps": [
                {"id": "02.1", "check": "test-automator subagent invoked", "subagent": "test-automator", "conditional": False},
                {"id": "02.2", "check": "Failing tests written for all ACs", "subagent": "test-automator", "conditional": False},
                {"id": "02.3", "check": "Test integrity snapshot captured", "subagent": None, "conditional": False},
                {"id": "02.4", "check": "Optional pre-phase planning", "subagent": None, "conditional": True},
            ]
        }
    }


@pytest.fixture
def registry_path(project_root):
    """Return the expected registry file path in src tree."""
    reg_dir = project_root / ".claude" / "hooks"
    reg_dir.mkdir(parents=True)
    return reg_dir / "phase-steps-registry.json"


@pytest.fixture
def registry_with_file(registry_path, sample_registry):
    """Write sample registry to disk and return path."""
    registry_path.write_text(json.dumps(sample_registry, indent=2))
    return registry_path
