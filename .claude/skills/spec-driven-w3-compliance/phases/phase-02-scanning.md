# Phase 02: Scanning

## Entry Gate

```bash
devforgeai-validate phase-check W3-AUDIT --workflow=w3-compliance --from=01 --to=02 --project-root=.
# Exit 0: proceed | Exit 1: HALT (Phase 01 not complete)
```

## Contract

PURPOSE: Execute all 4 W3 violation scans (CRITICAL, HIGH, MEDIUM, INFO) with exact Grep patterns, apply exclusion filters, and collect violation counts.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: $CRITICAL_COUNT, $HIGH_COUNT, $MEDIUM_COUNT, $subagent_violations, $skill_violations, $missing_w3_notes, $language_patterns
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 2.1: Load Scanning References [MANDATORY]

EXECUTE: Load scanning patterns and W3 rules reference files from disk. Do NOT rely on memory of previous reads.
```
Read(file_path="src/claude/skills/spec-driven-w3-compliance/references/scanning-patterns.md")
Read(file_path="src/claude/skills/spec-driven-w3-compliance/references/w3-rules.md")

IF any Read fails:
    HALT -- "Phase reference files not loaded. Cannot proceed."
    Do NOT rely on memory of previous reads. Load ALL references fresh.
```
VERIFY: Both reference files are loaded into context. Content from scanning-patterns.md includes Grep patterns. Content from w3-rules.md includes violation categories.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=02 --step=2.1 --project-root=.`

---

### Step 2.2: CRITICAL Scan - Subagent Skill Invocations

EXECUTE: Scan all subagent files for forbidden Skill() invocations. Subagents CANNOT invoke skills per architecture-constraints.md.
```
subagent_violations = Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/agents/',
    glob='*.md',
    output_mode='content',
    -n=true
)

# Exclude backup and template files from results
# Filter out any results from files matching: *.backup*, *.original*
filtered_subagent_violations = []
FOR result in subagent_violations:
    IF result.file does NOT contain ".backup" AND result.file does NOT contain ".original":
        filtered_subagent_violations.append(result)

subagent_violations = filtered_subagent_violations
CRITICAL_COUNT = count(subagent_violations)

Display: "CRITICAL scan complete: {CRITICAL_COUNT} subagent Skill() invocations found"
```
VERIFY: $CRITICAL_COUNT is set to an integer >= 0. $subagent_violations list is populated (may be empty if no violations).
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=02 --step=2.2 --project-root=.`

---

### Step 2.3: HIGH Scan - Non-Orchestration Skill Auto-Chaining

EXECUTE: Scan all skill files for Skill() invocations that lack user approval gates. Only devforgeai-orchestration may coordinate skills freely.
```
skill_violations_raw = Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/skills/',
    glob='*.md',
    output_mode='content',
    -n=true
)

# Exclude legitimate orchestration and backup files
skill_violations = []
FOR result in skill_violations_raw:
    IF result.file contains "devforgeai-orchestration/":
        SKIP  # Legitimate skill coordinator
    ELIF result.file contains ".backup":
        SKIP  # Historical files
    ELIF result.file contains ".original":
        SKIP  # Template files
    ELIF result.file contains ".md.bak":
        SKIP  # Editor backups
    ELSE:
        skill_violations.append(result)

# For each remaining violation, check if it has a user approval gate
# A user approval gate is: AskUserQuestion appearing before the Skill() call
# OR the Skill() call is in a "display-only" / "recommendation" context
filtered_skill_violations = []
FOR violation in skill_violations:
    file_content = Read(file_path=violation.file)

    # Check for user approval pattern before the Skill() line
    has_approval = file_content contains "AskUserQuestion" before violation.line

    # Check for display-only recommendation pattern
    is_display_only = file_content contains "display-only" OR "Recommended Next Action"

    IF NOT has_approval AND NOT is_display_only:
        filtered_skill_violations.append(violation)

skill_violations = filtered_skill_violations
HIGH_COUNT = count(skill_violations)

Display: "HIGH scan complete: {HIGH_COUNT} unauthorized auto-chaining violations found"
```
VERIFY: $HIGH_COUNT is set to an integer >= 0. $skill_violations list is populated (may be empty if no violations).
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=02 --step=2.3 --project-root=.`

---

### Step 2.4: MEDIUM Scan - Missing W3 Compliance Documentation

EXECUTE: Find all files with Skill() calls that lack W3 compliance notes.
```
files_with_skill_calls = Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/skills/',
    glob='*.md',
    output_mode='files_with_matches'
)

# Exclude orchestration (legitimate coordinator)
filtered_files = []
FOR file in files_with_skill_calls:
    IF file does NOT contain "devforgeai-orchestration/":
        filtered_files.append(file)

# Check each file for W3 compliance documentation
missing_w3_notes = []
FOR file in filtered_files:
    content = Read(file_path=file)
    IF "W3" NOT IN content AND "display-only" NOT IN content:
        missing_w3_notes.append(file)

MEDIUM_COUNT = count(missing_w3_notes)

Display: "MEDIUM scan complete: {MEDIUM_COUNT} files missing W3 compliance notes"
```
VERIFY: $MEDIUM_COUNT is set to an integer >= 0. $missing_w3_notes list is populated (may be empty).
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=02 --step=2.4 --project-root=.`

---

### Step 2.5: INFO Scan - Auto-Invoke Language Patterns

EXECUTE: Scan for language patterns that suggest auto-invocation intent.
```
language_patterns = Grep(
    pattern='(auto.*invoke|then invoke|invoking.*skill|automatically)',
    path='.claude/',
    glob='*.md',
    -i=true,
    output_mode='content',
    -n=true
)

# Filter to only concerning patterns
# Exclude: documentation files, README, changelog, archive folders
filtered_patterns = []
FOR result in language_patterns:
    IF result.file contains "README" OR result.file contains "CHANGELOG":
        SKIP  # Documentation
    ELIF result.file contains ".archive":
        SKIP  # Archived files
    ELIF result.file contains "backup":
        SKIP  # Backup files
    ELSE:
        filtered_patterns.append(result)

INFO_COUNT = count(filtered_patterns)

IF $MODE == "verbose":
    Display: "INFO scan complete: {INFO_COUNT} auto-invoke language patterns found"
    FOR p in filtered_patterns:
        Display: "  {p.file}:{p.line}: {p.content}"
ELSE:
    Display: "INFO scan complete: {INFO_COUNT} patterns found (use --verbose for details)"
```
VERIFY: $INFO_COUNT is set to an integer >= 0. Scan completed without errors.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=02 --step=2.5 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete W3-AUDIT --workflow=w3-compliance --phase=02 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 03 | Exit 1: HALT
```

## Phase 02 Completion Display

```
Phase 02 Complete: Scanning
  CRITICAL: ${CRITICAL_COUNT} violations
  HIGH: ${HIGH_COUNT} violations
  MEDIUM: ${MEDIUM_COUNT} violations
  INFO: ${INFO_COUNT} patterns
```
