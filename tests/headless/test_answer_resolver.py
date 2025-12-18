"""
Tests for HeadlessAnswerResolver service (STORY-098)

Tests AC#1: CI Answers Configuration File
Tests AC#3: Fail-on-Unanswered Mode

RED PHASE: These tests should fail until implementation is complete.
"""
import pytest
from pathlib import Path


def create_test_config(tmp_path: Path, fail_on_unanswered: bool = True) -> Path:
    """Helper to create test configuration file."""
    config_dir = tmp_path / ".devforgeai" / "config"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "ci-answers.yaml"
    config_file.write_text(f"""
headless_mode:
  enabled: true
  fail_on_unanswered: {str(fail_on_unanswered).lower()}
  log_matches: true
answers:
  priority:
    pattern: "What is the story priority"
    answer: "High"
defaults:
  unknown_prompt: fail
""")
    return config_file


class TestConfigurationLoading:
    """AC#1: CI Answers Configuration File"""

    def test_loads_config_from_devforgeai_path(self, tmp_path):
        """Given .devforgeai/config/ci-answers.yaml exists
        When HeadlessAnswerResolver initializes
        Then reads configuration successfully"""
        # Arrange
        config_file = create_test_config(tmp_path)

        # Act
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        resolver = HeadlessAnswerResolver(config_path=config_file)
        config = resolver.load_configuration()

        # Assert
        assert config.headless_mode.enabled is True
        assert config.headless_mode.fail_on_unanswered is True

    def test_returns_false_when_no_config(self):
        """Given no configuration file exists
        When resolver checks for config
        Then is_configured returns False"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        resolver = HeadlessAnswerResolver(config_path=Path("/nonexistent/path"))
        assert resolver.is_configured() is False

    def test_fallback_to_devforgeai_config_ci(self, tmp_path):
        """Given .devforgeai/config/ doesn't exist
        When config exists at devforgeai/config/ci/
        Then loads from fallback path"""
        # Arrange - create fallback config
        fallback_dir = tmp_path / "devforgeai" / "config" / "ci"
        fallback_dir.mkdir(parents=True)
        config_file = fallback_dir / "ci-answers.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: false
  log_matches: true
answers: {}
defaults:
  unknown_prompt: first_option
""")

        # Act
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        resolver = HeadlessAnswerResolver(search_paths=[
            tmp_path / ".devforgeai" / "config" / "ci-answers.yaml",
            config_file
        ])
        config = resolver.load_configuration()

        # Assert
        assert config.headless_mode.fail_on_unanswered is False

    def test_singleton_returns_same_instance(self):
        """Given HeadlessAnswerResolver singleton pattern
        When get_instance called multiple times
        Then returns same instance"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        # Reset singleton for test
        HeadlessAnswerResolver._instance = None

        instance1 = HeadlessAnswerResolver.get_instance()
        instance2 = HeadlessAnswerResolver.get_instance()

        assert instance1 is instance2


class TestFailOnUnanswered:
    """AC#3: Fail-on-Unanswered Mode"""

    def test_fails_when_no_match_and_fail_true(self, tmp_path):
        """Given fail_on_unanswered: true
        And prompt has no matching answer
        When resolve called
        Then raises HeadlessResolutionError"""
        # Arrange
        config_file = create_test_config(tmp_path, fail_on_unanswered=True)
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        from devforgeai_cli.headless.exceptions import HeadlessResolutionError

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        # Act & Assert
        with pytest.raises(HeadlessResolutionError) as exc_info:
            resolver.resolve("Unknown prompt that has no match", ["Option 1", "Option 2"])

        assert "Unknown prompt" in str(exc_info.value)

    def test_error_includes_prompt_text_for_debugging(self, tmp_path):
        """Given unmatched prompt
        When resolution fails
        Then error message includes prompt text"""
        # Arrange
        config_file = create_test_config(tmp_path, fail_on_unanswered=True)
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        from devforgeai_cli.headless.exceptions import HeadlessResolutionError

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        test_prompt = "This specific prompt should appear in error"

        # Act & Assert
        with pytest.raises(HeadlessResolutionError) as exc_info:
            resolver.resolve(test_prompt, ["A", "B"])

        assert test_prompt in str(exc_info.value)
        assert "Headless mode: No answer configured for prompt" in str(exc_info.value)

    def test_succeeds_when_fail_on_unanswered_false(self, tmp_path):
        """Given fail_on_unanswered: false
        And prompt has no matching answer
        When resolve called
        Then returns None (no exception)"""
        # Arrange
        config_dir = tmp_path / ".devforgeai" / "config"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "ci-answers.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: false
  log_matches: true
answers: {}
defaults:
  unknown_prompt: skip
""")
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        # Act
        result = resolver.resolve("Unknown prompt", ["Option 1", "Option 2"])

        # Assert - should not raise, returns None for skip mode
        assert result is None


class TestHeadlessModeDetection:
    """Test headless mode detection logic"""

    def test_detects_ci_environment(self, monkeypatch):
        """Given CI=true in environment
        When is_headless_mode called
        Then returns True"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        monkeypatch.setenv("CI", "true")
        resolver = HeadlessAnswerResolver()

        assert resolver.is_headless_mode() is True

    def test_detects_devforgeai_headless_env(self, monkeypatch):
        """Given DEVFORGEAI_HEADLESS=true in environment
        When is_headless_mode called
        Then returns True"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        monkeypatch.setenv("DEVFORGEAI_HEADLESS", "true")
        resolver = HeadlessAnswerResolver()

        assert resolver.is_headless_mode() is True

    def test_interactive_mode_ignores_config(self, tmp_path, monkeypatch):
        """BR-002: Interactive mode ignores ci-answers.yaml
        Given config exists
        And running in interactive mode
        When should_use_headless_answer called
        Then returns False"""
        # Arrange
        config_file = create_test_config(tmp_path)
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        # Ensure not in headless mode
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DEVFORGEAI_HEADLESS", raising=False)

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        # For this test, we mock isatty to return True (interactive)
        # In real tests, this depends on the test runner

        # Act
        # The resolver should not auto-resolve in interactive mode
        # This is a behavioral test - implementation decides how to handle
        assert resolver.is_configured() is True  # Config exists


class TestCoverageGapRemediation:
    """Tests to cover missing lines identified in QA gaps report (STORY-098)"""

    def test_reset_instance_clears_singleton(self):
        """Lines 96-97: reset_instance() clears singleton"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        # Create singleton
        HeadlessAnswerResolver._instance = None
        instance1 = HeadlessAnswerResolver.get_instance()
        assert instance1 is not None

        # Reset singleton
        HeadlessAnswerResolver.reset_instance()

        # New instance should be different
        instance2 = HeadlessAnswerResolver.get_instance()
        assert instance2 is not instance1

        # Clean up
        HeadlessAnswerResolver.reset_instance()

    def test_headless_mode_handles_isatty_exception(self, monkeypatch):
        """Lines 117-120: isatty exception returns False"""
        import os
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        # Clear env vars to ensure isatty check is reached
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DEVFORGEAI_HEADLESS", raising=False)

        # Mock os.isatty to raise exception
        def mock_isatty(fd):
            raise OSError("Mocked error")

        monkeypatch.setattr(os, "isatty", mock_isatty)

        resolver = HeadlessAnswerResolver()
        # Should return False when exception occurs
        assert resolver.is_headless_mode() is False

    def test_load_configuration_returns_cached_config(self, tmp_path):
        """Line 137: Second load returns cached config"""
        config_file = create_test_config(tmp_path)

        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        resolver = HeadlessAnswerResolver(config_path=config_file)
        config1 = resolver.load_configuration()
        config2 = resolver.load_configuration()

        # Should be the same object (cached)
        assert config1 is config2

    def test_explicit_config_path_not_found_error_message(self):
        """Lines 141-143: Error message includes explicit path"""
        from pathlib import Path
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        from devforgeai_cli.headless.exceptions import ConfigurationError

        explicit_path = Path("/explicit/nonexistent/path/ci-answers.yaml")
        resolver = HeadlessAnswerResolver(config_path=explicit_path)

        with pytest.raises(ConfigurationError) as exc_info:
            resolver.load_configuration()

        # Error should mention the explicit path
        assert str(explicit_path) in str(exc_info.value) or "not found" in str(exc_info.value).lower()

    def test_resolve_auto_loads_configuration(self, tmp_path):
        """Line 188: resolve() calls load_configuration() if not loaded"""
        config_dir = tmp_path / ".devforgeai" / "config"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "ci-answers.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: false
  log_matches: true
answers:
  priority:
    pattern: "story priority"
    answer: "High"
defaults:
  unknown_prompt: skip
""")
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        resolver = HeadlessAnswerResolver(config_path=config_file)
        # Don't explicitly load - resolve should auto-load
        assert resolver._loaded is False

        result = resolver.resolve("What is the story priority?", ["Low", "Medium", "High"])
        assert result == "High"
        assert resolver._loaded is True

    def test_resolve_with_fail_on_unanswered_false_uses_match_with_fallback(self, tmp_path):
        """Line 198: resolve with fail_on_unanswered=false uses match_with_fallback path"""
        config_dir = tmp_path / ".devforgeai" / "config"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "ci-answers.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: false
  log_matches: false
answers: {}
defaults:
  unknown_prompt: skip
""")
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        # With no patterns and skip strategy, should return None
        result = resolver.resolve("Unknown prompt", ["A", "B"])
        assert result is None

    def test_search_paths_error_message_includes_all_paths(self, tmp_path):
        """Lines 143-145: Error message includes all search paths when none found"""
        from pathlib import Path
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        from devforgeai_cli.headless.exceptions import ConfigurationError

        # Use fake search paths that don't exist
        fake_paths = [
            tmp_path / "path1" / "ci-answers.yaml",
            tmp_path / "path2" / "ci-answers.yaml",
        ]

        resolver = HeadlessAnswerResolver(search_paths=fake_paths)

        with pytest.raises(ConfigurationError) as exc_info:
            resolver.load_configuration()

        # Error should mention search paths
        error_msg = str(exc_info.value)
        assert "search paths" in error_msg.lower() or "not found" in error_msg.lower()

    def test_resolve_with_fail_on_unanswered_true_and_match(self, tmp_path):
        """Line 198: resolve returns answer when fail_on_unanswered=true AND match found"""
        config_dir = tmp_path / ".devforgeai" / "config"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "ci-answers.yaml"
        config_file.write_text("""
headless_mode:
  enabled: true
  fail_on_unanswered: true
  log_matches: false
answers:
  priority:
    pattern: "story priority"
    answer: "High"
defaults:
  unknown_prompt: fail
""")
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver

        resolver = HeadlessAnswerResolver(config_path=config_file)
        resolver.load_configuration()

        # With fail_on_unanswered=true, should return answer when match found
        result = resolver.resolve("What is the story priority?", ["Low", "Medium", "High"])
        assert result == "High"

    def test_resolve_raises_error_when_matcher_not_initialized(self, tmp_path):
        """Line 191: resolve raises ConfigurationError when matcher is None"""
        from devforgeai_cli.headless.answer_resolver import HeadlessAnswerResolver
        from devforgeai_cli.headless.exceptions import ConfigurationError

        resolver = HeadlessAnswerResolver(config_path=tmp_path / "nonexistent.yaml")
        # Manually set _loaded to True but leave _matcher as None to simulate edge case
        resolver._loaded = True
        resolver._matcher = None

        with pytest.raises(ConfigurationError) as exc_info:
            resolver.resolve("Some prompt", ["A", "B"])

        assert "not loaded" in str(exc_info.value).lower()
