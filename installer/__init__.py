"""
Version-aware installer framework for DevForgeAI with backup and rollback capability.

This package provides automated installation, upgrade, and rollback functionality
for the DevForgeAI framework, ensuring atomic operations with backup/restore.

Modules:
- version: Version detection and semantic version comparison
- backup: Automated backup creation with integrity verification
- deploy: Framework file deployment with exclusions and permissions
- rollback: Backup listing and restore operations
- validate: Installation validation and health checks
- install: Main orchestrator for all installation modes
"""

__version__ = "1.0.0"
