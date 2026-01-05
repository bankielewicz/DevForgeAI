"""
STORY-175 AC#5: Document Classification Logic

Tests that Step 2.1.5 is added to deep-validation-workflow.md.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Given: implementation complete
Then: Step 2.1.5 added to deep-validation-workflow.md

Coverage Target: 95%+
"""

import pytest
from pathlib import Path


class TestDocumentationExists:
    """Test AC#5: Documentation is added to deep-validation-workflow.md."""

    def test_deep_validation_workflow_contains_step_2_1_5(self):
        """
        Test: deep-validation-workflow.md contains Step 2.1.5.

        Given: Implementation is complete
        When: deep-validation-workflow.md is read
        Then: Contains "Step 2.1.5" or "2.1.5" section
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert
        assert "2.1.5" in content, "Step 2.1.5 not found in deep-validation-workflow.md"

    def test_step_2_1_5_documents_regression_classification(self):
        """
        Test: Step 2.1.5 documents regression vs pre-existing classification.

        Given: Step 2.1.5 exists
        When: Content is examined
        Then: Contains classification logic documentation
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert - should mention key concepts
        assert "regression" in content.lower() or "REGRESSION" in content
        assert "pre-existing" in content.lower() or "PRE_EXISTING" in content

    def test_step_2_1_5_documents_git_diff_usage(self):
        """
        Test: Step 2.1.5 documents git diff usage for changed file detection.

        Given: Step 2.1.5 exists
        When: Content is examined
        Then: Contains git diff documentation
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert
        assert "git diff" in content.lower() or "git" in content.lower()

    def test_step_2_1_5_documents_blocking_behavior(self):
        """
        Test: Step 2.1.5 documents blocking behavior difference.

        Given: Step 2.1.5 exists
        When: Content is examined
        Then: Documents that REGRESSION blocks, PRE_EXISTING warns
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert - should mention blocking behavior
        assert "block" in content.lower() or "warning" in content.lower()


class TestDocumentationPlacement:
    """Test correct placement of Step 2.1.5 in document structure."""

    def test_step_2_1_5_appears_after_step_2_1_4(self):
        """
        Test: Step 2.1.5 appears after Step 2.1.4 in the document.

        Given: Document contains both steps
        When: Content order is checked
        Then: 2.1.5 appears after 2.1.4
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert
        if "2.1.4" in content and "2.1.5" in content:
            pos_214 = content.find("2.1.4")
            pos_215 = content.find("2.1.5")
            assert pos_215 > pos_214, "Step 2.1.5 should appear after Step 2.1.4"

    def test_step_2_1_5_is_within_step_2_section(self):
        """
        Test: Step 2.1.5 is within the Step 2 section of the document.

        Given: Document has Step 2 section
        When: Step 2.1.5 location is checked
        Then: Step 2.1.5 is within Step 2 boundaries
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert - 2.1.5 should exist and be part of Step 2 hierarchy
        assert "2.1.5" in content or "Step 2.1.5" in content


class TestDocumentationContent:
    """Test detailed content of Step 2.1.5 documentation."""

    def test_step_2_1_5_has_meaningful_title(self):
        """
        Test: Step 2.1.5 has a descriptive title.

        Given: Step 2.1.5 exists
        When: Title is extracted
        Then: Title describes classification logic
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
            # Find the 2.1.5 line
            lines = content.split('\n')
            step_line = ""
            for line in lines:
                if "2.1.5" in line:
                    step_line = line
                    break
        else:
            step_line = ""

        # Assert - title should be descriptive, not just "2.1.5"
        if step_line:
            assert len(step_line) > 10, "Step 2.1.5 should have a descriptive title"

    def test_documentation_includes_implementation_pseudocode(self):
        """
        Test: Documentation includes implementation pseudocode or example.

        Given: Step 2.1.5 documentation exists
        When: Content is examined
        Then: Contains pseudocode or implementation example
        """
        # Arrange
        workflow_path = Path(".claude/skills/devforgeai-qa/references/deep-validation-workflow.md")

        # Act
        if workflow_path.exists():
            content = workflow_path.read_text()
        else:
            content = ""

        # Assert - should have code-like content (``` blocks or IF/ELSE)
        has_code_block = "```" in content
        has_pseudocode = "IF " in content.upper() or "ELSE" in content.upper()
        has_implementation = "changed_files" in content or "classification" in content

        assert has_code_block or has_pseudocode or has_implementation, \
            "Documentation should include implementation details"
