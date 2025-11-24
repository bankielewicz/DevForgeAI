"""
Test package for anti-pattern-scanner subagent (STORY-062).

This package contains comprehensive tests for the anti-pattern-scanner subagent
implementation, covering all 12 acceptance criteria plus integration tests.

Test Organization:
- AC1: Subagent Specification (6 tests)
- AC2: Library Substitution Detection (6 tests)
- AC3: Structure Violations Detection (4 tests)
- AC4: Layer Violations Detection (5 tests)
- AC5: Code Smells Detection (5 tests)
- AC6: Security Vulnerabilities Detection (7 tests)
- AC7: Severity-Based Blocking Logic (6 tests)
- AC8: Evidence-Based Reporting (7 tests)
- AC9: QA Integration (6 tests)
- AC10: Prompt Template Documentation (6 tests)
- AC11: Full Detection Coverage (7 tests)
- AC12: Error Handling (8 tests)
- Integration Tests (5 tests)
- Edge Cases (5 tests)

Total: 91 test scenarios

Test Status: RED (all failing - ready for implementation)

Run Tests:
  pytest tests/subagent_anti_pattern_scanner/ -v
  pytest tests/subagent_anti_pattern_scanner/test_anti_pattern_scanner.py::TestAC1SubagentSpecification -v
"""
