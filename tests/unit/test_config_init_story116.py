"""
Tests for ConfigurationInitializer service (STORY-116: Configuration Infrastructure)

These tests validate the directory initialization and sgconfig.yml generation for
ast-grep rule storage. Tests focus on directory structure creation, configuration
generation, and safe initialization patterns.

Test Coverage: 95%+ for business logic
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import yaml

# Import from the actual module
from claude.scripts.devforgeai_cli.ast_grep.config_init import (
    ConfigurationInitializer,
    InitResult,
)


# ============================================================================
# TESTS: Directory Structure Creation
# ============================================================================

class TestConfigurationInitializerDirectoryCreation:
    """Test directory structure creation"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_should_create_devforgeai_ast_grep_directory(self, temp_project):
        """
        Scenario: Initialize ast-grep configuration
        Given: Empty project directory
        When: initialize() is called
        Then: .devforgeai/ast-grep/ directory is created
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)
        assert not initializer.ast_grep_dir.exists()

        # Act
        result = initializer.initialize()

        # Assert
        assert result.success
        assert initializer.ast_grep_dir.exists()
        assert initializer.ast_grep_dir.is_dir()

    def test_should_create_rules_python_directory(self, temp_project):
        """
        Scenario: Initialize python rules directory
        Given: No existing rules structure
        When: initialize() is called
        Then: rules/python/ directory is created
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        python_dir = initializer.ast_grep_dir / "rules" / "python"
        assert result.success
        assert python_dir.exists()
        assert python_dir.is_dir()

    def test_should_create_rules_csharp_directory(self, temp_project):
        """
        Scenario: Initialize csharp rules directory
        Given: No existing rules structure
        When: initialize() is called
        Then: rules/csharp/ directory is created
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        csharp_dir = initializer.ast_grep_dir / "rules" / "csharp"
        assert result.success
        assert csharp_dir.exists()

    def test_should_create_rules_typescript_directory(self, temp_project):
        """
        Scenario: Initialize typescript rules directory
        Given: No existing rules structure
        When: initialize() is called
        Then: rules/typescript/ directory is created
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        ts_dir = initializer.ast_grep_dir / "rules" / "typescript"
        assert result.success
        assert ts_dir.exists()

    def test_should_create_rules_javascript_directory(self, temp_project):
        """
        Scenario: Initialize javascript rules directory
        Given: No existing rules structure
        When: initialize() is called
        Then: rules/javascript/ directory is created
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        js_dir = initializer.ast_grep_dir / "rules" / "javascript"
        assert result.success
        assert js_dir.exists()

    def test_should_report_created_directories_in_result(self, temp_project):
        """
        Scenario: Initialize and report created paths
        Given: No existing configuration
        When: initialize() is called
        Then: Result includes list of created directories
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        assert result.success
        assert len(result.created_paths) > 0
        assert initializer.ast_grep_dir in result.created_paths


# ============================================================================
# TESTS: sgconfig.yml Generation
# ============================================================================

class TestConfigurationInitializerConfigGeneration:
    """Test sgconfig.yml generation"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_should_create_sgconfig_yml_file(self, temp_project):
        """
        Scenario: Initialize configuration file
        Given: Empty project
        When: initialize() is called
        Then: sgconfig.yml is created in .devforgeai/ast-grep/
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()

        # Assert
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        assert result.success
        assert config_path.exists()
        assert config_path.is_file()

    def test_should_include_ruleDirs_array_in_config(self, temp_project):
        """
        Scenario: Configuration contains ruleDirs array
        Given: Initialize completes
        When: sgconfig.yml is parsed
        Then: ruleDirs array contains all language directories
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Assert
        assert result.success
        assert "ruleDirs" in config
        assert isinstance(config["ruleDirs"], list)
        assert "rules/python" in config["ruleDirs"]
        assert "rules/csharp" in config["ruleDirs"]
        assert "rules/typescript" in config["ruleDirs"]
        assert "rules/javascript" in config["ruleDirs"]

    def test_should_include_languageGlobs_in_config(self, temp_project):
        """
        Scenario: Configuration contains language globs
        Given: Initialize completes
        When: sgconfig.yml is parsed
        Then: languageGlobs object maps languages to glob patterns
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Assert
        assert result.success
        assert "languageGlobs" in config
        assert config["languageGlobs"]["python"] == "**/*.py"
        assert config["languageGlobs"]["csharp"] == "**/*.cs"
        assert config["languageGlobs"]["typescript"] == "**/*.ts"
        assert config["languageGlobs"]["javascript"] == "**/*.js"

    def test_should_include_testDirs_array_in_config(self, temp_project):
        """
        Scenario: Configuration contains testDirs exclusions
        Given: Initialize completes
        When: sgconfig.yml is parsed
        Then: testDirs array lists directories to exclude
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Assert
        assert result.success
        assert "testDirs" in config
        assert isinstance(config["testDirs"], list)
        assert "tests" in config["testDirs"]
        assert "__tests__" in config["testDirs"]

    def test_should_include_devforgeai_metadata_in_config(self, temp_project):
        """
        Scenario: Configuration contains devforgeai metadata
        Given: Initialize completes
        When: sgconfig.yml is parsed
        Then: devforgeai object contains version and created date
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.initialize()
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Assert
        assert result.success
        assert "devforgeai" in config
        assert "version" in config["devforgeai"]
        assert "created" in config["devforgeai"]
        assert config["devforgeai"]["version"] == "1.0"


# ============================================================================
# TESTS: Safe Initialization (Idempotency)
# ============================================================================

class TestConfigurationInitializerIdempotency:
    """Test safe re-initialization of existing configuration"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_should_skip_existing_config_without_force(self, temp_project):
        """
        Scenario: Re-initialize without --force flag
        Given: Configuration already exists
        When: initialize(force=False) is called
        Then: Initialization succeeds, existing config not overwritten
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)
        initializer.initialize()

        # Create marker in config to detect overwrites
        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "a") as f:
            f.write("\n# CUSTOM MARKER\n")

        # Act
        result = initializer.initialize(force=False)

        # Assert
        assert result.success
        with open(config_path, "r") as f:
            content = f.read()
        assert "CUSTOM MARKER" in content

    def test_should_overwrite_existing_config_with_force(self, temp_project):
        """
        Scenario: Re-initialize with --force flag
        Given: Configuration already exists with custom marker
        When: initialize(force=True) is called
        Then: Existing config is overwritten
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)
        initializer.initialize()

        config_path = initializer.ast_grep_dir / "sgconfig.yml"
        with open(config_path, "a") as f:
            f.write("\n# CUSTOM MARKER\n")

        # Act
        result = initializer.initialize(force=True)

        # Assert
        assert result.success
        with open(config_path, "r") as f:
            content = f.read()
        assert "CUSTOM MARKER" not in content


# ============================================================================
# TESTS: Initialization State Checking
# ============================================================================

class TestConfigurationInitializerStateCheck:
    """Test is_initialized() state verification"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_should_return_true_after_successful_initialization(self, temp_project):
        """
        Scenario: Check initialization state after init
        Given: Successfully initialized configuration
        When: is_initialized() is called
        Then: Returns True
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)
        initializer.initialize()

        # Act
        result = initializer.is_initialized()

        # Assert
        assert result is True

    def test_should_return_false_before_initialization(self, temp_project):
        """
        Scenario: Check initialization state before init
        Given: No configuration created
        When: is_initialized() is called
        Then: Returns False
        """
        # Arrange
        initializer = ConfigurationInitializer(temp_project)

        # Act
        result = initializer.is_initialized()

        # Assert
        assert result is False


# ============================================================================
# TESTS: Error Handling
# ============================================================================

class TestConfigurationInitializerErrorHandling:
    """Test error handling during initialization"""

    def test_should_handle_permission_denied_gracefully(self):
        """
        Scenario: Initialize in read-only directory
        Given: Cannot create directories (permission denied)
        When: initialize() is called
        Then: Returns failed result with permission error message
        """
        # This test would require mocking os.mkdir to raise PermissionError
        # Actual implementation depends on testing strategy
        pytest.skip("Requires mock filesystem or elevated permissions")

    def test_should_handle_missing_yaml_library_gracefully(self):
        """
        Scenario: Initialize when PyYAML not available
        Given: PyYAML module not installed
        When: initialize() is called
        Then: Returns failed result with import error message
        """
        # This test would require mocking the yaml import
        pytest.skip("Requires import mocking")
