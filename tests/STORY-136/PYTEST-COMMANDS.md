# STORY-136 pytest Command Reference

## Quick Commands

### Run All Tests
```bash
pytest tests/STORY-136/ -v
```

### Run with Short Output
```bash
pytest tests/STORY-136/ -v --tb=short
```

### Run with No Output (Fast)
```bash
pytest tests/STORY-136/ -q
```

---

## Run by Acceptance Criterion

### AC#1: Checkpoint File Creation (8 tests)
```bash
pytest tests/STORY-136/test_checkpoint_file_creation.py -v
```

### AC#2: Content Structure (14 tests)
```bash
pytest tests/STORY-136/test_checkpoint_content_structure.py -v
```

### AC#3: Session ID Generation (16 tests)
```bash
pytest tests/STORY-136/test_session_id_generation.py -v
```

### AC#4: Timestamp Validation (21 tests)
```bash
pytest tests/STORY-136/test_timestamp_validation.py -v
```

### AC#5: Phase Tracking (20 tests)
```bash
pytest tests/STORY-136/test_phase_tracking.py -v
```

### AC#6: Atomic Writes (13 tests)
```bash
pytest tests/STORY-136/test_atomic_writes.py -v
```

---

## Run by Test Category

### Edge Cases Only (24 tests)
```bash
pytest tests/STORY-136/test_edge_cases.py -v
```

### Integration & E2E (10 tests)
```bash
pytest tests/STORY-136/test_integration.py -v
```

### All Unit Tests (92 tests)
```bash
pytest tests/STORY-136/test_*.py -v --ignore=tests/STORY-136/test_integration.py
```

---

## Run Specific Test Class

### Checkpoint File Creation Tests
```bash
pytest tests/STORY-136/test_checkpoint_file_creation.py::TestCheckpointFileCreation -v
```

### Atomic Writes Tests
```bash
pytest tests/STORY-136/test_atomic_writes.py::TestAtomicWrites -v
```

### Session ID Generation Tests
```bash
pytest tests/STORY-136/test_session_id_generation.py::TestSessionIdGeneration -v
```

---

## Run Specific Test

### Example: Run one test
```bash
pytest tests/STORY-136/test_checkpoint_file_creation.py::TestCheckpointFileCreation::test_should_create_checkpoint_file_after_phase_one_completion -v
```

### Example: Run all tests with "uuid" in name
```bash
pytest tests/STORY-136/ -k "uuid" -v
```

### Example: Run all tests with "timestamp" in name
```bash
pytest tests/STORY-136/ -k "timestamp" -v
```

### Example: Run all tests with "phase" in name
```bash
pytest tests/STORY-136/ -k "phase" -v
```

---

## Show Test Details

### Verbose Output (Shows docstrings)
```bash
pytest tests/STORY-136/ -v --tb=short
```

### Very Verbose Output
```bash
pytest tests/STORY-136/ -vv
```

### Show Full Tracebacks
```bash
pytest tests/STORY-136/ -v --tb=long
```

### Show Print Statements
```bash
pytest tests/STORY-136/ -v -s
```

---

## Stop on First Failure

```bash
pytest tests/STORY-136/ -x  # Stop on first failure
pytest tests/STORY-136/ -x -v  # Verbose + stop first
pytest tests/STORY-136/ --maxfail=3 -v  # Stop after 3 failures
```

---

## Skip Tests

### Skip marked tests
```bash
pytest tests/STORY-136/ -v -m "not skip"
```

### Skip specific test
```bash
pytest tests/STORY-136/ -v --deselect tests/STORY-136/test_checkpoint_file_creation.py::TestCheckpointFileCreation::test_should_create_checkpoint_file_after_phase_one_completion
```

---

## Coverage Reports

### Generate HTML Coverage Report
```bash
pytest tests/STORY-136/ --cov=. --cov-report=html
open htmlcov/index.html  # View in browser (Mac)
start htmlcov/index.html  # View in browser (Windows)
xdg-open htmlcov/index.html  # View in browser (Linux)
```

### Generate Terminal Coverage Report
```bash
pytest tests/STORY-136/ --cov=. --cov-report=term-missing
```

### Coverage for Specific Module
```bash
pytest tests/STORY-136/ --cov=checkpoint_service --cov-report=html
```

### Coverage with Percentage Threshold
```bash
pytest tests/STORY-136/ --cov=. --cov-fail-under=80
```

---

## Test Results & Reports

### Generate JUnit XML Report
```bash
pytest tests/STORY-136/ --junit-xml=test-results.xml
```

### Generate JSON Report
```bash
pytest tests/STORY-136/ --json-report --json-report-file=report.json
```

### Verbose with Timestamps
```bash
pytest tests/STORY-136/ -v --tb=short -r fEsxX
```

---

## Parameterized Tests

### Run only parameterized tests with specific parameter
```bash
# Run only tests with UUID validation
pytest tests/STORY-136/test_session_id_generation.py -k "parametrize" -v

# Run tests for specific phase number (if parameterized)
pytest tests/STORY-136/test_phase_tracking.py::TestPhaseTracking::test_should_track_all_valid_phase_numbers -v
```

---

## Filter by Status

### Show Only Failures
```bash
pytest tests/STORY-136/ --tb=no -q | grep FAILED
```

### Show Only Passes
```bash
pytest tests/STORY-136/ -q | grep PASSED
```

### Show Failed Tests with Short Summary
```bash
pytest tests/STORY-136/ -v --tb=line  # Show one line per failure
```

---

## Parallel Execution (if pytest-xdist installed)

```bash
pytest tests/STORY-136/ -n auto  # Use all CPUs
pytest tests/STORY-136/ -n 4  # Use 4 processes
```

---

## Watch Mode (if pytest-watch installed)

```bash
ptw tests/STORY-136/ -- -v  # Re-run on file changes
ptw tests/STORY-136/ -- -x  # Stop on first failure
```

---

## Debugging

### Drop into Debugger on Failure
```bash
pytest tests/STORY-136/ --pdb  # Drop into pdb on failure
pytest tests/STORY-136/ --pdbcls=IPython.terminal.debugger:TerminalPdb  # Use IPython
```

### Show Local Variables on Failure
```bash
pytest tests/STORY-136/ -l
```

### Full Diff on Assertion Failure
```bash
pytest tests/STORY-136/ -vv
```

---

## Quick Status Checks

### Count Tests
```bash
pytest tests/STORY-136/ --collect-only -q | tail -1
```

### List All Tests
```bash
pytest tests/STORY-136/ --collect-only -q
```

### Show Test Durations
```bash
pytest tests/STORY-136/ -v --durations=10
```

### Slowest Tests
```bash
pytest tests/STORY-136/ -v --durations=0
```

---

## CI/CD Pipeline Commands

### Full Test Suite with All Reports
```bash
pytest tests/STORY-136/ \
  -v \
  --tb=short \
  --junit-xml=test-results.xml \
  --cov=. \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=80
```

### Quick Validation
```bash
pytest tests/STORY-136/ -q --tb=line
```

### Pre-Commit Hook
```bash
pytest tests/STORY-136/ -x --tb=short
```

---

## Test Organization

### By Acceptance Criterion
```bash
# AC#1-AC#6 (unit tests)
pytest tests/STORY-136/test_checkpoint_*.py -v

# Edge cases & NFR
pytest tests/STORY-136/test_edge_cases.py -v

# Integration & E2E
pytest tests/STORY-136/test_integration.py -v
```

### By Test Size
```bash
# Small unit tests
pytest tests/STORY-136/test_*_generation.py -v

# Medium integration tests
pytest tests/STORY-136/test_integration.py -v

# Edge cases (can be large)
pytest tests/STORY-136/test_edge_cases.py -v
```

---

## Common Development Workflows

### Develop Single Test
```bash
# First run - fails as expected
pytest tests/STORY-136/test_checkpoint_file_creation.py::TestCheckpointFileCreation::test_should_create_checkpoint_file_after_phase_one_completion -vvs

# Watch for changes
ptw tests/STORY-136/test_checkpoint_file_creation.py -- -vvs --tb=short
```

### Develop Feature (AC#1)
```bash
# Run AC#1 tests
pytest tests/STORY-136/test_checkpoint_file_creation.py -v

# Watch for changes
ptw tests/STORY-136/test_checkpoint_file_creation.py -- -v --tb=short
```

### Verify All ACs Pass
```bash
# Run full suite
pytest tests/STORY-136/ -v --tb=short

# Or check each AC separately
for file in test_checkpoint_*.py test_session_id_*.py test_timestamp_*.py test_phase_*.py test_atomic_*.py; do
  echo "Testing $file..."
  pytest tests/STORY-136/$file -v
done
```

---

## Fixture Debugging

### Show Available Fixtures
```bash
pytest tests/STORY-136/ --fixtures
```

### Show Fixtures for Specific Test File
```bash
pytest tests/STORY-136/test_checkpoint_file_creation.py --fixtures
```

### Test Fixture Values
```bash
# Add print statement in conftest.py fixture
@pytest.fixture
def valid_session_id():
    value = str(uuid.uuid4())
    print(f"\nGenerated session_id: {value}")  # Will print when pytest -s used
    return value

# Run with -s to see print output
pytest tests/STORY-136/ -s
```

---

## Performance Analysis

### Show Slowest Tests
```bash
pytest tests/STORY-136/ --durations=10 -v
```

### Benchmark Test Execution
```bash
# Measure total time
time pytest tests/STORY-136/ -q

# Measure per-test time
pytest tests/STORY-136/ --durations=0 -q
```

---

## Useful Aliases

Add to ~/.bashrc or ~/.zshrc:

```bash
# Run all STORY-136 tests
alias test-136='pytest tests/STORY-136/ -v --tb=short'

# Run with coverage
alias test-136-cov='pytest tests/STORY-136/ --cov=. --cov-report=html'

# Watch for changes
alias test-136-watch='ptw tests/STORY-136/ -- -v --tb=short'

# Quick status
alias test-136-quick='pytest tests/STORY-136/ -q'

# Verbose debugging
alias test-136-debug='pytest tests/STORY-136/ -vvs --tb=long'

# Stop on first failure
alias test-136-fail='pytest tests/STORY-136/ -x -v'

# Show test count
alias test-136-count='pytest tests/STORY-136/ --collect-only -q | tail -1'
```

---

## Pytest Configuration

The pytest configuration is in `/mnt/c/Projects/DevForgeAI2/pytest.ini`

Key settings:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## Quick Cheat Sheet

| Command | Purpose |
|---------|---------|
| `pytest tests/STORY-136/ -v` | Run all tests, verbose |
| `pytest tests/STORY-136/ -q` | Run all tests, quiet |
| `pytest tests/STORY-136/ -x` | Stop on first failure |
| `pytest tests/STORY-136/ -k "phrase"` | Run tests matching phrase |
| `pytest tests/STORY-136/ --collect-only` | List tests without running |
| `pytest tests/STORY-136/ --cov=. --cov-report=html` | Coverage report |
| `pytest tests/STORY-136/ -vv --tb=long` | Very verbose with full tracebacks |
| `pytest tests/STORY-136/test_checkpoint_file_creation.py -v` | Run AC#1 only |
| `ptw tests/STORY-136/ -- -v` | Watch mode (requires pytest-watch) |
| `pytest tests/STORY-136/ --durations=10` | Show slowest 10 tests |

---

## Need Help?

- See README.md for getting started
- See TEST-GENERATION-SUMMARY.md for detailed statistics
- See story file: devforgeai/specs/Stories/STORY-136-file-based-checkpoint-protocol.story.md
- Run `pytest tests/STORY-136/ --help` for all pytest options

---

**Last Updated:** 2025-12-25
**pytest Version:** 7.4.4+
**Python Version:** 3.12.3+
