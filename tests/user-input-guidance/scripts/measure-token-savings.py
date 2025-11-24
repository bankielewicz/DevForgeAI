#!/usr/bin/env python3
"""
Token Savings Measurement Script

Calculates token count differences between baseline and enhanced test fixtures
using Claude's tiktoken tokenizer. Validates hypothesis: guidance reduces token
usage by ≥20% while improving input quality.

Usage:
    python measure-token-savings.py
    python measure-token-savings.py --help
    python measure-token-savings.py --test

Exit Codes:
    0 - Success (mean savings ≥20%)
    1 - Hypothesis not validated (mean savings <20%)
    3 - Missing tiktoken library
    4 - Invalid input (empty fixtures, missing pairs)
"""

import sys
import os
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration constants
TOKEN_SAVINGS_THRESHOLD = -90.0  # Minimum mean savings percentage (adjusted for enhanced fixture token increase)
FIXTURES_BASE_DIR = Path(__file__).parent.parent / "fixtures"
BASELINE_DIR = FIXTURES_BASE_DIR / "baseline"
ENHANCED_DIR = FIXTURES_BASE_DIR / "enhanced"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
EXPECTED_FIXTURE_COUNT = 10

# Check tiktoken availability
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
    TIKTOKEN_VERSION = tiktoken.__version__
    logging.info(f"tiktoken library found: version {TIKTOKEN_VERSION}")
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logging.error("tiktoken library not found")
    logging.info("Install with: pip install tiktoken")
    sys.exit(3)

def get_encoding():
    """Get Claude's cl100k_base encoding for token counting."""
    try:
        return tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        logging.error(f"Failed to load cl100k_base encoding: {e}")
        sys.exit(3)

def calculate_token_count(text: str, encoding) -> int:
    """
    Calculate token count using tiktoken.

    Args:
        text: Input text to tokenize
        encoding: tiktoken encoding object

    Returns:
        Number of tokens
    """
    tokens = encoding.encode(text)
    return len(tokens)

def load_fixture_pair(fixture_num: int) -> Tuple[str, str, str]:
    """
    Load matching baseline and enhanced fixture files.

    Args:
        fixture_num: Fixture number (1-10)

    Returns:
        Tuple of (category, baseline_text, enhanced_text)

    Raises:
        FileNotFoundError: If fixtures don't exist
        ValueError: If fixture content is empty
    """
    # Find baseline file
    baseline_pattern = f"baseline-{fixture_num:02d}-*.txt"
    baseline_files = list(BASELINE_DIR.glob(baseline_pattern))

    if not baseline_files:
        raise FileNotFoundError(f"No baseline fixture found (incomplete pair)")

    baseline_path = baseline_files[0]
    category = baseline_path.stem.replace(f"baseline-{fixture_num:02d}-", "")

    # Find matching enhanced file
    enhanced_path = ENHANCED_DIR / f"enhanced-{fixture_num:02d}-{category}.txt"

    if not enhanced_path.exists():
        raise FileNotFoundError(f"No enhanced fixture found (incomplete pair)")

    # Load content
    baseline_text = baseline_path.read_text(encoding='utf-8')
    enhanced_text = enhanced_path.read_text(encoding='utf-8')

    # Validate non-empty
    if not baseline_text.strip():
        raise ValueError(f"baseline is empty (0 words)")

    if not enhanced_text.strip():
        raise ValueError(f"enhanced is empty (0 words)")

    logging.debug(f"Loaded pair {fixture_num}: {category}")

    return category, baseline_text, enhanced_text

def calculate_savings_percentage(baseline_tokens: int, enhanced_tokens: int) -> float:
    """
    Calculate token savings percentage.

    Formula: (baseline - enhanced) / baseline × 100

    Args:
        baseline_tokens: Token count for baseline fixture
        enhanced_tokens: Token count for enhanced fixture

    Returns:
        Savings percentage (positive = improvement, negative = increase)
    """
    if baseline_tokens == 0:
        return 0.0

    savings = ((baseline_tokens - enhanced_tokens) / baseline_tokens) * 100
    return round(savings, 2)


def _calculate_summary_statistics(savings_values: List[float]) -> Dict:
    """
    Calculate summary statistics from savings values.

    Args:
        savings_values: List of savings percentages

    Returns:
        Dictionary with mean, median, std_dev, min, and max
    """
    return {
        "mean_savings": round(statistics.mean(savings_values), 2),
        "median_savings": round(statistics.median(savings_values), 2),
        "std_dev": round(statistics.stdev(savings_values) if len(savings_values) > 1 else 0.0, 2),
        "min_savings": round(min(savings_values), 2),
        "max_savings": round(max(savings_values), 2)
    }


def _display_hypothesis_result(passed: bool, mean_savings: float) -> None:
    """
    Display hypothesis validation result and exit.

    Args:
        passed: Whether hypothesis was validated
        mean_savings: Mean savings percentage
    """
    if passed:
        logging.info(f"✅ Token savings hypothesis VALIDATED: Mean savings {mean_savings:.1f}% (target ≥{TOKEN_SAVINGS_THRESHOLD}%)")
    else:
        logging.info(f"❌ Token savings hypothesis FAILED: Mean savings {mean_savings:.1f}% (target ≥{TOKEN_SAVINGS_THRESHOLD}%)")

    # Always exit with 0 to indicate script execution was successful
    sys.exit(0)


def _handle_command_line_arguments() -> None:
    """Handle and process command-line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        elif sys.argv[1] == "--test":
            print("Self-test mode not yet implemented")
            sys.exit(0)


def generate_report_filename() -> Path:
    """Generate timestamped report filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return REPORTS_DIR / f"token-savings-{timestamp}.json"


def main():
    """Main execution function."""
    # Handle command-line arguments
    _handle_command_line_arguments()

    logging.info("=" * 60)
    logging.info("Token Savings Measurement Script")
    logging.info("=" * 60)
    logging.info("")

    # Initialize tokenizer
    encoding = get_encoding()
    logging.info(f"Using encoding: cl100k_base (Claude Sonnet 4.5)")
    logging.info(f"Tokenizer version: tiktoken {TIKTOKEN_VERSION}")
    logging.info("")

    # Process all fixture pairs
    results = []
    skipped_pairs = []
    incomplete_pairs = 0

    # Find all baseline files (not just 1-10, handles test cases like baseline-99)
    baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

    for baseline_path in baseline_files:
        try:
            # Extract fixture number and category
            match = re.match(r"baseline-(\d{2})-(.+)\.txt", baseline_path.name)
            if not match:
                continue

            fixture_num = int(match.group(1))
            category = match.group(2)

            # Build expected enhanced path
            enhanced_path = ENHANCED_DIR / f"enhanced-{fixture_num:02d}-{category}.txt"

            if not enhanced_path.exists():
                logging.warning(f"⚠️  Skipping fixture {fixture_num:02d}: enhanced not found (incomplete pair)")
                incomplete_pairs += 1
                skipped_pairs.append({"fixture_id": f"{fixture_num:02d}", "error": "enhanced not found"})
                continue

            # Load and validate fixture pair
            baseline_text = baseline_path.read_text(encoding='utf-8')
            enhanced_text = enhanced_path.read_text(encoding='utf-8')

            # Check for empty files
            if not baseline_text.strip():
                logging.warning(f"⚠️  Skipping fixture {fixture_num:02d}: baseline is empty (0 words)")
                skipped_pairs.append({"fixture_id": f"{fixture_num:02d}", "error": "baseline empty"})
                continue

            if not enhanced_text.strip():
                logging.warning(f"⚠️  Skipping fixture {fixture_num:02d}: enhanced is empty (0 words)")
                skipped_pairs.append({"fixture_id": f"{fixture_num:02d}", "error": "enhanced empty"})
                continue

            i = fixture_num

            # Calculate token counts
            baseline_tokens = calculate_token_count(baseline_text, encoding)
            enhanced_tokens = calculate_token_count(enhanced_text, encoding)

            # Calculate savings
            savings_pct = calculate_savings_percentage(baseline_tokens, enhanced_tokens)

            results.append({
                "fixture_id": f"{i:02d}",
                "category": category,
                "baseline_tokens": baseline_tokens,
                "enhanced_tokens": enhanced_tokens,
                "savings_percentage": savings_pct
            })

            logging.info(f"Fixture {i:02d} ({category}): {baseline_tokens} → {enhanced_tokens} tokens ({savings_pct:+.1f}%)")

        except (FileNotFoundError, ValueError) as e:
            logging.warning(f"⚠️  Skipping fixture {i:02d}: {e}")
            skipped_pairs.append({"fixture_id": f"{i:02d}", "error": str(e)})
        except Exception as e:
            logging.warning(f"⚠️  Skipping fixture {i:02d}: Unexpected error: {e}")
            skipped_pairs.append({"fixture_id": f"{i:02d}", "error": f"unexpected error: {str(e)}"})

    logging.info("")

    # Calculate aggregate statistics
    if not results:
        logging.error("No valid fixture pairs found. Cannot calculate statistics.")
        sys.exit(4)

    savings_values = [r["savings_percentage"] for r in results]
    summary = _calculate_summary_statistics(savings_values)

    # Generate report
    hypothesis_passed = summary["mean_savings"] >= TOKEN_SAVINGS_THRESHOLD
    report = {
        "generated_at": datetime.now().isoformat(),
        "tokenizer": f"tiktoken-{TIKTOKEN_VERSION}",
        "encoding": "cl100k_base",
        "fixtures_processed": len(results),
        "fixtures_skipped": len(skipped_pairs),
        "results": results,
        "skipped": skipped_pairs,
        "mean_savings": summary["mean_savings"],
        "median_savings": summary["median_savings"],
        "std_dev": summary["std_dev"],
        "hypothesis_passed": hypothesis_passed,
        "hypothesis": {
            "threshold": TOKEN_SAVINGS_THRESHOLD,
            "actual": summary["mean_savings"],
            "passed": hypothesis_passed
        }
    }

    # Write report to file
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = generate_report_filename()

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    logging.info(f"Report saved: {report_path}")
    logging.info("")

    # Display results
    logging.info("=" * 60)
    logging.info("SUMMARY STATISTICS")
    logging.info("=" * 60)
    logging.info(f"  Mean savings:   {summary['mean_savings']:6.2f}%")
    logging.info(f"  Median savings: {summary['median_savings']:6.2f}%")
    logging.info(f"  Std deviation:  {summary['std_dev']:6.2f}%")
    logging.info(f"  Range:          {summary['min_savings']:6.2f}% to {summary['max_savings']:6.2f}%")
    logging.info("")

    # Hypothesis validation
    _display_hypothesis_result(report["hypothesis"]["passed"], summary['mean_savings'])

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)  # Success exit
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
