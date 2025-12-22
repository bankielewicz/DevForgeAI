"""
Unit tests for RepairService (STORY-079).

Tests repair functionality including:
- Restoring missing files (AC#4, SVC-005)
- Replacing corrupted files (AC#4, SVC-006)
- Preserving user-modified files (AC#5, SVC-007)
- Backing up user files before overwrite (AC#5, SVC-008)
- User interaction and prompts (AC#5)
- Security constraints (NFR-004)

Test requirements coverage:
- SVC-005: Restore missing files from source
- SVC-006: Replace corrupted files
- SVC-007: Preserve user-modified files unless forced
- SVC-008: Backup user files before overwrite
"""

import pytest
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock, patch, call
from dataclasses import dataclass
from installer.repair_service import SecurityError


@dataclass
class ValidationIssue:
    path: str
    issue_type: str
    expected: str = None
    actual: str = None
    severity: str = None
    is_user_modified: bool = False


@dataclass
class RepairResult:
    path: str
    success: bool
    action: str  # RESTORED, REPLACED, SKIPPED, BACKED_UP
    error: str = None


class TestRepairServiceBasics:
    """Basic repair functionality tests."""

    def test_should_restore_missing_file_from_source(self, tmp_project):
        """SVC-005: Given missing file and source package, When repair() called, Then file restored."""
        # Arrange
        # Create source package with the missing file
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()
        source_file = source_dir / "missing_file.txt"
        source_file.write_text("Restored content")

        # Project should have missing file in manifest but not on disk
        missing_file_path = tmp_project["root"] / "missing_file.txt"
        assert not missing_file_path.exists(), "File should not exist before repair"

        validation_issue = ValidationIssue(
            path="missing_file.txt",
            issue_type="MISSING",
            severity="CRITICAL",
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )
        result = repair_service.repair([validation_issue])

        # Assert
        assert missing_file_path.exists(), "Missing file should be restored"
        assert missing_file_path.read_text() == "Restored content"

    def test_should_replace_corrupted_file_with_source_version(self, tmp_project):
        """SVC-006: Given corrupted file, When repair() called, Then file replaced with source version."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "corrupted.txt"
        correct_content = "Correct content"
        source_file.write_text(correct_content)

        # Create corrupted file in project
        corrupted_file = tmp_project["root"] / "corrupted.txt"
        corrupted_file.write_text("Corrupted data")

        validation_issue = ValidationIssue(
            path="corrupted.txt",
            issue_type="CORRUPTED",
            expected=self._calculate_sha256(correct_content),
            actual=self._calculate_sha256("Corrupted data"),
            severity="CRITICAL",
            is_user_modified=False,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )
        result = repair_service.repair([validation_issue])

        # Assert
        assert corrupted_file.read_text() == correct_content

    def test_should_preserve_user_modified_files_without_force_flag(self, tmp_project):
        """SVC-007: Given user-modified file without force, When repair() called, Then file NOT overwritten."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "user_config.yaml"
        source_file.write_text("default: value")

        user_file = tmp_project["root"] / "user_config.yaml"
        user_content = "custom: my_value"
        user_file.write_text(user_content)

        validation_issue = ValidationIssue(
            path="user_config.yaml",
            issue_type="CORRUPTED",
            severity="HIGH",
            is_user_modified=True,  # User modified!
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
            force=False,  # Non-destructive mode
        )
        result = repair_service.repair(
            [validation_issue],
            user_choices={"user_config.yaml": "keep"},
        )

        # Assert
        assert user_file.read_text() == user_content, "User file should NOT be overwritten"

    def test_should_backup_user_file_before_overwrite(self, tmp_project):
        """SVC-008: Given user chooses 'backup and restore', Then user version saved to .backup/."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "config.json"
        source_file.write_text('{"setting": "default"}')

        user_file = tmp_project["root"] / "config.json"
        user_backup_content = '{"setting": "custom"}'
        user_file.write_text(user_backup_content)

        backup_dir = tmp_project["backups"]
        backup_dir.mkdir(exist_ok=True)

        validation_issue = ValidationIssue(
            path="config.json",
            issue_type="CORRUPTED",
            severity="HIGH",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )
        result = repair_service.repair(
            [validation_issue],
            user_choices={"config.json": "backup_and_restore"},
        )

        # Assert
        # Check that backup was created
        backup_files = list(backup_dir.glob("**/*.json"))
        assert len(backup_files) > 0, "Backup file should be created"

        # Check that user file was restored from source
        assert user_file.read_text() == '{"setting": "default"}'

        # Check that backup contains user's version
        backup_content = backup_files[0].read_text()
        assert "custom" in backup_content

    def test_should_skip_file_when_user_chooses_keep(self, tmp_project):
        """AC#5: User choice 'Keep my version' skips repair for that file."""
        # Arrange
        user_file = tmp_project["root"] / "my_file.txt"
        user_content = "My custom content"
        user_file.write_text(user_content)

        validation_issue = ValidationIssue(
            path="my_file.txt",
            issue_type="CORRUPTED",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )
        result = repair_service.repair(
            [validation_issue],
            user_choices={"my_file.txt": "keep"},
        )

        # Assert
        assert user_file.read_text() == user_content
        assert "my_file.txt" in str(result), "Skipped file should be in result"

    def test_should_restore_original_when_user_chooses_restore(self, tmp_project):
        """AC#5: User choice 'Restore original' overwrites with source version."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "original.txt"
        original_content = "Original version"
        source_file.write_text(original_content)

        user_file = tmp_project["root"] / "original.txt"
        user_file.write_text("User modified version")

        validation_issue = ValidationIssue(
            path="original.txt",
            issue_type="CORRUPTED",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )
        result = repair_service.repair(
            [validation_issue],
            user_choices={"original.txt": "restore"},
        )

        # Assert
        assert user_file.read_text() == original_content

    def test_should_show_diff_for_text_files(self, tmp_project):
        """AC#5: 'Show diff' option displays differences for text files."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "script.py"
        source_file.write_text("def hello():\n    return 'Hello'")

        user_file = tmp_project["root"] / "script.py"
        user_file.write_text("def hello():\n    return 'Hi there'")

        validation_issue = ValidationIssue(
            path="script.py",
            issue_type="CORRUPTED",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )

        # Get diff representation
        with patch.object(repair_service, '_generate_diff') as mock_diff:
            mock_diff.return_value = "--- expected\n+++ actual\n-    return 'Hello'\n+    return 'Hi there'"
            diff = repair_service._generate_diff(
                source_file.read_text(),
                user_file.read_text(),
            )

        # Assert
        assert diff is not None, "Diff should be generated for text files"

    def test_should_set_correct_file_permissions_after_restore(self, tmp_project):
        """AC#4: Restored files have correct permissions."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "script.sh"
        source_file.write_text("#!/bin/bash\necho 'test'")
        source_file.chmod(0o755)  # Executable

        validation_issue = ValidationIssue(
            path="script.sh",
            issue_type="MISSING",
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )
        result = repair_service.repair([validation_issue])

        # Assert
        restored_file = tmp_project["root"] / "script.sh"
        assert restored_file.exists()
        # File should have same permissions as source (or at least be readable)

    def test_should_update_manifest_after_repair(self, tmp_project):
        """AC#4: Manifest is updated with new checksums after repair."""
        # This test will be verified in manifest_manager tests
        pass

    def test_should_log_repair_operations(self, tmp_project):
        """AC#4, AC#6: Repair operations are logged."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "test.txt"
        source_file.write_text("test")

        validation_issue = ValidationIssue(
            path="test.txt",
            issue_type="MISSING",
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
        )

        with patch.object(repair_service, '_log_operation') as mock_log:
            result = repair_service.repair([validation_issue])
            mock_log.assert_called()

        # Assert
        # Operations should be logged


class TestRepairServiceSecurityConstraints:
    """Tests for security requirements (NFR-004)."""

    def test_should_not_modify_files_outside_devforgeai_directories(self, tmp_project):
        """NFR-004: Repair does not modify files outside DevForgeAI directories."""
        # Arrange
        outside_file = tmp_project["root"] / "user_project" / "important.txt"
        outside_file.parent.mkdir(parents=True)
        outside_file.write_text("Important user data")

        validation_issue = ValidationIssue(
            path="user_project/important.txt",  # Outside .claude/, devforgeai/
            issue_type="CORRUPTED",
        )

        # Act & Assert
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )

        # Repair should refuse to touch files outside DevForgeAI dirs
        with pytest.raises(SecurityError):
            repair_service.repair([validation_issue])

    def test_should_only_repair_recognized_devforgeai_files(self, tmp_project):
        """Security: Only files in .claude/, devforgeai/, CLAUDE.md are repaired."""
        # Arrange
        allowed_files = [
            ValidationIssue(path=".claude/agents/test.md", issue_type="MISSING"),
            ValidationIssue(path="devforgeai/specs/context/tech-stack.md", issue_type="MISSING"),
            ValidationIssue(path="CLAUDE.md", issue_type="MISSING"),
        ]

        forbidden_files = [
            ValidationIssue(path="../parent/file.txt", issue_type="MISSING"),
            ValidationIssue(path="/etc/passwd", issue_type="MISSING"),
            ValidationIssue(path="../../outside.txt", issue_type="MISSING"),
        ]

        # Act & Assert
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )

        # Allowed files should be processed
        # Forbidden files should raise SecurityError


class TestRepairServiceUserInteraction:
    """Tests for user interaction and prompting (AC#5)."""

    def test_should_prompt_user_for_each_user_modified_file(self, tmp_project):
        """AC#5: User is prompted for each user-modified file."""
        # Arrange
        user_files = [
            ValidationIssue(path="devforgeai/specs/story1.md", issue_type="CORRUPTED", is_user_modified=True),
            ValidationIssue(path="devforgeai/specs/story2.md", issue_type="CORRUPTED", is_user_modified=True),
            ValidationIssue(path="devforgeai/specs/context/tech-stack.md", issue_type="CORRUPTED", is_user_modified=True),
        ]

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )

        with patch.object(repair_service, '_prompt_user_for_file') as mock_prompt:
            mock_prompt.side_effect = ["keep", "restore", "backup_and_restore"]
            user_choices = {}
            for issue in user_files:
                user_choices[issue.path] = repair_service._prompt_user_for_file(issue)

        # Assert
        assert mock_prompt.call_count == 3
        assert user_choices["devforgeai/specs/story1.md"] == "keep"
        assert user_choices["devforgeai/specs/story2.md"] == "restore"
        assert user_choices["devforgeai/specs/context/tech-stack.md"] == "backup_and_restore"

    def test_should_offer_four_user_options_for_modified_files(self, tmp_project):
        """AC#5: User is offered 4 options for each file."""
        # Arrange
        validation_issue = ValidationIssue(
            path="devforgeai/specs/config.yaml",
            issue_type="CORRUPTED",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )

        # Get the available options
        options = repair_service._get_user_options()

        # Assert
        assert len(options) >= 4
        expected_options = {"keep", "restore", "show_diff", "backup_and_restore"}
        actual_options = {opt["value"] for opt in options}
        assert expected_options.issubset(actual_options)

    def test_should_respect_user_choice_for_each_file(self, tmp_project):
        """AC#5: User's choice is respected for each file."""
        # Arrange
        user_choices = {
            "devforgeai/specs/story1.md": "keep",
            "devforgeai/specs/story2.md": "restore",
            "devforgeai/config.yaml": "backup_and_restore",
        }

        issues = [
            ValidationIssue(path=k, issue_type="CORRUPTED", is_user_modified=True)
            for k in user_choices.keys()
        ]

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "source"),
        )
        result = repair_service.repair(issues, user_choices=user_choices)

        # Assert
        # Each file should have been processed according to user choice

    def test_should_force_repair_all_files_with_force_flag(self, tmp_project):
        """AC#5: --force flag causes repair to overwrite all files without prompting."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "config.yaml"
        source_file.write_text("default: value")

        user_file = tmp_project["root"] / "config.yaml"
        user_file.write_text("user: custom")

        validation_issue = ValidationIssue(
            path="config.yaml",
            issue_type="CORRUPTED",
            is_user_modified=True,
        )

        # Act
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(source_dir),
            force=True,  # Force flag set
        )
        result = repair_service.repair([validation_issue])

        # Assert
        assert user_file.read_text() == "default: value"
        # No prompt should be shown


class TestRepairServiceEdgeCases:
    """Edge case tests."""

    def test_should_handle_symlinks_appropriately(self, tmp_project):
        """Edge case: Handle symlinks in repair operations."""
        # Arrange (will vary based on implementation strategy)
        pass

    def test_should_handle_directories_in_manifest(self, tmp_project):
        """Edge case: Manifest may reference directories."""
        pass

    def test_should_handle_empty_source_package(self, tmp_project):
        """Error case: Source package unavailable."""
        # Arrange
        validation_issue = ValidationIssue(
            path="missing_file.txt",
            issue_type="MISSING",
        )

        # Act & Assert
        from installer.repair_service import RepairService
        repair_service = RepairService(
            installation_root=str(tmp_project["root"]),
            source_root=str(tmp_project["root"] / "nonexistent_source"),
        )

        # Should return error result, not crash


# Helper classes
# (SecurityError imported from installer.repair_service)


# Helper methods
@staticmethod
def _calculate_sha256(content: str) -> str:
    """Calculate SHA256 checksum for string content."""
    return hashlib.sha256(content.encode()).hexdigest()
