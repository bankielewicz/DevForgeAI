"""
ast-grep configuration and rule management package.

Provides configuration initialization, validation, and rule metadata
for the DevForgeAI ast-grep integration.

STORY-116: Configuration Infrastructure - ast-grep Rule Storage
"""

from .models import (
    RuleMetadata,
    RuleSeverity,
    RuleLanguage,
)

from .config_init import (
    ConfigurationInitializer,
    InitResult,
)

from .config_validator import (
    ConfigurationValidator,
    ValidationResult,
    ValidationError,
)

__all__ = [
    # Models
    'RuleMetadata',
    'RuleSeverity',
    'RuleLanguage',
    # Initialization
    'ConfigurationInitializer',
    'InitResult',
    # Validation
    'ConfigurationValidator',
    'ValidationResult',
    'ValidationError',
]
