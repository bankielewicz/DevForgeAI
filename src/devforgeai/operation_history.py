"""
Operation History Tracking

Maintains history of operations and their associated feedback sessions.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import json
from pathlib import Path


class OperationHistory:
    """In-memory operation history store (for testing)."""

    _storage: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def get(cls, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get operation history by ID."""
        return cls._storage.get(operation_id)

    @classmethod
    def set(cls, operation_id: str, history: Dict[str, Any]) -> None:
        """Set operation history."""
        cls._storage[operation_id] = history

    @classmethod
    def update(cls, operation_id: str, **kwargs) -> None:
        """Update operation history fields."""
        if operation_id not in cls._storage:
            cls._storage[operation_id] = {}
        cls._storage[operation_id].update(kwargs)

    @classmethod
    def clear(cls) -> None:
        """Clear all history (for testing)."""
        cls._storage.clear()

    @classmethod
    def query(cls, **filters) -> list[Dict[str, Any]]:
        """
        Query operations by criteria.

        Args:
            feedback_linked: bool - Only return operations with feedback
            status: str - Filter by status
        """
        results = []
        for op_id, history in cls._storage.items():
            match = True
            if "feedback_linked" in filters:
                has_feedback = "feedback_session_id" in history and bool(history["feedback_session_id"])
                if filters["feedback_linked"] != has_feedback:
                    match = False
            if "status" in filters:
                if history.get("status") != filters["status"]:
                    match = False
            if match:
                results.append({"operation_id": op_id, **history})
        return results


def update_operation_history(
    operation_id: str,
    feedback_session_id: Optional[str] = None,
    feedback_status: Optional[str] = None,
    collection_timestamp: Optional[str] = None,
    initiated_by: Optional[str] = None,
    initiated_at: Optional[str] = None,
) -> None:
    """
    Update operation history with feedback link.

    Args:
        operation_id: UUID of operation
        feedback_session_id: UUID of feedback session
        feedback_status: Status (initiated, collected, etc.)
        collection_timestamp: When feedback was collected
        initiated_by: Who initiated the feedback
        initiated_at: When feedback was initiated
    """
    # Get or create history entry
    history = OperationHistory.get(operation_id) or {}

    # Update fields
    if feedback_session_id:
        history["feedback_session_id"] = feedback_session_id
    if feedback_status:
        history["feedback_status"] = feedback_status
    if collection_timestamp:
        history["collection_timestamp"] = collection_timestamp
    if initiated_by:
        history["initiated_by"] = initiated_by
    if initiated_at:
        history["initiated_at"] = initiated_at

    # Always update last modified
    history["last_updated"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Create audit trail entry if needed
    if "audit_trail" not in history:
        history["audit_trail"] = []

    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "action": "feedback_linked",
        "feedback_session_id": feedback_session_id,
    }
    if initiated_by:
        audit_entry["initiated_by"] = initiated_by

    history["audit_trail"].append(audit_entry)

    # Store back
    OperationHistory.set(operation_id, history)


# Backward compatibility alias (camelCase - deprecated)
updateOperationHistory = update_operation_history
