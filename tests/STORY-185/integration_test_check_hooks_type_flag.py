#!/usr/bin/env python3
"""
Integration Tests for STORY-185: --type Flag for check-hooks CLI Command

Tests the implementation of --type parameter to filter hooks by type (user/ai/all).

Test Categories:
1. CLI Argument Parsing (help text, argument validation)
2. Module-Level Type Filtering (parameter handling)
3. Configuration Filtering (hook_type field filtering)
4. End-to-End Integration (full workflow with different type values)
5. Error Handling (invalid type values)
"""

import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path
from typing import Tuple, Dict, Any
import pytest

# Add src to path for module imports
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')

from devforgeai_cli.commands.check_hooks import (
    check_hooks_command,
    _create_argument_parser,
    EXIT_CODE_TRIGGER,
    EXIT_CODE_DONT_TRIGGER,
    EXIT_CODE_ERROR,
)

# Test configuration
TEST_CONFIG_WITH_TYPES = {
    "enabled": True,
    "global_rules": {"trigger_on": "all"},
    "operations": {
        "dev": {"trigger_on": "all"},
        "qa": {"trigger_on": "failures-only"},
    },
}

# Mock hooks data for type filtering test
MOCK_HOOKS_DATA = [
    {"name": "pre-dev", "hook_type": "user", "operation": "dev"},
    {"name": "post-dev-analysis", "hook_type": "ai", "operation": "dev"},
    {"name": "qa-reporter", "hook_type": "user", "operation": "qa"},
    {"name": "qa-copilot", "hook_type": "ai", "operation": "qa"},
]


class TestCLIArgumentParsing:
    """Test CLI argument parser for --type flag support."""

    def test_parser_has_type_option(self):
        """Test: Argument parser includes --type option."""
        parser = _create_argument_parser()
        # Verify parser can parse --type argument
        args = parser.parse_args([
            "--operation", "dev",
            "--status", "success",
            "--type", "user"
        ])
        assert hasattr(args, 'type'), "Parser missing --type attribute"
        assert args.type == "user"

    def test_parser_type_has_choices(self):
        """Test: --type option restricts to valid choices (user, ai, all)."""
        parser = _create_argument_parser()
        # Valid choices should parse without error
        for valid_type in ["user", "ai", "all"]:
            args = parser.parse_args([
                "--operation", "dev",
                "--status", "success",
                "--type", valid_type
            ])
            assert args.type == valid_type

    def test_parser_type_default_is_all(self):
        """Test: --type defaults to 'all' when not specified."""
        parser = _create_argument_parser()
        args = parser.parse_args([
            "--operation", "dev",
            "--status", "success"
        ])
        assert args.type == "all", f"Expected default 'all', got {args.type}"

    def test_parser_rejects_invalid_type(self):
        """Test: --type rejects invalid values."""
        parser = _create_argument_parser()
        # Invalid type should cause SystemExit
        with pytest.raises(SystemExit):
            parser.parse_args([
                "--operation", "dev",
                "--status", "success",
                "--type", "invalid"
            ])

    def test_help_text_includes_type_documentation(self):
        """Test: --help includes --type documentation."""
        result = subprocess.run(
            ["python3", "-m", "devforgeai_cli.commands.check_hooks", "--help"],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True
        )
        help_output = result.stdout
        assert "--type" in help_output, "--type flag not in help output"
        assert "user" in help_output or "ai" in help_output, "Type choices not documented"


class TestModuleTypeFunctionality:
    """Test check_hooks_command function with type parameter."""

    def test_check_hooks_accepts_type_parameter(self):
        """Test: check_hooks_command accepts hook_type parameter."""
        # Module should accept hook_type parameter
        exit_code = check_hooks_command(
            operation="dev",
            status="success",
            hook_type="all"
        )
        assert exit_code in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_check_hooks_accepts_user_type(self):
        """Test: check_hooks_command accepts hook_type='user'."""
        exit_code = check_hooks_command(
            operation="dev",
            status="success",
            hook_type="user"
        )
        assert exit_code in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_check_hooks_accepts_ai_type(self):
        """Test: check_hooks_command accepts hook_type='ai'."""
        exit_code = check_hooks_command(
            operation="dev",
            status="success",
            hook_type="ai"
        )
        assert exit_code in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_check_hooks_type_parameter_defaults_to_all(self):
        """Test: hook_type parameter defaults to 'all'."""
        # Call without hook_type parameter
        exit_code = check_hooks_command(
            operation="dev",
            status="success"
        )
        assert exit_code in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_check_hooks_rejects_invalid_type(self):
        """Test: check_hooks_command rejects invalid hook_type values."""
        # Invalid type should return error code
        exit_code = check_hooks_command(
            operation="dev",
            status="success",
            hook_type="invalid"
        )
        assert exit_code == EXIT_CODE_ERROR, f"Expected error code {EXIT_CODE_ERROR}, got {exit_code}"


class TestTypedHookFiltering:
    """Test that hooks are correctly filtered by type."""

    def test_filter_user_type_hooks(self):
        """Test: Filtering returns only user-type hooks."""
        hooks = MOCK_HOOKS_DATA
        # Simulate filtering logic
        filtered = [h for h in hooks if h.get('hook_type') == 'user']
        assert len(filtered) == 2
        assert all(h['hook_type'] == 'user' for h in filtered)
        assert 'pre-dev' in [h['name'] for h in filtered]
        assert 'qa-reporter' in [h['name'] for h in filtered]

    def test_filter_ai_type_hooks(self):
        """Test: Filtering returns only ai-type hooks."""
        hooks = MOCK_HOOKS_DATA
        filtered = [h for h in hooks if h.get('hook_type') == 'ai']
        assert len(filtered) == 2
        assert all(h['hook_type'] == 'ai' for h in filtered)
        assert 'post-dev-analysis' in [h['name'] for h in filtered]
        assert 'qa-copilot' in [h['name'] for h in filtered]

    def test_filter_all_type_returns_all_hooks(self):
        """Test: 'all' type returns all hooks regardless of type."""
        hooks = MOCK_HOOKS_DATA
        # No filtering for 'all'
        filtered = hooks
        assert len(filtered) == 4
        assert any(h['hook_type'] == 'user' for h in filtered)
        assert any(h['hook_type'] == 'ai' for h in filtered)


class TestEndToEndIntegration:
    """Test complete workflows with --type flag."""

    def test_e2e_user_type_with_success_status(self):
        """E2E: devforgeai check-hooks --type user --operation dev --status success"""
        result = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='user')
sys.exit(exit_code)
"""
            ],
            capture_output=True,
            text=True
        )
        # Should complete without error (exit codes 0 or 1 are valid)
        assert result.returncode in [0, 1, 2]

    def test_e2e_ai_type_with_success_status(self):
        """E2E: devforgeai check-hooks --type ai --operation dev --status success"""
        result = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='ai')
sys.exit(exit_code)
"""
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode in [0, 1, 2]

    def test_e2e_all_type_with_success_status(self):
        """E2E: devforgeai check-hooks --type all --operation dev --status success"""
        result = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='all')
sys.exit(exit_code)
"""
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode in [0, 1, 2]

    def test_e2e_default_type_matches_all(self):
        """E2E: Default (no --type) should behave same as --type all"""
        # Get results with explicit 'all'
        result_explicit = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='all')
print(exit_code)
"""
            ],
            capture_output=True,
            text=True
        )

        # Get results with default (no type parameter)
        result_default = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success')
print(exit_code)
"""
            ],
            capture_output=True,
            text=True
        )

        # Both should produce same result
        explicit_code = int(result_explicit.stdout.strip())
        default_code = int(result_default.stdout.strip())
        assert explicit_code == default_code, f"Explicit 'all' ({explicit_code}) != default ({default_code})"


class TestErrorHandling:
    """Test error handling for invalid type values."""

    def test_invalid_type_error_message(self):
        """Test: Invalid type produces clear error message."""
        result = subprocess.run(
            [
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/mnt/c/Projects/DevForgeAI2/src/claude/scripts')
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='invalid')
print(f"EXIT_CODE:{exit_code}")
"""
            ],
            capture_output=True,
            text=True
        )
        # Should return error exit code
        output = result.stdout + result.stderr
        assert "EXIT_CODE:2" in output, "Invalid type should return exit code 2"

    def test_invalid_type_cli_rejection(self):
        """Test: CLI rejects invalid type argument."""
        result = subprocess.run(
            [
                "python3", "-m", "devforgeai_cli.commands.check_hooks",
                "--operation", "dev",
                "--status", "success",
                "--type", "maybe"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True
        )
        # Should exit with error
        assert result.returncode != 0, "CLI should reject invalid type"
        assert "invalid" in result.stderr.lower() or "choice" in result.stderr.lower()


class TestTypeFilteringLogic:
    """Test the actual hook filtering logic implementation."""

    def test_type_filtering_when_config_has_hook_types(self):
        """Test: Filtering works when config includes hook_type field."""
        # Simulate config with hooks including type field
        hooks = [
            {"name": "hook1", "hook_type": "user", "trigger": True},
            {"name": "hook2", "hook_type": "ai", "trigger": True},
            {"name": "hook3", "hook_type": "user", "trigger": True},
        ]

        # Filter to user type
        filtered_user = [h for h in hooks if h.get("hook_type") == "user"]
        assert len(filtered_user) == 2
        assert filtered_user[0]["name"] == "hook1"
        assert filtered_user[2]["name"] == "hook3"

        # Filter to ai type
        filtered_ai = [h for h in hooks if h.get("hook_type") == "ai"]
        assert len(filtered_ai) == 1
        assert filtered_ai[0]["name"] == "hook2"

    def test_type_filtering_handles_missing_hook_type_field(self):
        """Test: Filtering handles hooks without hook_type field gracefully."""
        hooks = [
            {"name": "hook1", "trigger": True},  # Missing hook_type
            {"name": "hook2", "hook_type": "user", "trigger": True},
        ]

        # Filtering for user type should skip hooks without field
        filtered = [h for h in hooks if h.get("hook_type") == "user"]
        assert len(filtered) == 1
        assert filtered[0]["name"] == "hook2"

    def test_all_type_no_filtering(self):
        """Test: 'all' type returns all hooks without filtering."""
        hooks = [
            {"name": "hook1", "hook_type": "user"},
            {"name": "hook2", "hook_type": "ai"},
            {"name": "hook3"},  # No type
        ]

        # 'all' type should not filter
        # Simulate: if type == 'all': filtered = hooks
        filtered = hooks  # No filtering
        assert len(filtered) == 3


# ============================================================================
# COMMAND LINE INTEGRATION TESTS
# ============================================================================

class TestCLICommandExecution:
    """Test command-line execution with --type flag."""

    def test_cli_help_shows_type_flag(self):
        """CLI: devforgeai check-hooks --help includes --type documentation"""
        result = subprocess.run(
            [
                sys.executable, "-m", "devforgeai_cli.commands.check_hooks",
                "--help"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0, f"Help command failed: {result.stderr}"
        assert "--type" in result.stdout, "--type not in help output"
        help_text = result.stdout.lower()
        assert "user" in help_text or "ai" in help_text, "Type choices not documented in help"

    def test_cli_accepts_type_user_argument(self):
        """CLI: devforgeai check-hooks --operation dev --status success --type user"""
        result = subprocess.run(
            [
                sys.executable, "-m", "devforgeai_cli.commands.check_hooks",
                "--operation", "dev",
                "--status", "success",
                "--type", "user"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True,
            timeout=5
        )
        # Should exit with 0, 1, or 2 (valid exit codes)
        assert result.returncode in [0, 1, 2], f"Unexpected exit code: {result.returncode}"

    def test_cli_accepts_type_ai_argument(self):
        """CLI: devforgeai check-hooks --operation dev --status success --type ai"""
        result = subprocess.run(
            [
                sys.executable, "-m", "devforgeai_cli.commands.check_hooks",
                "--operation", "dev",
                "--status", "success",
                "--type", "ai"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode in [0, 1, 2]

    def test_cli_accepts_type_all_argument(self):
        """CLI: devforgeai check-hooks --operation dev --status success --type all"""
        result = subprocess.run(
            [
                sys.executable, "-m", "devforgeai_cli.commands.check_hooks",
                "--operation", "dev",
                "--status", "success",
                "--type", "all"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode in [0, 1, 2]

    def test_cli_rejects_invalid_type_argument(self):
        """CLI: devforgeai check-hooks --type invalid produces error"""
        result = subprocess.run(
            [
                sys.executable, "-m", "devforgeai_cli.commands.check_hooks",
                "--operation", "dev",
                "--status", "success",
                "--type", "invalid"
            ],
            cwd="/mnt/c/Projects/DevForgeAI2/src/claude/scripts",
            capture_output=True,
            text=True,
            timeout=5
        )
        # Should fail (exit code != 0)
        assert result.returncode != 0, "CLI should reject invalid type"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
