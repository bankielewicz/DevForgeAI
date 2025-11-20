"""
Main installation orchestrator.

This module coordinates the complete installation workflow:
1. Detect existing installation (fresh vs upgrade)
2. Create backup before any modifications (atomic transaction)
3. Deploy files with error handling
4. Update version.json
5. Support 5 modes: fresh, upgrade, rollback, validate, uninstall

Functions:
- install(target_path: Path, mode: str = None, force: bool = False) -> dict
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
        # Get source version
        try:
            source_devforgeai = source_root / "devforgeai"
            source_version_data = ver_module.get_source_version(source_devforgeai)
            source_version = source_version_data.get("version")
            result["version"] = source_version
        except FileNotFoundError as e:
            result["errors"].append(f"Source version not found: {e}")
            result["status"] = "failed"
            return result

        # Validate target project structure
        if not target_root.exists():
            target_root.mkdir(parents=True, exist_ok=True)
            result["messages"].append(f"Created project directory: {target_root}")

        # Ensure .devforgeai directory exists
        devforgeai_path = target_root / ".devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        # Auto-detect mode if not specified
        if mode is None:
            mode = _detect_installation_mode(target_root, source_version)
            result["mode"] = mode

        # Handle "validate" mode (no modifications)
        if mode == "validate":
            validation = validate.validate_installation(target_root)
            result["status"] = "success" if validation["valid"] else "failed"
            result.update(validation)
            return result

        # Handle "rollback" mode
        if mode == "rollback":
            backups = rollback_module.list_backups(target_root)
            if not backups:
                result["errors"].append("No backups available for rollback")
                result["status"] = "failed"
                return result

            # Use most recent backup
            backup_to_restore = backups[0]
            backup_path = backup_to_restore["path"]

            # Verify backup integrity
            backup_verification = validate.validate_version_json(backup_path / "manifest.json")
            if not backup_verification["valid"]:
                result["errors"].append("Backup integrity check failed")
                result["status"] = "failed"
                return result

            # Restore from backup
            restore_result = rollback_module.restore_from_backup(target_root, backup_path)
            result["files_restored"] = restore_result["files_restored"]
            result["backup_path"] = str(backup_path)

            if restore_result["status"] == "failed":
                result["status"] = "failed"
                result["errors"].extend(restore_result["errors"])
                return result

            result["messages"].append(f"Restored from backup: {backup_to_restore['name']}")
            return result

        # Handle "uninstall" mode
        if mode == "uninstall":
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
                if (target_root / ".claude").exists():
                    shutil.rmtree(target_root / ".claude")
                    result["messages"].append("Removed .claude/")

                # Remove .devforgeai subdirs except context, ai_docs references
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

            except OSError as e:
                result["errors"].append(f"Uninstall failed: {e}")
                result["status"] = "failed"
                return result

            return result

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

        # Update version.json
        try:
            version_data = {
                "version": source_version,
                "installed_at": source_version_data.get("released_at", "2025-11-17T00:00:00Z"),
                "mode": mode,
                "schema_version": "1.0",
            }
            version_file = devforgeai_path / ".version.json"
            version_file.write_text(json.dumps(version_data, indent=2))
            result["messages"].append(f"Updated version.json: {source_version}")
        except OSError as e:
            result["errors"].append(f"Failed to write version.json: {e}")
            result["status"] = "failed"
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
            f"✅ DevForgeAI {source_version} installed successfully ({mode})"
        )

    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(f"Installation failed: {e}")

    return result
