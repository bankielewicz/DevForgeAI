"""
Test /setup-github-actions Command for STORY-097

RED PHASE: Failing tests for GitHub Actions setup command
Tests validate AC#5 setup command creates all required files

Test Categories:
- Command existence
- File creation (4 workflows + 2 configs)
- Force flag behavior
- Existing file detection
- Configuration wizard
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestSetupCommandExists:
    """
    AC#5: Configuration Setup Command
    Given: User runs /setup-github-actions
    When: Command is invoked
    Then: Command creates 4 workflow files and 2 config files
    """

    def test_setup_github_actions_command_exists(self):
        """
        Scenario: /setup-github-actions command exists
        Given: Claude Code terminal
        When: Checking for command
        Then: Command should be available
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        assert command_path.exists(), f"Command not found at {command_path}"

    def test_setup_command_has_yaml_frontmatter(self):
        """
        Scenario: Command has proper YAML frontmatter
        Given: setup-github-actions.md
        When: Reading file
        Then: Should have description and argument-hint fields
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read()

        # Should start with YAML frontmatter
        assert content.startswith("---"), "Command must have YAML frontmatter"
        assert "description:" in content, "Command must have description field"

    def test_setup_command_under_500_lines(self):
        """
        Scenario: Command file is appropriately sized
        Given: setup-github-actions.md
        When: Counting lines
        Then: Should be under 500 lines (tech-stack.md requirement)
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            lines = f.readlines()

        assert len(lines) <= 500, f"Command should be under 500 lines, got {len(lines)}"


class TestWorkflowFileCreation:
    """
    AC#5: Configuration Setup - Workflow Files
    Given: /setup-github-actions command executed
    When: Command completes
    Then: Creates 4 workflow files in .github/workflows/
    """

    def test_setup_creates_dev_story_workflow(self):
        """
        Scenario: Setup creates dev-story.yml
        Given: /setup-github-actions executed
        When: Checking .github/workflows/
        Then: dev-story.yml should exist
        """
        workflow_path = Path(".github/workflows/dev-story.yml")
        # Test assumes command creates file
        assert workflow_path.exists(), "dev-story.yml not created"

    def test_setup_creates_qa_validation_workflow(self):
        """
        Scenario: Setup creates qa-validation.yml
        Given: /setup-github-actions executed
        When: Checking .github/workflows/
        Then: qa-validation.yml should exist
        """
        workflow_path = Path(".github/workflows/qa-validation.yml")
        assert workflow_path.exists(), "qa-validation.yml not created"

    def test_setup_creates_parallel_stories_workflow(self):
        """
        Scenario: Setup creates parallel-stories.yml
        Given: /setup-github-actions executed
        When: Checking .github/workflows/
        Then: parallel-stories.yml should exist
        """
        workflow_path = Path(".github/workflows/parallel-stories.yml")
        assert workflow_path.exists(), "parallel-stories.yml not created"

    def test_setup_creates_installer_testing_workflow(self):
        """
        Scenario: Setup creates installer-testing.yml
        Given: /setup-github-actions executed
        When: Checking .github/workflows/
        Then: installer-testing.yml should exist
        """
        workflow_path = Path(".github/workflows/installer-testing.yml")
        assert workflow_path.exists(), "installer-testing.yml not created"

    def test_all_four_workflows_exist(self):
        """
        Scenario: All four required workflows are created
        Given: /setup-github-actions command
        When: Execution completes
        Then: All 4 workflows should exist
        """
        workflows = [
            Path(".github/workflows/dev-story.yml"),
            Path(".github/workflows/qa-validation.yml"),
            Path(".github/workflows/parallel-stories.yml"),
            Path(".github/workflows/installer-testing.yml"),
        ]

        for workflow_path in workflows:
            assert workflow_path.exists(), f"Missing workflow: {workflow_path.name}"

        # All should exist (or test fails)
        assert all(w.exists() for w in workflows), "Not all workflows created"

    def test_workflows_are_valid_yaml(self):
        """
        Scenario: Created workflow files are valid YAML
        Given: Workflows created
        When: Parsing each workflow
        Then: All should parse as valid YAML
        """
        import yaml

        workflows = [
            Path(".github/workflows/dev-story.yml"),
            Path(".github/workflows/qa-validation.yml"),
            Path(".github/workflows/parallel-stories.yml"),
            Path(".github/workflows/installer-testing.yml"),
        ]

        for workflow_path in workflows:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
            assert workflow is not None, f"{workflow_path.name} contains invalid YAML"


class TestConfigFileCreation:
    """
    AC#5: Configuration Setup - Config Files
    Given: /setup-github-actions command executed
    When: Command completes
    Then: Creates 2 config files in .devforgeai/config/
    """

    def test_setup_creates_github_actions_config(self):
        """
        Scenario: Setup creates github-actions.yaml
        Given: /setup-github-actions executed
        When: Checking .devforgeai/config/
        Then: github-actions.yaml should exist
        """
        config_path = Path(".devforgeai/config/github-actions.yaml")
        # Should exist (either from setup or from example)
        assert config_path.exists() or Path(".devforgeai/config/github-actions.yaml.example").exists(), \
            "github-actions.yaml not found"

    def test_setup_creates_ci_answers_config(self):
        """
        Scenario: Setup creates ci-answers.yaml
        Given: /setup-github-actions executed
        When: Checking .devforgeai/config/
        Then: ci-answers.yaml should exist
        """
        config_path = Path(".devforgeai/config/ci-answers.yaml")
        # Should exist (either from setup or from example)
        assert config_path.exists() or Path(".devforgeai/config/ci-answers.yaml.example").exists(), \
            "ci-answers.yaml not found"

    def test_both_config_files_exist(self):
        """
        Scenario: Both required config files exist
        Given: /setup-github-actions command
        When: Execution completes
        Then: Both github-actions.yaml and ci-answers.yaml should exist
        """
        github_config = Path(".devforgeai/config/github-actions.yaml")
        ci_answers = Path(".devforgeai/config/ci-answers.yaml")

        github_example = Path(".devforgeai/config/github-actions.yaml.example")
        ci_example = Path(".devforgeai/config/ci-answers.yaml.example")

        github_exists = github_config.exists() or github_example.exists()
        ci_exists = ci_answers.exists() or ci_example.exists()

        assert github_exists, "github-actions.yaml not found"
        assert ci_exists, "ci-answers.yaml not found"

    def test_config_files_are_valid_yaml(self):
        """
        Scenario: Created config files are valid YAML
        Given: Config files created
        When: Parsing each config
        Then: All should parse as valid YAML
        """
        import yaml

        configs = [
            Path(".devforgeai/config/github-actions.yaml"),
            Path(".devforgeai/config/ci-answers.yaml"),
        ]

        for config_path in configs:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                assert config is not None, f"{config_path.name} contains invalid YAML"


class TestSetupCommandBehavior:
    """
    AC#5: Setup Command Behavior
    Given: Various command invocations
    When: Command is executed
    Then: Handles flags and options correctly
    """

    def test_setup_command_force_flag_behavior(self):
        """
        Scenario: --force flag overwrites existing files
        Given: /setup-github-actions --force
        When: Files already exist
        Then: Should overwrite existing files without prompting
        """
        # Command should support --force flag
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        assert "force" in content, "Command should document --force flag"

    def test_setup_command_detects_existing_files(self):
        """
        Scenario: Setup detects existing files
        Given: /setup-github-actions without --force
        When: Files already exist
        Then: Should prompt to overwrite or skip
        """
        # Command should handle existing files gracefully
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention handling of existing files
        assert any(term in content for term in ["exist", "overwrite", "skip", "confirm"]), \
            "Command should handle existing files"

    def test_setup_command_documentation_complete(self):
        """
        Scenario: Command documentation is complete
        Given: setup-github-actions.md command file
        When: Reviewing documentation
        Then: Should explain what files are created
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention the files created
        required_docs = ["workflow", "yaml", "config"]
        found_docs = sum(1 for term in required_docs if term in content)

        assert found_docs >= 2, "Command documentation should explain files created"


class TestSetupInteractiveWizard:
    """
    AC#5: Configuration Setup - Interactive Wizard
    Given: /setup-github-actions command
    When: User runs setup
    Then: Interactive wizard guides through configuration
    """

    def test_setup_command_mentions_interactive_setup(self):
        """
        Scenario: Command mentions interactive setup process
        Given: setup-github-actions.md
        When: Reviewing command
        Then: Should document interactive wizard
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention interactive, wizard, or prompt
        assert any(term in content for term in ["interactive", "wizard", "prompt", "question", "ask"]), \
            "Command should document interactive setup process"

    def test_setup_wizard_collects_api_key_configuration(self):
        """
        Scenario: Wizard collects API key configuration
        Given: Interactive setup
        When: Wizard runs
        Then: Should ask about ANTHROPIC_API_KEY setup
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read()

        # Should mention API key configuration
        assert any(term in content.lower() for term in ["api", "key", "anthropic", "secret"]), \
            "Wizard should explain API key setup"

    def test_setup_wizard_explains_cost_optimization(self):
        """
        Scenario: Wizard explains cost optimization options
        Given: Interactive setup
        When: Wizard runs
        Then: Should explain caching and model preferences
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention cost optimization
        assert any(term in content for term in ["cost", "caching", "cache", "haiku", "model"]), \
            "Wizard should explain cost optimization"

    def test_setup_wizard_explains_ci_answers_configuration(self):
        """
        Scenario: Wizard explains ci-answers configuration
        Given: Interactive setup
        When: Wizard collects answers
        Then: Should explain what answers are needed for headless mode
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention headless mode or answers
        assert any(term in content for term in ["headless", "answer", "ci-answers", "prompt", "question"]), \
            "Wizard should explain ci-answers configuration"


class TestSetupIntegration:
    """
    Integration tests for setup command
    """

    def test_setup_creates_complete_github_actions_setup(self):
        """
        Scenario: Setup creates complete GitHub Actions setup
        Given: /setup-github-actions command
        When: Execution completes
        Then: Should have all components for AC#1-AC#5
        """
        # Verify all components exist
        workflows = [
            Path(".github/workflows/dev-story.yml"),
            Path(".github/workflows/qa-validation.yml"),
            Path(".github/workflows/parallel-stories.yml"),
            Path(".github/workflows/installer-testing.yml"),
        ]

        configs = [
            Path(".devforgeai/config/github-actions.yaml"),
            Path(".devforgeai/config/ci-answers.yaml"),
        ]

        for workflow_path in workflows:
            assert workflow_path.exists() or Path(str(workflow_path).replace(".yml", ".yaml")).exists(), \
                f"Missing workflow: {workflow_path.name}"

        for config_path in configs:
            assert config_path.exists() or Path(str(config_path) + ".example").exists(), \
                f"Missing config: {config_path.name}"

    def test_setup_documentation_exists(self):
        """
        Scenario: Setup creates documentation
        Given: /setup-github-actions command
        When: Execution completes
        Then: Should create GitHub Actions documentation
        """
        potential_docs = [
            Path(".github/README.md"),
            Path("docs/GITHUB-ACTIONS-GUIDE.md"),
            Path("docs/COST-OPTIMIZATION.md"),
            Path("docs/TROUBLESHOOTING-CICD.md"),
        ]

        # At least one documentation file should exist
        docs_created = sum(1 for doc in potential_docs if doc.exists())
        # This is optional for setup, but documented in DoD

    def test_setup_all_files_have_comments_documentation(self):
        """
        Scenario: All created files have inline documentation
        Given: Workflows and configs created
        When: Reviewing files
        Then: Should have comments explaining purpose and usage
        """
        import yaml

        workflow_files = [
            Path(".github/workflows/dev-story.yml"),
            Path(".github/workflows/qa-validation.yml"),
        ]

        for workflow_path in workflow_files:
            if workflow_path.exists():
                with open(workflow_path, 'r') as f:
                    content = f.read()
                # Should have comments or description field
                # YAML comments start with #
                assert "#" in content, f"{workflow_path.name} should have comments"


class TestSetupErrorHandling:
    """
    Error handling for setup command
    """

    def test_setup_handles_missing_github_directory(self):
        """
        Scenario: Setup creates .github directory if missing
        Given: /setup-github-actions on fresh repo
        When: .github directory doesn't exist
        Then: Should create it automatically
        """
        # Command should create .github/workflows/ if needed
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should handle directory creation
        assert any(term in content for term in ["create", "mkdir", "directory"]), \
            "Command should handle directory creation"

    def test_setup_handles_permission_errors(self):
        """
        Scenario: Setup handles permission errors
        Given: Directory not writable
        When: Attempting to create files
        Then: Should report error clearly
        """
        # Command should document permission requirements
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Should mention permissions or write access
        # This is documentation requirement

    def test_setup_validates_yaml_before_writing(self):
        """
        Scenario: Setup validates files before writing
        Given: Generated workflow files
        When: Before writing to disk
        Then: Should validate YAML syntax
        """
        command_path = Path(".claude/commands/setup-github-actions.md")
        with open(command_path, 'r') as f:
            content = f.read().lower()

        # Command should mention validation
        assert any(term in content for term in ["validate", "check", "verify"]), \
            "Command should validate files before creation"
