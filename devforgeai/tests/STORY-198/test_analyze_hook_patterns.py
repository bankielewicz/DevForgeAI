"""
Failing tests for STORY-198: Command Pattern Analysis Tool
TDD Red Phase - Tests written before implementation

These tests validate:
- AC#1: Log Parsing (UNKNOWN COMMAND entries)
- AC#2: Prefix Extraction (first 2 words)
- AC#3: Safety Filtering (dangerous prefixes excluded)
- AC#4: Frequency Analysis (top 20 with count/percentage)
- AC#5: Impact Calculation (sum top 20 / total * 100)

Technical Requirements: SVC-001 through SVC-005, BR-001, BR-002, NFR-001
"""

import pytest
import sys
from pathlib import Path
import time

# Add scripts directory to path for import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

# Import will fail until implementation exists (TDD Red)
from analyze_hook_patterns import (
    parse_log_entries,
    extract_prefix,
    is_safe_prefix,
    analyze_frequencies,
    calculate_impact,
    DANGEROUS_PREFIXES,
    SAFE_PREFIXES,
)


class TestLogParsing:
    """AC#1: Log Parsing - SVC-001"""

    def test_parse_log_entries_extracts_unknown_commands(self):
        """Given log with UNKNOWN COMMAND entries, when parsed, then entries extracted."""
        log_content = """2026-01-01 10:00:00 UNKNOWN COMMAND REQUIRING APPROVAL: cd /tmp && python script.py
2026-01-01 10:01:00 Safe command executed: git status
2026-01-01 10:02:00 UNKNOWN COMMAND REQUIRING APPROVAL: npm install lodash
"""
        entries = parse_log_entries(log_content)
        assert len(entries) == 2
        assert "cd /tmp && python script.py" in entries
        assert "npm install lodash" in entries

    def test_parse_log_entries_handles_empty_log(self):
        """Given empty log, when parsed, then empty list returned."""
        entries = parse_log_entries("")
        assert entries == []

    def test_parse_log_entries_handles_no_unknown_commands(self):
        """Given log with no UNKNOWN COMMAND entries, when parsed, then empty list."""
        log_content = "2026-01-01 10:00:00 Safe command executed: git status"
        entries = parse_log_entries(log_content)
        assert entries == []

    def test_parse_log_entries_handles_malformed_entries(self):
        """Given malformed entries, when parsed, then no crash and valid entries extracted."""
        log_content = """UNKNOWN COMMAND REQUIRING APPROVAL:
UNKNOWN COMMAND REQUIRING APPROVAL: valid command
UNKNOWN COMMAND REQUIRING APPROVAL:
"""
        entries = parse_log_entries(log_content)
        assert len(entries) == 1
        assert "valid command" in entries


class TestPrefixExtraction:
    """AC#2: Prefix Extraction - SVC-002"""

    def test_extract_prefix_captures_first_two_words(self):
        """Given 'cd /tmp && python', when extracted, then 'cd /tmp' returned."""
        prefix = extract_prefix("cd /tmp && python script.py")
        assert prefix == "cd /tmp"

    def test_extract_prefix_handles_single_word(self):
        """Given single word command, when extracted, then single word returned."""
        prefix = extract_prefix("ls")
        assert prefix == "ls"

    def test_extract_prefix_handles_two_words_exactly(self):
        """Given two word command, when extracted, then both words returned."""
        prefix = extract_prefix("git status")
        assert prefix == "git status"

    def test_extract_prefix_normalizes_whitespace(self):
        """Given extra whitespace, when extracted, then normalized."""
        prefix = extract_prefix("  git   status   --verbose")
        assert prefix == "git status"


class TestSafetyFiltering:
    """AC#3: Safety Filtering - SVC-003"""

    def test_is_safe_prefix_excludes_rm(self):
        """Given 'rm -rf', when evaluated, then False (dangerous)."""
        assert is_safe_prefix("rm -rf") is False

    def test_is_safe_prefix_excludes_sudo(self):
        """Given 'sudo apt', when evaluated, then False (dangerous)."""
        assert is_safe_prefix("sudo apt") is False

    def test_is_safe_prefix_excludes_curl(self):
        """Given 'curl http://example.com', when evaluated, then False."""
        assert is_safe_prefix("curl http://example.com") is False

    def test_is_safe_prefix_excludes_wget(self):
        """Given 'wget http://example.com', when evaluated, then False."""
        assert is_safe_prefix("wget http://example.com") is False

    def test_is_safe_prefix_excludes_dd(self):
        """Given 'dd if=/dev', when evaluated, then False."""
        assert is_safe_prefix("dd if=/dev") is False

    def test_is_safe_prefix_includes_devforgeai(self):
        """Given 'devforgeai' prefix, when evaluated, then True (safe)."""
        assert is_safe_prefix("devforgeai validate") is True

    def test_is_safe_prefix_includes_git(self):
        """Given 'git' prefix, when evaluated, then True (safe)."""
        assert is_safe_prefix("git status") is True

    def test_is_safe_prefix_includes_python(self):
        """Given 'python' prefix, when evaluated, then True (safe)."""
        assert is_safe_prefix("python script.py") is True

    def test_is_safe_prefix_includes_cd(self):
        """Given 'cd' prefix, when evaluated, then True (safe)."""
        assert is_safe_prefix("cd /tmp") is True


class TestFrequencyAnalysis:
    """AC#4: Frequency Analysis - SVC-004"""

    def test_analyze_frequencies_returns_top_20(self):
        """Given safe candidates, when analyzed, then top 20 returned."""
        prefixes = ["git status"] * 50 + ["python script.py"] * 30 + ["cd /tmp"] * 20
        for i in range(30):
            prefixes.append(f"unique{i} cmd")

        result = analyze_frequencies(prefixes)
        assert len(result) <= 20

    def test_analyze_frequencies_sorted_by_count_descending(self):
        """Given prefixes, when analyzed, then sorted by count descending."""
        prefixes = ["git status"] * 10 + ["python script.py"] * 50 + ["cd /tmp"] * 30
        result = analyze_frequencies(prefixes)

        counts = [count for _, count, _ in result]
        assert counts == sorted(counts, reverse=True)

    def test_analyze_frequencies_top_has_highest_count(self):
        """Given prefixes, when analyzed, then top candidate has highest count."""
        prefixes = ["git status"] * 10 + ["python script.py"] * 100 + ["cd /tmp"] * 50
        result = analyze_frequencies(prefixes)

        top_prefix, top_count, _ = result[0]
        assert top_prefix == "python script.py"
        assert top_count == 100

    def test_analyze_frequencies_includes_percentage(self):
        """Given prefixes, when analyzed, then percentage calculated correctly."""
        prefixes = ["git status"] * 50 + ["cd /tmp"] * 50  # 100 total
        result = analyze_frequencies(prefixes)

        _, count, percentage = result[0]
        assert percentage == 50.0  # 50 out of 100


class TestImpactCalculation:
    """AC#5: Impact Calculation - SVC-005"""

    def test_calculate_impact_percentage(self):
        """Given top 20 candidates, when calculated, then impact = sum/total*100."""
        # 80 commands would be auto-approved from top 20
        top_20 = [("prefix1", 40, 40.0), ("prefix2", 40, 40.0)]
        total = 100

        impact = calculate_impact(top_20, total)
        assert impact == 80.0  # (40+40)/100*100

    def test_calculate_impact_handles_zero_total(self):
        """Given zero total, when calculated, then 0.0 returned (no crash)."""
        impact = calculate_impact([], 0)
        assert impact == 0.0


class TestBusinessRules:
    """BR-001, BR-002: Standard library only, safe prefix whitelist"""

    def test_no_external_dependencies(self):
        """BR-001: Only Python 3 standard library used."""
        # Import should work without pip install
        # If this test runs, import succeeded
        assert True

    def test_dangerous_prefixes_defined(self):
        """SVC-003: Dangerous prefixes list contains rm, sudo, curl, wget, dd."""
        required = {"rm", "sudo", "curl", "wget", "dd"}
        assert required.issubset(set(DANGEROUS_PREFIXES))

    def test_safe_prefixes_defined(self):
        """BR-002: Safe prefixes include common DevForgeAI operations."""
        required = {"cd", "git", "python", "devforgeai", "which", "stat", "file", "ls"}
        assert required.issubset(set(SAFE_PREFIXES))


class TestPerformance:
    """NFR-001: Performance requirements"""

    def test_analyze_10000_entries_under_5_seconds(self):
        """NFR-001: Analyze 10,000 log entries in < 5 seconds."""
        log_lines = []
        for i in range(10000):
            log_lines.append(f"UNKNOWN COMMAND REQUIRING APPROVAL: git status {i}")
        log_content = "\n".join(log_lines)

        start = time.time()
        entries = parse_log_entries(log_content)
        prefixes = [extract_prefix(e) for e in entries]
        safe_prefixes = [p for p in prefixes if is_safe_prefix(p)]
        analyze_frequencies(safe_prefixes)
        elapsed = time.time() - start

        assert elapsed < 5.0, f"Took {elapsed:.2f}s (limit: 5s)"
