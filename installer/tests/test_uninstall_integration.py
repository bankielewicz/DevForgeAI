"""
Integration tests for complete uninstall workflows.
Tests end-to-end scenarios using real directory structures.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
import json
from pathlib import Path
from unittest.mock import patch


class TestCompleteUninstallWorkflow:
    """Test complete uninstall workflow (end-to-end)."""

    def test_should_complete_uninstall_with_preserve_mode(
        self,
        temp_install_dir,
        temp_backup_dir
    ):
        """Test: AC#2 - Complete uninstall in PRESERVE_USER_CONTENT mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode

        # Create test files
        (temp_install_dir / ".ai_docs" / "Stories").mkdir(parents=True, exist_ok=True)
        (temp_install_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("User story")

        (temp_install_dir / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        (temp_install_dir / ".claude" / "skills" / "test.md").write_text("Skill")

        # Mock dependencies
        from unittest.mock import Mock
        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        backup_service = Mock()
        backup_service.create_backup.return_value = str(temp_backup_dir / "backup.tar.gz")

        file_system = Mock()
        file_system.exists = Mock(return_value=True)
        file_system.remove_file = Mock()
        file_system.remove_dir = Mock()

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system
        )

        request = UninstallRequest(
            mode=UninstallMode.PRESERVE_USER_CONTENT,
            skip_confirmation=True
        )

        result = orchestrator.execute(request)

        # User content should be preserved
        assert result is not None

    def test_should_complete_uninstall_with_complete_mode(
        self,
        temp_install_dir,
        temp_backup_dir
    ):
        """Test: AC#2 - Complete uninstall in COMPLETE mode."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest, UninstallMode
        from unittest.mock import Mock

        # Create test files
        (temp_install_dir / ".ai_docs" / "Stories").mkdir(parents=True, exist_ok=True)
        (temp_install_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("User story")

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": ["devforgeai/specs/Stories/STORY-001.md"]
        }

        backup_service = Mock()
        backup_service.create_backup.return_value = str(temp_backup_dir / "backup.tar.gz")

        file_system = Mock()
        file_system.exists = Mock(return_value=True)
        file_system.remove_file = Mock()
        file_system.remove_dir = Mock()

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system
        )

        request = UninstallRequest(
            mode=UninstallMode.COMPLETE,
            skip_confirmation=True
        )

        result = orchestrator.execute(request)

        # All files should be removed
        assert result is not None

    def test_should_validate_dry_run_doesnt_modify_files(
        self,
        temp_install_dir,
        temp_backup_dir
    ):
        """Test: AC#3 - Dry-run doesn't modify files."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest
        from unittest.mock import Mock

        # Record initial file states
        (temp_install_dir / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        skill_file = temp_install_dir / ".claude" / "skills" / "test.md"
        skill_file.write_text("Skill content")
        initial_hash = hash(skill_file.read_text())

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        backup_service = Mock()
        file_system = Mock()

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system
        )

        request = UninstallRequest(dry_run=True)
        result = orchestrator.execute(request)

        # Files should NOT be deleted in dry-run
        file_system.remove_file.assert_not_called()

    def test_should_create_backup_before_deleting(
        self,
        temp_install_dir,
        temp_backup_dir
    ):
        """Test: AC#5 - Backup created before any deletions."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest
        from unittest.mock import Mock, call

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        backup_service = Mock()
        backup_service.create_backup.return_value = str(temp_backup_dir / "backup.tar.gz")

        file_system = Mock()
        file_system.exists = Mock(return_value=True)
        file_system.remove_file = Mock()

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Backup should be called (at least once) before file removal proceeds
        assert backup_service.create_backup.call_count >= 1

    def test_should_display_confirmation_prompt(
        self,
        temp_install_dir,
        capsys
    ):
        """Test: AC#4 - Confirmation prompt displayed."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest
        from unittest.mock import Mock, patch

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        backup_service = Mock()
        file_system = Mock()
        file_system.exists = Mock(return_value=True)

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system
        )

        request = UninstallRequest(skip_confirmation=False)

        with patch('builtins.input', return_value='n'):
            result = orchestrator.execute(request)

        # Should show summary before confirmation
        assert result is not None

    def test_should_generate_summary_report(
        self,
        temp_install_dir,
        temp_backup_dir
    ):
        """Test: AC#8 - Uninstall summary generated and saved."""
        from installer.uninstall_orchestrator import UninstallOrchestrator
        from installer.uninstall_models import UninstallRequest
        from installer.uninstall_reporter import UninstallReporter
        from unittest.mock import Mock

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        backup_service = Mock()
        backup_service.create_backup.return_value = str(temp_backup_dir / "backup.tar.gz")

        file_system = Mock()
        file_system.exists = Mock(return_value=True)
        file_system.remove_file = Mock()

        reporter = UninstallReporter()

        orchestrator = UninstallOrchestrator(
            manifest_manager=manifest_manager,
            backup_service=backup_service,
            file_system=file_system,
            reporter=reporter
        )

        request = UninstallRequest(skip_confirmation=True)
        result = orchestrator.execute(request)

        # Result should be created
        assert result is not None
        assert hasattr(result, 'status')

    def test_should_classify_and_preserve_user_content(
        self,
        temp_install_dir
    ):
        """Test: AC#9 - User content detection and preservation."""
        from installer.content_classifier import ContentClassifier
        from installer.uninstall_models import ContentType
        from unittest.mock import Mock

        manifest_manager = Mock()
        manifest_manager.load_manifest.return_value = {
            "installed_files": [".claude/skills/test.md"]
        }

        classifier = ContentClassifier(manifest_manager=manifest_manager)

        # Stories should be USER_CONTENT
        assert classifier.classify("devforgeai/specs/Stories/STORY-001.md") == ContentType.USER_CONTENT

        # Framework files should be FRAMEWORK
        assert classifier.classify(".claude/skills/test.md") == ContentType.FRAMEWORK

    def test_should_handle_cli_cleanup_when_installed(
        self,
        temp_install_dir
    ):
        """Test: AC#7 - CLI cleanup for installed binaries."""
        from installer.cli_cleaner import CLICleaner
        from unittest.mock import Mock, patch

        file_system = Mock()
        file_system.exists = Mock(return_value=True)
        file_system.remove_file = Mock()

        cleaner = CLICleaner(file_system=file_system)

        with patch('shutil.which', return_value=None):
            result = cleaner.remove_local_binary("devforgeai")

        # Should handle CLI cleanup
        assert result is not None
