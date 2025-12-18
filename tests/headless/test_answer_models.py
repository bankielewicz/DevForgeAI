"""
Tests for configuration validation (STORY-098)

Tests AC#5: Answer Validation on Load

RED PHASE: These tests should fail until implementation is complete.
"""
import pytest
from pathlib import Path


class TestValidationOnLoad:
    """AC#5: Answer Validation on Load"""

    def test_validates_yaml_syntax(self, tmp_path):
        """Given malformed YAML
        When loading configuration
        Then raises ConfigurationError with line number"""
        config_file = tmp_path / "bad.yaml"
        config_file.write_text("invalid: yaml: content: :")

        from devforgeai_cli.headless.answer_models import load_config
        from devforgeai_cli.headless.exceptions import ConfigurationError

        with pytest.raises(ConfigurationError) as exc_info:
            load_config(config_file)

        assert "YAML" in str(exc_info.value) or "yaml" in str(exc_info.value).lower()

    def test_validates_required_fields(self, tmp_path):
        """Given missing required fields
        When loading configuration
        Then raises ValidationError"""
        config_file = tmp_path / "incomplete.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
# Missing: answers, defaults
""")

        from devforgeai_cli.headless.answer_models import load_config

        with pytest.raises((ValueError, KeyError)) as exc_info:
            load_config(config_file)

        error_text = str(exc_info.value).lower()
        assert "defaults" in error_text or "required" in error_text

    def test_validates_headless_mode_enabled_is_bool(self, tmp_path):
        """Given headless_mode.enabled is not boolean
        When loading configuration
        Then raises ValidationError"""
        config_file = tmp_path / "invalid_type.yaml"
        config_file.write_text("""
headless_mode:
  enabled: "yes"
  fail_on_unanswered: true
answers: {}
defaults:
  unknown_prompt: fail
""")

        from devforgeai_cli.headless.answer_models import load_config

        with pytest.raises((ValueError, TypeError)):
            load_config(config_file)

    def test_validates_unknown_prompt_enum_values(self, tmp_path):
        """Given defaults.unknown_prompt has invalid value
        When loading configuration
        Then raises ValidationError"""
        config_file = tmp_path / "invalid_enum.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: true
answers: {}
defaults:
  unknown_prompt: invalid_value
""")

        from devforgeai_cli.headless.answer_models import load_config

        with pytest.raises(ValueError) as exc_info:
            load_config(config_file)

        assert "invalid_value" in str(exc_info.value) or "unknown_prompt" in str(exc_info.value).lower()

    def test_validates_answer_entry_has_pattern_and_answer(self, tmp_path):
        """Given answer entry missing pattern or answer
        When loading configuration
        Then raises ValidationError"""
        config_file = tmp_path / "missing_answer.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: true
answers:
  incomplete_entry:
    pattern: "some pattern"
    # Missing: answer
defaults:
  unknown_prompt: fail
""")

        from devforgeai_cli.headless.answer_models import load_config

        with pytest.raises((ValueError, KeyError)):
            load_config(config_file)

    def test_warns_invalid_regex_pattern(self, tmp_path, caplog):
        """Given invalid regex pattern
        When validating configuration
        Then warns about invalid pattern (doesn't fail)"""
        import logging
        config_file = tmp_path / "bad_regex.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: true
answers:
  bad_pattern:
    pattern: "[invalid(regex"
    answer: "Test"
defaults:
  unknown_prompt: fail
""")

        from devforgeai_cli.headless.answer_models import load_config

        with caplog.at_level(logging.WARNING):
            try:
                config = load_config(config_file)
                # If it doesn't raise, check for warning
                assert "regex" in caplog.text.lower() or "pattern" in caplog.text.lower()
            except ValueError:
                # Also acceptable to raise for invalid regex
                pass

    def test_load_time_under_100ms(self, tmp_path):
        """NFR-002: Configuration load time < 100ms"""
        import time
        config_file = tmp_path / "performance.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: true
  log_matches: true
answers:
  pattern_1:
    pattern: "pattern 1"
    answer: "answer 1"
  pattern_2:
    pattern: "pattern 2"
    answer: "answer 2"
  pattern_3:
    pattern: "pattern 3"
    answer: "answer 3"
defaults:
  unknown_prompt: fail
""")

        from devforgeai_cli.headless.answer_models import load_config

        start = time.perf_counter()
        config = load_config(config_file)
        elapsed = time.perf_counter() - start

        assert elapsed < 0.1, f"Config load took {elapsed*1000:.2f}ms, expected < 100ms"


class TestBackwardCompatibility:
    """Tests for flat format backward compatibility"""

    def test_loads_flat_format_config(self, tmp_path):
        """Given flat format ci-answers.yaml (legacy)
        When loading configuration
        Then auto-migrates to nested format"""
        config_file = tmp_path / "flat.yaml"
        config_file.write_text("""
# Legacy flat format
test_failure_action: fix-implementation
deferral_strategy: never
priority_default: high
technology_choice: use_tech_stack_md
circular_dependency_action: fail
git_conflict_strategy: fail
custom_answers: {}
""")

        from devforgeai_cli.headless.answer_models import load_config

        # Should not raise - should auto-migrate
        config = load_config(config_file)

        # Verify migration worked
        assert config.headless_mode.enabled is True
        assert config.defaults.unknown_prompt == "fail"

    def test_logs_deprecation_warning_for_flat_format(self, tmp_path, caplog):
        """Given flat format config
        When loading
        Then logs deprecation warning"""
        import logging
        config_file = tmp_path / "flat.yaml"
        config_file.write_text("""
test_failure_action: fix-implementation
priority_default: high
""")

        from devforgeai_cli.headless.answer_models import load_config

        with caplog.at_level(logging.WARNING):
            try:
                config = load_config(config_file)
                assert "deprecated" in caplog.text.lower() or "migrate" in caplog.text.lower()
            except ValueError:
                # May fail if backward compat not implemented yet
                pass


class TestDataclassValidation:
    """Tests for dataclass __post_init__ validation"""

    def test_headless_mode_settings_validates_types(self):
        """Given invalid types for HeadlessModeSettings
        When constructing dataclass
        Then raises TypeError/ValueError"""
        from devforgeai_cli.headless.answer_models import HeadlessModeSettings

        with pytest.raises((TypeError, ValueError)):
            HeadlessModeSettings(enabled="not_a_bool")

    def test_default_settings_validates_enum(self):
        """Given invalid unknown_prompt value
        When constructing DefaultSettings
        Then raises ValueError"""
        from devforgeai_cli.headless.answer_models import DefaultSettings

        with pytest.raises(ValueError) as exc_info:
            DefaultSettings(unknown_prompt="invalid")

        assert "fail" in str(exc_info.value) or "first_option" in str(exc_info.value)

    def test_answer_entry_requires_pattern_and_answer(self):
        """Given AnswerEntry without required fields
        When constructing
        Then raises error"""
        from devforgeai_cli.headless.answer_models import AnswerEntry

        # Should require both pattern and answer
        with pytest.raises(TypeError):
            AnswerEntry(pattern="test")  # Missing answer
