"""
conftest.py for GitHub Actions integration tests using act.

Provides fixtures for:
- act availability detection
- Temporary workflow environments
- Mock secrets injection
- Dry-run vs full execution modes

STORY-097: GitHub Actions Workflow Templates with Headless Claude Code
DoD Item: Integration tests with GitHub Actions
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional

import pytest


# act binary location - installed via nektos/act install script
ACT_BINARY = "/mnt/c/Projects/devforgeai2/bin/act"


@pytest.fixture(scope="session")
def act_binary_path() -> str:
    """Return the path to the act binary."""
    return ACT_BINARY


@pytest.fixture(scope="session")
def act_available() -> bool:
    """Check if act is installed and available."""
    # Try the known installation path first
    paths_to_try = [
        ACT_BINARY,
        "act",  # If in PATH
        "/usr/local/bin/act",
        str(Path.home() / "bin" / "act"),
    ]

    for act_path in paths_to_try:
        try:
            result = subprocess.run(
                [act_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return False


@pytest.fixture(scope="session")
def docker_available() -> bool:
    """Check if Docker is available (required by act)."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@pytest.fixture
def skip_if_act_unavailable(act_available, docker_available):
    """Skip test if act or Docker is not available."""
    if not act_available:
        pytest.skip(
            "act not installed - run: "
            "curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
        )
    if not docker_available:
        pytest.skip("Docker not available - required for act")


@pytest.fixture
def project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def workflows_dir(project_root) -> Path:
    """Return .github/workflows directory."""
    return project_root / ".github" / "workflows"


@pytest.fixture
def act_secrets() -> Dict[str, str]:
    """Mock secrets for act execution."""
    return {
        "ANTHROPIC_API_KEY": "test-mock-api-key-for-dry-run",
    }


@pytest.fixture
def act_env_file(tmp_path, act_secrets) -> Path:
    """Create temporary .secrets file for act."""
    secrets_file = tmp_path / ".secrets"
    with open(secrets_file, "w") as f:
        for key, value in act_secrets.items():
            f.write(f"{key}={value}\n")
    return secrets_file


class ActRunner:
    """Helper class to run act commands."""

    def __init__(
        self,
        project_root: Path,
        secrets_file: Optional[Path] = None,
        act_binary: str = ACT_BINARY
    ):
        self.project_root = project_root
        self.secrets_file = secrets_file
        self.act_binary = act_binary

    def run(
        self,
        workflow: str,
        event: str = "push",
        job: Optional[str] = None,
        inputs: Optional[Dict[str, str]] = None,
        dry_run: bool = True,
        timeout: int = 120
    ) -> subprocess.CompletedProcess:
        """
        Run act with specified parameters.

        Args:
            workflow: Workflow file name (e.g., "dev-story.yml")
            event: GitHub event type (push, pull_request, workflow_dispatch)
            job: Specific job to run (optional)
            inputs: Input parameters for workflow_dispatch
            dry_run: If True, use -n flag for dry-run mode
            timeout: Command timeout in seconds

        Returns:
            CompletedProcess with stdout, stderr, returncode
        """
        cmd = [self.act_binary, event]

        # Specify workflow file
        cmd.extend(["-W", f".github/workflows/{workflow}"])

        # Add secrets file
        if self.secrets_file:
            cmd.extend(["--secret-file", str(self.secrets_file)])

        # Add specific job if provided
        if job:
            cmd.extend(["-j", job])

        # Add inputs for workflow_dispatch
        if inputs:
            for key, value in inputs.items():
                cmd.extend(["--input", f"{key}={value}"])

        # Dry-run mode (no actual execution)
        if dry_run:
            cmd.append("-n")

        # Run from project root
        try:
            return subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired as e:
            # Return a fake CompletedProcess with timeout info
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=-1,
                stdout="",
                stderr=f"Timeout after {timeout}s"
            )


@pytest.fixture
def act_runner(project_root, act_env_file) -> ActRunner:
    """Create ActRunner instance with project configuration."""
    return ActRunner(project_root, act_env_file)


@pytest.fixture
def act_runner_no_secrets(project_root) -> ActRunner:
    """Create ActRunner instance without secrets (for testing missing secret handling)."""
    return ActRunner(project_root, secrets_file=None)
