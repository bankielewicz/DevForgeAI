"""
Tests for RuleMetadata dataclass (STORY-116: Configuration Infrastructure)

These tests validate the RuleMetadata model that defines the schema for individual
ast-grep rule YAML files. Tests focus on field validation, serialization/deserialization,
and enum constraint enforcement.

Test Coverage: 95%+ for business logic
"""

import pytest

# Import from the actual module
from claude.scripts.devforgeai_cli.ast_grep.models import (
    RuleMetadata,
    RuleSeverity,
    RuleLanguage,
)


# ============================================================================
# TESTS: RuleMetadata Basic Initialization
# ============================================================================

class TestRuleMetadataInitialization:
    """Test creating valid RuleMetadata instances"""

    def test_should_create_valid_rule_metadata_with_all_required_fields(self):
        """
        Scenario: Create RuleMetadata with required fields only
        Given: Valid required fields (id, language, severity, message, pattern)
        When: RuleMetadata is instantiated
        Then: Instance is created successfully
        """
        # Arrange
        rule_id = "SEC-001"
        language = RuleLanguage.PYTHON
        severity = RuleSeverity.CRITICAL
        message = "Security vulnerability detected"
        pattern = "$$$"

        # Act
        rule = RuleMetadata(
            id=rule_id,
            language=language,
            severity=severity,
            message=message,
            pattern=pattern,
        )

        # Assert
        assert rule.id == rule_id
        assert rule.language == language
        assert rule.severity == severity
        assert rule.message == message
        assert rule.pattern == pattern

    def test_should_create_rule_metadata_with_optional_fix_field(self):
        """
        Scenario: Create RuleMetadata with optional fix field
        Given: All required fields plus fix field
        When: RuleMetadata is instantiated
        Then: fix field is stored
        """
        # Arrange
        fix_text = "Replace with secure method"

        # Act
        rule = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.HIGH,
            message="Security vulnerability detected",
            pattern="$$$",
            fix=fix_text,
        )

        # Assert
        assert rule.fix == fix_text

    def test_should_create_rule_metadata_with_optional_note_field(self):
        """
        Scenario: Create RuleMetadata with optional note field
        Given: All required fields plus note field
        When: RuleMetadata is instantiated
        Then: note field is stored
        """
        # Arrange
        note_text = "This rule is experimental"

        # Act
        rule = RuleMetadata(
            id="AP-001",
            language=RuleLanguage.CSHARP,
            severity=RuleSeverity.MEDIUM,
            message="Anti-pattern detected in code",
            pattern="$$$",
            note=note_text,
        )

        # Assert
        assert rule.note == note_text

    def test_should_default_optional_fields_to_none(self):
        """
        Scenario: Create RuleMetadata without optional fields
        Given: Only required fields provided
        When: RuleMetadata is instantiated
        Then: Optional fields default to None
        """
        # Act
        rule = RuleMetadata(
            id="API-001",
            language=RuleLanguage.TYPESCRIPT,
            severity=RuleSeverity.LOW,
            message="This is a minimum message",
            pattern="$$$",
        )

        # Assert
        assert rule.fix is None
        assert rule.note is None


# ============================================================================
# TESTS: RuleMetadata Field Validation
# ============================================================================

class TestRuleMetadataValidation:
    """Test RuleMetadata field validation constraints"""

    def test_should_reject_empty_rule_id(self):
        """
        Scenario: Create RuleMetadata with empty ID
        Given: Empty string for id field
        When: RuleMetadata is instantiated
        Then: ValueError is raised
        """
        # Act & Assert
        with pytest.raises(ValueError, match="Rule ID cannot be empty"):
            RuleMetadata(
                id="",
                language=RuleLanguage.PYTHON,
                severity=RuleSeverity.CRITICAL,
                message="Security vulnerability detected",
                pattern="$$$",
            )

    def test_should_reject_empty_pattern(self):
        """
        Scenario: Create RuleMetadata with empty pattern
        Given: Empty string for pattern field
        When: RuleMetadata is instantiated
        Then: ValueError is raised
        """
        # Act & Assert
        with pytest.raises(ValueError, match="Pattern cannot be empty"):
            RuleMetadata(
                id="SEC-001",
                language=RuleLanguage.PYTHON,
                severity=RuleSeverity.CRITICAL,
                message="Security vulnerability detected",
                pattern="",
            )

    def test_should_reject_message_under_10_characters(self):
        """
        Scenario: Create RuleMetadata with message < 10 chars
        Given: Message with fewer than 10 characters
        When: RuleMetadata is instantiated
        Then: ValueError is raised
        """
        # Act & Assert
        with pytest.raises(ValueError, match="Message must be at least 10 characters"):
            RuleMetadata(
                id="SEC-001",
                language=RuleLanguage.PYTHON,
                severity=RuleSeverity.CRITICAL,
                message="Short msg",
                pattern="$$$",
            )

    def test_should_accept_message_exactly_10_characters(self):
        """
        Scenario: Create RuleMetadata with message exactly 10 chars
        Given: Message with exactly 10 characters
        When: RuleMetadata is instantiated
        Then: No error is raised
        """
        # Act
        rule = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.CRITICAL,
            message="1234567890",
            pattern="$$$",
        )

        # Assert
        assert rule.message == "1234567890"


# ============================================================================
# TESTS: RuleSeverity Enum
# ============================================================================

class TestRuleSeverityEnum:
    """Test RuleSeverity enum values and usage"""

    def test_should_have_critical_severity(self):
        """Verify CRITICAL severity exists"""
        assert RuleSeverity.CRITICAL.value == "CRITICAL"

    def test_should_have_high_severity(self):
        """Verify HIGH severity exists"""
        assert RuleSeverity.HIGH.value == "HIGH"

    def test_should_have_medium_severity(self):
        """Verify MEDIUM severity exists"""
        assert RuleSeverity.MEDIUM.value == "MEDIUM"

    def test_should_have_low_severity(self):
        """Verify LOW severity exists"""
        assert RuleSeverity.LOW.value == "LOW"


# ============================================================================
# TESTS: RuleLanguage Enum
# ============================================================================

class TestRuleLanguageEnum:
    """Test RuleLanguage enum values and usage"""

    def test_should_have_python_language(self):
        """Verify PYTHON language exists"""
        assert RuleLanguage.PYTHON.value == "python"

    def test_should_have_csharp_language(self):
        """Verify CSHARP language exists"""
        assert RuleLanguage.CSHARP.value == "csharp"

    def test_should_have_typescript_language(self):
        """Verify TYPESCRIPT language exists"""
        assert RuleLanguage.TYPESCRIPT.value == "typescript"

    def test_should_have_javascript_language(self):
        """Verify JAVASCRIPT language exists"""
        assert RuleLanguage.JAVASCRIPT.value == "javascript"


# ============================================================================
# TESTS: RuleMetadata Serialization
# ============================================================================

class TestRuleMetadataToDict:
    """Test RuleMetadata.to_dict() serialization"""

    def test_should_include_all_required_fields_in_dict(self):
        """
        Scenario: Serialize RuleMetadata to dict
        Given: Valid RuleMetadata with required fields only
        When: to_dict() is called
        Then: Dictionary includes all required fields with enum values as strings
        """
        # Arrange
        rule = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.CRITICAL,
            message="Security vulnerability detected",
            pattern="$$$",
        )

        # Act
        result = rule.to_dict()

        # Assert
        assert result["id"] == "SEC-001"
        assert result["language"] == "python"
        assert result["severity"] == "CRITICAL"
        assert result["message"] == "Security vulnerability detected"
        assert result["pattern"] == "$$$"

    def test_should_exclude_none_optional_fields_from_dict(self):
        """
        Scenario: Serialize RuleMetadata without optional fields
        Given: RuleMetadata with fix and note as None
        When: to_dict() is called
        Then: fix and note are not included in dictionary
        """
        # Arrange
        rule = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.CRITICAL,
            message="Security vulnerability detected",
            pattern="$$$",
        )

        # Act
        result = rule.to_dict()

        # Assert
        assert "fix" not in result
        assert "note" not in result

    def test_should_include_optional_fix_field_when_set(self):
        """
        Scenario: Serialize RuleMetadata with fix field
        Given: RuleMetadata with fix value
        When: to_dict() is called
        Then: Dictionary includes fix field
        """
        # Arrange
        rule = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.CRITICAL,
            message="Security vulnerability detected",
            pattern="$$$",
            fix="Use secure method",
        )

        # Act
        result = rule.to_dict()

        # Assert
        assert result["fix"] == "Use secure method"

    def test_should_include_optional_note_field_when_set(self):
        """
        Scenario: Serialize RuleMetadata with note field
        Given: RuleMetadata with note value
        When: to_dict() is called
        Then: Dictionary includes note field
        """
        # Arrange
        rule = RuleMetadata(
            id="AP-001",
            language=RuleLanguage.CSHARP,
            severity=RuleSeverity.MEDIUM,
            message="Anti-pattern detected in code",
            pattern="$$$",
            note="Experimental rule",
        )

        # Act
        result = rule.to_dict()

        # Assert
        assert result["note"] == "Experimental rule"


# ============================================================================
# TESTS: RuleMetadata Deserialization
# ============================================================================

class TestRuleMetadataFromDict:
    """Test RuleMetadata.from_dict() deserialization"""

    def test_should_create_rule_metadata_from_dict(self):
        """
        Scenario: Deserialize dict to RuleMetadata
        Given: Valid dictionary with required fields
        When: from_dict() is called
        Then: RuleMetadata instance is created correctly
        """
        # Arrange
        data = {
            "id": "SEC-001",
            "language": "python",
            "severity": "CRITICAL",
            "message": "Security vulnerability detected",
            "pattern": "$$$",
        }

        # Act
        rule = RuleMetadata.from_dict(data)

        # Assert
        assert rule.id == "SEC-001"
        assert rule.language == RuleLanguage.PYTHON
        assert rule.severity == RuleSeverity.CRITICAL
        assert rule.message == "Security vulnerability detected"
        assert rule.pattern == "$$$"

    def test_should_deserialize_optional_fix_field(self):
        """
        Scenario: Deserialize dict with optional fix field
        Given: Dictionary with fix field
        When: from_dict() is called
        Then: fix field is set correctly
        """
        # Arrange
        data = {
            "id": "SEC-001",
            "language": "python",
            "severity": "CRITICAL",
            "message": "Security vulnerability detected",
            "pattern": "$$$",
            "fix": "Use secure method",
        }

        # Act
        rule = RuleMetadata.from_dict(data)

        # Assert
        assert rule.fix == "Use secure method"

    def test_should_deserialize_optional_note_field(self):
        """
        Scenario: Deserialize dict with optional note field
        Given: Dictionary with note field
        When: from_dict() is called
        Then: note field is set correctly
        """
        # Arrange
        data = {
            "id": "AP-001",
            "language": "csharp",
            "severity": "MEDIUM",
            "message": "Anti-pattern detected in code",
            "pattern": "$$$",
            "note": "Experimental rule",
        }

        # Act
        rule = RuleMetadata.from_dict(data)

        # Assert
        assert rule.note == "Experimental rule"


# ============================================================================
# TESTS: RuleMetadata Roundtrip Serialization
# ============================================================================

class TestRuleMetadataRoundtrip:
    """Test roundtrip serialization (to_dict -> from_dict)"""

    def test_should_preserve_all_fields_in_roundtrip(self):
        """
        Scenario: Roundtrip serialization with all fields
        Given: RuleMetadata with all fields set
        When: to_dict() then from_dict() is called
        Then: Fields are preserved exactly
        """
        # Arrange
        original = RuleMetadata(
            id="SEC-001",
            language=RuleLanguage.PYTHON,
            severity=RuleSeverity.CRITICAL,
            message="Security vulnerability detected",
            pattern="$$$",
            fix="Use secure method",
            note="Critical security issue",
        )

        # Act
        serialized = original.to_dict()
        restored = RuleMetadata.from_dict(serialized)

        # Assert
        assert restored.id == original.id
        assert restored.language == original.language
        assert restored.severity == original.severity
        assert restored.message == original.message
        assert restored.pattern == original.pattern
        assert restored.fix == original.fix
        assert restored.note == original.note

    def test_should_preserve_minimal_fields_in_roundtrip(self):
        """
        Scenario: Roundtrip serialization with minimal fields
        Given: RuleMetadata with only required fields
        When: to_dict() then from_dict() is called
        Then: Required fields preserved, optional fields remain None
        """
        # Arrange
        original = RuleMetadata(
            id="AP-001",
            language=RuleLanguage.TYPESCRIPT,
            severity=RuleSeverity.MEDIUM,
            message="Anti-pattern detected in code",
            pattern="$$$",
        )

        # Act
        serialized = original.to_dict()
        restored = RuleMetadata.from_dict(serialized)

        # Assert
        assert restored.id == original.id
        assert restored.language == original.language
        assert restored.severity == original.severity
        assert restored.message == original.message
        assert restored.pattern == original.pattern
        assert restored.fix is None
        assert restored.note is None
