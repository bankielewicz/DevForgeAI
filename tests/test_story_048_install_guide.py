"""
Test Suite: STORY-048 AC-2 - INSTALL.md Comprehensive Guide

Tests validate that INSTALL.md exists and contains all required sections
with comprehensive installation documentation.
"""

import re
from pathlib import Path

import pytest


class TestInstallMdStructure:
    """Tests for INSTALL.md file structure and required sections."""

    @pytest.fixture
    def install_path(self):
        """Return path to INSTALL.md"""
        return Path("installer/INSTALL.md")

    @pytest.fixture
    def install_content(self, install_path):
        """Load INSTALL.md content"""
        if not install_path.exists():
            pytest.skip(f"INSTALL.md not found at {install_path}")
        return install_path.read_text()

    # AC-2 Required sections (10 total)

    def test_install_file_exists(self, install_path):
        """Test: File exists at installer/INSTALL.md"""
        # Assert
        assert install_path.exists(), \
            f"INSTALL.md must exist at {install_path}"

    def test_install_has_prerequisites_section(self, install_content):
        """Test: INSTALL.md contains Prerequisites section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+Prerequisite', install_content, re.IGNORECASE), \
            "INSTALL.md must have Prerequisites section"

    def test_install_has_modes_section(self, install_content):
        """Test: INSTALL.md contains Installation Modes section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Mm]ode', install_content, re.IGNORECASE), \
            "INSTALL.md must have Installation Modes section"

    def test_install_has_fresh_section(self, install_content):
        """Test: INSTALL.md contains Fresh Installation section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Ff]resh', install_content, re.IGNORECASE), \
            "INSTALL.md must have Fresh Installation section"

    def test_install_has_upgrade_section(self, install_content):
        """Test: INSTALL.md contains Upgrading section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Uu]pgrad', install_content, re.IGNORECASE), \
            "INSTALL.md must have Upgrading section"

    def test_install_has_rollback_section(self, install_content):
        """Test: INSTALL.md contains Rollback section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Rr]ollback', install_content, re.IGNORECASE), \
            "INSTALL.md must have Rollback section"

    def test_install_has_validation_section(self, install_content):
        """Test: INSTALL.md contains Validation section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Vv]alidat', install_content, re.IGNORECASE), \
            "INSTALL.md must have Validation section"

    def test_install_has_uninstall_section(self, install_content):
        """Test: INSTALL.md contains Uninstallation section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Uu]ninstall', install_content, re.IGNORECASE), \
            "INSTALL.md must have Uninstallation section"

    def test_install_has_troubleshooting_section(self, install_content):
        """Test: INSTALL.md contains Troubleshooting section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Tt]roubleshoot', install_content, re.IGNORECASE), \
            "INSTALL.md must have Troubleshooting section"

    def test_install_has_faq_section(self, install_content):
        """Test: INSTALL.md contains FAQ section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*FAQ|[Ff]requently [Aa]sked', install_content, re.IGNORECASE), \
            "INSTALL.md must have FAQ section"

    def test_install_has_support_section(self, install_content):
        """Test: INSTALL.md contains Support section"""
        # Act & Assert
        assert re.search(r'#{1,3}\s+.*[Ss]upport', install_content, re.IGNORECASE), \
            "INSTALL.md must have Support section"


class TestInstallMdTroubleshooting:
    """Tests for troubleshooting section completeness."""

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md content"""
        install_path = Path("installer/INSTALL.md")
        if not install_path.exists():
            pytest.skip(f"INSTALL.md not found")
        return install_path.read_text()

    def test_troubleshooting_section_exists(self, install_content):
        """Test: Troubleshooting section found"""
        # Act
        troubleshooting_match = re.search(
            r'#{1,3}\s+.*[Tt]roubleshoot.*?(?=#{1,3}|\Z)',
            install_content,
            re.DOTALL
        )

        # Assert
        assert troubleshooting_match, "Troubleshooting section not found"

    def test_troubleshooting_has_15_plus_scenarios(self, install_content):
        """Test: Troubleshooting section has 15+ scenarios"""
        # Arrange: Extract troubleshooting section
        troubleshooting_match = re.search(
            r'#{1,3}\s+.*[Tt]roubleshoot.*?(?=#{1,3}|\Z)',
            install_content,
            re.DOTALL
        )

        if not troubleshooting_match:
            pytest.skip("Troubleshooting section not found")

        troubleshooting_section = troubleshooting_match.group(0)

        # Act: Count issues (by looking for common patterns)
        # Count numbered items, bullet points, code blocks, or headers
        issue_count = 0
        issue_count += len(re.findall(r'^\s*\d+\.\s+', troubleshooting_section, re.MULTILINE))
        issue_count += len(re.findall(r'^\s*[-*+]\s+[A-Z]', troubleshooting_section, re.MULTILINE))
        issue_count += len(re.findall(r'####\s+', troubleshooting_section))

        # Assert: Must have at least 15 distinct issues
        assert issue_count >= 15, \
            f"Troubleshooting section must have 15+ scenarios (found {issue_count})"

    def test_troubleshooting_has_solutions(self, install_content):
        """Test: Troubleshooting scenarios include solutions"""
        # Arrange: Extract troubleshooting section
        troubleshooting_match = re.search(
            r'#{1,3}\s+.*[Tt]roubleshoot.*?(?=#{1,3}|\Z)',
            install_content,
            re.DOTALL
        )

        if not troubleshooting_match:
            pytest.skip("Troubleshooting section not found")

        troubleshooting_section = troubleshooting_match.group(0)

        # Act & Assert: Look for solution keywords
        assert re.search(r'[Ss]olution|[Ff]ix|[Rr]esolution|[Tt]ry', troubleshooting_section), \
            "Troubleshooting section should contain solutions/fixes"


class TestInstallMdFaq:
    """Tests for FAQ section completeness."""

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md content"""
        install_path = Path("installer/INSTALL.md")
        if not install_path.exists():
            pytest.skip(f"INSTALL.md not found")
        return install_path.read_text()

    def test_faq_section_exists(self, install_content):
        """Test: FAQ section found"""
        # Act
        faq_match = re.search(
            r'#{1,3}\s+.*(?:FAQ|[Ff]requently [Aa]sked).*?(?=#{1,3}|\Z)',
            install_content,
            re.DOTALL
        )

        # Assert
        assert faq_match, "FAQ section not found"

    def test_faq_has_10_plus_questions(self, install_content):
        """Test: FAQ section has 10+ Q&A pairs"""
        # Arrange: Extract FAQ section (from ## FAQ to next ## section)
        faq_match = re.search(
            r'##\s+FAQ[^\n]*\n(.*?)(?=\n##\s+|\Z)',
            install_content,
            re.DOTALL | re.IGNORECASE
        )

        if not faq_match:
            pytest.skip("FAQ section not found")

        faq_section = faq_match.group(1)  # Use group 1 (content after header)

        # Act: Count Q&A pairs
        # Look for questions marked with Q:, Qn:, or ####
        q_count = 0
        q_count += len(re.findall(r'\*\*Q(?:uestion)?[:\)]?\s*\*\*', faq_section, re.IGNORECASE))
        q_count += len(re.findall(r'#{4}\s+Q[A-Za-z\s:?]*\?', faq_section))
        q_count += len(re.findall(r'^\s*Q:\s+', faq_section, re.MULTILINE))
        # Also match **Q:** on its own line (STORY-048 format)
        q_count += len(re.findall(r'^\*\*Q:\*\*\s*$', faq_section, re.MULTILINE))

        # If no structured format, count question marks as approximation
        if q_count < 10:
            q_count = len(re.findall(r'\?\s*$', faq_section, re.MULTILINE))

        # Assert: Must have at least 10 questions
        assert q_count >= 10, \
            f"FAQ section must have 10+ Q&A pairs (found {q_count})"

    def test_faq_has_answers(self, install_content):
        """Test: FAQ questions have answers"""
        # Arrange: Extract FAQ section
        faq_match = re.search(
            r'#{1,3}\s+.*(?:FAQ|[Ff]requently [Aa]sked).*?(?=#{1,3}|\Z)',
            install_content,
            re.DOTALL
        )

        if not faq_match:
            pytest.skip("FAQ section not found")

        faq_section = faq_match.group(0)

        # Act & Assert: Look for answer keywords
        assert re.search(r'\*\*A(?:nswer)?[:\)]?\s*\*\*|^A:\s+', faq_section, re.MULTILINE | re.IGNORECASE), \
            "FAQ section should have answers to questions"


class TestInstallMdCommandAccuracy:
    """Tests for command examples accuracy and copy-paste ability."""

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md content"""
        install_path = Path("installer/INSTALL.md")
        if not install_path.exists():
            pytest.skip(f"INSTALL.md not found")
        return install_path.read_text()

    def test_install_examples_are_copyable(self, install_content):
        """Test: All command examples are copy-paste friendly"""
        # Arrange: Extract code blocks
        code_blocks = re.findall(
            r'```(?:bash|sh)?\s*\n(.*?)\n```',
            install_content,
            re.DOTALL
        )

        # Act: Check for valid syntax issues
        issues = []
        for i, block in enumerate(code_blocks):
            block = block.strip()

            # Check for unclosed quotes
            if block.count('"') % 2 != 0:
                issues.append(f"Block {i}: unmatched double quotes")
            if block.count("'") % 2 != 0:
                issues.append(f"Block {i}: unmatched single quotes")

            # Check for incomplete lines (ending with backslash but no next line)
            lines = block.split('\n')
            for j, line in enumerate(lines[:-1]):
                if line.rstrip().endswith('\\'):
                    next_line = lines[j + 1].strip()
                    if not next_line or next_line.startswith('#'):
                        issues.append(f"Block {i}, line {j}: continuation missing")

        # Assert
        assert len(issues) == 0, f"Command syntax issues: {issues}"

    def test_install_examples_dont_contain_placeholders_unexplained(self, install_content):
        """Test: Command examples explain any placeholders (like /path/to/)"""
        # Arrange: Extract commands with paths
        code_blocks = re.findall(
            r'```(?:bash|sh)?\s*\n(.*?)\n```',
            install_content,
            re.DOTALL
        )

        # Act: Check if placeholders are documented
        has_path_placeholder = False
        has_explanation = False

        for block in code_blocks:
            if '/path/to' in block or '<' in block or '[' in block:
                has_path_placeholder = True

        # Check if documentation explains placeholders
        if has_path_placeholder:
            has_explanation = re.search(
                r'replace|substitute|modify|your|path|project|directory',
                install_content,
                re.IGNORECASE
            )

        # Assert
        if has_path_placeholder:
            assert has_explanation, \
                "Placeholder paths should be documented with explanation"

    def test_install_mentions_required_installer_arguments(self, install_content):
        """Test: Documentation mentions key installer arguments"""
        # Act & Assert
        assert "--target" in install_content, "Should document --target argument"
        assert "--mode" in install_content, "Should document --mode argument"


class TestInstallMdIntegration:
    """Integration tests for INSTALL.md."""

    @pytest.fixture
    def install_content(self):
        """Load INSTALL.md content"""
        install_path = Path("installer/INSTALL.md")
        if not install_path.exists():
            pytest.skip(f"INSTALL.md not found")
        return install_path.read_text()

    def test_install_is_well_formed_markdown(self, install_content):
        """Test: INSTALL.md is well-formed markdown"""
        # Arrange: Count heading levels
        h1_count = len(re.findall(r'^#\s+', install_content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s+', install_content, re.MULTILINE))

        # Assert
        assert h1_count > 0, "INSTALL.md should have at least one H1"
        assert h2_count > 0, "INSTALL.md should have headings"

    def test_install_has_no_broken_links(self, install_content):
        """Test: INSTALL.md contains no obviously broken internal links"""
        # Arrange: Extract all links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', install_content)

        # Act: Check for common broken patterns
        broken = []
        for text, link in links:
            # Check for incomplete links
            if link.startswith('(') or link.endswith(')'):
                broken.append((text, link))
            # Check for placeholder links
            if link == '#' or link == 'TODO' or 'TODO' in link:
                broken.append((text, link))

        # Assert
        assert len(broken) == 0, f"Found broken links: {broken}"

    def test_install_content_substantial(self, install_content):
        """Test: INSTALL.md has substantial content"""
        # Assert
        assert len(install_content) > 2000, \
            "INSTALL.md should have substantial content (>2000 chars)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
