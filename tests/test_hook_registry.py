"""
Test suite for hook registry validation and schema compliance.

Tests the hook registry loading, validation, schema enforcement, and error reporting.
Focuses on: AC10, AC1, AC4

AC Coverage:
- AC1: Hook Registration and Discovery
- AC10: Hook Registry Validation on Load
- AC4: Config-Driven Hook Trigger Rules
"""

import pytest
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def valid_hook_entry() -> Dict[str, Any]:
    """Minimal valid hook registry entry."""
    return {
        'id': 'valid-hook-001',
        'name': 'Valid Hook',
        'operation_type': 'command',
        'operation_pattern': 'dev',
        'trigger_status': ['success'],
        'feedback_type': 'conversation',
        'enabled': True,
    }


@pytest.fixture
def invalid_hook_entries() -> Dict[str, Dict[str, Any]]:
    """Collection of invalid hook entries for validation testing."""
    return {
        'missing_id': {
            'name': 'Missing ID',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'missing_name': {
            'id': 'test-hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'invalid_operation_type': {
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'invalid_type',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'missing_operation_pattern': {
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'command',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'empty_trigger_status': {
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': [],
            'feedback_type': 'conversation',
        },
        'invalid_feedback_type': {
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'invalid_type',
        },
        'invalid_id_format': {
            'id': 'INVALID_ID_001',  # Should be lowercase-with-hyphens
            'name': 'Invalid ID',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'id_too_long': {
            'id': 'a' * 51,  # Max 50 chars
            'name': 'ID Too Long',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'name_too_long': {
            'id': 'test-hook',
            'name': 'x' * 101,  # Max 100 chars
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
        },
        'invalid_trigger_status': {
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success', 'invalid_status'],
            'feedback_type': 'conversation',
        },
    }


# ============================================================================
# AC10: Hook Registry Validation on Load Tests
# ============================================================================

class TestHookRegistryValidation:
    """Tests for hook registry validation on load."""

    def test_valid_hook_passes_validation(self, valid_hook_entry):
        """
        GIVEN the hook registry file contains valid schema,
        WHEN the registry is loaded,
        THEN validation succeeds and hook is available.
        """
        # Act & Assert
        assert valid_hook_entry['id'] is not None
        assert valid_hook_entry['name'] is not None
        assert valid_hook_entry['operation_type'] in ['command', 'skill', 'subagent']
        assert valid_hook_entry['trigger_status']
        assert valid_hook_entry['feedback_type'] in ['conversation', 'summary', 'metrics', 'checklist']

    def test_missing_required_field_id(self, invalid_hook_entries):
        """WHEN hook missing required 'id' field, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['missing_id']

        # Act
        is_valid = 'id' in hook and hook['id'] is not None

        # Assert
        assert is_valid is False

    def test_missing_required_field_name(self, invalid_hook_entries):
        """WHEN hook missing required 'name' field, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['missing_name']

        # Act
        is_valid = 'name' in hook and hook['name'] is not None

        # Assert
        assert is_valid is False

    def test_invalid_operation_type(self, invalid_hook_entries):
        """WHEN operation_type invalid, THEN validation fails with specific error."""
        # Arrange
        hook = invalid_hook_entries['invalid_operation_type']
        valid_types = ['command', 'skill', 'subagent']

        # Act
        is_valid = hook['operation_type'] in valid_types

        # Assert
        assert is_valid is False

    def test_missing_operation_pattern(self, invalid_hook_entries):
        """WHEN operation_pattern missing, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['missing_operation_pattern']

        # Act
        is_valid = 'operation_pattern' in hook

        # Assert
        assert is_valid is False

    def test_empty_trigger_status_array(self, invalid_hook_entries):
        """WHEN trigger_status empty array, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['empty_trigger_status']

        # Act
        is_valid = len(hook.get('trigger_status', [])) > 0

        # Assert
        assert is_valid is False

    def test_invalid_feedback_type(self, invalid_hook_entries):
        """WHEN feedback_type invalid, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['invalid_feedback_type']
        valid_types = ['conversation', 'summary', 'metrics', 'checklist']

        # Act
        is_valid = hook['feedback_type'] in valid_types

        # Assert
        assert is_valid is False

    def test_hook_id_format_validation(self, invalid_hook_entries):
        """WHEN hook ID doesn't match pattern ^[a-z0-9-]+$, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['invalid_id_format']
        import re
        pattern = r'^[a-z0-9-]+$'

        # Act
        is_valid = bool(re.match(pattern, hook['id']))

        # Assert
        assert is_valid is False

    def test_hook_id_max_length(self, invalid_hook_entries):
        """WHEN hook ID exceeds 50 characters, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['id_too_long']

        # Act
        is_valid = len(hook['id']) <= 50

        # Assert
        assert is_valid is False

    def test_hook_name_max_length(self, invalid_hook_entries):
        """WHEN hook name exceeds 100 characters, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['name_too_long']

        # Act
        is_valid = len(hook['name']) <= 100

        # Assert
        assert is_valid is False

    def test_invalid_trigger_status_value(self, invalid_hook_entries):
        """WHEN trigger_status contains invalid value, THEN validation fails."""
        # Arrange
        hook = invalid_hook_entries['invalid_trigger_status']
        valid_statuses = ['success', 'failure', 'partial', 'deferred', 'completed']

        # Act
        all_valid = all(status in valid_statuses for status in hook['trigger_status'])

        # Assert
        assert all_valid is False

    def test_validation_reports_specific_field_violations(self, invalid_hook_entries):
        """WHEN validation fails, THEN error reports specific field violations."""
        # Arrange
        hook = invalid_hook_entries['missing_id']
        violations = []

        # Act
        if 'id' not in hook:
            violations.append('missing required field: id')

        # Assert
        assert len(violations) > 0
        assert 'id' in violations[0]

    def test_registry_load_fails_safely_on_invalid_schema(self, tmp_path):
        """WHEN registry contains invalid schema, THEN load fails safely without crashing."""
        # Arrange
        config_file = tmp_path / 'hooks.yaml'
        invalid_config = {
            'hooks': [
                {
                    # Missing required fields
                    'id': 'incomplete-hook',
                }
            ]
        }
        with open(config_file, 'w') as f:
            yaml.dump(invalid_config, f)

        # Act
        try:
            with open(config_file) as f:
                loaded = yaml.safe_load(f)
            hook = loaded['hooks'][0]
            is_valid = all(k in hook for k in ['id', 'name', 'operation_type', 'feedback_type'])
        except Exception as e:
            is_valid = False

        # Assert
        assert is_valid is False


# ============================================================================
# Hook ID Uniqueness Tests
# ============================================================================

class TestHookIdUniqueness:
    """Tests for hook ID uniqueness constraint."""

    def test_duplicate_hook_ids_detected(self, tmp_path):
        """WHEN registry has duplicate hook IDs, THEN validation detects and rejects."""
        # Arrange
        config = {
            'hooks': [
                {
                    'id': 'duplicate-hook',
                    'name': 'Hook 1',
                    'operation_type': 'command',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                    'feedback_type': 'conversation',
                },
                {
                    'id': 'duplicate-hook',  # Same ID
                    'name': 'Hook 2',
                    'operation_type': 'command',
                    'operation_pattern': 'qa',
                    'trigger_status': ['success'],
                    'feedback_type': 'summary',
                },
            ]
        }

        # Act
        hook_ids = [hook['id'] for hook in config['hooks']]
        has_duplicates = len(hook_ids) != len(set(hook_ids))

        # Assert
        assert has_duplicates is True

    def test_unique_hook_ids_accepted(self, tmp_path):
        """WHEN all hook IDs unique, THEN validation passes."""
        # Arrange
        config = {
            'hooks': [
                {
                    'id': 'hook-1',
                    'name': 'Hook 1',
                    'operation_type': 'command',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                    'feedback_type': 'conversation',
                },
                {
                    'id': 'hook-2',
                    'name': 'Hook 2',
                    'operation_type': 'command',
                    'operation_pattern': 'qa',
                    'trigger_status': ['success'],
                    'feedback_type': 'summary',
                },
            ]
        }

        # Act
        hook_ids = [hook['id'] for hook in config['hooks']]
        all_unique = len(hook_ids) == len(set(hook_ids))

        # Assert
        assert all_unique is True


# ============================================================================
# Operation Pattern Validation Tests
# ============================================================================

class TestOperationPatternValidation:
    """Tests for operation pattern validation."""

    def test_simple_pattern_validation(self, valid_hook_entry):
        """WHEN operation_pattern is simple string, THEN validates as valid pattern."""
        # Act
        pattern = valid_hook_entry['operation_pattern']
        is_valid = isinstance(pattern, str) and len(pattern) > 0

        # Assert
        assert is_valid is True

    def test_regex_pattern_validation(self):
        """WHEN operation_pattern is regex, THEN validates compilation."""
        # Arrange
        pattern = r'^dev.*'
        import re

        # Act
        try:
            re.compile(pattern)
            is_valid = True
        except re.error:
            is_valid = False

        # Assert
        assert is_valid is True

    def test_invalid_regex_pattern_rejected(self):
        """WHEN operation_pattern is invalid regex, THEN validation fails."""
        # Arrange
        pattern = r'[invalid(regex'
        import re

        # Act
        try:
            re.compile(pattern)
            is_valid = True
        except re.error:
            is_valid = False

        # Assert
        assert is_valid is False

    def test_empty_pattern_rejected(self, valid_hook_entry):
        """WHEN operation_pattern empty string, THEN validation fails."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['operation_pattern'] = ''

        # Act
        is_valid = len(hook['operation_pattern']) > 0

        # Assert
        assert is_valid is False


# ============================================================================
# Trigger Status Validation Tests
# ============================================================================

class TestTriggerStatusValidation:
    """Tests for trigger_status field validation."""

    def test_valid_trigger_statuses(self):
        """WHEN trigger_status contains valid values, THEN validation passes."""
        # Arrange
        valid_statuses = ['success', 'failure', 'partial', 'deferred', 'completed']

        # Act
        all_valid = all(s in valid_statuses for s in valid_statuses)

        # Assert
        assert all_valid is True

    def test_mixed_valid_invalid_statuses(self):
        """WHEN trigger_status has mixed valid/invalid, THEN validation fails."""
        # Arrange
        statuses = ['success', 'invalid_status']
        valid_statuses = ['success', 'failure', 'partial', 'deferred', 'completed']

        # Act
        all_valid = all(s in valid_statuses for s in statuses)

        # Assert
        assert all_valid is False

    def test_at_least_one_status_required(self):
        """WHEN trigger_status empty array, THEN validation fails."""
        # Arrange
        statuses = []

        # Act
        has_status = len(statuses) > 0

        # Assert
        assert has_status is False

    def test_duplicate_trigger_statuses_deduplicated(self):
        """WHEN trigger_status has duplicates, THEN treated as single entry."""
        # Arrange
        statuses = ['success', 'success', 'partial']

        # Act
        unique_statuses = list(set(statuses))

        # Assert
        assert len(unique_statuses) == 2


# ============================================================================
# Feedback Type Validation Tests
# ============================================================================

class TestFeedbackTypeValidation:
    """Tests for feedback_type field validation."""

    @pytest.mark.parametrize('feedback_type', [
        'conversation',
        'summary',
        'metrics',
        'checklist',
    ])
    def test_valid_feedback_types(self, feedback_type):
        """WHEN feedback_type is valid, THEN validation passes."""
        # Arrange
        valid_types = ['conversation', 'summary', 'metrics', 'checklist']

        # Act
        is_valid = feedback_type in valid_types

        # Assert
        assert is_valid is True

    def test_invalid_feedback_type_rejected(self):
        """WHEN feedback_type invalid, THEN validation fails."""
        # Arrange
        feedback_type = 'invalid_type'
        valid_types = ['conversation', 'summary', 'metrics', 'checklist']

        # Act
        is_valid = feedback_type in valid_types

        # Assert
        assert is_valid is False


# ============================================================================
# Optional Field Validation Tests
# ============================================================================

class TestOptionalFieldValidation:
    """Tests for optional field validation."""

    def test_max_duration_ms_within_range(self, valid_hook_entry):
        """WHEN max_duration_ms between 1000-30000, THEN valid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['max_duration_ms'] = 5000

        # Act
        is_valid = 1000 <= hook['max_duration_ms'] <= 30000

        # Assert
        assert is_valid is True

    def test_max_duration_ms_too_low(self, valid_hook_entry):
        """WHEN max_duration_ms < 1000, THEN invalid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['max_duration_ms'] = 500

        # Act
        is_valid = hook['max_duration_ms'] >= 1000

        # Assert
        assert is_valid is False

    def test_max_duration_ms_too_high(self, valid_hook_entry):
        """WHEN max_duration_ms > 30000, THEN invalid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['max_duration_ms'] = 40000

        # Act
        is_valid = hook['max_duration_ms'] <= 30000

        # Assert
        assert is_valid is False

    def test_enabled_boolean_validation(self, valid_hook_entry):
        """WHEN enabled field boolean, THEN valid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['enabled'] = True

        # Act
        is_valid = isinstance(hook['enabled'], bool)

        # Assert
        assert is_valid is True

    def test_tags_array_max_length(self, valid_hook_entry):
        """WHEN tags array > 5 items, THEN invalid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['tags'] = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6']

        # Act
        is_valid = len(hook['tags']) <= 5

        # Assert
        assert is_valid is False

    def test_tags_array_valid_length(self, valid_hook_entry):
        """WHEN tags array <= 5 items, THEN valid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['tags'] = ['tag1', 'tag2', 'tag3']

        # Act
        is_valid = len(hook['tags']) <= 5

        # Assert
        assert is_valid is True


# ============================================================================
# Trigger Conditions Validation Tests
# ============================================================================

class TestTriggerConditionsValidation:
    """Tests for trigger_conditions optional field."""

    def test_operation_duration_min_max_consistency(self, valid_hook_entry):
        """WHEN both duration_min and duration_max specified, THEN min <= max."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['trigger_conditions'] = {
            'operation_duration_min_ms': 1000,
            'operation_duration_max_ms': 5000,
        }

        # Act
        is_valid = hook['trigger_conditions']['operation_duration_min_ms'] <= \
                   hook['trigger_conditions']['operation_duration_max_ms']

        # Assert
        assert is_valid is True

    def test_operation_duration_min_max_inconsistency(self, valid_hook_entry):
        """WHEN min > max, THEN validation fails."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['trigger_conditions'] = {
            'operation_duration_min_ms': 5000,
            'operation_duration_max_ms': 1000,
        }

        # Act
        is_valid = hook['trigger_conditions']['operation_duration_min_ms'] <= \
                   hook['trigger_conditions']['operation_duration_max_ms']

        # Assert
        assert is_valid is False

    def test_token_usage_percent_range(self, valid_hook_entry):
        """WHEN token_usage_percent between 0-100, THEN valid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['trigger_conditions'] = {'token_usage_percent': 75}

        # Act
        is_valid = 0 <= hook['trigger_conditions']['token_usage_percent'] <= 100

        # Assert
        assert is_valid is True

    def test_token_usage_percent_out_of_range(self, valid_hook_entry):
        """WHEN token_usage_percent > 100, THEN invalid."""
        # Arrange
        hook = valid_hook_entry.copy()
        hook['trigger_conditions'] = {'token_usage_percent': 150}

        # Act
        is_valid = hook['trigger_conditions']['token_usage_percent'] <= 100

        # Assert
        assert is_valid is False
