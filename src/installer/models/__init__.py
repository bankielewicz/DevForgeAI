"""
Models for CLAUDE.md merge operations.

Provides dataclasses for:
- MergeStatus (enum)
- MergeResult (result object)
- ConflictDetail (conflict information)
"""

from .merge_result import MergeStatus, MergeResult
from .conflict_detail import ConflictDetail

__all__ = ["MergeStatus", "MergeResult", "ConflictDetail"]
