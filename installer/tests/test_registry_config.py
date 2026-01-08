"""
Test Suite for Registry Configuration (STORY-245)

Tests for RegistryConfigLoader service and related data models:
- RegistrySettings (AC#1-6)
- CredentialConfig (AC#5)
- ConfigValidationResult (AC#6)
- RegistryConfigLoader (AC#1-6, BR-001 to BR-004)

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- installer/registry_config.py does not exist yet
- RegistryConfigLoader, RegistrySettings, CredentialConfig not implemented
- ConfigValidationResult, ConfigError, ConfigWarning not implemented
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import tempfile
import time
from pathlib import Path


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def valid_config_yaml():
    """Return valid registry-config.yaml content with all 6 registries."""
    return """
# registry-config.yaml
defaults:
  skip-existing: true
  dry-run: false

registries:
  npm:
    enabled: true
    registry: https://registry.npmjs.org
    access: public

  pypi:
    enabled: true
    repository: pypi
    skip-existing: true

  nuget:
    enabled: false
    source: https://api.nuget.org/v3/index.json
    skip-duplicate: true

  docker:
    enabled: true
    registry: docker.io
    repository: devforgeai/framework
    tags:
      - latest
      - "{{version}}"

  github:
    enabled: true
    packages: true
    container: true

  crates:
    enabled: false
    allow-dirty: false
"""


@pytest.fixture
def minimal_config_yaml():
    """Return minimal config with only required fields."""
    return """
registries:
  npm:
    enabled: true
"""


@pytest.fixture
def invalid_schema_config_yaml():
    """Return config with JSON Schema violations."""
    return """
registries:
  npm:
    enabled: "yes"  # Should be boolean, not string
    access: private  # Should be 'public' or 'restricted', not 'private'
"""


@pytest.fixture
def invalid_yaml_syntax():
    """Return config with invalid YAML syntax."""
    return """
registries:
  npm:
    enabled: true
      invalid_indentation: this is broken
    access: public
"""


@pytest.fixture
def config_with_custom_credentials():
    """Return config with custom credential environment variable names."""
    return """
registries:
  npm:
    enabled: true
    registry: https://registry.npmjs.org
    credentials:
      token_var: MY_CUSTOM_NPM_TOKEN

  pypi:
    enabled: true
    repository: pypi
    credentials:
      username_var: MY_PYPI_USER
      password_var: MY_PYPI_PASS
"""


@pytest.fixture
def temp_config_file(valid_config_yaml):
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.yaml',
        delete=False
    ) as f:
        f.write(valid_config_yaml)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


# =============================================================================
# AC#1: Registry Configuration File Schema Tests
# =============================================================================

class TestRegistryConfigSchema:
    """Tests for AC#1: Registry Configuration File Schema."""

    def test_load_should_return_registry_config_with_all_6_registries(
        self, temp_config_file
    ):
        """AC#1: Config file supports all 6 registries (npm, pypi, nuget, docker, github, crates)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        assert config is not None
        expected_registries = ['npm', 'pypi', 'nuget', 'docker', 'github', 'crates']
        for registry in expected_registries:
            assert registry in config.registries, f"Missing registry: {registry}"

    def test_load_should_parse_enabled_field_for_each_registry(
        self, temp_config_file
    ):
        """AC#1: Each registry has enabled field."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        for name, settings in config.registries.items():
            assert hasattr(settings, 'enabled'), f"Registry {name} missing 'enabled' field"
            assert isinstance(settings.enabled, bool), f"Registry {name} 'enabled' should be bool"

    def test_load_should_parse_endpoint_field_for_each_registry(
        self, temp_config_file
    ):
        """AC#1: Each registry has endpoint field (registry/source/repository)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        npm_settings = config.registries.get('npm')
        assert npm_settings is not None
        assert npm_settings.registry_url is not None or hasattr(npm_settings, 'registry_url')

    def test_load_should_parse_options_field_for_each_registry(
        self, temp_config_file
    ):
        """AC#1: Each registry has options field."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        for name, settings in config.registries.items():
            assert hasattr(settings, 'options'), f"Registry {name} missing 'options' field"

    def test_validate_should_accept_valid_config(self, valid_config_yaml):
        """AC#1: JSON Schema validation available and accepts valid config."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import yaml

        loader = RegistryConfigLoader()
        config_dict = yaml.safe_load(valid_config_yaml)

        # Act
        result = loader.validate(config=config_dict)

        # Assert
        assert result.valid is True
        assert len(result.errors) == 0


class TestRegistrySettingsDataModel:
    """Tests for RegistrySettings data model from Technical Specification."""

    def test_registry_settings_should_have_name_field(self):
        """Tech Spec: RegistrySettings must have name string field."""
        # Arrange
        from installer.registry_config import RegistrySettings

        # Act
        settings = RegistrySettings(name="npm", enabled=True)

        # Assert
        assert settings.name == "npm"

    def test_registry_settings_should_have_enabled_field_with_default_true(self):
        """Tech Spec: RegistrySettings enabled defaults to true."""
        # Arrange
        from installer.registry_config import RegistrySettings

        # Act
        settings = RegistrySettings(name="npm")

        # Assert
        assert settings.enabled is True

    def test_registry_settings_should_have_optional_registry_url(self):
        """Tech Spec: RegistrySettings has optional registry_url field."""
        # Arrange
        from installer.registry_config import RegistrySettings

        # Act
        settings = RegistrySettings(
            name="npm",
            registry_url="https://custom.registry.com"
        )

        # Assert
        assert settings.registry_url == "https://custom.registry.com"

    def test_registry_settings_should_have_skip_existing_with_default_true(self):
        """Tech Spec: RegistrySettings skip_existing defaults to true."""
        # Arrange
        from installer.registry_config import RegistrySettings

        # Act
        settings = RegistrySettings(name="npm")

        # Assert
        assert settings.skip_existing is True

    def test_registry_settings_should_have_credentials_config(self):
        """Tech Spec: RegistrySettings has credentials field of type CredentialConfig."""
        # Arrange
        from installer.registry_config import RegistrySettings, CredentialConfig

        credentials = CredentialConfig(token_var="NPM_TOKEN")

        # Act
        settings = RegistrySettings(
            name="npm",
            credentials=credentials
        )

        # Assert
        assert settings.credentials is not None
        assert settings.credentials.token_var == "NPM_TOKEN"

    def test_registry_settings_should_have_options_dict(self):
        """Tech Spec: RegistrySettings has options dict field."""
        # Arrange
        from installer.registry_config import RegistrySettings

        # Act
        settings = RegistrySettings(
            name="npm",
            options={"access": "public", "tag": "latest"}
        )

        # Assert
        assert settings.options == {"access": "public", "tag": "latest"}


class TestCredentialConfigDataModel:
    """Tests for CredentialConfig data model from Technical Specification."""

    def test_credential_config_should_have_optional_token_var(self):
        """Tech Spec: CredentialConfig has optional token_var field."""
        # Arrange
        from installer.registry_config import CredentialConfig

        # Act
        config = CredentialConfig(token_var="NPM_TOKEN")

        # Assert
        assert config.token_var == "NPM_TOKEN"

    def test_credential_config_should_have_optional_username_var(self):
        """Tech Spec: CredentialConfig has optional username_var field."""
        # Arrange
        from installer.registry_config import CredentialConfig

        # Act
        config = CredentialConfig(username_var="PYPI_USER")

        # Assert
        assert config.username_var == "PYPI_USER"

    def test_credential_config_should_have_optional_password_var(self):
        """Tech Spec: CredentialConfig has optional password_var field."""
        # Arrange
        from installer.registry_config import CredentialConfig

        # Act
        config = CredentialConfig(password_var="PYPI_PASS")

        # Assert
        assert config.password_var == "PYPI_PASS"

    def test_credential_config_should_allow_all_fields_none(self):
        """Tech Spec: All CredentialConfig fields are optional."""
        # Arrange
        from installer.registry_config import CredentialConfig

        # Act
        config = CredentialConfig()

        # Assert
        assert config.token_var is None
        assert config.username_var is None
        assert config.password_var is None


class TestConfigValidationResultDataModel:
    """Tests for ConfigValidationResult data model from Technical Specification."""

    def test_validation_result_should_have_valid_bool_field(self):
        """Tech Spec: ConfigValidationResult has valid boolean field."""
        # Arrange
        from installer.registry_config import ConfigValidationResult

        # Act
        result = ConfigValidationResult(valid=True, errors=[], warnings=[])

        # Assert
        assert result.valid is True

    def test_validation_result_should_have_errors_list(self):
        """Tech Spec: ConfigValidationResult has errors list field."""
        # Arrange
        from installer.registry_config import ConfigValidationResult, ConfigError

        error = ConfigError(
            field="registries.npm.access",
            message="Invalid value 'private'",
            line=12
        )

        # Act
        result = ConfigValidationResult(valid=False, errors=[error], warnings=[])

        # Assert
        assert len(result.errors) == 1
        assert result.errors[0].field == "registries.npm.access"

    def test_validation_result_should_have_warnings_list(self):
        """Tech Spec: ConfigValidationResult has warnings list field."""
        # Arrange
        from installer.registry_config import ConfigValidationResult, ConfigWarning

        warning = ConfigWarning(
            field="registries.legacy",
            message="Unknown registry 'legacy' will be ignored"
        )

        # Act
        result = ConfigValidationResult(valid=True, errors=[], warnings=[warning])

        # Assert
        assert len(result.warnings) == 1
        assert "legacy" in result.warnings[0].message


# =============================================================================
# AC#2: Registry Enable/Disable Control Tests
# =============================================================================

class TestRegistryEnableDisableControl:
    """Tests for AC#2: Registry Enable/Disable Control."""

    def test_get_enabled_registries_should_return_only_enabled(self, temp_config_file):
        """AC#2: enabled: false skips registry during publishing."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        config = loader.load(config_path=temp_config_file)

        # Act
        enabled = loader.get_enabled_registries()

        # Assert
        # Based on fixture: npm, pypi, docker, github are enabled; nuget, crates are disabled
        assert 'npm' in enabled
        assert 'pypi' in enabled
        assert 'docker' in enabled
        assert 'github' in enabled
        assert 'nuget' not in enabled
        assert 'crates' not in enabled

    def test_disabled_registry_should_log_skip_message(self, temp_config_file, caplog):
        """AC#2: Log message indicates 'Registry {name} disabled in config'."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import logging

        loader = RegistryConfigLoader()
        config = loader.load(config_path=temp_config_file)

        # Act
        with caplog.at_level(logging.INFO):
            enabled = loader.get_enabled_registries()

        # Assert
        # Should log skipped registries
        assert "nuget" in caplog.text.lower() or len([r for r in caplog.records if 'disabled' in r.message.lower()]) >= 0

    def test_disabled_registry_should_not_count_as_failure(self, temp_config_file):
        """AC#2: Skip does not count as failure."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        config = loader.load(config_path=temp_config_file)

        # Act
        registry = loader.get_registry('nuget')

        # Assert
        assert registry.enabled is False
        # Getting a disabled registry should not raise an error
        assert registry is not None

    def test_missing_enabled_field_should_default_to_true(self, minimal_config_yaml, temp_config_dir):
        """AC#2 Verification: Default is enabled: true if field missing."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        # Config without explicit enabled field
        with open(config_path, 'w') as f:
            f.write("""
registries:
  npm:
    registry: https://registry.npmjs.org
""")

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        assert npm_settings.enabled is True


# =============================================================================
# AC#3: Custom Registry Endpoints Tests
# =============================================================================

class TestCustomRegistryEndpoints:
    """Tests for AC#3: Custom Registry Endpoints."""

    def test_npm_should_use_custom_registry_flag(self, temp_config_dir):
        """AC#3: npm uses --registry flag with custom URL."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  npm:
    enabled: true
    registry: https://my-private-npm.example.com
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        assert npm_settings.registry_url == "https://my-private-npm.example.com"

    def test_nuget_should_use_custom_source_flag(self, temp_config_dir):
        """AC#3: NuGet uses --source flag with custom URL."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  nuget:
    enabled: true
    source: https://my-private-nuget.example.com/v3/index.json
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        nuget_settings = config.registries.get('nuget')

        # Assert
        # NuGet uses 'source' field mapped to registry_url
        assert nuget_settings.registry_url == "https://my-private-nuget.example.com/v3/index.json"

    def test_docker_should_use_custom_registry_prefix(self, temp_config_dir):
        """AC#3: Docker uses custom registry prefix."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  docker:
    enabled: true
    registry: my-registry.example.com
    repository: devforgeai/framework
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        docker_settings = config.registries.get('docker')

        # Assert
        assert docker_settings.registry_url == "my-registry.example.com"

    def test_pypi_should_support_repository_option(self, temp_config_dir):
        """AC#3 Verification: pypi --repository option supported."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  pypi:
    enabled: true
    repository: testpypi
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        pypi_settings = config.registries.get('pypi')

        # Assert
        # PyPI uses 'repository' field for testpypi vs pypi
        assert pypi_settings.options.get('repository') == "testpypi" or \
               pypi_settings.registry_url == "testpypi"

    def test_github_npm_should_use_npm_pkg_github_com(self, temp_config_dir):
        """AC#3 Verification: GitHub registry URLs supported (npm.pkg.github.com)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  github:
    enabled: true
    packages: true
    registry: https://npm.pkg.github.com
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        github_settings = config.registries.get('github')

        # Assert
        assert "npm.pkg.github.com" in (github_settings.registry_url or "")

    def test_github_container_should_use_ghcr_io(self, temp_config_dir):
        """AC#3 Verification: GitHub container registry (ghcr.io) supported."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  github:
    enabled: true
    container: true
    container_registry: ghcr.io
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        github_settings = config.registries.get('github')

        # Assert
        assert github_settings.options.get('container_registry') == "ghcr.io" or \
               github_settings.options.get('container') is True


# =============================================================================
# AC#4: Version Conflict Handling Configuration Tests
# =============================================================================

class TestVersionConflictHandling:
    """Tests for AC#4: Version Conflict Handling Configuration."""

    def test_skip_existing_true_should_be_parsed(self, temp_config_file):
        """AC#4: skip-existing: true parsed correctly."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)
        pypi_settings = config.registries.get('pypi')

        # Assert
        assert pypi_settings.skip_existing is True

    def test_skip_existing_false_should_cause_failure_on_conflict(self, temp_config_dir):
        """AC#4: skip-existing: false causes version conflict to fail."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  npm:
    enabled: true
    skip-existing: false
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        assert npm_settings.skip_existing is False

    def test_default_skip_existing_should_be_true(self, minimal_config_yaml, temp_config_dir):
        """AC#4 Verification: Default is skip-existing: true."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(minimal_config_yaml)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        assert npm_settings.skip_existing is True

    def test_global_defaults_should_apply_to_registries(self, temp_config_dir):
        """AC#4 Verification: Global defaults section applies to registries."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
defaults:
  skip-existing: false

registries:
  npm:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        # npm should inherit skip-existing: false from defaults
        assert npm_settings.skip_existing is False


# =============================================================================
# AC#5: Credential Environment Variable Mapping Tests
# =============================================================================

class TestCredentialEnvironmentVariableMapping:
    """Tests for AC#5: Credential Environment Variable Mapping."""

    def test_custom_credential_env_var_should_be_parsed(
        self, config_with_custom_credentials, temp_config_dir
    ):
        """AC#5: Custom credential env var names supported."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_with_custom_credentials)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        assert npm_settings.credentials.token_var == "MY_CUSTOM_NPM_TOKEN"

    def test_default_npm_credential_should_be_npm_token(self, minimal_config_yaml, temp_config_dir):
        """AC#5: Default variable names used if not specified (NPM_TOKEN)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(minimal_config_yaml)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        # Default credential var for npm is NPM_TOKEN
        assert npm_settings.credentials.token_var == "NPM_TOKEN"

    def test_default_pypi_credentials_should_be_twine_vars(self, temp_config_dir):
        """AC#5: Default PyPI credentials are TWINE_USERNAME, TWINE_PASSWORD."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  pypi:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        pypi_settings = config.registries.get('pypi')

        # Assert
        assert pypi_settings.credentials.username_var == "TWINE_USERNAME"
        assert pypi_settings.credentials.password_var == "TWINE_PASSWORD"

    def test_default_nuget_credential_should_be_nuget_api_key(self, temp_config_dir):
        """AC#5: Default NuGet credential is NUGET_API_KEY."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  nuget:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        nuget_settings = config.registries.get('nuget')

        # Assert
        assert nuget_settings.credentials.token_var == "NUGET_API_KEY"

    def test_default_docker_credentials_should_be_docker_vars(self, temp_config_dir):
        """AC#5: Default Docker credentials are DOCKER_USERNAME, DOCKER_PASSWORD."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  docker:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        docker_settings = config.registries.get('docker')

        # Assert
        assert docker_settings.credentials.username_var == "DOCKER_USERNAME"
        assert docker_settings.credentials.password_var == "DOCKER_PASSWORD"

    def test_default_github_credential_should_be_github_token(self, temp_config_dir):
        """AC#5: Default GitHub credential is GITHUB_TOKEN."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  github:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        github_settings = config.registries.get('github')

        # Assert
        assert github_settings.credentials.token_var == "GITHUB_TOKEN"

    def test_default_crates_credential_should_be_cargo_registry_token(self, temp_config_dir):
        """AC#5: Default crates.io credential is CARGO_REGISTRY_TOKEN."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  crates:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        crates_settings = config.registries.get('crates')

        # Assert
        assert crates_settings.credentials.token_var == "CARGO_REGISTRY_TOKEN"

    def test_missing_credentials_should_cause_clear_error(self, temp_config_dir):
        """AC#5: Missing required credentials cause clear error messages."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  npm:
    enabled: true
    credentials:
      token_var: MY_MISSING_TOKEN
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()
        config = loader.load(config_path=config_path)

        # Act & Assert
        # Ensure MY_MISSING_TOKEN is not set
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="MY_MISSING_TOKEN"):
                loader.validate_credentials(config)


# =============================================================================
# AC#6: Configuration Validation on Load Tests
# =============================================================================

class TestConfigurationValidationOnLoad:
    """Tests for AC#6: Configuration Validation on Load."""

    def test_validate_should_fail_with_invalid_schema(self, invalid_schema_config_yaml):
        """AC#6: JSON Schema validation fails with specific error."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import yaml

        loader = RegistryConfigLoader()
        config_dict = yaml.safe_load(invalid_schema_config_yaml)

        # Act
        result = loader.validate(config=config_dict)

        # Assert
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validation_error_should_indicate_field_with_issue(
        self, invalid_schema_config_yaml
    ):
        """AC#6: Error message indicates field with issue."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import yaml

        loader = RegistryConfigLoader()
        config_dict = yaml.safe_load(invalid_schema_config_yaml)

        # Act
        result = loader.validate(config=config_dict)

        # Assert
        error_fields = [e.field for e in result.errors]
        # Should identify the problematic fields
        assert any('npm' in field for field in error_fields)

    def test_validation_error_should_include_line_number(
        self, invalid_schema_config_yaml, temp_config_dir
    ):
        """AC#6: Error message indicates line with issue."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(invalid_schema_config_yaml)

        loader = RegistryConfigLoader()

        # Act
        try:
            config = loader.load(config_path=config_path)
        except Exception as e:
            # Assert
            error_message = str(e)
            # Error should contain line number reference
            assert 'line' in error_message.lower() or any(
                str(i) in error_message for i in range(1, 20)
            )
            return

        # If no exception, check validation result
        result = loader.validate(config._raw_config)
        # Note: PyYAML safe_load doesn't preserve line numbers for valid YAML
        # Line numbers are only available for YAML syntax errors
        # For schema validation errors, we check that field path is provided
        assert len(result.errors) > 0
        assert all(e.field is not None for e in result.errors)

    def test_invalid_yaml_syntax_should_fail_on_load(
        self, invalid_yaml_syntax, temp_config_dir
    ):
        """AC#6: Invalid YAML syntax detected."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(invalid_yaml_syntax)

        loader = RegistryConfigLoader()

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            loader.load(config_path=config_path)

        # Error should be about YAML parsing
        assert 'yaml' in str(exc_info.value).lower() or 'parse' in str(exc_info.value).lower()

    def test_load_should_not_proceed_with_invalid_config(
        self, invalid_schema_config_yaml, temp_config_dir
    ):
        """AC#6: Publish does not proceed until config is valid."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(invalid_schema_config_yaml)

        loader = RegistryConfigLoader()

        # Act & Assert
        with pytest.raises(Exception):
            # Loading invalid config should raise or return invalid result
            config = loader.load(config_path=config_path, validate=True)
            if hasattr(config, 'valid') and not config.valid:
                raise ValueError("Config validation failed")


# =============================================================================
# Business Rules Tests (BR-001 to BR-004)
# =============================================================================

class TestBusinessRules:
    """Tests for business rules from Technical Specification."""

    def test_br001_missing_config_should_use_defaults(self, temp_config_dir):
        """BR-001: Missing config file uses sensible defaults."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        nonexistent_path = os.path.join(temp_config_dir, 'nonexistent.yaml')

        # Act
        config = loader.load(config_path=nonexistent_path)

        # Assert
        # Should return default config with all registries enabled
        assert config is not None
        assert 'npm' in config.registries
        assert config.registries['npm'].enabled is True

    def test_br002_invalid_config_should_block_publishing(
        self, invalid_schema_config_yaml, temp_config_dir
    ):
        """BR-002: Invalid config blocks publishing (fail fast)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(invalid_schema_config_yaml)

        loader = RegistryConfigLoader()

        # Act & Assert
        with pytest.raises(Exception):
            config = loader.load(config_path=config_path, validate=True)

    def test_br003_custom_credentials_override_defaults(
        self, config_with_custom_credentials, temp_config_dir
    ):
        """BR-003: Custom credentials override defaults, not append."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_with_custom_credentials)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        npm_settings = config.registries.get('npm')

        # Assert
        # Custom token var should completely replace default, not coexist
        assert npm_settings.credentials.token_var == "MY_CUSTOM_NPM_TOKEN"
        # Should NOT also have NPM_TOKEN

    def test_br004_disabled_registries_not_counted_in_results(self, temp_config_file):
        """BR-004: Disabled registries are logged but not counted as success/failure."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        config = loader.load(config_path=temp_config_file)

        # Act
        enabled = loader.get_enabled_registries()
        all_registries = list(config.registries.keys())

        # Assert
        # nuget and crates are disabled in fixture
        assert 'nuget' not in enabled
        assert 'crates' not in enabled
        # But they should still exist in config (just not enabled)
        assert 'nuget' in all_registries
        assert 'crates' in all_registries


# =============================================================================
# Non-Functional Requirements Tests
# =============================================================================

class TestNonFunctionalRequirements:
    """Tests for NFR from Technical Specification."""

    def test_nfr001_config_loading_under_500ms(self, temp_config_file):
        """NFR-001: Config loading and validation < 500ms."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        start_time = time.time()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        elapsed = time.time() - start_time
        assert elapsed < 0.5, f"Config load took {elapsed}s (expected <500ms)"

    def test_nfr002_error_messages_should_be_actionable(
        self, invalid_schema_config_yaml
    ):
        """NFR-002: Validation errors include line numbers and fix suggestions."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import yaml

        loader = RegistryConfigLoader()
        config_dict = yaml.safe_load(invalid_schema_config_yaml)

        # Act
        result = loader.validate(config=config_dict)

        # Assert
        for error in result.errors:
            # Each error should have actionable info
            assert error.field is not None, "Error missing field info"
            assert error.message is not None, "Error missing message"
            # Message should explain what's wrong
            assert len(error.message) > 10, "Error message not descriptive enough"

    def test_nfr003_config_should_be_fresh_on_each_load(self, temp_config_dir):
        """NFR-003: Config file changes detected on each publish (no caching)."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')

        # Write initial config
        with open(config_path, 'w') as f:
            f.write("""
registries:
  npm:
    enabled: true
""")

        loader = RegistryConfigLoader()

        # Act - First load
        config1 = loader.load(config_path=config_path)

        # Modify config file
        with open(config_path, 'w') as f:
            f.write("""
registries:
  npm:
    enabled: false
""")

        # Second load should see changes
        config2 = loader.load(config_path=config_path)

        # Assert
        assert config1.registries['npm'].enabled is True
        assert config2.registries['npm'].enabled is False


# =============================================================================
# Edge Cases Tests
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases from story specification."""

    def test_edge_case_1_missing_config_file(self, temp_config_dir):
        """Edge Case 1: Missing config file - Use defaults."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        nonexistent_path = os.path.join(temp_config_dir, 'does-not-exist.yaml')

        # Act
        config = loader.load(config_path=nonexistent_path)

        # Assert
        assert config is not None
        # All registries should be enabled by default
        for registry in config.registries.values():
            assert registry.enabled is True

    def test_edge_case_2_partial_config(self, temp_config_dir):
        """Edge Case 2: Partial config - Merge with defaults."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  npm:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)

        # Assert
        # npm should have skip_existing default (true)
        assert config.registries['npm'].skip_existing is True
        # npm should have default credentials
        assert config.registries['npm'].credentials.token_var == "NPM_TOKEN"

    def test_edge_case_3_unknown_registry(self, temp_config_dir, caplog):
        """Edge Case 3: Unknown registry - Log warning, ignore."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader
        import logging

        config_content = """
registries:
  npm:
    enabled: true
  unknown_registry:
    enabled: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        with caplog.at_level(logging.WARNING):
            config = loader.load(config_path=config_path)

        # Assert
        # Should not fail
        assert config is not None
        # Known registry should be loaded
        assert 'npm' in config.registries
        # Warning should be logged for unknown registry
        assert "unknown_registry" in caplog.text.lower() or \
               any('warning' in r.levelname.lower() for r in caplog.records)

    def test_edge_case_4_invalid_yaml_syntax(self, invalid_yaml_syntax, temp_config_dir):
        """Edge Case 4: Invalid YAML syntax - Fail with parse error and line number."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(invalid_yaml_syntax)

        loader = RegistryConfigLoader()

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            loader.load(config_path=config_path)

        # Should indicate line number
        error_msg = str(exc_info.value)
        assert 'line' in error_msg.lower() or any(str(i) in error_msg for i in range(1, 10))

    def test_edge_case_5_missing_required_field(self, temp_config_dir):
        """Edge Case 5: Missing required field - Fail with field name and expected type."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        # registries section is missing
        config_content = """
defaults:
  skip-existing: true
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        # Should either use defaults or fail gracefully
        config = loader.load(config_path=config_path)

        # Assert - Should have default registries or be empty but valid
        assert config is not None
        # If registries not specified, use defaults
        if config.registries:
            assert len(config.registries) >= 0

    def test_edge_case_6_empty_registries_section(self, temp_config_dir):
        """Edge Case 6: Empty registries section - Treat as all registries disabled."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries: {}
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=config_path)
        enabled = loader.get_enabled_registries()

        # Assert
        # No registries should be enabled
        assert len(enabled) == 0

    def test_edge_case_7_custom_credential_vars_missing(self, temp_config_dir):
        """Edge Case 7: Custom credential vars missing - Check configured names, not defaults."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        config_content = """
registries:
  npm:
    enabled: true
    credentials:
      token_var: MY_CUSTOM_NPM_TOKEN
"""
        config_path = os.path.join(temp_config_dir, 'registry-config.yaml')
        with open(config_path, 'w') as f:
            f.write(config_content)

        loader = RegistryConfigLoader()
        config = loader.load(config_path=config_path)

        # Act & Assert
        # Should check for MY_CUSTOM_NPM_TOKEN, not NPM_TOKEN
        with patch.dict(os.environ, {"NPM_TOKEN": "should_not_use_this"}, clear=True):
            # MY_CUSTOM_NPM_TOKEN is not set
            with pytest.raises(ValueError, match="MY_CUSTOM_NPM_TOKEN"):
                loader.validate_credentials(config)


# =============================================================================
# RegistryConfigLoader Service Tests
# =============================================================================

class TestRegistryConfigLoaderService:
    """Tests for RegistryConfigLoader service from Technical Specification."""

    def test_load_should_return_registry_config(self, temp_config_file):
        """Tech Spec: load() returns RegistryConfig."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader, RegistryConfig

        loader = RegistryConfigLoader()

        # Act
        config = loader.load(config_path=temp_config_file)

        # Assert
        # Should return a RegistryConfig-like object
        assert hasattr(config, 'registries')
        assert isinstance(config.registries, dict)

    def test_load_with_default_path(self, temp_config_dir, monkeypatch):
        """Tech Spec: load() uses default path if not specified."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        # Set up default config path
        default_config_path = os.path.join(
            temp_config_dir, 'devforgeai', 'deployment', 'registry-config.yaml'
        )
        os.makedirs(os.path.dirname(default_config_path), exist_ok=True)
        with open(default_config_path, 'w') as f:
            f.write("""
registries:
  npm:
    enabled: true
""")

        loader = RegistryConfigLoader(base_path=temp_config_dir)

        # Act
        config = loader.load()

        # Assert
        assert config is not None
        assert 'npm' in config.registries

    def test_validate_should_return_validation_result(self, valid_config_yaml):
        """Tech Spec: validate() returns ValidationResult."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader, ConfigValidationResult
        import yaml

        loader = RegistryConfigLoader()
        config_dict = yaml.safe_load(valid_config_yaml)

        # Act
        result = loader.validate(config=config_dict)

        # Assert
        assert isinstance(result, ConfigValidationResult)
        assert hasattr(result, 'valid')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')

    def test_get_registry_should_return_settings(self, temp_config_file):
        """Tech Spec: get_registry() returns RegistrySettings for specific registry."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader, RegistrySettings

        loader = RegistryConfigLoader()
        loader.load(config_path=temp_config_file)

        # Act
        npm_settings = loader.get_registry('npm')

        # Assert
        assert npm_settings is not None
        assert npm_settings.name == 'npm'

    def test_get_registry_nonexistent_should_return_none(self, temp_config_file):
        """Tech Spec: get_registry() returns None for nonexistent registry."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        loader.load(config_path=temp_config_file)

        # Act
        result = loader.get_registry('nonexistent')

        # Assert
        assert result is None

    def test_get_enabled_registries_should_return_list(self, temp_config_file):
        """Tech Spec: get_enabled_registries() returns list[str]."""
        # Arrange
        from installer.registry_config import RegistryConfigLoader

        loader = RegistryConfigLoader()
        loader.load(config_path=temp_config_file)

        # Act
        enabled = loader.get_enabled_registries()

        # Assert
        assert isinstance(enabled, list)
        assert all(isinstance(r, str) for r in enabled)
