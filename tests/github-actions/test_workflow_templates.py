"""
Test Workflow Template Generation for STORY-097

RED PHASE: Failing tests for GitHub Actions workflow templates
Tests validate AC#1, AC#2, AC#3, AC#5

Test Categories:
- Workflow file existence
- YAML schema validation
- Trigger configuration
- Input validation
- Matrix strategy
- Job naming and structure
"""

import pytest
import yaml
from pathlib import Path


class TestDevStoryWorkflow:
    """
    AC#1: Automated /dev Execution Workflow
    Given: dev-story.yml workflow exists
    When: Parsing workflow
    Then: Has workflow_dispatch trigger, story_id input, runs /dev command
    """

    def test_dev_story_workflow_file_exists(self):
        """
        Scenario: Workflow template exists
        Given: .github/workflows directory
        When: Looking for dev-story.yml
        Then: File should exist
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        assert workflow_path.exists(), f"Workflow not found at {workflow_path}"

    def test_dev_story_workflow_valid_yaml(self):
        """
        Scenario: Workflow contains valid YAML
        Given: dev-story.yml file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        assert workflow is not None, "Failed to parse workflow YAML"

    def test_dev_story_workflow_has_name(self):
        """
        Scenario: Workflow has descriptive name
        Given: dev-story.yml parsed
        When: Checking name field
        Then: Should have meaningful name
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        assert "name" in workflow, "Workflow must have 'name' field"
        assert "Dev" in workflow["name"] or "dev" in workflow["name"], \
            "Workflow name should indicate dev execution"

    def test_dev_story_workflow_dispatch_trigger(self):
        """
        Scenario: Workflow has workflow_dispatch trigger
        Given: dev-story.yml parsed
        When: Checking triggers
        Then: Should have workflow_dispatch trigger for manual execution
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        assert "on" in workflow, "Workflow must have 'on' (triggers) section"
        assert "workflow_dispatch" in workflow["on"], \
            "Must have workflow_dispatch trigger"

    def test_dev_story_workflow_dispatch_has_story_id_input(self):
        """
        Scenario: workflow_dispatch trigger has story_id input
        Given: dev-story.yml with workflow_dispatch
        When: Checking inputs
        Then: Should have story_id input parameter
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        dispatch_inputs = workflow.get("on", {}).get("workflow_dispatch", {}).get("inputs", {})
        assert "story_id" in dispatch_inputs, "Must have story_id input"

    def test_dev_story_workflow_story_id_input_required(self):
        """
        Scenario: story_id input is required
        Given: dev-story.yml workflow_dispatch inputs
        When: Checking story_id configuration
        Then: Should be marked as required
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        story_id_input = workflow.get("on", {}).get("workflow_dispatch", {}).get("inputs", {}).get("story_id", {})
        assert story_id_input.get("required") is True, "story_id should be required"

    def test_dev_story_workflow_has_jobs_section(self):
        """
        Scenario: Workflow has jobs section
        Given: dev-story.yml parsed
        When: Checking jobs
        Then: Should have at least one job defined
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        assert "jobs" in workflow, "Workflow must have 'jobs' section"
        assert len(workflow["jobs"]) > 0, "Workflow must define at least one job"

    def test_dev_story_workflow_has_dev_job(self):
        """
        Scenario: Workflow has job to run /dev command
        Given: dev-story.yml jobs
        When: Checking job names
        Then: Should have job for development execution
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        job_names = list(workflow.get("jobs", {}).keys())
        assert len(job_names) > 0, "Must define at least one job"
        # Job could be named 'dev', 'run-dev', 'execute-dev', etc.
        assert any("dev" in name.lower() for name in job_names), \
            f"Must have dev-related job, found: {job_names}"

    def test_dev_story_workflow_runs_claude_dev_command(self):
        """
        Scenario: Workflow runs claude -p "/dev $story_id" command
        Given: dev-story.yml job steps
        When: Searching for Claude command execution
        Then: Should contain headless Claude Code execution
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        jobs = workflow.get("jobs", {})
        found_dev_command = False

        for job_name, job_config in jobs.items():
            steps = job_config.get("steps", [])
            for step in steps:
                step_run = step.get("run", "") or ""
                if "claude" in step_run.lower() and "/dev" in step_run:
                    found_dev_command = True
                    # Verify it uses inputs.story_id
                    assert "inputs.story_id" in step_run or "${{inputs.story_id}}" in step_run, \
                        "Command must reference inputs.story_id"

        assert found_dev_command, "Workflow must run 'claude -p \"/dev ${{inputs.story_id}}\"' command"

    def test_dev_story_workflow_headless_mode(self):
        """
        Scenario: Workflow runs Claude Code in headless mode
        Given: dev-story.yml job steps
        When: Checking Claude invocation
        Then: Should use -p (prompt) flag for headless mode
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        found_headless = False
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                step_run = step.get("run", "") or ""
                if "claude" in step_run.lower() and "-p" in step_run:
                    found_headless = True

        assert found_headless, "Workflow must use 'claude -p' for headless mode"

    def test_dev_story_workflow_uploads_artifacts(self):
        """
        Scenario: Workflow uploads test results and artifacts
        Given: dev-story.yml job steps
        When: Checking for artifact upload
        Then: Should upload test results, coverage, story file
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        found_upload = False
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                action = step.get("uses", "") or ""
                if "upload-artifact" in action.lower() or "upload" in action.lower():
                    found_upload = True

        assert found_upload, "Workflow must upload artifacts"

    def test_dev_story_workflow_artifact_includes_test_results(self):
        """
        Scenario: Uploaded artifacts include test results
        Given: dev-story.yml artifact upload step
        When: Checking artifact configuration
        Then: Should include test results
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                action = step.get("uses", "") or ""
                if "upload-artifact" in action.lower():
                    path = step.get("with", {}).get("path", "") or ""
                    if path:
                        # Should include test results
                        assert any(pattern in path.lower() for pattern in ["test", "result"]), \
                            "Artifact path should include test results"


class TestQAValidationWorkflow:
    """
    AC#2: PR Quality Gate Workflow
    Given: qa-validation.yml workflow exists
    When: PR is opened
    Then: Extracts story ID and runs /qa deep
    """

    def test_qa_validation_workflow_file_exists(self):
        """
        Scenario: QA validation workflow template exists
        Given: .github/workflows directory
        When: Looking for qa-validation.yml
        Then: File should exist
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        assert workflow_path.exists(), f"Workflow not found at {workflow_path}"

    def test_qa_validation_workflow_valid_yaml(self):
        """
        Scenario: Workflow contains valid YAML
        Given: qa-validation.yml file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        assert workflow is not None, "Failed to parse workflow YAML"

    def test_qa_validation_workflow_triggers_on_pull_request(self):
        """
        Scenario: Workflow triggers on pull request
        Given: qa-validation.yml parsed
        When: Checking triggers
        Then: Should have pull_request trigger for opened, synchronize
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        triggers = workflow.get("on", {})
        assert "pull_request" in triggers, "Must trigger on pull_request"

    def test_qa_validation_workflow_extracts_story_id_from_pr_title(self):
        """
        Scenario: Workflow extracts story ID from PR title
        Given: qa-validation.yml job steps
        When: Searching for story ID extraction
        Then: Should parse title with regex pattern [STORY-NNN]
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        found_extraction = False
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                step_text = str(step)
                if any(pattern in step_text.lower() for pattern in ["story", "title", "extract", "grep"]):
                    if "STORY" in step_text:
                        found_extraction = True

        assert found_extraction, "Must extract story ID from PR title"

    def test_qa_validation_workflow_runs_qa_deep(self):
        """
        Scenario: Workflow runs /qa deep command
        Given: qa-validation.yml job steps
        When: Searching for QA command
        Then: Should run claude -p "/qa deep"
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        found_qa_command = False
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                step_run = step.get("run", "") or ""
                if "claude" in step_run.lower() and "/qa" in step_run and "deep" in step_run:
                    found_qa_command = True

        assert found_qa_command, "Workflow must run 'claude -p \"/qa deep\"' command"

    def test_qa_validation_workflow_blocks_merge_on_failure(self):
        """
        Scenario: Workflow blocks merge if QA fails
        Given: qa-validation.yml job configuration
        When: Checking job failure handling
        Then: Should require successful completion (no continue-on-error)
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        # Check that steps don't have continue-on-error or that required checks are configured
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                # If this is the QA step, it should not continue on error
                if "/qa" in str(step.get("run", "")):
                    assert step.get("continue-on-error") is not True, \
                        "QA step must not continue on error (must block merge)"


class TestParallelStoriesWorkflow:
    """
    AC#3: Matrix Parallel Execution
    Given: parallel-stories.yml workflow exists
    When: Triggered with story_ids array
    Then: Uses matrix strategy, max 5 concurrent jobs
    """

    def test_parallel_stories_workflow_file_exists(self):
        """
        Scenario: Parallel stories workflow template exists
        Given: .github/workflows directory
        When: Looking for parallel-stories.yml
        Then: File should exist
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        assert workflow_path.exists(), f"Workflow not found at {workflow_path}"

    def test_parallel_stories_workflow_valid_yaml(self):
        """
        Scenario: Workflow contains valid YAML
        Given: parallel-stories.yml file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        assert workflow is not None, "Failed to parse workflow YAML"

    def test_parallel_stories_workflow_dispatch_trigger(self):
        """
        Scenario: Workflow has workflow_dispatch trigger
        Given: parallel-stories.yml parsed
        When: Checking triggers
        Then: Should support manual execution
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        assert "workflow_dispatch" in workflow.get("on", {}), \
            "Must have workflow_dispatch trigger"

    def test_parallel_stories_workflow_has_story_ids_input(self):
        """
        Scenario: Workflow has story_ids input
        Given: parallel-stories.yml workflow_dispatch
        When: Checking inputs
        Then: Should have story_ids input (array)
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        inputs = workflow.get("on", {}).get("workflow_dispatch", {}).get("inputs", {})
        assert "story_ids" in inputs, "Must have story_ids input"

    def test_parallel_stories_workflow_uses_matrix_strategy(self):
        """
        Scenario: Workflow uses matrix strategy for parallel execution
        Given: parallel-stories.yml jobs
        When: Checking job configuration
        Then: Should have strategy.matrix with story_id
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        jobs = workflow.get("jobs", {})
        found_matrix = False

        for job in jobs.values():
            strategy = job.get("strategy", {})
            matrix = strategy.get("matrix", {})
            if "story_id" in matrix or "story" in str(matrix).lower():
                found_matrix = True

        assert found_matrix, "Must use matrix strategy with story_id"

    def test_parallel_stories_workflow_max_parallel_5(self):
        """
        Scenario: Workflow limits parallel jobs to 5
        Given: parallel-stories.yml strategy
        When: Checking max-parallel
        Then: Should have max-parallel: 5
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        for job in workflow.get("jobs", {}).values():
            strategy = job.get("strategy", {})
            max_parallel = strategy.get("max-parallel")
            if max_parallel is not None:
                assert max_parallel == 5, f"max-parallel should be 5, got {max_parallel}"

    def test_parallel_stories_workflow_fail_fast_false(self):
        """
        Scenario: Workflow continues on job failure
        Given: parallel-stories.yml strategy
        When: Checking fail-fast
        Then: Should have fail-fast: false to continue on failures
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        for job in workflow.get("jobs", {}).values():
            strategy = job.get("strategy", {})
            fail_fast = strategy.get("fail-fast")
            if fail_fast is not None:
                assert fail_fast is False, "fail-fast should be false to continue on failures"


class TestInstallerTestingWorkflow:
    """
    AC#5: Configuration Setup Command (installer-testing.yml)
    Tests that workflow template is created for installer testing
    """

    def test_installer_testing_workflow_file_exists(self):
        """
        Scenario: Installer testing workflow template exists
        Given: .github/workflows directory
        When: Looking for installer-testing.yml
        Then: File should exist
        """
        workflow_path = Path(".github/workflows/installer-testing.yml")
        assert workflow_path.exists(), f"Workflow not found at {workflow_path}"

    def test_installer_testing_workflow_valid_yaml(self):
        """
        Scenario: Workflow contains valid YAML
        Given: installer-testing.yml file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        workflow_path = Path(".github/workflows/installer-testing.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        assert workflow is not None, "Failed to parse workflow YAML"

    def test_installer_testing_workflow_has_meaningful_name(self):
        """
        Scenario: Workflow has descriptive name
        Given: installer-testing.yml parsed
        When: Checking name
        Then: Should indicate installer testing purpose
        """
        workflow_path = Path(".github/workflows/installer-testing.yml")
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        assert "name" in workflow, "Workflow must have name"
        name = workflow["name"].lower()
        assert any(word in name for word in ["installer", "test", "validation"]), \
            "Name should indicate installer testing"
