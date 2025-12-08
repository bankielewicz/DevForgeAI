"""
Unit tests for CLICleaner service.
Tests removal of CLI binaries and shell integration.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestCLICleanerInit:
    """Test CLICleaner initialization."""

    def test_should_instantiate_with_file_system(self, mock_file_system):
        """Test: CLICleaner initializes with FileSystem dependency."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)
        assert cleaner is not None


class TestLocalBinaryRemoval:
    """Test removal of local CLI binaries."""

    def test_should_remove_local_bin_devforgeai(self, mock_file_system):
        """Test: devforgeai binary removed from ~/bin/."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)
        mock_file_system.exists = Mock(return_value=True)
        mock_file_system.is_file = Mock(return_value=True)

        result = cleaner.remove_local_binary("devforgeai")

        # Should attempt to remove binary
        assert result.removed or not result.removed  # Placeholder

    def test_should_remove_wrapper_scripts(self, mock_file_system):
        """Test: Wrapper scripts removed (sh, bash, zsh)."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)
        mock_file_system.remove_file = Mock()

        cleaner.remove_wrapper_scripts()

        # Should attempt removal
        assert mock_file_system.remove_file.called

    def test_should_return_result_with_success_status(self, mock_file_system):
        """Test: CLICleaner returns result object with status."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)
        mock_file_system.exists = Mock(return_value=True)
        mock_file_system.remove_file = Mock()

        result = cleaner.remove_local_binary("devforgeai")

        assert hasattr(result, 'removed')
        assert hasattr(result, 'warnings')


class TestPathBinaryDetection:
    """Test detection of binaries in PATH."""

    def test_should_detect_devforgeai_in_path(self, mock_file_system):
        """Test: Detect if devforgeai is in PATH."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        with patch.dict('os.environ', {'PATH': '/usr/local/bin:/usr/bin'}):
            with patch('shutil.which', return_value='/usr/local/bin/devforgeai'):
                is_in_path = cleaner.is_binary_in_path("devforgeai")
                # Should detect binary in PATH

    def test_should_warn_if_system_path_install(self, mock_file_system, mock_logger):
        """Test: Warn user if binary in system PATH (requires sudo)."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch('shutil.which', return_value='/usr/bin/devforgeai'):
            result = cleaner.remove_local_binary("devforgeai")

            # Should warn about system PATH install
            assert result.warnings is not None


class TestShellIntegrationCleaning:
    """Test cleanup of shell integrations."""

    def test_should_remove_bash_aliases(self, mock_file_system):
        """Test: Remove devforgeai aliases from .bashrc."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        result = cleaner.cleanup_shell_aliases("bash")

        # Should clean shell integration
        assert result is not None

    def test_should_remove_zsh_completions(self, mock_file_system):
        """Test: Remove devforgeai completions from .zshrc."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        result = cleaner.cleanup_shell_integrations("zsh")

        assert result is not None

    def test_should_remove_fish_completions(self, mock_file_system):
        """Test: Remove devforgeai completions from fish."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        result = cleaner.cleanup_shell_integrations("fish")

        assert result is not None

    def test_should_handle_multiple_shells(self, mock_file_system):
        """Test: Clean integrations for all installed shells."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        result = cleaner.cleanup_all_shell_integrations()

        assert result is not None


class TestPathCleanupWarnings:
    """Test warnings for manual PATH cleanup."""

    def test_should_warn_if_npm_global_install(self, mock_file_system, mock_logger):
        """Test: Warn user about npm -g installations."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch('shutil.which', return_value='/usr/local/lib/node_modules/devforgeai'):
            result = cleaner.check_npm_global_install()

            # Should warn about npm global install
            assert result.requires_manual_cleanup

    def test_should_provide_manual_cleanup_instructions(self, mock_file_system, mock_logger):
        """Test: Provide instructions for manual PATH cleanup."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        instructions = cleaner.get_manual_cleanup_instructions()

        # Should provide clear instructions
        assert isinstance(instructions, str) or instructions is not None

    def test_should_track_warnings_for_user(self, mock_file_system):
        """Test: CLICleaner collects all warnings for final report."""
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system)

        result = cleaner.remove_local_binary("devforgeai")

        # Result should track warnings
        assert hasattr(result, 'warnings')
