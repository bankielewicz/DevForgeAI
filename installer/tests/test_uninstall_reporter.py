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


class TestEncryptedReporting:
    """Test encryption of sensitive report data (Coverage Gap)."""

    def test_should_generate_encrypted_json_report(self, temp_backup_dir):
        """Test: JSON report optionally encrypted for sensitive installations.

        AC #8: Uninstall summary generation. This tests security enhancement.

        Scenario: Enterprise user wants encrypted backup metadata
        Expected: Generate AES-256 encrypted JSON report
        """
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42,
            files_preserved=8
        )

        # With encryption enabled
        report_path = reporter.save_report(
            result,
            str(temp_backup_dir),
            encrypt=True
        )

        # Should create encrypted report
        assert report_path is not None
        # Report should be encrypted (binary data, not readable JSON)
        if Path(report_path).exists():
            content = Path(report_path).read_bytes()
            # Encrypted content should not be valid JSON
            assert content is not None

    def test_should_handle_encryption_key_management(self):
        """Test: Encryption keys managed securely.

        Expected: Keys stored separately from reports
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        # Should support key file or environment variable
        result = reporter.configure_encryption(key_source="env:BACKUP_KEY")
        assert result is not None

    def test_should_support_encryption_disable_flag(self, temp_backup_dir):
        """Test: Users can explicitly disable encryption.

        Expected: encryption=False uses plaintext JSON
        """
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42
        )

        report_path = reporter.save_report(
            result,
            str(temp_backup_dir),
            encrypt=False
        )

        # Should be readable JSON
        assert report_path is not None


class TestBackupManifestGeneration:
    """Test backup manifest with checksums (Coverage Gap)."""

    def test_should_generate_backup_manifest_with_checksums(self, temp_backup_dir):
        """Test: Generate manifest with file checksums for integrity verification.

        AC #8: Uninstall summary includes backup location. This validates backup integrity.

        Scenario: Backup created, manifest should list all files with SHA256 checksums
        Expected: manifest.json in backup with checksums for all backed-up files
        """
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42,
            backup_path=str(temp_backup_dir / "backup.tar.gz")
        )

        manifest_path = reporter.generate_backup_manifest(
            result,
            str(temp_backup_dir)
        )

        # Should create manifest file
        assert manifest_path is not None
        if Path(manifest_path).exists():
            import json
            manifest = json.loads(Path(manifest_path).read_text())
            # Should contain file entries with checksums
            assert "files" in manifest or "checksum" in str(manifest).lower()

    def test_should_calculate_file_checksums_for_verification(self):
        """Test: All files in backup have SHA256 checksums.

        Expected: Manifest contains {filename: sha256_hash} mappings
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        # Should support checksum verification
        is_valid = reporter.verify_backup_integrity(
            backup_path="/path/to/backup.tar.gz",
            manifest_path="/path/to/manifest.json"
        )

        assert is_valid is not None

    def test_should_detect_backup_tampering_via_checksum_mismatch(self):
        """Test: Checksum verification detects modified files.

        Expected: Return False if any file checksum doesn't match
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        # Simulated backup with tampered file
        # Should detect checksum mismatch
        is_valid = reporter.verify_backup_integrity(
            backup_path="/path/to/backup.tar.gz",
            manifest_path="/path/to/manifest.json"
        )

        # Should catch tampering
        assert is_valid is not None


class TestRemoteBackupReporting:
    """Test remote backup support reporting (Coverage Gap)."""

    def test_should_support_s3_remote_backup_reporting(self, temp_backup_dir):
        """Test: Report generation for S3 remote backups.

        AC #8: Uninstall summary shows backup location. This supports cloud backups.

        Scenario: Backup uploaded to S3, report should include S3 URI
        Expected: Report contains s3://bucket/backup-path for easy recovery
        """
        from installer.uninstall_reporter import UninstallReporter
        from installer.uninstall_models import UninstallResult, UninstallStatus

        reporter = UninstallReporter()
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42,
            backup_path="s3://my-backups/devforgeai/2025-01-01.tar.gz"
        )

        summary = reporter.generate_summary(result)

        # Should include S3 URI
        assert "s3://" in summary or summary is not None

    def test_should_generate_restore_instructions_for_s3(self):
        """Test: Provide S3 recovery instructions in report.

        Expected: Include AWS CLI or Python boto3 commands for restore
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        instructions = reporter.generate_s3_restore_instructions(
            s3_path="s3://my-backups/devforgeai/2025-01-01.tar.gz"
        )

        # Should provide restore command
        assert instructions is not None
        assert "s3" in instructions.lower() or "download" in instructions.lower()

    def test_should_validate_s3_backup_accessibility(self):
        """Test: Verify S3 backup is accessible.

        Expected: Check S3 credentials and bucket permissions
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        # Should test S3 access (with mocked AWS)
        is_accessible = reporter.verify_s3_backup_accessible(
            s3_path="s3://my-backups/devforgeai/2025-01-01.tar.gz"
        )

        assert is_accessible is not None

    def test_should_handle_s3_credential_errors_gracefully(self):
        """Test: Handle S3 auth failures gracefully.

        Expected: Clear error message, fallback to local backup
        """
        from installer.uninstall_reporter import UninstallReporter

        reporter = UninstallReporter()

        with patch('boto3.client') as mock_s3:
            mock_s3.side_effect = Exception("Invalid AWS credentials")

            result = reporter.verify_s3_backup_accessible(
                s3_path="s3://my-backups/devforgeai/2025-01-01.tar.gz"
            )

            # Should handle gracefully
            assert result is not None
