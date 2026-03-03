#!/usr/bin/env python3
"""
Tests for STORY-314: Add Post-Install Validation Command

Tests validate-installation command that checks:
1. CLI availability (devforgeai-validate --version)
2. Context files (6 files in devforgeai/specs/context/)
3. Hook installation (.git/hooks/pre-commit exists)
4. PYTHONPATH configuration
5. Git repository (.git/ exists)
6. Settings file (.claude/settings.json exists)

TDD Phase: RED - Tests written before implementation
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add CLI module to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude' / 'scripts'))

# Import will fail until implementation exists - expected in RED phase
try:
    from devforgeai_cli.commands.validate_installation import (
        validate_installation_command,
        check_cli_available,
        check_context_files,
        check_hooks_installed,
        check_pythonpath,
        check_git_repository,
        check_settings_file,
        ValidationResult,
    )
    IMPLEMENTATION_EXISTS = True
except ImportError:
    IMPLEMENTATION_EXISTS = False


# =============================================================================
# AC#1: All 6 checks pass on valid installation
# =============================================================================

class TestValidInstallation:
    """Tests for AC#1: All 6 checks pass on valid installation."""

    @pytest.fixture
    def valid_project(self, tmp_path):
        """Create a valid DevForgeAI project structure for testing."""
        # Create context files
        context_dir = tmp_path / "devforgeai" / "specs" / "context"
        context_dir.mkdir(parents=True)
        context_files = [
            "tech-stack.md",
            "source-tree.md",
            "dependencies.md",
            "coding-standards.md",
            "architecture-constraints.md",
            "anti-patterns.md"
        ]
        for f in context_files:
            (context_dir / f).write_text(f"# {f}\nContent")

        # Create git directory and hooks
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir()
        (hooks_dir / "pre-commit").write_text("#!/bin/bash\n")

        # Create settings file
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text("{}")

        return tmp_path

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_validate_installation_all_checks_pass_on_valid_installation(self, valid_project):
        """AC#1: Given valid installation, all 6 checks should pass."""
        result = validate_installation_command(str(valid_project))

        assert result.success is True
        assert result.passed_count == 6
        assert result.failed_count == 0
        assert "PASS (6/6 checks passed)" in result.summary

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_cli_available_returns_pass_when_installed(self):
        """Check 1: CLI availability check passes when devforgeai-validate installed."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='devforgeai-validate 0.1.0')
            result = check_cli_available()

            assert result.passed is True
            assert "devforgeai-validate" in result.message

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_context_files_returns_pass_when_all_present(self, valid_project):
        """Check 2: Context files check passes when all 6 files present."""
        result = check_context_files(str(valid_project))

        assert result.passed is True
        assert "6/6 present" in result.message

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_hooks_installed_returns_pass_when_present(self, valid_project):
        """Check 3: Hook installation check passes when pre-commit exists."""
        result = check_hooks_installed(str(valid_project))

        assert result.passed is True
        assert "pre-commit installed" in result.message

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_pythonpath_returns_pass_when_configured(self):
        """Check 4: PYTHONPATH check passes when CLI imports succeed."""
        result = check_pythonpath()

        assert result.passed is True
        assert "configured" in result.message

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_git_repository_returns_pass_when_initialized(self, valid_project):
        """Check 5: Git repository check passes when .git exists."""
        result = check_git_repository(str(valid_project))

        assert result.passed is True
        assert "initialized" in result.message

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_settings_file_returns_pass_when_present(self, valid_project):
        """Check 6: Settings file check passes when .claude/settings.json exists."""
        result = check_settings_file(str(valid_project))

        assert result.passed is True
        assert "present" in result.message


# =============================================================================
# AC#2: Clear error for incomplete installation
# =============================================================================

class TestIncompleteInstallation:
    """Tests for AC#2: Clear error for incomplete installation."""

    @pytest.fixture
    def incomplete_project(self, tmp_path):
        """Create an incomplete DevForgeAI project (missing some files)."""
        # Only create 4 of 6 context files
        context_dir = tmp_path / "devforgeai" / "specs" / "context"
        context_dir.mkdir(parents=True)
        for f in ["tech-stack.md", "source-tree.md", "dependencies.md", "coding-standards.md"]:
            (context_dir / f).write_text(f"# {f}")

        # No git, no hooks, no settings
        return tmp_path

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_validate_installation_fails_on_incomplete_installation(self, incomplete_project):
        """AC#2: Given incomplete installation, should report failures clearly."""
        result = validate_installation_command(str(incomplete_project))

        assert result.success is False
        assert result.failed_count > 0
        assert "FAIL" in result.summary

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_cli_available_returns_clear_error_when_missing(self):
        """Check 1 Error: CLI not installed shows clear error message."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            result = check_cli_available()

            assert result.passed is False
            assert "CLI not installed" in result.message
            assert "To fix:" in result.fix_instruction
            assert "pip install -e .claude/scripts/" in result.fix_instruction

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_context_files_returns_missing_list_when_incomplete(self, tmp_path):
        """Check 2 Error: Missing context files listed with fix instruction."""
        # Create only 2 context files
        context_dir = tmp_path / "devforgeai" / "specs" / "context"
        context_dir.mkdir(parents=True)
        (context_dir / "tech-stack.md").write_text("# Tech Stack")
        (context_dir / "source-tree.md").write_text("# Source Tree")

        result = check_context_files(str(tmp_path))

        assert result.passed is False
        assert "2/6" in result.message or "Missing:" in result.message
        assert "To fix:" in result.fix_instruction
        assert "/create-context" in result.fix_instruction

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_hooks_installed_returns_error_when_missing(self, tmp_path):
        """Check 3 Error: Missing hooks shows clear error with fix instruction."""
        # Create .git but no hooks
        (tmp_path / ".git").mkdir()

        result = check_hooks_installed(str(tmp_path))

        assert result.passed is False
        assert "Hooks not installed" in result.message
        assert "To fix:" in result.fix_instruction

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_git_repository_returns_error_when_not_initialized(self, tmp_path):
        """Check 5 Error: Missing .git shows clear error with fix instruction."""
        result = check_git_repository(str(tmp_path))

        assert result.passed is False
        assert "Not a Git repository" in result.message
        assert "To fix:" in result.fix_instruction
        assert "git init" in result.fix_instruction

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_check_settings_file_returns_error_when_missing(self, tmp_path):
        """Check 6 Error: Missing settings file shows clear error."""
        result = check_settings_file(str(tmp_path))

        assert result.passed is False
        assert "Settings missing" in result.message
        assert "To fix:" in result.fix_instruction


# =============================================================================
# Business Rules
# =============================================================================

class TestBusinessRules:
    """Tests for business rules from Technical Specification."""

    @pytest.fixture
    def valid_project(self, tmp_path):
        """Create a valid project for testing."""
        # Create all required structure
        context_dir = tmp_path / "devforgeai" / "specs" / "context"
        context_dir.mkdir(parents=True)
        for f in ["tech-stack.md", "source-tree.md", "dependencies.md",
                  "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
            (context_dir / f).write_text(f"# {f}")

        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        (git_hooks / "pre-commit").write_text("#!/bin/bash")

        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text("{}")

        return tmp_path

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_br001_each_check_returns_pass_fail_with_clear_reason(self, valid_project):
        """BR-001: Each check must return pass/fail with clear reason."""
        # Test that each check function returns a ValidationResult with reason
        results = [
            check_git_repository(str(valid_project)),
            check_context_files(str(valid_project)),
            check_settings_file(str(valid_project)),
        ]

        for result in results:
            assert hasattr(result, 'passed')
            assert hasattr(result, 'message')
            assert isinstance(result.passed, bool)
            assert isinstance(result.message, str)
            assert len(result.message) > 0

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_br002_actionable_fix_suggested_for_each_failure(self, tmp_path):
        """BR-002: Actionable fix must be suggested for each failure."""
        # Test on empty project - all checks should fail with fix instructions
        result = validate_installation_command(str(tmp_path))

        # Each failure should have a fix instruction
        for check_result in result.checks:
            if not check_result.passed:
                assert hasattr(check_result, 'fix_instruction')
                assert "To fix:" in check_result.fix_instruction

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_br003_exit_code_0_only_if_all_checks_pass(self, valid_project):
        """BR-003: Exit code 0 only if all checks pass."""
        # Valid project should have exit code 0
        result_valid = validate_installation_command(str(valid_project))
        assert result_valid.exit_code == 0

        # Invalid project should have non-zero exit code
        # Use a separate temp directory since valid_project modifies tmp_path
        with tempfile.TemporaryDirectory() as invalid_dir:
            result_invalid = validate_installation_command(invalid_dir)
            assert result_invalid.exit_code != 0


# =============================================================================
# CLI Integration
# =============================================================================

class TestCLIIntegration:
    """Tests for CLI integration with argparse."""

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_cli_help_shows_validate_installation_command(self):
        """CLI-007: validate-installation subcommand should appear in --help."""
        import subprocess
        result = subprocess.run(
            ['devforgeai-validate', '--help'],
            capture_output=True,
            text=True
        )

        assert 'validate-installation' in result.stdout

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_cli_validate_installation_accepts_project_root_flag(self):
        """validate-installation should accept --project-root flag."""
        import subprocess
        result = subprocess.run(
            ['devforgeai-validate', 'validate-installation', '--help'],
            capture_output=True,
            text=True
        )

        assert '--project-root' in result.stdout


# =============================================================================
# Output Format Tests
# =============================================================================

class TestOutputFormat:
    """Tests for output format matching story specification."""

    @pytest.fixture
    def valid_project(self, tmp_path):
        """Create a valid project."""
        context_dir = tmp_path / "devforgeai" / "specs" / "context"
        context_dir.mkdir(parents=True)
        for f in ["tech-stack.md", "source-tree.md", "dependencies.md",
                  "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
            (context_dir / f).write_text(f"# {f}")

        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        (git_hooks / "pre-commit").write_text("#!/bin/bash")

        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.json").write_text("{}")

        return tmp_path

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_output_contains_checkmark_for_passed_checks(self, valid_project):
        """Output should show [✓] for passed checks."""
        result = validate_installation_command(str(valid_project))
        output = result.format_output()

        assert "[✓]" in output or "[✓]" in output.replace("✓", "✓")

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_output_contains_x_for_failed_checks(self, tmp_path):
        """Output should show [✗] for failed checks."""
        result = validate_installation_command(str(tmp_path))
        output = result.format_output()

        assert "[✗]" in output or "[✗]" in output.replace("✗", "✗")

    @pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not yet created")
    def test_output_header_shows_title(self, valid_project):
        """Output should have proper header."""
        result = validate_installation_command(str(valid_project))
        output = result.format_output()

        assert "DevForgeAI Installation Validation" in output
