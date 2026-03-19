---
description: Apply automated and guided fixes to story/epic files using validate-stories audit findings
argument-hint: "[AUDIT-FILE-PATH | STORY-NNN | EPIC-NNN] [--dry-run] [--finding=F-NNN] [--auto-only]"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill
execution-mode: immediate
---

# /fix-story - Fix Story and Epic Files from Audit Findings

Apply automated and guided fixes to story, epic, and context files based on structured audit findings from `/validate-stories`.

Do not skip any phases nor skip the spec-driven-remediation skill.

---

## Quick Reference

```bash
# Fix from audit file (most common)
/fix-story devforgeai/qa/audit/custody-chain-audit-stories-413-424.md

# Dry run — preview changes without modifying files
/fix-story devforgeai/qa/audit/custody-chain-audit-stories-413-424.md --dry-run

# Fix only automated (safe) findings
/fix-story devforgeai/qa/audit/custody-chain-audit-stories-413-424.md --auto-only

# Fix a single finding
/fix-story devforgeai/qa/audit/custody-chain-audit-stories-413-424.md --finding=F-002

# Find audit file by story ID
/fix-story STORY-414

# Find audit file by epic ID
/fix-story EPIC-066
```

---

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT parse findings from audit file
- ❌ DO NOT classify or triage findings
- ❌ DO NOT apply any edits to any files
- ❌ DO NOT prompt user for fix choices
- ❌ NEVER perform fix logic, verification, or reporting

**DO (command responsibilities only):**
- ✅ MUST validate input format (audit path OR story/epic ID)
- ✅ MUST resolve audit file path
- ✅ MUST set context markers for the skill
- ✅ MUST invoke skill immediately after validation

---

## Phase 0: Plan Mode Detection + Argument Validation

### Step 0.0: Plan Mode Auto-Exit [execution-mode: immediate]

```
IF plan mode is active:
    Display: "Note: /fix-story is an execution command. Exiting plan mode automatically."
    ExitPlanMode()
```

### Step 0.1: Validate Project Root [MANDATORY]

```
result = Read(file_path="CLAUDE.md")
IF result.success AND content_contains("DevForgeAI"):
    Display: "✓ Project root validated"
ELSE:
    HALT: Use AskUserQuestion to get correct path
```

### Step 0.2: Parse Arguments

```
AUDIT_FILE = null
INPUT_MODE = null
DRY_RUN = false
AUTO_ONLY = false
FINDING_FILTER = "all"

FOR arg in $ARGUMENTS:
    IF arg matches "--dry-run":
        DRY_RUN = true
    ELIF arg matches "--auto-only":
        AUTO_ONLY = true
    ELIF arg matches "--finding=F-\d+":
        FINDING_FILTER = extract F-NNN from arg
    ELIF arg ends with ".md" AND contains "audit" or "custody-chain":
        INPUT_MODE = "audit_file"
        AUDIT_FILE = arg
    ELIF arg matches "STORY-\d+":
        INPUT_MODE = "story_id"
        STORY_ID = arg
    ELIF arg matches "EPIC-\d+":
        INPUT_MODE = "epic_id"
        EPIC_ID = arg

IF INPUT_MODE is null:
    AskUserQuestion:
        Question: "Provide an audit file path, story ID, or epic ID"
        Header: "Input"
        Options:
            - label: "I have an audit file path"
              description: "Path to custody-chain-audit-*.md file"
            - label: "I have a story ID"
              description: "STORY-NNN — will search for matching audit file"
            - label: "I have an epic ID"
              description: "EPIC-NNN — will search for matching audit file"
```

### Step 0.3: Resolve Audit File Path

```
IF INPUT_MODE == "audit_file":
    result = Read(file_path=AUDIT_FILE)
    IF NOT result contains "## 4. Findings Detail":
        HALT: "File does not contain audit findings. Expected '## 4. Findings Detail' section."

ELIF INPUT_MODE == "story_id":
    # Search for audit file containing this story
    candidates = Glob(pattern="devforgeai/qa/audit/custody-chain-audit-*.md")
    FOR each candidate:
        content = Grep(pattern=STORY_ID, path=candidate)
        IF match:
            AUDIT_FILE = candidate
            BREAK
    IF AUDIT_FILE is null:
        HALT: "No audit file found containing {STORY_ID}. Run /validate-stories {STORY_ID} --chain first."

ELIF INPUT_MODE == "epic_id":
    candidates = Glob(pattern="devforgeai/qa/audit/custody-chain-audit-*.md")
    FOR each candidate:
        content = Grep(pattern=EPIC_ID, path=candidate)
        IF match:
            AUDIT_FILE = candidate
            BREAK
    IF AUDIT_FILE is null:
        HALT: "No audit file found for {EPIC_ID}. Run /validate-stories {EPIC_ID} first."
```

### Step 0.4: Set Context Markers

```
Display context markers for skill consumption:

**Fix Mode:** {INPUT_MODE}
**Audit File:** {AUDIT_FILE}
**Dry Run:** {DRY_RUN}
**Auto Only:** {AUTO_ONLY}
**Finding Filter:** {FINDING_FILTER}
```

---

## Phase 1: Invoke Skill

```
Skill(command="spec-driven-remediation")
```

**Skill handles ALL workflow** including finding parsing, classification, fix execution, verification, and reporting.

---

## Phase 2: Display Results

Display the fix report output from the skill. No additional processing.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Audit file not found | Run `/validate-stories` first to generate audit file |
| No findings in audit | Audit file exists but has 0 findings — nothing to fix |
| Skill not found | Check `.claude/skills/spec-driven-remediation/SKILL.md` exists |
| Finding filter no match | Specified `--finding=F-NNN` not found in audit |

---

## Integration

| Related Command | Relationship |
|----------------|-------------|
| `/validate-stories` | Produces the audit files that `/fix-story` consumes |
| `/create-story` | May be needed if fix requires creating new stories |
| `/qa` | Run after fixes to validate story quality |

---

## References

- Skill: `.claude/skills/spec-driven-remediation/SKILL.md`
- Audit output: `devforgeai/qa/audit/custody-chain-audit-{scope}.md`
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
