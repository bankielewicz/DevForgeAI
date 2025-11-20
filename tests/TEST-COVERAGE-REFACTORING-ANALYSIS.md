# Test Coverage Refactoring Analysis: Hook System

## Executive Summary

**Problem:** 182 tests with 0% coverage due to exclusive Mock/MagicMock usage (no real imports)

**Root Cause:** Tests fixture data and mock objects but never import `src/` modules

**Impact:**
- Coverage report: 0% despite 182 passing tests
- ~2,156 lines of production code untested at import level
- 6 core modules completely uncovered: hook_system, hook_registry, hook_patterns, hook_conditions, hook_circular, hook_invocation

**Solution:** Progressive refactoring from fixture-based to import-based testing

---

## Current State Analysis

### Test Files (8 files)
```
test_hook_system.py        (429 lines, 19 tests)   ← PILOT
test_hook_circular.py      (469 lines, 22 tests)
test_hook_timeout.py       (469 lines, 23 tests)
test_hook_patterns.py      (508 lines, 28 tests)
test_hook_stress.py        (564 lines, 31 tests)
test_hook_integration.py   (579 lines, 32 tests)
test_hook_registry.py      (661 lines, 36 tests)
+ 2 other files           (tests for feedback, template)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 3,679 lines, 182 tests, 0% coverage
```

### Source Files (6 hook modules)
```
hook_system.py      (222 lines)  - Main orchestrator
hook_registry.py    (405 lines)  - Config loading + validation
hook_patterns.py    (136 lines)  - Pattern matching (exact/glob/regex)
hook_conditions.py  (138 lines)  - Trigger condition evaluation
hook_circular.py    (171 lines)  - Circular dependency detection
hook_invocation.py  (318 lines)  - Hook execution context + invocation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 1,390 lines (+ feedback/template modules = 2,156 total)
```

### Current Mocking Pattern (All 8 Files)

**Imports:** None from `src/`
```python
# Current (conftest adds src/ to path, but tests don't use it)
from unittest.mock import Mock, MagicMock, patch, call
import yaml, asyncio, re
# MISSING: from src.hook_system import HookSystem
# MISSING: from src.hook_registry import HookRegistry
```

**Test Structure:** Fixture-based only
```python
@pytest.fixture
def hook_registry_config():
    return {'hooks': [...]}  # No real HookRegistry instantiation

def test_load_hook_registry(self, hook_registry_config):
    # Act: Manually parse YAML (mocking the registry)
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)  # NOT real HookRegistry
    # Assert: Validate dict structure
```

**Subclass/Method Mocking:** Heavy usage
```python
mock_hook_runner = Mock()
mock_hook_runner.run = AsyncMock(return_value={'status': 'success'})
# Tests the mock, not the real HookInvoker
```

---

## Why 0% Coverage?

**Coverage requires:**
1. ✅ Tests pass → YES (all 182 pass)
2. ✅ Code executes → NO (mocks prevent execution)
3. ✅ Real imports → NO (zero `from src` imports)

**Coverage calculation:**
```
Coverage = (lines executed) / (lines available)
         = 0 / 2,156
         = 0%

Because:
- Tests never import HookSystem, HookRegistry, etc.
- Tests never instantiate real classes
- Tests never execute src/ code paths
- Mock objects = no code execution in src/
```

---

## Refactoring Strategy

### Phase 1: Minimal Change for Coverage (Pragmatic Approach)

**Goal:** Get real imports + instantiations working without rewriting tests

**Key Insight:** Most tests don't need fixture data - they test logic directly

**Example Transformation:**

```python
# BEFORE (Fixture-based, 0% coverage)
def test_pattern_matching_simple(self):
    pattern = 'dev'
    operation = 'dev'
    matches = operation == pattern  # Manual logic
    assert matches is True

# AFTER (Real import, real code)
from src.hook_patterns import PatternMatcher

def test_pattern_matching_simple(self):
    matcher = PatternMatcher()  # Real class
    matches = matcher.match('dev', 'dev')  # Real method
    assert matches is True
```

**Impact:** 1 import, ~5 lines changed per test, 100% behavior preserved

### Phase 2: Smart Fixture Replacement

**Pattern 1: Config Fixtures → Real Classes**
```python
# BEFORE
@pytest.fixture
def hook_registry_config():
    return {'hooks': [{'id': 'test-hook-1', ...}]}

def test_hook_available(self, hook_system_config_file):
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)  # Manual parsing
    hook_ids = [hook['id'] for hook in registry_data['hooks']]

# AFTER
from src.hook_registry import HookRegistry

def test_hook_available(self, hook_system_config_file):
    registry = HookRegistry(hook_system_config_file)  # Real class
    hook_ids = [hook.id for hook in registry.get_hooks()]  # Real method
```

**Pattern 2: Mock Objects → Real Objects**
```python
# BEFORE
mock_hook_runner = Mock()
mock_hook_runner.run = AsyncMock(return_value={'status': 'success'})
result = await mock_hook_runner.run(hook_config, operation_context)

# AFTER
from src.hook_invocation import HookInvoker
invoker = HookInvoker(registry, circular_detector)  # Real classes
result = await invoker.invoke(hook_config, operation_context)  # Real method
```

**Pattern 3: Manual Logic → Real Pattern Matcher**
```python
# BEFORE (in test_hook_patterns.py)
def test_exact_pattern_matching(self, pattern, operation, expected):
    matches = operation == pattern  # Manual logic in test
    assert matches == expected

# AFTER
from src.hook_patterns import PatternMatcher

def test_exact_pattern_matching(self, pattern, operation, expected):
    matcher = PatternMatcher()
    matches = matcher.match(pattern, operation)  # Real pattern matching
    assert matches == expected
```

---

## Pilot: test_hook_system.py Refactoring

### Why This File?

**Advantages (Good Pilot):**
- ✅ Smallest: 429 lines (19 tests)
- ✅ Simplest: Uses fixtures only, no complex mocks
- ✅ Core: Tests HookSystem initialization
- ✅ Straightforward: Can serve as template for other files

**Test Structure:**
```
TestHookRegistrationAndDiscovery (5 tests)
  - Load registry, empty config, discover hooks, check availability, metadata

TestHookContextDataAvailability (7 tests)
  - Verify context fields, UUID uniqueness, timestamp format, stack tracking

TestHookInvocationTrigger (4 tests)
  - Hook invocation on completion, pattern matching, context passing

TestHookSystemIntegration (3 tests)
  - System init, missing config handling, invocation order
```

### Refactoring Steps (Estimated 1-1.5 hours)

**Step 1: Add Real Imports (10 minutes)**
```python
# Add after existing imports
from src.hook_system import HookSystem
from src.hook_registry import HookRegistry, HookRegistryEntry
from src.hook_invocation import HookInvocationContext
from src.hook_patterns import PatternMatcher
```

**Step 2: Update Fixtures to Create Real Objects (30 minutes)**

Replace:
```python
@pytest.fixture
def hook_registry_config():
    return {'hooks': [{...}]}
```

With:
```python
@pytest.fixture
def hook_system_instance(hook_system_config_file):
    """Real HookSystem instance instead of config fixture."""
    return HookSystem(config_path=hook_system_config_file)
```

**Step 3: Refactor Test Methods (45 minutes)**

For each test:
1. Replace YAML manual parsing → real HookRegistry call
2. Replace dict assertions → object assertions
3. Update assertions to call real methods

**Example Test Refactoring:**

```python
# BEFORE (0% coverage)
def test_load_hook_registry_from_yaml(self, hook_system_config_file):
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)
    assert 'hooks' in registry_data
    assert len(registry_data['hooks']) == 1
    hook = registry_data['hooks'][0]
    assert hook['id'] == 'test-hook-1'

# AFTER (~15% coverage for this module)
def test_load_hook_registry_from_yaml(self, hook_system_instance):
    """Real HookSystem loads real HookRegistry."""
    # Now testing actual HookSystem.registry instantiation
    hooks = hook_system_instance.registry.get_hooks()
    assert len(hooks) == 1
    assert hooks[0].id == 'test-hook-1'  # Real HookRegistryEntry
```

**Step 4: Verify Coverage Improves (15 minutes)**
```bash
python3 -m pytest tests/test_hook_system.py --cov=src/hook_system --cov=src/hook_registry --cov-report=term-missing
```

Expected result: ~40-50% coverage for hook_system and hook_registry modules

**Step 5: Run Full Test Suite (5 minutes)**
```bash
python3 -m pytest tests/test_hook_system.py -v
```

Expected result: ✅ All 19 tests pass (behavior preserved)

---

## Estimated Effort: Full Refactoring

### By Phase

**Phase 1: Pilot (test_hook_system.py)**
- Imports: 10 min
- Fixture refactoring: 30 min
- Test method refactoring: 45 min
- Verification: 15 min
- **Total: 1.5 hours**
- **Expected Coverage Gain: 0% → 15-20% (hook_system, hook_registry partial)**

**Phase 2: Pattern Module (test_hook_patterns.py, 508 lines)**
- More complex (multiple pattern types)
- Heavy use of manual pattern matching logic
- Estimated: **2-2.5 hours**
- **Expected Coverage: +20% (hook_patterns fully covered)**

**Phase 3: Circular Detector (test_hook_circular.py, 469 lines)**
- Moderate complexity (cycle detection algorithm)
- Estimated: **2 hours**
- **Expected Coverage: +10% (hook_circular fully covered)**

**Phase 4: Integration Tests (test_hook_integration.py, 579 lines)**
- Most complex (coordinates multiple modules)
- Estimated: **2.5-3 hours**
- **Expected Coverage: +15-20% (hook_invocation partial)**

**Phase 5: Registry Tests (test_hook_registry.py, 661 lines)**
- Very complex (validation, edge cases)
- Estimated: **2.5-3 hours**
- **Expected Coverage: +15-20% (hook_registry completion)**

**Phase 6: Stress & Timeout Tests (test_hook_stress.py, test_hook_timeout.py, 1,033 lines)**
- Performance/behavior tests
- Estimated: **1.5-2 hours**
- **Expected Coverage: +5-10% (edge cases)**

**Total Estimated Effort: 12-16 hours (2-3 working days)**

---

## Risk Analysis

### Low Risk (✅)
- Tests only test logic, not I/O
- No database, network, file system changes
- Fixtures create temporary files → easily cleaned up
- All tests currently pass
- Conftest already adds src/ to path

### Medium Risk (⚠️)
- AsyncMock handling needs verification
- Circular detector tests might timeout (test_hook_timeout.py)
- Pattern matcher has regex caching (need to verify thread safety)

### Mitigation
1. Run tests one file at a time
2. Use `--timeout=10` for timeout tests
3. Add fixture cleanup verification

---

## Implementation Plan: Realistic Schedule

### Day 1: Pilot + Foundation (Pilot = 1.5 hours, validation = 0.5 hours)
- ✅ Refactor test_hook_system.py (smallest)
- ✅ Verify coverage improves 0% → 15-20%
- ✅ Create refactoring template for other files
- ✅ Total: 2 hours
- **Target: Proof of concept**

### Day 2: Core Modules (test_hook_patterns.py + test_hook_circular.py = 4-4.5 hours)
- ✅ Refactor test_hook_patterns.py (pattern matching)
- ✅ Refactor test_hook_circular.py (circular detection)
- ✅ Run both with coverage
- ✅ Total: 4-5 hours (includes testing)
- **Target: 40-50% coverage**

### Day 3: Integration & Registry (test_hook_integration.py + test_hook_registry.py = 5-6 hours)
- ✅ Refactor test_hook_integration.py
- ✅ Refactor test_hook_registry.py
- ✅ Run full test suite with coverage
- ✅ Total: 5-6 hours (includes testing)
- **Target: 75-85% coverage**

### Day 4: Edge Cases & Validation (test_hook_stress.py + test_hook_timeout.py = 2 hours)
- ✅ Refactor test_hook_stress.py
- ✅ Refactor test_hook_timeout.py
- ✅ Final coverage report + cleanup
- ✅ Total: 2 hours
- **Target: 95%+ coverage for 6 modules**

---

## Coverage Targets

### Current State
```
Total Coverage: 0%
- hook_system.py:     0%
- hook_registry.py:   0%
- hook_patterns.py:   0%
- hook_conditions.py: 0%
- hook_circular.py:   0%
- hook_invocation.py: 0%
```

### After Phase 1 (test_hook_system.py refactored)
```
Total Coverage: ~3% (43 lines of 1,390)
- hook_system.py:     ~30%
- hook_registry.py:   ~25%
- hook_patterns.py:   0%
- hook_conditions.py: 0%
- hook_circular.py:   0%
- hook_invocation.py: 0%
```

### After Phase 2-3 (+ test_hook_patterns.py, test_hook_circular.py)
```
Total Coverage: ~25% (350 lines of 1,390)
- hook_system.py:     ~45%
- hook_registry.py:   ~35%
- hook_patterns.py:   ~85%
- hook_conditions.py: ~15%
- hook_circular.py:   ~90%
- hook_invocation.py: 0%
```

### Final State (All 8 files refactored)
```
Total Coverage: ~93% (1,293 lines of 1,390)
- hook_system.py:     95%
- hook_registry.py:   95%
- hook_patterns.py:   98%
- hook_conditions.py: 90%
- hook_circular.py:   95%
- hook_invocation.py: 92%

Business Logic:     95%+
Application Layer:  88%+
Infrastructure:     85%+

✅ All thresholds met
```

---

## Quick Start: Pilot Refactoring

### Copy-Paste Steps

**1. Add imports to test_hook_system.py (line 20, after existing imports):**
```python
from src.hook_system import HookSystem
from src.hook_registry import HookRegistry, HookRegistryEntry
from src.hook_invocation import HookInvocationContext
from src.hook_patterns import PatternMatcher
```

**2. Add new fixture (line 82, before TestHookRegistrationAndDiscovery):**
```python
@pytest.fixture
def hook_system_instance(hook_system_config_file):
    """Real HookSystem instance."""
    return HookSystem(config_path=hook_system_config_file)
```

**3. Replace test_load_hook_registry_from_yaml method:**
```python
def test_load_hook_registry_from_yaml(self, hook_system_instance):
    """Hook registry loads real hooks from YAML."""
    hooks = hook_system_instance.registry.get_hooks()
    assert len(hooks) == 1
    assert hooks[0].id == 'test-hook-1'
    assert hooks[0].operation_type == 'command'
    assert hooks[0].enabled is True
```

**4. Run test:**
```bash
python3 -m pytest tests/test_hook_system.py::TestHookRegistrationAndDiscovery::test_load_hook_registry_from_yaml -v --cov=src/hook_system --cov=src/hook_registry --cov-report=term-missing
```

**Expected:** ✅ Test passes + Coverage shows ~25% for hook_system

---

## Key Success Factors

1. **Import first, refactor second** - Add real imports before changing test logic
2. **Run tests frequently** - After each test file, verify coverage improves
3. **Template reuse** - Use pilot refactoring as template for other 7 files
4. **Fixture preservation** - Keep pytest fixtures, just make them use real classes
5. **Parallel possibility** - After pattern established, can refactor 2-3 files in parallel

---

## Next Steps

1. ✅ Review this analysis
2. ✅ Confirm pilot file (test_hook_system.py)
3. ✅ Estimate actual time with team
4. ✅ Start refactoring (Day 1: test_hook_system.py)
5. ✅ Measure actual vs estimated
6. ✅ Adjust approach for remaining files

---

## Appendix: Module Dependency Graph

```
hook_system.py
├─ depends on: hook_registry, hook_invocation, hook_circular, hook_patterns
├─ used by: tests (all files use directly/indirectly)

hook_registry.py
├─ depends on: none (standalone YAML loader + validator)
├─ used by: hook_system, tests

hook_patterns.py
├─ depends on: none (standalone pattern matching)
├─ used by: hook_system, tests

hook_conditions.py
├─ depends on: none (standalone condition evaluator)
├─ used by: hook_invocation, tests

hook_circular.py
├─ depends on: none (standalone cycle detector)
├─ used by: hook_system, hook_invocation, tests

hook_invocation.py
├─ depends on: hook_circular, hook_registry, hook_conditions
├─ used by: hook_system, tests

Refactoring Order (by dependency)
1. hook_registry (no deps)
2. hook_patterns (no deps)
3. hook_circular (no deps)
4. hook_conditions (no deps)
5. hook_invocation (depends on 1,3,4)
6. hook_system (depends on all)
```

---

