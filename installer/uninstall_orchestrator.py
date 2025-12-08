"""UninstallOrchestrator service for STORY-081.

Orchestrates the complete uninstall workflow:
1. Load manifest and classify files
2. Create uninstall plan based on mode
3. Display confirmation prompt (unless skipped)
4. Create backup before deletion
5. Remove files in safe order
6. Clean up CLI binaries and shell integrations
7. Generate and save summary report
"""

import time
from pathlib import Path
from typing import Any, List, Optional

from installer.uninstall_models import (
    UninstallRequest,
    UninstallPlan,
    UninstallResult,
    UninstallStatus,
    UninstallMode,
    ContentType,
    ClassifiedFile,
)
from installer.content_classifier import ContentClassifier
from installer.file_remover import FileRemover
from installer.cli_cleaner import CLICleaner
from installer.uninstall_reporter import UninstallReporter


class UninstallOrchestrator:
    """Orchestrates the complete uninstall workflow."""

    def __init__(
        self,
        manifest_manager: Any,
        backup_service: Any,
        file_system: Any = None,
        content_classifier: Optional[ContentClassifier] = None,
        file_remover: Optional[FileRemover] = None,
        cli_cleaner: Optional[CLICleaner] = None,
        reporter: Optional[UninstallReporter] = None,
        installation_root: Optional[Path] = None,
    ):
        """Initialize orchestrator with dependencies.

        Args:
            manifest_manager: Manager for installation manifest
            backup_service: Service for creating backups
            file_system: File system abstraction (optional)
            content_classifier: File classifier (created if not provided)
            file_remover: File remover (created if not provided)
            cli_cleaner: CLI cleaner (created if not provided)
            reporter: Report generator (created if not provided)
            installation_root: Root directory of installation
        """
        self.manifest_manager = manifest_manager
        self.backup_service = backup_service
        self.file_system = file_system
        self.installation_root = installation_root or Path.cwd()

        # Create or use provided services
        self.content_classifier = content_classifier or ContentClassifier(
            manifest_manager=manifest_manager,
            installation_root=self.installation_root,
        )
        self.file_remover = file_remover or FileRemover(
            file_system=file_system,
            installation_root=self.installation_root,
        )
        self.cli_cleaner = cli_cleaner or CLICleaner(file_system=file_system)
        self.reporter = reporter or UninstallReporter()

    def execute(self, request: UninstallRequest) -> UninstallResult:
        """Execute uninstall operation.

        Args:
            request: UninstallRequest with operation parameters

        Returns:
            UninstallResult with operation outcome
        """
        start_time = time.time()

        # Initialize result
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            errors=[],
            warnings=[],
        )

        try:
            # Step 1: Create uninstall plan
            plan = self._create_plan(request)

            # Step 2: Handle dry-run mode
            if request.dry_run:
                result.files_removed = 0
                result.files_preserved = len(plan.files_to_preserve)
                result.duration_seconds = time.time() - start_time
                return result

            # Step 3: Confirmation prompt (unless skipped)
            if not request.skip_confirmation:
                if not self._confirm_uninstall(plan):
                    result.status = UninstallStatus.CANCELLED
                    result.duration_seconds = time.time() - start_time
                    return result

            # Step 4: Create backup (unless skipped)
            if not request.skip_backup:
                backup_path = self._create_backup()
                result.backup_path = backup_path

            # Step 5: Remove files
            removal_result = self._remove_files(plan, request)
            result.files_removed = removal_result.get("files_removed", 0)
            result.files_preserved = len(plan.files_to_preserve)
            result.directories_removed = removal_result.get("directories_removed", 0)
            result.space_freed_mb = removal_result.get("space_freed_bytes", 0) / (1024 * 1024)
            result.errors.extend(removal_result.get("errors", []))

            # Step 6: Clean up CLI
            cli_result = self.cli_cleaner.remove_wrapper_scripts()
            result.warnings.extend(cli_result.warnings)

            # Step 7: Determine final status
            if result.errors:
                result.status = UninstallStatus.PARTIAL

        except Exception as e:
            result.status = UninstallStatus.FAILED
            result.errors.append(str(e))
            raise

        finally:
            result.duration_seconds = time.time() - start_time

        return result

    def _create_plan(self, request: UninstallRequest) -> UninstallPlan:
        """Create uninstall plan based on mode.

        Args:
            request: UninstallRequest with mode

        Returns:
            UninstallPlan with files to remove/preserve
        """
        plan = UninstallPlan()

        # Get all files from manifest
        manifest = self.manifest_manager.load_manifest()
        installed_files = manifest.get("installed_files", [])

        # Classify each file
        for file_path in installed_files:
            content_type = self.content_classifier.classify(file_path)

            classified = ClassifiedFile(
                path=file_path,
                content_type=content_type,
                size_bytes=self._get_file_size(file_path),
            )

            # Determine if file should be preserved
            if request.mode == "PRESERVE_USER_CONTENT":
                if content_type in [ContentType.USER_CONTENT, ContentType.USER_CREATED]:
                    plan.files_to_preserve.append(classified)
                    plan.preserved_size_bytes += classified.size_bytes
                elif content_type == ContentType.MODIFIED_FRAMEWORK:
                    # Preserve modified framework files with warning
                    plan.files_to_preserve.append(classified)
                    plan.preserved_size_bytes += classified.size_bytes
                else:
                    plan.files_to_remove.append(classified)
                    plan.total_size_bytes += classified.size_bytes
            else:
                # COMPLETE mode - remove everything
                plan.files_to_remove.append(classified)
                plan.total_size_bytes += classified.size_bytes

        # Identify directories to remove
        plan.directories_to_remove = self._get_directories_to_remove(
            [f.path for f in plan.files_to_remove],
            [f.path for f in plan.files_to_preserve],
        )

        return plan

    def _confirm_uninstall(self, plan: UninstallPlan) -> bool:
        """Display confirmation prompt to user.

        Args:
            plan: UninstallPlan to confirm

        Returns:
            True if user confirms, False otherwise
        """
        print(self.reporter.generate_dry_run_summary(plan))
        print("Are you sure you want to proceed? This cannot be undone. [y/N] ", end="")

        try:
            response = input().strip().lower()
            return response in ["y", "yes"]
        except EOFError:
            return False

    def _create_backup(self) -> str:
        """Create backup before uninstall.

        Returns:
            Path to backup

        Raises:
            Exception: If backup fails
        """
        return self.backup_service.create_backup()

    def _remove_files(self, plan: UninstallPlan, request: UninstallRequest) -> dict:
        """Remove files according to plan.

        Args:
            plan: UninstallPlan with files to remove
            request: UninstallRequest with mode

        Returns:
            Dict with removal statistics
        """
        stats = {
            "files_removed": 0,
            "directories_removed": 0,
            "space_freed_bytes": 0,
            "errors": [],
        }

        # Remove files
        file_paths = [f.path for f in plan.files_to_remove]
        removal_result = self.file_remover.remove_files(file_paths)

        stats["files_removed"] = removal_result.files_removed
        stats["space_freed_bytes"] = removal_result.total_space_bytes
        stats["errors"].extend(removal_result.errors)

        # Clean up empty directories
        dirs_removed = self.file_remover.cleanup_empty_directories(
            plan.directories_to_remove
        )
        stats["directories_removed"] = dirs_removed

        return stats

    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes.

        Args:
            file_path: Relative path to file

        Returns:
            File size in bytes, 0 if not found
        """
        if self.file_system:
            try:
                size = self.file_system.get_size(file_path)
                # Handle mock objects returning non-int
                return int(size) if isinstance(size, (int, float)) else 0
            except (Exception, TypeError):
                return 0

        full_path = self.installation_root / file_path
        if full_path.exists():
            return full_path.stat().st_size
        return 0

    def _get_directories_to_remove(
        self,
        files_to_remove: List[str],
        files_to_preserve: List[str],
    ) -> List[str]:
        """Get list of directories that can be removed.

        Args:
            files_to_remove: Files being removed
            files_to_preserve: Files being preserved

        Returns:
            List of directory paths safe to remove
        """
        # Collect all directories from files to remove
        dirs_from_remove = set()
        for file_path in files_to_remove:
            parts = Path(file_path).parts
            for i in range(1, len(parts)):
                dirs_from_remove.add("/".join(parts[:i]))

        # Collect directories containing preserved files
        dirs_with_preserved = set()
        for file_path in files_to_preserve:
            parts = Path(file_path).parts
            for i in range(1, len(parts)):
                dirs_with_preserved.add("/".join(parts[:i]))

        # Safe directories are those only containing removed files
        safe_dirs = dirs_from_remove - dirs_with_preserved

        # Sort by depth (deepest first)
        return sorted(safe_dirs, key=lambda p: p.count("/"), reverse=True)
