# Error Handling Procedures

**Purpose:** Complete error recovery procedures for subagent generation failures.

---

## Error Categories

| Category | Severity | Recovery |
|----------|----------|----------|
| Requirements | MEDIUM | Prompt for manual input or locate file |
| Validation | HIGH | Auto-fix or manual correction |
| File System | HIGH | Check permissions, create directories |
| YAML Syntax | MEDIUM | Regenerate with corrections |
| Framework Constraint | CRITICAL | HALT and report violation |

---

## Error: Requirements Document Not Found

**Condition:** `devforgeai/specs/requirements/phase-2-subagents-requirements.md` missing

**Detection:**
```
Read(file_path="devforgeai/specs/requirements/phase-2-subagents-requirements.md")
IF read fails:
  ERROR: REQUIREMENTS_NOT_FOUND
```

**Response:**
```
Report: "Requirements document not found at expected location"

AskUserQuestion:
  Question: "Requirements document not found. How should I proceed?"
  Header: "Missing Requirements"
  Options:
    - "I'll provide the subagent specification manually"
    - "Search for requirements in alternative locations"
    - "Create a basic requirements template"
    - "Cancel generation"
```

**Recovery Actions:**

| User Choice | Action |
|-------------|--------|
| Provide manually | Prompt for: name, purpose, responsibilities, tools, triggers |
| Search alternatives | Glob for `*requirements*.md` in specs directory |
| Create template | Generate minimal requirements template |
| Cancel | HALT gracefully |

---

## Error: Invalid Subagent Name

**Condition:** User requests subagent not in requirements document

**Detection:**
```
IF requested_subagent NOT IN requirements_subagents:
  ERROR: INVALID_SUBAGENT_NAME
```

**Response:**
```
Report: "Subagent '[name]' not found in requirements"

AskUserQuestion:
  Question: "Subagent '[name]' not in requirements. How should I proceed?"
  Header: "Unknown Subagent"
  Options:
    - "Generate custom subagent based on description I'll provide"
    - "List available subagents from requirements"
    - "Did you mean: [closest match]?"
    - "Cancel generation"
  multiSelect: false
```

**Recovery Actions:**

| User Choice | Action |
|-------------|--------|
| Custom subagent | Collect specification via questions |
| List available | Display all subagents from requirements |
| Closest match | Suggest and confirm closest name match |
| Cancel | HALT gracefully |

---

## Error: File Write Permission Denied

**Condition:** Cannot write to `.claude/agents/` directory

**Detection:**
```
Write(file_path=".claude/agents/[name].md", content=[content])
IF write fails with permission error:
  ERROR: PERMISSION_DENIED
```

**Response:**
```
Report: "Permission denied writing to .claude/agents/"

# Check if directory exists
Glob(pattern=".claude/agents/")
IF directory not found:
  Suggest: "Directory doesn't exist. Create with: mkdir -p .claude/agents"
ELSE:
  Suggest: "Check file permissions on .claude/agents/ directory"

AskUserQuestion:
  Question: "Cannot write file. Please resolve and confirm:"
  Header: "Permission Error"
  Options:
    - "I've created/fixed the directory - retry"
    - "Write to alternative location: src/.claude/agents/"
    - "Cancel generation"
```

**Recovery Actions:**

| User Choice | Action |
|-------------|--------|
| Retry | Attempt Write() again |
| Alternative location | Write to `src/.claude/agents/` instead |
| Cancel | HALT gracefully |

---

## Error: Invalid YAML Syntax

**Condition:** Generated YAML frontmatter has syntax errors

**Detection:**
```
# Validate YAML before writing
Parse YAML frontmatter
IF parse_error:
  ERROR: INVALID_YAML
  Store: error_message, error_line
```

**Response:**
```
Report: "YAML syntax error in generated frontmatter"
Show: Error message and line number

# Attempt auto-fix
Auto-fix common issues:
- Add missing quotes around special characters
- Fix indentation
- Escape problematic characters

Regenerate frontmatter
Retry validation (max 3 attempts)
```

**Recovery Actions:**

| Attempt | Action |
|---------|--------|
| 1st failure | Auto-fix common issues, retry |
| 2nd failure | Simplify description, retry |
| 3rd failure | HALT, show YAML for manual correction |

**Common YAML Fixes:**

| Issue | Auto-Fix |
|-------|----------|
| Unescaped quotes | Replace `"` with `\"` |
| Special characters | Wrap value in quotes |
| Bad indentation | Normalize to 2-space indent |
| Missing delimiter | Add `---` at start/end |

---

## Error: Framework Validation Failure

**Condition:** Generated subagent violates framework constraints

**Detection:**
```
Run validation workflow (see validation-workflow.md)
IF status == FAIL:
  ERROR: FRAMEWORK_VIOLATION
  Store: violations list
```

**Response:**
```
Report: "Framework validation failed"

Display violations:
| Check | Status | Issue | Auto-Fix Available |
|-------|--------|-------|-------------------|
| [check] | ❌ | [issue] | [yes/no] |

AskUserQuestion:
  Question: "Framework validation found issues. How to proceed?"
  Header: "Validation Failed"
  Options:
    - "Apply auto-fixes automatically"
    - "Show detailed issues for manual fix"
    - "Cancel generation"
```

**Recovery Actions:**

| User Choice | Action |
|-------------|--------|
| Auto-fix | Apply all available auto-fixes, re-validate |
| Show details | Display full validation report |
| Cancel | HALT gracefully, preserve partial work |

**Auto-Fixable Issues:**

| Issue | Auto-Fix |
|-------|----------|
| Missing Tool Usage Protocol section | Add standard section |
| Missing Token Efficiency section | Add standard section |
| Missing Framework Integration section | Add section with domain defaults |
| Bash for file operations | Replace with native tool calls |

**Non-Auto-Fixable Issues:**

| Issue | Manual Action Required |
|-------|----------------------|
| Invalid tool selection | User must specify correct tools |
| Wrong model for complexity | User must confirm model choice |
| Missing workflow steps | User must provide workflow details |

---

## Error: Reference File Creation Failure

**Condition:** Cannot create reference file for command-related subagent

**Detection:**
```
IF NEEDS_REFERENCE_FILE AND reference_creation_fails:
  ERROR: REFERENCE_FILE_FAILURE
```

**Response:**
```
Report: "Failed to create reference file"

# Check target location
target = ".claude/skills/[skill]/references/[topic]-guide.md"
Glob(pattern=".claude/skills/[skill]/")

IF skill directory not found:
  Suggest: "Related skill directory doesn't exist"
  Alternative: "Write to devforgeai-subagent-creation references"
ELSE:
  Check: References subdirectory exists

AskUserQuestion:
  Question: "Cannot create reference file. How to proceed?"
  Options:
    - "Create in alternative location"
    - "Skip reference file (subagent may lack guardrails)"
    - "Cancel generation"
```

---

## Error: Existing File Conflict

**Condition:** Subagent file already exists

**Detection:**
```
Read(file_path=".claude/agents/[name].md")
IF read succeeds:
  ERROR: FILE_EXISTS
```

**Response:**
```
Report: "Subagent file already exists: [name].md"

AskUserQuestion:
  Question: "Subagent '[name]' already exists. How to proceed?"
  Header: "File Conflict"
  Options:
    - "Overwrite existing file"
    - "Create backup and overwrite"
    - "Generate with different name"
    - "Cancel generation"
```

**Recovery Actions:**

| User Choice | Action |
|-------------|--------|
| Overwrite | Write new content directly |
| Backup + Overwrite | Copy to `.backup`, then write |
| Different name | Prompt for new name, generate |
| Cancel | HALT gracefully |

---

## Error: Context File Missing

**Condition:** Required context file not found during validation

**Detection:**
```
Read(file_path="devforgeai/specs/context/[file].md")
IF read fails:
  ERROR: CONTEXT_FILE_MISSING
```

**Response:**
```
Report: "Context file missing: [file].md"
Impact: "Cannot validate subagent against framework constraints"

AskUserQuestion:
  Question: "Context file missing. How to proceed?"
  Options:
    - "Skip context validation (not recommended)"
    - "Create context file first"
    - "Cancel generation"
```

---

## Error Recovery Summary

| Error Type | Auto-Recovery | User Action |
|------------|---------------|-------------|
| Requirements not found | Search alternatives | Provide manually |
| Invalid subagent name | Suggest closest | Confirm or specify |
| Permission denied | Suggest mkdir | Fix permissions |
| YAML syntax | Auto-fix (3 tries) | Manual correction |
| Framework violation | Auto-fix available | Review and fix |
| Reference file failure | Alternative location | Skip or fix |
| File conflict | Backup available | Choose action |
| Context file missing | None | Create or skip |

---

## Graceful HALT Protocol

When generation cannot continue:

```
1. Report: Clear error message with context
2. Preserve: Any partial work (temp files, partial content)
3. Suggest: Next steps for resolution
4. Return: Error status with details

{
  "status": "ERROR",
  "error_type": "[error_category]",
  "error_message": "[human-readable message]",
  "partial_work": "[path to any saved partial content]",
  "suggested_actions": [
    "[action 1]",
    "[action 2]"
  ],
  "can_resume": true|false
}
```
