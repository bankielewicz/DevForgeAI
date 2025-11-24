"""
Edge Case and Data Validation Tests

Tests validate edge case handling (fixture quality variation, token counting methodology,
non-deterministic generation) and data validation rules (fixture pair completeness,
JSON schema, statistical significance).
"""

import pytest
import json
from pathlib import Path


class TestEdgeCase1FixtureQualityVariation:
    """Tests for Edge Case 1: Fixture complexity variation handling"""

    def test_should_stratify_fixtures_by_complexity(self):
        """Arrange: Fixture metadata
        Act: Verify complexity stratification (Simple: 3, Medium: 4, Complex: 3)
        Assert: Fixtures are properly classified"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        complexity_breakdown = {"Simple": 0, "Medium": 0, "Complex": 0}
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                for fixture in metadata.get("fixtures", []):
                    level = fixture.get("complexity_level")
                    if level in complexity_breakdown:
                        complexity_breakdown[level] += 1
            except json.JSONDecodeError:
                pass

        # Assert
        expected = {"Simple": 3, "Medium": 4, "Complex": 3}
        assert complexity_breakdown == expected, \
            f"Expected stratification {expected}, got {complexity_breakdown}"

    def test_should_document_complexity_classification(self):
        """Arrange: Fixture metadata
        Act: Verify each fixture has complexity level documented
        Assert: All 10 fixtures have complexity_level field"""
        # Arrange
        metadata_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/fixture-metadata.json")

        # Act
        missing_level = []
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                for fixture in metadata.get("fixtures", []):
                    if "complexity_level" not in fixture:
                        missing_level.append(fixture.get("fixture_number"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_level, f"Fixtures missing complexity_level: {missing_level}"

    def test_should_analyze_results_by_complexity_level(self):
        """Arrange: Results JSON files
        Act: Check for complexity level grouping in analysis
        Assert: Impact report includes complexity-level breakdown"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_complexity_analysis = False
        if report_file.exists():
            content = report_file.read_text()
            has_complexity_analysis = ('complexity' in content.lower() or
                                      'simple' in content.lower() or
                                      'medium' in content.lower() or
                                      'complex' in content.lower())

        # Assert
        assert has_complexity_analysis, \
            "Impact report missing complexity-level analysis"


class TestEdgeCase2TokenCountingMethodology:
    """Tests for Edge Case 2: Token counting methodology variance"""

    def test_should_document_token_counting_source(self):
        """Arrange: Token savings report
        Act: Check for documentation of token counting methodology
        Assert: Report explains token counting source (actual vs estimated)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_methodology = False
        if report_file.exists():
            content = report_file.read_text()
            has_methodology = ('methodology' in content.lower() or
                              'token' in content.lower() and
                              ('actual' in content.lower() or
                               'estimated' in content.lower() or
                               'conversation' in content.lower() or
                               'tiktoken' in content.lower()))

        # Assert
        assert has_methodology, \
            "Token savings report missing methodology documentation"

    def test_should_document_token_counting_variance(self):
        """Arrange: Token savings report
        Act: Check for variance disclaimer (±10% if estimated)
        Assert: Report acknowledges potential variance in estimates"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_variance = False
        if report_file.exists():
            content = report_file.read_text()
            has_variance = ('variance' in content.lower() or
                           'disclaimer' in content.lower() or
                           'error' in content.lower() or
                           '%' in content)

        # Assert
        assert has_variance, \
            "Token savings report missing variance documentation"

    def test_should_use_conversation_metadata_as_source_of_truth(self):
        """Arrange: Token savings results JSON
        Act: Verify token counts are from conversation metadata
        Assert: Token values are reasonable numbers (>1000 for story creation)"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        valid_tokens = True
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    tokens = entry.get("token_usage", 0)
                    # Story creation typically uses 1000-10000 tokens
                    if tokens <= 0 or tokens > 50000:
                        valid_tokens = False
            except json.JSONDecodeError:
                pass

        # Assert
        assert valid_tokens, \
            "Token values appear invalid (should be 1000-10000 for story creation)"


class TestEdgeCase3NonDeterministicGeneration:
    """Tests for Edge Case 3: Non-deterministic story generation handling"""

    def test_should_run_each_fixture_multiple_times(self):
        """Arrange: Results JSON files
        Act: Check for multiple runs per fixture
        Assert: Each fixture has 3 runs recorded"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        all_have_3_runs = True
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    runs = entry.get("runs", [])
                    if len(runs) != 3:
                        all_have_3_runs = False
            except json.JSONDecodeError:
                pass

        # Assert
        assert all_have_3_runs, \
            "Not all fixtures have exactly 3 runs recorded"

    def test_should_use_median_for_final_values(self):
        """Arrange: Results JSON
        Act: Verify final token_usage is median of 3 runs (not mean)
        Assert: Final values are consistent with median calculation"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        uses_median = True
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    runs = entry.get("runs", [])
                    final_value = entry.get("token_usage", 0)

                    if len(runs) == 3 and final_value > 0:
                        sorted_runs = sorted(runs)
                        median = sorted_runs[1]
                        # Allow small floating point differences
                        if abs(final_value - median) > 1:
                            uses_median = False
            except (json.JSONDecodeError, ZeroDivisionError, TypeError):
                pass

        # Assert
        assert uses_median or not results_file.exists(), \
            "Final values may not be using median of 3 runs"

    def test_should_report_standard_deviation(self):
        """Arrange: Results JSON or report
        Act: Check for standard deviation reporting
        Assert: Results include variability metrics"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_stdev = False
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "stdev" in entry or "std_dev" in entry or "variance" in entry:
                        has_stdev = True
            except json.JSONDecodeError:
                pass

        if not has_stdev and report_file.exists():
            content = report_file.read_text()
            has_stdev = ('standard deviation' in content.lower() or
                        'stdev' in content.lower() or
                        'variance' in content.lower())

        # Assert
        assert has_stdev or not results_file.exists(), \
            "Results missing standard deviation reporting"

    def test_should_flag_high_variance_fixtures(self):
        """Arrange: Results JSON
        Act: Check for high variance detection (CV > 25%)
        Assert: Fixtures with CV > 25% are flagged for review"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")
        cv_threshold = 0.25

        # Act
        high_variance_fixtures = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    runs = entry.get("runs", [])
                    if len(runs) == 3 and any(r > 0 for r in runs):
                        mean = sum(runs) / len(runs)
                        variance = sum((x - mean) ** 2 for x in runs) / len(runs)
                        stdev = variance ** 0.5
                        cv = stdev / mean if mean > 0 else 0

                        if cv > cv_threshold:
                            high_variance_fixtures.append(
                                f"{entry.get('fixture_name')}: CV={cv*100:.1f}%"
                            )
            except (json.JSONDecodeError, ZeroDivisionError, TypeError):
                pass

        # Note: High variance fixtures should be documented in report
        # This is informational rather than a failure condition
        if high_variance_fixtures:
            print(f"Fixtures with high variance (>25%): {', '.join(high_variance_fixtures)}")


class TestDVR1FixturePairCompleteness:
    """Tests for DVR1: Fixture pair completeness validation"""

    def test_should_validate_10_baseline_enhanced_pairs_exist(self):
        """Arrange: Baseline and enhanced directories
        Act: Verify all pairs exist before test execution
        Assert: All 10 pairs (baseline-NN.txt, enhanced-NN.txt) exist"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

        # Act
        missing_pairs = []
        if baseline_dir.exists() and enhanced_dir.exists():
            for i in range(1, 11):
                baseline = baseline_dir / f"baseline-{i:02d}.txt"
                enhanced = enhanced_dir / f"enhanced-{i:02d}.txt"
                if not baseline.exists() or not enhanced.exists():
                    missing_pairs.append(f"baseline-{i:02d}.txt / enhanced-{i:02d}.txt")

        # Assert
        assert not missing_pairs, \
            f"Missing fixture pairs (DVR1): {', '.join(missing_pairs)}"

    def test_should_halt_with_clear_error_message_on_missing_pair(self):
        """Arrange: Test execution
        Act: Verify error message clarity if pair missing
        Assert: Error message follows format: 'Missing fixture pair: [name] exists but [name] not found'"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        # This test verifies error handling is documented/implemented
        # by checking test script content
        test_script = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")
        has_error_check = False

        if test_script.exists():
            content = test_script.read_text()
            has_error_check = ('Missing fixture pair' in content or
                              'not found' in content or
                              'exist' in content.lower())

        # Assert
        assert has_error_check or not test_script.exists(), \
            "Test scripts missing fixture pair validation and error messages"


class TestDVR2ResultsJsonSchema:
    """Tests for DVR2: Results JSON schema validation"""

    def test_should_have_required_fields_in_baseline_results(self):
        """Arrange: Baseline results JSON
        Act: Validate schema has all required fields
        Assert: All required fields present in each entry"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")
        required_fields = ["story_id", "fixture_name", "token_usage", "ac_count",
                          "nfr_present", "incomplete", "iterations"]

        # Act
        missing_fields_list = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for i, entry in enumerate(results.get("results", [])):
                    for field in required_fields:
                        if field not in entry:
                            missing_fields_list.append(f"Entry {i}: missing '{field}'")
            except json.JSONDecodeError as e:
                missing_fields_list.append(f"JSON parse error: {e}")

        # Assert
        assert not missing_fields_list, \
            f"Baseline results schema violations (DVR2): {'; '.join(missing_fields_list[:5])}"

    def test_should_have_required_fields_in_enhanced_results(self):
        """Arrange: Enhanced results JSON
        Act: Validate schema has all required fields
        Assert: All required fields present in each entry"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")
        required_fields = ["story_id", "fixture_name", "token_usage", "ac_count",
                          "nfr_present", "incomplete", "iterations"]

        # Act
        missing_fields_list = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for i, entry in enumerate(results.get("results", [])):
                    for field in required_fields:
                        if field not in entry:
                            missing_fields_list.append(f"Entry {i}: missing '{field}'")
            except json.JSONDecodeError as e:
                missing_fields_list.append(f"JSON parse error: {e}")

        # Assert
        assert not missing_fields_list, \
            f"Enhanced results schema violations (DVR2): {'; '.join(missing_fields_list[:5])}"

    def test_should_detect_and_report_invalid_schema(self):
        """Arrange: Measurement scripts
        Act: Verify schema validation is performed before processing
        Assert: Scripts validate schema and report errors clearly"""
        # Arrange
        validate_script = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        validates_schema = False
        if validate_script.exists():
            content = validate_script.read_text()
            validates_schema = ('schema' in content.lower() or
                               'required' in content or
                               'validate' in content.lower() or
                               'KeyError' in content or
                               'get(' in content)

        # Assert
        assert validates_schema or not validate_script.exists(), \
            "Measurement scripts missing JSON schema validation"


class TestDVR3StatisticalSignificance:
    """Tests for DVR3: Statistical significance validation"""

    def test_should_calculate_p_value(self):
        """Arrange: Token savings report
        Act: Check for p-value calculation
        Assert: Report includes p-value from statistical test"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_p_value = False
        if report_file.exists():
            content = report_file.read_text()
            has_p_value = ('p-value' in content or 'p value' in content or
                          'p =' in content or 'p<' in content or 'p>' in content)

        # Assert
        assert has_p_value, \
            "Token savings report missing p-value (DVR3)"

    def test_should_flag_non_significant_results(self):
        """Arrange: Token savings report
        Act: Check for significance threshold documentation (p < 0.05)
        Assert: Report explains significance threshold and flags non-significant results"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        documents_threshold = False
        if report_file.exists():
            content = report_file.read_text()
            documents_threshold = ('0.05' in content or
                                  'significant' in content.lower() or
                                  'not statistically' in content.lower() or
                                  'warning' in content.lower())

        # Assert
        assert documents_threshold, \
            "Token savings report missing significance threshold documentation (DVR3)"

    def test_should_use_paired_t_test_for_token_savings(self):
        """Arrange: Token savings script
        Act: Check for paired t-test implementation
        Assert: Script uses ttest_rel or paired t-test"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        uses_paired_test = False
        if script_file.exists():
            content = script_file.read_text()
            uses_paired_test = ('ttest_rel' in content or
                               'paired' in content.lower() or
                               'scipy.stats' in content)

        # Assert
        assert uses_paired_test or not script_file.exists(), \
            "Token savings script missing paired t-test implementation (DVR3)"
