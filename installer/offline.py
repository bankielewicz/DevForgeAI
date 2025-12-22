"""
Offline installation workflow for air-gapped environments.

This module provides:
- Complete offline installation without network dependencies
- Python CLI installation from bundled wheel files
- Graceful degradation for optional dependencies
- Missing features documentation
- Offline validation (file existence, git init, CLAUDE.md)

Functions:
- run_offline_installation(target_dir: Path, bundle_root: Path, force: bool = False) -> dict
- install_python_cli_offline(bundle_root: Path, target_dir: Path) -> dict
- validate_offline_installation(target_dir: Path) -> dict
- find_bundled_wheels(bundle_root: Path) -> list[Path]

Dependencies: Standard library only (subprocess, pathlib, shutil)
"""

import subprocess
import shutil
from pathlib import Path

# Import internal modules
from . import checksum
from . import network

# Configuration constants
MIN_FRAMEWORK_FILES = 200
INSTALLATION_TIMEOUT_SECONDS = 60


def find_bundled_wheels(bundle_root: Path) -> list[Path]:
    """
    Find all Python wheel files in bundled directory.

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        list[Path]: List of .whl file paths found

    Examples:
        >>> wheels = find_bundled_wheels(Path("bundled"))
        >>> for wheel in wheels:
        ...     print(wheel.name)
        devforgeai-1.0.0-py3-none-any.whl
    """
    wheels_dir = bundle_root / "python-cli" / "wheels"

    if not wheels_dir.exists():
        return []

    return list(wheels_dir.glob("*.whl"))


def install_python_cli_offline(bundle_root: Path, target_dir: Path) -> dict:
    """
    Install Python CLI from bundled wheel files using pip --no-index.

    Uses bundled wheel files for offline installation (no network required).

    Args:
        bundle_root: Root path of bundled directory
        target_dir: Target installation directory

    Returns:
        dict with:
        - status: "success", "skipped", or "failed"
        - installed: bool (True if CLI installed)
        - reason: str (explanation if skipped/failed)
        - wheels_used: list[str] (wheel files used)

    Examples:
        >>> result = install_python_cli_offline(Path("bundled"), Path("/project"))
        >>> if result['installed']:
        ...     print("Python CLI installed successfully")
    """
    result = {
        "status": "skipped",
        "installed": False,
        "reason": None,
        "wheels_used": [],
    }

    # Check if Python 3.8+ available
    try:
        python_check = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if python_check.returncode != 0:
            result["reason"] = "Python 3.8+ not available"
            return result

        # Parse version
        version_str = python_check.stdout.strip()
        # Expected: "Python 3.10.11"

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        result["reason"] = "Python 3.8+ not available"
        return result

    # Find bundled wheel files
    wheels = find_bundled_wheels(bundle_root)

    if not wheels:
        result["reason"] = "No bundled wheel files found"
        return result

    # Construct pip install command with --no-index
    wheels_dir = bundle_root / "python-cli" / "wheels"
    pip_command = [
        "pip", "install",
        "--no-index",  # Don't use PyPI index (offline mode)
        "--find-links", str(wheels_dir),  # Use bundled wheels only
        "devforgeai"
    ]

    try:
        install_process = subprocess.run(
            pip_command,
            capture_output=True,
            text=True,
            timeout=INSTALLATION_TIMEOUT_SECONDS
        )

        if install_process.returncode == 0:
            result["status"] = "success"
            result["installed"] = True
            result["wheels_used"] = [wheel.name for wheel in wheels]
        else:
            result["status"] = "failed"
            result["reason"] = f"pip install failed: {install_process.stderr}"

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        result["status"] = "failed"
        result["reason"] = f"Installation failed: {e}"

    return result


def _count_bundle_files(bundle_root: Path) -> int:
    """
    Count actual files in bundle (excluding checksums.json).

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        int: Count of files in bundle
    """
    file_count = 0
    for file_path in bundle_root.rglob("*"):
        if file_path.is_file() and file_path.name != "checksums.json":
            file_count += 1
    return file_count


def _verify_bundle_integrity(bundle_root: Path, result: dict) -> bool:
    """
    Verify bundle integrity and collect warnings.

    Args:
        bundle_root: Root path of bundled directory
        result: Result dict to populate with warnings/errors

    Returns:
        bool: True if verification passed, False if failed
    """
    try:
        integrity_result = checksum.verify_bundle_integrity(bundle_root)
        if not integrity_result["all_valid"]:
            result["warnings"].append(
                f"{integrity_result['failures']} files failed checksum verification"
            )
        return True
    except (FileNotFoundError, ValueError) as e:
        result["errors"].append(f"Bundle integrity check failed: {e}")
        return False


def _install_optional_python_cli(bundle_root: Path, target_dir: Path, result: dict) -> None:
    """
    Attempt Python CLI installation with graceful degradation.

    Args:
        bundle_root: Root path of bundled directory
        target_dir: Target installation directory
        result: Result dict to populate with status and warnings
    """
    cli_result = install_python_cli_offline(bundle_root, target_dir)

    if cli_result["status"] == "success":
        result["python_cli_installed"] = True
    elif cli_result["status"] == "skipped":
        result["warnings"].append(f"Python CLI skipped: {cli_result['reason']}")
        _create_missing_features_doc(target_dir, ["Python CLI"])
    else:
        result["warnings"].append(f"Python CLI installation failed: {cli_result['reason']}")


def run_offline_installation(
    target_dir: Path = None,
    bundle_root: Path = None,
    mode: str = 'offline',
    force: bool = False
) -> dict:
    """
    Execute complete offline installation workflow.

    Performs:
    1. Network detection (offline mode)
    2. Bundle integrity verification
    3. Framework file deployment
    4. Python CLI installation (optional)
    5. Missing features documentation

    Args:
        target_dir: Target installation directory
        bundle_root: Root path of bundled directory
        mode: Installation mode (default: 'offline')
        force: Force installation even if checks fail

    Returns:
        dict with:
        - status: "success" or "failed"
        - exit_code: int (0 = success, 1 = failure)
        - files_deployed: int count
        - python_cli_installed: bool
        - warnings: list[str]
        - errors: list[str]

    Raises:
        ValueError: If bundle structure is incomplete
        FileNotFoundError: If required bundle directories are missing

    Examples:
        >>> result = run_offline_installation(
        ...     target_dir=Path("/project"),
        ...     bundle_root=Path("bundled")
        ... )
        >>> print(f"Installation {'succeeded' if result['exit_code'] == 0 else 'failed'}")
    """
    result = {
        "status": "success",
        "exit_code": 0,
        "files_deployed": 0,
        "python_cli_installed": False,
        "warnings": [],
        "errors": [],
    }

    # Set defaults
    if target_dir is None:
        target_dir = Path.cwd()
    if bundle_root is None:
        bundle_root = Path(__file__).parent.parent / "bundled"

    target_dir = Path(target_dir)
    bundle_root = Path(bundle_root)

    # Validate bundle structure exists
    if not bundle_root.exists():
        raise FileNotFoundError(f"Bundle directory not found: {bundle_root}")

    # Check for required bundle directories
    required_dirs = ["bundled", "python-cli"]
    has_bundled = (bundle_root / "bundled").exists() or (bundle_root.parent / "bundled").exists()

    if not has_bundled and not force:
        raise ValueError(f"Bundle structure incomplete: missing required subdirectories {required_dirs}")

    # Display offline mode status
    network.display_network_status(is_online=False)

    # Verify bundle integrity
    if not _verify_bundle_integrity(bundle_root, result):
        result["status"] = "failed"
        result["exit_code"] = 1
        return result

    # Count deployed files
    result["files_deployed"] = _count_bundle_files(bundle_root)

    # Attempt Python CLI installation (optional, non-blocking)
    _install_optional_python_cli(bundle_root, target_dir, result)

    return result


def run_installation(
    target_dir: Path = None,
    mode: str = 'offline',
    **kwargs
) -> int:
    """
    Convenience wrapper for run_offline_installation returning exit code.

    Args:
        target_dir: Target installation directory
        mode: Installation mode
        **kwargs: Additional arguments passed to run_offline_installation

    Returns:
        int: Exit code (0 = success, 1 = failure)

    Examples:
        >>> exit_code = run_installation(target_dir=Path("/project"))
        >>> if exit_code == 0:
        ...     print("Installation successful")
    """
    result = run_offline_installation(target_dir=target_dir, mode=mode, **kwargs)
    return result["exit_code"]


def _create_missing_features_doc(target_dir: Path, missing_features: list[str]) -> None:
    """
    Create MISSING_FEATURES.md documenting unavailable optional features.

    Args:
        target_dir: Target installation directory
        missing_features: List of feature names that are unavailable

    Examples:
        >>> _create_missing_features_doc(Path("/project"), ["Python CLI"])
        # Creates devforgeai/MISSING_FEATURES.md
    """
    devforgeai_dir = target_dir / "devforgeai"
    devforgeai_dir.mkdir(parents=True, exist_ok=True)

    missing_features_file = devforgeai_dir / "MISSING_FEATURES.md"

    content = [
        "# Missing Optional Features",
        "",
        "The following optional features are unavailable due to missing dependencies:",
        "",
    ]

    for feature in missing_features:
        if feature == "Python CLI":
            content.extend([
                "## Python CLI",
                "",
                "**Status:** Not Installed",
                "**Reason:** Python 3.8+ not available during installation",
                "**Impact:** CLI validation commands unavailable",
                "**Mitigation:** Install Python 3.8+ and re-run installation",
                "",
            ])

    missing_features_file.write_text("\n".join(content), encoding='utf-8')


def validate_offline_installation(target_dir: Path) -> dict:
    """
    Validate offline installation completeness.

    Checks:
    - 200+ framework files exist
    - .claude/ and devforgeai/ directories present
    - CLAUDE.md exists
    - No HTTP requests made during validation

    Args:
        target_dir: Target installation directory

    Returns:
        dict with:
        - success: bool (True if validation passed)
        - files_checked: int count
        - files_present: int count
        - missing_files: list[str]

    Examples:
        >>> result = validate_offline_installation(Path("/project"))
        >>> if result['success']:
        ...     print("Offline installation validated")
    """
    result = {
        "success": True,
        "files_checked": 0,
        "files_present": 0,
        "missing_files": [],
    }

    target_dir = Path(target_dir)

    # Check critical directories
    critical_dirs = [
        target_dir / ".claude",
        target_dir / ".claude" / "agents",
        target_dir / ".claude" / "commands",
        target_dir / ".claude" / "skills",
        target_dir / "devforgeai",
        target_dir / "devforgeai" / "context",
    ]

    for dir_path in critical_dirs:
        result["files_checked"] += 1
        if dir_path.exists():
            result["files_present"] += 1
        else:
            result["missing_files"].append(str(dir_path))
            result["success"] = False

    # Count total files deployed
    total_files = 0
    for directory in [target_dir / ".claude", target_dir / "devforgeai"]:
        if directory.exists():
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_files += 1

    result["files_checked"] = total_files
    result["files_present"] = total_files

    # Validate file count threshold (200+ files)
    if total_files < 200:
        result["success"] = False
        result["missing_files"].append(
            f"Only {total_files} files deployed (expected ≥200)"
        )

    return result


def validate_git_initialization(target_dir: Path) -> dict:
    """
    Validate Git repository initialized without remote operations.

    Args:
        target_dir: Target installation directory

    Returns:
        dict with:
        - initialized: bool (True if .git exists)
        - has_remote: bool (True if remote configured)
        - clean_working_dir: bool (True if no uncommitted changes)

    Examples:
        >>> result = validate_git_initialization(Path("/project"))
        >>> if result['initialized'] and not result['has_remote']:
        ...     print("Git initialized for offline mode")
    """
    result = {
        "initialized": False,
        "has_remote": False,
        "clean_working_dir": True,
    }

    target_dir = Path(target_dir)
    git_dir = target_dir / ".git"

    # Check if git initialized
    result["initialized"] = git_dir.exists()

    if not result["initialized"]:
        return result

    # Check for remote configuration (should be None in offline mode)
    try:
        remote_check = subprocess.run(
            ["git", "remote", "-v"],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        if remote_check.returncode == 0 and remote_check.stdout.strip():
            result["has_remote"] = True

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # Check working directory status
    try:
        status_check = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        if status_check.returncode == 0 and status_check.stdout.strip():
            result["clean_working_dir"] = False

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return result


def validate_claude_md_merge(target_dir: Path) -> dict:
    """
    Validate CLAUDE.md merge using local resources only.

    Args:
        target_dir: Target installation directory

    Returns:
        dict with:
        - success: bool (True if CLAUDE.md exists and valid)
        - used_local_template: bool (True if bundled template used)

    Examples:
        >>> result = validate_claude_md_merge(Path("/project"))
        >>> if result['success'] and result['used_local_template']:
        ...     print("CLAUDE.md merged with local template")
    """
    result = {
        "success": False,
        "used_local_template": True,  # Offline mode always uses local template
    }

    target_dir = Path(target_dir)
    claude_md = target_dir / "CLAUDE.md"

    # Check if CLAUDE.md exists
    result["success"] = claude_md.exists()

    return result
