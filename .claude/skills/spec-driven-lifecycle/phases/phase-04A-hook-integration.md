# Phase 04A: Hook Integration

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=03A --to=04A
```

## Contract

PURPOSE: Execute feedback hook integration after deferral audit completion. Non-blocking - hook failures do not prevent audit success. Audit Deferrals mode only.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Hook invocation logged (if eligible)
STEP COUNT: 7 mandatory steps

---

## Mandatory Steps

### Step 1: Check Eligibility

EXECUTE: Verify hooks are configured and audit-deferrals operation is hook-eligible.
```
# Check for hooks configuration
hooks_config = Glob(pattern="devforgeai/feedback/config.yaml")
IF hooks_config is empty:
  hook_eligible = false
  Display: "No hooks configuration found - skipping hook integration"
ELSE:
  Read(file_path=hooks_config[0])
  Grep(pattern="audit-deferrals.*enabled", path=hooks_config[0])
  hook_eligible = (match found AND value is true)
```

VERIFY: hook_eligible flag is set.
```
IF hook_eligible == false:
  Display: "Hook integration skipped (not eligible)"
  # Skip remaining steps - proceed to Exit Gate
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=1`

### Step 2: Prepare Context

EXECUTE: Extract audit metadata for hook context.
```
IF hook_eligible == false: SKIP

hook_context = {
  "operation": "audit-deferrals",
  "timestamp": current_timestamp,
  "stories_audited": audit_story_count,
  "deferrals_found": deferral_count,
  "violations": violation_count,
  "resolvable_count": len(findings["MEDIUM"]),
  "critical_count": len(findings["CRITICAL"]),
  "report_path": audit_report_path
}
```

VERIFY: hook_context has all required fields.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=2`

### Step 3: Sanitize Data

EXECUTE: Remove sensitive information before passing to hooks.
```
IF hook_eligible == false: SKIP

# Remove any credentials, API keys, or secrets from context
# Sanitize story content (remove code blocks with potential secrets)
sanitized_context = sanitize(hook_context)

# Verify no sensitive patterns remain
Grep(pattern="(password|secret|api.key|token)", text=sanitized_context)
IF match: Remove matched content
```

VERIFY: No sensitive patterns in sanitized context.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=3`

### Step 4: Invoke Hooks

EXECUTE: Call devforgeai-validate invoke-hooks with audit context.
```
IF hook_eligible == false: SKIP

Bash(command="source .venv/bin/activate && devforgeai-validate invoke-hooks --operation=audit-deferrals --context='{sanitized_context}' 2>&1")
```

VERIFY: Hook invocation completed (exit code captured, regardless of success/failure).
```
# Non-blocking: capture result but don't HALT on failure
IF exit_code != 0:
  hook_result = "failed"
  Display: "Hook invocation failed (non-blocking): exit code {exit_code}"
ELSE:
  hook_result = "success"
  Display: "Hook invocation successful"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=4`

### Step 5: Log Invocation

EXECUTE: Append hook invocation record to log file.
```
IF hook_eligible == false: SKIP

log_entry = "[{timestamp}] audit-deferrals hook: {hook_result} | stories={audit_story_count} deferrals={deferral_count} violations={violation_count}"

# Ensure log directory exists
log_path = "devforgeai/feedback/logs/hook-invocations.log"
# Append to log (create if not exists)
```

VERIFY: Log entry written.
```
Grep(pattern="audit-deferrals hook", path=log_path)
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=5`

### Step 6: Handle Errors Gracefully

EXECUTE: If hook invocation failed, ensure audit continues successfully.
```
IF hook_eligible == false: SKIP

IF hook_result == "failed":
  Display: "Hook integration failed but audit completed successfully."
  Display: "Hook error logged to: {log_path}"
  # Non-blocking: continue to finalization
```

VERIFY: Error handling complete (no HALT on hook failure).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=6`

### Step 7: Prevent Circular Invocations

EXECUTE: Verify no circular command -> hook -> command -> hook loop.
```
IF hook_eligible == false: SKIP

# Check invocation depth
Grep(pattern="audit-deferrals hook", path=log_path, output_mode="count")
recent_invocations = count of entries in last 5 minutes

IF recent_invocations > 2:
  Display: "Warning: Potential circular invocation detected ({recent_invocations} in 5 min)"
  Display: "Skipping further hook invocations to prevent loop"
```

VERIFY: No circular invocation detected or mitigated.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04A --step=7`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=04A --checkpoint-passed
```
