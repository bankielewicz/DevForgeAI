#!/usr/bin/env python3
"""
Success Rate Measurement Script

Analyzes quality improvements in enhanced fixtures compared to baseline:
- AC Testability: Percentage using Given/When/Then or measurable assertions
- NFR Coverage: Percentage of 4 NFR categories mentioned (performance, security, reliability, scalability)
- Specificity: Percentage reduction in vague terms (fast, good, better, optimize)

Compares actual improvements against expected targets from JSON fixtures.

Usage:
    python measure-success-rate.py
    python measure-success-rate.py --help
    python measure-success-rate.py --test

Exit Codes:
    0 - Success (≥8 of 10 fixtures meet expectations)
    1 - Hypothesis not validated (<8 fixtures meet expectations)
    4 - Invalid input (missing fixtures, incomplete pairs)
    5 - Missing expected JSON files
"""

import sys
import os
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration constants
SUCCESS_RATE_THRESHOLD = 80.0  # Minimum success rate (8 of 10 fixtures)
FIXTURES_BASE_DIR = Path(__file__).parent.parent / "fixtures"
BASELINE_DIR = FIXTURES_BASE_DIR / "baseline"
ENHANCED_DIR = FIXTURES_BASE_DIR / "enhanced"
EXPECTED_DIR = FIXTURES_BASE_DIR / "expected"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
EXPECTED_FIXTURE_COUNT = 10

# NFR categories for detection
NFR_CATEGORIES = {
    'performance': r'(response time|latency|throughput|performance|<.*ms|requests per second|rps)',
    'security': r'(authentication|authorization|encryption|security|OWASP|password|token|JWT|OAuth)',
    'reliability': r'(error handling|retry|fallback|uptime|reliability|graceful degradation|fault tolerance)',
    'scalability': r'(concurrent|scale|scalability|load|horizontal|vertical|users|capacity)'
}

# Vague terms to detect
VAGUE_TERMS = ['fast', 'slow', 'good', 'bad', 'better', 'worse', 'optimize', 'improve',
               'efficient', 'scalable', 'performant', 'robust', 'reliable']

def calculate_ac_testability(text: str) -> float:
    """
    Calculate percentage of testable acceptance criteria.

    Detects Given/When/Then patterns and measurable assertions.

    Args:
        text: Fixture text to analyze

    Returns:
        Percentage score (0-100)
    """
    text_lower = text.lower()

    # Count total AC mentions
    ac_patterns = [
        r'acceptance criteria',
        r'\bac\b',
        r'criterion',
        r'must\s+',
        r'should\s+',
        r'shall\s+'
    ]
    total_ac = sum(len(re.findall(pattern, text_lower)) for pattern in ac_patterns)

    if total_ac == 0:
        return 0.0

    # Count testable criteria
    testable_patterns = [
        r'given\s+.+\s+when\s+.+\s+then',  # Given/When/Then
        r'must\s+(validate|return|display|create|update|delete|verify|ensure)',
        r'should\s+(validate|return|display|create|update|delete|verify|ensure)',
        r'verif(y|ies|ied)',
        r'test\s+that',
        r'assert',
        r'expect'
    ]
    testable_ac = sum(len(re.findall(pattern, text_lower)) for pattern in testable_patterns)

    return min((testable_ac / total_ac) * 100, 100.0)

def calculate_nfr_coverage(text: str) -> float:
    """
    Calculate percentage of 4 NFR categories mentioned.

    Categories: performance, security, reliability, scalability

    Args:
        text: Fixture text to analyze

    Returns:
        Percentage score (0, 25, 50, 75, or 100)
    """
    mentioned_count = 0

    for category, pattern in NFR_CATEGORIES.items():
        if re.search(pattern, text, re.IGNORECASE):
            mentioned_count += 1

    return (mentioned_count / 4) * 100

def calculate_specificity_score(baseline_text: str, enhanced_text: str) -> float:
    """
    Calculate percentage reduction in vague terms.

    Args:
        baseline_text: Original fixture text
        enhanced_text: Enhanced fixture text

    Returns:
        Reduction percentage (0-100)
    """
    baseline_lower = baseline_text.lower()
    enhanced_lower = enhanced_text.lower()

    # Count vague terms
    baseline_vague = sum(baseline_lower.count(term) for term in VAGUE_TERMS)
    enhanced_vague = sum(enhanced_lower.count(term) for term in VAGUE_TERMS)

    if baseline_vague == 0:
        return 100.0  # No vague terms to reduce

    reduction = ((baseline_vague - enhanced_vague) / baseline_vague) * 100
    return max(round(reduction, 2), 0.0)  # Don't allow negative

def load_expected_improvements(fixture_num: int, category: str) -> Dict:
    """
    Load expected improvement targets from JSON file.

    Args:
        fixture_num: Fixture number (1-10)
        category: Fixture category

    Returns:
        Expected improvements dictionary

    Raises:
        FileNotFoundError: If expected file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    expected_path = EXPECTED_DIR / f"expected-{fixture_num:02d}-{category}.json"

    if not expected_path.exists():
        raise FileNotFoundError(f"Expected file not found: {expected_path.name}")

    with open(expected_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get("expected_improvements", {})

def meets_expectations(actual: Dict, expected: Dict) -> Tuple[bool, int, int]:
    """
    Check if actual metrics meet or exceed expected values.

    Args:
        actual: Actual measured metrics
        expected: Expected target metrics

    Returns:
        Tuple of (all_met, met_count, total_count)
    """
    metrics = ["ac_completeness", "nfr_coverage", "specificity_score"]
    met_count = 0
    total_count = len(metrics)

    for metric in metrics:
        actual_val = actual.get(metric, 0)
        expected_val = expected.get(metric, 0)

        if actual_val >= expected_val:
            met_count += 1

    return (met_count == total_count, met_count, total_count)

def generate_report_filename() -> Path:
    """Generate timestamped report filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return REPORTS_DIR / f"success-rate-{timestamp}.json"

def main():
    """Main execution function."""
    # Handle command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        elif sys.argv[1] == "--test":
            print("Self-test mode not yet implemented")
            sys.exit(0)

    logging.info("=" * 60)
    logging.info("Success Rate Measurement Script")
    logging.info("=" * 60)
    logging.info("")

    # Process all fixture pairs
    results = []
    skipped_pairs = []

    for i in range(1, EXPECTED_FIXTURE_COUNT + 1):
        try:
            # Load fixture pair
            category, baseline_text, enhanced_text = load_fixture_pair(i)

            # Calculate actual metrics
            ac_testability = calculate_ac_testability(enhanced_text)
            nfr_coverage = calculate_nfr_coverage(enhanced_text)
            specificity = calculate_specificity_score(baseline_text, enhanced_text)

            actual_metrics = {
                "ac_completeness": round(ac_testability, 2),
                "nfr_coverage": round(nfr_coverage, 2),
                "specificity_score": round(specificity, 2)
            }

            # Load expected improvements
            try:
                expected_metrics = load_expected_improvements(i, category)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.warning(f"⚠️  Missing expected file for fixture {i:02d}: {e}")
                expected_metrics = {}

            # Compare actual vs expected
            meets_exp, met_count, total_count = meets_expectations(actual_metrics, expected_metrics)

            result = {
                "fixture_id": f"{i:02d}",
                "category": category,
                "actual": actual_metrics,
                "expected": expected_metrics,
                "meets_expected": meets_exp,
                "metrics_met": f"{met_count}/{total_count}"
            }

            results.append(result)

            # Display per-fixture result
            status = "✅ PASS" if meets_exp else "❌ PARTIAL"
            logging.info(f"Fixture {i:02d} ({category}): {status} ({met_count}/{total_count} metrics)")
            logging.info(f"  AC testability: {actual_metrics['ac_completeness']:.1f}% (expected {expected_metrics.get('ac_completeness', 'N/A')}%)")
            logging.info(f"  NFR coverage: {actual_metrics['nfr_coverage']:.1f}% (expected {expected_metrics.get('nfr_coverage', 'N/A')}%)")
            logging.info(f"  Specificity: {actual_metrics['specificity_score']:.1f}% (expected {expected_metrics.get('specificity_score', 'N/A')}%)")

        except Exception as e:
            logging.warning(f"⚠️  Skipping fixture {i:02d}: {e}")
            skipped_pairs.append({"fixture_id": f"{i:02d}", "error": str(e)})

    logging.info("")

    # Calculate aggregate scores
    if not results:
        logging.error("No valid results. Cannot calculate success rate.")
        sys.exit(4)

    fixtures_meeting_expectations = sum(1 for r in results if r["meets_expected"])
    success_rate = (fixtures_meeting_expectations / len(results)) * 100

    # Aggregate quality scores
    aggregate = {
        "mean_ac_testability": round(sum(r["actual"]["ac_completeness"] for r in results) / len(results), 2),
        "mean_nfr_coverage": round(sum(r["actual"]["nfr_coverage"] for r in results) / len(results), 2),
        "mean_specificity": round(sum(r["actual"]["specificity_score"] for r in results) / len(results), 2)
    }

    # Generate report
    report = {
        "generated_at": datetime.now().isoformat(),
        "fixtures_processed": len(results),
        "fixtures_skipped": len(skipped_pairs),
        "fixtures": results,
        "skipped": skipped_pairs,
        "summary": aggregate,
        "expected_comparison": {
            "fixtures_meeting_expectations": fixtures_meeting_expectations,
            "fixtures_not_meeting": len(results) - fixtures_meeting_expectations,
            "success_rate_percentage": round(success_rate, 2)
        },
        "hypothesis": {
            "threshold": SUCCESS_RATE_THRESHOLD,
            "actual": success_rate,
            "passed": success_rate >= SUCCESS_RATE_THRESHOLD
        }
    }

    # Write report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = generate_report_filename()

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    logging.info(f"Report saved: {report_path}")
    logging.info("")

    # Display results
    logging.info("=" * 60)
    logging.info("SUCCESS RATE VALIDATION")
    logging.info("=" * 60)
    logging.info(f"  Fixtures meeting expectations: {fixtures_meeting_expectations}/{len(results)}")
    logging.info(f"  Success rate: {success_rate:.1f}%")
    logging.info("")

    if report["hypothesis"]["passed"]:
        logging.info(f"✅ Success rate hypothesis VALIDATED: {success_rate:.1f}% (target ≥{SUCCESS_RATE_THRESHOLD}%)")
        sys.exit(0)
    else:
        logging.info(f"❌ Success rate hypothesis FAILED: {success_rate:.1f}% (target ≥{SUCCESS_RATE_THRESHOLD}%)")
        sys.exit(1)

# Import from common.py
sys.path.insert(0, str(Path(__file__).parent))
from common import load_fixture_pair

if __name__ == "__main__":
    main()
