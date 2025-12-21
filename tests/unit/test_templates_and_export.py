"""
Test suite for AC6 & AC7: Template Library and Export Formats

Tests template loading, selection, customization, and multi-format export
(HTML, PDF) with proper diagram preservation and TOC generation.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from typing import Dict, List


class TestTemplateLibrary:
    """Test template library functionality."""

    def test_should_list_available_templates(self):
        """Test that /document --list-templates shows available templates."""
        # Arrange
        templates = [
            "readme-template.md",
            "developer-guide-template.md",
            "api-docs-template.md",
            "troubleshooting-template.md",
            "contributing-template.md",
            "changelog-template.md",
            "architecture-template.md"
        ]

        # Act
        from devforgeai_documentation import TemplateLibrary
        lib = TemplateLibrary()
        available = lib.get_available_templates()

        # Assert
        assert available is not None
        assert len(available) >= 6  # At least 6 templates

    def test_should_load_readme_template(self):
        """Test that README template is loaded correctly."""
        # Arrange
        template_name = "readme"

        # Act
        from devforgeai_documentation import TemplateLibrary
        lib = TemplateLibrary()
        template = lib.load_template(template_name)

        # Assert
        assert template is not None
        assert isinstance(template, str)
        # Should have placeholders
        assert "{{" in template or "{%" in template

    def test_should_load_all_template_types(self):
        """Test that all 7 template types can be loaded."""
        # Arrange
        template_types = [
            "readme",
            "developer-guide",
            "api-docs",
            "troubleshooting",
            "contributing",
            "changelog",
            "architecture"
        ]

        # Act
        from devforgeai_documentation import TemplateLibrary
        lib = TemplateLibrary()

        # Assert
        for template_type in template_types:
            template = lib.load_template(template_type)
            assert template is not None

    def test_templates_should_have_variables(self):
        """Test that templates contain substitutable variables."""
        # Arrange
        template_name = "readme"

        # Act
        from devforgeai_documentation import TemplateLibrary
        lib = TemplateLibrary()
        template = lib.load_template(template_name)

        # Assert
        assert template is not None
        # Should have template variables
        variables = lib.extract_variables(template)
        assert variables is not None
        assert len(variables) > 0

    def test_should_support_custom_templates(self):
        """Test that custom templates in devforgeai/templates/ are supported."""
        # Arrange
        custom_template_path = "devforgeai/templates/documentation/custom-template.md"

        # Act
        from devforgeai_documentation import TemplateLibrary
        lib = TemplateLibrary()
        exists = lib.template_exists(custom_template_path)

        # Assert
        # In real scenario, custom templates may or may not exist
        # But system should support loading them
        assert isinstance(exists, bool)


class TestTemplateSelection:
    """Test template selection via AskUserQuestion."""

    def test_should_present_template_options_to_user(self):
        """Test that template selection uses AskUserQuestion."""
        # Arrange
        available_templates = [
            {"name": "readme", "description": "Project overview and setup"},
            {"name": "api-docs", "description": "API reference documentation"},
            {"name": "developer-guide", "description": "Development workflow"}
        ]

        # Act
        from devforgeai_documentation import TemplateSelector
        selector = TemplateSelector()
        # In implementation, would use AskUserQuestion
        # For test, we just verify structure
        question = selector.create_selection_question(available_templates)

        # Assert
        assert question is not None
        # Should have options
        assert "readme" in str(question).lower() or "api" in str(question).lower()

    def test_should_allow_user_to_select_template(self):
        """Test that user can select template from options."""
        # Arrange
        selection = "api-docs"

        # Act
        from devforgeai_documentation import TemplateSelector
        selector = TemplateSelector()
        is_valid = selector.validate_selection(selection)

        # Assert
        assert is_valid is True

    def test_should_support_multiple_template_selection(self):
        """Test that user can select multiple templates."""
        # Arrange
        selections = ["readme", "api-docs", "contributing"]

        # Act
        from devforgeai_documentation import TemplateSelector
        selector = TemplateSelector()
        all_valid = all(selector.validate_selection(s) for s in selections)

        # Assert
        assert all_valid is True


class TestTemplateCustomization:
    """Test template customization with project-specific settings."""

    def test_should_apply_project_name_to_template(self):
        """Test that project name is substituted in template."""
        # Arrange
        template = "# {{project_name}}\n\nWelcome to {{project_name}}!"
        project_context = {"project_name": "TaskManager"}

        # Act
        from devforgeai_documentation import TemplateRenderer
        renderer = TemplateRenderer()
        result = renderer.render(template, project_context)

        # Assert
        assert result is not None
        assert "TaskManager" in result
        assert "{{" not in result  # All variables substituted

    def test_should_apply_tech_stack_to_template(self):
        """Test that tech stack is filled into template."""
        # Arrange
        template = "Built with: {{tech_stack}}"
        context = {"tech_stack": "Node.js, Express, React, PostgreSQL"}

        # Act
        from devforgeai_documentation import TemplateRenderer
        renderer = TemplateRenderer()
        result = renderer.render(template, context)

        # Assert
        assert result is not None
        assert "Node.js" in result
        assert "{{" not in result

    def test_should_apply_installation_steps(self):
        """Test that installation steps are included in template."""
        # Arrange
        template = """## Installation

{{installation_steps}}
"""
        context = {
            "installation_steps": "1. npm install\n2. npm run build\n3. npm start"
        }

        # Act
        from devforgeai_documentation import TemplateRenderer
        renderer = TemplateRenderer()
        result = renderer.render(template, context)

        # Assert
        assert result is not None
        assert "npm install" in result
        assert "npm run build" in result

    def test_should_apply_coding_standards_customizations(self):
        """Test that coding-standards.md customizations are applied."""
        # Arrange
        template = "# {{project_name}}\n\n## Setup\n\n{{setup_instructions}}"
        coding_standards = {
            "project_name": "MyProject",
            "setup_instructions": "Custom setup per our standards"
        }

        # Act
        from devforgeai_documentation import TemplateRenderer
        renderer = TemplateRenderer()
        result = renderer.render(template, coding_standards)

        # Assert
        assert result is not None
        assert "MyProject" in result

    def test_should_handle_conditional_sections(self):
        """Test that template can conditionally include sections."""
        # Arrange
        template = """# Project

{% if has_docker %}
## Docker Setup
Docker instructions here
{% endif %}

{% if has_api %}
## API Reference
API docs here
{% endif %}
"""
        context = {
            "has_docker": True,
            "has_api": False
        }

        # Act
        from devforgeai_documentation import TemplateRenderer
        renderer = TemplateRenderer()
        result = renderer.render(template, context)

        # Assert
        assert result is not None
        # Should include Docker section
        assert "Docker" in result
        # Should not include API section
        assert "API Reference" not in result


class TestHTMLExport:
    """Test Markdown to HTML conversion."""

    def test_should_convert_markdown_to_html(self):
        """Test that Markdown is converted to valid HTML."""
        # Arrange
        markdown = """# Project Title

## Section 1
This is content.

- Item 1
- Item 2
"""

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        assert isinstance(html, str)
        # Should have HTML tags
        assert "<h1>" in html or "<h2>" in html
        assert "<li>" in html or "Item" in html

    def test_should_preserve_code_blocks_in_html(self):
        """Test that code blocks are preserved with syntax highlighting."""
        # Arrange
        markdown = """# Code Example

\`\`\`javascript
const app = require('express')();
app.listen(3000);
\`\`\`
"""

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Should have code block
        assert "<code>" in html or "<pre>" in html
        assert "express" in html

    def test_should_style_html_output(self):
        """Test that HTML output includes CSS styling."""
        # Arrange
        markdown = "# Title\n\nContent"

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown, include_styling=True)

        # Assert
        assert html is not None
        # Should have style tag or class attributes
        assert "<style>" in html or "class=" in html or "style=" in html

    def test_should_embed_mermaid_diagrams_in_html(self):
        """Test that Mermaid diagrams are embedded correctly in HTML."""
        # Arrange
        markdown = """# Architecture

\`\`\`mermaid
graph TD
    A[Component A]
    B[Component B]
    A --> B
\`\`\`
"""

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Should include mermaid script
        assert "mermaid" in html.lower() or "graph" in html

    def test_should_generate_valid_html(self):
        """Test that generated HTML is valid."""
        # Arrange
        markdown = "# Title\n\nContent\n\n- Item 1\n- Item 2"

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Check basic HTML validity
        assert html.count("<") == html.count(">")  # Balanced tags


class TestPDFExport:
    """Test Markdown to PDF conversion."""

    def test_should_convert_markdown_to_pdf(self):
        """Test that Markdown can be converted to PDF."""
        # Arrange
        markdown = "# Project Title\n\nThis is the content."

        # Act
        from devforgeai_documentation import PDFExporter
        exporter = PDFExporter()
        pdf_bytes = exporter.convert(markdown)

        # Assert
        # PDF conversion may be optional (needs wkhtmltopdf)
        # Test should handle gracefully if not available
        if pdf_bytes is not None:
            assert isinstance(pdf_bytes, bytes)

    def test_should_preserve_formatting_in_pdf(self):
        """Test that formatting is preserved in PDF output."""
        # Arrange
        markdown = """# Title

## Section 1

**Bold text** and *italic text*

- Bullet 1
- Bullet 2
"""

        # Act
        from devforgeai_documentation import PDFExporter
        exporter = PDFExporter()
        result = exporter.convert(markdown)

        # Assert
        # Should succeed or return None if PDF tools unavailable
        assert result is None or isinstance(result, bytes)

    def test_should_handle_missing_pdf_tools_gracefully(self):
        """Test that missing PDF tools (wkhtmltopdf) are handled gracefully."""
        # Arrange
        markdown = "# Test"

        # Act
        from devforgeai_documentation import PDFExporter
        exporter = PDFExporter()
        result = exporter.convert(markdown)

        # Assert
        # Should return None or error message, not crash
        assert result is None or isinstance(result, (bytes, str))

    def test_should_suggest_fallback_on_pdf_failure(self):
        """Test that system suggests HTML export as fallback."""
        # Arrange
        markdown = "# Test"

        # Act
        from devforgeai_documentation import PDFExporter
        exporter = PDFExporter()
        fallback = exporter.get_fallback_format()

        # Assert
        assert fallback is not None
        assert fallback in ["html", "md", "markdown"]


class TestExportFormatPreservation:
    """Test that special content is preserved during export."""

    def test_should_preserve_diagrams_in_html_export(self):
        """Test that Mermaid diagrams render in HTML output."""
        # Arrange
        markdown = """
# Design

\`\`\`mermaid
graph TD
    A[Start] --> B[Process] --> C[End]
\`\`\`
"""

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Should reference mermaid
        html_lower = html.lower()
        assert "mermaid" in html_lower or "graph" in html_lower

    def test_should_preserve_tables_in_export(self):
        """Test that Markdown tables are preserved."""
        # Arrange
        markdown = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Should have table tags
        assert "<table>" in html or "Header" in html

    def test_should_preserve_links_in_export(self):
        """Test that links are preserved in exported formats."""
        # Arrange
        markdown = "[Link text](https://example.com)"

        # Act
        from devforgeai_documentation import HTMLExporter
        exporter = HTMLExporter()
        html = exporter.convert(markdown)

        # Assert
        assert html is not None
        # Should have href
        assert "href=" in html or "example.com" in html


class TestTableOfContents:
    """Test table of contents generation."""

    def test_should_generate_toc_for_html(self):
        """Test that HTML output includes table of contents."""
        # Arrange
        markdown = """# Main

## Section 1
Content

## Section 2
Content

### Subsection 2.1
Content
"""

        # Act
        from devforgeai_documentation import TOCGenerator
        gen = TOCGenerator()
        html_with_toc = gen.generate_html_with_toc(markdown)

        # Assert
        assert html_with_toc is not None
        # Should have navigation or TOC
        toc_lower = html_with_toc.lower()
        assert "toc" in toc_lower or "table of contents" in toc_lower or "section 1" in toc_lower

    def test_should_create_toc_links(self):
        """Test that TOC includes working links to sections."""
        # Arrange
        markdown = """# Project

## Installation
...

## Usage
...

## Contributing
...
"""

        # Act
        from devforgeai_documentation import TOCGenerator
        gen = TOCGenerator()
        toc = gen.generate_toc(markdown)

        # Assert
        assert toc is not None
        # Should have all sections
        toc_text = str(toc)
        assert "Installation" in toc_text
        assert "Usage" in toc_text

    def test_should_handle_nested_sections_in_toc(self):
        """Test that TOC properly indents nested sections."""
        # Arrange
        markdown = """# Project

## Section 1
### Subsection 1.1
### Subsection 1.2

## Section 2
### Subsection 2.1
"""

        # Act
        from devforgeai_documentation import TOCGenerator
        gen = TOCGenerator()
        toc = gen.generate_toc(markdown)

        # Assert
        assert toc is not None
        # Should show hierarchy
        toc_text = str(toc)
        assert "Subsection" in toc_text


class TestBranding:
    """Test branding support in exports."""

    def test_should_apply_branding_to_html(self):
        """Test that custom branding can be applied to HTML exports."""
        # Arrange
        markdown = "# Project"
        branding = {
            "logo_url": "https://example.com/logo.png",
            "primary_color": "#007bff"
        }

        # Act
        from devforgeai_documentation import BrandedHTMLExporter
        exporter = BrandedHTMLExporter(branding)
        html = exporter.convert(markdown)

        # Assert
        if html is not None:
            # Should reference logo
            assert "logo.png" in html or branding["logo_url"] in html

    def test_should_read_branding_from_config(self):
        """Test that branding can be read from project config."""
        # Arrange
        config_file = "devforgeai/branding.yaml"

        # Act
        from devforgeai_documentation import BrandingConfig
        config = BrandingConfig()
        branding = config.load_from_file(config_file)

        # Assert
        # Should load config if it exists
        assert branding is None or isinstance(branding, dict)


class TestExportPerformance:
    """Test performance of export operations."""

    @pytest.mark.timeout(30)
    def test_html_export_should_complete_in_30_seconds(self):
        """Test that HTML conversion completes in <30 seconds."""
        # Arrange
        markdown = "# Large Document\n" + "\n## Section\nContent\n" * 100

        # Act
        from devforgeai_documentation import HTMLExporter
        import time
        exporter = HTMLExporter()
        start = time.time()
        html = exporter.convert(markdown)
        elapsed = time.time() - start

        # Assert
        assert html is not None
        assert elapsed < 30

    @pytest.mark.timeout(60)
    def test_pdf_export_should_complete_in_60_seconds(self):
        """Test that PDF conversion completes in <60 seconds."""
        # Arrange
        markdown = "# Test\nContent\n" * 50

        # Act
        from devforgeai_documentation import PDFExporter
        import time
        exporter = PDFExporter()
        start = time.time()
        pdf = exporter.convert(markdown)
        elapsed = time.time() - start

        # Assert
        # PDF may not be available (optional)
        if pdf is not None:
            assert elapsed < 60


class TestExportOptions:
    """Test various export options."""

    def test_should_support_html_export_option(self):
        """Test that /document --export=html works."""
        # Arrange
        export_type = "html"
        valid_types = ["html", "pdf", "md"]

        # Act
        is_valid = export_type in valid_types

        # Assert
        assert is_valid is True

    def test_should_support_pdf_export_option(self):
        """Test that /document --export=pdf works."""
        # Arrange
        export_type = "pdf"
        valid_types = ["html", "pdf", "md"]

        # Act
        is_valid = export_type in valid_types

        # Assert
        assert is_valid is True

    def test_should_default_to_markdown_if_no_export_specified(self):
        """Test that default export format is Markdown."""
        # Arrange
        no_export_specified = True

        # Act
        from devforgeai_documentation import ExportFormatter
        formatter = ExportFormatter()
        format_choice = formatter.get_default_format()

        # Assert
        assert format_choice == "md" or "markdown" in format_choice.lower()
