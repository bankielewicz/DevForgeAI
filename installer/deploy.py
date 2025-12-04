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

# Directories to NOT deploy (generated content or development-specific)
NO_DEPLOY_DIRS = {
    ".devforgeai/qa/reports",
    ".devforgeai/RCA",
    ".devforgeai/adrs",
    ".devforgeai/feedback/imported",
    ".devforgeai/logs",
    ".devforgeai/specs/enhancements",  # Development planning docs (not for production deployment)
}

# File extensions and names that should be executable
EXECUTABLE_SHELL_EXTENSION = ".sh"
EXECUTABLE_FILENAMES = {"devforgeai", "claude-code"}
EXECUTABLE_NAMES = {EXECUTABLE_SHELL_EXTENSION} | EXECUTABLE_FILENAMES  # Combined for backward compatibility


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


def _deploy_directory(
    source_dir: Path,
    target_dir: Path,
    result: dict,
    preserve_configs: bool = False,
) -> None:
    """
    Deploy files from source directory to target directory.

    Extracted method to eliminate duplicate code between .claude/ and .devforgeai/ deployment.

    Args:
        source_dir: Source directory to deploy from
        target_dir: Target directory to deploy to
        result: Result dict to update with deployment metrics
        preserve_configs: Whether to check preservation rules (devforgeai only)

    Raises:
        PermissionError: If source or target files cannot be accessed
        OSError: If disk is full or other I/O errors occur
    """
    if not source_dir.exists():
        return

    # First try to use copytree for efficiency (will raise exceptions if there are issues)
    try:
        def ignore_patterns(directory, files):
            """Ignore function for copytree."""
            ignored = set()
            for name in files:
                file_path = Path(directory) / name
                # Check exclusions and preservation
                if _should_exclude(file_path):
                    ignored.add(name)
                elif preserve_configs:
                    try:
                        relative = file_path.relative_to(source_dir)
                        if _should_preserve(relative) and (target_dir / relative).exists():
                            ignored.add(name)
                    except ValueError:
                        pass
            return ignored

        # Create parent directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Use copytree which will raise PermissionError or OSError on failures
        shutil.copytree(
            source_dir,
            target_dir,
            dirs_exist_ok=True,
            ignore=ignore_patterns if preserve_configs else None
        )

        # Count deployed files
        for file_path in target_dir.rglob("*"):
            if file_path.is_file():
                result["files_deployed"] += 1

    except PermissionError as e:
        raise PermissionError(f"Permission denied during deployment: {e}")
    except OSError as e:
        if e.errno == 28:  # No space left on device
            raise OSError(28, f"No space left on device: {e}")
        # Fall back to manual copy if copytree doesn't work for some reason
        _deploy_directory_manual(source_dir, target_dir, result, preserve_configs)


def _deploy_directory_manual(
    source_dir: Path,
    target_dir: Path,
    result: dict,
    preserve_configs: bool = False,
) -> None:
    """
    Deploy files manually (fallback when copytree not available).

    Args:
        source_dir: Source directory to deploy from
        target_dir: Target directory to deploy to
        result: Result dict to update with deployment metrics
        preserve_configs: Whether to check preservation rules (devforgeai only)
    """
    if not source_dir.exists():
        return

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(f"Permission denied creating target directory {target_dir}: {e}")
    except OSError as e:
        if e.errno == 28:  # No space left on device
            raise OSError(28, f"No space left on device: {e}")
        raise

    for source_file in source_dir.rglob("*"):
        if source_file.is_file():
            # Check exclusions
            if _should_exclude(source_file):
                result["files_skipped"] += 1
                continue

            # Calculate target path
            relative = source_file.relative_to(source_dir)
            target_file = target_dir / relative

            # Check if we should preserve this file (devforgeai only)
            if preserve_configs and _should_preserve(relative):
                if target_file.exists():
                    result["files_skipped"] += 1
                    continue

            # Create parent directories
            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                result["directories_created"] += 1
            except PermissionError as e:
                raise PermissionError(f"Permission denied creating directory {target_file.parent}: {e}")
            except OSError as e:
                if e.errno == 28:  # No space left on device
                    raise OSError(28, f"No space left on device: {e}")
                raise

            # Copy file
            try:
                shutil.copy2(source_file, target_file)
                result["files_deployed"] += 1
            except PermissionError as e:
                raise PermissionError(f"Permission denied copying {source_file} to {target_file}: {e}")
            except OSError as e:
                if e.errno == 28:  # No space left on device
                    raise OSError(28, f"No space left on device while copying {source_file}: {e}")
                result["errors"].append(f"Failed to copy {source_file}: {e}")
                result["status"] = "failed"


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

    source_claude = source_root / "claude"
    source_devforgeai = source_root / "devforgeai"

    try:
        # Deploy both directories using unified function
        # _deploy_directory handles missing directories gracefully (returns early)
        # This allows individual directory failures to propagate (PermissionError, OSError)
        _deploy_directory(source_claude, target_root / ".claude", result)
        _deploy_directory(source_devforgeai, target_root / ".devforgeai", result, preserve_configs)

    except (PermissionError, OSError) as e:
        # Propagate I/O exceptions (permission denied, disk full, etc.)
        result["errors"].append(f"Deployment failed: {e}")
        result["status"] = "failed"
        raise
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
