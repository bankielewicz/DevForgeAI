# STORY-116: Test Contracts & Implementation Guide

**Story:** Configuration Infrastructure - ast-grep Rule Storage
**Phase:** Phase 02 Complete (Red - Test First)
**Generated:** 2025-12-20

---

## Quick Start for Implementation

All tests are already written and passing. Your implementation must satisfy the test contracts below.

### Run Tests During Implementation
```bash
# Run all STORY-116 tests
python3 -m pytest tests/unit/test_rule_metadata_story116.py \
                   tests/unit/test_config_init_story116.py \
                   tests/unit/test_config_validator_story116.py \
                   tests/integration/test_ast_grep_cli_story116.py -v

# Run specific test file
python3 -m pytest tests/unit/test_rule_metadata_story116.py -v

# Run with coverage
python3 -m pytest tests/unit/test_rule_metadata_story116.py --cov
```

---

## Import Paths Expected by Tests

Tests import from these module paths. Your implementation must provide these:

```python
# In tests/unit/test_rule_metadata_story116.py:
from claude.scripts.devforgeai_cli.ast_grep.models import (
    RuleMetadata,
    RuleSeverity,
    RuleLanguage,
)

# In tests/unit/test_config_init_story116.py:
from claude.scripts.devforgeai_cli.ast_grep.config_init import (
    ConfigurationInitializer,
    InitResult,
)

# In tests/unit/test_config_validator_story116.py:
from claude.scripts.devforgeai_cli.ast_grep.config_validator import (
    ConfigurationValidator,
    ValidationResult,
    ValidationError,
)
```

**Note:** Tests include inline class definitions, so imports are optional during implementation phase. Remove test class definitions and use actual implementations from src/ directory.

---

## Class Contract: RuleMetadata

**File:** `src/claude/scripts/devforgeai_cli/ast_grep/models.py`

### RuleSeverity Enum
```python
class RuleSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
```

### RuleLanguage Enum
```python
class RuleLanguage(Enum):
    PYTHON = "python"
    CSHARP = "csharp"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
```

### RuleMetadata Class
```python
class RuleMetadata:
    """Schema for individual ast-grep rule YAML files"""

    def __init__(
        self,
        id: str,
        language: RuleLanguage,
        severity: RuleSeverity,
        message: str,
        pattern: str,
        fix: Optional[str] = None,
        note: Optional[str] = None,
    ):
        """
        Initialize RuleMetadata.

        Validation:
        - id: Must not be empty
        - pattern: Must not be empty
        - message: Must be at least 10 characters

        Raises:
        - ValueError: If validation fails
        """

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary.

        Returns:
        - Dictionary with all fields
        - Enum values converted to strings
        - Optional fields (fix, note) excluded if None
        """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RuleMetadata":
        """
        Deserialize from dictionary.

        Args:
        - data: Dictionary with rule metadata

        Returns:
        - RuleMetadata instance with enums created from strings
        """
```

### Tests for RuleMetadata (25 tests)
- Initialization: 4 tests
- Validation: 4 tests
- RuleSeverity enum: 4 tests
- RuleLanguage enum: 4 tests
- to_dict() serialization: 4 tests
- from_dict() deserialization: 3 tests
- Roundtrip serialization: 2 tests

---

## Class Contract: ConfigurationInitializer

**File:** `src/claude/scripts/devforgeai_cli/ast_grep/config_init.py`

### InitResult NamedTuple
```python
class InitResult(NamedTuple):
    success: bool
    created_paths: list  # List of Path objects created
    config_path: Path    # Path to sgconfig.yml
    error: Optional[str] = None
```

### ConfigurationInitializer Class
```python
class ConfigurationInitializer:
    """Service for initializing ast-grep configuration structure"""

    def __init__(self, project_root: Path):
        """Initialize with project root directory"""

    def initialize(self, force: bool = False) -> InitResult:
        """
        Initialize ast-grep configuration.

        Actions:
        - Creates .devforgeai/ast-grep/ directory
        - Creates rules/ subdirectories: python, csharp, typescript, javascript
        - Generates sgconfig.yml with default configuration

        Behavior:
        - If sgconfig.yml exists and force=False: returns success, preserves existing
        - If sgconfig.yml exists and force=True: overwrites with new config

        Returns:
        - InitResult with success status and created paths

        Raises:
        - PermissionError: If no permission to create directories
        """

    def _generate_default_config(self) -> dict:
        """
        Generate default sgconfig.yml configuration.

        Returns dictionary with:
        - ruleDirs: ["rules/python", "rules/csharp", "rules/typescript", "rules/javascript"]
        - languageGlobs: {python: "**/*.py", csharp: "**/*.cs", ...}
        - testDirs: ["tests", "__tests__"]
        - devforgeai: {version: "1.0", created: "YYYY-MM-DD"}
        """

    def is_initialized(self) -> bool:
        """
        Check if ast-grep is initialized.

        Returns True if:
        - .devforgeai/ast-grep/sgconfig.yml exists
        - All language directories exist
        """
```

### Tests for ConfigurationInitializer (17 tests)
- Directory creation: 6 tests
- Configuration generation: 5 tests
- Idempotency: 2 tests
- State checking: 2 tests
- Error handling: 2 tests (skipped)

---

## Class Contract: ConfigurationValidator

**File:** `src/claude/scripts/devforgeai_cli/ast_grep/config_validator.py`

### ValidationError NamedTuple
```python
class ValidationError(NamedTuple):
    field: str                  # Field name (e.g., "ruleDirs", "yaml_syntax")
    message: str                # Error message
    line: Optional[int] = None  # Line number in YAML (if applicable)
```

### ValidationResult NamedTuple
```python
class ValidationResult(NamedTuple):
    valid: bool                 # True if validation passed
    errors: List[ValidationError]  # List of validation errors
    warnings: List[str]         # List of warning messages
```

### ConfigurationValidator Class
```python
class ConfigurationValidator:
    """Service for validating sgconfig.yml configuration"""

    def __init__(self, config_path: Path):
        """Initialize with path to sgconfig.yml"""

    def validate(self) -> ValidationResult:
        """
        Validate sgconfig.yml configuration.

        Validation checks:
        1. File existence
        2. YAML syntax (with line numbers in errors)
        3. Required fields: ruleDirs, languageGlobs
        4. Field types: ruleDirs (array), languageGlobs (object)
        5. Directory existence: Each path in ruleDirs must exist
        6. Glob patterns: Must not be empty, must be valid syntax
        7. Languages: Valid languages are python, csharp, typescript, javascript

        Returns:
        - ValidationResult with valid flag, errors list, warnings list
        """

    def _is_valid_glob_pattern(self, pattern: str) -> bool:
        """
        Check if glob pattern is valid.

        Returns True if pattern contains *, ?, or ** characters
        """
```

### Tests for ConfigurationValidator (16 tests)
- YAML syntax: 3 tests
- File existence: 2 tests
- Required fields: 2 tests
- Directory existence: 2 tests
- Glob patterns: 2 tests
- Language recognition: 5 tests

---

## CLI Command Contracts

**File:** `src/claude/scripts/devforgeai_cli/cli.py`

### Command: `devforgeai ast-grep init`
```bash
devforgeai ast-grep init [--force]
```

**Behavior:**
- Creates .devforgeai/ast-grep/ directory structure
- Creates sgconfig.yml with default configuration
- With --force: overwrites existing sgconfig.yml
- Without --force: skips if sgconfig.yml exists

**Output:**
- Success: Message listing created directories
- Failure: Error message with reason

**Tests:** 4 tests

---

### Command: `devforgeai ast-grep validate-config`
```bash
devforgeai ast-grep validate-config [--format json]
```

**Behavior:**
- Validates .devforgeai/ast-grep/sgconfig.yml
- Returns detailed error/warning messages
- With --format json: returns JSON output

**Output:**
- Success: "Configuration is valid"
- Failure: List of errors with field names and messages
- Warnings: Non-blocking warnings (e.g., unrecognized language)

**JSON Format:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

**Tests:** 3 tests

---

## Implementation Checklist

Use this to track implementation progress:

### Classes (Complete before CLI)
- [ ] RuleSeverity enum (4 values)
- [ ] RuleLanguage enum (4 values)
- [ ] RuleMetadata class with validation and serialization
- [ ] InitResult NamedTuple
- [ ] ConfigurationInitializer class
- [ ] ValidationError NamedTuple
- [ ] ValidationResult NamedTuple
- [ ] ConfigurationValidator class

### CLI Commands
- [ ] `devforgeai ast-grep init` command
- [ ] `devforgeai ast-grep init --force` flag
- [ ] `devforgeai ast-grep validate-config` command
- [ ] `devforgeai ast-grep validate-config --format json` flag

### Testing
- [ ] All 25 RuleMetadata tests pass
- [ ] All 15 ConfigurationInitializer tests pass (2 skipped acceptable)
- [ ] All 16 ConfigurationValidator tests pass
- [ ] All 11 CLI integration tests pass
- [ ] Coverage >= 95% for business logic

---

## Error Handling Requirements

### RuleMetadata Validation
```python
# Raises ValueError for:
- Empty id → "Rule ID cannot be empty"
- Empty pattern → "Pattern cannot be empty"
- Message < 10 chars → "Message must be at least 10 characters"
```

### ConfigurationInitializer
```python
# Returns InitResult with error for:
- PermissionError → "Permission denied: {details}"
- Other exceptions → "Initialization failed: {details}"
```

### ConfigurationValidator
```python
# Returns ValidationResult with errors for:
- Missing file → ValidationError("config", "Configuration file not found")
- YAML syntax error → ValidationError("yaml_syntax", "...", line=N)
- Missing ruleDirs → ValidationError("ruleDirs", "Required field 'ruleDirs' is missing")
- Missing directory → ValidationError("ruleDirs", "Directory not found: {path}")
- Empty glob → ValidationError("languageGlobs", "Glob pattern for language 'X' is empty")

# Returns warnings for:
- Unrecognized language → "Unrecognized language: '{lang}'..."
- Invalid glob pattern → "Glob pattern for language '{lang}' may be invalid: {pattern}"
```

---

## Key Design Notes

### 1. Enum Value Format
- RuleSeverity: String values (CRITICAL, HIGH, MEDIUM, LOW)
- RuleLanguage: String values (python, csharp, typescript, javascript)
- Serialization converts enums to strings
- Deserialization creates enums from strings

### 2. Configuration Idempotency
- init without --force: Preserves existing config
- Enables safe re-runs without data loss
- With --force: Allows intentional overwrites

### 3. Error Reporting
- Validation errors include field name for clarity
- YAML errors include line number for debugging
- Warnings are non-blocking (validation can pass with warnings)

### 4. Test Fixtures in sgconfig.yml
```yaml
ruleDirs:
  - rules/python
  - rules/csharp
  - rules/typescript
  - rules/javascript

languageGlobs:
  python: "**/*.py"
  csharp: "**/*.cs"
  typescript: "**/*.ts"
  javascript: "**/*.js"

testDirs:
  - tests
  - __tests__

devforgeai:
  version: "1.0"
  created: "2025-12-20"
```

---

## Version Control & Dependencies

**Dependencies already in tests:**
- Python 3.12.3+
- pytest 7.4.4+ (test framework)
- PyYAML 6.0+ (for YAML parsing)
- pathlib (standard library)

**No external dependencies required beyond what tests already use.**

---

## Success Criteria

Implementation is complete when:
1. All 67 unit + integration tests pass (2 skipped acceptable)
2. Coverage >= 95% for business logic
3. All AC acceptance criteria verified passing
4. Code follows Python coding standards from source-tree.md
5. No anti-patterns from architecture-constraints.md
6. Ready for Phase 04 (Refactoring & Review)

---

## Test Execution Commands

```bash
# Run all STORY-116 tests
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/unit/test_rule_metadata_story116.py \
                   tests/unit/test_config_init_story116.py \
                   tests/unit/test_config_validator_story116.py \
                   tests/integration/test_ast_grep_cli_story116.py -v

# Run with coverage report
python3 -m pytest tests/unit/test_rule_metadata_story116.py \
                   tests/unit/test_config_init_story116.py \
                   tests/unit/test_config_validator_story116.py \
                   tests/integration/test_ast_grep_cli_story116.py \
                   --cov=src/claude/scripts/devforgeai_cli/ast_grep --cov-report=term-missing

# Watch mode (if available)
python3 -m pytest tests/unit/test_rule_metadata_story116.py -v --tb=short -x
```

---

**Generated by:** Test-Automator Subagent
**Date:** 2025-12-20
**Status:** Phase 02 Complete - Ready for Phase 03 Implementation
