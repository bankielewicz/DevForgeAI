"""
Network detection and availability checking for offline installation support.

This module provides:
- Network availability detection with configurable timeout
- Socket-based connection checking (no external dependencies)
- Graceful handling of network failures
- INetworkDetector interface implementation (clean architecture)

Classes:
- SocketNetworkDetector: Concrete implementation using socket connection test

Functions:
- check_network_availability(timeout: int = 2) -> bool
- display_network_status(is_online: bool) -> None

Dependencies: Standard library only (socket, sys)
"""

import socket
import sys
from .interfaces import INetworkDetector

# Configuration constants
NETWORK_CHECK_HOST = "8.8.8.8"
NETWORK_CHECK_PORT = 53
NETWORK_CHECK_TIMEOUT = 2
DISK_SPACE_REQUIRED_MB = 200
MIN_PYTHON_VERSION = (3, 8)

# Dependency-specific warnings
MISSING_DEPENDENCY_MESSAGES = {
    "python": {
        "display_name": "Python CLI",
        "reason_template": "{}",
        "impact": "CLI validation commands unavailable",
        "mitigation": "Install Python 3.8+ and re-run installation"
    }
}


class SocketNetworkDetector(INetworkDetector):
    """
    Concrete implementation of INetworkDetector using socket connections.

    ARCHITECTURE: Implements INetworkDetector interface (HIGH violation #2 fix)
    to enable dependency injection and testing.

    Uses DNS server connection test (8.8.8.8:53) as reliable network check.
    Port 53 commonly allowed through firewalls.
    """

    def __init__(self, host: str = NETWORK_CHECK_HOST, port: int = NETWORK_CHECK_PORT):
        """
        Initialize network detector with target host/port.

        Args:
            host: Target hostname or IP address (default: Google DNS 8.8.8.8)
            port: Target port (default: 53 for DNS)
        """
        self.host = host
        self.port = port

    def check_network_availability(self, timeout: int = 2) -> bool:
        """
        Check network availability using socket connection test.

        Tests connection to configured DNS server.
        Uses configurable timeout for air-gapped environments.

        Args:
            timeout: Connection timeout in seconds (default: 2)

        Returns:
            bool: True if network available, False if offline/timeout

        Examples:
            >>> detector = SocketNetworkDetector()
            >>> is_online = detector.check_network_availability(timeout=2)
            >>> if is_online:
            ...     print("Online mode - update checks enabled")
        """
        try:
            # Attempt connection to DNS server
            socket.create_connection((self.host, self.port), timeout=timeout)
            return True
        except (socket.timeout, socket.error, OSError):
            # Network unavailable, timeout, or permission denied
            return False


def check_network_availability(timeout: int = 2) -> bool:
    """
    Check network availability using socket connection test.

    ARCHITECTURE: Delegates to SocketNetworkDetector (interface implementation)
    for clean architecture and testability.

    Tests connection to reliable public DNS servers (8.8.8.8:53).
    Uses configurable timeout for air-gapped environments.

    Args:
        timeout: Connection timeout in seconds (default: 2)

    Returns:
        bool: True if network available, False if offline/timeout

    Examples:
        >>> is_online = check_network_availability(timeout=2)
        >>> if is_online:
        ...     print("Online mode - update checks enabled")
        ... else:
        ...     print("Offline mode - using bundled files only")
    """
    # Use concrete implementation (can be swapped via dependency injection)
    detector = SocketNetworkDetector()
    return detector.check_network_availability(timeout=timeout)


def display_network_status(is_online: bool) -> None:
    """
    Display network status message to user.

    Shows clear indication of online vs offline mode with appropriate
    messaging for air-gapped environments.

    Args:
        is_online: True if network available, False if offline

    Output:
        Prints status message to stdout

    Examples:
        >>> display_network_status(is_online=True)
        Network Status: Online

        >>> display_network_status(is_online=False)
        Network Status: Offline - Air-gapped mode
        Using bundled files only (no internet connection required)
    """
    if is_online:
        print("Network Status: Online")
    else:
        print("Network Status: Offline - Air-gapped mode")
        print("Using bundled files only (no internet connection required)")


def warn_network_feature_unavailable(
    feature_name: str,
    reason: str,
    impact: str = None,
    enable_command: str = None
) -> None:
    """
    Display warning for network-dependent features that cannot run offline.

    Provides clear messaging about:
    - What feature is unavailable
    - Why it requires network
    - Impact of skipping
    - How to enable later when online

    Args:
        feature_name: Name of unavailable feature (e.g., "Update Check")
        reason: Why network is required (e.g., "Requires GitHub API access")
        impact: Impact of skipping (optional)
        enable_command: Command to run later when online (optional)

    Output:
        Prints formatted warning to stdout

    Examples:
        >>> warn_network_feature_unavailable(
        ...     feature_name="Update Check",
        ...     reason="Requires GitHub API access",
        ...     impact="You won't receive update notifications",
        ...     enable_command="devforgeai update --check"
        ... )
        ⚠ Network-Dependent Feature Unavailable: Update Check
        Reason: Requires GitHub API access
        Impact: You won't receive update notifications
        Enable later: devforgeai update --check
    """
    print(f"\n⚠ Network-Dependent Feature Unavailable: {feature_name}")
    print(f"Reason: {reason}")

    if impact:
        print(f"Impact: {impact}")

    if enable_command:
        print(f"Enable later: {enable_command}")

    print()  # Blank line for readability


def detect_python_version() -> tuple[int, int] | None:
    """
    Detect Python version for CLI installation compatibility.

    Checks if Python 3.8+ is available for CLI tools installation.

    Returns:
        tuple[int, int]: (major, minor) version if Python available
        None: If Python not available or version < 3.8

    Examples:
        >>> version = detect_python_version()
        >>> if version and version >= (3, 8):
        ...     print(f"Python {version[0]}.{version[1]} detected")
        ... else:
        ...     print("Python 3.8+ not available")
    """
    try:
        major = sys.version_info.major
        minor = sys.version_info.minor

        if major >= 3 and minor >= 8:
            return (major, minor)
        else:
            return None
    except AttributeError:
        return None


def warn_missing_dependency(dependency: str, reason: str) -> None:
    """
    Display warning for missing optional dependencies.

    Used for graceful degradation when optional dependencies unavailable.
    Uses configuration-driven messaging for consistency.

    Args:
        dependency: Name of missing dependency (e.g., "python")
        reason: Why dependency is unavailable

    Output:
        Prints warning to stdout

    Examples:
        >>> warn_missing_dependency('python', reason='Python 3.8+ not found')
        ⚠ Optional Dependency Unavailable: Python CLI
        Reason: Python 3.8+ not found
        Impact: CLI validation commands unavailable
        Mitigation: Install Python 3.8+ and re-run installation
    """
    dependency_key = dependency.lower()
    messages = MISSING_DEPENDENCY_MESSAGES.get(dependency_key)

    if messages:
        print(f"\n⚠ Optional Dependency Unavailable: {messages['display_name']}")
        print(f"Reason: {reason}")
        print(f"Impact: {messages['impact']}")
        print(f"Mitigation: {messages['mitigation']}")
    else:
        print(f"\n⚠ Optional Dependency Unavailable: {dependency}")
        print(f"Reason: {reason}")

    print()  # Blank line


def check_disk_space(target_path, required_mb: int = DISK_SPACE_REQUIRED_MB) -> None:
    """
    Check available disk space before installation.

    Validates sufficient disk space exists for framework installation.
    Raises error if insufficient space (prevents partial installations).

    Args:
        target_path: Installation target directory path
        required_mb: Required space in megabytes (default: 200)

    Raises:
        RuntimeError: If insufficient disk space available or invalid input
        ValueError: If required_mb is negative

    Examples:
        >>> check_disk_space('/path/to/project', required_mb=200)
        # Passes if 200MB+ available

        >>> check_disk_space('/full/disk', required_mb=200)
        RuntimeError: Insufficient disk space: 50 MB available, 200 MB required
    """
    import shutil

    # Input validation
    if required_mb < 0:
        raise ValueError(f"required_mb must be non-negative, got {required_mb}")

    usage = shutil.disk_usage(target_path)
    available_mb = usage.free / (1024 * 1024)

    if available_mb < required_mb:
        raise RuntimeError(
            f"Insufficient disk space: {available_mb:.1f} MB available, "
            f"{required_mb} MB required"
        )


def check_git_available() -> None:
    """
    Check if Git is available in PATH.

    Validates Git installation before proceeding (required for DevForgeAI).

    Raises:
        RuntimeError: If Git not found in PATH

    Examples:
        >>> check_git_available()
        # Passes if git command available

        >>> check_git_available()  # Git not installed
        RuntimeError: Git is required for DevForgeAI but was not found in PATH
    """
    import shutil

    if shutil.which('git') is None:
        raise RuntimeError(
            "Git is required for DevForgeAI but was not found in PATH.\n"
            "Install Git: https://git-scm.com/downloads"
        )
