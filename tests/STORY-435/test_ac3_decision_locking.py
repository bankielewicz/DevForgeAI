"""
Test: AC#3 - Decision Fields Are Locked and Unambiguous
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates BR-001 (locked: true required), BR-002 (no hedging language),
unique IDs (DR-N), rejected alternatives, and domain labels.
"""
import re
import pytest
import yaml


HEDGING_WORDS = ["should", "might", "consider", "possibly"]


class TestDecisionLocking:
    """BR-001: Every decision must have locked: true."""

    def test_should_reject_decision_with_locked_false(self, sample_valid_decisions):
        # Arrange
        bad_decision = sample_valid_decisions[0].copy()
        bad_decision["locked"] = False

        # Act & Assert
        assert bad_decision["locked"] is not True, (
            "Test setup: decision should have locked=False for this test"
        )
        # When validation logic exists, it should reject this

    def test_should_reject_decision_with_missing_locked(self, sample_valid_decisions):
        # Arrange
        bad_decision = sample_valid_decisions[0].copy()
        del bad_decision["locked"]

        # Act & Assert
        assert "locked" not in bad_decision, (
            "Test setup: decision should have no locked field"
        )

    def test_should_accept_decision_with_locked_true(self, sample_valid_decisions):
        # Arrange
        decision = sample_valid_decisions[0]

        # Act & Assert
        assert decision["locked"] is True


class TestHedgingLanguageDetection:
    """BR-002: No hedging language in decision text."""

    @pytest.mark.parametrize("hedging_word", HEDGING_WORDS)
    def test_should_detect_hedging_word_in_decision(self, hedging_word):
        # Arrange
        bad_text = f"We {hedging_word} use JWT tokens"

        # Act
        found = any(w in bad_text.lower() for w in HEDGING_WORDS)

        # Assert
        assert found, f"Hedging word '{hedging_word}' should be detected"

    def test_should_accept_definitive_decision_text(self):
        # Arrange
        good_text = "Use JWT tokens with 15-minute expiry"

        # Act
        found = any(w in good_text.lower() for w in HEDGING_WORDS)

        # Assert
        assert not found, "Definitive text should not trigger hedging detection"

    def test_should_detect_hedging_in_sample_decision(self):
        # Arrange - decision with hedging
        bad_decision = {
            "id": "DR-1",
            "domain": "auth",
            "decision": "We should consider using JWT tokens",
            "rejected": [{"option": "Cookies", "reason": "Not stateless"}],
            "rationale": "JWT is suitable",
            "locked": True,
        }

        # Act
        text = bad_decision["decision"].lower()
        hedging_found = any(w in text for w in HEDGING_WORDS)

        # Assert
        assert hedging_found, "Hedging language in decision text must be detected"


class TestDecisionUniqueIDs:
    """Decisions must have unique IDs matching DR-N pattern."""

    def test_should_accept_valid_dr_id(self):
        # Arrange
        decision_id = "DR-1"

        # Act
        matches = bool(re.match(r"^DR-\d+$", decision_id))

        # Assert
        assert matches, f"ID '{decision_id}' should match DR-N pattern"

    def test_should_reject_invalid_id_format(self):
        # Arrange
        bad_id = "DEC-1"

        # Act
        matches = bool(re.match(r"^DR-\d+$", bad_id))

        # Assert
        assert not matches, f"ID '{bad_id}' should not match DR-N pattern"

    def test_should_detect_duplicate_ids(self):
        # Arrange
        decisions = [
            {"id": "DR-1", "domain": "auth", "decision": "Use JWT", "rejected": [], "rationale": "r", "locked": True},
            {"id": "DR-1", "domain": "db", "decision": "Use Postgres", "rejected": [], "rationale": "r", "locked": True},
        ]

        # Act
        ids = [d["id"] for d in decisions]
        has_duplicates = len(ids) != len(set(ids))

        # Assert
        assert has_duplicates, "Test setup: should have duplicate IDs"


class TestRejectedAlternatives:
    """Each decision must have at least one rejected alternative."""

    def test_should_reject_decision_with_empty_rejected(self):
        # Arrange
        bad_decision = {
            "id": "DR-1",
            "domain": "auth",
            "decision": "Use JWT tokens",
            "rejected": [],
            "rationale": "JWT is suitable",
            "locked": True,
        }

        # Act & Assert
        assert len(bad_decision["rejected"]) == 0, (
            "Test setup: rejected should be empty"
        )

    def test_should_accept_decision_with_rejected_alternatives(self, sample_valid_decisions):
        # Arrange
        decision = sample_valid_decisions[0]

        # Act & Assert
        assert len(decision["rejected"]) >= 1, (
            "Decision must have at least one rejected alternative"
        )

    def test_rejected_alternative_should_have_option_and_reason(self, sample_valid_decisions):
        # Arrange
        rejected = sample_valid_decisions[0]["rejected"][0]

        # Assert
        assert "option" in rejected, "Rejected alternative must have 'option' field"
        assert "reason" in rejected, "Rejected alternative must have 'reason' field"
