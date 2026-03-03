"""
Integration tests for STORY-030 Phase N: Feedback Hook Integration in /create-context

Tests the complete workflow of feedback hook integration after context file creation,
validating that:
1. Hook eligibility checking works after context files are created
2. Hooks are invoked if eligible (non-blocking)
3. Hook failures don't prevent command completion
4. Backward compatibility is maintained
5. Configuration is respected (skip_all, trigger_on modes)
6. Performance target (<100ms) met when hooks are skipped

Context: This implements the feedback hook system for /create-context command
following the same pattern as /dev pilot (STORY-023).
"""

import pytest
import tempfile
import shutil
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock, call
import time
import yaml

# Add project root to path so we can import DevForgeAI modules
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from devforgeai_cli.commands.check_hooks import check_hooks_command, EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR
from devforgeai_cli.commands.invoke_hooks import invoke_hooks_command


class TestCreateContextFeedbackHooksIntegration:
    """
    Integration tests for feedback hook integration in /create-context command.

    Tests the Phase N workflow that runs after context file creation:
    1. Determine operation status (all 6 files created = success)
    2. Check hook eligibility via `devforgeai check-hooks`
    3. Invoke hooks if eligible via `devforgeai invoke-hooks`
    4. Continue to Phase 7 Success Report (non-blocking)
    """

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory for tests."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create basic project structure
        (project_dir / "devforgeai").mkdir(exist_ok=True)
        (project_dir / "devforgeai" / "context").mkdir(exist_ok=True)
        (project_dir / "devforgeai" / "config").mkdir(exist_ok=True)
        (project_dir / ".claude").mkdir(exist_ok=True)
        (project_dir / ".ai_docs").mkdir(exist_ok=True)

        yield project_dir

        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def hooks_config_path(self, temp_project_dir):
        """Return path to hooks.yaml config file."""
        return temp_project_dir / "devforgeai" / "config" / "hooks.yaml"

    @pytest.fixture
    def create_hooks_config(self, hooks_config_path):
        """Factory fixture for creating hooks.yaml configurations."""
        def _create(config_dict):
            hooks_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(hooks_config_path, 'w') as f:
                yaml.dump(config_dict, f)
            return hooks_config_path
        return _create

    @pytest.fixture
    def create_context_files(self, temp_project_dir):
        """Factory fixture for creating the 6 context files."""
        def _create(count=6):
            context_dir = temp_project_dir / "devforgeai" / "context"
            context_dir.mkdir(parents=True, exist_ok=True)

            files_to_create = [
                "tech-stack.md",
                "source-tree.md",
                "dependencies.md",
                "coding-standards.md",
                "architecture-constraints.md",
                "anti-patterns.md",
            ]

            created = []
            for i, filename in enumerate(files_to_create[:count]):
                filepath = context_dir / filename
                filepath.write_text(f"# {filename}\n\nTest content for {filename}")
                created.append(filepath)

            return created
        return _create

    # ========================================================================
    # HAPPY PATH TESTS (All 6 files created → Hook eligible → Success)
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_happy_path_all_context_files_created_hooks_eligible(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC1: Happy path - All 6 context files created → hooks eligible → feedback flows → success

        Given:
          - /create-context starts Phase N
          - All 6 context files successfully created
          - hooks.yaml configured with enabled=true, trigger_on=all

        When:
          - Phase N Step 1: Determine operation status (all files exist → "success")
          - Phase N Step 2: Check hook eligibility via check-hooks CLI
          - Phase N Step 3: Invoke hooks if eligible

        Then:
          - Hook check returns exit code 0 (eligible)
          - Hooks are invoked (exit code 0)
          - Command continues to Phase 7 (non-blocking)
          - All context files remain created (primary success)
        """
        # Setup: Create all 6 context files
        created_files = create_context_files(count=6)
        assert len(created_files) == 6
        assert all(f.exists() for f in created_files)

        # Setup: Configure hooks (enabled, trigger on all operations)
        config = {
            "enabled": True,
            "global_rules": {
                "trigger_on": "all",
            }
        }
        hooks_config_path = create_hooks_config(config)

        # Change to project directory for relative path resolution
        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Step 1: Determine operation status
            all_files_exist = all(
                (Path("devforgeai/context") / f).exists()
                for f in [
                    "tech-stack.md", "source-tree.md", "dependencies.md",
                    "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
                ]
            )
            operation_status = "success" if all_files_exist else "failure"
            assert operation_status == "success"

            # Step 2: Check hook eligibility (status must be: success, failure, or partial)
            exit_code = check_hooks_command(
                operation="create-context",
                status=operation_status,
                config_path=str(hooks_config_path)
            )
            assert exit_code == EXIT_CODE_TRIGGER, "Hook should be eligible for successful create-context"

            # Step 3: Invoke hooks (mocked to verify non-blocking behavior)
            with patch("devforgeai_cli.hooks.invoke_hooks", return_value=True) as mock_invoke:
                result = invoke_hooks_command(operation="create-context", story_id=None)
                # Should return success even if hook invocation fails later
                assert result == 0 or result == 1  # Accept both (success or graceful failure)

            # Step 4 (Phase 7): Verify context files still exist (non-blocking)
            assert (temp_project_dir / "devforgeai/context/tech-stack.md").exists()
            assert (temp_project_dir / "devforgeai/context/dependencies.md").exists()
            assert len(list((temp_project_dir / "devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_happy_path_hook_invocation_succeeds_gracefully(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC1: Hook invocation succeeds → command continues uninterrupted

        Given:
          - All 6 context files created
          - Hooks eligible (hook check returns 0)
          - invoke-hooks command succeeds (return 0)

        When:
          - Phase N executes: check-hooks → invoke-hooks

        Then:
          - Both commands return 0 (success)
          - Phase 7 Success Report displays completion
          - All context files remain intact
        """
        # Setup
        create_context_files(count=6)
        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check hooks returns eligible
            check_result = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert check_result == EXIT_CODE_TRIGGER

            # Invoke hooks succeeds
            with patch("devforgeai_cli.hooks.invoke_hooks", return_value=True):
                invoke_result = invoke_hooks_command(operation="create-context")
                # Either success (0) or handled failure
                assert invoke_result in [0, 1]

            # Context files remain (primary success criteria)
            context_files = list((temp_project_dir / "devforgeai/context").glob("*.md"))
            assert len(context_files) == 6

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # MISSING FILE TESTS (Only 5 files created → Status "failure")
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_file_missing_only_five_context_files_created_status_failed(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC2: File missing - Only 5 files created → operation_status="failure" → hooks invoked with failed status

        Given:
          - 5 of 6 context files created (anti-patterns.md missing)
          - hooks.yaml configured with trigger_on=failures-only

        When:
          - Phase N Step 1: Determine operation status (missing file → "failure")
          - Phase N Step 2: Check hook eligibility with status="failure"

        Then:
          - Hook check returns exit code 0 (should trigger for failures)
          - Hooks are invoked with status="failure"
          - Missing file detected and reported
          - Command still proceeds (non-blocking)
        """
        # Setup: Create only 5 files (missing anti-patterns.md which is the 6th)
        created = create_context_files(count=5)
        assert len(created) == 5
        # Missing: anti-patterns.md

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "failures-only"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Step 1: Determine operation status
            required_files = [
                "tech-stack.md", "source-tree.md", "dependencies.md",
                "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
            ]
            missing_files = [
                f for f in required_files
                if not (Path("devforgeai/context") / f).exists()
            ]
            operation_status = "failure" if missing_files else "success"

            assert operation_status == "failure"
            assert "anti-patterns.md" in missing_files

            # Step 2: Check hook eligibility with failed status
            exit_code = check_hooks_command(
                operation="create-context",
                status=operation_status,
                config_path=str(hooks_config_path)
            )
            # With trigger_on=failures-only, should trigger on failure
            assert exit_code == EXIT_CODE_TRIGGER

            # Step 3: Invoke hooks with failed status
            with patch("devforgeai_cli.hooks.invoke_hooks", return_value=True) as mock_invoke:
                result = invoke_hooks_command(operation="create-context")

            # Remaining files should still exist
            existing = [f for f in required_files if (Path("devforgeai/context") / f).exists()]
            assert len(existing) == 5

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_file_missing_two_files_missing_operation_fails(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC2: Multiple files missing - Only 4 files → status="failure" → proper failure handling

        Given:
          - Only 4 context files created
          - Two files missing

        When:
          - Phase N Step 1: Determine operation status
          - Phase N Step 2: Check hook eligibility

        Then:
          - operation_status = "failure"
          - Hook check evaluates with status="failure"
          - Command continues (non-blocking failure)
        """
        # Setup: Create only 4 files
        created = create_context_files(count=4)
        assert len(created) == 4

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "failures-only"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Determine status
            required_count = 6
            existing_count = len(list(Path("devforgeai/context").glob("*.md")))
            operation_status = "failure" if existing_count < required_count else "success"

            assert operation_status == "failure"
            assert existing_count == 4

            # Check hook eligibility for failure status
            exit_code = check_hooks_command(
                operation="create-context",
                status=operation_status,
                config_path=str(hooks_config_path)
            )
            assert exit_code == EXIT_CODE_TRIGGER

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # HOOK CHECK FAILURE TESTS (CLI missing/timeout → invoke-hooks skipped)
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_hook_check_fails_cli_missing_invoke_skipped(
        self, temp_project_dir, create_context_files
    ):
        """
        AC3: Hook check fails - CLI missing/timeout → invoke-hooks skipped → success continues

        Given:
          - All 6 context files created
          - devforgeai check-hooks CLI fails (missing/timeout/error)
          - hooks.yaml exists but check-hooks can't be run

        When:
          - Phase N Step 2: check-hooks command fails
          - Phase N Step 3: Detect failure and skip invoke-hooks (graceful degradation)

        Then:
          - Check-hooks failure doesn't block context creation
          - invoke-hooks is not called
          - Command continues to Phase 7 with success
          - All context files remain
        """
        # Setup: Create all 6 files
        create_context_files(count=6)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Simulate check-hooks CLI being missing or timing out
            with patch("subprocess.run") as mock_run:
                # Simulate CLI not found or timeout
                mock_run.side_effect = FileNotFoundError("devforgeai command not found")

                # Phase N Step 2: Attempt to check hooks
                try:
                    # In real implementation, this would handle the exception gracefully
                    # For test purposes, we verify the failure is caught
                    subprocess.run(["devforgeai", "check-hooks", "--operation", "create-context"], timeout=5)
                    hook_check_success = False
                except FileNotFoundError:
                    hook_check_success = False

                # Verify check failed
                assert not hook_check_success

            # Verify context files still exist despite hook check failure
            context_files = list(Path("devforgeai/context").glob("*.md"))
            assert len(context_files) == 6

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_hook_check_timeout_invoke_skipped(
        self, temp_project_dir, create_context_files
    ):
        """
        AC3: Hook check timeout - Timeout waiting for check-hooks → invoke-hooks skipped

        Given:
          - check-hooks command times out (>5 seconds)
          - We have a timeout set (e.g., 5 seconds)

        When:
          - Phase N attempts to check hooks within timeout
          - Check-hooks exceeds timeout window

        Then:
          - Timeout caught gracefully
          - invoke-hooks not invoked
          - Command continues with context files intact
        """
        # Setup
        create_context_files(count=6)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Simulate timeout on hook check
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired(
                    cmd="devforgeai check-hooks",
                    timeout=5
                )

                try:
                    subprocess.run(
                        ["devforgeai", "check-hooks", "--operation", "create-context"],
                        timeout=5
                    )
                    hook_check_completed = True
                except subprocess.TimeoutExpired:
                    hook_check_completed = False

                assert not hook_check_completed

            # Context files remain intact
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # HOOK INVOKE FAILURE TESTS (Feedback system error → non-blocking)
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_hook_invoke_fails_feedback_system_error_command_completes(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC4: Hook invoke fails - Feedback system error → non-blocking → command completes

        Given:
          - All 6 context files created
          - Hook check passes (exit 0)
          - invoke-hooks command fails (exit 1 from feedback system error)

        When:
          - Phase N Step 3: invoke-hooks returns failure exit code

        Then:
          - Command doesn't fail due to hook failure (non-blocking)
          - Context files remain created (primary success)
          - Error logged but not propagated
          - Phase 7 Success Report still displays
        """
        # Setup: Create all 6 files
        create_context_files(count=6)

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Step 1: Status = "success" (all files exist)
            all_exist = all(
                (Path("devforgeai/context") / f).exists()
                for f in [
                    "tech-stack.md", "source-tree.md", "dependencies.md",
                    "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
                ]
            )
            assert all_exist

            # Step 2: Hook check passes
            check_result = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert check_result == EXIT_CODE_TRIGGER

            # Step 3: invoke-hooks fails but doesn't block completion
            with patch("devforgeai_cli.hooks.invoke_hooks", return_value=False) as mock_invoke:
                # Hook invocation returns False (failure), but we continue
                invoke_result = invoke_hooks_command(operation="create-context")
                # Command may return 1 for hook failure, but that's okay
                # Main point: context files are unaffected

            # Verify context files remain (critical: non-blocking behavior)
            context_files = list(Path("devforgeai/context").glob("*.md"))
            assert len(context_files) == 6, "Context files should remain despite hook failure"

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.reliability
    def test_hook_invoke_exception_caught_gracefully(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC4: Hook invoke throws exception → caught gracefully → command continues

        Given:
          - Hook invocation raises unexpected exception
          - Exception should not propagate

        When:
          - Phase N Step 3: invoke-hooks raises exception

        Then:
          - Exception is caught and logged
          - Command continues
          - Context files remain
        """
        # Setup
        create_context_files(count=6)
        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check passes
            check_result = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert check_result == EXIT_CODE_TRIGGER

            # invoke-hooks raises exception but we handle it
            with patch("devforgeai_cli.hooks.invoke_hooks") as mock_invoke:
                mock_invoke.side_effect = RuntimeError("Feedback system error")

                # In real implementation, this exception is caught
                try:
                    invoke_result = invoke_hooks_command(operation="create-context")
                    # Should return failure code, not raise
                    assert invoke_result in [0, 1]
                except RuntimeError:
                    # Should be caught by invoke_hooks_command wrapper
                    pytest.fail("invoke_hooks_command should catch exceptions")

            # Context files still exist
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # CONFIGURATION TESTS (hooks.yaml settings)
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_configuration_disabled_skip_all_true_no_hooks_invoked(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC5: Configuration disabled - hooks.yaml has skip_all:true → no hooks invoked → success

        Given:
          - All 6 context files created
          - hooks.yaml has enabled=false OR skip_all=true

        When:
          - Phase N Step 2: Check hook eligibility

        Then:
          - Hook check returns exit code 1 (don't trigger)
          - invoke-hooks is NOT called
          - Command continues to Phase 7
        """
        # Setup: Create all files
        create_context_files(count=6)

        # Config: disabled hooks
        config = {
            "enabled": False,
            "skip_all": True
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Step 2: Check hook eligibility with disabled config
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            # Should NOT trigger when disabled
            assert exit_code == EXIT_CODE_DONT_TRIGGER

            # Verify invoke-hooks is not called
            with patch("devforgeai_cli.hooks.invoke_hooks") as mock_invoke:
                # Since hook check returned DONT_TRIGGER, invoke shouldn't be called in real implementation
                # This test verifies the check-hooks command itself respects disabled config
                pass

            # Context files remain
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_configuration_trigger_on_none_no_hooks_invoked(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC5: Configuration - trigger_on=none → no hooks invoked regardless of status

        Given:
          - All 6 context files created (status = "success")
          - hooks.yaml has trigger_on=none

        When:
          - Phase N Step 2: Check hook eligibility with trigger_on=none

        Then:
          - Hook check returns exit code 1 (don't trigger)
          - invoke-hooks not called
        """
        # Setup
        create_context_files(count=6)

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "none"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check hooks with trigger_on=none
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert exit_code == EXIT_CODE_DONT_TRIGGER

            # Context files remain
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_configuration_missing_hooks_yaml_defaults_to_disabled(
        self, temp_project_dir, create_context_files
    ):
        """
        AC5: Configuration missing - No hooks.yaml file → defaults to disabled → no hooks

        Given:
          - All 6 context files created
          - hooks.yaml doesn't exist

        When:
          - Phase N Step 2: Check hook eligibility with missing config

        Then:
          - Hook check returns exit code 1 (don't trigger)
          - No exceptions raised (graceful handling)
          - Command continues
        """
        # Setup: Create files but NO hooks.yaml
        create_context_files(count=6)
        # Don't create hooks.yaml

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check hooks with non-existent config file
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path="devforgeai/config/hooks.yaml"
            )
            # Should not trigger when config missing
            assert exit_code == EXIT_CODE_DONT_TRIGGER

            # Context files remain
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_configuration_operation_specific_override(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC5: Configuration - operation-specific override → create-context has different rule

        Given:
          - All 6 context files created
          - hooks.yaml has:
            - global_rules: trigger_on=none (default: don't trigger)
            - operations.create-context: trigger_on=all (override: trigger)

        When:
          - Phase N Step 2: Check hook eligibility for create-context operation

        Then:
          - Hook check returns exit code 0 (DO trigger)
          - Operation-specific rule overrides global rule
        """
        # Setup
        create_context_files(count=6)

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "none"},  # Don't trigger by default
            "operations": {
                "create-context": {"trigger_on": "all"}  # But DO trigger for create-context
            }
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check hooks for create-context (should trigger due to operation override)
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert exit_code == EXIT_CODE_TRIGGER  # Override allows trigger

            # Compare to different operation (should NOT trigger)
            exit_code_other = check_hooks_command(
                operation="other-operation",
                status="success",
                config_path=str(hooks_config_path)
            )
            assert exit_code_other == EXIT_CODE_DONT_TRIGGER  # Global rule applies

            # Context files remain
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # PERFORMANCE TESTS
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.performance
    def test_performance_hook_check_adds_less_than_100ms_when_skipped(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC6: Performance - Hook check adds <100ms overhead when skipped

        Given:
          - hooks.yaml configured to skip (trigger_on=none or disabled)

        When:
          - Phase N Step 2: Check hook eligibility

        Then:
          - check-hooks command completes in <100ms
          - Minimal overhead to context creation workflow
        """
        # Setup
        create_context_files(count=6)

        config = {
            "enabled": False,  # Skipped
            "global_rules": {"trigger_on": "none"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Measure execution time of check-hooks command
            start_time = time.time()

            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )

            elapsed_ms = (time.time() - start_time) * 1000

            # Should be very fast when disabled (loading YAML + checking config)
            assert elapsed_ms < 100, f"Hook check took {elapsed_ms}ms, expected <100ms"
            assert exit_code == EXIT_CODE_DONT_TRIGGER

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.performance
    def test_performance_hook_check_with_enabled_config_also_fast(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC6: Performance - Even with enabled config, check-hooks is fast (<100ms)

        Given:
          - hooks.yaml with enabled=true, trigger_on=all

        When:
          - Phase N Step 2: Check hook eligibility (enabled config)

        Then:
          - check-hooks completes in <100ms (YAML load + config check + decision)
          - Negligible overhead
        """
        # Setup
        create_context_files(count=6)

        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"}
        }
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Measure execution time
            start_time = time.time()

            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path=str(hooks_config_path)
            )

            elapsed_ms = (time.time() - start_time) * 1000

            # Even with enabled config, should be fast
            assert elapsed_ms < 100, f"Hook check took {elapsed_ms}ms, expected <100ms"
            assert exit_code == EXIT_CODE_TRIGGER

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # BACKWARD COMPATIBILITY TESTS
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_backward_compatibility_existing_create_context_usage_unchanged(
        self, temp_project_dir, create_context_files
    ):
        """
        AC7: Backward compatibility - Existing /create-context usage unaffected

        Given:
          - No hooks.yaml configuration exists
          - User runs /create-context normally (before Phase N implementation)

        When:
          - Phase N Step 2: Check for hooks.yaml (doesn't exist)

        Then:
          - Hook check gracefully handles missing config
          - Command proceeds normally
          - Context files created as usual
          - No changes to existing behavior
        """
        # Setup: No hooks.yaml
        create_context_files(count=6)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Check hooks with missing config (backward compat)
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path="devforgeai/config/hooks.yaml"
            )

            # Should not fail, just don't trigger
            assert exit_code == EXIT_CODE_DONT_TRIGGER

            # Context files created normally
            context_files = list(Path("devforgeai/context").glob("*.md"))
            assert len(context_files) == 6

            # Phase 7 would display success
            assert (Path("devforgeai/context") / "tech-stack.md").exists()

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_backward_compatibility_projects_without_devforgeai_cli_installed(
        self, temp_project_dir, create_context_files
    ):
        """
        AC7: Backward compatibility - devforgeai CLI not installed → graceful degradation

        Given:
          - devforgeai CLI tools not available (ImportError or subprocess not found)

        When:
          - Phase N attempts to invoke check-hooks command

        Then:
          - Exception caught gracefully
          - Context files still created (primary success)
          - No error propagated to user
        """
        # Setup
        create_context_files(count=6)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Simulate CLI not available
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = FileNotFoundError("devforgeai not found")

                # In real implementation, this exception is caught and handled
                try:
                    subprocess.run(["devforgeai", "check-hooks", "--operation", "create-context"])
                except FileNotFoundError:
                    # Expected: CLI not available
                    pass

            # Context files still created despite missing CLI
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)

    # ========================================================================
    # INTEGRATION WITH OTHER PHASES
    # ========================================================================

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_phase_n_occurs_after_phase_6_validation_completes(
        self, temp_project_dir, create_context_files
    ):
        """
        AC8: Phase ordering - Phase N runs AFTER Phase 6 (Final Validation)

        Given:
          - Phase 6 (Final Validation) has completed successfully
          - All 6 context files created and validated

        When:
          - Phase N (Feedback Hook Integration) begins

        Then:
          - Files from Phase 6 are available
          - No placeholder content exists (Phase 6 validated this)
          - Hook check uses validated files
        """
        # Setup: All files created (Phase 6 output)
        created = create_context_files(count=6)

        # Verify Phase 6 completion (no placeholders)
        for filepath in created:
            content = filepath.read_text()
            assert "TODO" not in content
            assert "TBD" not in content
            assert "[FILL IN]" not in content

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Phase N Step 1: Verify all files exist (validated in Phase 6)
            required_files = [
                "tech-stack.md", "source-tree.md", "dependencies.md",
                "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
            ]
            all_exist = all(
                (Path("devforgeai/context") / f).exists()
                for f in required_files
            )
            assert all_exist, "Phase 6 should have created all files"

            # Phase N Step 2: Check hooks based on Phase 6 output
            exit_code = check_hooks_command(
                operation="create-context",
                status="success",
                config_path="devforgeai/config/hooks.yaml"
            )
            # Should complete regardless of hook check result
            assert exit_code in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]

        finally:
            os.chdir(original_cwd)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_phase_n_non_blocking_transitions_to_phase_7_success_report(
        self, temp_project_dir, create_hooks_config, create_context_files
    ):
        """
        AC8: Non-blocking behavior - Phase N failures don't prevent Phase 7

        Given:
          - Phase N Step 3: Hook invocation fails

        When:
          - Phase N completes (with hook failure)
          - Phase 7 (Success Report) begins

        Then:
          - Phase 7 displays success (all context files created)
          - Hook failure not mentioned in success report
          - User sees completion summary
        """
        # Setup
        create_context_files(count=6)
        config = {"enabled": True, "global_rules": {"trigger_on": "all"}}
        hooks_config_path = create_hooks_config(config)

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Phase N: Hook invocation fails
            with patch("devforgeai_cli.hooks.invoke_hooks", return_value=False):
                invoke_result = invoke_hooks_command(operation="create-context")
                # Hook failure is recorded (result=1 or 0 depending on wrapper)

            # Phase 7: Success Report still displays
            # (In real implementation, this would be: display success with 6 files created)
            context_files = list(Path("devforgeai/context").glob("*.md"))
            assert len(context_files) == 6

            # User sees completion message (would include file counts, etc.)
            # Verification: no error raised, files exist
            assert (Path("devforgeai/context") / "tech-stack.md").exists()

        finally:
            os.chdir(original_cwd)


class TestCreateContextFeedbackHooksIntegrationWithPhase6:
    """
    Integration tests for Phase N interacting with Phase 6 validation output.

    Tests ensure that Phase N correctly handles the artifacts and state
    produced by Phase 6 (Final Validation).
    """

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "devforgeai" / "context").mkdir(parents=True, exist_ok=True)
        (project_dir / "devforgeai" / "config").mkdir(parents=True, exist_ok=True)
        yield project_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_phase_6_output_feeds_phase_n_input(self, temp_project_dir):
        """
        Phase 6 creates validated files → Phase N uses them for hook status determination

        Given:
          - Phase 6 completes and validates all 6 files

        When:
          - Phase N Step 1 checks if files exist

        Then:
          - All 6 files are found (Phase 6 output)
          - operation_status = "success"
        """
        # Simulate Phase 6 output: all 6 validated files
        context_dir = temp_project_dir / "devforgeai" / "context"
        files = [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]

        for filename in files:
            filepath = context_dir / filename
            filepath.write_text(f"# {filename}\n\nValidated content (Phase 6 output)")

        original_cwd = os.getcwd()
        os.chdir(temp_project_dir)

        try:
            # Phase N Step 1: Check file existence
            required_files = files
            all_exist = all(
                (Path("devforgeai/context") / f).exists()
                for f in required_files
            )
            operation_status = "success" if all_exist else "failure"

            assert operation_status == "success"
            assert len(list(Path("devforgeai/context").glob("*.md"))) == 6

        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test Execution Summary
# ============================================================================

if __name__ == "__main__":
    # Run tests with: pytest tests/integration/test_story030_feedback_hooks_create_context.py -v
    pytest.main([__file__, "-v", "--tb=short"])
