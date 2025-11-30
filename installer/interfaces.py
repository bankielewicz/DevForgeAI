"""
Interfaces for dependency injection and clean architecture.

This module provides abstract interfaces for:
- Network detection (INetworkDetector)
- Bundle validation (IBundleValidator)

Following architecture-constraints.md: Layer abstraction through interfaces
prevents tight coupling to concrete implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class INetworkDetector(ABC):
    """
    Interface for network availability detection.

    Abstracts network checking logic to support:
    - Testing with mock implementations
    - Alternative detection strategies (DNS, HTTP, ICMP)
    - Dependency injection in offline installer
    """

    @abstractmethod
    def check_network_availability(self, timeout: int = 2) -> bool:
        """
        Check if network is available.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            bool: True if network available, False if offline
        """
        pass


class IBundleValidator(ABC):
    """
    Interface for bundle structure and integrity validation.

    Abstracts bundle validation logic to support:
    - Testing with mock bundles
    - Alternative validation strategies
    - Dependency injection in installer
    """

    @abstractmethod
    def verify_bundle_structure(self, bundle_root: Path) -> dict:
        """
        Verify bundle contains required directory structure.

        Args:
            bundle_root: Root path of bundled directory

        Returns:
            dict with status, file_count, missing_components

        Raises:
            FileNotFoundError: If critical components missing
        """
        pass

    @abstractmethod
    def verify_bundle_integrity(self, bundle_root: Path) -> dict:
        """
        Verify bundle integrity using checksums.

        Args:
            bundle_root: Root path of bundled directory

        Returns:
            dict with status, files_verified, all_valid, mismatches, failures

        Raises:
            FileNotFoundError: If checksums.json missing
            ValueError: If tamper detected (3+ failures)
        """
        pass

    @abstractmethod
    def validate_bundle_path(self, bundle_path: str) -> Path:
        """
        Validate and sanitize bundle path (prevent path traversal).

        Args:
            bundle_path: User-supplied bundle path string

        Returns:
            Path: Validated absolute path

        Raises:
            ValueError: If path contains invalid characters or traversal attempts
        """
        pass
