"""
Tests for STORY-137: Resume-from-Checkpoint Logic for Ideation Sessions

This test package provides comprehensive test coverage for:
- AC#1: Checkpoint Detection at Session Start
- AC#2: Resume vs Fresh Start User Choice
- AC#3: Checkpoint File Loading and Validation
- AC#4: Phase Replay with Pre-filled Answers
- AC#5: Resume from Last Incomplete Phase
- AC#6: Multi-Checkpoint Selection (Multiple Sessions)

Test modules:
- test_checkpoint_detector.py - AC#1 tests
- test_resume_choice.py - AC#2 tests
- test_checkpoint_loader.py - AC#3 tests
- test_phase_replay.py - AC#4, AC#5 tests
- test_multi_checkpoint.py - AC#6 tests
- test_integration.py - End-to-end resume workflow
"""
