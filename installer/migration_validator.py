"""
STORY-078: Migration Validator Service.

Validates post-migration state including file existence, schema validation,
and configuration key checking.

AC Mapping:
- AC#5: Migration Validation
  - Expected files verified to exist
  - Schemas validated (JSON/YAML well-formed)
  - Configuration tested for required keys
  - Validation failures trigger rollback
  - Validation results logged with pass/fail for each check

Technical Specification:
- SVC-015: Validate expected files exist after migration
- SVC-016: Validate JSON/YAML schema integrity
- SVC-017: Validate required configuration keys
- SVC-018: Return detailed validation report
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any

# Try to import yaml, but it's optional (stdlib-only requirement)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class SchemaValidationResult:
    """
    Result of validating a single file's schema.

    Attributes:
        passed: True if file contains valid JSON/YAML.
        error: Error message if validation failed, None otherwise.
    """
    passed: bool
    error: Optional[str] = None


@dataclass
class ConfigKeyValidationResult:
    """
    Result of validating required configuration keys.

    Attributes:
        passed: True if all required keys are present.
        missing_keys: List of keys that were not found.
    """
    passed: bool
    missing_keys: List[str] = field(default_factory=list)


@dataclass
class FileExistenceResult:
    """
    Result of file existence validation.

    Attributes:
        all_passed: True if all expected files exist.
        passed: List of files that exist.
        failed: List of files that do not exist.
    """
    all_passed: bool
    passed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)


@dataclass
class SchemaValidationReport:
    """
    Report of schema validations for multiple files.

    Attributes:
        all_passed: True if all files have valid schemas.
        passed: List of files with valid schemas.
        failed: List of files with invalid schemas.
        errors: Dictionary mapping file paths to error messages.
    """
    all_passed: bool
    passed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)


@dataclass
class ConfigKeyReport:
    """
    Report of configuration key validations for multiple files.

    Attributes:
        all_passed: True if all files have all required keys.
        passed: List of files with all required keys.
        failed: List of files missing required keys.
        missing_keys: Dictionary mapping file paths to lists of missing keys.
    """
    all_passed: bool
    passed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    missing_keys: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """
    Complete validation report (SVC-018).

    Aggregates results from file existence, schema, and config key validations.

    Attributes:
        overall_passed: True if all validations passed.
        file_existence: Results of file existence checks.
        schema_validation: Results of JSON/YAML schema checks.
        config_keys: Results of required key checks.
        should_rollback: True if validation failure requires rollback.
    """
    overall_passed: bool
    file_existence: FileExistenceResult = field(
        default_factory=lambda: FileExistenceResult(all_passed=True)
    )
    schema_validation: SchemaValidationReport = field(
        default_factory=lambda: SchemaValidationReport(all_passed=True)
    )
    config_keys: ConfigKeyReport = field(
        default_factory=lambda: ConfigKeyReport(all_passed=True)
    )
    should_rollback: bool = False


class MigrationValidator:
    """
    Validates post-migration state (AC#5).

    Performs three types of validation:
    1. File existence - verifies expected files were created
    2. Schema validation - ensures JSON/YAML files are well-formed
    3. Config key validation - checks required keys are present

    Validation failures trigger the should_rollback flag for the orchestrator.
    """

    def __init__(self, logger: Any = None) -> None:
        """
        Initialize migration validator.

        Args:
            logger: Optional logger for validation result messages.
        """
        self._logger = logger

    @property
    def logger(self) -> Any:
        """Return the logger instance (for backward compatibility)."""
        return self._logger

    def validate(
        self,
        project_root: Path,
        expected_files: Optional[List[str]] = None,
        json_files: Optional[List[str]] = None,
        yaml_files: Optional[List[str]] = None,
        config_keys: Optional[Dict[str, List[str]]] = None
    ) -> ValidationReport:
        """
        Run all validations and return comprehensive report (SVC-018).

        Executes file existence, schema, and config key validations in sequence.
        Any failure sets overall_passed to False and should_rollback to True.

        Args:
            project_root: Path to project root directory.
            expected_files: List of relative paths that must exist.
            json_files: List of JSON files to validate schema.
            yaml_files: List of YAML files to validate schema.
            config_keys: Dict of {file_path: [required_keys]} to validate.

        Returns:
            ValidationReport with all validation results.
        """
        report = ValidationReport(overall_passed=True)

        # Run each validation type
        report.file_existence = self._run_file_existence_validation(
            project_root, expected_files, report
        )
        report.schema_validation = self._run_schema_validation(
            project_root, json_files, yaml_files, report
        )
        report.config_keys = self._run_config_key_validation(
            project_root, config_keys, report
        )

        # Set rollback flag based on overall result
        report.should_rollback = not report.overall_passed
        self._log_validation_summary(report)

        return report

    def _run_file_existence_validation(
        self,
        project_root: Path,
        expected_files: Optional[List[str]],
        report: ValidationReport
    ) -> FileExistenceResult:
        """Run file existence validation (SVC-015)."""
        if not expected_files:
            return FileExistenceResult(all_passed=True)

        result = self._validate_files_exist(project_root, expected_files)
        if not result.all_passed:
            report.overall_passed = False
            self._log_validation_result(
                "File existence check", len(result.passed), len(result.failed)
            )
        return result

    def _run_schema_validation(
        self,
        project_root: Path,
        json_files: Optional[List[str]],
        yaml_files: Optional[List[str]],
        report: ValidationReport
    ) -> SchemaValidationReport:
        """Run schema validation (SVC-016)."""
        if not json_files and not yaml_files:
            return SchemaValidationReport(all_passed=True)

        result = self._validate_schemas(
            project_root, json_files or [], yaml_files or []
        )
        if not result.all_passed:
            report.overall_passed = False
            self._log_validation_result(
                "Schema validation", len(result.passed), len(result.failed)
            )
        return result

    def _run_config_key_validation(
        self,
        project_root: Path,
        config_keys: Optional[Dict[str, List[str]]],
        report: ValidationReport
    ) -> ConfigKeyReport:
        """Run config key validation (SVC-017)."""
        if not config_keys:
            return ConfigKeyReport(all_passed=True)

        result = self._validate_config_keys(project_root, config_keys)
        if not result.all_passed:
            report.overall_passed = False
            self._log_validation_result(
                "Config key validation", len(result.passed), len(result.failed)
            )
        return result

    def _log_validation_result(self, check_name: str, passed: int, failed: int) -> None:
        """Log a validation result summary."""
        if self._logger:
            self._logger.log_info(f"{check_name}: {passed} passed, {failed} failed")

    def _log_validation_summary(self, report: ValidationReport) -> None:
        """Log the overall validation status."""
        if self._logger:
            status = "PASSED" if report.overall_passed else "FAILED"
            self._logger.log_info(f"Migration validation: {status}")

    def validate_schema(self, file_path: Path, file_type: str) -> SchemaValidationResult:
        """
        Validate a single file's schema (SVC-016).

        Checks that the file contains well-formed JSON or YAML content.

        Args:
            file_path: Path to file to validate.
            file_type: "json" or "yaml".

        Returns:
            SchemaValidationResult with pass/fail and error message.
        """
        try:
            content = self._read_file_content(file_path)

            if not content.strip():
                return SchemaValidationResult(passed=False, error="File is empty")

            return self._validate_content(content, file_type)

        except json.JSONDecodeError as e:
            return SchemaValidationResult(passed=False, error=f"JSON parse error: {e}")
        except PermissionError:
            return SchemaValidationResult(passed=False, error="Permission denied reading file")
        except UnicodeDecodeError as e:
            return SchemaValidationResult(passed=False, error=f"File encoding error: {e}")
        except Exception as e:
            return SchemaValidationResult(passed=False, error=f"Validation error: {e}")

    def _read_file_content(self, file_path: Path) -> str:
        """Read file content with explicit open() for test mocking."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _validate_content(self, content: str, file_type: str) -> SchemaValidationResult:
        """
        Validate content based on file type.

        Args:
            content: File content as string.
            file_type: "json" or "yaml".

        Returns:
            SchemaValidationResult indicating success or failure.
        """
        if file_type == "json":
            json.loads(content)
        elif file_type == "yaml":
            self._validate_yaml_content(content)

        return SchemaValidationResult(passed=True)

    def _validate_yaml_content(self, content: str) -> None:
        """
        Validate YAML content.

        Uses PyYAML if available, otherwise performs basic syntax checks.

        Args:
            content: YAML content as string.

        Raises:
            Exception: If YAML is invalid (via yaml library or basic check).
        """
        if YAML_AVAILABLE:
            yaml.safe_load(content)
        else:
            self._validate_yaml_basic(content)

    def _validate_yaml_basic(self, content: str) -> None:
        """
        Basic YAML validation without external library.

        Checks for common YAML syntax errors like inconsistent indentation.

        Args:
            content: YAML content as string.

        Raises:
            ValueError: If indentation error detected.
        """
        lines = content.split('\n')
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if not stripped or stripped.startswith('#'):
                continue

            indent = len(line) - len(stripped)
            if ':' in stripped and indent > 0 and i > 0:
                prev_line = lines[i - 1]
                prev_stripped = prev_line.lstrip()
                prev_indent = len(prev_line) - len(prev_stripped)

                # Detect excessive indentation after non-block line
                if prev_stripped and not prev_stripped.endswith(':'):
                    if indent > prev_indent + 2:
                        raise ValueError(f"YAML indentation error at line {i + 1}")

    def validate_config_keys(
        self,
        file_path: Path,
        required_keys: List[str]
    ) -> ConfigKeyValidationResult:
        """
        Validate required configuration keys exist (SVC-017).

        Supports dot notation for nested keys (e.g., "database.host").

        Args:
            file_path: Path to config file (JSON).
            required_keys: List of required keys (supports dot notation for nested).

        Returns:
            ConfigKeyValidationResult with missing keys list.
        """
        try:
            content = json.loads(file_path.read_text())
            missing = [key for key in required_keys if not self._key_exists(content, key)]

            return ConfigKeyValidationResult(
                passed=len(missing) == 0,
                missing_keys=missing
            )

        except (json.JSONDecodeError, FileNotFoundError, PermissionError):
            return ConfigKeyValidationResult(
                passed=False,
                missing_keys=required_keys
            )

    def _key_exists(self, content: Dict[str, Any], key: str) -> bool:
        """
        Check if a key exists in the content dictionary.

        Supports dot notation for nested keys.

        Args:
            content: Dictionary to search.
            key: Key to find (may contain dots for nesting).

        Returns:
            True if key exists, False otherwise.
        """
        if '.' not in key:
            return key in content

        # Navigate nested structure
        parts = key.split('.')
        current = content
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        return True

    def _validate_files_exist(
        self,
        project_root: Path,
        expected_files: List[str]
    ) -> FileExistenceResult:
        """
        Validate expected files exist (SVC-015).

        Args:
            project_root: Path to project root.
            expected_files: List of relative paths.

        Returns:
            FileExistenceResult with passed/failed lists.
        """
        result = FileExistenceResult(all_passed=True)

        for file_path in expected_files:
            full_path = project_root / file_path
            if full_path.exists():
                result.passed.append(file_path)
            else:
                result.failed.append(file_path)
                result.all_passed = False

        return result

    def _validate_schemas(
        self,
        project_root: Path,
        json_files: List[str],
        yaml_files: List[str]
    ) -> SchemaValidationReport:
        """
        Validate schemas for multiple files (SVC-016).

        Args:
            project_root: Path to project root.
            json_files: List of JSON file relative paths.
            yaml_files: List of YAML file relative paths.

        Returns:
            SchemaValidationReport with results.
        """
        report = SchemaValidationReport(all_passed=True)

        # Validate all files using unified helper
        self._validate_file_list(report, project_root, json_files, "json")
        self._validate_file_list(report, project_root, yaml_files, "yaml")

        return report

    def _validate_file_list(
        self,
        report: SchemaValidationReport,
        project_root: Path,
        files: List[str],
        file_type: str
    ) -> None:
        """
        Validate a list of files and update the report.

        Args:
            report: Report to update with results.
            project_root: Path to project root.
            files: List of file relative paths.
            file_type: "json" or "yaml".
        """
        for file_path in files:
            full_path = project_root / file_path
            result = self.validate_schema(full_path, file_type)

            if result.passed:
                report.passed.append(file_path)
            else:
                report.failed.append(file_path)
                report.errors[file_path] = result.error
                report.all_passed = False

    def _validate_config_keys(
        self,
        project_root: Path,
        config_keys: Dict[str, List[str]]
    ) -> ConfigKeyReport:
        """
        Validate config keys for multiple files (SVC-017).

        Args:
            project_root: Path to project root.
            config_keys: Dict of {file_path: [required_keys]}.

        Returns:
            ConfigKeyReport with results.
        """
        report = ConfigKeyReport(all_passed=True)

        for file_path, required in config_keys.items():
            full_path = project_root / file_path
            result = self.validate_config_keys(full_path, required)

            if result.passed:
                report.passed.append(file_path)
            else:
                report.failed.append(file_path)
                report.missing_keys[file_path] = result.missing_keys
                report.all_passed = False

        return report
