"""
STORY-175: Pytest fixtures and configuration.

Shared fixtures for regression classification tests.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def sample_violations():
    """Sample violations for testing."""
    return [
        {
            "file": "src/module/file1.py",
            "line": 10,
            "column": 5,
            "message": "Cyclomatic complexity too high",
            "severity": "HIGH",
            "rule": "complexity-check"
        },
        {
            "file": "src/module/file2.py",
            "line": 25,
            "column": 1,
            "message": "Missing docstring",
            "severity": "MEDIUM",
            "rule": "docstring-check"
        },
        {
            "file": "src/legacy/old_code.py",
            "line": 100,
            "column": 20,
            "message": "Deprecated function usage",
            "severity": "LOW",
            "rule": "deprecation-check"
        },
    ]


@pytest.fixture
def changed_files():
    """Sample list of changed files."""
    return [
        "src/module/file1.py",
        "src/module/new_file.py",
        "tests/test_file1.py",
    ]


@pytest.fixture
def mock_git_diff():
    """Mock for git diff subprocess call."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="src/module/file1.py\nsrc/module/new_file.py\n",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def mock_git_not_available():
    """Mock for when git is not available."""
    import subprocess
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = FileNotFoundError("git not found")
        yield mock_run


@pytest.fixture
def mock_first_commit():
    """Mock for first commit scenario."""
    import subprocess
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = [
            subprocess.CalledProcessError(128, 'git'),  # HEAD~1 fails
            MagicMock(returncode=0, stdout="initial_file.py\n", stderr="")  # fallback
        ]
        yield mock_run


@pytest.fixture
def classified_violations():
    """Sample pre-classified violations."""
    return [
        {
            "file": "src/changed.py",
            "line": 1,
            "message": "Issue 1",
            "classification": "REGRESSION",
            "blocking": True
        },
        {
            "file": "src/old.py",
            "line": 2,
            "message": "Issue 2",
            "classification": "PRE_EXISTING",
            "blocking": False
        },
    ]


@pytest.fixture
def temp_workflow_file(tmp_path):
    """Create temporary deep-validation-workflow.md for testing."""
    workflow_dir = tmp_path / ".claude" / "skills" / "devforgeai-qa" / "references"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_file = workflow_dir / "deep-validation-workflow.md"
    workflow_file.write_text("""# Deep Validation Workflow

## Step 2: Validation Steps

### Step 2.1: Code Quality

#### Step 2.1.1: Lint Check
#### Step 2.1.2: Type Check
#### Step 2.1.3: Complexity Check
#### Step 2.1.4: Security Check
""")
    return workflow_file
