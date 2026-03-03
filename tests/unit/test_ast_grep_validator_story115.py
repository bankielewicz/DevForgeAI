"""
Test suite for AstGrepValidator - STORY-115 CLI Validator Foundation.

TDD Test-First Implementation following DevForgeAI framework patterns.
Tests organized by acceptance criteria and implementation phase.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from typing import Optional
import tempfile

# Imports will work because conftest.py adds src/ to sys.path
from claude.scriptsdevforgeai_cli.validators.ast_grep_validator import (
    parse_version,
    detect_headless_mode,
    AstGrepValidator,
    VersionInfo,
    InstallAction
)


# =============================================================================
# Phase 1: Version Parsing Tests (8 tests) - AC#4
# =============================================================================

class TestVersionParsing:
    """Phase 1: Test version string parsing and compatibility checking."""

    def test_parse_version_valid_simple(self):
        """Test: Parse simple version string '0.40.0' correctly."""
        result = parse_version("0.40.0")

        assert result is not None
        assert result.major == 0
        assert result.minor == 40
        assert result.patch == 0
        assert result.raw == "0.40.0"

    def test_parse_version_valid_complex(self):
        """Test: Parse version with prerelease suffix '0.40.5-beta.1'."""
        result = parse_version("0.40.5-beta.1")

        assert result is not None
        assert result.major == 0
        assert result.minor == 40
        assert result.patch == 5
        assert result.raw == "0.40.5-beta.1"

    def test_parse_version_invalid_format(self):
        """Test: Return None for invalid version format."""
        result = parse_version("invalid")
        assert result is None

    def test_parse_version_empty(self):
        """Test: Return None for empty string."""
        result = parse_version("")
        assert result is None

    def test_version_compatible_exact_min(self):
        """Test: Version 0.40.0 (exact minimum) is compatible."""
        version = parse_version("0.40.0")
        assert version is not None
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is True

    def test_version_compatible_below_min(self):
        """Test: Version 0.39.9 (below minimum) is NOT compatible."""
        version = parse_version("0.39.9")
        assert version is not None
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False

    def test_version_compatible_at_max(self):
        """Test: Version 1.0.0 (at max, exclusive) is NOT compatible."""
        version = parse_version("1.0.0")
        assert version is not None
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False

    def test_version_compatible_above_max(self):
        """Test: Version 1.1.0 (above max) is NOT compatible."""
        version = parse_version("1.1.0")
        assert version is not None
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False


# =============================================================================
# Phase 2: Installation Detection Tests (8 tests) - AC#1, AC#4
# =============================================================================

class TestInstallationDetection:
    """Phase 2: Test ast-grep installation detection via shutil.which/subprocess."""

    @pytest.fixture
    def validator(self):
        """Fixture: Create AstGrepValidator instance."""
        return AstGrepValidator(interactive=False)

    def test_is_installed_found_in_path(self, validator):
        """Test: Detection succeeds when ast-grep is in PATH."""
        with patch("shutil.which", return_value="/usr/bin/sg"):
            result = validator.is_installed()
        assert result is True

    def test_is_installed_not_found(self, validator):
        """Test: Detection fails gracefully when ast-grep missing."""
        with patch("shutil.which", return_value=None):
            result = validator.is_installed()
        assert result is False

    def test_get_version_success(self, validator):
        """Test: Version extraction from subprocess output."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ast-grep 0.45.0"

        with patch("subprocess.run", return_value=mock_result):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                version = validator.get_version()

        assert version is not None
        assert version.major == 0
        assert version.minor == 45
        assert version.patch == 0

    def test_get_version_parse_failure(self, validator):
        """Test: Return None when version output is malformed."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "unknown output format"

        with patch("subprocess.run", return_value=mock_result):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                version = validator.get_version()

        assert version is None

    def test_get_version_command_failure(self, validator):
        """Test: Return None when subprocess raises exception."""
        with patch("subprocess.run", side_effect=Exception("Command failed")):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                version = validator.get_version()

        assert version is None

    def test_check_version_compatible(self, validator):
        """Test: Compatible version returns success tuple."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ast-grep 0.45.0"

        with patch("subprocess.run", return_value=mock_result):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                is_compatible, message = validator.check_version_compatibility()

        assert is_compatible is True
        assert "0.45.0" in message or "compatible" in message.lower()

    def test_check_version_too_old(self, validator):
        """Test: Old version returns failure with warning message."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ast-grep 0.39.0"

        with patch("subprocess.run", return_value=mock_result):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                is_compatible, message = validator.check_version_compatibility()

        assert is_compatible is False
        assert "0.40.0" in message

    def test_check_version_too_new(self, validator):
        """Test: Too new version returns failure with warning message."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ast-grep 1.1.0"

        with patch("subprocess.run", return_value=mock_result):
            with patch("shutil.which", return_value="/usr/bin/sg"):
                is_compatible, message = validator.check_version_compatibility()

        assert is_compatible is False
        assert "1.0.0" in message


# =============================================================================
# Phase 3: Installation Flow Tests (4 tests) - AC#1
# =============================================================================

class TestInstallationFlow:
    """Phase 3: Test pip-based installation of ast-grep-cli."""

    @pytest.fixture
    def validator(self):
        """Fixture: Create AstGrepValidator instance."""
        return AstGrepValidator(interactive=False)

    def test_install_via_pip_success(self, validator):
        """Test: Successful pip install returns success tuple."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Successfully installed ast-grep-cli-0.45.0"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            success, message = validator.install_via_pip()

        assert success is True
        assert "success" in message.lower() or "installed" in message.lower()

    def test_install_via_pip_failure(self, validator):
        """Test: Failed pip install returns failure tuple."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "ERROR: Could not find a version that satisfies the requirement"

        with patch("subprocess.run", return_value=mock_result):
            success, message = validator.install_via_pip()

        assert success is False
        assert "error" in message.lower() or "fail" in message.lower()

    def test_install_via_pip_timeout(self, validator):
        """Test: Pip timeout returns failure with timeout message."""
        import subprocess

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pip", 120)):
            success, message = validator.install_via_pip()

        assert success is False
        assert "timeout" in message.lower()

    def test_install_then_verify(self, validator):
        """Test: After install, installation can be verified."""
        mock_install = Mock()
        mock_install.returncode = 0
        mock_install.stdout = "Successfully installed"
        mock_install.stderr = ""

        with patch("subprocess.run", return_value=mock_install):
            success, _ = validator.install_via_pip()
            assert success is True


# =============================================================================
# Phase 4: Interactive Prompts Tests (7 tests) - AC#2
# =============================================================================

class TestInteractivePrompts:
    """Phase 4: Test interactive prompts for missing dependency."""

    @pytest.fixture
    def validator_interactive(self):
        """Fixture: Create interactive AstGrepValidator instance."""
        return AstGrepValidator(interactive=True)

    @pytest.fixture
    def validator_headless(self):
        """Fixture: Create headless AstGrepValidator instance."""
        return AstGrepValidator(interactive=False)

    def test_prompt_shows_three_options(self, validator_interactive):
        """Test: Prompt displays exactly 3 options."""
        with patch("builtins.input", return_value="2"):
            with patch("builtins.print") as mock_print:
                validator_interactive.prompt_missing_dependency()

                printed_text = " ".join(str(call) for call in mock_print.call_args_list)
                assert "1" in printed_text
                assert "2" in printed_text
                assert "3" in printed_text

    def test_prompt_install_selection(self, validator_interactive):
        """Test: Selecting '1' returns INSTALL_NOW action."""
        with patch("builtins.input", return_value="1"):
            result = validator_interactive.prompt_missing_dependency()

        assert result == InstallAction.INSTALL_NOW

    def test_prompt_fallback_selection(self, validator_interactive):
        """Test: Selecting '2' returns USE_FALLBACK action."""
        with patch("builtins.input", return_value="2"):
            result = validator_interactive.prompt_missing_dependency()

        assert result == InstallAction.USE_FALLBACK

    def test_prompt_skip_selection(self, validator_interactive):
        """Test: Selecting '3' returns SKIP action."""
        with patch("builtins.input", return_value="3"):
            result = validator_interactive.prompt_missing_dependency()

        assert result == InstallAction.SKIP

    def test_headless_mode_detection_ci(self):
        """Test: CI=true environment variable triggers headless mode."""
        with patch.dict(os.environ, {"CI": "true"}):
            result = detect_headless_mode()

        assert result is True

    def test_headless_mode_detection_env(self):
        """Test: DEVFORGEAI_HEADLESS=true triggers headless mode."""
        with patch.dict(os.environ, {"DEVFORGEAI_HEADLESS": "true"}, clear=False):
            result = detect_headless_mode()

        assert result is True

    def test_headless_mode_no_prompt(self, validator_headless):
        """Test: In headless mode, no prompt is shown, uses config default."""
        with patch("builtins.input") as mock_input:
            result = validator_headless.prompt_missing_dependency()
            mock_input.assert_not_called()

        assert result == InstallAction.USE_FALLBACK


# =============================================================================
# Phase 6: Integration Tests (2 tests) - End-to-End
# =============================================================================

class TestIntegration:
    """Phase 6: End-to-end integration tests."""

    @pytest.fixture
    def validator(self):
        """Fixture: Create AstGrepValidator instance."""
        return AstGrepValidator(interactive=False)

    def test_validate_with_ast_grep_installed(self, validator):
        """Test: Uses ast-grep when installed and compatible."""
        mock_version = Mock()
        mock_version.returncode = 0
        mock_version.stdout = "ast-grep 0.45.0"

        with patch("shutil.which", return_value="/usr/bin/sg"):
            with patch("subprocess.run", return_value=mock_version):
                with patch.object(validator, "is_installed", return_value=True):
                    is_valid, violations = validator.validate("./src")

        assert isinstance(is_valid, bool)
        assert isinstance(violations, list)

    def test_validate_with_fallback(self, validator):
        """Test: Uses grep fallback when ast-grep not installed."""
        with patch("shutil.which", return_value=None):
            with patch.object(validator, "is_installed", return_value=False):
                is_valid, violations = validator.validate("./src")

        assert isinstance(is_valid, bool)
        assert isinstance(violations, list)


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Additional edge case and boundary tests."""

    def test_parse_version_with_v_prefix(self):
        """Test: Handle version strings with 'v' prefix like 'v0.45.0'."""
        result = parse_version("v0.45.0")

        assert result is not None
        assert result.major == 0
        assert result.minor == 45

    def test_version_middle_of_range(self):
        """Test: Version in middle of compatible range."""
        version = parse_version("0.55.0")

        assert version is not None
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is True

    def test_config_loading_missing_file(self):
        """Test: Config loading with missing file uses defaults."""
        validator = AstGrepValidator(
            config_path="/nonexistent/path/config.yaml",
            interactive=False
        )

        assert validator.config is not None
        assert "fallback_mode" in validator.config

    def test_config_loading_valid_file(self, tmp_path):
        """Test: Config loading with valid YAML file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
fallback_mode: true
min_version: "0.40.0"
max_version: "1.0.0"
allow_auto_install: false
""")

        validator = AstGrepValidator(
            config_path=str(config_file),
            interactive=False
        )

        assert validator.config["fallback_mode"] is True
        assert validator.config["allow_auto_install"] is False

    def test_prompt_invalid_input_retry(self):
        """Test: Invalid input prompts for retry."""
        from unittest.mock import call as mock_call

        validator = AstGrepValidator(interactive=True)

        # Simulate invalid input then valid
        with patch("builtins.input", side_effect=["invalid", "99", "2"]):
            with patch("builtins.print"):
                result = validator.prompt_missing_dependency()

        assert result == InstallAction.USE_FALLBACK

    def test_prompt_keyboard_interrupt(self):
        """Test: KeyboardInterrupt returns SKIP action."""
        validator = AstGrepValidator(interactive=True)

        with patch("builtins.input", side_effect=KeyboardInterrupt()):
            with patch("builtins.print"):
                result = validator.prompt_missing_dependency()

        assert result == InstallAction.SKIP

    def test_prompt_eof_error(self):
        """Test: EOFError returns SKIP action."""
        validator = AstGrepValidator(interactive=True)

        with patch("builtins.input", side_effect=EOFError()):
            with patch("builtins.print"):
                result = validator.prompt_missing_dependency()

        assert result == InstallAction.SKIP

    def test_validate_install_flow_complete(self):
        """Test: Complete validation flow with successful install."""
        validator = AstGrepValidator(interactive=False)

        mock_install = Mock()
        mock_install.returncode = 0
        mock_install.stdout = "Successfully installed"

        with patch("shutil.which", return_value=None):  # Not installed initially
            with patch.object(validator, "prompt_missing_dependency", return_value=InstallAction.INSTALL_NOW):
                with patch("subprocess.run", return_value=mock_install):
                    is_valid, violations = validator.validate("./src")

        # Should attempt install and succeed
        assert is_valid is True

    def test_validate_skip_action(self):
        """Test: Validation with SKIP action."""
        validator = AstGrepValidator(interactive=False)

        with patch("shutil.which", return_value=None):
            with patch.object(validator, "prompt_missing_dependency", return_value=InstallAction.SKIP):
                is_valid, violations = validator.validate("./src")

        # Should return info violation about skipped scan
        assert is_valid is True
        assert len(violations) == 1
        assert violations[0]["severity"] == "INFO"

    def test_validate_use_fallback_action(self):
        """Test: Validation with USE_FALLBACK action proceeds."""
        validator = AstGrepValidator(interactive=False)

        with patch("shutil.which", return_value=None):
            with patch.object(validator, "prompt_missing_dependency", return_value=InstallAction.USE_FALLBACK):
                is_valid, violations = validator.validate("./src")

        # Should proceed (fallback would be used in full implementation)
        assert is_valid is True

    def test_validate_install_failed(self):
        """Test: Validation when install fails returns violations."""
        validator = AstGrepValidator(interactive=False)

        mock_install_fail = Mock()
        mock_install_fail.returncode = 1
        mock_install_fail.stderr = "Network error"

        with patch("shutil.which", return_value=None):
            with patch.object(validator, "prompt_missing_dependency", return_value=InstallAction.INSTALL_NOW):
                with patch("subprocess.run", return_value=mock_install_fail):
                    is_valid, violations = validator.validate("./src")

        # Should report installation failure
        assert is_valid is False
        assert len(violations) > 0
        assert violations[0]["severity"] == "HIGH"

    def test_validate_version_incompatible_warning(self):
        """Test: Incompatible version generates warning violation."""
        validator = AstGrepValidator(interactive=False)

        mock_version = Mock()
        mock_version.returncode = 0
        mock_version.stdout = "ast-grep 0.30.0"  # Too old

        with patch("shutil.which", return_value="/usr/bin/sg"):
            with patch("subprocess.run", return_value=mock_version):
                is_valid, violations = validator.validate("./src")

        # Should generate version warning
        warning_violations = [v for v in violations if v["severity"] == "MEDIUM"]
        assert len(warning_violations) > 0

    def test_headless_mode_with_non_tty(self):
        """Test: Non-TTY terminal triggers headless mode."""
        # Mock sys.stdin.fileno() and os.isatty() to simulate non-TTY
        with patch("sys.stdin.fileno", return_value=0):
            with patch("os.isatty", return_value=False):
                result = detect_headless_mode()

        assert result is True

    def test_config_loading_yaml_error(self, tmp_path):
        """Test: Corrupted YAML file falls back to defaults."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("invalid: yaml: ::::")  # Corrupted YAML

        validator = AstGrepValidator(
            config_path=str(config_file),
            interactive=False
        )

        # Should fall back to defaults
        assert validator.config is not None
        assert validator.config["fallback_mode"] is False  # Default value


# =============================================================================
# Version Boundary Tests
# =============================================================================

class TestVersionBoundaries:
    """Test version comparison edge cases for complete branch coverage."""

    def test_version_major_less_than_min(self):
        """Test: Major version below minimum."""
        version = parse_version("0.30.0")
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False

    def test_version_major_equals_minor_less(self):
        """Test: Major equal, minor less than minimum."""
        version = parse_version("0.39.9")
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False

    def test_version_major_equals_minor_equals_patch_less(self):
        """Test: Major and minor equal, patch less than minimum."""
        version = parse_version("0.40.0")
        # Comparing against 0.40.1 to test patch comparison
        assert version.is_compatible(min_version="0.40.1", max_version="1.0.0") is False

    def test_version_major_greater_than_max(self):
        """Test: Major version exceeds maximum."""
        version = parse_version("2.0.0")
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False

    def test_version_major_equals_minor_at_max(self):
        """Test: Major equal to max, minor at boundary."""
        version = parse_version("1.0.0")
        assert version.is_compatible(min_version="0.40.0", max_version="1.0.0") is False
