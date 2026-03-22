---
id: EPIC-087
title: QA Integrity Enforcement
status: Active
complexity: Low
created: 2026-03-03
source: RCA-046
---

# EPIC-087: QA Integrity Enforcement

## Overview

Strengthen QA test integrity enforcement to prevent orchestrator rationalization of CRITICAL safety findings. Addresses the self-enforcement paradox identified in RCA-046 where the same agent that modifies test files is responsible for detecting and blocking on those modifications.

## Source

- **RCA-046:** QA Test Integrity Bypass Via Rationalization
- **Root Cause:** Self-enforcement paradox — orchestrator can rationalize away its own violations when safety mechanisms are expressed as documentation text without programmatic enforcement.

## Features

### Feature 1: Anti-Rationalization Protections (REC-3 + REC-4)
Add explicit anti-rationalization warnings to QA Phase 1.5 reference documentation and CLAUDE.md halt triggers to prevent the orchestrator from explaining away checksum mismatches.
- **Stories:** STORY-559

### Feature 2: CLI Test Integrity Verification (REC-5)
Create a `devforgeai-validate verify-test-integrity` CLI command that independently computes and compares checksums, producing a deterministic exit code that cannot be rationalized away.
- **Stories:** STORY-560

### Feature 3: Test-Folder-Protection Phase Return Option (RCA-047 REC-1)
Add "Return to Phase 02 (Recommended)" option to test-folder-protection AskUserQuestion protocol, steering orchestrator toward test-automator regeneration instead of direct test modification.
- **Stories:** STORY-566

### Feature 4: Phase Regression Backward Transition (RCA-047 REC-2)
Add backward phase transition support to implementing-stories workflow, allowing Phase 03/04 to return to Phase 02 for test regeneration.
- **Stories:** STORY-567

### Feature 5: Phase Regression Deviation Type (RCA-047 REC-3)
Add "Phase Regression" to the workflow-deviation-protocol deviation type taxonomy.
- **Stories:** STORY-568

### Feature 6: Phase-Reset CLI Command (RCA-047 REC-4)
Add `devforgeai-validate phase-reset` CLI command for programmatic backward phase transitions with audit logging.
- **Stories:** STORY-569

### Feature 7: Test-Automator Arithmetic Safety (RCA-047 REC-5)
Document bash arithmetic safety rule in test-automator to prevent `((VAR++))` under `set -e`.
- **Stories:** STORY-570

## Success Criteria

- [ ] QA Phase 1.5 blocks unconditionally on checksum mismatches without rationalization
- [ ] CLI command provides external enforcement independent of orchestrator reasoning
- [ ] CLAUDE.md halt trigger prevents integrity finding rationalization across all workflows

## Story Summary

| Story ID | Title | Points | Priority | Status |
|----------|-------|--------|----------|--------|
| STORY-559 | Anti-Rationalization Protections for Test Integrity | 2 | High | Backlog |
| STORY-560 | CLI Test Integrity Verification Command | 5 | Medium | Backlog |
| STORY-566 | Add Return to Phase 02 Option to Test-Folder-Protection Rule | 1 | Critical | Backlog |
| STORY-567 | Add Phase Regression Backward Transition to Implementing-Stories Workflow | 3 | Critical | Backlog |
| STORY-568 | Add Phase Regression Deviation Type to Workflow-Deviation-Protocol | 1 | High | Backlog |
| STORY-569 | Add phase-reset CLI Command to devforgeai-validate | 3 | High | Backlog |
| STORY-570 | Add Shell Test Arithmetic Safety Rule to Test-Automator | 1 | Medium | Backlog |
