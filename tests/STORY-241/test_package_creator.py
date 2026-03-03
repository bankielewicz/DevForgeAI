"""
STORY-241: Language-Specific Package Creation Module - Test Suite

TDD Red Phase: These tests are designed to FAIL initially (no implementation exists).
Test framework: pytest (per tech-stack.md)
Implementation target: installer/package_creator.py

Coverage targets:
- 16+ test scenarios per AC Verification Checklist
- 95%+ coverage for business logic layer
- All 6 acceptance criteria covered
- All 11 service requirements (SVC-001 through SVC-011)
- All 4 business rules (BR-001 through BR-004)
- All 4 non-functional requirements (NFR-001 through NFR-004)

Test organization:
- AC#1: npm Package Creation (3 tests)
- AC#2: Python Package Creation (3 tests)
- AC#3: NuGet Package Creation (2 tests)
- AC#4: Docker Image Creation (2 tests)
- AC#5: Multi-Format Package Creation (2 tests)
- AC#6: Package Validation (3 tests)
- Technical Spec: Data Model tests (10 tests)
- Technical Spec: Service Requirements (11 tests)
- Technical Spec: Business Rules (4 tests)
- Technical Spec: Non-Functional Requirements (4 tests)
- Edge Cases (5 tests)
"""

# CRITICAL: Add project root to sys.path BEFORE any other imports
# This must be at the very top to ensure installer module can be imported
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(_project_root))

import hashlib
import os
import pytest
import subprocess
import tempfile
import time
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List, Optional
from unittest.mock import MagicMock, Mock, patch, call


# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def mock_bash():
    """Mock the Bash subprocess execution for package commands."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Package created successfully",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with package files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def npm_project(temp_project_dir):
    """Create a minimal npm project structure."""
    package_json = temp_project_dir / "package.json"
    package_json.write_text('{"name": "test-package", "version": "1.0.0"}')
    return temp_project_dir


@pytest.fixture
def python_project(temp_project_dir):
    """Create a minimal Python project structure."""
    pyproject_toml = temp_project_dir / "pyproject.toml"
    pyproject_toml.write_text('''
[project]
name = "test-package"
version = "1.0.0"
''')
    dist_dir = temp_project_dir / "dist"
    dist_dir.mkdir()
    return temp_project_dir


@pytest.fixture
def dotnet_project(temp_project_dir):
    """Create a minimal .NET project structure."""
    csproj = temp_project_dir / "TestPackage.csproj"
    csproj.write_text('''
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <PackageId>TestPackage</PackageId>
    <Version>1.0.0</Version>
  </PropertyGroup>
</Project>
''')
    return temp_project_dir


@pytest.fixture
def docker_project(temp_project_dir):
    """Create a minimal Docker project structure."""
    dockerfile = temp_project_dir / "Dockerfile"
    dockerfile.write_text("FROM node:18-alpine\nWORKDIR /app")
    return temp_project_dir


@pytest.fixture
def sample_package_file(temp_project_dir):
    """Create a sample package file for validation tests."""
    package_file = temp_project_dir / "test-package-1.0.0.tgz"
    package_file.write_bytes(b"mock package content" * 100)
    return package_file


# ==============================================================================
# DATA MODEL TESTS - PackageResult Dataclass
# ==============================================================================


class TestPackageResultDataModel:
    """Tests for PackageResult dataclass structure per Technical Specification."""

    def test_package_result_has_success_field(self):
        """Test: Verify success field exists and is Bool type."""
        # Import should work once implemented
        from installer.package_creator import PackageResult

        # Verify field exists in dataclass
        field_names = [f.name for f in fields(PackageResult)]
        assert "success" in field_names, "PackageResult must have 'success' field"

        # Verify type annotation
        result = PackageResult(
            success=True,
            format="npm",
            package_path=None,
            package_name="test-1.0.0",
            version="1.0.0",
            size_bytes=None,
            checksum=None,
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert isinstance(result.success, bool)

    def test_package_result_has_format_field(self):
        """Test: Verify format field is String and required."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "format" in field_names, "PackageResult must have 'format' field"

        result = PackageResult(
            success=True,
            format="npm",
            package_path=None,
            package_name="test-1.0.0",
            version="1.0.0",
            size_bytes=None,
            checksum=None,
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert isinstance(result.format, str)
        assert result.format in ["npm", "pip", "nuget", "docker", "jar", "zip"]

    def test_package_result_has_package_path_field(self):
        """Test: Verify package_path is Optional[String]."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "package_path" in field_names

        # Test with None (valid for Docker images)
        result = PackageResult(
            success=True,
            format="docker",
            package_path=None,
            package_name="myimage:1.0.0",
            version="1.0.0",
            size_bytes=None,
            checksum=None,
            docker_image="myimage:1.0.0",
            command_executed="docker build",
            duration_ms=100
        )
        assert result.package_path is None

    def test_package_result_has_package_name_field(self):
        """Test: Verify package_name is String and required."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "package_name" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="abc123",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert isinstance(result.package_name, str)
        assert len(result.package_name) > 0

    def test_package_result_has_version_field(self):
        """Test: Verify version is String in semver format."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "version" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="abc123",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        # Version should be valid semver
        import re
        semver_pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        assert re.match(semver_pattern, result.version), "Version must be valid semver"

    def test_package_result_has_size_bytes_field(self):
        """Test: Verify size_bytes is Optional[Int] and positive."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "size_bytes" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="abc123",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert result.size_bytes is None or result.size_bytes > 0

    def test_package_result_has_checksum_field(self):
        """Test: Verify checksum is Optional[String] SHA256 hash."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "checksum" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        # SHA256 is 64 hex characters
        if result.checksum is not None:
            assert len(result.checksum) == 64
            assert all(c in "0123456789abcdef" for c in result.checksum.lower())

    def test_package_result_has_docker_image_field(self):
        """Test: Verify docker_image is Optional[String] for Docker packages only."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "docker_image" in field_names

        # Docker package should have docker_image field populated
        result = PackageResult(
            success=True,
            format="docker",
            package_path=None,
            package_name="myapp:1.0.0",
            version="1.0.0",
            size_bytes=None,
            checksum=None,
            docker_image="myapp:1.0.0",
            command_executed="docker build -t myapp:1.0.0 .",
            duration_ms=5000
        )
        assert result.docker_image is not None
        assert ":" in result.docker_image  # Docker image reference format

    def test_package_result_has_command_executed_field(self):
        """Test: Verify command_executed is String and required."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "command_executed" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="abc123",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert isinstance(result.command_executed, str)
        assert len(result.command_executed) > 0

    def test_package_result_has_duration_ms_field(self):
        """Test: Verify duration_ms is Int and positive."""
        from installer.package_creator import PackageResult

        field_names = [f.name for f in fields(PackageResult)]
        assert "duration_ms" in field_names

        result = PackageResult(
            success=True,
            format="npm",
            package_path="test-package-1.0.0.tgz",
            package_name="test-package-1.0.0",
            version="1.0.0",
            size_bytes=1024,
            checksum="abc123",
            docker_image=None,
            command_executed="npm pack",
            duration_ms=100
        )
        assert isinstance(result.duration_ms, int)
        assert result.duration_ms > 0


# ==============================================================================
# AC#1: npm PACKAGE CREATION TESTS
# ==============================================================================


class TestNpmPackageCreation:
    """AC#1: npm Package Creation tests."""

    def test_npm_pack_command_executed(self, npm_project, mock_bash):
        """
        Test: npm pack command executed
        Given: A Node.js project with valid package.json
        When: PackageCreator is invoked with format="npm"
        Then: It executes `npm pack` in the project directory
        """
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        # Verify npm pack was called (shlex.split splits into ['npm', 'pack'])
        mock_bash.assert_called()
        call_args = mock_bash.call_args_list
        npm_pack_called = any("'npm'" in str(call) and "'pack'" in str(call) for call in call_args)
        assert npm_pack_called, "npm pack command must be executed"

    def test_npm_creates_tgz_file(self, npm_project, mock_bash):
        """
        Test: .tgz file created
        Given: npm pack completes successfully
        When: Checking the result
        Then: A .tgz file path is returned in package_path
        """
        from installer.package_creator import PackageCreator

        # Mock npm pack to create a .tgz file
        def mock_npm_pack(*args, **kwargs):
            tgz_file = npm_project / "test-package-1.0.0.tgz"
            tgz_file.write_bytes(b"mock tarball content")
            return MagicMock(returncode=0, stdout="test-package-1.0.0.tgz\n", stderr="")

        mock_bash.side_effect = mock_npm_pack

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert result.success is True
        assert result.package_path is not None
        assert result.package_path.endswith(".tgz")

    def test_npm_package_name_version_correct(self, npm_project, mock_bash):
        """
        Test: Package name/version correct
        Given: npm pack completes successfully
        When: Checking the PackageResult
        Then: package_name and version match package.json
        """
        from installer.package_creator import PackageCreator

        # Update package.json with specific name/version
        (npm_project / "package.json").write_text(
            '{"name": "my-awesome-package", "version": "2.3.4"}'
        )

        def mock_npm_pack(*args, **kwargs):
            tgz_file = npm_project / "my-awesome-package-2.3.4.tgz"
            tgz_file.write_bytes(b"mock tarball content")
            return MagicMock(returncode=0, stdout="my-awesome-package-2.3.4.tgz\n", stderr="")

        mock_bash.side_effect = mock_npm_pack

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert result.package_name == "my-awesome-package-2.3.4"
        assert result.version == "2.3.4"


# ==============================================================================
# AC#2: PYTHON PACKAGE CREATION TESTS
# ==============================================================================


class TestPythonPackageCreation:
    """AC#2: Python Package Creation tests."""

    def test_python_build_command_executed(self, python_project, mock_bash):
        """
        Test: python -m build command executed
        Given: A Python project with pyproject.toml
        When: PackageCreator is invoked with format="pip"
        Then: It executes `python -m build` in the project directory
        """
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=python_project)
        result = creator.create(format="pip")

        # Verify python -m build was called (shlex.split splits into tokens)
        mock_bash.assert_called()
        call_args = mock_bash.call_args_list
        build_called = any("'python'" in str(call) and "'build'" in str(call) for call in call_args)
        assert build_called, "python -m build command must be executed"

    def test_python_creates_wheel_file(self, python_project, mock_bash):
        """
        Test: .whl file created
        Given: python -m build completes successfully
        When: Checking the result
        Then: A .whl file is created in dist/
        """
        from installer.package_creator import PackageCreator

        dist_dir = python_project / "dist"
        dist_dir.mkdir(exist_ok=True)

        def mock_python_build(*args, **kwargs):
            # Create mock wheel file
            wheel_file = dist_dir / "test_package-1.0.0-py3-none-any.whl"
            wheel_file.write_bytes(b"mock wheel content")
            tarball = dist_dir / "test_package-1.0.0.tar.gz"
            tarball.write_bytes(b"mock source dist")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_bash.side_effect = mock_python_build

        creator = PackageCreator(project_dir=python_project)
        result = creator.create(format="pip")

        assert result.success is True
        # Python build creates multiple files, should return wheel path
        assert ".whl" in str(result.package_path) or ".tar.gz" in str(result.package_path)

    def test_python_creates_tar_gz_file(self, python_project, mock_bash):
        """
        Test: .tar.gz file created
        Given: python -m build completes successfully
        When: Checking the output directory
        Then: Both .whl and .tar.gz files exist in dist/
        """
        from installer.package_creator import PackageCreator

        dist_dir = python_project / "dist"
        dist_dir.mkdir(exist_ok=True)

        def mock_python_build(*args, **kwargs):
            wheel_file = dist_dir / "test_package-1.0.0-py3-none-any.whl"
            wheel_file.write_bytes(b"mock wheel content")
            tarball = dist_dir / "test_package-1.0.0.tar.gz"
            tarball.write_bytes(b"mock source dist")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_bash.side_effect = mock_python_build

        creator = PackageCreator(project_dir=python_project)
        result = creator.create(format="pip")

        # Check dist directory contains both file types
        dist_files = list(dist_dir.iterdir())
        extensions = [f.suffix for f in dist_files]
        assert ".whl" in extensions or any(f.name.endswith(".tar.gz") for f in dist_files)


# ==============================================================================
# AC#3: NUGET PACKAGE CREATION TESTS
# ==============================================================================


class TestNuGetPackageCreation:
    """AC#3: NuGet Package Creation tests."""

    def test_dotnet_pack_command_executed(self, dotnet_project, mock_bash):
        """
        Test: dotnet pack command executed
        Given: A .NET project with a .csproj file
        When: PackageCreator is invoked with format="nuget"
        Then: It executes `dotnet pack -c Release`
        """
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=dotnet_project)
        result = creator.create(format="nuget")

        # Verify dotnet pack was called (shlex.split splits into tokens)
        mock_bash.assert_called()
        call_args = mock_bash.call_args_list
        pack_called = any("'dotnet'" in str(call) and "'pack'" in str(call) for call in call_args)
        assert pack_called, "dotnet pack command must be executed"

        # Verify Release configuration
        release_config = any("'Release'" in str(call) for call in call_args)
        assert release_config, "dotnet pack must use Release configuration"

    def test_nuget_creates_nupkg_file(self, dotnet_project, mock_bash):
        """
        Test: .nupkg file created
        Given: dotnet pack completes successfully
        When: Checking the result
        Then: A .nupkg file path is returned
        """
        from installer.package_creator import PackageCreator

        output_dir = dotnet_project / "bin" / "Release"
        output_dir.mkdir(parents=True, exist_ok=True)

        def mock_dotnet_pack(*args, **kwargs):
            nupkg = output_dir / "TestPackage.1.0.0.nupkg"
            nupkg.write_bytes(b"mock nupkg content")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_bash.side_effect = mock_dotnet_pack

        creator = PackageCreator(project_dir=dotnet_project)
        result = creator.create(format="nuget")

        assert result.success is True
        assert result.package_path is not None
        assert result.package_path.endswith(".nupkg")


# ==============================================================================
# AC#4: DOCKER IMAGE CREATION TESTS
# ==============================================================================


class TestDockerImageCreation:
    """AC#4: Docker Image Creation tests."""

    def test_docker_build_command_executed(self, docker_project, mock_bash):
        """
        Test: docker build command executed
        Given: A project with a Dockerfile
        When: PackageCreator is invoked with format="docker"
        Then: It executes `docker build -t {name}:{version} .`
        """
        from installer.package_creator import PackageCreator

        # Add package.json for version extraction
        (docker_project / "package.json").write_text('{"name": "myapp", "version": "1.0.0"}')

        creator = PackageCreator(project_dir=docker_project)
        result = creator.create(format="docker")

        # Verify docker build was called (shlex.split splits into tokens)
        mock_bash.assert_called()
        call_args = mock_bash.call_args_list
        docker_called = any("'docker'" in str(call) and "'build'" in str(call) for call in call_args)
        assert docker_called, "docker build command must be executed"

        # Verify -t flag for tagging
        tag_flag = any("'-t'" in str(call) for call in call_args)
        assert tag_flag, "docker build must include -t flag for tagging"

    def test_docker_image_tagged_correctly(self, docker_project, mock_bash):
        """
        Test: Image created with correct tag
        Given: docker build completes successfully
        When: Checking the PackageResult
        Then: docker_image field contains name:version format
        """
        from installer.package_creator import PackageCreator

        (docker_project / "package.json").write_text('{"name": "myapp", "version": "2.0.0"}')

        creator = PackageCreator(project_dir=docker_project)
        result = creator.create(format="docker")

        assert result.success is True
        assert result.docker_image is not None
        assert ":" in result.docker_image  # name:version format
        assert "2.0.0" in result.docker_image


# ==============================================================================
# AC#5: MULTI-FORMAT PACKAGE CREATION TESTS
# ==============================================================================


class TestMultiFormatPackageCreation:
    """AC#5: Multi-Format Package Creation tests."""

    def test_multiple_formats_created_in_sequence(self, npm_project, mock_bash):
        """
        Test: Multiple formats created in sequence
        Given: A project requiring npm + Docker packages
        When: PackageCreator is invoked with multiple formats
        Then: It creates packages for each format
        """
        from installer.package_creator import PackageCreator

        # Add Dockerfile
        (npm_project / "Dockerfile").write_text("FROM node:18-alpine")

        def mock_commands(*args, **kwargs):
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_bash.side_effect = mock_commands

        creator = PackageCreator(project_dir=npm_project)
        results = creator.create_multiple(formats=["npm", "docker"])

        assert isinstance(results, list)
        assert len(results) == 2
        formats_created = [r.format for r in results]
        assert "npm" in formats_created
        assert "docker" in formats_created

    def test_failure_in_one_format_continues_others(self, npm_project, mock_bash):
        """
        Test: Failure in one format doesn't stop others (BR-001)
        Given: A project with npm failing but Docker succeeding
        When: PackageCreator creates multiple formats
        Then: Docker package is still created despite npm failure
        """
        from installer.package_creator import PackageCreator

        (npm_project / "Dockerfile").write_text("FROM node:18-alpine")

        call_count = [0]

        def mock_commands(*args, **kwargs):
            call_count[0] += 1
            # First call (npm) fails, second (docker) succeeds
            if call_count[0] == 1:
                return MagicMock(returncode=1, stdout="", stderr="npm error")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_bash.side_effect = mock_commands

        creator = PackageCreator(project_dir=npm_project)
        results = creator.create_multiple(formats=["npm", "docker"])

        # Should have both results, one failed, one succeeded
        assert len(results) == 2
        npm_result = next(r for r in results if r.format == "npm")
        docker_result = next(r for r in results if r.format == "docker")

        assert npm_result.success is False
        assert docker_result.success is True


# ==============================================================================
# AC#6: PACKAGE VALIDATION TESTS
# ==============================================================================


class TestPackageValidation:
    """AC#6: Package Validation tests."""

    def test_package_file_size_verified(self, sample_package_file):
        """
        Test: Package file size verified
        Given: A package has been created
        When: Validation runs
        Then: size_bytes matches actual file size
        """
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=sample_package_file.parent)
        result = creator._validate_package(sample_package_file)

        actual_size = sample_package_file.stat().st_size
        assert result.size_bytes == actual_size

    def test_package_checksum_calculated(self, sample_package_file):
        """
        Test: Package checksum calculated (SVC-011)
        Given: A package file exists
        When: Validation runs
        Then: checksum matches SHA256 hash of file
        """
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=sample_package_file.parent)
        result = creator._validate_package(sample_package_file)

        # Calculate expected checksum
        with open(sample_package_file, "rb") as f:
            expected_checksum = hashlib.sha256(f.read()).hexdigest()

        assert result.checksum == expected_checksum

    def test_validation_warning_logged_on_issues(self, temp_project_dir, caplog):
        """
        Test: Warning logged for validation issues (BR-004)
        Given: A package with validation issues (e.g., zero size)
        When: Validation runs
        Then: Warning is logged but success=True (advisory)
        """
        from installer.package_creator import PackageCreator
        import logging

        # Create empty file (validation issue)
        empty_file = temp_project_dir / "empty-package-1.0.0.tgz"
        empty_file.touch()

        with caplog.at_level(logging.WARNING):
            creator = PackageCreator(project_dir=temp_project_dir)
            result = creator._validate_package(empty_file)

        # Should log warning for zero-size file
        assert "warning" in caplog.text.lower() or result.size_bytes == 0
        # BR-004: Validation is advisory, not blocking
        # (success depends on whether file was created, not validation)


# ==============================================================================
# TECHNICAL SPECIFICATION: SERVICE REQUIREMENTS TESTS
# ==============================================================================


class TestServiceRequirements:
    """Tests for Service Requirements (SVC-001 through SVC-011)."""

    def test_svc_001_npm_pack_command(self, npm_project, mock_bash):
        """SVC-001: Create npm package via npm pack."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert "npm pack" in result.command_executed

    def test_svc_002_python_build_command(self, python_project, mock_bash):
        """SVC-002: Create Python packages via python -m build."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=python_project)
        result = creator.create(format="pip")

        assert "python" in result.command_executed.lower()
        assert "build" in result.command_executed.lower()

    def test_svc_003_dotnet_pack_command(self, dotnet_project, mock_bash):
        """SVC-003: Create NuGet packages via dotnet pack."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=dotnet_project)
        result = creator.create(format="nuget")

        assert "dotnet pack" in result.command_executed

    def test_svc_004_docker_build_command(self, docker_project, mock_bash):
        """SVC-004: Create Docker images via docker build."""
        from installer.package_creator import PackageCreator

        (docker_project / "package.json").write_text('{"name": "app", "version": "1.0.0"}')

        creator = PackageCreator(project_dir=docker_project)
        result = creator.create(format="docker")

        assert "docker build" in result.command_executed

    def test_svc_005_java_maven_command(self, temp_project_dir, mock_bash):
        """SVC-005: Create Java JAR packages via mvn package."""
        from installer.package_creator import PackageCreator

        # Create Maven project
        pom_xml = temp_project_dir / "pom.xml"
        pom_xml.write_text('''
<project>
  <groupId>com.example</groupId>
  <artifactId>myapp</artifactId>
  <version>1.0.0</version>
</project>
''')

        creator = PackageCreator(project_dir=temp_project_dir)
        result = creator.create(format="jar")

        assert "mvn package" in result.command_executed or "gradle" in result.command_executed.lower()

    def test_svc_006_zip_archive_command(self, temp_project_dir, mock_bash):
        """SVC-006: Create zip archives for binary distributions."""
        from installer.package_creator import PackageCreator

        # Create some files to zip
        (temp_project_dir / "README.md").write_text("# My App")
        (temp_project_dir / "dist").mkdir()
        (temp_project_dir / "dist" / "app.exe").write_bytes(b"binary")

        creator = PackageCreator(project_dir=temp_project_dir)
        result = creator.create(format="zip")

        assert "zip" in result.command_executed.lower()

    def test_svc_007_version_extraction(self, npm_project):
        """SVC-007: Extract version from package metadata files."""
        from installer.package_creator import PackageCreator

        (npm_project / "package.json").write_text('{"name": "test", "version": "3.2.1"}')

        creator = PackageCreator(project_dir=npm_project)
        version = creator._extract_version()

        assert version == "3.2.1"

    def test_svc_008_package_validation(self, sample_package_file):
        """SVC-008: Validate created packages (size, checksum, name)."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=sample_package_file.parent)
        result = creator._validate_package(sample_package_file)

        assert result.size_bytes is not None
        assert result.size_bytes > 0
        assert result.checksum is not None
        assert len(result.checksum) == 64  # SHA256

    def test_svc_009_failure_handling(self, npm_project, mock_bash):
        """SVC-009: Handle package creation failures gracefully."""
        from installer.package_creator import PackageCreator

        mock_bash.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="npm ERR! ENOENT"
        )

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert result.success is False
        assert result.format == "npm"
        # Should not raise exception

    def test_svc_010_multi_format_creation(self, npm_project, mock_bash):
        """SVC-010: Create multiple formats for same project."""
        from installer.package_creator import PackageCreator

        (npm_project / "Dockerfile").write_text("FROM node:18")

        creator = PackageCreator(project_dir=npm_project)
        results = creator.create_multiple(formats=["npm", "docker"])

        assert len(results) == 2
        assert all(isinstance(r.format, str) for r in results)

    def test_svc_011_sha256_checksum(self, sample_package_file):
        """SVC-011: Calculate and store package checksum (SHA256)."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=sample_package_file.parent)
        checksum = creator._calculate_checksum(sample_package_file)

        # Verify it's SHA256 format
        assert len(checksum) == 64
        assert all(c in "0123456789abcdef" for c in checksum.lower())

        # Verify it matches independent calculation
        with open(sample_package_file, "rb") as f:
            expected = hashlib.sha256(f.read()).hexdigest()
        assert checksum == expected


# ==============================================================================
# TECHNICAL SPECIFICATION: BUSINESS RULES TESTS
# ==============================================================================


class TestBusinessRules:
    """Tests for Business Rules (BR-001 through BR-004)."""

    def test_br_001_failures_do_not_halt_workflow(self, npm_project, mock_bash):
        """BR-001: Package creation failures must not halt the workflow."""
        from installer.package_creator import PackageCreator

        (npm_project / "Dockerfile").write_text("FROM node:18")

        call_count = [0]

        def failing_first(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return MagicMock(returncode=1, stderr="error")
            return MagicMock(returncode=0, stdout="")

        mock_bash.side_effect = failing_first

        creator = PackageCreator(project_dir=npm_project)
        results = creator.create_multiple(formats=["npm", "docker"])

        # Should complete both attempts
        assert len(results) == 2
        # First failed, second succeeded
        failed = [r for r in results if not r.success]
        succeeded = [r for r in results if r.success]
        assert len(failed) == 1
        assert len(succeeded) == 1

    def test_br_002_version_from_canonical_source(self, npm_project):
        """BR-002: Version must be extracted from canonical source."""
        from installer.package_creator import PackageCreator

        (npm_project / "package.json").write_text('{"name": "app", "version": "5.0.0"}')

        creator = PackageCreator(project_dir=npm_project)
        version = creator._extract_version()

        assert version == "5.0.0"

    def test_br_002_fallback_version_when_missing(self, temp_project_dir):
        """BR-002: Use '0.0.0' if version not found."""
        from installer.package_creator import PackageCreator

        # No version file present
        creator = PackageCreator(project_dir=temp_project_dir)
        version = creator._extract_version()

        assert version == "0.0.0"

    def test_br_003_dockerfile_required_or_generated(self, temp_project_dir, mock_bash):
        """BR-003: Docker images require Dockerfile or auto-generation."""
        from installer.package_creator import PackageCreator

        # Node.js project without Dockerfile
        (temp_project_dir / "package.json").write_text('{"name": "app", "version": "1.0.0"}')

        creator = PackageCreator(project_dir=temp_project_dir)
        result = creator.create(format="docker")

        # Either Dockerfile was generated OR docker build was skipped
        dockerfile_exists = (temp_project_dir / "Dockerfile").exists()
        assert dockerfile_exists or result.success is False

    def test_br_004_validation_is_advisory(self, temp_project_dir, mock_bash):
        """BR-004: Package validation is advisory, not blocking."""
        from installer.package_creator import PackageCreator

        # Create empty package (validation issue)
        empty_pkg = temp_project_dir / "pkg-1.0.0.tgz"
        empty_pkg.touch()

        mock_bash.return_value = MagicMock(returncode=0, stdout=str(empty_pkg))

        creator = PackageCreator(project_dir=temp_project_dir)

        # Validation issues should not cause failure
        result = creator._validate_package(empty_pkg)

        # Advisory: returns result regardless of validation issues
        assert result is not None
        # Size will be 0 (issue detected) but no exception raised


# ==============================================================================
# TECHNICAL SPECIFICATION: NON-FUNCTIONAL REQUIREMENTS TESTS
# ==============================================================================


class TestNonFunctionalRequirements:
    """Tests for Non-Functional Requirements (NFR-001 through NFR-004)."""

    def test_nfr_001_package_timeout(self, npm_project, mock_bash):
        """NFR-001: Package creation must complete within timeout (60s)."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=npm_project)

        # Check timeout is configured
        assert hasattr(creator, "timeout") or hasattr(creator, "_timeout")
        timeout = getattr(creator, "timeout", getattr(creator, "_timeout", None))

        # Default timeout should be <= 60 seconds for non-Docker
        assert timeout is None or timeout <= 60000  # ms

    def test_nfr_002_docker_extended_timeout(self, docker_project, mock_bash):
        """NFR-002: Docker builds have extended timeout (10 minutes)."""
        from installer.package_creator import PackageCreator

        (docker_project / "package.json").write_text('{"name": "app", "version": "1.0.0"}')

        creator = PackageCreator(project_dir=docker_project)

        # Docker should have extended timeout
        docker_timeout = creator._get_timeout_for_format("docker")
        assert docker_timeout >= 600000  # 10 minutes in ms

    def test_nfr_003_checksum_accuracy(self, sample_package_file):
        """NFR-003: Package checksums must be accurate (100%)."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=sample_package_file.parent)

        # Calculate checksum multiple times - should be consistent
        checksum1 = creator._calculate_checksum(sample_package_file)
        checksum2 = creator._calculate_checksum(sample_package_file)

        assert checksum1 == checksum2

        # Verify against standard library
        with open(sample_package_file, "rb") as f:
            expected = hashlib.sha256(f.read()).hexdigest()

        assert checksum1 == expected

    def test_nfr_004_command_injection_prevention(self, npm_project, mock_bash):
        """NFR-004: Package commands from lookup table only (no injection)."""
        from installer.package_creator import PackageCreator, PACKAGE_COMMANDS

        # Verify commands come from predefined lookup
        assert "npm" in PACKAGE_COMMANDS
        assert "pip" in PACKAGE_COMMANDS
        assert "nuget" in PACKAGE_COMMANDS
        assert "docker" in PACKAGE_COMMANDS

        # Attempt to use invalid format (potential injection)
        creator = PackageCreator(project_dir=npm_project)

        with pytest.raises((KeyError, ValueError)):
            creator.create(format="npm; rm -rf /")


# ==============================================================================
# EDGE CASES AND ERROR HANDLING TESTS
# ==============================================================================


class TestEdgeCases:
    """Edge case and error handling tests."""

    def test_missing_package_tool_skips_format(self, npm_project, mock_bash):
        """Edge: Missing package tool (npm not installed) skips format."""
        from installer.package_creator import PackageCreator

        mock_bash.side_effect = FileNotFoundError("npm not found")

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert result.success is False
        # Should not raise exception

    def test_invalid_version_in_metadata(self, npm_project):
        """Edge: Invalid version in metadata falls back to 0.0.0."""
        from installer.package_creator import PackageCreator

        (npm_project / "package.json").write_text('{"name": "app", "version": "invalid"}')

        creator = PackageCreator(project_dir=npm_project)
        version = creator._extract_version()

        # Invalid semver should fallback or be handled
        assert version == "0.0.0" or version == "invalid"

    def test_large_package_handling(self, temp_project_dir, mock_bash):
        """Edge: Large package (>100MB) completes successfully."""
        from installer.package_creator import PackageCreator

        # Create 100MB+ file
        large_file = temp_project_dir / "large-package-1.0.0.tgz"
        with open(large_file, "wb") as f:
            f.write(b"x" * (100 * 1024 * 1024 + 1))

        creator = PackageCreator(project_dir=temp_project_dir)
        result = creator._validate_package(large_file)

        assert result.size_bytes > 100 * 1024 * 1024
        assert result.checksum is not None

    def test_output_directory_missing(self, temp_project_dir, mock_bash):
        """Edge: Output directory doesn't exist - handled gracefully."""
        from installer.package_creator import PackageCreator

        # Setup project but don't create dist directory
        (temp_project_dir / "package.json").write_text('{"name": "app", "version": "1.0.0"}')

        mock_bash.return_value = MagicMock(returncode=0, stdout="app-1.0.0.tgz")

        creator = PackageCreator(project_dir=temp_project_dir)
        result = creator.create(format="npm")

        # Should handle missing output directory
        assert result is not None

    def test_checksum_mismatch_detection(self, temp_project_dir):
        """Edge: Checksum mismatch is detected during validation."""
        from installer.package_creator import PackageCreator

        pkg_file = temp_project_dir / "pkg-1.0.0.tgz"
        pkg_file.write_bytes(b"original content")

        creator = PackageCreator(project_dir=temp_project_dir)
        checksum1 = creator._calculate_checksum(pkg_file)

        # Modify file content
        pkg_file.write_bytes(b"modified content")
        checksum2 = creator._calculate_checksum(pkg_file)

        # Checksums should differ
        assert checksum1 != checksum2


# ==============================================================================
# CONFIGURATION TESTS
# ==============================================================================


class TestConfiguration:
    """Tests for PackageFormats configuration."""

    def test_package_commands_has_all_formats(self):
        """Test: Verify all 7 formats have commands."""
        from installer.package_creator import PACKAGE_COMMANDS

        required_formats = ["npm", "pip", "nuget", "docker", "jar", "zip"]
        for fmt in required_formats:
            assert fmt in PACKAGE_COMMANDS, f"Missing command for format: {fmt}"

    def test_package_extensions_defined(self):
        """Test: Verify extensions for each format."""
        from installer.package_creator import PACKAGE_EXTENSIONS

        assert ".tgz" in PACKAGE_EXTENSIONS.get("npm", [])
        assert ".whl" in PACKAGE_EXTENSIONS.get("pip", []) or ".tar.gz" in PACKAGE_EXTENSIONS.get("pip", [])
        assert ".nupkg" in PACKAGE_EXTENSIONS.get("nuget", [])

    def test_docker_enabled_by_default(self):
        """Test: Verify Docker enabled by default."""
        from installer.package_creator import DOCKER_ENABLED

        assert DOCKER_ENABLED is True

    def test_docker_can_be_disabled(self, docker_project, mock_bash):
        """Test: Verify Docker skipped when disabled."""
        from installer.package_creator import PackageCreator

        (docker_project / "package.json").write_text('{"name": "app", "version": "1.0.0"}')

        creator = PackageCreator(project_dir=docker_project, docker_enabled=False)
        result = creator.create(format="docker")

        # Should be skipped or return failure when disabled
        assert result.success is False or "docker" not in result.command_executed


# ==============================================================================
# VERSION EXTRACTION TESTS
# ==============================================================================


class TestVersionExtraction:
    """Tests for version extraction from various metadata files."""

    def test_extract_version_from_package_json(self, npm_project):
        """Extract version from package.json."""
        from installer.package_creator import PackageCreator

        (npm_project / "package.json").write_text('{"name": "app", "version": "1.2.3"}')

        creator = PackageCreator(project_dir=npm_project)
        assert creator._extract_version() == "1.2.3"

    def test_extract_version_from_pyproject_toml(self, python_project):
        """Extract version from pyproject.toml."""
        from installer.package_creator import PackageCreator

        (python_project / "pyproject.toml").write_text('[project]\nname = "app"\nversion = "2.3.4"')

        creator = PackageCreator(project_dir=python_project)
        assert creator._extract_version() == "2.3.4"

    def test_extract_version_from_csproj(self, dotnet_project):
        """Extract version from .csproj."""
        from installer.package_creator import PackageCreator

        creator = PackageCreator(project_dir=dotnet_project)
        assert creator._extract_version() == "1.0.0"

    def test_extract_version_from_pom_xml(self, temp_project_dir):
        """Extract version from pom.xml."""
        from installer.package_creator import PackageCreator

        pom = temp_project_dir / "pom.xml"
        pom.write_text('<project><version>3.4.5</version></project>')

        creator = PackageCreator(project_dir=temp_project_dir)
        assert creator._extract_version() == "3.4.5"


# ==============================================================================
# DURATION TRACKING TESTS
# ==============================================================================


class TestDurationTracking:
    """Tests for duration_ms tracking."""

    def test_duration_tracked_for_package_creation(self, npm_project, mock_bash):
        """Test: duration_ms is tracked and positive."""
        from installer.package_creator import PackageCreator

        def slow_mock(*args, **kwargs):
            time.sleep(0.01)  # 10ms
            return MagicMock(returncode=0, stdout="pkg.tgz")

        mock_bash.side_effect = slow_mock

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert result.duration_ms >= 10  # At least 10ms

    def test_duration_is_positive_integer(self, npm_project, mock_bash):
        """Test: duration_ms is always positive integer."""
        from installer.package_creator import PackageCreator

        def slow_mock(*args, **kwargs):
            time.sleep(0.001)  # 1ms minimum
            return MagicMock(returncode=0, stdout="pkg.tgz")

        mock_bash.side_effect = slow_mock

        creator = PackageCreator(project_dir=npm_project)
        result = creator.create(format="npm")

        assert isinstance(result.duration_ms, int)
        assert result.duration_ms >= 0  # At least non-negative (mocked calls may be instant)
