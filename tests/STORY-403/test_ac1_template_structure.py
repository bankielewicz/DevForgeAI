"""
Test: AC#1 - 10-Element Canonical Template Structure
Story: STORY-403
Generated: 2026-02-14

Validates that the dead-code-detector subagent definition contains
all 10 elements required by the EPIC-061 canonical template.

These tests MUST FAIL initially (TDD Red phase) because the subagent
file does not exist yet.
"""
import re
import pytest


class TestCanonicalTemplateStructure:
    """Verify all 10 elements of the canonical template are present."""

    # === Element 1: Role ===

    def test_should_contain_role_element_when_subagent_defined(self, subagent_content):
        """AC#1: Role element must be present in subagent definition."""
        # Arrange
        content = subagent_content

        # Act & Assert
        assert re.search(
            r"(?i)(^#+\s*role|role\s*:|you are a)", content, re.MULTILINE
        ), "Role element not found in dead-code-detector.md"

    # === Element 2: Task ===

    def test_should_contain_task_element_when_subagent_defined(self, subagent_content):
        """AC#1: Task element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*task|task\s*:|purpose)", content, re.MULTILINE
        ), "Task element not found in dead-code-detector.md"

    # === Element 3: Context ===

    def test_should_contain_context_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Context element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*context|context\s*:)", content, re.MULTILINE
        ), "Context element not found in dead-code-detector.md"

    # === Element 4: Examples ===

    def test_should_contain_examples_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Examples element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*example)", content, re.MULTILINE
        ), "Examples element not found in dead-code-detector.md"

    # === Element 5: Input Data ===

    def test_should_contain_input_data_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Input Data element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*input|input\s*(data|specification))", content, re.MULTILINE
        ), "Input Data element not found in dead-code-detector.md"

    # === Element 6: Thinking ===

    def test_should_contain_thinking_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Thinking element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*thinking|thinking\s*:|reasoning)", content, re.MULTILINE
        ), "Thinking element not found in dead-code-detector.md"

    # === Element 7: Output Format ===

    def test_should_contain_output_format_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Output Format element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*output)", content, re.MULTILINE
        ), "Output Format element not found in dead-code-detector.md"

    # === Element 8: Constraints ===

    def test_should_contain_constraints_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Constraints element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*constraint)", content, re.MULTILINE
        ), "Constraints element not found in dead-code-detector.md"

    # === Element 9: Uncertainty Handling ===

    def test_should_contain_uncertainty_handling_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Uncertainty Handling element must be present."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*uncertainty|uncertainty\s*handling)", content, re.MULTILINE
        ), "Uncertainty Handling element not found in dead-code-detector.md"

    # === Element 10: Prefill ===

    def test_should_contain_prefill_element_when_subagent_defined(
        self, subagent_content
    ):
        """AC#1: Prefill element must be present in subagent definition."""
        content = subagent_content
        assert re.search(
            r"(?i)(^#+\s*prefill|prefill\s*:)", content, re.MULTILINE
        ), "Prefill element not found in dead-code-detector.md"

    # === Completeness Check ===

    def test_should_have_all_10_elements_when_template_complete(
        self, subagent_content
    ):
        """AC#1: All 10 canonical elements must be present simultaneously."""
        content = subagent_content
        elements = {
            "Role": r"(?i)(^#+\s*role|role\s*:|you are a)",
            "Task": r"(?i)(^#+\s*task|task\s*:|purpose)",
            "Context": r"(?i)(^#+\s*context|context\s*:)",
            "Examples": r"(?i)(^#+\s*example)",
            "Input Data": r"(?i)(^#+\s*input|input\s*(data|specification))",
            "Thinking": r"(?i)(^#+\s*thinking|thinking\s*:|reasoning)",
            "Output Format": r"(?i)(^#+\s*output)",
            "Constraints": r"(?i)(^#+\s*constraint)",
            "Uncertainty Handling": r"(?i)(^#+\s*uncertainty|uncertainty\s*handling)",
            "Prefill": r"(?i)(^#+\s*prefill|prefill\s*:)",
        }
        missing = []
        for name, pattern in elements.items():
            if not re.search(pattern, content, re.MULTILINE):
                missing.append(name)
        assert not missing, (
            f"Missing canonical template elements: {', '.join(missing)}. "
            f"Found {10 - len(missing)}/10 elements."
        )
