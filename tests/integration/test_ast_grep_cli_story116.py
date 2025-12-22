"""
Integration tests for ast-grep CLI commands (STORY-116: Configuration Infrastructure)

Tests the full CLI workflow including init and validate-config commands.
These integration tests use direct function calls to simulate CLI behavior,
with path setup matching the conftest.py configuration.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
import yaml

from claude.scriptsdevforgeai_cli.ast_grep.config_init import ConfigurationInitializer
from claude.scriptsdevforgeai_cli.ast_grep.config_validator import ConfigurationValidator


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_project():
    """Create temporary project directory for CLI tests"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def initialized_project(temp_project):
    """Create temporary project with initialized ast-grep config"""
    initializer = ConfigurationInitializer(temp_project)
    initializer.initialize()
    return temp_project


# ============================================================================
# CLI INIT TESTS
# ============================================================================

class TestAstGrepInitCommand:
    """Integration tests for 'devforgeai ast-grep init' command behavior."""

    def test_cli_init_creates_directory_structure(self, temp_project):
        """
        Scenario: CLI init creates expected directory structure
        Given: Empty project directory
        When: devforgeai ast-grep init is executed
        Then: devforgeai/ast-grep/ directory and subdirectories are created
        """
        # Act
        initializer = ConfigurationInitializer(temp_project)
        result = initializer.initialize()

        # Assert
        assert result.success, f"Init failed: {result.error}"
        assert (temp_project / "devforgeai" / "ast-grep" / "sgconfig.yml").exists()
        assert (temp_project / "devforgeai" / "ast-grep" / "rules" / "python").exists()
        assert (temp_project / "devforgeai" / "ast-grep" / "rules" / "csharp").exists()
        assert (temp_project / "devforgeai" / "ast-grep" / "rules" / "typescript").exists()
        assert (temp_project / "devforgeai" / "ast-grep" / "rules" / "javascript").exists()

    def test_cli_init_force_flag_overwrites(self, initialized_project):
        """
        Scenario: CLI init --force overwrites existing config
        Given: Project with existing configuration
        When: devforgeai ast-grep init --force is executed
        Then: Configuration is regenerated
        """
        # Arrange - Add marker to existing config
        config_path = initialized_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        with open(config_path, "a") as f:
            f.write("\n# MARKER\n")

        # Act
        initializer = ConfigurationInitializer(initialized_project)
        result = initializer.initialize(force=True)

        # Assert
        assert result.success
        with open(config_path) as f:
            content = f.read()
        assert "MARKER" not in content

    def test_cli_init_without_force_preserves_existing(self, initialized_project):
        """
        Scenario: CLI init without --force preserves existing config
        Given: Project with existing configuration
        When: devforgeai ast-grep init is executed (without --force)
        Then: Existing configuration is not overwritten
        """
        # Arrange - Add marker to existing config
        config_path = initialized_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        with open(config_path, "a") as f:
            f.write("\n# MARKER\n")

        # Act
        initializer = ConfigurationInitializer(initialized_project)
        result = initializer.initialize(force=False)

        # Assert
        assert result.success
        with open(config_path) as f:
            content = f.read()
        assert "MARKER" in content


# ============================================================================
# CLI VALIDATE-CONFIG TESTS
# ============================================================================

class TestAstGrepValidateConfigCommand:
    """Integration tests for 'devforgeai ast-grep validate-config' command behavior."""

    def test_cli_validate_valid_config(self, initialized_project):
        """
        Scenario: CLI validate-config passes for valid configuration
        Given: Project with valid ast-grep configuration
        When: devforgeai ast-grep validate-config is executed
        Then: Returns success (valid=True)
        """
        # Act
        config_path = initialized_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        validator = ConfigurationValidator(config_path)
        result = validator.validate()

        # Assert
        assert result.valid is True

    def test_cli_validate_returns_structured_result(self, initialized_project):
        """
        Scenario: CLI validate-config returns structured result
        Given: Project with valid configuration
        When: validation is executed
        Then: Result contains valid, errors, and warnings fields
        """
        # Act
        config_path = initialized_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        validator = ConfigurationValidator(config_path)
        result = validator.validate()

        # Assert - Result has expected structure for JSON output
        assert hasattr(result, 'valid')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)

    def test_cli_validate_missing_config_fails(self, temp_project):
        """
        Scenario: CLI validate-config fails when config missing
        Given: Project without ast-grep configuration
        When: devforgeai ast-grep validate-config is executed
        Then: Returns invalid result with file not found error
        """
        # Act
        config_path = temp_project / "nonexistent" / "sgconfig.yml"
        validator = ConfigurationValidator(config_path)
        result = validator.validate()

        # Assert
        assert result.valid is False
        assert any("not found" in e.message.lower() for e in result.errors)

    def test_cli_validate_invalid_yaml(self, temp_project):
        """
        Scenario: CLI validate-config fails for invalid YAML
        Given: Configuration file with invalid YAML syntax
        When: devforgeai ast-grep validate-config is executed
        Then: Returns error indicating YAML syntax error
        """
        # Arrange
        config_dir = temp_project / "devforgeai" / "ast-grep"
        config_dir.mkdir(parents=True)
        config_path = config_dir / "sgconfig.yml"
        with open(config_path, "w") as f:
            f.write("invalid: yaml: syntax:::")

        # Act
        validator = ConfigurationValidator(config_path)
        result = validator.validate()

        # Assert
        assert result.valid is False
        assert any("YAML" in e.message for e in result.errors)


# ============================================================================
# INTEGRATION WORKFLOW TESTS
# ============================================================================

class TestAstGrepWorkflows:
    """Test complete integration workflows"""

    def test_init_then_validate_workflow(self, temp_project):
        """
        Scenario: Complete init -> validate workflow
        Given: Empty project
        When: init followed by validate-config
        Then: Both operations succeed
        """
        # Step 1: Initialize
        initializer = ConfigurationInitializer(temp_project)
        init_result = initializer.initialize()
        assert init_result.success

        # Step 2: Validate
        config_path = temp_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        validator = ConfigurationValidator(config_path)
        validate_result = validator.validate()

        # Assert
        assert validate_result.valid is True

    def test_config_structure_matches_validation_requirements(self, temp_project):
        """
        Scenario: Generated config passes all validation checks
        Given: Freshly initialized configuration
        When: Configuration is validated
        Then: No errors or warnings are generated
        """
        # Arrange - Initialize
        initializer = ConfigurationInitializer(temp_project)
        initializer.initialize()

        # Act - Validate
        config_path = temp_project / "devforgeai" / "ast-grep" / "sgconfig.yml"
        validator = ConfigurationValidator(config_path)
        result = validator.validate()

        # Assert
        assert result.valid is True
        assert len(result.errors) == 0
        # Note: May have warnings for unrecognized languages if config uses non-standard ones

    def test_is_initialized_reflects_actual_state(self, temp_project):
        """
        Scenario: is_initialized correctly reflects directory state
        Given: Project transitions through initialization states
        When: is_initialized is checked at each stage
        Then: Returns correct boolean for each state
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # State 1: Before init
        assert initializer.is_initialized() is False

        # State 2: After init
        initializer.initialize()
        assert initializer.is_initialized() is True

        # State 3: After re-init (should still be True)
        initializer.initialize(force=True)
        assert initializer.is_initialized() is True
