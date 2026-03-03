# STORY-040 Test Suite Execution Guide

**Framework:** pytest
**Python Version:** 3.10+
**Status:** Red Phase (All Tests Failing - Expected)

---

## Quick Start

### 1. Install Test Dependencies
```bash
pip install pytest pytest-timeout pytest-cov pytest-mock
```

### 2. Verify Test Files Exist
```bash
ls -lah tests/unit/test_*.py
# Should show 7 test files
```

### 3. Run All Tests (Red Phase)
```bash
pytest tests/unit/ -v --tb=short
# Expected: 250+ FAILED
```

### 4. Run Tests for Specific AC
```bash
pytest tests/unit/test_greenfield_documentation.py -v
pytest tests/unit/test_brownfield_analysis.py -v
pytest tests/unit/test_diagram_generation.py -v
pytest tests/unit/test_incremental_updates.py -v
pytest tests/unit/test_quality_gates.py -v
pytest tests/unit/test_templates_and_export.py -v
pytest tests/unit/test_roadmap_generation.py -v
```

---

## Detailed Test Execution

### Run with Detailed Output
```bash
# Verbose output with full tracebacks
pytest tests/unit/ -vv

# Show print statements
pytest tests/unit/ -v -s

# Stop at first failure
pytest tests/unit/ -v -x

# Stop after N failures
pytest tests/unit/ -v --maxfail=5
```

### Run Specific Test Class
```bash
pytest tests/unit/test_greenfield_documentation.py::TestReadmeGeneration -v
```

### Run Specific Test Method
```bash
pytest tests/unit/test_greenfield_documentation.py::TestReadmeGeneration::test_readme_generation_should_create_file_with_project_overview -v
```

### Run Tests by Pattern
```bash
# All "coverage" tests
pytest tests/unit/ -k "coverage" -v

# All "performance" tests
pytest tests/unit/ -k "performance" -v

# All tests except performance
pytest tests/unit/ -k "not performance" -v

# All tests with "should" in name
pytest tests/unit/ -k "should" -v
```

---

## Test Organization

### By File (7 files)
| File | Tests | AC | Focus |
|------|-------|----|----|
| test_greenfield_documentation.py | 42 | AC1 | README, guides, APIs, troubleshooting |
| test_brownfield_analysis.py | 55 | AC2 | Codebase analysis, discovery, gaps |
| test_diagram_generation.py | 52 | AC3 | Flowcharts, sequences, architecture |
| test_incremental_updates.py | 48 | AC4 | Updates, preservation, changelog |
| test_quality_gates.py | 48 | AC5 | Coverage, APIs, README, diagrams |
| test_templates_and_export.py | 56 | AC6-7 | Templates, HTML, PDF, TOC |
| test_roadmap_generation.py | 50 | AC8 | Epics, sprints, milestones, deps |
| **TOTAL** | **251** | **8** | **All acceptance criteria** |

### By Test Class (71 classes)
Each test class focuses on a specific feature area:
- `TestReadmeGeneration` - README creation
- `TestAPIDocumentationGeneration` - API docs
- `TestCodebaseAnalysis` - Code analysis
- `TestDiagramValidation` - Diagram validation
- `TestIncrementalUpdateWorkflow` - Update workflow
- `TestQualityGateEnforcement` - Quality gates
- `TestTemplateLibrary` - Template management
- `TestRoadmapGeneration` - Roadmap creation

---

## Test Metrics and Reporting

### Generate Coverage Report
```bash
# Text report
pytest tests/unit/ --cov=devforgeai_documentation --cov-report=term

# HTML report (view in browser)
pytest tests/unit/ --cov=devforgeai_documentation --cov-report=html
# Open: htmlcov/index.html

# Multiple formats
pytest tests/unit/ --cov=devforgeai_documentation \
  --cov-report=term \
  --cov-report=html \
  --cov-report=json
```

### Show Which Tests Failed
```bash
# Show only failed tests
pytest tests/unit/ --tb=no --quiet

# Show test names (not output)
pytest tests/unit/ --collect-only -q
```

### Generate Test Report
```bash
# JUnit XML (for CI/CD)
pytest tests/unit/ --junit-xml=test-results.xml

# HTML report
pytest tests/unit/ --html=report.html
```

---

## Test Categories

### By Type

#### Unit Tests (180+)
```bash
pytest tests/unit/ -k "not performance and not integration" -v
```

#### Performance Tests (7)
```bash
pytest tests/unit/ -k "performance" -v
# Expected: FAIL (no implementation)
```

#### Integration Tests (40+)
```bash
pytest tests/unit/ -k "integration or workflow" -v
```

#### Edge Cases (20+)
```bash
pytest tests/unit/ -k "edge or empty or missing or error" -v
```

### By Acceptance Criteria

#### AC1 Tests (42)
```bash
pytest tests/unit/test_greenfield_documentation.py -v --tb=short
# Tests for README, guides, APIs, troubleshooting
```

#### AC2 Tests (55)
```bash
pytest tests/unit/test_brownfield_analysis.py -v --tb=short
# Tests for codebase analysis, gaps, recommendations
```

#### AC3 Tests (52)
```bash
pytest tests/unit/test_diagram_generation.py -v --tb=short
# Tests for Mermaid diagrams, validation, embedding
```

#### AC4 Tests (48)
```bash
pytest tests/unit/test_incremental_updates.py -v --tb=short
# Tests for incremental updates, preservation, changelog
```

#### AC5 Tests (48)
```bash
pytest tests/unit/test_quality_gates.py -v --tb=short
# Tests for quality gates, coverage, blocking
```

#### AC6-7 Tests (56)
```bash
pytest tests/unit/test_templates_and_export.py -v --tb=short
# Tests for templates, HTML export, PDF export, TOC
```

#### AC8 Tests (50)
```bash
pytest tests/unit/test_roadmap_generation.py -v --tb=short
# Tests for roadmap, timelines, milestones, dependencies
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'devforgeai_documentation'"

**Cause:** Implementation module doesn't exist yet (expected in Red phase)

**Solution:** This is correct for TDD Red phase. After Green phase implementation, tests will import properly.

### "pytest: command not found"

**Solution:** Install pytest
```bash
pip install pytest
```

### Tests Pass When They Should Fail

**Cause:** Implementation code was added before tests

**Solution:** For TDD, tests should drive implementation. If tests pass with no implementation, tests are likely too simple or mocking too much.

### Timeout Errors

**Solution:** Increase timeout
```bash
pytest tests/unit/ --timeout=300  # 5 minutes
```

---

## Performance Test Expectations

### Greenfield Tests (<2 minutes)
```bash
pytest tests/unit/test_greenfield_documentation.py::TestPerformanceNFR -v
# Expected: FAIL (no implementation)
```

### Brownfield Tests (<10 minutes)
```bash
pytest tests/unit/test_brownfield_analysis.py::TestAnalysisPerformance -v
# Expected: FAIL (no implementation)
```

### Diagram Tests (<30 seconds)
```bash
pytest tests/unit/test_diagram_generation.py::TestDiagramPerformance -v
# Expected: FAIL (no implementation)
```

### Update Tests (<1 minute)
```bash
pytest tests/unit/test_incremental_updates.py::TestPerformanceForUpdates -v
# Expected: FAIL (no implementation)
```

### Export Tests (<60 seconds)
```bash
pytest tests/unit/test_templates_and_export.py::TestExportPerformance -v
# Expected: FAIL (no implementation)
```

---

## Continuous Integration

### For GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e . && pip install pytest pytest-cov
      - run: pytest tests/unit/ --cov=devforgeai_documentation --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### For Pre-Commit Hook
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit/
        language: system
        stages: [commit]
EOF

# Install hook
pre-commit install
```

---

## Development Workflow

### Phase 1: Red (Current)
```bash
# Run all tests - expect FAIL
pytest tests/unit/ -v

# Result: 251 FAILED, 0 PASSED
# This is CORRECT - tests drive implementation
```

### Phase 2: Green (Next)
```bash
# After implementing code
pytest tests/unit/ -v

# Result: All tests should pass (or most)
# Focus on making tests green
```

### Phase 3: Refactor
```bash
# After implementation, run continuously
pytest tests/unit/ -v --timeout=10

# While refactoring:
# 1. Tests should stay GREEN
# 2. No functionality should change
# 3. Focus on code quality
```

---

## Test Fixtures and Mocks

### Common Fixtures (to implement in conftest.py)
```python
import pytest
from unittest.mock import Mock, MagicMock

@pytest.fixture
def mock_story():
    """Mock story object"""
    return {
        "id": "STORY-040",
        "title": "Documentation Skill",
        "status": "Ready for Dev"
    }

@pytest.fixture
def mock_context():
    """Mock context"""
    return {"project_name": "DevForgeAI"}

@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files"""
    return tmp_path
```

### Using Mocks in Tests
```python
def test_example(mock_story):
    # Use fixture
    assert mock_story["id"] == "STORY-040"

@patch('devforgeai_documentation.read_file')
def test_with_patch(mock_read):
    mock_read.return_value = "content"
    # Test code
```

---

## Test Data

### Sample Story (AC1)
```yaml
id: STORY-040
title: DevForgeAI Documentation Skill
status: QA Approved
acceptance_criteria:
  - "Generate README.md"
  - "Create developer guide"
  - "Generate API documentation"
technical_spec:
  setup_steps:
    - npm install
    - npm run dev
```

### Sample Codebase (AC2)
```
src/
  index.ts
  app.tsx
  services/
    UserService.ts
    AuthService.ts
  models/
    User.ts
    Auth.ts
tests/
  UserService.test.ts
docs/
  README.md
  API.md
```

---

## Exit Criteria (Red Phase Complete)

- [x] 7 test files created
- [x] 71 test classes defined
- [x] 250+ test methods written
- [x] All tests follow AAA pattern
- [x] Tests are syntactically valid (can be parsed by pytest)
- [x] All tests FAIL (no implementation)
- [x] Performance tests included
- [x] Edge case tests included
- [x] Integration tests included
- [x] Test summary documentation created

---

## Next Steps (Green Phase)

1. **Create Implementation Module**
   ```bash
   mkdir devforgeai_documentation
   touch devforgeai_documentation/__init__.py
   ```

2. **Implement Classes** (one test class at a time)
   - Focus on making one test pass
   - Then move to next test
   - Use TDD rhythm: Red → Green → Refactor

3. **Run Tests Frequently**
   ```bash
   pytest tests/unit/ -v  # After each implementation
   ```

4. **Track Progress**
   ```bash
   pytest tests/unit/ --tb=no  # See pass/fail counts
   ```

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)
- [pytest Mocking](https://docs.pytest.org/en/latest/monkeypatch.html)
- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)
- [AAA Pattern](https://www.freecodecamp.org/news/arrange-act-assert/)

---

**Generated:** 2025-11-18
**Framework:** DevForgeAI TDD Workflow
**Phase:** Red (Tests First)
