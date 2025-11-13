# User Guide: How to Enable/Disable Hooks for /dev

## Enabling Hooks

**Default Configuration** (`.devforgeai/config/hooks.yaml`):
```yaml
hooks:
  enabled: true           # Master switch for all hooks
  mode: "all"            # Options: "all", "failures_only", "none"
  operations:
    dev:
      enabled: true       # Enable hooks for /dev command
      on_success: true    # Trigger on successful completion
      on_failure: false   # Don't trigger on failure
```

**To enable feedback hooks for /dev:**
1. Ensure `.devforgeai/config/hooks.yaml` has `hooks.enabled: true`
2. Set `hooks.operations.dev.enabled: true`
3. Configure trigger conditions:
   - `on_success: true` - Feedback after successful /dev completion
   - `on_failure: true` - Feedback after /dev failure
4. Run `/dev STORY-ID` - feedback will trigger automatically if configured

## Disabling Hooks

**Option 1: Disable all hooks globally**
```yaml
hooks:
  enabled: false    # Master switch OFF
```

**Option 2: Disable only /dev hooks**
```yaml
hooks:
  enabled: true
  operations:
    dev:
      enabled: false    # /dev hooks OFF, other commands unaffected
```

**Option 3: Use failures-only mode**
```yaml
hooks:
  mode: "failures_only"    # Only trigger on failures
  operations:
    dev:
      on_success: false    # Skip feedback on success
      on_failure: true     # Feedback only when /dev fails
```

**Option 4: Use skip tracking to auto-disable**
- Skip feedback 3 times in a row
- System will prompt: "You've skipped 3 times - disable hooks?"
- Select "Yes" to automatically update config to `enabled: false`

## Configuration Reference

**File:** `.devforgeai/config/hooks.yaml`

**Key Settings:**
- `hooks.enabled` - Master switch (true/false)
- `hooks.mode` - Global mode ("all", "failures_only", "none")
- `hooks.operations.dev.enabled` - /dev-specific switch
- `hooks.operations.dev.on_success` - Trigger on success
- `hooks.operations.dev.on_failure` - Trigger on failure
- `hooks.operations.dev.skip_tracking.enabled` - Enable skip tracking
- `hooks.operations.dev.skip_tracking.threshold` - Skip count before disable prompt (default: 3)

**To verify configuration:**
```bash
# Check if hooks enabled for /dev
devforgeai check-hooks --operation=dev --status=completed

# Exit code 0 = hooks will trigger
# Exit code 1 = hooks will skip
```

---

**Created:** 2025-11-13 (STORY-023)
**Related:** STORY-021 (check-hooks), STORY-022 (invoke-hooks), EPIC-006
