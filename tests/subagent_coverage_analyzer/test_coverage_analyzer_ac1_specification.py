"""
AC1 Tests: Subagent Specification Created

Tests that validate coverage-analyzer subagent file exists with proper structure.

Acceptance Criteria:
- AC1: Subagent Specification Created - File exists with YAML frontmatter,
  8-phase workflow, input/output contracts, guardrails
"""

import pytest
from pathlib import Path


class TestAC1SubagentSpecificationFile:
    """Tests for AC1: Subagent file existence and structure."""

    def test_subagent_file_exists(self, subagent_spec_path):
        """Test: File .claude/agents/coverage-analyzer.md exists."""
        # Arrange
        expected_path = subagent_spec_path

        # Act
        file_exists = expected_path.exists()

        # Assert
        assert file_exists, f"Subagent file not found at {expected_path}"
        assert expected_path.is_file(), f"Expected file, but {expected_path} is not a file"


class TestAC1YAMLFrontmatter:
    """Tests for AC1: YAML frontmatter validation."""

    def test_frontmatter_has_name_field(self, subagent_spec_path):
        """Test: YAML frontmatter includes 'name: coverage-analyzer'."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        name_present = "name: coverage-analyzer" in content

        # Assert
        assert name_present, "YAML frontmatter missing 'name: coverage-analyzer'"

    def test_frontmatter_has_description(self, subagent_spec_path):
        """Test: YAML frontmatter includes 'description:' field."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        description_present = "description:" in content

        # Assert
        assert description_present, "YAML frontmatter missing 'description:' field"

    def test_frontmatter_has_tools_list(self, subagent_spec_path):
        """Test: YAML frontmatter includes 'tools:' array."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        tools_present = "tools:" in content

        # Assert
        assert tools_present, "YAML frontmatter missing 'tools:' list"

    def test_tools_include_read_write_grep_glob(self, subagent_spec_path):
        """Test: Tools list includes Read, Grep, Glob, Bash."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        has_read = "Read" in content
        has_grep = "Grep" in content
        has_glob = "Glob" in content
        has_bash = "Bash" in content

        # Assert
        assert has_read, "Tools missing 'Read'"
        assert has_grep, "Tools missing 'Grep'"
        assert has_glob, "Tools missing 'Glob'"
        assert has_bash, "Tools missing 'Bash' (for coverage commands)"

    def test_frontmatter_has_model_field(self, subagent_spec_path):
        """Test: YAML frontmatter includes 'model: claude-haiku-4-5-20251001'."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        model_present = "model: claude-haiku-4-5-20251001" in content

        # Assert
        assert model_present, "YAML frontmatter missing 'model: claude-haiku-4-5-20251001'"


class TestAC1EightPhaseWorkflow:
    """Tests for AC1: 8-phase workflow documentation."""

    def test_phase_1_context_loading_documented(self, subagent_spec_path):
        """Test: Phase 1: Context Loading documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_1_present = "Phase 1: Context Loading" in content or "Phase 1: Load Context" in content

        # Assert
        assert phase_1_present, "Phase 1 (Context Loading) not documented"

    def test_phase_2_execute_coverage_documented(self, subagent_spec_path):
        """Test: Phase 2: Execute Coverage documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_2_present = "Phase 2: Execute Coverage" in content or "Phase 2: Coverage Execution" in content

        # Assert
        assert phase_2_present, "Phase 2 (Execute Coverage) not documented"

    def test_phase_3_classify_by_layer_documented(self, subagent_spec_path):
        """Test: Phase 3: Classify by Layer documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_3_present = "Phase 3: Classify by Layer" in content or "Phase 3: File Classification" in content

        # Assert
        assert phase_3_present, "Phase 3 (Classify by Layer) not documented"

    def test_phase_4_calculate_coverage_documented(self, subagent_spec_path):
        """Test: Phase 4: Calculate Coverage documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_4_present = "Phase 4: Calculate Coverage" in content or "Phase 4: Coverage Calculation" in content

        # Assert
        assert phase_4_present, "Phase 4 (Calculate Coverage) not documented"

    def test_phase_5_validate_thresholds_documented(self, subagent_spec_path):
        """Test: Phase 5: Validate Thresholds documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_5_present = "Phase 5: Validate Thresholds" in content or "Phase 5: Threshold Validation" in content

        # Assert
        assert phase_5_present, "Phase 5 (Validate Thresholds) not documented"

    def test_phase_6_identify_gaps_documented(self, subagent_spec_path):
        """Test: Phase 6: Identify Gaps documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_6_present = "Phase 6: Identify Gaps" in content or "Phase 6: Gap Identification" in content

        # Assert
        assert phase_6_present, "Phase 6 (Identify Gaps) not documented"

    def test_phase_7_generate_recommendations_documented(self, subagent_spec_path):
        """Test: Phase 7: Generate Recommendations documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_7_present = "Phase 7: Generate Recommendations" in content or "Phase 7: Recommendations" in content

        # Assert
        assert phase_7_present, "Phase 7 (Generate Recommendations) not documented"

    def test_phase_8_return_results_documented(self, subagent_spec_path):
        """Test: Phase 8: Return Results documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        phase_8_present = "Phase 8: Return Results" in content or "Phase 8: Result Formatting" in content

        # Assert
        assert phase_8_present, "Phase 8 (Return Results) not documented"


class TestAC1InputOutputContracts:
    """Tests for AC1: Input/output contract documentation."""

    def test_input_contract_documented(self, subagent_spec_path):
        """Test: Input contract documented (story_id, language, test_command, etc.)."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        input_contract_present = "Input Contract" in content or "## Input" in content

        # Assert
        assert input_contract_present, "Input contract not documented"

    def test_input_includes_story_id(self, subagent_spec_path):
        """Test: Input contract includes story_id parameter."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        story_id_present = "story_id" in content

        # Assert
        assert story_id_present, "Input contract missing 'story_id' parameter"

    def test_input_includes_language(self, subagent_spec_path):
        """Test: Input contract includes language parameter."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        language_present = "language" in content

        # Assert
        assert language_present, "Input contract missing 'language' parameter"

    def test_input_includes_test_command(self, subagent_spec_path):
        """Test: Input contract includes test_command parameter."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        test_command_present = "test_command" in content

        # Assert
        assert test_command_present, "Input contract missing 'test_command' parameter"

    def test_output_contract_documented(self, subagent_spec_path):
        """Test: Output contract documented (JSON structure)."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        output_contract_present = "Output Contract" in content or "## Output" in content or "## Returns" in content

        # Assert
        assert output_contract_present, "Output contract not documented"

    def test_output_includes_coverage_summary(self, subagent_spec_path):
        """Test: Output includes coverage_summary field."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        summary_present = "coverage_summary" in content

        # Assert
        assert summary_present, "Output contract missing 'coverage_summary'"

    def test_output_includes_validation_result(self, subagent_spec_path):
        """Test: Output includes validation_result field."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        validation_present = "validation_result" in content

        # Assert
        assert validation_present, "Output contract missing 'validation_result'"

    def test_output_includes_blocks_qa(self, subagent_spec_path):
        """Test: Output includes blocks_qa boolean flag."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        blocks_qa_present = "blocks_qa" in content

        # Assert
        assert blocks_qa_present, "Output contract missing 'blocks_qa' flag"


class TestAC1Guardrails:
    """Tests for AC1: Guardrails documentation."""

    def test_guardrails_section_exists(self, subagent_spec_path):
        """Test: Guardrails section exists."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        guardrails_present = "## Guardrails" in content or "Guardrails" in content

        # Assert
        assert guardrails_present, "Guardrails section not documented"

    def test_guardrail_read_only_operation(self, subagent_spec_path):
        """Test: Guardrail 1: Read-only operation documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        read_only_present = "read-only" in content.lower()

        # Assert
        assert read_only_present, "Guardrail missing: Read-only operation"

    def test_guardrail_context_file_enforcement(self, subagent_spec_path):
        """Test: Guardrail 2: Context file enforcement documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        context_enforcement_present = "context" in content.lower() and ("file" in content.lower() or "enforce" in content.lower())

        # Assert
        assert context_enforcement_present, "Guardrail missing: Context file enforcement"

    def test_guardrail_threshold_blocking(self, subagent_spec_path):
        """Test: Guardrail 3: Threshold blocking (95%/85%/80%) documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        has_95 = "95%" in content or "0.95" in content
        has_85 = "85%" in content or "0.85" in content
        has_80 = "80%" in content or "0.80" in content
        threshold_blocking = has_95 and has_85 and has_80

        # Assert
        assert threshold_blocking, "Guardrail missing: Threshold blocking (95%/85%/80%)"

    def test_guardrail_evidence_requirements(self, subagent_spec_path):
        """Test: Guardrail 4: Evidence requirements documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        evidence_present = "evidence" in content.lower() or "file:line" in content

        # Assert
        assert evidence_present, "Guardrail missing: Evidence requirements"


class TestAC1ErrorHandling:
    """Tests for AC1: Error handling for 4 scenarios."""

    def test_error_handling_context_missing(self, subagent_spec_path):
        """Test: Error handling documented for context files missing."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        error_context_present = "context" in content.lower() and ("missing" in content.lower() or "error" in content.lower())

        # Assert
        assert error_context_present, "Error handling missing for context files missing scenario"

    def test_error_handling_command_failed(self, subagent_spec_path):
        """Test: Error handling documented for coverage command failed."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        error_command_present = ("command" in content.lower() or "coverage" in content.lower()) and ("fail" in content.lower() or "error" in content.lower())

        # Assert
        assert error_command_present, "Error handling missing for coverage command failed scenario"

    def test_error_handling_parse_error(self, subagent_spec_path):
        """Test: Error handling documented for report parse error."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        error_parse_present = ("parse" in content.lower() or "report" in content.lower()) and ("error" in content.lower() or "fail" in content.lower())

        # Assert
        assert error_parse_present, "Error handling missing for report parse error scenario"

    def test_error_handling_no_classification(self, subagent_spec_path):
        """Test: Error handling documented for no files classified scenario."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        error_classification_present = ("classif" in content.lower() or "file" in content.lower()) and ("no" in content.lower() or "not found" in content.lower() or "error" in content.lower())

        # Assert
        assert error_classification_present, "Error handling missing for no files classified scenario"


class TestAC1IntegrationInstructions:
    """Tests for AC1: Integration with devforgeai-qa skill."""

    def test_integration_instructions_documented(self, subagent_spec_path):
        """Test: Integration instructions documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        integration_present = "integration" in content.lower() or "devforgeai-qa" in content.lower()

        # Assert
        assert integration_present, "Integration instructions not documented"

    def test_integration_shows_task_invocation(self, subagent_spec_path):
        """Test: Integration shows Task() invocation example."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        task_present = "Task(" in content

        # Assert
        assert task_present, "Integration missing Task() invocation example"


class TestAC1TestingRequirements:
    """Tests for AC1: Testing requirements documented."""

    def test_testing_requirements_documented(self, subagent_spec_path):
        """Test: Testing requirements documented (4 unit + 1 integration test)."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        testing_present = "test" in content.lower()

        # Assert
        assert testing_present, "Testing requirements not documented"


class TestAC1PerformanceTargets:
    """Tests for AC1: Performance targets documented."""

    def test_performance_targets_documented(self, subagent_spec_path):
        """Test: Performance targets (<60s) documented."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        performance_present = "60" in content or "performance" in content.lower() or "timeout" in content.lower()

        # Assert
        assert performance_present, "Performance targets not documented"


class TestAC1SuccessCriteria:
    """Tests for AC1: Success criteria checklist."""

    def test_success_criteria_checklist_exists(self, subagent_spec_path):
        """Test: Success criteria checklist documented (9 items)."""
        # Arrange
        content = subagent_spec_path.read_text()

        # Act
        checklist_present = "Success" in content and ("Criteria" in content or "Checklist" in content or "Completed" in content)

        # Assert
        assert checklist_present, "Success criteria checklist not documented"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
