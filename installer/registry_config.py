"""
STORY-245: Registry Configuration Module

This module provides YAML configuration file support for registry publishing settings.
It allows customization of registry endpoints, enabling/disabling registries, and
version conflict behavior.

Implements:
- CredentialConfig: Environment variable mapping for credentials
- RegistrySettings: Per-registry configuration (name, enabled, registry_url, etc.)
- ConfigError/ConfigWarning: Validation result details
- ConfigValidationResult: Validation result with valid flag, errors, warnings
- RegistryConfig: Container for all registry settings
- RegistryConfigLoader: Service for loading and validating configuration
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
import os

import yaml

# Configure logging
logger = logging.getLogger(__name__)


# =============================================================================
# Default Credential Mappings (AC#5)
# =============================================================================

DEFAULT_CREDENTIALS = {
    "npm": {"token_var": "NPM_TOKEN"},
    "pypi": {"username_var": "TWINE_USERNAME", "password_var": "TWINE_PASSWORD"},
    "nuget": {"token_var": "NUGET_API_KEY"},
    "docker": {"username_var": "DOCKER_USERNAME", "password_var": "DOCKER_PASSWORD"},
    "github": {"token_var": "GITHUB_TOKEN"},
    "crates": {"token_var": "CARGO_REGISTRY_TOKEN"},
}

# Default registry endpoints
DEFAULT_ENDPOINTS = {
    "npm": "https://registry.npmjs.org",
    "pypi": "pypi",
    "nuget": "https://api.nuget.org/v3/index.json",
    "docker": "docker.io",
    "github": "https://npm.pkg.github.com",
    "crates": "https://crates.io",
}

# Known registries (for unknown registry warning)
KNOWN_REGISTRIES = {"npm", "pypi", "nuget", "docker", "github", "crates"}


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class CredentialConfig:
    """
    Credential environment variable configuration (AC#5).

    All fields are optional - defaults are used if not specified.
    Custom values override defaults (BR-003).
    """
    token_var: Optional[str] = None
    username_var: Optional[str] = None
    password_var: Optional[str] = None


@dataclass
class ConfigError:
    """
    Validation error with field path, message, and line number (AC#6).
    """
    field: str
    message: str
    line: Optional[int] = None


@dataclass
class ConfigWarning:
    """
    Validation warning with field path and message.
    """
    field: str
    message: str


@dataclass
class ConfigValidationResult:
    """
    Result of configuration validation (AC#6).

    Attributes:
        valid: True if config is valid and can be used
        errors: List of validation errors (blocking)
        warnings: List of validation warnings (non-blocking)
    """
    valid: bool
    errors: List[ConfigError] = field(default_factory=list)
    warnings: List[ConfigWarning] = field(default_factory=list)


@dataclass
class RegistrySettings:
    """
    Settings for a single registry (AC#1-5).

    Attributes:
        name: Registry identifier (npm, pypi, nuget, docker, github, crates)
        enabled: Whether registry is enabled (default: True)
        registry_url: Custom registry endpoint URL
        skip_existing: Skip if version already exists (default: True)
        credentials: Credential environment variable mapping
        options: Registry-specific options dict
    """
    name: str
    enabled: bool = True
    registry_url: Optional[str] = None
    skip_existing: bool = True
    credentials: CredentialConfig = field(default_factory=CredentialConfig)
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegistryConfig:
    """
    Container for all registry configurations.

    Attributes:
        registries: Dict mapping registry name to RegistrySettings
        defaults: Global default settings applied to all registries
    """
    registries: Dict[str, RegistrySettings] = field(default_factory=dict)
    defaults: Dict[str, Any] = field(default_factory=dict)
    _raw_config: Dict[str, Any] = field(default_factory=dict, repr=False)


# =============================================================================
# RegistryConfigLoader Service
# =============================================================================

class RegistryConfigLoader:
    """
    Service for loading and validating registry configuration (AC#1-6).

    Supports loading from YAML file with JSON Schema validation,
    default value merging, and credential validation.

    Usage:
        loader = RegistryConfigLoader()
        config = loader.load(config_path="devforgeai/deployment/registry-config.yaml")
        enabled = loader.get_enabled_registries()
    """

    # Default config path relative to base_path
    DEFAULT_CONFIG_PATH = "devforgeai/deployment/registry-config.yaml"

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize RegistryConfigLoader.

        Args:
            base_path: Base directory for config file lookup. Defaults to cwd.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self._config: Optional[RegistryConfig] = None
        self._schema: Optional[Dict] = None

    def load(
        self,
        config_path: Optional[str] = None,
        validate: bool = False
    ) -> RegistryConfig:
        """
        Load registry configuration from YAML file (AC#1).

        If config file is missing, returns defaults with all registries enabled (BR-001).
        If validate=True and config is invalid, raises ValueError (BR-002).

        Args:
            config_path: Path to registry-config.yaml. If None, uses default path.
            validate: If True, validate against JSON Schema and raise on error.

        Returns:
            RegistryConfig with loaded settings.

        Raises:
            ValueError: If validate=True and config is invalid.
            yaml.YAMLError: If YAML syntax is invalid.
        """
        # Determine config file path
        if config_path:
            path = Path(config_path)
        else:
            path = self.base_path / self.DEFAULT_CONFIG_PATH

        # Load YAML or use defaults (BR-001)
        if path.exists():
            try:
                raw_config = yaml.safe_load(path.read_text(encoding="utf-8"))
                if raw_config is None:
                    raw_config = {}
            except yaml.YAMLError as e:
                # Enhance error with file context
                raise yaml.YAMLError(f"YAML parse error in {path}: {e}") from e
        else:
            logger.info(f"Config file not found at {path}, using defaults")
            raw_config = {}

        # Validate if requested (BR-002)
        if validate and raw_config:
            result = self.validate(raw_config)
            if not result.valid:
                error_msgs = "; ".join(
                    f"{e.field}: {e.message}" + (f" (line {e.line})" if e.line else "")
                    for e in result.errors
                )
                raise ValueError(f"Config validation failed: {error_msgs}")

        # Parse and merge with defaults
        self._config = self._parse_config(raw_config)
        self._config._raw_config = raw_config

        return self._config

    def validate(self, config: Dict[str, Any]) -> ConfigValidationResult:
        """
        Validate configuration against JSON Schema (AC#6).

        Args:
            config: Raw configuration dict from YAML.

        Returns:
            ConfigValidationResult with valid flag, errors, and warnings.
        """
        errors: List[ConfigError] = []
        warnings: List[ConfigWarning] = []

        # Check registries section
        registries = config.get("registries", {})

        if registries:
            for name, settings in registries.items():
                if not isinstance(settings, dict):
                    continue

                # Check for unknown registries
                if name not in KNOWN_REGISTRIES:
                    warnings.append(ConfigWarning(
                        field=f"registries.{name}",
                        message=f"Unknown registry '{name}' will be ignored"
                    ))
                    continue

                # Validate enabled field type
                if "enabled" in settings:
                    enabled_val = settings["enabled"]
                    if not isinstance(enabled_val, bool):
                        errors.append(ConfigError(
                            field=f"registries.{name}.enabled",
                            message=f"'enabled' must be boolean, got {type(enabled_val).__name__}",
                            line=None
                        ))

                # Validate access field for npm (must be 'public' or 'restricted')
                if name == "npm" and "access" in settings:
                    access_val = settings["access"]
                    if access_val not in ("public", "restricted"):
                        errors.append(ConfigError(
                            field=f"registries.{name}.access",
                            message=f"'access' must be 'public' or 'restricted', got '{access_val}'",
                            line=None
                        ))

                # Validate repository field for pypi
                if name == "pypi" and "repository" in settings:
                    repo_val = settings["repository"]
                    valid_repos = ("pypi", "testpypi")
                    # Must be pypi, testpypi, or a URL
                    if repo_val not in valid_repos and not repo_val.startswith("http"):
                        errors.append(ConfigError(
                            field=f"registries.{name}.repository",
                            message=f"'repository' must be 'pypi', 'testpypi', or a URL",
                            line=None
                        ))

        return ConfigValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def get_registry(self, name: str) -> Optional[RegistrySettings]:
        """
        Get settings for a specific registry (Tech Spec).

        Args:
            name: Registry name (npm, pypi, nuget, docker, github, crates).

        Returns:
            RegistrySettings if registry exists, None otherwise.
        """
        if self._config is None:
            return None
        return self._config.registries.get(name)

    def get_enabled_registries(self) -> List[str]:
        """
        Get list of enabled registry names (AC#2).

        Logs disabled registries as skipped.

        Returns:
            List of registry names that are enabled.
        """
        if self._config is None:
            return []

        enabled = []
        for name, settings in self._config.registries.items():
            if settings.enabled:
                enabled.append(name)
            else:
                logger.info(f"Registry {name} disabled in config")

        return enabled

    def validate_credentials(self, config: RegistryConfig) -> None:
        """
        Validate that required credential environment variables exist (AC#5).

        Raises ValueError with the missing variable name if any required
        credential is not set in the environment.

        Args:
            config: RegistryConfig to validate.

        Raises:
            ValueError: If a required credential env var is missing.
        """
        for name, settings in config.registries.items():
            if not settings.enabled:
                continue

            creds = settings.credentials

            # Check token_var
            if creds.token_var:
                if not os.environ.get(creds.token_var):
                    raise ValueError(
                        f"Missing required credential: {creds.token_var} "
                        f"for registry '{name}'"
                    )

            # Check username/password pair
            if creds.username_var:
                if not os.environ.get(creds.username_var):
                    raise ValueError(
                        f"Missing required credential: {creds.username_var} "
                        f"for registry '{name}'"
                    )
            if creds.password_var:
                if not os.environ.get(creds.password_var):
                    raise ValueError(
                        f"Missing required credential: {creds.password_var} "
                        f"for registry '{name}'"
                    )

    def _parse_config(self, raw_config: Dict[str, Any]) -> RegistryConfig:
        """
        Parse raw YAML config into RegistryConfig with defaults merged.

        Handles partial configs by merging with defaults (Edge Case 2).
        """
        # Extract global defaults
        global_defaults = raw_config.get("defaults", {})
        default_skip_existing = global_defaults.get("skip-existing", True)

        # Parse registries section
        registries_raw = raw_config.get("registries", {})
        registries: Dict[str, RegistrySettings] = {}

        # Handle Edge Case 6: Empty registries section {} means all disabled
        # vs no registries key at all means use defaults (BR-001)
        if "registries" not in raw_config:
            # No registries key - use defaults for all known registries (BR-001)
            for name in KNOWN_REGISTRIES:
                registries[name] = self._create_default_settings(
                    name, default_skip_existing
                )
        elif not registries_raw:
            # Empty registries: {} - means no registries enabled (Edge Case 6)
            pass  # Leave registries empty
        else:
            # Parse each registry
            for name, settings_raw in registries_raw.items():
                if name not in KNOWN_REGISTRIES:
                    logger.warning(f"Unknown registry '{name}' in config, ignoring")
                    continue

                if not isinstance(settings_raw, dict):
                    settings_raw = {}

                registries[name] = self._parse_registry_settings(
                    name, settings_raw, default_skip_existing
                )

        return RegistryConfig(
            registries=registries,
            defaults=global_defaults
        )

    def _create_default_settings(
        self,
        name: str,
        default_skip_existing: bool
    ) -> RegistrySettings:
        """Create default settings for a registry."""
        return RegistrySettings(
            name=name,
            enabled=True,
            registry_url=DEFAULT_ENDPOINTS.get(name),
            skip_existing=default_skip_existing,
            credentials=self._create_default_credentials(name),
            options={}
        )

    def _parse_registry_settings(
        self,
        name: str,
        settings_raw: Dict[str, Any],
        default_skip_existing: bool
    ) -> RegistrySettings:
        """Parse a single registry's settings with defaults merged."""
        # Parse enabled (default True)
        enabled = settings_raw.get("enabled", True)
        if not isinstance(enabled, bool):
            enabled = True

        # Parse skip_existing (inherit from global defaults)
        skip_existing = settings_raw.get(
            "skip-existing",
            settings_raw.get("skip_existing", default_skip_existing)
        )

        # Parse registry URL (varies by registry type)
        registry_url = self._parse_registry_url(name, settings_raw)

        # Parse credentials (custom or defaults)
        credentials = self._parse_credentials(name, settings_raw)

        # Collect remaining options
        options = self._parse_options(name, settings_raw)

        return RegistrySettings(
            name=name,
            enabled=enabled,
            registry_url=registry_url,
            skip_existing=skip_existing,
            credentials=credentials,
            options=options
        )

    def _parse_registry_url(
        self,
        name: str,
        settings_raw: Dict[str, Any]
    ) -> Optional[str]:
        """Parse registry URL from config, handling different field names."""
        # Different registries use different field names
        if name == "npm":
            return settings_raw.get("registry", DEFAULT_ENDPOINTS.get("npm"))
        elif name == "nuget":
            return settings_raw.get("source", DEFAULT_ENDPOINTS.get("nuget"))
        elif name == "pypi":
            # PyPI uses 'repository' which can be 'pypi', 'testpypi', or URL
            repo = settings_raw.get("repository", DEFAULT_ENDPOINTS.get("pypi"))
            return repo
        elif name == "docker":
            return settings_raw.get("registry", DEFAULT_ENDPOINTS.get("docker"))
        elif name == "github":
            return settings_raw.get("registry", DEFAULT_ENDPOINTS.get("github"))
        elif name == "crates":
            return settings_raw.get("registry", DEFAULT_ENDPOINTS.get("crates"))
        else:
            return settings_raw.get("registry")

    def _parse_credentials(
        self,
        name: str,
        settings_raw: Dict[str, Any]
    ) -> CredentialConfig:
        """Parse credentials config, using defaults if not specified (BR-003)."""
        creds_raw = settings_raw.get("credentials", {})

        if creds_raw:
            # Custom credentials override defaults completely (BR-003)
            return CredentialConfig(
                token_var=creds_raw.get("token_var"),
                username_var=creds_raw.get("username_var"),
                password_var=creds_raw.get("password_var")
            )
        else:
            # Use defaults
            return self._create_default_credentials(name)

    def _create_default_credentials(self, name: str) -> CredentialConfig:
        """Create default credentials for a registry."""
        defaults = DEFAULT_CREDENTIALS.get(name, {})
        return CredentialConfig(
            token_var=defaults.get("token_var"),
            username_var=defaults.get("username_var"),
            password_var=defaults.get("password_var")
        )

    def _parse_options(
        self,
        name: str,
        settings_raw: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse registry-specific options (fields not handled elsewhere)."""
        # Fields handled by other parsers
        handled_fields = {
            "enabled", "registry", "source", "repository",
            "skip-existing", "skip_existing", "credentials"
        }

        options = {}
        for key, value in settings_raw.items():
            if key not in handled_fields:
                options[key] = value

        return options
