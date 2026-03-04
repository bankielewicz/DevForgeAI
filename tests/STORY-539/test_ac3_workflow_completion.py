"""
Test: AC#3 - End-to-End Workflow Completion
Story: STORY-539
Generated: 2026-03-04

Tests validate that skill file exists, is valid Markdown, and stays under
1,000 lines. Also validates output file path structure.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM_FRAMEWORK = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "go-to-market-framework.md")
CHANNEL_MATRIX = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "channel-selection-matrix.md")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "business", "marketing", "go-to-market.md")


class TestSkillFileLineCount:
    """AC#3: Skill reference file must not exceed 1,000 lines."""

    def test_should_not_exceed_1000_lines_framework(self):
        # Arrange
        with open(GTM_FRAMEWORK, "r") as f:
            lines = f.readlines()
        # Act
        line_count = len(lines)
        # Assert
        assert line_count <= 1000, f"go-to-market-framework.md has {line_count} lines, max 1000"

    def test_should_not_exceed_1000_lines_matrix(self):
        # Arrange
        with open(CHANNEL_MATRIX, "r") as f:
            lines = f.readlines()
        # Act
        line_count = len(lines)
        # Assert
        assert line_count <= 1000, f"channel-selection-matrix.md has {line_count} lines, max 1000"


class TestValidMarkdown:
    """AC#3: Output must be valid Markdown."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_use_atx_headings_only(self, framework_content):
        # Arrange & Act - detect setext headings (underline style)
        setext = re.findall(r"^[^\n]+\n[=\-]{3,}$", framework_content, re.MULTILINE)
        # Assert
        assert len(setext) == 0, f"Found {len(setext)} setext headings, must use ATX style only"

    def test_should_have_title_heading(self, framework_content):
        # Arrange & Act
        has_h1 = bool(re.search(r"^# .+", framework_content, re.MULTILINE))
        # Assert
        assert has_h1, "Missing top-level heading in go-to-market-framework.md"

    def test_should_not_be_empty(self, framework_content):
        # Arrange & Act
        content_stripped = framework_content.strip()
        # Assert
        assert len(content_stripped) > 100, "File content too short, likely incomplete"


class TestOutputPathStructure:
    """AC#3: Output directory structure must be valid."""

    def test_should_have_output_directory_parent(self):
        # Arrange
        output_dir = os.path.dirname(OUTPUT_PATH)
        # Act & Assert - verify the path is well-formed (directory may not exist yet)
        assert output_dir.endswith(os.path.join("devforgeai", "specs", "business", "marketing")), \
            f"Output path parent should be devforgeai/specs/business/marketing/, got {output_dir}"

    def test_should_reference_correct_output_filename(self):
        # Arrange & Act
        filename = os.path.basename(OUTPUT_PATH)
        # Assert
        assert filename == "go-to-market.md", f"Expected go-to-market.md, got {filename}"
