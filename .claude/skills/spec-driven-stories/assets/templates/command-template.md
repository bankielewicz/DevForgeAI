---
description: [Brief description of what the command does]
argument-hint: [PARAM] [options]
model: opus
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Skill, Bash(git:*)
execution-mode: immediate  # auto-exits plan mode before running
---

# /command-name - Title

**Purpose:** One-line description of the command's purpose.

Execute [action] for [target] following lean orchestration pattern.

Do not skip any phases nor skip the [skill-name] skill.

---

## Quick Reference

**Purpose:** Provide 3-5 usage examples for quick command reference.

- Standard usage: `/command-name PARAM-001`
- With optional flag: `/command-name PARAM-001 --flag`
- Alternative mode: `/command-name PARAM-001 mode`
- Show help/list: `/command-name --help`
- With multiple options: `/command-name PARAM-001 --option1 --option2`

```bash
# Standard usage
/command-name PARAM-001

# With optional flag
/command-name PARAM-001 --flag

# Alternative mode
/command-name PARAM-001 mode
```

---

## Budget Allocation

<!-- AUTHOR GUIDANCE - Reference for command authors, not runtime content -->

Guide authors on character budget distribution across sections.

| Section | Min | Max | Description |
|---------|-----|-----|-------------|
| YAML Frontmatter | 200 | 400 | Required metadata fields |
| Title + Description | 100 | 300 | Command name and purpose |
| Quick Reference | 300 | 600 | 3-5 usage examples |
| Phase 0: Validation | 800 | 1500 | Argument parsing, mode detection |
| Phase 1: Skill Invocation | 600 | 1200 | Context markers, skill call |
| Phase 2: Display Results | 400 | 800 | Output formatting |
| Error Handling | 600 | 1200 | 3-5 error categories |
| Success Criteria | 200 | 400 | Completion conditions |
| Integration | 200 | 400 | Related commands, next steps |
| **Total** | **3400** | **6800** | Optimal range: 6K-12K chars |

**Note:** Maximum allocations sum to 6,800 characters, well within 15,000 limit. Target 6K-12K for optimal token efficiency per lean orchestration protocol.

---

## Command Workflow

### Phase 0: Argument Validation

**Purpose:** Parse and validate command arguments before skill invocation.

**Step 0.0: Plan Mode Auto-Exit [execution-mode: immediate]**

```
IF plan mode is active:
    Display: "Note: /command-name is an execution command. Exiting plan mode."
    ExitPlanMode()
```

**Step 0.1: Parse Arguments**

```
PARAM_ID = null
MODE = default

FOR arg in arguments:
    IF arg matches "PARAM-[0-9]+":
        PARAM_ID = arg
    ELIF arg == "--flag":
        MODE = flag_mode

IF PARAM_ID empty:
    Display: "Usage: /command-name PARAM-NNN [--flag]"
    HALT
```

**Step 0.2: Load Resource File**

```
# @file references load file content into conversation context
@path/to/resource/${PARAM_ID}*.md

IF file not found:
    Display: "Resource not found: ${PARAM_ID}"
    HALT

Display: "✓ Resource: ${PARAM_ID}"
```

---

### Phase 1: Invoke Skill

**Purpose:** Delegate to specialized skill with proper context markers.

**Set context markers for skill:**

Context markers use format: **Param**: $VALUE

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Command Workflow Title"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""

**Param ID**: ${PARAM_ID}
**Mode**: ${MODE}

Display: ""
```

**⚠️ MANDATORY: Invoke skill - DO NOT proceed with manual analysis**

```
Skill(command="devforgeai-[skillname]")
```

**Commands ONLY orchestrate. Skills implement business logic.**

Skill executes all phases and returns structured result to command.

---

### Phase 2: Display Results

**Purpose:** Format and display skill results to user.

```
# result = skill output object

Display: result.display.template
Display: ""
Display: "Next Steps:"
FOR step in result.display.next_steps:
    Display: "  • {step}"
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**No processing, parsing, or template generation in command.**
**All business logic delegated to skill.**

---

### Phase 3: Next Steps (Optional)

**Purpose:** Suggest follow-up commands based on result status.

```
IF result.status == "success":
    Display: "Run: /next-command ${PARAM_ID}"
ELIF result.status == "incomplete":
    Display: "Run: /retry-command ${PARAM_ID}"
```

---

## Error Handling

Define standard error categories with user-facing messages.

**Argument Validation Failure**
- Detection: PARAM_ID empty or invalid format
- Message: "Usage: /command-name PARAM-NNN [options]"
- Recovery: Display usage, list valid parameters

**Context File Not Found**
- Detection: Read() fails for context file
- Message: "Context file missing: {path}"
- Recovery: "Run /create-context first"

**Skill Invocation Failure**
- Detection: Skill returns error status
- Message: "Skill failed: {error_message}"
- Recovery: Review skill output, check prerequisites

**Resource Not Found**
- Detection: Glob returns no matches for resource
- Message: "Resource not found: {PARAM_ID}"
- Recovery: "Run Glob() to list available resources"

Complex error recovery logic belongs in skills, not commands.

---

## Success Criteria

**Purpose:** Define when command execution is complete.

- [ ] Arguments validated and parsed
- [ ] Skill invoked with proper context
- [ ] Results displayed to user
- [ ] Next steps provided
- [ ] No errors or all errors handled

---

## Integration

**Purpose:** Document related commands and workflow position.

**Invoked by:** Manual user command, orchestration workflows
**Invokes:** devforgeai-[skillname] skill
**Followed by:** /next-command (on success)
**Related:** /related-command, /another-command

---

## Validation Notes

**Purpose:** Document template validation against existing commands.

### Command Mapping: /qa

| Template Section | /qa Equivalent | Status |
|------------------|----------------|--------|
| YAML Frontmatter | Lines 1-8 | ✓ Mapped |
| Quick Reference | Lines 19-29 | ✓ Mapped |
| Phase 0 | Lines 35-138 | ✓ Mapped |
| Phase 1 | Lines 142-160 | ✓ Mapped |
| Phase 2 | Lines 164-180 | ✓ Mapped |
| Error Handling | Inline in Phase 0 | ✓ Mapped |

### Command Mapping: /dev

| Template Section | /dev Equivalent | Status |
|------------------|-----------------|--------|
| YAML Frontmatter | Lines 1-7 | ✓ Mapped |
| Quick Reference | Lines 19-41 | ✓ Mapped |
| Phase 0 | Lines 47-133 | ✓ Mapped |
| Phase 1 | Lines 137-150 | ✓ Mapped |
| Phase 2 | Lines 154-170 | ✓ Mapped |
| Error Handling | Lines 173-185 | ✓ Mapped |

**Validation Result:** Template structure compatible with both /qa and /dev commands.

---

## Performance Notes (Optional)

**Purpose:** Document token efficiency and budget compliance.

- Target size: 6,000-12,000 characters (lean orchestration optimal range)
- Maximum: 15,000 characters / 500 lines
- This template: ~5,500 characters / ~250 lines
- Budget compliance: ✓ Within limits

---

**Template Version:** 1.0
**Last Updated:** 2026-02-12
**Reference:** lean-orchestration-pattern.md
