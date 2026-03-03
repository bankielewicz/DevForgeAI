"""
Test suite for coverage-analyzer subagent (STORY-061).

Coverage analyzer is a specialized subagent for test coverage analysis that:
- Detects language from tech-stack.md
- Maps language to appropriate coverage tool
- Classifies files by architectural layer (business_logic, application, infrastructure)
- Validates coverage against strict thresholds (95%/85%/80%)
- Identifies coverage gaps with file:line evidence
- Generates actionable remediation recommendations
- Integrates with devforgeai-qa skill Phase 1

This test suite covers all 9 acceptance criteria with:
- AC1 Tests (11 tests): Subagent specification file and structure
- AC2-AC6 Tests (27 tests): Language support, classification, thresholds, gaps, recommendations
- AC7-AC9 Tests (23 tests): QA integration, prompt template, error handling

Total: 61 unit tests (all FAIL initially in TDD Red phase)
"""
