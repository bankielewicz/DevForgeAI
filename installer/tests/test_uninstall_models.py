"""
Unit tests for uninstall data models.
Tests UninstallRequest, UninstallPlan, UninstallResult, and Enums.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class TestUninstallModeEnum:
    """Test UninstallMode enumeration."""

    def test_should_have_complete_mode(self):
        """Test: UninstallMode has COMPLETE value."""
        # This will FAIL - UninstallMode not implemented
        from installer.uninstall_models import UninstallMode
        assert hasattr(UninstallMode, 'COMPLETE')
        assert UninstallMode.COMPLETE.value == "COMPLETE"

    def test_should_have_preserve_user_content_mode(self):
        """Test: UninstallMode has PRESERVE_USER_CONTENT value."""
        from installer.uninstall_models import UninstallMode
        assert hasattr(UninstallMode, 'PRESERVE_USER_CONTENT')
        assert UninstallMode.PRESERVE_USER_CONTENT.value == "PRESERVE_USER_CONTENT"

    def test_should_preserve_user_content_be_default(self):
        """Test: Default mode is PRESERVE_USER_CONTENT."""
        from installer.uninstall_models import UninstallRequest
        request = UninstallRequest()
        assert request.mode == "PRESERVE_USER_CONTENT"


class TestContentTypeEnum:
    """Test ContentType enumeration."""

    def test_should_have_framework_type(self):
        """Test: ContentType has FRAMEWORK value."""
        from installer.uninstall_models import ContentType
        assert hasattr(ContentType, 'FRAMEWORK')

    def test_should_have_user_content_type(self):
        """Test: ContentType has USER_CONTENT value."""
        from installer.uninstall_models import ContentType
        assert hasattr(ContentType, 'USER_CONTENT')

    def test_should_have_modified_framework_type(self):
        """Test: ContentType has MODIFIED_FRAMEWORK value."""
        from installer.uninstall_models import ContentType
        assert hasattr(ContentType, 'MODIFIED_FRAMEWORK')


class TestUninstallRequest:
    """Test UninstallRequest data model."""

    def test_should_create_with_default_values(self):
        """Test: UninstallRequest instantiates with correct defaults."""
        from installer.uninstall_models import UninstallRequest
        request = UninstallRequest()

        assert request.mode == "PRESERVE_USER_CONTENT"
        assert request.dry_run is False
        assert request.skip_backup is False
        assert request.skip_confirmation is False

    def test_should_create_with_custom_values(self):
        """Test: UninstallRequest accepts custom values."""
        from installer.uninstall_models import UninstallRequest
        request = UninstallRequest(
            mode="COMPLETE",
            dry_run=True,
            skip_backup=True,
            skip_confirmation=True
        )

        assert request.mode == "COMPLETE"
        assert request.dry_run is True
        assert request.skip_backup is True
        assert request.skip_confirmation is True


class TestUninstallPlan:
    """Test UninstallPlan data model."""

    def test_should_initialize_empty_lists(self):
        """Test: UninstallPlan initializes with empty collections."""
        from installer.uninstall_models import UninstallPlan
        plan = UninstallPlan()

        assert plan.files_to_remove == []
        assert plan.files_to_preserve == []
        assert plan.directories_to_remove == []
        assert plan.total_size_bytes == 0

    def test_should_accumulate_file_entries(self):
        """Test: UninstallPlan collects file entries correctly."""
        from installer.uninstall_models import UninstallPlan
        plan = UninstallPlan()
        plan.files_to_remove = ["/path/file1.py", "/path/file2.py"]

        assert len(plan.files_to_remove) == 2
        assert "/path/file1.py" in plan.files_to_remove


class TestUninstallResult:
    """Test UninstallResult data model."""

    def test_should_create_with_success_status(self):
        """Test: UninstallResult accepts SUCCESS status."""
        from installer.uninstall_models import UninstallResult, UninstallStatus
        result = UninstallResult(status=UninstallStatus.SUCCESS)

        assert result.status == UninstallStatus.SUCCESS

    def test_should_track_files_removed(self):
        """Test: UninstallResult tracks file removal count."""
        from installer.uninstall_models import UninstallResult, UninstallStatus
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            files_removed=42,
            files_preserved=8
        )

        assert result.files_removed == 42
        assert result.files_preserved == 8

    def test_should_track_space_freed(self):
        """Test: UninstallResult calculates space freed in MB."""
        from installer.uninstall_models import UninstallResult, UninstallStatus
        result = UninstallResult(
            status=UninstallStatus.SUCCESS,
            space_freed_mb=256.5
        )

        assert result.space_freed_mb == 256.5

    def test_should_collect_errors(self):
        """Test: UninstallResult collects error messages."""
        from installer.uninstall_models import UninstallResult, UninstallStatus
        result = UninstallResult(
            status=UninstallStatus.PARTIAL,
            errors=["Permission denied on /path/file1", "File not found"]
        )

        assert len(result.errors) == 2
        assert "Permission denied" in result.errors[0]
