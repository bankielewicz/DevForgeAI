"""
STORY-149 Test Configuration

Ensures the installer package is in the Python path for test imports.
"""

import sys
from pathlib import Path

# Add project root to Python path so tests can import installer package
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
