"""
Unit tests for STORY-228 AC#2: Decision Tree Building

Test-Driven Development (RED PHASE):
All tests written BEFORE implementation - tests should FAIL initially.

Acceptance Criteria:
**Given** branching points,
**When** building trees,
**Then** decision tree shows: command A -> command B (70%) or command C (30%).

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
def branching_points_input() -> Dict[str, Any]:
    """
    Sample branching points from AC#1 detection output

    /dev leads to:
    - /qa (3 occurrences, 60%)
    - /rca (2 occurrences, 40%)
    """
    return {
        "/dev": {
            "downstream": {
                "/qa": {"frequency": 3},
                "/rca": {"frequency": 2}
            }
        },
        "/ideate": {
            "downstream": {
                "/create-story": {"frequency": 5},
                "/brainstorm": {"frequency": 3},
                "/create-context": {"frequency": 2}
            }
        }
    }


@pytest.fixture
def complex_branching_points() -> Dict[str, Any]:
    """
    Multi-level branching points for deeper decision trees

    /ideate -> /create-story (50%) -> /dev (70%) -> /qa (80%)
                                   -> /rca (20%)
              -> /brainstorm (30%)
              -> /create-context (20%)
    """
    return {
        "/ideate": {
            "downstream": {
                "/create-story": {"frequency": 10},
                "/brainstorm": {"frequency": 6},
                "/create-context": {"frequency": 4}
            }
        },
        "/create-story": {
            "downstream": {
                "/dev": {"frequency": 7}
            }
        },
        "/dev": {
            "downstream": {
                "/qa": {"frequency": 8},
                "/rca": {"frequency": 2}
            }
        }
    }


@pytest.fixture
def single_path_branching_point() -> Dict[str, Any]:
    """Branching point with only one downstream path (edge case)"""
    return {
        "/dev": {
            "downstream": {
                "/qa": {"frequency": 10}
            }
        }
    }


# ============================================================================
# AC#2: Decision Tree Building Tests
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestDecisionTreeBuilding:
    """AC#2: Decision tree shows command transitions with probabilities"""

    def test_build_decision_tree_from_branching_points(
        self, branching_points_input
    ):
        """
        Test: Decision tree is built from branching points

        Given: Branching points with /dev -> /qa (3x) and /dev -> /rca (2x)
        When: Building decision tree
        Then: Tree structure contains /dev with branches to /qa and /rca
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        assert "/dev" in tree, "Decision tree should contain /dev"
        assert "branches" in tree["/dev"], "/dev should have branches"
        assert len(tree["/dev"]["branches"]) == 2, \
            "/dev should have 2 branches"

    def test_decision_tree_includes_probabilities(
        self, branching_points_input
    ):
        """
        Test: Decision tree includes probabilities for each branch

        Given: /dev -> /qa (3x, 60%) and /dev -> /rca (2x, 40%)
        When: Building decision tree
        Then: Probabilities are calculated and included
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        branches = tree["/dev"]["branches"]
        qa_branch = next((b for b in branches if b["command"] == "/qa"), None)
        rca_branch = next((b for b in branches if b["command"] == "/rca"), None)

        assert qa_branch is not None, "/qa branch should exist"
        assert rca_branch is not None, "/rca branch should exist"
        assert "probability" in qa_branch, "/qa branch should have probability"
        assert "probability" in rca_branch, "/rca branch should have probability"

        # 3/(3+2) = 0.60 = 60%
        assert abs(qa_branch["probability"] - 0.60) < 0.01, \
            f"/qa probability should be ~60%, got {qa_branch['probability']}"
        # 2/(3+2) = 0.40 = 40%
        assert abs(rca_branch["probability"] - 0.40) < 0.01, \
            f"/rca probability should be ~40%, got {rca_branch['probability']}"

    def test_decision_tree_format_matches_spec(
        self, branching_points_input
    ):
        """
        Test: Decision tree format matches specification

        Spec: "command A -> command B (70%) or command C (30%)"

        Given: Branching points
        When: Formatting decision tree
        Then: Output matches "command -> command (probability%)" format
        """
        # Arrange
        from branching_analysis import format_decision_tree

        # Act
        formatted = format_decision_tree(branching_points_input)

        # Assert
        # Should contain formatted strings like "/dev -> /qa (60%)"
        assert "/dev" in formatted, "Formatted output should contain /dev"
        assert "->" in formatted, "Formatted output should contain arrow"
        assert "%" in formatted, "Formatted output should contain percentage"
        # Check for specific format pattern
        assert "/qa" in formatted, "Should contain downstream command /qa"
        assert "/rca" in formatted, "Should contain downstream command /rca"

    def test_decision_tree_preserves_all_branches(
        self, branching_points_input
    ):
        """
        Test: All branching paths are preserved in decision tree

        Given: /ideate -> /create-story (5x), /brainstorm (3x), /create-context (2x)
        When: Building decision tree
        Then: All 3 branches are present with correct probabilities
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        assert "/ideate" in tree, "Decision tree should contain /ideate"
        branches = tree["/ideate"]["branches"]
        assert len(branches) == 3, "/ideate should have 3 branches"

        # Verify all branches exist
        branch_commands = [b["command"] for b in branches]
        assert "/create-story" in branch_commands
        assert "/brainstorm" in branch_commands
        assert "/create-context" in branch_commands


# ============================================================================
# Decision Tree Structure Tests
# ============================================================================

@pytest.mark.unit
class TestDecisionTreeStructure:
    """Tests for decision tree internal structure"""

    def test_tree_nodes_have_required_fields(
        self, branching_points_input
    ):
        """
        Test: Each tree node has required fields

        Required fields:
        - command: The source command
        - branches: List of downstream branches
        - total_frequency: Sum of all downstream frequencies
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        for command, node in tree.items():
            assert "branches" in node, f"{command} should have 'branches'"
            assert "total_frequency" in node, \
                f"{command} should have 'total_frequency'"
            assert isinstance(node["branches"], list), \
                f"{command} branches should be a list"

    def test_branch_nodes_have_required_fields(
        self, branching_points_input
    ):
        """
        Test: Each branch node has required fields

        Required fields:
        - command: The downstream command
        - frequency: Raw count
        - probability: Calculated probability (0.0 - 1.0)
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        for command, node in tree.items():
            for branch in node["branches"]:
                assert "command" in branch, "Branch should have 'command'"
                assert "frequency" in branch, "Branch should have 'frequency'"
                assert "probability" in branch, "Branch should have 'probability'"
                # Probability should be between 0 and 1
                assert 0.0 <= branch["probability"] <= 1.0, \
                    f"Probability should be 0-1, got {branch['probability']}"

    def test_decision_tree_sorted_by_probability(
        self, branching_points_input
    ):
        """
        Test: Branches are sorted by probability (highest first)

        Given: Multiple branches with different probabilities
        When: Building decision tree
        Then: Branches are ordered from highest to lowest probability
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        for command, node in tree.items():
            branches = node["branches"]
            if len(branches) > 1:
                probabilities = [b["probability"] for b in branches]
                assert probabilities == sorted(probabilities, reverse=True), \
                    f"Branches for {command} should be sorted by probability desc"


# ============================================================================
# Multi-Level Decision Tree Tests
# ============================================================================

@pytest.mark.unit
class TestMultiLevelDecisionTree:
    """Tests for multi-level decision trees"""

    def test_build_multi_level_tree(self, complex_branching_points):
        """
        Test: Multi-level trees are built correctly

        Given: Chain of branching points (/ideate -> /create-story -> /dev -> /qa)
        When: Building decision tree
        Then: All levels are represented
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(complex_branching_points)

        # Assert
        assert "/ideate" in tree, "Level 1: /ideate should be in tree"
        assert "/create-story" in tree, "Level 2: /create-story should be in tree"
        assert "/dev" in tree, "Level 3: /dev should be in tree"

    def test_multi_level_tree_depth_tracking(self, complex_branching_points):
        """
        Test: Tree includes depth information for each node

        Given: Multi-level branching structure
        When: Building decision tree with depth tracking
        Then: Each node has depth field
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(complex_branching_points, track_depth=True)

        # Assert
        for command, node in tree.items():
            assert "depth" in node or "level" in node, \
                f"{command} should have depth tracking"


# ============================================================================
# Edge Cases
# ============================================================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestDecisionTreeEdgeCases:
    """Edge cases for decision tree building"""

    def test_empty_branching_points(self):
        """
        Edge Case: Empty branching points input

        Given: Empty branching points dictionary
        When: Building decision tree
        Then: Returns empty tree
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree({})

        # Assert
        assert tree == {}, "Empty input should return empty tree"

    def test_single_path_no_branching(self, single_path_branching_point):
        """
        Edge Case: Branching point with only one downstream

        Given: /dev -> /qa only
        When: Building decision tree
        Then: Single branch with 100% probability
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(single_path_branching_point)

        # Assert
        assert "/dev" in tree
        branches = tree["/dev"]["branches"]
        assert len(branches) == 1, "Should have single branch"
        assert branches[0]["probability"] == 1.0, \
            "Single branch should have 100% probability"

    def test_handles_zero_frequency(self):
        """
        Edge Case: Branch with zero frequency

        Given: Branching point with zero frequency branch
        When: Building decision tree
        Then: Handles gracefully (skip or 0% probability)
        """
        # Arrange
        from branching_analysis import build_decision_tree
        zero_frequency_data = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 5},
                    "/rca": {"frequency": 0}
                }
            }
        }

        # Act
        tree = build_decision_tree(zero_frequency_data)

        # Assert
        # Should either skip zero-frequency or include with 0% probability
        branches = tree["/dev"]["branches"]
        for branch in branches:
            if branch["command"] == "/rca":
                assert branch["probability"] == 0.0, \
                    "Zero frequency should have 0% probability"
                break
        else:
            # Zero-frequency branch was filtered out - also acceptable
            assert len(branches) == 1, \
                "Zero-frequency branch should be filtered"

    def test_probability_rounding_precision(self):
        """
        Edge Case: Probabilities that don't divide evenly

        Given: Frequencies that create repeating decimals (1/3)
        When: Calculating probabilities
        Then: Rounded appropriately (2 decimal places)
        """
        # Arrange
        from branching_analysis import build_decision_tree
        uneven_data = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 1},
                    "/rca": {"frequency": 1},
                    "/release": {"frequency": 1}
                }
            }
        }

        # Act
        tree = build_decision_tree(uneven_data)

        # Assert
        branches = tree["/dev"]["branches"]
        for branch in branches:
            # Each should be ~0.33 (33.33%)
            prob = branch["probability"]
            assert abs(prob - 0.33) < 0.01 or abs(prob - 0.34) < 0.01, \
                f"Probability should be ~33%, got {prob}"

    def test_large_frequency_values(self):
        """
        Edge Case: Very large frequency values

        Given: Frequencies in the thousands
        When: Building decision tree
        Then: Probabilities calculated correctly
        """
        # Arrange
        from branching_analysis import build_decision_tree
        large_frequency_data = {
            "/dev": {
                "downstream": {
                    "/qa": {"frequency": 10000},
                    "/rca": {"frequency": 5000}
                }
            }
        }

        # Act
        tree = build_decision_tree(large_frequency_data)

        # Assert
        branches = tree["/dev"]["branches"]
        qa_prob = next(b["probability"] for b in branches if b["command"] == "/qa")
        rca_prob = next(b["probability"] for b in branches if b["command"] == "/rca")

        # 10000/(10000+5000) = 0.667
        assert abs(qa_prob - 0.667) < 0.01, \
            f"/qa probability should be ~66.7%, got {qa_prob}"
        # 5000/(10000+5000) = 0.333
        assert abs(rca_prob - 0.333) < 0.01, \
            f"/rca probability should be ~33.3%, got {rca_prob}"


# ============================================================================
# Output Format Tests
# ============================================================================

@pytest.mark.unit
class TestDecisionTreeOutput:
    """Tests for decision tree output formatting"""

    def test_tree_json_serializable(self, branching_points_input):
        """
        Test: Decision tree is JSON serializable

        Given: Valid decision tree
        When: Serializing to JSON
        Then: No serialization errors
        """
        # Arrange
        from branching_analysis import build_decision_tree

        # Act
        tree = build_decision_tree(branching_points_input)

        # Assert
        try:
            json_str = json.dumps(tree)
            parsed = json.loads(json_str)
            assert parsed == tree, "Serialized tree should match original"
        except (TypeError, ValueError) as e:
            pytest.fail(f"Decision tree should be JSON serializable: {e}")

    def test_format_tree_human_readable(self, branching_points_input):
        """
        Test: Decision tree can be formatted for human readability

        Given: Decision tree structure
        When: Formatting for display
        Then: Output is human-readable string
        """
        # Arrange
        from branching_analysis import format_decision_tree

        # Act
        formatted = format_decision_tree(branching_points_input)

        # Assert
        assert isinstance(formatted, str), "Formatted output should be string"
        assert len(formatted) > 0, "Formatted output should not be empty"
        # Should contain arrow notation
        assert "->" in formatted, "Should use arrow notation"
        # Should contain percentage
        assert "%" in formatted, "Should include percentage"

    def test_format_includes_or_for_multiple_branches(self, branching_points_input):
        """
        Test: Format uses 'or' for multiple branches per spec

        Spec: "command A -> command B (70%) or command C (30%)"

        Given: Multiple branches
        When: Formatting
        Then: Uses 'or' to separate options
        """
        # Arrange
        from branching_analysis import format_decision_tree

        # Act
        formatted = format_decision_tree(branching_points_input)

        # Assert
        # For commands with multiple branches, should use 'or'
        assert "or" in formatted.lower(), \
            "Multiple branches should be separated by 'or'"


# ============================================================================
# Integration with AC#1 Tests
# ============================================================================

@pytest.mark.integration
class TestDecisionTreeIntegration:
    """Integration tests with AC#1 branching detection"""

    def test_tree_built_from_detection_output(self, branching_points_input):
        """
        Test: Decision tree accepts output from detect_branching_points

        Given: Output from AC#1 branching detection
        When: Passing to build_decision_tree
        Then: Tree is built without errors
        """
        # Arrange
        from branching_analysis import detect_branching_points, build_decision_tree
        raw_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        ]

        # Act
        branching = detect_branching_points(raw_data)
        tree = build_decision_tree(branching)

        # Assert
        assert isinstance(tree, dict), "Tree should be a dictionary"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
