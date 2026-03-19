# Phase 01: Capture

**Purpose:** Collect all failure artifacts and context before analysis begins. Read-only operations only.
**Applies to:** Both tactical and strategic modes (with different capture targets).

---

## Step 01.1: Collect Error/Issue Artifacts [MANDATORY]

### EXECUTE

**Tactical Mode — Collect Error Output:**

Capture the exact failure output from the dev workflow:
```
artifacts = {
    error_message: <exact error text — full, not summarized>,
    stack_trace: <full stack trace if available>,
    test_output: <complete test runner output>,
    exit_code: <numeric exit code>,
    failing_file: <path to file that failed>,
    failing_function: <function/test name>
}
```

If error output is in conversation context, extract it directly.
If not available, attempt to read recent test output.

**Strategic Mode — Clarify Issue:**

Issue description was extracted in Phase 00. Now ensure it includes:
- What happened (observed behavior)
- When it happened (story ID, phase, command invocation)
- Where it happened (which component)
- Expected vs actual behavior
- Impact (what was blocked or degraded)

If any element is missing:
```
AskUserQuestion:
    Question: "To complete the analysis, I need more detail. Please provide:"
    Header: "RCA Details"
    Options:
        - "What was the expected behavior?"
        - "What actually happened?"
        - "Which component was affected (skill/command/subagent)?"
        - "When did this occur (story ID, phase, command invocation)?"
    multiSelect: true
```

### VERIFY

- Tactical: error_message is non-empty and contains actual error text
- Strategic: issue description covers what/when/where/expected/actual

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.1
```

---

## Step 01.2: Collect Phase/Workflow State [MANDATORY]

### EXECUTE

**Tactical Mode — Read Workflow State:**

```
Read(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json")
```

Document:
- Current phase (Red/Green/Refactor/Integration/QA)
- Previous phase result
- Number of prior fix attempts for this issue
- Story ID and acceptance criteria being tested

If file does not exist, extract from conversation context.

**Strategic Mode — Determine Component Type:**

Based on AFFECTED_COMPONENT from Phase 00:

```
IF component_type == "Skill":
    primary_file = ".claude/skills/{skill_name}/SKILL.md"
IF component_type == "Command":
    primary_file = ".claude/commands/{command_name}.md"
IF component_type == "Subagent":
    primary_file = ".claude/agents/{subagent_name}.md"
IF component_type == "Context File":
    primary_file = "devforgeai/specs/context/{file_name}.md"
IF component_type == "Workflow":
    primary_file = "devforgeai/specs/Stories/{STORY_ID}.story.md"
```

### VERIFY

- Tactical: Phase state captured (current phase identified)
- Strategic: Component type determined with primary file path

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.2
```

---

## Step 01.3: Collect Recent Changes [MANDATORY]

### EXECUTE

**Tactical Mode — Git History:**

```bash
git diff HEAD~3 --stat
```

```bash
git log --oneline -5
```

Identify what changed since last passing state. Record modified files.

**Strategic Mode — Read Primary Files:**

```
Read(file_path="{primary_file}")
```

Then read secondary files based on component type:

**For Skill:**
```
# Check if skill invokes subagents
Grep(pattern="Task\\(.*subagent_type", path=".claude/skills/{skill_name}/", output_mode="content")

# Check command that invokes this skill
Grep(pattern="Skill\\(command=\"{skill_name}", path=".claude/commands/", output_mode="files_with_matches")
```

**For Command:**
```
# Read skill invoked by command
Extract skill name from Skill(command="...") line
Read(file_path=".claude/skills/{skill_name}/SKILL.md")
```

**For Subagent:**
```
# Find skills that invoke this subagent
Grep(pattern="subagent_type=\"{subagent_name}", path=".claude/skills/", output_mode="files_with_matches")
```

### VERIFY

- Tactical: Recent changes identified (file list captured)
- Strategic: Primary file read successfully, secondary files identified

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.3
```

---

## Step 01.4: Read Context Files (If Relevant) [CONDITIONAL]

### EXECUTE

**Condition:** Execute this step IF the issue involves constraint violations, spec drift, or context file references.

**Both Modes:**

```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

**Strategic Mode — Also load framework integration guide:**

```
Read(file_path=".claude/skills/spec-driven-rca/references/framework-integration-points.md")
```

Use the "Evidence Location by Breakdown Type" section to determine if additional files need reading.

### VERIFY

- Context files read successfully (all 6 if constraint-related)
- Strategic: framework-integration-points.md loaded

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.4
```

---

## Step 01.5: Search for Related RCAs (Strategic Only) [CONDITIONAL]

### EXECUTE

**Condition:** Strategic mode only.

```
Grep(pattern="{keywords from issue}", path="devforgeai/RCA/", output_mode="files_with_matches")
```

For each related RCA found, read and note:
- RCA number and title
- Root cause summary
- Whether same component was affected

Store as `related_rcas[]` for "Related RCAs" section in final document.

### VERIFY

- Search executed (may return 0 results — that is valid)
- Results stored in related_rcas array

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.5
```

---

## Step 01.6: Store File Metadata [MANDATORY]

### EXECUTE

For each file read during this phase, store metadata:

```
files_examined.append({
    path: <absolute path>,
    lines_read: <range or "all">,
    relevant_sections: [<section_name, line_range>],
    excerpts: [<lines, text, significance>]
})
```

### VERIFY

- files_examined array populated with at least 1 entry
- Each entry has path, lines_read, and at least one relevant section

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.6
```

---

## Step 01.7: Capture Summary [MANDATORY]

### EXECUTE

**Tactical Mode:**
```
CAPTURE SUMMARY
===============
Story: {STORY_ID}
Phase: {current_phase}
Failure: {one-line description}
Error: {error_message first line}
Files Changed: {list of recently modified files}
Fix Attempts: {count of prior attempts}
Files Examined: {count}
```

**Strategic Mode:**
```
CAPTURE SUMMARY
===============
Issue: {ISSUE_DESCRIPTION brief}
Severity: {SEVERITY}
Component: {AFFECTED_COMPONENT} ({component_type})
Files Read: {count}
  - Primary: {primary_file}
  - Secondary: {count of secondary files}
  - Context: {count of context files if applicable}
  - Related RCAs: {count}
Evidence Excerpts: {count of relevant excerpts}
```

Display summary to user.

### VERIFY

- Summary displayed with all fields populated

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=01 --step=01.7
```
