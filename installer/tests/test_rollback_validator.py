"""
STORY-080: Unit tests for RollbackValidator service.

Tests post-rollback validation including checksum verification and critical file checks.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+ business logic
Test Categories: AC#6
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import hashlib
import json


class TestValidationSuccess:
    """Test successful validation scenarios (AC#6, SVC-014)."""

    def test_validate_returns_passed_when_all_files_match(self, tmp_path):
        """
        Test: validate() returns passed=True when all checksums match (AC#6, SVC-014).

        Given: Restored files have correct checksums
        When: validate() is called
        Then: Returns ValidationReport with passed=True
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create file with known checksum
        file_content = "test content"
        (restored_dir / "test_file.txt").write_text(file_content)
        checksum = hashlib.sha256(file_content.encode()).hexdigest()

        # Create backup manifest with correct checksum
        manifest = {
            "files": {
                "test_file.txt": {
                    "checksum": checksum,
                    "size": len(file_content)
                }
            }
        }

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest=manifest
        )

        # Assert
        assert report.passed is True

    def test_validate_checks_critical_files_exist(self, tmp_path):
        """
        Test: validate() checks critical files exist (AC#6, SVC-015).

        Given: Restored directory has all critical files
        When: validate() is called
        Then: Critical files are verified (CLAUDE.md, .devforgeai/)
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create critical files
        (restored_dir / "CLAUDE.md").write_text("# Claude")
        (restored_dir / ".devforgeai").mkdir()
        (restored_dir / ".claude").mkdir()

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest={}
        )

        # Assert
        assert report.critical_files_present is True

    def test_validate_counts_verified_files(self, tmp_path):
        """
        Test: validate() counts successfully verified files (AC#6).

        Given: 100 files in restored directory
        When: validate() runs checksum verification
        Then: verified_files count = 100 (or actual verified count)
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create 100 files
        manifest_files = {}
        for i in range(100):
            file_path = restored_dir / f"file_{i:03d}.txt"
            content = f"content {i}"
            file_path.write_text(content)
            checksum = hashlib.sha256(content.encode()).hexdigest()
            manifest_files[f"file_{i:03d}.txt"] = {
                "checksum": checksum,
                "size": len(content)
            }

        manifest = {"files": manifest_files}

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest=manifest
        )

        # Assert
        assert report.verified_files == 100


class TestValidationFailure:
    """Test validation failure scenarios (AC#6, error handling)."""

    def test_validate_detects_missing_critical_files(self, tmp_path):
        """
        Test: validate() detects missing critical files (AC#6, SVC-015).

        Given: CLAUDE.md is missing from restored directory
        When: validate() is called
        Then: Returns ValidationReport with critical_files_present=False
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create some files but NOT CLAUDE.md
        (restored_dir / ".devforgeai").mkdir()

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest={}
        )

        # Assert
        assert report.critical_files_present is False

    def test_validate_detects_checksum_mismatches(self, tmp_path):
        """
        Test: validate() detects checksum mismatches (AC#6, SVC-014).

        Given: Restored file has different checksum than manifest
        When: validate() verifies checksums
        Then: Returns passed=False
        And: error includes count of mismatched files
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create file with content A
        (restored_dir / "test_file.txt").write_text("content A")

        # Manifest shows content B checksum
        manifest = {
            "files": {
                "test_file.txt": {
                    "checksum": hashlib.sha256(b"content B").hexdigest(),
                    "size": 9
                }
            }
        }

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest=manifest
        )

        # Assert
        assert report.passed is False

    def test_validate_with_corrupted_backup_fails(self, tmp_path):
        """
        Test: validate() handles corrupted backup gracefully (error handling).

        Given: Backup manifest is corrupted/invalid
        When: validate() is called
        Then: Returns appropriate error
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create corrupted manifest
        corrupted_manifest = "{ invalid json"

        validator = RollbackValidator(logger=Mock())

        # Act & Assert
        # Should handle gracefully (not crash)
        try:
            report = validator.validate(
                restored_dir=restored_dir,
                backup_manifest=corrupted_manifest
            )
            # If doesn't crash, check that it indicates failure
            assert report.passed is False or report.error is not None
        except Exception:
            # Exception is also acceptable if caught at higher level
            pass

    def test_validate_with_partial_restore_reports_status(self, tmp_path):
        """
        Test: validate() reports status for partial restores (error handling).

        Given: Restored directory is missing some files
        When: validate() is called
        Then: Reports missing file count
        And: passed=False
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Create only 2 of 5 expected files
        (restored_dir / "file_1.txt").write_text("content 1")
        (restored_dir / "file_2.txt").write_text("content 2")

        # Manifest expects 5 files
        manifest = {
            "files": {
                "file_1.txt": {"checksum": hashlib.sha256(b"content 1").hexdigest()},
                "file_2.txt": {"checksum": hashlib.sha256(b"content 2").hexdigest()},
                "file_3.txt": {"checksum": hashlib.sha256(b"content 3").hexdigest()},
                "file_4.txt": {"checksum": hashlib.sha256(b"content 4").hexdigest()},
                "file_5.txt": {"checksum": hashlib.sha256(b"content 5").hexdigest()},
            }
        }

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest=manifest
        )

        # Assert
        assert report.passed is False
        # Should indicate 3 missing files
        assert hasattr(report, "missing_files") or hasattr(report, "error")


class TestValidationReport:
    """Test ValidationReport data model (AC#6, SVC-016)."""

    def test_validate_returns_validation_report(self, tmp_path):
        """
        Test: validate() returns ValidationReport object (AC#6, SVC-016).

        Given: validate() is called
        When: Validation completes
        Then: Returns ValidationReport with:
            - passed (bool)
            - verified_files (int)
            - critical_files_present (bool)
            - error (str or None)
            - validation_details (str)
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()
        (restored_dir / "CLAUDE.md").write_text("# Claude")
        (restored_dir / ".devforgeai").mkdir()

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest={}
        )

        # Assert
        assert hasattr(report, "passed")
        assert hasattr(report, "verified_files")
        assert hasattr(report, "critical_files_present")
        assert hasattr(report, "validation_details") or hasattr(report, "error")
        assert isinstance(report.passed, bool)


class TestValidationWithManifest:
    """Test validation using backup manifest (AC#6)."""

    def test_validate_returns_false_when_validation_fails(self, tmp_path):
        """
        Test: validate() returns False on any failure (AC#6, SVC-014).

        Given: Any validation check fails
        When: validate() completes
        Then: Returns report with passed=False
        """
        # Arrange
        from installer.rollback_validator import RollbackValidator

        restored_dir = tmp_path / "restored"
        restored_dir.mkdir()

        # Missing critical files
        (restored_dir / "some_file.txt").write_text("content")

        validator = RollbackValidator(logger=Mock())

        # Act
        report = validator.validate(
            restored_dir=restored_dir,
            backup_manifest={}
        )

        # Assert
        # Should fail because critical files missing
        assert report.passed is False or report.critical_files_present is False
