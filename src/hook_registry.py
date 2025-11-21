"""
Hook registry for loading and managing hook configurations.

Loads hooks from YAML configuration, validates schema, and provides
hook lookup and filtering capabilities.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)

# Validation constants
MAX_HOOK_ID_LENGTH = 50
MAX_HOOK_NAME_LENGTH = 100
MAX_TAGS_COUNT = 5
MIN_DURATION_MS = 1000
MAX_DURATION_MS = 30000
MAX_TOKEN_USAGE_PERCENT = 100
MIN_TOKEN_USAGE_PERCENT = 0


class HookRegistryEntry:
    """Represents a single hook registry entry with validation."""

    # Valid enum values
    VALID_OPERATION_TYPES = {"command", "skill", "subagent"}
    VALID_TRIGGER_STATUSES = {"success", "failure", "partial", "deferred", "completed"}
    VALID_FEEDBACK_TYPES = {"conversation", "summary", "metrics", "checklist"}

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize hook registry entry from dict.

        Args:
            data: Dictionary with hook configuration

        Raises:
            ValueError: If validation fails

        """
        self.data = data
        self.violations = []
        self._validate()

    def _validate(self) -> None:
        """Validate hook entry against schema."""
        self._validate_required_fields()
        self._validate_id()
        self._validate_name()
        self._validate_operation_type()
        self._validate_operation_pattern()
        self._validate_trigger_status()
        self._validate_feedback_type()
        self._validate_max_duration()
        self._validate_enabled()
        self._validate_tags()
        if "trigger_conditions" in self.data:
            self._validate_trigger_conditions(self.data["trigger_conditions"])

    def _validate_required_fields(self) -> None:
        """Validate all required fields exist."""
        required_fields = {"id", "name", "operation_type", "operation_pattern", "trigger_status", "feedback_type"}
        for field in required_fields:
            if field not in self.data:
                self.violations.append(f"missing required field: {field}")

    def _validate_id(self) -> None:
        """Validate ID format and length."""
        if "id" not in self.data:
            return
        hook_id = self.data["id"]
        if not isinstance(hook_id, str):
            self.violations.append("id must be string")
        elif not re.match(r"^[a-z0-9-]+$", hook_id):
            self.violations.append("id must match ^[a-z0-9-]+$")
        elif len(hook_id) > MAX_HOOK_ID_LENGTH:
            self.violations.append(f"id must be <= {MAX_HOOK_ID_LENGTH} characters")

    def _validate_name(self) -> None:
        """Validate name length."""
        if "name" in self.data:
            if len(self.data["name"]) > MAX_HOOK_NAME_LENGTH:
                self.violations.append(f"name must be <= {MAX_HOOK_NAME_LENGTH} characters")

    def _validate_operation_type(self) -> None:
        """Validate operation_type value."""
        if "operation_type" in self.data:
            if self.data["operation_type"] not in self.VALID_OPERATION_TYPES:
                self.violations.append(
                    f"operation_type must be one of {self.VALID_OPERATION_TYPES}"
                )

    def _validate_operation_pattern(self) -> None:
        """Validate operation_pattern value."""
        if "operation_pattern" in self.data:
            pattern = self.data["operation_pattern"]
            if not isinstance(pattern, str) or len(pattern) == 0:
                self.violations.append("operation_pattern must be non-empty string")

    def _validate_trigger_status(self) -> None:
        """Validate trigger_status values."""
        if "trigger_status" not in self.data:
            return
        statuses = self.data["trigger_status"]
        if not isinstance(statuses, list) or len(statuses) == 0:
            self.violations.append("trigger_status must be non-empty array")
            return
        for status in statuses:
            if status not in self.VALID_TRIGGER_STATUSES:
                self.violations.append(
                    f"trigger_status '{status}' not in {self.VALID_TRIGGER_STATUSES}"
                )

    def _validate_feedback_type(self) -> None:
        """Validate feedback_type value."""
        if "feedback_type" in self.data:
            if self.data["feedback_type"] not in self.VALID_FEEDBACK_TYPES:
                self.violations.append(
                    f"feedback_type must be one of {self.VALID_FEEDBACK_TYPES}"
                )

    def _validate_max_duration(self) -> None:
        """Validate max_duration_ms value."""
        if "max_duration_ms" not in self.data:
            return
        duration = self.data["max_duration_ms"]
        if not isinstance(duration, int):
            self.violations.append("max_duration_ms must be integer")
        elif duration < MIN_DURATION_MS or duration > MAX_DURATION_MS:
            self.violations.append(f"max_duration_ms must be {MIN_DURATION_MS}-{MAX_DURATION_MS}")

    def _validate_enabled(self) -> None:
        """Validate enabled flag value."""
        if "enabled" in self.data:
            if not isinstance(self.data["enabled"], bool):
                self.violations.append("enabled must be boolean")

    def _validate_tags(self) -> None:
        """Validate tags array."""
        if "tags" in self.data:
            tags = self.data["tags"]
            if isinstance(tags, list):
                if len(tags) > MAX_TAGS_COUNT:
                    self.violations.append(f"tags array must have <= {MAX_TAGS_COUNT} items")

    def _validate_trigger_conditions(self, conditions: Dict[str, Any]) -> None:
        """Validate trigger_conditions sub-object."""
        # Check duration consistency
        if "operation_duration_min_ms" in conditions and "operation_duration_max_ms" in conditions:
            min_val = conditions["operation_duration_min_ms"]
            max_val = conditions["operation_duration_max_ms"]
            if min_val > max_val:
                self.violations.append("operation_duration_min_ms must be <= operation_duration_max_ms")

        # Check token usage ranges
        if "token_usage_percent" in conditions:
            val = conditions["token_usage_percent"]
            if not (MIN_TOKEN_USAGE_PERCENT <= val <= MAX_TOKEN_USAGE_PERCENT):
                self.violations.append(f"token_usage_percent must be {MIN_TOKEN_USAGE_PERCENT}-{MAX_TOKEN_USAGE_PERCENT}")

    def is_valid(self) -> bool:
        """Check if entry is valid."""
        return len(self.violations) == 0

    def get_violations(self) -> List[str]:
        """Get list of validation violations."""
        return self.violations.copy()

    def __getitem__(self, key: str) -> Any:
        """Get field from data dict."""
        return self.data[key]

    def get(self, key: str, default: Any = None) -> Any:
        """Get field from data dict with default."""
        return self.data.get(key, default)


class HookRegistry:
    """Registry for loading and managing hook configurations."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize hook registry.

        Args:
            config_path: Path to hooks.yaml (optional)

        """
        self.config_path = config_path or Path(".devforgeai/config/hooks.yaml")
        self.entries: Dict[str, HookRegistryEntry] = {}
        self.load_errors: List[str] = []
        self._load_config()

    def _load_config(self) -> None:
        """
        Load hooks from YAML configuration file.

        Handles:
        - Missing config file (gracefully returns empty)
        - YAML parse errors (logged, registry remains empty)
        - Validation errors (logged per hook, valid hooks still loaded)
        - Duplicate hook IDs (rejected with error logged)
        - File I/O errors (logged, registry remains empty)
        """
        self.entries.clear()
        self.load_errors.clear()

        # Handle missing config gracefully
        if not self.config_path.exists():
            logger.info(f"Hook config not found at {self.config_path}, using empty registry")
            return

        # Handle file I/O errors
        try:
            with open(self.config_path, "r") as f:
                config_content = f.read()
        except IOError as e:
            self.load_errors.append(f"Failed to read config file: {e}")
            logger.error(f"Cannot read {self.config_path}: {e}")
            return
        except Exception as e:
            self.load_errors.append(f"Unexpected file error: {e}")
            logger.error(f"Unexpected error reading {self.config_path}: {e}")
            return

        # Handle YAML parsing errors
        try:
            config = yaml.safe_load(config_content)
        except yaml.YAMLError as e:
            self.load_errors.append(f"YAML parse error: {e}")
            logger.error(f"Failed to parse {self.config_path}: {e}")
            return
        except Exception as e:
            self.load_errors.append(f"Unexpected YAML error: {e}")
            logger.error(f"Unexpected error parsing {self.config_path}: {e}")
            return

        # Validate config structure
        if not config:
            logger.info(f"Config file {self.config_path} is empty")
            return

        if "hooks" not in config:
            self.load_errors.append("No 'hooks' key found in config")
            logger.warning(f"No 'hooks' key in {self.config_path}")
            return

        hooks_data = config["hooks"]
        if not isinstance(hooks_data, list):
            self.load_errors.append("'hooks' must be array, got " + type(hooks_data).__name__)
            logger.error(f"'hooks' must be array in {self.config_path}, got {type(hooks_data).__name__}")
            return

        # Load and validate each hook
        for hook_index, hook_data in enumerate(hooks_data):
            hook_id_label = f"[hook #{hook_index}]"

            # Validate hook_data is dict
            if not isinstance(hook_data, dict):
                error_msg = f"Hook entry {hook_id_label} must be dict, got {type(hook_data).__name__}"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue

            hook_id = hook_data.get("id", hook_id_label)

            # Handle validation errors (continue loading valid hooks)
            try:
                entry = HookRegistryEntry(hook_data)
            except KeyError as e:
                error_msg = f"Hook {hook_id}: missing required field {e}"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue
            except TypeError as e:
                error_msg = f"Hook {hook_id}: type error {e}"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue
            except Exception as e:
                error_msg = f"Hook {hook_id}: unexpected error {e}"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue

            # Check for validation violations
            if not entry.is_valid():
                violations = entry.get_violations()
                error_msg = f"Hook {hook_id}: validation failed - {violations}"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue

            # Check for duplicate IDs
            if hook_id in self.entries:
                error_msg = f"Duplicate hook ID: {hook_id} (skipping second occurrence)"
                self.load_errors.append(error_msg)
                logger.warning(error_msg)
                continue

            # Add hook to registry
            self.entries[hook_id] = entry
            logger.debug(f"Loaded hook: {hook_id}")

        # Summary logging
        if len(self.entries) > 0:
            logger.info(f"Successfully loaded {len(self.entries)} hooks from {self.config_path}")
        else:
            logger.warning(f"No valid hooks loaded from {self.config_path} (see errors above)")

        if len(self.load_errors) > 0:
            logger.warning(f"Encountered {len(self.load_errors)} errors loading hooks")

    def get_hook(self, hook_id: str) -> Optional[HookRegistryEntry]:
        """
        Get hook by ID.

        Args:
            hook_id: Hook ID to retrieve

        Returns:
            HookRegistryEntry or None if not found

        """
        return self.entries.get(hook_id)

    def get_all_hooks(self) -> List[HookRegistryEntry]:
        """
        Get all hooks.

        Returns:
            List of all hook entries

        """
        return list(self.entries.values())

    def get_hooks_for_operation(
        self,
        operation_type: str,
        operation_pattern: str,
        trigger_status: str,
    ) -> List[HookRegistryEntry]:
        """
        Get hooks matching operation criteria.

        Args:
            operation_type: Type of operation (command, skill, subagent)
            operation_pattern: Operation name pattern
            trigger_status: Operation status

        Returns:
            List of matching hook entries

        """
        matching = []

        for entry in self.entries.values():
            # Skip disabled hooks
            if not entry.get("enabled", True):
                continue

            # Check operation_type match
            if entry["operation_type"] != operation_type:
                continue

            # Check trigger_status match
            statuses = entry["trigger_status"]
            if trigger_status not in statuses:
                continue

            matching.append(entry)

        return matching

    def reload(self) -> bool:
        """
        Reload configuration from file.

        Returns:
            True if reload successful

        """
        try:
            self._load_config()
            return len(self.load_errors) == 0
        except Exception as e:
            self.load_errors.append(f"Reload failed: {e}")
            logger.error(f"Failed to reload hooks: {e}")
            return False

    def get_load_errors(self) -> List[str]:
        """Get list of configuration load errors."""
        return self.load_errors.copy()

    def has_errors(self) -> bool:
        """Check if there are load errors."""
        return len(self.load_errors) > 0

    def size(self) -> int:
        """Get number of loaded hooks."""
        return len(self.entries)
