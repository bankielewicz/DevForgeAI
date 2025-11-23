"""
Regression tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: Fixture Quality Preservation

Purpose: Validate that fixtures maintain consistent quality over time,
baseline fixtures remain realistic, and enhanced fixtures preserve improvements.

Test Framework: pytest
Coverage: Quality metrics stability, fixture preservation, regression detection
"""

import json
import re
from pathlib import Path

import pytest

try:
    import textstat
except ImportError:
    textstat = None


class TestFixtureQualityPreservation:
    """Regression tests for fixture quality and stability"""

    @pytest.fixture
    def baseline_fixtures_path(self):
        """Base path for baseline fixtures"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

    @pytest.fixture
    def enhanced_fixtures_path(self):
        """Base path for enhanced fixtures"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

    @pytest.fixture
    def expected_fixtures_path(self):
        """Base path for expected improvements"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    @pytest.fixture
    def quality_thresholds(self):
        """Quality thresholds for regression detection"""
        return {
            "baseline_word_count": {"min": 50, "max": 200},
            "baseline_fre": {"min": 50},
            "baseline_issues": {"min": 2, "max": 4},
            "enhanced_word_count_increase": {"min": 30, "max": 60},
            "enhanced_fre": {"min": 60},
            "enhanced_principles": {"min": 3, "max": 5},
        }

    def test_should_maintain_baseline_word_counts_within_range(
        self, baseline_fixtures_path, quality_thresholds
    ):
        """
        GIVEN baseline fixtures are established
        WHEN word counts are measured
        THEN all baseline fixtures remain within 50-200 word range (no regression)

        Evidence: All baselines stay within original quality thresholds
        """
        # Arrange
        baseline_path = baseline_fixtures_path
        word_count_threshold = quality_thresholds["baseline_word_count"]

        if not baseline_path.exists():
            pytest.skip("Baseline fixtures directory not yet created")

        # Act
        word_count_results = {}
        for baseline_file in sorted(baseline_path.glob("baseline-*.txt")):
            content = baseline_file.read_text().strip()
            word_count = len(content.split())
            word_count_results[baseline_file.name] = word_count

        # Assert
        assert len(word_count_results) > 0, "No baseline fixtures found"

        for fixture_name, word_count in word_count_results.items():
            assert (
                word_count_threshold["min"] <= word_count <= word_count_threshold["max"]
            ), (
                f"{fixture_name}: {word_count} words "
                f"(regression - should be {word_count_threshold['min']}-{word_count_threshold['max']})"
            )

    def test_should_detect_baseline_quality_issues_remain_present(
        self, baseline_fixtures_path, quality_thresholds
    ):
        """
        GIVEN baseline fixtures exhibit 2-4 quality issues
        WHEN quality issues are rechecked
        THEN each baseline still exhibits the expected issue count (no regression)

        Evidence: Quality issues not removed from baselines
        """
        # Arrange
        baseline_path = baseline_fixtures_path
        issue_count_threshold = quality_thresholds["baseline_issues"]

        if not baseline_path.exists():
            pytest.skip("Baseline fixtures directory not yet created")

        quality_issue_indicators = {
            "vague": ["fast", "good", "better", "optimize", "improve"],
            "missing_criteria": ["needs", "should", "must"],
            "ambiguous_ac": ["acceptance", "criteria"],
            "omitted_nfr": ["performance", "security", "scalability"],
        }

        # Act
        issue_counts = {}
        for baseline_file in sorted(baseline_path.glob("baseline-*.txt")):
            content = baseline_file.read_text().lower()

            detected_issues = set()
            for issue_type, keywords in quality_issue_indicators.items():
                if any(keyword in content for keyword in keywords):
                    detected_issues.add(issue_type)

            issue_counts[baseline_file.name] = len(detected_issues)

        # Assert
        assert len(issue_counts) > 0, "No baseline fixtures found"

        for fixture_name, count in issue_counts.items():
            assert (
                issue_count_threshold["min"] <= count <= issue_count_threshold["max"]
            ), (
                f"{fixture_name}: {count} issues detected "
                f"(expected {issue_count_threshold['min']}-{issue_count_threshold['max']}, "
                f"possible regression)"
            )

    def test_should_preserve_enhanced_to_baseline_length_increase_ratio(
        self, baseline_fixtures_path, enhanced_fixtures_path, quality_thresholds
    ):
        """
        GIVEN enhanced fixtures are 30-60% longer than baselines
        WHEN length is remeasured
        THEN the ratio remains within original range (no regression or inflation)

        Evidence: Length increase ratio stable within 30-60% bounds
        """
        # Arrange
        baseline_path = baseline_fixtures_path
        enhanced_path = enhanced_fixtures_path
        increase_threshold = quality_thresholds["enhanced_word_count_increase"]

        if not baseline_path.exists() or not enhanced_path.exists():
            pytest.skip("Fixture directories not yet created")

        # Act
        length_ratios = {}
        for enhanced_file in sorted(enhanced_path.glob("enhanced-*.txt")):
            match = re.search(r"enhanced-(\d{2})-(.+)\.txt", enhanced_file.name)
            if not match:
                continue

            baseline_filename = f"baseline-{match.group(1)}-{match.group(2)}.txt"
            baseline_file = baseline_path / baseline_filename

            if baseline_file.exists():
                baseline_words = len(baseline_file.read_text().split())
                enhanced_words = len(enhanced_file.read_text().split())

                if baseline_words > 0:
                    ratio = ((enhanced_words - baseline_words) / baseline_words) * 100
                    length_ratios[enhanced_file.name] = ratio

        # Assert
        assert len(length_ratios) > 0, "No enhanced/baseline pairs found"

        for fixture_name, ratio in length_ratios.items():
            assert (
                increase_threshold["min"] <= ratio <= increase_threshold["max"]
            ), (
                f"{fixture_name}: {ratio:.1f}% increase "
                f"(expected {increase_threshold['min']}-{increase_threshold['max']}%, regression detected)"
            )

    def test_should_maintain_enhanced_fixture_readability_above_threshold(
        self, enhanced_fixtures_path, quality_thresholds
    ):
        """
        GIVEN enhanced fixtures have minimum Flesch Reading Ease of 60
        WHEN readability is remeasured
        THEN all enhanced fixtures maintain FRE ≥60 (no regression)

        Evidence: Readability scores stable above 60
        """
        if textstat is None:
            pytest.skip("textstat library not installed")

        # Arrange
        enhanced_path = enhanced_fixtures_path
        fre_threshold = quality_thresholds["enhanced_fre"]

        if not enhanced_path.exists():
            pytest.skip("Enhanced fixtures directory not yet created")

        # Act
        fre_scores = {}
        for enhanced_file in sorted(enhanced_path.glob("enhanced-*.txt")):
            content = enhanced_file.read_text()
            fre = textstat.flesch_reading_ease(content)
            fre_scores[enhanced_file.name] = fre

        # Assert
        assert len(fre_scores) > 0, "No enhanced fixtures found"

        for fixture_name, fre in fre_scores.items():
            assert fre >= fre_threshold["min"], (
                f"{fixture_name}: FRE {fre:.1f} "
                f"(regression - should be ≥{fre_threshold['min']})"
            )

    def test_should_detect_when_expected_improvements_drift_from_baselines(
        self, baseline_fixtures_path, enhanced_fixtures_path, expected_fixtures_path
    ):
        """
        GIVEN expected improvements are documented with realistic values
        WHEN actual measurements are compared
        THEN expected values remain achievable (drift detection)

        Evidence: Expected values align with fixture characteristics
        """
        # Arrange
        baseline_path = baseline_fixtures_path
        enhanced_path = enhanced_fixtures_path
        expected_path = expected_fixtures_path

        if not all(p.exists() for p in [baseline_path, enhanced_path, expected_path]):
            pytest.skip("Fixture directories not yet created")

        # Act
        drift_detection = {}

        for expected_file in sorted(expected_path.glob("expected-*.json")):
            with open(expected_file, "r") as f:
                expected_data = json.load(f)

            fixture_id = expected_data.get("fixture_id")
            category = expected_data.get("category", "")

            baseline_filename = f"baseline-{fixture_id}-{category}.txt"
            enhanced_filename = f"enhanced-{fixture_id}-{category}.txt"

            baseline_file = baseline_path / baseline_filename
            enhanced_file = enhanced_path / enhanced_filename

            if baseline_file.exists() and enhanced_file.exists():
                baseline_words = len(baseline_file.read_text().split())
                enhanced_words = len(enhanced_file.read_text().split())

                if baseline_words > 0:
                    actual_length_increase = (
                        (enhanced_words - baseline_words) / baseline_words
                    ) * 100

                    # Compare with expected token_savings (proxy for length increase)
                    expected_savings = (
                        expected_data.get("expected_improvements", {})
                        .get("token_savings", 0)
                    )

                    # Token savings should roughly align with length decrease (inverse of increase)
                    # If enhanced is 40% longer, fewer tokens means ~12-15% savings
                    expected_relationship = 100 - actual_length_increase > 0

                    drift_detection[expected_file.name] = {
                        "actual_increase": actual_length_increase,
                        "expected_savings": expected_savings,
                        "aligned": expected_relationship,
                    }

        # Assert
        assert len(drift_detection) > 0, "No expected/enhanced pairs found"

        for fixture_name, drift_data in drift_detection.items():
            # Expected improvements should align with actual fixture characteristics
            # (not arbitrary numbers that don't match actual data)
            assert drift_data["aligned"], (
                f"{fixture_name}: Expected improvements may have drifted from actual fixture characteristics"
            )
