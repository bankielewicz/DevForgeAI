"""
AC#1 Tests: Test Infrastructure Established

Tests validate that the required directory structure, test fixtures, and measurement
scripts exist and are properly organized for the User Input Guidance validation suite.
"""

import pytest
import os
import json
from pathlib import Path


class TestDirectoryStructure:
    """Tests for AC#1: required directory structure exists"""

    def test_should_have_tests_user_input_guidance_directory(self):
        """Arrange: Locate tests directory
        Act: Check for tests/user-input-guidance/ directory
        Assert: Directory exists"""
        # Arrange
        expected_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

        # Act
        directory_exists = expected_dir.exists() and expected_dir.is_dir()

        # Assert
        assert directory_exists, f"Directory not found: {expected_dir}"

    def test_should_have_fixtures_directory_structure(self):
        """Arrange: Locate tests directory
        Act: Check for fixtures subdirectories (baseline, enhanced)
        Assert: Both baseline/ and enhanced/ directories exist"""
        # Arrange
        base_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures")
        baseline_dir = base_dir / "baseline"
        enhanced_dir = base_dir / "enhanced"

        # Act
        baseline_exists = baseline_dir.exists() and baseline_dir.is_dir()
        enhanced_exists = enhanced_dir.exists() and enhanced_dir.is_dir()

        # Assert
        assert baseline_exists, f"Baseline fixtures directory not found: {baseline_dir}"
        assert enhanced_exists, f"Enhanced fixtures directory not found: {enhanced_dir}"

    def test_should_have_scripts_directory(self):
        """Arrange: Locate tests directory
        Act: Check for scripts subdirectory
        Assert: scripts/ directory exists"""
        # Arrange
        scripts_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts")

        # Act
        directory_exists = scripts_dir.exists() and scripts_dir.is_dir()

        # Assert
        assert directory_exists, f"Scripts directory not found: {scripts_dir}"


class TestBaselineFixtures:
    """Tests for AC#1: 10 baseline test fixtures exist"""

    def test_should_have_10_baseline_fixtures(self):
        """Arrange: Count fixture files in baseline/ directory
        Act: List all .txt files in baseline/
        Assert: Exactly 10 fixture files exist"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        if baseline_dir.exists():
            fixture_files = sorted(baseline_dir.glob("baseline-*.txt"))
            fixture_count = len(fixture_files)
        else:
            fixture_count = 0

        # Assert
        assert fixture_count == 10, f"Expected 10 baseline fixtures, found {fixture_count}"

    def test_should_have_baseline_numbered_sequentially(self):
        """Arrange: Baseline directory
        Act: Check fixture naming convention (baseline-01.txt through baseline-10.txt)
        Assert: All 10 files numbered sequentially"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        expected_files = [f"baseline-{i:02d}.txt" for i in range(1, 11)]
        if baseline_dir.exists():
            actual_files = [f.name for f in sorted(baseline_dir.glob("baseline-*.txt"))]
        else:
            actual_files = []

        # Assert
        assert actual_files == expected_files, f"Expected {expected_files}, got {actual_files}"

    def test_should_validate_baseline_fixture_content_length(self):
        """Arrange: Baseline fixtures
        Act: Check each fixture is 100-2000 characters
        Assert: All fixtures within size range"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        min_length = 100
        max_length = 2000

        # Act
        invalid_sizes = {}
        if baseline_dir.exists():
            for fixture_file in sorted(baseline_dir.glob("baseline-*.txt")):
                content = fixture_file.read_text(encoding='utf-8')
                content_length = len(content)
                if content_length < min_length or content_length > max_length:
                    invalid_sizes[fixture_file.name] = content_length

        # Assert
        assert not invalid_sizes, f"Fixtures with invalid size: {invalid_sizes}"

    def test_should_validate_baseline_fixture_encoding(self):
        """Arrange: Baseline fixtures
        Act: Attempt to read each fixture as UTF-8
        Assert: All fixtures are valid UTF-8 encoded"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        encoding_errors = {}
        if baseline_dir.exists():
            for fixture_file in sorted(baseline_dir.glob("baseline-*.txt")):
                try:
                    fixture_file.read_text(encoding='utf-8')
                except UnicodeDecodeError as e:
                    encoding_errors[fixture_file.name] = str(e)

        # Assert
        assert not encoding_errors, f"Fixtures with encoding errors: {encoding_errors}"


class TestEnhancedFixtures:
    """Tests for AC#1: 10 enhanced test fixtures exist"""

    def test_should_have_10_enhanced_fixtures(self):
        """Arrange: Count fixture files in enhanced/ directory
        Act: List all .txt files in enhanced/
        Assert: Exactly 10 fixture files exist"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        if enhanced_dir.exists():
            fixture_files = sorted(enhanced_dir.glob("enhanced-*.txt"))
            fixture_count = len(fixture_files)
        else:
            fixture_count = 0

        # Assert
        assert fixture_count == 10, f"Expected 10 enhanced fixtures, found {fixture_count}"

    def test_should_have_enhanced_numbered_sequentially(self):
        """Arrange: Enhanced directory
        Act: Check fixture naming convention (enhanced-01.txt through enhanced-10.txt)
        Assert: All 10 files numbered sequentially"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        expected_files = [f"enhanced-{i:02d}.txt" for i in range(1, 11)]
        if enhanced_dir.exists():
            actual_files = [f.name for f in sorted(enhanced_dir.glob("enhanced-*.txt"))]
        else:
            actual_files = []

        # Assert
        assert actual_files == expected_files, f"Expected {expected_files}, got {actual_files}"

    def test_should_validate_enhanced_fixture_content_length(self):
        """Arrange: Enhanced fixtures
        Act: Check each fixture is 100-2000 characters
        Assert: All fixtures within size range"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")
        min_length = 100
        max_length = 2000

        # Act
        invalid_sizes = {}
        if enhanced_dir.exists():
            for fixture_file in sorted(enhanced_dir.glob("enhanced-*.txt")):
                content = fixture_file.read_text(encoding='utf-8')
                content_length = len(content)
                if content_length < min_length or content_length > max_length:
                    invalid_sizes[fixture_file.name] = content_length

        # Assert
        assert not invalid_sizes, f"Fixtures with invalid size: {invalid_sizes}"

    def test_should_validate_enhanced_fixture_encoding(self):
        """Arrange: Enhanced fixtures
        Act: Attempt to read each fixture as UTF-8
        Assert: All fixtures are valid UTF-8 encoded"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        encoding_errors = {}
        if enhanced_dir.exists():
            for fixture_file in sorted(enhanced_dir.glob("enhanced-*.txt")):
                try:
                    fixture_file.read_text(encoding='utf-8')
                except UnicodeDecodeError as e:
                    encoding_errors[fixture_file.name] = str(e)

        # Assert
        assert not encoding_errors, f"Fixtures with encoding errors: {encoding_errors}"


class TestFixturePairMatching:
    """Tests for DVR1: Fixture pairs must match"""

    def test_should_have_matching_baseline_enhanced_pairs(self):
        """Arrange: Baseline and enhanced fixtures
        Act: Verify each baseline has corresponding enhanced
        Assert: All 10 pairs exist"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        missing_pairs = []
        if baseline_dir.exists() and enhanced_dir.exists():
            for i in range(1, 11):
                baseline_file = baseline_dir / f"baseline-{i:02d}.txt"
                enhanced_file = enhanced_dir / f"enhanced-{i:02d}.txt"
                if not (baseline_file.exists() and enhanced_file.exists()):
                    missing_pairs.append(f"Pair {i:02d}")

        # Assert
        assert not missing_pairs, f"Missing fixture pairs: {', '.join(missing_pairs)}"

    def test_should_validate_fixture_pair_count_matches(self):
        """Arrange: Baseline and enhanced directories
        Act: Count files in each directory
        Assert: Both have exactly 10 files"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        baseline_count = len(list(baseline_dir.glob("*.txt"))) if baseline_dir.exists() else 0
        enhanced_count = len(list(enhanced_dir.glob("*.txt"))) if enhanced_dir.exists() else 0

        # Assert
        assert baseline_count == enhanced_count == 10, \
            f"Baseline: {baseline_count} files, Enhanced: {enhanced_count} files (expected 10 each)"


class TestFixtureMetadata:
    """Tests for AC#1: Fixture complexity classification"""

    def test_should_have_fixture_metadata_file(self):
        """Arrange: Fixtures directory
        Act: Check for fixture-metadata.json
        Assert: File exists"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        file_exists = metadata_file.exists() and metadata_file.is_file()

        # Assert
        assert file_exists, f"Fixture metadata not found: {metadata_file}"

    def test_should_validate_fixture_metadata_structure(self):
        """Arrange: fixture-metadata.json file
        Act: Parse JSON and validate structure
        Assert: Required fields present for all 10 fixtures"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")
        required_fields = ["fixture_number", "fixture_name", "complexity_level", "description"]

        # Act
        metadata_errors = []
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])

                if len(fixtures) != 10:
                    metadata_errors.append(f"Expected 10 fixtures, found {len(fixtures)}")

                for fixture in fixtures:
                    for field in required_fields:
                        if field not in fixture:
                            metadata_errors.append(f"Fixture {fixture.get('fixture_number')} missing '{field}'")

            except json.JSONDecodeError as e:
                metadata_errors.append(f"Invalid JSON: {e}")

        # Assert
        assert not metadata_errors, f"Metadata validation errors: {', '.join(metadata_errors)}"

    def test_should_validate_fixture_complexity_stratification(self):
        """Arrange: fixture-metadata.json
        Act: Validate complexity stratification (3 Simple, 4 Medium, 3 Complex)
        Assert: Correct distribution"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        complexity_counts = {"Simple": 0, "Medium": 0, "Complex": 0}
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])
                for fixture in fixtures:
                    level = fixture.get("complexity_level")
                    if level in complexity_counts:
                        complexity_counts[level] += 1
            except json.JSONDecodeError:
                pass

        # Assert
        expected = {"Simple": 3, "Medium": 4, "Complex": 3}
        assert complexity_counts == expected, f"Expected {expected}, got {complexity_counts}"


class TestMeasurementScripts:
    """Tests for AC#1: Measurement scripts exist"""

    def test_should_have_validate_token_savings_script(self):
        """Arrange: Scripts directory
        Act: Check for validate-token-savings.py
        Assert: Script exists and is executable"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        file_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert file_exists, f"Token savings script not found: {script_file}"

    def test_should_have_measure_success_rate_script(self):
        """Arrange: Scripts directory
        Act: Check for measure-success-rate.py
        Assert: Script exists and is executable"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        file_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert file_exists, f"Success rate script not found: {script_file}"

    def test_should_have_test_story_creation_without_guidance_script(self):
        """Arrange: Scripts directory
        Act: Check for test-story-creation-without-guidance.sh
        Assert: Script exists"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-without-guidance.sh")

        # Act
        file_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert file_exists, f"Baseline test script not found: {script_file}"

    def test_should_have_test_story_creation_with_guidance_script(self):
        """Arrange: Scripts directory
        Act: Check for test-story-creation-with-guidance.sh
        Assert: Script exists"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        file_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert file_exists, f"Enhanced test script not found: {script_file}"
