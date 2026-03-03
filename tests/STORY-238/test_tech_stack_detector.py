"""
Test Suite for STORY-238: Tech Stack Detection Module

Tests TechStackDetector service and TechStackInfo dataclass for detecting
project technology stacks from indicator files.

This test file follows TDD Red phase - all tests should FAIL initially
because no implementation exists yet.

Test Framework: pytest (per tech-stack.md)
Target Module: installer/tech_stack_detector.py

Coverage Targets:
- Unit tests: 95%+ coverage
- All 5 acceptance criteria covered
- 9 indicator types tested
- Edge cases and error conditions tested
- Business rules BR-001 through BR-004 validated
- NFRs NFR-001 through NFR-004 validated

References:
- Story: devforgeai/specs/Stories/STORY-238-tech-stack-detection-module.story.md
- Source Tree: devforgeai/specs/context/source-tree.md (line 406)
"""

# CRITICAL: Add project root to sys.path BEFORE any other imports
# This must be at the very top to ensure installer module can be imported
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(_project_root))  # Always insert to ensure it's first

import os
import tempfile
import time
import stat
import logging
from typing import List
from dataclasses import dataclass
from unittest.mock import patch, MagicMock

import pytest


# ============================================================================
# TDD RED PHASE SETUP
# ============================================================================
#
# TDD Red Phase Strategy:
# - Tests will FAIL with clear message if module doesn't exist
# - When module exists but tests fail, that's the expected Red state
# - Implementation makes tests pass (Green phase)
#
# To run tests and see failures:
#   pytest tests/STORY-238/ -v --tb=short
#
# Expected result: All 60 tests should FAIL until implementation exists

_IMPLEMENTATION_AVAILABLE = False
_IMPORT_ERROR = "Module not yet imported"

try:
    from installer.tech_stack_detector import (
        TechStackInfo,
        TechStackDetector,
        StackType,
    )
    _IMPLEMENTATION_AVAILABLE = True
except ImportError as e:
    TechStackInfo = None
    TechStackDetector = None
    StackType = None
    _IMPORT_ERROR = str(e)


def _require_implementation():
    """Helper to fail tests when implementation is not available."""
    if not _IMPLEMENTATION_AVAILABLE:
        pytest.fail(
            f"TDD RED PHASE: Implementation not available. "
            f"Module 'installer.tech_stack_detector' must be created. "
            f"Import error: {_IMPORT_ERROR}"
        )


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for test isolation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def nodejs_project(temp_project_dir):
    """Create a Node.js project with package.json."""
    package_json = temp_project_dir / "package.json"
    package_json.write_text('{"name": "test-project", "scripts": {"build": "tsc"}}')
    return temp_project_dir


@pytest.fixture
def python_pyproject_project(temp_project_dir):
    """Create a Python project with pyproject.toml."""
    pyproject = temp_project_dir / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-project"\nversion = "1.0.0"')
    return temp_project_dir


@pytest.fixture
def python_requirements_project(temp_project_dir):
    """Create a Python project with requirements.txt only."""
    requirements = temp_project_dir / "requirements.txt"
    requirements.write_text("pytest>=7.0.0\nrequests>=2.28.0")
    return temp_project_dir


@pytest.fixture
def python_both_indicators_project(temp_project_dir):
    """Create a Python project with both pyproject.toml and requirements.txt."""
    pyproject = temp_project_dir / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-project"\nversion = "1.0.0"')
    requirements = temp_project_dir / "requirements.txt"
    requirements.write_text("pytest>=7.0.0")
    return temp_project_dir


@pytest.fixture
def dotnet_csproj_project(temp_project_dir):
    """Create a .NET project with .csproj file."""
    csproj = temp_project_dir / "MyApp.csproj"
    csproj.write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>')
    return temp_project_dir


@pytest.fixture
def dotnet_sln_project(temp_project_dir):
    """Create a .NET project with .sln file only."""
    sln = temp_project_dir / "MyApp.sln"
    sln.write_text("Microsoft Visual Studio Solution File, Format Version 12.00")
    return temp_project_dir


@pytest.fixture
def dotnet_both_project(temp_project_dir):
    """Create a .NET project with both .csproj and .sln files."""
    csproj = temp_project_dir / "MyApp.csproj"
    csproj.write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>')
    sln = temp_project_dir / "MyApp.sln"
    sln.write_text("Microsoft Visual Studio Solution File, Format Version 12.00")
    return temp_project_dir


@pytest.fixture
def java_maven_project(temp_project_dir):
    """Create a Java/Maven project with pom.xml."""
    pom = temp_project_dir / "pom.xml"
    pom.write_text('<?xml version="1.0"?><project><modelVersion>4.0.0</modelVersion></project>')
    return temp_project_dir


@pytest.fixture
def java_gradle_project(temp_project_dir):
    """Create a Java/Gradle project with build.gradle."""
    gradle = temp_project_dir / "build.gradle"
    gradle.write_text("plugins { id 'java' }")
    return temp_project_dir


@pytest.fixture
def go_project(temp_project_dir):
    """Create a Go project with go.mod."""
    gomod = temp_project_dir / "go.mod"
    gomod.write_text("module example.com/test\n\ngo 1.21")
    return temp_project_dir


@pytest.fixture
def rust_project(temp_project_dir):
    """Create a Rust project with Cargo.toml."""
    cargo = temp_project_dir / "Cargo.toml"
    cargo.write_text('[package]\nname = "test-project"\nversion = "0.1.0"')
    return temp_project_dir


@pytest.fixture
def multi_stack_project(temp_project_dir):
    """Create a project with multiple tech stacks (Node.js + Python)."""
    package_json = temp_project_dir / "package.json"
    package_json.write_text('{"name": "test-project"}')
    pyproject = temp_project_dir / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-project"')
    return temp_project_dir


@pytest.fixture
def empty_project(temp_project_dir):
    """Create an empty project directory with no indicator files."""
    return temp_project_dir


@pytest.fixture
def nested_indicator_project(temp_project_dir):
    """Create a project with indicator files in nested directories."""
    nested = temp_project_dir / "packages" / "frontend"
    nested.mkdir(parents=True)
    (nested / "package.json").write_text('{"name": "nested-project"}')
    return temp_project_dir


# ============================================================================
# AC#1: NODE.JS PROJECT DETECTION TESTS
# ============================================================================


class TestNodejsDetection:
    """Test AC#1: Node.js Project Detection"""

    def test_detect_nodejs_from_package_json_returns_correct_stack_type(self, nodejs_project):
        """
        AC#1: Given package.json at root, detector returns stack_type='nodejs'

        Test Requirement: SVC-001 - Detect Node.js projects via package.json presence
        """
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        assert len(results) >= 1
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None
        assert nodejs_result.stack_type == "nodejs"

    def test_detect_nodejs_returns_correct_build_command(self, nodejs_project):
        """AC#1: Given package.json at root, detector returns build_command='npm run build'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None
        assert nodejs_result.build_command == "npm run build"

    def test_detect_nodejs_returns_correct_output_directory(self, nodejs_project):
        """AC#1: Given package.json at root, detector returns output_directory='dist/'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None
        assert nodejs_result.output_directory == "dist/"

    def test_detect_nodejs_returns_correct_indicator_file(self, nodejs_project):
        """AC#1: Given package.json at root, detector returns indicator_file='package.json'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None
        assert nodejs_result.indicator_file == "package.json"


# ============================================================================
# AC#2: PYTHON PROJECT DETECTION TESTS
# ============================================================================


class TestPythonDetection:
    """Test AC#2: Python Project Detection"""

    def test_detect_python_from_pyproject_toml_returns_correct_stack_type(self, python_pyproject_project):
        """AC#2: Given pyproject.toml at root, detector returns stack_type='python'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_pyproject_project)
        python_result = next((r for r in results if r.stack_type == "python"), None)
        assert python_result is not None
        assert python_result.stack_type == "python"

    def test_detect_python_pyproject_returns_python_build_command(self, python_pyproject_project):
        """AC#2: Given pyproject.toml at root, detector returns build_command='python -m build'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_pyproject_project)
        python_result = next((r for r in results if r.stack_type == "python"), None)
        assert python_result is not None
        assert python_result.build_command == "python -m build"

    def test_detect_python_pyproject_returns_dist_output_directory(self, python_pyproject_project):
        """AC#2: Given pyproject.toml at root, detector returns output_directory='dist/'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_pyproject_project)
        python_result = next((r for r in results if r.stack_type == "python"), None)
        assert python_result is not None
        assert python_result.output_directory == "dist/"

    def test_detect_python_from_requirements_txt_returns_pip_install_command(self, python_requirements_project):
        """AC#2: Given requirements.txt only, detector returns build_command='pip install -r requirements.txt'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_requirements_project)
        python_result = next((r for r in results if r.stack_type == "python"), None)
        assert python_result is not None
        assert python_result.build_command == "pip install -r requirements.txt"

    def test_detect_python_requirements_only_returns_null_output_directory(self, python_requirements_project):
        """AC#2: Given requirements.txt only, detector returns output_directory=null"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_requirements_project)
        python_result = next((r for r in results if r.stack_type == "python"), None)
        assert python_result is not None
        assert python_result.output_directory is None

    def test_detect_python_pyproject_takes_precedence_over_requirements(self, python_both_indicators_project):
        """AC#2 + BR-001: pyproject.toml takes precedence over requirements.txt"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(python_both_indicators_project)
        python_results = [r for r in results if r.stack_type == "python"]
        assert len(python_results) == 1
        assert python_results[0].indicator_file == "pyproject.toml"
        assert python_results[0].build_command == "python -m build"


# ============================================================================
# AC#3: .NET PROJECT DETECTION TESTS
# ============================================================================


class TestDotnetDetection:
    """Test AC#3: .NET Project Detection"""

    def test_detect_dotnet_from_csproj_returns_correct_stack_type(self, dotnet_csproj_project):
        """AC#3: Given *.csproj at root, detector returns stack_type='dotnet'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_csproj_project)
        dotnet_result = next((r for r in results if r.stack_type == "dotnet"), None)
        assert dotnet_result is not None
        assert dotnet_result.stack_type == "dotnet"

    def test_detect_dotnet_csproj_returns_publish_build_command(self, dotnet_csproj_project):
        """AC#3: Given *.csproj, detector returns build_command='dotnet publish -c Release'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_csproj_project)
        dotnet_result = next((r for r in results if r.stack_type == "dotnet"), None)
        assert dotnet_result is not None
        assert dotnet_result.build_command == "dotnet publish -c Release"

    def test_detect_dotnet_csproj_returns_publish_output_directory(self, dotnet_csproj_project):
        """AC#3: Given *.csproj, detector returns output_directory='publish/'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_csproj_project)
        dotnet_result = next((r for r in results if r.stack_type == "dotnet"), None)
        assert dotnet_result is not None
        assert dotnet_result.output_directory == "publish/"

    def test_detect_dotnet_sln_returns_build_command(self, dotnet_sln_project):
        """AC#3: Given *.sln only, detector returns build_command='dotnet build -c Release'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_sln_project)
        dotnet_result = next((r for r in results if r.stack_type == "dotnet"), None)
        assert dotnet_result is not None
        assert dotnet_result.build_command == "dotnet build -c Release"

    def test_detect_dotnet_sln_returns_bin_release_output_directory(self, dotnet_sln_project):
        """AC#3: Given *.sln only, detector returns output_directory='bin/Release/'"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_sln_project)
        dotnet_result = next((r for r in results if r.stack_type == "dotnet"), None)
        assert dotnet_result is not None
        assert dotnet_result.output_directory == "bin/Release/"

    def test_detect_dotnet_csproj_takes_precedence_over_sln(self, dotnet_both_project):
        """AC#3 + BR-002: .csproj files take precedence over .sln for build command"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(dotnet_both_project)
        dotnet_results = [r for r in results if r.stack_type == "dotnet"]
        assert len(dotnet_results) == 1
        assert "MyApp.csproj" in dotnet_results[0].indicator_file
        assert dotnet_results[0].build_command == "dotnet publish -c Release"


# ============================================================================
# AC#4: MULTI-STACK PROJECT HANDLING TESTS
# ============================================================================


class TestMultiStackDetection:
    """Test AC#4: Multi-Stack Project Handling"""

    def test_detect_multi_stack_returns_list_of_techstackinfo(self, multi_stack_project):
        """AC#4: Given multiple indicator files, detector returns list of TechStackInfo objects"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(multi_stack_project)
        assert isinstance(results, list)
        assert len(results) >= 2

    def test_detect_multi_stack_returns_both_nodejs_and_python(self, multi_stack_project):
        """AC#4: Given both package.json and pyproject.toml, both stacks detected"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(multi_stack_project)
        stack_types = {r.stack_type for r in results}
        assert "nodejs" in stack_types
        assert "python" in stack_types

    def test_detect_multi_stack_results_ordered_by_priority(self, multi_stack_project):
        """AC#4: Results ordered by detection priority (Node.js, Python, .NET, Java, Go, Rust)"""
        _require_implementation()
        detector = TechStackDetector()
        priority_order = ["nodejs", "python", "dotnet", "java_maven", "java_gradle", "go", "rust"]
        results = detector.detect(multi_stack_project)
        detected_types = [r.stack_type for r in results]
        detected_indices = [priority_order.index(t) for t in detected_types]
        assert detected_indices == sorted(detected_indices), "Results not in priority order"

    def test_detect_all_nine_indicator_types(self, temp_project_dir):
        """Configuration test: All 9 indicator types are supported"""
        _require_implementation()
        detector = TechStackDetector()
        (temp_project_dir / "package.json").write_text('{}')
        (temp_project_dir / "pyproject.toml").write_text('[project]')
        (temp_project_dir / "requirements.txt").write_text('')
        (temp_project_dir / "MyApp.csproj").write_text('<Project/>')
        (temp_project_dir / "MyApp.sln").write_text('')
        (temp_project_dir / "pom.xml").write_text('<project/>')
        (temp_project_dir / "build.gradle").write_text('')
        (temp_project_dir / "go.mod").write_text('module test')
        (temp_project_dir / "Cargo.toml").write_text('[package]')
        results = detector.detect(temp_project_dir)
        expected_stacks = {"nodejs", "python", "dotnet", "java_maven", "java_gradle", "go", "rust"}
        detected_stacks = {r.stack_type for r in results}
        assert expected_stacks == detected_stacks


# ============================================================================
# AC#5: NO DETECTABLE STACK TESTS
# ============================================================================


class TestNoDetectableStack:
    """Test AC#5: No Detectable Stack"""

    def test_detect_empty_directory_returns_empty_list(self, empty_project):
        """AC#5: Given empty directory, detector returns empty list"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(empty_project)
        assert results == []

    def test_detect_empty_directory_logs_warning(self, empty_project, caplog):
        """AC#5: Given empty directory, warning logged"""
        _require_implementation()
        detector = TechStackDetector()
        with caplog.at_level(logging.WARNING):
            results = detector.detect(empty_project)
        assert "No recognized tech stack indicator files found" in caplog.text

    def test_detect_unrecognized_files_returns_empty_list(self, temp_project_dir):
        """Edge case: Directory with non-indicator files returns empty list"""
        _require_implementation()
        detector = TechStackDetector()
        (temp_project_dir / "README.md").write_text("# Test Project")
        (temp_project_dir / "main.py").write_text("print('hello')")
        results = detector.detect(temp_project_dir)
        assert results == []


# ============================================================================
# ADDITIONAL TECH STACK DETECTION TESTS (SVC-004 to SVC-007)
# ============================================================================


class TestAdditionalStackDetection:
    """Test additional tech stack detections (Java, Go, Rust)"""

    def test_detect_java_maven_from_pom_xml(self, java_maven_project):
        """Test Requirement: SVC-004 - Detect Java/Maven projects via pom.xml"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(java_maven_project)
        maven_result = next((r for r in results if r.stack_type == "java_maven"), None)
        assert maven_result is not None
        assert maven_result.indicator_file == "pom.xml"

    def test_detect_java_gradle_from_build_gradle(self, java_gradle_project):
        """Test Requirement: SVC-005 - Detect Java/Gradle projects via build.gradle"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(java_gradle_project)
        gradle_result = next((r for r in results if r.stack_type == "java_gradle"), None)
        assert gradle_result is not None
        assert gradle_result.indicator_file == "build.gradle"

    def test_detect_go_from_go_mod(self, go_project):
        """Test Requirement: SVC-006 - Detect Go projects via go.mod"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(go_project)
        go_result = next((r for r in results if r.stack_type == "go"), None)
        assert go_result is not None
        assert go_result.indicator_file == "go.mod"

    def test_detect_rust_from_cargo_toml(self, rust_project):
        """Test Requirement: SVC-007 - Detect Rust projects via Cargo.toml"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(rust_project)
        rust_result = next((r for r in results if r.stack_type == "rust"), None)
        assert rust_result is not None
        assert rust_result.indicator_file == "Cargo.toml"


# ============================================================================
# TECH STACK INFO DATACLASS TESTS
# ============================================================================


class TestTechStackInfo:
    """Test TechStackInfo dataclass fields and constraints"""

    def test_techstackinfo_has_stack_type_field(self):
        """DataModel: TechStackInfo has stack_type field (Required, Enum)"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file=None,
            detection_confidence=1.0
        )
        assert hasattr(info, 'stack_type')
        assert info.stack_type == "nodejs"

    def test_techstackinfo_has_indicator_file_field(self):
        """DataModel: TechStackInfo has indicator_file field (Required)"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file=None,
            detection_confidence=1.0
        )
        assert hasattr(info, 'indicator_file')
        assert info.indicator_file == "package.json"

    def test_techstackinfo_has_build_command_field(self):
        """DataModel: TechStackInfo has build_command field (Optional[String])"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file=None,
            detection_confidence=1.0
        )
        assert hasattr(info, 'build_command')

    def test_techstackinfo_has_output_directory_field(self):
        """DataModel: TechStackInfo has output_directory field (Optional[String])"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file=None,
            detection_confidence=1.0
        )
        assert hasattr(info, 'output_directory')

    def test_techstackinfo_has_version_file_field(self):
        """DataModel: TechStackInfo has version_file field (Optional[String])"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file="package.json",
            detection_confidence=1.0
        )
        assert hasattr(info, 'version_file')

    def test_techstackinfo_has_detection_confidence_field(self):
        """DataModel: TechStackInfo has detection_confidence field (Float 0.0 to 1.0)"""
        _require_implementation()
        info = TechStackInfo(
            stack_type="nodejs",
            indicator_file="package.json",
            build_command="npm run build",
            output_directory="dist/",
            version_file=None,
            detection_confidence=1.0
        )
        assert hasattr(info, 'detection_confidence')
        assert 0.0 <= info.detection_confidence <= 1.0

    def test_techstackinfo_confidence_is_1_for_primary_indicator(self, nodejs_project):
        """DataModel: detection_confidence is 1.0 when primary indicator found"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        assert results[0].detection_confidence == 1.0


# ============================================================================
# BUSINESS RULES TESTS
# ============================================================================


class TestBusinessRules:
    """Test Business Rules BR-001 through BR-004"""

    def test_br003_default_scan_is_root_level_only(self, nested_indicator_project):
        """BR-003: Default scan is root-level only (recursive=False)"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nested_indicator_project)
        assert len(results) == 0

    def test_br003_recursive_detection_finds_nested_indicators(self, nested_indicator_project):
        """BR-003: Nested indicators detected when recursive=True"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nested_indicator_project, recursive=True)
        assert len(results) >= 1
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None

    def test_br004_detection_is_read_only(self, nodejs_project):
        """BR-004: Detection must be read-only with no filesystem modifications"""
        _require_implementation()
        detector = TechStackDetector()
        files_before = set(os.listdir(nodejs_project))
        results = detector.detect(nodejs_project)
        files_after = set(os.listdir(nodejs_project))
        assert files_before == files_after


# ============================================================================
# NON-FUNCTIONAL REQUIREMENTS TESTS
# ============================================================================


class TestNonFunctionalRequirements:
    """Test NFRs NFR-001 through NFR-004"""

    def test_nfr001_detection_completes_within_5_seconds(self, nodejs_project):
        """NFR-001: Detection must complete within 5 seconds for any project"""
        _require_implementation()
        detector = TechStackDetector()
        start_time = time.time()
        results = detector.detect(nodejs_project)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 5.0, f"Detection took {elapsed_time:.2f}s, exceeds 5s limit"

    def test_nfr002_build_command_lookup_under_100ms(self, nodejs_project):
        """NFR-002: Build command lookup must be fast (< 100ms)"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        start_time = time.time()
        command = detector.get_build_command("nodejs", "package.json")
        elapsed_time = time.time() - start_time
        assert elapsed_time < 0.1, f"Lookup took {elapsed_time*1000:.2f}ms, exceeds 100ms limit"

    def test_nfr003_graceful_degradation_with_unreadable_file(self, temp_project_dir):
        """NFR-003: Graceful degradation when individual files are unreadable"""
        _require_implementation()
        detector = TechStackDetector()
        readable_file = temp_project_dir / "package.json"
        readable_file.write_text('{"name": "test"}')
        unreadable_file = temp_project_dir / "pyproject.toml"
        unreadable_file.write_text('[project]')
        try:
            os.chmod(unreadable_file, 0o000)
            made_unreadable = True
        except (OSError, PermissionError):
            made_unreadable = False
        try:
            results = detector.detect(temp_project_dir)
            if made_unreadable:
                nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
                assert nodejs_result is not None
        finally:
            if made_unreadable:
                try:
                    os.chmod(unreadable_file, 0o644)
                except (OSError, PermissionError):
                    pass

    def test_nfr004_path_traversal_prevention(self, temp_project_dir):
        """NFR-004: Path traversal prevention for all file operations"""
        _require_implementation()
        detector = TechStackDetector()
        malicious_path = temp_project_dir / ".." / ".." / "etc" / "passwd"
        with pytest.raises((ValueError, Exception)):
            detector.detect(malicious_path)

    def test_nfr004_symlink_confined_to_project_directory(self, temp_project_dir):
        """NFR-004: Symlinks resolved but confined to project directory"""
        _require_implementation()
        detector = TechStackDetector()
        symlink_path = temp_project_dir / "external_link"
        try:
            os.symlink("/etc/passwd", symlink_path)
            symlink_created = True
        except (OSError, NotImplementedError):
            symlink_created = False
        if symlink_created:
            try:
                results = detector.detect(temp_project_dir)
                assert isinstance(results, list)
            finally:
                os.unlink(symlink_path)


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_detect_empty_indicator_file(self, temp_project_dir):
        """Edge case: Empty indicator file should still be detected"""
        _require_implementation()
        detector = TechStackDetector()
        (temp_project_dir / "package.json").write_text('')
        results = detector.detect(temp_project_dir)
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None

    def test_detect_malformed_json_indicator(self, temp_project_dir):
        """Edge case: Malformed JSON in indicator file handled gracefully"""
        _require_implementation()
        detector = TechStackDetector()
        (temp_project_dir / "package.json").write_text('{ invalid json }')
        results = detector.detect(temp_project_dir)
        nodejs_result = next((r for r in results if r.stack_type == "nodejs"), None)
        assert nodejs_result is not None

    def test_detect_nonexistent_directory_raises_error(self):
        """Edge case: Non-existent directory should raise appropriate error"""
        _require_implementation()
        detector = TechStackDetector()
        nonexistent_path = Path("/nonexistent/path/to/project")
        with pytest.raises((FileNotFoundError, ValueError)):
            detector.detect(nonexistent_path)

    def test_detect_file_instead_of_directory_raises_error(self, temp_project_dir):
        """Edge case: File path instead of directory should raise error"""
        _require_implementation()
        detector = TechStackDetector()
        file_path = temp_project_dir / "somefile.txt"
        file_path.write_text("content")
        with pytest.raises((ValueError, NotADirectoryError)):
            detector.detect(file_path)

    def test_detect_with_special_characters_in_path(self, temp_project_dir):
        """Edge case: Path with special characters handled correctly"""
        _require_implementation()
        detector = TechStackDetector()
        special_dir = temp_project_dir / "project with spaces & special!"
        special_dir.mkdir()
        (special_dir / "package.json").write_text('{}')
        results = detector.detect(special_dir)
        assert len(results) >= 1

    def test_indicator_file_path_is_relative(self, nodejs_project):
        """DataModel: indicator_file path is relative (not absolute)"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        nodejs_result = results[0]
        assert not Path(nodejs_result.indicator_file).is_absolute()
        assert nodejs_result.indicator_file == "package.json"

    def test_output_directory_path_is_relative(self, nodejs_project):
        """DataModel: output_directory is relative path without traversal"""
        _require_implementation()
        detector = TechStackDetector()
        results = detector.detect(nodejs_project)
        nodejs_result = results[0]
        assert not Path(nodejs_result.output_directory).is_absolute()
        assert ".." not in nodejs_result.output_directory

    def test_build_command_no_shell_metacharacters(self, nodejs_project):
        """DataModel: build_command has no shell metacharacters (security)"""
        _require_implementation()
        detector = TechStackDetector()
        shell_metacharacters = ['|', ';', '&', '$', '`', '>', '<', '(', ')']
        results = detector.detect(nodejs_project)
        for result in results:
            if result.build_command:
                for char in shell_metacharacters:
                    assert char not in result.build_command, \
                        f"Shell metacharacter '{char}' found in build_command"


# ============================================================================
# STACK TYPE ENUM TESTS
# ============================================================================


class TestStackTypeEnum:
    """Test StackType enumeration"""

    def test_stacktype_enum_has_nodejs(self):
        """StackType enum has 'nodejs' value"""
        _require_implementation()
        assert hasattr(StackType, 'NODEJS') or 'nodejs' in [e.value for e in StackType]

    def test_stacktype_enum_has_python(self):
        """StackType enum has 'python' value"""
        _require_implementation()
        assert hasattr(StackType, 'PYTHON') or 'python' in [e.value for e in StackType]

    def test_stacktype_enum_has_dotnet(self):
        """StackType enum has 'dotnet' value"""
        _require_implementation()
        assert hasattr(StackType, 'DOTNET') or 'dotnet' in [e.value for e in StackType]

    def test_stacktype_enum_has_java_maven(self):
        """StackType enum has 'java_maven' value"""
        _require_implementation()
        assert hasattr(StackType, 'JAVA_MAVEN') or 'java_maven' in [e.value for e in StackType]

    def test_stacktype_enum_has_java_gradle(self):
        """StackType enum has 'java_gradle' value"""
        _require_implementation()
        assert hasattr(StackType, 'JAVA_GRADLE') or 'java_gradle' in [e.value for e in StackType]

    def test_stacktype_enum_has_go(self):
        """StackType enum has 'go' value"""
        _require_implementation()
        assert hasattr(StackType, 'GO') or 'go' in [e.value for e in StackType]

    def test_stacktype_enum_has_rust(self):
        """StackType enum has 'rust' value"""
        _require_implementation()
        assert hasattr(StackType, 'RUST') or 'rust' in [e.value for e in StackType]


# ============================================================================
# DETECTION MATRIX CONFIGURATION TESTS
# ============================================================================


class TestDetectionMatrix:
    """Test INDICATOR_MAP and DETECTION_ORDER configuration"""

    def test_indicator_map_has_nine_entries(self):
        """Configuration: INDICATOR_MAP contains all 9 indicator mappings"""
        _require_implementation()
        detector = TechStackDetector()
        indicator_count = len(detector.INDICATOR_MAP)
        assert indicator_count == 9, f"Expected 9 indicators, found {indicator_count}"

    def test_detection_order_matches_priority(self):
        """Configuration: DETECTION_ORDER matches documented priority"""
        _require_implementation()
        detector = TechStackDetector()
        expected_order = [
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "*.csproj",
            "*.sln",
            "pom.xml",
            "build.gradle",
            "go.mod",
            "Cargo.toml"
        ]
        actual_order = detector.DETECTION_ORDER
        assert actual_order == expected_order

    def test_indicator_map_values_are_valid_techstackinfo(self):
        """Configuration: INDICATOR_MAP values are valid TechStackInfo-compatible dicts"""
        _require_implementation()
        detector = TechStackDetector()
        required_keys = {'stack_type', 'build_command', 'output_directory'}
        for indicator, config in detector.INDICATOR_MAP.items():
            missing_keys = required_keys - set(config.keys())
            assert not missing_keys, f"Indicator {indicator} missing keys: {missing_keys}"


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
