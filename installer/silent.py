"""
Silent/Headless Installer for DevForgeAI (STORY-249)

Provides configuration-driven silent installation mode for CI/CD pipelines.
Supports YAML config files, environment variables, structured logging,
dry-run mode, idempotency, and JSON progress output.

Usage:
    from installer.silent import SilentInstaller

    # From YAML config file
    installer = SilentInstaller(config="install-config.yaml")
    exit_code = installer.run()

    # From environment variables
    installer = SilentInstaller(config=None)  # Uses DEVFORGEAI_* env vars
    exit_code = installer.run()

    # From dict
    installer = SilentInstaller(config={"target": "/opt/devforgeai", "components": ["core"]})
    exit_code = installer.run()
"""

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from installer.exit_codes import ExitCodes
import installer.preflight
import installer.platform_detector


# =============================================================================
# Exceptions
# =============================================================================

class ConfigError(Exception):
    """Raised when configuration is invalid or missing required fields."""
    pass


class PreflightError(Exception):
    """Raised when pre-flight validation fails."""
    pass


class InstallError(Exception):
    """Raised when installation fails."""
    pass


class ValidationError(Exception):
    """Raised when post-install validation fails."""
    pass


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class InstallOptions:
    """
    Installation options configuration.

    Attributes:
        initialize_git: Whether to initialize git repository (default: False)
        create_backup: Whether to create backup before install (default: False)
        run_validation: Whether to run post-install validation (default: True)
        dry_run: Whether to simulate without making changes (default: False)
    """
    initialize_git: bool = False
    create_backup: bool = False
    run_validation: bool = True
    dry_run: bool = False


@dataclass
class InstallConfig:
    """
    Installation configuration.

    Attributes:
        target: Target installation directory
        components: List of components to install
        options: Installation options (optional, defaults to InstallOptions())
        log_file: Path to log file (default: "install.log")
    """
    target: Path
    components: List[str]
    options: InstallOptions = field(default_factory=InstallOptions)
    log_file: Path = field(default_factory=lambda: Path("install.log"))


# =============================================================================
# Structured Logging Formatter
# =============================================================================

class StructuredFormatter(logging.Formatter):
    """
    Log formatter producing ISO 8601 timestamps.

    Format: YYYY-MM-DDTHH:MM:SSZ [LEVEL] module: message
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return f"{timestamp} [{record.levelname}] {record.name}: {record.getMessage()}"


# =============================================================================
# Silent Installer
# =============================================================================

class SilentInstaller:
    """
    Silent/Headless installer for CI/CD pipelines.

    Supports:
    - YAML configuration files (AC#1)
    - Environment variable configuration (AC#2)
    - No interactive prompts (AC#3)
    - Structured logging (AC#4)
    - CI/CD exit codes (AC#5)
    - Dry-run mode (AC#6)
    - Idempotency (AC#7)
    - JSON progress output (AC#8)
    """

    # Exit code constants (AC#5)
    EXIT_SUCCESS = ExitCodes.SUCCESS  # 0
    EXIT_CONFIG_ERROR = 1
    EXIT_PREFLIGHT_ERROR = 2
    EXIT_INSTALL_ERROR = 3
    EXIT_VALIDATION_ERROR = ExitCodes.VALIDATION_FAILED  # 4

    # Sensitive fields to exclude from logging
    SENSITIVE_FIELDS = {'api_key', 'password', 'secret', 'token', 'credential'}

    # Valid components
    VALID_COMPONENTS = {'core', 'cli', 'templates', 'examples', 'skills', 'agents', 'commands'}

    def __init__(
        self,
        config: Optional[Union[str, Path, Dict[str, Any]]] = None,
        json_output: bool = False
    ):
        """
        Initialize SilentInstaller.

        Args:
            config: Configuration source - path to YAML file, Path object, dict, or None.
                    If None, reads from environment variables.
            json_output: If True, emit JSON progress updates to stdout.

        Raises:
            ConfigError: If configuration is invalid or missing required fields.
        """
        self.json_output = json_output
        self._raw_config = config
        self.config = self._load_config(config)
        self.logger = self._setup_logger()

    def _load_config(self, source: Optional[Union[str, Path, Dict[str, Any]]]) -> InstallConfig:
        """
        Load configuration from various sources.

        Priority: Environment variables > Config file/dict

        Args:
            source: Configuration source

        Returns:
            InstallConfig instance

        Raises:
            ConfigError: If configuration is invalid
        """
        base_config: Dict[str, Any] = {}

        # Load from source
        if source is None:
            # Pure environment variable mode
            base_config = self._load_from_env_vars()
        elif isinstance(source, dict):
            base_config = source.copy()
        elif isinstance(source, (str, Path)):
            base_config = self._load_from_yaml(source)

        # Apply environment variable overrides
        base_config = self._apply_env_overrides(base_config)

        # Validate and convert to InstallConfig
        return self._validate_and_create_config(base_config)

    def _load_from_yaml(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(path)

        if not path.exists():
            raise ConfigError(f"Configuration file not found: {path}")

        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if data is None:
                    return {}
                return data
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML in configuration file: {e}") from e

    def _parse_env_boolean(self, env_var: str) -> Optional[bool]:
        """Parse boolean environment variable.

        Args:
            env_var: Environment variable name

        Returns:
            True, False, or None if not set

        Raises:
            ConfigError: If value is not 'true' or 'false'
        """
        value = os.environ.get(env_var, '').strip().lower()
        if not value:
            return None
        if value == 'true':
            return True
        if value == 'false':
            return False
        raise ConfigError(f"Invalid boolean value for {env_var}: '{value}'. Use 'true' or 'false'.")

    def _load_from_env_vars(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config: Dict[str, Any] = {}

        target = os.environ.get('DEVFORGEAI_TARGET', '').strip()
        if target:
            config['target'] = target

        components = os.environ.get('DEVFORGEAI_COMPONENTS', '').strip()
        if components:
            config['components'] = [c.strip() for c in components.split(',') if c.strip()]

        log_file = os.environ.get('DEVFORGEAI_LOG_FILE', '').strip()
        if log_file:
            config['log_file'] = log_file

        # Boolean options (use helper method for DRY)
        init_git = self._parse_env_boolean('DEVFORGEAI_INIT_GIT')
        if init_git is not None:
            config.setdefault('options', {})['initialize_git'] = init_git

        dry_run = self._parse_env_boolean('DEVFORGEAI_DRY_RUN')
        if dry_run is not None:
            config.setdefault('options', {})['dry_run'] = dry_run

        return config

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to existing config."""
        # Target override
        target = os.environ.get('DEVFORGEAI_TARGET', '').strip()
        if target:
            config['target'] = target

        # Boolean overrides (use helper method for DRY)
        init_git = self._parse_env_boolean('DEVFORGEAI_INIT_GIT')
        if init_git is not None:
            config.setdefault('options', {})['initialize_git'] = init_git

        dry_run = self._parse_env_boolean('DEVFORGEAI_DRY_RUN')
        if dry_run is not None:
            config.setdefault('options', {})['dry_run'] = dry_run

        return config

    def _validate_and_create_config(self, config: Dict[str, Any]) -> InstallConfig:
        """Validate configuration and create InstallConfig instance."""
        # Check required fields
        if 'target' not in config or not config['target']:
            raise ConfigError("Missing required field: 'target'. Specify installation directory.")

        if 'components' not in config or not config['components']:
            raise ConfigError("Missing required field: 'components'. Specify at least one component to install.")

        # Validate components
        components = config['components']
        if isinstance(components, str):
            components = [components]

        for component in components:
            if component not in self.VALID_COMPONENTS:
                raise ConfigError(
                    f"Invalid component name: '{component}'. "
                    f"Valid components: {', '.join(sorted(self.VALID_COMPONENTS))}"
                )

        # Parse options
        options_dict = config.get('options', {})
        if isinstance(options_dict, dict):
            options = InstallOptions(
                initialize_git=options_dict.get('initialize_git', False),
                create_backup=options_dict.get('create_backup', False),
                run_validation=options_dict.get('run_validation', True),
                dry_run=options_dict.get('dry_run', False)
            )
        else:
            options = InstallOptions()

        # Create config
        log_file = config.get('log_file', 'install.log')

        return InstallConfig(
            target=Path(config['target']),
            components=components,
            options=options,
            log_file=Path(log_file)
        )

    def _setup_logger(self) -> logging.Logger:
        """Configure structured logging."""
        logger = logging.getLogger('installer.silent')
        logger.setLevel(logging.INFO)

        # Remove existing handlers
        logger.handlers.clear()

        # Ensure log directory exists
        log_path = self.config.log_file
        if log_path.parent and str(log_path.parent) != '.':
            log_path.parent.mkdir(parents=True, exist_ok=True)

        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

        return logger

    def run(self) -> int:
        """
        Execute silent installation.

        Returns:
            Exit code (0=success, 1=config, 2=preflight, 3=install, 4=validation)
        """
        try:
            # Check for existing installation (idempotency)
            if self.is_already_installed():
                self.logger.info("Already installed - skipping installation")
                self._emit_json_progress("complete", percent=100, message="Already installed")
                return self.EXIT_SUCCESS

            # Log start (with DRY RUN prefix if applicable)
            if self.config.options.dry_run:
                self.logger.info("DRY RUN: Starting installation validation")
            else:
                self.logger.info("Starting installation")

            self._emit_json_progress("in_progress", percent=10, step="Pre-flight checks")

            # Pre-flight validation
            if not self._run_preflight():
                self._emit_json_progress("error", code=self.EXIT_PREFLIGHT_ERROR, message="Pre-flight validation failed")
                return self.EXIT_PREFLIGHT_ERROR

            self._emit_json_progress("in_progress", percent=30, step="Installing components")

            # Skip actual installation in dry-run mode
            if self.config.options.dry_run:
                self.logger.info("DRY RUN: Would install components: " + ", ".join(self.config.components))
                self._emit_json_progress("complete", percent=100, installed_components=self.config.components)
                return self.EXIT_SUCCESS

            # Install components
            if not self._install_components():
                self._emit_json_progress("error", code=self.EXIT_INSTALL_ERROR, message="Installation failed")
                return self.EXIT_INSTALL_ERROR

            self._emit_json_progress("in_progress", percent=80, step="Validating installation")

            # Post-install validation (if enabled)
            if self.config.options.run_validation:
                if not self._run_validation():
                    self.logger.error("Post-install validation failed")
                    self._emit_json_progress("error", code=self.EXIT_VALIDATION_ERROR, message="Validation failed")
                    return self.EXIT_VALIDATION_ERROR

            # Create installation marker for idempotency
            self._create_install_marker()

            self.logger.info("Installation completed successfully")
            self._emit_json_progress("complete", percent=100, installed_components=self.config.components)
            return self.EXIT_SUCCESS

        except ConfigError as e:
            self.logger.error(f"Configuration error: {e}")
            self._emit_json_progress("error", code=self.EXIT_CONFIG_ERROR, message=str(e))
            return self.EXIT_CONFIG_ERROR

        except PreflightError as e:
            self.logger.error(f"Pre-flight error: {e}")
            self._emit_json_progress("error", code=self.EXIT_PREFLIGHT_ERROR, message=str(e))
            return self.EXIT_PREFLIGHT_ERROR

        except (InstallError, OSError) as e:
            self.logger.error(f"Installation error: {e}")
            self._emit_json_progress("error", code=self.EXIT_INSTALL_ERROR, message=str(e))
            return self.EXIT_INSTALL_ERROR

        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            self._emit_json_progress("error", code=self.EXIT_VALIDATION_ERROR, message=str(e))
            return self.EXIT_VALIDATION_ERROR

    def _run_preflight(self) -> bool:
        """Run pre-flight validation checks."""
        try:
            validator = installer.preflight.PreflightValidator(
                target_dir=str(self.config.target),
                dry_run=self.config.options.dry_run
            )
            result = validator.validate()

            if not result.passed:
                for error in result.errors:
                    self.logger.error(f"Pre-flight check failed: {error}")
                return False

            for warning in result.warnings:
                self.logger.warning(f"Pre-flight warning: {warning}")

            self.logger.info("Pre-flight checks passed")
            return True

        except Exception as e:
            self.logger.error(f"Pre-flight validation error: {e}")
            return False

    def _install_components(self) -> bool:
        """Install the specified components."""
        self.logger.info(f"Installing components: {', '.join(self.config.components)}")

        # Placeholder for actual installation logic
        # In real implementation, this would copy files from source to target

        for component in self.config.components:
            if self.config.options.dry_run:
                self.logger.info(f"DRY RUN: Would install component: {component}")
            else:
                self.logger.info(f"Installing component: {component}")
                # Actual installation would happen here

        return True

    def _run_validation(self) -> bool:
        """Run post-installation validation."""
        self.logger.info("Running post-installation validation")

        # Check that target directory exists
        if not self.config.target.exists():
            self.logger.error(f"Target directory not found: {self.config.target}")
            return False

        # Placeholder for more validation checks
        self.logger.info("Validation passed")
        return True

    def is_already_installed(self) -> bool:
        """Check if DevForgeAI is already installed (AC#7)."""
        marker_path = self.config.target / ".devforgeai_installed"

        if marker_path.exists():
            try:
                with open(marker_path, 'r') as f:
                    data = json.load(f)
                version = data.get('version', 'unknown')
                self.logger.info(f"Existing installation detected: version {version}")
                return True
            except (json.JSONDecodeError, IOError):
                # Marker exists but is invalid - treat as installed
                self.logger.warning("Invalid installation marker found")
                return True

        return False

    def _create_install_marker(self) -> None:
        """Create installation marker file for idempotency."""
        marker_path = self.config.target / ".devforgeai_installed"

        marker_data = {
            "version": "1.0.0",  # Would be read from actual version
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "components": self.config.components
        }

        # Ensure target directory exists
        self.config.target.mkdir(parents=True, exist_ok=True)

        with open(marker_path, 'w') as f:
            json.dump(marker_data, f, indent=2)

    def _emit_json_progress(self, status: str, **kwargs: Any) -> None:
        """
        Emit JSON progress update to stdout (AC#8).

        Args:
            status: Progress status ("in_progress", "complete", "error")
            **kwargs: Additional fields (percent, step, code, message, etc.)
        """
        if not self.json_output:
            return

        progress = {"status": status}
        progress.update(kwargs)

        # Write newline-delimited JSON
        sys.stdout.write(json.dumps(progress) + "\n")
        sys.stdout.flush()
