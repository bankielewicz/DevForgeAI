"""
Shared fixtures for auto-detection service tests.

Provides common setup for detection service testing including:
- Temporary directories
- Mock detection results
- Common test data
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create temporary directory for test isolation.

    Automatically cleaned up after test completion.
    """
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def fresh_installation_dir(temp_dir: Path) -> Path:
    """
    Create empty directory for fresh installation testing.

    No existing DevForgeAI files present.
    """
    return temp_dir


@pytest.fixture
def existing_installation_dir(temp_dir: Path) -> Path:
    """
    Create directory with existing DevForgeAI installation structure.

    Contains:
    - .devforgeai/.version.json file
    - .claude/skills/ directory
    - .devforgeai/context/ directory
    """
    import json

    # Create .devforgeai structure
    devforgeai_dir = temp_dir / ".devforgeai"
    devforgeai_dir.mkdir()

    version_file = devforgeai_dir / ".version.json"
    version_data = {
        "installed_version": "1.0.0",
        "installed_at": "2025-11-25T10:30:00Z",
        "installation_source": "installer"
    }
    version_file.write_text(json.dumps(version_data))

    # Create .claude structure
    claude_dir = temp_dir / ".claude" / "skills"
    claude_dir.mkdir(parents=True)

    return temp_dir


@pytest.fixture
def git_repository_dir(temp_dir: Path) -> Path:
    """
    Create directory with git repository structure.

    Contains:
    - .git/ directory (simulated)
    """
    git_dir = temp_dir / ".git"
    git_dir.mkdir()

    return temp_dir


@pytest.fixture
def mock_version_info():
    """
    Mock VersionInfo for testing.

    Returns sample version info data structure.
    """
    from src.installer.services.version_detection_service import VersionInfo

    return VersionInfo(
        installed_version="1.0.0",
        installed_at="2025-11-25T10:30:00Z",
        installation_source="installer"
    )


@pytest.fixture
def mock_claudemd_info():
    """
    Mock ClaudeMdInfo for testing.

    Returns sample CLAUDE.md detection data structure.
    """
    from src.installer.services.claudemd_detection_service import ClaudeMdInfo
    from datetime import datetime

    return ClaudeMdInfo(
        exists=True,
        size=1024,
        modified=datetime.now().timestamp(),
        needs_backup=True
    )


@pytest.fixture
def mock_git_info(temp_dir: Path):
    """
    Mock GitInfo for testing.

    Returns sample git detection data structure.
    """
    from src.installer.services.git_detection_service import GitInfo

    return GitInfo(
        repository_root=temp_dir,
        is_submodule=False
    )


@pytest.fixture
def mock_conflict_info():
    """
    Mock ConflictInfo for testing.

    Returns sample conflict detection data structure.
    """
    from src.installer.services.file_conflict_detection_service import ConflictInfo

    return ConflictInfo(
        conflicts=[Path("CLAUDE.md"), Path(".claude/skills/test.md")],
        framework_count=1,
        user_count=1
    )


@pytest.fixture
def mock_detection_result(mock_version_info, mock_claudemd_info, mock_git_info, mock_conflict_info):
    """
    Mock DetectionResult for testing.

    Returns complete detection result with all fields populated.
    """
    from src.installer.services.auto_detection_service import DetectionResult

    return DetectionResult(
        version_info=mock_version_info,
        claudemd_info=mock_claudemd_info,
        git_info=mock_git_info,
        conflicts=mock_conflict_info
    )
