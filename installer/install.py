"""
Main installation orchestrator.

This module coordinates the complete installation workflow:
1. Detect existing installation (fresh vs upgrade)
2. Create backup before any modifications (atomic transaction)
3. Deploy files with error handling
4. Update version.json
5. Support 5 modes: fresh, upgrade, rollback, validate, uninstall
6. Offline installation support (STORY-069)

Functions:
- install(target_path: Path, mode: str = None, force: bool = False) -> dict
- check_network_availability(timeout: int = 2) -> bool (re-export from network module)
- display_network_status(is_online: bool) -> None (re-export from network module)
- run_offline_installation(...) -> dict (re-export from offline module)
- verify_bundle_structure(bundle_root: Path) -> dict (re-export from bundle module)
- count_bundled_files(bundle_root: Path) -> int (re-export from bundle module)
- measure_bundle_size(bundle_root: Path) -> dict (re-export from bundle module)
- verify_bundle_integrity(bundle_root: Path) -> dict (re-export from checksum module)
"""

import json
import shutil
from pathlib import Path

from . import version as ver_module
from . import backup
from . import deploy
from . import rollback as rollback_module
from . import validate
from . import merge

# STORY-069: Offline installation imports
from . import network
from . import offline
from . import checksum
from . import bundle

# Re-export offline installation functions for test compatibility
check_network_availability = network.check_network_availability
display_network_status = network.display_network_status
warn_network_feature_unavailable = network.warn_network_feature_unavailable
detect_python_version = network.detect_python_version
warn_missing_dependency = network.warn_missing_dependency
check_disk_space = network.check_disk_space
check_git_available = network.check_git_available

run_offline_installation = offline.run_offline_installation
run_installation = offline.run_installation
install_python_cli_offline = offline.install_python_cli_offline
find_bundled_wheels = offline.find_bundled_wheels
validate_offline_installation = offline.validate_offline_installation
validate_git_initialization = offline.validate_git_initialization
validate_claude_md_merge = offline.validate_claude_md_merge

verify_bundle_structure = bundle.verify_bundle_structure
count_bundled_files = bundle.count_bundled_files
measure_bundle_size = bundle.measure_bundle_size

calculate_sha256 = checksum.calculate_sha256
load_checksums = checksum.load_checksums
verify_file_checksum = checksum.verify_file_checksum
verify_bundle_integrity = checksum.verify_bundle_integrity
verify_all_files_have_checksums = checksum.verify_all_files_have_checksums

# Constants for version.json
VERSION_JSON_SCHEMA = "1.0"
INSTALLATION_SUCCESS_MESSAGE = "✅ DevForgeAI {version} installed successfully ({mode})"


def _update_version_file(devforgeai_path: Path, source_version: str, source_version_data: dict, mode: str, result: dict) -> bool:
    """
    Update version.json with current installation data.

    Args:
        devforgeai_path: Path to .devforgeai directory
        source_version: Version string being installed
        source_version_data: Version data dict from source
        mode: Installation mode (fresh_install, upgrade, etc.)
        result: Result dict to update with status/messages/errors

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        version_data = {
            "version": source_version,
            "installed_at": source_version_data.get("released_at", "2025-11-17T00:00:00Z"),
            "mode": mode,
            "schema_version": VERSION_JSON_SCHEMA,
        }
        version_file = devforgeai_path / ".version.json"
        version_file.write_text(json.dumps(version_data, indent=2))
        result["messages"].append(f"Updated version.json: {source_version}")
        return True
    except OSError as e:
        result["errors"].append(f"Failed to write version.json: {e}")
        result["status"] = "failed"
        return False


def _get_source_version_data(source_root: Path) -> tuple[str, dict]:
    """
    Get source version data and handle errors.

    Args:
        source_root: Root path of source

    Returns:
        tuple: (version_string, version_data_dict)

    Raises:
        FileNotFoundError: If source version not found
    """
    source_devforgeai = source_root / "devforgeai"
    source_version_data = ver_module.get_source_version(source_devforgeai)
    source_version = source_version_data.get("version")
    return source_version, source_version_data


def _handle_uninstall_mode(target_root: Path, devforgeai_path: Path, result: dict) -> dict:
    """
    Handle uninstall mode: create backup and remove framework files.

    Args:
        target_root: Root path of target project
        devforgeai_path: Path to .devforgeai directory
        result: Result dict to update

    Returns:
        dict: Updated result with uninstall outcome
    """
    # Create backup before uninstalling
    current_version_data = ver_module.get_installed_version(devforgeai_path)
    current_version = current_version_data.get("version") if current_version_data else "unknown"

    backup_path, backup_manifest = backup.create_backup(
        target_root,
        reason="uninstall",
        from_version=current_version,
    )
    result["backup_path"] = str(backup_path)
    result["messages"].append(f"Backup created: {backup_manifest['created_at']}")

    # Remove framework directories (preserve .ai_docs and context)
    try:
        _remove_framework_files(target_root, result)
    except OSError as e:
        result["errors"].append(f"Uninstall failed: {e}")
        result["status"] = "failed"

    return result


def _handle_claude_md_merge(target_root: Path, source_root: Path, result: dict) -> None:
    """
    Handle CLAUDE.md merge: preserve user content and merge framework updates.

    Args:
        target_root: Root path of target project
        source_root: Root path of source
        result: Result dict to update with merge messages
    """
    try:
        user_claude_path = target_root / "CLAUDE.md"
        framework_claude_path = source_root / "CLAUDE.md"

        if user_claude_path.exists() and framework_claude_path.exists():
            # User has existing CLAUDE.md - merge with framework template
            merger = merge.CLAUDEmdMerger(target_root)
            merge_result = merger.merge_claude_md(user_claude_path, framework_claude_path, backup=True)

            if merge_result.success:
                user_claude_path.write_text(merge_result.merged_content, encoding='utf-8')
                result["messages"].append("✓ CLAUDE.md merged with user content preserved")
            else:
                result["warnings"].append("CLAUDE.md merge had conflicts (kept user version)")
        elif not user_claude_path.exists() and framework_claude_path.exists():
            # No existing CLAUDE.md - copy framework template and substitute variables
            from . import variables

            framework_content = framework_claude_path.read_text(encoding='utf-8')
            detector = variables.TemplateVariableDetector(target_root)
            all_variables = detector.get_all_variables()
            substituted_content = detector.substitute_variables(framework_content, all_variables)

            user_claude_path.write_text(substituted_content, encoding='utf-8')
            result["messages"].append("✓ CLAUDE.md created from framework template")

    except Exception as e:
        result["warnings"].append(f"CLAUDE.md merge skipped: {e}")


def _remove_framework_files(target_root: Path, result: dict) -> None:
    """
    Remove framework files from target directory.

    Removes .claude/, most .devforgeai/ subdirs, and CLAUDE.md.
    Preserves .devforgeai/context/, .devforgeai/.backups/, .devforgeai/config/

    Args:
        target_root: Root path of target project
        result: Result dict to update with messages
    """
    if (target_root / ".claude").exists():
        shutil.rmtree(target_root / ".claude")
        result["messages"].append("Removed .claude/")

    # Remove .devforgeai subdirs except context, .backups, config
    devforgeai_dir = target_root / ".devforgeai"
    if devforgeai_dir.exists():
        for subdir in devforgeai_dir.iterdir():
            if subdir.name not in {"context", ".backups", "config"}:
                if subdir.is_dir():
                    shutil.rmtree(subdir)

    if (target_root / "CLAUDE.md").exists():
        (target_root / "CLAUDE.md").unlink()
        result["messages"].append("Removed CLAUDE.md")

    result["messages"].append("DevForgeAI framework uninstalled (context preserved)")


def _handle_rollback_mode(target_root: Path, result: dict) -> dict:
    """
    Handle rollback mode: restore from most recent backup using RollbackService.

    Steps (AC#4):
    1. Find most recent backup if backup_dir not specified
    2. Invoke RollbackService.rollback(backup_dir, target_dir)
    3. Verify checksums after restoration
    4. Validate installation state
    5. Update version metadata (reverted from backup)
    6. Return RollbackResult with status and file counts

    Args:
        target_root: Root path of target project
        result: Result dict to update

    Returns:
        dict: Updated result with rollback outcome
    """
    from installer.services.rollback_service import RollbackService
    from installer.services.install_logger import InstallLogger

    try:
        # Step 1: Find most recent backup
        backups = rollback_module.list_backups(target_root)
        if not backups:
            result["errors"].append("No backups available for rollback")
            result["status"] = "failed"
            return result

        # Use most recent backup (list is sorted newest first)
        backup_to_restore = backups[0]
        backup_path = backup_to_restore["path"]
        result["backup_path"] = str(backup_path)

        # Verify backup directory exists
        if not backup_path.exists():
            result["errors"].append(f"Backup directory not found: {backup_path}")
            result["status"] = "failed"
            return result

        # Step 2: Initialize RollbackService and invoke rollback workflow
        logger = InstallLogger()
        rollback_service = RollbackService(logger=logger, installation_root=target_root)

        # Execute full rollback: restore files, cleanup partials, remove empty dirs
        rollback_result = rollback_service.rollback(
            backup_dir=backup_path,
            target_dir=target_root
        )

        result["files_restored"] = rollback_result.files_restored

        # Clean up files that were created after backup but don't belong
        # (files in target that aren't in backup)
        import shutil

        # Remove directories that shouldn't exist after rollback
        # .devforgeai/ and .claude/ should be completely restored from backup
        devforgeai_target = target_root / ".devforgeai"
        claude_target = target_root / ".claude"

        # Delete and restore .claude/ to ensure complete cleanup
        if (backup_path / ".claude").exists() and claude_target.exists():
            shutil.rmtree(claude_target)
            shutil.copytree(backup_path / ".claude", claude_target, symlinks=False)

        # Delete and restore .devforgeai/ to ensure complete cleanup
        if (backup_path / ".devforgeai").exists() and devforgeai_target.exists():
            shutil.rmtree(devforgeai_target)
            shutil.copytree(backup_path / ".devforgeai", devforgeai_target, symlinks=False)

        result["messages"].append(
            f"Rolled back to version {backup_to_restore.get('to_version', 'unknown')} "
            f"from backup {backup_to_restore['name']}"
        )

        # Step 3: Verify checksums after restoration
        verification = rollback_module.verify_rollback(target_root, backup_path)
        if not verification["valid"]:
            result["warnings"].append(
                f"Rollback verification incomplete: {', '.join(verification.get('errors', []))}"
            )
        else:
            result["messages"].append("Backup integrity verified after restoration")

        # Step 4: Validate installation state
        validation = validate.validate_installation(target_root)
        if not validation.get("valid", False):
            result["warnings"].append("Installation validation found issues after rollback")
        else:
            result["messages"].append("Installation state validated after rollback")

        # Step 5: Update version metadata (reverted from backup)
        # Version.json should already be restored from backup by rollback_service
        devforgeai_path = target_root / ".devforgeai"
        current_version_data = ver_module.get_installed_version(devforgeai_path)
        if current_version_data:
            reverted_version = current_version_data.get("version", "unknown")
            result["version"] = reverted_version
            result["messages"].append(f"Version reverted to: {reverted_version}")

        # Success if rollback completed
        result["status"] = "success"
        return result

    except FileNotFoundError as e:
        result["errors"].append(f"Rollback failed: {e}")
        result["status"] = "failed"
        return result
    except Exception as e:
        result["errors"].append(f"Rollback error: {e}")
        result["status"] = "failed"
        return result


def _detect_installation_mode(
    target_root: Path,
    source_version: str,
) -> str:
    """
    Detect installation mode (fresh, patch_upgrade, etc.).

    Args:
        target_root: Root path of target project
        source_version: Version string from source

    Returns:
        str: Installation mode
    """
    devforgeai_path = target_root / ".devforgeai"
    installed_data = ver_module.get_installed_version(devforgeai_path)

    if installed_data is None:
        return "fresh_install"

    installed_version = installed_data.get("version")
    return ver_module.compare_versions(installed_version, source_version)


def install(
    target_path: str | Path,
    source_path: str | Path = None,
    mode: str = None,
    force: bool = False,
) -> dict:
    """
    Execute installation in specified mode.

    Modes:
    1. "fresh": Fresh install (no existing installation)
    2. "upgrade": Upgrade existing installation (create backup, deploy, update version)
    3. "rollback": Restore from backup (list backups, user selects, restore)
    4. "validate": Validate existing installation (check structure, files, CLI)
    5. "uninstall": Remove framework files (create backup, remove, preserve context)

    Atomic transaction behavior:
    - Creates backup BEFORE any file modifications
    - Auto-rollback on deployment failure
    - Returns detailed report on success/failure

    Args:
        target_path: Root path of target project
        source_path: Root path of source (default: current dir/src/)
        mode: Installation mode (auto-detected if None)
        force: Force installation even if checks fail

    Returns:
        dict: Installation result with:
        - "status": "success", "failed", or "rollback"
        - "mode": Installation mode used
        - "version": Version installed/verified
        - "backup_path": Path to backup created (if applicable)
        - "files_deployed": File count (if applicable)
        - "files_restored": File count (if rollback applicable)
        - "errors": list[str]
        - "warnings": list[str]
        - "messages": list[str] - User-friendly messages
    """
    target_root = Path(target_path)
    source_root = Path(source_path) if source_path else Path.cwd() / "src"

    result = {
        "status": "success",
        "mode": mode,
        "version": None,
        "backup_path": None,
        "files_deployed": 0,
        "files_restored": 0,
        "errors": [],
        "warnings": [],
        "messages": [],
    }

    try:
        # Validate target project structure
        if not target_root.exists():
            target_root.mkdir(parents=True, exist_ok=True)
            result["messages"].append(f"Created project directory: {target_root}")

        # Ensure .devforgeai directory exists
        devforgeai_path = target_root / ".devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        # Handle "validate" mode (no modifications, no source needed)
        if mode == "validate":
            validation = validate.validate_installation(target_root)
            result["status"] = "success" if validation["valid"] else "failed"
            result.update(validation)
            return result

        # Handle "rollback" mode (no source needed, uses backup)
        if mode == "rollback":
            return _handle_rollback_mode(target_root, result)

        # Validate source directory structure
        if not source_root.exists():
            result["errors"].append(f"Source directory not found: {source_root}")
            result["status"] = "failed"
            raise FileNotFoundError(f"Source directory not found: {source_root}")

        required_source_dirs = [source_root / "devforgeai", source_root / "claude"]
        missing_dirs = [d for d in required_source_dirs if not d.exists()]
        if missing_dirs:
            result["errors"].append(
                f"Source directory structure incomplete. Missing: {[str(d) for d in missing_dirs]}"
            )
            result["status"] = "failed"
            raise FileNotFoundError(
                f"Source directory structure incomplete. Missing directories: {missing_dirs}"
            )

        # Get source version (required for install/upgrade/uninstall modes)
        try:
            source_devforgeai = source_root / "devforgeai"
            source_version_data = ver_module.get_source_version(source_devforgeai)
            source_version = source_version_data.get("version")
            result["version"] = source_version
        except (FileNotFoundError, json.JSONDecodeError) as e:
            result["errors"].append(f"Source version not found or corrupted: {e}")
            result["status"] = "failed"
            raise

        # Auto-detect mode if not specified
        if mode is None:
            mode = _detect_installation_mode(target_root, source_version)
            result["mode"] = mode

        # Handle "uninstall" mode
        if mode == "uninstall":
            return _handle_uninstall_mode(target_root, devforgeai_path, result)

        # Handle "fresh" and "upgrade" modes (require deployment)
        if mode not in {"fresh_install", "patch_upgrade", "minor_upgrade", "major_upgrade", "reinstall", "downgrade"}:
            result["errors"].append(f"Unknown installation mode: {mode}")
            result["status"] = "failed"
            return result

        # Create backup for upgrade/downgrade OR if CLAUDE.md exists (even on fresh install)
        backup_path = None
        should_backup = (mode != "fresh_install") or (target_root / "CLAUDE.md").exists()

        if should_backup:
            current_version_data = ver_module.get_installed_version(devforgeai_path)
            current_version = current_version_data.get("version") if current_version_data else None

            try:
                backup_reason = "upgrade" if mode != "fresh_install" else "fresh_install_claude_md_preservation"
                backup_path, backup_manifest = backup.create_backup(
                    target_root,
                    reason=backup_reason,
                    from_version=current_version,
                    to_version=source_version,
                )
                result["backup_path"] = str(backup_path)
                result["messages"].append(f"Backup created: {backup_manifest['created_at']}")
            except OSError as e:
                result["errors"].append(f"Backup creation failed: {e}")
                result["status"] = "failed"
                return result

        # Deploy framework files
        try:
            deploy_result = deploy.deploy_framework_files(
                source_root,
                target_root,
                preserve_configs=True,
            )
            result["files_deployed"] = deploy_result["files_deployed"]

            if deploy_result["status"] == "failed":
                result["errors"].extend(deploy_result["errors"])
                result["status"] = "failed"
                # Auto-rollback on deployment failure
                if backup_path:
                    result["status"] = "rollback"
                    restore_result = rollback_module.restore_from_backup(target_root, backup_path)
                    result["files_restored"] = restore_result["files_restored"]
                    result["messages"].append("Auto-rolled back to previous version due to deployment failure")
                return result

        except (FileNotFoundError, OSError) as e:
            result["errors"].append(f"Deployment failed: {e}")
            result["status"] = "failed"
            # Auto-rollback if backup exists
            if backup_path:
                result["status"] = "rollback"
                try:
                    restore_result = rollback_module.restore_from_backup(target_root, backup_path)
                    result["files_restored"] = restore_result["files_restored"]
                    result["messages"].append("Auto-rolled back to previous version due to deployment failure")
                except Exception as rollback_error:
                    result["errors"].append(f"Rollback also failed: {rollback_error}")
            return result

        # Set file permissions
        perm_result = deploy.set_file_permissions(target_root)
        if perm_result["status"] == "failed":
            result["warnings"].extend(perm_result["errors"])

        # Merge CLAUDE.md if user has an existing CLAUDE.md
        _handle_claude_md_merge(target_root, source_root, result)

        # Update version.json
        if not _update_version_file(devforgeai_path, source_version, source_version_data, mode, result):
            # Rollback on version.json failure
            if backup_path:
                result["status"] = "rollback"
                try:
                    restore_result = rollback_module.restore_from_backup(target_root, backup_path)
                    result["files_restored"] = restore_result["files_restored"]
                    result["messages"].append("Auto-rolled back due to version.json write failure")
                except Exception as rollback_error:
                    result["errors"].append(f"Rollback also failed: {rollback_error}")
            return result

        # Success message
        result["messages"].append(
            INSTALLATION_SUCCESS_MESSAGE.format(version=source_version, mode=mode)
        )

    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(f"Installation failed: {e}")

    return result
