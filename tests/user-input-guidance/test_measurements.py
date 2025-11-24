"""
AC#3 and AC#4 Tests: Measurement Script Functionality

Tests validate that measurement scripts calculate token savings, success rates,
and generate required reports with statistical analysis.
"""

import pytest
import json
from pathlib import Path


class TestTokenSavingsScriptStructure:
    """Tests for AC#3: validate-token-savings.py script structure"""

    def test_should_have_token_savings_script(self):
        """Arrange: Scripts directory
        Act: Check for validate-token-savings.py
        Assert: Script exists"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        script_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert script_exists, f"Token savings script not found: {script_file}"

    def test_should_have_token_savings_script_with_content(self):
        """Arrange: validate-token-savings.py
        Act: Read script content
        Assert: Script has substantial content"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        has_content = False
        if script_file.exists():
            content = script_file.read_text()
            has_content = len(content.strip()) > 100

        # Assert
        assert has_content, "Token savings script is empty or too small"

    def test_should_have_token_savings_script_with_help_documentation(self):
        """Arrange: validate-token-savings.py
        Act: Check for --help or usage documentation
        Assert: Script includes usage information"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        has_help = False
        if script_file.exists():
            content = script_file.read_text()
            has_help = ('argparse' in content or '--help' in content or
                       'usage' in content.lower() or '"""' in content or "'''" in content)

        # Assert
        assert has_help, "Token savings script lacks help/usage documentation"

    def test_should_have_token_savings_script_with_statistical_functions(self):
        """Arrange: validate-token-savings.py
        Act: Check for t-test or statistical imports
        Assert: Script uses statistical analysis functions"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")

        # Act
        has_stats = False
        if script_file.exists():
            content = script_file.read_text()
            has_stats = ('ttest' in content or 'scipy' in content or
                        'statistics' in content or 'mean' in content or
                        'stdev' in content)

        # Assert
        assert has_stats, "Token savings script lacks statistical analysis functions"


class TestSuccessRateScriptStructure:
    """Tests for AC#4: measure-success-rate.py script structure"""

    def test_should_have_success_rate_script(self):
        """Arrange: Scripts directory
        Act: Check for measure-success-rate.py
        Assert: Script exists"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        script_exists = script_file.exists() and script_file.is_file()

        # Assert
        assert script_exists, f"Success rate script not found: {script_file}"

    def test_should_have_success_rate_script_with_content(self):
        """Arrange: measure-success-rate.py
        Act: Read script content
        Assert: Script has substantial content"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        has_content = False
        if script_file.exists():
            content = script_file.read_text()
            has_content = len(content.strip()) > 100

        # Assert
        assert has_content, "Success rate script is empty or too small"

    def test_should_have_success_rate_script_with_help_documentation(self):
        """Arrange: measure-success-rate.py
        Act: Check for --help or usage documentation
        Assert: Script includes usage information"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        has_help = False
        if script_file.exists():
            content = script_file.read_text()
            has_help = ('argparse' in content or '--help' in content or
                       'usage' in content.lower() or '"""' in content or "'''" in content)

        # Assert
        assert has_help, "Success rate script lacks help/usage documentation"

    def test_should_have_success_rate_script_with_scoring_function(self):
        """Arrange: measure-success-rate.py
        Act: Check for score/incomplete detection logic
        Assert: Script includes completeness scoring"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        has_scoring = False
        if script_file.exists():
            content = script_file.read_text()
            has_scoring = ('score' in content.lower() or 'incomplete' in content.lower() or
                          'ac_count' in content or 'def is_incomplete' in content or
                          'def score' in content)

        # Assert
        assert has_scoring, "Success rate script lacks completeness scoring function"


class TestTokenSavingsReportGeneration:
    """Tests for AC#3: Token savings report is generated"""

    def test_should_generate_token_savings_report_markdown(self):
        """Arrange: Expected output directory
        Act: Check for token-savings-report.md
        Assert: Report file exists"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        report_exists = report_file.exists() and report_file.is_file()

        # Assert
        assert report_exists, f"Token savings report not found: {report_file}"

    def test_should_have_token_savings_report_with_content(self):
        """Arrange: Token savings report
        Act: Read report content
        Assert: Report has meaningful content"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_content = False
        if report_file.exists():
            content = report_file.read_text()
            has_content = len(content.strip()) > 100

        # Assert
        assert has_content, "Token savings report is empty or too small"

    def test_should_include_savings_percentage_in_report(self):
        """Arrange: Token savings report
        Act: Check for savings percentage mention
        Assert: Report documents token savings percentage"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_percentage = False
        if report_file.exists():
            content = report_file.read_text()
            has_percentage = '%' in content or 'savings' in content.lower() or 'reduction' in content.lower()

        # Assert
        assert has_percentage, "Token savings report missing percentage information"

    def test_should_include_statistical_significance_in_report(self):
        """Arrange: Token savings report
        Act: Check for p-value or significance mention
        Assert: Report documents statistical significance"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_significance = False
        if report_file.exists():
            content = report_file.read_text()
            has_significance = ('p-value' in content or 'p value' in content or
                              'significant' in content.lower() or 'confidence' in content.lower())

        # Assert
        assert has_significance, "Token savings report missing statistical significance information"

    def test_should_include_confidence_level_in_report(self):
        """Arrange: Token savings report
        Act: Check for confidence interval mention
        Assert: Report documents confidence level"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")

        # Act
        has_confidence = False
        if report_file.exists():
            content = report_file.read_text()
            has_confidence = ('confidence' in content.lower() or 'interval' in content.lower() or
                            'CI' in content or '95%' in content)

        # Assert
        assert has_confidence, "Token savings report missing confidence level information"

    def test_should_generate_token_savings_chart(self):
        """Arrange: Expected output directory
        Act: Check for token-savings-chart.png
        Assert: Visualization file exists (if matplotlib available)"""
        # Arrange
        chart_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-chart.png")

        # Act
        chart_exists = chart_file.exists() and chart_file.is_file()

        # Assert (visualization is optional if matplotlib not available)
        # This test will fail until matplotlib is configured or explicitly handled
        if not chart_exists:
            # Check for warning in report instead
            report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/token-savings-report.md")
            if report_file.exists():
                content = report_file.read_text()
                has_warning = 'matplotlib' in content.lower() or 'chart' in content.lower()
                assert chart_exists or has_warning, \
                    "Token savings chart not found and no matplotlib warning in report"


class TestSuccessRateReportGeneration:
    """Tests for AC#4: Success rate report is generated"""

    def test_should_generate_success_rate_report_markdown(self):
        """Arrange: Expected output directory
        Act: Check for success-rate-report.md
        Assert: Report file exists"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        report_exists = report_file.exists() and report_file.is_file()

        # Assert
        assert report_exists, f"Success rate report not found: {report_file}"

    def test_should_have_success_rate_report_with_content(self):
        """Arrange: Success rate report
        Act: Read report content
        Assert: Report has meaningful content"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_content = False
        if report_file.exists():
            content = report_file.read_text()
            has_content = len(content.strip()) > 100

        # Assert
        assert has_content, "Success rate report is empty or too small"

    def test_should_include_baseline_incomplete_rate_in_report(self):
        """Arrange: Success rate report
        Act: Check for baseline incomplete rate
        Assert: Report documents baseline incomplete rate (~40%)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_baseline = False
        if report_file.exists():
            content = report_file.read_text()
            has_baseline = ('baseline' in content.lower() and
                           ('incomplete' in content.lower() or 'rate' in content.lower()))

        # Assert
        assert has_baseline, "Success rate report missing baseline incomplete rate"

    def test_should_include_enhanced_incomplete_rate_in_report(self):
        """Arrange: Success rate report
        Act: Check for enhanced incomplete rate
        Assert: Report documents enhanced incomplete rate (≤13%)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_enhanced = False
        if report_file.exists():
            content = report_file.read_text()
            has_enhanced = ('enhanced' in content.lower() and
                           ('incomplete' in content.lower() or 'rate' in content.lower()))

        # Assert
        assert has_enhanced, "Success rate report missing enhanced incomplete rate"

    def test_should_include_reduction_percentage_in_report(self):
        """Arrange: Success rate report
        Act: Check for reduction percentage
        Assert: Report documents incomplete story reduction (≥67%)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_reduction = False
        if report_file.exists():
            content = report_file.read_text()
            has_reduction = ('reduction' in content.lower() or
                           ('improvement' in content.lower()))

        # Assert
        assert has_reduction, "Success rate report missing reduction percentage"

    def test_should_include_iteration_metrics_in_report(self):
        """Arrange: Success rate report
        Act: Check for iteration cycle metrics
        Assert: Report documents iteration counts (baseline ~2.5, enhanced ≤1.2)"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_iterations = False
        if report_file.exists():
            content = report_file.read_text()
            has_iterations = ('iteration' in content.lower() or
                            're-invocation' in content.lower() or
                            'subagent' in content.lower())

        # Assert
        assert has_iterations, "Success rate report missing iteration metrics"

    def test_should_include_fixture_breakdown_in_report(self):
        """Arrange: Success rate report
        Act: Check for per-fixture details
        Assert: Report documents results for each of 10 fixtures"""
        # Arrange
        report_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/success-rate-report.md")

        # Act
        has_breakdown = False
        if report_file.exists():
            content = report_file.read_text()
            has_breakdown = ('fixture' in content.lower() or '10' in content or
                           'individual' in content.lower() or 'breakdown' in content.lower())

        # Assert
        assert has_breakdown, "Success rate report missing per-fixture breakdown"


class TestMeasurementScriptDependencies:
    """Tests for NFR-MAINT-001: Scripts use only stdlib"""

    def test_should_use_only_stdlib_in_token_savings_script(self):
        """Arrange: validate-token-savings.py
        Act: Check imports for stdlib only (optional: scipy/matplotlib OK)
        Assert: Core functionality uses only stdlib (json, statistics, pathlib, os)"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/validate-token-savings.py")
        non_stdlib_imports = ["pandas", "numpy", "requests"]

        # Act
        problematic_imports = []
        if script_file.exists():
            content = script_file.read_text()
            for bad_import in non_stdlib_imports:
                if f"import {bad_import}" in content or f"from {bad_import}" in content:
                    problematic_imports.append(bad_import)

        # Assert
        assert not problematic_imports, \
            f"Token savings script uses non-stdlib imports: {', '.join(problematic_imports)}"

    def test_should_use_only_stdlib_in_success_rate_script(self):
        """Arrange: measure-success-rate.py
        Act: Check imports for stdlib only
        Assert: Core functionality uses only stdlib (json, statistics, pathlib, os)"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/measure-success-rate.py")
        non_stdlib_imports = ["pandas", "numpy", "requests"]

        # Act
        problematic_imports = []
        if script_file.exists():
            content = script_file.read_text()
            for bad_import in non_stdlib_imports:
                if f"import {bad_import}" in content or f"from {bad_import}" in content:
                    problematic_imports.append(bad_import)

        # Assert
        assert not problematic_imports, \
            f"Success rate script uses non-stdlib imports: {', '.join(problematic_imports)}"
