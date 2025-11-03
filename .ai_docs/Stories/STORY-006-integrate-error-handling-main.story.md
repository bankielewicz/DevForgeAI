---
id: STORY-006
title: Integrate Error Handling in main.rs
epic: EPIC-001
sprint: Backlog
status: Backlog
points: 2
priority: High
dependencies:
  prerequisite_stories:
    - STORY-004
    - STORY-005
created: 2025-11-03
---

# STORY-006: Integrate Error Handling in main.rs

## User Story

As a CLI user,
I want errors to produce proper exit codes and formatted output,
so that TreeLint Codelens can be used in scripts and CI/CD pipelines.

## Context

**Created to resolve:** Circular deferral between STORY-004 and STORY-005
- STORY-004 deferred exit code handling to STORY-005
- STORY-005 deferred error integration to STORY-004
- Gap remains: main.rs error flow integration not completed in either story

**Identified by:** RCA-006 Deferral Validation Analysis

This story explicitly owns the integration work that was ambiguous between STORY-004 and STORY-005.

---

## Acceptance Criteria

### Scenario 1: Errors Exit with Code 2
**Given** the analyze command encounters an error (file not found, parse error, invalid config)
**When** an error occurs during execution
**Then** the process exits with code 2
**And** the error message is printed to stderr (not stdout)

### Scenario 2: Success Exits with Code 0
**Given** the analyze command completes successfully
**When** no errors occur (even if violations found - violations are not errors)
**Then** the process exits with code 0

### Scenario 3: JSON Errors Output to Stderr
**Given** an error occurs
**And** --format json is specified
**When** the error is output
**Then** a JSON error object is printed to stderr
**And** the error uses ErrorResponse struct from STORY-004

### Scenario 4: Error Chain Shown with RUST_BACKTRACE
**Given** an error occurs
**And** RUST_BACKTRACE=1 environment variable is set
**When** the error is printed
**Then** the full error chain is shown (via anyhow)
**And** each context layer is visible

---

## Technical Specification

### Error Handler Wrapper in main.rs

**File:** `src/bin/treelint.rs` (or `src/main.rs` depending on source-tree.md)

**Implementation Pattern:**

```rust
use anyhow::Result;
use treelint::cli::Cli;
use treelint::cli::output::{output_error, OutputFormat};
use treelint::core::ErrorResponse;

fn main() {
    std::process::exit(match run() {
        Ok(()) => 0,
        Err(e) => {
            // Get format from CLI args (or default to text)
            let format = OutputFormat::Text; // Extract from CLI if --format specified

            // Convert anyhow::Error to ErrorResponse
            let error_response = ErrorResponse::new(
                "ExecutionError",
                format!("{}", e)
            );

            // Output error to stderr
            if let Err(output_err) = output_error(&error_response, format) {
                eprintln!("Failed to output error: {}", output_err);
            }

            // Print error chain if RUST_BACKTRACE set
            if std::env::var("RUST_BACKTRACE").is_ok() {
                eprintln!("\nError chain:");
                for cause in e.chain().skip(1) {
                    eprintln!("  - {}", cause);
                }
            }

            2 // Exit code for errors
        }
    })
}

fn run() -> Result<()> {
    // Parse CLI
    let cli = Cli::parse();

    // Existing command handling...
    // All errors return anyhow::Result and propagate up

    Ok(())
}
```

### Integration Points

**From STORY-004:**
- Use `ErrorResponse` struct
- Use `output_error()` function
- Use `OutputFormat::Text` and `OutputFormat::Json` enums

**From STORY-005:**
- Use `TreeLintError` types when available
- Wrap in anyhow context for error chains
- Leverage anyhow's error chaining for context

**Estimated Size:** ~30 lines of code in main.rs

**Dependencies:**
- anyhow (already in tech-stack.md)
- STORY-004 error output functions
- STORY-005 error types (if available)

---

## Non-Functional Requirements

### Performance
- **Exit code handling:** <1ms overhead (trivial wrapper)

### Security
- **Error messages:** No sensitive data in error output (validated by security-auditor)
- **Stack traces:** Only with RUST_BACKTRACE (not in production by default)

### Usability
- **Error format:** Clear, actionable error messages
- **Script integration:** Exit codes follow Unix conventions (0=success, 2=error)

---

## Definition of Done

- [ ] main.rs has error handler wrapper (match run() pattern)
- [ ] Exit code 2 for all errors
- [ ] Exit code 0 for success
- [ ] Errors print to stderr (not stdout)
- [ ] JSON errors use ErrorResponse from STORY-004
- [ ] RUST_BACKTRACE=1 shows full error chain
- [ ] Integration test: `treelint analyze /nonexistent` → exit code 2
- [ ] Integration test: `treelint analyze valid_file.txt` → exit code 0
- [ ] All tests pass (100% pass rate)
- [ ] Code follows coding-standards.md
- [ ] No anti-pattern violations

---

## Notes

**Created by:** RCA-006 Analysis (deferral validation quality gate failure)

**Purpose:** Close gap created by circular deferrals in STORY-004 and STORY-005

**Scope Clarity:**
- STORY-004: Error output structures (ErrorResponse, format_json, output_error)
- STORY-005: Error type definitions (TreeLintError enums and implementations)
- **STORY-006:** Error integration in main.rs (exit codes and stderr routing)

This story explicitly owns what was previously ambiguous, preventing future circular deferrals.

---

## Related Stories

- **STORY-004:** JSON Output Format - Created ErrorResponse and output functions
- **STORY-005:** Error Handling Framework - Created TreeLintError types
- **Prerequisite:** Both STORY-004 and STORY-005 must complete before this story

---

## Workflow History

- **2025-11-03:** Story created by RCA-006 analysis
- **Status:** Backlog (ready for sprint planning)
