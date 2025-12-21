# STORY-037 Test Quick Reference

**Red Phase Failing Tests for Pattern Compliance Auditor**

---

## Test Files at a Glance

### 1. Fixtures (`command_fixtures.py`)
**861 lines**

Seven mock command files representing different patterns:

```python
FIXTURES = {
    'compliant': 0 violations, <12K chars ✅
    'moderate': 5 violations, <15K chars ⚠️
    'severe': 15+ violations, >15K chars ❌
    'malformed': Invalid YAML frontmatter ❌
    'bypass': 2 direct subagent bypasses ❌
    'templates': 180 lines of templates ⚠️
    'minimal': Minimal valid command ✅
}
```

---

### 2. Unit Tests (`test_pattern_compliance_auditor.py`)
**883 lines, 41 tests**

Tests individual functionality of the auditor:

```
TestViolationDetection (12 tests)
├─ business_logic violations (2 tests)
├─ templates violations (2 tests)
├─ parsing violations (2 tests)
├─ decision_making violations (2 tests)
├─ error_recovery violations (2 tests)
└─ direct_subagent_bypass violations (2 tests)

TestViolationAccuracy (3 tests)
├─ Line number accuracy (±0 lines)
├─ Code snippets included
└─ Recommendations present

TestBudgetClassification (5 tests)
├─ COMPLIANT classification
├─ WARNING classification
├─ OVER classification
├─ Percentage calculation
└─ Boundary testing

TestViolationCategorization (4 tests)
├─ Group by type
├─ Count by type
├─ Count by severity
└─ Frequency analysis

TestEffortEstimation (5 tests)
├─ 0 effort for compliant
├─ 2-3 hours for moderate
├─ 3-5 hours for severe
├─ Consistency check
└─ Scaling validation

TestPriorityQueue (3 tests)
├─ Correct ordering
├─ Effort estimates included
└─ Priority categories (P1/P2/P3)

TestEdgeCases (8 tests)
├─ Empty content
├─ Minimal command
├─ Malformed YAML
├─ Multiple violation types
├─ No false positives
├─ Immutability
├─ Very large files (10K+ lines)
└─ Unicode handling

TestFixtureValidation (4 tests)
├─ Compliant fixture validation
├─ Moderate fixture validation
├─ Severe fixture validation
└─ Bypass fixture validation

TestReportGeneration (3 tests)
├─ Summary section included
├─ JSON serializable
└─ Violations included
```

---

### 3. Integration Tests (`test_pattern_compliance_integration.py`)
**609 lines, 32 tests**

Tests complete workflows and end-to-end scenarios:

```
TestEndToEndAuditWorkflow (6 tests)
├─ Single command complete workflow
├─ Multiple commands parallel audit
├─ Markdown summary generation
├─ JSON report generation
├─ Actionable roadmap creation
└─ Priority-based roadmap ordering

TestViolationCategorization (3 tests)
├─ Group by type in report
├─ Group by severity in report
└─ Frequency analysis

TestRoadmapGeneration (4 tests)
├─ CRITICAL priority identification
├─ Total effort calculation
├─ Dependency identification
└─ Actionable recommendations

TestBudgetAnalysis (4 tests)
├─ Budget status in report
├─ Budget percentage in report
├─ Character count accuracy
└─ Over-budget flagging

TestComplexScenarios (4 tests)
├─ Audit all fixtures
├─ Mixed compliant/non-compliant
├─ Consistent ordering
└─ Incremental improvement tracking

TestReportFormatting (3 tests)
├─ Markdown readability
├─ JSON required fields
└─ Violation details

TestErrorHandling (3 tests)
├─ Malformed YAML handling
├─ Empty content handling
└─ Very large files (100K chars)

TestConsistency (3 tests)
├─ Deterministic violations
├─ Deterministic budget classification
└─ Deterministic effort estimation
```

---

## Coverage Matrix

### By Acceptance Criteria

| AC | Description | # Tests |
|---|---|---|
| AC-1 | Pattern Violation Detection | 15 |
| AC-2 | Skill Invocation Validation | 3 |
| AC-3 | Budget Compliance Check | 9 |
| AC-4 | Violation Categorization | 11 |
| AC-5 | Actionable Roadmap | 9 |

### By Violation Type (6 Types × 3 Scenarios = 18 Core Tests)

| Type | Unit | Integration | Total |
|---|---|---|---|
| business_logic | 2 | 1 | 3 |
| templates | 2 | 1 | 3 |
| parsing | 2 | 1 | 3 |
| decision_making | 2 | 1 | 3 |
| error_recovery | 2 | 1 | 3 |
| direct_subagent_bypass | 2 | 1 | 3 |

---

## Key Test Assertions

### Violation Detection

```python
# Detect violation type
assert v.type == ViolationType.BUSINESS_LOGIC

# Verify severity
assert v.severity == ViolationSeverity.HIGH

# Check line number accuracy
assert v.line_number == 4  # ±0 accuracy

# Code snippet included
assert len(v.code_snippet) > 0

# Recommendation present
assert len(v.recommendation) > 0
```

### Budget Classification

```python
# Compliant boundary
assert classify_budget("x" * 11999) == COMPLIANT
assert classify_budget("x" * 12000) == WARNING
assert classify_budget("x" * 15000) == OVER

# Percentage calculation
percentage = (len(content) / 15000) * 100
assert percentage == expected
```

### Effort Estimation

```python
# Compliant: 0 hours
assert estimate_effort(compliant_content) == 0

# Moderate: 2-3 hours
assert 2 <= estimate_effort(moderate_content) <= 3

# Severe: 3-5 hours
assert 3 <= estimate_effort(severe_content) <= 5

# Consistency
assert estimate_effort(content) == estimate_effort(content)
```

### Report Generation

```python
# Required fields
assert 'command' in report
assert 'summary' in report
assert 'violations' in report
assert 'budget' in report
assert 'roadmap' in report

# JSON serializable
json_str = json.dumps(report)
parsed = json.loads(json_str)
assert parsed == report
```

### Roadmap Generation

```python
# Priority ordering (CRITICAL → HIGH → MEDIUM → LOW)
assert roadmap[0]['priority'] in ['CRITICAL', 'HIGH']
assert roadmap[-1]['priority'] in ['MEDIUM', 'LOW']

# Effort estimates
for item in roadmap:
    assert item['effort_hours'] > 0

# Actionable recommendations
for item in roadmap:
    assert len(item['recommendations']) > 0
```

---

## Expected Red Phase Output

When running tests before implementation:

```bash
$ pytest tests/ -v

tests/unit/test_pattern_compliance_auditor.py::TestViolationDetection::test_detect_business_logic_violation_simple FAILED
    ModuleNotFoundError: No module named 'devforgeai.auditors.pattern_compliance_auditor'

tests/unit/test_pattern_compliance_auditor.py::TestViolationDetection::test_detect_templates_violation_single FAILED
    ModuleNotFoundError: No module named 'devforgeai.auditors.pattern_compliance_auditor'

[... 71 more failures ...]

======================== 73 failed in 12.34s =========================
```

This is **EXPECTED and CORRECT** for TDD Red phase.

---

## Implementation Checklist (Green Phase)

Implement to make tests pass:

- [ ] Create `devforgeai/auditors/__init__.py`
- [ ] Create `devforgeai/auditors/pattern_compliance_auditor.py`
- [ ] Implement `PatternComplianceAuditor` class
- [ ] Implement `Violation` dataclass (frozen)
- [ ] Implement `ViolationType` enum (6 types)
- [ ] Implement `ViolationSeverity` enum (4 levels)
- [ ] Implement `BudgetClassification` enum (3 levels)
- [ ] Implement `detect_violations()` method
  - [ ] Detect business_logic patterns
  - [ ] Detect templates patterns
  - [ ] Detect parsing patterns
  - [ ] Detect decision_making patterns
  - [ ] Detect error_recovery patterns
  - [ ] Detect direct_subagent_bypass patterns
- [ ] Implement `classify_budget()` method
- [ ] Implement `calculate_budget_percentage()` method
- [ ] Implement `estimate_effort()` method
- [ ] Implement `group_by_type()` method
- [ ] Implement `count_by_severity()` method
- [ ] Implement `generate_priority_queue()` method
- [ ] Implement `generate_report()` method
- [ ] Implement `generate_markdown_summary()` method
- [ ] Implement `generate_roadmap()` method
- [ ] Run tests: `pytest tests/ -v`
- [ ] Expected: All 73 tests PASS

---

## Test Execution Commands

### Quick Test
```bash
# Run just unit tests
pytest tests/unit/test_pattern_compliance_auditor.py -v

# Run just integration tests
pytest tests/integration/test_pattern_compliance_integration.py -v
```

### Full Test
```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with short traceback
pytest tests/ -v --tb=short

# Run with coverage report
pytest tests/ -v --cov=devforgeai.auditors.pattern_compliance_auditor --cov-report=html
```

### Specific Test Class
```bash
# Run only violation detection tests
pytest tests/unit/test_pattern_compliance_auditor.py::TestViolationDetection -v

# Run only edge case tests
pytest tests/unit/test_pattern_compliance_auditor.py::TestEdgeCases -v

# Run only roadmap tests
pytest tests/integration/test_pattern_compliance_integration.py::TestRoadmapGeneration -v
```

### Watch Mode (requires pytest-watch)
```bash
# Run tests on file changes
ptw tests/ -v
```

---

## Test Statistics

| Metric | Value |
|---|---|
| **Total Test Files** | 3 |
| **Total Tests** | 73 |
| **Unit Tests** | 41 (56%) |
| **Integration Tests** | 32 (44%) |
| **Total Lines** | 2,353 |
| **Fixture Lines** | 861 |
| **Test Fixtures** | 7 |
| **Violation Types Tested** | 6 |
| **Budget Classifications** | 3 |
| **Expected to FAIL** | 73/73 (100%) |

---

## Key Metrics for Implementation

### Line Number Accuracy
- Target: ±0 lines (exact match)
- Method: Parse content by lines, track violation location

### Budget Calculation
- Formula: `(character_count / 15000) * 100`
- Boundaries: 12K (COMPLIANT/WARNING), 15K (WARNING/OVER)

### Effort Estimation
- Compliant: 0 hours
- Moderate (5 violations): 2-3 hours
- Severe (15+ violations): 3-5 hours
- Formula: `0.5 hours per violation + 0.1 hours per 1K chars`

### Priority Ordering
- P1 (CRITICAL): Over budget (>15K chars) or CRITICAL violations
- P2 (HIGH): HIGH violations or WARNING budget (12-15K chars)
- P3 (MEDIUM): MEDIUM violations only

---

## Notes for Implementation

1. **Violation Detection**: Use regex patterns and AST parsing
2. **Line Tracking**: Maintain line numbers during parsing
3. **Code Snippets**: Extract 3-5 lines around violation
4. **Recommendations**: Based on violation type, suggest extraction target
5. **Budget Classification**: Strict boundaries at 12K and 15K
6. **Determinism**: Same input always produces same output
7. **Error Handling**: Graceful handling of malformed input
8. **JSON Output**: Fully serializable, no circular references
9. **Markdown Output**: Proper formatting, human-readable structure
10. **Roadmap**: Ordered by priority, includes effort and recommendations

---

## References

- **Full Test Summary**: `tests/STORY-037-TEST-SUMMARY.md`
- **Test Fixtures**: `tests/fixtures/command_fixtures.py`
- **Unit Tests**: `tests/unit/test_pattern_compliance_auditor.py`
- **Integration Tests**: `tests/integration/test_pattern_compliance_integration.py`
- **Acceptance Criteria**: STORY-037 story document
- **Lean Orchestration Pattern**: `devforgeai/protocols/lean-orchestration-pattern.md`

---

**Status: READY FOR IMPLEMENTATION**

All 73 tests are failing (Red phase). Ready to proceed with implementation.
