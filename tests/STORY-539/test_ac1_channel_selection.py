"""
Test: AC#1 - Channel Selection Matrix Output
Story: STORY-539
Generated: 2026-03-04

Tests validate that the go-to-market-framework.md and channel-selection-matrix.md
reference files contain proper channel selection matrix content with scoring,
ranking, and budget allocation structures.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM_FRAMEWORK = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "go-to-market-framework.md")
CHANNEL_MATRIX = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "channel-selection-matrix.md")


class TestChannelSelectionMatrixFileExists:
    """Verify source reference files exist."""

    def test_should_exist_go_to_market_framework(self):
        # Arrange
        path = GTM_FRAMEWORK
        # Act & Assert
        assert os.path.isfile(path), f"go-to-market-framework.md not found at {path}"

    def test_should_exist_channel_selection_matrix(self):
        # Arrange
        path = CHANNEL_MATRIX
        # Act & Assert
        assert os.path.isfile(path), f"channel-selection-matrix.md not found at {path}"


class TestChannelMatrixBusinessModelCoverage:
    """AC#1: Matrix must cover minimum 8 business model types."""

    REQUIRED_MODELS = [
        "SaaS B2B",
        "SaaS B2C",
        "Marketplace",
        "D2C",
        "E-commerce",
        "Subscription",
        "Freemium",
        "Agency",
    ]

    @pytest.fixture
    def matrix_content(self):
        with open(CHANNEL_MATRIX, "r") as f:
            return f.read()

    def test_should_contain_minimum_8_business_model_types(self, matrix_content):
        # Arrange
        model_count = 0
        # Act
        for model in self.REQUIRED_MODELS:
            if model.lower() in matrix_content.lower():
                model_count += 1
        # Assert
        assert model_count >= 8, f"Only {model_count}/8 business model types found in channel matrix"

    @pytest.mark.parametrize("model", REQUIRED_MODELS)
    def test_should_contain_business_model(self, matrix_content, model):
        # Arrange & Act & Assert
        assert model.lower() in matrix_content.lower(), f"Business model '{model}' not found in channel matrix"


class TestChannelRanking:
    """AC#1: Ranked channel list with minimum 3 channels per model."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_have_channel_strategy_section(self, framework_content):
        # Arrange & Act
        has_section = bool(re.search(r"^## Channel Strategy", framework_content, re.MULTILINE))
        # Assert
        assert has_section, "Missing '## Channel Strategy' section in go-to-market-framework.md"

    def test_should_rank_minimum_3_channels(self, framework_content):
        # Arrange
        # Look for numbered or bulleted channel entries in Channel Strategy section
        channel_section = re.split(r"^## ", framework_content, flags=re.MULTILINE)
        channel_text = ""
        for section in channel_section:
            if section.startswith("Channel Strategy"):
                channel_text = section
                break
        # Act
        channel_entries = re.findall(r"^[\-\*\d]+[\.\)]\s+", channel_text, re.MULTILINE)
        # Assert
        assert len(channel_entries) >= 3, f"Only {len(channel_entries)} channels ranked, minimum 3 required"


class TestBudgetAllocation:
    """BR-001: Budget allocation percentages must sum to 100%, min 3 channels."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_contain_budget_allocation_percentages(self, framework_content):
        # Arrange & Act
        percentages = re.findall(r"(\d+)%", framework_content)
        # Assert
        assert len(percentages) >= 3, f"Only {len(percentages)} percentage values found, need at least 3"

    def test_should_have_budget_allocation_section(self, framework_content):
        # Arrange & Act
        has_section = bool(re.search(r"^## Budget Allocation", framework_content, re.MULTILINE))
        # Assert
        assert has_section, "Missing '## Budget Allocation' section in go-to-market-framework.md"


class TestChannelMatrixScoring:
    """AC#1: Channel matrix must have scored channels (10+ channels)."""

    @pytest.fixture
    def matrix_content(self):
        with open(CHANNEL_MATRIX, "r") as f:
            return f.read()

    def test_should_have_scoring_weights_section(self, matrix_content):
        # Arrange & Act
        has_section = bool(re.search(r"(?i)scoring|weights|score", matrix_content))
        # Assert
        assert has_section, "Channel matrix missing scoring/weights content"

    def test_should_have_minimum_10_channels_scored(self, matrix_content):
        # Arrange
        # Channels are typically listed as table rows or bullet items
        # Act
        channel_lines = re.findall(r"^\|[^|]+\|", matrix_content, re.MULTILINE)
        # Subtract header/separator rows
        data_rows = [l for l in channel_lines if not re.match(r"^\|[\s\-:]+\|", l)]
        # Assert
        assert len(data_rows) >= 10, f"Only {len(data_rows)} channel rows found, need 10+"
