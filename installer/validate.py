"""
Installation validation and health checks.

This module handles:
- Validating directory structure (.claude/skills/, devforgeai/protocols/)
- Validating version.json schema
- Checking CLI installation
- Verifying critical files (11 commands, 10 skills, 3 protocols, CLAUDE.md)

Functions:
- validate_installation(project_root: Path) -> dict
- validate_version_json(version_file: Path) -> dict
"""

import json
import platform
import subprocess
from pathlib import Path

# Validation thresholds
MIN_COMMANDS = 11
MIN_SKILLS = 10
MIN_PROTOCOLS = 3

# CLI check timeout
CLI_CHECK_TIMEOUT = 5

# Required fields for version.json
REQUIRED_VERSION_FIELDS = ["version", "installed_at", "mode", "schema_version"]


def _check_directory_structure(project_root: Path) -> tuple[bool, list[str]]:
    """
    Check if required directories exist.

    Args:
        project_root: Root path of project

    Returns:
        tuple: (all_exist, missing_dirs)
    """
    required_dirs = [
        ".claude/skills",
        ".claude/agents",
        ".claude/commands",
        ".claude/memory",
        "devforgeai/protocols",
        "devforgeai/context",
        "devforgeai/adrs",
    ]

    missing = []
    for dir_path in required_dirs:
        if not (project_root / dir_path).exists():
            missing.append(dir_path)

    return len(missing) == 0, missing


def _check_critical_files(project_root: Path) -> tuple[int, list[str]]:
    """
    Check for critical framework files.

    Looks for:
    - 11 commands in .claude/commands/
    - 10 skills in .claude/skills/
    - 3 protocols in devforgeai/protocols/
    - CLAUDE.md in project root

    Args:
        project_root: Root path of project

    Returns:
        tuple: (file_count, missing_files)
    """
    file_count = 0
    missing = []

    file_count += _check_commands(project_root, missing)
    file_count += _check_skills(project_root, missing)
    file_count += _check_protocols(project_root, missing)
    file_count += _check_claude_md(project_root, missing)

    return file_count, missing


def _count_files_by_pattern(directory: Path, pattern: str, description: str, minimum: int, missing: list) -> int:
    """
    Count files in directory matching pattern. Report if below minimum.

    Args:
        directory: Directory to check
        pattern: Glob pattern (e.g., "*.md")
        description: Description for error messages (e.g., ".claude/commands/")
        minimum: Minimum expected count
        missing: List to append error messages to

    Returns:
        int: Count of matching files/directories
    """
    if not directory.exists():
        return 0

    items = list(directory.glob(pattern))
    count = len(items)
    if count < minimum:
        missing.append(f"{description} has {count} files (expected ≥{minimum})")
    return count


def _count_directories(directory: Path, description: str, minimum: int, missing: list) -> int:
    """
    Count subdirectories. Report if below minimum.

    Args:
        directory: Directory to check
        description: Description for error messages
        minimum: Minimum expected count
        missing: List to append error messages to

    Returns:
        int: Count of subdirectories
    """
    if not directory.exists():
        return 0

    dirs = [d for d in directory.iterdir() if d.is_dir()]
    count = len(dirs)
    if count < minimum:
        missing.append(f"{description} has {count} dirs (expected ≥{minimum})")
    return count


def _check_commands(project_root: Path, missing: list) -> int:
    """Check commands directory. Returns count of commands."""
    commands_dir = project_root / ".claude" / "commands"
    return _count_files_by_pattern(commands_dir, "*.md", ".claude/commands/", MIN_COMMANDS, missing)


def _check_skills(project_root: Path, missing: list) -> int:
    """Check skills directory. Returns count of skills."""
    skills_dir = project_root / ".claude" / "skills"
    return _count_directories(skills_dir, ".claude/skills/", MIN_SKILLS, missing)


def _check_protocols(project_root: Path, missing: list) -> int:
    """Check protocols directory. Returns count of protocols."""
    protocols_dir = project_root / "devforgeai" / "protocols"
    return _count_files_by_pattern(protocols_dir, "*.md", "devforgeai/protocols/", MIN_PROTOCOLS, missing)


def _check_claude_md(project_root: Path, missing: list) -> int:
    """Check CLAUDE.md file. Returns 1 if exists, 0 otherwise."""
    if not (project_root / "CLAUDE.md").exists():
        missing.append("CLAUDE.md not found in project root")
        return 0
    return 1


def _check_cli_installation() -> tuple[bool, str]:
    """
    Check if DevForgeAI CLI is installed and accessible.

    Args:
        None

    Returns:
        tuple: (is_installed, error_message or version)
    """
    # HIGH-5 FIX: Use platform-specific command (Windows: where, Unix: which)
    check_cmd = "where" if platform.system() == "Windows" else "which"

    try:
        result = subprocess.run(
            [check_cmd, "devforgeai"],
            capture_output=True,
            timeout=CLI_CHECK_TIMEOUT,
        )
        if result.returncode == 0:
            return True, result.stdout.decode().strip()
        else:
            return False, "CLI not found in PATH"
    except FileNotFoundError:
        # Fallback: try importing the module directly (if installed as Python package)
        try:
            import devforgeai_cli
            return True, f"Installed as Python module: {devforgeai_cli.__file__}"
        except ImportError:
            return False, f"Could not check CLI ({check_cmd} command not available)"
    except subprocess.TimeoutExpired:
        return False, "CLI check timed out"
    except Exception as e:
        return False, f"CLI check failed: {e}"


def validate_version_json(version_file: Path) -> dict:
    """
    Validate version.json schema and content.

    Required fields:
    - version: str (semantic version like "1.0.0")
    - installed_at: str (ISO timestamp)
    - mode: str (one of: fresh_install, patch_upgrade, minor_upgrade, major_upgrade, reinstall, downgrade)
    - schema_version: str (e.g., "1.0")

    Args:
        version_file: Path to devforgeai/.version.json

    Returns:
        dict: Validation result with:
        - "valid": bool
        - "errors": list[str]
        - "version": str (if valid)
        - "mode": str (if valid)
    """
    result = {
        "valid": False,
        "errors": [],
        "version": None,
        "mode": None,
    }

    if not version_file.exists():
        result["errors"].append("version.json not found")
        return result

    try:
        content = json.loads(version_file.read_text())
    except json.JSONDecodeError as e:
        result["errors"].append(f"Invalid JSON: {e}")
        return result

    # Check required fields
    for field in REQUIRED_VERSION_FIELDS:
        if field not in content:
            result["errors"].append(f"Missing required field: {field}")

    # Validate fields
    _validate_version_field(content, result)
    _validate_mode_field(content, result)
    _validate_timestamp_field(content, result)

    result["valid"] = len(result["errors"]) == 0

    return result


def _validate_version_field(content: dict, result: dict) -> None:
    """Validate semantic version format."""
    if "version" not in content:
        return

    version_str = content["version"]
    result["version"] = version_str
    parts = version_str.split(".")

    if len(parts) != 3:
        result["errors"].append(f"Invalid version format: {version_str} (expected X.Y.Z)")
        return

    try:
        for part in parts:
            int(part)
    except ValueError:
        result["errors"].append(f"Version parts must be numeric: {version_str}")


def _validate_mode_field(content: dict, result: dict) -> None:
    """Validate installation mode."""
    if "mode" not in content:
        return

    valid_modes = {
        "fresh_install",
        "patch_upgrade",
        "minor_upgrade",
        "major_upgrade",
        "reinstall",
        "downgrade",
    }
    mode = content["mode"]
    result["mode"] = mode

    if mode not in valid_modes:
        result["errors"].append(f"Invalid mode: {mode} (expected one of {valid_modes})")


def _validate_timestamp_field(content: dict, result: dict) -> None:
    """Validate ISO 8601 timestamp format."""
    if "installed_at" not in content:
        return

    installed_at = content["installed_at"]
    # Simple check: should contain 'T' and 'Z' for ISO format
    if not (("T" in installed_at and "Z" in installed_at) or "+" in installed_at):
        result["errors"].append(f"Invalid timestamp format: {installed_at} (expected ISO 8601)")


def validate_installation(project_root: Path) -> dict:
    """
    Validate complete installation.

    Checks:
    1. Directory structure (.claude/*, devforgeai/*)
    2. Critical files (11+ commands, 10+ skills, 3+ protocols, CLAUDE.md)
    3. version.json schema and content
    4. CLI installed and accessible

    Args:
        project_root: Root path of project

    Returns:
        dict: Complete validation report with:
        - "valid": bool - True if all checks pass
        - "directory_structure_valid": bool
        - "critical_files_present": bool
        - "version_json_valid": bool
        - "cli_installed": bool
        - "critical_files_count": int
        - "missing_directories": list[str]
        - "missing_files": list[str]
        - "cli_path": str (if installed)
        - "errors": list[str] - All validation errors
        - "warnings": list[str] - Non-fatal issues
    """
    result = {
        "valid": False,
        "directory_structure_valid": False,
        "critical_files_present": False,
        "version_json_valid": False,
        "cli_installed": False,
        "critical_files_count": 0,
        "missing_directories": [],
        "missing_files": [],
        "cli_path": None,
        "errors": [],
        "warnings": [],
    }

    # Check directory structure
    dirs_valid, missing_dirs = _check_directory_structure(project_root)
    result["directory_structure_valid"] = dirs_valid
    result["missing_directories"] = missing_dirs
    if not dirs_valid:
        result["errors"].extend([f"Missing directory: {d}" for d in missing_dirs])

    # Check critical files
    file_count, missing_files = _check_critical_files(project_root)
    result["critical_files_count"] = file_count
    result["critical_files_present"] = len(missing_files) == 0
    result["missing_files"] = missing_files
    if missing_files:
        result["errors"].extend(missing_files)

    # Check version.json
    version_file = project_root / "devforgeai" / ".version.json"
    version_validation = validate_version_json(version_file)
    result["version_json_valid"] = version_validation["valid"]
    if not version_validation["valid"]:
        result["errors"].extend(version_validation["errors"])

    # Check CLI installation
    cli_installed, cli_info = _check_cli_installation()
    result["cli_installed"] = cli_installed
    if cli_installed:
        result["cli_path"] = cli_info
    else:
        result["warnings"].append(f"CLI not accessible: {cli_info}")

    # Determine overall validity
    # Core checks must pass
    result["valid"] = (
        result["directory_structure_valid"]
        and result["critical_files_present"]
        and result["version_json_valid"]
    )

    return result
