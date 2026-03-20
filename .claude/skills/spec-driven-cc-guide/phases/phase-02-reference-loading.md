# Phase 02: Mandatory Reference Loading

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=cc-guide --from=01 --to=02 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 02 |
| 1 | Previous phase incomplete | HALT - complete Phase 01 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Load ALL reference files identified in Phase 01. This is the critical anti-skip phase — the entire reason this skill was migrated from claude-code-terminal-expert. Every reference file load is an Execute-Verify-Record triplet that cannot be skipped.
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** Loaded reference content in context, $LOADED_REFERENCES_COUNT
- **STEP COUNT:** 4 mandatory steps
- **REFERENCE FILES:** Files from $REFERENCE_FILES[] (determined in Phase 01)

**WHY THIS PHASE EXISTS:** The predecessor skill (claude-code-terminal-expert v4.0) had ~18,000 lines of reference content that Claude routinely skipped loading due to token optimization bias. This resulted in incomplete, inaccurate, or outdated answers drawn from SKILL.md summaries alone. This phase makes reference loading mandatory and verifiable — you cannot proceed to answer synthesis without first loading the authoritative content.

---

## Mandatory Steps (4)

### Step 2.1: Validate Reference File List

**EXECUTE:**
Verify that $REFERENCE_FILES from Phase 01 is non-empty. Cross-check each file exists on disk.

```
FOR each file in $REFERENCE_FILES:
    Glob(pattern=".claude/skills/spec-driven-cc-guide/{file}")
    IF not found: Remove from list, log warning
```

**VERIFY:**
At least one file in $REFERENCE_FILES exists on disk. If ALL files are missing, HALT — "No reference files found. Cannot answer without authoritative content."

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=02 --step=2.1 --project-root=.
```

---

### Step 2.2: Load Primary Reference File(s)

**EXECUTE:**
For EACH file in $REFERENCE_FILES, load the complete content:

```
FOR each file in $REFERENCE_FILES:
    Read(file_path=".claude/skills/spec-driven-cc-guide/{file}")
```

For subdirectory domains (prompt-engineering, skills-spec), load the most relevant files based on $QUESTION keywords rather than all files:

```
IF domain == "prompt-engineering":
    # Load overview first, then specific topic files
    Read(file_path=".claude/skills/spec-driven-cc-guide/references/prompt-engineering/overview.md")
    # Then load 1-2 specific files matching $QUESTION keywords

IF domain == "skills-spec":
    # Load overview first, then specific topic files
    Read(file_path=".claude/skills/spec-driven-cc-guide/references/skills/overview.md")
    # Then load 1-2 specific files matching $QUESTION keywords
```

**VERIFY:**
Each Read() returned non-empty content. Extract and note the key sections relevant to $QUESTION for use in Phase 03.

```
$LOADED_REFERENCES_COUNT = count of successfully loaded files
```

IF any Read() returned empty content: Log warning but continue if other files loaded successfully.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=02 --step=2.2 --project-root=.
```

---

### Step 2.3: Load Supplemental Assets (if applicable)

**EXECUTE:**
If $DOMAINS contains "reference" (user asking about shortcuts, command lists, cheat sheets, or feature comparisons):

```
Read(file_path=".claude/skills/spec-driven-cc-guide/assets/quick-reference.md")
Read(file_path=".claude/skills/spec-driven-cc-guide/assets/comparison-matrix.md")
```

If $DOMAINS does NOT contain "reference": Skip this step (note: this is an allowed skip because the step is explicitly conditional).

**VERIFY:**
If "reference" domain active: Both asset files loaded with non-empty content.
If "reference" domain not active: Step marked as "not-applicable".

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=02 --step=2.3 --project-root=.
```

---

### Step 2.4: Verify Minimum Content Threshold

**EXECUTE:**
Confirm that at least one reference file was successfully read into context. This is the final gate before answer synthesis.

```
IF $LOADED_REFERENCES_COUNT >= 1:
    Display: "{$LOADED_REFERENCES_COUNT} reference file(s) loaded successfully"
ELSE:
    HALT: "No reference files loaded. Cannot synthesize answer without authoritative content."
```

**VERIFY:**
$LOADED_REFERENCES_COUNT >= 1. Answer synthesis in Phase 03 will use ONLY content from loaded reference files — not from SKILL.md summaries or general knowledge.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=02 --step=2.4 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=cc-guide --phase=02 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 02 complete | Proceed to Phase 03 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 03 |

**Phase 02 Summary:**
- $LOADED_REFERENCES_COUNT: {value}
- Files loaded: {list}
- Supplemental assets loaded: {yes/no/not-applicable}
