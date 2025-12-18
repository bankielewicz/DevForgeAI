"""
Tests for pattern matching logic (STORY-098)

Tests AC#2: Answer Matching Logic
Tests AC#4: Default Answer Fallback

RED PHASE: These tests should fail until implementation is complete.
"""
import pytest


class TestPatternMatching:
    """AC#2: Answer Matching Logic"""

    def test_exact_pattern_match(self):
        """Given answer with pattern 'What is the story priority'
        When prompt matches exactly
        Then returns configured answer"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {
            "priority": {"pattern": "What is the story priority", "answer": "High"}
        }
        matcher = PromptPatternMatcher(patterns)

        result = matcher.match("What is the story priority?")
        assert result is not None
        assert result.answer == "High"
        assert result.key == "priority"

    def test_regex_pattern_match(self):
        """Given answer with regex pattern 'Tests failed.*proceed'
        When prompt contains matching text
        Then returns configured answer"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {
            "test_failure": {"pattern": "Tests failed.*proceed", "answer": "Fix implementation"}
        }
        matcher = PromptPatternMatcher(patterns)

        result = matcher.match("Tests failed. How should we proceed?")
        assert result is not None
        assert result.answer == "Fix implementation"

    def test_case_insensitive_matching(self):
        """Given pattern with mixed case
        When prompt has different case
        Then still matches (case insensitive by default)"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {
            "approval": {"pattern": "do you approve", "answer": "Yes"}
        }
        matcher = PromptPatternMatcher(patterns)

        result = matcher.match("Do You Approve this change?")
        assert result is not None
        assert result.answer == "Yes"

    def test_first_match_wins(self):
        """Given multiple patterns that could match
        When prompt matches both
        Then returns first matching pattern"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        # Order matters - first match wins
        patterns = {
            "specific": {"pattern": "story priority High", "answer": "Already High"},
            "general": {"pattern": "story priority", "answer": "Medium"}
        }
        matcher = PromptPatternMatcher(patterns)

        result = matcher.match("What is the story priority High or Medium?")
        assert result is not None
        assert result.answer == "Already High"

    def test_logs_match_selection(self, caplog):
        """AC#2: Given log_matches: true in config
        When match found
        Then logs 'CI Mode: Selected '{answer}' for prompt '{pattern}''"""
        import logging
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {
            "priority": {"pattern": "What is the story priority", "answer": "High"}
        }
        matcher = PromptPatternMatcher(patterns, log_matches=True)

        with caplog.at_level(logging.INFO):
            result = matcher.match("What is the story priority?")

        assert "CI Mode: Selected 'High'" in caplog.text
        assert "priority" in caplog.text.lower()

    def test_no_match_returns_none(self):
        """Given pattern that doesn't match prompt
        When match called
        Then returns None"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {
            "priority": {"pattern": "story priority", "answer": "High"}
        }
        matcher = PromptPatternMatcher(patterns)

        result = matcher.match("Completely unrelated prompt about something else")
        assert result is None


class TestDefaultFallback:
    """AC#4: Default Answer Fallback"""

    def test_uses_first_option_when_default_set(self):
        """Given defaults.unknown_prompt: 'first_option'
        When no pattern matches
        Then returns first option"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {}
        matcher = PromptPatternMatcher(patterns, default_strategy="first_option")

        result = matcher.match_with_fallback(
            "Some unknown prompt",
            options=["Option A", "Option B", "Option C"]
        )
        assert result is not None
        assert result.answer == "Option A"
        assert result.is_default is True

    def test_logs_warning_for_default_usage(self, caplog):
        """AC#4: Given default answer used
        When resolution succeeds via default
        Then logs warning 'Using default answer for unmatched prompt'"""
        import logging
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {}
        matcher = PromptPatternMatcher(patterns, default_strategy="first_option", log_matches=True)

        with caplog.at_level(logging.WARNING):
            result = matcher.match_with_fallback(
                "Unknown prompt",
                options=["First", "Second"]
            )

        assert "Using default answer for unmatched prompt" in caplog.text

    def test_skip_strategy_returns_none(self):
        """Given defaults.unknown_prompt: 'skip'
        When no pattern matches
        Then returns None (skip resolution)"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        patterns = {}
        matcher = PromptPatternMatcher(patterns, default_strategy="skip")

        result = matcher.match_with_fallback(
            "Unknown prompt",
            options=["A", "B"]
        )
        assert result is None

    def test_fail_strategy_raises_exception(self):
        """Given defaults.unknown_prompt: 'fail'
        When no pattern matches
        Then raises exception"""
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher
        from devforgeai_cli.headless.exceptions import HeadlessResolutionError

        patterns = {}
        matcher = PromptPatternMatcher(patterns, default_strategy="fail")

        with pytest.raises(HeadlessResolutionError):
            matcher.match_with_fallback(
                "Unknown prompt",
                options=["A", "B"]
            )


class TestPerformance:
    """NFR-001: Answer resolution time < 10ms per prompt lookup"""

    def test_pattern_matching_under_10ms(self):
        """Given 50 configured patterns
        When matching a prompt
        Then completes in under 10ms"""
        import time
        from devforgeai_cli.headless.pattern_matcher import PromptPatternMatcher

        # Create 50 patterns
        patterns = {
            f"pattern_{i}": {"pattern": f"pattern text {i}", "answer": f"Answer {i}"}
            for i in range(50)
        }
        matcher = PromptPatternMatcher(patterns)

        # Warm up
        matcher.match("pattern text 25")

        # Measure
        start = time.perf_counter()
        for _ in range(100):
            matcher.match("pattern text 42")
        elapsed = (time.perf_counter() - start) / 100  # Average time per match

        # Assert under 10ms (0.01 seconds)
        assert elapsed < 0.01, f"Pattern matching took {elapsed*1000:.2f}ms, expected < 10ms"
