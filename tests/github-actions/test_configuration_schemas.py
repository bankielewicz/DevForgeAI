"""
Test Configuration Schema Validation for STORY-097

RED PHASE: Failing tests for configuration file schemas
Tests validate github-actions.yaml and ci-answers.yaml structures

Test Categories:
- Schema validation (required keys, types)
- YAML parsing
- Default values
- Value constraints
"""

import pytest
import yaml
from pathlib import Path


class TestGitHubActionsConfigSchema:
    """
    Given: github-actions.yaml configuration file
    When: Loading and validating schema
    Then: All required keys exist with correct types and default values
    """

    def test_github_actions_config_file_exists(self):
        """
        Scenario: Configuration file exists at expected location
        Given: Framework has devforgeai/config/ci/ directory
        When: Looking for github-actions.yaml.example
        Then: File should exist
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        assert config_path.exists(), f"Configuration file not found at {config_path}"

    def test_github_actions_config_valid_yaml(self):
        """
        Scenario: Configuration file contains valid YAML
        Given: github-actions.yaml.example file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        assert config is not None, "Failed to parse YAML or file is empty"

    def test_github_actions_config_has_required_keys(self):
        """
        Scenario: Configuration has all required keys
        Given: github-actions.yaml.example parsed
        When: Checking required keys
        Then: max_parallel_jobs, cost_optimization section exist
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert "max_parallel_jobs" in config, "Missing 'max_parallel_jobs' key"
        assert "cost_optimization" in config, "Missing 'cost_optimization' section"
        assert isinstance(config["cost_optimization"], dict), "cost_optimization must be dict"

    def test_github_actions_config_max_parallel_jobs_type(self):
        """
        Scenario: max_parallel_jobs is integer type
        Given: github-actions.yaml.example parsed
        When: Reading max_parallel_jobs value
        Then: Should be integer
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        max_jobs = config.get("max_parallel_jobs")
        assert isinstance(max_jobs, int), f"max_parallel_jobs must be int, got {type(max_jobs)}"

    def test_github_actions_config_max_parallel_jobs_default_5(self):
        """
        Scenario: max_parallel_jobs defaults to 5
        Given: github-actions.yaml.example
        When: Reading max_parallel_jobs
        Then: Should default to 5
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert config.get("max_parallel_jobs") == 5, "Default should be 5 jobs"

    def test_github_actions_cost_optimization_enable_prompt_caching(self):
        """
        Scenario: cost_optimization.enable_prompt_caching exists
        Given: github-actions.yaml.example
        When: Checking cost optimization keys
        Then: enable_prompt_caching should exist and be boolean
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        cost_opts = config.get("cost_optimization", {})
        assert "enable_prompt_caching" in cost_opts, "Missing enable_prompt_caching"
        assert isinstance(cost_opts["enable_prompt_caching"], bool), "Should be boolean"

    def test_github_actions_cost_optimization_enable_prompt_caching_true(self):
        """
        Scenario: Prompt caching enabled by default
        Given: github-actions.yaml.example
        When: Reading enable_prompt_caching
        Then: Should default to True
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        cost_opts = config.get("cost_optimization", {})
        assert cost_opts.get("enable_prompt_caching") is True, "Prompt caching should be enabled"

    def test_github_actions_cost_optimization_prefer_haiku(self):
        """
        Scenario: prefer_haiku option exists and defaults to True
        Given: github-actions.yaml.example
        When: Checking prefer_haiku setting
        Then: Should exist as boolean and default to True
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        cost_opts = config.get("cost_optimization", {})
        assert "prefer_haiku" in cost_opts, "Missing prefer_haiku"
        assert cost_opts.get("prefer_haiku") is True, "Haiku should be preferred"

    def test_github_actions_cost_optimization_max_cost_per_story(self):
        """
        Scenario: max_cost_per_story is numeric and defaults to 0.15
        Given: github-actions.yaml.example
        When: Checking cost limit
        Then: Should be numeric (float) and equal to 0.15
        """
        config_path = Path("devforgeai/config/ci/github-actions.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        cost_opts = config.get("cost_optimization", {})
        max_cost = cost_opts.get("max_cost_per_story")
        assert isinstance(max_cost, (int, float)), "max_cost_per_story must be numeric"
        assert max_cost == 0.15, f"Default cost should be 0.15, got {max_cost}"


class TestCIAnswersConfigSchema:
    """
    Given: ci-answers.yaml configuration file
    When: Loading and validating schema
    Then: All required keys exist with correct types and valid values
    """

    def test_ci_answers_config_file_exists(self):
        """
        Scenario: Configuration file exists
        Given: Framework has devforgeai/config/ci/ directory
        When: Looking for ci-answers.yaml.example
        Then: File should exist
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        assert config_path.exists(), f"Configuration file not found at {config_path}"

    def test_ci_answers_config_valid_yaml(self):
        """
        Scenario: Configuration file contains valid YAML
        Given: ci-answers.yaml.example file
        When: Parsing as YAML
        Then: Should parse without errors
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        assert config is not None, "Failed to parse YAML or file is empty"

    def test_ci_answers_config_has_required_keys(self):
        """
        Scenario: Configuration has all required answer keys
        Given: ci-answers.yaml.example parsed
        When: Checking required keys
        Then: test_failure_action, deferral_strategy, priority_default exist
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert "test_failure_action" in config, "Missing test_failure_action"
        assert "deferral_strategy" in config, "Missing deferral_strategy"
        assert "priority_default" in config, "Missing priority_default"

    def test_ci_answers_test_failure_action_type(self):
        """
        Scenario: test_failure_action is string
        Given: ci-answers.yaml.example parsed
        When: Reading test_failure_action
        Then: Should be string type
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert isinstance(config["test_failure_action"], str), "test_failure_action must be string"

    def test_ci_answers_test_failure_action_valid_value(self):
        """
        Scenario: test_failure_action has valid default value
        Given: ci-answers.yaml.example
        When: Reading test_failure_action
        Then: Should be 'fix-implementation' (fixing failed tests in CI)
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        valid_actions = ["fix-implementation", "halt", "defer"]
        assert config["test_failure_action"] in valid_actions, \
            f"test_failure_action must be one of {valid_actions}"

    def test_ci_answers_deferral_strategy_type(self):
        """
        Scenario: deferral_strategy is string
        Given: ci-answers.yaml.example parsed
        When: Reading deferral_strategy
        Then: Should be string type
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert isinstance(config["deferral_strategy"], str), "deferral_strategy must be string"

    def test_ci_answers_deferral_strategy_valid_value(self):
        """
        Scenario: deferral_strategy has valid value
        Given: ci-answers.yaml.example
        When: Reading deferral_strategy
        Then: Should default to 'never' (no autonomous deferrals in CI)
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        valid_strategies = ["never", "on-timeout", "on-critical-only"]
        assert config["deferral_strategy"] in valid_strategies, \
            f"deferral_strategy must be one of {valid_strategies}"

    def test_ci_answers_priority_default_type(self):
        """
        Scenario: priority_default is string
        Given: ci-answers.yaml.example parsed
        When: Reading priority_default
        Then: Should be string type
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        assert isinstance(config["priority_default"], str), "priority_default must be string"

    def test_ci_answers_priority_default_valid_value(self):
        """
        Scenario: priority_default has valid value
        Given: ci-answers.yaml.example
        When: Reading priority_default
        Then: Should be one of: high, medium, low
        """
        config_path = Path("devforgeai/config/ci/ci-answers.yaml.example")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        valid_priorities = ["high", "medium", "low"]
        assert config["priority_default"] in valid_priorities, \
            f"priority_default must be one of {valid_priorities}"


class TestConfigurationValidation:
    """
    Integration tests for configuration validation
    """

    def test_both_config_files_exist(self):
        """
        Scenario: Both required config files exist
        Given: Framework setup
        When: Checking for config files
        Then: Both github-actions.yaml.example and ci-answers.yaml.example exist
        """
        github_config = Path("devforgeai/config/ci/github-actions.yaml.example")
        ci_answers = Path("devforgeai/config/ci/ci-answers.yaml.example")

        assert github_config.exists(), "github-actions.yaml.example missing"
        assert ci_answers.exists(), "ci-answers.yaml.example missing"

    def test_config_files_are_readable(self):
        """
        Scenario: Config files can be read
        Given: Config files exist
        When: Opening for reading
        Then: Should open without permission errors
        """
        github_config = Path("devforgeai/config/ci/github-actions.yaml.example")
        ci_answers = Path("devforgeai/config/ci/ci-answers.yaml.example")

        with open(github_config, 'r') as f:
            assert f.readable(), "github-actions.yaml.example not readable"

        with open(ci_answers, 'r') as f:
            assert f.readable(), "ci-answers.yaml.example not readable"

    def test_config_files_not_empty(self):
        """
        Scenario: Config files contain content
        Given: Config files exist
        When: Reading content
        Then: Should not be empty
        """
        github_config = Path("devforgeai/config/ci/github-actions.yaml.example")
        ci_answers = Path("devforgeai/config/ci/ci-answers.yaml.example")

        assert github_config.stat().st_size > 0, "github-actions.yaml.example is empty"
        assert ci_answers.stat().st_size > 0, "ci-answers.yaml.example is empty"
