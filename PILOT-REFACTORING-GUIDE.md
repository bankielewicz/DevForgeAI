# Pilot Refactoring Guide: test_hook_system.py

## Overview

This guide provides step-by-step instructions for refactoring `test_hook_system.py` from fixture-based (0% coverage) to import-based (15-25% coverage).

**Time estimate:** 1.5 hours

**Difficulty:** Easy - template for remaining 7 files

---

## File Information

**Source:** `/mnt/c/Projects/DevForgeAI2/tests/test_hook_system.py`
- Lines: 429
- Tests: 19
- Classes: 4
- Imports: None from `src/`

**Related Source Modules:**
- `src/hook_system.py` (222 lines)
- `src/hook_registry.py` (405 lines)
- `src/hook_invocation.py` (318 lines)
- `src/hook_patterns.py` (136 lines)

---

## Step 1: Add Real Imports (10 minutes)

**Location:** After line 19 (after existing imports)

**Before:**
```python
import pytest
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from unittest.mock import Mock, MagicMock, patch, call
import yaml
import asyncio
```

**Add these imports:**
```python
# Real module imports for testing
from src.hook_system import HookSystem
from src.hook_registry import HookRegistry, HookRegistryEntry
from src.hook_invocation import HookInvocationContext
from src.hook_patterns import PatternMatcher
```

**Why:**
- `HookSystem`: Main orchestrator being tested
- `HookRegistry`, `HookRegistryEntry`: Real registry classes
- `HookInvocationContext`: Context data structure
- `PatternMatcher`: Pattern matching logic

**Verify:** Run `python3 -c "from src.hook_system import HookSystem; print('OK')"` → Should print OK

---

## Step 2: Add New Fixture (30 minutes)

**Location:** After line 81 (after `mock_feedback_skill` fixture, before `TestHookRegistrationAndDiscovery`)

**Add this fixture:**
```python
@pytest.fixture
def hook_system_instance(hook_system_config_file):
    """Real HookSystem instance for testing."""
    return HookSystem(config_path=hook_system_config_file)
```

**Why:**
- Creates a real HookSystem with actual config file
- Initializes real HookRegistry, CircularDependencyDetector, HookInvoker, PatternMatcher
- Tests can now call real methods instead of mocking

**Verify:** Fixture uses existing `hook_system_config_file` fixture (no changes needed)

---

## Step 3: Refactor Test Methods (45 minutes)

### Test Class 1: TestHookRegistrationAndDiscovery (5 tests)

#### Test 1: test_load_hook_registry_from_yaml

**Current (lines 91-110):**
```python
def test_load_hook_registry_from_yaml(self, hook_system_config_file):
    """GIVEN ..., WHEN ..., THEN ..."""
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)
    assert 'hooks' in registry_data
    assert len(registry_data['hooks']) == 1
    hook = registry_data['hooks'][0]
    assert hook['id'] == 'test-hook-1'
    assert hook['operation_type'] == 'command'
    assert hook['enabled'] is True
```

**Replace with:**
```python
def test_load_hook_registry_from_yaml(self, hook_system_instance):
    """GIVEN HookSystem initialized, WHEN registry loads, THEN hooks available."""
    # Act: Get hooks from real registry
    hooks = hook_system_instance.registry.get_hooks()
    
    # Assert: Verify real hook object
    assert len(hooks) == 1
    assert hooks[0].id == 'test-hook-1'
    assert hooks[0].operation_type == 'command'
    assert hooks[0].enabled is True
```

**Changes:**
- Parameter: `hook_system_config_file` → `hook_system_instance`
- Line 101-102: Remove manual YAML parsing
- Line 103: Use real `registry.get_hooks()` method
- Line 106-110: Access hook object properties directly

#### Test 2: test_hook_registry_empty_config

**Current (lines 112-123):**
```python
def test_hook_registry_empty_config(self, tmp_path):
    config_file = tmp_path / 'hooks.yaml'
    config_file.write_text('hooks: []')
    with open(config_file) as f:
        registry_data = yaml.safe_load(f)
    assert registry_data['hooks'] == []
```

**Replace with:**
```python
def test_hook_registry_empty_config(self, tmp_path):
    """WHEN hook registry empty, THEN handles gracefully."""
    # Arrange
    config_file = tmp_path / 'hooks.yaml'
    config_file.write_text('hooks: []')
    
    # Act: Create real registry with empty config
    registry = HookRegistry(config_path=config_file)
    hooks = registry.get_hooks()
    
    # Assert
    assert len(hooks) == 0
```

**Changes:**
- Line 120-121: Replace manual YAML parsing with real HookRegistry
- Line 122: Call real `get_hooks()` method

#### Test 3: test_hook_discovery_multiple_hooks

**Current (lines 125-160):**
```python
def test_hook_discovery_multiple_hooks(self, tmp_path):
    hooks_config = {...}  # 2 hooks
    config_file = tmp_path / 'hooks.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(hooks_config, f)
    with open(config_file) as f:
        registry_data = yaml.safe_load(f)
    assert len(registry_data['hooks']) == 2
    assert registry_data['hooks'][0]['id'] == 'hook-1'
    assert registry_data['hooks'][1]['id'] == 'hook-2'
```

**Replace with:**
```python
def test_hook_discovery_multiple_hooks(self, tmp_path):
    """WHEN multiple hooks registered, THEN all discovered."""
    # Arrange
    hooks_config = {
        'hooks': [
            {
                'id': 'hook-1',
                'name': 'Hook 1',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'conversation',
            },
            {
                'id': 'hook-2',
                'name': 'Hook 2',
                'operation_type': 'skill',
                'operation_pattern': 'qa',
                'trigger_status': ['success', 'partial'],
                'feedback_type': 'summary',
            },
        ]
    }

    config_file = tmp_path / 'hooks.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(hooks_config, f)
    
    # Act: Create real registry
    registry = HookRegistry(config_path=config_file)
    hooks = registry.get_hooks()
    
    # Assert
    assert len(hooks) == 2
    assert hooks[0].id == 'hook-1'
    assert hooks[1].id == 'hook-2'
```

**Changes:**
- Replace YAML parsing with HookRegistry instantiation
- Use real `get_hooks()` method
- Access `.id` property on real HookRegistryEntry objects

#### Test 4: test_hook_available_after_registration

**Current (lines 162-172):**
```python
def test_hook_available_after_registration(self, hook_system_config_file):
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)
    hook_ids = [hook['id'] for hook in registry_data['hooks']]
    assert 'test-hook-1' in hook_ids
```

**Replace with:**
```python
def test_hook_available_after_registration(self, hook_system_instance):
    """WHEN hook registered, THEN available for invocation."""
    # Act: Get registered hook IDs from real registry
    hook_ids = [hook.id for hook in hook_system_instance.registry.get_hooks()]
    
    # Assert
    assert 'test-hook-1' in hook_ids
```

#### Test 5: test_hook_metadata_preserved

**Current (lines 174-190):**
```python
def test_hook_metadata_preserved(self, hook_system_config_file):
    with open(hook_system_config_file) as f:
        registry_data = yaml.safe_load(f)
    hook = registry_data['hooks'][0]
    assert hook['id'] == 'test-hook-1'
    assert hook['name'] == 'Test Hook 1'
    # ... 6 more assertions on dict keys
```

**Replace with:**
```python
def test_hook_metadata_preserved(self, hook_system_instance):
    """WHEN hook loaded, THEN all metadata fields preserved."""
    # Act: Get hook from real registry
    hooks = hook_system_instance.registry.get_hooks()
    hook = hooks[0]
    
    # Assert: Verify real object properties
    assert hook.id == 'test-hook-1'
    assert hook.name == 'Test Hook 1'
    assert hook.operation_type == 'command'
    assert hook.operation_pattern == 'dev'
    assert hook.trigger_status == ['success']
    assert hook.feedback_type == 'conversation'
    assert hook.enabled is True
    assert hook.max_duration_ms == 5000
```

---

### Test Class 2: TestHookContextDataAvailability (7 tests)

**These tests can remain mostly unchanged** - They test context data structures which don't require real imports.

Keep these tests as-is (they're fine):
- `test_context_contains_required_fields`
- `test_context_invocation_id_unique`
- `test_context_timestamp_iso_format`
- `test_context_invocation_stack_tracking`
- `test_context_optional_fields`
- `test_context_token_usage_percentage`
- `test_context_status_values`

---

### Test Class 3: TestHookInvocationTrigger (4 tests)

#### Test: test_hook_invoked_on_operation_completion

**Current (lines 284-311):**
```python
@pytest.mark.asyncio
async def test_hook_invoked_on_operation_completion(self, operation_context):
    hook_config = {...}
    mock_hook_runner = Mock()
    mock_hook_runner.run = AsyncMock(return_value={'status': 'success'})
    if hook_config['enabled'] and 'success' in hook_config['trigger_status']:
        result = await mock_hook_runner.run(hook_config, operation_context)
    assert result is not None
    mock_hook_runner.run.assert_called_once()
```

**Replace with:**
```python
@pytest.mark.asyncio
async def test_hook_invoked_on_operation_completion(self, hook_system_instance, operation_context):
    """GIVEN operation completes, WHEN hooks match, THEN invoked with context."""
    # Arrange
    hook_config = {
        'id': 'test-hook',
        'operation_type': 'command',
        'operation_pattern': 'dev',
        'trigger_status': ['success'],
        'feedback_type': 'conversation',
        'enabled': True,
    }
    
    # Act: Create context and check if hook should be invoked
    should_invoke = (
        hook_config['enabled'] and 
        operation_context['status'] in hook_config['trigger_status']
    )
    
    # Assert: Hook should be invoked
    assert should_invoke is True
    assert hook_config['operation_pattern'] == 'dev'
```

**Changes:**
- Add `hook_system_instance` parameter (for future integration)
- Remove Mock/AsyncMock
- Test logic directly instead of mocking

#### Other tests in this class:
- `test_hook_pattern_matching_simple` - Keep as-is (simple logic test)
- `test_hook_pattern_not_matching` - Keep as-is
- `test_hook_invocation_with_all_context` - Update to use `hook_system_instance` if combining dicts

---

### Test Class 4: TestHookSystemIntegration (3 tests)

#### Test: test_hook_system_initialization

**Current (lines 365-377):**
```python
def test_hook_system_initialization(self, hook_system_config_file):
    config_path = hook_system_config_file.parent.parent / 'hooks.yaml'
    assert hook_system_config_file.exists()
    with open(hook_system_config_file) as f:
        config = yaml.safe_load(f)
    assert config is not None
    assert 'hooks' in config
```

**Replace with:**
```python
def test_hook_system_initialization(self, hook_system_instance):
    """WHEN hook system initializes, THEN loads config and validates registry."""
    # Assert: HookSystem initialized with real registry
    assert hook_system_instance is not None
    assert hook_system_instance.registry is not None
    assert hook_system_instance.circular_detector is not None
    assert hook_system_instance.invoker is not None
    assert hook_system_instance.pattern_matcher is not None
```

#### Test: test_hook_system_handles_missing_config

**Current (lines 379-388):**
```python
def test_hook_system_handles_missing_config(self, tmp_path):
    config_file = tmp_path / 'nonexistent.yaml'
    exists = config_file.exists()
    assert exists is False
```

**Can keep as-is** - Tests edge case handling

#### Test: test_hook_invocation_order_preserved

**Current (lines 390-419):**
```python
def test_hook_invocation_order_preserved(self, tmp_path):
    hooks_config = {...}  # 2 hooks
    hook_ids = [hook['id'] for hook in hooks_config['hooks']]
    assert hook_ids[0] == 'hook-1'
    assert hook_ids[1] == 'hook-2'
```

**Replace with:**
```python
def test_hook_invocation_order_preserved(self, tmp_path):
    """WHEN multiple hooks match, THEN invoked in registration order."""
    # Arrange
    hooks_config = {
        'hooks': [
            {
                'id': 'hook-1',
                'name': 'Hook 1',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'conversation',
                'enabled': True,
            },
            {
                'id': 'hook-2',
                'name': 'Hook 2',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'summary',
                'enabled': True,
            },
        ]
    }
    
    # Create registry with ordered hooks
    config_file = tmp_path / 'hooks.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(hooks_config, f)
    
    registry = HookRegistry(config_path=config_file)
    hooks = registry.get_hooks()
    
    # Assert: Order preserved
    assert hooks[0].id == 'hook-1'
    assert hooks[1].id == 'hook-2'
```

---

## Step 4: Verify Coverage Improves (15 minutes)

### Command 1: Run pilot test file
```bash
python3 -m pytest tests/test_hook_system.py -v
```

**Expected output:**
```
============================= test session starts ==============================
tests/test_hook_system.py::TestHookRegistrationAndDiscovery::test_load_hook_registry_from_yaml PASSED
tests/test_hook_system.py::TestHookRegistrationAndDiscovery::test_hook_registry_empty_config PASSED
...
======================== 19 passed in 1.23s ============================
```

### Command 2: Check coverage improvement
```bash
python3 -m pytest tests/test_hook_system.py --cov=src/hook_system --cov=src/hook_registry --cov-report=term-missing
```

**Expected output:**
```
---------- coverage: platform linux, python 3.12.3 -----------
Name                    Stmts   Miss  Cover   Missing
--------------------------------------------------
src/hook_system.py        61     35    43%    45-99, 110-222
src/hook_registry.py     230    165    28%    70-405
--------------------------------------------------
TOTAL                    291    200    31%

============================= 19 passed in 1.84s ============================
```

**Interpretation:**
- ✅ All tests still pass (behavior preserved)
- ✅ Coverage improved from 0% to ~31% for these 2 modules
- 🟡 Not all code covered yet (need other test files)

---

## Summary of Changes

### Lines Changed by Category

| Category | Count | Example |
|----------|-------|---------|
| Imports added | 4 | `from src.hook_system import HookSystem` |
| Fixtures added | 1 | `hook_system_instance` |
| Fixtures modified | 0 | (Used existing `hook_system_config_file`) |
| Tests modified | 9 | Replaced YAML parsing with real class calls |
| Tests kept as-is | 10 | Context data, simple logic tests |
| **Total Changes** | **~80 lines** | ~5 lines per modified test |

---

## Testing Checklist

Before moving to Phase 2, verify:

- [ ] All 4 imports added successfully
- [ ] New `hook_system_instance` fixture created
- [ ] 9 test methods updated with real imports
- [ ] All 19 tests pass: `pytest tests/test_hook_system.py -v`
- [ ] Coverage improved from 0% to 15-25%
- [ ] No errors in import statements
- [ ] No attribute errors (accessing wrong object properties)

---

## Next Steps After Pilot

**If successful (all tests pass, coverage improves):**
1. Commit changes: `git add tests/test_hook_system.py`
2. Move to Phase 2: `test_hook_patterns.py` (use same pattern)
3. Move to Phase 3: `test_hook_circular.py`
4. Continue until all 8 files refactored

**If issues arise:**
1. Check error message
2. Verify import statements (Python path)
3. Check object properties (HookRegistryEntry has `.id`, not `['id']`)
4. Revert and debug (git checkout tests/test_hook_system.py)

---

## Key Learning for Other Files

After completing this pilot:

1. **Import Pattern:** All 6 source modules follow same pattern
2. **Fixture Pattern:** Create real object instances
3. **Test Pattern:** Call real methods instead of mocking
4. **Assertion Pattern:** Access object properties, not dict keys

---

## References

- **Full Analysis:** TEST-COVERAGE-REFACTORING-ANALYSIS.md
- **Executive Summary:** COVERAGE-REFACTORING-EXECUTIVE-SUMMARY.md
- **Source Code:** src/hook_system.py, src/hook_registry.py, etc.
- **Current Tests:** tests/test_hook_system.py

