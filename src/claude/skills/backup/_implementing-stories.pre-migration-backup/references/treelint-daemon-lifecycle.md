# Treelint Daemon Lifecycle Management

**Purpose:** Manage Treelint daemon lifecycle during DevForgeAI workflows, providing sub-5ms query performance with explicit user consent and transparent CLI fallback.

**Reference:** EPIC-058 (Treelint Advanced Features), ADR-013 (Treelint Integration), STORY-374

---

## Overview

The Treelint daemon provides a persistent background process that keeps the AST index in memory, reducing query latency from ~200ms (CLI mode) to <5ms (daemon mode) -- a 40x improvement. This reference documents the complete daemon lifecycle: status checking, user-prompted start, graceful decline handling, failure fallback, orphan process prevention, performance validation, and session suppression.

**EPIC-058 Constraint:** Daemon lifecycle is managed by the user. Claude MUST NOT start the daemon without explicit user consent.

---

## Configuration Defaults

| Parameter | Default Value | Range | Description |
|-----------|---------------|-------|-------------|
| `daemon_start_timeout_seconds` | `3` | 1-10 | Maximum wait time for `treelint daemon start` to return control |
| `status_check_timeout_ms` | `200` | 100-2000 | Maximum wait time for `treelint daemon status --format json` |
| `health_check_grace_period_ms` | `2000` | 1000-5000 | Wait time after daemon start before verifying health |

---

## Step 1: Daemon Status Check (Pre-Flight)

Before executing any Treelint query that benefits from daemon mode, the integration layer MUST first check daemon status. This status check executes before queries as a pre-flight gate.

### Command

```bash
Bash(command="treelint daemon status --format json", timeout=200)
```

### JSON Response Structure

The daemon status command returns a JSON response containing a `"status"` field:

```json
{
  "status": "running",
  "pid": 12345,
  "uptime_seconds": 3600,
  "index_path": ".treelint/index.db"
}
```

### Parsing the JSON Response

Parse the JSON response to extract the `"status"` field. Valid values are:

| Status Value | Meaning | Next Action |
|--------------|---------|-------------|
| `running` | Daemon is active and ready | Proceed with daemon-mode queries |
| `stopped` | Daemon is not running | Prompt user (Step 2) |
| `unknown` | Status cannot be determined | Treat as stopped, prompt user |

### Status Check Timeout

The status check uses a 200ms timeout. If the check does not complete within 200ms, treat the result as `unknown` and follow the stopped code path.

### Decision Logic

Based on the daemon state, the integration layer branches to the appropriate code path:

```
IF status == "running":
    Use daemon mode for queries (fast path, <5ms)
ELIF status == "stopped" OR status == "unknown":
    IF daemon_prompt_suppressed == true:
        Use CLI mode (skip prompt)
    ELSE:
        Prompt user via AskUserQuestion (Step 2)
```

---

## Step 2: User-Prompted Daemon Start

When the daemon status is stopped, Claude prompts the user via AskUserQuestion. Claude MUST NOT start the daemon without explicit user consent per EPIC-058 constraint. No silent auto-start is permitted.

### AskUserQuestion Template

```yaml
Question: "The Treelint daemon is not running. Starting it would improve AST query performance from CLI speed (~200ms per query) to daemon speed (~5ms per query). Would you like to start the daemon?"
Header: "Treelint Daemon"
Options:
  - "Yes, start the daemon (recommended for faster queries)"
  - "No, continue with CLI mode (~200ms per query)"
  - "No, and don't ask again this session (suppress future prompts)"
multiSelect: false
```

### Option Handling

| Option Selected | Action |
|-----------------|--------|
| **Yes, start the daemon** | Execute `treelint daemon start` (Step 2a) |
| **No, continue with CLI mode** | Fall back to CLI mode immediately (Step 3) |
| **No, and don't ask again this session** | Set `daemon_prompt_suppressed = true`, use CLI mode (Step 7) |

### User Consent Requirement

- AskUserQuestion invocation MUST precede any `treelint daemon start` command
- If AskUserQuestion is bypassed, HALT workflow with EPIC-058 constraint violation
- The performance benefit explanation (200ms to 5ms) helps the user make an informed decision

### Step 2a: Execute Daemon Start

Only after user consent, execute the daemon start command:

```bash
Bash(command="treelint daemon start", timeout=3000)
```

The daemon start command has a 3-second timeout. If the command does not return within 3 seconds, treat it as a failure (Step 4).

After the start command returns successfully (exit code 0), wait for the 2-second health check grace period before verifying the daemon is healthy:

```bash
# Wait for health check grace period (2 seconds)
sleep 2

# Verify daemon health
Bash(command="treelint daemon status --format json", timeout=200)
```

If the health check confirms `"status": "running"`, proceed with daemon-mode queries.

If the daemon crashes within the 2-second grace period (health check returns `stopped` or `unknown`), treat it as a start failure (Step 4).

---

## Step 3: Graceful Decline Handling

When the user declines the daemon start (selects "No, continue with CLI mode"), the workflow continues immediately using CLI mode without daemon. No error is raised, and the workflow proceeds gracefully.

### CLI Mode Fallback Behavior

- The workflow continues immediately using CLI mode
- Queries execute via direct CLI invocation: `treelint search --format json` (without daemon)
- No error is raised on decline -- this is a valid, expected code path
- Performance degrades gracefully to CLI-mode latency (~200ms per query instead of ~5ms)
- The user is not warned or prompted again unless they chose the suppress option

**Note:** Both decline paths result in CLI mode. The "don't ask again" variant additionally sets the session suppression flag (see Step 7).

---

## Step 4: Start Failure Fallback

When the user consents to daemon start but the start fails, the integration layer handles the failure transparently and falls back to CLI mode.

### Failure Scenarios

| Failure Type | Detection | Handling |
|-------------|-----------|----------|
| **Non-zero exit code** | `treelint daemon start` returns exit code != 0 | Log error, fall back to CLI |
| **Timeout** | Command exceeds 3-second timeout | Kill process, log timeout, fall back to CLI |
| **Port/socket conflict** | Exit code indicates EADDRINUSE or address already in use | Log conflict, fall back to CLI |
| **Crash within grace period** | Health check after 2-second grace period returns stopped | Log failure, fall back to CLI |

### Failure Handling Procedure

1. **Log the failure** with the specific error message from the daemon start command
2. **Inform the user** that daemon start failed and CLI mode is being used instead:
   ```
   "Treelint daemon start failed: [error message]. Continuing with CLI mode (~200ms per query)."
   ```
3. **Fall back to CLI mode** transparently -- the workflow continues without interruption
4. **Zero retries** -- the daemon start is not retried within the same workflow invocation (BR-002)
5. The workflow continues seamlessly without daemon

**Health check:** See Step 2a for the post-start health check procedure. If the health check fails, follow the fallback procedure above.

---

## Step 5: Orphaned Process Prevention

The framework prevents orphaned daemon processes through PID file management and stale artifact cleanup.

### PID File Management

The daemon PID is recorded in `.treelint/daemon.pid` when the daemon starts. This PID file is used to:

- Track which process is the active daemon
- Verify the daemon process is still alive
- Detect stale PID files from previous sessions

### PID Verification

To check if the PID file references a running process:

```bash
# Read PID from file
PID=$(cat .treelint/daemon.pid 2>/dev/null)

# Verify process is alive using kill -0
if kill -0 "$PID" 2>/dev/null; then
    echo "Daemon process $PID is alive"
else
    echo "Daemon process $PID is dead (stale PID file)"
fi
```

### Stale PID File Detection and Cleanup

A stale PID file exists when the PID references a dead process (the process exited but the PID file was not cleaned up). When a stale PID file is detected:

1. Remove the stale PID file: `rm .treelint/daemon.pid`
2. Log the cleanup: "Cleaned up stale PID file referencing dead process [PID]"

### Orphaned Socket File Cleanup

An orphaned socket file (`.treelint/daemon.sock`) may exist if the daemon crashed without cleaning up. When an orphaned socket is detected (socket file exists but no daemon process is attached):

1. Remove the orphaned socket file: `rm .treelint/daemon.sock`
2. Log the cleanup: "Cleaned up orphaned daemon socket file"

### Cleanup Before Daemon Start

Stale PID files and orphaned socket files are cleaned up before any daemon start attempt. This cleanup prevents EADDRINUSE errors and ensures a clean start:

```
Pre-Start Cleanup Sequence:
1. Check if .treelint/daemon.pid exists
2. If PID file exists, verify process is alive (kill -0)
3. If process is dead, remove stale PID file
4. Check if .treelint/daemon.sock exists without active process
5. If orphaned socket exists, remove it
6. Proceed with daemon start
```

### Daemon Left Running After Workflow

Per EPIC-058 (user-managed daemon lifecycle), the daemon is left running after workflow completion. The framework MUST NOT stop the daemon -- no `treelint daemon stop` command is issued by the framework. The user manages the daemon lifecycle independently.

---

## Step 6: Performance Validation

Daemon mode provides a significant performance benefit over CLI mode. The daemon keeps the `.treelint/index.db` SQLite index in memory, avoiding cold-start overhead on each query.

### Performance Targets

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Daemon query latency | < 5ms (p95) | Wall-clock time from command invocation to JSON response receipt |
| CLI query latency | ~200ms | Wall-clock elapsed time for CLI invocation |
| Status check latency | < 200ms | Wall-clock time for status query |
| Daemon start time | < 3 seconds | Wall-clock time for start command |

Performance targets are defined in the table above. The 40x improvement (daemon vs CLI) is the primary justification for daemon usage.

### Measurement Protocol

Performance is measured using wall-clock time:

```bash
# Measure daemon query latency
START=$(date +%s%N)
treelint search --type function --name "validate*" --format json
END=$(date +%s%N)
ELAPSED_MS=$(( (END - START) / 1000000 ))
echo "Query completed in ${ELAPSED_MS}ms"
```

### SQLite Index Requirement

The `.treelint/index.db` SQLite index must exist for daemon queries to achieve the <5ms target. If the index does not exist, the daemon must build it on first query, which will exceed the 5ms target. Subsequent queries will be fast once the index is populated.

---

## Step 7: Session Suppression

When the user selects "No, and don't ask again this session", the daemon start prompt is suppressed for the remainder of the Claude Code session.

### Suppression Flag: `daemon_prompt_suppressed`

The session suppression flag `daemon_prompt_suppressed` controls whether the daemon start prompt is shown:

| Property | Value |
|----------|-------|
| Type | Boolean (in-memory only) |
| Default | `false` (initially false) |
| Set to true | When user selects suppress option ("don't ask again this session") |
| Scope | Current Claude Code session only |
| Persistence | In-memory only -- no persistent file is written |
| Reset | Resets to false on new session start |

### Suppression Behavior

When `daemon_prompt_suppressed` is set to `true`:

1. Subsequent daemon status checks that find the daemon stopped will skip the AskUserQuestion prompt
2. CLI mode is used automatically without prompting (no AskUserQuestion invoked)
3. The suppression remains active for the remainder of the session
4. The flag resets on new session start (each new Claude Code session starts fresh)

### Suppression Flow

The suppression flag integrates into the Step 1 decision logic. When `daemon_prompt_suppressed == true` and daemon status is stopped/unknown, CLI mode is used automatically (skipping AskUserQuestion). See Step 1 Decision Logic for the complete branching.

---

## Complete Workflow Diagram

```
Treelint Query Requested
        |
        v
[Step 1] Check daemon status
        |
    +---+---+
    |       |
 running  stopped/unknown
    |       |
    |   Check daemon_prompt_suppressed
    |       |
    |   +---+---+
    |   |       |
    |  false   true
    |   |       |
    |  [Step 2] Skip prompt
    |  AskUser  |
    |   |       |
    |  +--+--+  |
    |  |  |  |  |
    | Yes No Suppress
    |  |  |     |
    |  |  |  Set flag=true
    |  |  |     |
    |  |  +--+--+
    |  |     |
    |  |  [Step 3]
    |  |  CLI Mode
    |  |  (~200ms)
    |  |
    | [Step 2a]
    | Cleanup stale files (Step 5)
    | treelint daemon start
    |     |
    |  +--+--+
    |  |     |
    | OK   Fail
    |  |     |
    | Health [Step 4]
    | Check  CLI Fallback
    |  |     (zero retries)
    |  |
    v  v
  Daemon Mode    CLI Mode
  (< 5ms)       (~200ms)
```

---

## Business Rules

| ID | Rule | Priority |
|----|------|----------|
| BR-001 | Claude MUST NOT start the Treelint daemon without explicit user consent via AskUserQuestion | Critical |
| BR-002 | Daemon start failures result in CLI fallback with zero retries within the same workflow invocation | High |
| BR-003 | The daemon is left running after workflow completion (user-managed lifecycle per EPIC-058) | High |
| BR-004 | Stale PID files and orphaned socket files are cleaned up before daemon start attempts | Medium |

## Non-Functional Requirements

| ID | Category | Requirement | Metric |
|----|----------|-------------|--------|
| NFR-001 | Performance | Daemon queries complete within 5ms | < 5ms wall-clock (p95) |
| NFR-002 | Performance | Status check completes within 200ms | < 200ms wall-clock |
| NFR-003 | Performance | Daemon start completes within 3 seconds | < 3s wall-clock |
| NFR-004 | Security | No privilege escalation in daemon commands | Zero sudo/setuid/runas |
| NFR-005 | Security | User consent required before daemon start | AskUserQuestion count >= start count |
| NFR-006 | Reliability | No orphan daemon processes | PID file matches running process |

---

## Error Handling Summary

| Error | Detection | Response | Retry? |
|-------|-----------|----------|--------|
| Status check timeout | >200ms elapsed | Treat as `unknown`, follow stopped path | No |
| Daemon start non-zero exit code | Exit code != 0 | Log error, inform user, CLI fallback | No (zero retries) |
| Daemon start timeout | >3 seconds elapsed | Kill, log timeout, CLI fallback | No |
| Port/socket conflict (EADDRINUSE) | Address already in use error | Log conflict, CLI fallback | No |
| Health check failure | Status not `running` after 2-second grace period | Log failure, CLI fallback | No |
| Stale PID file | kill -0 fails for recorded PID | Remove PID file, log cleanup | N/A |
| Orphaned socket | Socket exists, no process attached | Remove socket file, log cleanup | N/A |
| Treelint not installed | Command not found (exit 127) | CLI fallback to Grep | No |

---

## Fallback Chain

The complete fallback chain for Treelint queries:

```
1. Daemon Mode (< 5ms)      -- Preferred when daemon is running
        |
   (daemon unavailable)
        |
        v
2. CLI Mode (~200ms)         -- Direct treelint CLI invocation
        |
   (treelint unavailable)
        |
        v
3. Grep Fallback (~200ms)   -- Native Grep tool (text matching, no AST)
```

---

## References

- **EPIC-058:** Treelint Advanced Features
- **ADR-013:** Treelint Integration for AST-Aware Code Search
- **STORY-370:** Integrate Dependency Graph Analysis (fallback chain pattern)
- **STORY-374:** Implement Daemon Auto-Start Logic
- **tech-stack.md:** Treelint v0.12.0+ approved (Source: devforgeai/specs/context/tech-stack.md, lines 104-114)
- **source-tree.md:** `.treelint/` directory structure (Source: devforgeai/specs/context/source-tree.md, lines 328-331)
