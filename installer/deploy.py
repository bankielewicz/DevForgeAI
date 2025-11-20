"""
Framework file deployment with exclusions and permissions management.

This module handles:
- Deploying src/claude/ → target/.claude/ (~370 files)
- Deploying src/devforgeai/ → target/.devforgeai/ (~80 files)
- Excluding backup files, caches, reports
- Setting file permissions (dirs=755, scripts=755, docs=644)
- Preserving user configurations

Functions:
- deploy_framework_files(source_root: Path, target_root: Path, preserve_configs: bool = True) -> dict
- set_file_permissions(target_root: Path) -> dict
"""

import shutil
import stat
from pathlib import Path

# Permission constants (octal)
PERM_DIR = 0o755
PERM_EXECUTABLE = 0o755
PERM_REGULAR = 0o644

# Patterns to exclude during deployment
EXCLUDE_PATTERNS = {
    "*.backup",
    "*.bak",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".coverage",
}

# Directories to preserve (user configs)
PRESERVE_PATHS = {
    ".devforgeai/config/hooks.yaml",
    ".devforgeai/feedback/config.yaml",
    ".devforgeai/context/",
}

# Directories to NOT deploy (generated content)
NO_DEPLOY_DIRS = {
    ".devforgeai/qa/reports",
    ".devforgeai/RCA",
    ".devforgeai/adrs",
    ".devforgeai/feedback/imported",
    ".devforgeai/logs",
}

# File extensions and names that should be executable
EXECUTABLE_NAMES = {".sh", "", "devforgeai", "claude-code"}  # Last two are filenames, empty is for .sh extension


def _should_exclude(file_path: Path) -> bool:
    """
    Check if file should be excluded from deployment.

    Args:
        file_path: Path to file to check

    Returns:
        bool: True if file should be excluded
    """
    # Check filename patterns
    for pattern in EXCLUDE_PATTERNS:
        if file_path.match(pattern):
            return True

    # Check directory paths
    for no_deploy in NO_DEPLOY_DIRS:
        if _path_contains(file_path, no_deploy):
            return True

    return False


def _path_contains(file_path: Path, directory_name: str) -> bool:
    """
    Check if file_path contains the specified directory.

    Args:
        file_path: Path to file to check
        directory_name: Directory name/path to search for

    Returns:
        bool: True if directory is in file path
    """
    parts = file_path.parts
    for part in parts:
        if part == directory_name or directory_name in str(file_path).replace("\\", "/"):
            return True
    return False


def _should_preserve(relative_path: Path) -> bool:
    """
    Check if file should be preserved (not overwritten).

    Args:
        relative_path: Relative path from project root

    Returns:
        bool: True if file should be preserved
    """
    rel_str = str(relative_path).replace("\\", "/")

    for preserve_path in PRESERVE_PATHS:
        if rel_str.startswith(preserve_path):
            return True

    return False


def deploy_framework_files(
    source_root: Path,
    target_root: Path,
    preserve_configs: bool = True,
) -> dict:
    """
    Deploy framework files from source to target.

    Deploys:
    - src/claude/ → target/.claude/ (~370 files)
    - src/devforgeai/ → target/.devforgeai/ (~80 files)

    Excludes:
    - *.backup*, __pycache__, *.pyc
    - qa/reports/, RCA/, adrs/, feedback/imported/, logs/

    Preserves (if preserve_configs=True):
    - .devforgeai/config/hooks.yaml
    - .devforgeai/feedback/config.yaml
    - .devforgeai/context/*.md (user context files)

    Does NOT touch:
    - .ai_docs/ (never modified)

    Args:
        source_root: Root path of source (contains src/claude/, src/devforgeai/)
        target_root: Root path of target project
        preserve_configs: Whether to preserve user config files

    Returns:
        dict: Deployment report with:
        - "status": "success" or "failed"
        - "files_deployed": int count
        - "files_skipped": int count
        - "directories_created": int count
        - "errors": list[str] of any errors

    Raises:
        FileNotFoundError: If source directories don't exist
        OSError: If files can't be written
    """
    result = {
        "status": "success",
        "files_deployed": 0,
        "files_skipped": 0,
        "directories_created": 0,
        "errors": [],
    }

    # HIGH-3 FIX: Validate source directories exist before attempting deployment
    source_claude = source_root / "claude"
    source_devforgeai = source_root / "devforgeai"

    required_sources = [source_claude, source_devforgeai]
    missing_sources = [s for s in required_sources if not s.exists()]

    if missing_sources:
        result["status"] = "failed"
        result["errors"].append(
            f"Source directories missing: {[str(s) for s in missing_sources]}"
        )
        return result

    try:
        # Deploy .claude/ directory
        if source_claude.exists():
            target_claude = target_root / ".claude"
            target_claude.mkdir(parents=True, exist_ok=True)

            for source_file in source_claude.rglob("*"):
                if source_file.is_file():
                    # Check exclusions
                    if _should_exclude(source_file):
                        result["files_skipped"] += 1
                        continue

                    # Calculate target path
                    relative = source_file.relative_to(source_claude)
                    target_file = target_claude / relative

                    # Create parent directories
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    result["directories_created"] += 1

                    # Copy file
                    try:
                        shutil.copy2(source_file, target_file)
                        result["files_deployed"] += 1
                    except OSError as e:
                        result["errors"].append(f"Failed to copy {source_file}: {e}")
                        result["status"] = "failed"

        # Deploy .devforgeai/ directory (selective)
        source_devforgeai = source_root / "devforgeai"
        if source_devforgeai.exists():
            target_devforgeai = target_root / ".devforgeai"
            target_devforgeai.mkdir(parents=True, exist_ok=True)

            for source_file in source_devforgeai.rglob("*"):
                if source_file.is_file():
                    # Check exclusions
                    if _should_exclude(source_file):
                        result["files_skipped"] += 1
                        continue

                    # Calculate relative and target path
                    relative = source_file.relative_to(source_devforgeai)
                    target_file = target_devforgeai / relative

                    # Check if we should preserve this file
                    if preserve_configs and _should_preserve(relative):
                        if target_file.exists():
                            result["files_skipped"] += 1
                            continue

                    # Create parent directories
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    result["directories_created"] += 1

                    # Copy file
                    try:
                        shutil.copy2(source_file, target_file)
                        result["files_deployed"] += 1
                    except OSError as e:
                        result["errors"].append(f"Failed to copy {source_file}: {e}")
                        result["status"] = "failed"

    except FileNotFoundError as e:
        result["errors"].append(f"Source directory not found: {e}")
        result["status"] = "failed"
        raise

    return result


def _is_executable_file(file_path: Path) -> bool:
    """
    Check if file should have executable permissions.

    Args:
        file_path: Path to file to check

    Returns:
        bool: True if file should be executable
    """
    return file_path.suffix == ".sh" or file_path.name in ("devforgeai", "claude-code")


def set_file_permissions(target_root: Path) -> dict:
    """
    Set appropriate file permissions after deployment.

    Sets:
    - Directories: 755 (rwxr-xr-x)
    - .sh files: 755 (rwxr-xr-x)
    - Other files: 644 (rw-r--r--)

    Args:
        target_root: Root path of target project

    Returns:
        dict: Permission setting report with:
        - "status": "success" or "failed"
        - "dirs_updated": int count
        - "executable_updated": int count
        - "regular_updated": int count
        - "errors": list[str] of any errors
    """
    result = {
        "status": "success",
        "dirs_updated": 0,
        "executable_updated": 0,
        "regular_updated": 0,
        "errors": [],
    }

    try:
        # Walk through all files in framework directories
        for path in target_root.rglob("*"):
            _set_path_permissions(path, result)

    except Exception as e:
        result["errors"].append(f"Permission setting failed: {e}")
        result["status"] = "failed"

    return result


def _set_path_permissions(path: Path, result: dict) -> None:
    """
    Set permissions for a single path.

    Args:
        path: Path to file or directory
        result: Result dict to update with status
    """
    try:
        if path.is_dir():
            path.chmod(PERM_DIR)
            result["dirs_updated"] += 1
        elif path.is_file():
            if _is_executable_file(path):
                path.chmod(PERM_EXECUTABLE)
                result["executable_updated"] += 1
            else:
                path.chmod(PERM_REGULAR)
                result["regular_updated"] += 1
    except OSError as e:
        result["errors"].append(f"Failed to set permissions for {path}: {e}")
        result["status"] = "failed"
