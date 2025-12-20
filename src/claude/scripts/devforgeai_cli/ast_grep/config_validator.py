"""
ConfigurationValidator - ast-grep configuration validation.

Validates sgconfig.yml syntax, structure, and referenced directories
for STORY-116.
"""

import logging
from pathlib import Path
from typing import List, Optional, NamedTuple

try:
    import yaml
    from yaml import YAMLError
except ImportError:
    yaml = None
    YAMLError = Exception

logger = logging.getLogger(__name__)


class ValidationError(NamedTuple):
    """Represents a single validation error."""
    field: str
    message: str
    line: Optional[int] = None


class ValidationResult(NamedTuple):
    """Result of configuration validation."""
    valid: bool
    errors: List[ValidationError]
    warnings: List[str]


class ConfigurationValidator:
    """
    Validates ast-grep sgconfig.yml configuration files.

    Implements:
        SVC-004: Parse and validate YAML syntax (with line number errors)
        SVC-005: Verify referenced directories exist
        SVC-006: Validate language glob patterns
    """

    VALID_LANGUAGES = {"python", "csharp", "typescript", "javascript"}

    def __init__(self, config_path: Path):
        """
        Initialize with path to sgconfig.yml.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)

    def validate(self) -> ValidationResult:
        """
        Validate sgconfig.yml configuration.

        Returns:
            ValidationResult with status and any errors/warnings

        Implements:
            SVC-004: YAML syntax validation with line numbers
            SVC-005: Directory existence verification
            SVC-006: Glob pattern validation
        """
        errors: List[ValidationError] = []
        warnings: List[str] = []

        # Check PyYAML availability
        if yaml is None:
            return ValidationResult(
                valid=False,
                errors=[ValidationError("dependency", "PyYAML is required for configuration validation")],
                warnings=[],
            )

        # Check file exists
        if not self.config_path.exists():
            return ValidationResult(
                valid=False,
                errors=[ValidationError("config", "Configuration file not found")],
                warnings=[],
            )

        # SVC-004: Parse and validate YAML syntax
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except YAMLError as e:
            line_num = None
            if hasattr(e, "problem_mark") and e.problem_mark:
                line_num = e.problem_mark.line + 1
            return ValidationResult(
                valid=False,
                errors=[ValidationError("yaml_syntax", f"Invalid YAML syntax: {e}", line=line_num)],
                warnings=[],
            )

        if config is None:
            config = {}

        # Validate required fields
        errors.extend(self._validate_required_fields(config))

        # SVC-005: Verify referenced directories exist
        if "ruleDirs" in config and isinstance(config["ruleDirs"], list):
            errors.extend(self._validate_directories(config["ruleDirs"]))

        # SVC-006: Validate glob patterns and check languages
        if "languageGlobs" in config and isinstance(config["languageGlobs"], dict):
            glob_errors, lang_warnings = self._validate_globs(config["languageGlobs"])
            errors.extend(glob_errors)
            warnings.extend(lang_warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_required_fields(self, config: dict) -> List[ValidationError]:
        """Validate required schema fields."""
        errors = []

        if "ruleDirs" not in config:
            errors.append(ValidationError("ruleDirs", "Required field 'ruleDirs' is missing"))
        elif not isinstance(config["ruleDirs"], list):
            errors.append(ValidationError("ruleDirs", "Field 'ruleDirs' must be an array"))

        if "languageGlobs" not in config:
            errors.append(ValidationError("languageGlobs", "Required field 'languageGlobs' is missing"))
        elif not isinstance(config["languageGlobs"], dict):
            errors.append(ValidationError("languageGlobs", "Field 'languageGlobs' must be an object"))

        return errors

    def _validate_directories(self, rule_dirs: List[str]) -> List[ValidationError]:
        """Verify referenced directories exist (SVC-005)."""
        errors = []

        for dir_path in rule_dirs:
            full_path = self.config_path.parent / dir_path
            if not full_path.exists():
                errors.append(ValidationError("ruleDirs", f"Directory not found: {dir_path}"))

        return errors

    def _validate_globs(self, language_globs: dict) -> tuple:
        """Validate glob patterns (SVC-006)."""
        errors = []
        warnings = []

        for lang, glob_pattern in language_globs.items():
            # Check if language is recognized
            if lang not in self.VALID_LANGUAGES:
                warnings.append(
                    f"Unrecognized language: '{lang}'. Supported languages: {self.VALID_LANGUAGES}"
                )

            # Check for empty glob patterns
            if not glob_pattern or (isinstance(glob_pattern, str) and glob_pattern.strip() == ""):
                errors.append(
                    ValidationError("languageGlobs", f"Glob pattern for language '{lang}' is empty")
                )
            elif not self._is_valid_glob_pattern(glob_pattern):
                warnings.append(f"Glob pattern for language '{lang}' may be invalid: {glob_pattern}")

        return errors, warnings

    def _is_valid_glob_pattern(self, pattern: str) -> bool:
        """Check if glob pattern is valid."""
        if not pattern:
            return False
        # Valid patterns should contain * or ? or be literal paths
        if isinstance(pattern, str):
            return "*" in pattern or "?" in pattern or len(pattern) > 0
        return False
