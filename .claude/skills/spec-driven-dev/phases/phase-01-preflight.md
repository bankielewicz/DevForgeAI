# Phase 01: Pre-Flight Validation

## Entry Gate

```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```

## Contract

PURPOSE: Validate environment, context files, story specification, and session state before development begins.
REQUIRED SUBAGENTS: git-validator, tech-stack-detector, context-preservation-validator
REQUIRED ARTIFACTS: `.claude/memory/sessions/${STORY_ID}-session.md`
STEP COUNT: 8 mandatory steps

---

## Mandatory Steps

### Step 1: Validate Git Status

EXECUTE: Invoke git-validator subagent.
```
Task(subagent_type="git-validator", prompt="Validate Git repository status for ${STORY_ID}. Check: repo initialized, clean working tree or manageable changes, branch strategy. Report status.")
```
VERIFY: Task result returned with git status assessment. IF >10 uncommitted changes, use AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=git-validator`

### Step 2: Validate 6 Context Files

EXECUTE: Glob for all 6 constitutional context files.
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Expected files: tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

VERIFY: Glob returns exactly 6 files. Read each to confirm valid content (not empty).
```
IF count != 6: HALT — "Missing context files. Run /create-context first."
```

### Step 3: Load Story Specification

EXECUTE: Read the story file.
```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}-*.story.md")
# Use Glob first if exact filename unknown
```
VERIFY: File exists and contains `## Acceptance Criteria` and `## Technical Specification` sections.
```
Grep(pattern="## Acceptance Criteria", path="${STORY_FILE}")
Grep(pattern="## Technical Specification", path="${STORY_FILE}")
IF either missing: HALT — "Story file incomplete."
```

### Step 4: Detect Tech Stack

EXECUTE: Invoke tech-stack-detector subagent.
```
Task(subagent_type="tech-stack-detector", prompt="Detect project technology stack and validate against tech-stack.md for ${STORY_ID}. Report detected languages, frameworks, test frameworks, and any conflicts.")
```
VERIFY: Task result returned with detected stack. No conflicts with tech-stack.md.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=tech-stack-detector`

### Step 5: Technical Debt Threshold Check

EXECUTE: Read technical debt register if it exists.
```
Glob(pattern="devforgeai/specs/technical-debt-register.md")
# IF exists: Read and parse thresholds
# Thresholds: warning=5, critical=10, blocking=15
```
VERIFY: Check total_open against thresholds.
```
IF >= 15 AND NOT $IGNORE_DEBT_FLAG: HALT with AskUserQuestion
IF 10-14: Display warning, set $DEBT_OVERRIDE_BANNER if user consents
IF 5-9: Display notice
IF < 5: Silent proceed
```

### Step 6: Create Session Memory

EXECUTE: Write session memory file.
```
Write(file_path=".claude/memory/sessions/${STORY_ID}-session.md", content=<session template with story_id, status:active, timestamp>)
```
VERIFY: Confirm file exists.
```
Glob(pattern=".claude/memory/sessions/${STORY_ID}-session.md")
IF not found: HALT — "Session memory creation failed."
```

### Step 7: Stale Session Cleanup

EXECUTE: Glob for active sessions older than 7 days.
```
Glob(pattern=".claude/memory/sessions/*-session.md")
# For each: Read, check last_updated, archive if >7 days old
```
VERIFY: Any archived sessions logged. Current session remains active.

### Step 8: Context Preservation Validation

EXECUTE: Invoke context-preservation-validator subagent.
```
Task(subagent_type="context-preservation-validator", prompt="Validate context linkage for ${STORY_ID}. Check brainstorm-to-epic-to-story provenance chain. Report any context loss.")
```
VERIFY: Task result returned. No critical context loss detected.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=context-preservation-validator`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=01 --checkpoint-passed
# Exit 0: proceed to Phase 02 | Exit 1: HALT
```

## Optional Captures (Non-Blocking)

- Capture observations: friction, success, pattern, gap, idea, bug
- Update session memory with Phase 01 completion timestamp
- Reference: `references/observation-capture.md`
