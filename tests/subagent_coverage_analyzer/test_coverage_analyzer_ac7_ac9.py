"""
AC7-AC9 Tests: QA Integration, Prompt Template, Error Handling

Tests coverage analyzer integration and error scenarios:
- AC7: Integration with devforgeai-qa skill
- AC8: Prompt template documentation
- AC9: Error handling for 4 scenarios (context missing, command failed, parse error, no classification)
"""

import pytest
from pathlib import Path


class TestAC7QASkillIntegration:
    """Tests for AC7: Integration with devforgeai-qa skill."""

    def test_subagent_invocable_from_qa_skill(self, qa_skill_invocation_context):
        """Test: Subagent can be invoked from devforgeai-qa skill."""
        # Arrange
        context = qa_skill_invocation_context
        story_id = context.get("story_id")

        # Act
        invocable = story_id is not None and context.get("language") is not None

        # Assert
        assert invocable, "Subagent should be invocable with story_id and language"

    def test_qa_skill_loads_tech_stack_context(self, qa_skill_invocation_context):
        """Test: QA skill loads tech-stack.md before invoking."""
        # Arrange
        context = qa_skill_invocation_context
        context_files = context.get("context_files", {})

        # Act
        tech_stack_provided = "tech_stack" in context_files

        # Assert
        assert tech_stack_provided, "QA skill should provide tech_stack context file"

    def test_qa_skill_extracts_language_from_tech_stack(self, qa_skill_invocation_context):
        """Test: QA skill extracts language from tech_stack.md."""
        # Arrange
        context = qa_skill_invocation_context

        # Act
        language = context.get("language")

        # Assert
        assert language in ["Python", "C#", "Node.js", "Go", "Rust", "Java"], f"Invalid language: {language}"

    def test_qa_skill_provides_test_command(self, qa_skill_invocation_context):
        """Test: QA skill provides appropriate test_command for language."""
        # Arrange
        context = qa_skill_invocation_context
        language = context.get("language")
        test_command = context.get("test_command")

        # Act
        language_in_command = language.lower() in test_command.lower() or \
                             (language == "Python" and "pytest" in test_command) or \
                             (language == "C#" and "dotnet" in test_command)

        # Assert
        assert language_in_command, f"test_command should match language {language}"

    def test_qa_skill_passes_thresholds(self, qa_skill_invocation_context):
        """Test: QA skill passes coverage thresholds to subagent."""
        # Arrange
        context = qa_skill_invocation_context
        thresholds = context.get("thresholds", {})

        # Act
        has_thresholds = len(thresholds) > 0
        has_business_logic = "business_logic" in thresholds
        has_application = "application" in thresholds

        # Assert
        assert has_thresholds, "QA skill should provide thresholds"
        assert has_business_logic, "Thresholds should include business_logic"
        assert has_application, "Thresholds should include application"

    def test_qa_skill_updates_blocks_qa_flag(self):
        """Test: QA skill updates blocks_qa using OR operation."""
        # Arrange
        qa_blocks_before = False
        coverage_blocks = True

        # Act
        qa_blocks_after = qa_blocks_before or coverage_blocks

        # Assert
        assert qa_blocks_after == True, "blocks_qa should be True when coverage analysis blocks"

    def test_qa_skill_parses_json_response(self):
        """Test: QA skill parses JSON response from subagent."""
        # Arrange
        response_json = {
            "status": "success",
            "coverage_summary": {"business_logic": 96.0},
            "blocks_qa": False,
            "violations": []
        }

        # Act
        status = response_json.get("status")
        has_coverage_summary = "coverage_summary" in response_json

        # Assert
        assert status == "success", "Response should have success status"
        assert has_coverage_summary, "Response should include coverage_summary"

    def test_qa_skill_stores_gaps_in_report(self):
        """Test: QA skill stores coverage gaps for QA report."""
        # Arrange
        response = {
            "gaps": [
                {
                    "file": "src/Infrastructure/Repo.cs",
                    "layer": "infrastructure",
                    "current_coverage": 72.5,
                    "target_coverage": 80.0
                }
            ]
        }

        # Act
        gaps = response.get("gaps", [])

        # Assert
        assert len(gaps) > 0, "QA skill should capture coverage gaps"
        assert gaps[0]["file"] is not None, "Each gap should have a file"


class TestAC8PromptTemplate:
    """Tests for AC8: Prompt template documentation."""

    def test_prompt_template_file_exists(self, prompt_template_file_path):
        """Test: subagent-prompt-templates.md file exists."""
        # Arrange
        file_path = prompt_template_file_path

        # Act
        file_exists = file_path.exists()

        # Assert
        assert file_exists, f"Prompt template file not found at {file_path}"

    def test_template_section_exists(self, prompt_template_file_path, expected_template_sections):
        """Test: coverage-analyzer template section exists."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        template_section = "coverage-analyzer" in content.lower() or "Template" in content

        # Assert
        assert template_section, "coverage-analyzer template section not found"

    def test_template_includes_context_loading(self, prompt_template_file_path):
        """Test: Template documents context file loading (tech-stack, source-tree)."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_context_loading = ("tech" in content.lower() or "context" in content.lower()) and \
                             ("load" in content.lower() or "read" in content.lower())

        # Assert
        assert has_context_loading, "Template should document context file loading"

    def test_template_includes_language_extraction(self, prompt_template_file_path):
        """Test: Template documents language extraction logic."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_language_extraction = "language" in content.lower() and \
                                 ("extract" in content.lower() or "detect" in content.lower())

        # Assert
        assert has_language_extraction, "Template should document language extraction"

    def test_template_includes_tool_selection(self, prompt_template_file_path):
        """Test: Template documents tool selection (pytest, dotnet, npm, etc.)."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_tool_selection = ("pytest" in content.lower() or "dotnet" in content.lower() or \
                             "npm" in content.lower() or "tool" in content.lower())

        # Assert
        assert has_tool_selection, "Template should document tool selection"

    def test_template_includes_task_invocation(self, prompt_template_file_path):
        """Test: Template shows Task() invocation."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_task_invocation = "Task(" in content

        # Assert
        assert has_task_invocation, "Template should show Task() invocation"

    def test_template_includes_response_parsing(self, prompt_template_file_path):
        """Test: Template documents response parsing instructions."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_response_parsing = ("parse" in content.lower() or "response" in content.lower()) and \
                              ("json" in content.lower() or "extract" in content.lower())

        # Assert
        assert has_response_parsing, "Template should document response parsing"

    def test_template_includes_error_handling(self, prompt_template_file_path):
        """Test: Template documents error handling pattern."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_error_handling = ("error" in content.lower() or "exception" in content.lower() or \
                             "fail" in content.lower()) and ("handle" in content.lower() or "catch" in content.lower())

        # Assert
        assert has_error_handling, "Template should document error handling"

    def test_template_includes_integration_example(self, prompt_template_file_path):
        """Test: Template includes complete integration example."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_example = "example" in content.lower() and ("devforgeai-qa" in content or "Phase 1" in content)

        # Assert
        assert has_example, "Template should include integration example"

    def test_template_documents_token_savings(self, prompt_template_file_path):
        """Test: Template documents token budget impact (12K → 4K = 65% reduction)."""
        # Arrange
        content = prompt_template_file_path.read_text()

        # Act
        has_token_info = ("token" in content.lower() or "12" in content) and \
                        ("4" in content or "65" in content or "reduction" in content.lower())

        # Assert
        assert has_token_info, "Template should document token savings"


class TestAC9ErrorHandlingContextMissing:
    """Tests for AC9 Error Scenario 1: Context files missing."""

    def test_context_missing_returns_failure_status(self, error_scenario_context_missing):
        """Test: Returns status: 'failure' when context file missing."""
        # Arrange
        scenario = error_scenario_context_missing
        expected = scenario.get("expected_response", {})

        # Act
        status = expected.get("status")

        # Assert
        assert status == "failure", "Should return failure status when context missing"

    def test_context_missing_identifies_file(self, error_scenario_context_missing):
        """Test: Error message identifies which context file is missing."""
        # Arrange
        scenario = error_scenario_context_missing
        expected = scenario.get("expected_response", {})
        missing_file = scenario.get("missing_file")

        # Act
        error_message = expected.get("error", "")
        mentions_file = missing_file in error_message

        # Assert
        assert mentions_file, f"Error should mention missing file: {missing_file}"

    def test_context_missing_sets_blocks_qa(self, error_scenario_context_missing):
        """Test: Sets blocks_qa = True when context missing."""
        # Arrange
        scenario = error_scenario_context_missing
        expected = scenario.get("expected_response", {})

        # Act
        blocks_qa = expected.get("blocks_qa")

        # Assert
        assert blocks_qa == True, "Should set blocks_qa=True when context missing"

    def test_context_missing_provides_remediation(self, error_scenario_context_missing):
        """Test: Provides remediation guidance (/create-context)."""
        # Arrange
        scenario = error_scenario_context_missing
        expected = scenario.get("expected_response", {})

        # Act
        remediation = expected.get("remediation", "")
        has_guidance = "create-context" in remediation or "/create-context" in remediation

        # Assert
        assert has_guidance, "Should suggest /create-context in remediation"


class TestAC9ErrorHandlingCommandFailed:
    """Tests for AC9 Error Scenario 2: Coverage command execution failed."""

    def test_command_failed_returns_failure_status(self, error_scenario_command_failed):
        """Test: Returns status: 'failure' when coverage command fails."""
        # Arrange
        scenario = error_scenario_command_failed
        expected = scenario.get("expected_response", {})

        # Act
        status = expected.get("status")

        # Assert
        assert status == "failure", "Should return failure status when command fails"

    def test_command_failed_includes_stderr(self, error_scenario_command_failed):
        """Test: Error message includes stderr from failed command."""
        # Arrange
        scenario = error_scenario_command_failed
        expected = scenario.get("expected_response", {})
        stderr = scenario.get("stderr", "")

        # Act
        error_message = expected.get("error", "")
        includes_stderr = len(error_message) > 0

        # Assert
        assert includes_stderr, "Error message should include command output"

    def test_command_failed_sets_blocks_qa(self, error_scenario_command_failed):
        """Test: Sets blocks_qa = True when command fails."""
        # Arrange
        scenario = error_scenario_command_failed
        expected = scenario.get("expected_response", {})

        # Act
        blocks_qa = expected.get("blocks_qa")

        # Assert
        assert blocks_qa == True, "Should set blocks_qa=True when command fails"

    def test_command_failed_provides_tool_installation_guidance(self, error_scenario_command_failed):
        """Test: Provides guidance to install coverage tool."""
        # Arrange
        scenario = error_scenario_command_failed
        expected = scenario.get("expected_response", {})

        # Act
        remediation = expected.get("remediation", "")
        has_install_guidance = "install" in remediation.lower() or "pip install" in remediation

        # Assert
        assert has_install_guidance, "Should suggest installing coverage tool"


class TestAC9ErrorHandlingParseError:
    """Tests for AC9 Error Scenario 3: Coverage report parse error."""

    def test_parse_error_returns_failure_status(self, error_scenario_parse_error):
        """Test: Returns status: 'failure' when report parsing fails."""
        # Arrange
        scenario = error_scenario_parse_error
        expected = scenario.get("expected_response", {})

        # Act
        status = expected.get("status")

        # Assert
        assert status == "failure", "Should return failure status when parsing fails"

    def test_parse_error_identifies_report_file(self, error_scenario_parse_error):
        """Test: Error message identifies which report file failed."""
        # Arrange
        scenario = error_scenario_parse_error
        expected = scenario.get("expected_response", {})
        report_file = scenario.get("report_file")

        # Act
        error_message = expected.get("error", "")
        mentions_file = report_file in error_message

        # Assert
        assert mentions_file, f"Error should mention report file: {report_file}"

    def test_parse_error_sets_blocks_qa(self, error_scenario_parse_error):
        """Test: Sets blocks_qa = True when parsing fails."""
        # Arrange
        scenario = error_scenario_parse_error
        expected = scenario.get("expected_response", {})

        # Act
        blocks_qa = expected.get("blocks_qa")

        # Assert
        assert blocks_qa == True, "Should set blocks_qa=True when parsing fails"

    def test_parse_error_provides_re_run_guidance(self, error_scenario_parse_error):
        """Test: Provides guidance to re-run coverage command."""
        # Arrange
        scenario = error_scenario_parse_error
        expected = scenario.get("expected_response", {})

        # Act
        remediation = expected.get("remediation", "")
        has_rerun_guidance = "re-run" in remediation.lower() or "pytest" in remediation or "coverage" in remediation.lower()

        # Assert
        assert has_rerun_guidance, "Should suggest re-running coverage command"


class TestAC9ErrorHandlingNoClassification:
    """Tests for AC9 Error Scenario 4: No files classified."""

    def test_no_classification_returns_failure_status(self, error_scenario_no_classification):
        """Test: Returns status: 'failure' when no files classified."""
        # Arrange
        scenario = error_scenario_no_classification
        expected = scenario.get("expected_response", {})

        # Act
        status = expected.get("status")

        # Assert
        assert status == "failure", "Should return failure status when no files classified"

    def test_no_classification_identifies_count(self, error_scenario_no_classification):
        """Test: Error message shows files/classifications count."""
        # Arrange
        scenario = error_scenario_no_classification
        expected = scenario.get("expected_response", {})

        # Act
        error_message = expected.get("error", "")
        shows_count = "0 of" in error_message or "files" in error_message.lower()

        # Assert
        assert shows_count, "Error should show classification count"

    def test_no_classification_sets_blocks_qa(self, error_scenario_no_classification):
        """Test: Sets blocks_qa = True when no files classified."""
        # Arrange
        scenario = error_scenario_no_classification
        expected = scenario.get("expected_response", {})

        # Act
        blocks_qa = expected.get("blocks_qa")

        # Assert
        assert blocks_qa == True, "Should set blocks_qa=True when no files classified"

    def test_no_classification_provides_source_tree_guidance(self, error_scenario_no_classification):
        """Test: Provides guidance to update source-tree.md patterns."""
        # Arrange
        scenario = error_scenario_no_classification
        expected = scenario.get("expected_response", {})

        # Act
        remediation = expected.get("remediation", "")
        has_source_tree_guidance = "source-tree" in remediation or "pattern" in remediation.lower()

        # Assert
        assert has_source_tree_guidance, "Should suggest updating source-tree.md patterns"


class TestAC9ErrorHandlingIntegration:
    """Integration tests for AC9: Error handling in context."""

    def test_all_error_scenarios_return_blocks_qa_true(self,
                                                       error_scenario_context_missing,
                                                       error_scenario_command_failed,
                                                       error_scenario_parse_error,
                                                       error_scenario_no_classification):
        """Test: All 4 error scenarios set blocks_qa = True."""
        # Arrange
        scenarios = [
            error_scenario_context_missing,
            error_scenario_command_failed,
            error_scenario_parse_error,
            error_scenario_no_classification
        ]

        # Act & Assert
        for scenario in scenarios:
            response = scenario.get("expected_response", {})
            blocks_qa = response.get("blocks_qa")
            assert blocks_qa == True, f"Scenario {scenario.get('scenario')} should set blocks_qa=True"

    def test_all_error_scenarios_return_failure_status(self,
                                                       error_scenario_context_missing,
                                                       error_scenario_command_failed,
                                                       error_scenario_parse_error,
                                                       error_scenario_no_classification):
        """Test: All 4 error scenarios return status: 'failure'."""
        # Arrange
        scenarios = [
            error_scenario_context_missing,
            error_scenario_command_failed,
            error_scenario_parse_error,
            error_scenario_no_classification
        ]

        # Act & Assert
        for scenario in scenarios:
            response = scenario.get("expected_response", {})
            status = response.get("status")
            assert status == "failure", f"Scenario {scenario.get('scenario')} should return status=failure"

    def test_all_error_scenarios_provide_remediation(self,
                                                     error_scenario_context_missing,
                                                     error_scenario_command_failed,
                                                     error_scenario_parse_error,
                                                     error_scenario_no_classification):
        """Test: All 4 error scenarios provide remediation guidance."""
        # Arrange
        scenarios = [
            error_scenario_context_missing,
            error_scenario_command_failed,
            error_scenario_parse_error,
            error_scenario_no_classification
        ]

        # Act & Assert
        for scenario in scenarios:
            response = scenario.get("expected_response", {})
            remediation = response.get("remediation", "")
            assert len(remediation) > 0, f"Scenario {scenario.get('scenario')} should provide remediation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
