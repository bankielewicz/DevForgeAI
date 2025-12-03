"""
Configuration constants for pre-flight validation.

Defines thresholds and settings for all validation checks.
"""

# Python version requirements
MIN_PYTHON_VERSION = "3.10"

# Disk space requirements (in MB)
MIN_DISK_SPACE_MB = 100

# Timeout for subprocess checks (in seconds)
CHECK_TIMEOUT_SECONDS = 5

# Python executables to try (in priority order)
PYTHON_EXECUTABLES = ["python3", "python", "python3.11", "python3.10"]
