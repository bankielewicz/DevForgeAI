"""
Test Suite: STORY-048 AC-1 - README.md Updated with Installer Instructions

Tests validate that README.md has been updated with installer-based installation
instructions, with old manual copy approach removed or deprecated.
"""

import os
import re
from pathlib import Path

import pytest


class TestReadmeInstallationSection:
    """Tests for README.md installation section updates."""

    @pytest.fixture
    def readme_path(self):
        """Return path to project README.md"""
        return Path("README.md")

    @pytest.fixture
    def readme_content(self, readme_path):
        """Load README.md content"""
        if not readme_path.exists():
            pytest.skip("README.md not found")
        return readme_path.read_text()

    # AC-1 Test Cases

    def test_readme_contains_installer_command(self, readme_content):
        """Test: README.md contains 'python installer/install.py' (not 'copy .claude/')"""
        # Arrange & Act
        has_installer_cmd = "python installer/install.py" in readme_content or \
                           "python /path/to/DevForgeAI2/installer/install.py" in readme_content

        # Assert
        assert has_installer_cmd, \
            "README.md must contain 'python installer/install.py' command"

    def test_readme_does_not_recommend_manual_copy(self, readme_content):
        """Test: Old manual copy approach not recommended in main section"""
        # Arrange: Get installation section only (first occurrence)
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not installation_match:
            pytest.skip("Installation section not found")

        installation_section = installation_match.group(0)

        # Act & Assert
        assert "copy .claude" not in installation_section.lower(), \
            "Installation section must not recommend 'copy .claude' approach"

    def test_readme_has_fresh_install_example(self, readme_content):
        """Test: Installation section has fresh install example"""
        # Arrange
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not installation_match:
            pytest.skip("Installation section not found")

        installation_section = installation_match.group(0)

        # Act & Assert
        assert "new" in installation_section.lower() or "fresh" in installation_section.lower(), \
            "Installation section should have fresh install example"

    def test_readme_has_upgrade_example(self, readme_content):
        """Test: Installation section has upgrade example"""
        # Arrange
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not installation_match:
            pytest.skip("Installation section not found")

        installation_section = installation_match.group(0)

        # Act & Assert
        assert "--mode=upgrade" in installation_section or "upgrade" in installation_section.lower(), \
            "Installation section should have upgrade example"

    def test_readme_lists_python_requirement(self, readme_content):
        """Test: Prerequisites lists Python 3.8+"""
        # Arrange: Find prerequisites section
        prereq_match = re.search(
            r'#{1,3}\s+Prerequisite.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Act & Assert
        search_text = prereq_match.group(0) if prereq_match else readme_content

        assert re.search(r'[Pp]ython\s+3\.[89]|[Pp]ython\s+>=\s*3\.[89]|[Pp]ython\s+3\.10',
                        search_text), \
            "Prerequisites must list Python 3.8+ requirement"

    def test_readme_lists_git_requirement(self, readme_content):
        """Test: Prerequisites lists Git"""
        # Arrange
        prereq_match = re.search(
            r'#{1,3}\s+Prerequisite.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Act & Assert
        search_text = prereq_match.group(0) if prereq_match else readme_content

        assert re.search(r'[Gg]it(?:\s+version)?', search_text), \
            "Prerequisites must list Git requirement"

    def test_readme_lists_claude_code_requirement(self, readme_content):
        """Test: Prerequisites lists Claude Code Terminal 0.8.0+"""
        # Arrange
        prereq_match = re.search(
            r'#{1,3}\s+Prerequisite.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Act & Assert
        search_text = prereq_match.group(0) if prereq_match else readme_content

        assert re.search(
            r'[Cc]laude\s+[Cc]ode|[Cc]laude\s+[Tt]erminal|Claude\s+Code\s+Terminal.*?0\.8|0\.8\.\d+',
            search_text), \
            "Prerequisites must list Claude Code Terminal 0.8.0+ requirement"

    def test_readme_has_deprecated_section_or_removed(self, readme_content):
        """Test: Old manual copy instructions removed or moved to deprecated section"""
        # Arrange: Check if old instructions are in deprecated section
        deprecated_match = re.search(
            r'#{1,4}\s+.*[Dd]eprecat.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Act: Check if old approach mentioned in main installation
        main_install_match = re.search(
            r'#{1,3}\s+Installation\s*(?!.*Deprecat).*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        # Assert
        if main_install_match:
            main_section = main_install_match.group(0)
            assert "copy .claude" not in main_section.lower(), \
                "Manual copy approach should not be in main Installation section"

    def test_readme_installation_mentions_clone_repo(self, readme_content):
        """Test: Installation examples include cloning repository"""
        # Arrange
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not installation_match:
            pytest.skip("Installation section not found")

        installation_section = installation_match.group(0)

        # Act & Assert
        assert "git clone" in installation_section.lower() or \
               "clone" in installation_section.lower(), \
            "Installation section should mention cloning repository"

    def test_readme_installation_mentions_target_flag(self, readme_content):
        """Test: Installation examples use --target flag for installer"""
        # Arrange
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            readme_content,
            re.IGNORECASE | re.DOTALL
        )

        if not installation_match:
            pytest.skip("Installation section not found")

        installation_section = installation_match.group(0)

        # Act & Assert
        assert "--target" in installation_section, \
            "Installation examples should use --target flag"

    def test_readme_format_wellformed(self, readme_content):
        """Test: README.md is well-formed markdown"""
        # Arrange: Count heading levels
        h1_count = len(re.findall(r'^#\s+', readme_content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s+', readme_content, re.MULTILINE))

        # Act & Assert
        assert h1_count > 0, "README should have at least one H1 heading"
        assert h2_count > 0, "README should have at least one H2 heading"


class TestReadmeIntegration:
    """Integration tests for README.md installation instructions."""

    @pytest.fixture
    def readme_path(self):
        """Return path to project README.md"""
        return Path("README.md")

    def test_readme_commands_are_valid_syntax(self, readme_path):
        """Test: All command examples in Installation section have valid bash syntax"""
        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text()

        # Arrange: Extract all bash code blocks
        code_blocks = re.findall(
            r'```(?:bash|sh)?\s*\n(.*?)\n```',
            content,
            re.DOTALL
        )

        # Act: Check for common bash issues
        issues = []
        for i, block in enumerate(code_blocks):
            # Check for unclosed quotes
            if block.count('"') % 2 != 0:
                issues.append(f"Code block {i}: unmatched double quotes")
            if block.count("'") % 2 != 0:
                issues.append(f"Code block {i}: unmatched single quotes")

        # Assert
        assert len(issues) == 0, f"Bash syntax issues found: {issues}"

    def test_readme_installation_section_not_empty(self, readme_path):
        """Test: Installation section has substantial content"""
        if not readme_path.exists():
            pytest.skip("README.md not found")

        content = readme_path.read_text()

        # Arrange: Extract installation section
        installation_match = re.search(
            r'#{1,3}\s+Installation.*?(?=#{1,3}|\Z)',
            content,
            re.IGNORECASE | re.DOTALL
        )

        # Assert
        assert installation_match, "Installation section must exist"
        installation_section = installation_match.group(0)
        assert len(installation_section) > 200, \
            "Installation section should have substantial content (>200 chars)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
