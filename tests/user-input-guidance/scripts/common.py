"""
common.py - Shared utility functions for measurement scripts

Provides token counting, file I/O, report generation, and validation utilities
used across multiple measurement scripts.
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


# ===== CONFIGURATION CONSTANTS =====
# These thresholds are configurable and used across measurement scripts

FIXTURE_ROOT = Path(__file__).parent.parent
FIXTURE_BASELINE_DIR = FIXTURE_ROOT / "fixtures" / "baseline"
FIXTURE_ENHANCED_DIR = FIXTURE_ROOT / "fixtures" / "enhanced"
FIXTURE_EXPECTED_DIR = FIXTURE_ROOT / "fixtures" / "expected"
REPORTS_DIR = FIXTURE_ROOT / "reports"

# Thresholds
TOKEN_SAVINGS_THRESHOLD = 20.0  # Minimum mean savings for hypothesis validation
SUCCESS_RATE_THRESHOLD = 8  # Minimum fixtures meeting expectations (out of 10)
FLESCH_BASELINE_MIN = 50  # Minimum Flesch Reading Ease for baseline
FLESCH_ENHANCED_MIN = 60  # Minimum Flesch Reading Ease for enhanced
WORD_COUNT_MIN = 50  # Minimum words in baseline fixture
WORD_COUNT_MAX = 200  # Maximum words in baseline fixture
LENGTH_INCREASE_MIN = 30  # Minimum % length increase for enhanced
LENGTH_INCREASE_MAX = 60  # Maximum % length increase for enhanced
MIN_GUIDANCE_PRINCIPLES = 3  # Minimum guidance principles in enhanced
MIN_BASELINE_ISSUES = 2  # Minimum quality issues in baseline

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_INCOMPLETE_PAIRS = 2
EXIT_MISSING_LIBRARY = 3
EXIT_INVALID_INPUT = 4
EXIT_MISSING_DEPENDENCIES = 5


# ===== TOKEN COUNTING =====

def get_token_count(text: str) -> int:
    """
    Calculate token count for text using Claude's tokenizer.

    Args:
        text: Input text to tokenize

    Returns:
        Number of tokens

    Raises:
        ImportError: If tiktoken library not available
    """
    try:
        import tiktoken
    except ImportError:
        logger.error("tiktoken library not found. Install with: pip install tiktoken")
        sys.exit(EXIT_MISSING_LIBRARY)

    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        logger.error(f"Token calculation failed: {e}")
        sys.exit(EXIT_INVALID_INPUT)


def calculate_token_savings(baseline_tokens: int, enhanced_tokens: int) -> float:
    """
    Calculate token savings percentage.

    Formula: (baseline - enhanced) / baseline * 100

    Args:
        baseline_tokens: Tokens in baseline fixture
        enhanced_tokens: Tokens in enhanced fixture

    Returns:
        Savings percentage (can be negative if enhanced longer)
    """
    if baseline_tokens == 0:
        return 0.0
    return ((baseline_tokens - enhanced_tokens) / baseline_tokens) * 100


# ===== FILE OPERATIONS =====

def load_fixture(path: Path) -> str:
    """Load fixture file content."""
    if not path.exists():
        logger.error(f"Fixture not found: {path}")
        sys.exit(EXIT_INVALID_INPUT)
    return path.read_text(encoding='utf-8').strip()


def load_expected_json(path: Path) -> Dict:
    """Load and parse expected improvements JSON file."""
    if not path.exists():
        logger.error(f"Expected file not found: {path}")
        sys.exit(EXIT_MISSING_DEPENDENCIES)

    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path.name}: {e}")
        sys.exit(EXIT_INVALID_INPUT)


def get_fixture_pairs() -> List[Tuple[str, Path, Path, Path]]:
    """
    Get list of fixture pairs (baseline, enhanced, expected).

    Returns:
        List of (fixture_id, baseline_path, enhanced_path, expected_path) tuples

    Raises:
        SystemExit: If required directories don't exist
    """
    if not FIXTURE_BASELINE_DIR.exists():
        logger.error(f"Baseline fixtures directory not found: {FIXTURE_BASELINE_DIR}")
        sys.exit(EXIT_INVALID_INPUT)

    pairs = []
    baseline_files = sorted(FIXTURE_BASELINE_DIR.glob("baseline-*.txt"))

    if not baseline_files:
        logger.error("No baseline fixtures found")
        sys.exit(EXIT_INVALID_INPUT)

    for baseline_path in baseline_files:
        # Extract fixture ID (e.g., "01" from "baseline-01-crud-operations.txt")
        match = re.match(r"baseline-(\d+)-(.+)\.txt", baseline_path.name)
        if not match:
            continue

        fixture_num = match.group(1)
        category = match.group(2)

        # Build expected paths
        enhanced_path = FIXTURE_ENHANCED_DIR / f"enhanced-{fixture_num}-{category}.txt"
        expected_path = FIXTURE_EXPECTED_DIR / f"expected-{fixture_num}-{category}.json"

        # Check pair completeness
        if not enhanced_path.exists():
            logger.warning(f"Missing enhanced fixture: {enhanced_path.name}")
            continue

        if not expected_path.exists():
            logger.warning(f"Missing expected file: {expected_path.name}")
            continue

        pairs.append((fixture_num, baseline_path, enhanced_path, expected_path))

    return pairs


def get_latest_report(pattern: str) -> Optional[Path]:
    """
    Get most recent report file matching pattern.

    Args:
        pattern: Glob pattern (e.g., "token-savings-*.json")

    Returns:
        Path to latest matching file or None if not found
    """
    reports = list(REPORTS_DIR.glob(pattern))
    if not reports:
        return None
    return sorted(reports)[-1]  # Most recent (alphabetically)


def save_json_report(data: Dict, filename_prefix: str) -> Path:
    """
    Save JSON report with timestamp.

    Args:
        data: Dictionary to save as JSON
        filename_prefix: Prefix for filename (e.g., "token-savings")

    Returns:
        Path to saved file
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{filename_prefix}-{timestamp}.json"
    filepath = REPORTS_DIR / filename

    # Atomic write: write to temp, then rename
    temp_path = filepath.with_suffix('.json.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    temp_path.rename(filepath)

    return filepath


def save_markdown_report(content: str, filename_prefix: str) -> Path:
    """
    Save Markdown report with timestamp.

    Args:
        content: Markdown content
        filename_prefix: Prefix for filename

    Returns:
        Path to saved file
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{filename_prefix}-{timestamp}.md"
    filepath = REPORTS_DIR / filename

    # Atomic write: write to temp, then rename
    temp_path = filepath.with_suffix('.md.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    temp_path.rename(filepath)

    return filepath


# ===== TEXT ANALYSIS =====

def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def calculate_length_increase(baseline_text: str, enhanced_text: str) -> float:
    """Calculate percentage increase in length (word count)."""
    baseline_words = count_words(baseline_text)
    enhanced_words = count_words(enhanced_text)

    if baseline_words == 0:
        return 0.0
    return ((enhanced_words - baseline_words) / baseline_words) * 100


def count_vague_terms(text: str) -> int:
    """Count occurrences of vague terms in text."""
    vague_terms = ["fast", "good", "better", "optimize", "improve", "easy", "simple"]
    text_lower = text.lower()
    count = 0
    for term in vague_terms:
        # Word boundary matching
        pattern = r'\b' + re.escape(term) + r'\b'
        count += len(re.findall(pattern, text_lower))
    return count


def detect_given_when_then(text: str) -> int:
    """Count Given/When/Then structured blocks in text."""
    pattern = r'\b(Given|When|Then):'
    return len(re.findall(pattern, text, re.IGNORECASE))


def count_nfr_categories(text: str) -> int:
    """
    Count distinct NFR categories mentioned in text.

    Returns:
        Count of distinct categories (0-4)
    """
    text_lower = text.lower()
    categories = {
        'performance': ['performance', 'latency', 'throughput', 'response time', '<'],
        'security': ['security', 'encrypt', 'ssl', 'tls', 'auth', 'hash', 'bcrypt'],
        'reliability': ['reliability', 'uptime', 'availability', '99.9', 'fault', 'recovery'],
        'scalability': ['scalability', 'scale', 'concurrent', 'throughput', 'load']
    }

    count = 0
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            count += 1
    return count


def calculate_readability(text: str) -> Optional[float]:
    """
    Calculate Flesch Reading Ease score.

    Returns:
        Score (0-100) or None if textstat unavailable
    """
    try:
        import textstat
        return textstat.flesch_reading_ease(text)
    except ImportError:
        logger.warning("textstat library not available. Readability checks skipped.")
        return None
    except Exception as e:
        logger.warning(f"Readability calculation failed: {e}")
        return None


# ===== VALIDATION =====

def validate_fixture_naming(filename: str) -> bool:
    """Validate fixture filename format."""
    pattern = r"^(baseline|enhanced|expected)-\d{2}-[a-z0-9-]+\.(txt|json)$"
    return bool(re.match(pattern, filename))


def validate_json_schema(data: Dict, required_fields: List[str]) -> bool:
    """Validate JSON contains required fields."""
    return all(field in data for field in required_fields)


def get_tokenizer_version() -> str:
    """Get installed tiktoken version for transparency."""
    try:
        import tiktoken
        return f"tiktoken-{tiktoken.__version__}"
    except:
        return "tiktoken-unknown"
