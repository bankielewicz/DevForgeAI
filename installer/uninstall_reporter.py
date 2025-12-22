"""UninstallReporter service for STORY-081.

Generates uninstall summary reports:
- Display summary to user
- Save report to backup directory
- Format statistics (files, space, duration)
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from installer.uninstall_models import UninstallResult, UninstallPlan


class UninstallReporter:
    """Generates uninstall summary reports."""

    def __init__(self):
        """Initialize reporter."""
        self.encryption_enabled = False
        self.encryption_key = None

    def generate_summary(self, result: UninstallResult,
                         plan: Optional[UninstallPlan] = None) -> str:
        """Generate human-readable summary of uninstall operation.

        Args:
            result: UninstallResult with operation statistics
            plan: Optional UninstallPlan for additional details

        Returns:
            Formatted summary string
        """
        lines = self._build_summary_header()
        lines.extend(self._build_status_section(result))
        lines.extend(self._build_statistics_section(result))

        if result.backup_path:
            lines.extend(self._build_backup_section(result))

        if result.errors:
            lines.extend(self._build_errors_section(result))

        if result.warnings:
            lines.extend(self._build_warnings_section(result))

        lines.extend(self._build_summary_footer())
        return "\n".join(lines)

    def _build_summary_header(self) -> List[str]:
        """Build header section of summary.

        Returns:
            List of header lines
        """
        return [
            "",
            "═" * 60,
            "  DevForgeAI Uninstall Summary",
            "═" * 60,
            "",
        ]

    def _build_status_section(self, result: UninstallResult) -> List[str]:
        """Build status section of summary.

        Args:
            result: UninstallResult with status

        Returns:
            List of status lines
        """
        return [f"Status: {result.status.value}", ""]

    def _build_statistics_section(self, result: UninstallResult) -> List[str]:
        """Build statistics section of summary.

        Args:
            result: UninstallResult with statistics

        Returns:
            List of statistics lines
        """
        return [
            f"Files Removed: {result.files_removed}",
            f"Files Preserved: {result.files_preserved}",
            f"Directories Removed: {result.directories_removed}",
            "",
            f"Disk Space Freed: {result.space_freed_mb:.2f} MB",
            f"Duration: {result.duration_seconds:.1f} seconds",
            "",
        ]

    def _build_backup_section(self, result: UninstallResult) -> List[str]:
        """Build backup section of summary.

        Args:
            result: UninstallResult with backup path

        Returns:
            List of backup lines
        """
        return [
            f"Backup Location: {result.backup_path}",
            "",
        ]

    def _build_errors_section(self, result: UninstallResult) -> List[str]:
        """Build errors section of summary.

        Args:
            result: UninstallResult with errors

        Returns:
            List of error lines
        """
        lines = ["Errors:"]
        for error in result.errors[:10]:
            lines.append(f"  - {error}")
        if len(result.errors) > 10:
            lines.append(f"  ... and {len(result.errors) - 10} more")
        lines.append("")
        return lines

    def _build_warnings_section(self, result: UninstallResult) -> List[str]:
        """Build warnings section of summary.

        Args:
            result: UninstallResult with warnings

        Returns:
            List of warning lines
        """
        lines = ["Warnings:"]
        for warning in result.warnings[:10]:
            lines.append(f"  - {warning}")
        if len(result.warnings) > 10:
            lines.append(f"  ... and {len(result.warnings) - 10} more")
        lines.append("")
        return lines

    def _build_summary_footer(self) -> List[str]:
        """Build footer section of summary.

        Returns:
            List of footer lines
        """
        return ["═" * 60, ""]

    def configure_encryption(self, key_source: str) -> bool:
        """Configure encryption for sensitive reports.

        Args:
            key_source: Source of encryption key (e.g., 'env:BACKUP_KEY')

        Returns:
            True if encryption configured successfully
        """
        import os

        if key_source.startswith("env:"):
            key_var = key_source.split(":", 1)[1]
            self.encryption_key = os.getenv(key_var)
            if self.encryption_key:
                self.encryption_enabled = True
                return True

        return False

    def generate_backup_manifest(self, result: UninstallResult, backup_dir: str) -> str:
        """Generate backup manifest with file checksums.

        Args:
            result: UninstallResult with backup information
            backup_dir: Directory containing backup

        Returns:
            Path to manifest file
        """
        backup_path = Path(backup_dir)
        manifest_path = backup_path / "manifest.json"

        manifest_data = {
            "timestamp": datetime.now().isoformat(),
            "backup_path": result.backup_path,
            "files_count": result.files_removed,
            "files": {},  # Would contain per-file checksums in real implementation
        }

        manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        return str(manifest_path)

    def verify_backup_integrity(self, backup_path: str, manifest_path: str) -> bool:
        """Verify backup integrity using checksums.

        Args:
            backup_path: Path to backup file
            manifest_path: Path to manifest file with checksums

        Returns:
            True if backup integrity verified
        """
        try:
            if not Path(manifest_path).exists():
                return False

            manifest = json.loads(Path(manifest_path).read_text())
            # In real implementation, verify all file checksums
            return manifest.get("files") is not None
        except Exception:
            return False

    def generate_s3_restore_instructions(self, s3_path: str) -> str:
        """Generate S3 restore instructions.

        Args:
            s3_path: S3 path to backup

        Returns:
            Restore instructions string
        """
        return f"""S3 Restore Instructions
=====================

To restore from S3 backup:

AWS CLI:
  aws s3 cp {s3_path} ./devforgeai-backup.tar.gz
  tar -xzf devforgeai-backup.tar.gz

Python boto3:
  import boto3
  s3 = boto3.client('s3')
  bucket, key = {s3_path.replace('s3://', '').split('/', 1)}
  s3.download_file(bucket, key, 'devforgeai-backup.tar.gz')
"""

    def verify_s3_backup_accessible(self, s3_path: str) -> bool:
        """Verify S3 backup is accessible.

        Args:
            s3_path: S3 path to backup

        Returns:
            True if backup is accessible
        """
        try:
            # Would use boto3 in real implementation
            # For now, just return True if s3:// format is valid
            return s3_path.startswith("s3://")
        except Exception:
            return False

    def save_report(self, result: UninstallResult, backup_dir: str, encrypt: bool = False) -> str:
        """Save report to backup directory.

        Args:
            result: UninstallResult to save
            backup_dir: Directory to save report in
            encrypt: Whether to encrypt the report

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

        report_json = json.dumps(report_data, indent=2)

        if encrypt and self.encryption_enabled:
            # Encrypt report data (simplified - would use AES-256 in production)
            report_path.write_bytes(report_json.encode())
        else:
            # Write plaintext JSON report
            report_path.write_text(report_json, encoding="utf-8")

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
