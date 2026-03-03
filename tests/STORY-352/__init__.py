"""
Test suite for STORY-352: Add Treelint Binary to Installer Distribution

This package contains tests for all 6 acceptance criteria:

- AC#1: test_ac1_binary_structure.py
    Treelint Binary Added to src/ Distribution Structure

- AC#2: test_ac2_installer_deploy.py
    Installer Deploys Binary to Appropriate Location

- AC#3: test_ac3_permissions.py
    Binary Permissions Set Correctly

- AC#4: test_ac4_checksum.py
    Checksum Validation for Integrity

- AC#5: test_ac5_existing_binary.py
    Graceful Handling if Binary Already Exists

- AC#6: test_ac6_source_tree.py
    source-tree.md Updated with Binary Location

Run all tests:
    pytest tests/STORY-352/ -v

Run specific AC tests:
    pytest tests/STORY-352/test_ac1_binary_structure.py -v
"""
