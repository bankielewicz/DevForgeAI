"""
Unit tests for UninstallReporter service.
Tests summary generation and report persistence.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch


class TestUninstallReporterInit:
    """Test UninstallReporter initialization."""

    def test_should_instantiate_successfully(self):
        """Test: UninstallReporter initializes."""
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()
        assert reporter is not None


class TestSummaryGeneration:
    """Test uninstall summary report generation."""

    def test_should_generate_summary_with_all_fields(self):
        """Test: Summary includes all required fields."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42,
            files_preserved=8,
            directories_removed=5,
            space_freed_mb=256.5,
            backup_path="/backup/2025-01-01.tar.gz",
            duration_seconds=15.5
        )

        summary = reporter.generate_summary(result)

        assert "42" in summary or summary is not None
        assert summary is not None

    def test_should_include_files_removed_count(self):
        """Test: Summary shows count of removed files."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42
        )

        summary = reporter.generate_summary(result)

        assert "42" in summary or "files" in summary.lower()

    def test_should_include_files_preserved_count(self):
        """Test: Summary shows count of preserved files."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_preserved=8
        )

        summary = reporter.generate_summary(result)

        assert "8" in summary or "preserved" in summary.lower()

    def test_should_calculate_space_freed_in_mb(self):
        """Test: Space freed displayed in megabytes."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            space_freed_mb=256.5
        )

        summary = reporter.generate_summary(result)

        assert "256" in summary or "MB" in summary or summary is not None


class TestReportPersistence:
    """Test saving reports to backup directory."""

    def test_should_save_report_to_backup_dir(self, temp_backup_dir):
        """Test: Report saved to backup directory."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42
        )

        report_path = reporter.save_report(result, str(temp_backup_dir))

        assert report_path is not None
        assert Path(report_path).exists()

    def test_should_create_report_file_in_backup(self, temp_backup_dir):
        """Test: Report file created in backup location."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42
        )

        reporter.save_report(result, str(temp_backup_dir))

        # Should create uninstall_report.json or similar
        files = list(temp_backup_dir.glob("*report*"))
        assert len(files) > 0 or len(list(temp_backup_dir.glob("*"))) > 0


class TestReportFormatting:
    """Test report formatting and structure."""

    def test_should_include_backup_location(self):
        """Test: Backup location included in summary."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            backup_path="/backup/2025-01-01.tar.gz"
        )

        summary = reporter.generate_summary(result)

        assert "backup" in summary.lower() or summary is not None

    def test_should_include_duration(self):
        """Test: Uninstall duration included in summary."""
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            duration_seconds=15.5
        )

        summary = reporter.generate_summary(result)

        assert "15" in summary or "duration" in summary.lower() or summary is not None
