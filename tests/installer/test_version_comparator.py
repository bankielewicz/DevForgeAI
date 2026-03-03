"""
Unit tests for VersionComparator service (STORY-077).

Tests AC#3: Upgrade Path Validation
- Identify upgrade/downgrade/same version relationships
- Detect upgrade type (major/minor/patch)

Tests AC#7: Pre-release Version Handling
- Correct pre-release ordering (alpha < beta < rc < stable)
- Stable > pre-release of same version

Tests Technical Specification:
- SVC-008: Compare versions and return relationship
- SVC-009: Detect downgrade scenarios
- SVC-010: Handle pre-release version ordering
- SVC-011: Identify upgrade type (major/minor/patch)
- BR-002: Pre-release versions follow semver precedence
- BR-003: Build metadata ignored in comparisons
"""

import pytest
from unittest.mock import Mock


class TestVersionComparatorBasicComparison:
    """Test AC#3: Upgrade Path Validation - Basic Relationships"""

    def test_should_identify_same_version(self):
        """Given: current=1.0.0, target=1.0.0
        When: compare() called
        Then: returns CompareResult.SAME"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0")
        target = parser.parse("1.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "SAME"
        assert result.upgrade_type is None

    def test_should_identify_upgrade(self):
        """Given: current=1.0.0, target=1.1.0
        When: compare() called
        Then: returns CompareResult.UPGRADE"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0")
        target = parser.parse("1.1.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type in ["MAJOR", "MINOR", "PATCH"]

    def test_should_identify_downgrade(self):
        """Given: current=2.0.0, target=1.5.0
        When: compare() called
        Then: returns CompareResult.DOWNGRADE"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "DOWNGRADE"


class TestVersionComparatorUpgradeType:
    """Test AC#3: Identify upgrade type (major/minor/patch)"""

    def test_should_identify_major_upgrade(self):
        """Given: current=1.0.0, target=2.0.0
        When: compare() called
        Then: returns upgrade_type='MAJOR'"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type == "MAJOR"
        assert result.is_breaking is True

    def test_should_identify_major_upgrade_with_higher_minor_patch(self):
        """Given: current=1.9.9, target=2.0.0
        When: compare() called
        Then: returns upgrade_type='MAJOR' (major change dominates)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.9.9")
        target = parser.parse("2.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.upgrade_type == "MAJOR"

    def test_should_identify_minor_upgrade(self):
        """Given: current=1.0.0, target=1.1.0
        When: compare() called
        Then: returns upgrade_type='MINOR'"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0")
        target = parser.parse("1.1.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type == "MINOR"
        assert result.is_breaking is False

    def test_should_identify_minor_upgrade_with_higher_patch(self):
        """Given: current=1.0.9, target=1.1.0
        When: compare() called
        Then: returns upgrade_type='MINOR' (minor change dominates patch)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.9")
        target = parser.parse("1.1.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.upgrade_type == "MINOR"

    def test_should_identify_patch_upgrade(self):
        """Given: current=1.0.0, target=1.0.1
        When: compare() called
        Then: returns upgrade_type='PATCH'"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0")
        target = parser.parse("1.0.1")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type == "PATCH"
        assert result.is_breaking is False


class TestVersionComparatorPrerelease:
    """Test AC#7: Pre-release Version Handling"""

    def test_should_identify_alpha_less_than_beta(self):
        """Given: current=1.0.0-alpha, target=1.0.0-beta
        When: compare() called
        Then: returns UPGRADE (beta > alpha)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0-alpha")
        target = parser.parse("1.0.0-beta")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"

    def test_should_identify_beta_less_than_rc(self):
        """Given: current=1.0.0-beta, target=1.0.0-rc.1
        When: compare() called
        Then: returns UPGRADE (rc > beta)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0-beta")
        target = parser.parse("1.0.0-rc.1")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"

    def test_should_identify_rc_less_than_stable(self):
        """Given: current=1.0.0-rc.1, target=1.0.0
        When: compare() called
        Then: returns UPGRADE (stable > rc)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0-rc.1")
        target = parser.parse("1.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"

    def test_should_follow_full_prerelease_ordering(self):
        """Given: versions: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-beta, 1.0.0-rc.1, 1.0.0
        When: compared in sequence
        Then: follow semver precedence (alpha < alpha.1 < beta < rc.1 < stable)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        versions = [
            parser.parse("1.0.0-alpha"),
            parser.parse("1.0.0-alpha.1"),
            parser.parse("1.0.0-beta"),
            parser.parse("1.0.0-rc.1"),
            parser.parse("1.0.0")
        ]

        # Act & Assert
        for i in range(len(versions) - 1):
            result = comparator.compare(versions[i], versions[i + 1])
            assert result.relationship == "UPGRADE", \
                f"{versions[i]} -> {versions[i+1]} should be UPGRADE"

    def test_should_identify_stable_greater_than_prerelease_of_same_version(self):
        """Given: current=1.0.0-alpha, target=1.0.0
        When: compare() called
        Then: returns UPGRADE (stable > pre-release)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0-alpha")
        target = parser.parse("1.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"


class TestVersionComparatorBuildMetadata:
    """Test BR-003: Build metadata ignored in comparisons"""

    def test_should_treat_versions_with_different_build_metadata_as_same(self):
        """Given: current=1.0.0+build.1, target=1.0.0+build.2
        When: compare() called
        Then: returns SAME (build metadata ignored)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0+build.1")
        target = parser.parse("1.0.0+build.2")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "SAME"

    def test_should_ignore_build_metadata_in_upgrade_detection(self):
        """Given: current=1.0.0+old, target=1.0.1+new
        When: compare() called
        Then: returns PATCH (build ignored, only version compared)"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.0.0+old")
        target = parser.parse("1.0.1+new")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.upgrade_type == "PATCH"


class TestVersionComparatorEdgeCases:
    """Test edge cases for version comparison"""

    def test_should_handle_0_0_0_to_1_0_0_upgrade(self):
        """Given: current=0.0.0, target=1.0.0
        When: compare() called
        Then: returns UPGRADE with MAJOR"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("0.0.0")
        target = parser.parse("1.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type == "MAJOR"

    def test_should_handle_versions_with_large_numbers(self):
        """Given: current=1.2.3, target=10.20.30
        When: compare() called
        Then: correctly identifies multi-digit upgrade"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.2.3")
        target = parser.parse("10.20.30")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"
        assert result.upgrade_type == "MAJOR"

    def test_should_mark_major_changes_as_breaking(self):
        """Given: major version change 1.x.x to 2.x.x
        When: compare() called
        Then: is_breaking=True"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()
        current = parser.parse("1.5.3")
        target = parser.parse("2.0.0")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.is_breaking is True

    def test_should_not_mark_minor_patch_as_breaking(self):
        """Given: minor or patch change
        When: compare() called
        Then: is_breaking=False"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()

        # Minor
        result_minor = comparator.compare(
            parser.parse("1.0.0"),
            parser.parse("1.1.0")
        )
        assert result_minor.is_breaking is False

        # Patch
        result_patch = comparator.compare(
            parser.parse("1.0.0"),
            parser.parse("1.0.1")
        )
        assert result_patch.is_breaking is False


class TestVersionComparatorReturnValue:
    """Test CompareResult data model"""

    def test_should_return_compare_result_object(self):
        """Given: two versions
        When: compare() called
        Then: returns CompareResult with all required fields"""
        # Arrange
        from installer.version_comparator import VersionComparator, CompareResult
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()

        # Act
        result = comparator.compare(
            parser.parse("1.0.0"),
            parser.parse("2.0.0")
        )

        # Assert
        assert hasattr(result, 'relationship') or isinstance(result, dict)
        assert hasattr(result, 'upgrade_type') or 'upgrade_type' in result
        assert hasattr(result, 'is_breaking') or 'is_breaking' in result

    def test_should_include_warnings_in_compare_result(self):
        """Given: major version upgrade
        When: compare() called
        Then: result may include warnings list"""
        # Arrange
        from installer.version_comparator import VersionComparator
        from installer.version_parser import VersionParser

        parser = VersionParser()
        comparator = VersionComparator()

        # Act
        result = comparator.compare(
            parser.parse("1.0.0"),
            parser.parse("2.0.0")
        )

        # Assert (warnings optional)
        if hasattr(result, 'warnings'):
            assert isinstance(result.warnings, list)
