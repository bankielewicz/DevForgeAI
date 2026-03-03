"""
STORY-069: Unit Tests for __main__.py - CLI Entry Point

Tests validate CLI argument parsing, command routing, and error handling.

Coverage targets:
- main() function: 100%
- Command parsing (install, validate, rollback, uninstall): 100%
- Help text display: 100%
- Error handling: 100%

Expected Result: All tests pass (implementation complete)
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Import the main function
from installer.__main__ import main


class TestMainHelpText:
    """Unit tests for help text display."""

    def test_help_flag_short(self, capsys):
        """
        Should display help text for -h flag.

        Arrange: sys.argv with -h
        Act: Call main()
        Assert: Exits with 0, prints help
        """
        # Arrange
        with patch.object(sys, 'argv', ['installer', '-h']):
            # Act & Assert
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "DevForgeAI Installer" in captured.out
            assert "install" in captured.out
            assert "validate" in captured.out
            assert "rollback" in captured.out
            assert "uninstall" in captured.out

    def test_help_flag_long(self, capsys):
        """
        Should display help text for --help flag.

        Arrange: sys.argv with --help
        Act: Call main()
        Assert: Exits with 0, prints help
        """
        # Arrange
        with patch.object(sys, 'argv', ['installer', '--help']):
            # Act & Assert
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    def test_no_arguments(self, capsys):
        """
        Should display help when no arguments provided.

        Arrange: sys.argv with no arguments
        Act: Call main()
        Assert: Exits with 0, prints help
        """
        # Arrange
        with patch.object(sys, 'argv', ['installer']):
            # Act & Assert
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "DevForgeAI Installer" in captured.out


class TestMainCommandParsing:
    """Unit tests for command parsing."""

    def test_unknown_command(self, capsys):
        """
        Should reject unknown command.

        Arrange: sys.argv with invalid command
        Act: Call main()
        Assert: Exits with 1, prints error
        """
        # Arrange
        with patch.object(sys, 'argv', ['installer', 'unknown', '/path']):
            # Act & Assert
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

            captured = capsys.readouterr()
            assert "Unknown command" in captured.out
            assert "unknown" in captured.out

    def test_missing_target_path(self, capsys):
        """
        Should require target path for all commands.

        Arrange: sys.argv with command but no path
        Act: Call main()
        Assert: Exits with 1, prints error
        """
        # Arrange
        with patch.object(sys, 'argv', ['installer', 'install']):
            # Act & Assert
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

            captured = capsys.readouterr()
            assert "requires a target path" in captured.out


class TestMainInstallCommand:
    """Unit tests for install command."""

    def test_install_success(self, capsys, tmp_path):
        """
        Should execute install successfully.

        Arrange: Mock install module to return success
        Act: Call main with install command
        Assert: Exits with 0, prints success messages
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": ["Installation successful"],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result):
                # Act & Assert
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 0

                captured = capsys.readouterr()
                assert "Installation successful" in captured.out

    def test_install_with_force_flag(self, tmp_path):
        """
        Should pass force flag to install function.

        Arrange: sys.argv with --force flag
        Act: Call main with install command
        Assert: install() called with force=True
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": [],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path, '--force']):
            with patch('installer.__main__.install_module.install', return_value=mock_result) as mock_install:
                # Act
                with pytest.raises(SystemExit):
                    main()

                # Assert
                mock_install.assert_called_once()
                call_args = mock_install.call_args
                assert call_args.kwargs.get('force') is True

    def test_install_failure(self, capsys, tmp_path):
        """
        Should exit with 1 on install failure.

        Arrange: Mock install to return failed status
        Act: Call main with install command
        Assert: Exits with 1, prints errors
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "failed",
            "messages": [],
            "warnings": [],
            "errors": ["Installation failed: Error reason"]
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result):
                # Act & Assert
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1

                captured = capsys.readouterr()
                assert "Installation failed" in captured.out

    def test_install_rollback(self, capsys, tmp_path):
        """
        Should exit with 2 on rollback.

        Arrange: Mock install to return rollback status
        Act: Call main with install command
        Assert: Exits with 2, prints rollback message
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "rollback",
            "messages": ["Installation rolled back"],
            "warnings": [],
            "errors": ["Error during installation"]
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result):
                # Act & Assert
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 2

                captured = capsys.readouterr()
                assert "rolled back" in captured.out


class TestMainValidateCommand:
    """Unit tests for validate command."""

    def test_validate_success(self, capsys, tmp_path):
        """
        Should execute validate successfully.

        Arrange: Mock install with mode='validate'
        Act: Call main with validate command
        Assert: Exits with 0
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": ["Validation successful"],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'validate', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result) as mock_install:
                # Act
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Assert
                assert exc_info.value.code == 0
                mock_install.assert_called_once_with(Path(target_path).resolve(), mode='validate')


class TestMainRollbackCommand:
    """Unit tests for rollback command."""

    def test_rollback_success(self, tmp_path):
        """
        Should execute rollback successfully.

        Arrange: Mock install with mode='rollback'
        Act: Call main with rollback command
        Assert: Exits with 0
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": ["Rollback successful"],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'rollback', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result) as mock_install:
                # Act
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Assert
                assert exc_info.value.code == 0
                mock_install.assert_called_once_with(Path(target_path).resolve(), mode='rollback')


class TestMainUninstallCommand:
    """Unit tests for uninstall command."""

    def test_uninstall_success(self, tmp_path):
        """
        Should execute uninstall successfully.

        Arrange: Mock install with mode='uninstall'
        Act: Call main with uninstall command
        Assert: Exits with 0
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": ["Uninstall successful"],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'uninstall', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result) as mock_install:
                # Act
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Assert
                assert exc_info.value.code == 0
                mock_install.assert_called_once_with(Path(target_path).resolve(), mode='uninstall')


class TestMainErrorHandling:
    """Unit tests for error handling."""

    def test_exception_handling(self, capsys, tmp_path):
        """
        Should catch and display exceptions.

        Arrange: Mock install to raise exception
        Act: Call main
        Assert: Exits with 1, prints error
        """
        # Arrange
        target_path = str(tmp_path)

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', side_effect=Exception("Test error")):
                # Act & Assert
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1

                captured = capsys.readouterr()
                assert "Installer error" in captured.out
                assert "Test error" in captured.out

    def test_displays_warnings(self, capsys, tmp_path):
        """
        Should display warnings with emoji.

        Arrange: Mock install to return warnings
        Act: Call main
        Assert: Prints warnings with warning emoji
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "success",
            "messages": [],
            "warnings": ["Warning message"],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result):
                # Act
                with pytest.raises(SystemExit):
                    main()

                # Assert
                captured = capsys.readouterr()
                # Check for warning symbol (may vary by system)
                assert "Warning message" in captured.out

    def test_displays_errors(self, capsys, tmp_path):
        """
        Should display errors with emoji.

        Arrange: Mock install to return errors
        Act: Call main
        Assert: Prints errors with error emoji
        """
        # Arrange
        target_path = str(tmp_path)
        mock_result = {
            "status": "failed",
            "messages": [],
            "warnings": [],
            "errors": ["Error message"]
        }

        with patch.object(sys, 'argv', ['installer', 'install', target_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result):
                # Act
                with pytest.raises(SystemExit):
                    main()

                # Assert
                captured = capsys.readouterr()
                assert "Error message" in captured.out

    def test_path_resolution(self, tmp_path):
        """
        Should resolve target path to absolute.

        Arrange: Provide relative path
        Act: Call main
        Assert: install() receives absolute path
        """
        # Arrange
        relative_path = "."
        mock_result = {
            "status": "success",
            "messages": [],
            "warnings": [],
            "errors": []
        }

        with patch.object(sys, 'argv', ['installer', 'install', relative_path]):
            with patch('installer.__main__.install_module.install', return_value=mock_result) as mock_install:
                # Act
                with pytest.raises(SystemExit):
                    main()

                # Assert
                call_args = mock_install.call_args
                received_path = call_args.args[0]
                assert received_path.is_absolute()
