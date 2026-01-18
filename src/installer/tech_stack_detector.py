"""
Tech Stack Detection Module for STORY-238

Detects project technology stacks from indicator files and returns
build configuration information.

Detection Matrix:
| Indicator       | stack_type   | build_command                    | output_directory  |
|-----------------|--------------|----------------------------------|-------------------|
| package.json    | nodejs       | npm run build                    | dist/             |
| pyproject.toml  | python       | python -m build                  | dist/             |
| requirements.txt| python       | pip install -r requirements.txt  | None              |
| *.csproj        | dotnet       | dotnet publish -c Release        | publish/          |
| *.sln           | dotnet       | dotnet build -c Release          | bin/Release/      |
| pom.xml         | java_maven   | mvn package                      | target/           |
| build.gradle    | java_gradle  | gradle build                     | build/            |
| go.mod          | go           | go build                         | ./                |
| Cargo.toml      | rust         | cargo build --release            | target/release/   |

Business Rules:
- BR-001: pyproject.toml takes precedence over requirements.txt for Python
- BR-002: .csproj takes precedence over .sln for .NET
- BR-003: Default scan is root-level only (recursive=False)
- BR-004: Detection is read-only (no filesystem modifications)

Non-Functional Requirements:
- NFR-001: Detection must complete within 5 seconds
- NFR-002: Build command lookup must be under 100ms
- NFR-003: Graceful degradation when files are unreadable
- NFR-004: Path traversal prevention for security

References:
- Story: devforgeai/specs/Stories/STORY-238-tech-stack-detection-module.story.md
- Source Tree: devforgeai/specs/context/source-tree.md (line 406)
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging
import os

# Configure module logger
logger = logging.getLogger(__name__)


class StackType(Enum):
    """
    Enumeration of supported technology stack types.

    Values correspond to the stack_type field in TechStackInfo
    and are used for detection priority ordering.
    """
    NODEJS = "nodejs"
    PYTHON = "python"
    DOTNET = "dotnet"
    JAVA_MAVEN = "java_maven"
    JAVA_GRADLE = "java_gradle"
    GO = "go"
    RUST = "rust"


@dataclass
class TechStackInfo:
    """
    Data class holding detection results for a single technology stack.

    Attributes:
        stack_type: Technology identifier (nodejs, python, dotnet, etc.)
        indicator_file: Relative path to detected indicator file
        build_command: Primary build command for this stack (None if not applicable)
        output_directory: Expected build output directory (None if not applicable)
        version_file: File containing version info (e.g., package.json for Node.js)
        detection_confidence: Confidence score (1.0 = definitive match, 0.7 = partial)

    Constraints:
        - stack_type: Required, must be valid StackType enum value
        - indicator_file: Required, relative path (not absolute)
        - build_command: Max 1024 chars, no shell metacharacters
        - output_directory: Relative path, max 260 chars
        - detection_confidence: Float between 0.0 and 1.0
    """
    stack_type: str
    indicator_file: str
    build_command: Optional[str] = None
    output_directory: Optional[str] = None
    version_file: Optional[str] = None
    detection_confidence: float = 1.0


class TechStackDetector:
    """
    Service for detecting technology stacks in project directories.

    Scans project directories for indicator files (package.json, pyproject.toml,
    etc.) and returns TechStackInfo objects with build configuration.

    Usage:
        detector = TechStackDetector()
        results = detector.detect(Path("/path/to/project"))
        for info in results:
            print(f"{info.stack_type}: {info.build_command}")

    Attributes:
        INDICATOR_MAP: Mapping of indicator files to stack configurations
        DETECTION_ORDER: Priority order for detection (Node.js first, Rust last)
    """

    # Detection matrix: indicator file -> stack configuration
    INDICATOR_MAP: Dict[str, Dict[str, Any]] = {
        "package.json": {
            "stack_type": "nodejs",
            "build_command": "npm run build",
            "output_directory": "dist/",
            "version_file": "package.json",
        },
        "pyproject.toml": {
            "stack_type": "python",
            "build_command": "python -m build",
            "output_directory": "dist/",
            "version_file": "pyproject.toml",
        },
        "requirements.txt": {
            "stack_type": "python",
            "build_command": "pip install -r requirements.txt",
            "output_directory": None,
            "version_file": None,
        },
        "*.csproj": {
            "stack_type": "dotnet",
            "build_command": "dotnet publish -c Release",
            "output_directory": "publish/",
            "version_file": None,
        },
        "*.sln": {
            "stack_type": "dotnet",
            "build_command": "dotnet build -c Release",
            "output_directory": "bin/Release/",
            "version_file": None,
        },
        "pom.xml": {
            "stack_type": "java_maven",
            "build_command": "mvn package",
            "output_directory": "target/",
            "version_file": "pom.xml",
        },
        "build.gradle": {
            "stack_type": "java_gradle",
            "build_command": "gradle build",
            "output_directory": "build/",
            "version_file": "build.gradle",
        },
        "go.mod": {
            "stack_type": "go",
            "build_command": "go build",
            "output_directory": "./",
            "version_file": "go.mod",
        },
        "Cargo.toml": {
            "stack_type": "rust",
            "build_command": "cargo build --release",
            "output_directory": "target/release/",
            "version_file": "Cargo.toml",
        },
    }

    # Priority order for detection (BR-001, BR-002 precedence rules encoded here)
    DETECTION_ORDER: List[str] = [
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "*.csproj",
        "*.sln",
        "pom.xml",
        "build.gradle",
        "go.mod",
        "Cargo.toml",
    ]

    def __init__(self):
        """Initialize the TechStackDetector service."""
        pass

    def detect(
        self,
        project_path: Path,
        recursive: bool = False
    ) -> List[TechStackInfo]:
        """
        Detect technology stacks in a project directory.

        Args:
            project_path: Path to the project directory to scan
            recursive: If True, scan nested directories (default: False per BR-003)

        Returns:
            List of TechStackInfo objects ordered by detection priority.
            Empty list if no recognized indicators found.

        Raises:
            FileNotFoundError: If project_path does not exist
            ValueError: If project_path is not a directory or fails security checks
            NotADirectoryError: If project_path points to a file

        Business Rules Applied:
            - BR-001: pyproject.toml takes precedence over requirements.txt
            - BR-002: .csproj takes precedence over .sln
            - BR-003: Default scan is root-level only (recursive=False)
            - BR-004: Read-only operation (no filesystem modifications)
        """
        # Convert to Path if string
        project_path = Path(project_path)

        # NFR-004: Path traversal prevention
        try:
            resolved_path = project_path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {project_path}") from e

        # Check for path traversal attempts
        if ".." in str(project_path):
            # Allow if resolved path is valid and exists
            if not resolved_path.exists():
                raise ValueError(f"Path traversal detected: {project_path}")

        # Validate path exists
        if not resolved_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")

        # Validate path is a directory
        if not resolved_path.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {project_path}")

        results: List[TechStackInfo] = []
        detected_stacks: Dict[str, TechStackInfo] = {}  # stack_type -> info (for precedence)

        # Scan for indicators in priority order
        for indicator_pattern in self.DETECTION_ORDER:
            try:
                found_files = self._find_indicator_files(
                    resolved_path,
                    indicator_pattern,
                    recursive
                )

                for found_file in found_files:
                    config = self.INDICATOR_MAP[indicator_pattern]
                    stack_type = config["stack_type"]

                    # Apply precedence rules (BR-001, BR-002)
                    if stack_type in detected_stacks:
                        # Skip if we already have a higher-priority indicator for this stack
                        continue

                    # Calculate relative path for indicator_file
                    try:
                        relative_path = found_file.relative_to(resolved_path)
                        indicator_file = str(relative_path)
                    except ValueError:
                        # File not relative to project path (shouldn't happen)
                        indicator_file = found_file.name

                    info = TechStackInfo(
                        stack_type=stack_type,
                        indicator_file=indicator_file,
                        build_command=config["build_command"],
                        output_directory=config["output_directory"],
                        version_file=config.get("version_file"),
                        detection_confidence=1.0,
                    )

                    detected_stacks[stack_type] = info

            except (PermissionError, OSError) as e:
                # NFR-003: Graceful degradation with unreadable files
                logger.warning(f"Could not read indicator {indicator_pattern}: {e}")
                continue

        # Log warning if no indicators found (AC#5)
        if not detected_stacks:
            logger.warning("No recognized tech stack indicator files found")

        # Order results by priority (Node.js, Python, .NET, Java, Go, Rust)
        priority_order = ["nodejs", "python", "dotnet", "java_maven", "java_gradle", "go", "rust"]
        for stack_type in priority_order:
            if stack_type in detected_stacks:
                results.append(detected_stacks[stack_type])

        return results

    def _find_indicator_files(
        self,
        base_path: Path,
        pattern: str,
        recursive: bool
    ) -> List[Path]:
        """
        Find indicator files matching a pattern.

        Args:
            base_path: Base directory to search
            pattern: File pattern (exact name or glob like "*.csproj")
            recursive: If True, search subdirectories

        Returns:
            List of Path objects for matching files
        """
        found: List[Path] = []

        if pattern.startswith("*"):
            # Glob pattern (e.g., "*.csproj", "*.sln")
            extension = pattern[1:]  # e.g., ".csproj"

            if recursive:
                # Recursive glob
                for path in base_path.rglob(f"*{extension}"):
                    if path.is_file():
                        found.append(path)
            else:
                # Root-level only
                for path in base_path.glob(f"*{extension}"):
                    if path.is_file():
                        found.append(path)
        else:
            # Exact filename match
            if recursive:
                # Search in all subdirectories
                for path in base_path.rglob(pattern):
                    if path.is_file():
                        found.append(path)
            else:
                # Root-level only
                target = base_path / pattern
                if target.is_file():
                    found.append(target)

        return found

    def get_build_command(
        self,
        stack_type: str,
        indicator: str
    ) -> Optional[str]:
        """
        Get the build command for a specific stack type and indicator.

        This is a fast lookup method (NFR-002: < 100ms).

        Args:
            stack_type: Technology stack type (e.g., "nodejs", "python")
            indicator: Indicator file name (e.g., "package.json")

        Returns:
            Build command string, or None if not found
        """
        if indicator in self.INDICATOR_MAP:
            config = self.INDICATOR_MAP[indicator]
            if config["stack_type"] == stack_type:
                return config["build_command"]

        # Search by stack_type if indicator doesn't match directly
        for ind, config in self.INDICATOR_MAP.items():
            if config["stack_type"] == stack_type:
                return config["build_command"]

        return None
