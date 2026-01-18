"""
STORY-241: Language-Specific Package Creation Module

This module provides package creation capabilities for multiple technology stacks
as part of the DevForgeAI release skill (Phase 0.3).

Supports: npm, pip, nuget, docker, jar, zip
"""

import hashlib
import json
import logging
import re
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION CONSTANTS
# ==============================================================================

PACKAGE_COMMANDS: Dict[str, str] = {
    "npm": "npm pack",
    "pip": "python -m build",
    "nuget": "dotnet pack -c Release",
    "docker": "docker build -t {name}:{version} .",
    "jar": "mvn package",
    "zip": "zip -r {name}-{version}.zip .",
}

PACKAGE_EXTENSIONS: Dict[str, List[str]] = {
    "npm": [".tgz"],
    "pip": [".whl", ".tar.gz"],
    "nuget": [".nupkg"],
    "docker": [],  # Docker images don't have file extensions
    "jar": [".jar"],
    "zip": [".zip"],
}

DOCKER_ENABLED: bool = True

# Timeouts in milliseconds
DEFAULT_TIMEOUT_MS: int = 60000  # 60 seconds
DOCKER_TIMEOUT_MS: int = 600000  # 10 minutes


# ==============================================================================
# DATA MODEL
# ==============================================================================

@dataclass
class PackageResult:
    """
    Result from package creation operation.

    Attributes:
        success: True if package created successfully
        format: Package format (npm, pip, nuget, docker, jar, zip)
        package_path: Path to created package file (None for Docker images)
        package_name: Full package name including version
        version: Package version (semver format)
        size_bytes: Package file size in bytes (None for Docker)
        checksum: SHA256 hash of package file (None for Docker)
        docker_image: Docker image name:tag (only for Docker packages)
        command_executed: The exact command that was executed
        duration_ms: Package creation time in milliseconds
    """
    success: bool
    format: str
    package_path: Optional[str]
    package_name: str
    version: str
    size_bytes: Optional[int]
    checksum: Optional[str]
    docker_image: Optional[str]
    command_executed: str
    duration_ms: int


# ==============================================================================
# PACKAGE CREATOR SERVICE
# ==============================================================================

class PackageCreator:
    """
    Creates distribution packages for various technology stacks.

    Supports npm, Python (pip), NuGet, Docker, Java (JAR), and ZIP archives.
    Package creation failures return PackageResult with success=False rather
    than raising exceptions (BR-001).
    """

    def __init__(self, project_dir: Path, docker_enabled: bool = True):
        """
        Initialize PackageCreator.

        Args:
            project_dir: Path to the project directory
            docker_enabled: Whether Docker package creation is enabled
        """
        self.project_dir = Path(project_dir)
        self.docker_enabled = docker_enabled
        self.timeout = DEFAULT_TIMEOUT_MS
        self._timeout = DEFAULT_TIMEOUT_MS

    def _sanitize_for_shell(self, value: str) -> str:
        """
        Sanitize a value for safe use in shell commands.

        NFR-004: Prevent command injection by removing shell metacharacters.
        Only allows alphanumeric, dots, underscores, and hyphens.

        Args:
            value: String to sanitize (package name or version)

        Returns:
            Sanitized string safe for shell use
        """
        return re.sub(r'[^a-zA-Z0-9._-]', '', value)

    def _create_failure_result(
        self,
        format: str,
        name: str,
        version: str,
        command: str,
        duration_ms: int
    ) -> PackageResult:
        """Create a standardized failure result (DRY helper)."""
        package_name = f"{name}:{version}" if format == "docker" else f"{name}-{version}"
        return PackageResult(
            success=False,
            format=format,
            package_path=None,
            package_name=package_name,
            version=version,
            size_bytes=None,
            checksum=None,
            docker_image=None,
            command_executed=command,
            duration_ms=duration_ms
        )

    def _setup_docker_dockerfile(self, name: str, version: str, command: str) -> Optional[PackageResult]:
        """
        Ensure Dockerfile exists, auto-generate for Node.js if missing.

        Returns:
            None if setup successful, PackageResult with failure if cannot proceed.
        """
        dockerfile_path = self.project_dir / "Dockerfile"
        if dockerfile_path.exists():
            return None

        package_json = self.project_dir / "package.json"
        if package_json.exists():
            dockerfile_path.write_text(
                f"FROM node:18-alpine\n"
                f"WORKDIR /app\n"
                f"COPY . .\n"
                f"RUN npm install\n"
                f'CMD ["npm", "start"]\n'
            )
            return None

        return self._create_failure_result("docker", name, version, command, 0)

    def create(self, format: str) -> PackageResult:
        """
        Create a package in the specified format.

        Args:
            format: Package format (npm, pip, nuget, docker, jar, zip)

        Returns:
            PackageResult with creation status and metadata

        Raises:
            KeyError/ValueError: If format is not in PACKAGE_COMMANDS (NFR-004)
        """
        # NFR-004: Command injection prevention - only allow known formats
        if format not in PACKAGE_COMMANDS:
            raise ValueError(f"Unknown package format: {format}")

        # Check if Docker is disabled
        if format == "docker" and not self.docker_enabled:
            return self._create_failure_result(format, "", "0.0.0", "", 0)

        # Extract version from metadata
        version = self._extract_version()
        name = self._extract_name()

        # NFR-004: Sanitize inputs to prevent command injection
        safe_name = self._sanitize_for_shell(name)
        safe_version = self._sanitize_for_shell(version)

        # Get the command template
        command_template = PACKAGE_COMMANDS[format]
        command = command_template.format(name=safe_name, version=safe_version)

        # Handle Docker - check for Dockerfile, generate if needed (BR-003)
        if format == "docker":
            docker_failure = self._setup_docker_dockerfile(name, version, command)
            if docker_failure:
                return docker_failure

        # Execute the command
        start_time = time.time()
        try:
            timeout_seconds = self._get_timeout_for_format(format) / 1000
            # NFR-004: Use shell=False with shlex.split() to prevent command injection
            result = subprocess.run(
                shlex.split(command),
                shell=False,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            duration_ms = int((time.time() - start_time) * 1000)

            if result.returncode != 0:
                # SVC-009: Handle failures gracefully
                return self._create_failure_result(format, name, version, command, duration_ms)

            # Find the created package
            package_path = self._find_package(format, name, version, result.stdout)

            # Build result based on format
            if format == "docker":
                docker_image = f"{name}:{version}"
                return PackageResult(
                    success=True,
                    format=format,
                    package_path=None,
                    package_name=docker_image,
                    version=version,
                    size_bytes=None,
                    checksum=None,
                    docker_image=docker_image,
                    command_executed=command,
                    duration_ms=duration_ms
                )
            else:
                # Validate and get metadata for file-based packages
                size_bytes = None
                checksum = None

                if package_path and Path(package_path).exists():
                    pkg_file = Path(package_path)
                    size_bytes = pkg_file.stat().st_size
                    checksum = self._calculate_checksum(pkg_file)

                package_name = f"{name}-{version}"

                return PackageResult(
                    success=True,
                    format=format,
                    package_path=package_path,
                    package_name=package_name,
                    version=version,
                    size_bytes=size_bytes,
                    checksum=checksum,
                    docker_image=None,
                    command_executed=command,
                    duration_ms=duration_ms
                )

        except FileNotFoundError:
            # Tool not installed
            duration_ms = int((time.time() - start_time) * 1000)
            return self._create_failure_result(format, name, version, command, duration_ms)
        except subprocess.TimeoutExpired:
            duration_ms = int((time.time() - start_time) * 1000)
            return self._create_failure_result(format, name, version, command, duration_ms)
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.warning(f"Package creation failed for {format}: {e}")
            return self._create_failure_result(format, name, version, command, duration_ms)

    def create_multiple(self, formats: List[str]) -> List[PackageResult]:
        """
        Create packages for multiple formats.

        BR-001: Failures in one format do not stop other formats.

        Args:
            formats: List of package formats to create

        Returns:
            List of PackageResult for each format
        """
        results = []
        for fmt in formats:
            result = self.create(fmt)
            results.append(result)
        return results

    def _extract_version(self) -> str:
        """
        Extract version from package metadata files.

        Checks: package.json, pyproject.toml, .csproj, pom.xml
        BR-002: Falls back to '0.0.0' if version not found.

        Returns:
            Version string in semver format
        """
        # Try package.json (npm)
        package_json = self.project_dir / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                version = data.get("version", "0.0.0")
                if self._is_valid_semver(version):
                    return version
                return "0.0.0"
            except (json.JSONDecodeError, KeyError):
                pass

        # Try pyproject.toml (Python)
        pyproject = self.project_dir / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                # Simple TOML parsing for version
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    version = match.group(1)
                    if self._is_valid_semver(version):
                        return version
            except Exception:
                pass

        # Try .csproj (NuGet)
        for csproj in self.project_dir.glob("*.csproj"):
            try:
                tree = ET.parse(csproj)
                root = tree.getroot()
                # Handle namespaced and non-namespaced XML
                for elem in root.iter():
                    if elem.tag.endswith("Version") or elem.tag == "Version":
                        if elem.text:
                            return elem.text
            except Exception:
                pass

        # Try pom.xml (Maven)
        pom_xml = self.project_dir / "pom.xml"
        if pom_xml.exists():
            try:
                tree = ET.parse(pom_xml)
                root = tree.getroot()
                # Handle Maven namespace
                ns = {"m": "http://maven.apache.org/POM/4.0.0"}
                version_elem = root.find("m:version", ns)
                if version_elem is not None and version_elem.text:
                    return version_elem.text
                # Try without namespace
                version_elem = root.find("version")
                if version_elem is not None and version_elem.text:
                    return version_elem.text
            except Exception:
                pass

        # BR-002: Fallback
        return "0.0.0"

    def _extract_name(self) -> str:
        """Extract package name from metadata files."""
        # Try package.json
        package_json = self.project_dir / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                return data.get("name", "package")
            except (json.JSONDecodeError, KeyError):
                pass

        # Try pyproject.toml
        pyproject = self.project_dir / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
            except Exception:
                pass

        # Try .csproj
        for csproj in self.project_dir.glob("*.csproj"):
            try:
                tree = ET.parse(csproj)
                root = tree.getroot()
                for elem in root.iter():
                    if elem.tag.endswith("PackageId") or elem.tag == "PackageId":
                        if elem.text:
                            return elem.text
                # Fall back to filename
                return csproj.stem
            except Exception:
                pass

        # Try pom.xml
        pom_xml = self.project_dir / "pom.xml"
        if pom_xml.exists():
            try:
                tree = ET.parse(pom_xml)
                root = tree.getroot()
                ns = {"m": "http://maven.apache.org/POM/4.0.0"}
                artifact_id = root.find("m:artifactId", ns)
                if artifact_id is not None and artifact_id.text:
                    return artifact_id.text
                artifact_id = root.find("artifactId")
                if artifact_id is not None and artifact_id.text:
                    return artifact_id.text
            except Exception:
                pass

        return "package"

    def _is_valid_semver(self, version: str) -> bool:
        """Check if version string is valid semver."""
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        return bool(re.match(pattern, version))

    def _find_package(self, format: str, name: str, version: str, stdout: str) -> Optional[str]:
        """Find the created package file."""
        extensions = PACKAGE_EXTENSIONS.get(format, [])

        # Check stdout for filename (npm pack outputs filename)
        if stdout.strip():
            potential_file = self.project_dir / stdout.strip().split("\n")[-1]
            if potential_file.exists():
                return str(potential_file)

        # Search for files with expected extensions
        for ext in extensions:
            # Check project directory
            for f in self.project_dir.glob(f"*{ext}"):
                if name in f.name or version in f.name:
                    return str(f)

            # Check dist directory (Python)
            dist_dir = self.project_dir / "dist"
            if dist_dir.exists():
                for f in dist_dir.glob(f"*{ext}"):
                    return str(f)

            # Check bin/Release directory (.NET)
            release_dir = self.project_dir / "bin" / "Release"
            if release_dir.exists():
                for f in release_dir.rglob(f"*{ext}"):
                    return str(f)

            # Check target directory (Maven)
            target_dir = self.project_dir / "target"
            if target_dir.exists():
                for f in target_dir.glob(f"*{ext}"):
                    return str(f)

        return None

    def _validate_package(self, package_path: Path) -> PackageResult:
        """
        Validate a package file and return metadata.

        BR-004: Validation is advisory, not blocking.

        Args:
            package_path: Path to the package file

        Returns:
            PackageResult with validation metadata
        """
        package_path = Path(package_path)

        size_bytes = 0
        checksum = None

        if package_path.exists():
            size_bytes = package_path.stat().st_size

            # Warn if zero size (BR-004: advisory)
            if size_bytes == 0:
                logger.warning(f"Package file has zero size: {package_path}")

            checksum = self._calculate_checksum(package_path)

        # Determine format from extension
        format_type = "unknown"
        for fmt, exts in PACKAGE_EXTENSIONS.items():
            for ext in exts:
                if package_path.name.endswith(ext):
                    format_type = fmt
                    break

        # Extract name and version from filename
        name_version = package_path.stem
        version = self._extract_version()

        return PackageResult(
            success=True,
            format=format_type,
            package_path=str(package_path),
            package_name=name_version,
            version=version,
            size_bytes=size_bytes,
            checksum=checksum,
            docker_image=None,
            command_executed="",
            duration_ms=0
        )

    def _calculate_checksum(self, package_path: Path) -> str:
        """
        Calculate SHA256 checksum of a file.

        SVC-011: NFR-003 requires 100% accuracy.

        Args:
            package_path: Path to the file

        Returns:
            SHA256 hex digest (64 characters)
        """
        package_path = Path(package_path)
        sha256 = hashlib.sha256()

        with open(package_path, "rb") as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _get_timeout_for_format(self, format: str) -> int:
        """
        Get timeout in milliseconds for a package format.

        NFR-001: 60s default
        NFR-002: 10 minutes for Docker

        Args:
            format: Package format

        Returns:
            Timeout in milliseconds
        """
        if format == "docker":
            return DOCKER_TIMEOUT_MS
        return DEFAULT_TIMEOUT_MS
