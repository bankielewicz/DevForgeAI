# STORY-185: Manual CLI Integration Tests

**Purpose:** Document manual CLI testing attempted for STORY-185
**Date:** 2025-01-07
**Status:** Feature Not Yet Implemented

---

## Test Scenarios Attempted

### 1. CLI Test: `devforgeai check-hooks --operation dev --status success --type user`

**Command:**
```bash
python3 -m devforgeai_cli.commands.check_hooks \
  --operation dev \
  --status success \
  --type user
```

**Expected Result:**
- Exit code: 0 (trigger) or 1 (don't trigger)
- No error message

**Actual Result:**
```
devforgeai check-hooks: error: unrecognized arguments: --type user
Exit code: 2
```

**Status:** FAILED ✗ - Feature not implemented

---

### 2. CLI Test: `devforgeai check-hooks --operation dev --status success --type ai`

**Command:**
```bash
python3 -m devforgeai_cli.commands.check_hooks \
  --operation dev \
  --status success \
  --type ai
```

**Expected Result:**
- Exit code: 0 or 1
- No error

**Actual Result:**
```
devforgeai check-hooks: error: unrecognized arguments: --type ai
Exit code: 2
```

**Status:** FAILED ✗ - Feature not implemented

---

### 3. CLI Test: `devforgeai check-hooks --operation dev --status success --type all`

**Command:**
```bash
python3 -m devforgeai_cli.commands.check_hooks \
  --operation dev \
  --status success \
  --type all
```

**Expected Result:**
- Exit code: 0 or 1
- Processes all hooks regardless of type

**Actual Result:**
```
devforgeai check-hooks: error: unrecognized arguments: --type all
Exit code: 2
```

**Status:** FAILED ✗ - Feature not implemented

---

### 4. CLI Test: `devforgeai check-hooks --operation dev --status success --type invalid`

**Command:**
```bash
python3 -m devforgeai_cli.commands.check_hooks \
  --operation dev \
  --status success \
  --type invalid
```

**Expected Result:**
- Exit code: 2 (error)
- Error message like: "Invalid type 'invalid'. Must be one of: user, ai, all"

**Actual Result:**
```
devforgeai check-hooks: error: unrecognized arguments: --type invalid
Exit code: 2
```

**Status:** PARTIALLY MET (Error code correct, message not specific to invalid type choice)

---

### 5. CLI Test: `devforgeai check-hooks --help`

**Command:**
```bash
python3 -m devforgeai_cli.commands.check_hooks --help
```

**Expected Output (excerpt):**
```
optional arguments:
  -h, --help            show this help message and exit
  --operation OPERATION
                        Operation name (e.g., dev, qa, release)
  --status {success,failure,partial}
                        Operation status
  --type {user,ai,all}
                        Hook type to check (user, ai, or all)
  --config CONFIG       Path to hooks.yaml config file
```

**Actual Output:**
```
usage: devforgeai check-hooks [-h] --operation OPERATION --status
                              {success,failure,partial} [--config CONFIG]
devforgeai check-hooks: optional arguments:
  -h, --help            show this help message and exit
  --operation OPERATION
                        Operation name (e.g., dev, qa, release)
  --status {success,failure,partial}
                        Operation status
  --config CONFIG       Path to hooks.yaml config file (default: devforgeai/config/hooks.yaml)
```

**Status:** FAILED ✗ - `--type` option not documented

---

## Python Module Testing

### Test 1: Module accepts `hook_type='user'`

**Test:**
```python
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='user')
```

**Expected:** `exit_code` in [0, 1, 2]

**Actual Result:**
```
TypeError: check_hooks_command() got an unexpected keyword argument 'hook_type'
```

**Status:** FAILED ✗

---

### Test 2: Module accepts `hook_type='ai'`

**Test:**
```python
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='ai')
```

**Expected:** `exit_code` in [0, 1, 2]

**Actual Result:**
```
TypeError: check_hooks_command() got an unexpected keyword argument 'hook_type'
```

**Status:** FAILED ✗

---

### Test 3: Module accepts `hook_type='all'`

**Test:**
```python
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='all')
```

**Expected:** `exit_code` in [0, 1, 2]

**Actual Result:**
```
TypeError: check_hooks_command() got an unexpected keyword argument 'hook_type'
```

**Status:** FAILED ✗

---

### Test 4: Module rejects invalid `hook_type`

**Test:**
```python
from devforgeai_cli.commands.check_hooks import check_hooks_command
exit_code = check_hooks_command('dev', 'success', hook_type='invalid')
```

**Expected:** `exit_code` == 2 (error)

**Actual Result:**
```
TypeError: check_hooks_command() got an unexpected keyword argument 'hook_type'
```

**Status:** FAILED ✗

---

## Current Implementation Status

### What's Implemented

- ✓ Argument parser created
- ✓ Basic configuration loading
- ✓ Exit codes (0, 1, 2)
- ✓ Operation and status validation
- ✓ Circular invocation detection
- ✓ Trigger rule evaluation

### What's Missing for STORY-185

- ✗ `--type` argument in parser
- ✗ `hook_type` parameter in function
- ✗ Hook filtering by `hook_type` field
- ✗ Type validation with clear error messages
- ✗ Help text documentation for `--type`

---

## Implementation Plan

To make all CLI tests pass, implement the following:

### 1. Update Argument Parser (lines 297-330)

**Location:** `src/claude/scripts/devforgeai_cli/commands/check_hooks.py`

**Add after line 327 (after --config argument):**
```python
parser.add_argument(
    '--type',
    type=str,
    choices=['user', 'ai', 'all'],
    default='all',
    help='Hook type to check (user, ai, or all)'
)
```

### 2. Update Function Signature (line 227-247)

**Change from:**
```python
def check_hooks_command(
    operation: str,
    status: str,
    config_path: Optional[str] = None,
) -> int:
```

**Change to:**
```python
def check_hooks_command(
    operation: str,
    status: str,
    hook_type: str = 'all',
    config_path: Optional[str] = None,
) -> int:
```

### 3. Add Hook Filtering Logic (after line 290)

**Add after hook processing, before trigger check:**
```python
# AC3: Filter hooks by type if specified
if hook_type != 'all':
    # Get hooks from config if available
    if 'hooks' in config:
        config['hooks'] = [h for h in config['hooks']
                          if h.get('hook_type') == hook_type]
```

### 4. Pass Type to Function (line 338-342)

**Change from:**
```python
exit_code = check_hooks_command(
    operation=args.operation,
    status=args.status,
    config_path=args.config,
)
```

**Change to:**
```python
exit_code = check_hooks_command(
    operation=args.operation,
    status=args.status,
    hook_type=args.type,
    config_path=args.config,
)
```

---

## Expected Results After Implementation

### CLI Tests Results

```bash
# Test 1: --type user
$ python3 -m devforgeai_cli.commands.check_hooks --operation dev --status success --type user
# Exit code: 0 or 1 (depending on configuration)

# Test 2: --type ai
$ python3 -m devforgeai_cli.commands.check_hooks --operation dev --status success --type ai
# Exit code: 0 or 1

# Test 3: --type all
$ python3 -m devforgeai_cli.commands.check_hooks --operation dev --status success --type all
# Exit code: 0 or 1

# Test 4: --type invalid
$ python3 -m devforgeai_cli.commands.check_hooks --operation dev --status success --type invalid
# usage: devforgeai check-hooks [-h] --operation OPERATION --status
#                               {success,failure,partial} [--type {user,ai,all}]
#                               [--config CONFIG]
# devforgeai check-hooks: error: argument --type: invalid choice: 'invalid'
# (choose from 'user', 'ai', 'all')
# Exit code: 2

# Test 5: --help
$ python3 -m devforgeai_cli.commands.check_hooks --help
# (includes --type {user,ai,all} documentation)
```

### Module Tests Results

```python
# All tests accept hook_type parameter and return valid exit codes
from devforgeai_cli.commands.check_hooks import check_hooks_command

# Test 1: hook_type='user'
exit_code = check_hooks_command('dev', 'success', hook_type='user')
# exit_code in [0, 1, 2] ✓

# Test 2: hook_type='ai'
exit_code = check_hooks_command('dev', 'success', hook_type='ai')
# exit_code in [0, 1, 2] ✓

# Test 3: hook_type='all'
exit_code = check_hooks_command('dev', 'success', hook_type='all')
# exit_code in [0, 1, 2] ✓

# Test 4: hook_type='invalid'
exit_code = check_hooks_command('dev', 'success', hook_type='invalid')
# exit_code == 2 (error) ✓
```

---

## Summary

**Manual CLI Testing Results:**
- 5 test scenarios attempted
- 0 passed (feature not implemented)
- 5 failed (all due to missing --type flag)

**Integration Test Results:**
- 27 automated tests created
- 14 passed (helper functions and backward compatibility)
- 13 failed (all due to missing feature)

**Readiness for Implementation:**
- ✓ Test suite complete and comprehensive
- ✓ Clear failure points documented
- ✓ Implementation plan provided
- ✓ Expected results documented

**Recommendation:** Implement the 4-step changes above (~15-20 min), then run automated test suite to verify all 27 tests pass.
