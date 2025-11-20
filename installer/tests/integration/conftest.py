"""
Shared fixtures for integration tests (STORY-045).

This module provides fixtures for end-to-end integration testing with REAL file I/O:
- Temporary test projects in /tmp with realistic directory structures
- Source framework files (mock .claude/ and .devforgeai/)
- Version files with proper semantic versioning
- User config files that should be preserved
- Backup validation helpers
- Performance measurement utilities

Fixtures:
- integration_project: Temporary project directory with real files
- source_framework: Mock source framework in /tmp
- baseline_project: Project with v1.0.0 installed (for upgrade testing)
- real_user_files: User-created files that must be preserved
"""

import pytest
import json
import shutil
import time
from pathlib import Path
from datetime import datetime, timezone


@pytest.fixture
def integration_project(tmp_path):
    """
    Create a temporary project directory for integration testing (real file I/O).

    This fixture creates a complete project structure with:
    - .claude/ directory with subdirectories
    - .devforgeai/ directory with subdirectories
    - .ai_docs/ directory (user-created, must be preserved)
    - CLAUDE.md (user-created, must be preserved)

    AC: Project structure matches DevForgeAI installation structure

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        dict: Project structure with keys:
        - "root": Path to project root
        - "claude": Path to .claude/
        - "devforgeai": Path to .devforgeai/
        - "ai_docs": Path to .ai_docs/ (user directory)
    """
    root = tmp_path / "integration_project"
    root.mkdir(parents=True)

    # Create .claude/ structure
    claude_dir = root / ".claude"
    claude_dir.mkdir()
    (claude_dir / "agents").mkdir(parents=True)
    (claude_dir / "commands").mkdir(parents=True)
    (claude_dir / "memory").mkdir(parents=True)
    (claude_dir / "scripts").mkdir(parents=True)
    (claude_dir / "skills").mkdir(parents=True)

    # Create .devforgeai/ structure
    devforgeai_dir = root / ".devforgeai"
    devforgeai_dir.mkdir()
    (devforgeai_dir / "config").mkdir(parents=True)
    (devforgeai_dir / "context").mkdir(parents=True)
    (devforgeai_dir / "protocols").mkdir(parents=True)
    (devforgeai_dir / "specs").mkdir(parents=True)
    (devforgeai_dir / "qa").mkdir(parents=True)
    (devforgeai_dir / "adrs").mkdir(parents=True)

    # Create .backups/ directory (for backup operations)
    (root / ".backups").mkdir()

    # Create user-owned directories (not part of framework, must be preserved)
    ai_docs_dir = root / ".ai_docs"
    ai_docs_dir.mkdir()
    (ai_docs_dir / "Stories").mkdir(parents=True)
    (ai_docs_dir / "Epics").mkdir(parents=True)

    return {
        "root": root,
        "claude": claude_dir,
        "devforgeai": devforgeai_dir,
        "ai_docs": ai_docs_dir,
    }


@pytest.fixture
def source_framework(tmp_path):
    """
    Create mock source framework files (simulating src/claude and src/devforgeai).

    This fixture creates a realistic source structure with:
    - 370 mock files in src/claude/ (agents, commands, memory, skills)
    - 80 mock files in src/devforgeai/ (config, protocols, specs)
    - version.json with proper semantic versioning
    - File content that can be verified after deployment

    AC: Source structure matches production DevForgeAI src/ layout

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        dict: Source structure with keys:
        - "root": Path to source root
        - "version": Version string from version.json
        - "file_count": Total file count (450)
    """
    src_root = tmp_path / "source_framework"
    src_root.mkdir()

    # Create src/claude/ structure
    src_claude = src_root / "claude"
    src_claude.mkdir()
    (src_claude / "agents").mkdir(parents=True)
    (src_claude / "commands").mkdir(parents=True)
    (src_claude / "memory").mkdir(parents=True)
    (src_claude / "skills").mkdir(parents=True)

    # Create mock files in src/claude (370 files)
    file_count = 0
    for i in range(370):
        subdir = [
            src_claude / "agents",
            src_claude / "commands",
            src_claude / "memory",
            src_claude / "skills",
        ][i % 4]
        file_path = subdir / f"file_{i:03d}.md"
        file_path.write_text(f"# Framework file {i}\n\nContent for integration testing\n")
        file_count += 1

    # Create src/devforgeai/ structure
    src_devforgeai = src_root / "devforgeai"
    src_devforgeai.mkdir()
    (src_devforgeai / "config").mkdir(parents=True)
    (src_devforgeai / "protocols").mkdir(parents=True)
    (src_devforgeai / "specs").mkdir(parents=True)

    # Create mock files in src/devforgeai (80 files)
    for i in range(80):
        subdir = [
            src_devforgeai / "config",
            src_devforgeai / "protocols",
            src_devforgeai / "specs",
        ][i % 3]
        file_path = subdir / f"spec_{i:03d}.md"
        file_path.write_text(f"# Specification {i}\n\nContent for framework\n")
        file_count += 1

    # Create version.json
    version_data = {
        "version": "1.0.1",
        "released_at": "2025-11-17T12:00:00Z",
        "schema_version": "1.0",
        "changes": ["Bug fix 1", "Bug fix 2"],
    }
    version_file = src_devforgeai / "version.json"
    version_file.write_text(json.dumps(version_data, indent=2))

    return {
        "root": src_root,
        "version": "1.0.1",
        "file_count": file_count + 1,  # +1 for version.json
    }


@pytest.fixture
def baseline_project(integration_project):
    """
    Create a project with v1.0.0 already installed (for upgrade/rollback testing).

    This fixture prepares a project that simulates an existing installation by:
    - Creating .version.json with v1.0.0 metadata
    - Creating sample .claude/ files
    - Creating sample .devforgeai/ files
    - Setting proper file timestamps

    AC: Existing installation properly detected (prevents fresh_install mode)

    Args:
        integration_project: Base project fixture

    Returns:
        dict: Project with baseline installation, includes:
        - "project": integration_project dict
        - "version_file": Path to .version.json
        - "version": "1.0.0"
    """
    project_root = integration_project["root"]
    devforgeai_dir = integration_project["devforgeai"]

    # Create .version.json with v1.0.0
    version_data = {
        "version": "1.0.0",
        "installed_at": "2025-11-15T10:00:00Z",
        "mode": "fresh_install",
        "schema_version": "1.0",
    }
    version_file = devforgeai_dir / ".version.json"
    version_file.write_text(json.dumps(version_data, indent=2))

    # Create some sample files to simulate existing installation (30 files)
    claude_files_created = 0
    for i in range(30):
        subdir = [
            integration_project["claude"] / "agents",
            integration_project["claude"] / "commands",
            integration_project["claude"] / "memory",
        ][i % 3]
        subdir.mkdir(parents=True, exist_ok=True)
        file_path = subdir / f"existing_file_{i}.md"
        file_path.write_text(f"Existing content {i} from v1.0.0\n")
        claude_files_created += 1

    return {
        "project": integration_project,
        "version_file": version_file,
        "version": "1.0.0",
        "files_created": claude_files_created,
    }


@pytest.fixture
def real_user_files(integration_project):
    """
    Create user-owned files that must be preserved during upgrades/uninstall.

    This fixture creates:
    - User context files (.devforgeai/context/*.md)
    - User stories (.ai_docs/Stories/*.md)
    - User hooks configuration
    - User feedback configuration

    These files should NOT be modified or deleted during:
    - fresh_install
    - upgrade
    - patch_upgrade
    - rollback
    - uninstall (only framework files deleted, user files preserved)

    AC: User files preserved after install/upgrade/uninstall operations

    Args:
        integration_project: Base project fixture

    Returns:
        dict: User files with paths and checksums
    """
    project_root = integration_project["root"]

    # User context files
    context_dir = project_root / ".devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    tech_stack_file = context_dir / "tech-stack.md"
    tech_stack_content = "# User Tech Stack\n- Python 3.10+\n- pytest\n- DevForgeAI\n"
    tech_stack_file.write_text(tech_stack_content)

    source_tree_file = context_dir / "source-tree.md"
    source_tree_content = "# Source Tree\nsrc/\n├── installer/\n└── tests/\n"
    source_tree_file.write_text(source_tree_content)

    # User story files
    stories_dir = project_root / ".ai_docs" / "Stories"
    stories_dir.mkdir(parents=True, exist_ok=True)

    story_file = stories_dir / "STORY-001.md"
    story_content = "# STORY-001: Test Story\n\nUser story content...\n"
    story_file.write_text(story_content)

    # User hooks configuration
    config_dir = project_root / ".devforgeai" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    hooks_file = config_dir / "hooks.yaml"
    hooks_content = "# User custom hooks\ncustom_hook: value\n"
    hooks_file.write_text(hooks_content)

    # User feedback configuration
    feedback_dir = project_root / ".devforgeai" / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)

    feedback_config = feedback_dir / "config.yaml"
    feedback_content = "# User feedback config\nfeedback_enabled: true\n"
    feedback_config.write_text(feedback_content)

    return {
        "tech_stack": {
            "path": tech_stack_file,
            "content": tech_stack_content,
        },
        "source_tree": {
            "path": source_tree_file,
            "content": source_tree_content,
        },
        "story": {
            "path": story_file,
            "content": story_content,
        },
        "hooks": {
            "path": hooks_file,
            "content": hooks_content,
        },
        "feedback_config": {
            "path": feedback_config,
            "content": feedback_content,
        },
    }


@pytest.fixture
def performance_timer():
    """
    Provide a performance measurement context manager.

    NFR Validation:
    - Fresh install: <180 seconds
    - Patch update: <30 seconds
    - Backup creation: <20 seconds
    - Rollback: <45 seconds

    Usage:
        with performance_timer.measure("fresh_install") as timer:
            install.install(target, mode="fresh")
        assert timer.elapsed < 180

    Returns:
        object: Timer with measure() context manager and elapsed property
    """
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        @property
        def elapsed(self):
            """Return elapsed seconds"""
            if self.start_time is None or self.end_time is None:
                return None
            return self.end_time - self.start_time

        class measure:
            """Context manager for measuring operation time"""
            def __init__(self, timer, operation_name):
                self.timer = timer
                self.operation_name = operation_name

            def __enter__(self):
                self.timer.start_time = time.time()
                return self.timer

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.timer.end_time = time.time()

    timer = Timer()

    # Attach measure method
    original_measure = timer.measure
    timer.measure = lambda op_name: original_measure(timer, op_name)

    return timer


@pytest.fixture
def file_integrity_checker():
    """
    Provide utilities for verifying file deployment integrity.

    AC: All framework files deployed with correct:
    - Paths (relative to target root)
    - Content (matches source)
    - Permissions (dirs=755, scripts=755, docs=644)

    Returns:
        object: Checker with methods:
        - verify_file_exists(path) -> bool
        - verify_file_content(path, expected) -> bool
        - verify_file_permissions(path, expected_mode) -> bool
        - verify_directory_exists(path) -> bool
    """
    class FileChecker:
        def verify_file_exists(self, file_path):
            """Check if file exists and is readable"""
            path = Path(file_path)
            return path.exists() and path.is_file()

        def verify_file_content(self, file_path, expected_content):
            """Check if file content matches expected"""
            path = Path(file_path)
            if not path.exists():
                return False
            return path.read_text() == expected_content

        def verify_file_permissions(self, file_path, expected_mode):
            """Check if file has expected permissions (octal)"""
            path = Path(file_path)
            if not path.exists():
                return False
            actual = path.stat().st_mode & 0o777
            return actual == expected_mode

        def verify_directory_exists(self, dir_path):
            """Check if directory exists"""
            path = Path(dir_path)
            return path.exists() and path.is_dir()

        def count_files(self, root_path):
            """Count all files under directory (recursive)"""
            path = Path(root_path)
            if not path.exists():
                return 0
            return sum(1 for _ in path.rglob("*") if _.is_file())

    return FileChecker()
