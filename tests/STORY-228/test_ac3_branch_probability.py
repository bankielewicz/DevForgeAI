"""
Unit tests for STORY-228 AC#3: Branch Probability

Test-Driven Development (RED PHASE):
All tests written BEFORE implementation - tests should FAIL initially.

Acceptance Criteria:
**Given** decision trees,
**When** calculating probabilities,
**Then** branch probabilities sum to 100% for each decision point.

Coverage Target: 95% business logic
"""

import pytest
from typing import List, Dict, Any
from unittest.mock import Mock, patch
import json


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def decision_tree_two_branches() -> Dict[str, Any]:
    """Decision tree with two branches per node"""
    return {
        "/dev": {
            "branches": [
                {"command": "/qa", "frequency": 6, "probability": 0.60},
                {"command": "/rca", "frequency": 4, "probability": 0.40}
            ],
            "total_frequency": 10
        }
    }


@pytest.fixture
def decision_tree_three_branches() -> Dict[str, Any]:
    """Decision tree with three branches"""
    return {
        "/ideate": {
            "branches": [
                {"command": "/create-story", "frequency": 5, "probability": 0.50},
                {"command": "/brainstorm", "frequency": 3, "probability": 0.30},
                {"command": "/create-context", "frequency": 2, "probability": 0.20}
            ],
            "total_frequency": 10
        }
    }


@pytest.fixture
def decision_tree_multiple_nodes() -> Dict[str, Any]:
    """Decision tree with multiple decision points"""
    return {
        "/ideate": {
            "branches": [
                {"command": "/create-story", "frequency": 10, "probability": 0.50},
                {"command": "/brainstorm", "frequency": 6, "probability": 0.30},
                {"command": "/create-context", "frequency": 4, "probability": 0.20}
            ],
            "total_frequency": 20
        },
        "/dev": {
            "branches": [
                {"command": "/qa", "frequency": 8, "probability": 0.80},
                {"command": "/rca", "frequency": 2, "probability": 0.20}
            ],
            "total_frequency": 10
        },
        "/qa": {
            "branches": [
                {"command": "/release", "frequency": 7, "probability": 0.70},
                {"command": "/dev", "frequency": 3, "probability": 0.30}
            ],
            "total_frequency": 10
        }
    }


@pytest.fixture
def unvalidated_tree() -> Dict[str, Any]:
    """Tree with probabilities that don't sum to 100%"""
    return {
        "/dev": {
            "branches": [
                {"command": "/qa", "frequency": 6, "probability": 0.55},  # Wrong
                {"command": "/rca", "frequency": 4, "probability": 0.40}   # Sum = 0.95
            ],
            "total_frequency": 10
        }
    }


# ============================================================================
# AC#3: Branch Probability Sum Tests
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestBranchProbabilitySum:
    """AC#3: Branch probabilities sum to 100% for each decision point"""

    def test_two_branch_probabilities_sum_to_100(
        self, decision_tree_two_branches
    ):
        """
        Test: Two-branch decision point sums to 100%

        Given: /dev -> /qa (60%) and /rca (40%)
        When: Validating probabilities
        Then: Sum equals 1.0 (100%)
        """
        # Arrange
        from branching_analysis import validate_probability_sum

        # Act
        is_valid = validate_probability_sum(decision_tree_two_branches)

        # Assert
        assert is_valid is True, "Two-branch probabilities should sum to 100%"

        # Also verify manually
        branches = decision_tree_two_branches["/dev"]["branches"]
        total = sum(b["probability"] for b in branches)
        assert abs(total - 1.0) < 0.001, \
            f"Probability sum should be 1.0, got {total}"

    def test_three_branch_probabilities_sum_to_100(
        self, decision_tree_three_branches
    ):
        """
        Test: Three-branch decision point sums to 100%

        Given: /ideate -> /create-story (50%), /brainstorm (30%), /create-context (20%)
        When: Validating probabilities
        Then: Sum equals 1.0 (100%)
        """
        # Arrange
        from branching_analysis import validate_probability_sum

        # Act
        is_valid = validate_probability_sum(decision_tree_three_branches)

        # Assert
        assert is_valid is True, "Three-branch probabilities should sum to 100%"

        # Also verify manually
        branches = decision_tree_three_branches["/ideate"]["branches"]
        total = sum(b["probability"] for b in branches)
        assert abs(total - 1.0) < 0.001, \
            f"Probability sum should be 1.0, got {total}"

    def test_all_decision_points_sum_to_100(
        self, decision_tree_multiple_nodes
    ):
        """
        Test: ALL decision points in tree have probabilities summing to 100%

        Given: Multiple decision points (/ideate, /dev, /qa)
        When: Validating all decision points
        Then: Each decision point sums to 100%
        """
        # Arrange
        from branching_analysis import validate_all_probability_sums

        # Act
        validation_results = validate_all_probability_sums(decision_tree_multiple_nodes)

        # Assert
        for command, result in validation_results.items():
            assert result["valid"] is True, \
                f"{command} probabilities should sum to 100%"
            assert abs(result["sum"] - 1.0) < 0.001, \
                f"{command} probability sum should be 1.0, got {result['sum']}"

    def test_invalid_probability_sum_detected(self, unvalidated_tree):
        """
        Test: Invalid probability sums are detected

        Given: Tree with probabilities summing to 95% (not 100%)
        When: Validating
        Then: Invalid sum is detected
        """
        # Arrange
        from branching_analysis import validate_probability_sum

        # Act
        is_valid = validate_probability_sum(unvalidated_tree)

        # Assert
        assert is_valid is False, \
            "Should detect invalid probability sum (95% != 100%)"


# ============================================================================
# Probability Calculation Tests
# ============================================================================

@pytest.mark.unit
class TestProbabilityCalculation:
    """Tests for probability calculation correctness"""

    def test_probability_calculated_from_frequency(self):
        """
        Test: Probability = frequency / total_frequency

        Given: Frequencies of 6 and 4 (total 10)
        When: Calculating probabilities
        Then: 6/10 = 0.60, 4/10 = 0.40
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        branching_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 6},
                    "/rca": {"frequency": 4}
                }
            }
        }

        # Act
        result = calculate_probabilities(branching_input)

        # Assert
        branches = result["/dev"]["branches"]
        qa_prob = next(b["probability"] for b in branches if b["command"] == "/qa")
        rca_prob = next(b["probability"] for b in branches if b["command"] == "/rca")

        assert qa_prob == 0.60, f"/qa probability should be 0.60, got {qa_prob}"
        assert rca_prob == 0.40, f"/rca probability should be 0.40, got {rca_prob}"

    def test_single_branch_has_100_percent(self):
        """
        Test: Single branch gets 100% probability

        Given: Only one downstream path
        When: Calculating probabilities
        Then: Single branch has probability 1.0
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        single_branch_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 15}
                }
            }
        }

        # Act
        result = calculate_probabilities(single_branch_input)

        # Assert
        branches = result["/dev"]["branches"]
        assert len(branches) == 1, "Should have single branch"
        assert branches[0]["probability"] == 1.0, \
            "Single branch should have 100% probability"

    def test_equal_frequencies_equal_probabilities(self):
        """
        Test: Equal frequencies result in equal probabilities

        Given: Two branches each with frequency 5
        When: Calculating probabilities
        Then: Each has 50% probability
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        equal_frequency_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 5},
                    "/rca": {"frequency": 5}
                }
            }
        }

        # Act
        result = calculate_probabilities(equal_frequency_input)

        # Assert
        branches = result["/dev"]["branches"]
        for branch in branches:
            assert branch["probability"] == 0.50, \
                f"Equal frequencies should yield 50%, got {branch['probability']}"


# ============================================================================
# Probability Precision Tests
# ============================================================================

@pytest.mark.unit
class TestProbabilityPrecision:
    """Tests for probability precision and rounding"""

    def test_probabilities_rounded_to_two_decimals(self):
        """
        Test: Probabilities are rounded to 2 decimal places

        Given: Frequencies yielding repeating decimals
        When: Calculating probabilities
        Then: Rounded to 2 decimal places
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        repeating_decimal_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 1},
                    "/rca": {"frequency": 2}  # 1/3 and 2/3 = 0.333... and 0.666...
                }
            }
        }

        # Act
        result = calculate_probabilities(repeating_decimal_input)

        # Assert
        branches = result["/dev"]["branches"]
        for branch in branches:
            prob = branch["probability"]
            # Should be rounded to 2 decimal places
            rounded = round(prob, 2)
            assert prob == rounded, \
                f"Probability should be rounded to 2 decimals: {prob}"

    def test_probabilities_always_between_0_and_1(
        self, decision_tree_multiple_nodes
    ):
        """
        Test: All probabilities are within valid range [0, 1]

        Given: Any decision tree
        When: Checking probabilities
        Then: All are between 0 and 1 inclusive
        """
        # Arrange / Act
        tree = decision_tree_multiple_nodes

        # Assert
        for command, node in tree.items():
            for branch in node["branches"]:
                prob = branch["probability"]
                assert 0.0 <= prob <= 1.0, \
                    f"Probability for {command} -> {branch['command']} " \
                    f"should be 0-1, got {prob}"

    def test_sum_equals_100_after_rounding(self):
        """
        Test: Probabilities still sum to 100% after rounding

        Given: Frequencies that cause rounding
        When: Rounding probabilities
        Then: Sum still equals 1.0 (adjust last value if needed)
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        rounding_issue_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 1},
                    "/rca": {"frequency": 1},
                    "/release": {"frequency": 1}
                }
            }
        }

        # Act
        result = calculate_probabilities(rounding_issue_input)

        # Assert
        branches = result["/dev"]["branches"]
        total = sum(b["probability"] for b in branches)
        assert abs(total - 1.0) < 0.01, \
            f"Rounded probabilities should still sum to ~1.0, got {total}"


# ============================================================================
# Edge Cases
# ============================================================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestProbabilityEdgeCases:
    """Edge cases for probability calculations"""

    def test_zero_frequency_branch(self):
        """
        Edge Case: Branch with zero frequency

        Given: One branch has frequency 0
        When: Calculating probabilities
        Then: Zero-frequency branch has 0% probability
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        zero_freq_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 10},
                    "/rca": {"frequency": 0}
                }
            }
        }

        # Act
        result = calculate_probabilities(zero_freq_input)

        # Assert
        branches = result["/dev"]["branches"]
        qa_branch = next((b for b in branches if b["command"] == "/qa"), None)
        rca_branch = next((b for b in branches if b["command"] == "/rca"), None)

        if qa_branch:
            assert qa_branch["probability"] == 1.0, \
                "Non-zero branch should get 100% when other is 0"
        if rca_branch:
            assert rca_branch["probability"] == 0.0, \
                "Zero-frequency branch should have 0% probability"

    def test_all_zero_frequencies(self):
        """
        Edge Case: All branches have zero frequency

        Given: All frequencies are 0
        When: Calculating probabilities
        Then: Handle gracefully (equal distribution or error)
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        all_zero_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 0},
                    "/rca": {"frequency": 0}
                }
            }
        }

        # Act
        result = calculate_probabilities(all_zero_input)

        # Assert
        # Should either skip this decision point or assign equal probabilities
        if "/dev" in result:
            branches = result["/dev"]["branches"]
            total = sum(b["probability"] for b in branches)
            # Either 0 (skipped) or 1.0 (equal distribution)
            assert total == 0.0 or abs(total - 1.0) < 0.01, \
                f"All-zero case should yield 0 or 1 sum, got {total}"

    def test_very_small_probability(self):
        """
        Edge Case: Very small probability (1 vs 999)

        Given: Frequencies 1 and 999
        When: Calculating probabilities
        Then: Small probability is preserved (not rounded to 0)
        """
        # Arrange
        from branching_analysis import calculate_probabilities
        skewed_input = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 999},
                    "/rca": {"frequency": 1}
                }
            }
        }

        # Act
        result = calculate_probabilities(skewed_input)

        # Assert
        branches = result["/dev"]["branches"]
        rca_branch = next(b for b in branches if b["command"] == "/rca")
        # 1/1000 = 0.001 -> should be at least 0.00 or 0.01
        assert rca_branch["probability"] > 0, \
            "Small probability should not be rounded to 0"

    def test_empty_decision_tree(self):
        """
        Edge Case: Empty decision tree

        Given: Empty tree
        When: Validating probabilities
        Then: Returns True (vacuously true)
        """
        # Arrange
        from branching_analysis import validate_probability_sum

        # Act
        is_valid = validate_probability_sum({})

        # Assert
        assert is_valid is True, \
            "Empty tree should be considered valid"

    def test_no_branches(self):
        """
        Edge Case: Decision point with empty branches list

        Given: Node with empty branches array
        When: Validating probabilities
        Then: Handles gracefully
        """
        # Arrange
        from branching_analysis import validate_probability_sum
        empty_branches_tree = {
            "/dev": {
                "branches": [],
                "total_frequency": 0
            }
        }

        # Act
        is_valid = validate_probability_sum(empty_branches_tree)

        # Assert
        # Either True (vacuously) or False (invalid structure)
        assert isinstance(is_valid, bool), "Should return boolean"


# ============================================================================
# Validation Report Tests
# ============================================================================

@pytest.mark.unit
class TestProbabilityValidationReport:
    """Tests for probability validation reporting"""

    def test_validation_returns_details_per_node(
        self, decision_tree_multiple_nodes
    ):
        """
        Test: Validation returns details for each decision point

        Given: Tree with multiple nodes
        When: Running validation
        Then: Report includes each node's sum and validity
        """
        # Arrange
        from branching_analysis import validate_all_probability_sums

        # Act
        report = validate_all_probability_sums(decision_tree_multiple_nodes)

        # Assert
        for command in decision_tree_multiple_nodes.keys():
            assert command in report, f"{command} should be in report"
            assert "valid" in report[command], \
                f"{command} should have 'valid' field"
            assert "sum" in report[command], \
                f"{command} should have 'sum' field"

    def test_invalid_nodes_listed_in_report(self, unvalidated_tree):
        """
        Test: Invalid nodes are clearly identified in report

        Given: Tree with invalid probability sum
        When: Running validation
        Then: Invalid node is flagged in report
        """
        # Arrange
        from branching_analysis import validate_all_probability_sums

        # Act
        report = validate_all_probability_sums(unvalidated_tree)

        # Assert
        assert "/dev" in report
        assert report["/dev"]["valid"] is False, \
            "Invalid node should be flagged"
        assert report["/dev"]["sum"] != 1.0, \
            "Invalid sum should be reported"

    def test_report_json_serializable(self, decision_tree_multiple_nodes):
        """
        Test: Validation report is JSON serializable

        Given: Validation report
        When: Serializing to JSON
        Then: No errors
        """
        # Arrange
        from branching_analysis import validate_all_probability_sums

        # Act
        report = validate_all_probability_sums(decision_tree_multiple_nodes)

        # Assert
        try:
            json_str = json.dumps(report)
            assert json_str is not None
        except (TypeError, ValueError) as e:
            pytest.fail(f"Report should be JSON serializable: {e}")


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.integration
class TestProbabilityIntegration:
    """Integration tests for probability calculation workflow"""

    def test_end_to_end_probability_calculation(self):
        """
        Test: Full workflow from session data to validated probabilities

        Given: Raw session entries
        When: Processing through detection -> tree building -> validation
        Then: Final probabilities sum to 100%
        """
        # Arrange
        from branching_analysis import (
            detect_branching_points,
            build_decision_tree,
            validate_all_probability_sums
        )
        session_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T11:00:00Z", "command": "/dev", "status": "success", "session_id": "s2"},
            {"timestamp": "2025-01-02T11:30:00Z", "command": "/qa", "status": "success", "session_id": "s2"},
            {"timestamp": "2025-01-02T12:00:00Z", "command": "/dev", "status": "error", "session_id": "s3"},
            {"timestamp": "2025-01-02T12:30:00Z", "command": "/rca", "status": "success", "session_id": "s3"},
        ]

        # Act
        branching_points = detect_branching_points(session_data)
        tree = build_decision_tree(branching_points)
        validation = validate_all_probability_sums(tree)

        # Assert
        for command, result in validation.items():
            assert result["valid"] is True, \
                f"Probabilities for {command} should sum to 100%"

    def test_probability_consistency_across_runs(self):
        """
        Test: Same input yields same probabilities

        Given: Identical session data
        When: Running calculation twice
        Then: Results are identical
        """
        # Arrange
        from branching_analysis import (
            detect_branching_points,
            build_decision_tree
        )
        session_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        ]

        # Act
        result1 = build_decision_tree(detect_branching_points(session_data))
        result2 = build_decision_tree(detect_branching_points(session_data))

        # Assert
        assert result1 == result2, "Same input should yield same output"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
