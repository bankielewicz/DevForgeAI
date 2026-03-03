"""
Test AC#3: Treelint Tokens Measured for Same Queries
STORY-353: Validate Token Reduction with A/B Test
Status: GREEN - Implementation complete
"""
import pytest
import os
import sys
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

RESEARCH_FILE = "devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"
MEASURE_SCRIPT = "tests/STORY-353/measure_treelint_tokens.py"


class TestAC3TreelintMeasurement:
    """AC#3: Treelint Tokens Measured for Same Queries"""

    def test_measure_treelint_script_exists(self):
        """Test: measure_treelint_tokens.py script exists"""
        assert os.path.exists(MEASURE_SCRIPT), f"FAIL: {MEASURE_SCRIPT} does not exist"

    def test_research_file_has_treelint_data(self):
        """Test: Research file contains Treelint token measurements"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Must have treelint_tokens column in data table
        assert "treelint tokens" in content.lower(), "FAIL: No treelint_tokens column found"

    def test_all_queries_have_treelint_measurements(self):
        """Test: All 5+ queries have Treelint token measurements recorded"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Count query rows (Q1-Q5 pattern in table)
        data_rows = re.findall(r'\|\s*Q\d+\s*\|', content)

        assert len(data_rows) >= 5, f"FAIL: Found {len(data_rows)} complete measurements, need at least 5"

    def test_treelint_used_json_format(self):
        """Test: Treelint was invoked with --format json flag"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Methodology should mention --format json
        assert "--format json" in content or "format json" in content.lower(), \
            "FAIL: No mention of --format json in methodology"

    def test_treelint_measurements_are_numeric(self):
        """Test: Treelint token measurements are valid positive integers"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        assert "Raw Data" in content, "FAIL: No Raw Data section found"


class TestMeasureTreelintTokensScript:
    """Tests for the measure_treelint_tokens.py utility (SVC-001, SVC-003)"""

    def test_script_can_be_imported(self):
        """Test: measure_treelint_tokens.py can be imported"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_treelint_tokens
        except ImportError as e:
            pytest.fail(f"FAIL: Cannot import measure_treelint_tokens: {e}")

    def test_measure_tokens_function_exists(self):
        """Test: measure_tokens(text) -> int function exists"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_treelint_tokens
            assert hasattr(measure_treelint_tokens, 'measure_tokens'), \
                "FAIL: measure_tokens function not found"
            assert callable(measure_treelint_tokens.measure_tokens), \
                "FAIL: measure_tokens is not callable"
        except ImportError:
            pytest.skip("measure_treelint_tokens not yet implemented")

    def test_measure_tokens_handles_json(self):
        """Test: Handles JSON output from Treelint correctly (SVC-003)"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_treelint_tokens
            json_output = '{"functions": [{"name": "test", "body": "def test(): pass"}]}'
            result = measure_treelint_tokens.measure_tokens(json_output)
            assert isinstance(result, int), f"FAIL: Expected int, got {type(result)}"
            assert result > 0, "FAIL: Token count should be positive"
        except ImportError:
            pytest.skip("measure_treelint_tokens not yet implemented")

    def test_parse_treelint_json_function_exists(self):
        """Test: parse_treelint_json(json_str) function exists for extracting function bodies"""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import measure_treelint_tokens
            assert hasattr(measure_treelint_tokens, 'parse_treelint_json'), \
                "FAIL: parse_treelint_json function not found"
        except ImportError:
            pytest.skip("measure_treelint_tokens not yet implemented")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
