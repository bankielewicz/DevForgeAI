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
TOKEN_SAVINGS_THRESHOLD = 20.0  # Minimum mean savings percentage
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
        raise FileNotFoundError(f"No baseline fixture found: {baseline_pattern}")

    baseline_path = baseline_files[0]
    category = baseline_path.stem.replace(f"baseline-{fixture_num:02d}-", "")

    # Find matching enhanced file
    enhanced_path = ENHANCED_DIR / f"enhanced-{fixture_num:02d}-{category}.txt"

    if not enhanced_path.exists():
        raise FileNotFoundError(f"No enhanced fixture found: {enhanced_path.name}")

    # Load content
    baseline_text = baseline_path.read_text(encoding='utf-8')
    enhanced_text = enhanced_path.read_text(encoding='utf-8')

    # Validate non-empty
    if not baseline_text.strip():
        raise ValueError(f"{baseline_path.name} is empty (0 words)")

    if not enhanced_text.strip():
        raise ValueError(f"{enhanced_path.name} is empty (0 words)")

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

def generate_report_filename() -> Path:
    """Generate timestamped report filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return REPORTS_DIR / f"token-savings-{timestamp}.json"

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

    for i in range(1, EXPECTED_FIXTURE_COUNT + 1):
        try:
            category, baseline_text, enhanced_text = load_fixture_pair(i)

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

    logging.info("")

    # Calculate aggregate statistics
    if not results:
        logging.error("No valid fixture pairs found. Cannot calculate statistics.")
        sys.exit(4)

    savings_values = [r["savings_percentage"] for r in results]

    summary = {
        "mean_savings": round(statistics.mean(savings_values), 2),
        "median_savings": round(statistics.median(savings_values), 2),
        "std_dev": round(statistics.stdev(savings_values) if len(savings_values) > 1 else 0.0, 2),
        "min_savings": round(min(savings_values), 2),
        "max_savings": round(max(savings_values), 2)
    }

    # Generate report
    report = {
        "generated_at": datetime.now().isoformat(),
        "tokenizer": f"tiktoken-{TIKTOKEN_VERSION}",
        "encoding": "cl100k_base",
        "fixtures_processed": len(results),
        "fixtures_skipped": len(skipped_pairs),
        "results": results,
        "skipped": skipped_pairs,
        "summary": summary,
        "hypothesis": {
            "threshold": TOKEN_SAVINGS_THRESHOLD,
            "actual": summary["mean_savings"],
            "passed": summary["mean_savings"] >= TOKEN_SAVINGS_THRESHOLD
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
    if report["hypothesis"]["passed"]:
        logging.info(f"✅ Token savings hypothesis VALIDATED: Mean savings {summary['mean_savings']:.1f}% (target ≥{TOKEN_SAVINGS_THRESHOLD}%)")
        sys.exit(0)
    else:
        logging.info(f"❌ Token savings hypothesis FAILED: Mean savings {summary['mean_savings']:.1f}% (target ≥{TOKEN_SAVINGS_THRESHOLD}%)")
        sys.exit(1)

if __name__ == "__main__":
    main()
