"""
Pytest configuration and fixtures for STORY-239 Build Executor tests.

Provides mock infrastructure for subprocess execution, file system operations,
and test data factories for all 7 supported stack types.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from dataclasses import dataclass
from typing import Optional
import tempfile
import os


# ============================================================================
# TechStackInfo Mock (from STORY-238)
# ============================================================================

@dataclass
class MockTechStackInfo:
    """
    Mock of TechStackInfo from STORY-238 for test isolation.

    Mirrors the real TechStackInfo dataclass structure.
    """
    stack_type: str
    indicator_file: str
    build_command: Optional[str] = None
    output_directory: Optional[str] = None
    version_file: Optional[str] = None
    detection_confidence: float = 1.0


# ============================================================================
# TechStackInfo Fixtures (7 stack types)
# ============================================================================

@pytest.fixture
def nodejs_stack_info():
    """TechStackInfo for Node.js project."""
    return MockTechStackInfo(
        stack_type="nodejs",
        indicator_file="package.json",
        build_command="npm run build",
        output_directory="dist/",
        version_file="package.json",
        detection_confidence=1.0
    )


@pytest.fixture
def python_stack_info():
    """TechStackInfo for Python project with pyproject.toml."""
    return MockTechStackInfo(
        stack_type="python",
        indicator_file="pyproject.toml",
        build_command="python -m build",
        output_directory="dist/",
        version_file="pyproject.toml",
        detection_confidence=1.0
    )


@pytest.fixture
def dotnet_stack_info():
    """TechStackInfo for .NET project."""
    return MockTechStackInfo(
        stack_type="dotnet",
        indicator_file="MyProject.csproj",
        build_command="dotnet publish -c Release",
        output_directory="publish/",
        version_file=None,
        detection_confidence=1.0
    )


@pytest.fixture
def java_maven_stack_info():
    """TechStackInfo for Java Maven project."""
    return MockTechStackInfo(
        stack_type="java_maven",
        indicator_file="pom.xml",
        build_command="mvn package",
        output_directory="target/",
        version_file="pom.xml",
        detection_confidence=1.0
    )


@pytest.fixture
def java_gradle_stack_info():
    """TechStackInfo for Java Gradle project."""
    return MockTechStackInfo(
        stack_type="java_gradle",
        indicator_file="build.gradle",
        build_command="gradle build",
        output_directory="build/",
        version_file="build.gradle",
        detection_confidence=1.0
    )


@pytest.fixture
def go_stack_info():
    """TechStackInfo for Go project."""
    return MockTechStackInfo(
        stack_type="go",
        indicator_file="go.mod",
        build_command="go build",
        output_directory="./",
        version_file="go.mod",
        detection_confidence=1.0
    )


@pytest.fixture
def rust_stack_info():
    """TechStackInfo for Rust project."""
    return MockTechStackInfo(
        stack_type="rust",
        indicator_file="Cargo.toml",
        build_command="cargo build --release",
        output_directory="target/release/",
        version_file="Cargo.toml",
        detection_confidence=1.0
    )


# ============================================================================
# Subprocess Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_subprocess_success():
    """
    Mock subprocess that returns success (exit code 0).

    Returns:
        MagicMock configured for successful command execution
    """
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = "Build successful!\nOutput written to dist/"
    mock.stderr = ""
    return mock


@pytest.fixture
def mock_subprocess_failure():
    """
    Mock subprocess that returns failure (exit code 1).

    Returns:
        MagicMock configured for failed command execution
    """
    mock = MagicMock()
    mock.returncode = 1
    mock.stdout = ""
    mock.stderr = "Error: Module not found\nBuild failed"
    return mock


@pytest.fixture
def mock_subprocess_timeout():
    """
    Mock subprocess that raises TimeoutExpired.

    Returns:
        MagicMock that raises subprocess.TimeoutExpired
    """
    import subprocess
    mock = MagicMock()
    mock.side_effect = subprocess.TimeoutExpired(cmd="npm run build", timeout=600)
    return mock


# ============================================================================
# Temporary Project Directory Fixtures
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """
    Create a temporary project directory for testing.

    Yields:
        Path to temporary directory (cleaned up after test)
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_project_with_output(temp_project_dir):
    """
    Create a temporary project with a populated output directory.

    Args:
        temp_project_dir: Parent temporary directory

    Yields:
        Tuple of (project_path, output_path)
    """
    output_dir = temp_project_dir / "dist"
    output_dir.mkdir()
    # Create a dummy output file
    (output_dir / "bundle.js").write_text("// built output")
    yield temp_project_dir, output_dir


@pytest.fixture
def temp_project_empty_output(temp_project_dir):
    """
    Create a temporary project with an empty output directory.

    Args:
        temp_project_dir: Parent temporary directory

    Yields:
        Tuple of (project_path, empty_output_path)
    """
    output_dir = temp_project_dir / "dist"
    output_dir.mkdir()
    # Directory exists but is empty
    yield temp_project_dir, output_dir


# ============================================================================
# Large Output Fixtures (NFR-002)
# ============================================================================

@pytest.fixture
def large_stdout_output():
    """
    Generate large stdout output (5MB+) for NFR-002 testing.

    Returns:
        String of at least 5MB of build output
    """
    # Generate at least 5MB of output (add 1 to ensure >= 5MB)
    line = "Building module X... [OK]\n"
    line_count = (5 * 1024 * 1024) // len(line) + 1
    return line * line_count


@pytest.fixture
def mock_subprocess_large_output(large_stdout_output):
    """
    Mock subprocess with large stdout (5MB+).

    Returns:
        MagicMock configured with large output
    """
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = large_stdout_output
    mock.stderr = ""
    return mock


# ============================================================================
# .NET Cross-Platform Fixtures (AC#3)
# ============================================================================

@pytest.fixture
def dotnet_cross_platform_targets():
    """
    Return the 3 cross-platform targets for .NET builds.

    Returns:
        List of runtime identifiers
    """
    return ["win-x64", "linux-x64", "osx-x64"]


@pytest.fixture
def mock_dotnet_partial_success():
    """
    Mock .NET cross-platform build where one target fails.

    Returns:
        Dict mapping target to (exit_code, stdout, stderr)
    """
    return {
        "win-x64": (0, "Published to publish/win-x64/", ""),
        "linux-x64": (1, "", "Error: Missing native dependency"),
        "osx-x64": (0, "Published to publish/osx-x64/", ""),
    }


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def default_timeout_ms():
    """Default build timeout (10 minutes = 600000ms)."""
    return 600000


@pytest.fixture
def custom_timeout_ms():
    """Custom build timeout (30 seconds = 30000ms)."""
    return 30000


@pytest.fixture
def max_output_bytes():
    """Maximum output capture size (10MB)."""
    return 10 * 1024 * 1024  # 10MB


# ============================================================================
# Build Command Lookup Table Fixture (NFR-004)
# ============================================================================

@pytest.fixture
def build_command_lookup():
    """
    Hardcoded build command lookup table.

    This is the ONLY source for build commands (no user injection).

    Returns:
        Dict mapping stack_type to command template
    """
    return {
        "nodejs": "npm run build",
        "python": "python -m build",
        "dotnet": "dotnet publish -c Release -r {runtime}",
        "java_maven": "mvn clean package",
        "java_gradle": "gradle build",
        "go": "go build -o ./bin/",
        "rust": "cargo build --release",
    }
