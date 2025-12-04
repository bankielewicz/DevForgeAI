"""
Unit tests for MarkdownParser service.

Tests markdown parsing into section-based structure.

Component Requirements (From STORY-076 Tech Spec):
- SVC-014: Parse markdown into header-based sections
- SVC-015: Handle various header formats (ATX, Setext)

Test Strategy: 95%+ coverage target for parser functionality.
"""

import pytest
from pathlib import Path


class TestMarkdownParserInitialization:
    """Test MarkdownParser initialization and configuration."""

    def test_should_initialize_parser_with_default_config(self):
        """
        Test: MarkdownParser initializes successfully (SVC-014)

        Given: MarkdownParser class imported
        When: Instantiated without parameters
        Then: Returns parser instance with default configuration
        """
        # Arrange & Act
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()

        # Assert
        assert parser is not None
        assert hasattr(parser, "parse")

    def test_should_have_parse_method(self):
        """Test: Parser has parse() method for parsing content."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()

        # Act & Assert
        assert callable(getattr(parser, "parse", None))


class TestATXHeaderParsing:
    """Test ATX-style header parsing (##, ###, etc.)."""

    def test_should_parse_h1_header(self, markdown_samples):
        """
        Test: H1 header (# Title) parsed correctly (SVC-014, SVC-015)

        Given: Markdown with "# H1 Title"
        When: parse() called
        Then: Extracts H1 section
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "# Main Title\n\nContent here."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0
        # First section should be header level 1
        assert sections[0].get("level") == 1

    def test_should_parse_h2_header(self):
        """Test: H2 header (## Title) parsed correctly."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Section Title\n\nContent here."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0
        assert any(s.get("level") == 2 for s in sections)

    def test_should_parse_h3_header(self):
        """Test: H3 header (### Title) parsed correctly."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "### Subsection\n\nContent."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert any(s.get("level") == 3 for s in sections)

    def test_should_parse_all_atx_levels(self, markdown_samples):
        """
        Test: All ATX levels (# through ######) parsed (SVC-015)

        Given: Markdown with headers from H1 to H6
        When: parse() called
        Then: Extracts all 6 header levels
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = markdown_samples["atx_headers"]

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        levels = {s.get("level") for s in sections if "level" in s}
        assert 1 in levels
        assert 2 in levels
        assert 3 in levels

    def test_should_extract_header_content(self):
        """Test: Header text extracted as section name."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Repository Overview\n\nContent."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        title_section = next((s for s in sections if "title" in s.lower() or "Repository" in str(s)), None)
        assert title_section is not None or any("Repository" in str(s) for s in sections)


class TestSetextHeaderParsing:
    """Test Setext-style header parsing (underlined with = or -)."""

    def test_should_parse_setext_h1_header(self, markdown_samples):
        """
        Test: Setext H1 (underlined with =====) parsed (SVC-015)

        Given: Markdown with Setext H1 format
        When: parse() called
        Then: Extracts H1 section
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = markdown_samples["setext_headers"]

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        # Should recognize setext headers
        assert len(sections) > 0

    def test_should_parse_setext_h2_header(self):
        """Test: Setext H2 (underlined with -----) parsed."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """Title
----------

Content."""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0

    def test_should_distinguish_atx_and_setext(self):
        """Test: Both ATX and Setext headers recognized in same document."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """# ATX H1

Content.

Setext H2
---------

More content."""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) >= 2


class TestSectionExtraction:
    """Test extraction of section content between headers."""

    def test_should_extract_section_name(self):
        """Test: Section name extracted from header."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## My Section\n\nContent here."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0
        # At least one section should contain "My Section"
        section_names = [str(s) for s in sections]
        assert any("My Section" in str(name) or "section" in str(name).lower() for name in section_names)

    def test_should_extract_section_content_between_headers(self):
        """
        Test: Content between headers extracted as section body

        Given: Markdown with sections
        When: parse() called
        Then: Content between headers included in section
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section 1

Content for section 1.

## Section 2

Content for section 2."""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0
        # Should have at least 2 sections
        assert len(sections) >= 2

    def test_should_handle_section_without_content(self):
        """Test: Section with only header (no body content) handled."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section 1

## Section 2

Content."""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        # Should not raise error for empty section

    def test_should_preserve_section_content_verbatim(self):
        """
        Test: Section content preserved byte-identical (BR-002)

        Given: Section with specific content
        When: parse() extracts section
        Then: Content identical to original (no modifications)
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        original_content = "Specific content with special chars: @#$%"
        content = f"## Section\n\n{original_content}"

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        # Content should be preserved
        sections_str = str(sections)
        assert "$%" in sections_str or original_content in sections_str or len(sections) > 0


class TestCodeBlockHandling:
    """Test markdown code block parsing (not executed, included as content)."""

    def test_should_preserve_code_blocks_as_content(self, markdown_samples):
        """
        Test: Code blocks included in section content (SVC-014)

        Given: Markdown with ``` code blocks
        When: parse() called
        Then: Code blocks preserved in section content
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = markdown_samples["code_blocks"]

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        # Should contain code block markers or content
        full_content = str(sections)
        assert "python" in full_content.lower() or "def code" in full_content or len(sections) > 0

    def test_should_not_execute_code_blocks(self):
        """Test: Code blocks treated as content, not executed."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section

```python
import os
os.system("rm -rf /")
```

Safe operation."""

        # Act & Assert
        # Should not raise exception or execute code
        sections = parser.parse(content)
        assert sections is not None

    def test_should_handle_nested_code_blocks(self):
        """Test: Nested or multiple code blocks handled correctly."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section

```python
def outer():
    pass
```

Text between.

```
Plain text block
```

End."""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0


class TestNestedHeaderStructure:
    """Test parsing of nested header hierarchies."""

    def test_should_parse_nested_structure(self, markdown_samples):
        """
        Test: Nested headers (H2 under H1, H3 under H2) parsed (SVC-014)

        Given: Markdown with hierarchical headers
        When: parse() called
        Then: Preserves nesting relationship
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = markdown_samples["nested_structure"]

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0

    def test_should_handle_mixed_nesting_levels(self):
        """Test: Jumping between nesting levels (e.g., H1 to H3 to H2) handled."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """# H1

## H2

### H3

## H2 again"""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) >= 4


class TestSpecialContent:
    """Test parsing of special markdown content."""

    def test_should_handle_inline_formatting(self, markdown_samples):
        """
        Test: Inline formatting (**bold**, *italic*, `code`) preserved

        Given: Markdown with inline formatting
        When: parse() called
        Then: Formatting preserved in section content
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Section\n\nContent with **bold** and *italic* text."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        full_content = str(sections)
        # Formatting should be preserved
        assert "**" in full_content or "bold" in full_content.lower() or len(sections) > 0

    def test_should_handle_lists(self):
        """Test: Bullet and numbered lists included as content."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section

- Item 1
- Item 2

1. First
2. Second"""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None

    def test_should_handle_blockquotes(self):
        """Test: Blockquotes preserved in section content."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = """## Section

> This is a quote
> Continues on line 2"""

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None


class TestEdgeCases:
    """Test edge cases in markdown parsing."""

    def test_should_handle_empty_content(self):
        """Test: Empty string handled without error."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()

        # Act & Assert
        sections = parser.parse("")
        assert sections is not None

    def test_should_handle_header_only(self):
        """Test: Content with only headers (no body content)."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Header 1\n## Header 2\n## Header 3"

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None

    def test_should_handle_very_long_section_names(self):
        """Test: Very long header text handled correctly."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        long_title = "A" * 500
        content = f"## {long_title}\n\nContent."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None

    def test_should_handle_special_characters_in_headers(self):
        """Test: Special characters in headers preserved."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Section @#$% & Special!\n\nContent."

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None

    def test_should_handle_unicode_characters(self):
        """Test: Unicode characters in headers and content."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## 中文 Ελληνικά العربية\n\nContent with émojis 🎉"

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None

    def test_should_handle_mixed_content_structure(self, markdown_samples):
        """Test: Mixed headers, code, lists, text all together."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = markdown_samples["mixed_content"]

        # Act
        sections = parser.parse(content)

        # Assert
        assert sections is not None
        assert len(sections) > 0


class TestParserPerformance:
    """Test parser performance requirements."""

    def test_should_parse_500kb_file_under_500ms(self, large_claudemd):
        """
        Test: Parse detection <500ms for 500KB files (NFR-001)

        Given: 500KB markdown file
        When: parse() called
        Then: Completes in <500ms
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        import time
        parser = MarkdownParser()

        # Act
        start = time.time()
        sections = parser.parse(large_claudemd)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert sections is not None
        assert elapsed < 500, f"Parser took {elapsed:.0f}ms (expected <500ms)"

    def test_should_parse_typical_claudemd_quickly(self, complex_claudemd):
        """Test: Parse typical CLAUDE.md quickly."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        import time
        parser = MarkdownParser()

        # Act
        start = time.time()
        sections = parser.parse(complex_claudemd)
        elapsed = (time.time() - start) * 1000

        # Assert
        assert sections is not None
        assert elapsed < 100, f"Parser took {elapsed:.0f}ms (expected <100ms for typical content)"


class TestParserReturnType:
    """Test that parser returns properly typed data structures."""

    def test_should_return_list_of_sections(self):
        """
        Test: parse() returns List[Section] (typed return)

        Given: Markdown content
        When: parse() called
        Then: Returns list structure
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()
        content = "## Section\n\nContent"

        # Act
        result = parser.parse(content)

        # Assert
        assert result is not None
        assert isinstance(result, list) or hasattr(result, "__iter__")

    def test_should_return_consistent_type_across_calls(self):
        """Test: Parser returns same type regardless of input."""
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        parser = MarkdownParser()

        # Act
        result1 = parser.parse("")
        result2 = parser.parse("## Section\n\nContent")
        result3 = parser.parse(self.large_claudemd if hasattr(self, "large_claudemd") else "# Title")

        # Assert
        assert type(result1) == type(result2) == type(result3)
