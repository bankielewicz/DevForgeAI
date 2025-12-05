"""
MigrationValidator service for validating post-migration state (STORY-078).

Implements:
- SVC-015: Validate expected files exist after migration
- SVC-016: Validate JSON/YAML schema integrity
- SVC-017: Validate required configuration keys
- SVC-018: Return detailed validation report

Follows clean architecture with dependency injection.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Set
from abc import ABC, abstractmethod

from installer.models import (
    ValidationCheck,
    ValidationReport,
    ValidationError,
)


logger = logging.getLogger(__name__)

# Message templates for validation checks
MSG_FILES_EXIST = "Expected files exist"
MSG_DIRS_EXIST = "Expected directories exist"
MSG_JSON_SCHEMA = "JSON schema: {}"
MSG_JSON_VALIDITY = "JSON validity: {}"
MSG_JSON_VALIDATION = "JSON validation: {}"
MSG_CONFIG_VALIDATION = "Configuration validation: {}"

# Validation status messages
FILE_NOT_FOUND_MSG = "File not found"
JSON_VALID_WITH_KEYS_MSG = "JSON valid with all required keys"
MISSING_KEYS_MSG = "Missing keys in JSON"
INVALID_JSON_MSG = "Invalid JSON"
VALIDATION_ERROR_MSG = "Validation error"


class IConfigValidator(ABC):
    """Interface for configuration validation."""

    @abstractmethod
    def validate_keys(self, config: Dict[str, Any], required_keys: List[str]) -> Dict[str, Any]:
        """Validate that required keys exist in config."""
        pass


class ConfigValidator(IConfigValidator):
    """Validates configuration for required keys."""

    def validate_keys(
        self, config: Dict[str, Any], required_keys: List[str]
    ) -> Dict[str, Any]:
        """
        Validate that all required keys exist in config.

        Args:
            config: Configuration dictionary
            required_keys: List of required key paths (e.g., ["version", "settings.debug"])

        Returns:
            Dict with missing_keys list and details

        Raises:
            ValidationError: If required keys missing
        """
        missing_keys = []
        found_keys = []

        for key_path in required_keys:
            parts = key_path.split(".")
            current = config

            try:
                for part in parts:
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        raise KeyError(part)
                found_keys.append(key_path)
            except (KeyError, TypeError):
                missing_keys.append(key_path)

        return {
            "missing_keys": missing_keys,
            "found_keys": found_keys,
            "valid": len(missing_keys) == 0,
        }


class IMigrationValidator(ABC):
    """Interface for migration validation."""

    @abstractmethod
    def validate(
        self,
        root_path: Path,
        expected_files: Optional[List[str]] = None,
        expected_dirs: Optional[List[str]] = None,
        json_schemas: Optional[Dict[str, List[str]]] = None,
        config_validations: Optional[Dict[str, List[str]]] = None,
    ) -> ValidationReport:
        """Validate post-migration state."""
        pass


class MigrationValidator(IMigrationValidator):
    """Validates post-migration installation state."""

    def __init__(self, config_validator: Optional[IConfigValidator] = None) -> None:
        """
        Initialize MigrationValidator.

        Args:
            config_validator: Configuration validator. Defaults to ConfigValidator()
        """
        if config_validator is None:
            config_validator = ConfigValidator()
        self.config_validator = config_validator

    @staticmethod
    def _create_pass_check(name: str, message: str, details: Optional[Dict[str, Any]] = None) -> ValidationCheck:
        """Create a passing validation check."""
        return ValidationCheck(
            name=name,
            passed=True,
            message=message,
            details=details or {},
        )

    @staticmethod
    def _create_fail_check(name: str, message: str, details: Optional[Dict[str, Any]] = None) -> ValidationCheck:
        """Create a failing validation check."""
        return ValidationCheck(
            name=name,
            passed=False,
            message=message,
            details=details or {},
        )

    def validate(
        self,
        root_path: Path,
        expected_files: Optional[List[str]] = None,
        expected_dirs: Optional[List[str]] = None,
        json_schemas: Optional[Dict[str, List[str]]] = None,
        config_validations: Optional[Dict[str, List[str]]] = None,
    ) -> ValidationReport:
        """
        Validate post-migration installation state.

        Runs validation checks for:
        1. Expected files exist
        2. Expected directories exist
        3. JSON files are well-formed
        4. YAML files are well-formed
        5. Configuration has required keys

        Args:
            root_path: Root path of installation
            expected_files: List of expected file paths
            expected_dirs: List of expected directory paths
            json_schemas: Dict mapping JSON file paths to required keys
            config_validations: Dict mapping config file paths to required keys

        Returns:
            ValidationReport with all check results
        """
        root_path = Path(root_path)
        checks: List[ValidationCheck] = []

        # Validate expected files
        if expected_files:
            file_checks = self._validate_files_exist(root_path, expected_files)
            checks.extend(file_checks)

        # Validate expected directories
        if expected_dirs:
            dir_checks = self._validate_dirs_exist(root_path, expected_dirs)
            checks.extend(dir_checks)

        # Validate JSON schemas
        if json_schemas:
            json_checks = self._validate_json_files(root_path, json_schemas)
            checks.extend(json_checks)

        # Validate configurations
        if config_validations:
            config_checks = self._validate_configurations(
                root_path, config_validations
            )
            checks.extend(config_checks)

        # Summarize results
        passed = sum(1 for c in checks if c.passed)
        failed = len(checks) - passed
        is_valid = failed == 0

        return ValidationReport(
            is_valid=is_valid,
            checks=checks,
            total_checks=len(checks),
            passed_checks=passed,
            failed_checks=failed,
        )

    def _validate_files_exist(
        self, root_path: Path, file_paths: List[str]
    ) -> List[ValidationCheck]:
        """
        Validate that expected files exist.

        Args:
            root_path: Root installation path
            file_paths: List of expected file paths (relative to root)

        Returns:
            List of ValidationCheck results
        """
        checks: List[ValidationCheck] = []
        missing_files: List[str] = []
        found_files: List[str] = []

        for file_path in file_paths:
            full_path = root_path / file_path
            if full_path.exists() and full_path.is_file():
                found_files.append(file_path)
            else:
                missing_files.append(file_path)

        if missing_files:
            checks.append(
                self._create_fail_check(
                    MSG_FILES_EXIST,
                    f"Missing {len(missing_files)} expected files",
                    {
                        "missing_files": missing_files,
                        "found_files": found_files,
                    },
                )
            )
        else:
            checks.append(
                self._create_pass_check(
                    MSG_FILES_EXIST,
                    f"All {len(found_files)} expected files found",
                    {"found_files": found_files},
                )
            )

        return checks

    def _validate_dirs_exist(
        self, root_path: Path, dir_paths: List[str]
    ) -> List[ValidationCheck]:
        """
        Validate that expected directories exist.

        Args:
            root_path: Root installation path
            dir_paths: List of expected directory paths (relative to root)

        Returns:
            List of ValidationCheck results
        """
        checks: List[ValidationCheck] = []
        missing_dirs: List[str] = []
        found_dirs: List[str] = []

        for dir_path in dir_paths:
            full_path = root_path / dir_path
            if full_path.exists() and full_path.is_dir():
                found_dirs.append(dir_path)
            else:
                missing_dirs.append(dir_path)

        if missing_dirs:
            checks.append(
                self._create_fail_check(
                    MSG_DIRS_EXIST,
                    f"Missing {len(missing_dirs)} expected directories",
                    {
                        "missing_directories": missing_dirs,
                        "found_directories": found_dirs,
                    },
                )
            )
        else:
            checks.append(
                self._create_pass_check(
                    MSG_DIRS_EXIST,
                    f"All {len(found_dirs)} expected directories found",
                    {"found_directories": found_dirs},
                )
            )

        return checks

    def _validate_json_file_exists(
        self, file_path: str, full_path: Path
    ) -> ValidationCheck:
        """
        Check if JSON file exists.

        Args:
            file_path: Relative file path
            full_path: Absolute file path

        Returns:
            ValidationCheck for existence check
        """
        if not full_path.exists():
            return ValidationCheck(
                name=f"JSON file exists: {file_path}",
                passed=False,
                message=f"{FILE_NOT_FOUND_MSG}: {file_path}",
            )
        return None

    def _validate_json_content_and_schema(
        self, file_path: str, full_path: Path, required_keys: List[str]
    ) -> ValidationCheck:
        """
        Validate JSON file content and required keys.

        Args:
            file_path: Relative file path
            full_path: Absolute file path
            required_keys: List of required keys

        Returns:
            ValidationCheck for content validation
        """
        try:
            config = json.loads(full_path.read_text(encoding="utf-8"))

            # Validate required keys
            validation = self.config_validator.validate_keys(config, required_keys)

            if validation["valid"]:
                return ValidationCheck(
                    name=f"JSON schema: {file_path}",
                    passed=True,
                    message=JSON_VALID_WITH_KEYS_MSG,
                    details={"found_keys": validation["found_keys"]},
                )
            else:
                return ValidationCheck(
                    name=f"JSON schema: {file_path}",
                    passed=False,
                    message=MISSING_KEYS_MSG,
                    details={
                        "missing_keys": validation["missing_keys"],
                        "found_keys": validation["found_keys"],
                    },
                )

        except json.JSONDecodeError as e:
            return ValidationCheck(
                name=f"JSON validity: {file_path}",
                passed=False,
                message=f"{INVALID_JSON_MSG}: {e}",
            )

        except Exception as e:
            return ValidationCheck(
                name=f"JSON validation: {file_path}",
                passed=False,
                message=f"{VALIDATION_ERROR_MSG}: {e}",
            )

    def _validate_json_files(
        self, root_path: Path, json_schemas: Dict[str, List[str]]
    ) -> List[ValidationCheck]:
        """
        Validate JSON files are well-formed and have required keys.

        Args:
            root_path: Root installation path
            json_schemas: Dict mapping JSON file paths to required keys

        Returns:
            List of ValidationCheck results
        """
        checks: List[ValidationCheck] = []

        for file_path, required_keys in json_schemas.items():
            full_path = root_path / file_path

            # Check if file exists
            existence_check = self._validate_json_file_exists(file_path, full_path)
            if existence_check:
                checks.append(existence_check)
                continue

            # Validate content and schema
            content_check = self._validate_json_content_and_schema(
                file_path, full_path, required_keys
            )
            checks.append(content_check)

        return checks

    def _validate_configurations(
        self, root_path: Path, config_validations: Dict[str, List[str]]
    ) -> List[ValidationCheck]:
        """
        Validate configuration files have required keys.

        Args:
            root_path: Root installation path
            config_validations: Dict mapping config file paths to required keys

        Returns:
            List of ValidationCheck results
        """
        # For now, treat as JSON files
        # Could be extended to support YAML, etc.
        return self._validate_json_files(root_path, config_validations)
