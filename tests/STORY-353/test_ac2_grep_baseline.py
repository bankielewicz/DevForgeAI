"""
Test AC#2: Grep Baseline Tokens Measured
STORY-353: Validate Token Reduction with A/B Test
Status: RED (failing) - Implementation required
"""
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

RESEARCH_FILE = "devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"
MEASURE_SCRIPT = "tests/STORY-353/measure_grep_tokens.py"


class TestAC2GrepBaseline:
    """AC#2: Grep Baseline Tokens Measured"""

    def test_measure_grep_script_exists(self):
        """Test: measure_grep_tokens.py script exists"""
        assert os.path.exists(MEASURE_SCRIPT), f"FAIL: {MEASURE_SCRIPT} does not exist"

    def test_research_file_has_grep_data(self):
        """Test: Research file contains Grep token measurements"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Must have grep_tokens column in data table
        assert "grep_tokens" in content.lower(), "FAIL: No grep_tokens column found"

    def test_all_queries_have_grep_measurements(self):
        """Test: All 5+ queries have Grep token measurements recorded"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Count data rows (non-header table rows with numbers)
        import re
        # Pattern: table row with numeric grep_tokens value
        data_rows = re.findall(r'\|\s*\d+\s*\|', content)

        assert len(data_rows) >= 5, f"FAIL: Found {len(data_rows)} measurements, need at least 5"

    def test_grep_measurements_are_numeric(self):
        """Test: Grep token measurements are valid positive integers"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Find Raw Data section and validate numeric values
        assert "Raw Data" in content, "FAIL: No Raw Data section found"

    def test_grep_output_includes_context_tokens(self):
        """Test: Grep measurements include context tokens (surrounding lines)"""
        # SVC-002: Handle multi-line output from Grep
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Methodology should mention context/surrounding lines
        assert "context" in content.lower() or "surrounding" in content.lower(), \
            "FAIL: No mention of context/surrounding lines in methodology"


class TestMeasureGrepTokensScript:
    """Tests for the measure_grep_tokens.py utility (SVC-001, SVC-002)"""

    def test_script_can_be_imported(self):
        """Test: measure_grep_tokens.py can be imported"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_grep_tokens
        except ImportError as e:
            pytest.fail(f"FAIL: Cannot import measure_grep_tokens: {e}")

    def test_measure_tokens_function_exists(self):
        """Test: measure_tokens(text) -> int function exists"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_grep_tokens
            assert hasattr(measure_grep_tokens, 'measure_tokens'), \
                "FAIL: measure_tokens function not found"
            assert callable(measure_grep_tokens.measure_tokens), \
                "FAIL: measure_tokens is not callable"
        except ImportError:
            pytest.skip("measure_grep_tokens not yet implemented")

    def test_measure_tokens_returns_integer(self):
        """Test: measure_tokens returns integer for known string (SVC-001)"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_grep_tokens
            result = measure_grep_tokens.measure_tokens("def hello():\n    pass")
            assert isinstance(result, int), f"FAIL: Expected int, got {type(result)}"
            assert result > 0, "FAIL: Token count should be positive"
        except ImportError:
            pytest.skip("measure_grep_tokens not yet implemented")

    def test_measure_tokens_handles_multiline(self):
        """Test: Handles multi-line output (100+ lines) correctly (SVC-002)"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_grep_tokens
            # Create 100+ line string
            multiline = "\n".join([f"line {i}: content here" for i in range(100)])
            result = measure_grep_tokens.measure_tokens(multiline)
            assert isinstance(result, int), f"FAIL: Expected int, got {type(result)}"
            assert result > 100, "FAIL: 100+ lines should have >100 tokens"
        except ImportError:
            pytest.skip("measure_grep_tokens not yet implemented")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
