"""
Test AC#4: Reduction Percentage Calculated and Documented
STORY-353: Validate Token Reduction with A/B Test
Status: RED (failing) - Implementation required
"""
import pytest
import os
import sys
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

RESEARCH_FILE = "devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"
REDUCTION_THRESHOLD = 40.0  # BR-001: Must be >= 40% to validate hypothesis


class TestAC4ReductionCalculation:
    """AC#4: Reduction Percentage Calculated and Documented"""

    def test_research_file_has_reduction_column(self):
        """Test: Research file has reduction_pct column in data table"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        assert "reduction" in content.lower(), "FAIL: No reduction column found"

    def test_per_query_reduction_calculated(self):
        """Test: Each query has reduction percentage calculated"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Pattern: table row with percentage (e.g., "| 45.2% |" or "| 45.2 |")
        percentages = re.findall(r'\|\s*(\d+\.?\d*)\s*%?\s*\|', content)

        assert len(percentages) >= 5, f"FAIL: Found {len(percentages)} reduction values, need at least 5"

    def test_overall_average_calculated(self):
        """Test: Overall average reduction percentage is documented"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Should have "average" or "overall" with a percentage
        assert "average" in content.lower() or "overall" in content.lower(), \
            "FAIL: No overall/average reduction documented"

    def test_formula_documented(self):
        """Test: Reduction formula is documented: ((grep - treelint) / grep) * 100"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Formula should be documented
        formula_patterns = [
            "grep_tokens - treelint_tokens",
            "(grep - treelint)",
            "reduction",
            "formula"
        ]
        found = any(pattern.lower() in content.lower() for pattern in formula_patterns)
        assert found, "FAIL: Reduction formula not documented"

    def test_threshold_check_documented(self):
        """Test: 40% threshold validation is documented (BR-001)"""
        assert os.path.exists(RESEARCH_FILE), f"FAIL: {RESEARCH_FILE} does not exist"

        with open(RESEARCH_FILE, 'r') as f:
            content = f.read()

        # Should mention 40% threshold
        assert "40%" in content or "40 percent" in content.lower(), \
            "FAIL: 40% threshold not documented"


class TestReductionCalculationLogic:
    """Tests for the reduction calculation utility"""

    def test_calculate_reduction_formula_correct(self):
        """Test: Reduction formula: ((grep - treelint) / grep) * 100"""
        # Test data
        grep_tokens = 1000
        treelint_tokens = 400
        expected_reduction = ((1000 - 400) / 1000) * 100  # 60%

        # Try to import calculation module
        try:
            from tests.STORY_353 import measure_tokens
            if hasattr(measure_tokens, 'calculate_reduction'):
                result = measure_tokens.calculate_reduction(grep_tokens, treelint_tokens)
                assert abs(result - expected_reduction) < 0.01, \
                    f"FAIL: Expected {expected_reduction}%, got {result}%"
            else:
                pytest.skip("calculate_reduction not yet implemented")
        except ImportError:
            pytest.skip("measure_tokens module not yet implemented")

    def test_calculate_reduction_handles_zero_grep(self):
        """Test: Handles edge case of zero Grep tokens (avoid division by zero)"""
        try:
            from tests.STORY_353 import measure_tokens
            if hasattr(measure_tokens, 'calculate_reduction'):
                # Should return 0 or raise appropriate error
                result = measure_tokens.calculate_reduction(0, 100)
                assert result == 0 or result is None, \
                    "FAIL: Should handle zero grep_tokens gracefully"
            else:
                pytest.skip("calculate_reduction not yet implemented")
        except ImportError:
            pytest.skip("measure_tokens module not yet implemented")

    def test_threshold_validation_passes_above_40(self):
        """Test: Validates pass when reduction >= 40% (BR-001)"""
        try:
            from tests.STORY_353 import measure_tokens
            if hasattr(measure_tokens, 'validate_threshold'):
                assert measure_tokens.validate_threshold(45.0) == True
                assert measure_tokens.validate_threshold(40.0) == True
            else:
                pytest.skip("validate_threshold not yet implemented")
        except ImportError:
            pytest.skip("measure_tokens module not yet implemented")

    def test_threshold_validation_fails_below_40(self):
        """Test: Validates fail when reduction < 40% (BR-001)"""
        try:
            from tests.STORY_353 import measure_tokens
            if hasattr(measure_tokens, 'validate_threshold'):
                assert measure_tokens.validate_threshold(39.9) == False
                assert measure_tokens.validate_threshold(30.0) == False
            else:
                pytest.skip("validate_threshold not yet implemented")
        except ImportError:
            pytest.skip("measure_tokens module not yet implemented")


class TestNFRReproducibility:
    """NFR-001: Measurements must be reproducible within +/-5%"""

    def test_measurement_consistency(self):
        """Test: Same query produces same token count +/-5%"""
        try:
            from tests.STORY_353 import measure_tokens
            if hasattr(measure_tokens, 'measure_tokens'):
                test_text = "def example_function():\n    return 42"

                # Run 3 times
                results = [measure_tokens.measure_tokens(test_text) for _ in range(3)]

                # Check all within 5% of each other
                avg = sum(results) / len(results)
                for r in results:
                    variance = abs(r - avg) / avg * 100
                    assert variance <= 5.0, \
                        f"FAIL: Measurement variance {variance}% exceeds 5% threshold"
            else:
                pytest.skip("measure_tokens not yet implemented")
        except ImportError:
            pytest.skip("measure_tokens module not yet implemented")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
