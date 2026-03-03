# Test Folder Write Protection Rule

**Purpose:** Restrict write access to test files to only authorized subagents during their designated workflow phases.
**Scope:** All files under `tests/` directory and co-located test files.
**Enforcement:** Prompt-level HALT trigger with AskUserQuestion escalation.

---

## Protected Path Patterns

The following file patterns are under restricted-write protection:

```
tests/**
*.test.*
*.spec.*
test_*.py
*_test.py
```

Any Write(), Edit(), or file creation operation targeting these patterns triggers the HALT protocol below.

---

## HALT Trigger

**HALT immediately when ALL of the following are true:**

1. The active agent is **not authorized** for the current workflow phase (see Authorized Agents below)
2. The operation targets a file matching any protected path pattern listed above
3. The operation is a Write(), Edit(), or file creation command

**When HALT fires:**
- Stop all file operations immediately
- Do NOT proceed with the write
- Invoke AskUserQuestion to request explicit user approval
- Wait for user response before taking any action

**Non-authorized agents include:** orchestrator (opus), backend-architect, frontend-developer, refactoring-specialist, code-reviewer, documentation-writer, and any other agent not listed in the Authorized Agents section below.

Any unauthorized agent attempting to modify test files MUST be stopped. This prevents silent test tampering that could mask implementation defects.

---

## Authorized Agents

The following agents are permitted to write to test files during their designated phases ONLY:

| Agent | Phase | Authorization |
|-------|-------|---------------|
| **test-automator** | Phase 02 (Red) | Authorized and permitted to write test files during TDD Red phase |
| **integration-tester** | Phase 05 (Integration) | Authorized and permitted to write integration test files during Integration phase |

**Phase-specific restrictions:**
- test-automator is ONLY authorized during Phase 02. Writing tests during Phase 03, 04, or any other phase requires user approval.
- integration-tester is ONLY authorized during Phase 05. Writing tests during any other phase requires user approval.
- No agent has blanket authorization across all phases.

---

## AskUserQuestion Protocol

When a non-authorized agent attempts to modify test files, invoke AskUserQuestion with the following format:

```
AskUserQuestion:
  Question: "{agent_name} is attempting to modify test file: {file_path}. This requires explicit approval."
  Header: "Test Protection"
  Options:
    - label: "Approve this modification"
      description: "Grant one-time permission for this specific file change"
    - label: "Deny and HALT"
      description: "Block the modification and stop the current operation"
  multiSelect: false
```

**Approval is required before proceeding.** The agent must wait for user consent and must not continue with the file operation until approval is granted.

**Scope of approval:** Each approval covers a single file operation. Subsequent modifications to test files by the same non-authorized agent require separate approval.

---

## Phase-Specific Behavior

| Phase | Behavior |
|-------|----------|
| Phase 01 (Pre-Flight) | No test writes expected. HALT if attempted. |
| Phase 02 (Red) | test-automator writes freely. All other agents HALT. |
| Phase 03 (Green) | All test writes HALT + AskUserQuestion. |
| Phase 04 (Refactor) | All test writes HALT + AskUserQuestion. Prevents test tampering masquerading as refactoring. |
| Phase 05 (Integration) | integration-tester writes freely. All other agents HALT. |
| Phase 06-10 | No test writes expected. HALT if attempted. |

---

## Rationale

Test integrity is a critical quality gate in the DevForgeAI TDD workflow. If tests are modified outside designated phases by unauthorized agents, defects can be masked:

- **Phase 03 risk:** Implementation agents could weaken test assertions to make failing tests pass
- **Phase 04 risk:** Refactoring agents could delete or simplify tests that catch regressions
- **Silent tampering:** Without this rule, test modifications go undetected until QA validation

This rule works in conjunction with:
- **STORY-502:** Red-phase test integrity checksums (detection-based backup)
- **STORY-503:** Test tampering heuristic patterns (pattern-based detection)

---

## References

- **EPIC-085:** QA Diff Regression Detection and Test Integrity System
- **ADR-025:** QA Diff Regression Detection
- **STORY-502:** Red-Phase Test Integrity Checksums
- **STORY-503:** Test Tampering Heuristic Patterns
