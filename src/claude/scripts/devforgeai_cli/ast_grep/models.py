"""
Data models for ast-grep rule configuration.

Defines RuleMetadata schema and related enums for STORY-116.
"""

from enum import Enum
from typing import Optional, Dict, Any


class RuleSeverity(Enum):
    """Rule severity levels matching ast-grep conventions."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RuleLanguage(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    CSHARP = "csharp"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"


class RuleMetadata:
    """
    Schema for individual ast-grep rule YAML files.

    Attributes:
        id: Unique rule identifier within language (required)
        language: Target programming language (required)
        severity: Rule severity level (required)
        message: Human-readable violation message (required, min 10 chars)
        pattern: ast-grep pattern string (required)
        fix: Optional auto-fix pattern
        note: Optional additional notes for developers
    """

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
        Initialize RuleMetadata with validation.

        Args:
            id: Rule identifier (required, non-empty)
            language: Target language enum
            severity: Severity level enum
            message: Violation message (min 10 chars)
            pattern: ast-grep pattern (required, non-empty)
            fix: Optional auto-fix pattern
            note: Optional developer notes

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not id:
            raise ValueError("Rule ID cannot be empty")
        if not pattern:
            raise ValueError("Pattern cannot be empty")
        if len(message) < 10:
            raise ValueError("Message must be at least 10 characters")

        self.id = id
        self.language = language
        self.severity = severity
        self.message = message
        self.pattern = pattern
        self.fix = fix
        self.note = note

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for YAML serialization.

        Returns:
            Dictionary with enum values as strings.
            None optional fields are excluded.
        """
        result = {
            "id": self.id,
            "language": self.language.value,
            "severity": self.severity.value,
            "message": self.message,
            "pattern": self.pattern,
        }
        if self.fix is not None:
            result["fix"] = self.fix
        if self.note is not None:
            result["note"] = self.note
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RuleMetadata":
        """
        Create RuleMetadata from dictionary (parsed YAML).

        Args:
            data: Dictionary with rule configuration

        Returns:
            RuleMetadata instance
        """
        return cls(
            id=data["id"],
            language=RuleLanguage(data["language"]),
            severity=RuleSeverity(data["severity"]),
            message=data["message"],
            pattern=data["pattern"],
            fix=data.get("fix"),
            note=data.get("note"),
        )
