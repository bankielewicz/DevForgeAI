"""
STORY-239: Build Command Execution Module Tests

Test-Driven Development (TDD) - GREEN PHASE
Tests for BuildExecutor service that executes build commands for detected technology stacks.

Test Coverage:
- AC#1: Node.js Build Execution (3 tests)
- AC#2: Python Build Execution (2 tests)
- AC#3: .NET Cross-Platform Build (4 tests)
- AC#4: Build Failure Handling (3 tests)
- AC#5: Build Output Directory Verification (2 tests)

Technical Specification Requirements:
- BuildResult dataclass with 9 fields
- BuildExecutor service with execute() method
- 7 stack types: Node.js, Python, .NET, Maven, Gradle, Go, Rust
- BR-001: Build failures must not halt workflow
- BR-002: Cross-platform builds attempt all targets
- BR-003: Build commands execute in project root
- BR-004: Empty output directory logs warning but doesn't fail
- NFR-001: Build timeout configurable (default 10 minutes)
- NFR-002: Output captured completely up to 10MB
- NFR-003: Duration measured accurately
- NFR-004: Commands from lookup table only (no injection)

Test File: tests/STORY-239/test_build_executor.py
Module Under Test: installer/build_executor.py

Reference:
- Story: devforgeai/specs/Stories/STORY-239-build-command-execution.story.md
- Source Tree: devforgeai/specs/context/source-tree.md (line 407)
"""

# CRITICAL: Add project root to sys.path BEFORE any other imports
# This must be at the very top to ensure installer module can be imported
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(_project_root))  # Always insert to ensure it's first

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
import subprocess
import time


# ============================================================================
# MODULE IMPORT
# ============================================================================

# Import the module under test - now implemented in TDD Green phase
from installer.build_executor import BuildResult, BuildExecutor


# ============================================================================
# BUILDRESULT DATACLASS TESTS (9 FIELDS)
# ============================================================================

class TestBuildResultDataclass:
    """
    Tests for BuildResult dataclass structure and field validation.

    Technical Specification Requirements:
    - 9 fields: success, stack_type, command_executed, exit_code,
                stdout, stderr, output_directory, duration_ms, target_runtime
    """

    def test_buildresult_has_success_field(self):
        """
        Test: BuildResult has 'success' boolean field.

        Source: STORY-239 Tech Spec, lines 96-100
        Field: success (Bool, Required)
        """
        result = BuildResult(
            success=True,
            stack_type="nodejs",
            command_executed="npm run build",
            exit_code=0,
            stdout="",
            stderr="",
            output_directory="dist/",
            duration_ms=1000,
            target_runtime=None
        )
        assert hasattr(result, 'success')
        assert isinstance(result.success, bool)

    def test_buildresult_has_stack_type_field(self):
        """
        Test: BuildResult has 'stack_type' string field.

        Source: STORY-239 Tech Spec, lines 101-105
        Field: stack_type (String, Required)
        """
        result = BuildResult(
            success=True,
            stack_type="python",
            command_executed="python -m build",
            exit_code=0,
            stdout="",
            stderr="",
            output_directory="dist/",
            duration_ms=1000,
            target_runtime=None
        )
        assert hasattr(result, 'stack_type')
        assert isinstance(result.stack_type, str)
        assert result.stack_type == "python"

    def test_buildresult_has_command_executed_field(self):
        """
        Test: BuildResult has 'command_executed' string field.

        Source: STORY-239 Tech Spec, lines 106-110
        Field: command_executed (String, Required)
        """
        result = BuildResult(
            success=True,
            stack_type="dotnet",
            command_executed="dotnet publish -c Release -r win-x64",
            exit_code=0,
            stdout="",
            stderr="",
            output_directory="publish/",
            duration_ms=1000,
            target_runtime="win-x64"
        )
        assert hasattr(result, 'command_executed')
        assert "dotnet publish" in result.command_executed

    def test_buildresult_has_exit_code_field(self):
        """
        Test: BuildResult has 'exit_code' integer field.

        Source: STORY-239 Tech Spec, lines 111-115
        Field: exit_code (Int, Required)
        """
        result = BuildResult(
            success=False,
            stack_type="nodejs",
            command_executed="npm run build",
            exit_code=1,
            stdout="",
            stderr="Error",
            output_directory=None,
            duration_ms=500,
            target_runtime=None
        )
        assert hasattr(result, 'exit_code')
        assert isinstance(result.exit_code, int)
        assert result.exit_code == 1

    def test_buildresult_has_stdout_field(self):
        """
        Test: BuildResult has 'stdout' string field (optional).

        Source: STORY-239 Tech Spec, lines 116-120
        Field: stdout (String, Optional)
        """
        result = BuildResult(
            success=True,
            stack_type="go",
            command_executed="go build",
            exit_code=0,
            stdout="Build successful",
            stderr="",
            output_directory="./",
            duration_ms=2000,
            target_runtime=None
        )
        assert hasattr(result, 'stdout')
        assert result.stdout == "Build successful"

    def test_buildresult_has_stderr_field(self):
        """
        Test: BuildResult has 'stderr' string field (optional).

        Source: STORY-239 Tech Spec, lines 121-125
        Field: stderr (String, Optional)
        """
        result = BuildResult(
            success=False,
            stack_type="rust",
            command_executed="cargo build --release",
            exit_code=101,
            stdout="",
            stderr="error[E0433]: failed to resolve",
            output_directory=None,
            duration_ms=3000,
            target_runtime=None
        )
        assert hasattr(result, 'stderr')
        assert "error" in result.stderr

    def test_buildresult_has_output_directory_field(self):
        """
        Test: BuildResult has 'output_directory' optional string field.

        Source: STORY-239 Tech Spec, lines 126-130
        Field: output_directory (Optional[String])
        """
        result = BuildResult(
            success=True,
            stack_type="java_maven",
            command_executed="mvn clean package",
            exit_code=0,
            stdout="BUILD SUCCESS",
            stderr="",
            output_directory="target/",
            duration_ms=15000,
            target_runtime=None
        )
        assert hasattr(result, 'output_directory')
        assert result.output_directory == "target/"

    def test_buildresult_has_duration_ms_field(self):
        """
        Test: BuildResult has 'duration_ms' integer field.

        Source: STORY-239 Tech Spec, lines 131-135
        Field: duration_ms (Int, Required)
        """
        result = BuildResult(
            success=True,
            stack_type="java_gradle",
            command_executed="gradle build",
            exit_code=0,
            stdout="BUILD SUCCESSFUL",
            stderr="",
            output_directory="build/",
            duration_ms=8500,
            target_runtime=None
        )
        assert hasattr(result, 'duration_ms')
        assert isinstance(result.duration_ms, int)
        assert result.duration_ms == 8500

    def test_buildresult_has_target_runtime_field(self):
        """
        Test: BuildResult has 'target_runtime' optional string field.

        Source: STORY-239 Tech Spec, lines 136-140
        Field: target_runtime (Optional[String])
        """
        result = BuildResult(
            success=True,
            stack_type="dotnet",
            command_executed="dotnet publish -c Release -r linux-x64",
            exit_code=0,
            stdout="Published",
            stderr="",
            output_directory="publish/linux-x64/",
            duration_ms=12000,
            target_runtime="linux-x64"
        )
        assert hasattr(result, 'target_runtime')
        assert result.target_runtime == "linux-x64"


# ============================================================================
# AC#1: NODE.JS BUILD EXECUTION
# ============================================================================

class TestNodeJsBuildExecution:
    """
    AC#1: Node.js Build Execution Tests

    Given the TechStackDetector has identified a Node.js project,
    When the BuildExecutor is invoked,
    Then it executes `npm run build` in the project directory,
    And captures stdout/stderr output,
    And returns success if exit code is 0.
    """

    @patch('subprocess.run')
    def test_execute_nodejs_build_runs_npm_command(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: npm run build command executed.

        Source: STORY-239 AC#1, line 33
        Verifies: SVC-001 - Execute Node.js build via npm run build
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        # Verify npm run build was called
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert "npm" in call_args[0][0] or "npm" in str(call_args)
        assert "run" in str(call_args)
        assert "build" in str(call_args)

    @patch('subprocess.run')
    def test_execute_nodejs_build_captures_stdout_stderr(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: stdout/stderr captured.

        Source: STORY-239 AC#1, line 34
        Verifies: SVC-008 - Capture stdout/stderr from build command
        """
        expected_stdout = "webpack 5.88.0 compiled successfully"
        expected_stderr = "Warning: deprecated API usage"

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=expected_stdout,
            stderr=expected_stderr
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.stdout == expected_stdout
        assert result.stderr == expected_stderr

    @patch('subprocess.run')
    def test_execute_nodejs_build_returns_success_on_exit_code_zero(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: Exit code 0 returns success=True.

        Source: STORY-239 AC#1, line 35
        Verifies: BuildResult.success = True when exit code is 0
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build successful",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.success is True
        assert result.exit_code == 0
        assert result.stack_type == "nodejs"


# ============================================================================
# AC#2: PYTHON BUILD EXECUTION
# ============================================================================

class TestPythonBuildExecution:
    """
    AC#2: Python Build Execution Tests

    Given the TechStackDetector has identified a Python project with pyproject.toml,
    When the BuildExecutor is invoked,
    Then it executes `python -m build` in the project directory,
    And captures stdout/stderr output,
    And returns success if exit code is 0.
    """

    @patch('subprocess.run')
    def test_execute_python_build_runs_python_m_build_command(
        self,
        mock_run,
        python_stack_info,
        temp_project_dir
    ):
        """
        Test: python -m build command executed.

        Source: STORY-239 AC#2, line 42
        Verifies: SVC-002 - Execute Python build via python -m build
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Successfully built mypackage-1.0.0.tar.gz",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(python_stack_info, project_root=temp_project_dir)

        mock_run.assert_called_once()
        call_args = str(mock_run.call_args)
        assert "python" in call_args
        assert "-m" in call_args
        assert "build" in call_args

    @patch('subprocess.run')
    def test_execute_python_build_captures_output(
        self,
        mock_run,
        python_stack_info,
        temp_project_dir
    ):
        """
        Test: Output captured for Python build.

        Source: STORY-239 AC#2, lines 43-44
        Verifies: SVC-008 - Capture stdout/stderr from build command
        """
        expected_stdout = (
            "* Creating virtualenv isolated environment...\n"
            "* Installing packages in isolated environment...\n"
            "* Getting build dependencies...\n"
            "* Building wheel...\n"
            "Successfully built mypackage-1.0.0-py3-none-any.whl"
        )

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=expected_stdout,
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(python_stack_info, project_root=temp_project_dir)

        assert result.stdout == expected_stdout
        assert result.success is True
        assert result.stack_type == "python"


# ============================================================================
# AC#3: .NET CROSS-PLATFORM BUILD
# ============================================================================

class TestDotNetCrossPlatformBuild:
    """
    AC#3: .NET Cross-Platform Build Tests

    Given the TechStackDetector has identified a .NET project,
    When the BuildExecutor is invoked with cross-platform targets,
    Then it executes `dotnet publish -c Release -r {runtime}` for each target:
        - win-x64
        - linux-x64
        - osx-x64
    And captures output for each build,
    And returns success if all builds complete with exit code 0.
    """

    @patch('subprocess.run')
    def test_execute_dotnet_build_for_win_x64(
        self,
        mock_run,
        dotnet_stack_info,
        temp_project_dir,
        dotnet_cross_platform_targets
    ):
        """
        Test: dotnet publish executed for win-x64.

        Source: STORY-239 AC#3, line 53
        Verifies: SVC-003 - Execute .NET build with cross-platform targets
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Published to publish/win-x64/",
            stderr=""
        )

        executor = BuildExecutor()
        results = executor.execute_cross_platform(
            dotnet_stack_info,
            project_root=temp_project_dir,
            targets=["win-x64"]
        )

        assert len(results) == 1
        assert results[0].target_runtime == "win-x64"
        assert "win-x64" in results[0].command_executed

    @patch('subprocess.run')
    def test_execute_dotnet_build_for_linux_x64(
        self,
        mock_run,
        dotnet_stack_info,
        temp_project_dir
    ):
        """
        Test: dotnet publish executed for linux-x64.

        Source: STORY-239 AC#3, line 54
        Verifies: SVC-003 - Execute .NET build with cross-platform targets
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Published to publish/linux-x64/",
            stderr=""
        )

        executor = BuildExecutor()
        results = executor.execute_cross_platform(
            dotnet_stack_info,
            project_root=temp_project_dir,
            targets=["linux-x64"]
        )

        assert len(results) == 1
        assert results[0].target_runtime == "linux-x64"
        assert results[0].success is True

    @patch('subprocess.run')
    def test_execute_dotnet_build_for_osx_x64(
        self,
        mock_run,
        dotnet_stack_info,
        temp_project_dir
    ):
        """
        Test: dotnet publish executed for osx-x64.

        Source: STORY-239 AC#3, line 55
        Verifies: SVC-003 - Execute .NET build with cross-platform targets
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Published to publish/osx-x64/",
            stderr=""
        )

        executor = BuildExecutor()
        results = executor.execute_cross_platform(
            dotnet_stack_info,
            project_root=temp_project_dir,
            targets=["osx-x64"]
        )

        assert len(results) == 1
        assert results[0].target_runtime == "osx-x64"
        assert results[0].success is True

    @patch('subprocess.run')
    def test_execute_dotnet_cross_platform_returns_all_three_results(
        self,
        mock_run,
        dotnet_stack_info,
        temp_project_dir,
        dotnet_cross_platform_targets
    ):
        """
        Test: All 3 builds return results.

        Source: STORY-239 AC#3, lines 56-58
        Verifies: 3 separate BuildResult objects returned
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Published successfully",
            stderr=""
        )

        executor = BuildExecutor()
        results = executor.execute_cross_platform(
            dotnet_stack_info,
            project_root=temp_project_dir,
            targets=dotnet_cross_platform_targets
        )

        assert len(results) == 3
        assert mock_run.call_count == 3

        runtimes = [r.target_runtime for r in results]
        assert "win-x64" in runtimes
        assert "linux-x64" in runtimes
        assert "osx-x64" in runtimes


# ============================================================================
# AC#4: BUILD FAILURE HANDLING
# ============================================================================

class TestBuildFailureHandling:
    """
    AC#4: Build Failure Handling Tests

    Given any build command execution,
    When the build command returns a non-zero exit code,
    Then the BuildExecutor:
    - Captures the full error output
    - Returns a BuildResult with `success=False`
    - Includes the exit code and error message
    - Does NOT halt the release workflow (allows recovery)
    """

    @patch('subprocess.run')
    def test_nonzero_exit_code_returns_success_false(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: Non-zero exit code returns success=False.

        Source: STORY-239 AC#4, line 68
        Verifies: SVC-009 - Handle build failures gracefully
        """
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="npm ERR! Missing script: build"
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.success is False
        assert result.exit_code == 1

    @patch('subprocess.run')
    def test_error_output_captured_in_stderr(
        self,
        mock_run,
        python_stack_info,
        temp_project_dir
    ):
        """
        Test: Error output captured in stderr.

        Source: STORY-239 AC#4, line 67
        Verifies: BuildResult.stderr contains error message
        """
        error_message = (
            "ERROR: Could not find a version that satisfies the requirement\n"
            "ERROR: No matching distribution found"
        )

        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr=error_message
        )

        executor = BuildExecutor()
        result = executor.execute(python_stack_info, project_root=temp_project_dir)

        assert result.stderr == error_message
        assert result.success is False

    @patch('subprocess.run')
    def test_workflow_does_not_halt_on_failure(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: Workflow does not halt on failure (no exception raised).

        Source: STORY-239 AC#4, line 70
        Verifies: BR-001 - Build failures must not halt workflow
        """
        mock_run.return_value = MagicMock(
            returncode=127,
            stdout="",
            stderr="command not found: npm"
        )

        executor = BuildExecutor()

        # Should NOT raise an exception
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        # Result should be returned with failure status
        assert result is not None
        assert result.success is False
        assert result.exit_code == 127


# ============================================================================
# AC#5: BUILD OUTPUT DIRECTORY VERIFICATION
# ============================================================================

class TestBuildOutputDirectoryVerification:
    """
    AC#5: Build Output Directory Verification Tests

    Given a successful build execution,
    When the build completes,
    Then the BuildExecutor verifies the output directory exists,
    And logs a warning if expected output directory is empty,
    And includes the output directory path in the BuildResult.
    """

    @patch('subprocess.run')
    def test_output_directory_populated_on_success(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_with_output
    ):
        """
        Test: Output directory populated on success.

        Source: STORY-239 AC#5, lines 77-78
        Verifies: SVC-010 - Verify output directory exists after successful build
        """
        project_dir, output_dir = temp_project_with_output

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(
            nodejs_stack_info,
            project_root=project_dir
        )

        assert result.success is True
        assert result.output_directory is not None
        assert "dist" in result.output_directory or output_dir.name in result.output_directory

    @patch('subprocess.run')
    @patch('installer.build_executor.logger')
    def test_warning_logged_for_empty_output_directory(
        self,
        mock_logger,
        mock_run,
        nodejs_stack_info,
        temp_project_empty_output
    ):
        """
        Test: Warning logged for empty output directory.

        Source: STORY-239 AC#5, line 79
        Verifies: BR-004 - Empty output directory should log warning but not fail
        """
        project_dir, empty_output_dir = temp_project_empty_output

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(
            nodejs_stack_info,
            project_root=project_dir
        )

        # Should still succeed
        assert result.success is True

        # Warning should be logged
        mock_logger.warning.assert_called()
        warning_message = str(mock_logger.warning.call_args)
        assert "empty" in warning_message.lower() or "output" in warning_message.lower()


# ============================================================================
# ADDITIONAL STACK TYPE TESTS (SVC-004 to SVC-007)
# ============================================================================

class TestAdditionalStackTypes:
    """
    Tests for Maven, Gradle, Go, and Rust build execution.

    Verifies SVC-004 through SVC-007 from Tech Spec.
    """

    @patch('subprocess.run')
    def test_execute_maven_build_runs_mvn_command(
        self,
        mock_run,
        java_maven_stack_info,
        temp_project_dir
    ):
        """
        Test: mvn clean package command executed.

        Source: STORY-239 Tech Spec SVC-004, lines 167-170
        Verifies: Execute Java Maven build via mvn clean package
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="BUILD SUCCESS",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(java_maven_stack_info, project_root=temp_project_dir)

        call_args = str(mock_run.call_args)
        assert "mvn" in call_args
        assert result.stack_type == "java_maven"
        assert result.success is True

    @patch('subprocess.run')
    def test_execute_gradle_build_runs_gradle_command(
        self,
        mock_run,
        java_gradle_stack_info,
        temp_project_dir
    ):
        """
        Test: gradle build command executed.

        Source: STORY-239 Tech Spec SVC-005, lines 171-175
        Verifies: Execute Java Gradle build via gradle build
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="BUILD SUCCESSFUL",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(java_gradle_stack_info, project_root=temp_project_dir)

        call_args = str(mock_run.call_args)
        assert "gradle" in call_args
        assert result.stack_type == "java_gradle"
        assert result.success is True

    @patch('subprocess.run')
    def test_execute_go_build_runs_go_command(
        self,
        mock_run,
        go_stack_info,
        temp_project_dir
    ):
        """
        Test: go build -o ./bin/ command executed.

        Source: STORY-239 Tech Spec SVC-006, lines 176-180
        Verifies: Execute Go build via go build -o ./bin/
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(go_stack_info, project_root=temp_project_dir)

        call_args = str(mock_run.call_args)
        assert "go" in call_args
        assert "build" in call_args
        assert result.stack_type == "go"
        assert result.success is True

    @patch('subprocess.run')
    def test_execute_rust_build_runs_cargo_command(
        self,
        mock_run,
        rust_stack_info,
        temp_project_dir
    ):
        """
        Test: cargo build --release command executed.

        Source: STORY-239 Tech Spec SVC-007, lines 181-185
        Verifies: Execute Rust build via cargo build --release
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Compiling myproject v0.1.0\nFinished release",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(rust_stack_info, project_root=temp_project_dir)

        call_args = str(mock_run.call_args)
        assert "cargo" in call_args
        assert "release" in call_args
        assert result.stack_type == "rust"
        assert result.success is True


# ============================================================================
# BUSINESS RULE TESTS (BR-001 to BR-004)
# ============================================================================

class TestBusinessRules:
    """
    Tests for Business Rules from Technical Specification.

    BR-001: Build failures must not halt workflow
    BR-002: Cross-platform builds attempt all targets even if one fails
    BR-003: Build commands execute in project root directory
    BR-004: Empty output directory logs warning but doesn't fail
    """

    @patch('subprocess.run')
    def test_br001_failed_build_returns_result_no_exception(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: BR-001 - Failed build returns result, does not raise exception.

        Source: STORY-239 Tech Spec BR-001, lines 227-232
        """
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Build failed"
        )

        executor = BuildExecutor()

        # Should NOT raise exception
        try:
            result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)
            exception_raised = False
        except Exception:
            exception_raised = True

        assert not exception_raised
        assert result.success is False

    @patch('subprocess.run')
    def test_br002_cross_platform_continues_after_one_target_fails(
        self,
        mock_run,
        dotnet_stack_info,
        temp_project_dir,
        dotnet_cross_platform_targets
    ):
        """
        Test: BR-002 - One target fails, other 2 still execute.

        Source: STORY-239 Tech Spec BR-002, lines 234-239
        """
        # First call fails, others succeed
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="win-x64 success", stderr=""),
            MagicMock(returncode=1, stdout="", stderr="linux-x64 failed"),
            MagicMock(returncode=0, stdout="osx-x64 success", stderr=""),
        ]

        executor = BuildExecutor()
        results = executor.execute_cross_platform(
            dotnet_stack_info,
            project_root=temp_project_dir,
            targets=dotnet_cross_platform_targets
        )

        # All 3 should have been attempted
        assert len(results) == 3
        assert mock_run.call_count == 3

        # Verify which succeeded/failed
        success_count = sum(1 for r in results if r.success)
        failure_count = sum(1 for r in results if not r.success)

        assert success_count == 2
        assert failure_count == 1

    @patch('subprocess.run')
    def test_br003_build_executes_in_project_root_directory(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: BR-003 - Verify cwd is project root during build.

        Source: STORY-239 Tech Spec BR-003, lines 241-246
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        # Verify subprocess.run was called with cwd=project_root
        call_kwargs = mock_run.call_args.kwargs
        assert 'cwd' in call_kwargs
        assert str(call_kwargs['cwd']) == str(temp_project_dir) or \
               Path(call_kwargs['cwd']) == temp_project_dir

    @patch('subprocess.run')
    @patch('installer.build_executor.logger')
    def test_br004_empty_output_dir_logs_warning_success_still_true(
        self,
        mock_logger,
        mock_run,
        nodejs_stack_info,
        temp_project_empty_output
    ):
        """
        Test: BR-004 - Empty output dir logs warning, success=True still.

        Source: STORY-239 Tech Spec BR-004, lines 248-253
        """
        project_dir, empty_output_dir = temp_project_empty_output

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=project_dir)

        # Success should still be True
        assert result.success is True

        # Warning should have been logged
        assert mock_logger.warning.called


# ============================================================================
# NON-FUNCTIONAL REQUIREMENT TESTS (NFR-001 to NFR-004)
# ============================================================================

class TestNonFunctionalRequirements:
    """
    Tests for Non-Functional Requirements from Technical Specification.

    NFR-001: Build timeout configurable (default 10 minutes)
    NFR-002: Output captured completely up to 10MB
    NFR-003: Duration measured accurately
    NFR-004: Commands from lookup table only (no injection)
    """

    @patch('subprocess.run')
    def test_nfr001_build_times_out_after_configured_duration(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir,
        default_timeout_ms
    ):
        """
        Test: NFR-001 - Build times out after configured duration.

        Source: STORY-239 Tech Spec NFR-001, lines 257-261
        Default timeout: 10 minutes (600000ms)
        """
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="npm run build",
            timeout=600
        )

        executor = BuildExecutor()
        result = executor.execute(
            nodejs_stack_info,
            project_root=temp_project_dir,
            timeout_ms=default_timeout_ms
        )

        # Should return a result with timeout indication
        assert result.success is False
        assert "timeout" in result.stderr.lower() or result.exit_code == -1

    @patch('subprocess.run')
    def test_nfr001_custom_timeout_respected(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir,
        custom_timeout_ms
    ):
        """
        Test: NFR-001 - Custom timeout is respected.

        Source: STORY-239 Tech Spec NFR-001, lines 257-261
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(
            nodejs_stack_info,
            project_root=temp_project_dir,
            timeout_ms=custom_timeout_ms
        )

        # Verify timeout was passed to subprocess
        call_kwargs = mock_run.call_args.kwargs
        assert 'timeout' in call_kwargs
        # Convert ms to seconds
        expected_timeout_seconds = custom_timeout_ms / 1000
        assert call_kwargs['timeout'] == expected_timeout_seconds

    @patch('subprocess.run')
    def test_nfr002_large_output_captured_completely(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir,
        large_stdout_output
    ):
        """
        Test: NFR-002 - Large output (5MB) captured completely.

        Source: STORY-239 Tech Spec NFR-002, lines 263-267
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=large_stdout_output,
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        # Verify large output was captured
        assert len(result.stdout) >= 5 * 1024 * 1024  # At least 5MB
        assert result.success is True

    @patch('subprocess.run')
    def test_nfr003_duration_measured_accurately(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: NFR-003 - Duration measured accurately within 100ms.

        Source: STORY-239 Tech Spec NFR-003, lines 269-273
        """
        # Simulate a build that takes ~500ms
        def slow_build(*args, **kwargs):
            time.sleep(0.5)  # 500ms
            return MagicMock(
                returncode=0,
                stdout="Build complete",
                stderr=""
            )

        mock_run.side_effect = slow_build

        executor = BuildExecutor()

        start_time = time.time()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)
        actual_duration_ms = (time.time() - start_time) * 1000

        # Duration should be within 100ms of actual
        assert abs(result.duration_ms - actual_duration_ms) < 100

    def test_nfr004_command_uses_hardcoded_lookup_table(
        self,
        build_command_lookup
    ):
        """
        Test: NFR-004 - Commands from lookup table only (no injection).

        Source: STORY-239 Tech Spec NFR-004, lines 275-279
        """
        executor = BuildExecutor()

        # Verify executor uses hardcoded lookup table
        assert hasattr(executor, 'BUILD_COMMANDS') or hasattr(executor, 'COMMAND_LOOKUP')

        # Verify all 7 stack types have commands
        lookup = getattr(executor, 'BUILD_COMMANDS', None) or \
                 getattr(executor, 'COMMAND_LOOKUP', None)

        assert lookup is not None
        for stack_type in ["nodejs", "python", "dotnet", "java_maven",
                           "java_gradle", "go", "rust"]:
            assert stack_type in lookup

    @patch('subprocess.run')
    def test_nfr004_no_user_injection_in_command(
        self,
        mock_run,
        temp_project_dir
    ):
        """
        Test: NFR-004 - User input cannot inject commands.

        Source: STORY-239 Tech Spec NFR-004, lines 275-279
        Verifies: Build commands are constructed safely from lookup table
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )

        # Attempt to inject malicious command via stack_type
        malicious_stack_info = Mock()
        malicious_stack_info.stack_type = "nodejs; rm -rf /"
        malicious_stack_info.indicator_file = "package.json"

        executor = BuildExecutor()

        # Should either use lookup table (ignoring malicious stack_type)
        # or reject the unknown stack_type
        try:
            result = executor.execute(malicious_stack_info, project_root=temp_project_dir)
            # If it succeeds, verify no shell injection occurred
            call_args = str(mock_run.call_args)
            assert "rm -rf" not in call_args
        except (ValueError, KeyError):
            # Rejecting unknown stack_type is also acceptable
            pass


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """
    Edge case tests for robust error handling.
    """

    @patch('subprocess.run')
    def test_command_not_found_returns_failure(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: 'command not found' returns BuildResult with success=False.

        Source: STORY-239 Test Strategy, line 371
        """
        mock_run.return_value = MagicMock(
            returncode=127,
            stdout="",
            stderr="npm: command not found"
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.success is False
        assert result.exit_code == 127
        assert "not found" in result.stderr

    @patch('subprocess.run')
    def test_permission_denied_returns_failure(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: 'permission denied' returns BuildResult with success=False.

        Source: STORY-239 Test Strategy, line 372
        """
        mock_run.side_effect = PermissionError("Permission denied")

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.success is False
        assert "permission" in result.stderr.lower() or result.exit_code != 0

    @patch('subprocess.run')
    def test_empty_stdout_stderr_handled(
        self,
        mock_run,
        go_stack_info,
        temp_project_dir
    ):
        """
        Test: Empty stdout/stderr handled gracefully.

        Go builds often produce no output on success.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(go_stack_info, project_root=temp_project_dir)

        assert result.success is True
        assert result.stdout == ""
        assert result.stderr == ""

    @patch('subprocess.run')
    def test_nonexistent_project_root_raises_error(
        self,
        mock_run,
        nodejs_stack_info
    ):
        """
        Test: Non-existent project root raises appropriate error.
        """
        nonexistent_path = Path("/nonexistent/path/to/project")

        executor = BuildExecutor()

        with pytest.raises((FileNotFoundError, ValueError)):
            executor.execute(nodejs_stack_info, project_root=nonexistent_path)

    @patch('subprocess.run')
    def test_duration_zero_when_instant_build(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: duration_ms is non-negative even for instant builds.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert result.duration_ms >= 0


# ============================================================================
# SVC-011: DURATION MEASUREMENT TEST
# ============================================================================

class TestDurationMeasurement:
    """
    Tests for SVC-011: Build duration measurement.

    Verifies duration_ms is accurate within 100ms.
    """

    @patch('subprocess.run')
    def test_svc011_duration_is_positive_integer(
        self,
        mock_run,
        nodejs_stack_info,
        temp_project_dir
    ):
        """
        Test: SVC-011 - duration_ms is non-negative integer.

        Source: STORY-239 Tech Spec SVC-011, lines 201-205
        Note: With mocked subprocess, duration may be 0ms (instant return).
              The important property is that it's a valid non-negative integer.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        executor = BuildExecutor()
        result = executor.execute(nodejs_stack_info, project_root=temp_project_dir)

        assert isinstance(result.duration_ms, int)
        assert result.duration_ms >= 0  # Can be 0 with instant mock return


# ============================================================================
# INTEGRATION-STYLE TESTS (Using real TechStackInfo from STORY-238)
# ============================================================================

class TestIntegrationWithTechStackDetector:
    """
    Integration tests that use the real TechStackInfo from STORY-238.

    These tests verify the contract between TechStackDetector and BuildExecutor.
    """

    @patch('subprocess.run')
    def test_buildexecutor_accepts_real_techstackinfo(
        self,
        mock_run,
        temp_project_dir
    ):
        """
        Test: BuildExecutor accepts TechStackInfo from STORY-238.

        Verifies integration contract between modules.
        """
        # Import real TechStackInfo
        try:
            from installer.tech_stack_detector import TechStackInfo
        except ImportError:
            pytest.skip("TechStackInfo from STORY-238 not available")

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build complete",
            stderr=""
        )

        real_info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file="package.json",
            detection_confidence=1.0
        )

        executor = BuildExecutor()
        result = executor.execute(real_info, project_root=temp_project_dir)

        assert result.success is True
        assert result.stack_type == "nodejs"
