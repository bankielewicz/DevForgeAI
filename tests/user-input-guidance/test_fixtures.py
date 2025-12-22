"""
Fixture Validation Tests

Tests validate that fixtures are properly formatted, non-empty, and distinct
between baseline and enhanced versions per AC#1 and AC#2.
"""

import pytest
import json
from pathlib import Path


class TestFixtureContentValidation:
    """Tests validate fixture content is non-empty and distinct"""

    def test_should_validate_baseline_fixtures_not_empty(self):
        """Arrange: Baseline fixtures
        Act: Read each fixture file
        Assert: All fixtures contain content"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        empty_fixtures = []
        if baseline_dir.exists():
            for fixture_file in sorted(baseline_dir.glob("baseline-*.txt")):
                content = fixture_file.read_text(encoding='utf-8').strip()
                if not content:
                    empty_fixtures.append(fixture_file.name)

        # Assert
        assert not empty_fixtures, f"Empty baseline fixtures: {', '.join(empty_fixtures)}"

    def test_should_validate_enhanced_fixtures_not_empty(self):
        """Arrange: Enhanced fixtures
        Act: Read each fixture file
        Assert: All fixtures contain content"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        empty_fixtures = []
        if enhanced_dir.exists():
            for fixture_file in sorted(enhanced_dir.glob("enhanced-*.txt")):
                content = fixture_file.read_text(encoding='utf-8').strip()
                if not content:
                    empty_fixtures.append(fixture_file.name)

        # Assert
        assert not empty_fixtures, f"Empty enhanced fixtures: {', '.join(empty_fixtures)}"

    def test_should_validate_baseline_fixtures_have_no_placeholder_content(self):
        """Arrange: Baseline fixtures
        Act: Check for placeholder markers (TBD, TODO, [PLACEHOLDER])
        Assert: No placeholder content found"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        placeholders = ["[PLACEHOLDER]", "{{PLACEHOLDER}}", "[TODO]", "[TBD]"]

        # Act
        fixtures_with_placeholders = {}
        if baseline_dir.exists():
            for fixture_file in sorted(baseline_dir.glob("baseline-*.txt")):
                content = fixture_file.read_text(encoding='utf-8').upper()
                found_placeholders = [p for p in placeholders if p.upper() in content]
                if found_placeholders:
                    fixtures_with_placeholders[fixture_file.name] = found_placeholders

        # Assert
        assert not fixtures_with_placeholders, \
            f"Fixtures with placeholder content: {fixtures_with_placeholders}"

    def test_should_validate_enhanced_fixtures_have_no_placeholder_content(self):
        """Arrange: Enhanced fixtures
        Act: Check for placeholder markers (TBD, TODO, [PLACEHOLDER])
        Assert: No placeholder content found"""
        # Arrange
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")
        placeholders = ["[PLACEHOLDER]", "{{PLACEHOLDER}}", "[TODO]", "[TBD]"]

        # Act
        fixtures_with_placeholders = {}
        if enhanced_dir.exists():
            for fixture_file in sorted(enhanced_dir.glob("enhanced-*.txt")):
                content = fixture_file.read_text(encoding='utf-8').upper()
                found_placeholders = [p for p in placeholders if p.upper() in content]
                if found_placeholders:
                    fixtures_with_placeholders[fixture_file.name] = found_placeholders

        # Assert
        assert not fixtures_with_placeholders, \
            f"Fixtures with placeholder content: {fixtures_with_placeholders}"


class TestFixturePairDistinctness:
    """Tests validate that baseline and enhanced fixtures are distinct"""

    def test_should_have_distinct_baseline_and_enhanced_content(self):
        """Arrange: Baseline and enhanced fixture pairs
        Act: Compare content of matching pairs
        Assert: Enhanced versions are different from baseline versions"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        identical_pairs = []
        if baseline_dir.exists() and enhanced_dir.exists():
            for i in range(1, 11):
                baseline_file = baseline_dir / f"baseline-{i:02d}.txt"
                enhanced_file = enhanced_dir / f"enhanced-{i:02d}.txt"

                if baseline_file.exists() and enhanced_file.exists():
                    baseline_content = baseline_file.read_text(encoding='utf-8').strip()
                    enhanced_content = enhanced_file.read_text(encoding='utf-8').strip()

                    if baseline_content == enhanced_content:
                        identical_pairs.append(f"Pair {i:02d}")

        # Assert
        assert not identical_pairs, \
            f"Enhanced fixtures are identical to baseline: {', '.join(identical_pairs)}"

    def test_should_have_meaningful_enhanced_content_difference(self):
        """Arrange: Baseline and enhanced fixture pairs
        Act: Measure content similarity (length difference ratio)
        Assert: Enhanced versions have meaningful additions (min 10% length increase)"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")
        min_increase_ratio = 0.10

        # Act
        minimal_differences = []
        if baseline_dir.exists() and enhanced_dir.exists():
            for i in range(1, 11):
                baseline_file = baseline_dir / f"baseline-{i:02d}.txt"
                enhanced_file = enhanced_dir / f"enhanced-{i:02d}.txt"

                if baseline_file.exists() and enhanced_file.exists():
                    baseline_len = len(baseline_file.read_text(encoding='utf-8'))
                    enhanced_len = len(enhanced_file.read_text(encoding='utf-8'))

                    if baseline_len > 0:
                        difference_ratio = (enhanced_len - baseline_len) / baseline_len
                        if difference_ratio < min_increase_ratio:
                            minimal_differences.append(
                                f"Pair {i:02d}: {difference_ratio*100:.1f}% increase (expected ≥{min_increase_ratio*100:.0f}%)"
                            )

        # Assert
        assert not minimal_differences, \
            f"Enhanced fixtures lack meaningful differences: {', '.join(minimal_differences)}"


class TestFixtureComplexityClassification:
    """Tests validate complexity classification accuracy"""

    def test_should_classify_simple_fixtures_correctly(self):
        """Arrange: Fixture metadata
        Act: Identify Simple complexity fixtures
        Assert: Simple fixtures are identified and count is 3"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        simple_count = 0
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])
                simple_count = sum(1 for f in fixtures if f.get("complexity_level") == "Simple")
            except json.JSONDecodeError:
                pass

        # Assert
        assert simple_count == 3, f"Expected 3 Simple fixtures, found {simple_count}"

    def test_should_classify_medium_fixtures_correctly(self):
        """Arrange: Fixture metadata
        Act: Identify Medium complexity fixtures
        Assert: Medium fixtures are identified and count is 4"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        medium_count = 0
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])
                medium_count = sum(1 for f in fixtures if f.get("complexity_level") == "Medium")
            except json.JSONDecodeError:
                pass

        # Assert
        assert medium_count == 4, f"Expected 4 Medium fixtures, found {medium_count}"

    def test_should_classify_complex_fixtures_correctly(self):
        """Arrange: Fixture metadata
        Act: Identify Complex fixtures
        Assert: Complex fixtures are identified and count is 3"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        complex_count = 0
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])
                complex_count = sum(1 for f in fixtures if f.get("complexity_level") == "Complex")
            except json.JSONDecodeError:
                pass

        # Assert
        assert complex_count == 3, f"Expected 3 Complex fixtures, found {complex_count}"


class TestFixtureMetadataValidation:
    """Tests validate fixture metadata structure per DVR2"""

    def test_should_have_valid_fixture_metadata_json(self):
        """Arrange: fixture-metadata.json
        Act: Parse JSON file
        Assert: File is valid JSON"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        json_valid = False
        json_error = None
        if metadata_file.exists():
            try:
                json.loads(metadata_file.read_text())
                json_valid = True
            except json.JSONDecodeError as e:
                json_error = str(e)

        # Assert
        assert json_valid, f"Invalid JSON in fixture-metadata.json: {json_error}"

    def test_should_have_metadata_for_all_fixtures(self):
        """Arrange: fixture-metadata.json
        Act: Count fixtures in metadata
        Assert: Exactly 10 fixtures documented"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        fixture_count = 0
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixture_count = len(metadata.get("fixtures", []))
            except json.JSONDecodeError:
                pass

        # Assert
        assert fixture_count == 10, f"Expected 10 fixtures in metadata, found {fixture_count}"

    def test_should_have_description_for_all_fixtures(self):
        """Arrange: fixture-metadata.json
        Act: Check each fixture has a description
        Assert: All fixtures have non-empty description"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        missing_descriptions = []
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                fixtures = metadata.get("fixtures", [])
                for fixture in fixtures:
                    description = fixture.get("description", "").strip()
                    if not description:
                        missing_descriptions.append(f"Fixture {fixture.get('fixture_number')}")
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_descriptions, \
            f"Fixtures missing description: {', '.join(missing_descriptions)}"
