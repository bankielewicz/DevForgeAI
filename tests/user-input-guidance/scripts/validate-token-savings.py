#!/usr/bin/env python3

"""
Token Savings Validation Script

Analyzes token usage between baseline and enhanced test results,
calculating savings percentage and statistical significance.

Usage:
    python3 validate-token-savings.py [--help] [--dry-run]

Flags:
    --help      : Display help message
    --dry-run   : Skip file I/O, show calculated values
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration Constants
BASELINE_RESULTS_PATH = "/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/results/baseline-results.json"
ENHANCED_RESULTS_PATH = "/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/results/enhanced-results.json"
REPORT_OUTPUT_PATH = "/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/results/token-savings-report.md"
T_CRITICAL_95 = 2.262  # t-critical value for n=10 (df=9), 95% confidence


def print_help():
    """Display help message."""
    lines = __doc__.split('\n')[1:11]
    print('\n'.join(lines))


REQUIRED_FIELDS = [
    'story_id', 'fixture_name', 'runs',
    'median_token_usage', 'median_ac_count',
    'median_nfr_present', 'median_iterations', 'incomplete'
]


def validate_runs_array(runs, entry_index):
    """
    Validate runs array structure (DVR2).

    Args:
        runs: Runs array to validate
        entry_index: Index of entry for error message

    Raises:
        ValueError: If runs array invalid
    """
    if not isinstance(runs, list) or len(runs) != 3:
        raise ValueError(
            f"Invalid runs array in entry {entry_index}: expected 3 runs, got {len(runs)}"
        )


def validate_required_fields(result, entry_index, required_fields):
    """
    Validate that result has all required fields.

    Args:
        result: Result dictionary to validate
        entry_index: Index for error message
        required_fields: List of required field names

    Raises:
        ValueError: If field missing
    """
    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Invalid results JSON: missing required field '{field}' in entry {entry_index}"
            )


def load_results(json_file):
    """
    Load results from JSON file and validate schema (DVR2).

    Args:
        json_file: Path to results JSON file

    Returns:
        List of result dictionaries

    Raises:
        ValueError: If schema validation fails
    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    results = data.get('results', [])

    # Validate schema (DVR2)
    for i, result in enumerate(results):
        validate_required_fields(result, i, REQUIRED_FIELDS)
        validate_runs_array(result.get('runs', []), i)

    return results


def calculate_median_tokens(runs):
    """
    Calculate median token usage from 3 runs (BR-003).

    Args:
        runs: List of run dictionaries

    Returns:
        Median token usage value
    """
    tokens = sorted([run['token_usage'] for run in runs])
    return tokens[1]  # Middle value of sorted 3-element list


def paired_t_test(baseline_tokens, enhanced_tokens):
    """
    Perform paired t-test to determine statistical significance (BR-002).

    Args:
        baseline_tokens: List of baseline token counts
        enhanced_tokens: List of enhanced token counts

    Returns:
        Dictionary with t_statistic and p_value
    """
    if len(baseline_tokens) != len(enhanced_tokens):
        raise ValueError("Token lists must have same length")

    n = len(baseline_tokens)
    if n < 2:
        raise ValueError("Need at least 2 samples for t-test")

    # Calculate differences
    diffs = [b - e for b, e in zip(baseline_tokens, enhanced_tokens)]

    # Calculate mean difference
    mean_diff = sum(diffs) / n

    # Calculate standard deviation
    variance = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    std_dev = math.sqrt(variance) if variance > 0 else 0

    # Calculate t-statistic
    if std_dev == 0:
        t_statistic = 0
    else:
        t_statistic = mean_diff / (std_dev / math.sqrt(n))

    # Approximate p-value using t-distribution
    # For n=10, df=9, we use critical values
    # t=1.383 → p=0.10, t=1.833 → p=0.05, t=2.262 → p=0.02
    abs_t = abs(t_statistic)
    if abs_t < 1.383:
        p_value = 0.10
    elif abs_t < 1.833:
        p_value = 0.05
    elif abs_t < 2.262:
        p_value = 0.02
    else:
        p_value = 0.01

    return {
        't_statistic': t_statistic,
        'p_value': p_value,
        'degrees_of_freedom': n - 1,
        'mean_difference': mean_diff,
        'std_dev': std_dev
    }


def calculate_savings_percentage(baseline_avg, enhanced_avg):
    """
    Calculate token savings percentage.

    Args:
        baseline_avg: Average baseline tokens
        enhanced_avg: Average enhanced tokens

    Returns:
        Savings percentage (0-100)
    """
    if baseline_avg == 0:
        return 0
    return ((baseline_avg - enhanced_avg) / baseline_avg) * 100


def calculate_confidence_interval(tokens: List[float], confidence: float = 0.95) -> Dict[str, float]:
    """
    Calculate confidence interval for token usage.

    Args:
        tokens: List of token values
        confidence: Confidence level (default 95%)

    Returns:
        Dictionary with lower and upper bounds
    """
    n = len(tokens)
    if n < 2:
        return {'lower': min(tokens), 'upper': max(tokens)}

    mean = sum(tokens) / n
    variance = sum((t - mean) ** 2 for t in tokens) / (n - 1)
    std_dev = math.sqrt(variance)

    # Use t-critical value for n=10 (df=9), 95% confidence
    margin_error = T_CRITICAL_95 * (std_dev / math.sqrt(n))

    return {
        'mean': mean,
        'lower': mean - margin_error,
        'upper': mean + margin_error,
        'margin_error': margin_error
    }


def generate_report(baseline_avg, enhanced_avg, savings_pct, t_test_result,
                   baseline_ci, enhanced_ci, dry_run=False):
    """
    Generate markdown report for token savings analysis.

    Args:
        baseline_avg: Average baseline tokens
        enhanced_avg: Average enhanced tokens
        savings_pct: Savings percentage
        t_test_result: Paired t-test results
        baseline_ci: Baseline confidence interval
        enhanced_ci: Enhanced confidence interval
        dry_run: If True, don't write file

    Returns:
        Markdown report content
    """
    p_value = t_test_result['p_value']
    significant = "Yes (p < 0.05)" if p_value < 0.05 else "No (p >= 0.05)"

    report = f"""# Token Savings Analysis Report

## Executive Summary

This report analyzes token usage efficiency improvements from applying User Input Guidance
to story creation workflow across 10 test fixtures (3 Simple, 4 Medium, 3 Complex).

## Key Findings

- **Baseline Average Tokens**: {baseline_avg:.1f}
- **Enhanced Average Tokens**: {enhanced_avg:.1f}
- **Token Savings**: {savings_pct:.2f}%
- **Statistical Significance**: {significant}
- **Sample Size**: n=10 fixture pairs
- **Confidence Level**: 95%

## Detailed Metrics

### Baseline Token Usage
- Mean: {baseline_ci['mean']:.1f}
- 95% CI: [{baseline_ci['lower']:.1f}, {baseline_ci['upper']:.1f}]
- Margin of Error: ±{baseline_ci['margin_error']:.1f}

### Enhanced Token Usage
- Mean: {enhanced_ci['mean']:.1f}
- 95% CI: [{enhanced_ci['lower']:.1f}, {enhanced_ci['upper']:.1f}]
- Margin of Error: ±{enhanced_ci['margin_error']:.1f}

## Statistical Analysis

### Paired T-Test Results
- Test Type: Paired t-test (matched samples)
- Null Hypothesis: No difference between baseline and enhanced token usage
- Alternative Hypothesis: Enhanced uses fewer tokens than baseline
- t-statistic: {t_test_result['t_statistic']:.4f}
- p-value: {p_value:.4f}
- Degrees of Freedom: {t_test_result['degrees_of_freedom']}
- Mean Difference: {t_test_result['mean_difference']:.1f} tokens
- Standard Deviation (differences): {t_test_result['std_dev']:.1f}

### Interpretation
"""

    if p_value < 0.05:
        report += f"""
The p-value of {p_value:.4f} is less than 0.05, indicating the token savings is
**statistically significant** at the 95% confidence level. This means we can reject
the null hypothesis with >95% confidence that User Input Guidance reduces token usage.

**Conclusion**: The {savings_pct:.2f}% reduction in tokens is both meaningful and
statistically significant.
"""
    else:
        report += f"""
⚠️  The p-value of {p_value:.4f} is ≥0.05, indicating the token savings is
**NOT statistically significant** at the 95% confidence level. With only n=10 samples,
the observed {savings_pct:.2f}% difference could be due to random variation.

**Conclusion**: While a {savings_pct:.2f}% reduction is observed, it cannot be
confirmed as a real effect with sufficient confidence. Recommend larger sample size
(n=30+) for definitive validation.
"""

    report += """

## Limitations

- **Sample Size**: n=10 fixture pairs may be insufficient for robust statistical inference
- **Fixture Selection**: Fixtures stratified by complexity but may not represent production variety
- **Token Counting**: Uses synthetic token estimates; real Claude API usage may vary
- **Temporal Factors**: Single test run; does not account for model updates or prompt variations
- **Generalization**: Results specific to /create-story workflow; other workflows may differ

## Recommendations

1. If p-value < 0.05: Deploy guidance in production with monitoring of actual token usage
2. If p-value >= 0.05: Expand test with additional fixtures (n=30+) before making decision
3. Monitor actual Claude API token usage post-deployment to validate estimates
4. Compare token savings across different complexity levels (Simple/Medium/Complex)
5. Test guidance system with diverse feature categories (Auth, Payment, Reporting, etc.)

---
Generated: {json.dumps({"timestamp": None})[:0]}
Test Type: Baseline vs Enhanced Comparison
Sample Size: 10 fixture pairs
"""

    return report


def main():
    """Main execution."""
    # Parse command line arguments
    dry_run = '--dry-run' in sys.argv
    help_flag = '--help' in sys.argv or '-h' in sys.argv

    if help_flag:
        print_help()
        return 0

    try:
        # File paths
        baseline_file = Path(BASELINE_RESULTS_PATH)
        enhanced_file = Path(ENHANCED_RESULTS_PATH)

        # Verify files exist
        if not baseline_file.exists():
            print(f"ERROR: Baseline results not found: {baseline_file}")
            print("Run: test-story-creation-without-guidance.sh first")
            return 1

        if not enhanced_file.exists():
            print(f"ERROR: Enhanced results not found: {enhanced_file}")
            print("Run: test-story-creation-with-guidance.sh first")
            return 1

        print("Loading baseline results...")
        baseline_results = load_results(baseline_file)

        print("Loading enhanced results...")
        enhanced_results = load_results(enhanced_file)

        if len(baseline_results) != len(enhanced_results):
            raise ValueError("Baseline and enhanced results have different counts")

        # Extract token usage with median calculation (BR-003)
        baseline_tokens = []
        enhanced_tokens = []

        for baseline, enhanced in zip(baseline_results, enhanced_results):
            baseline_median = calculate_median_tokens(baseline['runs'])
            enhanced_median = calculate_median_tokens(enhanced['runs'])

            baseline_tokens.append(baseline_median)
            enhanced_tokens.append(enhanced_median)

        # Calculate statistics
        baseline_avg = sum(baseline_tokens) / len(baseline_tokens)
        enhanced_avg = sum(enhanced_tokens) / len(enhanced_tokens)
        savings_pct = calculate_savings_percentage(baseline_avg, enhanced_avg)

        # Perform paired t-test (BR-002)
        t_test_result = paired_t_test(baseline_tokens, enhanced_tokens)

        # Calculate confidence intervals
        baseline_ci = calculate_confidence_interval(baseline_tokens)
        enhanced_ci = calculate_confidence_interval(enhanced_tokens)

        # Print results to console
        print("\n" + "=" * 60)
        print("TOKEN SAVINGS ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Baseline Average: {baseline_avg:.1f} tokens")
        print(f"Enhanced Average: {enhanced_avg:.1f} tokens")
        print(f"Token Savings: {savings_pct:.2f}%")
        print(f"t-statistic: {t_test_result['t_statistic']:.4f}")
        print(f"p-value: {t_test_result['p_value']:.4f}")

        if t_test_result['p_value'] >= 0.05:
            print("\n⚠️  NOT STATISTICALLY SIGNIFICANT (p >= 0.05)")
        else:
            print("\n✓ STATISTICALLY SIGNIFICANT (p < 0.05)")
        print("=" * 60 + "\n")

        if not dry_run:
            # Generate report
            report = generate_report(
                baseline_avg, enhanced_avg, savings_pct,
                t_test_result, baseline_ci, enhanced_ci, dry_run=False
            )

            # Write report
            report_file = Path(REPORT_OUTPUT_PATH)
            report_file.parent.mkdir(parents=True, exist_ok=True)
            report_file.write_text(report)

            print(f"✓ Report written to: {report_file}")

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
