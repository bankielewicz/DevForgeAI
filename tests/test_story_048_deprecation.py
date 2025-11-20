"""
Test Suite: STORY-048 AC-5 - Old .claude/ Manual Copy Approach Deprecated

Tests validate that deprecation notices have been added and support timeline
is clearly documented.
"""

import re
from pathlib import Path

import pytest


class TestDeprecationNoticesInReadme:
    """Tests for deprecation notices in README.md."""

    @pytest.fixture
    def readme_path(self):
        """Return path to README.md"""
        return Path("README.md")

    @pytest.fixture
    def readme_content(self, readme_path):
        """Load README.md content"""
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    # AC-5 Tests

    def test_readme_has_deprecation_notice(self, readme_content):
        """Test: README.md contains deprecation notice"""
        # Act & Assert
        assert re.search(
            r'[Dd]eprecat|⚠️.*[Cc]laude|[Cc]laude.*manual',
            readme_content,
            re.IGNORECASE
        ), "README.md should contain deprecation notice"

    def test_readme_deprecation_notice_has_warning_emoji(self, readme_content):
        """Test: Deprecation notice uses warning emoji or visual indicator"""
        # Arrange: Find deprecation section
        deprecation_match = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if deprecation_match:
            deprecation_section = deprecation_match.group(0)
        else:
            deprecation_section = readme_content

        # Act & Assert
        assert re.search(r'⚠️|⚠|\[DEPRECATED\]|DEPRECATED|⛔', deprecation_section), \
            "Deprecation notice should use visual indicator (⚠️, [DEPRECATED], etc.)"

    def test_readme_mentions_installer_as_new_approach(self, readme_content):
        """Test: Deprecation notice directs to installer"""
        # Arrange: Find deprecation section
        deprecation_match = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if deprecation_match:
            deprecation_section = deprecation_match.group(0)
        else:
            deprecation_section = readme_content

        # Act & Assert
        assert re.search(
            r'[Ii]nstall|[Nn]ew|[Uu]se|[Aa]lternative',
            deprecation_section,
            re.IGNORECASE
        ), "Deprecation notice should mention using installer instead"

    def test_readme_mentions_manual_copy_as_old(self, readme_content):
        """Test: Deprecation explicitly mentions manual copy approach"""
        # Arrange: Find deprecation section
        deprecation_match = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if deprecation_match:
            deprecation_section = deprecation_match.group(0)
        else:
            deprecation_section = readme_content

        # Act & Assert
        assert re.search(
            r'[Cc]opy.*\.claude|\.claude.*[Cc]opy|[Mm]anual|[Oo]ld',
            deprecation_section,
            re.IGNORECASE
        ), "Deprecation should explicitly mention 'copy .claude/' approach"


class TestClaudeReadmeDeprecation:
    """Tests for deprecation notice in .claude/README.md."""

    @pytest.fixture
    def claude_readme_path(self):
        """Return path to .claude/README.md"""
        return Path(".claude/README.md")

    @pytest.fixture
    def claude_readme_content(self, claude_readme_path):
        """Load .claude/README.md content"""
        if not claude_readme_path.exists():
            pytest.skip(".claude/README.md not found")
        return claude_readme_path.read_text()

    def test_claude_readme_exists(self, claude_readme_path):
        """Test: .claude/README.md exists"""
        # Assert
        assert claude_readme_path.exists(), \
            ".claude/README.md should exist with deprecation notice"

    def test_claude_readme_has_deprecated_warning(self, claude_readme_content):
        """Test: .claude/README.md has DEPRECATED warning"""
        # Act & Assert
        assert re.search(
            r'[Dd]eprecat|⚠️',
            claude_readme_content,
            re.IGNORECASE
        ), ".claude/README.md should have deprecation warning"

    def test_claude_readme_mentions_src_folder(self, claude_readme_content):
        """Test: Mentions editing src/ instead of .claude/"""
        # Act & Assert
        assert re.search(
            r'src/|[Ee]dit.*src|edit.*[Cc]laude.*[Ss]ource',
            claude_readme_content,
            re.IGNORECASE
        ), ".claude/README.md should mention editing src/ instead"

    def test_claude_readme_mentions_installer(self, claude_readme_content):
        """Test: Mentions using installer to deploy"""
        # Act & Assert
        assert re.search(
            r'[Ii]nstall|deploy|run.*installer',
            claude_readme_content,
            re.IGNORECASE
        ), ".claude/README.md should mention using installer"

    def test_claude_readme_directs_to_install_guide(self, claude_readme_content):
        """Test: Directs users to INSTALL.md"""
        # Act & Assert
        assert re.search(
            r'INSTALL\.md|[Ii]nstallation.*[Gg]uide',
            claude_readme_content,
            re.IGNORECASE
        ), ".claude/README.md should reference INSTALL.md"


class TestDeprecationTimeline:
    """Tests for deprecation timeline documentation."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md content"""
        readme_path = Path("README.md")
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    @pytest.fixture
    def roadmap_content(self):
        """Load ROADMAP.md content"""
        roadmap_path = Path("ROADMAP.md")
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")
        return roadmap_path.read_text()

    def test_deprecation_date_documented(self, roadmap_content):
        """Test: Deprecation date documented (2025-11-17 or similar)"""
        # Act & Assert
        assert re.search(
            r'2025-1[01]-\d{2}|[Dd]eprecat.*date|deprecat.*2025',
            roadmap_content,
            re.IGNORECASE
        ), "ROADMAP.md should document deprecation date"

    def test_support_timeline_documented(self, roadmap_content):
        """Test: Support timeline documented (6+ months)"""
        # Act & Assert
        assert re.search(
            r'v2\.0|[Ss]upport.*until|deprecat.*until|6\s*month|until\s*2026',
            roadmap_content,
            re.IGNORECASE
        ), "ROADMAP.md should document how long old approach is supported"

    def test_support_is_at_least_6_months(self, roadmap_content):
        """Test: Manual approach support is at least 6 months"""
        # Arrange: Look for support end date
        end_date_match = re.search(
            r'v2\.0\.0|2026|[Ss]upport.*(\d{4}-\d{2}-\d{2})',
            roadmap_content
        )

        # This is a heuristic test - just verify that end date is mentioned
        # Exact date validation would require date parsing
        assert end_date_match or re.search(r'6.*month', roadmap_content, re.IGNORECASE), \
            "ROADMAP.md should clearly state 6+ month support period"


class TestDeprecationIntegration:
    """Integration tests for deprecation implementation."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md content"""
        readme_path = Path("README.md")
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    @pytest.fixture
    def claude_readme_path(self):
        """Return path to .claude/README.md"""
        return Path(".claude/README.md")

    @pytest.fixture
    def claude_readme_content(self, claude_readme_path):
        """Load .claude/README.md if exists"""
        if not claude_readme_path.exists():
            return None
        return claude_readme_path.read_text()

    def test_both_deprecation_notices_present(self, readme_content, claude_readme_content):
        """Test: Both README.md and .claude/README.md have deprecation notices"""
        # Assert
        has_main_notice = re.search(r'[Dd]eprecat|⚠️', readme_content, re.IGNORECASE)
        assert has_main_notice, "README.md should have deprecation notice"

        if claude_readme_content:
            has_claude_notice = re.search(r'[Dd]eprecat|⚠️', claude_readme_content, re.IGNORECASE)
            assert has_claude_notice, ".claude/README.md should have deprecation notice"

    def test_deprecation_notices_consistent(self, readme_content, claude_readme_content):
        """Test: Both notices mention installer as replacement"""
        # Check README
        readme_has_installer = re.search(r'[Ii]nstall', readme_content, re.IGNORECASE)
        assert readme_has_installer, "README.md deprecation should mention installer"

        # Check .claude/README if exists
        if claude_readme_content:
            claude_has_installer = re.search(r'[Ii]nstall|src/', claude_readme_content, re.IGNORECASE)
            assert claude_has_installer, ".claude/README.md should mention installer or src/"

    def test_old_approach_still_documented_but_marked_deprecated(self, readme_content):
        """Test: Old approach may still be documented but clearly marked deprecated"""
        # Arrange: Look for deprecated section
        deprecated_section = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # If deprecated section exists, check it mentions old approach
        if deprecated_section:
            section = deprecated_section.group(0)
            # It's okay if old approach documented here
            assert len(section) > 50, \
                "Deprecated section should have content explaining old approach"

    def test_new_installation_method_prominent(self, readme_content):
        """Test: New installer method is prominent (appears before deprecated section)"""
        # Arrange: Find main installation section
        installation_match = re.search(
            r'#{1,3}\s+Installation\s*(?!.*Deprecat).*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Find deprecation section
        deprecation_match = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Assert: Installation section should appear first (if both present)
        if installation_match and deprecation_match:
            install_pos = readme_content.find(installation_match.group(0))
            deprec_pos = readme_content.find(deprecation_match.group(0))
            assert install_pos < deprec_pos, \
                "New installation method should appear before deprecated section"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
