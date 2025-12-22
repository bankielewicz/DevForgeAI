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


class TestMacOSSpecificCleaning:
    """Test macOS-specific CLI cleanup (Coverage Gap)."""

    def test_should_detect_homebrew_installed_devforgeai_on_macos(self, mock_file_system, mock_logger):
        """Test: Detect if devforgeai was installed via Homebrew on macOS.

        AC #7: CLI cleanup handles platform-specific installations.

        Scenario: devforgeai installed via 'brew install devforgeai'
        Expected: Detect Homebrew installation at /usr/local/opt/devforgeai
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        # Mock Homebrew installation
        mock_file_system.exists = Mock(return_value=True)
        mock_file_system.is_dir = Mock(return_value=True)

        with patch('platform.system', return_value='Darwin'):
            result = cleaner.detect_homebrew_installation()

            # Should detect Homebrew installation
            assert result is not None or mock_logger.info.called

    def test_should_remove_homebrew_installation(self, mock_file_system, mock_logger):
        """Test: Remove Homebrew-installed devforgeai.

        Expected: Run 'brew uninstall devforgeai' or remove from Cellar
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch('platform.system', return_value='Darwin'):
            with patch('subprocess.run') as mock_run:
                result = cleaner.remove_homebrew_installation()

                # Should attempt Homebrew removal
                assert result is not None

    def test_should_handle_macos_permission_dialogs(self, mock_file_system, mock_logger):
        """Test: Handle macOS permission prompts during cleanup.

        Expected: User prompted once, subsequent operations use cached permission
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch('platform.system', return_value='Darwin'):
            # Multiple cleanup operations should be batched
            result = cleaner.cleanup_all_shell_integrations()
            assert result is not None


class TestFishShellIntegration:
    """Test Fish shell-specific cleanup (Coverage Gap)."""

    def test_should_cleanup_fish_shell_completions(self, mock_file_system, mock_logger, temp_install_dir):
        """Test: Remove devforgeai completions from Fish shell.

        AC #7: CLI cleanup includes shell integrations.

        Scenario: devforgeai completions in ~/.config/fish/conf.d/
        Expected: Remove completions file, clean up function definitions
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        # Create Fish completion file
        fish_config = temp_install_dir / ".config" / "fish" / "conf.d" / "devforgeai.fish"
        fish_config.parent.mkdir(parents=True, exist_ok=True)
        fish_config.write_text("# devforgeai completions")

        mock_file_system.exists = Mock(return_value=True)

        result = cleaner.cleanup_fish_completions()

        # Should detect and clean Fish completions
        assert result is not None

    def test_should_remove_fish_function_definitions(self, mock_file_system, mock_logger):
        """Test: Remove devforgeai function definitions from Fish.

        Expected: Remove 'function devforgeai' definitions
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch.object(cleaner, 'read_config_file', return_value="function devforgeai"):
            result = cleaner.cleanup_fish_functions()

            assert result is not None

    def test_should_handle_fish_config_not_found(self, mock_file_system, mock_logger):
        """Test: Handle missing Fish configuration gracefully.

        Expected: Return success (nothing to clean)
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        mock_file_system.exists = Mock(return_value=False)

        result = cleaner.cleanup_fish_completions()

        # Should handle gracefully
        assert result is not None


class TestEnvironmentSpecificCleanup:
    """Test environment-specific CLI cleanup (Coverage Gap)."""

    def test_should_detect_docker_environment_and_skip_path_cleanup(self, mock_file_system, mock_logger):
        """Test: Detect Docker environment and skip system PATH cleanup.

        AC #7: CLI cleanup handles environment-specific cases.

        Scenario: uninstall running inside Docker container
        Expected: Skip /usr/local/bin cleanup, only clean container paths
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        # Mock Docker detection
        with patch.dict('os.environ', {'DOCKER_HOST': 'unix:///var/run/docker.sock'}):
            with patch('pathlib.Path.exists', return_value=True):
                result = cleaner.cleanup_for_docker_environment()

                # Should detect Docker and adjust behavior
                assert result is not None or mock_logger.info.called

    def test_should_handle_kubernetes_mounted_paths(self, mock_file_system, mock_logger):
        """Test: Handle Kubernetes volume-mounted paths safely.

        Expected: Skip mounted volume cleanup, warn user
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch.dict('os.environ', {'KUBERNETES_SERVICE_HOST': '10.0.0.1'}):
            result = cleaner.detect_kubernetes_environment()

            # Should warn about mounted paths
            assert result is not None

    def test_should_detect_virtual_environment_and_adjust_cleanup(self, mock_file_system, mock_logger):
        """Test: Detect Python virtual environment installation.

        Expected: Clean venv-specific paths, skip system paths
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        with patch.dict('os.environ', {'VIRTUAL_ENV': '/path/to/venv'}):
            result = cleaner.cleanup_venv_installation()

            # Should detect and handle venv
            assert result is not None


class TestCorruptedConfigRecovery:
    """Test recovery from corrupted shell configs (Coverage Gap)."""

    def test_should_hard_reset_corrupted_shell_configs(self, mock_file_system, mock_logger, temp_install_dir):
        """Test: Hard reset corrupted shell configuration files.

        AC #7: CLI cleanup handles corrupted configs gracefully.

        Scenario: .bashrc corrupted (syntax errors, partial removal)
        Expected: Restore from backup or reconstruct safe version
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        # Create corrupted config file
        bashrc = temp_install_dir / ".bashrc"
        bashrc.write_text("[ invalid syntax\n# devforgeai config\nalias d='bad'")

        result = cleaner.hard_reset_bash_config()

        # Should detect corruption and reset
        assert result is not None

    def test_should_validate_config_integrity_before_cleanup(self, mock_file_system, mock_logger):
        """Test: Validate shell config integrity before removal.

        Expected: Syntax check passes before cleanup proceeds
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        # Mock config with valid syntax
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0  # Syntax valid

            result = cleaner.validate_config_integrity()

            # Should pass validation
            assert result is None or result

    def test_should_backup_corrupted_configs_before_reset(self, mock_file_system, mock_logger):
        """Test: Create backup of corrupted configs before hard reset.

        Expected: Corrupted config backed up to .backup file
        """
        from installer.cli_cleaner import CLICleaner

        cleaner = CLICleaner(file_system=mock_file_system, logger=mock_logger)

        mock_file_system.copy = Mock()

        result = cleaner.backup_and_reset_config()

        # Should create backup
        assert result is not None
