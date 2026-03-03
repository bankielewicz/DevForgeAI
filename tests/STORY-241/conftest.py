"""
STORY-241: Shared pytest fixtures and configuration.

This file provides common fixtures used across test modules for STORY-241.
"""

import hashlib
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_subprocess_run():
    """
    Mock subprocess.run for all package command executions.

    Yields a mock that can be configured per-test for specific behaviors.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def temp_workspace():
    """
    Create an isolated temporary workspace for package creation tests.

    Automatically cleaned up after test completion.
    """
    with tempfile.TemporaryDirectory(prefix="story241_") as tmpdir:
        workspace = Path(tmpdir)

        # Create common directories
        (workspace / "dist").mkdir()
        (workspace / "bin" / "Release").mkdir(parents=True)
        (workspace / "target").mkdir()
        (workspace / "build" / "libs").mkdir(parents=True)

        yield workspace


@pytest.fixture
def sample_npm_project(temp_workspace):
    """
    Create a sample npm project structure.

    Returns:
        Path: The project directory path
    """
    package_json = temp_workspace / "package.json"
    package_json.write_text('{"name": "sample-npm-project", "version": "1.0.0"}')

    # Create a sample source file
    (temp_workspace / "index.js").write_text("console.log('Hello');")

    return temp_workspace


@pytest.fixture
def sample_python_project(temp_workspace):
    """
    Create a sample Python project structure.

    Returns:
        Path: The project directory path
    """
    pyproject = temp_workspace / "pyproject.toml"
    pyproject.write_text('''
[project]
name = "sample-python-project"
version = "1.0.0"
description = "A sample Python project"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
''')

    # Create source structure
    src_dir = temp_workspace / "src" / "sample_python_project"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").write_text("__version__ = '1.0.0'")

    return temp_workspace


@pytest.fixture
def sample_dotnet_project(temp_workspace):
    """
    Create a sample .NET project structure.

    Returns:
        Path: The project directory path
    """
    csproj = temp_workspace / "SampleProject.csproj"
    csproj.write_text('''
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <PackageId>SampleProject</PackageId>
    <Version>1.0.0</Version>
    <Authors>DevForgeAI</Authors>
  </PropertyGroup>
</Project>
''')

    # Create sample source
    (temp_workspace / "Program.cs").write_text("Console.WriteLine(\"Hello\");")

    return temp_workspace


@pytest.fixture
def sample_docker_project(temp_workspace):
    """
    Create a sample Docker project structure.

    Returns:
        Path: The project directory path
    """
    dockerfile = temp_workspace / "Dockerfile"
    dockerfile.write_text('''
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "index.js"]
''')

    # Add package.json for version extraction
    (temp_workspace / "package.json").write_text(
        '{"name": "docker-app", "version": "1.0.0"}'
    )

    return temp_workspace


@pytest.fixture
def sample_maven_project(temp_workspace):
    """
    Create a sample Maven project structure.

    Returns:
        Path: The project directory path
    """
    pom_xml = temp_workspace / "pom.xml"
    pom_xml.write_text('''
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>sample-maven-project</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>
</project>
''')

    # Create source structure
    src_dir = temp_workspace / "src" / "main" / "java" / "com" / "example"
    src_dir.mkdir(parents=True)
    (src_dir / "App.java").write_text("package com.example; public class App {}")

    return temp_workspace


@pytest.fixture
def sample_gradle_project(temp_workspace):
    """
    Create a sample Gradle project structure.

    Returns:
        Path: The project directory path
    """
    build_gradle = temp_workspace / "build.gradle"
    build_gradle.write_text('''
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}
''')

    settings_gradle = temp_workspace / "settings.gradle"
    settings_gradle.write_text("rootProject.name = 'sample-gradle-project'")

    return temp_workspace


@pytest.fixture
def create_package_file(temp_workspace):
    """
    Factory fixture to create package files with specific content.

    Returns:
        Callable: Function to create package files
    """
    def _create_package(
        name: str = "test-package",
        version: str = "1.0.0",
        extension: str = ".tgz",
        size_bytes: int = 1024
    ) -> Path:
        filename = f"{name}-{version}{extension}"
        filepath = temp_workspace / filename

        # Create file with specified size
        content = b"mock package content" * (size_bytes // 20 + 1)
        filepath.write_bytes(content[:size_bytes])

        return filepath

    return _create_package


@pytest.fixture
def calculate_expected_checksum():
    """
    Factory fixture to calculate expected SHA256 checksums.

    Returns:
        Callable: Function to calculate checksum for a file
    """
    def _calculate(filepath: Path) -> str:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    return _calculate


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "ac1: Tests for AC#1 - npm Package Creation"
    )
    config.addinivalue_line(
        "markers", "ac2: Tests for AC#2 - Python Package Creation"
    )
    config.addinivalue_line(
        "markers", "ac3: Tests for AC#3 - NuGet Package Creation"
    )
    config.addinivalue_line(
        "markers", "ac4: Tests for AC#4 - Docker Image Creation"
    )
    config.addinivalue_line(
        "markers", "ac5: Tests for AC#5 - Multi-Format Package Creation"
    )
    config.addinivalue_line(
        "markers", "ac6: Tests for AC#6 - Package Validation"
    )
    config.addinivalue_line(
        "markers", "technical_spec: Tests for Technical Specification requirements"
    )
    config.addinivalue_line(
        "markers", "business_rule: Tests for Business Rules (BR-XXX)"
    )
    config.addinivalue_line(
        "markers", "nfr: Tests for Non-Functional Requirements (NFR-XXX)"
    )
    config.addinivalue_line(
        "markers", "edge_case: Tests for edge cases and error handling"
    )
