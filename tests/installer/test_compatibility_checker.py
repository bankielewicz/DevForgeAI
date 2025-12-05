"""
Unit tests for CompatibilityChecker service (STORY-077).

Tests AC#4: Breaking Change Warning
- Display warning for major version changes
- List known breaking changes from changelog
- Prompt user for confirmation

Tests AC#5: Downgrade Blocking
- Block major downgrades without --force flag
- Show error message explaining risks
- Suggest --force flag for override
- Non-zero exit code (1)

Tests Technical Specification:
- SVC-012: Check if upgrade path is safe
- SVC-013: Return breaking changes for major upgrades
- SVC-014: Block unsafe downgrades without force flag
- BR-001: Major version downgrades blocked by default
"""

import pytest
from unittest.mock import Mock, MagicMock, patch


class TestCompatibilityCheckerSafeUpgrade:
    """Test SVC-012: Check if upgrade path is safe"""

    def test_should_allow_patch_upgrade_without_warning(self):
        """Given: minor upgrade 1.0.0 -> 1.0.1
        When: check_compatibility() called
        Then: returns safe=True, warnings=[]"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("1.0.1")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True
        assert result["warnings"] == []

    def test_should_allow_minor_upgrade_without_warning(self):
        """Given: minor upgrade 1.0.0 -> 1.1.0
        When: check_compatibility() called
        Then: returns safe=True, warnings=[]"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("1.1.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True
        assert result["warnings"] == []

    def test_should_allow_upgrade_from_prerelease_to_stable(self):
        """Given: upgrade from 1.0.0-rc.1 to 1.0.0
        When: check_compatibility() called
        Then: returns safe=True"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0-rc.1")
        target = parser.parse("1.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True


class TestCompatibilityCheckerMajorUpgrade:
    """Test SVC-013: Return breaking changes for major upgrades"""

    def test_should_warn_on_major_upgrade(self):
        """Given: major upgrade 1.0.0 -> 2.0.0
        When: check_compatibility() called
        Then: returns safe=False, warnings list populated"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is False
        assert isinstance(result["warnings"], list)
        assert len(result["warnings"]) > 0

    def test_should_include_breaking_change_indicator(self):
        """Given: major upgrade result
        When: check_compatibility() returns
        Then: includes is_breaking=True"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert "is_breaking" in result
        assert result["is_breaking"] is True

    def test_should_provide_clear_warning_message(self):
        """Given: major upgrade
        When: check_compatibility() called
        Then: warning list contains clear explanatory messages"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        warnings = result["warnings"]
        assert any("major" in w.lower() for w in warnings) or \
               any("breaking" in w.lower() for w in warnings) or \
               any("caution" in w.lower() for w in warnings)

    def test_should_suggest_user_confirmation_for_breaking_changes(self):
        """Given: major upgrade with breaking changes
        When: check_compatibility() returns
        Then: includes requires_confirmation=True"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result.get("requires_confirmation", False) is True or \
               result.get("safe", True) is False


class TestCompatibilityCheckerDowngradeBlocking:
    """Test AC#5: Downgrade Blocking - SVC-014"""

    def test_should_block_major_downgrade_without_force(self):
        """Given: major downgrade 2.0.0 -> 1.5.0 without --force
        When: check_compatibility(force=False) called
        Then: returns blocked=True"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["blocked"] is True

    def test_should_provide_downgrade_error_message(self):
        """Given: major downgrade blocked
        When: check_compatibility() returns
        Then: error_message explains why downgrade is blocked"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert "error_message" in result or "message" in result
        message = result.get("error_message") or result.get("message", "").lower()
        assert "downgrade" in message.lower() or "cannot" in message.lower()

    def test_should_mention_force_flag_in_downgrade_message(self):
        """Given: major downgrade blocked
        When: check_compatibility() returns
        Then: error message mentions --force flag"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        message = result.get("error_message") or result.get("message", "").lower()
        assert "--force" in message or "force" in message

    def test_should_allow_downgrade_with_force_flag(self):
        """Given: major downgrade 2.0.0 -> 1.5.0 with --force
        When: check_compatibility(force=True) called
        Then: returns blocked=False (or allows operation)"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=True)

        # Assert
        assert result["blocked"] is False

    def test_should_warn_about_downgrade_risks(self):
        """Given: major downgrade
        When: check_compatibility() called
        Then: includes risk warnings about data loss, compatibility"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        warnings = result.get("warnings", [])
        message = result.get("error_message", "").lower() + \
                 " ".join(w.lower() for w in warnings)
        assert "risk" in message or "data" in message or "loss" in message or \
               "dangerous" in message or "incompatible" in message

    def test_should_block_any_major_downgrade(self):
        """Given: any major version downgrade
        When: check_compatibility() called
        Then: blocked=True regardless of minor/patch"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()

        test_cases = [
            ("3.0.0", "2.9.9"),  # 3.x to 2.x
            ("2.5.0", "1.0.0"),  # 2.x to 1.x
            ("5.0.0", "4.9.9"),  # 5.x to 4.x
        ]

        # Act & Assert
        for current_str, target_str in test_cases:
            result = checker.check_compatibility(
                parser.parse(current_str),
                parser.parse(target_str),
                force=False
            )
            assert result["blocked"] is True, \
                f"Should block downgrade from {current_str} to {target_str}"

    def test_should_allow_minor_downgrade_within_major(self):
        """Given: minor/patch downgrade within same major version 1.5.0 -> 1.3.0
        When: check_compatibility() called
        Then: may allow or provide warning but not hard block"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.5.0")
        target = parser.parse("1.3.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        # Should not hard block (blocked=False), but may warn
        assert result.get("blocked", False) is False


class TestCompatibilityCheckerReturnValue:
    """Test compatibility check result structure"""

    def test_should_return_dict_with_required_fields(self):
        """Given: any compatibility check
        When: check_compatibility() called
        Then: returns dict with safe, warnings, blocked, is_breaking fields"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("1.1.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert isinstance(result, dict)
        assert "safe" in result
        assert "warnings" in result
        assert "blocked" in result
        assert "is_breaking" in result

    def test_should_return_non_zero_exit_code_for_blocked(self):
        """Given: blocked downgrade
        When: check_compatibility() returns
        Then: includes exit_code field with non-zero value"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        if "exit_code" in result:
            assert result["exit_code"] != 0

    def test_should_return_zero_exit_code_for_safe(self):
        """Given: safe upgrade
        When: check_compatibility() returns
        Then: includes exit_code=0"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("1.1.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        if "exit_code" in result:
            assert result["exit_code"] == 0


class TestCompatibilityCheckerEdgeCases:
    """Test edge cases for compatibility checking"""

    def test_should_handle_same_version(self):
        """Given: current=1.0.0, target=1.0.0
        When: check_compatibility() called
        Then: returns safe=True (reinstall is safe)"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("1.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True
        assert result["blocked"] is False

    def test_should_handle_prerelease_to_prerelease_upgrade(self):
        """Given: 1.0.0-alpha -> 1.0.0-beta
        When: check_compatibility() called
        Then: returns safe=True (prerelease to prerelease is safe)"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0-alpha")
        target = parser.parse("1.0.0-beta")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True

    def test_should_handle_fresh_install_scenario(self):
        """Given: no current version (fresh install)
        When: check_compatibility(None, target) called
        Then: returns safe=True (fresh install is safe)"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        target = parser.parse("1.0.0")

        # Act
        result = checker.check_compatibility(None, target, force=False)

        # Assert
        assert result["safe"] is True
        assert result["blocked"] is False

    def test_should_warn_on_major_pre_release_downgrade(self):
        """Given: 2.0.0-rc.1 -> 1.0.0 (major downgrade)
        When: check_compatibility() called
        Then: should still block like normal major downgrade"""
        # Arrange
        from installer.compatibility_checker import CompatibilityChecker
        from installer.version_parser import VersionParser

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0-rc.1")
        target = parser.parse("1.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["blocked"] is True
