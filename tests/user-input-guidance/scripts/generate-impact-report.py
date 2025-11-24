#!/usr/bin/env python3
"""
Impact Report Generation Script

Generates comprehensive Markdown report from token-savings and success-rate
measurement results. Includes executive summary, metrics analysis, fixture
breakdown, and actionable recommendations.

Requires:
    - token-savings-*.json report in reports/ directory
    - success-rate-*.json report in reports/ directory

Usage:
    python generate-impact-report.py
    python generate-impact-report.py --help
    python generate-impact-report.py --test

Exit Codes:
    0 - Success (report generated)
    5 - Missing required input reports
"""

import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration constants
REPORTS_DIR = Path(__file__).parent.parent / "reports"
TOKEN_SAVINGS_THRESHOLD = 20.0
SUCCESS_RATE_THRESHOLD = 80.0
BAR_CHART_WIDTH = 50
TABLE_COLUMN_PADDING = 2

# Report section titles
SECTION_EXECUTIVE_SUMMARY = "Executive Summary"
SECTION_TOKEN_EFFICIENCY = "Token Efficiency"
SECTION_QUALITY_IMPROVEMENTS = "Quality Improvements"
SECTION_FIXTURE_ANALYSIS = "Fixture Analysis"
SECTION_RECOMMENDATIONS = "Recommendations"

def find_latest_report(pattern: str) -> Optional[Path]:
    """
    Find most recent report matching pattern.

    Args:
        pattern: Glob pattern (e.g., "token-savings-*.json")

    Returns:
        Path to latest report or None
    """
    reports = sorted(REPORTS_DIR.glob(pattern), reverse=True)
    return reports[0] if reports else None

def generate_bar_chart(percentage: float, width: int = 50) -> str:
    """
    Generate ASCII bar chart for percentage value.

    Args:
        percentage: Value 0-100
        width: Total width in characters

    Returns:
        Bar chart string using █ and ░ characters
    """
    filled = int((percentage / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty

def generate_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Generate ASCII table with Unicode box-drawing characters.

    Args:
        headers: Column headers
        rows: Table rows

    Returns:
        Formatted table string
    """
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build table
    lines = []

    # Top border
    lines.append("┌─" + "─┬─".join("─" * w for w in col_widths) + "─┐")

    # Headers
    header_row = "│ " + " │ ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " │"
    lines.append(header_row)

    # Header separator
    lines.append("├─" + "─┼─".join("─" * w for w in col_widths) + "─┤")

    # Data rows
    for row in rows:
        data_row = "│ " + " │ ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + " │"
        lines.append(data_row)

    # Bottom border
    lines.append("└─" + "─┴─".join("─" * w for w in col_widths) + "─┘")

    return "\n".join(lines)

def _handle_command_line_arguments() -> None:
    """Handle and process command-line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        elif sys.argv[1] == "--test":
            print("Self-test mode not yet implemented")
            sys.exit(0)


def main():
    """Main execution function."""
    # Handle command-line arguments
    _handle_command_line_arguments()

    logging.info("=" * 60)
    logging.info("Impact Report Generation Script")
    logging.info("=" * 60)
    logging.info("")

    # Find required input reports
    token_report_path = find_latest_report("token-savings-*.json")
    success_report_path = find_latest_report("success-rate-*.json")

    # Validate inputs exist
    if not token_report_path:
        logging.error("Missing required report: token-savings-*.json")
        logging.info("Run measure-token-savings.py before generating impact report.")
        sys.exit(5)

    if not success_report_path:
        logging.error("Missing required report: success-rate-*.json")
        logging.info("Run measure-success-rate.py before generating impact report.")
        sys.exit(5)

    logging.info(f"Loading token savings report: {token_report_path.name}")
    logging.info(f"Loading success rate report: {success_report_path.name}")
    logging.info("")

    # Load reports
    with open(token_report_path, 'r') as f:
        token_data = json.load(f)

    with open(success_report_path, 'r') as f:
        success_data = json.load(f)

    # Generate Markdown report
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report_path = REPORTS_DIR / f"impact-report-{timestamp}.md"

    with open(report_path, 'w', encoding='utf-8') as f:
        # Section 1: Executive Summary
        f.write("# User Input Guidance Impact Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write("## Executive Summary\n\n")

        hypothesis_passed = token_data["hypothesis"]["passed"] and success_data["hypothesis"]["passed"]

        if hypothesis_passed:
            f.write("**Hypothesis:** ✅ VALIDATED\n\n")
            f.write(f"User input guidance system successfully improves input quality:\n")
            f.write(f"- Token efficiency: {token_data['mean_savings']:.1f}% average reduction (target ≥20%)\n")
            f.write(f"- Quality metrics: {success_data['expected_comparison']['success_rate_percentage']:.1f}% fixtures meet expectations (target ≥80%)\n")
            f.write(f"- AC testability: {success_data['summary']['mean_ac_testability']:.1f}% average\n")
            f.write(f"- NFR coverage: {success_data['summary']['mean_nfr_coverage']:.1f}% average\n")
            f.write(f"- Specificity: {success_data['summary']['mean_specificity']:.1f}% vague term reduction\n\n")
            f.write("**Recommendation:** Continue using guidance system for all user inputs\n\n")
        else:
            f.write("**Hypothesis:** ❌ NOT VALIDATED\n\n")
            failures = []
            if not token_data["hypothesis"]["passed"]:
                failures.append(f"Token savings {token_data['mean_savings']:.1f}% < 20% target")
            if not success_data["hypothesis"]["passed"]:
                failures.append(f"Success rate {success_data['expected_comparison']['success_rate_percentage']:.1f}% < 80% target")

            f.write("Issues:\n")
            for failure in failures:
                f.write(f"- {failure}\n")
            f.write("\n**Recommendation:** Review and refine guidance system\n\n")

        # Section 2: Token Efficiency
        f.write("---\n\n")
        f.write("## Token Efficiency\n\n")
        f.write(f"**Mean Savings:** {token_data['mean_savings']:.2f}%\n")
        f.write(f"**Median Savings:** {token_data['median_savings']:.2f}%\n")
        f.write(f"**Std Deviation:** {token_data['std_dev']:.2f}%\n")
        f.write(f"**Range:** {token_data.get('min_savings', 0):.2f}% to {token_data.get('max_savings', 0):.2f}%\n\n")

        # Bar chart
        f.write("### Savings Distribution\n\n")
        f.write("```\n")
        for result in token_data["results"]:
            bar = generate_bar_chart(max(0, result["savings_percentage"]), 40)
            f.write(f"Fixture {result['fixture_id']}: {bar} {result['savings_percentage']:+6.1f}%\n")
        f.write("```\n\n")

        # Per-fixture table
        f.write("### Per-Fixture Breakdown\n\n")
        headers = ["Fixture", "Category", "Baseline", "Enhanced", "Savings"]
        rows = []
        for result in token_data["results"]:
            rows.append([
                result["fixture_id"],
                result["category"],
                f"{result['baseline_tokens']} tokens",
                f"{result['enhanced_tokens']} tokens",
                f"{result['savings_percentage']:+.1f}%"
            ])

        f.write(generate_table(headers, rows))
        f.write("\n\n")

        # Section 3: Quality Improvements
        f.write("---\n\n")
        f.write("## Quality Improvements\n\n")
        f.write(f"**AC Testability:** {success_data['summary']['mean_ac_testability']:.1f}% average\n")
        f.write(f"**NFR Coverage:** {success_data['summary']['mean_nfr_coverage']:.1f}% average\n")
        f.write(f"**Specificity:** {success_data['summary']['mean_specificity']:.1f}% average\n\n")

        # Section 4: Fixture Analysis
        f.write("---\n\n")
        f.write("## Fixture Analysis\n\n")
        f.write(f"**Fixtures Meeting Expectations:** {success_data['fixtures_meeting_expectations']}/{len(success_data['results'])}\n")
        f.write(f"**Success Rate:** {success_data['expected_comparison']['success_rate_percentage']:.1f}%\n\n")

        # Comparison table
        headers = ["Fixture", "AC Test", "NFR Cov", "Specificity", "Status"]
        rows = []
        for fixture in success_data["results"]:
            status = "✅ PASS" if fixture["meets_expected"] else "❌ PARTIAL"
            rows.append([
                fixture["fixture_id"],
                f"{fixture['actual']['ac_completeness']:.0f}%",
                f"{fixture['actual']['nfr_coverage']:.0f}%",
                f"{fixture['actual']['specificity_score']:.0f}%",
                status
            ])

        f.write(generate_table(headers, rows))
        f.write("\n\n")

        # Section 5: Recommendations
        f.write("---\n\n")
        f.write("## Recommendations\n\n")

        # Check for outliers
        outliers = success_data.get("outliers", [])
        outlier_count = success_data.get("outlier_count", 0)

        if hypothesis_passed:
            f.write("**Primary:** Continue using current guidance system\n\n")
            f.write("**Secondary:** Consider incremental refinements:\n")

            # Identify low-performing fixtures
            low_performers = [r for r in token_data["results"] if r["savings_percentage"] < 15]
            if low_performers:
                f.write(f"- Review guidance for: {', '.join(r['category'] for r in low_performers)} (lower savings)\n")

            not_meeting = [f for f in success_data["fixtures"] if not f["meets_expected"]]
            if not_meeting:
                f.write(f"- Improve quality metrics for: {', '.join(f['category'] for f in not_meeting)}\n")

            # Flag unrealistic expectations if outliers detected
            if outlier_count >= 3:
                f.write(f"- Review expected improvements for {outlier_count} outlier deviations\n")
        else:
            f.write("**Required:** Refine guidance system\n\n")
            f.write("Specific areas:\n")

            if token_data['mean_savings'] < 20:
                f.write(f"- Token efficiency below target ({token_data['mean_savings']:.1f}% < 20%)\n")
                f.write("  * Review guidance sections on removing verbosity\n")
                f.write("  * Emphasize clarity over detail\n")

            if success_data['expected_comparison']['success_rate_percentage'] < 80:
                f.write(f"- Quality success rate below target ({success_data['expected_comparison']['success_rate_percentage']:.1f}% < 80%)\n")
                f.write("  * Review fixture expectations for realism\n")
                f.write("  * Strengthen guidance principles\n")

        f.write("\n")

    logging.info(f"Impact report saved: {report_path}")
    logging.info("")
    logging.info("✅ Impact report generation complete")

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
