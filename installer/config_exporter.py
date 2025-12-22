"""Configuration exporter service (STORY-082).

Exports configuration to JSON file:
- Excludes sensitive values (tokens, passwords, keys)
- Includes schema version for compatibility
- Produces valid JSON output
"""

import json
from typing import Dict, Any
import re

from installer.config.config_models import InstallConfig


class ConfigExporter:
    """Exports configuration with sensitive value filtering.

    Implements SVC-012, SVC-013.
    """

    # Sensitive key patterns (exact matches and regex patterns)
    SENSITIVE_KEYS_EXACT = {
        "api_token",
        "api_key",
        "password",
        "secret",
        "credentials",
        "auth_token",
        "access_token",
        "refresh_token",
        "private_key",
    }

    # Regex patterns for sensitive keys (case-insensitive)
    # Only match if these words are substantial part of the key name
    SENSITIVE_PATTERNS = [
        r".*\btoken\b.*",
        r".*\bsecret\b.*",
        r".*\bpassword\b.*",
        r".*\bcredential\b.*",
        r".*\bkey\b.*",
    ]

    def __init__(self):
        """Initialize configuration exporter."""
        # Compile regex patterns
        self._compiled_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.SENSITIVE_PATTERNS
        ]

    def export(self, config: InstallConfig) -> str:
        """Export configuration to JSON string.

        SVC-012: Export configuration to JSON
        SVC-013: Exclude sensitive values from export

        Args:
            config: Configuration to export.

        Returns:
            Valid JSON string with sensitive values excluded.
        """
        config_dict = config.to_dict()
        filtered_dict = self._filter_sensitive_values(config_dict)

        return json.dumps(filtered_dict, indent=2)

    def _filter_sensitive_values(self, data: Any) -> Any:
        """Filter out sensitive values from configuration.

        Recursively processes dictionaries and lists,
        removing or masking sensitive values.

        Args:
            data: Data to filter (dict, list, or scalar).

        Returns:
            Filtered data with sensitive values removed.
        """
        if isinstance(data, dict):
            filtered = {}
            for key, value in data.items():
                if self._is_sensitive_key(key):
                    # Skip sensitive keys entirely
                    continue
                filtered[key] = self._filter_sensitive_values(value)
            return filtered

        elif isinstance(data, list):
            return [self._filter_sensitive_values(item) for item in data]

        else:
            # Scalar values pass through
            return data

    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key is sensitive.

        Args:
            key: Key to check.

        Returns:
            True if key contains sensitive information.
        """
        # Check exact matches (case-sensitive)
        if key in self.SENSITIVE_KEYS_EXACT:
            return True

        # Check regex patterns (case-insensitive)
        for pattern in self._compiled_patterns:
            if pattern.match(key):
                return True

        return False
