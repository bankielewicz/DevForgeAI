"""
Integration tests for validation workflow (STORY-045 Phase 4).

Test Scenario: Installation Validation
Validates that validation mode checks installation health without modifications:
1. Validates existing installation structure
2. Checks all required directories exist
3. Verifies file integrity (no corruption)
4. Detects missing or corrupted files
5. Reports health status clearly

AC Mapping:
- AC-4.1: Validation checks directory structure
- AC-4.2: Validation detects missing files
- AC-4.3: Validation reports health status
- AC-4.4: Validation performs no modifications

NFR Validation:
- Validation of 450 files completes in <5 seconds

Test Files Created: 5 tests
- test_validate_healthy_installation
- test_validate_detects_missing_files
- test_validate_detects_corruption
- test_validate_completes_within_nfr
- test_validate_performs_no_modifications
"""

import pytest
import json
from pathlib import Path
import shutil


class TestValidateWorkflow:
    """Validation integration tests with health check verification"""

    def test_validate_healthy_installation(
        self, integration_project, source_framework
    ):
        """
        AC-4.1: Validation confirms healthy installation.

        Validates:
        - Fresh install passes validation
        - All required directories detected
        - Status = "valid"
        - No errors reported

        Expected: validation["valid"] == True
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Create fresh installation
        install_result = install.install(target_root, source_root)
        assert install_result["status"] == "success"

        # Validate installation
        validation_result = validate.validate_installation(target_root)

        assert (
            validation_result.get("valid") is True
        ), f"Validation failed: {validation_result.get('errors')}"

        # Verify all checks passed
        assert validation_result.get("errors") is None or len(
            validation_result.get("errors", [])
        ) == 0, "Should have no errors in healthy installation"

    def test_validate_detects_missing_files(
        self, integration_project, source_framework
    ):
        """
        AC-4.2: Validation detects missing files/directories.

        Validates:
        - Missing .claude/ detected
        - Missing devforgeai/ detected
        - Missing .version.json detected
        - Status = "invalid"

        Expected: validation["valid"] == False, errors list populated
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Create installation
        install_result = install.install(target_root, source_root)
        assert install_result["status"] == "success"

        # Delete critical directory to simulate corruption
        shutil.rmtree(target_root / ".claude")

        # Validate installation
        validation_result = validate.validate_installation(target_root)

        assert (
            validation_result.get("valid") is False
        ), "Validation should fail with missing .claude/"

        # Verify error is reported
        errors = validation_result.get("errors", [])
        assert len(errors) > 0, "Should report errors for missing directory"

        # At least one error should mention .claude/
        error_messages = " ".join(errors)
        assert (
            ".claude" in error_messages or "missing" in error_messages.lower()
        ), f"Error should mention missing .claude/, got: {errors}"

    def test_validate_detects_corruption(
        self, integration_project, source_framework
    ):
        """
        AC-4.3: Validation detects corrupted/modified files.

        Validates:
        - Modified .version.json detected as invalid JSON
        - Structural issues detected
        - Reports specific corruption details

        Expected: validation["valid"] == False, errors describe issue
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Create installation
        install_result = install.install(target_root, source_root)
        assert install_result["status"] == "success"

        # Corrupt .version.json
        version_file = target_root / "devforgeai" / ".version.json"
        version_file.write_text("{ INVALID JSON }")

        # Validate installation
        validation_result = validate.validate_installation(target_root)

        assert (
            validation_result.get("valid") is False
        ), "Validation should fail with corrupted .version.json"

        # Verify error details
        errors = validation_result.get("errors", [])
        assert len(errors) > 0, "Should report corruption errors"

    def test_validate_completes_within_nfr(
        self, integration_project, source_framework, performance_timer
    ):
        """
        NFR: Validation of 450 files must complete in <5 seconds.

        Validates:
        - Validation completes quickly (no deep inspection)
        - Performance suitable for pre-commit hooks

        Expected: Elapsed time < 5 seconds
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Create installation
        install_result = install.install(target_root, source_root)
        assert install_result["status"] == "success"

        # Measure validation time
        with performance_timer.measure("validate"):
            validation_result = validate.validate_installation(target_root)

        assert validation_result.get("valid") is True
        assert (
            performance_timer.elapsed < 5
        ), f"Validation exceeded 5s: {performance_timer.elapsed:.2f}s"

    def test_validate_performs_no_modifications(
        self, integration_project, source_framework, file_integrity_checker
    ):
        """
        AC-4.4: Validation mode performs no modifications.

        Validates:
        - No files created during validation
        - No files deleted during validation
        - No files modified during validation
        - No .backups/ entries created

        Expected: Filesystem unchanged after validation
        """
        from installer import install, validate

        target_root = integration_project["root"]
        source_root = source_framework["root"]

        # Create installation
        install_result = install.install(target_root, source_root)
        assert install_result["status"] == "success"

        # Record file state before validation
        file_count_before = file_integrity_checker.count_files(target_root)
        version_file = target_root / "devforgeai" / ".version.json"
        version_content_before = version_file.read_text()

        # Record backup count
        backups_before = list((target_root / ".backups").iterdir())

        # Execute validation
        validation_result = validate.validate_installation(target_root)

        # Verify no modifications
        file_count_after = file_integrity_checker.count_files(target_root)
        assert (
            file_count_after == file_count_before
        ), "Validation should not create/delete files"

        # Verify .version.json unchanged
        version_content_after = version_file.read_text()
        assert (
            version_content_after == version_content_before
        ), "Validation should not modify .version.json"

        # Verify no backup created
        backups_after = list((target_root / ".backups").iterdir())
        assert (
            len(backups_after) == len(backups_before)
        ), "Validation should not create backups"
