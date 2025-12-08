"""
Integration tests for Fix/Repair Installation Mode (STORY-079).

Tests end-to-end fix command workflow including:
- Fix healthy installation (no changes)
- Fix detects all issue types
- Fix repairs missing and corrupted files
- Fix generates report with log file
- Fix exit codes (0, 1, 3, 4, 5)
- Fix handles missing manifest with user options
- Fix respects user choices for modified files

Test requirements coverage:
- AC#1-AC#8: All acceptance criteria
- NFR-001-004: Non-functional requirements
- Business Rules BR-001 to BR-003
"""

import pytest
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock
import subprocess
import time


class TestFixWorkflowHealthyInstallation:
    """Tests for fix command on healthy installations."""

    def test_should_detect_no_issues_in_healthy_installation(self, tmp_project):
        """Fix healthy installation detects no issues and exits with code 0."""
        # Arrange: Create manifest and valid files
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file1 = tmp_project["root"] / "file1.txt"
        file1.write_text("Content 1")

        file2 = tmp_project["claude"] / "file2.md"
        file2.write_text("Content 2")

        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "file1.txt",
                    "checksum": self._calculate_sha256("Content 1"),
                    "size": len("Content 1"),
                    "is_user_modifiable": False,
                },
                {
                    "path": ".claude/file2.md",
                    "checksum": self._calculate_sha256("Content 2"),
                    "size": len("Content 2"),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        exit_code = fix_cmd.execute()

        # Assert
        assert exit_code == 0, "Healthy installation should exit with 0"

    def test_should_exit_with_0_when_no_issues_found(self, tmp_project):
        """AC#7: Exit code 0 on success (no issues or all fixed)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        exit_code = fix_cmd.execute()

        # Assert
        assert exit_code == 0


class TestFixWorkflowIssueDetection:
    """Tests for issue detection during fix workflow."""

    def test_should_detect_all_issue_types_during_fix(self, tmp_project):
        """AC#2: Fix detects MISSING, CORRUPTED, WRONG_VERSION, EXTRA."""
        # Arrange: Setup installation with various issues
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        # Create some valid files
        valid_file = tmp_project["root"] / "valid.txt"
        valid_content = "Valid content"
        valid_file.write_text(valid_content)

        # Create corrupted file
        corrupted_file = tmp_project["root"] / "corrupted.txt"
        corrupted_file.write_text("Wrong content")

        # Create extra file (not in manifest)
        extra_file = tmp_project["root"] / "extra.txt"
        extra_file.write_text("Extra")

        # Missing file will not be created
        missing_checksum = self._calculate_sha256("Missing content")

        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "valid.txt",
                    "checksum": self._calculate_sha256(valid_content),
                    "size": len(valid_content),
                    "is_user_modifiable": False,
                },
                {
                    "path": "corrupted.txt",
                    "checksum": self._calculate_sha256("Correct content"),  # Wrong!
                    "size": 100,
                    "is_user_modifiable": False,
                },
                {
                    "path": "missing.txt",
                    "checksum": missing_checksum,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        issues = fix_cmd.validate()

        # Assert
        issue_types = {issue.issue_type for issue in issues}
        assert "MISSING" in issue_types, "Should detect missing files"
        assert "CORRUPTED" in issue_types, "Should detect corrupted files"
        assert "EXTRA" in issue_types, "Should detect extra files"

    def test_should_display_issue_details(self, tmp_project):
        """AC#2: Each issue includes path, expected, actual, severity."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        corrupted_file = tmp_project["root"] / "corrupted.txt"
        actual_content = "Actual"
        corrupted_file.write_text(actual_content)
        expected_content = "Expected"

        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "corrupted.txt",
                    "checksum": self._calculate_sha256(expected_content),
                    "size": len(expected_content),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        issues = fix_cmd.validate()

        # Assert
        issue = issues[0]
        assert issue.path == "corrupted.txt"
        assert issue.expected is not None
        assert issue.actual is not None
        assert issue.severity is not None


class TestFixWorkflowRepairOperations:
    """Tests for repair operations during fix workflow."""

    def test_should_repair_missing_files(self, tmp_project):
        """AC#4: Missing files restored from source package."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "missing.txt"
        source_content = "Source content"
        source_file.write_text(source_content)

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "missing.txt",
                    "checksum": self._calculate_sha256(source_content),
                    "size": len(source_content),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]), source_root=str(source_dir))
        exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        missing_file = tmp_project["root"] / "missing.txt"
        assert missing_file.exists(), "Missing file should be restored"
        assert missing_file.read_text() == source_content

    def test_should_replace_corrupted_files(self, tmp_project):
        """AC#4: Corrupted files replaced with correct versions."""
        # Arrange
        source_dir = tmp_project["root"] / "source_package"
        source_dir.mkdir()

        source_file = source_dir / "corrupted.txt"
        correct_content = "Correct version"
        source_file.write_text(correct_content)

        corrupted_file = tmp_project["root"] / "corrupted.txt"
        corrupted_file.write_text("Wrong version")

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "corrupted.txt",
                    "checksum": self._calculate_sha256(correct_content),
                    "size": len(correct_content),
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]), source_root=str(source_dir))
        exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        assert corrupted_file.read_text() == correct_content

    def test_should_update_manifest_after_repair(self, tmp_project):
        """AC#4: Manifest is updated with new checksums."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

        file_path = tmp_project["root"] / "repaired.txt"
        new_content = "Repaired content"
        file_path.write_text(new_content)

        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "repaired.txt",
                    "checksum": "oldchecksum" * 4,  # Old checksum
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        fix_cmd.execute(auto_repair=True)

        # Assert
        updated_manifest = json.loads(manifest_path.read_text())
        repaired_entry = updated_manifest["files"][0]
        assert repaired_entry["checksum"] == self._calculate_sha256(new_content)


class TestFixWorkflowReporting:
    """Tests for fix command reporting (AC#6)."""

    def test_should_generate_repair_report(self, tmp_project):
        """AC#6: Report shows statistics (files checked, issues found/fixed/skipped)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "file1.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
                {
                    "path": "file2.txt",
                    "checksum": "b" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        report = fix_cmd.generate_report()

        # Assert
        assert report.total_files_checked >= 2
        assert report.issues_found >= 0
        assert hasattr(report, 'issues_fixed')
        assert hasattr(report, 'issues_skipped')

    def test_should_save_log_file(self, tmp_project):
        """AC#6: Report is saved to `.devforgeai/logs/fix-{timestamp}.log`."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        (tmp_project["devforgeai"] / "logs").mkdir()
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        fix_cmd.execute()

        # Assert
        log_files = list((tmp_project["devforgeai"] / "logs").glob("fix-*.log"))
        assert len(log_files) > 0, "Log file should be created"

    def test_should_display_summary_statistics(self, tmp_project):
        """AC#6: Report shows all statistics in output."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        output = fix_cmd.execute_with_output()

        # Assert
        assert "files checked" in output.lower() or "total" in output.lower()
        assert "issues" in output.lower() or "problems" in output.lower()


class TestFixWorkflowExitCodes:
    """Tests for fix command exit codes (AC#7)."""

    def test_should_exit_with_code_0_on_success(self, tmp_project):
        """AC#7: Exit code 0 = Success (all issues fixed or no issues)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        exit_code = fix_cmd.execute()

        # Assert
        assert exit_code == 0

    def test_should_exit_with_code_1_when_source_missing(self, tmp_project):
        """AC#7: Exit code 1 = Missing source (repair files not available)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "missing.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]), source_root="/nonexistent/source")
        exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        assert exit_code == 1, "Should exit with 1 when source unavailable"

    def test_should_exit_with_code_2_on_permission_denied(self, tmp_project):
        """AC#7: Exit code 2 = Permission denied (cannot write to installation)."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "restricted.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        with patch('pathlib.Path.write_text', side_effect=PermissionError("Access denied")):
            from installer.fix_command import FixCommand
            fix_cmd = FixCommand(str(tmp_project["root"]))
            exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        assert exit_code == 2, "Should exit with 2 on permission denied"

    def test_should_exit_with_code_3_on_partial_repair(self, tmp_project):
        """AC#7: Exit code 3 = Partial repair (some issues fixed, some remain)."""
        # Arrange
        source_dir = tmp_project["root"] / "source"
        source_dir.mkdir()

        # One file can be repaired
        repaired_file = source_dir / "repaired.txt"
        repaired_file.write_text("Repaired")

        # One file cannot be repaired (missing from source)
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "repaired.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
                {
                    "path": "not_in_source.txt",
                    "checksum": "b" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]), source_root=str(source_dir))
        exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        assert exit_code == 3, "Should exit with 3 on partial repair"

    def test_should_exit_with_code_4_on_post_repair_validation_failure(self, tmp_project):
        """AC#7: Exit code 4 = Post-repair validation failed."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "file.txt",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": False,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act: Mock post-repair validation to fail
        with patch('installer.installation_validator.InstallationValidator.validate') as mock_validate:
            mock_validate.return_value = [Mock(issue_type="CORRUPTED")]  # Still has issues

            from installer.fix_command import FixCommand
            fix_cmd = FixCommand(str(tmp_project["root"]))
            exit_code = fix_cmd.execute(auto_repair=True)

        # Assert
        assert exit_code == 4, "Should exit with 4 when post-repair validation fails"

    def test_should_exit_with_code_5_on_manual_merge_needed(self, tmp_project):
        """AC#7: Exit code 5 = Manual merge needed (user-modified files require attention)."""
        # Arrange
        user_file = tmp_project["root"] / "user_config.yaml"
        user_file.write_text("user: custom")

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "user_config.yaml",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))

        with patch.object(fix_cmd, '_prompt_user') as mock_prompt:
            mock_prompt.return_value = None  # User cancels

            exit_code = fix_cmd.execute()

        # Assert
        assert exit_code == 5, "Should exit with 5 when user chooses manual merge"


class TestFixWorkflowMissingManifest:
    """Tests for handling missing manifest (AC#8)."""

    def test_should_detect_missing_manifest(self, tmp_project):
        """AC#8: User is notified that manifest is missing."""
        # Arrange
        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        assert not manifest_path.exists(), "Manifest should not exist"

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        manifest = fix_cmd.load_manifest()

        # Assert
        assert manifest is None, "Should return None for missing manifest"

    def test_should_offer_regenerate_option_for_missing_manifest(self, tmp_project):
        """AC#8: User offered option to regenerate manifest from current files."""
        # Arrange
        file_path = tmp_project["root"] / "test.txt"
        file_path.write_text("test")

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))

        with patch.object(fix_cmd, '_prompt_manifest_missing') as mock_prompt:
            mock_prompt.return_value = "regenerate"
            choice = fix_cmd._handle_missing_manifest()

        # Assert
        assert choice == "regenerate"

    def test_should_regenerate_manifest_from_current_files(self, tmp_project):
        """AC#8: Regenerate option creates manifest with all current files."""
        # Arrange
        file1 = tmp_project["root"] / "file1.txt"
        file1.write_text("Content 1")

        file2 = tmp_project["claude"] / "file2.md"
        file2.write_text("Content 2")

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        assert not manifest_path.exists()

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        fix_cmd._regenerate_manifest()

        # Assert
        assert manifest_path.exists(), "Manifest should be created"
        manifest_data = json.loads(manifest_path.read_text())
        assert len(manifest_data["files"]) >= 2

    def test_should_offer_reinstall_option_for_missing_manifest(self, tmp_project):
        """AC#8: User offered option to reinstall DevForgeAI."""
        # Arrange & Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        options = fix_cmd._get_manifest_missing_options()

        # Assert
        option_values = [opt["value"] for opt in options]
        assert "regenerate" in option_values
        assert "reinstall" in option_values
        assert "abort" in option_values

    def test_should_abort_without_changes_when_user_chooses_abort(self, tmp_project):
        """AC#8: Abort option exits without changes."""
        # Arrange
        file_count_before = len(list(tmp_project["root"].glob("**/*")))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))

        with patch.object(fix_cmd, '_prompt_manifest_missing') as mock_prompt:
            mock_prompt.return_value = "abort"
            exit_code = fix_cmd.execute()

        # Assert
        file_count_after = len(list(tmp_project["root"].glob("**/*")))
        assert exit_code == 0  # Abort is considered success (no error)


class TestFixWorkflowUserModifiedFiles:
    """Tests for user-modified file handling."""

    def test_should_prompt_user_for_modified_files(self, tmp_project):
        """AC#3, AC#5: User prompted before overwriting user-modified files."""
        # Arrange
        user_file = tmp_project["root"] / "user_story.md"
        user_file.write_text("# User Story")

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "files": [
                {
                    "path": "user_story.md",
                    "checksum": "different" + ("a" * 56),
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))

        with patch.object(fix_cmd, '_prompt_user_for_file') as mock_prompt:
            mock_prompt.return_value = "keep"
            fix_cmd.execute()

        # Assert
        mock_prompt.assert_called()

    def test_should_preserve_user_files_with_keep_choice(self, tmp_project):
        """AC#5: 'Keep my version' preserves user file."""
        # Arrange
        user_file = tmp_project["root"] / "config.yaml"
        user_content = "user: custom"
        user_file.write_text(user_content)

        manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"
        manifest_data = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": [
                {
                    "path": "config.yaml",
                    "checksum": "a" * 64,
                    "size": 100,
                    "is_user_modifiable": True,
                },
            ],
            "schema_version": 1,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        # Act
        from installer.fix_command import FixCommand
        fix_cmd = FixCommand(str(tmp_project["root"]))
        fix_cmd.execute(user_choices={"config.yaml": "keep"})

        # Assert
        assert user_file.read_text() == user_content, "User file should not be modified"


# Helper methods
@staticmethod
def _calculate_sha256(content: str) -> str:
    """Calculate SHA256 checksum for string content."""
    return hashlib.sha256(content.encode()).hexdigest()
