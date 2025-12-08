"""UninstallReporter service for STORY-081.

Generates uninstall summary reports:
- Display summary to user
- Save report to backup directory
- Format statistics (files, space, duration)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from installer.uninstall_models import UninstallResult, UninstallPlan


class UninstallReporter:
    """Generates uninstall summary reports."""

    def __init__(self):
        """Initialize reporter."""
        pass

    def generate_summary(self, result: UninstallResult,
                         plan: Optional[UninstallPlan] = None) -> str:
        """Generate human-readable summary of uninstall operation.

        Args:
            result: UninstallResult with operation statistics
            plan: Optional UninstallPlan for additional details

        Returns:
            Formatted summary string
        """
        lines = [
            "",
            "═" * 60,
            "  DevForgeAI Uninstall Summary",
            "═" * 60,
            "",
            f"Status: {result.status.value}",
            "",
            f"Files Removed: {result.files_removed}",
            f"Files Preserved: {result.files_preserved}",
            f"Directories Removed: {result.directories_removed}",
            "",
            f"Disk Space Freed: {result.space_freed_mb:.2f} MB",
            f"Duration: {result.duration_seconds:.1f} seconds",
            "",
        ]

        if result.backup_path:
            lines.append(f"Backup Location: {result.backup_path}")
            lines.append("")

        if result.errors:
            lines.append("Errors:")
            for error in result.errors[:10]:  # Show first 10 errors
                lines.append(f"  - {error}")
            if len(result.errors) > 10:
                lines.append(f"  ... and {len(result.errors) - 10} more")
            lines.append("")

        if result.warnings:
            lines.append("Warnings:")
            for warning in result.warnings[:10]:
                lines.append(f"  - {warning}")
            if len(result.warnings) > 10:
                lines.append(f"  ... and {len(result.warnings) - 10} more")
            lines.append("")

        lines.append("═" * 60)
        lines.append("")

        return "\n".join(lines)

    def save_report(self, result: UninstallResult, backup_dir: str) -> str:
        """Save report to backup directory.

        Args:
            result: UninstallResult to save
            backup_dir: Directory to save report in

        Returns:
            Path to saved report file
        """
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_filename = f"uninstall-report-{timestamp}.json"
        report_path = backup_path / report_filename

        # Create report data
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "status": result.status.value,
            "files_removed": result.files_removed,
            "files_preserved": result.files_preserved,
            "directories_removed": result.directories_removed,
            "space_freed_mb": result.space_freed_mb,
            "duration_seconds": result.duration_seconds,
            "backup_path": result.backup_path,
            "errors": result.errors,
            "warnings": result.warnings,
        }

        # Write JSON report
        report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

        # Also write human-readable summary
        summary_path = backup_path / f"uninstall-summary-{timestamp}.txt"
        summary_path.write_text(self.generate_summary(result), encoding="utf-8")

        return str(report_path)

    def format_file_list(self, files: list, max_items: int = 20) -> str:
        """Format a list of files for display.

        Args:
            files: List of file paths
            max_items: Maximum items to display

        Returns:
            Formatted string
        """
        if not files:
            return "  (none)"

        lines = []
        for i, file_path in enumerate(files[:max_items]):
            lines.append(f"  - {file_path}")

        if len(files) > max_items:
            lines.append(f"  ... and {len(files) - max_items} more")

        return "\n".join(lines)

    def generate_dry_run_summary(self, plan: UninstallPlan) -> str:
        """Generate summary for dry-run mode.

        Args:
            plan: UninstallPlan showing what would be removed

        Returns:
            Formatted summary string
        """
        total_mb = plan.total_size_bytes / (1024 * 1024)
        preserved_mb = plan.preserved_size_bytes / (1024 * 1024)

        lines = [
            "",
            "═" * 60,
            "  DevForgeAI Uninstall Plan (DRY RUN)",
            "═" * 60,
            "",
            "⚠️  NO FILES WILL BE MODIFIED",
            "",
            f"Files to Remove: {len(plan.files_to_remove)}",
            self.format_file_list([f.path if hasattr(f, 'path') else f
                                   for f in plan.files_to_remove]),
            "",
            f"Files to Preserve: {len(plan.files_to_preserve)}",
            self.format_file_list([f.path if hasattr(f, 'path') else f
                                   for f in plan.files_to_preserve]),
            "",
            f"Directories to Remove: {len(plan.directories_to_remove)}",
            self.format_file_list(plan.directories_to_remove),
            "",
            f"Space to Free: {total_mb:.2f} MB",
            f"Space Preserved: {preserved_mb:.2f} MB",
            "",
            "═" * 60,
            "",
            "Run without --dry-run to execute this plan.",
            "",
        ]

        return "\n".join(lines)
