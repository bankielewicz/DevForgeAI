"""
Unit tests for VersionParser service (STORY-077).

Tests AC#2: Semver Parsing
- Parse standard versions (X.Y.Z)
- Parse pre-release versions (X.Y.Z-prerelease)
- Parse build metadata (X.Y.Z+build)
- Reject invalid version strings

Tests Technical Specification:
- SVC-004: Parse standard semver (X.Y.Z)
- SVC-005: Parse pre-release versions
- SVC-006: Parse build metadata
- SVC-007: Reject invalid version strings
- DataModel: Version with major, minor, patch, prerelease, build fields
- NFR-002: Version parsing < 10ms
"""

import pytest
import time
from unittest.mock import Mock


class TestVersionParserStandardFormat:
    """Test AC#2: Semver Parsing - Standard Format"""

    def test_should_parse_standard_version(self):
        """Given: "1.0.0"
        When: parse() called
        Then: returns Version(major=1, minor=0, patch=0)"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0")

        # Assert
        assert version.major == 1
        assert version.minor == 0
        assert version.patch == 0
        assert version.prerelease is None
        assert version.build is None

    def test_should_parse_version_with_leading_v_prefix(self):
        """Given: "v1.2.3"
        When: parse() called
        Then: correctly parses despite v prefix (or rejects clearly)"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("v1.2.3")

        # Assert (either strips v or raises clear error)
        if version is not None:
            assert version.major == 1
            assert version.minor == 2
            assert version.patch == 3

    def test_should_parse_version_0_0_0(self):
        """Given: "0.0.0" (initial development version)
        When: parse() called
        Then: correctly parses zero version"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("0.0.0")

        # Assert
        assert version.major == 0
        assert version.minor == 0
        assert version.patch == 0

    def test_should_parse_large_version_numbers(self):
        """Given: "10.20.30" (large version numbers)
        When: parse() called
        Then: correctly handles multi-digit components"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("10.20.30")

        # Assert
        assert version.major == 10
        assert version.minor == 20
        assert version.patch == 30

    def test_should_extract_major_minor_patch_components(self):
        """Given: "2.1.3"
        When: parse() called
        Then: major, minor, patch correctly extracted"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("2.1.3")

        # Assert
        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 3


class TestVersionParserPrerelease:
    """Test AC#2: Pre-release Version Parsing"""

    def test_should_parse_prerelease_alpha(self):
        """Given: "1.0.0-alpha"
        When: parse() called
        Then: prerelease="alpha" extracted correctly"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0-alpha")

        # Assert
        assert version.major == 1
        assert version.minor == 0
        assert version.patch == 0
        assert version.prerelease == "alpha"

    def test_should_parse_prerelease_with_number(self):
        """Given: "2.1.3-beta.1"
        When: parse() called
        Then: prerelease="beta.1" extracted correctly"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("2.1.3-beta.1")

        # Assert
        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 3
        assert version.prerelease == "beta.1"

    def test_should_parse_prerelease_rc(self):
        """Given: "1.0.0-rc.1"
        When: parse() called
        Then: prerelease="rc.1" extracted correctly"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0-rc.1")

        # Assert
        assert version.prerelease == "rc.1"

    def test_should_parse_prerelease_alpha_with_multiple_identifiers(self):
        """Given: "1.0.0-alpha.1.2"
        When: parse() called
        Then: full prerelease string preserved"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0-alpha.1.2")

        # Assert
        assert version.prerelease == "alpha.1.2"

    def test_should_correctly_parse_prerelease_without_trailing_numbers(self):
        """Given: "1.0.0-beta"
        When: parse() called
        Then: prerelease="beta" (no version number)"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0-beta")

        # Assert
        assert version.prerelease == "beta"


class TestVersionParserBuildMetadata:
    """Test AC#2: Build Metadata Parsing"""

    def test_should_parse_build_metadata(self):
        """Given: "1.0.0+build.456"
        When: parse() called
        Then: build="build.456" extracted correctly"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0+build.456")

        # Assert
        assert version.major == 1
        assert version.minor == 0
        assert version.patch == 0
        assert version.build == "build.456"

    def test_should_parse_build_metadata_with_date(self):
        """Given: "1.0.0+20231105"
        When: parse() called
        Then: build="20231105" extracted"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0+20231105")

        # Assert
        assert version.build == "20231105"

    def test_should_parse_prerelease_and_build_metadata_together(self):
        """Given: "1.2.3-alpha.1+build.456"
        When: parse() called
        Then: prerelease="alpha.1", build="build.456" both extracted"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.2.3-alpha.1+build.456")

        # Assert
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert version.prerelease == "alpha.1"
        assert version.build == "build.456"

    def test_should_handle_complex_build_metadata(self):
        """Given: "1.0.0+exp.sha.5114f85"
        When: parse() called
        Then: complex build metadata preserved"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act
        version = parser.parse("1.0.0+exp.sha.5114f85")

        # Assert
        assert version.build == "exp.sha.5114f85"


class TestVersionParserInvalidFormats:
    """Test AC#2: Invalid Version String Rejection"""

    def test_should_reject_invalid_format_too_few_parts(self):
        """Given: "1.2" (missing patch)
        When: parse() called
        Then: returns error with clear message"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            parser.parse("1.2")

        assert "semver" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    def test_should_reject_invalid_format_non_numeric(self):
        """Given: "a.b.c"
        When: parse() called
        Then: returns error about non-numeric parts"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            parser.parse("a.b.c")

        assert "numeric" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    def test_should_reject_completely_invalid_string(self):
        """Given: "invalid"
        When: parse() called
        Then: returns clear error message"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            parser.parse("invalid")

        assert "invalid" in str(exc_info.value).lower() or "semver" in str(exc_info.value).lower()

    def test_should_reject_version_with_too_many_parts(self):
        """Given: "1.2.3.4"
        When: parse() called
        Then: returns error about too many parts"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            parser.parse("1.2.3.4")

        assert "semver" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    def test_should_reject_negative_version_numbers(self):
        """Given: "-1.0.0"
        When: parse() called
        Then: returns error about negative numbers"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError):
            parser.parse("-1.0.0")

    def test_should_reject_empty_string(self):
        """Given: ""
        When: parse() called
        Then: returns error"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError):
            parser.parse("")

    def test_should_reject_whitespace_only(self):
        """Given: "   "
        When: parse() called
        Then: returns error"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError):
            parser.parse("   ")

    def test_should_reject_version_with_extra_characters(self):
        """Given: "1.0.0xyz"
        When: parse() called
        Then: returns error about invalid format"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        with pytest.raises(ValueError):
            parser.parse("1.0.0xyz")


class TestVersionParserPerformance:
    """Test NFR-002: Version parsing < 10ms"""

    def test_should_parse_standard_version_under_10ms(self):
        """Given: "1.2.3"
        When: parse() called
        Then: completes in < 10ms (NFR-002)"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        start = time.time()
        parser.parse("1.2.3")
        elapsed = (time.time() - start) * 1000  # Convert to ms

        assert elapsed < 10, f"Parsing took {elapsed}ms (expected < 10ms)"

    def test_should_parse_complex_version_under_10ms(self):
        """Given: "1.2.3-alpha.1+build.456"
        When: parse() called
        Then: completes in < 10ms even with prerelease and build"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()

        # Act & Assert
        start = time.time()
        parser.parse("1.2.3-alpha.1+build.456")
        elapsed = (time.time() - start) * 1000  # Convert to ms

        assert elapsed < 10, f"Parsing took {elapsed}ms (expected < 10ms)"


class TestVersionParserDataModel:
    """Test Version data model"""

    def test_should_create_version_object_with_all_fields(self):
        """Given: parsed version with all components
        When: Version object created
        Then: all fields accessible and correct"""
        # Arrange
        from installer.version_parser import VersionParser, Version

        parser = VersionParser()
        version = parser.parse("1.2.3-alpha.1+build.456")

        # Act & Assert
        assert isinstance(version, Version) or hasattr(version, 'major')
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert version.prerelease == "alpha.1"
        assert version.build == "build.456"

    def test_should_convert_version_to_string(self):
        """Given: Version object
        When: str() called
        Then: returns valid semver string"""
        # Arrange
        from installer.version_parser import VersionParser

        parser = VersionParser()
        version = parser.parse("1.2.3")

        # Act
        version_str = str(version)

        # Assert
        assert "1" in version_str
        assert "2" in version_str
        assert "3" in version_str

    def test_should_validate_version_components_non_negative(self):
        """Given: Version components
        When: Version object created
        Then: major, minor, patch must be >= 0"""
        # Arrange
        from installer.version_parser import Version

        # Act & Assert
        with pytest.raises(ValueError):
            Version(major=-1, minor=0, patch=0)

        with pytest.raises(ValueError):
            Version(major=1, minor=-1, patch=0)

        with pytest.raises(ValueError):
            Version(major=1, minor=0, patch=-1)
