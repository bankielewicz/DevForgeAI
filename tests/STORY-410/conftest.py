"""
Shared fixtures for STORY-410 audit command tests.
Story: STORY-410 - Create Automated Audit for Command/Skill Hybrid Violations
"""
import os
import subprocess
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT_PATH = os.path.join(PROJECT_ROOT, ".claude", "scripts", "audit-command-skill-overlap.sh")
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def script_path():
    """Path to the audit script under test."""
    return SCRIPT_PATH


@pytest.fixture
def fixtures_dir():
    """Path to test fixture command files."""
    return FIXTURES_DIR


@pytest.fixture
def run_audit(script_path):
    """Run the audit script against a custom commands directory.

    Returns a callable that accepts a directory path and returns CompletedProcess.
    """
    def _run(commands_dir, timeout=10):
        env = os.environ.copy()
        env["COMMANDS_DIR"] = commands_dir
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(script_path),
            env=env,
        )
        return result

    return _run
