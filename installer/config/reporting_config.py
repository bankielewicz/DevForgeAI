"""
Configuration for Installation Reporting & Logging (STORY-075).

Contains paths and thresholds for logging, manifest generation, and reporting.
"""

# Log file location (relative to installation target)
LOG_FILE_PATH = ".devforgeai/install.log"

# Manifest file location (relative to installation target)
MANIFEST_FILE_PATH = ".devforgeai/.install-manifest.json"

# Maximum log file size before rotation (in MB)
LOG_MAX_SIZE_MB = 10

# File count threshold for showing progress (show progress when > this value)
PROGRESS_THRESHOLD = 100

# Valid file categories for manifest entries
VALID_CATEGORIES = ["skill", "agent", "command", "memory", "script", "config"]

# Error type constants
ERROR_TYPES = {
    "PERMISSION_DENIED": "PERMISSION_DENIED",
    "FILE_NOT_FOUND": "FILE_NOT_FOUND",
    "CHECKSUM_MISMATCH": "CHECKSUM_MISMATCH",
    "GIT_ERROR": "GIT_ERROR",
    "VALIDATION_ERROR": "VALIDATION_ERROR",
    "DEPENDENCY_ERROR": "DEPENDENCY_ERROR",
    "UNKNOWN_ERROR": "UNKNOWN_ERROR",
}
