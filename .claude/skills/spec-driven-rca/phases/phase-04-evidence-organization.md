# Phase 04: Evidence Organization (Strategic Mode Only)

**Purpose:** Organize evidence from Phases 01-02 into structured sections for the RCA document.
**Applies to:** Strategic mode only.

---

## Step 04.1: Load Evidence Collection Guide [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/references/evidence-collection-guide.md")
```

Use the "Evidence Organization" section for structuring.

### VERIFY

- Reference file content is in context
- Contains "Evidence Organization" section

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.1
```

---

## Step 04.2: Load Evidence Template [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/assets/evidence-section-template.md")
```

### VERIFY

- Template structure visible in context

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.2
```

---

## Step 04.3: Organize Files Examined [MANDATORY]

### EXECUTE

From Phase 01 `files_examined[]`:

```
FOR each file in files_examined:
    Determine significance: CRITICAL | HIGH | MEDIUM | LOW

    Significance criteria:
        CRITICAL: Directly contains root cause or violated constraint
        HIGH: Contains strong supporting evidence for a Why
        MEDIUM: Provides contextual information
        LOW: Read but not directly relevant

    IF significance >= MEDIUM:
        Extract relevant excerpts (10-30 lines with context)
        Format per template:
            - Path
            - Lines examined
            - Finding
            - Excerpt (with line numbers)
            - Significance explanation
            - Supports Why # (which of the 5 Whys this evidence supports)

Sort files by significance (CRITICAL first)
```

### VERIFY

- Files sorted by significance
- At least 3 files have significance MEDIUM or higher
- Each file entry has all required fields

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.3
```

---

## Step 04.4: Validate Context Files [MANDATORY]

### EXECUTE

```
Glob(pattern="devforgeai/specs/context/*.md")

EXPECTED = [
    "tech-stack.md",
    "source-tree.md",
    "dependencies.md",
    "coding-standards.md",
    "architecture-constraints.md",
    "anti-patterns.md"
]

FOR each expected_file:
    IF exists:
        status = "EXISTS"
        IF issue involves this constraint:
            Read file (if not already in context)
            Check if constraint violated
            status = "PASS" or "FAIL: {violation}"
    ELSE:
        status = "MISSING"

Create context_files_status table
```

### VERIFY

- All 6 context files accounted for (EXISTS, PASS, FAIL, or MISSING)
- Any FAIL status has specific violation description

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.4
```

---

## Step 04.5: Analyze Workflow State [CONDITIONAL]

### EXECUTE

**Condition:** Execute if issue involves workflow/story state transitions.

```
IF issue involves workflow:
    From story file YAML frontmatter:
        actual_state = status field

    From workflow documentation:
        expected_state = what state should be based on criteria

    From story Workflow History:
        recent_transitions = last 3-5 transitions

    Analyze:
        discrepancy = expected vs actual
        missing_transition = expected transition not recorded
        invalid_transition = transition violated lifecycle rules
```

### VERIFY

- Workflow state analysis completed (if applicable)
- Discrepancy between expected and actual documented

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.5
```

---

## Step 04.6: Check Evidence Sufficiency [MANDATORY]

### EXECUTE

Use sufficiency criteria from evidence-collection-guide.md:

```
Sufficiency Checklist:
- [ ] All 5 Whys have supporting evidence
- [ ] Root cause clearly demonstrated
- [ ] All files mentioned in 5 Whys examined
- [ ] At least 3 pieces of CRITICAL or HIGH evidence
- [ ] Can answer: "Where exactly do we fix this?"

IF insufficient:
    Collect additional evidence (re-read files with focus on gaps)
    Re-check sufficiency
```

### VERIFY

- All 5 items on sufficiency checklist are checked
- Evidence is sufficient to support recommendations

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.6
```

---

## Step 04.7: Phase 04 Summary [MANDATORY]

### EXECUTE

```
PHASE 04 COMPLETE (EVIDENCE)
=============================
Files Examined: {count}
  - CRITICAL: {count}
  - HIGH: {count}
  - MEDIUM: {count}
  - LOW: {count}
Excerpts Captured: {count}
Context Files: {PASS/FAIL counts}
Workflow State: {analyzed | N/A}
Evidence Sufficiency: PASS

Proceeding to Phase 05: Recommendation Generation...
```

### VERIFY

- Summary displayed with all fields

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=04 --step=04.7
```
