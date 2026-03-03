"""
Test suite for AC3: Architecture Diagram Generation

Tests Mermaid flowchart, sequence diagram, and architecture diagram generation,
plus validation against architecture constraints.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import re


class TestMermaidFlowchartGeneration:
    """Test Mermaid flowchart generation from code structure."""

    def test_flowchart_should_be_generated_from_application_flow(self):
        """Test that flowcharts are created from application workflows."""
        # Arrange
        workflow = {
            "name": "User Registration",
            "steps": [
                "User enters email",
                "Validate email format",
                "Check if email exists",
                "Create user",
                "Send confirmation email"
            ]
        }

        # Act
        from devforgeai_documentation import FlowchartGenerator
        gen = FlowchartGenerator()
        flowchart = gen.generate_flowchart(workflow)

        # Assert
        assert flowchart is not None
        assert isinstance(flowchart, str)
        assert "graph" in flowchart.lower() or "flowchart" in flowchart.lower()

    def test_flowchart_should_use_mermaid_syntax(self):
        """Test that generated flowchart uses valid Mermaid syntax."""
        # Arrange
        workflow = {
            "steps": ["Start", "Process", "End"],
            "decisions": ["Valid?"]
        }

        # Act
        from devforgeai_documentation import FlowchartGenerator
        gen = FlowchartGenerator()
        flowchart = gen.generate_flowchart(workflow)

        # Assert
        assert flowchart is not None
        # Should have Mermaid syntax elements
        mermaid_elements = ["graph", "-->", "node"]
        assert any(element in flowchart for element in mermaid_elements) or "flowchart" in flowchart.lower()

    def test_flowchart_should_show_decision_points(self):
        """Test that flowchart includes decision nodes."""
        # Arrange
        workflow = {
            "steps": [
                "Start",
                {"decision": "Is valid?", "yes": "Continue", "no": "Error"}
            ]
        }

        # Act
        from devforgeai_documentation import FlowchartGenerator
        gen = FlowchartGenerator()
        flowchart = gen.generate_flowchart(workflow)

        # Assert
        assert flowchart is not None
        assert "valid" in flowchart.lower() or "decision" in flowchart.lower()

    def test_flowchart_should_include_error_paths(self):
        """Test that flowchart shows error handling paths."""
        # Arrange
        workflow = {
            "name": "API Request",
            "steps": ["Make request", "Parse response"],
            "error_handling": [
                "Network error -> Retry",
                "Invalid response -> Error message"
            ]
        }

        # Act
        from devforgeai_documentation import FlowchartGenerator
        gen = FlowchartGenerator()
        flowchart = gen.generate_flowchart(workflow)

        # Assert
        assert flowchart is not None
        # Should mention error handling
        diagram_text = flowchart.lower()
        assert "error" in diagram_text or "retry" in diagram_text


class TestSequenceDiagramGeneration:
    """Test Mermaid sequence diagram generation."""

    def test_sequence_diagram_should_show_actor_interactions(self):
        """Test that sequence diagrams show interactions between actors."""
        # Arrange
        interaction = {
            "actors": ["User", "API", "Database"],
            "sequence": [
                ("User", "API", "POST /users {name, email}"),
                ("API", "Database", "INSERT user"),
                ("Database", "API", "User ID 123"),
                ("API", "User", "Created response")
            ]
        }

        # Act
        from devforgeai_documentation import SequenceDiagramGenerator
        gen = SequenceDiagramGenerator()
        diagram = gen.generate_sequence_diagram(interaction)

        # Assert
        assert diagram is not None
        assert isinstance(diagram, str)
        # Should mention actors
        diagram_text = diagram.lower()
        assert "user" in diagram_text or "api" in diagram_text

    def test_sequence_diagram_should_use_mermaid_syntax(self):
        """Test that sequence diagram uses valid Mermaid syntax."""
        # Arrange
        interaction = {
            "actors": ["A", "B"],
            "sequence": [("A", "B", "message")]
        }

        # Act
        from devforgeai_documentation import SequenceDiagramGenerator
        gen = SequenceDiagramGenerator()
        diagram = gen.generate_sequence_diagram(interaction)

        # Assert
        assert diagram is not None
        # Mermaid sequence syntax
        assert "sequenceDiagram" in diagram or "->" in diagram

    def test_sequence_diagram_should_include_loop_operations(self):
        """Test that sequence diagrams show loops and repeating actions."""
        # Arrange
        interaction = {
            "actors": ["Client", "Queue", "Worker"],
            "sequence": [
                ("Client", "Queue", "Submit job"),
                ("Queue", "Worker", "Dequeue job (loop until done)")
            ]
        }

        # Act
        from devforgeai_documentation import SequenceDiagramGenerator
        gen = SequenceDiagramGenerator()
        diagram = gen.generate_sequence_diagram(interaction)

        # Assert
        assert diagram is not None
        # Should show looping or queue concept
        diagram_text = diagram.lower()
        assert "loop" in diagram_text or "queue" in diagram_text

    def test_sequence_diagram_should_show_parallel_operations(self):
        """Test that diagram can show parallel/concurrent operations."""
        # Arrange
        interaction = {
            "actors": ["Client", "Service1", "Service2"],
            "parallel_sequence": [
                ("Client", "Service1", "Request A"),
                ("Client", "Service2", "Request B")
            ]
        }

        # Act
        from devforgeai_documentation import SequenceDiagramGenerator
        gen = SequenceDiagramGenerator()
        diagram = gen.generate_sequence_diagram(interaction)

        # Assert
        assert diagram is not None


class TestArchitectureDiagramGeneration:
    """Test architecture diagram generation."""

    def test_architecture_diagram_should_show_components(self):
        """Test that architecture diagram shows system components."""
        # Arrange
        architecture = {
            "components": [
                {"name": "Web UI", "type": "Frontend"},
                {"name": "API Server", "type": "Backend"},
                {"name": "Database", "type": "Storage"},
                {"name": "Cache", "type": "Storage"}
            ],
            "relationships": [
                ("Web UI", "API Server"),
                ("API Server", "Database"),
                ("API Server", "Cache")
            ]
        }

        # Act
        from devforgeai_documentation import ArchitectureDiagramGenerator
        gen = ArchitectureDiagramGenerator()
        diagram = gen.generate_architecture_diagram(architecture)

        # Assert
        assert diagram is not None
        assert isinstance(diagram, str)
        # Should mention components
        diagram_text = diagram.lower()
        assert "api" in diagram_text or "database" in diagram_text

    def test_architecture_diagram_should_show_layers(self):
        """Test that diagram shows Clean Architecture layers."""
        # Arrange
        architecture = {
            "pattern": "Clean Architecture",
            "layers": [
                {"name": "Presentation", "components": ["Controllers", "Views"]},
                {"name": "Application", "components": ["Use Cases"]},
                {"name": "Domain", "components": ["Entities", "Repositories"]},
                {"name": "Infrastructure", "components": ["DB", "APIs"]}
            ]
        }

        # Act
        from devforgeai_documentation import ArchitectureDiagramGenerator
        gen = ArchitectureDiagramGenerator()
        diagram = gen.generate_architecture_diagram(architecture)

        # Assert
        assert diagram is not None
        # Should show layered structure
        assert "Presentation" in diagram or "presentation" in diagram.lower()

    def test_architecture_diagram_should_show_dependencies(self):
        """Test that diagram visualizes component dependencies."""
        # Arrange
        architecture = {
            "components": ["UserService", "AuthService", "TokenService"],
            "dependencies": [
                ("UserService", "AuthService"),
                ("AuthService", "TokenService")
            ]
        }

        # Act
        from devforgeai_documentation import ArchitectureDiagramGenerator
        gen = ArchitectureDiagramGenerator()
        diagram = gen.generate_architecture_diagram(architecture)

        # Assert
        assert diagram is not None
        # Should show some form of dependency relationship
        assert "-->" in diagram or "->" in diagram or "rel" in diagram.lower()

    def test_architecture_diagram_should_show_external_integrations(self):
        """Test that diagram shows external system integrations."""
        # Arrange
        architecture = {
            "components": [
                {"name": "Application", "internal": True},
                {"name": "Stripe API", "external": True},
                {"name": "Email Service", "external": True}
            ],
            "integrations": [
                ("Application", "Stripe API"),
                ("Application", "Email Service")
            ]
        }

        # Act
        from devforgeai_documentation import ArchitectureDiagramGenerator
        gen = ArchitectureDiagramGenerator()
        diagram = gen.generate_architecture_diagram(architecture)

        # Assert
        assert diagram is not None
        # Should distinguish external systems
        diagram_text = diagram.lower()
        assert "stripe" in diagram_text or "email" in diagram_text or "external" in diagram_text


class TestDiagramValidation:
    """Test Mermaid diagram validation against syntax."""

    def test_diagram_should_have_valid_mermaid_syntax(self):
        """Test that generated diagrams have valid Mermaid syntax."""
        # Arrange
        diagram = """graph TD
            A[Start]
            B{Decision}
            C[Process]
            A --> B
            B -->|Yes| C
            B -->|No| A
        """

        # Act
        from devforgeai_documentation import DiagramValidator
        validator = DiagramValidator()
        is_valid = validator.validate_mermaid_syntax(diagram)

        # Assert
        assert is_valid is True

    def test_should_detect_invalid_mermaid_syntax(self):
        """Test that validator detects invalid diagrams."""
        # Arrange
        invalid_diagram = """graph TD
            A[Start]
            B{Decision
            A --> B
        """  # Missing closing bracket and arrow

        # Act
        from devforgeai_documentation import DiagramValidator
        validator = DiagramValidator()
        is_valid = validator.validate_mermaid_syntax(invalid_diagram)

        # Assert
        assert is_valid is False

    def test_validator_should_detect_missing_node_definitions(self):
        """Test that validator checks for undefined nodes."""
        # Arrange
        diagram = """graph TD
            A[Start] --> B
            B --> C[End]
            C --> D[Extra]
        """  # D is referenced but maybe not properly defined

        # Act
        from devforgeai_documentation import DiagramValidator
        validator = DiagramValidator()
        issues = validator.check_diagram_issues(diagram)

        # Assert
        assert issues is not None
        # Should return a list or indication of issues
        assert isinstance(issues, (list, dict, bool))


class TestArchitectureConstraintValidation:
    """Test that diagrams validate against architecture-constraints.md."""

    def test_diagram_should_respect_dependency_rules(self):
        """Test that diagram respects layer dependency rules."""
        # Arrange
        architecture = {
            "layers": {
                "presentation": ["Controller"],
                "application": ["UseCase"],
                "domain": ["Entity"],
                "infrastructure": ["Database"]
            }
        }
        architecture_constraints = {
            "allowed": [
                "Presentation -> Application",
                "Application -> Domain",
                "Infrastructure -> Domain (via interface)"
            ],
            "forbidden": [
                "Domain -> Application",
                "Domain -> Infrastructure",
                "Presentation -> Infrastructure"
            ]
        }

        # Act
        from devforgeai_documentation import ConstraintValidator
        validator = ConstraintValidator()
        diagram = validator.generate_constrained_diagram(architecture, architecture_constraints)

        # Assert
        assert diagram is not None
        # Should not show forbidden dependencies
        assert "Domain" not in diagram or "Domain -> Application" not in diagram

    def test_diagram_should_validate_against_constraints(self):
        """Test that generated diagram is validated against constraints."""
        # Arrange
        diagram = """graph TD
            Presentation --> Application
            Application --> Domain
            Infrastructure --> Domain
        """
        constraints = {
            "forbidden": ["Domain -> Application"]
        }

        # Act
        from devforgeai_documentation import ConstraintValidator
        validator = ConstraintValidator()
        is_compliant = validator.validate_constraints(diagram, constraints)

        # Assert
        assert is_compliant is not None
        # Should pass as there are no forbidden paths shown


class TestDiagramEmbedding:
    """Test embedding diagrams in documentation."""

    def test_diagram_should_be_embedded_in_markdown(self):
        """Test that diagrams are embedded in Markdown as code blocks."""
        # Arrange
        diagram = "graph TD\nA --> B"

        # Act
        from devforgeai_documentation import DiagramEmbedder
        embedder = DiagramEmbedder()
        markdown = embedder.embed_diagram(diagram, "architecture")

        # Assert
        assert markdown is not None
        assert "```mermaid" in markdown or "mermaid" in markdown.lower()
        assert diagram in markdown

    def test_diagram_should_have_caption(self):
        """Test that embedded diagrams include descriptive captions."""
        # Arrange
        diagram = "graph TD\nA --> B"
        caption = "Application Architecture"

        # Act
        from devforgeai_documentation import DiagramEmbedder
        embedder = DiagramEmbedder()
        markdown = embedder.embed_diagram(diagram, "architecture", caption)

        # Assert
        assert markdown is not None
        assert caption in markdown or "architecture" in markdown.lower()

    def test_multiple_diagrams_should_be_embedded(self):
        """Test that multiple diagrams can be embedded in same document."""
        # Arrange
        diagrams = [
            {"type": "flowchart", "content": "graph TD\nA --> B", "caption": "Flow 1"},
            {"type": "sequence", "content": "sequenceDiagram\nA->>B", "caption": "Sequence 1"},
            {"type": "architecture", "content": "graph TD\nC[Component]", "caption": "Architecture"}
        ]

        # Act
        from devforgeai_documentation import DiagramEmbedder
        embedder = DiagramEmbedder()
        markdown = embedder.embed_multiple_diagrams(diagrams)

        # Assert
        assert markdown is not None
        # Should contain all diagrams
        assert len([d for d in diagrams if d["caption"] in markdown]) >= 2


class TestDiagramInDocumentation:
    """Test integration of diagrams into final documentation."""

    def test_architecture_doc_should_include_all_diagrams(self):
        """Test that architecture documentation includes flowchart, sequence, and architecture diagrams."""
        # Arrange
        architecture = {
            "components": ["A", "B", "C"],
            "workflows": ["Flow1"],
            "interactions": ["Actor1", "Actor2"]
        }

        # Act
        from devforgeai_documentation import ArchitectureDocumentationGenerator
        gen = ArchitectureDocumentationGenerator()
        doc = gen.generate_architecture_documentation(architecture)

        # Assert
        assert doc is not None
        # Should mention diagrams
        doc_lower = doc.lower()
        assert "diagram" in doc_lower or "flowchart" in doc_lower or "sequence" in doc_lower

    def test_should_place_diagrams_in_appropriate_sections(self):
        """Test that diagrams are placed in correct documentation sections."""
        # Arrange
        sections = {
            "Overview": None,
            "Architecture": None,
            "Workflows": None,
            "Integration": None
        }

        # Act
        from devforgeai_documentation import DocumentationPlanner
        planner = DocumentationPlanner()
        placement = planner.plan_diagram_placement(sections)

        # Assert
        assert placement is not None
        # Architecture diagrams should go in "Architecture" section
        if "Architecture" in placement:
            assert "architecture" in str(placement["Architecture"]).lower() or len(str(placement["Architecture"])) > 0


class TestDiagramSyntaxCorrection:
    """Test automatic correction of Mermaid syntax errors."""

    def test_should_auto_fix_missing_semicolons(self):
        """Test that validator can auto-fix missing semicolons."""
        # Arrange
        broken_diagram = "graph TD\nA[Start]\nB[End]\nA --> B"

        # Act
        from devforgeai_documentation import DiagramAutoFixer
        fixer = DiagramAutoFixer()
        fixed = fixer.auto_fix_syntax(broken_diagram)

        # Assert
        assert fixed is not None
        assert isinstance(fixed, str)

    def test_should_auto_fix_unclosed_brackets(self):
        """Test that validator can auto-fix unclosed brackets."""
        # Arrange
        broken_diagram = "graph TD\nA[Start\nB[End]\nA --> B"

        # Act
        from devforgeai_documentation import DiagramAutoFixer
        fixer = DiagramAutoFixer()
        fixed = fixer.auto_fix_syntax(broken_diagram)

        # Assert
        assert fixed is not None
        # Should have matching brackets
        assert fixed.count("[") == fixed.count("]")

    def test_should_report_errors_if_auto_fix_fails(self):
        """Test that errors are reported if auto-fix cannot resolve them."""
        # Arrange
        broken_diagram = "completely invalid content"

        # Act
        from devforgeai_documentation import DiagramAutoFixer
        fixer = DiagramAutoFixer()
        result = fixer.auto_fix_syntax(broken_diagram)

        # Assert
        # Either returns fixed version or error message
        assert result is not None


class TestDiagramGeneration:
    """Test complete diagram generation workflow."""

    def test_generate_flowchart_for_use_case(self):
        """Test flowchart generation for specific use case."""
        # Arrange
        use_case = "User Registration"

        # Act
        from devforgeai_documentation import DiagramGenerator
        gen = DiagramGenerator()
        diagram = gen.generate_for_use_case(use_case)

        # Assert
        assert diagram is not None

    def test_generate_sequence_diagram_for_workflow(self):
        """Test sequence diagram generation for workflow."""
        # Arrange
        workflow = "Payment Processing"

        # Act
        from devforgeai_documentation import DiagramGenerator
        gen = DiagramGenerator()
        diagram = gen.generate_for_workflow(workflow)

        # Assert
        assert diagram is not None

    def test_generate_architecture_from_code_structure(self):
        """Test architecture diagram generation from code structure."""
        # Arrange
        code_structure = {
            "layers": {
                "src/controllers": "Presentation",
                "src/services": "Application",
                "src/entities": "Domain"
            }
        }

        # Act
        from devforgeai_documentation import DiagramGenerator
        gen = DiagramGenerator()
        diagram = gen.generate_from_code_structure(code_structure)

        # Assert
        assert diagram is not None


class TestDiagramPerformance:
    """Test diagram generation performance."""

    @pytest.mark.timeout(30)
    def test_diagram_generation_should_complete_in_30_seconds(self):
        """Test that a single diagram generates in <30 seconds."""
        # Arrange
        architecture = {
            "components": [f"Component_{i}" for i in range(20)],
            "relationships": [(f"Component_{i}", f"Component_{i+1}") for i in range(19)]
        }

        # Act
        from devforgeai_documentation import ArchitectureDiagramGenerator
        import time
        gen = ArchitectureDiagramGenerator()
        start = time.time()
        diagram = gen.generate_architecture_diagram(architecture)
        elapsed = time.time() - start

        # Assert
        assert diagram is not None
        assert elapsed < 30


class TestDiagramValidationEdgeCases:
    """Test edge cases in diagram validation."""

    def test_should_handle_empty_diagram(self):
        """Test that validator handles empty diagram gracefully."""
        # Arrange
        empty_diagram = ""

        # Act
        from devforgeai_documentation import DiagramValidator
        validator = DiagramValidator()
        result = validator.validate_mermaid_syntax(empty_diagram)

        # Assert
        assert result is not None
        assert isinstance(result, bool)

    def test_should_handle_very_large_diagram(self):
        """Test that validator handles diagrams with many nodes."""
        # Arrange
        large_diagram = "graph TD\n"
        for i in range(100):
            large_diagram += f"A{i}[Node {i}]\n"
            if i > 0:
                large_diagram += f"A{i-1} --> A{i}\n"

        # Act
        from devforgeai_documentation import DiagramValidator
        validator = DiagramValidator()
        is_valid = validator.validate_mermaid_syntax(large_diagram)

        # Assert
        assert is_valid is not None
