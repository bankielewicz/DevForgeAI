"""
Test Fixture: Unused Imports Vulnerable Pattern (Python)

This file contains import statements that are never used.
Expected detections: >=2 violations for AP-007
Rule ID: AP-007
Severity: MEDIUM (info)
"""

import os  # USED - referenced below
import sys  # UNUSED - VULNERABLE
import json  # UNUSED - VULNERABLE
import logging  # UNUSED - VULNERABLE
from typing import List, Dict, Optional  # Dict and Optional UNUSED - VULNERABLE
from pathlib import Path  # UNUSED - VULNERABLE


def get_current_directory():
    """Get current working directory."""
    return os.getcwd()  # Only 'os' is used


def process_items(items: List[str]) -> List[str]:
    """Process items - only List from typing is used."""
    return [item.upper() for item in items]
