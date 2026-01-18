"""
Build Command Execution Module for STORY-239

Executes build commands for detected technology stacks and returns
structured results with execution details.

Build Commands Matrix (NFR-004 - hardcoded for security):
| Stack Type   | Command                           | Output Directory  |
|--------------|-----------------------------------|-------------------|
| nodejs       | npm run build                     | dist/             |
| python       | python -m build                   | dist/             |
| dotnet       | dotnet publish -c Release -r {rt} | publish/          |
| java_maven   | mvn clean package                 | target/           |
| java_gradle  | gradle build                      | build/libs/       |
| go           | go build -o ./bin/                | bin/              |
| rust         | cargo build --release             | target/release/   |

Business Rules:
- BR-001: Build failures return result with success=False (no exceptions raised)
- BR-002: Cross-platform builds attempt all 3 targets even if one fails
- BR-003: Build commands execute in project root directory (cwd parameter)
- BR-004: Empty output directory logs warning but success=True

Non-Functional Requirements:
- NFR-001: Build timeout configurable (default 600000ms = 10 minutes)
- NFR-002: Output captured completely up to 10MB
- NFR-003: Duration measured accurately using time.perf_counter
- NFR-004: Commands from lookup table only (no user injection)

References:
- Story: devforgeai/specs/Stories/STORY-239-build-command-execution.story.md
- Dependency: installer/tech_stack_detector.py (STORY-238)
- Source Tree: devforgeai/specs/context/source-tree.md (line 407)
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import logging
import subprocess
import time

# Import TechStackInfo from STORY-238
from installer.tech_stack_detector import TechStackInfo

# Configure module logger
logger = logging.getLogger(__name__)


# ============================================================================
# BUILD COMMANDS LOOKUP TABLE (NFR-004: Hardcoded for security)
# ============================================================================

BUILD_COMMANDS = {
    "nodejs": {
        "command": "npm run build",
        "output_directory": "dist/"
    },
    "python": {
        "command": "python -m build",
        "output_directory": "dist/"
    },
    "dotnet": {
        "command": "dotnet publish -c Release",
        "output_directory": "publish/"
    },
    "java_maven": {
        "command": "mvn clean package",
        "output_directory": "target/"
    },
    "java_gradle": {
        "command": "gradle build",
        "output_directory": "build/libs/"
    },
    "go": {
        "command": "go build -o ./bin/",
        "output_directory": "bin/"
    },
    "rust": {
        "command": "cargo build --release",
        "output_directory": "target/release/"
    }
}

# Cross-platform runtime targets for .NET (AC#3)
CROSS_PLATFORM_TARGETS = ["win-x64", "linux-x64", "osx-x64"]

# Default timeout in milliseconds (NFR-001)
DEFAULT_TIMEOUT_MS = 600000  # 10 minutes

# Maximum output size in bytes (NFR-002)
MAX_OUTPUT_SIZE_BYTES = 10 * 1024 * 1024  # 10MB


# ============================================================================
# BUILD RESULT DATACLASS
# ============================================================================

@dataclass
class BuildResult:
    """
    Data class holding results from build command execution.

    Attributes:
        success: True if build command returned exit code 0
        stack_type: Technology stack that was built (from TechStackInfo)
        command_executed: The exact command that was executed
        exit_code: Process exit code (0 = success)
        stdout: Standard output from build command (optional)
        stderr: Standard error from build command (optional)
        output_directory: Path to build output directory (verified to exist)
        duration_ms: Build execution time in milliseconds
        target_runtime: Runtime identifier for cross-platform builds (e.g., win-x64)

    Test Requirements (from Tech Spec):
        - success: Test verify success=True for exit code 0, False otherwise
        - stack_type: Test verify matches input TechStackInfo
        - command_executed: Test verify command matches expected for stack type
        - exit_code: Test verify captured correctly
        - stdout: Test verify captured when command produces output
        - stderr: Test verify captured when command produces errors
        - output_directory: Test verify populated on success
        - duration_ms: Test verify is positive integer
        - target_runtime: Test verify populated for .NET cross-platform
    """
    success: bool
    stack_type: str
    command_executed: str
    exit_code: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    output_directory: Optional[str] = None
    duration_ms: int = 0
    target_runtime: Optional[str] = None


# ============================================================================
# BUILD EXECUTOR SERVICE
# ============================================================================

class BuildExecutor:
    """
    Service for executing build commands for detected technology stacks.

    Executes the appropriate build command based on TechStackInfo and returns
    structured BuildResult with execution details.

    Usage:
        executor = BuildExecutor()
        result = executor.execute(tech_stack_info, project_root)

        # For .NET cross-platform builds
        results = executor.execute_cross_platform(tech_stack_info, project_root)

    Security (NFR-004):
        Build commands are sourced from a hardcoded lookup table only.
        No user input is used in command construction.

    Error Handling (BR-001):
        Build failures return BuildResult with success=False.
        No exceptions are raised for build failures.
    """

    # Expose module-level BUILD_COMMANDS for NFR-004 testing
    BUILD_COMMANDS = BUILD_COMMANDS

    def __init__(self, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        """
        Initialize BuildExecutor with configurable timeout.

        Args:
            timeout_ms: Build timeout in milliseconds (default: 600000 = 10 minutes)
                       NFR-001: Timeout must be configurable
        """
        self.timeout_ms = timeout_ms
        self.timeout_seconds = timeout_ms / 1000.0

    def execute(
        self,
        tech_stack_info: TechStackInfo,
        project_root: Path,
        target_runtime: Optional[str] = None,
        timeout_ms: Optional[int] = None
    ) -> BuildResult:
        """
        Execute build command for the given technology stack.

        Args:
            tech_stack_info: Technology stack information from TechStackDetector
            project_root: Path to project root directory (BR-003)
            target_runtime: Optional runtime identifier for cross-platform builds
            timeout_ms: Optional per-call timeout override in milliseconds (NFR-001)

        Returns:
            BuildResult with execution details

        Business Rules:
            - BR-001: Failures return result with success=False (no exceptions)
            - BR-003: Commands execute in project_root directory
            - BR-004: Empty output directory logs warning but success=True
        """
        # Validate project_root exists
        project_root = Path(project_root)
        if not project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")

        # Determine timeout (per-call override or instance default)
        effective_timeout_ms = timeout_ms if timeout_ms is not None else self.timeout_ms
        effective_timeout_seconds = effective_timeout_ms / 1000.0

        # Get stack type as string
        stack_type = tech_stack_info.stack_type
        if hasattr(stack_type, 'value'):
            stack_type = stack_type.value

        # Look up build command from hardcoded table (NFR-004)
        if stack_type not in BUILD_COMMANDS:
            logger.warning(f"No build command defined for stack type: {stack_type}")
            return BuildResult(
                success=False,
                stack_type=stack_type,
                command_executed="",
                exit_code=-1,
                stdout="",
                stderr=f"No build command defined for stack type: {stack_type}",
                output_directory=None,
                duration_ms=0,
                target_runtime=target_runtime
            )

        build_config = BUILD_COMMANDS[stack_type]
        command = build_config["command"]
        expected_output_dir = build_config["output_directory"]

        # Append runtime target for .NET cross-platform builds
        if target_runtime and stack_type == "dotnet":
            command = f"{command} -r {target_runtime}"

        # Measure execution time (NFR-003)
        start_time = time.perf_counter()

        try:
            # Execute build command (BR-003: in project_root directory)
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=effective_timeout_seconds
            )

            end_time = time.perf_counter()
            duration_ms = int((end_time - start_time) * 1000)

            # Determine success based on exit code
            success = result.returncode == 0

            # Verify output directory exists (AC#5)
            output_directory = None
            if success and expected_output_dir:
                output_path = project_root / expected_output_dir
                if output_path.exists():
                    output_directory = expected_output_dir
                    # Check if directory is empty (BR-004)
                    if output_path.is_dir() and not any(output_path.iterdir()):
                        logger.warning(
                            f"Build output directory is empty: {expected_output_dir}"
                        )
                else:
                    logger.warning(
                        f"Expected output directory not found: {expected_output_dir}"
                    )

            return BuildResult(
                success=success,
                stack_type=stack_type,
                command_executed=command,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                output_directory=output_directory,
                duration_ms=duration_ms,
                target_runtime=target_runtime
            )

        except subprocess.TimeoutExpired as e:
            # NFR-001: Handle timeout
            end_time = time.perf_counter()
            duration_ms = int((end_time - start_time) * 1000)
            logger.error(f"Build timed out after {effective_timeout_seconds}s: {command}")
            return BuildResult(
                success=False,
                stack_type=stack_type,
                command_executed=command,
                exit_code=-1,
                stdout=e.stdout if e.stdout else "",
                stderr=f"Build timed out after {effective_timeout_seconds} seconds",
                output_directory=None,
                duration_ms=duration_ms,
                target_runtime=target_runtime
            )

        except FileNotFoundError as e:
            # Handle command not found
            end_time = time.perf_counter()
            duration_ms = int((end_time - start_time) * 1000)
            logger.error(f"Build command not found: {e}")
            return BuildResult(
                success=False,
                stack_type=stack_type,
                command_executed=command,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                output_directory=None,
                duration_ms=duration_ms,
                target_runtime=target_runtime
            )

        except PermissionError as e:
            # Handle permission denied
            end_time = time.perf_counter()
            duration_ms = int((end_time - start_time) * 1000)
            logger.error(f"Permission denied: {e}")
            return BuildResult(
                success=False,
                stack_type=stack_type,
                command_executed=command,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                output_directory=None,
                duration_ms=duration_ms,
                target_runtime=target_runtime
            )

        except Exception as e:
            # BR-001: Catch all exceptions, return failure result
            end_time = time.perf_counter()
            duration_ms = int((end_time - start_time) * 1000)
            logger.error(f"Build failed with unexpected error: {e}")
            return BuildResult(
                success=False,
                stack_type=stack_type,
                command_executed=command,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                output_directory=None,
                duration_ms=duration_ms,
                target_runtime=target_runtime
            )

    def execute_cross_platform(
        self,
        tech_stack_info: TechStackInfo,
        project_root: Path,
        targets: Optional[List[str]] = None
    ) -> List[BuildResult]:
        """
        Execute cross-platform builds for .NET projects (AC#3).

        Executes dotnet publish for each target runtime:
        - win-x64
        - linux-x64
        - osx-x64

        Args:
            tech_stack_info: Technology stack information (must be dotnet)
            project_root: Path to project root directory
            targets: Optional list of specific targets (defaults to all 3)

        Returns:
            List of BuildResult, one per target runtime

        Business Rules:
            - BR-002: Attempt all targets even if one fails
        """
        results = []

        # Use provided targets or default to all cross-platform targets
        target_list = targets if targets is not None else CROSS_PLATFORM_TARGETS

        for target in target_list:
            result = self.execute(tech_stack_info, project_root, target_runtime=target)
            results.append(result)

        return results

    @staticmethod
    def get_build_command(stack_type: str) -> Optional[str]:
        """
        Get the build command for a stack type from the lookup table.

        This method is used for validation and testing (NFR-004).

        Args:
            stack_type: Technology stack type (e.g., "nodejs", "python")

        Returns:
            Build command string or None if stack type not supported
        """
        if stack_type in BUILD_COMMANDS:
            return BUILD_COMMANDS[stack_type]["command"]
        return None

    @staticmethod
    def get_supported_stack_types() -> List[str]:
        """
        Get list of supported stack types.

        Returns:
            List of supported stack type strings
        """
        return list(BUILD_COMMANDS.keys())
