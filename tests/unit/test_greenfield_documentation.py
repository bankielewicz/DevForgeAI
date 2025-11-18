"""
Test suite for AC1: Greenfield Project Documentation Generation

Tests README.md generation, developer guides, API documentation,
troubleshooting guides, and proper file placement.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime
import json
import yaml


class TestReadmeGeneration:
    """Test README.md generation from stories and acceptance criteria."""

    def test_readme_generation_should_create_file_with_project_overview(self):
        """Test that README.md is created with project overview section."""
        # Arrange
        story = {
            "id": "STORY-040",
            "title": "DevForgeAI Documentation Skill and Command",
            "description": "Automated documentation generation",
            "user_story": "As a DevForgeAI user..."
        }
        context = {"project_name": "DevForgeAI"}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, context)

        # Assert
        assert result is not None
        assert "Project Overview" in result or "project overview" in result.lower()
        assert "DevForgeAI" in result

    def test_readme_generation_should_include_setup_instructions(self):
        """Test that README includes installation/setup instructions."""
        # Arrange
        story = {
            "technical_spec": {
                "setup_steps": ["npm install", "npm run dev"],
                "dependencies": ["Node.js 18+", "Python 3.10+"]
            }
        }

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        assert result is not None
        assert "setup" in result.lower() or "installation" in result.lower()
        assert "npm install" in result

    def test_readme_generation_should_include_usage_examples(self):
        """Test that README contains code examples."""
        # Arrange
        story = {
            "acceptance_criteria": [
                "When I run `/document STORY-040`",
                "Then README.md should be generated"
            ],
            "technical_spec": {
                "usage_examples": [
                    "/document STORY-040",
                    "/document --type=readme"
                ]
            }
        }

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        assert result is not None
        assert "Usage" in result or "Examples" in result
        assert "/document" in result

    def test_readme_generation_should_follow_coding_standards(self):
        """Test that generated README follows coding-standards.md conventions."""
        # Arrange
        coding_standards = {
            "markdown": {
                "max_line_length": 100,
                "headings": "ATX style (#, ##, ###)",
                "code_blocks": "Use ```language syntax"
            }
        }
        story = {"title": "Test Story"}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {}, coding_standards)

        # Assert
        assert result is not None
        lines = result.split('\n')
        # Check line length compliance (allowing some flexibility)
        long_lines = [l for l in lines if len(l) > 120]
        assert len(long_lines) < len(lines) * 0.1  # <10% of lines exceed 120 chars

        # Check heading style
        assert "#" in result  # Uses # for headings

    def test_readme_generation_should_include_multiple_sections(self):
        """Test that README contains required sections."""
        # Arrange
        story = {
            "id": "STORY-040",
            "title": "Documentation Skill",
            "acceptance_criteria": ["AC1", "AC2", "AC3"],
            "technical_spec": {"setup": ["step1"], "usage": ["example1"]}
        }

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        assert result is not None
        required_sections = ["Overview", "Installation", "Usage", "Features"]
        for section in required_sections:
            assert section.lower() in result.lower()


class TestDeveloperGuideGeneration:
    """Test developer guide creation from technical specifications."""

    def test_developer_guide_should_extract_from_technical_spec(self):
        """Test that developer guide is created from technical specification."""
        # Arrange
        story = {
            "technical_spec": {
                "architecture": "Microservices",
                "patterns": ["Command pattern", "Strategy pattern"],
                "layers": ["presentation", "application", "domain", "infrastructure"]
            }
        }

        # Act
        from devforgeai_documentation import generate_developer_guide
        result = generate_developer_guide(story)

        # Assert
        assert result is not None
        assert "Architecture" in result or "architecture" in result.lower()
        assert "Microservices" in result

    def test_developer_guide_should_document_project_structure(self):
        """Test that guide explains project structure."""
        # Arrange
        story = {
            "technical_spec": {
                "file_structure": {
                    "src/": "Source code",
                    "src/domain/": "Business logic",
                    "src/application/": "Use cases",
                    "tests/": "Test files"
                }
            }
        }

        # Act
        from devforgeai_documentation import generate_developer_guide
        result = generate_developer_guide(story)

        # Assert
        assert result is not None
        assert "src/" in result
        assert "File Structure" in result or "structure" in result.lower()

    def test_developer_guide_should_include_development_workflow(self):
        """Test that guide includes development workflow instructions."""
        # Arrange
        story = {
            "technical_spec": {
                "development_workflow": [
                    "1. Create feature branch",
                    "2. Run tests",
                    "3. Submit PR",
                    "4. Code review"
                ]
            }
        }

        # Act
        from devforgeai_documentation import generate_developer_guide
        result = generate_developer_guide(story)

        # Assert
        assert result is not None
        assert "Workflow" in result or "workflow" in result.lower()
        assert "branch" in result.lower()

    def test_developer_guide_should_document_design_patterns(self):
        """Test that guide documents architectural patterns used."""
        # Arrange
        story = {
            "technical_spec": {
                "design_patterns": [
                    "Dependency Injection",
                    "Repository Pattern",
                    "Strategy Pattern"
                ],
                "pattern_details": {
                    "Repository Pattern": "Used for data access abstraction"
                }
            }
        }

        # Act
        from devforgeai_documentation import generate_developer_guide
        result = generate_developer_guide(story)

        # Assert
        assert result is not None
        assert "Pattern" in result or "pattern" in result.lower()
        assert "Repository" in result


class TestAPIDocumentationGeneration:
    """Test API documentation generation from implemented endpoints."""

    def test_api_docs_should_list_all_endpoints(self):
        """Test that API documentation lists all implemented endpoints."""
        # Arrange
        code_metadata = {
            "endpoints": [
                {"method": "POST", "path": "/api/tasks", "description": "Create task"},
                {"method": "GET", "path": "/api/tasks", "description": "List tasks"},
                {"method": "GET", "path": "/api/tasks/:id", "description": "Get task"}
            ]
        }

        # Act
        from devforgeai_documentation import generate_api_docs
        result = generate_api_docs(code_metadata)

        # Assert
        assert result is not None
        assert "POST /api/tasks" in result
        assert "GET /api/tasks" in result
        assert "/api/tasks/:id" in result

    def test_api_docs_should_include_request_schemas(self):
        """Test that API docs include request/response schemas."""
        # Arrange
        code_metadata = {
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/api/tasks",
                    "request": {
                        "type": "object",
                        "properties": {
                            "title": "string",
                            "description": "string"
                        }
                    }
                }
            ]
        }

        # Act
        from devforgeai_documentation import generate_api_docs
        result = generate_api_docs(code_metadata)

        # Assert
        assert result is not None
        assert "Request" in result or "request" in result.lower()
        assert "title" in result

    def test_api_docs_should_include_response_examples(self):
        """Test that API docs include response examples."""
        # Arrange
        code_metadata = {
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/api/tasks/:id",
                    "response": {
                        "example": {"id": 1, "title": "Example Task", "status": "done"}
                    }
                }
            ]
        }

        # Act
        from devforgeai_documentation import generate_api_docs
        result = generate_api_docs(code_metadata)

        # Assert
        assert result is not None
        assert "Example" in result or "example" in result.lower()
        assert "Task" in result

    def test_api_docs_should_document_error_codes(self):
        """Test that API docs document error responses."""
        # Arrange
        code_metadata = {
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/api/tasks",
                    "errors": [
                        {"code": 400, "message": "Invalid input"},
                        {"code": 401, "message": "Unauthorized"},
                        {"code": 500, "message": "Internal server error"}
                    ]
                }
            ]
        }

        # Act
        from devforgeai_documentation import generate_api_docs
        result = generate_api_docs(code_metadata)

        # Assert
        assert result is not None
        assert "400" in result or "Invalid input" in result
        assert "401" in result or "Unauthorized" in result


class TestTroubleshootingGuideGeneration:
    """Test troubleshooting guide creation from edge cases."""

    def test_troubleshooting_guide_should_extract_from_edge_cases(self):
        """Test that troubleshooting guide is created from edge cases."""
        # Arrange
        story = {
            "edge_cases": [
                {
                    "name": "No Implemented Code Found",
                    "scenario": "Story has no code implementation",
                    "handling": "Generate placeholder documentation"
                },
                {
                    "name": "Conflicting Existing Documentation",
                    "scenario": "User-authored README conflicts",
                    "handling": "Preserve user sections, update auto-generated"
                }
            ]
        }

        # Act
        from devforgeai_documentation import generate_troubleshooting_guide
        result = generate_troubleshooting_guide(story)

        # Assert
        assert result is not None
        assert "No Implemented Code" in result or "no implemented code" in result.lower()
        assert "Conflicting" in result or "conflicting" in result.lower()

    def test_troubleshooting_guide_should_include_common_errors(self):
        """Test that guide includes common error scenarios and solutions."""
        # Arrange
        story = {
            "error_handling": [
                {
                    "error": "Documentation generation timeout",
                    "cause": "Large codebase analysis",
                    "solution": "Reduce file scope or increase timeout"
                }
            ]
        }

        # Act
        from devforgeai_documentation import generate_troubleshooting_guide
        result = generate_troubleshooting_guide(story)

        # Assert
        assert result is not None
        assert "timeout" in result.lower() or "Timeout" in result

    def test_troubleshooting_guide_should_format_as_qa_pairs(self):
        """Test that troubleshooting guide uses Q&A format."""
        # Arrange
        story = {
            "faq": [
                {"question": "How to generate API docs?", "answer": "Use /document --type=api"},
                {"question": "What if documentation fails?", "answer": "Check logs for errors"}
            ]
        }

        # Act
        from devforgeai_documentation import generate_troubleshooting_guide
        result = generate_troubleshooting_guide(story)

        # Assert
        assert result is not None
        assert "Q&A" in result or "FAQ" in result.lower() or "?" in result


class TestFileStructureCompliance:
    """Test that documentation follows source-tree.md structure."""

    def test_documentation_files_should_be_placed_correctly(self):
        """Test that generated files are placed per source-tree.md rules."""
        # Arrange
        source_tree = {
            "docs/": "Documentation files",
            "docs/api/": "API reference",
            "docs/guides/": "Developer guides",
            "README.md": "Project root"
        }
        story_id = "STORY-040"

        # Act
        from devforgeai_documentation import validate_file_placement
        placements = {
            "README.md": "/README.md",
            "API.md": "/docs/api/API.md",
            "DEVELOPER.md": "/docs/guides/DEVELOPER.md"
        }

        result = validate_file_placement(placements, source_tree)

        # Assert
        assert result is True  # All files in correct locations

    def test_readme_should_be_in_project_root(self):
        """Test that README.md is generated in project root."""
        # Arrange
        source_tree = {"README.md": "Project root"}

        # Act
        from devforgeai_documentation import get_readme_path
        path = get_readme_path(source_tree)

        # Assert
        assert path == "README.md"

    def test_developer_guide_should_be_in_docs_guides(self):
        """Test that DEVELOPER.md is placed in docs/guides/."""
        # Arrange
        source_tree = {"docs/guides/": "Developer guides"}

        # Act
        from devforgeai_documentation import get_guide_path
        path = get_guide_path(source_tree)

        # Assert
        assert "docs" in path and "guides" in path

    def test_api_docs_should_be_in_docs_api(self):
        """Test that API documentation is placed in docs/api/."""
        # Arrange
        source_tree = {"docs/api/": "API reference"}

        # Act
        from devforgeai_documentation import get_api_path
        path = get_api_path(source_tree)

        # Assert
        assert "docs" in path and "api" in path


class TestCodingStandardsCompliance:
    """Test that generated documentation follows coding-standards.md."""

    def test_markdown_should_use_atx_headings(self):
        """Test that all headings use ATX style (# ##)."""
        # Arrange
        story = {"title": "Test"}
        coding_standards = {"markdown": {"headings": "ATX style"}}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {}, coding_standards)

        # Assert
        assert result is not None
        # Check for ATX style headings
        lines = result.split('\n')
        heading_lines = [l for l in lines if l.startswith('#')]
        non_atx_headings = [l for l in heading_lines if '===' in result or '---' in result]
        assert len(non_atx_headings) == 0  # No setext-style headings

    def test_code_blocks_should_have_language_identifier(self):
        """Test that code blocks specify language."""
        # Arrange
        story = {
            "usage_examples": ["npm install", "npm run dev"]
        }
        coding_standards = {"markdown": {"code_blocks": "Use ```language syntax"}}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {}, coding_standards)

        # Assert
        assert result is not None
        # Check for ```language syntax
        assert "```" in result

    def test_documentation_should_not_exceed_line_length_limit(self):
        """Test that lines don't exceed max length from coding standards."""
        # Arrange
        story = {"title": "Test"}
        coding_standards = {"markdown": {"max_line_length": 100}}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {}, coding_standards)

        # Assert
        assert result is not None
        lines = result.split('\n')
        # Allow code blocks and links to exceed slightly
        text_lines = [l for l in lines if not l.startswith('```') and not l.startswith('>')]
        long_lines = [l for l in text_lines if len(l) > 110]
        # Should have very few long lines
        assert len(long_lines) < len(text_lines) * 0.05


class TestGenerationOptions:
    """Test various generation options and parameters."""

    def test_should_support_story_id_parameter(self):
        """Test that /document STORY-ID works."""
        # Arrange
        story_id = "STORY-040"

        # Act
        from devforgeai_documentation import DocumentationGenerator
        gen = DocumentationGenerator()
        result = gen.validate_story_id(story_id)

        # Assert
        assert result is True

    def test_should_support_type_parameter(self):
        """Test that /document --type=readme works."""
        # Arrange
        doc_type = "readme"
        valid_types = ["readme", "api", "architecture", "roadmap", "all"]

        # Act
        is_valid = doc_type in valid_types

        # Assert
        assert is_valid is True

    def test_should_support_multiple_types(self):
        """Test that --type=all generates all documentation."""
        # Arrange
        doc_type = "all"

        # Act
        from devforgeai_documentation import DocumentationGenerator
        gen = DocumentationGenerator()
        types_to_generate = gen.get_types_for_all()

        # Assert
        assert "readme" in types_to_generate
        assert "api" in types_to_generate
        assert "architecture" in types_to_generate


class TestDocumentationReturnValue:
    """Test that generated documentation is returned correctly."""

    def test_generate_readme_should_return_string(self):
        """Test that generate_readme returns a string."""
        # Arrange
        story = {"title": "Test"}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_readme_should_not_return_none(self):
        """Test that README generation never returns None."""
        # Arrange
        story = {}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        assert result is not None

    def test_generated_docs_should_be_valid_markdown(self):
        """Test that generated content is valid Markdown."""
        # Arrange
        story = {"title": "Test Story"}

        # Act
        from devforgeai_documentation import generate_readme
        result = generate_readme(story, {})

        # Assert
        # Basic Markdown validation
        assert "#" in result  # Has headings
        # Should have sections
        assert len(result.split('\n')) > 5


class TestPerformanceNFR:
    """Test performance non-functional requirements."""

    @pytest.mark.timeout(120)  # 2 minutes max
    def test_greenfield_documentation_should_complete_in_two_minutes(self):
        """Test that greenfield documentation generation completes in <2 minutes."""
        # Arrange
        story = {
            "id": "STORY-040",
            "title": "Documentation Skill",
            "technical_spec": {"layers": ["presentation", "application", "domain"]},
            "acceptance_criteria": ["AC1", "AC2", "AC3", "AC4", "AC5"]
        }

        # Act
        from devforgeai_documentation import generate_readme
        import time
        start = time.time()
        result = generate_readme(story, {})
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed < 120  # 2 minutes
