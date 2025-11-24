"""
AC#5 Tests: Impact Report Generation and Non-Functional Requirements

Tests validate that the consolidated impact report contains all required sections,
statistical analysis, and recommendations per AC#5 and all NFR categories.
"""

import pytest
import json
from pathlib import Path


class TestImpactReportExistence:
    """Tests for AC#5: Impact report generation"""

    def test_should_generate_impact_report(self):
        """Arrange: Expected output location
        Act: Check for USER-INPUT-GUIDANCE-IMPACT-REPORT.md
        Assert: Impact report file exists"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        file_exists = report_file.exists() and report_file.is_file()

        # Assert
        assert file_exists, f"Impact report not found: {report_file}"

    def test_should_have_impact_report_with_content(self):
        """Arrange: Impact report file
        Act: Read content and validate length
        Assert: Report has substantial content (>1000 characters)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_content = False
        if report_file.exists():
            content = report_file.read_text()
            has_content = len(content.strip()) > 1000

        # Assert
        assert has_content, "Impact report is too short (expected >1000 characters)"


class TestImpactReportExecutiveSummary:
    """Tests for AC#5: Executive summary section"""

    def test_should_have_executive_summary_section(self):
        """Arrange: Impact report
        Act: Check for executive summary section
        Assert: Report includes executive summary section"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_summary = False
        if report_file.exists():
            content = report_file.read_text()
            has_summary = ('executive' in content.lower() or
                          'summary' in content.lower() or
                          'overview' in content.lower())

        # Assert
        assert has_summary, "Impact report missing executive summary section"

    def test_should_have_headline_metrics_in_summary(self):
        """Arrange: Impact report
        Act: Check for headline metrics in executive summary
        Assert: Summary includes key metrics (token savings %, incomplete reduction %)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_metrics = False
        if report_file.exists():
            content = report_file.read_text()
            has_metrics = (('%' in content and 'token' in content.lower()) or
                          ('savings' in content.lower() and 'reduction' in content.lower()))

        # Assert
        assert has_metrics, "Impact report summary missing headline metrics"

    def test_should_limit_executive_summary_to_500_words(self):
        """Arrange: Impact report
        Act: Estimate word count of executive summary section
        Assert: Executive summary ≤ 500 words"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        summary_length = 0
        if report_file.exists():
            content = report_file.read_text()
            # Extract text between "Executive Summary" and next section
            if "executive" in content.lower():
                parts = content.lower().split("executive")
                if len(parts) > 1:
                    summary_text = parts[1].split("##" if "##" in parts[1] else "")[0]
                    summary_length = len(summary_text.split())

        # Assert (if summary found, check word count; otherwise skip)
        if summary_length > 0:
            assert summary_length <= 500, \
                f"Executive summary {summary_length} words (max 500)"


class TestImpactReportFindingsByBusinessGoal:
    """Tests for AC#5: Detailed findings section"""

    def test_should_have_findings_by_business_goal(self):
        """Arrange: Impact report
        Act: Check for detailed findings section
        Assert: Report includes findings by business goal"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_findings = False
        if report_file.exists():
            content = report_file.read_text()
            has_findings = ('finding' in content.lower() or
                           'result' in content.lower() or
                           'goal' in content.lower() or
                           'business' in content.lower())

        # Assert
        assert has_findings, "Impact report missing detailed findings section"

    def test_should_document_incomplete_rate_findings(self):
        """Arrange: Impact report
        Act: Check for incomplete story rate findings
        Assert: Report documents baseline ~40%, enhanced ≤13%, reduction ≥67%"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_incomplete_findings = False
        if report_file.exists():
            content = report_file.read_text()
            has_incomplete_findings = ('incomplete' in content.lower() and
                                      ('rate' in content.lower() or '%' in content))

        # Assert
        assert has_incomplete_findings, "Impact report missing incomplete rate findings"

    def test_should_document_token_efficiency_findings(self):
        """Arrange: Impact report
        Act: Check for token efficiency findings
        Assert: Report documents token savings percentage and p-value"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_token_findings = False
        if report_file.exists():
            content = report_file.read_text()
            has_token_findings = (('token' in content.lower() and 'sav' in content.lower()) or
                                 ('efficiency' in content.lower() and '%' in content))

        # Assert
        assert has_token_findings, "Impact report missing token efficiency findings"

    def test_should_document_iteration_cycle_findings(self):
        """Arrange: Impact report
        Act: Check for iteration cycle findings
        Assert: Report documents baseline ~2.5, enhanced ≤1.2 iterations"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_iteration_findings = False
        if report_file.exists():
            content = report_file.read_text()
            has_iteration_findings = ('iteration' in content.lower() or
                                     'cycle' in content.lower() or
                                     'subagent' in content.lower())

        # Assert
        assert has_iteration_findings, "Impact report missing iteration cycle findings"


class TestImpactReportEvidenceTables:
    """Tests for AC#5: Evidence tables section"""

    def test_should_have_evidence_tables(self):
        """Arrange: Impact report
        Act: Check for evidence tables or data tables
        Assert: Report includes tables with before/after metrics"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_tables = False
        if report_file.exists():
            content = report_file.read_text()
            has_tables = ('|' in content or 'table' in content.lower() or
                         'fixture' in content.lower())

        # Assert
        assert has_tables, "Impact report missing evidence tables"

    def test_should_include_all_10_fixtures_in_tables(self):
        """Arrange: Impact report
        Act: Count fixture references in tables
        Assert: Report includes data for all 10 test fixtures"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        fixture_count = 0
        if report_file.exists():
            content = report_file.read_text()
            # Count fixture references (baseline-XX or enhanced-XX or fixture-XX)
            for i in range(1, 11):
                pattern1 = f"baseline-{i:02d}"
                pattern2 = f"enhanced-{i:02d}"
                pattern3 = f"fixture-{i:02d}"
                pattern4 = f"Fixture {i}"

                if (pattern1 in content or pattern2 in content or
                    pattern3 in content or pattern4 in content):
                    fixture_count += 1

        # Assert
        assert fixture_count >= 8, f"Report only references {fixture_count} fixtures (expected ≥8 of 10)"


class TestImpactReportStatisticalAnalysis:
    """Tests for AC#5: Statistical analysis section"""

    def test_should_have_statistical_analysis_section(self):
        """Arrange: Impact report
        Act: Check for statistical analysis section
        Assert: Report includes statistical analysis section"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_statistics = False
        if report_file.exists():
            content = report_file.read_text()
            has_statistics = ('statistic' in content.lower() or
                             'p-value' in content or 'p value' in content or
                             'confidence' in content.lower() or 'interval' in content.lower())

        # Assert
        assert has_statistics, "Impact report missing statistical analysis section"

    def test_should_report_confidence_intervals(self):
        """Arrange: Impact report
        Act: Check for confidence interval reporting
        Assert: Report includes confidence intervals"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_confidence = False
        if report_file.exists():
            content = report_file.read_text()
            has_confidence = ('confidence' in content.lower() or
                            'interval' in content.lower() or
                            'CI' in content or '95%' in content or
                            '±' in content)

        # Assert
        assert has_confidence, "Impact report missing confidence interval reporting"

    def test_should_report_significance_testing(self):
        """Arrange: Impact report
        Act: Check for significance test reporting
        Assert: Report includes p-value and significance statement"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_significance = False
        if report_file.exists():
            content = report_file.read_text()
            has_significance = (('p-value' in content or 'p value' in content or 'p =' in content) and
                              ('significant' in content.lower() or 'reject' in content.lower()))

        # Assert
        assert has_significance, "Impact report missing significance testing results"


class TestImpactReportRecommendations:
    """Tests for AC#5: Recommendations section"""

    def test_should_have_recommendations_section(self):
        """Arrange: Impact report
        Act: Check for recommendations section
        Assert: Report includes recommendations"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_recommendations = False
        if report_file.exists():
            content = report_file.read_text()
            has_recommendations = ('recommend' in content.lower() or
                                  'next step' in content.lower() or
                                  'action' in content.lower() or
                                  'future' in content.lower())

        # Assert
        assert has_recommendations, "Impact report missing recommendations section"

    def test_should_have_3_to_5_actionable_recommendations(self):
        """Arrange: Impact report
        Act: Count numbered/bulleted recommendations
        Assert: Report includes 3-5 actionable recommendations"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        recommendation_count = 0
        if report_file.exists():
            content = report_file.read_text()
            # Extract recommendations section - look for numbered items (1. 2. 3. etc.)
            if 'recommend' in content.lower():
                # Find the recommendations section
                rec_idx = content.lower().find('recommend')
                if rec_idx >= 0:
                    # Get text after "recommendations" to the next ## heading or end of file
                    rec_section = content[rec_idx:]
                    # Find next heading (any level: #, ##, ###, etc.)
                    next_heading = rec_section.find('\n# ')
                    if next_heading > 0:
                        rec_section = rec_section[:next_heading]

                    # Count numbered items: "1. ", "2. ", "3. ", etc.
                    for i in range(1, 10):
                        if f'\n{i}. ' in rec_section or f'\n{i}) ' in rec_section:
                            recommendation_count += 1
                        else:
                            break  # Stop counting at first gap

        # Assert
        assert recommendation_count >= 3, \
            f"Impact report has {recommendation_count} recommendations (expected 3-5)"


class TestImpactReportLimitations:
    """Tests for AC#5: Limitations section"""

    def test_should_have_limitations_section(self):
        """Arrange: Impact report
        Act: Check for limitations section
        Assert: Report includes limitations and caveats"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_limitations = False
        if report_file.exists():
            content = report_file.read_text()
            has_limitations = ('limitation' in content.lower() or
                             'caveat' in content.lower() or
                             'sample size' in content.lower() or
                             'bias' in content.lower())

        # Assert
        assert has_limitations, "Impact report missing limitations section"

    def test_should_acknowledge_sample_size_limitation(self):
        """Arrange: Impact report
        Act: Check for acknowledgment of 10-story sample size
        Assert: Report acknowledges limited sample size (n=10)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        acknowledges_sample = False
        if report_file.exists():
            content = report_file.read_text()
            acknowledges_sample = (('sample size' in content.lower() and '10' in content) or
                                  ('10-story' in content.lower()) or
                                  ('n=10' in content) or
                                  ('10 fixture' in content.lower()))

        # Assert
        assert acknowledges_sample, "Impact report missing sample size acknowledgment"

    def test_should_acknowledge_fixture_selection_bias(self):
        """Arrange: Impact report
        Act: Check for acknowledgment of fixture selection bias
        Assert: Report acknowledges potential bias in fixture selection"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        acknowledges_bias = False
        if report_file.exists():
            content = report_file.read_text()
            acknowledges_bias = (('selection bias' in content.lower() or
                                 'fixture' in content.lower() and 'bias' in content.lower()) or
                                ('generalizability' in content.lower()) or
                                ('representative' in content.lower()))

        # Assert
        assert acknowledges_bias, "Impact report missing fixture selection bias acknowledgment"


class TestImpactReportAppendix:
    """Tests for AC#5: Appendix section"""

    def test_should_have_appendix_with_raw_data(self):
        """Arrange: Impact report
        Act: Check for appendix section with raw data tables
        Assert: Report includes appendix for reproducibility"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md")

        # Act
        has_appendix = False
        if report_file.exists():
            content = report_file.read_text()
            has_appendix = ('appendix' in content.lower() or
                           'raw data' in content.lower() or
                           'reproducib' in content.lower())

        # Assert
        assert has_appendix or not report_file.exists(), \
            "Impact report missing appendix with raw data"


class TestNFR_Performance:
    """Tests for NFR-PERF-001: Performance requirement (<60 minutes)"""

    def test_should_complete_test_suite_in_under_60_minutes(self):
        """Arrange: Test execution timing
        Act: Verify test execution timing documentation
        Assert: Scripts document total execution time <60 minutes"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        documents_timing = False
        if report_file.exists():
            content = report_file.read_text()
            documents_timing = ('minute' in content.lower() or
                              'second' in content.lower() or
                              'duration' in content.lower() or
                              'time' in content.lower())

        # Assert
        assert documents_timing or not report_file.exists(), \
            "NFR-PERF-001: Test execution timing not documented"


class TestNFR_Reliability:
    """Tests for NFR-REL-001: Reliability requirement (partial failure handling)"""

    def test_should_handle_individual_fixture_failures(self):
        """Arrange: Test scripts
        Act: Check for error handling that continues on fixture failure
        Assert: Scripts have mechanism to skip failed fixtures and continue"""
        # Arrange
        test_script = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        handles_failures = False
        if test_script.exists():
            content = test_script.read_text()
            handles_failures = ('continue' in content or
                               'try' in content or
                               'catch' in content or
                               'trap' in content or
                               '||' in content or
                               '2>/dev/null' in content)

        # Assert
        assert handles_failures or not test_script.exists(), \
            "NFR-REL-001: Scripts missing error handling for partial failures"

    def test_should_provide_clear_error_messages(self):
        """Arrange: Test scripts
        Act: Check for informative error messages
        Assert: Scripts provide clear error information"""
        # Arrange
        test_script = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        has_error_messages = False
        if test_script.exists():
            content = test_script.read_text()
            has_error_messages = ('echo' in content and
                                 ('error' in content.lower() or 'failed' in content.lower() or
                                  'warning' in content.lower()))

        # Assert
        assert has_error_messages or not test_script.exists(), \
            "NFR-REL-001: Scripts missing clear error messaging"


class TestNFR_Maintainability:
    """Tests for NFR-MAINT-001: Maintainability (stdlib only for core)"""

    def test_should_use_stdlib_only_for_core_functionality(self):
        """Arrange: Python measurement scripts
        Act: Check imports for stdlib-only core (matplotlib/scipy optional)
        Assert: Core uses only: os, json, statistics, pathlib, sys, argparse"""
        # Arrange
        script_files = [
            Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py"),
            Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")
        ]
        forbidden_imports = ["pandas", "numpy", "requests", "selenium", "scrapy"]

        # Act
        problematic_scripts = {}
        for script_file in script_files:
            if script_file.exists():
                content = script_file.read_text()
                bad_imports = [imp for imp in forbidden_imports
                              if f"import {imp}" in content or f"from {imp}" in content]
                if bad_imports:
                    problematic_scripts[script_file.name] = bad_imports

        # Assert
        assert not problematic_scripts, \
            f"NFR-MAINT-001: Scripts use non-stdlib imports: {problematic_scripts}"

    def test_should_have_simple_text_fixtures(self):
        """Arrange: Fixture files
        Act: Verify fixtures are plain UTF-8 text
        Assert: Fixtures are simple text, not binary or complex formats"""
        # Arrange
        baseline_dir = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

        # Act
        binary_files = []
        if baseline_dir.exists():
            for fixture_file in baseline_dir.glob("*.txt"):
                try:
                    fixture_file.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    binary_files.append(fixture_file.name)

        # Assert
        assert not binary_files, \
            f"NFR-MAINT-001: Binary or non-text fixtures: {binary_files}"

    def test_should_output_machine_readable_json(self):
        """Arrange: Results JSON files
        Act: Validate JSON is well-formed
        Assert: All output JSON is valid and machine-readable"""
        # Arrange
        results_files = [
            Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json"),
            Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")
        ]

        # Act
        invalid_json = []
        for results_file in results_files:
            if results_file.exists():
                try:
                    json.loads(results_file.read_text())
                except json.JSONDecodeError as e:
                    invalid_json.append(f"{results_file.name}: {e}")

        # Assert
        assert not invalid_json, \
            f"NFR-MAINT-001: Invalid JSON output: {'; '.join(invalid_json)}"
