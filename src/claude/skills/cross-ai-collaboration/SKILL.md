---
name: cross-ai-collaboration
description: |
  Generate self-contained collaboration documents for sharing issues with
  external AI systems (Gemini, ChatGPT, etc.). Use when the user wants to
  collaborate with another AI, share an issue for joint problem-solving,
  or get a fresh perspective from a peer LLM. Interactively gathers context,
  reads actual code files, and produces a complete package.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
metadata:
  author: DevForgeAI
  version: "1.0.0"
  category: collaboration
  last-updated: "2026-02-24"
---

# Cross-AI Collaboration Skill

Generate a self-contained collaboration document that packages an issue with actual code, context, analysis, and targeted questions for an external AI to review.

## Execution Model

This skill is an **INLINE PROMPT EXPANSION**. After `Skill(command="cross-ai-collaboration")`:
1. This SKILL.md content expands inline
2. YOU execute all 6 phases sequentially
3. YOU produce the output document

**Do NOT wait passively.** Execute all phases now.

---

## Phase Overview

| Phase | Name | Purpose |
|-------|------|---------|
| 01 | Context Gathering | Interactive collection of issue details via AskUserQuestion |
| 02 | Constitution Loading | Read 6 context files, extract relevant constraints |
| 03 | Code Collection | Read affected files, capture actual source code |
| 04 | Analysis & Population | Reason through the issue, populate template sections |
| 05 | Document Generation | Write the collaboration document to `tmp/` |
| 06 | Completion Report | Display summary and next steps to user |

---

## Phase 01: Context Gathering

Extract context markers set by the `/collaborate` command:

```
ISSUE_DESCRIPTION = extract from "**Issue Description:**" marker
TARGET_AI = extract from "**Target AI:**" marker (default: "Gemini")
```

### Step 01.1: Gather Affected Files

Identify files related to the issue. Use multiple strategies:

```
# Strategy 1: Check git status for recently modified files
recent_files = Grep(pattern relevant to issue keywords)

# Strategy 2: Ask user to confirm or add files
AskUserQuestion:
    Question: "Which files are involved in this issue? (I found some candidates from git status and keyword search)"
    Header: "Files"
    Options:
        - "Use the files you found (Recommended)"
        - "Let me specify the files manually"
        - "Add to what you found"
    multiSelect: false
```

IF user selects "specify manually" or "add":
- Accept file paths from user input
- Validate each path exists with `Read(file_path=...)`

Store: `AFFECTED_FILES[]` — list of absolute file paths

### Step 01.2: Gather What Has Been Tried

```
AskUserQuestion:
    Question: "What approaches have you already tried to resolve this issue?"
    Header: "Attempts"
    Options:
        - "Nothing yet — need fresh perspective"
        - "1-2 approaches that didn't work"
        - "3+ approaches — persistent issue"
    multiSelect: false
```

IF user selected "1-2 approaches" or "3+ approaches":
- Ask user to describe each attempt (accept free-text via "Other" option)
- For each attempt, record: what was done, result, and why it failed

Store: `ATTEMPTS[]` — list of {approach, result, failure_reason}

### Step 01.3: Gather Priority and Constraints

```
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
```

Store: `PRIORITY`, `EXTRA_CONSTRAINTS`

### Phase 01 Gate

```
VERIFY all required context captured:
  - [ ] ISSUE_DESCRIPTION is non-empty
  - [ ] TARGET_AI is set
  - [ ] AFFECTED_FILES has at least 1 file
  - [ ] ATTEMPTS captured (even if "nothing yet")
  - [ ] PRIORITY set

IF any missing: HALT and re-ask via AskUserQuestion
```

---

## Phase 02: Constitution Loading

Read all 6 constitutional context files. Extract constraints relevant to the issue.

### Step 02.1: Load All Constitution Files

```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

Load all 6 in parallel where possible.

### Step 02.2: Extract Relevant Constraints

For each file, identify constraints that:
- Directly relate to the ISSUE_DESCRIPTION
- Apply to any file in AFFECTED_FILES
- Would restrict potential solutions

Store: `RELEVANT_CONSTRAINTS[]` — list of {file, constraint_text, line_numbers}

### Phase 02 Gate

```
VERIFY:
  - [ ] All 6 files loaded successfully
  - [ ] At least 1 relevant constraint identified
  - [ ] Constraints include file path and line numbers

IF any file fails to load: HALT — constitution files are required
```

---

## Phase 03: Code Collection

Read each affected file and capture actual source code for the collaboration document.

### Step 03.1: Read Affected Files

```
FOR each file in AFFECTED_FILES:
    content = Read(file_path=file)

    IF file length > 200 lines:
        # Capture the most relevant section
        # Use Grep to find error-related or issue-related lines
        relevant_lines = Grep(pattern=issue_keywords, path=file)
        # Include 50 lines of context around each match
        Store: file path, relevant sections with line numbers
    ELSE:
        Store: file path, full content with line numbers
```

### Step 03.2: Collect Related Test Files

```
FOR each file in AFFECTED_FILES:
    # Find associated test files
    test_candidates = Glob(pattern matching test conventions for this file)

    IF test files found:
        Read each test file
        Store: test file path, content, line numbers
```

### Step 03.3: Collect Error Output

IF error messages or stack traces were mentioned in ISSUE_DESCRIPTION:
- Capture the exact error text
- Include full stack traces, not summaries

Store: `CODE_ARTIFACTS[]` — list of {file_path, content, line_range, type: "source"|"test"|"config"}

### Phase 03 Gate

```
VERIFY:
  - [ ] All AFFECTED_FILES read successfully
  - [ ] At least 1 code artifact captured
  - [ ] All artifacts include file paths and line numbers
  - [ ] Code is ACTUAL source, not summaries

IF any file fails to read: Warn user, continue with available files
```

---

## Phase 04: Analysis & Template Population

Load the output template and populate all 10 sections.

### Step 04.1: Load Template

```
Read(file_path=".claude/skills/cross-ai-collaboration/references/collaboration-prompt-template.md")
    <!-- FULL READ MANDATORY — do not use offset/limit -->
```

### Step 04.2: Reason Through the Issue

Before populating sections, reason through these questions:

1. **Root cause:** What is the most likely root cause? Rank hypotheses with confidence levels.
2. **Attempt analysis:** For each attempt in ATTEMPTS[], why specifically did it fail?
3. **Constitutional relevance:** Which constraints from RELEVANT_CONSTRAINTS[] most tightly bound the solution space?
4. **External context gap:** What does the target AI need to know that they could NOT infer from our code alone? (framework conventions, dual-path rules, WSL quirks, etc.)
5. **Targeted questions:** What specific questions would leverage the target AI's fresh perspective most effectively?
6. **Proposed plan:** What phased approach would we attempt next, with checkpoints?

### Step 04.3: Populate All 10 Sections

Using the template structure, populate:

| Section | Source Data |
|---------|------------|
| 1. Executive Summary | ISSUE_DESCRIPTION + PRIORITY + impact analysis |
| 2. Project Context | Framework description + relevant constitution constraints |
| 3. The Specific Problem | Current/Expected behavior from issue + error output |
| 4. Code Artifacts | CODE_ARTIFACTS[] — actual code with paths and line numbers |
| 5. What We've Tried | ATTEMPTS[] — each approach, result, and failure analysis |
| 6. Our Analysis | Hypotheses + RELEVANT_CONSTRAINTS[] + solution ideas |
| 7. Questions for Target AI | 4-6 targeted, answerable questions |
| 8. Proposed Plan | Phased plan with checkpoints and success criteria |
| 9. Files Reference | Table of all files referenced in the document |
| 10. Compliance Checklist | 10 constitutional compliance checkboxes |

### Phase 04 Gate

```
VERIFY:
  - [ ] All 10 sections populated
  - [ ] No empty sections or placeholder text
  - [ ] Code artifacts contain actual code (not summaries)
  - [ ] Constitutional constraints quoted verbatim with line numbers
  - [ ] Questions are specific and answerable (not vague)
  - [ ] Plan has checkpoints per phase
```

---

## Phase 05: Document Generation

### Step 05.1: Generate Filename

```
# Format: collaborate-{target_ai}-{issue_slug}-{date}.md
# Example: collaborate-gemini-phase-state-tracking-2026-02-24.md

FILENAME = "collaborate-" + lowercase(TARGET_AI) + "-" + slugify(ISSUE_TITLE, max=40) + "-" + TODAY_DATE + ".md"
OUTPUT_PATH = "tmp/" + FILENAME
```

### Step 05.2: Write Document

```
Write(file_path=OUTPUT_PATH, content=populated_document)
```

The document MUST include:
- Header with From/To/Date/Topic/Priority metadata
- All 10 sections from Phase 04
- Actual code in fenced blocks with language annotations
- Constitutional constraints quoted verbatim
- Compliance checklist at the end

### Step 05.3: Verify Write

```
Read(file_path=OUTPUT_PATH)

VERIFY:
  - [ ] File exists and is readable
  - [ ] Contains all 10 section headers
  - [ ] Contains at least 1 fenced code block
  - [ ] File is non-trivially long (>100 lines expected)
```

### Phase 05 Gate

```
IF file verification fails: HALT — document generation incomplete
IF file is <50 lines: HALT — document suspiciously short, likely missing sections
```

---

## Phase 06: Completion Report

Display summary to the user:

```
## Collaboration Document Generated

**Output file:** `{OUTPUT_PATH}`
**Target AI:** {TARGET_AI}
**Priority:** {PRIORITY}

### Document Summary
- **Sections:** 10/10 complete
- **Code files included:** {count of CODE_ARTIFACTS}
- **Questions for {TARGET_AI}:** {count of questions}
- **Constitutional constraints cited:** {count of RELEVANT_CONSTRAINTS}
- **Attempts documented:** {count of ATTEMPTS}

### Next Steps
1. Open `{OUTPUT_PATH}` and review the document
2. Copy the full contents
3. Paste into {TARGET_AI} for collaborative review
4. Share {TARGET_AI}'s response back here for integration

> There is power in collaboration rather than working in isolation.
```

---

## Error Handling

| Error | Phase | Resolution |
|-------|-------|------------|
| No issue description from command | 01 | AskUserQuestion for description |
| Affected file not found | 03 | Warn user, skip file, continue |
| Constitution file missing | 02 | HALT — constitution files are required |
| Template reference missing | 04 | HALT — check skill installation |
| `tmp/` directory missing | 05 | Create it, then write |
| Write fails | 05 | Report error path, suggest manual creation |

---

## References

- Output template: `references/collaboration-prompt-template.md`
- Prompt engineering: `.claude/skills/spec-driven-cc-guide/references/prompt-engineering/`
- Constitution files: `devforgeai/specs/context/` (6 files)
- Prior collaborations: `tmp/gemini-collaboration-*.md` (established patterns)
