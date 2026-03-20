# Phase 01: Context Gathering

Interactive collection of issue details, affected files, prior attempts, and constraints.

---

## Reference Loading [MANDATORY]

```
EXECUTE: Read(file_path="src/claude/skills/spec-driven-collaboration/references/context-gathering-guide.md")
VERIFY: File content loaded successfully (non-empty)
IF Read fails: HALT — "Phase 01 reference file not loaded"
Do NOT rely on memory of previous reads. Load reference fresh.
```

---

## Step 01.1: Extract Context Markers

```
EXECUTE: Search conversation for context markers set by /collaborate command:
  - "**Issue Description:**" → ISSUE_DESCRIPTION
  - "**Target AI:**" → TARGET_AI (default: "Gemini")

VERIFY: Both values extracted
  - ISSUE_DESCRIPTION is non-empty string
  - TARGET_AI is non-empty string (default "Gemini" if not found)

RECORD: "Step 01.1 complete — ISSUE_DESCRIPTION and TARGET_AI extracted"
```

IF ISSUE_DESCRIPTION not found in context markers:
```
AskUserQuestion:
    Question: "What issue should we collaborate on with an external AI?"
    Header: "Issue"
    Options:
        - "Test failures I can't resolve"
        - "Architecture decision needing fresh perspective"
        - "Implementation approach — want a second opinion"
        - "Bug that persists after multiple fix attempts"
    multiSelect: false
ISSUE_DESCRIPTION = user response
```

---

## Step 01.2: Gather Affected Files

Identify files related to the issue using multiple strategies.

```
EXECUTE:
  Strategy 1: Search for recently modified files related to issue keywords
    - Grep(pattern=<issue keywords>, output_mode="files_with_matches", head_limit=20)
    - Glob for files matching issue-related patterns

  Strategy 2: Ask user to confirm or specify files
    AskUserQuestion:
        Question: "Which files are involved in this issue? I found some candidates from keyword search."
        Header: "Files"
        Options:
            - "Use the files you found (Recommended)"
            - "Let me specify the files manually"
            - "Add to what you found"
        multiSelect: false

  IF user selects "specify manually" or "add":
    Accept file paths from user input
    Validate each path: Read(file_path=<path>) — confirm file exists

VERIFY:
  - AFFECTED_FILES[] contains at least 1 valid file path
  - Each file in AFFECTED_FILES confirmed to exist via Read()

RECORD: "Step 01.2 complete — {count} affected files identified"
```

Store: `AFFECTED_FILES[]` — list of validated file paths

---

## Step 01.3: Gather What Has Been Tried

```
EXECUTE:
  AskUserQuestion:
      Question: "What approaches have you already tried to resolve this issue?"
      Header: "Attempts"
      Options:
          - "Nothing yet — need fresh perspective"
          - "1-2 approaches that didn't work"
          - "3+ approaches — persistent issue"
      multiSelect: false

  IF user selected "1-2 approaches" or "3+ approaches":
    For each attempt, ask user to describe:
      - What was done (approach taken)
      - Result observed
      - Why it failed (root cause if known)

VERIFY:
  - ATTEMPTS[] captured (even if empty/"nothing yet")
  - If user reported attempts: each has {approach, result, failure_reason}

RECORD: "Step 01.3 complete — {count} attempts documented"
```

Store: `ATTEMPTS[]` — list of {approach, result, failure_reason}

---

## Step 01.4: Gather Priority and Constraints

```
EXECUTE:
  AskUserQuestion:
      Question: "What priority level for this collaboration request?"
      Header: "Priority"
      Options:
          - "Critical — blocking all progress"
          - "High — significant impact on current work"
          - "Medium — important but not blocking"
          - "Low — enhancement or nice-to-have"
      multiSelect: false

  AskUserQuestion:
      Question: "Any additional constraints beyond the standard constitution docs?"
      Header: "Constraints"
      Options:
          - "None — standard constitution constraints are sufficient"
          - "WSL/Linux-specific requirements"
          - "Must maintain backward compatibility"
      multiSelect: true

VERIFY:
  - PRIORITY is set (one of: Critical, High, Medium, Low)
  - EXTRA_CONSTRAINTS captured (even if "None")

RECORD: "Step 01.4 complete — Priority: {PRIORITY}, Extra constraints: {count}"
```

Store: `PRIORITY`, `EXTRA_CONSTRAINTS`

---

## Phase 01 Gate

```
VERIFY all required context captured:
  - [ ] ISSUE_DESCRIPTION is non-empty
  - [ ] TARGET_AI is set
  - [ ] AFFECTED_FILES has at least 1 file
  - [ ] ATTEMPTS captured (even if "nothing yet")
  - [ ] PRIORITY set
  - [ ] EXTRA_CONSTRAINTS captured

IF any item missing: HALT and re-ask via AskUserQuestion
IF all items present: Phase 01 PASSED — proceed to Phase 02
```
